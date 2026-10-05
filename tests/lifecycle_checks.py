"""Real killed-process acceptance and ordinary offline-readable M3 run bundles."""

from contextlib import closing
from dataclasses import asdict
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

import recovery.runner as runner_module
from recovery.accounting import Budget, BudgetStop
from recovery.attempts import ProcessProvider
from recovery.rounds import deserialize_state, snapshot_bytes
from recovery.runner import DurableRunner, WorkerReader
from recovery.state import OwnReply, ReceivedProse, Slot
from recovery.storage import WorkerStore
from recovery.tasks import Size, Task
from recovery.workers import LocalScheduler, WorkerSpec, _own_file
from tests.accounting_checks import slow_factory
from tests.attempt_checks import process_alive, read_trace
from tests.durable_checks import forbidden
from tests.event_checks import case_world, population, scheduled
from tests.lifecycle_fixture import (BOUNDS, backup_workers, offline_preview, progress,
    provide, provider_factory, schedules, scientific_records, stable_progress, tiny,
    tokenizer_factory, write_json)
from tests.replay_checks import SETTINGS
from tests.round_checks import TOKENIZER


class LifecycleTests(unittest.TestCase):
    # The archive entry point retains the same normal worker files used by tests.
    bundle = None
    evidence = {}

    def setUp(self):
        if self.bundle is None:
            temp = tempfile.TemporaryDirectory()
            self.addCleanup(temp.cleanup)
            self.root = Path(temp.name)
        else:
            self.root = Path(self.bundle) / self._testMethodName
            self.root.mkdir()

    def capture(self, directory, worlds, branches, paths, **details):
        snapshot = progress(worlds, branches, paths)
        write_json(directory / "selection.json", {"size": worlds[0].world.size.value,
            "world_ids": [w.world_id for w in worlds], "branch_ids": [b.branch_id for b in branches]})
        write_json(directory / "progress.json", snapshot)
        write_json(directory / "offline-preview.json", offline_preview(worlds, branches, paths))
        case = {"directory": str(directory.relative_to(self.root.parent)) if self.bundle else directory.name,
                "workers": [p.name for p in paths], "counts": snapshot["counts"], **details}
        self.evidence[case["directory"]] = case
        return snapshot

    def assert_backups(self, directory, worlds, branches, paths):
        restored = tuple(directory / f"backup-{i}.sqlite" for i in range(len(paths)))
        backup_workers(paths, restored)
        self.assertEqual(scientific_records(paths), scientific_records(restored))
        snapshot = progress(worlds, branches, paths)
        self.assertEqual(snapshot, progress(worlds, branches, restored, now=snapshot["at"]))
        for path in restored:
            with closing(WorkerStore(path, readonly=True)) as store:
                self.assertEqual(store.connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        # Close/reopen and explicit lost-acknowledgement operations cannot generate.
        for i, path in enumerate(restored):
            with DurableRunner(path, TOKENIZER, forbidden, scripted=True,
                    dependencies=tuple(p for j, p in enumerate(restored) if j != i)) as runner:
                owned = {r[0] for r in runner.store.connection.execute("SELECT DISTINCT branch_id FROM calls")}
                for branch in branches:
                    if branch.branch_id not in owned:
                        continue
                    if branch.phase == "control":
                        world = next(w for w in worlds if w.world_id == branch.world_id)
                        runner.run_control(world, branch, settings=SETTINGS)
                    else:
                        state = runner.state(branch.branch_id)
                        if state.last_slot is not None and state.last_slot.phase == state.phase:
                            runner.run_round(branch.branch_id, state.last_slot.round_number)
        self.assertEqual(scientific_records(paths), scientific_records(restored))
        self.assertEqual(snapshot, progress(worlds, branches, restored, now=snapshot["at"]))
        return [p.name for p in restored]

    def test_every_family_intervention_control_and_repeat_at_both_sizes(self):
        for size in Size:
            with self.subTest(size=size):
                directory = self.root / size.value
                directory.mkdir()
                worlds, branches = tiny(size)
                paths = tuple(directory / f"worker-{i}.sqlite" for i in range(2))
                workers = tuple(WorkerSpec(path, provider_factory) for path in paths)
                with LocalScheduler(workers, worlds, branches, tokenizer_factory, settings=SETTINGS,
                                    **BOUNDS, reverse=size is Size.FALLBACK, worker_rotation=1) as scheduler:
                    scheduler.run()
                snapshot = progress(worlds, branches, paths)
                self.assertEqual(snapshot["counts"]["scheduled_logical"], 2170)
                self.assertEqual(snapshot["counts"]["scheduled_generations"], 1978)
                self.assertEqual(snapshot["counts"]["finished_logical"], 2170)
                self.assertEqual(snapshot["counts"]["attempts"], 1978)
                self.assertEqual(snapshot["counts"]["replay_uses"], 192)
                self.assertEqual(snapshot["counts"]["retries"], 0)
                self.assertEqual(snapshot["counts"]["unknown_logical"], 0)
                self.assertEqual(snapshot["counts"]["completed_worlds"], 5)
                self.assertEqual(set(snapshot["counts"]["protocol_outcomes"]), {"valid", "invalid", "failed"})
                self.assertEqual({b.task for b in branches}, set(Task))
                self.assertEqual({b.replicate for b in branches}, {0, 1})
                records = scientific_records(paths)
                calls = {r["call_id"]: r for r in records["calls"]}
                attempts = {}
                for path in paths:
                    with closing(WorkerStore(path, readonly=True)) as store:
                        attempts.update({r["call_id"]: dict(r) for r in store.connection.execute("SELECT * FROM attempts")})
                measured = sum(a["elapsed_seconds"] for a in attempts.values())
                for value in snapshot["physical"]["attempt_seconds"]:
                    self.assertAlmostEqual(value, measured)
                self.assertEqual(snapshot["physical"]["request_tokens"], sum(calls[i]["request_tokens"] for i in attempts))
                self.assertEqual(snapshot["physical"]["output_tokens"], sum(len(json.loads(calls[i]["raw_json"])["token_ids"])
                    for i in attempts if calls[i]["raw_json"] is not None))
                by_branch = {b.branch_id: b for b in branches}
                for policy in snapshot["policy_costs"]:
                    branch = by_branch[policy["branch_id"]]
                    used = (*by_branch[branch.prefix_parent].calls, *branch.calls) if branch.prefix_parent else branch.calls
                    expected = sum(attempts[c.generation_id]["elapsed_seconds"] for c in used)
                    self.assertAlmostEqual(policy["seconds"][0], expected)
                    self.assertAlmostEqual(policy["seconds"][1], expected)
                    self.assertEqual(policy["request_tokens"], sum(calls[c.generation_id]["request_tokens"] for c in used))
                for row in calls.values():
                    self.assertIsNotNone(row["validation_json"])
                    if row["replay_parent"]:
                        parent = calls[row["replay_parent"]]
                        self.assertEqual(row["generation_id"], parent["call_id"])
                        self.assertEqual(row["validation_json"], parent["validation_json"])
                        self.assertIsNone(row["raw_json"])
                        self.assertIsNone(row["failure_json"])
                states = [deserialize_state(s.encode("utf-8")) for s in records["committed_transitions"]]
                for branch in branches:
                    if branch.phase != "continuation":
                        continue
                    own = [s for s in states if s.branch_id == branch.branch_id]
                    initial = next(s for s in own if s.last_slot.phase == "prefix")
                    self.assertTrue(initial.boundary_applied)
                    self.assertTrue(all(s.boundary_applied for s in own))
                    self.assertTrue(all(p.notice == initial.peers[i].notice and p.receipt == initial.peers[i].receipt
                                        for s in own for i, p in enumerate(s.peers)))
                    if branch.policy in ("C", "F", "C_delta", "Q_C"):
                        self.assertTrue(all(not p.history and not p.feedback and p.candidate.value is None for p in initial.peers))
                    if branch.policy in ("Q_B", "Q_C"):
                        first = next(s for s in own if s.last_slot == Slot("recovery", 1))
                        second = next(s for s in own if s.last_slot == Slot("recovery", 2))
                        self.assertTrue(first.pending)
                        self.assertTrue(all(d.text is not None and d.first_usable is None for d in first.pending))
                        self.assertFalse(second.pending)
                        parent = next(b for b in branches if b.world_id == branch.world_id and
                            b.event == branch.event and b.replicate == branch.replicate and b.policy == branch.policy[2:])
                        parent_first = next(s for s in states if s.branch_id == parent.branch_id and s.last_slot == Slot("recovery", 1))
                        for peer, comparison in zip(first.peers, parent_first.peers):
                            self.assertEqual(peer.sources, comparison.sources)
                            self.assertEqual(peer.source_deliveries, comparison.source_deliveries)
                            self.assertEqual(peer.candidate, comparison.candidate)
                            self.assertEqual([e for e in peer.history if type(e) is OwnReply and e.slot == Slot("recovery", 1)],
                                             [e for e in comparison.history if type(e) is OwnReply and e.slot == Slot("recovery", 1)])
                        for peer in first.peers:
                            self.assertFalse(any(type(e) is ReceivedProse and e.slot == Slot("recovery", 1) for e in peer.history))
                        for d in first.pending:
                            released = next(x for x in second.deliveries if x.delivery_id == d.delivery_id)
                            self.assertEqual(released.first_usable, Slot("recovery", 3))
                        for peer in second.peers:
                            received = [e.slot.round_number for e in peer.history if type(e) is ReceivedProse and e.slot.phase == "recovery"]
                            self.assertEqual(received, sorted(received))
                self.assertTrue(all(p["logical_calls"] == 32 for p in snapshot["policy_costs"]
                                    if next(b for b in branches if b.branch_id == p["branch_id"]).phase == "continuation"))
                backups = self.assert_backups(directory, worlds, branches, paths)
                self.capture(directory, worlds, branches, paths, backups=backups)

    def test_full_main_and_development_manifests_reconcile_without_executing(self):
        directory = self.root / "manifests"
        directory.mkdir()
        summaries = []
        for size in Size:
            prepared, saved = population(size), schedules(size)
            for count, distinct, logical in ((60, 16152, 17656), (40, 11504, 12560)):
                snapshot = progress(prepared.worlds(count), saved.main_for(prepared, count), (directory / "absent.sqlite",))
                self.assertEqual(snapshot["counts"]["scheduled_generations"], distinct)
                self.assertEqual(snapshot["counts"]["scheduled_logical"], logical)
                self.assertEqual(snapshot["counts"]["unknown_logical"], logical)
                self.assertEqual(snapshot["counts"]["attempts"], 0)
                summaries.append({"size": size.value, "stage": "main", "worlds": count, "counts": snapshot["counts"]})
            snapshot = progress(prepared.development, saved.development, (directory / "absent.sqlite",))
            self.assertEqual(snapshot["counts"]["scheduled_generations"], 1114)
            self.assertEqual(snapshot["counts"]["scheduled_logical"], 1178)
            self.assertEqual(snapshot["counts"]["unknown_logical"], 1178)
            self.assertEqual(len(saved.capability), 90)
            summaries.append({"size": size.value, "stage": "development", "counts": snapshot["counts"]})
        self.assertFalse((directory / "absent.sqlite").exists())
        write_json(directory / "reconciliation.json", summaries)
        self.evidence["manifest_reconciliation"] = summaries

    def prepare_crash(self, directory, policy="Q_B", completed=1, mode="normal", timeout=8):
        directory.mkdir()
        world = case_world(Task.SORT)
        from tests.durable_checks import prefix_branch
        prefix = prefix_branch(world)
        parents = tuple(scheduled(world, "revision", p) for p in ("B", "C", "K") if p != policy)
        branch = scheduled(world, "revision", policy)
        branches = (prefix, *parents, branch)
        parent, seed, baseline = (directory / name for name in
                                  ("worker-parent.sqlite", "worker-killed.sqlite", "worker-baseline.sqlite"))
        with DurableRunner(parent, TOKENIZER, provide, scripted=True) as runner:
            runner.start(world, prefix, settings=SETTINGS)
            for r in range(1, 5):
                runner.run_round(prefix.branch_id, r)
            for b in parents:
                runner.start(world, b, settings=SETTINGS)
                runner.run_round(b.branch_id, 1)
        with DurableRunner(seed, TOKENIZER, provide, scripted=True, dependencies=(parent,)) as runner:
            if completed:
                runner.start(world, branch, settings=SETTINGS)
                for r in range(1, completed + 1):
                    runner.run_round(branch.branch_id, r)
            runner.backup(baseline)
        with DurableRunner(baseline, TOKENIZER, partial(provide, mode=mode, timeout=timeout),
                           scripted=True, dependencies=(parent,)) as runner:
            runner.start(world, branch, settings=SETTINGS)
            for r in range(1, 5):
                runner.run_round(branch.branch_id, r)
        return world, branches, branch, parent, seed, baseline

    def kill(self, directory, path, parent, branch, point, r, peer=0, serial=0):
        marker, trace, output = (directory / f"{name}-{serial}.{suffix}" for name, suffix in
                                 (("boundary", "json"), ("physical", "jsonl"), ("controller", "log")))
        command = [sys.executable, "-m", "tests.lifecycle_worker", "--path", str(path), "--parent", str(parent),
            "--marker", str(marker), "--trace", str(trace), "--policy", branch.policy,
            "--round", str(r), "--peer", str(peer), "--point", point]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in sys.path if p))
        with output.open("xb") as log:
            controller = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, env=env)
            try:
                deadline = monotonic() + 20
                while not marker.exists():
                    if controller.poll() is not None:
                        self.fail(output.read_text(encoding="utf-8"))
                    self.assertLess(monotonic(), deadline, "controller did not reach requested crash boundary")
                    sleep(0.02)
                # Reading after an exclusive write completes avoids partial JSON.
                detail = None
                while detail is None:
                    try:
                        detail = json.loads(marker.read_text(encoding="utf-8"))
                    except json.JSONDecodeError:
                        self.assertLess(monotonic(), deadline)
                        sleep(0.01)
                self.assertEqual(detail["sqlite"], {"ledger": ["wal", 2], "checkpoint": ["wal", 2]})
                self.assertEqual(Path(detail["runner_module"]).resolve(), Path(runner_module.__file__).resolve())
                with closing(WorkerStore(path, readonly=True)) as store:
                    pids = [row[0] for row in store.connection.execute(
                        "SELECT pid FROM provider_processes WHERE stopped_at IS NULL AND recovered_at IS NULL")]
                    at_kill = [dict(row) for row in store.connection.execute("SELECT * FROM calls ORDER BY call_id")]
                before = scientific_records((parent,))
                controller.kill()
                code = controller.wait(timeout=5)
                self.assertNotEqual(code, 0)
                deadline = monotonic() + 5
                while any(process_alive(pid) for pid in pids) and monotonic() < deadline:
                    sleep(0.02)
                self.assertTrue(all(not process_alive(pid) for pid in pids), "inference survived killed owner")
                self.assertEqual(before, scientific_records((parent,)))
                # Confirm the dead owner's OS lock is available before relocation.
                with _own_file(path):
                    pass
                write_json(directory / f"kill-{serial}.json", {"command": command, "exit_code": code,
                    "provider_pids": pids, "marker": marker.name, "calls_at_kill": at_kill})
                return detail, trace
            finally:
                if controller.poll() is None:
                    controller.kill()
                controller.wait(timeout=5)

    def resume_compare(self, directory, data, *, timeout=8, retries=0, uncertain=0):
        world, branches, branch, parent, killed, baseline = data
        relocated = directory / "worker-resumed.sqlite"
        backup_workers((killed,), (relocated,))
        parent_before = scientific_records((parent,))
        provider = ProcessProvider(provider_factory, **dict(BOUNDS, timeout_seconds=timeout))
        with _own_file(relocated), DurableRunner(relocated, TOKENIZER, provider, dependencies=(parent,)) as runner:
            initial = runner.start(world, branch, settings=SETTINGS)
            self.assertTrue(initial.boundary_applied)
            for r in range(1, 5):
                runner.run_round(branch.branch_id, r)
            # Repeat start after progress; clearing or applying the event again is forbidden.
            final = runner.state(branch.branch_id)
            self.assertEqual(runner.start(world, branch, settings=SETTINGS), final)
        self.assertEqual(parent_before, scientific_records((parent,)))
        self.assertEqual(scientific_records((parent, baseline)), scientific_records((parent, relocated)))
        reference = progress((world,), branches, (parent, baseline))
        actual = progress((world,), branches, (parent, relocated))
        self.assertEqual(stable_progress(reference), stable_progress(actual))
        self.assertEqual(offline_preview((world,), branches, (parent, baseline)),
                         offline_preview((world,), branches, (parent, relocated)))
        self.assertEqual(actual["counts"]["retries"], retries)
        self.assertEqual(actual["counts"]["uncertain_attempts"], uncertain)
        for path in (parent, relocated):
            with closing(WorkerStore(path, readonly=True)) as store:
                self.assertLessEqual(store.connection.execute("SELECT MAX(number) FROM attempts").fetchone()[0], 2)
        backups = self.assert_backups(directory, (world,), branches, (parent, relocated))
        self.capture(directory, (world,), branches, (parent, relocated), baseline=baseline.name,
                     backups=backups, comparisons="all literal calls/barriers/committed transitions/deliveries/outcomes equal")
        return relocated

    def test_kill_before_raw_with_held_prose_retains_uncertainty_and_exact_retry_inputs(self):
        directory = self.root / "before_raw"
        data = self.prepare_crash(directory)
        world, branches, branch, parent, killed, baseline = data
        reader = WorkerReader(killed)
        try:
            held = snapshot_bytes(reader.state(branch.branch_id))
            self.assertTrue(reader.state(branch.branch_id).pending)
        finally:
            reader.close()
        _, trace = self.kill(directory, killed, parent, branch, "before_raw", 2)
        with closing(WorkerStore(killed, readonly=True)) as store:
            row = store.call(branch.calls[4].call_id)
            self.assertEqual(row["status"], "running")
            self.assertIsNone(row["raw_json"])
        reader = WorkerReader(killed)
        try:
            self.assertEqual(snapshot_bytes(reader.state(branch.branch_id)), held)
        finally:
            reader.close()
        relocated = self.resume_compare(directory, data, retries=1, uncertain=1)
        first = next(e for e in read_trace(trace) if e["event"] == "generation")
        with closing(WorkerStore(relocated, readonly=True, parents=())) as store:
            _, settings, requests = store.inputs(branch.branch_id, 2)
            self.assertEqual(first["seed"], branch.calls[4].seed)
            self.assertEqual(first["settings"], json.loads(settings))
            for k, value in (("view", requests.views[0]), ("rendered", requests.rendered[0]), ("tokenized", requests.tokenized[0])):
                self.assertEqual(first[k], json.loads(json.dumps(asdict(value))))
            attempts = store.attempts(branch.calls[4].call_id)
            self.assertEqual([a["status"] for a in attempts], ["interrupted", "completed"])
            self.assertIsNone(attempts[0]["finished_at"])
            self.assertIsNone(attempts[0]["elapsed_seconds"])
            self.assertGreater(attempts[0]["observed_seconds"], 0)

    def test_kill_after_durable_invalid_and_known_timeout_never_resamples(self):
        for point, peer, mode, timeout in (("after_raw", 1, "normal", 8), ("after_timeout", 0, "timeout", 2)):
            with self.subTest(point=point):
                directory = self.root / point
                data = self.prepare_crash(directory, mode=mode, timeout=timeout)
                _, _, branch, parent, killed, _ = data
                self.kill(directory, killed, parent, branch, point, 2, peer)
                with closing(WorkerStore(killed, readonly=True)) as store:
                    raw = store.response(branch.calls[4 + peer].call_id)
                    self.assertIsNone(store.call(branch.calls[4 + peer].call_id)["validation_json"])
                relocated = self.resume_compare(directory, data, timeout=timeout)
                with closing(WorkerStore(relocated, readonly=True)) as store:
                    self.assertEqual(store.response(branch.calls[4 + peer].call_id), raw)
                    self.assertEqual(len(store.attempts(branch.calls[4 + peer].call_id)), 1)
                reader = WorkerReader(relocated)
                try:
                    # An invalid/failed generating slot cannot inherit its prior valid candidate.
                    before_three = reader.store.inputs(branch.branch_id, 3)[2].before
                    self.assertIsNone(before_three.peers[peer].candidate.value)
                finally:
                    reader.close()

    def test_kill_during_cross_worker_replay_validation_and_staging(self):
        for point, policy, r, completed in (("validation", "P_G", 1, 0), ("staging", "Q_C", 2, 1)):
            with self.subTest(point=point):
                directory = self.root / point
                data = self.prepare_crash(directory, policy, completed)
                _, _, branch, parent, killed, _ = data
                self.kill(directory, killed, parent, branch, point, r)
                if r == 1:
                    with closing(WorkerStore(killed, readonly=True)) as store:
                        self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0], 0)
                self.resume_compare(directory, data)

    def test_kill_before_and_after_q_delivery_checkpoint_preserves_chronological_release(self):
        for point in ("before_checkpoint", "after_checkpoint"):
            with self.subTest(point=point):
                directory = self.root / point
                data = self.prepare_crash(directory)
                _, _, branch, parent, killed, _ = data
                self.kill(directory, killed, parent, branch, point, 2)
                reader = WorkerReader(killed)
                try:
                    state = reader.state(branch.branch_id)
                    self.assertEqual(state.last_slot.round_number, 1 if point == "before_checkpoint" else 2)
                    self.assertEqual(bool(state.pending), point == "before_checkpoint")
                finally:
                    reader.close()
                self.resume_compare(directory, data)

    def test_kill_after_c_and_f_boundary_does_not_restore_cleared_fields_or_repeat_event(self):
        for policy in ("C", "F"):
            with self.subTest(policy=policy):
                directory = self.root / policy
                data = self.prepare_crash(directory, policy, 0)
                _, _, branch, parent, killed, _ = data
                self.kill(directory, killed, parent, branch, "after_boundary", 1)
                reader = WorkerReader(killed)
                try:
                    state = reader.state(branch.branch_id)
                    self.assertTrue(state.boundary_applied)
                    self.assertTrue(all(not p.history and not p.feedback and p.candidate.value is None for p in state.peers))
                    if policy == "F":
                        self.assertTrue(all(all(s.owner == i or s.record_id == state.peers[i].notice.source.record_id for s in p.sources)
                                            for i, p in enumerate(state.peers)))
                finally:
                    reader.close()
                self.resume_compare(directory, data)

    def test_two_real_precommit_kills_exhaust_retry_without_a_third_attempt(self):
        directory = self.root / "exhausted"
        data = self.prepare_crash(directory, mode="exhausted")
        _, _, branch, parent, killed, _ = data
        self.kill(directory, killed, parent, branch, "before_raw", 2)
        self.kill(directory, killed, parent, branch, "before_raw", 2, serial=1)
        relocated = self.resume_compare(directory, data, retries=1, uncertain=2)
        with closing(WorkerStore(relocated, readonly=True)) as store:
            self.assertEqual(store.call(branch.calls[4].call_id)["status"], "infrastructure_failure")
            self.assertEqual([a["status"] for a in store.attempts(branch.calls[4].call_id)], ["interrupted", "interrupted"])

    def test_synthetic_budget_stop_retains_unknown_slots_and_resumes_same_configuration(self):
        directory = self.root / "budget"
        directory.mkdir()
        world = case_world(Task.SORT)
        from tests.durable_checks import prefix_branch
        branch = prefix_branch(world)
        path = directory / "worker-0.sqlite"
        budget = Budget(ceiling_gpu_hours=90 / 3600, development_reserve_gpu_hours=0,
            setup_reserve_gpu_hours=0, interruption_reserve_gpu_hours=0,
            shutdown_seconds=3, allocation_mode="synthetic")
        releases = []
        def release(index, device):
            releases.append((index, device))
            return True
        def scheduler(factory):
            return LocalScheduler((WorkerSpec(path, factory, allocated_device="synthetic:lifecycle"),),
                (world,), (branch,), tokenizer_factory, settings=SETTINGS, **BOUNDS,
                budget=budget, release_device=release, allocation_stage="validation")
        with scheduler(partial(slow_factory, hung=True)) as run:
            run.dispatch()
            deadline = monotonic() + 15
            while not run.readers[0].store.connection.execute("SELECT 1 FROM provider_processes WHERE ready_at IS NOT NULL").fetchone():
                self.assertLess(monotonic(), deadline)
                sleep(0.02)
            run.deadline = monotonic() + 0.1
            with self.assertRaises(BudgetStop):
                run.run()
        stopped = progress((world,), (branch,), (path,))
        self.assertEqual(stopped["counts"]["finished_logical"], 0)
        self.assertEqual(stopped["counts"]["unknown_logical"], 16)
        self.assertEqual(stopped["counts"]["attempts"], 1)
        self.assertFalse(stopped["resources"]["active_devices"])
        preview = offline_preview((world,), (branch,), (path,))
        self.assertTrue(all(r["correct"] is None for r in preview["outcomes"]))
        write_json(directory / "stopped-progress.json", stopped)
        write_json(directory / "stopped-preview.json", preview)
        stopped_path = directory / "worker-stopped.sqlite"
        backup_workers((path,), (stopped_path,))
        with scheduler(provider_factory) as run:
            run.run()
        final = progress((world,), (branch,), (path,))
        self.assertEqual(final["counts"]["finished_logical"], 16)
        self.assertEqual(final["counts"]["attempts"], 17)
        self.assertEqual(final["counts"]["retries"], 1)
        self.assertEqual(final["counts"]["uncertain_attempts"], 1)
        self.assertFalse(final["resources"]["active_devices"])
        self.assertEqual(releases, [(0, "synthetic:lifecycle")] * 2)
        self.assertLess(final["resources"]["allocated_gpu_hours"], budget.ceiling_gpu_hours)
        self.assertAlmostEqual(sum(final["resources"]["partition_seconds"].values()),
                               final["resources"]["allocated_gpu_hours"] * 3600)
        backups = self.assert_backups(directory, (world,), (branch,), (path,))
        self.capture(directory, (world,), (branch,), (path,), backups=backups,
                     stopped_counts=stopped["counts"], stopped_workers=[stopped_path.name], allocation_mode="synthetic")


if __name__ == "__main__":
    unittest.main()
