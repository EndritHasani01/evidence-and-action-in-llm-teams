"""Independent course packet/resource/memory checks; no inference dependencies."""

from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from recovery.manifests import load_population
from recovery.prompts import COURSE_LIMITS
from recovery.state import OwnReply, ReceivedProse
from recovery.tasks import Task
from scripts.build_course_smoke_packet import notebook, preparation_review
from scripts.build_kaggle_bundle import BASELINE_COMMIT, archive_manifest
from scripts.m5_course_preparation import course_envelope, memory_review, peer_view, read, verify_requests

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "notebooks/validation/course-m5-preparation"


class CourseSmokePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capacity = read(ROOT/"tests/fixtures/course_capacity.json.gz")
        cls.inspection = read(EVIDENCE/"candidate-inspection-accepted.json")
        cls.run6 = read(ROOT/"notebooks/validation/m5-t4-compatibility-run-6/validation.json")
        cls.packet = read(EVIDENCE/"inputs/smoke-requests.json.gz")

    def test_complete_bound_does_not_collapse_to_short_stress_requests(self):
        envelope = course_envelope(self.capacity)
        self.assertEqual(envelope["resident_tokens_upper"], 7*256*48+21*64*45+9430+69+256)
        self.assertEqual(envelope["resident_tokens_upper"], 156251)
        self.assertLess(max(r["resident_tokens_with_reserve"] for r in self.packet["requests"]), 23000)
        self.assertIsNone(envelope["upper_bound_attainability"])
        for key, value in (("limits", asdict(COURSE_LIMITS)|dict(prose_tokens=128)),
                           ("resident_tokens_upper", 22503)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                course_envelope(dict(self.capacity, **{key:value}))
        changed = deepcopy(self.capacity)
        changed["accounting"].pop()
        with self.assertRaises(ValueError):
            course_envelope(changed)

    def test_full_language_inventory_and_known_storage_leave_r7_unknown(self):
        actual = memory_review(self.capacity, self.inspection, self.run6)
        terms = actual["known_or_conditional_tensor_components"]
        # Independent architecture arithmetic: 96 MLP, 32 full-attention and 120 linear-attention matrices.
        h, intermediate = 2560, 9216
        parameters = 32*3*h*intermediate + 8*h*(8192+1024+1024+4096) + 24*h*(8192+4096+32+32+4096)
        self.assertEqual(terms["ideally_packed_nf4_all_linear_bytes"], parameters//2)
        self.assertEqual(terms["fp16_tied_embedding_head_bytes"], 248320*h*2)
        self.assertEqual(terms["fp16_full_attention_kv_bytes"], 156251*8*4*256*2*2)
        self.assertEqual(terms["fp32_recurrent_state_bytes"], 24*32*128*128*4)
        self.assertEqual(terms["active_layer_kv_growth_pair_copy_bytes"], 156251*4*256*2*2)
        self.assertEqual(terms["shared_mask_conversion_alignment_bytes"], 256*156256*6)
        self.assertIsNone(actual["complete_live_memory_upper_bound_bytes"])
        self.assertIsNone(actual["actual_headroom_acceptance"])
        self.assertFalse(actual["preparation_admitted"])
        self.assertFalse(actual["weight_staging_permitted"])
        self.assertFalse(actual["terminal_model_feasibility_failure"])
        for device in actual["devices"].values():
            self.assertGreater(device["remaining_for_omitted_terms_bytes"], 0)
            self.assertIsNone(device["current_free_bytes"])

    def test_inconsistent_or_unverified_shape_inventory_is_rejected(self):
        for key, value in (("actual_language_weights_loaded", True), ("revision", "main"),
                           ("total_unique_language_parameters", 1)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                memory_review(self.capacity, dict(self.inspection, **{key:value}), self.run6)
        changed = deepcopy(self.inspection)
        next(iter(changed["language_parameters"].values()))["elements"] += 1
        with self.assertRaises(ValueError):
            memory_review(self.capacity, changed, self.run6)

    @unittest.skipUnless(importlib.util.find_spec("pydantic"), "optional parser required to reconstruct saved views")
    def test_all_24_origins_are_saved_development_and_keep_call_owned_views(self):
        self.assertEqual(verify_requests(ROOT, self.packet)["verified_requests"], 24)
        worlds = {w.world_id: w for w in load_population(ROOT/"tests/fixtures/population_course.json").development}
        rows = self.packet["requests"]
        self.assertEqual([r["view"]["task"] for r in rows[:5]], [t.value for t in Task])
        for row in rows[:5]:
            world = worlds[row["development_world_id"]].world
            view = peer_view(row["view"])
            self.assertEqual({r.record_id for r in view.sources}, {r.record_id for r in world.records if r.owner == 0})
            self.assertEqual(view.history, ())
            self.assertNotIn(row["origin_call_id"], row["rendered"]["content"])
        self.assertEqual([r["view"]["peer"] for r in rows[5:8]], [None]*3)
        self.assertEqual([r["view"]["peer"] for r in rows[13:17]], list(range(4)))
        for row in rows[13:17]:
            view = peer_view(row["view"])
            self.assertEqual(view.history, ())
            self.assertIsNotNone(view.notice)
        for row in rows[17:19]:
            view = peer_view(row["view"])
            self.assertEqual(sum(isinstance(e, OwnReply) for e in view.history), 7)
            self.assertEqual(sum(isinstance(e, ReceivedProse) for e in view.history), 21)
            self.assertEqual(len(row["own_physical_ids_per_slot"]), 256)
        q = peer_view(rows[18]["view"])
        release = [e.slot.round_number for e in q.history if isinstance(e, ReceivedProse) and e.slot.phase == "recovery"]
        self.assertEqual(release, [1]*3+[2]*3+[3]*3)

    @unittest.skipUnless(importlib.util.find_spec("pydantic"), "optional parser required to reconstruct saved views")
    def test_request_drift_and_relabelled_pilot_or_executed_results_are_rejected(self):
        for key, value in (("origin_call_id", "main-prefix_sum-01/prefix/original/none/rep0/r1/p0"),
                           ("seed", 0), ("executed", True), ("outcome", "correct")):
            packet = deepcopy(self.packet)
            packet["requests"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_requests(ROOT, packet)
        packet = deepcopy(self.packet)
        packet["requests"][22]["tokenized"]["input_ids"][0] += 1
        with self.assertRaisesRegex(ValueError, "A/order/restart"):
            verify_requests(ROOT, packet)

    def test_unknown_prior_attempts_and_allocation_cannot_become_new_allowance(self):
        for key in ("prior_attempts", "prior_allocated_gpu_seconds", "remaining_smoke_attempts",
                    "remaining_smoke_gpu_seconds", "provider_quota", "provider_duration"):
            self.assertIsNone(self.packet[key])
        self.assertEqual(self.packet["max_physical_attempts_including_prior"], 24)
        self.assertEqual(self.packet["max_aggregate_allocated_gpu_seconds_including_prior"], 1800)
        self.assertEqual(self.packet["worst_retry_bounded_call_wall_seconds"], 2*(120+2))
        self.assertEqual(self.packet["required_safe_release_wall_seconds"], 120)
        self.assertFalse(self.packet["inference_executable"])

    def test_new_source_marker_is_explicit_and_original_transport_default_stays_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"source.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("SOURCE_COMMIT.txt", "a"*40+"\n")
            with self.assertRaisesRegex(ValueError, "source_baseline_marker"):
                archive_manifest(path)
            manifest = archive_manifest(path, source_commit="a"*40, payload_name="course-m5-source.payload")
            self.assertEqual(manifest["source_baseline_commit"], "a"*40)
            self.assertNotEqual(manifest["source_baseline_commit"], BASELINE_COMMIT)
            self.assertEqual(manifest["archive_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            for commit, name in (("main", "course.payload"), ("a"*40, "../escape.payload")):
                with self.assertRaises(ValueError):
                    archive_manifest(path, source_commit=commit, payload_name=name)

    def test_review_notebook_is_unexecuted_and_keeps_the_gate_withheld(self):
        helper = "marker='reused helper'\n"
        document = notebook(dict(review_helper_sha256=hashlib.sha256(helper.encode()).hexdigest()), helper)
        self.assertEqual(document["nbformat"], 4)
        for cell in document["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), cell["id"], "exec")
                self.assertEqual(cell["outputs"], [])
                self.assertIsNone(cell["execution_count"])
        text = "".join("".join(c["source"]) for c in document["cells"])
        self.assertIn("Accelerator **None**", text)
        self.assertIn("weight_staging_permitted", text)
        self.assertNotIn("ModelFactory", text)
        self.assertNotIn("run_preflight", text)

    def test_preparation_completion_keeps_physical_acceptance_and_execution_pending(self):
        review = preparation_review(ROOT)
        self.assertEqual(review["status"], "prepared")
        self.assertTrue(review["preparation_complete"])
        self.assertEqual(review["complete_input_tokens_upper"], 109851)
        self.assertEqual(review["complete_resident_tokens_upper"], 110107)
        self.assertEqual(review["conditional_tensor_component_sum_bytes"], 7400914336)
        self.assertEqual(review["conditional_loading_tensor_allowance_bytes"], 3214021348)
        self.assertEqual(review["physical_memory_acceptance_task"], "course/M5-T02")
        for key in ("physical_memory_accepted", "weight_staging_permitted", "gpu_admission",
                    "terminal_model_feasibility_failure"):
            self.assertIs(review[key], False)
        self.assertIsNone(review["complete_live_memory_upper_bound_bytes"])
        self.assertIsNone(review["actual_headroom_acceptance"])

    def test_preparation_rejects_proof_drift_and_invented_hardware_acceptance(self):
        cases = (("native-tightening-source.json", "revision", "different"),
                 ("native-tightening-source.json", "tokenizer_sha256", "0"*64),
                 ("outside-provenance.json", "proof_sha256", "0"*64),
                 ("outside-provenance.json", "source_pythonpath", True),
                 ("loading-review-source.json", "skips", 1),
                 ("offline-memory-review.json", "actual_headroom_acceptance", True),
                 ("offline-memory-review.json", "preparation_admitted", True),
                 ("loading-review-source.json", "weight_staging_permitted", True),
                 ("loading-review-source.json", "terminal_model_feasibility_failure", True))
        for filename, key, value in cases:
            def changed(path):
                result = read(path)
                if Path(path).name == filename:
                    result[key] = value
                return result
            with self.subTest(filename=filename, key=key), \
                    patch("scripts.build_course_smoke_packet.read", side_effect=changed), self.assertRaises(ValueError):
                preparation_review(ROOT)
