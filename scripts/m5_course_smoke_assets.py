"""Bounded online preparation and native verification of the pinned candidate."""

import argparse
import hashlib
import importlib.metadata
import json
import gzip
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

from scripts.m5_kaggle_preflight import (PIP_WHEEL_RUNNER, BUILD_RESERVE, EXPORT_SECONDS,
    candidate_environment, command, export_evidence, assigned_preparation_window, source_identity, installed_probe_script,
    installed_provenance, pip_wheel_download_script, require_space, save_json, sha256_file, utc)


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if str(path).endswith(".gz") else data)


def assigned_device_count():
    devices = Path("/proc/driver/nvidia/gpus")
    return len(list(devices.iterdir())) if devices.is_dir() else 0


def cpu_candidate_wheels(manifest):
    """Same pinned tokenizer/rendering/core dependencies, without GPU libraries."""
    excluded = {"torch","triton","bitsandbytes","accelerate","cuda-bindings","cuda-pathfinder","cuda-toolkit"}
    return [w for w in manifest["candidate_wheels"]
        if w["name"] not in excluded and not w["name"].startswith("nvidia-")]


def verify_assets(root, launch):
    from scripts.m5_course_preparation import CANDIDATE
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
    from scripts.m5_course_preparation import CANDIDATE
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


def download_weights_stdlib(root, manifest, cache, receipt, *, range_bytes=None):
    """Download-only native LFS verification, without importing inference packages."""
    from urllib.request import Request, urlopen
    inspection = read(root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
    model, revision = inspection["model"], inspection["revision"]
    with urlopen(Request(f"https://huggingface.co/api/models/{model}/revision/{revision}?blobs=true",
            headers={"User-Agent":"recovery-course-asset-preparation"}),timeout=30) as response:
        info = json.load(response)
    if info.get("sha") != revision:
        raise ValueError("immutable checkpoint revision differs")
    files = {s["rfilename"]:s for s in info["siblings"]}
    expected = {}
    snapshot = cache/("models--"+model.replace("/","--"))/"snapshots"/revision
    snapshot.mkdir(parents=True,exist_ok=range_bytes is not None)
    ranged = []
    for name in inspection["checkpoint_index"]["shard_files"]:
        lfs = files[name].get("lfs",{})
        if not re.fullmatch("[0-9a-f]{64}",lfs.get("sha256","")) or type(lfs.get("size")) is not int:
            raise ValueError("checkpoint shard lacks native LFS identity")
        expected[name] = dict(bytes=lfs["size"],sha256=lfs["sha256"])
        if range_bytes is not None:
            ranged.append((name,lfs))
            continue
        temporary = snapshot/(name+".partial")
        with urlopen(Request(f"https://huggingface.co/{model}/resolve/{revision}/{name}",
                headers={"User-Agent":"recovery-course-asset-preparation"}),timeout=60) as response, temporary.open("xb") as output:
            while block := response.read(1024*1024):
                output.write(block)
        if temporary.stat().st_size != lfs["size"] or sha256_file(temporary) != lfs["sha256"]:
            raise ValueError("downloaded checkpoint differs: "+name)
        temporary.replace(snapshot/name)
    if ranged:
        from concurrent.futures import ThreadPoolExecutor
        from scripts.m5_kaggle_preflight import download_native_ranges
        def fetch(item):
            name,lfs=item
            target=snapshot/name
            if target.exists():
                if target.stat().st_size != lfs["size"] or sha256_file(target) != lfs["sha256"]:
                    raise ValueError("cached checkpoint differs: "+name)
            else:
                download_native_ranges(f"https://huggingface.co/{model}/resolve/{revision}/{name}",
                    target,lfs["size"],lfs["sha256"],chunk_bytes=range_bytes)
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(fetch,ranged))
    for path,wanted in manifest["members"].items():
        if path.startswith("metadata/4B/"):
            import shutil
            name = Path(path).name
            shutil.copyfile(root/path,snapshot/name)
            if (snapshot/name).stat().st_size != wanted["bytes"] or sha256_file(snapshot/name) != wanted["sha256"]:
                raise ValueError("pinned metadata differs: "+name)
            expected[name] = wanted
    save_json(receipt,dict(model=model,revision=revision,
        checkpoint_files=expected,snapshot=str(snapshot),gpu_execution=False,model_weights_loaded=False,
        download_path="stdlib HTTPS; native revision/LFS identities; no weight conversion"))


