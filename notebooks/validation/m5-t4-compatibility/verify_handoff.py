"""Check documentation, task states and preservation without running notebook cells."""

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
BEFORE = "7f61fc7"
BASELINE = "ca46bcd55486b38bb453f5294e01f943bc7f7752"
USER_EDIT = "c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca"
DOCUMENTS = [
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/README.md",
    "docs/todos/M5/M5-T02-hardware-smoke-and-host-validation.md",
    "docs/validation/m5-t4-compatibility.md", "docs/validation/m5-kaggle-preflight.md",
    "docs/validation/m5-kaggle-full-preparation.md",
    *["docs/planning/m5-kaggle-first-run/" + name for name in ["README.md",
      "04-model-feasibility-and-smoke.md", "05-implementation-and-validation.md",
      "06-lessons-learned.md", "07-t4-compatibility.md"]],
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(path):
    with path.open("rb") as incoming:
        return hashlib.file_digest(incoming, "sha256").hexdigest()


def main():
    assert not OUTPUT.exists(), "Preserve previous handoff evidence"
    OUTPUT.write_text('{"status":"running"}\n', encoding="utf-8")
    report = {"status": "failed", "comparison_checkpoint": BEFORE, "scientific_baseline": BASELINE}
    try:
        links = 0
        for name in DOCUMENTS:
            path = ROOT / name
            for target in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", path.read_text(encoding="utf-8")):
                target = target.strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-z]+://|mailto:", target):
                    continue
                resolved = (path.parent / unquote(target)).resolve()
                assert resolved.exists(), (name, target)
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
        names = git("ls-tree", "-r", "--name-only", BEFORE, "--", "notebooks").decode().splitlines()
        data = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
            input="".join(BEFORE + ":" + name + "\n" for name in names).encode(),
            capture_output=True, check=True).stdout
        stream = io.BytesIO(data)
        returned = 0
        for name in names:
            _, kind, size = stream.readline().split()
            assert kind == b"blob", name
            original = stream.read(int(size))
            assert stream.read(1) == b"\n"
            assert (ROOT / name).read_bytes() == original, name
            returned += name.startswith("notebooks/run/")
        assert not stream.read()
        protected = ["recovery", "configs", "tests/fixtures", "AGENTS.md", "PROJECT_SPECIFICATION.md", "pyproject.toml"]
        assert not git("diff", "--name-only", BASELINE, "--", *protected)
        unchanged_operations = ["README.md", "scripts/m5_kaggle_preflight.py", ".gitattributes", "notebooks/.gitattributes"]
        assert not git("diff", "--name-only", BEFORE, "--", *unchanged_operations)
        edit = ROOT / "docs/validation/m5-inference-preparation.md"
        assert digest(edit) == USER_EDIT
        payloads = {}
        expected_archive = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
        for name in ["dist/m5-kaggle-preflight.zip", "dist/m5-kaggle-source-v2/m5-kaggle-source.payload",
                     "dist/m5-kaggle-pip-bootstrap-v3/m5-kaggle-source.payload"]:
            path = ROOT / name
            assert path.stat().st_size == 109248341 and digest(path) == expected_archive
            payloads[name] = {"bytes": path.stat().st_size, "sha256": expected_archive}
        kernel = json.loads((OUTPUT.parent / "kernel/validation.json").read_text(encoding="utf-8"))
        assert kernel["status"] == "passed" and not kernel["actual_t4_execution"]
        notebook = ROOT / "notebooks/recovery_m5_kaggle_t4_compatibility.ipynb"
        assert digest(notebook) == kernel["notebook_sha256"]
        report.update(status="passed", documents_checked=len(DOCUMENTS), local_links_checked=links,
            tasks_checked=len(tasks), task_states=dict(states), earlier_notebook_evidence_files_unchanged=len(names),
            supplied_run_files_unchanged=returned, protected_scientific_git_diff="empty", protected_paths=protected,
            unchanged_operational_and_root_git_diff="empty", unchanged_operational_paths=unchanged_operations,
            existing_user_edit_sha256=USER_EDIT, canonical_payloads=payloads, notebook_sha256=digest(notebook),
            notebook_bytes=notebook.stat().st_size, actual_t4_execution=False, model_generations=0)
    except BaseException as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
