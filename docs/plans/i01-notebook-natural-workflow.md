# I-01 notebook: ordinary cells and natural progression

Latest whole-study follow-up (15 October): 33 ordinary cells now cover the entire
experiment with Run All. The user approved objective pilot checks and retrospective
human review. Both notebook filenames are identical; configuration is locked
before inference and main resource admission is automatic. All ten fixed batches,
reports, verified export and closure are included. Earlier counts and manual
approval/preparation-only statements below are historical. See the current
[runbook](../I01_KAGGLE.md) and [evidence](../validation/i01-course-4-run-all.md).

15 October latest follow-up: the user now requests a fresh independent Run All
preparation without previous checkpoints. The default notebook has fourteen
ordinary cells from session facts to verified report/archive. The complete
twenty-six-cell pilot/review/freeze/main notebook remains individually operated.
See the [current runbook](../I01_KAGGLE.md) and
[fresh-run evidence](../validation/i01-fresh-run.md). Earlier cell counts and
blanket Run All restrictions below describe the previous interaction design.

14 October 2026. **Implemented; focused checks passed; Kaggle acceptance pending.**

Working checkout: `E:\Github\recovery_blueprint\recovery_blueprint`, branch
`feat/smaller-natural-experiment`, planning baseline `22220b9`.

The user requested a usability redesign and explicitly chose ordinary notebook
cells. Pressing **Run** should perform the cell's named stage. Routine operation
should require neither widget forms nor an additional button click. This document
records that change and its completion below. The delivered notebook now uses
25 ordinary execution cells and no widget panels.

