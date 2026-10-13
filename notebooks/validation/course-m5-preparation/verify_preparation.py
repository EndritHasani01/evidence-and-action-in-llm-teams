"""Audit the verified CPU checkpoint while keeping unresolved R7/task blocked."""

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
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
MUTABLE = {"README.md", "tests/fixtures/README.md", "docs/IMPLEMENTATION_PLAN.md",
    "docs/todos/course/README.md", "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/M5/M5-T01-course-inference-and-smoke-preparation.md",
    "docs/todos/course/M5/M5-T02-course-hardware-smoke-and-memory.md",
    "recovery/__main__.py", "scripts/build_kaggle_bundle.py"}


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if str(path).endswith(".gz") else data)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from ids(item)
        else:
            yield item.id()


def registration():
    sys.path.insert(0, str(ROOT))
    try:
        from recovery.__main__ import main
        collected = {}
        for mode, arguments in (("core", ["--core-only"]), ("full", [])):
            def collect(suite):
                collected[mode] = list(ids(suite))
                return SimpleNamespace(wasSuccessful=lambda: True)
            with patch("sys.argv", ["recovery", "validate", "--regime", "course",
                    "--config", str(ROOT/"configs/course-inputs.toml"), *arguments]), \
                    patch("unittest.TextTestRunner.run", side_effect=collect):
                assert main() == 0
        assert not any("_FailedTest" in test for values in collected.values() for test in values)
        course = [t for t in collected["full"] if t.startswith("tests.course_inference_checks.")]
        assert len(course) == len(set(course)) == 5
        assert not any(t.startswith("tests.course_inference_checks.") for t in collected["core"])
        return dict(core_methods_collected=len(collected["core"]), full_methods_collected=len(collected["full"]),
            course_inference_registered_once_only_in_full=len(course), collection_only_no_bodies_run=True)
    finally:
        sys.path.pop(0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists()
    baseline = read(FOLDER/"baseline-files.json.gz")
    protected = {p:h for p,h in baseline["files"].items() if p not in MUTABLE}
    for name, expected in protected.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
    plan = (ROOT/"docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    prior_plan = git("show", baseline["head"]+":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == prior_plan.split("## 11. Course living handoff")[0]
    prior = read(ROOT/"notebooks/validation/course-m4-report/completion-audit.json")
    assert prior["status"] == "passed" and prior["plan_rows"] == 22 and prior["consistency_categories"] == 7
    assert all(v == "passed and unchanged" for v in prior["prerequisite_audits"].values())
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1]
        for p in (ROOT/"docs/todos/course").glob("M*/*.md")}
    index = (ROOT/"docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    assert Counter(states.values()) == dict(done=11, blocked=10)
    assert states["M5-T01"] == "blocked" and all(states[k] == "blocked" for k in states if k.startswith("M6"))
    for milestone, done, total, active, ready, blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k,v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int,(done,active,ready,blocked))) == tuple(counts[k] for k in ("done","active","ready","blocked"))
    total = re.search(r"\*\*(\d+)/21 course tasks done; (\d+) remaining; (\d+) active; (\d+) ready; (\d+) blocked", index)
    assert tuple(map(int,total.groups())) == (11,10,0,0,10)

    suites = {}
    for name, count, skipped in (("source-final",64,0),("installed-corrected",64,0),
            ("native-course-final",4,0),("native-installed",4,0),("core-corrected",37,2)):
        command = read(FOLDER/(name+"-command.json"))
        log = gzip.decompress((FOLDER/command["log"]).read_bytes()).decode("utf-8")
        assert command["exit_code"] == 0 and re.findall(r"Ran (\d+) tests?",log) == [str(count)]
        actual_skips = int(re.search(r"OK \(skipped=(\d+)\)",log)[1]) if "OK (skipped=" in log else 0
        assert actual_skips == skipped
        suites[name] = dict(methods=count, skipped=skipped, source_head=command["source_head"], exit_code=0)
    source_head = suites["source-final"]["source_head"]
    assert suites["installed-corrected"]["source_head"] == source_head
    installed = read(FOLDER/"installed-provenance.json")
    assert installed["source_head"] == source_head and installed["matching_modules"] == 29
    assert installed["source_pythonpath"] is False and installed["exit_code"] == 0
    for name, expected in installed["modules"].items():
        assert hashlib.sha256((ROOT/"recovery"/name).read_bytes()).hexdigest() == expected
    # Runtime/request sources are committed at the packet head; prose is not runtime.
    changed = git("diff", source_head, "--name-only", "--", "recovery", "scripts", "tests", "configs", "pyproject.toml")
    assert set(changed.splitlines()) <= {"tests/fixtures/README.md"}, changed
    for label in ("metadata-index-accepted","exact-requests-corrected","packet-build-initial","notebook-corrected"):
        assert read(FOLDER/(label+"-command.json"))["exit_code"] == 0
    memory = read(FOLDER/"inputs/memory-review.json")
    requests = read(FOLDER/"inputs/smoke-requests.json.gz")
    assert memory["envelope"]["resident_tokens_upper"] == 156251
    assert memory["complete_live_memory_upper_bound_bytes"] is None
    assert sum(memory["known_or_conditional_tensor_components"].values()) == 9172843936
    assert not memory["preparation_admitted"] and not memory["weight_staging_permitted"]
    assert not memory["terminal_model_feasibility_failure"]
    assert len(requests["requests"]) == 24 and not requests["inference_executable"]
    assert all(not r["executed"] and r["outcome"] is None for r in requests["requests"])
    assert all(requests[k] is None for k in ("prior_attempts","prior_allocated_gpu_seconds",
        "remaining_smoke_attempts","remaining_smoke_gpu_seconds","provider_quota","provider_duration"))
    manifest = read(FOLDER/"packet/source-manifest.json.gz")
    review = read(FOLDER/"packet/verification.json")
    assert manifest["source_baseline_commit"] == review["source_commit"] == source_head
    assert review["notebook_cells_executed"] == 3 and len(review["reopened_closed_exports"]) == 2
    assert review["wrong_source_rejected"] and review["existing_output_preserved"]
    assert review["payload_sha256"] == manifest["archive_sha256"] and not review["gpu_admission"]
    assert hashlib.sha256((FOLDER/"packet/preflight-results.zip").read_bytes()).hexdigest() == review["export_zip_sha256"]
    constants = runpy.run_path(str(ROOT/"scripts/build_kaggle_bundle.py"))
    BASELINE_COMMIT, SOURCE_ARCHIVE_SHA256 = constants["BASELINE_COMMIT"], constants["SOURCE_ARCHIVE_SHA256"]
    old = read(ROOT/"dist/m5-kaggle-source-v2/source-manifest.json")
    assert old["source_baseline_commit"] == BASELINE_COMMIT and old["archive_sha256"] == SOURCE_ARCHIVE_SHA256
    old_payload = ROOT/"dist/m5-kaggle-source-v2"/old["payload_filename"]
    with old_payload.open("rb") as stream:
        assert hashlib.file_digest(stream,"sha256").hexdigest() == SOURCE_ARCHIVE_SHA256

    changed_docs = {ROOT/name for name in MUTABLE if name.endswith(".md")}
    changed_docs.add(ROOT/"docs/validation/course-m5-inference-and-smoke-preparation.md")
    helper = ROOT/"notebooks/validation/m5-attention-memory/check_document_links.py"
    sys.path.insert(0,str(helper.parent))
    try:
        anchors = runpy.run_path(str(helper))["anchors"]
    finally:
        sys.path.pop(0)
    checked = fragments = inbound = 0
    changed_docs = {p.resolve() for p in changed_docs}
    for source in sorted(set(ROOT.glob("docs/**/*.md")) | {ROOT/"README.md",ROOT/"tests/fixtures/README.md"}):
        for target in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            target = target.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", target):
                continue
            name, _, fragment = target.partition("#")
            name = re.sub(r":\d+(?:-\d+)?$", "", unquote(name))
            resolved = (source.parent/name).resolve() if name else source.resolve()
            in_scope = source.resolve() in changed_docs
            if not in_scope and resolved not in changed_docs:
                continue
            # The audit being written is the sole forward reference.
            assert resolved.exists() or resolved == args.output.resolve(), (source,target)
            checked += 1
            inbound += not in_scope
            if fragment and resolved.suffix == ".md":
                assert unquote(fragment) in anchors(resolved), (source,target)
                fragments += 1
    cli = registration()
    assert not git("diff", "--check")
    result = dict(status="passed", task_status="blocked", r7_preparation_admitted=False,
        baseline=baseline["head"], audited_head=git("rev-parse","HEAD"),
        protected_files_identical=len(protected), thesis_defaults_todos_historical_artifacts_preserved=True,
        plan_sections_1_to_10_identical=True, course_task_states=dict(Counter(states.values())),
        reused_course_m4_gate=dict(status="passed and unchanged", plan_rows=22, consistency_categories=7),
        suites=suites, installed_modules_identical=29, cli_registration=cli,
        exact_requests=24, all_unexecuted=True, native_resident_bound=156251,
        complete_live_memory_upper_bound_bytes=None, terminal_model_feasibility_failure=False,
        packet=dict(source_commit=source_head,payload_sha256=review["payload_sha256"],
            source_members=review["source_members"], closed_exports_reopened=2),
        local_references=checked, markdown_fragments=fragments, inbound_references=inbound,
        model_generations=0, gpu_admission=False, weight_staging_permitted=False, runtime_freeze=False)
    with args.output.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(result,output,indent=2)
        output.write("\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
