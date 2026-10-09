"""Read-only conditional memory audit; never model/GPU acceptance.

Run from the repository: python -S -B -m scripts.m5_model_feasibility --output PATH
Uses retained config/capacity/run-6 bytes and the opt-in chunk setting only.
No Torch import, pretrained weights, GPU operation or existing output mutation.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys
import zipfile

from recovery.t4_attention import PREFILL_CHUNK_SIZE, T4_ATTENTION

GIB = 2**30
HEADROOM = 3 * GIB // 2
ARCHIVE_SHA256 = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
CAPACITY_SHA256 = "e5b0843c9ce1c6a9deef81bf9d2af0b8af041ccbe867ebf31cf970a5f57a9871"
RUN6_SHA256 = "332237aa5b5b73b39bce42dc7ac98c7434bbea15148019b96dd615022c997a96"
CONFIG_SHA256 = {
    "9B": "d0883072e01861ed0b2d47be3c16c36a8e81c224c7ffaa310c6558fb3f932b05",
    "4B": "ddc63e1c717afa86c865bb5e01313d89d72bb53b97ad4a8a03ba8510c0621670",
}


def checked_file(path, expected=None):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if expected is not None and digest != expected:
        raise ValueError("retained input identity differs: " + str(path))
    return dict(path=path.as_posix(), bytes=path.stat().st_size, sha256=digest)


def capacity_envelopes(capacity):
    """Keep complete conservative bounds distinct from constructed fixtures."""
    if capacity["limits"] != dict(context=262144, feedback=32, own_reply=384, prose=128, reserved_output=384):
        raise ValueError("capacity limits differ")
    result = {}
    tasks = {"top_k", "prefix_sum", "difference_array", "distributed_sort", "bfs_distance"}
    for size in ("target", "fallback"):
        rows = [r for r in capacity["accounting"] if r["size"] == size]
        fixtures = [r for r in capacity["rendered_fixtures"] if r["size"] == size]
        if (len(rows) != 5 or {r["task"] for r in rows} != tasks
                or len(fixtures) != 40 or not all(r["bound_fits"] is True for r in rows)):
            raise ValueError("complete capacity coverage differs")
        for row in rows:
            payload = row["payload_token_allowances"]
            factors = row["input_tokens_per_payload_token_upper"]
            calculated = row["nontext_bytes"] + row["template_wrapper_bytes"]
            calculated += payload["own_replies"] * factors["own_replies"]
            calculated += payload["received_prose"] * factors["received_prose"]
            if (factors != dict(own_replies=48, received_prose=45)
                    or row["input_tokens_upper"] != calculated
                    or row["with_output_reserve_upper"] != calculated + 384
                    or calculated + 384 > 262144):
                raise ValueError("complete capacity arithmetic differs")
        if any(r["with_output_reserve"] != r["input_tokens"] + 384 or r["fits"] is not True for r in fixtures):
            raise ValueError("fixture capacity arithmetic differs")
        result[size] = dict(
            complete_input_tokens_upper=max(r["input_tokens_upper"] for r in rows),
            complete_resident_tokens_upper=max(r["with_output_reserve_upper"] for r in rows),
            constructed_fixture_max_input_tokens=max(r["input_tokens"] for r in fixtures),
            constructed_fixture_max_resident_tokens=max(r["with_output_reserve"] for r in fixtures),
            accounting_rows=len(rows), constructed_fixtures=len(fixtures),
            scope="Conservative bound for permitted histories; fixture maximum is not that bound or a model trajectory.",
            upper_bound_attainability=None,
        )
    return result


def model_estimates(outer, resident_tokens):
    """Conditional tensor arithmetic, never a complete live allocator bound."""
    c = outer["text_config"]
    layers = c["layer_types"]
    if ((c["num_attention_heads"], c["num_key_value_heads"], c["head_dim"],
         c["num_hidden_layers"], len(layers), layers.count("full_attention"),
         c["vocab_size"], c["max_position_embeddings"]) != (16, 4, 256, 32, 32, 8, 248320, 262144)
            or type(resident_tokens) is not int or not 1 <= resident_tokens <= 262144):
        raise ValueError("reviewed geometry or resident-token bound differs")
    tied = c.get("tie_word_embeddings", outer["tie_word_embeddings"])
    if type(tied) is not bool or tied != outer["tie_word_embeddings"]:
        raise ValueError("invalid/inconsistent embedding tie")
    kv_per_token = 2 * 8 * 4 * 256 * 2
    embeddings = c["vocab_size"] * c["hidden_size"] * 2 * (1 if tied else 2)
    mlp = 3 * c["hidden_size"] * c["intermediate_size"] * 32 // 2
    kv = kv_per_token * resident_tokens
    aligned_length = (resident_tokens + 7) // 8 * 8
    chunk = min(PREFILL_CHUNK_SIZE, resident_tokens)
    return dict(
        tie_word_embeddings=tied, kv_bytes_per_resident_token=kv_per_token,
        fp16_embedding_head_bytes=embeddings, ideal_packed_four_bit_mlp_bytes=mlp,
        fp16_full_attention_kv_bytes=kv,
        conditional_weight_kv_subtotal_bytes=embeddings + mlp + kv,
        materialized_repeat_additional_bytes=2 * 16 * 256 * 2 * resident_tokens,
        proposed_kv_view_additional_storage_bytes=0,
        kv_view_scope="Adapter views alias original K/V; actual CUDA kernel workspace is unmeasured.",
        conditional_active_layer_cache_growth_pair_copy_bytes=2 * 4 * 256 * 2 * resident_tokens,
        cache_growth_scope="Conservative one-layer K/V pair-copy term for maintained DynamicCache concatenation; not an observed simultaneous peak.",
        chunk_query_bytes=16 * chunk * 256 * 2, chunk_output_bytes=16 * chunk * 256 * 2,
        conditional_aligned_shared_mask_storage_bytes=chunk * aligned_length * 2,
        conditional_mask_conversion_tensor_allowance_bytes=chunk * aligned_length * 6,
        mask_scope="Head-shared boolean/additive conversion and row alignment before expansion. Six bytes per aligned element conservatively pays its visible tensors; internal workspace remains excluded.",
        excluded_terms=["other attention/linear-attention weights and norms", "NF4 scales/double-quantization metadata and padding",
            "hybrid recurrent/conv state", "other chunk activations, dequantization and attention/recurrent workspaces",
            "allocator fragmentation, CUDA context and non-model occupancy"],
        complete_allocator_upper_bound_bytes=None, measured_model_peak_bytes=None,
        full_envelope_memory_acceptance=None,
    )


def allowance_assessment(subtotal, devices):
    result = {}
    for name, device in devices.items():
        total, free = device["torch_total_bytes"], device["post_probe_free_bytes"]
        if any(type(n) is not int for n in (subtotal, total, free)) or not 0 <= free <= total or total <= HEADROOM:
            raise ValueError("invalid native memory")
        result[name] = dict(
            native_total_bytes=total, historical_post_probe_free_bytes=free,
            required_free_headroom_bytes=HEADROOM,
            native_total_minus_headroom_bytes=total - HEADROOM,
            historical_free_minus_headroom_bytes=free - HEADROOM,
            partial_subtotal_exceeds_native_allowance=subtotal > total - HEADROOM,
            partial_subtotal_exceeds_historical_free_allowance=subtotal > free - HEADROOM,
            scope="Historical run-6 device observation, not current free memory. Partial subtotal comparison proves neither model fit nor empirical failure.",
            full_envelope_memory_acceptance=None,
        )
    return result


def audit(archive_path, capacity_path, run6_path, review_path):
    identities = dict(
        canonical_archive=checked_file(archive_path, ARCHIVE_SHA256),
        capacity_archive=checked_file(capacity_path, CAPACITY_SHA256),
        run6_original_zip=checked_file(run6_path, RUN6_SHA256),
        run6_review=checked_file(review_path),
    )
    capacity = json.loads(gzip.decompress(capacity_path.read_bytes()))
    envelopes = capacity_envelopes(capacity)
    review = json.loads(review_path.read_bytes())
    devices = review["devices"]
    if (set(devices) != {"device_0", "device_1"} or review["model_generations"] != 0
            or review["summary"]["full_envelope_memory_acceptance"] is not None
            or review["conditional_allocation_bound_verified"] is not False
            or review["provider_duration_seconds"] is not None):
        raise ValueError("run-6 scope or allocation evidence differs")
    with zipfile.ZipFile(run6_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("run-6 ZIP CRC failure")
        for name, device in devices.items():
            raw = json.loads(archive.read(name + ".json"))
            if (raw["status"] != "passed" or raw["model_generations"] != 0
                    or raw["capability"] != [7, 5] or raw["torch_version"] != "2.11.0+cu128"
                    or raw["torch_cuda_build"] != "12.8"
                    or device["uuid"] != raw["assigned_uuid"]
                    or raw["observed_uuid"] != raw["assigned_uuid"].removeprefix("GPU-")
                    or device["torch_total_bytes"] != raw["total_memory"]
                    or device["post_probe_free_bytes"] != raw["post_probe_free_bytes"]):
                raise ValueError("review differs from original run-6 device bytes")
    if len({d["uuid"] for d in devices.values()}) != 2:
        raise ValueError("distinct physical devices required")
    models = {}
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("canonical archive CRC failure")
        for model in ("9B", "4B"):
            raw = archive.read(f"metadata/{model}/config.json")
            if hashlib.sha256(raw).hexdigest() != CONFIG_SHA256[model]:
                raise ValueError("retained config differs: " + model)
            config = json.loads(raw)
            cases = {}
            for size, envelope in envelopes.items():
                estimate = model_estimates(config, envelope["complete_resident_tokens_upper"])
                estimate["device_comparisons"] = allowance_assessment(estimate["conditional_weight_kv_subtotal_bytes"], devices)
                cases[size] = estimate
            models[model] = dict(config_sha256=CONFIG_SHA256[model], mathematical_sizes=cases)
    return dict(
        scope="Offline conditional memory audit; complete-envelope admission remains unresolved.",
        inputs=identities, candidate_attention=T4_ATTENTION, proposed_prefill_chunk_size=PREFILL_CHUNK_SIZE,
        envelopes=envelopes, models=models, required_free_headroom_bytes=HEADROOM,
        allocation=dict(provider_stop_user_reported=review["provider_stop_user_reported"],
            provider_duration_seconds=None, prior_allocated_gpu_seconds=None, remaining_smoke_gpu_seconds=None),
        full_envelope_memory_acceptance=None, model_selected=None, model_generations=0,
        actual_cuda_execution=False, pretrained_weights_downloaded=False,
        blockers=["Actual T4 zero-stride/masked/chunked Qwen path is unexecuted.",
            "No independently supported complete live-memory bound at the permitted input envelope.",
            "Full candidate GPU/host acceptance and prior allocation reconciliation remain open."],
        environment=dict(python=sys.version, os=platform.platform()),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=Path("dist/m5-kaggle-preflight.zip"))
    parser.add_argument("--capacity", type=Path, default=Path("tests/fixtures/capacity_report.json.gz"))
    parser.add_argument("--run6", type=Path, default=Path("notebooks/run/6/preflight-results.zip"))
    parser.add_argument("--review", type=Path, default=Path("notebooks/validation/m5-t4-compatibility-run-6/validation.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    # Refuse overwrite before doing work. An absent output remains absent on input failure.
    if args.output.exists():
        raise FileExistsError(args.output)
    report = audit(args.archive, args.capacity, args.run6, args.review)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print("Offline audit passed; model/GPU/full-envelope acceptance remains unknown: " + str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
