"""Bounded course smoke using existing worker/attempt/allocation records.

Importing this module performs no CUDA initialization, loading or download.
GPU execution requires an explicit launch record and admitted resource bounds.
"""

import argparse
from contextlib import ExitStack
from dataclasses import asdict, dataclass, replace
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
    allocated = result["allocated_gpu_hours"] or 0
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
    current = resources(stores, budget, now)
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
    if not stores:
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
    return cases


class SmokeBackend:
    def __init__(self, backend):
        self.backend = backend
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


def controlled_hang(*args, **kwargs):
    while True:
        sleep(1)


def hang_factory():
    """Infrastructure-only slot; never describe its timeout as model latency."""
    return controlled_hang


def execute_requests(root, packet, launch, devices, output, *, tokenizer, factory=SmokeFactory):
    """Serial isolated probes; all raw outcomes remain in the original ledger."""
    from recovery.manifests import load_population
    verify_requests(root,packet)
    branches = tuple(smoke_branch(row) for row in packet["requests"])
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
            for row, branch in zip(packet["requests"],branches):
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
                response = providers[index].obtain(store,row["smoke_call_id"],view,rendered,tokenized,
                    seed=row["seed"],settings=settings)
                validation = failed_reply(view) if isinstance(response,RecordedFailure) else validate_reply(view,response,tokenizer,limits=COURSE_LIMITS)
                store.save_control_validation(row["smoke_call_id"],validation)
                print(row["smoke_call_id"],store.call(row["smoke_call_id"])["status"],flush=True)
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
                store.backup(output/(store.path.stem+"-backup.sqlite"))
            cost = resources(stores,budget,utc())
            finished = sum(store.connection.execute("SELECT count(*) FROM calls WHERE status='completed'").fetchone()[0] for store in stores)
            attempts = sum(store.connection.execute("SELECT count(*) FROM attempts WHERE call_id != ?",(packet["requests"][-1]["smoke_call_id"],)).fetchone()[0] for store in stores)
    return dict(stop_reason=stopped,process_cleanup=cleanup,resources=cost,
        completed_model_generations=finished,model_physical_attempts=attempts,
        provider_release_confirmed=False,physical_memory_accepted=False,
        complete_live_memory_upper_bound_bytes=None,actual_headroom_acceptance=None,
        r7_status="incomplete: supported complete-envelope review required",pilot_admitted=False)


def run(root, launch, output):
    if output.exists():
        raise FileExistsError("fresh output required; preserve all previous evidence")
    output.mkdir(parents=True)
    report = dict(status="blocked",model_generations=0,gpu_admission=False,weights_staged_by_this_run=False,
        runtime_freeze=False,provider_release_confirmed=False,physical_memory_accepted=False,
        complete_live_memory_upper_bound_bytes=None,actual_headroom_acceptance=None,root_blocker=None)
    try:
        if launch.get("execute_gpu") is not True:
            raise BudgetStop("gpu_execution_disabled")
        admission(launch,next_attempt=True)
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
        report.update(status="incomplete",gpu_admission=True)
        report["smoke"] = execute_requests(root,packet,launch,[row[0].strip() for row in rows],output,tokenizer=tokenizer)
        report["model_generations"] = None  # Failed/interrupted completion is unknown; exact completed count is separate.
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
    args = parser.parse_args()
    run(args.root.resolve(),read(args.launch),args.output.resolve())


if __name__ == "__main__":
    main()
