"""Retained course tables, original workers and inference-free reproduction."""

import gzip
import json
import subprocess
import sys
import unittest

from tests.course_analysis_archive import FIXTURE, ROOT, reconstruct, worker_audit


class CourseAnalysisArchiveTests(unittest.TestCase):
    def test_original_course_lifecycle_tables_fixed_populations_and_unknowns(self):
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            self.assertEqual(actual, json.load(source))
        full = actual["cases"]["full-main-20"]
        self.assertEqual(full["coverage"]["scheduled"], 6280)
        self.assertEqual(full["coverage"]["recorded"], 2170)
        self.assertEqual(full["coverage"]["unknown"], 4110)
        self.assertEqual(len(full["estimands"]["world_contrasts"]), 6824)
        self.assertEqual(len(full["estimands"]["repeatability"]), 80)
        self.assertEqual(len(full["estimands"]["trajectory_changes"]), 50)
        primary = [r for r in full["estimands"]["summaries"] if r["primary"] and r["level"] == "all_families"]
        self.assertEqual(len(primary), 2)
        for row in primary:
            self.assertIsNone(row["value"])
            self.assertEqual((row["scheduled_worlds"], row["observed_worlds"]), (20, 5))
            self.assertEqual(set(row["family_denominators"].values()), {4})
            self.assertEqual(row["complete_case_description"]["value"], 0)
        populations = {r["population"]: r for r in full["estimands"]["populations"]}
        for name, count in (("main", 20), ("receipts", 8), ("prose_delay", 8), ("preserving", 8), ("repeat", 5)):
            self.assertEqual(len(populations[name]["world_ids"]), count)
        for row in full["outcomes"]:
            if row["protocol_outcome"] in ("invalid", "failed"): self.assertEqual(row["correct"], 0)
            if row["protocol_outcome"] == "unknown": self.assertIsNone(row["correct"])
        stopped = next(case for name, case in actual["cases"].items() if name.endswith("/stopped"))
        self.assertEqual((stopped["coverage"]["recorded"], stopped["coverage"]["unknown"]), (0, 16))
        self.assertEqual(stopped["trajectories"][0]["category"], "incomplete")
        for name, scheduled in (("unexecuted-main-20", 6280), ("unexecuted-development", 1178)):
            self.assertEqual(actual["cases"][name]["coverage"]["unknown"], scheduled)
            self.assertTrue(all(r["value"] is None for r in actual["cases"][name]["estimands"]["world_contrasts"]))
        development = actual["cases"]["unexecuted-development"]["estimands"]
        self.assertEqual(development["repeatability"], [])
        self.assertEqual(development["trajectory_changes"], [])

    def test_all_sixteen_original_worker_scopes_rejoin_without_mutation(self):
        actual = worker_audit()
        self.assertEqual(len(actual), 16)
        # These fault probes intentionally execute only selected rounds. They
        # are accepted restart mechanics, not complete scheduled experiments.
        self.assertEqual(sum(case["recorded"] for case in actual.values()), 1422)
        self.assertEqual(sum(case["unknown"] for case in actual.values()), 312)
        self.assertEqual(actual["test_cross_worker_replays_keep_failed_invalid_replies_and_independent_q_queues"]["unknown"], 72)

    def test_fresh_course_reconstruction_imports_no_model_or_runtime(self):
        script = '''
import importlib.abc, sys
blocked = {"torch", "transformers", "pydantic", "langgraph", "langchain", "numpy", "scipy", "pandas", "matplotlib"}
runtime = {"recovery.inference", "recovery.runner", "recovery.workers", "recovery.accounting", "recovery.protocol", "recovery.rounds", "recovery.replay"}
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked or fullname in runtime:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.course_analysis_archive import main
raise SystemExit(main())
'''
        result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT,
                                capture_output=True, text=True, timeout=150)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no inference or empirical result", result.stdout)


if __name__ == "__main__":
    unittest.main()
