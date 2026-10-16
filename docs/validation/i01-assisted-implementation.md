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

## Remaining work

Connect eight-control qualification and four diagnostics to the live workflow;
implement four-pilot objective admission, current-load requalification and the
exact forecast; complete all read-only statistics/process/casebook displays,
UI/CLI/notebook/release delivery and exposed-input audit. Verify the scripted
full workflow, exact portable resume, installed source/wheel and legacy analysis
before the requirement-by-requirement completion audit. Actual-host/model gates
remain separately authorized future work.
