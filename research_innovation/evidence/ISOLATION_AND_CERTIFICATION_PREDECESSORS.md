# Direct predecessors to isolation and validity-based reuse

Updated 2026-09-30. Primary full texts obtained through the web. These sources materially weaken broad novelty claims. Numerical claims below are source-reported and not reproduced.

## Continuity Kernel (2026)

Source: [Beyond Memory: A Transactional Continuity Kernel for Long-Lived AI Agents](https://arxiv.org/html/2608.11632v1). Inspected sections 1-4 and evaluation scope; full HTML accessible.

The paper separates candidate preparation from authoritative state activation. It implements exact predecessor checks, writer epochs, commit-time freshness and authorization, and stable Commit/Reject/Quarantine/Defer outcomes. Its evidence is bounded state-space exploration, not end-to-end recovery quality. Sections 2.3 and 3.4 explicitly exclude semantic correctness; prompts, caches, weights and tool-local state are outside the boundary unless separately mediated. Evaluators can be wrong.

**Implication:** neither an activation boundary nor quarantined old work is a new primitive. An empirical study of semantic recontamination through live context can remain distinct, but must cite CK and state exactly what additional guarantee or measured behavior it addresses.

## Agentic lakehouse (2025)

Source: [Safe, Untrusted, Proof-Carrying AI Agents](https://arxiv.org/html/2510.09567v1). Inspected full short paper, especially sections II-IV.

The prototype lets agents repair pipelines on data branches, then uses an owner-provided verifier before merge. Declarative I/O, isolated functions, versioned inputs and atomic publication preserve production state even when repair fails. Its authors describe a feasibility demonstration, not a comprehensive benchmark. The verifier is a business-context function, not a universal formal proof.

**Implication:** reuse-as-proposal plus verify-before-publish is already translated into LLM agents. The project would need a sharper question about changing inputs, partially valid collaborative state, verifier limits, or missing provenance.

## ESC-CR (September 2026; history requires checking)

Source: [Policy-Backed Selective Regeneration under Tainted Inter-Agent Communication](https://arxiv.org/html/2609.26072v1). Full HTML and methods (claim verification, taint closure, allowlist reconstruction, release boundary) inspected. Search date metadata conflicts with the arXiv identifier, so do not cite search-derived submission dates.

The abstract explicitly combines evidence-backed information preservation, tainting of a responsible message and rejected artifact, a clean reconstructed context, and regeneration under an external release policy. It contrasts polluted-context retry with indiscriminate message removal and uses matched budgets. The target is unauthorized instructions in agent communication, not benign source revision.

**Implication:** evidence-preserving clean-room recovery already has a direct security predecessor. A benign-correction extension is potentially useful, but cannot claim the first separation of useful message content from unsafe influence.

## APPA (July 2026)

Source: [Agentic Permissions Policy Algebra for Taint Confinement in LLM Agents](https://arxiv.org/html/2607.24625v1). Full HTML and branching/exit rules and limitations inspected.

The abstract proposes engine-managed child contexts for inspecting unvetted data and a trusted sanitizer returning bounded derivatives, while preserving parent labels. It addresses utility loss from permanent context taint and gives both a formal model and multi-model experiments.

**Implication:** context branching and bounded sanitized return are established. A recovery contribution must examine different failure semantics: formerly valid material becomes stale after exposure, rather than starting as known untrusted material.

## Further relevant primary texts obtained

- [Fides: Securing AI Agents with Information-Flow Control](https://arxiv.org/html/2505.23643v2): inspect conservative context-label propagation and endorsement; not the unrelated trading-strategy paper with the same acronym.
- [NeuroTaint: Ghost in the Agent](https://arxiv.org/html/2604.23374v1): offline semantic and causal source-to-sink auditing, including memory/session boundaries. Its claimed detection improvements do not establish a sound recovery gate.
- [No Certificate, No Execution](https://arxiv.org/html/2605.24462v1): Proposal-Certification-Execution and certified traces; distinguish permissions from factual correctness.

## Revised hypothesis

The scientifically interesting gap is unlikely to be another generic gate. It may be the mismatch between **recorded authority** and **actual semantic influence after change**: coarse runtime exposure is conservative but costly; self-reported fine dependencies are efficient but incomplete; clean contexts can still be recontaminated by an admitted summary. Compare these interfaces causally and report the conditions under which each works. Do not add the full CK/APPA machinery to a 30-GPU-hour thesis just to inherit their vocabulary.

