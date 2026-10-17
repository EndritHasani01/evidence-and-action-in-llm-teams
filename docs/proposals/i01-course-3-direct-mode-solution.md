# I-01 course-3: direct-mode solution and repair proposal

15 October 2026. **Proposal only: no scientific rule or production implementation
is changed.** The [course-3 analysis](../validation/i01-course-3-results-analysis.md)
and [audit receipt](../validation/course-3-audit.json) establish the observations.
This document extends the [course-2 fix proposal](i01-course-2-fix-proposal.md)
and the preserved [protocol-first evaluation](i01-protocol-first-qualification-evaluation.md);
it does not rewrite those historical documents.

## 1. Recommended decision

**Use the existing direct/nonthinking condition for the primary study, subject
to an explicit protocol-first scientific amendment and the repairs below.**
Keep its model, inputs, prompts, decoding settings and bounds. Report mathematical
accuracy as a measured property and outcome, rather than requiring near-perfect
mathematics for admission.

The current evidence favors that practical decision: on the five matched
controls, direct used 11.215 ready-model seconds and 81 generated tokens;
thinking used 1,022.044 seconds and 10,250 tokens. Thinking returned four correct
finals and one capped noncompletion. The four correct cases were already correct
in direct; the two direct errors belong to thinking cases that never ran.
This is a **91.13-fold observed cost difference**, not a general accuracy ranking.
The conditions also differ in sampling settings and output reserve, so it is not
a controlled single-factor estimate of enabling a reasoning flag.

Do not spend seven more calls merely to finish the abandoned thinking screen
before choosing direct. Under the unchanged zero-protocol-error requirement,
the already recorded invalid action prevents that thinking screen from passing.
Keep its five outcomes and seven unknown cases as incomplete qualification
evidence. Do not mark thinking accepted, replace the unfinished reply, or count
the four valid finals as a successful twelve-control screen.

No more model search, prompt tuning, new thinking caps, reasoning extraction,
runtime upgrades or parallel-serving infrastructure is needed to make this
decision. These would change the tested condition or add work without resolving
the demonstrated problem.

## 2. Scientific amendment required before continuation

[Specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
currently requires 11/12 correct qualification controls and correct original
pilot teams/six pilot controls. Course-3 passes neither a direct competence gate
nor an accepted thinking gate under that authority. The later headroom refusal
is therefore correct. An implementation fix must not quietly reinterpret those
saved failures as passes.

The proposed amendment is a principled separation of operational compatibility
from scientific success, not a new numerical cutoff selected to admit 10/12.

| Component | Proposed rule | Evidence that must remain visible |
|---|---|---|
| Qualification scope | Keep all twelve direct controls on the existing six worlds; no replacement or resampling | Original and revised exact answers, truth, validity, termination, tokens, seconds and call references |
| Qualification protocol | Require all twelve to return valid scalar actions, strict types, legal semantics and complete final framing | Twelve valid direct actions; no malformed/truncated final in this screen |
| Qualification mathematics | Diagnostic, not an admission threshold | Preserve **10/12**, both `788` errors, and the original failed 11/12 decision |
| Execution integrity | Keep source/runtime isolation, private views, fresh cache, finite scores, exact persistence/replay, bounded calls and reconciled spending as hard requirements | Passing implementation checks and actual-host evidence for each applicable bound |
| Hardware envelope | Keep two selected-mode 8,192-input/512-output direct probes and at least 1.5 GiB free headroom per T4 | A current successful load pair; short-control memory readings do not substitute |
| Pilot mathematics | Report every original team, recovery sibling and control result; wrong answers alone do not reject the model | All three existing pilot worlds and six controls, including unsuccessful outcomes |
| Pilot usability | Keep legal protocol, actual task-relevant original communication, inspectable traces/downloads and an affordable measured forecast | Human observations tied to call IDs, independent of a favorable retain/clear effect |
| Main | Keep twenty intended worlds, fixed schedules, bounded turns, paired sibling scoring and all failures | All-world primary analysis, correct-prefix descriptive analysis, controls, effort and missingness |

This must change pilot acceptance consistently. Keeping perfect original-team
and control accuracy after removing 11/12 would just move the same mathematical
barrier downstream. Conversely, a model returning the same legal scalar for
every prompt should not be mistaken for evidence of meaningful collaboration.
Pilot review must inspect actual information exchange and execution feasibility;
it must not select worlds or modes according to the retain/clear contrast.

Record this as a data-informed design revision: both direct screens and the
partial thinking screen were observed before the change; no pilot or main
outcomes have been observed. Preserve the old rule and its historical results,
state the recovery question motivating the new rule, and freeze the amended
policy before further experimental execution. The
[Center for Open Science transparency discussion](https://www.cos.io/blog/preregistration-plan-not-prison)
supports documenting departures and their timing; it does not imply this project
has a formal preregistration.

The scientific rationale remains defensible: retaining versus clearing an
imperfect conversation can be measured in an imperfect system. Reasoning and
integration failures are relevant to the motivating
[SILO-BENCH research](https://arxiv.org/abs/2603.01045). That motivation does not
establish that any protocol-compliant model is informative enough for this
particular twenty-world study.

Important limits remain:

- Frequent failure can create a floor effect and a weakly informative contrast.
  Twenty worlds cannot establish equivalence from a small or zero difference.
- Recovery following an already incorrect prefix is adaptation from an imperfect
  history. Keep it in the primary population; show the planned correct-prefix
  stratum separately, even if that denominator is small or zero.
- Full-information controls diagnose ability. They do not identify a private
  cognitive mechanism or justify subtracting their error rate from treatment
  success.
- The six qualification worlds are paired inputs, and course-2/course-3 repeat
  the same saved cases/seeds. Repetition is not twenty-four independent direct
  cases or a precise reliability estimate.

Exact scoring stays unchanged: terminal unsuccessful episodes score zero;
unexecuted/unresolved episodes remain unknown. Never discard a world because
its prefix or control failed. Invalid actions remain empty, turn-consuming model
outcomes in legal episode execution; this is distinct from the stricter
qualification/pilot prerequisite checks. Do not convert a wrong number into a
protocol defect or extract a number from private thinking to create a submission.

## 3. Repair normal output-failure classification

**C3-01 / C2-07, observed on the target host.** The last thinking call has
`termination='length'`, `truncated=true`, no provider failure, finite scores and
fresh cache evidence. No final delimiter/action was produced. In
[inference.py](../../recovery/i01/inference.py), `split_visible` correctly leaves
no usable final. In [workflow.py](../../recovery/i01/workflow.py), `Session.call`
incorrectly promotes every framing error into global `model_defect`. The control
is committed as `truncated_action`, then the global flag aborts the screen.

The minimal repair is to classify these facts separately in the existing outcome
handling: ordinary output truncation or malformed final framing is a model
protocol failure; real backend/numerical/cache/isolation failures retain a global
dispatch stop. Preserve the native text, token count, framing/validation evidence,
physical attempt and error effect. Do not fix the final delimiter, alter caps,
retry the call, or change its correctness from zero.

Use the existing lifecycle rather than introducing another error framework.
An ordinary invalid model action should consume its legal turn and deliver no
message/submission; a genuine unresolved process/runtime defect should continue
to block admission. A qualification screen may still fail on any invalid final;
that is a gate decision, not evidence of broken hardware.

**Existing flag handling is part of the repair.** Course-3 already contains a
saved global `model_defect`. Merely changing future classification will not
unblock it. A reviewed compatible continuation must preserve the original flag
and error receipt as history, record a narrow adjudication referencing this exact
call and its normal length termination, and remove only its incorrect active
runtime-blocking effect. Re-evaluate current prerequisites under the adopted
policy. Do not erase all defect metadata or exempt real provider/cache defects.
This action needs an implemented, tested continuation path; it is not a manual
SQLite-edit instruction for the current notebook.

**Focused acceptance:** use the saved capped outcome and a finite, well-framed
wrong direct outcome. Both retain their exact protocol/correctness results and
spending. Only the former is an invalid action; neither falsely becomes a
backend defect. A scripted genuine provider/cache/numerical failure still stops
dispatch. Replaying a committed result must perform zero provider calls.

## 4. Derive partial screens and truthful reports from existing records

**C3-02, observed.** `Session.screen` writes its aggregate only after a list of
twelve controls returns. A stop after five leaves no `screen/thinking`, despite
five durable outcomes. The aggregate's absence cannot mean zero execution.

Derive screen progress from the fixed manifest scope, existing call outcomes and
committed control states. Show planned, admitted, unresolved, committed, valid,
correct, incorrect, invalid and unexecuted counts with clear denominators. An
admitted unresolved outcome is not "unexecuted." No second authoritative progress
store is necessary. A partial screen must never become accepted through a
complete-case denominator.

For this archive the expected display is:

| Mode | Planned | Recorded/committed | Correct | Wrong scalar | Invalid | Unexecuted | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Direct | 12 | 12 | 10 | 2 | 0 | 0 | Complete; original mathematical gate failed; meets proposed scalar-protocol portion |
| Thinking | 12 | 5 | 4 | 0 | 1 | 7 | Incomplete and not acceptable under the zero-invalid rule |

Store or display historical criterion results separately from current eligibility
under an adopted amendment. Do not overwrite old `screen/direct.passed=false`
to make a new policy appear to have been in force originally. The minimum
existing-metadata extension should bind an explicit policy/source transition to
its derived eligibility; it should not create a parallel experiment database.

**C3-03 / C2-09–10, observed.**
[report.py](../../recovery/i01/report.py) reads team-event errors but omits scalar
control-state errors. Add the control state's `error` to the appropriate existing
failure category and obtain its call reference from the calls table. For course-3
the repaired report must show two direct wrong-submission entries and one
thinking truncated-action entry, all with actual call IDs. Keep category counts
separate from physical-attempt counts; do not invent extra attempts for labels.
The same derivation must feed CSV, overview, inspection and failure figures.

Also display why `control_completed` is terminal bookkeeping rather than a valid
or correct answer. A compact mode-level resource table should include all five
thinking calls, including the failed final, and show seven pending cases as
unknown. Main figures remain explicit no-data/missingness displays until team
episodes exist; empty figures are not evidence of zero policy effect.

**C3-04, observed.** `Study.check_headroom` selects a mode before entering the
central action wrapper. The later refusal appears in the executed notebook but
not in the earlier archived error receipts. Route public-stage precondition
failures through the existing operator receipt/export path, with zero admission
or inference. Preserve the latest durable checkpoint if a new export fails.
Do not create a new error ledger or pretend the 11:17 archive contains an event
from 11:28.

**Focused acceptance:** reconstruct this archived partial screen without workers;
assert 12/12 direct and 5/12 thinking, one invalid thinking final and seven
unexecuted. Check three trace-linked failure rows and matching derived figures/
tables. Reject selected-envelope admission before a passing current criterion,
record the refusal once through existing receipts, and assert zero new calls.

## 5. Reconcile the two studies before spending again

**C3-05, observed accounting boundary.** Course-3 is a new study, not a resume
of course-2. The course-3 local ledger's 23/500 is correct for its two DBs; it
cannot establish campaign spending. Eighteen calls were newly executed again
with the same logical IDs, requests, seeds and token sequences. Those executions
are not free replay.

| Spending quantity | Recorded value |
|---|---:|
| Course-2 physical attempts | 18 |
| Course-3 physical attempts | 23 |
| Known physical executions across these supplied studies | **41** |
| Course-3 local arithmetic remaining | 477 |
| Whole-campaign arithmetic remaining, if 500 covers both studies | **459**, before any other spending |

The historical 45 belong to the separate earlier regime. The earlier eighteen
I-01 executions must not be reclassified as those historical 45, as lost-spending
uncertainty, or as eligible infrastructure retries. They have complete outcomes.

Before any continuation, document the intended 500-attempt scope and reconcile
all supplied spending against it. Use the conservative whole-I-01 total until
that scope is explicitly settled. Check repeated-stage allowances too: across
these studies, twelve state diagnostics and twenty-nine qualification calls
already exceed the original one-study first-attempt allocations of eight and
twenty-four. Available global capacity does not automatically authorize those
repeats or silently convert them into contingency. Document the deviation and
any approved allocation amendment; preserve the original stage identities and
physical rows.

Enforce the reconciled bound in the existing single admission owner. If a
continuation legitimately excludes prior-study DBs from its live stores, retain
an explicit immutable prior-study spending charge, linked to those exact existing
study IDs/checkpoints and checked for overlap. Derive the charge from the
preserved ledgers; do not transplant their outputs into the new study's traces.
Admission must use current attempts plus prior charges and unresolved upper
bounds, with stage/contingency treatment explicit. Keep prior charge unchanged
through restore and prevent duplicate application. This is a small extension to
existing metadata/admission, not a campaign service, new database or new ID scheme.

For scale, two initial direct envelope probes plus up to sixty pilot and 380
main first attempts would require **442 further attempts**. Then course-3 alone
would total 465; the two supplied studies together would total **483**. The
remaining seventeen are **arithmetic slack, not an authorized contingency
allocation**. Neither that slack nor the ordinary twenty-eight reserve can be
promised without reconciling repeated preparation, stage limits, other spending
and future reloads/retries. Unused thinking capacity must not add worlds or
erase the five thinking attempts already consumed.

**Focused acceptance:** a fresh study cannot reset an established campaign charge;
current 23 plus prior 18 reports 41, restore preserves both charges and prior
uncertainty, duplicate prior evidence cannot double-charge, and admission refuses
before the reconciled global/stage/contingency limit. No inference is needed.

## 6. Preserve source binding and repair the other proven failures

**C2-12 remains a prerequisite.** The archived source is `8f5bcdb...`, not code
with these fixes. Loading a newer packet into the old run currently conflicts
with source binding. Do not bypass those checks, replace the archived wheel,
edit the manifest's source identity or set `START_MODE='new'` to evade the block.

Implement an explicit narrowly reviewed transition for these compatible fixes
and the separately adopted gate policy. It must preserve the course-3 study ID,
all twenty-three attempts, raw requests/outputs, seeds, immutable original source
packet and prior rule decisions, while identifying the new code/policy and the
eligibility/adjudication performed. Validate existing bytes before transition,
make a quiescent pre-transition export, and refuse unexpected scientific changes.
No pilot/main exists here, so no changed condition may be slipped into an
already executed experimental comparison. A fresh-study alternative still needs
the same spending reconciliation; it is not a free replacement run.

The remaining [course-2 fixes](i01-course-2-fix-proposal.md) are still necessary
before relying on their affected paths:

| Finding | Repair that remains required | Small acceptance case |
|---|---|---|
| C2-04: load-pair mismatch can reuse old envelope calls | Invalidate from actual successful old/current load references, independent of reload flags | Replace one non-None dead worker; old pair refuses and explicit reload charges exactly two probes |
| C2-05: latest-tail restore erases a prior spending gap | Preserve saved uncertainty and add only new post-boundary exposure once | A prior three-attempt gap survives both restore interfaces and a zero new tail |
| C2-06: duplicate logical DB can be accepted | Validate expected slot identity and reject duplicated/misplaced logical calls | Substituting slot-0 DB for slot-1 fails before analysis or dispatch |
| C2-08: live table reads can mix commits | Read related tables per worker within one SQLite read transaction | One controlled concurrent writer cannot produce the reproduced missing-call `KeyError` |
| C2-02/03: noisy warnings and huge load receipts | Compact display, explain known nonfatal diagnostics and retain full raw receipts | Render the saved loads with bounded output; downloads still contain exact full inventories |
| C2-11: ambiguous remaining-time evidence | Echo the actual fixed deadline, recorded observation and chosen safety margin | A decreasing observed timer does not reset a previous absolute bound or invent provider quota |

Do not add an extensive CPU campaign. Reuse the existing course-2 counterexamples
and course-3 saved outcomes in a few focused checks for these exact boundaries.
The present audit verifies archive integrity/reconstruction, not these proposed
repairs; the production defects remain open.

## 7. Ordinary-cell operator progression after approved repairs

Keep ordinary named Python stage cells, resident workers and reusable scientific
modules. No widget forms or sequence of action buttons is proposed. The notebook
should make the selected direct condition and its historical 10/12 diagnostic
visible without requiring the operator to falsify a pass flag.

1. Open/inspect the exact supplied checkpoint read-only; show source, study ID,
   both mode summaries, campaign/local spending and unresolved prerequisites.
2. Execute the supported compatibility/policy transition once, after adoption;
   validate preserved evidence and produce a downloadable checkpoint. Never
   re-run completed qualification controls as part of this step.
3. Record actual current Kaggle allowance/deadline, load the pinned replicas and
   perform only the readiness/envelope validation genuinely required by that
   session/load history. Reconcile its spending before admission. If no envelope
   was previously accepted, do not invent a past acceptance or free reload probes.
4. Run the selected direct full envelope. Stop if current devices, headroom,
   source/runtime/state, termination or accounting evidence is unacceptable.
5. Execute pilot 1, inspect its complete conversation/results and download its
   checkpoint; repeat separately for pilots 2 and 3. Show mathematical mistakes
   as outcomes and preserve actual human usability findings.
6. Review all pilots and a measured direct-mode resource forecast. Freeze the
   adopted policy and unchanged scientific condition before main, with explicit
   main authorization; no automatic advancement or outcome-based world selection.
7. Prepare/run/review the existing fixed main batches, downloading incremental
   checkpoints. Reconstruct reports read-only, verify the final archive and close
   processes explicitly when finished.

Keep the partial thinking results available through inspection/reporting as a
diagnostic side record. Do not make its incomplete screen a hidden dependency
of direct execution or offer an automatic thinking fallback. If a named stage
is blocked, the ordinary cell should state the missing prerequisite and expose
the saved evidence through the existing report/checkpoint interfaces.

Short direct controls are not a reliable estimate of distributed pilot/main
latency or correctness. Measured pilot calls, messages, time, failures and
remaining budget must determine feasibility before main. Parallelizing the
thinking screen cannot solve a 91-fold per-input time increase; neither changing
the UI nor removing checkpoints resolves this output-volume problem.

## 8. Implementation checkpoints and remaining target-host evidence

| Checkpoint | Concrete deliverable and acceptance | Current status |
|---|---|---|
| Decision/adoption | Explicit §12 amendment and consistent WBS/gate policy; preserved original failed screens; settled budget scope/repeated-preparation treatment | Proposed |
| Correctness/accounting repair | C2-04–08 plus C3-01/05 fixes, narrow existing-flag adjudication and source-compatible continuation; focused saved/scripted checks | Proposed; defects still present |
| Reporting/notebook release | Partial mode summaries, three trace-linked failure entries, compact loads, precondition receipts, ordinary-cell direct progression and coherent source/wheel/runbook | Proposed |
| Operator acceptance | Actual current-session load/state/full-envelope evidence, individual pilots/reviews/downloads, measured forecast and explicit freeze | Unexecuted |
| Main and final outputs | Twenty intended paired worlds or an honestly bounded partial result; final read-only report, archive verification and off-session download | Unexecuted |

Use meaningful commits at those engineering checkpoints if implementation is
subsequently authorized. Local validation should be saved-outcome replay,
targeted accounting/lifecycle fixtures, package/cell/link checks and read-only
archive reconstruction. No local model qualification, hidden diagnostic calls
or repeated inference is part of the repair work.

This proposal cannot guarantee absence of every future error. It addresses the
observed truncation/classification/reporting failures, the known reproduced
recovery defects and the newly exposed cross-study accounting boundary. Full
direct-envelope headroom, real collaboration, retain/clear effects, later
session restoration and browser downloads still require the operator's staged
Kaggle execution. All twenty main outcomes remain unknown.
