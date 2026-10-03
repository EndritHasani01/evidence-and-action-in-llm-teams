# Minimum decisive experiments

Design review: 2026-10-04. All model experiments below are **proposed**, not executed. The CPU evidence in [PROTOCOL_AUDIT.md](evidence/PROTOCOL_AUDIT.md) is separate. The selected addition refines the current PS; it does not replace its primary question.

## Finalist 1: what information must a correction preserve for useful work to remain reusable?

### Scientific question

Does giving an explicit, authenticated historical before-value change the measured value of retaining a team's previous derived history, when the current evidence, edit, prefix, peers and recovery allowance are fixed?

The comparison is about an observable correction-interface choice. It does not assume an LLM implements an incremental algorithm or that every old value is needed. A former input can legitimately inform a current computation **as a historical input** without retaining its authority as current truth.

### Minimal matched factorial

Use **every main Prefix Sum and Distributed Sort world**, selected by task before model inference: 16 worlds in the 48-world schedule or 12 in the 36-world fallback. Keep all six families and all original branches. Each focal prefix has the following four changed-event siblings:

| History | After-only notice | Before-and-after notice |
|---|---|---|
| Retain B | Existing B | New BΔ |
| Clear C | Existing C | New CΔ |

The two new branches have exactly B/C's respective current source tables and respective retention treatment. The extra receipt is constructed from the runtime's archived v1 record and actual v2 record. It contains only record ID, owner, source versions, input position where already public, historical old raw value, and current new raw value. It contains **no numerical delta, revised answer, affected-output indices, dependency annotations, suggested update formula, or evaluator feedback**. The old value is not restored to the active source table.

Freeze a common correction layout before the first pilot: a before-value field saying **not included in this receipt** in after-only arms versus the true historical-before field in the receipt arms. Do not say globally unavailable: B may still contain or reconstruct it. Both layouts mark v2 as current, v1 as historical only, and use the same neutral instruction to continue the task. Place this small notice outside derived history so C can retain it; render it consistently during recovery. This proposed rendering clarification must be documented when the specification is eventually revised. No existing model run is being altered: none exists.

Audit token lengths with the accepted tokenizer. Use a short, content-free padding convention only if necessary to keep notices at the same token length within a world; freeze it without consulting outcome differences. Keep the same total-context and generation caps. Padding controls token count, **not salience, authority cues or attention**. The estimand remains the effect of the historical receipt interface. Do not claim a pure information-processing mechanism from the factorial alone.

### Estimand and inference

Let a[p,1] be the fraction of peers with an entirely correct candidate in their **first recovery round**, before any newly generated recovery message can reach another peer. Define the focused secondary estimand within each focal world,

`eta1_w = (a[CΔ,1] - a[BΔ,1]) - (a[C,1] - a[B,1])`.

Average within each of the two families, then weight those means equally. **This sign convention is used throughout the final synthesis:** negative eta1 means the receipt favors retained-history B relative to reset C. Also report all four first-round accuracies and the two receipt effects `BΔ-B` and `CΔ-C`; a negative interaction alone could arise from harm to C rather than benefit to B. A sign-changing reset contrast is especially interpretable, but is not required for a useful result.

Retain `eta_A = (A[CΔ]-A[BΔ])-(A[C]-A[B])`, using the original four-round AUC, as a mandatory descriptive companion together with final/stable correctness, old-value errors and collateral damage. The first-round focus follows the mathematical observation boundary; it is not a claim of faster wall-clock reaction or guaranteed higher power. In a stylized prefix case where a receipt saves exactly one round for an average 1.5 downstream peers, the B effect is 0.375 at round one but 0.09375 in AUC. If both effect and standard deviation scale by four, standardized signal is unchanged. Real later-round noise and first-round floors are unmeasured. Early improvement followed by regression does not justify a recovery recommendation.

The original six-family `theta = (C-B)_change - (C-B)_sham` stays primary. Eta1 is one prespecified focused secondary estimand, with world-paired uncertainty and all raw points. Do not quietly use the old sham to claim an experimentally crossed receipt-by-sham effect: the new receipt arms are run on changed events only. Original sham and answer-preserving B/C remain useful core controls; effects of receipts on genuinely answer-preserving revisions remain untested.

If the thesis intends formal multiplicity-controlled claims for eta1 as well as the original three secondary policy contrasts, declare a four-contrast secondary family before main execution and use 98.75% intervals. Otherwise present eta1 as an explicitly exploratory mechanistic estimate with a 95% descriptive interval, retaining the original 98.33% intervals for the three core secondary contrasts. The recommended minimal extension uses the latter designation and does not manufacture a second powered primary test.

Only 8 or 6 worlds per focal family means family contrasts are descriptive. With paired eta1 SD 0.35, the rough normal-approximation 80%-power reference is about 0.245 at n=16 or 0.283 at n=12; at SD 0.60, approximately 0.420 or 0.485. These are sensitivity calculations, not measured power or justified equivalence margins; first-round SD need not match AUC SD. Repeated peers/rounds do not increase the independent n. A pooled null cannot refute the mathematical possibility, and a wide interval cannot establish the original interface is adequate.

### Predictions and discriminating observations

