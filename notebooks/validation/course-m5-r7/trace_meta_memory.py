"""Actual pinned language shapes/lifetimes on meta; no weights or CUDA kernel."""

import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import weakref

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer",required=True,type=Path)
    parser.add_argument("--bound",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    assert not args.output.exists()
    import torch
    import transformers
    from torch.utils._python_dispatch import TorchDispatchMode
    from torch.utils._pytree import tree_flatten
    from transformers import AttentionInterface, AutoConfig, DynamicCache, Qwen3_5ForCausalLM
    from recovery.t4_attention import grouped_inputs
    assert not torch.cuda.is_initialized()
    prior = json.loads((ROOT/"notebooks/validation/m5-attention-memory/transformers-source.json").read_bytes())
    sources = {}
    for row in prior["critical_installed_sources"]:
        path = Path(transformers.__file__).parent.parent/row["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == row["sha256"]
        sources[row["path"]] = digest
    bound = json.loads(args.bound.read_bytes())["resident_tokens_upper"]
    config = AutoConfig.from_pretrained(args.tokenizer,local_files_only=True).get_text_config()
    with torch.device("meta"):
        model = Qwen3_5ForCausalLM(config).to(dtype=torch.float16).eval()
    assert all(p.device.type == "meta" for p in model.parameters())
    assert model.get_input_embeddings().weight is model.get_output_embeddings().weight
    excluded = {p.untyped_storage()._cdata for p in (*model.parameters(),*model.buffers())}

    class Trace(TorchDispatchMode):
        def __init__(self):
            self.references = {}
            self.peak = 0
            self.peak_operation = None
            self.stage = "inputs"
            self.stages = {}
            self.operations = 0
            self.attention_calls = 0

        def observe(self, value, operation):
            for tensor in tree_flatten(value)[0]:
                if isinstance(tensor,torch.Tensor) and tensor.device.type == "meta":
                    self.references[id(tensor)] = weakref.ref(tensor)
            live = {}
            expired = []
            for identity,reference in self.references.items():
                tensor = reference()
                if tensor is None:
                    expired.append(identity)
                else:
                    storage = tensor.untyped_storage()
                    if storage._cdata not in excluded:
                        live[storage._cdata] = storage.nbytes()
            for identity in expired:
                del self.references[identity]
            current = sum(live.values())
            self.stages[self.stage] = max(self.stages.get(self.stage,0),current)
            if current > self.peak:
                self.peak,self.peak_operation = current,operation

        def __torch_dispatch__(self, function, types, args=(), kwargs=None):
            self.observe((args,kwargs),"before "+str(function))
            output = function(*args,**(kwargs or {}))
            self.operations += 1
            self.observe(output,str(function))
            return output

    trace = Trace()

    def attention(module,query,key,value,attention_mask,**kwargs):
        q,k,v,bias = grouped_inputs(query,key,value,attention_mask)
        assert k.untyped_storage()._cdata == key.untyped_storage()._cdata
        assert v.untyped_storage()._cdata == value.untyped_storage()._cdata
        # Only the public wrapper/storage layout runs. The efficient kernel
        # is substituted by its source-declared FP16 output + FP32 accumulator.
        accumulator = torch.empty_like(q,dtype=torch.float32)
        output = torch.empty_like(q)
        trace.attention_calls += 1
        output = output.permute(2,0,1,3).reshape(1,query.shape[2],query.shape[1],query.shape[-1])
        return output.contiguous(),None

    AttentionInterface.register("r7_meta_shape_only",attention)
    model.config._attn_implementation = "r7_meta_shape_only"
    hooks = []
    for index,layer in enumerate(model.model.layers):
        def enter(module,args,index=index):
            trace.stage = f"{config.layer_types[index]}/{index}"
        hooks.append(layer.register_forward_pre_hook(enter))
    cases = []
    for name,length,past in (("first-prefill",256,0),("largest-cached-chunk",256,bound-256),
                             ("full-envelope-decode",1,bound-1)):
        cache = DynamicCache(config=config)
        with torch.inference_mode():
            if past:
                for index,layer in enumerate(cache.layers):
                    if config.layer_types[index] == "full_attention":
                        shape = (1,config.num_key_value_heads,past,config.head_dim)
                        layer.update(torch.empty(shape,device="meta",dtype=torch.float16),
                                     torch.empty(shape,device="meta",dtype=torch.float16))
                    else:
                        channels = 2*config.linear_num_key_heads*config.linear_key_head_dim + config.linear_num_value_heads*config.linear_value_head_dim
                        layer.update_conv_state(torch.empty((1,channels,config.linear_conv_kernel_dim),device="meta",dtype=torch.float16))
                        layer.update_recurrent_state(torch.empty((1,config.linear_num_value_heads,
                            config.linear_key_head_dim,config.linear_value_head_dim),device="meta",dtype=torch.float32))
            trace.references.clear()
            trace.peak,trace.peak_operation,trace.operations,trace.attention_calls = 0,None,0,0
            trace.stage = "inputs"
            trace.stages = {}
            with trace:
                trace.observe([(getattr(l,"keys",None),getattr(l,"values",None),
                    getattr(l,"conv_states",None),getattr(l,"recurrent_states",None)) for l in cache.layers],"initial cache")
                inputs = torch.empty((1,length),device="meta",dtype=torch.long)
                mask = torch.empty((1,1,length,past+length),device="meta",dtype=torch.bool)
                if not past:
                    # Native unpadded first chunk needs no materialized mask.
                    mask = None
                output = model(input_ids=inputs,attention_mask=mask,past_key_values=cache,
                    logits_to_keep=1,use_cache=True,return_dict=True)
            assert output.logits.shape == (1,1,config.vocab_size) and trace.attention_calls == 8
            cases.append(dict(name=name,query_tokens=length,cached_tokens_before=past,
                peak_observed_meta_storage_bytes=trace.peak,peak_operation=trace.peak_operation,
                stages=trace.stages,aten_operations=trace.operations,attention_calls=trace.attention_calls))
            output = cache = inputs = mask = None
            trace.references.clear()
            gc.collect()
    for hook in hooks:
        hook.remove()
    assert not torch.cuda.is_initialized()
    report = dict(torch=str(torch.__version__),torch_git_version=torch.version.git_version,
        transformers=transformers.__version__,sources=sources,resident_tokens_upper=bound,
        parameter_storage_excluded=True,real_pretrained_weights_loaded=False,cuda_initialized=False,
        cases=cases,scope="Actual meta shape/lifetime trace with substituted efficient output/accumulator; not a complete allocator/CUDA/load/quantized-model upper bound.",
        gpu_headroom_accepted=False)
    with args.output.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(report,output,indent=2)
        output.write("\n")
    print(json.dumps({"cases":[{k:r[k] for k in ("name","peak_observed_meta_storage_bytes","peak_operation")} for r in cases],
        "cuda_initialized":False,"actual_gpu_upper_bound":None},indent=2))


if __name__ == "__main__":
    main()
