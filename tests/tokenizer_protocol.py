"""Explicit native-tokenizer CPU protocol checks and reproducible adversaries.

Run: python -m tests.tokenizer_protocol --tokenizer <local-metadata-directory>
No model weights, generation, GPU use, context-capacity or freeze admission.
"""

import argparse
from dataclasses import asdict, replace
import importlib.metadata
import json
from pathlib import Path
import unittest

from recovery.protocol import GeneratedReply, failed_reply, public_feedback, token_count, validate_reply
from recovery.state import PUBLIC_FEEDBACK
from recovery.tasks import PEERS, Size, Task
from tests.protocol_checks import placeholder, reference, world_view

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/protocol_replies.json"


def record(tokenizer, text, *, termination="eos", truncated=False):
    ids = tuple(tokenizer.encode(text, add_special_tokens=False))
    assert tokenizer.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False) == text
    return GeneratedReply(text, ids, termination, truncated)


def body(candidate, send=()):
    return json.dumps({"candidate": candidate, "send": list(send)}, ensure_ascii=True, separators=(",", ":"))


def padded_record(tokenizer, text, count, *, truncated=False):
    # Legal whitespace changes no reply content. In complete cases the final
    # closing brace is emitted at the cap, not before a trailing padding suffix.
    for n in range(2 * count):
        padded = text[:-1] + "\n " * n + "}" if text.endswith("}") else text + "\n " * n
        reply = record(tokenizer, padded, termination="length", truncated=truncated)
        if len(reply.token_ids) == count:
            return reply
    raise AssertionError(f"cannot construct {count}-token whitespace boundary")


def cases(tokenizer):
    _, view = world_view()
    candidate = placeholder(view)
    ref = reference(view.sources[0])
    values = {
        "wrong_but_valid": body(candidate),
        "duplicate_reply_key": '{"candidate":[],"candidate":[],"send":[]}',
        "duplicate_reference_key": '{"candidate":[],"send":[{"to":1,"source_refs":[{"record_id":"x000","version":1,"version":2}]}]}',
        "nonfinite_exponent": body(candidate).replace("-999", "1e400", 1),
        "boolean_candidate": body(candidate).replace("-999", "true", 1),
        "invalid_send_discards_candidate": body([0] * 8, [{"to": 1, "source_refs": [ref]}, {"to": 0}]),
        "stale_reference": body(candidate, [{"to": 1, "source_refs": [dict(ref, version=2)]}]),
        "repeated_lawful_reference": body(candidate, [{"to": 1, "source_refs": [ref, ref]}]),
        "prose_128": body(candidate, [{"to": 1, "text": " x" * 64}, {"to": 2, "text": " y" * 64}]),
        "prose_129": body(candidate, [{"to": 1, "text": " x" * 64}, {"to": 2, "text": " y" * 65}]),
        "literal_escaped_prose": body(candidate, [{"to": 1, "text": 'λ "quoted"\n\\ keep <|im_start|> literal'}]),
        "unexpected_special_marker": body(candidate) + "<|im_start|>",
        "malformed_below_cap": body(candidate)[:-1],
    }
    result = {name: (view, record(tokenizer, text)) for name, text in values.items()}
    result["complete_at_384"] = (view, padded_record(tokenizer, body(candidate), 384))
    result["complete_over_384"] = (view, padded_record(tokenizer, body(candidate), 385))
    result["incomplete_at_384"] = (view, padded_record(tokenizer, body(candidate)[:-1], 384, truncated=True))
    world, acquired = world_view()
    acquired = replace(acquired, sources=world.records)
    refs = [reference(r) for r in acquired.sources[:8]]
    result["eight_distinct_references"] = (acquired, record(tokenizer, body(candidate, [{"to": 1, "source_refs": refs}])))
    result["eight_distinct_nine_attempts"] = (acquired, record(tokenizer, body(candidate, [{"to": 1, "source_refs": refs + [refs[0]]}])))
    result["nine_distinct_references"] = (acquired, record(tokenizer, body(candidate, [{"to": 1, "source_refs": refs + [reference(acquired.sources[8])]}])))
    result["failed_slot"] = (view, None)
    return result


