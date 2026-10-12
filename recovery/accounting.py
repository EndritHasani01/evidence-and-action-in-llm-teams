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

from .costs import (FINAL, OVERHEAD_RULE, timestamp, _attempt_range, _allocation_resources, _union_length, ledger_generation_costs,
                    ledger_policy_costs, physical_costs)
from .rounds import deserialize_state
from .runner import WorkerReader, DurableRunner
from .schedule import dependency_order
from .storage import record_json, seconds, settings_json, utc_now, WorkerStore
from .workers import scheduled_work


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


@dataclass(frozen=True)
class CourseBudget(Budget):
    """Section 11.3 bounds in the existing saved budget, not available quota.

    Prior bounds cover ONLY spending absent from supplied worker ledgers. Each
    pair is a documented lower/upper GPU-hour bound; None is unresolved. Shared
    preparation belongs to the course categories and is charged once overall.
    other_overall excludes all course/shared spending. A verified zero requires
    evidence too. These inputs survive account/configuration changes and restart.
    """

    ceiling_gpu_hours: float = 30
    overall_ceiling_gpu_hours: float = 100
    prior_development_gpu_hours: tuple[float, float] | None = None
    prior_setup_gpu_hours: tuple[float, float] | None = None
    prior_interruption_gpu_hours: tuple[float, float] | None = None
    prior_other_course_gpu_hours: tuple[float, float] | None = None
    prior_other_overall_gpu_hours: tuple[float, float] | None = None
    # Smoke is a subset of preparation already charged above/in prior ledgers.
    # These cumulative historical totals are checked, never added a second time.
    prior_smoke_gpu_hours: tuple[float, float] | None = None
    prior_smoke_attempts: int | None = None
    prior_evidence: str = ""

    def __post_init__(self):
        super().__post_init__()
        seconds(self.overall_ceiling_gpu_hours)
        if (not 0 < self.overall_ceiling_gpu_hours <= 100 or self.ceiling_gpu_hours > 30
                or self.development_reserve_gpu_hours > 8 or self.setup_reserve_gpu_hours > 2
                or self.interruption_reserve_gpu_hours > 2):
            raise ValueError("course budget must respect the adopted 30/100-hour ceilings and 8/2/2 allowances")
        if type(self.prior_evidence) is not str:
            raise ValueError("prior allocation bounds require documented evidence")
        if self.prior_smoke_attempts is not None and (type(self.prior_smoke_attempts) is not int
                or self.prior_smoke_attempts < 0 or not self.prior_evidence.strip()):
            raise ValueError("prior smoke attempts require a nonnegative integer and evidence")
        for name in ("development", "setup", "interruption", "other_course", "other_overall", "smoke"):
            field = "prior_" + name + "_gpu_hours"
            bounds = getattr(self, field)
            if bounds is not None:
                if (not isinstance(bounds, (tuple, list)) or len(bounds) != 2
                        or seconds(bounds[0]) > seconds(bounds[1]) or not self.prior_evidence.strip()):
                    raise ValueError("prior allocation bounds require increasing lower/upper values and evidence")
                object.__setattr__(self, field, tuple(bounds))


class MonitoringCourseBudget(CourseBudget):
    """User-authorized observation policy; original budget JSON stays compatible.

    Historical limits remain available for retrospective reporting, while this
    course execution policy does not turn unknown spending into an admission stop.
    Per-call bounds and the controller's session deadline still apply.
    """


def budget_from_record(record):
    # Old thesis budget JSON and run bindings retain their exact representation.
    return (CourseBudget if "overall_ceiling_gpu_hours" in record else Budget)(**record)


