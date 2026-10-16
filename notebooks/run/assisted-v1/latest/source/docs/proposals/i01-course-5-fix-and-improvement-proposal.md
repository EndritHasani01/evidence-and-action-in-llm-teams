# I-01 course-5: fix and experiment-improvement proposal

15 October 2026. **Proposal only. No code, settings, gates, original plan, saved
responses or checkpoints are changed; no inference is run.** The user requested
analysis and recommendations, not adoption of a new scientific procedure.

Evidence: [complete course-5 analysis](../validation/i01-course-5-results-analysis.md),
[executed notebook](../../notebooks/run/course-5/multi-agents-course-v3nb.ipynb)
and [selected checkpoint](../../notebooks/run/course-5/latest.zip).
Authority remains [specification section 12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).

## 1. Recommended decision

Keep the strict validator and preserve both invalid actions. **Do not fix this
by coercing the replies or marking the original gate passed.** Both replies are
valid JSON with illegal message-plus-wait combinations, and the current
precommitted pilot policy explicitly rejects them.

For the stated objective—measuring recovery after a source change in an
error-prone distributed conversation—the best limited amendment is:

* Keep scalar qualification, baseline pilot interface/completion, backend/cache,
  headroom, source, durability, spending and measured resource prerequisites.
* Treat ordinary **post-revision team action errors and noncompletion as measured
  recovery outcomes**, rather than as grounds to abandon the whole study.
* Continue all three fixed pilots, then all twenty fixed main worlds if the
  amended objective prerequisites and resource forecast pass. Never replace a
  bad world, fix an answer, resample a recorded call or select on effect direction.
* Keep communication/mechanism review retrospective and visibly pending.

This narrower change retains valid, completed original-team interaction and
protocol-valid full-information controls as feasibility checks. It removes
admission selection on the very retain/clear recovery failures being studied.
Course-5's current prefix and controls satisfy that proposed baseline; its two
violations both occur after revision. This is **not** an implemented or
historically precommitted pass.

Make the diagnostic and failure-cleanup improvements at the same time. Defer
prompt redesign, new action semantics, thinking, model changes and larger budgets
to a separately approved experiment variant. This avoids changing several
scientific factors merely to get past one observed pilot.

## 2. Confirmed root cause and the integration trap

Both failing replies have a nonempty string in `message`, null `submit`, and
`wait: true`. In [core.py](../../recovery/i01/core.py), `validate_action()`
correctly enforces that waiting has neither a message nor a submission. Both
replies terminate normally below 512 tokens. There is no demonstrated malformed
JSON, truncation, provider fault or input overflow.

The stop chain is:

1. `scope_evidence(..., pilot=True)` evaluates all pilot phases and controls.
2. `check_pilot(1)` saves `valid_protocol: false` and raises.
3. The controller exports an error checkpoint; the notebook raises `ActionStopped`.
4. Subsequent pilot/main cells do not execute.

There is also a later rejection in `freeze()`: it reconstructs pilot eligibility,
rejects pilot truncation/provider/framing flags, and rejects any pilot episode
event error. **Changing only `check_pilot()` or one boolean cannot repair the
whole workflow.** It would likely move the stop to automatic main admission.

The original plan is bound before calls, and active code is source-bound.
Changing a notebook field or mutating a status record is not a legitimate way
to apply a different policy. The policy, revalidation and source-transition
interfaces must agree.

## 3. Distinguish three kinds of failure

| Category | Course-5 example | Appropriate handling |
|---|---|---|
| Mathematical/coordination outcome | Local 923 finalized too early; stale 988; invented 1023; missing submission/deadlock | Preserve exact response, score the terminal outcome, report effort and mechanism uncertainty |
| Ordinary model action violation | Parseable JSON containing both a message and waiting | Reject the action under the current semantics, consume its turn, record the violation; proposed recovery admission treats it as an outcome |
| Infrastructure/evidence failure | Missing raw output, unknown spending, unconfirmed timeout termination, broken cache/numerics, corrupt store/source | Stop admission, preserve evidence, diagnose/reconcile before any continuation |

