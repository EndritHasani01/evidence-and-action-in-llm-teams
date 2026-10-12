"""Automatic-stage and continuous-allocation CPU checks, never GPU evidence."""

from contextlib import closing, redirect_stdout
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from recovery.accounting import CourseBudget, BudgetStop
from recovery.storage import WorkerStore
from recovery.runner import DurableRunner
from recovery.workers import LocalScheduler, WorkerSpec, WorkerInterrupted
from scripts.course_kaggle_workflow import (accepted_budget, current_assignment, run_all,
    snapshot, transfer_assignment, worker_paths, scope, recover_bootstrap_refusals, refused_workers)
from scripts.m5_kaggle_preflight import download_native_ranges
from tests.course_worker_cases import SETTINGS, branches, course_inputs, provider_factory, tokenizer_factory

ROOT = Path(__file__).resolve().parents[1]


def config():
    value = json.loads((ROOT/"configs/course-kaggle.json").read_bytes())
    value.update(execute_gpu=True,continuous_assignment=True,allocated_at="2026-10-12T09:00:00+00:00",
        prior_sessions_released=True,provider_quota_gpu_hours=30,provider_session_seconds=43200)
    value["authorizations"].update({k:"CPU test fixture only" for k in value["authorizations"]})
    value["budget"]["prior_evidence"] = "CPU fixture bounds; no actual allocation or model"
    for key in value["budget"]:
        if key.startswith("prior_") and key.endswith("gpu_hours"): value["budget"][key] = [0,0]
    value["budget"]["prior_smoke_attempts"] = 0
    return value


