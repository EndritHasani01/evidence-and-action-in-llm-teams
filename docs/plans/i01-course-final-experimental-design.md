# I-01 course experiment: final design for approval

16 October 2026. **Design finalized for review; not adopted or implemented.**
This document selects one next experiment. It does not amend
[PROJECT_SPECIFICATION.md §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime),
which remains the sole scientific authority. All existing files, contracts and
Course-7 results remain unchanged. No implementation, inference, model loading
or GPU use occurred. Approval of a design is not authorization to execute it.

Read this decision document first, then the
[protocol and implementation acceptance annex](i01-course-final-design-protocol-and-acceptance.md).
Together they specify the selected design; the annex supplies exact presentation,
diagnostic fixtures, assignment rules and verification requirements.

## 1. Decision

Conduct **one new, bounded, natural-prefix retain/clear study with twenty main
worlds**, using the existing two-agent maximum task, model, action semantics
and exact scoring. Give both policies the same fixed assistance package:
clear action documentation, explicit global/private-finality instructions,
separated current/event/history presentation, short coordination guidance and
public-rule-specific rejection feedback.

Establish feasibility with four balanced pilot worlds before main. Preserve all
main worlds and ordinary failures. If the fixed candidate fails the declared
feasibility decision, end this campaign with a feasibility report. There is no
automatic prompt revision, model switch, supplied-prefix main experiment or
second attempt at the same screen.

The selected scientific question is:

> For this fixed assisted agent environment, what is the paired difference in
> exact team recovery and effort between retaining and clearing naturally
> generated visible history after the specified winning-record withdrawal?

The study evaluates the **total history-policy contrast**. It does not isolate
memory from information, pure anchoring, correction specificity, spontaneous
coordination, or the marginal effect of individual prompt ingredients. The
assistance is a declared behavioral condition, not a retrospective repair.

## 2. Resolution of the previous recommendations

The starting evidence is the [Course-7 independent audit](../validation/i01-course-7-independent-scientific-audit.md),
[quality proposal](../proposals/i01-course-7-experimental-quality-improvement.md),
[fifteen-paper review](../implementation-research/i01-course-7-targeted-scientific-literature-review.md),
[mechanism-oriented recommendations](../proposals/i01-course-7-literature-informed-recommendations.md)
and [latest practical investigation](../implementation-research/i01-course-practical-literature-investigation.md).

