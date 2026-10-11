"""Read-only audit of course intervention artifacts, preservation and handoff."""

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
    "recovery/rounds.py", "recovery/__main__.py", "README.md", "tests/fixtures/README.md",
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course/README.md",
    "docs/todos/course/M2/M2-T02-course-interventions-and-replay.md",
    "docs/todos/course/M2/M2-T03-course-attainability-and-capacity.md",
    "docs/planning/course-study-session-handoff.md",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--completion", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    baseline = json.loads(gzip.decompress((FOLDER / "baseline-files.json.gz").read_bytes()))
    protected = {p: h for p, h in baseline["files"].items() if p not in MUTABLE}
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert "docs/validation/m5-inference-preparation.md" not in git("diff", "--cached", "--name-only").splitlines()
    old_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    assert plan.split("## 11. Course living handoff")[0] == old_plan.split("## 11. Course living handoff")[0]
    old_rounds = git("show", baseline["head"] + ":recovery/rounds.py")
    expected = old_rounds.replace(
        "def run_prefix(world: World, branch_id: str, tokenizer, reply_provider, *, invocation_order=PEERS) -> ScriptedPrefix:",
        "def run_prefix(world: World, branch_id: str, tokenizer, reply_provider, *, invocation_order=PEERS,\n"
        "               limits: ProtocolLimits = THESIS_LIMITS) -> ScriptedPrefix:")
    expected = expected.replace("result = run_round(state, tokenizer, reply_provider, invocation_order=order)",
                                "result = run_round(state, tokenizer, reply_provider, invocation_order=order, limits=limits)")
    assert (ROOT / "recovery/rounds.py").read_text(encoding="utf-8").strip() == expected
    old_cli = git("show", baseline["head"] + ":recovery/__main__.py")
    expected = old_cli.replace('        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_settings_checks"))',
        '        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_settings_checks"))\n'
        '        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.course_intervention_checks"))')
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
    if args.completion:
        assert states["M2-T02"] == "done" and states["M2-T03"] == "ready"
        assert Counter(states.values()) == dict(done=4, ready=1, blocked=16)
        assert "4/21 course tasks done; 17 remaining; 0 active; 1 ready; 16 blocked" in index
    else:
        assert states["M2-T02"] == "active"

    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    changed_documents = {(ROOT / p).resolve() for p in MUTABLE if p.endswith(".md")}
    changed_documents.add((ROOT / "docs/validation/course-m2-interventions-and-replay.md").resolve())
    changed_documents.update(p.resolve() for p in tasks)
    references = fragments = 0
    for source in set(ROOT.glob("docs/**/*.md")) | {ROOT / p for p in ("README.md", "AGENTS.md", "PROJECT_SPECIFICATION.md", "tests/fixtures/README.md")}:
        for link in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            link = link.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", link):
                continue
            name, _, fragment = link.partition("#")
            name = re.sub(r":\d+$", "", unquote(name))
            target = (source.parent / name).resolve() if name else source.resolve()
            if source.resolve() not in changed_documents and target not in changed_documents:
                continue
            assert target.exists(), (source, link)
            references += 1
            if fragment and target.suffix == ".md":
                assert unquote(fragment) in anchors(target), (source, link)
                fragments += 1
    for p in changed_documents:
        text = p.read_text(encoding="utf-8")
        assert "\ufffd" not in text and sum(bool(re.match(r"^\s*```", line)) for line in text.splitlines()) % 2 == 0, p

    archive = json.loads(gzip.decompress((ROOT / "tests/fixtures/course_interventions.json.gz").read_bytes()))
    schedule = json.loads((ROOT / "tests/fixtures/schedules_course.json").read_bytes())
    expected_starts = {"/".join((b["world_id"], b["phase"], b["event"], b["policy"], "rep" + str(b["replicate"])))
        for b in schedule["main"] + schedule["development"] if b["phase"] == "continuation"}
    rounds = [r for c in archive["cases"] for r in c["rounds"]]
    starts = {r["branch_id"] for r in rounds if r["slot"]["round_number"] == 1}
    assert starts == expected_starts and len(starts) == 438
    calls = {call["call_id"]: reply for row in rounds for call, reply in zip(row["calls"], row["replies"])}
    assert len(calls) == len(rounds) * 4
    comparisons = [c for r in rounds for c in r["parent_comparisons"]]
    assert len(comparisons) == 592 and len({c["call_id"] for c in comparisons}) == 592
    for comparison in comparisons:
        assert all(comparison["equal"].values())
        assert calls[comparison["call_id"]] == calls[comparison["parent"]]
    environment = json.loads((FOLDER / "native-environment.json").read_bytes())
    prior = json.loads((ROOT / "notebooks/validation/course-m2-protocol/native-environment.json").read_bytes())
    assert environment["revision"] == prior["revision"] == archive["revision"]
    for row in prior["files"]:
        assert environment["files"][row["file"]] == {"bytes": row["bytes"], "sha256": row["sha256"]}

    suites = {}
    for label in ("baseline-checks", "course-corrected", "integration-checks", "native-initial", "native-hash37", "installed-checks", "cli-discovery"):
        receipt = FOLDER / f"{label}-command.json"
        if not receipt.exists() and not args.completion:
            continue
        command = json.loads(receipt.read_bytes())
        assert command["exit_code"] == 0, label
        log = gzip.decompress((FOLDER / command["log"]).read_bytes()).decode("utf-8").replace("\r", "")
        assert "FAILED (" not in log and "Traceback (" not in log, label
        suites[label] = dict(tests=[int(n) for n in re.findall(r"Ran (\d+) tests", log)], exit_code=0)
    if args.completion:
        installed = json.loads((FOLDER / "installed-provenance.json").read_bytes())
        assert not installed["source_pythonpath"] and installed["matching_modules"] == 29
        assert all(hashlib.sha256((ROOT / "recovery" / p).read_bytes()).hexdigest() == h for p, h in installed["modules"].items())
    report = dict(status="passed", baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"),
        protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        production_diff_limited_to_prefix_keyword_and_cpu_suite_registration=True,
        thesis_defaults_and_plan_sections_1_to_10_preserved=True, course_task_states=dict(Counter(states.values())),
        local_references=references, markdown_fragments=fragments,
        worlds=len(archive["cases"]), continuation_starts=len(starts), replay_parent_comparisons=len(comparisons),
        retained_continuation_rounds=len(rounds), pinned_metadata_matches=4, suites=suites,
        model_calls=0, complete_context_capacity="unaccepted", runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
