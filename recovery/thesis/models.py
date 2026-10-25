"""Two explicit model systems, exact requests, GPU loaders and a scripted double.

Specification section 3.8. There is no registry: exactly the two pinned systems
in configs/thesis.json. Importing this module never imports torch/transformers.
Qwen reuses the reviewed loader and generation path of recovery.inference;
Granite has its own equivalent loader with its own end-of-sequence framing.
"""

from dataclasses import dataclass, field
import json
import os
import random
import re
import sys
import threading
from time import monotonic, sleep
from types import SimpleNamespace

from ..i01.core import canonical
from . import MODELS, digest_bytes
from .protocol import messages, notice_text  # noqa: F401

GENERATION_KEYS = ("do_sample", "temperature", "top_p", "top_k", "min_p", "repetition_penalty",
                   "num_beams", "max_new_tokens", "eos_token_id", "pad_token_id", "use_cache",
                   "return_dict_in_generate", "output_scores", "remove_invalid_values")


def model_entry(config, model):
    if model not in MODELS:
        raise ValueError("only the two adopted model systems exist")
    return config["models"][model]


def settings(config, model, tokenizer, input_limit):
    """Exact decoding, framing and limits recorded with every request."""
    entry = model_entry(config, model)
    scripted = getattr(tokenizer, "scripted", False)
    if not scripted and (tokenizer.eos_token_id != entry["transport_token_id"]
                         or tokenizer.pad_token_id != entry["pad_token_id"]
                         or type(tokenizer.chat_template) is not str or not tokenizer.chat_template):
        raise ValueError(f"{model} tokenizer framing differs from the pinned configuration")
    if input_limit not in (config["input_tokens"], config["alternative_input_tokens"]):
        raise ValueError("input limit must be 8,192 or the CPU-decided uniform 12,288")
    generation = dict(do_sample=True, temperature=entry["temperature"], top_p=entry["top_p"],
                      top_k=entry["top_k"], min_p=0.0, repetition_penalty=1.0, num_beams=1,
                      max_new_tokens=config["output_tokens"], eos_token_id=list(entry["eos_token_ids"]),
                      pad_token_id=entry["pad_token_id"], use_cache=True, return_dict_in_generate=True,
                      output_scores=False, remove_invalid_values=False)
    if entry["attention"] == "recovery_t4_sdpa":
        generation["prefill_chunk_size"] = 256
    return dict(regime=config["regime"], model=model, repo=entry["repo"], revision=entry["revision"],
                scripted=scripted, chat_template_sha256=digest_bytes(tokenizer.chat_template.encode("utf-8")),
                enable_thinking=False, input_limit=input_limit, output_limit=config["output_tokens"],
                quantization="NF4-double-FP16", attention=entry["attention"],
                transport_token_id=entry["transport_token_id"], generation=generation)


def prepare(view, seed, config, model, tokenizer, input_limit, *, control=False, envelope=False):
    """Render with the native template, tokenize once and refuse oversize input."""
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError("use the saved nonnegative 63-bit seed")
    cfg = settings(config, model, tokenizer, input_limit)
    msgs = messages(view, control=control)
    rendered = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                             enable_thinking=False)
    ids = tokenizer.encode(rendered, add_special_tokens=False)
    if envelope:
        # Hardware diagnostic only: pad the control prompt to the full input limit.
        padding = tokenizer.encode(" 0", add_special_tokens=False)
        if not padding or len(ids) > input_limit:
            raise ValueError("invalid envelope framing")
        ids = (padding * (input_limit - len(ids)))[:input_limit - len(ids)] + ids
        rendered = tokenizer.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
    if len(ids) > input_limit:
        raise ValueError(f"permitted input has {len(ids)} tokens > {input_limit}; history is never truncated")
    return dict(view=view, messages=msgs, rendered=rendered, input_ids=ids, attention_mask=[1] * len(ids),
                seed=seed, settings=cfg, control=control, envelope=envelope)


