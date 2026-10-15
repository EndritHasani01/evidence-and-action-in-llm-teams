# I-01 course-5: complete saved-run analysis

15 October 2026. **Evidence analysis only; no implementation, scientific setting,
gate, checkpoint or saved outcome is changed. No inference is run for this audit.**

Companion: [fix and experiment-improvement proposal](../proposals/i01-course-5-fix-and-improvement-proposal.md).

## 1. Finding

The experiment stopped because the first pilot contained **two syntactically
valid JSON replies with an illegal action combination: a nonempty message and
`wait: true`**. Neither reply is a JSON parsing failure. The current protocol
requires a waiting action to have both `message` and `submit` null. The validator
therefore rejects both correctly, and the precommitted zero-error pilot gate
refuses main admission.

This is distinct from the pilot's incorrect answers, premature finalization,
repeated obsolete value, missing submissions and deadlock. Those are recorded
experimental outcomes. No observed runtime, memory, token-limit, persistence or
budget failure explains this stop. The gate operated as implemented; whether
that gate is appropriate for measuring error-prone recovery is a design question.

There is no justified parser bypass or answer correction. There is a small
diagnostic improvement to make the error intelligible, and there are explicit
policy/prompt options in the companion proposal. Removing only the first gate
would be incomplete: a later main-admission check rejects pilot errors again.

## 2. Evidence and verification boundary

