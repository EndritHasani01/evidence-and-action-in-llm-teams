# 07 — Keep the last answer, clear the conversation

**Recommendation: strongest optional live addition among these five when practical usefulness and simplicity are the priorities.** It adds a concrete middle policy to B/C/F and works with all six task families. This is a proposal, not an executed result. The PS and both innovation workspaces remain unchanged.

## Simple question and thesis value

Can a team keep useful completed calculation in a compact form while discarding most of the old conversation?

The current study compares retaining all derived history (B) with clearing it (C). A runtime might reasonably keep just each peer's last submitted answer. Testing this provides a usable recovery option and helps explain whether the value of history comes mainly from its final result or from the intermediate exchanges that produced it. Familiarity of the idea is no reason to exclude a useful comparison.

## Exact policy K

At the existing correction boundary, give every peer exactly B/C's corrected source table and broadcast notice. Clear the same derived history, received prose and validation history as C. Retain only that peer's **own actual typed candidate from prefix round four**, marked as that historical provisional answer. Do not reveal other peers' candidates unless they would subsequently communicate them normally. K supplies no former raw input, computed delta or reconstructed peer result.

If the latest reply has no schema-valid candidate, retain an explicit absence marker. Do not search backward for a better-looking answer, use a correctness test to choose an answer, repair it, summarize it with another model, or add gold values. A wrong but schema-valid candidate is retained. This exact fallback rule must be frozen before runs.

Keep the same four recovery rounds, 384-token output cap, peer routing permissions and generic task instruction. New recovery messages are delivered normally. Candidate retention does not grant the old answer authority as current truth.

## Minimum useful experiment

Select **12 main worlds in advance: two per family**, by fixed seed-list position. Add K under both answer-changing revision and no-change continuation. Reuse each world's existing B/C and, for changed events, F. The original six-family primary estimand remains untouched.

Report K−C and K−B after change using the original accuracy AUC, full recovery curves, final/stable completion and collateral damage. Show the corresponding sham contrasts. This reveals whether K offers a correction-specific compromise or simply provides a generally convenient short context. All selected worlds remain included, including incorrect prefixes and invalid latest candidates.

K changes the amount and content of retained context together. That is acceptable for a practical policy comparison. Record input tokens and actual allocated time; do not infer a particular psychological mechanism from an advantage. Equal call counts do not imply equal GPU cost.

With two worlds per family, family patterns are illustrations rather than precise rankings. Pool using equal family weights and keep all branches, peers and rounds clustered within their base world. Lack of significance is not evidence K is equivalent to B or C.

## What each family contributes

| Task | Why retaining the candidate could help or hurt |
|---|---|
| Maximum | The old maximum is short and often becomes wrong after the edit. It may anchor the team without retaining the runner-up. This is a useful case where compactness need not preserve useful work. |
| Top-K | Most of the old list may remain useful, but the new cutoff entrant may be absent. The test separates partial result preservation from the need to obtain alternatives. |
| Prefix sums | An old local result contains substantial calculation. Updating it can still require the former input or an upstream subtotal. |
| Difference array | Most coordinates survive a one-entry change. Retaining the complete vector may preserve considerable correct work, while also preserving any old errors. |
| Distributed sort | A local rank segment is useful but may need boundary values from other peers. This tests whether compact local results support coordination. |
| BFS | Distances provide a useful starting proposal but do not identify all alternate paths. Keeping them can accelerate recovery or preserve an incorrect path assumption. |

These differences make a broad six-task comparison worthwhile. They do not establish expected model performance.

## Incremental cost and effort

| Component | Extra scheduled model calls |
|---|---:|
| K after change on 12 worlds | 192 |
| K under sham on the same 12 | 192 |
| **Main addition** | **384** |
| K change+sham on two existing development worlds | 64 |

Use two worlds already assigned sham B/C in the original pilot; if selecting those now, prefix sum and BFS exercise segmented and longer replicated candidates. Otherwise adapt the choice to the already frozen pilot assignments rather than silently adding missing baseline cells. New worlds or extra prefix calls are unnecessary.

This produces main totals of **6,240** with the 48-world core or **4,872** with the 36-world core. With 24 hours reserved for main inference, their arithmetic break-even averages are about **13.85 / 17.73 allocated seconds per call**, before additional overhead. The original 588-call development pilot becomes **652**, before the existing maximum 24-call smoke allowance and failed attempts. At an illustrative 15 allocated seconds/call, the 384 main calls cost 1.60 aggregate GPU-hours and the 64 development calls cost 0.27 hours. These are arithmetic examples, not throughput forecasts. The 30-hour ceiling and measured phase-specific forecast still decide admission.

Estimated implementation effort beyond the PS: **2–4 focused working days**, including a state projection, renderer checks, two event branches and analysis. Verify that candidate absence is handled deterministically, source evidence is identical to B/C, and no old candidate is scored as a new answer without a new model reply.

If more room is available, 16 worlds across the six families can cap the addition at 512 main calls, but their unequal family counts require explicit weighting. Twelve worlds with an understandable balanced design is the simpler starting proposal.

## Useful outcomes

- K approaches B's recovery with shorter prompts: a compact answer is a practical way to preserve much of history's value.
- K beats C but loses to B: some completed calculation helps, and intermediate work still matters.
- K resembles C: final candidates contribute little beyond current evidence in this setting, or uncertainty is too wide to resolve their value.
- K preserves wrong answers or damages recovery: clearing derived results can be preferable even when they are compact.
- K helps similarly under change and sham: the result concerns general context management as much as correction.

**Choose this rather than running all five additions.** It gives the thesis a clear practical comparison with a small implementation burden. [ICR-related notes](../research_innovation_v2/sources/RECENT_AGENT_LITERATURE.md) provide useful background for answer-versus-reasoning comparisons; the purpose here is to learn what works in this particular distributed recovery study.
