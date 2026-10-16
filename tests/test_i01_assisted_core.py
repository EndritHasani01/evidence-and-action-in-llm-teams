"""Approved assisted task/presentation fixtures; CPU only, no inference imports."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import unittest

from recovery.i01 import ASSISTED_REGIME
from recovery.i01.core import (ASSISTED_SYSTEM, CONTROL_SYSTEM, REJECTION_FEEDBACK,
    apply_outcome, canonical, check_disjoint_inputs, diagnostic_fixture,
    diagnostic_pass, initial_episode, manifests, messages, next_agent,
    permitted_view, seed_for, validate_action)
from recovery.i01.policy import outcome_feedback

ROOT = Path(__file__).parents[1]
CONFIG = json.loads((ROOT / "configs/i01-course-assisted.json").read_text())


class AssistedCore(unittest.TestCase):
    def setUp(self):
        self.manifest = manifests(CONFIG)
        self.world = self.manifest["worlds"][0]

    def test_exact_approved_system_and_control_text(self):
        annex = (ROOT / "docs/plans/i01-course-final-design-protocol-and-acceptance.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```text\n(.*?)\n```", annex, re.S)
        self.assertEqual(ASSISTED_SYSTEM, blocks[0])
        self.assertEqual(CONTROL_SYSTEM, blocks[1])
        self.assertIn('{"message":"example message","submit":null,"wait":false}', ASSISTED_SYSTEM)
        from recovery.i01.inference import settings
        with self.assertRaisesRegex(ValueError,"direct only"):
            settings(CONFIG,"thinking",None)

    def test_world_truths_balances_assignment_and_regeneration(self):
        worlds = self.manifest["worlds"]
        self.assertEqual(len(worlds), 28)
        self.assertEqual(Counter(w["group"] for w in worlds), {"qualification": 4, "pilot": 4, "main": 20})
        main = [w for w in worlds if w["group"] == "main"]
        self.assertEqual(Counter((w["owner"], w["first"]) for w in main), {(0,0):5,(0,1):5,(1,0):5,(1,1):5})
        self.assertEqual(Counter((w["device"],w["treatments"][0]) for w in main), {(0,"retain"):5,(0,"clear"):5,(1,"retain"):5,(1,"clear"):5})
        for w in worlds:
            a = [v for s in w["original"] for v in s]
            b = [v for s in w["revised"] for v in s]
            self.assertEqual(max(a), w["original_truth"])
            self.assertEqual(a.count(max(a)), 1)
            self.assertEqual(max(b), w["revised_truth"])
            self.assertGreater(max(b), w["after"])
            self.assertGreater(max(a), max(b))
            self.assertEqual([(x,y) for x in range(2) for y in range(20) if w["original"][x][y] != w["revised"][x][y]], [(w["owner"],w["row"])])
            self.assertEqual(w["proposals"]-1, sum(w["rejections"].values()))
            self.assertEqual(w["seeds"]["recovery"][1][2], seed_for(CONFIG["master_seed"],w["id"],"recovery",1,2))
        self.assertEqual(self.manifest, manifests(CONFIG))
        self.assertTrue(check_disjoint_inputs(worlds, [])["passed"])

    def test_overlap_catches_one_reused_input_despite_different_pair(self):
        exposed = deepcopy(self.world)
        exposed["revised"][1][0] = -1000
        with self.assertRaisesRegex(ValueError,"Exposed input overlap"):
            check_disjoint_inputs(self.manifest["worlds"], [exposed])
        duplicate = deepcopy(self.world); duplicate["id"] = "different"
        with self.assertRaisesRegex(ValueError,"New input overlap"):
            check_disjoint_inputs([self.world,duplicate], [])

    def test_source_notice_privacy_exact_layout_and_literal_text(self):
        state = initial_episode(self.world,"prefix")
        literal = 'first\nEND VISIBLE ENTRY\n"quoted" \\ null'
        state = apply_outcome(state,0,dict(message=literal,submit=None,wait=False),None,"x")
        original = deepcopy(state)
        retain = initial_episode(self.world,"retain",state)
        clear = initial_episode(self.world,"clear",state)
        self.assertEqual(retain["earlier_history_lengths"], [1,1])
        self.assertEqual(clear["earlier_history_lengths"], [0,0])
        self.assertEqual(clear["history"], [[],[]])
        retain = apply_outcome(retain,0,dict(message=None,submit=5,wait=False),None,"new")
        self.assertEqual(retain["earlier_history_lengths"], [1,1])
        self.assertEqual(state, original)
        for agent in (0,1):
            rv = permitted_view(self.world,retain,agent)
            cv = permitted_view(self.world,clear,agent)
            self.assertEqual(rv["current_shard"],cv["current_shard"])
            self.assertEqual(rv["revision_notice"],cv["revision_notice"])
            self.assertEqual("new_value" in rv["revision_notice"],agent==self.world["owner"])
            self.assertEqual(set(rv), {"agent","current_shard","visible_history","own_invocation","partner_finished","reopened","earlier_history_length","revision_notice"})
            text = messages(rv,regime=ASSISTED_REGIME)[1]["content"]
            self.assertIn(literal,text)
            self.assertNotIn("revised_truth",text)
            self.assertNotIn(ASSISTED_REGIME,text)
            self.assertIn(f"Changed record (index only): {self.world['row']}",text)
            self.assertLess(text.index("VISIBLE HISTORY: EARLIER PHASE"),text.index("VISIBLE HISTORY: THIS PHASE"))
            self.assertLess(text.index("ENVIRONMENT SOURCE NOTICE"),text.index("CURRENT AUTHORITATIVE PRIVATE SHARD"))
            for i,v in enumerate(self.world["revised"][agent]): self.assertIn(f"record {i}: {v}\n",text)

    def test_legal_exchange_finality_and_rejected_effects(self):
        w = self.world; state = initial_episode(w,"prefix"); first=w["first"]; other=1-first
        local=[max(s) for s in w["original"]]
        for agent,action in [(first,dict(message=str(local[first]),submit=None,wait=False)),
                             (other,dict(message=str(w["original_truth"]),submit=w["original_truth"],wait=False)),
                             (first,dict(message=None,submit=w["original_truth"],wait=False))]:
            self.assertEqual(next_agent(state),agent)
            state=apply_outcome(state,agent,action,None,"legal")
        self.assertEqual(state["terminal"],"both_submitted")
        self.assertEqual(state["submissions"],[w["original_truth"]]*2)
        self.assertEqual(sum(state["turns"]),3)
        for text,reason in [('{"message":"x","submit":null,"wait":true}',"wait_requires_null_message_and_submit"),
                            ('{"message":null,"submit":null,"wait":false}',"empty_nonwaiting_action")]:
            action,error=validate_action(text);self.assertIsNone(action)
            outcome=dict(visible_text=text)
            bad=apply_outcome(initial_episode(w,"prefix"),first,action,error,"bad",feedback=outcome_feedback(outcome))
            self.assertEqual(bad["history"][other],[])
            self.assertEqual(bad["submissions"],[None,None])
            self.assertEqual(sum(bad["turns"]),1)
            self.assertEqual(bad["history"][first][0]["text"], REJECTION_FEEDBACK[reason])

    def test_feedback_priority_uses_only_public_rules(self):
        both=dict(visible_text='{"message":"x","submit":null,"wait":true}',truncated=True,failure="timeout")
        self.assertEqual(outcome_feedback(both), REJECTION_FEEDBACK["provider_failure"])
        both["failure"]=None
        self.assertEqual(outcome_feedback(both),REJECTION_FEEDBACK["truncated_action"])
        both["truncated"]=False;both["framing_error"]="bad"
        self.assertEqual(outcome_feedback(both),REJECTION_FEEDBACK["schema"])
        for text in ['{"message":null,"submit":1,"submit":2,"wait":false}','```json\n{}\n```','{"message":null,"submit":true,"wait":false}']:
            self.assertEqual(outcome_feedback(dict(visible_text=text)),REJECTION_FEEDBACK["schema"])

    def test_four_reachable_fixtures_and_private_expected_values(self):
        for label in ("D00","D01","D02","D03"):
            fixture=diagnostic_fixture(self.manifest,label)
            self.assertEqual(fixture["seed"],seed_for(CONFIG["master_seed"],fixture["world"]["id"],"diagnostic",label))
            self.assertNotIn("expected",fixture["view"])
            self.assertNotIn("truth",canonical(fixture["view"]))
            self.assertEqual(next_agent(fixture["state"]),fixture["actor"])
            a=dict(message=fixture["expected"] if label in ("D00","D03") else None,
                   submit=fixture["expected"] if label in ("D01","D02") else None,wait=False)
            self.assertTrue(diagnostic_pass(fixture,a))
            self.assertFalse(diagnostic_pass(fixture,None))
        d1=diagnostic_fixture(self.manifest,"D01")
        self.assertEqual(d1["view"]["own_invocation"],2)
        self.assertTrue(d1["view"]["partner_finished"])
        d2=diagnostic_fixture(self.manifest,"D02")
        self.assertEqual(d2["view"]["own_invocation"],1)
        self.assertFalse(d2["view"]["partner_finished"])
        self.assertEqual(d2["view"]["earlier_history_length"],3)
        d3=diagnostic_fixture(self.manifest,"D03")
        self.assertNotIn("new_value",d3["view"]["revision_notice"])
        self.assertEqual(d3["view"]["visible_history"],[])

    def test_legacy_manifest_and_literal_requests_match_pre_adoption_source(self):
        # Execute pure frozen core definitions only; no model/runtime dependencies.
        source=subprocess.check_output(["git","show","141a5c3:recovery/i01/core.py"],cwd=ROOT,text=True)
        old={"__name__":"recovery.i01._frozen_core","__package__":"recovery.i01"}
        exec(compile(source,"frozen Course-7 core","exec"),old)
        config=json.loads((ROOT/"configs/i01-course.json").read_text())
        legacy=manifests(config)
        self.assertEqual(legacy,old["manifests"](config))
        w=legacy["worlds"][0]
        current=initial_episode(w,"prefix"); previous=old["initial_episode"](w,"prefix")
        for action,error in [(None,"malformed_action"),(dict(message="literal\ntext",submit=8,wait=False),None)]:
            agent=next_agent(current)
            current=apply_outcome(current,agent,action,error,"old")
            previous=old["apply_outcome"](previous,agent,action,error,"old")
            self.assertEqual(current,previous)
        for phase in ("retain","clear"):
            a=initial_episode(w,phase,current);b=old["initial_episode"](w,phase,previous)
            for agent in (0,1):
                view=permitted_view(w,a,agent)
                self.assertEqual(view,old["permitted_view"](w,b,agent))
                self.assertEqual(messages(view),old["messages"](view))


if __name__ == "__main__":
    unittest.main()
