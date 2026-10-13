"""Verify header inventory and maintained CPU loading behavior, without weights/CUDA."""

import argparse
import base64
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
from io import BytesIO
import json
from math import prod
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import weakref
import zipfile

import torch
import transformers
from transformers import Qwen3_5Config, Qwen3_5ForCausalLM
from transformers import core_model_loading as loading
from transformers.modeling_utils import LoadStateDictConfig

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[2]
sys.path.insert(0, str(FOLDER))
from capture_headers import header, read_range


def read(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if str(path).endswith(".gz") else data)


def validate_headers(archive, inspection, index):
    if (any(archive[k] != inspection[k] for k in ("model", "revision"))
            or archive["checkpoint_index_sha256"] != inspection["checkpoint_index"]["sha256"]
            or archive["tensor_payload_bytes_read"] != 0
            or archive["model_weights_staged"] is not False or archive["gpu_execution"] is not False):
        raise ValueError("metadata-only pinned evidence required")
    tensors = {}
    payload_bytes = 0
    for shard, row in archive["headers"].items():
        prefix = base64.b64decode(row["prefix_base64"], validate=True)
        length = struct.unpack("<Q", prefix[:8])[0]
        if (len(prefix) != 8+length or length != row["header_bytes"]
                or hashlib.sha256(prefix).hexdigest() != row["prefix_sha256"]
                or row["url"] != f"https://huggingface.co/{archive['model']}/resolve/{archive['revision']}/{shard}"
                or row["ranges"] != [dict(start=0,end=7,file_bytes=row["file_bytes"],status=206,bytes_read=8),
                    dict(start=8,end=7+length,file_bytes=row["file_bytes"],status=206,bytes_read=length)]):
            raise ValueError("exact metadata range identity differs")
        entries = json.loads(prefix[8:])
        end = 0
        for name, tensor in sorted(((k,v) for k,v in entries.items() if k != "__metadata__"),
                                  key=lambda item:item[1]["data_offsets"][0]):
            size = prod(tensor["shape"]) * {"BF16":2, "F32":4}[tensor["dtype"]]
            if (name in tensors or index["weight_map"].get(name) != shard
                    or tensor["data_offsets"] != [end,end+size]):
                raise ValueError("checkpoint inventory/contiguous payload offsets differ")
            end += size
            tensors[name] = tensor
        if len(prefix)+end != row["file_bytes"]:
            raise ValueError("checkpoint total bytes differ")
        payload_bytes += end
    if (set(tensors) != set(index["weight_map"]) or payload_bytes != index["metadata"]["total_size"]
            or sum(8+r["header_bytes"] for r in archive["headers"].values()) != archive["downloaded_metadata_bytes"]):
        raise ValueError("complete checkpoint metadata required")
    language = {k.replace("model.language_model.","model.",1):v for k,v in tensors.items()
                if k.startswith("model.language_model.")}
    if (set(language) != set(inspection["language_parameters"])
            or any(v["shape"] != inspection["language_parameters"][k]["shape"] for k,v in language.items())
            or any(not k.startswith(("model.language_model.","model.visual.","mtp.")) for k in tensors)):
        raise ValueError("maintained language shape inventory differs")
    return language, tensors


