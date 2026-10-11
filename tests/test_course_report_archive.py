"""Original course reports, portable plots and preserved thesis report assembly."""

from functools import cache
from collections import Counter
import gzip
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

from tests.course_report_archive import AS_OF, FIXTURE, PORTABLE, RETAINED_SCOPES, ROOT, RUN, SEED, TERMINAL, extract
from tests.test_report_run import audit_links


@cache
def retained():
    with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
        return json.load(source)


class CourseReportTablesTests(unittest.TestCase):
    def test_full_intended_population_preserves_unknown_intervals_shared_bounds_and_small_sample_limits(self):
        reports = retained()["cases"]
        self.assertEqual(len(reports), 8)
        full = reports["full-main-20"]["report"]
        self.assertEqual(tuple(full["coverage"][k] for k in ("scheduled", "recorded", "unknown")), (6280, 2170, 4110))
        self.assertEqual(full["execution"]["status"], "incomplete")
        primaries = {r["estimand"]: r for r in full["plotting_data"]["effects"] if r["primary"]}
        self.assertEqual(set(primaries), {"theta", "E_keep"})
        for name, bounds in (("theta", [-1.5, 1.5]), ("E_keep", [-.75, .75])):
            row = primaries[name]
            self.assertIsNone(row["estimate"])
            self.assertIsNone(row["interval"])
            self.assertEqual(row["eligible_worlds"], 20)
            self.assertEqual(row["observed_worlds"], 5)
            self.assertEqual(list(row["family_denominators"].values()), [4]*5)
            self.assertEqual(row["sensitivity"]["interval"], bounds)
            self.assertEqual(row["complete_case_estimate"], 0)
            self.assertIsNotNone(row["complete_case_hoeffding"])
        self.assertEqual(full["settings"]["uncertainty"]["seed"], SEED)
        self.assertEqual({r["N"] for r in full["reporting_references"]["focal"]}, {8})
        self.assertEqual(len({r["world_id"] for r in full["repeatability"]}), 5)
        # Original workers have eight active and 24 unknown Q treatments;
        # do not invent inactive observations in this particular archive.
        self.assertEqual(Counter(r["active"] for r in full["prose_activity"]), {True: 8, None: 24})
        self.assertTrue(any(r["unknown_selections"] > 0 for r in full["boundary_rule"]))
        for case in reports.values():
            report = case["report"]
            self.assertEqual(len(report["exhibits"]), 7)
            self.assertLessEqual(len(report["cases"]), 6)
            self.assertEqual(report["scope"]["regime"], "course")
            self.assertIn("Synthetic CPU validation", report["kind"])
            self.assertIsNone(report["execution"]["accepted_main_freeze"])
            for card in report["cases"]:
                self.assertTrue(all(row["replicate"] == 0 for row in card["trajectories"]))
                self.assertTrue(all("rep1" not in row["call_id"] for row in card["excerpts"]))

    def test_stopped_unexecuted_and_terminal_scopes_keep_unknowns_and_no_fabricated_negative_results(self):
        reports = retained()["cases"]
        stopped = next(c["report"] for name, c in reports.items() if name.endswith("/stopped"))
        self.assertEqual(stopped["coverage"]["unknown"], 16)
        for name, count in (("unexecuted-main-20", 6280), ("unexecuted-development", 1178), ("terminal-feasibility", 6280)):
            report = reports[name]["report"]
            self.assertEqual(report["coverage"]["protocol_outcomes"], {"unknown": count})
            self.assertEqual(report["coverage"]["recorded"], 0)
            self.assertEqual(report["selection"]["status"], "unavailable")
            self.assertFalse(report["cases"])
            self.assertEqual(report["execution"]["coverage_status"], "incomplete")
            if name == "terminal-feasibility":
                self.assertEqual(report["execution"]["status"], "terminal_feasibility")
                self.assertEqual(report["execution"]["terminal_feasibility"], TERMINAL)
            else:
                self.assertEqual(report["execution"]["status"], "incomplete")
                self.assertIsNone(report["execution"]["terminal_feasibility"])


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "original checkpoints need declared CPU packages")
class CourseReportWorkerTests(unittest.TestCase):
    def test_fresh_process_reproduces_eight_scopes_twice_without_execution_model_or_plot_imports(self):
        script = '''
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'torch','transformers','accelerate','bitsandbytes','matplotlib'} or fullname in {'recovery.runner','recovery.workers','recovery.inference','recovery.storage'}:
            raise AssertionError('offline course report crossed into execution: '+fullname)
sys.meta_path.insert(0, Block())
from tests.course_report_archive import main
raise SystemExit(main())
'''
        completed = subprocess.run([sys.executable, "-X", "utf8", "-c", script], cwd=ROOT,
            env=dict(os.environ, PYTHONHASHSEED="73"), capture_output=True, text=True, timeout=600)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(completed.stdout.count("Verified twice:"), 8)

    def test_course_cli_infers_full_manifest_scope_and_keeps_unavailable_history_counts(self):
        with tempfile.TemporaryDirectory(prefix="course-report-cli-") as temporary, ZipFile(RUN) as archive:
            root = Path(temporary)
            case = next(c for c in json.loads(archive.read("evidence.json"))["cases"] if c["directory"].startswith("test_every_family"))
            base = case["directory"]
            selected = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, ["inputs/population.json", "inputs/schedules.json", *[base + "/" + p for p in selected["workers"]]])
            paths = [root / base / p for p in selected["workers"]]
            before = [p.read_bytes() for p in paths]
            output = root / "report"
            command = [sys.executable, "-X", "utf8", "-m", "recovery", "analyze", "--report",
                "--resampling-seed", str(SEED), "--as-of", AS_OF, "--manifest", str(root / "inputs/population.json"),
                "--schedule", str(root / "inputs/schedules.json"), "--output", str(output)]
            for path in paths: command.extend(("--worker", str(path)))
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            report = json.loads((output / "report.json").read_bytes())
            expected = retained()["cases"]["full-main-20"]["report"]
            for key in ("coverage", "scope", "execution", "settings", "selection", "cases", "boundary_rule", "repeatability", "prose_activity"):
                self.assertEqual(report[key], expected[key], key)
            self.assertIn("not supplied", report["history_tokenizer"])
            self.assertTrue(any(row["history_content_tokens"] is None for row in report["plotting_data"]["context"]))
            for key in report["plotting_data"]:
                if key != "context": self.assertEqual(report["plotting_data"][key], expected["plotting_data"][key], key)
            self.assertGreater(audit_links(output), 20)
            self.assertEqual([p.read_bytes() for p in paths], before)

    def test_thesis_portable_scopes_reassemble_and_export_byte_identically_from_accepted_tables(self):
        # Renew the changed assembler/HTML on accepted snapshots; do not rerun
        # unchanged scoring, costs, statistics and sixteen original worker joins.
        from recovery.manifests import load_population, load_schedules
        from recovery.report import assemble_report, write_report
        from tests.report_archive import RETAINED_SCOPES as THESIS_SCOPES
        with tempfile.TemporaryDirectory(prefix="course-thesis-preservation-") as temporary, ZipFile(
                ROOT / "tests/fixtures/scripted_lifecycle_run.zip") as workers, ZipFile(
                ROOT / "tests/fixtures/scripted_reports.zip") as portable:
            root = Path(temporary)
            populations, schedules = {}, {}
            for size in ("target", "fallback"):
                extract(workers, root, [f"inputs/{size}/population.json", f"inputs/{size}/schedules.json"])
                populations[size] = load_population(root / f"inputs/{size}/population.json")
                schedules[size] = load_schedules(root / f"inputs/{size}/schedules.json", populations[size])
            for folder in THESIS_SCOPES.values():
                saved = json.loads(portable.read(folder + "/report.json"))
                inputs = json.loads(gzip.decompress(portable.read(folder + "/inputs.json.gz")))
                tables = json.loads(gzip.decompress(portable.read(folder + "/tables.json.gz")))
                traces = json.loads(gzip.decompress(portable.read(folder + "/traces.json.gz")))
                size = saved["scope"]["size"]
                all_worlds = populations[size].main + populations[size].development
                all_branches = schedules[size].main + schedules[size].development
                worlds = tuple(w for w in all_worlds if w.world_id in saved["scope"]["world_ids"])
                # Serialized dataclasses omit computed branch_id properties.
                ids = {b["calls"][0]["call_id"].rsplit("/r", 1)[0] for b in inputs["branches"]}
                branches = tuple(b for b in all_branches if b.branch_id in ids)
                actual = assemble_report(worlds, branches, tables, traces, provenance=saved["provenance"])
                actual["settings"]["generation_settings"] = saved["settings"]["generation_settings"]
                self.assertEqual(json.loads(json.dumps(actual)), saved, folder)
                result = dict(report=actual, inputs=inputs, tables=tables, traces=traces)
                export = root / folder
                write_report(export, result)
                # The retained page has figures; use the same renderer-independent
                # HTML path to compare it without regenerating those unchanged plots.
                from recovery.report import _report_html
                self.assertEqual(_report_html(actual, True).encode(), portable.read(folder + "/report.html"), folder)
                for name in ("report.json", "plotting.json", "tables.json.gz", "traces.json.gz", "inputs.json.gz",
                        "cases.html", "calls.html", "world_contrasts.csv", "intervals.csv"):
                    self.assertEqual((export / name).read_bytes(), portable.read(folder + "/" + name), folder + "/" + name)


