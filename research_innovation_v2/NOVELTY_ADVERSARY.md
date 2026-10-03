# Hostile review of the finalists

Review date: **4 October 2026**. No recovery model runs have been executed. This document attacks the strongest interpretations of the candidates rather than treating search failure as evidence of novelty. Source methods and access limitations are recorded in [recent literature](sources/RECENT_AGENT_LITERATURE.md), [receipt review](sources/TRANSITION_RECEIPT_NOVELTY.md) and [search log](sources/search_log_recent.md).

## Verdict before empirical results

The best research-level addition among the finalists is **one focused factor: what historical transition information the correction receipt provides**, crossed with the existing retain/reset treatments on **all predetermined Prefix Sum and Distributed Sort worlds**. Keep the PS's original six-family primary question, sample target and estimand. Present the addition as a test of the conditions under which retained work remains useful, with exposure selectivity as a cheap descriptive companion. This final selection supersedes the initially considered all-six-family receipt matrix.

This is a **conditional preference**, not a finding that a novel recovery algorithm exists. The exact statistical interaction is not, by itself, a major theoretical contribution. The addition earns its place only if it produces a clear, bounded lesson about a real runtime decision at acceptable cost. If the claim requires calling a before/after event a new mechanism, interpreting ordinary prompt sensitivity as incremental reasoning, or sacrificing the main study's interpretability, keep the PS essentially unchanged.

The completion redirection has no presumptive advantage. It faces equally strong prior art while requiring more new state semantics, tasks, assumptions and controls.

## 1. Transition receipt × retained reasoning

### Strongest proposed claim

Current-state evidence is sufficient for solving afresh but need not be the same information required to update an existing intermediate result. The PS's B/C contrast controls current source tables, while removing history can also remove old values needed to interpret a transition. Test the reset contrast under after-only versus authenticated before/after receipts, using the first corrected response as the focused boundary:

`eta_1 = (a[C_delta,1] - a[B_delta,1]) - (a[C,1] - a[B,1])`, on the same changed world and shared prefix, where `a[p,1]` is the fraction of peers with an entirely correct candidate in recovery round one.

Keep `eta_A = (A[C_delta] - A[B_delta]) - (A[C] - A[B])` as the **mandatory descriptive four-round AUC companion**. For either quantity, a negative sign means the receipt benefits retained-history B more than reset C. The original change-versus-sham AUC interaction `theta` remains primary. These quantities ask about the correction interface; they do not revise the task or give a runtime access to its gold footprint.

### Final refinement: first-response alignment is scientifically justified

**Endorse eta_1 over eta_A as the one focused receipt estimand, provided this choice is frozen before any outcomes.** In the synchronous protocol, every first-round call occurs before any newly generated recovery message becomes visible. The mathematical observability examples identify an information gap at that boundary, not impossibility after four further communication rounds. The first response therefore tests the specified boundary directly. This is a question about available information and useful retained work, not a wall-clock reaction-time experiment.

AUC can dilute a short-lived advantage. As an illustration only, if an idealized receipt saves one round for an average of 1.5 of four peers and later performance is identical, its AUC contribution is `1.5 / (4 * 4) = 0.09375`. The premise is not established for the actual tasks or model; this number is neither a theorem nor a ceiling on possible effects. It explains why the original 0.10 practical AUC reference cannot automatically serve as the receipt study's detection target.

This refinement does **not** establish greater statistical power. If every world's AUC interaction were exactly one quarter of its first-round interaction, both the mean signal and its standard deviation would scale by one quarter: the standardized effect and corresponding power would be unchanged. First-response exactness is discrete and can vary more across worlds; sort may have a first-round floor because the receipt cannot supply missing remote rank values. Report all four first-round means, their receipt contrasts, eta_1 and paired uncertainty. Keep complete recovery curves, eta_A, stale-value frequency and unaffected-coordinate damage beside them. An early gain that disappears, reverses or causes collateral damage must not be presented as sustained recovery improvement. Earlier correct responses before new messages do not by themselves establish avoided communication or recomputation: that explanation requires supporting traces and remains vulnerable to salience effects. The fixed four-round schedule also means an earlier correct response demonstrates no actual reduction in allocated model calls. Under these restrictions, eta_1 is a sharper estimand rather than a cosmetic attempt to find significance.

