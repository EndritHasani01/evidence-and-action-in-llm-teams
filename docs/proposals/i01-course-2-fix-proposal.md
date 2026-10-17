# I-01 course-2: root causes and complete fix proposal

15 October 2026. **Proposal, not implemented repairs.** Production modules,
scientific settings and supplied execution files remain unchanged. Read the
[results analysis](../validation/i01-course-2-results-analysis.md) for the full
stage history, twelve control results, accounting and evidence limits. The
[audit receipt](../validation/course-2-audit.json) records five reproduced
implementation defects plus exact replay of the observed direct-screen result.

## 1. Decision and boundaries

The observed stop is a **valid competence refusal**: direct mode scored 10/12,
below the adopted 11/12 threshold, with zero protocol errors. Correct prompt
inputs and saved oracles show that qualification-03's `788` answers are wrong;
the internal model mechanism remains unknown. Repairing software must not turn
those two answers into correct ones, resample them, change seeds, lower the
threshold, substitute worlds, add a model, or tune prompts/decoding against the
failed case.

The approved scientific next option is documented **conditional thinking
qualification**, already implemented as a separate stage. It is not an automatic
fallback and has not run. Separate critical recovery/runtime defects reproduced
below should be repaired before relying on those future paths. The upstream
warning messages are explained by their sources and successful subsequent
execution; they do not justify an unreviewed dependency upgrade.

[Specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
continues to govern. Preserve the pinned 9B revision, runtime lock, NF4/FP16 and
reviewed attention, direct/thinking settings, private views, fixed world inputs,
literal retain/clear transformation, saved seeds and schedules, turn limits,
raw-before-effects persistence, exact replay, 500 new attempts, 28 contingency,
historical 45 separation, twenty intended main worlds and explicit stage cells.
Do not create another execution/accounting store or a generalized recovery
framework. No new GPU execution is part of implementing this proposal.

## 2. Finding register

P0 means scientific/accounting protection before further reliance on recovery or
main execution; P1 means runtime correctness/traceability; P2 means operator and
report clarity. "Reproduced" means a small deterministic synthetic fixture, not
an observed course-2 GPU failure.

| ID | Priority | Status and root cause | Minimal response |
|---|---|---|---|
| C2-01 | P1 | Observed valid 10/12 stop; completed stage and failed gate are presented as a generic error | Show exact failed controls and the permitted next decision without changing the gate |
| C2-02 | P2 | Observed upstream diagnostics look fatal despite successful loading/inference | Explain/classify known messages; retain full logs and pins |
| C2-03 | P2 | Observed 843,099-character load output; detailed inventories and inherited 256-token load configuration dominate inspection | Compact load summary, explicit loading-only versus actual per-call settings, downloadable full evidence |
| C2-04 | P0 | Reproduced stale envelope reuse when successful load references change without `reload_required` | Derive invalidation from old/current load pair, not the flag alone |
| C2-05 | P0 | Reproduced restore replacing an earlier lost-spending bound with zero | Preserve prior bound and merge only additional post-checkpoint tail evidence |
| C2-06 | P0 | Reproduced duplicate logical worker DB acceptance; manifest-only binding has no slot identity | Bind/validate the expected slot and reject duplicate/misplaced logical calls |
| C2-07 | P1 | Reproduced normal thinking truncation setting a global runtime-defect flag | Separate invalid model output from backend/cache/numerical defects |
| C2-08 | P1 | Reproduced live analysis `KeyError` from inconsistent table reads during a write | Read each worker's related tables in one SQLite read transaction |
| C2-09 | P1 | Observed failed-control labels have empty call references | Derive control references from the existing calls table and keep evidence-linked labels |
| C2-10 | P2 | Observed qualification evidence hidden behind recovery tables/first-six-call inspection | Explicit qualification tables and failure-focused inspection, including both evaluated modes |
| C2-11 | P2 | Session budget is 700 minutes while prose asserts twelve hours; provider timer is not independently captured | Echo the chosen fixed bound, distinguish observations/margins, never infer quota from prose |
| C2-12 | P1 | Existing source isolation prevents silently applying changed code to the in-progress run | Preserve the packet and eighteen admissions; define an explicit compatible transition before reuse |

The six audit cases take seconds and use temporary DBs/scripted providers only.
The current archive has no earlier spending gap, no duplicate worker DBs, no
reload envelope, no thinking outputs and no concurrent-write reconstruction
failure. C2-04–08 are additional defects, not explanations of the 10/12 result.

## 3. Observed stop and operator guidance: C2-01, C2-02

### C2-01: preserve the competence refusal and make its meaning actionable

**Evidence.** `screen/direct` records `correct=10`, `total=12`,
`protocol_errors=0`, `passed=false`. The direct-screen cell reports the same
values and raises `ActionStopped`. Its controller event first says
`screen: complete`, then the notebook reports a failed gate and creates another
error-boundary snapshot. These refer to different facts: all controls completed,
but the competence prerequisite did not pass.

**Code.** [workflow.py](../../recovery/i01/workflow.py), `Session.screen`, and
[ui.py](../../recovery/i01/ui.py), `Operator.run`, `show`, `thinking_screen`.

**Proposal.** Use concise result text such as "Direct screen completed: 10/12;
competence not accepted; zero protocol defects." Show two rows with failed call
IDs, truth/submission and links to saved prompt/output evidence. Keep the
stopped-cell barrier and zero automatic next-stage calls. Explain that the
operator may inspect, document a competence limitation and explicitly choose
the existing thinking stage. If thinking also fails, preserve its failure and
stop; do not offer uncontrolled prompt/model search.

For this run, zero-call inspection is already available:

```python
study.inspect_qualification()
study.inspect(world="qualification-03", audit_limit=None)
study.links()
```

If subsequently authorized and resource-admitted, the existing thinking cell's
reason can cite: "Direct qualification was 10/12 with zero protocol defects;
qualification-03 submitted 788 instead of 951 and 920 on complete inputs."
That documents eligibility; it is not a claim that thinking will pass or a
request to launch it during this repair.

Avoid redundant exports if no new durable evidence was added. If a new operator
receipt is appended, export that updated receipt once and label the boundary
accurately. Do not suppress real unexpected exceptions behind a generic gate
message. Replay must retain the failed direct result at exactly eighteen spent
attempts; the audit already verifies zero-provider-call replay.

### C2-02: upstream documentation/deprecation/fallback messages

The exact pinned Transformers
[auto-docstring implementation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/utils/auto_docstring.py#L3105)
prints documentation diagnostics. The
[Qwen3.5 implementation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py#L386)
selects a Torch recurrent fallback when optional kernels are unavailable.
[bitsandbytes 0.49.2](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/0.49.2/bitsandbytes/backends/cuda/ops.py)
calls the deprecated helper; its [upstream replacement](https://github.com/bitsandbytes-foundation/bitsandbytes/pull/1940)
is a separate dependency change. These sources explain message origin. Successful
loads/calls establish their nonfatal character in this saved run.

**Proposal.** Add a short load-result explanation for recognized messages and
the observed recurrent path. Keep raw stderr intact. Do not globally suppress
warnings, mask genuine errors, patch installed library internals, install FLA or
causal-conv1d opportunistically, or upgrade the lock to remove cosmetic output.
Any runtime change needs a separately identified package review and renewed
affected hardware/model evidence. No evidence shows that these warnings caused
the two wrong scalar answers.

## 4. Compact, accurate stage output: C2-03

[ui.py](../../recovery/i01/ui.py), `show`, compacts dictionary receipts but
embeds a list of full load receipts. In this notebook the load cell contributes
**843,099 serialized output characters**, while the entire notebook is 962,191
bytes. The embedded tensor/quantization inventories and repeated JSON are the
main source of output volume, not long agent conversations.

The reused loader also reports a 256-token configuration for its earlier loading
profile. [inference.py](../../recovery/i01/inference.py), `Adapter.__call__`,
sets the actual I-01 request settings before generation; all eighteen requests
record maximum 512. Displaying both without context encourages a false diagnosis.

**Proposal.** Show one row per slot: physical UUID, PID, actual model/revision,
load seconds, tensor-device acceptance, NF4/FP16 acceptance and recurrent path.
Show a compact I-01 per-call direct/thinking configuration separately. Retain
complete load JSON in the existing sessions table/export; link to it instead of
embedding every tensor. Display byte-verification progress after native file
fetches complete so the operator can distinguish hashing from stalled transfer.

**Acceptance.** Render the actual archived load receipts through the revised
presentation, confirm the full inventories remain downloadable and byte-correct,
and place a proportionate output-size limit on that one display fixture. Do not
retest model loading or weaken its underlying audit.

## 5. P0 envelope binding: C2-04

**Root cause.** [workflow.py](../../recovery/i01/workflow.py), `load`, defines
`replacing` using `process is None`, but a dead `Process` object can still be
non-None. `already_resident` correctly detects death later and a new successful
load record is written, while `reload_required` can remain false. `envelope`
checks that flag/session, but does not compare the prior receipt's `loads` with
the current pair before selecting the original call IDs. Those IDs return old
durable outcomes; the new receipt labels them with current load references.
`qualified` then compares those freshly relabelled references and accepts them.

**Reproduction.** The audit runs two scripted initial probes, changes slot 1's
successful load reference with no reload flag, and calls `envelope('direct')`.
It returns passed, produces **zero new probes**, adopts the new reference and
allows `qualified()`. This is a remaining hole in the earlier course-1 repair;
its tests covered replacements with the flag set, not flag-independent detection.

**Minimal fix.** Treat prior/current load-pair inequality as authoritative
invalidation, independently of advisory flags. A non-reload request must refuse
before reusing initial probe IDs when an earlier envelope belongs to another
pair. The explicit reload route must use the complete pair in its existing call
identity and charge the two probes to contingency. Set replacement metadata from
the actual successful new-load event, not just pre-loop nullable fields. Never
rewrite an old outcome as evidence for another physical load.

**Acceptance.** Cover a dead-but-non-None worker, explicit close/reload, a
same-controller single-slot replacement, a second replacement, and a fresh
controller. Each new pair after an accepted envelope requires two new charged
probes; an unchanged pair rerun charges zero. If no prior envelope ever existed,
the first selected-mode pair remains the two ordinary hardware attempts. Keep
qualified admission blocked on dead/unconfirmed workers.

## 6. P0 restore accounting: C2-05

**Root cause.** [cli.py](../../recovery/i01/cli.py), restore handling, and
[ui.py](../../recovery/i01/ui.py), `initialize(mode='restore')`, overwrite
`lost_spending` with `{upper: 0, resolved: true}` when the operator selects a
latest safe checkpoint. That choice describes **additional work after that
checkpoint**, not a resolution of an earlier gap already recorded inside it.

**Reproduction.** A temporary valid snapshot has a previously documented
three-attempt gap. Remaining allowance is 497. CLI restore with `--tail latest`
changes it to **500**, although the old affected-world block remains. This
forgets three already budgeted physical attempts and their contingency charge.
Course-2 itself has zero recorded gap, so its eighteen-attempt total is not
incorrect for this reason.

**Minimal fix.** Read and preserve the saved gap first. A verified zero new tail
must leave the saved bound/resolution unchanged. Additional bounded post-boundary
spending is added once to that saved bound; unknown prior or new spending keeps
admission unresolved. Retain affected-world blocks and evidence explaining both
boundaries. Use the existing metadata and admission calculation, with a small
shared restore operation for notebook/CLI rather than duplicate divergent logic.
Do not assume earlier uncertainty disappears when a ZIP passes integrity.

**Acceptance.** Both restore interfaces preserve prior zero, positive and
unresolved gaps; latest-tail zero never reduces prior charges; an additional
known tail consumes allowance/contingency once; unknown-tail restore refuses
generation but allows read-only reporting. Repeated inspection/reopen does not
double-charge or clear the gap. No new database or spending ledger is needed.

## 7. P0 canonical worker identity: C2-06

**Root cause.** [workflow.py](../../recovery/i01/workflow.py) supplies the same
`{'manifest': manifest}` binding to both stores.
[store.py](../../recovery/i01/store.py), `Store.validate`, checks schema,
integrity and that shared binding, but not the expected logical slot. Reopening
intact paths does not run the portable ZIP inventory check. Copying one complete
DB over the other can therefore pass validation even though one slot's unique
evidence is absent. Report dictionaries keyed by call/episode ID then obscure
duplicates while the attempt list counts them twice.

**Reproduction.** One scripted physical attempt is saved in slot 0. After closing
the fixture, its DB is copied over slot 1. `Session` accepts both; reported
attempts become **two for one distinct call**. This did not happen in course-2:
its two nine-call datasets have the expected distinct hardware/control IDs.

**Minimal fix.** Add an immutable expected-slot value to the existing canonical
metadata and validate it before writable opens. Also reject duplicate logical
call/episode IDs across slots and validate scheduled world/device placement in
read-only acceptance. Keep two existing DBs; do not introduce new identities or
another store. An expected path name alone is not sufficient evidence. Rejecting
identical file hashes alone is also wrong: legacy empty DBs can legitimately be
identical before slot metadata is introduced.

**Compatibility.** Existing files must not be silently recreated or assigned
new slot evidence on ordinary open. A narrow transition for a verified old
archive can validate its per-slot inventory, call IDs and schedule, record the
slot metadata explicitly, and preserve all prior admissions. Missing,
ambiguous or duplicated existing bytes require restoration/diagnosis first.
Coordinate this with C2-12 instead of bypassing existing source guards.

**Acceptance.** Correct slots reopen; swapped/copied/duplicated slots refuse
before writers and before generation; valid initial empty slots work; report
analysis fails with a precise consistency error rather than silently collapsing
duplicates. Original files remain untouched on refusal.

## 8. Thinking output versus runtime defects: C2-07

**Root cause.** [inference.py](../../recovery/i01/inference.py), `split_visible`,
returns `thinking_framing_defect` whenever the generated text lacks one closing
thinking delimiter. An output reaching the total cap while still thinking is a
normal model-output/protocol failure. [workflow.py](../../recovery/i01/workflow.py),
`call`, nevertheless sets global `model_defect` for **any** `framing_error`.
`episode` commits the invalid turn and then stops all subsequent dispatch as if
the backend/cache had failed. It also replaces the observable truncation label
with a framing-specific label that later maps to `provider_failure` in reports.

**Reproduction.** A scripted length-terminated thinking output without a closing
delimiter consumes one turn, leaves a nonterminal `[1,0]`-turn phase, and sets
the permanent runtime-defect flag. The fixture has no provider failure. No
thinking call exists in course-2; this is a future-path counterexample.

**Minimal fix.** Separate expected invalid model output from backend/request,
finite-score, cache or provider defects. A cap-hit unfinished reply is an invalid
`truncated_action`; malformed final framing or overlong visible output is a
protocol-invalid action with a recorded reason under the frozen rubric. Retain
all raw generated tokens, private thinking and the exact termination. Deliver
nothing, consume the invocation, and continue only if the phase has a later
legal turn. Never append a delimiter, extract a convenient JSON substring, or
repair the answer. Qualification/pilot gates still reject protocol defects as
specified; a main invalid turn is not automatically a global runtime failure.

Real numerical/cache/backend defects remain fail-closed. Recorded timeouts
retain their no-retry and termination-confirmation requirements. The fix changes
failure classification/control flow to match the adopted design, not the model's
generated text or decoding.

**Acceptance.** Tiny fixtures cover missing/duplicate delimiters, valid thinking
JSON, cap-hit reasoning, excessive visible output, malformed direct JSON, actual
provider/cache failure and a later legal team turn. Assert exact turn usage,
no delivered message, no forbidden resample, correct rubric and persistence before
effects. No real thinking qualification is needed for these software checks.

## 9. Consistent live reads: C2-08

**Root cause.** [report.py](../../recovery/i01/report.py), `read_run`, selects
episodes, calls, attempts and metadata separately without an explicit read
transaction. `status()` and inspection can run while an action writes. A new
call/admission committed between the calls and attempts queries leaves the
analysis input with an attempt whose call was absent from the earlier query.
The dictionary lookup in `analysis` raises `KeyError`.

**Reproduction.** A real SQLite commit is injected between these table reads.
Analysis raises **`KeyError('race-call')`** while the saved call and attempt are
intact. Course-2's quiescent archive reconstructs exactly; that does not test a
live read interleaving. Missing canonical DB corruption and this transient read
inconsistency are different diagnoses.

**Minimal fix.** Read all related tables/metadata from each read-only connection
inside one explicit SQLite read transaction. Keep WAL and the existing stores.
Live two-slot status may still describe a provisional observation across
independent workers; final export must remain quiescent and reconstruct exactly.
Do not substitute empty tables, drop orphan-looking attempts, invent zero cost,
or retry inference to make a status page render.

**Acceptance.** One barrier-controlled writer/read fixture must produce a
consistent old or new per-slot view, never a half-joined view. Verify no new
writes/inference by the reader, preserved writer admission, and exact quiescent
report reconstruction. A broad concurrency stress campaign is unnecessary.

## 10. Traceable partial reporting: C2-09, C2-10

### C2-09: link control labels to their actual calls

**Observed.** Both saved `wrong_submission` labels have `calls=[]` despite their
known exact call IDs. [report.py](../../recovery/i01/report.py), failure analysis,
extracts references only from team `events`; scalar control states have none.

**Proposal.** Derive references from calls matching that episode, falling back
to the control identity only after confirming the row exists. Keep event order
for team episodes. Exports should link directly to escaped conversation anchors
and preserve the frozen observable rubric. Do not convert a wrong scalar into
`obsolete_value_repeated` or infer internal anchoring.

**Acceptance.** The archived qualification-03 controls each receive their own
exact ID; all other controls retain no false failure labels. Existing team
labels retain event references and human annotations continue requiring notes
and valid call references.

### C2-10: show qualification before empty main results

**Root.** The general report foregrounds prefix/retain/clear rows even when all
executed work is qualification. The inspect helper chooses thinking only after
it passes, otherwise direct; a failed thinking screen can therefore leave the
main qualification table showing direct results. Default detailed call order
shows slot 0's six controls before the failed slot-1 controls.

**Proposal.** Add a small separate qualification table per evaluated mode:
world/input phase, physical slot, truth, returned scalar, correctness, protocol
status, tokens/seconds and exact trace link. State unexecuted modes explicitly.
Keep all twenty main unknowns, missingness bounds, failure-cost spending and
the distinction between qualification failure and recovery outcome. Prefer
failed controls in the bounded inspection preview, with complete evidence still
available using ordinary named commands. Do not require widgets/forms or move
scientific scoring into notebook cells.

Retain the final partial report and archive if any prerequisite fails. Do not
describe an automatically checkpointed report as proof that the notebook's
final-report cell ran. Preserve SVG/PNG raw plotting data and unknown semantics.
Clarify that zero dispatched calls on an unexecuted policy is an observed count,
not a known final logical cost: explicitly name observed counts or leave final
policy totals null until complete. Preserve the paired-cost table's existing
nulls rather than making unknown policies appear efficient.

**Acceptance.** Use this saved archive as an offline display fixture. Both failed
answers and original/revised truths must be immediately inspectable; a synthetic
failed thinking receipt must not hide its mode behind direct results; main
outcomes stay null. Do not infer a future treatment effect from the two controls.

## 11. Fixed session facts: C2-11

The executed number is 700, but the evidence string says twelve hours. This is
a shorter bound, not an observed deadline overrun. The missing explanation makes
the claimed quota difficult to audit. Neither notebook text nor this repository
can independently verify the provider's remaining session/weekly allowance.

**Proposal.** Keep the existing ordinary configuration cell. Echo requested
minutes, observation time, absolute UTC deadline and allowance evidence together.
If a conservative margin is intended, state it in the evidence. Preserve fixed
deadlines across reruns and require fresh observation for explicit refresh. Do
not supply a universal twelve-hour default, extend on every cell run, treat
observed-start time as provider allocation, or reuse this expired/future-run
deadline as current evidence. Explain that setup time is already spent.

This is a clarity improvement, not a mandate for new quota APIs or screenshot
upload flows. Existing actual-provider admission, per-call termination/export
margin and unknown-cost treatment remain in force.

## 12. Adoption into an in-progress study: C2-12

This run is bound to `8f5bcdb...`; the archive retains the matching complete
source/wheel. Changed production modules intentionally fail the source-binding
guard. Merely replacing attachments or editing `source_identity` would destroy
the provenance that makes the eighteen recorded outcomes reusable.

**Immediate preservation.** Keep the supplied notebook/ZIP and matching old
source. Read-only inspection requires no new model work. Do not reset the study
to zero, classify its eighteen known calls as new unbounded loss, add them to
the unrelated historical 45, or run a second direct screen under a new seed.

**Implementation choice.** Deliver a new matching notebook/source/wheel for
fresh studies. If these repairs must be adopted into this existing pre-main
study, implement a separately reviewed, narrow compatibility transition first.
It must name exact old/new code identities, verify unchanged scientific config,
worlds, schedule, prompts and request settings, preserve both original source
bytes and every recorded call/admission, and record the accepted implementation
transition through existing metadata. Plain reopen must never invent that
transition. Preserve old bindings as evidence; no blanket source check bypass.
The current implementation has no accepted transition tool, so do not describe
this as an already supported restore command.

A frozen study requires its own explicit change decision; this run has no
freeze. A proposal that cannot preserve these eighteen admissions must withhold
continued execution and present that limitation, rather than silently starting
an apparently fresh 500-attempt allowance. Keep this transition small and
specific, not a migration framework or second accounting authority.

## 13. Implementation order and focused acceptance

| Checkpoint | Deliverables | Required evidence |
|---|---|---|
| A: canonical/recovery correctness | C2-04, C2-05, C2-06, compatible adoption decision | Load-pair invalidation without flags; gap-preserving restore in both interfaces; slot refusal; unchanged source/input evidence |
| B: runtime/analysis correctness | C2-07, C2-08, C2-09 | Protocol versus backend distinction; one live-read interleaving; exact control trace references; raw-before-effects/idempotence retained |
| C: ordinary notebook/report clarity | C2-01–03, C2-10–11 | Archived load/qualification render fixtures; bounded output; explicit next decision; stable session window; no widget/action buttons |
| D: coherent package | Regenerated matching notebook/source/wheel/runbook and any explicit transition instructions | Source/wheel byte checks, outside-checkout isolated entry, cell compilation/scopes, restore/reconstruction, zero actual model calls |

Reuse existing exact-resume, retry/500/28, missing-DB, archive/expanded restore,
source-isolation and notebook checks. Add only the focused counterexamples above
and any regression their implementation requires. Run checks appropriate to
changed behavior; no independent extensive CPU campaign, GPU staging, actual
qualification, pilots or main execution during software repair. Commit at these
logical boundaries and update the existing WBS/handoff with executed receipts.

## 14. Later Kaggle validation and bounded continuation

Once repairs/package compatibility are accepted and actual execution is
authorized, validate the affected target-host paths with the original frozen
scientific conditions. Code/scripted acceptance cannot prove future model
competence or long-envelope memory. The execution order remains:

1. Open/restore with exact source identity and truthful tail evidence; reconcile
   any unresolved attempt/termination/spending before admission. Record a fresh
   actual window for the current controller. Preserve the eighteen known calls.
2. Load current workers with verified pinned files. Inspect existing direct
   qualification without resampling. If chosen, execute only the justified
   twelve-control thinking screen. Its failure remains a failed screen.
3. Only after a passing selected mode, run its two actual full-envelope probes.
   In this run there is no previous envelope, so these are the two remaining
   ordinary hardware attempts. After an accepted envelope, replacement-load
   pairs require two separately charged contingency probes as specified.
4. Execute each pilot separately, inspect complete conversation/controls/costs,
   save its checkpoint, and record actual communication/usability findings.
   Freeze only after all required pilots and a measured adequate forecast.
5. Prepare/run/review fixed one/two-world main scopes, then partial/final report,
   verified archive and explicit close/provider-stop observation. Never let a
   successful stage authorize the next automatically.

Budget arithmetic remains **18 already spent + 12 possible thinking + 2 initial
envelope + 60 pilot + 380 main = 472 planned first attempts**, with at most 28
shared contingency and the 500 hard ceiling. Loads/downloads do not erase or
add generation attempts. Available allowance, finite outputs, cache isolation,
selected full-envelope headroom, model competence, pilot usefulness and live
interrupt/restore/download behavior must all be observed where required.

No code audit can promise that future GPU execution will never fail. The concrete
objective is to close the demonstrated holes, classify failures correctly,
preserve evidence/spending, stop at the appropriate boundary and make the next
legal operator action clear.
