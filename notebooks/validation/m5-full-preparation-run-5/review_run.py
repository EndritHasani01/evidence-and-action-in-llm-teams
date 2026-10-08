"""Read-only review of the supplied run-5 continuation; never execute its cells."""

import ast
from contextlib import closing
from datetime import datetime
import hashlib
import inspect
import json
from pathlib import Path, PurePosixPath
import re
import sqlite3
import stat
import sys
import zipfile

import nbformat

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts import m5_kaggle_preflight as helper
from scripts.m5_kaggle_continue import continue_preflight


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source(cell):
    return "".join(cell.get("source", []))


def constants(program):
    result = {}
    for node in ast.parse(program).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        value = node.value
        if isinstance(value, ast.Call) and ast.unparse(value.func) == "json.loads":
            result[node.targets[0].id] = json.loads(ast.literal_eval(value.args[0]))
        else:
            try:
                result[node.targets[0].id] = ast.literal_eval(value)
            except (ValueError, TypeError):
                pass
    return result


originals = [ROOT / "notebooks/run/5" / name for name in
             ["notebook-exec.ipynb", "preflight-results.zip"]]
before = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
          for p in originals}
notebook = json.loads(originals[0].read_text(encoding="utf-8"))
nbformat.validate(nbformat.from_dict(notebook))
for cell_record in notebook["cells"]:
    if cell_record["cell_type"] == "code":
        ast.parse(source(cell_record))
delivered = json.loads((ROOT / "notebooks/recovery_m5_kaggle_preflight_v3.ipynb")
                       .read_text(encoding="utf-8"))
assert [source(c) for c in notebook["cells"][:6]] == [source(c) for c in delivered["cells"]]
assert len(notebook["cells"]) == 8 and source(notebook["cells"][7]) == ""
assert notebook["cells"][7].get("execution_count") is None
assert not notebook["cells"][7].get("outputs")
assert not any(o.get("output_type") == "error" for c in notebook["cells"] for o in c.get("outputs", []))
assert [c["execution_count"] for c in notebook["cells"] if c.get("execution_count") is not None] == [2, 3, 4, 5]
cell = source(notebook["cells"][6])
assert cell.encode("utf-8") == (ROOT / "notebooks/recovery_m5_kaggle_continue_run4.py").read_bytes()
binding = constants(cell)
program = binding["CONTINUATION_PROGRAM"]
delivery = json.loads((ROOT / "notebooks/validation/m5-probe-output-repair/cell-delivery.json")
                      .read_text(encoding="utf-8"))
assert digest(program.encode()) == delivery["program_sha256"]
assert program == "\n\n".join(inspect.getsource(f) for f in
                             [helper.installed_probe_script, helper.installed_provenance, continue_preflight])
setup = constants(source(notebook["cells"][1]))
expected = setup["EXPECTED"]
assert digest(setup["PREFLIGHT_PROGRAM"].encode()) == expected["helper_sha256"]
assert digest(setup["CANDIDATE_LOCK"].encode()) == expected["candidate_lock_sha256"]

with zipfile.ZipFile(originals[1]) as archive:
    members = archive.infolist()
    assert len(members) == 35 and sum(m.file_size for m in members) == 139386
    assert len({m.filename.casefold() for m in members}) == len(members)
    assert archive.testzip() is None
    exported = {}
    for member in members:
        name = PurePosixPath(member.filename)
        assert member.orig_filename == member.filename and not member.is_dir()
        assert not name.is_absolute() and not {".", ".."}.intersection(name.parts)
        assert "\\" not in member.filename and ":" not in member.filename
        assert not stat.S_ISLNK(member.external_attr >> 16)
        assert name.suffix in {".json", ".txt", ".lock", ".sqlite"}
        exported[member.filename] = archive.read(member)
    for name, data in exported.items():
        path = OUTPUT / "export" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_bytes() == data
        else:
            path.write_bytes(data)

read_json = lambda name: json.loads(exported[name])
report, summary = read_json("continuation-report.json"), read_json("summary.json")
assert report["summary"] == summary
assert summary["continuation_checks_passed"] and summary["tests_passed"] == 97
assert summary["root_blocker"] is None and summary["model_generations"] == 0
assert summary["model_smoke_ready"] is False
assert all(summary[k] is None for k in
           ["gpu_native_diagnostics", "model_smoke", "provider_assignment_utc", "provider_release_utc"])