def load_tokenizer(config, model, snapshot):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
    settings(config, model, tokenizer, config["input_tokens"])
    return tokenizer


# ---------------------------------------------------------------------------
# GPU adapters (run inside a spawned resident child; imports are lazy).
# ---------------------------------------------------------------------------

class Adapter:
    """Rebuild the exact request, generate once with fresh state, report evidence."""

    def __init__(self, backend, config, model, input_limit):
        self.backend, self.config, self.model, self.input_limit = backend, config, model, input_limit
        self.load_report = backend.load_report

    def __call__(self, request):
        backend = self.backend
        rebuilt = prepare(request["view"], request["seed"], self.config, self.model, backend.tokenizer,
                          request["settings"]["input_limit"], control=request["control"],
                          envelope=request["envelope"])
        if canonical(rebuilt) != canonical(request):
            raise ValueError("exact permitted rendering/tokenization/settings/seed mismatch")
        backend.settings = dict(generation={k: v for k, v in request["settings"]["generation"].items()})
        backend.limits = SimpleNamespace(output_tokens=request["settings"]["output_limit"])
        stop, samples = threading.Event(), []

        def observe():
            while not stop.is_set():
                samples.append(backend.torch.cuda.mem_get_info(0)[0])
                stop.wait(.05)

        observer = threading.Thread(target=observe, daemon=True)
        started = monotonic()
        observer.start()
        try:
            measured = backend._generate(SimpleNamespace(input_ids=tuple(request["input_ids"]),
                                                         attention_mask=tuple(request["attention_mask"])),
                                         request["seed"], force_output_reserve=request["envelope"])
        finally:
            stop.set()
            observer.join(timeout=1)
        if observer.is_alive() or not samples:
            raise ValueError("GPU headroom observation did not settle")
        elapsed = monotonic() - started
        reply = measured.response
        visible = "" if request["envelope"] else reply.text
        framing_error = None
        if not request["envelope"] and len(backend.tokenizer.encode(visible, add_special_tokens=False)) > request["settings"]["output_limit"]:
            framing_error = "visible_output_limit"
        diagnostics = dict(measured.backend)
        diagnostics["observed_free_min_bytes"] = min(samples)
        diagnostics["memory_samples"] = len(samples)
        diagnostics["observed_peak_free_lower_bytes"] = min(
            min(samples), diagnostics["free_bytes_with_cache"],
            diagnostics["free_bytes_with_cache"] + diagnostics["reserved_bytes"] - diagnostics["peak_reserved_bytes"])
        return dict(raw_text=reply.text, visible_text=visible, token_ids=list(reply.token_ids),
                    termination=reply.termination, truncated=reply.termination == "length",
                    framing_error=framing_error, ready_seconds=elapsed, input_tokens=len(request["input_ids"]),
                    generated_tokens=len(reply.token_ids), backend=diagnostics,
                    peak_memory_bytes=measured.peak_memory_bytes, failure=None)


def _one_t4(device):
    if type(device) is not str or device not in ("0", "1"):
        raise ValueError("one explicit physical GPU index")
    torch = sys.modules.get("torch")
    if torch is not None and torch.cuda.is_initialized():
        raise ValueError("device visibility must precede CUDA initialization")
    os.environ["CUDA_VISIBLE_DEVICES"] = device
    import torch
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise ValueError("one available CUDA device is required; never offload to CPU")
    if "T4" not in torch.cuda.get_device_name(0):
        raise ValueError("the adopted execution path requires an actual T4")
    return torch


