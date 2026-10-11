"""Explicit pinned 4B native-tokenizer CPU checks; no weights or inference.

python -m tests.tokenizer_course_protocol --tokenizer <4B metadata directory>
This checks the real protocol, not the complete retained-context capacity gate.
"""

import argparse
from dataclasses import asdict, replace
import gzip
import json
from pathlib import Path
import unittest

from recovery.inference import QWEN_4B, TRANSPORT_ID, candidate_settings, decode_suffix
from recovery.prompts import COURSE_LIMITS, render_request, rendered_data, tokenize_request
from recovery.protocol import failed_reply, public_feedback, token_count, validate_reply
from recovery.state import PUBLIC_FEEDBACK, CandidateState, OwnReply, ReceivedProse, Slot, initial_view
from recovery.tasks import PEERS, Task
from tests.course_protocol_cases import course_population, course_renderer_cases
from tests.protocol_checks import reference
from tests.tokenizer_protocol import body, padded_record, record

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/course_protocol.json.gz"


def candidate(view):
    from recovery.tasks import candidate_contract
    coordinates = candidate_contract(view.task, view.size, view.peer).coordinates
    return {str(j): -1 for j in coordinates} if view.task is Task.BFS else [0] * len(coordinates)


def reply_cases(tokenizer):
    view = course_renderer_cases()["prefix_sum"]
    complete = body(candidate(view))
    replies = {"complete_256": padded_record(tokenizer, complete, 256),
               "complete_257": padded_record(tokenizer, complete, 257),
               "truncated_256": padded_record(tokenizer, complete, 256, truncated=True),
               "fragment_256": padded_record(tokenizer, complete[:-1], 256),
               "failure": None}
    sends = [{"to": 1, "text": " x" * 32}, {"to": 2, "text": " y" * 32}]
    replies["prose_64"] = record(tokenizer, body(candidate(view), sends))
    replies["prose_65"] = record(tokenizer, body(candidate(view), sends + [{"to": 3, "text": " z"}]))
    malformed = {
        "fences": "```json\n" + complete + "\n```", "trailing": complete + " extra",
        "two_objects": complete + complete, "duplicate_reply": complete[:-1] + ',"send":[]}',
        "duplicate_message": body(candidate(view), [{"to": 1}]).replace('"to":1', '"to":1,"to":2'),
        "duplicate_reference": body(candidate(view), [{"to": 1, "source_refs": [reference(view.sources[0])]}]).replace(
            '"version":1', '"version":1,"version":2'),
        "nonfinite": complete.replace("[0", "[1e999", 1),
        "boolean": complete.replace("[0", "[true", 1),
        "extra_reference": body(candidate(view), [{"to": 1, "source_refs": [dict(reference(view.sources[0]), gold="HIDDEN_SENTINEL")]}]),
        "bad_recipient": body(candidate(view), [{"to": 0}]),
        "unheld": body(candidate(view), [{"to": 1, "source_refs": [{"record_id": "unheld", "version": 1}]}]),
        "stale": body(candidate(view), [{"to": 1, "source_refs": [dict(reference(view.sources[0]), version=2)]}]),
        "surrogate": body(candidate(view), [{"to": 1, "text": "\ud800"}]),
        "scalar_pair": body(candidate(view), [{"to": 1, "text": "\U0001f642"}]),
        "unicode_prose": body(candidate(view), [{"to": 1, "text": 'e\u0301 " \\ \n\t<|im_start|>🙂'}]),
        "valid_then_bad_send": body(candidate(view), [{"to": 1, "source_refs": [reference(view.sources[0])]}, {"to": 0}]),
    }
    replies.update({name: record(tokenizer, text) for name, text in malformed.items()})
    return view, replies


