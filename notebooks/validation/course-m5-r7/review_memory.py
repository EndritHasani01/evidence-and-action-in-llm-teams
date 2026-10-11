"""Supplement existing conditional arithmetic with verified R7 evidence."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))

from scripts.m5_course_preparation import memory_review, read
from scripts.m5_model_feasibility import model_estimates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("retain old evidence; use a fresh output")
    capacity_path = ROOT/"tests/fixtures/course_capacity.json.gz"
    capacity = read(capacity_path)
    bound = read(FOLDER/"native-tightening-source.json")
    installed = read(FOLDER/"outside-provenance.json")
    if (bound != installed["report"] or not installed["report_matches_source"]
            or bound["source_capacity_sha256"] != hashlib.sha256(capacity_path.read_bytes()).hexdigest()
            or bound["tokenizer_sha256"] != capacity["checkpoint_support"]["metadata_sha256"]["tokenizer.json"]
            or any(bound[k] != capacity[k] for k in ("model","revision","limits"))):
        raise ValueError("independently verified pinned proof required")
    old_rows = {r["task"]:r for r in capacity["accounting"]}
    if {r["task"] for r in bound["accounting"]} != set(old_rows) or len(bound["accounting"]) != 5:
        raise ValueError("complete family coverage differs")
    for row in bound["accounting"]:
        original = old_rows[row["task"]]
        if (any(row[k] != original[k] for k in ("size","nontext_bytes","template_wrapper_bytes"))
                or row["own_payload_tokens_upper"] != 7*256*32
                or row["prose_payload_tokens_upper"] != 21*64*32
                or row["input_tokens_upper"] != 7*256*32+21*64*32+row["nontext_bytes"]+row["template_wrapper_bytes"]
                or row["resident_tokens_upper"] != row["input_tokens_upper"]+256):
            raise ValueError("supplemental complete bound arithmetic differs")
    resident = max(r["resident_tokens_upper"] for r in bound["accounting"])
    if resident != bound["resident_tokens_upper"] or resident != 110107:
        raise ValueError("complete maximum differs")
    inspection = read(ROOT/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
    run6 = read(ROOT/"notebooks/validation/m5-t4-compatibility-run-6/validation.json")
    prior = memory_review(capacity,inspection,run6)
    terms = model_estimates(inspection["config"],resident)
    components = dict(prior["known_or_conditional_tensor_components"])
    for key,new in dict(fp16_full_attention_kv_bytes=terms["fp16_full_attention_kv_bytes"],
            active_layer_kv_growth_pair_copy_bytes=terms["conditional_active_layer_cache_growth_pair_copy_bytes"],
            shared_mask_conversion_alignment_bytes=terms["conditional_mask_conversion_tensor_allowance_bytes"]).items():
        components[key] = new
    devices = {name:dict(**row, tightened_conditional_component_sum_bytes=sum(components.values()),
        tightened_remaining_for_omitted_terms_bytes=row["historical_total_minus_required_headroom_bytes"]-sum(components.values()))
        for name,row in prior["devices"].items()}
    meta = read(args.meta)
    if (meta["resident_tokens_upper"] != resident or meta["cuda_initialized"] is not False
            or meta["real_pretrained_weights_loaded"] is not False or meta["gpu_headroom_accepted"] is not False):
        raise ValueError("meta-only evidence scope differs")
    matrices = [r["elements"] for r in inspection["language_parameters"].values() if r["kind"] == "nf4_linear"]
    largest = max(matrices)
    report = dict(model=bound["model"],revision=bound["revision"],limits=bound["limits"],
        original_resident_tokens_upper=capacity["resident_tokens_upper"],resident_tokens_upper=resident,
        original_conditional_component_sum_bytes=sum(prior["known_or_conditional_tensor_components"].values()),
        tightened_known_or_conditional_tensor_components=components,devices=devices,
        kv_reduction_bytes=(capacity["resident_tokens_upper"]-resident)*32768,
        observed_meta_cases=meta["cases"],
        meta_scope=meta["scope"],
        conditional_largest_nf4_projection=dict(elements=largest,fp16_dequantized_matrix_bytes=2*largest,
            two_fp16_matrices_plus_two_fp32_absmax_arrays_bytes=4*largest+8*((largest+63)//64)),
        conditional_default_workspace_per_handle_stream=dict(cublas_bytes=4096*1024*2+16*1024*8,cublaslt_bytes=1024*1024),
        component_scope="Existing conditional arithmetic evaluated at the independently verified tighter bound. Meta observations and conversion/workspace terms are separate alternatives/support, not additive complete peaks.",
        remaining_gaps=["actual quantized loading footprint and CUDA allocation liveness over the entire call",
            "selected cuDNN convolution plan workspace and actual CUDA kernel dispatch",
            "caching allocator reservation/fragmentation through all chunks and serial calls",
            "CUDA context, library occupancy and non-model device occupancy"],
        required_free_headroom_bytes=prior["required_free_headroom_bytes"],
        complete_live_memory_upper_bound_bytes=None,actual_gpu_peak_bytes=None,actual_headroom_acceptance=None,
        preparation_admitted=False,weight_staging_permitted=False,terminal_model_feasibility_failure=False,
        gpu_execution=False,model_weights_loaded=False,
        conclusion="R7 remains unresolved. A sound tighter input bound is verified; neither the conditional subtotal nor meta/storage/kernel-source observations establish full physical peak/headroom or impossibility.")
    with args.output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,indent=2)
        stream.write("\n")
    print(json.dumps(dict(resident_tokens_upper=resident,conditional_component_sum_bytes=sum(components.values()),
        kv_reduction_bytes=report["kv_reduction_bytes"],preparation_admitted=False),indent=2))


if __name__ == "__main__":
    main()
