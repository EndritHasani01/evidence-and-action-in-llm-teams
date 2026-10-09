"""Focused transport, failure/export and synthetic-backup checks; no model work."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

from scripts import build_kaggle_canary as builder
from scripts import m5_kaggle_upload_canary as canary


class KaggleUploadCanaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="m5-canary-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.artifact = builder.build(self.root / "build", self.root / "canary.ipynb")
        self.expected = self.artifact["expected"]
        self.payload = Path(self.artifact["payload"])
        self.input = self.root / "input"
        self.input.mkdir()

    def attach(self, folder="datasets/test/m5-source-canary"):
        target = self.input / folder / builder.PAYLOAD_NAME
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.payload.read_bytes())
        return target

    def run_canary(self):
        return canary.run_canary(self.input, self.root / "working", self.expected)

    def assert_export(self, result):
        path = Path(result["zip_path"])
        self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), result["zip_sha256"])
        with zipfile.ZipFile(path) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(json.loads(archive.read("summary.json")), result["summary"])
            for name in archive.namelist():
                self.assertEqual(archive.read(name), (path.parent / name).read_bytes())
        self.assertEqual(result["summary"]["model_generations"], 0)
        self.assertIsNone(result["summary"]["full_source_preparation"])
        self.assertIsNone(result["summary"]["model_smoke"])

    def test_build_preserves_originals_and_is_repeatable(self):
        other = builder.build(self.root / "second", self.root / "second.ipynb")
        self.assertEqual(Path(other["payload"]).read_bytes(), self.payload.read_bytes())
        self.assertEqual(other["expected"], self.expected)
        members = canary.verify_payload(self.payload, self.expected)
        self.assertIn(canary.GZIP_PATH, members)
        self.assertIn(canary.NESTED_PATH, members)
        with self.assertRaises(FileExistsError):
            builder.build(self.root / "build", self.root / "canary.ipynb")
        with self.assertRaises(ValueError):
            builder.build(self.root / "invalid", self.root / "invalid.ipynb", "not-a-commit")

    def test_notebook_embeds_exact_helper_and_canonical_expectations(self):
        document = json.loads((self.root / "canary.ipynb").read_text(encoding="utf-8"))
        namespace = {"__name__": "canary_test"}
        self.assertEqual(document["nbformat"], 4)
        for cell in document["cells"]:
            if cell["cell_type"] == "code":
                self.assertIsNone(cell["execution_count"])
                self.assertEqual(cell["outputs"], [])
                compile("".join(cell["source"]), cell["id"], "exec")
        exec("".join(document["cells"][1]["source"]), namespace)
        source = (builder.ROOT / "scripts/m5_kaggle_upload_canary.py").read_text(encoding="utf-8")
        self.assertEqual(namespace["CANARY_PROGRAM"], source)
        self.assertEqual(namespace["EXPECTED"], self.expected)

    def test_valid_payload_backup_export_and_new_run_preserve_inputs(self):
        target = self.attach()
        before = hashlib.sha256(target.read_bytes()).hexdigest()
        first, second = self.run_canary(), self.run_canary()
        self.assertTrue(first["summary"]["canary_checks_passed"])
        self.assertTrue(second["summary"]["canary_checks_passed"])
        self.assertNotEqual(first["run_directory"], second["run_directory"])
        self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)
        for result in [first, second]:
            self.assert_export(result)
            with zipfile.ZipFile(result["zip_path"]) as archive:
                restored = self.root / (Path(result["run_directory"]).name + ".sqlite")
                restored.write_bytes(archive.read("filesystem-backup.sqlite"))
            self.assertEqual(canary.check_sqlite(restored)["rows"], [[7]])
            self.assertEqual(result["report"]["filesystem"]["journal_mode"], "wal")
            self.assertEqual(result["report"]["filesystem"]["synchronous"], 2)

    def test_missing_payload_and_missing_input_export_real_failure(self):
        result = self.run_canary()
        self.assertFalse(result["summary"]["canary_checks_passed"])
        self.assertIn("payload_missing", result["summary"]["root_blocker"])
        self.assertEqual(result["report"]["stages"]["compressed_contents"]["status"], "blocked")
        self.assert_export(result)
        missing = canary.run_canary(self.root / "absent", self.root / "working", self.expected)
        self.assertIn("input_root_missing", missing["summary"]["root_blocker"])
        self.assert_export(missing)

    def test_transformed_input_is_inventory_evidence_not_repaired_source(self):
        source = self.input / "datasets/test/old-source"
        fixture = source / "tests/fixtures"
        fixture.mkdir(parents=True)
        (source / "SOURCE_COMMIT.txt").write_text(canary.BASELINE_COMMIT + "\n", encoding="utf-8")
        decompressed = fixture / "capacity_report.json"
        decompressed.write_text('{"originals_missing":true}\n', encoding="utf-8")
        (fixture / "scripted_lifecycle_run").mkdir()
        result = self.run_canary()
        legacy = result["report"]["legacy_source"]
        self.assertEqual(legacy["status"], "observed")
        paths = legacy["sources"][0]["paths"]
        self.assertEqual(paths[canary.GZIP_PATH]["kind"], "missing")
        self.assertEqual(paths[canary.GZIP_PATH[:-3]]["kind"], "file")
        self.assertEqual(paths[canary.NESTED_PATH[:-4]]["kind"], "directory")
        self.assertFalse((fixture / "capacity_report.json.gz").exists())
        self.assert_export(result)

    def test_ambiguous_and_altered_payloads_are_rejected(self):
        first = self.attach("one")
        second = self.attach("two")
        result = self.run_canary()
        self.assertIn("payload_ambiguous", result["summary"]["root_blocker"])
        self.assert_export(result)
        second.unlink()
        data = bytearray(first.read_bytes())
        data[20] ^= 1
        first.write_bytes(data)
        result = self.run_canary()
        self.assertIn("payload_hash_mismatch", result["summary"]["root_blocker"])
        self.assert_export(result)
        first.write_bytes(b"short")
        result = self.run_canary()
        self.assertIn("payload_size_mismatch", result["summary"]["root_blocker"])

    def test_archive_traversal_symlinks_duplicates_and_member_drift(self):
        for name in ["../outside", "/outside", "C:/outside", "..\\outside", "a//b", "a/./b"]:
            with self.subTest(name=name):
                data = builder.zip_bytes({name: b"bad"})
                with self.assertRaisesRegex(ValueError, "unsafe_archive_path"):
                    canary.verify_zip(data, builder.member_manifest({name: b"bad"}))
        import io
        for duplicate in [False, True]:
            buffer = io.BytesIO()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(buffer, "w") as archive:
                    info = zipfile.ZipInfo("fixture")
                    info.create_system = 3
                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                    archive.writestr(info, b"outside")
                    if duplicate:
                        archive.writestr("fixture", b"again")
            with self.assertRaisesRegex(ValueError, "duplicate_archive_member" if duplicate else "archive_symlink"):
                canary.verify_zip(buffer.getvalue(), {"fixture": {"bytes": 7, "sha256": canary.sha256(b"outside")}})
        data = builder.zip_bytes({"fixture": b"actual"})
        with self.assertRaisesRegex(ValueError, "archive_member_hash"):
            canary.verify_zip(data, builder.member_manifest({"fixture": b"alter!"}))
        with self.assertRaisesRegex(ValueError, "archive_member_set"):
            canary.verify_zip(data, {})
        with self.assertRaisesRegex(ValueError, "archive_member_size"):
            canary.verify_zip(data, builder.member_manifest({"fixture": b"short"}))
        self.assertFalse((self.root / "outside").exists())

    def test_inventory_limit_refuses_partial_uniqueness(self):
        self.attach()
        with patch.object(canary, "inventory", wraps=lambda root: canary_inventory(root, limit=1)):
            result = self.run_canary()
        self.assertIn("input_inventory_incomplete", result["summary"]["root_blocker"])
        self.assertEqual(result["report"]["stages"]["transport_bytes"]["status"], "blocked")
        self.assert_export(result)

    def test_symlinks_are_not_scanned_or_admitted(self):
        target = self.attach("real")
        link = self.input / "outside-link"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Host does not permit symlinks: {exc}")
        listing = canary.inventory(self.input)
        self.assertEqual(next(item for item in listing["entries"] if item["path"] == link.name)["kind"], "symlink")
        self.assertFalse(listing["truncated"])
        alias = self.input / builder.PAYLOAD_NAME
        alias.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "payload_not_regular_file"):
            canary.verify_payload(alias, self.expected)
        legacy = self.input / "old-source"
        legacy.mkdir()
        (legacy / "SOURCE_COMMIT.txt").write_text(canary.BASELINE_COMMIT, encoding="utf-8")
        (legacy / "tests").symlink_to(self.root, target_is_directory=True)
        observation = canary.legacy_source_observations(self.input, canary.inventory(self.input))
        self.assertEqual(observation["sources"][0]["paths"][canary.GZIP_PATH]["kind"], "symlink")

    def test_gpu_visibility_and_interruption_retain_reports(self):
        self.attach()
        with patch.object(canary, "visible_gpu_devices", return_value=["synthetic-device"]):
            result = self.run_canary()
        self.assertIn("gpu_visible", result["summary"]["root_blocker"])
        self.assertEqual(result["report"]["stages"]["transport_bytes"]["status"], "blocked")
        self.assert_export(result)
        with patch.object(canary, "verify_payload", side_effect=KeyboardInterrupt()):
            result = self.run_canary()
        self.assertIn("KeyboardInterrupt", result["summary"]["root_blocker"])
        self.assert_export(result)

    def test_compressed_defect_and_export_error_are_visible(self):
        self.attach()
        expected = copy.deepcopy(self.expected)
        expected["gzip_decoded"]["sha256"] = "0" * 64
        result = canary.run_canary(self.input, self.root / "working", expected)
        self.assertIn("gzip_decoded_bytes_mismatch", result["summary"]["root_blocker"])
        self.assert_export(result)
        with patch.object(canary, "export_results", side_effect=OSError("controlled full output")):
            result = self.run_canary()
        self.assertIsNone(result["zip_path"])
        self.assertIn("controlled full output", result["report"]["export_error"])
        retained = json.loads((Path(result["run_directory"]) / "canary-report.json").read_text(encoding="utf-8"))
        self.assertEqual(retained["export_error"], result["report"]["export_error"])

    def test_deadline_blocks_checks_and_still_exports(self):
        self.attach()
        with patch.object(canary.time, "monotonic", side_effect=[0] + [61] * 40):
            result = self.run_canary()
        self.assertIn("canary_deadline_reached", result["summary"]["root_blocker"])
        self.assertEqual(result["report"]["stages"]["transport_bytes"]["status"], "blocked")
        self.assert_export(result)


canary_inventory = canary.inventory


if __name__ == "__main__":
    unittest.main()
