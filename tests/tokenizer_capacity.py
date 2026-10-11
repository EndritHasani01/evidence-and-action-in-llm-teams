"""Conservative horizon accounting and adversarial native capacity evidence.

This command returns nonzero when capacity is blocked, even if all regression
checks pass. It never truncates, changes a size/configuration, or invokes a model.
"""

import argparse
from dataclasses import asdict, replace
import gzip
import hashlib
import json
from pathlib import Path
import unittest

from recovery.events import start_continuation
from recovery.prompts import (MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS, THESIS_LIMITS, RenderedRequest,
                              render_request, rendered_data, tokenize_request)
from recovery.protocol import GeneratedReply, validate_reply
from recovery.rounds import initial_branch, run_prefix, run_round
from recovery.schedule import _prepare_branches
from recovery.state import (PUBLIC_FEEDBACK, CandidateState, Feedback, OwnReply, ReceivedProse,
                            Slot, SourceDelivery, initial_view)
from recovery.tasks import PEERS, Size, Task, candidate_contract, numeric_range
from recovery.witness import witness_provider
from tests.event_checks import case_world, scheduled
from tests.round_checks import TOKENIZER
from tests.tokenizer_attainability import provenance
from tests.capacity_bound import audit_tokenizer, byte_alphabet, piece_upper

FIXTURE = Path(__file__).resolve().parent / "fixtures/capacity_report.json.gz"
# Actual model-vocabulary IDs, not text re-encoded to impersonate physical cost.
NEWLINES = 76374
CYRILLIC = 224227
SLOTS = tuple(Slot("prefix", r) for r in range(1, 5)) + tuple(Slot("recovery", r) for r in range(1, 4))


def native_measure(view, tokenizer, *, limits=THESIS_LIMITS):
    request = render_request(view, limits=limits)
    text = tokenizer.apply_chat_template(request.messages(), tokenize=False,
                                         add_generation_prompt=True, enable_thinking=False)
    # Count an overflowing fixture independently; the production path rejects it.
    encoded = tokenizer(text, add_special_tokens=False, truncation=False,
                        padding=False, return_attention_mask=True)
    count = len(encoded["input_ids"])
    return {"request": asdict(request), "input_tokens": count,
            "with_output_reserve": count + limits.output_tokens,
            "fits": count + limits.output_tokens <= limits.context_tokens,
            "template_wrapper_bytes": len(text.encode("utf-8")) - len(request.content.encode("utf-8"))}


def retained_view(world, own_text, prose_text, *, valid_candidate=None,
                  limits=THESIS_LIMITS, scheduled_branches=None):
    """A permitted seven-slot envelope, not an executed adversarial trajectory.

    The real witness supplies acquired source/delivery evidence and the event
    boundary. Payloads/labels are replaced offline for a maximal retained view.
    Each sender can legally direct its entire 128-token text allowance here.
    """

    branches = _prepare_branches((world,)) if scheduled_branches is None else scheduled_branches
    branch = next(b for b in branches if b.phase == "prefix")
    prefix = run_prefix(world.world, branch.branch_id, TOKENIZER, witness_provider(TOKENIZER), limits=limits)
    boundary = start_continuation(prefix.snapshot, world, next(b for b in branches
        if (b.phase, b.event, b.policy, b.replicate) == ("continuation", "revision", "B", 0)))
    base = boundary.peers[3].view(boundary.task, boundary.size, 3, Slot("recovery", 1), boundary.manifest)
    history = tuple(h for slot in SLOTS for h in
                    (OwnReply(slot, own_text), *(ReceivedProse(slot, p, prose_text) for p in PEERS if p != 3)))
    latest = (CandidateState("invalid", SLOTS[-1]) if valid_candidate is None else
              CandidateState.valid(base.task, base.size, base.peer, SLOTS[-1], valid_candidate))
    code = max(PUBLIC_FEEDBACK, key=lambda c: len(json.dumps(PUBLIC_FEEDBACK[c], ensure_ascii=True)))
    return replace(base, slot=Slot("recovery", 4), history=history, candidate=latest,
                   feedback=tuple(Feedback(s, code) for s in SLOTS) if valid_candidate is None else ())


