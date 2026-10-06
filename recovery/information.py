"""Offline §7.2 inventories and references. Never imported by execution.

Sources, literal derived work, oracle correctness and measured computation are
different evidence. A sufficiency argument always names its information view
and assumptions; it never certifies an actual candidate or selects a world.
"""

from collections import Counter, defaultdict
from dataclasses import asdict
import json
import re

from .evaluate import evaluate_records, read_records, score_candidate
from .prompts import RenderedRequest, rendered_data
from .tasks import PEERS, Task, candidate_contract, coordinate_map
from .truth import changed_coordinates, solve_world


ATLAS = (
    ("maximum_cpu_only", "Winning value and edited ID with old/new values",
     "Correct old maximum", "A demotion can require an omitted runner-up."),
    ("top_k", "Selected top ten and edited ID with old/new values",
     "Correct old top ten", "Reserve values and record-to-value association can be missing."),
    ("prefix_sum", "Local prefix segment and genuine old/new edited operand",
     "Correct old segment", "The operand delta updates the local suffix; after-only information can be ambiguous."),
    ("difference_array", "Complete differences and an unchanged current raw anchor",
     "Correct old differences; anchor really unchanged", "The anchor fixes the additive constant and reconstructs the old operand."),
    ("distributed_sort", "Local sorted segment and genuine old/new edited operand",
     "Correct old segment", "Remote segment boundaries can be missing; a complete correct multiset is sufficient."),
    ("bfs_distance", "Old distance labels and the deleted edge endpoints",
     "Correct old labels", "Labels need not determine alternative path topology."),
)


def information_atlas():
    return [dict(family=family, information_view=view, correctness_assumption=assumption,
                 conclusion=conclusion, scope="CPU specified-view reference; further communication can add information")
            for family, view, assumption, conclusion in ATLAS]


def source_inventory(current, sources, peer, *, exclude_record_id=None):
    """Tombstones are known current records; pending replacements are unknown."""
    sources = json.loads(json.dumps(sources))  # Canonical saved JSON, including BFS endpoint arrays.
    expected = {r.record_id: json.loads(json.dumps(asdict(r))) for r in current.records}
    known = [s for s in sources if "value" in s]
    if (len({s["record_id"] for s in sources}) != len(sources)
            or any(json.dumps(expected.get(s["record_id"]), sort_keys=True) != json.dumps(s, sort_keys=True) for s in known) or any(
                s["version"] != 2 or json.dumps({k: expected.get(s["record_id"], {}).get(k)
                    for k in ("record_id", "owner", "position", "version")}, sort_keys=True) != json.dumps(s, sort_keys=True)
                for s in sources if "value" not in s)):
        raise ValueError("inventory differs from current raw source authority")
    remote = [s for s in known if s["owner"] != peer and s["record_id"] != exclude_record_id]
    denominator = sum(r.owner != peer and r.record_id != exclude_record_id for r in current.records)
    complete = len(known) == len(expected)
    prefix_sufficient = current.task is Task.PREFIX and set(range((peer + 1) * current.size.shard_size)) <= {s["position"] for s in known}
    return {"known_current_records": len(known), "pending_records": sum("value" not in s for s in sources),
        "known_tombstones": sum(s["deleted"] for s in known),
        "complete_current_raw": complete, "raw_recomputation_sufficient": True if complete or prefix_sufficient else None,
        "raw_sufficiency_reason": "complete_current_manifest" if complete else "complete_raw_prefix_through_local_output_end" if prefix_sufficient else "unresolved_by_conservative_raw_check",
        "remote_known": len(remote), "remote_denominator": denominator,
        "remote_coverage": len(remote) / denominator if denominator else None,
        "remote_pairs": [[s["record_id"], s["version"]] for s in sorted(remote, key=lambda s: s["record_id"])],
        "excluded_record_id": exclude_record_id,
        "interpretation": "Raw completeness is sufficient for recomputation, not necessary; retained records can be unused."}


