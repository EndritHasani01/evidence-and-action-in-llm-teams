"""CPU protocol adversaries; Pydantic 2 required, no inference dependencies.

Run explicitly with `python -m unittest tests.protocol_checks -v`, or as part of
`python -m recovery validate`. Core-only discovery intentionally excludes this
module so the pre-existing dependency-free mathematical checks remain usable.
Real tokenizer checks live in the explicitly invoked tokenizer_protocol harness.
"""

from dataclasses import asdict, replace
import json
from pathlib import Path
from random import Random
import subprocess
import sys
import unittest

from recovery.prompts import render_request
from recovery.protocol import (GeneratedReply, failed_reply, public_feedback,
                               token_count, validate_reply)
from recovery.state import (PUBLIC_FEEDBACK, CandidateState, OwnReply, PeerView,
                            PendingSource, RevisionNotice, Slot, initial_view)
from recovery.tasks import PEERS, PublicSource, Size, Task, candidate_contract, generate_world
from recovery.truth import exact_candidate, solve_world


class WordTokenizer:
    """Injected counter for stage/limit unit cases, not tokenizer admission."""

    def encode(self, text, *, add_special_tokens):
        assert add_special_tokens is False
        return list(range(len(text.split())))


TOKENIZER = WordTokenizer()
ROOT = Path(__file__).resolve().parent.parent


def world_view(task=Task.PREFIX, size=Size.TARGET, peer=0):
    world = generate_world(task, size, generation_rng=Random(31), ownership_rng=Random(37))
    return world, initial_view(world, peer)


def placeholder(view):
    coords = candidate_contract(view.task, view.size, view.peer).coordinates
    return {str(j): -999 for j in coords} if view.task is Task.BFS else [-999] * len(coords)


def reference(source, **changes):
    return dict(record_id=source.record_id, version=source.version, **changes)


def recorded(text, count=None, termination="eos", truncated=False):
    # Explicitly injected physical IDs let CPU tests distinguish physical counts
    # from retokenizing text. Native tests supply actual Qwen token IDs.
    ids = tuple(TOKENIZER.encode(text, add_special_tokens=False)) if count is None else (1,) * count
    return GeneratedReply(text, ids, termination, truncated)


def validate_data(view, candidate=None, send=None, **recording):
    data = {"candidate": placeholder(view) if candidate is None else candidate,
            "send": [] if send is None else send}
    text = json.dumps(data, separators=(",", ":"))
    return validate_reply(view, recorded(text, **recording), TOKENIZER)