class GraniteBackend:
    """Fresh-cache serial generation for Granite, mirroring the reviewed Qwen path."""

    def __init__(self, torch, model, tokenizer, load_report, eos, transport):
        self.torch, self.model, self.tokenizer, self.load_report = torch, model, tokenizer, load_report
        self.eos, self.transport = tuple(eos), transport
        self.pid, self.active = os.getpid(), False
        self.settings = self.limits = None

    def _generate(self, tokenized, seed, *, force_output_reserve=False):
        from recovery.attempts import MeasuredReply
        from recovery.protocol import GeneratedReply
        from transformers import DynamicCache, GenerationConfig, LogitsProcessorList
        if os.getpid() != self.pid or self.active:
            raise ValueError("the model and global RNG belong to one serial process")
        torch, self.active = self.torch, True
        checks = {"calls": 0, "initial_empty": True, "same_call_cache": True}
        scores = _FiniteScores(torch)
        cache = handles = None
        try:
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.cuda.reset_peak_memory_stats(0)
            cache = DynamicCache(config=self.model.config)
            if cache.get_seq_length() != 0:
                raise ValueError("a new call must start with an empty cache")

            def check(module, args, kwargs):
                checks["calls"] += 1
                if kwargs.get("past_key_values") is not cache:
                    checks["same_call_cache"] = False
                    raise ValueError("generation replaced or reused an unowned cache")

            handles = [self.model.register_forward_pre_hook(check, with_kwargs=True)]
            inputs = torch.tensor([tokenized.input_ids], dtype=torch.long, device="cuda:0")
            mask = torch.tensor([tokenized.attention_mask], dtype=torch.long, device="cuda:0")
            config = GenerationConfig(**self.settings["generation"])
            if force_output_reserve:
                config.eos_token_id = []
                config.min_new_tokens = config.max_new_tokens = self.limits.output_tokens
            with torch.inference_mode():
                output = self.model.generate(input_ids=inputs, attention_mask=mask, generation_config=config,
                                             past_key_values=cache, logits_processor=LogitsProcessorList([scores]))
            torch.cuda.synchronize(0)
            sequences = output.sequences.tolist()
            if (len(sequences) != 1 or sequences[0][:len(tokenized.input_ids)] != list(tokenized.input_ids)
                    or not checks["calls"] or not scores.steps):
                raise ValueError("one exact prompt prefix and observed cache/finite scores are required")
            ids = tuple(sequences[0][len(tokenized.input_ids):])
            if not ids or len(ids) > self.limits.output_tokens:
                raise ValueError("expected one nonempty generated suffix within the output cap")
            raw = self.tokenizer.decode(list(ids), skip_special_tokens=False, clean_up_tokenization_spaces=False)
            terminal = ids[-1] == self.transport
            text = self.tokenizer.decode(list(ids[:-1]), skip_special_tokens=False,
                                         clean_up_tokenization_spaces=False) if terminal else raw
            termination = "eos" if ids[-1] in self.eos else "length"
            if termination == "length" and len(ids) != self.limits.output_tokens:
                raise ValueError("unexplained early stop")
            free, total = torch.cuda.mem_get_info(0)
            diagnostics = {"raw_suffix_text": raw, "removed_terminal_id": self.transport if terminal else None,
                           "seed": seed, "pid": self.pid, "cache": dict(checks, disposed_after_call=True),
                           "finite_score_steps": scores.steps, "device": "cuda:0",
                           "allocated_bytes": torch.cuda.memory_allocated(0),
                           "reserved_bytes": torch.cuda.memory_reserved(0),
                           "peak_reserved_bytes": torch.cuda.max_memory_reserved(0),
                           "free_bytes_with_cache": free, "total_bytes": total}
            return MeasuredReply(GeneratedReply(text, ids, termination), torch.cuda.max_memory_allocated(0), diagnostics)
        finally:
            for handle in handles or ():
                handle.remove()
            cache = None
            self.active = False


class _FiniteScores:
    def __init__(self, torch):
        self.torch, self.steps = torch, 0

    def __call__(self, input_ids, scores):
        if not self.torch.isfinite(scores).all().item():
            raise ValueError("nonfinite model scores; recorded as a provider failure")
        self.steps += 1
        return scores


