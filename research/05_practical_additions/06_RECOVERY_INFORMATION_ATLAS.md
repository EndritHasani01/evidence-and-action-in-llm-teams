# 06 — A small atlas of what retained work contains

**Recommendation: include a concise version. Additional model calls: 0. Estimated work: 2–3 focused days, overlapping with deterministic-reference analysis.**

## The idea and question

For each task, explain **what a peer would need to update its old result correctly**. Sometimes the old result plus the correction is enough. Sometimes it lacks the previous input value, an omitted alternative, or another peer's part of the answer.

This is a useful thesis addition because it separates “the model did not use available information” from “this restricted representation never contained enough information.” It also explains why retaining evidence and retaining a computed answer can help in different ways. The atlas is a small table with examples, not a new provenance system or a general theorem-development project.

Classical incremental view maintenance supplies the underlying idea; the project applies it to the actual source views and output assignments already chosen in the PS.

## Four distinctions to retain

1. **Current evidence:** raw records that remain valid now.
2. **Historical transition information:** the old and new values of the changed record. The PS guarantees the new value in B/C; it does not guarantee that the old raw value remains visible after source replacement.
3. **Retained result:** a scalar, ranked list, local output segment or distance map. Its usefulness depends on both what it encodes and whether the model originally computed it correctly.
4. **Information elsewhere:** a remote boundary value, discarded runner-up or alternative graph path. A complete correction does not automatically supply this.

“Enough information” must always name the view: one peer's latest candidate, all peers' candidates together, or current raw sources. A proof about the union of four outputs does not establish what one peer can know.

## Minimal atlas

| Retained representation | What can be done under stated assumptions | What can still be missing |
|---|---|---|
| Correct local Prefix Sum segment + changed position + authenticated old/new values | Add the input difference to the affected entries in that segment | Under the normal after-only notice, a remote old operand or first-shard boundary may be unidentified |
| Correct complete Difference Array + one unchanged current raw value | Reconstruct the old numeric array, including the former edited value | The model must actually perform the reconstruction; a wrong old difference vector is not trustworthy |
| All correct Sort segments together + old/new value | Replace one multiset occurrence and re-sort | Each peer only owns one output segment; source-ID-to-old-value identity and remote rank boundaries can be missing locally |
| Old maximum | Some increases are easy to apply | Lowering the unique maximum can require a runner-up that the scalar discarded |
| Old top-K list | Some updates remain within the retained ranked values | Lowering a selected value below the cutoff can require an omitted replacement |
| Old BFS distances + deleted edge | Some unaffected values remain useful | The map does not encode enough alternative-path structure to determine every new distance |

This table is about mathematical representations. It does not certify free-form peer prose, classify every natural transcript, or predict that one task must be harder for an LLM.

## Smallest useful deliverable

Use the existing CPU evidence rather than starting again:

- One constructive Prefix Sum update showing how many changed coordinates can be repaired from one known scalar difference.
- One local-prefix ambiguity example: the same old segment and new local records can require different new segments when the historical operand or earlier-shard total differs.
- The Difference Array reconstruction example showing that apparently missing information may be recoverable from a different representation.
- One max or top-K example where the old result discards the newly needed runner-up.
- One sort or BFS example illustrating distributed ownership or omitted alternatives.

The [v2 protocol audit](../04_design_extensions/evidence/PROTOCOL_AUDIT.md) and [cross-field notes](../04_design_extensions/CROSS_FIELD_INVENTIONS.md) already contain relevant exact examples. Reuse and verify the selected cases in the eventual analysis; this proposal does not claim new model results.

Keep the formal statement short: a revised answer can be determined from a retained representation and edit only if any two worlds with the same visible representation and edit require the same revised answer. One paragraph explaining this is sufficient for the main thesis. Put longer proofs in an appendix.

## Connect the atlas to actual runs

Before reading policy outcomes, annotate the frozen views with conservative categories:

- The former value is explicitly associated with the changed record in the rendered input.
- It is provably reconstructible under a named correct-candidate assumption.
- Complete current raw inputs are present, making exact fresh recomputation possible.
- The status is unresolved.

A bare matching number in prose is not proof of its association with a record. “Unresolved” is not “absent.” Treat old-candidate correctness as an offline stratum; never remove unsuccessful prefixes or use gold to decide what the runtime retains.

Then ask modest questions: do failures persist even with complete current sources? Do successful retained-history branches use a summary where source-only restart must reacquire evidence? Do wrong old results remain wrong after an otherwise correct adjustment? Traces can illustrate these cases; correlations alone do not identify their hidden reasoning mechanism.

## Outcomes and value

The atlas is useful with positive, negative or mixed policy results. It can explain why reuse helped, show that a proposed information gap never arose naturally, or reveal that all current facts were present and capability was the practical limit. It also prevents a misleading story that every unchanged output was independently justified or every exposed history item was harmful.

Do not require a receipt experiment to justify the atlas. Under the current priority—an interesting, useful and feasible thesis—the explanatory analysis is worthwhile on its own. Keep it to roughly one main-text table, two or three compact examples, and a short appendix.
