# I-01 final design: protocol and implementation acceptance annex

16 October 2026. **Implementation-ready design text; not implemented or adopted.**
Read with the [final experimental design](i01-course-final-experimental-design.md).
The current [scientific specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
remains authoritative until an explicit later adoption. This annex changes no
existing prompt, code, configuration, contract, data or result. Literal prompt
text and algorithms below specify a future implementation; they were not used
for inference or inserted into executable files.

## 1. Common agent instructions selected for approval

Use the following system text identically in the original phase and both
continuations. Preserve these words when implementing the approved version;
formatting/newline changes before release must be recorded as presentation
changes, not tuned against model answers.

```text
You are one of two agents finding the global maximum across your current
private integer shards. Both agents must separately submit that same GLOBAL
maximum. Submitting only your own local maximum is insufficient when the
other shard contains a larger value.

Your CURRENT AUTHORITATIVE PRIVATE SHARD is your source for current local
values. The other agent's shard is private. You can exchange ordinary text
messages. A message is a claim, not a certified source or a private submission.
The partner-finished flag reveals only whether that agent has finished.

A useful strategy is to establish the relevant maximum of each shard, compare
them, and send your partner any information needed before you finish. Choose
your messages and timing. Reuse earlier reports when justified; obtain new
information when needed. You do not have to repeat an exchange merely because
a new phase starts. Check what a source change invalidates and what remains
useful. An earlier final answer is not automatically a current answer.

An ENVIRONMENT SOURCE NOTICE is not a partner message, a partner maximum or
a partner submission. Its record index identifies a location, not an answer.
At a source-change boundary only the named record changes. The replacement
value is supplied only to that record's owner. Earlier-phase history records
what was visible then; current values come from your current shard.

Return exactly one JSON object with exactly these keys:
message: a string containing non-whitespace text or null
submit: an integer or null
wait: true or false

Legal choices are message only, submit only, message and submit together, or
wait alone. Waiting requires BOTH message and submit to be null. With wait
false, at least one of message or submit must be non-null.
Message-only example: {"message":"example message","submit":null,"wait":false}
Wait-only example: {"message":null,"submit":null,"wait":true}
These are action-form examples, not messages to copy for the task.

Your submission is private unless you explicitly message it. Submission is
FINAL for this phase: you cannot adjust it after another message arrives.
Sending and submitting together delivers your message and then finishes you.
Only an environment source change starts a new phase and reopens both agents.

Each agent has at most three calls per phase. Unused calls cannot be transferred.
Waiting wakes only on a delivered message. If both agents wait, neither can
send a waking message. Invalid replies use a call and deliver nothing.
There is no correctness feedback. Put no text outside the JSON object.
```

This intentionally supplies a coordination strategy. It does not require a
specific message template, acknowledgment, fresh peer report before every
submission, full-array broadcast, fixed call sequence or new round. Do not add
an answer-checking guard or reinterpret these instructions as enforced stages.
The public single-record-change rule is now stated explicitly in both policies;
the unique-winning-record and below-remaining-maximum eligibility rules remain
hidden. No numerical worked task demonstration is selected.

The scalar-control system text remains exactly the current text in
[core.py](../../recovery/i01/core.py):

```text
Find the maximum of the complete integer input below.
Return exactly {"message":null,"submit":INTEGER,"wait":false}.
No communication. A submission is final. No text outside the JSON.
```

Its user content remains `Complete input: ` followed by the complete flattened
integer list in original shard order. `INTEGER` is the existing scalar-output
placeholder, not a literal JSON value. Controls are one call, with no feedback
loop, collaborative history or correctness disclosure.

## 2. Team rendering and visible-history boundary

Render one system and one user message, using the existing native chat template
and direct/nonthinking adapter. No hidden treatment name, world ID, group, GPU
identity, seed, truth, score or eligibility field enters either message.

The user message has the following fixed order. Braces here denote substitution
sites, not extra model-visible JSON fields.

```text
You are agent {agent}. Your partner is agent {partner}.
This phase: {initial | reopened after an environment source change}.
Your invocation: {1-based own call}/3.
Partner finished: {true | false}. This is status only; no value is disclosed.

VISIBLE HISTORY: EARLIER PHASE
{earlier visible entries, or "(no visible entries)"}

VISIBLE HISTORY: THIS PHASE
{current visible entries, or "(no visible entries)"}

ENVIRONMENT SOURCE NOTICE
{notice block below, or "No source-change notice in this phase."}

CURRENT AUTHORITATIVE PRIVATE SHARD
record 0: {current value at index 0}
...
record 19: {current value at index 19}

Choose one legal action for the current phase. Return only the JSON object.
```

Current evidence is placed after historical prose deliberately, as one fixed
part of the assistance package. This is not a claim that ordering is causally
responsible for an improvement. Preserve the original record order: no sorting,
highlighting, host maximum, second-largest marker or omitted negative values.

The notice block is:

```text
Environment event: the following record changed before this phase began.
Changed owner (agent identity): {owner}
Changed record (index only): {record}
Replacement value for your record: {new value}
```

Omit the entire replacement-value line for a nonowner. Never print the before
value or the maximum-withdrawal eligibility rule. The notice is shown on every
recovery call, with the same bytes in retain and clear for the same agent.
The main system instruction is the same in both policies.

Entry rendering uses explicit boundaries and the existing literal contents:

```text
BEGIN VISIBLE ENTRY
Your action:
message={literal message text, or null}
submit={literal integer, or null}; wait={true or false}
END VISIBLE ENTRY
```

```text
BEGIN VISIBLE ENTRY
From agent {sender}:
{literal delivered message text}
END VISIBLE ENTRY
```

```text
BEGIN VISIBLE ENTRY
Environment feedback:
{literal previously delivered feedback text}
END VISIBLE ENTRY
```

Do not paraphrase, trim, correct, double-escape or deduplicate entry text.
Wrappers do not certify its content. Preserve chronological order within each
block. These are presentation boundaries, not a security guarantee against
prose imitating a header.

Use one minimal boundary in each episode state: `earlier_history_lengths`, a
two-integer list. It is `[0,0]` for an initial or clear start; for retain it is
the two prefix-history lengths at sibling initialization. New visible records
append after that boundary. It is initialized atomically with the sibling and
never recomputed from semantic text. This small metadata addition is justified
by the observed stale invocation/phase confusion. Do not add per-claim timestamps,
certification, dependency edges or another provenance store. Raw history records
and original prefix snapshots remain unchanged.

Native input limits must hold for the worst permitted literal history and
output reserve. Verify the exact renderer/tokenizer bound before release.
If it does not fit 8,192 input tokens, the release fails; do not truncate,
summarize, silently remove entries or change the cap during execution.

## 3. Rejection feedback and strict effects

The validator continues to decide whether an action exists. A reason-specific
feedback message is only a public explanation of rejection. Preserve the raw
reply and the historical `malformed_action` field; use derived reasons for
display. Do not relax parsing, accept fenced JSON or coerce types.

Select the first applicable row in this priority order:

| Outcome/reason | Exact visible feedback for a later permitted turn |
|---|---|
| Confirmed terminal provider timeout/failure with no action | `Call failed; no action was delivered.` |
| Truncated model reply | `Invalid: output was truncated. Nothing was delivered.` |
| Framing, JSON, duplicate-key, field-set or field-type error | `Invalid: output one JSON object with the required fields and types. Nothing was delivered.` |
| `wait=true` with either other field non-null | `Invalid: wait requires null message and null submit. Nothing was delivered.` |
| Empty non-wait action | `Invalid: choose message, submit, both, or wait. Nothing was delivered.` |

Unknown termination is an admission block, not an opportunity to supply feedback
and keep calling. Other unsafe backend/source/privacy faults also stop admission.
An integer answer below a current local value, disagreement, outdated answer or
implausible message is **not** an action-validation error and produces no
correctness-dependent feedback.

All feedback strings must pass the existing ≤32-native-token bound before
release. Do not shorten them dynamically on a live turn. No feedback is shown
unless another ordinary eligible turn already exists; no turn is added to
deliver it. Invalid output delivers neither its message nor its submission.

## 4. Data, seeds, assignment and execution

### 4.1 Saved world list

Use the existing `seed_for` function and generator mathematics. Set master seed
`2026101601`. Define stratum `s = 2*owner + first`, ordered 0,1,2,3.

| Group | IDs and placement | Device / sibling order |
|---|---|---|
| Qualification | `qualification-00`…`03`, index equals s | Device `s % 2`; no policy siblings |
| Pilot | `pilot-00`…`03`, index equals s | `(device, first policy)` for s=0…3: `(0,retain)`, `(1,retain)`, `(0,clear)`, `(1,clear)` |
| Main | `main-00`…`19`; index `i=4*k+s`, `k=0…4` | Assignment below; five worlds per stratum |

For each world, generate proposals from `Random(seed_for(master, world_id,
"world"))`. Reject nonunique maxima, remaining maxima at the floor and wrong
scheduled owners, with separate counters, at most 1,000 proposals total. Use the
existing uniform replacement draw and save every actual input, edit and counter.
First speaker is the same in original and recovery phases.

For each main stratum, create a list with all four `(device, first policy)`
combinations once. Add one extra combination according to s:

| s | Extra combination |
|---|---|
| 0 | `(0,retain)` |
| 1 | `(0,clear)` |
| 2 | `(1,retain)` |
| 3 | `(1,clear)` |

Shuffle that five-element list once with
`Random(seed_for(master, "assignment", owner, first))`; assign element k to
main index `4*k+s`. Save the resulting assignment before inference. This yields
exactly ten worlds per device, ten per first policy, and five of each joint
device/order combination. Every stratum includes both orders on both devices;
its necessary 2/3 imbalances are not hidden. No outcome informs assignment.

Use the existing invocation seeds:

```text
seed_for(master, world_id, "prefix", agent, zero_based_invocation)
seed_for(master, world_id, "recovery", agent, zero_based_invocation)
seed_for(master, world_id, "control", "original" | "revised")
```

Both policies share the recovery seed schedule, never a continuation response.
Adding a treatment name to that schedule would change the selected coupling.
Saved replies, including rejected/failed replies, are reused only for exact
resume with the prescribed request/settings/view checks.

### 4.2 Within-world and batch order

An ordinary pilot/main world executes original prefix, first assigned recovery,
second recovery, then scalar control(s), original before revised when both
exist. Controls are invisible to the peers and use fresh model state. Both
siblings stay on that world's assigned logical device. Source revision and
history transformation occur before the first continuation call in each sibling.

Run pilots in index order. Run main in ten batches `(00,01)`, `(02,03)`, …,
`(18,19)`. Different devices may run their assigned worlds concurrently; if
both worlds share a device, serialize them by index. Do not add a new parallel
orchestration service. Calls inside one episode remain sequential, and completed
messages become visible only through their branch-local committed effects.

### 4.3 Conservative resource forecast

Reuse the existing forecast structure, with new counts and diagnostics included.
Let `M` be the maximum known ready-model seconds among completed ordinary scalar,
diagnostic, pilot and main calls in this campaign; exclude hardware/state and
forced-envelope calls. Let `c = 1.25*M + 5` seconds. Let `N` be the remaining
worst-case ordinary pilot/main call slots from actual saved states, `P_m` the
number of unfinished main worlds and `P_p` the number of unfinished pilots.
Let `e` be the maximum measured successful checkpoint/export duration in the
current session. Define:

```text
T = N*c
exports = P_m + ceil(P_m/2) + 2*P_p + 4 + ceil(T/300)
forecast_seconds = T + exports*e + 120
```

Use this deliberately serial forecast even when devices can overlap work.
Require known `M` and `e`, `c <= 180`, enough remaining ordinary stage/total
attempt allowance for N, and remaining session time at least `forecast_seconds`
before admitting pilots/main or a further batch. Refresh from actual settled
records after each pilot/batch. Never count unknown time as zero or skip an
unexecuted ordinary scope in N. Inspection/setup/load time consumes the real
deadline even though it is not predicted by T. Reload eligibility also needs
its eight reserve slots and an adequate separate remaining-time check.

This retains the existing observed-maximum-plus-margin heuristic; it is not
a worst-case latency guarantee and does not budget unbounded abnormal tails.
Per-call deadline/cleanup/export guards remain in force. Before every dispatch,
retain the existing requirement for call deadline, bounded cleanup and export
margin to fit the actual remaining session time. A resource block preserves
partial data and unknown main slots; it does not authorize a changed sample.

## 5. Four diagnostic fixtures

These are **single-call diagnostic requests**, not natural original episodes,
training data, a controlled-history main arm or a treatment-effect estimate.
They reuse qualification inputs, which are already development-only. Scripted
history records have no fabricated model-call/attempt rows. Their provenance as
fixtures is recorded with the request in the existing stores and visible report.

Use the common team system text and renderer. The user message is unchanged
except for the two explicit diagnostic directives below, appended after the
normal closing line. Fixtures without a directive use the ordinary task alone.
No expected answer or diagnostic score returns to a peer.

For clarity, `L_a` below is the exact original local maximum of agent a, and
`L'_a` its revised local maximum. These symbols are construction/scoring notation,
never prompt fields. Histories contain only the resulting ordinary message text
and legal action fields specified below.

| Diagnostic | Input and reachable view | Directive / exact pass predicate |
|---|---|---|
| D00: message-only action | `qualification-00`, agent 0, original shard, first call, empty history, partner unfinished | Append `Interface check: send only the message ready. Do not submit or wait.` Pass: legal action, `message.strip()=="ready"`, `submit=null`, `wait=false` |
| D01: aggregate before finality | `qualification-01`, agent 1, original phase, second own call; scripted previous exchange below; partner finished | No directive. Pass: legal action, submission equals original global maximum, `wait=false`; message may be null or any legal text |
| D02: current source with usable old peer report | `qualification-03`, changed owner/first speaker agent 1, reopened first call; correct scripted original history below; partner unfinished after reset | No directive. Pass: legal action, submission equals revised global maximum, `wait=false`; message may be null or any legal text |
| D03: notice is not a local value | `qualification-02`, unchanged first speaker agent 0, reopened first call, empty history, partner unfinished; nonowner notice has no replacement value | Append `Local-source check: send only your current shard's maximum as decimal message text. Do not submit or wait.` Pass: legal action, `message.strip()==str(L'_0)`, `submit=null`, `wait=false` |

D01's supplied original trajectory is:

1. Agent 1 messages `My local maximum is {L_1}.`, with null submission and
   `wait=false`.
2. Agent 0 messages `My local maximum is {L_0}.`, submits `max(L_0,L_1)` and
   uses `wait=false`.
3. The single diagnostic call asks agent 1 for its next action. Its own
   invocation is 2/3; partner-finished is true; both earlier actions visible
   to it belong in **this phase**. The larger maximum belongs to agent 0 by
   qualification-world construction. The private partner submission is not
   separately exposed.

D02's scripted original trajectory is:

1. Agent 1 messages `My local maximum is {L_1}.`, without submission/wait.
2. Agent 0 messages `My local maximum is {L_0}.`, submits the original global
   maximum and does not wait.
3. Agent 1 submits the original global maximum, without message/wait.
4. Apply the saved revision and reopen both agents. Agent 1 sees its current
   revised shard, owner-only notice and its literal earlier-phase history:
   own first message, received agent-0 report, own final submission. Its call
   count is reset to 1/3 and partner-finished is false. The unchanged peer's
   historical report remains available as an uncertified claim.

These scripts are legal within the original per-agent limit. The fixture
constructor uses permitted original private values only; no revised remote
shard or gold certificate enters the request. Diagnostic scoring can use the
exact evaluator privately. D02 supplies a valid useful history, unlike natural
main. D00/D03 explicitly instruct a form/query unlike ordinary collaboration.
Thus a pass measures only that supplied-view behavior, not autonomous strategy
discovery or reliable memory recovery.

Diagnostic call IDs are `qualification-XX/diagnostic-D00` etc., with episode IDs
the same as their call IDs and seeds `seed_for(master, world_id, "diagnostic",
"D00")` etc. D01/D02 do not infer their seed from their scripted prior actions.
All four are first-attempt `diagnostic` charges in the ordinary ledger, with
usual eligible infrastructure retry rules. Use world devices, so two calls
occur per device. Execute D00, D01, D02, D03 once each.

Report each predicate, raw action, legality reason and exact expected scalar
privately in the diagnostic report. Whitespace trimming is only an equality
test on message text; it never changes a delivered action. Invalid or confirmed
terminal failure means diagnostic failure; unresolved execution is unknown.
No aggregate diagnostic threshold gates main. The main admission rule uses
complete live pilots and scalar controls as fixed in the decision document.

## 6. Exact reporting conventions

### 6.1 Success, coverage and bootstrap

Primary success is exactly `submissions == [revised_truth, revised_truth]` for
a terminal episode; otherwise a known terminal failure is zero. There is no
credit for only one correct agent, a correct message or wrong consensus.
Nonterminal/unexecuted/unresolved evidence is unknown, never carried forward.

The primary table includes all twenty intended worlds in index order. Define
`D=C-R`. The point estimate requires both outcomes in every world. For completion
bounds, substitute zero/one independently for each unknown binary outcome to
minimize/maximize each world's difference, sum and divide by twenty. Missing
prefix/control evidence is reported separately, even when both recoveries exist.
Do not call the complete study finished unless all scheduled required records
are settled and coverage/accounting reconcile.

For the exploratory bootstrap, order strata lexicographically `(0,0)`, `(0,1)`,
`(1,0)`, `(1,1)`, and members by world index. Initialize
`Random(2026101602)` afresh for each endpoint. Each of 10,000 draws samples
five members with replacement per stratum, using the existing `choice`-based
algorithm, and averages the twenty selected paired differences. Sort the draws;
report elements 250 and 9750, zero-based. Do not independently resample agents,
arms, calls or prefix records. The same algorithm applies to the principal
effort contrast. The original Course-7 seed/interval stays unchanged.

If any required pair is unknown, do not produce a primary paired interval from
complete cases. If any contrast stratum is constant, explicitly report its
zero empirical variation; if interval width is zero, add exactly:

```text
Degenerate empirical bootstrap interval; it does not establish population
equivalence or absence of an effect. Only the observed cohort contrast is known.
```

Display the warning even when both policies achieve perfect success, not only
at a failure floor. There is no precision/power claim, significance test,
equivalence margin or direction-based stopping rule in this course study.

### 6.2 Effort and process

For each continuation, include every actual attempt's ready-model seconds,
calls and input/output tokens, including rejected actions and unsuccessful
episodes. Count only legally delivered messages as messages. Unknown effort
remains unknown; do not silently sum missing time as zero. If any whole-world
effort pair is unknown, the intended-cohort mean contrast and its interval are
unavailable; separately show observed costs and their coverage.

The original prefix executes once physically. Charge that prefix to each
hypothetical end-to-end policy logically, and report it separately. Scalar and
diagnostic calls are physical research cost, not distributed-policy cost.
Show recovery outcome alongside each world's time/calls. Do not use cost per
successful case as a primary efficiency measure or count setup/load overlap
twice in wall time.

Derive these process displays from existing raw records and immutable worlds:

| Display | Definition / denominator |
|---|---|
| Syntax, schema, legal action | Separate checks per attempted call, by group and phase; call denominators are behavior-dependent |
| Episodes affected by illegality | At least one rejected action / intended episodes in that phase; unknown coverage separate |
| Terminal reason | Both submitted, waiting deadlock, horizon exhaustion, or other recorded terminal failure; no conflation with unknown |
| Completion / agreement | Both present; and identical submitted integers; identify wrong agreement separately |
| Locally refutable submission | Submitted value strictly below that agent's current local maximum; report count over forty intended main-agent slots per policy, plus present/unknown submission coverage |
| Obsolete-answer repetition | Submission equals the withdrawn original global maximum; show worlds and submissions; clear's old-value unavailability is a stated limitation |
| Original correctness | Correct original teams / twenty; descriptive correct-prefix recovery table, with no extra interval/test |

No new primary composite “coordination score” is introduced. A preceding message
alone does not establish sufficient information; a retained unchanged-peer report
can sometimes suffice without a new message. Avoid an automatic “no fresh message
means premature” label.

Use a six-category casebook selected without narrative discretion. For each
category take the lowest-index main world meeting it; categories may share a
case. Within a world, use phase order prefix/retain/clear, then persisted event
order. Categories are: illegal action; locally refutable recovery submission;
retained obsolete answer; clear-only success; retain-only success; both success.
Report an absent category as absent rather than substituting a striking case.

A human reads those exact permitted views/actions and may describe literal
notice-as-answer statements, impossible promised adjustment, or message/submit
contradictions, citing call IDs. Other observed issues can be appended explicitly
as exploratory cases. This is descriptive review, not causal attribution or an
estimated population frequency. One reviewer is acceptable if named as such;
do not claim independent coding, complete blinding, or human approval that did
not occur. No LLM judge is selected.

## 7. Later implementation work and acceptance

The [existing I-01 package](../../recovery/i01/) already supplies the small state
machine, raw-call storage, admission owner, resident processes and reports.
Inspection found hard-coded legacy counts/policies in `core.py`, `policy.py`,
`workflow.py`, `store.py` and report/continuation surfaces. Merely changing JSON
counts would not implement this design. Preserve historical paths and artifacts;
use explicit new-regime behavior rather than a generic experiment framework.

| Order / work item after approval | Existing surface to adapt | Required acceptance evidence |
|---|---|---|
| 1. Adopt the scoped amendment and immutable new condition | Specification §12 and living implementation handoff, new condition configuration | Explicit adoption diff lists changes versus legacy; no inference authorization inferred |
| 2. Bind data/schedule and common presentation | `core.py`, native request construction in `inference.py`, existing manifest/source binding | Exact text/rendering/privacy tests; 28 saved disjoint worlds; all assignment balances; seed schedules and literal sibling transforms |
| 3. Add four diagnostic request constructors and objective pilot decision | Existing workflow/policy/checks paths | Four reachable fixture views and predicate tests; 3/4 and 7/8 boundary cases; no recovery-direction/qualitative veto; fixed candidate unchanged |
| 4. Update finite admission and resume accounting | Existing store, process, workflow and continuation code | First-stage limits 8/8/4/80/380, reserve 20, total 500; reloads charged; known outcomes never regenerate; unknown spending blocks |
| 5. Update read-only reporting/export | Existing `report.py`, UI and archive exports | All-world counts, bounds, bootstrap edges, new qualification/diagnostic rows, correct-prefix description, process/time coverage and unchanged legacy Course-7 reconstruction |
| 6. Deliver the thin complete notebook/source packet | Existing notebook builder/CLI/client/setup | New four-pilot workflow and ten batches, ordinary finite rerunnable cells, exports/inspection and bounded cleanup; no duplicated stores or embedded scientific implementation |

All items above are **unimplemented in this task**. Final native byte rendering,
token counts and runtime/resource behavior require the later implemented source
and appropriate verification. A precise design is not evidence of a passed
software or GPU gate.

### Focused deterministic checks before any later model run

1. **Mathematics/data:** independent original/revised maxima; unique old winner;
   exactly one edited record; replacement support; conditional-owner rejection
   reasons and limit; exact saved-seed regeneration and input disjointness.
2. **Presentation/privacy:** exact system/control text; actual nulls; record IDs
   not presented as answers; current sources last and lossless; owner-only new
   value; no truth, before-value, hidden eligibility or policy label. Include
   arbitrary multiline messages and token-bound adversarial histories.
3. **State/protocol:** legal exchange completes in at most three total calls;
   message-plus-wait and empty non-wait reject without effects; irreversible
   finality, send-before-finish, wake/deadlock/horizon semantics and charged turns;
   history boundaries and literal feedback retention; fresh isolated siblings.
4. **Diagnostics/gate:** each scripted input is a permitted reachable view;
   qualification eight legal outputs required; all four pilots retained;
   exactly 3/4 prefixes and 7/8 controls passes, either one fewer fails; ordinary
   main invalid/incorrect outputs never veto subsequent fixed worlds. Probe
   results, recovery effect and message labels do not alter admission.
5. **Accounting/resume:** scripted full-bound execution reaches 480 ordinary
   attempts, never a 481st; reserve reaches 20, never a 21st; total never exceeds
   500. A settled stage rerun spends zero. Interrupted-call retry and reload
   cycles cannot import results or reset charges. Verify lost-spending blocks,
   exact raw-outcome replay and branch-local effects across quiescent restore.
6. **Analysis/delivery:** hand-computed paired tables, incomplete pairs,
   constant-stratum warnings, all-success/all-failure cases, missing cost and
   correct-prefix denominators; fixed bootstrap reconstruction; source/wheel
   binding; portable ZIP/extracted restore; complete escaped raw conversations.

Use existing deterministic fixtures/checks where valid, add only cases needed
for these changed behaviors, and preserve the read-only Course-7 audit result.
No new testing framework, broad runtime refactor, publication infrastructure or
GPU test belongs in documentation-only approval preparation.

### Later actual-host gates, after separate execution authorization

Verify pinned dependencies/source, two distinct devices, fresh-state and finite
score evidence, current-load A/B/A consistency, eight legal scalar controls,
full 8,192+512 envelopes and ≥1.5 GiB headroom per device. Check the actual
session allowance and fixed deadline. Then run the declared diagnostics and
four pilots without tuning, and use the exact objective decision in the design.
Only then is the saved main scope eligible; eligibility itself does not grant
GPU/main authorization. Unknown/failed status must remain explicit throughout.

## 8. Exact adoption delta and exclusions

| Existing §12 choice | Selected new-regime delta |
|---|---|
| Compact Course-7 team prompt / generic feedback | Exact assistance package, phase/source layout and public-rule feedback above |
| Six qualification worlds, twelve controls | Four qualification worlds, eight controls, plus four separate diagnostic calls |
| Three pilot worlds, 60-call pilot cap | Four balanced pilots, 80-call pilot cap |
| Recorded ordinary pilot outcomes do not veto main | Fixed original-team/scalar usefulness decision, with all outcomes preserved |
| Device and order coupled in the realized generator | Explicit balanced joint assignment, independently shuffled within strata |
| Original master/bootstrap seeds | New seeds `2026101601` / `2026101602`; fixed twenty-world main preserved |
| 28-attempt contingency cap | 20; first-attempt cap 480 and hard total 500 |
| Ambiguous wording about owner-placement rejection | Explicit uniform sampling conditional on scheduled owner, separately recorded |
| Correct-prefix exploratory interval | Descriptive counts only in the new regime; original historical interval untouched |

No other scientific change is selected. In particular: no new task/model,
thinking mode, extra turns, action union, decoder constraints, auto-repair,
correctness feedback, new finality/waiting rule, main prefix screening, sham,
selective retention, source certification, repeated-generation selection,
changed scoring, replay substitution or pooled historical results.

The adoption and implementation changes above remain pending user approval.
All current files, including the existing practical investigation, are preserved.
Only this annex and its companion decision document are created by this task.
