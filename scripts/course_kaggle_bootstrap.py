"""Online-first pinned Kaggle setup, with optional portable asset restoration.

The bare entry point uses the standard library. It never loads a model or
initializes CUDA; scientific execution remains in the existing workflow.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import subprocess
import sys
import time
import zipfile
from copy import deepcopy
from contextlib import closing
import sqlite3
from types import SimpleNamespace

if not __package__:
    import types
    namespace = types.ModuleType("scripts")
    namespace.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules.setdefault("scripts", namespace)

from scripts.m5_kaggle_preflight import (PIP_WHEEL_RUNNER, sha256_file, save_json,
    candidate_environment, command, source_identity, assigned_preparation_window, EXPORT_SECONDS, utc,
    smoke_attempt_usage, smoke_attempt_limit, validate_smoke_predecessor, hardware_matrix_recorded)


def qualification_choice(bundle, config):
    """Derive the next fixed candidate from existing terminal gate evidence.

    No model, dependency imports or new selection store. Incomplete sessions
    stay on their candidate; a frozen/main candidate can never fall back.
    """
    if config.get("candidate_order") != ["9B","4B"]:
        raise ValueError("qualification order must be the adopted 9B then 4B")
    prior = 23
    for label in config["candidate_order"]:
        target = Path(bundle)/"candidates"/label
        action = target/"automatic-run.json"
        run = json.loads((target/"run.json").read_bytes()) if (target/"run.json").exists() else {}
        result = json.loads(action.read_bytes()) if action.exists() else {}
        reason = result.get("reason") or ""
        gate_failure = any(code in reason for code in (
            "complete_hardware_stress_headroom_cache_and_loading_gate_not_passed",
            "recorded_model_attempt_failure", "observed_headroom_below_required_1_5_GiB"))
        capability = target/"capability-gate.json"
        if "first_90_capability_gate_not_passed" in reason and capability.exists():
            gate_failure |= json.loads(capability.read_bytes()).get("status") == "failed"
        pilot = target/"pilot-gate.json"
        if "complete_pilot_acceptance_not_passed" in reason and pilot.exists():
            gate = json.loads(pilot.read_bytes())
            gate_failure |= gate.get("complete") is True and gate.get("audit",{}).get("passed") is True
        hardware = target/"hardware/report.json"
        if hardware.exists():
            report = json.loads(hardware.read_bytes())
            gate_failure |= "out of memory" in (report.get("root_blocker") or "").lower()
        if label == "4B" or run.get("freeze") or not gate_failure:
            return label, prior
        for path in target.glob("hardware/worker-*.sqlite"):
            with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
                prior += db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
    raise AssertionError("fixed candidate order exhausted")


def preparation_budget(root, bundle, config, saved):
    """Read canonical allocation rows before large downloads, without dependencies.

    Use the existing allocation partition. Temporary release bounds never alter
    worker evidence; the installed workflow applies the actual receipt later.
    Hardware already incorporated in run.json is excluded exactly once.
    """
    sys.path.insert(0,str(root))
    from recovery.costs import _allocation_resources, timestamp
    budget = deepcopy(saved["budget"] if saved else config["budget"])
    paths = list(bundle.glob("development/worker-*.sqlite"))+list(bundle.glob("main/worker-*.sqlite"))
    paths += list(bundle.glob("refusals/*/worker-*.sqlite"))
    paths += list(bundle.glob("hardware/worker-*.sqlite"))
    rows = {name:[] for name in ("allocations","attempts","provider_processes")}
    now, release = utc(), config.get("previous_session_release", {})
    recorded_assignments = {}
    for index,path in enumerate(sorted(paths)):
        with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
            db.row_factory = sqlite3.Row
            for row in db.execute("SELECT started_at,billing_json FROM allocations"):
                identity = json.loads(row["billing_json"] or "{}").get("physical_gpu_uuid")
                recorded_assignments.setdefault(row["started_at"],set()).add(identity)
            if saved and path.parent.name == "hardware":
                continue
            for table in rows:
                rows[table].extend(dict(row,worker=index) for row in db.execute("SELECT * FROM "+table))
    for allocation in rows["allocations"]:
        if allocation["stopped_at"] is None:
            if allocation["started_at"] == config.get("allocated_at"):
                raise ValueError("reuse the existing verified environment for an active assignment")
            at = release.get("released_at")
            if (not at or not release.get("evidence", "").strip() or
                    not timestamp(allocation["started_at"]) <= timestamp(at) <= timestamp(now)):
                raise ValueError("actual_previous_provider_release_required_before_online_downloads")
            for row in rows["attempts"]+rows["provider_processes"]:
                if row["worker"] != allocation["worker"]:
                    continue
                if any(row.get(key) and timestamp(row[key]) > timestamp(at)
                        for key in ("finished_at","last_observed_at","stopped_at")):
                    raise ValueError("provider release precedes observed model work")
            allocation["stopped_at"] = at
    # Pre-install failures may not yet have an ordinary allocation-only worker.
    # Include their known two-device intervals; unknown facts still refuse.
    for path in sorted((bundle/"bootstrap-refusals").glob("*.json")):
        receipt = json.loads(path.read_bytes())
        correction = config.get("bootstrap_refusal_assignments", {}).get(path.name, {})
        if correction:
            if not correction.get("evidence", "").strip():
                raise ValueError("bootstrap_assignment_correction_requires_provider_evidence")
            receipt.update({key:correction[key] for key in ("allocated_at","physical_devices") if correction.get(key)})
        start,devices = receipt.get("allocated_at"),receipt.get("physical_devices")
        if not start or len(devices or ()) != 2 or timestamp(start) > timestamp(receipt["observed_at"]):
            raise ValueError("earlier_bootstrap_assignment_interval_unknown")
        if start in recorded_assignments:
            if recorded_assignments[start] != set(devices):
                raise ValueError("bootstrap_assignment_physical_devices_differ")
            continue
        at = release.get("released_at")
        if not at or not release.get("evidence", "").strip() or not timestamp(start) <= timestamp(at) <= timestamp(now):
            raise ValueError("bootstrap_assignment_release_evidence_required")
        for index,device in enumerate(devices):
            rows["allocations"].append(dict(worker=len(paths)+index,number=0,device=f"kaggle-t4-slot-{index}",
                started_at=start,stopped_at=at,stop_requested_at=None,stop_reason="supplied actual provider release",
                stage="main" if receipt.get("stage") == "main" else "development",
                billing_json=json.dumps(dict(unadmitted_action=receipt.get("stage","hardware"),physical_gpu_uuid=device))))
        recorded_assignments[start] = set(devices)
    used = _allocation_resources(rows["allocations"],rows["attempts"],rows["provider_processes"],now,SimpleNamespace(**budget))
    additional = dict(development=0.,setup=0.,interruption=0.,other_course=0.,smoke=0.)
    for device in used["devices"]:
        partition = device["partition_seconds"]
        additional["setup"] += partition["setup"]/3600
        additional["interruption"] += (partition["interruption"]+partition["uncertain_work"])/3600
        phase = "development" if device["stage"] == "development" else "other_course"
        additional[phase] += (partition["attempt"]+partition["idle"])/3600
        if not saved and json.loads(device["billing_json"] or "{}").get("unadmitted_action","hardware") == "hardware":
            additional["smoke"] += device["allocated_seconds"]/3600
    for name,hours in additional.items():
        if budget.get("prior_"+name+"_gpu_hours") is not None:
            budget["prior_"+name+"_gpu_hours"] = [v+hours for v in budget["prior_"+name+"_gpu_hours"]]
    if not saved and budget.get("prior_smoke_attempts") is not None:
        budget["prior_smoke_attempts"] += sum(row["worker"] in {d["worker"] for d in used["devices"]
            if json.loads(d["billing_json"] or "{}").get("unadmitted_action","hardware") == "hardware"}
            for row in rows["attempts"])
    return budget


def online(root, config_path, scratch, output):
    config = json.loads(config_path.read_bytes())
    manifest = json.loads((root/"source-manifest.json").read_bytes())
    source_identity(root,manifest)
    validate_smoke_predecessor(root,config["budget"])
    if not config.get("authorizations", {}).get("weights", "").strip():
        raise ValueError("explicit pinned checkpoint download authorization required")
    bundle = config_path.resolve().parent
    saved = json.loads((bundle/"run.json").read_bytes()) if (bundle/"run.json").exists() else None
    action = "main" if saved and saved["freeze"] else "pilot" if saved else "hardware"
    report_path = bundle/"hardware/report.json"
    if saved is None and report_path.exists():
        report = json.loads(report_path.read_bytes())
        stop = report.get("root_blocker") or report.get("smoke", {}).get("stop_reason")
        if stop and not str(stop).startswith(("KeyboardInterrupt:", "BudgetStop: allocation_deadline")):
            raise ValueError("saved_hardware_failure_before_downloads: "+str(stop))
    if config.get("resource_policy") == "observe" and saved is None:
        # This is stdlib-only and happens before multi-GB dependency downloads.
        paths = list(bundle.glob("hardware/worker-*.sqlite"))
        prior_paths = list(bundle.glob("refusals/*/worker-*.sqlite"))
        usage = smoke_attempt_usage(config["budget"],paths,prior_paths=prior_paths)
        canonical = [bundle/f"hardware/worker-{i}.sqlite" for i in range(2)]
        if usage["total_recorded"] >= smoke_attempt_limit(config) and not hardware_matrix_recorded(canonical):
            raise ValueError("recorded_smoke_attempt_limit_before_downloads")
    if not config.get("authorizations", {}).get(action, "").strip():
        raise ValueError("explicit_"+action+"_authorization_missing")
    launch = dict(stage_weights=True,execute_gpu=False,authorization=config["authorizations"]["weights"],
        provider="kaggle",reported_quota_gpu_hours=config.get("provider_quota_gpu_hours"),
        prior_sessions_released=config.get("prior_sessions_released",False),allocated_at=config.get("allocated_at"),
        provider_session_seconds=config.get("provider_session_seconds"),release_instructions=config.get("release_instructions",""),
        budget=(saved["budget"] if saved else config["budget"]) if config.get("resource_policy") == "observe" else preparation_budget(root,bundle,config,saved),
        resource_policy=config.get("resource_policy"),session_limit_seconds=config.get("max_work_seconds",36000),resume_workers=[],
        **({"candidate":config["candidate"],"envelope_timeout_seconds":config.get("envelope_timeout_seconds",600)} if config.get("candidate") else {}),
        smoke_attempt_limit=config.get("smoke_attempt_limit",24),smoke_attempt_allowance=config.get("smoke_attempt_allowance"),
        hf_cache=config.get("hf_cache"))
    from scripts.m5_course_smoke_assets import prepare
    result = prepare(root,manifest,launch,scratch,output,online_config=config_path,smoke_required=saved is None)
    if result["status"] != "prepared":
        raise ValueError(result["root_blocker"])
    return dict(interpreter=result["interpreter"],assets_receipt=result["assets_receipt"],hf_cache=result["hf_cache"],
        online=True,note="Pinned native wheel hashes, installed versions/module bytes and checkpoint revision/LFS hashes verified; no model loaded")


def check_resume(root, config_path, output):
    """Apply the real release receipt, then admit resources before resumed weights."""
    from scripts.course_kaggle_workflow import snapshot, session_window, course_budget, end_observations
    from recovery.accounting import CourseBudget, course_admission
    config = json.loads(config_path.read_bytes())
    bundle = config_path.resolve().parent
    run = json.loads((bundle/"run.json").read_bytes())
    stage = "main" if run["freeze"] else "development"
    # The pre-install screen already bounds known prior open intervals using
    # their real release receipt. The ordinary controller applies it on resume.
    from scripts.course_kaggle_workflow import recover_bootstrap_refusals, confirm_previous_release
    recover_bootstrap_refusals(root,bundle,config)
    if config.get("resource_policy") == "observe":
        end_observations(bundle,current_assignment=config.get("allocated_at"))
    else:
        confirm_previous_release(bundle,config.get("previous_session_release"))
    progress = snapshot(root,bundle,stage,run,devices=("kaggle-t4-slot-0","kaggle-t4-slot-1"))
    reason,seconds = course_admission(progress["resources"],progress["forecast"],course_budget(config,run["budget"]),stage,2)
    if reason:
        raise ValueError(reason)
    save_json(output/"admission.json",dict(gpu_execution=False,model_generations=0,stage=stage,
        allowed_gpu_seconds=seconds,provider_wall_seconds=session_window(config)))
    return dict(resume_admission=True)


def extract_assets(archive, destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(destination)
    with zipfile.ZipFile(archive) as source:
        seen = set()
        for item in source.infolist():
            path = PurePosixPath(item.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in item.filename or ":" in item.filename
                    or item.filename in seen or (item.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError("unsafe portable asset member")
            seen.add(item.filename)
        if shutil.disk_usage(destination.parent).free < sum(i.file_size for i in source.infolist())+512*1024**2:
            raise ValueError("insufficient disk for portable assets; prefer an extracted read-only Kaggle input dataset")
        destination.mkdir(parents=True)
        source.extractall(destination)


def export_assets(root, scratch, receipt, destination):
    """Portable downloads, not a copied venv or a second experiment store."""
    scratch, destination = Path(scratch), Path(destination)
    if destination.exists():
        raise FileExistsError(destination)
    source_manifest = json.loads((Path(root)/"source-manifest.json").read_bytes())
    assets = json.loads(Path(receipt).read_bytes())
    members = {"prepared-assets.json":Path(receipt)}
    for directory in ("wheels", "built"):
        for path in (scratch/directory).glob("*.whl"):
            members[f"{directory}/{path.name}"] = path
    for name in ("install.lock", "pip.lock", "build-constraints.txt"):
        members[name] = scratch/name
    cache = Path(assets["hf_cache"])
    snapshot = cache/("models--"+assets["model"].replace("/", "--"))/"snapshots"/assets["revision"]
    for name in assets["checkpoint_files"]:
        members["checkpoint/"+name] = snapshot/name
    # The environment is a reproducible staging copy, not experiment evidence.
    # Its verified receipt/wheel survives. Free it before packing large weights.
    venv = (scratch/"venv").resolve()
    if not venv.is_relative_to(scratch.resolve()) or venv.name != "venv":
        raise ValueError("setup environment cleanup escaped the fresh owned scratch")
    if venv.exists():
        shutil.rmtree(venv)
    largest = max(p.stat().st_size for p in members.values())
    if shutil.disk_usage(destination.parent).free < largest+512*1024**2:
        raise ValueError("insufficient disk space to pack the largest verified asset and export reserve")
    with zipfile.ZipFile(destination, "x", zipfile.ZIP_STORED) as archive:
        for name,path in sorted(members.items()):
            archive.write(path, name)
            # Consume only newly created, rebuildable setup downloads after
            # their entry is written. The ZIP replaces these staging copies;
            # no original research file, input dataset or receipt is deleted.
            target = path.resolve()
            if target.is_relative_to(scratch.resolve()):
                target.unlink()
                if path.is_symlink():
                    path.unlink()
    return dict(path=str(destination), bytes=destination.stat().st_size,
        source_commit=source_manifest["source_baseline_commit"], model_revision=assets["revision"],
        note="Reusable pinned target wheels/checkpoint; no GPU work or accepted environment freeze")


def setup(root, config, scratch, output):
    sys.path.insert(0,str(root))  # CPU preparation only; inference later uses -I ordinary install
    from scripts.m5_course_smoke_assets import prepare
    if not config.get("authorizations", {}).get("weights", "").strip():
        raise ValueError("explicit pinned weight-staging authorization required")
    launch = dict(stage_weights=True, execute_gpu=False, authorization=config["authorizations"]["weights"],
        provider="kaggle", reported_quota_gpu_hours=config.get("provider_quota_gpu_hours"),
        prior_sessions_released=config.get("prior_sessions_released", False),
        allocated_at=config.get("allocated_at"), provider_session_seconds=config.get("provider_session_seconds"),
        release_instructions=config.get("release_instructions", ""), budget=config["budget"], resume_workers=[])
    manifest = json.loads((root/"source-manifest.json").read_bytes())
    result = prepare(root, manifest, launch, scratch, output, workflow_seconds=1800, portable_assets=True)
    if result["status"] != "prepared":
        raise ValueError(result["root_blocker"])
    exported = export_assets(root, scratch, output/"prepared-assets.json", output.parent/"course-assets.zip")
    return dict(interpreter=None, assets_receipt=result["assets_receipt"],
        hf_cache=None, export=exported, requires_dataset_restore=True,
        note="Download the assets ZIP and restore it as a private input in a new CPU session; staging copies were consumed")


def restore(root, assets_zip, scratch, output, *, seconds=1800, config=None):
    if platform.system() != "Linux" or platform.machine() != "x86_64" or sys.version_info[:2] != (3,13):
        raise ValueError("Pinned candidate requires Linux x86_64 Python 3.13; changing it reopens host acceptance")
    manifest = json.loads((root/"source-manifest.json").read_bytes())
    source_identity(root, manifest)
    if config and config.get("execute_gpu"):
        bundle = Path(config["_bundle"])
        saved = json.loads((bundle/"run.json").read_bytes()) if (bundle/"run.json").exists() else None
        action = "main" if saved and saved["freeze"] else "pilot" if saved else "hardware"
        launch = dict(authorization=config.get("authorizations", {}).get(action, ""),
            prior_sessions_released=config.get("prior_sessions_released"),resume_workers=[],
            budget=saved["budget"] if saved else config["budget"],allocated_at=config.get("allocated_at"),
            reported_quota_gpu_hours=config.get("provider_quota_gpu_hours"),
            provider_session_seconds=config.get("provider_session_seconds"),release_instructions=config.get("release_instructions"))
        wall = assigned_preparation_window(launch,smoke_required=saved is None)
        seconds = min(seconds,wall-launch["budget"]["shutdown_seconds"]-EXPORT_SECONDS-124)
    if assets_zip.is_dir():
        if scratch.exists():
            raise FileExistsError(scratch)
        scratch.mkdir(parents=True)
        asset_root = assets_zip.resolve()
    else:
        extract_assets(assets_zip, scratch)
        asset_root = scratch
    output.mkdir(parents=True, exist_ok=False)
    assets = json.loads((asset_root/"prepared-assets.json").read_bytes())
    if assets["source_commit"] != manifest["source_baseline_commit"]:
        raise ValueError("portable assets belong to different source; resume the same uploaded package")
    env = candidate_environment(scratch)
    deadline = time.monotonic()+seconds
    def invoke(name, arguments, timeout=300):
        return command(output, name, arguments, deadline=deadline, timeout=timeout, cwd=scratch, env=env)
    venv = scratch/"venv"
    invoke("create-environment", [sys.executable, "-m", "venv", "--without-pip", venv], 60)
    python = venv/"bin/python"
    pip = manifest["build_tools"]["pip"]["wheels"][0]
    wheel_dir = asset_root/"wheels"
    for item in manifest["candidate_wheels"]+[pip]:
        path = wheel_dir/item["filename"]
        if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
            raise ValueError("portable target wheel differs: "+item["filename"])
    expanded = 0
    for path in wheel_dir.glob("*.whl"):
        with zipfile.ZipFile(path) as wheel:
            expanded += sum(i.file_size for i in wheel.infolist())
    if shutil.disk_usage(scratch).free < expanded+512*1024**2:
        raise ValueError("insufficient disk for the pinned installed environment and reserve")
    invoke("bootstrap-pip", [python, "-I", "-c", PIP_WHEEL_RUNNER, wheel_dir/pip["filename"],
        "--isolated", "install", "--no-deps", "--no-index", "--find-links", wheel_dir, "--require-hashes", "-r", asset_root/"pip.lock"], 120)
    invoke("install-pinned-environment", [python, "-m", "pip", "--isolated", "install", "--no-deps", "--no-index",
        "--no-compile", "--find-links", wheel_dir, "--require-hashes", "-r", asset_root/"install.lock"])
    project = list((asset_root/"built").glob("*.whl"))
    if len(project) != 1:
        raise ValueError("one portable ordinary project wheel required")
    invoke("install-project", [python, "-m", "pip", "--isolated", "install", "--no-deps", "--no-index", "--no-compile", project[0]], 60)
    # Recreate the native pinned snapshot layout without duplicating weights.
    cache = scratch/"hub"
    snapshot = cache/("models--"+assets["model"].replace("/", "--"))/"snapshots"/assets["revision"]
    snapshot.mkdir(parents=True)
    for name, expected in assets["checkpoint_files"].items():
        path = asset_root/"checkpoint"/name
        if path.stat().st_size != expected["bytes"] or sha256_file(path) != expected["sha256"]:
            raise ValueError("portable checkpoint differs: "+name)
        (snapshot/name).symlink_to(path)
    assets.update(interpreter=str(python), hf_cache=str(cache))
    receipt = output/"prepared-assets.json"
    save_json(receipt, assets)
    invoke("verify-ordinary-installed-source", [python, "-I", "-c",
        "import json,sys,types; from pathlib import Path; "
        "namespace=types.ModuleType('scripts'); namespace.__path__=[str(Path(sys.argv[1])/'scripts')]; sys.modules['scripts']=namespace; "
        "from scripts.m5_course_smoke_assets import verify_assets; "
        "print(verify_assets(Path(sys.argv[1]),dict(source_manifest=sys.argv[2],assets_receipt=sys.argv[3],hf_cache=sys.argv[4])))",
        root, root/"source-manifest.json", receipt, cache], 120)
    return dict(interpreter=str(python), assets_receipt=str(receipt), hf_cache=str(cache), restored=True,
        note="Same pinned environment/checkpoint/source; no downloads or model loading")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("online", "check-resume", "setup", "restore", "cpu"))
    for name in ("root", "scratch", "output"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--assets", type=Path)
    args = parser.parse_args()
    root, scratch, output = args.root.resolve(), args.scratch.resolve(), args.output.resolve()
    try:
        if args.action in ("online","check-resume"):
            if not args.config:
                raise ValueError(args.action+" requires configuration")
            result = (online(root,args.config,scratch,output) if args.action == "online" else
                check_resume(root,args.config,output))
            if args.action == "check-resume":
                return
        elif args.action == "setup":
            if not args.config:
                raise ValueError("setup requires configuration")
            result = setup(root, json.loads(args.config.read_bytes()), scratch, output)
        elif args.action == "restore":
            if not args.assets:
                raise ValueError("restore requires the portable assets ZIP")
            config = json.loads(args.config.read_bytes()) if args.config else None
            if config:
                config["_bundle"] = str(args.config.resolve().parent)
            result = restore(root, args.assets, scratch, output,config=config)
        else:
            if platform.system() == "Linux" and platform.machine() == "x86_64" and sys.version_info[:2] == (3,13):
                manifest = json.loads((root/"source-manifest.json").read_bytes())
                from scripts.m5_course_smoke_assets import prepare
                launch = dict(resource_policy="observe") if args.config and json.loads(args.config.read_bytes()).get("resource_policy") == "observe" else {}
                result = prepare(root,manifest,launch,scratch,output,cpu_only=True)
                if result["status"] != "prepared":
                    raise ValueError(result["root_blocker"])
                save_json(output/"bootstrap.json",result)
                print(json.dumps(result,indent=2),flush=True)
                return
            if scratch.exists() or output.exists():
                raise FileExistsError("fresh CPU environment/output required")
            output.mkdir(parents=True)
            subprocess.run([sys.executable, "-m", "venv", scratch], check=True, timeout=60)
            python = scratch/("Scripts/python.exe" if os.name == "nt" else "bin/python")
            subprocess.run([python, "-m", "pip", "--disable-pip-version-check", "install", "-r",
                root/"configs/course-cpu-reproduction.txt", root], check=True, timeout=900)
            freeze = subprocess.check_output([python, "-m", "pip", "freeze", "--all"], text=True, timeout=30)
            (output/"cpu-environment.lock").write_text(freeze, encoding="utf-8")
            result = dict(interpreter=str(python), assets_receipt=None, hf_cache=None,
                gpu_calls=0, model_weights_staged=False, note="CPU analysis environment; not the accepted inference environment")
        save_json(output/"bootstrap.json", result)
        print(json.dumps(result, indent=2), flush=True)
    except (Exception, KeyboardInterrupt) as error:
        output.mkdir(parents=True, exist_ok=True)
        save_json(output/"bootstrap.json", dict(status="blocked", reason=f"{type(error).__name__}: {error}", gpu_calls=0))
        raise


if __name__ == "__main__":
    main()