class StrictReplyTests(unittest.TestCase):
    def setUp(self):
        self.world, self.view = world_view()

    def assert_invalid(self, result, code):
        self.assertFalse(result.protocol_valid)
        self.assertEqual(result.candidate.status, "invalid")
        self.assertEqual(result.candidate.slot, self.view.slot)
        self.assertIsNone(result.candidate.value)
        self.assertEqual(result.messages, ())
        self.assertEqual(result.feedback.code, code)
        self.assertEqual(result.feedback.text, PUBLIC_FEEDBACK[code])
        self.assertLessEqual(result.feedback_tokens, 32)
        self.assertEqual(result.own_reply.text, result.generated.text)

    def test_unpaired_message_surrogates_reject_whole_reply_before_token_count(self):
        class ScalarTokenizer(WordTokenizer):
            def encode(self, text, *, add_special_tokens):
                text.encode("utf-8")
                return super().encode(text, add_special_tokens=add_special_tokens)

        before = asdict(self.view)
        for literal in ("\ud800", "\udfff", "a\ud800b", "\ud800\ud800", "\udfff\ud800"):
            with self.subTest(literal=ascii(literal)):
                text = json.dumps({"candidate": placeholder(self.view), "send": [
                    {"to": 1, "source_refs": [reference(self.view.sources[0])], "text": "legal"},
                    {"to": 2, "text": literal}]}, ensure_ascii=True)
                raw = recorded(text)
                result = validate_reply(self.view, raw, ScalarTokenizer())
                self.assert_invalid(result, "message_schema")
                self.assertTrue(result.json_valid)
                self.assertFalse(result.schema_valid)
                self.assertIsNone(result.prose_tokens)
                self.assertEqual(result.generated, raw)
                self.assertEqual(asdict(self.view), before)

    def test_scalar_prose_including_valid_escaped_pairs_is_not_normalized_or_repaired(self):
        literal = '\x00\t\n"\\e\u0301\U0001f642 <|im_start|>'
        text = json.dumps({"candidate": placeholder(self.view),
                           "send": [{"to": 1, "text": literal}]}, ensure_ascii=True)
        self.assertIn("\\ud83d\\ude42", text)
        result = validate_reply(self.view, recorded(text), TOKENIZER)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.messages[0].text, literal)
        self.assertEqual(result.generated.text, text)

    def test_complete_document_only_no_repair_or_fragment_extraction(self):
        body = json.dumps({"candidate": placeholder(self.view), "send": []})
        for text in ("", " ", "null", "[]", "1", '"object"',
                     "```json\n" + body + "\n```", "prefix " + body, body + " trailing",
                     body + body, body[:-1], body + ",", '\ufeff' + body,
                     body.replace('"send": []', '"send": [],'),
                     body + "<|im_start|>", body + "<|im_end|>"):
            with self.subTest(text=text):
                result = validate_reply(self.view, recorded(text), TOKENIZER)
                self.assert_invalid(result, "json")
                self.assertFalse(result.json_valid)
                self.assertIsNone(result.schema_valid)
        spaced = " \r\n\t" + body + "\t\n "
        result = validate_reply(self.view, recorded(spaced), TOKENIZER)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.generated.text, spaced)

    def test_duplicate_keys_recursively_including_decoded_key_collisions(self):
        cases = (
            '{"candidate":[],"candidate":[],"send":[]}',
            '{"candidate":[],"ca\\u006edidate":[],"send":[]}',
            '{"candidate":[],"send":[],"send":[]}',
            '{"candidate":{"0":1,"0":2},"send":[]}',
            '{"candidate":[],"send":[{"to":1,"to":2}]}',
            '{"candidate":[],"send":[{"to":1,"text":"a","text":"b"}]}',
            '{"candidate":[],"send":[{"to":1,"source_refs":[],"source_refs":[]}]}',
            '{"candidate":[],"send":[{"to":1,"source_refs":[{"record_id":"x000","record_id":"x001","version":1}]}]}',
            '{"candidate":[],"send":[{"to":1,"source_refs":[{"record_id":"x000","version":1,"version":2}]}]}',
            '{"candidate":[],"send":[],"extra":{"deep":[{"a":1,"a":2}]}}',
        )
        for text in cases:
            with self.subTest(text=text):
                result = validate_reply(self.view, recorded(text), TOKENIZER)
                self.assert_invalid(result, "json")
                self.assertFalse(result.json_valid)

    def test_nonfinite_constants_and_exponent_overflow_at_any_depth(self):
        for value in ("NaN", "Infinity", "-Infinity", "1e400", "-1e400", "1e9999999999"):
            for text in ('{"candidate":[' + value + '],"send":[]}',
                         '{"candidate":[],"send":[{"to":1,"source_refs":[{"record_id":"x000","version":' + value + '}]}]}',
                         '{"candidate":[],"send":[],"unknown":{"deep":[' + value + ']}}'):
                with self.subTest(value=value, text=text):
                    self.assert_invalid(validate_reply(self.view, recorded(text), TOKENIZER), "json")
        # Finite exponent forms still cannot be coerced to integers, even when
        # floating-point underflow would round the token to integral zero.
        for value in ("1.0", "1e0", "1e-400", "-0.0"):
            text = '{"candidate":[' + ','.join([value] * 8) + '],"send":[]}'
            result = validate_reply(self.view, recorded(text), TOKENIZER)
            self.assertTrue(result.json_valid)
            self.assert_invalid(result, "candidate_shape")

    def test_overlarge_integer_decoder_failure_is_recorded_and_valid_big_ints_stay_literal(self):
        text = '{"candidate":[' + '9' * 5000 + '],"send":[]}'
        self.assert_invalid(validate_reply(self.view, recorded(text), TOKENIZER), "json")
        value = 10**200
        result = validate_data(self.view, [value] * 8)
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.candidate.payload(self.view.task), [value] * 8)

    def test_required_outer_fields_exact_types_and_extra_fields(self):
        data = {"candidate": placeholder(self.view), "send": []}
        for bad in ({}, {"candidate": data["candidate"]}, {"send": []},
                    dict(data, extra=1), dict(data, send={}), dict(data, send=None)):
            with self.subTest(bad=bad):
                result = validate_reply(self.view, recorded(json.dumps(bad)), TOKENIZER)
                self.assertTrue(result.json_valid)
                self.assertFalse(result.schema_valid)
                self.assertIsNone(result.permissions_valid)
                self.assert_invalid(result, "reply_schema")

    def test_integer_types_shapes_and_wrong_lengths_all_families_sizes_and_controls(self):
        for task in Task:
            for size in Size:
                for peer in (*PEERS, None):
                    _, view = world_view(task, size, peer)
                    good = placeholder(view)
                    self.assertTrue(validate_data(view, good).protocol_valid)
                    for value in (True, 1.0, "1", None, [1], {"x": 1}):
                        bad = dict(good) if task is Task.BFS else list(good)
                        bad["0" if task is Task.BFS else 0] = value
                        with self.subTest(task=task, size=size, peer=peer, value=value):
                            result = validate_data(view, bad)
                            self.assertFalse(result.protocol_valid)
                            self.assertEqual(result.feedback.code, "candidate_shape")
                    bads = ([good[:-1], good + [0], {"0": 1}] if task is not Task.BFS
                            else [list(good.values()), {k: v for k, v in good.items() if k != "0"}])
                    for bad in bads:
                        self.assertFalse(validate_data(view, bad).protocol_valid)

    def test_bfs_exact_canonical_full_keys_order_independent_no_raw_sorting(self):
        for size in Size:
            _, view = world_view(Task.BFS, size)
            good = {str(j): -1 for j in reversed(range(size.node_count))}
            result = validate_data(view, good)
            self.assertTrue(result.protocol_valid)
            self.assertEqual(result.candidate.payload(Task.BFS), good)
            self.assertIn('"candidate":{"' + str(size.node_count - 1) + '":', result.generated.text)
            for replacement in ("01", "+1", "1.0", " 1", "١", "unknown"):
                bad = dict(good)
                bad[replacement] = bad.pop("1")
                self.assertEqual(validate_data(view, bad).feedback.code, "candidate_shape")
            self.assertFalse(validate_data(view, dict(good, extra=0)).protocol_valid)

    def test_control_requires_complete_candidate_and_empty_sends(self):
        for task in Task:
            for size in Size:
                world, control = world_view(task, size, None)
                self.assertTrue(validate_data(control).protocol_valid)
                result = validate_data(control, send=[{"to": 0}])
                self.assertEqual(result.feedback.code, "control_send")
                self.assertEqual(result.messages, ())
                if task in (Task.PREFIX, Task.SORT):
                    shard = solve_world(world).candidate(0)
                    self.assertEqual(validate_data(control, shard).feedback.code, "candidate_shape")

    def test_nested_schemas_extra_fields_coercions_and_explicit_nulls(self):
        source = self.view.sources[0]
        ref = reference(source)
        cases = [{"to": 1, "extra": "hidden"}, {"to": True}, {"to": 1.0}, {"to": "1"},
                 {"text": "missing recipient"}, {"to": 1, "text": None},
                 {"to": 1, "text": 1}, {"to": 1, "text": {}},
                 {"to": 1, "source_refs": None}, {"to": 1, "source_refs": ref},
                 {"to": 1, "source_refs": [dict(ref, extra=1)]}]
        for field, values in (("record_id", (True, 1, None)), ("version", (True, 1.0, "1", None))):
            for value in values:
                bad = dict(ref)
                bad[field] = value
                cases.append({"to": 1, "source_refs": [bad]})
        cases += [{"to": 1, "source_refs": [{"record_id": source.record_id}]},
                  {"to": 1, "source_refs": [{"version": 1}]}, None, [], 1]
        for message in cases:
            with self.subTest(message=message):
                self.assert_invalid(validate_data(self.view, send=[message]), "message_schema")
        for message in ({"to": 1}, {"to": 1, "source_refs": []}, {"to": 1, "text": ""}):
            self.assertTrue(validate_data(self.view, send=[message]).protocol_valid)
        self.assertIsNone(validate_data(self.view, send=[{"to": 1}]).messages[0].text)
        self.assertEqual(validate_data(self.view, send=[{"to": 1, "text": ""}]).messages[0].text, "")

    def test_recipient_permissions_uniqueness_and_three_message_maximum(self):
        for send in ([{"to": 0}], [{"to": -1}], [{"to": 4}], [{"to": 999}],
                     [{"to": 1}, {"to": 1}], [{"to": 1}, {"to": 2}, {"to": 3}, {"to": 1}]):
            self.assert_invalid(validate_data(self.view, send=send), "recipient")
        result = validate_data(self.view, send=[{"to": i} for i in (3, 1, 2)])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(tuple(m.recipient for m in result.messages), (3, 1, 2))

    def test_sources_are_resolved_only_against_held_current_sender_records(self):
        held = self.view.sources[0]
        remote = next(r for r in self.world.records if r.owner == 1)
        for ref in (reference(remote), dict(record_id="unknown", version=1),
                    dict(record_id=held.record_id, version=2),
                    dict(record_id=held.record_id, version=0),
                    dict(record_id=held.record_id, version=-1)):
            self.assert_invalid(validate_data(self.view, send=[{"to": 1, "source_refs": [ref]}]), "source_reference")
        replacement = replace(held, version=2, value=(held.value + 1) % 20)
        public = PublicSource(held.record_id, held.owner, held.position)
        revised = replace(self.view, sources=tuple(replacement if r == held else r for r in self.view.sources),
                          notice=RevisionNotice(public, 1, 2), source_deliveries=())
        self.assertFalse(validate_data(revised, send=[{"to": 1, "source_refs": [reference(held)]}]).protocol_valid)
        result = validate_data(revised, send=[{"to": 1, "source_refs": [reference(replacement)]}])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.messages[0].sources, (replacement,))
        pending = PendingSource(held.record_id, held.owner, held.position, 2)
        unknown = replace(revised, sources=tuple(pending if r == replacement else r for r in revised.sources))
        self.assertFalse(validate_data(unknown, send=[{"to": 1, "source_refs": [reference(replacement)]}]).protocol_valid)

    def test_known_tombstone_is_forwardable_but_pending_endpoints_are_not_revealed(self):
        _, view = world_view(Task.BFS)
        edge = view.sources[0]
        tombstone = replace(edge, version=2, deleted=True)
        view = replace(view, sources=tuple(tombstone if r == edge else r for r in view.sources),
                       notice=RevisionNotice(PublicSource(edge.record_id, edge.owner, None), 1, 2),
                       source_deliveries=())
        result = validate_data(view, send=[{"to": 1, "source_refs": [reference(tombstone)]}])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.messages[0].sources, (tombstone,))
        self.assertTrue(result.messages[0].sources[0].deleted)

    def test_distinct_reference_limit_is_per_recipient_and_repetitions_are_preserved(self):
        view = replace(self.view, sources=self.world.records)
        refs = [reference(r) for r in view.sources[:8]]
        result = validate_data(view, send=[{"to": to, "source_refs": refs} for to in (1, 2, 3)])
        self.assertTrue(result.protocol_valid)
        self.assertEqual([len(m.sources) for m in result.messages], [8, 8, 8])
        repeated = refs + [refs[0]] * 4
        result = validate_data(view, send=[{"to": 1, "source_refs": repeated}])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.messages[0].sources, view.sources[:8] + (view.sources[0],) * 4)
        for extras in (refs + [reference(view.sources[8])], repeated + [reference(view.sources[8])]):
            self.assert_invalid(validate_data(view, send=[{"to": 1, "source_refs": extras}]), "reference_limit")
        # Repetition never legalizes an unheld/stale reference.
        stale = dict(record_id=view.sources[0].record_id, version=2)
        self.assert_invalid(validate_data(view, send=[{"to": 1, "source_refs": [stale] * 9}]), "source_reference")

    def test_prose_limit_sums_each_literal_message_without_json_escaping(self):
        result = validate_data(self.view, send=[{"to": 1, "text": " x" * 64}, {"to": 2, "text": " y" * 64}])
        self.assertTrue(result.protocol_valid)
        self.assertEqual(result.prose_tokens, 128)
        self.assertTrue(result.prose_within_limit)
        for send in ([{"to": 1, "text": " x" * 128}, {"to": 2, "text": " y"}],
                     [{"to": 1, "text": " x" * 64}, {"to": 2, "text": " y" * 65}]):
            result = validate_data(self.view, send=send)
            self.assert_invalid(result, "prose_limit")
            self.assertEqual(result.prose_tokens, 129)
            self.assertTrue(result.permissions_valid)
            self.assertFalse(result.prose_within_limit)
        text = 'quoted "text"\nnew\tline \\ unicode λ'
        result = validate_data(self.view, send=[{"to": 1, "text": text}])
        self.assertEqual(result.messages[0].text, text)
        self.assertEqual(result.prose_tokens, token_count(text, TOKENIZER))

    def test_output_uses_physical_ids_and_complete_cap_ending_json_is_valid(self):
        for count in (383, 384):
            result = validate_data(self.view, count=count, termination="length")
            self.assertTrue(result.protocol_valid)
            self.assertEqual(result.output_tokens, count)
            self.assertEqual(result.generated.termination, "length")
            self.assertFalse(result.generated.truncated)
        result = validate_data(self.view, count=385, termination="eos")
        self.assert_invalid(result, "output_limit")
        self.assertTrue(result.json_valid and result.schema_valid and result.permissions_valid)
        self.assertFalse(result.output_within_limit)
        self.assertLess(token_count(result.generated.text, TOKENIZER), result.output_tokens)
        for count in (12, 384):
            for termination in ("eos", "length"):
                for text in ('{"candidate":[', '{"candidate":bad}', 'no json'):
                    self.assert_invalid(validate_reply(self.view, recorded(text, count, termination), TOKENIZER), "json")
        result = validate_data(self.view, truncated=True)
        self.assert_invalid(result, "json")
        self.assertTrue(result.json_valid)
        self.assertTrue(result.generated.truncated)

    def test_any_invalid_send_discards_the_correct_candidate_and_every_message(self):
        gold = solve_world(self.world).candidate(0)
        lawful = {"to": 1, "source_refs": [reference(self.view.sources[0])], "text": "use current sources"}
        for bad in ({"to": 0}, {"to": 2, "source_refs": [{"record_id": "unheld", "version": 1}]},
                    {"to": 2, "text": " x" * 129}, {"to": 2, "extra": 1}):
            result = validate_data(self.view, gold, [lawful, bad])
            self.assertFalse(result.protocol_valid)
            self.assertIsNone(result.candidate.value)
            self.assertEqual(result.messages, ())
            self.assertFalse(exact_candidate(solve_world(self.world), gold, 0, protocol_valid=result.protocol_valid))

    def test_wrong_unsorted_duplicate_and_negative_integers_remain_valid_unrepaired(self):
        for task in Task:
            world, view = world_view(task)
            wrong = placeholder(view)
            if task is not Task.BFS:
                wrong[:3] = [999, -3, 999]
            result = validate_data(view, wrong)
            self.assertTrue(result.protocol_valid)
            self.assertEqual(result.candidate.payload(task), wrong)
            self.assertFalse(exact_candidate(solve_world(world), wrong, 0, protocol_valid=True))
            self.assertIsNone(result.feedback)
            self.assertEqual(result.feedback_tokens, 0)

    def test_invalid_and_failed_latest_slots_never_inherit_earlier_candidates(self):
        old = validate_data(self.view)
        view = replace(self.view, slot=Slot("prefix", 2), history=(old.own_reply,), candidate=old.candidate)
        invalid = validate_reply(view, recorded('bad raw\n<|im_start|>'), TOKENIZER)
        next_view = replace(view, slot=Slot("prefix", 3), history=view.history + (invalid.own_reply,),
                            candidate=invalid.candidate, feedback=(invalid.feedback,))
        payload = json.loads(render_request(next_view).content.split("\nPeer data (JSON):\n")[1])
        self.assertEqual(payload["latest_candidate"]["status"], "invalid")
        self.assertIsNone(payload["latest_candidate"]["candidate"])
        self.assertEqual(payload["history"][0]["text"], old.generated.text)
        self.assertEqual(payload["history"][1]["text"], invalid.generated.text)
        # Feedback and replies cannot be exposed during their generating slot.
        with self.assertRaises(ValueError):
            replace(view, candidate=invalid.candidate, feedback=(invalid.feedback,))
        failed = failed_reply(view)
        self.assertEqual(failed.candidate.status, "failed")
        self.assertIsNone(failed.candidate.value)
        self.assertNotEqual(failed.candidate, CandidateState())
        self.assertIsNone(failed.generated)
        self.assertIsNone(failed.own_reply)
        self.assertIsNone(failed.feedback)
        self.assertIsNone(failed.json_valid)
        self.assertIsNone(failed.output_tokens)
        self.assertEqual(failed.messages, ())
        after_failure = replace(view, slot=Slot("prefix", 3), candidate=failed.candidate)
        self.assertIsNone(after_failure.candidate.payload(self.view.task))

    def test_validation_is_pure_repeatable_and_preserves_exact_raw_archive(self):
        text = ' \n{"send":[{"text":"raw \\u03bb \\n", "to":1}], "candidate":[-3,2,2,1,8,1,0,0]}\n '
        before = asdict(self.view)
        generated = recorded(text)
        first = validate_reply(self.view, generated, TOKENIZER)
        second = validate_reply(self.view, generated, TOKENIZER)
        self.assertTrue(first.protocol_valid)
        self.assertEqual(first, second)
        self.assertEqual(asdict(self.view), before)
        self.assertEqual(first.generated, generated)
        self.assertEqual(first.own_reply, OwnReply(self.view.slot, text))

    def test_feedback_is_fixed_public_and_never_echoes_supplied_sentinels(self):
        sentinel = 'HIDDEN_472193_FUTURE_GOLD_POLICY_secret'
        bodies = ('{"candidate":[],"send":[],"' + sentinel + '":1}',
                  '{"candidate":[],"candidate":"' + sentinel + '","send":[]}',
                  json.dumps({"candidate": placeholder(self.view), "send": [{"to": 1, "text": {sentinel: 1}}]}),
                  json.dumps({"candidate": placeholder(self.view), "send": [{"to": 1, "source_refs": [{"record_id": sentinel, "version": 1}]}]}))
        for text in bodies:
            result = validate_reply(self.view, recorded(text), TOKENIZER)
            self.assertFalse(result.protocol_valid)
            self.assertNotIn(sentinel, result.feedback.text)
            self.assertNotIn("validation error", result.feedback.text.lower())
            self.assertEqual(result.feedback_tokens, token_count(result.feedback.text, TOKENIZER))
            self.assertEqual(result.generated.text, text)
        for code in PUBLIC_FEEDBACK:
            feedback, count = public_feedback(self.view.slot, code, TOKENIZER)
            self.assertEqual(feedback.text, PUBLIC_FEEDBACK[code])
            self.assertLessEqual(count, 32)

    def test_feedback_token_overflow_and_bad_tokenizers_are_configuration_errors(self):
        class TooLong:
            def encode(self, text, **kwargs):
                return [1] * 33
        with self.assertRaisesRegex(ValueError, "feedback exceeds"):
            validate_reply(self.view, recorded("bad"), TooLong())
        class BadIds:
            def encode(self, text, **kwargs):
                return [True]
        with self.assertRaisesRegex(ValueError, "integer sequence"):
            token_count("text", BadIds())

    def test_malformed_host_inputs_do_not_become_model_protocol_failures(self):
        for ids in ([1], (True,), (-1,), (1.0,)):
            with self.assertRaises(ValueError):
                GeneratedReply("text", ids, "eos")
        with self.assertRaises(ValueError):
            validate_reply(self.world, recorded("{}"), TOKENIZER)
        with self.assertRaises(ValueError):
            failed_reply(self.world)
        with self.assertRaises(ValueError):
            validate_reply(self.view, "{}", TOKENIZER)

    def test_protocol_import_and_validation_without_model_stack_or_global_rng_effects(self):
        script = '''
import importlib.abc
import random
import sys
blocked = {"torch", "transformers", "accelerate", "bitsandbytes", "langgraph",
           "langchain", "numpy", "scipy", "pandas", "matplotlib"}
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("unexpected model dependency: " + fullname)
sys.meta_path.insert(0, BlockImports())
state = random.getstate()
from tests.protocol_checks import TOKENIZER, world_view, validate_data
_, view = world_view()
assert validate_data(view).protocol_valid
assert random.getstate() == state
assert not any(name.split(".")[0] in blocked for name in sys.modules)
'''
        result = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
