"""Real hardware controller on scripted CPU providers and original native inputs."""

from contextlib import redirect_stdout
from dataclasses import asdict, dataclass
from functools import partial
import gzip
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from recovery.attempts import ProcessProvider
from recovery.inference import TokenizerFactory
from recovery.prompts import COURSE_LIMITS
from recovery.protocol import GeneratedReply
from recovery.storage import WorkerStore
from scripts.m5_course_smoke import CANDIDATE, check_hardware_plan, execute_requests
from scripts.m5_kaggle_preflight import utc

ROOT = Path(__file__).resolve().parents[1]
INCIDENT = ROOT/"notebooks/run/final-online-3/course-resume.payload"


def scripted_reply(view, rendered, tokenized, *, seed, settings):
    return GeneratedReply("{}", (91, 93), "eos", False)


@dataclass(frozen=True)
class ScriptedFactory:
    device: str

    def __call__(self):
        return scripted_reply


def forbidden_factory(device):
    return forbidden_start


def forbidden_start():
    raise AssertionError("A saved ordinary call must not load a provider")


class HardwareIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(INCIDENT) as archive:
            cls.packet = json.loads(gzip.decompress(archive.read(
                "source/notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")))
            cls.config = json.loads(archive.read("operator-config.json"))
            for name in archive.namelist():
                if name.startswith("source/metadata/4B/"):
                    Path(cls.metadata.name,Path(name).name).write_bytes(archive.read(name))
        cls.tokenizer = TokenizerFactory(CANDIDATE, cls.metadata.name, COURSE_LIMITS)()

    @classmethod
    def tearDownClass(cls):
        cls.metadata.cleanup()

    def launch(self):
        return dict(self.config, allocated_at=utc(), provider="kaggle", continuous_assignment=True,
            session_limit_seconds=1800, resource_policy="observe", resume_workers=[],
            authorization="CPU scripted controller check; no GPU/model provider")

    def run_controller(self, output, launch, *, factory=ScriptedFactory):
        # Same loop, SQLite and process provider as production. Only the model,
        # host command and CPU-only per-attempt timeout are replaced.
        with patch("scripts.m5_course_smoke.host_checks", return_value=dict(tests=3, skipped=0)), \
             patch("scripts.m5_course_smoke.EnvelopeFactory", ScriptedFactory), \
             patch("scripts.m5_course_smoke.ProcessProvider", partial(ProcessProvider,
                   timeout_seconds=5, termination_seconds=1)), redirect_stdout(io.StringIO()):
            return execute_requests(ROOT, self.packet, launch, ["CPU-fixture-0", "CPU-fixture-1"],
                output, tokenizer=self.tokenizer, factory=factory, complete_envelope=True)

    def test_real_native_plan_and_pinned_generation_processors(self):
        from tests.generation_checks import check_generation_contract
        self.assertEqual(check_hardware_plan(ROOT, self.packet, self.tokenizer)["constructors_checked"], 24)
        result = check_generation_contract(self.tokenizer, self.packet["settings"])
        self.assertEqual(result["checks"]["diagnostic"]["effective_eos"], [])
        self.assertTrue(result["checks"]["old_none"]["finite_check_rejected"])

    def test_full_24_row_controller_persists_two_envelopes_and_bounded_hang(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            result = self.run_controller(output, self.launch())
            self.assertIsNone(result["stop_reason"])
            self.assertEqual(result["completed_model_generations"], 23)
            self.assertEqual(result["resources"]["smoke_attempt_usage"]["total_recorded"], 25)
            for index in range(2):
                store = WorkerStore(output/f"worker-{index}.sqlite", readonly=True)
                try:
                    self.assertEqual(store.call(f"course-hardware/envelope/device-{index}")["status"], "completed")
                    self.assertFalse(any(p[0] is None for p in store.connection.execute("SELECT stopped_at FROM provider_processes")))
                finally:
                    store.close()
            store = WorkerStore(output/"worker-1.sqlite", readonly=True)
            try:
                self.assertEqual(store.call("smoke/course-m5/24")["status"], "timeout")
                self.assertEqual(len(store.attempts("smoke/course-m5/24")), 1)
            finally:
                store.close()
            # A controller interruption after the final persisted attempt must
            # reconstruct the complete matrix at 25, without another admission.
            from scripts.m5_kaggle_preflight import hardware_matrix_recorded
            paths = [output/f"worker-{i}.sqlite" for i in range(2)]
            self.assertTrue(hardware_matrix_recorded(paths))
            for path in paths:
                store = WorkerStore(path)
                try:
                    for a in store.connection.execute("SELECT number FROM allocations WHERE stopped_at IS NULL").fetchall():
                        store.allocation_observation_ended(a[0],at=utc(),reason="CPU fixture window ended")
                finally:
                    store.close()
            launch = dict(self.launch(),resume_in_place=True,resume_workers=[str(p) for p in paths])
            resumed = self.run_controller(output,launch,factory=forbidden_factory)
            self.assertIsNone(resumed["stop_reason"])
            self.assertEqual(resumed["resources"]["smoke_attempt_usage"]["total_recorded"],25)

    def test_original_21_are_reused_and_only_three_attempts_are_added(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            original = {}
            with zipfile.ZipFile(INCIDENT) as archive:
                for index in range(2):
                    path = output/f"worker-{index}.sqlite"
                    path.write_bytes(archive.read(f"hardware/worker-{index}.sqlite"))
                    store = WorkerStore(path, readonly=True)
                    try:
                        original.update({c["call_id"]:dict(c) for c in store.connection.execute("SELECT * FROM calls")})
                    finally:
                        store.close()
            launch = dict(self.launch(), resume_in_place=True,
                resume_workers=[str(output/f"worker-{i}.sqlite") for i in range(2)])
            result = self.run_controller(output, launch, factory=forbidden_factory)
            self.assertIsNone(result["stop_reason"])
            self.assertEqual(result["resources"]["smoke_attempt_usage"]["total_recorded"], 25)
            count = 0
            for index in range(2):
                store = WorkerStore(output/f"worker-{index}.sqlite", readonly=True)
                try:
                    for call_id, saved in original.items():
                        row = store.connection.execute("SELECT * FROM calls WHERE call_id=?", (call_id,)).fetchone()
                        if row is not None:
                            self.assertEqual(dict(row), saved)
                            count += 1
                    self.assertEqual(store.run_inputs["bounds"], dict(timeout_seconds=120, termination_seconds=1))
                finally:
                    store.close()
            self.assertEqual(count, 21)

    def test_pre_attempt_failure_keeps_original_parent_frame_and_attempt_flag(self):
        from scripts.m5_course_smoke import hardware_plan
        rows = hardware_plan(self.packet, self.tokenizer)
        rows[0]["rendered"]["system"] = "unsupported"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch("scripts.m5_course_smoke.hardware_plan", return_value=rows):
                result = self.run_controller(output, self.launch())
            self.assertIn("unexpected keyword argument 'system'", result["stop_reason"])
            error = json.loads(next(output.glob("controller-error-*.json")).read_bytes())
            self.assertEqual(error["phase"], "request_preparation")
            self.assertFalse(error["attempt_started"])
            self.assertIn("RenderedRequest(**row", error["traceback"])
            self.assertEqual(result["resources"]["smoke_attempt_usage"]["total_recorded"], 1)


if __name__ == "__main__":
    unittest.main()
