"""Worker-local raw calls and pre-delivery inputs (spec §9).

Checkpoints, owned by runner.py, are the sole delivery/peer-state authority.
These ordinary SQLite transactions never span inference or use saver internals.
One worker serially owns a file; process bounds belong to attempts.py.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from math import isfinite
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


def connect(path: Path, *, readonly=False) -> sqlite3.Connection:
    location = Path(path).resolve().as_uri() + "?mode=ro" if readonly else str(path)
    connection = sqlite3.connect(location, uri=readonly, check_same_thread=False, timeout=30)
    try:
        connection.row_factory = sqlite3.Row
        if readonly:
            connection.execute("PRAGMA query_only=ON")
        else:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA foreign_keys=ON")
        if (connection.execute("PRAGMA journal_mode").fetchone()[0] != "wal"
                or not readonly and connection.execute("PRAGMA synchronous").fetchone()[0] != 2):
            raise ValueError("worker database requires on-disk WAL/FULL durability")
    except BaseException:
        connection.close()
        raise
    return connection


@dataclass(frozen=True, slots=True)
class RecordedFailure:
    """Final known outcome, never a missing/unexecuted call or retry request.

    Attempt termination and exhaustion are established by the process controller.
    Detail remains host-only.
    """

    status: str
    reason: str

    def __post_init__(self):
        if (type(self.status) is not str or self.status not in ("timeout", "infrastructure_failure")
                or type(self.reason) is not str or not self.reason):
            raise ValueError("record a timeout or exhausted infrastructure failure")


class UnresolvedAttempt(RuntimeError):
    """No durable response: establish worker interruption before any retry."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def seconds(value: float) -> float:
    if type(value) not in (int, float) or not isfinite(value) or value < 0:
        raise ValueError("timing must be finite and nonnegative")
    return float(value)


