"""Offline paired world uncertainty and shared-response sensitivity (spec §6).

Only original scheduled outcomes are observations. Sensitivity can constrain an
unexecuted logical copy using its recorded parent, without claiming execution.
All exports are derived; no inference, optimizer or additional store is used.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, fsum, isfinite, log, sqrt
from random import Random

from .analysis import MAIN_FAMILIES, SUMMARY_KEYS, _exact, _fraction

DRAWS = 10_000
DEFAULT_SEED = 20261006
QUANTILE = "linear interpolation at (B-1)*p; Hyndman-Fan type 7"
LIMITATION = ("Approximate percentile coverage; families are fixed tasks. The bounded-mean "
              "companion assumes independent generated worlds and does not cover systematic errors.")


def percentile(values, probability):
    """Explicit interpolation, including singleton samples and both endpoints."""
    if not values or not 0 <= probability <= 1 or any(not isfinite(v) for v in values):
        raise ValueError("percentile requires finite samples and a probability in [0,1]")
    values = sorted(values)
    position = (len(values) - 1) * probability
    i = int(position)
    return values[i] + (position - i) * (values[min(i + 1, len(values) - 1)] - values[i])


@lru_cache(maxsize=None)
def exact_binomial(successes, count, alpha=0.05):
    """Two-sided Clopper-Pearson bounds by exact binomial-tail inversion.

    Count zero is unavailable. Extreme counts have closed forms. The study's
    small fixed family sizes need neither SciPy nor an incomplete-beta library.
    """
    if (type(count) is not int or type(successes) is not int or not 0 <= successes <= count
            or not 0 < alpha < 1):
        raise ValueError("invalid binomial counts/error level")
    if not count:
        return None
    tail = alpha / 2
    if successes == 0:
        return [0.0, 1 - tail ** (1 / count)]
    if successes == count:
        return [tail ** (1 / count), 1.0]
    def invert(start, end, increasing):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            p = (lo + hi) / 2
            value = fsum(comb(count, k) * p ** k * (1 - p) ** (count - k)
                         for k in range(start, end + 1))
            if (value < tail) == increasing:
                lo = p
            else:
                hi = p
        return (lo + hi) / 2
    return [invert(successes, count, True), invert(0, successes, False)]


def hoeffding(estimate, limits, family_counts, alpha):
    if (not family_counts or any(type(n) is not int or n <= 0 for n in family_counts.values())
            or not 0 < alpha < 1 or not limits[0] <= estimate <= limits[1]):
        raise ValueError("invalid bounded-mean population/range")
    F = len(family_counts)
    squares = fsum(1 / (F * F * n) for n in family_counts.values())
    half = (limits[1] - limits[0]) * sqrt(0.5 * log(2 / alpha) * squares)
    return dict(interval=[max(limits[0], estimate - half), min(limits[1], estimate + half)],
        half_width=half, alpha=alpha, range=list(limits), sum_squared_world_weights=squares,
        world_weight_by_family={f: 1 / (F * n) for f, n in family_counts.items()},
        interpretation=LIMITATION)


def world_resamples(world_ids, seed):
    """One family stream. Draw IDs, never peer/round/replicate observations."""
    ids = tuple(sorted(world_ids))
    if not ids or len(set(ids)) != len(ids) or type(seed) is not int:
        raise ValueError("resampling requires unique world IDs and an integer seed")
    rng = Random(seed)
    return [tuple(rng.randrange(len(ids)) for _ in ids) for _ in range(DRAWS)]


def paired_interval(rows, families, *, seed=DEFAULT_SEED, primary=False, limits=None, cache=None):
    """Equal family means from the same family/world draws for every endpoint.

    The caller supplies an explicit eligible/observed cohort. Missing families
    yield N/A; this function never chooses a complete-case population itself.
    """
    if type(seed) is not int or len(set(families)) != len(families) or set(families) - set(MAIN_FAMILIES):
        raise ValueError("invalid resampling seed/families")
    seen, groups = set(), {f: [] for f in families}
    for row in rows:
        if row["world_id"] in seen or row["family"] not in groups:
            raise ValueError("duplicate/out-of-population world cluster")
        seen.add(row["world_id"])
        groups[row["family"]].append(row)
    groups = {f: sorted(v, key=lambda r: r["world_id"]) for f, v in groups.items()}
    counts = {f: len(v) for f, v in groups.items()}
    alpha = 0.025 if primary else 0.05
    probabilities = [alpha / 2, 1 - alpha / 2]
    base = dict(draws=DRAWS, seed=seed, probabilities=probabilities, quantile=QUANTILE,
        family_denominators=counts, independent_worlds=len(rows),
        family_world_ids={f: [r["world_id"] for r in v] for f, v in groups.items()},
        family_seeds={f: seed + MAIN_FAMILIES.index(f) for f in families},
        interval=None, estimate=None, degenerate=None, hoeffding=None, limitation=LIMITATION)
    if not families or any(not v for v in groups.values()):
        return dict(base, reason="empty_eligible_population_or_family")
    if any(r["value"] is None or not isfinite(r["value"]) for r in rows):
        return dict(base, reason="unknown_world_components")
    values = {f: [r["value"] for r in v] for f, v in groups.items()}
    estimate = fsum(fsum(v) / len(v) for v in values.values()) / len(families)
    constant = all(all(v == xs[0] for v in xs) for xs in values.values())
    cache = {} if cache is None else cache
    if constant:
        # These are exactly the 10,000 draws' identical values, not fewer draws.
        interval = [estimate, estimate]
    else:
        means = []
        for f, xs in values.items():
            key = f, tuple(base["family_world_ids"][f]), base["family_seeds"][f]
            if key not in cache:
                cache[key] = world_resamples(key[1], key[2])
            means.append([fsum(xs[i] for i in draw) / len(xs) for draw in cache[key]])
        samples = [fsum(v) / len(families) for v in zip(*means)]
        interval = [percentile(samples, p) for p in probabilities]
    return dict(base, estimate=estimate, interval=interval, degenerate=constant, reason=None,
        hoeffding=hoeffding(estimate, limits, counts, alpha) if constant and limits is not None else None)


def _put_known(values, key, value):
    if value is not None:
        if key in values and values[key] != value:
            raise ValueError("conflicting recorded values for a shared response")
        values[key] = value


def shared_values(outcomes, diagnostics=()):
    """Known constraints, without changing the original execution/unknown flags."""
    values = {}
    for row in outcomes:
        c = row["correct"]
        if c is not None and (type(c) is not int or c not in (0, 1)):
            raise ValueError("correctness must be 0/1/unknown")
        if row["protocol_outcome"] in ("invalid", "failed") and c != 0:
            raise ValueError("recorded failures must stay zero")
        _put_known(values, ("correct", row["generation_id"]), None if c is None else Fraction(c))
    for row in diagnostics:
        if row["metric"] == "preservation" and row["denominator"]:
            value = None if row["numerator"] is None else Fraction(row["numerator"], row["denominator"])
            _put_known(values, ("preservation", row["generation_id"], tuple(row["eligible_coordinates"])), value)
    return values


def _atom_key(atom, endpoint):
    return (("preservation", atom["generation_id"], tuple(atom["eligible_coordinates"]))
            if endpoint == "preservation" else ("correct", atom["generation_id"]))


def _identity(key):
    return [list(v) if isinstance(v, tuple) else v for v in key]


def contrast_bounds(row, known=None):
    """Combine shared coefficients before extrema; retain shared conjunctions.

    Small overlapping conjunctions are enumerated directly. Larger nonlinear
    expressions use a conservative shared-monomial envelope, not an optimizer.
    Unknown prefix eligibility can change diagnostic denominators: its broad
    bound is conditional on a nonempty eligible population and is labeled so.
    """
    known = known or {}
    if row["eligibility"] == "ineligible":
        return dict(interval=None, exact=None, method="structurally_ineligible", unknowns=[])
    if row["eligibility"] == "unknown":
        coefficients = defaultdict(Fraction)
        for c in row["components"]:
            signature = (c["endpoint"], c["operator"], tuple(c["rounds"]), tuple(c["peers"]),
                c["branch_id"] if not c["atoms"] else None,
                tuple((a["generation_id"], a.get("prefix_call_id"), a.get("denominator"),
                       tuple(a.get("eligible_coordinates", ()))) for a in c["atoms"]))
            coefficients[signature] += Fraction(str(c["coefficient"]))
        cancelled = bool(coefficients) and all(v == 0 for v in coefficients.values())
        return dict(interval=[0, 0] if cancelled else list(row["range"]), exact=None, unknowns=[],
            method="conditional_shared_endpoint_cancellation" if cancelled else "conservative_unknown_prefix_eligibility",
            response_ids=sorted({a["generation_id"] for c in row["components"] for a in c["atoms"]}),
            limitation="Conditional on defined endpoints; eligibility/denominators unknown and endpoint may be undefined.")
    constant, terms = Fraction(), defaultdict(Fraction)
    nonlinear = any(c["operator"] == "all" for c in row["components"])
    for component in row["components"]:
        coefficient = Fraction(str(component["coefficient"]))
        atoms = component["atoms"]
        if not atoms:
            # An unavailable component retains its existing branch/scope ID.
            key = ("unavailable", component["branch_id"], component["endpoint"],
                   tuple(component["rounds"]), tuple(component["peers"]))
            terms[frozenset((key,))] += coefficient
            continue
        if component["operator"] == "all":
            keys, zero = set(), False
            for atom in atoms:
                key = _atom_key(atom, component["endpoint"])
                value = known.get(key, atom["correct"])
                if value == 0:
                    zero = True
                elif value is None:
                    keys.add(key)
            if not zero:
                if keys:
                    terms[frozenset(keys)] += coefficient
                else:
                    constant += coefficient
        else:
            for atom in atoms:
                if atom["exact_weight"] is None:
                    continue  # Structurally empty preservation peers.
                weight = _fraction({"exact": atom["exact_weight"]})
                key = _atom_key(atom, component["endpoint"])
                fallback = atom["value"]
                if component["endpoint"] == "preservation":
                    fallback = None if atom["numerator"] is None else Fraction(atom["numerator"], atom["denominator"])
                value = known.get(key, fallback)
                if value is None:
                    terms[frozenset((key,))] += coefficient * weight
                else:
                    constant += coefficient * weight * Fraction(value)
    terms = {keys: c for keys, c in terms.items() if c}
    variables = sorted(set().union(*terms) if terms else set(), key=repr)
    if nonlinear and len(variables) <= 12:
        values = []
        for bits in product((0, 1), repeat=len(variables)):
            assigned = dict(zip(variables, bits))
            values.append(constant + sum((c for keys, c in terms.items()
                                          if all(assigned[k] for k in keys)), Fraction()))
        interval, method = [min(values), max(values)], "exact_shared_binary_enumeration"
    else:
        interval = [constant + sum((min(0, c) for c in terms.values()), Fraction()),
                    constant + sum((max(0, c) for c in terms.values()), Fraction())]
        method = "conservative_shared_monomial_envelope" if nonlinear else "exact_shared_linear"
    return dict(interval=[float(v) for v in interval], exact=[_exact(v) for v in interval],
        method=method, unknowns=[_identity(k) for k in variables],
        combined_terms=[dict(identities=[_identity(k) for k in sorted(keys, key=repr)], coefficient=_exact(c))
                        for keys, c in sorted(terms.items(), key=lambda item: repr(sorted(item[0], key=repr)))],
        limitation="Envelope extrema need not be simultaneously attainable." if method.startswith("conservative") else None)


def contrast_uncertainty(estimands, known, *, seed=DEFAULT_SEED, cache=None):
    """Intended estimates, separately labeled complete cases and frozen bounds."""
    grouped, bounds, summaries = defaultdict(list), [], []
    for row in estimands["world_contrasts"]:
        key = tuple(row[k] for k in SUMMARY_KEYS)
        grouped[key].append(row)
        bounds.append({k: row[k] for k in (*SUMMARY_KEYS, "world_id", "family")} |
            dict(sensitivity=contrast_bounds(row, known), execution_observed=row["exact"] is not None))
    by_bound = {(tuple(r[k] for k in SUMMARY_KEYS), r["world_id"]): r["sensitivity"] for r in bounds}
    cache = {} if cache is None else cache
    for summary in estimands["summaries"]:
        key = tuple(summary[k] for k in SUMMARY_KEYS)
        ids = set(summary["world_ids"])
        group = [r for r in grouped[key] if r["world_id"] in ids]
        eligible = [r for r in group if r["eligibility"] != "ineligible"]
        observed = [r for r in eligible if r["exact"] is not None]
        families = list(summary["family_denominators"])
        primary = summary["primary"] and summary["level"] == "all_families"
        intended = paired_interval(eligible, families, seed=seed, primary=primary, limits=summary["range"], cache=cache)
        cc = paired_interval(observed, families, seed=seed, primary=primary, limits=summary["range"], cache=cache)
        cc["label"] = "Descriptive complete cases; not the frozen-population estimand or its interval."
        if not eligible or summary["missing_families"]:
            sensitivity = dict(interval=None, method="empty_eligible_population_or_family")
        elif any(r["eligibility"] == "unknown" for r in eligible):
            sensitivity = dict(interval=[min(by_bound[key, r["world_id"]]["interval"][0] for r in eligible),
                                         max(by_bound[key, r["world_id"]]["interval"][1] for r in eligible)],
                method="conservative_unknown_eligibility",
                limitation="Conditional on nonempty eligible families; inclusion and denominators may change.")
        else:
            averages = []
            for j in (0, 1):
                averages.append(fsum(fsum(by_bound[key, r["world_id"]]["interval"][j]
                    for r in eligible if r["family"] == f) / n
                    for f, n in summary["family_denominators"].items()) / len(families))
            sensitivity = dict(interval=averages, method="equal_family_world_sensitivity",
                limitation="Completion extrema are sensitivity bounds, not confidence intervals.")
        atoms = {a["call_id"]: a for r in eligible for c in r["components"] for a in c["atoms"]}
        summaries.append({k: summary[k] for k in (*SUMMARY_KEYS, "level", "family", "range",
                "scheduled_worlds", "eligible_worlds", "observed_worlds", "unknown_worlds",
                "unknown_eligibility_worlds", "ineligible_worlds", "family_denominators", "world_ids")} |
            dict(primary_interval=primary, intended_population=intended, complete_case_description=cc,
                sensitivity=sensitivity, paired_coverage=dict(scheduled_calls=len(atoms),
                    executed_calls=sum(a["correct"] is not None for a in atoms.values()),
                    unknown_calls=sum(a["correct"] is None for a in atoms.values()),
                    distinct_response_ids=len({a["generation_id"] for a in atoms.values()}),
                    unresolved_response_ids=len({a["generation_id"] for a in atoms.values()
                        if ("correct", a["generation_id"]) not in known}))))
    return dict(world_bounds=bounds, summaries=summaries)


def reporting_references():
    """The specification's rough power/fallback arithmetic, never achieved power."""
    return dict(practical_difference=0.10, main=[dict(N=n, sd=sd, multiplier=3.08,
        reference=3.08 * sd / sqrt(n)) for n in (60, 40) for sd in (0.35, 0.60)],
        focal=[dict(N=n, sd=sd, multiplier=2.80, reference=2.80 * sd / sqrt(n))
               for n in (24, 16) for sd in (0.35, 0.60)],
        fallback_standard_error_ratio=sqrt(60 / 40),
        interpretation="Prespecified normal-approximation sensitivity references; not achieved power, "
            "a detection promise, or an equivalence margin.")


