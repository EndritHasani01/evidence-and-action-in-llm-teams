# Model feasibility, context coverage and bounded smoke

**Status: static planning; physical model acceptance unexecuted.** The source-input failure supplies no reason to alter the model, mathematical design, output cap or protocol. This document identifies the separate issues that must be resolved before a successful preparation run can become M5-T02 evidence.

[Actual run 5](../../validation/m5-kaggle-full-preparation-run-5.md) completes the unchanged candidate's CPU preparation with all 97 checks passed and zero skips. [Actual run 6](../../validation/m5-t4-compatibility-run-6.md) accepts R8's small-operator portion: 14 attention cases and four NF4 matmuls on both T4s. No repeat CPU or tiny-GPU preflight is requested. Its standalone matching-Torch/library environment does not accept the full model lock; later candidate GPU checks must repeat affected behavior. Supported model attention integration and R7 complete-envelope coverage remain unresolved; the physical model-smoke notebook remains unprepared. Next perform those reviews offline. A later GPU session needs verified environment staging and its own host checks, with all assigned time charged under the existing budgets.

## Scientific invariants

Retain Qwen3.5-9B first and the specified 4B hardware/runtime fallback, one full replica per physical T4, serial batch-one calls, NF4/double quantization, FP16 compute and supported sensitive FP32 paths. No CPU/disk offload, cross-device model splitting, custom kernels, alternative quantizers or serving stack are part of the proposed repair.

Retain non-thinking rendering, temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0, no presence penalty, exact template/EOS/PAD review, the 384-token output reserve and the 262,144 total context cap. Do not truncate histories, sanitize replies, repair JSON, impose schema constraints, stop at braces, or reuse completed malformed answers as new draws. Completed failures remain observed failures; unexecuted probes remain unknown.

Use the existing five development worlds, prescribed local-view witness, scheduled seeds, runner/worker SQLite stores, process/attempt evidence and exact parent replay. Smoke calls remain separate from pilot call IDs. Equal seeds alone never imply reply equivalence or permission to replay an independence probe.

## Disk fit is not memory fit

The [platform research](02-platform-research-and-decisions.md) gives exact original selected file sizes: 17.9924 GiB for 9B and 8.6918 GiB for 4B. They must be staged outside the run's 15.5397-GiB remaining working pool. Loading those shards into NF4 does not reduce their on-disk size.

For VRAM, `nvidia-smi` reports 15 GiB per T4. Actual run 6's Torch native properties report **14.56219482421875 GiB** usable total per device (15,636,037,632 bytes), and post-probe free memory is **14.39727783203125 GiB**. Retain both inventory/native measurements without inferring a cause for their difference. Each replica needs its own weights, KV/recurrent state, activations, workspaces, CUDA context and the required 1.5-GiB free headroom; two devices do not form a combined model pool. Tiny peaks are not model peaks.

### Static KV arithmetic

Both pinned text configs have eight full-attention layers, four key/value heads and head dimension 256. For batch one and FP16 K/V, ignoring other allocations:

`KV_bytes(S) = 2 × 8 × 4 × 256 × 2 × S = 32,768 × S`.

At 262,144 resident tokens, KV alone is 8 GiB. At 33,106 input tokens plus the full 384 reserve, it is about 1.022 GiB. The 4B config has the same full-attention KV geometry; choosing 4B does not halve this cache term. These are static estimates from the pinned configuration, not measured allocations or a claim that a particular native cache representation exactly equals the estimate.

### A useful conditional lower bound for 9B

The maintained MLP uses gate/up/down projections, with an MLP in each decoder layer. Default bitsandbytes conversion retains the output embedding module rather than quantizing it; actual loading diagnostics must verify this and the expected tied/untied heads. [Pinned Qwen implementation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py), [pinned quantizer base](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/quantizers/base.py).

Assume FP16 embeddings/output heads and ideally packed four-bit MLP weights. Exclude attention/recurrent weights, quantization scales/padding, activations, workspaces, contexts and temporary allocation:

