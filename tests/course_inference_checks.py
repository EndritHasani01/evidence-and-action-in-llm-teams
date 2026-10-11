"""Adopted 4B/256/64 candidate through the existing serial adapter and ledger."""

from dataclasses import asdict, replace
from contextlib import closing
import gc
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from recovery.attempts import ProcessProvider
from recovery.inference import (ModelFactory, QWEN_4B, QWEN_9B, TRANSPORT_ID,
    TransformersBackend, candidate_settings)
from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.state import initial_view
from recovery.t4_attention import PREFILL_CHUNK_SIZE, T4_ATTENTION
from recovery.tasks import Task
from tests.course_protocol_cases import course_population
from tests.inference_mocks import (LOADING_INFO, GenerationConfig, Qwen3_5ForCausalLM,
    Tokenizer, Torch, mock_transformers)

COURSE_CANDIDATE = replace(QWEN_4B, attention=T4_ATTENTION)


def course_backend():
    """Spawn fixture invokes the real adapter; neither weights nor CUDA exist."""
    sys.modules["transformers"] = mock_transformers()
    model = Qwen3_5ForCausalLM(tied=True)
    model.reply_ids = tuple(map(ord, '{"candidate":[0,0,0,0,0,0],"send":[]}')) + (TRANSPORT_ID,)
    return TransformersBackend(Torch(), model, Tokenizer(), COURSE_CANDIDATE,
        dict(kind="CPU course mock", model=QWEN_4B.model, revision=QWEN_4B.revision,
             attention=T4_ATTENTION, cuda_visible_devices=os.environ.get("CUDA_VISIBLE_DEVICES")),
        limits=COURSE_LIMITS)


