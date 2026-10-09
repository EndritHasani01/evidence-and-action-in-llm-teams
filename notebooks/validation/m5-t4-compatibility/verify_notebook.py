"""Execute shipped cells in Jupyter; unavailable Linux/GPU outcomes stay controlled."""

import ast
import argparse
import asyncio
from contextlib import closing
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import stat
import subprocess
import sys
import uuid
import zipfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts import m5_kaggle_preflight as operations


def constants(program):
    result = {}
    for node in ast.parse(program).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        try:
            value = node.value
            if isinstance(value, ast.Call) and ast.unparse(value.func) == "json.loads":
                result[node.targets[0].id] = json.loads(ast.literal_eval(value.args[0]))
            else:
                result[node.targets[0].id] = ast.literal_eval(value)
        except (ValueError, TypeError):
            pass
    return result


def main(evidence):
    evidence.mkdir(exist_ok=False)
    original = ROOT / "notebooks/recovery_m5_kaggle_t4_compatibility.ipynb"
    shipped = nbformat.read(original, as_version=4)
    nbformat.validate(shipped)
    binding = constants(shipped.cells[1].source)
    expected = binding["EXPECTED"]
    for key, source, path in [
        ("program_sha256", "COMPATIBILITY_PROGRAM", "scripts/m5_t4_compatibility.py"),
        ("operations_sha256", "OPERATIONS_PROGRAM", "scripts/m5_kaggle_preflight.py")]:
        assert hashlib.sha256(binding[source].encode()).hexdigest() == expected[key]
        committed = subprocess.check_output(["git", "show", expected["build_commit"] + ":" + path], cwd=ROOT)
        assert committed.decode().replace("\r\n", "\n") == binding[source]
    for cell in shipped.cells:
        if cell.cell_type == "code":
            ast.parse(cell.source)
            assert cell.execution_count is None and not cell.outputs
    scratch = ROOT / "build" / ("m5-t4-kernel-" + uuid.uuid4().hex)
    scratch.mkdir(parents=True, exist_ok=False)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = {"status": "passed", "environment": {"python": sys.version, "platform": sys.platform},
              "notebook_sha256": operations.sha256_file(original), "build_commit": expected["build_commit"],
              "program_sha256": expected["program_sha256"], "operations_sha256": expected["operations_sha256"],
              "scope": "Actual local Jupyter/file/wheel/SQLite/export checks; complete Linux/GPU receipts are controlled.",
              "actual_t4_execution": False, "full_candidate_gpu_acceptance": None, "model_generations": 0, "cases": {}}
    real_wheel = ROOT / "build/m5-t4-compatibility-input" / expected["bitsandbytes_wheel"]["filename"]
    assert real_wheel.stat().st_size == expected["bitsandbytes_wheel"]["bytes"]
    assert operations.sha256_file(real_wheel) == expected["bitsandbytes_wheel"]["sha256"]
    controls = """# LOCAL VALIDATION ONLY: Linux/T4/download outcomes below are controlled.
import shutil
from types import SimpleNamespace
from tests.test_t4_compatibility import controlled_probe,IDENTITIES,INVENTORY
real_sys=compatibility_namespace['sys']
real_platform=compatibility_namespace['platform']
real_metadata=compatibility_namespace['metadata']
compatibility_namespace['sys']=SimpleNamespace(**dict(vars(real_sys),version_info=(3,13,0)))
compatibility_namespace['platform']=SimpleNamespace(**dict(vars(real_platform),system=lambda:'Linux',machine=lambda:'x86_64'))
compatibility_namespace['metadata']=SimpleNamespace(**dict(vars(real_metadata),version=lambda name: '2.11.0+cu128' if name=='torch' else real_metadata.version(name)))
controlled_calls=[]
def local_command(output,name,args,**kwargs):
    controlled_calls.append(name)
    logs=output/'logs'
    logs.mkdir(exist_ok=True)
    stdout,stderr=logs/(name+'.stdout.txt'),logs/(name+'.stderr.txt')
    stdout.write_text('',encoding='utf-8')
    stderr.write_text('',encoding='utf-8')
    record={'scope':'Controlled command result, not an actual Linux/GPU process',
        'name':name,'args':list(map(str,args)),'stdout':stdout.relative_to(output).as_posix(),
        'stderr':stderr.relative_to(output).as_posix(),'status':'passed','exit_code':0,
        'leader_exited':True,'tree_confirmation':'exited'}
    if name=='gpu-inventory':
        stdout.write_text(INVENTORY,encoding='utf-8')
    elif name=='download-bitsandbytes-wheel':
        wheel=EXPECTED['bitsandbytes_wheel']
        shutil.copyfile(Path(LOCAL_VERIFIED_WHEEL),kwargs['cwd']/wheel['filename'])
        stdout.write_text(json.dumps(dict(wheel,verified=True)),encoding='utf-8')
    elif name.startswith('device_'):
        assert '-I' in args and '-B' in args
        assert kwargs['env']['CUDA_VISIBLE_DEVICES']==IDENTITIES[int(name[-1])]
        assert 'BNB_CUDA_VERSION' not in kwargs['env']
        package_root=Path(args[args.index('--package-root')+1])
        machine=Path(args[args.index('--output')+1])
        operations_namespace['save_json'](machine,controlled_probe(kwargs['env']['CUDA_VISIBLE_DEVICES'],package_root))
        stdout.write_text('[ERROR] controlled import diagnostic; machine JSON is separate\\n',encoding='utf-8')
    else:
        raise AssertionError('Unexpected command: '+name)
    operations_namespace['save_json'](logs/(name+'.json'),record)
    return record
operations_namespace['command']=local_command
"""
    for name in ["actual-host-refusal", "controlled-complete"]:
        case = evidence / name
        case.mkdir(exist_ok=False)
        document = copy.deepcopy(shipped)
        if name == "controlled-complete":
            document.cells.insert(2, nbformat.v4.new_code_cell(
                "LOCAL_VERIFIED_WHEEL=" + repr(str(real_wheel)) + "\n" + controls))
            document.cells.append(nbformat.v4.new_code_cell(shipped.cells[3].source + "\nassert len(controlled_calls)==4"))
        overrides = {"M5_COMPAT_OUTPUT_ROOT": str(case / "output"), "M5_COMPAT_SCRATCH_ROOT": str(scratch / name)}
        prior = {key: os.environ.get(key) for key in overrides}
        try:
            os.environ.update(overrides)
            executed = NotebookClient(document, timeout=180, kernel_name="python3",
                resources={"metadata": {"path": str(ROOT)}}).execute()
        finally:
            for key, value in prior.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        nbformat.write(executed, case / "executed.ipynb")
        nbformat.validate(executed)
        original_cells = [c for c in executed.cells if c.id in {v.id for v in shipped.cells}]
        assert [c.source for c in original_cells] == [c.source for c in shipped.cells]
        code = [c for c in executed.cells if c.cell_type == "code"]
        counts = list(range(1, 6 if name == "controlled-complete" else 4))
        assert [c.execution_count for c in code] == counts
        assert not any(o.output_type == "error" for c in code for o in c.outputs)
        archives = list((case / "output").glob("*/preflight-results.zip"))
        assert len(archives) == 1
        archive_path = archives[0]
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None
            members = archive.infolist()
            assert len({m.filename.casefold() for m in members}) == len(members)
            for member in members:
                path = PurePosixPath(member.filename)
                assert member.orig_filename == member.filename and not member.is_dir()
                assert not path.is_absolute() and not {".", ".."}.intersection(path.parts)
                assert "\\" not in member.filename and ":" not in member.filename
                assert not stat.S_ISLNK(member.external_attr >> 16)
                assert path.suffix in {".json", ".txt", ".sqlite"}
            summary = json.loads(archive.read("summary.json"))
            report = json.loads(archive.read("compatibility-report.json"))
            assert summary == report["summary"]
            assert summary["model_generations"] == 0 and summary["model_smoke_ready"] is False
            assert all(summary[k] is None for k in ["full_candidate_gpu_acceptance", "native_qwen_recurrent_acceptance",
                "full_envelope_memory_acceptance", "provider_assignment_utc", "provider_release_utc"])
            assert summary["conditional_allocation_upper_bound_seconds"] == 1080
            assert report["stages"]["filesystem_backup"]["status"] == "passed"
            if name == "controlled-complete":
                assert summary["library_checks_completed"] is True and summary["root_blocker"] is None
                assert report["stages"]["wheel_staging"]["result"]["verified_files"] == 85
                assert len([m for m in members if m.filename.startswith("logs/") and m.filename.endswith(".json")]) == 4
                assert json.loads(archive.read("extracted-wheel.json"))["wheel"] == expected["bitsandbytes_wheel"]
            else:
                assert summary["library_checks_completed"] is False
                assert "diagnostic_requires_linux_x86_64_python313" in summary["root_blocker"]
                assert report["stages"]["wheel_staging"]["status"] == "blocked"
                assert not any(m.filename.startswith("logs/") for m in members)
            snapshots = {}
            for member in ["filesystem.sqlite", "filesystem-backup.sqlite"]:
                copied = case / ("reopened-" + member)
                copied.write_bytes(archive.read(member))
                with closing(sqlite3.connect(copied.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)) as connection:
                    assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
                    assert connection.execute("SELECT value FROM probe").fetchall() == [(7,)]
                    try:
                        connection.execute("INSERT INTO probe VALUES (8)")
                    except sqlite3.OperationalError as exc:
                        assert "readonly" in str(exc).lower()
                    else:
                        raise AssertionError("Read-only snapshot accepted a write")
                snapshots[member] = operations.sha256_file(copied)
        output_text = "".join(o.get("text", "") for c in code for o in c.outputs)
        receipts = re.findall(r"Result ZIP SHA-256: ([0-9a-f]{64})", output_text)
        assert receipts == [operations.sha256_file(archive_path)]
        if name == "controlled-complete":
            assert "Already executed in this kernel" in output_text
        result["cases"][name] = {"executed": True, "execution_counts": counts, "shipped_cell_sources_unchanged": True,
            "library_outcome_scope": "Controlled Linux/T4 receipts" if name == "controlled-complete" else "Actual host refused",
            "library_checks_completed": summary["library_checks_completed"], "root_blocker": summary["root_blocker"],
            "zip_path": archive_path.relative_to(ROOT).as_posix(), "zip_sha256": receipts[0], "zip_members": len(members),
            "sqlite_integrity": "ok", "read_only_enforced": True, "reopened_snapshots": snapshots,
            "verified_real_wheel_files": 85 if name == "controlled-complete" else 0, "model_generations": 0}
    assert operations.sha256_file(original) == result["notebook_sha256"]
    operations.save_json(evidence / "validation.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-directory", type=Path, default=OUTPUT / "kernel")
    main(parser.parse_args().evidence_directory.resolve())
