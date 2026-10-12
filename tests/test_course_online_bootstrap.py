"""Online preparation/resume integration on CPU; no model or CUDA execution."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.runner import DurableRunner
from recovery.accounting import CourseBudget
from scripts.course_kaggle_bootstrap import online, preparation_budget
from scripts.m5_course_smoke_assets import cpu_candidate_wheels
from scripts.m5_kaggle_preflight import assigned_preparation_window, installed_probe_script
from tests.test_course_run_all import config

ROOT = Path(__file__).resolve().parents[1]


class OnlineBootstrapTests(unittest.TestCase):
    def test_cold_resume_counts_original_allocations_once_without_fresh_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)
            settings = config()
            settings["allocated_at"] = datetime.now(timezone.utc).isoformat()
            original = deepcopy(settings)
            # Hardware has already entered the accepted budget, and all 24
            # smoke attempts are consumed. It must not block accepted main setup.
            saved = dict(budget=deepcopy(settings["budget"]),freeze={"accepted":"CPU fixture"})
            saved["budget"]["prior_development_gpu_hours"] = [.5,.5]
            saved["budget"]["prior_smoke_gpu_hours"] = [.5,.5]
            saved["budget"]["prior_smoke_attempts"] = 24
            for stage,start,end in (("hardware","09:00","09:15"),("development","09:15","09:30"),
                    ("main","09:30","09:45")):
                (bundle/stage).mkdir()
                for index in range(2):
                    with DurableRunner(bundle/stage/f"worker-{index}.sqlite",None) as runner:
                        store = runner.store
                        number = store.allocation_started(f"kaggle-t4-slot-{index}",
                            "main" if stage == "main" else "development",budget=CourseBudget(**settings["budget"]),
                            started_at=f"2026-10-11T{start}:00+00:00",billing=dict(physical_gpu_uuid=f"fixture-{index}"))
                        store.allocation_stopped(number,"CPU fixture actual release",released_at=f"2026-10-11T{end}:00+00:00")
            (bundle/"bootstrap-refusals").mkdir()
            (bundle/"bootstrap-refusals/hardware.json").write_text(json.dumps(dict(stage="hardware",
                allocated_at="2026-10-11T09:00:00+00:00",observed_at="2026-10-11T09:14:00+00:00",
                physical_devices=["fixture-0","fixture-1"])))
            budget = preparation_budget(ROOT,bundle,settings,saved)
            self.assertEqual(budget["prior_development_gpu_hours"],[1.,1.])
            self.assertEqual(budget["prior_other_course_gpu_hours"],[.5,.5])
            self.assertEqual(budget["prior_smoke_gpu_hours"],[.5,.5])
            self.assertEqual(budget["prior_smoke_attempts"],24)
            launch = dict(authorization="CPU fixture",prior_sessions_released=True,budget=budget,
                allocated_at=settings["allocated_at"],reported_quota_gpu_hours=30,provider_session_seconds=43200,
                release_instructions="CPU fixture; no actual GPU")
            self.assertGreater(assigned_preparation_window(launch,smoke_required=False),3000)
            with self.assertRaisesRegex(ValueError,"remaining_cumulative_smoke_attempt"):
                assigned_preparation_window(launch)
            self.assertEqual(settings,original)

    def test_unknown_old_release_refuses_before_download_and_supplied_receipt_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)
            settings = config()
            path = bundle/"development/worker-0.sqlite"
            path.parent.mkdir()
            with DurableRunner(path,None) as runner:
                runner.store.allocation_started("kaggle-t4-slot-0","development",budget=CourseBudget(**settings["budget"]),
                    started_at="2026-10-11T09:00:00+00:00",billing={})
            with self.assertRaisesRegex(ValueError,"previous_provider_release"):
                preparation_budget(ROOT,bundle,settings,dict(budget=settings["budget"]))
            settings["previous_session_release"] = dict(released_at="2026-10-11T09:15:00+00:00",evidence="CPU fixture provider receipt")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            budget = preparation_budget(ROOT,bundle,settings,dict(budget=settings["budget"]))
            self.assertEqual(budget["prior_development_gpu_hours"],[.25,.25])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)

    def test_repeated_preinstall_refusals_share_one_original_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory); receipts=bundle/"bootstrap-refusals"; receipts.mkdir()
            settings=config()
            settings["previous_session_release"]=dict(released_at="2026-10-11T09:15:00+00:00",evidence="CPU fixture")
            receipt=dict(stage="hardware",allocated_at="2026-10-11T09:00:00+00:00",
                observed_at="2026-10-11T09:05:00+00:00",physical_devices=["fixture-0","fixture-1"])
            for name in ("first.json","second.json"):
                (receipts/name).write_text(json.dumps(receipt))
            budget=preparation_budget(ROOT,bundle,settings,None)
            self.assertEqual(budget["prior_smoke_gpu_hours"],[.5,.5])
            self.assertEqual(budget["prior_development_gpu_hours"],[.5,.5])
            receipt["physical_devices"]=["different-0","different-1"]
            (receipts/"second.json").write_text(json.dumps(receipt))
            with self.assertRaisesRegex(ValueError,"physical_devices_differ"):
                preparation_budget(ROOT,bundle,settings,None)

    def test_online_entry_point_reaches_admission_without_site_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); source = base/"source"; source.mkdir()
            members = {}
            for name in ("recovery/__init__.py","recovery/costs.py"):
                path = source/name; path.parent.mkdir(exist_ok=True)
                raw = (ROOT/name).read_bytes(); path.write_bytes(raw)
                members[name] = dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
            (source/"SOURCE_COMMIT.txt").write_text("a"*40)
            (source/"source-manifest.json").write_text(json.dumps(dict(source_baseline_commit="a"*40,members=members)))
            settings = config(); settings["budget"]["prior_development_gpu_hours"] = None
            config_path = base/"operator-config.json"; config_path.write_text(json.dumps(settings))
            output = base/"output"
            result = subprocess.run([sys.executable,"-I","-S",ROOT/"scripts/course_kaggle_bootstrap.py","online",
                "--root",source,"--config",config_path,"--scratch",base/"scratch","--output",output],
                capture_output=True,text=True,timeout=20)
            self.assertNotEqual(result.returncode,0)
            receipt = json.loads((output/"bootstrap.json").read_bytes())
            self.assertIn("prior_allocation_smoke_or_release_evidence_missing",receipt["reason"])
            self.assertNotIn("ModuleNotFoundError",receipt["reason"])
            self.assertFalse((base/"scratch").exists())

    def test_online_main_resume_uses_retained_installer_without_portable_export(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); root=base/"source"; root.mkdir()
            (root/"SOURCE_COMMIT.txt").write_text("a"*40)
            (root/"source-manifest.json").write_text(json.dumps(dict(source_baseline_commit="a"*40,members={})))
            bundle=base/"bundle"; bundle.mkdir()
            settings=config(); settings["budget"]["prior_smoke_attempts"]=24
            (bundle/"run.json").write_text(json.dumps(dict(budget=settings["budget"],freeze={"at":"CPU fixture"})))
            config_path=bundle/"operator-config.json"; config_path.write_text(json.dumps(settings))
            prepared=dict(status="prepared",interpreter="fixture/bin/python",assets_receipt="fixture/assets.json",hf_cache="fixture/hub")
            with patch("scripts.m5_course_smoke_assets.prepare",return_value=prepared) as installer:
                result=online(root,config_path,base/"scratch",base/"output")
            self.assertTrue(result["online"])
            self.assertEqual(result["interpreter"],prepared["interpreter"])
            self.assertFalse(installer.call_args.kwargs["smoke_required"])
            self.assertEqual(installer.call_args.kwargs["online_config"],config_path)
            self.assertFalse((base/"course-assets.zip").exists())

    def test_cpu_rendering_uses_same_native_pins_without_gpu_dependencies(self):
        manifest=dict(candidate_wheels=[dict(name=n,version="fixture") for n in
            ("torch","triton","nvidia-cudnn-cu12","cuda-toolkit","accelerate","bitsandbytes","matplotlib","numpy","transformers","pydantic")])
        self.assertEqual([w["name"] for w in cpu_candidate_wheels(manifest)],
            ["matplotlib","numpy","transformers","pydantic"])
        script=installed_probe_script(dict(members={}),{},Path("fixture.json"),gpu=False)
        compile(script,"CPU provenance probe","exec")
        self.assertNotIn("import torch",script)
        self.assertIn("find_spec('torch') is None",script)


if __name__ == "__main__":
    unittest.main()
