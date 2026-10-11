"""Read-only course M1 evidence audit; derived outputs, no inference or freeze."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
MUTABLE = {
    "recovery/populations.py", "recovery/manifests.py", "recovery/schedule.py", "recovery/__main__.py",
    "README.md", "tests/fixtures/README.md", "tests/test_t4_attention.py", "docs/IMPLEMENTATION_PLAN.md",
    "docs/todos/course/README.md", "docs/todos/course/M1/M1-T02-course-inputs-and-schedules.md",
    "docs/todos/course/M2/M2-T01-course-protocol-and-limits.md", "docs/planning/course-study-session-handoff.md",
}
USER_EDIT = "docs/validation/m5-inference-preparation.md"
USER_DIGEST = "c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca"


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT).decode("utf-8").strip()


def suite_result(path):
    raw = path.read_bytes()
    content = raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
    match = re.search(r"Ran (\d+) tests in ([\d.]+)s", content)
    assert match and re.search(r"^OK(?: \(skipped=\d+\))?\s*$", content, re.MULTILINE), path
    skip = re.search(r"OK \(skipped=(\d+)\)", content)
    return dict(log=path.name, tests=int(match[1]), skipped=int(skip[1]) if skip else 0,
                seconds=float(match[2]), status="passed")


def seed_values(value):
    if type(value) is int:
        return [value]
    if isinstance(value, dict):
        return [s for item in value.values() for s in seed_values(item)]
    return [s for item in value for s in seed_values(item)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--completion", action="store_true", help="also require passed suites and final course handoff")
    args = parser.parse_args()
    assert not args.output.exists(), "retain prior audit evidence"
    sys.path.insert(0, str(ROOT))
    from dataclasses import asdict
    from recovery.manifests import load_population, load_schedules, manifest_bytes, schedule_bytes
    from recovery.populations import prepare_population
    from recovery.schedule import component_counts, dependency_order, iter_calls, prepare_schedules
    from recovery.tasks import Size, Task
    from tests.test_course_schedules import independent_cells

    # Reuse M1-T01's independent specification enumeration, not the production matrix.
    independent = runpy.run_path(str(ROOT / "notebooks/validation/course-m1-contract/verify_contract.py"))["independent_schedule"]
    p = load_population(ROOT / "tests/fixtures/population_course.json")
    s = load_schedules(ROOT / "tests/fixtures/schedules_course.json", p)
    assert (p.regime, p.size, p.master_seed, len(p.main), len(p.development)) == ("course", Size.FALLBACK, 20261009, 20, 5)
    assert manifest_bytes(p) == (ROOT / "tests/fixtures/population_course.json").read_bytes()
    assert schedule_bytes(s) == (ROOT / "tests/fixtures/schedules_course.json").read_bytes()
    assert manifest_bytes(prepare_population(p.master_seed, p.size, regime="course")) == manifest_bytes(p)
    assert schedule_bytes(prepare_schedules(p)) == schedule_bytes(s)
    main_table, new, logical, replay = independent(4, 4, 1)
    dev_table, dev_new, dev_logical, dev_replay = independent(1, 1, 0, True)
    assert component_counts(s.main) == main_table
    assert component_counts(s.development) == dev_table
    assert (new, logical, replay, dev_new, dev_logical, dev_replay) == (5752, 6280, 528, 1114, 1178, 64)
    assert (len(dependency_order(tuple(reversed(s.main)))), len(dependency_order(s.development))) == (logical, dev_logical)
    for branches, worlds, development in ((s.main, p.main, False), (s.development, p.development, True)):
        assert {(b.world_id, b.phase, b.event, b.policy, b.replicate) for b in branches} == independent_cells(worlds, development)
    assert Counter(b.phase for b, _ in s.capability) == dict(prefix=80, control=10)
    assert tuple(iter_calls(s.development))[:90] == s.capability
    cohorts = {k: len(v) for k, v in p.subsets().items()}
    assert cohorts == dict(main=20, receipt=8, q=8, preserving=8, repeat=5)
    owners = {t.value: Counter(w.edited_owner for w in p.main if w.world.task is t) for t in Task}
    assert all(row == dict.fromkeys(range(4), 1) for row in owners.values())
    rejections = {w.world_id: [asdict(r) for r in w.rejections] for w in p.main + p.development if w.rejections}
    course_main = seed_values([asdict(w.streams) for w in p.main]) + list(p.owner_seeds)
    course_dev = seed_values([asdict(w.streams) for w in p.development]) + list(p.development_owner_seeds)
    assert (len(course_main), len(course_dev)) == (865, 200)
    assert len(set(course_main + course_dev)) == 1065
    assert set(course_main).isdisjoint(course_dev)
    thesis_totals = {}
    for size in Size:
        thesis = load_population(ROOT / f"tests/fixtures/population_{size.value}.json")
        assert thesis.regime == "thesis" and thesis.main_counts == (60, 40)
        assert manifest_bytes(thesis) == (ROOT / f"tests/fixtures/population_{size.value}.json").read_bytes()
        actual = seed_values([asdict(w.streams) for w in thesis.main + thesis.development])
        actual += list(thesis.owner_seeds + thesis.development_owner_seeds)
        assert set(course_main + course_dev).isdisjoint(actual)
        schedule = prepare_schedules(thesis)
        for count in (60, 40):
            _, n, l, _ = independent(count // 5, 8, 2)
            table = component_counts(schedule.main_for(thesis, count))
            assert tuple(sum(row[i] for row in table.values()) for i in (0, 1)) == (n, l)
            thesis_totals[f"{size.value}/{count}"] = [n, l]
        if size is Size.TARGET:
            assert schedule_bytes(schedule) == (ROOT / "tests/fixtures/schedules_target.json").read_bytes()

    # Check the current raw snapshot where available; clean replays also check Git's baseline.
    snapshot_path = Path(tempfile.gettempdir()) / "recovery-course-m1-t02-baseline.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8")) if snapshot_path.exists() else None
    baseline_head = snapshot["head"] if snapshot else git("rev-parse", "1dfb1e5")
    baseline_paths = set(snapshot["files"] if snapshot else git("ls-tree", "-r", "--name-only", baseline_head).splitlines())
    changed = set(git("diff", "--name-only", baseline_head).splitlines())
    changed_original = changed & baseline_paths
    assert changed_original <= MUTABLE | {USER_EDIT}, changed_original - MUTABLE - {USER_EDIT}
    original_plan = git("show", f"{baseline_head}:docs/IMPLEMENTATION_PLAN.md").replace("\r\n", "\n")
    current_plan = (ROOT / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    assert current_plan.split("## 11. Course living handoff")[0] == original_plan.split("## 11. Course living handoff")[0]
    protected_count = None
    if snapshot:
        assert Path(snapshot["root"]).resolve() == ROOT
        protected = {name: digest for name, digest in snapshot["files"].items() if name not in MUTABLE}
        for name, digest in protected.items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
        assert hashlib.sha256((ROOT / USER_EDIT).read_bytes()).hexdigest() == USER_DIGEST
        protected_count = len(protected)
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    assert USER_EDIT not in staged

    tasks = sorted((ROOT / "docs/todos/course").glob("M*/*.md"))
    states = {path.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", path.read_text(encoding="utf-8"))[1] for path in tasks}
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    indexed = {key: status for key, status in re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)}
    assert indexed == states and len(states) == 21
    for milestone, done, total, active, ready, blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index):
        counts = Counter(state for task, state in states.items() if task.startswith(milestone + "-"))
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(counts[key] for key in ("done", "active", "ready", "blocked"))
        assert int(total) == sum(counts.values())
    suites = {}
    if args.completion:
        assert states["M1-T01"] == states["M1-T02"] == "done" and states["M2-T01"] == "ready"
        assert Counter(states.values()) == dict(done=2, ready=1, blocked=18)
        assert "2/21 course tasks done; 19 remaining; 0 active; 1 ready; 18 blocked" in index
        folder = Path(__file__).parent
        for name in ("core-validation-pass.txt", "full-validation-pass.txt", "installed-validation.txt", "installed-hash37-validation.txt"):
            suites[name] = suite_result(folder / name)
        for name in ("core-command.json", "full-command.json", "installed-provenance.json", "installed-hash37-command.json"):
            assert json.loads((folder / name).read_text(encoding="utf-8"))["returncode"] == 0, name

    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    documents = {(ROOT / name).resolve() for name in MUTABLE if name.endswith(".md")}
    documents.add((ROOT / "docs/validation/course-m1-inputs-and-schedules.md").resolve())
    documents.update(tasks)
    references = fragments = 0
    sources = set(ROOT.glob("docs/**/*.md")) | {ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "PROJECT_SPECIFICATION.md", ROOT / "tests/fixtures/README.md"}
    for source in sorted(sources):
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
    report = dict(status="passed", stage="completion" if args.completion else "input_checkpoint",
        preparation_baseline=baseline_head, audited_head=git("rev-parse", "HEAD"), python=sys.version.split()[0],
        platform=sys.platform, course_master_seed=p.master_seed, course_cohorts=cohorts, owner_counts=owners,
        rejections=rejections, course_main_components=main_table, course_main=[new, logical, replay],
        course_development_components=dev_table, course_development=[dev_new, dev_logical, dev_replay],
        main_assigned_seeds_including_owner=865, development_assigned_seeds_including_owner=200,
        course_main_development_thesis_seed_domains_disjoint=True, thesis_totals=thesis_totals,
        raw_protected_files_identical=protected_count, preexisting_user_edit_sha256=USER_DIGEST if snapshot else None,
        thesis_roadmap_sections_1_to_10_preserved=True,
        local_references_checked=references, markdown_fragments_checked=fragments,
        course_task_states=dict(Counter(states.values())), suites=suites, model_calls=0,
        input_or_runtime_freeze=False, scope="Course CPU inputs/schedules; later protocol, runtime, model, resource, freeze and empirical gates remain open.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
