# Cross-field inventions and failed translations

Status: research synthesis, 4 October 2026. This file develops distinct additions to the existing PS. It does not replace the PS or prescribe a new runtime. Source IDs refer to [primary-source notes](sources/CROSS_FIELD_SOURCES.md). Algebra and examples below are this investigation's deductions, not claimed new mathematical theorems.

## Most promising translation: an obsolete value can still be useful historical evidence

**Original abstraction.** Change-data capture and incremental dataflow distinguish the current record from the before-image used to update a materialized computation [X3, X5, X6]. A value being obsolete does not erase its valid role in describing what changed.

**PS consequence.** The source table replaces version 1 with version 2; the old version survives offline, while raw source tables are not duplicated in history. B may nevertheless retain the old numerical value in peer prose or previous replies. C clears that prose as well as the candidates. Thus B and C have identical *current* source tables, but they need not contain equal information about the transition. Their difference remains a valid retention-policy effect. It is not solely a choice about obsolete deductions: a piece of seemingly stale text can carry useful, historically correct input data.

That is an interpretation boundary, not a defect invalidating the existing experiment. The PS already warns that C–B is a content-and-context package. The added scientific opportunity is to identify one concrete part of that package without inferring hidden semantic dependencies.

**Minimal capability.** An authoritative change receipt can state the changed record, version 1 value as historical, version 2 value as current, and replacement/deletion status. It never marks a candidate correct, reveals a gold output, identifies D/U coordinates, or decides what to recompute. Its data already exist in the host's audit trail. Historical fields must stay out of the current source table and must not be forwarded as current facts.

**Question.** Does explicitly supplying the transition change the relative value of retaining collaborative history? A receipt could make useful summaries easier to adjust, make obsolete premises more salient, or have no effect. Each outcome is interpretable.

**Where transfer breaks.** A database operator has defined delta semantics; an LLM may misunderstand the receipt, continue copying the old value, or hold an incorrect summary. Neither version tags nor a correct old/new pair guarantee correct adaptation. It is also inappropriate for privacy erasure, where disclosure of the old value may itself be forbidden. The PS concerns ordinary announced factual correction, so that separate requirement should not be imported.

**New contribution, if supported.** A controlled finding about *which historical information makes reasoning reuse useful or harmful in an opaque distributed team*. The mechanism is ordinary change-data capture. The possible contribution is an operational boundary of retention experiments and a cheap runtime interface with measured value. Do not claim invention of deltas, historical evidence, or information-ablation controls; CIR already uses the latter [X12]. StateAuditor also uses explicit previous/current state transitions and matched controls [X14], so even “transition-aware agent repair” is too broad a novelty claim.

### A precise indistinguishability example under the existing payload

Take a Prefix Sum peer owning positions 8–15. Its seven unchanged records at positions 9–15 are all 1. At recovery start, position 8 is 5. It has not acquired sources from the previous shard and retains only its correct old local candidate, `[14,15,16,17,18,19,20,21]`.

- In world W1, the preceding-shard sum was 12 and the old position-8 value was 2.
- In world W2, the preceding-shard sum was 10 and the old position-8 value was 4.

Both worlds obey the numeric range 1–9 and admit eight-record preceding shards. Both have the same new local sources, record identity/version notice, and old local candidate. But the new local candidate begins at 17 in W1 and 15 in W2. No rule seeing only that information can always produce the correct revision. A before-image, or acquisition of the preceding cumulative boundary, distinguishes them.

This proves only the stated **local observation boundary before any new recovery message arrives**. It concerns the first recovery call on its fixed start-of-round view. Other peers, fuller history, or already acquired raw evidence can supply the missing information; subsequent communication may remove the ambiguity. It does not say a distributed team is unable to recover without a receipt or impose a four-round impossibility.

**Executed CPU witness, October 4.** Constructed full arrays with W1 first shard `[5,1,1,1,1,1,1,1]`, W2 first shard `[3,1,1,1,1,1,1,1]`; old position 8 respectively 2 and 4; every position 9–31 equal to 1. A transient Python accumulation check returned the common old segment `[14,15,16,17,18,19,20,21]`, and new segments `[17,18,19,20,21,22,23,24]` and `[15,16,17,18,19,20,21,22]` after setting position 8 to 5. All 32 values satisfy the PS range. This is a verified constructed witness, not a model run or representative-frequency claim.

### Small decisive experiment

