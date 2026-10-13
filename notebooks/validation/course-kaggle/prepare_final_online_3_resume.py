"""Prepare the reviewed incident continuation offline; never execute an attempt.

The notebook keeps its ordinary exact-source checks. This tool preserves the
original source, reports and all worker bytes, and supplies a matching corrected
resume payload. It accepts only the submitted final-online-3 archive.
"""

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
ORIGINAL_SHA = "10eb1fc4015ff7a6cef31216be9890a405e424d57982974d48bfae62d9e61c43"
ORIGINAL_COMMIT = "075d10737c5f06a5a0de1122dac0e8236e8aac0a"
ALLOWED_CHANGES = {"SOURCE_COMMIT.txt", "recovery/inference.py", "recovery/attempts.py",
    "scripts/m5_course_smoke.py", "scripts/m5_course_smoke_assets.py", "scripts/m5_kaggle_preflight.py",
    "scripts/course_kaggle_bootstrap.py", "tests/generation_checks.py"}
MISSING_IDS = ["course-hardware/envelope/device-0", "course-hardware/envelope/device-1", "smoke/course-m5/24"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_incident(bundle):
    from recovery.storage import WorkerStore
    config = json.loads((bundle/"operator-config.json").read_bytes())
    if ((bundle/"run.json").exists() or list(bundle.glob("development/worker-*.sqlite")) or
            list(bundle.glob("main/worker-*.sqlite")) or config["budget"]["prior_smoke_attempts"] != 1 or
            config["smoke_attempt_limit"] != 25 or config["smoke_attempt_allowance"] != "final-online-2/one-time-repair"):
        raise ValueError("only the original preparation, prior failure and 25-attempt allowance are compatible")
    report = json.loads((bundle/"hardware/report.json").read_bytes())
    if report.get("root_blocker") is not None or report["smoke"]["stop_reason"] != (
            "TypeError: RenderedRequest.__init__() got an unexpected keyword argument 'system'"):
        raise ValueError("the reviewed pre-attempt constructor failure is required")
    count = 0
    bindings = []
    for index in range(2):
        store = WorkerStore(bundle/f"hardware/worker-{index}.sqlite", readonly=True)
        try:
            if store.connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("worker integrity failure")
            calls = [dict(c) for c in store.connection.execute("SELECT * FROM calls")]
            attempts = [dict(a) for a in store.connection.execute("SELECT * FROM attempts")]
            expected = {f"smoke/course-m5/{i:02d}" for i in (range(1,20) if index == 0 else range(20,22))}
            if ({c["call_id"] for c in calls} != expected or len(attempts) != len(expected) or
                    any(c["status"] != "completed" or not c["raw_json"] or not c["validation_json"] for c in calls) or
                    any(a["status"] != "completed" for a in attempts) or
                    store.connection.execute("SELECT 1 FROM allocations WHERE stopped_at IS NULL").fetchone() or
                    store.connection.execute("SELECT 1 FROM provider_processes WHERE stopped_at IS NULL").fetchone()):
                raise ValueError("exactly 21 completed quiescent calls, with no additional attempts, are required")
            count += len(attempts)
            bindings.append(store.run_inputs)
        finally:
            store.close()
    return config, bindings, count


def prepare(packet, incident, output):
    from recovery.inference import TokenizerFactory
    from recovery.prompts import COURSE_LIMITS
    from scripts.m5_course_smoke import CANDIDATE, check_hardware_plan, hardware_plan, read
    from scripts.m5_course_smoke_assets import source_identity
    if output.exists():
        raise FileExistsError(output)
    if digest(incident) != ORIGINAL_SHA:
        raise ValueError("this repair accepts only the exact submitted final-online-3 payload")
    manifest = json.loads((packet/"source-manifest.json").read_bytes())
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as directory:
        bundle = Path(directory)/"bundle"
        with zipfile.ZipFile(incident) as archive:
            if archive.testzip() is not None or len(set(archive.namelist())) != len(archive.infolist()):
                raise ValueError("invalid original export")
            for name in archive.namelist():
                path = PurePosixPath(name)
                if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                    raise ValueError("unsafe original export member")
            archive.extractall(bundle)
        source = bundle/"source"
        old = json.loads((source/"source-manifest.json").read_bytes())
        source_identity(source, old)
        config, bindings, count = validate_incident(bundle)
        if old["source_baseline_commit"] != ORIGINAL_COMMIT:
            raise ValueError("original incident source differs")
        for key in ("candidate_wheels", "candidate_lock_sha256", "build_tools"):
            if old[key] != manifest[key]:
                raise ValueError("reviewed native dependency pins differ: "+key)
        with zipfile.ZipFile(packet/manifest["payload_filename"]) as archive:
            if digest(packet/manifest["payload_filename"]) != manifest["archive_sha256"]:
                raise ValueError("corrected packet archive differs")
            current = {name:archive.read(name) for name in manifest["members"]}
        changed = {name for name in set(old["members"]) | set(current)
                   if name not in old["members"] or name not in current or
                   hashlib.sha256(current[name]).hexdigest() != old["members"][name]["sha256"]}
        if not changed <= ALLOWED_CHANGES or set(old["members"]) - set(current):
            raise ValueError("unreviewed source changes: "+repr(sorted(changed-ALLOWED_CHANGES)))
        # Prove the entire ordinary inference module is identical in syntax;
        # only the diagnostic branch's one EOS assignment may differ.
        tree = ast.parse((source/"recovery/inference.py").read_bytes())
        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == "force_output_reserve":
                for statement in node.body:
                    if (isinstance(statement, ast.Assign) and isinstance(statement.targets[0], ast.Attribute)
                            and statement.targets[0].attr == "eos_token_id"):
                        statement.value = ast.List(elts=[], ctx=ast.Load())
        if ast.dump(tree) != ast.dump(ast.parse(current["recovery/inference.py"])):
            raise ValueError("ordinary inference changed beyond the diagnostic EOS correction")
        before = {p.relative_to(bundle).as_posix():digest(p) for p in (bundle/"hardware").glob("*.sqlite")}
        repair = bundle/"repair"; repair.mkdir()
        shutil.move(source, repair/"original-source")
        source.mkdir()
        for name, raw in current.items():
            path = source/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
        shutil.copyfile(packet/"source-manifest.json",source/"source-manifest.json")
        source_identity(source, manifest)
        tokenizer = TokenizerFactory(CANDIDATE,str(source/"metadata/4B"),COURSE_LIMITS)()
        requests = read(source/"notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")
        contract = check_hardware_plan(source, requests, tokenizer)
        rows = hardware_plan(requests,tokenizer)
        previous_rows = json.loads((bundle/"hardware/executed-plan.json").read_bytes())["rows"]
        expected_rows = json.loads(json.dumps(previous_rows))
        for row in expected_rows:
            if row.get("hardware_diagnostic"):
                row["rendered"].pop("system")
        if rows != expected_rows or any(binding["settings"] != requests["settings"] for binding in bindings):
            raise ValueError("saved requests/settings differ beyond the two unattempted diagnostic schemas")
        for name in ("hardware/report.json", "hardware/executed-plan.json", "hardware-gate.json", "last-action.json",
                     "analysis-receipt.json", "automatic-run.json", "asset-receipt.json"):
            path = bundle/name
            if path.exists():
                target = repair/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.move(path,target)
        # Absence of a corrected hardware report accurately means the repaired
        # stage has not run. Existing hardware workers force in-place resumption.
        (bundle/"hardware/executed-plan.json").write_text(json.dumps(dict(rows=rows,
            note="Reviewed preparation-only schema repair; original plan retained under repair")),encoding="utf-8")
        after = {p.relative_to(bundle).as_posix():digest(p) for p in (bundle/"hardware").glob("*.sqlite")}
        if before != after:
            raise ValueError("original worker bytes changed")
        receipt = dict(incident="final-online-3", authorization="User requested full repair after the reviewed 13 October proposal",
            original_payload_sha256=ORIGINAL_SHA, original_source_commit=ORIGINAL_COMMIT,
            corrected_source_commit=manifest["source_baseline_commit"], source_changes=sorted(changed),
            preserved_source="repair/original-source", preserved_report="repair/hardware/report.json",
            ordinary_inference_ast_unchanged=True, ordinary_requests_unchanged=True,
            prior_smoke_attempts=1, preserved_current_attempts=count, cumulative_attempts=22,
            attempt_limit=25, pending_call_ids=MISSING_IDS, worker_hashes_unchanged=after,
            weights_loaded=False, gpu_calls=0, new_attempts=0, plan_contract=contract)
        (repair/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        resume = output/"course-resume.payload"
        with zipfile.ZipFile(resume,"x",zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(bundle.rglob("*")):
                if path.is_file(): archive.write(path,path.relative_to(bundle).as_posix())
        dataset = output/"course-kaggle-dataset.zip"
        with zipfile.ZipFile(dataset,"x",zipfile.ZIP_DEFLATED) as archive:
            for name in (manifest["payload_filename"],"source-manifest.json"):
                archive.write(packet/name,name,compress_type=zipfile.ZIP_STORED)
            archive.write(resume,resume.name,compress_type=zipfile.ZIP_STORED)
        for name in ("course_kaggle.ipynb","START_HERE.md","source-manifest.json",manifest["payload_filename"]):
            shutil.copyfile(packet/name,output/name)
        summary = json.loads((packet/"package-summary.json").read_bytes())
        summary.update(dataset=str(dataset),dataset_bytes=dataset.stat().st_size,dataset_sha256=digest(dataset),
            dataset_input_files=3, repair_resume_embedded=True, cumulative_smoke_attempts=22,
            remaining_smoke_attempts=3, preserved_native_outcomes=21, repair_receipt=receipt)
        (output/"package-summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet",type=Path,required=True)
    parser.add_argument("--incident",type=Path,default=ROOT/"notebooks/run/final-online-3/course-resume.payload")
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.packet.resolve(),args.incident.resolve(),args.output.resolve()),indent=2))
