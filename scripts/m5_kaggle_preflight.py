"""Bounded CPU source/environment preparation; never load weights or run models."""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import signal
import sqlite3
import stat
import subprocess
import sys
import time
import uuid
import zipfile


PINNED = {"torch": "2.11.0+cu128", "pydantic": "2.13.5", "langgraph": "1.2.12",
          "langgraph-checkpoint": "4.2.0", "langgraph-checkpoint-sqlite": "3.1.1",
          "langchain-core": "1.6.6", "transformers": "5.12.0", "accelerate": "1.14.0",
          "bitsandbytes": "0.49.2", "tokenizers": "0.22.2", "huggingface-hub": "1.19.0"}
INDEX_ARGS = ["--index-url", "https://pypi.org/simple", "--extra-index-url",
              "https://download.pytorch.org/whl/cu128"]
OUTPUT_RESERVE = 256 * 2**20
BUILD_RESERVE = 2**30
CPU_SECONDS = 2700
EXPORT_SECONDS = 90
INVENTORY_LIMIT = 2000
FOCUSED = ["tests.test_inference_preparation", "tests.inference_checks", "tests.durable_checks",
           "tests.attempt_checks", "tests.worker_checks"]
STAGES = ["input_inventory", "source", "cpu_host", "command_cleanup", "environment", "installed_packages",
          "focused_checks", "native_9b", "native_4b", "native_capacity", "filesystem_backup"]
MODEL_SELECTED_BYTES = {"9B": 19319226111, "4B": 9332739901}


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def inventory(root: Path, limit: int = INVENTORY_LIMIT) -> dict:
    entries, errors, pending = [], [], [root]
    truncated = False
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"input_root_missing_or_symlink: {root}")
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as children:
                for child in children:
                    if len(entries) >= limit:
                        truncated = True
                        break
                    info = child.stat(follow_symlinks=False)
                    kind = ("symlink" if child.is_symlink() else "directory" if stat.S_ISDIR(info.st_mode)
                            else "file" if stat.S_ISREG(info.st_mode) else "other")
                    entries.append({"path": Path(child.path).relative_to(root).as_posix(),
                                    "kind": kind, "bytes": info.st_size})
                    if kind == "directory":
                        pending.append(Path(child.path))
        except OSError as exc:
            errors.append({"path": str(directory), "reason": str(exc)})
        if truncated:
            break
    return {"root": str(root), "entries": sorted(entries, key=lambda x: x["path"]),
            "limit": limit, "truncated": truncated, "errors": errors}


def transformed_sources(root: Path, listing: dict) -> list[dict]:
    entries = {x["path"]: x for x in listing["entries"]}
    result = []
    for name, item in entries.items():
        if item["kind"] != "file" or not name.endswith("SOURCE_COMMIT.txt") or item["bytes"] > 128:
            continue
        source = PurePosixPath(name).parent
        paths = {}
        for fixture in ("capacity_report.json.gz", "capacity_report.json",
                        "scripted_lifecycle_run.zip", "scripted_lifecycle_run"):
            relative = (source / "tests/fixtures" / fixture).as_posix()
            paths[fixture] = entries.get(relative, {"kind": "missing"})
        result.append({"root": str(root / source), "paths": paths})
    return result


def safe_members(archive: zipfile.ZipFile, expected: dict) -> list[zipfile.ZipInfo]:
    infos = archive.infolist()
    names = []
    for entry in infos:
        name = entry.orig_filename
        if (not name or name != entry.filename or "\\" in name or ":" in name
                or name.startswith("/") or any(ord(c) < 32 for c in name)
                or any(part in {"", ".", ".."} for part in name.split("/"))
                or entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16)):
            raise ValueError(f"unsafe_archive_member: {name!r}")
        if name in names or any(str(p) in names for p in PurePosixPath(name).parents):
            raise ValueError(f"duplicate_or_conflicting_member: {name}")
        if any(other.startswith(name + "/") for other in names):
            raise ValueError(f"conflicting_member: {name}")
        names.append(name)
    if set(names) != set(expected):
        raise ValueError(f"archive_member_set: missing={sorted(set(expected)-set(names))}; "
                         f"unexpected={sorted(set(names)-set(expected))}")
    for entry in infos:
        if entry.file_size != expected[entry.filename]["bytes"]:
            raise ValueError(f"archive_member_size: {entry.filename}")
    return infos


