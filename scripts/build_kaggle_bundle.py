"""Preserve the canonical M5 archive under the tested raw-payload suffix."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import tomllib
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import zipfile


BASELINE_COMMIT = "ca46bcd55486b38bb453f5294e01f943bc7f7752"
SOURCE_ARCHIVE_SHA256 = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
PAYLOAD_NAME = "m5-kaggle-source.payload"
CHUNK = 1024 * 1024


def candidate_files(path: Path) -> list[dict]:
    """Use uv's target-specific wheel selection, not a home-grown wheel tag resolver."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    result = []
    for package in data["packages"]:
        wheels = package.get("wheels", [])
        if not wheels:
            raise ValueError(f"candidate_requires_target_wheel: {package['name']}")
        # uv has already restricted these to the target; pin one reproducibly.
        wheel = min(wheels, key=lambda p: Path(unquote(urlsplit(p['url']).path)).name)
        url = urlsplit(wheel["url"])
        if url.scheme != "https" or url.hostname not in {
                "files.pythonhosted.org", "download.pytorch.org", "download-r2.pytorch.org"}:
            raise ValueError(f"candidate_wheel_origin: {package['name']}")
        size = wheel.get("size")
        if size is None:
            request = Request(wheel["url"], headers={"Range": "bytes=0-0", "User-Agent": "uv/0.11.6"})
            # Read headers only; some official CDN endpoints reject ordinary HEAD.
            with urlopen(request, timeout=20) as response:
                content_range = response.headers.get("Content-Range")
                size = int(content_range.rsplit("/", 1)[1] if content_range else response.headers["Content-Length"])
        if not isinstance(size, int) or size <= 0:
            raise ValueError(f"candidate_wheel_size: {package['name']}")
        if re.fullmatch(r'[0-9a-f]{64}',wheel['hashes']['sha256']) is None:
            raise ValueError(f"candidate_wheel_hash: {package['name']}")
        result.append({"name": package["name"], "version": package["version"],
                       "url": wheel["url"], "filename": Path(unquote(url.path)).name,
                       "bytes": size, "sha256": wheel["hashes"]["sha256"]})
    return result


def candidate_lock(files: list[dict]) -> str:
    return "".join(f"{p['name']}=={p['version']} --hash=sha256:{p['sha256']}\n" for p in files)


def file_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def archive_manifest(path: Path) -> dict:
    members = {}
    with zipfile.ZipFile(path) as archive:
        for entry in archive.infolist():
            # orig_filename retains separators/NULs hidden by ZipInfo on Windows.
            name = entry.orig_filename
            if (not name or name != entry.filename or "\\" in name or ":" in name
                    or name.startswith("/") or any(ord(char) < 32 for char in name)
                    or any(part in {"", ".", ".."} for part in name.split("/"))
                    or stat.S_ISLNK(entry.external_attr >> 16) or entry.is_dir()):
                raise ValueError(f"unsafe_source_member: {name}")
            if name in members:
                raise ValueError(f"duplicate_source_member: {name}")
            for parent in PurePosixPath(name).parents:
                if str(parent) in members:
                    raise ValueError(f"conflicting_source_member: {name}")
            if any(other.startswith(name + "/") for other in members):
                raise ValueError(f"conflicting_source_member: {name}")
            digest, size = hashlib.sha256(), 0
            with archive.open(entry) as stream:
                while data := stream.read(CHUNK):
                    digest.update(data)
                    size += len(data)
            if size != entry.file_size:
                raise ValueError(f"source_member_size: {name}")
            members[name] = {"bytes": size, "sha256": digest.hexdigest()}
        marker = archive.read("SOURCE_COMMIT.txt").decode("ascii").strip()
    if marker != BASELINE_COMMIT:
        raise ValueError("source_baseline_marker")
    return {"schema_version": 1, "kind": "canonical-m5-source",
            "transport": "raw_payload", "payload_filename": PAYLOAD_NAME,
            "source_baseline_commit": BASELINE_COMMIT,
            "archive_bytes": path.stat().st_size, "archive_sha256": file_sha256(path),
            "expanded_bytes": sum(x["bytes"] for x in members.values()),
            "members": dict(sorted(members.items()))}


