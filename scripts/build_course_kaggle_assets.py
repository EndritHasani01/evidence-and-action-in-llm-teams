"""CPU-only prefetch for a single offline Kaggle dataset; never load weights."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import Request, urlopen

if not __package__:
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    import types
    namespace = types.ModuleType("scripts")
    namespace.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules.setdefault("scripts", namespace)

from scripts.m5_course_smoke_assets import CANDIDATE, download_weights_stdlib
from scripts.m5_kaggle_preflight import PIP_WHEEL_RUNNER, sha256_file, save_json, download_native_ranges


def download_exact(item, directory):
    path = directory/item["filename"]
    if path.exists():
        if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
            raise ValueError("cached asset differs: "+path.name)
        return path
    download_native_ranges(item["url"],path,item["bytes"],item["sha256"])
    print("Verified offline wheel: "+path.name, flush=True)
    return path


def prefetch(root, manifest, cache):
    cache.mkdir(parents=True, exist_ok=True)
    wheels = cache/"wheels"
    wheels.mkdir(exist_ok=True)
    tools = manifest["build_tools"]
    items = manifest["candidate_wheels"]+[tools[name]["wheels"][0] for name in ("pip","setuptools","wheel")]
    items = list({w["filename"]:w for w in items}.values())
    missing = sum(w["bytes"] for w in items if not (wheels/w["filename"]).exists())
    # The accepted checkpoint inspection supplies its exact total before the
    # native Hub revision/LFS metadata is independently checked by the downloader.
    checkpoint = cache/"weights.json"
    if shutil.disk_usage(cache).free < missing+12*1024**3:
        raise ValueError("leave at least 12 GiB for pinned checkpoint and packaging scratch")
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda item:download_exact(item,wheels),items))
    if not checkpoint.exists():
        download_weights_stdlib(root, manifest, cache/"hub", checkpoint,range_bytes=16*1024**2)
    else:
        receipt = json.loads(checkpoint.read_bytes())
        if (receipt["model"],receipt["revision"]) != (CANDIDATE.model,CANDIDATE.revision):
            raise ValueError("cached checkpoint revision differs")
        snapshot = Path(receipt["snapshot"])
        for name, wanted in receipt["checkpoint_files"].items():
            p = snapshot/name
            if p.stat().st_size != wanted["bytes"] or sha256_file(p) != wanted["sha256"]:
                raise ValueError("cached native checkpoint differs: "+name)
    return json.loads(checkpoint.read_bytes())


def portable_members(root, manifest, cache):
    """Build a pure Python ordinary wheel; Linux installation stays a host gate."""
    weights = prefetch(root, manifest, cache)
    tools = manifest["build_tools"]
    wheels = cache/"wheels"
    staging = cache/("source-"+manifest["source_baseline_commit"])
    if staging.exists():
        raise FileExistsError("fresh source-specific build required: "+str(staging))
    staging.mkdir()
    venv = staging/"build-env"
    subprocess.run([sys.executable,"-m","venv","--without-pip",venv],check=True,timeout=60)
    python = venv/("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    pip = tools["pip"]["wheels"][0]
    pip_lock = staging/"pip.lock"
    pip_lock.write_text(f"pip=={tools['pip']['version']} --hash=sha256:{pip['sha256']}\n")
    subprocess.run([python,"-I","-c",PIP_WHEEL_RUNNER,wheels/pip["filename"],"--isolated","install",
        "--no-deps","--no-index","--find-links",wheels,"--require-hashes","-r",pip_lock],check=True,timeout=120)
    build_lock = staging/"build.lock"
    build_lock.write_text("".join(f"{name}=={tools[name]['version']} --hash=sha256:{tools[name]['wheels'][0]['sha256']}\n"
        for name in ("setuptools","wheel")))
    subprocess.run([python,"-m","pip","--isolated","install","--no-deps","--no-index",
        "--find-links",wheels,"--require-hashes","-r",build_lock],check=True,timeout=120)
    built = staging/"built"
    subprocess.run([python,"-m","pip","--isolated","wheel","--no-deps","--no-index","--no-build-isolation",
        "--wheel-dir",built,root],check=True,timeout=120)
    projects = list(built.glob("*-py3-none-any.whl"))
    if len(projects) != 1:
        raise ValueError("one ordinary platform-independent project wheel required")
    import zipfile
    modules = {str(Path(name).relative_to("recovery")).replace("\\","/"):v["sha256"] for name,v in manifest["members"].items()
               if name.startswith("recovery/") and name.endswith(".py")}
    import hashlib
    with zipfile.ZipFile(projects[0]) as project:
        for name, digest in modules.items():
            if hashlib.sha256(project.read("recovery/"+name)).hexdigest() != digest:
                raise ValueError("built ordinary module differs: "+name)
    assets = dict(source_commit=manifest["source_baseline_commit"], model=CANDIDATE.model,revision=CANDIDATE.revision,
        versions={w["name"]:w["version"] for w in manifest["candidate_wheels"]},installed_modules=modules,
        checkpoint_files=weights["checkpoint_files"],interpreter=None,hf_cache=weights["snapshot"],
        weight_staging_authorization="user-requested offline dataset packaging; CPU download only",
        installation_verified=False, model_weights_loaded=False, gpu_execution=False,
        note="Native pinned assets. Ordinary Linux install/provenance and GPU acceptance are checked on Kaggle.")
    receipt = staging/"prepared-assets.json"
    save_json(receipt,assets)
    install = staging/"install.lock"
    install.write_text("".join(f"{w['name']}=={w['version']} --hash=sha256:{w['sha256']}\n" for w in manifest["candidate_wheels"]))
    constraints = staging/"build-constraints.txt"
    constraints.write_text("".join(f"{name}=={tools[name]['version']}\n" for name in ("setuptools","wheel")))
    members = {"prepared-assets.json":receipt,"pip.lock":pip_lock,"install.lock":install,"build-constraints.txt":constraints,
               "built/"+projects[0].name:projects[0]}
    for original, exported in (("LICENSE","LICENSE"),("README.md","MODEL_CARD.md")):
        target = staging/exported
        with urlopen(f"https://huggingface.co/{CANDIDATE.model}/resolve/{CANDIDATE.revision}/{original}",timeout=30) as response:
            target.write_bytes(response.read(512*1024))
        members[exported] = target
    for p in wheels.glob("*.whl"):
        members["wheels/"+p.name] = p
    for name in weights["checkpoint_files"]:
        members["checkpoint/"+name] = Path(weights["snapshot"])/name
    return members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root","manifest","cache"):
        parser.add_argument("--"+name,type=Path,required=True)
    args = parser.parse_args()
    receipt = prefetch(args.root,json.loads(args.manifest.read_bytes()),args.cache)
    print(json.dumps(dict(gpu_execution=False,model_weights_loaded=False,checkpoint_files=len(receipt["checkpoint_files"])),indent=2))


if __name__ == "__main__":
    main()
