# 11 — Tell the team what changed from the old value to the new one

**Recommendation: worthwhile focused explanatory addition; third among these five for broad practical thesis value.** The earlier investigation favored it under a novelty-focused objective. Here it is reassessed simply as a useful, feasible question. It should compete fairly with compact state and fixed delayed reset.

## Simple question and value

Does a team make better use of its earlier work when a correction says “this record changed from old to new,” rather than only giving its new value?

The PS gives B and C identical current source tables. B may still contain old values in its discussion; C clears that discussion. An explicitly historical before-value could make old calculations easier to update, help a reset team understand the edit, or confuse the model into repeating obsolete information. This is a concrete interface choice for an agent runtime.

## Exact receipt and arms

The runtime already archives v1 for audit. Construct a receipt containing the changed record ID, owner, old/new versions, historical old raw value and current new raw value. Include a position only when it was already part of the task's public source metadata. The old value stays outside the current source table and is labeled historical.

Add **BΔ** and **CΔ**. Their retention rules and current source tables remain exactly B and C. Their only new information is the receipt's historical before-value. No mathematical delta, affected output indices, suggested repair formula, gold answer, semantic dependency annotation or extra model opportunity is supplied.

Use a common correction layout with “not included in this receipt” in the after-only before-value field. Do not say the old value is globally unavailable: B may contain it. Preserve generic instructions and token caps. Record prompt lengths; the receipt is a package of information and presentation, so an advantage need not prove arithmetic delta reasoning.

## Minimum useful live comparison

Use **every main Prefix Sum and Distributed Sort world**, selected by task before any inference: 16 worlds with the 48-world core or 12 with the 36-world core. Add BΔ/CΔ for answer-changing revisions only, comparing the four siblings B/C/BΔ/CΔ from each original prefix.

The focused descriptive estimand is the first-recovery-round interaction:

`eta1 = (a[CΔ,1] - a[BΔ,1]) - (a[C,1] - a[B,1])`.

Round one precedes newly generated recovery messages, so this targets what the receipt changes before another exchange. Negative eta1 means the receipt favors B relative to C; show both direct effects because that sign can also arise from harm to C. Also report the four-round AUC interaction, complete curves, final/stable correctness, stale outputs and collateral damage. Earlier correctness does not itself demonstrate reduced communication or saved model calls.

There are **no new sham branches in this minimum design**. The original B/C sham branches remain part of the core, but they do not identify a receipt-by-sham interaction. A historical before/after receipt is naturally defined for a real change; a fabricated no-change event would introduce a different intervention. Effects on answer-preserving revisions are also outside this minimal focal study.

With 12–16 focal worlds, intervals may be wide. A zero interaction can conceal equal large benefits in B and C. Recommend or omit receipts using direct benefits, harms, cost and uncertainty, not the interaction alone.

## Why focus the live test but discuss all six families?

| Task | What the before-value contributes |
|---|---|
| Maximum | A correct old maximum already equals the former winning value. The harder missing item may be the runner-up. Useful as a redundancy example, not an automatic live priority. |
| Top-K | It can identify which old list member belongs to the edited record, but cannot supply a missing new entrant. |
| Prefix sums | It can distinguish updates that look identical from a downstream peer's retained subtotal and current local sources. Some old values are already reconstructible from adjacent sums. |
| Difference array | A correct full difference vector and an unaffected raw anchor can reconstruct the old array; a receipt can still reduce computation effort. |
| Distributed sort | Sorting loses source-to-value correspondence. The old value restores that association, while remote rank-boundary values may still be needed. |
| BFS | A tombstone or source ID may already reveal the deleted edge. A receipt cannot provide alternate paths absent from available evidence. |

The [existing mathematical analysis](../research_innovation_v2/CROSS_FIELD_INVENTIONS.md) makes these distinctions useful explanatory material. Its constructed examples establish possibility under specified views, not the frequency of those views in model runs. They do not imply that four subsequent communication rounds cannot recover the answer.

## Additional calls and effort

| Component | 48-world core | 36-world core |
|---|---:|---:|
| Focal prefix/sort worlds | 16 | 12 |
| BΔ/CΔ changed continuations | **512** | **384** |
| Additional sham continuations | 0 | 0 |
| **Extended main total** | **6,368** | **4,872** |
| BΔ/CΔ on two existing development worlds | 64 | 64 |

The 588-call pilot becomes 652, before the original 24-call smoke allowance and failed configurations. At an illustrative 15 allocated seconds/call, the main increment costs 2.13 or 1.60 aggregate GPU-hours. Actual timing, context sizes, failed attempts and reserves determine whether it fits the 30-hour ceiling; no inference has established that fit.

Estimated effort beyond the PS: **3–5 focused working days** for receipt rendering, paired branch setup, old-value visibility checks and the additional analysis. CPU/mock checks must ensure obsolete values are never restored as current evidence and that source references do not leak unrelated records.

## Useful outcomes and recommendation

- B benefits more: retained work is more useful with a clearer transition interface.
- Both benefit similarly: receipt presentation helps even though the retention comparison is stable.
- Benefits occur only before the next exchange: the receipt can accelerate an early response; later trajectories determine practical value.
- Receipts increase stale-value copying: historical/current labeling is insufficient for this model and protocol.
- The before-value is usually present already: the interface may be unnecessary or useful mainly as a retrieval cue.

This is a good choice if the thesis should explain **what information makes prior work reusable**. It is narrower across tasks than compact-state K and has a more delicate interaction estimate. Under the current usefulness-first objective, keep it as a serious alternative rather than automatically adopting the earlier recommendation. Run at most one of these live extensions unless measured resources and a clear combined research question justify more.
