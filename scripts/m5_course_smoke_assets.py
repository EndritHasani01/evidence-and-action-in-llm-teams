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
import shutil
import subprocess
import sys
import tempfile
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


def inspection_path(root, label=None):
    if label is not None:
        if label not in ("9B", "4B"):
            raise ValueError("unreviewed course candidate")
        return Path(root)/"notebooks/validation/course-kaggle/repair-candidates"/label/"inspection.json"
    return Path(root)/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json"


def metadata_members(manifest, model):
    result = {Path(p).name:(p,v) for p,v in manifest["members"].items() if p.startswith("metadata/4B/")}
    if model.endswith("-9B"):
        result.update({Path(p).name:(p,v) for p,v in manifest["members"].items() if p.startswith("metadata/9B/")})
    return result


def native_checkpoint_files(inspection):
    """Small immutable Hub metadata; never download or load a tensor here."""
    from urllib.request import Request, urlopen
    model, revision = inspection['model'], inspection['revision']
    with urlopen(Request(f"https://huggingface.co/api/models/{model}/revision/{revision}?blobs=true",
            headers={'User-Agent':'recovery-course-asset-preparation'}),timeout=30) as response:
        info = json.load(response)
    if info.get('sha') != revision:
        raise ValueError('immutable checkpoint revision differs')
    files = {s['rfilename']:s for s in info['siblings']}
    expected = {}
    for name in inspection['checkpoint_index']['shard_files']:
        lfs = files[name].get('lfs',{})
        if not re.fullmatch('[0-9a-f]{64}',lfs.get('sha256','')) or type(lfs.get('size')) is not int:
            raise ValueError('checkpoint shard lacks native LFS identity')
        expected[name] = dict(bytes=lfs['size'],sha256=lfs['sha256'])
    if sum(v['bytes'] for v in expected.values()) != inspection['checkpoint_index']['total_checkpoint_bytes']:
        raise ValueError('pinned checkpoint byte inventory differs')
    return expected


def checkpoint_pending(cache, inspection, expected, manifest):
    """Credit only the one representation the native downloader will use."""
    cache = Path(cache)
    snapshot = cache/('models--'+inspection['model'].replace('/','--'))/'snapshots'/inspection['revision']
    pending, rows = 0, []
    for name,wanted in expected.items():
        final, partial = snapshot/name, snapshot/(name+'.partial')
        if any(p.is_symlink() for p in (final,partial,snapshot,snapshot.parent,snapshot.parent.parent,cache)):
            raise ValueError('checkpoint cache contains a symlink')
        if final.exists():
            if not final.is_file() or final.stat().st_size != wanted['bytes'] or sha256_file(final) != wanted['sha256']:
                raise ValueError('native cached asset identity differs: '+name)
            remaining = 0
        elif partial.exists():
            if not partial.is_file() or partial.stat().st_size > wanted['bytes']:
                raise ValueError('partial asset is larger than its pinned native size: '+name)
            remaining = wanted['bytes']-partial.stat().st_size
        else:
            remaining = wanted['bytes']
        pending += remaining
        rows.append(dict(file=name,bytes=wanted['bytes'],remaining_bytes=remaining))
    for name,(_,wanted) in metadata_members(manifest,inspection['model']).items():
        path = snapshot/name
        if path.is_symlink():
            raise ValueError('checkpoint metadata contains a symlink')
        if path.exists():
            if not path.is_file() or path.stat().st_size != wanted['bytes'] or sha256_file(path) != wanted['sha256']:
                raise ValueError('native cached metadata identity differs: '+name)
        else:
            pending += wanted['bytes']
    return dict(snapshot=str(snapshot),remaining_bytes=pending,shards=rows)


def storage_locations(requested, output):
    requested, output = Path(requested), Path(output)
    workspace = output.parent.parent
    options = [Path('/kaggle/temp')/workspace.name/output.parent.name/'scratch',
               Path('/tmp')/workspace.name/output.parent.name/'scratch', requested]
    return list(dict.fromkeys(options)) if str(workspace).startswith('/kaggle/working/') else [requested]


