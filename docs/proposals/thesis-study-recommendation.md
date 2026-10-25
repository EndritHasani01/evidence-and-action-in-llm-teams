# Recommended thesis study: practical recovery after private information changes

**Decision package · 22 October 2026 · Prompt 1 of 3**

**Status: research proposal only.** The [project specification](../../PROJECT_SPECIFICATION.md) remains the sole scientific authority. This document recommends a different main study from both the [six-cell proposal](thesis-extension-2026-10-18.md) and the later [four-cell recommendation](../implementation-research/thesis-literature-2026-10-18/prioritized-design-tests.md). It adopts neither. It authorizes no implementation, configuration change, inference, GPU allocation, weight download, main experiment, paid compute, or publication.

## 1. The decision and its scientific value

Study **whether clearing a team's actual conversation improves its ability to complete a correct joint decision after a private fact changes, and whether that effect differs from simply reopening the same task without a change**. Use two agents, the existing distributed maximum task, literal retain/clear policies, and both intended model systems: Qwen3.5-9B and IBM Granite 4.2-8B.

The recommended main population has **192 independent worlds**, each with one naturally generated original interaction per model. Every realized prefix—including wrong, incomplete, and illegal behavior—feeds four isolated continuations: retain/revision, clear/revision, retain/no change, and clear/no change. Half the revisions demote the old winning record; half change its value while leaving it the winner. Both require a different numerical answer. The second kind prevents a deletion-only shortcut from succeeding throughout the population.

Use one primary continuation trial per cell, two additional trials on **24 predetermined worlds**, and a real answer-preserving edit on **32 predetermined worlds**. Both panels reuse their original natural prefixes. The fixed resource fallback is **128 main worlds**, chosen before any main inference. The recommendation requests a new, separately adopted ceiling of **17,192 physical attempts and 200 additional aggregate allocated GPU-hours**; the fallback ceiling is **13,096 attempts**, with the same hour ceiling. These are proposals, not available or approved resources.

The valuable unanswered question is operational. A team can have enough information, say the right answer, and still fail to complete two correct commitments. Clearing may remove harmful history, but also useful peer evidence; retention may save another exchange, but preserve mistakes or ineffective behavior. The thesis should measure that whole trade-off under live interaction. It should not start by assuming that explicit old-answer anchoring is the dominant problem.

The contribution would be a reproducible, uncertainty-aware study of **natural-history recovery, change specificity, and completed action** in two configured model systems. It would establish neither a general memory theory nor a new recovery algorithm. Its strength comes from exact private information, lawful paired interventions, honest populations, and observable outcomes—not a large condition matrix.

**Material conditions still preventing adoption-ready execution:** the new protocol has not passed a complete token/capacity proof; Granite has not been qualified in this repository; both models' baseline/reopening competence under the proposed interface is unknown; Kaggle persistence and allocated throughput are unmeasured; and the larger budget requires explicit adoption. Prompt 2 should resolve the technical feasibility case, and Prompt 3 should consolidate the resulting scientific contract. A failed feasibility condition must remain visible rather than trigger silent model or task substitution.

## 2. Evidence supporting the choice

### 2.1 What was checked, and what is actually established

The checkout started clean on `feat/thesis-final`, commit `7da5584b10f5aadeac64a1affa07f1eb22bd413d`. Preparation covered the root operating contract, specification, relevant living implementation-plan sections, README, [implementation synthesis](../implementation-research/SYNTHESIS.md), both earlier proposal/roadmap documents, all seven documents in the [18 October literature package](../implementation-research/thesis-literature-2026-10-18/README.md), the [evidence review](../analysis/thesis-extension-evidence-review.md), course analyses, [submission report](../reports/final-course-report-submission.md), and relevant I-01 source and verification records. The historical research archive was not needed for this decision.

This session used immutable, read-only connections to the four canonical course databases. All four integrity checks returned `ok`. Independent standard-library calculations of maxima and saved terminal submissions reproduced:

| Existing campaign | Physical attempts | Original team success | Retain / clear recovery | Both / retain-only / clear-only / neither | Revised scalar controls |
|---|---:|---:|---:|---|---:|
| [Course-7](../../notebooks/run/course-7-working/latest/run.json) | 252 | 3/20 | 2/20 / 2/20 | 1 / 1 / 1 / 17 | 15/20 |
| [Assisted-v2](../../notebooks/run/assisted-v1/latest/run.json), stored under `assisted-v1` | 356 | 10/20 | 2/20 / 3/20 | 0 / 2 / 3 / 15 | 18/20 |

The assisted stores also reproduce **32 entirely legal failed recoveries out of 35**, and **zero recovery submissions equal to the obsolete old maximum**. Selected exact requests confirm that a visible report of 949 was replaced in an agent's account by its own value 695; that prose promising to submit 954 accompanied `submit:null`; and that correct reports of 758 and 857 circulated without finalization. See the trace-linked [scientific analysis](../analysis/assisted-v1/scientific-analysis.md) and [existing exact-call table](../analysis/thesis-extension-evidence-review.md#22-current-raw-examples). These are observed association, information-use, and action failures. They do not reveal an internal belief or prove which intervention would fix them.

The earlier campaign did contain obsolete submissions; absence in the assisted campaign is not absence across all project evidence. Cross-campaign differences are descriptive because inputs, histories, interfaces, and schedules differ. Neither pooling campaigns nor attributing their difference to assistance is justified. The historical exploratory intervals remain as reported: Course-7 clear-minus-retain −10 to +10 percentage points; assisted −15 to +25 points. This session rechecked the decision-driving counts and three raw examples, not the entire forensic audit or those historical bootstrap runs.

| Evidence level | Current support | Boundary for this recommendation |
|---|---|---|
| Implemented | I-01 scalar task, alternating eligible actions, private finality, literal history, one admission owner, SQLite raw-before-effects persistence, bounded process execution, exact resume, export/reporting | New event types, balanced replacement population, repeats, stage limits, and Granite need scoped changes |
| CPU-verified | [Assisted implementation evidence](../validation/i01-assisted-implementation.md), including installed delivery, crash/restore/accounting and token checks; original thesis M1–M4 records | Historical named checks were inspected, not rerun or credited to the new design. The documented 108-test run had one wording failure and a focused correction; it is not an all-green run |
| Model-qualified | Historical Qwen qualification/readiness in its recorded course environment | Does not qualify the new prompt, all permitted contexts, new hardware, or Granite |
| Empirically executed | The two distinct course campaigns and their canonical artifacts | No proposed thesis cell, new model comparison, or new trial has been executed |

Dated README/specification handoffs that call assisted inference unrun precede the completed artifact; they are not the current outcome authority. Preserve them and the source/results they describe. The [existing evidence review](../analysis/thesis-extension-evidence-review.md) supplies the fuller inventory; duplicating that audit would not resolve the present design choice.

### 2.2 Why not make old commitments the main treatment?

| Candidate question | What its comparison identifies | What it does not identify | Decision |
|---|---|---|---|
| **Natural retain versus clear** | Total effect of retaining actual visible work after a fixed natural prefix, including evidence, errors, repetition, length, and interaction consequences | Pure evidence utility, an anchoring mechanism, or optimal selective memory | **Select.** Closest to the practical thesis question and the observed failures |
| Supplied source reports versus empty history | Effect of providing a complete historical evidence package | Whether agents naturally acquire that package; pure information versus presentation effects | Valuable controlled follow-up, but less direct for the practical claim |
| Identical supplied reports with versus without an old commitment, HS/HSC | Effect of adding that explicit historical field, including salience and length | Erasure of the old answer—it remains in reports—or a general reset benefit | Reject as primary. A clean but possibly small redundant-cue effect is not the strongest response to these failures |
| Literal removal of own submission fields from natural history | Effect of those fields, conditional on arbitrary old prose | Removal of conclusions repeated in messages; source-preserving recovery generally | Too narrow and inconsistently dosed for the principal question |
| Common source-label or coordination-prompt intervention | Effect of a specified instruction/presentation package | The effect of history policy independent of that package | Use one clear common interface, not a second main factorial |
| Original four-peer, five-family matrix | Rich task, evidence, teammate-reset and communication effects | Practical feasibility in these models without new qualification | Preserve the implementation; do not double its unaccepted model workload |
| Six supplied-history cells with two trials everywhere | Evidence availability and commitment exposure together | Natural end-to-end recovery; efficient allocation without variance evidence | Too much budget devoted to mechanistic arms and universal repeats |