def accounting(view, tokenizer, audit, *, limits=THESIS_LIMITS):
    """Full-horizon weighted byte proof, including the compact K alternative.

    Seven own replies and 21 received texts dominate every policy. K's one
    candidate plus three replies uses four of those seven own allowances; its
    nine received texts use nine of 21. Never add K's payload to all seven B
    replies. Literal blocks isolate native normalization from ASCII metadata.
    """

    sources = []
    for s in view.sources:
        if view.task is Task.BFS:
            # Static-size envelope, including the longest possible endpoints
            # and deletion spelling; not a claimed generated graph.
            value = (view.size.node_count - 2, view.size.node_count - 1)
            sources.append(replace(s, value=value, version=2, deleted=True))
        else:
            value = max(numeric_range(view.task), key=lambda n: len(str(n)))
            sources.append(replace(s, value=value, version=2))
    deliveries = tuple(SourceDelivery(s.record_id, s.version, "peer", 0,
                                      Slot("recovery", 3), Slot("recovery", 4)) for s in sources)
    empty = replace(view, sources=tuple(sources), source_deliveries=deliveries,
                    history=tuple(replace(h, text="") for h in view.history))
    # The edited ID/position can differ from the saved witness world. Use the
    # widest public identity, and the longer ordinary receipt description.
    identity = max(view.manifest, key=lambda s: len(json.dumps(asdict(s))))
    empty = replace(empty, notice=replace(empty.notice, source=identity),
                    receipt=(None if empty.receipt is None else
                             replace(empty.receipt, source=identity, before_value=None)))
    valid = CandidateState.valid(view.task, view.size, view.peer, SLOTS[-1],
                                 ({str(j): 0 for j in range(view.size.node_count)} if view.task is Task.BFS
                                  else [0] * len(candidate_contract(view.task, view.size, view.peer).coordinates)))
    nontext = max(len(render_request(v, limits=limits).content.encode("utf-8"))
                  for v in (empty, replace(empty, candidate=valid)))
    old = replace(valid, slot=Slot("prefix", 4), historical=True)
    compact_view = replace(empty, history=(), feedback=(), candidate=old)
    compact = rendered_data(render_request(compact_view, limits=limits))["latest_candidate"]
    compact["kind"] = "historical_candidate"
    # Pay both possible metadata layouts, although K keeps this only once.
    nontext += 2 * len(json.dumps(compact, ensure_ascii=True, separators=(",", ":")))
    # Empty fixtures have one-digit text lengths in each row. Pay
    # the maximum original-text length: own <=384*128 scalars; prose <=128*128*4
    # scalars, including non-NFC spellings. Both have at most five digits.
    max_length = max(limits.output_tokens * audit["payload_bytes_per_token_upper"],
                     limits.prose_tokens * audit["payload_bytes_per_token_upper"] * audit["max_nfd_scalars"])
    nontext += 28 * (len(str(max_length)) - 1)
    # Generated/usable recovery labels are widest; rows already pay them. A
    # null sender costs three more bytes than a peer ID, and event vs peer
    # origin costs one more. Overpay independently for every source row.
    nontext += len(sources) * 4
    control = initial_view(case_world(view.task, view.size).world, None)
    nontext = max(nontext, len(render_request(control, limits=limits).content.encode("utf-8")))
    wrapper = native_measure(empty, tokenizer, limits=limits)["template_wrapper_bytes"]
    expanded_bytes_per_token = {"own_replies": audit["own_tokens_per_physical_token_upper"],
                               "received_prose": audit["prose_tokens_per_counted_token_upper"]}
    allowances = {"own_replies": 7 * limits.output_tokens, "received_prose": 7 * 3 * limits.prose_tokens}
    upper = nontext + wrapper + sum(allowances[k] * expanded_bytes_per_token[k] for k in allowances)
    return {"task": view.task.value, "size": view.size.value,
            "nontext_bytes": nontext, "template_wrapper_bytes": wrapper,
            "payload_token_allowances": allowances,
            "input_tokens_per_payload_token_upper": expanded_bytes_per_token,
            "input_tokens_upper": upper, "with_output_reserve_upper": upper + limits.output_tokens,
            "bound_fits": upper + limits.output_tokens <= limits.context_tokens}


