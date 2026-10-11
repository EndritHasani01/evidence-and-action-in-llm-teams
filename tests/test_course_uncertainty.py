"""Independent course cluster arithmetic and shared-response sensitivity cases."""

from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import comb, log, sqrt
from random import Random
import unittest

from recovery.analysis import MAIN_FAMILIES, analyze_estimands
from recovery.costs import cost_records
from recovery.evaluate import evaluate_records
from recovery.tasks import Task
from recovery.uncertainty import (DRAWS, _duration_bounds, contrast_bounds, contrast_uncertainty,
    exact_binomial, hoeffding, paired_interval, policy_display_summaries, reporting_references,
    shared_values, trajectory_bounds, uncertainty_records)
from tests.cost_fixture import clock, fixture
from tests.estimand_fixture import constant, prepared, selection, tables
from tests.test_uncertainty import component, contrast


def quantile(samples, p):
    ordered = sorted(samples)
    index, remainder = divmod((len(samples) - 1) * p, 1)
    return (1 - remainder) * ordered[int(index)] + remainder * ordered[min(int(index) + 1, len(samples) - 1)]


def course_costs(policies=("B", "C", "K")):
    worlds, branches, records, inputs, attempts = fixture(Task.SORT, policies, size="course")
    return worlds, branches, records, inputs, attempts


def cost_tables(worlds, branches, records, inputs, attempts):
    data = evaluate_records(worlds, branches, records, inputs, attempts)
    data["costs"] = cost_records(worlds, branches, records, inputs, attempts, now=clock(400), tables=data)
    return data


