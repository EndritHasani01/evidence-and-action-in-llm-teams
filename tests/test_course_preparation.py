"""Course CPU CLI, package boundary and process-independent preparation."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.manifests import manifest_bytes, schedule_bytes
from recovery.populations import prepare_population
from recovery.schedule import prepare_schedules
from recovery.tasks import Size
from tests.test_course_inputs import COURSE_SEED

ROOT = Path(__file__).resolve().parent.parent


class CoursePreparationTests(unittest.TestCase):
    def test_cpu_discovery_keeps_native_stack_checks_explicitly_available(self):
        discovered = unittest.TestLoader().discover(str(ROOT / "tests"),
            pattern="test_t4_attention.py", top_level_dir=str(ROOT))
        self.assertEqual(discovered.countTestCases(), 0)
        explicit = unittest.TestLoader().loadTestsFromName("tests.test_t4_attention")
        self.assertGreater(explicit.countTestCases(), 0)

    def test_actual_cpu_cli_prepares_saved_inputs_and_schedule_and_refuses_scope_drift(self):
        p = prepare_population(COURSE_SEED, Size.FALLBACK, regime="course")
        with tempfile.TemporaryDirectory() as directory:
            population, schedules = (Path(directory) / name for name in ("population.json", "schedules.json"))
            command = [sys.executable, "-S", "-B", "-m", "recovery", "prepare", "--regime", "course",
                       "--config", str(ROOT / "configs/course-inputs.toml")]
            inputs = command + ["--seed", str(COURSE_SEED), "--output", str(population)]
            result = subprocess.run(inputs, cwd=ROOT, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertIn(b"main=20", result.stdout)
            self.assertEqual(population.read_bytes(), manifest_bytes(p))
            plan = command + ["--manifest", str(population), "--output", str(schedules)]
            result = subprocess.run(plan, cwd=ROOT, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertIn(b"5,752 distinct / 6,280 logical", result.stdout)
            self.assertIn(b"1,114 distinct / 1,178 logical", result.stdout)
            self.assertIn(b"first 90 capability", result.stdout)
            self.assertEqual(schedules.read_bytes(), schedule_bytes(prepare_schedules(p)))
            for invocation, expected in ((inputs, b"File exists"), (plan, b"File exists"),
                    (command + ["--config", str(ROOT / "configs/study.toml"), "--seed", str(COURSE_SEED),
                                "--output", str(Path(directory) / "bad.json")], b"fallback mathematical size"),
                    ([item if item != "course" else "thesis" for item in plan], b"regime differs"),
                    (command + ["--manifest", str(ROOT / "tests/fixtures/population_fallback.json"),
                                "--output", str(Path(directory) / "bad.json")], b"regime differs"),
                    (plan + ["--authoritative", str(ROOT / "tests/fixtures/population_fallback.json")],
                     b"authoritative manifest")):
                result = subprocess.run(invocation, cwd=ROOT, capture_output=True, timeout=20)
                self.assertEqual(result.returncode, 2, result.stdout.decode() + result.stderr.decode())
                self.assertIn(expected, result.stderr)
            self.assertEqual(population.read_bytes(), manifest_bytes(p))
            self.assertEqual(schedules.read_bytes(), schedule_bytes(prepare_schedules(p)))
            self.assertFalse((Path(directory) / "bad.json").exists())

    def test_hashing_and_optional_dependencies_cannot_change_course_inputs_or_schedule(self):
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
state = random.getstate()
from recovery.populations import prepare_population
from recovery.schedule import prepare_schedules, dependency_order
from recovery.manifests import manifest_bytes, schedule_bytes
from recovery.tasks import Size
p = prepare_population(20261009, Size.FALLBACK, regime="course")
s = prepare_schedules(p)
assert len(dependency_order(tuple(reversed(s.main)))) == 6280
assert len(dependency_order(s.development)) == 1178
assert random.getstate() == state
assert not any(name.split(".")[0] in blocked for name in sys.modules)
sys.stdout.buffer.write(manifest_bytes(p) + schedule_bytes(s))
'''
        p = prepare_population(COURSE_SEED, Size.FALLBACK, regime="course")
        expected = manifest_bytes(p) + schedule_bytes(prepare_schedules(p))
        for hash_seed in ("1", "3981"):
            result = subprocess.run([sys.executable, "-S", "-B", "-c", script], cwd=ROOT,
                env=dict(os.environ, PYTHONHASHSEED=hash_seed), capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(result.stdout, expected)


if __name__ == "__main__":
    unittest.main()