Valid JSON is not identical to a legal action. Conversely, an illegal action is
not necessarily an infrastructure defect. The two current rejected messages
must stay invalid even if their presence ceases to veto the entire experiment.

The integer 1023 is an example of a **legal wrong answer**. Clamping it to the
input range, replacing it with a shard maximum or requiring it to be an actual
input value would conceal scientific error and change the task.

## 4. Proposed automatic admission contract

Record a new, explicit policy version; do not edit the meaning of
`i01-whole-study-run-all-2026-10-15` retrospectively. Keep the original plan and
failed result as history. The table below is a proposal for the new policy.

| Check | Proposed decision | Reason |
|---|---|---|
| Exact model/runtime/source/input/prompt/decoding binding | Blocking | Reproducibility and strict isolation |
| Current-load readiness and full headroom | Blocking | Actual backend feasibility |
| Twelve qualification controls committed and protocol-valid | Blocking | Existing full-information interface qualification |
| Mathematical accuracy of legal controls | Diagnostic | Wrong mathematics is an outcome |
| Every planned pilot phase/control terminal with committed raw/effects | Blocking | Missing evidence cannot become a scored failure |
| Pilot original-team actions legal and both submissions present | Blocking, correctness-free | Minimal baseline interface/completion prerequisite, preserved from current intent |
| Pilot original/revised controls legal | Blocking, correctness-free | Separate complete-input interface evidence |
| Ordinary retain/clear wrong, malformed, truncated or noncompleting actions | Diagnostic; preserve invalid/failure scoring | These are post-revision recovery behavior |
| Confirmed terminal recovery timeout | Recorded failed outcome if cleanup is confirmed | Do not confuse a known failure with unknown process/exposure state |
| Real provider/cache/numerical defect or unconfirmed termination | Blocking | Invalid runtime/evidence cannot support interpretation |
| Unknown spending, unresolved admission or corrupt/missing DB/source | Blocking | Preserve accounting and unknownness |
| Communication quality or effect direction | Retrospective diagnostic | No invented human judgment or favorable-result gate |
| Attempt/time/export forecast | Blocking | Finite resource feasibility |

“Ordinary” output failure must be identified from existing raw/backend evidence;
it cannot be a blanket classification of every exception as harmless. A timeout
with uncertain process death remains blocking. A genuine cache/numerical defect
cannot be hidden as a malformed response.

Under this proposed split, pilot 1 has a valid three-call original phase,
both final original submissions, two valid controls, complete durable recovery
phases, no backend defect and no spending uncertainty. Its recovery errors remain
two invalid actions, and its team scores remain `0/0/0`. A new eligibility result
could be derived **only after adoption**; nothing becomes mathematically correct.

### Why this is scientifically defensible—and what changes

The primary question concerns practical retain/clear recovery. A rule requiring
perfect protocol behavior throughout both pilot recovery conditions can prevent
observing the failure process that the main analysis already counts as outcome.
The recommended gate aligns feasibility with evidence quality while leaving
post-revision behavior measurable. It applies identically to retain and clear,
without an error-rate threshold chosen to fit this one pilot.

This is still data-informed protocol development after inspecting pilot 1.
Disclose its timing and rationale. Main outcomes are unobserved, which limits
main-outcome selection risk; it does not make the amendment preregistered.
Keep the original stricter gate outcome visible.

A disjoint pilot feasibility gate is not itself cherry-picking main worlds;
keeping it strict can be legitimate for a protocol-compliant-system target.
The concern here is its fit to the requested recovery question and the resulting
feasibility selection, not proof that an unexecuted main estimator is biased.

The resulting study measures the **complete implemented systems**, including
action mistakes, information loss and finalization. It does not isolate a pure
memory/anchoring mechanism. Preserve all twenty main worlds and the prespecified
correct-prefix descriptive stratum. Do not silently change the primary target
to successful-prefix or valid-reply-only cases.

If the intended question instead requires an almost perfectly compliant team
interface, keep the original strict gate and report the present result as a
feasibility failure. Then improve protocol elicitation in a new prompt condition
before main. Both choices are defensible; claiming to have measured full main
recovery under the unmodified strict gate is not.

