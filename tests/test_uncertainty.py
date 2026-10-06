"""Independent arithmetic and finite-completion checks for spec §6."""

from fractions import Fraction
from itertools import product
import math
import unittest

from recovery.analysis import MAIN_FAMILIES, _exact
from recovery.uncertainty import (DRAWS, contrast_bounds, contrast_uncertainty, exact_binomial, hoeffding,
    paired_interval, percentile, reporting_references, shared_values, trajectory_bounds,
    uncertainty_records, world_resamples, _duration_bounds, policy_display_summaries)


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

    def test_independent_finite_stratified_distribution_has_expected_percentiles(self):
        f, g = MAIN_FAMILIES[:2]
        rows = [dict(world_id="a", family=f, value=0), dict(world_id="b", family=f, value=1),
                dict(world_id="c", family=g, value=0.5)]
        # Exhaustive support: family f's mean is 0, .5 or 1; g is always .5.
        # Equal-family pooled values .25/.5/.75 have probabilities .25/.5/.25.
        result = paired_interval(rows, [f, g], seed=37, primary=True, limits=[0, 1])
        self.assertEqual(result["estimate"], 0.5)
        self.assertEqual(result["interval"], [0.25, 0.75])
        self.assertFalse(result["degenerate"])
        self.assertIsNone(result["hoeffding"])
        self.assertEqual(len(set(result["family_seeds"].values())), 2)


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
        shared = contrast(component(["x"]), component(["x"], coefficient=-1), eligibility="unknown")
        self.assertEqual(contrast_bounds(shared)["interval"], [0, 0])
        self.assertEqual(contrast_bounds(shared)["method"], "conditional_shared_endpoint_cancellation")
        self.assertIn("undefined", contrast_bounds(shared)["limitation"])
        first, second = component([]), component([], coefficient=-1)
        first["branch_id"], second["branch_id"] = "unavailable-B", "unavailable-C"
        self.assertEqual(contrast_bounds(contrast(first, second, eligibility="unknown"))["interval"], [-1, 1])


class ContrastUncertaintyTests(unittest.TestCase):
    def test_structurally_empty_preservation_population_is_na_end_to_end(self):
        from tests.estimand_fixture import prepared, selection, tables
        worlds, branches = selection(worlds=[w for w in prepared("fallback")[0].main if w.index == 3])
        data = tables(worlds, branches)
        for diagnostic in data["peer_diagnostics"]:
            diagnostic.update(denominator=0, numerator=0, rate=None, eligible_coordinates=[], reason="no_correct_prefix_U_coordinates")
        result = uncertainty_records(worlds, branches, data)
        preservation = [r for r in result["summaries"] if r["endpoint"] == "preservation"]
        self.assertTrue(preservation)
        self.assertTrue(all(r["eligible_worlds"] == 0 for r in preservation))
        self.assertTrue(all(r["sensitivity"]["interval"] is None for r in preservation))
        self.assertTrue(all(r["intended_population"]["interval"] is None for r in preservation))

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


def trajectory_rows(matrix, shared=None):
    shared = shared or {}
    return [dict(round=r+1, peer=p, generation_id=shared.get((r, p), f"r{r}/p{p}"), correct=v)
            for r, row in enumerate(matrix) for p, v in enumerate(row)]


