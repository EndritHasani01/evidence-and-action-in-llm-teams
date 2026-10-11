"""Independent course repair, inventory, transport, censoring and whole-policy cases."""

import copy
from dataclasses import asdict, replace
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.costs import boundary_selections, cost_records, select_boundary_policy
from recovery.edits import Edit
from recovery.evaluate import (ANNOTATIONS, aggregate_diagnostics, evaluate_records,
    identical_wrong_agreement, score_coordinates, trajectory)
from recovery.information import (delta_transport, edit_descriptor, information_atlas,
    information_records, old_value_visibility, receipt_timing, reconstruct_before, source_inventory)
from recovery.tasks import Task
from recovery.truth import Truth
from tests.cost_fixture import clock, fixture as cost_fixture, set_boundary
from tests.information_examples import examples
from tests.information_fixture import CharacterTokenizer, fixture as information_fixture
from tests.outcome_fixture import ROOT, encode, prepared, saved_records, selection
from tests.references import numeric_reference, relaxation_distances


def gold(world):
    """Independent insertion-order numeric and synchronous graph references."""
    if world.task is Task.BFS:
        return relaxation_distances(8, [r.value for r in world.records if not r.deleted])
    records = world.records if world.task is Task.TOP_K else sorted(world.records, key=lambda r: r.position)
    return numeric_reference(world.task.value, [r.value for r in records])


def answer(world, peer):
    values = gold(world)
    return values[6 * peer:6 * (peer + 1)] if world.task in (Task.PREFIX, Task.SORT) else values


def set_answer(row, candidate):
    validation = json.loads(row["validation_json"])
    raw = json.loads(row["raw_json"])
    reply = json.loads(raw["text"])
    reply["candidate"] = candidate
    raw["text"] = encode(reply)
    validation["generated"] = raw
    validation["candidate"]["value"] = (list(map(list, sorted(candidate.items(), key=lambda p: int(p[0]))))
        if isinstance(candidate, dict) else candidate)
    row.update(raw_json=encode(raw), validation_json=encode(validation))


def invalidate(row):
    validation = json.loads(row["validation_json"])
    validation["candidate"].update(status="invalid", value=None)
    validation.update(messages=[], json_valid=False, schema_valid=False, permissions_valid=False)
    row["validation_json"] = encode(validation)


