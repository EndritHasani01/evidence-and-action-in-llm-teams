# Candidate comparison

Decision context: more than one month of implementation time; 30 aggregate allocated GPU-hours; no measured Qwen3.5/T4 throughput. Burdens are planning judgments, not measured estimates. See `ideas/CANDIDATE_GENERATION.md` for the initial alternatives and `DECISION_LOG.md` for changes of direction.

| Candidate | Useful capability / scientific question | Novelty and assumptions | Main failure mode | Experiments and burden | Verdict |
|---|---|---|---|---|---|
| Existing retention study | Separates delivery, source reuse and retained reasoning | Strong controlled study; reset/source preservation already studied | Generic context effect, capability floor, tiny tasks | Lowest implementation burden; existing 4,488/5,856-call designs remain unmeasured | Preserve as fallback and controls; insufficient as the sole ambition requested here |
| Dependency-guided selective repair | Recompute explicit affected work | REVISE, Faulty Memories, MemoRepair, build systems already establish principle | Missing semantic edges or overly broad exposure | Moderate adapter effort; no learned graph needed for a strong baseline | Required baseline, not invention |
| Checked artifact salvage | Reuse a historically affected artifact if it passes a current contract | Certifying algorithms, checked publication and agentic lakehouse are direct precedents | Checker solves task; weak checks confuse feasibility with optimality | Moderate effort; validators can be CPU-only, but hand engineering grows across domains | Strong alternative; use as a falsification baseline and contract lesson |
| **Reopen completion while preserving valid work** | Recover newly necessary search and coordination without discarding all useful results | Dynamic CSP, BDI reconsideration and control-aware recovery are predecessors; practical opaque-agent interface and causal evidence remain plausible contributions | Missing scope, perfunctory reclosure, stale prose, or equivalence to simple fresh planning | Small lifecycle plus query/coverage adapter; cheap CPU semantics, bounded live study | **Recommended research direction; implementation synthesis, not a claimed new foundational algorithm** |
| Prepare change-resilient work representations | Store reusable procedures, sufficient statistics or alternative frontiers | Incremental computation and Agentic Plan Caching already cover core reuse | Expensive preventive overhead; representation chosen with future-edit knowledge | Requires new prefix prompts/interfaces; difficult recovery/prevention causal separation | Defer; promising later if many revisions amortize overhead |
| Isolate reasoning compartments | Limit conservative taint across workers by narrower interfaces | Hermetic builds, IFC, APPA and ESC-CR precede it | Restricted interfaces reduce normal task quality; clean workers still reason wrongly | More intrusive prefix redesign; many interface ablations | Infrastructure option, not current scientific core |
| Optimize verification/recovery allocation | Spend finite checks where they matter most | Value of information, cache economics and MemoRepair selection are established | No calibrated risks/costs; optimizer exploits misspecified scores | High modeling burden; needs more data than 30 GPU-hours supports | Reject for this phase |
| Epoch/commit coordination | Prevent late obsolete attempts from committing | Distributed-system fencing and REVISE commit validation | New epoch attached to still-stale reasoning | Low CPU cost; clear conformance tests | Include as ordinary hygiene; not evidence of semantic recovery |
| Counterfactual execution replay | Remove target influence from reconstructible runtime | Execution-state unlearning is a direct predecessor | Expensive replay; stronger goal than ordinary correction requires | Runtime/cache restoration beyond present needs | Use to clarify claim boundaries, not implement as main method |

## Why the recommended direction wins this comparison

It identifies a failure that the present six-task design underemphasizes: a team can need new work even when its surviving positive work remains useful. This is relevant to research, coding, planning and procurement. It creates a falsifiable distinction between refreshing evidence, rechecking an old answer, and reopening the question that produced that answer.

The minimal implementation is small: a task's completion status has a validity lifetime separate from its artifacts. A revision can reopen that task without deleting its work. Uncertain scope triggers broader reconsideration. No confidence model, semantic graph extractor, new optimizer or learned verifier is required.

The strongest version may turn out to be coarse reopening. That is acceptable. A reliable result that broad task reconsideration outperforms expensive inferred dependencies would inform framework design; a result that ordinary fresh planning is just as good would argue against adding the mechanism.

## Two finalist challenges

**Why not artifact salvage?** It offers a clearer conditional safety argument, but most SILO validators are close to full solvers, and generic candidate validation already exists. The result risks measuring who received stronger external computation. It should inform artifact admission but not carry the claimed contribution.

**Why not just implement REVISE?** That is the correct reference wherever data/control dependencies are observable. If completion is explicitly represented as a node reading the objective and search domain, the proposed lifecycle can be implemented as a REVISE specialization. The research contribution would then be identifying the missing application-level state and showing its effects with imperfect observations—not inventing selective recomputation. A faithful adaptation that performs equally well is a positive engineering result and a negative algorithmic-novelty result.

## What would change the decision

Return to the controlled retention study if natural prefixes do not exhibit meaningful omitted-work failures, if generic reconsideration is equally effective and cheap, or if useful closure scopes require the answer oracle. Prefer a straightforward existing recovery system if ordinary automatic control instrumentation already supplies all needed state. Explore richer representations only after multiple-revision evidence shows enough amortized value to justify their construction.
