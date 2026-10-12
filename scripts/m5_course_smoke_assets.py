"""CPU preparation of the existing pinned environment/cache, then offline verification."""

import argparse
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from math import isfinite
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import zipfile

if not __package__:
    # CPU bootstrap precedes project installation. Its source imports are
    # stdlib-only; the later installed probe and GPU runner use -I isolation.
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    import types
    namespace = types.ModuleType("scripts")
    namespace.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules.setdefault("scripts",namespace)

from scripts.m5_course_preparation import CANDIDATE, read
from scripts.m5_kaggle_preflight import (PIP_WHEEL_RUNNER, BUILD_RESERVE, EXPORT_SECONDS,
    candidate_environment, command, export_evidence, installed_probe_script,
    installed_provenance, pip_wheel_download_script, require_space, save_json, sha256_file, utc)


def assigned_device_count():
    devices = Path("/proc/driver/nvidia/gpus")
    return len(list(devices.iterdir())) if devices.is_dir() else 0


def assigned_preparation_window(launch, now=None):
    """Conservative pre-install screen; installed CourseBudget still gates weights.

    The bare bootstrap has no LangGraph/Pydantic environment yet. Check the
    supplied bounds before downloads, without CUDA or resetting assignment time.
    Current allocation enters the ordinary smoke ledgers from this same clock.
    """
    if not launch.get("authorization", "").strip() or launch.get("prior_sessions_released") is not True:
        raise ValueError("authorization_or_prior_release_missing")
    if launch.get("resume_workers"):
        raise ValueError("assigned_preparation_requires_fresh_run; reuse admitted assets for resume")
    budget = launch["budget"]
    if not budget.get("prior_evidence", "").strip() or budget.get("allocation_mode") != "gpu":
        raise ValueError("documented_prior_bounds_and_gpu_charging_required")
    def number(value):
        if type(value) not in (int,float) or not isfinite(value) or value < 0:
            raise ValueError("finite_nonnegative_resource_bound_required")
        return value
    upper = {}
    for name in ("development","setup","interruption","other_course","other_overall","smoke"):
        bounds = budget.get("prior_"+name+"_gpu_hours")
        if not isinstance(bounds,(tuple,list)) or len(bounds) != 2 or number(bounds[0]) > number(bounds[1]):
            raise ValueError("supported_prior_allocation_and_smoke_bounds_required")
        upper[name] = bounds[1]
    attempts = budget.get("prior_smoke_attempts")
    if type(attempts) is not int or not 0 <= attempts < 24:
        raise ValueError("remaining_cumulative_smoke_attempt_required")
    remaining = []
    for name,ceiling in (("development",8),("setup",2),("interruption",2)):
        reserve = number(budget[name+"_reserve_gpu_hours"])
        if reserve > ceiling:
            raise ValueError("adopted_preparation_allowance_exceeded")
        remaining.append(reserve-upper[name])
    course = sum(upper[name] for name in ("development","setup","interruption","other_course"))
    for field,ceiling,spent in (("ceiling_gpu_hours",30,course),("overall_ceiling_gpu_hours",100,course+upper["other_overall"])):
        limit = number(budget[field])
        if not 0 < limit <= ceiling:
            raise ValueError("adopted_resource_ceiling_required")
        remaining.append(limit-spent)
    remaining.append(.5-upper["smoke"])
    if not launch.get("allocated_at"):
        raise ValueError("actual_provider_assignment_clock_required")
    assigned = datetime.fromisoformat(launch["allocated_at"])
    current = datetime.fromisoformat(now or utc())
    if assigned.tzinfo is None or current.tzinfo is None:
        raise ValueError("timezone_aware_assignment_required")
    elapsed = (current-assigned).total_seconds()
    if elapsed < 0:
        raise ValueError("provider_assignment_cannot_be_in_future")
    quota = number(launch.get("reported_quota_gpu_hours"))
    duration = number(launch.get("provider_session_seconds"))
    if quota == 0 or duration == 0 or not launch.get("release_instructions", "").strip():
        raise ValueError("provider_terms_required")
    shutdown = number(budget["shutdown_seconds"])
    if shutdown < 120:
        raise ValueError("at_least_120_seconds_for_provider_release_required")
    wall = min((3600*min(remaining)-number(budget["overhead_seconds"]))/2-elapsed,
        quota*3600/2,duration-elapsed)
    if wall <= shutdown+EXPORT_SECONDS+8+124:
        raise ValueError("insufficient_remaining_time_for_preparation_attempt_export_and_release")
    return wall