TRAJECTORY_CATEGORIES = ("continuously_correct", "correct_at_end_after_delay_or_regression",
    "temporarily_correct_but_incorrect_at_end", "never_jointly_correct")


def trajectory_bounds(rows, known=None):
    """Shared variables survive nonlinear trajectory completion, never splicing.

    Enumerate at most eight unknown replies. Larger missing branches use a
    conservative envelope with monotonic endpoints and witnessed constraints.
    First/stable completion times are not assigned to incomplete execution.
    """
    from .evaluate import trajectory
    known = known or {}
    rows = sorted(rows, key=lambda r: (r["round"], r["peer"]))
    if len(rows) != 16 or [(r["round"], r["peer"]) for r in rows] != [(r, p) for r in range(1, 5) for p in range(4)]:
        raise ValueError("trajectory sensitivity requires all sixteen scheduled opportunities")
    values = {r["generation_id"]: known.get(("correct", r["generation_id"]), r["correct"]) for r in rows}
    unknown = sorted(gid for gid, v in values.items() if v is None)
    def completed(bits):
        resolved = dict(values)
        resolved.update(zip(unknown, bits))
        matrix = [[int(resolved[r["generation_id"]]) for r in rows if r["round"] == number]
                  for number in range(1, 5)]
        return trajectory(matrix)
    def metrics(t):
        return dict(final_joint=t["final_joint"], joint_ever=int(t["joint_ever"]),
            all_individually_ever=int(all(t["individual_ever"])),
            individual_ever_mean=sum(t["individual_ever"]) / 4,
            fragmented=int(t["fragmented"]), regression=int(t["regression"]),
            **{category: int(t["category"] == category) for category in TRAJECTORY_CATEGORIES})
    if len(unknown) <= 8:
        completions = [metrics(completed(bits)) for bits in product((0, 1), repeat=len(unknown))]
        bounds = {k: [min(t[k] for t in completions), max(t[k] for t in completions)] for k in completions[0]}
        method = "exact_shared_trajectory_enumeration"
    else:
        low, high = completed([0]*len(unknown)), completed([1]*len(unknown))
        lo, hi = metrics(low), metrics(high)
        bounds = {k: [lo[k], hi[k]] for k in ("final_joint", "joint_ever", "all_individually_ever", "individual_ever_mean")}
        bounds["continuously_correct"] = [int(all(low["joint"])), int(all(high["joint"]))]
        bounds["never_jointly_correct"] = [1-hi["joint_ever"], 1-lo["joint_ever"]]
        for category, possible, forced in (
                ("correct_at_end_after_delay_or_regression", hi["final_joint"] and not all(low["joint"]),
                 lo["final_joint"] and not all(high["joint"])),
                ("temporarily_correct_but_incorrect_at_end", any(high["joint"][:3]) and not lo["final_joint"],
                 any(low["joint"][:3]) and not hi["final_joint"]),
                ("fragmented", hi["all_individually_ever"] and not lo["joint_ever"],
                 lo["all_individually_ever"] and not hi["joint_ever"]),
                ("regression", any(high["joint"][i] and not low["joint"][j] for i in range(4) for j in range(i+1, 4)),
                 any(low["joint"][i] and not high["joint"][j] for i in range(4) for j in range(i+1, 4)))):
            bounds[category] = [int(bool(forced)), int(bool(possible))]
        method = "conservative_shared_trajectory_envelope"
    return dict(method=method, metrics=bounds, unknown_response_ids=unknown,
        response_ids=[r["generation_id"] for r in rows],
        execution_complete=all(r["correct"] is not None for r in rows),
        limitation="Marginal metric/category extrema need not be jointly attainable; no missing completion time is imputed.")


