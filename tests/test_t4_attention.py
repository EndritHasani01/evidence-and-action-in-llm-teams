"""Real CPU numerical/native integration plus controlled CUDA selection checks.

No pretrained weights, actual CUDA operation or study generation is performed.
Run explicitly with the reviewed Torch/Transformers CPU interpreter.
"""

from contextlib import nullcontext
from dataclasses import replace
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class T4AttentionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        cls.torch = torch
        cls.previous_threads = torch.get_num_threads()
        torch.set_num_threads(1)

    @classmethod
    def tearDownClass(cls):
        cls.torch.set_num_threads(cls.previous_threads)

    def inputs(self, length=9, cached=0, dtype=None):
        t = self.torch
        generator = t.Generator().manual_seed(51)
        # Native projection layout: [batch, sequence, heads, dim].transpose.
        dtype = dtype or t.float64
        q = t.randn(1, length, 16, 256, generator=generator, dtype=dtype).transpose(1, 2)
        k = t.randn(1, length + cached, 4, 256, generator=generator, dtype=dtype).transpose(1, 2)
        v = t.randn(1, length + cached, 4, 256, generator=generator, dtype=dtype).transpose(1, 2)
        return q, k, v

    def forward(self, q, k, v, mask=None, **kwargs):
        from recovery.t4_attention import t4_sdpa_forward
        module = SimpleNamespace(training=False, num_key_value_groups=4, is_causal=True)
        return t4_sdpa_forward(module, q, k, v, mask, **kwargs)[0]

    def reference(self, q, k, v, mask=None, *, causal=False, scale=None):
        t = self.torch
        rows = []
        for head in range(16):
            score = q[0, head] @ k[0, head // 4].T
            score = score * (scale if scale is not None else 256**-0.5)
            if causal:
                score = score.masked_fill(~t.ones_like(score, dtype=t.bool).tril(), float("-inf"))
            if mask is not None:
                data = mask[0, 0]
                score = score.masked_fill(~data, float("-inf")) if data.dtype == t.bool else score + data
            probabilities = t.softmax(score, -1)
            # A fully blocked row is zero under maintained SDPA semantics.
            probabilities = t.where(t.isneginf(score).all(-1, keepdim=True), 0, probabilities)
            rows.append(probabilities @ v[0, head // 4])
        return t.stack(rows, dim=1).unsqueeze(0)

    def test_causal_prefill_matches_independent_per_head_reference(self):
        q, k, v = self.inputs()
        self.torch.testing.assert_close(self.forward(q, k, v), self.reference(q, k, v, causal=True), rtol=1e-12, atol=1e-12)

    def test_decode_reads_complete_cache_and_preserves_head_order(self):
        q, k, v = self.inputs(length=1, cached=8)
        self.torch.testing.assert_close(self.forward(q, k, v), self.reference(q, k, v), rtol=1e-12, atol=1e-12)

    def test_offset_causal_mask_matches_cached_multi_query_reference(self):
        q, k, v = self.inputs(length=3, cached=7)
        mask = (self.torch.arange(10)[None, :] <= self.torch.arange(7, 10)[:, None])[None, None]
        self.torch.testing.assert_close(self.forward(q, k, v, mask), self.reference(q, k, v, mask), rtol=1e-12, atol=1e-12)

    def test_causal_padding_mask_and_fully_masked_row_are_preserved(self):
        q, k, v = self.inputs()
        mask = self.torch.ones(1, 1, 9, 9, dtype=self.torch.bool).tril()
        mask[..., 0] = False
        before = mask.clone()
        self.torch.testing.assert_close(self.forward(q, k, v, mask), self.reference(q, k, v, mask), rtol=1e-12, atol=1e-12)
        self.assertTrue(self.torch.equal(before, mask))

    def test_additive_mask_scaling_and_explicit_bidirectional_mode(self):
        q, k, v = self.inputs()
        mask = self.torch.zeros(1, 1, 9, 9, dtype=q.dtype)
        mask[..., 2] = -0.5
        self.torch.testing.assert_close(self.forward(q, k, v, mask, scaling=0.125), self.reference(q, k, v, mask, scale=0.125), rtol=1e-12, atol=1e-12)
        self.torch.testing.assert_close(self.forward(q, k, v, is_causal=False), self.reference(q, k, v), rtol=1e-12, atol=1e-12)

    def test_fp16_prefill_and_decode_remain_finite_and_match_fp32(self):
        for length, cached in [(32, 0), (1, 31)]:
            q, k, v = self.inputs(length, cached, self.torch.float16)
            result = self.forward(q, k, v)
            self.assertTrue(self.torch.isfinite(result).all().item())
            expected = self.reference(q.float(), k.float(), v.float(), causal=length > 1)
            self.torch.testing.assert_close(result.float(), expected, rtol=0.02, atol=0.002)

    def test_kv_views_alias_original_storage_and_mask_rows_align_before_expand(self):
        from recovery.t4_attention import grouped_inputs
        q, k, v = self.inputs()
        mask = self.torch.ones(1, 1, 9, 9, dtype=self.torch.bool)
        original = [x.clone() for x in (q, k, v, mask)]
        grouped_q, grouped_k, grouped_v, bias = grouped_inputs(q, k, v, mask)
        self.assertEqual(grouped_q.shape, (4, 4, 9, 256))
        for before, after in [(k, grouped_k), (v, grouped_v)]:
            self.assertEqual(before.untyped_storage().data_ptr(), after.untyped_storage().data_ptr())
            self.assertEqual(before.untyped_storage().nbytes(), after.untyped_storage().nbytes())
            self.assertEqual(after.stride(1), 0)
        self.assertEqual(bias.stride(0), 0)
        self.assertEqual(bias.stride(1), 0)
        self.assertEqual(bias.stride(-2) % 8, 0)
        self.assertEqual(bias.untyped_storage().nbytes(), 9 * 16 * q.element_size())
        self.forward(q, k, v, mask)
        for before, after in zip(original, (q, k, v, mask)):
            self.assertTrue(self.torch.equal(before, after))

    def test_long_meta_kv_storage_is_not_multiplied(self):
        from recovery.t4_attention import grouped_inputs
        t = self.torch
        q = t.empty(1, 16, 1, 256, device="meta", dtype=t.float16)
        k = t.empty(1, 4, 262144, 256, device="meta", dtype=t.float16)
        _, grouped_k, grouped_v, _ = grouped_inputs(q, k, k)
        for view in (grouped_k, grouped_v):
            self.assertEqual(view.untyped_storage().nbytes(), 4 * 262144 * 256 * 2)
            self.assertEqual(view.stride(1), 0)

    def test_missing_offset_mask_training_dropout_and_weight_output_refuse(self):
        from recovery.t4_attention import t4_sdpa_forward
        q, k, v = self.inputs(length=3, cached=7)
        with self.assertRaisesRegex(ValueError, "offset mask"):
            self.forward(q, k, v)
        for kwargs in [dict(dropout=0.1), dict(output_attentions=True), dict(is_causal=1)]:
            with self.assertRaises(ValueError):
                self.forward(*self.inputs(), **kwargs)
        with self.assertRaisesRegex(ValueError, "inference-only"):
            t4_sdpa_forward(SimpleNamespace(training=True), q, k, v, None)

    def test_wrong_shapes_dtype_device_and_mask_refuse_before_dispatch(self):
        q, k, v = self.inputs()
        invalid = [(q.expand(2, -1, -1, -1), k, v, None), (q, k, v.float(), None),
            (q[:, :15], k, v, None), (q, k, v, self.torch.ones(9, 9, dtype=self.torch.bool)),
            (q, k, v, self.torch.ones(1, 16, 9, 9, dtype=q.dtype)),
            (q[..., ::2], k, v, None), (q, k, v, self.torch.zeros(1, 1, 9, 8, dtype=q.dtype))]
        for inputs in invalid:
            with self.subTest(shapes=[x.shape if x is not None else None for x in inputs]), self.assertRaises(ValueError):
                self.forward(*inputs)

    def test_cuda_selects_only_efficient_and_never_retries_math(self):
        from recovery.t4_attention import t4_sdpa_forward
        from torch.nn.attention import SDPBackend
        t = self.torch
        real = self.inputs(3, dtype=t.float16)
        query = SimpleNamespace(shape=real[0].shape, dtype=t.float16, device=SimpleNamespace(type="cuda"))
        module = SimpleNamespace(training=False, num_key_value_groups=4, is_causal=True)
        for error in [None, RuntimeError("No efficient kernel available")]:
            with patch("recovery.t4_attention.grouped_inputs", return_value=(*real, None)), \
                 patch.object(t, "__version__", "2.11.0+cu128"), patch.object(t.version, "cuda", "12.8"), \
                 patch.object(t.cuda, "get_device_capability", return_value=(7, 5)), \
                 patch("torch.nn.attention.sdpa_kernel", return_value=nullcontext()) as selector, \
                 patch("torch.nn.functional.scaled_dot_product_attention", return_value=t.zeros(4, 4, 3, 256), side_effect=error) as operation:
                if error:
                    with self.assertRaisesRegex(RuntimeError, "No efficient kernel"):
                        t4_sdpa_forward(module, query, real[1], real[2], None)
                else:
                    t4_sdpa_forward(module, query, real[1], real[2], None)
                selector.assert_called_once_with(SDPBackend.EFFICIENT_ATTENTION)
                operation.assert_called_once()

    def test_candidate_opt_in_changes_only_backend_and_maintained_prefill(self):
        from recovery.inference import QWEN_9B, candidate_settings
        from recovery.t4_attention import T4_ATTENTION, PREFILL_CHUNK_SIZE
        from tests.inference_mocks import Tokenizer
        baseline = candidate_settings(Tokenizer())
        alternate = candidate_settings(Tokenizer(), replace(QWEN_9B, attention=T4_ATTENTION))
        self.assertEqual(alternate.pop("attention"), T4_ATTENTION)
        self.assertEqual(alternate["generation"].pop("prefill_chunk_size"), PREFILL_CHUNK_SIZE)
        baseline.pop("attention")
        self.assertEqual(alternate, baseline)
        self.assertEqual(QWEN_9B.attention, "sdpa")

    def test_both_public_registries_preserve_builtin_sdpa_and_refuse_collision(self):
        from transformers import AttentionInterface, AttentionMaskInterface
        from transformers.masking_utils import sdpa_mask
        from recovery.t4_attention import register_t4_attention, t4_sdpa_forward, T4_ATTENTION
        native = (AttentionInterface()["sdpa"], AttentionMaskInterface()["sdpa"])
        register_t4_attention()
        register_t4_attention()
        self.assertIs(AttentionInterface()[T4_ATTENTION], t4_sdpa_forward)
        self.assertIs(AttentionMaskInterface()[T4_ATTENTION], sdpa_mask)
        self.assertEqual(native, (AttentionInterface()["sdpa"], AttentionMaskInterface()["sdpa"]))
        try:
            AttentionInterface.register(T4_ATTENTION, lambda *args: None)
            with self.assertRaisesRegex(ValueError, "different code"):
                register_t4_attention()
        finally:
            AttentionInterface.register(T4_ATTENTION, t4_sdpa_forward)


class NativeHybridIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        cls.previous_threads = torch.get_num_threads()
        torch.set_num_threads(1)

    @classmethod
    def tearDownClass(cls):
        import torch
        torch.set_num_threads(cls.previous_threads)

    def test_real_hybrid_model_chunked_prefill_matches_full_cache_logits_and_decode(self):
        self.exercise_hybrid(7, 3)

    def test_configured_256_token_chunks_preserve_hybrid_state_across_513_tokens(self):
        self.exercise_hybrid(513, 256)

    def exercise_hybrid(self, length, chunk_size):
        import torch
        from transformers import DynamicCache, GenerationConfig
        from transformers.models.qwen3_5.configuration_qwen3_5 import Qwen3_5TextConfig
        from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM
        from recovery.t4_attention import register_t4_attention, T4_ATTENTION
        register_t4_attention()
        config = Qwen3_5TextConfig(vocab_size=64, hidden_size=64, intermediate_size=96,
            num_hidden_layers=2, num_attention_heads=16, num_key_value_heads=4, head_dim=16,
            layer_types=["linear_attention", "full_attention"],
            linear_num_key_heads=2, linear_num_value_heads=4,
            linear_key_head_dim=8, linear_value_head_dim=8,
            rope_parameters={"rope_type": "default", "rope_theta": 10000.0,
                             "partial_rotary_factor": 0.5, "mrope_section": [1, 1, 0]},
            attn_implementation=T4_ATTENTION)
        with torch.random.fork_rng(devices=[]), torch.inference_mode():
            torch.manual_seed(73)
            model = Qwen3_5ForCausalLM(config).eval()
            ids = (torch.arange(length).remainder(59) + 3).unsqueeze(0)
            mask = torch.ones_like(ids)
            full = DynamicCache(config=config)
            chunked = DynamicCache(config=config)
            expected = model(ids, attention_mask=mask, past_key_values=full, logits_to_keep=1)
            actual = model._prefill(ids, GenerationConfig(prefill_chunk_size=chunk_size),
                dict(attention_mask=mask, past_key_values=chunked, use_cache=True, logits_to_keep=1))
            torch.testing.assert_close(actual.logits, expected.logits, rtol=2e-4, atol=2e-5)
            self.assertEqual(full.get_seq_length(), ids.shape[1])
            self.assertEqual(chunked.get_seq_length(), ids.shape[1])
            for left, right in zip(full.layers, chunked.layers):
                for name in ("keys", "values", "conv_states", "recurrent_states"):
                    if getattr(left, name, None) is not None:
                        torch.testing.assert_close(getattr(left, name), getattr(right, name), rtol=2e-4, atol=2e-5)
            next_id = torch.tensor([[19]])
            expected_next = model(next_id, attention_mask=torch.ones(1, length + 1, dtype=torch.long), past_key_values=full)
            actual_next = model(next_id, attention_mask=torch.ones(1, length + 1, dtype=torch.long), past_key_values=chunked)
            torch.testing.assert_close(actual_next.logits, expected_next.logits, rtol=2e-4, atol=2e-5)
            fresh = DynamicCache(config=config)
            repeated = model(ids, attention_mask=mask, past_key_values=fresh, logits_to_keep=1)
            torch.testing.assert_close(repeated.logits, expected.logits, rtol=0, atol=0)
            self.assertIsNot(fresh, full)


if __name__ == "__main__":
    unittest.main()
