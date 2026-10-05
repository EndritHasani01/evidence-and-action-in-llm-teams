"""Offline exact outcomes and §7.1 diagnostics, never imported by execution.

The saved schedule defines opportunities; the call ledger defines outcomes.
Gold and prefix correctness are evaluator-only. Tables are derived exports,
not another store. No tokenizer, inference provider or runner is needed.
"""

from collections import Counter, defaultdict
from contextlib import ExitStack
from dataclasses import asdict
from itertools import combinations
import gzip
import json
from pathlib import Path
import sqlite3

from .prompts import MAX_OUTPUT_TOKENS
from .schedule import dependency_order
from .tasks import PEERS, Task, candidate_contract
from .truth import changed_coordinates, exact_candidate, solve_world


def score_candidate(truth, status, candidate, peer):
    """Unknown execution is None; recorded invalid/failed replies are zero."""
    if status == "unknown":
        return None
    if status in ("invalid", "failed"):
        return 0
    if status != "valid" or candidate_contract(truth.task, truth.size, peer).error(candidate):
        raise ValueError("saved valid candidate violates the public contract")
    return int(exact_candidate(truth, candidate, peer))


def _values(truth, peer, status, candidate):
    # Check even wrong valid candidates; never coerce, sort, deduplicate or repair.
    score_candidate(truth, status, candidate, peer)
    if status != "valid":
        return {}
    coordinates = candidate_contract(truth.task, truth.size, peer).coordinates
    return ({j: candidate[str(j)] for j in coordinates} if truth.task is Task.BFS
            else dict(zip(coordinates, candidate)))


def score_coordinates(old, new, peer, status, candidate, prefix_status, prefix_candidate):
    """Return coordinate evidence and peer rates with explicit eligibility.

    Old-value persistence partitions D into new/old/other/malformed/unknown.
    Invalid/failed replies have no explicit value, while scoring zero for new
    accuracy and eligible preservation. Prefix eligibility uses only round four.
    """
    changes = changed_coordinates(old, new)
    values = _values(new, peer, status, candidate)
    prefix = _values(old, peer, prefix_status, prefix_candidate)
    old_values, new_values = old.by_coordinate, new.by_coordinate
    coordinates = candidate_contract(new.task, new.size, peer).coordinates
    rows = []
    for j in coordinates:
        changed = j in changes.changed
        prefix_correct = (None if prefix_status == "unknown" else
                          prefix_status == "valid" and prefix[j] == old_values[j])
        correct = (None if status == "unknown" else
                   int(status == "valid" and values[j] == new_values[j]))
        category = None
        if changed:
            category = ("unknown" if status == "unknown" else
                        "malformed_or_missing" if status != "valid" else
                        "new_gold" if correct else
                        "old_gold" if values[j] == old_values[j] else "other_valid")
        rows.append({"coordinate": j, "set": "D" if changed else "U",
            "old_gold": old_values[j], "new_gold": new_values[j],
            "value": values.get(j), "prefix_value": prefix.get(j),
            "new_correct": correct, "prefix_correct": prefix_correct,
            "preservation_eligible": None if prefix_status == "unknown" and not changed else
                bool(not changed and prefix_correct),
            "old_error_eligible": None if prefix_status == "unknown" and not changed else
                bool(not changed and prefix_status == "valid" and not prefix_correct),
            "changed_category": category,
            "changed_from_prefix": None if status != "valid" or prefix_status != "valid" else
                values[j] != prefix[j]})
    D = [r for r in rows if r["set"] == "D"]
    U = [r for r in rows if r["set"] == "U"]
    preserved = [r for r in U if r["preservation_eligible"]]
    old_errors = [r for r in U if r["old_error_eligible"]]
    metrics = []

    def rate(name, eligible, numerator, empty_reason, *, eligibility_unknown=False):
        denominator = None if eligibility_unknown else len(eligible)
        unknown = eligibility_unknown or status == "unknown" and bool(eligible)
        metrics.append({"metric": name, "denominator": denominator,
            "numerator": None if unknown else numerator,
            "rate": None if unknown or not denominator else numerator / denominator,
            "reason": ("prefix_round_four_unknown" if eligibility_unknown else
                       empty_reason if not denominator else "slot_unknown" if unknown else None),
            "eligible_coordinates": [r["coordinate"] for r in eligible]})

    rate("changed_accuracy", D, sum(r["new_correct"] or 0 for r in D), "no_changed_coordinates")
    for name, category in (("old_value_persistence", "old_gold"),
                           ("changed_other_valid", "other_valid"),
                           ("changed_malformed_or_missing", "malformed_or_missing")):
        rate(name, D, sum(r["changed_category"] == category for r in D), "no_changed_coordinates")
    unknown_prefix = prefix_status == "unknown" and bool(U)
    prefix_reason = ("prefix_round_four_not_protocol_valid" if prefix_status != "valid" else
                     "no_correct_prefix_U_coordinates")
    rate("preservation", preserved, sum(r["new_correct"] or 0 for r in preserved),
         "no_unchanged_coordinates" if not U else prefix_reason, eligibility_unknown=unknown_prefix)
    rate("collateral_damage", preserved, sum(r["new_correct"] == 0 for r in preserved),
         "no_unchanged_coordinates" if not U else prefix_reason, eligibility_unknown=unknown_prefix)
    rate("old_error_repair", old_errors, sum(r["new_correct"] or 0 for r in old_errors),
         "no_unchanged_coordinates" if not U else
         "prefix_round_four_not_protocol_valid" if prefix_status != "valid" else
         "no_old_prefix_U_errors", eligibility_unknown=unknown_prefix)
    return rows, metrics


