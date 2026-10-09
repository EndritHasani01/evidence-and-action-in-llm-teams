"""Read-only run-6 handoff checks; never execute notebook cells or GPU code."""

import ast
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parent / "handoff-validation.json"
BEFORE = "d71d117"
EVIDENCE = "0f9407f"
BASELINE = "ca46bcd55486b38bb453f5294e01f943bc7f7752"
USER_EDIT = "c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca"
DOCUMENTS = [
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/README.md",
    "docs/todos/M5/M5-T02-hardware-smoke-and-host-validation.md",
    "docs/validation/m5-t4-compatibility.md", "docs/validation/m5-t4-compatibility-run-6.md",
    "docs/validation/m5-kaggle-preflight.md", "docs/validation/m5-kaggle-full-preparation.md",
    *["docs/planning/m5-kaggle-first-run/" + name for name in ["README.md",
      "04-model-feasibility-and-smoke.md", "05-implementation-and-validation.md",
      "06-lessons-learned.md", "07-t4-compatibility.md"]],
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(path):
    with path.open("rb") as incoming:
        return hashlib.file_digest(incoming, "sha256").hexdigest()


def check_notebooks(commit):
    names = git("ls-tree", "-r", "--name-only", commit, "--", "notebooks").decode().splitlines()
    data = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
        input="".join(commit + ":" + name + "\n" for name in names).encode(),
        capture_output=True, check=True).stdout
    stream = io.BytesIO(data)
    for name in names:
        _, kind, size = stream.readline().split()
        assert kind == b"blob", name
        original = stream.read(int(size))
        assert stream.read(1) == b"\n"
        assert (ROOT / name).read_bytes() == original, name
    assert not stream.read()
    return {"files_unchanged": len(names),
            "supplied_run_files_unchanged": sum(name.startswith("notebooks/run/") for name in names)}


def main():
    assert not OUTPUT.exists(), "Preserve previous handoff evidence"
    OUTPUT.write_text('{"status":"running"}\n', encoding="utf-8")
    report = {"status": "failed", "comparison_checkpoint": BEFORE,
              "run_6_evidence_checkpoint": EVIDENCE, "scientific_baseline": BASELINE}
    try:
        links = 0
        for name in DOCUMENTS:
            path = ROOT / name
            for target in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", path.read_text(encoding="utf-8")):
                target = target.strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-z]+://|mailto:", target):
                    continue
                assert (path.parent / unquote(target)).resolve().exists(), (name, target)
                links += 1
        index = (ROOT / "docs/todos/README.md").read_text(encoding="utf-8")
        tasks = sorted(ROOT.glob("docs/todos/M[1-6]/M*-T*.md"))
        states = Counter()
        for task in tasks:
            state = re.search(r"\*\*Status:\*\* (\w+)", task.read_text(encoding="utf-8")).group(1)
            identity = re.match(r"M\d-T\d+", task.name).group()
            row = re.search(r"^\| \[" + identity + r"[^\n]+", index, flags=re.M).group()
            assert re.search(r"\)\s*\|\s*" + state + r"\s*\|", row), identity
            states[state] += 1
        assert len(tasks) == 29 and states == {"done": 21, "blocked": 8}
        assert "**Completed: 21/29. Remaining: 8. Active: 0. Ready: 0. Blocked: 8.**" in index
        snapshots = {commit: check_notebooks(commit) for commit in [BEFORE, EVIDENCE]}
        protected = ["recovery", "configs", "tests/fixtures", "AGENTS.md", "PROJECT_SPECIFICATION.md", "pyproject.toml"]
        assert not git("diff", "--name-only", BASELINE, "--", *protected)
        unchanged = ["README.md", "scripts", "tests", ".gitattributes", "notebooks/.gitattributes"]
        assert not git("diff", "--name-only", BEFORE, "--", *unchanged)
        edit = "docs/validation/m5-inference-preparation.md"
        assert digest(ROOT / edit) == USER_EDIT
        assert not git("diff", "--cached", "--name-only", "--", edit)
        payloads = {}
        archive_sha = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
        for name in ["dist/m5-kaggle-preflight.zip", "dist/m5-kaggle-source-v2/m5-kaggle-source.payload",
                     "dist/m5-kaggle-pip-bootstrap-v3/m5-kaggle-source.payload"]:
            path = ROOT / name
            assert path.stat().st_size == 109248341 and digest(path) == archive_sha
            payloads[name] = {"bytes": path.stat().st_size, "sha256": archive_sha}
        review = json.loads((OUTPUT.parent / "validation.json").read_text(encoding="utf-8"))
        assert review["attention_cases_passed"] == 14 and review["nf4_matmuls_passed"] == 4
        assert review["stages_passed"] == 6 and review["commands_passed"] == 4
        assert review["model_generations"] == 0 and review["provider_stop_user_reported"] is True
        assert review["provider_duration_seconds"] is None and review["provider_release_utc"] is None
        assert review["conditional_allocation_bound_verified"] is False
        envelope = json.loads((OUTPUT.parent.parent / "m5-t4-compatibility/static-envelope.json").read_text(encoding="utf-8"))
        assert envelope["full_envelope_memory_acceptance"] is None
        totals = {device["torch_total_bytes"] for device in review["devices"].values()}
        assert totals == {15636037632}
        native_gib = totals.pop() / 2**30
        assert native_gib == 14.56219482421875
        limit_gib = native_gib - 1.5
        assert limit_gib == 13.06219482421875
        conditional = {}
        for model, expected in [("9B", 18.0390625), ("4B", 14.23876953125)]:
            entry = envelope["models"][model]
            repeated_bytes = 2 * 16 * 256 * 2 * entry["resident_token_assumption"]
            assert repeated_bytes == entry["repeated_kv_one_layer_additional_bytes_at_cap"] == 4 * 2**30
            subtotal = (entry["conditional_subtotal_bytes_at_cap"] + repeated_bytes) / 2**30
            assert subtotal == expected
            conditional[model] = {"subtotal_gib_including_materialized_repeat": subtotal,
                "additional_repeat_gib": 4, "legal_cap_attainability": None, "empirical_model_failure": None}
        for name in ["review_run.py", "verify_handoff.py"]:
            ast.parse((OUTPUT.parent / name).read_text(encoding="utf-8"), filename=name)
        report.update(status="passed", documents_checked=len(DOCUMENTS), local_links_checked=links,
            tasks_checked=len(tasks), task_states=dict(states), unchanged_notebook_snapshots=snapshots,
            protected_scientific_git_diff="empty", protected_paths=protected,
            unchanged_operational_and_root_git_diff="empty", unchanged_paths=unchanged,
            existing_user_edit_sha256=USER_EDIT, existing_user_edit_unstaged=True,
            canonical_payloads=payloads, actual_t4_evidence_reviewed=True,
            local_gpu_execution=False, model_generations=0, provider_stop_user_reported=True,
            provider_duration_seconds=None, provider_release_utc=None,
            conditional_allocation_bound_verified=False,
            conditional_memory={"native_total_gib": native_gib,
                "native_total_minus_headroom_gib": limit_gib, "models": conditional,
                "full_envelope_memory_acceptance": None},
            evidence_python_syntax="passed")
    except BaseException as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
