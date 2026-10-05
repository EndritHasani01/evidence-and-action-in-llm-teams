"""CPU local scheduling, immutable cross-worker replay and assigned-work resume."""

from dataclasses import asdict, replace
from functools import partial
import json
from pathlib import Path
import sqlite3
import tempfile
from time import monotonic, sleep
import unittest

from recovery.replay import held_prose_counts
from recovery.rounds import prefix_snapshot, snapshot_bytes
from recovery.runner import DurableRunner, WorkerReader
from recovery.schedule import _prepare_branches
from recovery.storage import WorkerStore, record_json
from recovery.tasks import Size, Task
from recovery.workers import LocalScheduler, WorkerInterrupted, WorkerSpec, balanced_order
import recovery.workers as workers_module
from tests.attempt_checks import read_trace, process_alive
from tests.durable_checks import forbidden, prefix, prefix_branch, provider
from tests.event_checks import case_world, population, scheduled
from tests.replay_checks import SETTINGS, replay_provider
from tests.round_checks import TOKENIZER
from tests.worker_fixture import provider_factory, tokenizer_factory


class ParentAccessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paths = tuple(Path(self.temp.name) / f"worker-{i}.sqlite" for i in range(2))
        self.world = case_world(Task.SORT)
        self.parents = tuple(scheduled(self.world, "revision", p) for p in ("B", "C"))
        with DurableRunner(self.paths[0], TOKENIZER, provider, scripted=True) as runner:
            self.prefix = prefix(runner, self.world)
            self.prefix_bytes = prefix_snapshot(runner.state(self.prefix.branch_id))
            runner.reply_provider = replay_provider(TOKENIZER, "unicode")
            for parent in self.parents:
                runner.start(self.world, parent, settings=SETTINGS)
                runner.run_round(parent.branch_id, 1)
            self.parent_states = tuple(snapshot_bytes(runner.state(b.branch_id)) for b in self.parents)

    def test_cross_worker_invalid_failed_parents_keep_identity_cost_and_branch_local_queues(self):
        with DurableRunner(self.paths[1], TOKENIZER, forbidden, scripted=True,
                           dependencies=(self.paths[0],)) as runner:
            siblings = []
            for policy in ("P_G", "P_H", "Q_B", "Q_C"):
                branch = scheduled(self.world, "revision", policy)
                initial = runner.start(self.world, branch, settings=SETTINGS)
                result = runner.run_round(branch.branch_id, 1)
                self.assertEqual(result.barrier.replies[2].candidate.status, "invalid")
                self.assertIn("\\ud800", record_json(asdict(result.barrier.replies[2])))
                self.assertEqual(result.barrier.replies[3].candidate.status, "failed")
                for call in branch.calls[:4]:
                    row = runner.store.call(call.call_id)
                    self.assertEqual((row["generation_id"], row["replay_parent"], row["seed"], row["status"]),
                                     (call.replay_parent, call.replay_parent, call.seed, "replay"))
                    self.assertEqual(runner.store.response(call.call_id), runner.store.response(call.replay_parent))
                    self.assertEqual(len(runner.store.attempts(call.replay_parent)), 1)
                    self.assertFalse(runner.store.attempts(call.call_id))
                with self.assertRaisesRegex(ValueError, "original worker"):
                    runner.store.begin_attempt(branch.calls[0].replay_parent)
                self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)
                self.assertTrue(all(d.delivery_id.startswith(branch.branch_id + "/")
                                    for d in result.committed.deliveries if d.generated is not None and d.generated.phase == "recovery"))
                self.assertEqual(initial.prefix_parent, self.prefix.branch_id)
                siblings.append(result.committed)
            self.assertTrue(any(held_prose_counts(siblings[2])))
            self.assertFalse(any(held_prose_counts(siblings[0])))
            self.assertFalse({d.delivery_id for d in siblings[0].deliveries if d.generated is not None and d.generated.phase == "recovery"}
                             & {d.delivery_id for d in siblings[1].deliveries if d.generated is not None and d.generated.phase == "recovery"})
        reader = WorkerReader(self.paths[0])
        try:
            self.assertEqual(prefix_snapshot(reader.state(self.prefix.branch_id)), self.prefix_bytes)
            self.assertEqual(tuple(snapshot_bytes(reader.state(b.branch_id)) for b in self.parents), self.parent_states)
        finally:
            reader.close()

    def test_read_only_live_parent_access_rejects_writes_and_does_not_recover_or_copy(self):
        with DurableRunner(self.paths[0], TOKENIZER, forbidden, scripted=True) as owner:
            reader = WorkerReader(self.paths[0])
            try:
                before = owner.store.connection.total_changes
                self.assertEqual(prefix_snapshot(reader.state(self.prefix.branch_id)), self.prefix_bytes)
                with self.assertRaises(sqlite3.OperationalError):
                    reader.store.connection.execute("DELETE FROM calls")
                self.assertEqual(owner.store.connection.total_changes, before)
            finally:
                reader.close()

    def test_missing_or_misscoped_cross_worker_parent_stops_without_generation_or_effects(self):
        for defect in ("missing", "event", "seed", "validation"):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                parent_path = Path(directory) / "parent.sqlite"
                child_path = Path(directory) / "child.sqlite"
                with DurableRunner(self.paths[0], TOKENIZER, forbidden, scripted=True) as saved:
                    saved.backup(parent_path)
                con = sqlite3.connect(parent_path)
                call = self.parents[0].calls[0]
                if defect == "missing":
                    con.execute("DELETE FROM calls WHERE call_id=?", (call.call_id,))
                elif defect == "seed":
                    con.execute("UPDATE calls SET seed=seed+1 WHERE call_id=?", (call.call_id,))
                elif defect == "event":
                    row = con.execute("SELECT branch_json FROM round_inputs WHERE branch_id=? AND round_number=1", (self.parents[0].branch_id,)).fetchone()
                    data = json.loads(row[0]); data["event"] = "sham"
                    con.execute("UPDATE round_inputs SET branch_json=? WHERE branch_id=?", (record_json(data), self.parents[0].branch_id))
                else:
                    con.execute("UPDATE calls SET validation_json=NULL WHERE call_id=?", (call.call_id,))
                con.commit(); con.close()
                with DurableRunner(child_path, TOKENIZER, forbidden, scripted=True, dependencies=(parent_path,)) as runner:
                    branch = scheduled(self.world, "revision", "Q_B")
                    initial = runner.start(self.world, branch, settings=SETTINGS)
                    with self.assertRaises(ValueError):
                        runner.run_round(branch.branch_id, 1)
                    self.assertEqual(runner.state(branch.branch_id), initial)
                    self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)

    def test_controls_are_durable_empty_send_full_shape_and_reject_input_drift(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                path = Path(self.temp.name) / f"{task.value}-{size.value}.sqlite"
                controls = [b for b in _prepare_branches((world,)) if b.phase == "control"]
                with DurableRunner(path, TOKENIZER, provider, scripted=True) as runner:
                    for branch in controls:
                        # The normal prefix script has no control support; inject
                        # a lawful placeholder without reading evaluator truth.
                        from tests.round_checks import reply
                        runner.reply_provider = lambda view, *args, **kwargs: reply(TOKENIZER, view)
                        result = runner.run_control(world, branch, settings=SETTINGS)
                        self.assertEqual(result.candidate.status, "valid")
                        self.assertEqual(result.messages, ())
                        self.assertEqual(runner.store.response(branch.calls[0].call_id), result.generated)
                    runner.reply_provider = forbidden
                    for branch in controls:
                        runner.run_control(world, branch, settings=SETTINGS)
                    self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 2)
                    with self.assertRaisesRegex(ValueError, "equality"):
                        runner.run_control(world, controls[0], settings=dict(SETTINGS, temperature=0.7))


