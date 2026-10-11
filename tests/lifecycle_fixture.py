"""Small scripted providers and read-only exports for the M3 lifecycle gate.

The bundle uses ordinary manifests/worker SQLite files. Everything exported here
is derived; evaluator previews never enter a provider or scheduling decision.
"""

from contextlib import ExitStack
from dataclasses import asdict
from functools import cache, partial
import json
from pathlib import Path
from time import sleep

from recovery.accounting import progress_snapshot
from recovery.manifests import load_schedules
from recovery.rounds import deserialize_state, snapshot_bytes
from recovery.runner import WorkerReader
from recovery.schedule import prepare_schedules
from recovery.storage import RecordedFailure, record_json
from recovery.tasks import Size
from tests.attempt_checks import append_trace
from tests.event_checks import event_provider, population
from tests.replay_checks import SETTINGS, replay_provider
from tests.round_checks import TOKENIZER, raw_reply, reply

BOUNDS = dict(timeout_seconds=8, termination_seconds=0.25, heartbeat_seconds=0.05)
EXHAUSTED_REASON = ("two infrastructure attempts interrupted: "
                    "preceding exclusive worker owner interrupted before durable response")
ROOT = Path(__file__).resolve().parent.parent


@cache
def schedules(size):
    saved = ROOT / "tests/fixtures/schedules_target.json"
    return (load_schedules(saved, population(size)) if size is Size.TARGET
            else prepare_schedules(population(size)))


def tiny(size):
    worlds = tuple(w for w in population(size).main if w.index == 1)
    ids = {w.world_id for w in worlds}
    return worlds, tuple(b for b in schedules(size).main if b.world_id in ids)


def tokenizer_factory():
    return TOKENIZER


def provider_factory(trace=None, mode="normal", timeout=8):
    return partial(provide, trace=trace, mode=mode, timeout=timeout)


def provide(view, rendered, tokenized, *, seed, settings, trace=None, mode="normal", timeout=8,
            tokenizer=TOKENIZER):
    # Only permitted inputs influence scripted replies. No world or gold access.
    if trace:
        append_trace(trace, {"event": "generation", "seed": seed, "settings": settings,
            "view": asdict(view), "rendered": asdict(rendered), "tokenized": asdict(tokenized)})
    if view.slot.phase == "control":
        raw = reply(tokenizer, view)
    elif view.slot.phase == "prefix":
        raw = event_provider(tokenizer)(view, rendered, tokenized)
    elif view.slot.round_number == 2 and view.peer == 0 and mode == "hang":
        while True:
            sleep(0.05)
    elif view.slot.round_number == 2 and view.peer == 0 and mode == "timeout":
        raw = RecordedFailure("timeout", f"known {timeout:g}-second attempt deadline")
    elif view.slot.round_number == 2 and view.peer == 0 and mode == "exhausted":
        raw = RecordedFailure("infrastructure_failure", EXHAUSTED_REASON)
    elif view.slot.round_number == 2 and view.peer == 1:
        raw = raw_reply(tokenizer, "{invalid lifecycle literal \ud800")
    elif view.slot.round_number == 1 and view.peer == 3:
        raw = RecordedFailure("timeout", "scripted known timeout outcome")
    else:
        raw = replay_provider(tokenizer, "unicode")(view, rendered, tokenized, seed=seed, settings=settings)
    if raw is None:
        raw = RecordedFailure("infrastructure_failure", "provider recorded an exhausted failed slot")
    if trace:
        append_trace(trace, {"event": "returned", "slot": asdict(view.slot), "peer": view.peer,
                             "response": asdict(raw)})
    return raw


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as output:
        output.write(record_json(value) + "\n")


def scientific_records(paths):
    """Compare every literal input/outcome and committed transition, sans clocks.

    Saver channel values exclude pending node writes. Checkpoint IDs/timestamps,
    placement, attempts and allocation are operational evidence, not peer state.
    """
    calls, inputs, states = [], [], []
    for path in paths:
        reader = WorkerReader(path)
        try:
            db = reader.store.connection
            calls.extend(dict(r) for r in db.execute("SELECT * FROM calls ORDER BY call_id"))
            inputs.extend(dict(r) for r in db.execute("SELECT * FROM round_inputs ORDER BY branch_id,round_number"))
            for (branch_id,) in db.execute("SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id"):
                for saved in reader.saver.list({"configurable": {"thread_id": branch_id}}):
                    values = saved.checkpoint["channel_values"]
                    if "committed" in values:
                        state = deserialize_state(values["committed"])
                        states.append(snapshot_bytes(state).decode("utf-8"))
        finally:
            reader.close()
    return {"calls": sorted(calls, key=lambda r: r["call_id"]),
            "round_inputs": sorted(inputs, key=lambda r: (r["branch_id"], r["round_number"])),
            "committed_transitions": sorted(set(states))}


def stable_progress(snapshot):
    return {"counts": {k: v for k, v in snapshot["counts"].items()
                       if k not in ("attempts", "retries", "uncertain_attempts")},
            "slots": [{k: v for k, v in r.items() if k not in ("worker", "cost")}
                      for r in snapshot["logical_slots"]],
            "delivery_counts": snapshot["delivery_counts"],
            "deliveries": sorted(snapshot["validated_deliveries"], key=lambda d: d["delivery_id"]),
            "matched_comparisons": snapshot["matched_comparisons"]}


def offline_preview(worlds, branches, paths):
    """Minimal independent replay of slot outcomes/footprints, not M4 estimands."""
    from recovery.truth import changed_coordinates, exact_candidate, solve_world
    from recovery.evaluate import candidate_payload
    records = {r["call_id"]: r for r in scientific_records(paths)["calls"]}
    by_world = {w.world_id: w for w in worlds}
    outcomes, footprints = [], []
    for branch in branches:
        world = by_world[branch.world_id]
        old = solve_world(world.world)
        truth = old if branch.event == "original" else solve_world(world.event_world(branch.event))
        changed = changed_coordinates(old, truth)
        footprints.append({"branch_id": branch.branch_id, "D": sorted(changed.changed), "U": sorted(changed.unchanged)})
        for call in branch.calls:
            row = records.get(call.call_id)
            validation = json.loads(row["validation_json"]) if row and row["validation_json"] else None
            candidate = validation["candidate"] if validation else None
            outcomes.append({"call_id": call.call_id, "generation_id": call.generation_id,
                "status": row["status"] if row else "unexecuted",
                "protocol_outcome": candidate["status"] if candidate else None,
                "correct": exact_candidate(truth, candidate_payload(truth.task, truth.size, call.peer, candidate), call.peer,
                    protocol_valid=candidate["status"] == "valid") if candidate else None})
    return {"kind": "offline CPU correctness/footprint preview; not empirical results or M4 analysis",
            "outcomes": outcomes, "footprints": footprints}


def backup_workers(paths, destinations):
    # SQLite backup includes committed WAL. Raw copying a live .sqlite is unsafe.
    with ExitStack() as stack:
        for source, destination in zip(paths, destinations):
            reader = WorkerReader(source)
            stack.callback(reader.close)
            reader.store.backup(destination)


def progress(worlds, branches, paths, **kwargs):
    return progress_snapshot(worlds, branches, paths, **kwargs)