def delta_transport(prepared, event, peer, status, candidate):
    """Transport the actual last valid candidate, including its existing errors."""
    task, size = prepared.world.task, prepared.world.size
    result = {"information_view": "Actual protocol-valid prefix-round-four candidate plus privileged true raw edit",
              "correctness_assumption": "None for transport or residual identity",
              "available": False, "candidate": None}
    if task not in (Task.PREFIX, Task.DIFFERENCE) or event != "revision":
        return dict(result, reason="not_applicable")
    if status != "valid":
        return dict(result, reason="prefix_round_four_unknown" if status == "unknown" else "prefix_round_four_not_protocol_valid")
    if candidate_contract(task, size, peer).error(candidate):
        raise ValueError("transport requires the actual valid candidate shape")
    old_world, new_world = prepared.world, prepared.event_world(event)
    old, new = solve_world(old_world), solve_world(new_world)
    source = next(r for r in old_world.records if r.record_id == prepared.main_edit.record_id)
    replacement = next(r for r in new_world.records if r.record_id == source.record_id)
    k, delta = source.position, replacement.value - source.value
    coordinates = candidate_contract(task, size, peer).coordinates
    update = [(delta if j >= k else 0) if task is Task.PREFIX else
              (delta if j == k and k >= 1 else -delta if j == k + 1 and k <= size.numeric_length - 2 else 0)
              for j in coordinates]
    transported = [v + u for v, u in zip(candidate, update)]
    residual_old = [v - old.by_coordinate[j] for j, v in zip(coordinates, candidate)]
    residual_new = [v - new.by_coordinate[j] for j, v in zip(coordinates, transported)]
    if residual_old != residual_new:
        raise ValueError("delta transport violates the residual-error identity")
    return dict(result, available=True, reason=None, edited_position=k, delta=delta,
        coordinates=list(coordinates), update=update, candidate=transported,
        actual_old_candidate=candidate, old_candidate_correct=score_candidate(old, status, candidate, peer),
        transported_correct=score_candidate(new, "valid", transported, peer),
        residual_old=residual_old, residual_new=residual_new, residual_identity=True,
        interpretation="Exact updating preserves earlier errors; this reference is never model feedback.")


def reconstruct_before(prepared, peer, status, candidate, sources):
    """Conservative sufficient reconstructions under a correct-summary assumption.

    The assumed candidate is the actual last candidate; no gold is substituted.
    A wrong candidate may produce a wrong hypothetical historical operand.
    """
    task, size = prepared.world.task, prepared.world.size
    old_source = next(r for r in prepared.world.records if r.record_id == prepared.main_edit.record_id)
    k = old_source.position
    base = {"information_view": "Actual last local candidate and held unchanged current raw records",
            "correctness_assumption": "Actual candidate is assumed correct for the old world; not certified",
            "status": "unresolved", "before_value": None, "record_ids": []}
    if status != "valid":
        return dict(base, reason="old_candidate_unknown" if status == "unknown" else "old_candidate_unavailable")
    if candidate_contract(task, size, peer).error(candidate):
        raise ValueError("reconstruction requires a valid old candidate shape")
    raw = {s["position"]: s for s in sources if "value" in s and s["record_id"] != old_source.record_id}
    coordinates = candidate_contract(task, size, peer).coordinates
    values = dict(zip(coordinates, candidate)) if task is not Task.BFS else {}
    before, ids, method = None, [], None
    if task is Task.PREFIX:
        if k in values and (k == 0 or k - 1 in values):
            before = values[k] - (0 if k == 0 else values[k - 1])
            method = "adjacent_local_prefix_coordinates"
        else:
            j = next((j for j in coordinates if j >= k and all(a in raw for a in range(j + 1) if a != k)), None)
            if j is not None:
                before = values[j] - sum(raw[a]["value"] for a in range(j + 1) if a != k)
                ids = [raw[a]["record_id"] for a in range(j + 1) if a != k]
                method = "prefix_coordinate_plus_complete_unchanged_prefix_raw"
    elif task is Task.DIFFERENCE and raw:
        a = min(raw)
        before = raw[a]["value"] + (sum(values[j] for j in range(a + 1, k + 1)) if a < k else
                                   -sum(values[j] for j in range(k + 1, a + 1)))
        ids, method = [raw[a]["record_id"]], "complete_differences_plus_unchanged_anchor"
    elif task is Task.SORT and len(raw) == size.numeric_length - 1:
        after = next(r.value for r in prepared.event_world("revision").records if r.record_id == old_source.record_id)
        possible = [v for v in range(100) if v != after and
                    [sorted([s["value"] for s in raw.values()] + [v])[j] for j in coordinates] == candidate]
        if len(possible) != 1:
            return dict(base, reason="correct_local_segment_does_not_identify_operand",
                        possible_before_values=possible)
        before, ids, method = possible[0], [s["record_id"] for s in raw.values()], "unique_operand_given_all_other_raw_and_correct_local_sort"
    if before is None:
        return dict(base, reason="specified_sufficient_view_not_available")
    return dict(base, status="reconstructible_under_assumption", reason=None,
                before_value=before, record_ids=sorted(ids), method=method)


# Frozen narrow syntax: only literal ID/version/value association, not general
# semantic interpretation. Absence of a match stays unresolved, never absent.
ASSOCIATION = re.compile(r"(?<![A-Za-z0-9_])(?P<record_id>x\d{3})/v1=(?P<value>-?(?:0|[1-9]\d*))(?![A-Za-z0-9_])")


