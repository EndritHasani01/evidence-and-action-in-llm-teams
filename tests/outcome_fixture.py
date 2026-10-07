"""Saved-record fixtures for offline tests; gold is used only by this evaluator fixture."""

from dataclasses import asdict
from functools import cache
import json
from pathlib import Path
import sqlite3

from recovery.manifests import load_population, load_schedules
from recovery.truth import solve_world
from recovery.tasks import Task

ROOT = Path(__file__).resolve().parent.parent


@cache
def prepared(size="target"):
    population = load_population(ROOT / f"tests/fixtures/population_{size}.json")
    schedules = load_schedules(ROOT / f"tests/fixtures/schedules_{size}.json", population)
    return population, schedules


def selection(task=Task.DIFFERENCE, policies=("B",), size="target"):
    population, schedules = prepared(size)
    world = next(w for w in population.main if w.world.task is task and w.index == 1)
    branches = tuple(b for b in schedules.main if b.world_id == world.world_id
        and (b.phase == "prefix" or b.phase == "continuation" and b.event == "revision"
             and b.policy in policies and b.replicate == 0))
    return (world,), branches


def saved_records(worlds, branches):
    by_world = {w.world_id: w for w in worlds}
    records, inputs, attempts = {}, {}, []
    for branch in branches:
        prepared_world = by_world[branch.world_id]
        truth = solve_world(prepared_world.world if branch.phase == "prefix" else prepared_world.event_world(branch.event))
        for number in sorted({c.round_number for c in branch.calls}):
            current = prepared_world.event_world(branch.event) if branch.phase == "continuation" else prepared_world.world
            sources = [asdict(s) for s in current.records]
            deliveries = [{"delivery_id": f"{branch.branch_id}/host/p{i}/{s['record_id']}/v{s['version']}",
                "recipient": i, "source": s, "origin": "host", "first_usable": {"phase": "recovery", "round_number": 1}}
                for s in sources if s["version"] == 2 for i in range(4)]
            state = {"branch_id": branch.branch_id, "phase": "prefix" if branch.phase == "prefix" else "recovery",
                "task": branch.task.value, "size": truth.size.value, "manifest": [],
                "peers": [{"sources": sources} for _ in range(4)], "deliveries": deliveries}
            inputs[branch.branch_id, number] = {"branch_id": branch.branch_id, "round_number": number,
                "worker": 0, "worker_file": "worker.sqlite", "branch_json": encode(asdict(branch)),
                "settings_json": "{}", "requests": {"before": json.dumps(state),
                "slot": {"phase": state["phase"], "round_number": number},
                "rendered": [{"text": f"peer {i} round {number}"} for i in range(4)],
                "tokenized": [{"input_ids": [i, number]} for i in range(4)]}}
        for call in branch.calls:
            answer = truth.candidate(call.peer)
            value = ([[str(j), answer[str(j)]] for j in range(truth.size.node_count)]
                     if branch.task is Task.BFS else answer)
            raw = {"text": json.dumps({"candidate": answer, "send": []}), "token_ids": [1],
                   "termination": "fixture", "truncated": False}
            candidate = {"status": "valid", "slot": {"phase": "prefix" if branch.phase == "prefix" else "recovery",
                         "round_number": call.round_number}, "value": value, "historical": False}
            validation = {"generated": raw, "json_valid": True, "schema_valid": True,
                "permissions_valid": True, "candidate": candidate}
            records[call.call_id] = {"call_id": call.call_id, "branch_id": branch.branch_id,
                "round_number": call.round_number, "peer": call.peer, "seed": call.seed,
                "generation_id": call.generation_id, "replay_parent": call.replay_parent,
                "status": "completed", "raw_json": encode(raw), "failure_json": None,
                "validation_json": encode(validation), "worker": 0, "worker_file": "worker.sqlite"}
            if not call.replay_parent:
                attempts.append({"call_id": call.call_id, "number": 1, "status": "completed",
                                 "uncertain_completion": 0, "worker": 0, "worker_file": "worker.sqlite"})
    for branch in branches:
        for call in branch.calls:
            if call.replay_parent:
                row = records[call.call_id]
                row.update(status="replay", raw_json=None, validation_json=records[call.replay_parent]["validation_json"])
    return records, inputs, attempts


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":"))


def write_worker(path, records, inputs, attempts):
    """Minimal application-ledger schema; real M3 databases are tested separately."""
    con = sqlite3.connect(path)
    try:
        con.executescript("""
            CREATE TABLE calls (call_id TEXT PRIMARY KEY, branch_id TEXT, round_number INTEGER,
                peer INTEGER, seed INTEGER, generation_id TEXT, replay_parent TEXT, status TEXT,
                raw_json TEXT, failure_json TEXT, validation_json TEXT);
            CREATE TABLE round_inputs (branch_id TEXT, round_number INTEGER, branch_json TEXT,
                settings_json TEXT, requests_json TEXT, PRIMARY KEY(branch_id,round_number));
            CREATE TABLE attempts (call_id TEXT, number INTEGER, status TEXT, uncertain_completion INTEGER);
            CREATE TABLE run_inputs (singleton INTEGER PRIMARY KEY, inputs_json TEXT);
        """)
        for r in records.values():
            con.execute("INSERT INTO calls VALUES (?,?,?,?,?,?,?,?,?,?,?)", tuple(r[k] for k in
                ("call_id", "branch_id", "round_number", "peer", "seed", "generation_id", "replay_parent",
                 "status", "raw_json", "failure_json", "validation_json")))
        for r in inputs.values():
            con.execute("INSERT INTO round_inputs VALUES (?,?,?,?,?)", (r["branch_id"], r["round_number"],
                r["branch_json"], r["settings_json"], encode(r["requests"])))
        con.executemany("INSERT INTO attempts VALUES (?,?,?,?)", [tuple(r[k] for k in
            ("call_id", "number", "status", "uncertain_completion")) for r in attempts])
        con.commit()
    finally:
        con.close()