assert not report["process_cleanup_unconfirmed"] and "export_error" not in report
assert all(s["status"] == "passed" for s in report["stages"].values())
assert read_json("expected-source-manifest.json") == expected
with zipfile.ZipFile(ROOT / "notebooks/run/4/preflight-results.zip") as previous:
    assert exported["prior-preflight-report.json"] == previous.read("preflight-report.json")
    assert exported["expected-source-manifest.json"] == previous.read("expected-source-manifest.json")
assert digest(exported["prior-preflight-report.json"]) == report["prior_report_sha256"]
prior = read_json("prior-preflight-report.json")
assert report["previous_directory"] == prior["output_directory"]
assert report["stages"]["source_recheck"]["verified_members"] == len(expected["members"]) == 143
versions = {p["name"]: p["version"] for p in expected["candidate_wheels"]}
assert versions == prior["stages"]["environment"]["result"]["versions"] and len(versions) == 88
probe = read_json("installed-probe-result.json")
assert probe == read_json("installed-provenance.json")
assert probe["versions"] == versions
assert probe["verified_module_hashes"] == {n: p["sha256"] for n, p in expected["members"].items()
                                          if n.startswith("recovery/") and n.endswith(".py")}
assert len(probe["verified_module_hashes"]) == 28
assert probe["qwen_text_class"] == "Qwen3_5ForCausalLM" and probe["torch_cuda_build"] == "12.8"
assert probe["gpu_native_diagnostics"] is None and probe["model_generations"] == 0
assert probe["executable"] == probe["prefix"] + "/bin/python"
assert probe["module_root"] == probe["prefix"] + "/lib/python3.13/site-packages/recovery"
assert all("site-packages" not in p or p.startswith(probe["prefix"] + "/") for p in probe["sys_path"])
probe_command = read_json("logs/installed-probe.json")
machine_path = str(PurePosixPath(probe_command["args"][2]).with_name("installed-probe-result.json"))
assert exported["installed-probe-program.txt"].decode() == helper.installed_probe_script(expected, versions, PurePosixPath(machine_path))
normal = lambda name: re.sub(r"[-_.]+", "-", name).lower()
listed = {normal(p["name"]): p["version"] for p in read_json("installed-packages.json")}
assert len(listed) == 90
assert listed == versions | {"pip": "26.2.1", "evidence-and-action-in-llm-teams": "0.1.0"}
assert read_json("installed-packages.json") == read_json("logs/pip-list.stdout.txt")
assert exported["installed-freeze.txt"] == exported["logs/pip-freeze.stdout.txt"]
freeze_lines = exported["installed-freeze.txt"].decode().splitlines()
assert {normal(n): v for n, v in (line.split("==") for line in freeze_lines if "==" in line)} == versions | {"pip": "26.2.1"}
assert len([line for line in freeze_lines if " @ " in line]) == 1
project_url = "evidence-and-action-in-llm-teams @ file://" + prior["scratch_directory"] + "/built/evidence_and_action_in_llm_teams-0.1.0-py3-none-any.whl#sha256="
assert any(re.fullmatch(re.escape(project_url) + r"[0-9a-f]{64}", line) for line in freeze_lines)
assert exported["logs/pip-check.stdout.txt"].strip() == b"No broken requirements found."

commands = {PurePosixPath(n).stem: read_json(n) for n in exported if n.startswith("logs/") and n.endswith(".json")}
assert set(commands) == {"pip-check", "installed-probe", "pip-list", "pip-freeze",
                         "focused-checks", "native-9b", "native-4b", "native-capacity"}
checks = {}
for name, record in commands.items():
    assert record["status"] == "passed" and record["exit_code"] == 0 and record["leader_exited"]
    assert record["tree_confirmation"] == "exited" and record["elapsed_seconds"] < record["timeout_seconds"]
    assert record["args"][0] == probe["executable"]
    assert record["stdout"] in exported and record["stderr"] in exported