class SchedulingTests(unittest.TestCase):
    evidence = []
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.world = case_world(Task.SORT)
        self.branches = (prefix_branch(self.world), *[scheduled(self.world, "revision", p)
                                                    for p in ("B", "C", "P_G", "Q_B")])

    def specs(self, directory, *, pause=None):
        return tuple(WorkerSpec(Path(directory) / f"worker-{i}.sqlite",
            partial(provider_factory, str(Path(directory) / f"trace-{i}.jsonl"),
                    0.006 if i == 0 else 0.001, pause=pause), f"cpu-{i}") for i in range(2))

    def scheduler(self, directory, **kwargs):
        return LocalScheduler(self.specs(directory), (self.world,), self.branches, tokenizer_factory,
                              settings=SETTINGS, timeout_seconds=15, heartbeat_seconds=0.05, **kwargs)

    def outcomes(self, scheduler):
        result = {}
        for work in scheduler.status():
            reader = scheduler.readers[work.worker]
            result[work.branch_id] = snapshot_bytes(reader.state(work.branch_id))
        return result

    def capture(self, scheduler, case, **extra):
        """Derived evidence only; clocks/PIDs are real validation measurements."""
        work = scheduler.status()
        workers = []
        for index, reader in enumerate(scheduler.readers):
            reader.store.parents = tuple(other.store for other in scheduler.readers if other is not reader)
            try:
                rows = [dict(row) for row in reader.store.connection.execute("SELECT * FROM calls ORDER BY call_id")]
                for row in rows:
                    row["resolved_response"] = asdict(reader.store.response(row["call_id"]))
                workers.append({"worker": index, "calls": rows,
                    "round_inputs": [dict(row) for row in reader.store.connection.execute(
                        "SELECT * FROM round_inputs ORDER BY branch_id,round_number")],
                    "attempts": [dict(row) for row in reader.store.connection.execute(
                        "SELECT * FROM attempts ORDER BY call_id,number")],
                    "processes": [dict(row) for row in reader.store.connection.execute(
                        "SELECT * FROM provider_processes ORDER BY started_at")],
                    "instrumentation": read_trace(scheduler.paths[index].parent / f"trace-{index}.jsonl")})
            finally:
                reader.store.parents = ()
        self.evidence.append({"case": case, "work": [asdict(w) for w in work], "workers": workers,
            "states": {w.branch_id: asdict(scheduler.readers[w.worker].state(w.branch_id))
                       for w in work if scheduler.by_branch[w.branch_id].phase != "control"}, **extra})

    def test_two_processes_uneven_delays_reversal_rotation_preserve_exact_schedule_seeds_and_outcomes(self):
        first = Path(self.temp.name) / "first"
        second = Path(self.temp.name) / "second"
        with self.scheduler(first) as scheduler:
            pending = scheduler.status()
            self.assertTrue(any(w.status == "dependency_waiting" for w in pending))
            scheduler.run()
            expected = self.outcomes(scheduler)
            placements = {w.branch_id: w.worker for w in scheduler.status()}
            self.assertEqual(len(set(placements.values())), 2)
            self.capture(scheduler, "order_a")
        with self.scheduler(second, reverse=True, worker_rotation=1, invocation_order=(3, 2, 1, 0)) as scheduler:
            scheduler.run()
            self.assertEqual(self.outcomes(scheduler), expected)
            self.assertNotEqual({w.branch_id: w.worker for w in scheduler.status()}, placements)
            self.capture(scheduler, "order_b")
        traces = []
        for directory in (first, second):
            events = [e for i in range(2) for e in read_trace(directory / f"trace-{i}.jsonl")]
            self.assertEqual(len({e["pid"] for e in events if e["event"] == "load"}), 2)
            self.assertTrue(all(Path(e["module"]).resolve() == Path(workers_module.__file__).resolve()
                                for e in events if e["event"] == "load"))
            self.assertEqual({e["visibility"] for e in events}, {"cpu-0", "cpu-1"})
            generations = [e for e in events if e["event"] == "generation"]
            self.assertEqual(len(generations), sum(c.replay_parent is None for b in self.branches for c in b.calls))
            traces.append(sorted(record_json({k: e[k] for k in ("seed", "rng_probe", "view", "rendered", "tokenized", "settings")}) for e in generations))
        self.assertEqual(*traces)

    def test_resume_completed_run_changed_order_has_no_calls_and_rejects_settings_seed_parent_drift(self):
        directory = Path(self.temp.name) / "resume"
        with self.scheduler(directory) as scheduler:
            scheduler.run()
            expected = self.outcomes(scheduler)
        before = [read_trace(directory / f"trace-{i}.jsonl") for i in range(2)]
        with self.scheduler(directory, reverse=True, worker_rotation=1) as scheduler:
            scheduler.run()
            self.assertEqual(self.outcomes(scheduler), expected)
            self.capture(scheduler, "completed_reopen")
        self.assertEqual([read_trace(directory / f"trace-{i}.jsonl") for i in range(2)], before)
        with self.assertRaisesRegex(ValueError, "saved configuration"):
            with LocalScheduler(self.specs(directory), (self.world,), self.branches, tokenizer_factory,
                                settings=dict(SETTINGS, temperature=0.7), timeout_seconds=15, heartbeat_seconds=0.05):
                pass
        for defect in ("seed", "parent"):
            call = self.branches[-1].calls[0]
            changed = replace(call, seed=call.seed + 1) if defect == "seed" else replace(call, replay_parent=self.branches[1].calls[1].call_id)
            broken = replace(self.branches[-1], calls=(changed, *self.branches[-1].calls[1:]))
            with self.assertRaisesRegex(ValueError, "exact saved"):
                LocalScheduler(self.specs(directory), (self.world,), (*self.branches[:-1], broken), tokenizer_factory, settings=SETTINGS)

    def test_missing_parent_is_rejected_before_creating_worker_files(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            LocalScheduler(self.specs(self.temp.name), (self.world,), (self.branches[0], self.branches[-1]),
                           tokenizer_factory, settings=SETTINGS)
        self.assertFalse(any(Path(self.temp.name).glob("*.sqlite")))

    def test_second_controller_cannot_open_an_idle_exclusive_worker_or_start_duplicate_calls(self):
        directory = Path(self.temp.name) / "exclusive"
        with self.scheduler(directory) as owner:
            before = owner.status()
            self.assertTrue(all(reader.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0] == 0
                                for reader in owner.readers))
            with self.assertRaisesRegex(WorkerInterrupted, "exclusive worker"):
                with self.scheduler(directory):
                    pass
            self.assertEqual(owner.status(), before)
            owner.run()
            self.assertEqual(sum(reader.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0]
                                 for reader in owner.readers), 72)

    def test_interrupted_q_worker_resumes_assigned_checkpoint_with_one_retry_and_no_duplicate_effects(self):
        baseline = Path(self.temp.name) / "baseline"
        with self.scheduler(baseline) as scheduler:
            scheduler.run()
            expected = self.outcomes(scheduler)
            self.capture(scheduler, "q_baseline")
        directory = Path(self.temp.name) / "interrupted"
        flag = directory / "paused"
        with LocalScheduler(self.specs(directory, pause=str(flag)), (self.world,), self.branches, tokenizer_factory,
                            settings=SETTINGS, timeout_seconds=15, heartbeat_seconds=0.05) as scheduler:
            deadline = monotonic() + 40
            while not flag.exists() and monotonic() < deadline:
                scheduler.advance(0.05)
            self.assertTrue(flag.exists(), "Q never reached the held-prose interruption boundary")
            paused = [(i, e) for i in range(2) for e in read_trace(directory / f"trace-{i}.jsonl") if e["event"] == "paused"]
            # The marker may precede its trace line by a few filesystem writes.
            while not paused and monotonic() < deadline:
                sleep(0.01)
                paused = [(i, e) for i in range(2) for e in read_trace(directory / f"trace-{i}.jsonl") if e["event"] == "paused"]
            self.assertEqual(len(paused), 1)
            index, event = paused[0]
            branch_id, round_number = scheduler.inflight[index]
            self.assertEqual(branch_id, scheduled(self.world, "revision", "Q_B").branch_id)
            self.assertEqual(round_number, 2)
            held = scheduler.readers[index].state(branch_id)
            self.assertTrue(any(held_prose_counts(held)))
            with self.assertRaises(WorkerInterrupted):
                scheduler.restart(index)  # A live owner never permits duplicate generation.
            scheduler.processes[index].terminate()
            scheduler.processes[index].join(3)
            with self.assertRaises(WorkerInterrupted):
                scheduler.advance(0.05)
            scheduler.restart(index)
            self.assertFalse(process_alive(event["pid"]))
            scheduler.run()
            self.assertEqual(self.outcomes(scheduler), expected)
            branch = scheduler.by_branch[branch_id]
            attempts = scheduler.readers[index].store.attempts(branch.calls[4].call_id)
            self.assertEqual([a["status"] for a in attempts], ["interrupted", "completed"])
            self.assertEqual(attempts[0]["uncertain_completion"], 1)
            self.assertIsNone(attempts[0]["finished_at"])
            self.assertEqual(len({d.delivery_id for d in scheduler.readers[index].state(branch_id).deliveries}),
                             len(scheduler.readers[index].state(branch_id).deliveries))
            self.assertEqual(sum(reader.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0]
                                 for reader in scheduler.readers),
                             1 + sum(c.replay_parent is None for b in self.branches for c in b.calls))
            self.capture(scheduler, "q_resumed", held_before_interruption=asdict(held))

    def test_balanced_blocks_and_all_saved_opportunities_are_ordered_without_outcome_filtering(self):
        worlds = population(Size.TARGET).main
        branches = _prepare_branches(worlds)
        ordered = balanced_order(worlds, branches)
        self.assertEqual({b.branch_id for b in ordered}, {b.branch_id for b in branches})
        indices = {w.world_id: w.index for w in worlds}
        self.assertEqual([indices[b.world_id] for b in ordered], sorted(indices[b.world_id] for b in ordered))
        for index in range(1, 13):
            block = [b for b in ordered if indices[b.world_id] == index]
            self.assertEqual({b.task for b in block if b.phase == "prefix"}, set(Task))
            first_recovery = next(i for i, b in enumerate(block) if b.phase == "continuation")
            self.assertTrue(all(b.phase != "continuation" for b in block[:first_recovery]))
        self.assertNotEqual(ordered, balanced_order(worlds, branches, reverse=True))

    def test_saved_complete_manifests_keep_main_and_capability_schedule_totals(self):
        root = Path(__file__).resolve().parent / "fixtures"
        for count, logical in ((60, 17656), (40, 12560)):
            scheduler = LocalScheduler.from_manifests(self.specs(self.temp.name), root / "population_target.json",
                root / "schedules_target.json", tokenizer_factory, stage="main", count=count, settings=SETTINGS)
            self.assertEqual(sum(len(b.calls) for b in scheduler.branches), logical)
            self.assertEqual(len(scheduler.worlds), count)
        scheduler = LocalScheduler.from_manifests(self.specs(self.temp.name), root / "population_target.json",
            root / "schedules_target.json", tokenizer_factory, settings=SETTINGS)
        prelude = [b for b in scheduler.ordered if b.phase in ("prefix", "control")]
        self.assertEqual(sum(len(b.calls) for b in prelude), 90)
        self.assertEqual(sum(c.replay_parent is None for b in scheduler.branches for c in b.calls), 1114)
        self.assertFalse(any(Path(self.temp.name).glob("*.sqlite")))

    def test_lost_round_acknowledgment_restarts_from_committed_effects_without_new_attempt(self):
        directory = Path(self.temp.name) / "lost-ack"
        branches = (self.branches[0],)
        with LocalScheduler(self.specs(directory), (self.world,), branches, tokenizer_factory,
                            settings=SETTINGS, timeout_seconds=15, heartbeat_seconds=0.05) as scheduler:
            admitted = scheduler.dispatch()
            index, branch_id, _ = admitted[0]
            deadline = monotonic() + 15
            while monotonic() < deadline:
                values = scheduler.readers[index].values(branch_id)
                if values is not None and scheduler.readers[index].state(branch_id).last_slot is not None:
                    break
                sleep(0.02)
            before = scheduler.readers[index].state(branch_id)
            self.assertEqual(before.last_slot.round_number, 1)
            self.assertIn(index, scheduler.inflight)  # Durable effect, deliberately unread ack.
            scheduler.processes[index].terminate()
            scheduler.processes[index].join(3)
            scheduler.restart(index)
            self.assertEqual(scheduler.readers[index].state(branch_id), before)
            scheduler.run()
            self.assertEqual(len(scheduler.readers[index].store.attempts(branches[0].calls[0].call_id)), 1)
            self.assertEqual(scheduler.readers[index].store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 16)
            self.capture(scheduler, "lost_ack_resumed", committed_before_interruption=asdict(before))

    def test_five_family_cpu_prelude_executes_all_controls_before_recovery_with_invalid_slots_included(self):
        worlds = population(Size.FALLBACK).development
        branches = tuple(b for b in _prepare_branches(worlds) if b.phase in ("prefix", "control") or
                         (b.event == "revision" and b.policy == "B"))
        directory = Path(self.temp.name) / "five-family"
        with LocalScheduler(self.specs(directory), worlds, branches, tokenizer_factory,
                            settings=SETTINGS, timeout_seconds=15, heartbeat_seconds=0.05) as scheduler:
            observed = []
            while scheduler.inflight or any(w.status != "done" for w in scheduler.status()):
                observed.extend(scheduler.advance())
            first_recovery = next(i for i, (_, branch_id, _) in enumerate(observed)
                                  if scheduler.by_branch[branch_id].phase == "continuation")
            self.assertEqual(sum(1 if scheduler.by_branch[b].phase == "control" else 4
                                 for _, b, _ in observed[:first_recovery]), 90)
            self.assertEqual(sum(reader.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0]
                                 for reader in scheduler.readers), 170)
            for index, reader in enumerate(scheduler.readers):
                intervals = reader.store.connection.execute("SELECT device_visibility FROM provider_processes").fetchall()
                self.assertTrue(all(row[0] == f"cpu-{index}" for row in intervals))
            self.assertTrue(any(row[0] == "infrastructure_failure" for reader in scheduler.readers
                                for row in reader.store.connection.execute("SELECT status FROM calls")))
            self.capture(scheduler, "five_family_prelude")

    def test_deleted_committed_parent_stops_resume_before_spawning_or_regenerating(self):
        directory = Path(self.temp.name) / "missing-durable"
        with self.scheduler(directory) as scheduler:
            scheduler.run()
            work = next(w for w in scheduler.status() if w.branch_id == self.branches[1].branch_id)
            path = scheduler.paths[work.worker]
            self.capture(scheduler, "missing_parent_baseline")
        before = [read_trace(directory / f"trace-{i}.jsonl") for i in range(2)]
        con = sqlite3.connect(path)
        con.execute("DELETE FROM calls WHERE call_id=?", (self.branches[1].calls[0].call_id,))
        con.commit(); con.close()
        with self.assertRaisesRegex(ValueError, "missing committed"):
            with self.scheduler(directory):
                pass
        self.assertEqual([read_trace(directory / f"trace-{i}.jsonl") for i in range(2)], before)


if __name__ == "__main__":
    unittest.main()