| Term | 9B, untied head | 4B, tied head |
|---|---:|---:|
| FP16 input embedding plus distinct output head if untied | 3.7890625 GiB | 1.1840820 GiB |
| MLP packed weight payload: `3 × hidden × intermediate × 32 / 2` bytes | 2.2500000 GiB | 1.0546875 GiB |
| FP16 full-attention KV at 262,144 tokens | 8.0000000 GiB | 8.0000000 GiB |
| Subtotal, excluding all other memory | 14.0390625 GiB | 10.2387695 GiB |

The earlier 15-GiB inventory calculation leaves 13.5 GiB after headroom; 9B's conditional subtotal reaches that amount at 244,480 tokens, before omitted allocations. Actual run 6's **native total leaves only 13.06219482421875 GiB** after the required headroom, before existing occupancy. Use the relevant native/free measurements for actual admission. Sensitive FP32 parameters and CUDA overhead are additional; neither inventory arithmetic nor a tiny probe establishes full-model feasibility.

This does **not** prove this run's 9B model failed, that every legal view reaches 244k tokens, or that the conservative bound is attainable. No weights were loaded. Actual shapes/dtypes, ties and native cache paths must match the assumptions. It does show why an assertion that “262k fits because 9B is four-bit” is unsupported. 4B's lower subtotal is also not acceptance evidence.

### Repeated-K/V memory must remain explicit

Run 6 observes efficient dispatch after explicit repetition from four KV heads to 16 heads. A **fully materialized** repeated K/V temporary for one active full-attention layer is `2 × 16 × 256 × 2 × S` bytes, **4 GiB at 262,144 resident tokens**, in addition to the original eight-layer KV cache. Under that implementation and the table's assumptions, conditional 9B/4B subtotals become **18.0390625 / 14.23876953125 GiB**, before omitted memory, versus the native total minus headroom of **13.06219482421875 GiB**. A tiny efficient kernel does not remove this term.

This is a conditional implementation-memory calculation, not empirical failure or proof that a legal view reaches the cap. It rules out using the tiny repeated-K/V operation alone as the full-envelope memory argument. Review the maintained/public model route's actual cache, causal/mask and temporary-allocation behavior together with R7. No adapter, cap reduction or fallback is selected here.

## The complete-envelope evidence gap

The retained `capacity_report.json.gz` distinguishes two quantities:

| Quantity | Retained evidence | Interpretation |
|---|---|---|
| Largest concrete rendered fixture | 33,106 input / 33,490 with reserve, target Difference. | A concrete legal envelope construction measured by the native tokenizer. |
| Concrete target Prefix Thai-reencoding fixture | 33,038 input / 33,422 with reserve. | A useful long smoke request, not a measurement near 261k. |
| Maximum conservative target bound | 261,388 including reserve. | Complete token-capacity upper bound across the admitted protocol envelope. |
| Maximum conservative size-fallback bound | 259,868 including reserve. | Only 1,520 tokens lower; dominant retained-text allowances remain. |

A memory test on a 33k request cannot establish that all contexts allowed by a 261k bound fit. The existing smoke packet's “maximal retained view” wording needs to distinguish a constructed stress case from proven coverage of the full admitted envelope. Do not pad it with arbitrary tokens and call it a permitted recovery request.

R7 must produce one of three reviewed outcomes before full headroom acceptance:

1. A tighter, sound complete live-input bound from the existing tokenizer/renderer/capacity proof, with stress requests and conservative memory/activation coverage sufficient for that bound.
2. A valid construction and measured/analytical memory argument covering the complete required envelope, within the unchanged cap and supported execution path.
3. A retained feasibility blocker: the required envelope cannot be supported by the candidate within the resource/implementation constraints.

Do not substitute likely natural output length, omit malformed historical text, strip internal markers, lower text allowances or rely on the absence of a long output in 24 samples. If tightening the bound changes renderer/normalization/protocol semantics, it is a scientific change and reopens affected gates. Tightening a proof without changing bytes is a narrower capacity-analysis change, still requiring independent verification.

The uniform mathematical size fallback reduces the retained bound by only about 0.046 GiB of FP16 KV under this arithmetic. It is the prescribed arithmetic/context remedy, not a guaranteed solution to retained-prose memory. Do not apply it automatically for dataset storage or to conceal a failing worst-context gate.

