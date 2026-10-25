"""Command line: python -m recovery.thesis <command> [options].

Every scientific command opens the study (or restores it), does one bounded
piece of work, writes a verified checkpoint and a cell receipt, then exits.
Exit codes: 0 done or skipped, 3 expected stop, 1 unexpected error.
"""

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback
import uuid

from . import MODELS, SCOPES, SOURCE_ROOT, load_config

SCIENTIFIC = {"open", "check", "develop", "freeze", "main", "finish", "declare-stopped"}


def parser():
    p = argparse.ArgumentParser(prog="python -m recovery.thesis")
    p.add_argument("command", choices=["open", "status", "check", "develop", "freeze", "main", "report", "finish",
                                       "show", "declare-stopped", "build-worlds", "env-check"])
    p.add_argument("--run", type=Path)
    p.add_argument("--study", default="thesis-recovery-v1")
    p.add_argument("--source", type=Path, default=SOURCE_ROOT)
    p.add_argument("--source-commit", default="local-uncommitted")
    p.add_argument("--scope", choices=SCOPES, default="cpu")
    p.add_argument("--session")
    p.add_argument("--session-start")
    p.add_argument("--deadline")
    p.add_argument("--scratch", type=Path, default=Path(tempfile.gettempdir()) / "thesis-scratch")
    p.add_argument("--input-root", action="append", default=[])
    p.add_argument("--mirror-repo", default="")
    p.add_argument("--mirror-dir", default="")
    p.add_argument("--start-new", action="store_true")
    p.add_argument("--authorization", default="")
    p.add_argument("--reason", default="")
    p.add_argument("--model", choices=MODELS)
    p.add_argument("--world")
    p.add_argument("--cell")
    p.add_argument("--out", type=Path)
    p.add_argument("--draws", type=int)
    return p


def mirror_from(args):
    from .checkpoint import DirectoryMirror, HubMirror
    if args.mirror_repo:
        return HubMirror(args.mirror_repo, os.environ.get("HF_TOKEN", ""))
    if args.mirror_dir:
        return DirectoryMirror(args.mirror_dir)
    return None


def banner(kind, text):
    line = "=" * 78
    print(f"{line}\n{kind}: {text}\n{line}", flush=True)


def write_receipt(run, session, command, value):
    from ..i01.archive import atomic_json
    folder = Path(run) / "receipts" / "cells" / session
    folder.mkdir(parents=True, exist_ok=True)
    n = len(list(folder.glob("*.json"))) + 1
    atomic_json(folder / f"{n:02d}-{command}.json", value)


def env_check(source):
    """Pinned packages and isolated startup inside the study venv."""
    import importlib.metadata
    from ..i01.runtime import inventory
    lock = Path(source) / "configs/i01-runtime.lock"
    expected = {line.split("==")[0]: line.split("==")[1].split()[0]
                for line in lock.read_text().splitlines() if "==" in line}
    installed = {name: importlib.metadata.version(name) for name in expected}
    if installed != expected:
        raise SystemExit("installed packages differ from configs/i01-runtime.lock: " +
                         json.dumps({k: (installed[k], v) for k, v in expected.items() if installed[k] != v}))
    info = inventory()
    if not info["venv"] or not info["isolated"] or not info["site_processing_disabled"] or info["hook_automatically_imported"]:
        raise SystemExit("isolated startup acceptance failed: " + json.dumps(info))
    print(json.dumps(dict(passed=True, python=sys.version.split()[0], packages=len(installed), startup=info)))
    return 0


