# Assisted I-01 implementation evidence

16 October 2026. Software implementation and CPU/installed verification complete under
[specification §12.1](../../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026).
The [requirement checklist](../plans/i01-assisted-implementation-progress.md)
distinguishes completed software checks from unrun actual-host gates. No model is loaded and no
GPU inference, qualification, pilot or main experiment is executed.

## Adoption and first core checkpoint

Adoption `7a71783` adds the approved assisted-v2 condition and configuration
while preserving the dated design documents and all earlier regimes.

Implemented pure task/assignment logic, the exact approved common instruction
text and renderer, history boundaries, rejection-feedback selection, the four
single-call diagnostic constructors/predicates, exact whole-input overlap
checking and regime-bound admission limits. The native adapter selects the new
presentation explicitly and rejects thinking in this direct-only condition.
Initialization requires an explicit independent new campaign. These are code
and CPU findings, not demonstrated agent improvements.

Executed command:

```powershell
python -m unittest tests.test_i01_assisted_core tests.test_i01_assisted_accounting tests.test_i01_integration.Integration.test_raw_resume_literal_siblings_report tests.test_i01_fresh_run.FreshRun.test_fresh_twenty_attempt_preparation_replay_and_checkpoint -v
```

**12 tests pass** (24.684 seconds on this Windows/Python 3.11 CPU host). Tests
compare exact instructions against the annex; independently verify arithmetic,
balances and fresh-seed regeneration; test whole-input overlap, source privacy,
multiline literal rendering, finality/invalid effects and diagnostic reachability;
compare legacy core manifests/views/actions/messages to frozen `141a5c3` source;
exercise 480 ordinary +20 reserve admission and unknown-spending blocks; and
retain the legacy raw-resume/report and fresh-preparation/export checks.
The admission maximum is a synthetic ledger test, not a whole-model campaign.

An actual locally cached Qwen3.5-9B tokenizer/native-template check passes with
the new renderer: conservative retained input **7,612 ≤8,192**, direct resident
bound 8,704, and every selected rejection-feedback string ≤32 native tokens.
No model weights or GPU are used. The cache's metadata directory is under the
existing ignored `build/m5-kernel-v3-1348fd72a9494ee18d8607c9fe4c3277/`
preparation fixture. This is input-framing evidence, not T4 loading/headroom or
behavioral qualification. Receipt:
[assisted-core-checks.json](../../notebooks/validation/i01-development/assisted-core-checks.json).

## Workflow, resource and reporting checkpoint

Eleven additional distinct checks pass:

```powershell
python -m unittest tests.test_i01_assisted_report tests.test_i01_assisted_workflow -v
```

The first nine tests passed in 82.134 seconds. After adding the precommit/fixed
clock and pending-raw capacity guards, those two new tests passed in 4.026
seconds. The full-bound fixture uses a declared CPU oracle, not model responses:
480 ordinary attempts settle, all 288 pilot/main recovery actions are rejected
without delivery, and all twenty main pairs remain included. Exact 3/4 and 7/8
pilot usefulness passes despite those recovery failures and a diagnostic nonpass.
Either one fewer original/control fails. All four pilots are collected before
an unsuccessful feasibility decision, and main remains wholly unknown.

Two new-load cycles each consume six state checks and two envelopes, using
16 reserve attempts without regenerating accepted controls/diagnostics. A third
eight-call cycle is rejected. Completed stages replay with zero new attempts;
quiescent ZIP/extracted restore reproduces exact read-only analysis and spending.
A restored controller cannot reuse an old session's export-time measurement.
Known pending raw replay is excluded from new generation/first-slot capacity;
new attempts require precommitment, and a repeated session-window call cannot
extend its deadline.

Hand-scored saved-data cases verify paired coverage/bounds, unknown effort,
locally refutable/obsolete values, completion/wrong agreement, deterministic
six-category case selection, bootstrap ordering/degeneracy and intended-slot
denominators. Physical interrupted attempts retain unknown validity and are
distinguished from logical raw-call denominators. One complete report renders
all eight SVG/PNG figure pairs with an eight-control qualification scope.
The existing Course-7 analyzer output still equals its preserved saved
`analysis.json` exactly. A baseline comparison finds zero protected-file changes;
only authorized specification/plan and I-01 package changes differ so far.
Receipt: [assisted-workflow-report-checks.json](../../notebooks/validation/i01-development/assisted-workflow-report-checks.json).