class WorkerStore:
    def __init__(self, path: Path, *, readonly=False, parents=()):
        self.path = Path(path).resolve()
        self.parents = tuple(parents)
        self.connection = connect(self.path, readonly=readonly)
        if readonly:
            return
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
            CREATE TABLE IF NOT EXISTS provider_processes (
                call_id TEXT NOT NULL, number INTEGER NOT NULL,
                pid INTEGER NOT NULL, started_at TEXT NOT NULL,
                ready_at TEXT, last_observed_at TEXT NOT NULL,
                stopped_at TEXT, recovered_at TEXT, termination_reason TEXT,
                uncertain_stop INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (call_id, number),
                FOREIGN KEY (call_id, number) REFERENCES attempts(call_id, number)
            );
            CREATE TABLE IF NOT EXISTS run_inputs (
                singleton INTEGER PRIMARY KEY CHECK (singleton=1), inputs_json TEXT NOT NULL
            );
        """)
        # Reopen T01 worker files without replacing their calls/checkpoints.
        columns = {r[1] for r in self.connection.execute("PRAGMA table_info(attempts)")}
        with self.connection:
            for name, definition in (
                ("timeout_seconds", "REAL"), ("termination_seconds", "REAL"),
                ("observed_seconds", "REAL NOT NULL DEFAULT 0"),
                ("termination_reason", "TEXT"), ("reason", "TEXT"),
                ("recovered_at", "TEXT"), ("worker_pid", "INTEGER"),
            ):
                if name not in columns:
                    self.connection.execute(f"ALTER TABLE attempts ADD COLUMN {name} {definition}")

    def close(self):
        self.connection.close()

    def bind_run(self, worlds, branches, settings, bounds):
        """Reject restart input drift before admitting any new scheduled work.

        The same literal run inputs bind each worker file; placement/order are
        operational choices and do not change these scientific inputs.
        """
        payload = record_json({"worlds": [asdict(w) for w in sorted(worlds, key=lambda w: w.world_id)],
            "branches": [asdict(b) for b in sorted(branches, key=lambda b: b.branch_id)],
            "settings": json.loads(settings_json(settings)), "bounds": bounds})
        with self.connection:
            previous = self.connection.execute("SELECT inputs_json FROM run_inputs WHERE singleton=1").fetchone()
            if previous is not None and previous[0] != payload:
                raise ValueError("worker run inputs/settings/attempt bounds differ; resume the saved configuration")
            self.connection.execute("INSERT OR IGNORE INTO run_inputs VALUES (1,?)", (payload,))

    def _record(self, table, where, values):
        # Table/predicate are internal constants, never user-supplied SQL.
        matches = []
        for store in (self, *self.parents):
            row = store.connection.execute(f"SELECT * FROM {table} WHERE {where}", values).fetchone()
            if row is not None:
                matches.append((store, dict(row)))
        if len(matches) != 1:
            raise ValueError(f"{'missing' if not matches else 'duplicate'} saved {table} identity: {values}")
        return matches[0]

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
        return self._record("calls", "call_id=?", (call_id,))[1]

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

    def attempts(self, call_id: str) -> tuple[dict, ...]:
        store, _ = self._record("calls", "call_id=?", (call_id,))
        return tuple(dict(r) for r in store.connection.execute(
            "SELECT * FROM attempts WHERE call_id=? ORDER BY number", (call_id,)))

    def prepare_control(self, branch, settings, view, rendered, tokenized):
        call = branch.calls[0]
        payload = record_json({"view": asdict(view), "rendered": asdict(rendered), "tokenized": asdict(tokenized)})
        identity = record_json(asdict(branch))
        with self.connection:
            row = self.connection.execute("SELECT * FROM round_inputs WHERE branch_id=? AND round_number=1",
                                          (branch.branch_id,)).fetchone()
            if row is not None:
                if (row["branch_json"], row["settings_json"], row["requests_json"]) != (identity, settings, payload):
                    raise ValueError("saved control request/settings/branch equality failed")
                saved = self.call(call.call_id)
                if tuple(saved[k] for k in ("branch_id", "round_number", "peer", "seed", "generation_id", "replay_parent")) != (
                        branch.branch_id, 1, -1, call.seed, call.generation_id, None):
                    raise ValueError("saved control slot identity differs")
                return
            self.connection.execute("INSERT INTO round_inputs VALUES (?,1,?,?,?)",
                                    (branch.branch_id, identity, settings, payload))
            self.connection.execute("""INSERT INTO calls
                (call_id,branch_id,round_number,peer,seed,generation_id,status)
                VALUES (?, ?,1,-1,?,?,'pending')""", (call.call_id, branch.branch_id, call.seed, call.generation_id))

    def save_control_validation(self, call_id, reply):
        raw = self.response(call_id)
        if reply.generated != (raw if type(raw) is GeneratedReply else None):
            raise ValueError("control validation differs from durable outcome")
        encoded = record_json(asdict(reply))
        with self.connection:
            row = self.call(call_id)
            if row["validation_json"] is not None and row["validation_json"] != encoded:
                raise ValueError("control validation differs from recorded outcome")
            self.connection.execute("UPDATE calls SET validation_json=? WHERE call_id=?", (encoded, call_id))

    def begin_attempt(self, call_id: str, *, timeout_seconds=None, termination_seconds=None) -> int:
        for value in (timeout_seconds, termination_seconds):
            if value is not None and seconds(value) == 0:
                raise ValueError("attempt and termination bounds must be positive")
        with self.connection:
            row = self.call(call_id)
            if row["replay_parent"] is not None:
                raise ValueError("a replay cannot start physical inference")
            if row["status"] == "running":
                raise UnresolvedAttempt(f"unresolved attempt without a durable reply: {call_id}")
            if row["status"] != "pending":
                raise ValueError("only a pending physical call can start an attempt")
            previous = self.attempts(call_id)
            if previous and (len(previous) != 1 or previous[0]["status"] != "interrupted"):
                raise UnresolvedAttempt("only one established infrastructure interruption permits a retry")
            if previous and (previous[0]["timeout_seconds"], previous[0]["termination_seconds"]) != (
                    timeout_seconds, termination_seconds):
                raise ValueError("identical-request retry requires the original attempt bounds")
            number = len(previous) + 1
            self.connection.execute("""INSERT INTO attempts
                (call_id,number,status,started_at,timeout_seconds,termination_seconds)
                VALUES (?,?,'running',?,?,?)""",
                (call_id, number, utc_now(), timeout_seconds, termination_seconds))
            self.connection.execute("UPDATE calls SET status='running' WHERE call_id=?", (call_id,))
            return number

    def finish_attempt(self, call_id: str, response, elapsed_seconds: float, *, termination_reason=None):
        elapsed_seconds = seconds(elapsed_seconds)
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
            attempt = self.attempts(call_id)[-1]
            if attempt["status"] != "running":
                raise UnresolvedAttempt("a blocked attempt cannot commit an inferred outcome")
            self.connection.execute("UPDATE calls SET status=?,raw_json=?,failure_json=? WHERE call_id=?",
                                    (status, raw, failure, call_id))
            self.connection.execute("""UPDATE attempts SET status=?,finished_at=?,elapsed_seconds=?,
                observed_seconds=?,termination_reason=?,reason=? WHERE call_id=? AND number=?""",
                (status, utc_now(), elapsed_seconds, elapsed_seconds,
                 termination_reason or (response.termination if raw is not None else response.status),
                 response.reason if failure is not None else None, call_id, attempt["number"]))

    def interrupt_attempt(self, call_id: str, reason: str, *, elapsed_seconds=None,
                          termination_reason="worker_interruption"):
        """Only an absent durable outcome can authorize the single retry.

        After owner death, end time/duration are unknown. Keep observed work and
        recovery time separately; neither lost work nor its ambiguity is erased.
        """
        if type(reason) is not str or not reason:
            raise ValueError("interruption requires a concrete host-only reason")
        if elapsed_seconds is not None:
            elapsed_seconds = seconds(elapsed_seconds)
        with self.connection:
            row = self.call(call_id)
            if row["status"] in ("completed", "timeout", "infrastructure_failure", "replay"):
                return  # A durable outcome always wins, including a timeout.
            if row["status"] != "running":
                raise ValueError("interruption requires a running attempt")
            attempt = self.attempts(call_id)[-1]
            if attempt["status"] != "running":
                raise UnresolvedAttempt("diagnosed provider/protocol defects require repair, not retry")
            self.connection.execute("""UPDATE attempts SET status='interrupted',finished_at=?,
                elapsed_seconds=?,observed_seconds=MAX(observed_seconds,?),uncertain_completion=1,
                termination_reason=?,reason=?,recovered_at=? WHERE call_id=? AND number=?""",
                (utc_now() if elapsed_seconds is not None else None, elapsed_seconds,
                 elapsed_seconds or 0, termination_reason, reason,
                 utc_now() if elapsed_seconds is None else None, call_id, attempt["number"]))
            self.connection.execute("""UPDATE provider_processes SET uncertain_stop=1,
                recovered_at=?,termination_reason=? WHERE stopped_at IS NULL
                AND recovered_at IS NULL""", (utc_now(), termination_reason))
            if attempt["number"] == 2:
                failure = RecordedFailure("infrastructure_failure", "two infrastructure attempts interrupted: " + reason)
                self.connection.execute("UPDATE calls SET status=?,failure_json=? WHERE call_id=?",
                                        (failure.status, record_json(asdict(failure)), call_id))
            else:
                self.connection.execute("UPDATE calls SET status='pending' WHERE call_id=?", (call_id,))

    def block_attempt(self, call_id: str, reason: str, elapsed_seconds: float):
        """A diagnosed adapter/protocol defect stops; it is not a new sample."""
        with self.connection:
            attempt = self.attempts(call_id)[-1]
            if self.call(call_id)["status"] != "running" or attempt["status"] != "running":
                raise UnresolvedAttempt("defect requires its active attempt")
            self.connection.execute("""UPDATE attempts SET status='blocked',finished_at=?,
                elapsed_seconds=?,reason=?,termination_reason='provider_defect',uncertain_completion=1
                WHERE call_id=? AND number=?""",
                (utc_now(), seconds(elapsed_seconds), reason, call_id, attempt["number"]))

    def confirm_timeout_termination(self, call_id: str, elapsed_seconds: float):
        with self.connection:
            self.connection.execute("""UPDATE attempts SET elapsed_seconds=?,observed_seconds=?,
                finished_at=?,termination_reason='attempt_timeout' WHERE call_id=?
                AND status='timeout' AND termination_reason='timeout_termination_pending'""",
                (seconds(elapsed_seconds), seconds(elapsed_seconds), utc_now(), call_id))

    def recover_processes(self):
        """A new exclusive owner preserves unobserved prior process stop times."""
        with self.connection:
            self.connection.execute("""UPDATE provider_processes SET uncertain_stop=1,
                recovered_at=?,termination_reason='owner_interruption' WHERE stopped_at IS NULL
                AND recovered_at IS NULL""", (utc_now(),))

    def process_started(self, call_id: str, number: int, pid: int):
        now = utc_now()
        with self.connection:
            self.connection.execute("INSERT INTO provider_processes (call_id,number,pid,started_at,last_observed_at) VALUES (?,?,?,?,?)",
                                    (call_id, number, pid, now, now))

    def process_ready(self, call_id: str, number: int):
        with self.connection:
            self.connection.execute("UPDATE provider_processes SET ready_at=? WHERE call_id=? AND number=?",
                                    (utc_now(), call_id, number))

    def observe_attempt(self, call_id: str, number: int, elapsed_seconds: float, pid: int):
        with self.connection:
            self.connection.execute("UPDATE attempts SET observed_seconds=?,worker_pid=? WHERE call_id=? AND number=? AND status='running'",
                                    (seconds(elapsed_seconds), pid, call_id, number))
            self.connection.execute("UPDATE provider_processes SET last_observed_at=? WHERE pid=? AND stopped_at IS NULL AND recovered_at IS NULL",
                                    (utc_now(), pid))

    def process_stopped(self, call_id: str, number: int, reason: str):
        with self.connection:
            self.connection.execute("""UPDATE provider_processes SET stopped_at=?,termination_reason=?
                WHERE call_id=? AND number=? AND stopped_at IS NULL""", (utc_now(), reason, call_id, number))

    def inputs(self, branch_id: str, round_number: int):
        _, row = self._record("round_inputs", "branch_id=? AND round_number=?", (branch_id, round_number))
        branch = _branch(json.loads(row["branch_json"]))
        if branch.branch_id != branch_id:
            raise ValueError("saved barrier branch identity differs")
        calls = tuple(c for c in branch.calls if c.round_number == round_number)
        if len(calls) != 4 or tuple(c.peer for c in calls) != (0, 1, 2, 3):
            raise ValueError("saved barrier requires four ordered scheduled slots")
        for call in calls:
            saved_call = self.call(call.call_id)
            if tuple(saved_call[k] for k in ("branch_id", "round_number", "peer", "seed",
                                              "generation_id", "replay_parent")) != (
                    branch_id, round_number, call.peer, call.seed, call.generation_id, call.replay_parent):
                raise ValueError("saved call identity/seed/replay parent differs")
        data = json.loads(row["requests_json"])
        before = deserialize_state(data["before"].encode("utf-8"))
        slot = Slot(**data["slot"])
        if before.branch_id != branch_id or slot != before.next_slot or slot.round_number != round_number:
            raise ValueError("saved barrier differs from its pre-delivery state")
        views = tuple(p.view(before.task, before.size, i, slot, before.manifest)
                      for i, p in enumerate(before.peers))
        requests = RoundRequests(before, slot, views,
            tuple(RenderedRequest(**v) for v in data["rendered"]),
            tuple(TokenizedRequest(v["text"], tuple(v["input_ids"]), tuple(v["attention_mask"]))
                  for v in data["tokenized"]))
        return branch, row["settings_json"], requests

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
