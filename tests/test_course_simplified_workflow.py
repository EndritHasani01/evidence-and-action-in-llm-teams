"""User-approved automatic acceptance/observations, with no GPU execution."""

from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from recovery.accounting import CourseBudget, MonitoringCourseBudget, course_admission
from recovery.runner import DurableRunner
from scripts.course_kaggle_workflow import hardware_gate, MIN_HEADROOM, end_observations
from scripts.m5_course_smoke import CANDIDATE, admission
from scripts.build_course_kaggle import notebook
from scripts.m5_kaggle_preflight import utc
from recovery.workers import LocalScheduler, WorkerSpec
from tests.course_worker_cases import SETTINGS, branches, course_inputs, provider_factory, tokenizer_factory

ROOT=Path(__file__).resolve().parents[1]


class SimplifiedWorkflowTests(unittest.TestCase):
    def test_scheduler_admits_unknown_history_and_reuses_the_observed_open_interval(self):
        world=course_inputs()[0].development[0]
        selected=tuple(b for b in branches(world) if b.phase in ("prefix","control"))
        budget=MonitoringCourseBudget(); at=utc()
        with tempfile.TemporaryDirectory() as directory:
            specs=[]
            for index in range(2):
                path=Path(directory)/f"worker-{index}.sqlite"
                billing=dict(provider="kaggle",provider_assignment_at=at,physical_gpu_uuid=f"fixture-{index}",
                    measurement_scope="observed_notebook_interval")
                with DurableRunner(path,None) as runner:
                    runner.store.bind_run((world,),selected,SETTINGS,
                        dict(timeout_seconds=120.,termination_seconds=1.,heartbeat_seconds=1.),budget=budget,regime="course")
                    runner.store.allocation_started(f"kaggle-t4-slot-{index}","development",budget=budget,started_at=at,billing=billing)
                specs.append(WorkerSpec(path,provider_factory,allocated_device=f"kaggle-t4-slot-{index}",
                    allocated_at=at,provider_billing=billing,continuing_assignment=True))
            scheduler=LocalScheduler(specs,(world,),selected,tokenizer_factory,settings=SETTINGS,
                budget=budget,release_device=lambda *unused:False,regime="course")
            scheduler._allocate()  # Exercise actual accounting/admission; no worker or CUDA process.
            self.assertIsNone(scheduler.stop_reason)
            self.assertEqual(scheduler.allocations,{0:1,1:1})
            self.assertFalse(scheduler.progress()["resources"]["admission_available"])

    def test_observation_policy_does_not_invent_historical_cost_or_change_legacy_binding(self):
        ordinary=CourseBudget(); monitored=MonitoringCourseBudget()
        self.assertEqual(asdict(ordinary),asdict(monitored))
        unknown=dict(admission_available=False,admission_reason="prior_interval_unknown")
        self.assertEqual(course_admission(unknown,{},ordinary,"main",2),("prior_interval_unknown",0))
        reason,seconds=course_admission(unknown,{},monitored,"main",2)
        self.assertIsNone(reason); self.assertGreater(seconds,0)
        self.assertIsNone(monitored.prior_development_gpu_hours)
        launch=dict(resource_policy="observe",budget=asdict(monitored),authorization="CPU fixture only",
            allocated_at=utc(),session_limit_seconds=3600)
        resources,wall=admission(launch,next_attempt=True)
        self.assertGreater(wall,3000)
        self.assertFalse(resources["admission_available"])

    def test_observation_end_is_not_provider_release_and_unknown_gap_is_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory); path=bundle/"main/worker-0.sqlite"; path.parent.mkdir()
            with DurableRunner(path,None) as runner:
                number=runner.store.allocation_started("kaggle-t4-slot-0","main",budget=MonitoringCourseBudget(),
                    started_at="2026-10-12T09:00:00+00:00",billing=dict(measurement_scope="observed_notebook_interval",
                        provider_assignment_at="2026-10-12T09:00:00+00:00"))
                runner.store.allocation_observation_ended(number,at="2026-10-12T09:15:00+00:00",reason="CPU fixture observation")
                row=runner.store.connection.execute("SELECT * FROM allocations").fetchone()
                billing=json.loads(row["billing_json"])
                self.assertFalse(billing["provider_release_confirmed"])
                self.assertEqual(billing["unobserved_provider_time"],"unknown")
                self.assertEqual(row["stopped_at"],"2026-10-12T09:15:00+00:00")
            end_observations(bundle)  # Closed observations are idempotent.

    def test_measured_hardware_acceptance_still_requires_complete_probes_cache_and_headroom(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory); (bundle/"hardware").mkdir()
            (bundle/"hardware/report.json").write_text(json.dumps(dict(root_blocker=None,smoke=dict(stop_reason=None))))
            (bundle/"hardware/host-checks.json").write_text(json.dumps(dict(tests=3,skipped=0)))
            free=[MIN_HEADROOM]; probe_count=[2]
            class Rows(list):
                def fetchone(self): return self[0]
                def fetchall(self): return self
            class Connection:
                def __init__(self,index): self.index=index
                def execute(self,sql):
                    if "FROM allocations" in sql:
                        return Rows([dict(stopped_at="2026-10-12T09:01:00+00:00",billing_json=json.dumps(dict(measurement_scope="observed_notebook_interval")))])
                    if "COUNT(*)" in sql: return Rows([(0,)])
                    if "FROM provider_processes" in sql:
                        return Rows([(json.dumps(dict(model=CANDIDATE.model,revision=CANDIDATE.revision,candidate_attention=[1,2,3])),)])
                    if "FROM attempts" in sql:
                        facts=dict(cache=dict(initial_empty=True,same_call_cache=True),finite_score_steps=256,
                            observed_model_edge_memory=[dict(total_bytes=16*1024**3,free_bytes=free[0])])
                        rows=[dict(status="completed",backend_json=json.dumps(facts)) for _ in range(11 if self.index==0 else 10)]
                        if self.index < probe_count[0]:
                            rows.append(dict(status="completed",backend_json=json.dumps(dict(facts,hardware_diagnostic=True,
                                input_tokens=109851,forced_output_tokens=256))))
                        return Rows(rows)
                    raise AssertionError(sql)
            class Store:
                def __init__(self,path,**kwargs): self.connection=Connection(int(path.stem[-1]))
                def close(self): pass
            with patch("scripts.course_kaggle_workflow.WorkerStore",Store):
                measured=hardware_gate(bundle,dict(acceptance="measured_stress"))
                self.assertTrue(measured["passed"])
                self.assertFalse(measured["provider_release_confirmed"])
                self.assertIsNone(measured["complete_live_memory_upper_bound_bytes"])
                self.assertFalse(hardware_gate(bundle,{})["passed"])
                free[0]-=1
                self.assertFalse(hardware_gate(bundle,dict(acceptance="measured_stress"))["passed"])
                free[0]+=1; probe_count[0]=1
                self.assertFalse(hardware_gate(bundle,dict(acceptance="measured_stress"))["passed"])

    def test_gpu_setup_is_automatic_and_no_historical_zero_is_inserted(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle=Path(directory); source=bundle/"source"; (source/"configs").mkdir(parents=True)
            (source/"configs/course-kaggle.json").write_bytes((ROOT/"configs/course-kaggle.json").read_bytes())
            document=notebook("a"*64,"b"*40)
            values={"bundle":bundle,"source":source,"SOURCE_READY":True,"json":json}
            is_dir=Path.is_dir; iterdir=Path.iterdir
            def gpu_dir(path): return True if path.as_posix()=="/proc/driver/nvidia/gpus" else is_dir(path)
            def gpu_files(path): return iter([Path("fixture-0"),Path("fixture-1")]) if path.as_posix()=="/proc/driver/nvidia/gpus" else iterdir(path)
            with patch.object(Path,"is_dir",gpu_dir),patch.object(Path,"iterdir",gpu_files):
                for name in ("action","configuration"):
                    cell=next(c for c in document["cells"] if c["id"]==name)
                    exec("".join(cell["source"]),values)
            self.assertTrue(values["CONFIG"]["execute_gpu"])
            self.assertTrue(all(values["CONFIG"]["authorizations"].values()))
            self.assertEqual(values["CONFIG"]["resource_policy"],"observe")
            self.assertIsNone(values["CONFIG"]["budget"]["prior_setup_gpu_hours"])
            self.assertEqual(values["CONFIG"]["hardware_review"],dict(acceptance="measured_stress"))


if __name__=="__main__": unittest.main()
