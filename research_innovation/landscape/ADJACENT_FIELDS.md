# Adjacent-field investigation: recovery as controlled reuse

Updated: 2026-09-30. Status: completed first-pass adjacent-field investigation; final synthesis and candidate critique follow the chronological early notes. This file is owned by the adjacent-fields investigator. The project specification is read-only.

## Early finding

The central engineering tension is not how to draw a dependency graph. It is how to permit useful old work to influence new decisions when the runtime cannot observe all the semantic dependencies that produced that work. Existing systems have strong solutions under explicit computation semantics; their guarantees do not automatically carry across opaque LLM reasoning.

Three different avenues merit testing before choosing one:

1. **Reuse by current validity:** old artifacts are proposals whose acceptance depends on a current-world contract, not on trusting their recorded derivation. Certifying algorithms, proof-carrying code, and local certification are direct predecessors. Potential research question: can inexpensive, incomplete checks yield a useful risk/cost tradeoff when provenance is incomplete? Exact algorithmic checking is a diagnostic ceiling, not general LLM correctness.
2. **Separate influence from authority:** place pre-change reasoning in an archive outside active context, admit only bounded artifact proposals into fresh recovery contexts, and reject pre-change in-flight results at the recipient. Epoch fencing is established; a timestamp alone cannot remove semantic contamination from a newly generated answer. Potential research question: what minimal isolation/admission rule prevents stale reasoning from laundering itself into fresh work while preserving value?
3. **Prepare work for future revision:** retain composable summaries, alternatives, or executable procedures rather than only final conclusions, so revisions operate on a stable representation. This is directly related to incremental computation and sufficient statistics; it is not novel merely because an LLM produced the representation. Potential research question: when is modest pre-change redundancy worth its amortized recovery cost?

These are preliminary hypotheses, not recommendations. Each requires direct predecessor checks and a practical experiment that does not smuggle the gold solver into the runtime.

## Sources already located and inspected

