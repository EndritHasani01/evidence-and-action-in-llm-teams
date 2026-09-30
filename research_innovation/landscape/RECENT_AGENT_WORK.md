# Recent agent-recovery work: live research ledger

Inspected 2026-09-30. Primary papers are preprints unless noted. Findings below distinguish full-text inspection from abstract-only leads. Published claims are not reproduced results. This ledger is being updated during the investigation.

## Strongest immediate implications

- Recovery, staged publication, contaminated-descendant withdrawal, independent-support preservation, and selective replay already have direct agent implementations. None should be advertised as a first contribution.
- Important correction to inherited framing: **REVISE uses automatic structured-state read instrumentation**, not only handwritten dependency declarations. Its remaining difficulty is unknown or overly broad influence through opaque contexts and control, rather than absent field-level tracing.
- The promising question is narrower: what useful reuse remains possible when a runtime cannot establish that previously exposed context is unaffected, and how can that be studied without an oracle supplying semantic independence?

## Source map

| Work | Version/date | Access and relevant sections | Focused note |
|---|---|---|---|
| PlanFence | arXiv 2609.03340v1, 2026-09-03 | Full HTML, §§3–6 and appendix | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| From Faulty Memories to Corrected Actions | arXiv 2608.10502v1, 2026-08-11 | Full HTML, §§3–5 and appendices | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| REVISE | arXiv 2609.00643v1, 2026-09-01 | Full HTML, §3 and appendix integration/provenance sensitivity | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| AgentRewind | arXiv 2608.14380v1, August 2026 | Full HTML, framework and experiments | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| STALE | arXiv 2605.06527v1, May 2026 | Full HTML; latent conflicts/probing framework | [Semantic revision](SEMANTIC_REVISION.md) |
| MemTX | arXiv 2607.23929v2, July 2026 identifier | Full HTML; lifecycle, repair, assumptions | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| StateAuditor | arXiv 2608.01619, August 2026 | Full HTML opened; method inspection underway | [Semantic revision](SEMANTIC_REVISION.md) |
| PACMI | SSRN 7480138, written 2026-09-17, posted 09-19 | Primary abstract accessible; full text not yet | [Semantic revision](SEMANTIC_REVISION.md) |
| MemoRepair | arXiv 2605.07242, 2026-05-08 | Primary abstract; full text next | [Protocol recovery](PROTOCOL_RECOVERY.md) |
| Repair Sets Before Repair Choices | OpenReview IJoWb6T3RJ | Forum browser challenge; API route failed; title search produced no verified primary result | Unverified, no technical claims inherited |

## Search directions remaining

Find semantic revision methods operating without complete provenance; check memory-unlearning and invalidation-contract work (parallel investigation); follow MemoRepair's contract carefully; look for inexpensive measurements separating harmful inherited reasoning from harmless expensive work.