def prepare(root, manifest, launch, scratch, output, workflow_seconds=1800, *, portable_assets=False,
        online_config=None, smoke_required=True, cpu_only=False):
    if output.exists() or scratch.exists():
        raise FileExistsError("fresh CPU output/scratch required; preserve prior assets")
    output.mkdir(parents=True)
    report = dict(status="blocked",gpu_execution=False,model_weights_loaded=False,weights_staged=False,root_blocker=None)
    try:
        if not cpu_only and launch.get("stage_weights") is not True:
            raise ValueError("CPU weight staging disabled pending concrete authorization/resources")
        if not cpu_only and not launch.get("authorization", "").strip():
            raise ValueError("concrete_course_smoke_authorization_missing")
        if not cpu_only and launch.get("resource_policy") != "observe" and (launch.get("prior_sessions_released") is not True
                or any(launch["budget"].get("prior_"+name+"_gpu_hours") is None
                       for name in ("development","setup","interruption","other_course","other_overall","smoke"))
                or launch["budget"].get("prior_smoke_attempts") is None):
            raise ValueError("prior_allocation_smoke_or_release_evidence_missing")
        count = assigned_device_count()
        assigned = bool(count or launch.get("allocated_at"))
        if cpu_only and assigned and launch.get("resource_policy") != "observe":
            raise ValueError("CPU analysis installation requires Accelerator None")
        if portable_assets and assigned:
            raise ValueError("portable asset preparation requires Accelerator None")
        report.update(assigned_device_count=count,provider_assignment_utc=launch.get("allocated_at"),
            provider_release_confirmed=False)
        if count and count != 2:
            raise ValueError("selected_T4_x2_host_required")
        wall = assigned_preparation_window(launch,smoke_required=smoke_required) if assigned else None
        source_identity(root,manifest)
        if (platform.system() != "Linux" or platform.machine() != "x86_64" or sys.version_info[:2] != (3,13)):
            raise ValueError("reviewed Linux x86_64 Python 3.13 candidate required")
        scratch.mkdir(parents=True)
        tools = manifest["build_tools"]
        wheels = cpu_candidate_wheels(manifest) if cpu_only else manifest["candidate_wheels"]
        inspection = read(root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
        weight_bytes = inspection["checkpoint_index"]["total_checkpoint_bytes"]
        online = online_config is not None or cpu_only
        require_space(scratch,output,(sum(w["bytes"] for w in wheels)+BUILD_RESERVE if portable_assets or online else
            4*sum(w["bytes"] for w in wheels)+weight_bytes+BUILD_RESERVE))
        env = candidate_environment(scratch)
        deadline = time.monotonic()+min(workflow_seconds,
            wall-launch["budget"]["shutdown_seconds"]-124 if assigned else workflow_seconds)
        def invoke(name,args,timeout):
            nonlocal deadline
            if assigned:
                wall = assigned_preparation_window(launch,smoke_required=smoke_required)
                deadline = min(deadline,time.monotonic()+wall-launch["budget"]["shutdown_seconds"]-124)
                timeout = min(timeout,int(deadline-time.monotonic()-EXPORT_SECONDS-8))
                if timeout < 1:
                    raise TimeoutError("assigned_preparation_deadline")
            return command(output,name,args,deadline=deadline,timeout=timeout,cwd=scratch,env=env,
                stream=online_config is not None)
        venv = scratch/"venv"
        invoke("create-candidate",[sys.executable,"-m","venv","--without-pip",venv],60)
        interpreter = venv/"bin/python"
        wheel_dir = scratch/"wheels"
        wheel_dir.mkdir()
        pip_wheel = tools["pip"]["wheels"][0]
        invoke("download-pip",[interpreter,"-I","-S","-c",pip_wheel_download_script(pip_wheel,wheel_dir/pip_wheel["filename"])],60)
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
        require_space(scratch,output,expanded+BUILD_RESERVE+(0 if portable_assets or online else weight_bytes))
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
        invoke("installed-provenance",[interpreter,"-I","-c",installed_probe_script(manifest,versions,probe,gpu=not cpu_only)],30)
        installed_provenance(probe,manifest,versions,gpu=not cpu_only)
        if "tests/loading_checks.py" in manifest["members"]:
            invoke("loading-contract",[interpreter,"-I","-c",
                "import sys,types,unittest; from pathlib import Path; "
                "tests=types.ModuleType('tests'); tests.__path__=[str(Path(sys.argv[1])/'tests')]; "
                "sys.modules['tests']=tests; "
                "result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromName('tests.loading_checks')); "
                "sys.exit(not result.wasSuccessful())",root],30)
        if cpu_only:
            report.update(status="prepared",interpreter=str(interpreter),assets_receipt=None,hf_cache=None,
                environment_only=True,note="Hash-pinned CPU analysis/tokenizer/rendering environment; no torch or model weights")
            return report
        # Construct every hardware row and exercise real pinned generation
        # processors on CPU before downloading weights or creating GPU workers.
        invoke("hardware-plan-contract",[interpreter,"-I",root/"scripts/m5_course_smoke.py",
            "--root",root,"--launch",root/"configs/course-smoke-launch.json",
            "--output",output/"hardware-plan-contract.json","--check-plan-only"],60)
        # Reuse the full resource calculation only inside the installed candidate;
        # the bare CPU bootstrap must not assume LangGraph/Pydantic are installed.
        launch_path = output/"launch.json"
        save_json(launch_path,launch)
        if not smoke_required:
            invoke("resume-admission",[interpreter,"-I",root/"scripts/course_kaggle_bootstrap.py","check-resume",
                "--root",root,"--scratch",scratch,"--output",output,"--config",online_config],30)
        else:
            invoke("prospective-admission",[interpreter,"-I",root/"scripts/m5_course_smoke.py",
                "--root",root,"--launch",launch_path,"--output",output/"admission.json","--check-admission-only"],30)
        if online:
            # These are fresh, hash-verified installation downloads, not inputs or
            # experiment evidence. Reclaim them before the 9.3 GB checkpoint.
            for path in wheel_dir.glob("*.whl"):
                if not path.resolve().is_relative_to(scratch.resolve()) or path.is_symlink():
                    raise ValueError("download cleanup escaped the fresh owned scratch")
                path.unlink()
        cache = Path(launch.get("hf_cache") or scratch/"hub") if online else scratch/"hub"
        if online:
            snapshot=cache/("models--"+inspection["model"].replace("/","--"))/"snapshots"/inspection["revision"]
            staged=sum(p.stat().st_size for name in inspection["checkpoint_index"].get("shard_files",())
                for p in (snapshot/name,snapshot/(name+".partial")) if p.is_file() and not p.is_symlink())
            # Reused bytes still undergo native hash/range verification below.
            # They reduce incoming disk needs, not the scientific acceptance rule.
            require_space(scratch,output,max(0,weight_bytes-staged)+BUILD_RESERVE)
        env.update(HF_HUB_OFFLINE="0",TRANSFORMERS_OFFLINE="0",HF_HUB_CACHE=str(cache))
        weight_receipt = output/"weights.json"
        manifest_path = output/"source-manifest.json"
        save_json(manifest_path,manifest)
        weight_interpreter = interpreter
        if portable_assets:
            import shutil
            if not venv.resolve().is_relative_to(scratch.resolve()) or venv.name != "venv":
                raise ValueError("setup environment escaped its fresh scratch")
            shutil.rmtree(venv)
            require_space(scratch,output,weight_bytes+BUILD_RESERVE)
            weight_interpreter = sys.executable
        invoke("stage-pinned-checkpoint",[weight_interpreter,"-I"]+(["-S"] if online or portable_assets else [])+[root/"scripts/m5_course_smoke_assets.py",
            "weights","--root",root,"--manifest",manifest_path,"--cache",cache,"--receipt",weight_receipt]+
            (["--stdlib","--range-bytes",str(16*1024**2)] if online else ["--stdlib"] if portable_assets else []),600)
        weights = read(weight_receipt)
        assets = dict(source_commit=manifest["source_baseline_commit"],model=inspection["model"],revision=inspection["revision"],
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
    weights.add_argument("--stdlib",action="store_true")
    weights.add_argument("--range-bytes",type=int)
    for name in ("root","manifest","cache","receipt"):
        weights.add_argument("--"+name,type=Path,required=True)
    args = parser.parse_args()
    if args.command == "weights":
        if args.stdlib:
            download_weights_stdlib(args.root,read(args.manifest),args.cache,args.receipt,range_bytes=args.range_bytes)
        else:
            download_weights(args.root,read(args.manifest),args.cache,args.receipt)
    else:
        prepare(args.root.resolve(),read(args.manifest),read(args.launch),args.scratch.resolve(),args.output.resolve(),args.workflow_seconds)


if __name__ == "__main__":
    main()
