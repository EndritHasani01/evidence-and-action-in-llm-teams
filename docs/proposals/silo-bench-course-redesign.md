# Course redesign: recovery after withdrawing the global maximum

**PROPOSED — NOT APPROVED OR IMPLEMENTED**

Prepared 14 October 2026 against `714ed3083b49e954692462e41d51d6dbd3250184`. Planning only. The [scientific specification](../../PROJECT_SPECIFICATION.md) remains authoritative; this document changes no specification, source, configuration, or experiment artifact and authorizes no inference.

## 1. Recommendation

**Choose authentic SILO-BENCH I-01 Global Max, two agents, and one narrowly defined revision: lower the unique old maximum enough that another value becomes the answer.** Compare retaining versus clearing the actual collaborative transcript after that revision. Use **20 independent main worlds**, six model turns at most per phase, and **500 total new physical attempts at most**.

For this course project, remove the no-change arms, extra task families, and mandatory thinking comparison. Qualify **non-thinking Qwen3.5-9B first**; reserve a bounded thinking fallback only if direct mode fails competence qualification. Preserve exact evaluation, matched starts, durable evidence, and honest uncertainty.

This changes the question from “Does clearing help specifically because information changed?” to **“After withdrawal of a previously winning value, what are the correctness and effort consequences of keeping versus clearing the team's previous communication?”** The narrower question is worthwhile and cheaper to interpret. It does not require a publication-scale mechanism study.

## 2. What the evidence supports

The review covered the operating contract, specification including its course amendment, living implementation handoff, [v2 proposal](silo-bench-lean-redesign-v2.md) and [companion notes](silo-bench-lean-redesign-v2/README.md), implementation boundaries, saved CPU/GPU diagnoses, and authentic SILO source. Since the preceding repository review, changes through this HEAD are proposal documents only.

| Evidence | Implication |
|---|---|
| Existing course design schedules 5,752 distinct main slots and 6,280 logical uses | Reduce scientific scope, rather than shrinking every old comparison |
| Latest 9B diagnostics: 11/21 valid responses; all three full-information controls wrong | Simpler actions and easier mathematics both need qualification; formatting alone does not explain failure |
| 9B loaded and generated on both T4s; the 110,416-input-token probe failed the 1.5 GiB headroom gate | Short-context reuse is plausible; the old failure is not proof that 9B weights cannot fit |
| Latest 4B fallback stopped on checkpoint-byte accounting; backups inflated a derived attempt count | Reused operational paths need focused repair; no new 4B capability result follows |
| CPU durability/reporting checks exist, but no accepted model pilot or main execution | Preserve their infrastructure evidence without relabeling it as experimental success |

Sources: [latest GPU analysis](../validation/course-kaggle-final-online-6-analysis.md), [diagnostic receipt](../../notebooks/validation/course-kaggle/final-online-6-analysis.json), [CPU gate](../validation/course-m4-report-and-cpu-gate.md), and [living handoff](../IMPLEMENTATION_PLAN.md). Many diagnostic prompts lacked complete information, so their aggregate 0/21 exact-answer count is not a clean capability estimate. All 6,280 old main outcomes remain unknown.

V2 correctly narrowed the intervention and separated completion from correctness. Its preference for I-08 prioritized richer intermediate work over dependable completion. For a course, that trade-off should reverse. Its four-cell comparison and exact-source attachment machinery are also optional once the claim becomes an operational transcript-retention comparison.

## 3. Is Global Max scientifically meaningful enough?

