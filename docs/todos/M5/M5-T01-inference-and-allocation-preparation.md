# M5-T01 — Inference backend and allocation preparation

**Status:** active

**Dependencies:** [M4-T06](../M4/M4-T06-reproducible-report-and-cpu-gate.md). M1–M4 must have passed.
M4-T06 completes on 6 October 2026 and the
[M1–M4 CPU audit](../../validation/m4-cpu-gate.md) passes. The
[report handoff](../M4/M4-T06-reproducible-report-and-cpu-gate.md#completion-and-m4-gate)
supplies fixed case/annotation rules, analysis settings, assumptions, exact
original-worker reproduction and synthetic reports. This unblocks CPU
preparation only. Actual language weights, state/RNG and raw decoding,
finite outputs, T4 memory/headroom/timing, accepted-host persistence,
capability and complete-schedule allocation remain unverified M5 work;
execution still requires its explicit authorization.

## References

- [Repository contract/authorization](../../../AGENTS.md), [plan M5 runtime](../../IMPLEMENTATION_PLAN.md#runtimeenvironment-validation), and [unresolved allocation issues](../../IMPLEMENTATION_PLAN.md#unresolved-issues).
- Specification [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [loading](../../implementation-research/inference-and-capacity.md#text-only-loading-and-t4-behavior) and [rendering/termination/call independence](../../implementation-research/inference-and-capacity.md#rendering-termination-and-call-independence).

## Intended outcome

A CPU-reviewed direct inference backend and concrete allocation plan are ready for an authorized bounded T4 smoke test.

## Scope and boundaries

- Start with Qwen3.5-9B, maintained Transformers text-only loading and diagnostics for every language weight, including tied heads. Expected unused vision weights cannot excuse missing/newly initialized language weights.
- Configure NF4, double quantization and FP16 explicitly, preserving supported sensitive FP32 calculations. Batch one; one full replica/serial process per T4; no CPU offload, device splitting, conversion wrapper, alternative serving/quantization stack or custom kernel.
- Use enable_thinking=False, temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0 and no presence penalty. Freeze actual template/EOS/PAD behavior only after passing checks.
- Save exact requests, generated IDs and raw generated-suffix text without cleanup. Remove only verified terminal transport framing for parsing; unexpected/internal markers remain. No blanket special-token stripping, JSON repair, closing-brace stopping or constrained decoding.
- Provide fresh KV/recurrent state per call, process-owned device visibility before CUDA initialization, and saved per-call CPU/CUDA seed assignment. Instrument cache lifecycle and order/resume independence; do not promise seed-based exact regeneration.
- Prepare the existing runner's backend integration and concrete development manifest, including all planned validation calls within smoke/pilot limits.
- Record available/proposed device identities, durable storage/backup location, allocation start/stop and billing rules, development/setup/interruption budgets and safe termination allowance. Prepare the reviewable action/cost/configuration before seeking any compute authorization.

## Completion criteria

- CPU/static/mock tests cover exact decoding, terminal framing, full valid cap-ending JSON, overflow-before-generation and call identity/seed/state ownership.
- Host/package/model/tokenizer candidates and template inputs are identified, explicitly not yet a passing GPU lock.
- M1–M4 evidence is current for the chosen schema/template/size; changes reopen affected checks.
- A concrete <=24-call/0.5 aggregate GPU-hour smoke plan and the shared resource envelope are documented. This task performs no GPU allocation or inference.

## Validation and evidence

Use saved generated-token fixtures with internal special markers, invalid suffixes and exact cap endings; verify no normalization turns invalid output valid. Check backend-to-ledger fields and serial worker initialization with mocks. Review actual maintained loader/configuration sources and provider/storage facts; leave hardware-dependent claims for M5-T02.

### Preparation checkpoint

Started 7 October 2026 on clean `feat/m5-inference-preparation`.
Inspected the repository contract, this task, specification §§8–9, runtime
plan, technical synthesis/loading investigation and M4-T06/CPU-audit handoff.
`.venv/Scripts/python.exe -m unittest tests.test_schedules tests.test_schedule_manifests tests.test_peer_views -q`
passes 36 checks in 31.804 seconds on Windows, Python 3.11.9. Existing saved
schedules, identities, renderer, schemas and target/fallback sizes remain the
preparation authority. No frozen scientific configuration is changed.

The user selected a proposed Kaggle plan. No reservation, upload, weights,
inference, compute authorization or GPU lock is implied. Local model-stack
metadata identifies torch 2.11.0, Transformers 5.12.0, Accelerate 1.14.0,
bitsandbytes 0.49.2, tokenizers 0.22.2 and huggingface-hub 1.19.0; the repository
CPU virtual environment deliberately has no torch. Maintained source review
confirms native `AutoModelForCausalLM` text-config extraction, language-prefix
conversion, tied-weight initialization, supported FP32 recurrent paths and
per-call `DynamicCache`. Loading diagnostics and actual device/runtime behavior
remain smoke gates. Backend, fixtures and allocation evidence are in progress.

### Backend checkpoint

The direct adapter and ordinary ledger evidence are implemented. The focused
command `.venv/Scripts/python.exe -m unittest tests.test_inference_preparation tests.inference_checks -q`
passes 25 checks in 6.175 seconds: maintained loader settings, language/tied-head
diagnostics, no offload/splitting, exact suffix/terminal handling, valid cap-ending
JSON, pre-generation request/overflow rejection, finite-score failure, fresh
cache and CPU/CUDA seed assignment, failure cleanup, process ownership,
two serial worker visibility, load/attempt evidence and exact reopened/backup
reuse. A diagnosed nonfinite backend remains blocked with uncertain completion,
with no retry or fabricated raw reply. Optional inference packages are absent
from this CPU virtual environment; every generation is a labeled mock.

The broader deterministic command adds `tests.durable_checks`,
`tests.attempt_checks`, `tests.worker_checks`, `tests.accounting_checks` and
passes all 97 checks in 391.026 seconds at the earlier 20-check adapter checkpoint.
The final 25-check adapter run supersedes that adapter subset. Native 9B
metadata-only `tests.tokenizer_inference` passes four checks in 0.137 seconds,
covering all nine retained native suffix fixtures, actual template/request IDs,
fresh generation defaults and empty independent hybrid caches.
`tests.tokenizer_capacity` renews all eight checks and the unchanged complete
target/fallback bounds, 261,388/259,868 including output reserve.

The [candidate/allocation evidence](../../validation/m5-inference-preparation.md)
records the proposed host, source review, exact template/EOS/PAD candidates,
24-attempt smoke request matrix, unchanged pilot manifest, shared 8/2/2-hour
reserves, two-device allocation convention, 120-second shutdown allowance,
live/backup/off-host destinations and pending account/provider facts.
Full current-source/core/installed regressions and final consistency review
remain required before this task is done. No GPU or empirical gate is passed.

### Identity review checkpoint

Final review replaced Python numeric equality with the existing canonical JSON
representation for settings and token records. Changed booleans/integers/floats
cannot pass exact identity. A factory/worker device conflict is rejected before
creating a worker store or process, preventing two configured workers from
silently selecting the same physical GPU. All 27 final focused checks pass in
8.681 seconds. The noneditable installed package outside the checkout passes
those 27 plus all 14 worker checks (41 total) in 139.913 seconds under hash seed
37; all 28 installed module paths/bytes match the final source. The first
non-isolated build probe lacked `bdist_wheel`; ordinary isolated pip building
fixed it without modifying runtime dependencies or the project build contract.

Core validation passes 260 checks in 221.223 seconds (252 passed, eight expected
optional skips). Native tokenizer/config/cache/decoding checks pass four each
for 9B/4B in 0.180/0.205 seconds. Both immutable revisions were reverified through
the public Hub API; no weights were fetched. Full CPU regression and final
artifact/status review are still running. Prior protected artifacts and all
scientific schemas/inputs/rendering/analysis remain unchanged.

