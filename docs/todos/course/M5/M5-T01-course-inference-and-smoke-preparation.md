# Course M5-T01 — Course inference and smoke preparation

**Status:** blocked

**Dependencies:** [M2-T03](../M2/M2-T03-course-attainability-and-capacity.md), [M3-T02](../M3/M3-T02-course-accounting-and-lifecycle-gate.md). This is CPU preparation; actual GPU work also requires the course M4 gate.

## References

- [Specification inference/resource/consistency contract](../../../../PROJECT_SPECIFICATION.md#8-inference-configuration-and-feasible-allocation), accepted course clause and [plan runtime validation](../../../IMPLEMENTATION_PLAN.md#runtimeenvironment-validation).
- [Course configuration/memory proposal](../../../planning/abs-iis-course-study-proposal.md#memory-why-4b-and-fewer-worlds-are-insufficient-alone), [inference investigation](../../../implementation-research/inference-and-capacity.md), and [existing adapter preparation](../../M5/M5-T01-inference-and-allocation-preparation.md).
- [Actual run-5 CPU acceptance](../../../validation/m5-kaggle-full-preparation-run-5.md), [standalone run-6 diagnostic](../../../validation/m5-t4-compatibility-run-6.md), [attention/memory evidence](../../../validation/m5-attention-memory.md), and [R7 complete-envelope contract](../../../planning/m5-kaggle-first-run/04-model-feasibility-and-smoke.md#the-complete-envelope-evidence-gap).

## Intended outcome

The existing direct backend supports the adopted 4B course regime, and a concrete, bounded GPU smoke packet is reviewable without further architectural design.

## Scope and boundaries

- Reuse the maintained text-only Transformers adapter, serial process ownership, existing records and installed-source checks. The proposed 4B revision is `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`; verify model/tokenizer identity and actual metadata before selecting it. Preserve thesis defaults and avoid another serving, quantization or worker framework.
- Carry adopted course limits through template rendering, settings, raw decoding and overflow admission. Keep non-thinking decoding at temperature 0.7, top_p 0.8, top_k 20, min_p 0 and repetition penalty 1.0, with no presence penalty. Save generated suffix IDs/text unchanged; remove only verified terminal framing for parsing. Accept complete valid cap-ending JSON, retain unexpected/internal markers and reject repair or schema-constrained decoding.
- Confirm fresh KV/recurrent state, per-call CPU/CUDA seed ownership, device visibility before CUDA initialization, serial RNG use and exact backend-to-attempt fields with CPU/mock/native-metadata checks. These are preparation evidence, not actual model acceptance.
- Resolve the course R7 preparation gap with a sound complete-envelope argument or tighter legal live-input proof and a sufficient memory argument, or document a terminal feasibility blocker. Include weights, quantization, recurrent state, activations, cache growth, attention layout/workspace, occupancy and required headroom. A largest fixture, short prompt, arbitrary padding or the proposal's conditional 157,772-token estimate cannot substitute for this evidence.
- Prepare the existing notebook/runner path and exact smoke matrix, source/assets/package provenance, disk and durable backup/export checks, allocation/release instructions and all development/reserve costs. Preserve old source-v2/results; a changed course source packet needs the new committed source and renewed provenance. Reuse accepted CPU/library evidence only where it covers the candidate; verify the new attention layout on the full candidate GPU host later.
- Metadata/tokenizer checks may precede the integrated course CPU gate. Stage language weights only after the complete-envelope preparation gate permits it. Leave current quota, provider duration and remaining historical allowance unknown until verified; no GPU reservation, inference or main execution belongs here.

## Completion criteria

- Focused course adapter checks pass, with unchanged thesis behavior and exact cap/terminal/state/seed/provenance handling.
- The complete course input/memory preparation decision and selected supported attention path are explicit. An unresolved blocker leaves the gate unfinished and supplies limited evidence rather than an invented passing smoke plan.
- A runnable, reviewed packet identifies host/package candidates, storage, exact calls, at most 24 calls/0.5 aggregate GPU-hour, prior-spending treatment and safe release. Refresh it if later course changes alter its committed source or requests.

## Validation and evidence

Use native 4B metadata/tokenizer and saved generated-token fixtures, mocks for load/state/device ownership, installed-source verification and the course capacity proof. Check current maintained loader/package/provider sources only where needed. Record commands, source/candidate identities, limits, packet locations and pending actual-host checks; do not rerun unchanged generic preflight without an affected requirement.

**Evidence:** Preparation starts 11 October 2026 from `2753c18` on
`feat/course-m5-inference-preparation`, with a clean working tree. Follow
[the scoped acceptance record](../../../validation/course-m5-inference-and-smoke-preparation.md).
Reuse the accepted course M1–M4 CPU gates and earlier adapter/library evidence;
renew only course candidate, envelope and packet behavior. GPU/model smoke
and actual resource admission remain separate gates.

**Prerequisite handoff, 11 October 2026:**
[Course M3 accounting/lifecycle evidence](../../../validation/course-m3-accounting-and-lifecycle.md)
supplies the existing saved `CourseBudget` contract, original attempt/process/
allocation joins, conservative planned-device forecast admission, independent
deadline and confirmed-release semantics. Pass `regime="course"`; preserve
literal 4B/256/64 settings and run bindings. Supplemental documented prior bounds
cover only spending absent from supplied historical worker ledgers. Unknown
prior/smoke usage or setup attribution withholds admission; synthetic CPU
timings and assigned zero-prior test inputs establish no T4 throughput or quota.
The complete main forecast excludes recorded loading reserved separately while
physical/policy costs retain it. Recover actual prior allocation and cumulative
smoke usage, verify provider/billing/release terms, and prepare a new committed
course source packet without changing historical source-v2/results. The complete
156,251-token native bound is preparation input, not accepted model memory.
Course M3's final broad acceptance passes; its CPU prerequisites are accepted.
Course M4 and the runtime/resource/authorization gates still precede
any GPU allocation/inference.

**Preparation checkpoint, 11 October 2026:** The safe CPU implementation is
verified at `0260ca6`: 64 affected source/64 outside-checkout installed checks,
four native source/four native installed checks and the literal CPU review
notebook/export pass. All 24 exact proposed smoke requests, pinned metadata,
package/source manifest and conditional complete-envelope arithmetic are saved
in [the preparation evidence](../../../validation/course-m5-inference-and-smoke-preparation.md#packet-and-resource-handoff).
Thesis defaults/todos and prerequisite artifacts remain intact.

**Unresolved requirement:** R7 lacks a complete supported physical memory
upper bound. The original 156,251-token argument and 9,172,843,936-byte
conditional component sum remain historical preparation evidence. The offline
continuation below tightens that analysis, but still leaves loading, selected
native workspace and allocator/context costs without sufficient bounds.
Neither fit nor terminal model infeasibility is established. Under the
completion criterion above this task remains unfinished; weight staging and
M5-T02 admission are withheld. The delivered notebook runs only the safe CPU
review. Resolve R7, then renew any affected source/request/host provenance and
resource checks before preparing an executable model smoke. No terminal M5
failure or M6 limited-report route is accepted by this checkpoint.

**Offline continuation, 11 October 2026:** The user explicitly requested R7
resolution without GPU execution. Resume only capacity/source/meta-device
analysis, preserving the existing protocol and accepted evidence. Follow
[the offline R7 record](../../../validation/course-m5-r7-offline-review.md).
The supplemental proof at `5ce6d5f` verifies **109,851 input + 256 output reserve
= 110,107 resident tokens**, with unchanged runtime bytes/caps. Five source and
five outside-checkout native checks pass with zero skips; all 29 runtime modules
match the accepted installed code. The conditional component sum becomes
7,400,914,336 bytes. Three meta-device traces and 12 pinned native sources narrow
the remaining gap but do not bound CUDA reservation/workspace/occupancy across
the whole call. The task remains blocked and unfinished, with weights/model
smoke withheld and no accepted terminal failure. Reuse the passing proof and
existing CPU packet; obtain a sufficient complete memory argument before
refreshing affected provenance. No GPU or weights were used in this continuation.
