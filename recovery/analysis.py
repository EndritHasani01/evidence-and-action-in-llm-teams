"""Prespecified offline contrasts and conditional repeats (spec §§5.2–5.4, 6).

The complete supplied schedule fixes the population, never observed success.
Components retain unknown outcomes and original response identities for M4-T05.
This module does not calculate uncertainty, impute outcomes or call a model.
"""

from collections import defaultdict
from fractions import Fraction

from .schedule import _branch_id, dependency_order
from .tasks import PEERS, Task

ROUNDS = (1, 2, 3, 4)
LATER_ROUNDS = (2, 3, 4)
MAIN_FAMILIES = tuple(t.value for t in Task)
RECEIPT_FAMILIES = (Task.PREFIX.value, Task.SORT.value)
PROSE_FAMILIES = (Task.SORT.value, Task.BFS.value)
PRESERVING_FAMILIES = (Task.TOP_K.value, Task.BFS.value)


def _exact(value):
    return None if value is None else {"numerator": value.numerator, "denominator": value.denominator}


def _fraction(row):
    value = row["exact"]
    return None if value is None else Fraction(value["numerator"], value["denominator"])


def endpoint_component(branch, outcomes, endpoint, *, rounds=ROUNDS, peers=PEERS, diagnostics=()):
    """One branch endpoint with its calls, denominator and exact arithmetic.

    Accuracy means are linear in scheduled replies. Final joint completion is
    the all-four operator. Preservation averages eligible peers within rounds,
    then rounds; eligibility comes solely from valid original prefix round four.
    """
    if (endpoint not in ("auc", "accuracy", "collaborator_accuracy", "final_joint", "preservation")
            or not rounds or len(set(rounds)) != len(rounds) or set(rounds) - set(ROUNDS)
            or not peers or len(set(peers)) != len(peers) or set(peers) - set(PEERS)):
        raise ValueError("invalid endpoint/round/peer scope")
    if endpoint == "auc" and (tuple(rounds) != ROUNDS or tuple(peers) != PEERS):
        raise ValueError("AUC requires all sixteen opportunities")
    if endpoint == "final_joint" and (tuple(rounds) != (4,) or tuple(peers) != PEERS):
        raise ValueError("final joint completion requires all four final candidates")
    selected = sorted((r for r in outcomes if r["round"] in rounds and r["peer"] in peers),
                      key=lambda r: (r["round"], r["peer"]))
    if {(r["round"], r["peer"]) for r in selected} != {(r, p) for r in rounds for p in peers}:
        raise ValueError("endpoint lacks scheduled peer-round outcomes")
    if len(selected) != len(rounds) * len(peers):
        raise ValueError("duplicate endpoint outcome")
    atoms = [{k: row[k] for k in ("call_id", "generation_id", "replay_parent", "round", "peer",
                                  "seed", "prefix_call_id", "correct")}
             for row in selected]
    result = {"branch_id": branch.branch_id, "event": branch.event, "policy": branch.policy,
        "replicate": branch.replicate, "endpoint": endpoint, "rounds": list(rounds), "peers": list(peers),
        "operator": "all" if endpoint == "final_joint" else "mean",
        "scheduled_calls": len(selected), "observed_calls": sum(r["correct"] is not None for r in selected),
        "eligibility": "eligible", "reason": None, "atoms": atoms}
    value = None
    if endpoint == "preservation":
        metrics = {r["call_id"]: r for r in diagnostics if r["metric"] == "preservation"}
        if any(r["call_id"] not in metrics for r in selected):
            raise ValueError("preservation endpoint lacks original prefix eligibility")
        eligible, unknown_eligibility = [], False
        for atom in atoms:
            metric = metrics[atom["call_id"]]
            atom.update({k: metric[k] for k in ("denominator", "numerator", "eligible_coordinates", "reason")})
            atom["value"] = metric["rate"]
            atom["weight"] = None
            atom["exact_weight"] = None
            unknown_eligibility |= metric["denominator"] is None
            if metric["denominator"]:
                eligible.append(atom)
        # A fixed peer's prefix eligibility cannot change across recovery rounds.
        for peer in peers:
            den = [a["denominator"] for a in atoms if a["peer"] == peer]
            if any(d != den[0] for d in den):
                raise ValueError("preservation eligibility changes across rounds")
        result.update(eligible_peers=len({a["peer"] for a in eligible}),
            unknown_eligibility_peers=len({a["peer"] for a in atoms if a["denominator"] is None}),
            unique_coordinate_count=None if unknown_eligibility else
                len({j for a in eligible for j in a["eligible_coordinates"]}),
            peer_copy_count=None if unknown_eligibility else
                sum(a["denominator"] for a in eligible if a["round"] == rounds[0]))
        if unknown_eligibility:
            result.update(eligibility="unknown", reason="prefix_round_four_unknown")
        elif not eligible:
            result.update(eligibility="ineligible", reason="no_eligible_coordinates")
        else:
            for atom in eligible:
                atom["weight"] = 1 / len(eligible)
                atom["exact_weight"] = _exact(Fraction(1, len(eligible)))
            if all(a["numerator"] is not None for a in eligible):
                value = sum((Fraction(a["numerator"], a["denominator"]) for a in eligible), Fraction()) / len(eligible)
            else:
                result["reason"] = "slot_unknown"
    else:
        for atom in atoms:
            atom.update(value=atom["correct"], weight=None if endpoint == "final_joint" else 1 / len(atoms),
                exact_weight=None if endpoint == "final_joint" else _exact(Fraction(1, len(atoms))))
        if all(a["correct"] is not None for a in atoms):
            value = (Fraction(int(all(a["correct"] for a in atoms))) if endpoint == "final_joint" else
                     Fraction(sum(a["correct"] for a in atoms), len(atoms)))
        else:
            result["reason"] = "slot_unknown"
    result.update(value=None if value is None else float(value), exact=_exact(value))
    return result


