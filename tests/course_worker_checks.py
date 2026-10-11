"""Course worker scope, original parents and real bounded process interruptions."""

from contextlib import closing
from dataclasses import asdict, replace
from functools import partial
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from time import monotonic, sleep
import unittest

from recovery.attempts import ProcessProvider
from recovery.prompts import COURSE_LIMITS
from recovery.replay import held_prose_counts
from recovery.rounds import snapshot_bytes
from recovery.runner import DurableRunner, WorkerReader
from recovery.storage import WorkerStore, record_json
from recovery.tasks import Task
from recovery.workers import LocalScheduler, WorkerInterrupted, WorkerSpec, _own_file
from tests.attempt_checks import process_alive, process_factory, read_trace
from tests.course_worker_cases import (BOUNDS, SETTINGS, TOKENIZER, bind, branches, course_inputs,
    prefix_branch, provide, provider_factory, scheduled, sort_world, tokenizer_factory)
from tests.durable_checks import forbidden
from tests.lifecycle_fixture import backup_workers, progress, scientific_records, stable_progress, write_json


class CourseWorkerTests(unittest.TestCase):
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
        self.world = sort_world()

    def capture(self, directory, worlds, selected, paths, **detail):
        if self.bundle is None:
            return
        snapshot = progress(worlds, selected, paths, settings=SETTINGS)
        write_json(directory / "selection.json", dict(world_ids=[w.world_id for w in worlds],
            branch_ids=[b.branch_id for b in selected], workers=[p.name for p in paths]))
        write_json(directory / "progress.json", snapshot)
        self.evidence.append(dict(directory=directory.relative_to(Path(self.bundle)).as_posix(), **detail))

    def parent(self, directory, selected, bounds=BOUNDS, skip=None):
        path = directory / "parent.sqlite"
        with DurableRunner(path, TOKENIZER, provide, scripted=True) as runner:
            bind(runner.store, (self.world,), selected, bounds)
            prefix = prefix_branch(self.world)
            runner.start(self.world, prefix, settings=SETTINGS)
            for r in range(1, 5):
                runner.run_round(prefix.branch_id, r)
            for branch in selected:
                if branch.policy in ("B", "C", "K") and branch.branch_id != skip:
                    runner.start(self.world, branch, settings=SETTINGS)
                    runner.run_round(branch.branch_id, 1)
        return path

    def test_manifest_regime_default_counts_and_initial_timeout_are_preserved(self):
        root = Path(__file__).resolve().parent / "fixtures"
        specs = (WorkerSpec(self.root / "worker.sqlite", provider_factory),)
        for stage, worlds, generations, logical in (("main", 20, 5752, 6280), ("development", 5, 1114, 1178)):
            scheduler = LocalScheduler.from_manifests(specs, root / "population_course.json",
                root / "schedules_course.json", tokenizer_factory, stage=stage, settings=SETTINGS)
            self.assertEqual((scheduler.regime, len(scheduler.worlds)), ("course", worlds))
            self.assertEqual(sum(len(b.calls) for b in scheduler.branches), logical)
            self.assertEqual(sum(c.replay_parent is None for b in scheduler.branches for c in b.calls), generations)
            self.assertEqual(scheduler.bounds, dict(timeout_seconds=120., termination_seconds=1., heartbeat_seconds=1.))
        scheduler = LocalScheduler.from_manifests(specs, root / "population_target.json",
            root / "schedules_target.json", tokenizer_factory, stage="main", settings={})
        self.assertEqual((scheduler.regime, len(scheduler.worlds)), ("thesis", 60))
        for kwargs in (dict(count=60), dict(regime="thesis")):
            with self.assertRaises(ValueError):
                LocalScheduler.from_manifests(specs, root / "population_course.json", root / "schedules_course.json",
                    tokenizer_factory, stage="main", settings=SETTINGS, **kwargs)
        self.assertFalse(specs[0].database.exists())

    def test_binding_rejects_settings_hidden_input_seed_scope_and_bound_drift(self):
        selected = branches(self.world)
        path = self.root / "worker.sqlite"
        with DurableRunner(path, TOKENIZER, forbidden, scripted=True) as runner:
            bind(runner.store, (self.world,), selected)
            original = runner.store.run_inputs
            for settings in ({}, dict(SETTINGS, revision="foreign"), dict(SETTINGS, model="foreign")):
                with self.assertRaisesRegex(ValueError, "course limits|saved configuration"):
                    runner.store.bind_run((self.world,), selected, settings, BOUNDS, regime="course")
            for kwargs in (dict(regime="thesis"), dict(bounds=dict(BOUNDS, timeout_seconds=121)),
                           dict(settings=dict(SETTINGS, temperature=.5)),
                           dict(worlds=(replace(self.world, edited_owner=(self.world.edited_owner+1)%4),)),
                           dict(branches=(replace(selected[0], calls=(replace(selected[0].calls[0], seed=1),)),))):
                inputs = dict(worlds=(self.world,), branches=selected, settings=SETTINGS, bounds=BOUNDS, regime="course")
                inputs.update(kwargs)
                with self.assertRaisesRegex(ValueError, "saved configuration"):
                    runner.store.bind_run(**inputs)
            changed = replace(self.world, edited_owner=(self.world.edited_owner+1)%4)
            with self.assertRaisesRegex(ValueError, "saved configuration"):
                runner.start(changed, prefix_branch(self.world), settings=SETTINGS)
            self.assertEqual(runner.store.run_inputs, original)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM calls").fetchone()[0], 0)

    def test_cross_worker_replays_keep_failed_invalid_replies_and_independent_q_queues(self):
        selected = (prefix_branch(self.world), *(scheduled(self.world, "revision", p)
            for p in ("B", "C", "P_G", "P_H", "Q_B", "Q_C")))
        parent = self.parent(self.root, selected)
        original = scientific_records((parent,))
        child = self.root / "child.sqlite"
        with DurableRunner(child, TOKENIZER, forbidden, scripted=True, dependencies=(parent,)) as runner:
            bind(runner.store, (self.world,), selected)
            states = []
            for branch in selected[3:]:
                runner.start(self.world, branch, settings=SETTINGS)
                result = runner.run_round(branch.branch_id, 1)
                self.assertEqual([r.candidate.status for r in result.barrier.replies], ["valid", "valid", "invalid", "failed"])
                for call in branch.calls[:4]:
                    self.assertEqual(runner.store.response(call.call_id), runner.store.response(call.replay_parent))
                    self.assertEqual(runner.store.call(call.call_id)["generation_id"], call.replay_parent)
                    self.assertEqual(runner.store.attempts(call.call_id), ())
                    self.assertEqual(len(runner.store.attempts(call.replay_parent)), 1)
                states.append(result.committed)
                self.assertEqual(runner.run_round(branch.branch_id, 1), result)
            self.assertTrue(any(held_prose_counts(states[2])))
            self.assertFalse(any(held_prose_counts(states[0])))
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)
            runner.backup(self.root / "backup.sqlite")
        self.assertEqual(original, scientific_records((parent,)))
        self.assertEqual(scientific_records((child,)), scientific_records((self.root / "backup.sqlite",)))
        self.capture(self.root, (self.world,), selected, (parent, child), case="cross-worker-replays")

    def test_equal_ids_seeds_and_settings_never_authorize_foreign_or_unbound_parents(self):
        selected = (prefix_branch(self.world), scheduled(self.world, "revision", "B"), scheduled(self.world, "revision", "Q_B"))
        parent = self.parent(self.root, selected)
        before = scientific_records((parent,))
        for defect in ("regime", "world", "settings", "branches", "bounds", "unbound"):
            copy = self.root / f"{defect}.sqlite"
            backup_workers((parent,), (copy,))
            with closing(sqlite3.connect(copy)) as db, db:
                data = json.loads(db.execute("SELECT inputs_json FROM run_inputs").fetchone()[0])
                if defect == "unbound":
                    db.execute("DELETE FROM run_inputs")
                else:
                    if defect == "regime": data.pop("regime")
                    elif defect == "world": data["worlds"][0]["edited_owner"] = -1
                    elif defect == "settings": data["settings"]["temperature"] = .5
                    elif defect == "branches": data["branches"].pop()
                    else: data["bounds"]["timeout_seconds"] = 121
                    db.execute("UPDATE run_inputs SET inputs_json=?", (record_json(data),))
            child = self.root / f"child-{defect}.sqlite"
            with DurableRunner(child, TOKENIZER, forbidden, scripted=True, dependencies=(copy,)) as runner:
                bind(runner.store, (self.world,), selected)
                with self.assertRaisesRegex(ValueError, "bundle/configuration"):
                    runner.start(self.world, selected[-1], settings=SETTINGS)
                self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM calls").fetchone()[0], 0)
        # Even an unbound standalone course caller cannot import an unbound parent.
        with DurableRunner(self.root / "unbound-child.sqlite", TOKENIZER, forbidden, scripted=True,
                           dependencies=(self.root / "unbound.sqlite",)) as runner:
            with self.assertRaisesRegex(ValueError, "unbound"):
                runner.start(self.world, selected[-1], settings=SETTINGS)
        self.assertEqual(before, scientific_records((parent,)))

    def test_corrupt_native_request_seed_event_and_outcome_stop_without_effects(self):
        selected = (prefix_branch(self.world), scheduled(self.world, "revision", "B"), scheduled(self.world, "revision", "Q_B"))
        parent = self.parent(self.root, selected)
        for defect in ("tokens", "seed", "event", "validation"):
            copy = self.root / f"{defect}.sqlite"
            backup_workers((parent,), (copy,))
            with closing(sqlite3.connect(copy)) as db, db:
                branch = selected[1]
                if defect == "seed":
                    db.execute("UPDATE calls SET seed=seed+1 WHERE call_id=?", (branch.calls[0].call_id,))
                elif defect == "validation":
                    db.execute("UPDATE calls SET validation_json='{}' WHERE call_id=?", (branch.calls[0].call_id,))
                else:
                    field = "requests_json" if defect == "tokens" else "branch_json"
                    data = json.loads(db.execute(f"SELECT {field} FROM round_inputs WHERE branch_id=?", (branch.branch_id,)).fetchone()[0])
                    if defect == "tokens": data["tokenized"][0]["input_ids"][0] += 1
                    else: data["event"] = "sham"
                    db.execute(f"UPDATE round_inputs SET {field}=? WHERE branch_id=?", (record_json(data), branch.branch_id))
            with DurableRunner(self.root / f"child-{defect}.sqlite", TOKENIZER, forbidden, scripted=True, dependencies=(copy,)) as runner:
                bind(runner.store, (self.world,), selected)
                initial = runner.start(self.world, selected[-1], settings=SETTINGS)
                with self.assertRaises(ValueError): runner.run_round(selected[-1].branch_id, 1)
                self.assertEqual(runner.state(selected[-1].branch_id), initial)
                self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)

    def test_controls_all_saved_worlds_resume_exact_and_local_prefix_checks_settings(self):
        population, schedule = course_inputs()
        selected = tuple(b for b in schedule.main + schedule.development if b.phase == "control")
        path = self.root / "controls.sqlite"
        with DurableRunner(path, TOKENIZER, provide, scripted=True) as runner:
            bind(runner.store, population.main + population.development, selected)
            for branch in selected:
                world = next(w for w in population.main + population.development if w.world_id == branch.world_id)
                result = runner.run_control(world, branch, settings=SETTINGS)
                self.assertTrue(result.protocol_valid)
                self.assertFalse(result.messages)
                self.assertLessEqual(result.output_tokens, COURSE_LIMITS.output_tokens)
            runner.reply_provider = forbidden
            for branch in selected:
                world = next(w for w in population.main + population.development if w.world_id == branch.world_id)
                runner.run_control(world, branch, settings=SETTINGS)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 50)
        self.capture(self.root, population.main + population.development, selected, (path,), case="50-controls")
        # Local parents must check exact settings too, without a worker binding.
        with DurableRunner(self.root / "standalone.sqlite", TOKENIZER, provide, scripted=True) as runner:
            prefix = prefix_branch(self.world)
            runner.start(self.world, prefix, settings=SETTINGS)
            for r in range(1, 5): runner.run_round(prefix.branch_id, r)
            with self.assertRaisesRegex(ValueError, "prefix parent settings"):
                runner.start(self.world, scheduled(self.world, "revision", "B"), settings=dict(SETTINGS, temperature=.5))

    def test_two_workers_reverse_order_resume_and_concurrent_ownership(self):
        selected = branches(self.world)
        reference = None
        for reverse in (False, True):
            directory = self.root / str(reverse)
            paths = tuple(directory / f"worker-{i}.sqlite" for i in range(2))
            specs = tuple(WorkerSpec(p, partial(provider_factory, delay=.003 if i == 0 else .001), f"cpu-{i}") for i, p in enumerate(paths))
            with LocalScheduler(specs, (self.world,), selected, tokenizer_factory, settings=SETTINGS, regime="course",
                                **BOUNDS, reverse=reverse, worker_rotation=int(reverse), invocation_order=(3, 2, 1, 0) if reverse else range(4)) as scheduler:
                with self.assertRaises(WorkerInterrupted):
                    with LocalScheduler(specs, (self.world,), selected, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS): pass
                scheduler.run()
                self.assertTrue(all(w.status == "done" for w in scheduler.status()))
            actual = scientific_records(paths)
            if reference is None: reference = actual
            else: self.assertEqual(actual, reference)
            with LocalScheduler(specs, (self.world,), selected, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS, reverse=not reverse) as scheduler:
                scheduler.run()
            self.assertEqual(scientific_records(paths), actual)
            self.capture(directory, (self.world,), selected, paths, case="two-workers", reverse=reverse)

    def test_course_attempt_failures_exhaust_once_and_completed_invalid_timeout_never_retry(self):
        selected = (prefix_branch(self.world),)
        for mode in ("interrupt_always", "invalid", "hang_first"):
            directory = self.root / mode
            directory.mkdir()
            path, trace = directory / "worker.sqlite", directory / "physical.jsonl"
            bounds = dict(BOUNDS, timeout_seconds=2 if mode == "hang_first" else 8)
            provider = ProcessProvider(partial(process_factory, mode, str(trace)), **bounds)
            with DurableRunner(path, TOKENIZER, provider) as runner:
                bind(runner.store, (self.world,), selected, bounds)
                runner.start(self.world, selected[0], settings=SETTINGS)
                result = runner.run_round(selected[0].branch_id, 1)
                self.assertEqual(len(runner.store.attempts(selected[0].calls[0].call_id)), 2 if mode == "interrupt_always" else 1)
                self.assertEqual(result.barrier.replies[0].candidate.status, "invalid" if mode == "invalid" else "failed")
            with DurableRunner(path, TOKENIZER, forbidden, scripted=True) as runner:
                self.assertEqual(runner.run_round(selected[0].branch_id, 1), result)
            self.capture(directory, (self.world,), selected, (path,), case="bounded-attempt", mode=mode)

    def test_course_overflow_preserves_full_state_and_admits_no_attempt(self):
        class Oversized(type(TOKENIZER)):
            def __call__(self, text, **kwargs):
                result = super().__call__(text, **kwargs)
                result["input_ids"] = [1] * COURSE_LIMITS.context_tokens
                result["attention_mask"] = [1] * COURSE_LIMITS.context_tokens
                return result
        selected = (prefix_branch(self.world),)
        with DurableRunner(self.root / "overflow.sqlite", Oversized(), forbidden, scripted=True) as runner:
            bind(runner.store, (self.world,), selected)
            initial = runner.start(self.world, selected[0], settings=SETTINGS)
            with self.assertRaisesRegex(ValueError, "context|capacity"):
                runner.run_round(selected[0].branch_id, 1)
            self.assertEqual(runner.state(selected[0].branch_id), initial)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM calls").fetchone()[0], 0)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)

    def prepare_crash(self, directory, policy="Q_B", completed=1, timeout=8, mode="normal"):
        directory.mkdir()
        selected = (prefix_branch(self.world), *(scheduled(self.world, "revision", p) for p in ("B", "C") if p != policy),
                    scheduled(self.world, "revision", policy))
        bounds = dict(BOUNDS, timeout_seconds=timeout)
        parent = self.parent(directory, selected, bounds, skip=selected[-1].branch_id)
        killed, baseline = directory / "killed.sqlite", directory / "baseline.sqlite"
        with DurableRunner(killed, TOKENIZER, provide, scripted=True, dependencies=(parent,)) as runner:
            bind(runner.store, (self.world,), selected, bounds)
            if completed:
                runner.start(self.world, selected[-1], settings=SETTINGS)
                for r in range(1, completed+1): runner.run_round(selected[-1].branch_id, r)
            runner.backup(baseline)
        with DurableRunner(baseline, TOKENIZER, partial(provide, mode=mode, timeout=timeout), scripted=True, dependencies=(parent,)) as runner:
            runner.start(self.world, selected[-1], settings=SETTINGS)
            for r in range(1, 5): runner.run_round(selected[-1].branch_id, r)
        return selected, parent, killed, baseline, bounds

    def kill(self, directory, path, parent, branch, point, r, peer=0, serial=0):
        marker, trace, log = (directory / f"{name}-{serial}.{suffix}" for name, suffix in
            (("boundary", "json"), ("physical", "jsonl"), ("controller", "log")))
        command = [sys.executable, "-X", "utf8", "-m", "tests.lifecycle_worker", "--regime", "course",
            "--path", str(path), "--parent", str(parent), "--marker", str(marker), "--trace", str(trace),
            "--policy", branch.policy, "--round", str(r), "--peer", str(peer), "--point", point]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in sys.path if p))
        with log.open("xb") as output:
            controller = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT, env=env)
            try:
                deadline = monotonic()+25
                detail = None
                while detail is None:
                    if controller.poll() is not None: self.fail(log.read_text(encoding="utf-8"))
                    self.assertLess(monotonic(), deadline, "course controller did not reach crash boundary")
                    if marker.exists():
                        try: detail = json.loads(marker.read_bytes())
                        except json.JSONDecodeError: pass
                    sleep(.02)
                self.assertEqual(detail["sqlite"], dict(ledger=["wal", 2], checkpoint=["wal", 2]))
                import recovery.runner
                self.assertEqual(Path(detail["runner_module"]).resolve(), Path(recovery.runner.__file__).resolve())
                with closing(WorkerStore(path, readonly=True)) as store:
                    pids = [r[0] for r in store.connection.execute("SELECT pid FROM provider_processes WHERE stopped_at IS NULL")]
                controller.kill()
                self.assertNotEqual(controller.wait(timeout=5), 0)
                deadline = monotonic()+5
                while any(process_alive(pid) for pid in pids) and monotonic()<deadline: sleep(.02)
                self.assertFalse(any(process_alive(pid) for pid in pids))
                # Windows can finish releasing file locks shortly after the
                # controller handle signals exit. Confirm release, boundedly.
                deadline = monotonic()+5
                while True:
                    try:
                        with _own_file(path): pass
                        break
                    except WorkerInterrupted:
                        self.assertLess(monotonic(), deadline, "dead course owner did not release its OS lock")
                        sleep(.02)
                write_json(directory / f"kill-{serial}.json", dict(command=command, point=point, provider_pids=pids,
                    exit_code=controller.returncode, inference_children_exited=True, owner_lock_released=True))
                return detail, trace
            finally:
                if controller.poll() is None: controller.kill()
                controller.wait(timeout=5)

    def test_real_course_kills_at_raw_validation_staging_boundary_and_delivery_commits(self):
        cases = (("before_raw", "Q_B", 1, 2, 0), ("after_raw", "Q_B", 1, 2, 1),
                 ("validation", "P_G", 0, 1, 0), ("staging", "Q_C", 1, 2, 0),
                 ("before_checkpoint", "Q_B", 1, 2, 0), ("after_checkpoint", "Q_B", 1, 2, 0),
                 ("after_boundary", "C", 0, 1, 0), ("after_timeout", "Q_B", 1, 2, 0))
        for point, policy, completed, r, peer in cases:
            with self.subTest(point=point):
                directory = self.root / point
                timeout = 2 if point == "after_timeout" else 8
                selected, parent, killed, baseline, bounds = self.prepare_crash(directory, policy, completed,
                    timeout, "timeout" if point == "after_timeout" else "normal")
                branch = selected[-1]
                before = scientific_records((parent,))
                if completed:
                    reader = WorkerReader(killed)
                    try: self.assertTrue(any(held_prose_counts(reader.state(branch.branch_id))))
                    finally: reader.close()
                _, trace = self.kill(directory, killed, parent, branch, point, r, peer)
                with closing(WorkerStore(killed, readonly=True)) as store:
                    if point in ("after_raw", "after_timeout"):
                        raw = store.response(branch.calls[(r-1)*4+peer].call_id)
                resumed = directory / "resumed.sqlite"
                backup_workers((killed,), (resumed,))
                with DurableRunner(resumed, TOKENIZER, ProcessProvider(provider_factory, **bounds), dependencies=(parent,)) as runner:
                    runner.start(self.world, branch, settings=SETTINGS)
                    for number in range(1, 5): runner.run_round(branch.branch_id, number)
                    final = runner.state(branch.branch_id)
                    self.assertEqual(runner.start(self.world, branch, settings=SETTINGS), final)
                    target = branch.calls[(r-1)*4+peer].call_id
                    if point in ("after_raw", "after_timeout"):
                        self.assertEqual(runner.store.response(target), raw)
                        self.assertEqual(len(runner.store.attempts(target)), 1)
                    if point == "before_raw":
                        attempts = runner.store.attempts(target)
                        self.assertEqual([a["status"] for a in attempts], ["interrupted", "completed"])
                        self.assertTrue(attempts[0]["uncertain_completion"])
                        self.assertIsNone(attempts[0]["finished_at"])
                        first = next(e for e in read_trace(trace) if e["event"] == "generation")
                        _, saved_settings, requests = runner.store.inputs(branch.branch_id, r)
                        self.assertEqual(first["seed"], branch.calls[(r-1)*4].seed)
                        self.assertEqual(first["settings"], json.loads(saved_settings))
                        for key in ("view", "rendered", "tokenized"):
                            value = getattr(requests, {"view":"views", "rendered":"rendered", "tokenized":"tokenized"}[key])[0]
                            self.assertEqual(first[key], json.loads(record_json(asdict(value))))
                self.assertEqual(before, scientific_records((parent,)))
                self.assertEqual(scientific_records((baseline,)), scientific_records((resumed,)))
                expected = progress((self.world,), selected, (parent, baseline), settings=SETTINGS)
                actual = progress((self.world,), selected, (parent, resumed), settings=SETTINGS)
                self.assertEqual(stable_progress(expected), stable_progress(actual))
                backups = (directory / "backup-parent.sqlite", directory / "backup-resumed.sqlite")
                backup_workers((parent, resumed), backups)
                self.assertEqual(scientific_records((parent, resumed)), scientific_records(backups))
                self.assertEqual(progress((self.world,), selected, backups, settings=SETTINGS, now=actual["at"]), actual)
                for path in backups:
                    with closing(WorkerStore(path, readonly=True)) as store:
                        self.assertEqual(store.connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.capture(directory, (self.world,), selected, (parent, resumed), case="real-kill", point=point)

    def test_two_real_pre_persistence_kills_exhaust_without_third_attempt(self):
        directory = self.root / "two-kills"
        selected, parent, killed, _, bounds = self.prepare_crash(directory, mode="exhausted")
        branch = selected[-1]
        for serial in range(2): self.kill(directory, killed, parent, branch, "before_raw", 2, serial=serial)
        with DurableRunner(killed, TOKENIZER, ProcessProvider(provider_factory, **bounds), dependencies=(parent,)) as runner:
            runner.start(self.world, branch, settings=SETTINGS)
            for r in range(1, 5): runner.run_round(branch.branch_id, r)
            attempts = runner.store.attempts(branch.calls[4].call_id)
            self.assertEqual(len(attempts), 2)
            self.assertTrue(all(a["uncertain_completion"] for a in attempts))
            self.assertEqual(runner.store.call(branch.calls[4].call_id)["status"], "infrastructure_failure")
        self.capture(directory, (self.world,), selected, (parent, killed), case="two-real-kills")


if __name__ == "__main__":
    unittest.main()
