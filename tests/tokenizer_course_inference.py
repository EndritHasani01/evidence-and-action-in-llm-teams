"""Pinned-native course suffix/config/cache checks; no weights or generation."""

import argparse
from dataclasses import replace
import json
from pathlib import Path
import unittest

from recovery.inference import QWEN_4B, PAD_ID, TRANSPORT_ID, candidate_settings, decode_suffix
from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
from recovery.protocol import validate_reply
from recovery.state import initial_view
from recovery.t4_attention import T4_ATTENTION
from recovery.tasks import Task
from tests.course_protocol_cases import course_population
from tests.tokenizer_course_capacity import metadata_support

FIXTURE = Path(__file__).parent / "fixtures/course_inference_suffixes.json"
CANDIDATE = replace(QWEN_4B, attention=T4_ATTENTION)


def suffix_fixture(tokenizer):
    text = '{"candidate":[0,0,0,0,0,0],"send":[]}'
    encode = lambda value: tuple(tokenizer.encode(value, add_special_tokens=False))
    base = encode(text)
    space, = encode(" ")
    cap = lambda ids: ids + (space,) * (256 - len(ids))
    close, = encode("}")
    complete = encode(text[:-1])
    cases = [("terminal", base + (TRANSPORT_ID,), True),
        ("internal_terminal", base + (TRANSPORT_ID, TRANSPORT_ID), False),
        ("unexpected_eos", base + (PAD_ID,), False),
        ("thinking_marker", encode("<think>private</think>" + text) + (TRANSPORT_ID,), False),
        ("cap_complete", complete + (space,)*(255-len(complete)) + (close,), True),
        ("cap_incomplete", cap(encode(text[:-1])), False),
        ("extra_prose", encode(text + "extra") + (TRANSPORT_ID,), False)]
    result = dict(model=QWEN_4B.model, revision=QWEN_4B.revision, limits=256,
                  origin="Constructed native-token fixtures, not model outputs", cases=[])
    for name, ids, valid in cases:
        reply, raw = decode_suffix(tokenizer, ids, limits=COURSE_LIMITS)
        result["cases"].append(dict(name=name, token_ids=list(ids), raw_suffix_text=raw,
            parse_text=reply.text, termination=reply.termination, protocol_valid=valid))
    return result


class NativeCourseInferenceTests(unittest.TestCase):
    directory = tokenizer = None

    def view(self):
        world = next(w for w in course_population().development if w.world.task is Task.PREFIX)
        return initial_view(world.world, 0)

    def test_metadata_and_actual_template_are_the_pinned_4b_candidate(self):
        support = metadata_support(self.directory, self.tokenizer)
        self.assertEqual(support["native_positions"], 262144)
        settings = candidate_settings(self.tokenizer, CANDIDATE, limits=COURSE_LIMITS)
        self.assertEqual(settings["model"], QWEN_4B.model)
        self.assertEqual(settings["chat_template"], (self.directory / "chat_template.jinja").read_text(encoding="utf-8"))
        request = render_request(self.view(), limits=COURSE_LIMITS)
        tokens = tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
        native = self.tokenizer.apply_chat_template(request.messages(), tokenize=True,
            add_generation_prompt=True, enable_thinking=False)
        self.assertEqual(tokens.input_ids, tuple(native["input_ids"]))
        self.assertTrue(tokens.text.endswith("<think>\n\n</think>\n\n"))

    def test_saved_generated_ids_preserve_every_marker_and_cap_ending(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(fixture, suffix_fixture(self.tokenizer))
        self.assertEqual(fixture["revision"], QWEN_4B.revision)
        for row in fixture["cases"]:
            with self.subTest(case=row["name"]):
                reply, raw = decode_suffix(self.tokenizer, tuple(row["token_ids"]), limits=COURSE_LIMITS)
                self.assertEqual(raw, row["raw_suffix_text"])
                self.assertEqual(reply.text, row["parse_text"])
                self.assertEqual(reply.termination, row["termination"])
                self.assertFalse(reply.truncated)
                self.assertEqual(validate_reply(self.view(), reply, self.tokenizer,
                    limits=COURSE_LIMITS).protocol_valid, row["protocol_valid"])
                if row["name"].startswith("cap_"):
                    self.assertEqual(len(reply.token_ids), 256)

    def test_fresh_native_config_preserves_sampling_caps_and_supported_chunking(self):
        from transformers import GenerationConfig
        config = GenerationConfig(**candidate_settings(self.tokenizer, CANDIDATE,
                                                       limits=COURSE_LIMITS)["generation"])
        config.validate()
        self.assertEqual((config.max_new_tokens, config.prefill_chunk_size), (256, 256))
        self.assertEqual((config.temperature, config.top_p, config.top_k, config.min_p,
                          config.repetition_penalty), (0.7, 0.8, 20, 0.0, 1.0))
        for field in ("stop_strings", "forced_eos_token_id", "constraints", "suppress_tokens"):
            self.assertIsNone(getattr(config, field))
        self.assertFalse(config.remove_invalid_values)
        self.assertFalse(config.renormalize_logits)
        self.assertNotIn("presence_penalty", config.to_dict())

    def test_pinned_4b_hybrid_caches_have_independent_empty_kv_and_recurrent_layers(self):
        from transformers import AutoConfig, DynamicCache
        config = AutoConfig.from_pretrained(self.directory, local_files_only=True).get_text_config()
        self.assertTrue(config.tie_word_embeddings)
        caches = [DynamicCache(config=config) for _ in range(2)]
        self.assertEqual(len(caches[0].layers), 32)
        for a, b in zip(caches[0].layers, caches[1].layers):
            self.assertIsNot(a, b)
        for cache in caches:
            self.assertEqual(cache.get_seq_length(), 0)
            self.assertFalse(cache.has_previous_state())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--write-fixture", action="store_true")
    args = parser.parse_args(argv)
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    metadata_support(args.tokenizer, tokenizer)
    if args.write_fixture:
        with FIXTURE.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(suffix_fixture(tokenizer), output, indent=2, ensure_ascii=True)
            output.write("\n")
    NativeCourseInferenceTests.directory, NativeCourseInferenceTests.tokenizer = args.tokenizer, tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(NativeCourseInferenceTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
