# Offline attention integration and memory audit

Implemented 9 October 2026 at `8528105`, after the separate planning checkpoint `2182014`. The [next-step plan](../planning/m5-kaggle-first-run/08-attention-and-memory.md) is implemented and locally verified: **127 focused/native source checks and 15 installed attention checks pass with zero skips**. This follows the accepted [run-6 standalone GPU evidence](m5-t4-compatibility-run-6.md). It does not complete [M5-T02](../todos/M5/M5-T02-hardware-smoke-and-host-validation.md). Actual T4 execution of this new layout, complete-envelope memory, full candidate host/model validation, smoke and resource reconciliation remain open.

## Implemented behavior

[The optional adapter](../../recovery/t4_attention.py) groups the 16 query heads by their four KV heads, broadcasts K/V with storage views, and restores native head order. It preserves native causal, padding and cached-continuation masks, converts/aligns a head-shared bias before broadcast, and refuses unsupported formats or missing continuation masks. CUDA dispatch permits only the maintained efficient backend; a failure propagates without a math retry. CPU math supports numerical tests only. Both Transformers public attention/mask entries are registered under the new name; the built-in SDPA entries stay intact.

[Candidate wiring](../../recovery/inference.py) makes this explicit and opt-in:

```python
from dataclasses import replace
from recovery.inference import QWEN_9B
from recovery.t4_attention import T4_ATTENTION

proposed_candidate = replace(QWEN_9B, attention=T4_ATTENTION)
```

Constructing this value does not load weights or execute inference. Its existing settings record `attention=recovery_t4_sdpa` and maintained `prefill_chunk_size=256`. All input tokens and the unchanged output reserve remain in the same call-owned cache. Exact settings equality prevents baseline/alternative call reuse. The baseline 9B/4B SDPA settings remain unchanged. The factory rejects an incompatible Torch/CUDA/T4 stack before loading and checks the loaded attention name. This candidate remains proposed and unfrozen; it does not select the model fallback.

[The read-only audit](../../scripts/m5_model_feasibility.py) verifies the existing canonical archive/config, capacity archive and original run-6 ZIP identities, checks the reviewed native memory against original device bytes, and derives all four model/mathematical-size cases. It imports no inference stack, downloads no weights and refuses to overwrite an existing report:

```powershell
python -X utf8 -S -B -m scripts.m5_model_feasibility --output build/m5-memory-review.json
```

The command's success means the offline audit succeeded. Model selection, measured model peak, complete allocator upper bound and full-envelope acceptance remain `null`.

## Executed local checks

Raw commands, durations and separate output/error streams are retained in [the evidence folder](../../notebooks/validation/m5-attention-memory), with [separate local interpreter/package inventories](../../notebooks/validation/m5-attention-memory/local-environments.json) and [actual CPU Torch build](../../notebooks/validation/m5-attention-memory/native-runtime.json). The successful checks are:

| Check | Executed environment / result | Evidence |
|---|---|---|
| Focused inference, exact-setting separation, attempts, workers, durability and memory audit rejection | Project `.venv`, Windows/Python 3.11.9; 96 tests, zero skips; 271.889 command seconds | [Command](../../notebooks/validation/m5-attention-memory/focused-regression.json), [raw results](../../notebooks/validation/m5-attention-memory/focused-regression.stderr.txt) |
| Independent attention references and native hybrid Qwen integration | Local Torch 2.11.0+cpu / Transformers 5.12.0; 15 tests, zero skips | [Command](../../notebooks/validation/m5-attention-memory/native-attention-verified.json), [raw results](../../notebooks/validation/m5-attention-memory/native-attention-verified.stderr.txt) |
| Unchanged native tokenizer/template/decode/cache checks | Four checks per pinned model, zero skips | [9B](../../notebooks/validation/m5-attention-memory/native-tokenizer-9b.json), [4B](../../notebooks/validation/m5-attention-memory/native-tokenizer-4b.json) |
| Complete capacity archive reproduction | Eight checks, zero skips; original 10 accounting rows/80 constructed fixtures reproduced | [Command](../../notebooks/validation/m5-attention-memory/native-capacity.json), [raw results](../../notebooks/validation/m5-attention-memory/native-capacity.stderr.txt) |
| Selected Transformers wheel source | Exact 11,150,246-byte wheel/hash and CRC verified; eight relevant installed modules match it byte for byte | [Source verification](../../notebooks/validation/m5-attention-memory/transformers-source.json) |
| Ordinary wheel and external isolated import | All 29 packaged/installed project modules match current source; 15 attention tests pass outside the repository with `-I -B` | [Package build](../../notebooks/validation/m5-attention-memory/package-build-verified.json), [installed verification](../../notebooks/validation/m5-attention-memory/installed-native-check.json) |
| Existing project dependencies | `.venv` pip check passes | [Result](../../notebooks/validation/m5-attention-memory/project-pip-check.stdout.txt) |
| Actual retained-input memory audit | Standard-library interpreter with `-S`; no Torch import or model call | [Command](../../notebooks/validation/m5-attention-memory/actual-envelope-audit-verified.json), [derived report](../../notebooks/validation/m5-attention-memory/memory-audit.json) |
| Preservation, task states and documentation | Prior notebook/results bytes, canonical payloads, protected science, user edit and local links | [Handoff](../../notebooks/validation/m5-attention-memory/handoff-validation.json), [link check](../../notebooks/validation/m5-attention-memory/check_document_links.py) |

