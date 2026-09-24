# Multi-Agent Evaluation Science

**Research cutoff: 20 September 2026**

## Executive synthesis

Multi-agent evaluation has a foundational identification problem:

> **Observed team performance is not the same thing as evidence of teamwork.**

A multi-agent system can outperform a single-agent baseline because it uses more tokens, generates more independent samples, has more opportunities to recover from stochastic errors, receives additional context, or simply lets one strong agent take over the work. Conversely, genuine coordination can improve substantially while the final task score barely changes.

Recent results make both problems concrete. *Debate or Vote* finds that, on its evaluated NLP tasks, majority voting explains most of the benefit commonly attributed to multi-agent debate. *TeamBench* finds statistically similar pass rates between prompt-only and genuinely access-separated teams even though their internal behavior differs sharply: prompt-only teams exhibit much more role takeover. *DecisionBench* reports substantially different delegation fidelity under conditions with nearly indistinguishable end-task quality. ([arxiv.org](https://arxiv.org/abs/2508.17536?utm_source=chatgpt.com))

This leads to the central methodological conclusion of this report:

> **The principal quantity multi-agent evaluation should estimate is the marginal value of interaction under controlled resources and controlled information—not merely the performance of a system containing several agents.**

A mature evaluation science therefore needs at least four layers simultaneously: task outcome, interaction process, resource usage, and counterfactual controls. A benchmark that lacks the counterfactual layer usually cannot tell whether it is measuring collaboration.

The broader agent-evaluation literature is independently moving toward finer-grained, cost-aware, robust evaluation, with a 2026 ACL survey specifically identifying cost efficiency, safety, robustness, and fine-grained evaluation as unresolved priorities. Multi-agent evaluation adds another complication: observations inside one team are statistically and causally dependent. ([aclanthology.org](https://aclanthology.org/2026.findings-acl.1330/?utm_source=chatgpt.com))

---

# 1. The object of evaluation is an interaction effect

Suppose an interacting team obtains score \(Y_T\) and a conventional single agent obtains \(Y_S\).

The tempting quantity is

\[
Y_T-Y_S.
\]

That is a **system advantage**, not a teamwork effect.

The difference may simultaneously contain:

\[
\text{more inference compute}
+\text{sampling diversity}
+\text{different context}
+\text{specialization}
+\text{information pooling}
+\text{actual coordination}
-\text{communication overhead}
-\text{coordination errors}.
\]

Those factors are generally non-additive, so they should not be treated as an exact algebraic decomposition. They are different causal explanations that require different counterfactual comparisons.

A useful evaluation should therefore estimate several distinct quantities.

### Total system value

Compare the deployed team with the best realistic single-agent alternative.

\[
\Delta_{\text{system}}
=
E[Y_{\text{team}}]-E[Y_{\text{strong solo}}].
\]

This answers an engineering question: should the system be deployed?

It does **not** answer whether collaboration caused the improvement.

### Equal-resource organizational value

Hold a resource budget \(B\) approximately fixed:

\[
\Delta_{\text{org}}(B)
=
E[Y_{\text{team}}\mid B]
-
E[Y_{\text{solo}}\mid B].
\]

The budget could be tokens, model calls, monetary cost, FLOPs, or latency. None is universally correct.

*Towards a Science of Scaling Agent Systems* takes an important step in this direction by standardizing tools and token budgets across single, independent, centralized, decentralized, and hybrid organizations. Its reported architecture effects vary strongly by task type, including negative multi-agent effects on sequential tasks. ([arxiv.org](https://arxiv.org/abs/2512.08296))

### Interaction value

The strongest control is often:

\[
\Delta_{\text{interaction}}
=
E[Y_{\text{interacting team}}]
-
E[Y_{\text{independent ensemble}}]
\]

with the same models and approximately the same resource budget.

The independent ensemble can use voting, reranking, best-of-\(N\), or another task-appropriate aggregation method.

This is the quantity missing from many claims about multi-agent reasoning. If independent samples obtain the same gain, the evidence supports **parallel test-time computation**, not necessarily collaboration.

*Debate or Vote* is particularly important because it performs essentially this conceptual decomposition and finds majority voting responsible for most reported debate gains in its settings. ([arxiv.org](https://arxiv.org/abs/2508.17536?utm_source=chatgpt.com))

### Coordination-under-distribution value

For genuinely distributed tasks, the relevant counterfactual differs.

Each agent may possess private information or control rights that cannot simply be duplicated. Then compare:

\[
E[Y_{\text{communication enabled}}]
-
E[Y_{\text{same distributed system, communication disabled}}].
\]

SILO-BENCH and MAS-BENCH are useful precisely because information is intentionally partitioned. SILO-BENCH evaluates exact-answer algorithmic tasks under information silos and reports active communication despite poor distributed computation—the authors' “Communication-Reasoning Gap.” MAS-BENCH isolates distributed sorting by giving each agent only a local segment. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/))

A privileged centralized solver receiving all fragments is then an **upper-bound diagnostic**, not necessarily a deployment baseline.

That distinction matters enormously.

---

# 2. Multi-agent necessity must be constructed, not assumed

A benchmark should answer:

> Would this problem remain essentially unchanged if one sufficiently capable agent replaced the whole team?

There are three scientifically legitimate situations.

**Structural interdependence** is strongest. Different participants possess different observations, permissions, resources, objectives, or irreversible actions. Centralization changes the problem itself.

**Organizational advantage** is weaker but legitimate. A single solver is theoretically possible, but parallel work, specialization, context separation, or independent checking may improve performance under a resource constraint.

**Interaction as the phenomenon** is also legitimate. Multiple agents might be unnecessary, but researchers specifically want to understand conformity, communication failures, correlated errors, or organizational overhead created by deploying them.

What is weak is merely writing “researcher,” “critic,” and “manager” into three prompts and calling the result collaborative.

TeamBench demonstrates a particularly clean solution. Its Planner sees requirements but cannot edit the workspace; its Executor can modify the workspace but lacks the full specification; its Verifier can inspect and certify but cannot implement. No participant possesses every relevant capability. The authors then compare Solo, Restricted, Full Team, No-Plan, and No-Evaluate conditions. ([arxiv.org](https://arxiv.org/abs/2605.07073))

They even introduce a **Teamwork Necessity Index**:

\[
TNI=
\frac{S_{\text{team}}-S_{\text{restricted}}}
{\max(\epsilon,S_{\text{solo}}-S_{\text{restricted}})}.
\]

Conceptually, this is valuable because it asks how much of the capability removed through information/access restriction is recovered by actual teamwork. ([arxiv.org](https://arxiv.org/abs/2605.07073))

This style of evaluation is much more informative than “three agents scored 4% higher than one.”

---

# 3. Correct outcomes can arise for organizationally wrong reasons

This is arguably the deepest evaluation problem.

Imagine that Planner → Executor → Verifier is the intended organization.

The team succeeds.

That does not establish that planning was useful, that the Executor followed the plan, that the Verifier independently checked anything, or even that the nominal role separation existed behaviorally.

TeamBench supplies unusually clear evidence. Prompt-only and sandbox-enforced teams obtain statistically indistinguishable pass rates, yet enforcing actual role boundaries reduces Verifier code-edit attempts from 256 to 72 in the reported experiment. The same outcome metric therefore describes organizations behaving quite differently. ([arxiv.org](https://arxiv.org/abs/2605.07073))

Even more strikingly, its Verifiers approve roughly 49% of submissions that fail the deterministic grader, conditional on issuing a verdict. Removing the Verifier improves partial performance in one matched ablation. A “team with verification” can therefore contain a component called a verifier while failing to obtain dependable verification. ([arxiv.org](https://arxiv.org/abs/2605.07073))

DecisionBench reveals a different form of the same problem. Across awareness conditions, mean end-task quality was statistically indistinguishable, while routing fidelity@1 varied from 7.5% to 29.5%. If only the final task score were reported, the difference in delegation ability would largely disappear. ([arxiv.org](https://arxiv.org/abs/2605.19099?utm_source=chatgpt.com))

The general lesson is:

> **Outcome equivalence does not imply organizational equivalence.**

A benchmark capable of supporting claims about teamwork therefore needs observables below the final score.

---

# 4. Process evaluation is necessary—but dangerous

The natural response is to add process metrics. That is correct, but only if the metric represents a functionally meaningful construct.

Collab-Overcooked explicitly adds process-oriented metrics rather than evaluating only final completion, and its environment creates asymmetric knowledge and collaboration opportunities. Its experiments report substantial weaknesses in active collaboration and continual adaptation despite reasonable goal understanding. ([aclanthology.org](https://aclanthology.org/2025.emnlp-main.249/))

Useful process constructs include handoff correctness, commitment fulfillment, redundant work, conflicting actions, information retention, verification false acceptance, waiting caused by dependencies, unnecessary communication, delegation quality, and recovery following another participant's failure.

But **message count is not collaboration**.

Neither is communication density.

SILO-BENCH is revealing precisely because communication remains active while distributed computation fails. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/))

Likewise:

- agreement is not correctness;
- verbosity is not information exchange;
- role-labelled behavior is not specialization;
- asking for help is not successful delegation;
- giving feedback is not verification;
- acknowledging a plan is not following it.

Process metrics should therefore be grounded in **consequences**, wherever possible.

A message becomes scientifically interesting when removing, delaying, corrupting, or replacing it changes downstream behavior in the predicted way.

---

# 5. Information transfer should be decomposed into four stages

Multi-agent research frequently treats “information was communicated” as one event. Evaluation should distinguish at least four events:

\[
\text{availability}
\rightarrow
\text{transmission}
\rightarrow
\text{uptake}
\rightarrow
\text{causal use}.
\]

**Availability:** Did some agent possess the required fact?

**Transmission:** Did the relevant content reach the recipient?

**Uptake:** Did the recipient's subsequent representation or plan reflect it?

**Causal use:** Did the information materially influence the relevant decision?

These are different.

TeamBench illustrates this distinction directly. In its Planner-to-Executor analysis, substantially more specification-critical information appears in the Planner channel than survives into Executor tool interactions. ([arxiv.org](https://arxiv.org/abs/2605.07073))

SILO-BENCH makes the larger point experimentally: communication can occur without successful integration into globally correct computation. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/))

A strong future metric would therefore estimate something closer to **causal message utility** than raw communication volume.

For message \(m\),

\[
U(m)
=
E[Y\mid m]
-
E[Y\mid do(m=\text{removed/replaced})].
\]

The intervention need not always require a full expensive rerun. Carefully designed replay, deterministic environments, paired continuations, or restricted counterfactuals can sometimes approximate it.

This turns communication evaluation from descriptive linguistics into causal systems analysis.

---

# 6. Contribution attribution is becoming its own evaluation problem

Who caused the success?

Who caused the failure?

Those questions become increasingly difficult when output is sequential and interdependent.

Classical Shapley-style reasoning appears attractive because it measures marginal contribution across coalitions. But naive coalition evaluation is computationally expensive and becomes ambiguous when removing an agent changes the workflow itself.

Recent work is explicitly attacking this problem.

*Agents that Matter* formalizes agent attribution through cooperative games and argues that the chosen removal protocol defines the game being evaluated. Its experiments find Leave-One-Out attribution useful for identifying bottlenecks while being far cheaper than exhaustive coalition methods. ([arxiv.org](https://arxiv.org/abs/2605.27621?utm_source=chatgpt.com))

*Semantic Cooperative Games* instead represents realized information flow and derives semantic contribution attribution from a trajectory, motivated partly by the expense and variance of counterfactual reruns. ([arxiv.org](https://arxiv.org/abs/2607.18255?utm_source=chatgpt.com))

These approaches measure related but different things.

A removal-based quantity asks:

> What would happen to system utility without this participant?

A semantic-flow quantity asks something closer to:

> Which participant supplied semantic support used in the realized solution?

Neither automatically equals causal responsibility.

An agent may contribute critical evidence that another misuses. An agent may contribute little visible semantic content but prevent failure through verification. Removing a central coordinator may destroy the workflow entirely, assigning it enormous marginal value even if another organization could solve the same task.

Consequently, attribution reports should state explicitly:

**target metric + intervention/removal protocol + coalition distribution + workflow adaptation rules.**

“Agent X contributed 30%” without those definitions is underspecified.

---

# 7. Equal compute is essential, but there is no single correct definition

Multi-agent systems complicate compute accounting because resources are multidimensional.

Tokens are easy to count but imperfect: one token from a frontier model and one from a small model are not comparable computationally or economically.

Model calls are similarly crude.

Dollar cost changes across providers.

Wall-clock latency rewards parallelism even when total compute grows.

Long context can make later tokens substantially more expensive than early tokens.

Tool calls may dominate both cost and latency.

Therefore evaluation should usually present a **Pareto frontier** rather than a single cost-normalized score:

\[
(\text{task value},
\text{tokens},
\text{model cost},
\text{latency},
\text{tool calls}).
\]

The correct question is not simply “Which system scores highest?”

It is:

> For a given resource envelope, what additional value does interaction produce?

The controlled-token design of *Scaling Agent Systems* is important here, and the paper reports that coordination effects vary with task characteristics rather than providing a universal multi-agent benefit. ([arxiv.org](https://arxiv.org/abs/2512.08296))

A team beating an ordinary one-shot agent using five times the inference budget establishes little about teamwork.

A team beating best-of-\(N\), self-reflection, search, and independent ensembles under comparable expenditure establishes much more.

---

# 8. The minimum serious baseline matrix

A strong evaluation does not need every conceivable baseline, but collaboration claims usually need a family of counterfactuals rather than one competitor:

| Condition | What it diagnoses |
|---|---|
| Single agent, ordinary budget | Practical default |
| Single agent, matched inference budget | Extra-compute explanation |
| Independent agents + aggregation | Sampling/diversity explanation |
| Same team with communication disabled | Marginal interaction value |
| Pooled-information single agent | Cost of decentralization / information boundaries |
| Restricted single participant | Whether distributed information is actually necessary |
| Scripted or oracle partner | Whether failures arise from partner behavior or focal-agent capability |
| Role/component ablations | Marginal organizational contribution |
| Oracle coordinator/verifier | Headroom available if coordination or checking were perfect |

Not every study requires all nine. The appropriate subset follows from the claimed mechanism.

The crucial discipline is this:

> **Every plausible simpler explanation should have a corresponding control whenever feasible.**

---

# 9. Local capability must be separated from multi-agent capability

A difficult benchmark can create the appearance of a coordination problem when every individual model is simply incapable of its assigned subtask.

TeamBench explicitly reports this issue for some smaller open-weight models: performance becomes dominated by invalid tool calls and context problems rather than coordination. ([arxiv.org](https://arxiv.org/abs/2605.07073))

The evaluation therefore needs **local competence checks**.

If agent \(i\) is expected to perform subtask \(z\), evaluate:

\[
P(\text{solve }z\mid\text{complete information and correct tools}).
\]

Only after establishing adequate local capability does failure under distributed conditions strongly implicate communication, organization, incentives, or integration.

This gives a useful diagnostic sequence:

\[
\text{Can each agent do its part?}
\rightarrow
\text{Can necessary information move?}
\rightarrow
\text{Can recipients use it?}
\rightarrow
\text{Can actions remain jointly compatible?}
\rightarrow
\text{Can the team recover when something breaks?}
\]

A benchmark that jumps directly to final failure usually cannot locate the layer that failed.

---

# 10. Critical assessment of major multi-agent benchmarks

The following comparison concerns **what scientific claims each instrument can support**, not an overall ranking.

| Benchmark / study | Strongest evaluation contribution | What success does **not** prove |
|---|---|---|
| **TeamBench (2026)** | Enforced information/action separation, deterministic grading, matched role ablations, explicit teamwork-necessity construct. | General teamwork outside Planner–Executor–Verifier structures; high pass rate alone still does not guarantee good verification. ([arxiv.org](https://arxiv.org/abs/2605.07073)) |
| **SILO-BENCH (ACL 2026)** | Exact-answer distributed tasks with controlled information silos and communication-complexity levels. | Real-world organizational competence; communication density itself does not demonstrate information use. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/)) |
| **MAS-BENCH / distributed sorting (ACL Findings 2026)** | Very clean isolation of shared-state and scalable distributed coordination. | Broad problem-solving collaboration; sorting deliberately narrows the construct. ([aclanthology.org](https://aclanthology.org/2026.findings-acl.1698/)) |
| **CooperBench (2026)** | Real code dependencies where individually feasible changes can conflict when performed concurrently. It reports about a 30% average reduction in success when agents work together versus performing both tasks individually. | That coding coordination failures transfer unchanged to other domains; integration success still depends on local coding/tool capability. ([arxiv.org](https://arxiv.org/abs/2601.13295?utm_source=chatgpt.com)) |
| **Collab-Overcooked (EMNLP 2025)** | Asymmetric information/resources, joint action, and explicit process-level collaboration metrics. | General organizational intelligence; game-specific process metrics may not transfer directly to enterprise workflows. ([aclanthology.org](https://aclanthology.org/2025.emnlp-main.249/)) |
| **DecisionBench (2026)** | Separates delegation quality from final quality, cost, latency, routing fidelity, and counterfactual delegation headroom. | General peer-to-peer teamwork: delegation is a narrower interaction structure. ([arxiv.org](https://arxiv.org/abs/2605.19099?utm_source=chatgpt.com)) |
| **CoopEval (ICML 2026)** | Distinguishes institutional mechanisms—repetition, reputation, mediation, contracts—under explicit social dilemmas. | Task collaboration or “social intelligence” generally; cooperation depends on game structure and enforcement assumptions. ([arxiv.org](https://arxiv.org/abs/2604.15267)) |
| **MultiAgentBench (2025)** | Broad scenarios, multiple topologies, competition/collaboration, milestone-oriented KPIs. | A single coherent teamwork construct across heterogeneous tasks; broad coverage can reduce causal isolation. ([arxiv.org](https://arxiv.org/abs/2503.01935?utm_source=chatgpt.com)) |
| **CoffeeBench (2026)** | Persistent 90-day heterogeneous economic interaction, communication and transactions. | Team performance as such: one evaluated roaster interacts with fixed reference agents, making it especially useful for long-horizon agent-in-society evaluation. ([arxiv.org](https://arxiv.org/abs/2606.16613?utm_source=chatgpt.com)) |
| **MAST (2025)** | Fine-grained failure taxonomy derived from human analysis across multi-agent frameworks. | Causal explanations of failures; failure annotation is diagnosis rather than controlled intervention. ([arxiv.org](https://arxiv.org/abs/2503.13657?utm_source=chatgpt.com)) |

One striking pattern is visible across the table.

The scientifically strongest instruments increasingly **engineer a dependency** that can be controlled: hidden information, separate permissions, incompatible code changes, private payoffs, or persistent economic state.

That is much stronger than merely putting several language models into a chat room.

---

# 11. Welfare and fairness cannot be reduced to task success

Mixed-motive systems require different metrics from cooperative reasoning systems.

Suppose two agents negotiate an allocation.

A deal can be:

- feasible,
- highly efficient,
- extremely unequal,
- unacceptable to one participant,
- strategically unstable.

A scalar “success = agreement reached” loses most of that structure.

CoopEval is useful because its object is explicitly institutional cooperation rather than conventional task correctness. The Scoreable Games reproduction study offers a warning from negotiation evaluation: expanded experimentation found model comparisons ambiguous and raised concerns about objectivity, information leakage, and evaluation design. ([arxiv.org](https://arxiv.org/abs/2604.15267))

For strategic systems, evaluate at least:

\[
\text{joint welfare},\quad
\text{individual utility},\quad
\text{surplus efficiency},\quad
\text{inequality/fairness},\quad
\text{participation},\quad
\text{violations}.
\]

Do not hide these inside one weighted score unless the weights correspond to a defensible deployment objective.

A Pareto frontier is frequently more scientifically honest.

---

# 12. Robustness should change the dependency, not merely the wording

Multi-agent robustness includes failures that ordinary prompt perturbation misses.

Relevant changes include:

- replacing a familiar partner;
- changing which agent possesses a crucial fact;
- changing an agent's capability mid-run;
- delaying communication;
- introducing an incorrect but confident teammate;
- removing a verifier;
- changing tool reliability;
- changing incentives;
- adding another participant;
- changing the organizational topology.

The important question is whether the system's coordination policy transfers across these structural changes.

This is different from conventional linguistic robustness.

A team that works only with a fixed partner identity may have learned a convention, not general collaboration.

A verifier that works only when the producer belongs to one model family may be exploiting predictable error patterns rather than learning verification.

A router that correctly delegates only within the original capability distribution may be memorizing stable identities.

Evaluation should therefore treat **partner generalization** as its own axis.

---

# 13. Recovery deserves separate measurement from robustness

Robustness asks whether failure occurs.

Recovery asks what happens **after** it occurs.

A strong system may fail relatively often but detect and repair failures cheaply. Another may initially look stable but catastrophically fail once an assumption breaks.

Useful recovery quantities include:

\[
P(\text{detect failure}),
\]

\[
P(\text{recover}\mid\text{detected}),
\]

\[
\text{time-to-detection},
\]

\[
\text{time-to-recovery},
\]

\[
\text{recovery cost},
\]

and

\[
P(\text{recurrence after repair}).
\]

The counterfactual baseline is critical: regenerate the continuation from the same prefix **without the proposed repair**.

Otherwise stochastic rerunning can masquerade as successful recovery.

Long-running systems additionally need measurements of persistent damage: incorrect shared memory, broken commitments, reputation changes, unnecessary transactions, or environmental side effects may survive after the nominal task is repaired.

---

# 14. Long-horizon reliability requires another evaluation vocabulary

Average episodic success becomes increasingly inadequate as horizon increases.

τ-bench introduced \(pass^k\), the probability that all \(k\) repeated executions of a task succeed, specifically to capture reliability rather than the “at least one works” notion measured by pass@\(k\). The original study found substantial reliability degradation across repeated trials even where individual success was much higher. ([arxiv.org](https://arxiv.org/abs/2406.12045?utm_source=chatgpt.com))

The distinction is particularly important for multi-agent systems because every additional participant, handoff, tool interaction, and verification step can introduce another stochastic failure opportunity.

For persistent teams, evaluation should also consider survival-style quantities:

\[
S(t)=P(\text{team remains valid through time }t)
\]

and a failure hazard:

\[
h(t)=P(\text{failure at }t \mid \text{survived to }t).
\]

Then one can ask whether risk rises with organizational age because of stale beliefs, accumulated commitments, memory contamination, or partner drift.

CoffeeBench's 90-day simulated economy is useful partly because it moves evaluation beyond short episodic dialogue into persistent decisions and transactions. ([arxiv.org](https://arxiv.org/abs/2606.16613?utm_source=chatgpt.com))

A future long-horizon teamwork benchmark should additionally keep the same organization alive across many tasks so that memory, reputation, adaptation, and path dependence actually matter.

---

# 15. Repeated stochastic runs are not optional

LLM-agent runs are stochastic, often strongly so.

Reporting one trajectory is anecdotal evidence.

Reporting only an average from a handful of trajectories is better, but still insufficient when variance is high.

Several statistical principles from reinforcement-learning evaluation transfer directly. *Deep Reinforcement Learning at the Edge of the Statistical Precipice* shows how point estimates under limited-run regimes can yield misleading conclusions and advocates interval estimates, robust aggregates, and performance profiles. ([arxiv.org](https://arxiv.org/abs/2108.13264?utm_source=chatgpt.com))

Multi-agent experiments add another problem:

> **Agents inside one team are not independent samples.**

Messages from five agents in one trajectory do not give \(n=5\).

Nor do 100 messages give \(n=100\).

The relevant experimental unit is typically a **task episode / team trajectory**, with repetitions nested inside tasks.

For a general benchmark claim, tasks themselves are also sampled from some population.

A defensible analysis therefore looks more like:

\[
\text{task family}
\rightarrow
\text{task instance}
\rightarrow
\text{condition}
\rightarrow
\text{stochastic run}.
\]

Confidence intervals should preserve this hierarchy, for example through task-level paired bootstrap, hierarchical bootstrap, mixed-effects models, or an explicitly Bayesian hierarchical model.

When comparing two organizations, paired task comparisons are extremely useful because task difficulty cancels partially.

TeamBench, for example, uses paired bootstrap and confidence intervals for several comparisons rather than reporting raw point differences alone. ([arxiv.org](https://arxiv.org/abs/2605.07073))

“No significant difference” should never be translated into “the methods are equivalent” unless the design supports an equivalence claim with appropriately narrow intervals.

---

# 16. Benchmark validity has at least five layers

Multi-agent benchmarks need the traditional concept of construct validity more than most current leaderboards acknowledge.

### Construct validity

Does the task actually instantiate the claimed phenomenon?

If the paper studies distributed reasoning, relevant information should genuinely be distributed.

If it studies specialization, the roles should require different capabilities.

If it studies negotiation, participants should possess partially conflicting objectives and the possibility of rejecting an agreement.

### Internal validity

Does the comparison isolate the proposed mechanism?

If the team has four times the compute and a different prompt, a difference from a one-shot baseline does not isolate coordination.

### Criterion validity

Does the scorer actually recognize task success?

Deterministic tests and state-based graders are excellent when the construct permits them.

But even programmatic tests can be incomplete.

For LLM-judge evaluation, the situation is worse. AgentJudgeBench, released in August 2026, finds judge reliability degrading with workflow difficulty and substantial limitations even among strong judges, while rubric structure helps only partially. ([arxiv.org](https://arxiv.org/abs/2608.26623?utm_source=chatgpt.com))

### External validity

Does the result survive changing models, partner identities, task structures, horizons, and environments?

A second benchmark is valuable when it changes the causal structure—not merely when it supplies another dataset.

### Consequential validity

Does optimizing the metric produce the behavior we actually want?

A communication metric can reward chatter.

An agreement metric can reward premature conformity.

A speed metric can reward unsafe shortcuts.

A cooperation metric can reward exploitable generosity.

A team score can hide individual participants being systematically harmed.

A benchmark should be treated as an incentive mechanism imposed on researchers and eventually on trained systems.

---

# 17. LLM judges require explicit validation

Open-ended multi-agent settings make LLM judging tempting.

It should not be categorically rejected; sometimes no deterministic metric captures the desired construct.

But a benchmark should distinguish:

\[
\text{system uncertainty}
\quad\text{from}\quad
\text{evaluator uncertainty}.
\]

Otherwise leaderboard differences can be smaller than the evaluator's own instability.

Useful safeguards include human auditing of a stratified subset, multiple judge families, structured rubrics, blinded system identity, programmatic evidence where available, and reporting disagreement rather than forcing every instance into one “ground-truth” score.

The recent AgentJudgeBench results reinforce that judge reliability is task- and difficulty-dependent rather than a fixed model property. ([arxiv.org](https://arxiv.org/abs/2608.26623?utm_source=chatgpt.com))

When the benchmark's central claim is itself about collaboration quality, using another group of LLM agents to decide whether collaboration was “good” can create a particularly circular evaluation.

---

# 18. A benchmark should contain counterfactual worlds

The most promising design principle for future multi-agent evaluation is to generate **matched variants of the same task**.

For one underlying task, produce:

\[
T_{\text{pooled}},
T_{\text{distributed}},
T_{\text{no-communication}},
T_{\text{full-communication}},
T_{\text{oracle-partner}},
T_{\text{imperfect-partner}}.
\]

Now the environment becomes an experimental instrument.

The researcher can ask:

- How much difficulty comes from local reasoning?
- How much from information distribution?
- How much can communication recover?
- Does the recipient actually use transmitted information?
- Does adding a verifier help?
- Does a stronger teammate reduce or increase coordination errors?
- Does interaction outperform independent computation at matched cost?

The same task semantics remain approximately fixed while the interaction structure changes.

This is substantially more informative than collecting thousands of unrelated “agentic” tasks.

TeamBench's Solo/Restricted/Team conditions, SILO-BENCH's controlled information distribution, and MAS-BENCH's explicit communication constraints each instantiate pieces of this philosophy. ([arxiv.org](https://arxiv.org/abs/2605.07073))

---

# 19. Benchmark design can itself be a major scientific contribution

A new benchmark is not scientifically valuable merely because it contains new tasks.

It becomes a scientific contribution when it makes a previously difficult latent construct **identifiable**.

For multi-agent systems, a particularly strong benchmark would expose controlled axes such as:

\[
\text{information fragmentation},
\]

\[
\text{dependency density},
\]

\[
\text{capability heterogeneity},
\]

\[
\text{communication bandwidth/delay},
\]

\[
\text{partner reliability},
\]

\[
\text{action authority},
\]

\[
\text{incentive alignment},
\]

\[
\text{horizon length}.
\]

Then hypotheses can make structural predictions.

For example:

> Increasing information fragmentation should harm independent agents but not an omniscient centralized solver; communication should recover performance only when recipients can integrate the fragments.

Or:

> Verification should help when producer error exceeds verifier error and their errors are sufficiently independent; otherwise verification can reduce team performance.

Or:

> Specialization should become valuable as capability heterogeneity and task decomposability increase, but should lose value as coordination costs dominate.

These are reusable scientific statements.

“Framework A scores 63%” is not.

---

# 20. What an evaluation record should contain

A mature multi-agent benchmark should preserve the full causal trace rather than merely the final answer: observations available to each participant, messages, tool calls, state transitions, commitments, permissions, timing, costs, verifier decisions, and final state.

This does not mean every paper must analyze every field.

It means the benchmark should make later analysis possible.

The best benchmark artifact is therefore closer to an **instrumented experimental environment** than to a static question set.

This is especially important because new research questions appear after data collection. A benchmark that stores only final outputs cannot later investigate message timing, duplicated work, provenance, stale beliefs, or causal contribution.

---

# 21. A proposed evaluation stack

The field would benefit from treating multi-agent evaluation as six nested layers.

**Layer 1 — Local competence.**  
Can each participant perform its required function under ideal information and tools?

**Layer 2 — Structural necessity.**  
Does task success actually depend on distributed information, control, incentives, resources, or independent verification?

**Layer 3 — Interaction effectiveness.**  
Does communication/delegation/coordination outperform matched independent computation?

**Layer 4 — Organizational quality.**  
Which roles contribute, which create bottlenecks, and are responsibilities actually respected?

**Layer 5 — Reliability and adaptation.**  
Does the organization survive stochastic repetition, partner changes, faults, and long horizons?

**Layer 6 — Social/system consequences.**  
What does success cost, who receives the benefits, who bears failures, and does the system remain safe and fair?

Most present benchmarks evaluate two or three of these.

Very few evaluate the complete stack.

---

# 22. The major unresolved scientific problems

The deepest open problem is no longer simply constructing harder tasks. It is **identifying the causal contribution of interaction**.

Several particularly important gaps follow.

**Interaction-versus-compute identification.** We still lack broadly accepted protocols for estimating collaborative gain after controlling for test-time compute, self-reflection, independent sampling, and heterogeneous model mixtures.

**Causal information-use measurement.** Current work can measure communication or token overlap much more readily than whether a message changed the recipient's decision for the right reason.

**Sequential contribution attribution.** Shapley, LOO, semantic attribution, and trajectory interventions measure different counterfactuals. There is no settled attribution theory for adaptive language-mediated organizations. ([arxiv.org](https://arxiv.org/abs/2605.27621?utm_source=chatgpt.com))

**Benchmark-level teamwork necessity.** TeamBench provides one compelling operationalization, but an equivalent general principle across negotiation, distributed reasoning, coding, markets, and embodied systems is not established.

**Process-metric validity.** A system can optimize easily measured coordination proxies without becoming more capable. We need evidence that process measures predict genuine counterfactual value.

**Long-horizon organizational reliability.** We know far more about whether agents finish an episode than whether an organization remains coherent across hundreds of decisions, personnel changes, memory updates, and repeated tasks.

**Evaluator reliability.** Agent behavior is getting harder to score at roughly the same time that evaluation increasingly depends on LLM judges.

**Generalization of teamwork.** We need to know whether a protocol coordinates with unfamiliar partners, different model families, new distributions, altered authority, and changed incentives—not merely whether it works with the team on which it was designed.

---

# 23. What existing evidence already establishes

Several conclusions are now defensible.

First, **multi-agent gains cannot generally be interpreted as collaboration gains without controls for independent sampling and additional inference**. Debate research provides direct evidence for this concern. ([arxiv.org](https://arxiv.org/abs/2508.17536?utm_source=chatgpt.com))

Second, **final performance can conceal major organizational differences**. TeamBench's role-enforcement results and DecisionBench's routing results demonstrate this through different mechanisms. ([arxiv.org](https://arxiv.org/abs/2605.07073))

Third, **communication activity is not sufficient evidence of distributed reasoning**. SILO-BENCH shows substantial communication alongside failure to perform the needed distributed computation. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/))

Fourth, **adding organizational components can reduce performance**. TeamBench's verification results, CooperBench's coordination penalty, and broader controlled scaling experiments all demonstrate settings in which additional interaction creates failure rather than synergy. ([arxiv.org](https://arxiv.org/abs/2605.07073))

Fifth, **the value of multi-agent organization is conditional on task structure and base capability**, rather than uniformly positive. Both TeamBench and controlled scaling studies report stronger or weaker team value depending on the underlying single-agent regime and task characteristics. ([arxiv.org](https://arxiv.org/abs/2605.07073))

Sixth, **process-level evaluation is becoming necessary rather than optional**. Collab-Overcooked, DecisionBench, TeamBench, SILO-BENCH, and recent attribution research each reveal important phenomena invisible in one aggregate task-success number. ([aclanthology.org](https://aclanthology.org/2025.emnlp-main.249/))

What is **not** established is a universal theory of which metrics, controls, and task properties are sufficient to identify genuine collaboration.

That is the emerging research field.

---

# 24. A stronger scientific definition of genuine teamwork

For evaluation purposes, I would define genuine teamwork operationally as follows:

> **A system demonstrates teamwork when interaction among distinct decision-makers produces task-relevant causal value that cannot be explained adequately by extra independent computation, while respecting the information, capability, authority, and resource boundaries that define the team.**

This definition deliberately excludes mere multiplicity.

It also does not require the team to outperform a powerful centralized solver. Distributed organization can be scientifically meaningful even when it incurs a coordination tax.

The useful quantities become:

\[
\text{independent-compute value},
\]

\[
\text{interaction value},
\]

\[
\text{coordination tax},
\]

\[
\text{specialization value},
\]

\[
\text{verification value},
\]

\[
\text{recovery value}.
\]

That vocabulary is substantially more informative than “multi-agent accuracy.”

---

# 25. Research opportunity: evaluation science itself

Among the broader multi-agent fields, evaluation science is unusually foundational because weaknesses here contaminate conclusions everywhere else.

Trust research needs to know whether reputation scores measure actual reliability.

Mechanism-design research needs to separate equilibrium feasibility from observed cooperation.

Delegation research needs to distinguish router quality from worker capability.

Learned-collaboration research needs to distinguish improved local policies from better interaction.

Memory research needs to distinguish successful retrieval from correct shared-belief revision.

Security research needs to distinguish an unsafe model from vulnerability produced through interaction.

Without adequate evaluation, each field can produce impressive-looking improvements whose interpretation remains uncertain.

A particularly substantial benchmark contribution would therefore not be “the largest collection of multi-agent tasks.” It would be a **counterfactual evaluation environment where teamwork itself becomes identifiable**.

That environment would generate structurally matched tasks, vary information and authority boundaries, provide strong equal-compute and independent-sampling baselines, log causal process information, support controlled replay or intervention, use machine-verifiable outcomes where feasible, and report hierarchical uncertainty over repeated stochastic runs.

The scientific contribution would then be the instrument:

> **a way to determine when interaction is necessary, when it is useful, why it helps or hurts, and how confident we should be in that conclusion.**

That is substantially deeper than another leaderboard.

---

# Final assessment

Multi-agent evaluation is transitioning from **benchmarking systems** to **measuring organizations**.

The old evaluation question was:

> Did the multi-agent system complete the task?

The stronger question is:

> Who knew what, who did what, what depended on whom, what did communication change, what would have happened without that interaction, what resources were consumed, and would the organization still work under repetition or structural change?

The strongest recent benchmarks—especially TeamBench, SILO-BENCH, MAS-BENCH, CooperBench, DecisionBench, and Collab-Overcooked—each solve part of this problem. None yet constitutes a complete evaluation science. ([arxiv.org](https://arxiv.org/abs/2605.07073))

The central gap is therefore not another missing metric.

It is **causal identification of collective capability**.

A mature field should be able to distinguish at least four outcomes that today's headline scores routinely blur together:

\[
\boxed{
\text{more agents}
\neq
\text{more compute}
\neq
\text{more information}
\neq
\text{better teamwork}
}
\]

Once those quantities are separated experimentally, benchmark design stops being infrastructure around the science.

**It becomes part of the science itself.**
