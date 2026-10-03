# Strengthening recovery after distributed LLM work

Research phase completed **2026-10-04**. Governing foundation: [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md), unchanged. The [previous investigation](../research_innovation/README.md) remains intact and is evidence, including its rejected ideas and completion-reopening recommendation.

**Recommendation:** retain the six-task correction-and-recovery study. Test whether an authenticated historical before-value changes the benefit of retaining collaborative history, using BΔ/CΔ on existing Prefix Sum/Sort worlds only, subject to the original compute ceiling. Pair this with exact analysis of information retained outputs preserve or lose. This is an empirical/interface contribution, not a new delta algorithm.

Start with [RECOMMENDED_EXTENSION.md](RECOMMENDED_EXTENSION.md). For continuation, read [CURRENT_THINKING.md](CURRENT_THINKING.md), [DECISION_LOG.md](DECISION_LOG.md), and [LESSONS_LEARNED.md](LESSONS_LEARNED.md).

## Synthesis map

| Artifact | Purpose |
|---|---|
| [FOUNDATION_ASSESSMENT.md](FOUNDATION_ASSESSMENT.md) | Why the PS is strong and what must be preserved |
| [UPDATED_RESEARCH_LANDSCAPE.md](UPDATED_RESEARCH_LANDSCAPE.md) | Primary-source map, dates, assumptions and remaining gaps |
| [UNTAPPED_STRUCTURE.md](UNTAPPED_STRUCTURE.md) | Latent scientific structure in protocol, tasks and traces |
| [CANDIDATE_ADDITIONS.md](CANDIDATE_ADDITIONS.md) | Eleven distinct candidates, costs, reductions and rejection reasons |
| [CROSS_FIELD_INVENTIONS.md](CROSS_FIELD_INVENTIONS.md) | Transfers from incremental computation, systems, control and decision theory |
| [NOVELTY_ADVERSARY.md](NOVELTY_ADVERSARY.md) | Hostile reductions and strongest counterarguments |
| [FINALIST_EXPERIMENTS.md](FINALIST_EXPERIMENTS.md) | Smallest discriminating experiments and exact estimands |
| [FEASIBILITY_AND_VALUE.md](FEASIBILITY_AND_VALUE.md) | Call arithmetic, uncertainty, effort and prioritization |
| [RECOMMENDED_EXTENSION.md](RECOMMENDED_EXTENSION.md) | Final answer and bounded novelty claim |
| [FALSIFICATION_PLAN.md](FALSIFICATION_PLAN.md) | Conditions for abandoning, narrowing or rejecting the addition |
| [SPECIFICATION_CHANGE_PLAN.md](SPECIFICATION_CHANGE_PLAN.md) | Eventual scientific edits, with no implementation code |

## Evidence and reviews

- [Protocol audit](evidence/PROTOCOL_AUDIT.md), [previous-workspace coverage](evidence/READ_COVERAGE.md), [validation](evidence/WORKSPACE_VALIDATION.md).
- [CPU probe](evidence/protocol_probe.py) and [results](evidence/protocol_probe_results.json): identities, ambiguity, full scripted B-state witnesses and exposure examples.
- [Budget arithmetic](evidence/budget_and_precision.py) and [results](evidence/budget_and_precision_results.json).
- [Recent papers](sources/RECENT_AGENT_LITERATURE.md), [receipt novelty](sources/TRANSITION_RECEIPT_NOVELTY.md), [cross-field sources](sources/CROSS_FIELD_SOURCES.md), [recent search ledger](sources/search_log_recent.md), [root ledger](sources/ROOT_SEARCH_LEDGER.md).
- [Completion competitor](reviews/COMPLETION_COMPETITOR.md), [structural candidates](reviews/STRUCTURE_CANDIDATES.md), [cross-field critique](reviews/CROSS_FIELD_CANDIDATES.md), [closed final design review](reviews/FINAL_DESIGN_REVIEW.md).

Reproduce new CPU analyses from the repository root with `python research_innovation_v2/evidence/protocol_probe.py` and `python research_innovation_v2/evidence/budget_and_precision.py`.

**Evidence boundary:** no model inference, production recovery implementation, empirical treatment effect, measured power or GPU throughput. Scripts are research probes. Existing audit results are distinguished from newly executed checks. Before-images, incremental updating and causal evaluation have strong predecessors; the proposed originality is a narrowly measured relationship, conditional on future results.

Extended main totals would be 6,368/4,872 calls. If unaffordable, preserve the original complete 48/36-world study and use mathematical/trace analyses. No specification revision or implementation occurs in this research phase.
