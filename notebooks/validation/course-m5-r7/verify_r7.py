"""Audit limited offline evidence and protection; R7 must remain withheld."""

import argparse
import base64
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import struct
import sys
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
MUTABLE = {"README.md", "docs/IMPLEMENTATION_PLAN.md", "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/README.md", "docs/todos/course/M5/M5-T01-course-inference-and-smoke-preparation.md",
    "docs/todos/course/M5/M5-T02-course-hardware-smoke-and-memory.md"}


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if str(path).endswith(".gz") else data)


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT).decode("utf-8").strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    assert not args.output.exists()
    baseline = read(FOLDER/"baseline-files.json.gz")
    protected = {p:h for p,h in baseline["files"].items() if p not in MUTABLE}
    for name,expected in protected.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected,name
    plan = (ROOT/"docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    old_plan = git("show",baseline["head"]+":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == old_plan.split("## 11. Course living handoff")[0]
    states = {p.stem[:6]:re.search(r"\*\*Status:\*\* (\w+)",p.read_text(encoding="utf-8"))[1]
        for p in (ROOT/"docs/todos/course").glob("M*/*.md")}
    index = (ROOT/"docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|",index)) == states
    assert Counter(states.values()) == dict(done=11,blocked=10)
    assert states["M5-T01"] == "blocked" and all(states[k]=="blocked" for k in states if k.startswith(("M5","M6")))
    for milestone,done,total,active,ready,blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|",index):
        counts = Counter(v for k,v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int,(done,active,ready,blocked))) == tuple(counts[k] for k in ("done","active","ready","blocked"))
    total = re.search(r"\*\*(\d+)/21 course tasks done; (\d+) remaining; (\d+) active; (\d+) ready; (\d+) blocked",index)
    assert tuple(map(int,total.groups())) == (11,10,0,0,10)

    proof = read(FOLDER/"native-tightening-source.json")
    outside = read(FOLDER/"outside-provenance.json")
    assert outside["report"] == proof and outside["source_pythonpath"] is False
    assert outside["matching_installed_modules"] == 29 and outside["hash_seed"] == 211
    installed_root = Path(outside["module"]).parent
    assert not installed_root.is_relative_to(ROOT)
    assert hashlib.sha256((ROOT/"tests/course_capacity_tightening.py").read_bytes().replace(b"\r\n",b"\n")).hexdigest() == outside["proof_sha256"]
    for source in (ROOT/"recovery").glob("*.py"):
        assert source.read_bytes() == (installed_root/source.name).read_bytes()
    capacity = read(ROOT/"tests/fixtures/course_capacity.json.gz")
    assert (proof["audited_entries"],proof["unicode_scalars"],proof["unassigned_output_ids_decoding_empty"]) == (248077,1112064,243)
    assert (proof["tokenizers"],proof["eligible_byte_pairs"]) == ("0.22.2",4203)
    assert (proof["input_tokens_upper"],proof["resident_tokens_upper"],proof["original_resident_tokens_upper"]) == (109851,110107,156251)
    assert all(proof[k] is False for k in ("model_weights_loaded","gpu_execution","memory_preparation_admitted"))
    old = {r["task"]:r for r in capacity["accounting"]}
    for row in proof["accounting"]:
        assert row["nontext_bytes"] == old[row["task"]]["nontext_bytes"]
        assert row["input_tokens_upper"] == row["nontext_bytes"]+69+7*256*32+21*64*32
        assert row["resident_tokens_upper"] == row["input_tokens_upper"]+256

    meta = read(FOLDER/"meta-memory-corrected.json")
    assert meta["cuda_initialized"] is False and meta["real_pretrained_weights_loaded"] is False
    assert meta["gpu_headroom_accepted"] is False and meta["parameter_storage_excluded"] is True
    assert meta["resident_tokens_upper"] == proof["resident_tokens_upper"]
    assert [r["peak_observed_meta_storage_bytes"] for r in meta["cases"]] == [93315072,3897131776,3860368171]
    assert all(r["attention_calls"]==8 and r["aten_operations"]>0 for r in meta["cases"])
    prior_meta = read(FOLDER/"meta-memory.json")
    assert [r["peak_observed_meta_storage_bytes"] for r in meta["cases"]] == [r["peak_observed_meta_storage_bytes"] for r in prior_meta["cases"]]
    critical = read(ROOT/"notebooks/validation/m5-attention-memory/transformers-source.json")["critical_installed_sources"]
    assert meta["sources"] == {r["path"]:r["sha256"] for r in critical}
    sources = read(FOLDER/"native-sources.json.gz")["sources"]
    assert len(sources)==12 and sum(r["bytes"] for r in sources.values())==722473
    for row in sources.values():
        content = row["source"].encode("utf-8")
        assert len(content)==row["bytes"] and hashlib.sha256(content).hexdigest()==row["sha256"]
    review = read(FOLDER/"offline-memory-review.json")
    assert review["resident_tokens_upper"]==110107 and review["original_conditional_component_sum_bytes"]==9172843936
    components = review["tightened_known_or_conditional_tensor_components"]
    assert components["fp16_full_attention_kv_bytes"] == 110107*8*4*256*2*2
    assert components["active_layer_kv_growth_pair_copy_bytes"] == 110107*4*256*2*2
    assert components["shared_mask_conversion_alignment_bytes"] == 256*110112*6
    assert sum(components.values())==7400914336
    assert review["kv_reduction_bytes"]==(156251-110107)*32768==1512046592
    assert review["required_free_headroom_bytes"]==3*2**30//2
    for row in review["devices"].values():
        assert row["tightened_remaining_for_omitted_terms_bytes"]==6624510560
        assert row["current_free_bytes"] is None and row["actual_course_peak_bytes"] is None
    assert all(review[k] is False for k in ("preparation_admitted","weight_staging_permitted","terminal_model_feasibility_failure","gpu_execution","model_weights_loaded"))
    assert all(review[k] is None for k in ("complete_live_memory_upper_bound_bytes","actual_gpu_peak_bytes","actual_headroom_acceptance"))
    assert len(review["remaining_gaps"])==4

    # The loading supplement is pinned to its verified checkpoint; protect its
    # receipts, helpers and prior R7 evidence without repeating native runs.
    loading_checkpoint = git("rev-parse","109c8dc")
    loading_files = git("ls-tree","-r","--name-only",loading_checkpoint,
                        "notebooks/validation/course-m5-r7").splitlines()
    for name in loading_files:
        if name.endswith("/verify_r7.py"):
            continue
        committed = subprocess.check_output(["git","show",loading_checkpoint+":"+name],cwd=ROOT)
        current = (ROOT/name).read_bytes()
        assert (current == committed if name.endswith(".gz") else
                current.replace(b"\r\n",b"\n") == committed.replace(b"\r\n",b"\n")),name
    loading = read(FOLDER/"loading-review-source.json")
    assert (loading["checks"],loading["skips"],loading["language_tensors"],loading["checkpoint_tensors"]) == (5,0,426,738)
    assert (loading["model"],loading["revision"]) == (proof["model"],proof["revision"])
    assert loading["language_checkpoint_dtypes"] == dict(BF16=378,F32=48)
    assert (loading["source_derived_parameter_storage_upper_bytes"],
            loading["conditional_active_conversion_tensor_allowance_bytes"],
            loading["nonpersistent_buffer_fp32_allowance_bytes"],
            loading["tensor_storage_loading_allowance_bytes"]) == (3116700064,97321028,256,3214021348)
    assert sum(loading["source_derived_parameter_components_bytes"].values())==3116700064
    assert loading["tied_head_extra_materialization"] is False
    assert loading["maintained_loader_events"] == [[kind,name+".weight"]
        for name in ("first","second","third") for kind in ("materialize","quantize")]
    assert all(loading[k] is False for k in ("cuda_initialized","preparation_admitted","weight_staging_permitted",
        "terminal_model_feasibility_failure","gpu_execution","model_weights_staged","model_weights_loaded"))
    assert all(loading[k] is None for k in ("complete_live_memory_upper_bound_bytes","actual_gpu_peak_bytes","actual_headroom_acceptance"))
    headers = read(FOLDER/"checkpoint-headers.json.gz")
    assert (headers["model"],headers["revision"]) == (proof["model"],proof["revision"])
    assert headers["downloaded_metadata_bytes"] == loading["downloaded_metadata_bytes"] == 90240
    assert headers["tensor_payload_bytes_read"] == loading["tensor_payload_bytes_read"] == 0
    assert headers["model_weights_staged"] is False and headers["gpu_execution"] is False
    for row in headers["headers"].values():
        prefix = base64.b64decode(row["prefix_base64"],validate=True)
        assert len(prefix)==8+struct.unpack("<Q",prefix[:8])[0]==8+row["header_bytes"]
        assert hashlib.sha256(prefix).hexdigest()==row["prefix_sha256"]
        assert [r["bytes_read"] for r in row["ranges"]]==[8,row["header_bytes"]]
    loading_sources = read(FOLDER/"loading-sources.json.gz")["sources"]
    assert len(loading_sources)==5 and sum(r["bytes"] for r in loading_sources.values())==163569
    assert {name:row["sha256"] for name,row in loading_sources.items()}==loading["verified_additional_sources"]
    for row in loading_sources.values():
        raw = row["source"].encode("utf-8")
        assert (len(raw),hashlib.sha256(raw).hexdigest()) == (row["bytes"],row["sha256"])

    # Challenge the new review's rejection boundaries without touching saved
    # files or importing/executing a GPU kernel.
    spec = importlib.util.spec_from_file_location("r7_memory_review",FOLDER/"review_memory.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_read = module.read
    rejected = []
    for label,path,key,value in (("wrong_revision",FOLDER/"native-tightening-source.json","revision","main"),
            ("partial_family_coverage",FOLDER/"native-tightening-source.json","accounting",proof["accounting"][:-1]),
            ("GPU_meta_relabel",FOLDER/"meta-memory-corrected.json","cuda_initialized",True),
            ("headroom_meta_relabel",FOLDER/"meta-memory-corrected.json","gpu_headroom_accepted",True)):
        def altered(candidate,path=path,key=key,value=value):
            result = original_read(candidate)
            if Path(candidate).resolve()==path.resolve():
                result = deepcopy(result)
                result[key]=value
            return result
        with patch.object(module,"read",side_effect=altered),patch.object(sys,"argv",["review_memory", "--meta",str(FOLDER/"meta-memory-corrected.json"),"--output",str(args.output)]):
            try:
                module.main()
            except ValueError:
                rejected.append(label)
            else:
                raise AssertionError(label)
    assert len(rejected)==4 and not args.output.exists()
    for name,count,code in (("native-tightening-source",5,0),("outside-native",5,0)):
        receipt = read(FOLDER/(name+"-command.json"))
        log = gzip.decompress((FOLDER/receipt["log"]).read_bytes()).decode("utf-8")
        assert receipt["exit_code"]==code and re.search(rf"Ran {count} tests",log) and "OK" in log and "skipped=" not in log
    for name,code in (("native-tightening-initial",1),("meta-memory-corrected",0),("offline-memory-review",0),("source-capture",0)):
        receipt = read(FOLDER/(name+"-command.json"))
        assert receipt["exit_code"]==code and (FOLDER/receipt["log"]).is_file()
    for name,code in (("loading-headers",0),("loading-source-capture",0),
                      ("loading-review",1),("loading-review-corrected",0),("loading-review-source",0)):
        receipt = read(FOLDER/(name+"-command.json"))
        log = gzip.decompress((FOLDER/receipt["log"]).read_bytes()).decode("utf-8")
        assert receipt["exit_code"]==code
        if name=="loading-review-source":
            assert "Ran 5 tests" in log and "OK" in log and "skipped=" not in log

    docs = sorted(ROOT/p for p in MUTABLE) + [ROOT/"docs/implementation-research/course-m5-r7-capacity-proof.md",
        ROOT/"docs/validation/course-m5-r7-offline-review.md"]
    links = 0
    for path in docs:
        for target in re.findall(r"\[[^\]\n]+\]\(([^)]+)\)",path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            local = unquote(target.split("#",1)[0])
            if not local:
                continue
            resolved = (path.parent/local).resolve()
            assert resolved.exists() or resolved==args.output.resolve(),(path,target)
            links+=1
    record = dict(status="passed",source_head=git("rev-parse","HEAD"),protected_files=len(protected),
        authority_thesis_runtime_and_prerequisites="byte-identical",pre_course_plan="unchanged",
        course_tasks=dict(Counter(states.values())),native_source_checks=5,outside_native_checks=5,
        native_skips=0,matching_runtime_modules=29,unicode_scalars=1112064,vocabulary_entries=248077,
        complete_resident_tokens_upper=110107,meta_cases=3,pinned_native_sources=12,
        loading_checkpoint=loading_checkpoint,preserved_r7_checkpoint_files=len(loading_files)-1,
        loading_checks=5,loading_skips=0,pinned_loading_sources=5,
        checkpoint_header_bytes=90240,tensor_payload_bytes_read=0,
        explicit_loading_tensor_allowance_bytes=3214021348,
        review_negative_cases=rejected,local_links_checked=links,
        task_status="blocked",r7_resolved=False,preparation_admitted=False,weight_staging_permitted=False,
        terminal_model_feasibility_failure=False,gpu_execution=False,model_weights_loaded=False,
        scope="Verification of limited offline evidence and protected artifacts only; no M5 completion or GPU/headroom admission.")
    with args.output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(record,stream,indent=2)
        stream.write("\n")
    print(json.dumps(record,indent=2))


if __name__ == "__main__":
    main()
