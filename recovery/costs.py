"""Original ledger costs and offline whole-policy analysis (spec section 7.3).

Physical attempts/allocation are charged once. Hypothetical policies charge the
original prefix and all sixteen logical calls, including original replay costs.
The allocation partition reconciles wall clocks; it is never added to attempts.
"""

from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
import json

FINAL = {"completed", "timeout", "infrastructure_failure", "replay"}
OVERHEAD_RULE = "original measured attempt costs include in-attempt loading/transport/termination; outside allocation overhead remains experiment overhead; allocation partition is not added to attempts"

def timestamp(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("resource clocks require an explicit timezone")
    return result.timestamp()


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


def ledger_generation_costs(branches, records, attempts, now):
    """The M3 original-generation arithmetic, shared by status and analysis."""
    scheduled = {c.call_id: (b, c) for b in branches for c in b.calls}
    by_attempt = defaultdict(list)
    for attempt in attempts:
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
    return generation_costs


def ledger_policy_costs(branches, records, generation_costs):
    """Prefix plus every scheduled call; no early stopping or replay discount."""
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
    return policy_costs


def physical_costs(generation_costs, attempts, now):
    """Count each original generation and all its attempts exactly once."""
    return {"attempt_seconds": [sum(c["seconds"][i] for c in generation_costs.values()) for i in (0, 1)],
                "request_tokens": sum(c["physical_request_tokens"] for c in generation_costs.values()),
                "output_tokens": sum(c["output_tokens"] or 0 for c in generation_costs.values()),
                "unknown_output_attempts": sum(c["unknown_output_attempts"] for c in generation_costs.values()),
                "by_device_seconds": {d: [sum(_attempt_range(a, now)[i] for a in attempts if a["device"] == d)
                                           for i in (0, 1)] for d in sorted({a["device"] for a in attempts})},
                "peak_memory_bytes": max((c["peak_memory_bytes"] for c in generation_costs.values()
                                          if c["peak_memory_bytes"] is not None), default=None)}


def select_boundary_policy(manifest, peer_sources):
    """Frozen C/K choice using only initial held ID/version coverage.

    A persisted tombstone has a value (its endpoints); a pending replacement
    does not. Values, candidates, history, correctness and subsequent sources
    are never consulted. None represents an unobserved peer boundary.
    """
    expected = {(r["record_id"], r["version"]) for r in manifest}
    if len(expected) != len(manifest) or len({r["record_id"] for r in manifest}) != len(manifest):
        raise ValueError("duplicate current manifest identity")
    if len(peer_sources) != 4:
        raise ValueError("boundary rule requires all four peers")
    coverage = []
    for peer, sources in enumerate(peer_sources):
        if sources is None:
            coverage.append(dict(peer=peer, complete=None, known_pairs=None,
                missing_pairs=None, pending_pairs=None, tombstone_pairs=None,
                denominator=len(expected), reason="initial_coverage_unknown"))
            continue
        ids = [s["record_id"] for s in sources]
        if len(ids) != len(set(ids)) or set(ids) - {r[0] for r in expected}:
            raise ValueError("duplicate or unlisted boundary source")
        known = {(s["record_id"], s["version"]) for s in sources if "value" in s}
        missing = expected - known
        coverage.append(dict(peer=peer, complete=not missing,
            known_pairs=[list(p) for p in sorted(known & expected)],
            missing_pairs=[list(p) for p in sorted(missing)],
            pending_pairs=[[s["record_id"], s["version"]] for s in sources if "value" not in s],
            tombstone_pairs=[[s["record_id"], s["version"]] for s in sources
                             if "value" in s and s.get("deleted")],
            denominator=len(expected), reason=None))
    complete = [r["complete"] for r in coverage]
    policy = "C" if all(v is True for v in complete) else "K" if False in complete else None
    return dict(selected_policy=policy, coverage=coverage,
                reason="initial_coverage_unknown" if policy is None else None)


def boundary_selections(worlds, branches, inputs, *, committed=None):
    """One choice per world/event/replicate from recorded ordinary B/C/K starts.

    Their initial source tables must agree. A checkpoint can establish the
    boundary only before any recovery call; later acquisitions never substitute
    for missing round-one input. Branch availability never changes the choice.
    """
    by_world = {w.world_id: w for w in worlds}
    groups = defaultdict(dict)
    for branch in branches:
        if branch.phase == "continuation" and branch.policy in ("B", "C", "K"):
            key = branch.world_id, branch.event, branch.replicate
            if branch.policy in groups[key]:
                raise ValueError("duplicate boundary comparator")
            groups[key][branch.policy] = branch
    result = []
    for (world_id, event, replicate), siblings in sorted(groups.items()):
        prepared = by_world[world_id]
        current = prepared.event_world(event)
        manifest = [{"record_id": s.record_id, "version": s.version} for s in current.records]
        choices, provenance = [], []
        for policy in ("B", "C", "K"):
            branch = siblings.get(policy)
            if branch is None:
                continue
            saved = inputs.get((branch.branch_id, 1))
            state = json.loads(saved["requests"]["before"]) if saved else None
            origin = "round_one_input"
            if state is None:
                saved = (committed or {}).get(branch.branch_id)
                possible = saved["state"] if saved else None
                if possible and (not possible.get("last_slot") or possible["last_slot"]["phase"] == "prefix"):
                    state, origin = possible, "committed_pre_call_boundary"
            if state is None:
                continue
            if (state["branch_id"] != branch.branch_id or state["phase"] != "recovery"
                    or state["task"] != branch.task.value or state["size"] != current.size.value):
                raise ValueError("initial coverage differs from scheduled boundary")
            choices.append(select_boundary_policy(manifest, [p["sources"] for p in state["peers"]]))
            provenance.append(dict(branch_id=branch.branch_id, origin=origin,
                worker=saved.get("worker"), worker_file=saved.get("worker_file"),
                checkpoint_id=saved.get("checkpoint_id")))
        if choices and any(c != choices[0] for c in choices):
            raise ValueError("B/C/K initial current-source coverage differs")
        choice = choices[0] if choices else select_boundary_policy(manifest, [None] * 4)
        selected = siblings.get(choice["selected_policy"])
        result.append(dict(world_id=world_id, family=current.task.value, size=current.size.value,
            event=event, replicate=replicate, **choice,
            selected_branch_id=selected.branch_id if selected else None,
            comparator_branch_ids={p: siblings[p].branch_id if p in siblings else None for p in ("B", "C", "K")},
            prefix_parent=next(iter(siblings.values())).prefix_parent,
            boundary_provenance=provenance))
    return result
