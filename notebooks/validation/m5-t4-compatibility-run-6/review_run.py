"""Read-only review of supplied T4 diagnostics; never execute notebook cells."""

import ast
from contextlib import closing
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sqlite3
import stat
import subprocess
import sys
import zipfile

import nbformat

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts import m5_kaggle_preflight as helper
from scripts import m5_t4_compatibility as diagnostic


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source(cell):
    return "".join(cell.get("source", []))


def constants(program):
    result = {}
    for node in ast.parse(program).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            try:
                value = node.value
                if isinstance(value, ast.Call) and ast.unparse(value.func) == "json.loads":
                    result[node.targets[0].id] = json.loads(ast.literal_eval(value.args[0]))
                else:
                    result[node.targets[0].id] = ast.literal_eval(value)
            except (ValueError, TypeError):
                pass
    return result


originals = [ROOT / "notebooks/run/6" / name for name in ["notebook-exec.ipynb", "preflight-results.zip"]]
before = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in originals}
notebook = json.loads(originals[0].read_text(encoding="utf-8"))
shipped = json.loads((ROOT / "notebooks/recovery_m5_kaggle_t4_compatibility.ipynb").read_text(encoding="utf-8"))
nbformat.validate(nbformat.from_dict(notebook))
assert len(notebook["cells"]) == 7 and len(shipped["cells"]) == 6
assert [source(c) for c in notebook["cells"][:6]] == [source(c) for c in shipped["cells"]]
assert source(notebook["cells"][6]) == "" and notebook["cells"][6]["execution_count"] is None
assert not notebook["cells"][6]["outputs"]
code = [c for c in notebook["cells"] if c["cell_type"] == "code"]
for cell in code:
    ast.parse(source(cell))
assert [c["execution_count"] for c in code] == [1, 2, 3, None]
assert not any(o.get("output_type") == "error" for c in code for o in c["outputs"])
binding = constants(source(notebook["cells"][1]))
expected = binding["EXPECTED"]
for key, field, path in [
    ("program_sha256", "COMPATIBILITY_PROGRAM", "scripts/m5_t4_compatibility.py"),
    ("operations_sha256", "OPERATIONS_PROGRAM", "scripts/m5_kaggle_preflight.py")]:
    assert digest(binding[field].encode()) == expected[key]
    committed = subprocess.check_output(["git", "show", expected["build_commit"] + ":" + path], cwd=ROOT)
    assert binding[field] == committed.decode().replace("\r\n", "\n")

with zipfile.ZipFile(originals[1]) as archive:
    members = archive.infolist()
    assert len(members) == 23 and sum(m.file_size for m in members) == 268136
    assert len({m.filename.casefold() for m in members}) == len(members) and archive.testzip() is None
    exported = {}
    for member in members:
        path = PurePosixPath(member.filename)
        assert member.orig_filename == member.filename and not member.is_dir()
        assert not path.is_absolute() and not {".", ".."}.intersection(path.parts)
        assert "\\" not in member.filename and ":" not in member.filename
        assert not stat.S_ISLNK(member.external_attr >> 16) and path.suffix in {".json", ".txt", ".sqlite"}
        exported[member.filename] = archive.read(member)
for name, data in exported.items():
    path = OUTPUT / "export" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == data
    else:
        path.write_bytes(data)

read_json = lambda name: json.loads(exported[name])
report, summary = read_json("compatibility-report.json"), read_json("summary.json")
assert report["summary"] == summary and summary["library_checks_completed"] is True
assert report["root_blocker"] is None and not report["process_cleanup_unconfirmed"] and "export_error" not in report
assert all(stage["status"] == "passed" for stage in report["stages"].values()) and len(report["stages"]) == 6
assert type(summary["model_generations"]) is int and summary["model_generations"] == 0
assert summary["model_smoke_ready"] is False
assert all(summary[k] is None for k in ["full_candidate_gpu_acceptance", "native_qwen_recurrent_acceptance",
    "full_envelope_memory_acceptance", "provider_assignment_utc", "provider_release_utc"])
assert read_json("expected-inputs.json") == expected
assert exported["gpu-probe-program.txt"] == binding["COMPATIBILITY_PROGRAM"].encode()
assert report["stages"]["static_envelope"]["result"] == diagnostic.envelope_assessment(expected["configs"])
assert len(expected["candidate_versions"]) == 88
host = read_json("host-software.json")
assert set(host["versions"]) == set(expected["candidate_versions"]) and host["versions"]["torch"] == "2.11.0+cu128"
assert host["candidate_differences"] == {name: {"candidate": v, "host": host["versions"][name]}
    for name, v in expected["candidate_versions"].items() if host["versions"][name] != v}

