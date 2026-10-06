"""Original ledger costs and offline whole-policy analysis (spec section 7.3).

Physical attempts/allocation are charged once. Hypothetical policies charge the
original prefix and all sixteen logical calls, including original replay costs.
The allocation partition reconciles wall clocks; it is never added to attempts.
"""

from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
import json
from types import SimpleNamespace

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


def _initial_state(branch, inputs, committed):
    saved = inputs.get((branch.branch_id, 1))
    if saved:
        return json.loads(saved["requests"]["before"])
    state = committed.get(branch.branch_id, {}).get("state")
    if state and (not state.get("last_slot") or state["last_slot"]["phase"] == "prefix"):
        return state
    return None


def _delivery_views(branches, inputs, committed, outcomes, worlds):
    """The existing committed delivery IDs, counted once across shared prefixes."""
    from .information import source_inventory
    by_branch = {b.branch_id: b for b in branches}
    by_world = {w.world_id: w for w in worlds}
    states, complete = defaultdict(list), set()
    for (bid, _), saved in inputs.items():
        if by_branch[bid].phase != "control":
            states[bid].append(json.loads(saved["requests"]["before"]))
    for bid, saved in committed.items():
        branch, state = by_branch.get(bid), saved["state"]
        if (branch is None or branch.phase == "control" or not state.get("committed")
                or state["branch_id"] != bid or state["task"] != branch.task.value
                or state["phase"] != ("recovery" if branch.phase == "continuation" else branch.phase)):
            raise ValueError("committed cost state differs from schedule")
        current = by_world[branch.world_id].world if branch.event == "original" else by_world[branch.world_id].event_world(branch.event)
        if state["size"] != current.size.value:
            raise ValueError("committed cost size differs from manifest")
        for peer in range(4):
            source_inventory(current, state["peers"][peer]["sources"], peer)
        slot = state["last_slot"]
        number = slot["round_number"] if slot and slot["phase"] == state["phase"] else 0
        if any(outcomes[c.call_id]["protocol_outcome"] == "unknown" for c in branch.calls if c.round_number <= number):
            raise ValueError("committed cost state includes unexecuted outcomes")
        if number == 4:
            if state["pending"]:
                raise ValueError("complete cost checkpoint retains pending deliveries")
            complete.add(bid)
        states[bid].append(state)
    deliveries, branch_ids = {}, defaultdict(set)
    for bid, saved_states in states.items():
        branch = by_branch[bid]
        for state in saved_states:
            for d in state["deliveries"]:
                previous = deliveries.get(d["delivery_id"])
                if previous is not None and previous != d:
                    raise ValueError("shared delivery changed across cost inputs")
                deliveries[d["delivery_id"]] = d
                branch_ids[bid].add(d["delivery_id"])
                if branch.prefix_parent and (d.get("generated") or {}).get("phase") == "prefix":
                    branch_ids[branch.prefix_parent].add(d["delivery_id"])
            if branch.prefix_parent and (state.get("last_slot") or {}).get("phase") == "prefix":
                complete.add(branch.prefix_parent)
    return deliveries, branch_ids, complete


def _delivery_counts(deliveries):
    return {"source_attempts": sum(d.get("source") is not None for d in deliveries),
            "source_acquisitions": sum(d.get("acquired") is True for d in deliveries),
            "text_deliveries": sum(d.get("text") is not None for d in deliveries)}


def _selection_frequencies(selections):
    groups = defaultdict(list)
    for row in selections:
        base = row["size"], row["event"], row["replicate"]
        groups[("family", *base, row["family"])].append(row)
        groups[("pooled", *base, None)].append(row)
    result = []
    for key, rows in sorted(groups.items(), key=lambda r: str(r[0])):
        counts = {p: sum(r["selected_policy"] == p for r in rows) for p in ("C", "K")}
        unknown = sum(r["selected_policy"] is None for r in rows)
        constant = next((p for p, count in counts.items() if count == len(rows)), None)
        statement = (f"The boundary rule is constant: it selects {constant} for all {len(rows)} worlds."
            if constant else f"Rule constancy is unknown: {unknown} initial boundaries are unavailable."
            if unknown else "The boundary rule selects both C and K in this population.")
        result.append(dict(zip(("level", "size", "event", "replicate", "family"), key),
            scheduled_worlds=len(rows), observed_selections=len(rows) - unknown,
            counts=counts, unknown_selections=unknown,
            frequencies={p: count / len(rows) for p, count in counts.items()},
            frequency_denominator=len(rows), complete_selected_branches=sum(r["available"] for r in rows),
            constant_policy=constant, statement=statement, world_ids=[r["world_id"] for r in rows]))
    return result


