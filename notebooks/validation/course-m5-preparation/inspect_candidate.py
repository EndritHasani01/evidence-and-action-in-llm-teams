"""Verify pinned metadata/source and language shapes on meta, without weights."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def inspect(directory):
    import torch
    import transformers
    from transformers import AutoConfig, AutoTokenizer, Qwen3_5ForCausalLM
    from recovery.inference import QWEN_4B
    from tests.tokenizer_course_capacity import environment, metadata_support
    tokenizer = AutoTokenizer.from_pretrained(directory, local_files_only=True)
    support = metadata_support(directory, tokenizer)
    source = json.loads((ROOT / "notebooks/validation/m5-attention-memory/transformers-source.json").read_bytes())
    assert importlib.metadata.version("transformers") == source["version"] == "5.12.0"
    native_root = Path(transformers.__file__).parent.parent
    sources = {}
    for row in source["critical_installed_sources"]:
        raw = (native_root / row["path"]).read_bytes()
        assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"], row["path"]
        sources[row["path"]] = row["sha256"]
    config = AutoConfig.from_pretrained(directory, local_files_only=True).get_text_config()
    with torch.device("meta"):
        model = Qwen3_5ForCausalLM(config)
    assert all(p.device.type == "meta" for p in model.parameters())
    assert model.get_input_embeddings().weight is model.get_output_embeddings().weight
    linears = {id(module.weight) for module in model.modules() if isinstance(module, torch.nn.Linear)}
    embedding = id(model.get_input_embeddings().weight)
    parameters = {}
    for name, p in model.named_parameters():
        kind = "tied_embedding_head" if id(p) == embedding else "nf4_linear" if id(p) in linears else "other_fp16_fp32"
        parameters[name] = dict(shape=list(p.shape), elements=p.numel(), kind=kind)
    index_raw = (directory / "model.safetensors.index.json").read_bytes()
    with zipfile.ZipFile(ROOT / "dist/m5-kaggle-preflight.zip") as archive:
        assert index_raw == archive.read("metadata/4B/model.safetensors.index.json")
    index = json.loads(index_raw)
    language = {name.replace("model.language_model.", "model.", 1): shard
        for name, shard in index["weight_map"].items() if name.startswith("model.language_model.")}
    assert set(language) == set(parameters), (set(language) - set(parameters), set(parameters) - set(language))
    assert all(name.startswith(("model.language_model.", "model.visual.", "mtp.")) for name in index["weight_map"])
    # These are expected maintained language shapes; actual loading/NF4 remains unaccepted.
    return dict(model=QWEN_4B.model, revision=QWEN_4B.revision, metadata=environment(directory, tokenizer),
        native_support=support, config=json.loads((directory / "config.json").read_bytes()),
        verified_maintained_sources=sources, language_parameters=parameters,
        checkpoint_index=dict(bytes=len(index_raw), sha256=hashlib.sha256(index_raw).hexdigest(),
            total_checkpoint_bytes=index["metadata"]["total_size"], language_keys=len(language),
            shard_files=sorted(set(index["weight_map"].values())),
            retained_canonical_index_matches=True, tensor_payload_shapes_verified=False,
            official_source=f"https://huggingface.co/{QWEN_4B.model}/blob/{QWEN_4B.revision}/model.safetensors.index.json"),
        total_unique_language_parameters=sum(p["elements"] for p in parameters.values()),
        shape_only_meta_device=True, actual_language_weights_loaded=False, model_generations=0,
        cuda_execution=False, runtime_freeze=False, torch=str(torch.__version__))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = inspect(args.tokenizer)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(json.dumps(dict(parameters=result["total_unique_language_parameters"],
        unique_tensors=len(result["language_parameters"]), metadata_verified=True,
        selected_source_verified=True, pretrained_weights=False, cuda=False), indent=2))


if __name__ == "__main__":
    main()
