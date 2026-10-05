"""Hand-reconciled CPU accounting, read-only progress and safe allocation stops."""

from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
from functools import partial
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from time import monotonic, sleep
import unittest

from recovery.accounting import Budget, BudgetStop, format_status, progress_snapshot
from recovery.attempts import MeasuredReply, ProcessProvider
from recovery.manifests import load_population, load_schedules
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.storage import RecordedFailure, WorkerStore, record_json
from recovery.tasks import Task
from recovery.workers import LocalScheduler, WorkerSpec
from tests.durable_checks import prefix, provider
from tests.event_checks import case_world
from tests.replay_checks import SETTINGS, replay_provider, scheduled
from tests.round_checks import TOKENIZER, reply
from tests.worker_fixture import tokenizer_factory


BASE = datetime(2026, 10, 5, tzinfo=timezone.utc)


def clock(seconds):
    return (BASE + timedelta(seconds=seconds)).isoformat()


def slow_factory(delay=0, hung=False, measured=False):
    return partial(slow_reply, delay, hung, measured)


def slow_reply(delay, hung, measured, view, rendered, tokenized, *, seed, settings):
    if hung:
        while True:
            sleep(0.01)
    sleep(delay)
    raw = reply(TOKENIZER, view)
    return MeasuredReply(raw, 123456) if measured else raw


def synthetic_budget(seconds=30, **kwargs):
    return Budget(ceiling_gpu_hours=seconds / 3600, development_reserve_gpu_hours=0,
                  setup_reserve_gpu_hours=0, interruption_reserve_gpu_hours=0,
                  shutdown_seconds=3, allocation_mode="synthetic", **kwargs)


