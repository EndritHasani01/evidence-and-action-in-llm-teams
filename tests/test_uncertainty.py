"""Independent arithmetic and finite-completion checks for spec §6."""

from fractions import Fraction
from itertools import product
import math
import unittest

from recovery.analysis import MAIN_FAMILIES, _exact
from recovery.uncertainty import (DRAWS, contrast_bounds, contrast_uncertainty, exact_binomial, hoeffding,
    paired_interval, percentile, reporting_references, shared_values, world_resamples)


def component(ids, *, operator="mean", coefficient=1, values=None):
    values = values or {}
    return dict(branch_id="fixture", endpoint="final_joint" if operator == "all" else "auc",
        rounds=[4], peers=list(range(len(ids))), operator=operator, coefficient=coefficient,
        atoms=[dict(generation_id=gid, correct=values.get(gid), value=values.get(gid),
                    exact_weight=_exact(Fraction(1, len(ids)))) for gid in ids])


def contrast(*components, eligibility="eligible"):
    return dict(eligibility=eligibility, range=[sum(min(0, c["coefficient"]) for c in components),
        sum(max(0, c["coefficient"]) for c in components)], components=list(components))


class StatisticalArithmeticTests(unittest.TestCase):
    def test_percentile_exact_primary_and_secondary_endpoints(self):
        xs = list(range(10_000))
        for p, expected in ((0.0125, 124.9875), (0.9875, 9874.0125),
                            (0.025, 249.975), (0.975, 9749.025)):
            self.assertAlmostEqual(percentile(xs, p), expected)
        self.assertEqual([percentile([7], p) for p in (0, 0.5, 1)], [7, 7, 7])
        self.assertEqual(percentile([3, 1, 2], 0), 1)
        self.assertEqual(percentile([3, 1, 2], 1), 3)
        for xs, p in (([], 0.5), ([math.nan], 0.5), ([1], -0.1)):
            with self.assertRaises(ValueError):
                percentile(xs, p)

    def test_exact_binomial_extremes_mixed_counts_and_empty(self):
        self.assertEqual(exact_binomial(0, 0), None)
        self.assertAlmostEqual(exact_binomial(12, 12)[0], 0.7353515306029488)
        self.assertEqual(exact_binomial(12, 12)[1], 1)
        self.assertAlmostEqual(exact_binomial(0, 12)[1], 0.2646484693970512)
        self.assertEqual(exact_binomial(0, 12)[0], 0)
        self.assertAlmostEqual(exact_binomial(1, 2)[0], 1 - math.sqrt(0.975))
        self.assertAlmostEqual(exact_binomial(1, 2)[1], math.sqrt(0.975))
        # Independent published SciPy exact-binomial documentation example.
        self.assertAlmostEqual(exact_binomial(7, 50)[0], 0.05819170033997342)
        self.assertAlmostEqual(exact_binomial(7, 50)[1], 0.26739600249700846)
        self.assertLess(exact_binomial(12, 12, 0.025)[0], exact_binomial(12, 12)[0])
        with self.assertRaises(ValueError):
            exact_binomial(3, 2)

    def test_weighted_hoeffding_formula_ranges_alpha_and_clipping(self):
        counts = dict.fromkeys(MAIN_FAMILIES, 12)
        result = hoeffding(0, [-2, 2], counts, 0.025)
        expected = 4 * math.sqrt(math.log(80) / 120)
        self.assertAlmostEqual(result["half_width"], expected)
        self.assertAlmostEqual(result["sum_squared_world_weights"], 1 / 60)
        self.assertAlmostEqual(hoeffding(0, [-1, 1], counts, 0.025)["half_width"], expected / 2)
        self.assertEqual(hoeffding(1, [-1, 1], {MAIN_FAMILIES[0]: 1}, 0.05)["interval"], [-1, 1])
        unequal = hoeffding(0, [-2, 2], {MAIN_FAMILIES[0]: 2, MAIN_FAMILIES[1]: 4}, 0.025)
        self.assertAlmostEqual(unequal["sum_squared_world_weights"], 3 / 16)
        self.assertAlmostEqual(unequal["world_weight_by_family"][MAIN_FAMILIES[0]], 1 / 4)

    def test_stratified_equal_weighting_and_constant_within_family(self):
        f, g = MAIN_FAMILIES[:2]
        rows = [dict(world_id="a", family=f, value=0)] + [
            dict(world_id=str(i), family=g, value=1) for i in range(3)]
        result = paired_interval(rows, [f, g], primary=True, limits=[-2, 2])
        self.assertEqual(result["estimate"], 0.5)  # Pooling would incorrectly give .75.
        self.assertEqual(result["interval"], [0.5, 0.5])
        self.assertTrue(result["degenerate"])
        self.assertEqual(result["hoeffding"]["alpha"], 0.025)
        self.assertEqual(result["draws"], 10_000)
        self.assertEqual(result["independent_worlds"], 4)

    def test_shared_world_draws_preserve_matched_endpoint_relation(self):
        f = MAIN_FAMILIES[0]
        rows = [dict(world_id=str(i), family=f, value=v) for i, v in enumerate((0, 0.25, 1))]
        cache = {}
        first = paired_interval(rows, [f], seed=37, cache=cache)
        inverse = paired_interval([dict(r, value=1-r["value"]) for r in rows], [f], seed=37, cache=cache)
        self.assertEqual(len(cache), 1)
        self.assertAlmostEqual(inverse["interval"][0], 1-first["interval"][1])
        self.assertAlmostEqual(inverse["interval"][1], 1-first["interval"][0])
        self.assertEqual(first, paired_interval(list(reversed(rows)), [f], seed=37))
        self.assertEqual(first["family_world_ids"], inverse["family_world_ids"])
        self.assertEqual(len(world_resamples(["a", "b"], 37)), DRAWS)
        self.assertTrue(all(len(draw) == 2 for draw in world_resamples(["a", "b"], 37)))

    def test_empty_missing_families_unknowns_and_duplicate_worlds_are_explicit(self):
        f, g = MAIN_FAMILIES[:2]
        for rows, families in (([], []), ([], [f]), ([dict(world_id="a", family=f, value=1)], [f, g]),
                                ([dict(world_id="a", family=f, value=None)], [f])):
            result = paired_interval(rows, families)
            self.assertIsNone(result["interval"])
            self.assertIsNone(result["hoeffding"])
        row = dict(world_id="a", family=f, value=1)
        with self.assertRaises(ValueError):
            paired_interval([row, row], [f])


