"""Affected integration: capability barrier and separately accounted memory probe."""

from dataclasses import replace
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS, RenderedRequest, TokenizedRequest
from recovery.runner import WorkerReader
from recovery.workers import LocalScheduler, WorkerSpec
from scripts.m5_course_preparation import read
from scripts.m5_course_smoke import hardware_plan
from tests.course_worker_cases import SETTINGS, branches, course_inputs, provider_factory, tokenizer_factory
from tests.inference_mocks import backend, mock_transformers

ROOT = Path(__file__).resolve().parents[1]


class WorkflowCoreTests(unittest.TestCase):
    def test_capability_barrier_reuses_full_binding_then_continues_same_workers(self):
        world = course_inputs()[0].development[0]
        selected = tuple(b for b in branches(world) if b.phase in ("prefix", "control") or
                         b.policy == "B" and b.event == "revision")
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory)/f"worker-{i}.sqlite" for i in range(2)]
            specs = [WorkerSpec(path, provider_factory) for path in paths]
            with LocalScheduler(specs, (world,), selected, tokenizer_factory, settings=SETTINGS,
                    timeout_seconds=8, regime="course") as scheduler:
                scheduler.run(capability_only=True)
                self.assertTrue(all(w.status == "done" for w in scheduler.status()
                                    if scheduler.by_branch[w.branch_id].phase != "continuation"))
                self.assertTrue(all(w.completed_round == 0 for w in scheduler.status()
                                   if scheduler.by_branch[w.branch_id].phase == "continuation"))
                first = scheduler.progress()["counts"]
                self.assertEqual(first["finished_generations"], 18)
                scheduler.run()
                self.assertEqual(scheduler.progress()["counts"]["finished_generations"], 34)
            with LocalScheduler(specs, (world,), selected, tokenizer_factory, settings=SETTINGS,
                    timeout_seconds=8, regime="course") as scheduler:
                scheduler.run()
                self.assertEqual(scheduler.progress()["counts"]["attempts"], 34)
            for path in paths:
                reader = WorkerReader(path)
                try:
                    self.assertEqual(len(reader.store.run_inputs["branches"]), len(selected))
                finally:
                    reader.close()

    def test_envelope_plan_has_two_new_diagnostic_ids_within_24_attempts(self):
        packet = read(ROOT/"notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")
        from tests.inference_mocks import Tokenizer
        rows = hardware_plan(packet, Tokenizer())
        for row in rows:
            RenderedRequest(**row["rendered"])
            TokenizedRequest(**row["tokenized"])
        self.assertEqual(len(rows), 24)
        self.assertEqual(len({r["physical_generation_id"] for r in rows}), 24)
        probes = [r for r in rows if r.get("hardware_diagnostic")]
        self.assertEqual([r["intended_worker"] for r in probes], [0, 1])
        self.assertTrue(all(r["input_tokens"]+256 == 110107 for r in probes))
        self.assertNotIn("hardware_diagnostic", packet["requests"][21])
        self.assertTrue(rows[-1]["controlled_hang"])

    def test_envelope_uses_same_cache_finite_path_and_forces_only_diagnostic_output(self):
        value = backend()
        value.limits = COURSE_LIMITS
        value.settings = candidate_settings(value.tokenizer, QWEN_4B, limits=COURSE_LIMITS)
        value.model.reply_ids = (ord("a"),)*256
        tokens = TokenizedRequest("diagnostic", (ord("a"),)*109851, (1,)*109851)
        with patch.dict(sys.modules, transformers=mock_transformers()):
            result = value.probe_envelope(tokens, seed=71)
        self.assertTrue(result.backend["hardware_diagnostic"])
        self.assertEqual(len(result.response.token_ids), 256)
        self.assertTrue(result.backend["cache"]["initial_empty"])
        self.assertEqual(value.model.calls[-1]["config"]["eos_token_id"], [])
        self.assertEqual(value.settings["generation"]["eos_token_id"], [248044, 248046])
        with self.assertRaises(ValueError):
            value.probe_envelope(replace(tokens, input_ids=(1,)), seed=71)


if __name__ == "__main__":
    unittest.main()
