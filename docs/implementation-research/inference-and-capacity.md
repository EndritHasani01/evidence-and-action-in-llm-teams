# Inference and capacity decisions

Investigation: 4 October 2026. Authority: [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md), especially §§3.2, 8 and 9. This document records metadata, source inspection and CPU tokenizer probes. It does **not** report model loading, inference, a complete attainability witness, a pilot or T4 feasibility.

## Findings that affect planning

1. A maintained Transformers text-only loading path exists; do not load the vision-language wrapper merely because the checkpoint's architecture names it.
2. The pinned checkpoint's BF16 defaults must be overridden explicitly. Its supported recurrent fallback deliberately performs some operations in FP32; that behavior is compatible with the specification, but its memory and latency remain unmeasured on T4.
3. Candidate shapes and one-shard forwarding fit 384 tokens in the isolated fixtures. A deliberately crowded history fixture leaves only **633 tokens** for additional instructions/fields. The final renderer needs a hard capacity gate before GPU use.
4. Chat-template rewriting, termination IDs and decoding can silently change the scientific protocol. Preserve exact requests and generated token IDs; do not normalize away unexpected generated markers.
5. This workstation has CPU-only PyTorch. Passing tokenizer probes here cannot establish the GPU environment lock or admission thresholds.

## Evidence boundary and repository state

The current repository has no recovery inference implementation. Historical `research/01_original_blueprint/requirements-inference.in` and its configuration are proposals for an older design, not a passing environment lock. The vendored SILO runner's inference/retry lifecycle is unsuitable for the new protocol; mathematical task solvers may support the later scripted witness, with independent truth checks.

The read-only environment probe found Python 3.11.9, torch **2.11.0**, transformers **5.12.0**, accelerate **1.14.0**, bitsandbytes **0.49.2**, tokenizers **0.22.2**, huggingface-hub **1.19.0** and Jinja2 **3.1.6**. `torch.version.cuda is None`, `torch.cuda.is_available() is False`, and `nvidia-smi` was absent from PATH. Native Qwen model-class resolution imported successfully without constructing a model or downloading weights. These versions identify what was inspected; they are not a proposed GPU lock.

Only tokenizer/template/config/index metadata were downloaded to a temporary directory, approximately 13 MB per checkpoint. Model weights were not downloaded. The Hub API and immutable revisions checked were:

| Checkpoint | Revision | Important language difference |
|---|---|---|
| [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a) | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | Untied input embedding and `lm_head` |
| [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B/tree/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a) | `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` | Tied embedding/output head; no separate `lm_head.weight` in the index |

Both revisions have byte-identical tokenizer JSON, tokenizer configuration and external chat template. SHA-256: tokenizer JSON `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42`; template `a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715`. Freeze the accepted revision and actual template contents later; a model change still requires renewed capability checks despite this tokenizer equality.

## Text-only loading and T4 behavior

