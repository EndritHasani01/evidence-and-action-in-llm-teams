"""Thesis protocol: views, retention, notices, actions, scoring, funnel (spec 3.4-3.9, table A)."""
from copy import deepcopy
from pathlib import Path
import unittest

from recovery.i01.core import canonical, next_agent, validate_action
from recovery.i01.policy import outcome_action, outcome_feedback
from recovery.thesis import protocol
from recovery.thesis.checks import check_protocol, scripted_prefix
from recovery.thesis.worlds import load_manifest

ROOT = Path(__file__).parents[1]


def act(state, agent, message=None, submit=None, wait=False):
    return protocol.apply(state, agent, dict(message=message, submit=submit, wait=wait), None, f"c{len(state['events'])}")


class Protocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest, _ = load_manifest(ROOT)
        cls.worlds = {w["id"]: w for w in manifest["worlds"]}
        cls.world = cls.worlds["main-000"]

    def test_runtime_self_checks(self):
        self.assertEqual(len(check_protocol({"worlds": list(self.worlds.values())})), 7)

    def test_both_correct_scores_one_and_other_terminals_score_zero(self):
        w = self.world
        prefix = scripted_prefix(w)
        self.assertEqual(protocol.score(w, prefix), 1)
        state = protocol.start(w, "qwen", "RV", prefix)
        first, other = w["first"], 1 - w["first"]
        state = act(state, first, submit=w["revised_truth"])
        self.assertIsNone(protocol.score(w, state))  # not terminal: unknown
        state = act(state, other, message="waiting for you")
        state = act(state, other, submit=w["revised_truth"]) if next_agent(state) == other else state
        self.assertEqual(state["terminal"], "both_submitted")
        self.assertEqual(protocol.score(w, state), 1)
        wrong = protocol.start(w, "qwen", "RV", prefix)
        wrong = act(wrong, first, submit=w["original_truth"])
        wrong = act(wrong, other, submit=w["original_truth"])
        self.assertEqual(protocol.score(w, wrong), 0)
        funnel = protocol.funnel(w, wrong)
        self.assertTrue(funnel["wrong_agreement"])
        self.assertEqual(funnel["classes"], ["old_answer", "old_answer"])

    def test_prose_is_not_a_submission_and_horizon_ends_the_phase(self):
        w = self.world
        state = protocol.start(w, "qwen", "CV", scripted_prefix(w))
        for _ in range(6):
            agent = next_agent(state)
            if agent is None:
                break
            state = act(state, agent, message=f"{w['revised_truth']} is the global max. I will submit.")
        self.assertEqual(state["terminal"], "horizon_exhausted")
        self.assertEqual(state["submissions"], [None, None])
        self.assertEqual(protocol.score(w, state), 0)
        funnel = protocol.funnel(w, state)
        self.assertEqual(funnel["classes"], ["absent", "absent"])
        self.assertTrue(all(funnel["delivered_to_needer"].values()))

    def test_send_and_submit_finishes_and_later_messages_do_not_reopen(self):
        w = self.world
        state = protocol.start(w, "qwen", "RN", scripted_prefix(w))
        first, other = w["first"], 1 - w["first"]
        state = act(state, first, message="mine", submit=123)
        self.assertEqual(state["submissions"][first], 123)
        state = act(state, other, message="please change it")
        self.assertEqual(state["submissions"][first], 123)
        self.assertNotEqual(next_agent(state), first)
        state = act(state, other, wait=True)
        self.assertEqual(state["terminal"], "waiting_deadlock")

    def test_invalid_actions_consume_the_turn_deliver_nothing_and_give_feedback(self):
        w = self.world
        for text in ('```json\n{"message":null,"submit":1,"wait":false}\n```', '{"message":null,"submit":1,"wait":false,"x":1}',
                     '{"message":null,"submit":1,"submit":2,"wait":false}', '{"message":null,"submit":true,"wait":false}',
                     '{"message":"hi","submit":null,"wait":true}', '{"message":null,"submit":null,"wait":false} trailing'):
            outcome = dict(visible_text=text, truncated=False, failure=None, framing_error=None)
            action, error = outcome_action(outcome)
            self.assertIsNone(action, text)
            state = protocol.start(w, "qwen", "prefix")
            agent = next_agent(state)
            after = protocol.apply(state, agent, action, error, "x", outcome_feedback(outcome))
            self.assertEqual(after["turns"][agent], 1)
            self.assertEqual(after["history"][1 - agent], [])
            self.assertEqual(after["history"][agent][-1]["kind"], "feedback")
        truncated = dict(visible_text="x" * 10, truncated=True, failure=None, framing_error=None)
        self.assertEqual(outcome_action(truncated), (None, "truncated_action"))
        timeout = dict(visible_text="", truncated=False, failure="timeout", framing_error=None)
        self.assertEqual(outcome_feedback(timeout), "Call failed; no action was delivered.")

    def test_retain_and_clear_starts_and_no_change_reopening(self):
        w = self.world
        prefix = scripted_prefix(w)
        rv, rn = protocol.start(w, "qwen", "RV", prefix), protocol.start(w, "qwen", "RN", prefix)
        cv, cn = protocol.start(w, "qwen", "CV", prefix), protocol.start(w, "qwen", "CN", prefix)
        self.assertEqual(rv["history"], prefix["history"])
        self.assertEqual(rn["history"], prefix["history"])
        self.assertEqual(cv["history"], [[], []])
        self.assertEqual(cn["history"], [[], []])
        for state in (rv, rn, cv, cn):
            self.assertEqual(state["submissions"], [None, None])
            self.assertEqual(state["turns"], [0, 0])
            self.assertEqual(state["next"], w["first"])
        rn_text = protocol.messages(protocol.view(w, rn, 0))[1]["content"]
        self.assertIn(protocol.NOTICE_NONE, rn_text)
        self.assertIn("This phase: new phase after an earlier phase.", rn_text)
        self.assertIn("submit=" + str(w["original_truth"]), rn_text)  # old submission only as history
        # The prefix belongs to its world and model.
        with self.assertRaises(ValueError):
            protocol.start(w, "granite", "RV", prefix)
        with self.assertRaises(ValueError):
            protocol.start(self.worlds["main-001"], "qwen", "RV", prefix)

    def test_views_are_private_and_owner_only_replacement(self):
        w = self.world
        state = protocol.start(w, "qwen", "RV", scripted_prefix(w))
        owner, other = w["owner"], 1 - w["owner"]
        own = protocol.view(w, state, owner)
        non = protocol.view(w, state, other)
        self.assertEqual(own["notice"], dict(kind="change", owner=owner, record=w["row"], value=w["after"]))
        self.assertEqual(non["notice"], dict(kind="change", owner=owner, record=w["row"]))
        self.assertEqual(own["shard"], w["revised"][owner])
        self.assertEqual(non["shard"], w["original"][other])
        text = protocol.messages(non)[1]["content"]
        self.assertNotIn("Replacement value", text)
        self.assertIn(f"Changed record: agent {owner} record {w['row']}", text)
        self.assertIn(f"agent {other} record 19: {w['original'][other][19]}", text)

    def test_answer_preserving_cells(self):
        w = self.world
        prefix = scripted_prefix(w)
        owner, other = w["owner"], 1 - w["owner"]
        rp, cp = protocol.start(w, "qwen", "RP", prefix), protocol.start(w, "qwen", "CP", prefix)
        self.assertEqual(rp["history"], prefix["history"])
        self.assertEqual(cp["history"], [[], []])
        own, non = protocol.view(w, rp, owner), protocol.view(w, rp, other)
        self.assertEqual(own["notice"], dict(kind="change", owner=owner, record=w["preserving_row"],
                                             value=w["preserving_after"]))
        self.assertEqual(non["notice"], dict(kind="change", owner=owner, record=w["preserving_row"]))
        self.assertEqual(own["shard"], w["preserving"][owner])
        self.assertEqual(non["shard"], w["original"][other])
        text = protocol.messages(own)[1]["content"]
        self.assertIn(protocol.NOTICE_CHANGE + f"\nChanged record: agent {owner} record {w['preserving_row']}", text)
        self.assertIn(f"Replacement value for your record agent {owner} record {w['preserving_row']}: "
                      f"{w['preserving_after']}", text)
        # The answer is unchanged: resubmitting the original maximum succeeds.
        first, second = w["first"], 1 - w["first"]
        state = act(cp, first, submit=w["original_truth"])
        state = act(state, second, submit=w["original_truth"])
        self.assertEqual((state["terminal"], protocol.score(w, state)), ("both_submitted", 1))
        changed = act(act(rp, first, submit=w["runner_up"]), second, submit=w["runner_up"])
        self.assertEqual(protocol.score(w, changed), 0)
        self.assertNotIn("old_answer", protocol.funnel(w, changed)["classes"])  # the old answer is current here
        self.assertTrue(protocol.funnel(w, changed)["any_wrong"])

    def test_notices_differ_only_in_content_and_the_waiting_rule_is_stated(self):
        self.assertEqual(protocol.NOTICE_CHANGE.replace("one source record", "no source record"), protocol.NOTICE_NONE)
        self.assertIn("A finished partner cannot send messages, so waiting\nafter your partner has finished "
                      "ends the phase without your submission.", protocol.THESIS_SYSTEM)
        # The stated rule is the implemented one: waiting after the partner finished ends the phase.
        w = self.world
        state = protocol.start(w, "qwen", "CN", scripted_prefix(w))
        first, second = w["first"], 1 - w["first"]
        state = act(state, first, submit=w["original_truth"])
        state = act(state, second, wait=True)
        self.assertEqual((state["terminal"], state["submissions"][second]), ("waiting_deadlock", None))

    def test_repetition_diagnostic_counts_exact_own_repeats(self):
        w = self.world
        prefix = scripted_prefix(w)
        first, second = w["first"], 1 - w["first"]
        earlier = next(e["action"]["message"] for e in prefix["history"][first]
                       if e["kind"] == "own_action" and e["action"]["message"])
        state = protocol.start(w, "qwen", "RV", prefix)
        state = act(state, first, message=earlier)  # copies its own earlier-phase message
        state = act(state, second, message="hello")
        state = act(state, first, message="new text")
        state = act(state, second, message="hello")  # repeats within this phase
        state = act(state, first, submit=1)
        state = act(state, second, submit=1)
        funnel = protocol.funnel(w, state)
        self.assertEqual(funnel["repeats_earlier_phase"][first], True)
        self.assertEqual(funnel["repeats_earlier_phase"][second], False)
        self.assertEqual(funnel["repeats"], [True, True])
        clear = protocol.start(w, "qwen", "CV", prefix)
        clear = act(act(clear, first, message=earlier), second, submit=1)
        clear = act(clear, first, submit=1)
        self.assertEqual(protocol.funnel(w, clear)["repeats"], [False, False])

    def test_controls_render_the_complete_input(self):
        w = self.world
        msgs = protocol.messages(protocol.control_view(w, "revised"), control=True)
        self.assertEqual(msgs[0]["content"], protocol.CONTROL_SYSTEM)
        self.assertEqual(msgs[1]["content"], "Complete input: " + str(w["revised"][0] + w["revised"][1]))
        action, _ = validate_action('{"message":null,"submit":5,"wait":false}', control=True)
        self.assertEqual(action["submit"], 5)

    def test_information_witness(self):
        base = deepcopy(self.worlds["dev-00"])
        prefix = scripted_prefix(base)
        other = 1 - base["owner"]
        demote, keep = deepcopy(base), deepcopy(base)
        demote["revised"][base["owner"]][base["row"]] = base["runner_up"] - 1
        keep["revised"][base["owner"]][base["row"]] = base["runner_up"] + 1
        demote["after"], keep["after"] = base["runner_up"] - 1, base["runner_up"] + 1
        views = [canonical(protocol.view(w, protocol.start(w, "qwen", "CV", prefix), other)) for w in (demote, keep)]
        self.assertEqual(views[0], views[1])


if __name__ == "__main__":
    unittest.main()