class RunAllTests(unittest.TestCase):
    def test_unknown_bootstrap_clock_needs_evidence_and_original_receipt_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"; (bundle/"bootstrap-refusals").mkdir(parents=True)
            cfg=config()
            receipt=dict(config=cfg,allocated_at=None,physical_devices=["fixture-0","fixture-1"],
                observed_at="2026-10-12T09:05:00+00:00",stage="hardware",reason="CPU fixture refusal")
            path=bundle/"bootstrap-refusals/refusal.json"; path.write_text(json.dumps(receipt))
            original=path.read_bytes()
            with self.assertRaises(BudgetStop): recover_bootstrap_refusals(ROOT,bundle,cfg)
            cfg["bootstrap_refusal_assignments"]={"refusal.json":dict(allocated_at="2026-10-12T09:00:00+00:00",
                evidence="CPU fixture provider facts; no real allocation")}
            recover_bootstrap_refusals(ROOT,bundle,cfg)
            recover_bootstrap_refusals(ROOT,bundle,cfg)
            self.assertEqual(path.read_bytes(),original)
            self.assertEqual(len(refused_workers(bundle)),2)
            for worker in refused_workers(bundle):
                with closing(WorkerStore(worker,readonly=True)) as store:
                    self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],0)
                    self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM allocations").fetchone()[0],1)

    def test_stage_transfer_counts_every_assigned_second_once_without_release(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle, cfg = Path(directory)/"bundle", config()
            worker_paths(bundle,"hardware")[0].parent.mkdir(parents=True)
            for i,path in enumerate(worker_paths(bundle,"hardware")):
                with closing(WorkerStore(path)) as store:
                    store.allocation_started(f"kaggle-t4-slot-{i}","development",budget=CourseBudget(**cfg["budget"]),
                        started_at=cfg["allocated_at"],billing=dict(provider="kaggle",
                            provider_assignment_at=cfg["allocated_at"],physical_gpu_uuid=f"fixture-{i}"))
            with patch("scripts.course_kaggle_workflow.utc_now",return_value="2026-10-12T09:10:00+00:00"):
                moved=transfer_assignment(bundle,"hardware","development",cfg)
                budget=accepted_budget(bundle,cfg["budget"])
            self.assertFalse(moved["provider_release_confirmed"])
            self.assertTrue(current_assignment(bundle,"development",cfg,("fixture-0","fixture-1")))
            run=dict(budget=asdict(budget),settings=SETTINGS)
            actual=snapshot(ROOT,bundle,"development",run,now="2026-10-12T09:20:00+00:00")
            self.assertAlmostEqual(actual["resources"]["course_gpu_hours"][1],2*20/60)
            worlds,scheduled=scope(ROOT,bundle,"development")
            for path in worker_paths(bundle,"development"):
                with closing(WorkerStore(path)) as store:
                    store.bind_run(worlds,scheduled,SETTINGS,
                        dict(timeout_seconds=120.,termination_seconds=1.,heartbeat_seconds=1.),budget=budget,regime="course")
            with patch("scripts.course_kaggle_workflow.utc_now",return_value="2026-10-12T09:20:00+00:00"):
                transfer_assignment(bundle,"development","main",cfg,budget=budget)
            actual=snapshot(ROOT,bundle,"main",run,now="2026-10-12T09:30:00+00:00")
            self.assertAlmostEqual(actual["resources"]["course_gpu_hours"][1],1)
            self.assertEqual(actual["resources"]["active_devices"],["kaggle-t4-slot-0","kaggle-t4-slot-1"])
            for path in worker_paths(bundle,"development"):
                with closing(WorkerStore(path,readonly=True)) as store:
                    row=store.connection.execute("SELECT * FROM allocations").fetchone()
                    self.assertFalse(json.loads(row["billing_json"])["provider_release_confirmed"])
                    self.assertIn("stage transfer",row["stop_reason"])
            with self.assertRaises(BudgetStop):
                current_assignment(bundle,"main",dict(cfg,allocated_at="different"))

    def test_scheduler_reuses_only_matching_open_assignment_and_keeps_it_chargeable(self):
        world=course_inputs()[0].development[0]
        selected=tuple(b for b in branches(world) if b.phase in ("prefix","control"))
        cfg=config()
        cfg["allocated_at"]=(datetime.now(timezone.utc)-timedelta(seconds=20)).isoformat()
        budget=CourseBudget(**cfg["budget"])
        with tempfile.TemporaryDirectory() as directory:
            paths=[Path(directory)/f"worker-{i}.sqlite" for i in range(2)]
            specs=[]
            for i,path in enumerate(paths):
                billing=dict(provider="kaggle",provider_assignment_at=cfg["allocated_at"],physical_gpu_uuid=f"fixture-{i}")
                with DurableRunner(path,None) as runner:
                    store=runner.store
                    store.bind_run((world,),selected,SETTINGS,dict(timeout_seconds=120.,termination_seconds=1.,heartbeat_seconds=1.),
                        budget=budget,regime="course")
                    store.allocation_started(f"kaggle-t4-slot-{i}","development",budget=budget,
                        started_at=cfg["allocated_at"],billing=billing)
                specs.append(WorkerSpec(path,provider_factory,allocated_device=f"kaggle-t4-slot-{i}",
                    allocated_at=cfg["allocated_at"],provider_billing=billing,continuing_assignment=True))
            scheduler=LocalScheduler(specs,(world,),selected,tokenizer_factory,settings=SETTINGS,
                budget=budget,release_device=lambda *unused:False,regime="course")
            scheduler._allocate()  # No worker/provider/model is launched.
            self.assertEqual(scheduler.allocations,{0:1,1:1})
            with self.assertRaises(WorkerInterrupted): scheduler.close()
            resumed=LocalScheduler(specs,(world,),selected,tokenizer_factory,settings=SETTINGS,
                budget=budget,release_device=lambda *unused:False,regime="course")
            resumed._allocate()
            self.assertEqual(resumed.allocations,{0:1,1:1})
            with self.assertRaises(WorkerInterrupted): resumed.close()
            for path in paths:
                with closing(WorkerStore(path,readonly=True)) as store:
                    self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM allocations").fetchone()[0],1)
                    self.assertIsNone(store.connection.execute("SELECT stopped_at FROM allocations").fetchone()[0])
                    self.assertEqual(store.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],0)

    def exercise(self, *, memory_passed=True, capability_passed=True, inference_stop=None):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory)/"bundle"; (bundle/"hardware").mkdir(parents=True)
            (bundle/"hardware/report.json").write_text("{}")
            cfg=config(); order=[]
            run=dict(budget=cfg["budget"],settings=SETTINGS,freeze=None)
            def execute(root,bundle,cfg,stage):
                order.append(stage)
                return dict(counts=dict(finished_logical={"capability":90,"pilot":1178,"main":6280}[stage],
                    remaining_logical=0),stop_reason=inference_stop)
            def freeze(root,bundle,cfg):
                order.append("freeze"); run["freeze"]=dict(at="CPU fixture")
                (bundle/"run.json").write_text(json.dumps(run))
                return run["freeze"]
            def analyze(*unused):
                order.append("analysis")
                return dict(status="model_complete" if capability_passed and memory_passed and not inference_stop else "feasibility",
                    coverage=dict(recorded=0,unknown=6280))
            resources=dict(admission_available=True,remaining_ceiling_gpu_hours=30,
                           remaining_reserves_gpu_hours=dict(development=8))
            with patch("scripts.course_kaggle_workflow.session_window",return_value=3600), \
                 patch("scripts.course_kaggle_workflow.hardware_gate",return_value=dict(passed=memory_passed,accounting_segment_closed=True)), \
                 patch("scripts.course_kaggle_workflow.bind_candidate",return_value=run), \
                 patch("scripts.course_kaggle_workflow.start_assignment"), \
                 patch("scripts.course_kaggle_workflow.current_assignment",return_value=False), \
                 patch("scripts.course_kaggle_workflow.capability_gate",side_effect=[
                     dict(status="incomplete",passed=False),dict(status="passed" if capability_passed else "failed",passed=capability_passed)]), \
                 patch("scripts.course_kaggle_workflow.execute",side_effect=execute), \
                 patch("scripts.course_kaggle_workflow.freeze",side_effect=freeze), \
                 patch("scripts.course_kaggle_workflow.analyze",side_effect=analyze), \
                 patch("scripts.course_kaggle_workflow.snapshot",return_value=dict(resources=resources)), \
                 patch("scripts.course_kaggle_workflow.smoke_resources",return_value=dict(resources,remaining_smoke_gpu_hours=.5)), \
                 patch("scripts.course_kaggle_workflow.backup_bundle"), \
                 patch("scripts.course_kaggle_workflow.record_refused_allocation"),redirect_stdout(io.StringIO()):
                result=run_all(ROOT,bundle,cfg)
            return order,result

    def test_automatic_order_freezes_before_main_and_always_finishes_analysis(self):
        order,result=self.exercise()
        self.assertEqual(order,["capability","pilot","freeze","main","analysis"])
        self.assertEqual(result["status"],"complete_results")
        self.assertFalse(result["provider_release_confirmed"])

    def test_memory_capability_and_attempt_failures_never_advance_to_main(self):
        for kwargs in (dict(memory_passed=False),dict(capability_passed=False),dict(inference_stop="recorded headroom failure")):
            order,result=self.exercise(**kwargs)
            self.assertEqual(order[-1],"analysis")
            self.assertNotIn("main",order)
            self.assertNotIn("freeze",order)
            self.assertEqual(result["status"],"limited_result")
            self.assertFalse(result["gates_bypassed"])

    def test_range_download_resumes_and_rejects_server_drift_using_native_hash(self):
        raw=b"CPU fixture, not weights"
        class Response(io.BytesIO):
            status=206
            def __init__(self,offset,end):
                super().__init__(raw[offset:end+1]); self.headers={"Content-Range":f"bytes {offset}-{end}/{len(raw)}"}
        def request(req,**kwargs):
            a,b=map(int,req.get_header("Range").split("=")[1].split("-"))
            return Response(a,b)
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/"native.bin"
            target.with_suffix(".bin.partial").write_bytes(raw[:4])
            with patch("urllib.request.urlopen",side_effect=request):
                download_native_ranges("https://example.invalid/native",target,len(raw),hashlib.sha256(raw).hexdigest(),chunk_bytes=5)
            self.assertEqual(target.read_bytes(),raw)
            response=Response(0,4); response.headers["Content-Range"]="foreign"
            with patch("urllib.request.urlopen",return_value=response),self.assertRaises(ValueError):
                download_native_ranges("https://example.invalid/native",Path(directory)/"foreign.bin",len(raw),"0"*64,chunk_bytes=5)


if __name__=="__main__":
    unittest.main()
