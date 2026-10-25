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


if __name__ == "__main__":
    unittest.main()
