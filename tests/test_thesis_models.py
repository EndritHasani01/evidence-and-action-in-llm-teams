"""Model settings, exact requests and the capacity proof (spec 3.8). No model is loaded."""
import json
import os
from pathlib import Path
import tempfile
import unittest

from recovery.thesis import load_config
from recovery.thesis import protocol
from recovery.thesis.checks import scripted_prefix
from recovery.thesis.models import ScriptedProvider, ScriptedTokenizer, capacity_bound, prepare, settings
from recovery.thesis.worlds import load_manifest

ROOT = Path(__file__).parents[1]
TOKENIZERS = Path(os.environ.get("THESIS_TOKENIZER_RECEIPTS", ""))


class Models(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(ROOT)
        manifest, _ = load_manifest(ROOT)
        cls.world = manifest["worlds"][16]

    def test_settings_are_model_native_and_explicit(self):
        tok = ScriptedTokenizer()
        q = settings(self.config, "qwen", tok, 8192)["generation"]
        g = settings(self.config, "granite", tok, 8192)["generation"]
        self.assertEqual((q["temperature"], q["top_p"], q["top_k"]), (0.7, 0.8, 20))
        self.assertEqual((g["temperature"], g["top_p"], g["top_k"]), (1.0, 0.95, 0))
        for gen in (q, g):
            self.assertEqual((gen["min_p"], gen["repetition_penalty"], gen["num_beams"], gen["max_new_tokens"]),
                             (0.0, 1.0, 1, 512))
        self.assertEqual(q["prefill_chunk_size"], 256)
        self.assertNotIn("prefill_chunk_size", g)
        self.assertEqual(g["eos_token_id"], [100257])
        with self.assertRaises(ValueError):
            settings(self.config, "qwen", tok, 4096)
        with self.assertRaises(ValueError):
            settings(self.config, "llama", tok, 8192)

    def test_prepare_is_deterministic_and_never_truncates(self):
        tok = ScriptedTokenizer()
        state = protocol.start(self.world, "qwen", "RV", scripted_prefix(self.world))
        view = protocol.view(self.world, state, 0)
        a = prepare(view, 12345, self.config, "qwen", tok, 8192)
        b = prepare(view, 12345, self.config, "qwen", tok, 8192)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertLessEqual(len(a["input_ids"]), 8192)
        huge = dict(view, history=[dict(kind="received_message", sender=1, text="x" * 40000)], earlier=1)
        with self.assertRaises(ValueError):
            prepare(huge, 1, self.config, "qwen", tok, 8192)
        env = prepare(dict(complete_input=[0, 1]), 1, self.config, "qwen", tok, 8192, control=True, envelope=True)
        self.assertEqual(len(env["input_ids"]), 8192)
        with self.assertRaises(ValueError):
            prepare(view, 2**63, self.config, "qwen", tok, 8192)

    def test_scripted_tokenizer_round_trips(self):
        tok = ScriptedTokenizer()
        for text in ("plain", "line\nnext", "é漢\U0001f600", '{"a": -1000}'):
            self.assertEqual(tok.decode(tok.encode(text)), text)

    def test_scripted_provider_reply_shape(self):
        tok = ScriptedTokenizer()
        request = prepare(protocol.control_view(self.world, "original"), 7, self.config, "qwen", tok, 8192, control=True)
        outcome = ScriptedProvider("qwen", {})(request)
        self.assertEqual(json.loads(outcome["visible_text"])["submit"], self.world["original_truth"])
        for key in ("raw_text", "token_ids", "termination", "truncated", "framing_error", "ready_seconds",
                    "input_tokens", "generated_tokens", "backend", "peak_memory_bytes", "failure"):
            self.assertIn(key, outcome)

    def test_scripted_capacity_bound(self):
        bound = capacity_bound(self.config, "qwen", ScriptedTokenizer(), 8192)
        self.assertTrue(bound["fits"])

    @unittest.skipUnless((TOKENIZERS / "assets-qwen-metadata.json").exists(),
                         "set THESIS_TOKENIZER_RECEIPTS to a folder with downloaded tokenizer receipts")
    def test_real_tokenizers_fit_8192_and_native_direct_framing(self):
        from recovery.thesis.models import load_tokenizer
        endings = {"qwen": "<|im_start|>assistant\n<think>\n\n</think>\n\n", "granite": "<|im_start|>assistant\n<think></think>"}
        for model in ("qwen", "granite"):
            receipt = json.loads((TOKENIZERS / f"assets-{model}-metadata.json").read_text())
            tok = load_tokenizer(self.config, model, receipt["snapshot"])
            bound = capacity_bound(self.config, model, tok, 8192)
            self.assertTrue(bound["fits"], bound)
            request = prepare(protocol.control_view(self.world, "original"), 1, self.config, model, tok, 8192, control=True)
            self.assertTrue(request["rendered"].endswith(endings[model]))


if __name__ == "__main__":
    unittest.main()