def select_online_storage(requested, output, manifest, inspection, expected, launch, wheels):
    """Two ordinary temporary roots, then the requested path; observe every pool."""
    workspace = Path(output).parent.parent
    options = storage_locations(requested,output)
    preferred = Path(launch['hf_cache']) if launch.get('hf_cache') else None
    choices = [(path,preferred or path/'hub') for path in options]
    if preferred:
        choices += [(path,path/'hub') for path in options if path/'hub' != preferred]
    receipt = dict(source_commit=manifest['source_baseline_commit'],attempts=[],estimate=True,
                   rule='Peak of wheel download plus estimated expansion, or installed environment plus incoming checkpoint')
    for path,chosen_cache in choices:
        cache = None
        try:
            if path.is_symlink() or path.parent.is_symlink() or path.parent.parent.is_symlink():
                raise ValueError('scratch path contains a symlink')
            if path.is_relative_to(workspace/'bundle'):
                raise ValueError('scratch must be outside the experiment backup tree')
            marker = path/'SOURCE_COMMIT.txt'
            if path.exists() and (not marker.is_file() or marker.read_text().strip() != manifest['source_baseline_commit']):
                raise ValueError('existing scratch is not owned by this source')
            path.mkdir(parents=True,exist_ok=True)
            marker.write_text(manifest['source_baseline_commit']+'\n')
            cache = chosen_cache
            if cache.is_symlink():
                raise ValueError('cache path is a symlink')
            cache.mkdir(parents=True,exist_ok=True)
            for writable in (path,cache):
                with tempfile.TemporaryFile(dir=writable) as stream:
                    stream.write(b'course storage probe')
            pending = checkpoint_pending(cache,inspection,expected,manifest)['remaining_bytes']
            download = sum(w['bytes'] for w in wheels)
            expansion = 4*download  # Existing conservative allowance, not a proven quota bound.
            same = path.stat().st_dev == cache.stat().st_dev
            required = max(download+expansion,expansion+pending) if same else download+expansion
            facts = require_space(path,output,required+BUILD_RESERVE,
                                  receipt=output/'storage-location.json',stage='early-install-and-checkpoint')
            cache_facts = require_space(cache,output,(required if same else pending)+BUILD_RESERVE,
                                  receipt=output/'storage-cache-location.json',stage='early-checkpoint-cache')
            receipt['attempts'].append(dict(path=str(path),cache=str(cache),status='selected',
                                            storage=facts,cache_storage=cache_facts))
            save_json(output/'storage-selection.json',receipt)
            print(f"Setup storage: {path} | checkpoint cache: {cache}",flush=True)
            return path,cache
        except (OSError,ValueError) as error:
            # Capture facts on refusal too; a large UI total does not substitute for this path.
            from scripts.m5_kaggle_preflight import filesystem_facts
            facts = filesystem_facts({'scratch':path,'output':output}) if path.is_dir() else None
            receipt['attempts'].append(dict(path=str(path),status='refused',reason=str(error),storage=facts,
                cache_storage=filesystem_facts({'cache':cache,'output':output})
                    if cache is not None and cache.is_dir() else None))
            save_json(output/'storage-selection.json',receipt)
            if any(code in str(error) for code in ('native cached asset identity','native cached metadata identity',
                                                   'partial asset is larger','checkpoint cache contains a symlink')):
                raise  # Integrity faults are retained failures, not an excuse to choose different assets.
    raise ValueError('no_suitable_session_storage: '+receipt['attempts'][-1]['reason'])


def reclaim_installation(scratch, source_commit):
    """Discard only a source-owned, inactive installation; keep hub and receipts."""
    scratch = Path(scratch)
    if scratch.is_symlink() or (scratch/'SOURCE_COMMIT.txt').read_text().strip() != source_commit:
        raise ValueError('installation cleanup requires owned scratch')
    for name in ('venv','wheels','built','tmp'):
        path = scratch/name
        if path.is_symlink() or not path.resolve().is_relative_to(scratch.resolve()):
            raise ValueError('installation cleanup escaped owned scratch')
        if path.exists():
            shutil.rmtree(path)


