"""Bounded course smoke using existing worker/attempt/allocation records.

Importing this module performs no CUDA initialization, loading or download.
GPU execution requires an explicit launch record and admitted resource bounds.
"""

import argparse
from contextlib import ExitStack
from dataclasses import asdict, dataclass, replace
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from time import sleep

# -I direct-script execution uses installed recovery, plus source-only scripts.
if not __package__:
    import types
    namespace = types.ModuleType("scripts")
    namespace.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules.setdefault("scripts", namespace)
    test_namespace = types.ModuleType("tests")
    test_namespace.__path__ = [str(Path(__file__).resolve().parents[1]/"tests")]
    sys.modules.setdefault("tests",test_namespace)

from recovery.accounting import CourseBudget, BudgetStop, _course_resources, course_admission, timestamp
from recovery.attempts import ProcessProvider, MeasuredReply
from recovery.costs import _allocation_resources
from recovery.inference import ModelFactory, QWEN_4B, TokenizerFactory
from recovery.prompts import COURSE_LIMITS, RenderedRequest, TokenizedRequest
from recovery.protocol import failed_reply, validate_reply
from recovery.schedule import Branch, CallSlot
from recovery.storage import WorkerStore, RecordedFailure, record_json, settings_json
from recovery.tasks import Task
from recovery.t4_attention import T4_ATTENTION
from recovery.workers import _own_file
from scripts.m5_course_preparation import peer_view, read, verify_requests
from scripts.m5_kaggle_preflight import export_evidence, save_json, utc

CANDIDATE = replace(QWEN_4B, attention=T4_ATTENTION)
EXPORT_SECONDS = 15


def launch_defaults():
    return dict(execute_gpu=False, stage_weights=False, authorization="", provider="kaggle",
        reported_quota_gpu_hours=30, prior_sessions_released=True,
        allocated_at=None, provider_session_seconds=None, release_instructions="",
        budget=asdict(CourseBudget(shutdown_seconds=120)), hf_cache=None,
        assets_receipt=None, source_manifest=None, resume_workers=[])


def smoke_branch(row):
    call = CallSlot(row["smoke_call_id"], 1, row["view"]["peer"], row["seed"], None)
    return Branch(row["development_world_id"], Task(row["view"]["task"]), "smoke",
        row["smoke_call_id"].rsplit("/", 1)[1], None, 0, None, (call,))


def resources(stores, budget, now):
    rows = {name:[] for name in ("allocations", "attempts", "provider_processes")}
    for index, store in enumerate(stores):
        for table in rows:
            rows[table].extend(dict(row, worker=index) for row in store.connection.execute("SELECT * FROM "+table))
    result = _allocation_resources(rows["allocations"], rows["attempts"], rows["provider_processes"], now, budget)
    _course_resources(result, budget)
    allocated = sum(d["allocated_seconds"]/3600 for d in result["devices"]
        if json.loads(d["billing_json"] or "{}").get("unadmitted_action", "hardware") == "hardware")
    if result["remaining_smoke_gpu_hours"] is not None:
        result["remaining_smoke_gpu_hours"] = max(0, result["remaining_smoke_gpu_hours"]-allocated)
    if result["remaining_smoke_attempts"] is not None:
        result["remaining_smoke_attempts"] = max(0, result["remaining_smoke_attempts"]-len(rows["attempts"]))
    return result