def source_identity(root, manifest):
    if (root/"SOURCE_COMMIT.txt").read_text().strip() != manifest["source_baseline_commit"]:
        raise ValueError("prepared source commit differs")
    for name, wanted in manifest["members"].items():
        path = root/name
        if not path.is_file() or path.is_symlink() or path.stat().st_size != wanted["bytes"] or sha256_file(path) != wanted["sha256"]:
            raise ValueError("prepared source member differs: "+name)


def verify_assets(root, launch):
    manifest, assets = read(launch["source_manifest"]), read(launch["assets_receipt"])
    source_identity(root,manifest)
    if assets["source_commit"] != manifest["source_baseline_commit"]:
        raise ValueError("CPU assets belong to a different committed source")
    if (assets["model"],assets["revision"]) != (CANDIDATE.model,CANDIDATE.revision):
        raise ValueError("CPU assets candidate differs")
    for name, version in assets["versions"].items():
        if importlib.metadata.version(name) != version:
            raise ValueError("installed candidate package differs: "+name)
    import recovery
    package = Path(recovery.__file__).resolve().parent
    for name, wanted in assets["installed_modules"].items():
        if sha256_file(package/name) != wanted:
            raise ValueError("ordinary installed production module differs: "+name)
    if package == (root/"recovery").resolve():
        raise ValueError("GPU runner must use ordinary installed recovery, not the source checkout")
    cache = Path(launch["hf_cache"]).resolve()
    snapshot = cache/("models--"+CANDIDATE.model.replace("/","--"))/"snapshots"/CANDIDATE.revision
    for name, wanted in assets["checkpoint_files"].items():
        path = snapshot/name
        if not path.is_file() or path.stat().st_size != wanted["bytes"] or sha256_file(path) != wanted["sha256"]:
            raise ValueError("pinned checkpoint asset differs: "+name)
    return dict(source_commit=assets["source_commit"],ordinary_installed_module=str(package),
        matching_modules=len(assets["installed_modules"]),versions=assets["versions"],snapshot=str(snapshot),
        checkpoint_files_verified=len(assets["checkpoint_files"]),gpu_memory_accepted=False)


