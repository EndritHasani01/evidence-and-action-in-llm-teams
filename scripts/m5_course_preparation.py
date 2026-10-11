"""Materialize/review the course smoke inputs on CPU; never allocate or infer.

R7 remains withheld unless a complete supported live-memory bound exists.
This packet deliberately contains no weight-staging or model-execution command.
"""

import argparse
from copy import deepcopy
from dataclasses import asdict, replace
import gzip
import hashlib
import json
from math import prod
from pathlib import Path

from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
from recovery.state import CandidateState, Feedback, OwnReply, PUBLIC_FEEDBACK, ReceivedProse, Slot
from recovery.t4_attention import PREFILL_CHUNK_SIZE, T4_ATTENTION
from recovery.tasks import PublicSource, Size, Task
from scripts.m5_model_feasibility import HEADROOM, model_estimates

CANDIDATE = replace(QWEN_4B, attention=T4_ATTENTION)
PAYLOAD = "course-m5-source.payload"


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if str(path).endswith(".gz") else data)


def peer_view(data):
    from recovery.rounds import _read_peer
    fields = {name: data[name] for name in ("sources", "history", "candidate", "feedback",
                                           "notice", "receipt", "source_deliveries")}
    return _read_peer(fields).view(Task(data["task"]), Size(data["size"]), data["peer"],
        Slot(**data["slot"]), tuple(PublicSource(**s) for s in data["manifest"]))


def course_envelope(capacity):
    if (capacity["model"], capacity["revision"], capacity["limits"]) != (
            QWEN_4B.model, QWEN_4B.revision, asdict(COURSE_LIMITS)):
        raise ValueError("pinned course capacity identity/limits differ")
    rows = capacity["accounting"]
    if len(rows) != 5 or {r["task"] for r in rows} != {t.value for t in Task}:
        raise ValueError("complete course family coverage required")
    for row in rows:
        if (row["size"] != "fallback" or row["input_tokens_per_payload_token_upper"] !=
                dict(own_replies=48, received_prose=45) or row["payload_token_allowances"] !=
                dict(own_replies=7*256, received_prose=21*64)):
            raise ValueError("complete course payload proof differs")
        expected = row["nontext_bytes"] + row["template_wrapper_bytes"] + 7*256*48 + 21*64*45
        if (row["input_tokens_upper"] != expected or row["with_output_reserve_upper"] != expected+256
                or row["bound_fits"] is not True or expected+256 > 262144):
            raise ValueError("complete course bound arithmetic differs")
    input_upper = max(r["input_tokens_upper"] for r in rows)
    if (capacity["admitted"] is not True or capacity["input_tokens_upper"] != input_upper
            or capacity["resident_tokens_upper"] != input_upper+256):
        raise ValueError("saved complete course admission differs")
    return dict(input_tokens_upper=input_upper, reserved_output_tokens=256,
        resident_tokens_upper=input_upper+256,
        largest_constructed_resident_tokens=max(r["with_output_reserve"] for r in capacity["rendered_fixtures"]),
        scope="Complete permitted-input bound, including invalid text; fixture maximum is supporting evidence.",
        upper_bound_attainability=None)