def completion_and_trajectories(branches, outcomes, known):
    """Family completion counts and frozen-population trajectory sensitivity."""
    by_branch, world_rows, grouped = defaultdict(list), [], defaultdict(list)
    for row in outcomes:
        by_branch[row["branch_id"]].append(row)
    for branch in branches:
        if branch.phase == "control":
            continue
        rows = by_branch[branch.branch_id]
        sensitivity = trajectory_bounds(rows, known)
        from .evaluate import trajectory
        observed = trajectory([[r["correct"] for r in sorted(rows, key=lambda r: r["peer"])
                                if r["round"] == number] for number in range(1, 5)])
        row = dict(world_id=branch.world_id, family=branch.task.value, branch_id=branch.branch_id,
            phase=branch.phase, event=branch.event, policy=branch.policy, replicate=branch.replicate,
            observed=observed, sensitivity=sensitivity)
        world_rows.append(row)
        grouped[branch.phase, branch.event, branch.policy, branch.replicate, branch.task.value].append(row)
    counts = []
    for key, rows in sorted(grouped.items(), key=lambda item: repr(item[0])):
        complete_final = [r for r in rows if all(v is not None for v in r["observed"]["joint"][-1:])]
        # The evaluator's joint remains unknown until all four final replies are
        # recorded, even when a known failure already constrains sensitivity.
        successes = sum(r["observed"]["final_joint"] for r in complete_final)
        n, total = len(complete_final), len(rows)
        lo = sum(r["sensitivity"]["metrics"]["final_joint"][0] for r in rows)
        hi = sum(r["sensitivity"]["metrics"]["final_joint"][1] for r in rows)
        counts.append(dict(zip(("phase", "event", "policy", "replicate", "family"), key)) |
            dict(scheduled_worlds=total, executed_final_worlds=n, successes=successes, failures=n-successes,
                unknown_final_worlds=total-n, execution_complete_trajectories=sum(r["observed"]["complete"] for r in rows),
                incomplete_trajectories=sum(not r["observed"]["complete"] for r in rows),
                observed_category_counts=dict(Counter(r["observed"]["category"] for r in rows)),
                exact_binomial=exact_binomial(successes, n) if n == total else None,
                complete_case_binomial_description=exact_binomial(successes, n),
                binomial_alpha=0.05, binomial_method="two-sided Clopper-Pearson within this eligible family",
                binomial_scope="Final joint completion across worlds, not peer/round/repeat trials.",
                possible_success_counts=[lo, hi],
                frozen_population_proportion_bounds=[lo/total, hi/total],
                trajectory_metric_bounds={metric: [fsum(r["sensitivity"]["metrics"][metric][j] for r in rows)/total
                    for j in (0, 1)] for metric in rows[0]["sensitivity"]["metrics"]},
                world_ids=[r["world_id"] for r in rows]))
    return dict(world_trajectories=world_rows, family_completion=counts)