def _joint(values):
    return None if None in values else int(all(values))


def trajectory(correctness):
    """Four rounds of four peer outcomes, with None for unknown opportunities.

    First/stable joint times and the four categories require complete execution.
    Observed first joint correctness and witnessed regression remain visible in
    incomplete branches, without inventing a recovery time for failed branches.
    """
    if (len(correctness) != 4 or any(len(r) != 4 for r in correctness)
            or any(type(c) is not int or c not in (0, 1)
                   for r in correctness for c in r if c is not None)):
        raise ValueError("trajectories require four rounds of four 0/1/unknown outcomes")
    joint = [_joint(r) for r in correctness]
    complete = all(c is not None for r in correctness for c in r)
    first = next((r for r, c in enumerate(joint, 1) if c == 1), None)
    stable = next((r for r in range(1, 5) if all(c == 1 for c in joint[r - 1:])), None) if complete else None
    regression = any(joint[r] == 0 and 1 in joint[:r] for r in range(4))
    individual_ever, peer_regression = [], []
    for peer in PEERS:
        values = [r[peer] for r in correctness]
        individual_ever.append(True if 1 in values else None if None in values else False)
        regressed = any(values[r] == 0 and 1 in values[:r] for r in range(4))
        peer_regression.append(True if regressed else None if None in values else False)
    category = ("incomplete" if not complete else
                "continuously_correct" if all(joint) else
                "correct_at_end_after_delay_or_regression" if joint[-1] else
                "temporarily_correct_but_incorrect_at_end" if first else "never_jointly_correct")
    return {"complete": complete, "category": category, "joint": joint,
        "mean_peer_correctness": [None if None in r else sum(r) / 4 for r in correctness],
        "auc": sum(c for r in correctness for c in r) / 16 if complete else None,
        "final_joint": joint[-1], "first_joint_round": first if complete else None,
        "observed_first_joint_round": first, "first_stable_joint_round": stable,
        "regression": True if regression else False if complete else None,
        "peer_regression": peer_regression, "individual_ever": individual_ever,
        "joint_ever": True if first else False if complete else None,
        "fragmented": all(individual_ever) and first is None if complete else None}


def identical_wrong_agreement(task, outcomes):
    """Only replicated full outputs can meaningfully agree on an identical answer."""
    if task in (Task.PREFIX, Task.SORT):
        return None
    if any(r["protocol_outcome"] == "unknown" for r in outcomes):
        return None
    return (all(r["protocol_outcome"] == "valid" and r["correct"] == 0 for r in outcomes)
            and all(r["candidate"] == outcomes[0]["candidate"] for r in outcomes))


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":"))