class SharedMissingnessTests(unittest.TestCase):
    def test_shared_linear_cancellation_and_known_parent_constraint(self):
        row = contrast(component(["x"]), component(["x"], coefficient=-1))
        result = contrast_bounds(row)
        self.assertEqual(result["interval"], [0, 0])
        self.assertEqual(result["unknowns"], [])
        self.assertEqual(result["method"], "exact_shared_linear")
        row = contrast(component(["x", "y"]), component(["x"], coefficient=-1))
        self.assertEqual(contrast_bounds(row)["interval"], [-0.5, 0.5])
        self.assertEqual(contrast_bounds(row, {("correct", "x"): Fraction(0)})["interval"], [0, 0.5])

    def test_linear_bounds_match_independent_exhaustive_completions(self):
        row = contrast(component(["x", "y"], coefficient=0.5),
                       component(["x", "z"], coefficient=-1), component(["z"], coefficient=0.5))
        independent = [(x+y)/4 - (x+z)/2 + z/2 for x, y, z in product((0, 1), repeat=3)]
        self.assertEqual(contrast_bounds(row)["interval"], [min(independent), max(independent)])

    def test_nonlinear_feasible_shared_completions_and_exact_cancellation(self):
        # x OR y = x + y - xy. Independent endpoint bounds invent [-1,2].
        row = contrast(component(["x"], operator="all"), component(["y"], operator="all"),
                       component(["x", "y"], operator="all", coefficient=-1))
        independent = [x + y - x*y for x, y in product((0, 1), repeat=2)]
        result = contrast_bounds(row)
        self.assertEqual(result["interval"], [min(independent), max(independent)])
        self.assertEqual(result["method"], "exact_shared_binary_enumeration")
        equal = contrast(component(["x", "y"], operator="all"),
                         component(["y", "x"], operator="all", coefficient=-1))
        self.assertEqual(contrast_bounds(equal)["interval"], [0, 0])

    def test_known_failure_remains_zero_in_nonlinear_unknown_final(self):
        row = contrast(component(["failed", "unexecuted"], operator="all", values={"failed": 0}))
        self.assertEqual(contrast_bounds(row)["interval"], [0, 0])
        known = shared_values([dict(generation_id="failed", protocol_outcome="failed", correct=0),
            dict(generation_id="failed", protocol_outcome="unknown", correct=None)])
        self.assertEqual(known[("correct", "failed")], 0)
        with self.assertRaises(ValueError):
            shared_values([dict(generation_id="x", protocol_outcome="valid", correct=1),
                           dict(generation_id="x", protocol_outcome="valid", correct=0)])

    def test_large_nonlinear_envelope_retains_shared_variables_and_label(self):
        ids = [str(i) for i in range(13)]
        result = contrast_bounds(contrast(component(ids, operator="all")))
        self.assertEqual(result["interval"], [0, 1])
        self.assertEqual(len(result["unknowns"]), 13)
        self.assertEqual(result["method"], "conservative_shared_monomial_envelope")
        self.assertIn("attainable", result["limitation"])

    def test_unknown_eligibility_is_not_an_empty_or_fixed_denominator(self):
        row = contrast(component(["x"]), eligibility="unknown")
        self.assertEqual(contrast_bounds(row)["interval"], [0, 1])
        self.assertIn("undefined", contrast_bounds(row)["limitation"])
        self.assertIsNone(contrast_bounds(dict(row, eligibility="ineligible"))["interval"])


