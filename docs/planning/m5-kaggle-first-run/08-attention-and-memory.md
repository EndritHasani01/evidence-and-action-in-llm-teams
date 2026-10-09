# Offline attention integration and memory review

Planned 9 October 2026 after [actual run 6](../../validation/m5-t4-compatibility-run-6.md). This implements the next offline part of K10 under [M5-T02](../../todos/M5/M5-T02-hardware-smoke-and-host-validation.md), [AGENTS.md](../../../AGENTS.md), specification §§8–9 and the [model-feasibility contract](04-model-feasibility-and-smoke.md). Existing GPU authorization persists. No GPU execution, pretrained weight download, pilot/main execution or freeze belongs to this step. Keep the current user edit and every earlier result intact; make separate planning, implementation and evidence commits.

## Problem and proposed change

**Completion, 9 October:** implementation `8528105` passes [127 focused/native source and 15 installed checks](../../validation/m5-attention-memory.md), including actual small CPU hybrid Qwen chunk/cache/logit continuity and selected-wheel source verification. The read-only audit covers both models and both mathematical sizes. The offline deliverable is complete; actual T4 acceptance of the new layout and R7 remain open. Original notebook/payload/results bytes and default settings are preserved. No new GPU run or model-smoke notebook is requested by this step.

Run 6 observes native GQA math dispatch on T4 and efficient dispatch after materializing repeated K/V. Copying that operation into the model would add a conditional 4-GiB temporary per active full-attention layer at the cap. An adapter must preserve full causal attention, head mapping, cache ownership, masks and scaling while addressing that demonstrated allocation problem.

Implement one **opt-in** candidate backend, `recovery_t4_sdpa`, with the existing Transformers/PyTorch versions. Preserve the current `sdpa` candidate and its exact settings as the default. Record the alternative backend and its fixed 256-token maintained prefill chunk size in existing candidate settings/load evidence; do not create new identities, stores or orchestration. This is a proposed runtime configuration, not an accepted or frozen model configuration.

The attention computation is independent for each head. With one episode, 16 query heads and four KV heads, reinterpret Q as `[4 KV groups, 4 query heads, L, 256]`. Interpret K/V as `[4 KV groups, 1 head, S, 256]` and broadcast the head dimension with `expand`, retaining the original storage. Restore the original query-head order and the interface's `[1, L, 16, 256]` output. The kernel's batch axis now indexes KV groups, not four episodes; the scientific batch remains one. Q/output reshaping may allocate; the claim concerns K/V aliases only.

Use only public `scaled_dot_product_attention` and `sdpa_kernel(EFFICIENT_ATTENTION)` on CUDA. No math fallback, custom CUDA kernel, monkey patch or replacement of the built-in `sdpa` entry is allowed. On CPU, use the math backend solely for deterministic numerical tests. Refuse unsupported shapes, masks, dtypes, training/dropout and missing causal masks before dispatch. Actual CUDA acceptance is still required.

Register the new attention function **and the maintained `sdpa_mask` formatter** through Transformers' public interfaces. Retain native causal/padding masks. Square unmasked prefill uses the causal flag; single-query decode attends to the complete cache; multi-query continuation requires the native offset mask. Support the native head-shared 4D mask only. Convert boolean masks to additive masks before broadcast, and align their row storage before expanding, so mask preprocessing does not multiply a long mask across heads. Retain literal mask values and refuse unsupported formats rather than dropping them.

The maintained generation path supports `prefill_chunk_size`; using 256 bounds prompt-layer activations and offset-mask query length without truncating input or generating additional opportunities. Use one fresh call-owned hybrid cache across those forwards and dispose it after the call. Check the maintained recurrent continuation, mask positions and final logits against an unchunked CPU forward using a small random hybrid Qwen model. This is numerical integration evidence without pretrained weights, study generations or GPU calls; finite sampling, physical isolation, timing and headroom remain T02 requirements.

## Source evidence and remaining uncertainty

