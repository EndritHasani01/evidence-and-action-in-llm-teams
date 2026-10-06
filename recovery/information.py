"""Offline §7.2 inventories and references. Never imported by execution.

Sources, literal derived work, oracle correctness and measured computation are
different evidence. A sufficiency argument always names its information view
and assumptions; it never certifies an actual candidate or selects a world.
"""

from collections import Counter, defaultdict
from dataclasses import asdict
import json
import re

from .evaluate import score_candidate
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
    expected = {r.record_id: asdict(r) for r in current.records}
    known = [s for s in sources if "value" in s]
    if (len({s["record_id"] for s in sources}) != len(sources)
            or any(expected.get(s["record_id"]) != s for s in known)):
        raise ValueError("inventory differs from current raw source authority")
    remote = [s for s in known if s["owner"] != peer and s["record_id"] != exclude_record_id]
    denominator = sum(r.owner != peer and r.record_id != exclude_record_id for r in current.records)
    return {"known_current_records": len(known), "pending_records": sum("value" not in s for s in sources),
        "known_tombstones": sum(s["deleted"] for s in known),
        "complete_current_raw": len(known) == len(expected),
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
    first_exact = first and all(r["v2_available"] is False for r in rows if r["round"] < first["round"])
    correct_before = any(r["correct"] == 1 and r["v2_available"] is False for r in rows)
    after = [r for r in rows if first and r["round"] >= first["round"]]
    successes = [r for r in after if r["correct"] == 1]
    first_success = successes[0] if successes else None
    success_exact = first_success and all(r["correct"] is not None for r in after if r["round"] < first_success["round"])
    relevant = [d for d in deliveries if first and d["delivery_id"] in first["v2_delivery_ids"] and d["recipient"] == peer]
    origins = sorted({d["origin"] for d in relevant})
    if first and not relevant:
        raise ValueError("receipt timing lacks actual delivery evidence")
    censored = any(r["v2_available"] is None or r["correct"] is None for r in rows)
    category = ("receipt_or_outcome_censored" if not first_exact and first or not first and censored else
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
        "position": source.position, "old_value": source.value, "new_value": replacement.value,
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