def trajectory_summaries(rows, populations, *, seed=DEFAULT_SEED, cache=None):
    """World/family trajectory displays, with incomplete branches still in N."""
    grouped, result = defaultdict(list), []
    families = {p["population"]: p["families"] for p in populations}
    for row in rows:
        grouped[row["phase"], row["event"], row["policy"], row["replicate"]].append(row)
    for (phase, event, policy, replicate), group in sorted(grouped.items(), key=lambda item: repr(item[0])):
        population = ("preserving" if event == "preserving" else "receipts" if policy and policy.endswith("_delta")
                      else "prose_delay" if policy and policy.startswith("Q_") else "main")
        targets = families[population]
        counts = {f: sum(r["family"] == f for r in group) for f in targets}
        complete = [r for r in group if r["observed"]["complete"]]
        for metric in group[0]["sensitivity"]["metrics"]:
            observed = []
            for row in group:
                values = row["sensitivity"]["metrics"][metric]
                observed.append(dict(world_id=row["world_id"], family=row["family"],
                    value=values[0] if row["observed"]["complete"] else None))
            bound = [fsum(fsum(r["sensitivity"]["metrics"][metric][j] for r in group if r["family"] == f)/n
                          for f, n in counts.items())/len(targets) for j in (0, 1)] if all(counts.values()) else None
            result.append(dict(phase=phase, event=event, policy=policy, replicate=replicate,
                population=population, metric=metric, scheduled_worlds=len(group),
                complete_worlds=len(complete), incomplete_worlds=len(group)-len(complete),
                family_denominators=counts, world_ids=[r["world_id"] for r in group],
                intended_population=paired_interval(observed, targets, seed=seed, limits=[0, 1], cache=cache),
                complete_case_description=dict(paired_interval([r for r in observed if r["value"] is not None],
                    targets, seed=seed, limits=[0, 1], cache=cache), label="Complete trajectory description, not the frozen population."),
                sensitivity=dict(interval=bound, method="equal_family_marginal_trajectory_bounds",
                    limitation="Shared variables retained within worlds; displayed marginal extrema need not be jointly attainable.")))
    return result


