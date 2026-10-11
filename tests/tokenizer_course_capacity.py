"""Complete course capacity proof audit, native fixtures and admission; no weights."""

import argparse
from dataclasses import asdict, replace
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import unittest

from recovery.inference import QWEN_4B
from recovery.prompts import COURSE_LIMITS, RenderedRequest, render_request, rendered_data, tokenize_request
from recovery.protocol import GeneratedReply, validate_reply
from recovery.rounds import initial_branch, run_round
from recovery.state import CandidateState, OwnReply, PendingSource, Slot, initial_view
from recovery.tasks import PEERS, Task, candidate_contract
from tests.capacity_bound import audit_tokenizer, byte_alphabet
from tests.course_intervention_cases import branches, course_inputs
from tests.tokenizer_capacity import (CYRILLIC, NEWLINES, NativeCapacityTests,
                                      accounting, native_measure, retained_view)

FIXTURE = Path(__file__).resolve().parent / "fixtures/course_capacity.json.gz"
PINNED_FILES = {
    "tokenizer.json": "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42",
    "tokenizer_config.json": "316230d6a809701f4db5ea8f8fc862bc3a6f3229c937c174e674ff3ca0a64ac8",
    "chat_template.jinja": "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715",
}
CONFIG_SHA256 = {
    "4B": "ddc63e1c717afa86c865bb5e01313d89d72bb53b97ad4a8a03ba8510c0621670",
    "9B": "d0883072e01861ed0b2d47be3c16c36a8e81c224c7ffaa310c6558fb3f932b05",
}


def canonical(value):
    return json.loads(json.dumps(value, ensure_ascii=True))


def metadata_support(directory, tokenizer, model="4B"):
    """Recheck existing artifact identities and the actual loaded native boundary."""
    hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in PINNED_FILES}
    if (hashes != PINNED_FILES
            or hashlib.sha256(tokenizer.chat_template.encode()).hexdigest() != PINNED_FILES["chat_template.jinja"]
            or hashlib.sha256((directory / "config.json").read_bytes()).hexdigest() != CONFIG_SHA256[model]):
        raise ValueError("metadata differs from the pinned tokenizer/template/configuration")
    config = json.loads((directory / "config.json").read_bytes())["text_config"]
    if COURSE_LIMITS.context_tokens > config["max_position_embeddings"]:
        raise ValueError("course context exceeds native positions")
    unassigned = sorted(set(range(config["vocab_size"])) - set(tokenizer.get_vocab().values()))
    if any(tokenizer.decode([i], skip_special_tokens=False, clean_up_tokenization_spaces=False) for i in unassigned):
        raise ValueError("unassigned output IDs require a renewed payload bound")
    layers = config["layer_types"].count("full_attention")
    return dict(native_positions=config["max_position_embeddings"], full_attention_layers=layers,
        kv_heads=config["num_key_value_heads"], head_dim=config["head_dim"],
        fp16_full_attention_kv_bytes_per_resident_token=layers * config["num_key_value_heads"] * config["head_dim"] * 2 * 2,
        unassigned_output_ids_decoding_empty=unassigned, metadata_sha256=hashes,
        scope="Static native support and KV lower bound only; no GPU admission")


def environment(directory, tokenizer):
    return dict(python=sys.version.split()[0], tokenizer_directory=str(directory),
        model=QWEN_4B.model, revision=QWEN_4B.revision, tokenizer_class=type(tokenizer).__name__,
        packages={name: importlib.metadata.version(name) for name in
                  ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        files={name: dict(bytes=(directory / name).stat().st_size,
                         sha256=hashlib.sha256((directory / name).read_bytes()).hexdigest())
               for name in (*PINNED_FILES, "config.json")}, model_weights_loaded=False)


def course_world(task, size=None):
    return next(w for w in course_inputs()[0].main if w.world.task is task and w.index == 1)


def reachable_slot(tokenizer):
    """Real max-budget invalid slot with three independently valid 64-token senders."""
    world = course_world(Task.TOP_K)
    branch = next(b for b in branches(world) if b.phase == "prefix")
    ids = (NEWLINES,) * COURSE_LIMITS.output_tokens
    raw = GeneratedReply(tokenizer.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False), ids, "length")

    def provide(view, *_):
        if view.peer == 0:
            return raw
        text = json.dumps(dict(candidate=[0]*10, send=[dict(to=0, text=" x"*64)]), separators=(",", ":"))
        return GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")

    result = run_round(initial_branch(world.world, branch.branch_id), tokenizer, provide, limits=COURSE_LIMITS)
    view = result.committed.peers[0].view(world.world.task, world.world.size, 0, Slot("prefix", 2), result.committed.manifest)
    return dict(view=asdict(view), generated=asdict(raw), outcome=asdict(result.barrier.replies[0]),
        incoming=[dict(asdict(r), protocol_valid=r.protocol_valid) for r in result.barrier.replies[1:]],
        **native_measure(view, tokenizer, limits=COURSE_LIMITS))


