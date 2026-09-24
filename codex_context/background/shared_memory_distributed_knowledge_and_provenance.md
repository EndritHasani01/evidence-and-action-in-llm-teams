# Shared Memory, Distributed Knowledge and Provenance

**Research cutoff: 20 September 2026.**

This report focuses on memory as a multi-agent organizational problem rather than primarily as vector retrieval, summarization, or long-context engineering. Recent primary literature, including September 2026 preprints, is incorporated where relevant. Recent preprints are evidence of active research rather than established consensus. No benchmark was executed for this report.

## 1. The central conclusion: organizational memory is not a database

The deepest mistake in thinking about multi-agent memory is to treat it as:

> several agents + one better memory store.

The scientifically interesting problem appears when agents have different observations, permissions, responsibilities, histories, incentives, and beliefs.

An organization may simultaneously contain:

| Layer | What it represents |
|---|---|
| **Private agent memory** | An agent's observations, local reasoning, interactions, working assumptions, and experiences. |
| **Shared team memory** | Information intentionally made available to some or all collaborators. |
| **External knowledge** | Documents, databases, APIs, scientific papers, repositories, records, policies, telemetry, and other sources of evidence. |
| **Institutional knowledge** | Claims the organization currently accepts for some purpose. |
| **Organizational history** | Who observed, asserted, modified, rejected, approved, or relied upon something and when. |
| **Derived knowledge** | Conclusions, plans, summaries, predictions, commitments, and decisions produced from earlier information. |
| **Meta-memory** | Knowledge about agents themselves: competence, reliability, authority, past behavior, or relationships. |

These categories are not interchangeable.

A document can be visible without being trusted. A statement can be true without its speaker having authority to establish organizational policy. A memory can be correctly retrieved but obsolete. A conclusion can remain plausible after one of its supporting facts is withdrawn. And an agent can possess the current facts while continuing to execute an obsolete plan.

The latest literature increasingly exposes exactly these distinctions.

GroupMemBench, for example, reports a severe degradation when conventional agent-memory systems move from dyadic conversations to multi-party histories: its strongest tested system reaches only about 46% average accuracy, with particularly poor results on knowledge updates and term ambiguity. The benchmark makes speaker identity, audience, and updates part of the task rather than treating conversation history as one undifferentiated text stream. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/groupmembench-benchmarking-llm-agent-memory-in-multi-party-conversations/?utm_source=chatgpt.com))

