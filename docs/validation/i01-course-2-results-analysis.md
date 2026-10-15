# I-01 course-2: complete executed-evidence analysis

15 October 2026. This is an audit of supplied execution, not a new experiment.
The actual folder is [notebooks/run/course-2/](../../notebooks/run/course-2/).
The companion [fix proposal](../proposals/i01-course-2-fix-proposal.md) separates
the observed stop from additional implementation defects. No inference was
performed during this audit; production modules and supplied files are unchanged.

## 1. What happened

Course-2 successfully installed the pinned runtime, attached the controller,
passed the native self-check, verified the pinned weights, loaded **both actual
T4 replicas**, and completed six fresh-state diagnostics. The direct competence
screen then produced **10/12 correct controls, zero protocol errors**. The
required threshold is **at least 11/12 with zero malformed/truncated actions**.
The notebook therefore stopped correctly before thinking qualification,
full-envelope headroom checks, pilots, freeze, and main execution.

The two wrong answers are both from `qualification-03`. The model returned
`788` on the original input, whose maximum is `951`, and on the revised input,
whose maximum is `920`. Both replies are well-formed, short JSON actions ending
normally. Neither a Python crash nor an out-of-memory event caused this stop.

The four `[ERROR]` lines in the controller log concern upstream **docstrings**;
the two fast-path messages concern a recurrent-kernel fallback; the four
`FutureWarning` messages concern a deprecated bitsandbytes/PyTorch helper.
Loading and all eighteen calls continued after those messages. They should not
be counted as ten failed model calls or confused with the competence failure.

All twenty intended main pairs remain **unknown**. There is no retain/clear
effect estimate, pilot acceptance, frozen configuration, or completed experiment.

## 2. Authority and evidence identity

[Specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
is authoritative. The [WBS](../plans/i01-course-implementation-wbs.md),
[handoff](../IMPLEMENTATION_PLAN.md), [operator runbook](../I01_KAGGLE.md), and
[previous repair evidence](i01-course-1-repair.md) supply implementation context.
Historical thesis/course results are separate populations and are not substituted
for this I-01 run.

Reviewed checkout is `E:\Github\recovery_blueprint\recovery_blueprint`, on
`feat/smaller-natural-experiment`, after input commit `e2b8490`. The executed
source release is `8f5bcdb661a177ebf7e0ca320889612ba448c64b`; its scientific
Python modules match the reviewed checkout. Study ID is
`c2973855-84fa-411d-9f6c-a08f8acc79d6`; controller-session ID is
`1b2059eb-50e3-4952-b658-b13357130b8f`.

| Supplied artifact | Bytes | SHA256 |
|---|---:|---|
| [Executed notebook](../../notebooks/run/course-2/multi-agents-course-v1nb.ipynb) | 962,191 | `6052dd7718b8f568f67b3ec082a9e6f3b746a47e4e92f48d36dbc43c5e9ea046` |
| [Checkpoint](../../notebooks/run/course-2/latest.zip) | 1,385,553 | `3dc4040b82d75325cbce1103db04326c8af5cd2e635bb8f87549deeba6add782` |

The ZIP contains **122 members** and 6,200,323 uncompressed bytes. Its CRC,
all **121 integrity inventory entries**, both SQLite integrity checks, all
**67 source-release entries**, and all **44 wheel Python-module comparisons**
pass. Fresh read-only analysis of extracted copies exactly matches archived
`reports/analysis.json`, including outcomes, costs, raw traces, gates and metadata.

The final boundary is `operator-error-screen`, created at
**2026-10-15 09:50:09.013014 UTC** (11:50:09.013014 in Budapest). It contains the
post-screen operator receipt as well as all eighteen raw outcomes. Unlike the
course-1 self-check-boundary ZIP, this archive contains the later weight receipt
and the executed qualification evidence.

The notebook has 54 cells, including 26 code cells. Nine code cells executed
once, in counts 1–9; seventeen have no execution/output. Joining source lines
shows only one changed cell relative to the shipped notebook: the operator's
session-window configuration. No scientific prompt or research-stage code was
edited in the supplied notebook.

Machine-readable evidence and reproducible, temporary counterexamples are in
[course-2-audit.json](course-2-audit.json) and
[audit_i01_course2.py](../../scripts/audit_i01_course2.py).

## 3. Cell-by-cell execution and timing

Times below use notebook busy/idle metadata in UTC. These are cell wall times,
including controller, reporting and checkpoint work. They are not pure model
latency or provider billing boundaries. Budapest local time is UTC+2 on this date.

| Executed cell | UTC start → end | Wall seconds | Assessment |
|---|---|---:|---|
| Configure/workspace | 09:40:49 → 09:40:53 | 4.002 | Source and destination selected; two T4s observed |
| Install runtime | 09:40:53 → 09:44:11 | 198.297 | Pinned setup/metadata accepted; setup receipt measures 196.005 s internally |
| Open study | 09:44:11 → 09:44:14 | 2.756 | Fresh inputs, DBs, retained controller and checkpoint |
| Implementation check | 09:44:14 → 09:44:27 | 12.644 | Scripted invariants and native tokenizer acceptance passed |
| Download weights | 09:44:27 → 09:47:17 | 170.597 | Twelve exact native files verified; weight receipt checkpointed |
| Record window | 09:47:17 → 09:47:19 | 2.135 | Fixed deadline accepted; no inference |
| Load both workers | 09:47:19 → 09:49:20 | 120.263 | Both actual T4 replicas loaded successfully |
| Fresh-state readiness | 09:49:20 → 09:49:37 | 17.155 | Six calls; finite scores, fresh caches and A/B/A equality passed |
| Direct competence | 09:49:37 → 09:50:09 | 32.210 | Twelve calls; 10 correct; gate correctly withheld |

The observed notebook span is **560.068 seconds**, about 9 minutes 20 seconds.
Successive busy times follow preceding idle times closely; this is consistent
with queued cell execution, but does not prove which Kaggle UI command was used.
The saved failure prevented later cells from executing. This does not establish
that Run All is an approved or safe research workflow; use explicit stage cells.

## 4. Workspace, installation and weight retrieval

The host records Linux x86_64, Python **3.13.15**, CUDA driver **580.178.04**, two
Tesla T4 devices and 15,360 MiB reported by `nvidia-smi` per device. The distinct
UUIDs are:

- Slot 0: `GPU-955d8bbe-7d02-f9fb-e0aa-687a512f792d`.
- Slot 1: `GPU-47411471-240a-ec25-1677-fe5cb83001bc`.

Initial output storage was about 19.5 GiB free; scratch was about 1,069.9 GiB
free. The large native checkpoint was placed in scratch, not copied into the
small output archive. The source is
`/kaggle/working/i01-source-8f5bcdb661a1`; the fresh study destination is
`/kaggle/working/i01-repaired-study`.

The environment is release-labelled `i01-venv-8f5bcdb661a1`. Its startup receipt
confirms `isolated=true`, `site_processing_disabled=true`, distinct venv/base
prefixes and `hook_automatically_imported=false`. A discoverable system
`sitecustomize.py` is listed, but discovery is not execution. Listed `.pth`
filenames likewise do not establish processing. There are no `wrapt`,
`sitecustomize`, or inline-Matplotlib backend failures in the controller log.
This run supplies actual Linux evidence for the previous startup repair.

Pinned packages include Torch `2.11.0+cu128`, Transformers `5.12.0`,
bitsandbytes `0.49.2`, Accelerate `1.14.0`, tokenizers `0.22.2`, and
huggingface-hub `1.19.0`. Verified pip bootstrap remains `26.2.1`; ensurepip was
bypassed. Installation completed and `pip check` passed. These observations
accept this saved installation, not every possible future Kaggle image.

Metadata retrieval verified 22,991,639 bytes. Weight retrieval verified
**19,329,302,519 bytes (18.002 GiB)** across twelve files, including four native
Safetensors shards. Model and revision match the adopted Qwen3.5-9B pin. Downloads
and loads consume time/storage but are **zero model-generation attempts**.
The progress display remained at file-fetch completion while later work
continued; this alone is not evidence of a hung download.

## 5. Session allowance and model loading

The edited cell sets `SESSION_REMAINING_MINUTES = 700`. Its evidence text says
the provider shows twelve hours. These are not identical durations: the actual
recorded bound is **11 hours 40 minutes**, twenty minutes shorter than the text.
That difference may be an intentional safety margin; the evidence does not say.
The resulting deadline is **2026-10-15 21:27:17.689021 UTC**, with recorded
observation start 09:47:17.699644 UTC. This is an operator assertion, not an
independently captured provider timer/quota. Do not claim twelve verified hours
or use that historical deadline for another session. Preparation had already
consumed time before this window was recorded.

Both workers loaded the verified local pinned snapshot, with PIDs **394** and
**409**, in **73.116 s** and **43.881 s** respectively. The sum, **116.996 s**,
is consistent with sequential loading and the longer 120.263-second cell wall
time. Both report `Qwen3_5ForCausalLM`, the reviewed `recovery_t4_sdpa` attention,
and no missing/unexpected/mismatched tensor keys or loader errors.

Each load inventory has 427 parameters: 248 packed `uint8` parameters and 179
FP16 parameters, plus FP32 rotary buffers and 1,240 quantization-tensor entries.
The output head is untied in this model; `tied_output_head=false` is not itself
an error. Both replicas report logical `cuda:0` because each child sees only its
assigned physical device. `CUDA_VISIBLE_DEVICES` and actual UUIDs distinguish
the physical T4s; this is not accidental placement on one GPU.

The load receipt contains an inherited 256-token generation configuration from
the reused reviewed loader. It is labelled loading-only. All eighteen saved
requests instead have the adopted **512-token direct configuration**, and the
adapter sets that configuration before generation. The old load configuration
is confusing audit presentation, not evidence that this screen ran at 256 tokens.

## 6. Readiness: what the six calls establish

Each device ran A1 `[-7,3]`, B `[100,-9]`, A2 `[-7,3]`. A1/A2 match tokens on
both devices; their seeds repeat within device as intended. Answers were `3`,
`100`, `3`, all valid JSON and normally terminated. Every outcome records
finite-score checks, an initially empty call-owned cache, use of that same cache
within the call, and disposal. Recorded CPU/CUDA seeds equal the request seed.

Together these six calls consumed **88 generated tokens** and **14.810811 s**
of ready-model inference. The first calls are slower than repeated short calls,
consistent with initialization overhead, but no separate hidden warmup appears
in the saved ledger. These are physical attempts 1–6, counted in hardware/state.

These checks support fresh-state operation on the two loaded replicas. They do
not establish all future cache behavior, competence on forty numbers, or the
8,192-input/selected-output memory envelope. No state-review override was needed.

Some controls show seventeen cache-forward observations for sixteen generated
tokens. Inputs longer than the 256-token prefill chunk require a second prefill
forward. Across all eighteen calls, the counts equal generated tokens plus
prefill chunks minus one. These are internal forwards, not additional physical
attempts. The six hardware diagnostics also have `effect_committed=0` because
they save raw outcomes without a team-state effect; their outcomes and all
eighteen attempt completions are present, so this is not six unresolved calls.

## 7. Every direct competence result

Each control receives all forty current numbers, no conversation and one final
scalar submission. Original and revised controls are separately seeded calls.
All twelve have EOS termination, no truncation, no framing error, no provider
failure and valid exact-key actions.

| World | Slot | Original truth → submission | Revised truth → submission | Correct |
|---|---:|---|---|---:|
| qualification-00 | 0 | 950 → 950 | 921 → 921 | 2/2 |
| qualification-01 | 1 | 999 → 999 | 931 → 931 | 2/2 |
| qualification-02 | 0 | 1000 → 1000 | 981 → 981 | 2/2 |
| qualification-03 | 1 | **951 → 788** | **920 → 788** | **0/2** |
| qualification-04 | 0 | 956 → 956 | 918 → 918 | 2/2 |
| qualification-05 | 1 | 992 → 992 | 987 → 987 | 2/2 |

Accuracy is **83.33%**, with 5/6 correct in each input phase. Slot 0 has 6/6
correct controls; slot 1 has 4/6, and its other two worlds pass. That pattern
does not establish a defective GPU. The diagnostic calls on slot 1 also pass.

For qualification-03, the original top four numbers are `951, 920, 815, 788`.
The revised top three are `920, 815, 788`, after record 12 of agent 1 changes
from `951` to `-801`. The returned `788` is at zero-based flattened index 27,
or row 7 of that shard. The required maxima and other larger current values
appear in their respective saved prompts. Request views match the manifest, all input masks are ones,
and input counts are 257 tokens each, far below 8,192. The error is not explained
by a missing maximum, input clipping, wrong oracle, or malformed scalar parsing.

The failed original seed is `367958775560601292`; the revised seed is
`6417685603553177256`. These are distinct requests with separate admissions,
outcomes, timings and cache records. Identical visible answers do not establish
cross-call replay or shared hidden state. The revised answer is also not the
withdrawn winner `951`, so an obsolete-winner label would be unsupported here.

**Confirmed proximate cause:** under the approved direct prompt/decoding/model
condition, two recorded scalar answers are mathematically wrong. **Unknown
internal cause:** attention, stochastic choice, representation, quantization or
another model-level mechanism cannot be separated from these traces. There is
no saved private reasoning in direct mode. Do not attribute this to anchoring,
the fallback kernel, a hardware defect or quantization as a demonstrated cause.

The screen consumes **193 generated tokens**, **3,073 input tokens**, and
**27.427790 ready-model seconds**. Median per-control ready time is **2.225688 s**;
the range is **1.934073–2.744822 s**. These short controls are not a latency
forecast for full thinking output or long distributed conversations.

Exact replay of this screen on temporary copied records reproduces 10/12 with
**zero new provider calls**. Rerunning the direct cell preserves failure; it must
not resample the two answers, lower the threshold or replace the world.

## 8. Classification of visible errors and warnings

| Saved message | Count | Root/source and interpretation |
|---|---:|---|
| `loss`/`logits` undocumented signature `[ERROR]` | 4 | Two per replica; upstream import-time documentation diagnostics; loads and subsequent calls succeed |
| Recurrent fast path unavailable | 2 | Optional accelerated kernels unavailable; saved load reports `recurrent_fast_path=false`; Torch implementation used |
| bitsandbytes `_check_is_size` FutureWarning | 4 | Compatibility warning from existing CUDA operations, not four failed attempts |
| `ActionStopped` after direct screen | 1 | Expected notebook barrier for 10/12, with the completed evidence safely archived |
| OOM, CUDA crash, controller traceback, missing-wrapt startup failure | 0 observed | Their absence in this saved run is not a guarantee for unexecuted long-envelope paths |

The documentation diagnosis is supported by the matching
[Transformers 5.12.0 auto-docstring source](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/utils/auto_docstring.py#L3105)
and its diagnostic print path. The fallback comes from the
[5.12.0 Qwen3.5 implementation](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py#L386).
The deprecated helper is present in the
[bitsandbytes 0.49.2 CUDA source](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/0.49.2/bitsandbytes/backends/cuda/ops.py),
with a later [upstream replacement change](https://github.com/bitsandbytes-foundation/bitsandbytes/pull/1940).
These references explain message origin; the run's own completion evidence
establishes that these particular messages were nonfatal. No dependency or
optional-kernel installation is justified as an automatic cure for two wrong answers.

## 9. Accounting, durability and reports

Both worker databases have nine calls and nine completed physical attempts,
six completed control episodes and one successful load session. There are no
admitted/unresolved attempts, retries, recorded contingency, annotations,
provider failures or timeouts. Two **scientifically incorrect** answers still
have `status=completed`: transport completion and mathematical correctness are
different quantities.

| Quantity | Saved value |
|---|---:|
| New physical attempts | 18/500 |
| Hardware/state first attempts | 6/8 |
| Direct qualification first attempts | 12/12 |
| Thinking qualification first attempts | 0/12 |
| Pilot / main attempts | 0 / 0 |
| Recorded contingency | 0/28 |
| Remaining overall allowance, with this archive's zero gap | 482 |
| Prior historical attempts, separate | 45 |
| Generated tokens / input tokens, all eighteen calls | 281 / 3,479 |
| Ready-model / observed dispatch seconds | 42.238601 / 42.364530 |
| Successful model-load seconds | 116.996116 |

The two remaining ordinary hardware attempts are the two selected-mode envelope
probes. Conditional thinking permits its existing twelve controls; it does not
license extra direct attempts, different worlds, different seeds, another model,
or a reset of the eighteen already spent attempts. The 482 remaining attempts
are an overall bound, not permission to expand stage ceilings or main population.

Short-call observed free headroom is approximately **7.065–7.081 GiB** per
device. This is encouraging short-request evidence, not acceptance of the
required full envelope with at least 1.5 GiB headroom. No such probe ran.

The archive includes full JSON call requests/outcomes, token IDs, two SQLite
backups, load/runtime receipts, conversations, CSV tables, SVG/PNG figures and
partial reports. Every saved original/revised oracle and the fixed 29-world
manifest reproduce from the approved config. Main paired counts are
`unknown: 20`; the contrast and interval are null, missingness bounds are
`[-1, 1]`, and correct-prefix denominator is zero with twenty unknown prefixes.
Zero known prefixes does not mean twenty incorrect prefixes. Empty recovery-cost
plots and the unknown-pair bar accurately reflect unexecuted work. The two
failure-label counts and twelve control terminal counts describe qualification,
not failed recovery experiments.

Unexecuted policy rows have `complete=false`, unknown seconds/tokens, but
`logical_end_to_end_calls=0`; the observed dispatched count is indeed zero.
Completed-policy effort is nevertheless unknown. Consumers must honor the
completion flag; clearer naming/null final totals would prevent treating missing
execution as zero-cost policy efficiency. The paired-cost table already keeps
these unexecuted call contrasts null.

There are presentation defects: the failed-control label rows have empty `calls`
references because controls do not have team event lists; the report lacks a
clear qualification-result table; default detailed inspection shows six calls
from slot 0 before the failed slot-1 calls; and the load cell serializes about
843,099 output characters by embedding full inventories. Complete raw evidence
still exists; these are discoverability and trace-reference defects.

No notebook close cell ran. The archive records loaded processes, not their
subsequent live status or provider release. Provider assignment/release and quota
remain unknown beyond the operator assertion. A generated download link is not
proof of an off-session download, though the supplied ZIP itself is now available
for this audit. Native tokenizer files/weights are not embedded; their receipts
are checked, while a new independent native re-tokenization was not performed.

## 10. Every remaining stage

| Unexecuted cell(s) | What is known / required |
|---|---|
| Inspect qualification | Can inspect existing twelve controls with zero calls; failed case is qualification-03 |
| Optional thinking screen | Scientifically eligible after documented direct competence limitation and zero protocol errors; not executed or accepted |
| Selected headroom | Requires passing selected competence screen; 8,192 input and full selected output, two physical T4 probes |
| Pilot 1 and review | No team conversation or original/retain/clear outcomes; requires its own inspected checkpoint/review |
| Pilot 2 and review | Unexecuted; requires prior pilot review |
| Pilot 3 and review | Unexecuted; requires prior pilot review |
| Review configuration | No measured pilot forecast yet |
| Freeze | Absent; passing original teams, six pilot controls, communication/protocol/usability and adequate forecast still required |
| Prepare main batch | No scope prepared; fixed one/two-world actions only after freeze |
| Run main batch | No main calls or outcomes |
| Review main batch | No completed scope to acknowledge |
| Final report cell | Unexecuted; partial reports were generated by checkpoint export instead |
| Save/verify final archive cell | Unexecuted; the supplied error-boundary ZIP nevertheless verifies independently |
| Finish session | Unexecuted; later termination/provider release cannot be inferred |

## 11. Additional defects, confidence and next decision

The audit reproduces five separate future-path defects using temporary synthetic
records: lost-spending erasure on restore, acceptance of duplicate logical worker
files, stale envelope reuse when load references change without the reload flag,
global-stop classification of normal thinking truncation, and a live-analysis
read race. None occurred in course-2's saved eighteen calls. Their exact
counterexamples, priorities, fixes and acceptance checks are in the companion
proposal; this report does not present them as observed GPU failures.

The evidence supports successful target-host preparation, actual short inference,
state readiness and a failed direct competence screen. It does not support a
qualified model, accepted full-envelope memory, useful collaboration, or a
retention/clearing effect. The next scientific candidate is the already approved
conditional thinking screen, after evidence-based justification. The critical
implementation/recovery findings should be addressed before relying on those
future paths. This audit neither launches that screen nor changes the design.