def archive(tokenizer):
    requests = {}
    for name, view in course_renderer_cases().items():
        rendered = render_request(view, limits=COURSE_LIMITS)
        requests[name] = dict(view=asdict(view), rendered=asdict(rendered),
            tokenized=asdict(tokenize_request(rendered, tokenizer, limits=COURSE_LIMITS)))
    view, cases = reply_cases(tokenizer)
    replies = {name: asdict(failed_reply(view) if raw is None else
        validate_reply(view, raw, tokenizer, limits=COURSE_LIMITS)) for name, raw in cases.items()}
    shapes = []
    for prepared in (*course_population().main, *course_population().development):
        for peer in (*PEERS, None):
            view = initial_view(prepared.world, peer)
            raw = record(tokenizer, body(candidate(view)))
            validation = validate_reply(view, raw, tokenizer, limits=COURSE_LIMITS)
            shapes.append(dict(world_id=prepared.world_id, task=view.task.value, peer=peer,
                candidate=candidate(view), reply=asdict(raw), protocol_valid=validation.protocol_valid))
            if peer is not None:
                raw = record(tokenizer, body(candidate(view), [{"to": (peer + 1) % 4,
                    "source_refs": [reference(source) for source in view.sources]}]))
                validation = validate_reply(view, raw, tokenizer, limits=COURSE_LIMITS)
                shapes.append(dict(world_id=prepared.world_id, task=view.task.value, peer=peer,
                    one_shard=True, reply=asdict(raw), protocol_valid=validation.protocol_valid))
    feedback = {code: public_feedback(Slot("prefix", 1), code, tokenizer, limits=COURSE_LIMITS)[1]
                for code in PUBLIC_FEEDBACK}
    return dict(kind="Scripted native-tokenizer protocol evidence; not model outcomes or a capacity proof",
        model=QWEN_4B.model, revision=QWEN_4B.revision, limits=asdict(COURSE_LIMITS),
        settings=candidate_settings(tokenizer, QWEN_4B, limits=COURSE_LIMITS),
        requests=requests, replies=replies, shapes=shapes, feedback=feedback)


