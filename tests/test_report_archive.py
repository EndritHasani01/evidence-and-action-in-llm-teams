"""Retained ordinary-M3 report evidence and frozen unknown denominators."""

import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "ordinary checkpoint decoder needs declared CPU packages")
class ReportArchiveTests(unittest.TestCase):
    def test_all_sixteen_scopes_reproduce_all_m4_outputs_twice_from_original_workers(self):
        from tests.report_archive import FIXTURE, reconstruct
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            expected = json.load(source)
        self.assertEqual(actual.keys(), expected.keys())
        self.assertEqual(actual["cases"].keys(), expected["cases"].keys())
        for name, case in actual["cases"].items():
            self.assertTrue(case == expected["cases"][name], name)
            self.assertEqual(len(case["report"]["exhibits"]), 7)
            self.assertLessEqual(len(case["report"]["cases"]), 6)
            self.assertIn("not model capability", case["report"]["kind"])
            for card in case["report"]["cases"]:
                self.assertTrue(all(row["replicate"] == 0 for row in card["trajectories"]))
            if (case["report"]["selection"]["fallback"] or {}).get("reason") == "all_zero_regression":
                self.assertTrue(any(r["regression"] for r in case["report"]["cases"][0]["trajectories"]))
        for size, count, n, unknown in (("target", 60, 12, 15486), ("fallback", 40, 8, 10390)):
            report = actual["cases"][f"full-main-{size}-{count}"]["report"]
            self.assertEqual(report["coverage"]["unknown"], unknown)
            primaries = [r for r in report["plotting_data"]["effects"] if r["primary"]]
            self.assertEqual(len(primaries), 2)
            for row in primaries:
                self.assertIsNone(row["estimate"])
                self.assertIsNone(row["interval"])
                self.assertEqual(row["observed_worlds"], 5)
                self.assertEqual(row["eligible_worlds"], count)
                self.assertEqual(list(row["family_denominators"].values()), [n]*5)
                self.assertIsNotNone(row["complete_case_hoeffding"])
            self.assertTrue(any(r["active"] is None for r in report["prose_activity"]))
        stopped = next(c["report"] for n, c in actual["cases"].items() if n.endswith("/stopped"))
        self.assertEqual(stopped["coverage"]["unknown"], 16)
        self.assertEqual(stopped["selection"]["status"], "unavailable")
        self.assertFalse(stopped["cases"])

    def test_portable_complete_incomplete_and_stopped_reports_match_retained_evidence(self):
        from tests.report_archive import FIXTURE, RETAINED_SCOPES, ROOT
        from tests.test_report_run import audit_links
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            expected = json.load(source)["cases"]
        with tempfile.TemporaryDirectory(prefix="m4-report-artifact-") as directory, ZipFile(
                ROOT/"tests/fixtures/scripted_reports.zip") as archive:
            root = Path(directory)
            self.assertEqual(len(archive.namelist()), len(set(archive.namelist())))
            for name in archive.namelist():
                self.assertTrue((root/name).resolve().is_relative_to(root.resolve()))
                archive.extract(name, root)
            self.assertTrue((root/"INDEX.md").is_file())
            for scope, folder in RETAINED_SCOPES.items():
                report_root = root/folder
                report = json.loads((report_root/"report.json").read_bytes())
                self.assertEqual(report, expected[scope]["report"], scope)
                self.assertEqual(json.loads((report_root/"plotting.json").read_bytes()), report["plotting_data"])
                with gzip.open(report_root/"tables.json.gz", "rt", encoding="utf-8") as source:
                    tables = json.load(source)
                self.assertEqual({key: len(value) for key, value in tables.items() if isinstance(value, list)},
                                 expected[scope]["table_rows"])
                self.assertEqual(tables["coverage"], report["coverage"])
                self.assertEqual(audit_links(report_root), expected[scope]["links_checked"] + 7)
                with gzip.open(report_root/"traces.json.gz", "rt", encoding="utf-8") as source:
                    traces = json.load(source)
                calls = {row["call_id"]: row for row in traces["calls"]}
                for card in report["cases"]:
                    self.assertTrue(all(excerpt == calls[excerpt["call_id"]] for excerpt in card["excerpts"]))
                for exhibit in report["exhibits"]:
                    svg = report_root/"figures"/(exhibit["id"]+".svg")
                    ElementTree.parse(svg)
                    self.assertIn(report["kind"], svg.read_text(encoding="utf-8"))
                    png = report_root/"figures"/(exhibit["id"]+".png")
                    self.assertEqual(png.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
