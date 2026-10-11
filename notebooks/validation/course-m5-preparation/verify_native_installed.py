"""Repeat only four native course checks against the accepted installed package."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installation", required=True, type=Path)
    parser.add_argument("--tokenizer", required=True, type=Path)
    args = parser.parse_args()
    provenance = json.loads(args.installation.read_bytes())
    target = Path(provenance["target"])
    for name, expected in provenance["modules"].items():
        assert hashlib.sha256((target/"recovery"/name).read_bytes()).hexdigest() == expected
    environment = dict(os.environ, PYTHONHASHSEED="37", PYTHONUTF8="1")
    environment.pop("PYTHONPATH", None)
    probe = subprocess.check_output([sys.executable, "-c",
        "import recovery; print(recovery.__file__)"], cwd=target, env=environment).decode().strip()
    assert Path(probe).resolve() == (target/"recovery/__init__.py").resolve()
    command = [sys.executable, "-X", "utf8", "-B", "-m", "tests.tokenizer_course_inference",
        "--tokenizer", str(args.tokenizer.resolve())]
    result = subprocess.run(command, cwd=target, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.decode("utf-8", errors="replace"))
    print(json.dumps(dict(command=command, cwd=str(target), module=probe,
        source_pythonpath=False, hash_seed=37, exit_code=result.returncode), indent=2))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