An even broader policy allowing incomplete/invalid original pilot teams would
be another change. It is not necessary to address these two current recovery
violations and is not silently included in this recommendation.

## 5. Minimal complete implementation scope, if approved

| Component | Required work | Boundary |
|---|---|---|
| Specification and living handoff | Adopt the new baseline/recovery distinction and disclose pilot-informed timing | No changes to thesis sections 1–11 |
| `recovery/i01/policy.py` | Name the policy; derive detailed validity categories and phase-sensitive eligibility | Preserve old policy interpretation; no generic policy framework |
| `workflow.scope_evidence()` | Separate original-team, control and recovery diagnostics | Strict parsing and state effects remain unchanged |
| `workflow.check_pilot()` | Save phase-specific checks, failure/warning call IDs and the actual applied policy | No forced `passed=True`, no human-approval fiction |
| `workflow.freeze()` / `admit_main()` | Reuse the same adopted eligibility calculation; remove contradictory automatic-path rejections for allowed recovery outcomes | Keep legacy strict behavior for its own policy, current-load/resource gates and immutable settings |
| Source/plan validation | Add a narrow explicit course-5 pre-main policy transition, if continuation is chosen | Preserve old plan, raw calls, states and budget |
| `report.py` / notebook presentation | Distinguish syntax/schema/action validity, baseline checks and recovery outcomes; show exact failing calls | Keep primary scoring, missingness, costs and all-world denominators |
| Run All failure cleanup | Safe export followed by bounded worker closure when unattended execution stops | Never close unconfirmed active work as if settled; provider release stays unknown |
| Builder/release review | Matching notebook, wheel, source manifest, runbook and gate descriptions | Old upload cannot accidentally use the new notebook or policy |

Automatic main admission should consume one consistent derived eligibility result.
Do not maintain an updated first gate plus an old broad “any pilot error” check.
Use the existing canonical metadata, states and raw outcomes; a second progress
database, new orchestration service or generalized registry is unnecessary.

The current parser and action-application code need no permissive change to
address the observed rejection. Diagnostic explanation can live alongside the
existing policy/report derivation rather than changing core scientific behavior.

## 6. Diagnostics that would prevent this confusion

For every rejected call, derive and export:

* Exact call/world/phase/agent/invocation and existing seed reference.
* `json_valid`, `schema_valid`, `action_valid`, framing/provider/truncation flags.
* A precise reason such as `wait_requires_null_message_and_submit`.
* Raw/visible reply, committed effect status, and whether a message was delivered.
* Whether the reason blocks admission under the **recorded policy**, or is a
  measured recovery failure.

Do not replace the historical `malformed_action` label; add a compatible derived
explanation. For this checkpoint both events would be syntax-valid, schema-valid,
action-invalid and not delivered. Their individual call IDs should lead the
failure display. Always include failed raw replies before successful examples
when a bounded audit preview is used; the current first-six view hides one of
the two relevant calls.

Keep phase-level failure summaries, but distinguish their broad call lists from
exact offending events. Show a persistent “scientific gate blocked” status beside
the successful error snapshot, so `snapshot: complete` cannot be read as resumed
research. Avoid a new competing status store: derive this from the saved gate and
stage receipts.

## 7. Safe continuation of the 32-attempt study

**No automatic transition currently supports this checkpoint.** Existing
`continue-checkpoint` is restricted to reviewed `8f5bcdb` source, pre-experiment
evidence and no prior envelope. Course-5 uses `39ad71b`, has an envelope and has
executed a pilot. Its command must not be reused by pretending it is a course-3
checkpoint. Ordinary restore with identical source can inspect/replay it, but
will reproduce the strict failed gate.

If a policy-only continuation is approved, implement this narrow sequence:

1. Verify the exact selected ZIP, source inventory, worker bindings, planned
   worlds, 32 completed admissions and original plan. Require no main attempt or
   main-admission/freeze record. Verify the approved policy-only code difference;
   core math/views/prompt/action semantics, inference/runtime, config, seeds,
   schedules, scoring and bounds must remain exact.