def admission(launch, stores=(), *, now=None, next_attempt=False):
    """No available quota, per-account reset or successful output replaces usage evidence."""
    now = now or utc()
    budget = CourseBudget(**launch["budget"])
    if budget.allocation_mode != "gpu" or budget.shutdown_seconds < 120:
        raise ValueError("actual GPU charging and at least 120 seconds for release required")
    if launch.get("authorization", "").strip() == "":
        raise BudgetStop("concrete_course_smoke_authorization_missing")
    if launch.get("prior_sessions_released") is not True:
        raise BudgetStop("prior_provider_release_unconfirmed")
    extra_paths = launch.get("prior_allocation_workers", [])
    if extra_paths:
        with ExitStack() as stack:
            extra = [WorkerStore(Path(p), readonly=True) for p in extra_paths]
            for store in extra:
                stack.callback(store.close)
            resumed = []
            if not stores and launch.get("resume_workers"):
                resumed = [WorkerStore(Path(p),readonly=True) for p in launch["resume_workers"]]
                for store in resumed:
                    stack.callback(store.close)
            current = resources((*stores,*resumed,*extra),budget,now)
    elif not stores and launch.get("resume_workers"):
        resumed = []
        try:
            for path in launch["resume_workers"]:
                resumed.append(WorkerStore(Path(path),readonly=True))
            current = resources(resumed,budget,now)
        finally:
            for store in resumed:
                store.close()
    else:
        current = resources(stores, budget, now)
    if any(device["stopped_at"] is None and device["started_at"] != launch.get("allocated_at")
           for device in current["devices"]):
        raise BudgetStop("previous_worker_allocation_release_unconfirmed")
    reason, allowed_seconds = course_admission(current, dict(available=False), budget, "development", 2)
    if reason:
        raise BudgetStop(reason)
    quota, duration = launch.get("reported_quota_gpu_hours"), launch.get("provider_session_seconds")
    if (type(quota) not in (int, float) or quota <= 0 or type(duration) not in (int, float)
            or duration <= 0 or not launch.get("release_instructions", "").strip()):
        raise BudgetStop("provider_quota_duration_or_release_terms_missing")
    if not launch.get("allocated_at"):
        raise BudgetStop("provider_assignment_clock_missing")
    elapsed = timestamp(now)-timestamp(launch["allocated_at"])
    if elapsed < 0:
        raise ValueError("provider assignment cannot be in the future")
    # Before creating ledgers, the already-assigned interval is still chargeable.
    assignment_recorded = any(device["stopped_at"] is None and device["started_at"] == launch["allocated_at"]
                              for device in current["devices"])
    if not assignment_recorded:
        allowed_seconds -= 2*elapsed
        smoke_seconds = current["remaining_smoke_gpu_hours"]*3600-2*elapsed
    else:
        smoke_seconds = current["remaining_smoke_gpu_hours"]*3600
    remaining_wall = min(allowed_seconds/2, smoke_seconds/2, quota*3600/2, duration-elapsed)
    reserve = budget.shutdown_seconds + EXPORT_SECONDS
    if next_attempt:
        reserve += 124  # Loading/response, TERM/KILL and bounded pipe cleanup; retry is re-admitted.
        if current["remaining_smoke_attempts"] < 1:
            raise BudgetStop("cumulative_smoke_attempt_limit")
    if remaining_wall <= reserve:
        raise BudgetStop("insufficient_smoke_time_for_attempt_export_and_release")
    return current, remaining_wall


def memory_sample(torch):
    free, total = torch.cuda.mem_get_info(0)
    return dict(free_bytes=free,total_bytes=total,allocated_bytes=torch.cuda.memory_allocated(0),
        reserved_bytes=torch.cuda.memory_reserved(0),peak_reserved_bytes=torch.cuda.max_memory_reserved(0),
        peak_allocated_bytes=torch.cuda.max_memory_allocated(0))


