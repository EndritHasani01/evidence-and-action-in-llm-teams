"""Build and verify the CPU package outside the checkout with source paths absent."""

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


def run(command, directory, environment):
    result = subprocess.run(command, cwd=directory, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.decode("utf-8", errors="replace"), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=FOLDER / "installed-provenance.json")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("use a fresh provenance output path")
    environment = dict(os.environ, PYTHONHASHSEED="37", PYTHONUTF8="1")
    environment.pop("PYTHONPATH", None)
    target = Path(tempfile.mkdtemp(prefix="recovery-course-m2-interventions-installed-"))
    interpreter = ROOT / ".venv/Scripts/python.exe"
    run([str(interpreter), "-m", "pip", "wheel", str(ROOT), "--no-deps", "--wheel-dir", str(target)], target, environment)
    wheel, = target.glob("*.whl")
    run([str(interpreter), "-m", "pip", "install", "--no-deps", "--target", str(target), str(wheel)], target, environment)
    shutil.copytree(ROOT / "tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    modules = {}
    for source in (ROOT / "recovery").glob("*.py"):
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256((target / "recovery" / source.name).read_bytes()).hexdigest() == digest, source.name
        modules[source.name] = digest
    # Resolve the imported module in the actual installed interpreter and cwd.
    command = [str(interpreter), "-X", "utf8", "-c", "import json,recovery,sys; print(json.dumps(dict(module=recovery.__file__, paths=sys.path)))"]
    actual = json.loads(subprocess.check_output(command, cwd=target, env=environment))
    assert Path(actual["module"]).resolve() == (target / "recovery/__init__.py").resolve()
    assert str(ROOT).casefold() not in {str(Path(p).resolve()).casefold() for p in actual["paths"] if p}
    suites = ["tests.course_intervention_checks", "tests.round_checks", "tests.event_checks", "tests.replay_checks",
              "tests.course_protocol_checks", "tests.course_settings_checks", "tests.test_course_limits"]
    command = [str(interpreter), "-X", "utf8", "-m", "unittest", *suites, "-v"]
    run(command, target, environment)
    # Validate the full/core discovery boundary without rerunning unchanged
    # lifecycle/report suites. This CLI's ordinary loader must include course
    # interventions only in full CPU mode, with saved inputs checked first.
    run([str(interpreter), "-S", "-X", "utf8", "-c",
         "import unittest; s=unittest.defaultTestLoader.discover('tests',top_level_dir='.'); "
         "flatten=lambda s:[t for v in s for t in (flatten(v) if isinstance(v,unittest.TestSuite) else [v])]; "
         "ids=[t.id() for t in flatten(s)]; assert not any('course_intervention' in i for i in ids); "
         "assert not any('tokenizer_course_interventions' in i for i in ids); print('Core discovery excludes optional intervention and native suites.')"], target, environment)
    run([str(interpreter), "-m", "pip", "check"], target, environment)
    record = dict(source_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        target=str(target), interpreter=str(interpreter), module=actual["module"], source_pythonpath=False,
        hash_seed=37, matching_modules=len(modules), modules=modules, command=command,
        cwd=str(target), exit_code=0, wheel=wheel.name, wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest())
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
