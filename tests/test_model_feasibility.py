"""Admission arithmetic must retain unknowns and original evidence bytes."""

from contextlib import redirect_stdout
from copy import deepcopy
import gzip
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.m5_model_feasibility import (
    allowance_assessment, audit, capacity_envelopes, checked_file, main, model_estimates,
)


class ModelFeasibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capacity = json.loads(gzip.decompress(Path("tests/fixtures/capacity_report.json.gz").read_bytes()))

    def config(self, tied=False):
        return dict(tie_word_embeddings=tied, text_config=dict(
            tie_word_embeddings=tied, num_attention_heads=16, num_key_value_heads=4, head_dim=256,
            num_hidden_layers=32, layer_types=["linear_attention"] * 24 + ["full_attention"] * 8,
            vocab_size=248320, max_position_embeddings=262144,
            hidden_size=2560 if tied else 4096, intermediate_size=9216 if tied else 12288))

    def test_all_sizes_keep_proved_bounds_separate_from_constructed_fixtures(self):
        sizes = capacity_envelopes(self.capacity)
        for size, complete, fixture in [("target", 261388, 33490), ("fallback", 259868, 32913)]:
            self.assertEqual(sizes[size]["complete_resident_tokens_upper"], complete)
            self.assertEqual(sizes[size]["constructed_fixture_max_resident_tokens"], fixture)
            self.assertEqual(sizes[size]["complete_input_tokens_upper"], complete - 384)
            self.assertIsNone(sizes[size]["upper_bound_attainability"])
        self.assertEqual(len(sizes), 2)

    def test_missing_task_changed_limit_and_invalid_bound_are_rejected(self):
        for alter in ("limits", "coverage", "arithmetic", "reserve", "factor", "fit"):
            data = dict(self.capacity, limits=dict(self.capacity["limits"]),
                        accounting=deepcopy(self.capacity["accounting"]))
            if alter == "limits": data["limits"]["reserved_output"] = 128
            if alter == "coverage": data["accounting"].pop()
            if alter == "arithmetic": data["accounting"][0]["input_tokens_upper"] -= 1
            if alter == "reserve": data["accounting"][0]["with_output_reserve_upper"] -= 1
            if alter == "factor": data["accounting"][0]["input_tokens_per_payload_token_upper"]["own_replies"] = 1
            if alter == "fit": data["accounting"][0]["bound_fits"] = False
            with self.subTest(alter=alter), self.assertRaises(ValueError):
                capacity_envelopes(data)

    def test_tied_head_is_counted_once_and_kv_is_independent_of_model_width(self):
        large = model_estimates(self.config(), 262144)
        small = model_estimates(self.config(True), 262144)
        self.assertEqual(large["fp16_embedding_head_bytes"], 4068474880)
        self.assertEqual(small["fp16_embedding_head_bytes"], 1271398400)
        for result in (large, small):
            self.assertEqual(result["fp16_full_attention_kv_bytes"], 8 * 2**30)
            self.assertEqual(result["materialized_repeat_additional_bytes"], 4 * 2**30)
            self.assertEqual(result["proposed_kv_view_additional_storage_bytes"], 0)
            self.assertEqual(result["conditional_active_layer_cache_growth_pair_copy_bytes"], 2**30)
            self.assertIsNone(result["complete_allocator_upper_bound_bytes"])
            self.assertIsNone(result["measured_model_peak_bytes"])
            self.assertIsNone(result["full_envelope_memory_acceptance"])
        self.assertEqual(large["conditional_weight_kv_subtotal_bytes"], 15074328576)
        self.assertEqual(small["conditional_weight_kv_subtotal_bytes"], 10993795072)

    def test_chunk_bounds_pay_shared_mask_alignment_without_head_replication(self):
        result = model_estimates(self.config(True), 259868)
        self.assertEqual(result["chunk_query_bytes"], 2 * 2**20)
        self.assertEqual(result["chunk_output_bytes"], 2 * 2**20)
        self.assertEqual(result["conditional_aligned_shared_mask_storage_bytes"], 256 * 259872 * 2)
        self.assertEqual(result["conditional_mask_conversion_tensor_allowance_bytes"], 256 * 259872 * 6)

    def test_malformed_geometry_token_limit_and_contradictory_tie_are_rejected(self):
        for field, value in (("num_key_value_heads", 8), ("head_dim", 128), ("tie_word_embeddings", True)):
            config = self.config()
            config["text_config"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                model_estimates(config, 261388)
        for length in (0, True, 262145, 261388.0):
            with self.subTest(length=length), self.assertRaises(ValueError):
                model_estimates(self.config(), length)

    def test_subtotal_under_allowance_does_not_grant_fit_and_over_does_not_fail_model(self):
        devices = {"device_0": dict(torch_total_bytes=15636037632, post_probe_free_bytes=15458959360)}
        for tied, exceeds in ((False, True), (True, False)):
            subtotal = model_estimates(self.config(tied), 261388)["conditional_weight_kv_subtotal_bytes"]
            result = allowance_assessment(subtotal, devices)["device_0"]
            self.assertEqual(result["partial_subtotal_exceeds_native_allowance"], exceeds)
            self.assertIsNone(result["full_envelope_memory_acceptance"])
            self.assertEqual(result["native_total_minus_headroom_bytes"], 14025424896)
            self.assertEqual(result["historical_free_minus_headroom_bytes"], 13848346624)

    def test_inconsistent_or_coerced_device_memory_is_rejected(self):
        for total, free in [(10, 20), (15636037632, 15636037633), (15636037632.0, 0), (15636037632, True)]:
            with self.subTest(total=total, free=free), self.assertRaises(ValueError):
                allowance_assessment(100, dict(device_0=dict(torch_total_bytes=total, post_probe_free_bytes=free)))

    def test_corrupt_input_fails_before_creating_output_and_keeps_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / "input.zip", Path(folder) / "report.json"
            source.write_bytes(b"corrupt or wrong archive")
            with self.assertRaisesRegex(ValueError, "identity differs"):
                main(["--archive", str(source), "--output", str(output)])
            self.assertFalse(output.exists())
            self.assertEqual(source.read_bytes(), b"corrupt or wrong archive")

    def test_identity_check_and_existing_report_refuse_without_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / "report.json"
            report.write_bytes(b"original report")
            before = checked_file(report)
            with patch("scripts.m5_model_feasibility.audit") as audit, self.assertRaises(FileExistsError):
                main(["--output", str(report)])
            audit.assert_not_called()
            self.assertEqual(checked_file(report), before)
            with self.assertRaises(ValueError):
                checked_file(report, "0" * 64)

    def test_review_memory_changes_are_rejected_against_original_zip(self):
        original = Path("notebooks/validation/m5-t4-compatibility-run-6/validation.json")
        review = json.loads(original.read_bytes())
        review["devices"]["device_0"]["post_probe_free_bytes"] -= 1
        with tempfile.TemporaryDirectory() as folder:
            changed = Path(folder) / "changed-review.json"
            changed.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "original run-6 device bytes"):
                audit(Path("dist/m5-kaggle-preflight.zip"), Path("tests/fixtures/capacity_report.json.gz"),
                      Path("notebooks/run/6/preflight-results.zip"), changed)

    def test_report_writer_retains_unknown_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "report.json"
            data = dict(full_envelope_memory_acceptance=None, model_selected=None, model_generations=0,
                        allocation=dict(provider_duration_seconds=None, remaining_smoke_gpu_seconds=None))
            with patch("scripts.m5_model_feasibility.audit", return_value=data), redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--output", str(output)]), 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), data)


if __name__ == "__main__":
    unittest.main()