class CourseRepairTests(unittest.TestCase):
    def test_all_course_coordinate_contracts_against_independent_gold(self):
        for prepared_world in prepared("course")[0].main:
            world = prepared_world.world
            old = Truth(world.task, world.size, tuple(gold(world).values()) if world.task is Task.BFS else tuple(gold(world)))
            for event in ("revision", "sham", "preserving"):
                if event == "preserving" and prepared_world.preserving_edit is None:
                    continue
                current = prepared_world.event_world(event)
                new = Truth(world.task, world.size, tuple(gold(current).values()) if world.task is Task.BFS else tuple(gold(current)))
                changed = {j for j in old.by_coordinate if old.by_coordinate[j] != new.by_coordinate[j]}
                unique, copies = set(), 0
                for peer in range(4):
                    rows, rates = score_coordinates(old, new, peer, "valid", answer(current, peer), "valid", answer(world, peer))
                    self.assertEqual({r["coordinate"] for r in rows if r["set"] == "D"}, changed & {r["coordinate"] for r in rows})
                    unique.update(r["coordinate"] for r in rows)
                    copies += len(rows)
                    self.assertTrue(all(r["rate"] in (1, None) for r in rates if r["metric"] in ("changed_accuracy", "preservation")))
                expected = {Task.TOP_K: 10, Task.PREFIX: 24, Task.DIFFERENCE: 23, Task.SORT: 24, Task.BFS: 8}[world.task]
                self.assertEqual((len(unique), copies), (expected, expected if world.task in (Task.PREFIX, Task.SORT) else 4 * expected))
                if event != "revision": self.assertEqual(changed, set())

    def test_collateral_damage_is_separate_from_old_error_repair(self):
        world = prepared("course")[0].main[0].world
        old = Truth(Task.DIFFERENCE, world.size, (0,) * 23)
        new = Truth(Task.DIFFERENCE, world.size, (1, -1, *([0] * 21)))
        prefix, current = [0] * 23, [1, -1, *([0] * 21)]
        prefix[3], current[0], current[2] = -4, 0, -3
        rows, rates = score_coordinates(old, new, 0, "valid", current, "valid", prefix)
        metrics = {r["metric"]: r for r in rates}
        self.assertEqual((metrics["changed_accuracy"]["rate"], metrics["old_value_persistence"]["rate"]), (1 / 2, 1 / 2))
        self.assertEqual((metrics["preservation"]["denominator"], metrics["preservation"]["rate"]), (20, 19 / 20))
        self.assertEqual(metrics["collateral_damage"]["rate"], 1 / 20)
        self.assertEqual(metrics["old_error_repair"]["rate"], 1)
        self.assertTrue(rows[3]["old_error_eligible"])
        self.assertFalse(rows[3]["preservation_eligible"])

    def test_invalid_failed_unknown_and_empty_diagnostic_denominators(self):
        world = next(w for w in prepared("course")[0].main if w.world.task is Task.BFS)
        old = Truth(Task.BFS, world.world.size, tuple(gold(world.world).values()))
        new = Truth(Task.BFS, world.world.size, tuple(gold(world.event_world("revision")).values()))
        for status in ("invalid", "failed", "unknown"):
            rows, rates = score_coordinates(old, new, 0, status, None, "valid", gold(world.world))
            metrics = {r["metric"]: r for r in rates}
            self.assertEqual(metrics["changed_malformed_or_missing"]["rate"], None if status == "unknown" else 1)
            self.assertEqual(metrics["old_value_persistence"]["rate"], None if status == "unknown" else 0)
            self.assertTrue(all(r["value"] is None for r in rows))
        _, rates = score_coordinates(old, old, 0, "valid", gold(world.world), "unknown", None)
        metrics = {r["metric"]: r for r in rates}
        self.assertEqual((metrics["changed_accuracy"]["denominator"], metrics["changed_accuracy"]["reason"]), (0, "no_changed_coordinates"))
        self.assertIsNone(metrics["preservation"]["denominator"])
        self.assertEqual(metrics["preservation"]["reason"], "prefix_round_four_unknown")

    def test_eligible_peers_worlds_then_equal_families_and_copy_counts(self):
        base = dict(size="fallback", phase="continuation", event="revision", policy="B", replicate=0,
                    round=1, metric="preservation", reason=None)
        rows = [dict(base, family=f, world_id=w, branch_id=w + "/B", peer=p,
            denominator=d, numerator=n, rate=n / d if d else None, eligible_coordinates=list(range(d)))
            for f, w, p, n, d in (("difference_array", "a", 0, 1, 1), ("difference_array", "a", 1, 0, 9),
                ("difference_array", "b", 0, 0, 21), ("prefix_sum", "c", 0, 1, 1), ("bfs_distance", "d", 0, 0, 0))]
        summary = next(r for r in aggregate_diagnostics(rows) if r["level"] == "all_families")
        self.assertEqual((summary["rate"], summary["eligible_peers"], summary["eligible_worlds"], summary["eligible_families"]), (5 / 8, 4, 3, 2))
        self.assertEqual((summary["unique_coordinate_count"], summary["peer_copy_count"]), (31, 32))
        rows[0].update(numerator=None, rate=None, reason="slot_unknown")
        self.assertIsNone(next(r for r in aggregate_diagnostics(rows) if r["level"] == "all_families")["rate"])

    def test_four_trajectory_categories_fragmentation_regression_and_incomplete(self):
        matrices = (([[1] * 4] * 4, "continuously_correct", 1, 1),
            ([[1] * 4, [0] * 4, [0] * 4, [1] * 4], "correct_at_end_after_delay_or_regression", 1, 4),
            ([[1] * 4, [0] * 4, [0] * 4, [0] * 4], "temporarily_correct_but_incorrect_at_end", 1, None),
            ([[int(p == r) for p in range(4)] for r in range(4)], "never_jointly_correct", None, None))
        for matrix, category, first, stable in matrices:
            result = trajectory(matrix)
            self.assertEqual((result["category"], result["first_joint_round"], result["first_stable_joint_round"]), (category, first, stable))
        self.assertTrue(trajectory(matrices[-1][0])["fragmented"])
        self.assertTrue(trajectory(matrices[1][0])["regression"])
        partial = trajectory([[1] * 4, [0] * 4, [None] * 4, [None] * 4])
        self.assertEqual((partial["category"], partial["observed_first_joint_round"], partial["regression"]), ("incomplete", 1, True))
        self.assertIsNone(partial["first_joint_round"])
        self.assertIsNone(partial["first_stable_joint_round"])
        for task in Task:
            rows = [dict(protocol_outcome="valid", correct=0, candidate=[7]) for _ in range(4)]
            self.assertEqual(identical_wrong_agreement(task, rows), None if task in (Task.PREFIX, Task.SORT) else True)

    def test_six_nonexclusive_labels_and_intersections_with_original_ids(self):
        worlds, branches = selection(Task.DIFFERENCE, size="course")
        records, inputs, attempts = saved_records(worlds, branches)
        branch = next(b for b in branches if b.phase == "continuation")
        set_answer(records[branch.calls[0].call_id], answer(worlds[0].world, 0))
        last = next(c for c in branch.calls if c.round_number == 4 and c.peer == 0)
        invalidate(records[last.call_id])
        saved = inputs[branch.branch_id, 1]
        before = json.loads(saved["requests"]["before"])
        changed = next(s for s in before["peers"][1]["sources"] if s["version"] == 2)
        del changed["value"], changed["deleted"]
        saved["requests"]["before"] = encode(before)
        actual = evaluate_records(worlds, branches, records, inputs, attempts)
        rows = [r for r in actual["annotations"] if r["branch_id"] == branch.branch_id]
        self.assertEqual(set(rows[0]["labels"]), set(ANNOTATIONS))
        first = next(r for r in rows if r["round"] == 1 and r["peer"] == 0)
        self.assertTrue(first["labels"]["explicit_old_value_persistence"])
        self.assertTrue(first["labels"]["incorrect_after_v2"])
        self.assertTrue(first["v2_delivery_ids"])
        self.assertTrue(next(r for r in rows if r["round"] == 1 and r["peer"] == 1)["labels"]["v2_unavailable"])
        final = next(r for r in rows if r["call_id"] == last.call_id)
        for label in ("protocol_inference_failure", "collateral_error", "incorrect_after_v2", "regression"):
            self.assertTrue(final["labels"][label])
        counts = next(r for r in actual["annotation_counts"] if r["branch_id"] == branch.branch_id)
        self.assertEqual(sum(r["count"] for r in counts["patterns"]), 16)
        self.assertEqual(next(r["positive"] for r in counts["intersections"] if r["labels"] == ["protocol_inference_failure", "regression"]), 1)