class ContrastUncertaintyTests(unittest.TestCase):
    def test_frozen_population_bounds_and_separate_complete_case_uncertainty(self):
        from recovery.analysis import analyze_estimands
        from tests.estimand_fixture import prepared, selection, tables, constant
        worlds, branches = selection(worlds=[w for w in prepared("fallback")[0].main if w.index in (3, 4)])
        matrices = {(w.world_id, "revision", "C", 0): constant([1]*4) for w in worlds}
        matrices[worlds[0].world_id, "revision", "B", 0] = constant([None]*4)
        data = tables(worlds, branches, matrices)
        estimates = analyze_estimands(worlds, branches, data)
        result = contrast_uncertainty(estimates, shared_values(data["outcomes"], data["peer_diagnostics"]))
        theta = next(r for r in result["summaries"] if r["estimand"] == "theta" and r["endpoint"] == "auc"
                     and r["level"] == "all_families")
        self.assertEqual(theta["sensitivity"]["interval"], [0.9, 1])
        self.assertEqual(theta["intended_population"]["independent_worlds"], 10)
        self.assertIsNone(theta["intended_population"]["interval"])
        self.assertEqual(theta["complete_case_description"]["independent_worlds"], 9)
        self.assertEqual(theta["complete_case_description"]["interval"], [1, 1])
        self.assertEqual(theta["paired_coverage"]["unknown_calls"], 16)
        self.assertEqual(theta["intended_population"]["probabilities"], [0.0125, 0.9875])

    def test_repeats_never_increase_independent_n_and_overlap_uses_saved_world_ids(self):
        from recovery.analysis import analyze_estimands
        from tests.estimand_fixture import prepared, selection, tables
        worlds, branches = selection(worlds=[w for w in prepared("fallback")[0].main if w.index == 1])
        data = tables(worlds, branches)
        estimates = analyze_estimands(worlds, branches, data)
        result = contrast_uncertainty(estimates, shared_values(data["outcomes"], data["peer_diagnostics"]))
        theta = next(r for r in result["summaries"] if r["estimand"] == "theta" and r["endpoint"] == "auc"
                     and r["level"] == "all_families")
        self.assertEqual(theta["intended_population"]["independent_worlds"], 5)
        self.assertEqual(sum(len(ids) for ids in theta["intended_population"]["family_world_ids"].values()), 5)
        self.assertTrue(estimates["repeat_contrasts"])
        sort = MAIN_FAMILIES[3]
        shared = [r["intended_population"]["family_world_ids"][sort] for r in result["summaries"]
                  if r["family"] == sort and r["population"] in ("main", "receipts", "prose_delay")]
        self.assertTrue(shared)
        self.assertTrue(all(ids == shared[0] for ids in shared))
        self.assertTrue(all(r["replicate"] == 0 for r in result["summaries"]))

    def test_power_references_are_the_prespecified_arithmetic(self):
        result = reporting_references()
        self.assertEqual(result["practical_difference"], 0.10)
        self.assertEqual([round(r["reference"], 3) for r in result["main"]], [0.139, 0.239, 0.170, 0.292])
        self.assertEqual([round(r["reference"], 3) for r in result["focal"]], [0.200, 0.343, 0.245, 0.420])
        self.assertAlmostEqual(result["fallback_standard_error_ratio"], math.sqrt(1.5))
        self.assertIn("not achieved power", result["interpretation"])


if __name__ == "__main__":
    unittest.main()
