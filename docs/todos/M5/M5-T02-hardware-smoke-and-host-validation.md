# M5-T02 — Bounded hardware smoke and host validation

**Status:** blocked

**Dependencies:** [M5-T01](../M5/M5-T01-inference-and-allocation-preparation.md). M1–M4 must have passed. Explicit authorization covering the GPU/paid-compute scope is also required.

M5-T01 completes on 7 October 2026 with its
[CPU completion checks](M5-T01-inference-and-allocation-preparation.md#completion-and-handoff)
and [proposed private Kaggle T4-x2 packet](../../validation/m5-inference-preparation.md).
The preparation dependency is satisfied. Execution authorization is absent;
actual account/quota/monetary terms, device/host/storage checks, all 24 exact
smoke requests, durable off-host export and confirmed provider release remain
preflight work. The proposed ceiling is 24 physical attempts / 0.5 aggregate
GPU-hour (at most 900 wall seconds with two allocated T4s), including loading,
idle GPU 1 and shutdown. No upload, reservation or model inference has occurred.

## References

- [Repository contract/authorization](../../../AGENTS.md), [plan runtime validation](../../IMPLEMENTATION_PLAN.md#runtimeenvironment-validation), and [smoke/pilot gates](../../IMPLEMENTATION_PLAN.md#bounded-smoke-and-capability-pilot).
- Specification [§8.1–8.2](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [inference uncertainty](../../implementation-research/inference-and-capacity.md#resource-and-validation-conclusions).

## Intended outcome

One candidate configuration passes actual T4 loading, finite-output, worst-context memory, decoding and call-independence checks inside the smoke allowance.

## Scope and boundaries

- Explicit GPU/paid-compute authorization must cover this action. Passing M1–M4 or writing this task is not authorization; reuse valid existing authorization rather than asking again.
- Stop at 24 smoke calls or 0.5 aggregate GPU-hour, whichever comes first. Charge inference validation calls, failed attempts, loading and allocated idle time appropriately against the shared development/setup envelope; the allowance cannot override time limits.
- Test worst requests, all output shapes, useful forwarding, a corrected continuation, raw decode/termination and timeout handling.
- Inspect actual language-weight inventory/loading diagnostics, device placement, CUDA/driver/packages, selected attention/recurrent paths, precision, allocated/reserved/peak memory and finite outputs. Require >=1.5 GiB free headroom at the accepted worst prompt, no unexplained language weights, offload or splitting.
- Verify fresh cache/recurrent state, seeds and isolation under prior-call/order/resume perturbations, and document stochastic/device limits. Replay still uses saved exact parents.
- Rerun focused replacement/checkpoint/process-crash/backup checks in the candidate GPU host environment and verify its SQLite/durability/storage behavior. CPU Windows evidence is not host validation.
- If 9B fails hardware/runtime gates, only the specified 4B fallback is eligible, within the same development allocation. A changed model/template/lock/backend/timeout reopens affected earlier checks; never pool configurations.

## Completion criteria

- A named candidate passes all smoke/host checks with actual measured artifacts and no unresolved isolation/leakage/queue issue.
- Calls, attempts and aggregate allocation reconcile within both smoke and shared budgets; record all failed configurations.
- The candidate can proceed only to the first 90 capability slots, not recovery or main execution.
- If none passes within resources, keep the task blocked, record terminal feasibility evidence and enable the limited-evidence audit path in M6-T02. Do not mark the gate passed.

## Validation and evidence

Link every acceptance statement to load logs, actual requests/replies/token IDs, memory/device traces, cache instrumentation, host CPU/crash checks and cost rows. State accepted settings and limits, timeout observations, failed checks and any required fallback/reruns.

**Evidence:** CPU preparation is linked above; actual smoke/host acceptance
evidence is not yet recorded. No GPU work or compute authorization has been
supplied by completion of M5-T01.