class CourseStatisticalTests(unittest.TestCase):
    def test_four_world_family_bootstrap_matches_independent_saved_seed_draws_and_quantiles(self):
        population, _ = prepared("course")
        rows = [dict(world_id=w.world_id, family=w.world.task.value, value=(w.index - 1) / 4)
                for w in population.main]
        family_samples = []
        for i, family in enumerate(MAIN_FAMILIES):
            values = [r["value"] for r in sorted(rows, key=lambda r: r["world_id"]) if r["family"] == family]
            rng = Random(37 + i)
            family_samples.append([sum(values[rng.randrange(4)] for _ in range(4)) / 4 for _ in range(10_000)])
        samples = [sum(values) / 5 for values in zip(*family_samples)]
        for primary, endpoints in ((True, (.0125, .9875)), (False, (.025, .975))):
            actual = paired_interval(list(reversed(rows)), MAIN_FAMILIES, seed=37, primary=primary, limits=[-2, 2])
            self.assertEqual(actual["independent_worlds"], 20)
            self.assertEqual(actual["family_denominators"], dict.fromkeys(MAIN_FAMILIES, 4))
            self.assertEqual(actual["draws"], 10_000)
            self.assertEqual(actual["probabilities"], list(endpoints))
            self.assertEqual(actual["estimate"], .375)
            for value, p in zip(actual["interval"], endpoints):
                self.assertAlmostEqual(value, quantile(samples, p))
            self.assertEqual(actual, paired_interval(rows, MAIN_FAMILIES, seed=37, primary=primary, limits=[-2, 2]))

    def test_overlapping_eight_world_cohorts_reuse_family_draws_and_world_identities(self):
        population, _ = prepared("course")
        rows = [dict(world_id=w.world_id, family=w.world.task.value, value=w.index / 4) for w in population.main]
        cache = {}
        main = paired_interval(rows, MAIN_FAMILIES, seed=73, cache=cache)
        for cohort in ("receipts", "prose_delay", "preserving"):
            from recovery.analysis import population_table
            target = next(p for p in population_table(population.main) if p["population"] == cohort)
            subset = [r for r in rows if r["world_id"] in target["world_ids"]]
            focal = paired_interval(subset, target["families"], seed=73, cache=cache)
            self.assertEqual(focal["independent_worlds"], 8)
            for f in target["families"]:
                self.assertEqual(focal["family_world_ids"][f], main["family_world_ids"][f])
                self.assertEqual(focal["family_seeds"][f], main["family_seeds"][f])
            inverse = paired_interval([dict(r, value=1 - r["value"]) for r in subset], target["families"], seed=73, cache=cache)
            self.assertAlmostEqual(inverse["interval"][0], 1 - focal["interval"][1])
            self.assertAlmostEqual(inverse["interval"][1], 1 - focal["interval"][0])
        self.assertEqual(len(cache), 5)
        self.assertTrue(all(len(draws) == DRAWS and all(len(d) == 4 for d in draws) for draws in cache.values()))

    def test_course_degeneracy_has_weighted_bounded_companions_for_every_contrast_range(self):
        for counts, alpha, width in ((dict.fromkeys(MAIN_FAMILIES, 4), .025, 4),
                                     (dict.fromkeys(MAIN_FAMILIES, 4), .025, 2),
                                     (dict.fromkeys(MAIN_FAMILIES[:2], 4), .05, 4),
                                     (dict.fromkeys(MAIN_FAMILIES[:2], 4), .05, 2)):
            rows = [dict(world_id=f + str(i), family=f, value=.25) for f, n in counts.items() for i in range(n)]
            limits = [-width / 2, width / 2]
            actual = paired_interval(rows, list(counts), primary=alpha == .025, limits=limits)
            squares = sum(n * (1 / (len(counts) * n)) ** 2 for n in counts.values())
            half = width * sqrt(.5 * log(2 / alpha) * squares)
            self.assertEqual(actual["interval"], [.25, .25])
            self.assertTrue(actual["degenerate"])
            self.assertAlmostEqual(actual["hoeffding"]["half_width"], half)
            for value, expected in zip(actual["hoeffding"]["interval"], [max(limits[0], .25 - half), min(limits[1], .25 + half)]):
                self.assertAlmostEqual(value, expected)
            self.assertEqual(actual["hoeffding"]["world_weight_by_family"], {f: 1 / (len(counts) * n) for f, n in counts.items()})
        unequal = hoeffding(0, [-2, 2], {MAIN_FAMILIES[0]: 1, MAIN_FAMILIES[1]: 4}, .025)
        self.assertAlmostEqual(unequal["sum_squared_world_weights"], 5 / 16)

    def test_four_world_extreme_and_mixed_binomial_bounds_do_not_claim_certainty(self):
        self.assertEqual(exact_binomial(0, 0), None)
        self.assertEqual(exact_binomial(4, 4), [.025 ** .25, 1])
        self.assertEqual(exact_binomial(0, 4), [0, 1 - .025 ** .25])
        self.assertEqual(exact_binomial(1, 1), [.025, 1])
        lo, hi = exact_binomial(2, 4)
        self.assertAlmostEqual(sum(comb(4, k) * lo ** k * (1 - lo) ** (4 - k) for k in (2, 3, 4)), .025)
        self.assertAlmostEqual(sum(comb(4, k) * hi ** k * (1 - hi) ** (4 - k) for k in (0, 1, 2)), .025)

    def test_course_precision_references_are_exploratory_and_thesis_defaults_are_unchanged(self):
        course = reporting_references(regime="course")
        self.assertEqual([round(r["reference"], 3) for r in course["main"]], [.241, .413])
        self.assertEqual([round(r["reference"], 3) for r in course["focal"]], [.346, .594])
        self.assertEqual({r["N"] for r in course["main"]}, {20})
        self.assertEqual({r["N"] for r in course["focal"]}, {8})
        self.assertEqual(course["practical_difference"], .10)
        self.assertAlmostEqual(course["course_to_thesis_standard_error_ratio"], sqrt(3))
        for phrase in ("Exploratory", "four worlds per family", "not additional independent", "equivalence", "not achieved power"):
            self.assertIn(phrase, course["interpretation"])
        self.assertEqual(reporting_references(), reporting_references(regime="thesis"))
        self.assertEqual([r["N"] for r in reporting_references()["main"]], [60, 60, 40, 40])
        with self.assertRaises(ValueError): reporting_references(regime="unknown")


class CourseCohortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.population, cls.schedule = prepared("course")
        cls.data = tables(cls.population.main, cls.schedule.main)
        cls.result = uncertainty_records(cls.population.main, cls.schedule.main, cls.data, seed=37, regime="course")

    def test_primary_raw_worlds_and_family_counts_keep_the_declared_twenty_worlds(self):
        primaries = [r for r in self.result["summaries"] if r["primary_interval"]]
        self.assertEqual(len(primaries), 2)
        for row in primaries:
            self.assertEqual(row["scheduled_worlds"], 20)
            self.assertEqual(row["intended_population"]["independent_worlds"], 20)
            self.assertEqual(row["family_denominators"], dict.fromkeys(MAIN_FAMILIES, 4))
            self.assertEqual(row["intended_population"]["probabilities"], [.0125, .9875])
            self.assertEqual(row["intended_population"]["hoeffding"]["range"], [-2, 2] if row["estimand"] == "theta" else [-1, 1])
        estimates = analyze_estimands(self.population.main, self.schedule.main, self.data)
        for estimand in ("theta", "E_keep"):
            raw = [r for r in estimates["world_contrasts"] if r["estimand"] == estimand and r["replicate"] == 0 and r["endpoint"] in ("auc", "collaborator_accuracy") and (estimand != "E_keep" or r["event"] == "revision")]
            self.assertEqual(len(raw), 20)
            families = [r for r in self.result["summaries"] if r["estimand"] == estimand and r["endpoint"] in ("auc", "collaborator_accuracy") and r["level"] == "family" and (estimand != "E_keep" or r["event"] == "revision")]
            self.assertEqual(len(families), 5)
            self.assertTrue(all(r["intended_population"]["independent_worlds"] == 4 for r in families))
        self.assertIn("Exploratory", self.result["kind"])
        self.assertIn("four worlds per family", self.result["settings"]["limitation"])

    def test_receipt_prose_preserving_and_repeat_populations_have_fixed_shared_ids(self):
        populations = {r["population"]: r for r in self.result["populations"]}
        for cohort in ("receipts", "prose_delay", "preserving"):
            self.assertEqual(len(populations[cohort]["world_ids"]), 8)
            summaries = [r for r in self.result["summaries"] if r["population"] == cohort and r["level"] == "all_families" and r["endpoint"] != "preservation"]
            self.assertTrue(summaries)
            self.assertTrue(all(r["intended_population"]["independent_worlds"] == 8 for r in summaries))
            self.assertTrue(all(r["intended_population"]["probabilities"] == [.025, .975] for r in summaries))
        self.assertEqual(len(populations["repeat"]["world_ids"]), 5)
        repeated = [r for r in self.result["trajectory_summaries"] if r["replicate"]]
        self.assertTrue(repeated)
        self.assertTrue(all(r["population"] == "repeat" and r["scheduled_worlds"] == 5 for r in repeated))
        self.assertTrue(all(r["intended_population"]["independent_worlds"] == 5 for r in repeated))
        self.assertTrue(all(r["replicate"] == 0 for r in self.result["summaries"]))
        self.assertEqual(self.result["settings"]["population_estimates_use_replicate"], 0)

    def test_completion_extremes_use_each_eligible_family_and_repeats_remain_separate(self):
        for row in self.result["family_completion"]:
            n = 1 if row["replicate"] else 4
            self.assertEqual(row["scheduled_worlds"], n)
            self.assertEqual(row["executed_final_worlds"], n)
            successes = n if row["phase"] == "prefix" else 0
            self.assertEqual(row["successes"], successes)
            self.assertEqual(row["exact_binomial"], [.025 ** (1 / n), 1] if successes else [0, 1 - .025 ** (1 / n)])

    def test_one_unexecuted_world_keeps_intended_weights_and_separate_complete_cases(self):
        world = self.population.main[1]
        data = tables(self.population.main, self.schedule.main,
                      {(world.world_id, "revision", "B", 0): constant([None] * 4)})
        result = contrast_uncertainty(analyze_estimands(self.population.main, self.schedule.main, data), shared_values(data["outcomes"], data["peer_diagnostics"]), seed=37)
        theta = next(r for r in result["summaries"] if r["primary_interval"] and r["estimand"] == "theta")
        self.assertEqual(theta["sensitivity"]["interval"], [-1 / 20, 0])
        self.assertEqual(theta["family_denominators"], dict.fromkeys(MAIN_FAMILIES, 4))
        self.assertEqual(theta["intended_population"]["independent_worlds"], 20)
        self.assertIsNone(theta["intended_population"]["interval"])
        self.assertEqual(theta["complete_case_description"]["independent_worlds"], 19)
        self.assertEqual(theta["complete_case_description"]["interval"], [0, 0])
        self.assertEqual(theta["paired_coverage"]["unknown_calls"], 16)
        self.assertEqual(theta["paired_coverage"]["scheduled_calls"], 1280)
        self.assertIn("not the frozen-population", theta["complete_case_description"]["label"])


