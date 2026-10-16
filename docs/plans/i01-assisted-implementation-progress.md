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
| A02 | 28 saved disjoint worlds, owner counters, fixed assignment/seeds | Core generation/assignment/overlap checks pass; exposed-input release inventory pending |
| A03 | Exact common/control text, source-last renderer, private views, native bound | Core/native checks pass (7,612/8,192 conservative bound); full release checks pending |
| A04 | Literal history boundary, isolated siblings, strict effects/finality/wait | Core checks pass; workflow lifecycle verification pending |
| A05 | Exact ≤32-token rejection feedback and raw reason preservation | Core priority/native checks pass; integrated trace checks pending |
| A06 | Four reachable diagnostic fixtures, predicates and physical accounting | Pure constructors/predicates verified; workflow/report delivery pending |
| A07 | Four complete pilots and exact 3/4 + 7/8 objective decision | Pending |
| A08 | 480 ordinary /20 reserve /500 total; retry/reload/resume/unknown safeguards | Admission checks pass; new-load and full workflow verification pending |
| A09 | Exact conservative forecast, fixed session clock, per-call export guards | Pending |
| A10 | Primary/effort/unknown bounds/paired bootstrap/degeneracy and casebook | Pending |
| A11 | Honest qualification/diagnostic/pilot/main coverage and full raw UI | Pending |
| A12 | Thin full notebook/CLI/source wheel, finite cells, source-bound restore/cleanup | Pending |
| A13 | Legacy/thesis behavior and historical Course-7 evidence preserved | Baseline recorded externally; final comparison pending |
| A14 | Focused CPU checks, native tokenizer, scripted full-bound/resume/portable evidence | First 12 focused checks and native bound pass; full workflow/installed checks pending |
| A15 | Documentation, installed delivery, final requirement-by-requirement audit | Pending |

## Checkpoints

1. Adoption/preparation: §12.1, configuration and original approved design texts.
2. Core data/presentation/protocol and focused deterministic verification.
3. Diagnostics, workflow/admission/accounting and scripted lifecycle verification.
4. Reporting, UI/notebook/source delivery, installed checks and final evidence.

Core checkpoint evidence: [implementation evidence](../validation/i01-assisted-implementation.md).

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