def candidate_payload(task, size, peer, candidate_state):
    """Decode the existing CandidateState wire format, including canonical BFS pairs.

    This is representation decoding, not answer repair. Verify keys before
    building a dictionary so duplicated/missing persisted pairs cannot vanish.
    """
    if candidate_state["status"] != "valid":
        if candidate_state["value"] is not None:
            raise ValueError("invalid/failed reply has a fabricated candidate")
        return None
    value = candidate_state["value"]
    if task is Task.BFS:
        keys = [str(j) for j in candidate_contract(task, size, peer).coordinates]
        if (type(value) is not list or any(type(v) is not list or len(v) != 2 for v in value)
                or [v[0] for v in value] != keys):
            raise ValueError("saved BFS candidate lacks canonical complete node pairs")
        value = dict(value)
    if candidate_contract(task, size, peer).error(value):
        raise ValueError("saved valid candidate violates the public contract")
    return value


def read_records(worlds, branches, paths):
    """Read application records in SQLite snapshots without checkpoint setup.

    Only saved pre-delivery peer state is needed for call-boundary annotations.
    Reading it directly avoids importing the runner or interpreting private
    LangGraph checkpoint serialization. Missing files never get created.
    """
    paths = tuple(Path(p).resolve() for p in paths)
    if len(set(paths)) != len(paths):
        raise ValueError("each worker file must be supplied once")
    expected_worlds = {w.world_id: _json(asdict(w)) for w in worlds}
    expected_branches = {b.branch_id: _json(asdict(b)) for b in branches}
    records, inputs, attempts, bindings = {}, {}, [], []
    with ExitStack() as stack:
        for worker, path in enumerate(paths):
            if not path.exists():
                continue
            con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
            stack.callback(con.close)
            con.row_factory = sqlite3.Row
            con.execute("PRAGMA query_only=ON")
            con.execute("BEGIN")
            for saved in con.execute("SELECT * FROM calls"):
                row = dict(saved, worker=worker, worker_file=path.name)
                if row["call_id"] in records:
                    raise ValueError("duplicate logical/physical call across worker files")
                records[row["call_id"]] = row
            for saved in con.execute("SELECT * FROM round_inputs"):
                row = dict(saved, worker=worker, worker_file=path.name)
                key = row["branch_id"], row["round_number"]
                if key in inputs:
                    raise ValueError("duplicate saved round inputs")
                if row["branch_json"] != expected_branches.get(row["branch_id"]):
                    raise ValueError("saved round branch differs from schedule")
                row["requests"] = json.loads(row.pop("requests_json"))
                inputs[key] = row
            attempts.extend(dict(r, worker=worker, worker_file=path.name)
                            for r in con.execute("SELECT * FROM attempts"))
            binding = con.execute("SELECT inputs_json FROM run_inputs WHERE singleton=1").fetchone()
            if binding:
                bound = json.loads(binding[0])
                for w in bound["worlds"]:
                    if _json(w) != expected_worlds.get(w["world_id"]):
                        raise ValueError("saved world inputs differ from evaluator manifest")
                # Workers may execute a declared subset of the full schedule.
                from .manifests import _branch
                for b in bound["branches"]:
                    if _json(b) != expected_branches.get(_branch(b).branch_id):
                        raise ValueError("saved run branch differs from evaluator schedule")
                if any(json.loads(r["settings_json"]) != bound["settings"]
                       for r in inputs.values() if r["worker"] == worker):
                    raise ValueError("saved requests differ from bound generation settings")
                bindings.append(bound)
        if bindings and any(b != bindings[0] for b in bindings):
            raise ValueError("worker run bindings differ")
    return records, inputs, sorted(attempts, key=lambda r: (r["call_id"], r["number"]))


