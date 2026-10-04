from collections import Counter
from dataclasses import FrozenInstanceError, asdict, replace
from itertools import product
from pathlib import Path
import unittest
from unittest.mock import patch

from recovery.manifests import load_population
from recovery.schedule import (CAPABILITY_CALLS, SMOKE_MAX_CALLS, component_counts,
                               dependency_order, iter_calls, prepare_schedules, validate_schedules)
from recovery.tasks import Size, Task

ROOT = Path(__file__).resolve().parent.parent

# Independent specification arithmetic, not a second builder invocation. Each
# pair is (new generations, logical slots); masks/Q replay four of sixteen.
MAIN_TABLES = {
    60: dict(prefix=(960, 960), revised=(4800, 4800), sham=(2880, 2880),
             masks=(2880, 3840), controls=(120, 120), preserving=(768, 768),
             receipts=(1152, 1152), prose_delay=(1152, 1536), repeat=(1440, 1600)),
    40: dict(prefix=(640, 640), revised=(3200, 3200), sham=(1920, 1920),
             masks=(1920, 2560), controls=(80, 80), preserving=(768, 768),
             receipts=(768, 768), prose_delay=(768, 1024), repeat=(1440, 1600)),
}
PILOT_TABLE = dict(prefix=(80, 80), controls=(10, 10), revised=(400, 400), sham=(240, 240),
                   masks=(96, 128), receipts=(96, 96), prose_delay=(96, 128), preserving=(96, 96))


def independent_branch_population(worlds, development):
    """Expected cells as world/event/policy/replicate, independently of schedule helpers."""
    cells = set()
    for world in worlds:
        wid, task = world.world_id, world.world.task
        cells.update((wid, event, policy, 0) for event, policy in
                     [("revision", p) for p in ("L", "B", "C", "K", "F")]
                     + [("sham", p) for p in ("B", "C", "K")])
        if not development or task in (Task.PREFIX, Task.BFS):
            cells.update((wid, e, p, 0) for e, p in product(("revision", "sham"), ("P_G", "P_H")))
        if task in (Task.PREFIX, Task.SORT):
            cells.update((wid, "revision", p, 0) for p in ("B_delta", "C_delta", "K_delta"))
        if task in (Task.SORT, Task.BFS):
            cells.update((wid, e, p, 0) for e, p in product(("revision", "sham"), ("Q_B", "Q_C")))
        if task in (Task.TOP_K, Task.BFS) and (development or world.index <= 8):
            cells.update((wid, "preserving", p, 0) for p in ("B", "C", "K"))
        if not development and world.index <= 2:
            cells.update((wid, e, p, 1) for e, p in
                         product(("revision", "sham"), ("B", "C", "K", "P_G", "P_H")))
    return cells


class ScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.populations = {s: load_population(ROOT / f"tests/fixtures/population_{s.value}.json") for s in Size}
        cls.schedules = {s: prepare_schedules(p) for s, p in cls.populations.items()}

    def test_independent_main_component_tables_and_exact_generation_join(self):
        for size, schedules in self.schedules.items():
            population = self.populations[size]
            validate_schedules(schedules, population)
            for count, totals in ((60, (16152, 17656)), (40, (11504, 12560))):
                with self.subTest(size=size, count=count):
                    branches = schedules.main_for(population, count)
                    self.assertEqual(component_counts(branches), MAIN_TABLES[count])
                    calls = [c for _, c in iter_calls(branches)]
                    self.assertEqual((len({c.generation_id for c in calls}), len(calls)), totals)
                    self.assertEqual(sum(c.replay_parent is None for c in calls), totals[0])
                    self.assertEqual(len({c.call_id for c in calls}), totals[1])
                    self.assertEqual(len({b.branch_id for b in branches}), len(branches))

    def test_independent_pilot_components_capability_block_and_separate_smoke(self):
        for schedules in self.schedules.values():
            counts = component_counts(schedules.development)
            self.assertEqual(counts, PILOT_TABLE)
            base = sum(counts[k][0] for k in ("prefix", "controls", "revised", "sham"))
            self.assertEqual([base] + [counts[k][0] for k in
                                      ("masks", "receipts", "prose_delay", "preserving")], [730, 96, 96, 96, 96])
            calls = tuple(iter_calls(schedules.development))
            self.assertEqual(len(calls), 1178)
            self.assertEqual(len({c.generation_id for _, c in calls}), 1114)
            self.assertEqual(Counter(b.phase for b, _ in schedules.capability), {"prefix": 80, "control": 10})
            self.assertEqual(calls[:90], schedules.capability)
            self.assertEqual(CAPABILITY_CALLS, 90)
            self.assertEqual(SMOKE_MAX_CALLS, 24)
            self.assertEqual(1114 + SMOKE_MAX_CALLS, 1138)
            self.assertFalse(any(b.phase == "smoke" for b in schedules.development))
            self.assertTrue(all(c.replay_parent is None for _, c in schedules.capability))

    def test_exact_memberships_no_unprescribed_crossings_and_fixed_opportunities(self):
        for size, schedules in self.schedules.items():
            population = self.populations[size]
            for worlds, branches, development in (
                    (population.main, schedules.main, False),
                    (population.worlds(40), schedules.main_for(population, 40), False),
                    (population.development, schedules.development, True)):
                continuations = [b for b in branches if b.phase == "continuation"]
                self.assertEqual({(b.world_id, b.event, b.policy, b.replicate) for b in continuations},
                                 independent_branch_population(worlds, development))
                prefixes = {b.world_id: b for b in branches if b.phase == "prefix"}
                self.assertEqual(set(prefixes), {w.world_id for w in worlds})
                self.assertEqual(len(prefixes), sum(b.phase == "prefix" for b in branches))
                for branch in branches:
                    self.assertEqual(branch.task, next(w.world.task for w in worlds if w.world_id == branch.world_id))
                    if branch.phase == "control":
                        self.assertEqual([(c.round_number, c.peer) for c in branch.calls], [(1, None)])
                        self.assertIsNone(branch.prefix_parent)
                    else:
                        self.assertEqual(Counter(c.peer for c in branch.calls), dict.fromkeys(range(4), 4))
                        self.assertEqual(Counter(c.round_number for c in branch.calls), dict.fromkeys(range(1, 5), 4))
                    if branch.phase == "continuation":
                        self.assertEqual(branch.prefix_parent, prefixes[branch.world_id].branch_id)
                controls = Counter((b.world_id, b.event) for b in branches if b.phase == "control")
                self.assertEqual(controls, {(w.world_id, event): 1 for w in worlds for event in ("original", "revision")})
            nested_ids = {w.world_id for w in population.worlds(40)}
            self.assertEqual(schedules.main_for(population, 40), tuple(b for b in schedules.main if b.world_id in nested_ids))
            self.assertEqual({b.world_id for b in schedules.main if b.component == "preserving"},
                             set(population.subsets()["preserving"]))
            self.assertEqual({b.world_id for b in schedules.main if b.component == "repeat"},
                             set(population.subsets()["repeat"]))

    def test_only_required_first_round_replay_same_event_replicate_and_peer(self):
        for size, schedules in self.schedules.items():
            population = self.populations[size]
            for branches in (schedules.main, schedules.development):
                by_key = {(b.world_id, b.event, b.policy, b.replicate): b for b in branches if b.phase == "continuation"}
                worlds = {w.world_id: w for w in population.main + population.development}
                for branch, call in iter_calls(branches):
                    sharing = branch.policy in ("P_G", "P_H", "Q_B", "Q_C") and call.round_number == 1
                    if not sharing:
                        self.assertIsNone(call.replay_parent)
                        self.assertEqual(call.generation_id, call.call_id)
                        continue
                    if branch.policy in ("P_G", "P_H"):
                        g, h = worlds[branch.world_id].partition
                        cleared = g if branch.policy == "P_G" else h
                        policy = "C" if call.peer in cleared else "B"
                    else:
                        policy = "B" if branch.policy == "Q_B" else "C"
                    parent = by_key[branch.world_id, branch.event, policy, branch.replicate].calls[call.peer]
                    self.assertEqual(call.replay_parent, parent.call_id)
                    self.assertEqual(call.generation_id, parent.generation_id)
                    self.assertEqual(call.seed, parent.seed)
                # Equal B/C seeds do not collapse distinct stochastic generations.
                for key, b in by_key.items():
                    if b.policy == "B":
                        c = by_key[b.world_id, b.event, "C", b.replicate]
                        self.assertEqual([x.seed for x in b.calls], [x.seed for x in c.calls])
                        self.assertTrue({x.generation_id for x in b.calls}.isdisjoint(x.generation_id for x in c.calls))

    def test_extra_replicate_new_ids_seeds_original_prefix_and_partition(self):
        for size, schedules in self.schedules.items():
            population = self.populations[size]
            by_key = {(b.world_id, b.phase, b.event, b.policy, b.replicate): b for b in schedules.main}
            for repeat in (b for b in schedules.main if b.replicate == 1):
                original = by_key[repeat.world_id, repeat.phase, repeat.event, repeat.policy, 0]
                self.assertEqual(repeat.prefix_parent, original.prefix_parent)
                self.assertTrue({c.generation_id for c in repeat.calls}.isdisjoint(c.generation_id for c in original.calls))
                self.assertTrue({c.seed for c in repeat.calls}.isdisjoint(c.seed for c in original.calls))
                world = next(w for w in population.main if w.world_id == repeat.world_id)
                # Group membership and world inputs are joined from the original authority.
                for c in repeat.calls[:4]:
                    if repeat.policy in ("P_G", "P_H"):
                        group = world.partition[0 if repeat.policy == "P_G" else 1]
                        self.assertIn(f"/{'C' if c.peer in group else 'B'}/rep1/", c.replay_parent)
            self.assertFalse(any(b.replicate for b in schedules.development))

    def test_controls_full_world_candidate_lengths_and_empty_send(self):
        for size, schedules in self.schedules.items():
            for branches in (schedules.main, schedules.development):
                for branch in branches:
                    if branch.phase != "control":
                        self.assertFalse(branch.empty_send)
                        continue
                    self.assertTrue(branch.empty_send)
                    call, = branch.calls
                    self.assertIsNone(call.peer)
                    self.assertIsNone(call.replay_parent)
                    expected = (10 if branch.task is Task.TOP_K else size.node_count if branch.task is Task.BFS
                                else size.numeric_length - (branch.task is Task.DIFFERENCE))
                    contract = branch.output_contract(call, size)
                    self.assertEqual(len(contract.coordinates), expected)
                    candidate = {str(i): -1 for i in range(expected)} if branch.task is Task.BFS else [0] * expected
                    self.assertIsNone(contract.error(candidate))
                    if branch.task in (Task.PREFIX, Task.SORT):
                        self.assertEqual(contract.error([0] * size.shard_size), "candidate_length")

    def test_cpu_dependency_orders_even_after_branch_reordering(self):
        for size, schedules in self.schedules.items():
            for branches in (schedules.main, schedules.main_for(self.populations[size], 40), schedules.development):
                # Parents may be serialized later: topological sorting must still work.
                ordered = dependency_order(tuple(reversed(branches)))
                rank = {c.call_id: i for i, (_, c) in enumerate(ordered)}
                self.assertEqual(set(rank), {c.call_id for _, c in iter_calls(branches)})
                by_branch = {b.branch_id: b for b in branches}
                for branch, call in ordered:
                    if call.round_number > 1:
                        previous = [c for c in branch.calls if c.round_number == call.round_number - 1]
                    elif branch.prefix_parent:
                        previous = by_branch[branch.prefix_parent].calls[-4:]
                    else:
                        previous = ()
                    for parent in previous:
                        self.assertLess(rank[parent.call_id], rank[call.call_id])
                    if call.replay_parent:
                        self.assertLess(rank[call.replay_parent], rank[call.call_id])

    def test_poor_or_perfect_prefix_never_selects_or_changes_opportunities(self):
        for size, schedules in self.schedules.items():
            population = self.populations[size]
            before = asdict(schedules)
            planned = tuple(c.call_id for _, c in dependency_order(schedules.main))
            for status in ("correct", "wrong", "invalid", "timeout"):
                # Scripted outcomes stay offline; the plan retains every failed
                # prefix and every peer/round. No production solver is allowed.
                results = {c.call_id: status for b, c in iter_calls(schedules.main) if b.phase == "prefix"}
                self.assertEqual(len(results), 960)
                with patch("recovery.truth.solve_world", side_effect=AssertionError("outcome selection")):
                    validate_schedules(schedules, population)
                    self.assertEqual(tuple(c.call_id for _, c in dependency_order(schedules.main)), planned)
                self.assertEqual(asdict(schedules), before)
            with self.assertRaises(FrozenInstanceError):
                schedules.main = ()

    def test_missing_parents_and_cycles_fail_cpu_dependency_validation(self):
        branches = self.schedules[Size.TARGET].main
        first = branches[0]
        one, two = first.calls[:2]
        for changed, message in (
                (replace(first, calls=(replace(one, replay_parent="missing"),) + first.calls[1:]), "missing call"),
                (replace(first, calls=(replace(one, replay_parent=two.call_id), replace(two, replay_parent=one.call_id))
                         + first.calls[2:]), "cyclic")):
            with self.assertRaisesRegex(ValueError, message):
                dependency_order((changed,) + branches[1:])
        with self.assertRaisesRegex(ValueError, "missing prefix"):
            dependency_order(tuple(b for b in branches if b.branch_id != first.branch_id))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            dependency_order(branches + (first,))


if __name__ == "__main__":
    unittest.main()
