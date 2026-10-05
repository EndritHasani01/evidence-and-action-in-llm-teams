"""Hand-calculated exact, coordinate and trajectory fixtures for spec §7.1."""

import unittest

from recovery.evaluate import (identical_wrong_agreement, score_candidate,
                               score_coordinates, trajectory)
from recovery.tasks import Size, Task
from recovery.truth import Truth


def metric(rows, name):
    return next(r for r in rows if r["metric"] == name)


class ExactOutcomeTests(unittest.TestCase):
    def test_order_and_duplicate_multiplicity(self):
        gold = Truth(Task.TOP_K, Size.TARGET, (9, 9, 8, 8, 7, 7, 6, 6, 5, 5))
        for peer in range(4):
            self.assertEqual(score_candidate(gold, "valid", gold.candidate(peer), peer), 1)
            wrong = [9, 8, 7, 6, 5] * 2
            self.assertEqual(score_candidate(gold, "valid", wrong, peer), 0)
            self.assertEqual(score_candidate(gold, "valid", list(reversed(gold.values)), peer), 0)
            for status, expected in (("invalid", 0), ("failed", 0), ("unknown", None)):
                self.assertEqual(score_candidate(gold, status, gold.candidate(peer), peer), expected)
        with self.assertRaises(ValueError):
            score_candidate(gold, "valid", [True] * 10, 0)

    def test_bfs_full_dictionary_and_unreachable_node(self):
        gold = Truth(Task.BFS, Size.FALLBACK, (0, 1, 2, 3, 4, 5, 6, -1))
        answer = dict(reversed(list(gold.candidate().items())))
        self.assertEqual(score_candidate(gold, "valid", answer, 2), 1)
        answer["7"] = 7
        self.assertEqual(score_candidate(gold, "valid", answer, 2), 0)
        del answer["7"]
        with self.assertRaises(ValueError):
            score_candidate(gold, "valid", answer, 2)

    def test_segment_assignments_and_full_information_control(self):
        for task in (Task.PREFIX, Task.SORT):
            gold = Truth(task, Size.TARGET, tuple(range(32)))
            for peer in range(4):
                self.assertEqual(score_candidate(gold, "valid", list(range(8 * peer, 8 * peer + 8)), peer), 1)
            self.assertEqual(score_candidate(gold, "valid", list(range(32)), None), 1)


class CoordinateOutcomeTests(unittest.TestCase):
    def setUp(self):
        self.old = Truth(Task.DIFFERENCE, Size.FALLBACK, tuple(range(1, 24)))
        self.new = Truth(Task.DIFFERENCE, Size.FALLBACK, (101, 102, *range(3, 24)))

    def test_repair_old_errors_and_collateral_damage_are_distinct(self):
        old_answer = self.old.candidate(0)
        old_answer[3] = -4  # Coordinate 4 was an old U error, eligible for repair only.
        answer = self.new.candidate(0)
        answer[0] = 1  # Coordinate 1 explicitly persists at old gold.
        answer[2] = -3  # Coordinate 3 was old-correct U, now collateral damage.
        coordinates, rates = score_coordinates(self.old, self.new, 0, "valid", answer, "valid", old_answer)
        self.assertEqual(coordinates[0]["coordinate"], 1)
        self.assertEqual([r["set"] for r in coordinates[:3]], ["D", "D", "U"])
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 1 / 2)
        self.assertEqual(metric(rates, "old_value_persistence")["rate"], 1 / 2)
        self.assertEqual(metric(rates, "preservation")["denominator"], 20)
        self.assertEqual(metric(rates, "preservation")["rate"], 19 / 20)
        self.assertEqual(metric(rates, "collateral_damage")["rate"], 1 / 20)
        self.assertEqual(metric(rates, "old_error_repair")["rate"], 1)
        self.assertTrue(coordinates[3]["old_error_eligible"])
        self.assertFalse(coordinates[3]["preservation_eligible"])
        self.assertTrue(coordinates[3]["changed_from_prefix"])

    def test_invalid_current_is_incorrect_and_explicitly_malformed(self):
        coordinates, rates = score_coordinates(self.old, self.new, 0, "invalid", self.old.candidate(),
                                                "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 0)
        self.assertEqual(metric(rates, "old_value_persistence")["rate"], 0)
        self.assertEqual(metric(rates, "changed_malformed_or_missing")["rate"], 1)
        self.assertEqual(metric(rates, "preservation")["rate"], 0)
        self.assertEqual(metric(rates, "collateral_damage")["rate"], 1)
        self.assertTrue(all(r["value"] is None for r in coordinates))

    def test_final_invalid_prefix_never_backfills_an_earlier_answer(self):
        for prefix_status in ("invalid", "failed"):
            _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(),
                                        prefix_status, self.old.candidate())
            for name in ("preservation", "collateral_damage", "old_error_repair"):
                row = metric(rates, name)
                self.assertEqual(row["denominator"], 0)
                self.assertIsNone(row["rate"])
                self.assertEqual(row["reason"], "prefix_round_four_not_protocol_valid")

    def test_empty_D_empty_U_and_no_eligible_old_correct_coordinate(self):
        _, rates = score_coordinates(self.old, self.old, 0, "valid", self.old.candidate(),
                                    "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["reason"], "no_changed_coordinates")
        self.assertIsNone(metric(rates, "old_value_persistence")["rate"])
        self.assertEqual(metric(rates, "preservation")["rate"], 1)
        all_changed = Truth(self.old.task, self.old.size, tuple(v + 1 for v in self.old.values))
        _, rates = score_coordinates(self.old, all_changed, 0, "valid", all_changed.candidate(),
                                    "valid", self.old.candidate())
        self.assertEqual(metric(rates, "preservation")["reason"], "no_unchanged_coordinates")
        _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(),
                                    "valid", [-999] * 23)
        self.assertEqual(metric(rates, "preservation")["reason"], "no_correct_prefix_U_coordinates")
        self.assertEqual(metric(rates, "old_error_repair")["denominator"], 21)

    def test_unknown_slot_and_unknown_prefix_eligibility(self):
        _, rates = score_coordinates(self.old, self.new, 0, "unknown", None, "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["denominator"], 2)
        self.assertIsNone(metric(rates, "changed_accuracy")["numerator"])
        self.assertEqual(metric(rates, "preservation")["denominator"], 21)
        self.assertIsNone(metric(rates, "preservation")["rate"])
        _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(), "unknown", None)
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 1)
        self.assertIsNone(metric(rates, "preservation")["denominator"])
        self.assertEqual(metric(rates, "preservation")["reason"], "prefix_round_four_unknown")

    def test_unique_global_coordinates_for_segments(self):
        old = Truth(Task.PREFIX, Size.TARGET, tuple(range(32)))
        new = Truth(Task.PREFIX, Size.TARGET, (*range(16), *range(116, 132)))
        for peer in range(4):
            coordinates, rates = score_coordinates(old, new, peer, "valid", new.candidate(peer),
                                                    "valid", old.candidate(peer))
            self.assertEqual([r["coordinate"] for r in coordinates], list(range(peer * 8, peer * 8 + 8)))
            self.assertEqual(metric(rates, "changed_accuracy")["denominator"], 0 if peer < 2 else 8)


