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
        return dict(interval=list(row["range"]), exact=None, unknowns=[],
            method="conservative_unknown_prefix_eligibility",
            limitation="Eligibility/denominators unknown; endpoint may be undefined.")
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
                fallback = (None if atom["numerator"] is None else Fraction(atom["numerator"], atom["denominator"])) if component["endpoint"] == "preservation" else atom["value"]
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
        method=method, unknowns=[list(k) for k in variables],
        combined_terms=[dict(identities=[list(k) for k in sorted(keys, key=repr)], coefficient=_exact(c))
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
        group = [r for r in grouped[key] if r["world_id"] in set(summary["world_ids"])]
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
            sensitivity = dict(interval=summary["range"], method="conservative_unknown_eligibility",
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
