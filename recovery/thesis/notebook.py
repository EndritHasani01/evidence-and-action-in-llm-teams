"""Thin facade for notebooks/thesis_kaggle.ipynb (standard library only).

Each notebook cell calls one function here. GPU and scientific work runs in a
separate process inside the pinned virtual environment
(`python -m recovery.thesis <command>`); its output streams into the cell.
Cells never raise for expected stops: they print a banner, leave a receipt or
checkpoint, and later GPU cells skip. Specification section 7.
"""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import uuid

REPOSITORY = "EndritHasani01/evidence-and-action-in-llm-teams"
SCOPES = ("cpu", "rehearsal", "development", "main")
KAGGLE_SESSION_HOURS = 12.0   # documented hard limit of a Kaggle GPU session
SESSION_MARGIN_MINUTES = 15   # the deadline stays this far inside that limit
STATE = {}


def _now():
    return datetime.now(timezone.utc)


def _container_start(proc="/proc", ticks=None):
    """When this Kaggle session's container started (its PID 1), or None without Linux /proc."""
    try:
        uptime = float((Path(proc) / "uptime").read_text().split()[0])
        fields = (Path(proc) / "1" / "stat").read_text().rsplit(")", 1)[1].split()
        ticks = ticks or os.sysconf("SC_CLK_TCK")
        age = uptime - int(fields[19]) / ticks  # field 22: start time in clock ticks after boot
    except (OSError, ValueError, IndexError, AttributeError):
        return None
    return _now() - timedelta(seconds=max(0.0, age))


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _receipt(name, value):
    folder = Path(STATE["receipts"])
    folder.mkdir(parents=True, exist_ok=True)
    n = len(list(folder.glob("*.json"))) + 1
    path = folder / f"{n:02d}-{name}.json"
    path.write_text(json.dumps(dict(value, at=_now().isoformat()), indent=1, default=str) + "\n", encoding="utf-8")
    return path


def _banner(kind, text):
    print(f"{'=' * 78}\n{kind}: {text}\n{'=' * 78}", flush=True)