def admit_source(payload: Path, destination: Path, expected: dict) -> dict:
    if expected["expanded_bytes"] != sum(x["bytes"] for x in expected["members"].values()):
        raise ValueError("source_manifest_expanded_bytes")
    if payload.is_symlink() or not payload.is_file():
        raise ValueError("payload_not_regular")
    if payload.stat().st_size != expected["archive_bytes"]:
        raise ValueError("payload_size_mismatch")
    if sha256_file(payload) != expected["archive_sha256"]:
        raise ValueError("payload_hash_mismatch")
    if destination.exists():
        raise FileExistsError("source_destination_exists")
    with zipfile.ZipFile(payload) as archive:
        infos = safe_members(archive, expected["members"])
        # Validate every member before executing/importing/copying any source.
        for entry in infos:
            with archive.open(entry) as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != expected["members"][entry.filename]["sha256"]:
                raise ValueError(f"archive_member_hash: {entry.filename}")
        marker = archive.read("SOURCE_COMMIT.txt").decode("ascii").strip()
        if marker != expected["source_baseline_commit"]:
            raise ValueError("source_baseline_marker")
        destination.mkdir(parents=True, exist_ok=False)
        for entry in infos:
            target = destination / entry.filename
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError(f"source_path_escape: {entry.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(entry) as incoming, target.open("xb") as output:
                shutil.copyfileobj(incoming, output, 1024 * 1024)
            if sha256_file(target) != expected["members"][entry.filename]["sha256"]:
                raise ValueError(f"extracted_member_hash: {entry.filename}")
    return {"payload": str(payload), "archive_sha256": expected["archive_sha256"],
            "verified_members": len(infos), "expanded_bytes": expected["expanded_bytes"],
            "baseline_commit": marker, "build_commit": expected.get("build_commit"),
            "dataset_version": None, "dataset_reference": str(payload.parent),
            "closure": "Every canonical archive member, including unchanged compressed fixtures."}


def filesystem_facts(paths: dict[str, Path]) -> dict:
    locations, pools = {}, {}
    for role, path in paths.items():
        info, disk = path.stat(), shutil.disk_usage(path)
        key = str(info.st_dev)
        locations[role] = {"path": str(path), "pool": key, "free_bytes": disk.free,
                           "total_bytes": disk.total}
        pools[key] = {"free_bytes": min(disk.free, pools.get(key, {}).get("free_bytes", disk.free)),
                      "roles": pools.get(key, {}).get("roles", []) + [role]}
    return {"locations": locations, "pools": pools, "quota_verified": False,
            "interpretation": "Filesystem free space is observed; shared pools are counted once."}


def require_space(scratch: Path, output: Path, additional_scratch: int) -> dict:
    facts = filesystem_facts({"scratch": scratch, "output": output})
    same = scratch.stat().st_dev == output.stat().st_dev
    if shutil.disk_usage(output).free < OUTPUT_RESERVE:
        raise ValueError("output_evidence_reserve")
    required = additional_scratch + (OUTPUT_RESERVE if same else 0)
    scratch_pool=facts['locations']['scratch']['pool']
    if facts['pools'][scratch_pool]['free_bytes'] < required:
        raise ValueError(f"scratch_capacity: additional_required={required}")
    facts.update(additional_scratch_bytes=additional_scratch, output_reserve_bytes=OUTPUT_RESERVE)
    return facts


def _group_exists(pid: int, proc_root: Path = Path('/proc')) -> bool:
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return False
    if not proc_root.is_dir():
        return True  # Presence is known; live membership cannot be inspected.
    for path in proc_root.iterdir():
        if not path.name.isdigit():
            continue
        try:
            fields=(path/'stat').read_text().rsplit(')',1)[1].split()
            if int(fields[2])==pid and fields[0] not in {'Z','X'}:
                return True
        except FileNotFoundError:
            continue  # Process exited during the read.
        except (OSError,ValueError,IndexError):
            return True  # Never claim cleanup from an incomplete inspection.
    return False  # Zombies have exited and hold no executable/CUDA state.


def _stop_owned(process: subprocess.Popen) -> dict:
    if os.name == "nt":
        result = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                capture_output=True, timeout=5)
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
        return {"leader_exited": process.poll() is not None,
                "tree_confirmation": "taskkill" if result.returncode == 0 else "unconfirmed"}
    for sig in (signal.SIGTERM, signal.SIGKILL):
        if not _group_exists(process.pid):
            break
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            break
        end = time.monotonic() + 2
        while time.monotonic() < end:
            process.poll()
            if not _group_exists(process.pid):
                break
            time.sleep(0.05)
    process.wait(timeout=2)
    return {"leader_exited": True,
            "tree_confirmation": "exited" if not _group_exists(process.pid) else "unconfirmed"}


