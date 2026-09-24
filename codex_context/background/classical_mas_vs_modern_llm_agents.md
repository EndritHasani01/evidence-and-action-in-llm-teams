# Classical Multi-Agent Systems vs Modern LLM Agents
## A critical knowledge-transfer report

**Research cutoff: 20 September 2026.** This report treats modern LLM-agent systems as a new computational substrate for multi-agent systems rather than as an entirely new discipline. The classical literature is broad enough that “multi-agent AI” already had mature theories of distributed optimization, coordination, bargaining, organizations, trust, social choice, decentralized control, learning, and fault tolerance decades before LLM agents appeared. Shoham and Leyton-Brown's foundational text alone spans distributed constraint solving, game theory, communication, learning, social choice, mechanism design, auctions, coalitional games, and logics of knowledge and belief. ([masfoundations.org](https://masfoundations.org/?utm_source=chatgpt.com))

A particularly timely 2026 analysis reaches essentially the same high-level conclusion: current “Agentic AI” and traditional MAS have developed largely in parallel, and contemporary platforms only partially instantiate the richer agent, environment, interaction, and organizational structures studied in classical MAS. ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/FAIA251237?utm_source=chatgpt.com))

The central conclusion of this investigation is:

> **Most high-level multi-agent problems being discussed around LLMs are not new. What may be new is what happens when the agents solving those old problems are pretrained, stochastic, language-mediated foundation models that violate the assumptions under which classical solutions were developed.**

That distinction is extremely important. “Delegation,” “specialization,” “manager agents,” “agent reputation,” “negotiating agents,” “hierarchical teams,” “majority voting,” “shared beliefs,” and “learned communication” are generally not novelty claims. The scientifically interesting question is usually **which classical result ceases to work, why an LLM violates its assumptions, and what theory or mechanism replaces it.**

---

## 1. The right mental model: classical problem, new agent substrate

Classical MAS often assumes that an agent has some reasonably well-defined combination of observations, actions, goals or utilities, internal state, capabilities, and protocol semantics. These quantities can be incomplete or private, agents can be selfish or faulty, and the computational problem can be extremely hard—but at least the mathematical objects are normally specified.

LLM agents upset that picture in several ways simultaneously.

An LLM's “capability” is conditional on prompt wording, context contents, available tools, demonstrations, decoding, model version, conversation history, and sometimes the identities or statements of other agents. Its apparent “belief” is not necessarily a persistent proposition stored in an explicit epistemic state. Its stated confidence need not correspond to a calibrated probability. An instruction to maximize a payoff does not guarantee expected-utility maximization. A natural-language commitment is not equivalent to an executable constraint. Two separately instantiated agents may have highly correlated priors because they share training data or even identical weights. And communication can alter the recipient's reasoning process through persuasion or sycophancy rather than merely transmit information.

This is why merely taking a classical MAS problem and inserting LLMs does not automatically create a new scientific problem—but it **can** create one when one of those assumptions becomes consequential.

A useful crosswalk is:

| Area | Classical inheritance | Assumption most stressed by LLM agents | Particularly interesting modern question |
|---|---|---|---|
| Distributed problem solving | task allocation, DCSP/DCOP, Contract Net | tasks/capabilities are well represented | How can tasks and competence be inferred reliably from language and execution? |
| Dec-POMDPs | decentralized control under partial observability | finite/known state, action, observation and reward models | What is an adequate state representation for text/tool histories? |
| Coordination | joint plans, commitments, partial global plans | commitments and messages have stable semantics | How do we make linguistic commitments executable and auditable? |
| Negotiation | bargaining strategies, concessions, multi-issue negotiation | stable utilities and rational evaluation | What happens when preferences are latent, inconsistent or language-sensitive? |
| Auctions | truthful mechanisms, allocation algorithms | agents know valuations and understand rules | Can mechanisms remain robust to semantic misunderstanding and bounded reasoning? |
| Mechanism design | incentive compatibility, equilibrium, impossibility results | utility maximization is behaviorally predictive | How should institutions be designed for pretrained policies rather than ideal rational agents? |
| Trust | uncertainty-aware partner selection | outcomes reveal stable underlying ability | Can competence be identified when task assignment and context affect performance? |
| Reputation | aggregation of historical/social evidence | persistent identity and independent evidence | How should reputation handle correlated models, capability drift and identity laundering? |
| Coalition formation | coalition-value optimization and coalitional games | coalition value is reasonably well-defined | How should teams be composed when interaction itself changes members' performance? |
| Organizations | hierarchies, teams, markets, federations, matrices | roles and authority are enforceable | How do prompt-defined roles differ from actual authority and control? |
| Social choice | voting, manipulation, aggregation, impossibility | individual preferences/beliefs pre-exist aggregation | What if debate itself changes the “votes” through social influence? |
| Belief revision | AGM, epistemic logic, multi-agent belief change | beliefs are explicit propositions | How do we retract language-derived conclusions and their downstream effects? |
| Distributed planning | explicit operators, dependencies, shared plans | preconditions/effects and execution status are reliable | How do we plan when actions and completion claims themselves need verification? |
| MARL | nonstationarity, credit assignment, CTDE, learned communication | cheap repeated interaction and explicit rewards | How do we post-train enormous pretrained agents jointly and isolate coordination learning? |
| Byzantine tolerance | authenticated messages, quorums, explicit fault models | values have exact identity; “honest” processors execute correctly | What does agreement mean for semantically equivalent but nonidentical language? |

That table is the core bridge. The remainder explains why.

---

# 2. Distributed problem solving: orchestration is much older than LLM agents

One of the clearest examples of rediscovery is task delegation.

The **Contract Net Protocol**, published by Reid Smith in 1980, already treated distributed task assignment as negotiation: a node announces work, potentially capable nodes respond, and tasks are allocated based on those responses. It explicitly motivated negotiation as a way to distribute control and data and make resource-allocation decisions. ([cse-robotics.engr.tamu.edu](https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/smith80contract.pdf?utm_source=chatgpt.com))

So a modern architecture containing:

**manager → announce subtask → workers advertise capability → manager selects worker → worker reports result**

is not, at the organizational level, a new LLM idea. It is recognizably Contract Net.

Distributed constraint satisfaction and optimization went considerably further. **ADOPT**, for example, provides an asynchronous, polynomial-space DCOP algorithm with global-optimality guarantees and bounded-error approximation under its model. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0004370204001511?utm_source=chatgpt.com))

Modern “agent routing” therefore sits on top of a long task-allocation and distributed-optimization tradition. A 2026 system such as SkillOrchestra learns fine-grained skill-conditioned competence and cost and then routes work accordingly. That is technically interesting, but the abstract problem—**allocate tasks among heterogeneous agents under performance/cost differences**—is classical. ([arxiv.org](https://arxiv.org/abs/2602.19672?utm_source=chatgpt.com))

### What changes with LLM agents?

The hard new part is that the quantities being optimized become slippery.

A classical resource allocator may know that machine A processes a job at cost 5 and machine B at cost 8. An LLM orchestrator instead has to estimate statements such as:

> “Model A is probably better at debugging this kind of Python concurrency failure, given these particular tools, this prompt, this repository state, the preceding dialogue, and the fact that another agent has already produced an incomplete patch.”

That competence is **endogenous to the context**.

Furthermore, observed performance is selected by the orchestrator itself. If agent A gets only easy tasks and B gets difficult ones, raw success rates confound competence with assignment. If A is rarely selected, uncertainty remains high. This reconnects routing with contextual bandits, causal inference, reputation systems, and exploration—not merely “agent orchestration.”

### Rediscoveries

Much current language around “dynamic delegation,” “agent specialization,” “skill routing,” “manager-worker architectures,” and “agent selection” belongs here.

### Legitimately new directions

The stronger questions concern **capability identification under context-dependent performance**, semantic task specification, capability drift as models/tools change, and allocation when the worker can misunderstand or reinterpret the task rather than simply fail to execute it.

That is a different scientific claim from inventing delegation.

---

# 3. Distributed planning and coordination: stale state and commitments were already known problems

Modern papers often describe agents as failing because they have incomplete knowledge of what teammates are doing, make incompatible plans, communicate too late, or violate prior agreements.

Classical MAS studied precisely these phenomena.

Durfee and Lesser's **Partial Global Planning** work coordinated agents despite incomplete and potentially obsolete views of distributed activity. ([mas.cs.umass.edu](https://mas.cs.umass.edu/pub/paper_detail.php/26?utm_source=chatgpt.com))

The SharedPlans tradition explicitly formalized collaborative activity, including partial knowledge about how actions should be performed and the possibility of contracting actions to others. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0004370295001034?utm_source=chatgpt.com))

Tambe's **STEAM** model went still closer to what many LLM-team papers now call “agent coordination”: agents maintain joint intentions, monitor teammates, reorganize after failures, and selectively communicate depending on the costs and benefits of communication. This work dates to the 1990s. ([arxiv.org](https://arxiv.org/abs/cs/9709101?utm_source=chatgpt.com))

Consequently:

> “Agents need shared goals, role responsibilities, commitments, monitoring, repair, and selective communication”

is not a novel diagnosis of LLM teams.

### Where LLMs genuinely alter coordination

A symbolic commitment such as

\[
\text{committed}(A,\; \text{implement API X before }t)
\]

has defined semantics.

An LLM saying:

> “Sure, I'll handle the API layer.”

does not.

Did it understand the interface? Does “handle” imply implementation, tests, documentation, or merely analysis? Will that sentence constrain later action? Does it remain in context? Can another instruction override it? Can an external system verify whether the commitment has been discharged?

This **semantic-to-operational gap** is much more specific to language-mediated agents.