## SDPA dispatch is a separate runtime risk

The pinned Qwen configs use 16 query heads and four KV heads. Transformers 5.12.0 enables native GQA when its SDPA helper receives no attention mask on the reviewed Torch version. Torch 2.11's CUDA selector requires SM80+ for Flash/cuDNN attention, and its dense memory-efficient selector does not support unequal query/KV head counts. T4 is SM75. Together these reviewed sources predict math fallback for that mask-free GQA case; an actual model call's mask and dispatch were not observed. [Transformers SDPA helper](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/integrations/sdpa_attention.py), [Torch CUDA selector](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/transformers/cuda/sdp_utils.cpp), [Torch dense-head checks](https://github.com/pytorch/pytorch/blob/v2.11.0/aten/src/ATen/native/transformers/sdp_utils_cpp.h).

A dense attention-score tensor for 16 heads at 33,106 tokens contains `16 × S²` elements: about 32.66 GiB at FP16 or 65.33 GiB at FP32, before weights or other intermediates. The reviewed Torch math documentation describes FP32 intermediates for FP16 inputs. A retained 33k fixture can therefore be infeasible even though its KV estimate is only about one GiB. This is a conditional allocation analysis, not a measured OOM. [Pinned SDPA implementation/documentation](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/functional.py).

Both model candidates share this head geometry. Switching to 4B or reducing mathematical size does not automatically solve this dispatch problem. Transformers 5.16.1's inspected helper also permits GQA for mask-free equal K/V dimensions <=256, so the observed newer Kaggle version is not demonstrated to fix it. [5.16.1 SDPA helper](https://github.com/huggingface/transformers/blob/v5.16.1/src/transformers/integrations/sdpa_attention.py).

The [actual run-6 review](../../validation/m5-t4-compatibility-run-6.md) now observes the predicted native-GQA math dispatch for tiny causal prefill and single-query decode. Repeated-K/V automatic, forced-efficient and masked cases use an efficient SM75 kernel and match CPU FP32 references on both T4s. NF4/double-quantized synthetic matmuls also pass. No actual Qwen call or full candidate import was made; actual model mask/recurrent/cache behavior stays unobserved. No repeated tiny probe is requested.

The original cheap diagnostic sequence below has completed its standalone small-operator portion. Next review the supported model integration and complete-envelope memory argument offline, then renew affected GPU behavior in the eventual full candidate:

1. On the actual candidate T4, use tiny synthetic Q/K/V tensors with 16/4/4 heads, dimension 256, FP16, causal prefill and no mask. Record public backend-eligibility reasons and actual dispatch; do not allocate a 33k dense score matrix to discover this known risk.
2. Compare the maintained explicit K/V-expansion path on the same small tensors. Verify finite outputs and toleranced mathematical equivalence, plus the actual efficient-backend eligibility/dispatch. Also test decode shape and relevant mask behavior.
3. If mask-free model dispatch falls back to math, identify a maintained compatible version or reviewed public attention-interface route that preserves causal/mask semantics and explicitly repeats K/V without a dense S-by-S mask. No global monkey patch, custom CUDA kernel or silent eager fallback.
4. Record any resulting attention/backend change explicitly in candidate settings and load evidence, renew exact request/native/capacity/isolation tests, and rerun the bounded model gate before capability work. A small public-API Python attention adapter is an additional backend change requiring review, not an already selected fix. [Maintained attention interface](https://huggingface.co/docs/transformers/v5.12.0/en/attention_interface).

If no allowed supported path works within resources, retain a runtime feasibility blocker. R7's complete-envelope memory question remains necessary even if efficient dispatch succeeds: avoiding quadratic scores does not remove weights, KV, recurrent state or activation costs.

## Narrow possible inference changes

The current [ModelFactory](../../../recovery/inference.py) loads a Hub model identifier at the immutable revision. The [TokenizerFactory](../../../recovery/inference.py) already supports local tokenizer metadata. Compare these two simple weight-staging routes:

| Route | Change / evidence | Recommendation |
|---|---|---|
| Existing pinned Hub cache on verified scratch | Stage one complete revision into the explicit Hub cache; run offline and verify every selected file/hash and actual resolved snapshot. | Prefer when the cache survives the transition into the admitted session without copying files into working output. No backend change necessary. |
| Verified local snapshot/private input | Add an optional local directory to ModelFactory and pass the same directory to its tokenizer; use `local_files_only=True`. Verify revision/file manifest before construction and retain provenance in existing load evidence. | Use if it removes a demonstrated cache/persistence or duplicate-copy problem. Keep candidate settings/scientific identities unchanged. |

Do not add a model-conversion wrapper, alternate loader stack, global registry or model-specific inference service. A local path must not bypass the current maintained text-class, loading-info, language-weight, precision, NF4, full-device and tie checks. Test local/cache request equality and reject mixed/stale revisions before any generation.

The pinned generation source merges custom logits processors before sampling temperature/top-k/top-p warpers. Thus the existing finite-score hook is positioned before those filters in this reviewed version; no demonstrated hook-order fix is needed. Preserve a regression around that maintained ordering if the Transformers candidate changes. [Pinned generation implementation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/generation/utils.py).

Review memory instrumentation before acceptance. The current backend records end-of-call free memory while cache/output references are still live, plus peak Torch allocated/reserved bytes. End-of-call free memory alone need not equal minimum free memory during prefill. Retain baseline/non-model occupancy, peak allocation/reservation and actual device/process traces; use a conservative headroom argument including workspace/context allocations. Polling provides observed samples, not an exact guarantee between samples. A successful short output cannot erase a prefill peak. Keep any added evidence in existing process/attempt JSON, not a second telemetry database.

## Exact smoke preparation

Materialize all 24 slots in the [existing matrix](../../validation/m5-inference-preparation.md#concrete-development-manifest-and-smoke-requests) before model loading. Proposed orchestration is one importable, main-guarded `scripts/m5_smoke.py`, using the existing `ProcessProvider`, `WorkerStore`, tokenizer, request structures, validators and backup API. It is conditional later work, not part of the immediate preparation repair.

For each slot, retain development origin, permitted view, exact rendered/template text, input IDs/mask, full candidate settings, saved seed, smoke-local call/physical identity, intended device/restart/probe, token counts and request-construction provenance. Re-render/re-tokenize independently and reject drift. Do not write smoke outputs under pilot IDs or fabricate model-generated witness replies.

| Existing slots | Required coverage |
|---|---|
| 01–05 | First peer-zero prefix request for each of the five task families; finite scores and native output shapes. |
| 06–08 | Before Prefix/Sort and after BFS full-information controls; complete-world contracts, empty sends and exact saved seeds. |
| 09–13 | Round-four local-view witness for all families; acquired evidence and literally validated forwarding. |
| 14–17 | Four corrected-C Prefix continuation starts, from the prescribed offline witness prefix and actual saved edit. |
| 18–19 | Retained Prefix B and Sort Q_B stress views, with measured lengths and an explicit relationship to R7's complete-envelope argument. |
| 20–23 | A/B/A/A-after-confirmed-restart; identical A request/settings/seed, separate physical diagnostic calls, observed cache/RNG order behavior. |
| 24 | Labeled controlled hang/deadline probe; timeout persisted before bounded termination and confirmed process exit. |

No additional warmup, device-rotation sample or debugging generation may be added outside the ceiling. A retry consumes a physical attempt and displaces a later opportunity. Any required rotation probe replaces a planned slot with a reviewed coverage decision. Partial coverage remains unexecuted/unknown; it cannot pass a missing acceptance requirement.

## Allocation admission and stopping

The screen allows at most 24 physical attempts and 1,800 aggregate allocated GPU-seconds, including loading, assigned idle time, restarts and stopping. Two assigned T4s imply at most 900 wall seconds. Reserve the existing 120 wall seconds for backup/provider release; this leaves at most 780 seconds for work from actual assignment, even before earlier preparation spending. Across 24 attempts that is only 32.5 seconds each on average before other overhead. This is a feasibility constraint, not a promised completion time.

Cold installation, host CPU/crash checks, weight transfer and model restart can consume the allowance before useful model coverage. Stage assets/resolution on CPU; rerun the required affected checks on the actual candidate GPU host. Do not waive those checks or retroactively exclude assigned-GPU CPU time. Keep earlier preparation allocations and unknown interval bounds in the shared accounting.

Retain the initial 120-second attempt bound, including first loading/IPC, and one-second terminate/kill graces. Before starting a call, reserve all permitted infrastructure attempts, termination and safe stop time. A retry-bounded call can need 244 wall seconds; an entire four-peer round can need 976 and does not fit the short screen's work allowance. Admit smoke requests individually without changing scientific round barriers or effects.

`ProcessProvider.obtain` currently loops into an infrastructure retry after an interruption, while `WorkerStore.begin_attempt` enforces the one-retry rule. It does not itself enforce a smoke-wide attempt count/deadline. First prove that caller-side worst-case admission can protect both limits. If it cannot safely account for the final permitted attempt, add only a narrow optional admission check before `begin_attempt`, including retries. A budget refusal must create no new attempt, fabricate no timeout/invalid reply, and not be caught as a provider defect. Interrupted work remains honestly unresolved until permitted resume; completed outcomes remain final. Derive counts from authoritative attempt rows, not a separate mutable counter.

On any language-load defect, unexplained precision/device placement, nonfinite output, unresolved process termination, failed complete-envelope headroom or insufficient remaining resources: stop admission, retain raw/process evidence, back up safely and confirm provider release. Do not resample a wrong or malformed completed answer. A model timeout is final; only the existing confirmed infrastructure-interruption rule admits a retry.

## What passing T02 would require

The [offline next step](../../validation/m5-attention-memory.md) now verifies an opt-in public SDPA adapter and maintained 256-token hybrid prefill on CPU. Its read-only complete-bound report uses target/fallback resident bounds 261,388/259,868, giving conditional 9B subtotals 14.015991/13.969604 GiB and 4B subtotals 10.215698/10.169312 GiB against run 6's native-total-minus-headroom allowance of 13.062195 GiB. K/V view storage avoids the adapter's materialized-repeat allocation; actual kernel workspace remains unmeasured. Cache growth, mask conversion and omitted weights/activations/workspaces still matter. These comparisons do not establish fit, empirical failure, legal attainability of the upper bound or fallback selection. R7 remains unresolved under the existing three-outcome contract. The new layout's T4 acceptance and complete candidate/model smoke remain open.

Acceptance needs traceable actual language-weight/tie inventory, NF4/precision/path/device evidence, finite raw outputs and generated IDs, all required output/forwarding/continuation coverage, fresh KV/recurrent ownership and seeded serial behavior, complete-envelope >=1.5-GiB headroom, adequate observed attempt bounds, candidate-host checkpoint/crash/backup behavior, verified off-host recovery, and reconciled allocation/attempt ceilings. Review both failure and success logs. Static arithmetic or metadata cannot pass it.

Keep the later gates unchanged:

| Gate | Required evidence |
|---|---|
| T03 capability | Exactly 80 prefix plus 10 before/after controls first; >=9/10 controls, at least one per family, >=3 jointly correct final prefixes, >=14/20 final prefix peers. |
| T04 complete pilot | Exactly 1,114 distinct / 1,178 logical slots including those first 90; >=98% protocol validity without counting replays/retries as extra valid slots; phase/prompt/slower-device timing and no unresolved isolation defects. |
| T05 freeze/admission | Whole 60/40 schedules, 12-hour reserve and 25% main-cost margin within the initial 100 aggregate GPU-hours, complete storage/export plan, immutable accepted inputs/lock/settings and independent resume audits. |

Failed candidates share the existing 8/2/2-hour development/setup/interruption reserves and cannot be pooled into an accepted configuration. Prefer passing 9B/40 over changing models merely to obtain 60 worlds. If supported candidates cannot pass the envelope/runtime/resource gates, retain terminal feasibility evidence and use the limited-evidence reporting path. A scientific cap, architecture, design or resource change requires a concrete separate decision with affected gates identified; this plan makes none.
