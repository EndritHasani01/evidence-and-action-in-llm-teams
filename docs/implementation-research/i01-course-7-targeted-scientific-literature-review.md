# I-01 course-7: targeted scientific literature review

16 October 2026. **Research synthesis only.** Publication records and open full
texts were checked live. External results below are author-reported findings,
not reproductions. No model, inference, GPU, executable, prompt, configuration,
scientific contract or Course-7 artifact was changed.

Starting evidence: [independent scientific audit](../validation/i01-course-7-independent-scientific-audit.md)
and [existing improvement proposal](../proposals/i01-course-7-experimental-quality-improvement.md),
both read in full. Governing authority remains [specification §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
Decision companion: [literature-informed recommendations](../proposals/i01-course-7-literature-informed-recommendations.md).

## 1. Scientific judgment

The literature strengthens the case for diagnosing the agent environment before
spending on another natural policy comparison. It **does not establish that
prompt clarification is sufficient**, that a larger model is the best next
investment, or that selective memory repair requires a new runtime.

The most informative next question is narrower than “does forgetting help?”:
**When historical source evidence is held fixed, does exposure to a formerly
correct shared conclusion impair adaptation to an actual source change, beyond
its effect in a no-change continuation?** This requires a separately declared
controlled-history regime. It cannot be answered by reinterpreting Course-7.

There is substantial prior art for source-preserving memory, paired recovery,
and correction/preservation measurement. A defensible contribution would be a
careful extension to **private information, an initially valid world that
actually changes, and sequential peer interaction with final commitments**.
It would be an empirical boundary-condition study, not the invention of
evidence-preserving recovery. A well-controlled null would still be useful.

## 2. Search, selection and evidential standard

### 2.1 Scope and procedure

This is a targeted critical review, not an exhaustive systematic review or
meta-analysis. Live searches used arXiv, ACL Anthology, NeurIPS proceedings,
PMLR/ICML, OpenReview, author publication pages and scholarly indexing. Search
families included:

- `SILO-BENCH distributed coordination`, `multi-agent LLM failure attribution`;
- `multi-turn conversation premature answers`, `belief revision maintain update`;
- `JSON schema constrained decoding reasoning performance`;
- `memory source conclusion retention correction`, `cascade memory repair`;
- `paired counterfactual agent recovery`, `communication correction preservation`.

Repository references supplied leads, not verified bibliographic facts.
Backward/forward searches followed the particularly close source-retention and
communication-audit work. Fifteen papers were retained for their direct bearing
on observed failures or identification. Nine have verified conference publication
status; six are treated as preprints. Venue prestige does not erase mismatched
information access, supervision or evaluation.

Root `AGENTS.md`, specification §12, README, the current implementation handoff,
I-01 WBS, implementation-research synthesis, research navigation/manifest,
original related-work audit, updated landscape and relevant retention/recent-work
notes were inspected. The earlier four-agent work remains historical. Several
principles below were already known in that archive; the contribution of this
review is their independently checked application to **the executed Course-7
failures**, not their rediscovery.

### 2.2 Full-text and version policy

Every core paper has an obtained PDF. Relevant methods, configurations, results,
ablations, limitations and selected appendices were inspected; obtaining a full
PDF does not mean every reference or appendix example was read line by line.
The reading inventory in §7 makes that distinction explicit. Selected tables
were also rendered visually to check column alignment and qualifications.

Locators below are **one-based PDF pages**, unless a printed page is stated.
They refer to the exact reading versions in §7. P02's proceedings and arXiv v3
main text, pp. 4–10, were compared after whitespace normalization and match;
the proceedings appendices have different page offsets. P04's accessible arXiv
v1 is the analysis text; ICLR 2026 status is independently verified, without
asserting word-for-word identity with its access-blocked conference PDF.

Evidence labels distinguish **E** (reported experiment), **D** (design or formal
result under assumptions), **A** (author interpretation) and **I** (this review's
inference for I-01). No reported percentage is an expected I-01 improvement.

## 3. Course-7 determines the research priorities

The [audit §§5–8](../validation/i01-course-7-independent-scientific-audit.md#5-independently-reproduced-main-results)
establishes 2/20 exact team success for each policy, only three correct prefixes,
60 illegal actions among 206 team calls, and distinct stale-answer, finality and
source-use failures. The original paired result and exploratory interval remain
unchanged. These counts are audit evidence, not findings from the external papers.

Four canonical calls were additionally inspected directly through read-only
SQLite connections in this review:

| Course-7 observation | Exact record | Research implication |
|---|---|---|
| Correct local 910 is embedded in an illegal message-plus-wait action | `main-01/prefix/agent-1/invocation-0` | Distinguish selecting useful content from legally delivering it |
| Retain repeats its old 993 action despite a revised current shard | `main-03/retain/agent-0/invocation-0` | Test historical conclusion exposure with useful evidence controlled |
| Empty-history clear claims “Partner submitted 2”; 2 is the notice's record index | `main-08/clear/agent-1/invocation-0` | Test event interpretation independently of stale memory |
| Message identifies 959 as global, but submission is local 943 | `main-04/retain/agent-0/invocation-1` | Explanatory text is not the committed decision |

Records are in [the two canonical stores](../../notebooks/run/course-7-working/latest/)
and [conversation export](../../notebooks/run/course-7-working/latest/reports/conversations.jsonl).
The current [renderer and validator](../../recovery/i01/core.py) corroborate
private finality, strict rejection and the presentation of notices/history.
These spot checks do not constitute a new full audit or independent human coding.

## 4. Critical analysis of the fifteen papers

### P01. SILO-BENCH: the closest task precedent

**E/D:** Thirty algorithmic tasks combine private shards, three communication
substrates and six team sizes. Full-information baselines and failure traces
probe integration and premature submission (§§3–5; Tables 2, 14–18). Appendix C.2
states one execution per configuration; Appendix B gives structural guidance,
and the native wait action yields to a new round rather than blocking on a
message. These differ materially from I-01's three-call phases.

**Critical reading:** Table 18's protocol reminder improves Level-I success from
62.9 to 65.1 under one model/protocol, whereas a planning round benefits harder
levels more. This does not establish a universal prompt remedy. The paper's
claim that partial-score gaps isolate integration is stronger than those
descriptive metrics identify; different errors can yield the same gap.

**I:** Keep exact tasks, full-information controls and explicit finality
diagnostics. Neither native success rates nor “competent communication” transfer
to Course-7, where delivery itself often failed. Native scoring is not our
scoring authority. [Record and PDF](https://aclanthology.org/2026.acl-long.1354/).

### P02. MAST: useful diagnosis, limited intervention identification

**E:** Grounded analysis of 150 traces produced fourteen failure modes; the
larger 1,642-trace collection uses automated annotation (§3, Table 1). Human
agreement and judge agreement are separate validations. The categories include
termination ignorance, ignored peer input and reasoning/action mismatch.

**E:** Appendix H/Table 5 compares prompt and topology interventions. On GPT-4
GSM-Plus, prompt refinement raises 84.75 to 89.75, whereas topology reaches
85.50. Other systems show different patterns. The changes include verification,
role restrictions or revised stopping, rather than one isolated clarification.

**Critical reading:** Taxonomy labels organize symptoms; they do not identify
their causal proportions. The paper's primacy-of-design conclusion includes
conjecture (§5.3). More elaborate systems are not thereby shown necessary.

**I:** Borrow a small observable coding vocabulary and report intervention
ingredients separately. Do not import an LLM judge, universal failure frequencies,
or verifier architecture. Course-7 already permits exact legality checks that
need no judge. [Proceedings record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html).

### P03. CIR: distinguish rescue, harm and the recovery package

**D/E:** The same ALFWorld state branches into recovery/no-recovery under clean,
stale or missing observations (§3). Refresh, content-ablated refresh and replanning
separate some intervention components (§5.3; Appendix A). The learned router
uses pre-intervention features, out-of-fold threshold selection and separate
evaluation tasks (§§4–5).

**E:** The 3-point router gain is across 300 condition-episodes from **75 tasks**,
not 300 independent tasks (§5.4). Full and content-ablated refresh share eight
rescues in a 65-task executed-intervention comparison; their difference remains
uncertain (Appendix A, Table 2).

**Critical reading:** The environment is unchanged while observations are
corrupted. Some analyses condition on factual success; complete prefix-feasible
cohorts partly address that restriction. One model/harness and deterministic
continuations limit generalization.

**I:** Use paired benefit/harm tables and an event control. Do not train a router
on twenty Course-7 worlds or treat restoration of an observation as equivalent
to a formerly true source becoming false. [Full text](https://arxiv.org/pdf/2610.00372v1).

### P04. Lost in Conversation: early commitment can survive later evidence

**E:** The study compares original instructions, concatenated shards and
multi-turn disclosure on 600 instructions, fifteen models and repeated
simulations (§§3–6). CONCAT helps distinguish rephrasing from staged interaction.
RECAP and SNOWBALL repeat user information but only partly close the gap
(§7.1, Table 2, Appendix M). Lower temperature is not a general solution
(§7.2, Table 3).

**Critical reading:** This is simulated underspecification, not withdrawal of
a previously authoritative fact. The simulator can stop on a correct answer
(§3.2); I-01 never uses evaluator correctness to stop. Automated conversation
components and outcome-based sharding validation also constrain interpretation
(Appendices C–D). Observed early commitment is not a proof of one internal cause.

**I:** Separate performance with available evidence from performance across its
history. A consolidated current-state presentation is a reasonable candidate,
but a host summary could add interpretation or remove inconvenient evidence.
Repeated identical Course-7 executions would not provide the repeated-sampling
evidence used here. [Reading version](https://arxiv.org/pdf/2505.06120v1).

### P05. ICR: richer communication can help and harm simultaneously

**D/E:** Independent–Communicate–Revise freezes initial solutions, evaluates
directed sender/receiver pairs and adds a no-message revision control (§3).
Correction, preservation and paired gains/losses distinguish answer improvement
from indiscriminate influence. Questions, not six directions, are bootstrap units.

**E:** Full text versus answer-only increases correction but reduces preservation
on all four Qwen3-4B benchmarks (Table 3); structured verification also moves both
quantities, with task/channel-dependent net effects (Table 4).

**Critical reading:** All agents initially see the same problem; revised replies
never propagate. Several headline full-set accuracies contain **imputed**
unobserved outcomes (Appendix G, Table 15), so measured paired strata are stronger
evidence than those headline estimates. Sender answer correctness does not
certify every sentence of its explanation.

**I:** Hold historical evidence fixed, measure helpful and harmful changes and
keep unknown outcomes unknown. Do not transplant its selectivity index as a
new primary score or equate static answer revision with distributed recovery.
[Full text](https://arxiv.org/pdf/2610.01042v1).

### P06. JSONSchemaBench: validity needs an exact target language

**D/E:** The benchmark separates constraint coverage, compliance, efficiency and
task quality. It distinguishes under-constraint from over-constraint (§5;
Definitions 5.1–5.5). Quality experiments use Llama-3.1-8B, three reasoning tasks
and explicit reasoning/answer fields (§6; Table 8); constrained conditions improve
those particular scores.

**Critical reading:** Neither an accepted schema nor several valid generations
proves that a grammar admits exactly the intended actions. Speed measurements
use different inference backends on an A100 (§4.1), not our custom T4 runtime.
Prompting and tokenization matter; these are not universal performance gains.

**I:** JSON-only constraints would miss Course-7's already well-formed illegal
actions. An exact action union could exclude message-plus-wait while preserving
send-and-submit, but remains a behavioral decoding intervention. It cannot
establish information sufficiency or correct finalization. Verify both rejected
illegal examples and accepted legal alternatives before considering such a
condition; no current backend integration is established. [Full text](https://arxiv.org/pdf/2501.10868v3).

### P07. Format restrictions: do not infer a universal JSON penalty

**E:** Tam et al. compare constrained decoding, format instructions, two-stage
natural-language conversion and free text across models/tasks, using prompt
variants (§§2–4). One observed failure is answer-before-reason key ordering
(§4.1). Later schema-API results are mixed across tasks (Table 2, p. 6).

**Critical reading:** The “perfect parser” is an evaluated LLM extractor,
not a mathematical guarantee (§3.4). Formats, model support and prompting vary;
the headline degradation should not be read as an inherent cost of every
constraint. P06's contrasting results make implementation details consequential.
Two-stage conversion also adds computation and another possible error source.

**I:** Compare legality and exact task success independently. A new action schema
may change reasoning and commitment even when all outputs parse. Conversely,
free-form parsing would sacrifice I-01's auditable action boundary. This paper
supports testing a precise interface candidate, not abandoning strict scoring
or repairing old replies. [Publication](https://aclanthology.org/2024.emnlp-industry.91/).

### P08. Intrinsic self-correction: check the comparator and feedback source

**E:** Huang et al. remove oracle stopping labels from reasoning self-correction
and compare debate with response-count-matched self-consistency (§§3–4,
Tables 2–7). Several apparent gains disappear or reverse. They also test whether
putting informative feedback into the initial prompt is a stronger baseline (§5).

**Critical reading:** The evidence concerns particular older models, prompts
and tasks. It is not an impossibility theorem for all present models. Crucially,
I-01 supplies a real external source update, unlike intrinsic self-correction;
the negative result does not establish that factual recovery must fail.

**I:** Do not count more calls, an oracle-selected stopping point, or a better
instruction available only in the intervention as recovery competence. If a
future scaffold says “compare both shards before finalizing,” compare it with
that instruction present from the beginning. Never feed exact-answer feedback
to only one history policy. A generic reflection loop is not presently a
well-supported use of the limited budget. [Full text](https://arxiv.org/pdf/2310.01798v2).

### P09. ReConcile: a substantive competitor, with a different task

**E:** Three diverse models discuss a fully visible problem using explanations,
confidence and selected convincing demonstrations (§§3–5). Ablations attribute
part of the improvement to diversity and demonstrations (§6.2, Table 7).
Response-count comparisons include nine-way self-consistency (Appendix B.3,
Table 11); benefits vary by task.

**Critical reading:** The team answer is a host confidence-weighted vote, rather
than two private, final commitments. All models share the complete problem.
Human explanation examples and confidence recalibration are consequential
ingredients; matching call counts does not match model cost or information
access. API uncertainty is acknowledged in Limitations (p. 10).

**I:** Diverse-model debate is a plausible accuracy intervention in another
regime, but it would change model composition, supervision, aggregation and
cost together here. With only two private shards, a majority cannot manufacture
missing evidence. Preserve this as a competing approach to defer, rather than
selecting only negative debate literature. [Publication](https://aclanthology.org/2024.acl-long.381/).

### P10. LongMemEval: remembering, updating and reading are distinct

**E/D:** Five abilities include knowledge updates and abstention, alongside
retrieval and temporal reasoning (§3). The paper separates indexing, retrieval
and reading (§4). Extracted summaries/facts sometimes lose useful information
(§5.2, Figure 5); structured inputs help most in combination with a particular
reading strategy (§5.5, Figure 6).

**Critical reading:** Histories are constructed and edited, questions use an
LLM correctness judge, and commercial-system observations are dated (§3.3;
Appendices A–B). These are not current product comparisons. Its roughly 115k
and 1.5M-token settings differ from Course-7's short inputs. Retrieval recall
and answer accuracy can also disagree (Appendix E.5, Figure 14).

**I:** Add separate source-use/update diagnostics; do not call all failures
“memory.” Preserve literal evidence when evaluating a summary's effect, and
avoid inserting a retriever or vector store where all allowed text already fits.
Structured **input** benefits do not contradict task-dependent structured
**output** costs. [Full text](https://arxiv.org/pdf/2410.10813v2).

### P11. Belief-R: updating and maintaining both require measurement

**E/D:** Delta reasoning evaluates an initial inference followed by an additional
premise. Belief Update and Belief Maintain subsets test changing and keeping
answers (§§3–5). Models and prompting methods show a trade-off between them
(Figures 4–5; Appendix C/Table A1).

**Critical reading:** The suppression task relies on commonsense reinterpretation
of conditionals. Adding another sufficient condition does not invalidate modus
ponens in classical logic; the paper explicitly motivates a pragmatic necessary-
condition interpretation (§4, Figure 2). Gold therefore includes human judgments,
filtering and transfer of annotations between inference forms (§4.1–4.2).
Its scores are not exact mathematical revision scores.

**I:** Borrow the requirement to test warranted preservation as well as change,
while retaining I-01's exact numerical oracle. Always changing after a notice
could look competent in a world set that always changes its answer. A no-change
or answer-preserving event is therefore scientifically important. Do not import
the suppression task's semantic ambiguity or its composite score.
[Publication](https://aclanthology.org/2024.emnlp-main.586/).

### P12. Faulty Memories: preservation is not free, or uniformly beneficial

**D/E:** Typed runtime provenance, diagnosed faulty memory IDs, independent-
support checks and selective replay repair both answer and store (§3).
The 150-case controlled study reports 85.3% recovery, versus 77.3% for its best
competing repair method (Table 2). Removing support checking raises recovery to
88.0%, while reducing preservation and increasing work (Table 3).

**Critical reading:** Cases are retained only when injection changes the answer
and creates a downstream effect (§4). Results use one main seed/run; several
baselines are adapted and one uses oracle-assisted diagnostics (Appendix H).
The 50-case external subset is selected and converted, not a full benchmark
evaluation (Appendix I). Missing dependency inference is expressly outside scope.

**I:** Distinguish answer recovery, benign-evidence preservation and replay cost.
Do not turn opaque prose citations into trustworthy dependency edges. A graph
repair implementation would supply structure absent from Course-7 and could
solve the benchmark through the harness. [Full text](https://arxiv.org/pdf/2608.10502v1).

### P13. Reclaim Evaluation: information loss and stale influence differ

**D/E:** Matched memory notes keep source or conclusion; a padded condition
tests length (§§3–5). Source absence is imposed by construction. The behavioral
question is what models emit when recomputation is unsupported. Some abstain;
mandatory answer fields change that behavior (§5.3, Table 4; Appendix J,
Table 21). Source-first also fails when its source exceeds the budget (§7).

**Critical reading:** Character budgets are not token budgets. Repeated seeds
do not multiply the number of distinct tasks. Synthetic planted errors dominate;
the small endogenous-error test has a different stale-emission pattern
(Limitations, p. 23). Null effects for several answerers qualify the title's
“worse than empty” shorthand. Padding controls length imperfectly, not all
presentation effects.

**I:** Source-versus-conclusion retention is occupied prior art. Course-7 still
supplies current own shards and permits renewed peer exchange; its errors are
not the paper's source-absence wall. Study formerly correct conclusions after
actual world change, and never substitute old-value avoidance for accuracy.
[Full text](https://arxiv.org/pdf/2606.25449v5).

### P14. Who&When: an observable mistake is not an established decisive cause

**D/E:** The benchmark formalizes a decisive agent-step error through a
counterfactual correction, but its 184 attribution tasks are labeled by expert
inspection and consensus (§§2–3). Three automated attribution procedures have
poor exact-step performance, especially on hand-crafted systems (Table 1).
Stronger reasoning models do not consistently solve this (§4.8, Table 4).

**Critical reading:** Consensus labels do not execute the formal counterfactual
for every attributed cause. The dataset contains failed trajectories and a
chosen earliest-error convention, rather than an unrestricted causal inventory.
Task outcome labels provided to the auditor are additional information unavailable
to the acting agent.

**I:** Keep deterministic evidence separate from human descriptions and internal
mechanism hypotheses. Course-7 supports “this illegal message was not delivered,”
but not “this was the unique cause and fixing it would rescue the team.” A small
human-coded casebook is proportionate; automated root-cause judging is not a
validated shortcut. [Publication](https://proceedings.mlr.press/v267/zhang25cq.html).

### P15. MemoRepair: strong guarantees can belong to the harness

**D:** Withdrawal, validated successors and predecessor-closed publication
define a repair contract. For fixed candidate values/costs, the scalarized
selection reduces to min-cut (§2, Theorem 1). It does not solve every hard-budget
repair problem.

**E:** Under complete influence provenance, Table 1 retains most of the repair-all
publication ceiling at lower normalized operator cost. Zero exposure is shared
by withdrawal-based methods, not uniquely evidence of learned competence.
Table 4 explicitly degrades provenance and validation.

**Critical reading:** Normalized operator cost excludes the barrier and is not
our measured GPU effort. The diagnostic task score is defined from artifact
availability/staleness (§3), rather than an interchangeable exact team-success
endpoint. Guarantees depend on complete provenance and validators (§5).

**I:** Preserve current authority separately from historical claims. Do not add
publication barriers, min-cut or certified claim admission to this tiny experiment:
those would change who performs the scientific reasoning and what is measured.
Use this paper to delimit novelty and expose assumptions. [Full text](https://arxiv.org/pdf/2605.07242v1).

## 5. Integrated explanation and intervention priorities

### 5.1 What the combined evidence adds

The papers do not offer a single diagnosis. They instead support a sequence of
questions with different observable tests:

| Question raised by Course-7 | Most relevant evidence | Small discriminating comparison | Remaining interpretation limit |
|---|---|---|---|
| Does the agent understand the action language? | P01–02, P06–07 | Frozen presentation versus one common clarification, strict unchanged effects | Better elicitation changes the condition; it is not retrospective correction |
| Can it commit only after acquiring adequate information? | P01–02, P08–09 | Natural coordination versus a separately labeled strategy scaffold | Forced exchange measures competence with supplied strategy |
| Is the correction notice treated as data or a peer answer? | P04, P10–11 and raw empty-history calls | Same values with unambiguous event/source/history boundaries | Improved accuracy would not identify one cognitive mechanism |
| Does a stale conclusion hurt even when supporting evidence survives? | P05, P12–13 | Fixed historical evidence, conclusion present/absent | The exposure package includes salience and some length change |
| Is the effect specific to change? | P03, P08, P11 | Matched actual-edit versus no-change continuation | One withdrawal event type does not represent every revision |
| Is a trace label a causal explanation? | P02, P14 | Recorded facts and bounded interventions reported separately | No access to private cognition; multiple failure pathways coexist |

These are **I**, proposed discriminating tests, not interventions already
validated in the same environment. Evidence strength is greatest for the need
to separate constructs; expected accuracy gains remain uncertain.

### 5.2 Improving success and improving validity are different objectives

A decoder that prevents illegal actions could raise the number of delivered
messages. It also removes a behavior through which history might affect the
system. That is a changed agent condition. An enforced broadcast-and-compare
sequence could make original success common; it would supply the coordination
strategy. A host check that rejects an answer below the current local maximum
would disclose task correctness feedback. A global checker would effectively
perform the benchmark computation. None is a neutral repair of Course-7.

Conversely, controlled supplied histories can improve identification without
improving autonomous original collaboration at all. This is acceptable if the
claim concerns behavior **given that history**. It is not acceptable to call
the resulting original competence naturally acquired. Both sources of value
must be named in a thesis.

The existing proposal's minimal common clarification remains sensible as a
bounded usability experiment. Its default sequence—clarify, establish natural
competence, repeat a natural policy study—should no longer be the automatic
choice for a mechanism-oriented thesis. Natural competence could remain rare;
even a large improvement would leave evidence, conclusion, feedback and context
length bundled in retain versus clear.

### 5.3 Less obvious consequences

**Correct old conclusions are a cleaner intervention than planted errors.**
In a controlled I-01 history, the old answer can be valid when produced and
invalidated by a real edit. This avoids conflating recovery with resistance
to an originally misleading writer. It also makes the no-change condition
essential: persistence is correct there.

**A scalar is not necessarily a reusable evidence basis.** An old maximum from
the changed shard may lose authority when its winning record changes. Keeping
that scalar while deleting the old final answer does not guarantee preservation
of what is needed to recompute. A source-preserving condition must specify
which actual records or claims survive, whose shard they describe, their phase,
and what new information still has to be communicated. No host may use hidden
eligibility to tell agents that the replacement cannot win.

**Private information changes what “verification” can mean.** A receiver cannot
check a remote maximum against an unseen remote shard. Instructions to verify
every peer claim can therefore add an impossible requirement. A legal
acknowledgment establishes receipt, not truth or independent support. If the
experiment supplies source records for verification, that information change
must be explicit.

**Finality is part of the causal pathway.** Suppressing all early submissions
would remove a central observed failure, rather than identify why it occurs.
Likewise, analyzing only compliant or completed continuations would condition
on post-intervention behavior. Keep those outcomes in the denominator.

**A no-change control and an answer-preserving edit answer different questions.**
The former tests generic disruption from history processing and reopening. The
latter changes a real fact while leaving the maximum correct, testing warranted
preservation under an actual update. Start with one explicit control; do not
silently call a sham a representative harmless revision. A later substitution
of the latter is a new event distribution.

**I-01 has little expensive work to save.** Keeping two short arrays does not
demonstrate preservation of substantial distributed computation. First establish
an interpretable behavior contrast, then consider a precisely motivated task
with reusable intermediate work. Additional task complexity cannot rescue
unidentified history effects.

## 6. Contribution, novelty and unresolved alternatives

The nearest precedents occupy complementary pieces: P01 supplies static
private-information collaboration; P05 supplies controlled communication
revision; P03 supplies paired recovery and clean-state controls; P13 supplies
source/conclusion retention; P12/P15 supply structured selective repair.
Their conjunction motivates, but does not prove the novelty of, a controlled
distributed source-change experiment.

The strongest potential contribution is **an exact, transparent account of when
a formerly useful shared conclusion becomes harmful after its source changes,
despite access to a specified historical evidence basis and renewed ordinary
communication**. Evidence should distinguish failure to update the answer,
failure to acquire the changed peer's information, and failure to execute a
legal/final action. The combination is worth testing; twenty synthetic worlds
and one model would still support only a bounded study.

Reject first-ever claims for selective preservation, resetting contaminated
context, paired recovery evaluation, correction-versus-preservation metrics,
or dependency-aware repair. The recent preprints are technically close but
unreplicated here. Their existence is novelty pressure even where their empirical
claims are fragile. A publication decision needs another targeted novelty check
after the final question is frozen; this review is not proof that no matching
study exists.

Screened alternatives included MultiAgentBench (verified ACL 2025 record),
intent-mediation work (verified arXiv 2602.07338 record and inspected method),
and REVISE (verified arXiv 2609.00643 record). They were not promoted into the
fifteen-paper core: broad benchmark transfer, extra mediator supervision and
structured runtime repair are less direct next interventions. No uninspected
REVISE method/result is used to decide the recommendation.

## 7. Verified bibliography and full-text reading inventory

Records and links were checked on 16 October 2026. “Preprint” means no
peer-reviewed venue was verified in the records checked; it does not prove that
no venue exists. Version dates are manuscript dates, not conference dates.

### 7.1 Publication records

1. **P01 — Yuzhe Zhang, Feiran Liu, Yi Shan, Xinyi Huang, Xin Yang, Yueqi Zhu,
   Xuxin Cheng, Cao Liu, Ke Zeng, Terry Jingchen Zhang, Wenyuan Jiang.**
   *SILO-BENCH: A Scalable Environment for Evaluating Distributed Coordination
   in Multi-Agent LLM Systems.* **ACL 2026**, pp. 29379–29398.
   [Record/DOI 10.18653/v1/2026.acl-long.1354](https://aclanthology.org/2026.acl-long.1354/),
   [conference PDF](https://aclanthology.org/2026.acl-long.1354.pdf).
2. **P02 — Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal,
   Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein,
   Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica.**
   *Why Do Multi-Agent LLM Systems Fail?* **NeurIPS 2025, Datasets and Benchmarks**.
   [Official record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html),
   [conference PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf).
3. **P03 — Shuyao Xiao, Shengling Wang, Xuan Chen, Ke Chao, Ming Cui,
   Feifei Qian, Chaoyang Mei, Fanlin Meng, Ziming Yu, Junxi Yin.**
   *When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents.*
   **Preprint**, arXiv:2610.00372v1, 30 September 2026.
   [Record](https://arxiv.org/abs/2610.00372v1), [PDF](https://arxiv.org/pdf/2610.00372v1).
4. **P04 — Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville.**
   *LLMs Get Lost In Multi-Turn Conversation.* **ICLR 2026**;
   reading version arXiv:2505.06120v1, 9 May 2025.
   [Conference record](https://openreview.net/forum?id=VKGTGGcwl6),
   [author institutional publication record](https://www.microsoft.com/en-us/research/publication/llms-get-lost-in-multi-turn-conversation/),
   [accessible PDF](https://arxiv.org/pdf/2505.06120v1).
5. **P05 — Shixuan Li, Wei Yang, Peiyu Zhang, Anzhe Cheng, Heng Ping,
   Paul Bogdan.** *Beyond Final Accuracy: Auditing Communication in LLM
   Multi-Agent Systems.* **Preprint**, arXiv:2610.01042v1, 1 October 2026.
   [Record](https://arxiv.org/abs/2610.01042v1), [PDF](https://arxiv.org/pdf/2610.01042v1).
6. **P06 — Saibo Geng, Hudson Cooper, Michał Moskal, Samuel Jenkins,
   Julian Berman, Nathan Ranchin, Robert West, Eric Horvitz, Harsha Nori.**
   *JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language
   Models.* **Preprint**, arXiv:2501.10868v3, 27 February 2025.
   [Record](https://arxiv.org/abs/2501.10868v3), [PDF](https://arxiv.org/pdf/2501.10868v3).
   The earlier title *Generating Structured Outputs from Language Models:
   Benchmark and Studies* is not the title of the inspected v3.
7. **P07 — Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin,
   Hung-yi Lee, Yun-Nung Chen.** *Let Me Speak Freely? A Study On The Impact
   Of Format Restrictions On Large Language Model Performance.*
   **EMNLP 2024 Industry Track**, pp. 1218–1236.
   [Record/DOI 10.18653/v1/2024.emnlp-industry.91](https://aclanthology.org/2024.emnlp-industry.91/),
   [PDF](https://aclanthology.org/2024.emnlp-industry.91.pdf).
8. **P08 — Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng,
   Adams Wei Yu, Xinying Song, Denny Zhou.** *Large Language Models Cannot
   Self-Correct Reasoning Yet.* **ICLR 2024**; arXiv:2310.01798v2,
   14 March 2024. [Conference record](https://openreview.net/forum?id=IkmD3fKBPQ),
   [PDF](https://arxiv.org/pdf/2310.01798v2).
9. **P09 — Justin Chen, Swarnadeep Saha, Mohit Bansal.** *ReConcile:
   Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs.*
   **ACL 2024**, pp. 7066–7085.
   [Record/DOI 10.18653/v1/2024.acl-long.381](https://aclanthology.org/2024.acl-long.381/),
   [PDF](https://aclanthology.org/2024.acl-long.381.pdf).
10. **P10 — Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang,
    Dong Yu.** *LongMemEval: Benchmarking Chat Assistants on Long-Term
    Interactive Memory.* **ICLR 2025**; arXiv:2410.10813v2, 4 March 2025.
    [Conference record](https://openreview.net/forum?id=pZiyCaVuti),
    [arXiv record](https://arxiv.org/abs/2410.10813v2), [PDF](https://arxiv.org/pdf/2410.10813v2).
11. **P11 — Bryan Wilie, Samuel Cahyawijaya, Etsuko Ishii, Junxian He,
    Pascale Fung.** *Belief Revision: The Adaptability of Large Language
    Models Reasoning.* **EMNLP 2024**, pp. 10480–10496.
    [Record/DOI 10.18653/v1/2024.emnlp-main.586](https://aclanthology.org/2024.emnlp-main.586/),
    [PDF](https://aclanthology.org/2024.emnlp-main.586.pdf).
12. **P12 — Caili Yu, Yiqi Wang, Jiaqi Zhang, Yiqun Duan, Mingkai Zheng,
    Zhangkai Wu, Kaize Shi, Taotao Cai.** *From Faulty Memories to Corrected
    Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents.*
    **Preprint**, arXiv:2608.10502v1, 11 August 2026.
    [Record](https://arxiv.org/abs/2608.10502v1), [PDF](https://arxiv.org/pdf/2608.10502v1).
13. **P13 — Alex Kwon.** *Reclaim Evaluation: A Lossy Memory Is Worse Than
    an Empty One.* **Preprint**, arXiv:2606.25449v5, 21 July 2026;
    first submitted 24 June. [Record](https://arxiv.org/abs/2606.25449v5),
    [PDF](https://arxiv.org/pdf/2606.25449v5).
14. **P14 — Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han,
    Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu.**
    *Which Agent Causes Task Failures and When? On Automated Failure Attribution
    of LLM Multi-Agent Systems.* **ICML 2025**, PMLR 267, pp. 76583–76599.
    [Record](https://proceedings.mlr.press/v267/zhang25cq.html),
    [official PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/zhang25cq/zhang25cq.pdf).
15. **P15 — Yang Zhao, Chengxiao Dai, Mengying Kou, Yue Xiu.**
    *MEMOREPAIR: Barrier-First Cascade Repair in Agentic Memory.* **Preprint**,
    arXiv:2605.07242v1, 8 May 2026.
    [Record](https://arxiv.org/abs/2605.07242v1), [PDF](https://arxiv.org/pdf/2605.07242v1).

### 7.2 Reading and access ledger

| ID | Obtained version / PDF pages | Principal inspected material |
|---|---|---|
| P01 | ACL proceedings, 20; arXiv v2 cross-check | §§3–5, Appendices A–C/G–H, Tables 2/14–18; p. 20 visually checked |
| P02 | NeurIPS proceedings, 54; arXiv v3, 47 | Main §§3–5; proceedings Appendix H pp. 33–35, Table 5; main text equivalence checked as above |
| P03 | arXiv v1, 15 | §§3–5, pp. 3–8; Appendix A pp. 13–14 and paired counts p. 15 |
| P04 | arXiv v1, 36 | §§3–7/9; Appendix C–D p. 20; L–M p. 30 |
| P05 | arXiv v1, 32 | §§3–4 pp. 3–9; prompts pp. 16–17; Appendix G/Table 15 p. 25; Table 4 visually checked |
| P06 | arXiv v3, 32 | §§3–6 pp. 4–12, coverage definitions and Tables 5–8; Table 8 visually checked |
| P07 | EMNLP proceedings, 19 | §§2–5 pp. 2–6, model/prompt/parser setup, later schema ablation; p. 6 visually checked |
| P08 | arXiv v2, 17 | §§2–5 pp. 2–7, Tables 2–8; Appendix A example p. 13 |
| P09 | ACL proceedings, 20 | §§3–6 pp. 4–8; Limitations p. 10; Appendix B.3–B.5 pp. 15–16 |
| P10 | arXiv v2, 28 | §§3–5 pp. 4–10; Appendix A/B p. 21, E.5/Figure 14 p. 28 |
| P11 | EMNLP proceedings, 17 | §§3–7 pp. 3–9; Appendix C/Table A1 p. 14 |
| P12 | arXiv v1, 19 | §§3–5 pp. 3–7; baseline adaptations and external-subset limitations pp. 17–19 |
| P13 | arXiv v5, 36 | §§3–5 pp. 5–10, Tables 5–6 p. 12; boundaries pp. 17/20–24; Appendices F–K pp. 32–34; Table 21 visually checked |
| P14 | PMLR proceedings, 17 | §§2–4 pp. 2–9; algorithms p. 12; annotation instructions p. 15 |
| P15 | arXiv v1, 12 | §§2–5 pp. 2–9, Theorem 1, Tables 1/4 and cost/diagnostic definitions |

No core recommendation rests on an inaccessible paper or abstract alone.
OpenReview PDF downloads for P04/P08/P10 returned access challenges/403s;
legitimate arXiv full texts were obtained instead. The version limitation for
P04 is retained, rather than claiming its conference PDF was inspected.

One non-core foundational source remains **record-only**: Jon Doyle,
*A Truth Maintenance System*, **Artificial Intelligence 12(3), 231–272 (1979)**,
[DOI 10.1016/0004-3702(79)90008-0](https://doi.org/10.1016/0004-3702(79)90008-0).
The [MIT AIM-521 record](https://dspace.mit.edu/handle/1721.1/5733) verifies
an author memo/PDF, but local retrieval was rate-limited. A supplied journal
PDF or AIM-521 would help a later formal historical comparison. No detailed
theorem or method from that unexamined text is used here, and it is not one of
the fifteen full-text papers.

The organized local cache is
`C:/Users/EndritHasani/Downloads/i01-literature-2026-10-16/`: fifteen selected
PDFs, extracted text, source metadata and a README. It is outside Git; the links
and reading versions above make this document usable without that machine-local
cache. No paper binaries or new executable research infrastructure are added
to the repository. The selected PDFs total approximately 16.23 MiB.

Delivery verification checked 33 external URLs: 32 returned HTTP 200, including
the three explicitly identified OpenReview challenges; MIT returned HTTP 429.
Accessible arXiv/proceedings alternatives cover all fifteen core papers. Local
documentation links and anchors were checked, and protected specification,
configuration, source, original audit/proposal and Course-7 artifact hashes
remained unchanged.
