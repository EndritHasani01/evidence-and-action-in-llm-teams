"""Direct serial Qwen text inference; importing this module never loads weights.

These are candidates for M5 smoke validation, not an accepted GPU lock. The
existing ProcessProvider owns attempts/termination and SQLite owns raw evidence.
Only explicit permitted requests cross the generation boundary.
"""

from dataclasses import asdict, dataclass
import os
import sys

from .prompts import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS, render_request, tokenize_request


@dataclass(frozen=True)
class Candidate:
    model: str = "Qwen/Qwen3.5-9B"
    revision: str = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"

    def __post_init__(self):
        if (self.model, self.revision) not in (
            ("Qwen/Qwen3.5-9B", "c202236235762e1c871ad0ccb60c8ee5ba337b9a"),
            ("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"),
        ):
            raise ValueError("use the reviewed 9B candidate or prescribed 4B fallback revision")


QWEN_9B = Candidate()
QWEN_4B = Candidate("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
EOS_IDS = (248044, 248046)
PAD_ID = 248044
# Only a final im_end is verified message transport. endoftext is an EOS stop,
# but its generated text remains visible to the strict parser.
TRANSPORT_ID = 248046


def candidate_settings(tokenizer, candidate=QWEN_9B):
    """Save actual template inputs and all deliberate sampling/termination choices."""
    if (tokenizer.eos_token_id != TRANSPORT_ID or tokenizer.pad_token_id != PAD_ID
            or tokenizer.convert_ids_to_tokens(TRANSPORT_ID) != "<|im_end|>"
            or tokenizer.convert_ids_to_tokens(PAD_ID) != "<|endoftext|>"
            or type(tokenizer.chat_template) is not str or not tokenizer.chat_template):
        raise ValueError("candidate tokenizer/template/framing differs; reopen affected CPU checks")
    return {
        "model": candidate.model, "revision": candidate.revision,
        "chat_template": tokenizer.chat_template, "enable_thinking": False,
        "max_context_tokens": MAX_CONTEXT_TOKENS,
        "quantization": {"load_in_4bit": True, "bnb_4bit_quant_type": "nf4",
                         "bnb_4bit_use_double_quant": True, "bnb_4bit_compute_dtype": "float16"},
        "dtype": "float16", "attention": "sdpa", "batch_size": 1,
        "generation": {
            "do_sample": True, "temperature": 0.7, "top_p": 0.8, "top_k": 20,
            "min_p": 0.0, "repetition_penalty": 1.0, "num_beams": 1,
            "max_new_tokens": MAX_OUTPUT_TOKENS, "eos_token_id": list(EOS_IDS),
            "pad_token_id": PAD_ID, "use_cache": True,
            "return_dict_in_generate": True, "output_scores": False,
            "remove_invalid_values": False,
        },
        "terminal_transport_id": TRANSPORT_ID,
    }


def decode_suffix(tokenizer, token_ids):
    """Keep exact generated IDs/raw suffix; remove one verified terminal framing ID."""
    from .protocol import GeneratedReply

    if (type(token_ids) is not tuple or not token_ids or len(token_ids) > MAX_OUTPUT_TOKENS
            or any(type(i) is not int or i < 0 for i in token_ids)):
        raise ValueError("expected one nonempty generated suffix within the output cap")
    raw = tokenizer.decode(list(token_ids), skip_special_tokens=False,
                           clean_up_tokenization_spaces=False)
    terminal = token_ids[-1] == TRANSPORT_ID
    body_ids = token_ids[:-1] if terminal else token_ids
    text = tokenizer.decode(list(body_ids), skip_special_tokens=False,
                            clean_up_tokenization_spaces=False) if terminal else raw
    if terminal and (tokenizer.convert_ids_to_tokens(TRANSPORT_ID) != "<|im_end|>"
                     or raw != text + "<|im_end|>"):
        raise ValueError("terminal framing has not been verified; never normalize the suffix")
    termination = "eos" if token_ids[-1] in EOS_IDS else "length"
    if termination == "length" and len(token_ids) != MAX_OUTPUT_TOKENS:
        raise ValueError("unexplained early stop; no extra stopping criterion is permitted")
    # A cap stop does not establish content loss. Whole JSON validation decides.
    return GeneratedReply(text, token_ids, termination), raw


def audit_language_load(model, loading_info):
    """Reject unaccounted language initialization, mismatches and off-device tensors."""
    if type(model).__name__ != "Qwen3_5ForCausalLM" or model.config.model_type != "qwen3_5_text":
        raise ValueError("the maintained text-only Qwen class is required")
    required = {"missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs"}
    if not required <= loading_info.keys():
        raise ValueError("complete maintained loading diagnostics are required")
    if (any(loading_info[k] for k in ("missing_keys", "mismatched_keys", "error_msgs"))
            or loading_info.get("conversion_errors")):
        raise ValueError("unexplained missing/newly initialized/mismatched language weights: " + repr(loading_info))
    if any(not (key.startswith("model.visual.") or key.startswith("mtp."))
           for key in loading_info["unexpected_keys"]):
        raise ValueError("unexpected language weights are not unused vision/MTP weights")
    parameters = dict(model.named_parameters())
    embedding = model.get_input_embeddings().weight
    head = model.get_output_embeddings().weight
    tied = bool(model.config.tie_word_embeddings)
    if (tied and head is not embedding or not tied and head is embedding
            or "model.embed_tokens.weight" not in parameters
            or not tied and "lm_head.weight" not in parameters):
        raise ValueError("verify the actual language embedding/output head, including ties")
    tensors = tuple(parameters.items()) + tuple(model.named_buffers())
    if (not tensors or any(t.device.type != "cuda" or t.device.index != 0 for _, t in tensors)
            or not model.hf_device_map
            or any(str(device) not in ("0", "cuda:0") for device in model.hf_device_map.values())):
        raise ValueError("one complete local CUDA replica; no CPU/disk offload or device splitting")
    # Ordinary floating tensors are FP16 or supported sensitive FP32; packed
    # bitsandbytes tensors can be uint8. Never blanket-cast the loaded model.
    if any(t.is_floating_point() and str(t.dtype) not in ("torch.float16", "torch.float32")
           for _, t in tensors):
        raise ValueError("unexpected language precision; FP16 with supported FP32 paths is required")
    return {"loading_info": {key: sorted(value) if isinstance(value, set) else value
                             for key, value in loading_info.items()}, "class": type(model).__name__,
            "parameters": {name: {"shape": list(t.shape), "dtype": str(t.dtype),
                                    "device": str(t.device)} for name, t in parameters.items()},
            "tied_output_head": tied, "device_map": dict(model.hf_device_map)}


@dataclass(frozen=True)
class TokenizerFactory:
    candidate: Candidate = QWEN_9B
    local_directory: str | None = None

    def __call__(self):
        from transformers import AutoTokenizer

        if self.local_directory is None:
            tokenizer = AutoTokenizer.from_pretrained(self.candidate.model,
                revision=self.candidate.revision, trust_remote_code=False)
        else:
            tokenizer = AutoTokenizer.from_pretrained(self.local_directory,
                local_files_only=True, trust_remote_code=False)
        candidate_settings(tokenizer, self.candidate)
        return tokenizer


@dataclass(frozen=True)
class ModelFactory:
    """Spawn-picklable loader. Calling it requires separately authorized GPU work."""
    candidate: Candidate = QWEN_9B
    cuda_visible_devices: str = "0"

    def __call__(self):
        if (type(self.cuda_visible_devices) is not str or not self.cuda_visible_devices
                or "," in self.cuda_visible_devices):
            raise ValueError("one explicit physical GPU must be visible")
        torch = sys.modules.get("torch")
        if torch is not None and torch.cuda.is_initialized():
            raise ValueError("device visibility must precede CUDA initialization")
        os.environ["CUDA_VISIBLE_DEVICES"] = self.cuda_visible_devices
        import torch

        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise ValueError("one available CUDA device is required; never offload to CPU")
        if "T4" not in torch.cuda.get_device_name(0):
            raise ValueError("the candidate execution path requires an actual T4")
        from transformers import AutoModelForCausalLM, BitsAndBytesConfig
        tokenizer = TokenizerFactory(self.candidate)()
        quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
        model, info = AutoModelForCausalLM.from_pretrained(self.candidate.model,
            revision=self.candidate.revision, trust_remote_code=False,
            quantization_config=quantization, dtype=torch.float16,
            device_map={"": 0}, attn_implementation="sdpa", output_loading_info=True)
        model.eval()
        if not getattr(model, "is_loaded_in_4bit", False):
            raise ValueError("the language replica must actually be loaded in 4-bit NF4")
        actual_quantization = model.hf_quantizer.quantization_config
        if (actual_quantization.bnb_4bit_quant_type != "nf4"
                or actual_quantization.bnb_4bit_use_double_quant is not True
                or actual_quantization.bnb_4bit_compute_dtype != torch.float16):
            raise ValueError("actual quantization must match explicit NF4/double/FP16 settings")
        report = audit_language_load(model, info)
        import importlib.metadata
        from transformers import GenerationConfig
        source_module = sys.modules[type(model).__module__]
        report.update(model=self.candidate.model, revision=self.candidate.revision,
                      cuda_visible_devices=self.cuda_visible_devices,
                      device_name=torch.cuda.get_device_name(0), cuda=torch.version.cuda)
        report.update(attention=getattr(model.config, "_attn_implementation", None),
            recurrent_fast_path=getattr(source_module, "is_fast_path_available", None),
            generation_config=GenerationConfig(**candidate_settings(tokenizer, self.candidate)["generation"]).to_dict(),
            packages={name: importlib.metadata.version(name) for name in
                      ("torch", "transformers", "accelerate", "bitsandbytes", "tokenizers", "huggingface-hub")})
        return TransformersBackend(torch, model, tokenizer, self.candidate, report)


class _FiniteScores:
    def __init__(self, torch):
        self.torch, self.steps = torch, 0

    def __call__(self, input_ids, scores):
        if not self.torch.isfinite(scores).all().item():
            raise ValueError("nonfinite model scores; stop instead of sanitizing or retrying")
        self.steps += 1
        return scores


class TransformersBackend:
    """One resident model, fresh cache and per-call CPU/CUDA RNG assignment."""

    def __init__(self, torch, model, tokenizer, candidate, load_report):
        self.torch, self.model, self.tokenizer = torch, model, tokenizer
        self.settings = candidate_settings(tokenizer, candidate)
        self.load_report = load_report
        self.pid = os.getpid()
        self.active = False

    def __call__(self, view, rendered, tokenized, *, seed, settings):
        from .attempts import MeasuredReply
        from .storage import record_json, settings_json
        from transformers import DynamicCache, GenerationConfig, LogitsProcessorList

        if os.getpid() != self.pid or self.active:
            raise ValueError("the model and global RNG belong to one serial process")
        if type(seed) is not int or not 0 <= seed < 2**63:
            raise ValueError("use the saved nonnegative per-call seed")
        if settings_json(settings) != settings_json(self.settings):
            raise ValueError("exact model/template/decoding settings differ")
        if (len(tokenized.input_ids) + MAX_OUTPUT_TOKENS > MAX_CONTEXT_TOKENS
                or render_request(view) != rendered
                or record_json(asdict(tokenize_request(rendered, self.tokenizer))) != record_json(asdict(tokenized))):
            raise ValueError("exact permitted request/tokenization/capacity equality failed before generation")
        torch = self.torch
        self.active = True
        cache = output = None
        handles = []
        cache_checks = {"calls": 0, "initial_empty": True, "same_call_cache": True}
        scores = _FiniteScores(torch)
        try:
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.cuda.reset_peak_memory_stats(0)
            cache = DynamicCache(config=self.model.config)
            if cache.get_seq_length() != 0 or cache.has_previous_state():
                raise ValueError("a new call must start with empty KV/recurrent state")

            def check_cache(module, args, kwargs):
                cache_checks["calls"] += 1
                if kwargs.get("past_key_values") is not cache:
                    cache_checks["same_call_cache"] = False
                    raise ValueError("generation replaced or reused an unowned cache")

            handles.append(self.model.register_forward_pre_hook(check_cache, with_kwargs=True))
            inputs = torch.tensor([tokenized.input_ids], dtype=torch.long, device="cuda:0")
            mask = torch.tensor([tokenized.attention_mask], dtype=torch.long, device="cuda:0")
            # A fresh config avoids inherited checkpoint penalties, stopping
            # strings, forced tokens or schema constraints. The seed is not a
            # claim that regeneration will be exact on another order/device.
            config = GenerationConfig(**self.settings["generation"])
            with torch.inference_mode():
                output = self.model.generate(input_ids=inputs, attention_mask=mask,
                    generation_config=config, past_key_values=cache,
                    logits_processor=LogitsProcessorList([scores]))
            torch.cuda.synchronize(0)
            sequences = output.sequences.tolist()
            if (len(sequences) != 1 or sequences[0][:len(tokenized.input_ids)] != list(tokenized.input_ids)
                    or not cache_checks["calls"] or not scores.steps):
                raise ValueError("one exact prompt prefix and observed cache/finite scores are required")
            ids = tuple(sequences[0][len(tokenized.input_ids):])
            reply, raw_suffix = decode_suffix(self.tokenizer, ids)
            free, total = torch.cuda.mem_get_info(0)
            diagnostics = {"raw_suffix_text": raw_suffix,
                "removed_terminal_id": TRANSPORT_ID if ids[-1] == TRANSPORT_ID else None,
                "seed": seed, "cpu_seed": torch.initial_seed(),
                "cuda_seed": torch.cuda.initial_seed(), "pid": self.pid,
                "cache": dict(cache_checks, disposed_after_call=True),
                "finite_score_steps": scores.steps, "device": "cuda:0",
                "allocated_bytes": torch.cuda.memory_allocated(0),
                "reserved_bytes": torch.cuda.memory_reserved(0),
                "peak_reserved_bytes": torch.cuda.max_memory_reserved(0),
                "free_bytes_with_cache": free, "total_bytes": total}
            # Raw output persists even if its measured headroom is inadequate;
            # M5-T02 interprets that evidence without resampling the slot.
            return MeasuredReply(reply, torch.cuda.max_memory_allocated(0), diagnostics)
        finally:
            for handle in handles:
                handle.remove()
            output = cache = None
            self.active = False
