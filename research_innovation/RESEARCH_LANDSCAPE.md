# Research landscape

Search and source inspection date: **30 September 2026**. Recent arXiv papers are treated as source-reported preprints, not independently replicated findings. Detailed access levels, sections and limitations are in the linked working notes. This is a targeted research search with adversarial novelty checks, not an exhaustive systematic review.

## Closest agent research

| Cluster | Established capability | Why it changes this project |
|---|---|---|
| [PlanFence](https://arxiv.org/html/2609.03340v1) | Validates action-relevant plan dependencies and replans/blocks | Fresh facts with stale plans and scoped action validation are already explicit. |
| [From Faulty Memories to Corrected Actions](https://arxiv.org/html/2608.10502v1) | Runtime provenance, independent-support preservation and selective answer/state repair | Support-preserving recovery cannot be the novelty claim. |
| [REVISE](https://arxiv.org/html/2609.00643v1) | Automatically observes structured data/control/membership reads; reuses or recomputes with commit checks | Strongest reference for ordinary workflow recovery. It already handles explicit negative/control structure. |
| [MemoRepair](https://arxiv.org/html/2605.07242v1) | Withdraws affected memory, builds validated successors and selects publication under cost | Quarantine, repair/republication and missing-edge sensitivity are already studied. |
| [MemTX](https://arxiv.org/html/2607.23929v2) | Transactional belief admission and cascading repair | Transaction metadata guarantees must be distinguished from action-input semantic sufficiency. |
| [AgentRewind](https://arxiv.org/html/2608.14380v1) and [Revisable by Design](https://arxiv.org/html/2604.23283v1) | Context/environment recovery and revision-aware rollback boundaries | Restore controlled computation without accidentally restoring obsolete truth; external effects need separate treatment. |
| [StateAuditor](https://arxiv.org/html/2608.01619v1), [STALE](https://arxiv.org/html/2605.06527v1) | Test adaptation to changed state, including unstated stale assumptions | Implicit dependence is not an untouched topic. Verification of citation/chronology is weaker than semantic adjudication. |
| [Reclaim Evaluation](https://arxiv.org/html/2606.25449v1) | Separates source retention from conclusion retention under correction | The existing source-preserving-reset study is a useful distributed generalization, not the first demonstration of this tradeoff. |
| [Execution-state unlearning](https://arxiv.org/html/2609.04875v1) | Counterfactual cleanup of reconstructible agent execution state | Removing all historical influence is a distinct, stronger goal than producing a valid current decision. |

Focused evidence: [protocol recovery](landscape/PROTOCOL_RECOVERY.md), [semantic revision](landscape/SEMANTIC_REVISION.md), [retention/execution](landscape/RETENTION_AND_REVISABLE_EXECUTION.md), [unlearning/reuse](landscape/REUSE_AND_UNLEARNING.md).

## Additional novelty threats outside the original specification

[ESC-CR](https://arxiv.org/html/2609.26072v1) performs clean-context regeneration after tainted inter-agent communication. [APPA](https://arxiv.org/html/2607.24625v1) isolates untrusted processing and controls returned derivatives. [Continuity Kernel](https://arxiv.org/html/2608.11632v1) separates candidate preparation from activation. [The agentic lakehouse](https://arxiv.org/html/2510.09567v1) uses isolated repair branches with owner-provided checks before merging. These occupy generic isolation/admission designs, though their goals and evidence differ from benign correction.

[MemContinuum](https://raw.githubusercontent.com/krakozavr/MemContinuum/main/docs/SCHEMA.md) already records rejected alternatives, assumptions and revisit conditions. [GA-Rollback](https://aclanthology.org/2025.emnlp-main.892.pdf) already revisits earlier agent actions and raises search-sufficiency issues. [Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788) makes uncertainty-aware rollback a poor broad novelty claim. Details: [isolation predecessors](evidence/ISOLATION_AND_CERTIFICATION_PREDECESSORS.md), [reopening exclusions](evidence/REOPENING_EXCLUSIONS.md), [uncertain localization](landscape/UNCERTAIN_LOCALIZATION.md).

The 2025 foundations also include [LongMemEval](https://arxiv.org/html/2410.10813v2), [Zep](https://arxiv.org/html/2501.13956v1), and [Agentic Plan Caching](https://proceedings.neurips.cc/paper_files/paper/2025/hash/9549f7d06700f0966d5f938f1d11022a-Abstract-Conference.html). Evolving memory, temporal updates and procedural reuse are established evaluation/design subjects. Their existence does not establish that arbitrary teams recover consumed work correctly. See [2025 notes](landscape/MEMORY_AND_PLAN_REUSE_2025.md).

## Adjacent fields: what can actually be borrowed

| Field / representative primary source | Useful principle | Assumption that must not disappear in translation |
|---|---|---|
| [Build systems](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf) | Rebuild only where necessary; distinguish dependency checks from result reuse | Complete tracked inputs or conservative treatment of untracked ones. |
| [DBSP](https://arxiv.org/html/2203.16684) and [Adapton](https://matthewhammer.org/adapton/) | Propagate changes using operator semantics and demand | Explicit computation semantics; not arbitrary textual explanations. |
| [Semantic caching](https://www.sigmod.org/publications/dblp/db/conf/vldb/DarFJST96.html) | Retain old query regions; execute a remainder query | The cache must describe what region it covers. |
| [Truth maintenance](https://dspace.mit.edu/handle/1721.1/5733) | Distinguish a proposition from its surviving justifications | Stored justifications must mean something logically; a citation alone is insufficient. |
| [Dynamic constraint maintenance](https://muller.unitime.org/lscs04.pdf) | Reinstate excluded possibilities when their elimination reasons fail | Explicit domains and explanations; unknown omitted options require broader search. |
| [Why-not provenance](https://arxiv.org/abs/1701.05699) | Explain absent outputs and failed derivations | Known query/domain semantics. |
| [Certifying algorithms](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf) | Check a result without trusting its construction | A sufficient checker for the required property; feasibility is weaker than optimality. |
| [Chubby](https://research.google.com/archive/chubby-osdi06.pdf) | Recipients reject stale generations | Prevents obsolete authority, not reasoning errors in a current generation. |
| [CALM](https://arxiv.org/html/1901.01930) | Identify where nonmonotone decisions require coordination | Formal monotonicity does not follow from agents agreeing. |
| [Sagas](https://www.cs.princeton.edu/research/techreps/598) | Compensate long-running effects rather than pretending to erase them | Compensation is domain-specific and can differ from inverse execution. |

Program-analysis/IFC work contributes conservative exposure and implicit-flow reasoning; versioning/OCC contributes snapshot validation; provenance contributes explanation structure. None recovers unobserved semantic dependencies for free. The full comparison, including Nectar, DryadInc, local certification and access limitations, is in [ADJACENT_FIELDS.md](landscape/ADJACENT_FIELDS.md). Additional primary readings of AGM, ATMS actions, dynamic slicing, Chandy–Lamport snapshots and LPA* are in [formal boundaries](landscape/BELIEF_SLICING_AND_SNAPSHOTS.md).

## Solved, partially solved, crowded and open

**Solved under explicit contracts:** tracking reads, invalidating dependent computations, version fencing, revisiting negative derivations, checking suitable witnesses, and preserving unaffected query results. These are mature principles, not guaranteed turnkey solutions for opaque agent reasoning.

**Partially solved in agents:** adaptation to updated memories, repair after diagnosed faulty evidence, conservative recovery under unknown provenance, isolated regeneration, and safe publication according to specified checks. Their guarantees are bounded by observed state, validator strength and effect models.

**Crowded contribution claims:** selective rollback; provenance-based invalidation; independent-support preservation; fresh-memory/stale-plan failure; source-only reset; artifact quarantine; versioned recovery; verify-before-use; storing rejected alternatives.

**Plausibly open enough for this project:** how to represent and refresh completion/search obligations when agent reasoning and scope notes are incomplete; whether doing so adds value over fresh planning or control-aware recovery; and when the metadata is unnecessary. This is narrower than claiming that existing systems cannot represent the problem. They can, if the relevant application state is exposed.

## Limits and unresolved evidence

PACMI's primary SSRN abstract was accessible, but its full method was not verified. The OpenReview “Repair Sets Before Repair Choices” source remained inaccessible through the tested forum/PDF/API routes. Do not inherit technical details from older notes about either. Public implementation schemas were inspected for MemContinuum; its runtime was not reproduced. All numerical paper results are external author reports.

The appropriate recommendation is consequently a **carefully attributed research synthesis with explicit novelty gates**, not a first-ever recovery claim. The final decision and kill conditions appear in [RECOMMENDED_INNOVATION.md](RECOMMENDED_INNOVATION.md).