2. Restore into a fresh writable destination. Preserve the original ZIP, source,
   manifest, old plan, failed gate, requests, raw outcomes, effects, states,
   annotation history and spending. Use existing backup/extraction primitives.
3. Retain both original and active source and a traceable approved policy
   amendment, using the established implementation-transition pattern. Do not
   overwrite `execution_plan`, old source identity or old `passed: false` as if
   the new rule had existed before pilot 1.
4. Derive new eligibility from unchanged evidence. Confirm byte-for-byte equality
   of saved scientific rows and exact outcome/cost reconstruction. The new
   decision is a disclosed amendment; it is not a replayed historical pass.
5. Obtain real prior-exit and post-boundary exposure evidence. The ZIP's zero
   in-flight count does not prove no generation occurred later. Reuse the existing
   latest/unknown-tail and lost-spending rules; an unknown tail remains blocking.
6. In a new session, verify the active source/native/runtime evidence, record a
   fresh time window, load workers and perform the two existing **contingency-
   charged** current-load probes. Do not repeat the twelve completed controls or
   pilot 1's calls. Existing outcomes remain immutable and spent.
7. Complete pilots 2/3 under the disclosed amended gate, then evaluate actual
   resource feasibility and execute the same fixed twenty-world main population.
   Restore/replay and numbered-cell reruns must never advance another scope.

Budget for this policy-only route, assuming no extra exposure or retry:

| Component | Physical attempts |
|---|---:|
| Already recorded, preserved | 32 |
| Two remaining pilots, at most | 40 |
| Twenty main worlds, at most | 380 |
| Ordinary total at those ceilings | 452 |
| One new-session reload pair, charged to reserve | 2 |
| Total with that pair | 454 |
| Reserve left after that pair | 26 of 28 |

The 468 arithmetic remaining at the current boundary is not permission to create
extra worlds or to spend terminal pilot 1's unused turns. With at most 28 total
contingency attempts, the above realized-prefix ceiling would be 480 overall,
including the reload pair, before any separately reconciled exposure constraints.
No old attempt disappears and no new independent 500-call allowance is assumed.

If the user instead chooses a fresh new prompt/protocol cohort, define its
budget and authorization explicitly. Preserve course-5 as historical pilot
development evidence and never pool its responses as if the new prompt produced
them. This document authorizes neither a new quota nor any execution.

## 8. Prompt improvements as a separate versioned option

The trace suggests concrete misunderstandings, but not a need for thinking mode:
the model invents an extra agent and shard element, finalizes a local answer,
awaits a finalization confirmation that the protocol does not provide, and
combines messaging with waiting.

Useful common-to-both-conditions clarifications for a future prompt version are:

1. State the two IDs explicitly: 0 and 1; identify the partner consistently.
2. State that each shard has twenty current records and that record indices are
   zero-based. Keep all private records private; do not show the partner's shard.
3. Explain that **each** agent needs its own final submission of the global
   maximum; one agent submitting does not finish the other. Submission cannot be
   amended within a phase, and later messages cannot reopen it.
4. Show the valid message-only and silent-wait forms. For example:

   ```json
   {"message":"A message to the partner","submit":null,"wait":false}
   ```

   ```json
   {"message":null,"submit":null,"wait":true}
   ```

   Explain that message-plus-wait is forbidden and that no host confirmation will
   arrive from a finished partner. Do not repair a violating reply afterward.
5. Clarify phase reopening after the factual revision and current private-source
   authority. Preserve literal retained history; do not tell retain to discard
   history or supply a host-certified corrected answer.

Avoid answer-bearing few-shot values or a host-written solution protocol that
changes the natural collaboration target. Strong “exchange local maxima then
agree” scaffolding might improve task success, but is a substantive intervention,
not merely a formatting fix. Label and evaluate it separately if desired.

Any prompt change alters rendered inputs and possibly the distribution of model
actions. Version it, apply it symmetrically, recheck native token bounds, freeze
before main and handle requalification/budget explicitly. Never continue old
episodes with changed prompts under the same saved call IDs. There is no evidence
yet that these proposed clarifications will reliably eliminate the errors.