def _duration_bounds(components, generations):
    """Shared original costs cancel before bounding unavailable future work."""
    coefficients = Counter()
    for coefficient, ids in components:
        for gid in ids:
            coefficients[gid] += coefficient
    lower, upper, unknown = 0.0, 0.0, []
    for gid, coefficient in sorted(coefficients.items()):
        if not coefficient:
            continue
        row = generations[gid]
        a, b = row["seconds"]
        if row["protocol_outcome"] == "unknown":
            b = None  # No measured/frozen bound for all future work of this policy.
            unknown.append(gid)
        if coefficient > 0:
            if lower is not None:
                lower += coefficient * a
            upper = None if upper is None or b is None else upper + coefficient * b
        else:
            lower = None if lower is None or b is None else lower + coefficient * b
            if upper is not None:
                upper += coefficient * a
    return dict(interval=[lower, upper], method="shared_original_generation_costs",
        lower_unbounded=lower is None, upper_unbounded=upper is None,
        unknown_response_ids=unknown,
        limitation="Missing future policy work has no asserted finite cost bound; allocation caps are not policy measurements.")


def policy_display_rows(branches, tables, known):
    """Whole-policy and frozen-rule paired quality/preservation/cost records."""
    from .analysis import endpoint_component
    by_branch = {b.branch_id: b for b in branches}
    outcomes, diagnostics = defaultdict(list), defaultdict(list)
    for r in tables["outcomes"]:
        outcomes[r["branch_id"]].append(r)
    for r in tables["peer_diagnostics"]:
        diagnostics[r["branch_id"]].append(r)
    costs = tables["costs"]
    by_cost = {r["branch_id"]: r for r in costs["policy_costs"]}
    generations = {r["call_id"]: r for r in costs["generations"]}
    by_quality = {r["branch_id"]: r for r in costs["quality_preservation"]}
    for bid, row in by_cost.items():
        if bid not in by_branch:
            raise ValueError("cost table contains an unscheduled branch")
        branch = by_branch[bid]
        used = (*by_branch[branch.prefix_parent].calls, *branch.calls) if branch.prefix_parent else branch.calls
        if (row["call_ids"] != [c.call_id for c in used] or row["generation_ids"] != [c.generation_id for c in used]
                or row["world_id"] != branch.world_id or row["family"] != branch.task.value):
            raise ValueError("policy cost differs from original whole-branch schedule identity")
    cache, result = {}, []
    def endpoint(bid, metric):
        key = bid, metric
        if key not in cache:
            branch = by_branch[bid]
            name = "preservation" if metric == "final_preservation" else metric
            cache[key] = endpoint_component(branch, outcomes[bid], name,
                rounds=(4,) if metric in ("final_joint", "final_preservation") else (1, 2, 3, 4),
                diagnostics=diagnostics[bid])
        return cache[key]
    def emit(base, display, terms, *, population="main"):
        available = all(bid in by_quality and by_quality[bid]["complete"] and by_cost[bid]["complete"] for _, bid in terms)
        metrics = {}
        for metric in ("auc", "final_joint", "preservation", "final_preservation"):
            components = [dict(endpoint(bid, metric), coefficient=c) for c, bid in terms if bid in by_branch]
            limits = [sum(min(0, c) for c, _ in terms), sum(max(0, c) for c, _ in terms)]
            eligibility = ("unknown" if any(c["eligibility"] == "unknown" for c in components) or
                           "preservation" in metric and len(components) != len(terms) else
                           "ineligible" if any(c["eligibility"] == "ineligible" for c in components) else "eligible")
            known_components = len(components) == len(terms)
            value = sum(c["coefficient"] * c["value"] for c in components) if available and all(c["value"] is not None for c in components) else None
            sensitivity = (contrast_bounds(dict(components=components, range=limits, eligibility=eligibility), known)
                           if known_components else dict(interval=limits, method="conservative_unknown_rule_selection"))
            metrics[metric] = dict(value=value, observed=value is not None, eligibility=eligibility,
                range=limits, sensitivity=sensitivity, measured_interval=[value, value] if value is not None else None)
        durations = [(c, by_cost[bid]["generation_ids"]) for c, bid in terms if bid in by_cost]
        duration = (_duration_bounds(durations, generations) if len(durations) == len(terms) else
                    dict(interval=[None, None] if len(terms) > 1 else [0, None], method="unknown_rule_selection",
                         upper_unbounded=True, lower_unbounded=len(terms) > 1))
        measured = duration["interval"] if available else None
        metrics["policy_seconds"] = dict(value=measured[0] if measured and measured[0] == measured[1] else None,
            observed=measured is not None, eligibility="eligible", range=None, sensitivity=duration,
            measured_interval=measured)
        result.append(dict(base, display=display, population=population, quality_cost_available=available,
            whole_branch_terms=[dict(coefficient=c, branch_id=bid) for c, bid in terms], metrics=metrics))
    for q in costs["quality_preservation"]:
        if q["replicate"] != 0:
            continue
        base = {k: q[k] for k in ("world_id", "family", "event", "replicate", "prefix_parent")}
        population = "preserving" if q["event"] == "preserving" else "receipts" if q["policy"].endswith("_delta") else "prose_delay" if q["policy"].startswith("Q_") else "main"
        emit(base, "policy_" + q["policy"], [(1, q["branch_id"])], population=population)
    for selection in costs["boundary_selections"]:
        if selection["replicate"] != 0:
            continue
        base = {k: selection[k] for k in ("world_id", "family", "event", "replicate", "prefix_parent")}
        population = "preserving" if selection["event"] == "preserving" else "main"
        chosen = selection["selected_branch_id"]
        if chosen is not None and chosen != selection["comparator_branch_ids"].get(selection["selected_policy"]):
            raise ValueError("boundary rule must select its entire recorded C/K branch")
        emit(base, "boundary_rule", [(1, chosen)], population=population)
        for policy, bid in selection["comparator_branch_ids"].items():
            emit(base, "boundary_rule-always_" + policy, [(1, chosen), (-1, bid)], population=population)
    return result