def main(argv=None):
    args = parser().parse_args(argv)
    if args.command == "build-worlds":
        from .worlds import write_inputs
        print(json.dumps(write_inputs(args.source), indent=1))
        return 0
    if args.command == "env-check":
        return env_check(args.source)
    if args.run is None:
        raise SystemExit("--run is required")
    if args.command == "show":
        from .analysis import show
        print(show(args.run, args.model, args.world, args.cell))
        return 0
    from .run import EXIT_DONE, EXIT_ERROR, EXIT_STOPPED, Stop, close_controller, install_stop_handler, open_controller
    from .checkpoint import utc
    now = datetime.now(timezone.utc)
    session = args.session or str(uuid.uuid4())
    session_start = datetime.fromisoformat(args.session_start) if args.session_start else now
    deadline = datetime.fromisoformat(args.deadline) if args.deadline else now + timedelta(hours=11)
    if args.command == "report" and not (args.run / "lock.json").exists() and args.out:
        from .analysis import write_report
        write_report(args.run, args.out, draws=args.draws)
        print(f"report written to {args.out}")
        return 0
    started = utc()
    mirror = None
    if args.command in SCIENTIFIC:
        try:
            mirror = mirror_from(args)
        except Exception as error:  # an unreachable mirror never blocks work; local checkpoints continue
            banner("WARNING", f"checkpoint mirror unavailable ({type(error).__name__}: {error}); continuing without it")
    try:
        ctl = open_controller(args.run, study=args.study, source=args.source, source_commit=args.source_commit,
                              scope=args.scope, session=session, session_start=session_start, deadline=deadline,
                              scratch=args.scratch, start_new=args.start_new and args.command == "open",
                              roots=[Path(r) for r in args.input_root] if args.command == "open" else (),
                              mirror=mirror, command=args.command, restore_allowed=args.command == "open")
    except Stop as stop:
        banner("STOPPED", str(stop))
        return EXIT_STOPPED
    install_stop_handler(ctl)
    status, message, checkpoint = EXIT_DONE, "done", None
    try:
        if args.command == "open":
            print(json.dumps(summary(ctl), indent=1))
        elif args.command == "status":
            print(json.dumps(summary(ctl), indent=1))
        elif args.command == "check":
            from .checks import run_checks
            receipt = run_checks(ctl.source, ctl.config, scripted=ctl.profile.scripted, scratch=ctl.scratch,
                                 receipts=ctl.run / "receipts", progress=ctl.say)
            ctl.bind("input_limit", receipt["input_limit"])
            ctl.put("checks", dict(receipt, binding=ctl.store.meta("binding"), session=session, at=utc()))
            for line in receipt["checks"]:
                ctl.say("check passed: " + line)
        elif args.command == "develop":
            ctl.develop()
        elif args.command == "freeze":
            authorization = args.authorization
            if ctl.profile.name == "rehearsal" and not authorization and ctl.meta("gate_report"):
                authorization = ctl.meta("gate_report")["id"]
            ctl.freeze(authorization)
        elif args.command == "main":
            print(json.dumps(ctl.main(), indent=1))
        elif args.command == "report":
            from .analysis import write_report
            result = write_report(ctl.run, args.out, draws=args.draws)
            print(f"status {result['status']}; report at {(args.out or ctl.run / 'reports') / 'report.md'}")
        elif args.command == "declare-stopped":
            ctl.declare_stopped(args.reason)
        elif args.command == "finish":
            ctl.touch_session(closed=True, ended=utc())
    except Stop as stop:
        message = str(stop)
        status = EXIT_DONE if message.startswith("skipped") else EXIT_STOPPED
        banner("SKIPPED" if status == EXIT_DONE else "STOPPED", message)
    except Exception as error:  # keep evidence, export what exists, never hide the cause
        status, message = EXIT_ERROR, f"{type(error).__name__}: {error}"
        (ctl.run / "receipts").mkdir(exist_ok=True)
        with (ctl.run / "receipts" / "errors.log").open("a", encoding="utf-8") as stream:
            stream.write(f"\n[{utc()}] {args.command}\n{traceback.format_exc()}")
        banner("ERROR", message + " (full traceback in receipts/errors.log)")
    finally:
        try:
            ctl.close_slots()
            if args.command in SCIENTIFIC:
                checkpoint = ctl.maybe_checkpoint(force=True, reason=f"{args.command} ({message[:60]})")
        except Exception as error:
            banner("ERROR", f"checkpoint export failed: {error}; the previous checkpoint remains valid")
            status = EXIT_ERROR
        write_receipt(ctl.run, session, args.command, dict(
            command=args.command, scope=args.scope, started=started, ended=utc(), exit=status, message=message,
            checkpoint=None if not checkpoint else {k: checkpoint[k] for k in ("path", "seq", "sha256", "mirror")},
            kind="checkpoint" if checkpoint else "receipt"))
        close_controller(ctl)
    return status


def summary(ctl):
    freeze = ctl.meta("freeze")
    gates = {m: (ctl.meta(f"gates/{m}") or {}).get("admitted") for m in MODELS}
    dev = {m: sum(ctl.world_complete(m, ctl.worlds[i]) for i in ctl.profile.development) for m in MODELS}
    return dict(study=ctl.study, profile=ctl.profile.name, scope=ctl.scope, checkpoint_seq=ctl.meta("checkpoint_seq", 0),
                input_limit=ctl.meta("input_limit"), checks_passed=bool((ctl.meta("checks") or {}).get("passed")),
                development_worlds_complete=dev, development_total=len(ctl.profile.development),
                gates_admitted=gates, gate_report=(ctl.meta("gate_report") or {}).get("id"),
                frozen=None if not freeze else dict(n=freeze["n"], models=freeze["models"]),
                main=ctl.main_status(), declared_stopped=bool(ctl.meta("declared_stopped")),
                aggregate_gpu_hours=round(ctl.aggregate_hours(), 2), lost_gpu_sessions=ctl.lost_sessions(),
                attempts=sum(ctl.counts.values()))


if __name__ == "__main__":
    sys.exit(main())
