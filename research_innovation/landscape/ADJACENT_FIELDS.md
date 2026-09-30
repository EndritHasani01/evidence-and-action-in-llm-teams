# Adjacent-field investigation: recovery as controlled reuse

Updated: 2026-09-30. Status: working research notes; primary-source search and method inspection in progress. This file is owned by the adjacent-fields investigator. The project specification is read-only.

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
| [Build systems a la carte](https://simon.peytonjones.org/build-systems-a-la-carte/) | 2018; journal extension 2020 | Author landing page and search excerpts; full paper pending | Schedulers versus rebuilders; verifying and constructive traces; early cutoff | Requires a specified task evaluation model and tracked inputs; textual dependencies are not complete semantic read sets |
| [Chubby](https://research.google.com/archive/chubby-osdi06.pdf) | 2006 | PDF introduction and sections 2.3-2.4 | Recipient-side generation checks prevent delayed stale actors from affecting protected resources | A fresh generation proves authorization, not correctness or absence of old-fact influence |
| [Keeping CALM](https://arxiv.org/html/1901.01930) | 2019/2020 | Full HTML obtained; detailed inspection pending | Coordination-free consistency tied to logical monotonicity | Revisions/deletions are nonmonotone; convergence does not establish semantic correctness of LLM claims |
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