def counterexample(size, tokenizer):
    """One actual lawful slot; its invalid reply makes the next request overflow."""

    world = case_world(Task.TOP_K, size)
    branch = next(b for b in _prepare_branches((world,)) if b.phase == "prefix")
    before = initial_branch(world.world, branch.branch_id)
    ids = (NEWLINES,) * 384
    raw = GeneratedReply(tokenizer.decode(list(ids), skip_special_tokens=False,
                                         clean_up_tokenization_spaces=False), ids, "length")
    prose = " x" * 128

    def provider(view, rendered, encoded):
        if view.peer == 0:
            return raw
        candidate = [0] * 10
        text = json.dumps({"candidate": candidate, "send": [{"to": 0, "text": prose}]}, separators=(",", ":"))
        return GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")

    result = run_round(before, tokenizer, provider)
    view = result.committed.peers[0].view(before.task, size, 0, Slot("prefix", 2), before.manifest)
    outcome = result.barrier.replies[0]
    return {"size": size.value, "slot": asdict(view.slot), "view": asdict(view),
            "generated": asdict(raw), "recorded_status": outcome.candidate.status,
            "feedback_tokens": outcome.feedback_tokens,
            "valid_incoming_senders": [r.protocol_valid for r in result.barrier.replies[1:]],
            "incoming_prose_tokens": [r.prose_tokens for r in result.barrier.replies[1:]],
            **native_measure(view, tokenizer)}


