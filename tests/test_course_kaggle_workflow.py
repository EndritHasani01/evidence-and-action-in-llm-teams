"""Scripted integration of the actual package orchestration, never GPU evidence."""

from contextlib import redirect_stdout, closing
from dataclasses import replace
import io
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from recovery.runner import DurableRunner, WorkerReader
from recovery.schedule import dependency_order
from recovery.storage import WorkerStore, record_json
from recovery.witness import witness_reply
from scripts.build_course_kaggle import notebook
from scripts.course_kaggle_workflow import (audit_records, backup_bundle, capability_gate,
    confirm_previous_release, initialize, main, pilot_gate, safe_extract)
from tests.course_worker_cases import SETTINGS, TOKENIZER, bind, course_inputs

ROOT = Path(__file__).resolve().parents[1]


def legal_script(view, rendered, tokenized, *, seed, settings):
    return witness_reply(view, TOKENIZER)


class CourseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.directory = Path(cls.temporary.name)
        population, schedules = course_inputs()
        cls.worlds, cls.branches = population.development, schedules.development
        cls.path = cls.directory/"pilot.sqlite"
        cls.by_world = {w.world_id:w for w in cls.worlds}
        with DurableRunner(cls.path, TOKENIZER, legal_script, scripted=True) as runner:
            bind(runner.store, cls.worlds, cls.branches)
            prelude = [b for b in cls.branches if b.phase in ("prefix", "control")]
            for branch in prelude:
                if branch.phase == "control":
                    runner.run_control(cls.by_world[branch.world_id], branch, settings=SETTINGS)
                else:
                    runner.start(cls.by_world[branch.world_id], branch, settings=SETTINGS)
                    for number in range(1,5):
                        runner.run_round(branch.branch_id, number)
            cls.capability = capability_gate(cls.worlds, cls.branches, (cls.path,))
            runner.backup(cls.directory/"capability.sqlite")
            ordered = dict.fromkeys(b.branch_id for b,c in dependency_order(cls.branches))
            by_branch = {b.branch_id:b for b in cls.branches}
            for branch_id in ordered:
                branch = by_branch[branch_id]
                if branch.phase != "continuation":
                    continue
                runner.start(cls.by_world[branch.world_id], branch, settings=SETTINGS)
                for number in range(1,5):
                    runner.run_round(branch.branch_id, number)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_first90_positive_and_incomplete_denominators(self):
        self.assertTrue(self.capability["passed"])
        self.assertEqual(self.capability["counts"]["recorded"],90)
        self.assertEqual(self.capability["counts"]["controls_correct"],10)
        self.assertEqual(self.capability["counts"]["jointly_correct_prefixes"],5)
        unknown = capability_gate(self.worlds,self.branches,(self.directory/"absent.sqlite",))
        self.assertEqual(unknown["counts"]["recorded"],0)
        self.assertEqual(unknown["status"],"incomplete")
        self.assertFalse((self.directory/"absent.sqlite").exists())

    def test_actual_full_pilot_raw_reconstruction_and_gate(self):
        audit = audit_records(self.worlds,self.branches,(self.path,),TOKENIZER,SETTINGS)
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["coverage"]["recorded"],1178)
        self.assertEqual(audit["inference_calls"],0)
        gate = pilot_gate(self.worlds,self.branches,(self.path,),audit=audit)
        self.assertTrue(gate["passed"])
        self.assertEqual(gate["distinct_recorded"],1114)
        self.assertEqual(gate["protocol_valid"],1114)
        without_audit = pilot_gate(self.worlds,self.branches,(self.path,))
        self.assertFalse(without_audit["passed"])

    def test_failed_or_missing_capability_never_admits_full_pilot(self):
        gate = pilot_gate(self.worlds,self.branches,(self.directory/"capability.sqlite",),audit=dict(passed=True))
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["distinct_recorded"],90)
        self.assertEqual(gate["validity_denominator"],1114)
        self.assertEqual(gate["status"],"incomplete")

    def test_portable_backup_reopens_and_preserves_raw_calls_without_wal(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"
            (bundle/"development").mkdir(parents=True)
            source=bundle/"development/worker-0.sqlite"
            shutil.copyfile(self.path,source)
            archive=Path(directory)/"course-resume.zip"
            backup_bundle(bundle,archive)
            reopened=Path(directory)/"reopened"
            safe_extract(archive,reopened)
            with zipfile.ZipFile(archive) as z:
                self.assertFalse(any(name.endswith(("-wal","-shm",".owner")) for name in z.namelist()))
            store=WorkerStore(reopened/"development/worker-0.sqlite",readonly=True)
            try:
                self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM calls").fetchone()[0],1178)
                self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],1114)
                self.assertEqual(store.connection.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            finally:
                store.close()

    def test_missing_duplicate_seed_and_state_corruption_fail_offline_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            copy=Path(directory)/"copy.sqlite"
            shutil.copyfile(self.path,copy)
            with self.assertRaisesRegex(ValueError,"duplicate"):
                audit_records(self.worlds,self.branches,(self.path,copy),TOKENIZER,SETTINGS)
            with closing(sqlite3.connect(copy)) as db, db:
                db.execute("UPDATE calls SET seed=seed+1 WHERE call_id=(SELECT MIN(call_id) FROM calls)")
            with self.assertRaises(ValueError):
                audit_records(self.worlds,self.branches,(copy,),TOKENIZER,SETTINGS)
            shutil.copyfile(self.path,copy)
            with closing(sqlite3.connect(copy)) as db, db:
                db.execute("DELETE FROM calls WHERE call_id=(SELECT MIN(call_id) FROM calls)")
            with self.assertRaises(ValueError):
                audit_records(self.worlds,self.branches,(copy,),TOKENIZER,SETTINGS)

    def test_provider_release_is_separate_and_closes_both_original_allocations(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"
            (bundle/"main").mkdir(parents=True)
            for i in range(2):
                store=WorkerStore(bundle/"main"/f"worker-{i}.sqlite")
                store.allocation_started(f"physical-{i}","main",started_at="2026-10-12T09:00:00+00:00")
                store.close()
            self.assertEqual(confirm_previous_release(bundle,{}),0)
            receipt=dict(released_at="2026-10-12T09:15:00+00:00",evidence="CPU fixture provider receipt; not actual release")
            self.assertEqual(confirm_previous_release(bundle,receipt,now="2026-10-12T10:00:00+00:00"),2)
            self.assertEqual(confirm_previous_release(bundle,receipt,now="2026-10-12T10:00:00+00:00"),0)
            for i in range(2):
                store=WorkerStore(bundle/"main"/f"worker-{i}.sqlite",readonly=True)
                self.assertEqual(store.connection.execute("SELECT stopped_at FROM allocations").fetchone()[0],receipt["released_at"])
                store.close()

    def test_guarded_cli_exports_a_real_blocker_without_gpu_or_weights(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"
            config=Path(directory)/"config.json"
            config.write_bytes((ROOT/"configs/course-kaggle.json").read_bytes())
            with patch("scripts.m5_course_smoke.ModelFactory",side_effect=AssertionError("GPU forbidden")),redirect_stdout(io.StringIO()):
                code=main(["--root",str(ROOT),"--bundle",str(bundle),"--config",str(config),"--action","hardware"])
            self.assertEqual(code,2)
            result=json.loads((bundle/"last-action.json").read_bytes())
            self.assertIn("authorization_missing",result["reason"])
            self.assertTrue((Path(directory)/"course-resume.zip").exists())
            self.assertEqual(list(bundle.rglob("worker-*.sqlite")),[])

    def test_notebook_cells_compile_guard_defaults_and_safe_archives(self):
        document=notebook("a"*64,"b"*40)
        for cell in document["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]),cell["id"],"exec")
        options=next(c for c in document["cells"] if c["id"] == "action")
        text="".join(options["source"])
        self.assertIn('ACTION = "run_all"',text)
        values={}
        with patch("pathlib.Path.is_dir",return_value=False): exec(text,values)
        self.assertFalse(values["ENABLE_GPU"])
        with patch("pathlib.Path.is_dir",return_value=True), \
             patch("pathlib.Path.iterdir",return_value=iter([Path("CPU GPU-presence fixture")])):
            exec(text,values)
        self.assertTrue(values["ENABLE_GPU"])
        with tempfile.TemporaryDirectory() as directory:
            archive=Path(directory)/"unsafe.zip"
            with zipfile.ZipFile(archive,"w") as z:
                z.writestr("../escape","wrong")
            with self.assertRaises(ValueError):
                safe_extract(archive,Path(directory)/"destination")


if __name__ == "__main__":
    unittest.main()
