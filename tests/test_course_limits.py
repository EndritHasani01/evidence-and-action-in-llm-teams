"""Dependency-free course rendering/reservation and exact settings checks."""

from dataclasses import asdict, replace
import unittest

from recovery.prompts import (COMMON_INSTRUCTION, COURSE_LIMITS, THESIS_LIMITS,
                              ProtocolLimits, limits_from_settings, render_request,
                              rendered_data, tokenize_request)
from recovery.state import initial_view
from recovery.tasks import PEERS, Size, Task, candidate_contract
from tests.course_protocol_cases import course_population, course_renderer_cases
from tests.test_peer_views import RecordingTokenizer


class CourseLimitsTests(unittest.TestCase):
    def test_only_adopted_uniform_limits_are_available(self):
        self.assertEqual(asdict(COURSE_LIMITS), dict(output_tokens=256, prose_tokens=64,
            context_tokens=262144, recipients=3, distinct_references=8, feedback_tokens=32))
        for changes in (dict(output_tokens=255), dict(prose_tokens=63),
                        dict(context_tokens=32768), dict(recipients=2),
                        dict(distinct_references=6), dict(feedback_tokens=16),
                        dict(recipients=3.0), dict(output_tokens=True)):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(COURSE_LIMITS, **changes)

    def test_all_saved_course_peer_and_control_shapes_keep_the_same_task_hints(self):
        for prepared in course_population().main:
            hints = set()
            for peer in (*PEERS, None):
                view = initial_view(prepared.world, peer)
                thesis = render_request(view)
                course = render_request(view, limits=COURSE_LIMITS)
                self.assertTrue(thesis.content.startswith(COMMON_INSTRUCTION))
                self.assertEqual(course.content, thesis.content.replace(
                    "at most 128 tokenizer", "at most 64 tokenizer", 1).replace(
                    "reply limit is 384 tokens", "reply limit is 256 tokens", 1))
                data = rendered_data(course)
                self.assertEqual(data, rendered_data(thesis))
                contract = candidate_contract(view.task, Size.FALLBACK, peer)
                self.assertEqual(data["public"]["output_coordinates"], list(contract.coordinates))
                hints.add(data["public"]["hint"])
                self.assertNotIn("regime", data["public"])
                if peer is None:
                    self.assertEqual(data["public"]["communication"], "send must be an empty list")
            self.assertEqual(len(hints), 1)
        with self.assertRaisesRegex(ValueError, "fallback mathematical size"):
            from tests.peer_view_cases import renderer_cases
            render_request(renderer_cases()["retained_valid_reply"], limits=COURSE_LIMITS)

    def test_course_reservation_uses_all_256_tokens_and_rejects_without_truncating(self):
        request = render_request(next(iter(course_renderer_cases().values())), limits=COURSE_LIMITS)
        maximum = COURSE_LIMITS.context_tokens - COURSE_LIMITS.output_tokens
        for count in (maximum, maximum + 1):
            tokenizer = RecordingTokenizer(count)
            if count == maximum:
                result = tokenize_request(request, tokenizer, limits=COURSE_LIMITS)
                self.assertEqual(result.input_tokens + 256, 262144)
            else:
                with self.assertRaisesRegex(ValueError, "no truncation permitted"):
                    tokenize_request(request, tokenizer, limits=COURSE_LIMITS)
            self.assertFalse(tokenizer.encode_calls[-1][1]["truncation"])
        # The old reserve remains 384 even on the same mathematical size.
        with self.assertRaisesRegex(ValueError, "full output reserve"):
            tokenize_request(request, RecordingTokenizer(maximum))

    def test_lossless_history_footer_and_genuine_receipts_have_no_extra_source_authority(self):
        cases = course_renderer_cases()
        for name, view in cases.items():
            request = render_request(view, limits=COURSE_LIMITS)
            data = rendered_data(request)
            self.assertTrue(request.content.endswith("\nEnd peer data."))
            for entry, shown in zip(view.history, data["history"]):
                self.assertEqual(shown["text"], entry.text)
            if "receipt" in name:
                self.assertEqual(data["historical_receipt"]["before_value"],
                    "not included in this receipt" if view.receipt.before_value is None else view.receipt.before_value)
        a, b = (rendered_data(render_request(cases[name], limits=COURSE_LIMITS))
                for name in ("ordinary_receipt", "disclosed_receipt"))
        a["historical_receipt"]["before_value"] = b["historical_receipt"]["before_value"]
        self.assertEqual(a, b)
        self.assertTrue(any(source.get("status") == "deleted" for source in rendered_data(
            render_request(cases["known_tombstone"], limits=COURSE_LIMITS))["current_sources"]))

    def test_hidden_source_values_and_endpoints_do_not_influence_requests(self):
        for prepared in course_population().main:
            world = prepared.world
            for peer in PEERS:
                hidden = [i for i, r in enumerate(world.records) if r.owner != peer]
                records = list(world.records)
                first, second = hidden[:2]
                records[first] = replace(records[first], value=world.records[second].value)
                records[second] = replace(records[second], value=world.records[first].value)
                other = replace(world, records=tuple(records))
                self.assertEqual(render_request(initial_view(world, peer), limits=COURSE_LIMITS),
                                 render_request(initial_view(other, peer), limits=COURSE_LIMITS))
            with self.assertRaisesRegex(ValueError, "permitted PeerView"):
                render_request(prepared, limits=COURSE_LIMITS)

    def test_exact_settings_select_limits_and_reject_omission_or_contradiction(self):
        self.assertEqual(limits_from_settings({}), THESIS_LIMITS)
        self.assertEqual(limits_from_settings({"max_new_tokens": 384}), THESIS_LIMITS)
        course = {"protocol_limits": asdict(COURSE_LIMITS), "generation": {"max_new_tokens": 256},
                  "max_context_tokens": 262144}
        self.assertEqual(limits_from_settings(course), COURSE_LIMITS)
        for bad in ({"generation": {"max_new_tokens": 256}}, {"protocol_limits": None},
                    {"protocol_limits": {"output_tokens": 256}},
                    dict(course, generation={"max_new_tokens": 384}),
                    dict(course, max_context_tokens=32768),
                    dict(course, max_new_tokens=256.0)):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                limits_from_settings(bad)


if __name__ == "__main__":
    unittest.main()
