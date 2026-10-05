"""Offline exact outcomes and §7.1 diagnostics, never imported by execution.

The saved schedule defines opportunities; the call ledger defines outcomes.
Gold and prefix correctness are evaluator-only. Tables are derived exports,
not another store. No tokenizer, inference provider or runner is needed.
"""

from .tasks import PEERS, Task, candidate_contract
from .truth import changed_coordinates, exact_candidate


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
