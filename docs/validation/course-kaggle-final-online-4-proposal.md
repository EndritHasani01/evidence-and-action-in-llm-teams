# Kaggle final-online-4: diagnosis and complete repair proposal

Implementation update: the user subsequently requested "Fully repair it".
The scoped model/prompt/deadline/attempt adoption is in specification §11.3;
the [implemented repair and tested delivery](course-kaggle-final-online-4-repair.md)
records the final artifacts, implemented behavior and CPU checks.
The proposal below preserves the original diagnosis and then-pending decisions.

Prepared 13 October 2026 on `feat/course-m5-inference-preparation`, inspected
HEAD `7456186`. This is an evidence-backed proposal, not an adopted scientific
amendment or a new execution package. Production code, model settings, attempt
allowances and the submitted artifacts remain unchanged. This investigation
made zero GPU calls and downloaded no checkpoint weights.

Authority remains [PROJECT_SPECIFICATION §11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime).
The existing Run All authorization covers the adopted pinned configuration;
it does not authorize a different model, renderer, diagnostic deadline or
additional attempts. The proposed changes below need a concrete scope amendment
before GPU execution. They retain automatic orchestration and require no manual
memory proof, budget form or intermediate operator decisions.

## Recommendation

The repaired notebook now reaches real hardware characterization. Its new
failure is a **known 120-second timeout on the first complete-input probe**,
not either previously repaired software defect. There is also substantial
evidence of inadequate protocol compliance and answer quality from the original
4B smoke replies. Extending the timeout alone would not address that problem.

Keep the existing runtime and research pipeline. Add bounded live inference
progress and accurate failure reporting; propose a longer deadline for the two
hardware-only stress probes; clarify the uniform compact-output instructions;
and qualify pinned Qwen3.5-9B as the preferred development candidate, with 4B
under the same clarified instructions as a predeclared fallback. Run hardware,
the existing first-90 screen, the full pilot and conditional freeze/main in
that order. Reuse the saved development worlds and exact acceptance criteria.

This can prevent known interface defects and make future failures diagnosable
and bounded. It cannot guarantee model competence, physical memory fit, network
availability or uninterrupted Kaggle sessions. A failed gate must still finish
with an accurate limited report and preserved evidence.

## 1. What actually happened

Primary evidence is the [executed notebook](../../notebooks/run/final-online-4/notebook-exec.ipynb),
[resume payload](../../notebooks/run/final-online-4/course-resume.payload),
[results ZIP](../../notebooks/run/final-online-4/course-results.zip) and
[last action](../../notebooks/run/final-online-4/last-action.json).
The [read-only diagnostic](../../notebooks/validation/course-kaggle/analyse_final_online_4.py)
and [executed CPU receipt](../../notebooks/validation/course-kaggle/final-online-4-analysis.json)
record hashes, original worker-row equality, native timing, protocol outcomes,
independent mathematical checks and model architecture estimates.

Both submitted archives pass CRC checks. All 73 committed source members match
their source manifest, bound to `d6c2d6d9336dc80e85ca3e5fc75c8f1cb2d26797`.
All five code cells match the repaired notebook by Python AST. Both worker
databases pass SQLite integrity checks. All 21 original call rows and attempt
rows are identical to final-online-3: their replies were reused, not regenerated.
The two actual GPUs are distinct Tesla T4s, each reporting 15,360 MiB.

The repaired full-plan preflight passed all 24 constructors and the real pinned
generation-processor check. The host checks and native loading audits also
passed. There is no new `RenderedRequest.system`, inherited diagnostic EOS or
`hf_device_map` failure.

| Event | Recorded evidence |
|---|---|
| Attempt | `course-hardware/envelope/device-0`, number 1 |
| Complete input | 109,851 tokens; 110,107 including the output reserve |
| Attempt start, UTC | 2026-10-13 11:48:46.516788 |
| Child ready, UTC | 11:49:07.144067 |
| Provider startup | 20.621926 seconds from process start to ready |
| Remaining deadline after readiness | About 99.38 seconds for the remaining work |
| Terminal outcome | `timeout`, `known 120-second attempt deadline` |
| Recorded elapsed | 120.222352 seconds, including cleanup observation |
| Termination | Confirmed; child exit code -15; no uncertain completion |
| Returned raw reply, memory/cache evidence | None |