The released I-01 generates **20 integers per agent, uniformly from −1000 through 1000**, and asks every agent for the global maximum. Its guidance explicitly suggests local maxima followed by aggregation and dissemination. Two agents are an original benchmark scale. Preserve this mathematics, size, private distribution, and per-agent answer responsibility. [Official generator](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/benchmark_generator/paradigm_i.py#L53)

The paper's DeepSeek-V3.1 task averages are 93.3% for I-01 and 47.5% for I-08. These aggregated results favor investigating I-01, but do not qualify 9B or this interaction horizon. [Paper, Table 10](https://aclanthology.org/2026.acl-long.1354.pdf)

I-01 offers a small but real historical dependency. Raising a value above the old maximum often makes recovery trivial. **Withdrawing the winner instead exposes an alternative that the old answer discarded.** An unchanged partner's recorded local maximum can remain useful; an old global answer can become misleading. The old answer and changed owner's current shard alone do not generally determine the new global answer.

Do not oversell this. Finding a local maximum is a scan, not substantial expensive reasoning. Retention may save one exchange, do nothing, or cost more context processing than recomputation. An accuracy ceiling is plausible. That is acceptable if effort and actual communication are measured prospectively. Adding distractions, hiding necessary current inputs, or forcing elaborate summaries merely to create a memory effect would weaken the course study.

## 4. The proposed experiment

### Worlds and revision

Generate 20 independent native-size worlds, conditioned on a unique global maximum and a remaining maximum greater than −1000. Let the old maximum be \(M\), its record be \(r\), and

\[
M_2=\max_{j\ne r}x_j.
\]

Replace \(x_r\) with an integer sampled uniformly from \([-1000,M_2-1]\). Then the revised answer is exactly \(M_2<M\). Save inputs, edit, random streams, and mathematical rejection counts before main inference. Reject only mathematical ineligibility, never model behavior; use a finite generation-attempt limit. This is a **conditioned winner-withdrawal population**, not arbitrary factual changes.

Randomly relabel the two exchangeable shards to balance the changed owner, and preassign first speaker so each owner/first-speaker combination occurs five times. Keep a world's ordering identical across treatments. Do not force whether the replacement winner resides with the changed owner or its partner; report that naturally occurring distinction descriptively. Hide edit-selection rules and expected answer changes from agents.

### One prefix, two sibling continuations

Run an actual collaborative prefix once. Drain messages and save its exact terminal or capped state. Apply the same revision to two isolated sibling starts:

| Shared by both siblings | Retain | Clear |
|---|---|---|
| Current private arrays, task instructions, factual notice, speaker order, turn/token limits, and decoding configuration | Keep actual visible prefix messages and submissions, including mistakes, labeled as previous work | Remove prefix messages and submissions |

Only the owner receives the old/new record receipt and updated private array. Both know which owner's record changed; the partner receives no replacement payload automatically. Neither receives gold or a host-computed maximum. Clear active submissions and reopen both agents irrespective of prefix correctness.

**Simplification from v2:** use ordinary peer messages, with no separate source-attachment action, remote-source inventory, or pending-payload protocol. Private arrays are authoritative; communicated maxima and copied values are agent claims. Agents may send raw values if they choose, but the host neither verifies those claims live nor promotes them into canonical evidence.

Consequently, clearing the transcript can remove remote information as well as previous calculations. This is an intentional **total transcript-policy effect**, not a pure anchoring effect with equal total information. Both treatments retain the same current private inputs and equal opportunities to obtain partner information. If that broader estimand is unacceptable, retain v2's source machinery and accept additional engineering; do not claim it has been controlled away here.

### Agent behavior and stopping

Use alternating eligible turns, at most **three calls per agent per phase**, six total. This is a maximum, not six required outputs. A small action envelope permits an ordinary message to the sole partner, an optional integer submission, or waiting. Sending and submitting in the same response is allowed; message-only turns need no answer. Keep the native local-max guidance, without prescribing the conversation.

Deliver inbox contents automatically before activation. Submitted agents are quiescent; a subsequent message invalidates their active submission and permits review if a turn remains. Waiting agents wake on a message, not repeated polling. Do not transfer unused turns between agents.

End when both have active submissions and no pending review, the cap is reached, or no eligible progress remains. Different or wrong submitted integers can be procedurally complete: correctness is evaluated offline. A last-turn message can leave unresolved review and cause incomplete completion; the pilot must test this boundary. No semantic host classifier decides that a message is harmless.

This deliberately changes native execution: the released message tools use explicit receives and permanent submission, and the API wrapper retries indefinitely. None should be copied unchanged. [Native message tools](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/src/msg/tools.py) · [native retry wrapper](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/src/utils/llm.py)

### Concrete example

The [released two-agent instance](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/benchmarks/I-01_n2.json) has local maxima **827** and **780**. Replacing agent 0's zero-based row 12, `827`, with `100` makes its local maximum **518** and the global maximum **780**. These values were independently recomputed during this review.

A possible prefix is: agent 0 sends its maximum 827; agent 1 replies that its maximum is 780 and submits 827; agent 0 submits 827. After the revision:

- **Retain:** agent 0 can combine its new 518 with the recorded, unchanged partner maximum 780, communicate the updated result, and submit. Its partner verifies and submits. Two calls can suffice.
- **Clear:** agent 0 sends 518 without submitting; agent 1 supplies 780 and submits; agent 0 then submits. Three calls can suffice.

These are attainable examples, not scripts or predictions. Retain may instead repeat 827, or both arms may simply exchange maxima afresh. Both agents need partner-derived information to establish a global answer; the task is not two independent full-input computations. Full-data sharing, if chosen by agents, remains allowed.

Call the study **a controlled recovery extension of SILO-BENCH I-01**, not an unmodified benchmark evaluation.

## 5. Methodology and useful results

For world \(w\), let \(Y_{w,p}=1\) when both agents complete with correct current answers within the horizon under policy \(p\), and zero for an executed unsuccessful episode. An unresolved interrupted or unexecuted episode is unknown. The primary contrast is

\[
\Delta=\frac1{20}\sum_w(Y_{w,\mathrm{clear}}-Y_{w,\mathrm{retain}}).
\]

Positive values favor clearing. Report the complete paired table: both succeed, retain only, clear only, neither. Keep every valid main world; never rerun until a prefix succeeds. Report prefix correctness and a secondary correct-prefix analysis with its actual denominator. Only that stratum directly concerns recovery from an established correct result.

Each world also receives **two one-call full-information controls**, original and revised, with the selected configuration. These distinguish basic mathematical failure from distributed execution failure; they do not gate main-world inclusion or establish multi-agent superiority. No control output enters peer views.

Prespecify effort alongside success: post-revision model calls, input/output tokens, messages, and ready-model inference seconds. Separate setup and allocated idle time. Show costs for all paired outcome categories; a fast wrong answer is not an efficient solution. Equal accuracy can still reveal useful cost differences. Equal accuracy and cost mean no detected benefit in this bounded setting, not equivalence.

Review all traces with a short fixed rubric: wrong local maximum, stale old answer, submission without partner-derived evidence, unresolved request, disagreement, malformed output, truncation, or infrastructure failure. Annotate whether correct partner maxima existed in retained history. These observations support explanations but do not prove inner anchoring. Do not add an LLM judge.

Twenty worlds—not 40 branches or hundreds of calls—are the independent units. Show raw paired differences and exploratory 95% paired-world bootstrap intervals, with small-sample limitations. A degenerate interval is not certainty: even zero disagreements in 20 independent pairs permits an illustrative one-sided 95% disagreement bound of about 13.9%. No small-effect power, equivalence, cross-task, or cross-model claim is justified.

Removing sham arms forfeits the correction-specific interaction. Context length, forgotten remote information, and changed downstream communication are components of the policy effect, not separately identified mechanisms. This is the principal scientific sacrifice.

## 6. Complete new-attempt budget

| Allocation | Calculation | Maximum physical attempts |
|---|---:|---:|
| Main prefixes | 20 × 6 | 120 |
| Main retain/clear continuations | 20 × 2 × 6 | 240 |
| Main full-information controls | 20 × 2 | 40 |
| **Main subtotal** | 20 × 20 | **400** |
| Direct-mode qualification | Six development worlds × original/revised | 12 |
| Thinking qualification, only if direct fails | Same six worlds × original/revised | 12 |
| Complete pilot | Two additional worlds × 20 | 40 |
| Hardware/state diagnostics | Six short checks plus two selected-mode envelope calls | 8 |
| **Scheduled first attempts, worst case** | | **472** |
| Contingency for extra development diagnostics and eligible infrastructure retries | Hard shared allowance | 28 |
| **Total new-study ceiling** | | **500** |

If direct mode passes, the unused thinking screen reduces the maximum to **488**; do not spend it simply to fill the budget. Early completion reduces actual use further. There are 28 distinct worlds: six qualification, two pilot, twenty main. Main comprises 20 prefix episodes, 40 continuation episodes, and 40 single-call controls.

At maximum horizon, main execution generates 360 team responses and 40 controls. Charging the shared prefix to both hypothetical end-to-end policies yields **520 attributed main uses**, but only **400 physical first attempts**. Exact resume of a durable response generates nothing; a new failed invocation, warm-up, interruption, diagnostic, or retry consumes an attempt. The previous 45 documented preparation attempts remain historical spending, separate from this new ceiling.

The contingency is finite, not permission to search prompts until results look attractive. Additional model diagnostics must be declared and counted before main; changed prompts or protocols require requalification within the remaining allowance. Permit at most one identical retry only for established infrastructure interruption without a durable outcome. Wrong answers, malformed replies, truncation, and known terminal timeouts are outcomes, not retry invitations. If preparation cannot fit, stop and revise the budget.

## 7. Model and T4 feasibility

Use the demonstrated pinned 9B loading path (`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, NF4/double quantization, FP16 computation), one resident model and serial worker per T4. Two devices process different worlds; they do not pool memory. Use fresh call state and keep siblings on the same device where practical, with preassigned treatment order balanced across worlds.

**Direct first:** propose 512 total output tokens and an 8,192-token input ceiling. Allow ordinary messages within that envelope; retire the separate 64-token prose restriction. The six-call prefix plus six-call recovery permits at most eleven preceding visible responses, so the bound is plausible but needs the real tokenizer/renderer check. No silent history truncation.

**Conditional thinking fallback:** 4,096 total generated tokens, at most 512 visible final tokens, same input limit. Archive thinking but never carry it into later working context. Direct sampling starts at temperature 0.7/top-p 0.8/top-k 20; thinking at 1.0/0.95/20. Freeze exact settings before qualification; presence penalty zero is a deliberate candidate differing from the official general-task recommendation of 1.5, not a proven optimum. The model card supports both modes and recommends excluding past thinking; its much larger general output budgets do not establish that this bounded setting works. [Official model guidance](https://huggingface.co/Qwen/Qwen3.5-9B#best-practices)

Qualify actual short-envelope memory on both devices, retaining the existing 1.5 GiB free-headroom criterion. Do not repeat the irrelevant 110k-input stress. Bound timeouts from measurements; a 4,096-token output at six tokens/second needs about 683 seconds of decoding, so the old 120-second limit cannot govern thinking automatically. If direct passes, avoid implementing and qualifying thinking merely for comparison.

For planning only, with 500 attempts, average output length \(L\), rate \(r\), 25% overhead, and one aggregate GPU-hour setup, use \(H=1+1.25(500L)/(3600r)\):

| Assumption | Aggregate GPU-hours | Ideal two-device elapsed hours |
|---|---:|---:|
| 250 output tokens, 7 tokens/s | 7.20 | 3.60 |
| 700 output tokens, 7 tokens/s | 18.36 | 9.18 |
| 1,200 output tokens, 6 tokens/s | 35.72 | 17.86 |

These are sensitivities, not measured forecasts. At 4,096 tokens per call and six tokens/s, the same formula gives about 119.5 aggregate hours. Use measured phase costs and actual available Kaggle quota before admission. A small attempt count alone does not make thinking affordable. Do not add an automatic 4B or serving-engine search.

## 8. Alternatives and the practical decision

All numerical alternatives below include two complete pilot worlds, 24 qualification attempts, eight diagnostics, and the stated contingency.

| Candidate | Main worlds / ceiling | Judgment |
|---|---:|---|
| **I-01, two recovery arms, six calls/phase** | **20 / 500; 28 contingency** | Preferred: adequate conversational room, narrow claim, more independent evidence |
| I-01, two arms, four calls/phase | 30 / 500; 20 contingency | More worlds, but only two turns per agent; late review or a single repair can dominate outcomes |
| I-01, four arms including sham, four calls/phase | 18 / 500; 28 contingency | Closest to v2's I-01 alternative; preserves correction specificity but risks an unnecessarily tight lifecycle |
| I-01, four arms, six calls/phase | 12 / 500; 20 contingency | Best if the correction-specific interaction is essential; weaker replication for this course objective |
| I-08, four arms, six calls/phase | 12 / 500; 20 contingency | Richer summary reuse, but duplicate counting and overlap reasoning increase capability risk |

Prefer six-turn ceilings without requiring six-turn conversations. Do not choose four merely because an ideal trace takes three. Top-K, graph tasks, multiple families, and a third memory policy add risks that the course question does not need. A centralized-only study would be cheaper but lose distributed collaboration entirely.

## 9. Reuse, gates, and next steps

| Reuse | Adapt or simplify | Preserve outside this study |
|---|---|---|
| Saved inputs/seeds, exact raw outcomes, persist-before-effects, bounded retries, SQLite evidence, fresh model state | Add I-01; two-peer lifecycle; optional scalar submission; simple private-input/transcript views; episode-level reporting | Existing thesis/course specifications, fixtures, artifacts, mixed masks, receipt/delay interventions, multi-family schedules |

This is not a parameter-only change: [tasks](../../recovery/tasks.py) fixes four peers and five other families; [state](../../recovery/state.py), [runner](../../recovery/runner.py), and [storage](../../recovery/storage.py) encode fixed rounds/barriers; [inference](../../recovery/inference.py) fixes non-thinking framing. Reuse responsibilities and verified invariants, not incompatible assumptions. No new framework, database, source-certification service, semantic extractor, or general event platform is warranted. Repair known byte-inventory/accounting defects only where the selected path uses them.

Proceed later in this order:

1. **Adopt the narrower question explicitly.** Agree that transcript retention includes remembered remote information and that no correction-specific claim survives without sham arms.
2. **Establish the CPU contract.** Check released I-01 answers, duplicate/negative/last-winner cases, revision validity, hidden-information isolation, exact sibling starts, waiting/reopening/caps, and crash/resume accounting. Prove the actual token bound. Source inspection and mathematical checks in this review are not evidence that this redesigned runner already exists.
3. **Qualify direct mode, then thinking only if necessary.** Require at least 11/12 exact full-information answers and no malformed/truncated final action for a passing mode. Treat this as a small competence screen, not a population-reliability estimate. Use the eight diagnostic calls for short A/B/A state checks on each device and selected-mode envelope checks. If neither mode passes, stop.
4. **Run the two-world pilot after authorization.** Require correct original collaboration in both worlds, all four full-information controls correct, useful partner-derived information in histories, and no unresolved formatting, information-boundary, persistence, or horizon defect. Inspect recovery failures; do not require a particular treatment sign or a nonzero effect. A ceiling is acceptable; an inactive manipulation or protocol-dominated floor is not.
5. **Freeze and execute all twenty worlds after authorization.** Fix inputs, edits, prompts, mode, limits, rubric, schedule, and cost forecast. No effect-dependent stopping, extra worlds, or model switches. If interrupted, resume exactly or report intended coverage and unknown-outcome bounds; completed cases do not replace the intended population.

If six turns prove inadequate, eight-turn phases with the same twenty worlds, two pilots, and preparation allowances cost **632 attempts**. Prefer an explicit revision over undocumented extra turns. If I-01 is competent but yields no accuracy or cost distinction, report that bounded negative finding; do not manufacture difficulty after observing main outcomes.

**Decision:** adopt I-01 as the course direction, subject to these gates. Its contribution is a clean, reproducible study of whether keeping a short distributed conversation helps recovery from an obsolete winner. The main remaining uncertainty is whether real 9B conversations produce a useful accuracy or effort contrast beyond trivial re-exchange of two maxima. That uncertainty is appropriate for a course experiment; it does not justify carrying I-08's extra capability risk or the original study's full machinery.

## Review provenance

During this review, the vendored I-01 generator, released two-agent fixture, execution engine, message tools, and LLM wrapper matched upstream commit `e74127782ed1c42fff474249961f022c063d76f2` after line-ending normalization. The example and budget arithmetic were checked on CPU. Existing validation findings above were read from their saved evidence, not rerun. No GPU experiments or redesign implementation were performed.
