from copy import deepcopy
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.manifests import (assert_schedules_match, load_population, load_schedules,
                                save_schedules, schedule_bytes)
from recovery.schedule import dependency_order, prepare_schedules, validate_schedules
from recovery.tasks import Size

ROOT = Path(__file__).resolve().parent.parent


class ScheduleManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.populations = {s: load_population(ROOT / f"tests/fixtures/population_{s.value}.json") for s in Size}
        cls.schedules = {s: prepare_schedules(p) for s, p in cls.populations.items()}

    def test_both_sizes_round_trip_without_rebuilding_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            for size, schedules in self.schedules.items():
                population = self.populations[size]
                path = Path(temporary) / f"schedules_{size.value}.json"
                save_schedules(schedules, population, path)
                original = path.read_bytes()
                with patch("recovery.schedule._prepare_branches", side_effect=AssertionError("rebuilt")), \
                        patch("recovery.populations.generate_world", side_effect=AssertionError("resampled")):
                    loaded = load_schedules(path, population, authoritative=schedules)
                self.assertEqual(loaded, schedules)
                self.assertEqual(schedule_bytes(loaded), original)
                for count in (60, 40):
                    self.assertEqual(dependency_order(loaded.main_for(population, count)),
                                     dependency_order(schedules.main_for(population, count)))
                self.assertEqual(dependency_order(loaded.development), dependency_order(schedules.development))
                with self.assertRaises(FileExistsError):
                    save_schedules(schedules, population, path)
                self.assertEqual(path.read_bytes(), original)

    def test_retained_prepared_fixture_is_canonical_and_contains_only_host_schedule_fields(self):
        population = self.populations[Size.TARGET]
        path = ROOT / "tests/fixtures/schedules_target.json"
        with patch("recovery.schedule._prepare_branches", side_effect=AssertionError("rebuilt")):
            loaded = load_schedules(path, population, authoritative=self.schedules[Size.TARGET])
        self.assertEqual(path.read_bytes(), schedule_bytes(loaded))
        data = json.loads(path.read_bytes())
        self.assertEqual(set(data), {"format_version", "master_seed", "size", "main", "development"})
        self.assertEqual(set(data["main"][0]), {"world_id", "task", "phase", "event", "policy", "replicate",
                                             "prefix_parent", "calls"})
        self.assertEqual(set(data["main"][0]["calls"][0]), {"call_id", "round_number", "peer", "seed", "replay_parent"})
        # No duplicated raw worlds, edits, gold, model output, runtime statuses,
        # or inference configuration. Metadata here is still forbidden in views.
        serialized = path.read_text(encoding="utf-8")
        for field in ("records", "main_edit", "gold", "candidate", "correctness", "status", "model"):
            self.assertNotIn(f'"{field}":', serialized)

    def test_serialized_scientific_and_structural_mutations_fail(self):
        schedules = self.schedules[Size.TARGET]
        population = self.populations[Size.TARGET]
        baseline = asdict(schedules)
        b = next(i for i, row in enumerate(baseline["main"]) if row["phase"] == "continuation" and row["policy"] == "B")
        mask = next(i for i, row in enumerate(baseline["main"]) if row["policy"] == "P_G")
        receipt = next(i for i, row in enumerate(baseline["main"]) if row["policy"] == "B_delta")
        control = next(i for i, row in enumerate(baseline["main"]) if row["phase"] == "control")
        other_b = next(i for i, row in enumerate(baseline["main"]) if row["phase"] == "continuation"
                       and row["event"] == "revision" and row["policy"] == "B" and row["replicate"] == 0
                       and row["world_id"] != baseline["main"][b]["world_id"])
        # Work with JSON lists, just as an external edit would.
        baseline = json.loads(json.dumps(baseline))
        mutations = [
            ("format boolean", lambda d: d.update(format_version=True)),
            ("seed changed", lambda d: d.update(master_seed=d["master_seed"] + 1)),
            ("wrong size", lambda d: d.update(size="fallback")),
            ("unknown metadata", lambda d: d.update(extra=1)),
            ("missing branch", lambda d: d["main"].pop()),
            ("duplicate branch", lambda d: d["main"].append(deepcopy(d["main"][b]))),
            ("wrong task", lambda d: d["main"][b].update(task="prefix_sum")),
            ("unprescribed policy", lambda d: d["main"][b].update(policy="new_policy")),
            ("unprescribed receipt sham", lambda d: d["main"][receipt].update(event="sham")),
            ("wrong original prefix", lambda d: d["main"][b].update(prefix_parent=d["main"][1]["world_id"])),
            ("replicate boolean", lambda d: d["main"][b].update(replicate=False)),
            ("missing opportunity", lambda d: d["main"][b]["calls"].pop()),
            ("duplicate call", lambda d: d["main"][b]["calls"][1].update(call_id=d["main"][b]["calls"][0]["call_id"])),
            ("wrong round", lambda d: d["main"][b]["calls"][0].update(round_number=2)),
            ("boolean peer", lambda d: d["main"][b]["calls"][0].update(peer=False)),
            ("seed shifted", lambda d: d["main"][b]["calls"][0].update(seed=0)),
            ("float seed", lambda d: d["main"][b]["calls"][0].update(seed=float(d["main"][b]["calls"][0]["seed"]))),
            ("unexpected source payload", lambda d: d["main"][b]["calls"][0].update(gold=[])),
            ("extra reuse from equal seeds", lambda d: d["main"][b]["calls"][0].update(replay_parent=d["main"][b]["calls"][0]["call_id"])),
            ("missing replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=None)),
            ("nonexistent replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent="missing")),
            ("cross event replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][mask]["calls"][0]["replay_parent"].replace("/revision/", "/sham/"))),
            ("cross replicate replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][mask]["calls"][0]["replay_parent"].replace("/rep0/", "/rep1/"))),
            ("cross peer replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][mask]["calls"][1]["replay_parent"])),
            ("cross world replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][other_b]["calls"][0]["call_id"])),
            ("wrong retention replay", lambda d: d["main"][mask]["calls"][0].update(replay_parent=d["main"][mask]["calls"][0]["replay_parent"].replace("/C/", "/B/"))),
            ("control peer", lambda d: d["main"][control]["calls"][0].update(peer=0)),
            ("control prefix", lambda d: d["main"][control].update(prefix_parent=d["main"][0]["world_id"])),
            ("development from main", lambda d: d["development"].append(deepcopy(d["main"][mask]))),
            ("recovery before capability", lambda d: d["development"].insert(0, d["development"].pop())),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            for name, mutate in mutations:
                with self.subTest(mutation=name):
                    data = deepcopy(baseline)
                    mutate(data)
                    path.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_schedules(path, population)
            for malformed in ('{"format_version":1,"format_version":1}', '{"x":NaN}', '[]', '{}',
                              'true', 'null', '"text"', '{'):
                path.write_text(malformed, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_schedules(path, population)

    def test_valid_changed_order_requires_exact_saved_authority_comparison(self):
        schedules = self.schedules[Size.TARGET]
        population = self.populations[Size.TARGET]
        changed = replace(schedules, main=tuple(reversed(schedules.main)))
        validate_schedules(changed, population)  # Admissible dependency order, but different saved artifact.
        with self.assertRaisesRegex(ValueError, "authoritative schedule"):
            assert_schedules_match(changed, schedules)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "changed.json"
            save_schedules(changed, population, path)
            with self.assertRaisesRegex(ValueError, "authoritative schedule"):
                load_schedules(path, population, authoritative=schedules)
        assert_schedules_match(schedules, schedules)

    def test_wrong_population_rejected_and_invalid_schedule_not_saved(self):
        schedules = self.schedules[Size.TARGET]
        fallback = self.populations[Size.FALLBACK]
        with self.assertRaisesRegex(ValueError, "configuration differs"):
            schedules.main_for(fallback)
        with self.assertRaises(ValueError):
            schedules.main_for(self.populations[Size.TARGET], 50)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            with self.assertRaisesRegex(ValueError, "configuration differs"):
                save_schedules(schedules, fallback, path)
            self.assertFalse(path.exists())
            broken = replace(schedules, main=schedules.main[:-1])
            with self.assertRaisesRegex(ValueError, "missing required"):
                save_schedules(broken, self.populations[Size.TARGET], path)
            self.assertFalse(path.exists())

    def test_process_hashing_optional_imports_and_global_rng_cannot_change_schedules(self):
        script = '''
import importlib.abc
import random
import sys
from pathlib import Path
blocked = {"torch", "transformers", "accelerate", "bitsandbytes", "langgraph",
           "langchain", "numpy", "scipy", "pandas", "matplotlib", "pydantic"}
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("unexpected dependency import: " + fullname)
sys.meta_path.insert(0, BlockImports())
state = random.getstate()
from recovery.manifests import load_population, schedule_bytes
from recovery.schedule import prepare_schedules, dependency_order
p = load_population(Path("tests/fixtures/population_target.json"))
s = prepare_schedules(p)
assert len(dependency_order(s.main)) == 17656
assert len(dependency_order(s.main_for(p, 40))) == 12560
assert len(dependency_order(s.development)) == 1178
assert random.getstate() == state
assert not any(name.split(".")[0] in blocked for name in sys.modules)
sys.stdout.buffer.write(schedule_bytes(s))
'''
        for hash_seed in ("1", "3981"):
            result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT,
                                    env=dict(os.environ, PYTHONHASHSEED=hash_seed),
                                    capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(result.stdout, schedule_bytes(self.schedules[Size.TARGET]))


if __name__ == "__main__":
    unittest.main()