def _contrast(world, name, event, endpoint, components, *, population="main", replicate=0,
              round_number=None, construction_reference=False):
    components = [dict(component, coefficient=coefficient) for coefficient, component in components]
    eligibility = ("unknown" if any(c["eligibility"] == "unknown" for c in components) else
                   "ineligible" if any(c["eligibility"] == "ineligible" for c in components) else "eligible")
    known = all(c["exact"] is not None for c in components)
    value = sum((Fraction(c["coefficient"]) * _fraction(c) for c in components), Fraction()) if known else None
    formula = " + ".join(f"({c['coefficient']})*{c['endpoint']}({c['policy']},{c['event']},"
        f"peers={c['peers']},rounds={c['rounds']},rep={replicate})" for c in components)
    return {"world_id": world.world_id, "family": world.world.task.value, "size": world.world.size.value,
        "population": population, "estimand": name, "event": event, "endpoint": endpoint,
        "round": round_number, "replicate": replicate, "formula": formula,
        "primary": replicate == 0 and (name == "theta" and endpoint == "auc" or
            name == "E_keep" and event == "revision" and endpoint == "collaborator_accuracy"),
        "construction_reference": construction_reference, "eligibility": eligibility,
        "reason": None if known else "no_eligible_coordinates" if eligibility == "ineligible" else
            "prefix_round_four_unknown" if eligibility == "unknown" else "unknown_component",
        "value": None if value is None else float(value), "exact": _exact(value),
        "range": [sum(min(0, c["coefficient"]) for c in components),
                  sum(max(0, c["coefficient"]) for c in components)],
        "known_components": sum(c["exact"] is not None for c in components),
        "component_count": len(components), "components": components}


