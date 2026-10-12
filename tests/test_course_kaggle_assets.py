"""Tiny local assets exercise packaging, native identities and refusal accounting."""

from contextlib import closing
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from scripts.course_kaggle_bootstrap import export_assets, extract_assets
from scripts.course_kaggle_workflow import (confirm_previous_release, record_refused_allocation,
    refused_workers, snapshot, audit_records, scope)
from scripts.m5_course_smoke_assets import download_weights_stdlib
from scripts.m5_course_smoke import CANDIDATE
from recovery.storage import WorkerStore

ROOT = Path(__file__).resolve().parents[1]


class PortableAssetTests(unittest.TestCase):
    def test_full_missing_main_scope_audits_without_creating_control_workers(self):
        from tests.course_worker_cases import TOKENIZER, SETTINGS
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"
            worlds,branches=scope(ROOT,bundle,"main")
            paths=(bundle/"main/worker-0.sqlite",bundle/"main/worker-1.sqlite")
            result=audit_records(worlds,branches,paths,TOKENIZER,SETTINGS)
            self.assertEqual(result["coverage"]["unknown"],6280)
            self.assertTrue(result["passed"])
            self.assertFalse(result["committed_schedule_complete"])
            self.assertFalse(any(p.exists() for p in paths))

    def test_native_lfs_download_identity_and_copied_metadata_without_model_or_sdk(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/"source"
            inspection=root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json"
            inspection.parent.mkdir(parents=True)
            inspection.write_text(json.dumps(dict(checkpoint_index=dict(shard_files=["model.safetensors"]))))
            metadata=root/"metadata/4B/config.json"
            metadata.parent.mkdir(parents=True)
            metadata.write_bytes(b'{"test":"CPU fixture"}')
            manifest=dict(members={"metadata/4B/config.json":dict(bytes=metadata.stat().st_size,sha256=hashlib.sha256(metadata.read_bytes()).hexdigest())})
            weights=b"tiny CPU fixture, no pretrained weights"
            info=dict(sha=CANDIDATE.revision,siblings=[dict(rfilename="model.safetensors",lfs=dict(size=len(weights),sha256=hashlib.sha256(weights).hexdigest()))])
            receipt=Path(directory)/"weights.json"
            with patch("urllib.request.urlopen",side_effect=[io.BytesIO(json.dumps(info).encode()),io.BytesIO(weights)]):
                download_weights_stdlib(root,manifest,Path(directory)/"hub",receipt)
            actual=json.loads(receipt.read_bytes())
            self.assertFalse(actual["model_weights_loaded"])
            self.assertEqual(actual["revision"],CANDIDATE.revision)
            self.assertEqual((Path(actual["snapshot"])/"model.safetensors").read_bytes(),weights)
            info["sha"]="foreign"
            with patch("urllib.request.urlopen",return_value=io.BytesIO(json.dumps(info).encode())),self.assertRaises(ValueError):
                download_weights_stdlib(root,manifest,Path(directory)/"foreign",receipt)

    def test_export_consumes_only_fresh_rebuildable_downloads_and_keeps_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            root,scratch=base/"source",base/"scratch"
            root.mkdir(); scratch.mkdir()
            (root/"source-manifest.json").write_text(json.dumps(dict(source_baseline_commit="CPU-fixture")))
            (scratch/"venv").mkdir()
            (scratch/"venv/not-an-experiment.txt").write_text("rebuildable")
            for folder in ("wheels","built"):
                (scratch/folder).mkdir()
                (scratch/folder/"fixture.whl").write_bytes(b"tiny rebuildable wheel")
            for name in ("install.lock","pip.lock","build-constraints.txt"):
                (scratch/name).write_text("fixture")
            checkpoint=scratch/"hub/models--CPU--fixture/snapshots/revision"
            checkpoint.mkdir(parents=True)
            (checkpoint/"model.safetensors").write_bytes(b"tiny fixture")
            receipt=base/"receipt.json"
            receipt.write_text(json.dumps(dict(hf_cache=str(scratch/"hub"),model="CPU/fixture",revision="revision",checkpoint_files={"model.safetensors":{}})))
            target=base/"course-assets.zip"
            export_assets(root,scratch,receipt,target)
            self.assertTrue(receipt.exists())
            self.assertFalse((scratch/"venv").exists())
            self.assertFalse((checkpoint/"model.safetensors").exists())
            self.assertFalse((scratch/"wheels/fixture.whl").exists())
            unpacked=base/"unpacked"
            extract_assets(target,unpacked)
            self.assertEqual((unpacked/"checkpoint/model.safetensors").read_bytes(),b"tiny fixture")
            self.assertTrue((unpacked/"prepared-assets.json").exists())

    def test_early_gate_refusal_records_both_assigned_devices_without_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"
            config=json.loads((ROOT/"configs/course-kaggle.json").read_bytes())
            config.update(execute_gpu=True,allocated_at="2026-10-12T09:00:00+00:00")
            config["budget"]["prior_evidence"]="CPU fixture zero bounds; not actual resource evidence"
            for key in config["budget"]:
                if key.startswith("prior_") and key.endswith("gpu_hours"):
                    config["budget"][key]=[0,0]
            config["budget"]["prior_smoke_attempts"]=0
            record_refused_allocation(ROOT,bundle,config,"pilot","CPU fixture gate refusal",devices=("fixture-0","fixture-1"))
            paths=refused_workers(bundle)
            self.assertEqual(len(paths),2)
            for path in paths:
                store=WorkerStore(path,readonly=True)
                self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM calls").fetchone()[0],0)
                self.assertIsNone(store.connection.execute("SELECT stopped_at FROM allocations").fetchone()[0])
                store.close()
            receipt=dict(released_at="2026-10-12T09:15:00+00:00",evidence="CPU fixture provider release")
            self.assertEqual(confirm_previous_release(bundle,receipt,now="2026-10-12T10:00:00+00:00"),2)
            from scripts.m5_course_preparation import read
            run=dict(settings=read(ROOT/"notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")["settings"],budget=config["budget"])
            actual=snapshot(ROOT,bundle,"development",run,now="2026-10-12T10:00:00+00:00")
            self.assertAlmostEqual(actual["resources"]["course_gpu_hours"][1],.5)
            self.assertEqual(actual["counts"]["finished_generations"],0)


if __name__ == "__main__":
    unittest.main()
