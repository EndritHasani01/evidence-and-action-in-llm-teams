"""Portable checkpoints: verification, selection, restore and mirror failure (spec 7.5)."""
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from recovery.i01.store import Store
from recovery.thesis import checkpoint as ckpt
from recovery.thesis.checks import check_checkpoint

BINDING = dict(regime="thesis-recovery-v1", study="cp")


class Checkpoints(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="thesis-cp-"))
        self.run = self.tmp / "run"
        (self.run / "inputs").mkdir(parents=True)
        (self.run / "inputs" / "thesis.json").write_text("{}")
        self.store = Store(self.run / "study.sqlite", BINDING, create=True)

    def tearDown(self):
        self.store.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_selfcheck(self):
        self.assertEqual(check_checkpoint(), ["checkpoint export/verify/restore"])

    def test_sequence_keeps_two_local_files_and_restores_exactly(self):
        receipts = [ckpt.export(self.run, self.store, study="cp", session="s", reason=str(i)) for i in range(3)]
        self.assertEqual([r["seq"] for r in receipts], [1, 2, 3])
        local = sorted(p.name for p in (self.run / "checkpoints").glob("*.zip"))
        self.assertEqual(local, [ckpt.name_for("cp", 2), ckpt.name_for("cp", 3)])
        manifest = ckpt.restore(Path(receipts[-1]["path"]), self.tmp / "restored")
        self.assertEqual(manifest["seq"], 3)
        restored = Store(self.tmp / "restored" / "study.sqlite", BINDING)
        self.assertEqual(restored.meta("checkpoint_seq"), 3)
        restored.close()
        with self.assertRaises(ValueError):
            ckpt.restore(Path(receipts[-1]["path"]), self.tmp / "restored")  # never overwrite a store

    def test_tampered_or_unsafe_archives_are_refused(self):
        receipt = ckpt.export(self.run, self.store, study="cp", session="s", reason="x")
        bad = self.tmp / "bad.zip"
        with zipfile.ZipFile(receipt["path"]) as src, zipfile.ZipFile(bad, "w") as dst:
            for item in src.infolist():
                data = src.read(item)
                if item.filename == "inputs/thesis.json":
                    data = b'{"tampered": true}'
                dst.writestr(item, data)
        with self.assertRaises(ValueError):
            ckpt.verify(bad)
        unsafe = self.tmp / "unsafe.zip"
        with zipfile.ZipFile(unsafe, "w") as dst:
            dst.writestr("../escape.txt", "x")
        with self.assertRaises(ValueError):
            ckpt.verify(unsafe)

    def test_newest_selection_and_conflict(self):
        a = self.tmp / "a"
        b = self.tmp / "b"
        a.mkdir(); b.mkdir()
        first = ckpt.export(self.run, self.store, study="cp", session="s", reason="1")
        shutil.copy2(first["path"], a)
        second = ckpt.export(self.run, self.store, study="cp", session="s", reason="2")
        shutil.copy2(second["path"], a)
        chosen = ckpt.select(ckpt.find("cp", [a]))
        self.assertEqual(chosen["seq"], 2)
        # A different archive claiming the same sequence (two concurrent sessions) is refused.
        self.store.put_meta("checkpoint_seq", 1)
        other = ckpt.export(self.run, self.store, study="cp", session="other", reason="diverged")
        self.assertEqual(other["seq"], 2)
        shutil.copy2(other["path"], b)
        with self.assertRaises(ValueError):
            ckpt.select(ckpt.find("cp", [a, b]))

    def test_mirror_failure_keeps_the_local_checkpoint(self):
        class Broken:
            def upload(self, path):
                raise ConnectionError("network down")

        receipt = ckpt.export(self.run, self.store, study="cp", session="s", reason="x", mirror=Broken(),
                              progress=lambda line: None)
        self.assertFalse(receipt["mirror"]["uploaded"])
        self.assertTrue(Path(receipt["path"]).exists())
        ckpt.verify(receipt["path"])
        mirror = ckpt.DirectoryMirror(self.tmp / "mirror")
        good = ckpt.export(self.run, self.store, study="cp", session="s", reason="y", mirror=mirror)
        self.assertTrue(good["mirror"]["uploaded"])
        self.assertEqual([e["seq"] for e in mirror.list("cp")], [good["seq"]])

    def test_manifest_records_whether_the_writing_session_had_finished(self):
        import json
        from recovery.i01.core import canonical
        first = ckpt.verify(ckpt.export(self.run, self.store, study="cp", session="s", reason="running")["path"])
        self.assertIs(first["session_closed"], False)
        with self.store.transaction():
            self.store.db.execute("INSERT OR REPLACE INTO sessions VALUES (?,?)",
                                  ("session/s", canonical(dict(session="s", closed=True))))
        second = ckpt.verify(ckpt.export(self.run, self.store, study="cp", session="s", reason="finish")["path"])
        self.assertIs(second["session_closed"], True)
        self.assertEqual(json.loads(json.dumps(second))["seq"], 2)

    def test_hub_mirror_verifies_uploads_and_lists_in_one_call(self):
        from types import SimpleNamespace as NS

        class FakeHub:
            """Records calls; stores bytes like a dataset repo (large files as LFS)."""

            def __init__(self, private=True, corrupt=False, lfs_from=2000):
                self.private, self.corrupt, self.files, self.info_calls = private, corrupt, {}, 0
                self.lfs_from = lfs_from

            def create_repo(self, repo, **kw):
                pass

            def repo_info(self, repo, **kw):
                return NS(private=self.private)

            def upload_file(self, *, path_or_fileobj, path_in_repo, **kw):
                data = Path(path_or_fileobj).read_bytes()
                self.files[path_in_repo] = data + (b"x" if self.corrupt else b"")

            def list_repo_files(self, repo, **kw):
                return list(self.files) + ["README.md"]

            def get_paths_info(self, repo, paths, **kw):
                import hashlib
                self.info_calls += 1
                out = []
                for p in paths:
                    data = self.files[p]
                    lfs = NS(sha256=hashlib.sha256(data).hexdigest()) if len(data) > self.lfs_from else None
                    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
                    out.append(NS(path=p, size=len(data), lfs=lfs, blob_id=blob, xet_hash=None))
                return out

        with self.assertRaises(ValueError):
            ckpt.HubMirror("me/public", "token", api=FakeHub(private=False))
        hub = FakeHub(lfs_from=0)  # every checkpoint stored as LFS
        mirror = ckpt.HubMirror("me/private", "token", api=hub)
        receipts = [ckpt.export(self.run, self.store, study="cp", session="s", reason=str(i), mirror=mirror)
                    for i in range(3)]
        self.assertTrue(all(r["mirror"]["uploaded"] and r["mirror"]["content_verified"] for r in receipts))
        hub.info_calls = 0
        listed = mirror.list("cp")
        self.assertEqual(([e["seq"] for e in listed], hub.info_calls), ([1, 2, 3], 1))
        self.assertEqual(listed[-1]["sha256"], receipts[-1]["sha256"])  # large files: LFS SHA-256
        small = ckpt.HubMirror("me/private", "token", api=FakeHub(lfs_from=10**9)).upload(Path(receipts[-1]["path"]))
        self.assertEqual((small["sha256_verified"], small["content_verified"]), (False, True))  # Git blob hash
        for kind in (0, 10**9):  # corrupted remote bytes are refused on both verification paths
            bad = ckpt.HubMirror("me/private", "token", api=FakeHub(corrupt=True, lfs_from=kind))
            with self.assertRaises(ValueError):
                bad.upload(Path(receipts[-1]["path"]))


if __name__ == "__main__":
    unittest.main()
