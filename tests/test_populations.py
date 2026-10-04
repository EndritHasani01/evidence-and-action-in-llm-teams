from collections import Counter
from dataclasses import FrozenInstanceError, asdict, replace
import json
import os
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.manifests import assert_matches, load_population, manifest_bytes, save_population
from recovery.populations import (MAX_ATTEMPTS, PARTITIONS, PopulationExhausted,
                                  draw_partition, owner_order, owner_seed, prepare_population,
                                  prepare_world, validate_population)
from recovery.tasks import PEERS, Size, Task, source_manifest
from tests.references import numeric_reference, relaxation_distances
from tests.test_edits import BoundaryChoices
from tests.test_tasks import numeric_world
from tests.test_truth_contracts import star_world

ROOT = Path(__file__).resolve().parent.parent


def seed_values(streams):
    result = [streams.generation, streams.ownership, streams.main_edit,
              streams.preserving_edit, streams.partition, *streams.controls]
    result += [s for row in streams.prefix for s in row]
    result += [s for repeat in streams.continuation for row in repeat for s in row]
    return result


def independent_answer(world):
    if world.task is Task.BFS:
        return relaxation_distances(world.size.node_count,
                                    [r.value for r in world.records if not r.deleted])
    return numeric_reference(world.task.value,
                             [r.value for r in sorted(world.records, key=lambda r: r.position)])


class PopulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.populations = {size: prepare_population(20261004, size) for size in Size}

    def test_all_populations_edit_truth_subsets_owner_balance_and_nesting(self):
        for size, p in self.populations.items():
            validate_population(p)
            self.assertEqual((len(p.main), len(p.development)), (60, 5))
            self.assertEqual(len({w.world_id for w in p.main + p.development}), 65)
            self.assertTrue({w.world_id for w in p.main}.isdisjoint(w.world_id for w in p.development))
            self.assertEqual({w.world.task for w in p.development}, set(Task))
            for count in (60, 40):
                subsets = p.subsets(count)
                self.assertEqual({k: len(v) for k, v in subsets.items()},
                                 dict(main=count, receipt=2 * count // 5, q=2 * count // 5,
                                      preserving=16, repeat=10))
                worlds = p.worlds(count)
                for task in Task:
                    family = [w for w in worlds if w.world.task is task]
                    self.assertEqual(len(family), count // 5)
                    self.assertEqual(Counter(w.edited_owner for w in family),
                                     Counter({peer: count // 20 for peer in PEERS}))
                    for start in range(0, len(family), 4):
                        self.assertEqual({w.edited_owner for w in family[start:start + 4]}, set(PEERS))
                overlap = set(subsets["receipt"]) & set(subsets["q"])
                self.assertEqual(overlap, {w.world_id for w in worlds if w.world.task is Task.SORT})
                self.assertEqual(subsets["preserving"], p.subsets(60)["preserving"])
                self.assertEqual(subsets["repeat"], p.subsets(60)["repeat"])
            self.assertEqual(p.worlds(40), tuple(w for w in p.main if w.index <= 8))
            for w in p.main + p.development:
                with self.subTest(size=size, world=w.world_id):
                    owner = next(r.owner for r in w.world.records if r.record_id == w.main_edit.record_id)
                    self.assertEqual(owner, w.edited_owner)
                    old = independent_answer(w.world)
                    self.assertNotEqual(independent_answer(w.event_world("revision")), old)
                    self.assertIs(w.event_world("sham"), w.world)
                    self.assertEqual(source_manifest(w.event_world("revision")), source_manifest(w.world))
                    if w.world.task in (Task.TOP_K, Task.BFS):
                        self.assertIsNotNone(w.preserving_edit)
                        self.assertGreater(w.eligibility.preserving_pairs, 0)
                        self.assertEqual(independent_answer(w.event_world("preserving")), old)
                    else:
                        self.assertIsNone(w.preserving_edit)
                        with self.assertRaises(ValueError):
                            w.event_world("preserving")
                    self.assertIn(w.partition, PARTITIONS)
                    self.assertIn(0, w.partition[0])
                    self.assertEqual(set(w.partition[0]) | set(w.partition[1]), set(PEERS))
                    with self.assertRaises(FrozenInstanceError):
                        w.edited_owner = 0
            for task in (Task.TOP_K, Task.BFS):
                preserving_worlds = [w for w in p.main if w.world.task is task]
                self.assertTrue(any(next(r.owner for r in w.world.records
                                         if r.record_id == w.preserving_edit.record_id) != w.edited_owner
                                    for w in preserving_worlds))
            for invalid in (0, 8, 59, 61, True, 60.0):
                with self.assertRaises(ValueError):
                    p.worlds(invalid)

    def test_uniform_partition_domains_and_fixed_owner_orders(self):
        for i, expected in enumerate(PARTITIONS):
            rng = BoundaryChoices(i)
            self.assertEqual(draw_partition(rng), expected)
            self.assertEqual(rng.domains, [PARTITIONS])
        for task in Task:
            # Independent shuffle reconstruction; order exists before world draws.
            rng = Random(owner_seed(20261004, task))
            expected = []
            for _ in range(3):
                block = list(PEERS)
                rng.shuffle(block)
                expected.extend(block)
            self.assertEqual(owner_order(20261004, task), tuple(expected))

    def test_unique_disjoint_streams_matched_siblings_and_repeat_prefix(self):
        for p in self.populations.values():
            main = {s for w in p.main for s in seed_values(w.streams)}
            dev = {s for w in p.development for s in seed_values(w.streams)}
            owner_seeds = set(p.owner_seeds + p.development_owner_seeds)
            self.assertTrue(main.isdisjoint(dev))
            self.assertTrue((main | dev).isdisjoint(owner_seeds))
            all_values = [s for w in p.main + p.development for s in seed_values(w.streams)]
            self.assertEqual(len(all_values), len(set(all_values)))
            for w in p.main + p.development:
                streams = w.streams
                repeated = not w.development and w.index <= 2
                self.assertEqual(len(streams.continuation), 2 if repeated else 1)
                for round_number in range(1, 5):
                    for peer in PEERS:
                        siblings = [streams.continuation_seed(0, round_number, peer)
                                    for _ in ("B/revision", "C/sham", "P_G", "Q_C")]
                        self.assertEqual(len(set(siblings)), 1)
                        self.assertNotEqual(siblings[0], streams.prefix_seed(round_number, peer))
                        if repeated:
                            self.assertNotEqual(siblings[0], streams.continuation_seed(1, round_number, peer))
                        else:
                            with self.assertRaises(ValueError):
                                streams.continuation_seed(1, round_number, peer)
                for round_number, peer in ((0, 0), (5, 1), (1, 4), (True, 0), (1, True)):
                    with self.assertRaises(ValueError):
                        streams.prefix_seed(round_number, peer)

    def test_reordering_and_unrelated_stream_consumption_cannot_shift_worlds(self):
        for size, p in self.populations.items():
            unrelated = Random(901)
            for w in reversed(p.main + p.development):
                unrelated.random()
                # Consuming local edit/partition RNGs has no effect on a keyed re-preparation.
                Random(w.streams.main_edit).randbytes(100)
                Random(w.streams.partition).randbytes(100)
                actual = prepare_world(p.master_seed, w.world.task, size, w.index,
                                       w.edited_owner, development=w.development)
                self.assertEqual(actual, w)

    def test_rejection_reasons_owner_fixed_and_explicit_thousand_attempt_exhaustion(self):
        for size in Size:
            zero = numeric_world(Task.TOP_K, size, [99] + [0] * (size.numeric_length - 1))
            with patch("recovery.populations.generate_world", return_value=zero) as generate:
                with self.assertRaises(PopulationExhausted) as caught:
                    prepare_world(1, Task.TOP_K, size, 1, 3)
                failure = caught.exception
                self.assertEqual(generate.call_count, 1000)
                self.assertEqual((failure.world_id, failure.owner), ("main-top_k-01", 3))
                self.assertEqual([r.attempt for r in failure.rejections], list(range(1, 1001)))
                self.assertTrue(all(r.reasons == ("no_owner_changing_edit", "no_preserving_edit")
                                    for r in failure.rejections))
            valid = numeric_world(Task.TOP_K, size,
                                  list(range(99, 89, -1)) + [0] * (size.numeric_length - 10))
            # Main is possible for owner 0 but owner 3 is fixed: never switch it.
            owner_only = numeric_world(Task.TOP_K, size, [0] * (size.numeric_length - 10)
                                       + list(range(99, 89, -1)))
            with patch("recovery.populations.generate_world", side_effect=[owner_only, valid]):
                w = prepare_world(1, Task.TOP_K, size, 1, 0)
                self.assertEqual(w.attempts, 2)
                self.assertEqual(w.rejections[0].reasons, ("no_owner_changing_edit",))
            no_preserving = numeric_world(Task.TOP_K, size,
                                         list(range(99, 89, -1)) + [90] * (size.numeric_length - 10))
            with patch("recovery.populations.generate_world", side_effect=[no_preserving] * 999 + [valid]):
                w = prepare_world(1, Task.TOP_K, size, 1, 0)
                self.assertEqual(w.attempts, MAX_ATTEMPTS)
                self.assertTrue(all(r.reasons == ("no_preserving_edit",) for r in w.rejections))

    def test_bfs_rejects_fixed_owner_without_changing_edge(self):
        for size in Size:
            graph = star_world(size)  # Owner 3 holds only distance-redundant extra edges.
            with patch("recovery.populations.generate_world", return_value=graph) as generate:
                with self.assertRaises(PopulationExhausted) as caught:
                    prepare_world(1, Task.BFS, size, 1, 3)
                self.assertEqual(generate.call_count, 1000)
                self.assertTrue(all(r.reasons == ("no_owner_changing_edit",)
                                    for r in caught.exception.rejections))

    def test_multiple_roots_and_saved_configuration_regenerate_byte_stably(self):
        for size, original in self.populations.items():
            for seed in (0, 7, original.master_seed):
                p = prepare_population(seed, size)
                validate_population(p)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "population.json"
                    save_population(p, path)
                    # Loading is actual-record deserialization, not resampling.
                    with patch("recovery.populations.generate_world", side_effect=AssertionError("resampled")):
                        loaded = load_population(path)
                    self.assertEqual(loaded, p)
                    self.assertEqual(path.read_bytes(), manifest_bytes(loaded))
                    regenerated = prepare_population(loaded.master_seed, loaded.size)
                    self.assertEqual(manifest_bytes(regenerated), path.read_bytes())
                    with self.assertRaises(FileExistsError):
                        save_population(p, path)

    def test_retained_host_fixtures_reload_and_regenerate_without_evaluator_fields(self):
        for size, p in self.populations.items():
            path = ROOT / "tests" / "fixtures" / f"population_{size.value}.json"
            loaded = load_population(path, authoritative=p)
            self.assertEqual(path.read_bytes(), manifest_bytes(loaded))
            data = json.loads(path.read_bytes())
            self.assertEqual(set(data), {"format_version", "master_seed", "size", "owner_seeds",
                                         "development_owner_seeds", "main", "development"})
            for w in loaded.main + loaded.development:
                # Only the public source identity projection is suitable for peer metadata.
                public = source_manifest(w.world)
                self.assertEqual(set(asdict(public[0])), {"record_id", "owner", "position"})
            def fields(value):
                if isinstance(value, dict):
                    for key, nested in value.items():
                        yield key
                        yield from fields(nested)
                elif isinstance(value, (list, tuple)):
                    for nested in value:
                        yield from fields(nested)
            self.assertTrue(set(fields(data)).isdisjoint({"gold", "truth", "footprints", "changed",
                                                         "unchanged", "correctness", "candidate"}))

    def test_authoritative_comparison_detects_changed_but_mathematically_valid_inputs(self):
        for p in self.populations.values():
            # A Prefix edit at another position remains valid with unchanged selection,
            # seeds/ownership/eligibility; only saved input equality detects tampering.
            w = next(w for w in p.main if w.world.task is Task.PREFIX)
            source = next(r for r in w.world.records if r.record_id != w.main_edit.record_id)
            modified_world = replace(w.world, records=tuple(replace(r, value=9 if r.value != 9 else 1)
                                                           if r == source else r for r in w.world.records))
            modified = replace(p, main=tuple(replace(item, world=modified_world) if item == w else item
                                             for item in p.main))
            validate_population(modified)
            with self.assertRaisesRegex(ValueError, "authoritative manifest"):
                assert_matches(modified, p)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "modified.json"
                path.write_bytes(manifest_bytes(modified))
                with self.assertRaisesRegex(ValueError, "authoritative manifest"):
                    load_population(path, authoritative=p)
            assert_matches(p, p)

    def test_structural_and_scientific_manifest_mutations_rejected(self):
        p = self.populations[Size.TARGET]
        mutations = [
            lambda d: d.update(format_version=True),
            lambda d: d.update(format_version=2),
            lambda d: d.update(master_seed=-1),
            lambda d: d.update(main=d["main"][:-1]),
            lambda d: d.update(size="tiny"),
            lambda d: d.update(extra="unexpected"),
            lambda d: d["main"][0].update(edited_owner=True),
            lambda d: d["main"][0].update(index=True),
            lambda d: d["main"][0].update(development=0),
            lambda d: d["main"][0]["streams"].update(generation=float(d["main"][0]["streams"]["generation"])),
            lambda d: d["main"][0]["streams"].update(partition=0),
            lambda d: d["main"][0].update(partition=((0, 0), (1, 2))),
            lambda d: d["main"][0]["world"].update(gold=[1]),
            lambda d: d["main"][0]["eligibility"].update(extra="unexpected"),
            lambda d: d["main"][0]["main_edit"].update(record_id="unknown"),
            lambda d: d["main"][0].update(rejections=[dict(attempt=2, reasons=["no_owner_changing_edit"])]),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for mutate in mutations:
                data = asdict(p)
                mutate(data)
                path.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError, msg=str(mutate)):
                    load_population(path)
            for malformed in ('{"format_version":1,"format_version":1}', '{"x":NaN}',
                              '[]', '{}', 'true', 'null', '"text"', '{'):
                path.write_text(malformed, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_population(path)

    def test_process_hashing_global_rng_and_optional_dependencies_do_not_affect_preparation(self):
        p = self.populations[Size.FALLBACK]
        script = '''
import importlib.abc
import random
import sys
blocked = {"torch", "transformers", "accelerate", "bitsandbytes", "langgraph",
           "langchain", "numpy", "scipy", "pandas", "matplotlib", "pydantic"}
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("unexpected dependency import: " + fullname)
sys.meta_path.insert(0, BlockImports())
state = random.getstate()
from recovery.populations import prepare_population
from recovery.manifests import manifest_bytes
from recovery.tasks import Size
p = prepare_population(20261004, Size.FALLBACK)
assert random.getstate() == state
assert not any(name.split(".")[0] in blocked for name in sys.modules)
sys.stdout.buffer.write(manifest_bytes(p))
'''
        for hash_seed in ("1", "3981"):
            result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT,
                                    env=dict(os.environ, PYTHONHASHSEED=hash_seed),
                                    capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(result.stdout, manifest_bytes(p))


if __name__ == "__main__":
    unittest.main()
