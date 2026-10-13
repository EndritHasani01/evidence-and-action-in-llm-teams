"""Incident-specific recovery, counter and online-transfer checks; CPU only."""

from contextlib import closing, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import time
import sys
import traceback
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from recovery.accounting import BudgetStop
from recovery.storage import WorkerStore
from scripts.course_kaggle_workflow import run_all
from scripts.course_kaggle_bootstrap import online
from scripts.m5_course_smoke import admission
from scripts.m5_kaggle_preflight import download_native_ranges, smoke_attempt_usage, smoke_attempt_limit, utc
from scripts.build_course_kaggle import notebook

ROOT = Path(__file__).resolve().parents[1]


def config():
    value = json.loads((ROOT / "configs/course-kaggle.json").read_bytes())
    value.update(resource_policy="observe", execute_gpu=True, allocated_at=utc(), max_work_seconds=36000)
    value["authorizations"] = {key: "CPU fixture only" for key in value["authorizations"]}
    return value


class CourseRepairTests(unittest.TestCase):
    def test_prior_count_is_enforced_and_only_the_named_allowance_is_accepted(self):
        launch = config() | dict(authorization="CPU fixture only", session_limit_seconds=36000)
        launch["budget"]["prior_smoke_attempts"] = 25
        with self.assertRaisesRegex(BudgetStop, "recorded_smoke_attempt_limit"):
            admission(launch, next_attempt=True)
        self.assertEqual(smoke_attempt_limit(launch), 25)
        launch["smoke_attempt_limit"] = 100
        with self.assertRaises(ValueError):
            smoke_attempt_limit(launch)
        launch["smoke_attempt_limit"] = 25
        launch["smoke_attempt_allowance"] = "unapproved reset"
        with self.assertRaises(ValueError):
            smoke_attempt_limit(launch)
        launch.pop("smoke_attempt_limit")
        self.assertEqual(smoke_attempt_limit(launch), 24)

    def test_backups_and_predecessor_bound_are_counted_once(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("CREATE TABLE attempts(call_id TEXT,number INTEGER,started_at TEXT)")
                db.executemany("INSERT INTO attempts VALUES(?,?,?)", [("same-call", 1, "old"), ("same-call", 2, "new")])
            backup = path.with_name("backup.sqlite")
            shutil.copyfile(path, backup)
            prior = dict(prior_smoke_attempts=2, prior_evidence="Original predecessor rows, CPU fixture")
            self.assertEqual(smoke_attempt_usage(prior, prior_paths=[path, backup, path])["total_recorded"], 2)
            self.assertEqual(smoke_attempt_usage({}, [path, backup, path])["total_recorded"], 2)
            # Same logical call in a different execution has a different original
            # attempt start; it must not be mistaken for a copied backup.
            with closing(sqlite3.connect(backup)) as db, db:
                db.execute("UPDATE attempts SET started_at='another run' WHERE number=1")
            self.assertEqual(smoke_attempt_usage({}, [path, backup])["total_recorded"], 3)

    def test_exhausted_allowance_stops_before_any_download_or_prepare(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); cfg = config(); cfg["budget"]["prior_smoke_attempts"] = 25
            (root / "source-manifest.json").write_text("{}")
            config_path = root / "operator-config.json"; config_path.write_text(json.dumps(cfg))
            with patch("scripts.course_kaggle_bootstrap.source_identity"), \
                 patch("scripts.m5_course_smoke_assets.prepare") as prepare:
                with self.assertRaisesRegex(ValueError, "limit_before_downloads"):
                    online(root, config_path, root / "scratch", root / "output")
                prepare.assert_not_called()

    def test_known_hardware_defect_stops_before_cold_setup_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root/"hardware").mkdir()
            (root/"hardware/report.json").write_text(json.dumps(dict(smoke=dict(stop_reason="ProviderDefect: original error"))))
            (root/"source-manifest.json").write_text("{}")
            p = root/"operator-config.json"; p.write_text(json.dumps(config()))
            with patch("scripts.course_kaggle_bootstrap.source_identity"), \
                 patch("scripts.m5_course_smoke_assets.prepare") as prepare:
                with self.assertRaisesRegex(ValueError,"saved_hardware_failure_before_downloads"):
                    online(root,p,root/"scratch",root/"output")
                prepare.assert_not_called()

    def test_literal_notebook_rebuilds_failed_setup_without_removing_old_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory); bundle=workspace/"bundle"; bundle.mkdir()
            source=bundle/"source"; source.mkdir()
            original=workspace/"cpu-environment/bootstrap"; original.mkdir(parents=True)
            previous=dict(status="blocked",reason="Interrupted CPU setup")
            (original/"bootstrap.json").write_text(json.dumps(previous))
            log=original/"original.stderr.txt"; log.write_text("original setup traceback")
            cfg=config(); cfg["execute_gpu"]=False
            p=bundle/"operator-config.json"; p.write_text(json.dumps(cfg))
            calls=[]
            def child(arguments,limit):
                calls.append(arguments)
                if "--output" in arguments:
                    output=Path(arguments[arguments.index("--output")+1]); output.mkdir(parents=True)
                    (output/"bootstrap.json").write_text(json.dumps(dict(status="prepared",interpreter=sys.executable)))
                else:
                    (bundle/"last-action.json").write_text(json.dumps(dict(status="limited_result",reason="CPU fixture")))
                return 0
            code="".join(next(c for c in notebook('f'*64,'a'*40)['cells'] if c['id']=='execute')['source'])
            # Execute the literal orchestration body with a controlled child,
            # exercising its real filesystem/retry/receipt handling without pip.
            body=code[code.index("\ntry:\n"):]
            values=dict(SOURCE_READY=True,source=source,workspace=workspace,bundle=bundle,
                CONFIG=cfg,config_path=p,ACTION="run_all",ENABLE_GPU=False,ASSETS_ZIP=None,
                bounded_child=child,Path=Path,json=json,sys=sys,shutil=shutil,time=time,
                traceback=traceback,attached=lambda *args:None,inputs=workspace/"input")
            with redirect_stdout(io.StringIO()): exec(body,values)
            result=json.loads((bundle/"last-action.json").read_bytes())
            self.assertEqual(result['reason'],"CPU fixture",result)
            self.assertEqual(log.read_text(),"original setup traceback")
            self.assertEqual(len(list(original.glob("bootstrap-before-*.json"))),1)
            current=json.loads((original/"bootstrap.json").read_bytes())
            self.assertEqual(current['status'],"prepared")
            self.assertEqual(len(calls),2)
            self.assertIn("retry-",str(calls[0][calls[0].index("--output")+1]))

    def test_transient_transfer_retries_same_range_and_reuses_only_verified_cache(self):
        data = b"native CPU fixture"
        class Response(io.BytesIO):
            status = 206
            headers = {"Content-Range": f"bytes 0-{len(data)-1}/{len(data)}"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.bin"; digest = hashlib.sha256(data).hexdigest()
            error = HTTPError("https://fixture.invalid", 503, "transient", {}, None)
            with patch("urllib.request.urlopen", side_effect=[error, Response(data)]) as request, \
                 patch("scripts.m5_kaggle_preflight.time.sleep"), redirect_stdout(io.StringIO()):
                download_native_ranges("https://fixture.invalid", path, len(data), digest)
            self.assertEqual(request.call_count, 2)
            self.assertEqual(request.call_args_list[0].args[0].get_header("Range"), request.call_args_list[1].args[0].get_header("Range"))
            self.assertEqual(path.read_bytes(), data)
            with patch("urllib.request.urlopen") as request, redirect_stdout(io.StringIO()):
                download_native_ranges("https://fixture.invalid", path, len(data), digest)
                request.assert_not_called()
                path.write_bytes(b"corrupted")
                with self.assertRaisesRegex(ValueError, "cached asset identity"):
                    download_native_ranges("https://fixture.invalid", path, len(data), digest)
                request.assert_not_called()

    def exercise_failure(self, reason, *, recoverable=False):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory); hardware = bundle / "hardware"; hardware.mkdir()
            (hardware / "report.json").write_text(json.dumps(dict(smoke=dict(stop_reason=reason))))
            if recoverable:
                for index in range(2):
                    with closing(WorkerStore(hardware / f"worker-{index}.sqlite")):
                        pass
            with patch("scripts.course_kaggle_workflow.session_window", return_value=3600), \
                 patch("scripts.course_kaggle_workflow.hardware", return_value=dict(root_blocker="CPU resumed stop")) as execute, \
                 patch("scripts.course_kaggle_workflow.record_refused_allocation"), \
                 patch("scripts.course_kaggle_workflow.backup_bundle"), \
                 patch("scripts.course_kaggle_workflow.analyze", return_value=dict(status="feasibility")), \
                 redirect_stdout(io.StringIO()):
                result = run_all(ROOT, bundle, config())
            trace = json.loads((bundle / "logs/workflow-error.json").read_bytes())
            self.assertEqual(result["status"], "limited_result")
            self.assertIn("Traceback", trace["traceback"])
            self.assertEqual(execute.call_count, int(recoverable))
            return result

    def test_failed_report_retains_root_error_and_does_not_resample(self):
        result = self.exercise_failure("ProviderDefect: AttributeError: missing hf_device_map")
        self.assertIn("missing hf_device_map", result["reason"])

    def test_interrupted_hardware_report_resumes_existing_stage(self):
        result = self.exercise_failure("KeyboardInterrupt: operator interruption", recoverable=True)
        self.assertIn("CPU resumed stop", result["reason"])


if __name__ == "__main__":
    unittest.main()
