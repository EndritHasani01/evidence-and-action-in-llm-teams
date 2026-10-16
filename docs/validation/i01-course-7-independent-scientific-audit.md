# I-01 course-7: complete independent experimental analysis

16 October 2026. **Forensic analysis only.** No executable code, prompt, model,
configuration, scoring rule, scientific contract, checkpoint or original result
was changed. No model was loaded and no inference was run. This is a new review
of the evidence, not a replacement for the historical analysis or a completed
independent human annotation study.

Companion: [Experimental Quality Improvement Proposal](../proposals/i01-course-7-experimental-quality-improvement.md).
Authority: [specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
Engineering context: [implementation handoff](../IMPLEMENTATION_PLAN.md#i-01-implementation-handoff-15-october-2026)
and [I-01 WBS](../plans/i01-course-implementation-wbs.md).

## 1. Audit judgment

Course-7 is a **complete, internally consistent execution of the adopted
error-prone-system experiment**. It is also a **weak test of recovery from a
previously successful collaboration**. These judgments concern different things.

The two canonical databases independently establish twenty complete main pairs:
seventeen neither-success, one retain-only, one clear-only and one both-success.
Each policy succeeds on 2/20 worlds. The finite-cohort clear-minus-retain success
difference is exactly zero. The prespecified exploratory bootstrap interval is
−10 to +10 percentage points. Neither policy superiority nor equivalence follows.

Only three original teams were correct. Ten main prefixes delivered no legal
message; nine prefixes ended without both submissions. Valid JSON concealed
substantial action illegality: 42/82 main-prefix calls were invalid. Recovery
frequently finalized a local answer before acquiring the other shard's maximum,
misread revision metadata as a partner submission, or repeated historical text.
These are visible failures of this complete agent environment, not evidence
that the scalar maximum operation alone is too difficult.

Retain repeated the withdrawn maximum in ten main worlds; clear did so in none.
That is an important observable contrast, but clear has no access to the old
maximum through either its current input or its erased history. The contrast
does not isolate a psychological anchoring mechanism or establish that clear
successfully processed the correction. Clear still failed in eighteen worlds.

The evidence does **not** reveal a scoring, delivery, sibling-isolation or
recorded-state discrepancy that explains away the poor performance. The main
weakness is scientific resolution: the intervention combines useful information,
bad conclusions, conversational examples, feedback and context length, in a
system that rarely established a correct original solution. Additional samples
of this exact system would estimate its practical failure rate more precisely;
they would not by themselves isolate recovery mechanisms.

### 1.1 Prioritized findings

| ID | Priority | Finding and evidential status | Implication |
|---|---|---|---|
| F01 | Critical for interpretation | **Verified:** 3/20 correct prefixes; retain/clear each 2/20; only two discordant pairs | Very little evidence concerns revising a correct shared solution; zero aggregate difference is inconclusive beyond this cohort |
| F02 | High | **Verified:** 60/206 team calls violate action semantics, despite valid JSON and field types | Scalar-format qualification did not qualify the collaborative action environment |
| F03 | High | **Verified behavior:** private finality, local-only submissions and nonexistent partner-submission claims recur | Coordination and interface interpretation are major observed bottlenecks; repairing arithmetic alone is insufficient |
| F04 | High | **Verified design limitation:** history retention changes multiple information and presentation elements together | Identifies a total policy contrast, not a pure memory, anchoring or correction-specific effect |
| F05 | High | **Verified design limitation:** physical treatment order is perfectly coupled to GPU slot | Sibling comparisons control device within a world, but order and device interactions cannot be separated |
| F06 | High | **Verified:** all shared requests/token sequences match earlier runs; pilot gates were relaxed before main | Execution completion improved through admission changes, not demonstrated improvement in collaboration |
| F07 | Medium | **Verified:** retain uses 9.157 fewer mean recovery seconds, often while finalizing wrong answers | A bounded effort finding; not useful-work efficiency or time-to-correct-answer superiority |
| F08 | Medium | **Verified reporting limitation:** coarse `malformed_action` labels include legal-JSON/illegal actions; mechanism annotations are empty | Failure counts require explicit units and raw-call inspection |
| F09 | Medium | **Unresolved:** numerical equivalence of the quantized custom runtime to an independent reference; native retokenization not repeated here | Existing integrity evidence is strong but does not prove every numerical or tokenization property independently |
| F10 | Low, contract clarity | **Verified wording tension:** owner-placement rejection occurs although the contract says reject mathematical ineligibility only | Clarify balanced conditional sampling prospectively; no evidence of outcome-based selection |

## 2. Repository state, authority and evidence selection

### 2.1 State at the start of this audit

The working tree was clean on `feat/smaller-natural-experiment`, at
`464acc5a93e1418d58a37b904c7c99d7126b586b` (`run 7 unzip`). The preceding commits
were `4840458` (report/handoff), `7d8f854` (earlier read-only audit), and `3e0243c`
(imported run). The current checkout is **not** the executed source revision.

Inspection covered root `AGENTS.md`, README orientation, specification §12,
current I-01 handoffs/WBS, the historical course-3/5/6 decisions relevant to
admission and inference, and the implementation-research synthesis. Sections
1–11 and older four-peer experiments are separately scoped; they do not supply
extra I-01 requirements. Older WBS gate tables and preparation-only statements
remain dated history, superseded where §12 explicitly says so.

The run inventory contains `course-1` through `course-6` and one matching
`course-7/*` directory, `course-7-working`. Searches of the local notebook/run
tree found no newer course-7 archive or second study. This establishes the
latest **available local** complete run; it cannot establish what might exist
in an unconnected Kaggle session or another machine.

### 2.2 Canonical artifact identity

All archive-relative references below use this selected checkpoint:
[latest.zip](../../notebooks/run/course-7-working/latest.zip), also available as
[the extracted directory](../../notebooks/run/course-7-working/latest/).

| Identity | Independently checked value |
|---|---|
| Study | `b709c9bd-8d95-40c6-a19e-62a5f5e3c587` |
| Controller session | `a7bb7845-cf04-4efd-9b68-f74b9595cfaa` |
| Executed source commit | `65462e1e5fc687e1107d80a152e7d6c638ed93b7` |
| Execution policy | `i01-recorded-outcomes-run-all-2026-10-15` |
| Scalar qualification policy | `i01-direct-protocol-2026-10-15` |
| Archive boundary | `controller-close` |
| Final checkpoint, recorded UTC | `2026-10-15T18:15:12.210624+00:00` |
| Archive bytes / SHA-256 | 2,878,097 / `e4e2ce613dc8949ed6d5224e09bff19b96ee97f5d53065a80437e68b42cc4aca` |
| [Executed notebook](../../notebooks/run/course-7-working/multi-agents-course-v5nb.ipynb) bytes / SHA-256 | 4,067,407 / `f88899ca4b21faf970684be2be6ffa3f1fb4d189e87abf993af1107616f260a6` |
| Canonical stores | `worker-0.sqlite`, `worker-1.sqlite` |
| SQLite integrity | `PRAGMA integrity_check`: `ok` on both |

The ZIP and extracted directory agree byte-for-byte on all **161 ZIP files**.
The earlier audit also verifies the archive inventory, 49 scientific source
identity members, 98 source-release members and 46 Python modules in the wheel.
The scientific source hashes match the current checkout; the specification
snapshot also matches its current file. Release metadata lists only untracked
historical course-3/4/5/6 directories. That is not evidence of modified executed
scientific code. The bound source bytes provide stronger provenance than the
commit name alone.

### 2.3 Evidence hierarchy and audit scope

The primary records are [run.json](../../notebooks/run/course-7-working/latest/run.json),
the two SQLite stores, the packaged source, setup/load/native-check receipts,
attempt timestamps and the executed notebook. Generated summaries, CSVs and
plots were checked **against** these records.

The review inspected all 206 team responses, all 38 scalar scientific controls,
all 69 team episode states, original/revised shards and truths for all 29 worlds,
the eight hardware-call records, settings/seeds/token-vector evidence,
qualification/pilot/batch receipts and relevant logs. Every team request's
permitted view was reconstructed. Complete conversations include rejected raw
responses as well as legal delivered messages: those are different evidence.

There were two calculation paths:

1. The existing [course-7 audit](../../scripts/audit_i01_course7.py) was inspected
   and rerun with output in a temporary directory. All its assertions passed:
   exact saved-report reconstruction, 206 team replays, 38 control replays,
   regenerated inputs, source/wheel binding, seeds/settings, token-vector
   lengths and paired bootstrap reconstruction.
2. A separate temporary Python analysis used standard-library SQLite/JSON/math
   operations, without importing the project scorer or transition functions.
   It recomputed maxima, action legality, success, costs and intervals; walked
   turn eligibility, histories, waiting and finality; checked permitted views
   and reconstructed all terminal submission states. Its results agree.

The independent walk verifies that illegal replies delivered nothing, that
already submitted agents were not invoked again within a phase, and that the
literal retained/cleared histories were correct. The conversation JSONL contains
359 records: **252 exact call records + 107 exact episode checkpoints**, each
matching the SQLite fields. The 252 attempts are all completed first attempts;
their evidence equals their call outcomes. Scientific effects are committed
for 244 calls; hardware probes do not have scientific episode effects.

This audit did not rerun GPU inference, inspect inaccessible model internals,
retokenize using a newly loaded native tokenizer, or independently reproduce
custom-kernel numerical results. Source-enforced native request equality and
saved token vectors are evidence, not a substitute for such a separate check.
Snapshot consistency also cannot establish unrecorded past write timestamps.

## 3. What experiment was actually executed?

### 3.1 Task and population

Two agents each hold twenty integers in −1000…1000. A world has a unique original
global maximum. Its record is replaced by a value strictly below the maximum
of the other 39 records. Therefore the correct answer **always changes** and
the replacement is **never** the revised global maximum. The unchanged 39
records are still authoritative. Revised ties, such as two occurrences of 944
in `main-19`, do not make the maximum-value answer ambiguous.

All 29 original inputs are distinct: six qualification worlds, three pilots,
twenty main worlds. Independent arithmetic confirms every saved original and
revised truth, the single-record edit, the bounds and unique original maximum.
All worlds regenerate exactly from the recorded seed/configuration. No world
was replaced using a model outcome.

Main has five worlds in each `(changed owner, first speaker)` cell. First speaker
is the same before and after revision. The changed maximum's owner remains the
revised maximum's owner in six worlds; it moves to the other agent in fourteen.
These are realized task properties, not balanced post hoc success strata.

The generator conditions on the scheduled owner by rejecting otherwise eligible
draws. Across all 29 worlds it rejects 28 draws for `owner_block` (9 qualification,
1 pilot, 18 main), and zero for nonunique maxima or floor constraints; no world
needs more than five proposals. Exchangeable independent shards make this a
reasonable way to obtain the required balanced conditional population. However,
§12's phrase “Reject mathematical ineligibility only” does not literally describe
these placement rejections. This is a documentation ambiguity, not evidence of
favorable outcome selection or changed mathematical truths.

The native [I-01 generator](../../acl26-silo-bench/benchmark_generator/paradigm_i.py)
uses the same maximum-of-private-integers mathematics, with explicit aggregation
and broadcast guidance. Course-7 uses its own recovery event, action interface,
bounded schedule and scoring. It is an extension, not a native benchmark score.
SILO-BENCH motivates studying distributed computation failures; its general
findings do not establish the cause of this particular run's errors.
[SILO-BENCH paper, v2](https://arxiv.org/abs/2603.01045v2).

### 3.2 Information and intervention

| Element | Prefix | Retain recovery | Clear recovery |
|---|---|---|---|
| Current private shard | Original | Revised/current | Same revised/current |
| Changed owner/record notice | Absent | Present | Identical |
| Replacement value | Not visible in advance | Owner only | Owner only |
| Previously visible own legal actions, explicit submissions, received messages and feedback | Accumulates | Kept literally | Erased |
| Own invocation count / private submission / waiting status | New phase | Reset | Reset |
| Partner submission values | Private unless messaged | Private unless messaged | Private unless messaged |
| Partner finished indicator | Public boolean | Public boolean | Public boolean |
| Hidden evaluator truth / future edit / treatment label | Absent | Absent | Absent |

Retain does not retain old authoritative shard arrays as a separate source;
old values survive only where they were included in historical visible actions
or messages. Invalid raw outputs are preserved for the auditor, but not delivered
or inserted as successful actions in the peer's history. Generic invalid-action
feedback is retained. No private reasoning or cross-call hidden cache is intended
to carry forward.

The exact history presentation matters. A revision notice precedes the literal
history, whose entries are rendered as “Your action” and “From agent …” without
an entry-specific original/recovery phase tag. Thus old utterances such as
“3/3 invocations” appear in a new first invocation. This is a plausible temporal
interpretation burden; it is **not** a demonstrated implementation violation.

### 3.3 Actions and stopping

One reply has exactly `message`, `submit`, `wait`. Message-only, submit-only,
message-and-submit, and wait-only actions are legal. A nonempty message with
`wait: true` is illegal. Submission is final within a phase. Sending a message
and submitting delivers the message, then permanently finishes that sender for
the phase. Later messages are archived but do not reopen its answer.

There are at most three invocations per agent and six per phase. Invalid replies
consume an invocation and deliver nothing. Waiting resumes only on a legal
delivered message, not merely when a partner privately submits. The scheduler
can correctly invoke one agent consecutively if the other is waiting or finished.
It stops when both submit or no unfinished agent can progress. Correctness does
not determine stopping. An exhausted terminal failure is zero, not missing.

The task is solvable inside these limits: first agent messages its local maximum;
second agent messages and submits the maximum of the two local maxima; first
agent submits that result. This needs three total calls and at most two calls
for either agent, assuming correct local computation and message use. The
experiment's failures cannot be attributed to mathematical impossibility under
the declared budget. The protocol still requires learned planning and finality
discipline; it does not enforce this strategy.

### 3.4 Model and actual runtime

The run uses pinned Qwen3.5-9B revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, direct/nonthinking generation,
NF4 double quantization with FP16 computation, temperature 0.7, top-p 0.8,
top-k 20, repetition penalty 1, presence penalty 0, 512 output and 8,192 input
tokens. Siblings match per-agent invocation seeds; they do not share generated
continuation replies.

Actual host receipts identify Linux/Python 3.13.15 and two distinct Tesla T4s.
Each resident process sees one physical device. Both report all model tensors
on local `cuda:0`, which is expected under per-process device visibility, not
evidence that they used the same physical GPU. UUIDs differ. Torch is
2.11.0+cu128, Transformers 5.12.0, bitsandbytes 0.49.2, tokenizers 0.22.2,
accelerate 1.14.0 and huggingface-hub 1.19.0. Pip check reports no broken
requirements; loading records report no missing, unexpected or mismatched keys.

The attention implementation is `recovery_t4_sdpa`, prefill chunk size 256;
the recurrent fast path is unavailable. The loader's historical generation
report includes a 256-token default, but the I-01 adapter replaces settings
before each call. Every scientific persisted request has the selected 512-token
configuration; this is not evidence that scientific calls used a 256-token cap.

The official pinned model card's general direct-mode temperature/top-p/top-k
match this run, while its presence-penalty advice differs. The card also gives
different reasoning recommendations in different sections. None licenses
silently changing this frozen study or identifies its poor coordination as a
decoding defect. [Pinned model card](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/README.md).

## 4. Execution chronology, qualification and development history

Times in this table are recorded **UTC**; the run occurred during the evening
of 15 October 2026 in Budapest (UTC+2).

| Boundary | Evidence |
|---|---|
| Notebook begins | 17:40:46.594 |
| Independent study created | 17:44:38.664 |
| Native/scripted self-check | Pass, 17:44:54; no model attempts |
| Execution plan bound | 17:49:51.505, before the first attempt |
| First model admission | 17:49:54.406 |
| Six short A/B/A state checks | Complete; repeated A token sequences agree on each device |
| Twelve direct qualification controls | 12 legal, 10 correct; strict scalar-protocol gate passes |
| Two full-envelope probes | Each 8,192 input + 512 forced output tokens; headroom passes |
| Three pilots | All terminal, 35 attempts including controls; all three objective checks pass |
| Main admission/freeze | 17:57:54.267; no settings tuning recorded |
| First main admission | 17:57:57.858 |
| Ten fixed two-world batches | All terminal, 197 attempts; final main call finishes 18:14:34.730 |
| Report and verified snapshot | Notebook cells 31–32 complete |
| Worker closure | Both terminations confirmed at approximately 18:15:02 |
| Final checkpoint / notebook end | 18:15:12.211 / 18:15:17.128 |

All 33 ordinary notebook code cells execute in order, counts 1…33, with no
notebook error output. The complete notebook spans 2,070.534 seconds (34.51
minutes); study creation to final checkpoint spans 1,833.547 seconds. The
700-minute session window is explicitly an operator-reported planning estimate,
not measured provider entitlement. It was not needed to explain this stop: the
run finished with ample recorded deadline margin.

### 4.1 Qualification is narrower than collaborative capability

Qualification is scalar-only: no messaging, waiting, private finality planning
or source-revision interpretation. The model answers 10/12 correctly across six
original/revised world pairs. Both errors are on `qualification-03`, submitting
788 when the original/revised truths are 951/920. It succeeds on both inputs
of the other five worlds. Treating twelve related controls as twelve independent
capability worlds would overstate evidence.

The scalar legality gate correctly passes. It does not imply a low probability
of illegal collaborative actions. The all-legal scalar controls and frequently
illegal team actions occur under materially different prompts and action demands.
The two forced envelope length terminations are deliberate hardware diagnostics,
not truncated scientific responses. None of the 244 scientific replies is
truncated, framed incorrectly or marked with a provider failure.

### 4.2 Complete pilot evidence

| Pilot | Original truth → revised | Prefix submissions | Retain | Clear | Illegal calls, prefix/retain/clear | Controls |
|---|---|---|---|---|---|---|
| `pilot-00` | 988 → 932 | [988,923] | [988,null], horizon | [null,1023], deadlock | 0 / 1 / 1 | Both correct |
| `pilot-01` | 985 → 966 | [813,985] | [813,985] | [25,25] | 1 / 0 / 1 | Both correct |
| `pilot-02` | 981 → 911 | [981,911] | [981,981] | [847,974] | 3 / 0 / 0 | Both correct |

All three original teams and all six recoveries fail exact team success. All
six full-information pilot controls succeed. The first pilot's retained partner
repeatedly messages while leaving `submit:null`; its text says “Agent 1 submits
null,” which is not a final submission. The third pilot clear branch fabricates
974 from a shard containing −974 and calls the revision record `9` a partner
maximum. These are useful warnings about task interpretation beyond formatting.

All three pilot gates pass because the **adopted recorded-outcome policy**
requires terminal committed evidence, reconciled spending, runtime integrity
and inspectable checkpoints. Ordinary pilot wrong answers, illegal actions and
terminal noncompletion are diagnostic under that policy. Gate receipts openly
record four prefix and three recovery violations. Useful communication is `null`,
human review is `retrospective_pending`, and canonical annotations have zero rows.
Passing is therefore procedurally correct; calling it successful scientific
collaboration would be incorrect.

### 4.3 What changed across previous runs?

The relevant history is in the [course-3](i01-course-3-results-analysis.md),
[course-5](i01-course-5-results-analysis.md) and
[course-6](i01-course-6-results-analysis.md) records and the adopted §12 amendments.
The initial mathematical 11/12 screen was replaced with direct protocol-first
qualification; whole-study automatic admission followed; recovery violations
were then admitted as outcomes; finally ordinary sampled prefix/later-control
failures were also admitted. These decisions preceded this run's main outcomes
but followed observed qualification and development-pilot failures.

An independent comparison extracted old canonical stores into temporary
directories and matched exact requests and generated token IDs:

| Earlier run | Its calls | Logical calls also in course-7 | Exact request matches | Exact token-sequence matches among them |
|---|---:|---:|---:|---:|
| course-2 | 18 | 18 | 18 | 18 |
| course-3 | 23 | 18 | 18 | 18 |
| course-4 | 20 | 20 | 20 | 20 |
| course-5 | 32 | 32 | 32 | 32 |
| course-6 | 43 | 43 | 43 | 43 |

The five thinking calls in course-3 are absent from this direct run. These are
separate physical executions and charges, not cross-study response replay.
Their equality supplies some reproducibility evidence for the unchanged shared
requests. It does **not** create additional independent worlds, new seeds or
independent validation of pilot capability. In particular, course-7's first two
pilots did not improve on course-6. The broader admission rule enabled completion.

Repeated gate relaxation is transparent here and does not establish selective
main-world deletion: all twenty main worlds remain included. It does weaken any
claim that the final study was wholly prospectively specified before development
data, or that its admission process established a competent recovering team.
Future work should settle its scientific target before another gate change.

## 5. Independently reproduced main results

### 5.1 Primary paired result and population

| Retain success | Clear success | Worlds | IDs |
|---|---|---:|---|
| 0 | 0 | 17 | All except 03, 06, 12 |
| 0 | 1 | 1 | `main-03` |
| 1 | 0 | 1 | `main-06` |
| 1 | 1 | 1 | `main-12` |

With `D_w = success(clear,w) − success(retain,w)`, the twenty values contain one
`+1`, one `−1` and eighteen zeros. Thus `sum(D_w)/20 = 0`. All forty recovery
episodes are terminal; there are no missing primary outcomes. Missingness bounds
are `[0,0]`, which describe missing evidence, **not sampling uncertainty**.

The frozen analysis resamples whole worlds within the four five-world owner/
first-speaker strata, preserving siblings, 10,000 times with seed `2026101402`.
Independent reconstruction gives the saved 95% percentile interval `[−0.10,0.10]`.
This is an exploratory small-sample interval, not a guarantee of nominal coverage
in this sparse setting. Two strata have no observed nonzero contrast, so their
empirical resamples cannot represent unobserved discordance.

Supplemental checks, explicitly **not replacement primary analyses**, reinforce
the limited resolution. Conditional on the two discordant pairs, an exact
two-sided binomial/sign comparison gives `p=1` for one win in each direction.
Even two discordances favoring the same arm would give `p=0.5`. With twenty pairs,
the most favorable exact 5% two-sided discordance test first becomes possible
at six wins versus zero (`2/2^6 = 0.03125`), a 30-point difference. This is a
coarse design for detecting modest differences.

For scale, an ordinary exact binomial interval for one arm's 2/20 success is
approximately 1.23%–31.70%, under independent comparable-world assumptions. It
is not a paired treatment-effect interval and ignores the fixed-stratum design;
it must not replace the prespecified result. The numbers were calculated by
inverting binomial tails, not by fitting a model to the report.
[Exact binomial inference documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html).

### 5.2 Prefixes, controls and subgroups

| Scope | Prefix success | Retain success | Clear success |
|---|---:|---:|---:|
| All intended main worlds | 3/20 | 2/20 | 2/20 |
| Correct-prefix descriptive subset: 00, 03, 09 | 3/3 by definition | 0/3 | 1/3 |
| Other main prefixes | 0/17 | 2/17 | 1/17 |
| Owner 0 / first 0 | 2/5 | 0/5 | 1/5 |
| Owner 0 / first 1 | 1/5 | 1/5 | 0/5 |
| Owner 1 / first 0 | 0/5 | 1/5 | 1/5 |
| Owner 1 / first 1 | 0/5 | 0/5 | 0/5 |

The correct-prefix descriptive contrast is +1/3; its saved interval is
`[0,2/3]`. With three worlds in only two represented strata, that apparently
nonnegative interval is not persuasive evidence of a general clear advantage.
The prefix is shared and precedes treatment, but selecting its three successes
changes the target population. The primary denominator remains twenty.
Only `main-03` completes both original and revised tasks correctly under clear;
none does so under retain. The other recovery successes start from failed
prefixes. These facts limit the phrase “recovery of successful collaboration.”

Even the three correct prefixes provide unequal evidence of competent
coordination. In `main-00` and `main-09`, the first final submission occurs
without a received partner message; the other agent subsequently adopts the
correct winning value. `main-03` exchanges both local maxima before the first
final commitment. All three retain their exact success credit, but only the
latter visibly demonstrates that particular information-before-finality
strategy. Correct outcomes alone do not establish reliable global reasoning.

The main revised full-information controls succeed on 15/20. Errors are:

| Control call | Submission | Revised truth | Observable fact |
|---|---:|---:|---|
| `main-03/control-revised-direct` | 783 | 822 | Picks changed owner's local maximum |
| `main-07/control-revised-direct` | 890 | 880 | 890 is absent from revised input |
| `main-09/control-revised-direct` | 976 | 933 | 976 is absent from revised input |
| `main-10/control-revised-direct` | 94 | 918 | Picks a nonmaximum input value |
| `main-16/control-revised-direct` | 895 | 916 | Picks changed owner's local maximum |

These controls demonstrate imperfect scalar capability under the realized
configuration. Conversely, thirteen worlds with correct controls have neither
recovery succeeding. That is evidence that full-information success alone does
not ensure distributed success. It does not identify thirteen purely
communication-caused failures: the controls have different views, prompts and
seeds, and the distributed phases include multiple mechanisms. There is no
main original full-information control; original capability cannot be inferred
world-by-world from a nonexistent measurement.

### 5.3 Completion, consensus and individual accuracy

| Main metric | Prefix | Retain | Clear |
|---|---:|---:|---:|
| Exact team success | 3/20 | 2/20 | 2/20 |
| Both agents submitted | 11/20 | 20/20 | 19/20 |
| Waiting deadlock | 7 | 0 | 0 |
| Horizon exhaustion | 2 | 0 | 1 |
| Final submissions present | 24/40 | 40/40 | 39/40 |
| Correct individual submissions | 15/40 | 12/40 | 16/40 |
| Agreement on a submitted integer | 3/20 | 7/20 | 6/20 |
| Wrong agreement | 0/20 | 5/20 | 4/20 |

Individual denominators include the intended forty agent submissions; absent
submissions are not correct. Correctness is against the relevant global truth,
not the agent's local maximum. Individual outcomes and calls are not independent
replicates. Better completion/consensus under retain does not imply better
answers. Clear has four more correct agent submissions but no greater team
success because both agents must submit the exact answer in the same world.

## 6. Failure anatomy from the complete traces

### 6.1 Structural validity versus action legality

| Scientific scope | Calls | Valid JSON and field schema | Legal actions | Illegal actions | Episodes with an illegal action |
|---|---:|---:|---:|---:|---:|
| Qualification controls | 12 | 12 | 12 | 0 | 0 |
| Pilot prefix | 12 | 12 | 8 | 4 | 2/3 |
| Pilot retain | 9 | 9 | 8 | 1 | 1/3 |
| Pilot clear | 8 | 8 | 6 | 2 | 2/3 |
| Pilot controls | 6 | 6 | 6 | 0 | 0 |
| Main prefix | 82 | 82 | 40 | 42 | 15/20 |
| Main retain | 44 | 44 | 42 | 2 | 2/20 |
| Main clear | 51 | 51 | 42 | 9 | 6/20 |
| Main controls | 20 | 20 | 20 | 0 | 0 |
| **All scientific** | **244** | **244** | **184** | **60** | Different episode types; do not sum percentages |

The 206 team calls contain 146 legal actions (70.87%) and 60 illegal actions
(29.13%). Fifty-eight violations combine a nonempty message with `wait:true`;
two are empty nonwaiting actions, `message:null, submit:null, wait:false`.
The latter are `main-01/retain/agent-1/invocation-0` and
`main-05/clear/agent-1/invocation-1`. All are correctly rejected by the strict
validator. No rejected message was delivered. No scientific violation was caused
by reaching the 512-token output limit: maximum scientific output was 294 tokens.

Main-prefix illegality is 51.22% of calls, versus 4.55% retain and 17.65% clear.
These rates have endogenous denominators: waiting, submission and prior invalid
actions determine how many calls occur. They are not independent binomial
observations or controlled estimates of a protocol-training effect. Eighteen
retain episodes have no illegal action, yet only two succeed; fourteen clear
episodes have none, yet only one succeeds. Legality is necessary for actions to
take effect but does not resolve the study's broader failure.

### 6.2 Waiting and feedback loops

In `main-01/prefix`, agent 0 legally waits. Agent 1 then returns three illegal
message-plus-wait replies. Its first two texts correctly identify local maximum
910, but none reaches the partner. Agent 0 remains asleep; the episode stops
with `[null,null]` after four calls and zero delivered messages. This is an
observable pathway from invalid coordination actions to noncompletion.

`main-04`, `main-05` and `main-07` show similar patterns. `main-02` ultimately
has both agents waiting after unsuccessful attempts to communicate. By contrast,
`main-06` and `main-12` deadlock after two **legal** wait-only actions. Thus
action illegality is neither a necessary nor a sufficient explanation for every
deadlock. The host correctly terminates an episode with no possible wake-up.

Across main-prefix per-agent sequences, there are 21 adjacent pairs of invalid
actions. Generic feedback says only “Previous action invalid; no action
delivered.” The system prompt already states the wait rule. Repetition despite
feedback is observed; the hypothesis that more specific feedback would fix it
requires a prospective comparison. It would also change future model behavior.

### 6.3 Finality and failure to aggregate

All 124 legal main team actions break down as 85 message-and-submit, 18
submit-only, 15 wait-only and just six message-only. A message saying “I propose”
does not make an accompanying integer submission provisional.

In `main-10/prefix/agent-0/invocation-0`, agent 0 submits local maximum 758 while
asking the partner to send a larger value “so we can adjust.” Adjustment is
impossible after finality. Agent 1 later correctly submits 937; the team fails.
In `main-11/prefix/agent-0/invocation-1`, the visible message reports 972, but
agent 0 submits its own 757 anyway. In `main-04/retain/agent-0/invocation-1`,
the response explicitly recognizes 959 as the global maximum and submits 943
to “complete my turn.” This is direct evidence that correct comparative text
does not guarantee a correct final action.

The first recovery call already submits in 18/20 retain and 14/20 clear worlds,
versus 3/20 prefixes. At submission time, no received message exists anywhere in
the visible history for 13/24 prefix, 12/40 retain and 21/39 clear submissions.
The retain count includes old history; these counts use a deliberately simple
presence-of-message criterion, not an annotation of whether information was
sufficient. They show frequent commitment without explicit partner evidence.
A correct first commitment may still be a lucky local maximum, not a justified
global computation.

### 6.4 Stale results and literal repetition

Retain submits the old global maximum **14 times across ten main worlds**:
00, 03, 08, 09, 10, 11, 13, 15, 17 and 18. Four have both agents doing so;
six have one. The three correct prefixes all lose their original correctness
after revision under retain. The exact original submission pair is reproduced
in nine worlds: 00, 03, 08, 09, 11, 13, 15, 17, 18.

Thirteen retained final actions are exactly equal as parsed JSON to an earlier
own prefix action. This includes correct unchanged-side responses and wrong
ones; repetition itself is not a failure label. In `main-11/retain/agent-1/
invocation-0`, a new first invocation repeats text claiming “3/3 invocations.”
In `main-03`, both agents repeat 993 although current truth is 822. These
examples support an observable description of stale-result persistence and
historical text repetition. They do not reveal the model's internal reasoning.

Clear never submits the old maximum. Since that value was unique, withdrawn
from current shards and absent from its history, this is partly an information
availability contrast by construction. An old-value metric should accompany
accuracy, not serve as a substitute for successful correction.

### 6.5 Revision notices mistaken for communications or answers

Several especially strong examples occur on the **first clear call**, with
empty history and `partner_finished:false`. No partner action can explain them:

| Call | Notice actually visible | Response behavior |
|---|---|---|
| `main-08/clear/agent-1/invocation-0` | Owner 0, record 2; no new value | Says “Partner submitted 2” |
| `main-09/clear/agent-1/invocation-0` | Owner 0, record 5 | Calls partner's shard maximum 5; submits 97 rather than local 933 |
| `main-12/clear/agent-0/invocation-0` | Owner 1, record 2 | Says “Partner submitted 2”; nevertheless submits correct local/global 983 |
| `main-14/clear/agent-0/invocation-0` | Owner 1, record 2 | Interprets partner as having “2 records” |
| `main-15/clear/agent-1/invocation-0` | Owner 1, record 12, new value −614 | Says partner submitted −614; it is the agent's own corrected record |
| `main-18/clear/agent-1/invocation-0` | Owner 1, record 15, new value 333 | Calls 333 the shard/global maximum although its shard contains 827 |

The permitted-view reconstruction rules out host leakage of partner submissions
in these calls. It does not establish a single cognitive cause. The notice's
placement, numeric fields, task framing and learned expectations about dialogue
are plausible contributing factors. Misinterpretations can also propagate:
`main-04/clear` reaches false consensus 629 after the owner labels the replacement
its maximum; `pilot-01/clear` reaches `[25,25]` similarly.

Replacement-value submissions occur twice under main retain and eight times
under clear (in six clear worlds). Every such value is guaranteed wrong by the
world construction. The host must not tell peers this hidden eligibility rule
or suppress those submissions; the audit can use it to diagnose the behavior.

### 6.6 Locally refutable values, invented values and message quality

Six retain submissions and eleven clear submissions are strictly below a larger
value in the submitting agent's **current own shard**. No unavailable partner
information is required to refute those answers. This supports a combined
local-computation/source-use problem, without identifying whether the response
came from scanning failure, imitation, notice confusion or another mechanism.
None of the 24 recorded prefix submissions is below its own original local
maximum; many prefix failures instead concern noncompletion or failure to agree.

`main-02`'s second recovery agent copies the first agent's entire shard prose and
submits 830 even though its own shard contains 914; both policies fail this way.
`main-14` repeats 461 despite own 712. `main-09` misidentifies 97 as local maximum
despite 933. These examples are stronger evidence than a broad “reasoning error”
label because their contradiction is visible inside the call's permitted input.

Other false claims include 21 integers in actual twenty-integer shards, “Agent 2”
in a zero-indexed two-agent task, index errors, and claims to see a partner shard.
These claims were not supplied by the host. A response's message can also
contradict its submission, as `main-04/retain` does. Fluent, lengthy messages,
numeric mentions and eventual consensus are weak proxies for coordination quality.

### 6.7 Contrasting successful cases and why they do not settle mechanisms

**Clear-only: `main-03`.** Prefix agents legally exchange maxima 993 and 822 and
both submit 993. Revised owner 0 now has maximum 783; partner still has 822.
Retain immediately repeats 993 twice. Clear's first action correctly identifies
783 but combines it with wait and is rejected. Agent 1 then sends a legal
message containing its actual 822; agent 0 adopts 822, and agent 1 agrees.
Clear succeeds despite an illegal action and inaccurate explanatory language.
Its full-information control fails with 783. This is a useful example of a clear
recovery success, not proof that all its intermediate reasoning was sound.

**Retain-only: `main-06`.** The prefix is two legal waits, with no exchanged
maximum and no old submission. In retain, first speaker agent 1 correctly
messages/submits 926; agent 0 then adopts it. The first message incorrectly says
the partner's shard also has 926, but its own shard really does. Clear's initial
agent-1 message-plus-wait is rejected; agent 0 privately submits 905, and agent 1
later submits 926. This is not evidence that retained *computed results* helped:
the prefix retained only waiting actions. Retained dialogue cues or stochastic
prompt differences are possible explanations; the trace does not distinguish them.

**Both: `main-12`.** Again the prefix contains only two legal waits. Both policies
produce `[983,983]` in two calls. Both first responses falsely call record ID 2
a partner submission, and both second responses repeat “my shard max is 983,”
although agent 1's actual local maximum is 548. The final global answer is correct
through message adoption, not uniformly correct provenance statements.

Success must remain the exact prespecified scalar score. These observations do
not justify downgrading successful answers after the fact. They do justify
separating answer correctness from an interpretation of reliable reasoning.

### 6.8 How to read the saved failure taxonomy

Saved episode-level labels count 60 `wrong_submission`, 28 `malformed_action`,
13 `obsolete_value_repeated`, eight `waiting_deadlock`, and four
`horizon_exhausted` across **all scientific scopes**, including controls/pilots.
Labels overlap; they are not an exclusive partition or main-only rates.

In particular, 28 episodes with malformed actions contain 60 invalid team calls.
The coarse label does not mean broken JSON: all 244 scientific outputs parse
and have the required field types. `validation_details.csv` supplies the exact
legality reasons. The frozen rubric also names `premature_finalization` and
`ambiguous`, but the automatic report does not supply a systematic human-coded
count for them. Zero annotation rows cannot be read as zero occurrences.
This audit's descriptive examples do not retroactively populate that database.

## 7. Effort, accounting and engineering reliability

### 7.1 Paired recovery effort

| Main total / mean | Prefix | Retain | Clear |
|---|---:|---:|---:|
| Calls | 82 / 4.10 | 44 / 2.20 | 51 / 2.55 |
| Input tokens | 29,609 / 1,480.45 | 20,319 / 1,015.95 | 20,350 / 1,017.50 |
| Generated tokens | 5,246 / 262.30 | 2,434 / 121.70 | 4,077 / 203.85 |
| Legal messages | 21 / 1.05 | 33 / 1.65 | 37 / 1.85 |
| Ready-model seconds | 648.145 / 32.407 | 314.664 / 15.733 | 497.803 / 24.890 |
| Median world seconds | 34.265 | 11.152 | 18.701 |

The mean paired clear-minus-retain effort is **9.156966 seconds**, with the
independently reproduced frozen bootstrap interval **[1.964391,17.123815]**.
Clear is slower in fifteen worlds, faster in five; the median paired difference
is 2.742 seconds. Deleting any one world leaves the mean difference positive
(range 6.896–11.078 seconds). This last check is descriptive sensitivity, not a
second prespecified test.

Retain inputs are longer per call (461.8 versus 399.0 tokens), but clear makes
more calls and generates 67.5% more output tokens. Total recovery input tokens
are almost equal. Much of the observed effort contrast is consistent with
different stopping and verbosity. The adapter's `ready_seconds` measures the
generation interval plus its memory-observer lifecycle and synchronized work;
it is not a direct hardware-utilization measurement or purely kernel time.

Retain uses approximately 36.8% less total recovery ready time in this sample,
while both succeed only twice. Cost per observed success, if presented alone,
would conceal seventeen double failures and different successful worlds.
Neither output-per-second nor mean time establishes useful work quality.
Report success and effort jointly, retaining failed worlds' full effort.

Prefix calls are physically executed once. Hypothetical end-to-end policy costs
charge that prefix to each policy: 126 calls for retain and 133 for clear across
main, versus 177 physical main team calls. The twenty main controls are diagnostic
physical cost, not part of either hypothetical distributed policy. The shared
prefix cancels in the paired recovery contrast; charging it twice physically
would be wrong.

### 7.2 Attempts and resources

| Stage | Actual attempts | Relevant interpretation |
|---|---:|---|
| Hardware/state | 8 | Six short checks plus two forced full envelopes |
| Direct qualification | 12 | No thinking calls in this study |
| Pilots | 35 | 29 team calls + six controls |
| Main | 197 | 177 team calls + twenty controls |
| **Total** | **252** | All first attempts; no contingency or retry |

The 500 ceiling is respected. The direct schedule's 460 first-attempt upper
bound is not an obligation to spend: early finality/deadlock leaves 208 potential
ordinary calls unused. A displayed remaining hard allowance of 248 does not
authorize new worlds or another sample; the stage/reserve and scientific scope
still apply. Historical executions remain separately identified and were not
imported as current outcomes or erased.

All attempts have known ready time and token counts. Total physical ready time
is 1,943.106 seconds, dispatch time 1,944.281 seconds, and generated tokens 15,472.
Observed loads total 119.029 seconds; setup reports 228.421 seconds. These sums
can overlap between devices and with notebook intervals; adding them to wall
time would double-count. No precise GPU utilization, billed GPU-hours, energy,
monetary cost or provider assignment/release interval is supplied.

Minimum recorded conservative free headroom is approximately 6.776 GiB, above
the required 1.5 GiB. Maximum scientific prompt is 783 tokens, far below 8,192.
There is no evidence of input truncation or insufficient context. The envelope
probes exercise the full reserve independently of the short scientific requests.
No inference timeout, OOM, nonfinite-score or provider-failure outcome appears.

Logs contain Transformers output-docstring `[ERROR]` messages, missing recurrent
fast-path warnings and bitsandbytes future warnings. The run nevertheless loads
and finishes all calls with finite/cache evidence. These warnings do not establish
a causal explanation for wrong maxima. Conversely, successful completion and
finite scores do not independently prove numerical equivalence to another backend.

### 7.3 Persistence, privacy and isolation assessment

Source inspection and replay agree on register/admit before dispatch, raw outcome
persistence before effects, atomic state/effect commit and exact raw reuse on
resume. SQLite uses WAL/FULL during execution and backup snapshots in the archive.
The final stores contain no admitted unresolved attempts. Siblings start from
deep-copied terminal prefixes with independent state. Seeds are assigned by
world/phase/agent/invocation, not arrival order. Matched seeds are a coupling
choice, not proof of identical randomness under different prompts.

All persisted scientific requests expose only the permitted current shard,
literal history, invocation, partner-finished flag and allowed notice fields.
No evaluator truth, hidden partner shard, future edit or condition label was found.
Fabricated claims of seeing private information are model text, contradicted by
the actual view. No invalid message leakage or host correction of model answers
was found. All saved final states reproduce independently.

Both model workers have confirmed exit code −15 at deliberate controller closure,
after scientific calls finish. This is consistent with requested termination,
not a mid-run crash. The final archive is written afterward. Provider release,
survival of an arbitrary hard kill and successful restore on a different GPU
session are separate claims. This completed run does not empirically demonstrate
every crash-resume path previously tested on scripted data.

## 8. Scientific validity and competing explanations

### 8.1 What the paired design identifies

Each world shares one realized prefix, current edited input, order and per-agent
invocation seed schedule. Both treatments are executed on the same logical
device. This is a strong control for original world difficulty and realized
prefix history. Within the cohort, it observes both policy outcomes rather than
imputing an unobserved sibling. No successful-world selection or missing-main
imputation is needed.

The treatment is the **whole visible-history policy**. Retain keeps source claims,
wrong and right submissions, communicative conventions, action examples and
feedback; clear removes all of them. Prompt length, information content and
behavioral cues therefore move together. Their downstream effects on protocol
legality and call counts are part of the practical treatment, not nuisance
variables to remove by restricting analysis to compliant calls.

The estimand is adaptation after a deliberately outcome-changing maximum
withdrawal in this specific error-prone system. There is no no-revision/sham
control, so a revision-specific effect cannot be separated from a generic
benefit or cost of erasing history. There is no selective fact/conclusion
retention arm, so information loss cannot be separated from removal of bad
answers. The current contract correctly does not license those stronger claims.

### 8.2 Randomization and order limits

Worlds and call seeds are deterministically generated from a frozen master seed;
owner/first-speaker cells are balanced. Balance is not independent randomization
of every execution factor. `device=index%2` and treatment order is retain-first
for even indices, clear-first for odd indices. Consequently:

| Logical slot | Main worlds | Physical sibling order |
|---|---:|---|
| 0 | 10 | Always retain then clear |
| 1 | 10 | Always clear then retain |

Both policies run on each slot, so a simple constant device speed difference
does not automatically confound every paired contrast. However, a device-specific
order effect, allocator/warm-up effect or temporal load interaction cannot be
estimated separately. Within each five-world owner/first block, order splits
3/2 or 2/3; blocks also run in index order. Stateful caches are explicitly reset
and A/B/A probes agree, reducing one concern, but they do not prove the absence
of all order effects. This limitation is especially relevant to timing and
cross-device numerical reproducibility. It is not evidence that the observed
success difference would become nonzero after counterbalancing.

### 8.3 Task suitability and research contribution

Global maximum is a good debugging task: exact truth is trivial to verify,
communication requirements are small, wrong provenance can be inspected, and
revision cannot leave the old answer accidentally correct. Its low mathematical
complexity makes the observed coordination failures informative about this
system's practical usability.

It is a limited test of the benefits of retaining expensive distributed work.
Recomputing one local maximum and exchanging two scalars is cheap. The design
forces removal of the winning value in every world and has no harmless revision
or preserved-answer comparison. It intentionally concentrates exposure to a
stale winner while providing little reusable computation whose preservation
could be valuable. This can support an exploratory policy case study; it cannot
support a general recommendation about memory resets in substantial research,
coding or distributed reasoning workflows.

At present, the strongest contribution is a traceable example of **multiple
failure layers interacting with a history intervention**: formatting can pass
while actions fail; local computation can be right while finalization is wrong;
old-answer repetition can disappear while exact team accuracy remains low.
This is more defensible than presenting a null 20-world effect as a general
finding about forgetting.

### 8.4 Causal hypotheses and current confidence

| Hypothesis | Supporting evidence | What remains unresolved |
|---|---|---|
| Mutually exclusive wait/message fields are poorly elicited | 58 exact violations, repeated feedback loops, no JSON syntax failures | Relative benefit of clarification, alternative actions or constrained generation |
| Private finality is misunderstood or poorly planned around | Explicit “adjust” after submitting; own-local submissions despite larger received value | Whether wording, task understanding, generation policy or deeper reasoning dominates |
| Retained text competes with current source use | Old answers, exact action repetitions, stale invocation wording | Internal anchoring, imitation and other prompt effects are not separately identified |
| Revision metadata is treated as a conversational answer | First clear calls claim partner submissions matching notice fields | Which presentation change helps, and whether it transfers to unseen cases |
| Scalar competence contributes to failures | Seven wrong controls; locally refutable recovery answers | Quantization, direct mode, scanning, prompt load and stochastic error are not separated |
| Numerical/runtime corruption caused the main failure | No direct supporting failure record; finite scores, source binding, state checks pass | Independent numerical reference comparison remains absent |
| More turns would solve it | Some horizons exhaust | Many episodes finalize immediately or legally deadlock; extra budget alone need not help |

These hypotheses are not mutually exclusive. Their frequencies cannot be added
into a causal percentage decomposition. The audit establishes visible actions
and contradictions, not private chains of reasoning.

## 9. Defects, limitations and conclusions a reviewer can defend

### 9.1 Engineering findings versus design choices

No verified defect in the scorer, effect application, delivery, sibling starts,
source binding or current run accounting was found. Poor performance is not
grounds to call the correct rejection of an illegal action a parser bug.

Verified limitations are narrower: coarse failure nomenclature, no independent
systematic mechanism annotation, perfect device/order coupling, and ambiguity
between balanced owner conditioning and the prose restriction on rejections.
The narrow scalar qualification and later gate relaxations are adopted design
choices whose scientific consequences need disclosure. They are not unapproved
deviations in this execution. Numerical equivalence and off-session GPU restore
remain unverified, rather than established defects.

The earlier [report-ready course-7 analysis](i01-course-7-results-analysis.md)
gets the main counts, scoring and costs right. This audit adds explicit emphasis
on information availability in the old-value contrast, exact historical
re-execution equality, private-finality evidence, correct answers with unreliable
provenance, action-only repeated-output counts and the device/order alias.
Descriptions such as “clear failed because other errors remained” should be
read as a trace-supported account of observed errors, not an identified causal
mediation analysis.

### 9.2 Supported and unsupported claims

| Supported by this execution | Unsupported stronger interpretation |
|---|---|
| Twenty intended main pairs completed with reconciled records | A reliably collaborating system was qualified |
| Both policies achieved 10% exact team success in this cohort | Retain and clear are equivalent in a wider population |
| Retain repeated an obsolete answer in ten worlds | A pure internal anchoring mechanism was identified |
| Clear had no obsolete-answer submissions | Clear reliably understood and applied corrections |
| Retain used less recorded recovery ready time | Retain performed more useful reasoning or minimizes time to a correct answer |
| Protocol, finality, provenance and scalar errors coexist | A unique cause or numerical attribution of failures is established |
| Some shared requests reproduce identical token sequences across runs | Earlier studies supply independent replication samples |
| Source/checkpoint/replay checks agree | Every numerical kernel or possible crash/restore path is independently validated |

Course-7 is usable exploratory evidence with unusually good raw traceability.
For a thesis, it can support a bounded methodological case study and motivate a
more discriminating next experiment. For a strong general scientific claim,
the current number of informative pairs, baseline competence, intervention
specificity and replication breadth are insufficient. Preserving the negative
and limited outcomes is scientifically preferable to retrospectively repairing
them or relabeling them as a successful recovery benchmark.

## Appendix A. Complete main evidence matrix

Pairs are `[agent 0,agent 1]`; `null` means no submission in a known terminal
episode, not an unknown outcome. `D` = waiting deadlock, `H` = horizon exhaustion;
otherwise the episode ends with both submitted. `P/R/C illegal` are call counts.
Local maxima are from the **revised** shards. The last column is the revised
full-information control submission, not its truth.

| World | Owner/first | Old → new truth | Revised local maxima | Prefix | Retain | Clear | P/R/C illegal | Control |
|---|---|---|---|---|---|---|---|---:|
| 00 | 0/0 | 894 → 872 | [753,872] | [894,894] | [894,894] | [753,872] | 2/0/0 | 872 |
| 01 | 0/0 | 936 → 910 | [723,910] | [null,null] D | [-152,-992] | [723,910] | 3/1/0 | 910 |
| 02 | 0/0 | 957 → 914 | [830,914] | [null,null] D | [830,830] | [830,830] | 2/0/0 | 914 |
| 03 | 0/0 | 993 → 822 | [783,822] | [993,993] | [993,993] | [822,822] | 0/0/1 | 783 |
| 04 | 0/0 | 994 → 959 | [943,959] | [null,null] D | [943,959] | [629,629] | 3/1/0 | 959 |
| 05 | 0/1 | 949 → 915 | [915,870] | [null,null] D | [915,870] | [915,null] H | 3/0/1 | 915 |
| 06 | 0/1 | 977 → 926 | [905,926] | [null,null] D | [926,926] | [905,926] | 0/0/1 | 926 |
| 07 | 0/1 | 917 → 880 | [759,880] | [null,null] D | [-721,669] | [-721,669] | 3/0/0 | 890 |
| 08 | 0/1 | 965 → 960 | [960,928] | [965,928] | [965,928] | [948,928] | 1/0/0 | 960 |
| 09 | 0/1 | 999 → 933 | [916,933] | [999,999] | [999,999] | [97,97] | 3/0/0 | 976 |
| 10 | 1/0 | 937 → 918 | [758,918] | [758,937] | [937,937] | [867,867] | 1/0/2 | 94 |
| 11 | 1/0 | 972 → 963 | [757,963] | [757,972] | [757,972] | [757,963] | 2/0/0 | 963 |
| 12 | 1/0 | 997 → 983 | [983,548] | [null,null] D | [983,983] | [983,983] | 0/0/0 | 983 |
| 13 | 1/0 | 982 → 953 | [737,953] | [737,982] | [737,982] | [737,953] | 0/0/0 | 953 |
| 14 | 1/0 | 984 → 730 | [712,730] | [null,984] H | [461,730] | [461,730] | 4/0/1 | 730 |
| 15 | 1/1 | 967 → 959 | [959,947] | [959,967] | [959,967] | [959,947] | 4/0/0 | 959 |
| 16 | 1/1 | 919 → 916 | [916,895] | [916,919] | [916,895] | [916,895] | 0/0/0 | 895 |
| 17 | 1/1 | 885 → 878 | [878,774] | [878,885] | [878,885] | [878,774] | 2/0/0 | 878 |
| 18 | 1/1 | 908 → 848 | [848,827] | [848,908] | [848,908] | [848,333] | 4/0/0 | 848 |
| 19 | 1/1 | 951 → 944 | [944,875] | [944,null] H | [944,875] | [944,875] | 5/0/3 | 944 |

Six sibling pairs have identical final submissions: 02, 07, 12, 14, 16, 19.
Equal final values are not cross-treatment replay; requests and continuation
records are independent, with matched seed schedules as specified.

## Appendix B. Reproduction and trace navigation

The existing full audit can be rerun without model dependencies or inference:

```powershell
python scripts/audit_i01_course7.py --output "$env:TEMP/course7-readonly-review"
```

Use `mode=ro` SQLite URI connections when inspecting originals. For example,
this returns a complete call without opening a writable store:

```python
from pathlib import Path
import json, sqlite3
p = Path("notebooks/run/course-7-working/latest/worker-0.sqlite").resolve()
with sqlite3.connect(p.as_uri() + "?mode=ro", uri=True) as db:
    request, outcome = db.execute(
        "SELECT request,outcome FROM calls WHERE id=?",
        ("main-04/retain/agent-0/invocation-1",)
    ).fetchone()
    print(json.loads(request)["view"])
    print(json.loads(outcome)["visible_text"])
```

World slot is saved in `run.json` (`main index % 2` here). Invocation IDs are
zero-based, whereas the visible invocation field is one-based. All specific
call references in this document use canonical IDs. The independent calculation
recipe is:

1. Merge `calls`, `attempts`, `episodes` from exactly two canonical stores;
   require unique call IDs and one completed attempt/outcome per call.
2. Compute truth directly with `max` over saved shards. Score only terminal
   team states as `submissions == [truth,truth]`.
3. Parse each raw scientific reply. Check exact keys/types and mutually exclusive
   waiting; reject provider/framing/truncation failures. Reconstruct deliveries,
   waiting, eligible turns, submissions and final histories from those replies.
4. Sum **attempt** effort within world/phase; count messages only for legal
   delivered actions. Derive paired differences before aggregation.
5. Group main worlds by `(owner,first)`. For each of 10,000 draws, sample five
   worlds with replacement within each group using `random.Random(2026101402)`;
   average their paired differences. Read sorted indices 250 and 9750, matching
   the frozen percentile convention. For the correct-prefix subset preserve its
   realized within-stratum counts, two and one.
6. Compare derived results to saved reports, never overwrite the originals.

Preserved primary evidence includes [complete conversations](../../notebooks/run/course-7-working/latest/reports/conversations.txt),
[machine-readable conversations](../../notebooks/run/course-7-working/latest/reports/conversations.jsonl),
[per-call validation](../../notebooks/run/course-7-working/latest/reports/validation_details.csv),
[failure references](../../notebooks/run/course-7-working/latest/reports/failure_analysis.csv),
[attempts](../../notebooks/run/course-7-working/latest/reports/attempts.csv),
[paired costs](../../notebooks/run/course-7-working/latest/reports/paired_costs.csv),
[source release](../../notebooks/run/course-7-working/latest/source/source-release.json),
and [controller log](../../notebooks/run/course-7-working/latest/receipts/controller-stderr.log).
These are navigation aids; the SQLite/raw-source checks above establish their
agreement. This review adds no retrospective gate waiver, no new scientific
outcome and no claim of independent human coding reliability.
