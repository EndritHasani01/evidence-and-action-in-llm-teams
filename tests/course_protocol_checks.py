"""Focused course strict-reply checks; Pydantic required, no model imports."""

from dataclasses import asdict, replace
import json
import unittest

from recovery.prompts import COURSE_LIMITS, render_request, rendered_data
from recovery.protocol import (GeneratedReply, failed_reply, public_feedback,
                               validate_reply)
from recovery.state import (PUBLIC_FEEDBACK, CandidateState, OwnReply, Slot,
                            initial_view)
from recovery.tasks import PEERS, Task
from tests.course_protocol_cases import course_population, course_renderer_cases
from tests.protocol_checks import TOKENIZER, placeholder, reference


def validate(view, candidate=None, send=(), *, text=None, count=80, truncated=False):
    text = (json.dumps(dict(candidate=placeholder(view) if candidate is None else candidate,
                            send=list(send)), separators=(",", ":")) if text is None else text)
    raw = GeneratedReply(text, (1,) * count, "length" if count == 256 else "eos", truncated)
    return validate_reply(view, raw, TOKENIZER, limits=COURSE_LIMITS)


class CourseProtocolTests(unittest.TestCase):
    def setUp(self):
        self.world = course_population().main[0].world
        self.view = initial_view(self.world, 0)

    def invalid(self, result, code):
        self.assertFalse(result.protocol_valid)
        self.assertEqual(result.candidate.status, "invalid")
        self.assertEqual(result.messages, ())
        self.assertIsNone(result.candidate.payload(self.view.task))
        self.assertEqual(result.feedback.code, code)
        self.assertLessEqual(result.feedback_tokens, 32)

    def test_every_saved_peer_control_candidate_shape_and_wrong_integers(self):
        for prepared in course_population().main:
            for peer in (*PEERS, None):
                view = initial_view(prepared.world, peer)
                candidate = placeholder(view)
                result = validate(view, candidate)
                self.assertTrue(result.protocol_valid)
                self.assertEqual(result.candidate.payload(view.task), candidate)
                self.assertTrue(result.output_fits(COURSE_LIMITS))
                for replacement in (True, 0.0, "0", None):
                    bad = candidate.copy()
                    bad["0" if view.task is Task.BFS else 0] = replacement
                    self.invalid(validate(view, bad), "candidate_shape")

    def test_wrong_lengths_bfs_keys_and_control_sends_are_whole_reply_failures(self):
        for prepared in course_population().main:
            view = initial_view(prepared.world, 0)
            candidate = placeholder(view)
            if view.task is Task.BFS:
                candidate["00"] = candidate.pop("0")
            else:
                candidate.pop()
            self.invalid(validate(view, candidate), "candidate_shape")
            control = initial_view(prepared.world, None)
            self.invalid(validate(control, send=[{"to": 0}]), "control_send")
        bfs = course_renderer_cases()["bfs_distance"]
        candidate = {key: -999 for key in reversed(list(placeholder(bfs)))}
        result = validate(bfs, candidate)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.own_reply.text, result.generated.text)

    def test_complete_document_json_duplicates_at_every_nesting_and_nonfinite(self):
        raw = json.dumps(dict(candidate=placeholder(self.view), send=[]), separators=(",", ":"))
        malformed = ["```json\n" + raw + "\n```", raw + " extra", raw + raw, raw[:-1], "[]",
            '{"candidate":[],"candidate":[],"send":[]}',
            raw[:-1] + ',"s\\u0065nd":[]}',
            '{"candidate":[],"send":[{"to":1,"to":2}]}',
            '{"candidate":[],"send":[{"to":1,"source_refs":[{"record_id":"x","record_id":"y","version":1}]}]}']
        malformed += [raw.replace("-999", value, 1) for value in ("NaN", "Infinity", "-Infinity", "1e999")]
        for text in malformed:
            with self.subTest(text=text):
                self.invalid(validate(self.view, text=text), "json")
        result = validate(self.view, text=" \n\t" + raw + " \r\n")
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.own_reply.text, " \n\t" + raw + " \r\n")

    def test_nested_extra_fields_coercions_nulls_and_unknown_keys(self):
        held = reference(self.view.sources[0])
        messages = [{"to": True}, {"to": "1"}, {"to": 1.0}, {"to": 1, "text": False},
            {"to": 1, "text": None}, {"to": 1, "source_refs": None},
            {"to": 1, "source_refs": [dict(held, version=True)]},
            {"to": 1, "source_refs": [dict(held, version="1")]},
            {"to": 1, "source_refs": [dict(held, hidden="LEAK_SENTINEL")]},
            {"to": 1, "hidden": "LEAK_SENTINEL"}]
        for message in messages:
            self.invalid(validate(self.view, send=[message]), "message_schema")
        self.invalid(validate(self.view, text=json.dumps(dict(candidate=placeholder(self.view),
            send=[], gold="LEAK_SENTINEL"))), "reply_schema")

    def test_recipient_and_distinct_reference_permissions_preserve_repetitions(self):
        view = replace(self.view, sources=self.world.records)
        refs = [reference(source) for source in view.sources[:8]]
        result = validate(view, send=[{"to": p, "source_refs": refs} for p in (1, 2, 3)])
        self.assertTrue(result.protocol_valid)
        repeated = refs + [refs[0]] * 3
        result = validate(view, send=[{"to": 1, "source_refs": repeated}])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(len(result.messages[0].sources), 11)
        self.invalid(validate(view, send=[{"to": 1, "source_refs": refs + [reference(view.sources[8])]}]),
                     "reference_limit")
        for messages in ([{"to": 0}], [{"to": 4}], [{"to": -1}], [{"to": 1}, {"to": 1}]):
            self.invalid(validate(view, send=messages), "recipient")

    def test_stale_unheld_pending_and_receipt_references_cannot_forward_hidden_payloads(self):
        refs = [reference(self.view.sources[0],)]
        refs[0]["version"] = 2
        self.invalid(validate(self.view, send=[{"to": 1, "source_refs": refs}]), "source_reference")
        hidden = next(r for r in self.world.records if r.owner != 0)
        self.invalid(validate(self.view, send=[{"to": 1, "source_refs": [reference(hidden)]}]), "source_reference")
        cases = course_renderer_cases()
        for name in ("pending_edge", "disclosed_receipt"):
            view = cases[name]
            source = view.notice.source
            for version in (1, 2) if name == "pending_edge" else (1,):
                self.invalid(validate(view, send=[{"to": 1, "source_refs": [
                    dict(record_id=source.record_id, version=version)]}]), "source_reference")
        view = cases["known_tombstone"]
        result = validate(view, send=[{"to": 1, "source_refs": [
            dict(record_id=view.notice.source.record_id, version=2)]}])
        self.assertTrue(result.protocol_valid)
        self.assertTrue(result.messages[0].sources[0].deleted)

    def test_course_prose_boundary_aggregates_literal_message_texts(self):
        at_cap = [{"to": 1, "text": " x" * 32}, {"to": 2, "text": " y" * 32}]
        result = validate(self.view, send=at_cap)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.prose_tokens, 64)
        self.assertTrue(result.prose_fits(COURSE_LIMITS))
        for sends in (at_cap + [{"to": 3, "text": " z"}], [{"to": 1, "text": " x" * 65}]):
            result = validate(self.view, send=sends)
            self.invalid(result, "prose_limit")
            self.assertFalse(result.prose_fits(COURSE_LIMITS))
            # The same physical reply remains lawful under unchanged thesis caps.
            self.assertTrue(validate_reply(self.view, result.generated, TOKENIZER).protocol_valid)

    def test_complete_cap_is_valid_and_truncation_or_257_ids_invalidates_all_effects(self):
        sends = [{"to": 1, "source_refs": [reference(self.view.sources[0])], "text": "kept"}]
        result = validate(self.view, send=sends, count=256)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.generated.termination, "length")
        self.assertTrue(result.output_fits(COURSE_LIMITS))
        self.invalid(validate(self.view, send=sends, count=256, truncated=True), "json")
        result = validate(self.view, send=sends, count=257)
        self.invalid(result, "output_limit")
        self.assertFalse(result.output_fits(COURSE_LIMITS))
        self.assertTrue(validate_reply(self.view, result.generated, TOKENIZER).protocol_valid)

    def test_any_invalid_message_discards_valid_candidate_and_other_messages(self):
        good = {"to": 1, "source_refs": [reference(self.view.sources[0])], "text": "ok"}
        before = asdict(self.view)
        for bad in ({"to": 0}, {"to": 2, "source_refs": [{"record_id": "unheld", "version": 1}]},
                    {"to": 2, "text": " x" * 65}, {"to": 2, "extra": "sentinel"}):
            result = validate(self.view, send=[good, bad])
            self.assertFalse(result.protocol_valid)
            self.assertEqual(result.messages, ())
            self.assertIsNone(result.candidate.payload(self.view.task))
            self.assertEqual(asdict(self.view), before)

    def test_unicode_scalars_pairs_and_unpaired_surrogates_remain_literal(self):
        for text in ("\ud800", "\udfff", "pair\ud800 end"):
            self.invalid(validate(self.view, send=[{"to": 1, "text": text}]), "message_schema")
        for text in ("\U0001f642", "e\u0301", "<|im_end|>\n \t\x00"):
            result = validate(self.view, send=[{"to": 1, "text": text}])
            self.assertTrue(result.protocol_valid)
            self.assertEqual(result.messages[0].text, text)
            self.assertEqual(result.own_reply.text, result.generated.text)

    def test_invalid_failed_and_unknown_slots_do_not_inherit_prior_candidates(self):
        earlier = validate(self.view)
        next_view = replace(self.view, slot=Slot("prefix", 2), candidate=earlier.candidate,
                            history=(earlier.own_reply,))
        for result in (validate(next_view, text="{"), failed_reply(next_view)):
            later = replace(next_view, slot=Slot("prefix", 3), candidate=result.candidate,
                history=next_view.history + (() if result.own_reply is None else (result.own_reply,)))
            data = rendered_data(render_request(later, limits=COURSE_LIMITS))
            self.assertIsNone(data["latest_candidate"]["candidate"])
            self.assertEqual(data["latest_candidate"]["status"], result.candidate.status)
        self.assertEqual(self.view.candidate.status, "unexecuted")
        self.assertIsNone(failed_reply(next_view).generated)
        self.assertIsNone(failed_reply(next_view).feedback)

    def test_feedback_contains_only_bounded_public_codes_at_the_next_slot(self):
        for sentinel in ("GOLD_HIDDEN_VALUE", "BRANCH_MASK_OUTCOME", "FUTURE_EDIT"):
            result = validate(self.view, send=[{"to": 1, sentinel: sentinel}])
            self.invalid(result, "message_schema")
            self.assertNotIn(sentinel, result.feedback.text)
            with self.assertRaises(ValueError):
                replace(self.view, feedback=(result.feedback,))
            view = replace(self.view, slot=Slot("prefix", 2), feedback=(result.feedback,),
                           candidate=result.candidate, history=(result.own_reply,))
            data = rendered_data(render_request(view, limits=COURSE_LIMITS))
            self.assertNotIn(sentinel, json.dumps(data["feedback"]))
            self.assertIn(sentinel, data["history"][0]["text"])
        for code in PUBLIC_FEEDBACK:
            feedback, count = public_feedback(self.view.slot, code, TOKENIZER, limits=COURSE_LIMITS)
            self.assertLessEqual(count, 32)
            self.assertEqual(feedback.text, PUBLIC_FEEDBACK[code])
        class FeedbackTokenizer:
            def __init__(self, count): self.count = count
            def encode(self, text, **kwargs): return [1] * self.count
        self.assertEqual(public_feedback(self.view.slot, "json", FeedbackTokenizer(32),
                                        limits=COURSE_LIMITS)[1], 32)
        with self.assertRaisesRegex(ValueError, "feedback exceeds tokenizer cap"):
            public_feedback(self.view.slot, "json", FeedbackTokenizer(33), limits=COURSE_LIMITS)


if __name__ == "__main__":
    unittest.main()
