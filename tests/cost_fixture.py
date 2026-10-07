"""Hand-measured ordinary ledger fixtures; no providers or execution decisions."""

from datetime import datetime, timedelta, timezone
import json
import sqlite3

from recovery.tasks import Task
from tests.outcome_fixture import encode, saved_records, selection

BASE = datetime(2026, 10, 6, tzinfo=timezone.utc)


def clock(seconds):
    return (BASE + timedelta(seconds=seconds)).isoformat()


def fixture(task=Task.SORT, policies=("B", "C", "K", "F", "P_G", "Q_B", "Q_C")):
    worlds, branches = selection(task, policies)
    records, inputs, attempts = saved_records(worlds, branches)
    for row in records.values():
        row["request_tokens"] = 2
    for n, attempt in enumerate(attempts):
        attempt.update(elapsed_seconds=2, observed_seconds=2, started_at=clock(n * 2),
            finished_at=clock(n * 2 + 2), recovered_at=None, device="synthetic:0", peak_memory_bytes=1000)
    retried = next(c.call_id for b in branches if b.policy == "B" for c in b.calls
        if c.round_number == 1 and c.peer == worlds[0].partition[1][0]) if "B" in policies else None
    if retried:
        original = next(a for a in attempts if a["call_id"] == retried)
        original["number"] = 2
        attempts.append(dict(original, number=1, status="interrupted", uncertain_completion=1,
            elapsed_seconds=3, observed_seconds=3, started_at=clock(300), finished_at=clock(303)))
    if "C" in policies:
        failed = next(b for b in branches if b.policy == "C").calls[4].call_id
        row = records[failed]
        validation = json.loads(row["validation_json"])
        validation.update(generated=None, json_valid=False, schema_valid=False, permissions_valid=False)
        validation["candidate"].update(status="failed", value=None)
        row.update(status="timeout", raw_json=None, failure_json=encode({"status": "timeout", "reason": "fixture timeout"}),
                   validation_json=encode(validation))
        next(a for a in attempts if a["call_id"] == failed)["status"] = "timeout"
    return worlds, branches, records, inputs, sorted(attempts, key=lambda a: (a["call_id"], a["number"]))


def set_boundary(inputs, branches, sources_by_peer):
    for branch in branches:
        if branch.policy in ("B", "C", "K"):
            saved = inputs[branch.branch_id, 1]
            state = json.loads(saved["requests"]["before"])
            for peer, sources in zip(state["peers"], sources_by_peer):
                peer["sources"] = sources
            saved["requests"]["before"] = encode(state)


def write_cost_worker(path, records, inputs, attempts):
    from tests.outcome_fixture import write_worker
    write_worker(path, records, inputs, attempts)
    con = sqlite3.connect(path)
    try:
        con.execute("ALTER TABLE calls ADD COLUMN request_tokens INTEGER")
        fields = ("elapsed_seconds", "observed_seconds", "started_at", "finished_at", "recovered_at", "peak_memory_bytes")
        for name in fields:
            con.execute(f"ALTER TABLE attempts ADD COLUMN {name}")
        for cid, row in records.items():
            con.execute("UPDATE calls SET request_tokens=? WHERE call_id=?", (row.get("request_tokens"), cid))
        for a in attempts:
            con.execute("UPDATE attempts SET " + ",".join(name + "=?" for name in fields) + " WHERE call_id=? AND number=?",
                        (*[a[name] for name in fields], a["call_id"], a["number"]))
        con.commit()
    finally:
        con.close()