def candidate_attention(torch):
    """Three affected zero-stride/mask/chunk shapes, not another generic R8 screen."""
    from types import SimpleNamespace
    from recovery.t4_attention import grouped_inputs, t4_sdpa_forward
    module = SimpleNamespace(training=False,num_key_value_groups=4,is_causal=True)
    cases = []
    generator = torch.Generator(device="cuda:0").manual_seed(741)
    for query_length, key_length in ((256,256),(256,512),(1,513)):
        query = torch.randn(1,query_length,16,256,device="cuda:0",dtype=torch.float16,generator=generator).transpose(1,2)
        key = torch.randn(1,key_length,4,256,device="cuda:0",dtype=torch.float16,generator=generator).transpose(1,2)
        value = torch.randn(1,key_length,4,256,device="cuda:0",dtype=torch.float16,generator=generator).transpose(1,2)
        mask = None
        if query_length > 1:
            mask = (torch.arange(key_length,device="cuda:0")[None,:] <=
                    torch.arange(key_length-query_length,key_length,device="cuda:0")[:,None])[None,None]
        _, grouped_key, grouped_value, _ = grouped_inputs(query,key,value,mask)
        assert grouped_key.stride(1) == grouped_value.stride(1) == 0
        assert grouped_key.untyped_storage().data_ptr() == key.untyped_storage().data_ptr()
        assert grouped_value.untyped_storage().data_ptr() == value.untyped_storage().data_ptr()
        if not cases:
            with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as profile:
                actual,_ = t4_sdpa_forward(module,query,key,value,mask)
                torch.cuda.synchronize(0)
            operators = sorted({event.key for event in profile.key_averages()})
            kernels = sorted({event.name for event in profile.events() if event.device_type == torch.autograd.DeviceType.CUDA})
            if not kernels or not any("efficient_attention" in name for name in operators):
                raise ValueError("actual candidate efficient-attention CUDA trace missing")
        else:
            actual,_ = t4_sdpa_forward(module,query,key,value,mask)
        weights = query.float() @ key.repeat_interleave(4,dim=1).float().transpose(-2,-1) / 16
        if mask is not None:
            weights = weights.masked_fill(~mask,float("-inf"))
        expected = (weights.softmax(dim=-1) @ value.repeat_interleave(4,dim=1).float()).transpose(1,2)
        torch.testing.assert_close(actual.float(),expected,atol=2e-3,rtol=2e-2)
        assert torch.isfinite(actual).all()
        cases.append(dict(query_tokens=query_length,key_tokens=key_length,finite=True,reference_matches=True,
            kv_storage_alias=True,group_stride=0,forced_backend="EFFICIENT_ATTENTION",
            maximum_absolute_error=(actual.float()-expected).abs().max().item(),atol=2e-3,rtol=2e-2))
        if len(cases) == 1:
            cases[-1].update(profiled_operators=operators,cuda_kernels=kernels)
    return cases


