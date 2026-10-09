"""Deployment guards for the bounded diagnostic; GPU outcomes are controlled."""

import ast
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

from scripts import m5_kaggle_preflight as operations
from scripts import m5_t4_compatibility as diagnostic
from scripts import build_t4_compatibility_notebook as builder
from scripts.build_t4_compatibility_notebook import notebook_document

IDENTITIES = ["GPU-00000000-0000-0000-0000-000000000001", "GPU-00000000-0000-0000-0000-000000000002"]
INVENTORY = "\n".join(f"{i}, {u}, Tesla T4, 00000000:00:0{i}.0, 580.65.06, 15360, 15000" for i, u in enumerate(IDENTITIES))


def configs():
    result = {}
    for model, hidden, intermediate, tied in [("9B", 4096, 12288, False), ("4B", 2560, 9216, True)]:
        raw = json.dumps({"tie_word_embeddings": tied, "text_config": {
            "num_attention_heads": 16, "num_key_value_heads": 4, "head_dim": 256,
            "num_hidden_layers": 32, "layer_types": ["linear_attention"]*24 + ["full_attention"]*8,
            "hidden_size": hidden, "intermediate_size": intermediate, "vocab_size": 248320}})
        result[model] = {"text": raw, "sha256": hashlib.sha256(raw.encode()).hexdigest()}
    return result


def controlled_probe(identity, package_root):
    attention = {}
    for name, phase, expanded, masked, forced in diagnostic.ATTENTION_CASES:
        attention[name] = {"status": "passed", "finite": True, "reference_matches": True,
            "query_shape": [1, 16, 32 if phase == "prefill" else 1, 256],
            "key_shape": [1, 16 if expanded else 4, 32, 256], "value_shape": [1, 16 if expanded else 4, 32, 256],
            "mask_shape": [32, 32] if masked else None, "dtype": "torch.float16", "enable_gqa": not expanded,
            "is_causal": phase == "prefill" and not masked, "forced_efficient": forced,
            "operator_backend": "efficient" if expanded else "math"}
    return {"scope": "Controlled test receipt, not actual GPU evidence", "status": "passed", "assigned_uuid": identity,
        "observed_uuid": identity, "device_count": 1, "capability": [7, 5], "torch_version": "2.11.0+cu128",
        "torch_cuda_build": "12.8", "bitsandbytes_version": "0.49.2", "model_generations": 0,
        "bitsandbytes_root": str(package_root / "bitsandbytes/__init__.py"),
        "bitsandbytes_native_library": str(package_root / "bitsandbytes/libbitsandbytes_cuda128.so"),
        "attention": attention, "nf4": {"status": "passed", "quant_type": "nf4", "double_quantization": True,
            "weight_shape": [128, 256], "weight_dtype": "torch.float16", "blocksize": 64,
            "operations": [{"batch": b, "output_shape": [b, 128], "output_dtype": "torch.float16",
                            "finite": True, "reference_matches": True} for b in (8, 1)]}}