def download_weights(root, manifest, cache, receipt):
    """Called only by the admitted, bounded CPU child; no model/CUDA loading."""
    from huggingface_hub import HfApi, snapshot_download
    inspection = read(root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
    info = HfApi().model_info(CANDIDATE.model,revision=CANDIDATE.revision,files_metadata=True)
    if info.sha != CANDIDATE.revision:
        raise ValueError("immutable checkpoint revision differs")
    files = {s.rfilename:s for s in info.siblings}
    expected = {}
    for name in inspection["checkpoint_index"]["shard_files"]:
        item = files[name]
        if item.lfs is None or not re.fullmatch("[0-9a-f]{64}",item.lfs.sha256):
            raise ValueError("checkpoint shard lacks native LFS identity")
        expected[name] = dict(bytes=item.lfs.size,sha256=item.lfs.sha256)
    for path, wanted in manifest["members"].items():
        if path.startswith("metadata/4B/"):
            expected[Path(path).name] = wanted
    snapshot = Path(snapshot_download(CANDIDATE.model,revision=CANDIDATE.revision,
        cache_dir=cache,allow_patterns=list(expected),max_workers=2))
    for name, wanted in expected.items():
        path = snapshot/name
        if path.stat().st_size != wanted["bytes"] or sha256_file(path) != wanted["sha256"]:
            raise ValueError("downloaded checkpoint differs: "+name)
    save_json(receipt,dict(model=CANDIDATE.model,revision=CANDIDATE.revision,
        checkpoint_files=expected,snapshot=str(snapshot),gpu_execution=False,model_weights_loaded=False))


def prepare(root, manifest, launch, scratch, output, workflow_seconds=1800):
    if output.exists() or scratch.exists():
        raise FileExistsError("fresh CPU output/scratch required; preserve prior assets")
    output.mkdir(parents=True)
    report = dict(status="blocked",gpu_execution=False,model_weights_loaded=False,weights_staged=False,root_blocker=None)
    try:
        if launch.get("stage_weights") is not True:
            raise ValueError("CPU weight staging disabled pending concrete authorization/resources")
        if not launch.get("authorization", "").strip():
            raise ValueError("concrete_course_smoke_authorization_missing")
        if (launch.get("prior_sessions_released") is not True
                or any(launch["budget"].get("prior_"+name+"_gpu_hours") is None
                       for name in ("development","setup","interruption","other_course","other_overall","smoke"))
                or launch["budget"].get("prior_smoke_attempts") is None):
            raise ValueError("prior_allocation_smoke_or_release_evidence_missing")
        count = assigned_device_count()
        assigned = bool(count or launch.get("allocated_at"))
        report.update(assigned_device_count=count,provider_assignment_utc=launch.get("allocated_at"),
            provider_release_confirmed=False)
        if count and count != 2:
            raise ValueError("selected_T4_x2_host_required")
        wall = assigned_preparation_window(launch) if assigned else None
        source_identity(root,manifest)
        if (platform.system() != "Linux" or platform.machine() != "x86_64" or sys.version_info[:2] != (3,13)):
            raise ValueError("reviewed Linux x86_64 Python 3.13 candidate required")
        scratch.mkdir(parents=True)
        tools, wheels = manifest["build_tools"],manifest["candidate_wheels"]
        weight_bytes = read(root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")["checkpoint_index"]["total_checkpoint_bytes"]
        require_space(scratch,output,4*sum(w["bytes"] for w in wheels)+weight_bytes+BUILD_RESERVE)
        env = candidate_environment(scratch)
        deadline = time.monotonic()+min(workflow_seconds,
            wall-launch["budget"]["shutdown_seconds"]-124 if assigned else workflow_seconds)
        def invoke(name,args,timeout):
            nonlocal deadline
            if assigned:
                wall = assigned_preparation_window(launch)
                deadline = min(deadline,time.monotonic()+wall-launch["budget"]["shutdown_seconds"]-124)
                timeout = min(timeout,int(deadline-time.monotonic()-EXPORT_SECONDS-8))
                if timeout < 1:
                    raise TimeoutError("assigned_preparation_deadline")
            return command(output,name,args,deadline=deadline,timeout=timeout,cwd=scratch,env=env)
        venv = scratch/"venv"
        invoke("create-candidate",[sys.executable,"-m","venv","--without-pip",venv],60)
        interpreter = venv/"bin/python"
        wheel_dir = scratch/"wheels"
        wheel_dir.mkdir()
        pip_wheel = tools["pip"]["wheels"][0]
        invoke("download-pip",[interpreter,"-I","-c",pip_wheel_download_script(pip_wheel,wheel_dir/pip_wheel["filename"])],60)
        pip_lock = scratch/"pip.lock"
        pip_lock.write_text(f"pip=={tools['pip']['version']} --hash=sha256:{pip_wheel['sha256']}\n")
        invoke("bootstrap-pip",[interpreter,"-I","-c",PIP_WHEEL_RUNNER,wheel_dir/pip_wheel["filename"],
            "--isolated","install","--no-deps","--no-index","--find-links",wheel_dir,"--require-hashes","-r",pip_lock],120)
        pip = [interpreter,"-m","pip","--isolated","--disable-pip-version-check"]
        all_files = wheels+[tools[name]["wheels"][0] | dict(name=name,version=tools[name]["version"]) for name in ("setuptools","wheel")]
        direct = scratch/"downloads.lock"
        direct.write_text("".join(f"{w['name']} @ {w['url']} --hash=sha256:{w['sha256']}\n" for w in wheels))
        invoke("download-candidate",pip+["download","--no-deps","--only-binary=:all:","--no-cache-dir",
            "--require-hashes","-r",direct,"--dest",wheel_dir],900)
        tool_downloads = scratch/"build-downloads.lock"
        tool_downloads.write_text("".join(f"{name} @ {tools[name]['wheels'][0]['url']} --hash=sha256:{tools[name]['wheels'][0]['sha256']}\n"
            for name in ("setuptools","wheel")))
        invoke("download-build-tools",pip+["download","--no-deps","--only-binary=:all:","--no-cache-dir",
            "--require-hashes","-r",tool_downloads,"--dest",wheel_dir],120)
        expanded = 0
        for item in all_files:
            path = wheel_dir/item["filename"]
            if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
                raise ValueError("pinned candidate wheel differs: "+item["filename"])
            with zipfile.ZipFile(path) as archive:
                expanded += sum(member.file_size for member in archive.infolist())
        require_space(scratch,output,expanded+weight_bytes+BUILD_RESERVE)
        install = scratch/"install.lock"
        install.write_text("".join(f"{w['name']}=={w['version']} --hash=sha256:{w['sha256']}\n" for w in wheels))
        invoke("install-candidate",pip+["install","--no-deps","--no-index","--find-links",wheel_dir,
            "--no-compile","--require-hashes","-r",install],300)
        constraints = scratch/"build-constraints.txt"
        constraints.write_text("".join(f"{name}=={tools[name]['version']}\n" for name in ("setuptools","wheel")))
        built = scratch/"built"
        built.mkdir()
        invoke("build-project",pip+["wheel","--no-deps","--no-index","--find-links",wheel_dir,
            "--build-constraint",constraints,"--wheel-dir",built,root],120)
        project_wheels = list(built.glob("*.whl"))
        if len(project_wheels) != 1:
            raise ValueError("one ordinary project wheel required")
        invoke("install-project",pip+["install","--no-deps","--no-index","--no-compile",project_wheels[0]],60)
        modules = {Path(name).name:item["sha256"] for name,item in manifest["members"].items() if name.startswith("recovery/") and name.endswith(".py")}
        versions = {w["name"]:w["version"] for w in wheels}
        probe = output/"installed.json"
        invoke("installed-provenance",[interpreter,"-I","-c",installed_probe_script(manifest,versions,probe)],30)
        installed_provenance(probe,manifest,versions)
        # Reuse the full resource calculation only inside the installed candidate;
        # the bare CPU bootstrap must not assume LangGraph/Pydantic are installed.
        launch_path = output/"launch.json"
        save_json(launch_path,launch)
        invoke("prospective-admission",[interpreter,"-I",root/"scripts/m5_course_smoke.py",
            "--root",root,"--launch",launch_path,"--output",output/"admission.json","--check-admission-only"],30)
        cache = scratch/"hub"
        env.update(HF_HUB_OFFLINE="0",TRANSFORMERS_OFFLINE="0",HF_HUB_CACHE=str(cache))
        weight_receipt = output/"weights.json"
        manifest_path = output/"source-manifest.json"
        save_json(manifest_path,manifest)
        invoke("stage-pinned-checkpoint",[interpreter,"-I",root/"scripts/m5_course_smoke_assets.py",
            "weights","--root",root,"--manifest",manifest_path,"--cache",cache,"--receipt",weight_receipt],600)
        weights = read(weight_receipt)
        assets = dict(source_commit=manifest["source_baseline_commit"],model=CANDIDATE.model,revision=CANDIDATE.revision,
            versions=versions,installed_modules=modules,checkpoint_files=weights["checkpoint_files"],
            interpreter=str(interpreter),hf_cache=str(cache),weight_staging_authorization=launch["authorization"])
        save_json(output/"prepared-assets.json",assets)
        report.update(status="prepared",weights_staged=True,assets_receipt=str(output/"prepared-assets.json"),
            interpreter=str(interpreter),hf_cache=str(cache),gpu_memory_accepted=False)
    except (Exception,KeyboardInterrupt) as error:
        report["root_blocker"] = f"{type(error).__name__}: {error}"
    finally:
        save_json(output/"report.json",report)
        print(json.dumps(export_evidence(output),indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    stage = commands.add_parser("prepare")
    for name in ("root","manifest","launch","scratch","output"):
        stage.add_argument("--"+name,type=Path,required=True)
    stage.add_argument("--workflow-seconds",type=float,default=1800)
    weights = commands.add_parser("weights")
    for name in ("root","manifest","cache","receipt"):
        weights.add_argument("--"+name,type=Path,required=True)
    args = parser.parse_args()
    if args.command == "weights":
        download_weights(args.root,read(args.manifest),args.cache,args.receipt)
    else:
        prepare(args.root.resolve(),read(args.manifest),read(args.launch),args.scratch.resolve(),args.output.resolve(),args.workflow_seconds)


if __name__ == "__main__":
    main()