Retain B/C and add BΔ/CΔ from the same prefix, with identical current tables and four recovery rounds. The added branches receive an authenticated before-image as well as the normal after-image. Let `a[p,1]` be the fraction of four peers with an entirely correct candidate in the first recovery round. The sole focused secondary interaction is

`eta_1 = (a[CΔ,1] - a[BΔ,1]) - (a[C,1] - a[B,1])`.

Negative eta_1 means the historical receipt has a more favorable first-round effect under retained history than under cleared history. Both direct effects could still be harmful, so a practical benefit requires examining `a[BΔ,1]-a[B,1]` and `a[CΔ,1]-a[C,1]` separately. This endpoint matches the local pre-new-message boundary: newly generated messages are committed only after all first-round calls, so they cannot repair missing inputs for those same calls. It does not prove that a hidden chain of thought used arithmetic deltas.

Continue all four rounds unchanged. The mandatory descriptive companion is `eta_A = (A[CΔ] - A[BΔ]) - (A[C] - A[B])`, using the original four-round AUC. Together with the full round-by-round curves, it describes whether the relative effect persists, fades, reverses, or cancels in the aggregate. Eta_A alone cannot distinguish those trajectories. Report both direct receipt effects and corrected-world C–B contrasts for both endpoints; preserve the original six-family change-versus-sham theta as the **only primary estimand**. Eta_A was considered as the focused endpoint earlier in this exploration; the final design assigns that role to eta_1 and retains eta_A descriptively, without selecting the better-looking endpoint after outcomes.

A demonstrated direct first-round benefit means more correct responses before new recovery messages arrive. Avoided communication or recomputation is a possible explanation requiring corroborating traces; salience or attention can also explain the behavior. A near-zero eta_1 concerns only the immediate retention interaction, with eta_A evaluated separately. Moreover, both B and C could benefit substantially and equally, giving a zero interaction. Neither zero interaction makes receipts unnecessary without the direct effects, costs and uncertainty.

Because implementation is not frozen, the after-only and before/after notices can share the same schema and wording. The after-only historical field must say **“not included in this receipt”**; it must not claim the old value is globally unavailable or unknowable, since retained history may contain it. Use neutral token-matched padding if needed. Never fill the control with a false old number. This lets existing B/C supply the controls and requires two new branches. Padding controls length, not salience, authority cues or attention. If original notice rendering is already frozen when implemented, use separate matched after-only controls; do not silently overwrite an existing treatment.

An initial possibility was a balanced six-family subset. The adversarial review below rejects that as the preferred live design: several families contain strong redundancy cases, so a pooled interaction would be diluted and difficult to interpret. The final focused allocation is **all existing main Prefix Sum and Distributed Sort worlds**, selected before any model outcome: 12 clusters for the 36-world core, or 16 for the 48-world core. Both new branches require 384 or 512 extra calls. At illustrative 10/15/20 allocated GPU-seconds per call these cost 1.07/1.60/2.13 or 1.42/2.13/2.84 aggregate hours, before margins. No such speed has been measured. Receipt rendering, invariants and analysis plausibly require several focused implementation days, not a new framework; this is a planning judgment.

The complete main schedules become 4,872 or 6,368 calls. Adding both receipt branches to the two existing Prefix Sum/Sort development worlds adds 64 pilot calls, for 652 before the existing at-most-24-call smoke test. The same three-hour development cap and thirty-hour aggregate ceiling apply. The extension earns no extra allocation and cannot remove original sham arms, families, or protocol validity gates to fit. With 24 hours for main inference alone, average allowable allocated time becomes about 17.73 or 13.57 seconds/call, before further overhead. The pilot remains necessary.

**Budget priority:** first determine which intact original schedule fits. If the original 48-world core fits, preserve it and append the extension only when the combined schedule fits. Never reduce 48 to 36 merely to fund this exploratory interaction. The 36-world extension is available only when the original PS's budget rules already select the 36-world fallback. If added development cannot fit the existing allowance, retain the original pilot and deliver the CPU/trace analyses without a live receipt extension. See [final budget decision order](FEASIBILITY_AND_VALUE.md).