def _source_manifest(root):
    import hashlib
    files = {}
    for base in ("recovery", "configs"):
        for path in sorted((root / base).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def start(*, source_commit, study, scope, session_hours, start_new_study=False, main_authorization="",
          checkpoint_repo="", source_root, working="/kaggle/working", scratch="/kaggle/temp/thesis",
          inputs="/kaggle/input"):
    """Cell 1: record settings and the session deadline; verify the downloaded source."""
    if scope not in SCOPES:
        raise ValueError(f"SCOPE must be one of {SCOPES}")
    root = Path(source_root)
    recorded = (root / ".source-commit").read_text().strip() if (root / ".source-commit").exists() else None
    if recorded != source_commit:
        raise ValueError(f"downloaded source is {recorded}, not SOURCE_COMMIT {source_commit}")
    # One session per Kaggle container: a cell rerun or a kernel restart keeps the session and its
    # deadline, and the deadline never passes the container's 12-hour limit.
    container = _container_start()
    marker = Path(scratch) / "session.json"
    saved = _read_json(marker)
    if STATE.get("kernel_pid") == os.getpid():
        session, started, deadline = STATE["session"], STATE["session_start"], STATE["deadline"]  # reruns keep it
    elif (saved and container is not None and saved.get("source_commit") == source_commit
          and abs(datetime.fromisoformat(saved["container_start"]) - container) < timedelta(minutes=2)):
        session, started = saved["session"], datetime.fromisoformat(saved["session_start"])
        deadline = datetime.fromisoformat(saved["deadline"])
        _banner("NOTE", f"the kernel restarted inside the same Kaggle session; continuing session {session[:8]} "
                        "and its deadline")
    else:
        session, started = str(uuid.uuid4()), _now()
        deadline = started + timedelta(hours=float(session_hours))
        if container is not None:
            limit = container + timedelta(hours=KAGGLE_SESSION_HOURS, minutes=-SESSION_MARGIN_MINUTES)
            if deadline > limit:
                deadline = limit
                print(f"Deadline capped at {limit:%H:%M} UTC: this Kaggle session started at {container:%H:%M} UTC "
                      f"and ends {KAGGLE_SESSION_HOURS:.0f} hours later.", flush=True)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps(dict(session=session, session_start=started.isoformat(), deadline=deadline.isoformat(),
                                      source_commit=source_commit,
                                      container_start=container.isoformat() if container else None)), encoding="utf-8")
    if (deadline - _now()).total_seconds() < 3600:
        _banner("WARNING", f"less than an hour remains before this session's deadline ({deadline:%H:%M} UTC); "
                           "GPU stages stop early. Start a fresh session for GPU work")
    study_id = study + "-rehearsal" if scope == "rehearsal" else study
    token = ""
    if checkpoint_repo:
        try:
            from kaggle_secrets import UserSecretsClient
            token = UserSecretsClient().get_secret("HF_TOKEN")
        except Exception:
            token = os.environ.get("HF_TOKEN", "")
    STATE.update(kernel_pid=os.getpid(), session=session, session_start=started, deadline=deadline,
                 source_commit=source_commit, study=study_id, scope=scope, start_new=bool(start_new_study),
                 authorization=main_authorization.strip(), repo=checkpoint_repo if token else "", token=token,
                 source=root, working=Path(working), scratch=Path(scratch), inputs=inputs,
                 run=Path(working) / "thesis" / study_id,
                 receipts=Path(working) / "thesis-receipts" / session, python=STATE.get("python"),
                 stopped=None)  # a rerun of cell 1 is a fresh attempt; the store re-checks every stop condition
    files = _source_manifest(root)
    _receipt("settings", dict(kind="preparation receipt", session=session, scope=scope, study=study_id,
                              source_commit=source_commit, session_start=started.isoformat(),
                              deadline=deadline.isoformat(), mirror=bool(STATE["repo"]),
                              start_new_study=bool(start_new_study), source_files=len(files)))
    hours_left = (deadline - _now()).total_seconds() / 3600
    print(f"Study {study_id} · scope {scope} · session {session[:8]} · deadline {deadline:%Y-%m-%d %H:%M} UTC "
          f"({hours_left:.1f} h from now) · source {source_commit[:12]} ({len(files)} files) · "
          f"mirror {'on' if STATE['repo'] else 'off'}")
    if checkpoint_repo and not token:
        # Restoring without the configured mirror could silently continue from an older checkpoint.
        _stop("CHECKPOINT_REPO is set but the HF_TOKEN secret is not available: attach it under "
              "Add-ons > Secrets, or set CHECKPOINT_REPO = \"\" to work from attached inputs only")
    return dict(session=session, deadline=deadline.isoformat(), run=str(STATE["run"]))


