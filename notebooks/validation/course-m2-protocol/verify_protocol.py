"""Read-only audit of course M2 protocol evidence, preservation and handoff."""

import argparse
from collections import Counter
from dataclasses import asdict, replace
import gzip
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import types
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
MUTABLE = {
    "recovery/prompts.py", "recovery/protocol.py", "recovery/rounds.py", "recovery/replay.py",
    "recovery/runner.py", "recovery/storage.py", "recovery/inference.py", "recovery/__main__.py",
    "tests/round_checks.py", "README.md", "tests/fixtures/README.md", "docs/IMPLEMENTATION_PLAN.md",
    "docs/todos/course/README.md", "docs/todos/course/M2/M2-T01-course-protocol-and-limits.md",
    "docs/todos/course/M2/M2-T02-course-interventions-and-replay.md",
    "docs/planning/course-study-session-handoff.md",
}
USER_EDIT = "docs/validation/m5-inference-preparation.md"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--completion", action="store_true")
    args = parser.parse_args()
    assert not args.output.exists(), "retain previous audit evidence"
    baseline = json.loads(gzip.decompress((FOLDER / "baseline-files.json.gz").read_bytes()))
    protected = {path: digest for path, digest in baseline["files"].items() if path not in MUTABLE}
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert USER_EDIT not in git("diff", "--cached", "--name-only").splitlines()
    original_plan = git("show", baseline["head"] + ":docs/IMPLEMENTATION_PLAN.md")
    current_plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    assert current_plan.split("## 11. Course living handoff")[0] == original_plan.split("## 11. Course living handoff")[0]

    # Check actual thesis settings against original source, without weights or
    # optional packages; no new golden settings file or competing config store.
    sys.path.insert(0, str(ROOT))
    from recovery.inference import candidate_settings, QWEN_9B, QWEN_4B
    from recovery.prompts import COURSE_LIMITS, THESIS_LIMITS, limits_from_settings
    from recovery.t4_attention import T4_ATTENTION
    from tests.inference_mocks import Tokenizer
    old = types.ModuleType("recovery._course_m2_baseline")
    old.__package__ = "recovery"
    sys.modules[old.__name__] = old
    exec(compile(git("show", baseline["head"] + ":recovery/inference.py"),
                 "baseline/recovery/inference.py", "exec"), vars(old))
    for original, current in ((old.QWEN_9B, QWEN_9B), (old.QWEN_4B, QWEN_4B)):
        for attention in ("sdpa", T4_ATTENTION):
            assert old.candidate_settings(Tokenizer(), replace(original, attention=attention)) == candidate_settings(
                Tokenizer(), replace(current, attention=attention))
    assert limits_from_settings({}) == THESIS_LIMITS

    native = json.loads(gzip.decompress((ROOT / "tests/fixtures/course_protocol.json.gz").read_bytes()))
    assert native["limits"] == asdict(COURSE_LIMITS)
    assert limits_from_settings(native["settings"]) == COURSE_LIMITS
    assert native["revision"] == "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
    assert (len(native["requests"]), len(native["replies"]), len(native["shapes"])) == (11, 23, 225)
    assert all(row["protocol_valid"] and len(row["reply"]["token_ids"]) <= 256 for row in native["shapes"])
    assert native["replies"]["complete_256"]["candidate"]["status"] == "valid"
    assert native["replies"]["complete_257"]["candidate"]["status"] == "invalid"
    assert native["replies"]["prose_64"]["prose_tokens"] == 64
    assert native["replies"]["prose_65"]["prose_tokens"] == 65
    environment = json.loads((FOLDER / "native-environment.json").read_bytes())
    assert environment["revision"] == native["revision"]
    assert len(environment["files"]) == 4 and all(row["matches"] for row in environment["files"])

    tasks = sorted((ROOT / "docs/todos/course").glob("M*/*.md"))
    states = {path.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", path.read_text(encoding="utf-8"))[1] for path in tasks}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    indexed = dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index))
    assert indexed == states and len(states) == 21
    for milestone, done, total, active, ready, blocked in re.findall(
            r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(value for key, value in states.items() if key.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[key] for key in ("done", "active", "ready", "blocked"))

    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    documents = {(ROOT / name).resolve() for name in MUTABLE if name.endswith(".md")}
    documents.add((ROOT / "docs/validation/course-m2-protocol-and-limits.md").resolve())
    documents.update(path.resolve() for path in tasks)
    references = fragments = 0
    for source in sorted(set(ROOT.glob("docs/**/*.md")) | {ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "PROJECT_SPECIFICATION.md", ROOT / "tests/fixtures/README.md"}):
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
        text = path.read_text(encoding="utf-8")
        assert "\ufffd" not in text and sum(bool(re.match(r"^\s*```", line)) for line in text.splitlines()) % 2 == 0, path

    suites = {}
    if args.completion:
        assert states["M2-T01"] == "done" and states["M2-T02"] == "ready"
        assert Counter(states.values()) == dict(done=3, ready=1, blocked=17)
        assert "3/21 course tasks done; 18 remaining; 0 active; 1 ready; 17 blocked" in index
        result = runpy.run_path(str(ROOT / "notebooks/validation/course-m1-inputs/verify_inputs.py"))["suite_result"]
        for name in ("integration-pass", "core-validation", "full-validation", "native-hash37",
                     "installed-validation", "installed-hash37"):
            suites[name] = result(FOLDER / (name + ".txt"))
            receipt = json.loads((FOLDER / (name + "-command.json")).read_bytes())
            assert receipt["exit_code"] == 0, name
        assert all(suites[name]["skipped"] == 0 for name in suites if name != "core-validation")
        installed = json.loads((FOLDER / "installed-provenance.json").read_bytes())
        assert installed["source_pythonpath"] is False and installed["matching_modules"] == 29
        assert all(hashlib.sha256((ROOT / "recovery" / name).read_bytes()).hexdigest() == digest
                   for name, digest in installed["modules"].items())
        assert "No broken requirements found." in (FOLDER / "pip-check.txt").read_text(encoding="utf-8")
    report = dict(status="passed", stage="completion" if args.completion else "checkpoint",
        baseline=baseline["head"], audited_head=git("rev-parse", "HEAD"), python=sys.version.split()[0],
        raw_protected_files_identical=len(protected), user_edit_identical_and_unstaged=True,
        thesis_settings_identical=True, thesis_roadmap_sections_1_to_10_preserved=True,
        local_references_checked=references, markdown_fragments_checked=fragments,
        course_task_states=dict(Counter(states.values())), suites=suites,
        native_requests=11, native_replies=23, native_shapes_and_shards=225,
        maximum_useful_output_tokens=max(len(row["reply"]["token_ids"]) for row in native["shapes"]),
        maximum_feedback_tokens=max(native["feedback"].values()), pinned_metadata_files_match=4,
        model_calls=0, complete_context_capacity="unaccepted", runtime_freeze=False)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