def _world_contrasts(world, by_branch, outcomes, diagnostics, replicate=0):
    """Write the finite scientific comparison matrix directly, without a registry."""
    rows, cache = [], {}

    def component(policy, event, endpoint, round_number=None, peers=PEERS):
        rounds = (round_number,) if round_number else (4,) if endpoint == "final_joint" else (
            LATER_ROUNDS if endpoint == "collaborator_accuracy" else ROUNDS)
        key = policy, event, endpoint, rounds, peers
        if key not in cache:
            branch_id = _branch_id(world.world_id, "continuation", event, policy, replicate)
            branch = by_branch.get(branch_id)
            if branch is None:
                cache[key] = {"branch_id": branch_id, "event": event, "policy": policy, "replicate": replicate,
                    "endpoint": endpoint, "rounds": list(rounds), "peers": list(peers), "operator":
                    "all" if endpoint == "final_joint" else "mean", "scheduled_calls": 0, "observed_calls": 0,
                    "eligibility": "eligible", "reason": "branch_not_in_supplied_schedule",
                    "atoms": [], "value": None, "exact": None}
            else:
                cache[key] = endpoint_component(branch, outcomes[branch_id], endpoint, rounds=rounds,
                    peers=peers, diagnostics=diagnostics.get(branch_id, ()))
        return cache[key]

    def emit(name, event, endpoint, terms, *, population="main", round_number=None, construction=False):
        rows.append(_contrast(world, name, event, endpoint, terms, population=population,
            replicate=replicate, round_number=round_number, construction_reference=construction))

    # AUC/final and preservation companions. A preservation mean uses the four
    # recovery rounds; the final and round-specific preservation rates stay visible.
    endpoints = [("auc", None), ("final_joint", None), ("preservation", None)] + [
        ("preservation", r) for r in ROUNDS]
    for endpoint, number in endpoints:
        for event in ("revision", "sham"):
            pairs = (("C", "B"), ("K", "C"), ("K", "B"))
            if event == "revision" and replicate == 0:
                pairs += (("B", "L"), ("C", "F"))
            for left, right in pairs:
                emit(f"{left}-{right}", event, endpoint, [(1, component(left, event, endpoint, number)),
                    (-1, component(right, event, endpoint, number))], round_number=number)
        for left, right in (("C", "B"), ("K", "C"), ("K", "B")):
            emit("theta" if left == "C" else f"{left}-{right}_corr", "revision_minus_sham", endpoint,
                [(1, component(left, "revision", endpoint, number)),
                 (-1, component(right, "revision", endpoint, number)),
                 (-1, component(left, "sham", endpoint, number)),
                 (1, component(right, "sham", endpoint, number))], round_number=number)

    G, H = world.partition
    for endpoint, number in [("collaborator_accuracy", None)] + [("accuracy", r) for r in ROUNDS]:
        keep = {}
        for event in ("revision", "sham"):
            def M(policy, peers):
                return component(policy, event, endpoint, number, peers)
            keep[event] = [(0.5, M("P_H", G)), (-0.5, M("B", G)),
                           (0.5, M("P_G", H)), (-0.5, M("B", H))]
            emit("E_keep", event, endpoint, keep[event], round_number=number, construction=number == 1)
            emit("E_clear", event, endpoint, [(0.5, M("C", G)), (-0.5, M("P_G", G)),
                (0.5, M("C", H)), (-0.5, M("P_H", H))], round_number=number, construction=number == 1)
            emit("own_reset_other_retained", event, endpoint,
                [(0.5, M("P_G", G)), (-0.5, M("B", G)),
                 (0.5, M("P_H", H)), (-0.5, M("B", H))], round_number=number)
            emit("own_reset_other_cleared", event, endpoint,
                [(0.5, M("C", G)), (-0.5, M("P_H", G)),
                 (0.5, M("C", H)), (-0.5, M("P_G", H))], round_number=number)
            for policy, mask in (("B", "00"), ("P_G", "10"), ("P_H", "01"), ("C", "11")):
                for peers, group in ((G, "G"), (H, "H")):
                    emit(f"M_{group}_{mask}", event, endpoint, [(1, M(policy, peers))], round_number=number)
        emit("phi_corr", "revision_minus_sham", endpoint, keep["revision"] +
            [(-coefficient, c) for coefficient, c in keep["sham"]], round_number=number,
            construction=number == 1)

    for event in ("revision", "sham"):
        for endpoint, number in [("auc", None), ("final_joint", None)] + [("accuracy", r) for r in ROUNDS]:
            for policy in ("B", "P_G", "P_H", "C"):
                emit(f"cell_{policy}", event, endpoint, [(1, component(policy, event, endpoint, number))],
                     round_number=number)
            emit("mixed_mean", event, endpoint, [(0.5, component("P_G", event, endpoint, number)),
                 (0.5, component("P_H", event, endpoint, number))], round_number=number)

    if replicate:
        return rows  # The repeated design contains no L/F, receipt, Q or preserving arms.
    if world.world.task.value in RECEIPT_FAMILIES:
        for endpoint, number in [("accuracy", 1), *endpoints]:
            def R(policy):
                return component(policy, "revision", endpoint, number)
            emit("eta", "revision", endpoint, [(1, R("K_delta")), (-1, R("C_delta")),
                (-1, R("K")), (1, R("C"))], population="receipts", round_number=number)
            for policy in ("B", "C", "K", "B_delta", "C_delta", "K_delta"):
                emit(f"receipt_cell_{policy}", "revision", endpoint, [(1, R(policy))],
                     population="receipts", round_number=number)
            for policy in ("B", "C", "K"):
                emit(f"{policy}_delta-{policy}", "revision", endpoint,
                    [(1, R(policy + "_delta")), (-1, R(policy))], population="receipts", round_number=number)
            for suffix in ("", "_delta"):
                for other in ("C", "K"):
                    emit(f"B{suffix}-{other}{suffix}", "revision", endpoint,
                        [(1, R("B" + suffix)), (-1, R(other + suffix))],
                        population="receipts", round_number=number)
    if world.world.task.value in PROSE_FAMILIES:
        for event in ("revision", "sham"):
            for endpoint, number in [("accuracy", r) for r in ROUNDS] + endpoints:
                for parent in ("B", "C"):
                    emit(f"Q_{parent}-{parent}", event, endpoint,
                        [(1, component("Q_" + parent, event, endpoint, number)),
                         (-1, component(parent, event, endpoint, number))],
                        population="prose_delay", round_number=number, construction=endpoint == "accuracy" and number == 1)
    if world.world.task.value in PRESERVING_FAMILIES and world.index <= 8:
        for endpoint, number in endpoints:
            for policy in ("B", "C", "K"):
                emit(f"preserving_cell_{policy}", "preserving", endpoint,
                    [(1, component(policy, "preserving", endpoint, number))], population="preserving", round_number=number)
            for left, right in (("C", "B"), ("K", "C"), ("K", "B")):
                emit(f"{left}-{right}", "preserving", endpoint,
                    [(1, component(left, "preserving", endpoint, number)),
                     (-1, component(right, "preserving", endpoint, number))], population="preserving", round_number=number)
    return rows