class SmokeBackend:
    def __init__(self, backend):
        self.backend = backend
        inspection = read(Path(__file__).resolve().parents[1]/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
        expected = inspection["language_parameters"]
        actual = dict(backend.model.named_parameters())
        if set(actual) != set(expected):
            raise ValueError("actual language inventory differs from all 426 pinned names")
        for name,tensor in actual.items():
            shape = getattr(getattr(tensor,"quant_state",None),"shape",None) if expected[name]["kind"] == "nf4_linear" else tensor.shape
            if shape is None or list(shape) != expected[name]["shape"]:
                raise ValueError("actual original language tensor shape differs: "+name)
        self.load_report = dict(backend.load_report, candidate_attention=candidate_attention(backend.torch),
            observed_load_memory=memory_sample(backend.torch))

    def __call__(self, *args, **kwargs):
        torch = self.backend.torch
        observations = []
        def observe(*unused):
            observations.append(memory_sample(torch))
        # Model-edge samples complement the adapter's allocator peaks. They
        # do not claim to see every native workspace/context allocation.
        handles = [self.backend.model.register_forward_pre_hook(observe),
                   self.backend.model.register_forward_hook(observe)]
        try:
            reply = self.backend(*args, **kwargs)
            facts = dict(reply.backend,observed_model_edge_memory=observations,
                complete_envelope_memory_accepted=False)
            return MeasuredReply(reply.response,reply.peak_memory_bytes,facts)
        finally:
            for handle in handles:
                handle.remove()


@dataclass(frozen=True)
class SmokeFactory:
    device: str
    def __call__(self):
        return SmokeBackend(ModelFactory(CANDIDATE,self.device,COURSE_LIMITS)())


class EnvelopeBackend(SmokeBackend):
    """Full-length tensor diagnostic; its output is excluded from capability."""

    def __call__(self, view, rendered, tokenized, *, seed, settings):
        if settings_json(settings) != settings_json(self.backend.settings):
            raise ValueError("envelope diagnostic candidate settings differ")
        torch = self.backend.torch
        observations = []
        def observe(*unused):
            observations.append(memory_sample(torch))
        handles = [self.backend.model.register_forward_pre_hook(observe),
                   self.backend.model.register_forward_hook(observe)]
        try:
            reply = self.backend.probe_envelope(tokenized, seed=seed)
            return MeasuredReply(reply.response, reply.peak_memory_bytes,
                dict(reply.backend, observed_model_edge_memory=observations,
                     complete_envelope_memory_accepted=False))
        finally:
            for handle in handles:
                handle.remove()


@dataclass(frozen=True)
class EnvelopeFactory:
    device: str
    def __call__(self):
        return EnvelopeBackend(ModelFactory(CANDIDATE,self.device,COURSE_LIMITS)())


def hardware_plan(packet, tokenizer):
    """Keep 21 native smoke probes, two envelope attempts and one timeout.

    Replaces two redundant worker-one independence probes with separately
    identified diagnostics, within the existing cumulative 24-attempt ceiling.
    Saved scientific pilot requests and settings are never changed.
    """
    rows = deepcopy(packet["requests"])
    token_id = tokenizer.encode("a", add_special_tokens=False)[0]
    ids = [token_id]*109851
    text = tokenizer.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
    for index, worker in ((21, 0), (22, 1)):
        row = rows[index]
        row.update(smoke_call_id=f"course-hardware/envelope/device-{worker}",
            physical_generation_id=f"course-hardware/envelope/device-{worker}",
            intended_worker=worker, confirmed_restart_before=True, hardware_diagnostic=True,
            input_tokens=109851, resident_tokens_with_reserve=110107,
            rendered=dict(system="Hardware memory diagnostic; no scientific scoring", content=text),
            tokenized=dict(text=text, input_ids=ids, attention_mask=[1]*109851))
    return rows


def controlled_hang(*args, **kwargs):
    while True:
        sleep(1)


def hang_factory():
    """Infrastructure-only slot; never describe its timeout as model latency."""
    return controlled_hang


def host_checks(root,launch,stores,output):
    """Affected Linux persistence/cleanup checks; no generic CPU acceptance rerun."""
    import time
    from scripts.m5_kaggle_preflight import command, test_result, EXPORT_SECONDS as COMMAND_EXPORT_SECONDS
    _,wall = admission(launch,stores,next_attempt=True)
    timeout = min(30,int(wall-launch["budget"]["shutdown_seconds"]-COMMAND_EXPORT_SECONDS-8))
    if timeout < 1:
        raise BudgetStop("insufficient_time_for_affected_host_checks")
    record = command(output,"affected-host-checks",[sys.executable,"-I",root/"scripts/m5_course_smoke.py",
        "--root",root,"--launch",output/"launch.json","--output",output/"host-checks.json","--host-checks"],
        deadline=time.monotonic()+wall-launch["budget"]["shutdown_seconds"],timeout=timeout,cwd=output,env=dict(os.environ))
    return test_result(output,record,3)


def execute_requests(root, packet, launch, devices, output, *, tokenizer, factory=SmokeFactory,
                     complete_envelope=False):
    """Serial isolated probes; all raw outcomes remain in the original ledger."""
    from recovery.manifests import load_population
    verify_requests(root,packet)
    rows = hardware_plan(packet, tokenizer) if complete_envelope else packet["requests"]
    branches = tuple(smoke_branch(row) for row in rows)
    save_json(output/"executed-plan.json", dict(rows=rows,
        note="Envelope rows are tensor diagnostics; never score as scientific outcomes"))
    worlds = load_population(root/"tests/fixtures/population_course.json").development
    settings = packet["settings"]
    paths = [output/f"worker-{i}.sqlite" for i in range(2)]
    budget = CourseBudget(**launch["budget"])
    providers = []
    stopped = None
    with ExitStack() as stack:
        stores = []
        resume = launch.get("resume_workers", [])
        if resume and len(resume) != 2:
            raise ValueError("resume requires both original worker snapshots")
        for index, path in enumerate(paths):
            if resume:
                import shutil
                if Path(resume[index]).resolve() != path.resolve():
                    shutil.copyfile(resume[index],path)
            stack.enter_context(_own_file(path))
            store = WorkerStore(path)
            stack.callback(store.close)
            stores.append(store)
            store.bind_run(worlds,branches,settings,dict(timeout_seconds=120,termination_seconds=1),budget=budget,regime="course")
        # Charge both assigned devices, including time before the first code cell.
        for device, store in zip(devices,stores):
            previous = store.connection.execute("SELECT * FROM allocations ORDER BY number DESC LIMIT 1").fetchone()
            if previous is not None and previous["stopped_at"] is None:
                raise BudgetStop("smoke_resume_requires_confirmed_previous_provider_release_and_new_admission")
            store.allocation_started(device,"development",budget=budget,started_at=launch["allocated_at"],
                billing=dict(provider=launch["provider"],release_instructions=launch["release_instructions"]))
        def before_attempt(*unused):
            admission(launch,stores,next_attempt=True)
        for device in devices:
            providers.append(ProcessProvider(factory(device),before_attempt=before_attempt))
        try:
            host_output = output
            if launch.get("resume_in_place"):
                count = stores[0].connection.execute("SELECT COUNT(*) FROM allocations").fetchone()[0]
                host_output = output/f"host-session-{count}"
                host_output.mkdir()
                save_json(host_output/"launch.json",launch)
            save_json(output/"host-checks.json",host_checks(root,launch,stores,host_output))
            for row, branch in zip(rows,branches):
                index = row["intended_worker"]
                view = peer_view(row["view"])
                rendered = RenderedRequest(**row["rendered"])
                tokenized = TokenizedRequest(row["tokenized"]["text"],tuple(row["tokenized"]["input_ids"]),tuple(row["tokenized"]["attention_mask"]))
                store = stores[index]
                store.prepare_control(branch,settings_json(settings),view,rendered,tokenized)
                if row["confirmed_restart_before"] or row["controlled_hang"]:
                    providers[index].close()
                if row["controlled_hang"]:
                    providers[index] = ProcessProvider(hang_factory,before_attempt=before_attempt)
                elif row.get("hardware_diagnostic"):
                    providers[index] = ProcessProvider(EnvelopeFactory(devices[index]),before_attempt=before_attempt)
                response = providers[index].obtain(store,row["smoke_call_id"],view,rendered,tokenized,
                    seed=row["seed"],settings=settings)
                validation = failed_reply(view) if isinstance(response,RecordedFailure) else validate_reply(view,response,tokenizer,limits=COURSE_LIMITS)
                store.save_control_validation(row["smoke_call_id"],validation)
                print(row["smoke_call_id"],store.call(row["smoke_call_id"])["status"],flush=True)
                attempt = store.attempts(row["smoke_call_id"])[-1]
                facts = json.loads(attempt["backend_json"]) if attempt["backend_json"] else {}
                observed_free = [sample["free_bytes"] for sample in facts.get("observed_model_edge_memory",[])]
                if facts.get("free_bytes_with_cache") is not None:
                    observed_free.append(facts["free_bytes_with_cache"])
                if observed_free and min(observed_free) < 1610612736:
                    stopped = "observed_headroom_below_required_1_5_GiB"
                    break
                if isinstance(response,RecordedFailure) and not row["controlled_hang"]:
                    stopped = "recorded_model_attempt_failure"
                    break
        except (Exception,KeyboardInterrupt) as error:
            stopped = f"{type(error).__name__}: {error}"
        finally:
            cleanup = []
            for provider in providers:
                try:
                    provider.close()
                    cleanup.append("confirmed process exit")
                except Exception as error:
                    cleanup.append(str(error))
            for store in stores:
                for allocation in store.connection.execute("SELECT number FROM allocations WHERE stopped_at IS NULL").fetchall():
                    store.allocation_stop_requested(allocation[0],"smoke_finished; provider_release_unconfirmed")
                destination = output/(store.path.stem+"-backup.sqlite")
                if destination.exists():
                    count = store.connection.execute("SELECT COUNT(*) FROM allocations").fetchone()[0]
                    destination = output/(store.path.stem+f"-backup-session-{count}.sqlite")
                store.backup(destination)
            cost = resources(stores,budget,utc())
            finished = sum(store.connection.execute("SELECT count(*) FROM calls WHERE status='completed'").fetchone()[0] for store in stores)
            attempts = sum(store.connection.execute("SELECT count(*) FROM attempts WHERE call_id != ?",(packet["requests"][-1]["smoke_call_id"],)).fetchone()[0] for store in stores)
    return dict(stop_reason=stopped,process_cleanup=cleanup,resources=cost,
        completed_model_generations=finished,model_physical_attempts=attempts,
        complete_resident_tokens_upper=110107,
        largest_prepared_request_resident_tokens=max(row["resident_tokens_with_reserve"] for row in packet["requests"]),
        provider_release_confirmed=False,physical_memory_accepted=False,
        complete_live_memory_upper_bound_bytes=None,actual_headroom_acceptance=None,
        r7_status="incomplete: supported complete-envelope review required",pilot_admitted=False)


def run(root, launch, output):
    if output.exists() and not launch.get("resume_in_place"):
        raise FileExistsError("fresh output required; preserve all previous evidence")
    if output.exists():
        import shutil
        previous = output/("report-before-resume-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".json")
        if (output/"report.json").exists():
            shutil.copyfile(output/"report.json",previous)
    else:
        output.mkdir(parents=True)
    report = dict(status="blocked",model_generations=0,gpu_admission=False,weights_staged_by_this_run=False,
        runtime_freeze=False,provider_release_confirmed=False,physical_memory_accepted=False,
        complete_live_memory_upper_bound_bytes=None,actual_headroom_acceptance=None,root_blocker=None)
    try:
        if launch.get("execute_gpu") is not True:
            raise BudgetStop("gpu_execution_disabled")
        admission(launch,next_attempt=True)
        save_json(output/"launch.json",launch)
        # Import/read native assets only after authorization and resources pass.
        os.environ.update(HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1",HF_HUB_CACHE=launch["hf_cache"])
        from scripts.m5_course_smoke_assets import verify_assets
        assets = verify_assets(root,launch)
        import subprocess
        inventory = subprocess.check_output(["nvidia-smi","--query-gpu=uuid,name,driver_version,memory.total","--format=csv,noheader"],text=True,timeout=5)
        rows = [line.split(",") for line in inventory.splitlines()]
        if len(rows) != 2 or any("T4" not in row[1] for row in rows) or rows[0][0].strip() == rows[1][0].strip():
            raise ValueError("two distinct physical T4s required")
        report["host_inventory"] = inventory
        report["assets"] = assets
        tokenizer = TokenizerFactory(CANDIDATE,str(root/"metadata/4B"),COURSE_LIMITS)()
        packet = read(root/"notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")
        from scripts.m5_course_preparation import verify_native_requests
        verify_native_requests(root,tokenizer,packet)
        report.update(status="incomplete",gpu_admission=True,model_generations=None)
        report["smoke"] = execute_requests(root,packet,launch,[row[0].strip() for row in rows],output,tokenizer=tokenizer,
            complete_envelope=launch.get("complete_envelope_diagnostics",False))
    except (Exception,KeyboardInterrupt) as error:
        report["root_blocker"] = f"{type(error).__name__}: {error}"
    finally:
        save_json(output/"report.json",report)
        exported = export_evidence(output)
        print(json.dumps(exported,indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--launch",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--check-admission-only",action="store_true")
    parser.add_argument("--host-checks",action="store_true")
    args = parser.parse_args()
    launch = read(args.launch)
    if args.host_checks:
        import unittest
        names = ["tests.worker_checks.ParentAccessTests.test_controls_are_durable_empty_send_full_shape_and_reject_input_drift",
            "tests.durable_checks.DurableTests.test_checkpoint_write_failure_before_and_after_commit_has_one_authoritative_effect",
            "tests.attempt_checks.ProcessAttemptTests.test_interrupted_backend_retries_identical_inputs_and_preserves_ambiguous_completed_work"]
        result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        raise SystemExit(not result.wasSuccessful())
    elif args.check_admission_only:
        # Keep an already-assigned GPU clock, including all asset preparation.
        prospective = not launch.get("allocated_at")
        admission(dict(launch,allocated_at=utc()) if prospective else launch,next_attempt=True)
        save_json(args.output,dict(prospective_resource_check=prospective,gpu_execution=False,model_generations=0))
    else:
        run(args.root.resolve(),launch,args.output.resolve())


if __name__ == "__main__":
    main()