def audit_granite(model, info, torch):
    """No missing/unexpected language weights; one complete local FP16/NF4 replica."""
    if type(model).__name__ != "GraniteForCausalLM":
        raise ValueError("GraniteForCausalLM required")
    if any(info.get(k) for k in ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")):
        raise ValueError("unexplained missing/unexpected/mismatched Granite weights: " + repr(info))
    if not getattr(model, "is_loaded_in_4bit", False):
        raise ValueError("the replica must actually be loaded in 4-bit NF4")
    q = model.hf_quantizer.quantization_config
    if q.bnb_4bit_quant_type != "nf4" or q.bnb_4bit_use_double_quant is not True or q.bnb_4bit_compute_dtype != torch.float16:
        raise ValueError("actual quantization must be NF4/double/FP16")
    tensors = list(model.named_parameters()) + list(model.named_buffers())
    if any(t.device.type != "cuda" or t.device.index != 0 for _, t in tensors):
        raise ValueError("one complete local CUDA replica; no offload or splitting")
    if any(t.is_floating_point() and t.dtype not in (torch.float16, torch.float32) for _, t in tensors):
        raise ValueError("unexpected precision; FP16 with FP32 sensitive paths only")
    return dict(loading_info={k: sorted(v) if isinstance(v, set) else v for k, v in info.items()},
                tensors=len(tensors), attention=getattr(model.config, "_attn_implementation", None))


@dataclass(frozen=True)
class Factory:
    """Spawn-picklable loader for one replica; calling it requires authorized GPU work."""
    config: dict
    model: str
    device: str
    snapshot: str
    input_limit: int

    def __call__(self):
        os.environ["HF_HUB_OFFLINE"] = "1"
        entry = model_entry(self.config, self.model)
        if self.model == "qwen":
            from recovery.inference import ModelFactory, course_candidate
            from recovery.prompts import COURSE_LIMITS
            backend = ModelFactory(course_candidate("9B"), self.device, COURSE_LIMITS, local_directory=self.snapshot)()
        else:
            torch = _one_t4(self.device)
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
            tokenizer = AutoTokenizer.from_pretrained(self.snapshot, local_files_only=True, trust_remote_code=False)
            quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                              bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
            print(f"Model load: Granite pinned weights on physical device {self.device}", flush=True)
            model, info = AutoModelForCausalLM.from_pretrained(
                self.snapshot, local_files_only=True, trust_remote_code=False, quantization_config=quantization,
                dtype=torch.float16, device_map={"": 0}, attn_implementation="sdpa", output_loading_info=True)
            model.eval()
            report = audit_granite(model, info, torch)
            backend = GraniteBackend(torch, model, tokenizer, report, entry["eos_token_ids"], entry["transport_token_id"])
        settings(self.config, self.model, backend.tokenizer, self.input_limit)
        properties = backend.torch.cuda.get_device_properties(0)
        backend.load_report.update(model=self.model, repo=entry["repo"], revision=entry["revision"],
                                   snapshot=self.snapshot, physical_device=self.device,
                                   cuda_device_uuid=str(properties.uuid), total_device_bytes=properties.total_memory)
        return Adapter(backend, self.config, self.model, self.input_limit)


# ---------------------------------------------------------------------------
# Scripted double: CPU rehearsal and tests through the same process boundary.
# Its replies are never model evidence.
# ---------------------------------------------------------------------------

class ScriptedTokenizer:
    """Deterministic reversible tokenizer: one token per 4 UTF-8 bytes, close to the
    pinned tokenizers' measured density on this protocol's text (request overhead
    1,411 scripted versus 1,472 Qwen and 1,433 Granite tokens on 25 October 2026),
    with a simple chat template."""
    scripted = True
    eos_token_id = pad_token_id = 0
    chat_template = "SCRIPTED: <system>/<user>/<assistant> chunk template"

    def apply_chat_template(self, msgs, *, tokenize, add_generation_prompt, enable_thinking):
        if tokenize or not add_generation_prompt or enable_thinking is not False:
            raise ValueError("scripted template mirrors the adopted call")
        return "".join(f"<{m['role']}>\n{m['content']}\n" for m in msgs) + "<assistant>\n"

    def encode(self, text, add_special_tokens=False):
        data = text.encode("utf-8")
        return [sum((b + 1) * 257 ** j for j, b in enumerate(data[i:i + 4])) for i in range(0, len(data), 4)]

    def decode(self, ids, skip_special_tokens=False, clean_up_tokenization_spaces=False):
        out = bytearray()
        for value in ids:
            while value:
                value, rest = divmod(value, 257)
                out.append(rest - 1)
        return out.decode("utf-8", errors="replace")


def _scripted_text(request, rng):
    """A plausible deterministic policy with occasional mistakes."""
    view = request["view"]
    if request["control"]:
        return json.dumps(dict(message=None, submit=max(view["complete_input"]), wait=False))
    shard = view["shard"]
    local = max(shard)
    reports = []
    for entry in view["history"][view["earlier"]:]:
        if entry["kind"] == "received_message":
            reports += [int(n) for n in re.findall(r"-?\d+", entry["text"])]
    roll = rng.random()
    if roll < 0.06:
        return "I think the answer is " + str(local)          # malformed
    if roll < 0.10:
        return json.dumps(dict(message=None, submit=None, wait=True))
    if roll < 0.16:
        return json.dumps(dict(message=f"My local maximum is {local}.", submit=local, wait=False))
    if reports:
        best = max(local, max(reports))
        return json.dumps(dict(message=f"My local maximum is {local}; submitting {best}.", submit=best, wait=False))
    return json.dumps(dict(message=f"My local maximum is {local}.", submit=None, wait=False))


class ScriptedProvider:
    def __init__(self, model, behaviors):
        self.model, self.behaviors = model, dict(behaviors)
        self.tokenizer = ScriptedTokenizer()
        self.load_report = dict(scripted=True, model=model, cuda_device_uuid="scripted", total_device_bytes=0,
                                note="Scripted CPU double; never model or GPU evidence.")

    def __call__(self, request):
        behavior = self.behaviors.get(request["seed"])
        if behavior and behavior.startswith("once:"):
            # "once:|<marker-path>|<behavior>" fires only the first time (marker file).
            _, marker, behavior = behavior.split("|") if "|" in behavior else (None, None, None)
            if marker and not os.path.exists(marker):
                open(marker, "w").close()
            else:
                behavior = None
        if behavior == "exit":
            os._exit(3)
        if behavior == "hang":
            sleep(3600)
        if behavior == "defect":
            raise ValueError("scripted nonfinite scores")
        started = monotonic()
        if request["envelope"]:
            text, ids, termination = "0" * request["settings"]["output_limit"], [48] * request["settings"]["output_limit"], "length"
        else:
            rng = random.Random(request["seed"])
            text = _scripted_text(request, rng)
            if behavior == "invalid":
                text = "```json\n" + text + "\n```"
            ids, termination = self.tokenizer.encode(text) + [0], "eos"
            if behavior == "truncate":
                ids, termination = [121] * request["settings"]["output_limit"], "length"
                text = "x" * request["settings"]["output_limit"]
        backend = dict(finite_score_steps=len(ids), cache=dict(initial_empty=True, same_call_cache=True, calls=1),
                       observed_free_min_bytes=8 * 2**30, observed_peak_free_lower_bytes=8 * 2**30,
                       scripted=True)
        return dict(raw_text=text, visible_text="" if request["envelope"] else text, token_ids=ids,
                    termination=termination, truncated=termination == "length", framing_error=None,
                    ready_seconds=monotonic() - started, input_tokens=len(request["input_ids"]),
                    generated_tokens=len(ids), backend=backend, peak_memory_bytes=0, failure=None)


@dataclass(frozen=True)
class ScriptedFactory:
    model: str
    behaviors: tuple = field(default_factory=tuple)

    def __call__(self):
        return ScriptedProvider(self.model, self.behaviors)


# ---------------------------------------------------------------------------
# CPU capacity proof (specification sections 3.8 and 5).
# ---------------------------------------------------------------------------

def capacity_bound(config, model, tokenizer, input_limit):
    """Conservative worst reachable request size, as in the reviewed I-01 check."""
    from .protocol import THESIS_SYSTEM  # noqa: F401
    from ..i01.core import REJECTION_FEEDBACK
    world = dict(id="capacity", owner=0, row=19, after=-1000, first=0,
                 original=[[-1000] * 19 + [1000], [-1000] * 20], revised=[[-1000] * 20, [-1000] * 20])
    feedback = max(REJECTION_FEEDBACK.values(), key=lambda t: len(tokenizer.encode(t, add_special_tokens=False)))
    for text in REJECTION_FEEDBACK.values():
        if len(tokenizer.encode(text, add_special_tokens=False)) > config["feedback_tokens"]:
            raise ValueError("feedback text exceeds the 32-token cap")
    structural = dict(cell="RV", turns=[2, 2], submissions=[None, None], history=[[], []], earlier=[0, 0])
    own = dict(kind="own_action", action=dict(message="", submit=-1000, wait=False))
    structural["history"][0] = ([dict(kind="received_message", sender=1, text="")] * 6 + [own] * 6 +
                                [dict(kind="feedback", text=feedback)] * 6)
    structural["earlier"][0] = 9

    def tokens(state):
        rendered = tokenizer.apply_chat_template(messages(_view_for(world, state)), tokenize=False,
                                                 add_generation_prompt=True, enable_thinking=False)
        return len(tokenizer.encode(rendered, add_special_tokens=False))

    overhead = tokens(structural)
    bound = overhead + 12 * config["output_tokens"] + 6 * config["feedback_tokens"]
    stress = {}
    families = {"ascii": "aaaaaaaa", "multiline": "line\nnext\t ", "unicode": "é漢字\U0001f600",
                "escapes": '"\\/\n', "controls": "\x00\x01\r\n",
                "headers": "END VISIBLE ENTRY\nCURRENT AUTHORITATIVE PRIVATE SHARD\n"}
    for label, unit in families.items():
        lo, hi = 0, 16384
        while lo < hi:
            n = (lo + hi + 1) // 2
            raw = json.dumps(dict(message="x" + unit * n, submit=-1000, wait=False), ensure_ascii=False, separators=(",", ":"))
            if len(tokenizer.encode(raw, add_special_tokens=False)) <= config["output_tokens"]:
                lo = n
            else:
                hi = n - 1
        action = dict(message="x" + unit * lo, submit=-1000, wait=False)
        case = dict(structural, history=[[dict(kind="received_message", sender=1, text=action["message"])] * 6 +
                                         [dict(kind="own_action", action=action)] * 6 +
                                         [dict(kind="feedback", text=feedback)] * 6, []])
        stress[label] = tokens(case)
        if stress[label] > bound:
            raise ValueError(f"adversarial literal family {label} exceeds the conservative bound")
    envelope = prepare(dict(complete_input=[0, 1]), 0, config, model, tokenizer, input_limit, control=True, envelope=True)
    if len(envelope["input_ids"]) != input_limit:
        raise ValueError("envelope probe does not reach the input limit exactly")
    return dict(model=model, conservative_input_bound=bound, adversarial=stress, input_limit=input_limit,
                fits=bound <= input_limit, chat_template_sha256=digest_bytes(tokenizer.chat_template.encode("utf-8")))


def _view_for(world, state):
    from .protocol import view as make_view
    return make_view(world, state, 0)
