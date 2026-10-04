import copy
from dataclasses import FrozenInstanceError, replace
import itertools
import unittest

from recovery.tasks import (PEERS, Size, SourceRecord, Task, World, candidate_contract,
                            coordinate_map, source_manifest)
from recovery.truth import (Truth, bfs_distances, changed_coordinates,
                            exact_candidate, solve_world)
from tests.references import relaxation_distances
from tests.test_tasks import changed_record, generated, numeric_world


def star_world(size):
    # Nodes 7/11 remain leaves; five extra edges give alternative paths elsewhere.
    edges = [(0, v) for v in range(1, size.node_count)]
    edges += [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    per_peer = size.edge_count // 4
    return World(Task.BFS, size,
                 tuple(SourceRecord(f"e{i:03d}", i // per_peer, None, edge)
                       for i, edge in enumerate(edges)))


class RevisionTruthTests(unittest.TestCase):
    def test_prefix_all_positions_and_both_delta_directions(self):
        for size in Size:
            n = size.numeric_length
            for original, replacement in ((1, 9), (9, 1)):
                old_world = numeric_world(Task.PREFIX, size, [original] * n)
                old = solve_world(old_world)
                for k in range(n):
                    with self.subTest(size=size, original=original, position=k):
                        new = solve_world(changed_record(old_world, k, replacement))
                        changes = changed_coordinates(old, new)
                        self.assertEqual(changes.changed, frozenset(range(k, n)))
                        self.assertEqual(changes.unchanged, frozenset(range(k)))
                        delta = replacement - original
                        self.assertEqual(new.candidate(), [value + (delta if j >= k else 0)
                                                          for j, value in enumerate(old.values)])
                        self.assert_changes_and_copies(old, new)
                # Each segment starts with the global prefix, not a local reset.
                for peer in PEERS:
                    self.assertEqual(old.candidate(peer)[0], original * (peer * size.shard_size + 1))

    def test_difference_all_positions_endpoints_boundaries_and_negatives(self):
        for size in Size:
            n = size.numeric_length
            raw = [0, 30] * (n // 2)
            world = numeric_world(Task.DIFFERENCE, size, raw)
            old = solve_world(world)
            self.assertIn(-30, old.values)
            for k in range(n):
                replacement = 30 - raw[k]
                delta = replacement - raw[k]
                new = solve_world(changed_record(world, k, replacement))
                expected_D = ({k} if k >= 1 else set()) | ({k + 1} if k <= n - 2 else set())
                self.assertEqual(changed_coordinates(old, new).changed, frozenset(expected_D))
                for j in range(1, n):
                    expected = old.by_coordinate[j] + delta * ((j == k) - (j == k + 1))
                    self.assertEqual(new.by_coordinate[j], expected)
                    self.assertEqual(new.candidate()[j - 1], expected)
                self.assert_changes_and_copies(old, new)

    def test_top_k_duplicate_cutoff_missing_reserve_and_preserving_edit(self):
        for size in Size:
            raw = list(range(99, 91, -1)) + [91, 91, 90] + [0] * (size.numeric_length - 11)
            world = numeric_world(Task.TOP_K, size, raw)
            old = solve_world(world)
            self.assertEqual(old.candidate(), list(range(99, 91, -1)) + [91, 91])
            revised = solve_world(changed_record(world, 0, 0))
            self.assertNotIn(90, old.values)
            self.assertIn(90, revised.values)
            self.assertEqual(revised.values.count(91), 2)
            self.assertEqual(revised.candidate(), list(range(98, 91, -1)) + [91, 91, 90])
            self.assertEqual(changed_coordinates(old, revised).unchanged, frozenset({8}))
            self.assert_changes_and_copies(old, revised)
            preserving = solve_world(changed_record(world, 12, 1))
            self.assertEqual(changed_coordinates(old, preserving).changed, frozenset())
            self.assertEqual(changed_coordinates(old, preserving).unchanged, frozenset(range(10)))
            self.assert_changes_and_copies(old, preserving)
            # A zero cutoff is legal in the unconditioned core; M1-T02 rejects
            # worlds without a legal main edit rather than changing this draw.
            zero_cutoff = numeric_world(Task.TOP_K, size, [99] + [0] * (size.numeric_length - 1))
            self.assertEqual(solve_world(zero_cutoff).values[-1], 0)

    def test_sort_global_rank_crossings_and_distinct_source_ownership(self):
        for size in Size:
            n = size.numeric_length
            original = numeric_world(Task.SORT, size, list(range(n)))
            # Reverse source ownership while keeping output rank ownership fixed.
            world = replace(original, records=tuple(replace(r, owner=3 - r.owner)
                                                    for r in original.records))
            old = solve_world(world)
            new_world = changed_record(world, n - 1, 0)
            new = solve_world(new_world)
            self.assertEqual(new.candidate(), [0] + list(range(n - 1)))
            self.assertEqual(changed_coordinates(old, new).changed, frozenset(range(1, n)))
            self.assertEqual(new_world.records[-1].owner, 0)
            self.assertEqual(coordinate_map(Task.SORT, size).coordinate_peers[n - 1], (3,))
            self.assert_changes_and_copies(old, new)
            # Equal-valued records retain multiplicity, including rank boundaries.
            duplicates = numeric_world(Task.SORT, size, [4, 1, 4, 1] * (n // 4))
            self.assertEqual(solve_world(duplicates).candidate(), [1] * (n // 2) + [4] * (n // 2))

    def test_bfs_preserving_alternatives_longer_paths_and_disconnection(self):
        for size in Size:
            world = star_world(size)
            old = solve_world(world)
            for index, expected_D in ((size.node_count - 1, set()),  # extra edge
                                      (0, {1}),                      # 0-1 has alternate 0-2-1
                                      (size.node_count - 2, {size.node_count - 1})):
                revised = changed_record(world, index, delete=True)
                new = solve_world(revised)
                self.assertEqual(changed_coordinates(old, new).changed, frozenset(expected_D))
                self.assertEqual(new.candidate(), relaxation_distances(size.node_count,
                                                                     [r.value for r in revised.records
                                                                      if not r.deleted]))
                self.assertEqual(revised.records[index].value, world.records[index].value)
                self.assertTrue(revised.records[index].deleted)
                self.assertEqual(revised.records[index].version, 2)
                self.assertEqual(source_manifest(revised), source_manifest(world))
                self.assert_changes_and_copies(old, new)
                if index == size.node_count - 2:
                    self.assertEqual(new.candidate()[str(size.node_count - 1)], -1)
                if index == 0:
                    self.assertEqual(new.candidate()["1"], 2)
                self.assertEqual(new.candidate()["0"], 0)
        diamond = [(0, 1), (0, 2), (1, 3), (2, 3)]
        self.assertEqual(bfs_distances(5, diamond), {"0": 0, "1": 1, "2": 1, "3": 2, "4": -1})
        self.assertEqual(bfs_distances(5, diamond), bfs_distances(5, diamond[:-1]))

    def assert_changes_and_copies(self, old, new):
        changes = changed_coordinates(old, new)
        mapping = coordinate_map(old.task, old.size)
        self.assertFalse(changes.changed & changes.unchanged)
        self.assertEqual(changes.changed | changes.unchanged, frozenset(mapping.coordinates))
        copies = sum(len(changes.changed & set(assigned)) for assigned in mapping.peer_coordinates)
        multiplier = 1 if old.task in (Task.PREFIX, Task.SORT) else 4
        self.assertEqual(copies, multiplier * len(changes.changed))
        for peer in PEERS:
            self.assertTrue(exact_candidate(new, new.candidate(peer), peer))

    def test_record_order_is_not_output_order_and_updates_do_not_repair_candidates(self):
        for size, task in itertools.product(Size, Task):
            world = generated(task, size)
            truth = solve_world(world)
            retained = truth.candidate(1)
            if isinstance(retained, list):
                retained[0] = -12345
            else:
                retained["0"] = -12345
            snapshot = copy.deepcopy(retained)
            reversed_world = replace(world, records=tuple(reversed(world.records)))
            self.assertEqual(truth, solve_world(reversed_world))
            self.assertEqual(source_manifest(world), source_manifest(reversed_world))
            self.assertEqual(changed_coordinates(truth, solve_world(world)).changed, frozenset())
            record = world.records[0]
            revised = (changed_record(world, 0, delete=True) if task is Task.BFS else
                       changed_record(world, 0, 1 if record.value != 1 else 2))
            solve_world(revised)
            self.assertEqual(retained, snapshot)
            self.assertEqual(world.records[0].version, 1)
            self.assertEqual(truth, solve_world(world))
            with self.assertRaises(FrozenInstanceError):
                world.records[0].version = 3
        with self.assertRaises(ValueError):
            changed_coordinates(solve_world(generated(Task.TOP_K)),
                                solve_world(generated(Task.SORT)))
        with self.assertRaises(ValueError):
            changed_coordinates(solve_world(generated(Task.BFS)),
                                solve_world(generated(Task.BFS, Size.FALLBACK)))


class CandidateContractTests(unittest.TestCase):
    def test_output_lengths_keys_assignments_and_inverse_maps(self):
        for size, task in itertools.product(Size, Task):
            expected = (10 if task is Task.TOP_K else size.numeric_length - 1
                        if task is Task.DIFFERENCE else size.node_count
                        if task is Task.BFS else size.numeric_length)
            mapping = coordinate_map(task, size)
            self.assertEqual(len(mapping.coordinates), expected)
            self.assertEqual(len(candidate_contract(task, size).coordinates), expected)
            for peer in PEERS:
                coords = candidate_contract(task, size, peer).coordinates
                self.assertEqual(len(coords), size.shard_size if task in (Task.PREFIX, Task.SORT) else expected)
                for j in coords:
                    self.assertIn(peer, mapping.coordinate_peers[j])
            if task is Task.DIFFERENCE:
                self.assertEqual(mapping.coordinates, tuple(range(1, size.numeric_length)))
            else:
                self.assertEqual(mapping.coordinates, tuple(range(expected)))
            if task in (Task.PREFIX, Task.SORT):
                self.assertEqual(tuple(j for assigned in mapping.peer_coordinates for j in assigned),
                                 mapping.coordinates)
            else:
                self.assertEqual(mapping.peer_coordinates, (mapping.coordinates,) * 4)

    def test_numeric_strict_types_lengths_order_multiplicity_and_reply_validity(self):
        for size, task in itertools.product(Size, (Task.TOP_K, Task.PREFIX, Task.DIFFERENCE, Task.SORT)):
            truth = solve_world(generated(task, size))
            for peer in (None, *PEERS):
                contract, valid = candidate_contract(task, size, peer), truth.candidate(peer)
                for invalid in (None, {}, tuple(valid), valid[:-1], valid + [0]):
                    self.assertIsNotNone(contract.error(invalid))
                    self.assertFalse(exact_candidate(truth, invalid, peer))
                for bad in (True, False, 1.0, "1", None, float("inf"), float("nan"), [], {}):
                    invalid = valid[:]
                    invalid[0] = bad
                    self.assertEqual(contract.error(invalid), "candidate_integer_required")
                    self.assertFalse(exact_candidate(truth, invalid, peer))
                wrong = valid[:]
                wrong[0] += 1
                self.assertIsNone(contract.error(wrong))
                self.assertFalse(exact_candidate(truth, wrong, peer))
                self.assertFalse(exact_candidate(truth, valid, peer, protocol_valid=False))
            if task in (Task.PREFIX, Task.SORT):
                self.assertEqual(candidate_contract(task, size, 0).error(truth.candidate()), "candidate_length")
                self.assertEqual(candidate_contract(task, size).error(truth.candidate(0)), "candidate_length")
        raw = [99, 98, 97, 96, 95, 94, 93, 92, 91, 91] + [0] * 22
        truth = solve_world(numeric_world(Task.TOP_K, Size.TARGET, raw))
        swapped = truth.candidate()
        swapped[0], swapped[1] = swapped[1], swapped[0]
        self.assertFalse(exact_candidate(truth, swapped))
        deduplicated = list(dict.fromkeys(truth.candidate()))
        self.assertFalse(exact_candidate(truth, deduplicated))
        wrong_multiplicity = truth.candidate()
        wrong_multiplicity[-2] = 92
        self.assertEqual(set(wrong_multiplicity), set(truth.candidate()))
        self.assertEqual(len(wrong_multiplicity), len(truth.candidate()))
        self.assertIsNone(candidate_contract(Task.TOP_K, Size.TARGET).error(wrong_multiplicity))
        self.assertFalse(exact_candidate(truth, wrong_multiplicity))

    def test_bfs_exact_canonical_keys_and_unreachable_integers(self):
        for size in Size:
            world = star_world(size)
            truth = solve_world(changed_record(world, size.node_count - 2, delete=True))
            contract = candidate_contract(Task.BFS, size)
            valid = truth.candidate()
            self.assertTrue(exact_candidate(truth, dict(reversed(list(valid.items())))))
            for key in ("00", "01", "-0", "0.0", " 0", 0, size.node_count, str(size.node_count)):
                invalid = {key: valid["0"], **{k: v for k, v in valid.items() if k != "0"}}
                self.assertEqual(contract.error(invalid), "candidate_node_keys")
                self.assertFalse(exact_candidate(truth, invalid))
            for invalid in (valid | {str(size.node_count): 0}, {"0": 0}, list(valid.values())):
                self.assertIsNotNone(contract.error(invalid))
            for bad in (True, -1.0, "-1", None):
                invalid = valid | {str(size.node_count - 1): bad}
                self.assertEqual(contract.error(invalid), "candidate_integer_required")
            wrong = valid | {"0": 1}
            self.assertIsNone(contract.error(wrong))
            self.assertFalse(exact_candidate(truth, wrong))

    def test_undeclared_sizes_tasks_peers_and_malformed_truth_rejected(self):
        for size in (8, 6, "tiny", "target", None, True):
            with self.assertRaises(ValueError):
                coordinate_map(Task.PREFIX, size)
        for task in ("global_max", "top_k", None):
            with self.assertRaises(ValueError):
                coordinate_map(task, Size.TARGET)
        for peer in (-1, 4, True, 0.0, "0"):
            with self.assertRaises(ValueError):
                candidate_contract(Task.BFS, Size.TARGET, peer)
        for values in ([0] * 10, (0,) * 9, (True,) * 10):
            with self.assertRaises(ValueError):
                Truth(Task.TOP_K, Size.TARGET, values)


if __name__ == "__main__":
    unittest.main()
