"""Audit report acceptance, prerequisite reuse, protected bytes and course handoff."""

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
    "docs/todos/course/M4/M4-T04-course-report-and-cpu-gate.md",
    "recovery/report.py", "recovery/__main__.py", "recovery/figures.py"}
PREREQUISITES = ("course-m1-inputs", "course-m2-protocol", "course-m2-interventions",
    "course-m2-capacity", "course-m3-workers", "course-m3-accounting",
    "course-m4-outcomes", "course-m4-diagnostics", "course-m4-uncertainty")


def read(path):
    path = Path(path)
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


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
    prior_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == prior_plan.split("## 11. Course living handoff")[0]
    prior = {name: read(ROOT / "notebooks/validation" / name / "completion-audit.json") for name in PREREQUISITES}
    assert all(p["status"] == "passed" for p in prior.values())
    assert prior["course-m4-uncertainty"]["suites"]["source-accepted"]["tests"] == [70]
    assert prior["course-m4-diagnostics"]["suites"]["core-accepted"]["tests"] == [394]
    assert prior["course-m4-diagnostics"]["reused_real_course_kills"] == 10

    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1]
        for p in (ROOT / "docs/todos/course").glob("M*/*.md")}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    for milestone, done, total, active, ready, blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k, v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[k] for k in ("done", "active", "ready", "blocked"))
    assert Counter(states.values()) == (dict(done=11, ready=1, blocked=9) if args.completion else dict(done=10, active=1, ready=1, blocked=9))
    assert states["M4-T04"] == ("done" if args.completion else "active") and states["M5-T01"] == "ready"
    assert all(states[k] == "blocked" for k in states if k.startswith("M6"))
    total = re.search(r"\*\*(\d+)/21 course tasks done; (\d+) remaining; (\d+) active; (\d+) ready; (\d+) blocked", index)
    count = Counter(states.values())
    assert tuple(map(int, total.groups())) == (count["done"], 21-count["done"], count["active"], count["ready"], count["blocked"])

    audit_path = ROOT / "docs/validation/course-m4-report-and-cpu-gate.md"
    audit = audit_path.read_text(encoding="utf-8")
    plan_rows = re.findall(r"^\| ([^|]+) \|", plan.split("## 9. Coverage map")[1].split("## 10.")[0], re.M)[1:]
    rows = re.findall(r"^\| ([^|]+) \|", audit.split("## Plan coverage audit")[1].split("## Seven specification")[0], re.M)[1:]
    assert rows == plan_rows and len(rows) == 22
    categories = re.findall(r"^\| ([1-7]\. [^|]+) \|", audit, re.M)
    assert len(categories) == 7
    helper = ROOT / "notebooks/validation/m5-attention-memory/check_document_links.py"
    sys.path.insert(0, str(helper.parent))
    anchors = runpy.run_path(str(helper))["anchors"]
    documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")} | {audit_path.resolve()}
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

    labels = ["focused-accepted", "archive-create-corrected", "report-review-corrected"]
    if args.completion: labels += ["source-accepted", "installed-accepted", "core-focused", "pip-check", "compile-check"]
    suites = {}
    for label in labels:
        receipt = read(FOLDER / f"{label}-command.json")
        assert receipt["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / receipt["log"]).read_bytes()).decode("utf-8")
        assert not re.search(r"^FAILED \(|^ERROR:|^OK \(skipped=", log, re.M), label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    if args.completion:
        package = read(FOLDER / "installed-provenance.json")
        assert package["exit_code"] == 0 and not package["source_pythonpath"] and package["matching_modules"] == 29
        for name, digest in package["modules"].items():
            assert hashlib.sha256((ROOT / "recovery" / name).read_bytes()).hexdigest() == digest, name
        source = read(FOLDER / "source-accepted-command.json")
        installed = read(FOLDER / "installed-accepted-command.json")
        assert source["source_head"] == installed["source_head"] == package["source_head"]
        assert not git("diff", "--name-only", source["source_head"], "HEAD", "--", "recovery", "tests", "configs", "pyproject.toml")
        assert suites["source-accepted"]["tests"] == suites["installed-accepted"]["tests"] == [52]
        assert suites["core-focused"]["tests"] == [33]
    reports = read(ROOT / "tests/fixtures/course_report_tables.json.gz")
    full = reports["cases"]["full-main-20"]["report"]
    assert len(reports["cases"]) == 8 and full["coverage"]["recorded"] == 2170 and full["coverage"]["unknown"] == 4110
    assert full["execution"]["status"] == "incomplete" and full["execution"]["accepted_main_freeze"] is None
    visual = read(FOLDER / "figure-review.json")
    assert visual["status"] == "passed" and len(visual["inspected_pngs"]) == 10
    result = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        thesis_defaults_todos_artifacts_and_plan_sections_1_to_10_preserved=True,
        course_task_states=dict(Counter(states.values())), plan_rows=len(rows), consistency_categories=len(categories),
        local_references=references, markdown_fragments=fragments, suites=suites,
        prerequisite_audits={n: "passed and unchanged" for n in PREREQUISITES},
        reused_core_methods=394, reused_real_course_kills=10,
        reports=dict(scopes=8, portable_scopes=5, figure_pairs=35, seed=reports["seed"], full_main_coverage=full["coverage"]),
        model_calls=0, gpu_admission=False, runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
