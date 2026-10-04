import itertools
import json
import random
import unittest
from pathlib import Path

from pydantic import ValidationError
from reference.contracts import ActionDraft, AgentReply, Correction, ExperimentConfig, Expr, Event, validate_event_payload
from reference.support import (atom, AND, OR, NOT, Obs, antichain, labels,
                               exhaustive_labels, estimated_mask, exact_mask, survives)
from reference.budget import compute


class SupportTests(unittest.TestCase):
    def test_all_partial_observations_against_exhaustive_oracle(self):
        a, b, c, d = map(atom, "abcd")
        formulas = [AND(a, b), OR(a, b), AND(OR(a, b), OR(c, d)),
                    OR(AND(a, b), AND(c, d)), AND(a, OR(a, b)),
                    NOT(OR(a, b)), AND(NOT(a), b), OR(a, AND(b, c)),
                    Expr(op="const", constant=True), Expr(op="const", constant=False)]
        comparisons = 0
        for expr in formulas:
            for states in itertools.product((None, False, True), repeat=4):
                observed = {k: Obs(k + "@1", v) for k, v in zip("abcd", states) if v is not None}
                for wanted in (False, True):
                    self.assertEqual(labels(expr, wanted, observed), exhaustive_labels(expr, wanted, observed))
                    comparisons += 1
        self.assertEqual(comparisons, 1620)

    def test_random_monotone_formulas(self):
        rng = random.Random(113)
        def expr(depth):
            if depth == 0 or rng.random() < .25:
                return atom(rng.choice("abcde"))
            return rng.choice([AND, OR])(expr(depth-1), expr(depth-1))
        for _ in range(80):
            f = expr(3)
            for _ in range(4):
                observations = {a: Obs(a+"@1", bool(rng.randrange(2))) for a in "abcde" if rng.random() < .75}
                for wanted in (False, True):
                    self.assertEqual(labels(f, wanted, observations), exhaustive_labels(f, wanted, observations))

    def test_unknown_is_not_false(self):
        self.assertFalse(labels(atom("a"), False, {}))
        self.assertEqual(labels(atom("a"), False, {"a": Obs("a@1", False)}), frozenset({frozenset({"a@1"})}))

    def test_supersets_and_duplicates_not_alternatives(self):
        self.assertEqual(antichain([{"a"}, {"a", "b"}, {"a"}]), frozenset({frozenset({"a"})}))

    def test_correcting_one_and_premise_breaks_unique_proof(self):
        family = labels(AND(atom("a"), atom("b")), True, {"a": Obs("a@1", True), "b": Obs("b@1", True)})
        self.assertFalse(survives(family, {"a@2", "b@1"}))

    def test_alternative_preserves_claim_not_bound_action(self):
        x, y, p = map(atom, ["x", "y", "permit"])
        q = AND(p, OR(x, y))
        after = {"x": Obs("x@2", False), "y": Obs("y@1", True), "permit": Obs("p@1", True)}
        assertions = {"q": (q, True), "actX": (AND(p, x), True)}
        self.assertEqual(exact_mask(assertions, {n: after for n in assertions}), {"actX"})
        self.assertEqual(labels(q, True, after), frozenset({frozenset({"p@1", "y@1"})}))

    def test_negative_conclusion_requires_both_false_witnesses(self):
        f = OR(atom("x"), atom("y"))
        after = {"x": Obs("x@2", False), "y": Obs("y@1", False)}
        self.assertEqual(labels(f, False, after), frozenset({frozenset({"x@2", "y@1"})}))

    def test_same_root_copy_does_not_change_label(self):
        f = OR(atom("x"), atom("x"))
        self.assertEqual(labels(f, True, {"x": Obs("x@1", True)}), frozenset({frozenset({"x@1"})}))

    def test_mixed_polarity_rejected_not_given_wrong_label(self):
        with self.assertRaises(ValueError):
            labels(OR(atom("x"), NOT(atom("x"))), True, {})
        self.assertEqual(exhaustive_labels(OR(atom("x"), NOT(atom("x"))), True, {}), frozenset({frozenset()}))

    def test_estimated_policy_fallback_and_empty_proof(self):
        active = {"claim", "action", "other"}
        edges = [("x@1", "claim"), ("claim", "action")]
        est = {"claim": frozenset({frozenset({"y@1"})}), "action": None}
        self.assertEqual(estimated_mask(active, {"x@1"}, edges, est, {"x@2", "y@1"}), {"action"})
        est["action"] = frozenset({frozenset()})
        self.assertEqual(estimated_mask(active, {"x@1"}, edges, est, {"x@2", "y@1"}), {"action"})

    def test_no_event_has_empty_mask(self):
        self.assertEqual(estimated_mask({"c"}, set(), [("e", "c")], {}, {"e"}), set())


class ContractAndBudgetTests(unittest.TestCase):
    def test_invalid_action_shapes(self):
        with self.assertRaises(ValidationError):
            ActionDraft(job="target", verb="dispatch", value=True)
        with self.assertRaises(ValidationError):
            ActionDraft(job="target", verb="publish", value=True, resource="X")

    def test_extra_reply_field_rejected(self):
        with self.assertRaises(ValidationError):
            AgentReply(ack_epoch=0, expected_answer=True)
        with self.assertRaises(ValidationError):
            AgentReply.model_validate_json('{"ack_epoch":0,"claims":[{"slot":"q","value":"true"}]}', strict=True)
        event = Event(event_id="ev1", branch_id="b", seq=1, epoch=0,
                      logical_step=1, actor="A", kind="claim",
                      payload={"claim_id":"c1", "owner":"A", "slot":"eligible:X",
                               "value":"true", "created_epoch":0, "created_call_id":"call1"},
                      previous_sha256="0"*64, sha256="0"*64)
        with self.assertRaises(ValidationError):
            validate_event_payload(event)

    def test_bad_no_event_rejected(self):
        with self.assertRaises(ValidationError):
            Correction(correction_id="none", old_version_ids=(), replacements=(), from_epoch=0, to_epoch=1, kind="no_event", notice="none")

    def test_exact_matrix(self):
        cfg = ExperimentConfig.model_validate_json((Path(__file__).parents[1]/"configs/experiment.json").read_text())
        rows = compute(cfg)
        self.assertEqual(sum(x["total_calls"] for x in rows), 6400)
        self.assertEqual(sum(x["long_calls"] for x in rows), 480)
        self.assertEqual(sum(x["short_calls"] for x in rows), 5920)


if __name__ == "__main__":
    unittest.main()
