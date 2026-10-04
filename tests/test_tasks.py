import itertools
import json
from dataclasses import asdict, replace
from pathlib import Path
import random
import unittest

from recovery.tasks import (PEERS, Size, SourceRecord, Task, World, _prufer_tree,
                            candidate_contract, coordinate_map, generate_world,
                            numeric_range, source_manifest)
from recovery.truth import (bfs_distances, changed_coordinates, differences,
                            exact_candidate, prefix_sums, solve_world,
                            sorted_values, top_k)
from tests.references import numeric_reference, relaxation_distances


def generated(task, size=Size.TARGET, seed=0, owner_seed=1):
    return generate_world(task, size, generation_rng=random.Random(seed),
                          ownership_rng=random.Random(owner_seed))


def numeric_world(task, size, values):
    return World(task, size, tuple(SourceRecord(f"x{j:03d}", j // size.shard_size,
                                               j, value)
                                   for j, value in enumerate(values)))


def changed_record(world, index, value=None, *, delete=False):
    record = world.records[index]
    revised = replace(record, version=record.version + 1, deleted=delete,
                      value=record.value if delete else value)
    return replace(world, records=world.records[:index] + (revised,) + world.records[index + 1:])


class GeneratedWorldTests(unittest.TestCase):
    def test_all_families_both_sizes_independent_truth_and_contracts(self):
        # 1,000 deterministic draws, no population conditioning or inference.
        for size, task, seed in itertools.product(Size, Task, range(100)):
            with self.subTest(size=size, task=task, seed=seed):
                world = generated(task, size, seed, seed + 1000)
                truth = solve_world(world)
                if task is Task.BFS:
                    expected = relaxation_distances(size.node_count,
                                                    [r.value for r in world.records])
                    self.assertTrue(all(d >= 0 for d in expected.values()))
                    self.assertEqual(len(world.records), size.edge_count)
                    self.assertEqual(len(set(r.value for r in world.records)), size.edge_count)
                    self.assertTrue(all(r.position is None for r in world.records))
                else:
                    raw = [r.value for r in sorted(world.records, key=lambda r: r.position)]
                    expected = numeric_reference(task.value, raw)
                    self.assertEqual(len(raw), size.numeric_length)
                    low, high = numeric_range(task)
                    self.assertTrue(all(low <= value <= high for value in raw))
                self.assertEqual(truth.candidate(), expected)
                mapping = coordinate_map(task, size)
                self.assertEqual(set(mapping.coordinate_peers), set(mapping.coordinates))
                for peer in PEERS:
                    count = size.edge_count // 4 if task is Task.BFS else size.shard_size
                    self.assertEqual(sum(r.owner == peer for r in world.records), count)
                    contract = candidate_contract(task, size, peer)
                    self.assertEqual(contract.coordinates, mapping.peer_coordinates[peer])
                    candidate = truth.candidate(peer)
                    self.assertIsNone(contract.error(candidate))
                    self.assertTrue(exact_candidate(truth, candidate, peer))
                    if task in (Task.PREFIX, Task.SORT):
                        m = size.shard_size
                        self.assertEqual(candidate, expected[peer * m:(peer + 1) * m])
                    else:
                        self.assertEqual(candidate, expected)

    def test_reproducibility_and_unrelated_random_streams(self):
        global_state = random.getstate()
        other = random.Random(888)
        other_state = other.getstate()
        for task in Task:
            for size in Size:
                world = generated(task, size)
                self.assertEqual(world, generated(task, size))
                encoded = json.dumps(asdict(world), sort_keys=True)
                self.assertEqual(encoded, json.dumps(asdict(generated(task, size)), sort_keys=True))
        self.assertEqual(random.getstate(), global_state)
        self.assertEqual(other.getstate(), other_state)
        stream = random.Random(2)
        with self.assertRaises(ValueError):
            generate_world(Task.SORT, Size.TARGET, generation_rng=stream, ownership_rng=stream)

    def test_ids_and_source_ownership_do_not_depend_on_values(self):
        for size in Size:
            for task in Task:
                first, second = generated(task, size, 1, 99), generated(task, size, 2, 99)
                self.assertEqual(source_manifest(first), source_manifest(second))
                for public in source_manifest(first):
                    self.assertEqual(set(asdict(public)), {"record_id", "owner", "position"})
            for task in (Task.TOP_K, Task.SORT):
                first, second = generated(task, size, 5, 10), generated(task, size, 5, 11)
                self.assertEqual([r.value for r in first.records], [r.value for r in second.records])
                self.assertNotEqual([r.owner for r in first.records], [r.owner for r in second.records])
            first, second = generated(Task.BFS, size, 5, 10), generated(Task.BFS, size, 5, 11)
            self.assertEqual({r.value for r in first.records}, {r.value for r in second.records})
            self.assertNotEqual([r.value for r in first.records], [r.value for r in second.records])
            self.assertNotEqual([r.value for r in first.records], sorted(r.value for r in first.records))

    def test_numeric_uniform_inclusive_domains(self):
        class EndpointRandom(random.Random):
            def randint(self, low, high):
                self.calls.append((low, high))
                return high if len(self.calls) % 2 else low

        for size in Size:
            for task in (Task.TOP_K, Task.PREFIX, Task.DIFFERENCE, Task.SORT):
                stream = EndpointRandom(0)
                stream.calls = []
                world = generate_world(task, size, generation_rng=stream,
                                       ownership_rng=random.Random(1))
                low, high = numeric_range(task)
                self.assertEqual(stream.calls, [(low, high)] * size.numeric_length)
                self.assertEqual({r.value for r in world.records}, {low, high})

    def test_prufer_bijection_for_all_four_node_sequences(self):
        class SequenceRandom(random.Random):
            def randrange(self, stop):
                self.assert_stop.append(stop)
                return next(self.labels)

        trees = set()
        for labels in itertools.product(range(4), repeat=2):
            stream = SequenceRandom(0)
            stream.labels, stream.assert_stop = iter(labels), []
            tree = _prufer_tree(4, stream)
            self.assertEqual(stream.assert_stop, [4, 4])
            self.assertEqual(len(tree), 3)
            self.assertTrue(all(d >= 0 for d in relaxation_distances(4, tree).values()))
            trees.add(frozenset(tree))
        self.assertEqual(len(trees), 4 ** (4 - 2))

    def test_bfs_tree_plus_exactly_five_uniform_nonedges(self):
        class SamplingRandom(random.Random):
            def randrange(self, stop):
                self.label_domains.append(stop)
                return super().randrange(stop)

            def sample(self, population, k):
                self.nonedges, self.sample_count = list(population), k
                self.extra = super().sample(population, k)
                return self.extra

        for size in Size:
            stream = SamplingRandom(71)
            stream.label_domains = []
            tree = _prufer_tree(size.node_count, random.Random(71))
            world = generate_world(Task.BFS, size, generation_rng=stream,
                                   ownership_rng=random.Random(23))
            self.assertEqual(stream.label_domains, [size.node_count] * (size.node_count - 2))
            self.assertEqual(stream.nonedges, [e for e in itertools.combinations(range(size.node_count), 2)
                                              if e not in tree])
            self.assertEqual(stream.sample_count, 5)
            self.assertEqual(len(set(stream.extra)), 5)
            self.assertEqual({r.value for r in world.records}, tree | set(stream.extra))