class TrajectoryTests(unittest.TestCase):
    def test_four_complete_categories_times_auc_and_regression(self):
        examples = [
            ([1, 1, 1, 1], "continuously_correct", 1, 1, False, 1),
            ([0, 0, 1, 1], "correct_at_end_after_delay_or_regression", 3, 3, False, 1 / 2),
            ([1, 0, 0, 1], "correct_at_end_after_delay_or_regression", 1, 4, True, 1 / 2),
            ([0, 1, 0, 0], "temporarily_correct_but_incorrect_at_end", 2, None, True, 1 / 4),
            ([0, 0, 0, 0], "never_jointly_correct", None, None, False, 0),
        ]
        for rounds, category, first, stable, regression, auc in examples:
            with self.subTest(rounds=rounds):
                result = trajectory([[c] * 4 for c in rounds])
                self.assertEqual(result["category"], category)
                self.assertEqual(result["first_joint_round"], first)
                self.assertEqual(result["first_stable_joint_round"], stable)
                self.assertEqual(result["regression"], regression)
                self.assertEqual(result["auc"], auc)
                self.assertEqual(result["final_joint"], rounds[-1])

    def test_fragmentation_does_not_splice_best_answers(self):
        result = trajectory([[int(peer == r) for peer in range(4)] for r in range(4)])
        self.assertEqual(result["individual_ever"], [True] * 4)
        self.assertFalse(result["joint_ever"])
        self.assertTrue(result["fragmented"])
        self.assertEqual(result["auc"], 1 / 4)
        self.assertEqual(result["final_joint"], 0)
        self.assertIsNone(result["first_joint_round"])

    def test_incomplete_is_separate_from_never_correct(self):
        result = trajectory([[None] * 4] * 4)
        self.assertEqual(result["category"], "incomplete")
        for name in ("auc", "final_joint", "first_joint_round", "first_stable_joint_round", "fragmented", "regression"):
            self.assertIsNone(result[name])
        result = trajectory([[1] * 4, [0] * 4, [None] * 4, [1] * 4])
        self.assertEqual(result["observed_first_joint_round"], 1)
        self.assertTrue(result["regression"])
        self.assertIsNone(result["first_stable_joint_round"])
        self.assertEqual(result["category"], "incomplete")

    def test_identical_wrong_only_for_replicated_outputs(self):
        outcomes = [{"protocol_outcome": "valid", "correct": 0, "candidate": [4] * 10}] * 4
        for task in (Task.TOP_K, Task.DIFFERENCE, Task.BFS):
            self.assertTrue(identical_wrong_agreement(task, outcomes))
        for task in (Task.PREFIX, Task.SORT):
            self.assertIsNone(identical_wrong_agreement(task, outcomes))
        self.assertFalse(identical_wrong_agreement(Task.TOP_K, [*outcomes[:3], dict(outcomes[3], protocol_outcome="invalid")]))
        self.assertIsNone(identical_wrong_agreement(Task.TOP_K, [*outcomes[:3], dict(outcomes[3], protocol_outcome="unknown")]))


if __name__ == "__main__":
    unittest.main()