## 9. Changes that are not recommended as quick fixes

| Candidate | Why it is insufficient or scientifically costly |
|---|---|
| Set `valid_protocol=True` or delete the first check | Hides the actual violation; later `freeze()` still rejects; contradicts immutable policy |
| Flip `wait` to false in saved JSON | Changes execution, delivered messages, future prompts and sampled outcomes |
| Deliver the message despite rejection | Changes a treatment's information flow; downstream replies cannot be reused as counterfactuals |
| Allow message-plus-wait as a new legal action | Potentially reasonable future protocol, but changes waiting/delivery semantics and requires a new condition/version |
| Rerun the same pilot until it passes | Resamples recorded outcomes, spends more and selects favorable behavior |
| Increase turns or output tokens | Current errors are 50/65-token EOS replies; changes ceilings/interaction semantics without evidence of solving the cause |
| Clamp 1023 or fill missing submissions from history | Conceals wrong answers and noncompletion, violating exact scoring/finality |
| Switch to thinking or a new model | No demonstrated remedy for this action combination; prior course-3 thinking evidence is costly and incomplete |
| Set a threshold of two tolerated errors because two occurred | Outcome-tuned threshold with no independent rationale |
| Use an LLM judge to approve conversation quality | Adds an unapproved evaluator and does not establish protocol correctness |

Grammar/schema-constrained generation is another possible future intervention,
but it changes the generator's distribution and may remove an error class from
the phenomenon being measured. It should constrain structure/action syntax only,
not choose correct numerical values. Runtime compatibility, bounded decoding,
token accounting and scientific comparability would require explicit work. It
is not the smallest next change and no new dependency is recommended here.

## 10. Reliability and operator improvements

### Error cleanup without losing evidence

Course-5's error export succeeds, but the final close cell does not execute.
For unattended Run All, add a policy-aware failure finalizer: stop new admission,
settle or boundedly terminate active calls, preserve a truthful partial report/
checkpoint, then close resident workers with actual process acknowledgements.
Record cleanup failure explicitly and preserve the previous good archive.

Reuse the current controller/client and locks. Do not recursively call another
notebook action while its busy lock is held, race a checkpoint against active
effects, or convert unknown termination into confirmed death. A paused manual
inspection session can retain models deliberately; the unattended error path
should not leave residency as an unnoticed default. Closing workers still does
not establish provider deallocation; the operator must stop Kaggle.

### Honest clock and forecast evidence

The estimated deadline correctly remains fixed across setup, but the saved
`window.observation.remaining_minutes` becomes null when initialization reapplies
only an absolute deadline. Preserve the original observation/planning timestamp,
700-minute value and estimate/observed basis through that handoff in the existing
window receipt. Keep provider quota/assignment/release separately unknown.

Show the measured forecast beside remaining pilot/main work and export margin.
After only one pilot the reconstructed main-only heuristic is about 101.49
minutes; it excludes the two remaining pilots and is not a guarantee. Do not use
this number to promise twelve-hour completion or increase timeouts. Incorporate
remaining work and measured checkpoint overhead before claiming a whole-run
forecast; distinguish serial conservative estimates from actual parallel batches.

### Preserve existing successful engineering

Keep source-only input, exact source/wheel checks, verified pip bootstrap,
headless isolated processes, pinned dependencies, native checks, current-load
headroom, literal private views, WAL/FULL raw-before-effects, global admission,
numbered fixed batches, replay, checkpoints and read-only reporting. Course-5
does not justify rebuilding these systems or upgrading the runtime.

## 11. Improve scientific reporting and interpretation

Report action compliance as separate syntax, schema and legal-action measures,
with explicit phase/group denominators. Course-5 has 10/10 parseable team replies
and 8/10 legal team actions; scalar controls are a different context. Do not
combine forced headroom outputs with scientific JSON rates or mistake repeated
fixed controls for independent populations.