## Source delivery and compatibility checkpoint

The assisted operator/CLI and both identical 37-cell notebooks now expose the
four diagnostics, preparation checkpoint, four finite pilots/checks and ten
fixed main batches. The builder's legacy default still generates its separate
33-cell flow. Explicit regime selection prevents an old packet or cached import
from silently entering the assisted notebook. Full raw inspection, intended
coverage, scalar/diagnostic distinctions, observed partial cost and unknown
whole-phase cost remain visible. Correct-prefix reporting is counts only.

The historical course-3 migration guard now checks the unchanged legacy core
functions/prompts and native settings while permitting reviewed assisted-only
additions. Proposed source must also equal the actually imported reviewed
library. Existing negative source-change checks remain effective. Assisted
studies cannot use that historical migration route.

Executed the affected source regression:

```powershell
python -m unittest discover -s tests -p test_i01*.py -v
```

This exercised **108 tests in 490.675 seconds: 107 passed and one failed** because
the legacy error changed from `Three passing` to `3 passing`. The error wording
was restored without changing admission. The failing case and four delivery/
report cases then passed together (**five tests, 24.957 seconds**). The complete
108-test command is not represented as a clean passing run. No known failure
remains; the focused rerun covers the correction and final counts-only report.
The three delivery tests exercise both finite notebook flows, actual exposed
input inventory and exact packet-world binding (including tamper rejection),
and a real assisted operator opening/inspecting/exporting with zero model calls.

The final native tokenizer self-check passed after strengthening its private
source/notice extremes and adversarial histories: conservative bound
**7,634/8,192**, resident direct bound 8,704; seven literal families include
multiline, Unicode, escapes/control bytes, header imitation and large integers.
All five feedback strings use 8–17 native tokens. The actual disjointness audit
checks **56 new ordered original/revised inputs against 60 distinct exposed
inputs**, from nine sources covering Course-1…7 and the native fixture. The
source release carries the checked 28-world manifest and requires exact
regeneration, preventing an unnoticed host-RNG version change. Diagnostics
intentionally reuse qualification inputs. No binary research/model material is
added. Receipt:
[assisted-final-source-checks.json](../../notebooks/validation/i01-development/assisted-final-source-checks.json).

## Installed release and final requirement audit

Executed successfully after code/delivery commit
`d95bb01223590bb889d4612199662266ce78968d`:

```powershell
python scripts/build_i01_course_release.py --assisted --output dist/i01-course-assisted
python scripts/verify_i01_course_release.py --assisted
```

The source-only ZIP is **896,376 bytes**, SHA-256
`35cce02abbbf8c8b2e91675c605f047f5d291eaabc8d81a9ec8e5beb10252d13`.
It has 111 inventoried source members, one matching wheel, both identical
unexecuted 37-cell notebooks and the checked 28-world input proof. The upload
directory contains only `i01-source.zip`. Weights, dependency binaries and
research PDFs are excluded. The packet's source/progress snapshots precede
this installed receipt; this final evidence/handoff does not rebuild it.

The [installed receipt](../../notebooks/validation/i01-development/assisted-release-review.json)
passes: archive/member integrity, deterministic notebook contents, ZIP/extracted
bootstrap and finite reruns, wrong-packet/stale-import rejection, all installed
package bytes matching the source, isolated outside-checkout CLI initialization,
status, CPU self-check and no-plot report without optional dependencies, exact
installed portable export/restore and complete source capture. The installed
restore explicitly confirms neither `torch` nor `transformers` was imported.
Notebook stage execution in this verifier uses a recording stub; the separate
source workflow tests use CPU scripted workers. Neither is model inference.

The final audit inspected the actual implementation, named checks and delivered
artifacts against the design, annex §§1–8 and adopted specification §12.1:

| Requirement | Implemented surfaces | Evidence inspected / result |
|---|---|---|
| A01: scoped adoption and legacy boundaries | Specification §12.1; new explicit config/regime | `7a71783`; specification diff is a 95-line addition, with no removals; earlier regimes/default config preserved |
| A02: population, 28 inputs, owner counters, seeds and joint assignment | `core.manifests`, `make_world`, `check_disjoint_inputs`; `checks.input_separation`; initialization/release | Core truth/regeneration/balance/overlap tests; actual nine-source audit, exact packet regeneration and tamper rejection; release contains all 28 checked worlds |
| A03: exact instructions, renderer, privacy, native limits | `core.messages`, `permitted_view`; explicit `inference.prepare` regime | Exact-annex text and literal/private-view tests; final native conservative bound 7,634 plus seven adversarial literal families; installed bytes match |
| A04: strict action effects, source boundary and independent siblings | Existing validator/scheduler with assisted history lengths | Legal three-call exchange, rejected message-plus-wait/empty actions, finality, waiting and literal-history checks; full scripted workflow and exact portable replay |
| A05: public-only feedback | `policy.outcome_feedback`, `core.rejection_feedback` | Priority/public-rule tests and exact five strings; actual native lengths 8–17, all ≤32; ordinary invalid actions remain charged with no delivery |
| A06: four declared diagnostic requests | Fixture/predicate constructors and finite workflow/report rows | Reachable private views and expected-value privacy tests; scripted history has no fabricated model attempts; nonpasses do not veto main |
| A07: complete pilots, exact gate, fixed candidate | `policy.pilot_usefulness`; plan, pilot, scope evidence and main admission | Full 480-call fixture passes at 3/4 originals and 7/8 controls despite 288 rejected recovery actions; 2/4 or 6/8 fails; failed usefulness collects all pilots and leaves main unknown |
| A08: 480/20/500, retries/reloads/resume/unknowns | Existing admission owner/stores and workflow | Joint-cap tests reach exactly 480 ordinary +20 reserve and reject excess; unknown-tail block; two eight-call reload cycles, no scientific regeneration; zero-call saved-stage replay and exact ZIP/extracted restore |
| A09: exact forecast and finite clock/export behavior | Forecast, resource admission, current-load checks and finite actions | Formula inspected against annex §4.3; maximum ordinary-call cost/current-session export accounting; precommit/fixed-clock and pending-raw tests; exactly two pilot exports; per-dispatch guards retained |
| A10: exact cohort analysis, unknowns, costs, bootstrap and cases | Read-only report, process tables and deterministic casebook | Hand-scored pairs/bounds/coverage; missing costs stay unknown; paired whole-world seeded order/indices, degeneracy and counts-only subgroup; exact six-category selection and eight figure pairs |
| A11: honest UI/trace/qualification displays | Existing operator/Study and report inspection | Real zero-model operator opens, inspects eight controls/four diagnostics, verifies export and closes; full raw conversation rendering and explicit intended/unknown coverage remain |
| A12: complete thin delivery | Explicit CLI flag; 37 finite cells; source builder/verifier | Both legacy 33/new 37 recording-stub scopes pass; installed source/wheel/CLI/report/self-check, source-bound bootstrap and exact portable restore pass |
| A13: historical/thesis/legacy preservation | Explicit new regime, unchanged defaults and preserved artifacts | Final baseline comparison: 2,293 protected initial files unchanged; only 22 named task-owned initial files differ; current legacy Course-7 analysis exactly equals saved JSON; reviewed migration and negative source guards pass |
| A14: proportionate verification | Existing unittest/native/self-check/delivery paths | The source run's single wording failure and focused correction are recorded above; all 24 assisted test cases are covered within the affected suite; native and installed checks pass; unrelated thesis/GPU checks not repeated |
| A15: documentation, release evidence and final audit | README, runbook, living handoff/WBS, this evidence/checklist | Named packet/receipts, local-link and consistency checks, final preservation/source binding receipt and logical checkpoint commits; no software requirement left pending |

Machine-readable preservation and packet binding:
[assisted-final-audit.json](../../notebooks/validation/i01-development/assisted-final-audit.json).
All current scientific source files and both notebooks were compared directly
with the verified ZIP. The initial preservation inventory covers 2,315 tracked
or visible untracked files; ignored caches/builds are outside it. The changed
initial files are the explicit authorized specification/handoff, I-01 package,
current notebook and delivery surfaces. Course-7, older releases, thesis source,
legacy config and the original design/research documents remain byte-identical.
The separate untracked approval-decision document from the intervening design
review is preserved and not staged in this implementation handoff.

**Software completion does not imply experimental completion.** Actual T4
loading, current-load A/B/A/headroom/finite-score/latency evidence, eight real
scalar controls, four diagnostics, four pilots and twenty main worlds remain
unrun for this new condition. They require separate execution authorization and
their own actual-host gates. Provider allocation/release, GPU utilization and
external download completion remain unknown until actually observed. No agent
performance improvement or retain/clear effect is claimed.