Readiness does not establish how the remaining time divided between transfer,
prefill and decoding. No partial forward telemetry survived in a structured
result. Consequently, **OOM, nonfinite scores, cache correctness and full-input
headroom are unestablished**, rather than proven causes or successes. The
generic outer `BudgetStop: recorded_model_attempt_failure` is a workflow stop
label; the SQLite timeout row provides the actual cause. No GPU-hour budget
ceiling stopped this run.

The reported 4.14 GiB peak and 10.42 GiB minimum free memory derive from the
previously completed ordinary probes. They do not characterize this failed
109,851-token attempt. Native preflight is CPU configuration evidence, not
complete-input acceptance. The HTML copied at the submission root is also
identical to the previous submission; the current analysis is the payload's
`analyses/20261013T115050859262Z/` export. Analysis reports zero recorded main
uses and all **6,280 unknown**. An exported notebook with no uncaught cell error
is not a completed experiment.

## 2. Attempt accounting and restart consequences

The current worker databases contain 22 physical attempts: 21 retained ordinary
probes and the new terminal timeout. With the retained final-online-2 loader
failure, cumulative preparation usage is **23/25**. Device-1's full-envelope
probe and the controlled hang are still unattempted.

The two remaining slots cannot turn device-0's failed probe into a passing
matrix. A known timeout is not an infrastructure interruption eligible for the
one identical retry. Restarting this payload under the unchanged configuration
should refuse further dependent execution before costly cold setup. Preserve
that behavior. Never delete the timeout, reset spending, overwrite `run_inputs`,
resample the 21 replies or relabel a changed request as the original attempt.

For a timing-only investigation with unchanged 4B ordinary requests, repeating
device-0 under a reviewed diagnostic deadline and completing device-1/hang
would require **three additional diagnostics**, bringing the cumulative count
to 26. That exceeds the incident authorization. A narrow addendum would have
to define the new diagnostic settings/IDs, evidence aggregation and strict
source-bound continuation explicitly. This cheaper route can characterize
hardware; it does not solve the observed output-quality failures.

For the recommended model/prompt route, start a fresh, normally bound candidate
bundle. Historical 4B records remain evidence in the original bundle. They are
not replayable outcomes for 9B or for changed rendering. Existing IDs may be
used within their separate bundles as the contract permits; no new identity
registry or permissive source-hash bypass is needed.

## 3. What the original model replies tell us

The 21 reused replies comprise:

| Outcome | Count | Interpretation |
|---|---:|---|
| Invalid JSON | 12 | All reached the 256-token output cap |
| Wrong candidate shape | 5 | Parseable JSON, incorrect answer representation/width |
| Wrong message schema | 2 | Required recipient field absent |
| Protocol-valid | 2 | Both sorting candidates are mathematically incorrect |

Independent insertion-order calculations agree with the production truth for
both valid candidates. One saw only six source records; the other saw all 24.
Their expected first six sorting ranks are `[0,2,5,12,15,15]`; the replies were
`[24,62,65,83,71,95]` and `[2,5,7,8,9,10]`.

The full-information controls give more direct warnings:

- `smoke/course-m5/06`, prefix sums: all 24 inputs visible, but 25 values
  returned. The first 20 are correct; the final values also contain arithmetic
  errors. This is not solely whitespace or insufficient private information.
- `/07`, sorting: all 24 inputs visible, but 23 values returned in an incorrect
  order, with zero placed last and multiplicity lost.
- `/08`, revised BFS: all 12 source records visible, including one tombstone
  and 11 live edges. The reply is a schema description with string values,
  rather than the required map of canonical node keys to integer distances.
- `/14` and `/15` use `"and":true` where a send's `"to"` field is required.
  The long `/18` reply similarly uses `"recipient"`, echoes candidate schema
  fields and then truncates.

Thus zero smoke replies are both accepted and exactly correct. These deliberately
selected hardware witnesses are **not the first-90 capability sample**, a
treatment-effect estimate or an unbiased model benchmark. Several private views
are underinformed, and retained stress history is artificial. Nevertheless, the
full-information errors justify a development configuration review.

