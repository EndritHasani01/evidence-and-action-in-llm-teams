"""Explicit optional CPU check with local Qwen tokenizer metadata, never weights.

Run: python -m tests.tokenizer_peer_views --tokenizer <local-metadata-directory>
The standard-library discovery suite does not import this optional harness.
"""

import argparse
from dataclasses import asdict, replace
import importlib.metadata
import json
from pathlib import Path
from random import Random
import unittest

from recovery.prompts import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS, render_request, rendered_data, tokenize_request
from recovery.state import PUBLIC_FEEDBACK, CandidateState, OwnReply, ReceivedProse, Slot, initial_view
from recovery.tasks import PEERS, Size, Task, generate_world
from tests.peer_view_cases import SPECIAL_TEXT, renderer_cases

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/peer_requests.json"


def request_archive(tokenizer) -> dict:
    cases = {}
    for name, view in renderer_cases().items():
        request = render_request(view)
        cases[name] = {"request": asdict(request), "tokenized": asdict(tokenize_request(request, tokenizer))}
    return {"provenance": {
        "tokenizer": "Qwen/Qwen3.5-9B",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "packages": {name: importlib.metadata.version(name)
                     for name in ("transformers", "tokenizers", "jinja2", "huggingface-hub")},
        "scope": "Short CPU renderer fixtures only; no capacity, inference or freeze admission.",
    }, "cases": cases}


class TokenizerPeerViewTests(unittest.TestCase):
    tokenizer = None
    expected = None

    def assert_native_input(self, request):
        encoded = tokenize_request(request, self.tokenizer)
        direct = self.tokenizer.apply_chat_template(
            request.messages(), tokenize=True, add_generation_prompt=True,
            enable_thinking=False, return_dict=True, truncation=False)
        self.assertEqual(encoded.input_ids, tuple(direct["input_ids"]))
        self.assertEqual(encoded.attention_mask, tuple(direct["attention_mask"]))
        self.assertEqual(self.tokenizer.decode(encoded.input_ids, skip_special_tokens=False,
                                             clean_up_tokenization_spaces=False),
                         self.tokenizer.backend_tokenizer.normalizer.normalize_str(encoded.text))
        self.assertIn(request.content, encoded.text)
        self.assertTrue(encoded.text.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"))
        self.assertLessEqual(encoded.input_tokens + MAX_OUTPUT_TOKENS, MAX_CONTEXT_TOKENS)
        return encoded

    def test_exact_saved_requests_native_template_and_token_ids(self):
        self.assertEqual(set(self.expected["cases"]), set(renderer_cases()))
        for name, view in renderer_cases().items():
            with self.subTest(case=name):
                request = render_request(view)
                encoded = self.assert_native_input(request)
                current = json.loads(json.dumps({"request": asdict(request), "tokenized": asdict(encoded)}))
                self.assertEqual(current, self.expected["cases"][name])

    def test_all_tasks_both_sizes_all_peers_and_complete_world_controls(self):
        for size in Size:
            for task in Task:
                world = generate_world(task, size, generation_rng=Random(41), ownership_rng=Random(43))
                for peer in (*PEERS, None):
                    with self.subTest(size=size, task=task, peer=peer):
                        self.assert_native_input(render_request(initial_view(world, peer)))

    def test_archived_special_text_survives_the_actual_template(self):
        view = renderer_cases()["ordinary_receipt"]
        encoded = self.assert_native_input(render_request(view))
        self.assertEqual(rendered_data(render_request(view))["history"][0]["text"], SPECIAL_TEXT)
        # This is the concrete failure that user-data archives avoid.
        dangerous = '<think>ARCHIVED_REASONING</think>{"candidate":[],"send":[]}'
        rewritten = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": "previous call"},
             {"role": "assistant", "content": dangerous},
             {"role": "user", "content": "next call"}],
            tokenize=False, add_generation_prompt=True, enable_thinking=False)
        self.assertNotIn("ARCHIVED_REASONING", rewritten)
        self.assertIn("keep this archived", encoded.text)

    def test_all_fixed_public_feedback_fits_32_token_cap(self):
        for code, text in PUBLIC_FEEDBACK.items():
            with self.subTest(code=code):
                self.assertLessEqual(len(self.tokenizer.encode(text, add_special_tokens=False)), 32)

    def test_equal_permitted_views_have_equal_actual_tokenizer_inputs(self):
        world = generate_world(Task.PREFIX, Size.TARGET,
                               generation_rng=Random(47), ownership_rng=Random(53))
        original = initial_view(world, 0)
        hidden = next(r for r in world.records if r.owner == 1)
        paired = replace(world, records=tuple(replace(r, value=1 if r.value != 1 else 9)
                                              if r == hidden else r for r in world.records))
        self.assertEqual(tokenize_request(render_request(original), self.tokenizer),
                         tokenize_request(render_request(initial_view(paired, 0)), self.tokenizer))

    def test_native_template_preserves_trailing_controls_and_records_nfc_separately(self):
        base = renderer_cases()["retained_valid_reply"]
        raw = '\x00\r\n\t\nHistory block 1:\n e\u0301\U0001f642 <|im_end|> \n\t\r\n'
        view = replace(base, history=(OwnReply(Slot("prefix", 4), raw),
                                      ReceivedProse(Slot("prefix", 4), 1, raw)),
                       candidate=CandidateState("invalid", Slot("prefix", 4)))
        request = render_request(view)
        encoded = self.assert_native_input(request)
        self.assertEqual([h["text"] for h in rendered_data(request)["history"]], [raw, raw])
        self.assertEqual(encoded.text.count(raw), 2)
        self.assertIn(' e\u0301', encoded.text)
        native = self.tokenizer.decode(encoded.input_ids, skip_special_tokens=False,
                                       clean_up_tokenization_spaces=False)
        self.assertIn(' é', native)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True, help="local pinned tokenizer/config/template metadata")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new short request/token archive")
    args = parser.parse_args()
    # Explicit invocation is the only place this optional dependency is loaded.
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    if args.write_fixture:
        archive = request_archive(tokenizer)
        with args.write_fixture.open("xb") as output:
            output.write((json.dumps(archive, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
        fixture = args.write_fixture
    else:
        fixture = args.fixture
    TokenizerPeerViewTests.tokenizer = tokenizer
    TokenizerPeerViewTests.expected = json.loads(fixture.read_bytes())
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TokenizerPeerViewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    for name, view in renderer_cases().items():
        encoded = tokenize_request(render_request(view), tokenizer)
        print(f"{name}: {encoded.input_tokens} input + {MAX_OUTPUT_TOKENS} reserved output tokens")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