class Checks(unittest.TestCase):
    def test_header_ranges_reject_unbounded_reads(self):
        class Response(BytesIO):
            status = 206
            headers = {"Content-Range":"bytes 0-7/100"}
            reads = 0
            def read(self, count=-1):
                self.reads += 1
                self.asserted_count = count
                return super().read(count)
        for status, content_range in ((200,""),(206,"bytes 0-99/100"),(206,"bytes 1-8/100")):
            response = Response(b"unread payload")
            response.status = status
            response.headers = {"Content-Range":content_range}
            with self.assertRaises(ValueError):
                read_range("https://example.invalid",0,7,lambda *a,**k:response)
            self.assertEqual(response.reads,0)
        response = Response(struct.pack("<Q",1024*1024))
        with self.assertRaises(ValueError):
            header("https://example.invalid",lambda *a,**k:response)
        self.assertEqual((response.reads,response.asserted_count),(1,8))

    def test_complete_header_inventory_and_rejections(self):
        language, tensors = validate_headers(HEADERS, INSPECTION, INDEX)
        self.assertEqual((len(language),len(tensors)),(426,738))
        for field, value in (("revision","wrong"),("tensor_payload_bytes_read",1),("model_weights_staged",True)):
            altered = deepcopy(HEADERS)
            altered[field] = value
            with self.assertRaises(ValueError):
                validate_headers(altered,INSPECTION,INDEX)
        altered = deepcopy(HEADERS)
        altered["headers"].pop(next(iter(altered["headers"])))
        with self.assertRaises(ValueError):
            validate_headers(altered,INSPECTION,INDEX)
        altered = deepcopy(HEADERS)
        next(iter(altered["headers"].values()))["prefix_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            validate_headers(altered,INSPECTION,INDEX)
        altered = deepcopy(INSPECTION)
        altered["language_parameters"]["model.embed_tokens.weight"]["shape"][0] += 1
        with self.assertRaises(ValueError):
            validate_headers(HEADERS,altered,INDEX)

    def test_actual_loader_materializes_sequentially(self):
        events, inputs = [], []
        class Slice:
            def __init__(self, name):
                self.name = name
            def __getitem__(self, key):
                assert not any(ref() is not None for ref in inputs)
                events.append(("materialize",self.name))
                value = torch.empty((8,8),dtype=torch.float16)
                inputs.append(weakref.ref(value))
                return value
        class Quantize(loading.ConversionOps):
            def convert(self, input_dict, **kwargs):
                assert len(input_dict)==1 and sum(ref() is not None for ref in inputs)==1
                name = next(iter(input_dict))
                events.append(("quantize",name))
                return {name:torch.zeros((32,1),dtype=torch.uint8)}
        quantizer = SimpleNamespace(pre_quantized=False,
            param_needs_quantization=lambda *a:True, get_quantize_ops=lambda:Quantize())
        model = torch.nn.Module()
        model.base_model_prefix = "model"
        model.config = SimpleNamespace()
        for name in ("first","second","third"):
            model.add_module(name,torch.nn.Linear(8,8,bias=False,device="meta",dtype=torch.float16))
        state = {name+".weight":Slice(name+".weight") for name in ("third","second","first")}
        state["visual.unused"] = Slice("must not materialize")
        config = LoadStateDictConfig(dtype=torch.float16, device_map={"":"cpu"}, hf_quantizer=quantizer)
        with patch.object(loading,"ThreadPoolExecutor",side_effect=AssertionError("async loading forbidden")), \
                patch.dict("os.environ",{"HF_DEACTIVATE_ASYNC_LOAD":"0"}):
            info, _ = loading.convert_and_load_state_dict_in_model(model,state,config,tp_plan={})
        self.assertFalse(info.missing_keys or info.mismatched_keys or info.conversion_errors or info.error_msgs)
        self.assertEqual(info.unexpected_keys,{"visual.unused"})
        self.assertEqual(events,[(kind,name+".weight") for name in ("first","second","third")
                                for kind in ("materialize","quantize")])
        self.assertTrue(all(ref() is None for ref in inputs))
        RESULT["maintained_loader_events"] = events

    def test_native_tied_head_is_not_materialized_twice(self):
        config = Qwen3_5Config(**INSPECTION["config"]).get_text_config()
        with torch.device("meta"):
            model = Qwen3_5ForCausalLM(config)
            model.lm_head.weight = torch.nn.Parameter(torch.empty_like(model.lm_head.weight))
        self.assertIsNot(model.lm_head.weight,model.model.embed_tokens.weight)
        created = []
        original = torch.empty_like
        def tracked(value, **kwargs):
            created.append(value.numel())
            return original(value,device="meta")
        with patch.object(torch,"empty_like",side_effect=tracked):
            model._move_missing_keys_from_meta_to_device({"lm_head.weight"},{"":"cpu"},None,None)
        self.assertNotIn(635699200,created)
        model.tie_weights(missing_keys={"lm_head.weight"},recompute_mapping=False)
        self.assertIs(model.lm_head.weight,model.model.embed_tokens.weight)
        buffers = list(model.named_buffers())
        RESULT["nonpersistent_buffer_fp32_allowance_bytes"] = sum(p.numel()*4 for _,p in buffers)
        RESULT["tied_head_extra_materialization"] = False

    def test_pinned_sources_and_storage_arithmetic(self):
        self.assertEqual(transformers.__version__,"5.12.0")
        native_root = Path(transformers.__file__).parent
        for path,digest in INSPECTION["verified_maintained_sources"].items():
            self.assertEqual(hashlib.sha256((native_root.parent/path).read_bytes()).hexdigest(),digest)
        sources = read(FOLDER/"loading-sources.json.gz")["sources"]
        for row in sources.values():
            raw = row["source"].encode("utf-8")
            self.assertEqual((len(raw),hashlib.sha256(raw).hexdigest()),(row["bytes"],row["sha256"]))
        for name,relative in (("transformers-core-loading.py","core_model_loading.py"),
                ("transformers-bnb-integration.py","integrations/bitsandbytes.py"),
                ("transformers-bnb-quantizer.py","quantizers/quantizer_bnb_4bit.py")):
            row = sources[name]
            raw = (native_root/relative).read_bytes()
            self.assertEqual(raw,row["source"].encode("utf-8"))
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row["sha256"])
        RESULT["verified_additional_sources"] = {k:v["sha256"] for k,v in sources.items()}
        parameters = INSPECTION["language_parameters"]
        matrices = [p["elements"] for p in parameters.values() if p["kind"]=="nf4_linear"]
        components = dict(fp16_tied_embedding_head_bytes=635699200*2,
            packed_nf4_bytes=sum((n+1)//2 for n in matrices),
            double_quant_state_bytes=sum((n+63)//64+4*((n+16383)//16384)+16*4+256*4+4 for n in matrices),
            ordinary_parameter_fp32_allowance_bytes=sum(p["elements"]*4 for p in parameters.values() if p["kind"]=="other_fp16_fp32"),
            shared_dynamic_code_map_bytes=256*4)
        self.assertEqual((len(matrices),max(matrices)),(248,23592960))
        self.assertEqual(sum(components.values()),3116700064)
        RESULT["source_derived_parameter_components_bytes"] = components
        RESULT["source_derived_parameter_storage_upper_bytes"] = sum(components.values())
        # Two matrix copies, absmax plus its centered input, and NF4 map abs/max temporaries.
        RESULT["conditional_active_conversion_tensor_allowance_bytes"] = 4*max(matrices)+8*((max(matrices)+63)//64)+16*4+4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("retain old evidence; use a fresh output")
    global HEADERS, INSPECTION, INDEX, RESULT
    HEADERS = read(FOLDER/"checkpoint-headers.json.gz")
    INSPECTION = read(ROOT/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json")
    with zipfile.ZipFile(ROOT/"dist/m5-kaggle-preflight.zip") as archive:
        index_raw = archive.read("metadata/4B/model.safetensors.index.json")
    assert hashlib.sha256(index_raw).hexdigest()==HEADERS["checkpoint_index_sha256"]
    INDEX = json.loads(index_raw)
    RESULT = {}
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
    if not result.wasSuccessful():
        return 1
    language, tensors = validate_headers(HEADERS,INSPECTION,INDEX)
    RESULT.update(model=HEADERS["model"],revision=HEADERS["revision"],torch=str(torch.__version__),
        transformers=transformers.__version__,checks=result.testsRun,skips=len(result.skipped),
        checkpoint_tensors=len(tensors),language_tensors=len(language),
        language_checkpoint_dtypes=dict(Counter(t["dtype"] for t in language.values())),
        downloaded_metadata_bytes=HEADERS["downloaded_metadata_bytes"],tensor_payload_bytes_read=0,
        tensor_storage_loading_allowance_bytes=RESULT["source_derived_parameter_storage_upper_bytes"]+
            RESULT["nonpersistent_buffer_fp32_allowance_bytes"]+RESULT["conditional_active_conversion_tensor_allowance_bytes"],
        allocation_scope="Source-derived explicit parameter/conversion Tensor storage, conditional on maintained NF4 CUDA layout. Excludes allocator reservations, native reduction/library/workspace/context allocations and actual weight loading acceptance.",
        complete_live_memory_upper_bound_bytes=None, actual_gpu_peak_bytes=None,actual_headroom_acceptance=None,
        preparation_admitted=False,weight_staging_permitted=False,terminal_model_feasibility_failure=False,
        cuda_initialized=torch.cuda.is_initialized(),model_weights_staged=False,model_weights_loaded=False,gpu_execution=False)
    assert RESULT["cuda_initialized"] is False
    with args.output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(RESULT,stream,indent=2)
        stream.write("\n")
    print(json.dumps(RESULT,indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
