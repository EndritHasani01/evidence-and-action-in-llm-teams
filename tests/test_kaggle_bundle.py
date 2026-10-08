"""Transport manifests preserve gzip/nested bytes without regenerating fixtures."""

import gzip
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile

from scripts.build_kaggle_bundle import BASELINE_COMMIT, PAYLOAD_NAME, archive_manifest, build


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source.zip"
        nested = io.BytesIO()
        with zipfile.ZipFile(nested, "w") as archive:
            archive.writestr("probe.json", b'{"value":7}\n')
        self.members = {"SOURCE_COMMIT.txt": (BASELINE_COMMIT + "\n").encode(),
                        "tests/fixtures/capacity_report.json.gz": gzip.compress(b"synthetic\n", mtime=0),
                        "tests/fixtures/scripted_lifecycle_run.zip": nested.getvalue()}
        self.write_archive(self.members)

    def write_archive(self, members):
        with zipfile.ZipFile(self.source, "w") as archive:
            for name, data in members.items():
                archive.writestr(name, data)

    def test_raw_payload_and_each_compressed_member_are_exact(self):
        original = self.source.read_bytes()
        expected = hashlib.sha256(original).hexdigest()
        manifest = build(self.source, self.root / "delivery", "a" * 40,
                         expected_source_hash=expected)
        self.assertEqual((self.root / "delivery" / PAYLOAD_NAME).read_bytes(), original)
        self.assertEqual(manifest["expanded_bytes"], sum(map(len, self.members.values())))
        for name, content in self.members.items():
            self.assertEqual(manifest["members"][name],
                             {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
        self.assertEqual(manifest["build_commit"], "a" * 40)
        self.assertEqual(self.source.read_bytes(), original)

    def test_rejects_drift_and_never_overwrites_outputs(self):
        with self.assertRaisesRegex(ValueError, "canonical_source_archive_hash"):
            build(self.source, self.root / "absent")
        self.assertFalse((self.root / "absent").exists())
        existing = self.root / "existing"
        existing.mkdir()
        marker = existing / "keep"
        marker.write_bytes(b"original")
        with self.assertRaises(FileExistsError):
            build(self.source, existing)
        self.assertEqual(marker.read_bytes(), b"original")

    def test_rejects_invalid_build_provenance_and_source_marker(self):
        with self.assertRaisesRegex(ValueError, "build_commit"):
            build(self.source, self.root / "out", "main")
        self.write_archive(dict(self.members, **{"SOURCE_COMMIT.txt": b"main\n"}))
        with self.assertRaisesRegex(ValueError, "source_baseline_marker"):
            archive_manifest(self.source)

    def test_rejects_unsafe_duplicates_symlinks_and_path_conflicts(self):
        cases = [("../escape", b"x"), ("/escape", b"x"), ("C:/escape", b"x"),
                 ("a\\escape", b"x"), ("a//escape", b"x"), ("a/./escape", b"x"),
                 ("SOURCE_COMMIT.txt", b"duplicate"), ("a", b"x")]
        for name, data in cases:
            with self.subTest(name=name):
                with warnings.catch_warnings(record=True), zipfile.ZipFile(self.source, "w") as archive:
                    archive.writestr("SOURCE_COMMIT.txt", (BASELINE_COMMIT + "\n").encode())
                    archive.writestr("a/b", b"x")
                    # ZipInfo normally normalizes Windows separators at construction.
                    entry = zipfile.ZipInfo("member")
                    entry.filename = name
                    archive.writestr(entry, data)
                with self.assertRaises(ValueError):
                    archive_manifest(self.source)
        with zipfile.ZipFile(self.source, "w") as archive:
            entry = zipfile.ZipInfo("linked")
            entry.external_attr = 0o120777 << 16
            archive.writestr(entry, b"outside")
        with self.assertRaisesRegex(ValueError, "unsafe_source_member"):
            archive_manifest(self.source)


if __name__ == "__main__":
    unittest.main()
