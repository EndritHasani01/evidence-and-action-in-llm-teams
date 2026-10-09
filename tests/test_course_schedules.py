"""Independent course matrix, parents and saved-schedule adversaries (§11.2)."""

from collections import Counter
from copy import deepcopy
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

from recovery.manifests import (assert_schedules_match, load_population, load_schedules,
                                manifest_bytes, save_schedules, schedule_bytes)
from recovery.populations import prepare_population
from recovery.schedule import (component_counts, dependency_order, iter_calls,
                               prepare_schedules, validate_schedules)
from recovery.tasks import PEERS, Size, Task
from tests.test_course_inputs import COURSE_SEED
from tests.test_schedules import PILOT_TABLE

ROOT = Path(__file__).resolve().parent.parent
MAIN_TABLE = dict(prefix=(320, 320), revised=(1600, 1600), sham=(960, 960),
    masks=(960, 1280), controls=(40, 40), preserving=(384, 384),
    receipts=(384, 384), prose_delay=(384, 512), repeat=(720, 800))


def independent_cells(worlds, development):
    """Declare eligible experimental cells without production schedule helpers."""
    cells = set()
    for w in worlds:
        wid, task = w.world_id, w.world.task
        cells.add((wid, "prefix", "original", None, 0))
        cells.update((wid, "control", event, None, 0) for event in ("original", "revision"))
        cells.update((wid, "continuation", "revision", policy, 0) for policy in ("L", "B", "C", "K", "F"))
        cells.update((wid, "continuation", "sham", policy, 0) for policy in ("B", "C", "K"))
        if not development or task in (Task.PREFIX, Task.BFS):
            cells.update((wid, "continuation", event, policy, 0)
                         for event, policy in product(("revision", "sham"), ("P_G", "P_H")))
        if task in (Task.PREFIX, Task.SORT):
            cells.update((wid, "continuation", "revision", policy, 0)
                         for policy in ("B_delta", "C_delta", "K_delta"))
        if task in (Task.SORT, Task.BFS):
            cells.update((wid, "continuation", event, policy, 0)
                         for event, policy in product(("revision", "sham"), ("Q_B", "Q_C")))
        if task in (Task.TOP_K, Task.BFS):
            cells.update((wid, "continuation", "preserving", policy, 0) for policy in ("B", "C", "K"))
        if not development and w.index == 1:
            cells.update((wid, "continuation", event, policy, 1)
                for event, policy in product(("revision", "sham"), ("B", "C", "K", "P_G", "P_H")))
    return cells


class CourseScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.population = prepare_population(COURSE_SEED, Size.FALLBACK, regime="course")
        cls.schedules = prepare_schedules(cls.population)

    def test_independent_component_counts_cells_and_all_fixed_opportunities(self):
        p, s = self.population, self.schedules
        validate_schedules(s, p)
        self.assertEqual((s.regime, s.size), ("course", Size.FALLBACK))
        self.assertEqual(s.main_for(p), s.main)
        self.assertEqual(s.main_for(p, 20), s.main)
        for branches, worlds, development, table, totals in (
                (s.main, p.main, False, MAIN_TABLE, (5752, 6280, 528)),
                (s.development, p.development, True, PILOT_TABLE, (1114, 1178, 64))):
            cells = [(b.world_id, b.phase, b.event, b.policy, b.replicate) for b in branches]
            self.assertEqual(set(cells), independent_cells(worlds, development))
            self.assertEqual(len(cells), len(set(cells)))
            self.assertEqual(component_counts(branches), table)
            calls = [c for _, c in iter_calls(branches)]
            self.assertEqual((len({c.generation_id for c in calls}), len(calls),
                              sum(c.replay_parent is not None for c in calls)), totals)
            self.assertEqual(len({c.call_id for c in calls}), len(calls))
            for b in branches:
                positions = [(1, None)] if b.phase == "control" else list(product(range(1, 5), PEERS))
                self.assertEqual([(c.round_number, c.peer) for c in b.calls], positions)
                prefix = f"{b.world_id}/prefix/original/none/rep0" if b.phase == "continuation" else None
                self.assertEqual(b.prefix_parent, prefix)
                self.assertEqual(b.empty_send, b.phase == "control")
        self.assertEqual(Counter(b.phase for b, _ in s.capability), dict(prefix=80, control=10))
        self.assertEqual(s.capability, tuple(iter_calls(s.development))[:90])
        self.assertFalse(any(c.replay_parent for _, c in s.capability))
        self.assertFalse(any(b.replicate for b in s.development))

    def test_every_replay_has_the_same_world_event_replicate_peer_and_required_retention(self):
        p, s = self.population, self.schedules
        worlds = {w.world_id: w for w in p.main + p.development}
        for branches in (s.main, s.development):
            calls = {c.call_id: (b, c) for b, c in iter_calls(branches)}
            seeds = {}
            for b, c in iter_calls(branches):
                if b.phase != "continuation":
                    self.assertIsNone(c.replay_parent)
                    continue
                key = (b.world_id, b.replicate, c.round_number, c.peer)
                self.assertEqual(seeds.setdefault(key, c.seed), c.seed)
                if c.round_number != 1 or b.policy not in ("P_G", "P_H", "Q_B", "Q_C"):
                    self.assertIsNone(c.replay_parent)
                    self.assertEqual(c.generation_id, c.call_id)
                    continue
                if b.policy.startswith("Q_"):
                    expected_policy = b.policy[-1]
                else:
                    group = worlds[b.world_id].partition[0 if b.policy == "P_G" else 1]
                    expected_policy = "C" if c.peer in group else "B"
                parent, reply = calls[c.replay_parent]
                self.assertEqual((parent.world_id, parent.event, parent.replicate, parent.policy,
                                  reply.round_number, reply.peer, reply.seed),
                                 (b.world_id, b.event, b.replicate, expected_policy, 1, c.peer, c.seed))
                self.assertIsNone(reply.replay_parent)
                self.assertEqual(c.generation_id, reply.call_id)
        by_key = {(b.world_id, b.event, b.policy, b.replicate): b for b in s.main if b.phase == "continuation"}
        repeats = [b for b in s.main if b.replicate == 1]
        self.assertEqual(len(repeats), 50)
        self.assertEqual({b.world_id for b in repeats}, set(p.subsets()["repeat"]))
        for b in repeats:
            original = by_key[b.world_id, b.event, b.policy, 0]
            self.assertEqual(b.prefix_parent, original.prefix_parent)
            self.assertTrue({c.seed for c in b.calls}.isdisjoint(c.seed for c in original.calls))
            self.assertTrue({c.generation_id for c in b.calls}.isdisjoint(c.generation_id for c in original.calls))

    def test_reversed_dependencies_respect_all_prefix_and_previous_round_barriers(self):
        for branches in (self.schedules.main, self.schedules.development):
            ordered = dependency_order(tuple(reversed(branches)))
            ranks = {c.call_id: i for i, (_, c) in enumerate(ordered)}
            self.assertEqual(len(ranks), sum(len(b.calls) for b in branches))
            by_branch = {b.branch_id: b for b in branches}
            for b, c in ordered:
                if c.round_number > 1:
                    parents = [p for p in b.calls if p.round_number == c.round_number - 1]
                elif b.prefix_parent:
                    parents = by_branch[b.prefix_parent].calls[-4:]
                else:
                    parents = ()
                for parent in parents:
                    self.assertLess(ranks[parent.call_id], ranks[c.call_id])
                if c.replay_parent:
                    self.assertLess(ranks[c.replay_parent], ranks[c.call_id])

    def test_retained_fixtures_and_saved_round_trips_without_resampling_or_rebuilding(self):
        p, s = self.population, self.schedules
        with patch("recovery.populations.generate_world", side_effect=AssertionError("resampled")), \
                patch("recovery.schedule._prepare_branches", side_effect=AssertionError("rebuilt")):
            loaded = load_population(ROOT / "tests/fixtures/population_course.json", authoritative=p)
            self.assertEqual(manifest_bytes(loaded), (ROOT / "tests/fixtures/population_course.json").read_bytes())
            retained = load_schedules(ROOT / "tests/fixtures/schedules_course.json", loaded, authoritative=s)
            self.assertEqual(schedule_bytes(retained), (ROOT / "tests/fixtures/schedules_course.json").read_bytes())
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "schedule.json"
                save_schedules(s, p, path)
                self.assertEqual(load_schedules(path, p, authoritative=s), s)
                with self.assertRaises(FileExistsError):
                    save_schedules(s, p, path)
                self.assertEqual(path.read_bytes(), schedule_bytes(s))
        data = json.loads(schedule_bytes(s))
        self.assertEqual(set(data), {"format_version", "regime", "size", "master_seed", "main", "development"})
        for field in ("records", "main_edit", "gold", "candidate", "correctness", "status", "model"):
            self.assertNotIn(f'"{field}":', schedule_bytes(s).decode())
        # Reordering is mathematically admissible but changes the saved schedule authority.
        changed = replace(s, main=tuple(reversed(s.main)))
        validate_schedules(changed, p)
        with self.assertRaisesRegex(ValueError, "authoritative schedule"):
            assert_schedules_match(changed, s)

    def test_configuration_branch_and_replay_mutations_are_rejected(self):
        p, s = self.population, self.schedules
        baseline = json.loads(schedule_bytes(s))
        main = baseline["main"]
        b = next(i for i, row in enumerate(main) if row["phase"] == "continuation" and row["policy"] == "B")
        mask = next(i for i, row in enumerate(main) if row["policy"] == "P_G")
        receipt = next(i for i, row in enumerate(main) if row["policy"] == "B_delta")
        repeat = next(i for i, row in enumerate(main) if row["replicate"] == 1)
        control = next(i for i, row in enumerate(main) if row["phase"] == "control")
        mutations = [lambda d: d.pop("regime"), lambda d: d.update(regime="thesis"),
            lambda d: d.update(regime=True), lambda d: d.update(size="target"),
            lambda d: d.update(master_seed=d["master_seed"] + 1), lambda d: d.update(format_version=True),
            lambda d: d["main"].pop(), lambda d: d["main"].append(deepcopy(d["main"][b])),
            lambda d: d["main"][b]["calls"].pop(), lambda d: d["main"][b].update(prefix_parent="wrong"),
            lambda d: d["main"][receipt].update(event="sham"),
            lambda d: d["main"][repeat].update(world_id=d["main"][repeat]["world_id"][:-2] + "02"),
            lambda d: d["main"][b]["calls"][0].update(seed=0),
            lambda d: d["main"][b]["calls"][0].update(peer=False),
            lambda d: d["main"][control]["calls"][0].update(peer=0),
            lambda d: d["main"][b]["calls"][0].update(replay_parent=d["main"][b]["calls"][0]["call_id"]),
            lambda d: d["main"][mask]["calls"][0].update(replay_parent=None),
            lambda d: d["main"][mask]["calls"][0].update(replay_parent="missing"),
            lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][mask]["calls"][1]["replay_parent"]),
            lambda d: d["development"].insert(0, d["development"].pop())]
        for old, new in (("/revision/", "/sham/"), ("/rep0/", "/rep1/"), ("-01/", "-02/")):
            mutations.append(lambda d, old=old, new=new: d["main"][mask]["calls"][0].update(
                replay_parent=d["main"][mask]["calls"][0]["replay_parent"].replace(old, new)))
        parent = main[mask]["calls"][0]["replay_parent"]
        mutations.append(lambda d: d["main"][mask]["calls"][0].update(
            replay_parent=parent.replace("/C/", "/B/") if "/C/" in parent else parent.replace("/B/", "/C/")))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for i, mutate in enumerate(mutations):
                with self.subTest(mutation=i):
                    data = deepcopy(baseline)
                    mutate(data)
                    path.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_schedules(path, p)
            with self.assertRaises(ValueError):
                save_schedules(replace(s, regime="thesis"), p, path)
        for count in (40, 60, True, 20.0):
            with self.assertRaises(ValueError):
                s.main_for(p, count)
        with self.assertRaisesRegex(ValueError, "configuration differs"):
            s.main_for(replace(p, regime="thesis"))


if __name__ == "__main__":
    unittest.main()