def build(source: Path, output: Path, build_commit: str | None = None,
          *, expected_source_hash: str = SOURCE_ARCHIVE_SHA256,
          candidate_wheels: list[dict] | None = None, build_tools: dict | None = None,
          helper: Path | None = None, notebook: Path | None = None) -> dict:
    if build_commit is not None and re.fullmatch(r"[0-9a-f]{40}", build_commit) is None:
        raise ValueError("build_commit must be a verified full Git commit or None")
    if output.exists() or (notebook is not None and notebook.exists()):
        raise FileExistsError("Use a new directory; earlier bundles/evidence are never overwritten.")
    if source.is_symlink() or not source.is_file() or file_sha256(source) != expected_source_hash:
        raise ValueError("canonical_source_archive_hash")
    manifest = archive_manifest(source)
    manifest.update(build_commit=build_commit, build_python=platform.python_version())
    if notebook is not None:
        if not candidate_wheels or not build_tools or helper is None:
            raise ValueError('notebook_requires_candidate_wheels_build_tools_and_helper')
        lock_text=candidate_lock(candidate_wheels)
        program=helper.read_text(encoding='utf-8')
        manifest.update(candidate_wheels=candidate_wheels,build_tools=build_tools,
                        candidate_lock_sha256=hashlib.sha256(lock_text.encode()).hexdigest(),
                        helper_sha256=hashlib.sha256(program.encode()).hexdigest())
        document=preparation_notebook(program,manifest,lock_text)
    output.mkdir(parents=True, exist_ok=False)
    payload = output / PAYLOAD_NAME
    shutil.copyfile(source, payload)
    if file_sha256(payload) != manifest["archive_sha256"]:
        raise ValueError("copied_payload_hash")
    (output / "source-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if notebook is not None:
        (output/'candidate-linux313.lock').write_text(lock_text,encoding='utf-8')
        notebook.parent.mkdir(parents=True,exist_ok=True)
        notebook.write_text(json.dumps(document,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
    return manifest


def preparation_notebook(program: str, expected: dict, lock_text: str) -> dict:
    def cell(kind,text,identifier):
        result={'cell_type':kind,'id':identifier,'metadata':{},'source':text.splitlines(keepends=True)}
        if kind=='code':result.update(execution_count=None,outputs=[])
        return result
    instructions='''# M5 corrected source and environment preparation — CPU

1. Create a **private Kaggle dataset** named `m5-kaggle-source-v2`. Upload only
   **`m5-kaggle-source.payload`**, preserving that filename and extension.
2. Import this notebook as a **private notebook**. Set **Accelerator: None** and
   **Internet: On**. Use Add Input to attach the new dataset. The older dataset
   is unnecessary; keeping it attached is supported for input diagnosis.
3. Select **Run All**. Defaults need no cell edits. Installation and checks may
   take several minutes; the CPU workflow has a 45-minute limit.
4. Download `preflight-results.zip` from the final cell and the executed notebook.
   Stop the session. Save both files under your local `notebooks/run/3/` and return them.

This verifies every canonical source member, stages WHEEL_GB GB of pinned CUDA wheels
on disposable scratch, creates a clean candidate venv, checks installed package
provenance, and runs 81 focused plus 16 native checks. The installed-package probe
runs separately outside the source directory. The active Kaggle kernel is unchanged.

No language weights are downloaded and no language-model generations occur.
This stage uses CPU with GPU-compatible packages. A passing result still requires
review before GPU library probes, model staging or bounded smoke. Accelerator None
is required so a cold installation cannot consume the short GPU allocation window.
Both passing checks and handled failures produce diagnostic evidence.
'''.replace('WHEEL_GB',f"{sum(p['bytes'] for p in expected['candidate_wheels'])/10**9:.2f}")
    setup=("import hashlib,json,os\nfrom pathlib import Path\n\n"
           f"PREFLIGHT_PROGRAM={program!r}\n"
           f"EXPECTED=json.loads({json.dumps(expected,sort_keys=True)!r})\n"
           f"CANDIDATE_LOCK={lock_text!r}\n"
           "assert hashlib.sha256(PREFLIGHT_PROGRAM.encode()).hexdigest()==EXPECTED['helper_sha256']\n"
           "assert hashlib.sha256(CANDIDATE_LOCK.encode()).hexdigest()==EXPECTED['candidate_lock_sha256']\n"
           "preflight_namespace={'__name__':'recovery_m5_preflight'}\n"
           "exec(compile(PREFLIGHT_PROGRAM,'m5_kaggle_preflight.py','exec'),preflight_namespace)\n")
    run=("# Overrides support controlled local validation; Kaggle defaults need no edits.\n"
         "input_root=Path(os.environ.get('M5_PREFLIGHT_INPUT_ROOT','/kaggle/input'))\n"
         "output_root=Path(os.environ.get('M5_PREFLIGHT_OUTPUT_ROOT','/kaggle/working'))\n"
         "scratch_root=Path(os.environ.get('M5_PREFLIGHT_SCRATCH_ROOT','/tmp/recovery-m5'))\n"
         "PREFLIGHT_RESULT=preflight_namespace['run_preflight'](input_root,output_root,scratch_root,EXPECTED,CANDIDATE_LOCK)\n"
         "print(json.dumps(PREFLIGHT_RESULT['summary'],indent=2))\n")
    download=("from IPython.display import FileLink,display\n\n"
              "print(PREFLIGHT_RESULT['summary']['next_action'])\n"
              "if PREFLIGHT_RESULT['zip_path']:\n"
              "    print('Result ZIP SHA-256:',PREFLIGHT_RESULT['zip_sha256'])\n"
              "    display(FileLink(os.path.relpath(PREFLIGHT_RESULT['zip_path'],Path.cwd())))\n"
              "else:\n"
              "    print('Export failed; retain completed JSON/logs in:',PREFLIGHT_RESULT['run_directory'])\n"
              "    print(PREFLIGHT_RESULT['report'].get('export_error'))\n"
              "print('Stop the Kaggle session after download. Model smoke remains unexecuted.')\n")
    return {'nbformat':4,'nbformat_minor':5,'metadata':{
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},
        'cells':[cell('markdown',instructions,'preparation-instructions'),cell('code',setup,'preparation-bootstrap'),
                 cell('markdown','## Run source, package and storage checks\n','preparation-run-title'),
                 cell('code',run,'preparation-run'),cell('markdown','## Download the evidence and stop\n','preparation-export-title'),
                 cell('code',download,'preparation-export')]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--build-commit")
    parser.add_argument('--candidate-pylock',type=Path)
    parser.add_argument('--build-tools',type=Path)
    parser.add_argument('--helper',type=Path)
    parser.add_argument('--notebook',type=Path)
    args = parser.parse_args()
    manifest = build(args.source_archive, args.output_dir, args.build_commit,
        candidate_wheels=candidate_files(args.candidate_pylock) if args.candidate_pylock else None,
        build_tools=json.loads(args.build_tools.read_text()) if args.build_tools else None,
        helper=args.helper,notebook=args.notebook)
    print(json.dumps({k: manifest[k] for k in (
        "archive_bytes", "archive_sha256", "expanded_bytes", "build_commit")}, indent=2))


if __name__ == "__main__":
    main()