The numerical checks cover causal prefill, full-cache decode, offset/additive/padding masks, fully blocked rows, explicit scaling, head order, noncontiguous input layout, input immutability and K/V storage aliases. A meta-device check retains original K/V storage sizes at 262,144 tokens without allocating GPU memory. A controlled selector verifies efficient-only CUDA routing and refusal to retry; it executes no CUDA operation.

The small random **unquantized CPU** hybrid Qwen model checks both seven tokens with three-token chunks and **513 tokens with the configured 256-token chunks**, including full/chunked final logits, KV/conv/recurrent state, subsequent decode and independent fresh-cache execution. Its maintained Torch recurrent path emits the retained optional-fast-path warning. No pretrained model, NF4 model load, finite sampled study output, GPU workspace or physical device isolation is tested by these CPU forwards. Installed tests use the same local optional stack, not the accepted Linux/Python 3.13 GPU candidate.

The initial combined command retained an import failure because the optional global interpreter lacks the SQLite checkpoint package; the complete project regression subsequently passes in its existing `.venv`. The first audit compared prefixed provider UUIDs with native UUID strings directly; comparison now preserves the assigned ID and checks its native representation explicitly. The first non-isolated wheel build used an old `.venv` builder without `bdist_wheel`; the existing compatible global Setuptools 81 builds the verified wheel without dependency changes. Initial test/audit/build logs and the first handoff-helper failure remain present. The final handoff compares original model IDs, constants and complete default settings directly from the previous Git blob. No missing check is treated as passed, and no package upgrade or prior evidence rewrite was needed.

## Complete-envelope result

The existing proof pays for all permitted histories, including malformed own replies and retained prose. Target/fallback input bounds are **261,004 / 259,484**, plus the unchanged 384-token reserve: **261,388 / 259,868 resident tokens**. Largest constructed fixtures are only **33,490 / 32,913 resident tokens**; they neither replace that proof nor establish a trajectory attaining its upper bound.

| Model | Mathematical size | FP16 embedding/head + ideally packed MLP + full-attention KV conditional subtotal (GiB) |
|---|---|---:|
| 9B | Target | 14.015991 |
| 9B | Fallback | 13.969604 |
| 4B | Target | 10.215698 |
| 4B | Fallback | 10.169312 |

Run 6's native total minus required headroom is **13.062195 GiB** per T4, before other occupancy. Its historical post-probe free memory minus headroom is **12.897278 GiB**. These historical observations are not current availability. The audit pays tied 4B embeddings once, separates the materialized-repeat allocation from the proposed K/V aliases, and exposes cache-growth copies and chunk Q/output/mask terms. Actual CUDA workspace remains unmeasured. Other weights, quantization metadata, recurrent state, activations, workspaces and allocator/context occupancy prevent treating this subtotal as a complete memory upper bound.

Thus the 9B calculation cannot establish complete-envelope fit at the existing conservative bound. It is not an empirical failure or proof that a permitted view attains that bound. The 4B subtotal below the allowance likewise does not prove fit or authorize fallback selection. **R7 and full-envelope memory acceptance remain unresolved.** Caps, physical/logical opportunities, retained bytes, model revisions, package pins, populations, scoring and frozen settings are unchanged.

## Handoff

Preservation review checks **483 prior notebook/result files byte for byte**, including all 22 returned run files, and all three canonical payloads. Scientific configuration/fixtures, root contract/specification and all recovery code except the reviewed inference wiring/new adapter remain unchanged. The user's pre-existing edit stays intact and unstaged. The document/inbound-anchor audit checks **383 local references and 122 Markdown fragments**; all 29 task states match the index.

This offline step is complete; no repeat CPU preparation, run-6 diagnostic, GPU reservation or user upload is requested. No new runnable model-smoke notebook is delivered by this step.

Before model assets/smoke, resolve R7 through the [existing three-outcome contract](../planning/m5-kaggle-first-run/04-model-feasibility-and-smoke.md#the-complete-envelope-evidence-gap): a sound tighter live-input proof with sufficient memory coverage, a valid complete-envelope memory argument, or a documented feasibility blocker. Do not use a short successful prompt or arbitrary padding as coverage. The next full candidate GPU environment must verify this specific zero-stride/masked/chunked layout and native model path; accepted standalone run 6 does not do that.

The original `m5-kaggle-source-v2` and bootstrap payloads remain preserved. They contain earlier source and cannot deliver this new adapter; an eventual model packet must use the new committed source with renewed provenance. Exact prior allocation duration is still unknown despite the user's stopped-session report, so no remaining smoke allowance is invented. Existing authorization persists within unchanged resource gates. T02 stays blocked; progress stays **21 done / eight blocked**. No model generations, pilot/main execution, GPU use or freeze occurred here.
