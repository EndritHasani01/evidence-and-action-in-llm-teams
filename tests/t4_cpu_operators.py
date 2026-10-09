"""Real CPU API/numerical checks, explicitly not CUDA/T4 acceptance."""

import unittest

import bitsandbytes as bnb
import torch
from torch.nn.attention import SDPBackend, sdpa_kernel

from scripts.m5_t4_compatibility import ATTENTION_CASES, attention_inputs, nf4_comparison, sdpa_comparison


class CPUOperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if torch.__version__ != "2.11.0+cpu" or bnb.__version__ != "0.49.2":
            raise AssertionError("This retained CPU check requires Torch 2.11.0+cpu and bitsandbytes 0.49.2")
        torch.set_num_threads(1)

    def test_automatic_small_shape_cases_match_reference(self):
        for case in ATTENTION_CASES:
            if not case[-1]:
                with self.subTest(case=case[0]):
                    result = sdpa_comparison(torch, torch.device("cpu"), case)
                    self.assertEqual(result["status"], "passed")
                    self.assertTrue(result["finite"] and result["reference_matches"])
                    self.assertFalse(result["cuda_kernel_trace_available"])
                    self.assertEqual(result["cuda_kernels"], [])

    def test_decode_attends_all_keys_and_matches_independent_matrix_formula(self):
        q, k, v = attention_inputs(torch, "decode")
        k, v = k.repeat_interleave(4, dim=1), v.repeat_interleave(4, dim=1)
        expected = ((q @ k.transpose(-2, -1))/16).softmax(dim=-1) @ v
        with sdpa_kernel(SDPBackend.MATH):
            actual = torch.nn.functional.scaled_dot_product_attention(q, k, v, dropout_p=0, is_causal=False)
        torch.testing.assert_close(actual, expected)
        self.assertFalse(torch.allclose(actual, v[:, :, :1, :]))

    def test_causal_prefill_matches_independent_masked_matrix_formula(self):
        q, k, v = attention_inputs(torch, "prefill")
        k, v = k.repeat_interleave(4, dim=1), v.repeat_interleave(4, dim=1)
        allowed = torch.ones(32, 32, dtype=torch.bool).tril()
        expected = ((q @ k.transpose(-2, -1))/16).masked_fill(~allowed, float("-inf")).softmax(dim=-1) @ v
        with sdpa_kernel(SDPBackend.MATH):
            actual = torch.nn.functional.scaled_dot_product_attention(q, k, v, dropout_p=0, is_causal=True)
        torch.testing.assert_close(actual, expected)

    def test_nf4_double_quantized_fp16_api_and_dequantized_reference(self):
        result = nf4_comparison(torch, bnb, torch.device("cpu"))
        self.assertEqual(result["weight_shape"], [128, 256])
        self.assertEqual(result["quant_type"], "nf4")
        self.assertTrue(result["double_quantization"])
        self.assertTrue(all(row["finite"] and row["reference_matches"] for row in result["operations"]))
        self.assertEqual([row["batch"] for row in result["operations"]], [8, 1])


if __name__ == "__main__":
    unittest.main()
