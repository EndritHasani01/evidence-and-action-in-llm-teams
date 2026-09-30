# Reopening search after change: promising distinction, strong novelty caution

Working analysis, 2026-09-30. This is a candidate assessment, not a verified novelty claim.

## The failure that artifact validity misses

A team researched three vendors, selected A, and stopped searching under a low budget. The budget increases. Every retained vendor fact remains true, every provenance link remains current, and A is still feasible. Nonetheless, the decision may be wrong because options excluded by the old budget have never been inspected. Similarly, deleting an edge can invalidate a shortest-path conclusion, while adding an edge can improve it without falsifying any old path witness. Recovery concerns both **whether retained work is true** and **whether the recovered task has adequate coverage**.

The first obligation can validate objects already present. The second may require creating work absent from the old trace. A clean validator supplied only old artifacts cannot establish the latter by verifying those artifacts independently.

## What close systems already cover

- [REVISE §3.2–3.3](https://arxiv.org/html/2609.00643v1): collection membership and control reads are first-class. If stopping/selection is explicit and its domain/objective is instrumented, the relevant route is already invalidated and replanned. Do **not** claim insertion or negative dependencies categorically defeat REVISE.
- [PlanFence §§3–4](https://arxiv.org/html/2609.03340v1): a complete action dependency contract can include the requirement, query domain, or selection decision. A change then triggers replanning. It does not implement a general search-completeness abstraction, but an adequate wrapper can encode the issue.
- [MemoRepair §2](https://arxiv.org/html/2605.07242v1): a rejection/closure decision can be represented as a durable artifact with influence parents. The contract then governs its repair. The missing feature cannot simply be another node type in its graph.
- [StateAuditor §4.3](https://arxiv.org/html/2608.01619): changed state can be checked against draft behavior even when the premise is unstated. A proposal saying “look at the new requirement and reconsider the answer” is insufficient differentiation.

## Narrow opportunity

Make **search closure** explicit at the runtime boundary: record a bounded question/scope, the basis for stopping, and the events under which the question must reopen. On revision, preserving facts should be independent from accepting the prior closure decision. Test whether cheap explicit closure obligations improve recovery when useful work was never performed and positive-artifact validation would pass.

Potential interface (illustrative): `close(question, scope, stop_reason, objective_version, support)` and `reopen(question, reason)`. Scope may be coarse; unknown scope must reopen. The difficult, research-worthy part is whether agents can produce useful closure records whose errors are detected or tolerated. A handwritten exact contract for every task reduces this to ordinary incremental query maintenance.

## Necessary comparisons and kill tests

1. Fresh requirement + retained evidence + generic replanning with the same model-call budget.
2. Full control/membership provenance where available; broad invalidation when unavailable.
3. Retain all positive work but clear prior selection/stopping decisions.
4. Explicit closure notes without a runtime mechanism, to test whether a prompt reminder suffices.
5. Unknown scope, omitted closure, changed objective, inserted options, and invalid but still feasible old decisions.

If a simple fresh planner recovers the same choices at equal cost, the obligation interface adds no demonstrated value. If the generator supplies a perfect search frontier or completeness test, claims must be bounded to that contract rather than general open-ended agents. If the mechanism's own certificate discovery costs as much as reopening everything, use it only as a characterization study.

## Search performed

Queries included LLM agent negative dependencies; memory recovery absence dependencies; agent search coverage; search completeness; optimality certificate recovery; replanning discarded options; decision invalidation alternatives. No verified primary 2025–2026 work implementing this exact *agent-generated closure obligation* interface was located in this pass. This is a search boundary, not evidence of firstness. Classical query maintenance, partial-order planning, search reuse, and kinetic certificates remain essential neighboring novelty checks in the broader investigation.