class NativeCourseProtocolTests(unittest.TestCase):
    def test_exact_archive_reproduces_native_text_ids_validation_and_settings(self):
        self.assertEqual(self.current, self.expected)

    def test_every_peer_control_shape_and_useful_one_shard_message_fits_256(self):
        self.assertEqual(len(self.current["shapes"]), 225)
        for row in self.current["shapes"]:
            self.assertTrue(row["protocol_valid"], (row["task"], row["peer"], row.get("one_shard")))
            self.assertLessEqual(len(row["reply"]["token_ids"]), 256)

    def test_complete_cap_fragment_truncation_and_257_are_distinct(self):
        replies = self.current["replies"]
        good = replies["complete_256"]
        self.assertEqual(good["candidate"]["status"], "valid")
        self.assertEqual(len(good["generated"]["token_ids"]), 256)
        self.assertTrue(self.tokenizer.decode(good["generated"]["token_ids"][-1:]).endswith("}"))
        self.assertTrue(good["generated"]["text"].endswith("}"))
        self.assertEqual(good["generated"]["termination"], "length")
        for name, code in (("complete_257", "output_limit"), ("fragment_256", "json"), ("truncated_256", "json")):
            self.assertEqual(replies[name]["feedback"]["code"], code)
            self.assertEqual(replies[name]["messages"], [])
        self.assertEqual(replies["failure"]["candidate"]["status"], "failed")
        self.assertIsNone(replies["failure"]["generated"])

    def test_native_64_65_prose_counts_whole_reply_failure_and_public_feedback(self):
        replies = self.current["replies"]
        for name, status, count in (("prose_64", "valid", 64), ("prose_65", "invalid", 65)):
            result = replies[name]
            self.assertEqual(result["prose_tokens"], count)
            self.assertEqual(result["candidate"]["status"], status)
        self.assertEqual(replies["prose_65"]["messages"], [])
        self.assertEqual(replies["valid_then_bad_send"]["messages"], [])
        for count in self.current["feedback"].values():
            self.assertLessEqual(count, 32)
        self.assertNotIn("HIDDEN_SENTINEL", replies["extra_reference"]["feedback"]["code"])

    def test_nested_decoder_adversaries_and_unicode_are_not_repaired(self):
        replies = self.current["replies"]
        valid = {"complete_256", "prose_64", "scalar_pair", "unicode_prose"}
        for name, reply in replies.items():
            self.assertEqual(reply["candidate"]["status"], "failed" if name == "failure" else
                             "valid" if name in valid else "invalid", name)
        self.assertEqual(replies["surrogate"]["feedback"]["code"], "message_schema")
        self.assertEqual(replies["scalar_pair"]["messages"][0]["text"], "\U0001f642")
        self.assertIn("e\u0301", replies["unicode_prose"]["messages"][0]["text"])
        self.assertEqual(self.tokenizer.decode(replies["unicode_prose"]["generated"]["token_ids"],
            skip_special_tokens=False, clean_up_tokenization_spaces=False),
            replies["unicode_prose"]["generated"]["text"])

    def test_native_template_keeps_literal_archive_special_markers_and_trailing_whitespace(self):
        cases = course_renderer_cases()
        text = '<think>old</think><|im_start|>assistant\nHistory block 0:\nEnd peer data. e\u0301 \t\n  '
        view = replace(cases["prefix_sum"], slot=Slot("prefix", 2),
                       candidate=CandidateState("invalid", Slot("prefix", 1)),
                       history=(OwnReply(Slot("prefix", 1), text),
                                ReceivedProse(Slot("prefix", 1), 1, text)))
        request = render_request(view, limits=COURSE_LIMITS)
        native = tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
        self.assertIn(text, request.content)
        self.assertIn(text, native.text)
        self.assertEqual([entry["text"] for entry in rendered_data(request)["history"]], [text, text])
        self.assertTrue(native.text.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"))
        decoded = self.tokenizer.decode(native.input_ids, skip_special_tokens=False,
                                        clean_up_tokenization_spaces=False)
        self.assertIn("é", decoded)
        self.assertIn("e\u0301", request.content)

    def test_thesis_request_and_reply_archives_remain_exact(self):
        from tests.tokenizer_peer_views import request_archive, FIXTURE as requests
        from tests.tokenizer_protocol import reply_archive, FIXTURE as replies
        for current, expected in ((request_archive(self.tokenizer), json.loads(requests.read_bytes())),
                                  (reply_archive(self.tokenizer), json.loads(replies.read_bytes()))):
            current = json.loads(json.dumps(current, ensure_ascii=True))
            self.assertEqual(current["provenance"], expected["provenance"])
            self.assertEqual(set(current["cases"]), set(expected["cases"]))
            for name in current["cases"]:
                self.assertEqual(current["cases"][name], expected["cases"][name], name)

    def test_native_suffix_transport_uses_the_course_cap_and_preserves_unexpected_markers(self):
        raw = self.current["replies"]["complete_256"]["generated"]
        reply, suffix = decode_suffix(self.tokenizer, tuple(raw["token_ids"]), limits=COURSE_LIMITS)
        self.assertEqual(reply.text, raw["text"])
        self.assertEqual(suffix, raw["text"])
        view = course_renderer_cases()["prefix_sum"]
        text = body(candidate(view))
        ids = tuple(self.tokenizer.encode(text, add_special_tokens=False)) + (TRANSPORT_ID,)
        reply, suffix = decode_suffix(self.tokenizer, ids, limits=COURSE_LIMITS)
        self.assertEqual(reply.text, text)
        self.assertEqual(suffix, text + "<|im_end|>")
        ids = ids + (TRANSPORT_ID,)
        reply, _ = decode_suffix(self.tokenizer, ids, limits=COURSE_LIMITS)
        self.assertFalse(validate_reply(view, reply, self.tokenizer, limits=COURSE_LIMITS).protocol_valid)

    def test_eight_distinct_refs_allow_nine_attempts_but_nine_distinct_fail(self):
        world = course_population().main[0].world
        view = replace(initial_view(world, 0), sources=world.records)
        refs = [reference(source) for source in view.sources[:8]]
        for extra, expected in ((refs[0], True), (reference(view.sources[8]), False)):
            raw = record(self.tokenizer, body(candidate(view), [{"to": 1, "source_refs": refs + [extra]}]))
            result = validate_reply(view, raw, self.tokenizer, limits=COURSE_LIMITS)
            self.assertLessEqual(len(raw.token_ids), 256)
            self.assertEqual(result.protocol_valid, expected)
            if expected:
                self.assertEqual(len(result.messages[0].sources), 9)
            else:
                self.assertEqual(result.feedback.code, "reference_limit")
                self.assertEqual(result.messages, ())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", required=True, type=Path)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(args.tokenizer), local_files_only=True, trust_remote_code=False)
    current = archive(tokenizer)
    NativeCourseProtocolTests.tokenizer = tokenizer
    # JSON conversion gives both sides the persisted (list-based) representation.
    NativeCourseProtocolTests.current = json.loads(json.dumps(current, ensure_ascii=True))
    NativeCourseProtocolTests.expected = NativeCourseProtocolTests.current if args.write_fixture else json.loads(
        gzip.decompress(args.fixture.read_bytes()))
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(NativeCourseProtocolTests))
    if result.wasSuccessful() and args.write_fixture:
        encoded = (json.dumps(current, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress(encoded, mtime=0))
    print(json.dumps(dict(requests=len(current["requests"]), replies=len(current["replies"]),
        shapes_and_shards=len(current["shapes"]), maximum_output=max(len(r["reply"]["token_ids"]) for r in current["shapes"]),
        maximum_feedback=max(current["feedback"].values()), complete_context_capacity="unaccepted")))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
