# Skeptical verdict on revision-sensitive completion

Review date: 2026-09-30. Candidate supplied during the investigation: every task starts pending; `done` records scope/predicate, objective/source-view versions, and a stopping reason; a relevant revision expires completion and reopens a current query while retaining admissible work; unknown scope escalates to the parent/root.

## Verdict

**A credible narrow systems interface and experimental question; currently not a novel recovery algorithm.** Treat this as explicit decision/coverage state that ordinary dependency recovery can operate on. Its potential value is making an often implicit recovery obligation observable and enforceable in peer-agent workflows, then establishing whether doing so improves outcomes under imperfect agent state. Do not claim a new consistency principle, general completeness proof, or advantage over correctly instrumented REVISE by construction.

The exact test against existing work is straightforward: encode each completion record as a workflow node reading the query predicate, objective version, and collection-membership version. A revision conflicts with those reads; the runtime invalidates that node and descendants while retaining independent facts. That is already within [REVISE's data/control/membership semantics](https://arxiv.org/html/2609.00643v1). A completion record could likewise be a derived artifact governed by [MemoRepair](https://arxiv.org/html/2605.07242v1). Calling the record an obligation does not change that reduction.

## What can still be contributed

1. **Empirical distinction:** recovery can fail through an obsolete stopping decision even when every reusable positive artifact is correct and no old factual value is repeated. This should be tested separately from ordinary stale-answer propagation.
2. **Minimal reusable interface:** task creation and current-version closure are tracked by the runtime, so a missing agent-authored dependency cannot silently imply completion. Unknown scope causes visible extra work. The protocol's guarantee is merely that an old completion token cannot authorize a current `done`.
3. **Measured design boundary:** determine when retaining positive work and reopening decision commitments beats retaining full context, fresh planning, and source-only reset after consequential changes. Quantify the price of conservative reopening and incomplete scope.
4. **Extension point:** integrate the interface into an existing validity runtime; the interface supplies better recovery units, while prior invalidation/replay machinery supplies execution semantics.

These contributions can support a useful paper without a first-ever algorithm claim. A null result is meaningful if it shows that a simple fresh planner or broad closure invalidation captures all benefits, or that agent-generated stop reasons are too unreliable to buy selectivity.

## Minimal rigorous experiment

Use a small retrieval-controlled task rather than only existing all-visible SILO arrays. Four peers have private candidate shards. A query chooses the highest-utility feasible candidate. Initial work gathers stable candidate facts and closes some search scopes. An authoritative threshold/objective change makes a previously excluded or unqueried candidate decisive; the prior choice remains feasible and its factual description remains true. This creates a **valid-positive-work / obsolete-completion** event. Pair it with answer-preserving threshold changes and no-change notices. Add a contrasting ordinary factual-replacement event.

Fork each prefix into: (a) retain plus clear correction; (b) source-only reset/fresh planner; (c) invalidate all completions, retain permitted artifacts; (d) scoped closure interface with unknown-scope escalation; and (e) complete data/control/membership instrumentation where possible. The last arm is a strong reference implementation, not an oracle gold-answer method. For compute, first run (a–c) on 12 pilot worlds; expand scope selection only if the three-arm contrast exposes a real tradeoff.

Independent evaluators compute exact optimum, current feasibility, and whether the improving region was searched. The runtime must never receive the optimum, affected-output set, relevant frontier, or gold scope. Log scope proposals before the edit; randomly omit or broaden them separately from naturally erroneous scopes. Count all post-revision reads, model tokens, reopening calls, invalid completions, remaining errors, and unnecessary reopened scopes. Pair by prefix, include unsuccessful prefixes, and stratify only secondarily on pre-change correctness.

## Failure cases to settle before adopting

- If scopes are few, reopen-all is probably cheaper and safer than scope reasoning. Prefer that outcome if observed.
- If rechecking the current objective requires reading the whole catalog, selectivity may have no economic value; report it.
- Correct positive facts can still anchor the new decision. Versioning completion does not isolate contaminated reasoning. Keep an explicit artifact admission/context policy and test stale-summary leakage.
- A new objective may require a new search universe, which no old scope describes. Root reopening must create fresh discovery work, not only rerun old queries.
- Finite catalog coverage is enforceable; open-web completeness is not. Generalize the interface and epistemic status, not a benchmark-specific completeness guarantee.
- If the current spec's tiny shards and all-visible source views are retained unchanged, “expensive work preserved” is weakly motivated. At least one retrieval-cost/coverage setting is necessary, with cost measured rather than invented.

## Recommended claim language

“We study recovery of completed collaborative searches after authoritative revision, separating the validity of accumulated evidence from the validity of stopping. A runtime completion interface makes this distinction explicit and enables controlled reopening without treating missing provenance as evidence of safety. We evaluate its benefits and costs against broad reopening, fresh planning, and established dependency recovery.”

Avoid: “We introduce the first mechanism that reopens stale conclusions,” “we solve incomplete provenance,” or “all reused work is semantically safe.”
