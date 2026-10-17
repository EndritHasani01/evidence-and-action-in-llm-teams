# I-01 course-3: thinking results and direct-mode comparison

15 October 2026. Audit of the supplied [course-3 artifacts](../../notebooks/run/course-3/),
with [course-2](../../notebooks/run/course-2/) as the earlier comparison. No model
was run during this analysis. The companion
[solution proposal](../proposals/i01-course-3-direct-mode-solution.md) recommends
a direct-mode research path and specifies the required scientific amendment,
software repairs and spending reconciliation. It is not implemented here.

## 1. Finding

**Direct/nonthinking is the better practical choice for this bounded course
study on the supplied evidence.** Thinking generated much more output, consumed
about seventeen ready-model minutes for five short controls, and stopped on a
4,096-token unfinished reply. It demonstrated no improvement on the cases where
direct had made its two errors, because those thinking cases never ran.

This supports a resource decision, not a claim that thinking is inherently less
accurate. The completed thinking answers are all correct, but they concern four
cases direct already answered correctly. One additional attempted case has no
valid final action; seven planned thinking cases remain unexecuted.

| Observation | Direct | Thinking |
|---|---:|---:|
| Planned qualification controls | 12 | 12 |
| Recorded controls | 12 | 5 |
| Valid final scalar actions | 12 | 4 |
| Correct delivered answers | 10 | 4 |
| Incorrect delivered scalars | 2 | 0 |
| Invalid/truncated final actions | 0 | 1 |
| Unexecuted controls | 0 | 7 |
| Generated tokens in recorded controls | 193 | 10,250 |
| Ready-model seconds in recorded controls | 26.328 | 1,022.044 |
| Median recorded control seconds | 2.161 | 177.085 |

The mode totals cover different numbers/cases and cannot establish an accuracy
ranking. On the **same five attempted inputs**, direct takes **11.215 seconds
and 81 generated tokens**, versus thinking's **1,022.044 seconds and 10,250
tokens**: **91.13 times the ready-model time and 126.54 times the tokens**.
Both costs include the fifth thinking attempt that produced no usable final.

## 2. Authority, source and evidence integrity

