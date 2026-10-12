"""Stdlib-only Kaggle setup and offline restoration of the pinned candidate.

Use the existing CPU asset builder. Model weights and target wheels are optional
operator-authorized downloads, kept in a separate reusable assets ZIP.
No imports in this module initialize CUDA or load a model.
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

if not __package__:
    import types
    namespace = types.ModuleType("scripts")
    namespace.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules.setdefault("scripts", namespace)

from scripts.m5_kaggle_preflight import (PIP_WHEEL_RUNNER, sha256_file, save_json,
    candidate_environment, command, EXPORT_SECONDS, utc)


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


def restore(root, assets_zip, scratch, output, *, seconds=1800):
    if platform.system() != "Linux" or platform.machine() != "x86_64" or sys.version_info[:2] != (3,13):
        raise ValueError("Pinned candidate requires Linux x86_64 Python 3.13; changing it reopens host acceptance")
    manifest = json.loads((root/"source-manifest.json").read_bytes())
    from scripts.m5_course_smoke_assets import source_identity
    source_identity(root, manifest)
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
    parser.add_argument("action", choices=("setup", "restore", "cpu"))
    for name in ("root", "scratch", "output"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--assets", type=Path)
    args = parser.parse_args()
    root, scratch, output = args.root.resolve(), args.scratch.resolve(), args.output.resolve()
    try:
        if args.action == "setup":
            if not args.config:
                raise ValueError("setup requires configuration")
            result = setup(root, json.loads(args.config.read_bytes()), scratch, output)
        elif args.action == "restore":
            if not args.assets:
                raise ValueError("restore requires the portable assets ZIP")
            result = restore(root, args.assets, scratch, output)
        else:
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