@unittest.skipUnless(importlib.util.find_spec("matplotlib"), "portable figures need optional report extra")
class CourseReportPortableTests(unittest.TestCase):
    def test_clean_reopened_portable_reports_cases_links_and_all_35_rendered_pairs_reproduce(self):
        from recovery.figures import render_figures
        expected = retained()["cases"]
        with tempfile.TemporaryDirectory(prefix="course-report-portable-") as temporary, ZipFile(PORTABLE) as archive:
            root = Path(temporary)
            self.assertEqual(len(archive.namelist()), len(set(archive.namelist())))
            self.assertIn("INDEX.md", archive.namelist())
            for scope, folder in RETAINED_SCOPES.items():
                names = [n for n in archive.namelist() if n.startswith(folder + "/") and "/figures/" not in n]
                extract(archive, root, names)
                report_root = root / folder
                report = json.loads((report_root / "report.json").read_bytes())
                self.assertEqual(report, expected[scope]["report"], scope)
                self.assertEqual(json.loads((report_root / "plotting.json").read_bytes()), report["plotting_data"])
                tables = json.loads(gzip.decompress((report_root / "tables.json.gz").read_bytes()))
                self.assertEqual(tables["coverage"], report["coverage"])
                traces = json.loads(gzip.decompress((report_root / "traces.json.gz").read_bytes()))
                calls = {r["call_id"]: r for r in traces["calls"]}
                for card in report["cases"]:
                    self.assertTrue(all(excerpt == calls[excerpt["call_id"]] for excerpt in card["excerpts"]))
                    self.assertTrue(all(row["replicate"] == 0 for row in card["trajectories"]))
                render_figures(report_root)
                self.assertEqual(audit_links(report_root), expected[scope]["links_checked"] + 7)
                self.assertEqual((report_root / "report.html").read_bytes(), archive.read(folder + "/report.html"))
                for path in (report_root / "figures").iterdir():
                    original = archive.read(folder + "/figures/" + path.name)
                    self.assertEqual(path.read_bytes(), original, folder + "/" + path.name)
                    if path.suffix == ".svg":
                        ElementTree.parse(path)
                        self.assertIn("Exploratory course:", path.read_text(encoding="utf-8"))
                    elif path.suffix == ".png":
                        self.assertEqual(original[:8], b"\x89PNG\r\n\x1a\n")
                html = (report_root / "report.html").read_text(encoding="utf-8")
                self.assertIn("not achieved power", html)
                self.assertIn("accepted_main_freeze", html)
                if scope == "terminal-feasibility":
                    self.assertIn("not an actual model/GPU failure", html)


if __name__ == "__main__":
    unittest.main()
