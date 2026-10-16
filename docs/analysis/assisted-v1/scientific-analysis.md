# Assisted-v1: independent scientific analysis and evidence base

16 October 2026. **Analysis for later report writing; this is not the final course report.** The completed condition is `i01-course-assisted-v2`, study `cbbe6590-00e7-477a-88fc-f6449ea6797c`, under execution policy `i01-assisted-feasibility-2026-10-16`. The directory name “assisted-v1” is an artifact label; it does not change the manifest's scientific regime.

The principal finding is **2/20 exact revised-team successes with retain and 3/20 with clear**, a clear-minus-retain difference of **+5 percentage points**. The exploratory, prespecified stratified paired bootstrap interval is **−15 to +25 percentage points**. The conditions succeed on different worlds; no world succeeds under both. Original collaboration is much better than in Course-7, but reliable recovery is not established. The most characteristic new failures involve repeated legal communication without final commitments, inaccurate extraction from current sources, confusion about whose record a value belongs to, and disagreement between textual reasoning and the submitted integer.

This analysis independently reconstructs evidence from the two canonical databases. It does not accept the generated overview as ground truth. The [executable forensic audit](forensic-reproducibility.md) passes **10,953 record-level assertions with no discrepancies** at the initial complete audit checkpoint. The [complete trace ledger](exhaustive-trace-ledger.md) gives every one of the 356 saved responses, all 28 worlds, all natural episodes and individual case interpretations. Subsequent supplementary checks and their limits are documented with the artifact inventory in the forensic companion. All original files remain preserved.

## Contents and evidence conventions