class CourseInformationTests(unittest.TestCase):
    def test_actual_course_prefix_exposure_history_tokens_communication_and_strata(self):
        for task in Task:
            w, b, r, i, a, c = information_fixture(task, size="course")
            result = information_records(w, b, r, i, a, committed=c, tokenizer=CharacterTokenizer())
            self.assertEqual(len(result["prefix"]), 16)
            self.assertTrue(all(row["owner_v1_exposure"] and len(row["exposed_call_ids"]) == 4 for row in result["owner_exposure"]))
            self.assertEqual([p["old_gold_correct"] for p in result["prefix"]], [1] * 16)
            self.assertTrue(any(p["history_content_tokens"] > 0 for p in result["prefix"]))
            self.assertTrue(all(p["input_tokens"] > p["history_content_tokens"] for p in result["prefix"]))
            self.assertTrue(all(row["source_attempts"] == 0 for row in result["communication"]))
            for row in result["receipt_strata"]:
                self.assertEqual((row["old_candidate_correct"], row["prefix_round_four_joint"]), (1, 1))
                self.assertEqual(row["scheduled"], 4)
            unknown = information_records(w, b, r, i, a, committed=c)
            self.assertTrue(any(p["history_content_tokens"] is None for p in unknown["prefix"]))
            with self.assertRaisesRegex(ValueError, "tokenizer"):
                information_records(w, b, r, i, a, committed=c, tokenizer=type("Bad", (), {"encode": lambda *args, **kw: []})())

    def test_initial_inventories_pending_tombstones_and_injected_revision_exclusion(self):
        for task in (Task.PREFIX, Task.BFS):
            prepared_world = next(w for w in prepared("course")[0].main if w.world.task is task)
            current = prepared_world.event_world("revision")
            sources = [asdict(r) for r in current.records]
            edit = prepared_world.main_edit.record_id
            row = source_inventory(current, sources, 0, exclude_record_id=edit)
            self.assertTrue(row["complete_current_raw"])
            self.assertEqual(row["remote_denominator"], sum(r.owner != 0 and r.record_id != edit for r in current.records))
            self.assertTrue(all(pair[0] != edit for pair in row["remote_pairs"]))
            self.assertEqual(row["known_tombstones"], int(task is Task.BFS))
            source = next(r for r in sources if r["record_id"] == edit)
            del source["value"], source["deleted"]
            pending = source_inventory(current, sources, 0)
            self.assertEqual(pending["pending_records"], 1)
            self.assertFalse(pending["complete_current_raw"])
            self.assertEqual(pending["known_tombstones"], 0)
            sources[0]["version"] = 17
            with self.assertRaisesRegex(ValueError, "authority"):
                source_inventory(current, sources, 0)

    def test_censoring_retains_no_receipt_no_success_same_later_and_pre_authoritative_correctness(self):
        def timing(availability, correctness, origin="peer"):
            rows = [dict(round=n, call_id=f"course/r{n}/p0", correct=c, v2_available=a, v2_delivery_ids=["delivery"] if a else [])
                for n, (a, c) in enumerate(zip(availability, correctness), 1)]
            first = next((n for n, a in enumerate(availability, 1) if a), None)
            delivery = dict(delivery_id="delivery", recipient=0, origin=origin,
                first_usable={"phase": "recovery", "round_number": first})
            return receipt_timing(rows, [delivery], 0)
        for a, c, origin, category, lag in (([False] * 4, [1] * 4, "peer", "no_receipt", None),
            ([True] * 4, [0] * 4, "host", "receipt_without_success", None),
            ([True] * 4, [1] * 4, "host", "same_call_success", 0),
            ([False, True, True, True], [0, 0, 1, 0], "peer", "later_success", 1),
            ([False, None, True, True], [0, None, 1, 1], "peer", "receipt_or_outcome_censored", None),
            ([True] * 4, [0, None, 1, 1], "host", "receipt_or_outcome_censored", None)):
            result = timing(a, c, origin)
            self.assertEqual((result["category"], result["receipt_to_success_lag"]), (category, lag))
            self.assertEqual(result["scheduled_rounds"], 4)
            if True in a: self.assertEqual(result["receipt_origins"], [origin])
        self.assertTrue(timing([False, False, True, True], [1, 0, 0, 0])["correct_before_authoritative_receipt"])
        self.assertIsNone(timing([None] * 4, [None] * 4)["correct_before_authoritative_receipt"])
        with self.assertRaisesRegex(ValueError, "delivery evidence"):
            receipt_timing([dict(round=n, call_id=str(n), correct=1, v2_available=True, v2_delivery_ids=[]) for n in range(1, 5)], [], 0)

    def test_source_bound_literals_keep_exact_spans_and_numeric_coincidence_unresolved(self):
        world = next(w for w in prepared("course")[0].main if w.world.task is Task.PREFIX)
        source = next(r for r in world.world.records if r.record_id == world.main_edit.record_id)
        literal = f"unchanged excerpt {source.record_id}/v1={source.value}."
        result = old_value_visibility(source.record_id, source.value, None,
            [dict(text=literal, call_id="original-prefix/r4/p0", message_id="original-prefix/r4/p0/to1", delivery_id="original-prefix/r4/p0/to1/text", history_index=2)])
        matched = result["evidence"][0]
        self.assertEqual(literal[slice(*matched["span"])], matched["excerpt"])
        self.assertEqual(matched["call_id"], "original-prefix/r4/p0")
        for spelling in (str(source.value), f"{source.record_id}/v1={source.value}.5", f"{source.record_id}/v1={source.value}e2",
            f"{source.record_id}/v1={source.value}_1", f"{source.record_id}/v1={source.value}+1", f"{source.record_id}/v2={source.value}"):
            unresolved = old_value_visibility(source.record_id, source.value, None, [dict(text=spelling, call_id="call")])
            self.assertEqual((unresolved["status"], unresolved["visible"]), ("unresolved", None))
        wrong = old_value_visibility(source.record_id, source.value, None, [dict(text=f"{source.record_id}/v1={source.value + 1}", call_id="call")])
        self.assertEqual(len(wrong["conflicting_assertions"]), 1)
        receipt = dict(record_id=source.record_id, previous_version=1, new_version=2, before_value=source.value)
        self.assertEqual(old_value_visibility(source.record_id, source.value, receipt, [])["evidence"][0]["origin"], "host_receipt")
        with self.assertRaisesRegex(ValueError, "genuine"):
            old_value_visibility(source.record_id, source.value, dict(receipt, before_value=source.value + 1), [])

    def test_wrong_last_candidates_transport_every_course_position_without_repair(self):
        for base in prepared("course")[0].main:
            if base.world.task not in (Task.PREFIX, Task.DIFFERENCE): continue
            for source in base.world.records:
                for replacement in ((1, 9) if base.world.task is Task.PREFIX else (0, 30)):
                    if replacement == source.value: continue
                    revised = replace(base, main_edit=Edit(source.record_id, replacement))
                    for peer in range(4):
                        original = answer(base.world, peer)
                        original[0] += 17
                        reference = delta_transport(revised, "revision", peer, "valid", original)
                        expected = answer(revised.event_world("revision"), peer)
                        expected[0] += 17
                        self.assertEqual(reference["candidate"], expected)
                        self.assertEqual(reference["residual_old"], reference["residual_new"])
                        self.assertFalse(reference["old_candidate_correct"])
                        self.assertFalse(reference["transported_correct"])
                        self.assertEqual(reference["actual_old_candidate"], original)

    def test_last_invalid_failed_and_missing_candidates_never_backfill(self):
        for task in (Task.PREFIX, Task.DIFFERENCE):
            w, b, r, i, a, c = information_fixture(task, policies=("C",), size="course")
            last = next(call for branch in b if branch.phase == "prefix" for call in branch.calls if call.round_number == 4 and call.peer == 0)
            invalidate(r[last.call_id])
            actual = information_records(w, b, r, i, a, committed=c)
            row = next(row for row in actual["transport_references"] if row["peer"] == 0)
            self.assertFalse(row["available"])
            self.assertEqual(row["prefix_call_id"], last.call_id)
            for status in ("failed", "unknown"):
                self.assertFalse(delta_transport(w[0], "revision", 0, status, None)["available"])

    def test_reconstruction_has_explicit_assumptions_and_cleared_work_unavailable(self):
        for task in (Task.PREFIX, Task.DIFFERENCE, Task.SORT):
            base = next(w for w in prepared("course")[0].main if w.world.task is task)
            raw = [asdict(r) for r in base.event_world("revision").records]
            source = next(r for r in base.world.records if r.record_id == base.main_edit.record_id)
            results = [reconstruct_before(base, peer, "valid", answer(base.world, peer), raw) for peer in range(4)]
            self.assertTrue(all(row["information_view"] and "assumed" in row["correctness_assumption"] for row in results))
            self.assertTrue(any(row["before_value"] == source.value for row in results))
        w, b, r, i, a, c = information_fixture(size="course")
        result = information_records(w, b, r, i, a, committed=c)
        cleared = [row for row in result["receipt_information"] if row["policy"] in ("C", "C_delta")]
        self.assertTrue(all(not row["old_candidate_in_view"] for row in cleared))
        self.assertTrue(all(row["reconstructibility"]["status"] == "old_candidate_unavailable_in_view" for row in cleared))

    def test_stated_view_atlas_and_course_descriptors_remain_descriptive(self):
        atlas = information_atlas()
        self.assertEqual({r["family"] for r in atlas}, {r["family"] for r in examples()})
        self.assertTrue(all(r["information_view"] and r["correctness_assumption"] for r in atlas))
        for base in prepared("course")[0].main:
            descriptor = edit_descriptor(base, "revision")
            old, new = gold(base.world), gold(base.event_world("revision"))
            old = list(old.values()) if isinstance(old, dict) else old
            new = list(new.values()) if isinstance(new, dict) else new
            start = 1 if base.world.task is Task.DIFFERENCE else 0
            self.assertEqual(descriptor["changed_coordinates"], [j + start for j, (a, b) in enumerate(zip(old, new)) if a != b])
            if base.preserving_edit: self.assertEqual(edit_descriptor(base, "preserving")["changed_coordinates"], [])