def command(output: Path, name: str, args: list, *, deadline: float, timeout: float,
            cwd: Path, env: dict) -> dict:
    remaining = deadline - time.monotonic() - EXPORT_SECONDS
    if remaining < timeout + 7:
        raise TimeoutError(f"deadline_before_command: {name}, remaining={remaining:.1f}, bound={timeout}")
    logs = output / "logs"
    logs.mkdir(exist_ok=True)
    stdout, stderr = logs / (name + ".stdout.txt"), logs / (name + ".stderr.txt")
    record = {"name": name, "args": list(map(str, args)), "cwd": str(cwd), "started_utc": utc(),
              "timeout_seconds": timeout, "stdout": stdout.relative_to(output).as_posix(),
              "stderr": stderr.relative_to(output).as_posix(), "status":"failed",
              "leader_exited":False,"tree_confirmation":"not_started"}
    started, process = time.monotonic(), None
    try:
        with stdout.open("xb") as out, stderr.open("xb") as err:
            options = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {
                "start_new_session": True}
            process = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env, stdout=out, stderr=err,
                                       stdin=subprocess.DEVNULL, **options)
            record["pid"] = process.pid
            record['tree_confirmation']='unconfirmed'
            try:
                record["exit_code"] = process.wait(timeout=timeout)
                record["status"] = "passed" if process.returncode == 0 else "failed"
                record["leader_exited"] = True
                if os.name != "nt" and _group_exists(process.pid):
                    record.update(_stop_owned(process), status="failed", reason="descendants_survived")
                elif os.name != "nt":
                    record['tree_confirmation']='exited'
                else:
                    record['tree_confirmation']='not_checked_on_windows'
            except BaseException as exc:
                record.update(status="failed", reason=type(exc).__name__, **_stop_owned(process))
                raise
    finally:
        record.update(ended_utc=utc(), elapsed_seconds=time.monotonic()-started)
        save_json(logs / (name + ".json"), record)
    if record["status"] != "passed":
        raise RuntimeError(f"command_failed: {name}, exit={record.get('exit_code')}, "
                           f"reason={record.get('reason')}; see logs/{name}.stderr.txt")
    return record


def json_stdout(output: Path, record: dict) -> object:
    path = output / record["stdout"]
    if path.stat().st_size > 2 * 2**20:
        raise ValueError(f"machine_stdout_too_large: {record['name']}")
    return json.loads(path.read_text(encoding="utf-8"))


def process_tree_diagnostic(output: Path, scratch: Path, deadline: float, env: dict) -> dict:
    ticker=scratch/'process-tree-ticks'
    grandchild="import pathlib,time;p=pathlib.Path("+repr(str(ticker))+");[(p.write_text(str(n)),time.sleep(.05)) for n in range(600)]"
    child="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(grandchild)+"]);time.sleep(30)"
    parent="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);print('owned-tree-started',flush=True);time.sleep(30)"
    try:
        command(output,'owned-process-timeout',[sys.executable,'-c',parent],deadline=deadline,
                timeout=2,cwd=scratch,env=env)
    except subprocess.TimeoutExpired:
        record=json.loads((output/'logs/owned-process-timeout.json').read_text())
    else:
        raise ValueError('owned_tree_expected_timeout_missing')
    confirmation='taskkill' if os.name=='nt' else 'exited'
    if not record.get('leader_exited') or record.get('tree_confirmation')!=confirmation or not ticker.is_file():
        raise ValueError('owned_tree_cleanup_unconfirmed')
    before=ticker.read_text()
    time.sleep(.2)
    if ticker.read_text()!=before:
        raise ValueError('owned_grandchild_still_running')
    return {'expected_timeout':True,'leader_exited':True,'tree_confirmation':confirmation,
            'grandchild_stopped':True,'scope':'Synthetic CPU process diagnostic; no model or GPU initialization.'}