def _course_resources(resources, budget):
    """Combine original allocation partitions and unrecorded prior bounds once."""
    observed = Counter()
    for allocation in resources["devices"]:
        part = allocation["partition_seconds"]
        observed["setup"] += part["setup"] / 3600
        observed["interruption"] += (part["interruption"] + part["uncertain_work"]) / 3600
        category = "development" if allocation["stage"] == "development" else "other_course"
        observed[category] += (part["attempt"] + part["idle"]) / 3600
    prior = {name: getattr(budget, "prior_" + name + "_gpu_hours")
             for name in ("development", "setup", "interruption", "other_course", "other_overall")}
    unknown = [name for name, value in prior.items() if value is None]
    ranges = {name: [observed[name] + value[i] for i in (0, 1)] if value is not None else None
              for name, value in prior.items()}
    course = [sum(ranges[name][i] for name in ranges if name != "other_overall") for i in (0, 1)] if not any(name != "other_overall" for name in unknown) else None
    overall = [course[i] + ranges["other_overall"][i] for i in (0, 1)] if course is not None and ranges["other_overall"] is not None else None
    reserves = {name: max(0, getattr(budget, name + "_reserve_gpu_hours") - ranges[name][1])
                if ranges[name] is not None else None for name in ("development", "setup", "interruption")}
    exceeded = [name for name in reserves if ranges[name] is not None
                and ranges[name][1] > getattr(budget, name + "_reserve_gpu_hours")]
    if course is not None and course[1] > budget.ceiling_gpu_hours:
        exceeded.append("course_ceiling")
    if overall is not None and overall[1] > budget.overall_ceiling_gpu_hours:
        exceeded.append("overall_ceiling")
    smoke_unknown = budget.prior_smoke_gpu_hours is None or budget.prior_smoke_attempts is None
    if not smoke_unknown and (budget.prior_smoke_gpu_hours[1] > .5 or budget.prior_smoke_attempts > 24):
        exceeded.append("smoke")
    reason = ("unknown_prior_allocation" if unknown else "unknown_prior_smoke" if smoke_unknown
              else "cumulative_allowance_exceeded" if exceeded else None)
    remaining_course = budget.ceiling_gpu_hours - course[1] if course is not None else None
    remaining_overall = budget.overall_ceiling_gpu_hours - overall[1] if overall is not None else None
    resources.update(prior_bounds_gpu_hours=prior, prior_evidence=budget.prior_evidence,
        spending_bounds_gpu_hours=ranges, course_gpu_hours=course, overall_gpu_hours=overall,
        unknown_prior_categories=unknown, exceeded_allowances=exceeded,
        admission_available=reason is None, admission_reason=reason,
        remaining_course_gpu_hours=remaining_course, remaining_overall_gpu_hours=remaining_overall,
        remaining_ceiling_gpu_hours=min(remaining_course, remaining_overall) if not unknown else None,
        remaining_reserves_gpu_hours=reserves,
        remaining_smoke_gpu_hours=None if budget.prior_smoke_gpu_hours is None else max(0, .5-budget.prior_smoke_gpu_hours[1]),
        remaining_smoke_attempts=None if budget.prior_smoke_attempts is None else max(0, 24-budget.prior_smoke_attempts),
        cumulative_rule="course/shared prior plus original allocations once; other overall once; unspent 8/2/2 reserves plus 1.25 complete main forecast")


def course_admission(resources, forecast, budget, stage, device_count):
    """Conservative time before provider setup, including every assigned device."""
    if isinstance(budget, MonitoringCourseBudget):
        return None, device_count*24*3600  # Controller independently bounds the session.
    if not resources["admission_available"]:
        return resources["admission_reason"], 0
    available = resources["remaining_ceiling_gpu_hours"]
    reserves = resources["remaining_reserves_gpu_hours"]
    if stage == "main":
        available -= sum(reserves.values())
        if not forecast["available"]:
            return "remaining_forecast_unavailable", 0
        if forecast["remaining_gpu_hours"][1] + device_count * budget.shutdown_seconds / 3600 >= available:
            return "remaining_forecast_exceeds_budget", 0
        # The independent allocation deadline also protects future unmeasured
        # loading/interruption time. Reaching it retains the original schedule
        # for another admission check; it never drops a branch or refunds cost.
        available = min(available, reserves["setup"], reserves["interruption"])
    else:
        # Until measured, any allocated second may be loading, interrupted or
        # development work. Bound each nonoverlapping allowance conservatively.
        available = min(available, *reserves.values())
    if available * 3600 <= device_count * budget.shutdown_seconds + budget.overhead_seconds:
        return "budget_exhausted_before_allocation", 0
    return None, available * 3600 - budget.overhead_seconds


