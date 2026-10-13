"""Repeat the new proof against unchanged installed code outside the checkout."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", required=True, type=Path)
    parser.add_argument("--temporary-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("retain old evidence; use a fresh output")
    prior = json.loads((ROOT/"notebooks/validation/course-m5-preparation/installed-provenance.json").read_bytes())
    target = Path(tempfile.mkdtemp(prefix="r7-installed-", dir=args.temporary_root))
    installed = Path(prior["target"])/"recovery"
    for name, digest in prior["modules"].items():
        if hashlib.sha256((installed/name).read_bytes()).hexdigest() != digest or hashlib.sha256((ROOT/"recovery"/name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"accepted installed module differs: {name}")
    shutil.copytree(installed, target/"recovery", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name in ("tests", "scripts"):
        shutil.copytree(ROOT/name, target/name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    relative = "tests/course_capacity_tightening.py"
    committed = subprocess.check_output(["git", "show", head+":"+relative], cwd=ROOT)
    copied = (target/relative).read_bytes()
    if copied.replace(b"\r\n",b"\n") != committed:
        raise ValueError("new proof is not the exact committed source")
    environment = dict(os.environ, PYTHONHASHSEED="211", PYTHONUTF8="1")
    environment.pop("PYTHONPATH",None)
    probe = subprocess.check_output([sys.executable,"-X","utf8","-B","-c",
        "import recovery; print(recovery.__file__)"],cwd=target,env=environment).decode().strip()
    if Path(probe).resolve() != (target/"recovery/__init__.py").resolve():
        raise ValueError("outside verification imported a different package")
    output = target/"native-tightening.json"
    command = [sys.executable,"-X","utf8","-B","-m","tests.course_capacity_tightening",
        "--tokenizer",str(args.tokenizer.resolve()),"--output",str(output)]
    result = subprocess.run(command,cwd=target,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(result.stdout.decode("utf-8",errors="replace"),flush=True)
    if result.returncode:
        return result.returncode
    report = json.loads(output.read_bytes())
    if report != json.loads((FOLDER/"native-tightening-source.json").read_bytes()):
        raise ValueError("independent native proof report differs")
    record = dict(source_head=head, accepted_installed_source_head=prior["source_head"],
        matching_installed_modules=len(prior["modules"]), module=probe,cwd=str(target),
        proof_sha256=hashlib.sha256(committed).hexdigest(), source_pythonpath=False,
        hash_seed=211, command=command, report_matches_source=True, report=report,
        gpu_execution=False, model_weights_loaded=False)
    with args.output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(record,stream,indent=2)
        stream.write("\n")
    print(json.dumps({k:v for k,v in record.items() if k != "report"},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
