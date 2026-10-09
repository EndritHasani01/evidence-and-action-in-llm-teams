"""Read-only evidence/preservation review; never run notebook cells or GPU code."""

import ast
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
BEFORE = "c8680c2"
IMPLEMENTATION = "8528105"
USER_EDIT = "c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca"
DOCUMENTS = [
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/README.md",
    "docs/todos/M5/M5-T02-hardware-smoke-and-host-validation.md",
    "docs/validation/m5-attention-memory.md",
    *["docs/planning/m5-kaggle-first-run/" + name for name in ["README.md",
      "04-model-feasibility-and-smoke.md", "05-implementation-and-validation.md",
      "06-lessons-learned.md", "08-attention-and-memory.md"]],
]
CODE = ["recovery/inference.py", "recovery/t4_attention.py", "scripts/m5_model_feasibility.py",
        "tests/test_inference_preparation.py", "tests/inference_checks.py",
        "tests/test_model_feasibility.py", "tests/test_t4_attention.py"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def prior_notebooks():
    names = git("ls-tree", "-r", "--name-only", BEFORE, "--", "notebooks").decode().splitlines()
    result = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
        input="".join(BEFORE + ":" + name + "\n" for name in names).encode(), capture_output=True, check=True)
    stream = io.BytesIO(result.stdout)
    for name in names:
        _, kind, size = stream.readline().split()
        assert kind == b"blob", name
        expected = stream.read(int(size))
        assert stream.read(1) == b"\n"
        assert (ROOT / name).read_bytes() == expected, name
    assert not stream.read()
    return dict(files_unchanged=len(names), returned_run_files_unchanged=sum(n.startswith("notebooks/run/") for n in names))


def baseline_settings():
    # Extract just the original pure settings function; no original loader runs.
    sys.path.insert(0, str(ROOT))
    from recovery.inference import QWEN_9B, QWEN_4B, candidate_settings
    from recovery.prompts import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS
    from tests.inference_mocks import Tokenizer
    source = ast.parse(git("show", BEFORE + ":recovery/inference.py").decode())
    original = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "candidate_settings")
    definitions = next(n for n in source.body if isinstance(n, ast.ClassDef) and n.name == "Candidate")
    baseline_9b = SimpleNamespace(**{n.target.id: ast.literal_eval(n.value) for n in definitions.body
                                   if isinstance(n, ast.AnnAssign) and n.target.id in ("model", "revision")})
    fallback = next(n.value for n in source.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "QWEN_4B" for t in n.targets))
    baseline_4b = SimpleNamespace(model=ast.literal_eval(fallback.args[0]), revision=ast.literal_eval(fallback.args[1]))
    namespace = dict(QWEN_9B=baseline_9b, MAX_CONTEXT_TOKENS=MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS=MAX_OUTPUT_TOKENS)
    for node in source.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("EOS_IDS", "PAD_ID", "TRANSPORT_ID"):
                    namespace[target.id] = ast.literal_eval(node.value)
    exec(compile(ast.Module(body=[original], type_ignores=[]), "original-candidate-settings", "exec"), namespace)
    for candidate, baseline in ((QWEN_9B, baseline_9b), (QWEN_4B, baseline_4b)):
        assert candidate.attention == "sdpa"
        assert namespace["candidate_settings"](Tokenizer(), baseline) == candidate_settings(Tokenizer(), candidate)
    return "Original 9B/4B complete settings match current defaults exactly"


