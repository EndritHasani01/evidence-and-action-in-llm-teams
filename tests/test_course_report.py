"""Course report status, literal feasibility evidence and primary-only displays."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.report import assemble_report, report_run, write_report
from tests.cost_fixture import clock, write_cost_worker
from tests.information_fixture import fixture
from tests.outcome_fixture import ROOT
from tests.test_report_run import audit_links


class CourseReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="course-report-unit-")
        cls.root = Path(cls.temporary.name)
        cls.worlds, cls.branches, records, inputs, attempts, _ = fixture(size="course")
        for n, row in enumerate(attempts):
            row.update(elapsed_seconds=2, observed_seconds=2, started_at=clock(2*n),
                finished_at=clock(2*n+2), recovered_at=None, device="synthetic:0", peak_memory_bytes=1000)
        cls.worker = cls.root / "worker.sqlite"
        write_cost_worker(cls.worker, records, inputs, attempts)
        cls.before = cls.worker.read_bytes()
        cls.result = report_run(cls.worlds, cls.branches, [cls.worker], now=clock(400), regime="course")

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_complete_means_supplied_synthetic_scope_and_not_accepted_main_model_evidence(self):
        report = self.result["report"]
        self.assertEqual(report["scope"]["regime"], "course")
        self.assertEqual(report["scope"]["scheduled_worlds"], 1)
        self.assertEqual(report["execution"]["status"], "complete")
        self.assertEqual(report["coverage"]["unknown"], 0)
        for key in ("accepted_main_freeze", "model_capability", "gpu_memory_headroom", "terminal_feasibility"):
            self.assertIsNone(report["execution"][key])
        self.assertIn("not empirical completion", report["execution"]["coverage_scope"])
        self.assertEqual({r["N"] for r in report["reporting_references"]["main"]}, {20})
        self.assertEqual({r["N"] for r in report["reporting_references"]["focal"]}, {8})
        self.assertTrue(any("inactive/unobserved Q" in text for text in report["interpretations"]))
        self.assertTrue(any("not pass the model capability" in text for text in report["interpretations"]))
        self.assertEqual(self.worker.read_bytes(), self.before)

    def test_missing_scope_is_incomplete_and_unknowns_do_not_establish_terminal_failure(self):
        missing = self.root / "absent.sqlite"
        result = report_run(self.worlds, self.branches, [missing], now=clock(400), regime="course")
        self.assertFalse(missing.exists())
        report = result["report"]
        self.assertEqual(report["execution"]["status"], "incomplete")
        self.assertIsNone(report["execution"]["terminal_feasibility"])
        self.assertEqual(report["coverage"]["recorded"], 0)
        self.assertEqual(report["coverage"]["unknown"], report["coverage"]["scheduled"])
        self.assertEqual(report["selection"]["status"], "unavailable")
        self.assertFalse(report["cases"])
        self.assertTrue(all(r["raw_reply"] is None for r in result["traces"]["calls"]))

    def test_terminal_document_does_not_change_tables_or_repair_results_and_keeps_coverage_separate(self):
        evidence = dict(source="synthetic-gate.md", text="Synthetic terminal gate failure.\r\n\tUnavailable <model> evidence.\n")
        result = report_run(self.worlds, self.branches, [self.worker], now=clock(400), regime="course",
            terminal_feasibility=evidence)
        self.assertEqual(result["tables"], self.result["tables"])
        self.assertEqual(result["traces"], self.result["traces"])
        self.assertEqual(result["report"]["selection"], self.result["report"]["selection"])
        execution = result["report"]["execution"]
        self.assertEqual(execution["status"], "terminal_feasibility")
        self.assertEqual(execution["coverage_status"], "complete")
        self.assertEqual(execution["terminal_feasibility"], evidence)
        evidence["text"] = "changed after call"
        self.assertNotEqual(execution["terminal_feasibility"], evidence)
        output = self.root / "terminal"
        write_report(output, result)
        html = (output / "report.html").read_bytes().decode("utf-8")
        self.assertIn("\r\n\tUnavailable &lt;model&gt; evidence.\n", html)
        self.assertIn("not achieved power", html)
        self.assertIn("not an equivalence margin", html)
        self.assertIn("no accepted model freeze", html)
        self.assertGreater(audit_links(output), 20)
        self.assertEqual(self.worker.read_bytes(), self.before)

    def test_invalid_regime_or_unsubstantiated_terminal_status_is_rejected_before_worker_reads(self):
        for regime, evidence in (("unknown", None), ("thesis", dict(source="x", text="failure")),
                ("course", {}), ("course", dict(source="x", text=" \n")),
                ("course", dict(source="x", text="failure", accepted_freeze=True))):
            with self.subTest(regime=regime, evidence=evidence), self.assertRaises(ValueError):
                report_run(self.worlds, self.branches, [self.root / "never-created.sqlite"], now=clock(400),
                    regime=regime, terminal_feasibility=evidence)
        self.assertFalse((self.root / "never-created.sqlite").exists())

    def test_primary_case_and_plot_joins_ignore_repeat_one_even_if_supplied_after_zero(self):
        tables = copy.deepcopy(self.result["tables"])
        primary = next(r for r in tables["estimands"]["world_contrasts"] if r["primary"])
        repeated = copy.deepcopy(primary)
        repeated.update(replicate=1, primary=True, value=-999)
        tables["estimands"]["world_contrasts"].append(repeated)
        actual = assemble_report(self.worlds, self.branches, tables, self.result["traces"], regime="course")
        for key in ("plotting_data", "selection", "cases"):
            self.assertEqual(actual[key], self.result["report"][key])

    def test_report_label_cannot_disagree_with_the_accepted_uncertainty_population_scope(self):
        with self.assertRaisesRegex(ValueError, "differs from saved uncertainty scope"):
            assemble_report(self.worlds, self.branches, self.result["tables"], self.result["traces"])
        tables = copy.deepcopy(self.result["tables"])
        tables["uncertainty"]["settings"].pop("regime")
        with self.assertRaisesRegex(ValueError, "differs from saved uncertainty scope"):
            assemble_report(self.worlds, self.branches, tables, self.result["traces"], regime="course")


class CourseReportCLITests(unittest.TestCase):
    def test_terminal_cli_reproduces_unknown_development_exports_and_preserves_literal_evidence(self):
        with tempfile.TemporaryDirectory(prefix="course-terminal-cli-") as temporary:
            root = Path(temporary)
            missing = root / "absent.sqlite"
            evidence = root / "terminal.md"
            literal = b"Synthetic terminal feasibility fixture.\r\nNo pretrained model was executed.\n"
            evidence.write_bytes(literal)
            command = [sys.executable, "-S", "-X", "utf8", "-m", "recovery", "analyze", "--report",
                "--stage", "development", "--manifest", str(ROOT / "tests/fixtures/population_course.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_course.json"), "--worker", str(missing),
                "--as-of", clock(400), "--resampling-seed", "37", "--terminal-feasibility", str(evidence)]
            for name in ("first", "second"):
                completed = subprocess.run(command + ["--output", str(root / name)], cwd=ROOT,
                    capture_output=True, text=True, timeout=120)
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                report = json.loads((root / name / "report.json").read_bytes())
                self.assertEqual(report["execution"]["status"], "terminal_feasibility")
                self.assertEqual(report["execution"]["coverage_status"], "incomplete")
                self.assertEqual(report["execution"]["terminal_feasibility"]["text"].encode(), literal)
                self.assertEqual(report["coverage"]["unknown"], 1178)
                self.assertEqual(report["settings"]["uncertainty"]["seed"], 37)
                self.assertFalse(report["cases"])
                self.assertGreaterEqual(audit_links(root / name), 20)
            for path in (root / "first").iterdir():
                self.assertEqual(path.read_bytes(), (root / "second" / path.name).read_bytes(), path.name)
            self.assertEqual(evidence.read_bytes(), literal)
            self.assertFalse(missing.exists())
            protected = subprocess.run(command + ["--output", str(root / "first")], cwd=ROOT,
                capture_output=True, text=True, timeout=120)
            self.assertEqual(protected.returncode, 2)
            self.assertIn("already exists", protected.stderr)

    def test_cli_rejects_missing_blank_thesis_and_nonreport_feasibility_evidence(self):
        with tempfile.TemporaryDirectory(prefix="course-terminal-errors-") as temporary:
            root = Path(temporary)
            evidence = root / "evidence.md"
            evidence.write_text("\n \t", encoding="utf-8")
            for regime, report, path, error in (("course", True, evidence, "nonempty"),
                    ("course", True, root / "missing.md", "No such file"),
                    ("target", True, evidence, "requires a course --report"),
                    ("course", False, evidence, "requires a course --report")):
                with self.subTest(regime=regime, report=report, path=path):
                    command = [sys.executable, "-S", "-X", "utf8", "-m", "recovery", "analyze",
                        "--stage", "development", "--manifest", str(ROOT / f"tests/fixtures/population_{regime}.json"),
                        "--schedule", str(ROOT / f"tests/fixtures/schedules_{regime}.json"),
                        "--worker", str(root / "absent.sqlite"), "--output", str(root / "rejected"),
                        "--terminal-feasibility", str(path)]
                    if report: command += ["--report", "--as-of", clock(400)]
                    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
                    self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
                    self.assertIn(error, completed.stderr)
                    self.assertFalse((root / "rejected").exists())
            self.assertFalse((root / "absent.sqlite").exists())


if __name__ == "__main__":
    unittest.main()