def _recorded_outcome(branch, call, size, records, inputs):
    row = records.get(call.call_id)
    if row is None:
        return "unknown", None
    expected = (branch.branch_id, call.round_number, -1 if call.peer is None else call.peer,
                call.seed, call.generation_id, call.replay_parent)
    if tuple(row[k] for k in ("branch_id", "round_number", "peer", "seed", "generation_id", "replay_parent")) != expected:
        raise ValueError("saved call scope/seed/parent differs from schedule")
    barrier = inputs.get((branch.branch_id, call.round_number))
    if barrier is None or barrier["worker"] != row["worker"]:
        raise ValueError("recorded call lacks its original saved round input")
    status = row["status"]
    if status in ("pending", "running"):
        if any(row[k] is not None for k in ("raw_json", "failure_json", "validation_json")):
            raise ValueError("unfinished slot contains a completed outcome")
        return "unknown", None
    if status not in ("completed", "timeout", "infrastructure_failure", "replay"):
        raise ValueError("unrecognized recorded execution status")
    if (status == "replay") != (call.replay_parent is not None):
        raise ValueError("saved replay status differs from scheduled parent")
    physical = row
    if call.replay_parent:
        physical = records.get(call.generation_id)
        if (physical is None or physical["replay_parent"] is not None
                or physical["status"] not in ("completed", "timeout", "infrastructure_failure")):
            raise ValueError("replay lacks its original physical outcome")
        if row["raw_json"] is not None or row["failure_json"] is not None:
            raise ValueError("replay duplicates a physical outcome")
        parent_input = inputs[(physical["branch_id"], physical["round_number"])]
        if (row["validation_json"] != physical["validation_json"]
                or row["seed"] != physical["seed"]
                or barrier["settings_json"] != parent_input["settings_json"]):
            raise ValueError("replay validation/seed/settings differs from parent")
        for field in ("rendered", "tokenized"):
            if barrier["requests"][field][call.peer] != parent_input["requests"][field][call.peer]:
                raise ValueError("replayed exact request differs from parent")
        child_state = json.loads(barrier["requests"]["before"])
        parent_state = json.loads(parent_input["requests"]["before"])
        if (any(child_state[k] != parent_state[k] for k in ("task", "size", "manifest"))
                or child_state["peers"][call.peer] != parent_state["peers"][call.peer]):
            raise ValueError("replayed permitted peer state differs from parent")
    failure = physical["status"] in ("timeout", "infrastructure_failure")
    validation = json.loads(row["validation_json"]) if row["validation_json"] else None
    phase = "recovery" if branch.phase == "continuation" else branch.phase
    if validation and (validation["candidate"]["slot"] != {"phase": phase, "round_number": call.round_number}
                       or validation["candidate"]["historical"] is not False):
        raise ValueError("saved candidate belongs to another opportunity")
    if failure:
        if (not physical["failure_json"] or physical["raw_json"] is not None
                or json.loads(physical["failure_json"])["status"] != physical["status"]
                or validation and (validation["candidate"]["status"] != "failed"
                                   or validation["generated"] is not None)):
            raise ValueError("recorded failure differs from saved outcome")
        if validation:
            candidate_payload(branch.task, size, call.peer, validation["candidate"])
        return "failed", None
    if not physical["raw_json"] or physical["failure_json"] is not None:
        raise ValueError("completed generation lacks an exact raw reply")
    if validation is None:
        raise ValueError("completed raw reply lacks saved protocol validation; resume validation before scoring")
    raw = json.loads(physical["raw_json"])
    if validation["generated"] != raw:
        raise ValueError("saved validation differs from exact raw reply")
    candidate = validation["candidate"]
    if candidate["status"] not in ("valid", "invalid"):
        raise ValueError("saved candidate belongs to another opportunity")
    if candidate["status"] == "valid":
        value = candidate_payload(branch.task, size, call.peer, candidate)
        if (not all(validation[k] is True for k in ("json_valid", "schema_valid", "permissions_valid"))
                or raw["truncated"] or len(raw["token_ids"]) > MAX_OUTPUT_TOKENS
                or json.loads(raw["text"])["candidate"] != value):
            raise ValueError("saved valid candidate differs from literal reply/validity")
    elif candidate["value"] is not None:
        raise ValueError("invalid reply has a fabricated candidate")
    return candidate["status"], candidate_payload(branch.task, size, call.peer, candidate)


