"""Optional standard plotting renderer: uncertainty, gaps and stable artifacts."""

import importlib.util
import tempfile
from pathlib import Path
import unittest

from recovery.report import report_run, write_report
from tests.cost_fixture import clock, write_cost_worker
from tests.test_report_run import audit_links, measured_fixture


@unittest.skipUnless(importlib.util.find_spec("matplotlib"), "SVG/PNG rendering needs optional report extra")
class ReportFigureTests(unittest.TestCase):
    def test_all_seven_figures_reproduce_with_coherent_synthetic_labels_and_links(self):
        from recovery.figures import render_figures
        w, b, r, i, a = measured_fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root/"worker.sqlite"
            write_cost_worker(path, r, i, a)
            result = report_run(w, b, [path], now=clock(400))
            first, second = root/"first", root/"second"
            write_report(first, result, figures=True)
            write_report(second, result, figures=True)
            self.assertEqual(len([p for p in (first/"figures").iterdir() if p.suffix in (".svg", ".png")]), 14)
            for path in (first/"figures").iterdir():
                self.assertEqual(path.read_bytes(), (second/"figures"/path.name).read_bytes(), path.name)
                if path.suffix != ".json":
                    self.assertGreater(path.stat().st_size, 1000)
                if path.suffix == ".svg":
                    self.assertIn("Synthetic CPU validation", path.read_text(encoding="utf-8"))
            self.assertGreater(audit_links(first), 0)
            with self.assertRaises(FileExistsError):
                render_figures(first)

    def test_all_unknown_report_renders_missing_values_without_zero_points(self):
        from recovery.figures import render_figures
        w, b, _, _, _ = measured_fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = root/"missing.sqlite"
            result = report_run(w, b, [missing], now=clock(400))
            output = root/"unknown"
            write_report(output, result)
            render_figures(output)
            self.assertFalse(missing.exists())
            svg = (output/"figures/quality_cost.svg").read_text(encoding="utf-8")
            self.assertIn("unavailable", svg)
            self.assertFalse(result["report"]["cases"])
            self.assertGreater(audit_links(output), 0)


if __name__ == "__main__":
    unittest.main()
