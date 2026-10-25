"""Estimands, bootstrap conventions, degenerate and missing-outcome handling (spec 3.10)."""
import random
import unittest

from recovery.thesis.analysis import (LINEAR, Bootstrap, hoeffding, interval_indices, paired_categories,
                                      stratified_mean, subgroup_summary, summarize, value_range, world_value)
from recovery.thesis.checks import HAND_TABLE, check_analysis

HAND = [dict(ys) for ys in HAND_TABLE]


class Analysis(unittest.TestCase):
    def test_hand_scored_example(self):
        self.assertEqual(len(check_analysis()), 5)
        strata = list(range(8))
        self.assertEqual(stratified_mean([world_value(LINEAR["delta_H"][0], ys) for ys in HAND], strata), .125)
        self.assertEqual(stratified_mean([world_value(LINEAR["delta_E"][0], ys) for ys in HAND], strata), .4375)
        self.assertEqual(stratified_mean([world_value(LINEAR["theta"][0], ys) for ys in HAND], strata), .375)
        self.assertEqual(paired_categories(HAND, "RV", "CV"),
                         dict(both=1, only_first=1, only_second=2, neither=4, unknown=0))

    def test_decomposition_and_reopening_hand_values(self):
        strata = list(range(8))
        mean = lambda name: stratified_mean([world_value(LINEAR[name][0], ys) for ys in HAND], strata)  # noqa: E731
        self.assertEqual((mean("delta_announce"), mean("delta_answer"), mean("reopening")), (.125, .3125, .125))
        self.assertEqual(mean("delta_announce") + mean("delta_answer"), mean("delta_E"))
        self.assertEqual((mean("delta_announce_retain"), mean("delta_announce_clear")), (.25, 0))
        self.assertEqual((mean("delta_answer_retain"), mean("delta_answer_clear")), (.375, .25))
        self.assertEqual(mean("delta_H_preserving"), 0)
        for name in ("delta_announce", "delta_answer", "delta_H_preserving", "reopening"):
            self.assertEqual(value_range(LINEAR[name][0]), (-1, 1))

    def test_subgroup_summary_resamples_worlds_and_keeps_members(self):
        strata = [s for s in range(8) for _ in range(24)]
        rng = random.Random(4)
        values = [1.0 if rng.random() < .6 else 0.0 for _ in strata]
        members = [i % 2 == 0 for i in range(len(strata))]
        boot = Bootstrap(strata, 2000, 2026102302)
        result = subgroup_summary(values, members, boot, .95)
        expected = sum(v for v, m in zip(values, members) if m) / sum(members)
        self.assertEqual(result["n"], 96)
        self.assertAlmostEqual(result["estimate"], expected, places=6)
        self.assertLess(result["interval"][0], expected)
        self.assertGreater(result["interval"][1], expected)
        self.assertEqual(result["direction"], "positive")
        empty = subgroup_summary(values, [False] * len(strata), boot, .95)
        self.assertEqual((empty["n"], empty["estimate"], empty["interval"]), (0, None, None))
        rare = subgroup_summary(values, [i == 0 for i in range(len(strata))], boot, .95)
        self.assertIsNone(rare["interval"])  # some resamples contain no member

    def test_ranges_and_interval_indices(self):
        self.assertEqual(value_range(LINEAR["delta_H"][0]), (-1, 1))
        self.assertEqual(value_range(LINEAR["theta"][0]), (-2, 2))
        self.assertEqual(value_range(LINEAR["delta_E"][0]), (-1.0, 1.0))
        self.assertEqual(interval_indices(10000, .975), (125, 9874))
        self.assertEqual(interval_indices(10000, .95), (250, 9749))
        strata = [s for s in range(8) for _ in range(24)]
        self.assertAlmostEqual(hoeffding(strata, 2, .025), .2137, places=3)
        self.assertAlmostEqual(hoeffding([s for s in range(8) for _ in range(16)], 2, .025), .2617, places=3)

    def synthetic(self, effect, seed=1, n=24):
        rng = random.Random(seed)
        strata = [s for s in range(8) for _ in range(n)]
        table = []
        for _ in strata:
            base = rng.random() < .3
            table.append(dict(RV=int(base), CV=int(base or rng.random() < effect) if effect >= 0 else int(base and rng.random() > -effect),
                              RN=1, CN=1))
        return strata, table

    def test_signs_of_synthetic_effects(self):
        for effect, expected in ((.6, "positive"), (-.9, "negative"), (0, "inconclusive")):
            strata, table = self.synthetic(effect)
            boot = Bootstrap(strata, 2000, 2026102302)
            values = [world_value(LINEAR["delta_H"][0], ys) for ys in table]
            result = summarize(values, strata, boot, .975, (-1, 1))
            self.assertEqual(result["direction"], expected, (effect, result))

    def test_bootstrap_is_reproducible_and_stratified(self):
        strata = [s for s in range(8) for _ in range(3)]
        a, b = Bootstrap(strata, 50, 7), Bootstrap(strata, 50, 7)
        self.assertTrue((a.index == b.index).all())
        for row in a.index:
            for block, members in zip(range(8), a.blocks):
                start = sum(len(m) for m in a.blocks[:block])
                self.assertTrue(set(row[start:start + len(members)]) <= set(members))

    def test_degenerate_contrast_reports_hoeffding_and_no_claim(self):
        strata = [s for s in range(8) for _ in range(24)]
        boot = Bootstrap(strata, 500, 3)
        result = summarize([1.0] * len(strata), strata, boot, .975, (-1, 1))
        self.assertTrue(result["degenerate"])
        self.assertEqual(result["hoeffding"][1], 1.0)
        self.assertAlmostEqual(result["hoeffding"][0], 1 - 0.2137, places=3)
        self.assertEqual(result["direction"], "positive")  # both intervals exclude zero here
        zero = summarize([0.0] * len(strata), strata, boot, .975, (-1, 1))
        self.assertEqual(zero["direction"], "inconclusive")

    def test_missing_outcomes_are_bounded_by_coefficient_sign(self):
        table = [dict(t) for t in HAND]
        table[3]["CV"] = None
        strata = list(range(8))
        h = [stratified_mean([world_value(LINEAR["delta_H"][0], ys, f) for ys in table], strata) for f in ("min", "max")]
        e = [stratified_mean([world_value(LINEAR["delta_E"][0], ys, f) for ys in table], strata) for f in ("min", "max")]
        self.assertEqual(h, [.125, .25])
        self.assertEqual(e, [.375, .4375])
        self.assertIsNone(world_value(LINEAR["delta_H"][0], table[3]))


if __name__ == "__main__":
    unittest.main()
