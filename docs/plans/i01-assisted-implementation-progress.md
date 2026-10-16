# Assisted I-01 implementation progress

16 October 2026. User-authorized implementation; **no GPU inference or experimental
execution authorized**. Scientific authority is
[specification §12.1](../../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026),
which adopts the [design](i01-course-final-experimental-design.md) and
[exact annex](i01-course-final-design-protocol-and-acceptance.md).
Their dated proposal text is preserved. This checklist tracks implementation
and evidence; it changes no scientific requirement.

| ID | Required deliverable / invariant | Current evidence |
|---|---|---|
| A01 | Scoped adoption, explicit new configuration, legacy authority retained | Adoption commit `7a71783` |
| A02 | 28 saved disjoint worlds, owner counters, fixed assignment/seeds | Core and actual exposed-input inventory pass: 56 new inputs versus 60 distinct exposed inputs, nine checked sources; exact packet/regeneration binding verified |
| A03 | Exact common/control text, source-last renderer, private views, native bound | Final native check passes (7,634/8,192 conservative bound), including seven adversarial literal families; installed delivery pending |
| A04 | Literal history boundary, isolated siblings, strict effects/finality/wait | Core and full scripted workflow/portable replay pass |
| A05 | Exact ≤32-token rejection feedback and raw reason preservation | Core/native and full scripted invalid-action traces pass |
| A06 | Four reachable diagnostic fixtures, predicates and physical accounting | Core/workflow/report verified; legal diagnostic nonpass does not veto main |
| A07 | Four complete pilots and exact 3/4 + 7/8 objective decision | Live scripted and raw-control boundary cases pass; failed rule leaves main unknown |
| A08 | 480 ordinary /20 reserve /500 total; retry/reload/resume/unknown safeguards | Full 480-call scripted workflow, 500 admission bound, two eight-call reload cycles and exact portable replay pass |
| A09 | Exact conservative forecast, fixed session clock, per-call export guards | Implemented; current-session export reset, raw replay capacity and deadline/precommit guards verified |
| A10 | Primary/effort/unknown bounds/paired bootstrap/degeneracy and casebook | Hand-scored cases, physical/logical denominators, eight figure pairs and fixed case selection verified |
| A11 | Honest qualification/diagnostic/pilot/main coverage and full raw UI | Source tests pass: eight qualification rows, four diagnostics, intended arm/stratum coverage, unknown effort and real zero-model operator inspection/export |
| A12 | Thin full notebook/CLI/source wheel, finite cells, source-bound restore/cleanup | Source delivery checks pass: 37 assisted /33 legacy finite cells, explicit regime selection and real operator checkpoint; installed release pending |
| A13 | Legacy/thesis behavior and historical Course-7 evidence preserved | Baseline recorded externally; final comparison pending |
| A14 | Focused CPU checks, native tokenizer, scripted full-bound/resume/portable evidence | 108 affected source tests exercised; one legacy wording regression corrected and rerun with four delivery/report checks (five pass); final native checks pass; installed/final audit pending |
| A15 | Documentation, installed delivery, final requirement-by-requirement audit | Pending |

## Checkpoints

1. Adoption/preparation: §12.1, configuration and original approved design texts.
2. Core data/presentation/protocol and focused deterministic verification.
3. Diagnostics, workflow/admission/accounting and scripted lifecycle verification.
4. Reporting, UI/notebook/source delivery, installed checks and final evidence.

Core checkpoint evidence: [implementation evidence](../validation/i01-assisted-implementation.md).
Core implementation commit: `4bf4020`. Workflow/report verification adds eleven
distinct checks without repeating unrelated thesis/GPU tests.

## Preservation and pending gates

Initial checkout: `141a5c311feaf379cd4b60fab27079d9c9e2349f` on
`feat/smaller-natural-experiment`, with four task-owned untracked research/design
documents. Initial 2,315 tracked/visible untracked file hashes were recorded
outside the repository. Only explicitly task-owned changes may be committed.
Course-7 and earlier release/run directories remain protected historical evidence.
Do not require amended current source to have Course-7's historical source hash;
reconstruct against its frozen source and check legacy behavior separately.

Actual T4 loading, current-load state/headroom/latency, qualification, pilots and
main remain unrun. Passing CPU checks or completing implementation grants no
execution authorization. The existing thesis task index/status is separately
scoped and must not be rewritten as I-01 progress.
