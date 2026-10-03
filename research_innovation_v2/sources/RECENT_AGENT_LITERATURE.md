# Recent agent literature: independent update

Inspection date: **4 October 2026**, using the client's date. This note records primary-source findings, not reproduced performance. The search is targeted and adversarial, not exhaustive. See [search log](search_log_recent.md) for queries, routes, date discrepancies and access failures. No source's absence from these results establishes novelty.

## The update changes the novelty assessment

The previous workspace correctly rejected generic selective rollback, fresh-state validation, support preservation and reopening as first inventions. Its latest-paper coverage was nevertheless incomplete. New papers and previously missed late-September work substantially crowd **causal recovery evaluation**, **communication correction/preservation**, **salvage under intent revision**, **obligation-aware memory admission**, and **versioned work reuse**. Neither an adaptive recovery router nor an obligation ledger is an easy novelty escape route.

The strongest remaining opening suggested by this literature review is an *identified boundary of recovery selectivity under opaque collaborative reasoning*: compare what the runtime can conservatively retain using actual exposure history with what is semantically affected and what helps recovery in the existing exact tasks. This is a hypothesis for the overall investigation, not a verified gap or selected recommendation. Any resulting contribution must distinguish a measured phenomenon from familiar transitive invalidation.

## New or previously missed close sources

### R1. Causal recovery evaluation / CIR