def population_table(worlds):
    """Fixed pre-outcome subsets, overlapping IDs, prefixes, partitions and seeds."""
    populations = []
    for name, families in (("main", MAIN_FAMILIES), ("receipts", RECEIPT_FAMILIES),
                           ("prose_delay", PROSE_FAMILIES), ("preserving", PRESERVING_FAMILIES),
                           ("repeat", MAIN_FAMILIES)):
        selected = [w for w in worlds if w.world.task.value in families and
                    (name != "preserving" or w.index <= 8) and
                    (name != "repeat" or not w.development and w.index <= 2)]
        populations.append({"population": name, "families": list(families),
            "world_ids": [w.world_id for w in selected],
            "family_counts": {f: sum(w.world.task.value == f for w in selected) for f in families},
            "weighting": "equal family means; preservation uses eligible peers, worlds and families",
            "worlds": [{"world_id": w.world_id, "family": w.world.task.value, "index": w.index,
                "prefix_parent": _branch_id(w.world_id, "prefix", "original", None, 0),
                "partition": [list(group) for group in w.partition], "development": w.development,
                "continuation_seeds": [[list(round_seeds) for round_seeds in replicate]
                                       for replicate in w.streams.continuation]} for w in selected]})
    return populations


SUMMARY_KEYS = ("population", "estimand", "event", "endpoint", "round", "replicate")


