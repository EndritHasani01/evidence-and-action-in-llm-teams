"""Audit course uncertainty receipts, protected bytes and the existing handoff."""

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

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
MUTABLE = {"README.md", "tests/fixtures/README.md", "docs/IMPLEMENTATION_PLAN.md",
    "docs/todos/course/README.md", "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/M4/M4-T03-course-uncertainty-and-missingness.md",
    "docs/todos/course/M4/M4-T04-course-report-and-cpu-gate.md",
    "recovery/uncertainty.py", "recovery/report.py", "recovery/__main__.py"}


def read(path):
    path = Path(path)
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


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
    for name, digest in protected.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    user_edit = "docs/validation/m5-inference-preparation.md"
    assert user_edit not in git("diff", "--cached", "--name-only").splitlines()
    assert re.search(r"(?m)^ ?M docs/validation/m5-inference-preparation.md$", git("status", "--short"))
    plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    assert plan.split("## 11. Course living handoff")[0] == git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md").split("## 11. Course living handoff")[0]
    prior = read(ROOT / "notebooks/validation/course-m4-diagnostics/completion-audit.json")
    assert prior["status"] == "passed" and prior["reused_real_course_kills"] == 10
    assert prior["suites"]["source-m4-accepted"]["tests"] == prior["suites"]["installed-accepted"]["tests"] == [217]
    assert prior["suites"]["core-accepted"]["tests"] == [394]
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1]
              for p in (ROOT / "docs/todos/course").glob("M*/*.md")}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    for milestone, done, total, active, ready, blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k, v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[k] for k in ("done", "active", "ready", "blocked"))
    expected = dict(done=10, ready=2, blocked=9) if args.completion else dict(done=9, active=1, ready=1, blocked=10)
    assert Counter(states.values()) == expected
    assert states["M4-T03"] == ("done" if args.completion else "active")
    assert states["M4-T04"] == ("ready" if args.completion else "blocked")
    assert states["M5-T01"] == "ready"
    documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")}
    documents.add((ROOT / "docs/validation/course-m4-uncertainty-and-missingness.md").resolve())
    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    references = fragments = 0
    for source in set(ROOT.glob("docs/**/*.md")) | {ROOT / p for p in ("README.md", "AGENTS.md", "PROJECT_SPECIFICATION.md", "tests/fixtures/README.md")}:
        for link in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            link = link.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", link): continue
            name, _, fragment = link.partition("#")
            target = (source.parent / re.sub(r":\d+$", "", unquote(name))).resolve() if name else source.resolve()
            if source.resolve() not in documents and target not in documents: continue
            assert target.exists(), (source, link)
            references += 1
            if fragment and target.suffix == ".md":
                assert unquote(fragment) in anchors(target), (source, link)
                fragments += 1
    labels = ["formulas-accepted", "archive-create", "archive-table-corrected", "core-focused", "pip-check", "compile-check"]
    if args.completion: labels += ["source-accepted", "installed-accepted"]
    suites = {}
    for label in labels:
        receipt = read(FOLDER / f"{label}-command.json")
        assert receipt["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / receipt["log"]).read_bytes()).decode("utf-8")
        assert not re.search(r"^FAILED \(|^ERROR:|^OK \(skipped=", log, re.M), label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    if args.completion:
        installed = read(FOLDER / "installed-provenance.json")
        assert installed["exit_code"] == 0 and not installed["source_pythonpath"] and installed["matching_modules"] == 29
        for path, digest in installed["modules"].items(): assert hashlib.sha256((ROOT / "recovery" / path).read_bytes()).hexdigest() == digest, path
        source = read(FOLDER / "source-accepted-command.json")
        package = read(FOLDER / "installed-accepted-command.json")
        assert source["source_head"] == package["source_head"]
        assert not git("diff", "--name-only", source["source_head"], installed["source_head"], "--", "recovery", "tests", "configs", "pyproject.toml")
        assert suites["source-accepted"]["tests"] == suites["installed-accepted"]["tests"] == [70]
    assert suites["core-focused"]["tests"] == [19]
    archive = read(ROOT / "tests/fixtures/course_uncertainty_tables.json.gz")
    full = archive["cases"]["full-main-20"]
    assert len(archive["cases"]) == 7 and full["coverage"]["unknown"] == 4110 and full["coverage"]["recorded"] == 2170
    assert sum(r["independent_shared_linear_rows"] for r in archive["independent_checks"].values()) == 11422
    record = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        thesis_spec_defaults_todos_and_plan_sections_1_to_10_preserved=True, course_task_states=dict(Counter(states.values())),
        local_references=references, markdown_fragments=fragments, suites=suites,
        bundle=dict(cases=7, coverage=full["coverage"], independent_linear_rows=11422, seed=20261011),
        reused_prerequisite_source_installed=217, reused_core_methods=394, reused_real_course_kills=10,
        model_calls=0, gpu_admission=False, runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
