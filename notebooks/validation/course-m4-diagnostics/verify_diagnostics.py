"""Audit course diagnostic/cost acceptance, handoff and protected starting bytes."""

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
MUTABLE = {"tests/cost_fixture.py", "tests/information_fixture.py", "README.md", "tests/fixtures/README.md",
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course/README.md", "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/M4/M4-T02-course-diagnostics-and-policy-costs.md",
    "docs/todos/course/M4/M4-T03-course-uncertainty-and-missingness.md"}


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
    assert re.search(r"(?m)^ ?M docs/validation/m5-inference-preparation.md$", git("status", "--short"))
    plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    old_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == old_plan.split("## 11. Course living handoff")[0]
    prerequisite = read(ROOT / "notebooks/validation/course-m4-outcomes/completion-audit.json")
    assert prerequisite["status"] == "passed" and prerequisite["reused_real_course_kills"] == 10
    assert prerequisite["suites"]["source-m4-accepted"]["tests"] == [191]
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1]
              for p in (ROOT / "docs/todos/course").glob("M*/*.md")}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    for milestone, done, total, active, ready, blocked in re.findall(
            r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k, v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[k] for k in ("done", "active", "ready", "blocked"))
    assert Counter(states.values()) == (dict(done=9, ready=2, blocked=10) if args.completion else dict(done=8, active=1, ready=1, blocked=11))
    assert states["M3-T01"] == states["M3-T02"] == "done"
    assert states["M4-T01"] == "done"
    assert states["M4-T02"] == ("done" if args.completion else "active")
    assert states["M4-T03"] == ("ready" if args.completion else "blocked")
    assert states["M5-T01"] == "ready"
    documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")}
    documents.add((ROOT / "docs/validation/course-m4-diagnostics-and-policy-costs.md").resolve())
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
    required = ["formulas-corrected", "archive-worker-final"]
    if args.completion:
        required += ["source-m4-accepted", "installed-accepted", "core-accepted", "pip-check", "compile-check"]
    for label in required:
        command = read(FOLDER / f"{label}-command.json")
        assert command["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / command["log"]).read_bytes()).decode("utf-8")
        assert not re.search(r"^FAILED \(|^ERROR:", log, re.M), label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    bundle_summary = None
    if args.completion:
        installed = read(FOLDER / "installed-provenance.json")
        assert installed["exit_code"] == 0 and not installed["source_pythonpath"]
        assert installed["hash_seed"] == 37 and installed["matching_modules"] == 29
        source = read(FOLDER / "source-m4-accepted-command.json")
        installed_command = read(FOLDER / "installed-accepted-command.json")
        # The wrapper records the starting head; the installed receipt records
        # the head when its checks finish. Documentation commits can proceed
        # meanwhile, but production, tests and scientific inputs must match.
        assert source["source_head"] == installed_command["source_head"]
        assert not git("diff", "--name-only", source["source_head"], installed["source_head"],
                       "--", "recovery", "tests", "configs", "pyproject.toml")
        for label, count in {"formulas-corrected": 76, "archive-worker-final": 26,
                "source-m4-accepted": 217, "installed-accepted": 217, "core-accepted": 394}.items():
            assert suites[label]["tests"] == [count], label
        for path, digest in installed["modules"].items():
            assert hashlib.sha256((ROOT / "recovery" / path).read_bytes()).hexdigest() == digest, path
        tables = read(ROOT / "tests/fixtures/course_diagnostic_cost_tables.json.gz")
        assert len(tables["cases"]) == 7
        full = tables["cases"]["full-main-20"]
        assert full["coverage"]["unknown"] == 4110 and full["coverage"]["recorded"] == 2170
        selections = full["costs"]["boundary_selections"]
        assert Counter(str(row["selected_policy"]) for row in selections) == {"K": 22, "None": 36}
        assert len(full["information"]["prefix"]) == 320
        assert len(full["information"]["owner_exposure"]) == 28
        assert len(full["information"]["receipt_timing"]) == 212
        assert len(full["information"]["receipt_information"]) == 864
        workers = read(FOLDER / "original-worker-audit-command.json")
        native = read(FOLDER / "native-original-audit-command.json")
        assert workers["exit_code"] == native["exit_code"] == 0
        bundle_summary = dict(cases=7, coverage=full["coverage"], selections=dict(Counter(str(row["selected_policy"]) for row in selections)),
            prefix_rows=320, owner_exposure_rows=28, receipt_peers=212, receipt_rows=864,
            source_bundles_unchanged=True, no_inference=True)
    record = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        thesis_spec_defaults_todos_and_plan_sections_1_to_10_preserved=True, course_task_states=dict(Counter(states.values())),
        local_references=references, markdown_fragments=fragments, suites=suites, bundle=bundle_summary,
        reused_real_course_kills=10, model_calls=0, gpu_admission=False, runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2)
        output.write("\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
