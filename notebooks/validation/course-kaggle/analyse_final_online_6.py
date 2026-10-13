"""Read-only final-online-6 diagnosis; replay metadata defects without GPU/network.

Original submissions are never modified. SQLite copies open immutable/read-only.
Only archived stdlib functions are executed for the two software reproductions.
Pinned Hub responses and header-only HTTP receipts were collected separately.
"""

import argparse
import ast
from collections import Counter
from contextlib import closing
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
ORIGINALS = (
    "calls.html", "cases.html", "course-results.zip", "course-resume.payload",
    "intervals.csv", "last-action.json", "notebook-exec.ipynb", "plotting.json",
    "report.html", "world_contrasts.csv",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def archived_function(archive, module, name, scope):
    tree = ast.parse(archive.read("source/" + module))
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    assert len(nodes) == 1
    exec(compile(ast.Module(body=nodes, type_ignores=[]), module, "exec"), scope)
    return scope[name]


def analyse():
    from recovery.edits import apply_edit
    from recovery.evaluate import score_candidate
    from recovery.manifests import load_population
    from recovery.truth import solve_world
    from scripts.m5_kaggle_preflight import smoke_attempt_usage

    incident = ROOT / "notebooks/run/final-online-6"
    fixtures = Path(__file__).with_name("final-online-6-metadata")
    originals = {name: dict(bytes=(incident/name).stat().st_size,
                           sha256=digest((incident/name).read_bytes()))
                 for name in ORIGINALS}
    executed = json.loads((incident/"notebook-exec.ipynb").read_bytes())
    delivered = json.loads((ROOT/"notebooks/run/final-online-5/notebook-fixed.ipynb").read_bytes())
    assert len(executed["cells"]) == len(delivered["cells"]) == 9
    assert all("".join(a["source"]) == "".join(b["source"]) for a, b in zip(executed["cells"], delivered["cells"]))
    cell_outputs = [{"cell": i, "execution_count": cell.get("execution_count"),
                     "output_types": [o["output_type"] for o in cell.get("outputs", [])]}
                    for i, cell in enumerate(executed["cells"], 1)]
    assert not any("error" in c["output_types"] for c in cell_outputs)

    with zipfile.ZipFile(incident/"course-results.zip") as results, \
         zipfile.ZipFile(incident/"course-resume.payload") as resume, \
         tempfile.TemporaryDirectory(prefix="final-online-6-readonly-") as temporary:
        archives = {}
        for name, archive in (("results", results), ("resume", resume)):
            assert archive.testzip() is None
            assert len(archive.namelist()) == len(set(archive.namelist()))
            archives[name] = dict(members=len(archive.namelist()),
                                 expanded_bytes=sum(m.file_size for m in archive.infolist()), crc="passed")
        manifest_raw = resume.read("source/source-manifest.json")
        manifest = json.loads(manifest_raw)
        for name, expected in manifest["members"].items():
            raw = resume.read("source/" + name)
            assert len(raw) == expected["bytes"] and digest(raw) == expected["sha256"]
            if name.startswith("recovery/"):
                assert (ROOT/name).read_text(encoding="utf-8") == raw.decode("utf-8").replace("\r\n", "\n"), "Offline evaluator must match submitted core (native line endings normalized)"
        expected_sha = next(node.value.value for cell in delivered["cells"] if cell["cell_type"] == "code"
                            for node in ast.walk(ast.parse("".join(cell["source"])))
                            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                            and any(isinstance(t, ast.Name) and t.id == "EXPECTED_MANIFEST_SHA256" for t in node.targets))
        assert digest(manifest_raw) == expected_sha
        read = lambda name: json.loads(resume.read(name))
        last = read("last-action.json")
        assert last == json.loads(results.read("last-action.json")) == json.loads((incident/"last-action.json").read_bytes())
        config, coordinator = read("operator-config.json"), read("automatic-run.json")
        gate = read("candidates/9B/hardware-gate.json")
        report = read("candidates/9B/hardware/report.json")
        plan = read("candidates/9B/hardware/executed-plan.json")
        prefix = "environment-receipts/gpu-environment-bootstrap"
        setup = read(prefix+"/report.json")
        stages = sorted((read(n) for n in resume.namelist()
                         if n.startswith(prefix+"/logs/") and n.endswith(".json")),
                        key=lambda row: row["started_utc"])
        stages = [{k: row[k] for k in ("name", "status", "exit_code", "elapsed_seconds", "started_utc", "ended_utc")}
                  for row in stages]
        assert len(stages) == 13 and all(s["status"] == "passed" and s["exit_code"] == 0 for s in stages)

        temp = Path(temporary)
        population_file = temp/"population.json"
        population_file.write_bytes(resume.read("candidates/9B/inputs/population.json"))
        population = load_population(population_file)
        worlds = {world.world_id: world for world in population.development}
        planned = {row["smoke_call_id"]: row for row in plan["rows"]}
        paths, rows, processes, identities, table_checks = [], [], [], set(), []
        for worker in (0, 1):
            base = f"candidates/9B/hardware/worker-{worker}"
            path = temp/(base+".sqlite")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(resume.read(base+".sqlite"))
            backup = temp/(base+"-backup.sqlite")
            backup.write_bytes(resume.read(base+"-backup.sqlite"))
            paths.extend((path, backup))
            with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro&immutable=1", uri=True)) as db, \
                 closing(sqlite3.connect(backup.resolve().as_uri()+"?mode=ro&immutable=1", uri=True)) as old:
                db.row_factory = sqlite3.Row
                assert db.execute("PRAGMA integrity_check").fetchone()[0] == old.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
                differences = []
                for table in tables:
                    original_rows = [tuple(r) for r in db.execute('SELECT * FROM "'+table+'"')]
                    backup_rows = old.execute('SELECT * FROM "'+table+'"').fetchall()
                    if original_rows != backup_rows:
                        differences.append(table)
                    if table != "allocations":
                        assert original_rows == backup_rows
                assert differences == ["allocations"]
                table_checks.append(dict(worker=worker, tables=len(tables), backup_attempts_and_calls_identical=True,
                                         backup_different_tables=differences, integrity="ok"))
                for attempt in db.execute("SELECT * FROM attempts"):
                    identities.add((attempt["call_id"], attempt["number"], attempt["started_at"]))
                    call = db.execute("SELECT * FROM calls WHERE call_id=?", (attempt["call_id"],)).fetchone()
                    row = planned[call["call_id"]]
                    facts, raw, validation = (json.loads(attempt["backend_json"]), json.loads(call["raw_json"]), json.loads(call["validation_json"]))
                    samples = facts["observed_model_edge_memory"]
                    diagnostic = bool(facts.get("hardware_diagnostic"))
                    origin = row["origin_call_id"].split("/")
                    world = worlds[origin[0]]
                    truth = solve_world(apply_edit(world.world, world.main_edit) if origin[2] == "revision" else world.world)
                    peer = None if origin[-1] == "full" else int(origin[-1][1:])
                    candidate_status = validation["candidate"]["status"]
                    candidate = json.loads(raw["text"])["candidate"] if candidate_status == "valid" else None
                    scored = None if diagnostic else score_candidate(truth, candidate_status, candidate, peer)
                    rows.append(dict(call_id=call["call_id"], worker=worker, origin_call_id=row["origin_call_id"],
                                     purpose=row["purpose"], task=world.world.task.value, hardware_diagnostic=diagnostic,
                                     attempt_number=attempt["number"], status=attempt["status"], seed=call["seed"],
                                     request_tokens=call["request_tokens"], input_tokens=row["input_tokens"],
                                     output_tokens=len(raw["token_ids"]), termination=raw["termination"],
                                     elapsed_seconds=attempt["elapsed_seconds"], timeout_seconds=attempt["timeout_seconds"],
                                     uncertain_completion=attempt["uncertain_completion"],
                                     protocol_status=candidate_status if not diagnostic else "not_applicable_tensor_diagnostic",
                                     feedback=(validation["feedback"] or {}).get("code") if not diagnostic else None,
                                     prose_tokens=validation["prose_tokens"] if not diagnostic else None,
                                     exact_correct=scored, model_text=raw["text"],
                                     evaluator_gold=truth.candidate(peer) if not diagnostic else None,
                                     peak_allocated_bytes=attempt["peak_memory_bytes"],
                                     peak_reserved_bytes=facts["peak_reserved_bytes"],
                                     device_peak_occupied_bytes=max(s["total_bytes"]-s["free_bytes"] for s in samples),
                                     minimum_free_bytes=min(s["free_bytes"] for s in samples),
                                     ending_free_with_cache=facts["free_bytes_with_cache"],
                                     finite_score_steps=facts["finite_score_steps"], cache=facts["cache"],
                                     memory_samples=len(samples), raw_sha256=digest(call["raw_json"].encode()),
                                     settings_sha256=digest(db.execute("SELECT settings_json FROM round_inputs WHERE branch_id=? AND round_number=?", (call["branch_id"], call["round_number"])).fetchone()[0].encode())))
                for process in db.execute("SELECT * FROM provider_processes"):
                    load = json.loads(process["backend_json"])
                    processes.append(dict(worker=worker, pid=process["pid"], call_id=process["call_id"],
                                          started_at=process["started_at"], ready_at=process["ready_at"],
                                          stopped_at=process["stopped_at"], uncertain_stop=process["uncertain_stop"],
                                          device_uuid=load["cuda_visible_devices"], model=load["model"], revision=load["revision"],
                                          recurrent_fast_path=load["recurrent_fast_path"], loading_info=load["loading_info"],
                                          actual_tensor_devices=load["actual_tensor_devices"]))
        rows.sort(key=lambda row: (row["hardware_diagnostic"], row["call_id"]))
        assert len(rows) == len(identities) == 22
        assert all(r["status"] == "completed" and not r["uncertain_completion"] for r in rows)
        assert all(p["stopped_at"] and not p["uncertain_stop"] for p in processes)
        ordinary = [r for r in rows if not r["hardware_diagnostic"]]
        controls = [r for r in ordinary if "/control/" in r["origin_call_id"]]
        validity = dict(Counter(r["protocol_status"] for r in ordinary))
        assert validity == {"invalid": 10, "valid": 11}
        assert len(controls) == 3 and sum(r["exact_correct"] for r in controls) == 0
        duplicate_replies = []
        for first, second in (("02", "20"), ("05", "21")):
            a, b = [next(r for r in rows if r["call_id"] == "smoke/course-m5/"+n) for n in (first, second)]
            assert a["raw_sha256"] == b["raw_sha256"] and a["settings_sha256"] == b["settings_sha256"] and a["seed"] == b["seed"]
            duplicate_replies.append(dict(first=a["call_id"], second=b["call_id"], exact_raw_match=True, full_restart_sequence_complete=False))
        usage = smoke_attempt_usage(config["budget"], paths)
        assert usage["total_recorded"] == 45 and coordinator["cumulative_preparation_attempts"] == 67
        # Execute the archived selector against unmodified canonical+backup data.
        child = temp/"candidates/9B"
        (child/"automatic-run.json").write_bytes(resume.read("candidates/9B/automatic-run.json"))
        (child/"hardware/report.json").write_bytes(resume.read("candidates/9B/hardware/report.json"))
        choice = archived_function(resume, "scripts/course_kaggle_bootstrap.py", "qualification_choice",
                                   dict(Path=Path, json=json, sqlite3=sqlite3, closing=closing))
        assert choice(temp, config) == ("4B", 67)
        # Scope diagnosis to the known stdlib inventory function, offline fixture.
        inventory = archived_function(resume, "scripts/m5_course_smoke_assets.py", "native_checkpoint_files", dict(json=json, re=re))
        checkpoint = {}
        for label in ("9B", "4B"):
            inspection = read(f"source/notebooks/validation/course-kaggle/repair-candidates/{label}/inspection.json")
            hub_raw = (fixtures/f"{label}-hub.json").read_bytes()
            hub = json.loads(hub_raw)
            native = {s["rfilename"]: dict(bytes=s["lfs"]["size"], sha256=s["lfs"]["sha256"])
                      for s in hub["siblings"] if s["rfilename"] in inspection["checkpoint_index"]["shard_files"]}
            native_total = sum(v["bytes"] for v in native.values())
            with patch("urllib.request.urlopen", side_effect=lambda *a, **kw: io.BytesIO(hub_raw)):
                try:
                    actual = inventory(inspection)
                    reproduction = dict(status="passed", native_inventory_equal=actual == native)
                except ValueError as error:
                    reproduction = dict(status="refused", reason=str(error))
            checkpoint[label] = dict(model=inspection["model"], revision=inspection["revision"],
                                     native_files=native, native_file_bytes=native_total,
                                     archived_total_checkpoint_bytes=inspection["checkpoint_index"]["total_checkpoint_bytes"],
                                     difference_bytes=native_total-inspection["checkpoint_index"]["total_checkpoint_bytes"],
                                     metadata_fixture_sha256=digest(hub_raw), reproduction=reproduction)
        assert checkpoint["9B"]["reproduction"]["status"] == "passed"
        assert checkpoint["4B"]["reproduction"]["reason"] == "pinned checkpoint byte inventory differs"
        headers = []
        for name, native in checkpoint["4B"]["native_files"].items():
            header_raw = (fixtures/(name+".header.json")).read_bytes()
            header, receipt = json.loads(header_raw), json.loads((fixtures/(name+".header-receipt.json")).read_bytes())
            payload = sum(v["data_offsets"][1]-v["data_offsets"][0] for k, v in header.items() if k != "__metadata__")
            assert payload+len(header_raw)+8 == native["bytes"] == receipt["file_bytes"]
            assert payload == receipt["payload_bytes"] and receipt["tensor_bytes_downloaded"] == 0
            headers.append(dict(receipt, header_sha256=digest(header_raw)))
        assert sum(h["payload_bytes"] for h in headers) == checkpoint["4B"]["archived_total_checkpoint_bytes"]
        assert sum(h["header_bytes"]+8 for h in headers) == checkpoint["4B"]["difference_bytes"] == 90240
        coverage = read("candidates/9B/analysis-receipt.json")
        assert coverage["coverage"] == {"protocol_outcomes": {"unknown": 6280}, "recorded": 0, "scheduled": 6280, "unknown": 6280}
        assert not any(n.startswith(("candidates/4B/hardware/", "candidates/9B/development/", "candidates/9B/main/")) and n.endswith(".sqlite") for n in resume.namelist())
        assert not any(n.endswith("/run.json") for n in resume.namelist())
        external_reports = {}
        report_prefix = "candidates/9B/analyses/20261013T195440312066Z/"
        for name in ("calls.html", "cases.html", "report.html", "intervals.csv", "world_contrasts.csv", "plotting.json"):
            external_reports[name] = (incident/name).read_bytes() == resume.read(report_prefix+name)
        assert all(external_reports.values())
        # Result ZIP is a readable subset; canonical workers live in resume only.
        assert not any(n.endswith(".sqlite") for n in results.namelist())
        submission_unchanged = all(digest((incident/n).read_bytes()) == f["sha256"] for n, f in originals.items())
        assert submission_unchanged
        evidence = dict(source_commit=manifest["source_baseline_commit"], manifest_sha256=digest(manifest_raw),
                        verified_source_members=len(manifest["members"]), notebook_literal_match=True, cell_outputs=cell_outputs,
                        originals=originals, archives=archives, external_reports_match=external_reports,
                        setup=setup, setup_stages=stages, hardware_gate=gate, attempts=rows,
                        worker_checks=table_checks, processes=processes, repeated_response_checks=duplicate_replies,
                        ordinary_protocol_counts=validity, ordinary_feedback_counts=dict(Counter(r["feedback"] or "valid" for r in ordinary)),
                        hardware_control_exact_correct=sum(r["exact_correct"] for r in controls), hardware_control_count=len(controls),
                        all_ordinary_exact_correct=sum(r["exact_correct"] for r in ordinary),
                        unexecuted_matrix_ids=sorted(set(planned)-{r["call_id"] for r in rows}),
                        stale_executed_plan_rows=sum(r.get("executed") is False for r in plan["rows"]),
                        hardware_report_largest_resident=report["smoke"]["largest_prepared_request_resident_tokens"],
                        accounting=dict(canonical_usage=usage, coordinator_reported=coordinator["cumulative_preparation_attempts"],
                                        archived_selector_candidate="4B", archived_selector_prior=67, corrected_prior=45,
                                        remaining_cumulative=71-usage["total_recorded"], remaining_4B_matrix=24,
                                        hardware_observed_gpu_hours=report["smoke"]["resources"]["allocated_gpu_hours"],
                                        hardware_partition_seconds=report["smoke"]["resources"]["partition_seconds"]),
                        checkpoint=checkpoint, safetensors_headers=headers,
                        last_action=last, controller_error=read("logs/controller-error.json"),
                        coordinator_selected_candidate=coordinator["selected_candidate"],
                        saved_4B_prior=read("candidates/4B/operator-config.json")["budget"]["prior_smoke_attempts"],
                        coverage=coverage, main_audit=read("candidates/9B/main-audit.json"),
                        submission_unchanged=submission_unchanged,
                        diagnostic_execution=dict(gpu_calls=0, tensor_bytes_downloaded=0, network_required=False,
                                                  scientific_outcomes_modified=False, production_code_modified=False))
        start = datetime.fromisoformat(config["allocated_at"])
        stop = datetime.fromisoformat(evidence["controller_error"]["at"])
        evidence["notebook_observation_seconds_to_error"] = (stop-start).total_seconds()
        return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("final-online-6-analysis.json"))
    args = parser.parse_args()
    evidence = analyse()
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(status="passed", output=str(args.output), new_recorded_attempts=22,
                          canonical_cumulative_attempts=45, ordinary_protocol=evidence["ordinary_protocol_counts"],
                          hardware_control_exact_correct="0/3", main_recorded=0, main_unknown=6280,
                          offline_defects_reproduced=2, gpu_calls=0, submission_unchanged=True), indent=2))
