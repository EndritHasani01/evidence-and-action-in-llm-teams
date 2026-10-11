"""Retain exact CPU commands and lossless logs without overwriting evidence."""

import argparse
from datetime import datetime, timezone
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--temporary-root", type=Path, help="task-owned scratch directory on a drive with sufficient space")
    parser.add_argument("--hash-seed", type=int, help="explicit fresh-process Python hash seed")
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    folder = Path(__file__).resolve().parent
    receipt = folder / f"{args.label}-command.json"
    log = folder / f"{args.label}.txt.gz"
    if not command or receipt.exists() or log.exists():
        parser.error("provide a command and a fresh evidence label")
    started = datetime.now(timezone.utc).isoformat()
    before = time.monotonic()
    environment = dict(os.environ)
    if args.hash_seed is not None:
        environment["PYTHONHASHSEED"] = str(args.hash_seed)
    if args.temporary_root:
        args.temporary_root.resolve().mkdir(parents=True, exist_ok=True)
        environment.update(TEMP=str(args.temporary_root.resolve()), TMP=str(args.temporary_root.resolve()))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment)
    lines = []
    for line in process.stdout:
        lines.append(line)
        sys.stdout.buffer.write(line)
        sys.stdout.buffer.flush()
    process.stdout.close()
    exit_code = process.wait()
    log.write_bytes(gzip.compress(b"".join(lines), mtime=0))
    record = dict(command=command, cwd=str(Path.cwd()), started_utc=started,
                  seconds=time.monotonic() - before, exit_code=exit_code,
                  log=log.name, hash_seed=environment.get("PYTHONHASHSEED"),
                  temporary_root=str(args.temporary_root.resolve()) if args.temporary_root else None)
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
