"""Worker-local raw calls and pre-delivery inputs (spec §9).

Checkpoints, owned by runner.py, are the sole delivery/peer-state authority.
These ordinary SQLite transactions never span inference or use saver internals.
One worker serially owns a file; scheduling/attempt recovery belongs to M3-T02/03.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from .manifests import _branch
from .prompts import RenderedRequest, TokenizedRequest
from .protocol import GeneratedReply
from .replay import SavedRound
from .rounds import RoundRequests, deserialize_state, snapshot_bytes, validate_round
from .state import Slot


def record_json(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":"))


def settings_json(settings: dict) -> str:
    if type(settings) is not dict:
        raise ValueError("generation settings must be a complete JSON object")
    return record_json(settings)


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(path), check_same_thread=False, timeout=30)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA foreign_keys=ON")
        if (connection.execute("PRAGMA journal_mode").fetchone()[0] != "wal"
                or connection.execute("PRAGMA synchronous").fetchone()[0] != 2):
            raise ValueError("worker database requires on-disk WAL/FULL durability")
    except BaseException:
        connection.close()
        raise
    return connection


@dataclass(frozen=True, slots=True)
class RecordedFailure:
    """Final known outcome, never a missing/unexecuted call or retry request.

    Attempt termination and exhaustion must be established by the provider;
    M3-T02 supplies that bounded process boundary. Detail remains host-only.
    """

    status: str
    reason: str

    def __post_init__(self):
        if self.status not in ("timeout", "infrastructure_failure") or not self.reason:
            raise ValueError("record a timeout or exhausted infrastructure failure")


class UnresolvedAttempt(RuntimeError):
    """No durable response: M3-T02 must resolve interruption before any retry."""


class WorkerStore:
    def __init__(self, path: Path):
        self.path = Path(path).resolve()
        self.connection = connect(self.path)
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS round_inputs (
                branch_id TEXT NOT NULL, round_number INTEGER NOT NULL,
                branch_json TEXT NOT NULL, settings_json TEXT NOT NULL,
                requests_json TEXT NOT NULL,
                PRIMARY KEY (branch_id, round_number)
            );
            CREATE TABLE IF NOT EXISTS calls (
                call_id TEXT PRIMARY KEY, branch_id TEXT NOT NULL,
                round_number INTEGER NOT NULL, peer INTEGER NOT NULL,
                seed INTEGER NOT NULL, generation_id TEXT NOT NULL,
                replay_parent TEXT,
                status TEXT NOT NULL CHECK (status IN
                    ('pending','running','completed','timeout','infrastructure_failure','replay')),
                raw_json TEXT, failure_json TEXT, validation_json TEXT,
                FOREIGN KEY (branch_id, round_number)
                    REFERENCES round_inputs(branch_id, round_number),
                CHECK (NOT (raw_json IS NOT NULL AND failure_json IS NOT NULL))
            );
            CREATE TABLE IF NOT EXISTS attempts (
                call_id TEXT NOT NULL REFERENCES calls(call_id),
                number INTEGER NOT NULL CHECK (number BETWEEN 1 AND 2),
                status TEXT NOT NULL, started_at TEXT NOT NULL,
                finished_at TEXT, elapsed_seconds REAL,
                uncertain_completion INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (call_id, number)
            );
        """)

    def close(self):
        self.connection.close()

    def prepare(self, branch, settings: str, requests: RoundRequests):
        """Save the frozen barrier and all pending slots in one transaction."""
        r = requests.slot.round_number
        payload = record_json({
            "before": snapshot_bytes(requests.before).decode("utf-8"),
            "slot": asdict(requests.slot),
            "rendered": [asdict(v) for v in requests.rendered],
            "tokenized": [asdict(v) for v in requests.tokenized],
        })
        identity = record_json(asdict(branch))
        calls = tuple(c for c in branch.calls if c.round_number == r)
        with self.connection:
            previous = self.connection.execute(
                "SELECT * FROM round_inputs WHERE branch_id=? AND round_number=?",
                (branch.branch_id, r)).fetchone()
            if previous is not None:
                if (previous["branch_json"], previous["settings_json"], previous["requests_json"]) != (
                        identity, settings, payload):
                    raise ValueError("saved round request/settings/branch equality failed")
                for call in calls:
                    row = self.call(call.call_id)
                    expected = (branch.branch_id, r, call.peer, call.seed,
                                call.generation_id, call.replay_parent)
                    if tuple(row[k] for k in ("branch_id", "round_number", "peer", "seed",
                                              "generation_id", "replay_parent")) != expected:
                        raise ValueError("saved call identity differs from scheduled slot")
                return
            self.connection.execute("INSERT INTO round_inputs VALUES (?,?,?,?,?)",
                                    (branch.branch_id, r, identity, settings, payload))
            for call in calls:
                self.connection.execute("""INSERT INTO calls
                    (call_id,branch_id,round_number,peer,seed,generation_id,replay_parent,status)
                    VALUES (?,?,?,?,?,?,?,'pending')""",
                    (call.call_id, branch.branch_id, r, call.peer, call.seed,
                     call.generation_id, call.replay_parent))

    def call(self, call_id: str) -> dict:
        row = self.connection.execute("SELECT * FROM calls WHERE call_id=?", (call_id,)).fetchone()
        if row is None:
            raise ValueError(f"missing saved call: {call_id}")
        return dict(row)

    def response(self, call_id: str) -> GeneratedReply | RecordedFailure:
        row = self.call(call_id)
        if row["replay_parent"] is not None:
            if row["status"] != "replay":
                raise ValueError("logical replay has not been obtained")
            row = self.call(row["generation_id"])
            if row["replay_parent"] is not None:
                raise ValueError("replay parent must be an original physical generation")
        if row["status"] == "completed" and row["raw_json"] is not None:
            raw = json.loads(row["raw_json"])
            return GeneratedReply(**dict(raw, token_ids=tuple(raw["token_ids"])))
        if row["status"] in ("timeout", "infrastructure_failure") and row["failure_json"] is not None:
            return RecordedFailure(**json.loads(row["failure_json"]))
        raise ValueError("call has no durable completed response/failure")

    def begin_attempt(self, call_id: str):
        with self.connection:
            row = self.call(call_id)
            if row["replay_parent"] is not None:
                raise ValueError("a replay cannot start physical inference")
            if row["status"] == "running":
                raise UnresolvedAttempt(f"unresolved attempt without a durable reply: {call_id}")
            if row["status"] != "pending":
                raise ValueError("only a pending physical call can start an attempt")
            self.connection.execute("INSERT INTO attempts (call_id,number,status,started_at) VALUES (?,1,'running',?)",
                                    (call_id, datetime.now(timezone.utc).isoformat()))
            self.connection.execute("UPDATE calls SET status='running' WHERE call_id=?", (call_id,))

    def finish_attempt(self, call_id: str, response, elapsed_seconds: float):
        if response is None:
            response = RecordedFailure("infrastructure_failure", "provider recorded an exhausted failed slot")
        if type(response) not in (GeneratedReply, RecordedFailure):
            raise ValueError("provider must return exact generated output or a recorded failure")
        raw = record_json(asdict(response)) if type(response) is GeneratedReply else None
        failure = record_json(asdict(response)) if type(response) is RecordedFailure else None
        status = "completed" if raw is not None else response.status
        with self.connection:
            row = self.call(call_id)
            if row["status"] != "running":
                raise ValueError("response commit requires its active attempt")
            self.connection.execute("UPDATE calls SET status=?,raw_json=?,failure_json=? WHERE call_id=?",
                                    (status, raw, failure, call_id))
            self.connection.execute("""UPDATE attempts SET status=?,finished_at=?,elapsed_seconds=?
                WHERE call_id=? AND number=1""",
                (status, datetime.now(timezone.utc).isoformat(), elapsed_seconds, call_id))

    def inputs(self, branch_id: str, round_number: int):
        row = self.connection.execute("SELECT * FROM round_inputs WHERE branch_id=? AND round_number=?",
                                      (branch_id, round_number)).fetchone()
        if row is None:
            raise ValueError("missing saved pre-delivery barrier")
        data = json.loads(row["requests_json"])
        before = deserialize_state(data["before"].encode("utf-8"))
        slot = Slot(**data["slot"])
        if slot != before.next_slot:
            raise ValueError("saved barrier differs from its pre-delivery state")
        views = tuple(p.view(before.task, before.size, i, slot, before.manifest)
                      for i, p in enumerate(before.peers))
        requests = RoundRequests(before, slot, views,
            tuple(RenderedRequest(**v) for v in data["rendered"]),
            tuple(TokenizedRequest(v["text"], tuple(v["input_ids"]), tuple(v["attention_mask"]))
                  for v in data["tokenized"]))
        return _branch(json.loads(row["branch_json"])), row["settings_json"], requests

    def save_validation(self, branch, barrier):
        """Save deterministic outcomes only after every raw reply is durable."""
        calls = tuple(c for c in branch.calls if c.round_number == barrier.requests.slot.round_number)
        with self.connection:
            for call, reply in zip(calls, barrier.replies):
                row = self.call(call.call_id)
                if call.replay_parent is not None:
                    parent = self.response(call.replay_parent)
                    raw = parent if type(parent) is GeneratedReply else None
                    if reply.generated != raw:
                        raise ValueError("replay outcome differs from its durable generation")
                    if row["status"] not in ("pending", "replay"):
                        raise ValueError("replay slot acquired a physical attempt")
                    self.connection.execute("UPDATE calls SET status='replay' WHERE call_id=?", (call.call_id,))
                raw = self.response(call.call_id)
                if reply.generated != (raw if type(raw) is GeneratedReply else None):
                    raise ValueError("validation differs from the durable raw outcome")
                encoded = record_json(asdict(reply))
                if row["validation_json"] is not None and row["validation_json"] != encoded:
                    raise ValueError("saved validation outcome equality failed")
                self.connection.execute("UPDATE calls SET validation_json=? WHERE call_id=?", (encoded, call.call_id))

    def saved_round(self, branch_id: str, round_number: int, tokenizer) -> SavedRound:
        branch, settings, requests = self.inputs(branch_id, round_number)
        calls = tuple(c for c in branch.calls if c.round_number == round_number)
        generated = []
        for call in calls:
            row = self.call(call.call_id)
            if row["validation_json"] is None:
                raise ValueError("missing saved validation for pre-delivery parent")
            response = self.response(call.call_id)
            generated.append(response if type(response) is GeneratedReply else None)
        barrier = validate_round(requests, tuple(generated), tokenizer)
        for call, reply in zip(calls, barrier.replies):
            if self.call(call.call_id)["validation_json"] != record_json(asdict(reply)):
                raise ValueError("replayed validation differs from the recorded parent outcome")
        return SavedRound(branch, settings, barrier)

    def backup(self, destination: Path):
        destination = Path(destination).resolve()
        # Exclusive creation protects an existing experiment archive.
        with destination.open("xb"):
            pass
        target = sqlite3.connect(destination)
        try:
            self.connection.backup(target)
        finally:
            target.close()