commands = {PurePosixPath(n).stem: read_json(n) for n in exported if n.startswith("logs/") and n.endswith(".json")}
assert set(commands) == {"gpu-inventory", "download-bitsandbytes-wheel", "device_0", "device_1"}
for name, record in commands.items():
    assert record["status"] == "passed" and record["exit_code"] == 0 and record["leader_exited"] is True
    assert record["tree_confirmation"] == "exited" and record["elapsed_seconds"] < record["timeout_seconds"]
    assert record["stdout"] in exported and record["stderr"] in exported
    measured = (datetime.fromisoformat(record["ended_utc"]) - datetime.fromisoformat(record["started_utc"])).total_seconds()
    assert abs(measured - record["elapsed_seconds"]) < 0.01
assert commands["gpu-inventory"]["timeout_seconds"] == 10
assert all(commands[name]["timeout_seconds"] == 60 for name in commands if name != "gpu-inventory")
assert all(commands[name]["args"][1:3] == ["-I", "-B"] for name in commands if name != "gpu-inventory")
inventory = diagnostic.parse_inventory(exported[commands["gpu-inventory"]["stdout"]].decode())
assert inventory == report["stages"]["host_inventory"]["result"]["devices"]
snapshot = read_json("extracted-wheel.json")
wheel = expected["bitsandbytes_wheel"]
assert snapshot["wheel"] == wheel and snapshot["expanded_bytes"] == wheel["expanded_bytes"]
assert len(snapshot["files"]) == wheel["members"] == 85
assert read_json(commands["download-bitsandbytes-wheel"]["stdout"]) == dict(wheel, verified=True)
local_wheel = ROOT / "build/m5-t4-compatibility-input" / wheel["filename"]
assert local_wheel.stat().st_size == wheel["bytes"] and helper.sha256_file(local_wheel) == wheel["sha256"]
with zipfile.ZipFile(local_wheel) as archive:
    assert archive.testzip() is None and set(archive.namelist()) == set(snapshot["files"])
    for member in archive.infolist():
        assert snapshot["files"][member.filename] == {"bytes": member.file_size, "sha256": digest(archive.read(member))}

devices = {}
for index, physical in enumerate(inventory):
    name = "device_" + str(index)
    probe = read_json(name + ".json")
    command = commands[name]
    assert probe == report["stages"][name]["result"]
    package = PurePosixPath(command["cwd"]) / "diagnostic-package"
    for field in ["bitsandbytes_root", "bitsandbytes_native_library"]:
        assert PurePosixPath(probe[field]).is_absolute() and PurePosixPath(probe[field]).is_relative_to(package)
    diagnostic.validate_probe(probe, physical["uuid"], Path(package.as_posix()))
    assert command["args"][command["args"].index("--uuid")+1] == physical["uuid"]
    assert command["args"][command["args"].index("--package-root")+1] == package.as_posix()
    observations = {}
    for case, row in probe["attention"].items():
        assert row["status"] == "passed" and diagnostic.backend_name(row["operators"]) == row["operator_backend"]
        backend = "math" if case.endswith("-gqa") else "efficient"
        assert row["operator_backend"] == backend and row["eligibility"]["efficient"] is (backend == "efficient")
        assert row["eligibility"]["flash"] is False and row["eligibility"]["cudnn"] is False
        assert row["cuda_kernel_trace_available"] is True and row["cuda_kernels"]
        assert math.isfinite(row["max_absolute_error"]) and row["max_absolute_error"] <= row["atol"] == 0.002
        if backend == "efficient":
            assert any("fmha_cutlass" in k and "sm75" in k for k in row["cuda_kernels"])
        observations[case] = {"backend": backend, "finite": True, "reference_matches": True,
            "max_absolute_error": row["max_absolute_error"], "cuda_kernel_count": len(row["cuda_kernels"])}
    assert summary["attention_dispatch"][name] == {case: {"status": "passed", "backend": row["backend"]}
        for case, row in observations.items()}
    assert all(math.isfinite(row["max_absolute_error"]) and row["max_absolute_error"] <= probe["nf4"]["atol"] == 0.01
        for row in probe["nf4"]["operations"])
    assert "sm_75" in probe["compiled_architectures"]
    assert 0 < probe["peak_allocated_bytes"] <= probe["peak_reserved_bytes"] < probe["total_memory"]
    assert probe["post_probe_free_bytes"] > 1.5 * 2**30
    devices[name] = {"uuid": physical["uuid"], "capability": probe["capability"],
        "torch_version": probe["torch_version"], "torch_cuda_build": probe["torch_cuda_build"],
        "driver_version": physical["driver_version"], "nvidia_reported_total_bytes": physical["total_bytes"],
        "torch_total_bytes": probe["total_memory"], "peak_allocated_bytes": probe["peak_allocated_bytes"],
        "peak_reserved_bytes": probe["peak_reserved_bytes"], "post_probe_free_bytes": probe["post_probe_free_bytes"],
        "attention": observations, "nf4": probe["nf4"], "command_seconds": command["elapsed_seconds"]}

