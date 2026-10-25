"""The Kaggle notebook is thin, and its facade runs the rehearsal through the CLI (spec 7.3)."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]


class Notebook(unittest.TestCase):
    def test_every_cell_is_one_facade_call(self):
        nb = json.loads((ROOT / "notebooks/thesis_kaggle.ipynb").read_text(encoding="utf-8"))
        code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
        self.assertEqual(len(code), 10)
        self.assertIn("nb.start(", code[0])
        self.assertIn("pax_headers", code[0])
        calls = ["nb.install()", "nb.open_study()", "nb.cpu_checks()", "nb.develop()", "nb.freeze()",
                 "nb.main()", "nb.report()", "nb.finish()"]
        for cell, call in zip(code[1:9], calls):
            self.assertEqual(cell.strip(), call)
        self.assertTrue(code[9].lstrip().startswith("# nb.show("))
        from recovery.thesis import notebook
        for call in calls + ["nb.show("]:
            self.assertTrue(hasattr(notebook, call[3:].split("(")[0]))
        import importlib.util
        spec = importlib.util.spec_from_file_location("build_thesis_notebook", ROOT / "scripts/build_thesis_notebook.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        self.assertEqual(nb, json.loads(json.dumps(builder.build())))

    def test_facade_rehearsal_cells_end_with_checkpoints_or_receipts(self):
        from recovery.thesis import notebook as nb
        with tempfile.TemporaryDirectory(prefix="thesis-nb-") as name:
            base = Path(name)
            src = base / "src"
            for part in ("recovery", "configs"):
                shutil.copytree(ROOT / part, src / part, ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copy2(ROOT / "pyproject.toml", src / "pyproject.toml")
            (src / ".source-commit").write_text("a" * 40)
            nb.STATE.clear()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                nb.start(source_commit="a" * 40, study="nbtest", scope="rehearsal", session_hours=2,
                         start_new_study=True, source_root=src, working=base / "working",
                         scratch=base / "scratch", inputs=base / "inputs")
                nb.use_python(sys.executable)
                codes = [nb.open_study(), nb.cpu_checks(), nb.develop(), nb.freeze(), nb.main(), nb.report(), nb.finish()]
            text = out.getvalue()
            self.assertEqual(codes, [0] * 7, text[-3000:])
            run = base / "working" / "thesis" / "nbtest-rehearsal"
            self.assertTrue((run / "reports" / "report.md").exists())
            cells = sorted((run / "receipts" / "cells").rglob("*.json"))
            kinds = [json.loads(p.read_text())["kind"] for p in cells]
            self.assertEqual(kinds.count("checkpoint"), 6)  # open, check, develop, freeze, main, finish
            self.assertIn("receipt", kinds)  # report
            receipts = sorted((base / "working" / "thesis-receipts").rglob("*.json"))
            self.assertGreaterEqual(len(receipts), 8)
            self.assertIn("Off-session copy", text)
            # A rerun in the same kernel keeps the session deadline and repeats no work.
            deadline = nb.STATE["deadline"]
            with contextlib.redirect_stdout(io.StringIO()):
                nb.start(source_commit="a" * 40, study="nbtest", scope="rehearsal", session_hours=9,
                         source_root=src, working=base / "working", scratch=base / "scratch", inputs=base / "inputs")
            self.assertEqual(nb.STATE["deadline"], deadline)
            nb.STATE.clear()


if __name__ == "__main__":
    unittest.main()