class NativeFixtureTests(unittest.TestCase):
    def test_stored_mathematics_with_independent_references(self):
        fixtures = json.loads((Path(__file__).parent / "fixtures" / "silo_selected.json").read_text())
        self.assertEqual(len(fixtures), 10)
        tasks = {"I-09": Task.TOP_K, "II-11": Task.PREFIX, "II-17": Task.DIFFERENCE,
                 "III-21": Task.SORT, "III-24": Task.BFS}
        for fixture in fixtures:
            with self.subTest(source=fixture["source"]):
                task = tasks[fixture["case_id"]]
                raw = [value for shard in fixture["inputs"] for value in shard]
                expected = fixture["expected"]
                if task is Task.BFS:
                    nodes = len(expected[0])
                    result = bfs_distances(nodes, raw)
                    self.assertEqual(result, relaxation_distances(nodes, raw))
                else:
                    result = {Task.TOP_K: top_k, Task.PREFIX: prefix_sums,
                              Task.DIFFERENCE: differences, Task.SORT: sorted_values}[task](raw)
                    self.assertEqual(result, numeric_reference(task.value, raw))
                if task in (Task.PREFIX, Task.SORT):
                    self.assertEqual(result, [v for segment in expected for v in segment])
                else:
                    self.assertTrue(all(result == gold for gold in expected))

    def test_extracted_inputs_and_gold_equal_attributed_vendor_sources(self):
        root = Path(__file__).resolve().parent.parent
        fixtures = json.loads((root / "tests/fixtures/silo_selected.json").read_text())
        for fixture in fixtures:
            source = json.loads((root / fixture["source"]).read_text())
            self.assertEqual(fixture["case_id"], source["case_id"])
            self.assertEqual(fixture["inputs"], [a["input_shard"] for a in source["agent_configs"]])
            self.assertEqual(fixture["expected"], source["expected_output"]["per_agent_values"])


if __name__ == "__main__":
    unittest.main()