CooperBench illustrates the point empirically. Its coding tasks give two agents individually feasible but potentially conflicting modifications. The authors report an average coordination penalty and diagnose vague/poorly timed communication, deviations from commitments, and incorrect expectations about teammates. ([arxiv.org](https://arxiv.org/abs/2601.13295?utm_source=chatgpt.com))

But “agents violate commitments” itself is not the scientific novelty. The deeper LLM-specific problem is:

> **What makes a language-model commitment causally binding enough to function as a coordination primitive?**

Potential answers might involve structured commitments, executable interface contracts, acknowledgement protocols, shared state, test-backed verification, or external enforcement.

That is a much stronger research question than inventing another “coordinator agent.”

---

# 4. Dec-POMDPs: distributed partial observability is not a new LLM problem

Suppose several agents each possess only part of the relevant information and must cooperate without access to the entire state.

That is almost the canonical motivation for **Decentralized Partially Observable Markov Decision Processes**.

The classical framework formalizes multi-agent sequential decision-making under decentralized observation. The difficulty is fundamental: Bernstein et al. established NEXP-hardness for finite-horizon decentralized problems even with only two agents, under the formulations they study. ([pubsonline.informs.org](https://pubsonline.informs.org/doi/abs/10.1287/moor.27.4.819.297?journalCode=moor&utm_source=chatgpt.com)) Oliehoek and Amato's monograph develops exact, approximate, and heuristic planning approaches for Dec-POMDPs. ([link.springer.com](https://link.springer.com/book/10.1007/978-3-319-28929-8?utm_source=chatgpt.com))

So:

> “Different agents have different observations and need to communicate in order to solve the global problem”

is not a novel multi-agent formulation.

SILO-BENCH is valuable precisely because it studies how **LLM policies instantiate** this old structural problem. It splits information across agents and varies the communication structure; the 2026 paper reports that agents can communicate heavily yet fail to translate communication into the distributed computation required by harder tasks. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/?utm_source=chatgpt.com))

### What classical Dec-POMDP assumptions become problematic?

The usual formalism requires a state space, observation model, transition structure, action space and reward specification. They may be huge or unknown to the agents, but the researcher knows what the objects mean.

In an open-ended LLM workflow:

- the “state” can include millions of tokens of documents, tool outputs and external application state;
- observations are semantic text, not fixed symbols;
- generated actions can be malformed or novel;
- tool descriptions partially define action semantics;
- conversation history itself changes future policy;
- the effective observation depends on retrieval and context truncation;
- model updates or provider changes can change the policy during deployment.

The promising research direction is therefore not merely “Dec-POMDP + LLM.”

It is developing **tractable abstractions of decentralized open-world semantic state** and determining which classical decentralized-control results survive those abstractions.

For example, what counts as a sufficient statistic for an agent's history when the policy is an LLM? Can a structured belief state outperform raw transcript accumulation? What information must be communicated for decentralized optimality—or at least safe bounded behavior—when agents cannot exactly model one another?

Those are real bridges between the fields.

---

# 5. Negotiation: LLM bargaining did not invent automated negotiation

Autonomous-agent negotiation was mature well before modern language models.

Faratin, Sierra and Jennings presented a formal computational model in 1998 covering generation of initial offers, proposal evaluation, counteroffers, strategies and tactics. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0921889098000293?utm_source=chatgpt.com)) Classical literature subsequently became extensive enough that modern MAS textbooks divide negotiation into single-issue, multi-issue, heuristic, human-agent, and argumentation-based approaches. ([mitpress.ublish.com](https://mitpress.ublish.com/book/multiagent-systems-0?utm_source=chatgpt.com))

Therefore buyer and seller LLMs exchanging proposals in natural language do not by themselves constitute a new problem.

### Classical assumptions that become fragile

Negotiation theory usually needs preferences or utilities sufficiently well specified that one can evaluate an agreement.

An LLM negotiating “on behalf of” someone may instead have:

- an incompletely specified goal;
- soft natural-language constraints;
- contradictory instructions;
- no stable preference ordering over possible deals;
- imperfect understanding of the other side's proposal;
- difficulty calculating its own utility;
- susceptibility to framing or rhetoric;
- normative conversational tendencies learned during alignment.

This makes **preference formation part of the negotiation process itself**.

In classical bargaining, language usually communicates information about preferences and offers. With LLMs, language may also alter the computational policy evaluating those preferences.

### New scientific questions

The more interesting frontier is therefore negotiation under **semantic, behavioral and objective uncertainty**.

Can an agent distinguish “I prefer this” from “the other party persuaded my language model to describe this as preferable”? Can an autonomous buyer verify that a natural-language agreement satisfies hard constraints before committing funds? How should a mechanism respond when an agent misunderstands a payoff matrix rather than strategically misreporting its valuation?

That is much more distinctive than showing that two LLMs can bargain.

---

# 6. Auctions: marketplaces and bidding are deeply classical

Agent auctions are another area where historical awareness matters.

Vickrey's 1961 work established the canonical second-price auction setting. ([doi.org](https://doi.org/10.1111/j.1540-6261.1961.tb02789.x?utm_source=chatgpt.com)) Classical computational MAS subsequently studied combinatorial auctions, bidding languages and winner determination. General combinatorial winner determination is NP-complete, motivating exact search, approximation and restricted cases. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S000437020100159X?utm_source=chatgpt.com))

Thus future systems in which AI agents bid for compute, tasks, data or services are applying old economic machinery to new participants.

### What is actually new?

The valuation itself may no longer be clean.

An autonomous coding agent may not know in advance:

\[
v(\text{access to GPU for 20 min})
\]

because its expected benefit depends on whether its current reasoning strategy succeeds, whether another agent finishes first, whether its context contains the relevant information, and whether the purchased resource actually proves useful.

LLM agents may also fail to understand a truthful mechanism. Strategy-proofness says that truthful reporting is optimal **given the mechanism model and relevant rationality assumptions**. It does not guarantee that an LLM will infer, understand or execute the dominant strategy.

This suggests a potentially important concept:

> **behaviorally robust mechanism design**—mechanisms that work well not merely against perfectly rational strategic agents, but with bounded, semantically imperfect pretrained policies.

The classical mechanism remains the baseline. The novelty would lie in characterizing the deviations.

---

# 7. Mechanism design: “design incentives for agents” is almost the definition of the field

Nisan and Ronen's 2001 **Algorithmic Mechanism Design** explicitly starts from distributed computational settings where participants cannot be assumed simply to execute the intended algorithm because they pursue their own interests. The designer therefore constructs incentives so correct behavior serves those interests. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S089982569990790X?utm_source=chatgpt.com))

Mechanism design also provides impossibility results rather than only solutions. Myerson and Satterthwaite showed, under their bilateral-trade assumptions, that one cannot simultaneously obtain all the desired efficiency, incentive and participation properties without outside subsidy. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0022053183900480?utm_source=chatgpt.com))

This is exactly why modern LLM-agent research should be cautious with claims such as:

> “We introduce incentives to make agents cooperate.”

The idea of changing the rules of interaction so self-interested agents produce desirable outcomes is not new.

CoopEval is intellectually interesting in part because it explicitly imports classical institutional mechanisms—repetition, reputation, mediation and contracts—and asks how present LLMs behave inside them. Its 2026 experiments report meaningful differences between these mechanisms, including strong performance from contracting and mediation in the studied games. ([arxiv.org](https://arxiv.org/abs/2604.15267?utm_source=chatgpt.com))

That is the right direction: **test classical institutions on a strange new class of bounded agent**, rather than rename the institution.

### The key LLM distinction: equilibrium existence versus equilibrium realization

Classical theory might establish that cooperation is an equilibrium under contract \(M\).

Three separate questions arise for an LLM:

\[
\text{Exists} \;\neq\; \text{Recognized} \;\neq\; \text{Selected}.
\]

The mechanism can make a cooperative strategy optimal while the model fails to understand why.

This suggests an underdeveloped research space between mechanism design and behavioral economics:

**mechanism comprehension**, **equilibrium discovery**, **policy realization**, and **institutional robustness under bounded semantic reasoning**.

Those are legitimate LLM-agent questions.

---

# 8. Trust and reputation: an especially high-risk area for rediscovery

Computational trust was already a substantial MAS topic by the early 2000s. Ramchurn, Huynh and Jennings described trust as a way of reducing uncertainty in interactions in large, open, changing systems and surveyed multiple computational approaches. ([cambridge.org](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/trust-in-multiagent-systems/C5B2F5A2B8D66354CB04F2148BF144F2?utm_source=chatgpt.com)) Classical reputation work separately studied how social evaluations should be represented and aggregated. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0888613X07000059?utm_source=chatgpt.com))

