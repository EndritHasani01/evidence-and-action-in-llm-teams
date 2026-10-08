"""Transport manifests preserve gzip/nested bytes without regenerating fixtures."""

import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile

from scripts.build_kaggle_bundle import BASELINE_COMMIT, PAYLOAD_NAME, archive_manifest, build
from scripts.build_kaggle_bundle import candidate_files, candidate_lock
from unittest.mock import patch, MagicMock


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

    def test_target_wheel_selection_pins_one_compatible_file_and_byte_range_total(self):
        pylock=self.root/'pylock.toml'
        pylock.write_text('''lock-version="1.0"
[[packages]]
name="probe"
version="1.0"
wheels=[{url="https://files.pythonhosted.org/probe-1.0-py3-none-any.whl",size=9,hashes={sha256="SHA_A"}},
        {url="https://files.pythonhosted.org/probe-1.0-cp313-cp313-manylinux_2_28_x86_64.whl",hashes={sha256="SHA_B"}}]
'''.replace('SHA_A','a'*64).replace('SHA_B','b'*64))
        response=MagicMock()
        response.headers={'Content-Length':'1','Content-Range':'bytes 0-0/17'}
        with patch('scripts.build_kaggle_bundle.urlopen') as open_url:
            open_url.return_value.__enter__.return_value=response
            files=candidate_files(pylock)
        self.assertEqual(files[0]['bytes'],17)
        self.assertIn('-cp313-',files[0]['filename'])
        self.assertEqual(candidate_lock(files),'probe==1.0 --hash=sha256:'+'b'*64+'\n')

    def test_target_metadata_refuses_untrusted_origin_or_missing_wheel(self):
        path=self.root/'pylock.toml'
        for wheels in ['[]','[{url="https://unreviewed.invalid/probe.whl",size=1,hashes={sha256="abc"}}]']:
            path.write_text('lock-version="1.0"\n[[packages]]\nname="probe"\nversion="1.0"\nwheels='+wheels+'\n')
            with self.assertRaises(ValueError):candidate_files(path)

    def test_notebook_bootstrap_binds_the_delivered_helper_manifest_and_lock(self):
        helper=self.root/'helper.py'
        helper.write_text("marker='reviewed helper'\n",encoding='utf-8')
        notebook=self.root/'prepared.ipynb'
        output=self.root/'prepared'
        files=[{'name':'probe','version':'1.0','bytes':7,'sha256':'a'*64}]
        manifest=build(self.source,output,'a'*40,expected_source_hash=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                       candidate_wheels=files,build_tools={'pip':{}},helper=helper,notebook=notebook)
        document=json.loads(notebook.read_text(encoding='utf-8'))
        code=[c for c in document['cells'] if c['cell_type']=='code']
        self.assertEqual(len(document['cells']),6);self.assertEqual(len(code),3)
        for cell in code:
            self.assertEqual(cell['outputs'],[]);self.assertIsNone(cell['execution_count'])
            compile(''.join(cell['source']),'notebook-cell','exec')
        namespace={};exec(''.join(code[0]['source']),namespace)
        self.assertEqual(namespace['preflight_namespace']['marker'],'reviewed helper')
        self.assertEqual(namespace['EXPECTED'],manifest)
        with self.assertRaises(FileExistsError):
            build(self.source,self.root/'not-created',notebook=notebook)
        self.assertFalse((self.root/'not-created').exists())


if __name__ == "__main__":
    unittest.main()
