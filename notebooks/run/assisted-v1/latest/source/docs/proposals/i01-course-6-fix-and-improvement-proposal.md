# I-01 course-6: repair and experiment-improvement proposal

15 October 2026. **Proposal only. No implementation, policy adoption, changed
prompt, checkpoint migration or inference is authorized or performed by this
document.** Evidence is the [complete course-6 analysis](../validation/i01-course-6-results-analysis.md),
[executed notebook](../../notebooks/run/course-6/multi-agents-course-v4nb.ipynb)
and [selected archive](../../notebooks/run/course-6/latest.zip).
[Specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
remains authoritative. Historical policies, failed gates and source packets must
retain their original meaning.

## 1. Recommendation

Keep strict action validation and all saved invalid outcomes. For this practical
recovery objective, the best next design is to **qualify the scalar interface
once, then treat ordinary sampled pilot/team behavior as outcomes in every
phase**, while keeping runtime, privacy, durability, source, spending, termination,
capacity and measured resource requirements blocking.

That means original-prefix malformed/waiting/wrong/noncompletion behavior would
be handled consistently with retain/clear behavior after successful fixed
qualification. Pilot full-information controls would still all execute and be
reported, but ordinary sampled invalid or wrong replies in those later controls
would be diagnostic under this recommended version. They would not become a
second, undeclared qualification screen. Genuine provider defects anywhere
would still block. The existing twelve direct qualification controls would
remain strict and correctness-free.

This is a **new scientific admission amendment**, broader than the adopted
course-5 repair. It is recommended, not silently applied. It aligns pilot
admission with a main experiment that already counts ordinary model mistakes
and incomplete collaboration as outcomes. It also avoids merely moving the
stop from prefix legality to another sampled-team outcome prerequisite.

If the research instead requires a reliably protocol-compliant collaborating
system before studying memory, retaining the current strict gate is defensible.
Then the honest result is a feasibility failure, and the next cohort should
improve protocol elicitation before main. Do not call a policy-only relaxation
evidence that collaboration itself improved.

The default implementation direction, if later approved, should respect the
user's expressed preference for a complete **fresh Run All**, with a newly
identified plan/source/destination and no old-result import. An optional
continuation route is discussed separately; it is not currently implemented for
course-6 and should not be added unless selected.

## 2. What failed and what the previous repair already fixed

Course-6 uses the expected `b92cdbf` source and
`i01-recovery-admission-run-all-2026-10-15` policy. Pilot 1 now passes with its two
ordinary invalid recovery replies preserved. Source/wheel/cells match; all 32
calls shared with course-5 have identical requests and generated tokens.

Pilot 2's blocking call is:

```text
pilot-01/prefix/agent-1/invocation-0
JSON valid: true
Schema valid: true
Legal action: false
Reason: wait_requires_null_message_and_submit
Runtime safe: true
Admission blocking: true
```

Its nonempty message is combined with `wait: true`; the reply ends at EOS after
149 tokens. Both original agents later submit, so completion, raw/effects,
spending, runtime and checkpoint checks all pass. Only the strict original-
prefix protocol requirement blocks. Pilot 2's other illegal action, in clear,
is already diagnostic.

The root-cause layers are distinct:

| Layer | Finding | Consequence |
|---|---|---|
| Generated action | The model combines communicating and waiting, despite an explicit prohibition | Reject that action and preserve its consumed turn |
| Admission design | Perfect prefix legality remains mandatory after relaxing recovery legality | A transient ordinary prefix error vetoes the entire study |
| Top-level diagnosis | The exception says only `valid_protocol` | The operator has to inspect detailed evidence to learn which phase blocks |
| Scientific behavior | Both pilots' original teams and all four recoveries are wrong/incomplete | Passing an amended gate cannot establish useful collaboration or a treatment effect |

The validator, scheduler and view boundary are not demonstrated defects. In
particular, agent 1's consecutive original turns are correct: agent 0 is waiting
until a legal delivered message wakes it. The rejected 149-token text is never
delivered. Claims about seeing a partner shard are contradicted by the exact
permitted view, not evidence of host leakage.

## 3. Choose a principle before changing another gate

There are three coherent options. Do not implement a tolerance threshold chosen
because precisely one prefix violation occurred.

| Option | What changes | Scientific tradeoff |
|---|---|---|
| Keep the current gate | Nothing scientific; improve diagnostics only | Valid for a compliant-team feasibility target; course-6 remains blocked |
| Narrow completion-based baseline | Permit ordinary prefix errors if both original submissions eventually exist; keep pilot controls strict | Resolves this run with less amendment, but original noncompletion or a later control violation can still stop future runs |
| **Recommended: post-qualification recorded-outcome policy** | Ordinary behavior in all pilot phases/controls is diagnostic; require terminal durable evidence and intact runtime/resources | Fits the all-world error-prone-system target, avoids outcome-based pilot vetoes, but accepts the possibility of an uninformative floor-effect study |

The middle option is not inherently wrong, and it would admit pilot 2's present
evidence. Its residual completion/control gates must be intentional and disclosed;
it cannot be advertised as preventing future stops on ordinary sampled behavior.

The recommended option changes **admission**, not legality or scoring. An illegal
wait remains illegal, its message remains undelivered, its turn remains spent,
and a terminal failed phase remains score zero. A missing or unresolved phase
remains unknown and cannot be promoted to a measured failure just to advance.

### Why the recommended amendment is scientifically defensible

The primary target is a practical retain/clear contrast across twenty fixed
worlds, including imperfect original conversations and recovery failures. Original
mistakes can be exactly the material carried into retain, while clear removes
that history. Once scalar interface/runtime compatibility is established,
ordinary team mistakes are part of the implemented system's behavior.

A disjoint pilot feasibility gate is not proof that a main estimator is biased;
main worlds have not been selected or executed. However, repeatedly changing a
gate until the current pilot passes creates a weak, data-informed development
process and an unclear target system. A fixed rule covering ordinary behavior
across all phases is more principled than another exception tied to this call.

Keep a transparent chronology: original mathematical qualification; direct
protocol-first amendment; whole-study automatic progression; recovery-only
admission; course-6 prefix failure; then any approved broader amendment. The
next rule is not preregistered relative to these development pilots. Main
outcomes remain unobserved, which limits main-outcome selection risk but does
not erase development-informed decisions.

### Risks that a passing gate cannot remove

- **Floor effects:** both original teams and all four recoveries currently fail.
  A complete study could produce mostly zero paired outcomes and little evidence
  about a useful recovery benefit. Report that result; do not select easier
  worlds, extra seeds or a new success threshold after inspecting it.
- **Interpretation:** the contrast concerns the complete implemented systems,
  including bad messages, private finalization and protocol mistakes. It does
  not isolate pure memory, forgetting or anchoring.
- **Diagnostic stratum:** the prespecified correct-prefix descriptive subset
  may be small or empty. Do not replace the twenty-world primary target with
  successful prefixes or protocol-valid-only calls.
- **Operational safety:** “ordinary model outcome” cannot be a catch-all for
  missing replies, source mismatch, unconfirmed termination or cache/numerical
  faults. Those undermine evidence and must still block.
- **Capability claims:** 12 legal scalar controls and 10 correct answers show
  only a small full-information interface screen. They do not qualify natural
  collaboration, and repeated identical screens are not independent worlds.

## 4. Proposed admission matrix

Bind a new explicit policy version before any new dispatch. Reuse the existing
execution-plan field and gate receipts; no new database, policy registry,
framework or identity service is needed. Preserve the old version's semantics.

| Evidence or outcome | Recommended new handling |
|---|---|
| Fixed twelve direct qualification controls | All twelve committed and protocol-legal; mathematics diagnostic; no replacement or resampling |
| Source/model/runtime/prompt/settings binding | Blocking |
| Native checks, distinct T4 placement, finite/cache evidence | Blocking |
| Current-load full input/output headroom | Blocking; preserve two-probe load-pair binding and reserve charges |
| Every scheduled pilot episode/control has terminal committed evidence | Blocking; unresolved/unexecuted evidence is unknown |
| Pilot original-team wrong answer or ordinary malformed/truncated/framing action | Diagnostic; reject invalid action, consume turn, retain exact outcome |
| Original-team deadlock/horizon/noncompletion with genuine terminal evidence | Diagnostic; record failed outcome, never fabricate submissions |
| Retain/clear wrong/invalid/noncompletion | Same diagnostic treatment |
| Later pilot-control ordinary wrong/invalid output | Diagnostic after the fixed scalar qualification; controls still execute and remain visible |
| Known timeout | Failed outcome only with confirmed termination; current replica health still required before further dispatch |
| Provider/cache/numerical defect or unconfirmed process death | Blocking |
| In-flight/unreconciled admissions, unknown spending, missing/corrupt source/DB | Blocking |
| Attempt/time/export forecast inadequate | Blocking |
| Message quality, number of messages, effect direction | Retrospective diagnostic; no fabricated human review or LLM judge |

Keeping strict initial qualification does not promise no future qualification
failure. It is an explicit prospective interface prerequisite. Changing that
screen would be a separate decision; this proposal adds neither an always-pass
switch nor an unspecified number of attempts until twelve good replies appear.

## 5. Implement the policy coherently, not at one exception

If the broader policy is approved, all of these existing interfaces must agree:

1. **Authority and plan:** amend specification §12 explicitly; identify fresh
   study scope, gate version and the decision to defer or adopt prompt changes.
   Preserve model, config, schedule, views, strict action semantics, seeds,
   inference, scoring and populations unless separately approved.
2. **Policy helper:** extend [`policy.py`](../../recovery/i01/policy.py) with the
   new version's ordinary-outcome classification. Keep `outcome_action()` and
   the core validator unchanged. Maintain strict interpretation of historical
   `AUTOMATIC_POLICY` and `RECOVERY_POLICY` data.
3. **Scope reconstruction:** in [`workflow.scope_evidence()`](../../recovery/i01/workflow.py),
   handle both the per-call `admission_blocks()` result **and** the independent
   prefix/control state-event-error check. For the recommended version,
   `original_team_completed` and ordinary pilot-control validity are diagnostics,
   not hidden hard checks. Preserve committed/terminal/every-episode requirements.
4. **Pilot progression:** `check_pilot()` stores a versioned decision from
   immutable evidence; next-pilot checks use that actual version. Never update
   old `passed: false` records to pretend the rule had always existed.
5. **Main admission:** `freeze()` reconstructs all pilot scopes and contains
   additional legacy rejection branches for truncation/provider/framing and
   episode errors when the policy differs from the present recovery version.
   A new constant added without updating those branches would move the failure
   here. Test the later gate explicitly, including terminal noncompletion.
6. **Numbered batches:** preserve ten fixed two-world scopes, all twenty intended
   worlds and exact completed-call reuse. A completed numbered-cell rerun must
   never resample or advance a different scope.
7. **Reporting/UI:** distinguish action compliance from admission eligibility.
   Do not label a study protocol-perfect because its evidence is admissible.
   Preserve raw error labels, exact counts, costs, unknowns and pending review.
8. **Delivery:** update plan/source markers, notebook metadata/bootstrap,
   builder/verifier, wheel, runbook, handoff and WBS together. Both notebook names
   should remain identical complete ordinary-cell workflows. Use a fresh source
   cache/environment and study destination when the source version changes.

For the new version, name the blocking checks by what they establish, such as
durable terminal evidence and runtime integrity. Keep the separate measured
`legal_action`/error counts. Avoid a `valid_protocol` gate that appears to mean
all actions were valid when the actual rule only qualifies an interface.

## 6. Immediate engineering improvements that need no scientific relaxation

### 6.1 Put the offending call in the exception

The current checkpoint already has correct, detailed diagnostics. Surface the
blocking subset directly when a pilot check fails, for example:

```text
Pilot 2 blocked by the current prefix/control admission rule.
pilot-01/prefix/agent-1/invocation-0:
wait_requires_null_message_and_submit (JSON/schema valid; illegal action).
All eleven pilot calls and their effects are committed; runtime/spending passed.
```

This is presentation, not a new pass. Include policy ID, failed check, phase,
call, raw-audit link and whether workers closed. `check_pilot()` currently raises
before returning a payload, so the notebook sees no result value even though
the complete failed gate was persisted. Read that existing receipt for display;
do not create another authoritative status record.

Retain the compact failure table and failure-first raw audit added previously.
The operator should not need to search a large history/manifest dump to locate
the one blocking prefix action. Offer full raw conversation links and explicit
inspection commands without restoring button/forms as the normal interaction.

### 6.2 Make reporting distinctions easier to read

- Add a concise run-level panel: scalar qualification passed, pilot 1 admitted,
  pilot 2 blocked under which rule, pilot 3 unknown, main 0/20, cleanup confirmed,
  provider release unknown.
- Label an empty main-cost plot explicitly: “No main worlds executed; pilot
  results are separate.” Keep twenty unknown worlds in the primary outcome plot.
- Keep denominators per context: qualification worlds versus paired scalar calls,
  prefix versus retain/clear, and pilot controls. Exclude forced hardware outputs
  from scientific JSON/action compliance.
- Preserve episode-level failure labels, but distinguish broad episode call
  lists from exact offending calls. For this run, four exact action violations
  are available; an episode-wide list does not identify which call violated.
- Show success and terminal reason beside effort. Pilot 2 retain's two-call
  failure must not be labelled more efficient successful recovery.

These changes can be implemented without changing the experimental treatment,
model, scoring or saved data.

### 6.3 Preserve the engineering that now works

Keep verified pip bootstrap, isolated headless processes, pinned dependencies,
source-only input, exact wheel/source checks, resident workers, two canonical
WAL/FULL stores, raw-before-effects, fresh-cache isolation, bounded attempts,
quiescent exports, persistent blocked status and failure cleanup.

Course-6 now supplies actual-host evidence for the clock and cleanup repairs.
Do not replace those mechanisms in response to an ordinary model action error.
Both workers closed with real acknowledgements after export, but provider release
and controller exit are unknown. A resume must load new replicas and satisfy
existing current-load evidence requirements; pretending the old workers remain
resident would create a genuine execution error.

The forecast should remain explicitly scoped. The reconstructed 165.45-minute
main-only estimate excludes pilot 3, future export growth and abnormal runtime
tails. Include remaining scheduled pilot/control work and measured checkpoint
overhead before presenting a whole-run forecast. Do not turn this estimate into
a completion promise or relax the timeout/export margins.

## 7. Prompt/interface improvement as a separate scientific option

The current system prompt already forbids message-plus-wait and states private,
phase-final submission. The model nevertheless repeatedly violates the rule.
The same misleading action shape appears in original and recovery contexts,
so this is not a JSON parser defect peculiar to retention.

A small, symmetric clarification is plausible if the goal is a more usable
collaboration interface. It should be a **separately identified prompt version**,
not slipped into a policy-only continuation:

1. State IDs 0 and 1 and the partner explicitly; each current shard contains
   twenty values, with zero-based record indices. Keep partner records private.
2. Show distinct message-only and silent-wait forms with generic, non-answer-
   bearing text. State that a message sent with `wait: true` is rejected and
   therefore cannot request information from the partner.
3. Clarify that each agent must privately submit its own answer to the **global**
   task; a partner's final status is not host confirmation of correctness.
   Communication must occur before that agent's irrevocable submission.
4. Clarify that a factual edit notice reports a changed **record**, not a partner
   submission or a certified maximum. Only the owner receives the new value;
   the current shard remains authoritative. Do not give the corrected maximum.
5. Consider specific bounded **nonsemantic** invalid-action feedback identifying
   the wait constraint, within the existing 32-token feedback limit. This changes
   later rendered requests and retained feedback, so version and disclose it.

Apply the same prompt/feedback implementation to both conditions. Never instruct
retain to discard history, certify partner prose, reveal truth or fill in missing
messages. Do not turn prose-number agreement into a host semantic validator:
pilot 2's legal message/submission inconsistency is a measured behavior.

Explicitly coaching “compute local maxima, exchange them, then submit their
maximum” would impose a collaboration strategy and might solve much of the task.
That is a more substantive scaffold, not a neutral formatting fix. Constrained
decoding or allowing message-plus-wait changes the generator/action space and
needs its own justification, runtime/bound checks and scientific version.

**Recommended sequencing:** for the smallest admission-only experiment, defer
prompt changes and measure the present error-prone system honestly. If the goal
requires meaningful compliant collaboration instead, choose the clarified prompt
cohort first, freeze it prospectively and accept that its outputs may still fail.
Do not collect half a main cohort and then change the prompt. Thinking/new models
remain separate options; course-6 supplies no evidence they repair these errors.

## 8. Fresh start versus preserving the 43-attempt study

### Preferred operator flow if a fresh rerun is selected

Build a complete matched source/wheel/notebook package, new policy/plan and new
study directory. Preserve course-6 as development evidence; import no old outcomes
or checkpoint by default. Retain automatic local checkpoints even if the operator
ignores links during Run All. Repeated cells must keep their study ID, deadline,
bound plan, spending and exact saved calls.

A fresh allocation must be explicit in the eventual adoption. The currently
approved independent study does not silently reset because a pilot failed.
Keep the same 500 hard ceiling, 28 contingency ceiling, twelve direct controls,
eight initial hardware calls, three fixed pilots and twenty main worlds. The
direct-only ordinary first-attempt ceiling remains 460; unused thinking scope
does not create extra reserve/worlds. No actual execution is authorized here.

### Optional policy-only continuation: not supported today

The existing explicit transition only accepts reviewed pre-experiment `8f5bcdb`
source without an envelope. Course-6 uses `b92cdbf`, has completed its envelope
and two pilots. Reusing the old `continue-checkpoint` command or overwriting the
policy/source metadata would be invalid. Same-source restoration can preserve
and inspect this study, but the current gate will fail again deterministically.

If continuation is later selected, implement a narrow reviewed amendment route:

1. Verify the exact ZIP/source inventories, both canonical DBs, study identity,
   43 completed attempts, zero contingency and absence of main/freeze data.
2. Restore into a fresh writable destination; preserve original source/manifest,
   plan, pilot-1 pass, pilot-2 failure, calls, requests, raw outputs, effects,
   costs, states and annotation history. Record an approved amendment separately.
3. Restrict a policy-only transition to reviewed admission/diagnostic/presentation
   differences. Reject prompt, feedback, model/runtime, seeds, world, semantic,
   decoding or bound changes. Reconstruct the new decision from unchanged data;
   never relabel the historical failure as an original pass.
4. Verify real old-process/session exit and latest/unknown-tail evidence. The ZIP's
   zero in-flight count alone cannot bound later spending. Preserve existing gaps
   and blocked worlds; unknown exposure remains blocking.
5. In a new session, record actual time facts, load both replicas, and run exactly
   the existing **two contingency-charged reload probes**. Reuse completed
   readiness/control/pilot calls when their required exact evidence matches;
   never resample pilot 2 to obtain a better action.
6. Execute fixed pilot 3 and measured main admission, then the unchanged twenty
   worlds in their numbered batches, subject to the new approved rule and genuine
   resource/evidence prerequisites.

No-extra-exposure continuation arithmetic:

| Component | Maximum physical attempts |
|---|---:|
| Already completed and preserved | 43 |
| New-load probe pair, charged to contingency | 2 |
| Remaining pilot | 20 |
| All twenty main worlds | 380 |
| Total with that reload pair | **445** |

The initial snapshot arithmetic is 457 remaining, but it does not authorize
additional worlds or spending unused turns from terminal pilots. With at most
28 total contingency attempts, the realized-prefix ceiling is 43 + 20 + 380 +
28 = **471**, before any separately reconciled exposure constraints. The pair
uses two of that reserve, leaving 26. No prior attempt disappears.

Do not build both a migration subsystem and fresh-only workflow without a
selected need. The current user preference favors fresh Run All; continuation
is optional and adds implementation/validation work.

## 9. Focused verification for a future repair

Reuse these saved traces and the existing lightweight checks; do not start a
large CPU campaign or run model qualification to test admission logic.

| Check | Required evidence |
|---|---|
| Exact course-6 prefix reply | JSON/schema valid; illegal wait/message remains invalid, consumes one turn, delivers nothing |
| Existing historical policies | Original strict and recovery-only rules still block the appropriate old evidence |
| Approved new policy | A distinct new decision passes the ordinary-error cases without changing raw data, states, costs or original decisions |
| Main admission integration | `check_pilot()` and `freeze()` use the same rule; no leftover baseline/event or legacy error check moves the stop downstream |
| Boundary cases | Original deadlock/horizon/missing submission, recovery error, and later control invalid output follow the chosen matrix, not an undocumented fallback |
| Genuine faults | Provider/cache/numerical defect, unconfirmed timeout, in-flight/spending gap, missing raw/effect, source/slot mismatch and inadequate time remain blocking |
| Full ordinary-cell flow | A tiny scripted complete twenty-world run with ordinary errors in different phases reaches every fixed scope, writes truthful reports and closes workers |
| Replay/restore | Repeating completed numbered cells costs zero; exact archive reconstruction preserves unknowns and source/attempt identity |
| Failed prerequisites | Export before closure, partial report, last-good archive, acknowledgement truth and persistent blocked status remain correct |
| Matched release | Both notebook names, all 33 ordinary cells, source selection, wheel, dependency pins, policy markers and fresh source/destination integrate coherently |

If a policy-only continuation is selected, additionally prove byte-for-byte
preservation of its 43-attempt scientific tables/manifest and exact first-use
accounting, old failed decisions, unknown-tail refusal, two-probe reserve charge
and refusal of frozen/main or unreviewed prompt/runtime transitions.

If prompt changes are separately selected, add native tokenizer/bound/privacy
checks and freeze the new source before new research. Actual compliance and
collaboration remain unverified until the operator later runs that cohort.

## 10. Avoid fixes that conceal the result

- Do not set `valid_protocol=True`, remove only the first gate or bypass source
  binding. Later main admission reconstructs evidence and the old plan is immutable.
- Do not flip `wait`, deliver the rejected text, fix JSON or replace submissions
  from prose/current truth. That changes information flow and all downstream calls.
- Do not rerun the pilot, add seeds or replace this world until it passes. Identical
  requests/seeds are not permission to resample a recorded outcome.
- Do not clamp 1023, certify message claims, invent missing submissions, or treat
  `[25,25]` as success because the agents agree.
- Do not expand turns/output limits: the observed violations ended at EOS in
  50–149 tokens, far below the cap. Larger limits do not address the illegal action.
- Do not pool repeated preparation/pilot worlds across course runs as independent
  observations, or substitute the two development pilots for the twenty main worlds.
- Do not increase sample size, use unused attempts as extra reserve, select a
  model/thinking fallback, or tune a pilot error threshold from this one example.

## 11. Delivery order if approved

First implement the selected scientific contract and shared Python admission
logic, then diagnostics/reporting and any separately selected prompt work. Run
the focused saved/scripted checks, build the complete fresh ordinary-cell package,
and verify source/wheel/notebook integration. Update the existing WBS/handoff
with implemented versus tested versus Kaggle-executed status and make meaningful
milestone commits. Do not stop at a new core helper or leave an old freeze check.

The recommended next package should retain all useful work from the present
runtime. Its purpose is a coherent prospective rule for measuring ordinary
team failures, clearer operator evidence and a complete end-to-end execution
path—not claiming that these observed failures have been repaired in the model.
