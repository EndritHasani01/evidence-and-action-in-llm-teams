"""I-01 boundary around the reviewed text-only NF4 loader and fresh-cache engine."""

from dataclasses import dataclass
import json
from time import monotonic
from types import SimpleNamespace

from .core import canonical, messages
from . import assisted


def settings(config, mode, tokenizer):
    if assisted(config) and mode != "direct":
        raise ValueError("The assisted I-01 condition is direct only")
    if mode not in ("direct", "thinking"):
        raise ValueError("only declared modes")
    from recovery.inference import EOS_IDS, PAD_ID, TRANSPORT_ID
    from recovery.t4_attention import T4_ATTENTION, PREFILL_CHUNK_SIZE
    if tokenizer.eos_token_id != TRANSPORT_ID or tokenizer.pad_token_id != PAD_ID:
        raise ValueError("pinned tokenizer framing differs")
    return dict(regime=config["regime"], model=config["model"], revision=config["revision"], mode=mode,
                chat_template=tokenizer.chat_template, input_limit=8192, visible_limit=512,
                quantization="NF4-double-FP16", attention=T4_ATTENTION, presence_penalty=0,
                generation=dict(do_sample=True, temperature=0.7 if mode == "direct" else 1.0,
                                top_p=0.8 if mode == "direct" else 0.95, top_k=20, min_p=0.0,
                                repetition_penalty=1.0, num_beams=1,
                                max_new_tokens=512 if mode == "direct" else 4096,
                                eos_token_id=list(EOS_IDS), pad_token_id=PAD_ID, use_cache=True,
                                return_dict_in_generate=True, output_scores=False,
                                remove_invalid_values=False, prefill_chunk_size=PREFILL_CHUNK_SIZE))


def prepare(view, seed, config, mode, tokenizer, *, control=False, envelope=False):
    cfg = settings(config, mode, tokenizer)
    msgs = messages(view, control=control, regime=config["regime"])
    rendered = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                             enable_thinking=mode == "thinking")
    ids = tokenizer.encode(rendered, add_special_tokens=False)
    if envelope:
        # Synthetic diagnostic only, never used to force scientific responses.
        padding = tokenizer.encode(" 0", add_special_tokens=False)
        if not padding or len(ids) > 8192:
            raise ValueError("invalid envelope framing")
        ids = (padding * (8192 - len(ids)))[:8192-len(ids)] + ids
        rendered = tokenizer.decode(ids,skip_special_tokens=False,clean_up_tokenization_spaces=False)
    if len(ids) > 8192:
        raise ValueError("full permitted input exceeds 8192; never truncate")
    return dict(view=view, messages=msgs, rendered=rendered, input_ids=ids,
                attention_mask=[1]*len(ids), seed=seed, settings=cfg,
                control=control, envelope=envelope)


def split_visible(tokenizer, reply, mode):
    text = reply.text
    thinking = None
    if mode == "thinking":
        if text.count("</think>") != 1:
            return "", text, "thinking_framing_defect"
        thinking, text = text.split("</think>", 1)
        # Template opens thinking; preserve raw text, only separate final framing.
        text = text.lstrip("\n")
    if len(tokenizer.encode(text, add_special_tokens=False)) > 512:
        return text, thinking, "visible_output_limit"
    return text, thinking, None


@dataclass(frozen=True)
class ModelFactory:
    config: dict
    device: str
    snapshot: str

    def __call__(self):
        import os
        os.environ["HF_HUB_OFFLINE"] = "1"
        from recovery.inference import ModelFactory as ReviewedFactory, course_candidate
        from recovery.prompts import COURSE_LIMITS
        backend = ReviewedFactory(course_candidate("9B"), self.device, COURSE_LIMITS,local_directory=self.snapshot)()
        backend.load_report["i01_loading_only"] = True
        backend.load_report['verified_snapshot']=self.snapshot
        properties=backend.torch.cuda.get_device_properties(0)
        backend.load_report["cuda_device_uuid"]=str(properties.uuid)
        backend.load_report["total_device_bytes"]=properties.total_memory
        return Adapter(backend, self.config)


class Adapter:
    def __init__(self, backend, config):
        self.backend, self.config = backend, config
        self.load_report = backend.load_report

    def __call__(self, request):
        backend = self.backend
        rebuilt = prepare(request["view"], request["seed"], self.config, request["settings"]["mode"],
                          backend.tokenizer, control=request["control"], envelope=request["envelope"])
        if canonical(rebuilt) != canonical(request):
            raise ValueError("exact permitted rendering/tokenization/settings/seed mismatch")
        backend.settings = request["settings"]
        backend.limits = SimpleNamespace(output_tokens=request["settings"]["generation"]["max_new_tokens"])
        from threading import Event, Thread
        stop=Event(); samples=[]
        def observe_memory():
            while not stop.is_set():
                samples.append(backend.torch.cuda.mem_get_info(0)[0])
                stop.wait(.05)
        observer=Thread(target=observe_memory,daemon=True)
        started = monotonic()
        observer.start()
        try:
            measured = backend._generate(SimpleNamespace(input_ids=tuple(request["input_ids"]),
                                                         attention_mask=tuple(request["attention_mask"])),
                                         request["seed"], force_output_reserve=request["envelope"])
        finally:
            stop.set(); observer.join(timeout=1)
        if observer.is_alive() or not samples:
            raise ValueError("GPU headroom observation did not settle")
        elapsed = monotonic()-started
        reply = measured.response
        visible, thinking, framing_error = split_visible(backend.tokenizer, reply, request["settings"]["mode"])
        if request["envelope"]:
            # Forced diagnostic tokens have no scientific action/final framing.
            visible, thinking, framing_error = "", None, None
        diagnostics = measured.backend
        diagnostics["observed_free_min_bytes"]=min(samples)
        diagnostics["memory_samples"]=len(samples)
        diagnostics["observed_peak_free_lower_bytes"] = min(min(samples),diagnostics["free_bytes_with_cache"],
            diagnostics["free_bytes_with_cache"] + diagnostics["reserved_bytes"] - diagnostics["peak_reserved_bytes"])
        return dict(raw_text=reply.text, visible_text=visible, thinking=thinking,
                    token_ids=list(reply.token_ids), termination=reply.termination,
                    truncated=reply.termination == "length", framing_error=framing_error,
                    ready_seconds=elapsed, input_tokens=len(request["input_ids"]),
                    generated_tokens=len(reply.token_ids), backend=diagnostics,
                    peak_memory_bytes=measured.peak_memory_bytes, failure=None)
