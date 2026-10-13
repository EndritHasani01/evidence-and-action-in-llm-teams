"""Small delivered CPU contract probe; no inference dependency or model load."""

from types import SimpleNamespace
import unittest

from recovery.inference import audit_language_load


class SingleDeviceLoadingTests(unittest.TestCase):
    def test_optional_dispatch_annotation_never_excuses_off_device_tensors(self):
        tensor = SimpleNamespace(device=SimpleNamespace(type="cuda", index=0), dtype="torch.float16",
                                 shape=(2, 2), is_floating_point=lambda: True)
        model = type("Qwen3_5ForCausalLM", (), {})()
        model.config = SimpleNamespace(model_type="qwen3_5_text", tie_word_embeddings=True)
        model.named_parameters = lambda: iter((("model.embed_tokens.weight", tensor),))
        model.named_buffers = lambda: iter(())
        model.get_input_embeddings = model.get_output_embeddings = lambda: SimpleNamespace(weight=tensor)
        info = dict(missing_keys=[], unexpected_keys=[], mismatched_keys=[], error_msgs=[])
        report = audit_language_load(model, info)
        self.assertIsNone(report["device_map"])
        self.assertEqual(report["actual_tensor_devices"], ["cuda:0"])
        model.hf_device_map = {"": 0}
        self.assertEqual(audit_language_load(model, info)["device_map"], {"": 0})
        del model.hf_device_map
        for device in ("cpu", "meta"):
            tensor.device = SimpleNamespace(type=device, index=None)
            with self.assertRaises(ValueError):
                audit_language_load(model, info)
        tensor.device = SimpleNamespace(type="cuda", index=1)
        with self.assertRaises(ValueError):
            audit_language_load(model, info)
