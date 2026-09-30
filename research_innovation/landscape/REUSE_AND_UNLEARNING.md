# Additional close prior work: reuse and unlearning

Inspected 2026-09-30. Primary HTML or author-authored material; claims below are reported by sources, not reproduced locally.

## Invalidation Contracts for Cross-Episode Agent Memory

[Primary paper, v1, 31 August 2026](https://arxiv.org/html/2609.00243v1). Inspected protocol, experimental design, results and limitation passages. The protocol attaches versions and cacheability information to cached API recovery suggestions, with row-level invalidation, dependency vectors and rule fingerprints. It separates validity from the planner's actual use of a valid suggestion. The synthetic API evaluation spans multiple models and serving paths; its exact invalidation properties rely on controlled server semantics. Implication: neither versioned reuse contracts nor separating validity from compliance is new. Relevant unresolved questions concern opaque derived peer work and independently defensible artifact semantics, not a new cache stamp.

## Forgetting Without Restarting

[Primary paper, v1, September 2026](https://arxiv.org/html/2609.04875v1). Inspected formal model, method and evaluation discussion. It defines execution-state unlearning using a never-observed counterfactual, restores a clean prefix, and regenerates the sanitized suffix across prompt, memory and cache. Its exactness and lower bound depend on its transition-system/access assumptions; they are not universal results about all semantic artifact reuse. Implication: context cleanup and selective counterfactual replay are occupied. Ordinary correction can have a weaker goal: accept an old artifact that demonstrably satisfies the new task, without asserting that its construction was historically independent of the old source.

## The Process Is the Memory

[Author technical report, dated 17 July 2026](https://yonk.dev/blog/process-as-memory/). Inspected cost model, simulation claims and explicit limitations. It prices process reuse against checking and rederivation, studies missed dependencies, and uses broad fingerprints with narrower refinement. It openly attributes its components to earlier systems work. Evidence is chiefly deterministic simulation, not validation of arbitrary LLM semantics. Implication: cost-aware reuse, broad canaries, and process-over-fact caching cannot be presented as untouched ideas. A fingerprint detects changes in represented state; it cannot detect a semantic change absent from that representation.

## Research inference

The interesting remaining comparison is not simply selective versus total deletion. It is whether current-world evidence can justify useful reuse when historical dependency attribution is unreliable, and when acquiring that evidence is cheaper than reconstruction. Any proposed mechanism must answer this without smuggling the task's gold answer into a checker.