text = "".join("".join(o.get("text", [])) for c in code for o in c["outputs"])
assert re.findall(r"Result ZIP SHA-256: ([0-9a-f]{64})", text) == [before["preflight-results.zip"]["sha256"]]
run_text = "".join("".join(o.get("text", [])) for o in notebook["cells"][3]["outputs"])
assert json.JSONDecoder().raw_decode(run_text[run_text.index("{"):])[0] == summary
assert 0 < summary["observed_controller_wall_seconds"] < report["controller_limit_seconds"] == 360
assert summary["observed_gpu_seconds_lower_bound"] == 2 * summary["observed_controller_wall_seconds"]
assert summary["conditional_allocation_upper_bound_seconds"] == 1080
assert commands["device_0"]["ended_utc"] <= commands["device_1"]["started_utc"]

databases = {}
for name in ["filesystem.sqlite", "filesystem-backup.sqlite"]:
    copied = OUTPUT / ("reopened-" + name)
    if copied.exists():
        assert copied.read_bytes() == exported[name]
    else:
        copied.write_bytes(exported[name])
    with closing(sqlite3.connect(copied.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
        assert db.execute("SELECT value FROM probe").fetchall() == [(7,)]
        try:
            db.execute("INSERT INTO probe VALUES (8)")
        except sqlite3.OperationalError as exc:
            assert "readonly" in str(exc).lower()
        else:
            raise AssertionError("Read-only copy accepted a write")
    assert copied.read_bytes() == exported[name]
    databases[name] = {"sha256": digest(copied.read_bytes()), "integrity": "ok", "rows": [[7]],
                       "read_only_enforced": True, "copy_unchanged": True}
assert databases["filesystem-backup.sqlite"]["sha256"] == report["stages"]["filesystem_backup"]["result"]["backup_sha256"]
assert before == {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in originals}
review = {"review_status": "Actual standalone T4 library diagnostics accepted; model/resource acceptance remains open",
    "artifacts": before, "nbformat_valid": True, "first_six_cell_sources_match": True,
    "trailing_cell_empty_and_unexecuted": True, "executed_code_counts": [1, 2, 3], "notebook_error_outputs": [],
    "build_commit": expected["build_commit"], "scientific_baseline_commit": expected["scientific_baseline_commit"],
    "program_sha256": expected["program_sha256"], "operations_sha256": expected["operations_sha256"],
    "zip_members": len(members), "zip_expanded_bytes": 268136, "zip_crc": "passed", "receipt_matches_zip": True,
    "wheel_files_independently_verified": len(snapshot["files"]), "host_candidate_differences": len(host["candidate_differences"]),
    "stages_passed": 6, "commands_passed": len(commands), "commands": commands, "devices": devices,
    "attention_cases_passed": sum(len(d["attention"]) for d in devices.values()),
    "nf4_matmuls_passed": sum(len(d["nf4"]["operations"]) for d in devices.values()),
    "sqlite_off_host": databases, "summary": summary, "model_generations": 0,
    "provider_stop_user_reported": True, "provider_duration_seconds": None, "provider_release_utc": None,
    "provider_statement": "User reports the GPU session is stopped and the run was fast; exact allocation duration was not supplied. No rerun requested.",
    "conditional_allocation_bound_verified": False, "original_artifacts_unchanged": True,
    "acceptance_scope": "R8 small-operator portion on matching host Torch and private verified bitsandbytes wheel; not a full model lock or T02 smoke."}
(OUTPUT / "validation.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"review_status": review["review_status"], "attention_cases_passed": review["attention_cases_passed"],
    "nf4_matmuls_passed": review["nf4_matmuls_passed"], "commands_passed": review["commands_passed"],
    "zip_members": len(members), "sqlite_copies_verified": 2, "observed_controller_wall_seconds": summary["observed_controller_wall_seconds"],
    "provider_stop_user_reported": True, "provider_duration_seconds": None}, indent=2))