Thinking was already disabled correctly: native requests contain the empty
`<think>...</think>` assistant prefix produced by `enable_thinking=False`.
Turning it off again is not a fix. Native long witnesses of about 22,200 input
tokens completed in approximately 59 seconds; the complete input is nearly
five times larger. The pinned runtime logs show the Torch recurrent fallback,
and the maintained prefill chunk is 256 tokens. These are plausible performance
contributors, not measured attribution of the timeout.

## 4. Concrete engineering changes

### A. Explain progress and the actual terminal failure

Use the existing child stdout, workflow logs, process records and status exports.
Emit a rate-limited line, approximately every 15 seconds, with call/device,
phase, elapsed time, prefilled/total tokens or completed decode steps. Capture
allocator peak/free memory at phase boundaries with the existing memory tools.
Keep output volume bounded and avoid per-token synchronization or logging
generated peer text before the ordinary persistence boundary.

On a timeout, render its call ID, configured deadline, startup time, last known
phase/progress and termination outcome directly in the notebook and hardware
report. Label partial samples as incomplete; never promote them to full-envelope
acceptance. Keep the completed-result memory audit and finite-score check.
The host can preserve flushed phase lines even when the child is terminated.
No progress database, telemetry service or replacement scheduler is required.

### B. Separate stress characterization from ordinary-call timing

Propose **600 seconds only for each of the two forced-256-token hardware
envelope probes**, retaining ordinary scientific calls at 120 seconds and
existing bounded TERM/KILL cleanup. Record the distinct diagnostic setting
explicitly. Ten minutes is a bounded characterization allowance, not a measured
runtime prediction or proof of eventual success.

A successful 600-second stress probe could establish the amended memory/state
criterion. It cannot establish success under the original 120-second hardware
rule or adequacy of ordinary-call deadlines. Ordinary timeouts remain recorded
failures and count against capability/pilot acceptance. If 120 seconds is
inadequate there, stop with evidence and seek a separate uniform pre-freeze
decision; do not quietly lengthen individual conditions.