def capacity_archive(tokenizer, metadata):
    # The bound requires the actual byte-level, NFC tokenizer, not
    # an assumed property of an arbitrary injected counter.
    if (metadata["model"]["type"] != "BPE" or metadata["normalizer"] != {"type": "NFC"}
            or metadata["decoder"]["type"] != "ByteLevel"
            or any(t["lstrip"] or t["rstrip"] or t["normalized"] for t in metadata["added_tokens"])):
        raise ValueError("capacity accounting requires the audited NFC byte-level BPE")
    audit = audit_tokenizer(metadata, tokenizer)
    rows, bounds = [], []
    own_ids = (NEWLINES,) * 384
    own = tokenizer.decode(list(own_ids), skip_special_tokens=False, clean_up_tokenization_spaces=False)
    other_ids = (CYRILLIC,) * 384
    other = tokenizer.decode(list(other_ids), skip_special_tokens=False, clean_up_tokenization_spaces=False)
    forward = {value: glyph for glyph, value in byte_alphabet().items()}
    byte_ids = {value: metadata["model"]["vocab"][glyph] for value, glyph in forward.items()}
    adversaries = [("cyrillic_reencoding", other_ids), ("thai_reencoding", (241302,) * 384),
                   ("split_unicode_scalars", tuple(byte_ids[b] for b in "\u1f82".encode()) * 128),
                   ("invalid_utf8_bytes", (byte_ids[0xE2],) * 384),
                   ("special_token_history", (tokenizer.convert_tokens_to_ids("<|im_start|>"),) * 384)]
    for size in Size:
        for task in Task:
            world = case_world(task, size)
            view = retained_view(world, own, " x" * 128)
            bounds.append(accounting(view, tokenizer, audit))
            texts = [("max_newline_history", own, own_ids),
                     ("max_ascii_history", " x" * 384,
                      tuple(tokenizer.encode(" x" * 384, add_special_tokens=False)))]
            texts += [(shape, tokenizer.decode(list(ids), skip_special_tokens=False,
                                               clean_up_tokenization_spaces=False), ids)
                      for shape, ids in adversaries]
            for shape, raw, ids in texts:
                current = replace(view, history=tuple(replace(h, text=raw) if type(h) is OwnReply else h
                                                      for h in view.history))
                rows.append({"task": task.value, "size": size.value, "shape": shape,
                             "view": asdict(current), "own_physical_ids": ids,
                             "own_reencoded_tokens": len(tokenizer.encode(raw, add_special_tokens=False)),
                             "prose_tokens_per_sender_slot": 128, **native_measure(current, tokenizer)})
            # Large valid integer mistakes stay literal, with no candidate copy
            # beside the own reply and no correctness feedback.
            candidate = {str(j): 0 for j in range(size.node_count)} if task is Task.BFS else \
                        [0] * len(candidate_contract(task, size, 3).coordinates)
            if task is Task.BFS:
                candidate["0"] = int("9" * 200)
            else:
                candidate[0] = -int("9" * 200)
            text = json.dumps({"candidate": candidate, "send": []}, separators=(",", ":"))
            raw = GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")
            checked = validate_reply(replace(view, history=(), feedback=(), candidate=CandidateState()), raw, tokenizer)
            large = retained_view(world, text, " x" * 128, valid_candidate=candidate)
            rows.append({"task": task.value, "size": size.value, "shape": "large_wrong_integer",
                         "view": asdict(large), "own_physical_ids": raw.token_ids,
                         "protocol_valid": checked.protocol_valid, **native_measure(large, tokenizer)})
    # Preserve these illustrative historical probes. They refute 8,192 only;
    # admission now depends on the complete bound and finalized renderer.
    alternatives = []
    for ascii_mode in (True, False):
        text = json.dumps([{"phase": s.phase, "round": s.round_number, "text": other} for s in SLOTS],
                          ensure_ascii=ascii_mode, separators=(",", ":"))
        alternatives.append({"layout": "JSON ASCII" if ascii_mode else "JSON UTF-8",
                             "text": text, "input_tokens": len(tokenizer.encode(text, add_special_tokens=False))})
    text = "".join(f"Own reply {s.phase} round {s.round_number}, literal data:\n{other}\n" for s in SLOTS)
    alternatives.append({"layout": "literal raw text with labels", "text": text,
                         "input_tokens": len(tokenizer.encode(text, add_special_tokens=False))})
    report = {"provenance": dict(provenance(), scope="CPU capacity counterexamples and conservative accounting; no model inference."),
              "limits": {"context": MAX_CONTEXT_TOKENS, "reserved_output": 384, "own_reply": 384, "prose": 128, "feedback": 32},
              "tokenizer_bound_audit": audit, "normalizer": "NFC",
              "accounting": bounds, "rendered_fixtures": rows,
              "reachable_counterexamples": [counterexample(size, tokenizer) for size in Size],
              "lossless_layout_probes": alternatives,
              "special_strings": [], "requested_sizes": [s.value for s in Size]}
    # Actual valid JSON escapes include controls, Unicode and special-looking
    # strings. Preserve exactly what the parser delivers.
    special = '\x00\t\n"\\é中🙂 <think>x</think> <|im_start|>'
    initial = initial_view(case_world(Task.TOP_K, Size.TARGET).world, 0)
    text = json.dumps({"candidate": [0]*10, "send": [{"to": 1, "text": special}]}, ensure_ascii=True, separators=(",", ":"))
    generated = GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")
    checked = validate_reply(initial, generated, tokenizer)
    received = replace(initial_view(case_world(Task.TOP_K, Size.TARGET).world, 1),
                       slot=Slot("prefix", 2), history=(ReceivedProse(Slot("prefix", 1), 0, special),),
                       candidate=CandidateState("failed", Slot("prefix", 1)))
    report["special_strings"].append({"generated": asdict(generated), "literal_prose": special,
                                      "protocol_valid": checked.protocol_valid, "prose_tokens": checked.prose_tokens,
                                      "received_fixture": native_measure(received, tokenizer)})
    # The authorized scalar-text contract rejects this whole reply before
    # native prose counting. Retain the exact raw failure and bounded outcome.
    text = json.dumps({"candidate": [0]*10, "send": [{"to": 1, "text": "\ud800"}]}, ensure_ascii=True, separators=(",", ":"))
    generated = GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")
    checked = validate_reply(initial, generated, tokenizer)
    report["unsupported_prose"] = {"generated": asdict(generated), "literal_prose": "\ud800",
                                   "validation": asdict(checked), "resolved": (
                                       checked.json_valid and checked.schema_valid is False
                                       and checked.prose_tokens is None and not checked.messages
                                       and checked.feedback.code == "message_schema")}
    report["admitted_sizes"] = [size.value for size in Size
        if all(b["bound_fits"] for b in bounds if b["size"] == size.value)
        and all(r["fits"] for r in rows + report["reachable_counterexamples"] if r["size"] == size.value)
        and report["unsupported_prose"]["resolved"]]
    return json.loads(json.dumps(report, ensure_ascii=True))