class TrajectorySensitivityTests(unittest.TestCase):
    def test_fragmented_complete_trajectory_has_no_joint_completion(self):
        rows = trajectory_rows([[int(r != p) for p in range(4)] for r in range(4)])
        result = trajectory_bounds(rows)
        self.assertTrue(result["execution_complete"])
        self.assertEqual(result["metrics"]["fragmented"], [1, 1])
        self.assertEqual(result["metrics"]["joint_ever"], [0, 0])
        self.assertEqual(result["metrics"]["all_individually_ever"], [1, 1])
        self.assertEqual(result["metrics"]["never_jointly_correct"], [1, 1])

    def test_shared_unknown_first_and_final_cannot_create_infeasible_temporary_success(self):
        matrix = [[None, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [None, 1, 1, 1]]
        rows = trajectory_rows(matrix, {(0, 0): "x", (3, 0): "x"})
        result = trajectory_bounds(rows)
        self.assertFalse(result["execution_complete"])
        self.assertEqual(result["unknown_response_ids"], ["x"])
        self.assertEqual(result["metrics"]["temporarily_correct_but_incorrect_at_end"], [0, 0])
        self.assertEqual(result["metrics"]["final_joint"], [0, 1])
        self.assertEqual(result["metrics"]["regression"], [0, 1])
        constrained = trajectory_bounds(rows, {("correct", "x"): Fraction(1)})
        self.assertFalse(constrained["execution_complete"])
        self.assertEqual(constrained["metrics"]["final_joint"], [1, 1])
        self.assertEqual(constrained["metrics"]["regression"], [1, 1])

    def test_nonlinear_trajectory_bounds_match_independent_tiny_enumeration(self):
        matrix = [[1]*4, [None, 1, 1, 1], [0, 1, 1, 1], [None, 1, 1, 1]]
        result = trajectory_bounds(trajectory_rows(matrix))
        independent = []
        for x, y in product((0, 1), repeat=2):
            joint = [1, x, 0, y]
            independent.append(dict(final_joint=y, joint_ever=1,
                regression=int(any(joint[i] and not joint[j] for i in range(4) for j in range(i+1, 4))),
                temporarily_correct_but_incorrect_at_end=int(not y)))
        for metric in independent[0]:
            self.assertEqual(result["metrics"][metric], [min(r[metric] for r in independent), max(r[metric] for r in independent)])

    def test_large_incomplete_trajectory_has_conservative_labeled_marginals(self):
        result = trajectory_bounds(trajectory_rows([[None]*4 for _ in range(4)]))
        self.assertFalse(result["execution_complete"])
        self.assertEqual(len(result["unknown_response_ids"]), 16)
        self.assertEqual(result["method"], "conservative_shared_trajectory_envelope")
        self.assertTrue(all(interval == [0, 1] for interval in result["metrics"].values()))

    def test_conservative_trajectory_envelope_contains_every_independent_completion(self):
        matrix = [[None]*4, [None]*4, [None, 1, 1, 1], [1]*4]
        result = trajectory_bounds(trajectory_rows(matrix))
        self.assertEqual(result["method"], "conservative_shared_trajectory_envelope")
        independent = []
        for bits in product((0, 1), repeat=9):
            completed = [list(bits[:4]), list(bits[4:8]), [bits[8], 1, 1, 1], [1]*4]
            joint = [int(all(row)) for row in completed]
            ever = [any(row[p] for row in completed) for p in range(4)]
            category = "continuously_correct" if all(joint) else "correct_at_end_after_delay_or_regression"
            independent.append(dict(final_joint=joint[-1], joint_ever=int(any(joint)),
                all_individually_ever=int(all(ever)), individual_ever_mean=sum(ever)/4,
                fragmented=int(all(ever) and not any(joint)),
                regression=int(any(joint[i] and not joint[j] for i in range(4) for j in range(i+1, 4))),
                **{name:int(category == name) for name in result["metrics"] if name in (
                    "continuously_correct", "correct_at_end_after_delay_or_regression",
                    "temporarily_correct_but_incorrect_at_end", "never_jointly_correct")}))
        for metric, interval in result["metrics"].items():
            self.assertLessEqual(interval[0], min(r[metric] for r in independent))
            self.assertGreaterEqual(interval[1], max(r[metric] for r in independent))


class PolicyUncertaintyTests(unittest.TestCase):
    def test_costs_reject_changed_original_generation_and_selected_branch_ids(self):
        import copy
        from recovery.costs import cost_records
        from recovery.evaluate import evaluate_records
        from tests.cost_fixture import fixture, clock
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        data = evaluate_records(w, b, r, i, a)
        data["costs"] = cost_records(w, b, r, i, a, now=clock(400), tables=data)
        changed = copy.deepcopy(data)
        changed["costs"]["policy_costs"][0]["generation_ids"][0] = "wrong-original"
        with self.assertRaisesRegex(ValueError, "schedule identity"):
            uncertainty_records(w, b, changed)
        changed = copy.deepcopy(data)
        changed["costs"]["boundary_selections"][0]["selected_branch_id"] = next(branch.branch_id for branch in b if branch.policy == "B")
        with self.assertRaisesRegex(ValueError, "entire recorded C/K"):
            uncertainty_records(w, b, changed)

    def test_preservation_cost_axis_keeps_its_own_eligible_world_cohort(self):
        f = MAIN_FAMILIES[0]
        rows = []
        for wid, eligible, seconds in (("a", True, 10), ("b", False, 20)):
            rows.append(dict(world_id=wid, family=f, population="main", display="policy_C", event="revision",
                quality_cost_available=True, metrics={
                    "preservation": dict(value=1 if eligible else None, observed=eligible,
                        eligibility="eligible" if eligible else "ineligible", range=[0, 1],
                        measured_interval=[1, 1] if eligible else None, sensitivity=dict(interval=[1, 1] if eligible else None)),
                    "policy_seconds": dict(value=seconds, observed=True, eligibility="eligible", range=None,
                        measured_interval=[seconds, seconds], sensitivity=dict(interval=[seconds, seconds]))}))
        result = policy_display_summaries(rows, [dict(population="main", families=[f])])
        preservation = next(r for r in result if r["family"] == f and r["metric"] == "preservation")
        self.assertEqual(preservation["eligible_worlds"], 1)
        self.assertEqual(preservation["paired_cost"]["intended_population"]["interval"], [10, 10])
        self.assertEqual(preservation["paired_cost"]["intended_population"]["lower"]["family_world_ids"], {f: ["a"]})

    def test_shared_unknown_original_costs_cancel_before_unbounded_extrema(self):
        generations = {"prefix": dict(seconds=[1, 3], protocol_outcome="unknown"),
                       "C": dict(seconds=[2, 2], protocol_outcome="valid"),
                       "B": dict(seconds=[4, 4], protocol_outcome="valid")}
        self.assertEqual(_duration_bounds([(1, ["prefix", "C"]), (-1, ["prefix", "B"])], generations)["interval"], [-2, -2])
        self.assertEqual(_duration_bounds([(1, ["prefix", "C"])], generations)["interval"], [3, None])
        self.assertEqual(_duration_bounds([(-1, ["prefix", "B"])], generations)["interval"], [None, -5])

    def test_whole_policy_pairing_exact_costs_and_incomplete_selected_bounds(self):
        from recovery.costs import cost_records
        from recovery.evaluate import evaluate_records
        from tests.cost_fixture import fixture, clock
        worlds, branches, records, inputs, attempts = fixture(policies=("B", "C", "K"))
        data = evaluate_records(worlds, branches, records, inputs, attempts)
        data["costs"] = cost_records(worlds, branches, records, inputs, attempts, now=clock(400), tables=data)
        result = uncertainty_records(worlds, branches, data)
        display = next(r for r in result["policy_world_displays"] if r["display"] == "boundary_rule-always_B")
        self.assertEqual(display["metrics"]["policy_seconds"]["sensitivity"]["interval"], [-3, -3])
        q, cost = [next(r for r in result["policy_display_summaries"] if r["display"] == "boundary_rule-always_B"
                  and r["metric"] == metric and r["family"] == worlds[0].world.task.value) for metric in ("auc", "policy_seconds")]
        self.assertEqual(q["complete_case_description"]["lower"]["family_world_ids"], cost["complete_case_description"]["lower"]["family_world_ids"])
        self.assertEqual(cost["intended_population"]["interval"], [-3, -3])
        for r in result["policy_display_summaries"]:
            if r["paired_cost"]:
                self.assertEqual(r["complete_case_description"]["lower"]["family_world_ids"],
                    r["paired_cost"]["complete_case_description"]["lower"]["family_world_ids"])
        C = next(b for b in branches if b.policy == "C")
        for call in C.calls[4:]:
            del records[call.call_id]
        attempts = [a for a in attempts if a["call_id"] in records]
        data = evaluate_records(worlds, branches, records, inputs, attempts)
        data["costs"] = cost_records(worlds, branches, records, inputs, attempts, now=clock(400), tables=data)
        result = uncertainty_records(worlds, branches, data)
        selected = next(r for r in result["policy_world_displays"] if r["display"] == "boundary_rule")
        self.assertFalse(selected["quality_cost_available"])
        self.assertEqual(selected["whole_branch_terms"], [dict(coefficient=1, branch_id=C.branch_id)])
        self.assertEqual(selected["metrics"]["auc"]["sensitivity"]["interval"], [0.25, 1])
        self.assertIsNone(selected["metrics"]["policy_seconds"]["sensitivity"]["interval"][1])
        self.assertIsNone(selected["metrics"]["policy_seconds"]["value"])

    def test_preservation_sharing_uses_coordinate_rate_not_whole_candidate_credit(self):
        c = component(["shared"])
        c["endpoint"] = "preservation"
        c["atoms"][0].update(denominator=3, numerator=2, eligible_coordinates=[0, 1, 2], value=2/3)
        self.assertEqual(contrast_bounds(contrast(c))["exact"], [_exact(Fraction(2, 3))]*2)
        other = dict(c, coefficient=-1)
        c["atoms"][0].update(numerator=None, value=None)
        self.assertEqual(contrast_bounds(contrast(c, other))["interval"], [0, 0])


if __name__ == "__main__":
    unittest.main()
