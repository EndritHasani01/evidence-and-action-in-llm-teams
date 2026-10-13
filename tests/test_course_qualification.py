"""Fixed repair qualification and exact compact request integration; CPU only."""

from contextlib import closing, redirect_stdout
from dataclasses import asdict
import gzip
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from recovery.inference import course_candidate, candidate_settings, TokenizerFactory, QWEN_9B
from recovery.prompts import COURSE_LIMITS, COMPACT_PROFILE, DATA_MARKER, render_request
from recovery.protocol import GeneratedReply
from recovery.runner import DurableRunner
from recovery.storage import WorkerStore
from scripts.course_kaggle_bootstrap import qualification_choice
from scripts.course_kaggle_workflow import all_workers, backup_bundle, save, run_qualification
from scripts.m5_course_preparation import preparation_files, read, peer_view
from scripts.m5_course_smoke import check_hardware_plan, admission
from scripts.m5_kaggle_preflight import smoke_attempt_limit, utc
from tests.course_worker_cases import TOKENIZER, SETTINGS, sort_world, prefix_branch

ROOT = Path(__file__).resolve().parents[1]


def scripted_hardware_reply(view, rendered, tokenized, *, seed, settings):
    return GeneratedReply("{}",(91,93),"eos",False)


class ScriptedHardwareFactory:
    def __init__(self,device,*args):
        self.device = device

    def __call__(self):
        return scripted_hardware_reply