def _check_inputs(worlds, branches, inputs):
    """Check original/event sources even in manually started, unbound workers."""
    by_branch = {b.branch_id: b for b in branches}
    for (branch_id, number), saved in inputs.items():
        branch = by_branch.get(branch_id)
        if branch is None or number not in {c.round_number for c in branch.calls}:
            raise ValueError("unscheduled saved round input")
        prepared = worlds[branch.world_id]
        current = prepared.world if branch.event == "original" else prepared.event_world(branch.event)
        expected = {r.record_id: asdict(r) for r in current.records}
        data = saved["requests"]
        phase = "recovery" if branch.phase == "continuation" else branch.phase
        if branch.phase == "control":
            state, peers, slot = data["view"], [data["view"]], data["view"]["slot"]
        else:
            state, slot = json.loads(data["before"]), data["slot"]
            peers = state["peers"]
            if state["branch_id"] != branch_id or state["phase"] != phase or len(peers) != 4:
                raise ValueError("saved state differs from branch scope")
        if (state["task"] != branch.task.value or state["size"] != current.size.value
                or slot != {"phase": phase, "round_number": number}):
            raise ValueError("saved input differs from task/size/opportunity")
        for peer in peers:
            if len({s["record_id"] for s in peer["sources"]}) != len(peer["sources"]):
                raise ValueError("duplicate saved source in evaluator input")
            for source in peer["sources"]:
                record = expected.get(source["record_id"])
                if record is not None and "value" not in source:
                    record = {k: record[k] for k in ("record_id", "owner", "position", "version")}
                if record is None or _json(record) != _json(source):
                    raise ValueError("saved current source differs from evaluator manifest")


def _availability(branch, call, prepared, inputs):
    if branch.phase != "continuation" or branch.event == "sham":
        return {"v2_available": None, "v2_reason": "not_applicable", "v2_delivery_ids": []}
    saved = inputs.get((branch.branch_id, call.round_number))
    if saved is None:
        return {"v2_available": None, "v2_reason": "call_boundary_unknown", "v2_delivery_ids": []}
    before = json.loads(saved["requests"]["before"])
    if (before["branch_id"] != branch.branch_id or before["task"] != branch.task.value
            or before["size"] != prepared.world.size.value or before["phase"] != "recovery"):
        raise ValueError("saved call-boundary state differs from scheduled scope")
    edit = prepared.main_edit if branch.event == "revision" else prepared.preserving_edit
    known = next((s for s in before["peers"][call.peer]["sources"]
                  if s["record_id"] == edit.record_id and s["version"] == 2 and "value" in s), None)
    deliveries = [d for d in before["deliveries"] if d["recipient"] == call.peer and d["source"]
                  and d["source"]["record_id"] == edit.record_id and d["source"]["version"] == 2
                  and d["first_usable"] is not None]
    if known is not None and not deliveries:
        raise ValueError("known v2 lacks archived delivery provenance")
    return {"v2_available": known is not None, "v2_reason": None,
            "v2_delivery_ids": [d["delivery_id"] for d in deliveries]}


METRIC_KEYS = ("size", "phase", "event", "policy", "replicate", "round", "metric")
ANNOTATIONS = ("protocol_inference_failure", "v2_unavailable", "incorrect_after_v2",
               "explicit_old_value_persistence", "collateral_error", "regression")