def old_value_visibility(record_id, before_value, receipt, excerpts):
    evidence, conflicting = [], []
    if receipt and receipt["record_id"] == record_id and type(receipt["before_value"]) is int:
        if receipt["before_value"] != before_value or (receipt["previous_version"], receipt["new_version"]) != (1, 2):
            raise ValueError("historical receipt differs from genuine archived v1")
        evidence.append({"origin": "host_receipt", "record_id": record_id, "version": 1,
                         "value": before_value, "field": "historical_receipt.before_value"})
    numeric_occurrences = 0
    for excerpt in excerpts:
        literal = excerpt["text"]
        numeric_occurrences += len(re.findall(r"(?<!\w)" + re.escape(str(before_value)) + r"(?!\w)", literal))
        for match in ASSOCIATION.finditer(literal):
            if match["record_id"] != record_id:
                continue
            row = {k: v for k, v in excerpt.items() if k != "text"}
            row.update(origin="literal_derived_assertion", record_id=record_id, version=1,
                       value=int(match["value"]), excerpt=match.group(), span=list(match.span()))
            (evidence if row["value"] == before_value else conflicting).append(row)
    return {"status": "explicit_source_bound" if evidence else "unresolved",
            "visible": True if evidence else None, "evidence": evidence,
            "conflicting_assertions": conflicting, "numeric_occurrences": numeric_occurrences,
            "reason": None if evidence else "no_rubric_match_does_not_establish_absence",
            "interpretation": "Literal derived assertions are untrusted; this is no claim of internal use or complete provenance."}


def receipt_timing(rows, deliveries, peer):
    """Retain all four opportunities and censored peers, with no success-only lag."""
    rows = sorted(rows, key=lambda r: r["round"])
    if [r["round"] for r in rows] != [1, 2, 3, 4]:
        raise ValueError("receipt alignment requires all four scheduled calls")
    received = [r for r in rows if r["v2_available"] is True]
    first = received[0] if received else None
    first_exact = first is not None and all(r["v2_available"] is False for r in rows if r["round"] < first["round"])
    before_witnessed = any(r["correct"] == 1 and r["v2_available"] is False for r in rows)
    before_unknown = any((r["v2_available"] is False and r["correct"] is None) or
                         (r["v2_available"] is None and r["correct"] != 0) for r in rows)
    correct_before = True if before_witnessed else None if before_unknown else False
    after = [r for r in rows if first and r["round"] >= first["round"]]
    successes = [r for r in after if r["correct"] == 1]
    first_success = successes[0] if successes else None
    success_exact = first_success is not None and all(r["correct"] is not None for r in after if r["round"] < first_success["round"])
    relevant = [d for d in deliveries if first and d["delivery_id"] in first["v2_delivery_ids"] and d["recipient"] == peer]
    origins = sorted({d["origin"] for d in relevant})
    if first and not relevant:
        raise ValueError("receipt timing lacks actual delivery evidence")
    if any(d.get("first_usable", {}).get("phase") != "recovery" or
           d.get("first_usable", {}).get("round_number", 5) > first["round"] for d in relevant if "first_usable" in d):
        raise ValueError("receipt is not usable at its observed call boundary")
    censored = any(r["v2_available"] is None or r["correct"] is None for r in rows)
    category = ("receipt_or_outcome_censored" if (first is not None and not first_exact) or (first is None and any(r["v2_available"] is None for r in rows)) else
                "no_receipt" if not first else
                "same_call_success" if first["correct"] == 1 else
                "later_success" if first_success and success_exact else
                "receipt_or_outcome_censored" if any(r["correct"] is None for r in after) else
                "receipt_without_success")
    return {"category": category, "censored": censored, "correct_before_authoritative_receipt": correct_before,
        "first_observed_receipt_round": first["round"] if first else None,
        "first_receipt_round": first["round"] if first_exact else None,
        "receipt_origins": origins, "receipt_delivery_ids": [d["delivery_id"] for d in relevant],
        "first_observed_success_after_receipt": first_success["round"] if first_success else None,
        "receipt_to_success_lag": first_success["round"] - first["round"] if first_exact and success_exact else None,
        "observed_rounds": sum(r["correct"] is not None for r in rows), "scheduled_rounds": 4,
        "rounds": [{k: r[k] for k in ("call_id", "round", "correct", "v2_available", "v2_delivery_ids")} for r in rows]}