**When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents**, arXiv 2610.00372v1, **30 September 2026**. [Primary full text](https://arxiv.org/html/2610.00372v1); [submission history](https://arxiv.org/abs/2610.00372). Methods §§3–4 and experiments §5, including mechanism controls, inspected.

It branches identical ALFWorld states into recovery/no-recovery, separates rescue from harm, compares stale and clean observations, and fits three logistic models for a runtime router. Inputs are available before intervention; thresholds are selected using out-of-fold predictions. Refresh, content-ablated refresh and replanning distinguish new information from intervention effects. The environment is unchanged when observations are corrupted; this differs from the PS's formerly valid fact becoming false. The reported router advantage over a rate-matched anomaly policy has an interval crossing zero. No runtime was reproduced.

**Threat:** paired counterfactual evaluation, correction-specific interaction, rescue/harm decomposition and lightweight learned intervention selection already have a very close agent precedent. **PS opportunity:** distributed history, source-versus-derived-state retention, and exact coordinate-level change after an actual world edit remain different experimental objects. Those differences support a generalization; alone they do not establish a new principle. The primary page shows only v1: a third-party October-2 “updated” label is not a verified paper revision.

### R2. ICR communication audit

**Beyond Final Accuracy: Auditing Communication in LLM Multi-Agent Systems**, arXiv 2610.01042v1, **1 October 2026**. [Primary full text](https://arxiv.org/html/2610.01042v1). §§3–4 and implementation/scope appendices inspected; [code landing page](https://anonymous.4open.science/r/AgentICR-AA82/) opened but did not expose files through the web reader.

ICR freezes three independently generated trajectories and evaluates each directed sender/receiver pair. It compares no message, answer-only, full text and latent channels; no-message revision controls additional reasoning. Correctness-conditioned correction/preservation and question-cluster inference are explicit. Crucially, revised answers are never propagated: its stated scope is **single-hop revision without sequential feedback**. Initial agents share the same problem rather than private source shards; the gold task is static.

**Threat:** a new metric distinguishing communication's beneficial and harmful effects, or a full-reasoning versus answer-only ablation, is insufficient. **PS opportunity:** corrections arriving after several rounds of actual collaboration create inherited dependence and feedback absent from ICR. A narrowly controlled test of that history may add knowledge. Do not infer temporal contamination from a simple content-length comparison.

### R3. Commitment hierarchies and salvage

**Commitment Hierarchies under Intent Revision: A Belief-Revision Account of Salvage in Tool-Use Agents**, arXiv 2609.37453v1, **28 September 2026**. [Full text](https://arxiv.org/html/2609.37453v1); [metadata](https://arxiv.org/abs/2609.37453). Entire short paper read; metadata reports acceptance at PRIMA. Code release is promised, not verified available.

The framework labels cached nodes keep/patch/discard. Its locality impossibility uses indistinguishable node-local observations with different producer status. Structured achievability assumes sound provenance, correct revision classification and an exact minimum-cost replanner. Benchmarks are constructed with governing constraints; missing latent dependencies are expressly excluded, with broad dependence sacrificing optimality. A live comparison also separates retained environment state from retained full history.

**Threat:** generic safety-versus-maximal-reuse impossibility, commitment hierarchies, and classification followed by deterministic propagation are occupied. **PS opportunity:** empirically characterize how an unstructured team reaches the broad-dependence boundary without supplying exact producer semantics. Do not claim this elementary observation-model argument as a new theorem.

### R4. TRACE return-state admission

**TRACE: Governing Memory Validity in Evolving Multi-Agent Systems**, arXiv 2609.33517v1, **27 September 2026**. [Full text](https://arxiv.org/html/2609.33517v1); [code](https://github.com/xiong-wenjun/TRACE). §§2–3, evaluation design, limitations and Appendix C.3 inspected; repository tree inspected through GitHub API on October 4 (default branch `main`, last reported push October 1).

TRACE governs one agent's return after four teammates change shared state. It combines explicit lifecycle invalidation, model-based implicit checks, item admission and budgeted evidence coverage for open obligations. The task adapter supplies obligations and their evidence relations; coverage means supporting information is available, **not that the task is complete**. Missed dependencies and overly broad checks remain acknowledged failure modes. Its stronger implicit-update performance has substantial extra token cost. It is not a completion/search-reopening experiment.

**Threat:** preserving valid while rejecting stale state, context admission and obligation coverage already coexist in a recent multi-agent method. **PS opportunity:** all peers' recovery from one matched collaboration and identical evidence tables can isolate retention effects more simply. Do not compare against TRACE by withholding its observable metadata or granting the proposed method an equivalent advantage.

### R5. GitHarness

**GitHarness: Git Init Your Harness Working Memory for Perpetual User Requirements**, arXiv 2609.36789v1, **29 September 2026**. [Full text](https://arxiv.org/html/2609.36789v1). Formulation, §§4.1–4.3, evaluation setup and routing appendix inspected.

It couples requirement versions to branchable work states. A trained selector resolves requirements and chooses compatible history; downstream agents then reuse, patch or inspect restored work. Its verifier-preserving benchmark spans multiple tasks and distinguishes requirement transitions from final correctness. The selector is trained with black-box reinforcement learning; training and broad harness reproduction do not fit this project's resource envelope.

**Threat:** Git-style branching, versioned working memory and requirement-driven selective restoration are established agent designs. **PS opportunity:** avoid competing on orchestration scale; use exact, transparent intervention semantics to test which runtime information is useful under a fixed small-model budget. GitHarness's explicit requirement-resolution problem is distinct from the PS's already diagnosed source edit.

### R6. Retire serving system

**Serving a Revisable World: Versioned Execution for Interruptible Agents**, arXiv 2610.01160v1, **1 October 2026**. [Full text](https://arxiv.org/html/2610.01160v1); [metadata](https://arxiv.org/abs/2610.01160). Scope, transition semantics, lifecycle guarantees and evaluation inspected.

Retire revokes publication authority while retaining a certified compatible KV prefix, separating successor progress from old-resource reclamation. The runtime chooses the revised context; serving enforces that choice. It implements this division in vLLM, including distributed execution. Its guarantees concern output authority and valid cache inheritance, not whether an opaque old argument remains semantically useful.

**Threat:** epoch fencing plus selective inheritance is a direct systems precedent, newly published after the earlier search. **PS opportunity:** study the runtime's semantic retention decision while preserving the existing fresh-per-call model state; implementing this serving stack would not answer that question.

### R7. Explicit beliefs / PoS

**Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States**, arXiv 2610.01415v1, **1 October 2026**. [Full text](https://arxiv.org/html/2610.01415v1). §3 and recovery appendix inspected.

PoS maintains structured world beliefs, objectives, epistemic gaps and achievement gaps. A sentinel checks belief updates; persistence, stagnation and recurrence signals trigger factorized recovery constraints, with a generic fallback. Its semantics depend on model judgments about beliefs and task progress.

**Threat:** explicit unresolved-work state, disagreement/uncertainty signals and stagnation-triggered adaptive recovery are crowded. **PS opportunity:** deterministic observed exposure or known version delivery can be tested without training or additional semantic judges; this advantage is causal clarity, not proof of superior accuracy.

### R8. VeriHarness

**VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks**, arXiv 2610.00972v1, **1 October 2026**. [Full text](https://arxiv.org/html/2610.00972v1). Method overview and consensus/disagreement procedure inspected.

An evidence-backed verifier resolves disagreement and challenges consensus, including omitted requirements. It uses the generator's base model and environment rather than hidden test answers. Its multi-rollout frontier-model evaluation is far outside the project's budget.

**Threat:** adding an agreement detector, consensus challenger, or omitted-requirement reviewer does not offer a fresh principle. **PS opportunity:** an exact benchmark can measure how agreement relates to stale influence without introducing another model or interpreting agreement as correctness.

## Rechecked older predecessors and version corrections

### R9. RIAG dynamic task routing (late follow-up)

**Revision-Aware Independent Agent Graphs for Dynamic Reasoning**, arXiv 2610.01249v1, **1 October 2026**. [Full text](https://arxiv.org/html/2610.01249v1); [metadata](https://arxiv.org/abs/2610.01249). §§3–4, experiment controls and public query semantics inspected after a lead from the main investigation.

RIAG resolves versioned task bindings, caches exact document/configuration matches and records invocation exposure ancestry. Its six-benchmark collection uses three **fixed-content** task documents per episode: events alter which document is in force, not the mathematical input inside a document. Historical queries test effective-time versus arrival-time binding. A different immutable document version forces recomputation. Initial solver/checker calls are unexposed; later audit/repair outputs are not independent votes.

**Threat:** temporal routing, historical-state reconstruction, version-keyed reuse and explicit exposure graphs are already combined. **Boundary:** this is not recovery of distributed computation after an input record changes. The relevant contribution cannot be merely introducing an ancestry graph or distinguishing current from historical state. Its public semantics and exact provenance are useful design references, but its large aggregate routing gains are not evidence about B/C reasoning retention.

| Source and current access | Verified principle / implication |
|---|---|
| [REVISE 2609.00643v1](https://arxiv.org/html/2609.00643v1), September 1; primary history still v1; §§3–4 inspected | Recursive proxies observe structured data/control/membership reads; unknown/coarse reads expand recovery. Correctly encoding completion as a control node is already supported. A chronological descendant filter is an instance of its principle, not a new recovery algorithm. Opaque prompt-wide reads are precisely where useful selectivity can disappear. |
| [PlanFence 2609.03340v2](https://arxiv.org/html/2609.03340v2), latest primary history September 27; contract and extended comparisons inspected | The prior workspace used v1. Current version explicitly discusses conservative declaration of every supplied record, S-Bus session read evidence and native-validator controls. Recorded derivation currency is separate from semantic correctness; declaring all inputs is safe for the stated version contract but may cause excess replans/blocks. |
| [Reclaim 2606.25449v5](https://arxiv.org/html/2606.25449v5), latest primary history July 21 | Prior workspace inspected v1, even though later versions existed. Latest full HTML is accessible. Source-versus-conclusion retention and matched-budget/padding controls remain close precedents. Do not cite v1 as the latest paper or imply evidence-preserving reset is newly invented here. |
| [APPA 2607.24625v2](https://arxiv.org/html/2607.24625v2), primary history August 26; recovery and evaluation passages inspected | Context branching, policy-backed admission and recoverable information-flow control already address the utility cost of broad taint. Security labels differ from correction truth, but changing the vocabulary does not create a new isolation method. |
| [ESC-CR 2609.26072](https://arxiv.org/html/2609.26072), method inspected; date discrepancy in search log | Ambiguous attribution includes all visible untrusted messages; recorded descendants are tainted; an allowlisted recovery context excludes everything else. Verified claims preserve useful content. Direct precedent for clean-context recovery under uncertain provenance; security release checks are stronger domain-specific assumptions than the PS permits. |
| [NeuroTaint 2604.23374v1](https://arxiv.org/html/2604.23374v1), April 25; execution model/design inspected | Context provenance, semantic transformation, persistent lineage and counterfactual sink analysis are explicit. Exposure reachability and actual influence must be distinguished; graph terminology alone cannot establish that distinction as new. Its offline semantic/causal auditor is not a cheap exact runtime oracle. |
| [Trace-Level Analysis 2604.27586](https://arxiv.org/html/2604.27586), April 30; framework and outcome scope inspected | Controlled artifact perturbations and paired traces show that structural divergence and answer correctness can separate. A new project cannot claim that logs and correctness differ as an original insight; it can characterize a specific operational consequence for correction recovery. |
| [Reliability–Contagion Feasibility 2607.21912](https://arxiv.org/html/2607.21912), July 24; model assumptions and experimental design inspected | Correction-aware network propagation and connectivity/reliability tradeoffs are modeled explicitly. Per-edge exposure versus fixed sender budget changes the theoretical conclusion. Four-peer unrestricted routing cannot support a new density law; temporal exposure structure must be separated from graph density and message volume. |

## Boundaries that survive the search, subject to experiment

1. **A runtime can know exposure without knowing semantic dependence.** The question is whether this observable structure provides practically useful recovery selectivity, not whether transitive closure is new.
2. **A small mathematical edit can have a large historical exposure cone.** Conversely, a globally changed answer may follow little collaboration. The PS's six tasks can separate these quantities descriptively; causal claims require an intervention that does not alter information access or task difficulty.
3. **History after useful collaboration is different from independent answers followed by one message.** ICR supplies the closest content-control design, but explicitly removes feedback. A PS extension should exploit that distinction rather than repeat its one-hop experiment.
4. **Outcome preservation is not historical independence.** Exact unchanged coordinates supply an offline semantic target; they cannot be passed to a runtime filter as if they were observable provenance.
5. **A selective policy can fail by becoming total reset.** This degeneration can be measured deterministically before inference. If nearly every retained artifact lies in the conservative cone, an extra recovery arm may be scientifically unnecessary; that is a boundary finding, not proof that reuse is harmful.

These are project-specific deductions from source assumptions and the PS, not claims that no one has studied them. A completed thesis could teach the field when complete runtime observation is still too coarse for useful semantic recovery; it cannot promise that the answer is favorable before measuring the traces.

## Follow-up: a more focused information-contract candidate

The main investigation identified a potentially more decisive PS-preserving intervention: vary whether the authoritative correction includes the historical before-value as well as the current after-value. See [transition receipt novelty review](TRANSITION_RECEIPT_NOVELTY.md). This emerged after the initial source synthesis above; exposure selectivity is no longer presumed the strongest extension. The receipt is not a new recovery algorithm. Its possible contribution is identifying whether the measured value of retaining reasoning depends on the information contained in the revision interface.

## Read coverage

Read `PROJECT_SPECIFICATION.md`; all eleven files under `research_innovation/landscape/`; `RESEARCH_LANDSCAPE.md`, `RESEARCH_REDIRECTION.md`, `RECOMMENDED_INNOVATION.md`, `evidence/SEARCH_AND_CLAIM_LEDGER.md`; and additionally `VALIDATION_STRATEGY.md`, `FALSIFICATION_AND_RISKS.md`, and `evidence/REOPENING_EXCLUSIONS.md`. These are the prior exploration's evidence and recommendations, not governing instructions. The original files were not edited.