Therefore the following are not inherently new:

- assigning trust scores;
- weighting testimony by historical reliability;
- decaying old evidence;
- asking other agents for recommendations;
- choosing partners based on reputation;
- maintaining separate direct and indirect evidence.

### Where LLM-agent trust becomes genuinely difficult

Classical reputation commonly treats an agent as having a persistent enough behavioral property for historical performance to carry information forward.

For LLM agents, what is the entity being trusted?

The API endpoint? The base model? The system prompt? The model-plus-tools bundle? The organization operating it? The current conversation? A named “persona” instantiated yesterday and recreated today?

Furthermore,

\[
P(\text{success}\mid \text{agent})
\]

is often the wrong quantity. A better object may be something like

\[
P(
\text{success}
\mid
\text{model},
\text{skill},
\text{task difficulty},
\text{tools},
\text{prompt},
\text{teammates},
\text{context},
\text{evaluator}
).
\]

This converts reputation into an **identification problem**.

Identity-driven social behavior makes this more serious. ACL 2026 work reports both peer-directed sycophancy and self-bias in multi-agent debate, and finds that anonymizing identity markers can reduce the effect. ([aclanthology.org](https://aclanthology.org/2026.acl-long.650/?utm_source=chatgpt.com))

So an apparent “trust update” may not actually reflect Bayesian learning about competence. It may partly be a social response to who allegedly produced the message.

### Strong modern question

A much more defensible trust project would ask:

> **Under what observable evidence is another LLM agent's task-conditional reliability identifiable at all?**

That immediately connects to selective assignment, confounding, calibration, feedback delays, correlated errors and exploration.

It is substantially deeper than another scalar reputation score.

---

# 9. Coalition formation: dynamically creating teams is also classical

Coalition formation has a mature algorithmic and game-theoretic literature.

Sandholm and colleagues showed that optimal coalition-structure generation is NP-complete and developed anytime search algorithms with worst-case guarantees. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0004370299000363?utm_source=chatgpt.com)) Classical MAS also studies coalition values, payoff allocation, stability, externalities and compact representations.

Consequently, dynamically deciding:

> “Which subset of available agents should work together?”

is not by itself a new problem.

### Where LLMs change coalition value

Classical coalition analysis typically needs some notion of coalition value \(v(S)\).

With LLM agents, \(v(S)\) may not be stable.

Adding another model can:

- provide complementary knowledge;
- add independent sampling;
- introduce correlated mistakes;
- persuade correct agents away from their answers;
- consume context;
- increase latency;
- create coordination overhead;
- alter role behavior;
- change how other agents reason.

Thus,

\[
v(S)
\]

may depend on the communication protocol, ordering, prompts, model identities, context budget and even the conversation trajectory.

In other words, coalition value becomes **interaction-endogenous**.

That is a legitimate scientific complication.

A modern coalition-formation project becomes much stronger if it models not just “which experts have which skills,” but how coalition composition changes the **joint error structure and interaction dynamics**.

---

# 10. Organizational structures: “hierarchical agents” are several decades late as a concept

This is perhaps the starkest terminology mismatch.

Horling and Lesser's survey of MAS organizations explicitly covers:

**hierarchies, holarchies, coalitions, teams, congregations, societies, federations, markets and matrix organizations**, discussing their different strengths and weaknesses and the fact that organizational design measurably changes system performance. ([mas.cs.umass.edu](https://mas.cs.umass.edu/pub/paper_detail.php/366?utm_source=chatgpt.com))

Classical teamwork theories also formalized roles, team plans, responsibilities and reorganization after failures. ([arxiv.org](https://arxiv.org/abs/cs/9709101?utm_source=chatgpt.com))

So comparing a “flat multi-agent system” with a “hierarchical multi-agent system” in 2026 is not conceptually novel.

### But modern implementations often contain something strange

A classical organizational role can correspond to actual information rights, action authority, obligations and communication structure.

In many LLM frameworks:

> “You are the manager.”

is merely text in a prompt.

The “manager” may have no actual power except that its message is appended to another model's context. A “reviewer” may have no ability to prevent deployment. A “specialist” may use the exact same model with a different role description. A nominally independent verifier may share the same training biases as the worker.

This creates an extremely interesting distinction:

\[
\text{role label} \neq \text{authority} \neq \text{capability} \neq \text{control right}.
\]

The 2026 paper comparing Agentic AI with traditional MAS makes a similar structural observation: contemporary agentic systems tend to offer much thinner environment, interaction and organization modeling than traditional MAS frameworks, with communication frequently centered on task delegation. ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/FAIA251237?utm_source=chatgpt.com))

### A genuinely modern organizational question

Instead of asking:

> “Are hierarchies better than flat teams?”

ask:

> **Which organizational properties must be externally enforced rather than represented linguistically for an LLM organization to behave like the organization its architecture claims to implement?**

That question connects MAS organization theory with access control, software architecture, HCI and institutional design.

---

# 11. Social choice: majority voting among agents is very old; endogenous persuasion is not

Whenever several agents produce candidate answers and a system aggregates them, computational social choice should immediately come to mind.

The classical field studies preference aggregation, voting rules, manipulation, control, bribery, fairness and impossibility. The Gibbard-Satterthwaite theorem, for example, sharply limits what unrestricted deterministic voting rules can simultaneously achieve when there are at least three alternatives. ([cambridge.org](https://www.cambridge.org/core/books/abs/handbook-of-computational-social-choice/barriers-to-manipulation-in-voting/6D69B6B30A67AB0BB0F671D309C3CFDD?utm_source=chatgpt.com))

Modern multi-agent debate frequently ends in majority voting. But NeurIPS 2025's **Debate or Vote** reports that majority voting alone explains much of the gain attributed to multi-agent debate on the authors' seven evaluated NLP benchmarks. Their theoretical result is conditional on their stochastic belief-update model; it should not be generalized into “debate can never help.” ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html?utm_source=chatgpt.com))

Scientifically, this is an excellent example of classical concepts clarifying modern work:

**independent sampling + aggregation** and **interaction** are distinct mechanisms.

### What genuinely changes with LLMs?

Traditional social-choice analysis often takes voter preferences as the objects being aggregated.

LLM debate makes the aggregation process endogenous:

\[
\text{message from B}
\rightarrow
\text{changes A's reasoning}
\rightarrow
\text{changes A's vote}.
\]

The “voters” are influencing one another before aggregation.

ACL 2026 evidence of identity-related sycophancy makes this especially concrete. ([aclanthology.org](https://aclanthology.org/2026.acl-long.650/?utm_source=chatgpt.com))

The richer modern question is therefore:

> **How should collective decisions be aggregated when participants are correlated, socially influenceable computational policies rather than independent holders of stable preferences?**

That is closer to social learning, opinion dynamics and Bayesian social choice than generic “LLM debate.”

---

# 12. Belief revision: shared memory is not the beginning of belief-change theory

Modern agent systems increasingly maintain persistent organizational memories and attempt to update them when new information arrives.

Classical AI already developed a deep theory of belief change. AGM belief revision formalized rational principles for adding, removing and revising beliefs. The theory was later generalized explicitly to multi-agent settings; Aucher's 2010 work shows how classical AGM results transfer and introduces additional postulates particular to multiple agents. ([academic.oup.com](https://academic.oup.com/jigpal/article-abstract/18/4/530/726837?utm_source=chatgpt.com))

Therefore:

> “An agent receives contradictory information and must update its belief”

is very old.

### Why LLM memory is nevertheless a serious new problem

The classical theory manipulates propositions and explicit epistemic structures.

An LLM organization's “belief” may be distributed across:

- pretrained model weights;
- conversation context;
- retrieved documents;
- vector-store entries;
- summaries;
- databases;
- previous agent outputs;
- cached plans;
- downstream conclusions derived from an earlier claim.

Suppose a team learns that claim \(p\) was false.

Deleting the memory containing \(p\) does not necessarily remove:

\[
q,\;r,\;s
\]

that were derived from \(p\).

And an LLM may regenerate \(p\) from its parametric prior after the explicit record is removed.

This turns belief revision into a combined problem of **provenance, dependency tracking, semantic equivalence and persistent model priors**.

That is substantially different from simply storing larger memories.

A strong research direction is therefore:

> **dependency-aware organizational belief revision for semantically represented knowledge.**

The classical literature supplies rational desiderata; LLM systems introduce the difficult representational substrate.

---

# 13. MARL: “agents learning to collaborate” is emphatically not a new conceptual category

Multi-agent reinforcement learning has spent decades on precisely the challenges now appearing in “learning LLM collaboration”:

- non-stationarity because other learners change;
- coordination;
- decentralized execution;
- communication learning;
- partial observability;
- credit assignment;
- scalability;
- partner adaptation.

A major MARL survey explicitly identifies nonstationarity, communication, coordination, credit assignment, scalability and partial observability as core multi-agent challenges. ([doi.org](https://doi.org/10.1007/s10462-021-09996-w?utm_source=chatgpt.com))

So phrases such as:

> “team reward,” “credit assignment,” “emergent communication,” “joint policy optimization,” “centralized training/decentralized execution”

belong directly to MARL.

The 2026 MAGRPO paper makes this connection explicitly: it formulates multi-turn LLM collaboration as cooperative MARL and optimizes LLM policies with team rewards. ([ojs.aaai.org](https://ojs.aaai.org/index.php/AAAI/article/view/40487?utm_source=chatgpt.com))

### What LLMs contribute that MARL did not already settle

The policy class has changed dramatically.

Classical MARL often trains policies from scratch through enormous numbers of relatively cheap interactions. An LLM agent begins as an enormous pretrained policy containing language, world knowledge, social conventions, reasoning heuristics and instruction-following tendencies.

Training it jointly raises unusual questions.

If team performance improves after multi-agent post-training, was the model taught:

- better individual reasoning,
- better communication,
- better task decomposition,
- a benchmark-specific convention,
- better imitation of teammates,
- or actual partner-general collaboration?

If several agents share parameters, who exactly learned what?

If one model update changes all roles simultaneously, traditional notions of independent learner nonstationarity require reinterpretation.

And because episodes involving large LLMs are expensive, the sample regime differs drastically from many classical MARL settings.

So the strongest research is not “apply RL to multi-agent LLMs.” It is:

> **Which MARL concepts survive foundation-model pretraining, parameter sharing, natural-language action spaces and extremely expensive trajectories?**

That is legitimately interesting.

---

# 14. Byzantine fault tolerance: majority voting is not fault tolerance

Fault-tolerant distributed computing supplies another body of theory that LLM research risks rediscovering incompletely.

Lamport, Shostak and Pease's Byzantine Generals work formalized agreement in the presence of faulty or malicious participants. In the classical unauthenticated setting, agreement requires more than two-thirds of participants to be nonfaulty; authenticated signatures materially change what can be tolerated. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/byzantine-generals-problem/?utm_source=chatgpt.com))

Thus a paper that places five LLMs together, makes one malicious and then adds majority voting is entering a domain with strong existing theory.

### Yet LLMs expose a genuinely unusual fault model

Classical consensus normally asks nodes to agree on values whose identity is exact.

LLMs generate statements such as:

> “The transfer is safe because condition A holds.”

and

> “I recommend proceeding; requirement A appears satisfied.”

These may be semantically equivalent without byte equality.

Worse, a completely “honest” LLM can hallucinate.

So we need at least three categories:

\[
\text{correct honest agent},\qquad
\text{honest but semantically wrong agent},\qquad
\text{adversarial agent}.
\]

Traditional Byzantine models usually do not equate honest execution with a stochastic semantic reasoner that can confidently produce false propositions.

The June 2026 H-CSC preprint explicitly tackles this mismatch by distinguishing semantic-level commitments from verdict-level commitments and safe aborts rather than requiring byte-identical LLM proposals. It should currently be treated as recent preprint evidence, not settled BFT theory. ([arxiv.org](https://arxiv.org/abs/2606.07316?utm_source=chatgpt.com))

### Real new questions

The useful frontier includes semantic agreement, correlated non-adversarial faults, provenance-aware consensus, semantic equivocation, and deciding what “agreement” should mean when outputs are structured natural language rather than deterministic machine values.

Crucially:

> **consensus is not truth.**

One hundred agents can Byzantine-agree on a false proposition.

That distinction should be central to LLM verification research.

---

# 15. The deepest modern difference: language is simultaneously message, state and intervention

Across all these areas, one distinctive feature keeps recurring.

Classical communication protocols tend to distinguish a message's **content** from the recipient's decision procedure.

LLM systems blur them.

A message can simultaneously:

1. transmit factual information;
2. provide an instruction;
3. alter the recipient's framing of the task;
4. change perceived authority;
5. induce conformity;
6. overwrite working memory;
7. introduce executable content for a later tool call.

That makes natural language not merely a communication channel but a **policy-level intervention**.

This helps explain why classical communication-theoretic intuitions alone may be insufficient. SILO-BENCH finds active communication without effective distributed computation, while identity-bias experiments show that even irrelevant identity information can change how peer evidence is weighted. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1354/?utm_source=chatgpt.com))

A useful conceptual decomposition for modern research is therefore:

\[
\text{message} =
\text{evidence}
+
\text{control signal}
+
\text{social cue}
+
\text{context modification}.
\]

Classical MAS contains pieces of all four. Their fusion inside a single pretrained language policy is much more distinctive.

---

# 16. Another major difference: errors are correlated in ways “multiple agents” can hide

Calling ten LLM instances ten agents can create an illusion of independence.

If all ten use the same base model, similar prompts and the same retrieved evidence, they can share:

- training-data misconceptions;
- reasoning heuristics;
- safety/alignment biases;
- confidence patterns;
- prompt sensitivities;
- missing knowledge;
- vulnerabilities.

Therefore

\[
n=10 \text{ model instances}
\]

does not mean

\[
n=10 \text{ independent information sources}.
\]

This is central to voting, reputation, verification and BFT.

Classical systems theory certainly studies correlated faults, common-mode failures and dependent information. What is new is that **opaque pretraining makes the correlation structure difficult to observe or model**.

This may ultimately be one of the most important scientific connections between classical MAS and LLM teams: the key object is not agent count but **effective informational diversity**.

---

# 17. Current LLM-agent terminology that often renames classical MAS concepts

The correspondence is close enough that a researcher should mentally translate modern terms before searching for novelty.

| Current phrase | Older literature to search first |
|---|---|
| Agent orchestration | task allocation, distributed problem solving, organization design |
| Dynamic delegation | Contract Net, distributed task allocation, scheduling |
| Agent specialization | heterogeneous agents, role allocation, organizational roles |
| Planner–worker system | hierarchical planning, team plans, task decomposition |
| Manager agent | organizational hierarchy, supervisory control |
| Agent handoff | task transfer, contracting, coordination |
| Shared agent memory | distributed knowledge, belief maintenance, blackboards |
| Agent reputation | computational trust and reputation |
| Debate/voting | computational social choice, ensemble decision systems |
| Agent negotiation | automated negotiation, bargaining theory |
| Agent marketplace | auctions, resource allocation, mechanism design |
| Contracting agents | mechanism design, contracting, commitment protocols |
| Agent teams | teamwork, joint intentions, SharedPlans |
| Dynamic team formation | coalition formation |
| Learned communication | MARL communication |
| Learned cooperation | cooperative MARL |
| Agent consensus | distributed consensus/BFT or social choice, depending on meaning |
| Malicious teammate | Byzantine/adversarial participant models |
| Multiple reviewers | fault tolerance, redundant verification, ensemble aggregation |
| Agent topology | organizational structure, interaction graphs |
| Partial information agents | Dec-POMDPs, distributed sensing, DCSP |
| Coordination failure | potentially DCOP, teamwork, planning, organization or protocol failure |

Searching only for the modern phrase can therefore give a badly distorted view of novelty.

---

# 18. What genuinely seems new about LLM multi-agent systems?

After subtracting classical MAS, several substantial scientific problems remain.

### Semantic rather than symbolic interaction

Inputs, plans, contracts, reputations and commitments exist as natural language whose operational meaning has to be inferred.

### Context-dependent capabilities

An agent's competence is not a fixed scalar and may change drastically with prompts, tools, context and collaborators.

### Opaque epistemic state

There is no clean mapping from generated language to persistent beliefs, confidence or intentions.

### Socially responsive reasoning policies

Identity, authority and rhetorical framing can change a model's answer independently of evidence quality. ACL 2026 measurements of sycophancy and self-bias provide concrete evidence of such effects. ([aclanthology.org](https://aclanthology.org/2026.acl-long.650/?utm_source=chatgpt.com))

### Pretrained correlated populations

Separate instances can inherit common priors and failure modes through shared model weights and training data.

### Language-mediated commitments without enforcement

Agents can agree fluently while later behaving inconsistently with the agreement, a pattern visible in CooperBench. ([arxiv.org](https://arxiv.org/abs/2601.13295?utm_source=chatgpt.com))

### Natural-language actions interacting with real tools

Errors move from propositions into external state: code, purchases, databases, emails, infrastructure and other agents.

### Foundation-model MARL

Instead of learning small policies from scratch, researchers are trying to modify enormous pretrained general-purpose policies through relatively sparse interaction data. ([ojs.aaai.org](https://ojs.aaai.org/index.php/AAAI/article/view/40487?utm_source=chatgpt.com))

### Semantic fault tolerance

Consensus has to handle equivalent-but-nonidentical language, uncertain reasoning, hallucination and adversarial semantic manipulation. ([arxiv.org](https://arxiv.org/abs/2606.07316?utm_source=chatgpt.com))

These are not “LLMs made MAS new.” They are **specific points where a new substrate invalidates an old abstraction**.

---

# 19. MAST-style failures: new observations do not necessarily imply new mechanisms

Modern failure taxonomies remain useful even when their categories have historical analogues.

MAST analyzes more than 1,600 multi-agent LLM traces and identifies 14 failure modes organized around system design, inter-agent misalignment, and verification. ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html?utm_source=chatgpt.com))

Failures such as poor task allocation, failure to coordinate, premature termination and bad verification clearly echo classical problems.

That does **not** make MAST scientifically unimportant.

There is a critical distinction:

> **“This conceptual class of failure was known” does not imply “we already know whether present LLM systems exhibit it, at what frequency, under what conditions, or why.”**

Empirical characterization of a known theoretical phenomenon in a radically different policy class can be a real contribution.

The novelty should simply be stated correctly.

For example:

**Weak claim:**  
“We discover that agents can fail because they do not coordinate.”

**Stronger claim:**  
“Classical teamwork predicts failure when commitments are not synchronized; we show that LLM agents systematically violate explicitly communicated commitments even when message delivery and local competence are controlled, and identify condition X under which the violation increases.”

The second advances knowledge.

---

# 20. A useful novelty taxonomy

After comparing the literatures, I would divide prospective LLM-MAS projects into four categories.

### A. Direct rediscovery

The classical formulation already captures the essential problem and the LLM merely supplies a different implementation.

Examples include generic task delegation, basic voting, fixed hierarchies, simple reputation averages and role assignment.

These may be worthwhile engineering projects, but the scientific novelty bar is high.

### B. Classical problem, empirical new population

The phenomenon is known theoretically, but we do not know how foundation-model policies behave under it.

Examples include testing established bargaining mechanisms on LLM agents or measuring whether joint-intention failures occur in coding agents.

This can support good empirical science.

### C. Classical model under violated assumptions

An old theorem or algorithm depends on an assumption that LLMs systematically violate.

Examples include social choice with socially influenceable voters, BFT with semantically stochastic honest nodes, or reputation with context-dependent identities.

This is especially promising because the classical literature gives a precise baseline.

### D. New interaction object created by LLMs

The substrate introduces something that the classical abstraction did not naturally contain.

Examples include prompt injection propagating between agents, language simultaneously carrying data and control, model-weight-induced common-mode reasoning failures, or natural-language agreements whose semantic interpretation is itself strategic.

These have the strongest claim to genuinely new scientific territory.

---

# 21. Classical theory should be used as an experimental generator

The best use of classical MAS is not merely adding citations to the related-work section.

It should generate experiments.

Suppose you think an LLM hierarchy fails because workers obey an incorrect manager.

Classical organization theory tells you to distinguish **information centralization**, **decision authority**, **communication topology**, and **responsibility**. Instead of comparing two giant frameworks called “flat” and “hierarchical,” vary one property at a time.

Suppose you think LLM reputation fails.

Trust theory tells you to separate **direct evidence**, **social testimony**, **confidence**, **context**, **recency** and **witness reliability**. Then test which signal is actually identifiable.

Suppose you think LLM agents cannot collaborate over information silos.

Dec-POMDP and distributed-algorithm literature suggests measuring what minimum information must move and whether the observed communication approaches that requirement.

Suppose contracts appear to increase cooperation.

Mechanism design says first determine whether the desired strategy is actually incentive-compatible; behavioral experiments then ask whether LLM agents understand and select it.

This is the real payoff of recovering the classical literature: it produces **stronger controls and sharper hypotheses**.

---

# 22. What classical MAS does *not* give modern researchers for free

It would also be a mistake to swing too far and claim that old MAS has already solved modern LLM teamwork.

A DCOP algorithm with optimality guarantees does not solve natural-language organizational work if no one can specify the cost functions correctly.

A Dec-POMDP formulation does not make an open-world software repository into a tractable finite state space.

A truthful auction does not ensure an LLM understands its valuation.

AGM revision does not tell us how to delete a misconception embedded in model weights.

A Byzantine quorum does not establish truth when honest LLMs hallucinate the same thing.

Joint intentions do not automatically make a sentence generated by an LLM into a persistent commitment.

MARL theory does not tell us how to cheaply post-train five 100-billion-parameter foundation models.

This is why the relationship should be viewed as:

\[
\boxed{
\text{Modern LLM-MAS science}
=
\text{classical interaction structure}
+
\text{foundation-model assumption failures}
}
\]

rather than either “everything is new” or “everything was already solved.”

---

# 23. The concepts a modern LLM multi-agent researcher should know first

Before proposing serious work, I would consider the following a minimum conceptual foundation:

1. **Distributed problem solving, DCSP and DCOP** — especially the distinction between decomposing computation and genuinely decentralized information/control.
2. **Contract Net and distributed task allocation** — so delegation and worker selection are not mistaken for new concepts.
3. **Dec-POMDPs and stochastic games** — for partial observability, decentralized policies and sequential interdependence.
4. **Joint intentions, SharedPlans and teamwork models** — for commitments, responsibilities, monitoring and repair. ([sri.com](https://www.sri.com/publication/teamwork/?utm_source=chatgpt.com))
5. **Partial Global Planning and distributed planning** — particularly stale state, partial plans and coordination under incomplete knowledge. ([mas.cs.umass.edu](https://mas.cs.umass.edu/pub/paper_detail.php/26?utm_source=chatgpt.com))
6. **Automated negotiation and bargaining theory** — utilities, reservation values, concessions, private information and agreement efficiency. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0921889098000293?utm_source=chatgpt.com))
7. **Auction theory and combinatorial allocation** — truthful mechanisms, bidding languages, allocation complexity and winner determination. ([doi.org](https://doi.org/10.1111/j.1540-6261.1961.tb02789.x?utm_source=chatgpt.com))
8. **Mechanism design and its impossibility results** — incentive compatibility, individual rationality, budget balance, efficiency and equilibrium. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S089982569990790X?utm_source=chatgpt.com))
9. **Computational trust and reputation** — context-sensitive evidence, witness information, temporal effects and adversarial manipulation. ([cambridge.org](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/trust-in-multiagent-systems/C5B2F5A2B8D66354CB04F2148BF144F2?utm_source=chatgpt.com))
10. **Coalitional game theory and coalition-structure generation** — because dynamic “agent teams” are coalitions in everything but terminology. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0004370299000363?utm_source=chatgpt.com))
11. **Organizational MAS** — hierarchies, markets, teams, federations, matrices, role relations and organizational adaptation. ([mas.cs.umass.edu](https://mas.cs.umass.edu/pub/paper_detail.php/366?utm_source=chatgpt.com))
12. **Computational social choice** — voting, strategic manipulation, impossibility and preference aggregation. ([cambridge.org](https://www.cambridge.org/core/books/abs/handbook-of-computational-social-choice/barriers-to-manipulation-in-voting/6D69B6B30A67AB0BB0F671D309C3CFDD?utm_source=chatgpt.com))
13. **Belief revision and epistemic logic** — particularly the difference between receiving information, believing it, knowing its source and changing beliefs rationally. ([academic.oup.com](https://academic.oup.com/jigpal/article-abstract/18/4/530/726837?utm_source=chatgpt.com))
14. **MARL** — nonstationarity, decentralized execution, credit assignment, partner adaptation and communication learning. ([doi.org](https://doi.org/10.1007/s10462-021-09996-w?utm_source=chatgpt.com))
15. **Distributed consensus and Byzantine fault models** — including exactly what assumptions produce a fault-tolerance guarantee. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/byzantine-generals-problem/?utm_source=chatgpt.com))

Shoham and Leyton-Brown's *Multiagent Systems* remains unusually efficient as a common foundation because it puts many of these otherwise separate intellectual traditions into one framework. ([masfoundations.org](https://masfoundations.org/?utm_source=chatgpt.com))

---

# 24. A better novelty test for future LLM-agent research

Before accepting a proposed contribution, I would require the researcher to complete this sentence:

> **Classical work X establishes Y under assumptions A. LLM agents violate assumption A because of phenomenon B. Existing work does not establish whether Y still holds under B. Our experiment/intervention C distinguishes the classical prediction from alternative D.**

That one sentence eliminates a surprising number of weak ideas.

For example:

> Contract Net already solves structured task bidding. However, it assumes bids meaningfully encode capability. LLM self-assessments may be systematically miscalibrated and assignment outcomes are selection-biased. We therefore study whether task-specific competence can be identified from realistic execution histories rather than inventing a new delegation protocol.

That is plausible research.

Or:

> Classical social choice studies aggregation of individual preferences, while LLM debate allows communication to endogenously alter those preferences through identity-sensitive influence. We therefore measure when deliberation improves information integration versus merely increasing correlated conformity.

Also plausible.

Or:

> Classical BFT establishes agreement under explicit fault and message assumptions. LLM agents generate semantically equivalent but nonidentical values and honest agents can share hallucinated errors. We therefore study the distinction between semantic agreement, factual validity and common-mode failure.

Again, a clear scientific bridge.

---

# 25. Where I would be especially skeptical of novelty claims in 2026

There is now strong novelty pressure around generic:

**manager-worker architectures, fixed agent roles, hierarchy-vs-flat comparisons, basic debate, majority voting, scalar trust scores, task routing, simple negotiation, reputation, dynamic expert selection, repeated-game cooperation and generic multi-agent RL.**

Not because they are exhausted topics, but because their central abstractions are mature.

The novelty has to lie one layer deeper.

For example, the interesting question is probably not whether routing helps but **whether competence is identifiable**; not whether a hierarchy helps but **which authority mechanism causes the effect**; not whether debate helps but **whether interaction contributes beyond independent sampling**; not whether reputation helps but **what historical evidence actually measures**; not whether contracts induce cooperation but **whether agents comprehend, adopt and correctly execute incentive-compatible agreements**.

Recent LLM research is already beginning to make exactly these decompositions. Debate-or-Vote separates interaction from aggregation; SILO-BENCH separates communication activity from distributed computation; CooperBench separates individual coding ability from interaction failure; MAGRPO reconnects LLM post-training to MARL; and the 2026 traditional-MAS analysis explicitly argues for reconnecting modern agentic AI with established MAS principles. ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html?utm_source=chatgpt.com))

---

# 26. Final assessment

The relationship between classical MAS and modern LLM agents is best understood as **continuity with a major change of substrate**.

The continuity is stronger than much current agentic terminology admits. Multi-agent researchers had already studied decentralized information, negotiation, commitments, heterogeneous capabilities, trust, organizations, coalition formation, voting, incentive design, learning, belief revision and malicious participants long before foundation models.

The change of substrate is nevertheless profound.

LLMs introduce agents whose capabilities are highly contextual; whose internal beliefs and utilities are poorly observable; whose language can simultaneously communicate evidence and modify another agent's policy; whose errors may be strongly correlated through shared pretraining; whose commitments are often merely linguistic; whose “identities” can be ephemeral prompt constructs; and whose open-ended actions interact with external software and humans.

That suggests the most productive intellectual stance for the next generation of research:

\[
\boxed{
\text{Do not ask “What multi-agent problem can we invent for LLMs?”}
}
\]

Ask instead:

\[
\boxed{
\begin{aligned}
&\text{What classical multi-agent problem is actually present?}\\
&\text{What did the classical literature establish?}\\
&\text{Which assumption does an LLM violate?}\\
&\text{What observable consequence follows from that violation?}\\
&\text{What new theory, measurement, or mechanism is therefore required?}
\end{aligned}
}
\]

That framing dramatically raises the novelty bar—but it also exposes better research opportunities.

**The promising scientific frontier is not rediscovering delegation, coordination, voting, reputation, negotiation or institutions. It is developing a theory of those things for pretrained semantic agents for which capability, belief, commitment, identity and even rationality are endogenous and only partially observable.**

That is where classical MAS stops being historical background and becomes one of the most useful tools for deciding what modern multi-agent LLM research is actually new.