Estimate eta_1 and eta_A with world-level pairing and equal weighting of the **two prespecified families**; do not label either an average over all six. Preserve the original six-family primary theta. With only 12/16 clusters, precision is limited: for the chosen endpoint's own paired SD, the rough 80%-power normal approximation `2.8*SD/sqrt(n)` gives about 0.28/0.245 if SD=0.35 and 0.485/0.42 if SD=0.60. These are generic sensitivity calculations, not measured endpoint variances or power. The first-round choice is motivated by identification, **not a claimed power gain**. If every world's later-round interaction is zero, then eta_A=eta_1/4 and its SD scales by the same factor, leaving the standardized effect unchanged. Wide intervals and nulls are acceptable outcomes; no positive-effect pilot gate is allowed.

Use numeric tasks for the strongest historical-value test. BFS requires a separate audit of whether a tombstone or stable edge ID already identifies the deleted endpoints; if so, its receipt adds no missing semantic content and is a natural boundary case. Do not count metadata repetition as an additional information treatment.

**Strong rival:** retain the latest typed candidate without prose, under the same historical receipt. This may preserve nearly all useful work. Its generic form is crowded by ICR and earlier artifact-reuse systems; do not add it merely to obtain a new algorithm. A second rival is the original C: if straightforward recomputation is already cheap and reliable, explicit historical evidence may be unnecessary.

**Claim-specific falsifiers:** if the old value is always already available or provably reconstructible, abandon the claim that receipts resolve missing information; the receipt interface could still alter attention or reasoning cost. If useful summaries never exist, abandon a summary-adjustment explanation. Equal effects under a matched redundant-value or wording control would weaken a semantic-content explanation, but that stronger control is not included in the minimal budget and must not be described as executed. Abandon a practical default-receipt recommendation if harmful old-value copying outweighs benefit. Reject a deployable mechanism claim if benefits require evaluator-selected correct artifacts, special delta formulas unavailable to normal peers, or extra unseen *current* sources.

Distinguish **representational necessity** from **easier access to already derivable information**. Even when a before-image can be reconstructed from a candidate, the receipt may reduce cognitive work or highlight the edit. Such an effect is valid but must not be described as removing an information-theoretic impossibility. A CPU observation audit can expose this before inference. It may justify dropping the addition on scientific grounds before main execution, but must not be tuned to choose favorable worlds or retain only correct prefixes.

## Second translation: update sufficiency rather than output footprint

**Original abstraction.** Self-maintainable materialized views can be updated from the view and specified changes; other views need auxiliary data [X1, X2, X4]. This is older than LLM agents. Its useful transfer is a benchmark criterion, not an algorithm invention.

For deterministic task f, retained summary S, and fully specified edit d, say that S is update-sufficient on a domain if there exists u with `u(S(x),d)=f(d(x))` for every valid x. Equivalently, any two worlds with the same S and d must have the same revised output. This elementary equivalence is an observation-model fact. When S is a model-produced candidate, the property is conditional on the candidate being correct; that condition cannot be certified by a runtime merely by trusting the candidate.

| Task / retained view | With correct old view and authenticated old/new edit | Important limitation |
|---|---|---|
| Prefix Sum, each local output segment | Add the numerical delta to local coordinates at or after the edited position | Without the old value, a peer's first boundary can be ambiguous as above |
| Difference Array, full required vector | Add delta to coordinate k and subtract it from k+1, omitting endpoints outside the output | If old value is absent, a full correct difference vector plus an unchanged current raw anchor can reconstruct it; simple labels must account for this |
| Distributed Sort, **union** of all correct segments | Delete one copy of old value, insert new value, sort/repartition | A single peer's segment is not sufficient near changing rank boundaries; collective sufficiency does not imply locally available information |
| Global Max, old maximum | An increase can sometimes be resolved directly; lowering the unique winner generally loses the runner-up | PS main edits intentionally choose the latter regime. Do not leak that selection predicate as a runtime hint |
| Top-K, old top-K list | Some increases are maintainable; lowering a selected value below cutoff generally needs an omitted replacement | Selected old values and duplicate multiplicities matter |
| BFS, old distances | Generally insufficient after deleting an edge | Old distances omit alternative-path structure; exact current graph access can resolve it |

**Counterexample separating footprint from missing information.** Maximum changes one output coordinate but lowering the winner may require a previously omitted runner-up. A prefix edit may change 31 coordinates, yet a correct prefix vector plus a scalar delta determines all of them. Therefore the count of changed output coordinates cannot alone bound the missing information needed for recovery. It also cannot predict LLM difficulty: emitting 31 corrected coordinates may still be harder than recomputing one maximum.