def main():
    output = Path(__file__).resolve().parent / "handoff-validation.json"
    assert not output.exists(), "Preserve prior handoff evidence"
    report = dict(status="failed", previous_checkpoint=BEFORE, implementation_checkpoint=IMPLEMENTATION)
    try:
        assert git("merge-base", "--is-ancestor", IMPLEMENTATION, "HEAD") == b""
        changed = set(git("diff", "--name-only", BEFORE).decode().splitlines())
        unexpected = changed - set(CODE + DOCUMENTS + ["docs/validation/m5-inference-preparation.md"])
        unexpected = {p for p in unexpected if not p.startswith("notebooks/validation/m5-attention-memory/")}
        assert not unexpected, sorted(unexpected)
        protected = ["configs", "tests/fixtures", "AGENTS.md", "PROJECT_SPECIFICATION.md", "pyproject.toml", "README.md"]
        assert not git("diff", "--name-only", BEFORE, "--", *protected)
        recovery_diff = set(git("diff", "--name-only", BEFORE, "--", "recovery").decode().splitlines())
        assert recovery_diff == {"recovery/inference.py", "recovery/t4_attention.py"}, recovery_diff
        assert not git("diff", "--name-only", IMPLEMENTATION, "--", *CODE)
        for name in CODE:
            ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
        edit = "docs/validation/m5-inference-preparation.md"
        assert digest(ROOT / edit) == USER_EDIT
        assert not git("diff", "--cached", "--name-only", "--", edit)
        snapshots = prior_notebooks()
        payloads = {}
        for name in ["dist/m5-kaggle-preflight.zip", "dist/m5-kaggle-source-v2/m5-kaggle-source.payload",
                     "dist/m5-kaggle-pip-bootstrap-v3/m5-kaggle-source.payload"]:
            p = ROOT / name
            assert p.stat().st_size == 109248341
            assert digest(p) == "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
            payloads[name] = dict(bytes=p.stat().st_size, sha256=digest(p))
        index = (ROOT / "docs/todos/README.md").read_text(encoding="utf-8")
        states = Counter()
        for task in ROOT.glob("docs/todos/M[1-6]/M*-T*.md"):
            state = re.search(r"\*\*Status:\*\* (\w+)", task.read_text(encoding="utf-8")).group(1)
            identity = re.match(r"M\d-T\d+", task.name).group()
            row = re.search(r"^\| \[" + identity + r"[^\n]+", index, flags=re.M).group()
            assert re.search(r"\)\s*\|\s*" + state + r"\s*\|", row), identity
            states[state] += 1
        assert states == {"done": 21, "blocked": 8}
        counts = {}
        for name, expected in [("focused-regression", 96), ("native-attention-verified", 15),
                               ("native-tokenizer-9b", 4), ("native-tokenizer-4b", 4),
                               ("native-capacity", 8), ("installed-native-check", 15)]:
            result = json.loads((output.parent / (name + ".json")).read_bytes())
            raw = (output.parent / (name + ".stderr.txt")).read_text(encoding="utf-8")
            assert result["exit_code"] == 0 and result["actual_cuda_execution"] is False
            assert int(re.search(r"Ran (\d+) tests", raw).group(1)) == expected
            assert re.search(r"\bOK\b", raw) and "FAILED (" not in raw and "skipped=" not in raw
            assert not re.search(r"\.\.\. skipped", raw)
            counts[name] = expected
        memory = json.loads((output.parent / "memory-audit.json").read_bytes())
        assert memory["model_generations"] == 0 and memory["actual_cuda_execution"] is False
        assert memory["full_envelope_memory_acceptance"] is None and memory["model_selected"] is None
        assert memory["allocation"]["provider_duration_seconds"] is None
        assert memory["allocation"]["remaining_smoke_gpu_seconds"] is None
        assert set(memory["models"]) == {"9B", "4B"}
        for size, bound in [("target", 261388), ("fallback", 259868)]:
            assert memory["envelopes"][size]["complete_resident_tokens_upper"] == bound
            for model in ("9B", "4B"):
                case = memory["models"][model]["mathematical_sizes"][size]
                assert case["full_envelope_memory_acceptance"] is None
                assert case["complete_allocator_upper_bound_bytes"] is None
                assert case["proposed_kv_view_additional_storage_bytes"] == 0
                for comparison in case["device_comparisons"].values():
                    assert comparison["full_envelope_memory_acceptance"] is None
                    assert comparison["partial_subtotal_exceeds_native_allowance"] is (model == "9B")
        installed = json.loads((output.parent / "installed-native-check.json").read_bytes())
        assert installed["verified_module_count"] == 29 and installed["isolated_interpreter"] is True
        for module in installed["modules"]:
            assert digest(ROOT / module["path"]) == module["sha256"]
        selected = json.loads((output.parent / "transformers-source.json").read_bytes())
        assert len(selected["critical_installed_sources"]) == 8
        assert all(m["installed_bytes_match"] for m in selected["critical_installed_sources"])
        assert selected["wheel_sha256"] == "500be9eb644ede81c3103eee7687fc36d05dd75d1c76686c3820b26396fe7c7c"
        for name in ("actual-envelope-audit-verified", "project-pip-check", "package-build-verified"):
            assert json.loads((output.parent / (name + ".json")).read_bytes())["exit_code"] == 0
        for name in ("verify_handoff.py", "check_document_links.py"):
            ast.parse((output.parent / name).read_text(encoding="utf-8"), filename=name)
        report.update(status="passed", original_notebooks=snapshots, canonical_payloads=payloads,
            protected_scientific_paths_unchanged=protected, recovery_diff=sorted(recovery_diff),
            unexpected_tracked_changes=[], code_matches_implementation_commit=True,
            baseline_settings=baseline_settings(), existing_user_edit_sha256=USER_EDIT,
            existing_user_edit_unstaged=True, task_states=dict(states), test_counts=counts,
            source_and_native_checks=127, additional_installed_checks=15, skipped_checks=0,
            installed_modules_verified=29, selected_transformers_sources_verified=8,
            full_envelope_memory_acceptance=None, model_generations=0, actual_cuda_execution=False,
            provider_duration_seconds=None, remaining_smoke_gpu_seconds=None)
    except BaseException as error:
        report["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        with output.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
