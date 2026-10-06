"""Independent cost arithmetic and frozen coverage choice, with CPU records."""

import copy
from dataclasses import replace
import json
import unittest
from unittest.mock import patch

from recovery.costs import (boundary_selections, ledger_generation_costs,
    ledger_policy_costs, physical_costs, select_boundary_policy, _allocation_resources)
from recovery.tasks import Task
from recovery.truth import solve_world
from tests.cost_fixture import clock, fixture, set_boundary


class LedgerCostTests(unittest.TestCase):
    def test_shared_prefix_mixed_q_f_failure_retry_and_unknown_tokens(self):
        _, branches, records, _, attempts = fixture()
        generations = ledger_generation_costs(branches, records, attempts, clock(400))
        physical = physical_costs(generations, attempts, clock(400))
        self.assertEqual(len(generations), 116)
        self.assertEqual(len(attempts), 117)
        self.assertEqual(physical["attempt_seconds"], [235, 235])
        self.assertEqual(physical["request_tokens"], 234)
        self.assertEqual(physical["output_tokens"], 115)
        self.assertEqual(physical["unknown_output_attempts"], 2)
        policies = {r["policy"]: r for r in ledger_policy_costs(branches, records, generations)}
        for policy, expected in (("B", 67), ("C", 64), ("K", 64), ("F", 64), ("P_G", 67), ("Q_B", 67), ("Q_C", 64)):
            self.assertEqual(policies[policy]["seconds"], [expected, expected], policy)
            self.assertEqual(policies[policy]["logical_calls"], 32)
            self.assertEqual(policies[policy]["unknown_calls"], 0)
        self.assertEqual(policies["B"]["request_tokens"], 66)
        self.assertEqual(policies["P_G"]["request_tokens"], 66)
        self.assertEqual(policies["Q_B"]["uncertain_attempt_uses"], 1)
        self.assertEqual(policies["C"]["unknown_output_attempt_uses"], 1)

    def test_ambiguous_duration_retains_observation_and_upper_clock_bound(self):
        _, branches, records, _, attempts = fixture()
        lost = next(a for a in attempts if a["status"] == "interrupted")
        lost.update(elapsed_seconds=None, observed_seconds=1, finished_at=None, recovered_at=clock(303))
        generations = ledger_generation_costs(branches, records, attempts, clock(400))
        self.assertEqual(physical_costs(generations, attempts, clock(400))["attempt_seconds"], [233, 235])
        self.assertIsNone(lost["finished_at"])
        policies = {r["policy"]: r for r in ledger_policy_costs(branches, records, generations)}
        self.assertEqual(policies["Q_B"]["seconds"], [65, 67])

    def test_idle_allocation_setup_interruption_partition_and_billing_are_separate(self):
        _, _, _, _, attempts = fixture()
        allocations = [dict(worker=0, device="synthetic:0", started_at=clock(0), stopped_at=clock(400),
            stage="validation", stop_reason="fixture_complete", billing_json='{"billed_hours":1}')]
        processes = [dict(worker=0, started_at=clock(0), ready_at=clock(1), stopped_at=clock(400), recovered_at=None)]
        resources = _allocation_resources(allocations, attempts, processes, clock(400), None)
        self.assertEqual(resources["partition_seconds"], dict(setup=1, interruption=3, attempt=231, uncertain_work=0, idle=165))
        self.assertEqual(resources["allocated_gpu_hours"], 400 / 3600)
        self.assertEqual(resources["provider_billing"][0]["record"], {"billed_hours": 1})


class BoundaryRuleTests(unittest.TestCase):
    def test_all_covered_includes_bfs_deleted_edge_tombstone(self):
        w, b, _, i, _ = fixture(Task.BFS, ("B", "C", "K"))
        row = boundary_selections(w, b, i)[0]
        self.assertEqual(row["selected_policy"], "C")
        self.assertTrue(all(p["complete"] and len(p["tombstone_pairs"]) == 1 for p in row["coverage"]))

    def test_missing_pending_stale_and_mixed_coverage_select_k(self):
        manifest = [dict(record_id="a", version=2), dict(record_id="b", version=1)]
        complete = [dict(record_id="a", version=2, value=0), dict(record_id="b", version=1, value=1)]
        for missing in (complete[:1], [dict(record_id="a", version=2), complete[1]],
                        [dict(record_id="a", version=1, value=0), complete[1]]):
            row = select_boundary_policy(manifest, [complete, complete, missing, complete])
            self.assertEqual(row["selected_policy"], "K")
            self.assertFalse(row["coverage"][2]["complete"])

    def test_gold_candidates_and_derived_history_never_determine_choice(self):
        w, b, _, i, _ = fixture(Task.DIFFERENCE, ("B", "C", "K"))
        baseline = boundary_selections(w, b, i)
        edit = replace(w[0].main_edit, replacement=(w[0].main_edit.replacement + 1) % 31)
        if edit.replacement == next(r.value for r in w[0].world.records if r.record_id == edit.record_id):
            edit = replace(edit, replacement=(edit.replacement + 1) % 31)
        changed = replace(w[0], main_edit=edit)
        self.assertNotEqual(solve_world(w[0].event_world("revision")), solve_world(changed.event_world("revision")))
        for saved in i.values():
            state = json.loads(saved["requests"]["before"])
            for peer in state["peers"]:
                peer.update(candidate={"value": "wrong"}, history=["anything"], correct=False)
                for source in peer["sources"]:
                    source["value"] = 99999
            saved["requests"]["before"] = json.dumps(state)
        with patch("recovery.truth.solve_world", side_effect=AssertionError("gold consulted")):
            self.assertEqual(boundary_selections((changed,), b, i), baseline)

    def test_later_acquisitions_never_fill_missing_initial_boundary(self):
        w, b, _, i, _ = fixture(policies=("B", "C", "K"))
        for branch in b:
            i.pop((branch.branch_id, 1))
        self.assertIsNone(boundary_selections(w, b, i)[0]["selected_policy"])

    def test_mismatched_sibling_coverage_is_a_protocol_defect(self):
        w, b, _, i, _ = fixture(policies=("B", "C", "K"))
        C = next(branch for branch in b if branch.policy == "C")
        state = json.loads(i[C.branch_id, 1]["requests"]["before"])
        state["peers"][0]["sources"].pop()
        i[C.branch_id, 1]["requests"]["before"] = json.dumps(state)
        with self.assertRaisesRegex(ValueError, "coverage differs"):
            boundary_selections(w, b, i)

    def test_selected_policy_is_not_replaced_when_its_branch_is_unscheduled(self):
        w, b, _, i, _ = fixture(policies=("B",))
        row = boundary_selections(w, b, i)[0]
        self.assertEqual(row["selected_policy"], "C")
        self.assertIsNone(row["selected_branch_id"])
        self.assertIsNotNone(row["comparator_branch_ids"]["B"])

    def test_committed_pre_call_boundary_is_valid_later_checkpoint_is_not(self):
        w, b, _, i, _ = fixture(policies=("B", "C", "K"))
        C = next(branch for branch in b if branch.policy == "C")
        state = json.loads(i[C.branch_id, 1]["requests"]["before"])
        state.update(last_slot={"phase": "prefix", "round_number": 4}, committed=True)
        committed = {C.branch_id: dict(state=state, checkpoint_id="start")}
        self.assertEqual(boundary_selections(w, b, {}, committed=committed)[0]["selected_policy"], "C")
        state["last_slot"] = {"phase": "recovery", "round_number": 1}
        self.assertIsNone(boundary_selections(w, b, {}, committed=committed)[0]["selected_policy"])


if __name__ == "__main__":
    unittest.main()