| Source | Date | Inspection | Established principle | Transfer boundary |
|---|---:|---|---|---|
| [Build systems a la carte](https://simon.peytonjones.org/build-systems-a-la-carte/) | 2018; journal extension 2020 | Author landing page and search excerpts; full paper subsequently inspected; see final matrix | Schedulers versus rebuilders; verifying and constructive traces; early cutoff | Requires a specified task evaluation model and tracked inputs; textual dependencies are not complete semantic read sets |
| [Chubby](https://research.google.com/archive/chubby-osdi06.pdf) | 2006 | PDF introduction and sections 2.3-2.4 | Recipient-side generation checks prevent delayed stale actors from affecting protected resources | A fresh generation proves authorization, not correctness or absence of old-fact influence |
| [Keeping CALM](https://arxiv.org/html/1901.01930) | 2019/2020 | Full HTML obtained; sections 1-3 and 4.3 subsequently inspected | Coordination-free consistency tied to logical monotonicity | Revisions/deletions are nonmonotone; convergence does not establish semantic correctness of LLM claims |
| [DBSP](https://arxiv.org/html/2203.16684) | VLDB 2023 | Full HTML obtained; abstract and technical scope inspected | Incremental view maintenance for rich query languages, including nonmonotonic recursion | Formal operators give delta semantics; no comparable automatic derivative for opaque generation |
| [Certifying Algorithms](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf) | 2011 | Author PDF located; publisher abstract/introduction read | Outputs plus independently checkable witnesses; checker need not trust producer | Strong checks must correspond to actual task validity; easy checking is not universal |
| [Introduction to local certification](https://arxiv.org/abs/1910.12747) | 2019/2021 | Abstract | Distributed local certificates can establish global configuration predicates | Labels/checkers are problem-specific; local acceptance may require global all-nodes success |
| [Complexity Landscape for Local Certification](https://drops.dagstuhl.de/storage/00lipics/lipics-vol356-disc2025/html/LIPIcs.DISC.2025.18/LIPIcs.DISC.2025.18.html) | DISC 2025 | Abstract/introduction excerpt | Active 2025 work on local proof-label complexity | The model abstracts certificate construction into an oracle; cannot inherit its algorithmic feasibility for LLMs |

## Important distinctions to preserve

- **Current** is not **correct**: version metadata validates which source snapshot was intended, not whether the output follows from it.
- **Unaffected answer** is not **unaffected derivation**: old proof/support may fail even if the same answer can be reproved.
- **Dependency completeness** is an assumption, not a property conferred by logging citations.
- **Old work reused as a hypothesis** differs from old work treated as authority. The former can still anchor an LLM and must be tested.
- **Safe to compute** differs from **safe to publish/act**: expensive speculative work can continue if its outputs are prevented from committing before validation.
- A single global epoch is simple and safe for fencing old processes, but can discard useful work unnecessarily; fine-grained epochs require trustworthy scope.

## Next checks

Read full build-system sections on nondeterminism and early cutoff; truth maintenance and belief revision; sagas and optimistic concurrency; dynamic slicing and implicit flow; recent LLM verification/recovery predecessors; derive an explicit impossibility boundary from indistinguishable recorded state rather than overclaiming a new theorem.

## Update: direct agent predecessors substantially narrow novelty

The first two candidate avenues are already represented directly in agent systems, beyond their classical predecessors. See [focused notes](../evidence/ISOLATION_AND_CERTIFICATION_PREDECESSORS.md): Continuity Kernel (2026), proof-carrying agentic lakehouse (2025), ESC-CR (September 2026), APPA (July 2026), Fides (2025), and NeuroTaint (2026). This shifts the plausible contribution toward measuring and controlling the gap between recorded version/authority and actual stale influence, especially after formerly valid information changes. Generic clean-room recovery, quarantine, or verify-then-publish is not an adequate novelty claim.

## Final adjacent-field synthesis

### What is already solved under explicit semantics

| Field / primary source | Inspected depth | Established capability | Boundary for this project |
|---|---|---|---|
| [Build systems a la carte](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf), 2018 | Sections 4.2, 6.3-6.5; PDF text | Verification/constructive traces, early cutoff, handling untracked inputs conservatively, self-tracking task definitions; discusses nondeterministic inconsistent builds | Stochastic LLM generation is not itself the unsolved issue: build theory already models nondeterminism. The difficult gap is missing semantic observations and a meaningful correctness predicate |
| [DBSP](https://arxiv.org/html/2203.16684), 2023 | Abstract and operator/model scope | General incrementalization within a formal stream algebra | A delta rule cannot be inferred soundly from arbitrary free-form reasoning just by changing an input version |
| [Adapton](https://matthewhammer.org/adapton/), 2014 | Author abstract and artifact summary | Recompute only demanded results; reuse across changing contexts | 'Repair only what is needed now' is established. Useful translation: do not eagerly repair abandoned subgoals |
| [Nectar](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/10/nectar-final.pdf), 2010 | Abstract/introduction and dependency-analysis excerpts | Shared subcomputation reuse, primary/derived separation, regeneration from stored programs | Preserving procedures or recipes instead of all outputs is old. Correct declarative I/O makes the guarantee possible |
| [DryadInc](https://www.usenix.org/event/hotcloud09/tech/full_papers/popa.pdf), 2009 | Introduction | Identical-computation reuse and append/merge incrementality | Nontrivial savings need structured workload assumptions; generic reuse is not an algorithm |
| [Semantic Data Caching and Replacement](https://www.sigmod.org/publications/dblp/db/conf/vldb/DarFJST96.html), 1996 | Publisher-hosted abstract | Semantic cache regions plus remainder queries | A partial old answer can reduce new work only if coverage and the missing remainder can be specified |
| [Chubby](https://research.google.com/archive/chubby-osdi06.pdf), 2006 | Sections 2.3-2.4 | Recipient-enforced generation checks reject delayed stale requests | Essential runtime hygiene for in-flight work; cannot establish that a current result is free of stale reasoning |
| [Sagas](https://www.cs.princeton.edu/research/techreps/598), 1987 | Institutional abstract; scan PDF obtained but text unavailable | Long-lived transactions composed from transactions with compensations | Revision cannot undo already sent messages or physical actions; compensation is domain-specific, not a hidden reset |
| [Optimistic concurrency control](https://db.cs.cmu.edu/publications/), 1981 Kung/Robinson entry | Primary bibliographic record/abstract; direct PDF route failed | Nonlocking execution validated against conflicting transactions | A read-set validation rule is only as good as the read set and intended isolation property |
| [A Truth Maintenance System](https://dspace.mit.edu/handle/1721.1/5733), 1979 | Primary metadata/abstract; companion classical explanatory material | Maintains support and retracts unsupported beliefs | Storing support and preserving alternate support are established; free-form support extraction is a different empirical problem |
| [Certifying algorithms](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf), 2011 | Abstract/introduction and witness formulation | Trust a small checker instead of the complex producer | Exact checking can validate old outputs without trusting history, but some tasks lack a cheap complete checker |
| [Local certification](https://arxiv.org/pdf/1910.12747), 2019/2021; [2025 complexity study](https://drops.dagstuhl.de/storage/00lipics/lipics-vol356-disc2025/html/LIPIcs.DISC.2025.18/LIPIcs.DISC.2025.18.html) | Introductory definitions; 2025 abstract/introduction | Local labels collectively establish global predicates | Certificate size, communication, producer cost and unobserved nodes matter; a local pass alone need not establish a global property |
| [CALM](https://arxiv.org/html/1901.01930), 2019/2020 | Sections 1-3 and 4.3 | Separates monotone accumulation from operations needing coordination; distinguishes confluence from freshness | Corrections are not merely new monotone facts. Move coordination to publication when possible, but do not infer arbitrary LLM consistency from CALM |
| [Dynamic CSP explanation maintenance](https://muller.unitime.org/lscs04.pdf), 2004 | Section 2.2 | Reinstates excluded candidates when their elimination explanations no longer hold | This supplies the most promising translation: revising search closure rather than only materialized artifacts |
| [Why-not provenance](https://arxiv.org/abs/1701.05699), 2017; [approximate summaries](https://www.vldb.org/pvldb/vol13/p912-lee.pdf), 2020 | Abstracts and 2020 definition/introduction excerpts | Represents failed derivations and bounded summaries of missing answers | Negative dependencies and compressed exclusion explanations are not new, but opaque incomplete LLM search creates a distinct reliability question |

No source-reported performance figure is needed to select the conceptual direction. The entries above establish mechanisms and assumptions, not evidence that they beat LLM recovery baselines.

### A useful information boundary (our reasoning, not a new claimed theorem)

Let a runtime observe a transcript/log L and correction delta. Suppose two hidden histories have the same L and delta, but an unrecorded source exposure influenced a retained artifact in one and not the other. Any policy based only on L and delta must choose the same reuse action for both. It therefore cannot guarantee both perfect stale-influence exclusion and maximal reuse across these histories. It needs additional observation, a sufficient current validity check, a conservative invalidation rule, or an explicit residual-risk allowance.

This statement concerns the chosen observation model. It does not prove recovery is impossible: a fresh solver can recompute, and an independent validator can sometimes establish an old output's current validity. Nor does runtime exposure imply actual causal dependence; using it as taint intentionally trades precision for coverage.

A parallel boundary applies to omitted search: if a decision ledger covers only some exclusions, absence of a trigger is not proof no excluded option became relevant. Coverage certificates or scope rescans must carry the missing obligation. Confidence scores alone add no missing observation.

### Candidate comparison after novelty checks

| Direction | Independent value | Main novelty threat | Feasible core experiment | Verdict |
|---|---|---|---|---|
| Current-world salvage with an independent checker | Reuse an old artifact despite incomplete/contaminated history | Certifying algorithms, MemoRepair independent support, lakehouse verify-then-merge, ESC-CR evidence reconstruction | Same candidate artifacts; imperfect provenance; current validator versus graph rules; matched verification cost | Useful baseline or empirical synthesis. Generic mechanism novelty weak |
| Isolated archive with bounded admission and recipient fencing | Prevent old state/late work from silently regaining authority | CK, APPA, Fides, ESC-CR, Chubby | Inject late stale results and alias/summary reentry under clean/noisy context conditions | Necessary system discipline. Too crowded as central algorithm claim |
| Revision-ready representations (procedures, sufficient summaries, alternatives) | Amortize recovery over future changes | Incremental computation, Nectar, semantic caching | Charge prefix preparation; sweep change frequency/locality; compare summary forms | Potentially useful but broad and easy to confound with algorithm tutoring |
| Reopen search decisions whose exclusions lost support | Correct decisions that remain feasible but are no longer optimal/complete | Dynamic CSP, why-not provenance, REVISE control dependencies, decision-memory stores | Positive-validity-preserving corrections; bounded exclusion records; incomplete logging; coarse rescan and generic prompt controls | Strongest narrower research question found, conditional on native agent coverage and a simple fallback |

### Recommendation from the adjacent-fields review

Prefer a **recovery-completeness study centered on reopening excluded work** over introducing another generic rollback/admission system, provided an early pilot confirms that the agents naturally make relevant exclusions and that logging them does not simply solve the task. Present the mechanism as a lightweight adaptation of classical explanation maintenance with explicit coverage/fallback semantics. The defensible novelty would be an empirical characterization and operational interface for opaque collaborative search, not discovery of negative dependencies.

If the exclusion pilot fails, the honest fallback is a rigorous empirical study of conservative current-world salvage under incomplete provenance, with no first-ever algorithm claim. A clean causal null about when simple reset or scoped rescan suffices is stronger than an elaborate renamed classical mechanism.

Detailed candidate, predecessors, example, falsifiers and experimental sketch: [Reopening exclusions](../evidence/REOPENING_EXCLUSIONS.md). Recent isolation predecessors: [Isolation and certification](../evidence/ISOLATION_AND_CERTIFICATION_PREDECESSORS.md).

### Scope cautions for the final project

- Do not freeze the world merely because synchronous SILO makes that convenient. At least CPU protocol tests should include a second revision and late old-epoch arrivals.
- Do not claim deployment generality from max/top-K alone. Add one small tool-mediated selection/planning transfer case with feasible incumbents and reopened alternatives.
- Model evidence defects as well as provenance defects: missing observations, an omitted candidate, a wrong exclusion reason, partial source coverage, and a valid old result with a broken old justification are different conditions.
- Output correctness, freshness, authorization, stability, and search completeness are separate properties. A runtime receipt must say which one it establishes.
- A research algorithm that checks the hidden gold answer at runtime has moved the intelligence into the checker. Use exact solvers only for evaluator gold or explicitly marked diagnostic ceilings.
- End-to-end cost includes preparation and abandoned work. A recovery method can save post-change tokens while losing in total expected cost if changes are rare.