def test_result(output: Path, record: dict, expected_count: int) -> dict:
    text = (output / record["stderr"]).read_text(encoding="utf-8")
    matches = re.findall(r"^Ran (\d+) tests? in ([\d.]+)s$", text, flags=re.MULTILINE)
    ok = re.search(r"^OK(?: \(([^\n]+)\))?\s*$", text, flags=re.MULTILINE)
    skipped = re.search(r"skipped=(\d+)", ok.group(1) or "") if ok else None
    if len(matches) != 1 or not ok or int(matches[0][0]) != expected_count or skipped:
        raise ValueError(f"test_count_or_skip: {record['name']}, expected={expected_count}")
    return {"tests": expected_count, "skipped": 0, "reported_seconds": float(matches[0][1]),
            "scope": "Source-mode candidate-host checks; no physical model generation."}


def sqlite_diagnostic(output: Path) -> dict:
    database, backup = output / "filesystem.sqlite", output / "filesystem-backup.sqlite"
    with closing(sqlite3.connect(database, timeout=1)) as db:
        journal = db.execute("PRAGMA journal_mode=WAL").fetchone()[0]
        db.execute("PRAGMA synchronous=FULL")
        synchronous = db.execute("PRAGMA synchronous").fetchone()[0]
        db.execute("CREATE TABLE probe(value INTEGER NOT NULL)")
        db.execute("INSERT INTO probe VALUES (7)")
        db.commit()
        with closing(sqlite3.connect(backup, timeout=1)) as copy:
            db.backup(copy)
    with closing(sqlite3.connect(backup.as_uri()+"?mode=ro&immutable=1", uri=True, timeout=1)) as db:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        rows = db.execute("SELECT value FROM probe").fetchall()
        try:
            db.execute("INSERT INTO probe VALUES (8)")
        except sqlite3.OperationalError:
            read_only = True
        else:
            read_only = False
    if journal != "wal" or synchronous != 2 or integrity != "ok" or rows != [(7,)] or not read_only:
        raise ValueError("filesystem_sqlite_diagnostic")
    return {"journal_mode": journal, "synchronous": synchronous, "integrity": integrity,
            "rows": rows, "read_only_enforced": read_only, "backup_sha256": sha256_file(backup),
            "scope": "Small synthetic diagnostic; actual worker/crash checks are separate."}


def candidate_environment(scratch: Path) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("PYTHON", "PIP_", "HF_", "TRANSFORMERS_", "VIRTUAL_ENV",
                                "LANGSMITH_", "LANGCHAIN_"))}
    env.update(PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1",
               TOKENIZERS_PARALLELISM="false", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
               HF_HUB_CACHE=str(scratch/"hub"), TMPDIR=str(scratch/"tmp"), TEMP=str(scratch/"tmp"),
               TMP=str(scratch/"tmp"), PIP_CONFIG_FILE=os.devnull)
    (scratch/"tmp").mkdir(exist_ok=True)
    return env


def installed_probe_script(expected: dict, versions: dict) -> str:
    hashes = {n: item["sha256"] for n, item in expected["members"].items()
              if n.startswith("recovery/") and n.endswith(".py")}
    return "\n".join([
        "import hashlib,json,sys,site", "from pathlib import Path",
        "from importlib.metadata import version", "import recovery,recovery.inference,recovery.runner",
        "from langgraph.checkpoint.sqlite import SqliteSaver",
        "from transformers import Qwen3_5ForCausalLM", "import torch",
        f"wanted={versions!r}", "actual={n:version(n) for n in wanted}",
        "assert actual==wanted, {'expected':wanted,'actual':actual}",
        "assert sys.prefix!=sys.base_prefix and site.ENABLE_USER_SITE is False",
        "assert torch.__version__=='2.11.0+cu128' and torch.version.cuda=='12.8'",
        "package=Path(recovery.__file__).resolve().parent", f"expected={hashes!r}",
        "observed={'recovery/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in package.glob('*.py')}",
        "assert observed==expected, 'source-to-installed module bytes differ'",
        "assert package.is_relative_to(Path(sys.prefix).resolve()), 'base/source import contamination'",
        "print(json.dumps({'versions':actual,'executable':sys.executable,'prefix':sys.prefix,",
        "'sys_path':sys.path,'module_root':str(package),'verified_module_hashes':observed,",
        "'qwen_text_class':Qwen3_5ForCausalLM.__name__,'torch_cuda_build':torch.version.cuda,",
        "'gpu_native_diagnostics':None,'model_generations':0}))", ""])