**Executed BFS witness.** On nodes 0–11, let G1's four core edges be `(0,1),(0,2),(1,3),(2,3)` and G2's be `(0,1),(0,2),(1,3),(1,2)`. Add the same twelve edges to both: `(0,i)` for i=4 through 11 plus `(4,5),(6,7),(8,9),(10,11)`. Both are connected twelve-node/sixteen-edge graphs in the support of the PS tree-plus-five-nonedges construction. A CPU BFS check returned the common old vector `[0,1,1,2,1,1,1,1,1,1,1,1]`. Delete the same edge `(0,1)`: the new vectors are `[0,3,1,2,1,1,1,1,1,1,1,1]` and `[0,2,1,3,1,1,1,1,1,1,1,1]`. Therefore even a complete correct old distance vector plus an explicit deleted edge does not determine the new vector. This is an output-view counterexample; additional visible graph sources may distinguish the worlds.

### Why the receipt experiment is targeted rather than six-family

| Family | Is the before-value missing information under an ideal correct retained output? | Scientific implication |
|---|---|---|
| Maximum | In the actual main-edit distribution, the changed value is the unique old maximum, so the old correct scalar determines it. Models are not told that edit-selection predicate | A receipt primarily makes a relation explicit or reduces reasoning burden; do not claim necessary new information |
| Difference Array | Full old differences plus any unaffected current raw value determine the old array, and each peer has unaffected own records | Before-image is theoretically redundant in that ideal view; retrieving it may still cost model computation |
| Prefix Sum | A peer can reconstruct an interior owned old value from consecutive old prefix entries, but remote edited values and some shard boundaries remain unidentified | Strong natural distinction between local reconstruction and distributed acquisition; the live addition targets this family |
| Sort | Full old multiset lacks source-ID correspondence; each peer additionally lacks other output segments. Before-image identifies which value to remove but does not solve rank-boundary transfer | A contrasting limitation: receipt may help while coordination remains necessary; include this family without assuming a positive result |
| Top-K | The changed old value occurs in the old list but its source identity may be unknown; the missing replacement can remain outside the list | Historical identity and omitted frontier are separate bottlenecks; useful formal case, weaker clean live receipt test |
| BFS | Depends on whether the deleted endpoints are already encoded in the notification/ID; full distances still omit alternatives | Freeze schema before classification; do not manufacture an information gain through an arbitrary tombstone encoding |

This table does not classify unconstrained free-text histories as sufficient or insufficient. It analyzes explicitly stated views. It also distinguishes information content from information easy for a bounded model to use.

**Clean within-task distinction.** Compare upward and downward revisions of the same max/top-K record with chosen numeric constraints and the same prefix. However the required output, edit magnitude, and need for replacement evidence differ. It is a controlled *edit-direction package*, not an isolated causal effect of abstract sufficiency. A stronger benchmark construction matches these where possible; there is no free cross-task causal law.

**Why not the main invention?** A CPU solver can demonstrate these properties, but that only reproduces classical incremental maintenance. A model experiment must test whether this criterion explains retention effects beyond prefix quality, evidence coverage and output length, or identifies a failure case in which extra retained history is provably uninformative. With 36–48 worlds, a many-covariate prediction law is not credible. Use a small prespecified stratification or formal explanatory table. This is strongest as theory supporting the receipt experiment.

## Third translation: conservative dependence can destroy selectivity

**Original abstraction.** Recovery lines in message-passing systems and broad read sets in build systems protect against unrecorded effects [X8; prior workspace adjacent-field sources]. A model call exposed to a revised source and later messages can be treated conservatively as potentially dependent, without pretending a citation graph is complete.

**Question.** After four rounds of useful collaboration, how much derived history remains outside the source's temporal exposure cone? Does selectivity collapse even when only a few gold coordinates change?

**Real contribution possibility.** A measured boundary showing when runtime-complete observation is too coarse to support useful fine-grained recovery. A CPU analysis of actual prefix logs adds zero inference; a selective arm is earned only if meaningful safe-looking state remains. It must compare against random deletion matched in retained volume and a simple recency filter before claiming that reachability is useful.

**Analogy break.** Under complete logging, absence of an exposure path can bound possible dependence of the specific derived objects represented in the graph. This is not full counterfactual noninterference: the earlier value may have influenced which still-current sources were acquired, who received them, or their presentation. Presence of a path is not semantic dependence, invalidity, or harm. A resulting filter is familiar taint/invalidation. APPA, ESC-CR, REVISE, PlanFence and NeuroTaint are direct threats; see the recent landscape.

