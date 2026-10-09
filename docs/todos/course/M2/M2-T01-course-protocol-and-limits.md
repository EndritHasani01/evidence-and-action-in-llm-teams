# Course M2-T01 — Course protocol and limits

**Status:** active

**Dependencies:** [M1-T02](../M1/M1-T02-course-inputs-and-schedules.md).

## References

- [Specification common protocol](../../../../PROJECT_SPECIFICATION.md#3-common-peer-protocol), accepted course clause from [M1-T01](../M1/M1-T01-course-contract-and-reuse-boundary.md), and [plan M2](../../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Existing [views/rendering](../../M2/M2-T01-peer-views-and-rendering.md), [strict reply validation](../../M2/M2-T02-strict-replies-and-feedback.md), and [capacity argument](../../../implementation-research/m2-t06-capacity-proof.md).

## Intended outcome

The existing lossless renderer and strict validator consistently apply accepted course shapes and limits, with no leakage, history repair or change to thesis defaults.

## Scope and boundaries

- Thread the single accepted course limits through requests, token reservation, reply validation and settings. Use 256 total generated tokens and 64 prose tokens unless the authoritative adoption records another explicit decision; retain three recipients, eight distinct current references per recipient and 32-token public feedback per slot. Do not impose an arbitrary smaller input window or globally change thesis constants.
- Preserve only permitted current sources, pending replacements/tombstones, public assignments, own replies, received prose and bounded feedback. Keep genuine receipts/notices outside clearable history. Hide gold, hidden values/endpoints, future edits, policy/branch/scope/mask labels and outcome metadata. Render current sources once and archive historical text losslessly with the existing literal layout/footer. Keep one generic authority instruction and the same short task hint across conditions, without imposing a leader/route or requesting a support proof or chain-of-thought.
- Keep full-document strict JSON and nested extra/duplicate-key rejection; reject booleans/coercions/nonfinite numbers, wrong shapes/keys, fragments, fences, stale/unheld references and unauthorized recipients. Repeated references remain subject to the distinct-reference limit, not an invented duplicate prohibition. Wrong numeric answers remain protocol-valid.
- Invalidate the entire reply before any effects when any message fails. Distinguish invalid/failed versus unknown slots without candidate inheritance. Preserve Unicode scalar handling, valid surrogate pairs and unpaired-surrogate rejection. A complete legal reply at the cap remains valid; no JSON repair, schema-constrained generation, extra call or closing-brace stopping.

## Completion criteria

- Course and thesis settings/limits are explicit and isolated; template instructions, validation and token reservation agree. Exact rendered text/native IDs remain separately available.
- Focused course boundary/adversarial checks pass for all peer/control shapes and genuine receipts, with no hidden-field influence on permitted requests.
- Subsequent intervention/capacity tasks can use this real renderer/validator; no whole-envelope capacity claim is made here.

## Validation and evidence

Exercise all candidate shapes and malformed-message whole-reply failures, special-looking/trailing-whitespace archive text, feedback leakage, permission/limit edges and cap-complete versus truncated output. Confirm old thesis fixtures/settings remain intact. Record native-tokenizer and dependency-free checks separately with actual environment and retained artifacts.

**Evidence:** Implementation started 9 October 2026 from `58890ad` on
`feat/course-m1-contract-and-inputs`. The adopted Section 11 limits and course M1
input/schedule gate were inspected. The existing renderer, validator and exact
settings will receive explicit course limits while thesis defaults and retained
archives stay intact. Preparation records are retained in
[course-m2-protocol](../../../../notebooks/validation/course-m2-protocol/).
Course protocol acceptance is pending; no GPU/model, pilot, freeze, main run or
publication is authorized by this work. The pre-existing thesis M5 evidence edit
is preserved and excluded from task commits.

The prerequisite renderer/protocol/inference and course M1 regression passes
80 checks in the repository `.venv` (CPython 3.11.9, Pydantic 2.13.5,
LangGraph 1.2.12, SQLite saver 3.1.1); `pip check` passes. The initial global
interpreter attempt failed because its SQLite saver dependency is missing;
both logs are retained. Native-tokenizer verification uses a separate
environment and remains pending for this task.

**Protocol checkpoint:** one immutable `ProtocolLimits` value in the existing
renderer supplies the two adopted regimes. Explicit course rendering/reservation
and whole-reply validation pass six dependency-free checks and twelve course
strict checks; the combined existing/new renderer and validator regression passes
58 checks. Requests, native text/IDs and validation record shapes are unchanged;
course limit audits use `output_fits(COURSE_LIMITS)` and
`prose_fits(COURSE_LIMITS)`, preserving legacy thesis properties and archive bytes.
Exact settings/round integration and native-tokenizer acceptance remain pending.

**Settings/native checkpoint:** 110 focused integration checks pass, including
real course round/control rendering, whole-reply validation, exact durable
reopen and rejection of thesis replay/settings. An initially missed restart
comparison used the thesis reserve/instruction; it now derives limits from the
saved settings. The existing barrier test spies forward the new keyword without
changing their ordering assertions. The pinned 4B tokenizer passes nine native
checks in a fresh hash-seed-37 process, reproducing the new
[course archive](../../../../tests/fixtures/course_protocol.json.gz) and both
original thesis request/reply archives. Eleven rendered cases, 23 reply cases
and 225 candidate/one-shard cases are retained; those useful cases need at most
132 output tokens and fixed feedback at most 14. Complete JSON at 256 is valid;
257 IDs, 65 prose tokens, known truncation and malformed messages reject all
effects. No whole-envelope capacity claim is made. Full CPU, installed-package
and preservation/documentation audits remain pending.

**Prerequisite handoff, 9 October 2026:** Course/M1-T02 passes the
[input/schedule CPU gate](../../../validation/course-m1-inputs-and-schedules.md#completion-and-handoff),
with saved 20-main/five-development inputs, balanced cohorts, disjoint streams
and complete 5,752/6,280 main and 1,114/1,178 development schedules. Safe protocol
implementation may begin. The input-only course TOML supplies mathematical size;
256/64 rendering, validation, reservation and exact settings still belong to
this task. The handoff admits no model, GPU, pilot, freeze or main execution.