def policy_display_summaries(rows, populations, *, seed=DEFAULT_SEED, cache=None):
    """Use common world cohorts for paired quality/preservation/cost intervals."""
    groups, result = defaultdict(list), []
    cache = {} if cache is None else cache
    families = {p["population"]: p["families"] for p in populations}
    for row in rows:
        groups[row["population"], row["display"], row["event"]].append(row)
    for (population, display, event), group in sorted(groups.items()):
        for family in [*families[population], None]:
            current = [r for r in group if family is None or r["family"] == family]
            for metric in group[0]["metrics"]:
                included = [r for r in current if r["metrics"][metric]["eligibility"] != "ineligible"]
                targets = [family] if family else list(families[population])
                if "preservation" in metric:
                    targets = [f for f in targets if any(r["family"] == f for r in included)]
                observed = [r for r in included if r["quality_cost_available"] and r["metrics"][metric]["observed"]]
                def intervals(cohort, measure=None):
                    # The two ends share draws and world identities. For uncertain
                    # durations this is a percentile envelope, not a point CI.
                    measure = metric if measure is None else measure
                    ends = [paired_interval([dict(world_id=r["world_id"], family=r["family"],
                        value=r["metrics"][measure]["measured_interval"][j] if r["metrics"][measure]["measured_interval"] else None)
                        for r in cohort], targets, seed=seed, limits=group[0]["metrics"][measure]["range"], cache=cache)
                        for j in (0, 1)]
                    return dict(lower=ends[0], upper=ends[1], interval=[ends[0]["interval"][0], ends[1]["interval"][1]]
                        if all(e["interval"] is not None for e in ends) else None,
                        interpretation="Paired percentile envelope across measured endpoints; unknown future costs are excluded only from labeled descriptions.")
                den = {f: sum(r["family"] == f for r in included) for f in targets}
                sensitivity = None
                unknown_eligibility = any(r["metrics"][metric]["eligibility"] == "unknown" for r in included)
                if included and targets and all(den.values()):
                    if unknown_eligibility:
                        sensitivity = [min(r["metrics"][metric]["sensitivity"]["interval"][0] for r in included),
                                       max(r["metrics"][metric]["sensitivity"]["interval"][1] for r in included)]
                    else:
                        sensitivity = []
                        for j in (0, 1):
                            endpoints = [r["metrics"][metric]["sensitivity"]["interval"][j] for r in included]
                            sensitivity.append(None if None in endpoints else fsum(fsum(
                                r["metrics"][metric]["sensitivity"]["interval"][j] for r in included if r["family"] == f)/n
                                for f, n in den.items()) / len(targets))
                result.append(dict(population=population, display=display, event=event, metric=metric,
                    level="family" if family else "all_families", family=family,
                    scheduled_worlds=len(current), eligible_worlds=len(included), paired_observed_worlds=len(observed),
                    unknown_worlds=len(included)-len(observed), unknown_eligibility=unknown_eligibility,
                    family_denominators=den, world_ids=[r["world_id"] for r in current],
                    intended_population=intervals(included), complete_case_description=dict(intervals(observed),
                        label="Paired complete-case description; does not replace the frozen population."),
                    paired_cost=None if metric == "policy_seconds" else dict(
                        intended_population=intervals(included, "policy_seconds"),
                        complete_case_description=intervals(observed, "policy_seconds"),
                        interpretation="Cost axis uses this endpoint's same eligible/observed world cohort and draws."),
                    sensitivity=dict(interval=sensitivity, method="conservative_unknown_eligibility" if unknown_eligibility else "equal_family_world_bounds",
                        interpretation="Sensitivity, not statistical uncertainty; null cost ends mean unbounded.")))
    return result


