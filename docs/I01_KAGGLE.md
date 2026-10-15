# I-01 Kaggle: repaired direct-mode continuation

Use [notebooks/i01_course_kaggle.ipynb](../notebooks/i01_course_kaggle.ipynb) with
[dist/i01-course/i01-source.zip](../dist/i01-course/i01-source.zip). The notebook
has 26 ordinary code cells, zero widget forms/buttons and no automatic later
stage. **Do not use Run All / Save & Run All**: those commands can execute
multiple inference stages.

The adopted 15 October amendment uses direct/nonthinking with protocol-first
qualification. All twelve direct controls remain valid and 10/12 mathematically
correct; the old 11/12 failure stays in history. Thinking remains five diagnostic
attempts: four correct finals, one unfinished 4,096-token reply, seven unexecuted.
Mathematical mistakes are outcomes in qualification and pilots; runtime,
protocol, communication, resource and evidence prerequisites remain strict.
See [repair evidence](validation/i01-course-3-repair.md) and
[specification section 12](../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
No model inference is performed while building or checking this repair.

## First execution: continue course-3 without resampling

1. Create ONE private Kaggle dataset from the three files in
   **dist/i01-course/kaggle-input/**: i01-source.zip, course-3-latest.zip and
   course-2-latest.zip. Attach that dataset to the matching uploaded notebook.
   These are the new source and exact original checkpoint bytes with unique
   filenames. Kaggle-expanded roots and identical ZIP/expanded copies work. Select Internet on and **GPU T4 x2**.
   Restart the kernel after replacing source attachments; remove stale active
   source attachments or set SOURCE_BUNDLE explicitly if ambiguous. The bootstrap
   ignores the old source packets embedded inside the supplied checkpoints.
2. In Configure and inspect the workspace, keep **START_MODE = "continue"** and
   **RUN_DIR = "/kaggle/working/i01-direct-study"**. Leave RESTORE_CHECKPOINT and
   PRIOR_CHECKPOINTS as None when each exact study has one attached candidate;
   selection uses study IDs, never filenames/timestamps. If ambiguous, set the
   exact course-3 path and a one-element list containing the course-2 path.
3. Set **RESTORE_TAIL** and **RESTORE_EVIDENCE** before opening. Use "latest" only
   when no generation occurred after the supplied course-3 boundary and the old
   session/processes have ended. Write your actual evidence. For example, only
   if true: "I stopped the old session after the saved headroom refusal; no
   generation followed the checkpoint." If uncertain, use "unknown" and say so;
   reporting remains available, but loading/admission wait for reconciliation.
   The notebook cannot determine this provider/session fact from a ZIP alone.
4. Run workspace, Install the pinned runtime, then Continue the saved study.
   This is a zero-model preparation step. It preserves the course-3 study ID,
   original manifest/source, 23 physical calls, states and old failed gates. It
   adds the active source/policy transition, narrowly adjudicates the normal-cap
   misclassification and imports course-2's verified eighteen-call reserve charge.
   Expected status: **23 local / 41 campaign attempts, 18/28 reserve used,
   459 arithmetic remaining** before other exposure. Download this checkpoint.
5. Run Check the implementation and Download verified weights. Setup, native
   checks, metadata/weights and source validation do not generate model outputs.
   The pinned runtime and HF/pip caches are reused where valid; old environments
   are preserved. No ensurepip, host startup hooks or unpinned upgrades are used.
6. In Record this session window, enter the CURRENT actual remaining minutes and
   actual allowance evidence observed in Kaggle. Rerunning keeps a fixed deadline;
   it does not grant another twelve hours. Loading is the separate next cell.
7. Run Load both T4 workers. Inspect its concise device/load evidence; complete
   tensor inventories remain in sessions.csv/checkpoints. The known optional
   recurrent-kernel fallback and documentation/deprecation diagnostics are
   explained; raw logs remain available. Models stay resident during inspection.
8. Run readiness and direct protocol qualification. Existing six/twelve calls
   are reused with **zero new model attempts**. Direct is eligible under the new
   protocol policy and still 10/12 mathematically correct. Inspect qualification;
   optional thinking history is read-only and may be skipped. Do not complete
   its seven missing controls or manually edit a saved pass/defect flag.
9. Run direct headroom with **study.check_headroom()**. No envelope previously
   ran, so these are TWO ordinary 8,192-input/512-output probes, not reload
   contingency. Each T4 must retain at least 1.5 GiB measured free headroom.
   Expected campaign count after successful first attempts: 43. For later
   replacement loads after an accepted envelope use reload=True instead.
10. Run pilot 1 only; inspect the complete conversation, exact outcomes/costs and
    download its checkpoint. Enter actual communication/usability findings and
    trace-based notes. Repeat separately for pilots 2 and 3. Wrong mathematical
    answers alone do not reject a pilot. Invalid protocol, missing evidence,
    useless communication or an inadequate resource forecast still block main.
11. Review configuration/forecast, freeze explicitly with actual notes, then
    prepare/run/review the fixed one/two-world main batches. Each cell requests
    only that bounded stage; review/download before preparing the next batch.
    All twenty worlds remain in the primary population regardless of prefix or
    control correctness. A passed gate does not itself authorize later execution.
12. Build the final/partial report, save and verify the archive, and download the
    archive and executed notebook outside Kaggle WITHOUT Save & Run All. Finish
    the session, then stop Kaggle through its UI. Process exit alone does not
    establish provider deallocation.

Use "reopen" for intact repaired files after kernel restart, or "restore" with
an exact repaired checkpoint and fresh destination. Do not choose "new" to evade
an old gate/source mismatch: that would rerun already spent controls. A genuinely
fresh study must explicitly carry every prior preparation checkpoint through
PRIOR_CHECKPOINTS; known campaign spending is not reset by another study ID.
Both known study IDs must be reconciled. Charging all prior work to a third fresh
study can exceed the reserve and block admission; continue course-3 instead.

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

Model/runtime, inputs, prompts, decoding, limits and exact scoring remain unchanged; protocol/pilot admission and campaign reserve treatment are explicitly amended. I-01 runs through a
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

The original 8f5bcdb delivery is preserved locally at dist/i01-course-8f5bcdb661a1/; course-1 packets remain at dist/i01-course-659c056abfd1/ and dist/i01-course-4db263ea25c8/. Ordinary reopen/restore keeps exact active-source binding. Only the reviewed pre-main 8f5bcdb transition is supported; frozen/experimental runs and unreviewed scientific/runtime differences are refused. The repaired checkpoint retains source/ as original and source/continuation/ as active, including their wheels. The persistence-version tag changes only through this
explicit transition and prevents old runtime code from writing a repaired study;
original source and scientific rows stay intact. Never overwrite old source/manifest bytes or assume a ZIP proves no later spending.

## Accounting, archives and reports

Hard admission is 500 new campaign attempts and 28 shared reserve. Course-3's
23 local attempts plus eighteen verified course-2 repetitions total 41; those
eighteen are an explicit prior preparation reserve charge, not infrastructure
retries, lost calls or historical-45 spending. Ten reserve attempts remain.
At most 442 further ordinary envelope/pilot/main calls bring the known total to
483. Seventeen arithmetic slots are not seventeen usable reserve attempts;
seven belong to the unexecuted thinking scope and add no worlds/reserve.
Prior proof ZIPs are preserved under receipts/prior-studies/ and their charges
survive restoration. A failed prior-proof import blocks admission until repaired.

Local first-attempt ceilings remain 380 main, 60 pilot, twelve direct controls
and eight hardware/state calls; five historical thinking calls stay spent and
no further thinking is selected. All failures/diagnostics and eligible retries
count. Loads/downloads do not. A retry requires no durable outcome and confirmed
prior process termination; wrong/malformed/truncated replies and recorded
terminal timeouts never retry. Global/runtime faults stop; ordinary invalid
model actions consume their bounded turn and deliver nothing.

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
After an accepted envelope, new/replaced replicas require two contingency probes bound to actual load IDs. If none exists (as in course-3), first use study.check_headroom() for its two ordinary probes. For a replacement after acceptance:

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
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION continue-checkpoint COURSE3_CHECKPOINT --prior COURSE2_CHECKPOINT --tail latest --evidence "Actual no-later-generation and prior-exit evidence"
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION status
python scripts/i01_course.py --source CURRENT_SOURCE --run FRESH_DESTINATION report --output REPORT_DIRECTORY
```

Use --tail unknown if appropriate; the evidence text must describe actual facts.
For resident inference the notebook's named Study methods keep the controller
and replicas alive; one-shot CLI actions close them by design. For later
reconstruction, CURRENT_SOURCE is the verified repaired packet (or the preserved
source/continuation/ in its checkpoint), not the historical source/ at the root.

For a small CPU environment without Matplotlib, append --no-plots to report.
This still exports complete tables/traces/HTML; use the default report in the
pinned Kaggle runtime to include all eight SVG/PNG figure pairs.