def admit_checkpoint(cache, output, inspection, expected, manifest, *, retired_assets=None, retired_workers=()):
    """Share exact cache admission across initial, resumed and fallback staging."""
    cache = Path(cache)
    cache.mkdir(parents=True,exist_ok=True)
    pending = checkpoint_pending(cache,inspection,expected,manifest)
    save_json(output/'checkpoint-pending.json',pending)
    try:
        return require_space(cache,output,pending['remaining_bytes']+BUILD_RESERVE,
                             receipt=output/'storage-checkpoint.json',stage='checkpoint-cache')
    except ValueError as error:
        if not str(error).startswith('scratch_capacity:') or not retired_assets:
            raise
        if inspection['model'] != 'Qwen/Qwen3.5-4B' or retired_assets['model'] != 'Qwen/Qwen3.5-9B':
            raise ValueError('only the declared retired 9B cache can be reclaimed for 4B') from error
        if retired_assets.get('source_commit') != manifest['source_baseline_commit']:
            raise ValueError('retired cache source differs') from error
        if not re.fullmatch('[0-9a-f]{40}',retired_assets.get('revision','')):
            raise ValueError('retired checkpoint revision is not an immutable commit') from error
        import sqlite3
        from contextlib import closing
        for path in retired_workers:
            with closing(sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True)) as db:
                if db.execute('SELECT COUNT(*) FROM provider_processes WHERE stopped_at IS NULL OR uncertain_stop=1').fetchone()[0]:
                    raise ValueError('retired candidate is not confirmed quiescent') from error
        marker = cache.parent/'SOURCE_COMMIT.txt'
        if marker.is_symlink() or not marker.is_file() or marker.read_text().strip() != manifest['source_baseline_commit']:
            raise ValueError('cache reclamation requires package-owned scratch') from error
        snapshot = cache/('models--'+retired_assets['model'].replace('/','--'))/'snapshots'/retired_assets['revision']
        if not snapshot.resolve().is_relative_to(cache.resolve()) or any(p.is_symlink() for p in
                (cache,cache.parent,snapshot,snapshot.parent,snapshot.parent.parent)):
            raise ValueError('checkpoint cleanup escaped owned cache') from error
        allowed = set(retired_assets['checkpoint_files'])
        if not snapshot.is_dir() or any(p.is_symlink() or not p.is_file() or
                p.name.removesuffix('.partial') not in allowed for p in snapshot.iterdir()):
            raise ValueError('retired snapshot contains unowned files') from error
        save_json(output/'checkpoint-cache-reclaimed.json',dict(snapshot=str(snapshot),
            asset_evidence=retired_assets,reason=str(error),scientific_artifacts_deleted=False))
        shutil.rmtree(snapshot)
        return require_space(cache,output,pending['remaining_bytes']+BUILD_RESERVE,
                             receipt=output/'storage-checkpoint-after-reclaim.json',stage='fallback-after-cache-reclaim')


def verify_assets(root, launch):
    manifest, assets = read(launch["source_manifest"]), read(launch["assets_receipt"])
    source_identity(root,manifest)
    if assets["source_commit"] != manifest["source_baseline_commit"]:
        raise ValueError("CPU assets belong to a different committed source")
    label = launch.get("candidate") or ("9B" if assets["model"].endswith("-9B") else None)
    if label is None:
        from scripts.m5_course_preparation import CANDIDATE
        inspection = dict(model=CANDIDATE.model,revision=CANDIDATE.revision)
    else:
        inspection = read(inspection_path(root,label))
    if (assets["model"],assets["revision"]) != (inspection["model"],inspection["revision"]):
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
    snapshot = cache/("models--"+inspection["model"].replace("/","--"))/"snapshots"/inspection["revision"]
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


def download_weights_stdlib(root, manifest, cache, receipt, *, range_bytes=None, candidate=None):
    """Download-only native LFS verification, without importing inference packages."""
    from urllib.request import Request, urlopen
    inspection = read(inspection_path(root,candidate))
    model, revision = inspection["model"], inspection["revision"]
    expected = native_checkpoint_files(inspection)
    snapshot = cache/("models--"+model.replace("/","--"))/"snapshots"/revision
    snapshot.mkdir(parents=True,exist_ok=range_bytes is not None)
    ranged = []
    for name in inspection["checkpoint_index"]["shard_files"]:
        wanted = expected[name]
        lfs = dict(size=wanted['bytes'],sha256=wanted['sha256'])
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
    import shutil
    for name,(path,wanted) in metadata_members(manifest,model).items():
        if not (snapshot/name).exists():
            shutil.copyfile(root/path,snapshot/name)
        if (snapshot/name).stat().st_size != wanted["bytes"] or sha256_file(snapshot/name) != wanted["sha256"]:
            raise ValueError("pinned metadata differs: "+name)
        expected[name] = wanted
    save_json(receipt,dict(model=model,revision=revision,
        checkpoint_files=expected,snapshot=str(snapshot),gpu_execution=False,model_weights_loaded=False,
        download_path="stdlib HTTPS; native revision/LFS identities; no weight conversion"))


