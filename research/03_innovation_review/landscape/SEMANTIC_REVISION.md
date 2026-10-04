# Semantic revision without perfect dependencies

Inspected 2026-09-30. Primary-source evidence and explicitly bounded interpretations.

## STALE

[Primary full text](https://arxiv.org/html/2605.06527v1), May 2026 identifier, introduction, task construction, probes, experiments.

Evaluates implicit conversational updates, including same-attribute changes and consequences across different attributes. Its 400 scenarios produce 1,200 questions across state resolution, premise resistance, and implicit policy adaptation. The latent-state formulation explains why retrieving old semantically similar facts misses indirect changes. Recognizing the new state and acting consistently with it are distinct capabilities. This is a benchmark and diagnostic framing, not a recovery runtime preserving expensive collaborative work. It occupies the claim that hidden semantic dependencies and stale downstream behavior have been overlooked entirely.

## StateAuditor

[Primary full text, v1](https://arxiv.org/html/2608.01619), 2026-08-03, §§4–7.

Combines draft-to-state premise auditing with the reverse state-to-draft check, explicitly targeting unstated dependencies. A transition proposer emits old/new values and timestamped quotations; deterministic code checks quotation grounding and chronology, **not semantic supersession**. Typed regeneration responds to stale/unknown verdicts. Official single-query STALE evaluation reports a five-point improvement over the locked predecessor; a matched evidence/call-budget control attributes this to transition handling. On HorizonBench most gain comes from ordinary draft auditing; a harder authored lifecycle set shows no gain. A trained Qwen3-4B auditor is explored. This is response-level recovery, not team-history isolation. Nevertheless, “audit changes against outputs rather than extract dependencies only from outputs” is directly occupied. Any adaptation must compare against this principle instead of claiming it anew.

## PACMI

[Primary SSRN abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7480138), written 2026-09-17, posted 2026-09-19. **Abstract-only access**: direct opening failed; indexed primary text available. No full-method validation yet.

Typed provenance links and a four-state validity lattice support downstream invalidation, historical retention, retrieval, and stale-premise checks. Reports 100 cases/300 queries across five domains. Its abstract distinguishes memory-state gains from final-answer gains: removing cascade propagation raises errors, but the paired answer difference does not reach significance. This is enough to defeat a broad novelty claim for validity lattices plus historical preservation; insufficient to assess realism of dependencies or detailed baselines.

## Implication for invention

Neither confidence labels nor a reverse audit is a fresh mechanism. A useful new project must target a capability these methods do not establish: controlled reuse of costly team-produced artifacts after shared context is no longer trustworthy, with imperfect semantic judges and measurable abstention/recomputation costs. Current evidence does not yet establish that such a capability is unoccupied.