def edit_descriptor(prepared, event):
    old_world, current = prepared.world, prepared.event_world(event)
    old, new = solve_world(old_world), solve_world(current)
    changed = changed_coordinates(old, new).changed
    affected = sorted({p for j in changed for p in coordinate_map(old.task, old.size).coordinate_peers[j]})
    edit = prepared.main_edit if event == "revision" else prepared.preserving_edit
    source = next(r for r in old_world.records if r.record_id == edit.record_id)
    replacement = next(r for r in current.records if r.record_id == edit.record_id)
    result = {"world_id": prepared.world_id, "family": old.task.value, "size": old.size.value,
        "event": event, "record_id": source.record_id, "source_owner": source.owner,
        "position": source.position,
        "old_value": list(source.value) if source.position is None else source.value,
        "new_value": list(replacement.value) if source.position is None else replacement.value,
        "changed_coordinates": sorted(changed), "affected_output_owners": affected,
        "affected_output_owner_count": len(affected), "direction": "deletion" if source.position is None else
            "increase" if replacement.value > source.value else "decrease",
        "magnitude": None if source.position is None else abs(replacement.value - source.value),
        "sort_crossed_boundaries": None, "bfs_disconnected": None,
        "interpretation": "Descriptive footprint; no causal moderator or population filter."}
    if old.task is Task.SORT:
        # ID breaks equal-value ties for displacement descriptors only; exact
        # candidate correctness still compares the specified sorted values.
        before = sorted(old_world.records, key=lambda r: (r.value, r.record_id))
        after = sorted(current.records, key=lambda r: (r.value, r.record_id))
        a = next(i for i, r in enumerate(before) if r.record_id == source.record_id)
        b = next(i for i, r in enumerate(after) if r.record_id == source.record_id)
        result.update(sort_old_rank=a, sort_new_rank=b, sort_rank_tie_rule="value then stable record ID",
            sort_crossed_boundaries=[j for j in range(old.size.shard_size, old.size.numeric_length, old.size.shard_size)
                                    if min(a, b) < j <= max(a, b)])
    if old.task is Task.BFS:
        result.update(bfs_disconnected=-1 in new.values, bfs_unreachable_nodes=[j for j, v in new.by_coordinate.items() if v == -1])
    return result


IDENTITY = ("world_id", "branch_id", "family", "size", "phase", "event", "policy", "replicate",
            "prefix_parent", "call_id", "generation_id", "replay_parent", "prefix_call_id", "round", "peer")


def _boundary(saved, peer, tokenizer):
    """Measure the actual displayed history, checking its source projection."""
    before = json.loads(saved["requests"]["before"])
    data = rendered_data(RenderedRequest(saved["requests"]["rendered"][peer]["content"]))
    expected = []
    for source in before["peers"][peer]["sources"]:
        item = {k: source[k] for k in ("record_id", "owner", "position", "version")}
        if item["position"] is None:
            del item["position"]
        item["status"] = "update_pending" if "value" not in source else "deleted" if source["deleted"] else "known"
        if "value" in source:
            item["endpoints" if before["task"] == Task.BFS.value else "value"] = source["value"]
        expected.append(item)
    if (json.dumps(data["current_sources"], sort_keys=True) != json.dumps(expected, sort_keys=True) or data["public"]["peer"] != peer or
            data["public"]["slot"] != {"phase": before["phase"], "round": saved["round_number"]}):
        raise ValueError("actual rendered sources/slot differ from saved call-boundary state")
    literal_state = [("received_prose" if "sender" in entry else "own_reply", entry["slot"]["phase"],
        entry["slot"]["round_number"], entry.get("sender"), entry["text"])
        for entry in before["peers"][peer]["history"] if "text" in entry]
    literal_rendered = [(entry["kind"], entry["slot"]["phase"], entry["slot"]["round"], entry.get("sender"), entry["text"])
                        for entry in data["history"] if "text" in entry]
    if literal_state != literal_rendered:
        raise ValueError("actual rendered history differs from literal saved history")
    tokenized = saved["requests"]["tokenized"][peer]
    if tokenizer is not None and list(tokenizer.encode(tokenized["text"], add_special_tokens=False)) != tokenized["input_ids"]:
        raise ValueError("diagnostic tokenizer does not reproduce exact saved input IDs")
    components = [entry["text"] if "text" in entry else json.dumps(entry, ensure_ascii=True, separators=(",", ":"))
                  for entry in data["history"]]
    if data["latest_candidate"].get("historical"):
        components.append(json.dumps(data["latest_candidate"], ensure_ascii=True, separators=(",", ":")))
    components.extend(entry["text"] for entry in data["feedback"])
    tokens = (sum(len(tokenizer.encode(s, add_special_tokens=False)) for s in components) if tokenizer is not None
              else 0 if not components else None)
    return before, data, {"input_tokens": len(tokenized["input_ids"]), "history_content_tokens": tokens,
        "history_token_reason": None if tokens is not None else "matching_tokenizer_not_supplied",
        "history_entries": len(data["history"]), "history_characters": sum(len(s) for s in components),
        "history_token_definition": "Sum of independently encoded displayed history/candidate/feedback content; excludes headers, not marginal prompt tokens."}