### Attack: a zero interaction does not make the receipt useless

Eta_1 can be zero when the receipt improves B and C by equally large amounts. A precisely bounded null establishes only stability of the **immediate retain/reset contrast** under this interface change. Eta_A addresses trajectory-level stability separately. Neither alone justifies omitting the receipt. That operational recommendation also needs the direct receipt benefits, harms and added costs to be sufficiently bounded; with 12–16 focal worlds, such bounds may remain wide. Always show `a[B_delta,1]-a[B,1]`, `a[C_delta,1]-a[C,1]` and the corresponding AUC contrasts alongside both interactions.

### Reduction: this is ordinary change-data capture

A before/after record is a conventional update event. Incremental view maintenance, differential computation, event sourcing and temporal databases already preserve historical values to propagate changes or reconstruct prior states. Calling the record a “receipt” creates no new algorithm, representation principle or guarantee. A deterministic delta updater for a known sum is likewise not an invention.

[StateAuditor](https://arxiv.org/html/2608.01619), §§4.3–4.4, explicitly represents previous/current states and transition evidence; its matched controls distinguish transition machinery from more evidence/calls. [RIAG](https://arxiv.org/html/2610.01249), §§3–4, separates historical and current bindings and uses exposure ancestry. Thus neither “historical information may remain useful” nor “transitions aid revision” can carry the novelty claim.

**Residual claim that survives:** under bounded opaque peer computation, measure whether a runtime's revision payload changes the relative value of retaining derived state, with current evidence, pre-event work, output budgets and exact scoring controlled. The inspected predecessors do not establish this particular result. That supports a focused empirical addition, not an absence-of-prior-art assertion.

### Reduction: it is a clearer prompt

The before-value changes information, token count, lexical overlap and the salience of the change. [Precomputed-memory correction research](https://arxiv.org/html/2608.30647), §6, already demonstrates strong sensitivity to update wording and a false-value compliance control. An observed BΔ/B improvement cannot automatically be called better causal understanding or arithmetic delta reasoning.

Use a fixed receipt layout, the same current value and generic correction instruction, and make the status of an unavailable before-value explicit. Preserve the generation cap and count any additional prompt cost. Do not require an elaborate padding matrix merely to obtain permission to report the package effect. Conversely, if the final claim isolates “historical information” rather than the whole receipt interface, a minimal matched-format/salience diagnostic is necessary. Arbitrary neutral padding does not prove equal attention.

**Abandon the stronger mechanistic interpretation** if the benefit is reproduced by a same-information clearer instruction, if output patterns do not distinguish transition use from renewed solving, or if only a specially tuned phrasing works.

### Attack the mathematical premise using the actual PS

The proposition “the old value is missing, therefore recovery is impossible without a receipt” is false in general. Any impossibility witness must specify exactly which old outputs and current sources are available. A witness over a restricted summary is not automatically a theorem about the full PS prompt.

| Family | Hostile counterargument | What remains worth testing |
|---|---|---|
| Maximum | Under the main edit, the corrected record was the unique maximum. A correct retained scalar answer already gives its old value. The new maximum generally requires the runner-up, which the before-value does not supply. | A receipt may be redundant, may identify the event more clearly, or may worsen stale-value repetition. Treat this as a structural control, not a positive delta showcase. |
| Top-K | The old changed value occurs in the old correct list, but the source-ID-to-value correspondence may be missing. The newly entering cutoff value is outside that list, so the receipt alone cannot reconstruct the updated top ten. | Before-value identification can support removal and partial reuse, but acquisition of the missing competitor remains necessary. Do not attribute an entire answer repair to the receipt. |
| Prefix sums | A peer holding adjacent correct prefix sums can recover many old entries by differencing; a peer's own segment and source position may already reveal the before-value. Other peers and shard-boundary positions have different observability. | Exact edit position, output ownership and retained state determine when the receipt adds information versus computational convenience. Analyze these distinctions before inference. |
| Difference array | A complete correct difference vector plus any unaffected raw-value anchor reconstructs the original array. Under the PS each peer has multiple current own records, so such anchors often exist. | The receipt can make repair easier under bounded reasoning even where it is information-theoretically redundant. Do not call this a universal insufficiency theorem. |
| Distributed sort | A complete old sorted multiset plus old/new values permits a multiset update; a peer owns only a rank segment. Shifted boundaries can still require remote values and communication. | Distinguish complete-output algebra from the actual per-peer state. Receipt utility may concern coordination and identifying a removed member, not a general closed-form local repair. |
| BFS | If the tombstoned record ID or visible deletion payload identifies endpoints, the old edge is already known. Distances alone do not encode alternate paths. | Freeze the source-ID/tombstone schema. If endpoints are already exposed, this family is a factual-redundancy control. No free shortest-path solver belongs in the receipt. |

These arguments do not predict the model's outcomes. They prevent incorrect explanations of those outcomes. A runtime-observable literal old number is not enough to establish that the transition is reconstructible: repeated numerical values can appear for unrelated reasons. Prefer source-bound occurrences and exact mathematical checks over unqualified string matching.

### Attack: the extension benefits the baseline more

There is no reason the reset arm must gain most. B retains candidate aggregates; C removes them. Before/after information may let B update useful old work while C still needs fresh computation. A negative eta_1 can therefore be the interesting finding. Selecting the extension because an early pilot shows a favored sign would undermine the experiment.

Do not condition the primary analysis on correct old answers. Correct-prefix strata are scientifically useful because the algebra assumes correct old statistics, but they remain secondary, defined before intervention. Wrong retained candidates can turn a correct arithmetic update into a wrong new answer.

### Attack: the primary PS contrast was never invalid

The original study explicitly estimates the total effect of clearing derived history while preserving current sources. Historical information lost with that state is part of its defined treatment. The receipt addition refines the interpretation and tests an operational alternative. It must not be sold as discovering that the original matched comparison was confounded or scientifically unsound.

### Attack: the budget buys an underpowered interaction

The six families are not exchangeable opportunities for arithmetic incremental repair. If an effect of 0.30 appears in only two families and is zero elsewhere, the equally weighted mean is 0.10. That dilution is appropriate for a six-family estimand, but it makes a small study unlikely to support a universal principle.

At 36 worlds there are only six per family. Under the PS's illustrative normal approximation, an interaction with world-level SD 0.35 needs approximately 0.16 for 80% power; SD 0.60 gives approximately 0.28. Those are references for a proposed full-36-world extension, which is not the final preferred design. In the preferred focused extension, **16 focal worlds** have corresponding sensitivity references of approximately **0.245 and 0.420**; **12 focal worlds** give approximately **0.283 and 0.485**. These are sensitivity calculations, not measured variances or promised detection limits. Matched branches do not make agent-round coordinates independent samples.

Prefer an explicitly descriptive eta_1 balanced over **the two focal families**, show its component contrasts and uncertainty, and prespecify an algebra-motivated prefix-sum prediction without a second collection of significance claims. Eta_A remains a descriptive trajectory companion rather than a second target to choose after inspection. The focal set is fixed by task before inference, not chosen by correct prefix, old-value absence or a favored treatment effect. It cannot support a six-family receipt claim. A broad null does not refute conditional algebra. A wide interval establishes neither equivalence nor that the addition is useless. It may simply show that the added branch was too expensive for the information gained.

### Acceptance / rejection criteria

Accept this as the main **additional scientific dimension** only if:

- the after-only versus before/after difference is real under the frozen schema;
- a no-oracle runtime can produce both receipts;
- sufficient prefix competence and compliant receipt use are feasible under the existing bounded pilot;
- the analysis states the difference between information sufficiency and computational help;
- complete matched branches fit without exceeding the GPU ceiling or deleting essential controls;
- the eventual thesis can state an interpretable result even when the receipt is redundant or harmful.

Drop or demote it if receipt information is already derivable in every relevant realized state with no meaningful bounded-computation question; if a same-information wording control accounts for the apparent benefit; if the extra matrix forces incomplete pairs or loss of sham controls; or if the result would amount only to “a longer, more explicit correction sometimes helps.”

## 2. Conservative exposure selectivity

### Strongest proposed claim

A runtime can record which source versions and peer outputs were visible to each call without pretending to recover hidden semantic dependencies. Use the actual temporal exposure graph to quantify how much derived history a conservative recovery policy would exclude after the selected edit.

### Reduction: REVISE plus a coarse read set

[REVISE](https://arxiv.org/html/2609.00643v1), §3, already invalidates readers and descendants, treating incomplete/coarse provenance conservatively. If the invocation reads an entire prompt, the conservative read set is broad. The proposed cone rule is a specialization of that algorithm. [ESC-CR](https://arxiv.org/html/2609.26072) already expands ambiguous responsibility to visible inputs and reconstructs an allowlisted recovery context. [APPA](https://arxiv.org/html/2607.24625v2) addresses broad information-flow restrictions through context isolation.

There is no defensible first algorithm claim for “trace exposure and reset descendants.” Give an established policy the same observable graph and it can make the same retention decision.

### Reduction: familiar propagation and dependence explosion

[Reliability–Contagion Feasibility](https://arxiv.org/html/2607.21912) studies correction-aware network propagation; [NeuroTaint](https://arxiv.org/html/2604.23374v1) distinguishes recorded paths, content transfer and hidden control influence; [trace contamination analysis](https://arxiv.org/html/2604.27586) separates structural divergence from task correctness. A new phrase for information spreading after collaboration does not create a new phenomenon.

The remaining possible contribution is specific: natural PS traces may show that a rigorously observable conservative policy has little useful selectivity by the actual correction point. This requires executed traces. A dense toy graph only establishes a possibility.

### Attack: incomparable units manufacture over-invalidation

The fraction of exposed calls/messages and the fraction of changed gold coordinates measure different objects. A large cone and small output footprint do **not** prove that all removed reasoning outside the footprint was semantically unaffected or useful. Do not divide one by the other and call the result unnecessary invalidation without a justified mapping.

A valid same-unit diagnostic can ask how many *typed candidate coordinates* were correct before the change, remain gold-correct afterward, yet belong to a conservatively exposed candidate. That establishes extensional answer preservation, not validity of the associated rationale. Keep these distinctions explicit.

### Attack: clean records retain selection effects

Even if source values are independently authenticated, which records reached a peer may depend on prior reasoning and the old source. C retains that selected evidence. Removing a derived-history cone while retaining the same source table therefore does not produce the never-exposed counterfactual. This is acceptable for current-world recovery, but kills any broad noninterference/unlearning guarantee.

### Attack: saturation makes the new arm unnecessary

If the conservative cone covers every retained derived object, cone-reset equals C. That equality can be established from the saved prefix before spending inference. If no eligible history remains in most worlds, an extra cone-reset arm mostly pays to resample C-like prompts. Retain the zero-call diagnosis, not the redundant policy arm.

If a selective arm does retain history, it also changes context length and content. It must beat simple retention-volume controls before claiming that graph placement caused any accuracy benefit. That additional control can consume the supposed simplicity advantage.

### Verdict

**Keep as descriptive CPU analysis by default.** It uses already planned logs and can explain why a selective policy is or is not worth implementing. Promote it only if natural traces contain meaningful variation and the analysis tests something beyond transitive reachability. Do not elevate an observational association into an empirical law of recovery difficulty or a causal effect of communication topology.

## 3. Candidate-only typed retention

### Strongest proposed claim

Preserve a peer's last typed candidate while clearing explanations and other derived history. This provides a middle state between B's complete history and C's source-only reset, potentially retaining computational value with less stale discourse.

### Reduction: answer-only communication / compressed working state

[ICR](https://arxiv.org/html/2610.01042v1) already compares answer-only and full-reasoning communication under frozen initial trajectories with a no-message control. The adaptation differs through private shards, several communication rounds and a real source edit. Those are valuable environmental differences, but answer-only versus rationale retention is not a new representation principle.

### Causal and scientific weaknesses

- The candidate is both a useful result and a possible source of anchoring. Removing the rest of history changes amount, content and intermediate-work availability together.
- A wrong candidate is not rescued by giving it a typed schema. Old-prefix correctness must remain a pre-treatment diagnostic, not an inclusion criterion.
- For maximum and some arrays, the candidate already encodes old source information; candidate retention can interact with the receipt factor. Adding both without adequate factorial controls creates a large matrix.
- An agent's own candidate is not the same object as all peers' candidates. Revealing previously unseen peers' outputs would change information access.
- The PS's task outputs differ greatly in size and information content. One scalar max and a full difference vector are not uniform compression levels.

### Verdict

**Useful optional diagnostic; weaker central addition than the receipt factorial.** It becomes attractive if the main result demands a concrete low-cost compromise, but should not be included simply because it sits between B and C. A candidate-only policy that matches B or C may be informative; the sample and context controls still need to earn their costs.

## 4. Completion/search reopening

The complete comparative review is [COMPLETION_COMPETITOR.md](reviews/COMPLETION_COMPETITOR.md).

### Reduction: represent completion as an ordinary control node

A node reading objective version and domain membership is invalidated when those change; descendants are revisited and independent facts remain. That is within REVISE. A closure decision can also be a repairable artifact. Classical incremental search and dynamic constraint maintenance already reopen regions after their exclusion reasons fail.

[TRACE](https://arxiv.org/html/2609.33517v1) further occupies obligation-aware admission, while [Commitment Hierarchies](https://arxiv.org/html/2609.37453v1) and [GitHarness](https://arxiv.org/html/2609.36789v1) study salvage under requirement revision. None automatically proves open-world search completeness; equally, adding a completion status does not do so here.

### Attack: enforcement is just forced extra acquisition

If a reopened obligation requires a current query, the method obtains information that the control might not seek. That can be a useful operational policy, but the observed gain is not automatically a superior reasoning-state representation. A matched-observation control and an equal-opportunity generic reconsideration baseline are mandatory for a stronger claim.

### Attack: the benchmark is rebuilt to make the mechanism necessary

The PS keeps peers active after correction, provides source records without a new query tool, and already asks for continued candidates. Natural stopping omissions are not guaranteed. A new retrieval-controlled adapter may expose them, but replaces much of the existing empirical object. Selective scope additionally needs metadata that may be incomplete, unobserved, or nearly as expensive to verify as reopening everything.

### Verdict

**Do not select as the main direction on present evidence.** It remains a credible separate study if natural omissions and nontrivial acquisition costs are demonstrated. Its known reductions and larger scope burden make it a worse first choice than a focused addition to the PS.

## Budget adversary: novelty must not consume the original study

| Main schedule | Scheduled calls | What must be admitted explicitly |
|---|---:|---|
| Original 48-world PS | 5,856 | Original target, no added receipt arms |
| Original 36-world fallback | 4,488 | Original fallback, no added receipt arms |
| **Preferred 48-world core, receipt on all prefix/sort worlds** | **6,368** | Keeps 48 core clusters; eta has 16 focal clusters; 24-main-hour threshold about 13.57 allocated seconds/call |
| **36-world core fallback, receipt on all prefix/sort worlds** | **4,872** | Keeps the complete original fallback; eta has 12 focal clusters; threshold about 17.73 seconds/call |
| 36 worlds, BΔ/CΔ on all 36 | 5,640 | Loses 12 original base-world clusters relative to the preferred 48-world core; about 15.5% larger standard error for theta if variance is unchanged |
| 48 worlds, BΔ/CΔ on all 48 | 7,392 | Fits 24 main hours only below about 11.69 allocated seconds/call, before extra overhead |
| 36 worlds, receipt diagnostic on 24 | 5,256 | Eta is a smaller prespecified paired subset; complete family balance is possible |

One receipt pair is 32 calls per prefix. Adding it to all six development worlds would raise the pilot from 588 to 780 calls and exceeds the separate three-hour development allowance at 15 allocated seconds/call. The final bounded alternative adds it only on the two predetermined **prefix-sum and sort** development worlds, giving **652 pilot calls**, or **676 including the 24-call smoke allowance**. At 15 seconds/call this is about **2.82 hours**: arithmetically possible but still conditional on measured allocation and overhead. These are feasibility thresholds, not timing forecasts. Infrastructure failures, rejected configurations and smoke attempts still count.

Choose schedules from measured timing and scientific coverage, before main outcomes. The mere fact that 36+receipt uses fewer calls than original48 does not make it a free improvement. It reallocates independent worlds into extra within-world contrasts. Conversely, preserving48 regardless of timing is not mandatory: the PS already permits36. The final specification must state why the added dimension justifies the precision tradeoff.

**Preservation-first ranking:** prefer 48-core plus the focused receipt contrast when the complete schedule fits. If the core itself requires36, admit the focused 36-world extension only when it also fits. If 48-core fits but 48-plus-receipt does not, do not automatically reduce the main sample to36 merely to purchase an exploratory interaction: the preferred conservative choice is 48-core plus the mathematical/trace analyses unless an explicit scientific-value review justifies that trade. Focused receipt runs are more coherent than an all-six factorial because the selection follows known representation/ownership questions while preserving the primary study; they are still an exploratory, large-effect diagnostic.

## Minimum credible claims before and after execution

**Before execution:** “We propose a matched extension testing whether the effect of reasoning retention depends on the historical information supplied with a correction. Established transition representations motivate the intervention; exact task algebra identifies where information is redundant, reconstructible or incomplete.”

**After informative execution:** state the measured interaction and its boundaries, report the original theta alongside it, and distinguish earlier correct responses from an inferred incremental-repair mechanism. A precisely bounded eta_1 null establishes immediate retention-contrast stability only; eta_A is the mandatory trajectory-level companion. Preferring the simpler interface additionally requires bounds on the direct receipt effects, harms and costs, since a zero interaction can conceal equally large benefits in B and C.

**Claims unavailable from this investigation:** first recovery algorithm; solved semantic provenance; universally sufficient change receipts; hidden-state erasure; optimal reuse; universal communication-contagion law; proof that history retention is always helpful or harmful.

## Conditions under which no addition stronger than the PS survives

1. Every plausible mechanism reduces to known recovery given the same observations, and its empirical adaptation offers no clear additional question.
2. Receipt information is universally redundant under the actual schema, with no nontrivial bounded-computation hypothesis beyond prompt wording.
3. A small matched-format control captures the full receipt effect while eta_1 is both negligible and precisely bounded; eta_A and the trajectory diagnostics supply no other useful boundary finding.
4. Natural exposure graphs supply no meaningful selective middle ground, so cone-reset equals C, while descriptive saturation adds no explanatory result beyond protocol construction.
5. Candidate-only retention adds no useful quality/cost distinction, or its apparent gain comes from revealing previously private outputs.
6. Completion reopening needs oracle scope or newly manufactured search behavior, or generic reconsideration obtains the same result.
7. The original capability/protocol gates fail, the extra branches cause incomplete matched coverage, or the fixed budget cannot support an interpretable study.

In those cases, the scientifically stronger choice is the original controlled generalization study, with transparent limits and richer descriptive analysis. Keeping an excellent design is preferable to claiming originality from a renamed known mechanism or an underpowered extra matrix.
