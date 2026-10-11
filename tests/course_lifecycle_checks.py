"""Tiny ordinary course lifecycle, accounting bounds, safe stop and M4 handoff."""

from contextlib import closing
from functools import partial
import hashlib
import json
from pathlib import Path
import tempfile
from time import monotonic, sleep
import unittest

from recovery.accounting import BudgetStop, progress_snapshot
from recovery.rounds import deserialize_state
from recovery.runner import DurableRunner
from recovery.state import OwnReply, ReceivedProse, Slot
from recovery.storage import WorkerStore, record_json
from recovery.tasks import Task
from recovery.workers import LocalScheduler, WorkerSpec
from tests.accounting_checks import clock
from tests.course_accounting_checks import independent_records, known_budget
from tests.course_intervention_cases import TOKENIZER, branches, course_inputs, scheduled
from tests.course_worker_cases import SETTINGS, prefix_branch, provide, provider_factory, sort_world, tokenizer_factory
from tests.lifecycle_fixture import (BOUNDS, backup_workers, offline_preview, scientific_records,
    stable_progress, write_json)


class CourseLifecycleTests(unittest.TestCase):
    bundle = None
    evidence = []

    def setUp(self):
        if self.bundle is None:
            temporary = tempfile.TemporaryDirectory()
            self.addCleanup(temporary.cleanup)
            self.root = Path(temporary.name)
        else:
            self.root = Path(self.bundle) / self._testMethodName
            self.root.mkdir()

    def capture(self, worlds, selected, paths, snapshot, **detail):
        expected = independent_records(worlds, selected, paths, snapshot)
        if self.bundle is None:
            return
        write_json(self.root / "selection.json", dict(world_ids=[w.world_id for w in worlds],
            branch_ids=[b.branch_id for b in selected], workers=[p.name for p in paths]))
        write_json(self.root / "progress.json", snapshot)
        write_json(self.root / "offline-preview.json", offline_preview(worlds, selected, paths))
        self.evidence.append(dict(directory=self.root.relative_to(self.bundle).as_posix(), independent_counts=expected, **detail))

    def check_backups(self, worlds, selected, paths, snapshot):
        copies = tuple(self.root / f"backup-{i}.sqlite" for i in range(len(paths)))
        backup_workers(paths, copies)
        self.assertEqual(scientific_records(paths), scientific_records(copies))
        self.assertEqual(progress_snapshot(worlds, selected, copies, now=snapshot["at"], regime="course"), snapshot)
        independent_records(worlds, selected, copies, snapshot)
        digests = [hashlib.sha256(p.read_bytes()).hexdigest() for p in copies]
        if self.bundle is not None:
            # The archive command runs its fresh-process audit after packaging.
            write_json(self.root / "backup-workers.json", [p.name for p in copies])
        for before, path in zip(digests, copies):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)
        return copies

    def test_every_family_intervention_control_repeat_and_branch_local_prose(self):
        p, s = course_inputs()
        worlds = tuple(w for w in p.main if w.index == 1)
        ids = {w.world_id for w in worlds}
        selected = tuple(b for b in s.main if b.world_id in ids)
        paths = tuple(self.root / f"worker-{i}.sqlite" for i in range(2))
        with LocalScheduler(tuple(WorkerSpec(path, provider_factory) for path in paths), worlds, selected,
                tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS, reverse=True, worker_rotation=1) as scheduler:
            scheduler.run()
        snapshot = progress_snapshot(worlds, selected, paths, regime="course")
        for key, value in dict(scheduled_logical=2170, scheduled_generations=1978, finished_logical=2170,
                               attempts=1978, replay_uses=192, retries=0, unknown_logical=0, completed_worlds=5).items():
            self.assertEqual(snapshot["counts"][key], value)
        self.assertEqual({b.task for b in selected}, set(Task))
        self.assertEqual({b.replicate for b in selected}, {0, 1})
        self.assertEqual({b.policy for b in selected if b.phase == "continuation"},
            {"L", "B", "C", "K", "F", "P_G", "P_H", "B_delta", "C_delta", "K_delta", "Q_B", "Q_C"})
        self.assertEqual(set(snapshot["counts"]["protocol_outcomes"]), {"valid", "invalid", "failed"})
        self.assertTrue(all(cost["logical_calls"] == 32 for cost in snapshot["policy_costs"] if cost["policy"]))
        states = [deserialize_state(value.encode()) for value in scientific_records(paths)["committed_transitions"]]
        for branch in selected:
            if branch.phase != "continuation":
                continue
            own = [state for state in states if state.branch_id == branch.branch_id]
            initial = next(state for state in own if state.last_slot.phase == "prefix")
            self.assertTrue(all(state.boundary_applied for state in own))
            if branch.policy in ("C", "F", "C_delta", "Q_C"):
                self.assertTrue(all(not peer.history and not peer.feedback and peer.candidate.value is None for peer in initial.peers))
            if branch.policy in ("Q_B", "Q_C"):
                first = next(state for state in own if state.last_slot == Slot("recovery", 1))
                second = next(state for state in own if state.last_slot == Slot("recovery", 2))
                self.assertTrue(first.pending)
                self.assertFalse(second.pending)
                for peer in first.peers:
                    self.assertFalse(any(type(item) is ReceivedProse and item.slot == Slot("recovery", 1) for item in peer.history))
                for delivery in first.pending:
                    self.assertEqual(next(d for d in second.deliveries if d.delivery_id == delivery.delivery_id).first_usable, Slot("recovery", 3))
                for peer in second.peers:
                    rounds = [item.slot.round_number for item in peer.history if type(item) is ReceivedProse and item.slot.phase == "recovery"]
                    self.assertEqual(rounds, sorted(rounds))
        self.check_backups(worlds, selected, paths, snapshot)
        self.capture(worlds, selected, paths, snapshot, kind="all-family tiny scripted lifecycle")

    def test_hand_costs_uncertain_retry_replays_failed_slots_and_reopened_backups(self):
        world = sort_world()
        policies = ("B", "C", "K", "F", "P_G", "P_H", "Q_B", "Q_C")
        selected = (prefix_branch(world), *(b for b in branches(world) if b.phase == "control"),
                    *(scheduled(world, "revision", policy) for policy in policies))
        paths = tuple(self.root / f"worker-{i}.sqlite" for i in range(2))
        budget = known_budget()
        with DurableRunner(paths[0], TOKENIZER, provide, scripted=True) as runner:
            runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=budget, regime="course")
            for branch in selected[:7]:
                if branch.phase == "control": runner.run_control(world, branch, settings=SETTINGS)
                else:
                    runner.start(world, branch, settings=SETTINGS)
                    for number in range(1, 5): runner.run_round(branch.branch_id, number)
        with DurableRunner(paths[1], TOKENIZER, provide, scripted=True, dependencies=(paths[0],)) as runner:
            runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=budget, regime="course")
            for branch in selected[7:]:
                runner.start(world, branch, settings=SETTINGS)
                for number in range(1, 5): runner.run_round(branch.branch_id, number)
        retry = scheduled(world, "revision", "B").calls[world.partition[1][0]].call_id
        for index, path in enumerate(paths):
            with closing(WorkerStore(path)) as store:
                con = store.connection
                with con:
                    if index == 0:
                        con.execute("UPDATE attempts SET number=2 WHERE call_id=?", (retry,))
                        con.execute("INSERT INTO attempts(call_id,number,status,started_at,uncertain_completion,observed_seconds) VALUES (?,1,'interrupted',?,1,1)", (retry, clock(0)))
                    rows = con.execute("SELECT * FROM attempts ORDER BY call_id,number").fetchall()
                    cursor = 0
                    for row in rows:
                        uncertain = row["call_id"] == retry and row["number"] == 1
                        duration = 3 if uncertain else 2
                        con.execute("UPDATE attempts SET started_at=?,finished_at=?,elapsed_seconds=?,observed_seconds=?,recovered_at=?,peak_memory_bytes=? WHERE call_id=? AND number=?",
                            (clock(cursor), None if uncertain else clock(cursor+duration), None if uncertain else duration,
                             1 if uncertain else duration, clock(cursor+duration) if uncertain else None, 1000+index, row["call_id"], row["number"]))
                        cursor += duration
                    first = rows[0]
                    con.execute("INSERT INTO provider_processes(call_id,number,pid,started_at,ready_at,last_observed_at,stopped_at) VALUES (?,?,1,?,?,?,?)",
                        (first["call_id"], first["number"], clock(0), clock(1), clock(180), clock(180)))
                allocation = store.allocation_started(f"synthetic:{index}", "development", budget=budget,
                    started_at=clock(0), billing={"billed_hours": 1, "rule": "separate provider rule"})
                store.allocation_stopped(allocation, "synthetic measured fixture", released_at=clock(200))
        snapshot = progress_snapshot((world,), selected, paths, now=clock(200), regime="course")
        self.assertEqual(snapshot["counts"]["scheduled_logical"], 146)
        self.assertEqual(snapshot["counts"]["scheduled_generations"], 130)
        self.assertEqual(snapshot["counts"]["attempts"], 131)
        self.assertEqual(snapshot["counts"]["replay_uses"], 16)
        self.assertEqual(snapshot["counts"]["uncertain_attempts"], 1)
        self.assertEqual(snapshot["physical"]["attempt_seconds"], [261, 263])
        self.assertEqual(snapshot["resources"]["partition_seconds"], dict(setup=2, interruption=1, attempt=258, uncertain_work=2, idle=137))
        self.assertEqual(snapshot["resources"]["allocated_gpu_hours"], 400/3600)
        self.assertEqual(snapshot["counts"]["unknown_logical"], 0)
        # A GPU budget cannot use these synthetic allocation or duration records.
        with self.assertRaisesRegex(ValueError, "budget differs"):
            progress_snapshot((world,), selected, paths, now=clock(200), budget=known_budget(allocation_mode="gpu"))
        before = scientific_records(paths)
        self.check_backups((world,), selected, paths, snapshot)
        digests = [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]
        self.assertEqual(progress_snapshot((world,), selected, paths, now=clock(200), regime="course"), snapshot)
        self.assertEqual(scientific_records(paths), before)
        self.assertEqual([hashlib.sha256(path.read_bytes()).hexdigest() for path in paths], digests)
        self.capture((world,), selected, paths, snapshot, kind="independent hand accounting", synthetic_allocated_seconds=400)

    def test_budget_deadline_preserves_unknowns_releases_and_resumes_original_course_scope(self):
        world = sort_world()
        selected = (prefix_branch(world),)
        path = self.root / "worker-0.sqlite"
        budget = known_budget(ceiling_gpu_hours=90/3600, shutdown_seconds=3)
        releases = []
        def release(index, device):
            releases.append((index, device))
            return True
        def scheduler(factory):
            return LocalScheduler((WorkerSpec(path, factory, allocated_device="synthetic:0"),), (world,), selected,
                tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
                budget=budget, release_device=release, allocation_stage="validation")
        with scheduler(partial(provider_factory, delay=2)) as run:
            run.dispatch()
            deadline = monotonic()+15
            while not run.readers[0].store.connection.execute("SELECT 1 FROM provider_processes WHERE ready_at IS NOT NULL").fetchone():
                self.assertLess(monotonic(), deadline)
                sleep(.02)
            run.deadline = monotonic()+.1
            with self.assertRaisesRegex(BudgetStop, "allocation_deadline"):
                run.run()
        stopped = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertEqual(stopped["counts"]["finished_logical"], 0)
        self.assertEqual(stopped["counts"]["unknown_logical"], 16)
        self.assertEqual(stopped["counts"]["attempts"], 1)
        self.assertFalse(stopped["resources"]["active_devices"])
        self.assertEqual(stopped["work"][0]["completed_round"], 0)
        self.assertTrue(all(row["correct"] is None for row in offline_preview((world,), selected, (path,))["outcomes"]))
        stopped_path = self.root / "stopped.sqlite"
        backup_workers((path,), (stopped_path,))
        if self.bundle is not None:
            write_json(self.root / "stopped-progress.json", stopped)
        with scheduler(provider_factory) as run:
            run.run()
        resumed = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertEqual(resumed["counts"]["finished_logical"], 16)
        self.assertEqual(resumed["counts"]["attempts"], 17)
        self.assertEqual(resumed["counts"]["retries"], 1)
        self.assertEqual(resumed["counts"]["uncertain_attempts"], 1)
        self.assertLess(resumed["resources"]["allocated_gpu_hours"], budget.ceiling_gpu_hours)
        self.assertEqual(releases, [(0, "synthetic:0"), (0, "synthetic:0")])
        baseline = self.root / "baseline.sqlite"
        with DurableRunner(baseline, TOKENIZER, provide, scripted=True) as runner:
            runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=budget, regime="course")
            runner.start(world, selected[0], settings=SETTINGS)
            for number in range(1, 5): runner.run_round(selected[0].branch_id, number)
        self.assertEqual(scientific_records((path,)), scientific_records((baseline,)))
        self.assertEqual(stable_progress(resumed), stable_progress(progress_snapshot((world,), selected, (baseline,))))
        self.check_backups((world,), selected, (path,), resumed)
        self.capture((world,), selected, (path,), resumed, kind="safe budget stop/resume", stopped_worker=stopped_path.name)


if __name__ == "__main__":
    unittest.main()