def _excerpts(branch, peer, data, deliveries, records):
    result = []
    for index, entry in enumerate(data["history"]):
        if "text" not in entry:
            continue
        slot = entry["slot"]
        sender = entry.get("sender", peer)
        bid = branch.prefix_parent if slot["phase"] == "prefix" and branch.prefix_parent else branch.branch_id
        call_id = f"{bid}/r{slot['round']}/p{sender}"
        row = {"text": entry["text"], "history_index": index, "kind": entry["kind"], "call_id": call_id}
        if entry["kind"] == "received_prose":
            message_id = f"{call_id}/to{peer}"
            matches = [d for d in deliveries if d["message_id"] == message_id and d["text"] == entry["text"]]
            if len(matches) != 1:
                raise ValueError("retained prose lacks its exact archived message/delivery")
            row.update(message_id=message_id, delivery_id=matches[0]["delivery_id"])
        else:
            logical = records.get(call_id)
            physical = records.get(logical["generation_id"]) if logical else None
            if not physical or not physical["raw_json"] or json.loads(physical["raw_json"])["text"] != entry["text"]:
                raise ValueError("retained own reply differs from its original raw call")
        result.append(row)
    return result


def _communication(branch, call, outcome, saved, before):
    """All validated send attempts, with committed delivery/acquisition separate."""
    if outcome["protocol_outcome"] == "unknown":
        return None, []
    validation = json.loads(saved["validation_json"]) if saved["validation_json"] else {}
    messages = validation.get("messages", [])
    if outcome["protocol_outcome"] != "valid":
        if messages:
            raise ValueError("invalid/failed reply has staged message effects")
        return {"validated_messages": 0, "source_attempts": 0, "text_attempts": 0, "prose_tokens": None}, []
    raw = validation["generated"]
    sends = json.loads(raw["text"])["send"]
    if len(sends) != len(messages):
        raise ValueError("saved validated messages differ from literal reply")
    held = {s["record_id"]: s for s in before["peers"][call.peer]["sources"] if "value" in s}
    attempts = []
    for send, message in zip(sends, messages):
        if (send["to"] != message["recipient"] or message["sender"] != call.peer or
                send.get("text") != message["text"] or message["slot"] !=
                {"phase": before["phase"], "round_number": call.round_number} or
                [(s["record_id"], s["version"]) for s in message["sources"]] !=
                [(s["record_id"], s["version"]) for s in send.get("source_refs", [])] or
                any(held.get(s["record_id"]) != s for s in message["sources"])):
            raise ValueError("saved validated forwarding differs from literal held-source message")
        message_id = f"{call.call_id}/to{message['recipient']}"
        for index, source in enumerate(message["sources"]):
            attempts.append({"delivery_id": f"{message_id}/source{index}", "message_id": message_id,
                "recipient": message["recipient"], "kind": "source", "source": source, "text": None})
        if message["text"] is not None:
            attempts.append({"delivery_id": f"{message_id}/text", "message_id": message_id,
                "recipient": message["recipient"], "kind": "text", "source": None, "text": message["text"]})
    return {"validated_messages": len(messages), "source_attempts": sum(a["kind"] == "source" for a in attempts),
        "text_attempts": sum(a["kind"] == "text" for a in attempts), "prose_tokens": validation["prose_tokens"]}, attempts


def _strata(rows):
    groups = defaultdict(list)
    keys = ("family", "size", "policy", "replicate", "round", "old_candidate_correct", "prefix_round_four_joint")
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    result = []
    for key, group in sorted(groups.items(), key=lambda kv: repr(kv[0])):
        result.append(dict(zip(keys, key), unit="scheduled_peer_call_offline_stratum", scheduled=len(group),
            scheduled_worlds=len({r["world_id"] for r in group}), observed_boundaries=sum(r["boundary_observed"] for r in group),
            observed_outcomes=sum(r["correct"] is not None for r in group),
            intended_mean_correct=None if any(r["correct"] is None for r in group) else sum(r["correct"] for r in group) / len(group),
            explicit_visibility=dict(sorted(Counter(r["visibility"]["status"] for r in group).items())),
            reconstructibility=dict(sorted(Counter(r["reconstructibility"]["status"] for r in group).items())),
            raw_sufficiency={"sufficient": sum(r["complete_current_raw"] is True for r in group),
                "incomplete": sum(r["complete_current_raw"] is False for r in group),
                "unknown": sum(r["complete_current_raw"] is None for r in group)},
            conservative_raw_recomputation={"sufficient": sum(r["raw_recomputation_sufficient"] is True for r in group),
                "unresolved": sum(r["boundary_observed"] and r["raw_recomputation_sufficient"] is None for r in group),
                "boundary_unknown": sum(not r["boundary_observed"] for r in group)},
            interpretation="Offline correctness strata with denominators; never admission or causal adjustment."))
    return result


