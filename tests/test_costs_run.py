"""Read-only cost exports and CLI integration without inference imports."""

import gzip
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from recovery.costs import costs_run
from recovery.evaluate import read_records, write_evaluation
from tests.cost_fixture import clock, fixture, write_cost_worker
from tests.outcome_fixture import ROOT


class CostRunTests(unittest.TestCase):
    def test_original_worker_snapshot_tokens_costs_and_exclusive_exports(self):
        w, b, r, i, a = fixture()
        with tempfile.TemporaryDirectory() as directory:
            worker = Path(directory) / "worker.sqlite"
            write_cost_worker(worker, r, i, a)
            before = worker.read_bytes()
            tables = costs_run(w, b, [worker], now=clock(400), estimands=True)
            self.assertEqual(worker.read_bytes(), before)
            self.assertEqual(tables["costs"]["physical"]["attempt_seconds"], [235, 235])
            self.assertIn("estimands", tables)
            for suffix in ("json", "json.gz"):
                output = Path(directory) / ("costs." + suffix)
                write_evaluation(output, tables)
                opener = gzip.open if suffix.endswith("gz") else open
                with opener(output, "rt", encoding="utf-8") as source:
                    self.assertEqual(json.load(source), tables)
                with self.assertRaises(FileExistsError):
                    write_evaluation(output, tables)
            with self.assertRaisesRegex(ValueError, "once"):
                costs_run(w, b, [worker, worker], now=clock(400))
            missing = worker.with_name("missing.sqlite")
            unknown = costs_run(w, b, [missing], now=clock(400))
            self.assertEqual(unknown["coverage"]["unknown"], 128)
            self.assertFalse(missing.exists())

    def test_resource_records_share_the_application_snapshot_and_provider_billing_stays_separate(self):
        w, b, r, i, a = fixture()
        with tempfile.TemporaryDirectory() as directory:
            worker = Path(directory) / "worker.sqlite"
            write_cost_worker(worker, r, i, a)
            con = sqlite3.connect(worker)
            try:
                con.execute("CREATE TABLE allocations(device TEXT,started_at TEXT,stopped_at TEXT,stage TEXT,stop_reason TEXT,billing_json TEXT,budget_json TEXT)")
                con.execute("INSERT INTO allocations VALUES(?,?,?,?,?,?,?)", ("synthetic:0", clock(0), clock(400), "validation", "done", '{"billed_hours":1}', None))
                con.execute("CREATE TABLE provider_processes(started_at TEXT,ready_at TEXT,stopped_at TEXT,recovered_at TEXT)")
                con.execute("INSERT INTO provider_processes VALUES(?,?,?,?)", (clock(0), clock(1), clock(400), None))
                con.commit()
            finally:
                con.close()
            before = worker.read_bytes()
            records = read_records(w, b, [worker], include_resources=True)
            self.assertEqual(len(records[-1]["allocations"]), 1)
            tables = costs_run(w, b, [worker], now=clock(400))["costs"]
            self.assertEqual(worker.read_bytes(), before)
            self.assertEqual(tables["resources"]["allocated_gpu_hours"], 400 / 3600)
            self.assertEqual(tables["resources"]["partition_seconds"]["idle"], 165)
            self.assertEqual(tables["physical"]["attempt_seconds"], [235, 235])
            self.assertEqual(tables["resources"]["provider_billing"][0]["record"], {"billed_hours": 1})

    def test_cli_costs_diagnostics_estimands_full_unknown_schedule_and_existing_export(self):
        with tempfile.TemporaryDirectory() as directory:
            output, worker = Path(directory) / "costs.json.gz", Path(directory) / "missing.sqlite"
            command = [sys.executable, "-S", "-m", "recovery", "analyze", "--costs", "--diagnostics", "--estimands",
                "--as-of", clock(400), "--stage", "development", "--manifest", str(ROOT / "tests/fixtures/population_target.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_target.json"), "--worker", str(worker), "--output", str(output)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(gzip.decompress(output.read_bytes()))
            self.assertEqual(data["coverage"]["unknown"], 1178)
            self.assertIn("information", data)
            self.assertIn("estimands", data)
            self.assertTrue(all(row["selected_policy"] is None for row in data["costs"]["boundary_selections"]))
            self.assertFalse(worker.exists())
            before = output.read_bytes()
            repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(output.read_bytes(), before)

    def test_pure_costs_and_rule_never_import_runtime_or_model_dependencies(self):
        code = '''
import sys, importlib.abc
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('torch','transformers','pydantic','langgraph'):
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.cost_fixture import fixture, clock
from recovery.costs import cost_records
w,b,r,i,a = fixture()
cost_records(w,b,r,i,a,now=clock(400))
assert all(n not in sys.modules for n in ('recovery.runner','recovery.protocol','recovery.rounds','recovery.inference'))
'''
        result = subprocess.run([sys.executable, "-S", "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
