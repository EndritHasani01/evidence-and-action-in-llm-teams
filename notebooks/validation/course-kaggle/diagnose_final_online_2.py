"""Read the submitted incident and reproduce its adapter defect without a GPU.

Run from the repository root. This does not modify submitted artifacts, load
weights, fix production code, or certify physical model placement.
"""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import zipfile


def diagnose(incident, wheel=None):
    from recovery.inference import audit_language_load
    from tests.inference_mocks import LOADING_INFO, Qwen3_5ForCausalLM, Tensor
    from scripts.m5_course_smoke import admission, utc

    notebook = json.loads((incident / "notebook-exec.ipynb").read_bytes())
    files = {p.name: {"bytes": p.stat().st_size,
                      "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(incident.iterdir()) if p.is_file()}
    with zipfile.ZipFile(incident / "course-results.zip") as results:
        assert results.testzip() is None
        action = json.loads(results.read("last-action.json"))
        gate = json.loads(results.read("hardware-gate.json"))
        analysis = json.loads(results.read("analysis-receipt.json"))
        smoke = next(s["result"]["smoke"] for s in action["stages"]
                     if s["stage"] == "hardware")
    with zipfile.ZipFile(incident / "preflight-results.zip") as preflight:
        assert preflight.testzip() is None
        manifest = json.loads(preflight.read("source-manifest.json"))
        commands = []
        for name in sorted(preflight.namelist()):
            if name.startswith("logs/") and name.endswith(".json"):
                command = json.loads(preflight.read(name))
                commands.append({key: command.get(key) for key in
                                 ("name", "status", "elapsed_seconds", "started_utc", "ended_utc")})
        weights = json.loads(preflight.read("weights.json"))
    original = subprocess.check_output(["git", "show", manifest["source_baseline_commit"]+":recovery/inference.py"])
    audit_node = next(n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef) and n.name == "audit_language_load")
    namespace = {}
    exec(compile(ast.Module(body=[audit_node],type_ignores=[]), "submitted-source/recovery/inference.py", "exec"),namespace)
    historical_audit = namespace["audit_language_load"]
    model = Qwen3_5ForCausalLM()
    baseline = historical_audit(model, LOADING_INFO)["device_map"]
    del model.hf_device_map
    try:
        historical_audit(model, LOADING_INFO)
    except AttributeError as error:
        reproduced = f"{type(error).__name__}: {error}"
    else:
        raise AssertionError("The historical missing-map defect no longer reproduces; update diagnosis")
    model.embedding = Tensor(device="cpu")
    try:
        audit_language_load(model, LOADING_INFO)
    except ValueError as error:
        cpu_rejected = str(error)
    else:
        raise AssertionError("Off-device tensor was admitted")
    budget = json.loads(Path("configs/course-kaggle.json").read_bytes())["budget"]
    budget.update(prior_smoke_attempts=24, prior_evidence="Synthetic CPU diagnostic: 24 prior recorded attempts")
    launch = dict(resource_policy="observe", authorization="CPU diagnosis only; no inference",
                  budget=budget, allocated_at=utc(), session_limit_seconds=36000)
    from recovery.accounting import BudgetStop
    try:
        _, window = admission(launch, next_attempt=True)
        prior_limit_enforced = False
    except BudgetStop:
        prior_limit_enforced = True
    corrected_model = Qwen3_5ForCausalLM()
    del corrected_model.hf_device_map
    corrected_report = audit_language_load(corrected_model, LOADING_INFO)
    wheel_evidence = None
    if wheel:
        pinned = next(w for w in manifest["candidate_wheels"] if w["name"] == "transformers")
        assert wheel.stat().st_size == pinned["bytes"]
        assert hashlib.sha256(wheel.read_bytes()).hexdigest() == pinned["sha256"]
        with zipfile.ZipFile(wheel) as archive:
            lines = archive.read("transformers/modeling_utils.py").decode().splitlines()
        matches = [i for i, line in enumerate(lines)
                   if "if device_map is not None and len(set(device_map.values())) > 1:" in line]
        assert len(matches) == 1
        i = matches[0]
        wheel_evidence = dict(version=pinned["version"], sha256=pinned["sha256"],
                              member="transformers/modeling_utils.py", line=i + 1,
                              excerpt=lines[i - 1:i + 2])
    fixed = json.loads(Path("notebooks/run/final-online-1/notebook-fixed.ipynb").read_bytes())
    return dict(analysis_date="2026-10-13", scope="CPU incident diagnosis; production code unchanged",
                incident_files=files, source_commit=manifest["source_baseline_commit"],
                kernel=notebook["metadata"]["language_info"]["version"],
                delivered_cell_sources_match=all("".join(a["source"]) == "".join(b["source"])
                                                for a, b in zip(notebook["cells"], fixed["cells"])),
                result_status=action["status"], reason=action["reason"],
                smoke={k: smoke[k] for k in ("completed_model_generations", "model_physical_attempts", "process_cleanup")},
                hardware_gate=gate, coverage=analysis["coverage"],
                checkpoint_bytes=sum(f["bytes"] for f in weights["checkpoint_files"].values()),
                wheel_bytes=sum(w["bytes"] for w in manifest["candidate_wheels"]),
                commands=commands, pinned_loader=wheel_evidence,
                cpu_reproductions=dict(baseline_device_map=baseline, missing_map_error=reproduced,
                                       off_device_tensor_rejected=cpu_rejected,
                                       current_prior_limit_enforced=prior_limit_enforced,
                                       current_absent_map_accepted=corrected_report["device_map"] is None),
                diagnostic_gpu_calls=0, diagnostic_weights_loaded=False,
                evidence_limits=["No course-resume.payload supplied: original SQLite attempts/processes were not inspected",
                                 "No successful native load report or model generation; no T4 feasibility established"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incident", type=Path, default=Path("notebooks/run/final-online-2"))
    parser.add_argument("--transformers-wheel", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    print(json.dumps(diagnose(args.incident, args.transformers_wheel), indent=2))