This is a deliberate reversal of the latest recommendation, not a claim that its controlled estimand is invalid. The course results do not single out old commitments as the chief failure source. A natural policy effect remains interpretable when histories are poor: that is part of the population a practical reset policy encounters. Correct-prefix strata can describe a narrower situation, but cannot replace the main denominator.

The cost argument for supplied histories is weaker than it first appears. Four continuations and two scalar controls cost at most **26 calls per model/world**. A natural prefix adds six: **32 instead of 26**, a 23.1% increment, or 18.75% of the resulting total. At N=192, natural prefixes add 2,304 calls across both models. Removing the previous 32-world natural bridge saves 2,048. With the same repeat and preserving panels, the proposed main programme is therefore **15,424 rather than 15,168 slots: only 256 more**, while directly targeting natural recovery. These are different estimands, not equivalent designs made cheaper.

### 2.3 Literature that changes a decision

The earlier [source/version ledger](../implementation-research/thesis-literature-2026-10-18/sources-and-reading-ledger.md) and thematic reviews remain the broad literature base. A targeted independent search examined natural trajectories versus supplied evidence, distributed disclosure, recovery controls, repeated evaluation, and the official models. The following actual full texts and relevant appendices were consulted on 22 October; findings are not independently reproduced here.

| Primary source and checked version | Researchers' result and important scope | Decision or transfer hypothesis here |
|---|---|---|
| [Li, Naito and Shirado, distributed-information reasoning, v4, 13 May 2026](https://arxiv.org/html/2505.11556v4), §§3–6 and Appendix A prompts | Forced disclosure improves performance substantially in their selected hidden-profile tasks. A prompt requesting disclosure and mechanically appending all facts are different interventions. Their explanation emphasizes evidence surfacing | Preserve communication as an agent action. Our visible-evidence failures mean their diagnosis cannot simply be imported; supplying all old reports would change the problem |
| [Kwon, Reclaim Evaluation, v5, 21 July 2026](https://arxiv.org/html/2606.25449v5), note construction, §5.4 and source-size/noise appendices | Source preservation helps when templated lossy memories omit the recomputation basis; a source-plus-conclusion contrast can be much smaller. Planted erroneous commitments differ from formerly correct conclusions made stale by an edit | Source/conclusion separation is useful prior art, not evidence that HS/HSC is our most valuable primary contrast. No expected effect size is transferred |
| [Laban et al., LLMs Get Lost in Multi-Turn Conversation, v1, 9 May 2025](https://arxiv.org/html/2505.06120v1), simulation controls and Appendices L–N | Sharded instruction conversations reduce reliability in their tasks. Recap adds a turn; snowball changes presentation throughout. These are not controlled private factual revisions | Keep genuine histories and disclose assistance/call costs. Their result motivates a question; it does not establish that clearing will help here |
| [Useful Memories Become Faulty When Continuously Updated by LLMs, v2, 29 August 2026](https://arxiv.org/html/2605.12978v2), §§3–5, Table 4, Appendix K.1 | Episodic baselines can compete with consolidation; component ablations attribute much of the reported gain to episodes. Several inputs are successful or ground-truth trajectories, and table results are not uniform dominance | Newly followed lead: supports retaining raw-history baselines and examining provenance. It does not justify selecting successful prefixes or adding a consolidator. The authors' preferred memory architecture is not adopted |
| [Miller, Adding Error Bars to Evals, v1, 1 November 2024](https://arxiv.org/html/2411.00640v1), §§2–5 and Appendices A–C | Pairing, clustering, and within-item versus between-item variance change precision and repeat allocation | Analyze worlds, not calls; calculate the prefix-cost/repeat trade-off explicitly. A temperature change changes the evaluated system |
| Official pinned [Qwen card](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/README.md) and [Granite card](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/README.md), configs, generation files and templates | Native modes and supported configurations, plus vendor benchmark claims | Fix two explicit direct-mode systems. Cards are not accepted performance, memory, or throughput in this task |

Version checks matter: the newly followed memory paper has a v2, so the initial v1 access was not used as its final evidential version. The other named arXiv records matched the cited versions on this date. No claim of an exhaustive novelty search or a first-ever recovery study is made. The practical policy, natural-history population, actual private edit, and private action endpoint define the contribution if executed.

## 3. Exact proposed task, population, and information

### 3.1 World distribution

Each agent owns twenty indexed integers. Propose all forty values independently uniformly from **−1000 through 1000**, preserving original order. Require a unique old maximum `M1`, and let `M2` be the maximum of the other thirty-nine records. Assign the old winner's owner in advance. Require `M2 > −1000` and a nonempty set `{M2+1,…,1000} minus {M1}`. The latter excludes ceiling cases in which a different winning replacement is impossible. All main worlds must support both revision types, avoiding different mathematical eligibility across types.

Generate in eight equally weighted strata: **edit type × old-winner owner × first speaker**, two values each. Condition proposals on the assigned winner owner and the common mathematical eligibility; do not condition on model behavior. Select the unique winner's record and sample one saved replacement:

| Main revision stratum | Replacement | Revised answer | Information consequence |
|---|---|---|---|
| Winner demoted | Uniform integer in `[−1000,M2−1]` | `M2` | Complete old reports permit an outcome-scoring deletion shortcut; natural summaries may omit the required runner-up |
| Winner remains | Uniform integer in `{M2+1,…,1000} minus {M1}` | Replacement | A correct non-owner answer requires new information depending on the private replacement, or an unsupported guess |

“Winner remains” can increase or decrease the numerical maximum; it is not an increase-only population. The revised maximum may have multiple occurrences in the demotion stratum; scalar scoring is unambiguous. Do not require `M2` to belong to the other agent. Its location, edit size, and historical coverage are offline descriptors, not extra selection criteria or primary factors.

Bound generation at 1,000 proposals per world and save rejection reasons/counts. Failure to generate a slot stops preparation; it does not license a model-dependent replacement. Use separate saved streams for inputs, replacement, assignment/order, prefix calls, continuation calls, and controls. Proposed master/bootstrap seeds are `2026102201` and `2026102202`; they are not generated manifests or an adopted freeze. Save actual arrays, edits and exact integer seeds. Check exact complete-input overlap against accessible historical/development manifests before release; seeds alone do not prove separation.

There are **8 qualification worlds, 16 development worlds, and 192 main worlds**: 216 independent base worlds, or 152 at fallback. Qualification and development are disjoint from main and from each other. Eight supplied diagnostic calls derive views from qualification inputs; they are not eight additional independent worlds. The repeat and preserving panels are subsets of main. No additional natural bridge or supplied-history main cohort is scheduled.

### 3.2 What each peer may see

Every call gives one common task/strategy instruction, the agent's identity and own invocation count, partner-finished status, its permitted history, the current environmental notice, and its **current authoritative private shard**. Use explicit owner-qualified labels such as `agent-0:record-13`, constructed from existing identities. Keep history before notice/current source as in the assisted renderer; do not sort values or highlight maxima.

At a real edit, both peers learn the changed owner and record. Only the owner sees the replacement in its notice/private shard. The public rule says exactly one named record changed. It does not reveal that it was the old winner, its replacement range, the edit stratum, whether the answer changed, any gold value, or any future edit. A peer report is ordinary unverified text. The host never refreshes the partner's historical report, computes a maximum for peers, or certifies a reported value.

The evaluator alone sees both complete shards, old/new gold, eligibility, stratum, policy IDs, seeds, selected panels and counterfactual edits. Partner submissions remain private unless messaged; the finished flag discloses status only. No hidden KV/recurrent state, earlier thinking, other world's transcript, other model's history, or sibling outcome crosses a call boundary.

### 3.3 Natural versus supplied histories

Acquire **one original episode per model/world**, at most six calls. Its actual terminal snapshot becomes the common parent of all that model's sibling continuations and repeat trials. A wrong submission, no submission, deadlock, invalid action, or recorded timeout stays in the sample. Raw rejected output stays in the audit store; only the feedback that was actually visible enters peer history. Do not fill missing reports, replace errors with solver results, or choose a better prefix.

The population thus averages over generated worlds, a natural prefix from the fixed model/interface, and subsequent sampled behavior. It is **not recovery conditional on competent original collaboration**. Report correct-prefix and incorrect/incomplete-prefix strata with their full denominators, explicitly descriptive. With one prefix per world, repeated continuations do not establish robustness to regenerating that world's prefix.

Supplied full old reports would answer a valuable conditional question: can a team recover once a competent evidence basis is guaranteed? The edited owner would immediately have its current shard and the unchanged remote shard, partly centralizing recovery. Such fixtures cost no model prefix calls but do not demonstrate evidence acquisition. A 32-world natural bridge would only illustrate transfer limitations: it changes content, mistakes, length, provenance and often the policy itself, has wide uncertainty, and cannot transport an HS/HSC effect to natural histories. At discordance .50, its approximate 95% direct-effect half-width would be 24.5 percentage points near zero, before considering the change of estimand. **Because the intended claim is practical natural recovery, make natural histories the main population instead.** Supplied views remain eight bounded diagnostics and CPU illustrations, never pooled thesis outcomes.

## 4. Policies, phase boundaries, controls, and actions

### 4.1 Four main cells

| Cell | Sources and notice | History at reopening |
|---|---|---|
| Retain / revision | Saved revised own shard; real changed-record notice | Literal own visible prefix history |
| Clear / revision | Identical sources/notice to retain / revision | Empty |
| Retain / no change | Original own shard; truthful no-change reopening notice | Same literal prefix history |
| Clear / no change | Identical sources/notice to retain / no change | Empty |

Retain copies the valid own actions, received messages, own explicit submissions, and public rejection feedback actually visible in the original episode, preserving text and order. It does not copy the partner's private actions. Clear removes all those historical fields. Neither policy changes current sources, common instructions, notice, opportunities, or scoring. Both accumulate ordinary new history after the boundary. The intervention is applied once, not as continual deletion or summarization.

**Every declared continuation boundary reopens both agents, including no change.** Set both active, waiting false, current-phase submissions null, invocation counters zero, current-phase deliveries/events empty, and next speaker to the saved first speaker. Start from a drained immutable parent snapshot, including any messages already delivered before original termination. Historical submissions remain final actions of the old phase and never serve as current submissions. Later messages cannot reopen an agent within a phase. The common instruction must explicitly replace the old “only a source change reopens” rule with this phase-boundary rule.

A no-change notice states that no source changed and a new decision phase begins; it names no counterfactual edit or record. A real-edit notice states that the named record changed and a new decision phase begins. Thus the event contrast concerns **source change plus its truthful notice**, not an isolated hidden-data mutation. The reopening mechanism and action budget are identical.

### 4.2 Interaction and finality

Retain the assisted I-01 strategy: establish relevant local maxima, compare the necessary evidence, and communicate needed information before finishing. The host suggests this strategy but does not enforce exchange, fresh-message acquisition, consensus, acknowledgment, a designated leader, or a vote. The new labels and phase wording are common to both models and all cells; their benefit is not separately identified.

Actions remain exactly `message`, `submit`, `wait` in one strict JSON object. Message is nonblank text or null, submission a strict integer or null, waiting boolean. Wait excludes both other actions; an empty non-wait action is invalid. No coerced integer, duplicate key, extra field, fence, nonfinite value, truncated fragment, or repaired text is accepted. Whole-reply invalidity delivers nothing and consumes the invocation. Public-rule feedback, at most 32 native tokens, may appear on a later eligible call; it gives no numerical correctness information or extra turn.

Agents alternate when eligible, with **at most three invocations each** and no transferable turns. Messages are delivered before the next eligible call. Send-and-submit delivers the message then irreversibly finishes its sender. Waiting wakes only on a delivered message; delivery to a finished peer is archived and does not undo finality. Stop when both submit or no unfinished agent can progress because of waiting/exhaustion. Never stop on correctness. This is the existing sequential I-01 contract, not the original thesis's synchronous provisional-candidate protocol.

Use fresh call-owned hidden state. Persist the exact request/settings/seed, then raw outcome before effects; exact resume consumes the saved outcome, including invalid outcomes. No continuation reply is shared across policies, events, models or trials. Matching invocation seeds is a coupling, not replay. Only an infrastructure attempt without a durable outcome and with confirmed prior termination may receive one identical retry. Recorded wrong, malformed, truncated and timeout outcomes do not earn a retry.

### 4.3 Necessary controls and the preserving panel

Run one original and one revised **full-information scalar control** per main model/world. Each sees all forty values and returns one submission without messaging. These controls distinguish elementary maximum extraction from the distributed action problem; their prompt/access differ, so a control-team accuracy gap is not an isolated coordination effect. Never feed their answers into a team.

On the first four main worlds per stratum (32 total), save an additional **answer-preserving edit** before inference: choose uniformly one of the assigned owner's nineteen nonwinning records, then uniformly a different integer below `M1`. The old winning record stays unchanged. Run retain and clear once each, from the same original prefix, plus one preserving scalar control per model/world. All 32 worlds lie in the nested fallback. The common real-edit notice does not say that the answer is preserved.

This is different from no change: a source really changes and must be interpreted, even though gold is unchanged. The probe can reveal unnecessary damage after a real edit. It is descriptive, with N=32 and intentional overlap with main; it is not a third powered event or new independent cohort. No control or probe is replicated solely because it failed.

## 5. Worked information and action examples

**All examples below are illustrative deterministic constructions, not experimental findings.** Short shards stand in for twenty-record shards; additional records can be lower values without changing the argument.

Suppose agent A owns `[90,80]`, B owns `[70,60]`, and the old global answer is 90.

| Situation | Evaluator knows | A's initial allowed continuation view | B's initial allowed continuation view | What follows |
|---|---|---|---|---|
| A's first value changes to 10 | Gold is 80 | Current `[10,80]`; notice names A:0; whatever history A actually had | Current `[70,60]`; A:0 changed; B's own history, without 10 | Complete old reports permit deletion of 90 to return 80. Without a fresh report, B has not established that the replacement is below 80 |
| A:0 changes to 85 or 95 | Gold is respectively 85 or 95 | Current shard includes the private 85 or 95 | The same own shard, same old history and same notice in both worlds | B cannot distinguish the two correct answers before new communication. Information depending on the replacement must arrive, perhaps as a reported current maximum; an exact guess is still scored normally |
| A:1 changes from 80 to 65 | Gold remains 90 | Current `[90,65]` | Real notice names A:1; value remains private | A real answer-preserving revision; repeating 90 may be justified, unlike blindly preserving every old answer |
| No record changes | Gold remains 90 | Original shard and no-change notice | Original shard and no-change notice | Both agents still need new formal submissions in the reopened phase |

**Useful history.** With original A=`[90,60]`, B=`[80,70]`, B previously reported its local maximum 80. After A's 90 becomes 50, A sees `[50,60]` and can use the unchanged B report to conclude 80, without reacquiring B's entire shard. It must still get appropriate information to B before finishing. In clear, that earlier report is unavailable and must be reacquired or guessed. Accuracy of the old report is a property checked offline, not host certification in the live view.

**Harmful or irrelevant history.** An old own submission of 90, or a repeated recommendation to answer 90, is wrong after the first example's edit. A retained instruction to keep waiting can also lead to noncompletion without any stale numerical submission. Conversely, an irrelevant old greeting need not help at all. These are possible pathways; observing the text does not prove its causal role. If natural history retained only “global answer 90,” it does not reveal the missing alternative 80.

**An utterance is not a submission.**

```json
{"message":"The current global maximum is 80; I will submit it.","submit":null,"wait":false}
```

This sends a claim and leaves the sender unfinished. By contrast,

```json
{"message":"My current maximum is 80.","submit":80,"wait":false}
```

sends the explicit report and commits 80 privately. Both peers must commit the correct current value for team success. The host must not infer a submission from the first message, even on the last available turn. A legal but wrong submission is final; a later correct peer message cannot repair it.

**Why the extension is sufficient.** Winner-remains counterexamples defeat a uniformly successful deletion shortcut even when history is complete. They do not prove that every successful model used sound reasoning, nor require verbatim transmission of the raw replacement: any message conveying sufficient replacement-dependent information can work. The hidden balanced mixture must never be disclosed as a solution rule.

## 6. Why keep maximum rather than add another task?

The smallest worthwhile alternative is **two-agent top-two selection**, preserving multiplicity and requiring an ordered pair of current largest values. It would add partial-answer preservation and reserve retrieval: after lowering the old largest item, the old top-two result can omit the third value now needed. This is a real scientific extension, not just another numerical benchmark.

It is nevertheless weaker as the first recommendation. The current I-01 parser/action endpoint accepts a scalar; top-two needs a new output contract, exact shape/multiplicity checks, generator/edit eligibility, capability qualification and report semantics. The original thesis's Top-K solver offers mathematical reuse, but its four-peer top-ten task and execution semantics are not a drop-in two-agent study. Lowering a winner below the cutoff can still admit an old-table shortcut, so adding Top-K does not itself solve the information problem.

At a similar call budget, splitting the 192 worlds over two tasks leaves approximately 96 per task before extra qualification costs, increasing each task's standard error by roughly √2 at equal variance. A pooled effect would hide task differences; a task-by-policy interaction would be less precise. Prefix Sum would more directly test reuse of a calculation, but adds arithmetic/output-placement and historical-operand issues that may restore a competence floor.

**Choose maximum with the two edit strata.** It already separates useful historical evidence, required new private information, and final action with minimal new mathematics. Accept its limitation: it does not measure preservation of expensive computation or generalize to multi-step plans, Top-K vectors, graphs, or four-agent teammate-reset effects. If those are essential thesis claims, this candidate should be rejected explicitly rather than decorated with an underpowered extra task.

## 7. Model systems and a fair comparison

Use these **specific previously inspected revisions**, not a moving `main` branch:

| Setting | Qwen3.5-9B | IBM Granite 4.2-8B |
|---|---|---|
| Repository | `Qwen/Qwen3.5-9B` | `ibm-granite/granite-4.2-8b` |
| Selected revision | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | `f8de16cdcdbc6c779ca517604e050d82cc119e44` |
| Direct mode | Native template `enable_thinking=False` | Native template `enable_thinking=False`, `low_effort=False`, no low-effort reasoning override |
| Sampling | Temperature .7, top-p .8, top-k 20 | Temperature 1.0, top-p .95, explicit top-k 0 |
| Common settings | Sampling on; min-p 0; repetition penalty 1; presence penalty 0; one beam; no constrained decoder | Same |
| Context/output | At most 8,192 native input tokens plus 512 generated tokens | Same numerical caps, own native tokenizer |
| Numerical regime | Text-only NF4, double quantization, FP16 computation with required FP32 sensitive operations | Same declared quantization/compute policy through the maintained Granite path |

The live Hub metadata check still resolved Qwen to the selected revision. **Granite's current head was `a7042144125ce5ae64f89610e8289647fc000b9a`, updated 20 October**, according to the [Hub repository metadata](https://huggingface.co/api/models/ibm-granite/granite-4.2-8b) accessed on 22 October. This session fetched the selected older revision's small card/config/template metadata. It did not download tensors or establish whether the newer head changes weights. Keep the selected revision; Prompt 2 must document availability and compatibility without silently upgrading it. A later checkpoint change is a scientific/configuration amendment.

Qwen's card lists several task/mode presets, including presence penalties and much longer output recommendations. The selected course-aligned general direct preset deliberately omits presence penalty to avoid penalizing legitimate schema/ID repetition. Granite's [generation configuration](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/generation_config.json) specifies sampling, temperature 1 and top-p .95; unrestricted top-k is an explicit study choice rather than an inherited framework default. These bounded direct systems are not the cards' unrestricted reasoning benchmark conditions.

Both native templates insert an empty thinking prefix for direct mode. Archive only the generated suffix as response, preserving raw IDs/text and validated native termination handling; do not strip arbitrary generated thinking or malformed text to rescue JSON. Render historical actions as literal labeled user data, not a sequence of native assistant turns that may rewrite history. Freeze all actual EOS/pad/BOS, template, decoding and numerical settings. Native [Qwen](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/chat_template.jinja) and [Granite](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/chat_template.jinja) templates need separate tests.

Fairness means identical semantic inputs, source privacy, phase/action rules, common instructions, cell schedule, output requirements, and **equal prospective development opportunities**. It does not mean identical tokenization, equal effective randomness from the same integer seed, or equal numerical sensitivity to NF4. Use one model-native sampler per system, with no thinking or smaller-model fallback. A common-temperature arm would answer another question and is not budgeted. Historical Qwen interface development is an asymmetry that equal future budgets cannot erase; disclose it.

The primary comparison is within each model. Cross-model results are a replication across two configured systems, including their naturally different prefixes, templates, decoding and quantization behavior—not an architectural causal comparison or the same-history ability test. Published instruction-following, reasoning and agentic benchmark scores do not establish maximum extraction, ownership interpretation, legal action or finalization here.

For the 8,704 resident-token envelope, the ordinary FP16 full-attention KV components derived from the pinned [Qwen config](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json) and [Granite config](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/config.json) are:

`2 × layers × KV heads × head dimension × tokens × 2 bytes`:

- Qwen: eight full-attention layers, four KV heads, dimension 256 → **0.265625 GiB**, plus its recurrent state.
- Granite: forty layers, eight KV heads, dimension 128 → **1.328125 GiB**.

These are tensor calculations, not total resident memory or T4 acceptance. Weights, unquantized components, prefill/workspace, allocator and runtime overhead remain. Granite's native configured position limit is 131,072; advertised extensions are irrelevant to this short-context proposal. Start the feasibility investigation with one replica per T4, batch one, no offload or cross-device split, and **at least 1.5 GiB measured free headroom on each used device** at the full allowed envelope. Two T4s do not form one memory pool. A different hardware class requires an explicit prospective decision, not an automatic escape path.

## 8. Trial schedule and analysis contract

### 8.1 Fixed allocation and order

The target is 24 main worlds per eight-way stratum. The fallback is the first 16 per stratum (128 total), selected only using resources before any main prefix or control is run. First speaker is the same across original and all continuation phases. Each model independently acquires its prefix on the same mathematical world.

Trial 0 in all four cells is the primary dataset. The first three worlds per stratum (24 total) receive **trials 1 and 2 in every cell**, reusing the exact original prefix and using independent continuation streams. Do not replace trial 0, average the repeat panel into the primary estimate, or choose the best result. Report per-cell 0/1/2/3 successes and policy-discordance changes on this panel, with world-level summaries. It measures conditional continuation repeatability, not three independent worlds or prefix-generation stability.

Counterbalance all four cell positions. One concrete schedule uses all 24 cell permutations once in each target stratum; organize them in six four-permutation cyclic groups so the first four groups form a position-balanced 16-world fallback. Randomize the group/base ordering prospectively. Balance original/revised scalar-control order separately. Balance repeat trial/cell order in saved blocks. Rotate models and physical device assignment across blocks; keep a model/world's siblings on the same logical device. Prefix dependencies, exports and reload checks constrain order, but model outputs never choose the next condition. Prompt 2 should map this finite schedule to sessions without losing those balances.

Use the existing stable-ID seed mechanism with explicit new regime/model/world/trial/agent/invocation keys. Prefix and control streams are separate. Within a model/world/trial, match per-agent invocation seeds across policy/event siblings while excluding those treatment labels from the sampling key. IDs for physical calls still distinguish every cell. Cross-model streams are separate. Exact seed integers must never pass through floating-point prose/JSON rendering that loses precision.

### 8.2 Primary estimands and sign

Let `Y[m,w,p,e,r]` equal 1 if **both** agents submit the exact current maximum before ordinary phase termination, and 0 for a known terminal failure. An unresolved/unexecuted episode is unknown. Let `p` be clear C or retain R, `e` revision V or no change N, and `r` continuation trial. Define:

```text
D[m,w] = Y[m,w,C,V,0] - Y[m,w,R,V,0]
Delta[m] = (1/8) sum over strata s E[D[m,w] | s]
```

There are **two primary estimands: Delta[Qwen] and Delta[Granite]**. Positive favors clear. Their population includes the specified input/edit generator, each fixed model's unfiltered natural prefix distribution, and continuation sampling under the fixed interface. The unit is the whole world/prefix bundle; agents, calls, cells and repeats are not independent sample units. Equal stratum weights give equal edit-type weight, not the prevalence of edits in a real deployment.

The direct effect answers: **after the specified change, how much does clearing improve or harm the probability that the team finishes correctly?** It includes all downstream changes in communication and finality. This is a total policy effect, not a pure memory mechanism.

Prespecify the secondary interaction:

```text
I[m,w] = (Y[C,V,0] - Y[R,V,0]) - (Y[C,N,0] - Y[R,N,0])
Theta[m] = equal-stratum mean of I[m,w]
```

Positive theta means clearing becomes relatively more favorable when a source changes. It does not by itself imply successful recovery. For example, revision rates .20/.20 for clear/retain and no-change rates .40/.80 yield `Delta=0`, `Theta=+.40`. This is a constructed example. It shows why **all four means, the direct effect and no-change contrast must accompany the interaction**. No parallel-trends assumption is needed for these matched interventions, but the interaction still includes the truthful notice difference.

Report separate edit-stratum estimates and the direct cross-model contrast `Delta[Qwen]−Delta[Granite]` descriptively with their uncertainty. One model's interval excluding zero while another's includes zero does not establish that models differ. Prefix-success conditional estimates and preserving-panel effects are descriptive, not extra primaries.

### 8.3 Uncertainty, multiplicity and missingness

Use 10,000 seeded paired bootstrap resamples of whole worlds **within all eight strata**, carrying both models and all associated main cells together. Main estimates use trial 0 only. Analyze panels separately: resample three complete world bundles per stratum for repeat-panel summaries and four per stratum for the preserving panel, keeping their models/cells/trials paired; never treat the overlapping panels as extra independent main observations. Use type-7 percentile quantiles, explicitly replacing neither historical report conventions nor their intervals. Give each primary a **97.5% two-sided interval** (Bonferroni allocation of .025 per model); familywise protection is approximate because bootstrap coverage is approximate. Secondary 95% intervals are labeled descriptive, without a catalogue of significance claims or post-hoc endpoint promotion.

Freeze the constant/degenerate rule. If a contrast has zero empirical within-stratum variation or its bootstrap endpoints coincide, display that empirical interval **and** a conservative weighted Hoeffding companion clipped to the mathematical range. With stratum weights `a_s=1/8`, counts `n_s`, range `[L,U]`, and chosen tail probability alpha, its half-width is:

```text
h = (U-L) * sqrt( log(2/alpha) * sum_s(a_s^2/n_s) / 2 )
```

Use `[−1,1]` for direct effects, `[−2,2]` for revision interactions and the difference of two model-specific direct effects, and `[0,1]` for cell rates. For primary direct effects, alpha=.025 gives **21.4 pp at N=192**, **26.2 pp at N=128**. That deliberately conservative companion prevents an all-zero empirical interval being presented as certainty. A degenerate primary does not support superiority unless the companion also excludes zero; no equivalence conclusion is planned. Report discordant counts even when the bootstrap is not degenerate.

Preserve the four paired categories for each event: both succeed, only clear, only retain, neither. Show correct/wrong/absent commitments over the fixed two-agent denominator; completion, wrong agreement/disagreement, terminal reason, legal/illegal calls and coverage. Malformed output or a confirmed timeout consumes an invocation; a later allowed call may still succeed. Only the **terminal episode** determines Y. Unused opportunities after lawful early termination are neither failures nor missing observations.

Known terminal noncompletion is zero. Unexecuted episodes, interrupted unfinished phases and unresolved attempts remain unknown. Publish the intended denominator, settled coverage and feasible lower/upper completion bounds by varying unknown binary endpoints jointly through each estimand, preserving shared-prefix dependencies and known results. Do not turn complete cases into the target population or assign zero to unknown time. If a missing prefix prevents sibling construction, keep all dependent scopes unknown until exact restoration. Separately display sampling uncertainty and incomplete-execution bounds.

An independently verified input/protocol/evaluator defect can invalidate affected measurements, but repair requires disclosure and a prospective decision for all affected matched scopes. Ordinary scientific failures never justify rerunning, replacing worlds, expanding sample size or relaxing a gate.

### 8.4 Precision and the repeat trade-off

For paired binary D, discordance `q=P(D≠0)` gives `Var(D)=q−Delta²`. The following **analytic sensitivities, not model measurements or simulated results**, use near-zero effect and normal approximations. The actual stratified variance can differ; no course or pilot variance is treated as known.

| Assumed discordance q | N=192: approximate 97.5% half-width | N=192: approximate 80% detection reference | N=128: half-width | N=128: detection reference |
|---:|---:|---:|---:|---:|
| .10 | 5.1 pp | 7.0 pp | 6.3 pp | 8.6 pp |
| .20 | 7.2 pp | 10.0 pp | 8.9 pp | 12.2 pp |
| .50 | 11.4 pp | 15.7 pp | 14.0 pp | 19.3 pp |
| .80 | 14.5 pp | 19.9 pp | 17.7 pp | 24.4 pp |
| 1.00, worst marginal variance near zero | 16.2 pp | 22.2 pp | 19.8 pp | 27.3 pp |

Formulas are `2.2414 sqrt(q/N)` and `3.0830 sqrt(q/N)`. At q=.30, a 5-point effect needs roughly **1,141 worlds** and a 10-point effect **286**, using the same near-null approximation; using `q−Delta²` gives 1,132/276. These are planning references, not exact discrete-test power. N=192 has only 96 worlds per edit stratum, N=128 only 64. The N=32 preserving panel cannot rank small policy differences reliably.

Interactions may be noisier. For world-interaction SD .5/.8/1.0, approximate descriptive 95% half-widths are **7.1/11.3/14.1 pp** at N=192 and **8.7/13.9/17.3 pp** at N=128. SD can reach 2 in principle. An interaction is not granted the direct contrast's discordance-based precision.

For repeats conditional on one prefix, write variance approximately as `(A+B/R)/N`, where A includes differences between worlds and realized prefixes and B is continuation variance of the paired contrast. Ignoring auxiliary panels, the cost is `N(8+24R)` calls per model: six prefix and two scalar calls are fixed acquisition costs, while each trial costs four six-call cells. At fixed cost, moving from R=1 to R=2 has variance ratio `1.75(1−f/2)`, where `f=B/(A+B)`. It helps only if f exceeds about **.857**. At f=.25/.50/.75/.90, the ratios are **1.531/1.313/1.094/.963**. The 192-world R=1 budget supports only about 109.7 worlds at R=2 before balance/integer constraints. No evidence establishes such dominant continuation variance here. Prefer more worlds and the fixed repeat panel. This derives an allocation choice, not an optimality claim from a small pilot.

**Precision gate:** accept a study of moderate/large policy effects and useful coarse bounds. Predeclare 10 pp as a practical reporting reference, not a promised detection limit or equivalence margin. The target's worst-variance approximate half-width is below 17 pp; fallback's below 20 pp. If reliably detecting 5 pp, or uniformly excluding 10 pp, is essential, neither sample passes that purpose. Do not let an unusually favorable pilot discordance authorize a smaller sample. There is no efficacy/futility peeking or outcome-adaptive stopping.

### 8.5 Informative outcomes and process evidence

| Result pattern | Defensible conclusion |
|---|---|
| Positive direct effect with substantial clear success | Clearing improves this practical recovery package; show which worlds are gained and lost and its costs |
| Negative direct effect | Retaining actual history helps in this regime; useful unchanged evidence is one possible explanation, not an isolated cause |
| Positive interaction but direct effect near zero | Clearing is relatively less harmful after change; this alone is not recovery improvement |
| Good no-change and scalar performance, poor revision in both policies | An observed change-dependent recovery deficit; trace evidence can locate visible information/action failures without diagnosing a unique mechanism |
| Low original/no-change performance in main despite development passage | Baseline competence did not generalize. Report a floor-limited policy result and the failed screening generalization; do not substitute a model |
| Null with narrow enough bounds for a stated practical decision | Bound large effects in this regime; do not claim universal memory irrelevance |
| Null or mixed estimates with wide intervals | Inconclusive ranking, with useful rates, gain/loss patterns and feasibility limits |
| Strong differences between edit types or model systems | A boundary of the result needing the actual difference estimate; no post-hoc new primary or pooled winner |

Freeze an eight-world qualitative panel, one per stratum, both models and all four trial-0 cells: 64 continuation episodes, at most 384 calls already in the budget. Inspect exact permitted views for current evidence availability, unambiguous owner/value associations, correct current-result utterances, actual submissions, waiting and finality. Preserve “ambiguous” and “not expressed” categories. A peer can solve without verbalizing every step. Automated facts cover numeric submissions, timing, legality and literal availability; semantic interpretation needs trace references. Independent double-coding is desirable if a reviewer is available; do not claim it happened or substitute an LLM judge. No new inference is needed for annotation.

## 9. Complete physical-call budget and policy costs

All counts are **maximum first-attempt slots**, assuming every team episode uses six calls. Early termination may use fewer; it never buys more worlds or replacement trials. Preparation, controls, diagnostics and reload tests are charged. No unlisted warmup call is free.

### 9.1 Development and initial qualification: expanded stages

Use **one frozen common candidate**, with equal prospective opportunities for both models. There is no prompt-search reserve or automatic alternative mode. A scientifically changed candidate requires a new explicit amendment, fresh development data, and a new cost decision; the contingency below cannot fund it.

| Initial stage | Exact scope per model | Per-model slots | Both-model slots |
|---|---|---:|---:|
| Offline preparation | Source, deterministic fixtures, token proof, schedule, analysis and restore checks; no model generation | 0 | 0 |
| Initial replica readiness | Two intended replicas: A/B/A isolation checks plus one full 8,192+512 envelope per replica | 8 | 16 |
| Scalar qualification | Eight disjoint worlds, one per stratum; original and revised scalar actions | 16 | 32 |
| Supplied-view diagnostics | Two one-call fixtures each for local extraction, owner/record interpretation, using an available peer report, and formal-action/finality rules | 8 | 16 |
| Development prefix acquisition | Sixteen disjoint worlds, two per stratum, one natural original episode each | 96 | 192 |
| Development retain / revision | 16 × 6 | 96 | 192 |
| Development clear / revision | 16 × 6 | 96 | 192 |
| Development retain / no change | 16 × 6 | 96 | 192 |
| Development clear / no change | 16 × 6 | 96 | 192 |
| Development scalar controls | Original/revised once per development world | 32 | 64 |
| **Initial total** | `8+16+8+16×32` | **544** | **1,088** |

Diagnostic targets must be frozen from allowed fixture information before model calls. Local/ownership probes can explicitly request a local scalar; available-report probes can request a global formal submission; finality probes use predefined legal-action targets. They are diagnostic tasks with additional directives, not natural recovery outcomes or teaching calls. Require complete raw evidence; report every nonpass. Their aggregate accuracy has **no admission threshold**, because forcing a favorable response on these artificial views would not qualify natural interaction.

### 9.2 Main programme, panels and contingency

| Component | Target per model | Target both models | Fallback both models |
|---|---:|---:|---:|
| Natural prefixes: N × 6 | 1,152 | 2,304 | 1,536 |
| Retain / revision, trial 0: N × 6 | 1,152 | 2,304 | 1,536 |
| Clear / revision, trial 0 | 1,152 | 2,304 | 1,536 |
| Retain / no change, trial 0 | 1,152 | 2,304 | 1,536 |
| Clear / no change, trial 0 | 1,152 | 2,304 | 1,536 |
| Original scalar controls: N | 192 | 384 | 256 |
| Revised scalar controls: N | 192 | 384 | 256 |
| Repeat retain / revision: 24 × 2 extra trials × 6 | 288 | 576 | 576 |
| Repeat clear / revision | 288 | 576 | 576 |
| Repeat retain / no change | 288 | 576 | 576 |
| Repeat clear / no change | 288 | 576 | 576 |
| Preserving retain: 32 × 6 | 192 | 384 | 384 |
| Preserving clear: 32 × 6 | 192 | 384 | 384 |
| Preserving scalar controls: 32 | 32 | 64 | 64 |
| Separate natural/supplied bridge, regenerated prefixes, additional tasks | 0 | 0 | 0 |
| **Main and panels subtotal** | **7,712** | **15,424** | **11,328** |
| Initial qualification/development above | 544 | 1,088 | 1,088 |
| Additional unchanged-runtime replica readiness | At most ten reloads × four calls | 80 | 80 |
| Infrastructure retry/reconciliation reserve | Global shared cap, not 600 per model | 600 | 600 |
| **Campaign attempt ceiling** | No independent reset of shared reserves | **17,192** | **13,096** |

Main formula: `2×[32N + 24×4×2×6 + 32×13]`. Campaign formula adds 1,088+80+600. All extra readiness is at most twenty replica reloads in total, ten per model, in addition to two initial replicas per model. One device may reduce initial/reload use but does not release slots for extra scientific work. At two replicas loaded together, the allocation allows up to six such load sessions per model; Prompt 2 must prove that its actual session plan fits. Readiness failures and eligible infrastructure retries consume their applicable ceilings and the global ceiling. Renaming directories or restoring a checkpoint never resets spending.

**Physical versus logical costs.** Each natural prefix is generated once physically. For a hypothetical deployed policy, charge that prefix plus that policy's continuation; it is not free because the experiment shares it. Recovery-only cost excludes the prefix and is reported separately. Controls, diagnostics and all alternative cells are research overhead, not runtime work of a single deployed policy. Repeats are evaluation cost, not best-of-three deployment. Report calls, input/output tokens, all-attempt ready time and allocated GPU time separately, beside quality. A quick wrong submission or deadlock can be cheap; do not combine accuracy and time into an invented utility score.

## 10. Conservative resource scenarios and feasibility gates

### 10.1 Hours, downloads, loading and interruption

Real throughput for this proposal is **unmeasured**. Historical short Qwen calls do not establish Granite throughput or full-envelope cost. Use aggregate allocated device-hours, including idle devices assigned to the session. Two simultaneously assigned GPUs halve ideal elapsed compute time only when both are used; they do not halve aggregate hours.

For conservative screening, separate ordinary scientific calls from expensive readiness/contingency. The target contains **16,496 scientific slots**, fallback **12,400**, plus **96 initial/reload readiness calls** and **600 contingency attempts**. Price readiness and contingency at the provisional **180-second call deadline**, rather than the ordinary-call average. Reserve another 24 aggregate GPU-hours for non-call allocation:

| Non-call category | Screening reserve | What must be measured or bounded |
|---|---:|---|
| Online code/dependency/model download and verification | 6 h | Network, caches, duplication and whether GPUs are already allocated |
| Model loads and device initialization | 4 h | All intended initial/reload placements, including failed loads |
| Checkpoint creation, transfer, verification and exports | 4 h | Per-cell receipts plus durable snapshot cadence and final off-session copy |
| Allocated idle/operator/session transitions | 6 h | Include assigned unused second-device time; do not count only busy workers |
| Interruption cleanup and restoration overhead | 4 h | Termination, recovery, evidence reconciliation and emergency export |
| **Non-call reserve** | **24 h** | Exclusive categories; no double charging the same interval |

For a common assumed per-call allocated contribution `g` seconds (generation plus assigned between-call overhead once):

```text
H = 24 + 96×180/3600 + 600×180/3600 + 1.25×S×g/3600
  = 58.8 + 1.25×S×g/3600
S = 16,496 target; 12,400 fallback
```

The 25% scientific-call margin and explicit deadline-priced contingency are conservative planning allowances. They are not a probabilistic completion guarantee. A meaningful measured forecast must replace common g with per-model/stage durations and actual remaining counts, use the slower eligible device, and include actual expenditure plus remaining reserves exactly once. Use the maximum observed ordinary development duration within each model/stage category as the starting forecast input, including failures; for an unmeasured preserving category use that model's largest comparable scientific duration. A small-sample maximum is not a proven tail bound. Full-envelope readiness remains separately deadline-priced. Unknown exposure/allocation cannot be assumed zero. If the deadline changes, recompute all affected reserves before freeze.

| Assumed g | Target N=192 | Fallback N=128 |
|---:|---:|---:|
| 10 s | 116.1 aggregate GPU-h | 101.9 aggregate GPU-h |
| 15 s | 144.7 | 123.4 |
| 20 s | 173.4 | 144.9 |
| 25 s | 202.0 | 166.4 |
| 30 s | 230.6 | 188.0 |
| 45 s | 316.6 | 252.6 |

Under this screening formula, 200 hours requires g ≤**24.65 s** for target or **32.79 s** for fallback. The original thesis's 100-hour ceiling would require ≤**7.19/9.57 s** respectively. These thresholds explain why 200 hours is a substantive requested amendment. They do not establish that even the fallback fits Kaggle. The 20-second target scenario corresponds to about 86.7 ideal two-device wall-hours, or at least nine ten-hour allocated session equivalents if that entire envelope is spent. Actual calls may finish earlier and reserves may remain unused. Ten hours here is a planning example, not a verified Kaggle entitlement or limit.

The pinned tensor indexes list approximately **19.31 GB for Qwen and 16.76 GB for Granite**, excluding file/serialization overhead: about 36.07 GB total, not quantized device footprints. At an assumed sustained 5 MiB/s, one cold download of both takes about 1.91 wall hours; two assigned GPUs would charge about 3.82 GPU-hours. Repeating that transfer over sessions could exhaust the six-hour download reserve. Source/dependency downloads add time. Prompt 2 must resolve caching/staging and actual disk limits rather than assume both checkpoints fit in persistent notebook output. Inspect [Qwen's index](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/model.safetensors.index.json) and [Granite's index](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/model.safetensors.index.json) when preparing the exact asset list.

Provisional load/call/termination limits are 600/180/5 seconds. These are starting engineering constraints, not accepted throughput. Many deadline-length scientific calls would exhaust the hour ceiling long before the attempt ceiling; per-dispatch resource guards must stop safely and report incomplete coverage. A provider process whose death is unconfirmed blocks further dispatch. No inference from a passed software test supplies GPU authorization. No paid provider or current quota is assumed.

### 10.2 Concrete gates and consequences

| Gate | Required evidence before dependent work | If it fails |
|---|---|---|
| Scientific adoption and precision | Explicit new-regime amendment; acceptance of natural-history package estimands, moderate/large-effect precision, 192/128 rule and proposed resources | Reconsider the question or budget. The present document remains research evidence |
| Mathematical/protocol acceptance, CPU | Independent gold/edit checks; common eligibility; no-leak views; winner-remains indistinguishability witness; a legal local-information strategy within three calls/agent for both first speakers; literal retain/clear; true no-change reopening; finality/wait/invalid-action cases | Correct the scoped implementation before inference; no task simplification hidden in a technical fix |
| Complete numerical representation | Lossless exact seeds; strict action types; model-specific template/EOS framing; actual permitted histories including feedback and Unicode fit 8,192 input plus 512 output for both tokenizers; useful messages/action fit output | Stop for a common prospective cap/representation amendment. No truncation or removal of inconvenient history |
| Durability and accounting, CPU/host | Raw-before-effects; exact saved failure/resume; idempotent delivery; one global admission owner; crash and restored-copy reconciliation; complete exports | Resolve storage/process/accounting defects; affected unknown scopes remain unknown |
| Actual numerical/state/memory readiness | Correct language weights and placement; no unexplained missing weights; finite scores; fresh per-call state and A/B/A isolation; full allowed envelope; ≥1.5 GiB free headroom on every used device; confirmed cleanup | Block dependent model calls. No silent dtype/backend/checkpoint fallback |
| Scalar capability, per model | Sixteen qualification actions all legal/committed, at least 15/16 exact; no correctness feedback or retries | Preserve failure and reconsider task/interface/numerical regime with equal future opportunities; do not quietly drop the model |
| Fixed development usefulness, per model | All 16 worlds and cells have settled evidence; at least 30/32 exact scalar controls, at least 8/16 original joint successes, ≥95% legal original-phase calls, and at least 16/32 joint successes pooled across the two no-change policies | Report feasibility failure. Reconsider baseline/reopening interface or the intended practical question before a new candidate; do not select successful prefixes |
| Recovery behavior | Revision success, policy differences, stale outputs and diagnostic targets are reported **without an admission threshold** | Wrong/illegal/unfinished recoveries remain outcomes, including zero recovery in both policies |
| Resource/session admission | Both systems accepted; actual host memory/disk/session quota and restoration established; complete target forecast within remaining attempts/hours/reloads, else fixed fallback within them; export reserve protected | Choose fallback before main data, or stop. Do not omit a model, cell, panel or unfavorable world |
| Main stopping | Fixed cohort; ordinary mistakes never stop enrollment. Only integrity, health, unresolved spending, session deadline or hard resource exhaustion stops dispatch | Export a truthful partial result, restore settled calls exactly, resume only within the same authorized scope; no efficacy stopping |

The development thresholds are coarse screening choices with wide statistical uncertainty, not population reliability certifications. They test whether the common task and reopening are usable, not whether a preferred policy wins. Pooling no-change usefulness avoids requiring both policies individually to perform well and thereby screening away a potentially harmful policy. Both model results are reported even if either gate fails; the two-model main plan then remains unexecuted. Diagnostics and revision outcomes cannot be relabeled infrastructure failures to obtain more attempts.

## 11. Explicit scientific-amendment table

These changes require a future scoped adoption. The new regime should preserve all earlier specifications, defaults, freezes and artifact meanings. The old roadmap's six-cell implementation stages are evidence of reusable seams, not instructions to implement the rejected design.

| Current authority or prior proposal | Recommended amendment for this new campaign |
|---|---|
| Original thesis §§1–2: five families, four peers, 60/40 worlds | Two-agent maximum, 192/128 independent natural-history worlds; no original-task pooling |
| Course §12: old-winner withdrawal below M2 | Balanced demotion and winner-remains strata, common eligibility, hidden mixture |
| Course §12.1: only actual change reopens agents | Every declared continuation boundary reopens both agents; truthful no-change control with identical phase reset |
| Original thesis provisional synchronous candidates | Explicitly use sequential private-final I-01 semantics, without modifying original synchronous machinery |
| Earlier proposals: supplied HS/HSC/H0 main or HS/HSC main plus natural bridge | Natural retain/clear main; supplied views only in bounded diagnostics; no separate bridge |
| Original reset/interference AUC primaries; proposed commitment interaction | Two model-specific direct clear-minus-retain joint-success effects; interactions secondary; all means and gains/losses retained |
| Uniform two-trial proposal | One primary trial everywhere; fixed 24-world panel with two extra continuations; 32-world preserving panel |
| Course Qwen-only model and existing prompt | Two exact pinned direct systems, common owner-qualified labels/phase clarification; separate templates and load acceptance |
| Original 262,144 context and course short-call acceptance | New common 8,192+512 proof and hardware qualification; no transfer of an old proof by assertion |
| Existing 100-hour thesis planning ceiling; separate 500-attempt course campaigns | Request a new 200 additional aggregate GPU-hour cap and exact 17,192/13,096 attempt cap; no reset or concealment of historical usage |
| Existing historical analysis conventions | New eight-stratum paired analysis, type-7 intervals, two-primary multiplicity and explicit degeneracy/missingness rules; old reports unchanged |

No approved budget is enlarged here. Historical allocated spending remains separately reported, including unknown intervals. Research acceptance, scientific adoption, deterministic implementation, bounded GPU qualification, frozen main authorization, paid resources and publication remain distinct decisions. Prompt 2 is research; Prompt 3 should produce a reviewable contract, not infer any of those permissions.

## 12. Handoff to Prompt 2: finite online-workflow research

**Exact next task:** research whether—and how—the stated stage schedule can run in Kaggle with these two pinned models, Python scripts first and one thin main notebook, preserving the scientific contract and fitting the conservative resource envelope. Produce a concrete architecture/reuse and feasibility recommendation for Prompt 3. Do not implement or execute the experiment during that research.

Inputs are this population/cell/seed contract, the complete call table, the numerical/model pins, gates and reserves above, plus existing [I-01 source](../../recovery/i01/core.py), [runbook](../I01_KAGGLE.md), [implementation evidence](../validation/i01-assisted-implementation.md), and the [earlier roadmap](../plans/thesis-extension-roadmap.md) for reusable interfaces only. The relevant seams are concrete:

- `core.py`: generator, permitted view, explicit event/reopening, state initialization and literal rendering. It currently treats every non-prefix phase as revised and accepts only prefix/retain/clear phase names.
- `inference.py` and the reviewed loader: fixed Qwen assumptions, templates, termination, load audits and fresh state; Granite needs an explicit maintained path, not merely a new model ID.
- `store.py`, `process.py`, `policy.py`, `workflow.py`, `archive.py`, `report.py`: existing persistence, finite stage control, process health, attempt ownership, export and read-only reporting. Current stage/config admission is scoped to existing course sizes and must remain intact for those regimes.

Resolve these **eight technical questions**, with documentation/source evidence and named later acceptance checks rather than invented hardware results:

1. **Compatibility:** which exact supported Python/PyTorch/Transformers/bitsandbytes lock loads the pinned text-only Qwen and Granite systems on actual intended Kaggle hardware? Which Qwen-specific attention/recurrent patches must stay out of Granite? Can one lock serve both without offload, custom kernels or semantic changes?
2. **Online source delivery:** how does one thin notebook download a pinned source packet/revision and dependencies, verify its existing source binding, and invoke installed scripts outside an accidental stale checkout? Keep experiment logic in reusable Python. No general agent framework, new outcome store, semantic graph or cloud service.
3. **Model assets and storage:** exact immutable asset allowlists, download sizes, cache behavior, free disk/RAM, concurrent replicas sharing local assets, partial-download recovery, and session-to-session asset retention. Does the six-hour download reserve survive the actual plan? Do not resolve the newer Granite head by upgrading it.
4. **Native rendering and capacity:** how are both direct prefixes, raw suffix/termination IDs, literal historical data, exact 64-bit seeds and complete worst-case contexts verified? Can the full horizon fit both tokenizers and the 8,704 resident envelope without truncation?
5. **Device memory and numerical acceptance:** which existing CPU/source checks can be reused, which current-host measurements are still required, and how will the finite readiness calls establish isolation, finite scores, full-envelope headroom, deadlines and shutdown? Vendor claims and cache arithmetic cannot answer actual fit.
6. **Session schedule and time:** current Kaggle account/session/quota facts, one versus two replicas, model/device rotation, stage ordering, at most twenty additional replica reloads, idle accounting, deadline margins and conservative per-category throughput collection. Show a complete target and fallback mapping; do not assume a historical approximate session limit is current entitlement.
7. **Persistence and restoration:** which storage survives process death, kernel restart and full session loss? Specify the existing quiescent database/manifest/source backup route, off-session export, exact tail reconciliation, lost-call exposure accounting, confirmed termination and restoration acceptance. A local checkpoint alone is not evidence of survival after session deletion.
8. **Notebook inspection and stage boundaries:** one finite main notebook that downloads code/dependencies/assets only in their authorized stages; frequent world/cell/call progress and attempt/resource counters; a checkpoint or preparation receipt after **every code cell**, including setup and diagnostic failures; durable snapshots on a bounded cadence and at stage ends; visible paths/downloads and exact resume behavior. A receipt should state whether it is a preparation record or a restore-capable snapshot. Completed-stage reruns make no new model calls. Do not cross authorization gates merely because Run All was pressed for preparation.

Prompt 2 should return a stage-to-script/notebook map, exact dependency and asset proposal, state/restore ownership diagram if useful, target/fallback session forecasts, a short list of genuinely unresolved host measurements, and any **specific proposed scientific amendments** forced by feasibility. It must not change this scientific question through an implementation convenience. Prompt 3 can then consolidate one specification with explicit precedence and remaining gates.

## 13. Verification and remaining limits

This research used no inference, GPU operation, model-weight download, experiment run, statistical simulation, or production change. Small deterministic Python calculations outside historical artifacts checked call totals, precision/power sensitivities, repeat-cost ratios, memory components and worked maxima. Only model cards/configuration/template metadata and paper texts were retrieved. Read-only SQLite checks are evidence verification, not new model qualification.

Documentation verification resolved all 18 local links/fragments, reconciled both stage/campaign totals and the runtime/precision formulas, and found all 2,543 pre-existing tracked files byte-identical to the research baseline. The only repository addition is this proposal. No existing specification, plan, configuration, source, notebook, report or canonical artifact was changed.

The decisive limitations remain substantive: the policy bundles useful and harmful history; one short numerical task limits external validity; one natural prefix per world cannot estimate within-world prefix variation; private irreversible actions may produce floors; two fixed quantized direct systems do not represent all LLMs; and this sample cannot reliably resolve small effects. None is repaired by labeling the controlled old-commitment experiment cleaner. The recommended choice is a **bounded natural recovery-policy study with an honest action endpoint and matched controls**, conditional on explicit scientific adoption and the online feasibility work above.