def _paired_seconds(chosen, comparator, generations):
    coefficients = Counter(chosen)
    coefficients.subtract(comparator)
    return [sum(n * generations[cid]["seconds"][j if n > 0 else 1 - j]
                for cid, n in coefficients.items() if n) for j in (0, 1)]


def cost_records(worlds, branches, records, inputs, attempts=(), *, committed=None,
                 allocations=(), processes=(), budgets=(), now=None, tables=None):
    """Derive auditable costs and whole-branch comparisons, never feed execution.

    The unchanged M3 totals are retained as measured subtotals. Unknown scheduled
    work makes the complete policy cost unavailable, even if a replay parent has
    already been measured. Unavailable output/memory measurements remain explicit.
    """
    from .evaluate import evaluate_records
    from .information import source_inventory
    worlds, branches, committed = tuple(worlds), tuple(sorted(branches, key=lambda b: b.branch_id)), committed or {}
    attempts, allocations, processes = tuple(attempts), tuple(allocations), tuple(processes)
    now = now or datetime.now(timezone.utc).isoformat()
    timestamp(now)
    tables = evaluate_records(worlds, branches, records, inputs, attempts) if tables is None else tables
    outcomes = {r["call_id"]: r for r in tables["outcomes"]}
    by_branch, by_world = {b.branch_id: b for b in branches}, {w.world_id: w for w in worlds}
    records = {cid: dict(r) for cid, r in records.items()}
    for row in records.values():
        saved = inputs.get((row["branch_id"], row["round_number"]))
        if saved:
            tokenized = saved["requests"]["tokenized"]
            count = len((tokenized if row["peer"] == -1 else tokenized[row["peer"]])["input_ids"])
            if row.get("request_tokens") is not None and row["request_tokens"] != count:
                raise ValueError("ledger request count differs from exact saved token IDs")
            row["request_tokens"] = count
    attempts = [dict(a) for a in attempts]
    by_attempt = defaultdict(list)
    for a in attempts:
        a["device"] = next((d["device"] for d in reversed(allocations)
            if d["worker"] == a["worker"] and timestamp(d["started_at"]) <= timestamp(a["started_at"])
            <= timestamp(d["stopped_at"] or now)), f"worker:{a['worker']}")
        by_attempt[a["call_id"]].append(a)
    for branch in branches:
        for call in branch.calls:
            if not call.replay_parent and records.get(call.call_id, {}).get("status") in FINAL and not by_attempt[call.call_id]:
                raise ValueError("recorded original outcome lacks physical attempt costs")
    configs = list(budgets) + [json.loads(a["budget_json"]) for a in allocations if a.get("budget_json")]
    if configs and any(c != configs[0] for c in configs):
        raise ValueError("allocation budget bindings differ")
    budget = SimpleNamespace(**configs[0]) if configs else None
    resources = _allocation_resources(allocations, attempts, processes, now, budget)
    generations = ledger_generation_costs(branches, records, attempts, now)
    physical = physical_costs(generations, attempts, now)
    physical.update(scheduled_generations=len(generations), attempts=len(attempts),
        finished_generations=sum(records.get(cid, {}).get("status") in FINAL for cid in generations),
        unknown_generations=sum(records.get(cid, {}).get("status") not in FINAL for cid in generations),
        retries=sum(a["number"] == 2 for a in attempts),
        uncertain_attempts=sum(a["uncertain_completion"] for a in attempts),
        unknown_duration_attempts=sum(a["elapsed_seconds"] is None for a in attempts),
        unknown_peak_memory_attempts=sum(a.get("peak_memory_bytes") is None for a in attempts))
    physical["recorded_failure_generations"] = sum(outcomes[cid]["protocol_outcome"] in ("invalid", "failed") for cid in generations)
    deliveries, delivery_ids, delivery_complete = _delivery_views(branches, inputs, committed, outcomes, worlds)
    policy_costs, quality, evidence = [], [], []
    trajectories = {r["branch_id"]: r for r in tables["trajectories"]}
    preservation_by_branch = defaultdict(list)
    for r in tables["diagnostic_summaries"]:
        if r["level"] == "world" and r["metric"] == "preservation":
            preservation_by_branch[r["branch_id"]].append(r)
    for row in ledger_policy_costs(branches, records, generations):
        branch = by_branch[row["branch_id"]]
        used = (*by_branch[branch.prefix_parent].calls, *branch.calls) if branch.prefix_parent else branch.calls
        uses = [generations[c.generation_id] for c in used]
        attempt_uses = [a for c in used for a in by_attempt[c.generation_id]]
        identity = dict(world_id=branch.world_id, size=by_world[branch.world_id].world.size.value,
                        phase=branch.phase, prefix_parent=branch.prefix_parent)
        ids = delivery_ids[branch.branch_id] | (delivery_ids[branch.prefix_parent] if branch.prefix_parent else set())
        horizon = branch.branch_id in delivery_complete and (not branch.prefix_parent or branch.prefix_parent in delivery_complete)
        measured = row["unknown_calls"] == 0
        row.update(identity, call_ids=[c.call_id for c in used], generation_ids=[c.generation_id for c in used],
            attempts=sum(c["attempts"] for c in uses), retries=sum(a["number"] == 2 for a in attempt_uses),
            unknown_duration_attempt_uses=sum(c["unknown_duration_attempts"] for c in uses),
            unknown_peak_memory_attempt_uses=sum(a.get("peak_memory_bytes") is None for a in attempt_uses),
            peak_memory_bytes=max((c["peak_memory_bytes"] for c in uses if c["peak_memory_bytes"] is not None), default=None),
            protocol_outcomes=dict(sorted(Counter(outcomes[c.call_id]["protocol_outcome"] for c in used).items())),
            complete=measured, complete_policy_seconds=row["seconds"] if measured else None,
            complete_request_tokens=row["request_tokens"] if measured and not row["unknown_request_calls"] else None,
            complete_output_tokens=row["output_tokens"] if measured and not row["unknown_output_attempt_uses"] else None,
            observed_deliveries=_delivery_counts([deliveries[d] for d in sorted(ids)]),
            complete_delivery_horizon=horizon,
            complete_deliveries=_delivery_counts([deliveries[d] for d in sorted(ids)]) if horizon else None,
            delivery_ids=sorted(ids), overhead_rule=OVERHEAD_RULE,
            external_overhead_attribution="Experiment allocation overhead, reported separately; no per-policy reassignment.")
        policy_costs.append(row)
        if branch.phase != "continuation":
            continue
        base = {k: row[k] for k in ("branch_id", "world_id", "family", "size", "event", "policy", "replicate", "prefix_parent")}
        preservation = preservation_by_branch[branch.branch_id]
        trajectory = trajectories[branch.branch_id]
        stable = trajectory["first_stable_joint_round"]
        continuation_ids = {c.call_id for c in branch.calls}
        stable_used = [c for c in used if c.call_id not in continuation_ids or stable and c.round_number <= stable]
        quality.append(dict(base, complete=trajectory["complete"], auc=trajectory["auc"], final_joint=trajectory["final_joint"],
            trajectory=trajectory, preservation=preservation, cost_branch_id=branch.branch_id,
            retrospective_stable_completion=dict(round=stable,
                seconds=[sum(generations[c.generation_id]["seconds"][j] for c in stable_used) for j in (0, 1)] if stable and measured else None,
                call_ids=[c.call_id for c in stable_used] if stable else [],
                reason="complete_policy_or_stable_completion_unavailable" if not stable or not measured else None,
                interpretation="Retrospective oracle-recognized completion within four rounds; the fixed schedule still executes all calls.")))
        initial = _initial_state(branch, inputs, committed)
        current = by_world[branch.world_id].event_world(branch.event)
        for peer in range(4):
            evidence.append(dict(base, peer=peer, inventory=source_inventory(current, initial["peers"][peer]["sources"], peer) if initial else None,
                reason=None if initial else "initial_coverage_unknown"))
    by_cost, by_quality = {r["branch_id"]: r for r in policy_costs}, {r["branch_id"]: r for r in quality}
    selections = boundary_selections(worlds, branches, inputs, committed=committed)
    strategy_worlds, comparisons = [], []
    for selection in selections:
        strategies = {"boundary_rule": selection["selected_branch_id"],
                      **{f"always_{p}": bid for p, bid in selection["comparator_branch_ids"].items()}}
        rows = {}
        for strategy, bid in strategies.items():
            q, cost = by_quality.get(bid), by_cost.get(bid)
            available = bool(q and q["complete"] and cost["complete"])
            reason = (None if available else "initial_coverage_unknown" if strategy == "boundary_rule" and selection["selected_policy"] is None
                      else "branch_unscheduled" if bid is None else "branch_or_prefix_incomplete")
            preservation = next((r for r in q["preservation"] if r["round"] == 4), None) if q else None
            row = {k: selection[k] for k in ("world_id", "family", "size", "event", "replicate", "prefix_parent")}
            row.update(strategy=strategy, selected_policy=selection["selected_policy"] if strategy == "boundary_rule" else strategy[-1],
                branch_id=bid, cost_branch_id=bid, available=available, reason=reason,
                auc=q["auc"] if available else None, final_joint=q["final_joint"] if available else None,
                preservation=preservation, complete_policy_seconds=cost["complete_policy_seconds"] if available else None,
                auc_denominator=16, final_peer_denominator=4,
                continuation_call_ids=[c.call_id for c in by_branch[bid].calls] if bid else [],
                continuation_generation_ids=[c.generation_id for c in by_branch[bid].calls] if bid else [],
                call_ids=cost["call_ids"] if cost else [], generation_ids=cost["generation_ids"] if cost else [])
            strategy_worlds.append(row)
            rows[strategy] = row
        selection.update(available=rows["boundary_rule"]["available"], unavailable_reason=rows["boundary_rule"]["reason"])
        for policy in ("B", "C", "K"):
            chosen, comparator = rows["boundary_rule"], rows[f"always_{policy}"]
            available = chosen["available"] and comparator["available"]
            p0, p1 = chosen["preservation"], comparator["preservation"]
            comparisons.append({k: selection[k] for k in ("world_id", "family", "size", "event", "replicate", "prefix_parent")} | dict(
                comparator=policy, selected_policy=selection["selected_policy"], selected_branch_id=chosen["branch_id"],
                comparator_branch_id=comparator["branch_id"], paired_available=available,
                auc_difference=chosen["auc"] - comparator["auc"] if available else None,
                final_joint_difference=chosen["final_joint"] - comparator["final_joint"] if available else None,
                preservation_difference=p0["rate"] - p1["rate"] if available and p0 and p1 and p0["rate"] is not None and p1["rate"] is not None else None,
                preservation_components=[p0, p1],
                policy_seconds_difference=_paired_seconds(chosen["generation_ids"], comparator["generation_ids"], generations) if available else None))
    generation_rows = []
    for branch in branches:
        for call in branch.calls:
            if call.replay_parent:
                continue
            generation_rows.append(dict(generations[call.call_id], call_id=call.call_id,
                branch_id=branch.branch_id, world_id=branch.world_id, family=branch.task.value,
                phase=branch.phase, event=branch.event, policy=branch.policy, replicate=branch.replicate,
                round=call.round_number, peer=call.peer, execution_status=outcomes[call.call_id]["execution_status"],
                protocol_outcome=outcomes[call.call_id]["protocol_outcome"],
                attempt_numbers=outcomes[call.call_id]["attempt_numbers"]))
    return dict(kind="Offline measured costs and frozen descriptive boundary rule; scripted data are CPU validation",
        at=now, physical=physical, generations=generation_rows,
        policy_costs=policy_costs, resources=resources, overhead_rule=OVERHEAD_RULE,
        validated_deliveries=[deliveries[d] for d in sorted(deliveries)], delivery_counts=_delivery_counts(list(deliveries.values())),
        retained_evidence=evidence, quality_preservation=quality,
        boundary_selections=selections, selection_frequencies=_selection_frequencies(selections),
        strategy_worlds=strategy_worlds, paired_comparisons=comparisons)


def costs_run(worlds, branches, paths, *, now=None, diagnostics=False, estimands=False, tokenizer=None):
    """One read-only snapshot per original worker, with optional other M4 tables."""
    from .evaluate import evaluate_records, read_records
    worlds, branches = tuple(worlds), tuple(branches)
    records, inputs, attempts, committed, resources = read_records(worlds, branches, paths,
        include_committed=True, include_resources=True)
    tables = evaluate_records(worlds, branches, records, inputs, attempts)
    tables["costs"] = cost_records(worlds, branches, records, inputs, attempts, committed=committed,
        allocations=resources["allocations"], processes=resources["processes"], budgets=resources["budgets"], now=now, tables=tables)
    if diagnostics:
        from .information import information_records
        tables["information"] = information_records(worlds, branches, records, inputs, attempts,
            committed=committed, tokenizer=tokenizer, tables=tables)
    if estimands:
        from .analysis import analyze_estimands, prose_activity
        tables["estimands"] = analyze_estimands(worlds, branches, tables)
        tables["estimands"]["prose_activity"] = prose_activity(worlds, branches, inputs)
    return tables