class CoursePolicyCostTests(unittest.TestCase):
    def case(self, task=Task.SORT):
        return cost_fixture(task, size="course")

    def test_replay_retry_failure_and_f_abandoned_prefix_cost(self):
        w, b, r, i, a = self.case()
        result = cost_records(w, b, r, i, a, now=clock(400))
        # 16 prefix + four ordinary continuations + three 12-new-call replays:
        # this fixture has seven continuations, with P_G/Q_B/Q_C sharing round 1.
        self.assertEqual((len(a), result["physical"]["attempt_seconds"]), (117, [235, 235]))
        self.assertEqual(result["physical"]["recorded_failure_generations"], 1)
        policies = {row["policy"]: row for row in result["policy_costs"]}
        for policy in ("F", "P_G", "Q_B", "Q_C"):
            row = policies[policy]
            self.assertEqual(row["logical_calls"], 32)
            self.assertEqual(len(row["generation_ids"]), 32)
            self.assertEqual(row["complete_policy_seconds"], [67, 67] if policy in ("Q_B", "P_G") else [64, 64])
            self.assertEqual(row["call_ids"][:16], [c.call_id for branch in b if branch.phase == "prefix" for c in branch.calls])
        self.assertTrue(any(cid != gid for cid, gid in zip(policies["P_G"]["call_ids"], policies["P_G"]["generation_ids"])))

    def test_boundary_rule_uses_initial_coverage_pending_and_tombstones_only(self):
        for task in (Task.PREFIX, Task.BFS):
            w, b, r, i, a = self.case(task)
            sources = [asdict(record) for record in w[0].event_world("revision").records]
            manifest = [dict(record_id=s["record_id"], version=s["version"]) for s in sources]
            self.assertEqual(select_boundary_policy(manifest, [sources] * 4)["selected_policy"], "C")
            pending = copy.deepcopy(sources)
            edited = next(s for s in pending if s["version"] == 2)
            del edited["value"], edited["deleted"]
            choice = select_boundary_policy(manifest, [sources, pending, sources, sources])
            self.assertEqual(choice["selected_policy"], "K")
            self.assertEqual(choice["coverage"][1]["denominator"], 12 if task is Task.BFS else 24)
            self.assertIsNone(select_boundary_policy(manifest, [None] * 4)["selected_policy"])
            self.assertEqual(select_boundary_policy(manifest, [None, pending, None, None])["selected_policy"], "K")

    def test_constant_rule_whole_branch_and_unknown_selected_cost_no_fallback(self):
        w, b, r, i, a = self.case()
        full = cost_records(w, b, r, i, a, now=clock(400))
        self.assertEqual(full["selection_frequencies"][0]["constant_policy"], "C")
        chosen = next(row for row in full["strategy_worlds"] if row["strategy"] == "boundary_rule")
        c = next(branch for branch in b if branch.policy == "C")
        self.assertEqual(chosen["branch_id"], c.branch_id)
        self.assertEqual(chosen["continuation_call_ids"], [call.call_id for call in c.calls])
        self.assertEqual(chosen["final_joint"], 1)
        removed = c.calls[-1].call_id
        del r[removed]
        a = [attempt for attempt in a if attempt["call_id"] != removed]
        unknown = cost_records(w, b, r, i, a, now=clock(400))
        selection_row = unknown["boundary_selections"][0]
        self.assertEqual(selection_row["selected_policy"], "C")
        self.assertFalse(selection_row["available"])
        chosen = next(row for row in unknown["strategy_worlds"] if row["strategy"] == "boundary_rule")
        self.assertIsNone(chosen["auc"])
        self.assertIsNone(chosen["complete_policy_seconds"])
        self.assertTrue(all(row["policy_seconds_difference"] is None for row in unknown["paired_comparisons"]))

    def test_selection_cannot_read_later_sources_gold_candidates_or_branch_success(self):
        w, b, r, i, a = self.case()
        sources = [asdict(record) for record in w[0].event_world("revision").records]
        set_boundary(i, b, [sources[:-1], sources, sources, sources])
        choice = boundary_selections(w, b, i)
        self.assertEqual(choice[0]["selected_policy"], "K")
        for branch in b:
            if branch.policy in ("B", "C", "K"):
                state = json.loads(i[branch.branch_id, 1]["requests"]["before"])
                state["peers"][0].update(candidate="ignored", history="ignored", gold="ignored")
                i[branch.branch_id, 1]["requests"]["before"] = encode(state)
        self.assertEqual(boundary_selections(w, b, i), choice)
        saved = i[next(branch.branch_id for branch in b if branch.policy == "B"), 1]
        state = json.loads(saved["requests"]["before"])
        state["peers"][0]["sources"] = sources
        saved["requests"]["before"] = encode(state)
        with self.assertRaisesRegex(ValueError, "coverage differs"):
            boundary_selections(w, b, i)

    def test_unmeasured_completed_outcomes_and_mismatched_sources_are_rejected(self):
        w, b, r, i, a = self.case()
        with self.assertRaisesRegex(ValueError, "physical attempt"):
            cost_records(w, b, r, i, a[1:], now=clock(400))
        saved = next(iter(i.values()))
        state = json.loads(saved["requests"]["before"])
        state["peers"][0]["sources"][0]["value"] += 100
        saved["requests"]["before"] = encode(state)
        with self.assertRaisesRegex(ValueError, "source.*manifest"):
            cost_records(w, b, r, i, a, now=clock(400))


