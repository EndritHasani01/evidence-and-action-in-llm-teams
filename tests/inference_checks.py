"""Exact decoding, state/RNG isolation and subprocess-to-ledger CPU integration."""

from dataclasses import replace
from contextlib import closing
import gc
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.attempts import MeasuredReply, ProcessProvider, ProviderDefect
from recovery.inference import (PAD_ID, TRANSPORT_ID, candidate_settings, decode_suffix)
from recovery.prompts import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS, render_request, tokenize_request
from recovery.protocol import validate_reply
from recovery.runner import DurableRunner
from recovery.state import initial_view
from tests.durable_checks import prefix_branch, forbidden
from tests.event_checks import case_world
from tests.inference_mocks import Tokenizer, backend, mock_transformers, process_backend
from recovery.tasks import Task


class DecodingTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.view = initial_view(case_world(Task.PREFIX).world, 0)
        self.valid = '{"candidate":[0,0,0,0,0,0,0,0],"send":[]}'

    def decode(self, text, *, terminal=True):
        ids = tuple(map(ord, text)) + ((TRANSPORT_ID,) if terminal else ())
        if not terminal:
            ids += (32,) * (MAX_OUTPUT_TOKENS - len(ids))
        return decode_suffix(self.tokenizer, ids)

    def test_final_transport_is_removed_once_and_ids_raw_text_remain_exact(self):
        reply, raw = self.decode(self.valid)
        self.assertEqual(reply.text, self.valid)
        self.assertEqual(raw, self.valid + "<|im_end|>")
        self.assertEqual(reply.token_ids[-1], TRANSPORT_ID)
        self.assertTrue(validate_reply(self.view, reply, self.tokenizer).protocol_valid)

    def test_internal_special_markers_and_unexpected_suffix_are_never_normalized(self):
        for text in ("<think>" + self.valid, self.valid + "extra", self.valid + "<|im_start|>",
                     self.valid + "<|im_end|>", self.valid + "<|endoftext|>", self.valid[:-1]):
            with self.subTest(text=text):
                reply, raw = self.decode(text)
                self.assertEqual(reply.text, text)
                self.assertEqual(raw, text + "<|im_end|>")
                self.assertFalse(validate_reply(self.view, reply, self.tokenizer).protocol_valid)
        # A genuine internal special-token ID survives, even with a final frame.
        ids = tuple(map(ord, self.valid)) + (TRANSPORT_ID, TRANSPORT_ID)
        reply, raw = decode_suffix(self.tokenizer, ids)
        self.assertEqual(reply.text, self.valid + "<|im_end|>")
        self.assertFalse(validate_reply(self.view, reply, self.tokenizer).protocol_valid)

    def test_endoftext_eos_is_preserved_for_strict_validation(self):
        reply, raw = decode_suffix(self.tokenizer, tuple(map(ord, self.valid)) + (PAD_ID,))
        self.assertEqual(reply.termination, "eos")
        self.assertTrue(reply.text.endswith("<|endoftext|>"))
        self.assertEqual(reply.text, raw)
        self.assertFalse(validate_reply(self.view, reply, self.tokenizer).protocol_valid)

    def test_full_valid_json_at_exact_cap_is_accepted_and_incomplete_is_invalid(self):
        for text, valid in ((self.valid, True), (self.valid[:-1], False), (self.valid + "extra", False)):
            reply, raw = self.decode(text, terminal=False)
            self.assertEqual(len(reply.token_ids), 384)
            self.assertEqual(reply.termination, "length")
            self.assertFalse(reply.truncated)
            self.assertEqual(raw, reply.text)
            self.assertEqual(validate_reply(self.view, reply, self.tokenizer).protocol_valid, valid)

    def test_unexplained_short_stop_overlong_ids_and_empty_generation_fail(self):
        for ids in ((), (1,), (True, TRANSPORT_ID), (-1, TRANSPORT_ID), (1,) * 385):
            with self.assertRaises(ValueError):
                decode_suffix(self.tokenizer, ids)


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.backend = backend()
        self.tokenizer = self.backend.tokenizer
        self.view = initial_view(case_world(Task.PREFIX).world, 0)
        self.rendered = render_request(self.view)
        self.tokenized = tokenize_request(self.rendered, self.tokenizer)
        self.settings = candidate_settings(self.tokenizer)
        self.modules = patch.dict(sys.modules, transformers=mock_transformers())
        self.modules.start()
        self.addCleanup(self.modules.stop)

    def call(self, *, seed=31, **kwargs):
        return self.backend(kwargs.get("view", self.view), kwargs.get("rendered", self.rendered),
            kwargs.get("tokenized", self.tokenized), seed=seed, settings=kwargs.get("settings", self.settings))

    def test_one_exact_unpadded_prompt_fresh_cache_and_saved_cpu_cuda_seed(self):
        measured = self.call()
        self.assertEqual(measured.backend["seed"], 31)
        self.assertEqual(measured.backend["cpu_seed"], 31)
        self.assertEqual(measured.backend["cuda_seed"], 31)
        self.assertEqual(measured.backend["cache"], dict(calls=1, initial_empty=True, same_call_cache=True, disposed_after_call=True))
        self.assertEqual(measured.peak_memory_bytes, 750)
        call = self.backend.model.calls[0]
        self.assertEqual(call["inputs"], [list(self.tokenized.input_ids)])
        self.assertIsNone(call["cache"]())
        self.assertNotIn("stopping_criteria", call["kwargs"])
        self.assertFalse(call["config"]["remove_invalid_values"])

    def test_prior_calls_order_and_reconstructed_backend_do_not_retain_state_or_rng(self):
        a = self.call(seed=31)
        self.call(seed=99)
        repeated = self.call(seed=31)
        fresh = backend()
        self.assertEqual(a.response, repeated.response)
        other = fresh(self.view, self.rendered, self.tokenized, seed=31, settings=self.settings)
        self.assertEqual(a.response, other.response)
        self.assertEqual([c["seed"] for c in self.backend.model.calls], [31, 99, 31])
        gc.collect()
        self.assertTrue(all(c["cache"]() is None for c in self.backend.model.calls + fresh.model.calls))
        self.assertEqual(self.backend.model.hooks, [])

    def test_generation_exception_disposes_cache_hooks_and_serial_flag(self):
        self.backend.model.fail = True
        with self.assertRaises(ValueError):
            self.call()
        gc.collect()
        self.assertFalse(self.backend.active)
        self.assertEqual(self.backend.model.hooks, [])
        self.assertIsNone(self.backend.model.calls[0]["cache"]())

    def test_nonfinite_scores_stop_without_sanitization(self):
        self.backend.torch.finite = False
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            self.call()
        self.assertFalse(self.backend.active)

    def test_empty_and_same_call_cache_checks_fail_before_using_stale_state(self):
        transformers = mock_transformers()
        def stale_cache(**kwargs):
            cache = transformers.DynamicCache(**kwargs)
            cache.recurrent = True
            return cache
        from types import SimpleNamespace
        with patch.dict(sys.modules, transformers=SimpleNamespace(
                DynamicCache=stale_cache, GenerationConfig=transformers.GenerationConfig, LogitsProcessorList=list)), \
                self.assertRaisesRegex(ValueError, "empty"):
            self.call()
        self.assertEqual(self.backend.model.calls, [])
        original = self.backend.model.generate
        def different_cache(**kwargs):
            kwargs["past_key_values"] = transformers.DynamicCache(config=self.backend.model.config)
            return original(**kwargs)
        self.backend.model.generate = different_cache
        with self.assertRaisesRegex(ValueError, "unowned cache"):
            self.call()
        self.assertFalse(self.backend.active)
        self.assertEqual(self.backend.model.hooks, [])

    def test_changed_prompt_prefix_or_unexplained_early_stop_is_an_adapter_defect(self):
        original = self.backend.model.generate
        def wrong_prefix(**kwargs):
            output = original(**kwargs)
            output.sequences.data[0][0] += 1
            return output
        self.backend.model.generate = wrong_prefix
        with self.assertRaisesRegex(ValueError, "exact prompt"):
            self.call()
        self.backend.model.generate = original
        self.backend.model.reply_ids = (32,)
        with self.assertRaisesRegex(ValueError, "early stop"):
            self.call()
        self.assertFalse(self.backend.active)

    def test_unsavable_backend_measurements_are_rejected_before_transmission(self):
        measured = self.call()
        for evidence in (dict(value=float("nan")), dict(value=object()), []):
            with self.assertRaises((ValueError, TypeError)):
                MeasuredReply(measured.response, 1, evidence)

    def test_process_and_concurrent_rng_ownership_and_seed_types(self):
        for seed in (-1, True, 2**63, "31"):
            with self.assertRaises(ValueError):
                self.call(seed=seed)
        self.backend.active = True
        with self.assertRaises(ValueError):
            self.call()
        self.backend.active = False
        with patch("recovery.inference.os.getpid", return_value=self.backend.pid + 1), self.assertRaises(ValueError):
            self.call()
        self.assertEqual(self.backend.model.calls, [])

    def test_overflow_or_changed_view_ids_mask_template_settings_fail_before_generation(self):
        overflow = replace(self.tokenized, input_ids=(1,) * (MAX_CONTEXT_TOKENS - MAX_OUTPUT_TOKENS + 1))
        for kwargs in (dict(tokenized=overflow), dict(tokenized=replace(self.tokenized, text="changed template")),
                       dict(tokenized=replace(self.tokenized, input_ids=(1,))),
                       dict(tokenized=replace(self.tokenized, attention_mask=(0,))),
                       dict(rendered=replace(self.rendered, content="other request")),
                       dict(view=replace(self.view, peer=1)),
                       dict(settings=dict(self.settings, revision="different"))):
            with self.subTest(kwargs=tuple(kwargs)), self.assertRaises(ValueError):
                self.call(**kwargs)
        self.assertEqual(self.backend.model.calls, [])
        self.assertIsNone(self.backend.torch.seed)

    def test_numeric_type_changes_cannot_pass_exact_json_settings_or_tokenization_equality(self):
        generation = dict(self.settings["generation"], top_k=20.0)
        for kwargs in (dict(settings=dict(self.settings, generation=generation)),
                       dict(settings=dict(self.settings, enable_thinking=0)),
                       dict(tokenized=replace(self.tokenized, attention_mask=(True,) * len(self.tokenized.attention_mask))),
                       dict(tokenized=replace(self.tokenized, input_ids=tuple(float(i) for i in self.tokenized.input_ids)))):
            with self.assertRaises(ValueError):
                self.call(**kwargs)
        self.assertEqual(self.backend.model.calls, [])
        self.assertIsNone(self.backend.torch.seed)