def prepare(root, manifest, launch, scratch, output, workflow_seconds=1800, *, portable_assets=False,
        online_config=None, smoke_required=True, cpu_only=False):
    automatic = online_config is not None and launch.get("resource_policy") == "observe"
    if output.exists() or (scratch.exists() and not automatic):
        raise FileExistsError("fresh CPU output/scratch required; preserve prior assets")
    output.mkdir(parents=True)
    report = dict(status="blocked",gpu_execution=False,model_weights_loaded=False,weights_staged=False,
        root_blocker=None,source_commit=manifest["source_baseline_commit"],installed_verified=False,
        stage="authorization",scratch=str(scratch),interpreter=None,hf_cache=None)
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
        tools = manifest["build_tools"]
        wheels = cpu_candidate_wheels(manifest) if cpu_only else manifest["candidate_wheels"]
        inspection = read(inspection_path(root,launch.get("candidate")))
        weight_bytes = inspection["checkpoint_index"]["total_checkpoint_bytes"]
        online = online_config is not None or cpu_only
        report["stage"] = "storage-selection"
        expected = native_checkpoint_files(inspection) if automatic else None
        resume_path = launch.get("setup_resume_report")
        previous = read(resume_path) if automatic and resume_path and Path(resume_path).is_file() else {}
        if previous and previous.get("source_commit") != manifest["source_baseline_commit"]:
            raise ValueError("setup resume source differs")
        reusable = bool(previous.get("installed_verified") and
                        Path(previous.get("interpreter") or "/missing").is_file())
        if reusable:
            scratch = Path(previous["scratch"])
            marker = scratch/"SOURCE_COMMIT.txt"
            if (scratch not in storage_locations(Path(report['scratch']),output) or scratch.is_symlink()
                    or marker.is_symlink() or marker.read_text().strip() != manifest["source_baseline_commit"]):
                raise ValueError("saved installation is not source-owned")
            cache = Path(launch.get("hf_cache") or previous["hf_cache"])
            cache.mkdir(parents=True,exist_ok=True)
        elif automatic:
            scratch,cache = select_online_storage(scratch,output,manifest,inspection,expected,launch,wheels)
            if any((scratch/name).exists() for name in ('venv','wheels','built','tmp')):
                reclaim_installation(scratch,manifest["source_baseline_commit"])
        else:
            scratch.mkdir(parents=True)
            cache = Path(launch.get("hf_cache") or scratch/"hub") if online else scratch/"hub"
            require_space(scratch,output,(sum(w["bytes"] for w in wheels)+BUILD_RESERVE if portable_assets or online else
                4*sum(w["bytes"] for w in wheels)+weight_bytes+BUILD_RESERVE),
                receipt=output/"storage-initial.json",stage="initial")
        report.update(scratch=str(scratch),hf_cache=str(cache),interpreter=str(scratch/"venv/bin/python"),
                      reused_installation=reusable)
        if expected is not None:
            save_json(output/"native-checkpoint.json",expected)
        env = candidate_environment(scratch)
        deadline = time.monotonic()+min(workflow_seconds,
            wall-launch["budget"]["shutdown_seconds"]-124 if assigned else workflow_seconds)
        def invoke(name,args,timeout):
            nonlocal deadline
            report["stage"] = name
            save_json(output/"report.json",report)
            if assigned:
                wall = assigned_preparation_window(launch,smoke_required=smoke_required)
                deadline = min(deadline,time.monotonic()+wall-launch["budget"]["shutdown_seconds"]-124)
                timeout = min(timeout,int(deadline-time.monotonic()-EXPORT_SECONDS-8))
                if timeout < 1:
                    raise TimeoutError("assigned_preparation_deadline")
            return command(output,name,args,deadline=deadline,timeout=timeout,cwd=scratch,env=env,
                stream=online_config is not None)
        venv = scratch/"venv"
        interpreter = venv/"bin/python"
        wheel_dir = scratch/"wheels"
        versions = {w["name"]:w["version"] for w in wheels}
        modules = {Path(name).name:item["sha256"] for name,item in manifest["members"].items()
                   if name.startswith("recovery/") and name.endswith(".py")}
        probe = output/"installed.json"
        if reusable:
            print("Setup: verifying the completed installation; dependency install is not repeated",flush=True)
            try:
                invoke("reused-installed-provenance",[interpreter,"-I","-c",
                    installed_probe_script(manifest,versions,probe,gpu=not cpu_only)],30)
                installed_provenance(probe,manifest,versions,gpu=not cpu_only)
            except Exception as error:
                save_json(output/"installation-reuse-refused.json",dict(reason=str(error)))
                reclaim_installation(scratch,manifest["source_baseline_commit"])
                env = candidate_environment(scratch)
                reusable = False
                report["reused_installation"] = False
        if not reusable:
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
            incoming = checkpoint_pending(cache,inspection,expected,manifest)["remaining_bytes"] if automatic else weight_bytes
            shared_cache = automatic and scratch.stat().st_dev == cache.stat().st_dev
            require_space(scratch,output,expanded+BUILD_RESERVE+(incoming if shared_cache or not (portable_assets or online) else 0),
                receipt=output/"storage-install.json",stage="expanded-installation-and-checkpoint")
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
        report["installed_verified"] = True
        save_json(output/"report.json",report)
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
        launch_path = output/"launch.json"
        save_json(launch_path,launch)
        invoke("hardware-plan-contract",[interpreter,"-I",root/"scripts/m5_course_smoke.py",
            "--root",root,"--launch",launch_path,
            "--output",output/"hardware-plan-contract.json","--check-plan-only"],60)
        # Reuse the full resource calculation only inside the installed candidate;
        # the bare CPU bootstrap must not assume LangGraph/Pydantic are installed.
        if not smoke_required:
            invoke("resume-admission",[interpreter,"-I",root/"scripts/course_kaggle_bootstrap.py","check-resume",
                "--root",root,"--scratch",scratch,"--output",output,"--config",online_config],30)
        else:
            invoke("prospective-admission",[interpreter,"-I",root/"scripts/m5_course_smoke.py",
                "--root",root,"--launch",launch_path,"--output",output/"admission.json","--check-admission-only"],30)
        if online:
            # These are fresh, hash-verified installation downloads, not inputs or
            # experiment evidence. Reclaim them before the pinned checkpoint.
            for path in wheel_dir.glob("*.whl"):
                if not path.resolve().is_relative_to(scratch.resolve()) or path.is_symlink():
                    raise ValueError("download cleanup escaped the fresh owned scratch")
                path.unlink()
        if online:
            cache.mkdir(parents=True,exist_ok=True)
            if expected is None and inspection["checkpoint_index"].get("shard_files"):
                expected = native_checkpoint_files(inspection)
            pending = checkpoint_pending(cache,inspection,expected,manifest) if expected is not None else dict(remaining_bytes=weight_bytes)
            save_json(output/"checkpoint-pending.json",pending)
            report["stage"] = "checkpoint-capacity"
            if expected is not None:
                try:
                    admit_checkpoint(cache,output,inspection,expected,manifest,
                        retired_assets=launch.get('retired_assets'),retired_workers=launch.get('retired_workers',()))
                except ValueError as error:
                    if not automatic or not str(error).startswith('scratch_capacity:'):
                        raise
                    # Keep the verified interpreter, trying another measured cache
                    # pool before any model attempt. Old caches/evidence remain.
                    _,cache = select_online_storage(Path(report['scratch']),output,manifest,inspection,expected,
                        dict(launch,hf_cache=str(cache)),[])
                    report['hf_cache'] = str(cache)
                    admit_checkpoint(cache,output,inspection,expected,manifest)
            else:
                require_space(cache,output,pending["remaining_bytes"]+BUILD_RESERVE,
                    receipt=output/"storage-checkpoint.json",stage="checkpoint-cache")
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
            (["--stdlib","--range-bytes",str(16*1024**2)] if online else ["--stdlib"] if portable_assets else [])+
            (["--candidate",launch["candidate"]] if launch.get("candidate") else []),900)
        weights = read(weight_receipt)
        assets = dict(source_commit=manifest["source_baseline_commit"],model=inspection["model"],revision=inspection["revision"],
            versions=versions,installed_modules=modules,checkpoint_files=weights["checkpoint_files"],
            interpreter=str(interpreter),hf_cache=str(cache),weight_staging_authorization=launch["authorization"])
        save_json(output/"prepared-assets.json",assets)
        report.update(status="prepared",stage="complete",weights_staged=True,assets_receipt=str(output/"prepared-assets.json"),
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
    weights.add_argument("--candidate",choices=("9B","4B"))
    args = parser.parse_args()
    if args.command == "weights":
        if args.stdlib:
            download_weights_stdlib(args.root,read(args.manifest),args.cache,args.receipt,range_bytes=args.range_bytes,candidate=args.candidate)
        else:
            download_weights(args.root,read(args.manifest),args.cache,args.receipt)
    else:
        prepare(args.root.resolve(),read(args.manifest),read(args.launch),args.scratch.resolve(),args.output.resolve(),args.workflow_seconds)


if __name__ == "__main__":
    main()