class CourseDiagnosticsCLITests(unittest.TestCase):
    def test_course_full_main_and_development_unknown_exports_are_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "absent.sqlite"
            for stage, count in (("main", 6280), ("development", 1178)):
                output = Path(directory) / (stage + ".json.gz")
                command = [sys.executable, "-S", "-m", "recovery", "analyze", "--costs", "--diagnostics", "--estimands",
                    "--as-of", clock(400), "--stage", stage, "--manifest", str(ROOT / "tests/fixtures/population_course.json"),
                    "--schedule", str(ROOT / "tests/fixtures/schedules_course.json"), "--worker", str(missing), "--output", str(output)]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                data = json.loads(gzip.decompress(output.read_bytes()))
                self.assertEqual((data["coverage"]["scheduled"], data["coverage"]["unknown"]), (count, count))
                self.assertTrue(all(row["selected_policy"] is None for row in data["costs"]["boundary_selections"]))
                self.assertTrue(all(row["complete_policy_seconds"] is None for row in data["costs"]["policy_costs"]))
                self.assertTrue(all(row["owner_v1_exposure"] is None for row in data["information"]["owner_exposure"]))
                self.assertTrue(all(row["category"] == "incomplete" for row in data["trajectories"]))
                before = output.read_bytes()
                repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.assertEqual(repeated.returncode, 2)
                self.assertEqual(output.read_bytes(), before)
            self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
