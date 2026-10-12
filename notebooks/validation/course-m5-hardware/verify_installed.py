"""Reuse the ordinary-wheel audit for the four affected persistence checks."""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
audit = runpy.run_path(str(ROOT / "notebooks/validation/course-m5-preparation/verify_installed.py"))
audit["main"].__globals__["SUITES"] = [
    "tests.test_course_hardware_smoke.CourseHardwareSmokeTests.test_isolated_smoke_uses_actual_peer_and_exact_identity_without_relabelled_controls",
    "tests.worker_checks.ParentAccessTests.test_controls_are_durable_empty_send_full_shape_and_reject_input_drift",
    "tests.durable_checks.DurableTests.test_checkpoint_write_failure_before_and_after_commit_has_one_authoritative_effect",
    "tests.attempt_checks.ProcessAttemptTests.test_interrupted_backend_retries_identical_inputs_and_preserves_ambiguous_completed_work",
]

if __name__ == "__main__":
    raise SystemExit(audit["main"]())