def install():
    """Cell 2: pinned virtual environment in scratch space (reused within a session)."""
    if STATE.get("stopped"):
        _banner("SKIPPED", f"install: an earlier cell stopped ({STATE['stopped']})")
        return None
    root, scratch = STATE["source"], STATE["scratch"]
    sys.path.insert(0, str(root)) if str(root) not in sys.path else None
    from recovery.i01.setup import PIP_BOOTSTRAP, create_environment, host_inventory, invoke
    from recovery.i01.client import child_environment
    from recovery.i01.runtime import command
    receipts = STATE["receipts"] / "setup"
    receipts.mkdir(parents=True, exist_ok=True)
    host = host_inventory(scratch, STATE["working"])
    gpus = host["gpus"]
    print(f"Host: Python {host['python'].split()[0]} · GPUs: {', '.join(g['name'] for g in gpus) or 'none'} · "
          f"scratch free {host['paths']['scratch']['free'] / 2**30:.0f} GiB · working free "
          f"{host['paths']['working']['free'] / 2**30:.1f} GiB")
    needs_gpu = STATE["scope"] in ("development", "main")
    if host["python_version"][:2] != [3, 13]:
        _stop(f"the pinned lock needs Python 3.13; this image has {host['python'].split()[0]}. "
              "Use the notebook's original (pinned) environment.")
        return None
    if needs_gpu and (len(gpus) != 2 or any("T4" not in g["name"] for g in gpus)):
        _stop("scope needs GPU T4 x2: select it in Settings > Accelerator")
        return None
    venv = scratch / f"venv-{STATE['source_commit'][:12]}"
    python = venv / "bin" / "python"
    env = child_environment(scratch / "hf-cache")
    env.update(TMPDIR=str(scratch / "tmp"), PIP_CONFIG_FILE=os.devnull, PIP_DISABLE_PIP_VERSION_CHECK="1",
               PIP_DEFAULT_TIMEOUT="60")
    (scratch / "tmp").mkdir(parents=True, exist_ok=True)
    if not (venv / ".installed").exists():
        try:
            python = create_environment(venv, scratch, receipts, env)
            invoke(command(python, root, "-m", "pip", "--isolated", "--cache-dir", scratch / "pip-cache", "install",
                           "--only-binary=:all:", "--require-hashes", "--retries", "5",
                           "--index-url", "https://pypi.org/simple", "--extra-index-url", "https://download.pytorch.org/whl/cu128",
                           "-r", root / "configs/i01-runtime.lock"), receipts / "dependencies.log", 3600, env=env)
        except Exception as error:  # an expected stop: later cells skip and Save & Run All still saves receipts
            shutil.rmtree(venv, ignore_errors=True)
            _stop(f"installing the pinned environment failed ({type(error).__name__}: {str(error)[-600:]}); "
                  f"logs in {receipts}. Check that Internet is on, then run cell 2 again")
            return None
        (venv / ".installed").write_text(STATE["source_commit"])
    result = subprocess.run(command(python, root, "-m", "recovery.thesis", "env-check", "--source", root),
                            env=env, capture_output=True, text=True, timeout=300)
    if result.returncode:
        _stop("environment check failed: " + (result.stdout + result.stderr)[-800:])
        return None
    STATE.update(python=python, env=env)
    _receipt("install", dict(kind="preparation receipt", host=host, venv=str(venv), pip=PIP_BOOTSTRAP["version"],
                             env_check=json.loads(result.stdout.strip().splitlines()[-1])))
    print("Pinned environment ready.")
    return str(python)


def use_python(python=None, env=None):
    """Local or test use: run commands with an existing interpreter instead of install()."""
    STATE.update(python=Path(python or sys.executable), env=env or dict(os.environ))


def _stop(message):
    STATE["stopped"] = message
    _banner("STOPPED", message)
    _receipt("stopped", dict(kind="preparation receipt", message=message))


def _common():
    args = ["--run", STATE["run"], "--study", STATE["study"], "--source", STATE["source"],
            "--source-commit", STATE["source_commit"], "--scope", STATE["scope"], "--session", STATE["session"],
            "--session-start", STATE["session_start"].isoformat(), "--deadline", STATE["deadline"].isoformat(),
            "--scratch", STATE["scratch"]]
    if STATE["repo"]:
        args += ["--mirror-repo", STATE["repo"]]
    return args


def _cli(command, *extra):
    if not STATE.get("python"):
        _banner("SKIPPED", f"{command}: the pinned environment is not installed (cell 2)")
        return None
    root = STATE["source"]
    sys.path.insert(0, str(root)) if str(root) not in sys.path else None
    from recovery.i01.runtime import command as runtime_command
    env = dict(STATE.get("env") or os.environ)
    if STATE.get("token"):
        env["HF_TOKEN"] = STATE["token"]
    cmd = [str(c) for c in runtime_command(STATE["python"], root, "-m", "recovery.thesis", command,
                                           *_common(), *extra)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
                               encoding="utf-8", errors="replace", env=env, start_new_session=os.name != "nt")
    try:
        for line in process.stdout:
            print(line, end="", flush=True)
    except KeyboardInterrupt:
        print("Interrupt: asking the stage process to stop at the next call boundary...", flush=True)
        process.send_signal(signal.SIGTERM if os.name != "nt" else signal.CTRL_BREAK_EVENT)
        for line in process.stdout:
            print(line, end="", flush=True)
    process.stdout.close()
    code = process.wait()
    latest = Path(STATE["run"]) / "checkpoints" / "latest.json"
    checkpoint = json.loads(latest.read_text()) if latest.exists() else None
    _receipt(command, dict(kind="cell", exit=code, checkpoint=checkpoint and {k: checkpoint.get(k) for k in ("seq", "path", "sha256")}))
    if code not in (0, 3):
        STATE["stopped"] = f"{command} ended with an error (see the output above and receipts/errors.log)"
    elif code == 3 and command in ("develop", "main", "check", "open", "freeze"):
        STATE["stopped"] = f"{command} stopped; later GPU cells will skip"
    return code