| Evidence | Observed value |
|---|---|
| [Executed notebook](../../notebooks/run/course-5/multi-agents-course-v3nb.ipynb) | 510,244 bytes; 33 code cells |
| [Selected checkpoint](../../notebooks/run/course-5/latest.zip) | 1,757,535 bytes |
| Source commit recorded inside checkpoint | `39ad71bf6b00aebade13c443ff3c693128945add` |
| Study ID | `20785b0a-1904-4cbe-9c8c-0442c39eb9ce` |
| Controller session ID | `bca33bff-34fa-4e19-a633-2a90cf36c736` |
| Study creation, recorded UTC | `2026-10-15T14:55:07.665191+00:00` |
| Latest archive boundary | `operator-error-check_pilot` |
| Archive boundary time, recorded UTC | `2026-10-15T15:04:17.087162+00:00` |
| Runtime | Linux, Python 3.13.15, two distinct Tesla T4 devices |
| Model | Pinned Qwen3.5-9B, revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` |
| Scientific mode | Direct/nonthinking, unchanged NF4/FP16 runtime and decoding |

SHA256 of the supplied ZIP:
`e70724265ed35c5232b85fbc9e769b05fd7cde5972dd4f6d3e7e82b8f0f910c8`.

SHA256 of the supplied executed notebook:
`b1cc0704c23c786b239013d7aa4d2b69eb4d03fab8c8d0527150e3ed37a006e4`.

Audit work actually performed:

1. Verified/extracted the selected archive into a temporary directory using the
   existing safe archive code. Its inventory and SQLite integrity checks pass.
2. Rebuilt `analysis()` read-only and compared it with the saved
   `reports/analysis.json`: **exact equality**.
3. Verified all **81** members listed in the saved source-release inventory.
   Saved scientific/runtime source identity matches the active implementation.
4. Regenerated all **29** worlds from the recorded configuration: exact equality.
5. Replayed the ten team calls through the actual strict validator and state
   transitions, checking turn eligibility, permitted views, prompt messages,
   scheduled seeds, literal retain/clear starts and complete terminal states.
   **All match exactly**. No model or tokenizer inference was needed.
6. Inspected all twelve pilot replies, qualification outcomes, stage/operator
   receipts, load/cache/headroom evidence, notebook execution coverage and logs.
7. Compared the twenty preparation outcomes with course-4 by logical call ID:
   all twenty have identical visible text and generated token-ID sequences.
   These remain separate charged physical executions, not reused observations.

Locations such as `reports/analysis.json` below refer to files **inside this
selected checkpoint**, unless a repository link is given. Artifact timestamps
are recorded UTC, not a proposed current-session deadline.

## 3. Notebook progression and the exact stopping point

The first fourteen code cells succeed. Cell fifteen, `check-pilot-1`, records one
`ActionStopped` exception. The remaining eighteen cells have no execution count
or outputs.

| Stage | Saved evidence | Interpretation |
|---|---|---|
| Configuration/workspace/window | Executed; 700-minute estimated window | No old result import; provider quota is unverified |
| Installation | Successful; 185.615 setup seconds | Earlier ensurepip/controller startup problems do not recur |
| New study | Created independent study with zero prior charges | No course-3/4 checkpoint reuse |
| Native/scripted self-check | Passed; `native_tokenizer: true` | Actual host/tokenizer acceptance is present |
| Weights and two workers | Both loaded; 71.935 + 33.653 seconds | Total observed load time 105.588 seconds |
| Execution plan | Bound at `14:59:59.655273+00:00` | Automatic policy fixed before model calls |
| Readiness | Six calls; both A/B/A comparisons equal | Cache/finite checks pass; no state-review request |
| Direct controls | Twelve valid, ten correct | Protocol-first admission passes |
| Full headroom | Both probes pass | Actual full-envelope feasibility observed |
| Pilot 1 | All three team phases and two controls terminal | Completed execution, unsuccessful recovery |
| Pilot 1 check | `valid_protocol: false` | Deliberate admission refusal, not a crashed pilot |
| Pilots 2/3 | Unexecuted | Unknown, not failed |
| Main admission and ten batches | Unexecuted; no `freeze` record | No main experimental result exists |
| Final report/archive/close cells | Unexecuted | Stage-error export still produced reports and a checkpoint |

The checkpoint's last generic action is a **successful error snapshot**. That
does not mean the failed scientific gate passed. The failed pilot-check record
and both error receipts remain available. Likewise, `pilot: complete` means the
pilot's bounded execution ended, not that its answers or protocol passed.

## 4. Hardware, runtime and framing

| Full-envelope measurement | Logical slot 0 | Logical slot 1 |
|---|---:|---:|
| Input tokens | 8,192 | 8,192 |
| Forced diagnostic output tokens | 512 | 512 |
| Ready-model seconds | 65.996 | 63.754 |
| Conservative observed free headroom | 6.787903 GiB | 6.783997 GiB |
| Required headroom | 1.5 GiB | 1.5 GiB |
| Result | Pass | Pass |

All twelve pilot calls have `failure: null`, `framing_error: null`, normal EOS
termination and positive native finite-score evidence. Their cache receipts
record fresh initial state, same-call cache use and disposal after the call.
This is evidence against a stale-cache explanation for this trace; it does not
prove every possible backend defect absent.

Pilot prompts are short relative to the frozen limits: prefix 337–416 input
tokens, retain 498–598, clear 355–413. The longest pilot reply is 78 tokens,
well below 512. Neither rejected reply was truncated. The only two `length`
terminations among all 32 calls are the intentionally forced headroom probes;
they are not failed scientific actions.

The controller log contains Transformers docstring `[ERROR]` messages about
`loss`/`logits` documentation and bitsandbytes deprecation warnings. Subsequent
load/inference/headroom success and the actual stop receipt show that these are
not the causal exception here. An unpinned dependency upgrade is not supported
as a remedy by this evidence.

One pilot uses logical slot 0 by its fixed world assignment. Slot 1 being idle
during that individual pilot is expected. The concurrent two-world main path
has not been exercised empirically in this run.

## 5. Qualification: accuracy and validity remain separate

| Qualification world | Original truth / submission | Revised truth / submission | Protocol |
|---|---|---|---|
| 00 | 950 / 950 | 921 / 921 | Both valid |
| 01 | 999 / 999 | 931 / 931 | Both valid |
| 02 | 1000 / 1000 | 981 / 981 | Both valid |
| 03 | 951 / 788 | 920 / 788 | Both valid, both mathematically wrong |
| 04 | 956 / 956 | 918 / 918 | Both valid |
| 05 | 992 / 992 | 987 / 987 | Both valid |

The earlier 11/12 mathematical cutoff is not the present blocker. The current
record correctly admits 12/12 protocol-valid controls with 10/12 exact accuracy.
Thinking makes zero calls and has twelve unexecuted planned controls.

These scalar controls contain the complete input and forbid messaging/waiting.
They do not test message-plus-wait choices, private information exchange or
two-agent finalization. Scalar JSON reliability therefore does not establish
team-action reliability. This is the observed qualification-coverage gap.

The twenty preparation calls repeat course-4's text and token sequences exactly,
with different measured execution time. Repetition is not independent evidence
that a new context will follow the protocol, and cannot be deduplicated out of
physical spending. A blind same-configuration rerun is not a demonstrated fix.

## 6. Pilot world and exact outcomes

Pilot `pilot-00` has twenty integers per private shard, not twenty-one. Its
unique original global maximum is **988**, at agent 0's zero-based record 15.
That value becomes **672**. The revised global maximum is **932**, also in
agent 0's current shard. Agent 1's unchanged local maximum is **923**.

Both independent full-information pilot controls are correct: original 988 and
revised 932. This shows success on these particular complete-input calls; it
does not establish that the team can coordinate on the same answer.

| Phase | Final private submissions `[agent 0, agent 1]` | Terminal reason | Exact team success | Turns / unused turns |
|---|---|---|---:|---|
| Original prefix | `[988, 923]` | `both_submitted` | 0 | `[2,1]` / `[1,2]` |
| Retain | `[988, null]` | `horizon_exhausted` | 0 | `[1,3]` / `[2,0]` |
| Clear | `[null, 1023]` | `waiting_deadlock` | 0 | `[2,1]` / `[1,2]` |

Original completion passes the objective completion check because both agents
submit. Correctness is a different condition: their values disagree, so the
team is unsuccessful. The revised phases are completed **terminal records**,
not successful two-submission recoveries. Their missing submissions are recorded
noncompletion in executed phases, not unknown/unexecuted work.

## 7. Original conversation: a coordination failure before revision

1. Agent 0 performs a legal silent wait.
2. Agent 1 sends a generic plan and privately submits its local maximum, 923.
   Its public message does not actually report 923. It claims twenty-one values
   and refers to “Agent 2”, although the actual agent IDs are 0 and 1.
3. Agent 0 receives that plan, announces 988 and submits 988. The phase ends
   because both submissions are final. Agent 1 cannot revise its earlier 923
   when the later message arrives.

The original failure is not a missing oracle or broken maximum generator. It
shows local-answer finalization without achieving a common global answer.
Agent 0 is individually correct in this phase; that alone is not team success.
The false shard count and extra agent are model claims, not host data changes.

## 8. Retain: obsolete value, illegal wait and missing final submission

Retain starts with each agent's own prefix history preserved literally and
current revised source data. Agent 0 sees its changed record and current shard;
its authoritative local/global maximum is now 932.

1. Agent 0 nevertheless repeats its old maximum 988, sends the same old message
   and submits 988 immediately. Its visible reply **and generated token IDs are
   identical** to its earlier prefix submission, despite different current
   prompts and seeds. This is observable stale-value reuse, not evidence of a
   replay or cache implementation defect: the recorded request is revised and
   fresh-cache checks pass.
2. Agent 1 emits the first illegal message-plus-wait action. Its message and
   submission effects are rejected; the turn is consumed and generic invalid
   action feedback is recorded.
3. Agent 1 then twice sends a legal message-only action, explicitly reporting
   923 and reasoning from the stale 988. Each action keeps `submit: null` and
   `wait: false`. Messaging alone is legal, so these are not additional malformed
   actions. Neither produces the required final submission.
4. Agent 1 exhausts its three invocations. Agent 0 already submitted, so its
   two unused turns cannot be transferred or used to repair its final answer.

The visible evidence supports obsolete-value repetition and finalization/
coordination problems. It does not identify an internal “anchoring” mechanism
or prove that retaining history caused this outcome in a broader population.

## 9. Clear: recognized edit, illegal wait and a hallucinated maximum

Clear starts with empty agent histories and the same revised private shards,
notice, per-agent invocation seeds and recovery-first-speaker order as retain.

1. Agent 0's raw response explicitly recognizes the changed record value 672,
   but combines that message with waiting. The host rejects the whole action.
   Consequently **the message is not delivered** to agent 1. Recognizing an edit
   inside rejected text is not a submitted or communicated correction.
2. Agent 1 claims a maximum of 1023 and privately submits it. That value is
   absent from both saved shards and outside the generator's −1000…1000 range.
   Its statement about a partner record is also incorrect; −688 appears in its
   own shard, not the partner's revised record 15. Role/index confusion is a
   plausible interpretation, not an established internal cause.
3. Agent 0 receives the explicit 1023 message, sees the partner finished and
   performs a legal silent wait. Waiting only wakes on a later message. The
   partner is final and no other unfinished eligible agent can send one, so the
   phase terminates as `waiting_deadlock` with turns left unused.

The integer 1023 is **protocol-valid and mathematically wrong**. The validator
does not silently constrain submissions to actual input values or repair them.
The deadlock follows the declared waiting/finality rules and exact replay; it
is not an operating-system hang or provider timeout.

## 10. The two rejected replies, precisely

Call `pilot-00/retain/agent-1/invocation-0`:

```json
{"message":"Agent 0 has submitted 988. My shard maximum is 923. Since 988 > 923, I will not submit a new value. I am waiting for Agent 0's final submission confirmation.","submit":null,"wait":true}
```

Call `pilot-00/clear/agent-0/invocation-0`:

```json
{"message":"I see a revision notice updating my shard index 15 to 672. I will wait for the partner's submission to confirm the global maximum before finalizing.","submit":null,"wait":true}
```

For both calls:

| Check | Result |
|---|---|
| One JSON object parses | Pass |
| Exactly `message`, `submit`, `wait` | Pass |
| Declared field types | Pass |
| Native final framing, EOS and output bound | Pass |
| `wait` implies null message and submission | **Fail** |

The first has 65 output tokens and the second 50; neither reaches 512. Increasing
the token cap does not address this violation. Changing `wait` to false after
generation would change action execution and subsequent prompts. Allowing
message-plus-wait would introduce different protocol semantics. Neither is an
innocent JSON-parser correction.

Of the **ten team calls**, all ten parse as JSON and eight are legal actions.
Both pilot scalar controls are legal. Thus the pilot has **12/12 parseable JSON
replies, 10/12 protocol-valid actions, two semantic action violations**. Do not
report a 2/12 JSON syntax failure rate. These small, dependent denominators are
descriptive, not reliable estimates of a general failure probability.

## 11. Why execution stops and why one bypass is insufficient

The saved `automatic/pilot-1` record contains:

| Objective check | Saved result |
|---|---|
| Terminal evidence | True |
| Committed calls | True |
| Every required episode has calls | True |
| Both original-team submissions | True |
| Reconciled spending | True |
| Runtime integrity | True |
| Inspectable checkpoint | True |
| Valid protocol across all pilot phases/controls | **False** |

`scope_evidence(..., pilot=True)` counts both violations and sets `valid_protocol`
false. `check_pilot(1)` saves that result, then raises. The controller records
the stage error and exports; the notebook wrapper records its operator error,
exports again and raises `ActionStopped`. The frontend halts subsequent cells.

In [workflow.py](../../recovery/i01/workflow.py), `freeze()` later reconstructs
the pilot eligibility and also unconditionally rejects pilot truncation/
provider/framing flags and episode errors. Therefore removing one boolean check
or manually overwriting the pilot result cannot produce a coherent fix. The
immutable `execution_plan` and source binding also prevent an honest silent
change of procedure. This is an admission-policy change if adopted.

## 12. Effort, spending and time

| Scope | Physical calls | Generated tokens | Ready-model seconds |
|---|---:|---:|---:|
| Six readiness checks | 6 | 88 | 13.343 |
| Two forced headroom probes | 2 | 1,024 | 129.750 |
| Direct qualification | 12 | 193 | 25.433 |
| Pilot prefix | 3 | 155 | 18.095 |
| Pilot retain | 4 | 250 | 30.267 |
| Pilot clear | 3 | 121 | 14.772 |
| Two pilot controls | 2 | 32 | 3.900 |
| **Total** | **32** | **1,863** | **235.560** |

Physical observed dispatch time totals 235.730 seconds. Installation's 185.615
seconds and loading's 105.588 seconds are separate cost components; they are not
extra inference calls or exact provider billing. No effort field is missing for
these attempts. Retain has three delivered messages, clear one; rejected messages
are not counted as delivery.

Clear minus retain is −15.495712 ready-model seconds, −129 generated tokens and
−1 physical call in this one pilot. **Neither recovers successfully.** Earlier
deadlock is not evidence of more efficient successful recovery; no main effect
or superiority claim follows from these differences.

The shared prefix is physically executed once. Hypothetical end-to-end policy
costs would attribute its three calls to each policy: seven calls / 48.362176
ready-model seconds for prefix-plus-retain, versus six calls / 32.866464 seconds
for prefix-plus-clear. These are logical attributions, not two separately
executed prefixes, and exclude the separately charged controls. Adding them
would double-count the prefix in physical spending. Main logical policy costs
remain unavailable because the main episodes have not executed.

All 32 attempts are `completed`; there are zero in-flight, retry, contingency,
prior-study charges or recorded lost-spending exposure. Remaining arithmetic
allowance is **468/500**, with **28/28** contingency unused. Twenty-four scientific
calls have committed effects; the eight hardware diagnostics have durable raw
outcomes without episode effects by design.

The deadline in the archive is `2026-10-16T02:31:59.412575+00:00`, explicitly a
700-minute estimate within an approximately twelve-hour session. At the selected
snapshot, that configured clock has about 41,262 seconds left; about 737.675
seconds elapsed since its configured start. Neither establishes actual provider
allocation, quota, continued process life or release.

For context only, reconstructing the current main-only forecast formula using
the largest observed pilot/direct call, 8.566611 seconds, gives
`380 × (1.25 × 8.566611 + 5) + 120 = 6,089.140 seconds`, about 101.49 minutes.
This is an unaccepted heuristic, excludes the two unexecuted pilots and is not
a measured main runtime bound. It does show that the **observed stop was not a
session-time refusal**. Main admission has never run, so no final feasibility
decision exists yet.

## 13. Durability, reporting and shutdown

The failed action preserved both the controller stage receipt and notebook
operator receipt. The final ZIP contains the canonical worker pair, exact
source/wheel, manifest, plan, raw replies, effects, analysis, conversations,
tables, pilot-check CSV and all eight SVG/PNG figure pairs. The main notebook's
final report/export cells were unnecessary for this failure snapshot to exist.

Three saved PNGs were also visually checked against the reconstructed data:

| Figure | Verified interpretation |
|---|---|
| `paired-outcomes` | All twenty main worlds are in **Unknown**, not Neither |
| `qualification-outcomes` | Direct ten correct/two wrong; thinking twelve pending/unexecuted; excludes the separate pilot controls |
| `failure-labels` | Five episodes labelled wrong submission, two malformed action, one each horizon exhausted, waiting deadlock and obsolete value; labels overlap |

The failure figure counts labelled episodes, not mutually exclusive causes or
independent samples. The source charts preserve the distinction between a wrong
recorded answer and absent main evidence. All eight figure pairs exist; this
audit does not claim a separate visual review of every plot.

Two reporting limitations matter:

* `malformed_action` is too broad to explain syntax versus action semantics.
  The failing-check output omits the two exact violations and their call IDs.
* Failure CSV rows reference all calls of an affected episode. They are useful
  phase-level links, not precise attribution to every listed call. The default
  first-six raw audit view also omits the eighth pilot call, the clear violation.
  Complete raw evidence exists in the exported conversation files.

The `close` cell did not execute, and saved load records contain no process-close
acknowledgement. This does **not** prove the workers are alive now, but automatic
shutdown after this error is not evidenced. An unattended stopped notebook can
leave allocated GPUs idle. Downloading the archive and stopping Kaggle remain
operator responsibilities; a checkpoint link is not an external backup proof.

## 14. What these results support

Supported observations: the pinned runtime can execute this preparation and
pilot; scalar mathematical capability exceeds the observed collaboration
performance on this world; the original interaction finalizes inconsistent
answers; retain visibly repeats an obsolete value; clear contains an invented
maximum; both recovery branches contain the same forbidden message-plus-wait
action type; storage and exact replay preserve these failures correctly.

Not established: a general retention effect, clean causal anchoring, clearing
superiority, thinking superiority, a population protocol-error probability,
twenty-world main performance, actual twelve-hour completion or completed human
communication review. One pilot world, one prefix realization and one invocation
seed schedule cannot support those claims.

All twenty intended main pairs remain **unknown**. Their clear-minus-retain mean
and bootstrap interval are unavailable, with the intended-population unknown
bounds still **[−1, +1]**. Pilots 2/3 are also unknown. Pilot 1's zeros must not
replace those missing outcomes. Correct-prefix analysis remains a later
descriptive stratum, not a reason to discard unfavorable main worlds.

## 15. Root-cause classification

| Finding | Classification | Consequence |
|---|---|---|
| Two message-plus-wait replies | Confirmed model action-protocol violations | Preserve invalid actions and turn costs |
| Correct strict validation | Confirmed implementation behavior | No parser relaxation justified as a bug fix |
| Zero-error pilot gate covers recovery failures | Current approved policy; potential mismatch with recovery objective | A changed gate needs a disclosed amendment |
| Scalar qualification does not cover team action choices | Demonstrated coverage limitation | Improve diagnostics and protocol guidance; do not infer team reliability |
| Premature local finalization and absent second submissions | Observed collaboration behavior | Clarify interface or measure as outcomes; never repair answers |
| Stale 988 and invented 1023 | Observed wrong scientific responses | Keep exact scoring; internal mechanisms remain uncertain |
| Duplicate later pilot-error rejection | Confirmed integration dependency | Fix proposal must cover automatic main admission too |
| Generic diagnostics and unexecuted close path | Operator-experience gaps | Improve explanation and bounded cleanup without changing outcomes |
| No model/headroom/accounting failure | Supported within this recorded run | No evidence-based need to change model/runtime, token caps or turn limits |

The [companion proposal](../proposals/i01-course-5-fix-and-improvement-proposal.md)
specifies a bounded recovery-policy amendment, safe continuation requirements,
optional future prompt work and focused checks. All remain proposals.

## 16. Minimal read-only reproduction

With the recorded `39ad71b` Python implementation (also the code in `3274411`),
the central archive/report check is reproducible from the repository root:

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from recovery.i01.archive import extract_selected
from recovery.i01.report import analysis

with TemporaryDirectory(prefix="i01-course5-read-") as temporary:
    run = Path(temporary) / "run"
    receipt = extract_selected("notebooks/run/course-5/latest.zip", run)
    rebuilt = analysis(run)
    saved = json.loads((run / "reports/analysis.json").read_text(encoding="utf-8"))
    assert rebuilt == saved
    assert rebuilt["summary"]["attempts"] == 32
    assert rebuilt["summary"]["known_pairs"] == 0
    assert rebuilt["summary"]["gates"]["automatic/pilot-1"]["protocol_errors"] == 2
    print(receipt["boundary"], rebuilt["summary"]["status"])
```

This extracts only into a temporary directory and creates no model/controller.
Use the saved version when reproducing exact JSON report equality after future
code changes; an intentionally extended report schema need not be byte-for-byte
identical to an older version's derived report.
