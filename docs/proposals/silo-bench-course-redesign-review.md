# I-01 course redesign: pre-implementation review

**PROPOSED REVIEW — NOT APPROVED OR IMPLEMENTED**

14 October 2026. Reviews [the I-01 course proposal](silo-bench-course-redesign.md) against repository HEAD `714ed3083b49e954692462e41d51d6dbd3250184`, the prior proposals, current implementation boundaries, saved diagnostics, and official task/model documentation. The reviewed proposal remains unchanged. The [scientific specification](../../PROJECT_SPECIFICATION.md) remains authoritative; this review authorizes neither implementation nor inference.

## 1. Verdict and priorities

**Conditional GO for the I-01 direction; NO-GO for implementing the current submission-invalidation rule unchanged.** The course question is defensible, but it concerns short communication reuse after an obsolete winner, not substantial reasoning recovery. Its strongest potential result may be equal accuracy with different recovery cost.

| Priority | Finding | Smallest useful response |
|---|---|---|
| **P0: resolve before implementation** | Every message can invalidate a correct submission and manufacture noncompletion | Make submissions final within a phase; reopen both agents only at the factual revision |
| **P0: resolve before freezing the study** | Several effort measures are listed without one principal practical comparison | Keep exact team success; designate post-revision ready-model inference time as the principal effort measure, with calls/tokens explaining it |
| **P1: recommended simplification** | The old/new receipt gives the cleared owner the old winning value again | Show the new value/current shard, retaining before/after values only in the audit archive |
| **P1: better preparation allocation** | Two pilot worlds cover little actual interaction; 20 original-input main controls repeat an easier diagnostic | Exchange those 20 controls for a third complete pilot, preserving 20 main worlds and the 500-attempt ceiling |
| **P1: clarify, not expand** | Order, seed mapping, and qualification failure handling can quietly determine the result | Freeze those rules explicitly; do not add an order, decoding, or model factorial |

The task's simplicity, lack of sham arms, and small sample are **acceptable limitations**, provided the claims remain narrow. Missing evidence of model competence, valid execution, or affordable runtime is a **main-execution blocker**, not a reason to build more infrastructure first.

## 2. Is this meaningful recovery?