def aggregate_diagnostics(peers):
    """Eligible peers → worlds → equal eligible families, never pooled coordinates."""
    worlds, families, pooled = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in peers:
        key = tuple(row[k] for k in METRIC_KEYS)
        worlds[(*key, row["family"], row["world_id"], row["branch_id"])].append(row)
        families[(*key, row["family"])].append(row)
        pooled[key].append(row)
    result, world_children, family_children = [], defaultdict(list), defaultdict(list)

    def summary(rows, children, level):
        known = [r for r in rows if r["denominator"] and r["denominator"] > 0]
        unknown_prefix = sum(r["denominator"] is None for r in rows)
        eligible = [r for r in children if r["denominator"] is None or r["denominator"] > 0]
        unknown = unknown_prefix or any(r["rate"] is None for r in eligible)
        coordinates = {(r["world_id"], j) for r in rows for j in r["eligible_coordinates"]}
        copies = sum(r["denominator"] or 0 for r in rows)
        row = {k: rows[0][k] for k in METRIC_KEYS}
        row.update(level=level, world_id=rows[0]["world_id"] if level == "world" else None,
            branch_id=rows[0]["branch_id"] if level == "world" else None,
            family=rows[0]["family"] if level != "all_families" else None,
            denominator=None if unknown_prefix else copies,
            numerator=None if unknown else sum(r["numerator"] or 0 for r in rows),
            rate=None if unknown or not eligible else sum(r["rate"] for r in eligible) / len(eligible),
            reason="prefix_round_four_unknown" if unknown_prefix else "slot_unknown" if unknown else
                "no_eligible_coordinates" if not eligible else None,
            scheduled_peers=len(rows), eligible_peers=len(known),
            observed_eligible_peers=sum(r["rate"] is not None for r in known),
            unknown_eligibility_peers=unknown_prefix,
            scheduled_worlds=len({r["world_id"] for r in rows}),
            eligible_worlds=len({r["world_id"] for r in known}),
            scheduled_families=len({r["family"] for r in rows}),
            eligible_families=len({r["family"] for r in known}),
            unique_coordinate_count=None if unknown_prefix else len(coordinates),
            peer_copy_count=None if unknown_prefix else copies,
            known_unique_coordinate_count=len(coordinates), known_peer_copy_count=copies)
        return row

    for key, rows in worlds.items():
        row = summary(rows, rows, "world")
        world_children[key[:len(METRIC_KEYS) + 1]].append(row)
        result.append(row)
    for key, rows in families.items():
        row = summary(rows, world_children[key], "family")
        family_children[key[:len(METRIC_KEYS)]].append(row)
        result.append(row)
    for key, rows in pooled.items():
        result.append(summary(rows, family_children[key], "all_families"))
    return result


def annotation_counts(rows):
    """Inclusive pair intersections plus exact patterns retain higher overlaps.

    The analysis unit is a scheduled peer-round, including unknown slots. These
    are counts, not independent samples or a partition of failure causes.
    """
    grouping = ("size", "phase", "event", "policy", "replicate")
    groups = defaultdict(list)
    for row in rows:
        base = tuple(row[k] for k in grouping)
        groups[("world", *base, row["family"], row["world_id"], row["branch_id"])].append(row)
        groups[("family", *base, row["family"], None, None)].append(row)
        groups[("all_families", *base, None, None, None)].append(row)
    result = []
    for key, group in groups.items():
        counts = {}
        for label in ANNOTATIONS:
            applicable = [r for r in group if r["reasons"].get(label) != "not_applicable"]
            counts[label] = {"applicable": len(applicable),
                "observed": sum(r["labels"][label] is not None for r in applicable),
                "positive": sum(r["labels"][label] is True for r in applicable),
                "unknown": sum(r["labels"][label] is None for r in applicable),
                "not_applicable": len(group) - len(applicable)}
        intersections = []
        for left, right in combinations(ANNOTATIONS, 2):
            applicable = [r for r in group if all(r["reasons"].get(k) != "not_applicable" for k in (left, right))]
            intersections.append({"labels": [left, right], "applicable": len(applicable),
                "observed": sum(all(r["labels"][k] is not None for k in (left, right)) for r in applicable),
                "positive": sum(all(r["labels"][k] is True for k in (left, right)) for r in applicable)})
        patterns = Counter((tuple(k for k in ANNOTATIONS if r["labels"][k] is True),
                            tuple(k for k in ANNOTATIONS if r["labels"][k] is None and r["reasons"].get(k) != "not_applicable"),
                            tuple(k for k in ANNOTATIONS if r["reasons"].get(k) == "not_applicable")) for r in group)
        result.append(dict(zip(("level", *grouping, "family", "world_id", "branch_id"), key),
            unit="scheduled_peer_round", scheduled=len(group), counts=counts, intersections=intersections,
            patterns=[{"positive_labels": list(p[0]), "unknown_labels": list(p[1]),
                       "not_applicable_labels": list(p[2]), "count": count} for p, count in sorted(patterns.items())]))
    return result