def export_evidence(output: Path) -> dict:
    paths = sorted(p for p in output.rglob("*") if p.is_file() and not p.is_symlink()
                   and (p.suffix in {".json", ".txt", ".lock", ".sqlite"}))
    partial, final = output/"preflight-results.zip.partial", output/"preflight-results.zip"
    with zipfile.ZipFile(partial, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(partial) as archive:
        if archive.testzip() is not None or archive.namelist() != [p.relative_to(output).as_posix() for p in paths]:
            raise ValueError("export_crc_or_members")
    partial.replace(final)
    return {"zip_path": str(final), "zip_sha256": sha256_file(final), "zip_bytes": final.stat().st_size}


def run_preflight(input_root: Path, output_root: Path, scratch_root: Path, expected: dict,
                  lock_text: str, *, workflow_seconds: float = CPU_SECONDS) -> dict:
    started = time.monotonic()
    deadline = started + workflow_seconds
    label = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+"-"+uuid.uuid4().hex[:8]
    output = output_root/('recovery-m5-preflight-'+label)
    output.mkdir(parents=True, exist_ok=False)
    scratch = scratch_root/label
    source, candidate = scratch/"source", scratch/"venv"
    report = {"schema_version": 2, "kind": "cpu-canonical-source-preparation", "started_utc": utc(),
              "output_directory": str(output), "scratch_directory": str(scratch),
              "cpu_workflow_limit_seconds": workflow_seconds, "export_reserve_seconds": EXPORT_SECONDS,
              "stages": {n: {"status": "not_run", "reason": None} for n in STAGES}, "root_blocker": None}
    payload, listing, env = None, None, None

    def stage(name, prerequisites, action):
        state = report["stages"][name]
        state["prerequisites"] = prerequisites
        blocked = [p for p in prerequisites if report["stages"][p]["status"] != "passed"]
        if blocked:
            state.update(status="blocked", reason="prerequisites: "+", ".join(blocked))
        elif deadline-time.monotonic() < EXPORT_SECONDS:
            state.update(status="blocked", reason="cpu_deadline_before_stage")
            report["root_blocker"] = report["root_blocker"] or "cpu_deadline_before_stage"
        else:
            then = time.monotonic()
            state.update(started_utc=utc(), status="running")
            save_json(output/"preflight-report.json", report)
            try:
                state.update(result=action(), status="passed")
            except KeyboardInterrupt:
                state.update(status="failed", reason="user_interruption")
                report["root_blocker"] = report["root_blocker"] or "user_interruption"
                raise
            except Exception as exc:
                state.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
                report["root_blocker"] = report["root_blocker"] or state["reason"]
            finally:
                state.update(ended_utc=utc(), elapsed_seconds=time.monotonic()-then)
        save_json(output/"preflight-report.json", report)
        print(f"{name}: {state['status']}"+(f" — {state['reason']}" if state["reason"] else ""), flush=True)

    def input_stage():
        nonlocal payload, listing
        listing = inventory(input_root)
        save_json(output/"input-inventory.json", listing)
        save_json(output/"source-input-diagnosis.json", {"transformed_sources": transformed_sources(input_root, listing)})
        if listing["truncated"] or listing["errors"]:
            raise ValueError("incomplete_input_inventory")
        choices = [input_root/x["path"] for x in listing["entries"]
                   if x["kind"] == "file" and PurePosixPath(x["path"]).name == expected["payload_filename"]]
        if len(choices) != 1:
            raise ValueError("payload_missing" if not choices else "payload_ambiguous")
        payload = choices[0]
        return {"selected_payload": str(payload), "entries": len(listing["entries"])}

    def source_stage():
        scratch.mkdir(parents=True, exist_ok=False)
        facts = require_space(scratch, output, expected["expanded_bytes"]+BUILD_RESERVE)
        save_json(output/"storage-before-source.json", facts)
        return admit_source(payload, source, expected)

    def host_stage():
        gpu_dir = Path("/proc/driver/nvidia/gpus")
        gpus = sorted(p.name for p in gpu_dir.iterdir()) if gpu_dir.is_dir() else []
        host = {"python": platform.python_version(), "os": platform.platform(),
                "sqlite": sqlite3.sqlite_version, "visible_driver_gpu_entries": gpus,
                "cuda_initialized_by_kernel": False}
        save_json(output/"host.json", host)
        if gpus:
            raise ValueError("cpu_stage_gpu_visible: stop session and select Accelerator None")
        if platform.system() != "Linux" or sys.version_info[:2] != (3, 13) or platform.machine() != "x86_64":
            raise ValueError("candidate_host_requires_linux_x86_64_python313")
        return host

    def invoke(name, args, timeout, *, cwd=None, source_mode=False):
        if report.get('process_cleanup_unconfirmed'):
            raise RuntimeError('prior_process_cleanup_unconfirmed')
        require_space(scratch, output, BUILD_RESERVE)
        process_env = dict(env)
        if source_mode:
            process_env["PYTHONPATH"] = str(source)
        try:
            return command(output, name, args, deadline=deadline, timeout=timeout,
                           cwd=cwd or scratch, env=process_env)
        except BaseException:
            record_path = output/'logs'/(name+'.json')
            if record_path.exists() and json.loads(record_path.read_text()).get('tree_confirmation')=='unconfirmed':
                report['process_cleanup_unconfirmed']=True
            raise

    interpreter = candidate/("Scripts/python.exe" if os.name == "nt" else "bin/python")

    def environment_stage():
        nonlocal env
        if hashlib.sha256(lock_text.encode()).hexdigest() != expected["candidate_lock_sha256"]:
            raise ValueError("candidate_lock_hash")
        env = candidate_environment(scratch)
        lock = scratch/"candidate.lock"
        lock.write_text(lock_text, encoding="utf-8")
        (output/"candidate.lock").write_text(lock_text, encoding="utf-8")
        versions = dict(re.findall(r"^([\w.-]+)==([^\s\\]+)", lock_text, flags=re.MULTILINE))
        if any(versions.get(n) != v for n,v in PINNED.items()):
            raise ValueError("candidate_roots_changed")
        invoke("create-venv", [sys.executable, "-m", "venv", candidate], 60)
        configuration = (candidate/"pyvenv.cfg").read_text().lower()
        if "include-system-site-packages = false" not in configuration:
            raise ValueError("candidate_inherits_base_packages")
        tools = expected["build_tools"]
        files = expected["candidate_wheels"]
        if {p['name']:p['version'] for p in files} != versions:
            raise ValueError("candidate_wheel_closure")
        download_bytes = sum(p["bytes"] for p in files)
        # This stated package-expansion forecast is replaced by exact wheel ZIP sizes below.
        facts = require_space(scratch, output, 4*download_bytes+BUILD_RESERVE)
        facts.update(download_bytes=download_bytes, package_expansion_forecast_multiplier=4)
        save_json(output/"storage-before-wheels.json", facts)
        save_json(output/"wheel-files.json", files)
        bootstrap = scratch/"pip-bootstrap.lock"
        p = tools["pip"]
        bootstrap.write_text(f"pip=={p['version']} --hash=sha256:{p['wheels'][0]['sha256']}\n")
        invoke("bootstrap-pip", [interpreter,"-m","pip","--isolated","install","--no-cache-dir",
               "--no-deps","--require-hashes","--report",output/"pip-bootstrap.json",
               "--index-url","https://pypi.org/simple","-r",bootstrap], 120)
        pip = [interpreter,"-m","pip","--isolated","--disable-pip-version-check"]
        common = ["--no-cache-dir","--only-binary=:all:","--require-hashes","-r",lock]
        wheels = scratch/"wheels"
        wheels.mkdir()
        direct_lock = scratch/"candidate-download.lock"
        direct_lock.write_text("".join(f"{p['name']} @ {p['url']} --hash=sha256:{p['sha256']}\n" for p in files))
        invoke("download-candidate", pip+["download","--no-deps","--dest",wheels,"--no-cache-dir",
               "--require-hashes","--only-binary=:all:","-r",direct_lock],900)
        tool_lock = scratch/"build-tools.lock"
        tool_lock.write_text("".join(f"{n}=={tools[n]['version']} --hash=sha256:{tools[n]['wheels'][0]['sha256']}\n"
                                    for n in ("setuptools","wheel")))
        invoke("download-build-tools", pip+["download","--no-deps","--dest",wheels,"--only-binary=:all:",
               "--require-hashes","--no-cache-dir","-r",tool_lock,"--index-url","https://pypi.org/simple"],120)
        expected_files = {p['filename']:p for p in files}
        expected_files.update({tools[n]['wheels'][0]['filename']:tools[n]['wheels'][0] for n in ('setuptools','wheel')})
        actual_files = {p.name:p for p in wheels.iterdir()}
        if set(actual_files) != set(expected_files):
            raise ValueError("wheel_file_set")
        expanded = 0
        for name,path in actual_files.items():
            wanted = expected_files[name]
            if path.stat().st_size != wanted['bytes'] or sha256_file(path) != wanted['sha256']:
                raise ValueError(f"wheel_bytes: {name}")
            with zipfile.ZipFile(path) as archive:
                expanded += sum(p.file_size for p in archive.infolist())
        save_json(output/"storage-before-install.json", require_space(scratch,output,expanded+BUILD_RESERVE))
        invoke("resolve-candidate",pip+["install","--dry-run","--ignore-installed","--no-index",
               "--find-links",wheels,"--report",output/"resolver.json"]+common,120)
        resolver = json.loads((output/"resolver.json").read_text())
        resolved = {p["metadata"]["name"].lower().replace("_","-"): p["metadata"]["version"]
                    for p in resolver["install"]}
        if resolved != versions:
            raise ValueError("actual_resolver_closure_differs_from_candidate")
        invoke("install-candidate",pip+["install","--no-index","--find-links",wheels,"--no-compile",
               "--report",output/"install.json"]+common,300)
        constraints = scratch/"build-constraints.txt"
        constraints.write_text("".join(f"{n}=={tools[n]['version']}\n" for n in ('setuptools','wheel')))
        built = scratch/"built"
        built.mkdir()
        invoke("build-source",pip+["wheel","--no-deps","--no-index","--find-links",wheels,
               "--build-constraint",constraints,"--wheel-dir",built,source,"-v"],120)
        built_files = list(built.glob('*.whl'))
        if len(built_files) != 1:
            raise ValueError("source_wheel_count")
        save_json(output/"source-wheel.json", {"filename":built_files[0].name,
                  "bytes":built_files[0].stat().st_size,"sha256":sha256_file(built_files[0]),
                  "build_tools":{n:tools[n]['version'] for n in ('setuptools','wheel')}})
        invoke("install-source",pip+["install","--no-deps","--no-index","--no-compile",
               "--report",output/"source-install.json",built_files[0]],60)
        return {"mode":"clean-venv-offline-wheel-install","versions":versions,
                "resolved_packages":len(versions),"download_bytes":download_bytes,
                "wheel_expanded_bytes":expanded,"build_tools":tools}

    def packages_stage():
        invoke("pip-check", [interpreter,"-m","pip","--isolated","check"],30)
        probe = scratch/"installed_probe.py"
        versions = report['stages']['environment']['result']['versions']
        probe.write_text(installed_probe_script(expected,versions),encoding='utf-8')
        record = invoke("installed-probe", [interpreter,"-I",probe],90)
        result = json_stdout(output,record)
        wanted_hashes = {n:p['sha256'] for n,p in expected['members'].items()
                         if n.startswith('recovery/') and n.endswith('.py')}
        if (not isinstance(result,dict) or result.get('versions')!=versions
                or result.get('verified_module_hashes')!=wanted_hashes
                or result.get('qwen_text_class')!='Qwen3_5ForCausalLM'
                or result.get('torch_cuda_build')!='12.8' or result.get('model_generations')!=0):
            raise ValueError('installed_probe_schema_or_provenance')
        save_json(output/"installed-provenance.json",result)
        record = invoke("pip-list", [interpreter,"-m","pip","--isolated","list","--format=json"],30)
        save_json(output/"installed-packages.json",json_stdout(output,record))
        freeze = invoke("pip-freeze", [interpreter,"-m","pip","--isolated","freeze","--all"],30)
        shutil.copyfile(output/freeze['stdout'],output/'installed-freeze.txt')
        return result

    def tests_stage(name,args,count,bound):
        record = invoke(name,[interpreter]+args,bound,cwd=source,source_mode=True)
        return test_result(output,record,count)

    result = {"zip_path":None,"zip_sha256":None,"run_directory":str(output)}
    try:
        save_json(output/"expected-source-manifest.json",expected)
        stage("input_inventory",[],input_stage)
        stage("source",["input_inventory"],source_stage)
        stage("cpu_host",[],host_stage)
        stage("command_cleanup",["source","cpu_host"],lambda:process_tree_diagnostic(output,scratch,deadline,candidate_environment(scratch)))
        stage("environment",["source","cpu_host","command_cleanup"],environment_stage)
        stage("installed_packages",["environment"],packages_stage)
        stage("focused_checks",["installed_packages"],lambda:tests_stage("focused-checks",["-m","unittest",*FOCUSED,"-q"],81,360))
        stage("native_9b",["installed_packages"],lambda:tests_stage("native-9b",["-m","tests.tokenizer_inference","--tokenizer","metadata/9B"],4,60))
        stage("native_4b",["installed_packages"],lambda:tests_stage("native-4b",["-m","tests.tokenizer_inference","--tokenizer","metadata/4B"],4,60))
        stage("native_capacity",["installed_packages"],lambda:tests_stage("native-capacity",["-m","tests.tokenizer_capacity","--tokenizer","metadata/9B"],8,90))
        stage("filesystem_backup",[],lambda:sqlite_diagnostic(output))
    except KeyboardInterrupt:
        report['root_blocker'] = report['root_blocker'] or 'user_interruption'
        for state in report['stages'].values():
            if state['status'] in {'running','not_run'}:
                state.update(status='blocked',reason='user_interruption')
    finally:
        states = report['stages']
        passed = all(s['status']=='passed' for s in states.values())
        tests = sum(s.get('result',{}).get('tests',0) for s in states.values() if s['status']=='passed')
        summary = {"preparation_checks_passed":passed,"root_blocker":report['root_blocker'],
                   "tests_passed":tests,"model_generations":0,"model_smoke_ready":False,
                   "gpu_native_diagnostics":None,"model_assets_verified":None,"model_smoke":None,
                   "provider_assignment_utc":None,"provider_release_utc":None,
                   "observed_cpu_wall_seconds":time.monotonic()-started,
                   "next_action":("Download the ZIP and stop the session. Return it for candidate-host review before GPU/model work."
                    if passed else "Download the ZIP and stop the session. Return the root-blocker evidence for review; do not rerun or repair fixtures.")}
        if report['root_blocker'] and 'payload_missing' in report['root_blocker']:
            summary['next_action']='Attach the private dataset containing unchanged m5-kaggle-source.payload. Download this ZIP, stop the session, and return the evidence.'
        report['summary']=summary
        save_json(output/'preflight-report.json',report)
        save_json(output/'summary.json',summary)
        try:
            if scratch.exists():
                storage=filesystem_facts({'scratch':scratch,'output':output})
                storage['models']={n:{'selected_file_bytes':b,'assets_staged':False,'quota_admitted':False}
                                   for n,b in MODEL_SELECTED_BYTES.items()}
                save_json(output/'storage-after.json',storage)
        except Exception as exc:
            report['storage_after_error']=f'{type(exc).__name__}: {exc}'
            save_json(output/'preflight-report.json',report)
        try:
            result.update(export_evidence(output))
        except Exception as exc:
            report['export_error']=f'{type(exc).__name__}: {exc}'
            save_json(output/'preflight-report.json',report)
        result.update(summary=summary,report=report)
    return result