Retain the primary twenty-world paired exact-success analysis, unknown bounds,
stratified exploratory bootstrap and correct-prefix descriptive stratum. Report
effort jointly with success and terminal reason. Clear's 15.496-second lower
pilot cost ends in deadlock, so it is not successful-recovery efficiency.
Complete-case or successful-only summaries cannot replace intended populations.

Use retrospective call-linked labels for obsolete-value repetition, premature
finalization, role/index claims, message delivery failures, waiting deadlock and
noncompletion. Separate observable events from inferred internal mechanisms.
Do not claim that the wrong 1023 was caused by forgetting or that repeated 988
proves a particular anchoring mechanism. No native-benchmark or broad superiority
claim follows from this controlled extension.

Keep a development/amendment chronology: earlier mathematical gate, direct-only
protocol amendment, Run All procedural amendment, course-5 observations, then
any new recovery-admission or prompt change. Main data collected afterward must
identify the actually used version. Do not erase the stricter failed pilot.

## 12. Focused validation required for a later implementation

No extensive CPU campaign or GPU research run is needed to validate code changes.
Use targeted saved/scripted checks plus the existing evidence:

1. Replay both exact rejected replies: JSON/schema pass, action validation fails;
   no message or submission is delivered and the turn is consumed.
2. Old strict policy still blocks these pilot errors; the adopted new policy
   derives a separate decision with unchanged raw replies, states and costs.
3. Baseline prefix/control defects, unresolved admissions, real backend defects,
   source mismatch and inadequate time remain blocking under the new policy.
4. Both the pilot gate and automatic main admission use the same phase-sensitive
   policy. Explicitly test the later unconditional error checks to prevent a
   moved failure at `freeze()`.
5. A course-5 continuation preserves the original study ID/plan, all 32 attempts,
   exact requests/outcomes/effects and the old failed gate. No control or pilot 1
   reply is resampled. Reject changes to model, prompts, seeds or math in the
   policy-only route; reject main/frozen or unresolved-boundary transitions.
6. New workers require exactly the existing two reserve probes; unchanged load
   reruns reuse evidence; unknown tails and earlier gap charges survive restore.
7. A scripted full Run All containing recovery protocol mistakes still reaches
   every fixed main world under the new policy, reports the failures honestly,
   verifies the portable archive and closes workers. Repeating a numbered cell
   spends zero calls and never advances a different scope.
8. Unattended failure cleanup exports before closing safely, handles a failed
   export without deleting the last good ZIP, and never asserts unknown death
   or provider release. No new retry is hidden in cleanup.
9. Diagnostic/report CSV/HTML state the exact violation, applied policy and
   pending human review. Both source-matched notebook names retain ordinary
   stage cells, no approval forms, and correct total attempt caps.

Prompt changes, if separately chosen, additionally need native-tokenizer/private-
view/bound checks and later target-host qualification. CPU fixtures cannot prove
future model compliance, collaboration quality or completion time.

## 13. Proposed delivery sequence and decision boundary

| Priority | Deliverable | New inference needed to implement/verify |
|---|---|---|
| P0 | Precise diagnostics, persistent failed-gate explanation, safe unattended cleanup | Zero; saved/scripted checks |
| P1 | Explicitly adopted recovery-phase admission amendment covering pilot and main gates | Zero; requires scientific approval before changing the contract |
| P1 | Narrow course-5 source/policy transition, if continuation is selected | Zero for implementation; later actual reload probes are two charged calls |
| P1 | Matched notebook/source/wheel/runbook/report release and focused evidence | Zero |
| P2 | Symmetric role/finality/wait prompt clarification as a separate version | New empirical validation later; budget/design must be explicit |
| P3 | Constrained decoding, new action space, larger study or model comparison | Separate research variants, not necessary to resolve the present stop |

The smallest scientifically coherent next implementation is **diagnostics + the
approved phase-sensitive gate + all dependent main-admission checks + explicit
source/plan handling + safe cleanup**. It requires neither thinking mode nor
repairing the model's output. Until adopted, the current source should continue
to report pilot 1 as blocked, exactly as the saved evidence shows.