1. **Missing before-value with useful old summary:** an explicit transition can make updating possible from that representation before another communication round. A negative eta1 is plausible, particularly for downstream prefix peers. It is not guaranteed: prose may be wrong or models may recompute instead.
2. **Before-value already available or reconstructible:** the receipt adds presentation/retrieval assistance rather than new determinative information. An observed benefit here weakens the narrower information-deficit explanation.
3. **Other necessary information missing:** a receipt cannot recreate an omitted reserve or a remote rank-boundary value. Sort improvement may require further communication even with a correct old segment.
4. **Wrong previous work:** receipts can help apply a delta to an already wrong result, preserving its old error. Report all worlds and pre-correction correctness strata; never promote only correct old candidates into the runtime.
5. **Historical/current role confusion:** supplying the old value may increase old-gold outputs or collateral errors. That would argue against deploying the receipt by default, even though the historical fact is accurate.

The mathematical atlas identifies distinctions, not a six-task causal ranking. Prefix-versus-sort differences are not solely caused by update sufficiency: arithmetic, output allocation and coordination differ too.

### Offline observability audit

Before scoring recovery outcomes, derive from the frozen prefix and renderer:

- Which peers had actually received v1 and when. Delivery does not imply v1 is still visible after replacement.
- Whether a structured source reference in retained history identifies v1 but omits its raw value.
- Exact matches between the changed record/value and rendered historical content, where unambiguous. Numeric-token occurrence alone is not semantic evidence that the value belongs to that record.
- Correctness and shape of the old typed candidate, for evaluator-only stratification.
- Whether complete current sources are available, a strong sufficient condition for exact fresh recomputation; absence of full coverage is **not** proof that the prompt lacks enough information.
- Task-specific constructive sufficiency cases (for example, correct full difference vector plus an unchanged raw anchor) and clearly stated unresolved cases.

Use conservative labels: directly visible, provably reconstructible under specified correct-summary assumptions, or unresolved. Do not use an LLM dependency extractor or treat unresolved as mathematically absent. The audit never chooses receipt delivery or removes worlds based on the expected effect.

### Stronger controls and stop rules

The four-way factorial, shared rendering, token accounting and exact unaffected-coordinate diagnostics are mandatory. CΔ is essential: BΔ alone cannot distinguish a general correction-interface effect from an interaction with retained work. No extra calls, thinking tokens or stronger repair instructions are permitted.

A candidate-only history arm or a separate redundant-value wording arm could help diagnose an unexpected result, but would require new preregistered calls and a new budget. They are **not** silently promised by this minimal experiment. Without them, constrain claims to the receipt interface and observed behavior. A runtime-optimal exact updater is a CPU reference, not a fair model competitor and not a policy allowed to consult gold.

Admission depends on generator/renderer correctness, model capability, valid outputs, context capacity and measured cost. It must never depend on the desired eta1 sign. If natural prefixes make historical information uniformly redundant, the thesis may downgrade the information-deficit interpretation; presentation/computation effects could still be studied with narrower claims. It must not tune prefixes or select worlds to manufacture receipt dependence.

## Finalist 2: conservative exposure versus useful selectivity

Use existing immutable source-delivery and message histories to construct a time-respecting possible-dependence graph. A call can depend on all inputs actually visible to it; own later histories and recipients can inherit exposure. Distinguish an exposed message present at the boundary from a candidate generated before that message arrived. Counting static graph edges is insufficient. This is an envelope under a specified delivered-content model: missing expected messages, routing decisions and evidence selection can carry additional implicit influence, so actual delivered edges alone do not certify full noninterference.

Report the fraction of retained derived objects inside the corrected record's conservative cone, by prefix round, and contrast it descriptively with exact output footprint D and observed recovery outcomes. Keep evidence-table selection influence explicitly outside any narrow derived-object noninterference claim. This is a **zero-extra-call analysis**, not a new taint algorithm or a causal law of topology.

An additional cone-cut arm would require a size/age-matched history-removal control and preferably sham counterparts. That is at least two additional changed continuations (32 calls/world), more for sham; degenerate cones often reduce the policy to C. Do not run this arm unless the trace analysis reveals genuine nontrivial retained regions and a scientific question beyond known conservative invalidation. This optional gate concerns treatment distinctness, not whether C wins.

## Finalist 3: candidate-only retention

Keep C's evidence plus only the last own typed candidate, without copying other peers' private candidates into the prompt. Compare with B and C under change and sham. This adds two continuations per chosen world (32 calls). Its useful question is whether a small result representation captures most of history's value.

[ICR](https://arxiv.org/html/2610.01042v1) already studies answer-only versus full reasoning communication. The application to changed private collaborative worlds remains different, but this is a weaker original addition than the receipt interaction. A typed candidate is not guaranteed correct, and local outputs need not be sufficient for updating. Retain as a simpler rival explanation and future ablation; do not append it automatically.

## Finalist 4: completion/search reopening

Use the earlier [validation strategy](../research_innovation/VALIDATION_STRATEGY.md) and [new competitor review](reviews/COMPLETION_COMPETITOR.md). The decisive comparison remains enforced reconsideration versus generic reconsideration with identical artifacts, evidence, task records and opportunities, plus a matched-observation and control/membership-aware baseline. This needs new acquisition/search semantics and would replace much of the original matrix. No such replacement is recommended here.

The old CPU counterexamples remain valid lessons. They do not establish natural omitted-work prevalence or model benefit. If a straightforward existing control-node invalidation rule reproduces the behavior with identical observable state, present it as an application of that rule.
