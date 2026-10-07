"""Independent cost arithmetic and frozen coverage choice, with CPU records."""

import copy
from dataclasses import replace
import json
import unittest
from unittest.mock import patch

from recovery.costs import (boundary_selections, ledger_generation_costs,
    ledger_policy_costs, physical_costs, select_boundary_policy, _allocation_resources, cost_records)
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


class WholePolicyTests(unittest.TestCase):
    def test_selected_complete_branch_cost_quality_preservation_and_denominators_match(self):
        w, b, r, i, a = fixture()
        tables = cost_records(w, b, r, i, a, now=clock(400))
        selection = tables["boundary_selections"][0]
        self.assertEqual(selection["selected_policy"], "C")
        self.assertTrue(selection["available"])
        selected = next(row for row in tables["strategy_worlds"] if row["strategy"] == "boundary_rule")
        always = next(row for row in tables["strategy_worlds"] if row["strategy"] == "always_C")
        for key in ("auc", "final_joint", "preservation", "complete_policy_seconds", "branch_id", "call_ids", "generation_ids"):
            self.assertEqual(selected[key], always[key], key)
        self.assertEqual(selected["auc"], 15 / 16)
        self.assertEqual(selected["final_joint"], 1)
        self.assertEqual(selected["preservation"]["rate"], 1)
        self.assertGreater(selected["preservation"]["peer_copy_count"], 0)
        self.assertEqual(len(selected["call_ids"]), 32)
        self.assertEqual(tables["physical"]["attempt_seconds"], [235, 235])
        self.assertIsNone(next(c for c in tables["policy_costs"] if c["policy"] == "C")["complete_output_tokens"])

    def test_k_choice_uses_k_whole_cost_despite_better_c_outcomes(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        sources = json.loads(i[next(branch.branch_id for branch in b if branch.policy == "B"), 1]["requests"]["before"])["peers"][0]["sources"]
        set_boundary(i, b, [sources, sources[:-1], sources, sources])
        tables = cost_records(w, b, r, i, a, now=clock(400))
        chosen = next(row for row in tables["strategy_worlds"] if row["strategy"] == "boundary_rule")
        self.assertEqual(chosen["selected_policy"], "K")
        self.assertEqual(chosen["branch_id"], next(branch.branch_id for branch in b if branch.policy == "K"))
        self.assertEqual(chosen["complete_policy_seconds"], [64, 64])
        self.assertEqual(chosen["auc"], 1)

    def test_unavailable_selected_c_does_not_fall_back_to_completed_k(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        C = next(branch for branch in b if branch.policy == "C")
        for call in C.calls[4:]:
            del r[call.call_id]
        a = [attempt for attempt in a if attempt["call_id"] in r]
        tables = cost_records(w, b, r, i, a, now=clock(400))
        chosen = tables["boundary_selections"][0]
        self.assertEqual(chosen["selected_policy"], "C")
        self.assertFalse(chosen["available"])
        row = next(row for row in tables["strategy_worlds"] if row["strategy"] == "boundary_rule")
        self.assertIsNone(row["auc"])
        self.assertIsNone(row["complete_policy_seconds"])
        self.assertEqual(row["reason"], "branch_or_prefix_incomplete")
        self.assertTrue(next(row for row in tables["strategy_worlds"] if row["strategy"] == "always_K")["available"])
        self.assertTrue(all(not row["paired_available"] for row in tables["paired_comparisons"]))

    def test_incomplete_prefix_blocks_full_policy_cost_without_erasing_recorded_quality(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        prefix_call = next(branch for branch in b if branch.phase == "prefix").calls[0]
        del r[prefix_call.call_id]
        a = [attempt for attempt in a if attempt["call_id"] in r]
        tables = cost_records(w, b, r, i, a, now=clock(400))
        C = next(row for row in tables["policy_costs"] if row["policy"] == "C")
        self.assertEqual(C["unknown_calls"], 1)
        self.assertIsNone(C["complete_policy_seconds"])
        self.assertFalse(tables["boundary_selections"][0]["available"])
        self.assertEqual(next(row for row in tables["quality_preservation"] if row["policy"] == "C")["auc"], 15 / 16)

    def test_unrecorded_replay_does_not_become_completed_just_because_parent_exists(self):
        w, b, r, i, a = fixture()
        Q = next(branch for branch in b if branch.policy == "Q_B")
        del r[Q.calls[0].call_id]
        tables = cost_records(w, b, r, i, a, now=clock(400))
        cost = next(row for row in tables["policy_costs"] if row["policy"] == "Q_B")
        self.assertEqual(cost["seconds"], [67, 67])
        self.assertEqual(cost["unknown_calls"], 1)
        self.assertIsNone(cost["complete_policy_seconds"])

    def test_constant_rule_is_explicit_and_unknown_boundaries_keep_population_denominator(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        result = cost_records(w, b, r, i, a, now=clock(400))
        frequency = next(row for row in result["selection_frequencies"] if row["level"] == "pooled")
        self.assertEqual(frequency["constant_policy"], "C")
        self.assertIn("constant", frequency["statement"])
        self.assertEqual(frequency["counts"], {"C": 1, "K": 0})
        unknown = cost_records(w, b, {}, {}, now=clock(400))
        frequency = next(row for row in unknown["selection_frequencies"] if row["level"] == "pooled")
        self.assertEqual(frequency["frequency_denominator"], 1)
        self.assertEqual(frequency["unknown_selections"], 1)
        self.assertIsNone(frequency["constant_policy"])
        self.assertIsNone(unknown["strategy_worlds"][0]["complete_policy_seconds"])
        self.assertIsNone(unknown["resources"]["allocated_gpu_hours"])

    def test_shared_ambiguous_prefix_cost_cancels_in_paired_difference(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        prefix_call = next(branch for branch in b if branch.phase == "prefix").calls[0].call_id
        attempt = next(row for row in a if row["call_id"] == prefix_call)
        attempt.update(elapsed_seconds=None, observed_seconds=1, finished_at=None, recovered_at=clock(10))
        result = cost_records(w, b, r, i, a, now=clock(400))
        against_B = next(row for row in result["paired_comparisons"] if row["comparator"] == "B")
        self.assertEqual(against_B["policy_seconds_difference"], [-3, -3])
        against_C = next(row for row in result["paired_comparisons"] if row["comparator"] == "C")
        self.assertEqual(against_C["policy_seconds_difference"], [0, 0])

    def test_retrospective_stable_cost_includes_prefix_and_is_not_actual_savings(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        result = cost_records(w, b, r, i, a, now=clock(400))
        q = next(row for row in result["quality_preservation"] if row["policy"] == "K")
        self.assertEqual(q["retrospective_stable_completion"]["round"], 1)
        self.assertEqual(q["retrospective_stable_completion"]["seconds"], [40, 40])
        self.assertEqual(len(q["retrospective_stable_completion"]["call_ids"]), 20)
        self.assertIn("fixed schedule", q["retrospective_stable_completion"]["interpretation"])
        self.assertEqual(next(row for row in result["policy_costs"] if row["policy"] == "K")["seconds"], [64, 64])

    def test_observed_inventory_and_output_preservation_are_separate_from_measured_cost(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        before = copy.deepcopy((r, i, a))
        result = cost_records(w, b, r, i, a, now=clock(400))
        self.assertEqual(before, (r, i, a))
        self.assertEqual(len(result["retained_evidence"]), 12)
        self.assertTrue(all(row["inventory"]["complete_current_raw"] for row in result["retained_evidence"]))
        self.assertEqual(len(result["quality_preservation"]), 3)
        self.assertTrue(all(row["complete_deliveries"] is None for row in result["policy_costs"]))
        self.assertGreater(result["delivery_counts"]["source_attempts"], 0)

    def test_token_scalar_drift_and_unzoned_resource_clocks_are_rejected(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        r[next(iter(r))]["request_tokens"] = 99
        with self.assertRaisesRegex(ValueError, "token IDs"):
            cost_records(w, b, r, i, a, now=clock(400))
        with self.assertRaisesRegex(ValueError, "timezone"):
            cost_records(w, b, {}, {}, now="2026-10-06T00:00:00")

    def test_completed_raw_reply_without_attempt_cost_cannot_be_reported_free(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        missing = next(branch for branch in b if branch.phase == "prefix").calls[0].call_id
        a = [attempt for attempt in a if attempt["call_id"] != missing]
        with self.assertRaisesRegex(ValueError, "physical attempt costs"):
            cost_records(w, b, r, i, a, now=clock(400))

    def test_nonconstant_rule_keeps_paired_worlds_and_frequencies(self):
        w0, b0, r0, i0, a0 = fixture(Task.SORT, ("B", "C", "K"))
        w1, b1, r1, i1, a1 = fixture(Task.DIFFERENCE, ("B", "C", "K"))
        sources = json.loads(i1[next(branch.branch_id for branch in b1 if branch.policy == "B"), 1]["requests"]["before"])["peers"][0]["sources"]
        set_boundary(i1, b1, [sources[:-1], sources, sources, sources])
        result = cost_records((*w0, *w1), (*b0, *b1), r0 | r1, i0 | i1, a0 + a1, now=clock(400))
        frequency = next(row for row in result["selection_frequencies"] if row["level"] == "pooled")
        self.assertEqual(frequency["counts"], {"C": 1, "K": 1})
        self.assertEqual(frequency["frequencies"], {"C": 0.5, "K": 0.5})
        self.assertIsNone(frequency["constant_policy"])
        self.assertEqual(len(result["paired_comparisons"]), 6)
        for row in result["strategy_worlds"]:
            self.assertEqual(row["auc_denominator"], 16)
            self.assertEqual(len(row["continuation_call_ids"]), 16)
            self.assertEqual(len(row["call_ids"]), 32)

    def test_unavailable_selected_k_keeps_unknown_cost_even_with_complete_c(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        sources = json.loads(i[next(branch.branch_id for branch in b if branch.policy == "B"), 1]["requests"]["before"])["peers"][0]["sources"]
        set_boundary(i, b, [sources[:-1], sources, sources, sources])
        K = next(branch for branch in b if branch.policy == "K")
        for call in K.calls:
            del r[call.call_id]
        a = [attempt for attempt in a if attempt["call_id"] in r]
        result = cost_records(w, b, r, i, a, now=clock(400))
        selection = result["boundary_selections"][0]
        self.assertEqual(selection["selected_policy"], "K")
        self.assertFalse(selection["available"])
        chosen = next(row for row in result["strategy_worlds"] if row["strategy"] == "boundary_rule")
        self.assertIsNone(chosen["complete_policy_seconds"])
        self.assertTrue(next(row for row in result["strategy_worlds"] if row["strategy"] == "always_C")["available"])

    def test_retained_remote_inventory_excludes_host_v2_but_rule_requires_it(self):
        w, b, r, i, a = fixture(policies=("B", "C", "K"))
        result = cost_records(w, b, r, i, a, now=clock(400))
        record_id = w[0].main_edit.record_id
        for row in result["retained_evidence"]:
            inventory = row["inventory"]
            self.assertEqual(inventory["excluded_record_id"], record_id)
            self.assertNotIn([record_id, 2], inventory["remote_pairs"])
            self.assertTrue(inventory["complete_current_raw"])
        self.assertEqual(result["boundary_selections"][0]["selected_policy"], "C")
        sources = json.loads(i[next(branch.branch_id for branch in b if branch.policy == "B"), 1]["requests"]["before"])["peers"][0]["sources"]
        missing_v2 = [s for s in sources if s["record_id"] != record_id]
        set_boundary(i, b, [missing_v2, sources, sources, sources])
        result = cost_records(w, b, r, i, a, now=clock(400))
        self.assertEqual(result["boundary_selections"][0]["selected_policy"], "K")


if __name__ == "__main__":
    unittest.main()