class _SnapshotChanged(ValueError):
    """A dependent worker committed after its parent's read snapshot opened."""


def _setup_free_seconds(attempts, processes, now):
    """Forecast computation only; physical/policy attempts retain full costs.

    Loading is already in the setup allowance. Use the original ready/process
    clocks, including resident reuse, and withhold samples with unknown loading.
    """
    result = {}
    for attempt in attempts:
        cid = attempt["call_id"]
        if cid in result and result[cid] is None:
            continue
        elapsed = attempt["elapsed_seconds"]
        if elapsed is None or attempt["finished_at"] is None:
            result[cid] = None
            continue
        start, end = timestamp(attempt["started_at"]), timestamp(attempt["finished_at"])
        matching = [p for p in processes if p["worker"] == attempt["worker"] and p["pid"] == attempt.get("worker_pid")
                    and timestamp(p["started_at"]) <= end and timestamp(p["stopped_at"] or p["recovered_at"] or now) >= start]
        if not matching or any(p["ready_at"] is None for p in matching):
            result[cid] = None
            continue
        setup = [(timestamp(p["started_at"]), timestamp(p["ready_at"])) for p in matching]
        if any(b < a for a, b in setup) or end < start:
            raise ValueError("provider/attempt clocks cannot reconstruct setup")
        loading = min(elapsed, _union_length(setup, start, end))
        result[cid] = result.get(cid, 0) + elapsed - loading
    return result


