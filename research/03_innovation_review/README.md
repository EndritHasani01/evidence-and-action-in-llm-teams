# Research innovation workspace

Investigation started 2026-09-30. This is a research record, not an implementation specification. `../PROJECT_SPECIFICATION.md` remains unchanged and authoritative for existing work.

**Recommendation: option 3 — reframe around recovery of completion/search decisions while preserving valid work.** A changed world can require previously omitted work even when surviving artifacts remain correct. The mechanism is a deliberately small, attributed systems synthesis; no first-ever algorithm or performance advantage is claimed.

Start with [CURRENT_THINKING.md](CURRENT_THINKING.md), then [RECOMMENDED_INNOVATION.md](RECOMMENDED_INNOVATION.md). Major changes and rejected novelty claims are preserved in [DECISION_LOG.md](DECISION_LOG.md).

Working areas: `landscape/` for focused source notes; `evidence/` for repository observations, executable CPU checks and claim traceability; `ideas/` for candidate generation; `risks/` for independent critique; `decisions/` for review resolutions. Root files hold the final synthesis and durable lessons. Empty categories were not created just to match a template.

Research constraints: preserve correction after substantial collaboration; inspect the full SILO checkout; investigate beyond LLM literature; do not run paid inference or change the specification during this phase. Available experimental resources are provisionally the specification's 30 aggregate allocated GPU-hours on two T4s, subject to measured feasibility.

The user clarified that implementation can take more than a month. This research phase did not use GPU/model inference. Full source/data inspection and cheap CPU checks were executed; paper results were not reproduced.

## Synthesis reading order

1. [REAL_WORLD_PROBLEM.md](REAL_WORLD_PROBLEM.md) — practical problem independent of SILO.
2. [RESEARCH_LANDSCAPE.md](RESEARCH_LANDSCAPE.md) — closest mechanisms, adjacent fields and access limits.
3. [OPEN_RESEARCH_GAPS.md](OPEN_RESEARCH_GAPS.md) — consequential opportunities and occupied claims.
4. [CANDIDATE_INNOVATIONS.md](CANDIDATE_INNOVATIONS.md) — nine different directions and their tradeoffs.
5. [RECOMMENDED_INNOVATION.md](RECOMMENDED_INNOVATION.md) — mechanism, boundaries and honest novelty positioning.
6. [FALSIFICATION_AND_RISKS.md](FALSIFICATION_AND_RISKS.md) — strongest objections and kill conditions.
7. [VALIDATION_STRATEGY.md](VALIDATION_STRATEGY.md) — causal controls, exact outcomes and complete call envelope.
8. [RESEARCH_REDIRECTION.md](RESEARCH_REDIRECTION.md) — what survives, changes and disappears.

## Evidence and continuation

- [Repository inspection](evidence/REPOSITORY_INSPECTION.md): complete source/task inventory, new runner hazards, all-case CPU results and limitations.
- [Executed counterexamples](evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md): valid support, feasible artifacts and adequate search are different properties.
- [Search/claim ledger](evidence/SEARCH_AND_CLAIM_LEDGER.md): routes from major conclusions to evidence.
- [Recent-agent source map](landscape/RECENT_AGENT_WORK.md), [adjacent fields](landscape/ADJACENT_FIELDS.md), and [classical formal boundaries](landscape/BELIEF_SLICING_AND_SNAPSHOTS.md).
- [Independent literature review](risks/LITERATURE_REVIEW.md), [mechanism review](risks/MECHANISM_REVIEW.md), [feasibility review](risks/FEASIBILITY_REVIEW.md), and [resolutions](decisions/REVIEW_RESOLUTIONS.md).
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) preserves insights that should not be lost during continuation.
- [Final workspace validation](evidence/WORKSPACE_VALIDATION.md) records file/link checks, budget arithmetic and specification preservation.

Reproduce CPU evidence with `python research/03_innovation_review/evidence/audit_repository.py` and `python research/03_innovation_review/evidence/recovery_counterexamples.py` from the project root. The audit documents its standard-library persistence shim and floating-point caveat; it is not a live benchmark run.

## Evidence discipline

- A paper's existence and inspected text must be verified before inheriting detailed claims from project notes.
- Dates, versions, access limitations, and the scope of inspected material belong in source notes.
- Absence from search is not evidence of novelty.
- Exact evaluators are measurement instruments, not information available to a recovery policy.
- No proposed performance advantage is an executed result.