Course-7 completed twenty pairs with 2/20 successes in each policy, but only
3/20 correct originals. Sixty of 206 team actions were illegal despite valid
JSON. Current-source, notice and final-submission failures also occurred.
The audit found no scorer/delivery/isolation defect explaining these outcomes.
These observations justify one common environment intervention and a real
feasibility decision; they do not justify repairing old replies or assuming
that a larger model will solve the problem. [Audit §§5–6, 9](../validation/i01-course-7-independent-scientific-audit.md#5-independently-reproduced-main-results).

| Conflict or assumption | Final decision and reason |
|---|---|
| Natural policy study versus four-cell mechanism study | Choose the natural two-policy study. It answers the existing practical question with substantially less new machinery. Accept the bundled treatment and narrow the claim |
| Clarification first, strategy only after another failure | Include one short strategy now. Discovering the maximum-exchange algorithm is not the course's research target. Agents still calculate, communicate, choose evidence and commit |
| Guarantee correct original histories | Do not guarantee or screen individual main prefixes. Use natural one-shot originals; pilot feasibility selects a system, not favorable main worlds |
| Force communication before every submission | Do not enforce it. Valid retained information may already suffice; compulsory fresh exchange would suppress a possible retention benefit |
| Eight static probes and three pilots | Use four focused probes and four pilots. Complete coverage of the four owner/first-speaker combinations is more valuable than a larger hand-crafted probe battery |
| Twelve scalar qualification calls and 28 reserve attempts | Use eight scalar calls and 20 reserve attempts. Qualification still covers both inputs on both devices; this funds the extra complete pilot within 500 |
| More controls always improve validity | Keep scalar controls and source/action diagnostics. No sham or selective-memory main arm because no correction-specific or content-mechanism claim is selected |
| Obtain a prompt-improvement estimate | Not a campaign objective. Course-7 is a historical reference; different worlds/runtime occasions prevent a causal prompt-improvement claim |
| A null or unsuccessful next campaign is inadequate | Reject. A bounded policy null or a failed feasibility screen is a legitimate course outcome, with appropriate uncertainty and trace evidence |

The literature supports testing this direction, not a promised gain. SWE-agent's
interface ablations demonstrate sensitivity to the environment with a fixed
model (Table 3, PDF p. 6). τ²-bench's workflow intervention helps some conditions
and harms its oracle-plan conditions (Figure 4, p. 7). FlowBench distinguishes
actions given correct previous histories from live accumulated interaction
(§4.3, pp. 6–7). These findings support a compact package and live pilots rather
than assuming a static probe certifies readiness.
[SWE-agent](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html),
[τ²-bench](https://proceedings.mlr.press/v306/barres26a.html),
[FlowBench](https://aclanthology.org/2024.findings-emnlp.638/).
The reviews above document full-text versions, methods and transfer limitations.

This is a course-scale replication/extension under a more explicit environment.
No new memory architecture, first-ever mechanism, multi-agent superiority or
publication-level novelty claim is required.

## 3. Fixed design at a glance

| Item | Selected value |
|---|---|
| Proposed regime | `i01-course-assisted-v2` |
| Proposed execution policy | `i01-assisted-feasibility-2026-10-16` |
| Agent environment | One assistance package, exact text/rendering in annex; no worked numerical demonstration |
| Main comparison | Literal retain versus literal clear; all other permitted inputs and settings matched |
| Mathematical task | Two private shards, twenty integers each; both agents submit the global maximum |
| Event | One unique original maximum replaced below the remaining maximum; answer necessarily changes |
| Qualification worlds | Four; original and revised full-information scalar control each |
| Diagnostic calls | Four single-call fixtures derived from qualification worlds; not main data |
| Pilot worlds | Four, one in each changed-owner/first-speaker cell |
| Main worlds | Twenty, five per cell; one natural prefix per world |
| Per phase | At most three invocations per agent, six total; original strict finality/waiting/delivery |
| Model | Pinned Qwen3.5-9B, same quantization, runtime and direct settings as Course-7 |
| Replication | One generation per scheduled logical call; no repeated seeds to select a better outcome |
| Main endpoint | Both exact revised submissions within bounds |
| Principal effort | Paired post-revision ready-model seconds, including unsuccessful continuations |
| Analysis unit | World; siblings and their shared prefix remain dependent |
| First-attempt ceiling | 480 across all stages |
| Contingency ceiling | 20 additional physical attempts; total hard ceiling 500 |
| Primary scientific endpoint count | One policy-success contrast; effort and process are secondary |

The regime and policy identifiers distinguish a necessary changed condition;
they are not a new registry or provenance system. Current source/configuration
binding and existing study IDs remain the recording mechanism.

## 4. Task, information and agent behavior

### 4.1 Population and generation

Use the current integer task and existing seed derivation. Each shard contains
twenty independent draws from the uniform integers −1000 through 1000, conditional
on mathematical eligibility and the scheduled owner of the original maximum.
There must be one unique original maximum; the maximum of the other 39 values
must exceed −1000. Replace its record uniformly in `[-1000, M2-1]`.

The four equally weighted strata are `(changed owner, first speaker)` in
`{0,1} × {0,1}`. Owner conditioning is explicitly permitted: reject draws whose
winning record has the wrong scheduled owner, and record that reason separately
from mathematical ineligibility. This resolves the audit's generator-wording
tension without rewriting previous inputs. Never reject using model behavior.
The 1,000-proposal limit per world remains; exhaustion stops generation without
inventing a substitute seed or quietly altering the population.

Save all 28 worlds before inference: four qualification, four pilot and twenty
main. Use proposed master seed `2026101601`. The annex fixes their ordering,
device/treatment assignment and invocation seed rules. Actual arrays are created
only in a later authorized preparation step, not in this documentation task.

Check for exact original/revised input-pair overlap against every exposed
Course-1…7 world and any saved development fixture. A collision is a technical
data-separation failure: stop before inference and seek a documented design
revision; do not keep trying seeds until attractive worlds appear. Main arrays,
answers and histories must not inform prompt editing or example selection.

### 4.2 Permitted information and literal retention

The current own shard is authoritative. The common notice identifies the sole
changed owner and record; only that owner sees the replacement value. The new
presentation explicitly states that this is an environment event, not a partner
message or private submission. It does not reveal which value used to win, the
new global answer, future events or the mathematical eligibility rule.

After every natural prefix, both continuations start from independent copies:

- **Retain:** keep the exact own previously visible legal actions/submissions,
  received messages and public-rule feedback, including wrong content.
- **Clear:** erase that entire previous visible history. Start with the same
  current own shard, notice, instructions and fresh phase state as retain.

Both reset turns, waiting and current submissions. Private reasoning and hidden
KV/recurrent state never cross calls. Rejected raw outputs remain auditor data,
never delivered or inserted as successful historical actions. New feedback is
retained/cleared by the same literal rule as other visible records.

Earlier/current phase wrappers may identify when a record was visible; message
bytes and action values stay literal. No source certification, stale-only
deletion, semantic summary or host-computed maximum is introduced. The annex
defines the minimal historical boundary needed for these wrappers.

### 4.3 Protocol remains strict

Keep exactly the existing fields `message`, `submit`, `wait`, their strict types,
duplicate-key rejection and whole-output parsing. Message-only, submit-only,
send-and-submit and wait-only remain legal. Waiting excludes both other fields;
an empty non-wait action is invalid. Invalid/truncated/framing replies deliver
nothing and consume the scheduled turn. Feedback adds no turn or retry.

Submission is private unless explicitly messaged and final within a phase.
Send-and-submit delivers the message before finishing the sender. Later messages
do not reopen the submission. Waiting wakes only on a delivered message.
The existing sequential eligible-agent scheduler and terminal rules remain;
do not import the older four-agent synchronous-round protocol.

Stop a phase on both submissions or inability of unfinished agents to progress,
including waiting deadlock/horizon exhaustion, regardless of correctness. The
single factual revision reopens both agents once. All known terminal mistakes
score zero; unresolved execution remains unknown.

### 4.4 Capability and runtime are held fixed

Use `Qwen/Qwen3.5-9B` revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, text-only NF4 double quantization,
FP16 computation and the reviewed T4 SDPA runtime on two distinct T4 devices.
Direct/nonthinking generation: temperature 0.7, top-p 0.8, top-k 20, repetition
penalty 1, presence penalty 0. Input cap 8,192 native tokens, output cap 512,
fresh call-owned state. Scalar controls retain their current scalar prompt.

Keep load/direct deadlines of 600/180 seconds, five-second bounded termination,
120-second export reserve, 300-second periodic checkpoints and ≥1.5 GiB measured
free-headroom requirement. The selected presentation must fit the native input
bound losslessly; never truncate retained history or raise a limit silently.
No thinking fallback, extra model, calculator, constrained decoder or numerical
backend redesign is selected. An established runtime defect still blocks
execution; poor answers alone do not establish such a defect.

## 5. Feasibility decision and execution order

Lock the complete candidate, source/runtime, data, schedule, limits, scoring and
this admission rule before the first model call. There is no within-campaign
prompt search. Preserve the existing complete Run All capability with finite,
idempotent stage cells, complete conversation inspection and checkpoint export.
A later operator request to execute the whole fixed campaign may authorize its
automatic stages; this design document authorizes none.

### 5.1 Preparation

After source/privacy/lifecycle checks, load the two workers once. Perform six
short A/B/A state checks, eight scalar qualification calls (original/revised
for four worlds), and two full-envelope probes. The eight scalar actions must
all be legally recorded scalar outputs; their accuracy is diagnostic at this
point. A malformed qualification output fails this prespecified format screen,
not the implementation. Do not resample it.

After current-load health and envelopes pass, execute the four diagnostic calls
in the annex. All need settled durable evidence; ordinary probe errors are
reported, not an extra numerical gate. These single-call supplied-view tests
do not certify live coordination. No diagnostic result may rewrite the fixed
candidate, and no model state from a probe carries into another call.
Create and verify a quiescent portable checkpoint after preparation/diagnostics,
before pilots. Its measured export duration supplies the first checkpoint-cost
observation for the resource forecast.

### 5.2 Four complete pilots, then one objective decision

Execute all four pilots once, each with a natural prefix, both siblings, original
and revised scalar controls. Keep all ordinary mistakes and complete all four
unless a genuine integrity/resource/termination problem stops execution.

**Main is scientifically eligible exactly when:**

1. All four pilot scopes have settled terminal evidence for all scheduled
   phases/controls, committed effects, reconciled spending and valid exports.
2. At least **3/4 original teams** are exactly correct.
3. At least **7/8 pilot scalar controls** are exactly correct.
4. Source/privacy/state/resource checks remain valid and the remaining fixed
   scope fits the measured attempt/time budget.

Recorded invalid actions and terminal noncompletion enter these denominators
as failures. There is no separate all-pilot-actions-legal requirement and no
gate on recovery success, retention-effect direction, agreement or message style.
There is no qualitative discretionary failure-mode veto after the numerical
rule passes. Trace review supplies interpretation, not outcome-based tuning.

The 3/4 and 7/8 thresholds are explicit course-usefulness judgments, not paper-
derived reliability guarantees. Four pilots are small. They screen out another
campaign dominated by unusable originals while preserving a feasible study.
They do not guarantee that main recovery will avoid a floor or ceiling.
Balance gives the original-team threshold a concrete rationale: a first speaker
that always commits its local maximum before learning anything from its partner
can at best exploit the two owner-equals-first cells. Requiring three successes
therefore requires success beyond that particular shortcut, without claiming
that three outcomes prove a reliable reasoning process.

If the rule fails, write a complete feasibility report and stop scientific
admission. Do not relax thresholds, replace pilots, retry known answers, change
models or draw another pilot cohort in this campaign. Main stays unexecuted,
not failed. A later redesigned campaign would require another explicit decision.

### 5.3 Main

If eligible and separately authorized, execute all twenty saved main worlds in
ten fixed two-world batches. Each world gets one natural prefix, both recovery
siblings and one revised scalar control. Keep main originals regardless of
their correctness. Outcomes never determine which world/batch runs next.

Export after each pilot, each main batch and any settled error. Completed stage
reruns reuse exact saved data and spend zero additional calls. Genuine runtime,
privacy, source, storage, unresolved spending or resource faults stop admission;
ordinary main model mistakes do not. Keep weights resident through reporting
and inspection, then close workers after the final settled export.

## 6. Resource contract selected for later adoption

| First-attempt stage | Maximum |
|---|---:|
| Hardware/state: six checks plus two envelopes | 8 |
| Direct scalar qualification | 8 |
| Diagnostic fixtures | 4 |
| Four pilots, at most `4 × (6+6+6+2)` | 80 |
| Twenty main worlds, at most `20 × (6+6+6+1)` | 380 |
| **Ordinary first attempts** | **480** |
| Contingency: eligible interruptions/requalification | **20** |
| **Hard whole-campaign physical-attempt ceiling** | **500** |

This replaces the latest proposal's 496-attempt option. More complete live
coverage takes priority over eight static probes. All diagnostics, failures,
warmups and eligible retries count. Downloads/model loading do not count as
inference attempts but consume real time. Early stopping within a phase saves
attempts without adding worlds, candidates, probes or stage capacity.

Reuse the single admission owner and two canonical stores. The stage ceilings
above and total/reserve must both hold. Do not use unused main turns to enlarge
development or move ordinary calls into reserve.

One identical infrastructure retry is allowed only without a durable outcome,
with exact request/settings/seed equality and confirmed prior termination.
Known wrong/invalid/truncated outputs and recorded terminal timeouts never
retry. Unresolved loss is not free spending. On a new load of the unchanged
frozen runtime, require six current-load state checks and two envelopes,
charged to reserve; accepted scalar/probe/pilot outcomes remain saved and are
not regenerated. Twenty reserve attempts can fund at most two such eight-call
reload cycles, leaving at most four for other eligible interruptions.

Use the actual session's remaining allowance and one fixed deadline. A 700-minute
window remains only an operator-informed conservative planning estimate, not
a verified provider guarantee. Rerunning cells cannot extend a session deadline.
Forecast from new measured call/export times and remaining worst-case call
slots; never extrapolate Course-7's fast wrong finalizations as a completion
guarantee. If scope cannot fit, stop truthfully; do not shrink the main cohort
after observing outcomes or waive current-load checks to fit the budget.
The annex fixes the conservative forecast calculation and its admission checks.

A fresh independent 500-attempt campaign must be explicitly authorized later.
It does not inherit, erase, pool or reset Course-7 or prior campaign spending.
Restoring this new campaign never resets its own charges or unknown exposure.

## 7. Estimands, uncertainty and reporting

For each main world `w`, let `R_w` and `C_w` be exact both-agent revised success
under retain and clear. Each is 0 or 1 for a known terminal episode and unknown
otherwise. The primary finite-cohort estimate is:

```text
D_w = C_w - R_w
delta = sum(D_w over the 20 intended worlds) / 20
```

Positive delta favors clear on exact success. Show both arm rates and all four
paired counts: both, retain-only, clear-only, neither. Treat the owner/first
strata equally, as their sizes are equal. The target concerns these world and
invocation-seed draws under this one fixed environment, not all models/tasks.

Use the existing **exploratory stratified world bootstrap**: 10,000 draws,
five worlds with replacement per stratum, preserving each sibling pair; proposed
bootstrap seed `2026101602`. Use sorted draw indices 250 and 9750, zero-based,
without percentile interpolation. The annex fixes ordering and edge cases.
This is a descriptive uncertainty display with small-sample limitations, not
a calibrated equivalence or noninferiority test. Always report discordant counts
and warn about empty/constant contrast strata. A zero-width interval cannot
establish absence of a population effect. No primary p-value or significance
threshold is selected; no post hoc choice among interval methods.

With missing episodes, the primary point estimate/interval is unavailable.
Keep all twenty intended worlds and report sharp outcome-completion bounds:
unknown success is allowed to be either 0 or 1. Complete-case means, if shown,
must have a separate label and denominator; they never replace the primary
population. A known terminal noncompletion is zero, not missing.

The principal effort contrast is mean `clear ready_seconds − retain
ready_seconds` across the same twenty worlds, with the same paired bootstrap
when effort is fully known. Include unsuccessful continuations' full effort.
Also report calls, tokens, legal messages and observed wall/load/setup cost
separately. No accuracy/cost composite or success-only efficiency claim.

Original correctness and correct-prefix recovery are secondary context. Show
their actual counts and denominator, without a subgroup confidence interval or
an extra hypothesis test. Controls are capability diagnostics with different
views/prompts; subtracting their accuracy from team accuracy does not identify
a causal communication-failure rate. Agreement, old-answer avoidance, legal
JSON and fluent reasoning are not substitutes for primary exact success.

Report protocol/action reasons, terminal reasons, locally refutable submissions
and obsolete-answer repetition from exact records. Use a small trace-linked
casebook for notice confusion and reasoning/action contradiction; do not claim
an internal mechanism or a causal failure percentage from those labels.
The annex supplies definitions and deterministic case selection.

Twenty worlds have limited precision. A larger observed difference may be
descriptively meaningful; a small/null difference remains inconclusive about
modest population effects. This design is intentionally sufficient for a
bounded course finding, not a powered claim of broad policy superiority.

## 8. Interpretation and completion criteria

| Result | Required interpretation / endpoint of this campaign |
|---|---|
| Pilot usefulness fails | Feasibility study completed; main unexecuted; no automatic rescue campaign |
| Main succeeds well in both policies with a small/null contrast | Bounded practical null under assistance; do not add difficulty to seek a winner |
| Main remains poor in both policies | The selected system still fails after withdrawal; explain visible failures and preserve the full contrast |
| One policy performs better | Evidence for this total history-policy contrast, with small-sample and information-availability limits |
| Retain is faster but often wrong | Effort difference, not demonstrated useful-work efficiency |
| Runtime/resource interruption | Partial study with truthful coverage/unknowns; completed calls retained exactly |

The course deliverable is complete when its admitted scope has a reproducible
report, full trace/coverage/accounting evidence and portable verified export,
or when a prespecified failure gate yields the corresponding complete
feasibility/partial report. Passing a gate alone is not completion or authority
to spend on another scope.

Course-7 remains a separate historical result. Do not pool its data with new
outcomes, regrade rejected messages, overwrite artifacts or describe differences
between campaigns as an identified prompt effect. Preserve negative results.

## 9. Approval boundary

The decisions requiring later adoption are exactly: the new assisted condition
and rendering/feedback, four qualification worlds, four diagnostics, four pilots,
the objective usefulness gate, stage/reserve reallocations, fresh inputs/seeds,
decoupled execution assignment and the reporting choices above. All unchanged
§12 invariants remain required. No historical rule is retroactively superseded.

If approved, these decisions provide the basis for a scoped amendment and the
implementation tasks in the annex. That future work must update the living
engineering handoff and scientific authority explicitly. They are deliberately
untouched now because this task authorizes **new Markdown only**.
Implementation and actual GPU execution remain subsequent authorized stages.