class NativeCapacityTests(unittest.TestCase):
    current = None
    expected = None
    tokenizer = None

    def test_report_exactly_reproduces_measured_fixtures_and_accounting(self):
        for key in self.current.keys() - {"provenance"}:
            self.assertEqual(self.current[key], self.expected[key], key)
        for key in self.current["provenance"].keys() - {"packages"}:
            self.assertEqual(self.current["provenance"][key], self.expected["provenance"][key], key)

    def test_original_reachable_overflow_is_now_lossless_and_fits_in_both_sizes(self):
        for row in self.current["reachable_counterexamples"]:
            self.assertEqual(len(row["generated"]["token_ids"]), 384)
            self.assertEqual(row["recorded_status"], "invalid")
            self.assertEqual(row["valid_incoming_senders"], [True]*3)
            self.assertEqual(row["incoming_prose_tokens"], [128]*3)
            self.assertTrue(row["fits"])
            self.assertLessEqual(row["feedback_tokens"], 32)

    def test_production_tokenization_preserves_literal_data_and_never_truncates(self):
        for row in self.current["reachable_counterexamples"]:
            request = RenderedRequest(**row["request"])
            before = request.content
            tokenized = tokenize_request(request, self.tokenizer)
            self.assertEqual(tokenized.input_tokens, row["input_tokens"])
            self.assertEqual(request.content, before)
            data = rendered_data(request)
            self.assertEqual(data["history"][0]["text"], row["generated"]["text"])

    def test_complete_bound_covers_adversarial_views_and_admits_both_sizes(self):
        for row in self.current["rendered_fixtures"]:
            bound = next(b for b in self.current["accounting"] if (b["task"], b["size"]) == (row["task"], row["size"]))
            self.assertLessEqual(row["input_tokens"], bound["input_tokens_upper"])
            self.assertTrue(bound["bound_fits"])
            self.assertLessEqual(len(row["own_physical_ids"]), 384)
            if row["shape"] == "large_wrong_integer":
                self.assertTrue(row["protocol_valid"])
                data = rendered_data(RenderedRequest(**row["request"]))
                self.assertTrue(data["latest_candidate"]["in_own_reply"])
                self.assertNotIn("candidate", data["latest_candidate"])

    def test_historical_layout_probes_refute_old_cap_and_special_strings_remain_literal(self):
        for row in self.current["lossless_layout_probes"]:
            # These contain only history. Sources/instructions can only consume
            # further space; no passing complete-renderer proof is claimed.
            self.assertGreater(row["input_tokens"] + 384, 8192)
        for row in self.current["special_strings"]:
            self.assertTrue(row["protocol_valid"])
            self.assertLessEqual(row["prose_tokens"], 128)
            data = rendered_data(RenderedRequest(**row["received_fixture"]["request"]))
            self.assertEqual(data["history"][0]["text"], row["literal_prose"])

    def test_unpaired_surrogate_is_bounded_schema_failure_without_repair_or_delivery(self):
        row = self.current["unsupported_prose"]
        self.assertTrue(row["resolved"])
        raw = GeneratedReply(**dict(row["generated"], token_ids=tuple(row["generated"]["token_ids"])))
        self.assertLessEqual(len(raw.token_ids), 384)
        view = initial_view(case_world(Task.TOP_K, Size.TARGET).world, 0)
        before = asdict(view)
        checked = validate_reply(view, raw, self.tokenizer)
        self.assertEqual(asdict(checked), asdict(validate_reply(view, raw, self.tokenizer)))
        self.assertFalse(checked.schema_valid)
        self.assertEqual(checked.feedback.code, "message_schema")
        self.assertEqual(checked.messages, ())
        self.assertIsNone(checked.prose_tokens)
        self.assertEqual(checked.generated, raw)
        self.assertEqual(checked.own_reply.text, raw.text)
        self.assertEqual(asdict(view), before)

    def test_native_run_edges_and_canonical_spelling_stay_within_audited_weights(self):
        from tokenizers.normalizers import NFD
        audit = self.current["tokenizer_bound_audit"]
        self.assertEqual(audit["audited_entries"], len(self.tokenizer.get_vocab()))
        self.assertEqual(audit["own_tokens_per_physical_token_upper"], 48)
        self.assertEqual(audit["prose_tokens_per_counted_token_upper"], 45)
        nfd = NFD()
        for char in audit["ascii_doubling_ladders"]:
            for size in (7, 8, 15, 16, 31, 32, 63, 64, 127, 128, 129, 513, 4097):
                for before, after in (("", ""), ("a", "z"), ("?", "'t"),
                                      (" ", "\n"), ("\n", "é"), ("", "\u0325")):
                    text = before + char * size + after
                    upper = (piece_upper(char * size, audit["ascii_doubling_ladders"], nfd=nfd)
                             + len(nfd.normalize_str(before + after).encode()))
                    with self.subTest(char=ascii(char), size=size, context=(before, after)):
                        self.assertLessEqual(len(self.tokenizer.encode(text, add_special_tokens=False)), upper)

    def test_native_overflow_guard_reserves_all_output_without_truncation(self):
        request = RenderedRequest(" x" * MAX_CONTEXT_TOKENS)
        before = request.content
        with self.assertRaisesRegex(ValueError, "no truncation permitted"):
            tokenize_request(request, self.tokenizer)
        self.assertEqual(request.content, before)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create new capacity evidence")
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    metadata = json.loads((args.tokenizer / "tokenizer.json").read_bytes())
    current = capacity_archive(tokenizer, metadata)
    # Reuse the artifact identities already established by the prerequisite
    # investigation. These identify the tokenizer/template, not experiment IDs.
    expected = {"tokenizer.json": "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42",
                "tokenizer_config.json": "316230d6a809701f4db5ea8f8fc862bc3a6f3229c937c174e674ff3ca0a64ac8",
                "chat_template.jinja": "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"}
    actual = {name: hashlib.sha256((args.tokenizer / name).read_bytes()).hexdigest() for name in expected}
    if actual != expected or hashlib.sha256(tokenizer.chat_template.encode()).hexdigest() != expected["chat_template.jinja"]:
        raise ValueError("tokenizer/template identity differs from the audited artifacts")
    config = json.loads((args.tokenizer / "config.json").read_bytes())
    config = config.get("text_config", config)
    if MAX_CONTEXT_TOKENS > config["max_position_embeddings"]:
        raise ValueError("uniform context exceeds the pinned checkpoint's native positions")
    full_layers = config["num_hidden_layers"] // config["full_attention_interval"]
    unassigned = sorted(set(range(config["vocab_size"])) - set(tokenizer.get_vocab().values()))
    if any(tokenizer.decode([i], skip_special_tokens=False, clean_up_tokenization_spaces=False)
           for i in unassigned):
        raise ValueError("unassigned output IDs require a renewed decoded-payload bound")
    current["checkpoint_support"] = {
        "native_positions": config["max_position_embeddings"],
        "full_attention_layers": full_layers, "kv_heads": config["num_key_value_heads"],
        "head_dim": config["head_dim"], "fp16_full_attention_kv_bytes_at_cap": (
            MAX_CONTEXT_TOKENS * full_layers * config["num_key_value_heads"] * config["head_dim"] * 2 * 2),
        "unassigned_output_ids_decoding_empty": unassigned,
        "scope": "Static support and KV lower bound only; GPU memory/capability/timing remain M5."}
    current["provenance"].update(metadata_sha256=actual, tokenizer_class=type(tokenizer).__name__,
                                 enable_thinking=False, add_generation_prompt=True)
    fixture = args.write_fixture or args.fixture
    if args.write_fixture:
        payload = (json.dumps(current, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode()
        with fixture.open("xb") as output:
            output.write(gzip.compress(payload, mtime=0) if fixture.suffix == ".gz" else payload)
    payload = fixture.read_bytes()
    NativeCapacityTests.current = current
    NativeCapacityTests.expected = json.loads(gzip.decompress(payload) if fixture.suffix == ".gz" else payload)
    NativeCapacityTests.tokenizer = tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeCapacityTests))
    for row in current["reachable_counterexamples"]:
        print(f"{row['size']}: former overflow uses {row['input_tokens']} input + 384 output = {row['with_output_reserve']} / {MAX_CONTEXT_TOKENS}")
    for row in current["accounting"]:
        print(f"{row['size']} {row['task']}: complete input + reserve upper {row['with_output_reserve_upper']} / {MAX_CONTEXT_TOKENS}")
    if not result.wasSuccessful():
        return 2
    if not current["admitted_sizes"]:
        print("CAPACITY BLOCKED: neither size admitted; M2 stays open for an explicit protocol decision.")
        return 1
    print(f"Capacity admitted sizes: {', '.join(current['admitted_sizes'])}; final size selection remains M5.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
