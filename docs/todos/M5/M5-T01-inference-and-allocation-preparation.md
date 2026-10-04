# M5-T01 — Inference backend and allocation preparation

**Status:** blocked

**Dependencies:** [M4-T06](../M4/M4-T06-reproducible-report-and-cpu-gate.md). M1–M4 must have passed.

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

**Evidence:** Not yet recorded. Add CPU checks, candidate environment and concrete allocation preparation artifacts before marking done.