Report call/message/history-object cone sizes in their own units and output-coordinate footprint D in its own units. A large call cone and small D are a descriptive coexistence, not an “overinvalidation ratio,” since they count different objects and no semantic-validity oracle for the history is available.

**Reason to prefer another addition.** With four peers, a four-round prefix and unrestricted messaging, most calls may quickly lie in the cone. The useful result could be a deterministic degeneration finding, but building an extra arm after knowing it equals C would waste inference. Topology or prefix redesign changes the original intervention and must not be slipped in to rescue the hypothesis.

## Fourth translation: fault containment as a property of recovery trajectories

**Original abstraction.** Self-stabilization separates eventual convergence from legitimate-state closure [X7]; fault-containing variants additionally limit transient disruption. MeshHeal applies self-healing language to degraded agents [X11].

**Question.** Does a recovery policy repair affected coordinates by disrupting already-correct, unchanged coordinates, and how long does that disruption last?

The PS already records nearly everything needed. An integrated collateral-damage area over U, with a separately reported worst affected peer, can supplement its pointwise preservation. That is CPU-only and useful for practice. But it is largely another summary of existing PS metrics; it is not sufficient central novelty. Four rounds cannot prove self-stabilization or eventual convergence. A result may be “less transient damage within the measured horizon,” never a general convergence guarantee.

## Fifth translation: revisions as probes of path dependence

**Original abstraction.** Control and dynamical systems distinguish the present input from the trajectory that brought the system there. A source revision x→x′→x can leave state different from a no-change trajectory despite identical final truth.

**Question.** Does a team retain damage or anchoring after a truth-restoring revision cycle? Compare same-final-world histories with equal calls, notices and source coverage. This targets temporal history more directly than a one-time correction.

**Failure of the easy version.** A two-change branch has different opportunities, prompts and acquired evidence from a no-change branch. A difference need not be hysteresis caused by stale reasoning. Context adaptation and iterated belief-revision literature are immediate novelty threats; a search lead already exists for contextual-adaptation hysteresis. A fully matched experiment requires another stage and careful controls. This is an interesting follow-up, but expensive and less clean than the existing one-correction design. Do not make it the core now.

## Sixth translation: online reset schedules and active diagnosis

**Original abstraction.** Restart theory allocates time between continued search and fresh attempts; value-of-information policies allocate diagnostic effort. A simple rule could retain history for one recovery round, then reset if a runtime signal indicates stagnation.

**Critical break.** Luby-style guarantees assume recognizable correct termination [X9]. A SILO runtime sees schema validity and agreement, not exact correctness. A wrong consensus is not a solved instance; the evaluator cannot become the stopping oracle. Fitting a detector or calibrated policy is also crowded by CIR/PoS and is poorly supported by tens of worlds.

Fixed delayed reset is feasible (one 16-call arm per world), but without a discriminating hypothesis it is merely another recovery schedule. Keep as a simple rival only if another candidate needs adaptive timing. Reject it as the core invention.

## Current cross-field ranking

1. **Historical evidence versus current authority**, tested through transition receipts on the existing Prefix Sum/Sort worlds: strongest focused addition found here, conditional on an observation audit and acceptable incremental budget. Its claim is empirical and conceptual, not algorithmic priority. The six-task core remains the main study; the targeted addition has only 12/16 clusters and may be inconclusive.
2. **Exposure selectivity boundary**: strong zero-inference companion and potential empirical alternative; immediate classical/direct-agent reductions must be accepted.
3. **Update sufficiency of retained results**: valuable formal support and benchmark interpretation; not a standalone new theory.
4. **Candidate-only retention**: simple serious rival, but newly published ICR and established artifact reuse sharply weaken novelty.
5. **Path dependence / cyclic revision**: interesting, more experimental disruption and unresolved matching.
6. **New reset router, new validator, universal recovery optimizer**: reject under budget and novelty constraints.

Completion reopening remains a legitimate competitor, but the receipt investigation retains the PS's main question, six tasks, prefixes and all controls with fewer new behavioral assumptions. If the observation audit finds no missing information, narrow the interpretation to presentation or computation rather than manufacturing an information deficit. If that reduced question is not worth the budget, retain the original PS plus the CPU/trace analysis. Never gate admission on the desired eta_1 or eta_A sign.