[PROJECT_SPECIFICATION.md §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
still requires at least 11/12 correct controls, zero protocol defects and later
pilot accuracy gates. The user's preference and
[verbatim protocol-first evaluation](../proposals/i01-protocol-first-qualification-evaluation.md)
have not changed those rules. The earlier
[course-2 analysis](i01-course-2-results-analysis.md) and
[fix proposal](../proposals/i01-course-2-fix-proposal.md) remain historical records.

Reviewed checkout is `E:\Github\recovery_blueprint\recovery_blueprint`, branch
`feat/smaller-natural-experiment`, starting at `e5b0a40`. Course-3 uses source
`8f5bcdb661a177ebf7e0ca320889612ba448c64b`. Its preserved Python modules match
the current production modules; the earlier proposed fixes are still unapplied.

| Supplied course-3 file | Bytes | SHA256 |
|---|---:|---|
| [Executed notebook](../../notebooks/run/course-3/multi-agents-course-v1nb.ipynb) | 1,142,170 | `a8f5166ef487af3d49647233962389f734cdde304e08f5909b6e0e349c3163f5` |
| [latest.zip](../../notebooks/run/course-3/latest.zip) | 1,553,567 | `7524c6a553a76ab2dd218fbeb45a5160db7de9b5661c1da395fa11d03168e739` |

The ZIP has **123 members**, 7,837,274 uncompressed bytes and **122 integrity
entries**. CRC, all inventory bytes/hashes, both SQLite integrity checks, all
67 source-release entries and 44 wheel/source Python-module comparisons pass.
Fresh read-only reconstruction exactly equals archived `reports/analysis.json`.
The previous course-2 archive independently passes the same reconstruction.

The final archived boundary is `operator-error-screen`, created at
**2026-10-15 11:17:15.109484 UTC**, or 13:17:15.109484 Budapest time. It includes
all 23 recorded calls, raw output before committed control effects, setup/load
evidence, full traces, reports, figures and the thinking-stage traceback.

The notebook has 54 cells and 26 code cells; twelve saved code cells executed.
Only the session-window and thinking-screen source cells differ from the shipped
notebook. The former sets 700 minutes with evidence text asserting twelve hours;
the latter supplies the documented direct-competence limitation. Other scientific
stage code and settings match the shipped source.

Reproducible metrics, input hashes, stage times and matched comparisons are in
[course-3-audit.json](course-3-audit.json). The
[audit script](../../scripts/audit_i01_course3.py) extracts only temporary copies,
opens evidence read-only and performs zero inference.

## 3. Course-3 is a fresh study, not a continuation of course-2

| Identity | Course-2 | Course-3 |
|---|---|---|
| Study ID | `c2973855-84fa-411d-9f6c-a08f8acc79d6` | `de1b347e-2cb7-41e5-a8b9-2789abda2da3` |
| Manifest created UTC | 09:44:11.698941 | 10:54:05.586952 |
| Saved physical attempts | 18 | 23 |
| Readiness/direct attempts | 6 + 12 | 6 + 12 |
| Thinking attempts | 0 | 5 |

Both studies have identical world arrays, schedules, configuration, request IDs
and seeds for the common eighteen calls. Their saved requests and output token
sequences match exactly on all eighteen common IDs. However, the course-3 calls
have new admissions, timings, worker PIDs and physical GPU UUIDs. They are new
recorded physical executions, not zero-call replay from the earlier checkpoint.

There are therefore **41 recorded I-01 physical attempts across these two
studies**, and 23 distinct logical call IDs across their union. Do not deduplicate
physical spending because prompts, seeds or outputs match. Do not pool repeated
direct cases as twenty-four independent qualification instances. They are the
same twelve input cases executed twice under the same saved seeds.

The per-study course-3 ledger reports 23/500, zero contingency and 477 remaining.
It does not import course-2's eighteen attempts. If the intended 500 ceiling
covers the overall I-01 research campaign, the known arithmetic allowance is
instead **459 before any other missing spending is reconciled**. The historical
45 remain a separate earlier-regime category. Budget scope and repeated-stage
spending need explicit reconciliation; the current interface does not enforce a
campaign cap merely by giving every fresh study its own 500 allowance.

## 4. Every executed stage and its timing

Times use saved notebook busy/idle metadata in UTC. Budapest is UTC+2 on this
date. The cell wall includes Python, display, dispatch and export overhead; the
ready-model measure isolates the recorded model-call effort.

| Saved cell | UTC start → end | Wall seconds | Outcome |
|---|---|---:|---|
| Workspace | 10:51:23 → 10:51:23 | 0.755 | Matching source, fresh destination and two T4s observed |
| Setup | 10:51:23 → 10:54:05 | 161.583 | Pinned runtime/metadata accepted; internal setup receipt is 158.547 s |
| Open study | 10:54:05 → 10:54:08 | 2.512 | New study and fresh canonical files |
| Self-check | 10:54:08 → 10:54:17 | 9.785 | Native/tokenizer and scripted checks pass |
| Weights | 10:54:17 → 10:56:57 | 159.996 | Pinned native files verified and checkpointed |
| Session window | 10:56:57 → 10:56:59 | 1.833 | Fixed 700-minute bound recorded |
| Load workers | 10:56:59 → 10:58:44 | 104.759 | Both T4 replicas load |
| Readiness | 10:58:44 → 10:59:00 | 16.100 | Six A/B/A diagnostics pass |
| Direct qualification | 10:59:00 → 10:59:31 | 31.005 | 10/12 correct, zero protocol errors; stopped cell |
| Inspect qualification | 10:59:41 → 10:59:41 | 0.119 | Existing evidence only |
| Thinking qualification | 11:00:05 → 11:17:15 | 1,029.954 | Five attempts, then truncation/framing stop |
| Selected headroom request | 11:28:50 → 11:28:50 | 0.040 | Refused before generation: no passing competence screen |

The thinking cell took **17 minutes 9.954 seconds**; its model calls account
for **17 minutes 2.044 seconds**. The remaining approximately 7.910 seconds cover
dispatch, checks, reporting and checkpoint overhead. Removing notebook rendering
or checkpoints would not eliminate the dominant delay.

The whole saved span through the later headroom refusal is 37 minutes 26.835
seconds. It contains an approximately 11 minute 34.5 second gap after thinking
stops. No additional call from that gap appears in the saved evidence. It is not
another seventeen minutes of active inference, nor a provider billing record.

## 5. Preparation, placement, state and source acceptance

The runtime remains pinned Qwen3.5-9B, NF4 double quantization/FP16, Torch
`2.11.0+cu128`, Transformers `5.12.0`, bitsandbytes `0.49.2`, and the reviewed
T4 attention. Source-labelled interpreter isolation remains accepted. The
controller log has no missing-wrapt/sitecustomize startup failure and no OOM.

Physical GPUs differ from course-2:

- Slot 0: UUID `f65bed71-9416-2d2e-4822-91cadc4b9a5b`, PID 362, load 68.565 s.
- Slot 1: UUID `dc71ae04-5d53-bb13-42f7-3cf8c07f8a36`, PID 377, load 33.297 s.

Successful loads total 101.862 seconds. Each child exposes its selected physical
device as logical `cuda:0`; this is expected and does not mean both replicas are
on the same GPU. Both retain `recurrent_fast_path=false`, using the existing
Torch recurrent path. The matching
[Transformers source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py#L386)
explains the optional-kernel fallback. Its performance contribution is not isolated
by this run; installing another kernel would be a separate runtime change.

The same four documentation `[ERROR]` lines, two fallback warnings and four
bitsandbytes future warnings recur. They are followed by successful loading and
23 saved raw outcomes. The actual fatal stage message is the application's
`control provider/framing defect recorded`, with its stack saved separately in
`receipts/stage-error.json`.

All six readiness probes again answer `3`, `100`, `3` by slot, with matching
A1/A2 token sequences. They consume 88 tokens and 13.962 ready-model seconds.
All 23 outcomes, including the long capped output, have finite-score steps,
matching request/CPU/CUDA seeds and fresh call-owned cache evidence. No hidden
extra warmup, recorded retry or unresolved dispatch appears in these ledgers.

The recorded deadline is 22:36:57.871771 UTC on 15 October. Its 700-minute bound
is shorter than the twelve-hour evidence text, as in course-2. The failed thinking
call stopped after about 405 seconds, well below its **900-second timeout** and
before the session deadline. Deadline exhaustion did not cause this failure.

## 6. Direct results reproduced

| World | Original truth → direct answer | Revised truth → direct answer | Correct |
|---|---|---|---:|
| qualification-00 | 950 → 950 | 921 → 921 | 2/2 |
| qualification-01 | 999 → 999 | 931 → 931 | 2/2 |
| qualification-02 | 1000 → 1000 | 981 → 981 | 2/2 |
| qualification-03 | **951 → 788** | **920 → 788** | **0/2** |
| qualification-04 | 956 → 956 | 918 → 918 | 2/2 |
| qualification-05 | 992 → 992 | 987 → 987 | 2/2 |

All twelve direct controls emit valid normally terminated scalar JSON actions.
Their 10/12 score exactly repeats course-2; original and revised qualification-03
are the same mathematical errors, with larger correct values present in the
permitted inputs. There is no evidence of input clipping, a changed oracle or
cross-agent information leakage in these full-information requests.

This run's twelve direct controls use **193 generated tokens**, **3,073 input
tokens** and **26.328435 ready-model seconds**, median **2.161065 seconds**.
Under the current scientific rule the screen still fails. Under the previously
proposed protocol-first rule these controls would meet the scalar protocol check;
that proposed rule has not been adopted or implemented.

## 7. Every thinking result and the matched comparison

The table follows actual admission order. Requests use the same complete arrays
and per-input seeds as their direct counterparts, but the native thinking prefix
and declared generation settings differ. Direct uses temperature 0.7/top-p 0.8
and maximum 512 tokens; thinking uses 1.0/0.95 and maximum 4,096 tokens. This
is a comparison of those complete operating conditions, not a single-factor
causal experiment on the reasoning flag alone.

| Control | Truth | Direct final | Thinking final | Direct seconds | Thinking seconds | Direct / thinking tokens |
|---|---:|---:|---|---:|---:|---:|
| qualification-00 original | 950 | 950 | 950 | 2.271 | 177.085 | 16 / 1,710 |
| qualification-00 revised | 921 | 921 | 921 | 1.921 | 124.833 | 16 / 1,259 |
| qualification-01 original | 999 | 999 | 999 | 2.519 | 190.602 | 16 / 1,929 |
| qualification-01 revised | 931 | 931 | 931 | 2.026 | 124.750 | 16 / 1,256 |
| qualification-02 original | 1000 | 1000 | **No valid final; capped** | 2.479 | 404.775 | 17 / 4,096 |
| **Matched total** | | **5 correct finals** | **4 correct finals, 1 invalid** | **11.215** | **1,022.044** | **81 / 10,250** |

The four valid thinking finals are each 42 characters of visible JSON. Their
private reasoning strings have 3,726, 1,892, 3,678 and 2,495 characters. The fifth
contains 9,329 characters and no closing thinking delimiter. All private text
is preserved for audit and counted in physical cost; it is not peer-visible
conversation and is not treated as a faithful explanation of internal causation.

Even excluding the capped failure, the four valid thinking responses take
**617.269 seconds versus 8.736 seconds** for the same four direct controls:
**70.66 times the model time**. Counting the capped failure is necessary for
the complete resource comparison and gives the 91.13-fold result.

Observed thinking throughput is approximately **10.03 total generated tokens per
ready-model second**; individual calls are about 9.66–10.12 tokens/s. Thus the
long wait is explained primarily by generating 1,256–4,096 tokens to deliver a
short scalar action, not by a stalled controller or a uniquely slow token step
on the failed example. Forward progress continues throughout that example.
Serial qualification leaves the other resident device idle during each call;
parallelization could reduce some wall time but would not remove the per-call
output volume or the missing-final problem.

**Accuracy caveat:** 4/4 among completed valid finals is a selected subset, not
100% thinking qualification accuracy. The attempted-control result is 4 correct,
1 invalid, and 7 unexecuted. Neither 4/12 with seven failures nor 12/12 success
is supported. In particular, both qualification-03 thinking controls are unknown.
No evidence establishes that thinking would correct the observed direct errors.

## 8. Exact failure chain

1. `qualification-02/control-original-thinking` is admitted at 11:10:26.695196
   UTC as slot-0 attempt 12, global course-3 attempt 23.
2. It produces **exactly 4,096 tokens** in **404.774738 seconds** with
   `termination='length'`, `truncated=true`, `failure=null`, finite scores and
   fresh-cache evidence. There is no `</think>` delimiter and no final action.
3. [inference.py](../../recovery/i01/inference.py), `split_visible`, returns empty
   visible output and `thinking_framing_defect`. Its raw text includes mentions
   of the correct number `1000`, but those are not a submitted answer. Extracting
   one would be host-side answer repair.
4. [workflow.py](../../recovery/i01/workflow.py), `Session.call`, saves raw output
   and marks the physical attempt completed because the provider returned. It
   also sets global `model_defect` for any framing error.
5. `control` commits a terminal control state with `correct=0`,
   `error='truncated_action'`, and `submissions=[]`, then raises the global
   provider/framing error. The twelve-control list does not finish.
6. `run_action` records the traceback and exports; the notebook records its
   stopped action and a further error-boundary checkpoint. All five outcomes
   remain inspectable; no retry or answer substitution occurs.

There are two distinct findings: a real **model-output truncation/noncompletion**,
and an **implementation classification error** that calls it a global runtime
defect. The second was a scripted course-2 counterexample; it is now observed in
target-host evidence. Fixing that classification would improve reporting and
legal turn handling, but would not make this 4,096-token reply a valid answer or
make the existing strict thinking qualification pass.

The saved private text repeatedly scans candidates and rechecks output format;
it already mentions the correct maximum before exhausting the cap. This describes
the visible audit text only. The internal reason it continued generating cannot
be established from that text, and no additional inference is needed to score
the absent final action.

## 9. Partial-screen reporting and later headroom refusal

The aggregate `screen/thinking` receipt is **absent** because the comprehension
raises before `Session.screen` writes its twelve-control summary. Individual
call outcomes and control states are present. Treating an absent aggregate as
"thinking never ran" would therefore lose five expensive recorded attempts.

The failure-analysis export lists only the two direct wrong submissions. It
omits the thinking truncation despite its explicit control-state error.
[report.py](../../recovery/i01/report.py) derives errors from team event arrays,
which scalar control states lack. Its two direct failure labels also still have
empty call references. Consequently, the failure-label figure understates the
observed invalid-control evidence, while the attempt ledger and conversations
retain it correctly. `control_completed: 17` means terminal controls, not seventeen
valid or correct answers.

At 11:28:50 UTC the notebook invokes selected headroom and receives
`No passing competence screen`. This is a correct refusal under the unchanged
rules: direct failed and thinking has no accepted screen. No full-envelope
request reaches inference. This error occurs in mode selection before the
central operator action/receipt wrapper, so it is absent from archived
`operator-errors.jsonl` and the final ZIP remains at its earlier 11:17:15 boundary.
The notebook is the evidence for the later refusal; the archive should not be
described as containing that later event. There is no basis to add a physical
attempt for this refusal.

## 10. Durability, memory, remaining stages and scientific limits

The two databases contain respectively **12 and 11 calls/attempts**, and **9 and
8 terminal control states**. All 23 physical rows are completed, including the
invalid output. There are no admitted/unresolved attempts, known timeouts,
recorded retries, contingency charges or human annotations. Completion denotes
a durably returned provider outcome, independently of protocol/mathematical success.

Two periodic settled-call checkpoints appear during thinking, followed by the
action and operator-error exports. The first two calls together exceed five
minutes before the first periodic snapshot; a single later call lasts more than
six minutes. The policy checkpoints at settled boundaries, not halfway through
an active generation. Error-boundary reconstruction passes and raw evidence is
not lost. The final-report, final-save/verify and close cells were not executed.

Observed short/request headroom is about 7.081 GiB in readiness, at least 7.065
GiB in direct controls, and at least **7.042 GiB** in thinking. The capped call
has 7.042 GiB observed headroom and valid cache/finite instrumentation. It is not
an OOM diagnosis. These requests have only about 67–258 input tokens; they do not
accept the required **8,192-input full selected-output envelope**.

| Recorded quantity | Course-3 |
|---|---:|
| Physical attempts | 23 |
| Hardware / direct / thinking attempts | 6 / 12 / 5 |
| All generated tokens / input tokens | 10,531 / 4,751 |
| All ready-model / observed dispatch seconds | 1,062.335 / 1,062.467 |
| Successful load seconds | 101.862 |
| Main pairs known / intended | 0 / 20 |
| Clear-minus-retain effect / interval | Unknown / unavailable |
| Missingness bounds | [-1, 1] |
| Correct-prefix denominator / unknown prefixes | 0 / 20 |

All three pilots/reviews, configuration review, freeze, main-batch preparation,
main execution/review and final notebook report/archive/close cells are
unexecuted. The fourteen unexecuted code cells must not be inferred successful
from the presence of partial reports. Main outcome/cost plots remain empty or
unknown because there are no team episodes. No distributed collaboration,
retention/clearing effect, or accepted model mode has yet been observed.

Later process liveness, provider allocation/release, actual available quota and
off-session browser-download behavior remain outside these receipts. The
notebook retains a large embedded load inventory and a direct inspection dump;
those explain much of its file size but not the seventeen-minute inference cost.

## 11. Recommended interpretation

Choose direct mode for the proposed continuation because it supplies valid
short actions at roughly two seconds on these controls and the observed thinking
condition adds a very large cost with an incomplete protocol outcome and no
demonstrated correction of the difficult case. Frame this as a **pragmatic,
qualification-informed mode choice**, not a statistically established general
accuracy superiority claim.

To proceed scientifically, the proposed removal of mathematical accuracy as an
admission gate must be explicitly adopted, consistently including pilot accuracy
rules. Keep exact outcome scoring, controls, failed prefixes, all twenty worlds,
the correct-prefix secondary stratum and strict execution/protocol/resource
checks. Separately repair the now-observed framing classification and report
gaps, resolve source-compatible continuation and reconcile the repeated physical
spending. The solution proposal gives that order without implementing changes
or launching any further calls.