def reply_archive(tokenizer):
    return {"provenance": {
        "tokenizer": "Qwen/Qwen3.5-9B",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "packages": {name: importlib.metadata.version(name) for name in
                     ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        "scope": "Scripted strict replies and literal tokenizer caps only; no model/capacity/freeze admission.",
    }, "cases": {name: asdict(failed_reply(view) if generated is None
                             else validate_reply(view, generated, tokenizer))
                 for name, (view, generated) in cases(tokenizer).items()}}


class TokenizerProtocolTests(unittest.TestCase):
    tokenizer = None
    expected = None

    def test_exact_saved_adversaries_raw_ids_stages_candidates_messages_and_feedback(self):
        actual = json.loads(json.dumps(reply_archive(self.tokenizer)))
        self.assertEqual(actual["cases"], self.expected["cases"])
        self.assertEqual(actual["provenance"]["tokenizer"], self.expected["provenance"]["tokenizer"])
        self.assertEqual(actual["provenance"]["revision"], self.expected["provenance"]["revision"])
        for name, (view, generated) in cases(self.tokenizer).items():
            with self.subTest(case=name):
                result = failed_reply(view) if generated is None else validate_reply(view, generated, self.tokenizer)
                if generated is not None:
                    self.assertEqual(result.generated, generated)
                    self.assertEqual(result.own_reply.text, generated.text)
                if not result.protocol_valid:
                    self.assertIsNone(result.candidate.value)
                    self.assertEqual(result.messages, ())
                if result.feedback is not None:
                    self.assertLessEqual(result.feedback_tokens, 32)
                    self.assertEqual(result.feedback_tokens, token_count(result.feedback.text, self.tokenizer))

    def test_every_family_size_peer_and_complete_world_candidate_shape_fits_output(self):
        for task in Task:
            for size in Size:
                for peer in (*PEERS, None):
                    _, view = world_view(task, size, peer)
                    generated = record(self.tokenizer, body(placeholder(view)))
                    with self.subTest(task=task, size=size, peer=peer):
                        result = validate_reply(view, generated, self.tokenizer)
                        self.assertTrue(result.protocol_valid)
                        self.assertLessEqual(result.output_tokens, 384)
                        self.assertEqual(result.messages, ())

    def test_prose_is_literal_and_aggregated_128_vs_129_actual_tokens(self):
        scripted = cases(self.tokenizer)
        for name, expected_count, valid in (("prose_128", 128, True), ("prose_129", 129, False)):
            view, generated = scripted[name]
            result = validate_reply(view, generated, self.tokenizer)
            self.assertEqual(result.prose_tokens, expected_count)
            self.assertEqual(result.protocol_valid, valid)
            self.assertTrue(result.output_within_limit)
            if not valid:
                self.assertEqual(result.feedback.code, "prose_limit")
        view, generated = scripted["literal_escaped_prose"]
        result = validate_reply(view, generated, self.tokenizer)
        self.assertTrue(result.protocol_valid)
        literal = json.loads(generated.text)["send"][0]["text"]
        self.assertEqual(result.messages[0].text, literal)
        self.assertEqual(result.prose_tokens, len(self.tokenizer.encode(literal, add_special_tokens=False)))
        self.assertIn("<|im_start|>", literal)
        result = validate_reply(view, record(self.tokenizer, body(placeholder(view),
                                [{"to": 1, "text": "a"}, {"to": 2, "text": "b"}])), self.tokenizer)
        self.assertEqual(result.prose_tokens, token_count("a", self.tokenizer) + token_count("b", self.tokenizer))
        self.assertNotEqual(result.prose_tokens, token_count("ab", self.tokenizer))

    def test_complete_and_incomplete_cap_stops_and_unexpected_markers(self):
        scripted = cases(self.tokenizer)
        for name, count, valid, code in (("complete_at_384", 384, True, None),
                                         ("complete_over_384", 385, False, "output_limit"),
                                         ("incomplete_at_384", 384, False, "json")):
            view, generated = scripted[name]
            result = validate_reply(view, generated, self.tokenizer)
            self.assertEqual(result.output_tokens, count)
            self.assertEqual(result.generated.termination, "length")
            self.assertEqual(result.generated.truncated, name == "incomplete_at_384")
            self.assertEqual(result.protocol_valid, valid)
            self.assertEqual(result.feedback.code if result.feedback else None, code)
            if result.json_valid:
                self.assertTrue(generated.text.endswith("}"))
        view, generated = scripted["unexpected_special_marker"]
        self.assertFalse(validate_reply(view, generated, self.tokenizer).protocol_valid)
        # Blanket special-token stripping would silently change this raw output.
        stripped = self.tokenizer.decode(generated.token_ids, skip_special_tokens=True,
                                         clean_up_tokenization_spaces=False)
        self.assertNotEqual(stripped, generated.text)
        self.assertTrue(validate_reply(view, record(self.tokenizer, stripped), self.tokenizer).protocol_valid)

    def test_repeated_lawful_references_preserve_every_attempt(self):
        view, generated = cases(self.tokenizer)["repeated_lawful_reference"]
        result = validate_reply(view, generated, self.tokenizer)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.messages[0].sources, (view.sources[0], view.sources[0]))
        for name, distinct, attempts, valid in (("eight_distinct_references", 8, 8, True),
                                               ("eight_distinct_nine_attempts", 8, 9, True),
                                               ("nine_distinct_references", 9, 9, False)):
            view, generated = cases(self.tokenizer)[name]
            result = validate_reply(view, generated, self.tokenizer)
            self.assertTrue(result.output_within_limit)
            self.assertEqual(result.protocol_valid, valid)
            if valid:
                self.assertEqual(len(result.messages[0].sources), attempts)
                self.assertEqual(len(set(result.messages[0].sources)), distinct)
            else:
                self.assertEqual(result.feedback.code, "reference_limit")

    def test_every_fixed_public_feedback_fits_actual_32_token_limit(self):
        _, view = world_view()
        for code in PUBLIC_FEEDBACK:
            with self.subTest(code=code):
                feedback, count = public_feedback(view.slot, code, self.tokenizer)
                self.assertEqual(feedback.text, PUBLIC_FEEDBACK[code])
                self.assertEqual(count, len(self.tokenizer.encode(feedback.text, add_special_tokens=False)))
                self.assertLessEqual(count, 32)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True, help="local pinned tokenizer metadata only")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new adversarial reply archive")
    args = parser.parse_args()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    current = reply_archive(tokenizer)
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write((json.dumps(current, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
        fixture = args.write_fixture
    else:
        fixture = args.fixture
    TokenizerProtocolTests.tokenizer = tokenizer
    TokenizerProtocolTests.expected = json.loads(fixture.read_bytes())
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TokenizerProtocolTests))
    for name, value in current["cases"].items():
        generated = value["generated"]
        count = None if generated is None else len(generated["token_ids"])
        print(f"{name}: output={count}, prose={value['prose_tokens']}, "
              f"feedback={value['feedback_tokens']}, candidate={value['candidate']['status']}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
