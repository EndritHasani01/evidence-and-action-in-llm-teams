"""Independent sign/order/missingness expectations for the frozen case rule."""

from fractions import Fraction
import unittest

from recovery.report import CASE_CONTRASTS, select_cases


def contrast(wid, value, key=CASE_CONTRASTS[0], replicate=0):
    exact = None if value is None else Fraction(value)
    return dict(world_id=wid, estimand=key[0], event=key[1], endpoint=key[2], round=key[3],
        replicate=replicate, eligibility="eligible", value=None if exact is None else float(exact),
        exact=None if exact is None else dict(numerator=exact.numerator, denominator=exact.denominator))


def outcomes(*ids, unknown=()):
    return [dict(world_id=wid, correct=None if wid in unknown else 0) for wid in ids]


def regression(wid, *, replicate=0, phase="continuation"):
    return dict(world_id=wid, regression=True, replicate=replicate, phase=phase)


class CaseSelectionTests(unittest.TestCase):
    def test_lower_observed_median_sorts_effect_before_id_for_both_signs(self):
        values = {"p4": 4, "p1": 1, "p3": 3, "p2": 2, "n4": -4, "n1": -1, "n3": -3, "n2": -2}
        selected = select_cases([contrast(k, v) for k, v in values.items()], outcomes(*values), [])
        self.assertEqual([r["world_id"] for r in selected["selected"]], ["n3", "p2"])
        self.assertEqual([r["sign_worlds"] for r in selected["signs"][:2]], [4, 4])

    def test_tied_effects_use_immutable_ids_and_are_order_independent(self):
        rows = [contrast(k, Fraction(1, 7)) for k in ("w4", "w2", "w1", "w3")]
        first = select_cases(rows, outcomes("w3", "w2", "w4", "w1"), [])
        self.assertEqual(first["selected"][0]["world_id"], "w2")
        self.assertEqual(first, select_cases(rows[::-1], outcomes("w1", "w2", "w3", "w4"), []))

    def test_tiny_nonzero_rational_is_not_rounded_to_a_zero_tie(self):
        rows = [contrast("small", Fraction(1, 10**400)), contrast("zero", 0)]
        actual = select_cases(rows, outcomes("small", "zero"), [])
        self.assertEqual(actual["selected"][0]["world_id"], "small")
        self.assertFalse(actual["all_zero"])

    def test_missing_signs_are_explicit_and_unknown_world_cannot_be_selected(self):
        rows = [contrast("known", 1), contrast("unexecuted", -1), contrast("unknown", None)]
        actual = select_cases(rows, outcomes("known", "unexecuted", "unknown", unknown=("unexecuted",)), [])
        self.assertEqual([r["world_id"] for r in actual["selected"]], ["known"])
        self.assertEqual(actual["signs"][1]["status"], "sign_absent")
        self.assertEqual(actual["signs"][1]["sign_worlds"], 0)

    def test_any_unexecuted_world_slot_blocks_card_without_treating_failure_as_missing(self):
        slots = outcomes("complete", "partial") + [dict(world_id="partial", correct=None)]
        actual = select_cases([contrast("complete", -1), contrast("partial", 1)], slots, [])
        self.assertEqual(actual["complete_world_ids"], ["complete"])
        self.assertEqual(actual["selected"][0]["world_id"], "complete")

    def test_duplicate_selections_merge_all_reasons_and_card_count_is_bounded(self):
        rows = [contrast(wid, value, key) for key in CASE_CONTRASTS for wid, value in (("a", 1), ("b", -1))]
        actual = select_cases(rows, outcomes("a", "b"), [])
        self.assertEqual(len(actual["selected"]), 2)
        self.assertTrue(all(len(r["reasons"]) == 3 for r in actual["selected"]))
        unique = [contrast(str(i), (-1)**i, key) for i, key in enumerate(CASE_CONTRASTS*2)]
        self.assertEqual(len(select_cases(unique, outcomes(*(str(i) for i in range(6))), [])["selected"]), 6)

    def test_all_zero_uses_smallest_regression_world_then_smallest_complete_world(self):
        rows = [contrast(wid, 0) for wid in ("a", "c", "b")]
        actual = select_cases(rows, outcomes("a", "b", "c"), [regression("c"), regression("b")])
        self.assertEqual(actual["fallback"], dict(world_id="b", reason="all_zero_regression"))
        no_regression = select_cases(rows, outcomes("a", "b", "c"), [regression("a", replicate=1)])
        self.assertEqual(no_regression["fallback"], dict(world_id="a", reason="all_zero_smallest_complete"))

    def test_zero_fallback_does_not_replace_an_existing_sign(self):
        rows = [contrast("zero", 0), contrast("positive", 1)]
        actual = select_cases(rows, outcomes("zero", "positive"), [regression("zero")])
        self.assertFalse(actual["all_zero"])
        self.assertIsNone(actual["fallback"])
        self.assertEqual(actual["selected"][0]["world_id"], "positive")

    def test_no_eligible_complete_cases_is_unavailable_not_a_zero_fallback(self):
        for rows, slots in (([], []), ([contrast("a", None)], outcomes("a")),
                            ([contrast("a", 0)], outcomes("a", unknown=("a",)))):
            with self.subTest(rows=rows):
                actual = select_cases(rows, slots, [])
                self.assertEqual(actual["status"], "unavailable")
                self.assertFalse(actual["all_zero"])
                self.assertFalse(actual["selected"])

    def test_repeats_never_replace_original_and_duplicate_contrasts_fail(self):
        actual = select_cases([contrast("a", -1), contrast("a", 1, replicate=1)], outcomes("a"), [])
        self.assertEqual(actual["selected"][0]["reasons"][0]["sign"], "negative")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            select_cases([contrast("a", 1)]*2, outcomes("a"), [])


if __name__ == "__main__":
    unittest.main()