def _forecast(branches, calls, generations, devices, budget, history=(), gpu_generations=None):
    course_gpu = isinstance(budget, CourseBudget) and budget.allocation_mode == "gpu"
    samples = defaultdict(list)
    for branch in branches:
        for call in branch.calls:
            row = calls.get(call.call_id)
            if call.replay_parent is not None or row is None or row["status"] not in FINAL:
                continue
            if gpu_generations is not None and call.generation_id not in gpu_generations:
                continue
            generation = generations[call.generation_id]
            if generation["unknown_duration_attempts"]:
                continue
            duration = generation.get("forecast_seconds_excluding_setup") if course_gpu else generation["seconds"][0]
            if duration is None:
                continue
            key = (branch.task.value, branch.phase, branch.policy or "none")
            for device in generation.get("by_device_seconds", {generation["device"]: generation["seconds"]}):
                # A retry spanning devices supplies its full workflow cost to
                # each participating device, conservatively preserving lost work.
                samples[key].append((duration, device, generation["request_tokens"]))
    for snapshot in history:
        if course_gpu and snapshot["resources"]["allocation_mode"] != "gpu":
            continue  # CPU timings cannot forecast T4 throughput.
        if course_gpu:
            for slot in snapshot["logical_slots"]:
                cost = slot["cost"]
                duration = cost.get("forecast_seconds_excluding_setup")
                if not slot["finished"] or slot["replay_parent"] is not None or duration is None:
                    continue
                key = slot["family"], slot["phase"], slot["policy"] or "none"
                for device in cost["by_device_seconds"]:
                    samples[key].append((duration, device, cost["request_tokens"]))
            continue
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
    course = isinstance(budget, CourseBudget)
    return {"available": bool(samples) or not remaining, "reason": None, "cells": rows, "unavailable_cells": [],
            "remaining_gpu_hours": [low / 3600, (device_count * high + (1.25 if course else 1) * overhead) / 3600],
            "elapsed_seconds": [low / device_count, high + (1.25 if course else 1) * overhead],
            "rule": ("observed minimum to slower-device maximum plus 25%; upper charges idle devices during serial dependencies; external overhead once, inside the 25% main margin"
                     if course else "observed minimum to slower-device maximum plus 25%; upper charges idle devices during serial dependencies; external overhead once")}


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
                      inflight=None, settings=None, prior_paths=(), regime=None, planned_devices=(), _read_retries=2):
    """Read only, including for nonexistent files; never recover or create them.

    Each file is read in one SQLite snapshot. Cross-worker parent/raw commits
    precede dependent replay commits; no writer lock is held or requested.
    """
    supplied_now = now
    now = now or utc_now()
    timestamp(now)
    if regime is not None:
        from .populations import _check_regime
        _check_regime(regime)
    planned_devices = tuple(planned_devices)
    if len(set(planned_devices)) != len(planned_devices) or any(type(d) is not str or not d for d in planned_devices):
        raise ValueError("forecast requires distinct identified planned devices")
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
            if regime is not None and bound.get("regime", "thesis") != regime:
                raise ValueError("status regime differs from saved run")
            if (record_json(bound["branches"]) != record_json([asdict(b) for b in sorted(branches, key=lambda b: b.branch_id)])
                    or record_json(bound["worlds"]) != record_json([asdict(w) for w in sorted(worlds, key=lambda w: w.world_id)])):
                raise ValueError("status manifest differs from saved run")
            if settings is not None and bound["settings"] != settings:
                raise ValueError("status settings differ")
            settings = bound["settings"]
            if bound.get("budget"):
                saved_budget = budget_from_record(bound["budget"])
                if budget is not None and asdict(budget) != asdict(saved_budget):
                    raise ValueError("budget differs from saved run")
                budget = budget if budget is not None else saved_budget
        scheduled = {c.call_id: (b, c) for b in branches for c in b.calls}
        if records.keys() - scheduled.keys() or checkpoints.keys() - {b.branch_id for b in branches}:
            raise ValueError("worker contains unscheduled work")
        if budget is None:
            configurations = {a["budget_json"] for a in allocations if a["budget_json"]}
            if len(configurations) > 1:
                raise ValueError("allocation budget bindings differ")
            if configurations:
                budget = budget_from_record(json.loads(configurations.pop()))
        for attempt in attempts:
            # The status clock can precede a concurrent attempt commit. Only a
            # recorded release closes device ownership; now is a cost clock.
            attempt["device"] = next((a["device"] for a in reversed(allocations)
                if a["worker"] == attempt["worker"] and timestamp(a["started_at"]) <= timestamp(attempt["started_at"])
                and (a["stopped_at"] is None or timestamp(attempt["started_at"]) <= timestamp(a["stopped_at"]))),
                f"worker:{attempt['worker']}")
        # Read-only compatibility with pre-T04 backups. Ordinary migrated
        # calls already carry the scalar request count.
        for row in records.values():
            if row.get("request_tokens") is None:
                reader = dict(readers)[row["worker"]]
                row["request_tokens"] = reader.store.connection.execute("""SELECT json_array_length(requests_json,?)
                    FROM round_inputs WHERE branch_id=? AND round_number=?""",
                    ("$.tokenized.input_ids" if row["peer"] == -1 else f"$.tokenized[{row['peer']}].input_ids",
                     row["branch_id"], row["round_number"])).fetchone()[0]
        generation_costs = ledger_generation_costs(branches, records, attempts, now)
        if isinstance(budget, CourseBudget) and budget.allocation_mode == "gpu":
            setup_free = _setup_free_seconds(attempts, processes, now)
            for cid, cost in generation_costs.items():
                cost["forecast_seconds_excluding_setup"] = setup_free.get(cid)
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
        policy_costs = ledger_policy_costs(branches, records, generation_costs)
        resources = _allocation_resources(allocations, attempts, processes, now, budget)
        if budget is not None and budget.allocation_mode == "gpu":
            # A stopped process without a ready receipt may have been loading
            # or computing. Its allocated total is known, but setup versus
            # interruption attribution cannot establish either unused reserve.
            resources["unknown_setup_allocation"] = any(p["ready_at"] is None
                and (p["stopped_at"] or p["recovered_at"]) and any(a["worker"] == p["worker"]
                    and timestamp(p["started_at"]) < timestamp(a["stopped_at"] or now)
                    and timestamp(p["stopped_at"] or p["recovered_at"]) > timestamp(a["started_at"])
                    for a in allocations) for p in processes) or any(
                        h["resources"].get("unknown_setup_allocation", False) for h in history)
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
        if planned_devices:
            forecast_devices = sorted(planned_devices)
        gpu_generations = None
        if isinstance(budget, CourseBudget) and budget.allocation_mode == "gpu":
            gpu_attempts = {(a["call_id"], a["number"]) for a in attempts if any(
                allocation["worker"] == a["worker"] and allocation["device"] == a["device"]
                and allocation["budget_json"] and json.loads(allocation["budget_json"])["allocation_mode"] == "gpu"
                and timestamp(allocation["started_at"]) <= timestamp(a["started_at"])
                and (allocation["stopped_at"] is None or timestamp(a["started_at"]) <= timestamp(allocation["stopped_at"]))
                for allocation in allocations)}
            unclassified = {a["call_id"] for a in attempts if (a["call_id"], a["number"]) not in gpu_attempts}
            gpu_generations = {a["call_id"] for a in attempts} - unclassified
        forecast = _forecast(branches, records, generation_costs, forecast_devices, budget,
                             [h for h in history if h["settings"] == settings], gpu_generations=gpu_generations)
        if isinstance(budget, CourseBudget):
            if regime == "thesis" or any(b.get("regime", "thesis") != "course" for b in bindings):
                raise ValueError("course budget requires the course regime")
            _course_resources(resources, budget)
            if budget.allocation_mode == "gpu" and (len(gpu_attempts) != len(attempts) or any(
                    h["counts"]["attempts"] and h["resources"]["allocation_mode"] != "gpu" for h in history)
                    or any(not a["budget_json"] or json.loads(a["budget_json"])["allocation_mode"] != "gpu"
                           for a in resources["devices"])):
                resources.update(admission_available=False, admission_reason="unknown_allocation_classification")
            elif resources.get("unknown_setup_allocation"):
                resources.update(admission_available=False, admission_reason="unknown_setup_allocation")
                for category in ("setup", "interruption"):
                    resources["spending_bounds_gpu_hours"][category] = None
                    resources["remaining_reserves_gpu_hours"][category] = None
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
        elif isinstance(budget, CourseBudget) and not resources["admission_available"]:
            gate = resources["admission_reason"]
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
            "physical": physical_costs(generation_costs, attempts, now),
            "validated_deliveries": list(deliveries.values()),
            "delivery_counts": {"source_attempts": sum(d["source"] is not None for d in deliveries.values()),
                                "source_acquisitions": sum(d["acquired"] is True for d in deliveries.values()),
                                "text_deliveries": sum(d["text"] is not None for d in deliveries.values())},
            "current": current, "checkpoints": checkpoint_rows,
            "work": work, "matched_comparisons": _comparisons(worlds, branches, completed),
            "resources": resources, "forecast": forecast,
            "prior_runs": [{"counts": h["counts"], "physical": h["physical"]} for h in history],
            "overhead_rule": OVERHEAD_RULE}
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
            inflight=inflight, settings=settings, prior_paths=prior_paths, regime=regime,
            planned_devices=planned_devices, _read_retries=_read_retries - 1)
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
    if "course_gpu_hours" in r:
        lines.append(f"Cumulative course/overall GPU-hour bounds: {r['course_gpu_hours']} / {r['overall_gpu_hours']}; admission {r['admission_reason'] or 'resource bounds available'}; unused reserves {r['remaining_reserves_gpu_hours']}; prior evidence: {r['prior_evidence']}.")
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