class AccountingTests(unittest.TestCase):
    evidence = {}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paths = tuple(Path(self.temp.name) / f"worker-{i}.sqlite" for i in range(2))
        self.world = case_world(Task.SORT)
        branches = _prepare_branches((self.world,))
        self.prefix = next(b for b in branches if b.phase == "prefix")
        self.branches = (self.prefix,) + tuple(scheduled(self.world, "revision", p)
            for p in ("B", "C", "F", "P_G", "Q_B", "Q_C"))

    def make_schedule(self):
        with DurableRunner(self.paths[0], TOKENIZER, provider, scripted=True) as runner:
            prefix(runner, self.world)
            runner.reply_provider = replay_provider(TOKENIZER, "unicode")
            for branch in self.branches[1:4]:
                runner.start(self.world, branch, settings=SETTINGS)
                for r in range(1, 5):
                    runner.run_round(branch.branch_id, r)
        with DurableRunner(self.paths[1], TOKENIZER, replay_provider(TOKENIZER, "unicode"),
                           scripted=True, dependencies=(self.paths[0],)) as runner:
            for branch in self.branches[4:]:
                runner.start(self.world, branch, settings=SETTINGS)
                for r in range(1, 5):
                    runner.run_round(branch.branch_id, r)
        # One retained peer's B first-round response was retried after a measured
        # three-second infrastructure interruption. Its final two-second raw
        # response is replayed by P_G and Q_B. Every other original call is 2s.
        retained = self.world.partition[1][0]
        self.retried = self.branches[1].calls[retained].call_id
        for index, path in enumerate(self.paths):
            store = WorkerStore(path)
            con = store.connection
            with con:
                if index == 0:
                    con.execute("UPDATE attempts SET number=2 WHERE call_id=?", (self.retried,))
                    con.execute("""INSERT INTO attempts
                        (call_id,number,status,started_at,finished_at,elapsed_seconds,observed_seconds,
                         uncertain_completion,termination_reason,reason)
                        VALUES (?,1,'interrupted',?,?,3,3,1,'infrastructure_interruption','synthetic lost reply')""",
                        (self.retried, clock(0), clock(3)))
                cursor = 0
                rows = con.execute("SELECT * FROM attempts ORDER BY call_id,number").fetchall()
                for row in rows:
                    duration = 3 if row["call_id"] == self.retried and row["number"] == 1 else 2
                    con.execute("""UPDATE attempts SET started_at=?,finished_at=?,elapsed_seconds=?,observed_seconds=?,
                        peak_memory_bytes=? WHERE call_id=? AND number=?""",
                        (clock(cursor), clock(cursor + duration), duration, duration, 1000 + index,
                         row["call_id"], row["number"]))
                    cursor += duration
                first = rows[0]
                con.execute("""INSERT INTO provider_processes
                    (call_id,number,pid,started_at,ready_at,last_observed_at,stopped_at,device_visibility)
                    VALUES (?,?,1,?,?,?,?,?)""", (first["call_id"], first["number"], clock(0), clock(1),
                        clock(180), clock(180), str(index)))
            number = store.allocation_started(f"synthetic:{index}", "validation", budget=synthetic_budget(1000),
                billing={"unit": "provider reservation", "billed_hours": 1}, started_at=clock(0))
            store.allocation_stopped(number, "fixture_complete", released_at=clock(200))
            store.close()

    def snapshot(self, **kwargs):
        return progress_snapshot((self.world,), self.branches, self.paths, now=clock(200), **kwargs)

    def test_hand_calculated_physical_policy_replays_f_retry_and_delivery_reconciliation(self):
        self.make_schedule()
        s = self.snapshot()
        self.assertEqual((s["counts"]["scheduled_logical"], s["counts"]["scheduled_generations"],
                          s["counts"]["replay_uses"], s["counts"]["attempts"], s["counts"]["retries"]), (112, 100, 12, 101, 1))
        self.assertEqual(s["physical"]["attempt_seconds"], [203, 203])
        self.assertEqual(s["physical"]["peak_memory_bytes"], 1001)
        policies = {r["policy"]: r for r in s["policy_costs"]}
        for p, seconds in (("B", 67), ("C", 64), ("F", 64), ("P_G", 67), ("Q_B", 67), ("Q_C", 64)):
            self.assertEqual(policies[p]["logical_calls"], 32, p)
            self.assertEqual(policies[p]["seconds"], [seconds, seconds], p)
            self.assertEqual(policies[p]["unknown_calls"], 0)
        self.assertEqual(s["resources"]["allocated_gpu_hours"], 400 / 3600)
        self.assertEqual(s["resources"]["partition_seconds"], {"setup": 2, "interruption": 3,
                         "attempt": 198, "uncertain_work": 0, "idle": 197})
        self.assertEqual(len(s["resources"]["provider_billing"]), 2)
        self.assertEqual(sum(r["cost"]["attempts"] for r in s["logical_slots"] if r["replay_parent"]), 14)
        ids = [d["delivery_id"] for d in s["validated_deliveries"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreater(s["delivery_counts"]["source_attempts"], 0)
        self.assertGreater(s["delivery_counts"]["text_deliveries"], 0)
        self.assertEqual(s["counts"]["finished_logical"], 112)
        self.assertGreater(s["counts"]["recorded_failures"], 0)
        self.assertNotIn("success", format_status(s))
        self.evidence["reconciliation"] = s

    def test_unknown_crash_duration_uses_observation_and_recovery_bounds_without_fabricated_finish(self):
        self.make_schedule()
        con = sqlite3.connect(self.paths[0])
        row = con.execute("SELECT started_at,finished_at FROM attempts WHERE call_id=? AND number=1", (self.retried,)).fetchone()
        with con:
            con.execute("""UPDATE attempts SET elapsed_seconds=NULL,finished_at=NULL,observed_seconds=1,recovered_at=?
                WHERE call_id=? AND number=1""", (row[1], self.retried))
        con.close()
        s = self.snapshot()
        self.assertEqual(s["physical"]["attempt_seconds"], [201, 203])
        self.assertEqual(s["counts"]["uncertain_attempts"], 1)
        self.assertEqual(sum(s["resources"]["partition_seconds"].values()), 400)
        self.assertEqual(s["resources"]["partition_seconds"]["uncertain_work"], 2)
        con = sqlite3.connect(self.paths[0])
        self.assertIsNone(con.execute("SELECT finished_at FROM attempts WHERE call_id=? AND number=1", (self.retried,)).fetchone()[0])
        con.close()
        self.evidence["ambiguous"] = {"physical": s["physical"], "resources": s["resources"]}

    def test_backup_restart_reconstructs_identical_progress_costs_and_committed_deliveries(self):
        self.make_schedule()
        before = self.snapshot()
        backups = []
        for i, path in enumerate(self.paths):
            store = WorkerStore(path, readonly=True)
            backup = Path(self.temp.name) / f"backup-{i}.sqlite"
            store.backup(backup)
            store.close()
            backups.append(backup)
        after = progress_snapshot((self.world,), self.branches, backups, now=clock(200))
        self.assertEqual(before, after)

    def test_no_measurements_no_allocations_are_unavailable_not_zero_cost_or_runtime_percentage(self):
        s = self.snapshot()
        self.assertEqual(s["counts"]["unknown_logical"], 112)
        self.assertFalse(s["forecast"]["available"])
        self.assertIsNone(s["forecast"]["remaining_gpu_hours"])
        self.assertIsNone(s["resources"]["allocated_gpu_hours"])
        self.assertIsNone(s["physical"]["peak_memory_bytes"])
        self.assertTrue(all(not p.exists() for p in self.paths))
        self.assertIn("runtime percentage is unavailable", format_status(s))

    def test_slow_device_forecast_margin_requires_each_device_and_cell_measurements(self):
        # Same phase/condition on two independent worlds gives genuine samples
        # from both devices; the remaining world cannot choose the faster one.
        from recovery.accounting import _forecast
        worlds = [replace(self.world, world_id=f"sample-{i}") for i in range(3)]
        branches = [next(b for b in _prepare_branches((w,)) if b.phase == "control" and b.event == "original") for w in worlds]
        calls, generations = {}, {}
        for i, b in enumerate(branches):
            cid = b.calls[0].call_id
            generations[cid] = {"seconds": [2 if i == 0 else 8, 2 if i == 0 else 8], "unknown_duration_attempts": 0,
                                "device": f"synthetic:{i}", "request_tokens": 100 + i}
            if i < 2:
                calls[cid] = {"status": "completed"}
        forecast = _forecast(branches, calls, generations, ["synthetic:0", "synthetic:1"], None)
        self.assertTrue(forecast["available"])
        self.assertEqual(forecast["remaining_gpu_hours"], [2 / 3600, 10 / 3600])
        self.assertEqual(forecast["elapsed_seconds"], [1, 10])
        self.assertFalse(_forecast(branches, calls, generations, ["synthetic:0", "synthetic:1", "new-device"], None)["available"])
        self.evidence["slower_device_forecast"] = forecast

    def test_idle_device_setup_reserve_and_billing_are_not_double_charged(self):
        for i, path in enumerate(self.paths):
            with DurableRunner(path, None) as runner:
                n = runner.store.allocation_started(f"synthetic:{i}", "development", budget=Budget(allocation_mode="synthetic"), started_at=clock(0))
                runner.store.allocation_stopped(n, "idle_complete", released_at=clock(60))
        s = progress_snapshot((self.world,), self.branches, self.paths, now=clock(60))
        self.assertEqual(s["resources"]["allocated_gpu_hours"], 120 / 3600)
        self.assertEqual(s["resources"]["partition_seconds"]["idle"], 120)
        self.assertEqual(s["resources"]["remaining_reserves_gpu_hours"]["development"], 8 - 120 / 3600)
        self.assertEqual(s["physical"]["attempt_seconds"], [0, 0])

    def test_duplicate_paths_physical_generations_missing_parents_and_overlap_are_rejected(self):
        self.make_schedule()
        with self.assertRaisesRegex(ValueError, "once"):
            progress_snapshot((self.world,), self.branches, self.paths + self.paths, now=clock(200))
        con = sqlite3.connect(self.paths[1])
        with con:
            con.execute("UPDATE allocations SET device='synthetic:0'")
        con.close()
        with self.assertRaisesRegex(ValueError, "same device twice"):
            self.snapshot()
        con = sqlite3.connect(self.paths[0])
        with con:
            con.execute("DELETE FROM calls WHERE call_id=?", (self.retried,))
        con.close()
        with self.assertRaisesRegex(ValueError, "parent|missing"):
            self.snapshot()

    def test_completed_world_and_matched_subset_coverage_uses_committed_horizons_not_correctness(self):
        # Complete all matched cells without executing model or main outcomes.
        self.make_schedule()
        s = self.snapshot()
        self.assertEqual(s["counts"]["completed_worlds"], 1)
        self.assertEqual([r["complete"] for r in s["matched_comparisons"] if r["subset"] == "prose"], [1])
        self.assertGreater(s["counts"]["protocol_outcomes"]["invalid"], 0)
        con = sqlite3.connect(self.paths[1])
        # Delete only a final raw outcome: status must diagnose a broken durable
        # checkpoint, not quietly turn a recorded outcome into completion.
        with con:
            con.execute("DELETE FROM calls WHERE call_id=?", (self.branches[-1].calls[-1].call_id,))
        con.close()
        with self.assertRaisesRegex(ValueError, "checkpoint|committed"):
            self.snapshot()

    def test_full_saved_main_and_development_counts_cli_is_read_only_without_workers(self):
        root = Path(__file__).resolve().parent / "fixtures"
        population = load_population(root / "population_target.json")
        schedules = load_schedules(root / "schedules_target.json", population)
        for count, physical, logical in ((60, 16152, 17656), (40, 11504, 12560)):
            s = progress_snapshot(population.worlds(count), schedules.main_for(population, count), self.paths)
            self.assertEqual((s["counts"]["scheduled_generations"], s["counts"]["scheduled_logical"]), (physical, logical))
            self.assertEqual(s["counts"]["unknown_logical"], logical)
        result = subprocess.run([sys.executable, "-m", "recovery", "status", "--manifest", str(root / "population_target.json"),
            "--schedule", str(root / "schedules_target.json"), "--worker", str(self.paths[0]), "--json"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual((data["counts"]["scheduled_logical"], data["counts"]["scheduled_generations"]), (1178, 1114))
        self.assertFalse(self.paths[0].exists())


class BudgetTests(unittest.TestCase):
    evidence = {}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "worker.sqlite"
        self.world = case_world(Task.SORT)
        self.branch = next(b for b in _prepare_branches((self.world,)) if b.phase == "prefix")
        self.releases = []

    def release(self, index, device):
        self.releases.append((index, device))
        return True

    def scheduler(self, *, factory=None, budget=None, **kwargs):
        return LocalScheduler((WorkerSpec(self.path, factory or partial(slow_factory, delay=0.005),
                                          allocated_device="synthetic:0"),),
            (self.world,), (self.branch,), tokenizer_factory, settings=SETTINGS,
            timeout_seconds=3, termination_seconds=0.5, heartbeat_seconds=0.05,
            budget=budget or synthetic_budget(30), release_device=self.release,
            allocation_stage="validation", **kwargs)

    def snapshot(self):
        return progress_snapshot((self.world,), (self.branch,), (self.path,))

    def test_timeout_boundary_admission_stops_safely_and_retains_finished_failures_and_unknown_slots(self):
        with self.scheduler(factory=partial(slow_factory, hung=True), budget=synthetic_budget(45)) as scheduler:
            with self.assertRaises(BudgetStop):
                scheduler.run()
        s = self.snapshot()
        self.assertEqual(s["counts"]["finished_logical"], 4)
        self.assertEqual(s["counts"]["unknown_logical"], 12)
        self.assertEqual(s["counts"]["protocol_outcomes"], {"failed": 4})
        self.assertEqual(s["counts"]["attempts"], 4)
        self.assertEqual(s["counts"]["retries"], 0)
        self.assertLess(s["resources"]["allocated_gpu_hours"], 45 / 3600)
        self.assertEqual(self.releases, [(0, "synthetic:0")])
        self.assertTrue(set(s["resources"]["stop_reasons"]) <= {"timeout_and_termination_allowance", "remaining_forecast_exceeds_budget"})
        self.assertEqual(s["work"][0]["completed_round"], 1)
        self.evidence["timeout_admission_stop"] = s

    def test_deadline_terminates_hung_generation_with_unknown_raw_outcome_and_resumable_checkpoint(self):
        with self.scheduler(factory=partial(slow_factory, hung=True), budget=synthetic_budget(80)) as scheduler:
            scheduler.dispatch()
            deadline = monotonic() + 10
            while not scheduler.progress()["current"] or not scheduler.readers[0].store.connection.execute(
                    "SELECT 1 FROM provider_processes WHERE ready_at IS NOT NULL").fetchone():
                self.assertLess(monotonic(), deadline)
                sleep(0.01)
            # Synthetic adverse budget boundary, independent of the model
            # timeout. A hard stop must not fabricate a timeout or raw reply.
            scheduler.deadline = monotonic() + 0.15
            with self.assertRaises(BudgetStop):
                scheduler.run()
        s = self.snapshot()
        self.assertEqual(s["counts"]["finished_logical"], 0)
        self.assertEqual(s["counts"]["unknown_logical"], 16)
        self.assertEqual(s["counts"]["attempts"], 1)
        self.assertEqual(s["work"][0]["completed_round"], 0)
        self.assertEqual(s["resources"]["active_devices"], [])
        self.assertIn("allocation_deadline", s["resources"]["stop_reasons"])
        self.evidence["hard_deadline_stop"] = s
        # The same saved bounds/settings/budget resume the single interrupted
        # call, recording ambiguity. Completed outcomes are never resampled.
        with self.scheduler(budget=synthetic_budget(80)) as scheduler:
            scheduler.run()
        resumed = self.snapshot()
        self.assertEqual(resumed["counts"]["finished_logical"], 16)
        self.assertEqual(resumed["counts"]["attempts"], 17)
        self.assertEqual(resumed["counts"]["retries"], 1)
        self.assertEqual(resumed["counts"]["uncertain_attempts"], 1)
        self.evidence["resumed_deadline_stop"] = resumed

    def test_budget_exhaustion_before_first_call_preserves_all_slots_without_loading(self):
        with self.scheduler(budget=synthetic_budget(10)) as scheduler:
            with self.assertRaisesRegex(BudgetStop, "timeout_and_termination"):
                scheduler.run()
        s = self.snapshot()
        self.assertEqual(s["counts"]["attempts"], 0)
        self.assertEqual(s["counts"]["unknown_logical"], 16)
        self.assertEqual(s["resources"]["active_devices"], [])

    def test_terminal_transitions_heartbeats_and_status_reads_remain_responsive_during_calls(self):
        reports, times = [], []
        def capture(snapshot):
            reports.append(snapshot)
            times.append(monotonic())
        with self.scheduler(factory=partial(slow_factory, delay=0.2, measured=True), report=capture,
                            budget=synthetic_budget(80)) as scheduler:
            scheduler.dispatch()
            con = sqlite3.connect(self.path)
            con.execute("PRAGMA query_only=ON")
            before = con.total_changes
            while scheduler.inflight:
                scheduler.advance()
                begin = monotonic()
                s = self.snapshot()
                self.assertLess(monotonic() - begin, 1)
                if s["current"]:
                    self.assertTrue(any(w["status"] == "active" for w in s["work"]))
            self.assertEqual(con.total_changes, before)
            con.close()
        self.assertGreaterEqual(sum(bool(s["current"]) for s in reports), 5)
        self.assertTrue(any(s["counts"]["finished_logical"] == 4 for s in reports))
        self.assertLess(max(b - a for a, b in zip(times, times[1:])), 1)
        self.assertEqual(self.snapshot()["physical"]["peak_memory_bytes"], 123456)
        self.evidence["heartbeat"] = {"reports": len(reports), "max_gap_seconds": max(b-a for a,b in zip(times, times[1:])),
                                     "status": format_status(reports[-1])}

    def test_unconfirmed_provider_release_remains_open_chargeable_and_blocks_reallocation(self):
        scheduler = self.scheduler(budget=synthetic_budget(30))
        scheduler.release_device = lambda *_: False
        scheduler.__enter__()
        with self.assertRaisesRegex(RuntimeError, "release is unconfirmed"):
            scheduler.close()
        s = self.snapshot()
        self.assertEqual(s["resources"]["active_devices"], ["synthetic:0"])
        scheduler.release_device = self.release
        scheduler.close()
        self.assertEqual(self.snapshot()["resources"]["active_devices"], [])

    def test_main_forecast_unavailable_stops_before_generation_and_budget_drift_rejects_resume(self):
        scheduler = self.scheduler(budget=synthetic_budget(30))
        scheduler.allocation_stage = "main"
        with scheduler:
            with self.assertRaisesRegex(BudgetStop, "forecast_unavailable"):
                scheduler.run()
        with self.assertRaisesRegex(ValueError, "bounds differ"):
            with self.scheduler(budget=synthetic_budget(40)):
                pass
        self.assertEqual(self.snapshot()["counts"]["attempts"], 0)


if __name__ == "__main__":
    unittest.main()
