from dataclasses import FrozenInstanceError
from random import Random
import unittest

from recovery.edits import Edit, apply_edit, legal_edits, select_edit
from recovery.tasks import PEERS, Size, Task, numeric_range
from tests.references import numeric_reference, relaxation_distances
from tests.test_tasks import numeric_world
from tests.test_truth_contracts import star_world


class BoundaryChoices:
    """Enumerate every choice boundary and capture the actual choice domains."""

    def __init__(self, *indices):
        self.indices = iter(indices)
        self.domains = []

    def choice(self, sequence):
        self.domains.append(tuple(sequence))
        return sequence[next(self.indices)]


class LegalEditTests(unittest.TestCase):
    def test_numeric_exact_sets_all_owners_endpoints_and_sizes(self):
        for size in Size:
            for task in (Task.PREFIX, Task.DIFFERENCE, Task.SORT):
                low, high = numeric_range(task)
                world = numeric_world(task, size, [low, high] * (size.numeric_length // 2))
                for owner in PEERS:
                    expected = tuple(Edit(r.record_id, value) for r in world.records
                                     if r.owner == owner for value in range(low, high + 1)
                                     if value != r.value)
                    self.assertEqual(legal_edits(world, owner=owner), expected)
                    # Enumerate selection boundaries instead of statistical frequencies.
                    records = [r for r in world.records if r.owner == owner]
                    for i, record in enumerate(records):
                        options = [e for e in expected if e.record_id == record.record_id]
                        for j, expected_edit in enumerate(options):
                            rng = BoundaryChoices(i, j)
                            self.assertEqual(select_edit(expected, rng), expected_edit)
                            self.assertEqual(rng.domains[0], tuple(r.record_id for r in records))
                            self.assertEqual(rng.domains[1], tuple(options))
                    self.assertEqual(legal_edits(world, preserving=True), ())

    def test_top_k_exact_unique_cutoff_and_preserving_pair_sets(self):
        for size in Size:
            # Duplicate values above cutoff are excluded from main edits.
            values = [99, 99, 98, 97, 96, 95, 94, 93, 50, 50, 49, 0]
            values += [0] * (size.numeric_length - len(values))
            world = numeric_world(Task.TOP_K, size, values)
            expected_main = tuple(Edit(f"x{i:03d}", v) for i in range(2, 8) for v in range(50))
            expected_preserving = tuple(Edit(f"x{i:03d}", v)
                                        for i in range(10, size.numeric_length)
                                        for v in range(51) if v != values[i])
            self.assertEqual(legal_edits(world), expected_main)
            self.assertEqual(legal_edits(world, preserving=True), expected_preserving)
            old = numeric_reference(task="top_k", values=values)
            for edit in expected_main + expected_preserving:
                revised = apply_edit(world, edit)
                new = numeric_reference("top_k", [r.value for r in revised.records])
                self.assertEqual(new == old, edit in expected_preserving)
            for owner in PEERS:
                ids = {r.record_id for r in world.records if r.owner == owner}
                self.assertEqual(legal_edits(world, owner=owner),
                                 tuple(e for e in expected_main if e.record_id in ids))
            zero = numeric_world(Task.TOP_K, size, [99] + [0] * (size.numeric_length - 1))
            self.assertEqual(legal_edits(zero), ())
            self.assertEqual(legal_edits(zero, preserving=True), ())

    def test_preserving_is_one_uniform_pair_draw_main_is_two_draws(self):
        # Unequal pair counts make accidental record-first preserving sampling visible.
        legal = (Edit("x000", 0), Edit("x001", 0), Edit("x001", 1))
        for i, edit in enumerate(legal):
            rng = BoundaryChoices(i)
            self.assertEqual(select_edit(legal, rng, preserving=True), edit)
            self.assertEqual(rng.domains, [legal])
        for record_index, value_index, edit in ((0, 0, legal[0]), (1, 0, legal[1]), (1, 1, legal[2])):
            self.assertEqual(select_edit(legal, BoundaryChoices(record_index, value_index)), edit)
        with self.assertRaisesRegex(ValueError, "no eligible"):
            select_edit((), Random(0))

    def test_bfs_all_legal_edges_against_independent_relaxation(self):
        for size in Size:
            world = star_world(size)
            old = relaxation_distances(size.node_count, [r.value for r in world.records])
            for preserving in (False, True):
                expected = tuple(Edit(r.record_id, None) for r in world.records
                                 if (relaxation_distances(size.node_count,
                                     [s.value for s in world.records if s != r]) == old) == preserving)
                self.assertTrue(expected)
                self.assertEqual(legal_edits(world, preserving=preserving), expected)
                for owner in PEERS:
                    owner_ids = {r.record_id for r in world.records if r.owner == owner}
                    self.assertEqual(legal_edits(world, owner=owner, preserving=preserving),
                                     tuple(e for e in expected if e.record_id in owner_ids))
                for i, edit in enumerate(expected):
                    indices = (i,) if preserving else (i, 0)
                    self.assertEqual(select_edit(expected, BoundaryChoices(*indices),
                                                 preserving=preserving), edit)
            self.assertEqual(set(legal_edits(world)) | set(legal_edits(world, preserving=True)),
                             {Edit(r.record_id, None) for r in world.records})

    def test_source_events_are_immutable_single_edits_from_original(self):
        for size in Size:
            numeric = numeric_world(Task.PREFIX, size, [1] * size.numeric_length)
            for world, edit in ((numeric, Edit("x000", 9)),
                                (star_world(size), Edit("e000", None))):
                revised = apply_edit(world, edit)
                changed = [r for r in revised.records if r.version == 2]
                self.assertEqual(len(changed), 1)
                original = next(r for r in world.records if r.record_id == edit.record_id)
                self.assertEqual((original.version, original.deleted), (1, False))
                self.assertEqual(changed[0].owner, original.owner)
                self.assertEqual(changed[0].position, original.position)
                if world.task is Task.BFS:
                    self.assertEqual(changed[0].value, original.value)
                    self.assertTrue(changed[0].deleted)
                self.assertIs(apply_edit(world, None), world)
                with self.assertRaisesRegex(ValueError, "original v1"):
                    apply_edit(revised, edit)
                with self.assertRaisesRegex(ValueError, "original v1"):
                    legal_edits(revised)
                with self.assertRaises(FrozenInstanceError):
                    edit.replacement = 0
            for bad in (Edit("missing", 2), Edit("x000", 1), Edit("x000", None),
                        Edit("x000", True), Edit("x000", 1.0), Edit("x000", 10)):
                with self.assertRaises(ValueError):
                    apply_edit(numeric, bad)
            with self.assertRaises(ValueError):
                apply_edit(star_world(size), Edit("e000", 1))
            for bad_owner in (-1, 4, True, "0"):
                with self.assertRaises(ValueError):
                    legal_edits(numeric, owner=bad_owner)


if __name__ == "__main__":
    unittest.main()
