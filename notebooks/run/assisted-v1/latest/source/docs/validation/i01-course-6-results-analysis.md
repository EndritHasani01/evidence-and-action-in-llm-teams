# I-01 course-6: complete saved-run analysis

15 October 2026. **Read-only evidence analysis. No model inference, experiment
implementation, scientific amendment, checkpoint transition or outcome editing
was performed.** Companion: [repair and experiment-improvement proposal](../proposals/i01-course-6-fix-and-improvement-proposal.md).
The governing authority remains [specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).

## 1. Main finding

The course-5 repair **did work for pilot 1**. Its two illegal recovery actions
remain invalid, but the recovery-specific policy admits their recorded outcomes.
Course-6 proceeds to pilot 2 and stops there because the same class of model
error occurs in the **original prefix**, where the adopted policy deliberately
still requires every attempted action to be legal.

The blocking call is **`pilot-01/prefix/agent-1/invocation-0`**. It returns valid
JSON and correctly typed fields, but combines a nonempty message with
`wait: true`. Waiting permits neither a message nor a submission. The validator
rejects the action correctly; it consumes a turn and delivers no message.
Pilot 2 later reaches both original submissions, but the earlier protocol
violation remains part of its evidence and fails the strict prefix gate.

This is an **admission-policy limitation**, not recurrence of the earlier
environment failure, a stale source packet, incorrect JSON parsing, inadequate
GPU memory, insufficient time, an unfinished pilot or an accounting failure.
The current policy was explicitly narrower than allowing all team action
mistakes. Its implementation and the recorded failure agree.

The saved recovery behavior is nevertheless weak. Both executed pilots have
incorrect original teams and unsuccessful retain/clear recovery. Pilot 2's
retain branch repeats obsolete information; its clear branch confuses the new
record value with a submitted global answer. These failures must remain visible
even if a future admission amendment lets the experiment continue.

## 2. Evidence identity and checks actually performed

