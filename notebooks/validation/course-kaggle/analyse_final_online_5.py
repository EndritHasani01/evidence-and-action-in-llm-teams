"""Read the submitted storage incident and exercise its real guard on CPU.

No downloads, installation, model imports, GPU calls or submitted-file writes.
The dashboard transcription is user-supplied, not filesystem telemetry.
"""

import argparse
import ast
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
HISTORICAL_GUARD = None


def guard_probe(additional, readings, location="scratch"):
    from scripts import m5_kaggle_preflight as preflight

    paths = {role: Path("/synthetic") / role for role in readings}
    by_path = {paths[role]: reading for role, reading in readings.items()}

    def disk_usage(path):
        reading = by_path[Path(path)]
        return shutil._ntuple_diskusage(
            reading["total"], reading["total"] - reading["free"], reading["free"])

    with patch.object(Path, "stat", lambda p: SimpleNamespace(st_dev=by_path[p]["device"])), \
         patch.object(preflight.shutil, "disk_usage", side_effect=disk_usage):
        try:
            facts = HISTORICAL_GUARD(paths[location], paths["output"], additional)
            return dict(status="admitted", facts=facts)
        except ValueError as error:
            return dict(status="refused", reason=str(error))


def analyse():
    global HISTORICAL_GUARD
    from scripts.m5_kaggle_preflight import BUILD_RESERVE, OUTPUT_RESERVE

    incident = ROOT / "notebooks/run/final-online-5"
    originals = [incident/name for name in ('course-results.zip','course-resume.payload','last-action.json','notebook-exec.ipynb')]
    hashes = {p.name: dict(bytes=p.stat().st_size,
                         sha256=hashlib.sha256(p.read_bytes()).hexdigest())
              for p in originals}
    executed = json.loads((incident / "notebook-exec.ipynb").read_bytes())
    delivered = json.loads((ROOT / "notebooks/run/final-online-4/notebook-fixed.ipynb").read_bytes())

    def code(nb):
        return [ast.dump(ast.parse("".join(c["source"])))
                for c in nb["cells"] if c["cell_type"] == "code"]

    assert code(executed) == code(delivered)
    with zipfile.ZipFile(incident / "course-results.zip") as results, \
         zipfile.ZipFile(incident / "course-resume.payload") as resume:
        assert results.testzip() is None and resume.testzip() is None
        manifest_bytes = resume.read("source/source-manifest.json")
        manifest = json.loads(manifest_bytes)
        expected_manifest = [node.value.value
                             for c in delivered["cells"] if c["cell_type"] == "code"
                             for node in ast.walk(ast.parse("".join(c["source"])))
                             if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                             and any(isinstance(t, ast.Name) and t.id == "EXPECTED_MANIFEST_SHA256"
                                     for t in node.targets)]
        assert len(expected_manifest) == 1
        manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
        assert manifest_sha256 == expected_manifest[0]
        # Keep this incident reproducible after repairing the live guard. Only
        # these two original stdlib functions are executed on simulated paths.
        original = ast.parse(resume.read('source/scripts/m5_kaggle_preflight.py'))
        selected = [n for n in original.body if isinstance(n,ast.FunctionDef)
                    and n.name in ('filesystem_facts','require_space')]
        assert len(selected) == 2
        scope = dict(Path=Path,shutil=shutil,OUTPUT_RESERVE=OUTPUT_RESERVE)
        exec(compile(ast.Module(body=selected,type_ignores=[]),'submitted-storage-guard','exec'),scope)
        HISTORICAL_GUARD = scope['require_space']
        for name, expected in manifest["members"].items():
            raw = resume.read("source/" + name)
            assert len(raw) == expected["bytes"]
            assert hashlib.sha256(raw).hexdigest() == expected["sha256"]
        prefix = next(n.rsplit("/", 1)[0] for n in resume.namelist()
                      if n.startswith("environment-receipts/") and n.endswith("/report.json"))
        report = json.loads(resume.read(prefix + "/report.json"))
        assert report == json.loads(results.read(prefix + "/report.json"))
        with zipfile.ZipFile(io.BytesIO(resume.read(prefix + "/preflight-results.zip"))) as nested:
            assert nested.testzip() is None
            assert report == json.loads(nested.read("report.json"))
        launch = json.loads(resume.read(prefix + "/launch.json"))
        plan = json.loads(resume.read(prefix + "/hardware-plan-contract.json"))
        config = json.loads(resume.read("operator-config.json"))
        last = json.loads(resume.read("last-action.json"))
        assert last == json.loads(results.read("last-action.json"))
        assert last == json.loads((incident / "last-action.json").read_bytes())
        stages = []
        for n in resume.namelist():
            if n.startswith(prefix + "/logs/") and n.endswith(".json"):
                row = json.loads(resume.read(n))
                stages.append({k: row[k] for k in
                               ("name", "status", "started_utc", "ended_utc", "elapsed_seconds", "exit_code")})
        stages.sort(key=lambda row: row["started_utc"])
        workers = [n for n in resume.namelist() if n.endswith((".sqlite", ".sqlite3", ".db"))]
        assert not workers
        assert all(row["status"] == "passed" and row["exit_code"] == 0 for row in stages)
        assert not any(row["name"] == "stage-pinned-checkpoint" for row in stages)
        assert not any(report[k] for k in ("gpu_execution", "model_weights_loaded", "weights_staged"))
        assert plan["plan_rows"] == plan["constructors_checked"] == 24
        assert plan["gpu_calls"] == 0
        checkpoint_bytes = {}
        for label in ("9B", "4B"):
            name = f"source/notebooks/validation/course-kaggle/repair-candidates/{label}/inspection.json"
            checkpoint_bytes[label] = json.loads(resume.read(name))["checkpoint_index"]["total_checkpoint_bytes"]
        additional = checkpoint_bytes["9B"] + BUILD_RESERVE
        required = additional + OUTPUT_RESERVE
        assert report["root_blocker"] == f"ValueError: scratch_capacity: additional_required={required}"
        assert required == 20_648_488_160
        assert launch["hf_cache"] is None and config["candidate"] == "9B"
        command_scratch = json.loads(resume.read(prefix + "/logs/create-candidate.json"))["cwd"]
        text_outputs = "\n".join("".join(o.get("text", []))
                                 for c in executed["cells"] for o in c.get("outputs", []))
        error_outputs = sum(o.get("output_type") == "error"
                            for c in executed["cells"] for o in c.get("outputs", []))
        assert "Bootstrap failed; its receipt and logs are retained" in text_outputs
        assert not any("storage" in n for n in resume.namelist()
                       if n.startswith("environment-receipts/"))

    gib = 2**30

    def reading(free, device=1, total=60):
        return dict(device=device, total=int(total*gib), free=int(free*gib))

    # Reproduce the exact exception, then show that the dashboard's approximate
    # values cannot explain it when supplied to the actual guard on this pool.
    low = guard_probe(additional, dict(scratch=reading(18), output=reading(18)))
    assert low["reason"] == f"scratch_capacity: additional_required={required}"
    dashboard = guard_probe(additional, dict(scratch=reading(55.4, total=57.6),
                                            output=reading(55.4, total=57.6)))
    assert dashboard["status"] == "admitted"
    # The call site currently checks installation scratch rather than the cache.
    # Different writable pools expose both a false refusal and a false admission.
    separate = dict(scratch=reading(18), output=reading(18), cache=reading(40, device=2))
    wrong_refusal = guard_probe(additional, separate)
    correct_cache = guard_probe(additional, separate, location="cache")
    assert wrong_refusal["status"] == "refused" and correct_cache["status"] == "admitted"
    separate_low_cache = dict(scratch=reading(40), output=reading(40), cache=reading(1, device=2))
    wrong_admission = guard_probe(additional, separate_low_cache)
    correct_refusal = guard_probe(additional, separate_low_cache, location="cache")
    assert wrong_admission["status"] == "admitted" and correct_refusal["status"] == "refused"
    # An already complete shard and its obsolete partial cannot both reduce
    # bytes still needed for other shards. The current sum credits both.
    total, complete, obsolete_partial = 200, 100, 80
    credited = max(0, total - complete - obsolete_partial)
    actual_incoming = total - complete
    assert credited == 20 and actual_incoming == 100

    failure_at = stages[-1]["ended_utc"]
    observed_seconds = (datetime.fromisoformat(failure_at) -
                        datetime.fromisoformat(launch["allocated_at"])).total_seconds()
    return dict(
        status="analysed_read_only", submitted_files=hashes,
        source_commit=manifest["source_baseline_commit"], verified_source_members=len(manifest["members"]),
        source_manifest_sha256=manifest_sha256, manifest_matches_delivered_notebook=True,
        notebook_code_equal=True, archive_crc_checks=3, command_stages=stages,
        executed_notebook_uncaught_errors=error_outputs,
        failure=report, outer_last_action=last, scratch_path=command_scratch,
        inferred_default_cache=command_scratch + "/hub",
        required_bytes=dict(checkpoint=checkpoint_bytes["9B"], build_reserve=BUILD_RESERVE,
                            shared_output_reserve=OUTPUT_RESERVE, total=required,
                            total_gib=required/gib),
        physical_generations=0, worker_databases=workers,
        historical_preparation_attempts=config["budget"]["prior_smoke_attempts"],
        cumulative_attempt_limit=config["smoke_attempt_limit"],
        main_coverage=dict(recorded=0, unknown=6280),
        weights_download_command_started=False, elapsed_observed_to_last_setup_command_seconds=observed_seconds,
        provider_release_confirmed=False,
        user_dashboard=dict(source="chat screenshot, later session-level observation",
                            session_minutes=12, session_limit_hours=12,
                            disk_used_gib=2.2, disk_max_gib=57.6,
                            ram_used_gib=2.1, ram_max_gib=30,
                            gpu_count=2, gpu_type="T4", gpu_utilization_percent=[0, 0],
                            gpu_memory_bytes=[0, 0], gpu_memory_max_gib_each=15,
                            filesystem_paths_or_mounts_not_shown=True),
        missing_failure_telemetry=["free_bytes", "total_bytes", "mount or filesystem identity",
                                   "cache disk measurement", "installed environment disk footprint"],
        cpu_counterexamples=dict(exact_refusal=low, dashboard_values=dashboard,
                                 wrong_scratch_refusal=wrong_refusal, cache_admitted=correct_cache,
                                 wrong_scratch_admission=wrong_admission, cache_refused=correct_refusal,
                                 stale_partial_credit=dict(current_incoming_estimate=credited,
                                                           actual_incoming=actual_incoming)),
        checkpoint_shard_bytes=checkpoint_bytes,
        candidate_wheel_count=len(manifest["candidate_wheels"]),
        candidate_wheel_download_bytes=sum(w["bytes"] for w in manifest["candidate_wheels"]),
        constraints_unchanged=True, production_files_changed=False,
        analysis_environment=dict(python=sys.version.split()[0], platform=sys.platform,
                                  gpu_calls=0, weight_downloads=0, model_imports=0),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = analyse()
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(receipt, output, indent=2)
        output.write("\n")
    print(json.dumps(dict(status=receipt["status"], root_blocker=receipt["failure"]["root_blocker"],
                          verified_source_members=receipt["verified_source_members"],
                          gpu_calls=0, output=str(args.output))))
