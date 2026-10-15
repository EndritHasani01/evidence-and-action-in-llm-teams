# I-01 Kaggle execution

## Fresh start with Run All

The latest user instruction replaces course-3 continuation as the default.
No previous result or checkpoint is required. The direct/nonthinking protocol
repair remains active: all twelve controls must follow the JSON/action protocol;
mathematical mistakes are reported as outcomes, without an accuracy cutoff.
No model inference is performed while building or checking this package.

1. Upload **dist/i01-course-fresh/i01_course_kaggle.ipynb** to Kaggle.
2. Make one private dataset from **dist/i01-course-fresh/kaggle-input/**. It contains
   only **i01-source.zip**. Attach it, enable Internet and select **GPU T4 x2**.
   Use a fresh Kaggle session. Do not attach course-2/course-3 checkpoints or old
   source releases. Restart the kernel after replacing an active source package.
3. In the first cell, set `SESSION_REMAINING_MINUTES` to the actual minutes left
   in the CURRENT Kaggle session, and `SESSION_ALLOWANCE_EVIDENCE` to a truthful
   note describing the current GPU allowance shown by Kaggle. Leave RUN_DIR at
   `/kaggle/working/i01-fresh-study`. No old deadline is reusable. Example values
   must not be copied as if they were your provider's observation.
4. Press **Run All**. Fourteen ordinary code cells perform configuration,
   workspace/source inspection, fixed-window recording, pinned installation,
   explicit new-study creation, native/scripted self-check, verified weights,
   loading, readiness, direct qualification, inspection, headroom, reporting and
   verified checkpoint export. No thinking, pilot, freeze or main call runs.
5. Successful first attempts total **20 here, zero prior charges**: six readiness,
   twelve direct controls and two headroom probes. Every inference has durable
   admission and raw output. Mathematical accuracy can be below 12/12; malformed,
   truncated or illegal controls still fail protocol qualification. Hardware/
   cache/provider defects, insufficient headroom and inadequate session time
   still block inference and preserve an error receipt/checkpoint.
6. Download **/kaggle/working/i01-fresh-study/exports/latest.zip**, the reports and
   executed notebook using the displayed links. Every completed action already
   offers its cumulative checkpoint. Save the output without scheduling another
   Run All solely to save it. Workers stay resident for inspection/continuation.
   When finished, `study.finish_session()` closes the controller; stop Kaggle
   through its UI to release the allocation.

The observation is recorded BEFORE installation and downloads, so their elapsed
wall time consumes the same fixed deadline. Cell reruns do not extend it. Supply
an explicit fresh observation with refresh=True only when the provider actually
shows a new remaining duration. A/B/A inequality requires trace-based human review
before qualification, not an automatic waiver or extra samples.

This is an explicitly authorized independent study with its own 500-attempt
ceiling and 28-attempt reserve. It starts with empty calls/attempts and a new
study ID. The prior 41 executions and earlier 45 remain historical evidence,
not imported results. Independent scope is stored and exported. Repeating the
new-study cell reuses that same study; it cannot clear its accounting or convert
an old campaign to an independent one. Scientific settings are unchanged.

## Complete research workflow after preparation

**i01_course_research.ipynb** contains all ordinary pilot, review, freeze,
batch, reporting, restore and shutdown stages. Its individual-stage operation
preserves the required human findings; Run All is for the preparation notebook.

To retain the current model replicas, copy the pilot 1 and review cells from the
research notebook into the successfully prepared notebook and run them with its
existing `study` object. Continue pilot 2/review, pilot 3/review, configuration
review, explicit freeze, then prepare/run/review each one/two-world main batch.
Each pilot automatically shows its complete conversation and checkpoint. Actual
useful-communication/usability findings and notes are human observations, not
inferred from mathematical accuracy. All twenty main worlds remain primary.
No research gate or condition is automatically waived or changed.

Alternatively, finish the preparation controller, download its NEW checkpoint,
and upload the full research notebook. Attach the matching new source plus that
checkpoint; set START_MODE="restore", a fresh RUN_DIR, RESTORE_CHECKPOINT and
actual RESTORE_TAIL/RESTORE_EVIDENCE. Set actual current session facts in its
session-window cell. Rerun native checks/weight verification, load the replicas,
reuse readiness/qualification without resampling, and run
set `RELOAD_HEADROOM = True` in its headroom cell for the two charged
current-load probes (`study.check_headroom(reload=True)`).
Then continue the individually reviewed research stages. A source mismatch or
unresolved tail blocks; naming a new directory never resets a restored study.

For a complete study from scratch using individual cells instead, keep the
research notebook's START_MODE="new" default. It explicitly creates an
independent study, just as the preparation notebook does. The older course-3
continuation remains an explicit CLI capability for historical reproduction;
it is not used or required by this fresh upload.

## Explicit session commands

The normal cell accepts actual observed minutes. Alternatively:

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
The preparation notebook consumes up to twenty of those 460, not an extra pool.
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

For intact files after kernel restart, attach matching source, set START_MODE
= "reopen" and preserve the exact RUN_DIR. Rerun workspace/setup as needed, then
Open the study. The ownership lock refuses a second live owner. For a selected
archive, use START_MODE = "restore", a fresh RUN_DIR, exact RESTORE_CHECKPOINT,
RESTORE_TAIL (latest or unknown) and genuine RESTORE_EVIDENCE. ZIP and expanded
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