def _retained_old_candidate(data, old_row):
    if old_row["protocol_outcome"] != "valid":
        return False
    for entry in [*data["history"], data["latest_candidate"]]:
        slot = entry.get("slot", {})
        if slot != {"phase": "prefix", "round": 4}:
            continue
        if entry.get("kind") == "own_reply":
            return True  # Its original exact raw call is checked by _excerpts.
        if entry.get("historical") and entry.get("status") == "valid" and entry.get("candidate") == old_row["candidate"]:
            return True
    return False


def information_records(worlds, branches, records, inputs, attempts=(), *, committed=None, tokenizer=None, tables=None):
    """Derive inventory tables from complete schedules and original records."""
    worlds, branches = tuple(worlds), tuple(sorted(branches, key=lambda b: b.branch_id))
    tables = evaluate_records(worlds, branches, records, inputs, attempts) if tables is None else tables
    by_world = {w.world_id: w for w in worlds}
    outcomes = {r["call_id"]: r for r in tables["outcomes"]}
    trajectories = {r["branch_id"]: r for r in tables["trajectories"]}
    by_branch = {b.branch_id: b for b in branches}
    states, deliveries = defaultdict(list), defaultdict(dict)
    for (bid, _), saved in inputs.items():
        if by_branch[bid].phase != "control":
            states[bid].append(json.loads(saved["requests"]["before"]))
    completed = {}
    for bid, saved in (committed or {}).items():
        state, branch = saved["state"], by_branch.get(bid)
        if (branch is None or state["branch_id"] != bid or not state["committed"] or
                state["task"] != branch.task.value or state["size"] != by_world[branch.world_id].world.size.value or
                state["phase"] != ("recovery" if branch.phase == "continuation" else branch.phase)):
            raise ValueError("committed diagnostic state differs from schedule")
        slot = state["last_slot"]
        number = slot["round_number"] if slot and slot["phase"] == state["phase"] else 0
        if number == 4 and state["pending"]:
            raise ValueError("complete checkpoint retains pending deliveries")
        if any(outcomes[c.call_id]["protocol_outcome"] == "unknown" for c in branch.calls if c.round_number <= number):
            raise ValueError("committed diagnostic state includes unexecuted outcomes")
        current = (by_world[branch.world_id].world if branch.event == "original" else
                   by_world[branch.world_id].event_world(branch.event))
        for peer in PEERS:
            source_inventory(current, state["peers"][peer]["sources"], peer)
        states[bid].append(state)
        completed[bid] = number
    for bid, saved_states in states.items():
        for state in saved_states:
            for delivery in state["deliveries"]:
                previous = deliveries[bid].get(delivery["delivery_id"])
                if previous is not None and previous != delivery:
                    raise ValueError("archived delivery changes across committed inputs")
                deliveries[bid][delivery["delivery_id"]] = delivery
    prefix, communication, send_attempts, receipts, inventories, transports, timing, descriptors, exposure = [], [], [], [], [], [], [], [], []
    views = {}
    for branch in branches:
        prepared = by_world[branch.world_id]
        if branch.phase == "control":
            continue
        current = prepared.world if branch.event == "original" else prepared.event_world(branch.event)
        for call in branch.calls:
            row = outcomes[call.call_id]
            identity = {k: row[k] for k in IDENTITY}
            saved = inputs.get((branch.branch_id, call.round_number))
            before, data, metrics = _boundary(saved, call.peer, tokenizer) if saved else (None, None, {
                "input_tokens": None, "history_content_tokens": None, "history_token_reason": "call_boundary_unknown",
                "history_entries": None, "history_characters": None})
            inventory = source_inventory(current, before["peers"][call.peer]["sources"], call.peer) if before else None
            views[call.call_id] = (before, data, inventory)
            comm, sends = _communication(branch, call, row, records.get(call.call_id), before)
            communication.append(dict(identity, observed=comm is not None, **metrics,
                **(comm or {"validated_messages": None, "source_attempts": None, "text_attempts": None, "prose_tokens": None})))
            for attempt in sends:
                observed = deliveries[branch.branch_id].get(attempt["delivery_id"])
                if completed.get(branch.branch_id, 0) >= call.round_number and observed is None and (
                        attempt["kind"] == "source" or completed[branch.branch_id] == 4):
                    raise ValueError("committed checkpoint lacks a validated delivery attempt")
                if observed and any(observed[k] != attempt[k] for k in ("message_id", "recipient", "source", "text")):
                    raise ValueError("committed delivery differs from validated attempt")
                send_attempts.append(dict(identity, **attempt, delivered=observed is not None,
                    first_usable=observed["first_usable"] if observed else None,
                    acquired=observed["acquired"] if observed else None,
                    delivery_observation="committed" if observed else "release_not_observed"))
            if branch.phase == "prefix":
                prefix.append(dict(identity, old_gold_correct=row["correct"], boundary_observed=before is not None,
                    **metrics, inventory=inventory))
        if branch.phase == "prefix":
            for event, edit in (("revision", prepared.main_edit), ("preserving", prepared.preserving_edit)):
                if edit is None:
                    continue
                source = next(r for r in prepared.world.records if r.record_id == edit.record_id)
                owner_rows = [r for r in prefix if r["branch_id"] == branch.branch_id and r["peer"] == source.owner]
                exposed = []
                for row in owner_rows:
                    _, data, _ = views[row["call_id"]]
                    if data and any(s["record_id"] == source.record_id and s["version"] == 1 and s["status"] == "known" and
                                    s.get("endpoints" if branch.task is Task.BFS else "value") ==
                                    (list(source.value) if branch.task is Task.BFS else source.value) for s in data["current_sources"]):
                        exposed.append(row["call_id"])
                exposure.append({"world_id": prepared.world_id, "family": branch.task.value, "size": current.size.value,
                    "event": event, "record_id": source.record_id, "owner": source.owner, "exposed_call_ids": exposed,
                    "observed_owner_calls": sum(r["boundary_observed"] for r in owner_rows), "scheduled_owner_calls": 4,
                    "owner_v1_exposure": True if exposed else False if all(r["boundary_observed"] for r in owner_rows) else None,
                    "interpretation": "Rendered exposure only, not internal use or prefix-success admission."})
            continue
        for peer in PEERS:
            peer_rows = [outcomes[c.call_id] for c in branch.calls if c.peer == peer]
            initial = next(r for r in peer_rows if r["round"] == 1)
            identity = {k: initial[k] for k in IDENTITY if k not in ("round", "call_id", "generation_id", "replay_parent")}
            old_row = outcomes[initial["prefix_call_id"]]
            transports.append(dict(identity, prefix_call_id=old_row["call_id"],
                **delta_transport(prepared, branch.event, peer, old_row["protocol_outcome"], old_row["candidate"])))
            observed = list(deliveries[branch.branch_id].values())
            if branch.policy in ("L", "B") and branch.event != "sham":
                timing.append(dict(identity, **receipt_timing(peer_rows, observed, peer)))
            if branch.policy in ("C", "F"):
                before, _, _ = views[initial["call_id"]]
                boundary_origin = "saved_round_one_request" if before else "unobserved"
                if before is None and completed.get(branch.branch_id) == 0:
                    before = committed[branch.branch_id]["state"]
                    boundary_origin = "committed_pre_call_boundary"
                edit_id = None if branch.event == "sham" else (prepared.main_edit if branch.event == "revision" else prepared.preserving_edit).record_id
                boundary = source_inventory(current, before["peers"][peer]["sources"], peer, exclude_record_id=edit_id) if before else None
                relevant = [a for a in send_attempts if a["branch_id"] == branch.branch_id and a["recipient"] == peer and a["kind"] == "source"]
                acquisitions = sorted({(a["source"]["record_id"], a["source"]["version"]) for a in relevant if a["acquired"] is True})
                all_known = all(r["protocol_outcome"] != "unknown" for r in (outcomes[c.call_id] for c in branch.calls))
                inventories.append(dict(identity, boundary=boundary, boundary_origin=boundary_origin,
                    complete_delivery_horizon=completed.get(branch.branch_id) == 4,
                    observed_unique_acquired_pairs=[list(a) for a in acquisitions], observed_unique_acquired_count=len(acquisitions),
                    unique_acquired_count=len(acquisitions) if completed.get(branch.branch_id) == 4 else None,
                    observed_delivery_attempts=sum(a["delivered"] for a in relevant),
                    all_validated_delivery_attempts=len(relevant) if all_known else None,
                    validated_attempt_delivery_ids=[a["delivery_id"] for a in relevant],
                    interpretation="Post-intervention acquisition is an outcome, never a policy-effect adjustment."))
            if branch.event == "revision" and branch.policy in ("B", "C", "K", "B_delta", "C_delta", "K_delta") and branch.task in (Task.PREFIX, Task.SORT):
                source = next(r for r in prepared.world.records if r.record_id == prepared.main_edit.record_id)
                for row in peer_rows:
                    before, data, inventory = views[row["call_id"]]
                    visible = old_value_visibility(source.record_id, source.value, data["historical_receipt"],
                        _excerpts(branch, peer, data, observed, records)) if data else {"status": "boundary_unknown", "visible": None, "evidence": []}
                    retained = _retained_old_candidate(data, old_row) if data else None
                    reconstructed = ({"status": "boundary_unknown", "reason": "call_boundary_unknown",
                        "information_view": "Unobserved call-boundary state",
                        "correctness_assumption": "No reconstruction asserted for an unobserved view"} if before is None else
                        reconstruct_before(prepared, peer, old_row["protocol_outcome"], old_row["candidate"], before["peers"][peer]["sources"])
                        if retained else {"status": "old_candidate_unavailable_in_view", "before_value": None,
                            "information_view": "Held current raw and literal derived content; no valid retained own last prefix candidate",
                            "correctness_assumption": "No correct-old-candidate reconstruction asserted",
                            "reason": "old_candidate_not_retained_or_not_protocol_valid"})
                    receipts.append(dict({k: row[k] for k in IDENTITY}, boundary_observed=before is not None, correct=row["correct"],
                        old_candidate_in_view=retained,
                        old_candidate_correct=old_row["correct"], prefix_round_four_joint=trajectories[branch.prefix_parent]["final_joint"],
                        visibility=visible, reconstructibility=reconstructed,
                        raw_recomputation_sufficient=inventory["raw_recomputation_sufficient"] if inventory else None,
                        raw_sufficiency_reason=inventory["raw_sufficiency_reason"] if inventory else "call_boundary_unknown",
                        complete_current_raw=inventory["complete_current_raw"] if inventory else None))
    for prepared in worlds:
        for event in ("revision", "preserving"):
            if any(b.world_id == prepared.world_id and b.event == event for b in branches):
                descriptors.append(edit_descriptor(prepared, event))
    counts = defaultdict(Counter)
    for row in timing:
        counts[(row["family"], row["size"], row["event"], row["policy"], row["replicate"])][row["category"]] += 1
    timing_counts = []
    for key, count in sorted(counts.items()):
        group = [r for r in timing if (r["family"], r["size"], r["event"], r["policy"], r["replicate"]) == key]
        timing_counts.append(dict(zip(("family", "size", "event", "policy", "replicate"), key),
            scheduled_peers=len(group), censored_peers=sum(r["censored"] for r in group), categories=dict(sorted(count.items())),
            correctness_before_receipt={"positive": sum(r["correct_before_authoritative_receipt"] is True for r in group),
                "negative": sum(r["correct_before_authoritative_receipt"] is False for r in group),
                "unknown": sum(r["correct_before_authoritative_receipt"] is None for r in group)}))
    return {"kind": "Offline information/work diagnostics; inventories and references do not certify model use or correctness",
        "history_tokenizer": "caller-supplied tokenizer, exact saved input IDs verified" if tokenizer is not None else "not supplied; nonempty history token counts unavailable",
        "atlas": information_atlas(), "prefix": prefix, "owner_exposure": exposure, "communication": communication,
        "delivery_attempts": send_attempts, "receipt_timing": timing,
        "receipt_timing_counts": timing_counts,
        "boundary_acquisition": inventories, "receipt_information": receipts, "receipt_strata": _strata(receipts),
        "transport_references": transports, "edit_descriptors": descriptors,
        "separation": "Evidence inventory is here; preserved correct output is in peer_diagnostics; measured computation is in original attempts/later cost tables."}


def information_run(worlds, branches, paths, *, tokenizer=None, estimands=False):
    """One read-only worker snapshot, using the public saved checkpoint decoder."""
    worlds, branches = tuple(worlds), tuple(branches)
    records, inputs, attempts, committed = read_records(worlds, branches, paths, include_committed=True)
    tables = evaluate_records(worlds, branches, records, inputs, attempts)
    tables["information"] = information_records(worlds, branches, records, inputs, attempts,
        committed=committed, tokenizer=tokenizer, tables=tables)
    if estimands:
        from .analysis import analyze_estimands, prose_activity
        tables["estimands"] = analyze_estimands(worlds, branches, tables)
        tables["estimands"]["prose_activity"] = prose_activity(worlds, branches, inputs)
    return tables