class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.metadata = Path(cls.directory.name)
        with zipfile.ZipFile(ROOT/"notebooks/run/final-online-4/course-resume.payload") as archive:
            for name in archive.namelist():
                if name.startswith("source/metadata/4B/"):
                    (cls.metadata/Path(name).name).write_bytes(archive.read(name))
        cls.tokenizer = TokenizerFactory(course_candidate("9B"),str(cls.metadata),COURSE_LIMITS)()

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_both_actual_native_plans_and_generation_contracts(self):
        from tests.generation_checks import check_generation_contract
        for label in ("9B","4B"):
            candidate = course_candidate(label)
            packet = read(preparation_files(ROOT,candidate)["packet"])
            result = check_hardware_plan(ROOT,packet,self.tokenizer)
            self.assertEqual(result["constructors_checked"],24)
            self.assertEqual(packet["complete_input_tokens_upper"],110416)
            self.assertEqual(packet["settings"]["prompt_profile"],COMPACT_PROFILE)
            generation = check_generation_contract(self.tokenizer,packet["settings"])
            self.assertEqual(generation["checks"]["diagnostic"]["effective_eos"],[])
            self.assertEqual(packet["settings"]["generation"]["max_new_tokens"],256)
        with self.assertRaises(ValueError):
            candidate_settings(self.tokenizer,QWEN_9B,limits=COURSE_LIMITS)

    def test_new_instruction_preserves_every_permitted_data_byte(self):
        packet = read(preparation_files(ROOT,course_candidate("9B"))["packet"])
        for row in packet["requests"]:
            view = peer_view(row["view"])
            original = render_request(view,limits=COURSE_LIMITS).content
            compact = render_request(view,limits=COURSE_LIMITS,profile=COMPACT_PROFILE).content
            self.assertEqual(original.split(DATA_MARKER,1)[1],compact.split(DATA_MARKER,1)[1])
            self.assertIn("compact single-line JSON",compact)

    def test_compact_durable_rounds_resume_without_provider_and_reject_profile_drift(self):
        world = sort_world(); branch = prefix_branch(world)
        settings = dict(SETTINGS,prompt_profile=COMPACT_PROFILE)
        seen = []
        def provide(view,rendered,tokens,**kwargs):
            self.assertEqual(rendered,render_request(view,limits=COURSE_LIMITS,profile=COMPACT_PROFILE))
            seen.append((view.slot,view.peer))
            text = '{"candidate":[0,0,0,0,0,0],"send":[]}'
            return GeneratedReply(text,tuple(TOKENIZER.encode(text,add_special_tokens=False)),"eos",False)
        def forbidden(*args,**kwargs):
            raise AssertionError("saved calls must not invoke a provider")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"worker.sqlite"
            with DurableRunner(path,TOKENIZER,provide,scripted=True) as runner:
                runner.start(world,branch,settings=settings)
                for number in range(1,5):
                    runner.run_round(branch.branch_id,number)
                saved = [dict(r) for r in runner.store.connection.execute("SELECT * FROM calls")]
            self.assertEqual(len(seen),16)
            with DurableRunner(path,TOKENIZER,forbidden,scripted=True) as runner:
                runner.start(world,branch,settings=settings)
                runner.run_round(branch.branch_id,4)
                self.assertEqual(saved,[dict(r) for r in runner.store.connection.execute("SELECT * FROM calls")])
                with self.assertRaises(ValueError):
                    runner.start(world,branch,settings=SETTINGS)

    def choice(self,root,reason,*,capability=None,pilot=None,freeze=None):
        child = root/"candidates/9B"
        save(child/"automatic-run.json",dict(status="limited_result",reason=reason))
        if capability: save(child/"capability-gate.json",capability)
        if pilot: save(child/"pilot-gate.json",pilot)
        if freeze: save(child/"run.json",dict(freeze=freeze))
        return qualification_choice(root,dict(candidate_order=["9B","4B"]))

    def test_incomplete_capability_audit_defect_and_frozen_run_cannot_fall_back(self):
        cases = [("first_90_capability_gate_not_passed",dict(capability=dict(status="incomplete"))),
                 ("complete_pilot_acceptance_not_passed",dict(pilot=dict(complete=True,audit=dict(passed=False)))),
                 ("recorded_model_attempt_failure",dict(freeze=dict(accepted=True))),
                 ("BudgetStop: allocation_deadline",{})]
        for reason,kwargs in cases:
            with tempfile.TemporaryDirectory() as directory:
                self.assertEqual(self.choice(Path(directory),reason,**kwargs),("9B",23))

    def test_complete_quality_failure_selects_only_declared_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.choice(Path(directory),"first_90_capability_gate_not_passed",
                             capability=dict(status="failed")),("4B",23))

    def test_nested_canonical_workers_receive_real_sqlite_backups(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/"bundle"
            paths = [root/"candidates"/label/"hardware/worker-0.sqlite" for label in ("9B","4B")]
            for path in paths:
                path.parent.mkdir(parents=True)
                with closing(WorkerStore(path)) as store:
                    with store.connection:
                        store.connection.execute("INSERT INTO run_inputs VALUES (1,?)",(json.dumps({"CPU-candidate":path.parts[-3]}),))
            self.assertEqual(set(all_workers(root)),set(paths))
            result = backup_bundle(root,Path(directory)/"resume.payload")
            self.assertEqual(result["canonical_workers"],2)
            with zipfile.ZipFile(result["path"]) as archive:
                for path in paths:
                    restored = Path(directory)/(path.parts[-3]+".sqlite")
                    restored.write_bytes(archive.read(path.relative_to(root).as_posix()))
                    with closing(sqlite3.connect(restored)) as db:
                        self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0],"ok")
                        self.assertEqual(json.loads(db.execute("SELECT inputs_json FROM run_inputs").fetchone()[0]),
                                         {"CPU-candidate":path.parts[-3]})

    def test_adopted_allowance_does_not_reset_history(self):
        launch = dict(smoke_attempt_limit=71,smoke_attempt_allowance="final-online-4/qualification",
                      budget=dict(prior_smoke_attempts=23))
        self.assertEqual(smoke_attempt_limit(launch),71)
        launch["budget"]["prior_smoke_attempts"] = 22
        with self.assertRaises(ValueError): smoke_attempt_limit(launch)
        with tempfile.TemporaryDirectory() as directory:
            cfg = dict(candidate_order=["9B","4B"],budget=dict(prior_smoke_attempts=30))
            self.assertEqual(qualification_choice(Path(directory),cfg),("9B",30))
            cfg["budget"]["prior_smoke_attempts"] = 22
            with self.assertRaises(ValueError): qualification_choice(Path(directory),cfg)

    def test_9b_worker_binding_requires_reviewed_profile_and_exact_revision(self):
        from recovery.accounting import MonitoringCourseBudget
        world = sort_world(); branch = prefix_branch(world)
        settings = candidate_settings(self.tokenizer,course_candidate("9B"),limits=COURSE_LIMITS)
        budget = MonitoringCourseBudget(**read(ROOT/"configs/course-kaggle.json")["budget"])
        with tempfile.TemporaryDirectory() as directory, closing(WorkerStore(Path(directory)/"worker.sqlite")) as store:
            store.bind_run((world,),(branch,),settings,dict(timeout_seconds=120),budget=budget,regime="course")
            bad = dict(settings,prompt_profile="original")
            with self.assertRaises(ValueError):
                store.bind_run((world,),(branch,),bad,dict(timeout_seconds=120),budget=budget,regime="course")

    def test_actual_24_row_controller_binds_new_9b_settings_and_hardware_deadline(self):
        from recovery.attempts import ProcessProvider
        from scripts.m5_course_smoke import execute_requests
        packet = read(preparation_files(ROOT,course_candidate("9B"))["packet"])
        config = read(ROOT/"configs/course-kaggle.json")
        launch = dict(config,allocated_at=utc(),provider="kaggle",continuous_assignment=True,
            session_limit_seconds=36000,resource_policy="observe",resume_workers=[],
            authorization="CPU scripted check only; no model/GPU")
        deadlines = []
        def provider(factory,**kwargs):
            deadlines.append(kwargs.get("timeout_seconds",120))
            # Deliberately replace the physical provider and deadline only in
            # this CPU fixture. Verify the real caller requests 600 for probes.
            return ProcessProvider(factory,timeout_seconds=5,termination_seconds=1,
                                   before_attempt=kwargs.get("before_attempt"))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch("scripts.m5_course_smoke.host_checks",return_value=dict(tests=3,skipped=0)), \
                 patch("scripts.m5_course_smoke.EnvelopeFactory",ScriptedHardwareFactory), \
                 patch("scripts.m5_course_smoke.ProcessProvider",provider),redirect_stdout(io.StringIO()):
                result = execute_requests(ROOT,packet,launch,["CPU-0","CPU-1"],output,
                    tokenizer=self.tokenizer,factory=ScriptedHardwareFactory,complete_envelope=True)
            self.assertIsNone(result["stop_reason"])
            self.assertEqual(deadlines.count(600),2)
            self.assertEqual(result["resources"]["smoke_attempt_usage"]["total_recorded"],47)
            self.assertEqual(result["complete_resident_tokens_upper"],110672)
            for path in output.glob("worker-?.sqlite"):
                with closing(WorkerStore(path,readonly=True)) as store:
                    self.assertEqual(store.run_inputs["settings"]["model"],"Qwen/Qwen3.5-9B")
            paths = list(output.glob("worker-?.sqlite"))
            with self.assertRaisesRegex(Exception,"fixed_candidate_24_attempt_limit"):
                admission(dict(launch,resume_workers=paths),next_attempt=True)

    def test_wrapper_runs_only_fixed_fallback_and_resumes_selected_bundle(self):
        import scripts.course_kaggle_workflow as workflow
        config = read(ROOT/"configs/course-kaggle.json")
        config.update(execute_gpu=True,resource_policy="observe")
        called = []
        def run(root,child,selected):
            label = selected["candidate"]; called.append(label)
            result = dict(status="limited_result",reason="first_90_capability_gate_not_passed" if label=="9B" else "CPU fixture stop",
                          analysis=None,gates_bypassed=False)
            if label=="9B": save(child/"capability-gate.json",dict(status="failed"))
            save(child/"automatic-run.json",result)
            return result
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)/"bundle"
            for label in ("9B","4B"):
                candidate = course_candidate(label)
                save(bundle/"candidates"/label/"asset-receipt.json",dict(model=candidate.model,revision=candidate.revision))
            with patch.object(workflow,"run_all",run),patch.object(workflow,"CANDIDATE",workflow.CANDIDATE),redirect_stdout(io.StringIO()):
                result = run_qualification(ROOT,bundle,config)
                self.assertEqual(called,["9B","4B"])
                self.assertEqual(result["selected_candidate"],"4B")
                called.clear()
                result = run_qualification(ROOT,bundle,config)
                self.assertEqual(called,["4B"])
                self.assertFalse(result["gates_bypassed"])


if __name__ == "__main__":
    unittest.main()
