# Course M5-T02 — Course hardware smoke and memory acceptance

**Status:** blocked

**Dependencies:** [M4-T04](../M4/M4-T04-course-report-and-cpu-gate.md), [M5-T01](M5-T01-course-inference-and-smoke-preparation.md). Explicit GPU authorization and resource admission are separate prerequisites; reuse prior authorization only within its recorded scope.

## References

- [Specification model/controls](../../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [resources/freeze](../../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), [consistency requirements](../../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements), accepted course clause and [plan bounded smoke](../../../IMPLEMENTATION_PLAN.md#bounded-smoke-and-capability-pilot).
- [Course memory proposal](../../../planning/abs-iis-course-study-proposal.md#memory-why-4b-and-fewer-worlds-are-insufficient-alone), [existing hardware task](../../M5/M5-T02-hardware-smoke-and-host-validation.md), and [attention/memory limits](../../../validation/m5-attention-memory.md).

## Intended outcome

Actual 4B inference on the selected T4 host passes course-envelope memory, language-loading, isolation, decoding, persistence and safe-release checks within the bounded smoke allowance.

## Scope and boundaries

- Before allocation, confirm the current source packet, course CPU/R7 preparation gates, package/assets/storage, account/provider constraints, durable export and allocation clock. No unrecorded historical allocation becomes zero; another account does not erase cost. Respect the adopted ceiling and remaining shared smoke/development allowance.
- Stop at 24 calls or 0.5 aggregate GPU-hour, whichever comes first, including assigned load/setup/idle/release time. Two assigned T4s allow at most 900 wall seconds before other charged intervals; elapsed time and aggregate device-hours are distinct. Record every failed/interrupted attempt and stop safely if any limit cannot be respected.
- Verify actual driver/CUDA/packages, full candidate source/environment, one complete text-only replica and one serial worker per device, batch one, NF4/double quantization/FP16 and supported sensitive FP32 paths. Diagnose every language weight and tied head; expected unused vision weights cannot excuse missing/new language weights. No CPU offload, device split, alternate quantizer or custom kernel.
- Establish at least 1.5 GiB free headroom for the proved complete course envelope, including peak/cache-growth/workspace/allocator occupancy. Validate the selected attention/recurrent path on actual CUDA; if the existing adapter is used, check its zero-stride head layout, masks/causality and chunk boundaries. Combine justified proof and measured coverage; do not replace full-envelope acceptance with short outputs or arbitrary padding.
- Cover finite outputs, exact native rendering/generated suffix/terminal handling, complete versus malformed cap endings, forwarding, a corrected continuation, overflow rejection and timeout cleanup. Instrument fresh hybrid state and per-call RNG, perturb call order/resume and record nondeterminism/device limits. Archived parent replies remain the source of exact replay.
- Rerun affected checkpoint/attempt/isolation checks on the accepted GPU host. Export ordinary closed snapshots/raw receipts, reopen them off-host and verify confirmed provider release. A standalone library diagnostic or successful model answer does not substitute for these checks.

## Completion criteria

- All actual-host smoke thresholds pass for one course candidate, linked to calls, memory measurements, loading diagnostics and host persistence checks.
- Allocation/attempt costs and prior uncertainty are reconciled; exports independently reopen and session release is confirmed. No pilot or main result is inferred.
- Failed capability/memory/runtime/resource admission stops inference and records the terminal blocker for limited reporting; changing candidate reopens affected gates and charges both attempts.

## Validation and evidence

Execute the approved packet within its exact limits. Retain raw IDs/text, candidate/host facts, cache/state observations, boundary-memory evidence, failure/timeout cleanup, closed-copy checks and allocation/release receipts. Record incomplete checks explicitly rather than extending smoke to finish them.

**Evidence:** Not yet recorded. Standalone run-6 diagnostics and CPU adapter checks do not pass this course model gate.

**Preparation handoff, 11 October 2026:**
[Course M5-T01 evidence](../../../validation/course-m5-inference-and-smoke-preparation.md#packet-and-resource-handoff)
supplies 24 exact unexecuted requests, a new committed source/asset/package
packet and a passing CPU review/export. R7 remains unresolved; its conditional
memory subtotal supplies no loading or GPU admission. Preserve unknown prior
attempts/allocation/quota/duration and the cumulative 24-attempt/1,800-device-second
ceiling. Do not reserve devices or stage weights from this blocked packet.
The full candidate attention layout, model memory/state, actual storage,
provider release and resource/authorization gates remain pending.