def uncertainty_records(worlds, branches, tables, *, seed=DEFAULT_SEED):
    """Use the existing validated joins; derive all §6 tables without new I/O."""
    from .analysis import analyze_estimands
    if type(seed) is not int:
        raise ValueError("resampling seed must be an integer")
    worlds, branches = tuple(worlds), tuple(branches)
    # Reconstruct rather than trusting a stale derived estimand/trajectory export.
    estimands = analyze_estimands(worlds, branches, tables)
    known = shared_values(tables["outcomes"], tables["peer_diagnostics"])
    cache = {}
    result = contrast_uncertainty(estimands, known, seed=seed, cache=cache)
    result.update(completion_and_trajectories(branches, tables["outcomes"], known))
    result["trajectory_summaries"] = trajectory_summaries(result["world_trajectories"], estimands["populations"], seed=seed, cache=cache)
    displays = policy_display_rows(branches, tables, known) if "costs" in tables else []
    result.update(policy_world_displays=displays,
        policy_display_summaries=policy_display_summaries(displays, estimands["populations"], seed=seed, cache=cache),
        cost_display_status="available" if "costs" in tables else "requires_original_cost_tables",
        kind="Paired uncertainty and missingness; scripted data are CPU validation, not empirical findings",
        settings=dict(draws=DRAWS, seed=seed, family_seeds={f: seed+i for i, f in enumerate(MAIN_FAMILIES)},
            rng="Python random.Random; randrange(n), n draws per family per resample in sorted world-ID order",
            quantile=QUANTILE, primary_probabilities=[0.0125, 0.9875], secondary_probabilities=[0.025, 0.975],
            cluster="Generated world and one realized prefix; all siblings, peers, rounds, groups, controls and repeats travel together",
            replicate_zero_only=True, weighting="equal eligible-family means", limitation=LIMITATION),
        reporting_references=reporting_references(), populations=estimands["populations"], coverage=tables.get("coverage"))
    return result


def uncertainty_run(worlds, branches, paths, *, seed=DEFAULT_SEED, now=None, diagnostics=False, tokenizer=None):
    """One original-worker read; costs/estimands accompany uncertainty exports."""
    from .costs import costs_run
    worlds, branches = tuple(worlds), tuple(branches)
    tables = costs_run(worlds, branches, paths, now=now, diagnostics=diagnostics, estimands=True, tokenizer=tokenizer)
    tables["uncertainty"] = uncertainty_records(worlds, branches, tables, seed=seed)
    return tables
