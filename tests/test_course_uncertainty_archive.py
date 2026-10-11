"""Course intended coverage, original-worker reproduction and reporting scope."""

from functools import cache
import gzip
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

from tests.course_uncertainty_archive import AS_OF, FIXTURE, ROOT, RUN, SEED, extract


@cache
def retained():
    with gzip.open(FIXTURE, "rt", encoding="utf-8") as source: return json.load(source)


class CourseUncertaintyTablesTests(unittest.TestCase):
    def test_full_declared_coverage_primary_bounds_and_fixed_focal_repeat_populations(self):
        actual = retained()
        self.assertEqual(len(actual["cases"]), 7)
        full = actual["cases"]["full-main-20"]
        self.assertEqual((full["coverage"]["scheduled"], full["coverage"]["recorded"], full["coverage"]["unknown"]), (6280, 2170, 4110))
        self.assertEqual(full["settings"]["seed"], SEED)
        self.assertEqual(full["settings"]["draws"], 10_000)
        self.assertEqual(full["settings"]["regime"], "course")
        self.assertIn("Exploratory", full["kind"])
        for row in (r for r in full["summaries"] if r["primary_interval"]):
            self.assertEqual(row["intended_population"]["independent_worlds"], 20)
            self.assertEqual(set(row["family_denominators"].values()), {4})
            self.assertEqual(row["complete_case_description"]["independent_worlds"], 5)
            self.assertIsNone(row["intended_population"]["interval"])
            self.assertEqual(row["complete_case_description"]["interval"], [0, 0])
            self.assertEqual(row["sensitivity"]["interval"], [-1.5, 1.5] if row["estimand"] == "theta" else [-.75, .75])
            expected = (1280, 320, 960) if row["estimand"] == "theta" else (480, 120, 360)
            self.assertEqual(tuple(row["paired_coverage"][k] for k in ("scheduled_calls", "executed_calls", "unknown_calls")), expected)
        populations = {p["population"]: p for p in full["populations"]}
        self.assertEqual(len(populations["main"]["world_ids"]), 20)
        for cohort in ("receipts", "prose_delay", "preserving"): self.assertEqual(len(populations[cohort]["world_ids"]), 8)
        self.assertEqual(len(populations["repeat"]["world_ids"]), 5)
        shared = [r for r in full["world_bounds"] if r["endpoint"] == "accuracy" and r["round"] == 1
                  and r["estimand"] in ("Q_B-B", "Q_C-C", "E_keep", "E_clear")]
        self.assertTrue(any(not r["execution_observed"] for r in shared))
        self.assertTrue(all(r["sensitivity"]["interval"] == [0, 0] for r in shared))
        self.assertEqual(actual["independent_checks"]["full-main-20"]["independent_shared_linear_rows"], 4152)

    def test_stopped_and_absent_scopes_keep_unknown_trajectories_costs_and_denominators(self):
        for name, case in retained()["cases"].items():
            self.assertTrue(all(r["replicate"] == 0 for r in case["summaries"]))
            self.assertTrue(all(r["population"] == "repeat" for r in case["trajectory_summaries"] if r["replicate"]))
            self.assertTrue(all(r["metric"] == "policy_seconds" or r["paired_cost"] is not None for r in case["policy_display_summaries"]))
            if name.endswith("/stopped"):
                self.assertEqual(case["coverage"]["unknown"], 16)
                self.assertTrue(all(r["observed"]["category"] == "incomplete" for r in case["world_trajectories"]))
                self.assertTrue(all(r["exact_binomial"] is None for r in case["family_completion"]))
            if name.startswith("unexecuted"):
                self.assertEqual(case["coverage"]["recorded"], 0)
                self.assertEqual(case["coverage"]["unknown"], 6280 if "main" in name else 1178)
                self.assertTrue(all(r["intended_population"]["interval"] is None for r in case["summaries"]))
                self.assertTrue(all(not r["quality_cost_available"] for r in case["policy_world_displays"]))
                self.assertTrue(all(r["observed"]["first_joint_round"] is None and r["observed"]["first_stable_joint_round"] is None
                                    for r in case["world_trajectories"]))
                self.assertTrue(any(r["unknown_eligibility_worlds"] and r["sensitivity"]["method"] == "conservative_unknown_eligibility"
                                    for r in case["summaries"] if r["endpoint"] == "preservation"))
        full = retained()["cases"]["full-main-20"]
        unknown_costs = [r for r in full["policy_display_summaries"] if r["metric"] == "policy_seconds" and r["unknown_worlds"]]
        self.assertTrue(unknown_costs)
        self.assertTrue(any(r["sensitivity"]["interval"] and r["sensitivity"]["interval"][1] is None for r in unknown_costs))


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "original checkpoint decoder needs declared CPU dependencies")
class CourseUncertaintyArchiveTests(unittest.TestCase):
    def test_seven_original_scopes_reproduce_in_fresh_process_without_inference_or_execution(self):
        script = '''
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch','transformers','numpy','scipy','matplotlib','bitsandbytes','accelerate'} or fullname in {'recovery.inference','recovery.runner','recovery.workers','recovery.accounting','recovery.protocol','recovery.rounds','recovery.events','recovery.replay'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.course_uncertainty_archive import main
raise SystemExit(main())
'''
        environment = dict(os.environ, PYTHONHASHSEED="73")
        result = subprocess.run([sys.executable, "-X", "utf8", "-c", script], cwd=ROOT,
            env=environment, capture_output=True, text=True, timeout=240)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Seven original course scopes reproduce", result.stdout)

    def test_course_cli_infers_manifest_regime_and_exports_full_original_scope_read_only(self):
        with tempfile.TemporaryDirectory(prefix="course-uncertainty-cli-") as temporary, ZipFile(RUN) as archive:
            root = Path(temporary)
            case = next(c for c in json.loads(archive.read("evidence.json"))["cases"] if c["directory"].startswith("test_every_family"))
            base = case["directory"]
            selected = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, ["inputs/population.json", "inputs/schedules.json", *[base + "/" + p for p in selected["workers"]]])
            paths = [root / base / p for p in selected["workers"]]
            before = [p.read_bytes() for p in paths]
            output = root / "uncertainty.json.gz"
            command = [sys.executable, "-X", "utf8", "-m", "recovery", "analyze", "--uncertainty",
                "--resampling-seed", str(SEED), "--as-of", AS_OF, "--manifest", str(root / "inputs/population.json"),
                "--schedule", str(root / "inputs/schedules.json"), "--output", str(output)]
            for path in paths: command.extend(("--worker", str(path)))
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=150)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            actual = json.loads(gzip.decompress(output.read_bytes()))
            expected = retained()["cases"]["full-main-20"]
            for key, value in actual["uncertainty"].items(): self.assertTrue(value == expected[key], key)
            self.assertEqual(actual["coverage"], expected["coverage"])
            self.assertEqual(actual["estimands"]["world_contrasts"], expected["world_contrasts"])
            self.assertEqual([p.read_bytes() for p in paths], before)


class CourseUncertaintyReportScopeTests(unittest.TestCase):
    def test_report_consumer_receives_course_precision_scope_without_changing_thesis_defaults(self):
        # Narrow consumer check, not the subsequent complete course report gate.
        with tempfile.TemporaryDirectory(prefix="course-uncertainty-report-scope-") as temporary:
            root = Path(temporary)
            for regime in ("course", "target"):
                directory = root / regime
                command = [sys.executable, "-S", "-X", "utf8", "-m", "recovery", "analyze", "--report",
                    "--stage", "development", "--resampling-seed", "37", "--as-of", AS_OF,
                    "--manifest", str(ROOT / f"tests/fixtures/population_{regime}.json"),
                    "--schedule", str(ROOT / f"tests/fixtures/schedules_{regime}.json"),
                    "--worker", str(root / "absent.sqlite"), "--output", str(directory)]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                report = json.loads((directory / "report.json").read_bytes())
                expected = {20} if regime == "course" else {60, 40}
                self.assertEqual({r["N"] for r in report["reporting_references"]["main"]}, expected)
                if regime == "course": self.assertIn("Exploratory", report["reporting_references"]["interpretation"])
            self.assertFalse((root / "absent.sqlite").exists())


if __name__ == "__main__":
    unittest.main()
