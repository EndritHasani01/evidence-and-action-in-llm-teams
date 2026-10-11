"""Independent course ledger/resource reconstruction; CPU/synthetic evidence."""

from contextlib import closing
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from time import monotonic, sleep
import unittest

from recovery.accounting import (Budget, BudgetStop, CourseBudget, _course_resources,
    _forecast, budget_from_record, course_admission, format_status, progress_snapshot)
from recovery.runner import DurableRunner, WorkerReader
from recovery.storage import WorkerStore, record_json
from recovery.tasks import Task
from recovery.workers import LocalScheduler, WorkerSpec
from tests.accounting_checks import clock
from tests.course_intervention_cases import TOKENIZER, branches, course_inputs, scheduled
from tests.course_worker_cases import SETTINGS, prefix_branch, provide, provider_factory, sort_world, tokenizer_factory
from tests.lifecycle_fixture import BOUNDS, backup_workers, scientific_records, stable_progress, write_json

ROOT = Path(__file__).resolve().parents[1]


def known_budget(**kwargs):
    values = {"prior_" + name + "_gpu_hours": (0, 0)
              for name in ("development", "setup", "interruption", "other_course", "other_overall")}
    values.update(allocation_mode="synthetic", prior_evidence="synthetic CPU validation; verified zero unrecorded allocation")
    values.update(prior_smoke_gpu_hours=(0, 0), prior_smoke_attempts=0)
    values.update(kwargs)
    return CourseBudget(**values)


def independent_records(worlds, selected, paths, snapshot):
    """Rejoin literal rows without using the production cost/count helpers."""
    calls, attempts = {}, []
    for path in paths:
        with closing(WorkerStore(path, readonly=True)) as store:
            calls.update((row["call_id"], dict(row)) for row in store.connection.execute("SELECT * FROM calls"))
            attempts.extend(dict(row) for row in store.connection.execute("SELECT * FROM attempts"))
            assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    slots = [c for b in selected for c in b.calls]
    final = {"completed", "timeout", "infrastructure_failure", "replay"}
    finished = sum(c.call_id in calls and calls[c.call_id]["status"] in final for c in slots)
    expected = dict(scheduled_logical=len(slots), scheduled_generations=len({c.generation_id for c in slots}),
        finished_logical=finished, unknown_logical=len(slots)-finished, attempts=len(attempts),
        replay_uses=sum(row["status"] == "replay" for row in calls.values()),
        retries=sum(row["number"] == 2 for row in attempts),
        uncertain_attempts=sum(row["uncertain_completion"] for row in attempts))
    assert all(snapshot["counts"][name] == value for name, value in expected.items()), expected
    by_generation = {}
    for row in attempts:
        by_generation.setdefault(row["call_id"], []).append(row)
    lower = {cid: sum(a["elapsed_seconds"] if a["elapsed_seconds"] is not None else a["observed_seconds"] for a in rows)
             for cid, rows in by_generation.items()}
    assert abs(snapshot["physical"]["attempt_seconds"][0] - sum(lower.values())) < 1e-8
    assert snapshot["physical"]["request_tokens"] == sum(calls[a["call_id"]]["request_tokens"] for a in attempts)
    assert snapshot["physical"]["output_tokens"] == sum(len(json.loads(row["raw_json"])["token_ids"])
        for row in calls.values() if row["raw_json"] is not None)
    by_branch = {b.branch_id: b for b in selected}
    for cost in snapshot["policy_costs"]:
        branch = by_branch[cost["branch_id"]]
        used = (*by_branch[branch.prefix_parent].calls, *branch.calls) if branch.prefix_parent else branch.calls
        assert cost["logical_calls"] == len(used)
        assert abs(cost["seconds"][0] - sum(lower.get(c.generation_id, 0) for c in used)) < 1e-8
        assert cost["unknown_calls"] == sum(c.call_id not in calls or calls[c.call_id]["status"] not in final for c in used)
    for slot in slots:
        if slot.call_id in calls and calls[slot.call_id]["status"] == "replay":
            assert slot.call_id not in by_generation
            assert calls[slot.call_id]["validation_json"] == calls[slot.replay_parent]["validation_json"]
    return expected


class CourseAccountingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_manifest_counts_cohorts_and_cli_select_declared_scope_without_writes(self):
        p, s = course_inputs()
        summaries = []
        for worlds, selected, distinct, logical in ((p.main, s.main, 5752, 6280), (p.development, s.development, 1114, 1178)):
            absent = self.root / "absent.sqlite"
            snapshot = progress_snapshot(worlds, selected, (absent,), regime="course")
            self.assertEqual(snapshot["counts"]["scheduled_generations"], distinct)
            self.assertEqual(snapshot["counts"]["scheduled_logical"], logical)
            self.assertEqual(snapshot["counts"]["unknown_logical"], logical)
            self.assertEqual(len({c.generation_id for b in selected for c in b.calls}), distinct)
            self.assertFalse(snapshot["forecast"]["available"])
            self.assertIsNone(snapshot["resources"]["allocated_gpu_hours"])
            self.assertFalse(absent.exists())
            self.assertEqual({row["status"] for row in snapshot["work"]}, {"runnable", "dependency_waiting"})
            summaries.append(snapshot["counts"])
        groups = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",))["matched_comparisons"]
        for subset, replicate, expected in (("reset_interaction", 0, 20), ("receipts", 0, 8),
                                           ("prose", 0, 16), ("preserving", 0, 8), ("repeatability", 1, 10)):
            self.assertEqual(sum(g["scheduled"] for g in groups if g["subset"] == subset and g["replicate"] == replicate), expected)
        base = [sys.executable, "-X", "utf8", "-m", "recovery", "status", "--manifest", str(ROOT / "tests/fixtures/population_course.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_course.json"), "--worker", str(self.root / "absent.sqlite")]
        for stage, expected in (("main", 6280), ("development", 1178)):
            result = subprocess.run([*base, "--stage", stage, "--json", "--as-of", clock(0)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["counts"]["scheduled_logical"], expected)
        result = subprocess.run([*base, "--stage", "main", "--count", "40"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "absent.sqlite").exists())

    def test_default_unknown_prior_withholds_allocation_before_any_provider(self):
        world = sort_world()
        path = self.root / "worker.sqlite"
        scheduler = LocalScheduler((WorkerSpec(path, provider_factory, allocated_device="synthetic:0"),),
            (world,), (prefix_branch(world),), tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
            budget=CourseBudget(allocation_mode="synthetic"), release_device=lambda *_: True, allocation_stage="validation")
        with self.assertRaisesRegex(BudgetStop, "unknown_prior_allocation"):
            with scheduler:
                self.fail("unknown prior spending admitted a provider")
        snapshot = progress_snapshot((world,), (prefix_branch(world),), (path,), regime="course")
        self.assertEqual(snapshot["counts"]["attempts"], 0)
        self.assertEqual(snapshot["counts"]["unknown_logical"], 16)
        self.assertIsNone(snapshot["resources"]["remaining_ceiling_gpu_hours"])
        self.assertIsNone(snapshot["resources"]["course_gpu_hours"])
        self.assertFalse(snapshot["resources"]["devices"])
        self.assertEqual(scheduler.stop_reason, "unknown_prior_allocation")
        self.assertIn("unknown_prior_allocation", format_status(snapshot))

    def test_cumulative_prior_reserves_overall_ceiling_and_documented_bounds(self):
        budget = known_budget(prior_development_gpu_hours=(3, 3), prior_setup_gpu_hours=(.5, .5),
            prior_interruption_gpu_hours=(.25, .25), prior_other_course_gpu_hours=(.25, .25),
            prior_other_overall_gpu_hours=(71, 71))
        p, s = course_inputs()
        snapshot = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), budget=budget, regime="course")
        resources = snapshot["resources"]
        self.assertEqual(resources["course_gpu_hours"], [4, 4])
        self.assertEqual(resources["overall_gpu_hours"], [75, 75])
        self.assertEqual(resources["remaining_reserves_gpu_hours"], dict(development=5, setup=1.5, interruption=1.75))
        # P + unspent D/S/I + 1.25*M = 4 + 8.25 + 16.25 = 28.5;
        # overall = 75 + 8.25 + 16.25 = 99.5, before release allowance.
        forecast = dict(available=True, remaining_gpu_hours=[13, 1.25*13])
        self.assertIsNone(course_admission(resources, forecast, budget, "main", 2)[0])
        for other, main in ((72, 13), (0, 15)):
            changed = replace(budget, prior_other_overall_gpu_hours=(other, other))
            new = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), budget=changed, regime="course")["resources"]
            self.assertEqual(course_admission(new, dict(available=True, remaining_gpu_hours=[main, 1.25*main]), changed, "main", 2)[0],
                             "remaining_forecast_exceeds_budget")
        changed = replace(budget, prior_development_gpu_hours=(8.1, 8.1))
        new = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), budget=changed, regime="course")["resources"]
        self.assertEqual(new["remaining_reserves_gpu_hours"]["development"], 0)
        self.assertEqual(new["admission_reason"], "cumulative_allowance_exceeded")
        self.assertIn("development", new["exceeded_allowances"])
        changed = replace(budget, prior_setup_gpu_hours=(.5, 2.1))
        new = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), budget=changed, regime="course")["resources"]
        self.assertIn("setup", new["exceeded_allowances"])
        self.assertEqual(new["course_gpu_hours"], [4, 5.6])
        with self.assertRaisesRegex(ValueError, "evidence"):
            CourseBudget(prior_development_gpu_hours=(0, 0))
        for bad in ((-1, 0), (2, 1), (0, float("nan")), (True, 1)):
            with self.assertRaises(ValueError):
                known_budget(prior_setup_gpu_hours=bad)
        self.assertEqual(asdict(Budget())["ceiling_gpu_hours"], 100)
        self.assertNotIn("overall_ceiling_gpu_hours", asdict(Budget()))
        self.assertEqual(budget_from_record(json.loads(record_json(asdict(budget)))), budget)
        exhausted_setup = replace(budget, prior_setup_gpu_hours=(2, 2))
        new = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), budget=exhausted_setup, regime="course")["resources"]
        self.assertEqual(course_admission(new, forecast, exhausted_setup, "main", 2)[0], "budget_exhausted_before_allocation")

    def test_two_assigned_devices_setup_idle_billing_and_prior_are_charged_once(self):
        world = sort_world()
        selected = (prefix_branch(world),)
        paths = tuple(self.root / f"idle-{i}.sqlite" for i in range(2))
        budget = known_budget(prior_setup_gpu_hours=(.1, .2))
        for i, path in enumerate(paths):
            with DurableRunner(path, None) as runner:
                runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=budget, regime="course")
                number = runner.store.allocation_started(f"synthetic:{i}", "development", budget=budget,
                    started_at=clock(0), billing={"billed_hours": 1, "rule": "provider rounds up"})
                runner.store.allocation_stopped(number, "synthetic idle", released_at=clock(900))
        snapshot = progress_snapshot((world,), selected, paths, now=clock(900), regime="course")
        resources = snapshot["resources"]
        self.assertEqual(resources["allocated_gpu_hours"], .5)
        self.assertEqual(resources["course_gpu_hours"], [.6, .7])
        self.assertEqual(resources["overall_gpu_hours"], [.6, .7])
        self.assertEqual(resources["remaining_reserves_gpu_hours"], dict(development=7.5, setup=1.8, interruption=2))
        self.assertEqual(snapshot["physical"]["attempt_seconds"], [0, 0])
        self.assertEqual(len(resources["provider_billing"]), 2)
        self.assertEqual(resources["partition_seconds"]["idle"], 1800)
        self.assertFalse(snapshot["forecast"]["available"])

    def test_cpu_or_unclassified_measurements_never_forecast_gpu_throughput(self):
        p, s = course_inputs()
        selected = tuple(b for b in s.main if b.phase == "control")[:2]
        calls = {selected[0].calls[0].call_id: dict(status="completed")}
        generations = {selected[0].calls[0].call_id: dict(seconds=[2, 2], unknown_duration_attempts=0,
            device="cpu", request_tokens=100)}
        cpu = _forecast(selected, calls, generations, ["cpu"], known_budget())
        self.assertTrue(cpu["available"])
        gpu = _forecast(selected, calls, generations, ["T4:0"], known_budget(allocation_mode="gpu"),
            history=[dict(forecast=cpu, resources=dict(allocation_mode="synthetic"))], gpu_generations=set())
        self.assertFalse(gpu["available"])
        self.assertIsNone(gpu["remaining_gpu_hours"])
        # All devices and overhead are inside M before the single 25% margin.
        measured = {selected[0].calls[0].call_id: dict(seconds=[8, 8], unknown_duration_attempts=0,
            device="synthetic:0", request_tokens=100)}
        forecast = _forecast(selected, calls, measured, ["synthetic:0"], known_budget(overhead_seconds=4))
        self.assertEqual(forecast["remaining_gpu_hours"][1], 1.25*(8+4)/3600)

    def test_course_regime_budget_and_saved_inputs_cannot_drift_or_reset(self):
        world = sort_world()
        selected = (prefix_branch(world),)
        path = self.root / "bound.sqlite"
        budget = known_budget()
        with DurableRunner(path, None) as runner:
            runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=budget, regime="course")
        for changed in (replace(budget, ceiling_gpu_hours=29), replace(budget, prior_setup_gpu_hours=(1, 1))):
            with DurableRunner(path, None) as runner:
                with self.assertRaisesRegex(ValueError, "bounds differ"):
                    runner.store.bind_run((world,), selected, SETTINGS, BOUNDS, budget=changed, regime="course")
        with self.assertRaisesRegex(ValueError, "regime"):
            progress_snapshot((world,), selected, (path,), regime="thesis")
        with self.assertRaisesRegex(ValueError, "manifest differs"):
            progress_snapshot((replace(world, edited_owner=(world.edited_owner+1)%4),), selected, (path,), regime="course")
        with self.assertRaisesRegex(ValueError, "requires CourseBudget"):
            LocalScheduler((WorkerSpec(path, provider_factory, allocated_device="synthetic:0"),), (world,), selected,
                tokenizer_factory, settings=SETTINGS, regime="course", budget=Budget(), release_device=lambda *_: True)

    def test_unknown_smoke_and_spent_envelope_never_create_a_new_allowance(self):
        p, s = course_inputs()
        for budget, reason in ((known_budget(prior_smoke_gpu_hours=None), "unknown_prior_smoke"),
                               (known_budget(prior_smoke_attempts=None), "unknown_prior_smoke"),
                               (known_budget(prior_smoke_attempts=25), "cumulative_allowance_exceeded"),
                               (known_budget(prior_smoke_gpu_hours=(.4, .6), prior_development_gpu_hours=(.4, .6)), "cumulative_allowance_exceeded")):
            resources = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), regime="course", budget=budget)["resources"]
            self.assertEqual(resources["admission_reason"], reason)
            self.assertEqual(course_admission(resources, dict(available=True, remaining_gpu_hours=[0, 0]), budget, "main", 1)[0], reason)
        resources = progress_snapshot(p.main, s.main, (self.root / "absent.sqlite",), regime="course",
            budget=known_budget(prior_development_gpu_hours=(.4, .4), prior_smoke_gpu_hours=(.4, .4), prior_smoke_attempts=20))["resources"]
        self.assertEqual(resources["course_gpu_hours"], [.4, .4])  # Smoke subset is not added again.
        self.assertEqual(resources["remaining_smoke_attempts"], 4)
        self.assertAlmostEqual(resources["remaining_smoke_gpu_hours"], .1)

    def test_main_needs_measured_forecast_before_setup_and_charges_existing_reservation(self):
        world = sort_world()
        selected = (prefix_branch(world),)
        path = self.root / "worker.sqlite"
        releases = []
        earlier = (datetime.now(timezone.utc)-timedelta(seconds=5)).isoformat()
        scheduler = LocalScheduler((WorkerSpec(path, provider_factory, allocated_device="synthetic:0", allocated_at=earlier),),
            (world,), selected, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
            budget=known_budget(), release_device=lambda index, device: releases.append((index, device)) or True)
        with self.assertRaisesRegex(BudgetStop, "remaining_forecast_unavailable"):
            with scheduler:
                self.fail("unmeasured main admitted a provider")
        snapshot = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertEqual(snapshot["counts"]["attempts"], 0)
        self.assertEqual(snapshot["counts"]["unknown_logical"], 16)
        self.assertGreaterEqual(snapshot["resources"]["allocated_gpu_hours"], 5/3600)
        self.assertEqual(releases, [(0, "synthetic:0")])
        self.assertFalse(snapshot["resources"]["active_devices"])
        self.assertEqual(snapshot["gate"], "remaining_forecast_unavailable")

    def test_failed_configuration_and_historical_files_charge_once_without_gpu_forecasts(self):
        p, s = course_inputs()
        dev = next(w for w in p.development if w.world.task is Task.SORT)
        selected = tuple(b for b in s.development if b.world_id == dev.world_id and b.phase == "control")[:1]
        paths = tuple(self.root / f"prior-{i}.sqlite" for i in range(2))
        for i, path in enumerate(paths):
            settings = SETTINGS if i == 0 else dict(SETTINGS, temperature=.5)
            start, duration, end = (0, 2, 20) if i == 0 else (20, 90, 120)
            with DurableRunner(path, TOKENIZER, provide if i == 0 else lambda *a, **k: provide(*a, **dict(k, settings=SETTINGS)), scripted=True) as runner:
                runner.store.bind_run((dev,), selected, settings, BOUNDS, budget=known_budget(), regime="course")
                runner.run_control(dev, selected[0], settings=settings)
                with runner.store.connection:
                    runner.store.connection.execute("UPDATE attempts SET started_at=?,finished_at=?,elapsed_seconds=?,observed_seconds=?",
                        (clock(start), clock(start+duration), duration, duration))
                number = runner.store.allocation_started("synthetic:0", "development", budget=known_budget(), started_at=clock(start))
                runner.store.allocation_stopped(number, "synthetic historical configuration", released_at=clock(end))
        world = sort_world()
        main = tuple(b for b in branches(world) if b.phase == "control")[:1]
        future = self.root / "future.sqlite"
        snapshot = progress_snapshot((world,), main, (future,), prior_paths=paths, settings=SETTINGS,
            budget=known_budget(), now=clock(120), regime="course")
        self.assertEqual(snapshot["resources"]["course_gpu_hours"], [120/3600, 120/3600])
        self.assertEqual(snapshot["resources"]["overall_gpu_hours"], [120/3600, 120/3600])
        self.assertEqual(snapshot["forecast"]["remaining_gpu_hours"], [2/3600, 2.5/3600])
        self.assertEqual(sum(row["physical"]["attempt_seconds"][0] for row in snapshot["prior_runs"]), 92)
        gpu = progress_snapshot((world,), main, (future,), prior_paths=paths, settings=SETTINGS,
            budget=known_budget(allocation_mode="gpu"), now=clock(120), regime="course")
        self.assertFalse(gpu["forecast"]["available"])
        self.assertEqual(gpu["resources"]["admission_reason"], "unknown_allocation_classification")
        scheduler = LocalScheduler((WorkerSpec(future, provider_factory, allocated_device="new-synthetic-device"),),
            (world,), main, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
            budget=known_budget(), release_device=lambda *_: True, prior_paths=paths)
        with self.assertRaisesRegex(BudgetStop, "remaining_forecast_unavailable"):
            with scheduler:
                self.fail("a new unmeasured device admitted main setup")
        self.assertEqual(progress_snapshot((world,), main, (future,), regime="course")["counts"]["attempts"], 0)
        with self.assertRaisesRegex(ValueError, "once"):
            progress_snapshot((world,), main, (future,), prior_paths=paths+paths, settings=SETTINGS, regime="course")
        copy = self.root / "duplicate.sqlite"
        backup_workers((paths[0],), (copy,))
        with self.assertRaisesRegex(ValueError, "duplicate|overlap"):
            progress_snapshot((world,), main, (future,), prior_paths=(paths[0], copy), settings=SETTINGS, regime="course")

    def test_original_course_kill_bundle_remains_readable_with_independent_accounting(self):
        from tests.course_worker_archive import FIXTURE, audit, selected
        from tests.lifecycle_archive import extract
        extract(FIXTURE, self.root)
        summary = audit(self.root)
        evidence = json.loads((self.root / "evidence.json").read_bytes())
        self.assertEqual(summary["real_kills"], 10)
        for case in evidence["cases"]:
            directory, worlds, chosen, paths = selected(self.root, case)
            snapshot = json.loads((directory / "progress.json").read_bytes())
            independent_records(worlds, chosen, paths, snapshot)

    def test_course_terminal_heartbeats_are_read_only_and_report_fixed_call_transitions(self):
        from functools import partial
        world = sort_world()
        selected = (prefix_branch(world),)
        path = self.root / "worker.sqlite"
        reports, times = [], []
        def report(snapshot):
            reports.append(snapshot)
            times.append(monotonic())
        with LocalScheduler((WorkerSpec(path, partial(provider_factory, delay=.15), allocated_device="synthetic:0"),),
                (world,), selected, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
                budget=known_budget(ceiling_gpu_hours=90/3600, shutdown_seconds=3),
                release_device=lambda *_: True, allocation_stage="validation", report=report) as scheduler:
            scheduler.dispatch()
            with closing(sqlite3.connect(path)) as con:
                con.execute("PRAGMA query_only=ON")
                before = con.total_changes
                while scheduler.inflight:
                    scheduler.advance()
                    begin = monotonic()
                    snapshot = scheduler.progress()
                    self.assertLess(monotonic()-begin, 1)
                    if snapshot["current"]:
                        self.assertEqual(snapshot["current"][0]["stage"], "main")
                        self.assertEqual(snapshot["current"][0]["device"], "synthetic:0")
                        self.assertTrue(any(row["status"] == "active" for row in snapshot["work"]))
                self.assertEqual(con.total_changes, before)
            scheduler.run()
        self.assertGreaterEqual(sum(bool(r["current"]) for r in reports), 5)
        self.assertLess(max(b-a for a,b in zip(times, times[1:])), 1)
        self.assertTrue(any(r["counts"]["finished_logical"] == 4 for r in reports))
        final = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertEqual(final["counts"]["finished_logical"], 16)
        self.assertEqual(final["counts"]["attempts"], 16)
        self.assertIn("runtime percentage is unavailable", format_status(final))

    def test_course_unconfirmed_provider_release_stays_chargeable_and_blocks_reallocation(self):
        world = sort_world()
        selected = (prefix_branch(world),)
        path = self.root / "worker.sqlite"
        scheduler = LocalScheduler((WorkerSpec(path, provider_factory, allocated_device="synthetic:0"),),
            (world,), selected, tokenizer_factory, settings=SETTINGS, regime="course", **BOUNDS,
            budget=known_budget(ceiling_gpu_hours=90/3600, shutdown_seconds=3),
            release_device=lambda *_: False, allocation_stage="validation")
        scheduler.__enter__()
        self.addCleanup(lambda: scheduler.close())
        with self.assertRaisesRegex(RuntimeError, "release is unconfirmed"):
            scheduler.close()
        before = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertEqual(before["resources"]["active_devices"], ["synthetic:0"])
        self.assertEqual(before["counts"]["attempts"], 0)
        scheduler.release_device = lambda *_: True
        # A second owner cannot admit another interval over an unreleased one.
        with self.assertRaisesRegex(BudgetStop, "confirmed provider release"):
            with LocalScheduler(scheduler.specs, (world,), selected, tokenizer_factory, settings=SETTINGS,
                    regime="course", **BOUNDS, budget=scheduler.budget, release_device=lambda *_: True,
                    allocation_stage="validation"):
                self.fail("unreleased allocation was admitted twice")
        scheduler.close()
        after = progress_snapshot((world,), selected, (path,), regime="course")
        self.assertGreaterEqual(after["resources"]["allocated_gpu_hours"], before["resources"]["allocated_gpu_hours"])
        self.assertFalse(after["resources"]["active_devices"])


if __name__ == "__main__":
    unittest.main()
