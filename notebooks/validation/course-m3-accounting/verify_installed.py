"""Verify course accounting/lifecycle and CPU children from a committed wheel."""

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent


def run(command, directory, environment):
    result = subprocess.run(command, cwd=directory, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.decode("utf-8", errors="replace"), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists()
    target = Path(tempfile.mkdtemp(prefix="recovery-course-accounting-installed-"))
    interpreter = ROOT / ".venv/Scripts/python.exe"
    environment = dict(os.environ, PYTHONHASHSEED="37", PYTHONUTF8="1")
    environment.pop("PYTHONPATH", None)
    run([str(interpreter), "-m", "pip", "wheel", str(ROOT), "--no-deps", "--wheel-dir", str(target)], target, environment)
    wheel, = target.glob("*.whl")
    run([str(interpreter), "-m", "pip", "install", "--no-deps", "--target", str(target), str(wheel)], target, environment)
    shutil.copytree(ROOT / "tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(ROOT / "configs", target / "configs")
    modules = {}
    for source in (ROOT / "recovery").glob("*.py"):
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256((target / "recovery" / source.name).read_bytes()).hexdigest() == digest
        modules[source.name] = digest
    probe = [str(interpreter), "-X", "utf8", "-c", "import json,recovery,sys; print(json.dumps(dict(module=recovery.__file__,paths=sys.path)))"]
    actual = json.loads(subprocess.check_output(probe, cwd=target, env=environment))
    assert Path(actual["module"]).resolve() == (target / "recovery/__init__.py").resolve()
    assert str(ROOT).casefold() not in {str(Path(p).resolve()).casefold() for p in actual["paths"] if p}
    suites = ["tests.durable_checks", "tests.worker_checks", "tests.course_worker_checks",
              "tests.accounting_checks", "tests.course_accounting_checks", "tests.lifecycle_checks", "tests.course_lifecycle_checks"]
    command = [str(interpreter), "-X", "utf8", "-m", "unittest", *suites, "-v"]
    run(command, target, environment)
    # The unchanged failure/scheduling fixtures retain exact scientific records.
    run([str(interpreter), "-X", "utf8", "-m", "tests.course_lifecycle_archive", "--audit-only"], target, environment)
    run([str(interpreter), "-X", "utf8", "-m", "tests.course_worker_archive", "--audit-only"], target, environment)
    run([str(interpreter), "-X", "utf8", "-m", "tests.lifecycle_archive", "--audit-only"], target, environment)
    run([str(interpreter), "-m", "pip", "check"], target, environment)
    record = dict(source_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        target=str(target), interpreter=str(interpreter), module=actual["module"], source_pythonpath=False,
        matching_modules=len(modules), modules=modules, hash_seed=37, command=command, cwd=str(target), exit_code=0,
        wheel=wheel.name, wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),
        packages={p: importlib.metadata.version(p) for p in
            ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")})
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
