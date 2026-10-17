# I-01 assisted-v2: fixed campaign and current delivery

The current implementation follows
[specification §12.1](../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026)
and the approved [design](plans/i01-course-final-experimental-design.md) /
[exact annex](plans/i01-course-final-design-protocol-and-acceptance.md).
Implementation and CPU checks are authorized. **Actual GPU inference and
experimental execution require a separate explicit request.** No actual-host
or agent-performance result is established by the new software.

The assisted source-only delivery is `dist/i01-course-assisted/`. Both notebook
names contain the same complete **37 finite code cells**. The legacy builder
default still generates the original 33-cell recorded-outcome flow; its
configuration, reports and historical release/run directories remain separate.

The packet at source `d95bb01223590bb889d4612199662266ce78968d` passes the
[installed review](../notebooks/validation/i01-development/assisted-release-review.json):
896,376 bytes, SHA-256
`35cce02abbbf8c8b2e91675c605f047f5d291eaabc8d81a9ec8e5beb10252d13`.
Its bundled progress documents are snapshots taken before installed verification;
the [final evidence and audit](validation/i01-assisted-implementation.md#installed-release-and-final-requirement-audit)
record completion afterward without changing the verified source packet.

## Build and verify on CPU

```powershell
python scripts/build_i01_course_notebook.py --assisted
python scripts/build_i01_course_release.py --assisted --output dist/i01-course-assisted
python scripts/verify_i01_course_release.py --assisted
```

These commands package and check source/wheel/notebook/empty-store behavior.
They do not load weights, run qualification or execute a research experiment.
The source packet contains its checked 28-world input manifest and a receipt
identifying the locally available historical inputs checked for exact overlap.
Initialization/self-check require exact regeneration of those checked worlds;
the runtime must not quietly generate another set under the same seed labels.
Paper PDFs and model/dependency binaries are not included.

## First execution, only after separate authorization

1. Use a fresh online T4 x2 Kaggle session. Upload either generated notebook and
   attach only `dist/i01-course-assisted/kaggle-input/i01-source.zip` as a private
   source dataset. The notebook accepts the assisted-policy source packet;
   another condition or cached imported source is rejected.
2. Review `RUN_DIR=/kaggle/working/i01-assisted-study`, actual remaining GPU
   allowance and the fixed session window. The default 700 minutes is an
   operator planning estimate, not a verified provider entitlement. Installation,
   downloads and inspection use the same clock; cell reruns cannot extend it.
3. An authorized Run All locks the fixed candidate before its first model call,
   performs six state checks, eight legal scalar controls and two full envelopes,
   then four single-call diagnostics and a verified preparation checkpoint.
   Probe nonpasses are diagnostic; they do not select a different candidate.
4. All four balanced pilots run once, each with a natural original, both literal
   siblings and original/revised scalar controls. Ordinary mistakes remain
   outcomes. Main eligibility requires complete committed/effect/accounting/export
   evidence, at least 3/4 correct original teams, at least 7/8 correct pilot controls,
   current health and an adequate measured resource forecast. There is no
   recovery-success, effect-direction or qualitative-message veto.
5. On eligibility, the ten numbered batches execute all twenty fixed worlds.
   Same-device worlds serialize; different devices may overlap. Ordinary main
   failures do not replace worlds or stop later batches. Real health, source,
   storage, unresolved-spending or resource faults stop dispatch and preserve
   truthful partial evidence.
6. Download `i01-assisted-study/exports/latest.zip`, reports and the executed
   notebook. Export follows each pilot/batch and settled error; weights remain
   resident through reporting and close after final export. Actual process exit
   is reported separately from unknown provider deallocation/download completion.

The whole campaign is capped at **480 ordinary +20 contingency =500 physical
attempts**: hardware/state 8, scalar qualification 8, diagnostics 4, pilots 80,
main 380. Early terminal episodes save attempts without enlarging another stage.
Known wrong/invalid/truncated/timeout outcomes never retry. Eligible identical
pre-outcome infrastructure retry and new-load qualification consume reserve.
Course-7's unused allowance and a renamed directory provide no new authority.

If usefulness fails, the report says `feasibility_complete`, main stays wholly
unknown, and workers close after settled export. A partial integrity/resource
stop remains partial. Neither outcome licenses prompt tuning or another cohort.
All four pilot checks concern durable scopes; the distinct main decision applies
the numerical usefulness thresholds. Four pilots do not certify reliability.

## Inspect, resume and review

Use `study.inspect(..., audit_limit=None)` for all raw calls. Eight qualification
controls, four diagnostic predicates, four pilot scopes, physical and logical
validity denominators, unknown cost coverage and the deterministic casebook are
visible in the report/UI. Both arm rates and the all-world paired contrast stay
primary; correct-prefix results are descriptive counts only. Human review is
pending unless actually recorded. Optional `reviewer=` on `study.annotate(...)`
records a supplied identity, not independent coding or causal attribution.

Restore only this campaign's exact portable checkpoint and source. Construct
`Study(source_root, run=RUN_DIR, assisted=True)`, use the existing explicit
restore/reopen commands with actual exit/tail evidence, and set a new session's
actual time window. Unknown additional spending blocks continuation until
reconciled. A new loaded pair requires **six state checks plus two envelopes**,
all charged to reserve: after loading use `study.check_headroom(reload=True)`.
Completed scalar/diagnostic/pilot/main outcomes do not regenerate. Two full
eight-call reload cycles fit the reserve only if other spending permits them.
No Course-3/7 migration, prior-result import, implicit fresh campaign, relaxed
gate or model fallback is selected for assisted-v2. Preserve existing outputs
without rerunning inference merely to save them.

Read [implementation evidence](validation/i01-assisted-implementation.md) and
the [requirement checklist](plans/i01-assisted-implementation-progress.md) for
verified status and remaining actual-host gates.

## Legacy v1 runbook (historical condition)

The following instructions describe `i01-course-v1` and its preserved
recorded-outcome packet. Its counts, policies and paths do not govern assisted-v2.

# I-01: the entire experiment with Run All

The current delivery is one complete 33-cell notebook. Both
**i01_course_kaggle.ipynb** and **i01_course_research.ipynb** contain identical
end-to-end content. The earlier preparation-only and manual-approval notebooks
remain in their historical release directories. No course-2/3/4/5 result is imported.

## First execution

1. Upload **dist/i01-course-outcomes-run-all/i01_course_kaggle.ipynb** to a fresh Kaggle
   notebook. The research filename works identically; you need only one.
2. Create one private dataset from **dist/i01-course-outcomes-run-all/kaggle-input/**,
   containing only **i01-source.zip**, and attach it. Select **GPU T4 x2** and
   enable Internet. Remove old active source datasets; restart the kernel when
   replacing an already imported source release. Only a matching whole-study
   source packet is accepted, including ZIP or Kaggle-expanded roots.
3. Check the first cell. It defaults to `/kaggle/working/i01-outcomes-study` and
   a **700-minute fresh-session planning window**, leaving twenty minutes against
   your approximately twelve-hour maximum. The evidence note explicitly says
   provider allowance/deadline is unverified. Reduce the minutes to actual time
   left if the session is already running or the provider shows a lower bound;
   check account GPU allowance. Do not use a previous session's deadline.
4. Press **Run All**. Setup/source/native checks, verified weights, two resident
   workers, plan locking, readiness, direct qualification and headroom run first.
   Then all three pilots and their objective checks run, followed by automatic
   measured main admission, all ten fixed two-world main batches, full reporting,
   verified checkpoint export and worker/controller shutdown. No forms, review
   placeholders, freeze-note fields, batch acknowledgements or further Run clicks.
5. Download **/kaggle/working/i01-outcomes-study/exports/latest.zip**, reports and
   the executed notebook using the displayed links. Save the existing output;
   do not schedule another inference run solely to save it. Stop Kaggle through
   its UI to release the allocation. Process closure cannot prove deallocation
   or that an external download succeeded.

## What advances and what stops

The configuration, inputs, seeds/schedule, source/prompt implementation, direct
settings, endpoints and rubric are bound before the first model call. Pilots
cannot tune them. Mathematical mistakes never select qualification/pilot/main
worlds or trigger an accuracy cutoff. Direct qualification still requires twelve
committed, protocol-valid controls. Readiness/headroom and strict isolation gates
remain. Thinking is not selected and there is no model fallback.

Each pilot requires terminal prefix/retain/clear and both controls, committed
raw/effects, reconciled spending, intact runtime and inspectable exports. After
the fixed twelve-control scalar qualification, ordinary prefix, recovery and
later pilot-control wrong/invalid/truncated/framing replies and terminal
noncompletion are measured outcomes. Original-team completion and legal-action
counts are diagnostics, not admission vetoes. Invalid actions still deliver
nothing and consume a turn. The policy is
`i01-recorded-outcomes-run-all-2026-10-15`; historical strict/recovery-only plans
keep their original meaning. Source/privacy/backend/cache/numerical faults,
unknown termination/spending and inadequate resources still block. Message
quality and mechanisms remain **retrospective review pending**.

All three pilots must pass before automatic main resource admission. The measured
attempt/time forecast, including remaining work and checkpoint overhead, must fit the unchanged settings and configured deadline.
The notebook then runs all twenty predetermined main worlds in ten numbered
batches, one world per logical slot. Wrong/malformed/truncated recorded main
replies remain measured outcomes; real runtime, unresolved evidence, storage,
source or resource failures stop. A failed guard attempts a settled partial report/export, then bounded closure of both workers with actual acknowledgements. Cleanup failure remains explicit; the latest valid archive is preserved. A successful error snapshot does not clear a blocked scientific gate. No success/effect-dependent selection or replacement.

Every numbered cell requests its own finite scope. Repeating a completed pilot
or batch makes zero new model calls and cannot advance the next scope. Rerunning
window configuration keeps the same deadline. Setup/download time consumes that
window. A full Run All is an execution request, not a completion-time guarantee;
a provider may terminate earlier and account quota remains external.

## Spending, progress and exports

This explicitly independent study starts at 0/500, with unchanged 28-attempt
contingency. At most 460 direct first attempts are planned: twenty preparation,
sixty pilot and 380 main. Early terminal phases use fewer calls. The unused
thinking allocation does not add reserve/worlds. Diagnostics, failed calls,
eligible retries, restores and reload probes remain spent. Previous studies are
preserved historical evidence, never silently imported or pooled.

Progress shows call/world/phase/slot, physical spending, action outcomes and
checkpoints. `validation_details.csv` and `protocol_compliance.csv` separate syntax, schema and legal-action compliance by phase; invalid raw calls appear first in inspection. The original clock timestamp/minutes/estimate basis survives setup. Forecasts distinguish the original main-only calculation from remaining pilot/main work and measured export overhead; neither guarantees provider duration. Models remain resident through inspection and research stages.
Each pilot shows its complete conversation and cumulative archive; every main
batch displays its exact worlds, results and cumulative archive. Every settled
error also attempts export. Checkpoints require no clicks and are not disabled
when you ignore download links. Do not delete them to make the interface simpler.

Reports include all twenty intended worlds, paired outcomes and unknown bounds,
world-bootstrap uncertainty, costs, failures, qualification/control tables,
objective pilot checks, all escaped conversations/raw calls and eight SVG/PNG
figure pairs. `pilot_checks.csv` separates objective admission from pending human
communication findings. Exact source/wheel, canonical SQLite backups, settings,
inputs, plan/admission receipts and raw outcomes travel with the checkpoint.

## Later recovery and retrospective inspection

A convenient restore interface is not part of the normal Run All flow; the
existing explicit primitives below remain implemented. If a later failure occurs,
use the latest saved checkpoint with its exact source. No missing bytes or unknown
tail is silently assumed zero; external preservation still requires a download.
For an interrupted stage, resume its exact numbered cell. New replicas after an
accepted envelope require two separately charged reload probes. Never repeat a
completed screen or reset the study to bypass a failed prerequisite.

After completion, `study.build_report()` and `study.inspect(audit_limit=None)`
work from intact files without reloading models. Inspect pilot/main conversations
and record real human rubric annotations with exact call references; automatic
checks do not establish meaningful communication or any favorable scientific
mechanism. Adding a review never changes the prespecified primary population.

The [course-6 repair evidence](validation/i01-course-6-repair.md)
distinguishes observed course-6 preparation/pilot behavior from this newly
implemented broader admission policy. No course-6 migration or prompt/feedback
change is selected; this new study starts at zero with its own unchanged ceiling. Target Kaggle pilot/main execution remains unverified.

## Explicit session commands

The first cell uses the explicitly labelled 700-minute planning estimate. For a genuinely observed current deadline, use:

```python
study.configure_session(
    deadline="ACTUAL-FUTURE-ISO-TIME-WITH-UTC-OFFSET",
    evidence="Actual current Kaggle allowance evidence"
)
```

Replace the placeholder with an actual time. Earlier illustrative times/quotas
are not current-session evidence. After a fresh provider observation only:

```python
study.configure_session(remaining_minutes=ACTUAL_CURRENT_MINUTES,
    evidence="Actual fresh observation", refresh=True)
```

The original study.set_session_window(deadline, evidence) remains available.
A new controller never automatically reuses the previous controller's window.
Opening/inspection/reporting can precede a window; model loading/admission cannot.
The configured load/direct/thinking bounds are 600/180/900 seconds, with bounded
cleanup and 120 seconds reserved for export. The 500-call ceiling is separate
from provider time. Idle inspection and setup also consume allocated resources;
actual quota units/boundaries must come from the active account.

## Runtime and source preservation

Model/runtime, inputs, prompts, decoding, limits and exact scoring remain unchanged; protocol/pilot admission and the explicitly independent rerun are adopted in specification section 12. I-01 runs through a
stdlib-only -I -S -X utf8 entry, explicitly restores Python 3.13 venv prefixes,
and adds normal verified wheel directories without processing sitecustomize or
.pth hooks. Spawned residents restore the same prefixes; plotting selects Agg
before import. No wrapt or inline-renderer dependency is added. Setup receipts
record actual paths/hook origins and recheck cached package/source inventory.

New releases use /kaggle/temp/i01/i01-venv-<source-head> and
/kaggle/working/i01-setup-<source-head>. The shared HF cache stays at
/kaggle/temp/i01/hf-cache. Completed mismatching environments are refused;
matching ones are checked and reused without reinstalling. Logs append.
Source caches use /kaggle/working/i01-source-<source-head>.

The completed continuation delivery is preserved at dist/i01-course-0f600584dc10/. The original 8f5bcdb delivery is preserved locally at dist/i01-course-8f5bcdb661a1/; course-1 packets remain at dist/i01-course-659c056abfd1/ and dist/i01-course-4db263ea25c8/. Ordinary reopen/restore keeps exact active-source binding. Only the reviewed pre-main 8f5bcdb transition is supported; frozen/experimental runs and unreviewed scientific/runtime differences are refused. The repaired checkpoint retains source/ as original and source/continuation/ as active, including their wheels. The persistence-version tag changes only through this
explicit transition and prevents old runtime code from writing a repaired study;
original source and scientific rows stay intact. Never overwrite old source/manifest bytes or assume a ZIP proves no later spending.

## Accounting, archives and reports

Hard admission for the fresh study is 500 physical attempts with 28 shared
contingency attempts. First-attempt ceilings remain 380 main, 60 pilot, twelve
direct controls and eight hardware/state calls; no thinking is selected.
Direct-only first attempts total at most 460, plus at most 28 contingency.
The preparation stages consume up to twenty of those 460, not an extra pool.
All failures/diagnostics and eligible retries count. Loads/downloads do not.
A retry requires no durable outcome and confirmed prior process termination;
wrong/malformed/truncated replies and recorded timeouts never retry. Global
runtime faults stop; ordinary invalid team actions consume their bounded turn.
Restores retain all calls, charges and lost-spending uncertainty. Prior-campaign
continuation, when explicitly selected instead, still preserves its verified
41 calls and eighteen reserve charges; the independent path never mutates it.

Two explicitly named WAL/FULL canonical DBs own inputs, raw results, effects and
spending. Missing/corrupt/incomplete existing DBs refuse before writers open;
new initialization publishes a complete pair atomically. Reports do not create
workers, repair answers or infer missing outcomes. Periodic checkpoints occur
at the next settled boundary after five minutes, including controls/diagnostics.
Active calls must settle first. Each world/pilot/action and successful setup,
download/window change has a cumulative checkpoint. Failure export preserves
the last good ZIP and shows its true older boundary if a new export fails.

Download under the exact RUN_DIR:

| Artifact | Meaning |
|---|---|
| exports/latest.zip | Verified source/wheel/configuration, manifest, both DB snapshots, receipts and reports; no weights/venvs/caches/credentials |
| reports/overview.html, overview.md, analysis.json | Complete or partial intended-population results, costs, gates, unknowns and limitations |
| reports/conversations.html, .txt, .jsonl | All call/phase evidence, raw tokens/thinking and private evaluator audit |
| reports/*.csv | Qualification controls by mode, worlds, paired results/costs, attempts, policy costs, trace-linked failures, annotations and plotting data |
| reports/figures/*.svg, *.png | Qualification coverage/effort plus main outcomes, principal effort, calls/tokens, failures and coverage; unexecuted main is not zero effect |
| receipts/operator-errors.jsonl, stage-error.json | Full operational cause/traceback; expected notebook failures remain concise |

study.inspect(world=..., phase=..., agent=..., audit_limit=None) displays all
saved audits. Empty exports explain that no calls exist. Inspection remains
available after controller loss, with live state marked unavailable. Private
truth, partner submissions and thinking never enter peer prompts. Unknown
unexecuted episodes remain unknown; recorded terminal failures score zero;
complete-case summaries never replace twenty intended worlds.

If links are unsupported, download exact files via Kaggle Output/Files. A link
or review acknowledgement does not prove download or human understanding. Save
the executed notebook separately and retain external archives.

## Pause, restore and replica replacement

```python
study.show_status()
study.pause()  # Request: an admitted call may still be running.
# After settlement or confirmed bounded termination:
study.save_checkpoint(verify=True)
```

For intact files after kernel restart, attach matching source and use `study.open("reopen")` with the exact run destination. Rerun workspace/setup as needed. Current Run All cells do not expose a START_MODE form. The ownership lock refuses a second live owner. For a selected archive, construct Study with a fresh run destination and use `study.open("restore", selected=EXACT_CHECKPOINT, tail="latest", evidence="Actual prior exit/no-later-generation evidence")`; use tail="unknown" when appropriate. ZIP and expanded
roots work. No archive timestamp guessing or implicit new study when missing.
An already restored destination requires the explicit reopen route.

Record a fresh actual window, reuse/verify weights and load both workers. An
accepted study need not repeat readiness/qualification merely for restore.
After an accepted envelope, new/replaced replicas require two contingency probes bound to actual load IDs. If none exists in this study, first use study.check_headroom() for its two ordinary probes. For a replacement after acceptance:

```python
study.check_headroom(reload=True)
study.run_main_batch()  # Only for an already saved interrupted main scope.
```

Each distinct replacement pair receives new probe IDs even within one controller;
unchanged-pair reruns reuse durable probes with zero calls. Completed research
calls reuse raw outputs/effects. Notebook interrupt is a pause request, not exit
proof. After observed prior process/session exit, reconcile exact identifiers:

```python
study.reconcile_attempt(slot=SLOT, attempt=EXACT_ATTEMPT_ID,
    evidence={"termination_confirmed": True, "reason": "Actual observed exit"})
study.confirm_timeout_termination(slot=SLOT, call=EXACT_CALL_ID,
    evidence={"termination_confirmed": True, "reason": "Actual observed exit"})
study.record_lost_spending(
    {"resolved": False, "upper": None, "evidence": "Actual unknown-tail facts"},
    affected_worlds=EXACT_AFFECTED_WORLD_IDS)
```

Unknown spending is not zero. A known timeout consumes attempt/turn and never
retries. Missing DBs require verified complete restore or explicit evidence
handling, never an empty recreated ledger. Report honest partial coverage if
protocol/resources/evidence cannot satisfy the adopted gates.

For an unknown restored tail, bound the ADDITIONAL exposure beyond that saved
boundary after verifying old process/session exit. Earlier gap charges remain:

```python
study.resolve_restore_tail(
    upper=ACTUAL_ADDITIONAL_ATTEMPT_UPPER_BOUND,
    evidence="Actual observed prior exit and bounded additional exposure",
    affected_worlds=EXACT_AFFECTED_WORLD_IDS)
study.save_checkpoint(verify=True)
```

A positive bound needs affected worlds. A zero new tail does not erase an older
positive or unresolved gap; use honest partial reporting if older exposure still
cannot be bounded. Ordinary total-gap reconciliation cannot silently decrease
an already charged bound or remove affected-world blocks.

## Explicit-command equivalents

All scientific behavior remains in the same Python modules. For zero-model
preparation outside a notebook, use the current source and its isolated runtime:

```text
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION init --independent
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION status
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION report --output REPORT_DIRECTORY
```

This explicit independent init never imports an old checkpoint. The optional
historical command `continue-checkpoint COURSE3_CHECKPOINT --prior COURSE2_CHECKPOINT
--tail latest --evidence "Actual exit/boundary evidence"` instead preserves that
old campaign's calls and reserve charge; it is not part of the fresh workflow.
Use --tail unknown when appropriate; the evidence must describe actual facts.
For resident inference the notebook's named Study methods keep the controller
and replicas alive; one-shot CLI actions close them by design. For later
reconstruction, CURRENT_SOURCE is the verified repaired packet (or the preserved
source/continuation/ in its checkpoint), not the historical source/ at the root.

For a small CPU environment without Matplotlib, append --no-plots to report.
This still exports complete tables/traces/HTML; use the default report in the
pinned Kaggle runtime to include all eight SVG/PNG figure pairs.
