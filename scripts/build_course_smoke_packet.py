"""Committed course CPU preparation and handoff; physical R7 acceptance is M5-T02."""

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

from scripts.build_kaggle_bundle import (BASELINE_COMMIT, SOURCE_ARCHIVE_SHA256,
    archive_manifest, candidate_lock)
from scripts.m5_course_preparation import PAYLOAD, read, memory_review, verify_native_requests
from recovery.tasks import Task

SOURCE_PATHS = ("recovery", "scripts", "tests", "configs", "pyproject.toml", "AGENTS.md", "PROJECT_SPECIFICATION.md",
    "notebooks/validation/course-m5-preparation/inputs",
    "notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json",
    "notebooks/validation/m5-t4-compatibility-run-6/validation.json",
    "notebooks/validation/course-m5-r7",
    "docs/implementation-research/course-m5-r7-capacity-proof.md")


def preparation_review(root):
    """Reuse pinned prerequisite receipts; complete preparation never admits hardware."""
    evidence = root / "notebooks/validation/course-m5-r7"
    proof = read(evidence / "native-tightening-source.json")
    outside = read(evidence / "outside-provenance.json")
    memory = read(evidence / "offline-memory-review.json")
    loading = read(evidence / "loading-review-source.json")
    requests = read(root / "notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")
    # The old receipt hashes checkout text; Git archive can change its line endings.
    # Only this Python source comparison permits LF/CRLF; artifact/request bytes stay exact.
    proof_source = (root/"tests/course_capacity_tightening.py").read_bytes().replace(b"\r\n", b"\n")
    proof_digests = {hashlib.sha256(data).hexdigest() for data in (proof_source, proof_source.replace(b"\n", b"\r\n"))}
    for item in (proof, memory, loading):
        if (item["model"], item["revision"]) != (requests["settings"]["model"], requests["settings"]["revision"]):
            raise ValueError("supplemental candidate identity differs")
    if (json.dumps(proof["limits"], sort_keys=True) != json.dumps(requests["settings"]["protocol_limits"], sort_keys=True)
            or proof["source_capacity_sha256"] != hashlib.sha256((root/"tests/fixtures/course_capacity.json.gz").read_bytes()).hexdigest()
            or proof["tokenizer_sha256"] != read(root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")["metadata"]["files"]["tokenizer.json"]["sha256"]):
        raise ValueError("supplemental input proof provenance differs")
    if (outside["source_pythonpath"] is not False or outside["matching_installed_modules"] != 29
            or outside["report_matches_source"] is not True
            or json.dumps(outside["report"], sort_keys=True) != json.dumps(proof, sort_keys=True)
            or outside["proof_sha256"] not in proof_digests):
        raise ValueError("supplemental installed proof differs")
    rows = proof["accounting"]
    if {row["task"] for row in rows} != {task.value for task in Task} or len(rows) != 5:
        raise ValueError("complete five-family input coverage required")
    for row in rows:
        expected = 7*256*proof["own_tokens_per_physical_token_upper"] + 21*64*proof["prose_tokens_per_counted_token_upper"]
        expected += row["nontext_bytes"] + row["template_wrapper_bytes"]
        if row["input_tokens_upper"] != expected or row["resident_tokens_upper"] != expected+256:
            raise ValueError("complete input accounting differs")
    if (proof["input_tokens_upper"] != max(row["input_tokens_upper"] for row in rows)
            or proof["resident_tokens_upper"] != 110107 or memory["resident_tokens_upper"] != 110107
            or loading["checks"] != 5 or loading["skips"] != 0 or loading["tensor_payload_bytes_read"] != 0):
        raise ValueError("verified capacity/loading evidence differs")
    for item in (memory, loading):
        if (item["complete_live_memory_upper_bound_bytes"] is not None
                or item["actual_headroom_acceptance"] is not None
                or item["preparation_admitted"] is not False or item["weight_staging_permitted"] is not False
                or item["terminal_model_feasibility_failure"] is not False):
            raise ValueError("CPU preparation cannot grant physical-memory admission")
    return dict(status="prepared", preparation_complete=True, complete_input_tokens_upper=proof["input_tokens_upper"],
        complete_resident_tokens_upper=proof["resident_tokens_upper"], physical_memory_acceptance_task="course/M5-T02",
        conditional_tensor_component_sum_bytes=sum(memory["tightened_known_or_conditional_tensor_components"].values()),
        conditional_loading_tensor_allowance_bytes=loading["tensor_storage_loading_allowance_bytes"],
        complete_live_memory_upper_bound_bytes=None, actual_headroom_acceptance=None,
        physical_memory_accepted=False, weight_staging_permitted=False, gpu_admission=False,
        terminal_model_feasibility_failure=False)


def notebook(expected, helper):
    def cell(kind, text, identifier):
        value = dict(cell_type=kind, id=identifier, metadata={}, source=text.splitlines(keepends=True))
        if kind == "code":
            value.update(execution_count=None, outputs=[])
        return value
    instructions = """# Course M5 preparation review — CPU only

Use Accelerator **None** and Internet **Off**. Attach the new course source
payload identified in this notebook; historical source-v2 cannot supply it.
This local packet has not been uploaded or published. Set `COURSE_M5_PAYLOAD`
to the delivered payload path when running locally. On a later approved host,
attach that exact payload as a private input. Run All, download the result ZIP
and executed notebook, and stop the CPU session.

Course M5-T01 preparation is complete after this review passes. Physical R7
memory acceptance belongs to M5-T02 and remains **unaccepted**. This notebook
verifies new source/assets, all 24 prepared inputs, the reused complete input
proof/loading review and a small durable backup/export. It
downloads no packages or weights, starts no inference worker and makes no GPU
call. It grants no smoke/resource/model/freeze admission. Quota, old spending,
provider duration/release and the complete CUDA memory envelope remain unknown.
The 24-call matrix is a cumulative ceiling, including earlier attempts; it
does not grant 24 new calls. Later bounded loading/diagnostics require separate
authorization and resource/host admission. Full memory/headroom acceptance
still precedes pilot admission. Historical `preparation_admitted=False` fields
record the earlier physical-memory gate, independently of preparation completion.
"""
    bootstrap = ("import gzip,hashlib,json,os\nfrom pathlib import Path\n"
        f"EXPECTED=json.loads({json.dumps(expected, sort_keys=True)!r})\n"
        f"HELPER={helper!r}\n"
        "assert hashlib.sha256(HELPER.encode()).hexdigest()==EXPECTED['review_helper_sha256']\n"
        "helpers={'__name__':'course_cpu_review_helper'}\n"
        "exec(compile(HELPER,'m5_kaggle_preflight.py','exec'),helpers)\n"
        "configured=os.environ.get('COURSE_M5_PAYLOAD')\n"
        "if configured:\n    payload=Path(configured).resolve()\n"
        "else:\n"
        "    matches=list(Path('/kaggle/input').rglob(EXPECTED['payload_filename']))\n"
        "    assert len(matches)==1, 'Attach the one exact new course payload'\n"
        "    payload=matches[0].resolve()\n"
        "output=Path(os.environ.get('COURSE_M5_OUTPUT','/kaggle/working/course-m5-cpu-review')).resolve()\n"
        "assert not output.exists(), 'Use a fresh output; preserve previous evidence'\n"
        "output.mkdir(parents=True)\n"
        "source=output/'source'\n"
        "admitted=helpers['admit_source'](payload,source,EXPECTED)\n")
    review = """import sys
sys.path.insert(0,str(source))
from scripts.build_course_smoke_packet import preparation_review
preparation=preparation_review(source)
assert preparation==EXPECTED['preparation']
prepared_root=source/'notebooks/validation/course-m5-preparation/inputs'
prepared=json.loads(gzip.decompress((prepared_root/'smoke-requests.json.gz').read_bytes()))
memory=json.loads((prepared_root/'memory-review.json').read_bytes())
assert prepared['regime']=='course' and len(prepared['requests'])==24
assert not prepared['inference_executable'] and not prepared['preparation_admitted']
assert not memory['preparation_admitted'] and not memory['weight_staging_permitted']
assert memory['complete_live_memory_upper_bound_bytes'] is None
assert memory['envelope']['resident_tokens_upper']==156251
assert prepared['settings']['model']=='Qwen/Qwen3.5-4B'
assert prepared['settings']['generation']['max_new_tokens']==256
assert prepared['settings']['protocol_limits']['prose_tokens']==64
assert prepared['settings']['attention']=='recovery_t4_sdpa'
assert len({r['smoke_call_id'] for r in prepared['requests']})==24
for row in prepared['requests']:
    assert not row['executed'] and row['outcome'] is None
    assert row['settings']==prepared['settings'] and row['origin_call_id'].startswith('dev-')
    assert len(row['tokenized']['input_ids'])==row['input_tokens']
    assert len(row['tokenized']['attention_mask'])==row['input_tokens']
    assert row['resident_tokens_with_reserve']==row['input_tokens']+256<=156251
storage=helpers['sqlite_diagnostic'](output)
report=dict(status='prepared',preparation=preparation,source_verification=admitted,prepared_requests=24,
    historical_memory_review=memory,storage=storage,model_generations=0,pretrained_weights_staged=False,
    provider_quota=None,provider_duration=None,prior_allocation=None,provider_release=None,
    gpu_admission=False,runtime_freeze=False)
helpers['save_json'](output/'report.json',report)
EXPORTED=helpers['export_evidence'](output)
print(json.dumps(dict(status='prepared',physical_memory_accepted=False,**EXPORTED),indent=2))
"""
    export = """from IPython.display import FileLink,display
display(FileLink(EXPORTED['zip_path']))
print('Retain this ZIP and executed notebook. Stop the CPU session. M5-T02 memory/resource/authorization gates remain pending.')
"""
    return dict(nbformat=4, nbformat_minor=5, metadata=dict(kernelspec=dict(
        display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")),
        cells=[cell("markdown", instructions, "course-instructions"),
               cell("code", bootstrap, "course-source"), cell("code", review, "course-review"),
               cell("code", export, "course-export")])


def build(root, tokenizer, prepared, inspection, output):
    if output.exists():
        raise FileExistsError(output)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    if subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", *SOURCE_PATHS], cwd=root).strip():
        raise ValueError("commit current source before creating a course source packet")
    candidate = read(root / "dist/m5-kaggle-source-v2/source-manifest.json")
    if candidate["source_baseline_commit"] != BASELINE_COMMIT or candidate["archive_sha256"] != SOURCE_ARCHIVE_SHA256:
        raise ValueError("reuse only the accepted CPU candidate provenance")
    lock = candidate_lock(candidate["candidate_wheels"])
    if hashlib.sha256(lock.encode()).hexdigest() != candidate["candidate_lock_sha256"]:
        raise ValueError("candidate lock differs from accepted CPU evidence")
    memory = read(prepared / "memory-review.json")
    if memory["preparation_admitted"] is not False or memory["weight_staging_permitted"] is not False:
        raise ValueError("this reviewed packet implements only CPU preparation")
    preparation = preparation_review(root)
    from transformers import AutoTokenizer
    from tests.tokenizer_course_capacity import metadata_support
    native = AutoTokenizer.from_pretrained(tokenizer, local_files_only=True)
    metadata_support(tokenizer, native)
    verify_native_requests(root, native, read(prepared/"smoke-requests.json.gz"))
    expected_memory = memory_review(read(root/"tests/fixtures/course_capacity.json.gz"), read(inspection),
        read(root/"notebooks/validation/m5-t4-compatibility-run-6/validation.json"))
    if memory != expected_memory:
        raise ValueError("prepared memory review differs from original capacity/shape/device evidence")
    code_archive = subprocess.check_output(["git", "archive", "--format=zip", commit, *SOURCE_PATHS], cwd=root)
    members = {}
    with zipfile.ZipFile(io.BytesIO(code_archive)) as archive:
        for entry in archive.infolist():
            if not entry.is_dir():
                members[entry.filename] = archive.read(entry)
    members["SOURCE_COMMIT.txt"] = (commit+"\n").encode()
    for name in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja", "config.json", "model.safetensors.index.json"):
        data = (tokenizer/name).read_bytes()
        expected = read(inspection)["checkpoint_index"] if name == "model.safetensors.index.json" else read(inspection)["metadata"]["files"][name]
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("pinned inspected metadata asset differs: "+name)
        members[f"metadata/4B/{name}"] = data
    canonical_inputs = "notebooks/validation/course-m5-preparation/"
    from recovery.storage import record_json
    for name, path in (("candidate-inspection-accepted.json", inspection),
                       ("inputs/memory-review.json", prepared/"memory-review.json"),
                       ("inputs/smoke-requests.json.gz", prepared/"smoke-requests.json.gz")):
        committed = members[canonical_inputs+name]
        data = json.loads(gzip.decompress(committed) if name.endswith(".gz") else committed)
        if record_json(data) != record_json(read(path)):
            raise ValueError("prepared input differs from committed packet source: "+name)
    members["candidate-linux313.lock"] = lock.encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(members.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 11, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    output.mkdir(parents=True, exist_ok=False)
    payload = output/PAYLOAD
    payload.write_bytes(buffer.getvalue())
    manifest = archive_manifest(payload, source_commit=commit, payload_name=PAYLOAD)
    helper = (root/"scripts/m5_kaggle_preflight.py").read_text(encoding="utf-8")
    manifest.update(kind="committed-course-cpu-preparation", build_commit=commit, preparation=preparation,
        review_helper_sha256=hashlib.sha256(helper.encode()).hexdigest(),
        candidate_wheels=candidate["candidate_wheels"], build_tools=candidate["build_tools"],
        candidate_lock_sha256=candidate["candidate_lock_sha256"],
        candidate_scope="Unchanged run-5 CPU candidate; full current GPU candidate is unaccepted.",
        memory_preparation_admitted=False, weight_staging_permitted=False,
        disk=dict(payload_bytes=payload.stat().st_size, expanded_source_bytes=manifest["expanded_bytes"],
            candidate_wheel_download_bytes=sum(p["bytes"] for p in candidate["candidate_wheels"]),
            future_full_checkpoint_bytes=read(inspection)["checkpoint_index"]["total_checkpoint_bytes"],
            current_host_free_bytes=None, staging_replicas=None,
            requirement="Verify scratch/output space for downloads, expansion, environment and two independent durable exports before staging; checkpoint bytes are not complete disk admission."),
        execution=dict(gpu=False, model_generations=0, prior_allocation=None, prior_smoke_attempts=None,
            remaining_smoke_seconds=None, provider_quota=None, provider_duration=None, runtime_freeze=False))
    (output/"source-manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2)+"\n", encoding="utf-8")
    (output/"candidate-linux313.lock").write_text(lock, encoding="utf-8")
    (output/"course_m5_cpu_review.ipynb").write_text(json.dumps(notebook(manifest, helper), indent=1)+"\n", encoding="utf-8")
    print(json.dumps(dict(source_commit=commit, members=len(manifest["members"]),
        payload_bytes=manifest["archive_bytes"], payload_sha256=manifest["archive_sha256"],
        preparation_complete=True, complete_resident_tokens_upper=preparation["complete_resident_tokens_upper"],
        gpu_admission=False, weight_staging_permitted=False), indent=2))
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--inspection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.root.resolve(), args.tokenizer, args.prepared, args.inspection, args.output)


if __name__ == "__main__":
    main()