First use the new phase timing to establish whether prefill is the bottleneck.
If needed, investigate a larger maintained chunk, such as 512 or 1,024, after
CPU chunked/unchunked logit, position, mask and cache equivalence checks and
bounded native memory measurement. Keep one declared choice for the selected
configuration. No blind library upgrade or speculative custom kernel is needed.
Standard FlashAttention-2 targets Ampere/Ada/Hopper; Turing support is a separate
implementation with different constraints, so installing its usual wheel is
not a justified T4 fix. [Official FlashAttention support](https://github.com/Dao-AILab/flash-attention/blob/main/README.md).
Any FLA path must demonstrate compatibility with the actual SM75 environment
and preserve recurrent-state/logit semantics before adoption.

### C. Clarify the uniform output instructions

Change only the common rendering instructions, uniformly across conditions.
Preserve permitted sources, notice, literal retained history, authority rules,
coordinate assignment, reference bounds and source/prose delivery. State that:

- `candidate` is the answer value, not a copy of `candidate_shape` metadata;
- numeric answers are flat integer arrays of the declared width in assigned
  coordinate order; ownership does not redefine assigned output ranks;
- BFS is the actual canonical node-to-integer map, not `type/keys/values`;
- a send has exactly `to`, `source_refs`, `text`; controls require `send=[]`;
- output is compact single-line JSON without Markdown or explanatory text.

The CPU diagnostic reserialized nine already parseable replies with identical
content. Native token counts fell, for example, from 247 to 161 and from 242
to 112. This demonstrates whitespace overhead only. It does not repair or
rescore any recorded reply, establish that the model will comply, or solve
arithmetic errors. Do not enlarge the uniform 256/64 caps, hide peer history,
inject oracle values, repair JSON, impose a guided decoder or switch to greedy
sampling. Any proposed few-shot examples or sampling changes need their own
review; begin with the smaller explicit instruction change.

Recompute the complete permitted-input bound with the actual selected tokenizer
and renderer. The current 109,851/110,107 constants must not silently carry
over to a changed prompt. Have the planner, envelope backend and gate consume
the existing validated capacity artifact as their common source of truth.

## 5. Model choice on two independent T4s

**Preferred candidate: Qwen3.5-9B**, revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, using the existing direct text-only
loader, NF4/double quantization and FP16/necessary FP32 calculations. One complete
independent replica belongs on each GPU. Its native text context is 262,144;
its configuration has eight full-attention layers with four KV heads of width
256. [Pinned 9B configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json).

The official model table reports stronger instruction following than 4B, for
example IFEval 91.5 versus 89.8 and IFBench 64.5 versus 59.2. Those published
evaluations do not establish performance with our quantization, non-thinking
mode, 256-token replies or research protocol. Local gates remain decisive.
[Official model comparison](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/README.md).

CPU-only meta construction with Torch 2.11.0 and Transformers 5.12.0 verified
the actual text architectures without allocating model parameter storage:

| Component per replica, GiB | 4B | 9B |
|---|---:|---:|
| Ideal packed four-bit linear weights, excluding LM head | 1.662 | 3.222 |
| Remaining weights assuming FP16 | 1.186 | 3.791 |
| Full-attention KV at the reference 110,107-token envelope | 3.360 | 3.360 |
| **Conditional subtotal** | **6.208** | **10.373** |

The 9B text model has 8,953,803,264 parameters and an untied embedding/head;
assuming all parameters cost half a byte would materially understate memory.
The subtotal excludes quantization metadata, necessary FP32 tensors, recurrent
state, activations, workspaces, transient cache copies and allocator overhead.
On an observed 15 GiB device, preserving 1.5 GiB headroom leaves approximately
3.13 GiB beyond that subtotal. **9B is plausible, not proven to fit or run fast
enough.** The estimate uses the old envelope for comparison; the new renderer's
bound must be recomputed before its stress test.

Pinned Hub metadata reports 19,306,310,880 checkpoint bytes across four shards,
about 17.98 GiB. Continue direct verified online downloading, with staging RAM,
largest-shard/transient disk, installed environment and export capacity checked
before allocation/loading. Keep these weights out of the dataset ZIP.

Other candidates are less attractive for this unchanged full-context design:

| Candidate | Reason to deprioritize |
|---|---|
| Qwen2.5-7B-Instruct | Useful structured-output alternative, but its pinned native configuration is 32,768; long context requires an explicit YaRN change and renewed capacity/backend review. |
| Qwen3-8B | Thirty-six full-attention layers/eight KV heads; at the reference envelope its FP16 KV alone is about 15.12 GiB. Native context is also shorter. |
| Qwen3-4B-Instruct-2507 | Native context is long enough, but the same dense KV geometry makes smaller weight size insufficient for this envelope on one T4. |
| Qwen3.5-27B / 35B-A3B | Larger resident weights/cache; 35B's active 3B is not its stored parameter count. No evidence supports independent full-context T4 replicas. |

These are configuration-based exclusions, not GPU benchmarks.
[Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct),
[Qwen3-8B configuration](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json),
[Qwen3-4B-Instruct configuration](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/blob/main/config.json),
[Qwen3.5-27B configuration](https://huggingface.co/Qwen/Qwen3.5-27B/blob/main/config.json),
[Qwen3.5-35B-A3B configuration](https://huggingface.co/Qwen/Qwen3.5-35B-A3B/blob/main/config.json).
Do not treat two T4s as a pooled 30 GiB replica, introduce tensor parallelism or
CPU offload, or select a smaller context by favorable empirical observations.

9B is not a notebook dropdown change. `Candidate` already knows its revision,
but course `candidate_settings` explicitly admits only 4B; the smoke inventory,
native metadata, fixtures and hardware bound are also 4B-specific. Update those
existing checks with the approved candidate's actual shapes, tied/untied behavior,
loading diagnostics and tokenizer/template. Retain `limits=COURSE_LIMITS`;
using the thesis defaults to bypass the guard would change the experiment.

## 6. Bounded qualification and automatic execution

Use a predeclared order: **9B plus compact instructions first; 4B plus the same
instructions only if 9B cannot pass qualification.** This is engineering
qualification on the five existing development worlds, not selection by main
treatment effects. The historical 4B replies establish the motivation, but
cannot isolate the separate benefit of model size versus prompt wording.

For each candidate:

1. Complete CPU shape/protocol/capacity, real pinned-generation, source-bound
   notebook/package and loading-contract checks. Download only verified online
   assets. Preserve all source/configuration decisions before native attempts.
2. Run its **fresh 24-row hardware matrix**, with the proposed diagnostic-only
   deadlines. Check actual independent devices, loading/state/finite-output,
   both complete-input forced-output/headroom probes and bounded hang cleanup.
   A failed matrix stops this candidate before capability inference.
3. Run the existing **first 90 development slots**, not a new control-screen
   subsystem. Require 9/10 correct controls including one per family, 3/5 jointly
   correct final prefixes and 14/20 correct final prefix-peer candidates.
4. Continue that same accepted bundle to the complete 1,114-generation pilot;
   first-90 outcomes are reused exactly inside it. Require at least 98%
   protocol validity and the independent raw/effect audit. Inspect family,
   arithmetic, truncation, timeout and condition failures.
5. Produce the measured runtime/coverage forecast, then conditionally freeze
   the unchanged accepted configuration and run the 5,752 new main generations
   / 6,280 logical uses under the already adopted Run All sequence. Derive
   reports, progress and reproducible exports from the existing workers.

The preferred single-candidate path requests **24 additional hardware attempts**
(47 historical cumulative preparation attempts including the current 23), then
up to 1,114 scheduled development generations. A preauthorized two-candidate
fallback path requests at most **48 additional hardware attempts** (71 cumulative)
and at most two complete development schedules. Unexecuted fallback calls are
never admitted or counted as performed. These are proposed scope ceilings,
not a reset of the original 25-attempt incident allowance. Failed configurations,
bounded infrastructure retries and observed setup/idle intervals remain visible
and counted under the reviewed amendment. Retain the existing maximum of one
identical retry only after an infrastructure interruption without a durable
outcome. Hardware retries consume the candidate's 24-attempt allowance; if that
prevents completing the matrix, stop rather than add attempts automatically.
The 1,114 development count denotes distinct scheduled generations, not a
physical-attempt cap: with that same one-retry rule its absolute bound is 2,228
physical attempts per candidate. No wrong-answer, truncation or known-timeout
retry is permitted.

At ordinary 120-second deadlines, 21 normal rows contribute at most 42 minutes
of serial attempt deadlines; two 600-second stress probes add 20 minutes.
The controlled hang, setup, cleanup and exports are additional. First-90 deadline
arithmetic is at most three serial attempt-hours, not a runtime forecast.
Two GPUs can reduce elapsed time; they do not halve allocated device-hours.
Measure actual phase times before predicting completion. Existing historical
GPU-hour ceilings remain observational, as the user already authorized.

If neither candidate passes, export a limited feasibility result with all raw
failures and unknown main coverage. Do not silently add more models, increase
output limits, change populations, retry wrong answers or weaken acceptance.

## 7. Implementation and verification plan

Keep the nine-cell notebook and existing commands. Configuration declares the
reviewed candidate order and stages; the user uploads the small dataset and
clicks Run All. The notebook displays setup progress, current call/phase,
completed versus scheduled slots, timeout/invalid counts and export paths.
Existing checkpoints persist raw replies before effects; identical completed
calls resume without inference. Known terminal failure is explained promptly;
an authorized new configuration has its own source-bound candidate bundle.

Update only the demonstrated boundaries:

| Existing code/artifact | Work |
|---|---|
| `recovery/inference.py` | Reviewed course candidate admission; selected load audit; flushed phase progress; diagnostic bound from validated inputs |
| `recovery/prompts.py` and existing capacity checks | Uniform compact instruction; permitted-view invariants; renewed native-token bound |
| `scripts/m5_course_smoke.py` and preparation helpers | Candidate-specific native inventory; diagnostic deadline; fresh fixed matrix |
| `scripts/course_kaggle_workflow.py` | Correct failure detail, evidence-scoped memory fields, predeclared qualification/fallback and cumulative history |
| Existing bootstrap/build/notebook generators | Small online package, pinned candidate metadata/integrity, exact-source resume, Run All and final exports |
| Existing specification/plan | Explicit approved model/prompt/deadline/attempt scope; implemented versus empirically accepted status |

Do focused CPU checks for the actual loaded generation processors, 9B untied
head/inventory, course limits, unchanged permitted-view transformations, exact
source/input/settings binding, terminal-timeout nonretry, cumulative accounting,
phase-log survival after child termination and honest incomplete-memory reporting.
If prefill changes, verify cache/position/logit equivalence as well. Then execute
the exact generated notebook against deterministic providers through stop,
resume, export and read-only reproduction. Retain unknown main outcomes and
byte-identical original artifacts. Reuse existing tests instead of adding a
second validation framework or repeating unrelated milestone suites.

Actual T4 qualification is a separate authorized stage. CPU meta estimates,
short load success, old 22k-token peaks and public benchmark tables cannot pass
it. After native acceptance, the existing first-90/pilot audits determine whether
the research can proceed. Only then can the notebook legitimately finish with
reproducible empirical main results.

## 8. How future failures should behave

Reuse the current defenses and repair only the demonstrated reporting/progress
gaps. A single Run All needs predictable terminal behavior, including failure:

| Failure class | Required behavior |
|---|---|
| Request, template or generation-processor mismatch | Fail the complete native CPU preflight before weight download or inference. |
| Dependency/version or checkpoint integrity mismatch | Keep exact pins/hashes; bounded transient download retries and verified cache reuse; preserve setup logs and refuse unverified assets. |
| Wrong GPU placement, loading inventory or missing language weights | Fail native load audit before scheduled research calls; preserve device and loading evidence. |
| OOM, nonfinite scores, insufficient full-input headroom | Preserve child phase/traceback and attempt outcome; withhold hardware acceptance and dependent work. |
| Known timeout | Persist terminal failure, stop/confirm the child within cleanup bounds, retain last flushed progress; no automatic retry. |
| Infrastructure/controller interruption without a durable outcome | Recover from the existing ledger; permit only the one exact eligible retry and count both attempts. |
| Invalid or incorrect model reply | Persist the original output before effects; apply normal protocol/scoring rules; never correct or resample it. |
| Session interruption or nearing controller deadline | Stop admitting work, quiesce workers and export supported backups; forced external termination may leave the latest unsaved export unavailable. |
| Changed source/settings/inputs on resume | Refuse cross-configuration continuation; require a normally bound reviewed bundle instead of disabling equality checks. |
| Missing observations or stale derived reports | Rebuild from supplied workers read-only; show unknown coverage and scope each memory/timing claim to its actual probe/session. |

Keep disk/export admission and the existing evidence-preserving setup/cache
behavior. A hard Kaggle kill cannot be made crash-proof by notebook code;
regular durable records and supported exports limit loss and make the remaining
uncertainty explicit. Harmless library warnings should remain available in logs,
while the notebook foregrounds actual stage status and terminal cause.

## 9. Investigation verification and limits

The diagnostic executed on Windows, Python 3.11, Torch 2.11.0+cpu,
Transformers 5.12.0 and the native pinned Rust tokenizer. It verified both ZIP
CRCs, 73 source-member hashes, notebook code AST equality, both SQLite integrity
checks and exact original call/attempt equality; rechecked the valid sorting
answers with an independent mathematical implementation; diagnosed the three
full-information controls from their visible source records; and constructed
both language models with meta tensors only. It fetched the pinned 9B config
and small Hub metadata, verifying revision and config SHA-256. No checkpoint
weights, GPU model calls, new package, freeze, main run or publication occurred.

To reproduce without touching submitted artifacts:

```powershell
.venv/Scripts/python.exe notebooks/validation/course-kaggle/analyse_final_online_4.py --output $env:TEMP/course-final-online-4-analysis.json
```

The command requires the repository CPU environment and internet for pinned 9B
metadata. It refuses to overwrite an existing output. The committed receipt
records all five submitted file hashes. Every native claim above comes from the
submitted evidence; proposed deadlines, configurations and future outcomes are
explicitly unexecuted.
