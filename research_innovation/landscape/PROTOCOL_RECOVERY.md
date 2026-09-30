# Agent recovery protocols: closest prior art

Inspected 2026-09-30. Condensed primary-source notes; methodological implications are hypotheses, not novelty proofs.

## PlanFence

[Primary full text, v1](https://arxiv.org/html/2609.03340v1), 2026-09-03, §§3–6 and live-evaluation appendices.

Action-boundary validation binds plans to immutable public records, compares declared dependency frontiers with authoritative owner heads, and replans once or blocks. Tool wrappers supply complete action-relevant dependencies; private reasoning lies outside public lineage. The protocol does not guarantee atomic multi-owner validation or atomicity with the external action. Its 30 matched live five-agent workflows support a controlled stale-plan repair claim; replay studies support coordination-cost boundaries, not general task-accuracy gains. Fresh facts coexisting with stale plans, scoped validation, and isolated replanning are occupied contributions. A remaining issue is behavior influenced through undeclared context; simply adding a graph or a version gate does not solve it.

## From Faulty Memories to Corrected Actions

[Primary full text, v1](https://arxiv.org/html/2608.10502v1), 2026-08-11, §§3–5 and schemas/replay prompts.

Conditions on diagnosed faulty memories. A typed runtime graph covers memory, claims, plans, actions, observations, answers, and memory mutations. Reachability proposes affected state; independent trusted support can preserve candidates; deterministic repair deactivates unsupported state and selectively replays answer-relevant computation. Irreversible effects require resettable tools or compensations. The paper reports 150 controlled cases and a 50-case adapted LongMemEval-V2 stress test; clean traces and evaluation labels are withheld from repair. It expressly distinguishes its execution repair from MemoRepair's memory publication contract. Missing semantic edges and unreliable evidence remain important boundaries. Independent support plus selective replay is already an implemented agent mechanism.

## REVISE

[Primary full text, v1](https://arxiv.org/html/2609.00643v1), 2026-09-01, §3, §4, Appendix A.4/A.6.

Versioned workflow DAG attempts record data/control selectors. Recursive read-only proxies capture structured field access and collection membership, framework edges capture parents, and old/new diffs derive revision deltas. Recovery cancels, avoids, recomputes, continues, or reuses attempts; commit revalidation protects outputs/effects. Coarse and unknown provenance expands invalidation conservatively. This is stronger than relying solely on model-declared dependencies. Its main application results use live Qwen3-14B LangGraph/LLMCompiler workflows; challenging event orderings test latest-version correctness. Broad opaque prompt access can destroy useful selectivity even when runtime tracing is complete at the call boundary. The opportunity is the gap between influence exposure and semantic necessity, not invention of selective DAG recovery.

## AgentRewind

[Primary full text, v1](https://arxiv.org/html/2608.14380v1), August 2026, framework and experiments.

Aligned checkpoints restore agent context and workspace filesystem; agent-selected rewind memory carries experience from abandoned attempts. External network/service effects are not undone. MettleBench contains 82 engineering tasks with hidden ordered executable acceptance checks; feedback names the first unmet criterion. Results compare continue, restart-with-experience, safety review, and rewind, principally using GPT-5.4 and mini. Runs terminate on success or repeated failure, without fixed wall-time/token caps. Restoring a trajectory while retaining selected experience is prior art. Our correction problem instead requires the new source state to remain authoritative, and matched budget comparisons cannot directly inherit its success/cost conclusions.

## MemTX

[Primary full text, v2](https://arxiv.org/html/2607.23929v2), version accessed 2026-09-30, lifecycle/protocol and evaluation.

Treats writes as tentative records rather than immediate actionable beliefs. Snapshot transactions, evidence/permission/provenance metadata, staged admission, action gating, and typed cascade repair jointly address stale writes and downstream effects. Tests include bounded protocol enumeration and multiple model backbones. These establish properties of the specified state machine and controlled evaluation, not complete discovery of semantic influence in arbitrary language. Transactional staging, record maturity, provenance quarantine, and cascading repair are therefore occupied design space. Any proposed admission gate must explain what new evidence it obtains and why its acceptance decision is more reliable under missing dependencies.

Critical boundary in §3.5: the stronger action invariant requires **at least one** action-safe record in the snapshot, not proof that the action's actual inputs are safe. The live LLM evaluation uses weaker low/medium risk tiers. Cascade completeness covers recorded descendants and repair bookkeeping; external compensation is not replayed.

## MemoRepair

[Primary full text, v1](https://arxiv.org/html/2605.07242v1), 2026-05-08, §§2–5. HTML text downloaded through requests for uninterrupted method/results reading after web excerpts were truncated.

Withdraws an affected influence-provenance cascade before constructing successors from retained support and repaired predecessors. Artifact-specific operators recompute, regenerate, parametrically repair, or remove. Only validated predecessor-closed successors reenter service. Fixed value/cost terms yield a classical maximum-weight closure/min-cut selection problem. The paper explicitly disclaims inventing min-cut.

Missing-edge robustness is already tested: dropping 1% of influence edges produces 17.7% exposed affected artifacts. Schema-only and task-regression-only validators also fail. Therefore neither “missing dependencies matter” nor “withdraw then validate and republish” is new. Task effects use a diagnostic artifact-based score; cost excludes the withdrawal barrier. Validation coverage limits semantic correctness. These details matter when interpreting its zero stale-use and inexpensive-repair claims. A project improving safety under incomplete traces must provide something beyond repeating these ablations.
