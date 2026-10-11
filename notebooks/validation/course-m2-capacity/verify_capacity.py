"""Read-only course capacity artifact, preservation, task and evidence audit."""

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
MUTABLE = {
    "recovery/__main__.py", "tests/attainability_checks.py", "tests/tokenizer_attainability.py",
    "tests/tokenizer_capacity.py", "README.md", "tests/fixtures/README.md",
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course/README.md",
    "docs/todos/course/M2/M2-T03-course-attainability-and-capacity.md",
    "docs/todos/course/M3/M3-T01-course-durable-workers-and-failures.md",
    "docs/planning/course-study-session-handoff.md",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def read(path):
    path = Path(path)
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--completion", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists()
    baseline = read(FOLDER / "baseline-files.json.gz")
    protected = {p: h for p, h in baseline["files"].items() if p not in MUTABLE}
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert "docs/validation/m5-inference-preparation.md" not in git("diff", "--cached", "--name-only").splitlines()
    plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    old_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == old_plan.split("## 11. Course living handoff")[0]
    cli = git("show", baseline["head"] + ":recovery/__main__.py")
    expected = cli.replace('        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_intervention_checks"))',
        '        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_intervention_checks"))\n'
        '        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_attainability_checks"))')
    assert (ROOT / "recovery/__main__.py").read_text(encoding="utf-8").strip() == expected

    tasks = sorted((ROOT / "docs/todos/course").glob("M*/*.md"))
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1] for p in tasks}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)) == states
    for milestone, done, total, active, ready, blocked in re.findall(
            r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(v for k, v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[k] for k in ("done", "active", "ready", "blocked"))
    expected_counts = dict(done=5, ready=1, blocked=15) if args.completion else dict(done=4, active=1, blocked=16)
    assert Counter(states.values()) == expected_counts
    assert states["M2-T03"] == ("done" if args.completion else "active")
    assert states["M3-T01"] == ("ready" if args.completion else "blocked")

    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")}
    documents.update(p.resolve() for p in tasks)
    documents.update(p.resolve() for p in (ROOT / "docs").rglob("course-m2-*capacity*.md"))
    references = fragments = 0
    for source in set(ROOT.glob("docs/**/*.md")) | {ROOT / p for p in ("README.md", "AGENTS.md", "PROJECT_SPECIFICATION.md", "tests/fixtures/README.md")}:
        for link in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            link = link.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", link):
                continue
            name, _, fragment = link.partition("#")
            name = re.sub(r":\d+$", "", unquote(name))
            target = (source.parent / name).resolve() if name else source.resolve()
            if source.resolve() not in documents and target not in documents:
                continue
            assert target.exists(), (source, link)
            references += 1
            if fragment and target.suffix == ".md":
                assert unquote(fragment) in anchors(target), (source, link)
                fragments += 1
    for path in documents:
        content = path.read_text(encoding="utf-8")
        assert "\ufffd" not in content and sum(bool(re.match(r"^\s*```", line)) for line in content.splitlines()) % 2 == 0, path

    capacity = read(ROOT / "tests/fixtures/course_capacity.json.gz")
    assert capacity["admitted"] and capacity["resident_tokens_upper"] == 156251
    assert capacity["input_tokens_upper"] + 256 == capacity["resident_tokens_upper"]
    for row in capacity["accounting"]:
        assert row["payload_token_allowances"] == dict(own_replies=7*256, received_prose=21*64)
        assert row["input_tokens_per_payload_token_upper"] == dict(own_replies=48, received_prose=45)
        assert row["with_output_reserve_upper"] == row["nontext_bytes"]+69+7*256*48+21*64*45+256
        assert row["bound_fits"]
    witness_file = ROOT / "tests/fixtures/course_attainability.json.gz"
    witness_summary = {}
    if witness_file.exists():
        witness = read(witness_file)
        schedule = read(ROOT / "tests/fixtures/schedules_course.json")
        expected_calls = {c["call_id"] for b in schedule["main"]+schedule["development"] for c in b["calls"]}
        calls, comparisons = {}, []
        for case in witness["cases"]:
            calls.update((c["call_id"], outcome) for c, outcome in zip(case["prefix_calls"],
                [o for r in case["prefix_rounds"] for o in r["barrier"]["replies"]]))
            for row in case["rounds"]:
                calls.update((c["call_id"], outcome) for c, outcome in zip(row["calls"], row["replies"]))
                comparisons.extend(row["parent_comparisons"])
            calls.update((r["call"]["call_id"], r["outcome"]) for r in case["controls"])
        assert set(calls) == expected_calls and len(calls) == 7458
        assert len(comparisons) == len({c["call_id"] for c in comparisons}) == 592
        for c in comparisons:
            assert all(c["equal"].values()) and calls[c["call_id"]] == calls[c["parent"]]
        assert all(r["protocol_valid"] and r["correct_value_token_upper"] <= 256 for r in witness["output_shapes"])
        witness_summary = dict(worlds=len(witness["cases"]), logical_opportunities=len(calls), replay_joins=len(comparisons),
            correct_output_upper=max(r["correct_value_token_upper"] for r in witness["output_shapes"]))
    elif args.completion:
        raise AssertionError("native witness evidence missing")

    suites = {}
    labels = ("baseline-checks", "course-witness-corrected", "integration-checks", "native-witness-initial",
              "native-capacity-corrected", "native-witness-hash37", "native-capacity-hash37",
              "thesis-native-witness", "thesis-native-capacity", "installed-checks", "cli-discovery", "pip-check")
    for label in labels:
        receipt = FOLDER / f"{label}-command.json"
        if not receipt.exists() and not args.completion:
            continue
        command = read(receipt)
        assert command["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / command["log"]).read_bytes()).decode("utf-8").replace("\r", "")
        assert "FAILED (" not in log and "Traceback (" not in log, label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    if args.completion:
        installed = read(FOLDER / "installed-provenance.json")
        assert not installed["source_pythonpath"] and installed["matching_modules"] == 29
        for path, digest in installed["modules"].items():
            assert hashlib.sha256((ROOT / "recovery" / path).read_bytes()).hexdigest() == digest
        env = read(FOLDER / "native-capacity-environment.json")
        assert not env["model_weights_loaded"] and env["comparison_tokenizer"]
        assert env["revision"] == capacity["revision"]
    report = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        production_diff_limited_to_cpu_suite_registration=True, thesis_defaults_and_plan_sections_1_to_10_preserved=True,
        course_task_states=dict(Counter(states.values())), local_references=references, markdown_fragments=fragments,
        resident_tokens_upper=capacity["resident_tokens_upper"], adversarial_envelopes=len(capacity["rendered_fixtures"]),
        witness=witness_summary, suites=suites, model_calls=0, gpu_admission=False, runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
