# Bounded T4 library compatibility preparation

Planned 9 October 2026 after [actual run 5](../../validation/m5-kaggle-full-preparation-run-5.md) passes the unchanged candidate's 97 CPU checks. The user explicitly requests planning and implementation of the next compatibility notebook. Existing GPU authorization persists. [AGENTS.md](../../../AGENTS.md), specification [§8](../../../PROJECT_SPECIFICATION.md#8-inference-configuration-and-feasible-allocation) and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements) govern this work; this document makes no scientific change.

## Scope and decision

Resolve the **small-operator portion of R8** before any pretrained weights. The pinned [Transformers 5.12 SDPA helper](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/integrations/sdpa_attention.py) selects native GQA without a mask and explicit K/V repetition otherwise. [Torch 2.11](https://docs.pytorch.org/docs/2.11/generated/torch.nn.functional.scaled_dot_product_attention.html) documents fused-backend limitations, public backend selection, FP32 math intermediates and restricted GQA support. Tiny tensors can identify this risk without allocating a long quadratic score matrix.

The accepted CPU environment is disposable and cannot be assumed to survive a GPU transition. Recreating its 4.07-GB CUDA closure during a short library check would obscure the operator question and spend allocation on setup. Instead:

- Require the **host Torch 2.11.0+cu128 / CUDA-build 12.8**, Linux x86-64/Python 3.13 and two distinct T4s. Record host package versions and differences from the CPU candidate. Fail with retained diagnostics on a different Torch build; do not upgrade the kernel.
- Fetch only the already pinned **bitsandbytes 0.49.2 Linux wheel**, 60,651,714 bytes, SHA-256 `54b771f06e1a3c73af5c7f16ccf0fc23a846052813d4b008d10cb6e017dd1c8c`. Verify receipt/size/hash, CRC/member safety and expansion capacity before extraction into owned scratch. No pip installation, populated-venv copy or mutation of the base environment.
- Run fresh isolated child interpreters with one physical GPU UUID visible before importing Torch. Only the verified bitsandbytes wheel is added to that child's import path. Capture its package/native-library origins and the host Torch/configuration facts.
- This is a **standalone library diagnostic**, not the clean scientific candidate. Transformers is not imported or installed: tests exercise public Torch calls matching the reviewed helper's mask/head semantics. Full candidate GPU provenance and actual Qwen attention/recurrent paths must be rechecked in the eventual model environment. A tiny NF4 module is synthetic, not a pretrained model or generation.

This deliberate diagnostic scope avoids inheriting base packages as an accepted model lock. It cannot pass T02, freeze a backend, select 4B, or waive R7. A different library version needs a new reviewed diagnostic rather than silently pooling results.

The [local wheel-byte audit](../../../notebooks/validation/m5-t4-compatibility/wheel-audit.json) verifies all 85 members/CRCs and **184,269,948 expanded bytes**. This is a real read-only Linux-wheel audit on Windows; no Linux native library is imported. Temporary extraction needs about 184 MB plus reserves, not a second CUDA package closure.

## Exact diagnostic operations

Extract both immutable config bytes from the existing canonical archive; preserve their hashes and verify shared geometry: batch one, 16 query heads, four K/V heads, dimension 256 and eight full-attention layers. Probe each physical T4 serially:

1. FP16 causal prefill with length **32**, no mask, native GQA.
2. The same input with explicit K/V repetition, both automatic and forced memory-efficient dispatch.
3. An explicit tiny causal boolean mask with repeated K/V, matching the maintained masked branch.
4. Decode with query length **one**, K/V length **32**, no mask and `is_causal=False`, comparing GQA, repetition and forced efficient dispatch.
5. A **128-by-256** NF4/double-quantized synthetic weight, FP16 computation, with batch-eight and single-row inputs. Compare finite outputs against that same dequantized weight, not the original unquantized weight.

Record public eligibility/debug reasons, warnings, actual profiled operator/backend names and CUDA kernel names when available, finite/toleranced comparisons, shapes/dtypes, elapsed time and CUDA allocated/reserved/peak/free memory. The forced-backend negative case may be unsupported; arbitrary CUDA errors, nonfinite outputs, UUID conflicts and mismatches are failures. Missing profiler evidence remains unknown rather than being inferred from speed. No custom kernel, global monkey patch or production attention change is introduced.

## Context and resource boundaries

Renew the existing conditional arithmetic from verified config bytes: FP16 full-attention KV is **32,768 bytes/token**, 8 GiB at the 262,144 cap. FP16 embeddings/heads plus ideally packed four-bit MLPs and KV subtotal **14.0390625 / 10.23876953125 GiB** for 9B/4B under the stated assumptions, excluding other memory. Also show the separate repeated-K/V temporary and dense-score terms. These estimates do not establish legal attainability, actual weight dtypes/placement or measured memory. **R7 remains unresolved**, with full-envelope acceptance explicitly unknown; never pad arbitrary tokens or change the cap.

The notebook has a **360-second controller deadline**, including the existing 90-second export reserve. Owned commands are bounded; no next device starts after unconfirmed cleanup. Reserve **120 seconds** for download/provider stopping and conservatively allow **60 seconds** before the first code cell. The user must enable T4 x2 only when ready and start Run All within one minute of assignment; otherwise stop and report elapsed allocation instead. The conditional upper bound is `2 × (60 + 360 + 120) = 1,080 allocated GPU-seconds` (**0.3 aggregate GPU-hour**). This is a ceiling under that declared start/stop discipline, not an independently verified provider interval.

Count actual compatibility/setup/idle/shutdown spending within existing shared budgets and conservatively retain it for later smoke reconciliation; it does not grant a fresh 0.5-hour allowance or reset spending by notebook/account. Provider assignment/release and prior allocation remain unknown until external evidence arrives. Record observed workflow time separately from conditional bounds. Stop admission before each command, preserve partial/unknown stages and export on handled failure/interrupt. Do not automatically retry operations or execute model smoke afterwards.

## Files and validation checkpoints

| Checkpoint | Small implementation / acceptance |
|---|---|
| Planning | This contract, exact input-wheel/config audit and primary-source review. Commit before implementation. |
| Controller/probe | `scripts/m5_t4_compatibility.py`; reuse existing bounded command, downloader, storage, SQLite and allowlisted export helpers. No changes to scientific modules, fixtures, candidate pins or prior notebooks. |
| Notebook builder | `scripts/build_t4_compatibility_notebook.py`; embed the reviewed helper/program/config/wheel identities, reject overwriting an earlier artifact, no source/input dataset needed. |
| Focused verification | Static arithmetic, package/hash/path safety, wrong host/build/UUID, backend evidence versus unknown, partial/failure export, deadline/restart/cleanup gates; real CPU numerical comparisons where available. No mock result called a T4 success. |
| Delivery | `notebooks/recovery_m5_kaggle_t4_compatibility.ipynb`; valid schema/syntax, empty outputs/counts, exact source/checkpoint binding. Real Jupyter refusal plus controlled complete workflow must exercise the shipped cells/export, preserving originals. |
| Handoff | Actual local evidence in `notebooks/validation/m5-t4-compatibility/`, linked validation/task/progress updates and logical commits. User runs **T4 x2 / Internet On**, downloads ZIP/executed notebook, stops the session and returns them under `notebooks/run/6/`. |

Actual T4 dispatch/NF4 observations remain pending until that returned run. An efficient repeated-K/V observation may motivate a separately reviewed public attention-interface change; it is not already selected. Model assets, exact 24-slot requests, admission guards, full model smoke, pilot and freeze remain the later K11–K15 gates.

## Controller/probe checkpoint, 9 October

The controller, standalone probe and immutable builder are implemented. [Named local checks](../../../notebooks/validation/m5-t4-compatibility/implementation-validation.json) pass **42 operational tests and four real CPU numerical tests**, zero skips, on Windows/Python 3.11.9. They cover byte/path/import origins, wrong host/build/UUID, forced-backend negatives, deadline and cleanup refusal, partial exports, repeated-cell protection and immutable builder inputs. Real isolated imports verify the extracted package remains unchanged across workers: `-I` ignores `PYTHONDONTWRITEBYTECODE`, so each child also uses `-B`. [Torch's pinned device binding](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/csrc/cuda/Module.cpp) supplies the UUID string representation used for comparison; actual physical matching is still unrun here.

The first arithmetic test had an incorrect expected 4B literal; a later test incorrectly required Linux process-group status from a normally exited Windows child. Both test assertions are corrected, their original failed logs are retained, and the complete 42-test suite passes. Neither required changing scientific settings or the existing operational helper. The installed CPU Torch 2.11.0/bitsandbytes 0.49.2 APIs produce finite matched SDPA/NF4 results; their retained deprecation warnings are not T4 kernel evidence. [Actual canonical-config arithmetic](../../../notebooks/validation/m5-t4-compatibility/static-envelope.json) reproduces the conditional estimates above with acceptance unknown.

Notebook generation and real Jupyter delivery checks follow this source checkpoint; actual T4 execution and all model gates remain pending.
