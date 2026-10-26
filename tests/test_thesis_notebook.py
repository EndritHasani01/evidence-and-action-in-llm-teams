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


class Sessions(unittest.TestCase):
    """Deadlines, kernel restarts, the mirror token and install failures (no network, no GPU)."""

    def setUp(self):
        from recovery.thesis import notebook as nb
        self.nb, self.saved = nb, nb._container_start
        self.tmp = Path(tempfile.mkdtemp(prefix="thesis-nb-session-"))
        self.src = self.tmp / "src"
        for part in ("recovery", "configs"):
            shutil.copytree(ROOT / part, self.src / part, ignore=shutil.ignore_patterns("__pycache__"))
        (self.src / ".source-commit").write_text("b" * 40)
        nb.STATE.clear()

    def tearDown(self):
        self.nb._container_start = self.saved
        self.nb.STATE.clear()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def start(self, **kw):
        args = dict(source_commit="b" * 40, study="nbsession", scope="cpu", session_hours=11, source_root=self.src,
                    working=self.tmp / "working", scratch=self.tmp / "scratch", inputs=self.tmp / "inputs")
        args.update(kw)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.nb.start(**args)
        return out.getvalue()

    def test_deadline_is_capped_inside_the_kaggle_session_and_survives_a_kernel_restart(self):
        from datetime import timedelta
        container = self.nb._now() - timedelta(hours=11, minutes=30)
        self.nb._container_start = lambda: container
        text = self.start()
        session, deadline = self.nb.STATE["session"], self.nb.STATE["deadline"]
        self.assertEqual(deadline, container + timedelta(hours=11, minutes=45))
        self.assertIn("Deadline capped", text)
        self.assertIn("less than an hour remains", text)
        self.nb.STATE["kernel_pid"] = -1  # a restarted kernel keeps nothing in memory but shares the container
        text = self.start(session_hours=11)
        self.assertEqual((self.nb.STATE["session"], self.nb.STATE["deadline"]), (session, deadline))
        self.assertIn("kernel restarted inside the same Kaggle session", text)
        self.nb.STATE["kernel_pid"] = -1
        self.nb._container_start = lambda: self.nb._now()  # a new Kaggle session: new container
        self.start()
        self.assertNotEqual(self.nb.STATE["session"], session)

    def test_container_start_is_read_from_proc(self):
        from datetime import timedelta
        proc = self.tmp / "proc"
        (proc / "1").mkdir(parents=True)
        (proc / "uptime").write_text("50000.25 12345.00\n")
        # PID 1 started 40,000 s after boot (100 ticks/s), so the container is 10,000.25 s old.
        # Field 22 is counted after the command name, which may itself contain ") ".
        (proc / "1" / "stat").write_text("1 (tini) x) S 0 1 1 0 -1 4194560 " + "0 " * 12 + "4000000 1 2\n")
        started = self.nb._container_start(proc, ticks=100)
        age = (self.nb._now() - started).total_seconds()
        self.assertAlmostEqual(age, 10000.25, delta=2)
        self.assertIsNone(self.nb._container_start(self.tmp / "missing"))
        self.assertLess(abs((started + timedelta(seconds=age)) - self.nb._now()), timedelta(seconds=2))

    def test_configured_mirror_without_token_stops_before_install(self):
        import os
        saved = os.environ.pop("HF_TOKEN", None)
        try:
            self.start(checkpoint_repo="someone/thesis-checkpoints")
        finally:
            if saved is not None:
                os.environ["HF_TOKEN"] = saved
        self.assertIn("HF_TOKEN", self.nb.STATE["stopped"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(self.nb.install())
            self.assertIsNone(self.nb.open_study())  # no environment, so no study work is attempted

    def test_install_failure_is_a_recorded_stop_not_an_exception(self):
        from unittest import mock
        self.start()
        host = dict(python="3.13.15 (main)", python_version=[3, 13, 15], gpus=[],
                    paths=dict(scratch=dict(free=2**40), working=dict(free=2**34)))
        with mock.patch("recovery.i01.setup.host_inventory", return_value=host), \
                mock.patch("recovery.i01.setup.create_environment", side_effect=RuntimeError("pip: no network")), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertIsNone(self.nb.install())
        self.assertIn("installing the pinned environment failed", self.nb.STATE["stopped"])
        self.assertIn("STOPPED", out.getvalue())
        self.assertFalse((self.tmp / "scratch" / f"venv-{'b' * 12}").exists())


class SourcePacket(unittest.TestCase):
    def test_packet_holds_committed_bytes_even_on_an_autocrlf_checkout(self):
        import subprocess
        import zipfile
        try:
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True,
                                    text=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git checkout not available")
        import importlib.util
        spec = importlib.util.spec_from_file_location("build_thesis_source", ROOT / "scripts/build_thesis_source.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as name, contextlib.redirect_stdout(io.StringIO()):
            packet = builder.build(commit, name)
            with zipfile.ZipFile(packet) as archive:
                for member in ("configs/i01-runtime.lock", "recovery/thesis/run.py", "configs/thesis.json"):
                    committed = subprocess.run(["git", "cat-file", "blob", f"{commit}:{member}"], cwd=ROOT,
                                               check=True, capture_output=True).stdout
                    self.assertEqual(archive.read(member), committed, member)
                self.assertEqual(archive.read(".source-commit").decode(), commit)


if __name__ == "__main__":
    unittest.main()