class CourseSharedMissingnessTests(unittest.TestCase):
    def test_absent_course_replay_uses_keep_execution_unknown_and_known_parent_constraints(self):
        worlds, branches, records, inputs, attempts = course_costs(("B", "C", "K", "P_G", "Q_B"))
        delayed = next(b for b in branches if b.policy == "Q_B")
        for call in delayed.calls[:4]: del records[call.call_id]
        data = cost_tables(worlds, branches, records, inputs, attempts)
        result = uncertainty_records(worlds, branches, data, regime="course")
        row = next(r for r in result["world_bounds"] if r["estimand"] == "Q_B-B" and r["endpoint"] == "accuracy" and r["round"] == 1)
        self.assertFalse(row["execution_observed"])
        self.assertEqual(row["sensitivity"]["interval"], [0, 0])
        summary = next(r for r in result["summaries"] if r["estimand"] == "Q_B-B" and r["endpoint"] == "accuracy" and r["round"] == 1 and r["level"] == "all_families")
        self.assertEqual(summary["paired_coverage"]["unknown_calls"], 4)
        self.assertEqual(summary["paired_coverage"]["unresolved_response_ids"], 0)
        self.assertIsNone(summary["intended_population"]["interval"])
        cost = next(r for r in result["policy_world_displays"] if r["display"] == "policy_Q_B")["metrics"]["policy_seconds"]
        self.assertFalse(cost["observed"])
        self.assertIsNone(cost["measured_interval"])
        self.assertEqual(cost["sensitivity"]["interval"], [67, 67])

    def test_course_response_linear_and_nonlinear_bounds_match_tiny_shared_enumeration(self):
        worlds, branches = selection(Task.SORT, 1, size="course")
        b = next(b for b in branches if b.policy == "B" and b.event == "revision" and b.replicate == 0)
        x, y, z = [c.generation_id for c in b.calls[:3]]
        linear = contrast(component([x, y]), component([x, z], coefficient=-1))
        nonlinear = contrast(component([x, y], operator="all"), component([x, z], operator="all", coefficient=-1))
        for row, values in ((linear, [(a + c) / 2 - (a + d) / 2 for a, c, d in product((0, 1), repeat=3)]),
                            (nonlinear, [a * c - a * d for a, c, d in product((0, 1), repeat=3)])):
            self.assertEqual(contrast_bounds(row)["interval"], [min(values), max(values)])
        self.assertEqual(contrast_bounds(nonlinear, {("correct", x): Fraction(0)})["interval"], [0, 0])
        self.assertEqual(contrast_bounds(contrast(component([x], values={x: 0})))["interval"], [0, 0])

    def test_course_stopped_trajectory_envelope_contains_every_tiny_completion(self):
        _, branches = selection(Task.BFS, 1, size="course")
        branch = next(b for b in branches if b.policy == "C" and b.event == "revision" and b.replicate == 0)
        rows = [dict(round=c.round_number, peer=c.peer, generation_id=c.generation_id,
                     correct=None if i < 9 else 1) for i, c in enumerate(branch.calls)]
        actual = trajectory_bounds(rows)
        self.assertEqual(actual["method"], "conservative_shared_trajectory_envelope")
        self.assertFalse(actual["execution_complete"])
        self.assertIn("no missing completion time", actual["limitation"])
        for bits in product((0, 1), repeat=9):
            matrix = [list(bits[:4]), list(bits[4:8]), [bits[8], 1, 1, 1], [1] * 4]
            joint = [int(all(r)) for r in matrix]
            reference = dict(final_joint=1, joint_ever=1, continuously_correct=int(all(joint)),
                never_jointly_correct=0, fragmented=0, all_individually_ever=1, individual_ever_mean=1,
                correct_at_end_after_delay_or_regression=int(not all(joint)), temporarily_correct_but_incorrect_at_end=0,
                regression=int(any(joint[i] and not joint[j] for i in range(4) for j in range(i + 1, 4))))
            for metric, value in reference.items():
                self.assertLessEqual(actual["metrics"][metric][0], value)
                self.assertGreaterEqual(actual["metrics"][metric][1], value)

    def test_empty_and_unknown_course_preservation_denominators_remain_explicit(self):
        worlds, branches = selection(Task.DIFFERENCE, 3, size="course")
        data = tables(worlds, branches)
        for row in data["peer_diagnostics"]:
            row.update(denominator=0, numerator=0, rate=None, eligible_coordinates=[], reason="no_correct_prefix_U_coordinates")
        result = uncertainty_records(worlds, branches, data, regime="course")
        rows = [r for r in result["summaries"] if r["endpoint"] == "preservation"]
        self.assertTrue(rows)
        self.assertTrue(all(r["eligible_worlds"] == 0 and r["sensitivity"]["interval"] is None for r in rows))
        missing = contrast(component([branches[0].calls[0].generation_id]), eligibility="unknown")
        bound = contrast_bounds(missing)
        self.assertEqual(bound["interval"], [0, 1])
        self.assertIn("undefined", bound["limitation"])

    def test_shared_course_prefix_and_first_round_costs_cancel_before_future_bounds(self):
        _, branches = selection(Task.SORT, 3, size="course")
        prefix = next(b for b in branches if b.phase == "prefix")
        b, q = [next(b for b in branches if b.policy == p and b.event == "revision") for p in ("B", "Q_B")]
        ids = lambda branch: [c.generation_id for c in branch.calls]
        generations = {c.generation_id: dict(seconds=[0, 0], protocol_outcome="unknown") for branch in branches for c in branch.calls}
        exact = _duration_bounds([(1, ids(prefix) + ids(q)[:4]), (-1, ids(prefix) + ids(b)[:4])], generations)
        self.assertEqual(exact["interval"], [0, 0])
        self.assertEqual(exact["unknown_response_ids"], [])
        full = _duration_bounds([(1, ids(prefix) + ids(q)), (-1, ids(prefix) + ids(b))], generations)
        self.assertEqual(full["interval"], [None, None])
        self.assertEqual(len(full["unknown_response_ids"]), 24)
        self.assertTrue(set(ids(prefix)).isdisjoint(full["unknown_response_ids"]))

    def test_course_policy_quality_and_preservation_cost_axes_keep_paired_eligible_cohorts(self):
        rows = []
        for f in MAIN_FAMILIES[:2]:
            for i in range(4):
                eligible, seconds = i != 3, 10 + i
                rows.append(dict(world_id=f + str(i), family=f, population="receipts", display="policy_C_delta", event="revision",
                    quality_cost_available=True, metrics={
                        "preservation": dict(value=1 if eligible else None, observed=eligible,
                            eligibility="eligible" if eligible else "ineligible", range=[0, 1],
                            measured_interval=[1, 1] if eligible else None, sensitivity=dict(interval=[1, 1] if eligible else None)),
                        "policy_seconds": dict(value=seconds, observed=True, eligibility="eligible", range=None,
                            measured_interval=[seconds, seconds], sensitivity=dict(interval=[seconds, seconds]))}))
        result = policy_display_summaries(rows, [dict(population="receipts", families=list(MAIN_FAMILIES[:2]))], seed=37)
        p = next(r for r in result if r["metric"] == "preservation" and r["level"] == "all_families")
        self.assertEqual(p["eligible_worlds"], 6)
        self.assertEqual(p["paired_cost"]["intended_population"]["lower"]["estimate"], 11)
        for scope in ("intended_population", "complete_case_description"):
            self.assertEqual(p[scope]["lower"]["family_world_ids"], p["paired_cost"][scope]["lower"]["family_world_ids"])
            self.assertEqual(p[scope]["lower"]["family_seeds"], p["paired_cost"][scope]["lower"]["family_seeds"])

    def test_incomplete_selected_course_policy_keeps_quality_and_cost_unknown_without_fallback(self):
        worlds, branches, records, inputs, attempts = course_costs()
        c = next(b for b in branches if b.policy == "C")
        for call in c.calls[4:]: del records[call.call_id]
        attempts = [a for a in attempts if a["call_id"] in records]
        data = cost_tables(worlds, branches, records, inputs, attempts)
        result = uncertainty_records(worlds, branches, data, regime="course")
        rule = next(r for r in result["policy_world_displays"] if r["display"] == "boundary_rule")
        self.assertEqual(rule["whole_branch_terms"], [dict(coefficient=1, branch_id=c.branch_id)])
        self.assertFalse(rule["quality_cost_available"])
        self.assertEqual(rule["metrics"]["auc"]["sensitivity"]["interval"], [.25, 1])
        self.assertIsNone(rule["metrics"]["policy_seconds"]["sensitivity"]["interval"][1])
        self.assertIsNone(rule["metrics"]["policy_seconds"]["value"])
        changed = deepcopy(data)
        changed["costs"]["boundary_selections"][0]["selected_policy"] = "B"
        with self.assertRaisesRegex(ValueError, "entire recorded C/K"):
            uncertainty_records(worlds, branches, changed, regime="course")


if __name__ == "__main__":
    unittest.main()