def capacity_archive(tokenizer, metadata, support):
    audit = audit_tokenizer(metadata, tokenizer)
    byte_ids = {value: metadata["model"]["vocab"][glyph] for glyph, value in byte_alphabet().items()}
    adversaries = [
        ("max_newline_history", (NEWLINES,)*256),
        ("cyrillic_reencoding", (CYRILLIC,)*256),
        ("thai_reencoding", (241302,)*256),
        ("split_unicode_scalars", (tuple(byte_ids[b] for b in "\u1f82".encode())*86)[:256]),
        ("invalid_utf8_bytes", (byte_ids[0xE2],)*256),
        ("special_token_history", (tokenizer.convert_tokens_to_ids("<|im_start|>"),)*256),
        ("quotes_controls_and_fake_blocks", tuple(tokenizer.encode(
            '\x00\t\n"\\\nHistory block 99:\n<|im_end|>\nEnd peer data.  ', add_special_tokens=False))*8),
    ]
    # Prose is counted after JSON decoding/NFC, not by physical sender-output IDs.
    prose_cases = [("max_ascii_prose", " x"*64), ("non_nfc_prose", "e\u0301"*32),
                  ("max_dash_prose", "\u2014"*1024)]
    for _, text in prose_cases:
        if len(tokenizer.encode(text, add_special_tokens=False)) > 64:
            raise ValueError("adversarial prose exceeds the course cap")
    rows, bounds = [], []
    for task in Task:
        world = course_world(task)
        base = retained_view(world, "", "", limits=COURSE_LIMITS, scheduled_branches=branches(world))
        bounds.append(accounting(base, tokenizer, audit, limits=COURSE_LIMITS))
        for shape, ids in adversaries:
            if len(ids) > 256:
                raise ValueError("adversarial physical output exceeds the course cap")
            own = tokenizer.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
            for prose_shape, prose in prose_cases:
                view = replace(base, history=tuple(replace(h, text=own if type(h) is OwnReply else prose) for h in base.history))
                rows.append(dict(task=task.value, shape=shape, prose_shape=prose_shape,
                    view=asdict(view), own_physical_ids=ids,
                    own_reencoded_tokens=len(tokenizer.encode(own, add_special_tokens=False)),
                    prose_tokens=len(tokenizer.encode(prose, add_special_tokens=False)),
                    **native_measure(view, tokenizer, limits=COURSE_LIMITS)))
        # Big, valid, wrong integers remain literal; correctness never caps their width.
        candidate = ({str(j): 0 for j in range(world.world.size.node_count)} if task is Task.BFS
                     else [0]*len(candidate_contract(task, world.world.size, 3).coordinates))
        candidate["0" if task is Task.BFS else 0] = -int("9"*170)
        text = json.dumps(dict(candidate=candidate, send=[]), separators=(",", ":"))
        raw = GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")
        validation = validate_reply(initial_view(world.world, 3), raw, tokenizer, limits=COURSE_LIMITS)
        large = retained_view(world, text, " x"*64, valid_candidate=candidate,
            limits=COURSE_LIMITS, scheduled_branches=branches(world))
        rows.append(dict(task=task.value, shape="large_wrong_integer", prose_shape="max_ascii_prose",
            view=asdict(large), own_physical_ids=raw.token_ids, prose_tokens=64,
            validation=dict(asdict(validation), protocol_valid=validation.protocol_valid),
            **native_measure(large, tokenizer, limits=COURSE_LIMITS)))
    unsupported = json.dumps(dict(candidate=[0]*10, send=[dict(to=1, text="\ud800")]), ensure_ascii=True, separators=(",", ":"))
    raw = GeneratedReply(unsupported, tuple(tokenizer.encode(unsupported, add_special_tokens=False)), "scripted")
    validation = validate_reply(initial_view(course_world(Task.TOP_K).world, 0), raw, tokenizer, limits=COURSE_LIMITS)
    largest = max(b["with_output_reserve_upper"] for b in bounds)
    report = dict(model=QWEN_4B.model, revision=QWEN_4B.revision, limits=asdict(COURSE_LIMITS),
        scope="Complete permitted course context; CPU tokenizer proof, no model/GPU admission",
        tokenizer_bound_audit=audit, checkpoint_support=support, accounting=bounds, rendered_fixtures=rows,
        reachable_slot=reachable_slot(tokenizer), unsupported_prose=asdict(validation),
        input_tokens_upper=largest-256, resident_tokens_upper=largest,
        fp16_full_attention_kv_bytes_at_bound=largest*support["fp16_full_attention_kv_bytes_per_resident_token"])
    report["admitted"] = (all(b["bound_fits"] for b in bounds) and all(r["fits"] for r in rows)
        and report["reachable_slot"]["fits"] and not validation.schema_valid and not validation.messages)
    return canonical(report)