def _gpu_allowed(stage):
    if STATE.get("stopped"):
        _banner("SKIPPED", f"{stage}: an earlier cell stopped ({STATE['stopped']})")
        _receipt(f"{stage}-skipped", dict(kind="preparation receipt", reason=STATE["stopped"]))
        return False
    allowed = {"develop": ("development", "main", "rehearsal"), "freeze": ("main", "rehearsal"),
               "main": ("main", "rehearsal")}[stage]
    if STATE["scope"] not in allowed:
        _banner("SKIPPED", f"{stage}: scope {STATE['scope']} does not include it")
        _receipt(f"{stage}-skipped", dict(kind="preparation receipt", reason="scope"))
        return False
    return True


def open_study():
    """Cell 3: restore the newest checkpoint, reopen, or (first run only) create the study."""
    extra = ["--input-root", STATE["inputs"]]
    if STATE["start_new"]:
        extra.append("--start-new")
    return _cli("open", *extra)


def cpu_checks():
    """Cell 4: manifest, separation, protocol, analysis, checkpoint and capacity checks."""
    if STATE.get("stopped"):
        _banner("SKIPPED", f"check: an earlier cell stopped ({STATE['stopped']})")
        _receipt("check-skipped", dict(kind="preparation receipt", reason=STATE["stopped"]))
        return None
    return _cli("check")


def develop():
    """Cell 5: readiness, 16 development worlds per model, gate report."""
    return _cli("develop") if _gpu_allowed("develop") else None


def freeze():
    """Cell 6: freeze the main size and models under MAIN_AUTHORIZATION."""
    if not _gpu_allowed("freeze"):
        return None
    return _cli("freeze", "--authorization", STATE["authorization"])


def main():
    """Cell 7: continue frozen main work until complete or the session cutoff."""
    return _cli("main") if _gpu_allowed("main") else None


def report():
    """Cell 8: rebuild the report from the canonical store."""
    return _cli("report")


def finish():
    """Cell 9: final checkpoint, mirror and download links; closes this session's record."""
    code = _cli("finish")
    folder = Path(STATE["run"]) / "checkpoints"
    files = sorted(folder.glob("thesis-checkpoint-*.zip")) if folder.exists() else []
    latest = Path(STATE["run"]) / "checkpoints" / "latest.json"
    receipt = json.loads(latest.read_text()) if latest.exists() else {}
    print(f"\nNewest checkpoint: {files[-1] if files else 'none'}")
    mirror = receipt.get("mirror")
    print("Off-session copy: " + ("private mirror verified" if mirror and mirror.get("uploaded") else
                                  "NONE - download the checkpoint, or end with Save & Run All so Kaggle keeps /kaggle/working"))
    try:
        from IPython.display import FileLink, display
        for path in files[-1:] + [Path(STATE["run"]) / "reports" / "report.md"]:
            if path.exists():
                display(FileLink(os.path.relpath(path, STATE["working"])))
    except Exception:
        pass
    print("A link is not proof of a completed download. Stopping the Kaggle session releases the GPU.")
    if STATE.get("stopped"):
        _banner("NOTE", f"this session stopped early: {STATE['stopped']}")
    return code


def show(model, world, cell):
    """Optional: print exact requests and replies of one episode."""
    return _cli("show", "--model", model, "--world", world, "--cell", cell)


def stop_running():
    """Ask a running stage process (from an interrupted cell) to stop safely."""
    lock = Path(STATE["run"]) / "lock.json"
    if not lock.exists():
        print("No stage process holds this study.")
        return False
    held = json.loads(lock.read_text())
    try:
        os.kill(held["pid"], signal.SIGTERM)
        print(f"Stop requested for pid {held['pid']} ({held.get('command')}); it checkpoints and exits.")
        return True
    except (ProcessLookupError, PermissionError, OSError) as error:
        print(f"Could not signal pid {held.get('pid')}: {error}")
        return False


def clean_scratch():
    """Free scratch space (venv, caches, weights); never touches /kaggle/working."""
    shutil.rmtree(STATE["scratch"], ignore_errors=True)
