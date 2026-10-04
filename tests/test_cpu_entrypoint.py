from pathlib import Path
from contextlib import redirect_stderr
import io
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.__main__ import load_size, main
from recovery.tasks import Size
from recovery.manifests import load_population, manifest_bytes
from recovery.populations import PopulationExhausted, Rejection, prepare_population

ROOT = Path(__file__).resolve().parent.parent


class CPUEntryPointTests(unittest.TestCase):
    def test_declared_configuration_and_only_uniform_size_choices(self):
        self.assertIs(load_size(ROOT / "configs/study.toml"), Size.TARGET)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "study.toml"
            for size in Size:
                path.write_text(f'size = "{size.value}"\n')
                self.assertIs(load_size(path), size)
            for invalid in ('size = "tiny"', 'size = 8', 'size = true',
                            'size = ["target"]', '', 'size = "target"\nm = 6'):
                path.write_text(invalid)
                with self.assertRaises(ValueError):
                    load_size(path)

    def test_cpu_import_and_all_task_shapes_with_inference_imports_forbidden(self):
        # A fresh interpreter without site packages also blocks every model-stack
        # import attempt, so a missing optional dependency cannot hide a try/import.
        script = '''
import importlib.abc
import random
import sys

blocked = {"torch", "transformers", "accelerate", "bitsandbytes", "langgraph",
           "langchain", "numpy", "scipy", "pandas", "matplotlib", "pydantic"}
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("unexpected dependency import: " + fullname)
sys.meta_path.insert(0, BlockImports())
unrelated_state = random.getstate()
import recovery
import recovery.__main__
from recovery.tasks import Task, Size, generate_world
from recovery.truth import solve_world, exact_candidate
for size in Size:
    for task in Task:
        world = generate_world(task, size, generation_rng=random.Random(31),
                               ownership_rng=random.Random(17))
        truth = solve_world(world)
        for peer in (None, 0, 1, 2, 3):
            assert exact_candidate(truth, truth.candidate(peer), peer)
assert not any(name.split(".")[0] in blocked for name in sys.modules)
assert random.getstate() == unrelated_state
'''
        result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cli_rejects_invalid_configuration_with_failure_exit(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "study.toml"
            path.write_text('size = "tiny"\n')
            result = subprocess.run([sys.executable, "-S", "-m", "recovery", "validate",
                                     "--config", str(path)], cwd=ROOT,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("error:", result.stderr)

    def test_cli_prepares_each_size_and_refuses_overwrite_or_bad_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            config = directory / "study.toml"
            for size in Size:
                config.write_text(f'size = "{size.value}"\n')
                manifest = directory / f"{size.value}.json"
                command = [sys.executable, "-S", "-m", "recovery", "prepare", "--config", str(config),
                           "--seed", "7", "--output", str(manifest)]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("not an M5 freeze", result.stdout)
                loaded = load_population(manifest)
                self.assertEqual(manifest.read_bytes(), manifest_bytes(prepare_population(7, size)))
                original_bytes = manifest.read_bytes()
                repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=20)
                self.assertEqual(repeated.returncode, 2)
                self.assertEqual(manifest.read_bytes(), original_bytes)
                self.assertIs(loaded.size, size)
            invalid = subprocess.run([sys.executable, "-S", "-m", "recovery", "prepare",
                                      "--seed", "-1", "--output", str(directory / "bad.json")],
                                     cwd=ROOT, capture_output=True, text=True, timeout=20)
            self.assertEqual(invalid.returncode, 2)
            self.assertFalse((directory / "bad.json").exists())

    def test_cli_rejects_changed_manifest_and_wrong_config_before_test_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            saved = directory / "saved.json"
            candidate = directory / "candidate.json"
            saved.write_bytes(manifest_bytes(prepare_population(7, Size.FALLBACK)))
            # Other seed produces a valid manifest; equality must still reject it.
            candidate.write_bytes(manifest_bytes(prepare_population(8, Size.FALLBACK)))
            config = directory / "study.toml"
            config.write_text('size = "fallback"\n')
            for arguments, message in (
                    (["--manifest", str(candidate), "--authoritative", str(saved),
                      "--config", str(config)], "authoritative manifest"),
                    (["--manifest", str(saved)], "size differs"),
                    (["--authoritative", str(saved)], "requires --manifest")):
                result = subprocess.run([sys.executable, "-S", "-m", "recovery", "validate", *arguments],
                                        cwd=ROOT, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertNotIn("test_", result.stderr)

    def test_cli_exhaustion_retains_every_rejection_and_writes_no_manifest(self):
        failure = PopulationExhausted("main-top_k-01", 3,
                                     tuple(Rejection(i, ("no_owner_changing_edit",))
                                           for i in range(1, 1001)))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "exhausted.json"
            arguments = ["recovery", "prepare", "--seed", "1", "--output", str(path)]
            evidence = io.StringIO()
            with patch.object(sys, "argv", arguments), redirect_stderr(evidence), \
                    patch("recovery.__main__.prepare_population", side_effect=failure):
                self.assertEqual(main(), 1)
            self.assertFalse(path.exists())
            self.assertEqual(len(evidence.getvalue().splitlines()), 1001)
            self.assertIn("exhausted 1000 generation attempts for owner 3", evidence.getvalue())
            self.assertIn("attempt 1000: no_owner_changing_edit", evidence.getvalue())


if __name__ == "__main__":
    unittest.main()
