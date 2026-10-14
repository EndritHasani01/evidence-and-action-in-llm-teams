# I-01 Kaggle operator runbook

This is a fully implemented preparation package for the separately adopted
[I-01 scientific regime](../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
Actual Kaggle host/UI, model capability, headroom, pilots, freeze and main results
remain unverified. No GPU/model run was performed during implementation.

## First execution

1. Upload `dist/i01-course/i01-source.zip` as a **private Kaggle dataset**.
   Kaggle may expose the ZIP or expanded files. Attach it to a new notebook.
2. Upload `notebooks/i01_course_kaggle.ipynb` (also in `dist/i01-course/`).
   Select **GPU T4 ×2** and **Internet On**. Keep the study private.
3. Run N01 to select/verify the unique small source attachment and inspect the
   actual host. If several source bundles exist, set `SOURCE_BUNDLE` to one exact
   ZIP or expanded directory. A incompatible host stops; do not update pins.
4. Click N02 **Online setup**. It installs the reviewed Linux Python 3.13
   candidate in a separate venv, verifies the installed source/package lock,
   and downloads pinned metadata/tokenizer only. View logs in
   `/kaggle/working/i01-setup/`. No kernel Torch replacement or model warmup occurs.
5. In N03 explicitly choose **new**, or restore an exact saved bundle into a
   fresh writable run directory. Set the actual session deadline in UTC and
   describe the allowance seen in Kaggle's current UI. This is needed for bounded
   admission; the notebook does not invent quota, assignment or release evidence.
6. Click N04 **Lightweight self-check**. The native tokenizer and scripted
   mathematics/view/finality/storage/budget/export/restore checks must pass.
   They use temporary scripted DBs and zero model attempts.
7. Click N05 **Pinned weights**, then N06 **Load two replicas**. These make zero
   generation attempts. Downloads verify native file sizes and Git/LFS identities,
   reuse partial cache bytes, and stop for measured storage incompatibility.
8. Click N07 readiness (six attempts maximum), N08 direct screen (twelve).
   Inspect/export N09. Only a documented mathematical competence limitation
   without protocol defects enables the separately requested thinking screen.
9. Select the passing mode in N11 and explicitly run two full-input/full-output
   envelope probes. These diagnostics count; research output is never forced.
10. Execute pilot 1 in N12, inspect/download/review N13; repeat separately for
    pilot 2 (N14/N15) and pilot 3 (N16/N17). A failed stage still exposes evidence
    and checkpoint links. Review genuine original communication and operational
    usability; recovery mistakes or the effect sign alone do not disqualify.
11. N18 shows status/forecast and an explicit freeze action. Gates require correct
    original teams/controls, valid protocol and adequate resource evidence.
    Freeze makes no main calls. Download its pre-main checkpoint.
12. N19 prepares the next fixed one/two-world batch; N20 executes that scope once;
    N21 inspects/downloads and records review notes. Repeat those cells by choice.
    Models stay resident between actions. No button silently starts a later stage.
13. Use N23 for read-only final/partial analysis and annotations; N24 for final
    archive/reconstruction. Save/download the **executed notebook** separately
    through Kaggle. Download the latest archive off session before closing models
    and stopping Kaggle through its UI. Process shutdown is not provider release.

Running all cells renders controls; it cannot initiate inference or main research.
Each stage has one bounded scope, prerequisites, visible attempt allowance and
progress. Every completed/stopped action exposes a cumulative checkpoint. A
download link proves file creation/integrity, not off-host durability.

## Explicit-command fallback and inspection

If a widget is missing or unreliable, the same finite APIs work in an ordinary
notebook cell. Do not turn on automatic execution to compensate:

```python
ui.run("setup")
ui.run("initialize", mode="new")
ui.run("window", deadline="ACTUAL-UTC-ISO-DEADLINE", evidence="Current Kaggle UI allowance")
ui.run("selfcheck")
ui.run("weights")
ui.run("load")
ui.run("readiness")
ui.run("screen", mode="direct")
ui.inspect(world="qualification-00")
ui.run("envelope", mode="direct", reload=False)
ui.run("pilot", number=1)
ui.inspect(world="pilot-00")
ui.run("review", scope="pilot-1", notes="Trace locations and usability review",
       useful_communication=True, usable=True)
# Repeat pilots 2 and 3 explicitly, inspect/download/review each.
ui.run("freeze", notes="Configuration, pilot reviews and measured allowance accepted")
ui.run("prepare_batch", count=2)
ui.run("main")
ui.inspect()
ui.run("review", scope="batch/main-00+main-01", notes="Reviewed all batch traces/export")
ui.run("pause")
ui.run("snapshot")
ui.run("close_models")
ui.run("shutdown")
```

`ui.run` is synchronous; widget callbacks use the same method on a background
thread. A notebook interrupt requests pause. If a request is still active, use
`ui.run("pause")`/`ui.run("status")`; wait for the bounded call to settle before
snapshot/close. Child logs show prefill/decode progress in
`i01-study/receipts/controller-stderr.log`; turn/attempt events appear live.
`ui.client.start(...)` and `ui.client.wait(action_id)` are explicit asynchronous
alternatives. Double-clicks attach/refuse instead of duplicating work.

All prompts, views, messages, private submissions, raw invalid outputs, token IDs,
thinking and delivery timelines are available in `reports/conversations.html`,
`.jsonl` and `.txt`. Thinking is audit material, not a faithful explanation.
Use the selector for world/phase/agent without changing the experiment. Label
failures through `ui.annotate(id, frozen_label, [exact_call_ids], notes)`; ambiguous
mechanisms stay ambiguous. No LLM judge is used.

## Restore and interruption

An exact current archive is `i01-study/exports/latest.zip`. It contains both
canonical SQLite backups, exact source wheel/code/config, saved worlds/seeds,
gate/freeze/session evidence, raw outputs/tokens, reports and integrity inventory.
It excludes weights, environments, caches and credentials. The last valid ZIP
survives a failed replacement. Writers quiesce at the same call/effect boundary
without unloading resident weights, including periodic five-minute refreshes.

For another Kaggle session, attach the latest downloaded checkpoint alongside
the same source release. Select its exact ZIP or expanded root in N03, use a
fresh writable run directory, and document whether it is the latest complete
snapshot. Unknown session-tail spending blocks admission. Missing a ZIP filename
never implies a new study. Several candidates require explicit selection.

```python
ui.run("initialize", mode="restore", selected="/kaggle/input/EXACT-BUNDLE",
       tail="latest", evidence="Latest downloaded safe-boundary archive; previous session stopped")
# Repeat setup/self-check/download as needed, set current deadline, and load.
ui.run("envelope", mode="direct", reload=True)  # two contingency attempts, not cached evidence
ui.run("main")  # resumes only the saved prepared scope; completed calls reuse raw outcomes
```

For files intact after a kernel restart, choose `mode="reopen"`; the OS ownership
lock refuses a second controller. Confirm old model/controller exit before
replacement. An admitted call with no durable outcome stays spent and unknown:

```python
ui.client.command("reconcile", slot=0, attempt=EXACT_ATTEMPT_ID,
    evidence={"termination_confirmed": True, "reason": "Observed old process/session exit"})
```

Only one identical infrastructure retry is allowed. Known timeouts, malformed,
truncated or wrong responses never retry. A raw-persisted call without effects
reapplies effects without generation. If a timeout termination acknowledgement
is absent, new dispatch is refused. Do not infer process death from a stale PID.

A known timeout is never retryable. If its termination acknowledgement was lost,
record later observed exit without changing the outcome:

```python
ui.client.command("confirm_timeout_termination", slot=0, call="EXACT_CALL_ID",
    evidence={"termination_confirmed": True, "reason": "Observed prior session/process exit"})
```

If the latest archive predates lost work, it is **partial recovery**. Bound
missing spending with real evidence; mark affected worlds and never silently
regenerate their lost prefixes. If no bound is defensible, reporting remains
available and generation stops. Use:

```python
ui.client.command("lost_spending", gap={"resolved": True, "upper": UPPER_BOUND,
    "evidence": "Recorded operator/session evidence"}, affected_worlds=["main-XX"])
```

Unbounded loss uses `resolved=False, upper=None`. A bound beyond contingency
cannot be admitted. A download is only an external backup after you save it off
Kaggle. No local SQLite design recovers erased session bytes.

## Read-only reconstruction and package maintenance

Without CUDA, extract the checkpoint and use its exact source:

```text
python scripts/i01_course.py --source SOURCE --run EXTRACTED status
python scripts/i01_course.py --source SOURCE --run EXTRACTED report --output REPORT_DIR
```

The source/wheel provides `i01-course` and `python -m recovery.i01.cli` as well.
Analysis cannot create a worker or infer missing outcomes. Final status remains
partial until all twenty prefixes, forty continuations and twenty revised
controls have known terminal outcomes and spending/evidence reconcile.

Development rebuild commands (no model calls):

```text
python scripts/build_i01_course_notebook.py
python scripts/build_i01_course_release.py
python -m unittest tests.test_i01_integration
```

Use [the WBS handoff](plans/i01-course-implementation-wbs.md#14-living-implementation-handoff)
and [focused evidence](validation/i01-implementation.md) for implemented versus
verified status. The short-envelope headroom and real 9B conversations must be
qualified on Kaggle; historical hardware probes are not I-01 results.