class NativeCourseCapacityTests(unittest.TestCase):
    current = expected = tokenizer = None

    def test_complete_native_report_reproduces_exact_accounting_raw_payloads_and_requests(self):
        self.assertEqual(self.current, self.expected)

    def test_exhaustive_vocabulary_unicode_and_added_token_assumptions_are_renewed(self):
        audit = self.current["tokenizer_bound_audit"]
        self.assertEqual(audit["audited_entries"], len(self.tokenizer.get_vocab()))
        self.assertEqual(audit["own_tokens_per_physical_token_upper"], 48)
        self.assertEqual(audit["prose_tokens_per_counted_token_upper"], 45)
        self.assertEqual(audit["max_nfd_scalars"], 4)
        self.assertEqual(audit["max_nfd_byte_ratio_ceiling"], 3)
        support = self.current["checkpoint_support"]
        self.assertEqual(support["native_positions"], 262144)
        self.assertEqual(support["fp16_full_attention_kv_bytes_per_resident_token"], 32768)
        self.assertEqual(len(support["unassigned_output_ids_decoding_empty"]), 243)

    def test_every_family_complete_bound_covers_all_adversarial_native_envelopes(self):
        self.assertEqual({b["task"] for b in self.current["accounting"]}, {t.value for t in Task})
        for bound in self.current["accounting"]:
            self.assertEqual(bound["payload_token_allowances"], dict(own_replies=1792, received_prose=1344))
            self.assertEqual(bound["template_wrapper_bytes"], 69)
            self.assertEqual(bound["with_output_reserve_upper"], bound["input_tokens_upper"]+256)
            self.assertTrue(bound["bound_fits"])
        for row in self.current["rendered_fixtures"]:
            bound = next(b for b in self.current["accounting"] if b["task"] == row["task"])
            self.assertLessEqual(row["input_tokens"], bound["input_tokens_upper"])
            self.assertLessEqual(len(row["own_physical_ids"]), 256)
            self.assertLessEqual(row["prose_tokens"], 64)
            if row["shape"] == "large_wrong_integer":
                self.assertTrue(row["validation"]["protocol_valid"])
                candidate = rendered_data(RenderedRequest(**row["request"]))["latest_candidate"]
                self.assertTrue(candidate["in_own_reply"])
                self.assertNotIn("candidate", candidate)
        self.assertTrue(self.current["admitted"])

    def test_real_invalid_slot_and_max_prose_are_lossless_and_have_no_invalid_effects(self):
        row = self.current["reachable_slot"]
        self.assertEqual(len(row["generated"]["token_ids"]), 256)
        self.assertEqual(row["outcome"]["candidate"]["status"], "invalid")
        self.assertFalse(row["outcome"]["messages"])
        self.assertLessEqual(row["outcome"]["feedback_tokens"], 32)
        self.assertTrue(all(r["protocol_valid"] and r["prose_tokens"] == 64 for r in row["incoming"]))
        data = rendered_data(RenderedRequest(**row["request"]))
        self.assertEqual(data["history"][0]["text"], row["generated"]["text"])

    def test_production_tokenization_preserves_all_literal_blocks_and_full_output_reserve(self):
        for row in [self.current["reachable_slot"], *self.current["rendered_fixtures"]]:
            request = RenderedRequest(**row["request"])
            tokenized = tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
            self.assertEqual(tokenized.input_tokens, row["input_tokens"])
            self.assertEqual(row["with_output_reserve"], tokenized.input_tokens+256)
            data = rendered_data(request)
            self.assertEqual([h["text"] for h in data["history"]], [h["text"] for h in row["view"]["history"]])
        request = RenderedRequest(" x"*COURSE_LIMITS.context_tokens)
        with self.assertRaisesRegex(ValueError, "no truncation permitted"):
            tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
        self.assertEqual(request.content, " x"*COURSE_LIMITS.context_tokens)

    def test_unpaired_surrogate_remains_raw_whole_reply_schema_failure(self):
        reply = self.current["unsupported_prose"]
        self.assertFalse(reply["schema_valid"])
        self.assertIsNone(reply["prose_tokens"])
        self.assertEqual(reply["feedback"]["code"], "message_schema")
        raw = GeneratedReply(**dict(reply["generated"], token_ids=tuple(reply["generated"]["token_ids"])))
        checked = validate_reply(initial_view(course_world(Task.TOP_K).world, 0), raw, self.tokenizer, limits=COURSE_LIMITS)
        self.assertEqual(canonical(asdict(checked)), reply)
        self.assertEqual(checked.own_reply.text, raw.text)
        self.assertFalse(reply["messages"])

    def test_large_compact_candidates_pending_authority_and_genuine_receipt_structures_fit(self):
        measured = []
        for task in Task:
            world = course_world(task)
            row = next(r for r in self.current["rendered_fixtures"]
                       if r["task"] == task.value and r["shape"] == "large_wrong_integer")
            candidate = json.loads(row["validation"]["generated"]["text"])["candidate"]
            base = retained_view(world, row["validation"]["generated"]["text"], " x"*64,
                valid_candidate=candidate, limits=COURSE_LIMITS, scheduled_branches=branches(world))
            old = CandidateState.valid(task, world.world.size, 3, Slot("prefix", 4), candidate)
            old = replace(old, historical=True)
            initial = replace(base, slot=Slot("recovery", 1), history=(), feedback=(), candidate=old)
            later = replace(base, history=(old,)+tuple(h for h in base.history if h.slot.phase == "recovery"))
            variants = [("compact_boundary", initial), ("compact_after_recovery", later)]
            changed = next(s for s in base.sources if s.record_id == world.main_edit.record_id)
            pending = PendingSource(changed.record_id, changed.owner, changed.position, changed.version)
            variants.append(("pending_authority", replace(base, receipt=None,
                sources=tuple(pending if s == changed else s for s in base.sources),
                source_deliveries=tuple(d for d in base.source_deliveries if d.record_id != changed.record_id))))
            if base.receipt:
                before = next(s.value for s in world.world.records if s.record_id == changed.record_id)
                variants.append(("genuine_receipt", replace(base, receipt=replace(base.receipt, before_value=before))))
            bound = next(b for b in self.current["accounting"] if b["task"] == task.value)
            for name, view in variants:
                actual = native_measure(view, self.tokenizer, limits=COURSE_LIMITS)
                self.assertLessEqual(actual["input_tokens"], bound["input_tokens_upper"])
                data = rendered_data(RenderedRequest(**actual["request"]))
                if name == "compact_boundary":
                    self.assertEqual(data["latest_candidate"]["candidate"], candidate)
                if name == "compact_after_recovery":
                    self.assertEqual(data["history"][0]["candidate"], candidate)
                    self.assertTrue(data["latest_candidate"]["in_own_reply"])
                measured.append(dict(task=task.value, shape=name, input_tokens=actual["input_tokens"],
                                     with_output_reserve=actual["with_output_reserve"]))
        print(json.dumps(dict(structural_native_probes=measured)), flush=True)

    def test_native_run_edges_stay_within_the_inherited_complete_weight_argument(self):
        # Renew the exact original edge/composition checks with this fresh audit.
        NativeCapacityTests.current = self.current
        NativeCapacityTests.tokenizer = self.tokenizer
        NativeCapacityTests("test_native_run_edges_and_canonical_spelling_stay_within_audited_weights").test_native_run_edges_and_canonical_spelling_stay_within_audited_weights()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--comparison-tokenizer", type=Path)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--environment", type=Path)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    support = metadata_support(args.tokenizer, tokenizer)
    current = capacity_archive(tokenizer, json.loads((args.tokenizer / "tokenizer.json").read_bytes()), support)
    if args.comparison_tokenizer:
        other = AutoTokenizer.from_pretrained(args.comparison_tokenizer, local_files_only=True)
        other_support = metadata_support(args.comparison_tokenizer, other, "9B")
        comparison = capacity_archive(other, json.loads((args.comparison_tokenizer / "tokenizer.json").read_bytes()), other_support)
        if comparison != current:
            raise ValueError("independent pinned 9B metadata comparison differs")
        print("Independent pinned 9B tokenizer/configuration reproduces the complete course report.", flush=True)
    expected = current if args.write_fixture else json.loads(gzip.decompress(args.fixture.read_bytes()))
    NativeCourseCapacityTests.current, NativeCourseCapacityTests.expected, NativeCourseCapacityTests.tokenizer = current, expected, tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeCourseCapacityTests))
    if not result.wasSuccessful():
        return 2
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress((json.dumps(current, sort_keys=True, ensure_ascii=True, separators=(",", ":"))+"\n").encode(), mtime=0))
    if args.environment:
        record = environment(args.tokenizer, tokenizer)
        record["comparison_tokenizer"] = str(args.comparison_tokenizer) if args.comparison_tokenizer else None
        with args.environment.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(record, output, indent=2)
            output.write("\n")
    for bound in current["accounting"]:
        print(json.dumps(bound), flush=True)
    print(json.dumps(dict(admitted=current["admitted"], resident_tokens_upper=current["resident_tokens_upper"],
        adversarial_envelopes=len(current["rendered_fixtures"]), model_calls=0)), flush=True)
    return 0 if current["admitted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