Yes, at a modest level. Native I-01 requires local maximum computation and cross-agent aggregation; two agents with 20 integers each are authentic benchmark settings. Lowering the unique winner exposes an alternative absent from the old scalar answer. [Official I-01 definition](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/benchmark_generator/paradigm_i.py#L53)

For example, after the owner's maximum falls from 827 to 518, an unchanged partner maximum of 780 or 790 gives different revised answers despite the same old answer and owner-local update. Previous communication can supply that missing fact. But rescanning 20 numbers and exchanging two maxima is cheap. This is **retention of a distributed conversation**, not evidence about preserving expensive computation, long-term memory, or pure anchoring.

Clearing also removes remote information embedded in messages. That is part of the declared policy effect. Equal current private arrays do not imply equal total information. Full-information controls help diagnose capability, but do not remove this difference or identify internal mechanisms. Do not restore source certification or add a third memory condition to claim otherwise.

Two important qualifications:

- A correct original collaboration may preserve only the global answer, without the partner's useful reserve maximum. That is a valid strategy outcome. Require genuine original collaboration in the pilot, not a history deliberately selected to benefit retention.
- Recomputing correctly in both treatments is a legitimate recovery result. If accuracy and cost both tie, report no detected practical benefit in this short-history regime. Do not add distractions, lengthen histories, or select harder main worlds afterward to obtain an effect.

**Remove the before-value from the agent-facing revision receipt.** In this population it is exactly the obsolete global maximum. Reintroducing it into the cleared owner's prompt weakens the intended erasure and is unnecessary for computing a maximum from current inputs. Both arms should receive the same current private shard and owner-local new-value notice; preserve the full edit offline. This is a sharpening of the policy comparison, not proof that any remaining error is anchoring.

## 3. The lifecycle has a concrete artificial-failure case

Under the proposed automatic invalidation rule, the following legal sequence can fail despite correct computation throughout:

| Call | Action | Effect under the current proposal |
|---|---|---|
| A1 | Sends its local maximum | B can aggregate |
| B1 | Sends the correct global maximum and submits it | B has submitted |
| A2 | Sends agreement and submits the same correct answer | A's message invalidates B's submission |
| B2, A3, B3 | Each sends confirmation and submits the same correct answer | Each invalidates the other; A eventually has no review turn left |

The phase reaches six calls and can receive zero completion credit. This is a logical counterexample to the proposed rule, not an observed model run. A treatment that encourages more reassurance could lose accuracy because of this mechanism alone.

### Recommended minimal replacement

Use **phase-final submissions**, consistent with the native submit operation's finality. A response may send a message and submit; deliver its message before marking the sender finished. The sender then receives no more model calls in that phase. Subsequent messages to it are archived but do not cancel its answer. Stop when both have submitted, irrespective of correctness, disagreement, or late confirmations. Only the explicit factual revision reopens both agents. [Native submission behavior](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/src/msg/tools.py#L74)

Keep six-call ceilings, optional answers, automatic inbox delivery, and waiting for unsubmitted agents. There is no mandatory acknowledgement or correctness feedback. Submission values are private to the evaluator unless an agent communicates them; do not turn submission into an uncounted broadcast. Explain finality and the need to share necessary information before finishing in the common task instructions.

This deliberately accepts a remaining failure: an agent that finishes before helping its partner may strand the partner. Classify that as premature finalization. The controller neither decides evidence sufficiency nor supplies a rescue turn. If that behavior dominates the pilot, the protocol is not ready; do not dismiss it as merely a model failure.

The alternative—keeping provisional answers while supporting explicit review requests—is possible, but introduces another distinction agents must learn. It is unnecessary for a task with one revision strictly **between** phases. Keeping automatic reopening and merely increasing the cap postpones the confirmation-loop problem. Phase-final semantics are the simplest defensible starting point, not a guarantee of competent collaboration.

## 4. Evaluate accuracy and effort together

Keep the all-world paired team-success contrast and the correct-prefix secondary stratum. Report its actual denominator; never replace failed prefixes or exclude main worlds using their controls. An executed failure is zero; unresolved execution is unknown. Do not count unused opportunities after completion as failures.

Before main, designate:

- **Correctness:** both agents submit the exact revised maximum within the common limits. Report both-success, retain-only, clear-only, and neither counts, separating wrong submissions from noncompletion.
- **Principal practical effort:** sum of post-revision per-call elapsed inference time with the model already loaded, including prefill and decoding. Separate loading, queueing, idle allocation, and prefix cost. Partial interrupted costs are observed spending, not complete episode costs.
- **Explanatory costs:** calls, input tokens, generated tokens, and messages. Fewer calls need not mean less time when retained prompts are longer.

Show paired costs alongside all four success categories. An all-world cost difference describes resource consumption; it does not by itself establish useful efficiency. A both-success-only cost summary is descriptive because membership is post-treatment. Do not introduce an arbitrary failure penalty or a success-per-token ranking that hides failures.

One world changes the accuracy estimate by five percentage points. Twenty paired worlds cannot establish equivalence; zero disagreements still gives an illustrative one-sided 95% upper bound of 13.9% under an i.i.d. binomial model. Use the paired table and approximate world-level intervals, with no seed-stability or order-subgroup claims. The previous proposal's correction-specific interaction remains unavailable without sham arms; that is acceptable for this operational question.

## 5. Order and decoding: keep control without creating more conditions

### Speaker order is a moderator, not automatically a confound

Keep the proposed balance: ten worlds with the changed owner speaking first in recovery, ten with its partner first, and equal owner labels. Hold recovery order identical within each retain/clear pair. Specify prefix order separately in the saved schedule; retaining the same order across phases is acceptable, but then prefix-content and recovery-order effects are not separately identified.

The size of a plausible benefit is smaller than the proposal's best-case example suggests. For an illustrative strategy that shares both local maxima: clear needs three calls; retain can need two when the changed owner starts, but three when the uninformed partner starts. Across the balanced sample this is **60 clear calls versus 50 retain calls**, a 16.7% call saving, not a universal one-call saving per world. This is an attainable illustration, not a lower bound or prediction; missing summaries and longer prompts can eliminate it.

Do not make the changed owner always start merely to improve this contrast. Require pilot coverage of both relative orders. Also balance physical treatment execution order and keep siblings on the same device where practical, so timing drift does not systematically favor a policy.

### Keep one fixed direct-mode decoding configuration

The existing inference path already uses sampling at temperature 0.7, top-p 0.8, top-k 20; these match the model card's general non-thinking guidance. Keep this candidate, including the proposal's explicitly documented penalty choices, rather than adding a decoding sweep. [Current inference code](../../recovery/inference.py) · [official guidance](https://huggingface.co/Qwen/Qwen3.5-9B#best-practices)

Greedy decoding would remove sampling variability, but is not guaranteed more competent and would not remove implementation or floating-point nondeterminism. It is a reasonable separate candidate only if a diagnosed problem warrants it; it is not a prerequisite for causal comparison.

Bind seeds to world, phase, agent, and that agent's invocation index, with matched continuation seeds across retain/clear. Do not derive them from global execution order or shift later seeds because another branch stopped early. Different prompts with the same seed do not constitute identical model randomness or authorize replay. One realized prefix and one continuation per treatment estimate behavior under this fixed sampling policy, not a model's seed-invariant preference.

## 6. Qualification and budget: improve coverage, not ambition

The current budget adds correctly. The weak point is the allocation's diagnostic value, not its arithmetic. Keep the direct-first screen, conditional thinking, and hardware checks. **Do not automatically respond to malformed outputs, premature submission, or a lifecycle defect by enabling thinking.** Diagnose those failures first. Thinking is a candidate for demonstrated competence limitations; it adds framing, runtime, and qualification work.

The 11/12 full-information threshold is a screening rule, not 12 independent reliability trials: original/revised controls share six worlds. Passing it does not establish dependable collaboration. Conversely, main controls diagnose observed behavior; they must never filter the analyzed population.

### Recommended exchange within the same ceiling

Remove the 20 **original-input main** single-call controls. Retain all 20 revised controls, original/revised qualification, and both controls in every pilot. Spend the saved 20 calls on a third complete pilot world.

| Allocation | Current proposal | Review recommendation |
|---|---:|---:|
| Main: 20 prefixes and 40 continuations, six-call ceilings | 360 | 360 |
| Main full-information controls | 40 | 20 revised |
| Complete pilot worlds, including two controls each | 40, two worlds | 60, three worlds |
| Direct qualification + conditional thinking qualification | 12 + 12 | 12 + 12 |
| Hardware/state diagnostics | 8 | 8 |
| Development/interruption contingency | 28 | 28 |
| **Maximum new attempts** | **500** | **500** |

The recommendation preserves 20 independent main worlds and 28 contingency attempts. It has 472 scheduled first attempts at worst, or 460 if direct passes; including contingency, the direct-only ceiling remains 488. There are six qualification, three pilot, and twenty main worlds. All exploratory calls and retries count. Do not spend unused allowances just to reach 500.

The sacrifice is per-world full-information diagnosis of a failed original main prefix. Its observed collaborative result remains available, and original task competence is screened in qualification and pilots. For an easy course task, an additional complete interaction is the more valuable investment. Keeping the original allocation remains defensible; this exchange is a recommendation, not a validity prerequisite.

Preselect the three pilots to cover both recovery speaker orders, both owner labels, and examples where the next winner stays with the owner or moves to its partner. These are mathematical coverage choices made before model outputs, not effect selection. Three pilots still do not estimate failure rates precisely.

Other trades are less attractive:

- Four pilots under this revised control allocation cost **520** with the 28-attempt reserve, or leave only eight reserve attempts at 500.
- Eight-call phases throughout the revised twenty-main/three-pilot plan cost **638**. Extra calls do not solve an ill-defined stopping rule.
- Four-call phases can buy more worlds, but reducing each agent to two turns is premature before the natural lifecycle is shown usable.

A generation ceiling is not a GPU-time guarantee. Keep the proposed short-context envelope and actual-host headroom checks. Use measured readiness, input/output lengths, and remaining quota before admission; no new model or serving stack is justified by this review.

## 7. Minimal next validation steps and final decision

1. **Resolve the small contract changes on paper:** phase-final submission, owner-facing notice without the old value, principal effort measure, exact visibility, and seed/order mapping. Retain only each agent's own previously visible work; do not inject the global transcript, another agent's private submission, old prompts containing hidden arrays, or correctness flags.
2. **After separate adoption, perform focused CPU validation:** the confirmation trace above; a normal three-call solve; premature finalization; waiting/deadlock; disagreement; cap exhaustion; exact revision reopening; paired view equality; and interruption before/after persisted output/effects. No correctness-driven stopping or live answer repair. Preserve raw failures and exact resume.
3. **Qualify one direct configuration, then the conditional fallback only when justified.** Require the proposed full-information screen, valid finite outputs, actual short-envelope headroom, and fresh state. If neither qualifies within the allocation, stop rather than expand a hidden search.
4. **Run the three preselected pilots after authorization.** Require correct original teams and controls, genuine original communication, and no unresolved protocol, persistence, leakage, truncation, or budget defect. Recovery errors can be legitimate observations; a nonzero or favorable retention effect is not a gate. Investigate any deadlock or premature-finalization failure before main. If the protocol or prompts change, requalification consumes the same finite allowance.
5. **Freeze and execute only after those gates and authorization.** Preserve all intended main worlds, failed prefixes, interruptions, and unknown outcomes. A repeated protocol defect or unaffordable runtime blocks execution; accurate equal-cost recovery does not.

Reuse the proven durability, model ownership, seed records, and offline evidence access. Adapt the currently fixed four-peer/barrier assumptions in [state](../../recovery/state.py), [runner](../../recovery/runner.py), and their consumers only where the new lifecycle requires it. Do not redesign storage or introduce a generic event framework to support this review. The [saved GPU diagnosis](../validation/course-kaggle-final-online-6-analysis.md) still establishes neither I-01 competence nor acceptance of the redesigned protocol.

**Final assessment:** proceed with the small I-01 study after clarifying finality and evaluation; prefer the receipt simplification and third-pilot reallocation. Do not proceed unchanged with automatic submission invalidation, or claim meaningful memory benefits merely because a revised maximum was eventually recomputed. A clean estimate of a small communication/cost effect—or a well-bounded absence of one—is sufficient for this course project.

This review used source/document inspection and arithmetic checks only. No specification, existing proposal, code, test, or experiment artifact was modified; no GPU experiment was run.