1. [Question, authority and scope](#1-question-authority-and-scope)
2. [What was executed](#2-what-was-executed)
3. [Execution reconstruction and stage distinctions](#3-execution-reconstruction-and-stage-distinctions)
4. [Main outcomes and uncertainty](#4-main-outcomes-and-uncertainty)
5. [Process, communication and failures](#5-process-communication-and-failures)
6. [Why original collaboration did not yield reliable recovery](#6-why-original-collaboration-did-not-yield-reliable-recovery)
7. [Individual cases and the fixed casebook](#7-individual-cases-and-the-fixed-casebook)
8. [Computational effort and resource accounting](#8-computational-effort-and-resource-accounting)
9. [Critical comparison with Course-7](#9-critical-comparison-with-course-7)
10. [Scientific context and interpretation](#10-scientific-context-and-interpretation)
11. [Limitations and unresolved questions](#11-limitations-and-unresolved-questions)
12. [Reusable claims and reporting guidance](#12-reusable-claims-and-reporting-guidance)

**Verified fact** means a result recomputed from the supplied immutable records, or an explicitly identified property of those records. **Recorded runtime evidence** means a historical measurement/receipt whose internal consistency can be checked now, without re-running its original measurement. **Interpretation** means a reasoned account of observable behavior. **Unresolved** means the artifacts do not identify the answer. Textual explanations are not access to internal model reasoning. This is one AI-assisted review supported by deterministic calculations; no human reviewer, blinded coding panel or inter-rater reliability study is claimed. The preserved annotations table remains empty and historical human-review flags remain pending.

Trace citations use exact persisted IDs. Agent and invocation suffixes are zero-based. The trace ledger supplies direct links to full requests and replies. Audit-derived maxima, hidden source values and scores in these documents were never inserted into model requests.

## 1. Question, authority and scope

### 1.1 The adopted question

[PROJECT_SPECIFICATION.md §12.1](../../../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026) adopts the total practical retain/clear comparison after withdrawing one previously winning record, under one fixed assisted environment. It incorporates the [protocol and acceptance annex](../../../notebooks/run/assisted-v1/latest/source/docs/plans/i01-course-final-design-protocol-and-acceptance.md) for exact instructions, rendering, fixtures, schedule, gates and analysis. The packaged specification is byte-identical to the current root specification.

The comparison concerns **whole visible conversation histories**, including own actions, messages and explicit old submissions. It does not isolate a single stored answer, a particular cognitive bias, or a pure memory operation. Current private sources and the source-change notice are available in both arms. The same assisted system instructions apply from the initial phase onward.

The primary outcome is whether **both agents separately and finally submit the exact revised global maximum**. A correct message, one correct agent, fluent comparison, legal action, completed episode or wrong consensus is insufficient.

### 1.2 Scope of this audit

The audit covers the entire supplied run folder at the byte/inventory level, the executed notebook's 37 code cells and output records, both complete canonical databases, every saved request/outcome and attempt, all 112 episode checkpoints, the archive and release/wheel bindings, raw conversation exports, all CSV/report surfaces, all eight figure pairs, runtime/setup receipts and logs, and scientific documents governing the executed condition. The complete response ledger reads every natural conversation, including ordinary failures and successful episodes with questionable explanations.

Packaged tests and historical implementation evidence are identified as software evidence; their existence is not treated as proof of model competence. Unrelated thesis and legacy source modules are inventoried and identity-checked where packaged, with detailed behavioral inspection concentrated on the executed I-01 call path. This is not a line-by-line re-audit of every unused module or an independent re-execution of the previous software test suites.

Only new Markdown documents are created. No experimental call, model loading, inference, GPU operation, historical annotation mutation, report regeneration in the run folder or source-code change is performed. The explicit user restriction on preserving all existing files takes precedence over ordinary instructions to update the living engineering plan.

### 1.3 What the artifact can and cannot prove

The final ZIP, extracted tree, source manifest, wheel, canonical rows, JSONL exports, request views and reported calculations agree. Every scientific outcome is settled and committed. The reconstruction finds no scoring error, leaked evaluator field, sibling-history contamination, unrecorded continuation reuse, missing required world or favorable-outcome stopping.

These statements concern the supplied evidence. A consistent final snapshot cannot independently prove the historical timing of every transaction, detect work never recorded anywhere, establish an external authorization conversation, certify floating-point kernel correctness, or measure provider allocation/billing. Source inspection corroborates persist-before-effects, idempotent exact-request resume and bounded admission; no crash or retry occurred in this campaign to test those paths empirically.

## 2. What was executed

### 2.1 Frozen condition

| Component | Executed value / verified meaning |
|---|---|
| Model | Qwen/Qwen3.5-9B |
| Checkpoint revision | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` |
| Source release | `d95bb01223590bb889d4612199662266ce78968d` |
| Task | Two private shards, 20 integers each, values in [−1000,1000]; global maximum |
| Natural phases | One original prefix, then isolated retain and clear siblings |
| Per-agent opportunities | At most three calls in each phase; at most six team calls |
| Decoding | Direct/nonthinking; sampling temperature 0.7, top-p 0.8, top-k 20 |
| Other generation settings | Repetition penalty 1; presence penalty 0; one beam; fresh cache per call |
| Limits | 8,192 input tokens; at most 512 generated output tokens; 180 s direct deadline |
| Runtime | Text-only NF4 double quantization, FP16; reviewed T4 attention path; prefill chunk 256 |
| Hardware | Two distinct Tesla T4 devices; one resident replica per logical worker |
| Scientific data | Four qualification worlds, four pilots, twenty main worlds |
| Master seed | `2026101601` |
| Primary uncertainty | 10,000 stratified paired bootstrap draws; seed `2026101602` |
| Physical budget | 480 ordinary first-attempt capacity + 20 contingency; hard ceiling 500 |
| Actual spending | 356 first attempts; zero retries, contingency charges or unresolved attempts |

The request settings, not a model's generic load-time generation configuration, establish actual decoding. All ordinary saved requests share the same settings. A load receipt's default `max_new_tokens=256` does not contradict the persisted per-call maximum of 512, which the adapter explicitly installs before generation. Configuration retains inactive legacy thinking limits; every executed request is direct, and no private thinking is saved or passed forward.

The runtime receipt records Python 3.13.15, PyTorch 2.11.0+cu128, Transformers 5.12.0, bitsandbytes 0.49.2, tokenizers 0.22.2 and accelerate 1.14.0. These are records of the Kaggle environment, not descriptions of the local analysis host. The recurrent fast path is recorded as false, consistent with the selected reviewed execution path rather than evidence of a fallback model.

### 2.2 World generation and assignment

For each world, uniform integer proposals are drawn from a separate identity-derived stream. A proposal must have a unique old maximum, a remaining maximum above −1000, and the scheduled winning-record owner. The winning record is replaced uniformly below the largest remaining value. Thus every world genuinely changes its global maximum; a correct old answer is necessarily wrong after revision.

Independent regeneration reproduces every input, replacement, proposal count, rejection counter, invocation seed and assignment. There are 48 proposals for 28 accepted worlds, with 20 owner-block rejections, zero nonunique-maximum rejections, zero remaining-at-floor rejections, and a maximum of eight proposals for any world. These are mathematical/assignment exclusions before inference, not filtering by model performance.

All 56 ordered original/revised whole inputs are distinct from one another and from the 60 distinct locally exposed historical/native inputs checked by the release. The historical runs repeatedly use the same underlying 29-world set; their file count does not imply hundreds of distinct prior worlds. Exact whole-input disjointness does not claim disjoint individual integers, records or model pretraining data.

The main list interleaves four owner/first-speaker strata, with five worlds per stratum. Main indices satisfy `i=4*k+s`, `s=2*owner+first`. First speaker stays the same across original and both recoveries. Independently shuffled device/order assignments give:

| Assignment feature | Main count |
|---|---:|
| Owner 0 / owner 1 | 10 / 10 |
| First speaker 0 / first speaker 1 | 10 / 10 |
| Device 0 / device 1 | 10 / 10 |
| Retain physically first / clear physically first | 10 / 10 |
| Each joint (device, first-policy) combination | 5 |

Every owner/first-speaker stratum includes both orders on both devices, with the declared unavoidable 2/3 imbalances. Both siblings of a world use its same device. The ten batches are the fixed consecutive pairs 00–01 through 18–19; worlds sharing a device are serialized. All call admission/finish timestamps agree with within-world phase order and same-device nonoverlap.

Seven main worlds transfer the revised winner to the unchanged agent: 00, 02, 07, 08, 14, 15 and 17. This is a descriptive property of the fixed cohort, not a selected subgroup or extra experimental arm.

### 2.3 Literal information and protocol boundaries

At each natural call the model receives its current shard, its own visible history, own-call counter, partner-finished status, and, in recovery, the changed owner and record index. Only the owner receives the replacement value. Neither receives the other's private shard or submission, private gold, world/group/arm labels, hidden winner-withdrawal eligibility or future edits. A numeric old answer can appear legitimately in retained history; the host does not reissue the before-value as authoritative current evidence.

Retain copies the actual prefix history, including incorrect reports and explicit old submissions. Clear starts with empty histories. Both reset turns, submissions and waiting flags. Earlier-phase boundaries are saved literally, not inferred later from prose. Each sibling starts independently from the prefix; the second arm never inherits messages, submissions or current-phase history from the first.

The I-01 protocol is a sequential alternating eligible-call state machine. A completed legal message is delivered before the next eligible call, and a send-and-submit action delivers before finality. This differs from the thesis four-peer synchronous-round regime; imposing that older regime on these traces would be a scientific error. The adopted I-01 contract governs.

An action must contain exactly `message`, `submit`, and `wait` with strict types. Wait must be alone; an empty non-wait action is illegal. An invalid action consumes a call and delivers nothing. Public rejection feedback explains the violated action rule without checking numerical truth. Submission is private unless explicitly messaged and irreversible within the phase. Waiting wakes only on a delivered message. When a partner has finished, waiting can deadlock even if only one agent is waiting.

## 3. Execution reconstruction and stage distinctions

### 3.1 Chronology

All artifact times below are UTC; add two hours for Budapest on 16 October 2026.

| Stage / boundary | Recorded time | Evidential interpretation |
|---|---|---|
| First notebook code cell | 14:16:26.094 | Start of the observed notebook span |
| Study manifest creation | 14:19:23.516 | New independent study initialized |
| Implementation/native selfcheck receipt | 14:19:40.443 | Scripted checks before model calls |
| First / second model loaded | 14:23:22.210 / 14:23:56.015 | Two resident replicas |
| Execution plan cell | 14:23:59–14:24:02 | Fixed plan before the first model call |
| First state-check admission | 14:24:02.097 | Start of physical model-attempt ledger |
| Qualification scalar controls | 14:24:19.870–14:24:38.964 | Eight one-call complete-input controls |
| Last forced envelope settles | 14:26:57.023 | Full input/output hardware envelope checked |
| Four diagnostics | 14:26:59.861–14:27:24.140 | Single supplied-view calls |
| Natural pilot calls | 14:27:30.227–14:33:32.577 | Four complete pilot scopes |
| Main eligibility/freeze record | 14:33:39.756 | Pilot usefulness and resources accepted |
| Main calls | 14:33:43.857–14:53:52.635 | All twenty intended worlds |
| Main batch-10 cell ends | 14:54:07.645 | Includes final batch export/inspection |
| Both worker terminations confirmed | 14:54:24.896 / 14:54:25.252 | Model worker processes stopped |
| Last notebook cell ends | 14:54:41.757 | Observed notebook completion |

All 37 code cells have consecutive execution counts 1–37, no Jupyter error output, and source identical to the packaged notebook. Its approximate 38.26-minute span is not an independently measured provider allocation. Finite action cells and all ten batches complete. The final shutdown output states that controller process exit is not yet confirmed; worker exit receipts are stronger, explicit evidence for the two model workers. GPU allocation release remains unknown.

The final ZIP is an intact snapshot. Metadata records 53 successful checkpoint exports and notebook outputs show intermediate export receipts. Those intermediate ZIP generations are not all preserved individually in this folder. Their existence/duration is recorded, but this audit can independently hash and reopen only the supplied final ZIP and surviving records.

### 3.2 Hardware readiness is not scientific success

Six A–B–A state checks, three per device, produce their expected scalar answers. For each device A1 and A2 have identical saved requests, seeds, raw answers and token IDs despite the intervening B call. This is bounded evidence against simple state carryover; it cannot prove isolation for all possible hidden backend behavior.

Two synthetic envelopes deliberately pad input to 8,192 tokens and force 512 generated tokens, overriding normal early EOS stopping. Their length termination, repetitive special-token-containing raw continuations and empty scientific visible output are intentional probe behavior. They are not two failed natural actions. The measured minimum free headroom across saved call observations is 7,280,066,560 bytes, about 6.78 GiB, well above the 1.5 GiB gate. Observed memory sampling cannot certify every instantaneous allocation, but no recorded headroom, cache, finite-score or provider defect occurs.

All scientific replies stop at EOS. Maximum scientific output length is only 124 tokens, and scientific input lengths range from 245 to 1,318 tokens. The current recovery failures therefore do not have recorded truncation, output-cap exhaustion, input-cap exhaustion or timeouts as their proximate explanation. This does not prove the model's numerical implementation is infallible.

### 3.3 Qualification: correct scalar execution, limited transfer

All eight qualification controls are legal, committed and exactly correct: original/revised truths 964/937, 943/925, 987/986 and 929/907. They consume 18.838417 ready-model seconds and 128 generated tokens.

These requests give a single model all 40 integers, use a short scalar system instruction, require no communication, expose no partner status or source notice, and permit a single final answer. They do not test shared-source ownership, scheduling, history use, message uptake or two separate commitments. Accuracy is diagnostic under the adopted protocol-first qualification policy; eight correct outcomes do not estimate reliability over future seeds or guarantee recovery.

### 3.4 Diagnostics: one pass, three different nonpasses

| Fixture | Supplied situation and exact target | Actual response | Result |
|---|---|---|---|
| D00 | Empty initial view; appended instruction to message exactly “ready” | Reports local maximum 964 in explanatory text | Legal action; exact directive missed |
| D01 | Original exchange already supplied; partner finished; submit global 943 | Messages comparison and submits 943 | Pass |
| D02 | Reopened changed owner; correct old peer report 907 remains useful; submit 907 | Messages its correct current local maximum 829, no submission | Target behavior absent |
| D03 | Clear nonowner; appended instruction to message current local maximum 986 | Messages 107 | Correct output form; wrong source computation |

Exact calls are `qualification-00/diagnostic-D00`, `qualification-01/diagnostic-D01`, `qualification-03/diagnostic-D02`, and `qualification-02/diagnostic-D03`. D03's 107 is at record 14 in the actor's own shard; it is not the notice's record index 2 or its own value at record 2. Calling it a literal “notice-index answer” would overstate the evidence.

D02 is especially informative: the model extracts its current local maximum correctly but does not use the still-valid historical peer maximum to make the required global commitment. It does not prove that a later ordinary turn would also fail. D00 and D03 have special appended directives, so their nonpasses cannot be interpreted as ordinary action-schema violations. All four diagnostics are legal and all settle. Their aggregate 1/4 pass count has no prespecified numerical admission threshold.

### 3.5 Pilots: complete and useful originals, failed recovery

| Pilot | Original global success | Original/revised scalar controls | Retain final submissions | Clear final submissions |
|---|---:|---|---|---|
| 00 | 1 | 938 / 898, both correct | [null,null] | [898,648] |
| 01 | 1 | 984 / 952, both correct | [null,755] | [952,755] |
| 02 | 1 | 978 / 944, both correct | [685,841] | [944,null] |
| 03 | 1 | 876 / 784, both correct | [null,784] | [784,660] |

All eight recovery episodes fail exact team success. All 50 pilot team actions are legal, and all 58 pilot-stage calls settle and commit. The original teams are 4/4 correct and scalar controls 8/8 correct. The objective main gate requires at least 3/4 correct originals, at least 7/8 correct controls, complete terminal pilot evidence, reconciled exports/spending and current health/resources. It **does not require a successful recovery, a favorable policy difference, or qualitative approval of messages**. Main admission is therefore consistent with the adopted rule despite plainly poor recovery.

Pilot “passed” fields describe durable scope/health checks, not correct recovery. The saved feasibility result is consistent with the raw states. No pilot is omitted, repeated or substituted, and no parameter tuning follows these outcomes. Reporting this as a failed reliability certification would invent a gate the study did not adopt; reporting it as evidence of reliable recovery would be equally wrong.

The pilot-to-main difference is not in-context learning across worlds: backend state is reset and earlier-world conversations are absent from later requests. Different fixed inputs, seeds and realized interactions can produce different success counts. Four perfect pilot originals followed by 10/20 main originals illustrate the limits of a small development sample.

## 4. Main outcomes and uncertainty

### 4.1 Exact twenty-world table

`B` = both submitted; `H` = horizon exhausted; `W` = waiting deadlock. Null is known absence in a terminal episode. The full inputs and every response are in the trace ledger.

| World | Old → revised truth | Original submissions | Retain submissions / terminal | Clear submissions / terminal | Revised scalar control |
|---|---|---|---|---|---:|
| 00 | 943 → 922 | [943,943] | [null,null] H | [922,922] B | 922 |
| 01 | 956 → 931 | [956,956] | [931,931] B | [null,931] H | 931 |
| 02 | 976 → 964 | [976,976] | [964,964] B | [964,null] H | 964 |
| 03 | 946 → 893 | [null,946] | [810,893] B | [876,null] H | 893 |
| 04 | 972 → 954 | [972,972] | [null,839] H | [954,null] H | 954 |
| 05 | 952 → 884 | [952,868] | [884,null] H | [884,868] B | 884 |
| 06 | 941 → 917 | [941,941] | [917,null] H | [766,null] H | 917 |
| 07 | 991 → 980 | [991,991] | [null,null] H | [null,980] H | 980 |
| 08 | 874 → 857 | [874,874] | [null,null] H | [786,786] B | 857 |
| 09 | 979 → 949 | [979,836] | [949,836] B | [949,836] B | 949 |
| 10 | 991 → 987 | [878,991] | [null,987] H | [878,987] B | 987 |
| 11 | 984 → 950 | [null,984] | [null,950] W | [950,null] H | 950 |
| 12 | 963 → 905 | [963,null] | [null,null] H | [null,null] H | 905 |
| 13 | 992 → 873 | [992,992] | [873,864] B | [873,864] B | 873 |
| 14 | 980 → 975 | [980,980] | [975,null] H | [975,null] H | 975 |
| 15 | 917 → 815 | [815,917] | [null,null] H | [815,815] B | **881, wrong** |
| 16 | 702 → 601 | [702,null] | [601,500] B | [601,500] B | **585, wrong** |
| 17 | 974 → 955 | [974,955] | [663,955] B | [null,955] H | 955 |
| 18 | 961 → 912 | [961,961] | [805,805] B | [764,805] B | 912 |
| 19 | 931 → 896 | [860,931] | [null,null] H | [896,896] B | 896 |

### 4.2 Paired primary result

| Paired category | Worlds | Exact IDs |
|---|---:|---|
| Both correct | 0 | None |
| Retain only | 2 | 01, 02 |
| Clear only | 3 | 00, 15, 19 |
| Neither correct | 15 | 03–14 except already listed, plus 16–18 |
| Unknown pair | 0 | None |

For each intended world `D_i=C_i−R_i`. There are three +1, two −1 and fifteen zero differences, giving `sum(D_i)/20=(3−2)/20=0.05`. Complete coverage makes missingness completion bounds exactly [0.05,0.05]. These bounds describe the known cohort, not sampling uncertainty.

The adopted bootstrap sorts the four owner/first-speaker strata lexicographically, orders their five worlds by index, samples five complete paired worlds within each stratum, and averages twenty paired differences. With 10,000 draws and seed 2026101602, sorted indices 250 and 9750 give [−0.15,0.25]. Each stratum has some nonzero contrast, so none is constant and the primary interval is not degenerate.

The interval contains zero and substantial effects in both directions. It does not establish clear superiority, no effect, equivalence, statistical power, calibrated small-sample coverage or reliability over repeated model generations. A single world's success change moves a policy rate by five points. The realized cohort contrast is exactly known; its expected value for new worlds and seeds is not.

### 4.3 Descriptive strata

| Changed owner, first speaker | N | Original correct | Retain correct | Clear correct | Clear−retain |
|---|---:|---:|---:|---:|---:|
| 0,0 | 5 | 3 | 0 | 1 | +20 pp |
| 0,1 | 5 | 2 | 1 | 0 | −20 pp |
| 1,0 | 5 | 4 | 1 | 0 | −20 pp |
| 1,1 | 5 | 1 | 0 | 2 | +40 pp |

These sparse cells describe heterogeneity; they do not establish speaker/owner interactions. Device 0 has 1 retain and 1 clear success; device 1 has 1 retain and 2 clear successes. Worlds assigned clear-first have 7/10 correct original prefixes, whereas retain-first worlds have 3/10, even though neither recovery order has occurred when a prefix is generated. That imbalance cautions against attributing subgroup differences to physical arm order. The design balances assignments, not every realized outcome.

### 4.4 Correct-prefix recovery

Ten main prefixes are exactly correct: 00, 01, 02, 04, 06, 07, 08, 13, 14 and 18. Among them retain recovers on 2/10 (01,02), clear on 1/10 (00). Both other clear successes, 15 and 19, start from incorrect original teams. The adopted contract allows **descriptive counts only** for this subset; no conditional bootstrap or separate inferential claim is supplied.

A correct old team is helpful evidence about original collaboration, but it is not a certificate that all earlier reports were accurate or that either recovery will be correct. Pilot-00 succeeds originally despite an inaccurate subordinate local maximum. Main-00's correct prefix includes a verbally incorrect comparison while the committed integer is correct.

### 4.5 Controls and natural outcomes disagree in informative ways

Main revised scalar controls succeed on 18/20. Main-16 selects 585 rather than the visible 601; main-15 generates 881, absent from its complete input, rather than 815. These are legal scalar mistakes, not scoring errors or missing outcomes.

Clear nevertheless solves main-15. A scalar control's single realized answer is not a deterministic capability ceiling or latent certificate for that world. Conversely, 18 correct controls coexist with very poor distributed recovery. The conditions differ in information distribution, prompt length/structure, conversation, decisions and invocation seed. They do not isolate “communication cost” or support subtracting control accuracy from recovery accuracy as a causal decomposition.

## 5. Process, communication and failures

### 5.1 Separate syntax, action legality, completion and correctness

All 348 scientific responses are valid JSON with valid field types. Six actions violate the mutually exclusive wait rule. All six are message-plus-wait, with no submission; their message text is preserved for audit but never delivered. There are no empty non-wait, framing, provider or scientific truncation failures.

| Main phase | Calls | Legal actions | Delivered messages | Correct team /20 | Both submitted /20 |
|---|---:|---:|---:|---:|---:|
| Original | 82 | 81 | 70 | 10 | 16 |
| Retain | 91 | 90 | 85 | 2 | 8 |
| Clear | 85 | 81 | 77 | 3 | 10 |

Across all natural pilot and main team calls, 302/308 actions are legal. The remaining 40 scientific responses are 36 controls and four diagnostics, all legal. Ordinary action illegality is now uncommon, but terminal success remains low.

Exact illegal calls:

- `main-03/clear/agent-0/invocation-0`
- `main-03/clear/agent-1/invocation-1`
- `main-03/clear/agent-0/invocation-1`
- `main-05/prefix/agent-1/invocation-0`
- `main-17/retain/agent-1/invocation-0`
- `main-18/clear/agent-1/invocation-0`

The three main-03 clear violations occur despite reason-specific feedback on later eligible turns. They consume scarce calls and prevent useful messages from reaching the partner. Yet **17 of 18 failed retain episodes and 15 of 17 failed clear episodes contain no illegal action**. Thus 32/35 failed main recoveries are entirely legal at the action level. This is an observable overlap, not a causal percentage attribution.

### 5.2 Final submission coverage

| Main phase | Intended agent slots | Correct final integers | Wrong final integers | Known absent | Unknown |
|---|---:|---:|---:|---:|---:|
| Original | 40 | 30 | 6 | 4 | 0 |
| Retain | 40 | 14 | 8 | 18 | 0 |
| Clear | 40 | 18 | 11 | 11 | 0 |

The correct individual-submission counts are useful secondary evidence, but do not replace the both-agent endpoint. A complete-case accuracy among submitted answers would discard 18 retain and 11 clear slots and give a misleadingly favorable impression of recovery.

Retain's 18 failed episodes comprise 12 noncompletions and six completed-but-wrong teams. Clear's 17 failed episodes comprise ten noncompletions and seven completed-but-wrong teams. This is a mutually exclusive description of terminal states, not an estimate of which mechanism caused the failure.

### 5.3 Legal action distributions and conversational stalling

| Main phase | Message only | Message + submit | Submit only | Wait alone | Illegal |
|---|---:|---:|---:|---:|---:|
| Original | 41 | 29 | 7 | 4 | 1 |
| Retain | 65 | 20 | 2 | 3 | 1 |
| Clear | 51 | 26 | 3 | 1 | 4 |

Retain has more delivered messages and more calls than clear but fewer completed and correct teams. Communication volume alone is not successful coordination.

Using literal message equality within each (episode, sender), delivered-message counts minus distinct message strings are 3 original, 31 retain and 18 clear. Thirteen retained agent trajectories send the exact same message on all three own calls, versus four clear trajectories. These counts are deterministic string facts, not a semantic “loop detector”; punctuation changes can hide repetition and repeated text can sometimes be useful.

The clearest retained full-team loops are 00, 07, 08, 12, 15 and 19, each ending [null,null] after six calls. Clear has one such no-submission world, 12. In main-08 retain, both revised maxima are correctly reported on the first exchange and repeated; no stale value is submitted and no action is illegal, but neither agent commits. In main-19 retain the repeated reported maxima 896 and 860 are also correct. The missing behavior is finalization after available information, not a missing source-change notice.

Saying “I will wait” inside `message` with `wait:false` remains an ordinary message and does not suspend the sender. Conversely, `wait:true` alone really blocks until a new message. Main-06 retain illustrates real waits that wake after partner messages; main-11 retain illustrates a legal wait that cannot wake after the other agent has finished.

### 5.4 Source extraction and ownership confusion

A deliberately narrow lexical audit finds explicit own-maximum claims in 70 original, 85 retain and 77 clear main calls. Of those, 3, 14 and 9 respectively contain at least one number unequal to the actor's exact current local maximum. These occur in 2, 8 and 5 worlds. The match rule is documented in the verifier and ledger; it does not cover all phrasings, score invalid undelivered text as delivered, or diagnose an internal cause.

Some errors merely understate a losing shard and leave the global answer unaffected; others remove the true global maximum from the effective conversation:

- `main-04/retain/agent-0/invocation-0`: claims 601 despite a current local 954. The partner later submits 839.
- `main-08/clear/agent-1/invocation-0`: claims 786 despite 857, leading to wrong agreement on 786.
- `main-18/retain/agent-1/invocation-0`: reports/submits 805 despite 912; the partner follows it.
- `main-19/prefix/agent-1/invocation-0`: initially misses the old 931 and reports 896, then later corrects. A wrong intermediate report is not always terminal failure.

Several remote claims equal numbers in the actor's own shard at a partner-mentioned record location:

| Exact call | Observable statement / numerical provenance | Why it matters |
|---|---|---|
| `pilot-01/retain/agent-1/invocation-0` | Says owner's maximum is 409; own record 7 is 409; changed remote record is 7 | Uses a locally available number as a remote claim before a fresh owner report |
| `main-09/clear/agent-1/invocation-1` | Says remote maximum is 695 at record 13; own record 13 is 695; remote report was 949 | Disregards delivered current report and matches notice location to own source |
| `main-12/clear/agent-1/invocation-0` | Calls 92 its maximum; own record 6 is 92; notice names the other agent's record 6 | Treats a particular local location as salient despite own maximum 851 |
| `main-13/clear/agent-1/invocation-0` | Says partner record 9 changed to 397; own record 9 is 397; true remote replacement is −509, not disclosed to it | Directly asserts private remote replacement information that the request does not supply |
| `main-16/retain/agent-1/invocation-2` | Replaces received remote maximum 601 at record 17 with 11 at record 17; own record 17 is 11 | Correct report is visible, then a local-location substitution accompanies wrong final 500 |
| `main-18/clear/agent-0/invocation-1` | Says remote changed record 4 has value 199; own record 4 is 199; actual remote replacement is −473 | Same pattern persists without earlier-phase history |

These exact numerical correspondences support an **interpretation of source/agent ownership confusion**. They do not prove a single hidden attention mechanism. Some other false remote maxima are simply values elsewhere in the speaker's own source: main-02 retain's 940 is its own record 13; main-14 retain's 858 is its own record 19. Their indices should not be falsely described as the notice indices 19 and 2.

The environment's record number is a location, and a peer's claimed location belongs to that peer's private shard. Explicitly stating this distinction in the assisted prompt does not ensure the model uses it correctly.

### 5.5 Textual reasoning and committed action

Exact examples show why explanations cannot substitute for action scoring:

| Call | Textual content | Actual commitment |
|---|---|---|
| `main-15/prefix/agent-0/invocation-1` | Recognizes partner 917 exceeds own 815 | Submits 815 |
| `main-19/prefix/agent-0/invocation-1` | States 860 < 931 | Submits 860 |
| `main-10/retain/agent-0/invocation-1` and `invocation-2` | Identifies 987 as global | Submit remains null |
| `main-04/clear/agent-1/invocation-2` | States 954 is global and says it will submit | Submit remains null |
| `main-11/retain/agent-0/invocation-0` | Names 950 as larger and says it is submitting | Submit remains null; later waits |

The state machine correctly preserves these literal outcomes. Repairing a null or wrong submit field from prose would change the experiment after the fact. The same caution applies to successful calls: main-00's original last explanation is verbally inconsistent while its submitted 943 is correct.

### 5.6 Finality and partner-finished status

After one agent submits, its private value is not automatically disclosed and it cannot revise within the phase. Its explicit message can still give the partner all necessary information; finality is not itself evidence that information is unavailable.

There are 21 original, 19 retain and 24 clear main calls with partner-finished true. Respectively 5, 11 and 14 of these are legal actions with null submission. They include repeated requests, waiting and incomplete commitments. These are call-level descriptive counts with behavior-dependent denominators.

Main-01 clear and pilot-03 retain demonstrate a partner continuing without finalizing after receiving a useful current message. Main-17 retain demonstrates an early wrong final commitment that cannot later be repaired by the correct partner. No additional turn, public submission value or semantic guard is silently supplied.

### 5.7 Locally refutable and obsolete submissions

Three retained and two clear main submissions are below a value in the actor's own authoritative current shard:

| Policy | Call | Submitted | Own current maximum |
|---|---|---:|---:|
| Retain | `main-03/retain/agent-0/invocation-1` | 810 | 876 |
| Retain | `main-17/retain/agent-0/invocation-0` | 663 | 819 |
| Retain | `main-18/retain/agent-1/invocation-0` | 805 | 912 |
| Clear | `main-08/clear/agent-1/invocation-1` | 786 | 857 |
| Clear | `main-18/clear/agent-1/invocation-1` | 805 | 912 |

These are a strict lower bound on observable numerical inconsistency: an answer can be wrong without being locally refutable, because the larger value lies in the other private shard. The intended denominator is forty agent slots per policy, with present/absent coverage reported separately.

There are **zero retained and zero clear main submissions equal to the withdrawn old global maximum**. Earlier incorrect reports and obsolete submissions still exist in retained prompt history, but they do not become final recovery answers here. This sharply differs from Course-7. It does not establish the absence of any history effect: retained behavior can still repeat ineffective strategies, current-source mistakes or commitment failures.

Clear also removes the unique old answer from current sources and old visible history. Thus a retain/clear obsolete-answer comparison has asymmetric old-value availability; zero clear repetition is not proof of resistance to anchoring. In this run zero retain repetition is a real additional observation, but not a causal demonstration that assistance removed a cognitive bias.

### 5.8 Agreement can be wrong

Retain agreement occurs in three worlds: the two successes and wrong agreement [805,805] in 18. Clear agreement occurs in four worlds: the three successes and wrong agreement [786,786] in 08. The original phase has ten agreements, all correct.

Wrong consensus can arise after a false local report and its uptake even when a larger source value remains visible to one of the agents. Agreement therefore neither certifies correct source integration nor eliminates individual extraction error.

## 6. Why original collaboration did not yield reliable recovery

### 6.1 A chain of requirements replaces a single scalar computation

Original success requires enough accurate local extraction, exchange, comparison and two final commitments for that realized history. Recovery adds a new notice, changed source, reopened counters, still-useful unchanged information and potentially obsolete earlier text. These are jointly required behaviors. Improvement in one part of the chain does not imply improvement in every part.

The observed main original-to-recovery success rates fall from 50% to 10% retain and 15% clear. This is a descriptive difference between distinct phases and inputs; without no-change continuations it is not a causal estimate of the damage caused specifically by a revision. The correct-prefix table is stronger descriptive evidence that previously successful collaboration often fails on reopening, but it still does not identify why.

### 6.2 Removing one failure pattern leaves others

Compared with Course-7, illegal messaging and obsolete final answers are much less common or absent. Yet both current policies frequently fail with entirely legal actions and no obsolete submission. That narrows the explanation: neither “the parser rejected most communication” nor “agents simply kept submitting the old answer” accounts for the current main cohort.

The traces show at least four persistent requirements that the assistance does not make reliable:

1. **Extract all relevant current values.** Main-04 retain and main-18 both miss a visible larger local value; D03 fails even a direct local-source message query.
2. **Maintain source ownership.** Notice locations and peer record references are sometimes projected onto the actor's own array.
3. **Use available evidence in the action.** Main-10 retain identifies the correct global value without committing it; main-15 original recognizes a larger peer value but submits its own.
4. **End both agents' work.** Main-08 and main-19 retain have correct current local reports but no final submission from either agent.

These observations can overlap in one trace. No percentages are assigned to mutually exclusive “root causes,” and no claim is made that fixing one observed error would necessarily have yielded a correct counterfactual trajectory.

### 6.3 Historical information is available without being used well

Retain preserves useful evidence about the unchanged peer, as well as potentially misleading old conclusions. The public rule states only the named record changes, so an unchanged peer's genuinely correct earlier source report can remain useful. Old claims are not certified, and a correct old team can contain an inaccurate subordinate report.

Retain success on main-01 is consistent with productive use of a still-valid 926 peer report together with a current 931 update. Main-02 also succeeds, but a later wrong remote value demonstrates that successful commitment does not certify faithful historical reasoning. D02 supplies an unusually favorable, correct old peer history and still does not elicit the target immediate global submission.

In many unsuccessful retained cases the agents re-exchange local maxima anyway, then repeat the exchange. History may influence this repeated action pattern, but the available data cannot distinguish strategic imitation, action-form persistence, source extraction difficulty, prompt interpretation or stochastic variation as separate causes. Calling these loops “behavioral anchoring” is a hypothesis, not an established mechanism.

### 6.4 Clear is also a recovery task

Clear erases earlier derived work but does not erase the source-change notice or the fact that the phase is reopened. It therefore differs from an ordinary initial episode, even when its history is empty. Main-13 clear invents a remote replacement; main-12 clear emphasizes the actor's own value at the notice index; pilot-01 clear continues using incorrect remote record values despite a correct delivered report.

Consequently poor clear performance cannot be blamed solely on stale retained text. Conversely a clear success does not isolate “forgetting helps”: it can also reflect differences in prompt length, history content, available evidence, message choices and generated sequence.

### 6.5 Formal success can rest on inaccurate premises

Main-19 clear succeeds in two calls even though its first speaker invents a remote maximum of 639; 639 is in that speaker's own shard and the true remote maximum is 860. Since 896 exceeds both, the incorrect premise does not change the committed result. Main-02 retain similarly succeeds despite a wrong later remote maximum.

The exact endpoint properly credits the correct answers. A methodology/discussion section should additionally state that such successes are insufficient evidence of robust reasoning or reliable source tracking. Conversely, pilot-02 clear broadcasts 944 correctly once and produces one correct submission but still fails as a team. Content-level progress and final joint success are distinct.

### 6.6 What the pilots warned about

The diagnostics and pilots already exhibit current-source computation error, unused historical evidence, source-location projection and failure to finalize after useful messages. The main findings extend those observed patterns; they are not an entirely new kind of failure emerging only after admission.

The main gate deliberately measures whether the fixed course study can produce interpretable original collaboration and complete evidence, not whether recovery is already good. Its successful admission is compatible with the scientific question having a largely negative answer about practical reliability. There is no evidence of hidden live tuning, favorable replacement worlds or recovery-based gate relaxation.

## 7. Individual cases and the fixed casebook

The prescribed six-category casebook uses the lowest-index qualifying main world, phase order prefix/retain/clear and stored event order. Independent reading agrees with the retained case selection:

| Category | Selected world / exact event | Status |
|---|---|---|
| Illegal action | 03, `main-03/clear/agent-0/invocation-0` | Present |
| Locally refutable recovery submission | 03, `main-03/retain/agent-0/invocation-1` | Present |
| Retained obsolete answer | None | Absent |
| Clear-only success | 00 | Present |
| Retain-only success | 01 | Present |
| Both success | None | Absent |

For policy-success categories the saved `selected_call` is the first prefix event of the chosen world, serving as its context entry point; it is not itself a recovery success event. Actual success is established by the terminal recovery submissions. This distinction avoids misleading isolated quotations.

The full ledger interprets every pilot and main world, not only the deterministic casebook. Particularly useful additional cases for later report discussion are:

- **08:** correct original; correct retained local reports but no finalization; clear wrong consensus after a false local maximum.
- **09 and 13:** identical final disagreements in both policies, with local-value/remote-location confusion visible under different histories.
- **10 and 11:** correct global prose paired with null or wrong commitments, followed by horizon exhaustion or waiting.
- **15:** clear recovery succeeds although its scalar control hallucinates an absent number.
- **16:** both arms disagree and the scalar control is also wrong, but in distinct ways.
- **18:** retained wrong agreement follows a false owner report; clear also exhibits source-location substitution.
- **19:** retained report loop versus a fast clear success that nevertheless includes a false remote premise.

These are exploratory explanatory cases, not additional preselected categories or a statistical failure taxonomy. All numerical observations remain inspectable by exact ID.

## 8. Computational effort and resource accounting

### 8.1 Physical campaign cost

| Physical stage | Attempts | Ready-model seconds | Input tokens | Generated tokens |
|---|---:|---:|---:|---:|
| Hardware/state and envelopes | 8 | 149.257140 | 16,790 | 1,112 |
| Qualification scalar controls | 8 | 18.838417 | 2,062 | 128 |
| Four diagnostics | 4 | 24.145502 | 3,618 | 157 |
| Pilots, including controls | 58 | 340.318541 | 52,229 | 2,222 |
| Main, including revised controls | 278 | 1,641.773157 | 262,698 | 10,073 |
| **Total** | **356** | **2,174.332757** | **337,397** | **13,692** |

Summed dispatch time is 2,176.601758 s. All effort fields are observed; none is silently replaced with zero. Both model loads sum to 90.247900 s. Loads and downloads consume real wall time but are not generation attempts. Hardware envelopes contribute 1,024 generated tokens for headroom testing; these are not scientific answer tokens.

Worker 0 has 182 calls and 1,106.899878 ready-model seconds; worker 1 has 174 calls and 1,067.432878 s. The two workers use local `cuda:0` under different `CUDA_VISIBLE_DEVICES` settings and distinct device UUIDs; the common local index is not accidental sharing of one GPU.

Unused capacity is 124 ordinary first-attempt slots plus 20 unused contingency slots = 144 below the 500 ceiling. Early episode termination, rather than omitted worlds, explains spending below the worst-case 480. Capacity is not permission to add more worlds, repeat seeds or repair failures.

### 8.2 Principal paired recovery effort

| Main recovery metric | Retain total / mean | Clear total / mean | Mean clear−retain |
|---|---|---|---:|
| Calls | 91 / 4.55 | 85 / 4.25 | −0.30 |
| Ready-model seconds | 588.777817 / 29.438891 | 513.114911 / 25.655746 | **−3.783145 s** |
| Input tokens | 102,922 / 5,146.10 | 80,352 / 4,017.60 | −1,128.50 |
| Generated tokens | 3,411 / 170.55 | 3,194 / 159.70 | −10.85 |
| Delivered messages | 85 / 4.25 | 77 / 3.85 | −0.40 |

The principal effort interval is **−8.240557 to +0.588860 seconds per world**, calculated with the same prescribed stratified paired resampling and a freshly initialized seed. All twenty effort pairs are complete. The mean observed reduction is about 12.85% of retain's mean recovery time, but the interval includes zero and no general efficiency advantage is established.

Recovery costs include unsuccessful episodes and rejected actions. A fast wrong commitment or early waiting deadlock can be cheap; a legal report loop can be expensive. Main-16 clear takes 15.106966 s and ends [601,500]; retain takes 42.135935 s and ends with the same wrong disagreement. The largest positive clear−retain difference is main-11, about +15.57 s, where retain deadlocks early while clear continues to the horizon. Such timing differences must be interpreted with outcomes and termination.

The 82 main prefix calls execute once physically. Their 493.775462 ready-model seconds and 3,148 generated tokens are charged logically to each hypothetical end-to-end policy:

- Retain: 82+91 = 173 logical calls; 1,082.553279 ready-model seconds; 6,559 generated tokens.
- Clear: 82+85 = 167 logical calls; 1,006.890373 ready-model seconds; 6,342 generated tokens.

Adding both logical totals would double-count the shared physical prefix. Controls, diagnostics and hardware are research cost, not distributed-policy cost.

### 8.3 Forecasts, timing and allocation limits

At main admission the largest completed ordinary ready time is 14.743357 s. The selected margin gives `c=1.25*M+5=23.429196 s` per remaining worst-case call. With `N=380`, measured checkpoint maximum 3.164908 s and 64 forecast exports, the saved whole remaining forecast is 9,225.648639 s, including the 120 s reserve. The observed session allowance at that point is much larger. This is the declared conservative heuristic, not a latency guarantee or a provider-confirmed deadline.

Main calls actually use 278 attempts and roughly 1,641.77 summed ready-model seconds; physical overlap means this sum is not a wall-clock duration. The ten batch cells span about 20.41 minutes including orchestration, inspection and exports. The notebook's entire observed span is 2,295.663043 s, about 38.26 minutes. Setup/download, loading, envelopes, checkpoints and waiting/idle allocation all matter outside the main scientific generation sum.

No monetary cost, energy use, GPU utilization percentage or billable allocation duration can be recovered from these artifacts. Multiplying an observed notebook span by two devices would only be a conditional occupied-device-time proxy; it is not a verified provider charge. The 700-minute window is explicitly a planning estimate from the operator, not a confirmed quota.

## 9. Critical comparison with Course-7

### 9.1 What was independently rechecked

The historical comparison reads `notebooks/run/course-7-working/latest/` directly. Its 206 natural model actions and 69 natural checkpoints are independently re-walked under the historical state machine, including generic rejection feedback and the older presentation. The saved historical result is not rescored with assisted rules or the new seed. Historical controls and main summaries are rederived from raw submissions.

| Observed quantity | Course-7 | Assisted-v1 / assisted-v2 condition |
|---|---:|---:|
| Main original exact team success | 3/20 (15%) | 10/20 (50%) |
| Main retain success | 2/20 (10%) | 2/20 (10%) |
| Main clear success | 2/20 (10%) | 3/20 (15%) |
| Main both-policy success worlds | 1 | 0 |
| Main revised scalar-control correctness | 15/20 | 18/20 |
| All natural team calls | 206 | 308 |
| Illegal scientific/team actions | 60/206 team calls | 6/308 team calls |
| Main original illegal calls | 42/82 | 1/82 |
| Main retain illegal calls | 2/44 | 1/91 |
| Main clear illegal calls | 9/51 | 4/85 |
| Main retain both-submitted episodes | 20/20 | 8/20 |
| Main clear both-submitted episodes | 19/20 | 10/20 |
| Main retain obsolete-answer worlds | 10/20 | 0/20 |
| Main clear obsolete-answer worlds | 0/20 | 0/20 |
| Total physical campaign attempts | 252 | 356 |
| Mean recovery ready seconds: retain | 15.733183 | 29.438891 |
| Mean recovery ready seconds: clear | 24.890149 | 25.655746 |
| Mean clear−retain ready seconds | +9.156966 | −3.783145 |

Course-7's clear-minus-retain outcome contrast remains 0 pp with its historical exploratory interval [−10,+10] pp; its seed is 2026101402. The assisted interval [−15,+25] pp is wider, not evidence that the newer estimate is more precise. The old outcome strata and raw records remain untouched.

Historical main paired categories are both=1 (12), retain-only=1 (06), clear-only=1 (03), neither=17. Assisted categories are both=0, retain-only=2, clear-only=3, neither=15. Main IDs refer to different actual inputs across campaigns and must never be matched as identical experimental units.

### 9.2 Observed improvement versus causal improvement

It is correct to say **the new campaign exhibits more successful original collaboration, far fewer illegal actions, and no retained obsolete final submissions**. It is not established that the assistance caused those differences.

Several features change together: full common instructions, explicit coordination/finality/wait examples, source-notice explanation, current-source placement, phase-history boundaries and rule-specific feedback; the master seed and complete world list; assignment and batch order; qualification/pilot counts; usefulness thresholds and diagnostic fixtures. Native checkpoint and ordinary decoding settings are held nominally the same, but a nominally shared model is not a matched repeated experiment.

Course-7 couples device and sibling order in its historical assignment. Assisted scheduling deliberately decouples these with overlap within strata and keeps siblings on the same assigned device. This improves design balance prospectively, but cannot retrospectively make the old cohort a randomized prompt-control arm.

The descriptive original difference is +35 pp and the clear recovery difference +5 pp, while retain recovery is unchanged. These are cross-campaign descriptive differences, not difference-in-differences estimates, mediation effects, or statistically demonstrated gains. There is no same-world crossed assistance condition, no paired repeated-seed experiment and no prespecified between-campaign causal estimand.

### 9.3 The failure and cost profile changes substantially

The newer retained policy completes far fewer teams and spends more time repeating communication. Course-7 retained outcomes often terminate rapidly by submitting obsolete old answers, which are cheap and wrong. Removing that observable failure pattern does not necessarily reduce cost; it can expose or prolong noncompletion. Assisted retain has 91 main calls versus Course-7's 44.

Clear main recovery time changes much less across campaigns than retain time, while the clear−retain timing sign reverses. This supports a concrete descriptive account of why the older “retain is faster” observation does not generalize here. It is not evidence that a particular prompt component caused slower retain behavior.

Both campaigns demonstrate poor practical recovery, but their same 2/20 retain headline hides different trajectories: stale commitments versus legal communication loops, source mistakes and unfinished agents. Equal success counts do not imply equivalent behavior, and elimination of a conspicuous failure label does not establish successful collaboration.

## 10. Scientific context and interpretation

The following context was checked against primary sources on 16 October 2026. These are author-reported findings and conceptual parallels, not reproductions or external validation of this experiment. They supply framing, not a license to override the adopted contract.

**Distributed computation and communication.** SILO-BENCH treats Global Maximum as aggregation across private shards and reports a gap between active communication and effective distributed computation. Its native wait semantics yield to the next synchronous round, whereas this experiment's wait blocks until a delivered message. Its methods and results therefore motivate the task but do not supply I-01 recovery scoring or directly comparable rates. The present legal report loops instantiate a related observable distinction in a much smaller, modified recovery setting. [Zhang et al., SILO-BENCH, ACL 2026, §3 and Appendix A.5/B](https://aclanthology.org/2026.acl-long.1354.pdf).

**Multi-turn reliability.** Laban and colleagues compare fully specified and multi-turn sharded instructions and discuss premature assumptions, reliance on earlier answers and unreliable later adjustment. Those observations motivate separating single-call ability from interaction reliability. Their user–assistant conversations, tasks and repeated-simulation measures differ from two private agents with irreversible submissions. Current repeated requests are not automatically instances of their inferred explanation, and this run has no repeated-seed reliability decomposition. [Laban et al., LLMs Get Lost In Multi-Turn Conversation, §6 and Appendix F](https://arxiv.org/html/2505.06120v1).

**Updating and maintaining.** Belief-R explicitly separates cases requiring belief update from cases requiring preservation. That distinction highlights why selective use of unchanged peer evidence matters here, and why removing an obsolete answer alone is insufficient. Belief-R is not this distributed source-withdrawal experiment. All current worlds actually change their global maximum; no no-change continuation is present to distinguish a revision-specific impairment from a general reopening/interface problem. This last limitation is an inference about the current design. [Wilie et al., Belief Revision: The Adaptability of Large Language Models Reasoning, §3–4](https://aclanthology.org/2024.emnlp-main.586.pdf).

**Failure analysis and evidence quality.** MAST distinguishes multiple system, inter-agent and verification failure modes and uses an explicit human annotation methodology. Its approach motivates careful operational definitions and trace references. This analysis does not import its percentages, assume its taxonomy explains every current failure, or claim comparable human-coded reliability. Exact action/state/score calculations are reproducible; narrative mechanism interpretations remain descriptive. [Cemri et al., Why Do Multi-Agent LLM Systems Fail?, NeurIPS 2025, §3–4](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf).

The university report can reasonably contribute an auditable small study showing how a source-changing two-agent system can improve observable interface behavior while retaining poor joint recovery. It should not claim to discover source-preserving memory, prove a general theory of anchoring, or establish that forgetting is superior.

## 11. Limitations and unresolved questions

### 11.1 Identification and generalization

- **Twenty worlds and one realized seed schedule.** Calls, agents and repeated messages are not independent replications. The bootstrap resamples fixed world pairs, not repeated model samples.
- **Small diagnostic and pilot scope.** Four supplied views and four pilots reveal failure examples and establish the adopted gate; they do not estimate general interface competence or reliability.
- **No same-world assistance control.** Cross-campaign improvements are observed, not causally isolated.
- **No no-change reopening control.** Failures cannot be partitioned into factual revision, reopening/status interpretation and ordinary coordination difficulty.
- **Bundled retention intervention.** History presence changes information, length, wording and opportunities for imitation together. Retain/clear is a practical policy contrast, not a pure cognitive-memory assay.
- **Natural prefix heterogeneity.** Half the main prefixes are wrong; successful prefixes can still contain false messages. The descriptive correct-prefix subset is small and has no new inferential status.
- **Conditional input distribution.** Worlds are conditioned on unique winner and scheduled owner; the target is this fixed experiment, not arbitrary numerical tasks or all possible source changes.
- **One model/runtime/task scale.** Qwen3.5-9B, quantized direct decoding, two agents and 20-value shards do not support claims for other models, precision modes, long reasoning, agent counts or tasks.
- **Matched seeds are not matched outputs.** Retain and clear use the same recovery invocation seeds but different requests. This does not hold their generated reasoning or sampling paths fixed.
- **Incomplete blinding for interpretation.** The forensic review sees outcomes and evaluator truth. Literal quantitative checks are explicit; qualitative explanations are not independently blinded human coding.

### 11.2 Measurement and artifact limits

- **Internal reasoning is unobserved.** Message text may be fluent, contradictory, copied or strategically useful; it is not a verified internal chain of thought.
- **Source-projection examples are observational.** Exact value/location matches are verifiable, but the process that generated them is not identified.
- **Lexical audits are incomplete.** The maximum-claim regex covers declared forms only. It cannot establish complete rates of arithmetic, hallucination, historical uptake or semantic inconsistency.
- **No semantic oracle was given to peers.** Wrong values remain legal actions, and finality is preserved. Post hoc repairs would invalidate interpretation.
- **No complete remeasurement of kernels/tokenizer.** Stored token lengths, settings, rendered bytes, native selfcheck receipts and runtime cache/headroom diagnostics are checked; this audit does not reload weights, retokenize with a newly obtained tokenizer or reproduce GPU numerical behavior.
- **Snapshot evidence has temporal limits.** Persist-before-effects is visible in source and final consistency; actual individual transaction order and crash safety are not independently demonstrated by an uninterrupted final run.
- **Provider timing/cost is unknown.** Notebook span, ready time, dispatch time, load time, process exit and paid allocation boundaries differ.
- **Historical human approval remains pending.** These new AI-assisted documents do not rewrite human-review flags or establish a human signoff.
- **Intermediate exports are not all retained.** Recorded 53 export successes do not provide 53 separately verifiable historical ZIP generations.
- **External authorization history is incomplete.** Notebook finite commands and operator metadata are present; the original authorization conversation is outside the supplied artifact. No inference about unauthorized execution is warranted.

### 11.3 Questions the evidence does not settle

It remains unknown whether selective removal of old conclusions while retaining unchanged peer evidence would help; whether a no-change reopening would show the same stalls; whether clearer agent/record identifiers would reduce observed source projection; whether the two final commitments would improve under another model or precision; whether more calls would resolve loops or simply repeat them; and how stable any outcome is over new seeds.

These are prospective questions, not authorized changes or remedies adopted by this audit. The current data must retain their original protocol, failure outcomes and population.

## 12. Reusable claims and reporting guidance

### 12.1 Claims directly supported for later writing

| Candidate claim | Evidence | Qualification to keep |
|---|---|---|
| Complete fixed main cohort was executed | All twenty prefixes, forty recoveries and twenty revised controls; 278 main attempts | Completion is empirical coverage, not success |
| Retain 10%, clear 15%, paired difference +5 pp | Raw final submissions; independent scoring | Exploratory interval −15 to +25 pp; no superiority/equivalence |
| Original collaboration is better in this campaign than Course-7 | 10/20 versus 3/20 on their respective cohorts | Different inputs and bundled conditions; no causal attribution |
| Legal messaging improved markedly in the observed run | 6/308 illegal team calls versus 60/206 historical | Call counts are behavior-dependent; compare phase/world denominators too |
| Correct scalar controls do not guarantee recovery | Qualification 8/8, pilot controls 8/8, main revised 18/20 | Controls differ in prompt, information and seed |
| No obsolete old answer is submitted during main recovery | Zero in both current policies | Not absence of all historical influence; clear old-value availability differs |
| Noncompletion is prominent despite useful communication | Retain 12/20, clear 10/20; exact repeated-report cases | Procedural description, not an exclusive causal label |
| Clear uses less mean ready-model recovery time in this cohort | −3.783145 s/world, complete twenty-pair cost coverage | Interval −8.240557 to +0.588860; speed can reflect wrong/early stopping |
| Explanations and submissions can diverge | Exact calls in §5.5 | Do not substitute prose for the submitted integer |
| Successful results can contain false intermediate claims | Main-02 retain and main-19 clear | Endpoint remains correct; robustness of reasoning is unproven |

### 12.2 Claims to avoid

Do not write that the experiment proves forgetting helps, retaining is harmful, the policies are equivalent, the model cannot compute maxima, all recovery failure is anchoring, the prompt caused a 35-point improvement, the pilot certified reliable recovery, more messages mean better collaboration, the model used the true remote shard, GPU/kernel errors caused the observed mistakes, or the measured notebook span equals the billed GPU cost.

A particularly misleading formulation would be “the new prompt solved the original problem but recovery stayed broken.” The verified statement is narrower: the new campaign's original teams are correct on half the main worlds and all four pilot worlds, while revised exact team success remains low under both practical history policies. The causal role of assistance is unresolved.

### 12.3 Evidence map for assembling the final report later

- **Methodology:** specification §12.1, packaged annex, manifest/configuration, schedule and literal state reconstruction in the forensic companion.
- **Results:** complete twenty-world table, paired categories/intervals, intended-slot submission coverage, stage distinctions and complete effort totals.
- **Discussion:** source extraction/ownership cases, legal repetition, finality, prose/action divergence, useful historical evidence and successful-but-inaccurate explanations.
- **Limitations:** finite worlds/seeds, bundled condition, cross-campaign confounds, absent no-change arm, unobserved internal reasoning and provider timing.
- **Reproducibility appendix:** executable independent verifier, artifact hashes, exact call IDs, all-response ledger and preservation check.

The final course report has deliberately not been drafted here. These documents provide its auditable evidence base while preserving the original experimental record.

