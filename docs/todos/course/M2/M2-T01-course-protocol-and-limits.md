# Course M2-T01 — Course protocol and limits

**Status:** done

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

**Evidence:** Completed 9 October 2026 from `58890ad` on
`feat/course-m1-contract-and-inputs`, following the adopted Section 11 limits and
the [M1 input/schedule gate](../../../validation/course-m1-inputs-and-schedules.md#completion-and-handoff).
The [course protocol evidence](../../../validation/course-m2-protocol-and-limits.md)
records implementation, exact commands, environments, failures/corrections,
installed provenance and preservation/link/status audits. Raw records remain in
[course-m2-protocol](../../../../notebooks/validation/course-m2-protocol/).

One immutable `ProtocolLimits` value in the existing renderer supplies the
adopted course 256/64 limits while preserving thesis 384/128 defaults. Rendering,
full output reservation, strict validation, generation/suffix handling and exact
saved settings agree across rounds, controls, durable reopen and replay. Course
settings require the pinned 4B candidate and retain all six limits in the existing
settings JSON. No record-shape changes, new persistence, dependency or runtime
fork are needed. Course token audits pass explicit limits; legacy thesis
properties and original settings/archive bytes remain compatible.

Six dependency-free limits/rendering, twelve strict course and six exact-settings
checks pass. The affected course/thesis integration passes 110 checks without
skips. The pinned 4B tokenizer passes nine native checks in a fresh hash-seed-37
process, reproducing the new [course archive](../../../../tests/fixtures/course_protocol.json.gz)
and both original thesis request/reply archives. Eleven rendered cases, 23 reply
cases and 225 candidate/one-shard cases cover all saved main/development peer and
control shapes. Useful outputs need at most 132 tokens and public feedback at
most 14; complete JSON at 256 is valid. The 257/64/65, truncation, permission,
strict JSON, Unicode and literal-history edges have whole-reply assertions.

Installed-package checks outside the source checkout pass 81 checks and a
24-check hash-seed-37 repeat without skips; all 29 production module bytes match
the verified source. Core-only discovery passes 340 of 348 checks with eight
expected optional-library skips. The full CPU command reached all 558 checks:
549 non-lifecycle checks and seven lifecycle methods passed, with four failing
kill-point subcases in two methods caused solely by an old validation-spy
signature. The spy now forwards `limits`; the complete nine-method lifecycle
rerun passes with every original external-kill/restart assertion retained.
Production code did not change after the full run. The original failing log and
passing rerun remain separately recorded; no single-command full pass is claimed.

Preservation audits verify the adopted specification, course inputs/schedules,
original thesis todos/defaults/fixtures, plan Sections 1-10 and the pre-existing
M5 evidence edit. That user edit remains unchanged and unstaged. `pip check`,
whitespace and documentation/status checks pass.

**Handoff:** [Course/M2-T02](M2-T02-course-interventions-and-replay.md) is ready to
renew course event/retention/replay acceptance using the real renderer/validator
and explicit settings. The complete-context witness/capacity gate remains
course/M2-T03. CPU verification accepts no GPU/model, capability/pilot, runtime
freeze, main execution or publication; original thesis gates remain separate.