| Artifact or identity | Observed value |
|---|---|
| [Executed notebook](../../notebooks/run/course-6/multi-agents-course-v4nb.ipynb) | 736,397 bytes; 33 code cells |
| [Selected checkpoint](../../notebooks/run/course-6/latest.zip) | 1,870,644 bytes |
| Source commit inside checkpoint | `b92cdbfcc9084e873dc231a4a27fe9114aed5725` |
| Execution policy | `i01-recovery-admission-run-all-2026-10-15` |
| Scalar qualification policy | `i01-direct-protocol-2026-10-15` |
| Study | `3855b41b-5333-491d-91bc-78629d519ec0` |
| Controller session | `44b57b0b-62cd-4493-b373-bcbf5ef188e7` |
| Study creation, recorded UTC | `2026-10-15T16:32:07.233487+00:00` |
| Last archive boundary | `operator-error-check_pilot` |
| Archive boundary time, recorded UTC | `2026-10-15T16:43:02.797788+00:00` |
| Runtime/model | Linux Python 3.13.15; pinned Qwen3.5-9B, direct/nonthinking, NF4/FP16 |
| Model revision | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` |

ZIP SHA256:
`8b48977d6389940f92eb694d67a636362de0f5ee27127b8223d452ff57b19c79`.

Executed-notebook SHA256:
`e2765537e83cb5e2e6b33a7b5c6ac00a026962032e7e2e4d99591688a456ad10`.

The two supplied files contain the available evidence; the study folder is
inside the ZIP. References such as `reports/analysis.json` below refer to that
selected archive. All artifact times below are explicitly recorded UTC, not a
deadline to reuse for a later session.

Checks actually completed without inference:

1. Safely extracted the selected ZIP into a temporary audit directory using
   the existing archive verifier. Inventory/hash verification and both SQLite
   integrity checks passed.
2. Reconstructed read-only `analysis()` and compared it with saved
   `reports/analysis.json`: **exact equality**.
3. Verified all **89 source-release inventory members**. The saved source
   identity exactly matches the active implementation; all **46 Python modules**
   in that identity match the bundled wheel bytes.
4. Regenerated all **29** qualification/pilot/main worlds from the saved config:
   exact equality, including revisions, seeds and orders.
5. Replayed all **19 team calls** across the two pilots through the actual
   validator and state transitions. Turn eligibility, call IDs, permitted
   views, prompt messages, seeds, literal sibling starts and final states all
   match. The four pilot control calls were also inspected against exact truth.
6. Inspected all raw pilot replies, direct qualification rows, attempt/effect
   accounting, notebook execution coverage, host/load/cache/headroom receipts,
   cleanup evidence and controller logs.
7. Compared the first **32 logical calls** with course-5: all exact requests,
   visible replies and generated token sequences match. These are separate,
   newly charged executions, not reused physical calls or independent worlds.
8. Compared normalized code text in all 33 executed cells with the notebook
   bundled in the source packet: exact equality. Kaggle's JSON representation
   and execution metadata differ; the stage code does not.
9. Confirmed eight PNG/SVG figure pairs are present. Visually inspected paired
   outcomes, failure labels and recovery-time figures against their data.

The audit did not modify the supplied ZIP/notebook, run workers, download
weights, execute a model or create an amended passing decision.

## 3. Notebook progression

Sixteen code cells finish successfully. The seventeenth, `check-pilot-2`, raises
one `ActionStopped` exception carrying the reported `ValueError`. The remaining
sixteen code cells have no execution count or output.

| Stage | Saved result | Interpretation |
|---|---|---|
| Configuration/source/window | Executed; correct b92cdbf packet and planning basis | No old checkpoint import |
| Runtime setup | Passed; 197.637 seconds | Verified pip bootstrap, no ensurepip failure |
| Native self-check | Passed; `native_tokenizer: true` | Includes scripted persistence/protocol/bound checks; zero model attempts |
| Weights/load | Both replicas loaded; 110.860 seconds total | Exact pinned model/runtime preserved |
| Execution plan | Bound at `16:37:06.408701+00:00` | Before first admission at `16:37:09.303634+00:00` |
| Readiness | Six probes; both A/B/A comparisons equal | No state-review override needed |
| Direct qualification | 12 legal committed controls; 10 correct | Protocol gate passes; accuracy remains diagnostic |
| Full envelope | Both 8,192-input/512-output probes pass | Current-load capacity acceptance present |
| Pilot 1 and check | Executed, terminal, admitted | Course-5 recovery errors no longer veto |
| Pilot 2 | All three team phases and both controls terminal | Its execution completed before the check |
| Pilot 2 check | Only `valid_protocol` fails | One original-prefix action is admission-blocking |
| Pilot 3/check | Unexecuted | Unknown, not a failure |
| Main admission and ten batches | Unexecuted; no `freeze` record | No main outcome exists |
| Final report/archive/close cells | Unexecuted | Error finalization nevertheless produced reports, export and worker closure |

There is no evidence that the operator failed to upload the repaired notebook.
Pilot 1's passing gate, the recorded policy and matching source/wheel/cell code
directly establish that the repaired flow was used.

## 4. Runtime, isolation and accounting

### 4.1 Hardware and native execution

The host reports two distinct Tesla T4 UUIDs, each with 15,360 MiB:

- Slot 0: `GPU-5e6614e1-d36a-82b3-cebd-17337700771d`.
- Slot 1: `GPU-d9ce1bfa-65a1-9e31-8a6c-2e4c2d50b956`.

Replica PIDs are 357 and 371, with load times 64.042 and 46.817 seconds.
Their `CUDA_VISIBLE_DEVICES` values are respectively `0` and `1`. Both child
backends report `cuda:0` because each masked process numbers its visible device
locally; this is **not evidence that both replicas used one physical GPU**.
The slot/UUID/mask/PID evidence resolves that apparent ambiguity.

Each full-envelope probe uses exactly 8,192 input and 512 generated tokens.
Observed free-memory lower bounds are **6.787903 GiB** and **6.783997 GiB**,
well above the required 1.5 GiB. Their ready-model times are 68.027 and 68.351
seconds. These are deliberately forced-length hardware diagnostics; their
`truncated: true` flags do not indicate truncated scientific replies.

All 43 outcomes have null provider failure and framing error. Forty-one end at
EOS; only the two forced envelope probes end at the length limit. The longest
ordinary scientific response is 149 tokens, below the 512-token limit. All calls
record fresh initial caches, same-call cache use and disposal after the call.
The finite-score and A/B/A evidence passes. None of these observations proves
all future GPU calls will succeed, but none implicates a backend defect here.

Controller log `[ERROR]` entries concern missing `loss`/`logits` documentation in
an upstream output class, and FutureWarnings concern bitsandbytes size checks.
They coexist with successful loading/generation. No execution traceback, OOM,
NaN/cache failure or provider-death record explains this gate. Upgrading the
runtime or installing unrelated packages is unsupported by the evidence.

### 4.2 Physical and logical accounting

| Stage | Completed physical attempts | Generated tokens | Ready-model seconds |
|---|---:|---:|---:|
| Hardware: six readiness plus two envelopes | 8 | 1,112 | 150.568 |
| Direct qualification | 12 | 193 | 27.044 |
| Two pilots including four controls | 23 | 1,113 | 139.481 |
| Total | **43** | **2,418** | **317.093** |

All 43 admissions are completed; there is no admitted/in-flight attempt. Slots
contain 22 and 21 calls. All **35 scientific calls** have committed effects.
The eight hardware calls are raw diagnostics without episode effects, as
designed; they are not eight persistence failures.

The study is explicitly independent: prior spending is zero, contingency is
0/28 and arithmetic remaining allowance is **457/500**. Historical 45-attempt
context is labelled separately, not imported. No retry, unknown spending or
gap charge is recorded. This archive still cannot establish absence of any
activity after its own boundary; later resume needs real exit/tail evidence.

Physical dispatch time is 317.326 seconds. Loading, setup, downloads, checkpoint
work and allocated idle time are separate. Shared prefixes count once physically
and toward each logical retain/clear policy cost. Do not add the logical policy
totals and call the result physical spending.

## 5. Direct qualification and full-information controls

The direct screen is **12/12 legal and committed, 10/12 mathematically correct**.
The two wrong scalar replies remain:

| Call | Truth | Submitted | Action legality |
|---|---:|---:|---|
| `qualification-03/control-original-direct` | 951 | 788 | Legal |
| `qualification-03/control-revised-direct` | 920 | 788 | Legal |

This screen therefore passes the adopted protocol-first policy. Thinking is not
selected or executed. Both controls on each executed pilot are legal and correct:
pilot 1 gives 988/932; pilot 2 gives 985/966. Across direct qualification plus
these pilot controls there are 16 legal scalar calls and 14 correct answers.
That is a descriptive call count across distinct scopes, not a 16-world accuracy
estimate: qualification pairs share six worlds and pilot controls share two.

Successful full-information controls do not establish competent distributed
collaboration. The team has only private shards and must communicate through
final actions. The gap between legal scalar output and natural team behavior
is central to this run, not evidence that the host should compute answers for it.

## 6. Pilot 1: the earlier recovery repair is verified on Kaggle

The original global maximum is 988 in agent 0's record 15. It is replaced by 672;
the revised global maximum is 932. Agent 1's original local maximum is 923.
Each shard has exactly twenty integers.

| Phase | Calls | Final submissions `[agent 0, agent 1]` | Terminal reason | Team success |
|---|---:|---|---|---:|
| Prefix | 3 | `[988, 923]` | `both_submitted` | 0 |
| Retain | 4 | `[988, null]` | `horizon_exhausted` | 0 |
| Clear | 3 | `[null, 1023]` | `waiting_deadlock` | 0 |
| Original control | 1 | `988` | `control_completed` | 1 |
| Revised control | 1 | `932` | `control_completed` | 1 |

The two illegal wait/message combinations from course-5 recur identically in
retain agent 1's first invocation and clear agent 0's first invocation. Both
are preserved as `malformed_action`, with diagnostic reason
`wait_requires_null_message_and_submit`, and **`admission_blocking: false`**.
The pilot passes because its prefix/controls are legal and all durable/runtime
prerequisites pass. It does not become a successful team experiment.

Earlier observed errors persist: claims of 21 integers and an extra “Agent 2,”
premature local-maximum submission, withdrawn 988 repeated under retain, missing
final submission, and an invented clear answer 1023. The integer 1023 is a legal
wrong submission under the strict-integer action contract; there is no rule to
clamp it or replace it with an input value.

All 32 calls shared with course-5, including preparation and this pilot, have
identical requests and token sequences. This supports reproducibility of these
observations and confirms that the policy repair did not modify model prompts
or delivery. It does not provide a second independent pilot-world replication.

## 7. Pilot 2: complete trace and the blocking action

### 7.1 World and revision

Agent 0's local maximum is **813**. Agent 1's original local/global maximum is
**985** at zero-based record 15. That record is replaced by **25**, leaving
**966** as both agent 1's local maximum and the revised global maximum. Agent 0's
shard stays unchanged. Recovery runs **clear first, then retain**, with matched
per-agent/invocation seeds across siblings on logical slot 1.

### 7.2 Original prefix: four calls, one illegal action, both submissions

1. **Agent 0, invocation 0:** silent legal wait. No answer or message is delivered.
2. **Agent 1, invocation 0:** identifies its maximum as 985 and produces this raw
   reply, 149 tokens, EOS, 16.645948 ready-model seconds:

   ```json
   {"message":"I see your shard. I will scan for the maximum value. My shard: [497, 966, -234, 36, 849, 815, -663, -6, -768, 34, -430, 328, -282, -891, 740, 985, -998, -348, 150, -746]. Max in my shard is 985. I will wait for your shard to confirm the global maximum.","submit":null,"wait":true}
   ```

   JSON syntax and field types pass; action legality fails. Nothing in this
   message reaches agent 0. Agent 1 receives only the bounded feedback
   “Previous action invalid; no action delivered.” Its turn is consumed.
3. **Agent 1, invocation 1:** emits “I see your shard contains -998. I will submit
   985 as my maximum.” and privately submits 985 with `wait: false`. This legal
   message wakes agent 0. Agent 1 acts twice consecutively because agent 0 was
   waiting; the replay verifies this is the intended scheduler behavior.
4. **Agent 0, invocation 1:** sees the delivered 985 message and the partner's
   finished status, but submits its own local maximum 813 without a message.

The final pair is `[813,985]`, incorrect for global truth 985, but both final
submissions exist within bounds. `original_team_completed` is therefore true.
The earlier invalid action still makes prefix `valid_protocol` false. Later
legal completion does not erase a prior consumed invalid turn.

The claim about seeing a partner shard is unsupported by the permitted view:
agent 1 received no partner message, and -998 is actually in its own shard.
The replay shows no hidden partner input. This is a model attribution error,
not evidence that the host leaked the partner's private records.

### 7.3 Clear: revision-value confusion and propagation

Agent 0 initially asks for the new value at the changed partner record, again
using a nonempty message with `wait: true`. Its 112-token EOS response is
rejected, so **the request is never delivered**. Its index claims are also wrong:
its own zero-based record 15 is -547, not -690; index 17 is 169. Asking a partner
for unavailable private information is not itself a host defect, but the illegal
action suppresses that attempted communication.

Agent 1 then receives only its actual revised shard and owner notice containing
`new_value: 25`; no partner submission/message has arrived. Nevertheless it says:

> Partner submitted 25, which is already in my shard at index 15. No other value
> in my shard is greater than 25. I will submit 25.

It legally sends that text and submits 25. The message misattributes the factual
edit as a partner submission and contradicts its current shard, which contains
966 and several other values above 25.

Agent 0 receives that public message and emits **the same visible reply and
token sequence**, submitting 25 too. The claim “in my shard at index 15” is false
for agent 0, whose unchanged local maximum is 813. This is observable propagation
of an erroneous message; the host does not certify or repair it.

Clear ends `both_submitted`, final pair `[25,25]`, score zero. Agreement and
procedural completion are not evidence of correctness. The illegal clear action
is diagnostic under the current policy and is not the admission blocker.

### 7.4 Retain: preserved mistakes, message/submission inconsistency

Retain starts from the literal original histories, not the already executed
clear conversation. Both agents are reopened with authoritative current shards
and the same factual revision notice rules.

Agent 0 sends the previous partner text about -998/985, but its private submission
is **813**. The message claims a submission of 985 while the actual submission
field says 813. This is legal under the schema: message claims are not certified
and the host must not replace the private submission with a number in prose.

Agent 1, whose current shard contains 966 and whose old 985 record now contains
25, repeats that same public sentence and submits **985**. It has also received
agent 0's repeated message. Retain ends in only two calls, `[813,985]`, score
zero. The repeated sentence remains token-identical to the original legal
agent-1 prefix reply, even though the relevant requests differ.

These are strong observable examples of obsolete-value repetition and incorrect
source/role attribution. They do not identify an internal anchoring mechanism.
Current values, historical messages and a new received message coexist; no
hidden-thought audit establishes why the model chose them.

## 8. Exact gate decision and why the error name repeats

Pilot 2 has these saved objective checks:

| Check | Result |
|---|---|
| All required phases/control states terminal | True |
| Raw outcomes/effects committed | True |
| Every required episode has calls | True |
| Both original-team submissions present | True |
| Reconciled spending | True |
| Runtime integrity | True |
| Inspectable checkpoint | True |
| `valid_protocol` under the adopted phase-sensitive policy | **False** |

All eleven pilot-2 replies are valid JSON with valid field types. Nine are legal
actions. Its two illegal actions have the same precise reason, but only the
prefix one is admission-blocking. This distinction is explicitly persisted in
`automatic/pilot-2.validation` and `reports/validation_details.csv`.

The source path is:

1. [`policy.admission_blocks()`](../../recovery/i01/policy.py) treats a pilot
   illegal action as blocking unless its phase is retain/clear under the current
   recovery policy.
2. [`workflow.scope_evidence()`](../../recovery/i01/workflow.py) also checks
   prefix/control state-event errors. Thus changing only one diagnostic boolean
   would not implement a legitimate alternative gate.
3. `check_pilot(2)` persists `passed: false`, then raises the reported error.
4. The stage wrapper exports, closes workers, exports closure evidence and
   returns a stopped action. The notebook raises before any later stage.
5. Automatic main admission also reconstructs pilot evidence. A first-gate
   bypass would still be insufficient and would violate the precommitted plan.

The generic `valid_protocol` label obscures which phase blocks. The detailed
diagnostics are now correct and available, but the top-level exception can be
improved to name the exact blocking call and reason immediately.

## 9. Compliance, outcomes and effort

### 9.1 Syntax, schema and legal actions are distinct

| Scientific pilot context | Recorded replies | JSON/schema valid | Legal actions | Admission-blocking replies |
|---|---:|---:|---:|---:|
| Original prefix | 7 | 7 | 6 | 1 |
| Retain | 6 | 6 | 5 | 0 |
| Clear | 6 | 6 | 4 | 0 |
| Original controls | 2 | 2 | 2 | 0 |
| Revised controls | 2 | 2 | 2 | 0 |
| Total pilot calls | **23** | **23** | **19** | **1** |

Team actions alone are 19/19 parseable and 15/19 legal. All four violations are
message-plus-wait combinations. Do not report 100% protocol compliance from
100% JSON parsing, or treat hardware forced output as scientific JSON trials.
The 35 scientific calls overall contain 31 legal actions and four illegal ones.

Both original teams are wrong. All four observed recovery episodes fail, and
none of their six non-null final submissions equals its revised truth. Two
additional agent submissions are missing in pilot 1. Pilot 3 is unknown.

### 9.2 Measured team-phase costs

| World | Phase | Calls | Generated tokens | Ready-model seconds | Delivered messages |
|---|---|---:|---:|---:|---:|
| pilot-00 | Prefix | 3 | 155 | 19.273 | 2 |
| pilot-00 | Retain | 4 | 250 | 31.859 | 3 |
| pilot-00 | Clear | 3 | 121 | 15.372 | 1 |
| pilot-01 | Prefix | 4 | 223 | 27.187 | 1 |
| pilot-01 | Retain | 2 | 78 | 10.557 | 2 |
| pilot-01 | Clear | 3 | 222 | 26.277 | 2 |

Retain is 16.487 seconds slower in pilot 1 and 15.720 seconds faster in pilot 2.
Every compared recovery fails. Shorter time reflects different early exits,
noncompletion and premature final answers; it is not successful-recovery
efficiency. The sum of recovery calls is six per condition across these two
pilots, but averaging away their different failure modes is uninformative.

The existing failure figure counts episodes with overlapping labels: wrong
submission 8, malformed action 4, obsolete repetition 2, horizon exhaustion 1,
waiting deadlock 1. The wrong-submission count includes two qualification
controls. These are episode-label counts, not eight independent team worlds.
`failure_analysis.csv` often lists all calls in the labelled episode; exact
offending-action references should instead come from `validation_details.csv`.

## 10. Clock, resource feasibility and cleanup

The session-clock repair works. Its saved observation retains:

- Timestamp `2026-10-15T16:28:48.171020+00:00`.
- `remaining_minutes: 700` and `basis: planning_estimate`.
- Fixed deadline `2026-10-16T04:08:48.171001+00:00`.

Initialization records the controller observation later, without erasing the
original estimate. Setup/downloads therefore consume the window. At the archive
boundary, **854.627 seconds** of that planning window have elapsed and
**41,145.373 seconds** remain. This is approximately 14.24 minutes elapsed and
685.76 configured minutes remaining, not verified provider quota or GPU-hours.

No main-admission forecast was accepted, because pilot 2 blocked first. Using
the existing formula read-only, the maximum observed scientific call is
16.645948 seconds. The main-only heuristic is
`380 × (16.645948 × 1.25 + 5) + 120 = 9,926.825 seconds`, about 165.45 minutes.
It excludes the remaining pilot and is not a whole-run guarantee. The latest
saved export-timing maximum is 3.290 seconds; that does not prove final exports
with twenty-world traces/figures will cost the same. Time/budget shortage is not
the observed stop, and no forecast licenses extra worlds or larger limits.

Error cleanup is positively evidenced:

1. Stage failure recorded at `16:42:53.019600+00:00`.
2. Pre-close checkpoint receipt created at `16:42:55.847957+00:00`.
3. Both workers acknowledge termination at `16:42:56.594341+00:00` and
   `16:42:56.905019+00:00`, exit codes -15.
4. Closure evidence is saved in the load-session rows and failure-cleanup
   receipt; the later operator-error archive verifies.

The last management action is a successful snapshot, but summary status remains
**partial / scientific gate blocked**. The notebook prints that distinction,
so `snapshot: complete` no longer implies resumed research. `provider_release`
remains **unknown**. Worker termination does not prove controller exit, Kaggle
deallocation or external download. Neither final close-cell execution nor those
external events can be inferred from this archive.

## 11. Reporting completeness and limits on conclusions

The archive contains full conversations in HTML/text/JSONL, raw prompts/replies,
SQLite backups, inputs/config/seeds, qualifications, pilot checks, validation
details, compliance denominators, costs, sessions, annotations and eight figure
pairs. The final notebook report cell did not run, but automatic checkpoints
generated the saved reports correctly. The annotation table is empty; human
communication/mechanism review remains retrospective and pending.

All **twenty main pairs are unknown**. The primary contrast is unavailable,
missingness bounds are `[-1,1]`, and the correct-prefix main stratum has no
observed denominator. These are not twenty failures or an estimated zero effect.
The paired plot correctly shows twenty unknown worlds. The main recovery-cost
plot is empty because it excludes pilot worlds and no main world ran; an
explicit “no main data” notice would explain this better than empty axes.

The evidence supports conclusions about this small development run:

- The patched online runtime, native capacity, source binding, raw/effect replay,
  recovery-specific gate, detailed diagnostics, clock provenance and failure
  worker cleanup functioned in the observed stages.
- Scalar JSON compliance does not transfer automatically to legal waiting,
  reliable collaboration, factual role attribution or revision interpretation.
- The remaining prefix-perfect admission rule can stop otherwise complete,
  auditable team episodes on an ordinary model mistake.
- Repeated obsolete values, misleading messages and revision-value errors are
  observable; internal mechanisms and treatment superiority are not established.

It does not establish that direct mode is universally better, that thinking
would repair these behaviors, that clear is superior/inferior, or that a future
complete study has sufficient precision. Four failed pilot recoveries across
two fixed worlds cannot replace the intended twenty-world paired analysis.

## 12. Diagnosis and next decision

There is no demonstrated host/validator defect to repair by installing packages,
changing GPU settings or coercing JSON. The immediate policy choice is whether
the study targets a perfectly compliant team interface or the practical recovery
of an error-prone team whose ordinary mistakes are measurable outcomes.

The earlier amendment only relaxed recovery legality; course-6 exposes the
remaining boundary. The companion proposal evaluates a consistent policy across
all team phases, an explicitly separate prompt-clarification option, better
top-level diagnostics, focused regression cases, and truthful fresh/continuation
routes. None of those proposed scientific changes has been adopted here.
