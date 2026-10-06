"""Independent failure-mode checks for the §7.2 pure diagnostic functions."""

from dataclasses import asdict, replace
import unittest

from recovery.edits import Edit
from recovery.information import (delta_transport, edit_descriptor, information_atlas,
    old_value_visibility, receipt_timing, reconstruct_before, source_inventory)
from recovery.tasks import Size, Task
from recovery.truth import solve_world
from tests.estimand_fixture import prepared
from tests.information_examples import examples


class InformationCoreTests(unittest.TestCase):
    def world(self, task, size="target"):
        return next(w for w in prepared(size)[0].main if w.world.task is task)

    def test_transport_all_positions_directions_shards_sizes_and_wrong_candidates(self):
        for size in Size:
            for task in (Task.PREFIX, Task.DIFFERENCE):
                base = self.world(task, size.value)
                for source in base.world.records:
                    for replacement in (1, 9) if task is Task.PREFIX else (0, 30):
                        if replacement == source.value:
                            continue
                        world = replace(base, main_edit=Edit(source.record_id, replacement))
                        old, new = solve_world(world.world), solve_world(world.event_world("revision"))
                        for peer in range(4):
                            for wrong in (False, True):
                                actual = old.candidate(peer)
                                if wrong:
                                    actual[0] += 17
                                result = delta_transport(world, "revision", peer, "valid", actual)
                                expected = new.candidate(peer)
                                if wrong:
                                    expected[0] += 17
                                self.assertEqual(result["candidate"], expected)
                                self.assertEqual(result["residual_old"], result["residual_new"])
                                self.assertEqual(result["transported_correct"], int(not wrong))
                                self.assertEqual(result["actual_old_candidate"], actual)

    def test_transport_invalid_unknown_and_other_tasks_never_backfill(self):
        world = self.world(Task.PREFIX)
        for status, reason in (("unknown", "prefix_round_four_unknown"),
                               ("invalid", "prefix_round_four_not_protocol_valid"),
                               ("failed", "prefix_round_four_not_protocol_valid")):
            result = delta_transport(world, "revision", 0, status, None)
            self.assertFalse(result["available"])
            self.assertIsNone(result["candidate"])
            self.assertEqual(result["reason"], reason)
        self.assertEqual(delta_transport(world, "sham", 0, "valid", [])['reason'], "not_applicable")
        self.assertEqual(delta_transport(self.world(Task.SORT), "revision", 0, "valid", [])['reason'], "not_applicable")

    def test_tombstone_pending_remote_coverage_and_revision_exclusion(self):
        world = self.world(Task.BFS)
        current = world.event_world("revision")
        changed = next(r for r in current.records if r.version == 2)
        sources = [asdict(r) for r in current.records]
        result = source_inventory(current, sources, (changed.owner + 1) % 4)
        self.assertTrue(result["complete_current_raw"])
        self.assertEqual(result["known_tombstones"], 1)
        excluded = source_inventory(current, sources, (changed.owner + 1) % 4, exclude_record_id=changed.record_id)
        self.assertEqual(excluded["remote_known"], result["remote_known"] - 1)
        pending = [{k: v for k, v in s.items() if k not in ("value", "deleted")} if s['version'] == 2 else s for s in sources]
        result = source_inventory(current, pending, 0)
        self.assertFalse(result["complete_current_raw"])
        self.assertEqual((result["pending_records"], result["known_tombstones"]), (1, 0))

    def test_numeric_coincidence_wrong_ids_versions_and_unrecognized_prose_unresolved(self):
        for text in ("7 is useful", "candidate [7,7]", "x001/v1=7", "x000/v2=7", "x000/v1=70",
                     "x000 used to be seven", "x000/v1=07", "ax000/v1=7"):
            result = old_value_visibility("x000", 7, None, [{"text": text, "call_id": "original"}])
            self.assertEqual(result["status"], "unresolved", text)
            self.assertIsNone(result["visible"])
        self.assertEqual(old_value_visibility("x000", 7, None, [{"text": "7 7"}])["numeric_occurrences"], 2)

    def test_source_bound_literal_and_host_receipt_keep_original_links_and_conflicts(self):
        result = old_value_visibility("x000", 7, None, [{"text": "x000/v1=7 and x000/v1=8",
            "call_id": "call-a", "message_id": "msg-a", "delivery_id": "delivery-a", "history_index": 2}])
        self.assertTrue(result["visible"])
        self.assertEqual(result["evidence"][0]["delivery_id"], "delivery-a")
        self.assertEqual(result["evidence"][0]["excerpt"], "x000/v1=7")
        self.assertEqual(len(result["conflicting_assertions"]), 1)
        receipt = dict(record_id="x000", before_value=7, previous_version=1, new_version=2)
        self.assertTrue(old_value_visibility("x000", 7, receipt, [])["visible"])
        receipt["before_value"] = 8
        with self.assertRaisesRegex(ValueError, "genuine"):
            old_value_visibility("x000", 7, receipt, [])

    def test_prefix_reconstruction_local_first_interior_and_missing_boundary(self):
        base = self.world(Task.PREFIX)
        for k in (0, 1, 8, 9, 31):
            source = base.world.records[k]
            world = replace(base, main_edit=Edit(source.record_id, 1 if source.value != 1 else 2))
            peer = k // 8
            old = solve_world(world.world).candidate(peer)
            result = reconstruct_before(world, peer, "valid", old, [])
            self.assertEqual(result["status"], "unresolved" if k == 8 else "reconstructible_under_assumption")
            if k != 8:
                self.assertEqual(result["before_value"], source.value)
            else:
                raw = [asdict(r) for r in world.event_world("revision").records[:8]]
                self.assertEqual(reconstruct_before(world, peer, "valid", old, raw)["before_value"], source.value)

    def test_wrong_difference_candidate_is_only_hypothetical_reconstruction(self):
        world = self.world(Task.DIFFERENCE)
        k = next(r.position for r in world.world.records if r.record_id == world.main_edit.record_id)
        anchor = next(r for r in world.world.records if r.position != k)
        old = solve_world(world.world).candidate(0)
        result = reconstruct_before(world, 0, "valid", old, [asdict(anchor)])
        self.assertEqual(result["before_value"], world.world.records[k].value)
        old[min(k, anchor.position)] += 1
        wrong = reconstruct_before(world, 0, "valid", old, [asdict(anchor)])
        self.assertNotEqual(wrong["before_value"], result["before_value"])
        self.assertIn("assumed", wrong["correctness_assumption"])
        self.assertEqual(reconstruct_before(world, 0, "valid", old, [])["status"], "unresolved")

    def test_sort_reconstruction_publishes_ambiguity_and_domain(self):
        world = self.world(Task.SORT)
        old = solve_world(world.world)
        raw = [asdict(r) for r in world.event_world("revision").records]
        results = [reconstruct_before(world, peer, "valid", old.candidate(peer), raw) for peer in range(4)]
        self.assertTrue(any(r["status"] == "unresolved" and len(r["possible_before_values"]) > 1 for r in results))
        self.assertTrue(any(r["status"] == "reconstructible_under_assumption" for r in results))

    def timing(self, availability, correctness, origin="peer"):
        rows = [dict(round=r, call_id=str(r), correct=c, v2_available=a,
                     v2_delivery_ids=["receipt"] if a else []) for r, (a, c) in enumerate(zip(availability, correctness), 1)]
        return receipt_timing(rows, [dict(delivery_id="receipt", origin=origin, recipient=0)], 0)

    def test_receipt_same_later_none_without_success_and_before_receipt(self):
        self.assertEqual(self.timing([True] * 4, [1] * 4, "host")["category"], "same_call_success")
        later = self.timing([False, True, True, True], [0, 0, 1, 0])
        self.assertEqual((later["category"], later["receipt_to_success_lag"], later["receipt_origins"]), ("later_success", 1, ["peer"]))
        self.assertEqual(self.timing([True] * 4, [0] * 4)["category"], "receipt_without_success")
        before = self.timing([False, False, True, True], [1, 0, 0, 0])
        self.assertTrue(before["correct_before_authoritative_receipt"])
        self.assertEqual(self.timing([False] * 4, [1] * 4)["category"], "no_receipt")

    def test_receipt_unknowns_censor_first_boundaries_and_lags(self):
        for a, c in (([False, None, True, True], [0, None, 1, 1]),
                     ([True] * 4, [0, None, 1, 1]), ([False, False, None, None], [0, 0, None, None])):
            result = self.timing(a, c)
            self.assertEqual(result["category"], "receipt_or_outcome_censored")
            self.assertIsNone(result["receipt_to_success_lag"])
            self.assertTrue(result["censored"])

    def test_atlas_selected_independent_ambiguity_and_sufficiency_witnesses(self):
        rows = examples()
        self.assertEqual({r["family"] for r in rows}, {r["family"] for r in information_atlas()})
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertTrue(row["information_view"] and row["correctness_assumption"])
        self.assertEqual(rows[-1]["reconstructed"], [5, 8, 7, 11])

    def test_descriptors_distinguish_source_and_output_owners_and_preserving_empty(self):
        for task in Task:
            world = self.world(task)
            result = edit_descriptor(world, "revision")
            self.assertEqual(result["source_owner"], world.edited_owner)
            self.assertTrue(result["affected_output_owner_count"] > 0)
            if task in (Task.TOP_K, Task.DIFFERENCE, Task.BFS):
                self.assertEqual(result["affected_output_owner_count"], 4)
            if task in (Task.TOP_K, Task.BFS):
                self.assertEqual(edit_descriptor(world, "preserving")["affected_output_owner_count"], 0)
            if task is Task.SORT:
                self.assertIsInstance(result["sort_crossed_boundaries"], list)
            if task is Task.BFS:
                self.assertEqual(result["bfs_disconnected"], bool(result["bfs_unreachable_nodes"]))


if __name__ == "__main__":
    unittest.main()