Scientific behavior remains governed by [specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
The [implementation WBS](i01-course-implementation-wbs.md) and
[current runbook](../I01_KAGGLE.md) describe the existing delivery. This follow-up
changes its operator interaction, not the adopted experiment.

## 1. Initial usability problems (before the redesign)

Inspection of the current generator, notebook and `recovery/i01/ui.py` found:

- The notebook has 24 code cells and 35 action panels. Most cells only render
  controls; running them does not do the work advertised by the stage heading.
- Routine settings, state and human decisions appear together in forms. For
  example, the operator selects the envelope mode, supplies main-batch review
  scope and encounters restore options during a normal first run.
- `Operator.show()` renders full JSON in a scrolling block. `links()` repeats
  archive, report, table and figure links after many actions. Important outcomes
  and the next step compete with implementation detail.
- Conversation inspection requires selecting filters and pressing another
  button. Pilot reviews then appear as separate forms with unchecked boxes.
- N22 places status, pause, export, model closure, reload probes, main execution
  and controller shutdown together. N24 repeats closure controls.
- Errors returned by the controller are displayed by `Operator.run()` as ordinary
  results. A direct-cell redesign must make a stopped action visibly fail the
  cell after presenting its evidence; otherwise later queued cells could proceed.

The problem is interaction structure. A new dashboard, JavaScript application,
framework or persistence layer would add work without addressing that structure.

## 2. Interaction decision

Use a conventional, readable Kaggle research notebook:

1. A short introduction explains the experiment and the execution order.
2. A small configuration cell contains the few operator-supplied facts.
3. Ordinary cells run meaningful stages through reusable Python functions.
4. Each result explains what happened, where evidence is saved, and which cell
   comes next. Technical details remain available in expandable output/files.
5. Three pilots have individual execution and review cells. Main execution uses
   a repeatable prepare → execute → inspect/review sequence for one fixed batch.
6. Recovery and exceptional operations live in an appendix with direct commands.

All normal stages work with `ipywidgets` absent. Standard HTML, text and file
links may enrich results; no custom frontend is necessary to execute the study.
The existing retained controller and two resident model processes stay in use.

### Run All policy change (implemented)

The original WBS §7 and M5-T02 required Run All to render controls without starting
inference. That rule is incompatible with the requested direct execution cells:
an ordinary cell calling `ui.run("pilot", number=1)` performs the same action
whether queued by Run Cell or Run All. This design will not claim to distinguish
them or add arming flags, confirmation prompts or another control layer.

The implemented engineering requirement is:

- **Run one stage cell at a time.** Its execution is the operator's explicit
  request for the displayed bounded scope.
- **Run All / Save & Run All is not a supported study execution method.** It can
  execute multiple stage cells, including inference. Put this statement at the
  top of the notebook and in the upload instructions.
- No function starts a later research stage on successful completion. Review
  gates, prerequisites, the prepared main scope and admission limits still apply.
- Verification checks each cell's scope and failure behavior rather than claiming
  that executing every direct-action cell starts zero actions.

This is an explicit change to notebook interaction and its engineering acceptance
checks. It changes no population, inference setting, scientific gate or physical
attempt allocation. The implementation does not gain permission to run any model.

## 3. Information the operator actually needs to provide

| Input | When it is needed | Presentation |
|---|---|---|
| Actual session deadline and allowance evidence | Each new controller session, before resource admission | Two clearly explained configuration values; never an invented quota or duration |
| Source attachment | Only when source discovery is ambiguous | Default unique verified attachment; list candidates and exact override |
| Start mode | At study opening | One configuration value: new, reopen or restore; no repeated selector |
| Exact checkpoint and tail evidence | Restore only | A separate restore example and the existing evidence checks |
| Direct competence limitation reason | Conditional thinking qualification only | A commented optional cell; never prefilled with fabricated justification |
| Communication/usability findings and notes | After each pilot | A small ordinary review cell with unset findings and a short notes template |
| Batch size | Main preparation | Default two fixed worlds; change to one explicitly when appropriate |
| Batch review acknowledgement | After each main batch | Run the review cell after inspecting its report; extra notes optional |
| Reconciliation evidence | Unresolved interrupted work only | Appendix with exact identifiers and explicit evidence requirements |

Mode for envelope/pilots/main, main-batch identity, report paths, gate state,
completed scope and counters come from existing canonical state. Do not ask the
operator to retype them. Readiness or a correct full-information answer does not
establish useful original communication; pilot findings remain a human decision.
Unreviewed findings must stay unset, not silently default to approved.

Opening an existing directory never resets it. Restore attachment discovery may
list candidates, but must not choose by date or treat a missing ZIP as a new study.
For intact files after kernel restart, show the explicit reopen route. A second
controller must still be refused until the original owner has exited.

## 4. Proposed notebook sequence

The headings below express the operator's tasks. Execution, inspection and review
remain separate wherever they have different effects. Cell count is not a goal;
avoid merging stages merely to shorten the notebook.

| Section / cell | Running it does | Output / next step |
|---|---|---|
| Start here | Markdown only | Short study explanation; workflow; one-cell-at-a-time rule; T4×2 and Internet instructions |
| 1. Configure and inspect workspace | Verify the small source attachment; read actual host/storage inventory | Compact compatibility table; editable facts only; setup prerequisites |
| 2. Install the pinned runtime | Existing setup and metadata/tokenizer retrieval | Live installation progress; interpreter and provenance summary; log link |
| 3. Open the study | Initialize, reopen or explicitly restore; record actual session allowance | Study identity, coverage, spending, selected starting route; no generation |
| 4. Check the implementation | Existing lightweight native/scripted self-check | Named checks and concise receipt; failure explanation and evidence |
| 5. Download verified weights | Existing pinned download/cache reuse | Progress, verified revision, actual space, cache summary |
| 6. Load both T4 workers | Existing resident loading only | Two device rows: identity, load time, residency and memory; no hidden warmup |
| 7. Check fresh-state readiness | Exactly the six declared checks | Pass/fail table, raw evidence and actual attempt count; ≤6 first attempts |
| 8. Check direct-mode competence | Exactly the twelve declared controls | Original/revised results, protocol errors, threshold; ≤12 first attempts |
| 9. Inspect qualification | Read-only results and traces | Passing mode or precise blocked state; transcript/files available |
| Optional: thinking qualification | Only the predeclared conditional screen, after documented justification | Skipped message if direct passed; otherwise explicit bounded request, ≤12 first attempts; no automatic fallback |
| 10. Check selected-mode headroom | Two full-envelope probes in the passing recorded mode | Per-device measured headroom and reserve, qualified/blocked status; ≤2 first attempts |
| 11. Run pilot 1 | Only pilot 1 | Phase outcomes, conversation, costs and cumulative checkpoint; ≤20 first attempts |
| Review pilot 1 | Record the operator's actual communication/usability findings | Recorded review or clear missing findings; no pilot 2 execution |
| 12. Run pilot 2 | Only pilot 2, after pilot 1 review/export | Same report structure and download; ≤20 first attempts |
| Review pilot 2 | Record actual findings | Recorded review; no pilot 3 execution |
| 13. Run pilot 3 | Only pilot 3, after pilot 2 review/export | Same report structure and download; ≤20 first attempts |
| Review pilot 3 | Record actual findings and display combined pilot gate report | Qualification, three reviews and measured forecast; no freeze |
| 14. Review the main configuration | Read-only exact configuration, gate state and forecast | What will be frozen, unmet requirements, available attempts and deadline margin |
| 15. Freeze for main | Existing explicit freeze, with operator notes | Frozen receipt and pre-main checkpoint; no main calls |
| 16. Prepare the next main batch | Prepare one/two next fixed worlds, or display the existing incomplete scope | World IDs, remaining work, ≤19/38 first attempts, retry allowance and forecast |
| 17. Run the prepared main batch | Only that saved scope | Live progress, outcome matrix, costs and cumulative checkpoint; no next-batch preparation |
| 18. Inspect and acknowledge the batch | Read-only full report followed by an explicit review acknowledgement | Coverage and review receipt; directs operator back to preparation, or to final analysis |
| 19. Build the final or partial report | Read-only analysis, figures and export presentation | Intended denominators, unknowns, paired results, costs, limitations and file links |
| 20. Save and verify the final archive | Quiescent snapshot and existing fresh-directory reconstruction check | Integrity receipt, archive download and executed-notebook save instructions |
| Finish the session | Explicit close-models/controller command, run after saving artifacts | Process exit evidence; separate instruction to stop Kaggle through its UI |

The setup cells still perform separate meaningful operations; there is no
run-everything cell. A generation cell must not quietly qualify another mode,
freeze, start another pilot, or select/run a later batch. Successful read-only
presentation and automatic post-action checkpointing are permitted consequences
of the requested scope. The provisional and frozen runtime bounds remain intact.

### Main execution loop

The operator repeatedly runs just these three cells:

```text
Prepare next fixed batch → Run prepared batch → Inspect and acknowledge batch
```

Preparation returns an existing incomplete scope on resume. It never chooses
worlds based on results. The acknowledgement derives the saved batch ID and records
that the operator executed the review cell; it does not claim a download occurred
or invent substantive review notes. Once all intended work is recorded, preparation
shows completion and execution becomes a harmless status display with no new calls.

## 5. Result presentation

Use notebook-native typography and spacing. Avoid decorative dashboards, nested
scrolling JSON containers, custom fonts, animated elements and separate navigation.
Use clear headings, ordinary tables and textual status alongside restrained colors.
Support light/dark notebook themes and a readable text fallback.

Every stage uses the same small result structure:

```text
Pilot 1 — completed / stopped / paused
Original team | Retain team | Clear team | Original/revised controls
Recorded attempts used | Study total / 500 | Retry allowance | Remaining session time

Conversation and submissions
Checkpoint: current cumulative ZIP · saved boundary · integrity · download
Next: inspect these results, then run “Review pilot 1”.

Details: exact prompts, private audit, tokens/thinking, timings, logs and inventory
```

Labels must distinguish unknown/not executed from recorded failure. Show measured
costs separately from unknown timing; physical attempts separately from logical
policy costs. Show the additional eligible retry allowance alongside each first
attempt ceiling. Never relabel a scientific failure as a software crash or approve
a gate from a favorable recovery effect.

For long-running work, show stage/phase/world, committed turns, actual attempts and
elapsed time. Use existing admitted/raw-persisted/effect/checkpoint events and the
existing heartbeat; do not create another progress store. A turn ceiling is not a
predicted duration, so do not display an invented percent complete or ETA.

### Conversations and downloads

- A pilot result automatically presents its own conversation, with phase headings,
  speakers and exact delivered messages. The operator does not first select a
  world or press Inspect. Default views remain bounded; the complete transcript
  is retained and directly accessible.
- Private submissions, evaluator truth/source edit, exact prompts, raw malformed
  replies, tokens and thinking are clearly labelled audit details. They never
  flow into model requests. Show actual execution/delivery order and do not repair
  or summarize away invalid outputs.
- A main batch presents its one/two worlds, followed by the cumulative paired
  table. World/phase/agent filtering remains available through ordinary inspection
  arguments; widgets are unnecessary.
- Show one prominent current checkpoint link and a few relevant report links.
  Put the full file/integrity inventory in details. Keep HTML/JSONL/text, tables,
  figures and all raw evidence downloadable.
- `latest.zip` is cumulative and advances after later actions. Label its current
  boundary/time/hash honestly; an old displayed link must not imply an immutable
  historical pilot archive. Refresh its details from disk before presenting it.
- Download links fall back to the exact Kaggle Output/Files path. File creation,
  integrity and browser download remain separate facts. Failed pilots and stopped
  batches still expose their saved evidence and last valid archive.

## 6. Interruptions and restoration

Normal inspection/reporting keeps models resident. Rerunning a display cell does
not load a second pair of workers. Reexecuting a completed scope reuses recorded
outcomes; it does not resample. Changed inputs/settings remain rejected.

Use the existing synchronous `Client.action()` path for ordinary generation
cells. Notebook interruption already requests pause from `Client.wait()`. Explain
that pause stops new admissions while an admitted call must settle or terminate
within its existing bound. Show the saved scope, in-flight state and exact next
recovery command. Do not claim that interrupt instantly produces a safe snapshot.

Put these direct-command recipes in a clearly labelled support appendix:

1. Status; request safe pause; make a quiescent checkpoint.
2. Reopen intact files after kernel restart; preserve saved inputs and exact scope.
3. Restore a selected ZIP or expanded checkpoint into a fresh writable directory.
4. Reload workers and run the two explicitly contingency-charged envelope probes,
   then resume only the saved incomplete scope.
5. Reconcile an unresolved attempt or confirm later-observed timeout termination.
6. Record bounded/unknown lost-session spending and affected worlds.
7. Reconstruct reports without CUDA or reopening a generation session.

Missing bytes or unknown unbounded spending can still block generation while
allowing reporting. A restoration helper must never guess that the archive was
latest, assert old-process death or replace unavailable results with zero.

## 7. Implementation work and checkpoints

| Task | Concrete change | Acceptance |
|---|---|---|
| UX-01: direct execution and useful output | Extend the existing `Operator.run`, `show`, `emit`, `links` and inspection methods; add only small I-01 helpers for derived mode/current batch/review presentation | Plain commands work without widgets; controller errors display evidence then fail the cell; no scientific gate is inferred from presentation |
| UX-02: normal notebook sequence | Replace panel calls in the existing generator with direct bounded calls and read-only presentation; use the sequence above; separate support appendix | Each normal cell executes its named work; no forms/extra buttons; three individual pilots; fixed main loop; optional thinking remains explicitly conditional |
| UX-03: pilot/batch review and recovery | Present conversation/download immediately; simplify review inputs and derive batch ID; explain interrupt/reopen/restore in ordinary cells | Human findings remain unset until supplied; export/review dependencies enforced; failed/stopped work remains inspectable; no automatic reload probe or retry |
| UX-04: integrated delivery | Update runbook, WBS §7/M5-T02, handoff and release verifier; rebuild notebook, wheel and source ZIP from one committed code version | Matching generated/source notebook, complete wheel/source/checkpoint compatibility, honest Run All policy, coherent upload instructions |

Implement and make clean commits at these checkpoints: operator behavior;
notebook/review/recovery integration; verified release and documentation. Keep
historical deliveries/evidence intact. Existing checkpoints must remain readable;
avoid changing canonical schemas for an interface change. Do not delete reusable
legacy entry points merely because the generated notebook no longer uses panels.

Primary affected files:

- `recovery/i01/ui.py`, and `client.py` only if a demonstrated interruption or
  rendering issue requires it. Reuse workflow/report/archive APIs.
- `scripts/build_i01_course_notebook.py` and generated
  `notebooks/i01_course_kaggle.ipynb`.
- `scripts/verify_i01_course_release.py`, its current AST/render-only assertions,
  and focused integration checks in `tests/test_i01_integration.py`.
- `scripts/build_i01_course_release.py` if its source allowlist must include new
  helper/document files; regenerate the complete existing wheel and source ZIP.
- `docs/I01_KAGGLE.md`, `docs/IMPLEMENTATION_PLAN.md`, the WBS living handoff and
  concise development receipts identifying the new interaction checks.

There is no reason to modify `core.py`, scientific configuration/runtime pins,
the attempt ledger, SQLite ownership, scoring/uncertainty formulas, fixed schedule
or retention transformations for this redesign.

## 8. Proportionate validation

This planning change needs document/link/diff checks only. The implementation
will use focused lightweight checks and reuse existing prerequisite evidence:

- Compile/schema/empty-output and deterministic generator review. Replace brittle
  expectations of exactly 24 code cells/35 panels with the agreed stage sequence.
- Execute changed cells against a fake operator/controller, one cell at a time:
  confirm their exact bounded actions, direct-pass skipping of thinking, refusal
  without justification, per-pilot separation and main-scope preservation.
- Scripted checks for readable stopped-action exceptions after evidence display,
  absent prerequisites, duplicate scope reruns, unset pilot review fields, derived
  batch ID, no unintended retry and no transition to the next research stage.
- Check the interrupt path's pause request and that management commands do not
  imply settlement/termination. Reuse the existing durability/restore checks;
  extend only behavior changed by this work.
- Inspect a synthetic ordinary-cell pilot/batch output, including malformed HTML
  text, failed and unknown states, long transcripts and checkpoint fallback paths.
  Check the text-only/no-widget route.
- Regenerate and verify the complete release: installed wheel outside the checkout,
  source identity, ZIP/expanded bootstrap, exact read-only restoration and matching
  notebook in checkout and delivery. Replace the old zero-action Run All receipt
  with per-cell scope receipts and explicit policy metadata.

No GPU inference, actual model qualification, pilot, freeze or main execution is
part of implementation validation. Actual Kaggle layout, output updates, interrupt
responsiveness and browser downloads remain target-host acceptance. Linux/T4
qualification and empirical results remain the original operator-run gates.

## 9. Completion criteria

The follow-up is complete when an operator can run the documented path with
ordinary cells, inspect/download each pilot immediately, repeat bounded main
batches, produce complete/partial reports and restore exact saved work without
interacting with widget forms. Only genuinely required facts/findings are entered.

The artifact must retain the 500 physical-attempt ceiling, exact saved outcomes,
experiment isolation, resident models, original gates, unknown-aware reporting and
complete source/checkpoint package. Documentation must clearly distinguish the
planned redesign, its eventual implementation checks and later Kaggle verification.

Interaction planning used the available UI/UX skill checklist for clear primary
actions, progressive disclosure, readable feedback and recovery paths. Its local
search helper is not installed; no generated design-system result is claimed or
needed for this notebook workflow.

## 10. Completion record

The user authorized full implementation after selecting ordinary notebook cells.
UX-01–UX-04 are implemented. The current notebook has 25 named code cells, zero
widget panels, empty execution outputs and direct bounded calls. Models and
canonical stores remain in the existing controller; no dependency/schema or
scientific configuration changed. The old panel API remains for source-bound
historical packages but is unused by the generated notebook.

Milestones: `a8fa948` operator behavior; `cbbe200` ordinary notebook, recovery
recipes and cell-scope verification. The final documentation/release checkpoint
and its package identity are recorded in the development receipts.

Executed focused checks: sixteen tests in 26.115 seconds, with zero failures,
errors or skips, on Windows Python 3.11.9. They cover changed ordinary-cell
behavior plus the existing affected scripted durability/controller integration.
Twenty-five cell scopes execute against a recording fake operator, with no model
calls; notebook schema/compile/empty-output checks pass. Source/wheel/bootstrap/
read-only reconstruction checks are recorded in the regenerated package review.

Evidence: `notebooks/validation/i01-development/ordinary-cell-checks.json` and
`release-review.json`; details in the
[implementation evidence](../validation/i01-implementation.md).
Current operator instructions are in the [runbook](../I01_KAGGLE.md).

The later user report showed a failure inside `ensurepip` and clarified that
generic `ui.run(...)` calls still felt unnatural. The current notebook replaces
those with named `Study` methods (`install_runtime`, `run_pilot`, fixed main-batch
steps and reporting/recovery methods) while reusing the same resident operator.
Environment creation now bypasses ensurepip, installs the previously accepted
verified pip 26.2.1 wheel, preserves partial environments/logs and displays actual
log tails. Version-labelled source extraction and a stale-import guard make
source replacement explicit without deleting old files. Four setup checks and
one real named-step/controller/archive integration check pass; the new record is
`setup-repair-checks.json`. No scientific/runtime dependency pin was changed.

No model/GPU inference, actual qualification, pilot, freeze, main or publication
ran. Actual Kaggle ordinary output/interrupt/download behavior, native framing,
Linux installation, T4 residency/headroom/competence and the empirical workflow
remain operator acceptance. Existing scientific outcomes are neither replaced
nor inferred by this UI revision.

Controller-startup follow-up: reported Kaggle installation now completes, but
inherited inline plotting/Python startup settings prevent controller attachment.
The child runtime now isolates those settings and selects Agg before import;
failed startup displays actual stderr and confirms bounded process cleanup.
Opening/inspection can precede session facts; Load both T4 workers records the
actual window before model allocation. The notebook retains 25 ordinary cells
and named methods. Fourteen focused checks pass in 22.269 seconds with zero
model attempts (controller-startup-checks.json); target-host controller/model
and empirical acceptance remain pending. Bound source and scientific settings
remain preserved, with a same-source recovery recipe for the current session.
