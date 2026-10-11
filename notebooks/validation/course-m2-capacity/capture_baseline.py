"""Capture starting tracked bytes once, including unrelated working edits."""

import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).with_name("baseline-files.json.gz")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode()


if __name__ == "__main__":
    names = git("ls-files", "-z").split("\0")
    record = dict(head=git("rev-parse", "HEAD").strip(), status=git("status", "--short"),
        files={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
               for p in names if p and (ROOT / p).is_file()})
    with OUTPUT.open("xb") as output:
        output.write(gzip.compress((json.dumps(record, sort_keys=True) + "\n").encode(), mtime=0))
    print(json.dumps(dict(head=record["head"], files=len(record["files"]), status=record["status"])))
