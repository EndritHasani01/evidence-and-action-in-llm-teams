"""Course limits across exact settings, CPU adapter doubles and durable records."""

from dataclasses import asdict
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.events import start_continuation
from recovery.inference import (QWEN_4B, TRANSPORT_ID, TransformersBackend,
                                candidate_settings, decode_suffix)
from recovery.prompts import COURSE_LIMITS, THESIS_LIMITS, limits_from_settings, render_request, tokenize_request
from recovery.protocol import GeneratedReply, validate_reply
from recovery.replay import obtain_continuation_round
from recovery.rounds import initial_branch, prefix_snapshot, run_round
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.state import initial_view
from recovery.tasks import Task
from tests.course_protocol_cases import course_population
from tests.inference_mocks import (Tokenizer, Torch, Qwen3_5ForCausalLM, mock_transformers)
from tests.protocol_checks import placeholder


def raw(view, *, count=256):
    return GeneratedReply(json.dumps(dict(candidate=placeholder(view), send=[]),
                                    separators=(",", ":")), (1,) * count, "length")


class CourseSettingsTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.settings = candidate_settings(self.tokenizer, QWEN_4B, limits=COURSE_LIMITS)
        self.world = next(w for w in course_population().main if w.world.task is Task.SORT)
        self.branches = _prepare_branches((self.world,))
        self.prefix = next(b for b in self.branches if b.phase == "prefix")

    def test_course_settings_record_all_limits_while_both_thesis_models_keep_defaults(self):
        self.assertEqual(self.settings["model"], "Qwen/Qwen3.5-4B")
        self.assertEqual(self.settings["revision"], "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
        self.assertEqual(self.settings["protocol_limits"], asdict(COURSE_LIMITS))
        self.assertEqual(self.settings["generation"]["max_new_tokens"], 256)
        self.assertEqual(limits_from_settings(self.settings), COURSE_LIMITS)
        for settings in (candidate_settings(self.tokenizer), candidate_settings(self.tokenizer, QWEN_4B)):
            self.assertNotIn("protocol_limits", settings)
            self.assertEqual(settings["generation"]["max_new_tokens"], 384)
            self.assertEqual(limits_from_settings(settings), THESIS_LIMITS)
        with self.assertRaisesRegex(ValueError, "pinned 4B"):
            candidate_settings(self.tokenizer, limits=COURSE_LIMITS)

    def test_suffix_complete_at_256_is_valid_and_transport_removal_is_exact(self):
        view = initial_view(self.world.world, 0)
        text = raw(view).text
        text = text[:-1] + " " * (256 - len(text)) + "}"
        ids = tuple(map(ord, text))
        reply, suffix = decode_suffix(self.tokenizer, ids, limits=COURSE_LIMITS)
        self.assertEqual(reply.text, text)
        self.assertEqual(suffix, text)
        self.assertEqual(reply.termination, "length")
        self.assertTrue(validate_reply(view, reply, self.tokenizer, limits=COURSE_LIMITS).protocol_valid)
        ids = tuple(map(ord, raw(view).text)) + (TRANSPORT_ID,)
        reply, suffix = decode_suffix(self.tokenizer, ids, limits=COURSE_LIMITS)
        self.assertEqual(reply.text, raw(view).text)
        self.assertEqual(suffix, reply.text + "<|im_end|>")
        for ids in ((1,) * 257, (1,) * 255, ()):
            with self.assertRaises(ValueError):
                decode_suffix(self.tokenizer, ids, limits=COURSE_LIMITS)

    def test_cpu_backend_double_uses_course_generation_and_rejects_mismatched_request_settings(self):
        model = Qwen3_5ForCausalLM()
        view = initial_view(self.world.world, 0)
        model.reply_ids = tuple(map(ord, raw(view).text)) + (TRANSPORT_ID,)
        backend = TransformersBackend(Torch(), model, self.tokenizer, QWEN_4B, {}, limits=COURSE_LIMITS)
        request = render_request(view, limits=COURSE_LIMITS)
        tokens = tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
        with patch.dict(sys.modules, transformers=mock_transformers()):
            for settings, rendered, tokenized in (
                    (candidate_settings(self.tokenizer, QWEN_4B), request, tokens),
                    (self.settings, render_request(view), tokenize_request(render_request(view), self.tokenizer))):
                with self.assertRaises(ValueError):
                    backend(view, rendered, tokenized, seed=11, settings=settings)
            self.assertEqual(model.calls, [])
            result = backend(view, request, tokens, seed=11, settings=self.settings)
        self.assertEqual(model.calls[0]["config"]["max_new_tokens"], 256)
        self.assertTrue(result.backend["cache"]["initial_empty"])
        self.assertTrue(validate_reply(view, result.response, self.tokenizer, limits=COURSE_LIMITS).protocol_valid)

    def test_scripted_round_uses_real_course_renderer_and_whole_reply_validation(self):
        def provide(view, rendered, tokenized):
            self.assertEqual(rendered, render_request(view, limits=COURSE_LIMITS))
            self.assertEqual(tokenized, tokenize_request(rendered, self.tokenizer, limits=COURSE_LIMITS))
            return None if view.peer == 3 else raw(view, count=257 if view.peer == 1 else 256)
        state = initial_branch(self.world.world, self.prefix.branch_id)
        result = run_round(state, self.tokenizer, provide, limits=COURSE_LIMITS)
        self.assertEqual([p.candidate.status for p in result.committed.peers],
                         ["valid", "invalid", "valid", "failed"])
        self.assertEqual(state.peers[0].candidate.status, "unexecuted")
        self.assertEqual(result.barrier.replies[1].feedback.code, "output_limit")

    def test_durable_course_prefix_resume_and_full_information_controls_share_exact_limits(self):
        seen = []
        def provide(view, rendered, tokenized, *, seed, settings):
            seen.append(view.peer)
            self.assertEqual(settings, self.settings)
            self.assertEqual(rendered, render_request(view, limits=COURSE_LIMITS))
            return raw(view, count=257 if view.peer == 1 else 256)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            with DurableRunner(path, self.tokenizer, provide, scripted=True) as runner:
                runner.start(self.world, self.prefix, settings=self.settings)
                original = runner.run_round(self.prefix.branch_id, 1)
            def forbidden(*args, **kwargs):
                raise AssertionError("recorded response must not be regenerated")
            with DurableRunner(path, self.tokenizer, forbidden, scripted=True) as runner:
                resumed = runner.run_round(self.prefix.branch_id, 1)
                self.assertEqual(original, resumed)
                saved = runner.store.saved_round(self.prefix.branch_id, 1, self.tokenizer)
                self.assertEqual(json.loads(saved.settings_json), self.settings)
                self.assertFalse(saved.barrier.replies[1].output_fits(COURSE_LIMITS))
                self.assertEqual(saved.barrier.replies[1].candidate.status, "invalid")
            with DurableRunner(path, self.tokenizer, provide, scripted=True) as runner:
                for branch in self.branches:
                    if branch.phase == "control":
                        self.assertTrue(runner.run_control(self.world, branch, settings=self.settings).protocol_valid)
        self.assertEqual(seen, [0, 1, 2, 3, None, None])

    def test_replay_rejects_thesis_settings_before_provider_or_effects(self):
        state = initial_branch(self.world.world, self.prefix.branch_id)
        for _ in range(4):
            state = run_round(state, self.tokenizer, lambda v, r, t: raw(v), limits=COURSE_LIMITS).committed
        snapshot = prefix_snapshot(state)
        parent = next(b for b in self.branches if b.event == "revision" and b.policy == "B")
        q = next(b for b in self.branches if b.event == "revision" and b.policy == "Q_B")
        saved = obtain_continuation_round(start_continuation(snapshot, self.world, parent), parent,
            self.tokenizer, lambda v, r, t, **kw: raw(v), settings=self.settings)
        state = start_continuation(snapshot, self.world, q)
        before = asdict(state)
        def forbidden(*args, **kwargs):
            raise AssertionError("replay must consume the exact parent")
        replay = obtain_continuation_round(state, q, self.tokenizer, forbidden,
            settings=self.settings, parents=(saved,))
        self.assertEqual(replay.barrier.replies, saved.barrier.replies)
        with self.assertRaisesRegex(ValueError, "equality failed"):
            obtain_continuation_round(state, q, self.tokenizer, forbidden,
                settings=candidate_settings(self.tokenizer, QWEN_4B), parents=(saved,))
        self.assertEqual(asdict(state), before)


if __name__ == "__main__":
    unittest.main()
