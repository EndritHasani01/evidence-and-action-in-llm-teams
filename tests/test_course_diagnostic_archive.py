"""Original course checkpoints, independent SQL references and read-only reproduction."""

import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

from tests.course_diagnostics_archive import AS_OF, FIXTURE, ROOT, RUN, extract, native_audit, reconstruct, worker_audit


class CourseDiagnosticTablesTests(unittest.TestCase):
    def test_saved_full_intended_populations_and_unavailable_costs_are_explicit(self):
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            actual = json.load(source)
        self.assertEqual(len(actual["cases"]), 7)
        self.assertIn("CPU", actual["kind"])
        full = actual["cases"]["full-main-20"]
        self.assertEqual((full["coverage"]["scheduled"], full["coverage"]["recorded"], full["coverage"]["unknown"]), (6280, 2170, 4110))
        self.assertEqual(len(full["information"]["prefix"]), 320)
        self.assertEqual(len(full["information"]["owner_exposure"]), 28)
        self.assertEqual(len({r["world_id"] for r in full["costs"]["policy_costs"]}), 20)
        for row in full["costs"]["selection_frequencies"]:
            expected = 20 if row["event"] in ("revision", "sham") and row["replicate"] == 0 else 8 if row["event"] == "preserving" else 5
            if row["level"] == "pooled": self.assertEqual(row["frequency_denominator"], expected)
            self.assertEqual(sum(row["counts"].values()) + row["unknown_selections"], row["scheduled_worlds"])
        for case in actual["cases"].values():
            for row in case["costs"]["strategy_worlds"]:
                self.assertEqual(row["auc_denominator"], 16)
                self.assertEqual(row["final_peer_denominator"], 4)
                if not row["available"]:
                    self.assertIsNone(row["auc"])
                    self.assertIsNone(row["complete_policy_seconds"])
                elif row["strategy"] == "boundary_rule":
                    selection = next(r for r in case["costs"]["boundary_selections"] if (r["world_id"], r["event"], r["replicate"]) == (row["world_id"], row["event"], row["replicate"]))
                    self.assertEqual(row["branch_id"], selection["selected_branch_id"])
            for row in case["information"]["receipt_timing"]:
                self.assertEqual(row["scheduled_rounds"], 4)
                self.assertEqual(len(row["rounds"]), 4)
            for row in case["peer_diagnostics"]:
                self.assertTrue(row["call_id"] and row["prefix_call_id"] and row["generation_id"])
        for name, count in (("unexecuted-main-20", 6280), ("unexecuted-development", 1178)):
            case = actual["cases"][name]
            self.assertEqual(case["coverage"]["unknown"], count)
            self.assertEqual(case["costs"]["physical"]["attempts"], 0)
            self.assertTrue(all(r["selected_policy"] is None for r in case["costs"]["boundary_selections"]))
            self.assertTrue(all(r["complete_policy_seconds"] is None for r in case["costs"]["policy_costs"]))
            self.assertTrue(all(r["unique_acquired_count"] is None for r in case["information"]["boundary_acquisition"]))
        self.assertEqual(len(actual["atlas_examples"]), 6)
        self.assertTrue(any(actual["raw_unchanged_excerpts"].values()))


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "saved checkpoint decoder needs declared CPU dependencies")
class CourseDiagnosticArchiveTests(unittest.TestCase):
    def test_full_course_cli_original_workers_and_exclusive_export(self):
        with tempfile.TemporaryDirectory(prefix="course-diagnostic-cli-") as temporary, ZipFile(RUN) as archive:
            root = Path(temporary)
            case = next(c for c in json.loads(archive.read("evidence.json"))["cases"] if c["directory"].startswith("test_every_family"))
            base = case["directory"]
            selection = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, ["inputs/population.json", "inputs/schedules.json", *[base + "/" + name for name in selection["workers"]]])
            paths = [root / base / name for name in selection["workers"]]
            before = [path.read_bytes() for path in paths]
            output = root / "diagnostics.json.gz"
            command = [sys.executable, "-X", "utf8", "-m", "recovery", "analyze", "--costs", "--diagnostics", "--estimands",
                "--as-of", AS_OF, "--stage", "main", "--manifest", str(root / "inputs/population.json"),
                "--schedule", str(root / "inputs/schedules.json"), "--output", str(output)]
            for path in paths: command.extend(("--worker", str(path)))
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            actual = json.loads(gzip.decompress(output.read_bytes()))
            with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
                expected = json.load(source)["cases"]["full-main-20"]
            self.assertTrue(actual["costs"] == expected["costs"], "original full-policy CLI cost export differs")
            self.assertEqual(actual["coverage"], expected["coverage"])
            self.assertEqual(len(actual["estimands"]["populations"][0]["world_ids"]), 20)
            for name, rows in expected["information"].items():
                if not isinstance(rows, list): continue
                self.assertEqual(len(actual["information"][name]), len(rows))
                for a, b in zip(actual["information"][name], rows):
                    keys = a.keys() - {"history_content_tokens", "history_token_reason"}
                    self.assertTrue({k: a[k] for k in keys} == {k: b[k] for k in keys}, name)
            self.assertEqual([path.read_bytes() for path in paths], before)
            exported = output.read_bytes()
            repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(output.read_bytes(), exported)

    def test_seven_course_scopes_match_independent_original_references_and_saved_tables(self):
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            saved = json.load(source)
        # Avoid unittest's quadratic multi-megabyte automatic dictionary diff.
        self.assertTrue(actual.keys() == saved.keys())
        for name, case in actual["cases"].items():
            for table, value in case.items():
                self.assertTrue(value == saved["cases"][name][table], f"{name}/{table} differs")
        for key in actual.keys() - {"cases"}:
            self.assertTrue(actual[key] == saved[key], key + " differs")
        hand = next(a for name, a in actual["independent_original_checks"].items() if name.startswith("test_hand_costs"))
        self.assertEqual(hand["physical_seconds"], [261, 263])
        self.assertEqual(hand["original_attempts"], 131)
        stopped = next(case for name, case in actual["cases"].items() if name.endswith("/stopped"))
        self.assertEqual(stopped["coverage"]["unknown"], 16)
        self.assertTrue(all(not row["complete"] and row["complete_policy_seconds"] is None for row in stopped["costs"]["policy_costs"]))

    def test_sixteen_fault_probe_scopes_and_native_original_requests_remain_unmodified(self):
        cases = worker_audit()
        self.assertEqual(len(cases), 16)
        self.assertEqual(sum(row["recorded"] for row in cases.values()), 1422)
        self.assertEqual(sum(row["unknown"] for row in cases.values()), 312)
        native = native_audit()
        self.assertGreater(native["native_saved_requests"], 0)
        self.assertEqual(native["native_saved_requests"], native["native_input_token_counts"])
        self.assertGreater(native["nonempty_history_tokens_unavailable_without_matching_tokenizer"], 0)

    def test_fresh_hash_process_reproduces_without_runtime_or_model_imports(self):
        script = '''
import importlib.abc, sys
blocked = {"torch", "transformers", "numpy", "scipy", "pandas", "matplotlib"}
runtime = {"recovery.inference", "recovery.runner", "recovery.workers", "recovery.accounting", "recovery.protocol", "recovery.rounds", "recovery.replay", "recovery.events"}
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked or fullname in runtime:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.course_diagnostics_archive import main
raise SystemExit(main())
'''
        result = subprocess.run([sys.executable, "-X", "utf8", "-c", script], cwd=ROOT,
            capture_output=True, text=True, timeout=360)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no inference or empirical result", result.stdout)


if __name__ == "__main__":
    unittest.main()