def evaluate_records(worlds, branches, records, inputs, attempts=()):
    """Join the entire supplied manifest before deriving any offline outcomes."""
    worlds, branches = tuple(worlds), tuple(sorted(branches, key=lambda b: b.branch_id))
    dependency_order(branches)
    by_world, by_branch = {w.world_id: w for w in worlds}, {b.branch_id: b for b in branches}
    if len(by_world) != len(worlds) or len(by_branch) != len(branches):
        raise ValueError("duplicate world/branch in evaluation manifest")
    scheduled = {c.call_id: (b, c) for b in branches for c in b.calls}
    if len(scheduled) != sum(len(b.calls) for b in branches) or records.keys() - scheduled.keys():
        raise ValueError("duplicate or unscheduled call in evaluation records")
    if any(b.world_id not in by_world or b.task is not by_world[b.world_id].world.task for b in branches):
        raise ValueError("scheduled branch lacks matching prepared world")
    _check_inputs(by_world, branches, inputs)
    by_attempt = defaultdict(list)
    for attempt in attempts:
        scope = scheduled.get(attempt["call_id"])
        if scope is None or scope[1].replay_parent or attempt["call_id"] not in records:
            raise ValueError("unscheduled/replayed attempt or missing physical record")
        if attempt["number"] in by_attempt[attempt["call_id"]]:
            raise ValueError("duplicate physical attempt")
        by_attempt[attempt["call_id"]].append(attempt["number"])
    # This full join also establishes the sole final-prefix outcome per peer.
    replies = {c.call_id: _recorded_outcome(b, c, by_world[b.world_id].world.size, records, inputs)
               for b, c in scheduled.values()}
    outcomes, coordinates, diagnostics, rounds, trajectories, annotations = [], [], [], [], [], []
    for branch in branches:
        prepared = by_world[branch.world_id]
        old = solve_world(prepared.world)
        new = old if branch.event == "original" else solve_world(prepared.event_world(branch.event))
        base = {"branch_id": branch.branch_id, "world_id": branch.world_id, "family": branch.task.value,
                "size": prepared.world.size.value, "phase": branch.phase, "event": branch.event,
                "policy": branch.policy, "replicate": branch.replicate, "prefix_parent": branch.prefix_parent}
        branch_outcomes = []
        prefix_calls = ({c.peer: c for c in by_branch[branch.prefix_parent].calls if c.round_number == 4}
                        if branch.prefix_parent else {})
        for call in sorted(branch.calls, key=lambda c: (c.round_number, -1 if c.peer is None else c.peer)):
            status, candidate = replies[call.call_id]
            saved = records.get(call.call_id)
            prefix_call = prefix_calls.get(call.peer)
            prefix_status, prefix_candidate = replies[prefix_call.call_id] if prefix_call else ("unknown", None)
            correct = score_candidate(new, status, candidate, call.peer)
            row = dict(base, call_id=call.call_id, generation_id=call.generation_id, replay_parent=call.replay_parent,
                round=call.round_number, peer=call.peer, seed=call.seed,
                execution_status=saved["status"] if saved else "unexecuted", protocol_outcome=status,
                candidate=candidate, correct=correct, worker=saved["worker"] if saved else None,
                worker_file=saved["worker_file"] if saved else None,
                outcome_call_id=call.generation_id if status != "unknown" else None,
                attempt_numbers=by_attempt[call.generation_id],
                prefix_call_id=prefix_call.call_id if prefix_call else None,
                prefix_protocol_outcome=prefix_status if prefix_call else None,
                prefix_correct=score_candidate(old, prefix_status, prefix_candidate, call.peer) if prefix_call else None)
            row.update(_availability(branch, call, prepared, inputs))
            outcomes.append(row)
            branch_outcomes.append(row)
            metrics = []
            if branch.phase == "continuation":
                coord, metrics = score_coordinates(old, new, call.peer, status, candidate, prefix_status, prefix_candidate)
                identity = {k: row[k] for k in (*base, "call_id", "generation_id", "replay_parent", "round", "peer", "prefix_call_id")}
                coordinates.extend(dict(identity, **r) for r in coord)
                diagnostics.extend(dict(identity, **r) for r in metrics)
            if call.peer is not None:
                labels = {k: None for k in ANNOTATIONS}
                reasons = {k: "not_applicable" for k in ANNOTATIONS}
                labels["protocol_inference_failure"] = None if status == "unknown" else status != "valid"
                reasons["protocol_inference_failure"] = "slot_unknown" if status == "unknown" else None
                if row["v2_reason"] != "not_applicable":
                    labels["v2_unavailable"] = None if row["v2_available"] is None else not row["v2_available"]
                    labels["incorrect_after_v2"] = (False if row["v2_available"] is False or correct == 1 else
                        None if row["v2_available"] is None or correct is None else correct == 0)
                    reasons["v2_unavailable"] = row["v2_reason"]
                    reasons["incorrect_after_v2"] = "outcome_or_boundary_unknown" if labels["incorrect_after_v2"] is None else None
                for label, name in (("explicit_old_value_persistence", "old_value_persistence"),
                                    ("collateral_error", "collateral_damage")):
                    if metrics:
                        rate = next(r for r in metrics if r["metric"] == name)
                        labels[label] = None if rate["denominator"] == 0 or rate["numerator"] is None else rate["numerator"] > 0
                        reasons[label] = "not_applicable" if rate["denominator"] == 0 else rate["reason"]
                earlier = [r["correct"] for r in branch_outcomes if r["peer"] == call.peer and r["round"] < call.round_number]
                labels["regression"] = (False if correct == 1 else True if correct == 0 and 1 in earlier else
                    None if correct is None or None in earlier else False)
                reasons["regression"] = "prior_or_current_slot_unknown" if labels["regression"] is None else None
                annotations.append({k: row[k] for k in (*base, "call_id", "generation_id", "replay_parent", "round", "peer",
                    "worker", "worker_file", "prefix_call_id", "prefix_correct", "v2_delivery_ids")}
                    | {"labels": labels, "reasons": reasons})
        if branch.phase != "control":
            matrix = [[r["correct"] for r in branch_outcomes if r["round"] == number] for number in range(1, 5)]
            result = trajectory(matrix)
            trajectories.append(dict(base, **result))
            for number in range(1, 5):
                peers = [r for r in branch_outcomes if r["round"] == number]
                rounds.append(dict(base, round=number, mean_peer_correctness=result["mean_peer_correctness"][number - 1],
                    joint=result["joint"][number - 1], scheduled=4,
                    recorded=sum(r["correct"] is not None for r in peers),
                    identical_wrong_agreement=identical_wrong_agreement(branch.task, peers),
                    call_ids=[r["call_id"] for r in peers], generation_ids=[r["generation_id"] for r in peers]))
    return {"kind": "Offline exact outcomes and trajectories; scripted fixtures are validation, not empirical findings",
            "coverage": {"scheduled": len(outcomes), "recorded": sum(r["correct"] is not None for r in outcomes),
                "unknown": sum(r["correct"] is None for r in outcomes),
                "protocol_outcomes": dict(sorted(Counter(r["protocol_outcome"] for r in outcomes).items()))},
            "outcomes": outcomes, "coordinates": coordinates, "peer_diagnostics": diagnostics,
            "diagnostic_summaries": aggregate_diagnostics(diagnostics), "rounds": rounds,
            "trajectories": trajectories, "annotations": annotations, "annotation_counts": annotation_counts(annotations),
            "attempts": list(attempts)}


def evaluate_run(worlds, branches, paths):
    worlds, branches = tuple(worlds), tuple(branches)
    records, inputs, attempts = read_records(worlds, branches, paths)
    return evaluate_records(worlds, branches, records, inputs, attempts)


def write_evaluation(path, tables):
    """Exclusively create a derived JSON export, optionally gzip compressed."""
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "xt", encoding="utf-8", newline="\n") as output:
        json.dump(tables, output, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":"))
        output.write("\n")
