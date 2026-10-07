"""Read-only original-worker/CLI checks for uncertainty and missing execution."""

import gzip
import importlib.abc
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.evaluate import write_evaluation
from recovery.tasks import Task
from recovery.uncertainty import uncertainty_run
from tests.cost_fixture import fixture, clock, write_cost_worker
from tests.outcome_fixture import ROOT


class OfflineUncertaintyRunTests(unittest.TestCase):
    def test_saved_worker_is_read_only_reproducible_and_export_is_exclusive(self):
        worlds, branches, records, inputs, attempts = fixture(Task.SORT, ("B", "C", "K"))
        with tempfile.TemporaryDirectory() as directory:
            worker = Path(directory)/"worker.sqlite"
            write_cost_worker(worker, records, inputs, attempts)
            before = worker.read_bytes()
            result = uncertainty_run(worlds, branches, [worker], seed=37, now=clock(400))
            self.assertEqual(worker.read_bytes(), before)
            self.assertEqual(result, uncertainty_run(worlds, branches, [worker], seed=37, now=clock(400)))
            self.assertEqual(result["uncertainty"]["settings"]["seed"], 37)
            self.assertEqual(result["coverage"]["scheduled"], 64)
            self.assertEqual(result["coverage"]["protocol_outcomes"]["failed"], 1)
            self.assertTrue(result["uncertainty"]["policy_display_summaries"])
            for extension in ("json", "json.gz"):
                output = Path(directory)/("uncertainty."+extension)
                write_evaluation(output, result)
                with (gzip.open if extension.endswith("gz") else open)(output, "rt", encoding="utf-8") as source:
                    self.assertEqual(json.load(source), result)
                with self.assertRaises(FileExistsError):
                    write_evaluation(output, result)
            with self.assertRaises(ValueError):
                uncertainty_run(worlds, branches, [worker, worker], now=clock(400))

    def test_absent_workers_leave_frozen_population_unknown_without_creating_files(self):
        worlds, branches, _, _, _ = fixture(Task.BFS, ("B", "C", "K"))
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory)/"absent.sqlite"
            result = uncertainty_run(worlds, branches, [missing], now=clock(400))
            self.assertFalse(missing.exists())
            self.assertEqual(result["coverage"]["recorded"], 0)
            self.assertTrue(all(r["observed"]["category"] == "incomplete" for r in result["uncertainty"]["world_trajectories"]))
            self.assertTrue(all(r["exact_binomial"] is None for r in result["uncertainty"]["family_completion"]))
            self.assertTrue(all(r["intended_population"]["interval"] is None for r in result["uncertainty"]["summaries"]))
            self.assertTrue(all(not r["quality_cost_available"] for r in result["uncertainty"]["policy_world_displays"]))

    def test_cli_includes_estimands_and_costs_saves_seed_and_preserves_existing_export(self):
        with tempfile.TemporaryDirectory() as directory:
            missing, output = Path(directory)/"missing.sqlite", Path(directory)/"tables.json.gz"
            args = [sys.executable, "-S", "-m", "recovery", "analyze", "--uncertainty", "--diagnostics",
                "--resampling-seed", "37", "--as-of", clock(400), "--stage", "development",
                "--manifest", str(ROOT/"tests/fixtures/population_target.json"),
                "--schedule", str(ROOT/"tests/fixtures/schedules_target.json"),
                "--worker", str(missing), "--output", str(output)]
            executed = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
            self.assertEqual(executed.returncode, 0, executed.stderr)
            self.assertIn("0/1178 recorded", executed.stdout)
            self.assertFalse(missing.exists())
            with gzip.open(output, "rt", encoding="utf-8") as source:
                result = json.load(source)
            self.assertTrue(all(k in result for k in ("estimands", "costs", "information", "uncertainty")))
            self.assertEqual(result["uncertainty"]["settings"]["seed"], 37)
            self.assertEqual(result["uncertainty"]["coverage"]["unknown"], 1178)
            self.assertEqual(result["estimands"]["repeatability"], [])
            before = output.read_bytes()
            repeated = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(output.read_bytes(), before)

    def test_resampling_seed_requires_uncertainty_and_invalid_clock_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"invalid.json"
            args = [sys.executable, "-S", "-m", "recovery", "analyze", "--stage", "development",
                "--manifest", str(ROOT/"tests/fixtures/population_target.json"),
                "--schedule", str(ROOT/"tests/fixtures/schedules_target.json"),
                "--worker", str(Path(directory)/"missing.sqlite"), "--output", str(output)]
            for extra, error in ((["--resampling-seed", "0"], "requires --uncertainty"),
                                 (["--uncertainty", "--resampling-seed", "-1"], "nonnegative integer"),
                                 (["--uncertainty", "--as-of", "2026-10-06"], "explicit timezone")):
                run = subprocess.run(args+extra, cwd=ROOT, capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 2)
                self.assertIn(error, run.stderr)
                self.assertFalse(output.exists())

    def test_offline_stack_does_not_import_execution_or_model_modules(self):
        script = '''
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'torch','transformers','accelerate','bitsandbytes'} or fullname in {'recovery.runner','recovery.workers','recovery.inference','recovery.storage'}:
            raise AssertionError('offline import crossed into execution: '+fullname)
sys.meta_path.insert(0, Block())
from recovery.uncertainty import uncertainty_run
from tests.cost_fixture import fixture, clock, write_cost_worker
from pathlib import Path
import tempfile
w,b,r,i,a = fixture(policies=('B','C','K'))
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)/'worker.sqlite'
    write_cost_worker(path,r,i,a)
    assert uncertainty_run(w,b,[path],now=clock(400))['uncertainty']['policy_world_displays']
'''
        run = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == "__main__":
    unittest.main()