def summarize_contrasts(rows, populations):
    """Family/world denominators remain fixed in the intended-population estimate.

    Complete-case values are separately labeled descriptions. Structurally empty
    preservation denominators are excluded only from that diagnostic; unknown
    eligibility/outcomes never masquerade as structural emptiness.
    """
    grouped, result = defaultdict(list), []
    families = {p["population"]: p["families"] for p in populations}
    for row in rows:
        grouped[tuple(row[k] for k in SUMMARY_KEYS)].append(row)
    for key, group in grouped.items():
        targets = families[group[0]["population"]]
        eligible = [r for r in group if r["eligibility"] != "ineligible"]
        if group[0]["endpoint"] == "preservation":
            targets = [f for f in targets if any(r["family"] == f for r in eligible)]
        for family in [*targets, None]:
            current = [r for r in group if family is None or r["family"] == family]
            included = [r for r in current if r["eligibility"] != "ineligible"]
            observed = [r for r in included if r["exact"] is not None]
            selected_families = [family] if family else targets
            den = {f: sum(r["family"] == f for r in included) for f in selected_families}
            cc_den = {f: sum(r["family"] == f for r in observed) for f in selected_families}
            missing_families = [f for f, n in den.items() if not n]
            def balanced(items, counts):
                if not counts or any(n == 0 for n in counts.values()):
                    return None
                return sum((sum((_fraction(r) for r in items if r["family"] == f), Fraction()) / n
                            for f, n in counts.items()), Fraction()) / len(counts)
            value = balanced(included, den) if len(observed) == len(included) else None
            cc = balanced(observed, cc_den)
            result.append({k: group[0][k] for k in SUMMARY_KEYS} | {
                "level": "family" if family else "all_families", "family": family,
                "primary": group[0]["primary"], "range": group[0]["range"],
                "formula": "(1/F) * sum_f [(1/n_f) * sum_w world_contrast]",
                "value": None if value is None else float(value), "exact": _exact(value),
                "reason": None if value is not None else "no_eligible_worlds" if not included else
                    "missing_eligible_family" if missing_families else "unknown_world_components",
                "scheduled_worlds": len(current), "eligible_worlds": len(included), "observed_worlds": len(observed),
                "unknown_worlds": len(included) - len(observed),
                "unknown_eligibility_worlds": sum(r["eligibility"] == "unknown" for r in included),
                "ineligible_worlds": len(current) - len(included), "family_denominators": den,
                "target_families": len(selected_families),
                "eligible_families": sum(n > 0 for n in den.values()), "missing_families": missing_families,
                "world_ids": [r["world_id"] for r in current],
                "ineligible_world_ids": [r["world_id"] for r in current if r["eligibility"] == "ineligible"],
                "unknown_world_ids": [r["world_id"] for r in included if r["exact"] is None],
                "complete_case_description": {"value": None if cc is None else float(cc), "exact": _exact(cc),
                    "world_ids": [r["world_id"] for r in observed], "family_denominators": cc_den,
                    "missing_families": [f for f, n in cc_den.items() if not n],
                    "label": "descriptive complete cases; does not replace the intended estimand"}})
    return result


def compare_replicates(original, repeated):
    """Zero contrasts are ties; a strict opposite sign is a sign reversal."""
    left, right = _fraction(original), _fraction(repeated)
    category = ("unknown" if left is None or right is None else
                "both_ties" if left == 0 and right == 0 else
                "replicate_zero_tie" if left == 0 else "replicate_one_tie" if right == 0 else
                "sign_reversal" if left * right < 0 else "same_sign")
    delta = None if left is None or right is None else right - left
    return {"classification": category, "replicate_zero": original["value"], "replicate_one": repeated["value"],
        "equal_values": None if delta is None else delta == 0, "difference": None if delta is None else float(delta),
        "exact_difference": _exact(delta)}


