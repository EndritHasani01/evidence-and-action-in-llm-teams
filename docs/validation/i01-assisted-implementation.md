# Assisted I-01 implementation evidence

16 October 2026. Implementation in progress under
[specification §12.1](../../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026).
The [requirement checklist](../plans/i01-assisted-implementation-progress.md)
distinguishes completed checks from remaining work. No model is loaded and no
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

## Remaining work

Build and verify the source-only installed release, then complete preservation
and the requirement-by-requirement audit. Actual-host/model gates remain
separately authorized future work.