def memory_review(capacity, inspection, run6):
    envelope = course_envelope(capacity)
    if (inspection["model"] != QWEN_4B.model or inspection["revision"] != QWEN_4B.revision
            or inspection["shape_only_meta_device"] is not True
            or inspection["actual_language_weights_loaded"] is not False
            or inspection["checkpoint_index"]["retained_canonical_index_matches"] is not True):
        raise ValueError("verified shape-only pinned language inventory required")
    parameters = inspection["language_parameters"]
    for row in parameters.values():
        if (not row["shape"] or any(type(d) is not int or d <= 0 for d in row["shape"])
                or type(row["elements"]) is not int or prod(row["shape"]) != row["elements"]
                or row["kind"] not in {"tied_embedding_head", "nf4_linear", "other_fp16_fp32"}):
            raise ValueError("language tensor shape arithmetic differs")
    if sum(p["elements"] for p in parameters.values()) != inspection["total_unique_language_parameters"]:
        raise ValueError("language tensor total differs")
    c = inspection["config"]["text_config"]
    terms = model_estimates(inspection["config"], envelope["resident_tokens_upper"])
    embedding = sum(p["elements"]*2 for p in parameters.values() if p["kind"] == "tied_embedding_head")
    if embedding != terms["fp16_embedding_head_bytes"]:
        raise ValueError("tied embedding/head inventory differs")
    matrices = [p["elements"] for p in parameters.values() if p["kind"] == "nf4_linear"]
    other = sum(p["elements"]*4 for p in parameters.values() if p["kind"] == "other_fp16_fp32")
    if len(matrices) != 248 or len(parameters) != 426 or inspection["total_unique_language_parameters"] != 4205751296:
        raise ValueError("maintained pinned 4B language inventory differs")
    components = dict(fp16_tied_embedding_head_bytes=embedding,
        ideally_packed_nf4_all_linear_bytes=sum((n+1)//2 for n in matrices),
        conditional_double_quant_metadata_bytes=sum((n+63)//64 + 4*((n+16383)//16384) + 1092 for n in matrices),
        ordinary_parameter_fp32_allowance_bytes=other,
        fp16_full_attention_kv_bytes=terms["fp16_full_attention_kv_bytes"],
        fp32_recurrent_state_bytes=24*c["linear_num_value_heads"]*c["linear_key_head_dim"]*c["linear_value_head_dim"]*4,
        fp16_conv_state_bytes=24*(2*c["linear_num_key_heads"]*c["linear_key_head_dim"]+
            c["linear_num_value_heads"]*c["linear_value_head_dim"])*c["linear_conv_kernel_dim"]*2,
        active_layer_kv_growth_pair_copy_bytes=terms["conditional_active_layer_cache_growth_pair_copy_bytes"],
        chunk_query_output_bytes=terms["chunk_query_bytes"]+terms["chunk_output_bytes"],
        shared_mask_conversion_alignment_bytes=terms["conditional_mask_conversion_tensor_allowance_bytes"])
    devices = {}
    for name, device in run6["devices"].items():
        total = device["torch_total_bytes"]
        if type(total) is not int or total <= HEADROOM:
            raise ValueError("historical native device memory required")
        devices[name] = dict(historical_native_total_bytes=total,
            historical_total_minus_required_headroom_bytes=total-HEADROOM,
            conditional_component_sum_bytes=sum(components.values()),
            remaining_for_omitted_terms_bytes=total-HEADROOM-sum(components.values()),
            current_free_bytes=None, actual_course_peak_bytes=None)
    return dict(envelope=envelope, candidate_attention=T4_ATTENTION, prefill_chunk_size=PREFILL_CHUNK_SIZE,
        known_or_conditional_tensor_components=components, devices=devices, required_free_headroom_bytes=HEADROOM,
        component_scope="Source-derived conditional storage arithmetic, not a complete live allocator upper bound.",
        unbounded_terms=["remaining chunk/rotary/MLP/FP32 recurrent temporaries and their simultaneous liveness",
            "NF4 conversion/dequantization temporaries and actual load footprint",
            "efficient-attention, convolution and GEMM workspace on the full candidate CUDA host",
            "allocator reservations/fragmentation, CUDA context and non-model occupancy"],
        complete_live_memory_upper_bound_bytes=None, actual_headroom_acceptance=None,
        preparation_admitted=False, weight_staging_permitted=False,
        blocker="R7: no complete supported live-memory upper bound for the 156,251-token course envelope.",
        terminal_model_feasibility_failure=False,
        conclusion="Keep preparation/model admission blocked. Positive component slack establishes neither fit nor impossibility.")


def smoke_requests(root, tokenizer):
    from recovery.storage import record_json
    archive = read(root / "tests/fixtures/course_attainability.json.gz")
    if (archive["model"], archive["revision"], archive["limits"]) != (
            QWEN_4B.model, QWEN_4B.revision, asdict(COURSE_LIMITS)):
        raise ValueError("course witness origin differs")
    development = {Task(c["task"]): c for c in archive["cases"] if c["development"]}
    if set(development) != set(Task):
        raise ValueError("all five disjoint development origins required")
    settings = candidate_settings(tokenizer, CANDIDATE, limits=COURSE_LIMITS)
    rows = []

    def add(case, call, raw_view, purpose, construction="saved CPU local-view witness", *, expected_tokens=None):
        view = peer_view(raw_view) if isinstance(raw_view, dict) else raw_view
        request = render_request(view, limits=COURSE_LIMITS)
        tokens = tokenize_request(request, tokenizer, limits=COURSE_LIMITS)
        if expected_tokens is not None and record_json(asdict(tokens)) != record_json(expected_tokens):
            raise ValueError("saved native request differs from current course rendering")
        number = len(rows)+1
        rows.append(dict(smoke_call_id=f"smoke/course-m5/{number:02d}", physical_generation_id=f"smoke/course-m5/{number:02d}",
            development_world_id=case["world_id"], origin_call_id=call["call_id"], seed=call["seed"],
            purpose=purpose, construction=construction, intended_worker=0 if number <= 19 else 1,
            confirmed_restart_before=number == 23, controlled_hang=number == 24,
            view=asdict(view), rendered=asdict(request), tokenized=asdict(tokens), settings=deepcopy(settings),
            input_tokens=len(tokens.input_ids), resident_tokens_with_reserve=len(tokens.input_ids)+256,
            executed=False, outcome=None))

    def prefix(case, round_number, peer, purpose):
        saved = case["prefix_rounds"][round_number-1]["barrier"]["requests"]
        call = next(c for c in case["prefix_calls"] if c["round_number"] == round_number and c["peer"] == peer)
        add(case, call, saved["views"][peer], purpose, expected_tokens=saved["tokenized"][peer])

    def continuation(case, policy, round_number):
        return next(r for r in case["rounds"] if r["branch_id"] ==
            f"{case['world_id']}/continuation/revision/{policy}/rep0" and r["slot"]["round_number"] == round_number)

    for task in Task:
        prefix(development[task], 1, 0, "private-shard output shape and finite scores")
    for task, after in ((Task.PREFIX, False), (Task.SORT, False), (Task.BFS, True)):
        case = development[task]
        control = case["controls"][int(after)]
        add(case, control["call"], control["view"], "full-information control with empty sends",
            expected_tokens=control["tokenized"])
    for task in Task:
        prefix(development[task], 4, 0, "locally acquired evidence and literal forwarding")
    case = development[Task.PREFIX]
    corrected = continuation(case, "C", 1)
    for peer in range(4):
        add(case, corrected["calls"][peer], corrected["requests"][peer]["view"],
            "corrected C start from the drained offline witness prefix",
            expected_tokens=corrected["requests"][peer]["tokenized"])
    own_ids = (241302,)*256  # Existing course capacity Thai re-encoding adversary.
    own = tokenizer.decode(own_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
    prose = "\u2014"*1024
    if len(tokenizer.encode(prose, add_special_tokens=False)) != 64:
        raise ValueError("reviewed maximal prose adversary differs")
    slots = [Slot("prefix", r) for r in range(1, 5)] + [Slot("recovery", r) for r in range(1, 4)]
    code = max(PUBLIC_FEEDBACK, key=lambda c: len(json.dumps(PUBLIC_FEEDBACK[c], ensure_ascii=True)))
    for task, policy in ((Task.PREFIX, "B"), (Task.SORT, "Q_B")):
        case = development[task]
        saved = continuation(case, policy, 4)
        base = peer_view(saved["requests"][3]["view"])
        received = lambda slot: [ReceivedProse(slot, p, prose) for p in range(3)]
        history = [h for slot in slots[:4] for h in (OwnReply(slot, own), *received(slot))]
        if policy == "Q_B":
            history += [OwnReply(slots[4], own), OwnReply(slots[5], own), *received(slots[4]),
                        *received(slots[5]), OwnReply(slots[6], own), *received(slots[6])]
        else:
            history += [h for slot in slots[4:] for h in (OwnReply(slot, own), *received(slot))]
        stress = replace(base, history=tuple(history), candidate=CandidateState("invalid", slots[-1]),
                         feedback=tuple(Feedback(slot, code) for slot in slots))
        add(case, saved["calls"][3], stress, "permitted retained stress construction; not full-envelope memory coverage",
            construction="development witness sources/boundary; seven native 256-token own replies and 21 native 64-token prose blocks")
        rows[-1]["own_physical_ids_per_slot"] = list(own_ids)
    a, b = deepcopy(rows[1]), deepcopy(rows[4])
    for source in (a, b, a, a):
        case = development[Task(source["view"]["task"])]
        add(case, dict(call_id=source["origin_call_id"], seed=source["seed"]), source["view"],
            "A/B/A/A after confirmed process restart", expected_tokens=source["tokenized"])
    source = rows[0]
    add(development[Task.TOP_K], dict(call_id=source["origin_call_id"], seed=source["seed"]), source["view"],
        "controlled hang/deadline; infrastructure probe, not observed model latency", expected_tokens=source["tokenized"])
    return dict(scope="24 proposed smoke opportunities; all unexecuted, separate from pilot/main identities",
        regime="course", settings=settings, requests=rows, model_generations=0,
        max_physical_attempts_including_prior=24, max_aggregate_allocated_gpu_seconds_including_prior=1800,
        prior_attempts=None, prior_allocated_gpu_seconds=None, remaining_smoke_attempts=None,
        remaining_smoke_gpu_seconds=None, provider_quota=None, provider_duration=None,
        required_safe_release_wall_seconds=120, attempt_timeout_seconds=120, termination_grace_seconds=1,
        worst_retry_bounded_call_wall_seconds=244, preparation_admitted=False,
        inference_executable=False, runtime_freeze=False)


def verify_requests(root, packet):
    """Independent saved-origin/cap/pair check, usable without optional libraries."""
    from recovery.manifests import load_population, load_schedules
    from recovery.storage import record_json
    population = load_population(root/"tests/fixtures/population_course.json")
    schedule = load_schedules(root/"tests/fixtures/schedules_course.json", population)
    calls = {c.call_id: c for b in schedule.development for c in b.calls}
    rows = packet["requests"]
    if len(rows) != 24 or len({r["smoke_call_id"] for r in rows}) != 24 or packet["regime"] != "course":
        raise ValueError("complete distinct course smoke matrix required")
    for number, row in enumerate(rows, 1):
        call = calls.get(row["origin_call_id"])
        if (call is None or record_json(row["seed"]) != record_json(call.seed) or row["view"]["peer"] != call.peer
                or row["smoke_call_id"] != f"smoke/course-m5/{number:02d}"
                or row["physical_generation_id"] != row["smoke_call_id"]
                or not row["origin_call_id"].startswith(row["development_world_id"]+"/")):
            raise ValueError("exact separate smoke identity/development seed origin differs")
        view = peer_view(row["view"])
        if record_json(asdict(render_request(view, limits=COURSE_LIMITS))) != record_json(row["rendered"]):
            raise ValueError("exact permitted course rendering differs")
        if (record_json(row["settings"]) != record_json(packet["settings"])
                or row["input_tokens"] != len(row["tokenized"]["input_ids"])
                or record_json(row["tokenized"]["attention_mask"]) != record_json([1]*row["input_tokens"])
                or any(type(i) is not int or i < 0 for i in row["tokenized"]["input_ids"])
                or row["resident_tokens_with_reserve"] != row["input_tokens"]+256
                or row["resident_tokens_with_reserve"] > 156251
                or row["executed"] is not False or row["outcome"] is not None):
            raise ValueError("exact settings/native count/unexecuted status differs")
    for number in (19, 21, 22):  # 20, 22, 23 are the same A as slot 02.
        for key in ("view", "rendered", "tokenized", "seed", "settings"):
            if record_json(rows[number][key]) != record_json(rows[1][key]):
                raise ValueError("A/order/restart equality differs")
    if rows[22]["confirmed_restart_before"] is not True or rows[23]["controlled_hang"] is not True:
        raise ValueError("confirmed restart and controlled deadline coverage required")
    return dict(verified_requests=24, exact_saved_development_origins=True, model_generations=0)


def verify_native_requests(root, tokenizer, packet):
    from recovery.storage import record_json
    verify_requests(root, packet)
    expected = candidate_settings(tokenizer, CANDIDATE, limits=COURSE_LIMITS)
    if record_json(packet["settings"]) != record_json(expected):
        raise ValueError("exact adopted course candidate settings differ")
    for row in packet["requests"]:
        rendered = render_request(peer_view(row["view"]), limits=COURSE_LIMITS)
        native = tokenize_request(rendered, tokenizer, limits=COURSE_LIMITS)
        if record_json(asdict(native)) != record_json(row["tokenized"]):
            raise ValueError("exact native IDs/mask/template differ")


def materialize(root, tokenizer_directory, inspection_path, output):
    if output.exists():
        raise FileExistsError(output)
    from transformers import AutoTokenizer
    from recovery.storage import record_json
    from tests.tokenizer_course_capacity import metadata_support
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_directory, local_files_only=True)
    metadata_support(tokenizer_directory, tokenizer)
    inspection = read(inspection_path)
    config = json.loads((tokenizer_directory / "config.json").read_bytes())
    if config != inspection["config"]:
        raise ValueError("inspection and actual pinned config differ")
    review = memory_review(read(root / "tests/fixtures/course_capacity.json.gz"), inspection,
        read(root / "notebooks/validation/m5-t4-compatibility-run-6/validation.json"))
    requests = smoke_requests(root, tokenizer)
    verify_native_requests(root, tokenizer, requests)
    output.mkdir(parents=True, exist_ok=False)
    (output / "smoke-requests.json.gz").write_bytes(gzip.compress(record_json(requests).encode(), mtime=0))
    (output / "memory-review.json").write_text(json.dumps(review, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(requests=len(requests["requests"]), memory_preparation_admitted=False,
        largest_request=max(r["resident_tokens_with_reserve"] for r in requests["requests"]),
        complete_bound=review["envelope"]["resident_tokens_upper"], weights_staged=False), indent=2))
    return review


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--inspection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    materialize(args.root.resolve(), args.tokenizer, args.inspection, args.output)
    # Exit zero means safe CPU preparation was recorded, never that R7 passed.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