AIM/MUMBench, released in September 2026, makes private versus public memory and memory operations explicit. Its reported 96% visibility-classification accuracy contrasts with only 58.8% strict operation accuracy, illustrating an important point: correctly deciding *who may see a memory* is substantially easier than correctly managing the evolving shared state itself. ([arxiv.org](https://arxiv.org/abs/2609.12320?utm_source=chatgpt.com))

**Synthesis:** multi-agent memory is becoming a problem about the governance and evolution of shared belief, not merely finding relevant text.

---

## 2. What is uniquely multi-agent?

Many ordinary memory problems survive unchanged when additional agents are added. Retrieval ranking, compression, context-window management, and forgetting irrelevant records are not intrinsically multi-agent.

The genuinely multi-agent problems arise from **relationships between epistemic states**.

| Single-agent problem | Additional multi-agent problem |
|---|---|
| Was the fact remembered? | **Who originally asserted it?** |
| Is the memory relevant? | **Is this agent permitted to see it?** |
| Is the memory current? | **Have all agents learned that it changed?** |
| Is the fact reliable? | **Are multiple apparent confirmations actually copied from the same source?** |
| Should a memory be overwritten? | **Who has authority to supersede it?** |
| Should a bad fact be deleted? | **Which conclusions, plans, or other agents already depend on it?** |
| Was an inference incorrect? | **Which participant introduced the error and which merely propagated it?** |
| Should information be shared? | **With whom, at what abstraction level, and for what purpose?** |
| Is memory poisoned? | **Can one compromised writer contaminate the whole organization?** |
| Does forgetting work? | **Do other agents, caches, summaries, and derived conclusions still retain the information?** |

This is why a conventional long-term-memory benchmark can provide useful component tests without resolving the multi-agent problem.

MemoryAgentBench, for example, evaluates retrieval, test-time learning, long-range understanding, and selective forgetting in incrementally accumulated interactions. Those capabilities are important, but they do not by themselves answer questions of cross-agent authority, lineage, permission, or collective belief revision. ([mlanthology.org](https://mlanthology.org/iclr/2026/hu2026iclr-evaluating/?utm_source=chatgpt.com))

A 2026 systems characterization of ten agent-memory implementations likewise highlights construction, retrieval, generation, latency, freshness, and fleet-management tradeoffs. That systems work is valuable, but organizational epistemology adds another layer: *even perfectly fast retrieval can faithfully retrieve the wrong organizational state*. ([arxiv.org](https://arxiv.org/abs/2606.06448?utm_source=chatgpt.com))

---

## 3. Three kinds of consistency must be separated

“Memory consistency” is too vague. At least three distinct properties matter.

**Storage consistency** asks whether agents eventually observe compatible versions of shared records.

**Epistemic consistency** asks whether agents' beliefs appropriately reflect those records. Two agents can read identical evidence but interpret it differently.

**Decision consistency** asks whether current actions remain valid under the current state of knowledge.

The third distinction became unusually concrete in the September 2026 *Fresh Memory, Stale Plans* preprint. Its authors construct cases where an executor possesses the updated shared record but still acts according to a plan derived from its superseded predecessor. In 30 controlled workflows containing a post-plan revision, the freshness-only system executed the obsolete plan in every task, whereas the proposed dependency-scoped validation mechanism prevented the invalid action in the tested setting.

That result deserves emphasis:

> **Fresh information does not imply fresh reasoning.**

Synchronization protocols can guarantee that everyone sees `requirement_v4`. They cannot automatically guarantee that the travel plan, software patch, diagnosis, procurement decision, or financial position derived from `requirement_v3` has been reconsidered.

This is where memory becomes a **dependency-management problem**.

---

## 4. Provenance is more than a citation

The foundations are much older than LLM agents.

Doyle's Truth Maintenance System proposed explicitly recording the reasons supporting beliefs so that contradictions could trigger dependency-directed revision rather than indiscriminate rollback. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0004370279900080?utm_source=chatgpt.com))

de Kleer's Assumption-Based Truth Maintenance System went further by maintaining assumption sets, allowing multiple possible belief contexts to coexist rather than forcing one globally consistent state immediately. ([doi.org](https://doi.org/10.1016/0004-3702%2886%2990080-9?utm_source=chatgpt.com))

Classical multi-agent belief-revision research similarly recognized that source identity and credibility become essential once information comes from multiple participants. ([cambridge.org](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/modeling-knowledge-dynamics-in-multiagent-systems-based-on-informants/5CE5458A0505FF49DABA7D4DC813D9EE?utm_source=chatgpt.com))

The W3C PROV model later formalized provenance around entities, activities, agents, derivations, attribution, association, delegation, and temporal relationships. Its motivating observation remains strikingly relevant: provenance helps determine how information should be trusted and integrated when sources differ or conflict. ([w3.org](https://www.w3.org/TR/2013/PR-prov-dm-20130312/?utm_source=chatgpt.com))

LLM-agent systems are rediscovering this problem in a less structured environment.

The recent MAP-Graph preprint treats provenance as an *operational control signal*, not merely audit metadata. Memories and actions are connected through typed lineage; permission-ineligible ancestors can disqualify descendants, and trust can propagate through derivation paths. Its controlled benchmark contains 2,700 synthetic tasks per evaluated method across three domains; the authors report improvements from provenance-aware permission filtering and risk-sensitive action gating in their tested setting. ([arxiv.org](https://arxiv.org/abs/2608.10509?utm_source=chatgpt.com))

This distinction is fundamental:

> **Provenance should explain not only where a sentence came from, but why an organizational belief or action is allowed to exist.**

---

## 5. Provenance collapse may be one of the most important memory failures

LLM memory systems frequently summarize, merge, rewrite, compress, or “reflect” upon source material.

Those transformations are useful for retrieval.

They are dangerous for epistemology.

Suppose an external website says:

> Vendor X says component A is safe.

A consolidating agent might store:

> Component A is safe.

The linguistic compression seems harmless, but an important fact disappeared: **who made the claim**.

A July 2026 preprint calls a security version of this phenomenon *memory provenance laundering*: untrusted external information can be rewritten during consolidation into something that appears to be trusted user history or workflow knowledge. The proposed defense attempts to enforce a source-authority non-amplification property so that memory transformation cannot silently increase the authority of its source. ([arxiv.org](https://arxiv.org/abs/2607.29167?utm_source=chatgpt.com))

The broader scientific question goes beyond security.

Compression can erase:

- uncertainty;
- dissent;
- speaker identity;
- observation conditions;
- time;
- permission restrictions;
- evidence quality;
- causal dependencies;
- whether something was observed, inferred, assumed, or merely proposed.

Consequently, **semantic equivalence is not enough** for organizational memory. A concise paraphrase may preserve apparent meaning while destroying precisely the metadata needed for later revision.

---

## 6. “Who said it?” and “why do we believe it?” are different questions

A useful organizational memory should separate at least four properties.

| Property | Question |
|---|---|
| **Provenance** | Where did this information originate? |
| **Truth/evidential support** | How strongly is the claim supported? |
| **Authority** | Is this source permitted to establish this kind of fact or policy? |
| **Access permission** | Who is permitted to observe or use it? |

These dimensions can disagree.

A junior software agent may correctly discover a production vulnerability without having authority to deploy a patch.

A doctor may be authorized to update a medical record but still enter an incorrect observation.

A document can be confidential and highly reliable.

A publicly visible statement can be false.

An exact provenance chain can faithfully demonstrate the origin of misinformation.

This is why a scalar “memory confidence” score is generally inadequate for sophisticated organizations.

---

## 7. When should information become organizational knowledge?

This is one of the strongest unresolved questions in the area.

The wrong abstraction is:

> memory write = knowledge acquisition.

A better abstraction is a **knowledge-admission process**.

A useful conceptual state machine is:

**observation → attributed claim → shared candidate → validated organizational belief → action-eligible knowledge**

Information need not pass through every stage, and different organizations may deliberately apply different admission regimes.

For example, a team might want to make an unverified incident report visible immediately while preventing high-impact actions from relying on it until independently checked.

Therefore memory systems should ideally distinguish statuses such as:

`private`, `shared-unverified`, `corroborated`, `authoritative`, `disputed`, `superseded`, `revoked`, and `archived`.

The recent viewpoint *Governed Collaborative Memory as Artificial Selection* frames this general issue explicitly: persistent organizations require a selection regime deciding which candidate memories remain local, which become institutional state, which are rejected, and which are later superseded. The paper is primarily conceptual rather than decisive empirical evidence, but the framing captures a problem largely absent from retrieval-centric work. ([arxiv.org](https://arxiv.org/abs/2605.04264?utm_source=chatgpt.com))

An information item should therefore not become authoritative organizational knowledge merely because it is frequently retrieved, confidently phrased, repeated by multiple agents, or recent.

A defensible admission decision may depend on its **source, evidence, independence from other evidence, scope, temporal validity, sensitivity, organizational authority, conflict status, and consequences of being wrong**.

The policy for a brainstorming hypothesis should be different from the policy for authorizing a bank transfer.

---

## 8. Majority agreement is not independent evidence

Multi-agent systems introduce a particularly subtle failure that ordinary retrieval systems do not: **the illusion of evidence multiplicity**.

Imagine five agents all assert the same fact.

That sounds stronger than one agent asserting it.

But perhaps all five copied the same erroneous webpage.

Or Agent B copied Agent A, Agent C copied B, and Agents D and E summarized C.

There are five memories but approximately **one evidence source**.

Recent work on correlation-aware multi-agent memory explicitly studies this failure. *Beyond Memory Majority* argues that memories written by different agents can inherit the same upstream source or shared bias, creating a false majority if a system treats them as independent evidence. Its proposed CAMA system attempts to estimate effective evidence independence using provenance and dependency inference before arbitration. ([arcxiv.org](https://arcxiv.org/abs/2608.19701?utm_source=chatgpt.com))

Related empirical evidence appears in *When Truth Is Distributed*. In controlled five-agent environments, the authors report aggregate truth recovery falling from 72.5% in all-honest collaboration to 14.17% when a critical evidence holder provides false testimony. Importantly, the misinformation continued propagating through honest agents after the original deceiver left the interaction. ([arxiv.org](https://arxiv.org/abs/2608.03421?utm_source=chatgpt.com))

This implies a major principle:

> **Count evidence roots, not memory copies.**

Without lineage, a consensus mechanism can transform copying into apparent corroboration.

---

## 9. Persistent shared misconceptions are qualitatively different from ordinary hallucination

A hallucination generated once can disappear with the context window.

A false organizational belief can reproduce itself.

Once misinformation has entered shared memory, later agents may retrieve it, paraphrase it, cite one another, make decisions from it, and store those decisions as additional memories.

The ICLR 2026 paper *When Agents “Misremember” Collectively* studies collective false-memory formation across several interaction structures and memory timescales. The authors report substantial susceptibility and an average 74.4% reduction under their proposed mitigation strategies, although those results remain tied to MANBENCH's particular construction. ([arxiv.org](https://arxiv.org/abs/2602.00428?utm_source=chatgpt.com))

Another ICLR 2026 paper, ARGUS/MisInfoTask, studies misinformation propagating through multi-agent information flows and reports roughly a 28.17% reduction in misinformation toxicity and a 10.33% task-success improvement under attack in its experiments. ([openreview.net](https://openreview.net/pdf?id=6Y9NP1qhoM&utm_source=chatgpt.com))

These systems largely examine communication trajectories. Persistent organizational memory raises an additional problem:

**misinformation can outlive the participants who originally created it.**

At that point, source removal is insufficient. The organization must identify and repair the descendants of the false belief.

---

## 10. Memory poisoning turns organizational learning into an attack surface

Persistent memory creates an unusual security asymmetry.

A malicious input may be encountered once but influence hundreds of future actions.

The 2026 systematic memory-poisoning study underlying MPBench identifies multiple write channels and architectural vulnerabilities through which adversarial content can enter persistent agent state; the authors report that agents configured to store and retrieve memory aggressively are more exploitable in their tests, and that ordinary prompt-injection defenses do not adequately address persistent memory poisoning. ([arxiv.org](https://arxiv.org/abs/2606.04329?utm_source=chatgpt.com))

The *Sleeper Memory Poisoning* study goes further. It evaluates delayed attacks in which malicious external content causes fabricated information to be stored and activated much later. The authors report poisoned-memory write rates as high as 99.8% on GPT-5.5 and 95% on Kimi-K2.6 in their configurations; among successful retrievals, attacker-intended agentic actions occurred in 60–89% of evaluations. ([arxiv.org](https://arxiv.org/abs/2605.15338?utm_source=chatgpt.com))

Those are single-agent statefulness results, but multi-agent sharing adds a propagation layer:

**one poisoned writer may become a supply-chain attack on everyone who trusts organizational memory.**

The scientific object then becomes not simply attack success rate but **contamination propagation**:

\[
\text{untrusted source}
\rightarrow
\text{writer}
\rightarrow
\text{shared memory}
\rightarrow
\text{derived memories}
\rightarrow
\text{other agents}
\rightarrow
\text{actions}.
\]

A secure shared-memory architecture therefore needs write governance at least as much as read filtering.

---

## 11. Private versus shared memory is a policy problem, not a partitioning trick

A simple architecture might create two vector databases:

- private;
- shared.

That does not resolve the scientific problem.

Permissions evolve.

Information can be combined.

Derived conclusions can leak restricted inputs.

An employee may lose authorization.

A medical observation may be visible to one clinical team but not another.

An agent may need to know *that a restriction exists* without being allowed to know the restricted content.

Collaborative Memory formalizes private/shared memory with asymmetric and changing user-agent-resource relationships, immutable provenance metadata, and retrospective permission enforcement. ([arxiv.org](https://arxiv.org/abs/2505.18279?utm_source=chatgpt.com))

GateMem evaluates a related governance problem explicitly across medical, workplace, education, and household scenarios. Its reported results show that no evaluated system simultaneously achieved strong legitimate-memory utility, robust access control, and reliable active forgetting. ([arxiv.org](https://arxiv.org/abs/2606.18829?utm_source=chatgpt.com))

The September 2026 AIM/MUMBench work similarly evaluates creation, retrieval, update, and deletion under multi-user privacy constraints. ([arxiv.org](https://arxiv.org/abs/2609.12320?utm_source=chatgpt.com))

The emerging lesson is:

> **Read scope, write authority, derivation authority, retention, and action authority are different permissions.**

A memory system that implements only retrieval ACLs handles just one of them.

---

## 12. Central memory governance is becoming an explicit systems abstraction

Several 2026 systems move control over memory away from individual agents.

*Kernel-Managed Shared Memory*, submitted September 9, places retrieval, privacy enforcement, and prompt injection under a central agent-system kernel. Across 1,800 reported trials on three assistant models, the authors report substantially stronger personalization than an unmanaged external-memory backend while using shorter prompts than unfiltered context concatenation. ([arxiv.org](https://arxiv.org/abs/2609.10144?utm_source=chatgpt.com))

*Governed Shared Memory for Multi-Agent LLM Systems* describes scoped retrieval, temporal supersession, provenance tracking, and policy-controlled propagation. Its live-system evaluation reports correct reconstruction of the tested depth-four derivation chains and also documents implementation failures, including an initially bypassable sub-tenant scope and a pipeline-ordering problem where duplicate filtering could interfere with contradiction processing. ([arxiv.org](https://arxiv.org/abs/2606.24535?utm_source=chatgpt.com))

Those negative engineering results are scientifically useful.

They show why “we support permissions and versioning” is not enough. Governance primitives interact, and the order in which they execute can change organizational behavior.

---

## 13. Updating a fact is different from updating a world model

Suppose organizational memory contains:

> Project release date = 20 October.

Later:

> Project release date = 10 November.

A retrieval benchmark may declare success if future queries return 10 November.

But a real organization may already contain:

- a deployment reservation based on 20 October;
- a marketing campaign;
- a contractual milestone;
- staffing allocations;
- a testing plan;
- an inferred statement that “there are 30 days remaining”;
- another agent's task queue.

The original fact has been corrected, but the organization remains inconsistent.

StateMemBench targets part of this problem by evaluating whether memory agents track an evolving state rather than merely retrieve previously mentioned facts. Across 234 multi-session scenarios, its authors report substantial difficulty for existing memory and retrieval systems, while explicit state/supersession structure improves current-state accuracy in their evaluated configurations. ([arxiv.org](https://arxiv.org/abs/2608.19652?utm_source=chatgpt.com))

PlanFence exposes the next step: even after the new state is correctly represented, **plans already derived from the obsolete state can survive**.

The progression is therefore:

**fact update → state update → dependency update → plan/action revalidation**

Most current memory benchmarks stop before the final two steps.

---

## 14. How can a team correct a shared belief without destroying everything derived from it?

This question connects modern agent memory to truth-maintenance systems surprisingly directly.

Suppose:

\[
A \land B \rightarrow C
\]

and

\[
C \land D \rightarrow E.
\]

Later, evidence shows that \(A\) was wrong.

A naïve memory implementation might delete `A`.

That leaves `C` and `E` silently present.

Another naïve implementation might recursively delete everything downstream.

That can also be wrong because `C` may have independent support:

\[
F \rightarrow C.
\]

The correct operation is not “delete descendants.”

It is **re-evaluate their support**.

A dependency-aware repair procedure would preserve immutable source records, append the correction rather than rewriting history, identify all beliefs whose support includes the changed assumption, and recompute only the affected region of the dependency graph. A conclusion supported solely by the revoked premise becomes invalid; a conclusion with independent support can survive. Active plans and pending actions depending on invalidated descendants must then be revalidated separately.

This is essentially the intuition behind truth maintenance and assumption-based truth maintenance applied to agent organizations. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0004370279900080?utm_source=chatgpt.com))

W3C-style provenance provides useful representational concepts for the lineage, while current systems such as MAP-Graph and PlanFence demonstrate why lineage can matter operationally. ([w3.org](https://www.w3.org/TR/2013/PR-prov-dm-20130312/?utm_source=chatgpt.com))

The hard part for LLM agents is that their derivations are often **implicit**.

An agent may produce a plan without accurately declaring every fact on which the plan depends. Natural-language reasoning traces also cannot simply be assumed to be faithful causal explanations.

This leads to a major unsolved problem:

> **How can an organization recover dependency structure accurately enough for selective belief revision when its members reason with opaque language models?**

That is much deeper than memory retrieval.

---

## 15. Forgetting actually means at least three different things

Current memory discussions often use “forgetting” ambiguously.

**Retrieval forgetting** means an item is no longer returned in ordinary searches.

**Epistemic retraction** means the organization no longer treats a proposition as true or actionable.

**Physical deletion** means the underlying information is actually removed from persistent storage.

These are not equivalent.

An organization may legitimately retract an obsolete medical measurement while retaining it historically.

Conversely, a privacy deletion request may require physical erasure rather than merely marking the record “superseded.”

The most difficult case is **derived information**.

Suppose a confidential document yields a derived risk score. The original document is later deleted. Must the risk score also disappear?

There is no universal answer. It depends on whether the derivative itself contains protected information, whether retaining it is legally or organizationally permissible, whether it could reconstruct the underlying source, and why deletion occurred.

GateMem's inclusion of active forgetting is therefore useful, but the deeper question is not simply whether the deleted item resurfaces. It is:

> **What should happen to knowledge derived from information the organization is no longer allowed to possess?** ([arxiv.org](https://arxiv.org/abs/2606.18829?utm_source=chatgpt.com))

This intersects access control, provenance, privacy, and belief revision simultaneously.

---

## 16. Reputation itself is organizational memory

Shared memory need not describe the task environment.

It can describe the other agents.

Σ-Mem, for instance, stores historical evidence about peer competence and peer relationships and updates this state from correctness feedback. The authors report adaptation to counterfactual reliability changes and transfer to unseen peers and domains in their evaluation. ([arxiv.org](https://arxiv.org/abs/2607.27958?utm_source=chatgpt.com))

This opens a different memory problem:

> Agent A's past performance becomes Agent B's future evidence about whether to trust A.

Such meta-memory introduces its own contamination and identification problems.

Observed performance depends on:

- which tasks the agent received;
- task difficulty;
- available tools;
- instructions;
- collaborators;
- evaluator quality;
- whether outcomes were ever observed.

A reputation memory can therefore confidently encode **selection bias**.

More observations do not necessarily solve the problem if all feedback is correlated or systematically missing.

Organizational memory research should consequently distinguish:

**memory about the world**, **memory about organizational decisions**, and **memory about the reliability of participants**.

---

## 17. Shared memory can destroy useful epistemic diversity

An organization wants participants to learn from one another.

But perfect synchronization is not necessarily desirable.

If every agent immediately incorporates the same intermediate conclusions, errors can become correlated and the organization can lose independent lines of reasoning.

The false-majority and collective-misinformation results discussed earlier illustrate this danger. ([arcxiv.org](https://arcxiv.org/abs/2608.19701?utm_source=chatgpt.com))

This creates a real trade-off:

**information sharing improves coverage but can reduce epistemic independence.**

The scientifically interesting question is therefore not “should memory be shared?”

It is:

> **Which information should become common knowledge, which should remain private evidence, and when should independent reasoning be preserved before synchronization?**

For scientific research agents, for example, early hypotheses may be more valuable if separate teams explore them independently before reading a dominant explanation.

This is a memory-governance analogue of preserving useful dissent.

---

## 18. Organizational history may matter more than semantic memory

The September 2026 Agora preprint provides an unusually concrete example.

Instead of treating memory mainly as retrieved prose, Agora stores autonomous research as an append-only Git DAG. Contributions are immutable commits, parent edges say what each result builds upon, and other agents can inspect or reproduce earlier work. In one nearly 12-day run, 13 language-model workers produced 1,703 contributions. The final result had a 145-commit ancestry and 165 posted reproductions. The authors explicitly acknowledge that the run does not by itself establish the causal advantage of shared memory over matched isolated-agent baselines. ([arxiv.org](https://arxiv.org/abs/2609.18094?utm_source=chatgpt.com))

The scientific importance is the representation:

> The memory is not merely “facts researchers should remember.” It is the **history of knowledge production**.

That preserves:

- failed experiments;
- parent hypotheses;
- independent reproductions;
- abandoned branches;
- contributor identity;
- verification state.

For scientific organizations, this may be substantially more useful than a vector database containing only summaries of successful conclusions.

A similar enterprise motivation appears in work on organizational memory for agentic business processes, which argues that organization-specific procedural knowledge otherwise fragments into duplicated agent prompts and inconsistent retrieval setups. ([alphaxiv.org](https://www.alphaxiv.org/abs/2607.03228?utm_source=chatgpt.com))

---

## 19. The research object should be an epistemic lifecycle

A stronger abstraction for future work is:

\[
\text{observe}
\rightarrow
\text{attribute}
\rightarrow
\text{share}
\rightarrow
\text{validate}
\rightarrow
\text{derive}
\rightarrow
\text{act}
\rightarrow
\text{observe outcome}
\rightarrow
\text{revise}
\]

Each transition can fail.

| Transition | Example failure |
|---|---|
| Observe → attribute | The source is forgotten during summarization. |
| Attribute → share | Private evidence becomes globally visible. |
| Share → validate | Repetition is mistaken for independent confirmation. |
| Validate → derive | A correct fact is combined with a stale assumption. |
| Derive → act | The plan becomes obsolete before execution. |
| Act → outcome | The result is incorrectly credited to one contributor. |
| Outcome → revise | Reputation changes even though evaluation was unreliable. |
| Revise → propagate | Some agents retain the obsolete belief. |

This framing unifies what otherwise appear to be unrelated topics: access control, provenance, trust, synchronization, memory poisoning, reputation, belief revision, and stale plans.

---

## 20. What current benchmarks still measure poorly

The benchmark landscape is advancing quickly, but the organizational problem remains only partially covered.

GroupMemBench examines speaker-grounded and multi-party memory. GateMem and AIM/MUMBench introduce governance, privacy, updates, deletion, and multi-principal interactions. StateMemBench stresses supersession. MAP-Graph examines provenance-aware permission and trust decisions. PlanFence studies dependency validity. MANBENCH and MisInfoTask study collective misinformation. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/groupmembench-benchmarking-llm-agent-memory-in-multi-party-conversations/?utm_source=chatgpt.com))

But a comprehensive organizational-memory evaluation would need all of these mechanisms in the same evolving environment.

Useful measurements would include:

| Dimension | Example measurement |
|---|---|
| **Source fidelity** | Can the system identify the original evidence behind a derived belief? |
| **Current-state correctness** | Does it distinguish current, historical, disputed, and superseded facts? |
| **Lineage completeness** | Are the true dependencies of conclusions captured? |
| **Retraction precision** | Are invalid descendants retracted without destroying independently supported ones? |
| **Stale-action rate** | How often are actions executed from obsolete dependencies? |
| **Access-control violation** | Does any agent receive information outside its scope? |
| **Derivation leakage** | Can restricted information leak through summaries or conclusions? |
| **Write-authority violation** | Can unauthorized participants establish organizational knowledge? |
| **Evidence independence** | Does the system detect multiple memories copied from one source? |
| **Poison propagation** | How many agents/decisions become affected after one malicious insertion? |
| **Recovery latency** | How long until the organization becomes behaviorally consistent after correction? |
| **Collateral forgetting** | How much valid knowledge is lost during deletion or repair? |
| **Auditability** | Can a decision be reconstructed from the evidence and rules available at the time? |
| **Cost** | Storage, retrieval, validation, communication, and re-computation overhead. |

A final-answer accuracy score conceals almost all of these properties.

---

## 21. Domain consequences

### Enterprise workflows

The central difficulty is not merely locating company documents. Organizations have policies, exceptions, decision histories, confidentiality boundaries, approval authority, and interpretations that evolve.

A policy change should update more than search results. The organization may need to invalidate active workflows, regenerate recommendations, notify affected agents, and preserve the historical record explaining why older actions were legitimate when originally made.

### Scientific research

Scientific memory must preserve distinctions among observation, hypothesis, analysis, replication, contradiction, and accepted conclusion.

Deleting unsuccessful experiments because they are “irrelevant memories” may produce duplicate work and publication-like selection bias. Shared memory should preserve negative evidence without automatically treating it as current consensus.

Agora's immutable contribution graph is particularly relevant here, although matched experiments are still needed to establish how much the shared structure improves scientific discovery. ([arxiv.org](https://arxiv.org/abs/2609.18094?utm_source=chatgpt.com))

### Software engineering

Requirements, APIs, architectural decisions, tests, branches, tickets, and deployment state evolve concurrently.

The key failure is often not forgetting the latest requirement. It is failing to identify which designs, code changes, tests, or release plans depended upon the old requirement.

This is precisely the structural distinction illustrated by stale-plan execution.

### Healthcare

Healthcare combines nearly every difficult property: different professional roles, sensitive access control, temporally changing state, uncertain observations, high costs of stale information, and requirements for auditability.

A clinically valid historical observation should generally not disappear merely because a newer observation exists; nevertheless, current decisions must distinguish historical from current state. Meanwhile, deletion and authorization rules cannot simply be delegated to semantic relevance.

### Long-running autonomous organizations

The most interesting regime may be organizations lasting long enough that no currently active agent experienced the events that produced their institutional knowledge.

At that point, organizational memory becomes the mechanism by which **past agents govern future agents**.

Poor provenance means inherited claims cannot be challenged rationally. Poor versioning causes obsolete policy to survive. Excessive compression converts contingent judgments into apparent facts. Excessive trust in institutional memory makes old attacks persistent. Excessive forgetting forces the organization to rediscover the same lessons.

---

## 22. Strong scientific questions emerging from the landscape

The literature now makes several generic projects much less interesting. Another semantic memory store, private/shared vector partition, memory graph, summarization method, or “agent with long-term memory” faces considerable novelty pressure.

The deeper unresolved questions concern the **rules governing collective knowledge**:

1. **Knowledge admission:** Under what evidence, authority, and independence conditions should a private observation become shared organizational belief?
2. **Dependency-aware revision:** Can an organization retract the consequences of a false belief while preserving conclusions that remain independently supported?
3. **Lineage inference:** How accurately can LLM-agent systems recover the real dependencies underlying plans and conclusions when explicit reasoning traces are incomplete?
4. **Permission propagation:** If a conclusion derives from private and public evidence, what access rights should the conclusion inherit?
5. **Authority non-amplification:** Can summarization, delegation, repetition, or consensus transform low-authority information into apparently authoritative institutional knowledge?
6. **Evidence independence:** How should agents distinguish true corroboration from repeated descendants of the same source?
7. **Epistemic diversity:** When should information sharing be delayed so that independent reasoning is preserved?
8. **Distributed revision:** How should belief correction propagate when agents are offline, partitioned, or operating under different local versions?
9. **Decision validity:** How can systems determine which active plans or commitments must be reconsidered after a memory update?
10. **Organizational forgetting:** What should happen to valid derived knowledge when its original evidence must be deleted, becomes inaccessible, or loses authority?
11. **Persistent contamination:** How does one malicious or mistaken memory propagate through long-lived organizations, and which structures contain it?
12. **Reputation provenance:** Can partner reliability be learned without confusing agent competence with task selection, teammates, tool quality, or evaluator error?
13. **Institutional drift:** When does accumulated memory produce useful organizational learning versus obsolete doctrine and path dependence?
14. **Decentralized governance:** How can independently owned agents establish shared knowledge when no central memory administrator or universally trusted authority exists?

These are families of questions, not claims that every formulation is untouched.

---

## 23. The particularly promising intersection: provenance × belief revision × action

The literature historically treated these as separate topics.

**Provenance** asks where information came from.

**Belief revision** asks what should remain believed after new evidence.

**Planning** asks what actions follow from current beliefs.

Long-running multi-agent systems connect them.

A future organizational memory system needs to answer:

> This action was proposed because of conclusion C; C depended on B and D; B came from source X under version 4; X has now been revoked; D remains independently valid; therefore only this part of the plan requires reconsideration.

Neither ordinary RAG nor a conventional database transaction provides that semantic reasoning.

Recent MAP-Graph and PlanFence work independently moves toward parts of this picture. ([arxiv.org](https://arxiv.org/abs/2608.10509?utm_source=chatgpt.com))

Classical truth-maintenance work provides the conceptual ancestry. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0004370279900080?utm_source=chatgpt.com))

W3C provenance provides a mature vocabulary for lineage. ([w3.org](https://www.w3.org/TR/2013/PR-prov-dm-20130312/?utm_source=chatgpt.com))

The unresolved scientific problem is making the combination work under **imperfectly explicit LLM reasoning, changing permissions, uncertain sources, and distributed agents**.

That appears much more durable as a research direction than another particular memory architecture.

---

## 24. Research-selection implications

Several areas now look relatively occupied at the generic level:

| Direction | Status by September 2026 |
|---|---|
| Better retrieval for long agent histories | Very active and crowded. |
| Graph versus vector memory | Crowded; graph representation alone is not a contribution. |
| Private/shared memory separation | Already directly studied. |
| Memory ACLs | Active systems and benchmarks now exist. |
| Simple temporal supersession | Increasingly benchmarked. |
| Memory poisoning | Rapidly developing security field. |
| Peer-reliability memory | Already demonstrated experimentally. |
| Organizational memory concept | Explicit 2026 work now exists. |
| Provenance-aware shared memory | Active competing work, including MAP-Graph. |
| Shared Git-like research history | Agora appeared immediately before this report's cutoff. |

The higher-value uncertainties appear one level deeper:

**how provenance changes belief revision; how belief revision changes active plans; how access restrictions propagate through derivations; how evidence correlation affects organizational consensus; and how an organization repairs itself after discovering that a long-standing belief was wrong.**

Those are less about “memory architecture” than about the **science of collective epistemic state**.

---

## 25. Final assessment

The strongest conceptual shift is this:

> **A multi-agent memory system is an institution for deciding what persists.**

Its decisions about writing, sharing, consolidating, trusting, superseding, forgetting, and exposing information determine what future agents will perceive as reality.

That introduces properties absent or much weaker in ordinary single-agent memory:

**distributed belief, source identity, shared authority, selective visibility, social reinforcement, correlated evidence, asynchronous updates, institutional history, collective correction, and downstream dependency management.**

The two questions posed at the start therefore have fairly clear answers at the conceptual level.

### When should information become organizational knowledge?

Not simply when it is memorable, repeated, relevant, or retrieved successfully.

It should become organizational knowledge only under an explicit admission regime that separates **visibility, evidential support, authority, scope, temporal validity, and action eligibility**. Different kinds of claims should require different levels of evidence and authorization.

### How can a team correct a shared belief without destroying valid information that depended on it?

Not through simple deletion or last-write-wins replacement.

The organization must preserve **versioned provenance and dependency structure**, mark the changed premise, identify affected descendants, distinguish conclusions with alternative support from those that depended exclusively on the invalid premise, selectively recompute affected reasoning, and separately revalidate active plans and actions.

That is essentially **truth maintenance for autonomous organizations**, complicated by language-model uncertainty, incomplete provenance, access control, strategic participants, and persistent external actions.

The most consequential future question may therefore no longer be:

> “How should an agent remember?”

It may be:

> **“How should an autonomous organization decide what it knows—and change its mind safely?”**
