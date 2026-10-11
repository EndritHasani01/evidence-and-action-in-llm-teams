"""Independent course population checks; no model or protocol acceptance (§11)."""

from collections import Counter
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
from random import Random
import random
import tempfile
import unittest
from unittest.mock import patch

from recovery.manifests import assert_matches, load_population, manifest_bytes, save_population
from recovery.populations import (PARTITIONS, PopulationExhausted, owner_order, prepare_population,
                                  prepare_world, streams_for, validate_population)
from recovery.tasks import PEERS, Size, Task, candidate_contract, source_manifest
from tests.test_populations import independent_answer, seed_values
from tests.test_tasks import numeric_world

ROOT = Path(__file__).resolve().parent.parent
COURSE_SEED = 20261009


class CourseInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.population = prepare_population(COURSE_SEED, Size.FALLBACK, regime="course")

    def test_exact_cohorts_owner_block_shapes_and_independent_edit_truth(self):
        p = self.population
        validate_population(p)
        self.assertEqual((p.regime, p.size, len(p.main), len(p.development)),
                         ("course", Size.FALLBACK, 20, 5))
        self.assertEqual(p.main_counts, (20,))
        self.assertEqual(p.worlds(), p.worlds(20))
        self.assertEqual(p.worlds(), p.main)
        expected = dict(main=tuple(w.world_id for w in p.main),
            receipt=tuple(w.world_id for w in p.main if w.world.task in (Task.PREFIX, Task.SORT)),
            q=tuple(w.world_id for w in p.main if w.world.task in (Task.SORT, Task.BFS)),
            preserving=tuple(w.world_id for w in p.main if w.world.task in (Task.TOP_K, Task.BFS)),
            repeat=tuple(w.world_id for w in p.main if w.index == 1))
        self.assertEqual(p.subsets(), expected)
        self.assertEqual({k: len(v) for k, v in expected.items()},
                         dict(main=20, receipt=8, q=8, preserving=8, repeat=5))
        self.assertEqual({w.world.task for w in p.development}, set(Task))
        for task in Task:
            family = [w for w in p.main if w.world.task is task]
            self.assertEqual(Counter(w.edited_owner for w in family), Counter(PEERS))
            rng = Random(COURSE_SEED * 2**20 + 1 + tuple(Task).index(task))
            owners = list(PEERS)
            rng.shuffle(owners)
            self.assertEqual([w.edited_owner for w in family], owners)
            self.assertEqual(owner_order(COURSE_SEED, task, regime="course"), tuple(owners))
        for w in p.main + p.development:
            with self.subTest(world=w.world_id):
                original = independent_answer(w.world)
                self.assertNotEqual(independent_answer(w.event_world("revision")), original)
                self.assertIs(w.event_world("sham"), w.world)
                edited = next(r for r in w.world.records if r.record_id == w.main_edit.record_id)
                self.assertEqual(edited.owner, w.edited_owner)
                if w.world.task in (Task.TOP_K, Task.BFS):
                    self.assertEqual(independent_answer(w.event_world("preserving")), original)
                    self.assertGreater(w.eligibility.preserving_pairs, 0)
                else:
                    self.assertIsNone(w.preserving_edit)
                self.assertEqual(len(w.world.records), 12 if w.world.task is Task.BFS else 24)
                lengths = (10 if w.world.task is Task.TOP_K else
                           8 if w.world.task is Task.BFS else
                           23 if w.world.task is Task.DIFFERENCE else 24)
                self.assertEqual(len(candidate_contract(w.world.task, p.size, None).coordinates), lengths)
                for peer in PEERS:
                    contract = candidate_contract(w.world.task, p.size, peer)
                    self.assertEqual(len(contract.coordinates), 6 if w.world.task in (Task.PREFIX, Task.SORT)
                                     else lengths)
                    if w.world.task is Task.BFS:
                        self.assertEqual(contract.coordinates, tuple(range(8)))
                    if w.world.task is Task.DIFFERENCE:
                        self.assertEqual(contract.coordinates, tuple(range(1, 24)))
                self.assertEqual(w.partition, Random(w.streams.partition).choice(PARTITIONS))
                self.assertIn(0, w.partition[0])
                public = source_manifest(w.world)
                self.assertEqual(set(asdict(public[0])), {"record_id", "owner", "position"})
        self.assertTrue(set(w.partition for w in p.main + p.development) <= set(PARTITIONS))
        for count in (60, 40, 0, True, 20.0):
            with self.assertRaises(ValueError):
                p.worlds(count)

    def test_independent_seed_slots_and_separation_from_actual_thesis_inputs(self):
        p = self.population
        course_seeds = set(p.owner_seeds + p.development_owner_seeds)
        self.assertEqual(p.owner_seeds, tuple(COURSE_SEED * 2**20 + 1 + i for i in range(5)))
        self.assertEqual(p.development_owner_seeds, tuple(COURSE_SEED * 2**20 + 6 + i for i in range(5)))
        all_world_seeds = []
        for w in p.main + p.development:
            family = tuple(Task).index(w.world.task)
            slot = 60 + family if w.development else family * 12 + w.index - 1
            base = COURSE_SEED * 2**20 + (slot + 1) * 4096
            s = w.streams
            self.assertEqual((s.generation, s.ownership, s.main_edit, s.preserving_edit, s.partition),
                             tuple(base + offset for offset in range(5)))
            self.assertEqual(s.controls, (base + 64, base + 65))
            self.assertEqual(s.prefix, tuple(tuple(base + 16 + r * 4 + peer for peer in PEERS)
                                             for r in range(4)))
            replicates = 2 if not w.development and w.index == 1 else 1
            self.assertEqual(s.continuation, tuple(tuple(tuple(base + 32 + k * 16 + r * 4 + peer
                for peer in PEERS) for r in range(4)) for k in range(replicates)))
            with self.assertRaises(ValueError):
                s.continuation_seed(replicates, 1, 0)
            all_world_seeds.extend(seed_values(s))
        self.assertEqual(len(all_world_seeds), len(set(all_world_seeds)))
        self.assertTrue(course_seeds.isdisjoint(all_world_seeds))
        main = {s for w in p.main for s in seed_values(w.streams)}
        dev = {s for w in p.development for s in seed_values(w.streams)}
        self.assertEqual((len(main), len(dev)), (860, 195))
        self.assertTrue(main.isdisjoint(dev))
        course_seeds.update(all_world_seeds)
        for size in Size:
            thesis = load_population(ROOT / f"tests/fixtures/population_{size.value}.json")
            thesis_seeds = set(thesis.owner_seeds + thesis.development_owner_seeds)
            thesis_seeds.update(s for w in thesis.main + thesis.development for s in seed_values(w.streams))
            self.assertTrue(course_seeds.isdisjoint(thesis_seeds))
            self.assertNotEqual(p.master_seed, thesis.master_seed)
        self.assertEqual(len(course_seeds), 1065)

    def test_repreparation_order_and_unrelated_random_draws_do_not_change_inputs(self):
        p = self.population
        state = random.getstate()
        for w in reversed(p.main + p.development):
            Random(w.streams.main_edit).randbytes(100)
            Random(w.streams.partition).randbytes(100)
            self.assertEqual(prepare_world(p.master_seed, w.world.task, p.size, w.index, w.edited_owner,
                development=w.development, regime="course"), w)
        self.assertEqual(random.getstate(), state)

    def test_course_reuses_the_thousand_attempt_limit_and_records_fixed_owner(self):
        impossible = numeric_world(Task.TOP_K, Size.FALLBACK, [99] + [0] * 23)
        with patch("recovery.populations.generate_world", return_value=impossible) as generate:
            with self.assertRaises(PopulationExhausted) as caught:
                prepare_world(COURSE_SEED, Task.TOP_K, Size.FALLBACK, 1, 3, regime="course")
        self.assertEqual(generate.call_count, 1000)
        self.assertEqual((caught.exception.world_id, caught.exception.owner), ("main-top_k-01", 3))
        self.assertEqual([r.attempt for r in caught.exception.rejections], list(range(1, 1001)))
        self.assertTrue(all(r.reasons == ("no_owner_changing_edit", "no_preserving_edit")
                            for r in caught.exception.rejections))

    def test_saved_course_round_trip_has_explicit_scope_and_never_resamples_or_overwrites(self):
        p = self.population
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "population.json"
            save_population(p, path)
            payload = path.read_bytes()
            self.assertEqual(json.loads(payload)["regime"], "course")
            with patch("recovery.populations.generate_world", side_effect=AssertionError("resampled")):
                self.assertEqual(load_population(path, authoritative=p), p)
            self.assertEqual(payload, manifest_bytes(p))
            with self.assertRaises(FileExistsError):
                save_population(p, path)
            self.assertEqual(path.read_bytes(), payload)
            # A valid edit to an unselected Prefix operand still needs exact authority comparison.
            w = next(w for w in p.main if w.world.task is Task.PREFIX)
            record = next(r for r in w.world.records if r.record_id != w.main_edit.record_id)
            world = replace(w.world, records=tuple(replace(r, value=9 if r.value != 9 else 1)
                if r == record else r for r in w.world.records))
            changed = replace(p, main=tuple(replace(item, world=world) if item == w else item for item in p.main))
            validate_population(changed)
            with self.assertRaisesRegex(ValueError, "authoritative manifest"):
                assert_matches(changed, p)

    def test_course_rejects_missing_scope_changed_configuration_and_unassigned_replicates(self):
        p = self.population
        baseline = json.loads(manifest_bytes(p))
        mutations = [lambda d: d.pop("regime"), lambda d: d.update(regime="thesis"),
            lambda d: d.update(regime=True), lambda d: d.update(regime="future"),
            lambda d: d.update(size="target"), lambda d: d["main"].pop(),
            lambda d: d["development"].pop(), lambda d: d["main"][0].update(edited_owner=3 - d["main"][0]["edited_owner"]),
            lambda d: d["main"][1]["streams"]["continuation"].append(d["main"][0]["streams"]["continuation"][1]),
            lambda d: d["main"][0]["streams"]["continuation"].pop(),
            lambda d: d["main"][0]["streams"].update(generation=float(d["main"][0]["streams"]["generation"])),
            lambda d: d["main"][0]["main_edit"].update(replacement=-1),
            lambda d: d["main"][0].update(partition=[[1, 0], [2, 3]])]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for i, mutate in enumerate(mutations):
                with self.subTest(mutation=i):
                    data = deepcopy(baseline)
                    mutate(data)
                    path.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_population(path)
        for invalid in ("other", True, None):
            with self.assertRaises(ValueError):
                prepare_population(COURSE_SEED, Size.FALLBACK, regime=invalid)
        with self.assertRaises(ValueError):
            prepare_population(COURSE_SEED, Size.TARGET, regime="course")
        with self.assertRaises(ValueError):
            streams_for(COURSE_SEED, Task.PREFIX, 5, regime="course")


if __name__ == "__main__":
    unittest.main()
