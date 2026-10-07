"""Candidate/loading contracts are CPU checks, independent of inference packages."""

import json
import subprocess
import sys
import unittest
from unittest.mock import patch

from recovery.inference import (Candidate, ModelFactory, QWEN_9B, QWEN_4B,
                                audit_language_load, candidate_settings)
from tests.inference_mocks import GenerationConfig, LOADING_INFO, Qwen3_5ForCausalLM, Tensor, Tokenizer, Torch


class InferencePreparationTests(unittest.TestCase):
    def test_only_reviewed_candidates_and_complete_non_thinking_settings(self):
        for candidate in (QWEN_9B, QWEN_4B):
            settings = candidate_settings(Tokenizer(), candidate)
            self.assertEqual(settings["revision"], candidate.revision)
            self.assertFalse(settings["enable_thinking"])
            self.assertEqual(settings["generation"]["max_new_tokens"], 384)
            self.assertEqual(settings["max_context_tokens"], 262144)
            self.assertEqual(settings["generation"]["eos_token_id"], [248044, 248046])
            self.assertNotIn("presence_penalty", settings["generation"])
            self.assertEqual(settings["quantization"], dict(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype="float16"))
        with self.assertRaises(ValueError):
            Candidate("arbitrary/model", "main")

    def test_template_ids_and_exact_terminal_spelling_are_verified(self):
        for key, value in (("eos_token_id", 1), ("pad_token_id", 2), ("chat_template", None)):
            tokenizer = Tokenizer()
            setattr(tokenizer, key, value)
            with self.assertRaises(ValueError):
                candidate_settings(tokenizer)
        tokenizer = Tokenizer()
        tokenizer.convert_ids_to_tokens = lambda token: "unverified marker"
        with self.assertRaises(ValueError):
            candidate_settings(tokenizer)

    def test_all_loading_errors_and_unexpected_language_keys_are_rejected(self):
        for key, value in (("missing_keys", {"model.layers.0.weight"}),
                           ("mismatched_keys", {("lm_head.weight", (2,), (3,))}),
                           ("error_msgs", ["load failed"]),
                           ("unexpected_keys", {"language_model.layers.0.weight"})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                audit_language_load(Qwen3_5ForCausalLM(), dict(LOADING_INFO, **{key: value}))
        with self.assertRaises(ValueError):
            audit_language_load(Qwen3_5ForCausalLM(), {})
        report = audit_language_load(Qwen3_5ForCausalLM(),
            dict(LOADING_INFO, unexpected_keys={"model.visual.weight", "mtp.weight"}))
        json.dumps(report, allow_nan=False)  # Maintained loader returns sets.

    def test_tied_head_is_verified_and_does_not_excuse_missing_embedding(self):
        self.assertTrue(audit_language_load(Qwen3_5ForCausalLM(tied=True), LOADING_INFO)["tied_output_head"])
        self.assertFalse(audit_language_load(Qwen3_5ForCausalLM(), LOADING_INFO)["tied_output_head"])
        tied = Qwen3_5ForCausalLM(tied=True)
        tied.head = Tensor()
        with self.assertRaises(ValueError):
            audit_language_load(tied, LOADING_INFO)
        with self.assertRaises(ValueError):
            audit_language_load(Qwen3_5ForCausalLM(tied=True), dict(LOADING_INFO, missing_keys={"model.embed_tokens.weight"}))

    def test_offload_splitting_meta_and_unsupported_precision_fail(self):
        for device in ("cpu", "cuda:1", "meta"):
            model = Qwen3_5ForCausalLM()
            model.embedding = Tensor(device=device)
            with self.subTest(device=device), self.assertRaises(ValueError):
                audit_language_load(model, LOADING_INFO)
        for device in ("cpu", "disk", 1):
            model = Qwen3_5ForCausalLM()
            model.hf_device_map = {"": device}
            with self.assertRaises(ValueError):
                audit_language_load(model, LOADING_INFO)
        model = Qwen3_5ForCausalLM()
        model.head.dtype = "torch.bfloat16"
        with self.assertRaises(ValueError):
            audit_language_load(model, LOADING_INFO)
        model.head.dtype = "torch.float32"
        audit_language_load(model, LOADING_INFO)

    def test_loader_sets_visibility_before_any_cuda_call_and_requests_native_nf4(self):
        import os
        from types import SimpleNamespace
        torch = Torch()
        seen = []
        torch.cuda.is_available = lambda: seen.append(os.environ["CUDA_VISIBLE_DEVICES"]) or True
        loader = unittest.mock.Mock(return_value=(Qwen3_5ForCausalLM(), LOADING_INFO))
        quantizer = unittest.mock.Mock(return_value="NF4 configuration")
        tokenizer_loader = unittest.mock.Mock(return_value=Tokenizer())
        transformers = SimpleNamespace(AutoModelForCausalLM=SimpleNamespace(from_pretrained=loader),
            BitsAndBytesConfig=quantizer, AutoTokenizer=SimpleNamespace(from_pretrained=tokenizer_loader),
            GenerationConfig=GenerationConfig)
        with patch.dict(os.environ), patch.dict(sys.modules, torch=torch, transformers=transformers), \
                patch("importlib.metadata.version", return_value="CPU mock"):
            model_backend = ModelFactory(cuda_visible_devices="1")()
        self.assertEqual(seen, ["1"])
        args = loader.call_args.kwargs
        self.assertEqual(args["device_map"], {"": 0})
        self.assertEqual(args["dtype"], torch.float16)
        self.assertEqual(args["attn_implementation"], "sdpa")
        self.assertTrue(args["output_loading_info"])
        self.assertFalse(args["trust_remote_code"])
        self.assertEqual(args["revision"], QWEN_9B.revision)
        self.assertEqual(quantizer.call_args.kwargs, dict(load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16))
        self.assertEqual(model_backend.load_report["cuda_visible_devices"], "1")

    def test_initialized_cuda_multiple_or_non_t4_devices_are_rejected_before_loading(self):
        for attribute, value in (("is_initialized", True), ("is_available", False),
                                 ("device_count", 2), ("get_device_name", "GPU other than T4")):
            torch = Torch()
            setattr(torch.cuda, attribute, lambda *args, value=value: value)
            if attribute == "get_device_name":
                torch.cuda.get_device_name = lambda device: "P100"
            with patch.dict(sys.modules, torch=torch, transformers=None), self.assertRaises(ValueError):
                ModelFactory()()
        with self.assertRaises(ValueError):
            ModelFactory(cuda_visible_devices="0,1")()

    def test_importing_adapter_never_imports_optional_inference_stack(self):
        script = '''
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, name, *args):
        if name.split('.')[0] in {'torch','transformers','accelerate','bitsandbytes'}:
            raise RuntimeError('unexpected inference import ' + name)
sys.meta_path.insert(0, Block())
import recovery.inference
print(recovery.inference.QWEN_9B.model)
'''
        result = subprocess.run([sys.executable, "-S", "-c", script], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Qwen/Qwen3.5-9B", result.stdout)
