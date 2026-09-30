# Reopening discarded possibilities after change

Updated: 2026-09-30. Status: promising narrower research question, with substantial classical prior art. This is a candidate analysis, not a novelty certification.

## The asymmetry that matters

Suppose an agent team chooses supplier A after rejecting B because B's lead time exceeds a deadline. A remains available and every stored fact about A remains current. Then B's lead time improves. Revalidating the chosen artifact succeeds, yet the decision can be wrong under the revised objective. The stale object is the decision to stop considering B, not necessarily a positive statement inside A's plan.

In algorithmic terms, validity of retained witnesses establishes feasibility or soundness, not optimality or completeness. For an existential query a positive witness may suffice; a maximum, top-K, shortest path, uniqueness claim, or exhaustive report also requires exclusion of better/missing alternatives. Verifying only what the team kept misses the omitted branch.

This is an analytical observation, not a new theorem. To make it experimentally meaningful, construct corrections for which retained positive artifacts remain locally valid while the correct global selection changes. The reverse intervention (selected artifact becomes invalid) supplies an important matched contrast.

## Direct classical precedents

### Dynamic constraint satisfaction

[Iterative Forward Search: Combining Local Search with Maintaining Arc Consistency and a Conflict-based Statistics](https://muller.unitime.org/lscs04.pdf), Müller, Barták and Rudová, 2004. Inspected full PDF introduction and section 2.2, pp. 7-8.

When propagation removes a domain value, the algorithm stores an explanation. Removing an assignment requires reconsidering values whose explanations used it; they can either receive another exclusion explanation or return to the domain. This explicitly reinstates eliminated possibilities when their reasons cease to apply. It is directly analogous to revision-triggered reopening, and prohibits claiming that logging/revoking exclusion reasons is new.

### Incremental heuristic search

[Lifelong Planning A*](https://publications.ri.cmu.edu/lifelong-planning-a), Koenig, Likhachev and Furcy, 2004. Primary institutional abstract inspected. It reuses prior search-tree structure while edge costs and vertices change. D* Lite and LPA* are necessary related work for any claim about reopening search after revised costs. Detailed algorithm equivalence would require reading the full paper before implementation.

### Why-not provenance

[Efficiently Computing Provenance Graphs for Queries with Negation](https://arxiv.org/abs/1701.05699), Lee et al., 2017. Abstract inspected. Captures failed as well as successful derivations and answers focused why/why-not questions.

[Approximate Summaries for Why and Why-not Provenance](https://www.vldb.org/pvldb/vol13/p912-lee.pdf), Lee et al., 2020. Introduction and formalization excerpts inspected. Bounded summaries of missing-result explanations are also established, not a new memory compression idea.

**Transfer distinction:** these methods know the finite domain, query/operator semantics, or search expansion rules. An LLM may never enumerate an alternative, may hallucinate its elimination reason, and may omit the decision from the log. Their completeness does not transfer automatically.

## Closest recent agent threats

[REVISE](https://arxiv.org/html/2609.00643v1), sections 3.1-3.3 inspected. It tracks both data and control selectors, plus collection membership reads; structural revisions can invalidate routes and trigger recomputation of now-required workflow nodes. Therefore do not characterize REVISE as positive-data-only. A declared exclusion node could fit its model. The possible remaining dimension is whether opaque, internal search exclusions are externalized adequately and whether cheap conservative fallback repairs missing exclusions.

[From Faulty Memories to Corrected Actions](https://arxiv.org/html/2608.10502v1), sections 3.1-3.6 inspected. Its trace graph includes claim/plan/action nodes, independent-support preservation, and answer-relevant replay. A recorded rejection could be represented as a claim or plan. No dedicated omitted-alternative mechanism was found in inspected sections; keyword absence is not evidence the system cannot support it.

[PlanFence](https://arxiv.org/html/2609.03340v1), sections 3-4 and appendix A.3 inspected. It validates declared plan/action dependencies and allows a fresh replan. A correct complete dependency declaration can include exclusion facts; the potential failure is incomplete semantic scope, not absence of a version check.

A primary implementation lead is [MemContinuum](https://github.com/krakozavr/MemContinuum), discovered through an external catalog that describes `alternatives`, `rejected_because`, `revisit_if`, and assumptions. Primary README subsequently inspected: it explicitly stores declined alternatives and decisions, but warns hooks deliver context after the triggering edit and fail open. Schema and runtime code not yet audited; the automatic reopening claim is unestablished. Decision-log memory by itself would be too weak as a novelty claim. EvoCF (ICLR 2026 MALGAI workshop) is another search lead: counterfactual collaboration planning from memory, currently only abstract/excerpt inspected.

## Minimal research mechanism worth evaluating

A **bounded reconsideration ledger**, without a general semantic graph:

- Each completed decision may record a small set of excluded option scopes, the reason it was excluded, the source keys/constraints involved, and a continuation action capable of reopening that scope.
- Revisions invalidate matching exclusion reasons. Invalidating an exclusion schedules reconsideration; it does not assert that the excluded option is now correct.
- Missing, malformed, or low-coverage records trigger rescan of a declared coarse search scope. The runtime cannot identify omissions merely from the absence of a record; coverage must be part of the interface or experimentally controlled.
- Positive work that passes the existing retention rule remains available, but it is not a certificate that search is complete.
- A new candidate can compete with the retained incumbent only after its own current evidence is acquired. The ledger must not promote a stale rejected candidate into authority.

This is a translation of dynamic CSP and why-not reasoning, with a possible empirical systems contribution about imperfect LLM-produced search state. Keep the name descriptive; avoid presenting the ledger as an invented general algorithm.

## Why this might be stronger than generic salvage

The output can be entirely internally consistent and still wrong due to an option that is never reconsidered. That makes a clean causal failure distinct from obvious stale facts. It also creates an interpretable null: if a generic prompt to reconsider alternatives or a scope-level rescan matches the ledger, the simpler mechanism wins. The project then establishes that elaborate decision provenance adds no value in the measured regime.

## What could invalidate the direction

1. Recording exclusions solves the task for the model by supplying explicit top-K candidates or graph frontiers; gains come from representation help rather than recovery.
2. Recovery tasks are designed around only recorded alternatives, making coverage artificially perfect.
3. Fine-grained versioned control provenance in a strong REVISE-style baseline already handles all relevant cases.
4. A generic 'reconsider prior exclusions after this correction' prompt performs equally well at lower cost.
5. The corrected optimum requires an option never seen before; bounded retention provides no advantage and scope rescan is unavoidable.
6. Ledger creation, communication and checking consume more than they save under realistic change rates.
7. The runtime uses a solver to identify the newly relevant option. This would measure oracle routing, not agent recovery.

## Experiment that isolates the claim

Use at least two classes: (a) chosen-work invalidation and (b) newly viable/improved omitted alternatives with still-valid incumbent. Cross positive-only state versus explicit exclusions, holding total context/token allowance fixed. Compare retention, evidence reset, generic reconsideration prompt, affected-scope rescan, and ledger-triggered reconsideration. Use independent gold only for scoring. Deliberately drop or corrupt ledger entries at prespecified rates and measure whether fallback preserves recovery at a cost. Include no-change controls, unchanged-optimum corrections, and a case with an unseen newly relevant option. Report success, missed improvements, useless reopening, preserved useful work, and total pre- plus post-change cost.

SILO max/top-K provide small controlled examples, but the six existing task edits predominantly damage selected facts. Broaden change direction to improving previously nonselected records, and add one compact distributed selection/scheduling case if the central claim requires feasibility versus optimality. Do not retain six families merely for breadth if they do not discriminate the mechanism.

