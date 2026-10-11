"""Read-only course contract audit; no inference or course runtime acceptance."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
BASE = "96df569603dc940b4284791e17771e2dc19285b2"
FAMILIES = ("top_k", "prefix", "difference", "sort", "bfs")
DOCUMENTS = (
    "PROJECT_SPECIFICATION.md", "docs/IMPLEMENTATION_PLAN.md", "README.md",
    "docs/todos/course/README.md",
    "docs/todos/course/M1/M1-T01-course-contract-and-reuse-boundary.md",
    "docs/todos/course/M1/M1-T02-course-inputs-and-schedules.md",
    "docs/planning/course-study-session-handoff.md",
    "docs/validation/course-m1-contract-and-reuse.md",
)


def independent_schedule(per_family, preserving_per_family, repeated_per_family, development=False):
    counts, calls, parents = {}, set(), []
    for family in FAMILIES:
        for index in range(1, per_family + 1):
            rows = [("prefix", "original", "prefix", 0),
                    ("controls", "original", "control", 0),
                    ("controls", "revision", "control", 0)]
            rows += [("revised", "revision", p, 0) for p in ("L", "B", "C", "K", "F")]
            rows += [("sham", "sham", p, 0) for p in ("B", "C", "K")]
            if not development or family in ("prefix", "bfs"):
                rows += [("masks", z, p, 0) for z in ("revision", "sham") for p in ("P_G", "P_H")]
            if family in ("prefix", "sort"):
                rows += [("receipts", "revision", p, 0) for p in ("B_delta", "C_delta", "K_delta")]
            if family in ("sort", "bfs"):
                rows += [("prose_delay", z, p, 0) for z in ("revision", "sham") for p in ("Q_B", "Q_C")]
            if family in ("top_k", "bfs") and index <= preserving_per_family:
                rows += [("preserving", "preserving", p, 0) for p in ("B", "C", "K")]
            if not development and index <= repeated_per_family:
                rows += [("repeat", z, p, 1) for z in ("revision", "sham") for p in ("B", "C", "K", "P_G", "P_H")]
            for component, event, policy, replicate in rows:
                opportunities = [(1, None)] if policy == "control" else [(r, p) for r in range(1, 5) for p in range(4)]
                for round_number, peer in opportunities:
                    key = (family, index, event, policy, replicate, round_number, peer)
                    assert key not in calls
                    calls.add(key)
                    replay = round_number == 1 and policy in ("P_G", "P_H", "Q_B", "Q_C")
                    new, logical = counts.get(component, (0, 0))
                    counts[component] = (new + int(not replay), logical + 1)
                    if replay:
                        # Counts/parent existence are independent of which legal pair is G.
                        reset = peer in ((0, 1) if policy == "P_G" else (2, 3))
                        parent = policy[2:] if policy.startswith("Q_") else ("C" if reset else "B")
                        parents.append((family, index, event, parent, replicate, 1, peer))
    assert all(parent in calls for parent in parents), "replay parent scope"
    return counts, len(calls) - len(parents), len(calls), len(parents)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    stage = parser.add_mutually_exclusive_group()
    stage.add_argument("--adopted", action="store_true")
    stage.add_argument("--pending-adoption", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists(), "retain earlier audit output"
    snapshot_path = Path(tempfile.gettempdir()) / "recovery-course-m1-t01-baseline.json"
    baseline = json.loads(snapshot_path.read_text(encoding="utf-8"))
    assert baseline["head"] == BASE and Path(baseline["root"]).resolve() == ROOT
    for name, digest in baseline["protected"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name

    patch = ROOT / "docs/planning/course-contract-amendment.patch"
    command = ["git", "apply", "--check", "--unidiff-zero", "--ignore-space-change"]
    if args.adopted:
        command += ["--reverse"]
    subprocess.run(command + [str(patch)], cwd=ROOT, check=True, capture_output=True)
    additions, target = {}, None
    for line in patch.read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith("+++ b/"):
            target = line[6:].strip()
            additions[target] = ""
        elif line.startswith("+") and target:
            additions[target] += line[1:]
        elif line.startswith("-") and not line.startswith("--- "):
            raise AssertionError("amendment must preserve thesis sections")
    spec = (ROOT / "PROJECT_SPECIFICATION.md").read_text(encoding="utf-8")
    assert spec == baseline["specification"] + (additions["PROJECT_SPECIFICATION.md"] if args.adopted else "")

    main_rows, new, logical, replays = independent_schedule(4, 4, 1)
    assert (new, logical, replays) == (5752, 6280, 528)
    assert main_rows == dict(prefix=(320, 320), revised=(1600, 1600), sham=(960, 960),
        masks=(960, 1280), controls=(40, 40), preserving=(384, 384),
        receipts=(384, 384), prose_delay=(384, 512), repeat=(720, 800))
    names = ("Shared prefixes", "Revised L/B/C/K/F", "Sham B/C/K",
        "Complementary masks under both events", "Before/after full-information controls",
        "Preserving B/C/K", "Historical receipts, revision only", "Q_B/Q_C under both events",
        "Additional B/C/K/mask replicate under both events")
    components = ("prefix", "revised", "sham", "masks", "controls", "preserving", "receipts", "prose_delay", "repeat")
    clause = additions["PROJECT_SPECIFICATION.md"]
    for name, component in zip(names, components):
        match = re.search(r"\| " + re.escape(name) + r" \| ([\d,]+) \| ([\d,]+) \|", clause)
        assert match and tuple(int(v.replace(",", "")) for v in match.groups()) == main_rows[component]
    dev_rows, dev_new, dev_logical, dev_replays = independent_schedule(1, 1, 0, True)
    assert (dev_new, dev_logical, dev_replays) == (1114, 1178, 64)
    assert dev_rows["prefix"][0] + dev_rows["controls"][0] == 90
    assert new + dev_new + 24 == 6890
    thesis = {}
    for n, expected in ((60, (16152, 17656)), (40, (11504, 12560))):
        _, distinct, slots, _ = independent_schedule(n // 5, 8, 2)
        assert (distinct, slots) == expected
        thesis[n] = expected

    # Inspect the unchanged saved implementation; this does not prepare course inputs.
    sys.path.insert(0, str(ROOT))
    from recovery.manifests import load_population, load_schedules
    from recovery.prompts import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS
    assert (MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS) == (262144, 384)
    seed_checks = []
    for size in ("target", "fallback"):
        population = load_population(ROOT / f"tests/fixtures/population_{size}.json")
        def seeds(worlds):
            def flatten(value):
                if isinstance(value, int):
                    return {value}
                return set().union(*(flatten(v) for v in (value.values() if isinstance(value, dict) else value)))
            return set().union(*(flatten(asdict(w.streams)) for w in worlds))
        main_seeds, development_seeds = seeds(population.main), seeds(population.development)
        assert main_seeds.isdisjoint(development_seeds)
        assert max(main_seeds | development_seeds) - population.master_seed * 2**20 < 2**20
        try:
            population.worlds(20)
        except ValueError:
            pass
        else:
            raise AssertionError("course adaptation unexpectedly present")
        seed_checks.append({"size": size, "master_seed": population.master_seed,
            "main_assigned_seeds": len(main_seeds), "development_assigned_seeds": len(development_seeds),
            "domains_disjoint": True, "complete_block_span_below": 2**20})
        if size == "target":
            load_schedules(ROOT / "tests/fixtures/schedules_target.json", population)

    tasks = sorted((ROOT / "docs/todos/course").glob("M*/*.md"))
    states = {p.stem[:6]: re.search(r"\*\*Status:\*\* (\w+)", p.read_text(encoding="utf-8"))[1] for p in tasks}
    assert len(tasks) == len(states) == 21
    index = (ROOT / "docs/todos/course/README.md").read_text(encoding="utf-8")
    table = {key: status for key, status in re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|", index)}
    assert table == states, "course task index mismatch"
    completed = args.adopted and states["M1-T01"] == "done"
    expected_states = (Counter(done=1, ready=1, blocked=19) if completed else
                       Counter(blocked=21) if args.pending_adoption else Counter(active=1, blocked=20))
    assert Counter(states.values()) == expected_states
    expected_summary = ("1/21 course tasks done; 20 remaining; 0 active; 1 ready; 19 blocked" if completed else
        "0/21 course tasks done; 21 remaining; 0 active; 0 ready; 21 blocked" if args.pending_adoption else
        "0/21 course tasks done; 21 remaining; 1 active; 0 ready; 20 blocked")
    assert expected_summary in index
    milestone_rows = re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|", index)
    assert len(milestone_rows) == 6
    for milestone, done, total, active, ready, blocked in milestone_rows:
        actual = Counter(status for task, status in states.items() if task.startswith(milestone + "-"))
        assert tuple(map(int, (done, active, ready, blocked))) == tuple(actual[s] for s in ("done", "active", "ready", "blocked"))
        assert int(total) == sum(actual.values())

    # Reuse the existing Markdown slug rules without running its historical writer.
    helper = ROOT / "notebooks/validation/m5-attention-memory"
    sys.path.insert(0, str(helper))
    anchors = runpy.run_path(str(helper / "check_document_links.py"))["anchors"]
    changed = {(ROOT / name).resolve() for name in DOCUMENTS} | set(tasks)
    sources = set(ROOT.glob("docs/**/*.md")) | {ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "PROJECT_SPECIFICATION.md"}
    candidate_contents = {(ROOT / name).resolve(): (ROOT / name).read_text(encoding="utf-8") + addition
                          for name, addition in additions.items()} if not args.adopted else {}
    checked = fragments = 0
    from urllib.parse import unquote
    for source in sorted(sources):
        content = candidate_contents.get(source.resolve(), source.read_text(encoding="utf-8"))
        for link in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", content):
            link = link.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:", link):
                continue
            name, _, fragment = link.partition("#")
            resolved = (source.parent / unquote(name)).resolve() if name else source.resolve()
            if source.resolve() not in changed and resolved not in changed:
                continue
            assert resolved.exists(), (source, link)
            checked += 1
            if fragment and resolved.suffix == ".md":
                document = SimpleNamespace(read_text=lambda encoding: candidate_contents[resolved]) if resolved in candidate_contents else resolved
                assert unquote(fragment) in anchors(document), (source, link)
                fragments += 1

    report = {"status": "passed", "stage": "adopted" if args.adopted else "pending_adoption" if args.pending_adoption else "prepared",
        "contract_task_completed": completed,
        "code_baseline": BASE, "environment": sys.version.split()[0], "protected_files_identical": len(baseline["protected"]),
        "preexisting_user_edit_sha256": baseline["protected"]["docs/validation/m5-inference-preparation.md"],
        "thesis_specification_preserved": True, "thesis_runtime_defaults_preserved": True,
        "patch_check": "reverse" if args.adopted else "forward", "course_main_components": main_rows,
        "course_main": [new, logical, replays], "course_development_components": dev_rows,
        "course_development": [dev_new, dev_logical, dev_replays], "thesis_totals": thesis,
        "existing_seed_domains": seed_checks, "course_inputs_or_seeds_frozen": False,
        "course_task_states": dict(Counter(states.values())), "local_references_checked": checked,
        "markdown_fragments_checked": fragments, "gpu_allocations_or_model_calls": 0,
        "scope": "Contract/independent arithmetic and unchanged thesis audit; course behavioral and model gates remain open."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
