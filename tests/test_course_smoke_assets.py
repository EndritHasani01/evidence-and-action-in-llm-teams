"""Pinned asset/provenance guards using tiny CPU files, never model weights."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
import io
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.m5_course_smoke import CANDIDATE, launch_defaults
from scripts.m5_course_smoke_assets import prepare, source_identity, verify_assets, assigned_preparation_window
from scripts.build_course_hardware_packet import hardware_notebook


def item(data):
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())


class CourseSmokeAssetTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)/"source"
        root.mkdir()
        commit = "a"*40
        marker = (commit+"\n").encode()
        (root/"SOURCE_COMMIT.txt").write_bytes(marker)
        manifest = dict(source_baseline_commit=commit,members={"SOURCE_COMMIT.txt":item(marker)})
        manifest_path = Path(directory)/"manifest.json"
        manifest_path.write_text(json.dumps(manifest))
        installed = Path(directory)/"installed/recovery"
        installed.mkdir(parents=True)
        module = b"# CPU fixture, not production\n"
        (installed/"inference.py").write_bytes(module)
        cache = Path(directory)/"hub"
        snapshot = cache/"models--Qwen--Qwen3.5-4B"/"snapshots"/CANDIDATE.revision
        snapshot.mkdir(parents=True)
        data = b"tiny CPU asset fixture; not tensor weights"
        (snapshot/"config.json").write_bytes(data)
        assets = dict(source_commit=commit,model=CANDIDATE.model,revision=CANDIDATE.revision,
            versions={"fixture-package":"1"},installed_modules={"inference.py":item(module)["sha256"]},
            checkpoint_files={"config.json":item(data)})
        receipt = Path(directory)/"assets.json"
        receipt.write_text(json.dumps(assets))
        launch = launch_defaults() | dict(source_manifest=str(manifest_path),assets_receipt=str(receipt),hf_cache=str(cache))
        return root,manifest,launch,installed,snapshot,assets,receipt

    def test_exact_source_and_assets_bind_installed_code_and_do_not_accept_gpu_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,launch,installed,snapshot,assets,receipt = self.fixture(directory)
            with patch("recovery.__file__",str(installed/"__init__.py")), \
                    patch("scripts.m5_course_smoke_assets.importlib.metadata.version",return_value="1"):
                result = verify_assets(root,launch)
            self.assertEqual(result["source_commit"],manifest["source_baseline_commit"])
            self.assertEqual(result["matching_modules"],1)
            self.assertFalse(result["gpu_memory_accepted"])

    def test_code_checkpoint_and_package_drift_are_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,launch,installed,snapshot,assets,receipt = self.fixture(directory)
            with patch("recovery.__file__",str(installed/"__init__.py")), \
                    patch("scripts.m5_course_smoke_assets.importlib.metadata.version",return_value="1"):
                (installed/"inference.py").write_bytes(b"changed code")
                with self.assertRaisesRegex(ValueError,"installed production"):
                    verify_assets(root,launch)
                (installed/"inference.py").write_bytes(b"# CPU fixture, not production\n")
                (snapshot/"config.json").write_bytes(b"changed checkpoint")
                with self.assertRaisesRegex(ValueError,"checkpoint asset"):
                    verify_assets(root,launch)
            with patch("scripts.m5_course_smoke_assets.importlib.metadata.version",return_value="2"):
                with self.assertRaisesRegex(ValueError,"candidate package"):
                    verify_assets(root,launch)

    def test_source_marker_and_bytes_cannot_be_relabelled(self):
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,*rest = self.fixture(directory)
            source_identity(root,manifest)
            changed = deepcopy(manifest)
            changed["source_baseline_commit"] = "b"*40
            with self.assertRaisesRegex(ValueError,"source commit"):
                source_identity(root,changed)
            (root/"SOURCE_COMMIT.txt").write_bytes(("a"*40+"\n# changed").encode())
            with self.assertRaises(ValueError):
                source_identity(root,manifest)

    def test_default_staging_is_disabled_and_exports_no_fabricated_fit_or_weights(self):
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,launch,*rest = self.fixture(directory)
            output, scratch = Path(directory)/"output",Path(directory)/"scratch"
            with patch("scripts.m5_course_smoke_assets.command",side_effect=AssertionError("no subprocess")):
                result = prepare(root,manifest,launch,scratch,output)
            self.assertEqual(result["status"],"blocked")
            self.assertFalse(result["weights_staged"])
            self.assertFalse(result["gpu_execution"])
            self.assertFalse(scratch.exists())
            self.assertTrue((output/"preflight-results.zip").is_file())
            with self.assertRaises(FileExistsError):
                prepare(root,manifest,launch,scratch,output)

    def test_delivered_notebook_has_disabled_defaults_and_bounded_child_execution(self):
        helper = "marker='CPU-only fixture'\n"
        document = hardware_notebook(dict(review_helper_sha256=hashlib.sha256(helper.encode()).hexdigest()),helper,launch_defaults())
        for cell in document["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]),cell["id"],"exec")
                self.assertEqual(cell["outputs"],[])
                self.assertIsNone(cell["execution_count"])
        text = "".join("".join(cell["source"]) for cell in document["cells"])
        self.assertIn("T4 x2 before starting",text)
        gpu = next("".join(c["source"]) for c in document["cells"] if c["id"] == "hardware-gpu-smoke")
        self.assertNotIn("LAUNCH['execute_gpu'] =",gpu)
        self.assertNotIn("LAUNCH['allocated_at'] =",gpu)
        self.assertIn("assigned_preparation_window",text)
        self.assertIn("Stop Session",text)
        self.assertIn("bounded-model-smoke",text)
        self.assertIn("provider_release_confirmed=False",text)
        self.assertNotIn("ModelFactory(",text)

    def test_controlled_cpu_stager_keeps_runtime_and_build_setuptools_separate(self):
        from tests.test_course_hardware_smoke import known_launch
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,launch,*rest = self.fixture(directory)
            inspection = root/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json"
            inspection.parent.mkdir(parents=True)
            inspection.write_text(json.dumps(dict(checkpoint_index=dict(total_checkpoint_bytes=1))))
            data = io.BytesIO()
            with zipfile.ZipFile(data,"w") as archive:
                archive.writestr("fixture.txt","controlled CPU wheel, not a package")
            wheel_bytes = data.getvalue()
            def wheel(name,version):
                return dict(name=name,version=version,filename=f"{name}-{version}-fixture.whl",
                    url=f"https://files.pythonhosted.org/{name}-{version}.whl",**item(wheel_bytes))
            runtime, build, pip, tool = wheel("setuptools","81.0.0"),wheel("setuptools","84.0.0"),wheel("pip","26.2.1"),wheel("wheel","0.48.0")
            manifest.update(candidate_wheels=[runtime],build_tools={name:dict(version=w["version"],wheels=[w])
                for name,w in (("setuptools",build),("pip",pip),("wheel",tool))})
            launch = known_launch() | dict(stage_weights=True)
            launch["allocated_at"] = None
            scratch,output = Path(directory)/"scratch",Path(directory)/"output"
            captured = {}
            def command(output,name,args,**kwargs):
                if name in ("download-pip","download-candidate","download-build-tools"):
                    for w in (runtime,build,pip,tool):
                        (scratch/"wheels"/w["filename"]).write_bytes(wheel_bytes)
                if name == "install-candidate":
                    captured["runtime_lock"] = (scratch/"install.lock").read_text()
                if name == "build-project":
                    captured["build_constraints"] = (scratch/"build-constraints.txt").read_text()
                    (scratch/"built"/"recovery_fixture.whl").write_bytes(wheel_bytes)
                if name == "installed-provenance":
                    (output/"installed.json").write_text(json.dumps(dict(versions={"setuptools":"81.0.0"},
                        verified_module_hashes={},qwen_text_class="Qwen3_5ForCausalLM",torch_cuda_build="12.8",model_generations=0)))
                if name == "stage-pinned-checkpoint":
                    (output/"weights.json").write_text(json.dumps(dict(checkpoint_files={},gpu_execution=False)))
                return dict(status="passed",kind="controlled CPU command fixture; no downloads or GPU")
            with patch("scripts.m5_course_smoke_assets.command",side_effect=command), \
                    patch("scripts.m5_course_smoke_assets.require_space",return_value={}), \
                    patch("scripts.m5_course_smoke_assets.platform.system",return_value="Linux"), \
                    patch("scripts.m5_course_smoke_assets.platform.machine",return_value="x86_64"), \
                    patch("scripts.m5_course_smoke_assets.sys.version_info",(3,13)):
                result = prepare(root,manifest,launch,scratch,output)
            self.assertEqual(result["status"],"prepared",result)
            self.assertIn("setuptools==81.0.0",captured["runtime_lock"])
            self.assertNotIn("84.0.0",captured["runtime_lock"])
            self.assertIn("setuptools==84.0.0",captured["build_constraints"])
            self.assertFalse(result["gpu_execution"])
            self.assertFalse(result["model_weights_loaded"])
            # The same tiny-file pipeline also permits an already-assigned host.
            # No package download, CUDA initialization or actual allocation occurs.
            from scripts.m5_kaggle_preflight import utc
            launch["allocated_at"] = utc()
            scratch,output = Path(directory)/"assigned-scratch",Path(directory)/"assigned-output"
            timeouts = []
            def assigned_command(*args,**kwargs):
                timeouts.append(kwargs["timeout"])
                return command(*args,**kwargs)
            with patch("scripts.m5_course_smoke_assets.command",side_effect=assigned_command), \
                    patch("scripts.m5_course_smoke_assets.assigned_device_count",return_value=2), \
                    patch("scripts.m5_course_smoke_assets.require_space",return_value={}), \
                    patch("scripts.m5_course_smoke_assets.platform.system",return_value="Linux"), \
                    patch("scripts.m5_course_smoke_assets.platform.machine",return_value="x86_64"), \
                    patch("scripts.m5_course_smoke_assets.sys.version_info",(3,13)):
                assigned_result = prepare(root,manifest,launch,scratch,output)
            self.assertEqual(assigned_result["status"],"prepared",assigned_result)
            self.assertEqual(assigned_result["assigned_device_count"],2)
            self.assertEqual(assigned_result["provider_assignment_utc"],launch["allocated_at"])
            self.assertTrue(all(0 < timeout <= 565 for timeout in timeouts))
            self.assertFalse(assigned_result["provider_release_confirmed"])

    def test_assigned_preparation_charges_the_original_clock_and_preserves_release_time(self):
        from tests.test_course_hardware_smoke import known_launch
        from scripts.m5_course_smoke import admission
        launch = known_launch()
        now = "2026-10-12T10:01:00+00:00"
        self.assertEqual(assigned_preparation_window(launch,now),840)
        self.assertEqual(assigned_preparation_window(launch,now),admission(launch,now=now)[1])
        launch["budget"]["prior_smoke_gpu_hours"] = [.3,.3]
        self.assertEqual(assigned_preparation_window(launch,launch["allocated_at"]),360)
        with self.assertRaisesRegex(ValueError,"insufficient_remaining_time"):
            assigned_preparation_window(launch,now)
        launch = known_launch()
        launch["budget"]["prior_setup_gpu_hours"] = None
        with self.assertRaisesRegex(ValueError,"supported_prior"):
            assigned_preparation_window(launch,now)
        launch = known_launch()
        launch["budget"]["prior_setup_gpu_hours"] = [2.1,2.1]
        with self.assertRaisesRegex(ValueError,"insufficient_remaining_time"):
            assigned_preparation_window(launch,now)

    def test_assigned_host_without_actual_clock_stops_before_environment_or_downloads(self):
        from tests.test_course_hardware_smoke import known_launch
        with tempfile.TemporaryDirectory() as directory:
            root,manifest,*rest = self.fixture(directory)
            launch = known_launch() | dict(stage_weights=True,allocated_at=None)
            scratch,output = Path(directory)/"scratch",Path(directory)/"output"
            with patch("scripts.m5_course_smoke_assets.assigned_device_count",return_value=2), \
                    patch("scripts.m5_course_smoke_assets.command") as command:
                result = prepare(root,manifest,launch,scratch,output)
            command.assert_not_called()
            self.assertFalse(scratch.exists())
            self.assertEqual(result["assigned_device_count"],2)
            self.assertIn("actual_provider_assignment_clock_required",result["root_blocker"])
            self.assertFalse(result["provider_release_confirmed"])

    def test_installed_admission_does_not_reset_an_existing_assignment_clock(self):
        from tests.test_course_hardware_smoke import known_launch
        import scripts.m5_course_smoke as smoke
        launch = known_launch()
        args = ["smoke","--root","fixture","--launch","launch.json","--output","admission.json","--check-admission-only"]
        with patch.object(smoke.sys,"argv",args), patch.object(smoke,"read",return_value=launch), \
                patch.object(smoke,"admission") as admission, patch.object(smoke,"save_json") as save:
            smoke.main()
        self.assertEqual(admission.call_args.args[0]["allocated_at"],launch["allocated_at"])
        self.assertFalse(save.call_args.args[1]["prospective_resource_check"])