Transformers 5.12.0's [AutoModel mapping](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/auto/modeling_auto.py#L779) maps the multimodal `qwen3_5` configuration to `Qwen3_5ForCausalLM`. The [AutoModel factory](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/auto/auto_factory.py) extracts `text_config` when that is the selected class's configuration type. The [conversion mapping](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/conversion_mapping.py#L782) removes the `language_model` checkpoint prefix. CPU inspection resolved both checkpoints to this class and identified actual `model.language_model.*` index keys.

**Recommendation:** use this native `AutoModelForCausalLM.from_pretrained` path with the immutable checkpoint revision; use `AutoTokenizer`, no multimodal processor or remote model code. Do not manually rename checkpoint weights or create a converted language-only checkpoint. The native class constructs a text model and explicitly recognizes unused vision/MTP keys. At the later load gate, inspect loading diagnostics and reject every unexplained missing or newly initialized language weight. The 4B tied head is expected, not a missing-weight failure. Metadata inspection is not evidence that NF4 loading has passed. [Text-only class source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py#L1613).

Set all four quantization choices explicitly: `load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`, `bnb_4bit_use_double_quant=True`, and `bnb_4bit_compute_dtype=torch.float16`; also set the model's ordinary `dtype=torch.float16`. `dtype="auto"` follows the checkpoint's BF16 declaration, and the bitsandbytes compute default is FP32. These are separate settings. NF4 support includes T4-class hardware, but that does not establish whole-model compatibility. [Official quantization documentation](https://huggingface.co/docs/transformers/quantization/bitsandbytes).

The inspected Qwen source provides ordinary PyTorch convolution and gated-delta fallbacks when optional fast kernels are absent. It casts recurrent intermediates/state, normalization, rotary calculations and attention softmax to FP32 in sensitive paths. In particular, its FP16 guard computes `A_log.float().exp()` rather than the overflowing FP16 exponential. Preserve these supported casts instead of adding blanket FP16 conversions or custom kernels. This is source evidence; finite outputs and actual precision/kernel paths still require the smoke gate. [Pinned model source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py).

[NVIDIA's T4 specifications](https://www.nvidia.com/en-us/data-center/tesla-t4/) list 16 GB and FP16/FP32 mixed precision. The upstream [FlashAttention-2 support statement](https://github.com/Dao-AILab/flash-attention#nvidia-cuda-support) requires newer architectures for its standard CUDA path. Prefer supported PyTorch attention/recurrent execution; record what is actually selected. Installing another serving stack, special Turing kernels, CPU offload or a split two-GPU model would violate or complicate the specified execution regime.

Two memory observations explain why estimates cannot replace the hardware gate:

- 9B has a large **untied** vocabulary embedding and output head that do not all become four-bit linear weights. A naive parameter-count-times-four-bits estimate omits this and runtime buffers.
- From the inspected configuration, eight full-attention layers at 8,192 tokens need approximately **256 MiB** of FP16 KV storage; 24 linear layers' FP32 recurrent matrices add approximately **48 MiB**, excluding convolution state and all activations. FP32 prefill intermediates and allocator reservations add further memory. These are arithmetic component estimates, not measured peaks.

The generation source defaults `logits_to_keep=1` for supporting models, avoiding a full sequence-by-vocabulary logits allocation. Do not request retained logits, scores, attentions or hidden states for ordinary experiment accounting. Token IDs, termination and timings are sufficient. Measure load footprint, peak allocated/reserved memory, actual device map and at least 1.5 GiB free headroom on the accepted worst request. [Generation source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/utils.py#L2528).

## Rendering, termination and call independence

The checked tokenizer resolves to `Qwen2Tokenizer`. `enable_thinking=False` adds the closed `<think>\n\n</think>\n\n` block to the **request's generation prefix**. Keep that exact template output in saved requests and equality checks. It is not generated response text. A minimal user fixture encoded to 15 tokens, versus 13 with thinking enabled. [Pinned template](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/chat_template.jinja).

The same template rewrites assistant-role content containing `</think>`: the probe's archived invalid reply `<think>should stay archived</think>{"candidate":[],"send":[]}` became just the JSON object when rendered as an earlier assistant turn. **Render permitted derived history as explicitly labeled data in the call's user content**, rather than asking the model's conversational template to reconstruct raw prior assistant turns. Keep the offline raw archive untouched. Before freeze, verify exact preservation of special-looking strings inside history, JSON escaping, phase labels and receipt/notice fields. This recommendation prevents template transformation; it is not a new history deletion rule.

There is a concrete termination mismatch: the checked text configuration's EOS is **248044** (`<|endoftext|>`), while tokenizer EOS is **248046** (`<|im_end|>`) and tokenizer PAD is **248044**. Neither checkpoint exposes a separate `generation_config.json`. `GenerationConfig.from_model_config(text_config)` reproduced EOS 248044 locally. Direct `generate` has no tokenizer from which to discover the chat terminator. Explicitly freeze audited EOS/PAD settings covering the actual chat termination; test the accepted set during smoke. Do not add JSON-closing-brace stopping, response repair or alternate decoding strategies. [9B configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json), [tokenizer configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/tokenizer_config.json), [generation configuration derivation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/configuration_utils.py#L1255).

The decode probe turned `{"candidate":[]}<|im_start|>` into `{"candidate":[]}` under `skip_special_tokens=True`. Blanket removal could make an invalid reply pass strict JSON. Archive generated IDs and exact decoded text; remove only audited terminal transport framing for the parser, preserving unexpected/internal markers. Decode only the newly generated suffix, with text-space cleanup disabled. A complete object at the 384-token cap remains valid even when the stop reason is length; inspect completeness instead of declaring every length stop invalid (§3.2).

Use explicit sampling (`do_sample=True`, one return sequence) and the specification's settings, including **no presence penalty**. Make no framework default or model-card server example an extra control. Count tokens with the accepted tokenizer after applying the exact chat template: `len(input_ids) + 384 <= 8192`, with truncation disabled. In Transformers 5.12.0, the probe used `return_dict=True` and counted `input_ids`; counting the dictionary itself would have incorrectly reported two tokens.

Each worker is serial and owns one replica. The inspected sampling loop uses `torch.multinomial` without a per-call `generator` argument. Reset the saved call seed immediately before each generation in that worker, covering CPU/CUDA RNGs; do not pass an assumed supported `generator=` keyword. Runtime libraries can consume RNG between calls, so seed once per episode is insufficient. [Sampling and seed source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/utils.py#L2839), [Transformers set_seed](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/trainer_utils.py#L180).

Root additionally inspected PyTorch 2.11.0's `manual_seed` implementation: it invokes `cuda.manual_seed_all` and resets the process-wide CPU generator. Two concurrently sampling worker threads in one process could therefore disturb one another's saved call seeds. Prefer one process per GPU with that worker's device visibility fixed before CUDA initialization; verify scheduling/resume independence in the accepted environment. This is an RNG isolation choice, not distributed-serving infrastructure. [PyTorch manual_seed](https://docs.pytorch.org/docs/2.11/generated/torch.manual_seed.html).

Use a fresh dynamic KV/recurrent cache inside each generation and discard it afterward. Supported generation creates that cache when none is supplied; recurrent state lives in it. Reusing weights is safe only with verified fresh call state. Avoid persistent/static/offloaded cache, continuous batching or backend conversation handles. Matched seeds do not guarantee equality across different prompts, devices or package versions; exact mixed/Q first-round replay remains mandatory. [Cache initialization source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/utils.py#L1943), [PyTorch reproducibility limitations](https://docs.pytorch.org/docs/2.11/notes/randomness.html).

## Tokenizer-only capacity probe

Fixtures used compact JSON, short value-independent IDs `r0…`, reference fields `record_id`/`version`, numeric extremes within the task input/output ranges, and no prose. These are illustrative field spellings, not a newly frozen protocol schema. Results were identical across the two checked tokenizer artifacts.

| Target-size shape | Candidate + empty send | Candidate + own shard to one recipient |
|---|---:|---:|
| Top-K: ten integers | 36 | 124 |
| Prefix: eight integers | 38 | 126 |
| Difference: 31 integers | 99 | 187 |
| Sort: eight integers | 30 | 118 |
| BFS: twelve node keys | 56 | 104 |
| Full-information Prefix: 32 integers, empty send required | 134 | Not applicable |
| Full-information Sort: 32 integers, empty send required | 102 | Not applicable |

Fallback `m=6` one-shard figures were 104/98/143/92 for Top-K/Prefix/Difference/Sort; eight-node BFS with three owned edges was 76. This supports the prescribed witness's **one recipient per round** strategy. It does not prove scripted truth, source acquisition, update recovery, Q timing, all IDs/versions or arbitrary legal response payloads. Simultaneous maximum references plus maximum prose need not fit 384 (§3.2).

Before recovery round four, B can hold seven prior call slots. The raw bound `7 × (384 own reply + 3 × 128 incoming prose + 32 feedback) = 5,600` tokens deliberately allows maximum incoming prose directed to the focal peer from each sender. Labels and serialization add overhead. A synthetic fixture with those payloads, 32 rendered current sources, the public manifest and a short revision/receipt notice encoded to **7,175 input tokens**, or **7,559 including output reserve**. Its 633 remaining tokens exclude the real instructions/hints, full source-delivery metadata, separately rendered latest candidate, final history/reference representations and potentially longer IDs/field shapes. It is **not a proof of the permitted worst context**. Do not certify the channel from these measurements or silently truncate it.

The final renderer can remain simple and compact, but all permitted extremes must fit with the retained-history treatment preserved. Numeric candidates accept integer mistakes, not only bounded correct answers; generated invalid fragments and unusual escaping also need stress fixtures. Q delay must preserve the complete held/released prose without extra duplication. If the final checks fail, use only the specification's defined size fallback where applicable, or document a pre-main protocol revision; no hidden shortening of B history.

The following CPU-only probe reproduces the target output figures and constructed context figure. It downloads four metadata files into a temporary directory, performs no generation and constructs no experiment runner or task prompt:

```python
import json, pathlib, tempfile, urllib.request
from transformers import AutoTokenizer

revision = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
folder = pathlib.Path(tempfile.mkdtemp(prefix="recovery-capacity-"))
for name in ["config.json", "tokenizer.json", "tokenizer_config.json",
             "chat_template.jinja"]:
    urllib.request.urlretrieve(
        f"https://huggingface.co/Qwen/Qwen3.5-9B/resolve/{revision}/{name}",
        folder / name)
t = AutoTokenizer.from_pretrained(folder, local_files_only=True)
pack = lambda x: json.dumps(x, separators=(",", ":"))
count = lambda s: len(t.encode(s, add_special_tokens=False))
cases = {"Top-K": [99]*10, "Prefix": [288]*8,
         "Difference": [-30]*31, "Sort": [99]*8,
         "BFS": {str(i): -1 for i in range(12)},
         "Prefix control": [288]*32, "Sort control": [99]*32}
for name, candidate in cases.items():
    refs = [{"record_id": f"r{i}", "version": 1}
            for i in range(4 if name == "BFS" else 8)]
    empty = {"candidate": candidate, "send": []}
    forward = {"candidate": candidate,
               "send": [{"to": 1, "source_refs": refs}]}
    print(name, count(pack(empty)),
          None if name.endswith("control") else count(pack(forward)))
own, prose, feedback = " x"*384, " x"*128, " x"*32
assert [count(x) for x in [own, prose, feedback]] == [384, 128, 32]
sources = "\n".join(pack({"record_id": f"r{i}", "owner": i//8,
    "version": 2, "position": i, "value": 99}) for i in range(32))
manifest = "\n".join(f"r{i} owner={i//8} position={i}" for i in range(32))
notice = ("Revision: r31 owner=3 version=2. Version 1 is invalid. "
          "Historical before-value receipt: r31 version=1 value=98.")
history = []
for slot in range(7):
    phase = "prefix" if slot < 4 else "recovery"
    rnd = (slot if slot < 4 else slot-4)+1
    label = f"{phase} round={rnd}"
    history.append(f"{label} own reply:"+own)
    history += [f"{label} received from={sender}:"+prose
                for sender in [1, 2, 3]]
    history.append(f"{label} schema feedback:"+feedback)
fixture = ("Current sources:\n"+sources+"\nPublic manifest:\n"+manifest+
    "\nPersistent notice:\n"+notice+"\nDerived history:\n"+"\n".join(history))
encoded = t.apply_chat_template([{"role": "user", "content": fixture}],
    tokenize=True, add_generation_prompt=True, enable_thinking=False,
    return_dict=True)["input_ids"]
print("input", len(encoded), "with reserve", len(encoded)+384,
      "remaining", 8192-len(encoded)-384)
```

Run as a temporary Python file using the inspected environment; expected last line: `input 7175 with reserve 7559 remaining 633`. The complete production attainability witness is deliberately deferred to implementation, where it can use the real schema/rendering and branch rules.

## Resource and validation conclusions

The schedule is already specified, not an architecture optimization opportunity: **16,152 / 11,504** new main generation slots, **17,656 / 12,560** logical slots, and at most **1,138** distinct development pilot/smoke slots. Replayed first rounds require exact persisted parent replies; they do not become free hypothetical-policy work. Retries, failed configurations, allocations while idle and setup must remain visible (§§7.3, 8.3–8.4, 9).

Under the specification's illustrative `12 + 1.25 × calls × g/3600` forecast, the 100-hour ceiling corresponds to at most **15.69 allocated seconds per new generation** for 60 worlds, or **22.03** for 40. This algebra identifies the required measurement; it is not a timing forecast. FP32 recurrent fallback performance, the longest retained contexts, output lengths, worker imbalance and provider allocation rules can defeat a throughput estimate from a few short calls. Two devices reduce elapsed time only when both are productive; they do not halve aggregate device-hours.

Resolved for planning: native Transformers text loading, explicit FP16/NF4 configuration, fresh per-call state and seed ownership, exact template/request accounting, strict decoding, and the need for final rendered-capacity checks. Deliberately unresolved: the complete passing CUDA/package lock, selected attention/recurrent paths, actual peak memory/headroom, adequate 120-second attempt timeout, capability admission, accepted 9B/4B model, size and 60/40 schedule. Resolve those only through the specification's bounded smoke/pilot and measured allocation forecast after implementation; no new empirical research matrix is needed.

Before expensive execution, the small gates that matter are: (a) real-schema capacity and a complete locally informed witness; (b) text-language load diagnostics plus long-request memory/finite-output smoke; (c) raw special-token/termination and independent-call/seed fixtures; (d) the specified capability/validity thresholds; and (e) a complete-schedule cost forecast using the slower worker and the full reserve. Further metadata research is unlikely to replace any of these measurements.