- [Transformers 5.12 attention interface](https://huggingface.co/docs/transformers/v5.12.0/en/attention_interface) documents registering attention and a matching mask formatter. Without that formatter, causal/padding masks can be skipped.
- [Torch 2.11 attention entry point](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/transformers/cuda/attention.cu) propagates head strides to the efficient kernel; its alignment checks accept zero strides. [Maintained efficient kernel](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/transformers/cuda/mem_eff_attention/kernel_forward.h) includes a zero-head-stride decode branch. These sources motivate the layout; they do not establish actual T4 execution of this new layout.
- [Torch SDPA](https://docs.pytorch.org/docs/2.11/generated/torch.nn.functional.scaled_dot_product_attention.html) defines masks, scaling, non-square causal alignment and backend selection. Use the native continuation mask rather than guessing an offset from the square causal flag.
- [Transformers generation source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/utils.py) supplies maintained chunked prefill and keeps only the final needed logits. Verify installed candidate source against the existing exact selected wheel before relying on it; no package upgrade is proposed.
- The [existing capacity proof](../../implementation-research/m2-t06-capacity-proof.md) pays 48/45 tokens per own/prose token and covers all permitted histories. Sampled re-encoding ratios or the largest 33k fixture cannot replace that complete proof. Do not tighten it by assumption or alter retained bytes.

## Memory audit

Add one read-only, standard-library command, `scripts/m5_model_feasibility.py`, deriving its report from the retained canonical config bytes, existing capacity archive and actual run-6 native/free memory. Verify the original archive/config identities and reject inconsistent geometry or input evidence. It must not import Torch, construct a model or modify any prior result.

For both models and both mathematical sizes, report:

- Complete proved resident-token upper bound (input plus unchanged 384 reserve), largest constructed fixture and their distinct meanings.
- FP16 embedding/head, ideally packed four-bit MLP and full-attention KV conditional subtotal; omitted weights/scales/activations/workspaces remain explicit. Count tied 4B heads once.
- The separate materialized-repeat term versus the proposed alias path, cache-growth copy and bounded chunk Q/output/mask terms. These are conditional implementation calculations, not measured peaks or a complete allocator upper bound.
- Native device total/free memory, required 1.5-GiB headroom and whether even the partial subtotal exceeds that allowance. A subtotal below the allowance is not acceptance; an upper-bound calculation above it is not empirical model failure or proof the bound is attained.

Keep `full_envelope_memory_acceptance` unknown unless an independently supported complete memory argument exists. R7 can remain a documented admission blocker after a successful audit. Do not automatically select 4B, lower the context/output cap, shorten histories, pad arbitrary tokens or promise that the next notebook will pass. Model assets and bounded smoke still depend on actual resource admission and sufficient envelope evidence.

## Implementation and checks

| Checkpoint | Files / verification |
|---|---|
| Planning | This file plus the living plan's K10 decision; commit before behavioral changes. |
| Attention | One lazy-import module `recovery/t4_attention.py`; opt-in candidate wiring in `recovery/inference.py`; preserve default settings and fresh cache/seed/attempt semantics. |
| Deterministic tests | Independent per-head reference, causal/padding/additive/offset masks, decode, head ordering, noncontiguous inputs, K/V storage aliases and input immutability; refuse missing masks, unsupported geometry/training/dtypes. Verify CUDA permits only efficient dispatch using a controlled selector, without claiming a GPU result. |
| Native CPU integration | Both public registry entries, unchanged built-in SDPA, small random full/linear-attention Qwen forward/cache continuity, chunked versus full final logits and state, fresh-call ownership. Verify actual candidate package source; retain raw output. |
| Memory command | Wrong/corrupt evidence rejection, model ties, all four model/size cases, native-memory arithmetic, unknown states, original-byte preservation and refusal to overwrite reports. No guessed allocation duration or fallback selection. |
| Regression / handoff | Existing inference/worker/attempt checks and native metadata/capacity checks affected by candidate wiring. Local links, task states, archive/user-edit preservation and logical commits. No broad analysis rerun for unchanged science. |

The eventual GPU model environment must validate the new zero-stride layout, aligned masks, recurrent/chunk behavior, actual NF4 loading, complete-envelope headroom and bounded time. The old `m5-kaggle-source-v2` payload remains preserved and cannot deliver newly changed adapter source; a future model packet must bind to the new committed source. This step does not ask the user to repeat CPU preparation or run 6. Its deliverable is verified offline code and an honest admission report, with T02 and later gates unchanged until measured criteria pass.