class CourseInferencePreparationTests(unittest.TestCase):
    def setUp(self):
        self.world = next(w for w in course_population().development if w.world.task is Task.PREFIX)
        self.branch = next(b for b in _prepare_branches((self.world,)) if b.phase == "prefix")
        self.view = initial_view(self.world.world, 0)
        self.tokenizer = Tokenizer()
        self.settings = candidate_settings(self.tokenizer, COURSE_CANDIDATE, limits=COURSE_LIMITS)

    def test_course_attention_candidate_changes_only_explicit_backend_and_prefill(self):
        baseline = candidate_settings(self.tokenizer, QWEN_4B, limits=COURSE_LIMITS)
        actual = json.loads(json.dumps(self.settings))
        self.assertEqual(actual.pop("attention"), T4_ATTENTION)
        self.assertEqual(actual["generation"].pop("prefill_chunk_size"), PREFILL_CHUNK_SIZE)
        baseline.pop("attention")
        self.assertEqual(actual, baseline)
        self.assertEqual(self.settings["protocol_limits"], asdict(COURSE_LIMITS))
        for model in (QWEN_4B, QWEN_9B):
            thesis = candidate_settings(self.tokenizer, model)
            self.assertEqual(thesis["generation"]["max_new_tokens"], 384)
            self.assertEqual(thesis["attention"], "sdpa")
            self.assertNotIn("prefill_chunk_size", thesis["generation"])

    def test_course_loader_keeps_pinned_language_tie_nf4_visibility_and_limits(self):
        torch = Torch()
        torch.__version__, torch.version.cuda = "2.11.0+cu128", "12.8"
        torch.cuda.get_device_capability = lambda device: (7, 5)
        model = Qwen3_5ForCausalLM(tied=True)
        model.config._attn_implementation = T4_ATTENTION
        loader, quantizer, tokenizer = Mock(return_value=(model, LOADING_INFO)), Mock(), Mock(return_value=self.tokenizer)
        modules = SimpleNamespace(AutoModelForCausalLM=SimpleNamespace(from_pretrained=loader),
            AutoTokenizer=SimpleNamespace(from_pretrained=tokenizer), BitsAndBytesConfig=quantizer,
            GenerationConfig=GenerationConfig)
        with patch.dict(os.environ), patch.dict(sys.modules, torch=torch, transformers=modules), \
                patch("importlib.metadata.version", return_value="CPU mock"), \
                patch("recovery.t4_attention.register_t4_attention") as register:
            torch.cuda.is_available = lambda: os.environ["CUDA_VISIBLE_DEVICES"] == "GPU-course-mock"
            backend = ModelFactory(COURSE_CANDIDATE, "GPU-course-mock", COURSE_LIMITS)()
        register.assert_called_once()
        self.assertEqual(backend.settings, self.settings)
        self.assertEqual(backend.load_report["revision"], QWEN_4B.revision)
        self.assertTrue(backend.load_report["tied_output_head"])
        self.assertEqual(tokenizer.call_args.kwargs["revision"], QWEN_4B.revision)
        self.assertEqual(loader.call_args.args, (QWEN_4B.model,))
        self.assertEqual(loader.call_args.kwargs["revision"], QWEN_4B.revision)
        self.assertEqual(loader.call_args.kwargs["device_map"], {"": 0})
        self.assertEqual(quantizer.call_args.kwargs["bnb_4bit_compute_dtype"], torch.float16)
        self.assertEqual(backend.load_report["generation_config"]["max_new_tokens"], 256)

    def test_course_order_restart_and_exception_dispose_state_and_restore_call_seed(self):
        with patch.dict(sys.modules, transformers=mock_transformers()):
            value = course_backend()
            rendered = render_request(self.view, limits=COURSE_LIMITS)
            tokens = tokenize_request(rendered, self.tokenizer, limits=COURSE_LIMITS)
            a = value(self.view, rendered, tokens, seed=17, settings=self.settings)
            value(self.view, rendered, tokens, seed=29, settings=self.settings)
            repeated = value(self.view, rendered, tokens, seed=17, settings=self.settings)
            fresh = course_backend()(self.view, rendered, tokens, seed=17, settings=self.settings)
            self.assertEqual(a.response, repeated.response)
            self.assertEqual(a.response, fresh.response)
            for result in (a, repeated, fresh):
                self.assertEqual(result.backend["cpu_seed"], 17)
                self.assertEqual(result.backend["cuda_seed"], 17)
                self.assertEqual(result.backend["raw_suffix_text"], result.response.text + "<|im_end|>")
                self.assertTrue(result.backend["cache"]["disposed_after_call"])
            value.model.fail = True
            with self.assertRaisesRegex(ValueError, "simulated"):
                value(self.view, rendered, tokens, seed=17, settings=self.settings)
            gc.collect()
            self.assertTrue(all(call["cache"]() is None for call in value.model.calls))
            self.assertEqual(value.model.hooks, [])
            self.assertFalse(value.active)

    def test_course_overflow_and_thesis_settings_reject_before_seed_or_generation(self):
        with patch.dict(sys.modules, transformers=mock_transformers()):
            value = course_backend()
            request = render_request(self.view, limits=COURSE_LIMITS)
            tokens = tokenize_request(request, self.tokenizer, limits=COURSE_LIMITS)
            for changed in (dict(settings=candidate_settings(self.tokenizer, QWEN_4B)),
                dict(tokens=replace(tokens, input_ids=(1,) * (262144 - 256 + 1))),
                dict(settings=candidate_settings(self.tokenizer, QWEN_4B, limits=COURSE_LIMITS))):
                with self.subTest(changed=list(changed)), self.assertRaises(ValueError):
                    value(self.view, request, changed.get("tokens", tokens), seed=17,
                          settings=changed.get("settings", self.settings))
            self.assertEqual(value.model.calls, [])
            self.assertIsNone(value.torch.seed)

    def test_course_subprocess_attempt_fields_survive_raw_resume_and_closed_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path, backup = Path(directory) / "worker.sqlite", Path(directory) / "closed.sqlite"
            provider = ProcessProvider(course_backend, timeout_seconds=30)
            # Explicit worker visibility precedes creation of the spawned fixture.
            with patch.dict(os.environ, CUDA_VISIBLE_DEVICES="GPU-course-mock"), \
                    DurableRunner(path, self.tokenizer, provider) as runner:
                runner.start(self.world, self.branch, settings=self.settings)
                original = runner.run_round(self.branch.branch_id, 1)
                for call in self.branch.calls[:4]:
                    record = runner.store.call(call.call_id)
                    attempt, = runner.store.attempts(call.call_id)
                    evidence = json.loads(attempt["backend_json"])
                    saved_settings, = runner.store.connection.execute(
                        "SELECT settings_json FROM round_inputs WHERE branch_id=? AND round_number=1",
                        (self.branch.branch_id,)).fetchone()
                    self.assertEqual(json.loads(saved_settings), self.settings)
                    self.assertEqual(evidence["seed"], call.seed)
                    self.assertEqual(evidence["cpu_seed"], call.seed)
                    self.assertEqual(evidence["cuda_seed"], call.seed)
                    self.assertEqual(evidence["pid"], attempt["worker_pid"])
                    self.assertEqual(evidence["removed_terminal_id"], TRANSPORT_ID)
                    self.assertEqual(evidence["raw_suffix_text"],
                        json.loads(record["raw_json"])["text"] + "<|im_end|>")
                    self.assertEqual(attempt["peak_memory_bytes"], 750)
                process, = runner.store.connection.execute("SELECT backend_json FROM provider_processes").fetchall()
                self.assertEqual(json.loads(process[0])["revision"], QWEN_4B.revision)
            def forbidden(*args, **kwargs):
                raise AssertionError("durable course replies cannot be resampled")
            with DurableRunner(path, self.tokenizer, forbidden, scripted=True) as runner:
                self.assertEqual(runner.run_round(self.branch.branch_id, 1), original)
                runner.backup(backup)
            import sqlite3
            with closing(sqlite3.connect(f"file:{backup.as_posix()}?mode=ro&immutable=1", uri=True)) as connection:
                self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 4)