class LedgerIntegrationTests(unittest.TestCase):
    def test_conflicting_factory_worker_visibility_fails_before_store_or_process_creation(self):
        from recovery.inference import ModelFactory
        from recovery.workers import LocalScheduler, WorkerSpec
        world = case_world(Task.PREFIX)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            worker = WorkerSpec(path, ModelFactory(cuda_visible_devices="0"), cuda_visible_devices="1")
            with self.assertRaisesRegex(ValueError, "visibility"):
                LocalScheduler([worker], [world], [prefix_branch(world)], Tokenizer,
                    settings=candidate_settings(Tokenizer()))
            self.assertFalse(path.exists())

    def test_diagnosed_nonfinite_generation_is_blocked_uncertain_and_cannot_retry(self):
        from tests.inference_mocks import process_nonfinite_backend
        from recovery.storage import UnresolvedAttempt
        world = case_world(Task.PREFIX)
        branch = prefix_branch(world)
        tokenizer = Tokenizer()
        with tempfile.TemporaryDirectory() as folder:
            with DurableRunner(Path(folder) / "worker.sqlite", tokenizer,
                               ProcessProvider(process_nonfinite_backend, timeout_seconds=30)) as runner:
                runner.start(world, branch, settings=candidate_settings(tokenizer))
                with self.assertRaises(ProviderDefect):
                    runner.run_round(branch.branch_id, 1)
                attempts = runner.store.attempts(branch.calls[0].call_id)
                self.assertEqual(len(attempts), 1)
                self.assertEqual(attempts[0]["status"], "blocked")
                self.assertEqual(attempts[0]["uncertain_completion"], 1)
                self.assertIsNone(runner.store.call(branch.calls[0].call_id)["raw_json"])
                with self.assertRaises(UnresolvedAttempt):
                    runner.run_round(branch.branch_id, 1)
                self.assertEqual(len(runner.store.attempts(branch.calls[0].call_id)), 1)

    def test_two_serial_workers_inherit_visibility_and_keep_original_seed_and_attempt_records(self):
        from recovery.workers import LocalScheduler, WorkerSpec
        worlds = tuple(case_world(task) for task in (Task.PREFIX, Task.SORT))
        branches = tuple(prefix_branch(world) for world in worlds)
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"worker-{i}.sqlite" for i in range(2)]
            workers = [WorkerSpec(path, process_backend, cuda_visible_devices=str(i)) for i, path in enumerate(paths)]
            with LocalScheduler(workers, worlds, branches, Tokenizer,
                                settings=candidate_settings(Tokenizer()), timeout_seconds=30) as scheduler:
                scheduler.run()
                self.assertIsNone(scheduler.stop_reason)
            import sqlite3
            owners = []
            for i, path in enumerate(paths):
                with closing(sqlite3.connect(path)) as connection:
                    rows = connection.execute("SELECT device_visibility,backend_json,pid FROM provider_processes").fetchall()
                    self.assertEqual(len(rows), 1)
                    self.assertEqual(rows[0][0], str(i))
                    self.assertEqual(json.loads(rows[0][1])["cuda_visible_devices"], str(i))
                    owners.append(rows[0][2])
                    attempts = connection.execute("SELECT number,backend_json FROM attempts").fetchall()
                    self.assertEqual(len(attempts), 16)
                    self.assertTrue(all(row[0] == 1 for row in attempts))
                    self.assertTrue(all(json.loads(row[1])["pid"] == rows[0][2] for row in attempts))
            self.assertNotEqual(owners[0], owners[1])

    def test_spawned_adapter_persists_loading_raw_suffix_ids_seeds_before_effects_and_resumes(self):
        world = case_world(Task.PREFIX)
        branch = prefix_branch(world)
        tokenizer = Tokenizer()
        settings = candidate_settings(tokenizer)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "worker.sqlite"
            with DurableRunner(path, tokenizer, ProcessProvider(process_backend, timeout_seconds=30)) as runner:
                runner.start(world, branch, settings=settings)
                result = runner.run_round(branch.branch_id, 1)
                self.assertEqual(len(result.barrier.replies), 4)
                rows = list(runner.store.connection.execute("SELECT * FROM attempts ORDER BY call_id"))
                self.assertEqual(len(rows), 4)
                self.assertEqual(len({row["worker_pid"] for row in rows}), 1)
                for row in rows:
                    response = runner.store.response(row["call_id"])
                    diagnostic = json.loads(row["backend_json"])
                    self.assertEqual(diagnostic["raw_suffix_text"], response.text + "<|im_end|>")
                    self.assertEqual(response.token_ids[-1], TRANSPORT_ID)
                    self.assertEqual(diagnostic["seed"], runner.store.call(row["call_id"])["seed"])
                    self.assertEqual(row["peak_memory_bytes"], 750)
                    self.assertEqual(row["status"], "completed")
                loads = runner.store.connection.execute("SELECT backend_json FROM provider_processes").fetchall()
                self.assertEqual(len(loads), 1)
                self.assertEqual(json.loads(loads[0][0])["kind"], "CPU mock load")
                before = [tuple(row) for row in rows]
                runner.backup(Path(folder) / "backup.sqlite")
            with DurableRunner(path, tokenizer, forbidden, scripted=True) as runner:
                runner.run_round(branch.branch_id, 1)
                self.assertEqual([tuple(row) for row in runner.store.connection.execute("SELECT * FROM attempts ORDER BY call_id")], before)
            with DurableRunner(Path(folder) / "backup.sqlite", tokenizer, forbidden, scripted=True) as runner:
                runner.run_round(branch.branch_id, 1)
                self.assertEqual(len(runner.store.attempts(branch.calls[0].call_id)), 1)