for name, count in [("focused-checks", 81), ("native-9b", 4), ("native-4b", 4), ("native-capacity", 8)]:
    record = commands[name]
    stderr = exported[record["stderr"]].decode()
    matches = re.findall(r"^Ran (\d+) tests in ([\d.]+)s$", stderr, re.MULTILINE)
    assert len(matches) == 1 and int(matches[0][0]) == count and re.search(r"^OK\s*$", stderr, re.MULTILINE)
    assert not re.search(r"^FAILED|^ERROR:|^FAIL:|skipped=|\.\.\. skipped", stderr, re.MULTILINE)
    stage = report["stages"][name.replace("-", "_")]["result"]
    assert stage["tests"] == count and stage["skipped"] == 0 and stage["reported_seconds"] == float(matches[0][1])
    assert record["cwd"] == prior["scratch_directory"] + "/source"
    checks[name] = {"tests": count, "skipped": 0, "reported_seconds": float(matches[0][1]),
                    "command_seconds": record["elapsed_seconds"]}
stream = "".join("".join(o.get("text", [])) for o in notebook["cells"][6]["outputs"])
assert "Result ZIP SHA-256: " + before["preflight-results.zip"]["sha256"] in stream
assert json.JSONDecoder().raw_decode(stream[stream.index("{"):])[0] == summary
assert abs((datetime.fromisoformat(report["ended_utc"]) - datetime.fromisoformat(report["started_utc"])).total_seconds()
           - summary["observed_cpu_wall_seconds"]) < 0.1
assert summary["observed_cpu_wall_seconds"] < report["cpu_limit_seconds"] == 900

databases = {}
for name in ["filesystem.sqlite", "filesystem-backup.sqlite"]:
    copy = OUTPUT / ("reopened-" + name)
    if copy.exists():
        assert copy.read_bytes() == exported[name]
    else:
        copy.write_bytes(exported[name])
    with closing(sqlite3.connect(copy.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        db.execute("PRAGMA query_only=ON")
        assert db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
        assert db.execute("SELECT value FROM probe").fetchall() == [(7,)]
        try:
            db.execute("INSERT INTO probe VALUES (8)")
        except sqlite3.OperationalError as exc:
            assert "readonly" in str(exc).lower()
        else:
            raise AssertionError("Read-only copy accepted a write")
    assert copy.read_bytes() == exported[name]
    databases[name] = {"sha256": digest(copy.read_bytes()), "integrity": "ok", "rows": [[7]],
                       "read_only_enforced": True, "copy_unchanged": True}
assert databases["filesystem-backup.sqlite"]["sha256"] == report["stages"]["filesystem_backup"]["result"]["backup_sha256"]
assert before == {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in originals}
review = {
    "review_status": "CPU continuation accepted; actual GPU/model gates remain unknown",
    "artifacts": before, "nbformat_valid": True, "code_cell_syntax_valid": True,
    "notebook_first_six_sources_match_v3": True,
    "continuation_cell_exact_bytes_match": True, "continuation_source_checkpoint": binding["CONTINUATION_BUILD_COMMIT"],
    "embedded_program_matches_three_reviewed_functions": True, "executed_code_counts": [2, 3, 4, 5],
    "notebook_error_outputs": [], "zip_members": len(members), "zip_expanded_bytes": 139386,
    "zip_crc": "passed", "receipt_matches_zip": True, "prior_run4_report_and_manifest_exact_bytes_match": True,
    "prior_report_sha256": report["prior_report_sha256"], "source_rechecked_members": 143,
    "candidate_packages_verified": 88, "total_installed_distributions": 90, "installed_module_hashes_verified": 28,
    "machine_provenance_file_and_program_verified": True, "checks": checks, "commands": commands,
    "sqlite_off_host": databases, "summary": summary, "original_artifacts_unchanged": True,
    "source_baseline_commit": expected["source_baseline_commit"], "v3_build_commit": expected["build_commit"],
    "warnings": {"sitecustomize_missing_wrapt": "Retained; hook origin unknown; commands/tests passed",
                 "transformers_docstrings": "Retained on stdout; machine JSON file passed independently",
                 "capacity_overflow": "Expected deliberate overflow-guard warning; native tests passed"},
    "acceptance_scope": "Run 4 installation/source/cleanup plus run 5 CPU provenance/97 checks/export; no GPU/model admission",
    "provider_release_utc": None,
}
(OUTPUT / "validation.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"review_status": review["review_status"], "tests_passed": 97, "skipped": 0,
                  "commands_passed": len(commands), "zip_members": len(members), "sqlite_copies_verified": 2}, indent=2))
