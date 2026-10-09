"""Native CPU-only decode/config/cache checks; no model construction or inference."""

import argparse
import json
from pathlib import Path
import unittest

from recovery.inference import (QWEN_9B, candidate_settings, decode_suffix)
from recovery.prompts import render_request, tokenize_request
from recovery.protocol import validate_reply
from recovery.state import initial_view
from recovery.tasks import Task
from tests.event_checks import case_world


class NativeInferenceTests(unittest.TestCase):
    tokenizer = None
    directory = None

    def test_saved_native_ids_preserve_raw_internal_invalid_and_cap_ending_suffixes(self):
        fixture = json.loads((Path(__file__).parent / "fixtures/inference_suffixes.json").read_text())
        self.assertEqual(fixture["revision"], QWEN_9B.revision)
        view = initial_view(case_world(Task.PREFIX).world, 0)
        for row in fixture["cases"]:
            with self.subTest(case=row["name"]):
                reply, raw = decode_suffix(self.tokenizer, tuple(row["token_ids"]))
                self.assertEqual(raw, row["raw_suffix_text"])
                self.assertEqual(reply.text, row["parse_text"])
                self.assertEqual(reply.termination, row["termination"])
                self.assertFalse(reply.truncated)
                self.assertEqual(validate_reply(view, reply, self.tokenizer).protocol_valid, row["protocol_valid"])

    def test_actual_template_and_renderer_inputs_are_saved_without_modification(self):
        settings = candidate_settings(self.tokenizer)
        self.assertEqual(settings["chat_template"], (self.directory / "chat_template.jinja").read_text())
        view = initial_view(case_world(Task.SORT).world, 0)
        request = render_request(view)
        actual = tokenize_request(request, self.tokenizer)
        expected = self.tokenizer.apply_chat_template(request.messages(), tokenize=True,
            add_generation_prompt=True, enable_thinking=False)
        self.assertEqual(actual.input_ids, tuple(expected["input_ids"]))
        self.assertTrue(actual.text.endswith("<think>\n\n</think>\n\n"))

    def test_fresh_generation_config_has_no_inherited_penalties_or_extra_stops(self):
        from transformers import GenerationConfig
        config = GenerationConfig(**candidate_settings(self.tokenizer)["generation"])
        config.validate()
        self.assertEqual(config.temperature, 0.7)
        self.assertEqual(config.top_p, 0.8)
        self.assertEqual(config.top_k, 20)
        self.assertEqual(config.min_p, 0)
        self.assertEqual(config.repetition_penalty, 1.0)
        self.assertIsNone(config.stop_strings)
        self.assertIsNone(config.forced_eos_token_id)
        self.assertIsNone(config.constraints)
        self.assertIsNone(config.suppress_tokens)
        self.assertFalse(config.remove_invalid_values)
        self.assertFalse(config.renormalize_logits)

    def test_native_hybrid_cache_instances_start_without_kv_or_recurrent_state(self):
        from transformers import AutoConfig, DynamicCache
        config = AutoConfig.from_pretrained(self.directory, local_files_only=True).get_text_config()
        caches = [DynamicCache(config=config) for _ in range(2)]
        self.assertIsNot(caches[0], caches[1])
        self.assertIsNot(caches[0].layers[0], caches[1].layers[0])
        for cache in caches:
            self.assertEqual(cache.get_seq_length(), 0)
            self.assertFalse(cache.has_previous_state())
        # No model or tensors for a forward pass are constructed by this check.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    NativeInferenceTests.directory = args.tokenizer
    NativeInferenceTests.tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeInferenceTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
