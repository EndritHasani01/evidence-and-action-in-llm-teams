"""Derived resource/progress views; no inference, evaluator or progress store.

Attempt costs include loading/transport/termination inside the attempt. Outside
allocation overhead stays experiment overhead, never another physical call.
The allocation partition is a wall-clock reconciliation, not a second sum of
monotonic attempt durations. Hypothetical policies reuse original attempt costs.
"""

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

from .rounds import deserialize_state
from .runner import WorkerReader, DurableRunner
from .schedule import dependency_order
from .storage import record_json, seconds, settings_json, utc_now, WorkerStore
from .workers import scheduled_work


FINAL = {"completed", "timeout", "infrastructure_failure", "replay"}


def timestamp(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("resource clocks require an explicit timezone")
    return result.timestamp()


@dataclass(frozen=True)
class Budget:
    """Execution bounds supplied by the eventual accepted freeze, not authority.

    shutdown_seconds covers the whole controller/provider release operation.
    The provider release hook must be bounded and acknowledge actual release.
    Synthetic CPU tests explicitly label allocations as synthetic.
    """

    ceiling_gpu_hours: float = 100
    development_reserve_gpu_hours: float = 8
    setup_reserve_gpu_hours: float = 2
    interruption_reserve_gpu_hours: float = 2
    overhead_seconds: float = 0
    shutdown_seconds: float = 10
    allocation_mode: str = "gpu"

    def __post_init__(self):
        for name in ("ceiling_gpu_hours", "development_reserve_gpu_hours", "setup_reserve_gpu_hours",
                     "interruption_reserve_gpu_hours", "overhead_seconds", "shutdown_seconds"):
            seconds(getattr(self, name))
        if (self.ceiling_gpu_hours <= 0 or self.shutdown_seconds <= 0
                or self.allocation_mode not in ("gpu", "synthetic")):
            raise ValueError("positive ceiling/shutdown bound and explicit gpu/synthetic allocation mode required")


class BudgetStop(RuntimeError):
    """Admission/allocation stopped; every remaining scheduled slot is resumable."""


class _SnapshotChanged(ValueError):
    """A dependent worker committed after its parent's read snapshot opened."""


def _attempt_range(attempt, now):
    measured = attempt["elapsed_seconds"]
    low = measured if measured is not None else attempt.get("observed_seconds", 0)
    uncertain = measured is None or bool(attempt["uncertain_completion"])
    if measured is None:
        end = attempt.get("recovered_at") or now
        high = max(low, timestamp(end) - timestamp(attempt["started_at"]))
    else:
        high = low
    return low, high, uncertain


def _union_length(intervals, start, end):
    spans = sorted((max(start, a), min(end, b)) for a, b in intervals if b > start and a < end)
    total, cursor = 0.0, start
    for a, b in spans:
        total += max(0, b - max(a, cursor))
        cursor = max(cursor, b)
    return total


def _allocation_resources(allocations, attempts, processes, now, budget):
    """Partition allocation once: setup, interruptions, attempts, idle.

    Loading wins over attempt time, so it cannot also be added as setup. Known
    attempt intervals use their recorded wall clocks; potential unobserved work
    is separate. All uncovered time is still charged, including idle devices.
    """
    clock = timestamp(now)
    totals = Counter()
    reserve_used = Counter()
    devices, active, billing, reasons = [], [], [], []
    windows = defaultdict(list)
    for allocation in allocations:
        start = timestamp(allocation["started_at"])
        end = timestamp(allocation["stopped_at"]) if allocation["stopped_at"] else clock
        if end < start:
            raise ValueError("allocation ends before it starts")
        device = allocation["device"]
        for a, b in windows[device]:
            if min(end, b) > max(start, a):
                raise ValueError("overlapping allocations charge the same device twice")
        windows[device].append((start, end))
        worker = allocation["worker"]
        spans = defaultdict(list)
        for process in processes:
            if process["worker"] != worker:
                continue
            a = timestamp(process["started_at"])
            b = timestamp(process["ready_at"] or process["stopped_at"] or process["recovered_at"] or now)
            spans["setup" if process["ready_at"] else "uncertain_work"].append((a, b))
        for attempt in attempts:
            if attempt["worker"] != worker:
                continue
            a = timestamp(attempt["started_at"])
            observed = a + attempt.get("observed_seconds", 0)
            b = timestamp(attempt["finished_at"]) if attempt["finished_at"] else observed
            category = "interruption" if attempt["status"] in ("interrupted", "blocked") else "attempt"
            spans[category].append((a, b))
            if attempt["finished_at"] is None:
                spans["uncertain_work"].append((observed, timestamp(attempt.get("recovered_at") or now)))
        # Subtract the union of higher-priority spans, rather than adding overlap.
        used, partition = [], {}
        for category in ("setup", "interruption", "attempt", "uncertain_work"):
            before = _union_length(used, start, end)
            used.extend(spans[category])
            partition[category] = _union_length(used, start, end) - before
        partition["idle"] = max(0, end - start - sum(partition.values()))
        for k, v in partition.items():
            totals[k] += v
        reserve_used["setup"] += partition["setup"]
        reserve_used["interruption"] += partition["interruption"] + partition["uncertain_work"]
        if allocation["stage"] == "development":
            reserve_used["development"] += partition["attempt"] + partition["idle"]
        devices.append(dict(allocation, allocated_seconds=end - start, partition_seconds=partition))
        if not allocation["stopped_at"]:
            active.append(device)
        if allocation["billing_json"]:
            billing.append({"device": device, "record": json.loads(allocation["billing_json"])})
        if allocation["stop_reason"]:
            reasons.append(allocation["stop_reason"])
    reserves = None
    if budget is not None:
        reserves = {name: max(0, getattr(budget, name + "_reserve_gpu_hours") - reserve_used[name] / 3600)
                    for name in ("development", "setup", "interruption")}
    allocated = sum(totals.values()) / 3600 if allocations else None
    return {"allocation_mode": budget.allocation_mode if budget else "unclassified",
            "allocated_gpu_hours": allocated, "partition_seconds": dict(totals),
            "devices": devices, "active_devices": active, "provider_billing": billing,
            "remaining_ceiling_gpu_hours": None if budget is None else budget.ceiling_gpu_hours - (allocated or 0),
            "remaining_reserves_gpu_hours": reserves, "stop_reasons": sorted(set(reasons))}


def _forecast(branches, calls, generations, devices, budget, history=()):
    samples = defaultdict(list)
    for branch in branches:
        for call in branch.calls:
            row = calls.get(call.call_id)
            if call.replay_parent is not None or row is None or row["status"] not in FINAL:
                continue
            generation = generations[call.generation_id]
            if generation["unknown_duration_attempts"]:
                continue
            key = (branch.task.value, branch.phase, branch.policy or "none")
            for device in generation.get("by_device_seconds", {generation["device"]: generation["seconds"]}):
                # A retry spanning devices supplies its full workflow cost to
                # each participating device, conservatively preserving lost work.
                samples[key].append((generation["seconds"][0], device, generation["request_tokens"]))
    for snapshot in history:
        for cell in snapshot["forecast"]["cells"]:
            key = (cell["family"], cell["phase"], cell["condition"])
            for device, bounds in cell["by_device"].items():
                prompt = cell["observed_prompt_tokens"][1]
                samples[key].extend((cost, device, prompt) for cost in bounds)
    remaining = Counter()
    for branch in branches:
        for call in branch.calls:
            if call.replay_parent is None and (call.call_id not in calls or calls[call.call_id]["status"] not in FINAL):
                remaining[(branch.task.value, branch.phase, branch.policy or "none")] += 1
    rows, unavailable, low, high = [], [], 0.0, 0.0
    for key in sorted(set(samples) | set(remaining)):
        # The declared pilot does not contain masks in every main family.
        # Use the measured phase/condition across families, keeping the observed
        # prompt envelope and every device; no extra pilot calls are introduced.
        data = [sample for cell, values in samples.items() if cell[1:] == key[1:] for sample in values]
        measured_devices = {v[1] for v in data}
        missing_devices = sorted(set(devices) - measured_devices)
        available = bool(data) and not missing_devices
        count = remaining[key]
        bounds = [min(v[0] for v in data), 1.25 * max(v[0] for v in data)] if available else None
        if count and not available:
            unavailable.append({"family": key[0], "phase": key[1], "condition": key[2],
                                "unmeasured_devices": missing_devices})
        if available:
            low += count * bounds[0]
            high += count * bounds[1]
        rows.append({"family": key[0], "phase": key[1], "condition": key[2], "remaining_generations": count,
                     "measured_calls": len(data), "measured_devices": sorted(measured_devices),
                     "measurement_scope": "phase/condition pooled across measured families",
                     "seconds_per_generation": bounds,
                     "observed_prompt_tokens": [min(v[2] for v in data), max(v[2] for v in data)] if data else None,
                     "by_device": {device: [min(v[0] for v in data if v[1] == device),
                                            max(v[0] for v in data if v[1] == device)]
                                   for device in sorted(measured_devices)}})
    if unavailable:
        return {"available": False, "reason": "unmeasured phase/condition/device cells", "cells": rows,
                "unavailable_cells": unavailable, "remaining_gpu_hours": None, "elapsed_seconds": None}
    overhead = budget.overhead_seconds if budget else 0
    device_count = max(1, len(devices))
    return {"available": bool(samples) or not remaining, "reason": None, "cells": rows, "unavailable_cells": [],
            "remaining_gpu_hours": [low / 3600, (device_count * high + overhead) / 3600],
            "elapsed_seconds": [low / device_count, high + overhead],
            "rule": "observed minimum to slower-device maximum plus 25%; upper charges idle devices during serial dependencies; external overhead once"}


def _comparisons(worlds, branches, completed):
    definitions = (
        ("retention", ("revision",), ("L", "B", "C", "K", "F")),
        ("retention", ("sham",), ("B", "C", "K")),
        ("reset_interaction", ("revision", "sham"), ("B", "C")),
        ("compact_interaction", ("revision", "sham"), ("B", "C", "K")),
        ("collaborators", ("revision",), ("B", "C", "P_G", "P_H")),
        ("collaborators", ("sham",), ("B", "C", "P_G", "P_H")),
        ("collaborator_interaction", ("revision", "sham"), ("B", "C", "P_G", "P_H")),
        ("receipts", ("revision",), ("B", "C", "K", "B_delta", "C_delta", "K_delta")),
        ("prose", ("revision",), ("B", "C", "Q_B", "Q_C")),
        ("prose", ("sham",), ("B", "C", "Q_B", "Q_C")),
        ("preserving", ("preserving",), ("B", "C", "K")),
    )
    cells = defaultdict(lambda: {"scheduled": 0, "complete": 0, "world_ids": []})
    by_world = defaultdict(dict)
    for branch in branches:
        by_world[branch.world_id][(branch.event, branch.policy, branch.replicate)] = branch.branch_id
    for world in worlds:
        for subset, events, policies in definitions:
            for rep in (0, 1):
                ids = [by_world[world.world_id].get((event, policy, rep)) for event in events for policy in policies]
                if all(ids):
                    cell = cells[(world.world.task.value, "+".join(events), subset, rep)]
                    cell["scheduled"] += 1
                    if all(completed.get(b) == 4 for b in ids):
                        cell["complete"] += 1
                        cell["world_ids"].append(world.world_id)
        for event in ("revision", "sham"):
            ids = [by_world[world.world_id].get((event, policy, rep))
                   for policy in ("B", "C", "K", "P_G", "P_H") for rep in (0, 1)]
            if all(ids):
                cell = cells[(world.world.task.value, event, "repeatability", 1)]
                cell["scheduled"] += 1
                if all(completed.get(b) == 4 for b in ids):
                    cell["complete"] += 1
                    cell["world_ids"].append(world.world_id)
    return [dict(family=k[0], event=k[1], subset=k[2], replicate=k[3], **v) for k, v in sorted(cells.items())]


def progress_snapshot(worlds, branches, paths, *, now=None, budget=None, gate="M3 CPU verification; M5 inference gate open",
                      inflight=None, settings=None, prior_paths=(), _read_retries=2):
    """Read only, including for nonexistent files; never recover or create them.

    Each file is read in one SQLite snapshot. Cross-worker parent/raw commits
    precede dependent replay commits; no writer lock is held or requested.
    """
    supplied_now = now
    now = now or utc_now()
    timestamp(now)
    worlds, branches, paths = tuple(worlds), tuple(branches), tuple(Path(p).resolve() for p in paths)
    dependency_order(branches)
    if len(set(paths)) != len(paths):
        raise ValueError("each physical worker file must be supplied once")
    prior_paths = tuple(Path(p).resolve() for p in prior_paths)
    if len(set(prior_paths)) != len(prior_paths) or set(prior_paths) & set(paths):
        raise ValueError("historical physical files must be supplied once")
    history = []
    # Previous measured development/failed-configuration allocations remain
    # chargeable. Their run bindings reconstruct their own schedule; they do
    # not change the current scientific population or copy any physical reply.
    historical_runs = defaultdict(list)
    for path in prior_paths:
        store = WorkerStore(path, readonly=True)
        try:
            row = store.connection.execute("SELECT inputs_json FROM run_inputs WHERE singleton=1").fetchone()
            if not row:
                raise ValueError("historical measurement file lacks saved run inputs")
            historical_runs[row[0]].append(path)
        finally:
            store.close()
    from .manifests import _branch, _prepared
    for binding, run_paths in historical_runs.items():
        bound = json.loads(binding)
        history.append(progress_snapshot(tuple(_prepared(w) for w in bound["worlds"]),
            tuple(_branch(b) for b in bound["branches"]), run_paths, now=now))
    readers, records, inputs, attempts, processes, allocations, checkpoints = [], {}, {}, [], [], [], {}
    bindings = []
    try:
        for index, path in enumerate(paths):
            if not path.exists():
                continue
            reader = WorkerReader(path)
            readers.append((index, reader))
            # The pinned saver's first public read performs setup via
            # executescript, which commits an existing SQLite transaction even
            # when all tables already exist. Prime it BEFORE the read snapshot.
            reader.saver.get_tuple(DurableRunner._config(""))
            con = reader.store.connection
            con.execute("BEGIN")
            for row in con.execute("SELECT * FROM calls"):
                data = dict(row, worker=index)
                if data["call_id"] in records:
                    raise ValueError("duplicate logical/physical call across worker files")
                records[data["call_id"]] = data
            for row in con.execute("SELECT branch_id,round_number FROM round_inputs"):
                key = row["branch_id"], row["round_number"]
                if key in inputs:
                    raise ValueError("duplicate branch barrier")
                inputs[key] = True
            attempts.extend(dict(r, worker=index) for r in con.execute("SELECT * FROM attempts"))
            processes.extend(dict(r, worker=index) for r in con.execute("SELECT * FROM provider_processes"))
            tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "allocations" in tables:
                allocations.extend(dict(r, worker=index) for r in con.execute("SELECT * FROM allocations"))
            bound = con.execute("SELECT inputs_json FROM run_inputs WHERE singleton=1").fetchone()
            if bound:
                bindings.append(json.loads(bound[0]))
            for row in con.execute("SELECT DISTINCT thread_id FROM checkpoints"):
                branch_id = row[0]
                if branch_id in checkpoints:
                    raise ValueError("duplicate branch checkpoint")
                saved = reader.saver.get_tuple(DurableRunner._config(branch_id))
                checkpoints[branch_id] = (index, saved)
        if bindings:
            if any(b != bindings[0] for b in bindings):
                raise ValueError("worker run bindings differ")
            bound = bindings[0]
            if (record_json(bound["branches"]) != record_json([asdict(b) for b in sorted(branches, key=lambda b: b.branch_id)])
                    or record_json(bound["worlds"]) != record_json([asdict(w) for w in sorted(worlds, key=lambda w: w.world_id)])):
                raise ValueError("status manifest differs from saved run")
            if settings is not None and bound["settings"] != settings:
                raise ValueError("status settings differ")
            settings = bound["settings"]
            if bound.get("budget"):
                saved_budget = Budget(**bound["budget"])
                if budget is not None and budget != saved_budget:
                    raise ValueError("budget differs from saved run")
                budget = saved_budget
        scheduled = {c.call_id: (b, c) for b in branches for c in b.calls}
        if records.keys() - scheduled.keys() or checkpoints.keys() - {b.branch_id for b in branches}:
            raise ValueError("worker contains unscheduled work")
        if budget is None:
            configurations = {a["budget_json"] for a in allocations if a["budget_json"]}
            if len(configurations) > 1:
                raise ValueError("allocation budget bindings differ")
            if configurations:
                budget = Budget(**json.loads(configurations.pop()))
        by_attempt = defaultdict(list)
        for attempt in attempts:
            attempt["device"] = next((a["device"] for a in reversed(allocations)
                if a["worker"] == attempt["worker"] and timestamp(a["started_at"]) <= timestamp(attempt["started_at"])
                <= timestamp(a["stopped_at"] or now)), f"worker:{attempt['worker']}")
            by_attempt[attempt["call_id"]].append(attempt)
        generation_costs = {}
        for call_id, (branch, call) in scheduled.items():
            row = records.get(call_id)
            if row is not None and tuple(row[k] for k in ("seed", "generation_id", "replay_parent", "round_number", "peer")) != (
                    call.seed, call.generation_id, call.replay_parent, call.round_number, -1 if call.peer is None else call.peer):
                raise ValueError("saved slot seed/scope/parent differs")
            if row is not None and (row["status"] == "completed" and row["raw_json"] is None
                    or row["status"] in ("timeout", "infrastructure_failure") and row["failure_json"] is None):
                raise ValueError("finished slot lacks its exact raw outcome")
            if call.replay_parent is not None:
                if by_attempt[call_id]:
                    raise ValueError("replay has physical attempts")
                continue
            request_tokens = row.get("request_tokens") if row else None
            if row is not None and request_tokens is None:
                # Read-only compatibility with a pre-T04 backup. The normal
                # migrated path uses the existing call ledger's scalar count.
                reader = dict(readers)[row["worker"]]
                request_tokens = reader.store.connection.execute("""SELECT json_array_length(requests_json,?)
                    FROM round_inputs WHERE branch_id=? AND round_number=?""",
                    ("$.tokenized.input_ids" if call.peer is None else f"$.tokenized[{call.peer}].input_ids",
                     branch.branch_id, call.round_number)).fetchone()[0]
            measured = by_attempt[call_id]
            ranges = [_attempt_range(a, now) for a in measured]
            device = measured[-1]["device"] if measured else "unassigned"
            raw = json.loads(row["raw_json"]) if row and row["raw_json"] else None
            memory = [a.get("peak_memory_bytes") for a in measured if a.get("peak_memory_bytes") is not None]
            generation_costs[call_id] = {"generation_id": call_id, "device": device, "attempts": len(measured),
                "seconds": [sum(r[0] for r in ranges), sum(r[1] for r in ranges)],
                "uncertain_attempts": sum(r[2] for r in ranges),
                "unknown_duration_attempts": sum(a["elapsed_seconds"] is None for a in measured),
                "request_tokens": request_tokens, "physical_request_tokens": (request_tokens or 0) * len(measured),
                "output_tokens": len(raw["token_ids"]) if raw else None,
                "unknown_output_attempts": len(measured) - int(raw is not None),
                "peak_memory_bytes": max(memory) if memory else None}
            generation_costs[call_id]["by_device_seconds"] = {
                d: [sum(_attempt_range(a, now)[i] for a in measured if a["device"] == d) for i in (0, 1)]
                for d in sorted({a["device"] for a in measured})}
        logical = []
        for branch in branches:
            for call in branch.calls:
                row = records.get(call.call_id)
                validation = json.loads(row["validation_json"]) if row and row["validation_json"] else None
                if row and row["status"] == "replay" and (call.replay_parent not in records or records[call.replay_parent]["status"] not in FINAL):
                    raise _SnapshotChanged("replay lacks original completed physical parent")
                logical.append({"call_id": call.call_id, "generation_id": call.generation_id, "replay_parent": call.replay_parent,
                    "world_id": branch.world_id, "family": branch.task.value, "phase": branch.phase,
                    "event": branch.event, "policy": branch.policy, "replicate": branch.replicate,
                    "round": call.round_number, "peer": call.peer, "worker": row["worker"] if row else None,
                    "status": row["status"] if row else "unexecuted", "finished": bool(row and row["status"] in FINAL),
                    "protocol_outcome": validation["candidate"]["status"] if validation else
                        "failed" if row and row["status"] in ("timeout", "infrastructure_failure") else None,
                    "cost": generation_costs[call.generation_id]})
        completed, deliveries, checkpoint_rows = {}, {}, []
        for branch_id, (worker, saved) in checkpoints.items():
            values = saved.checkpoint["channel_values"]
            branch = next(b for b in branches if b.branch_id == branch_id)
            if values["branch_json"] != record_json(asdict(branch)) or settings is not None and values["settings_json"] != settings_json(settings):
                raise ValueError("saved checkpoint differs from schedule/settings")
            state = deserialize_state(values["committed"])
            completed[branch_id] = state.last_slot.round_number if state.last_slot and state.last_slot.phase == state.phase else 0
            checkpoint_rows.append({"branch_id": branch_id, "worker": worker, "checkpoint_id": saved.checkpoint["id"],
                                    "at": saved.checkpoint["ts"], "completed_round": completed[branch_id]})
            for delivery in state.deliveries:
                encoded = asdict(delivery)
                if delivery.delivery_id in deliveries and deliveries[delivery.delivery_id] != encoded:
                    raise ValueError("shared prefix delivery changed in a sibling")
                deliveries[delivery.delivery_id] = encoded
        for branch in branches:
            if branch.phase == "control":
                row = records.get(branch.calls[0].call_id)
                completed[branch.branch_id] = int(bool(row and row["validation_json"]))
            r = completed.get(branch.branch_id, 0)
            if any(not records.get(c.call_id) or records[c.call_id]["status"] not in FINAL
                   or not records[c.call_id]["validation_json"] for c in branch.calls if c.round_number <= r):
                raise ValueError("committed checkpoint has missing raw/validation records")
        policy_costs = []
        by_branch = {b.branch_id: b for b in branches}
        for branch in branches:
            used = tuple(branch.calls)
            if branch.prefix_parent:
                used = by_branch[branch.prefix_parent].calls + used
            costs = [generation_costs[c.generation_id] for c in used]
            policy_costs.append({"branch_id": branch.branch_id, "family": branch.task.value, "event": branch.event,
                "policy": branch.policy, "replicate": branch.replicate, "logical_calls": len(used),
                "finished_calls": sum(c.call_id in records and records[c.call_id]["status"] in FINAL for c in used),
                "seconds": [sum(c["seconds"][i] for c in costs) for i in (0, 1)],
                "unknown_calls": sum(c.call_id not in records or records[c.call_id]["status"] not in FINAL for c in used),
                "request_tokens": sum(c["physical_request_tokens"] for c in costs),
                "logical_request_tokens": sum(c["request_tokens"] or 0 for c in costs),
                "output_tokens": sum(c["output_tokens"] or 0 for c in costs),
                "unknown_request_calls": sum(c["request_tokens"] is None for c in costs),
                "unknown_output_attempt_uses": sum(c["unknown_output_attempts"] for c in costs),
                "uncertain_attempt_uses": sum(c["uncertain_attempts"] for c in costs)})
        resources = _allocation_resources(allocations, attempts, processes, now, budget)
        if history:
            all_devices = resources["devices"] + [a for h in history for a in h["resources"]["devices"]]
            seen = defaultdict(list)
            for allocation in all_devices:
                a, b = timestamp(allocation["started_at"]), timestamp(allocation["stopped_at"] or now)
                for x, y in seen[allocation["device"]]:
                    if min(b, y) > max(a, x):
                        raise ValueError("historical/current allocations overlap on the same device")
                seen[allocation["device"]].append((a, b))
            physical_ids = {(settings_json(settings or {}), c["generation_id"]) for c in generation_costs.values() if c["attempts"]}
            for previous in history:
                previous_ids = {(settings_json(previous["settings"] or {}), c["generation_id"])
                                for c in previous["generations"] if c["attempts"]}
                if physical_ids & previous_ids:
                    raise ValueError("historical physical generations supplied twice")
                physical_ids.update(previous_ids)
            # Partitioned intervals suffice to recompute reserves; no second
            # historical ledger or copied measurement store is introduced.
            totals, spent = Counter(), Counter()
            for allocation in all_devices:
                part = allocation["partition_seconds"]
                totals.update(part)
                spent["setup"] += part["setup"]
                spent["interruption"] += part["interruption"] + part["uncertain_work"]
                if allocation["stage"] == "development":
                    spent["development"] += part["attempt"] + part["idle"]
            resources.update(devices=all_devices, partition_seconds=dict(totals),
                allocated_gpu_hours=sum(totals.values()) / 3600 if all_devices else None,
                active_devices=[a["device"] for a in all_devices if not a["stopped_at"]],
                provider_billing=resources["provider_billing"] + [b for h in history for b in h["resources"]["provider_billing"]])
            if budget is not None:
                resources["remaining_ceiling_gpu_hours"] = budget.ceiling_gpu_hours - sum(totals.values()) / 3600
                resources["remaining_reserves_gpu_hours"] = {name: max(0, getattr(budget, name + "_reserve_gpu_hours") - spent[name] / 3600)
                                                           for name in ("development", "setup", "interruption")}
        forecast_devices = sorted(set(a["device"] for a in allocations)) or [f"worker:{i}" for i in range(len(paths))]
        if resources["devices"]:
            forecast_devices = sorted({a["device"] for a in resources["devices"]})
        forecast = _forecast(branches, records, generation_costs, forecast_devices, budget,
                             [h for h in history if h["settings"] == settings])
        finished = sum(r["finished"] for r in logical)
        outcomes = Counter(r["protocol_outcome"] or "unvalidated" for r in logical if r["finished"])
        current = []
        for attempt in attempts:
            if attempt["status"] == "running":
                branch, call = scheduled[attempt["call_id"]]
                current.append({"stage": "development" if next(w for w in worlds if w.world_id == branch.world_id).development else "main",
                    "family": branch.task.value, "world_id": branch.world_id, "branch_id": branch.branch_id,
                    "replicate": branch.replicate, "round": call.round_number, "peer": call.peer,
                    "device": generation_costs[call.generation_id]["device"], "attempt": attempt["number"],
                    "elapsed_seconds": max(0, timestamp(now) - timestamp(attempt["started_at"])),
                    "last_observed_seconds": attempt.get("observed_seconds", 0)})
        # Use the scheduler's exact dependency rules, also when called from CLI.
        chosen_settings = settings
        if chosen_settings is None and checkpoints:
            chosen_settings = json.loads(next(iter(checkpoints.values()))[1].checkpoint["channel_values"]["settings_json"])
        reader_by_index = dict(readers)
        work = [asdict(w) for w in scheduled_work(worlds, branches, [reader_by_index.get(i) for i in range(len(paths))],
                settings=chosen_settings or {}, inflight=inflight, recorded_active=True)]
        if any(w["status"] == "blocked" for w in work):
            gate = "provider defect requires diagnosis; recorded unknown work retained"
        elif len(logical) > finished and allocations:
            reason = max(allocations, key=lambda a: a["started_at"])["stop_reason"]
            if reason and reason != "scheduler_close":
                gate = reason
        return {"at": now, "gate": gate, "budget": asdict(budget) if budget else None, "settings": settings,
            "counts": {"scheduled_logical": len(logical), "finished_logical": finished, "remaining_logical": len(logical) - finished,
                "scheduled_generations": len(generation_costs),
                "finished_generations": sum(records.get(c, {}).get("status") in FINAL for c in generation_costs),
                "remaining_generations": sum(records.get(c, {}).get("status") not in FINAL for c in generation_costs),
                "replay_uses": sum(r["status"] == "replay" for r in logical), "attempts": len(attempts),
                "retries": sum(a["number"] == 2 for a in attempts), "protocol_outcomes": dict(outcomes),
                "recorded_failures": outcomes["invalid"] + outcomes["failed"],
                "unknown_logical": len(logical) - finished, "uncertain_attempts": sum(a["uncertain_completion"] for a in attempts),
                "completed_worlds": sum(all(completed.get(b.branch_id) == (1 if b.phase == "control" else 4)
                                            for b in branches if b.world_id == w.world_id) for w in worlds)},
            "logical_slots": logical, "generations": list(generation_costs.values()), "policy_costs": policy_costs,
            "physical": {"attempt_seconds": [sum(c["seconds"][i] for c in generation_costs.values()) for i in (0, 1)],
                "request_tokens": sum(c["physical_request_tokens"] for c in generation_costs.values()),
                "output_tokens": sum(c["output_tokens"] or 0 for c in generation_costs.values()),
                "unknown_output_attempts": sum(c["unknown_output_attempts"] for c in generation_costs.values()),
                "by_device_seconds": {d: [sum(_attempt_range(a, now)[i] for a in attempts if a["device"] == d)
                                           for i in (0, 1)] for d in sorted({a["device"] for a in attempts})},
                "peak_memory_bytes": max((c["peak_memory_bytes"] for c in generation_costs.values()
                                          if c["peak_memory_bytes"] is not None), default=None)},
            "validated_deliveries": list(deliveries.values()),
            "delivery_counts": {"source_attempts": sum(d["source"] is not None for d in deliveries.values()),
                                "source_acquisitions": sum(d["acquired"] is True for d in deliveries.values()),
                                "text_deliveries": sum(d["text"] is not None for d in deliveries.values())},
            "current": current, "checkpoints": checkpoint_rows,
            "work": work, "matched_comparisons": _comparisons(worlds, branches, completed),
            "resources": resources, "forecast": forecast,
            "prior_runs": [{"counts": h["counts"], "physical": h["physical"]} for h in history],
            "overhead_rule": "original measured attempt costs include in-attempt loading/transport/termination; outside allocation overhead remains experiment overhead; allocation partition is not added to attempts"}
    except _SnapshotChanged:
        if not _read_retries:
            raise
        # There is no global SQLite snapshot across worker files. Raw parents
        # are immutable once final, so a fresh bounded read resolves this live
        # transition. A genuinely missing parent still fails after two rereads.
        for _, reader in readers:
            reader.store.connection.rollback()
            reader.close()
        readers.clear()
        return progress_snapshot(worlds, branches, paths, now=supplied_now, budget=budget, gate=gate,
            inflight=inflight, settings=settings, prior_paths=prior_paths, _read_retries=_read_retries - 1)
    finally:
        for _, reader in readers:
            reader.store.connection.rollback()
            reader.close()


def format_status(snapshot):
    c, r, forecast = snapshot["counts"], snapshot["resources"], snapshot["forecast"]
    lines = [f"Gate: {snapshot['gate']}",
        f"Logical slots: {c['finished_logical']}/{c['scheduled_logical']} finished; {c['remaining_logical']} remaining/unknown.",
        f"Generations: {c['finished_generations']}/{c['scheduled_generations']}; replays {c['replay_uses']}; attempts {c['attempts']}, retries {c['retries']}.",
        f"Protocol outcomes: {c['protocol_outcomes']}; uncertain attempts {c['uncertain_attempts']}; completed worlds {c['completed_worlds']}."]
    if r["allocated_gpu_hours"] is None:
        lines.append("Allocation: unavailable (no device allocation records).")
    else:
        lines.append(f"Allocation ({r['allocation_mode']}): {r['allocated_gpu_hours']:.6f} GPU-hours; active devices {r['active_devices']}; remaining ceiling {r['remaining_ceiling_gpu_hours']}; reserves {r['remaining_reserves_gpu_hours']}.")
    lines.append(f"Remaining forecast: {forecast['remaining_gpu_hours']} GPU-hours; elapsed {forecast['elapsed_seconds']} seconds."
                 if forecast["available"] else f"Remaining forecast: unavailable ({forecast['reason']}).")
    lines.append("Slot completion is a work count; runtime percentage is unavailable.")
    for current in snapshot["current"]:
        lines.append(f"Active: {current['stage']} {current['family']} {current['world_id']} {current['branch_id']} rep{current['replicate']} r{current['round']} peer={current['peer']} device={current['device']} attempt={current['attempt']} elapsed={current['elapsed_seconds']:.3f}s.")
    checkpoints = snapshot["checkpoints"]
    if checkpoints:
        last = max(checkpoints, key=lambda v: v["at"])
        lines.append(f"Last checkpoint: {last['at']} {last['branch_id']} round {last['completed_round']}.")
    lines.append(f"Branches: {dict(Counter(w['status'] for w in snapshot['work']))}; stop reasons: {r['stop_reasons']}.")
    for group in snapshot["matched_comparisons"]:
        lines.append(f"Matched {group['family']}/{group['event']}/{group['subset']}/rep{group['replicate']}: {group['complete']}/{group['scheduled']} worlds complete.")
    lines.append("Resumable branch/call identities and original costs are in the JSON status view.")
    return "\n".join(lines)


def terminal_progress(snapshot):
    print(format_status(snapshot), flush=True)
