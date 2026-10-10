"""Retain exact CPU commands and lossless logs without overwriting evidence."""

import argparse
from datetime import datetime, timezone
import gzip
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_bytes(gzip.compress(result.stdout, mtime=0))
    record = dict(command=command, cwd=str(Path.cwd()), started_utc=started,
                  seconds=time.monotonic() - before, exit_code=result.returncode,
                  log=log.name, hash_seed=os.environ.get("PYTHONHASHSEED"))
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(result.stdout.decode("utf-8", errors="replace"))
    print(json.dumps(record, indent=2))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
