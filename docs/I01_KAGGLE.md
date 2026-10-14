# I-01 Kaggle: repaired ordinary-cell workflow

Run one named stage cell at a time. There are 26 code cells and no widget forms
or action buttons. **Run All / Save & Run All can execute inference and is not a
supported research execution method.** Successful stages start no later stage.

The saved course-1 notebook completed pinned setup, controller attachment,
native self-check and verified weight retrieval, then refused missing session
facts before model loading. Its original files remain unchanged. See the
[audit proposal](proposals/i01-course-1-complete-fix-proposal.md) and
[repair evidence](validation/i01-course-1-repair.md). Actual T4 model qualification,
pilots, freeze and main remain operator stages; no GPU inference ran during repair.

## First execution of this repair

1. Upload **dist/i01-course/i01-source.zip** as a private Kaggle dataset and
   attach it. Upload the matching **notebooks/i01_course_kaggle.ipynb**. Select
   Internet on and GPU T4 x2. Replace old source attachments or choose the exact
   SOURCE_BUNDLE when multiple candidates remain. Restart the kernel after
   replacing source; cached foreign imports are refused.
2. Run Configure and inspect the workspace with START_MODE = "new" and
   RUN_DIR = "/kaggle/working/i01-repaired-study" for a fresh repaired study.
   The earlier i01-study stays preserved. Do not rewrite its source binding.
   Changing an attached destination requires finishing and restarting, rather
   than silently switching study objects.
3. Separately run Install the pinned runtime, Open the study and Check the
   implementation. Existing release commit labels distinguish venvs/setup
   receipts, preserving old environments while sharing the verified HF/pip
   caches. No ensurepip, kernel package replacement, unpinned upgrade, weight
   loading or generation occurs here. Startup records prove isolated prefixes,
   ordinary wheel paths and disabled host startup hooks.
4. Run Download verified weights. Reuse/verify the exact pinned native files;
   bounded transport retries preserve partial bytes. Its new checkpoint includes
   the verification receipt, not model weights. Loading/downloads are not LLM calls.
5. In **Record this session window**, replace SESSION_REMAINING_MINUTES = None
   with the actual remaining minutes observed in this Kaggle session, and fill
   SESSION_ALLOWANCE_EVIDENCE with actual provider allowance evidence. Run that
   cell. It records a fixed UTC deadline; rerunning the same duration does not
   extend it. An absolute deadline alternative appears below. No quota is guessed.
6. Run Load both T4 workers. It uses the current recorded window and verified
   local snapshot, verifies both physical UUIDs, and keeps replicas resident.
   No hidden warmup. Loads/calls retain bounded termination and export margins.
7. Run Check fresh-state readiness: six counted A/B/A calls. Finite/cache defects
   block work. Unequal repeated replies require explicit review of saved tokens
   and cache evidence through study.record_state_review(notes) before
   qualification. No extra samples or changed decoding settings.
8. Run direct competence: twelve controls, at least 11/12 correct and zero
   malformed/truncated actions. Inspect qualification. Skip thinking if direct
   passed; only a documented competence limitation without protocol defects
   permits its twelve-control screen. No automatic fallback or extra model.
9. Run selected-mode headroom: two full-input/full-output probes, at least
   1.5 GiB measured free headroom per T4. Output forcing is diagnostic only.
10. Run pilot 1 only, inspect complete conversations/outcomes/costs, and download
    its checkpoint. Record actual communication/usability findings and notes.
    Repeat separately for pilots 2 and 3, at most twenty first attempts each.
    Original teams/controls and useful communication must pass; recovery effect
    direction alone is not a gate.
11. Review configuration and measured forecast, explicitly freeze with notes,
    and download the pre-main archive. Prepare a fixed one/two-world main batch,
    run/resume only it, inspect/download/acknowledge it, then repeat the three
    batch cells only by choice. Completed-scope reruns produce zero model calls.
12. Build the final or partial report; save/verify the final archive. Download
    archive and executed notebook outside Kaggle **without Save & Run All**.
    Finish the session to close models/controller, then stop Kaggle through its
    UI. Process exit does not establish provider deallocation.

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

Pinned runtime/model/scientific settings remain unchanged. I-01 runs through a
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

The course-1 source packet is preserved locally at dist/i01-course-659c056abfd1/;
the earlier packet is at dist/i01-course-4db263ea25c8/. Restore old studies only
with their matching source. This is a fresh repair release, not a migration of
populated/frozen studies. Reconcile any unseen later tail before claiming zero
spending; an older archive is not proof that nothing happened afterward.

## Accounting, archives and reports

Hard admission is 500 new physical model attempts with 28 shared contingency.
Diagnostics, warmups if any, failures and eligible retries all count; loads and
downloads do not. Planned first attempts are 460 direct-only or 472 with the
conditional thinking screen: at most 380 main, 60 pilot, twelve controls per
mode and eight hardware/state diagnostics. Historical 45 stay separate. Unused
capacity adds no worlds. One identical infrastructure retry requires no durable
raw outcome and confirmed prior termination. Wrong/malformed/truncated answers
and recorded timeouts never retry.

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
| reports/*.csv | Worlds, paired results/costs, attempts, policy costs, failures, annotations and plotting data |
| reports/figures/*.svg, *.png | Accuracy, principal effort, calls/tokens, failure and coverage figures |
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
New/replaced replicas require two contingency probes bound to actual load IDs:

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
qualification/resources/evidence cannot satisfy the original gates.
