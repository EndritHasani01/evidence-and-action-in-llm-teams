from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.__main__ import load_size
from recovery.tasks import Size

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


if __name__ == "__main__":
    unittest.main()