class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="m5-t4-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.wheel = self.root / "controlled.whl"
        with zipfile.ZipFile(self.wheel, "x") as archive:
            archive.writestr("bitsandbytes/__init__.py", "# controlled bytes only\n")
            archive.writestr("bitsandbytes-0.49.2.dist-info/METADATA", "Name: bitsandbytes\nVersion: 0.49.2\n")
        with zipfile.ZipFile(self.wheel) as archive:
            meta = {"name": "bitsandbytes", "version": "0.49.2", "filename": self.wheel.name,
                    "url": "https://files.pythonhosted.org/controlled.whl", "bytes": self.wheel.stat().st_size,
                    "sha256": operations.sha256_file(self.wheel), "expanded_bytes": sum(m.file_size for m in archive.infolist()), "members": 2}
        self.expected = {"configs": configs(), "bitsandbytes_wheel": meta,
                         "candidate_versions": {"torch": "2.11.0+cu128", "bitsandbytes": "0.49.2"}}
        self.calls = []
        self.failure = None

    def command(self, output, name, args, **kwargs):
        self.calls.append(name)
        logs = output / "logs"
        logs.mkdir(exist_ok=True)
        stdout, stderr = logs / (name+".stdout.txt"), logs / (name+".stderr.txt")
        stdout.write_text("", encoding="utf-8")
        stderr.write_text("", encoding="utf-8")
        record = {"name": name, "args": list(map(str, args)), "stdout": stdout.relative_to(output).as_posix(),
                  "stderr": stderr.relative_to(output).as_posix(), "status": "passed", "exit_code": 0,
                  "leader_exited": True, "tree_confirmation": "exited"}
        if self.failure == name:
            record.update(status="failed", tree_confirmation="unconfirmed")
            operations.save_json(logs / (name+".json"), record)
            raise RuntimeError("controlled cleanup failure")
        if name == "gpu-inventory":
            stdout.write_text(INVENTORY, encoding="utf-8")
        elif name == "download-bitsandbytes-wheel":
            target = kwargs["cwd"] / self.expected["bitsandbytes_wheel"]["filename"]
            target.write_bytes(self.wheel.read_bytes())
            stdout.write_text(json.dumps(dict(self.expected["bitsandbytes_wheel"], verified=True)), encoding="utf-8")
        elif name.startswith("device_"):
            self.assertEqual(kwargs["env"]["CUDA_VISIBLE_DEVICES"], IDENTITIES[int(name[-1])])
            self.assertNotIn("BNB_CUDA_VERSION", kwargs["env"])
            self.assertIn("-I", args)
            self.assertIn("-B", args)
            package_root = Path(args[args.index("--package-root")+1])
            destination = Path(args[args.index("--output")+1])
            operations.save_json(destination, controlled_probe(kwargs["env"]["CUDA_VISIBLE_DEVICES"], package_root))
            stdout.write_text("[ERROR] controlled noisy import diagnostic\n", encoding="utf-8")
        else:
            raise AssertionError("Unexpected command: " + name)
        operations.save_json(logs / (name+".json"), record)
        return record

    def run_case(self, *, started=None, version="2.11.0+cu128", controlled=True):
        ops = dict(vars(operations), command=self.command if controlled else operations.command)
        with patch.object(diagnostic.platform, "system", return_value="Linux"), \
             patch.object(diagnostic.platform, "machine", return_value="x86_64"), \
             patch.object(diagnostic.sys, "version_info", (3, 13, 0)), \
             patch.object(diagnostic.metadata, "version", side_effect=lambda n: version if n == "torch" else "0.49.2"):
            return diagnostic.run_compatibility(self.root / "output", self.root / "scratch", self.expected, ops,
                                                Path(diagnostic.__file__).read_text(encoding="utf-8"), started)

    def test_conditional_bounds_preserve_context_and_tie_assumptions(self):
        result = diagnostic.envelope_assessment(configs())
        self.assertIsNone(result["full_envelope_memory_acceptance"])
        a, b = result["models"]["9B"], result["models"]["4B"]
        self.assertEqual(a["kv_bytes_per_token"], 32768)
        self.assertEqual(a["fp16_kv_bytes_at_cap"], 8*2**30)
        self.assertEqual(a["conditional_subtotal_bytes_at_cap"], 15074328576)
        self.assertEqual(b["conditional_subtotal_bytes_at_cap"], 10993795072)
        self.assertEqual(a["repeated_kv_one_layer_additional_bytes_at_cap"], 4*2**30)
        self.assertEqual(a["dense_score_fp32_bytes_at_cap"], 4096*2**30)

    def test_isolated_children_leave_verified_imports_unchanged(self):
        package_root = self.root / "extracted"
        snapshot = diagnostic.unpack_wheel(self.wheel, package_root, self.expected["bitsandbytes_wheel"],
                                           vars(operations), self.root)
        program = "import sys;sys.path.insert(0," + repr(str(package_root)) + ");import bitsandbytes;print(bitsandbytes.__file__)"
        for index in range(2):
            record = operations.command(self.root, "isolated-import-"+str(index),
                [diagnostic.sys.executable, "-I", "-B", "-c", program], deadline=time.monotonic()+150,
                timeout=10, cwd=self.root, env=operations.candidate_environment(self.root))
            self.assertIs(record["leader_exited"], True)
            self.assertEqual(record["status"], "passed")
            self.assertEqual({p.relative_to(package_root).as_posix() for p in package_root.rglob("*") if p.is_file()}, set(snapshot["files"]))
        self.assertEqual(operations.sha256_file(package_root / "bitsandbytes/__init__.py"),
                         snapshot["files"]["bitsandbytes/__init__.py"]["sha256"])

    def test_builder_refuses_overwrite_changed_archive_and_checkpoint(self):
        destination = self.root / "delivered.ipynb"
        destination.write_text("retain previous bytes", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            builder.build(self.root / "absent.zip", destination, "HEAD")
        self.assertEqual(destination.read_text(encoding="utf-8"), "retain previous bytes")
        destination = self.root / "new.ipynb"
        with self.assertRaisesRegex(ValueError, "canonical_source_archive_changed"):
            builder.build(self.wheel, destination, "HEAD")
        with patch.object(builder.subprocess, "check_output", return_value=b"changed source\n"):
            with self.assertRaisesRegex(ValueError, "build_checkpoint_differs_from_source"):
                builder.build(builder.ROOT / "dist/m5-kaggle-preflight.zip", destination, "HEAD")
        self.assertFalse(destination.exists())

    def test_changed_config_or_geometry_rejected(self):
        c = configs()
        c["9B"]["text"] += " "
        with self.assertRaisesRegex(ValueError, "hash"):
            diagnostic.envelope_assessment(c)
        c = configs()
        raw = json.loads(c["9B"]["text"])
        raw["text_config"]["num_key_value_heads"] = 8
        c["9B"]["text"] = json.dumps(raw)
        c["9B"]["sha256"] = hashlib.sha256(c["9B"]["text"].encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, "geometry"):
            diagnostic.envelope_assessment(c)

    def test_duplicate_uuid_wrong_device_and_low_space_refused(self):
        self.assertEqual(len(diagnostic.parse_inventory(INVENTORY)), 2)
        for raw in [INVENTORY.replace(IDENTITIES[1], IDENTITIES[0]), INVENTORY.replace("Tesla T4", "A100"),
                    INVENTORY.replace("15000", "100"), "unavailable"]:
            with self.subTest(raw=raw), self.assertRaises((ValueError, IndexError)):
                diagnostic.parse_inventory(raw)

    def test_wheel_bytes_and_unsafe_member_refused_before_extraction(self):
        output = self.root / "out"
        output.mkdir()
        with self.assertRaisesRegex(ValueError, "bytes"):
            diagnostic.unpack_wheel(self.wheel, self.root / "bad-hash", dict(self.expected["bitsandbytes_wheel"], sha256="0"*64), vars(operations), output)
        for name in ["../escape", "bitsandbytes/../../escape", "C:/escape", "other/package.py"]:
            wheel = self.root / (hashlib.sha256(name.encode()).hexdigest()+".whl")
            with zipfile.ZipFile(wheel, "x") as archive:
                archive.writestr(name, "bad")
            meta = dict(self.expected["bitsandbytes_wheel"], bytes=wheel.stat().st_size,
                        sha256=operations.sha256_file(wheel), members=1, expanded_bytes=3)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "unsafe"):
                diagnostic.unpack_wheel(wheel, self.root / "bad-path", meta, vars(operations), output)
            self.assertFalse((self.root / "bad-path").exists())

    def test_controlled_complete_export_no_install_or_model_acceptance(self):
        result = self.run_case()
        self.assertEqual(self.calls, ["gpu-inventory", "download-bitsandbytes-wheel", "device_0", "device_1"])
        self.assertTrue(result["summary"]["library_checks_completed"])
        self.assertIsNone(result["summary"]["full_candidate_gpu_acceptance"])
        self.assertIsNone(result["summary"]["full_envelope_memory_acceptance"])
        self.assertEqual(result["summary"]["model_generations"], 0)
        self.assertEqual(result["summary"]["conditional_allocation_upper_bound_seconds"], 1080)
        with zipfile.ZipFile(result["zip_path"]) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("device_1.json", archive.namelist())
            self.assertIn("filesystem-backup.sqlite", archive.namelist())
            self.assertFalse(any(n.endswith((".whl", ".so", ".py")) for n in archive.namelist()))

    def test_wrong_torch_exports_before_download(self):
        result = self.run_case(version="2.11.0+cpu")
        self.assertFalse(self.calls)
        self.assertIn("torch_differs", result["summary"]["root_blocker"])
        self.assertTrue(Path(result["zip_path"]).is_file())

    def test_uncertain_cleanup_prevents_second_device(self):
        self.failure = "device_0"
        result = self.run_case()
        self.assertNotIn("device_1", self.calls)
        self.assertTrue(result["report"]["process_cleanup_unconfirmed"])
        self.assertEqual(result["report"]["stages"]["device_1"]["status"], "blocked")
        self.assertTrue(Path(result["zip_path"]).is_file())

    def test_real_command_admission_refuses_expired_deadline(self):
        output = self.root / "deadline"
        output.mkdir()
        with self.assertRaisesRegex(TimeoutError, "deadline_before_command"):
            operations.command(output, "never-start", ["not-a-real-executable"], deadline=time.monotonic(),
                               timeout=60, cwd=self.root, env={})
        self.assertFalse((output / "logs").exists())

    def test_expired_workflow_exports_without_starting_gpu_commands(self):
        result = self.run_case(started=time.monotonic()-360, controlled=False)
        self.assertIn("deadline_before_command", result["summary"]["root_blocker"])
        self.assertFalse((Path(result["run_directory"])/"logs").exists())
        self.assertTrue(Path(result["zip_path"]).is_file())

    def test_unknown_or_ambiguous_dispatch_stays_unknown(self):
        self.assertIsNone(diagnostic.backend_name(["unknown_future_operator"]))
        self.assertIsNone(diagnostic.backend_name(["aten::_scaled_dot_product_attention_math", "aten::_scaled_dot_product_efficient_attention"]))
        self.assertEqual(diagnostic.backend_name(["aten::_scaled_dot_product_attention_math"]), "math")

    def test_bad_uuid_nf4_mask_or_scope_receipts_rejected(self):
        root = self.root / "package"
        original = controlled_probe(IDENTITIES[0], root)
        mutations = [lambda x: x.update(observed_uuid=IDENTITIES[1]),
                     lambda x: x.update(model_generations=1),
                     lambda x: x.update(full_candidate_gpu_acceptance=True),
                     lambda x: x.update(bitsandbytes_root=str(self.root / "base/__init__.py")),
                     lambda x: x["nf4"].update(double_quantization=False),
                     lambda x: x["attention"]["decode-gqa"].update(is_causal=True),
                     lambda x: x["attention"]["prefill-mask-expanded"].update(mask_shape=None),
                     lambda x: x["attention"]["prefill-gqa"].update(finite=False)]
        diagnostic.validate_probe(original, IDENTITIES[0], root)
        for mutate in mutations:
            value = copy.deepcopy(original)
            mutate(value)
            with self.assertRaises(ValueError):
                diagnostic.validate_probe(value, IDENTITIES[0], root)

    def test_only_expected_forced_backend_failure_is_an_observation(self):
        root = self.root / "package"
        result = controlled_probe(IDENTITIES[0], root)
        row = result["attention"]["decode-expanded-efficient"]
        row.update(status="unsupported", reason="No available kernel. Aborting execution.")
        diagnostic.validate_probe(result, IDENTITIES[0], root)
        row["reason"] = "CUDA illegal memory access"
        with self.assertRaises(ValueError):
            diagnostic.validate_probe(result, IDENTITIES[0], root)

    def test_notebook_sources_compile_and_repeat_run_cell_reuses_result(self):
        program = Path(diagnostic.__file__).read_text(encoding="utf-8")
        ops = Path(operations.__file__).read_text(encoding="utf-8")
        expected = dict(self.expected, program_sha256=hashlib.sha256(program.encode()).hexdigest(),
                        operations_sha256=hashlib.sha256(ops.encode()).hexdigest())
        notebook = notebook_document(program, ops, expected)
        for c in notebook["cells"]:
            if c["cell_type"] == "code":
                ast.parse(c["source"])
                self.assertIsNone(c["execution_count"])
                self.assertEqual(c["outputs"], [])
        env = {"COMPATIBILITY_RESULT": {"retained": True}}
        exec(notebook["cells"][3]["source"], env)
        self.assertEqual(env["COMPATIBILITY_RESULT"], {"retained": True})


if __name__ == "__main__":
    unittest.main()