def analyze_estimands(worlds, branches, tables):
    """Derive all estimates from M4-T01's full outcome and diagnostic join.

    Replicate-zero population summaries and conditional repeat displays are
    separate. A missing supplied sibling is explicitly unavailable, not a new
    complete-case population. The ordinary CLI supplies the full saved schedule.
    """
    worlds = tuple(sorted(worlds, key=lambda w: w.world_id))
    branches = tuple(sorted(branches, key=lambda b: b.branch_id))
    dependency_order(branches)
    by_world, by_branch = {w.world_id: w for w in worlds}, {b.branch_id: b for b in branches}
    if (len(by_world) != len(worlds) or len({w.world.size for w in worlds}) != 1
            or len({w.development for w in worlds}) != 1):
        raise ValueError("analysis requires unique worlds at one declared size and population domain")
    expected = {c.call_id: (b, c) for b in branches for c in b.calls}
    outcomes, diagnostics = defaultdict(list), defaultdict(list)
    seen = set()
    for row in tables["outcomes"]:
        scope = expected.get(row["call_id"])
        if scope is None or row["call_id"] in seen:
            raise ValueError("duplicate/unscheduled analysis outcome")
        b, c = scope
        world = by_world.get(b.world_id)
        if world is None or b.task is not world.world.task or any(row[k] != v for k, v in {
                "branch_id": b.branch_id, "world_id": b.world_id, "family": b.task.value,
                "size": world.world.size.value, "phase": b.phase, "event": b.event, "policy": b.policy,
                "replicate": b.replicate, "prefix_parent": b.prefix_parent, "round": c.round_number,
                "peer": c.peer, "seed": c.seed, "generation_id": c.generation_id,
                "replay_parent": c.replay_parent}.items()):
            raise ValueError("analysis outcome differs from original schedule/world")
        correct = row["correct"]
        if correct is not None and (type(correct) is not int or correct not in (0, 1)):
            raise ValueError("analysis correctness must be exact 0/1/unknown")
        if ((row["protocol_outcome"] == "unknown") != (correct is None)
                or row["protocol_outcome"] in ("invalid", "failed") and correct != 0):
            raise ValueError("analysis failure/unknown scoring differs from evaluator")
        seen.add(row["call_id"])
        outcomes[b.branch_id].append(row)
    if seen != expected.keys():
        raise ValueError("analysis must retain the complete scheduled outcome join")
    seen_diagnostics = set()
    for row in tables["peer_diagnostics"]:
        key = row["call_id"], row["metric"]
        if key in seen_diagnostics or row["call_id"] not in expected:
            raise ValueError("duplicate/unscheduled analysis diagnostic")
        seen_diagnostics.add(key)
        diagnostics[row["branch_id"]].append(row)
    populations = population_table(worlds)
    primary, repeats = [], []
    for world in worlds:
        primary.extend(_world_contrasts(world, by_branch, outcomes, diagnostics))
        if not world.development and world.index <= 2:
            repeats.extend(_world_contrasts(world, by_branch, outcomes, diagnostics, replicate=1))
    originals = {(r["world_id"], r["estimand"], r["event"], r["endpoint"], r["round"]): r for r in primary}
    repeatability = []
    for repeated in repeats:
        if (repeated["estimand"] not in ("theta", "E_keep", "K-C", "K-B", "K-C_corr", "K-B_corr")
                or repeated["endpoint"] not in ("auc", "final_joint", "collaborator_accuracy")):
            continue
        key = tuple(repeated[k] for k in ("world_id", "estimand", "event", "endpoint", "round"))
        repeatability.append({k: repeated[k] for k in ("world_id", "family", "estimand", "event", "endpoint")} |
            compare_replicates(originals[key], repeated))
    trajectories = {(r["world_id"], r["event"], r["policy"], r["replicate"]): r
                    for r in tables["trajectories"] if r["phase"] == "continuation"}
    changes = []
    for world in worlds:
        if world.development or world.index > 2:
            continue
        for event in ("revision", "sham"):
            for policy in ("B", "C", "K", "P_G", "P_H"):
                pair = [trajectories.get((world.world_id, event, policy, k)) for k in (0, 1)]
                complete = all(r is not None and r["complete"] for r in pair)
                changes.append({"world_id": world.world_id, "family": world.world.task.value,
                    "event": event, "policy": policy, "prefix_parent": _branch_id(world.world_id, "prefix", "original", None, 0),
                    "partition": [list(g) for g in world.partition],
                    "replicate_zero_category": pair[0]["category"] if pair[0] else "not_scheduled",
                    "replicate_one_category": pair[1]["category"] if pair[1] else "not_scheduled",
                    "category_changed": pair[0]["category"] != pair[1]["category"] if complete else None,
                    "fragmentation_changed": pair[0]["fragmented"] != pair[1]["fragmented"] if complete else None,
                    "complete_pair": complete})
    return {"kind": "Prespecified offline estimates; scripted data validate implementation, not empirical effects",
        "scope": "development validation" if all(w.development for w in worlds) else "supplied main manifest",
        "population_summaries_use_replicate": 0, "repeatability_scope": "conditional on original prefix and partition",
        "populations": populations, "world_contrasts": primary,
        "summaries": summarize_contrasts(primary, populations), "repeat_contrasts": repeats,
        "repeatability": repeatability, "trajectory_changes": changes}
