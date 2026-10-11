"""Audit course worker evidence, task handoff, links and protected starting bytes."""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
from urllib.parse import unquote
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
MUTABLE = {"recovery/__main__.py", "recovery/runner.py", "recovery/storage.py", "recovery/workers.py",
    "tests/lifecycle_fixture.py", "tests/lifecycle_worker.py", "tests/worker_archive.py", "README.md", "tests/fixtures/README.md",
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course/README.md", "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/M3/M3-T01-course-durable-workers-and-failures.md",
    "docs/todos/course/M3/M3-T02-course-accounting-and-lifecycle-gate.md"}


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if Path(path).suffix == ".gz" else data)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--completion", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    baseline = read(FOLDER / "baseline-files.json.gz")
    protected = {p: h for p, h in baseline["files"].items() if p not in MUTABLE}
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert "docs/validation/m5-inference-preparation.md" not in git("diff", "--cached", "--name-only").splitlines()
    assert " M docs/validation/m5-inference-preparation.md" in git("status", "--short")
    plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    old_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == old_plan.split("## 11. Course living handoff")[0]
    prerequisite = read(ROOT / "notebooks/validation/course-m2-capacity/handoff-audit.json")
    assert prerequisite["status"] == "passed" and prerequisite["witness"]["logical_opportunities"] == 7458
    assert prerequisite["resident_tokens_upper"] == 156251
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1]
              for p in (ROOT / "docs/todos/course").glob("M*/*.md")}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    for milestone, done, total, active, ready, blocked in re.findall(
            r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k, v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[k] for k in ("done", "active", "ready", "blocked"))
    assert Counter(states.values()) == (dict(done=6, ready=1, blocked=14) if args.completion else dict(done=5, active=1, blocked=15))
    assert states["M3-T01"] == ("done" if args.completion else "active")
    assert states["M3-T02"] == ("ready" if args.completion else "blocked")
    documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")}
    documents.add((ROOT / "docs/validation/course-m3-durable-workers-and-failures.md").resolve())
    documents.update(p.resolve() for p in (ROOT / "docs/todos/course").glob("M*/*.md"))
    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    references = fragments = 0
    for source in set(ROOT.glob("docs/**/*.md")) | {ROOT / p for p in ("README.md", "AGENTS.md", "PROJECT_SPECIFICATION.md", "tests/fixtures/README.md")}:
        for link in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            link = link.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", link): continue
            name, _, fragment = link.partition("#")
            name = re.sub(r":\d+$", "", unquote(name))
            target = (source.parent / name).resolve() if name else source.resolve()
            if source.resolve() not in documents and target not in documents: continue
            assert target.exists(), (source, link)
            references += 1
            if fragment and target.suffix == ".md":
                assert unquote(fragment) in anchors(target), (source, link)
                fragments += 1
    suites = {}
    required = ["baseline-durable", "course-final"]
    if args.completion:
        required += ["course-archive", "course-reproduction", "offline-audit", "native-workers-corrected",
                     "source-full", "installed-checks", "core-checks", "pip-check"]
    for label in required:
        command = read(FOLDER / f"{label}-command.json")
        assert command["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / command["log"]).read_bytes()).decode("utf-8")
        assert not re.search(r"^FAILED \(|^ERROR:", log, re.M), label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    native = None
    if args.completion:
        native = read(FOLDER / "native-provenance.json")
        assert native["model_calls"] == 0 and native["replay_uses"] == 8 and native["exact_native_request_checks"] == 20
        installed = read(FOLDER / "installed-provenance.json")
        assert installed["exit_code"] == 0 and not installed["source_pythonpath"]
        for path, digest in installed["modules"].items():
            assert hashlib.sha256((ROOT / "recovery" / path).read_bytes()).hexdigest() == digest, path
        with ZipFile(ROOT / "tests/fixtures/course_worker_run.zip") as bundle:
            cases = json.loads(bundle.read("evidence.json"))["cases"]
            kills = [name for name in bundle.namelist() if re.search(r"/kill-\d+\.json$", name)]
            assert len(cases) == 16 and len(kills) == 10
            assert all(json.loads(bundle.read(p))["inference_children_exited"] for p in kills)
        command = read(FOLDER / "offline-audit-command.json")
        log = gzip.decompress((FOLDER / command["log"]).read_bytes()).decode()
        bundle_summary = json.loads(next(line for line in log.splitlines() if line.startswith('{"attempts"')))
    else:
        bundle_summary = None
    record = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        thesis_spec_defaults_todos_and_plan_sections_1_to_10_preserved=True, course_task_states=dict(Counter(states.values())),
        local_references=references, markdown_fragments=fragments, suites=suites, bundle=bundle_summary,
        native=native, model_calls=0, gpu_admission=False, runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
