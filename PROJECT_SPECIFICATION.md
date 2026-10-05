# Recovering Distributed LLM Teams After Information Changes

**State reuse, historical evidence, and communication effects**

Final authoritative specification · 5 October 2026

This document governs implementation, execution, evaluation, and reporting. It supersedes conflicting instructions in [FINAL_PROJECT_SPECIFICATION_PLAN.md](research/06_final_design/FINAL_PROJECT_SPECIFICATION_PLAN.md), the numbered blueprint, research/addition directories, old configurations, and dependency lists. Those artifacts preserve the design history and supporting evidence; they are not additional requirements.

**Status:** the repository contains SILO source/data audits and deterministic information/update probes. The recovery runner, new state transformations, hardware/capability pilot, main inference, and empirical results remain unexecuted. Existing reference tests do not validate this experiment.

## 1. Research purpose and design

> A distributed team of LLM agents has already performed substantial collaborative work. Previously valid information then changes. How should the team recover while preserving useful previous work without allowing obsolete work to harm the revised result?

Study recovery as a joint decision about **retained evidence, retained computation, and subsequent interaction**. A team may benefit from old calculations, need historical input values to update them, or need alternatives that its previous answer discarded. Resetting one peer can also change what its collaborators receive. The study must explain these tradeoffs, rather than only rank policies by final accuracy.

Use four identical peers with private inputs, one natural four-round collaborative prefix per generated world, one announced source revision, and matched four-round continuations. Target **60 worlds, 12 per task family**; the resource fallback is **40 worlds, eight per family**. All worlds receive the main retention, delivery, restart, and complementary half-team-reset comparisons. Focused historical-information and communication interventions share these prefixes and controls.

| Scientific question | Identifying comparison | Evidential role |
|---|---|---|
| Does clearing derived history help specifically after facts change? | Broadcast retain/reset under revision and sham | Primary θ |
| Does resetting teammates affect a peer whose own initial state is retained? | Complementary reset groups versus all-retain after revision | Primary φ; sham assesses correction specificity secondarily |
| Can a compact old result preserve useful work, and what historical information makes it reusable? | Evidence only, own last candidate, full history; crossed with before-value disclosure on Prefix Sum/Sort | Prespecified secondary estimates |
| When does immediate derived communication help or hinder recovery? | Delay first-round received prose while preserving source delivery, under retain/reset and revision/sham | Prespecified secondary estimates |
| What was repaired, preserved, lost, or propagated, and at what cost? | Exact trajectories, information inventories, synchronization, deterministic references, and repeated continuations | Descriptive explanation and practical guidance |

The two primary estimands answer different questions. θ is deliberately correction-specific. φ is the **direct effect on retained collaborators in the revised world**: subtracting an equally large sham effect would conceal operationally important team interference. Report that subtraction separately. Neither primary result must be positive for the study to be informative.

```mermaid
flowchart LR
    P["Four peers: four rounds of collaborative work"] --> S["Deliver messages; freeze shared prefix"]
    S --> X["Announced source revision"]
    S --> Z["No-change continuation"]
    X --> R["Retained-state and team-reset comparisons"]
    Z --> R
    X --> H["Historical-information comparison: Prefix and Sort"]
    X --> Q["Prose timing: Sort and BFS"]
    Z --> Q
    S --> U["Real answer-preserving edits: fixed subset"]
    R --> E["Four recovery rounds: exact quality, preservation, interaction, cost"]
    H --> E
    Q --> E
    U --> E
```

All interventions are sibling continuations of the original prefix. They are not applied sequentially or crossed into one large factorial. One additional continuation replicate on ten predetermined prefixes checks the stability of the main account.

## 2. Worlds, task structure, and events

### 2.1 Task definitions

Let numeric shard size `m=8`, total length `n=4m=32`, and peer IDs be 0–3. Indices and ranks are zero-based except difference coordinates, explicitly indexed below. Every peer initially sees only its own raw records and public task metadata.

| SILO-derived family | Inputs and required candidate | Answer-changing edit | Scientific purpose |
|---|---|---|---|
| **Top-K, I-09** | Independent uniform integers 0–99; random equal ownership partitions. Every peer returns the descending top ten, including duplicates. | Lower a uniquely occurring value strictly above the old tenth-value cutoff to below that cutoff. | Partial result reuse; a newly needed reserve may be absent from the old list. |
| **Prefix Sum, II-11** | Independent uniform integers 1–9; contiguous shards. Peer i returns global cumulative sums at positions `im … (i+1)m−1`. | Replace one entry with a different in-range value. | A suffix changes; a retained segment can be updated from a historical operand, but peers have different local views. |
| **Difference Array, II-17** | Independent uniform integers 0–30; contiguous shards. Every peer returns the full ordered vector `d_j=x_j−x_(j−1)`, `j=1…n−1`. | Replace one entry with a different in-range value. | At most two coordinates change, yet every peer has a full-output responsibility. |
| **Distributed Sort, III-21** | Independent uniform integers 0–99; random equal ownership partitions. Peer i returns ascending global ranks `im … (i+1)m−1`. | Replace one entry with a different in-range value. | Output ownership differs from source ownership; updated segments can require remote boundary values. |
| **BFS Distance, III-24** | Public nodes 0–11, source 0, 16 unique undirected edges, four per peer. Every peer returns all node distances; unreachable = −1. | Delete an edge that changes at least one distance. | Nonlinear effects and alternatives omitted from old distance labels. |

For BFS, sample a uniform labeled Prüfer tree, add five uniformly sampled nonedges without replacement, then randomly partition edges equally. The initial graph is connected; the edit may disconnect it. This is a declared modified distribution, not the native SILO graph distribution.

The five families supply complementary information and output-placement problems. Global Max remains a CPU illustration of discarded alternatives; Top-K covers that phenomenon more richly in the live study. SILO level is a descriptive label, not a randomized complexity variable. Results are **SILO-derived revision-task results**, not native benchmark scores or coverage of all algorithmic tasks.

### 2.2 Sampling and reproducibility

Generate the complete world/seed manifest before main inference, with disjoint development seeds. Use separate saved random streams for world generation, edit selection, partition assignment, prefix generation, and continuation sampling. Save actual inputs and chosen edits, not only seeds.

Within each family, randomize edited-owner order in blocks of four containing each peer once. Twelve worlds therefore give three edits per owner; the first eight give two each and define the nested fallback. Numeric source ownership and global positions are recorded separately. For each fixed owner:

- Prefix, Difference, and Sort: sample a position uniformly among that owner's records, then a different replacement uniformly in the stated range.
- Top-K: condition generation on at least one eligible record belonging to the owner; choose uniformly among eligible records, then uniformly among legal lower values.
- BFS: choose uniformly among the owner's answer-changing edges; regenerate if none exists.

All Top-K/BFS worlds must also support an answer-preserving edit. Select that edit uniformly over legal record/replacement pairs or removable edges, without constraining its owner to match the main edit. Conditioning on these eligibility rules is part of the study population. Permit at most 1,000 generation attempts per world; record rejection counts and fail explicitly afterward. Reject only violations of these mathematical constraints, never model outcomes.

Run all four prefix rounds regardless of early correctness. The edited v1 record must have appeared in its owner's rendered prefix input. Include every valid generated world, including unsuccessful prefixes. Exposure is not proof of internal use; do not require a citation, successful prefix, or demonstrated model dependence to retain a world.

### 2.3 Events and populations

| Event/comparison | Target / fallback worlds | Selection and interpretation |
|---|---:|---|
| Answer-changing revision and sham; main policies and complementary reset groups | 60 / 40 | All worlds, equally allocated over five families |
| Historical receipt crossing | 24 / 16 | All Prefix Sum and Sort worlds |
| Prose-delay crossing | 24 / 16 | All Sort and BFS worlds |
| Answer-preserving revision | 16 / 16 | First eight Top-K and first eight BFS worlds |
| Extra continuation replicate | 10 / 10 | First two worlds per family |

**Revision:** one record becomes v2, replacing its value or tombstoning its edge. **Sham:** no source changes; all peers receive the same neutral notice to continue solving and submit current candidates. **Answer-preserving revision:** a below-cutoff Top-K value changes without entering the top ten, or a distance-redundant BFS edge is deleted; the exact target remains unchanged. Run B/C/K on this subset. Its empty changed-coordinate set tests avoiding damage after a real update, not repair of a changed answer.

All events start from the original prefix. No live episode contains a second revision. No preserving single-entry edits are fabricated for Prefix Sum, Difference, or Sort. Subsets and partitions are fixed before model output; their overlap is intentional and does not increase independent sample size.

## 3. Common peer protocol

### 3.1 State and visibility

Each peer has separate state containing a current source table, derived history, latest candidate, and validation feedback. Source records have stable ID, owner, version, and raw value or deletion payload. The host owns the full world for delivery and offline evaluation; model calls receive only their permitted views.

Render current sources once per call, outside history, in a fixed order. Initially supply only private records. Peers forward evidence by naming a currently held record/version; the host copies its exact payload to the named recipient. It reveals no unseen record on request and computes no aggregate. Source references and delivery metadata are distinct from free-text messages. Prose, candidates, and proposed aggregates remain untrusted derived work.

History contains prior own replies, received prose, and schema-error feedback capped at 32 tokenizer tokens per slot, with phase/round labels. Feedback describes only the public contract violation and never echoes hidden source values or evaluates answer correctness. Do not append historical raw source tables or resolved source payloads to history. Old raw values can nevertheless remain in model-generated text or candidates; that is part of the retention treatment. Keep the complete raw audit archive offline.

All peers know the source-ID/owner manifest, their output assignments, task definitions, and public array positions or node set. IDs must not encode hidden values or private edge endpoints. At a revision, a persistent public notice names the changed ID, owner, and new version, and invalidates v1 everywhere. Nonrecipients retain only an update-pending marker, not a usable old source. Replacement content is rendered only after its delivery. The notice and any assigned historical receipt remain outside clearable history for the entire continuation.

For BFS, the delivered v2 tombstone identifies the deleted endpoints and deletion status; it does not restore an active edge. The public notice alone does not reveal those endpoints to an unexposed peer. A tombstone counts as a known current record for coverage; an unknown replacement does not.

Hide condition names, branch IDs, subset membership, future edits, gold answers, affected-output masks, and anticipated effects from prompts. Use one generic instruction about current-source authority and historical work. Supply the same short algorithm hint and communication permissions within each task. Hints do not enforce routes or a leader; peers may centralize information. There is no supervisor, external solver tool, semantic dependency extractor, or correctness feedback.

### 3.2 Synchronous rounds and replies

Each round gives every peer one scheduled call on an immutable start-of-round view. Validate all replies, then commit deliveries together for the next round. Invocation order cannot expose another peer's current-round output. After prefix round four, deliver its messages and freeze an immutable snapshot with no pending prefix deliveries. Apply the event and state intervention once, then execute four recovery rounds. All peers remain active throughout; provisional candidates never terminate an agent.

Each reply is one complete JSON object with `candidate` and `send`. Messages contain `to`, optional `source_refs` with record ID/version, and optional `text`. Retain these limits:

| Resource | Limit |
|---|---|
| Total context, including reserved output | 262,144 tokenizer tokens |
| Generated output | 384 tokens per scheduled call |
| Recipients | At most one message per other peer; three total |
| Source references | At most eight distinct references per recipient |
| Prose | At most 128 tokenizer tokens summed over message texts in the reply |

Numeric candidates are JSON integer lists of the task's required length. BFS candidates are JSON objects with exactly the canonical decimal-string node keys and integer distances; key order is irrelevant. Reject fields outside the declared reply/message/reference schemas. The full-information controls use the same outer reply schema with an empty send list and the complete-world candidate length.

Parse strict JSON, permitting whitespace but not code fences, extra prose, duplicate object keys, nonfinite numbers, or truncated fragments. Enforce candidate integer types, lengths, and coordinate keys; reject booleans as integers. Enforce recipient/reference permissions and payload caps. Numeric answer errors are scored, not repaired. A protocol-invalid reply produces no messages and no valid candidate, even if a candidate field looks plausible. Supply only schema/permission feedback at the next scheduled call, without an extra opportunity. A complete valid reply that finishes exactly at the generation cap is accepted; record its termination reason separately from actual truncation.

Message text must contain Unicode scalar values after JSON decoding. Valid escaped surrogate pairs are accepted; unpaired surrogates make the entire reply schema-invalid before native prose counting or effects. Preserve the exact raw reply and generated IDs, use bounded message-schema feedback, and never replace, normalize or repair the sender's text. This pre-main clarification resolves the tokenizer incompatibility documented in M2-T06; it was authorized with the selected capacity remedy on 5 October 2026.

An invalid or failed slot never inherits the previous candidate as a new answer. No separate chain-of-thought or support proof is requested. Short peer explanations are allowed inside the prose budget.

The simultaneous maximum prose/reference payload need not fit within 384 tokens. Before GPU use, verify that every candidate shape, useful legal messages, and worst permitted retained contexts fit the declared caps. Do not silently truncate history. The only predefined input-size fallback is in Section 8; further cap changes require a documented pre-main protocol revision and renewed checks for all conditions.

**Authorized pre-main capacity revision, 5 October 2026:** M2-T06 disproved the
original 8,192-token input budget. The selected remedy preserves every retained
own reply and received text in labeled literal blocks, with structural metadata
and delivery/history column tables in one user message. A fixed footer prevents
the native template from stripping final archived whitespace. The uniform limit
is now 262,144 including the unchanged 384 output reserve, within both pinned
checkpoints' native windows; no positional extension is used. The
[complete CPU proof](docs/implementation-research/m2-t06-capacity-proof.md)
bounds the full retained horizon, including invalid outputs and Unicode.
Exact rendered text remains archived separately from native token IDs: the
checkpoint's existing NFC normalizer operates during tokenization, with no host
normalization or answer repair. This changes the input-budget and representation
regime uniformly; populations, interventions and output/prose limits remain fixed.
M5 must establish memory, headroom, capability and timing for this limit before
accepting a configuration. CPU admission does not establish GPU feasibility.

## 4. Recovery interventions and their controls

### 4.1 What each peer retains

For a revised broadcast branch, let E be that peer's acquired source table after invalidating v1 and delivering v2; for sham, E is the unchanged acquired table. B, C, K, and the mixed-team conditions have identical initial E for each peer within an event.

| Policy | Replacement delivery | Initial evidence | Initial derived state |
|---|---|---|---|
| **L: local delivery** | Content only to edited owner; public notice to all | Acquired current records; replacement absent until received | Retain history |
| **B: broadcast retain** | Content to all | E | Retain history |
| **C: evidence-only reset** | Same as B | E | Clear history, candidates, and validation feedback |
| **K: compact result** | Same as B | E | Retain only own prefix-round-four candidate from a protocol-valid reply, explicitly historical |
| **F: fresh corrected restart** | Same broadcast record as B | Corrected private shard plus revision; discard other acquired remote records | Empty history/candidates |
| **P_G: reset group G** | Same as B | E | C for G; B for H |
| **P_H: reset group H** | Same as B | E | B for G; C for H |

K keeps the actual candidate even when wrong. A protocol-invalid round-four reply yields an absence marker. Never select an earlier/better candidate, repair it, summarize it, or expose another peer's private candidate. After the boundary, every policy accumulates ordinary new history. K is a compact initial state, not continuous compression.

Run **L/B/C/K/F/P_G/P_H under answer-changing revision** and **B/C/K/P_G/P_H under sham** on every world. Use unmodified acquired evidence for shams and the same retention rules. B/C/K after answer-preserving edits are separate siblings.

B−L estimates guaranteed replacement-content delivery after an announced change. C−F estimates acquired-current-evidence retention with derived state cleared. K−C estimates keeping the last output; B−K estimates keeping the additional conversation/intermediate work. C−B is the total effect of clearing derived state with current evidence fixed. These package effects include context length, representation, useful historical information, and earlier evidence-selection decisions; they do not isolate hidden anchoring or semantic erasure. All policies receive equal round/output budgets and the same generic instructions.

### 4.2 Complementary groups: recovery is a team intervention

For each world, independently sample one of the three unordered two-pair partitions uniformly, using a saved pre-outcome seed. Name the pair containing peer 0 G and its complement H. This fixes labels without selecting on correctness, exposure, or the edited owner. Use both complementary masks and the same partition under every event and continuation replicate. Each peer, including the owner, is reset in one mixed branch and retained in the other.

The four cells are `00=B`, `10=P_G`, `01=P_H`, and `11=C`, where each bit denotes clearing its group. They identify effects of other peers' reset while holding the focal peers' initial local state fixed. All main worlds receive these cells; no separate smaller primary population is needed. The experiment does not enumerate all masks or learn which peers to reset.

Hide other peers' reset status. In recovery round one, a retained peer's request must exactly equal its B request and a cleared peer's request its C request. **Replay those exact saved first-round replies**, including invalid replies, into the mixed branch. Assemble the mixed outgoing set before delivery and apply its recipient effects independently. Never initialize a mixed branch from B/C's post-delivery recipient tables. Only rounds 2–4 require new generations.

This sharing is required experimental semantics, not an optional speed assumption. Identical prompts/seeds alone do not guarantee identical stochastic outputs. Verify request, settings, seed, and permitted-state equality before replay; a mismatch is a protocol defect. With replay, first-round equality is a construction check, not empirical evidence that interference is absent. Subsequent differences can arise through source forwarding, prose, routing, and feedback.

### 4.3 Historical information × retained representation

On every Prefix Sum and Sort world, add BΔ/CΔ/KΔ after the main revision. They share the exact current sources and respective retention rules of B/C/K. The six cells cross **full history / own last output / evidence only** with **after-only / before-and-after information**.

The host supplies the genuine archived v1 raw value as a historical field, associated with the changed ID, owner, versions, and already-public position. The current v2 payload is supplied identically in both receipt modes. The ordinary historical field says “not included in this receipt”; it does not claim that history lacks or cannot reconstruct the value. Keep the historical value outside current-source lookup/forwarding.

Use one notice layout and generic instruction. Supply no computed delta, update formula, relevant-output indices, gold, corrected candidate, or additional unchanged source. Record token cost; do not add padding/wording arms. This identifies the historical-receipt interface package, not a pure information or attention mechanism. Some peers may receive a historical value they never previously held; that is the intended information intervention.

KΔ is needed to determine whether a compact actual result plus transition information captures useful work. CΔ controls benefits that also occur without a retained result; BΔ tests whether richer history adds value. Prefix updating can be locally sufficient with the old operand; Sort can still require remote rank-boundary values. Do not select worlds with favorable old summaries or apparent information gaps. No receipt-sham or receipt-preserving factorial is run or claimed.

### 4.4 Early prose availability, with current sources fixed

On every Sort and BFS world, add Q_B and Q_C under both revision and sham. Each inherits B or C, with this sole delivery change:

1. Replay the exact corresponding first-round B/C replies from their pre-delivery barrier.
2. Deliver validated source references and their current records normally before round two.
3. Hold only received round-one free-text prose until before round three. Senders retain their own replies normally.
4. Release held prose before round-two prose, ordered by generation round and sender ID, with stable IDs and generation labels. Continue ordinary delivery thereafter.

Append delayed entries at their actual release boundary; do not reorder the history already seen by a peer.

Do not delay the host revision, drop text permanently, add a fifth round, or announce the queue policy in prompts. Do not expose held text through summaries, validation errors, candidate sharing, or delivery metadata. For messages with sources, render the same source-delivery metadata in both siblings. For text-only messages, introduce no placeholder revealing held content or extra advice.

Before round two, each Q/B or Q/C pair has identical current source tables and own first-round reply. Incoming prose differs. Exact first-round replay is required for that control; independently regenerating round one would not preserve realized source deliveries. After round two, acquisition may diverge as a treatment consequence, so later contrasts are total scheduling effects.

C's comparison distinguishes a general prose effect from dependence on retained old history; shams distinguish ordinary scheduling behavior from behavior after revision. Prose can contain useful facts and summaries. A benefit of delay does not prove that a particular sentence was stale. Report how often text was actually held, including inactive treatments with no prose. Do not condition inclusion on talkativeness or cross these variants with receipt/mask variants.

## 5. Outcomes and prespecified estimands

### 5.1 Exact outcomes

Use independent task-specific gold solvers before/after each event. Preserve order and multiplicity for lists and compare BFS dictionaries on the complete node set. The native generic partial scorer is unsuitable. Gold and scoring stay outside all model-visible execution and stopping decisions.

For world w, policy p, event z, peer i, and recovery round r, let `c[w,p,z,i,r]` be 1 exactly when that scheduled reply is protocol-valid and its entire assigned candidate equals gold; otherwise a recorded failed slot scores 0. An unexecuted slot is unknown, handled in Section 6.

`a[w,p,z,r] = (1/4) Σ_i c[w,p,z,i,r]`

`A[w,p,z] = (1/4) Σ_(r=1…4) a[w,p,z,r]`

A is normalized exact-peer recovery AUC in [0,1]. It rewards earlier correctness over 16 peer-round opportunities without treating them as independent samples. Do not count the reset boundary as an incorrect round. Report final joint completion, defined as all four final candidates correct, alongside A. Agreement on a wrong answer is failure.

Define task balancing as `⟨d⟩=(1/5)Σ_f mean_(w in f)d_w`; use an analogous equal two-family mean for focal comparisons. Main estimates use continuation replicate zero.

### 5.2 Primary 1: correction-specific reset value

`θ = ⟨(A[C,revision]−A[B,revision]) − (A[C,sham]−A[B,sham])⟩`.

Report both component contrasts. Positive θ means resetting becomes relatively more favorable after revision; it does not by itself mean reset improves revised-world performance. A practical reset benefit also requires the direct corrected C−B contrast and its preservation/cost consequences.

### 5.3 Primary 2: effects on retained collaborators

For each event, let `M_G^ab` be mean exact-candidate correctness over peers in G and recovery rounds **2–4** in mask ab; define `M_H^ab` analogously. Define:

`E_keep(z) = ½[(M_G^01(z)−M_G^00(z)) + (M_H^10(z)−M_H^00(z))]`

`φ = ⟨E_keep(revision)⟩`.

Each term compares the same retained peers when their other group is reset versus retained. φ in [−1,1] estimates a benefit or harm to those collaborators after factual revision. Round one is excluded because their requests/replies are identical by construction. It remains visible as the zero-effect reference in trajectory plots.

Prespecified secondary companions are `⟨E_keep(sham)⟩` and the correction-specific interaction `φ_corr=⟨E_keep(revision)−E_keep(sham)⟩`. A shared effect across events is still an operational team effect. Also report effects on already-reset peers:

`E_clear(z) = ½[(M_G^11(z)−M_G^10(z)) + (M_H^11(z)−M_H^01(z))]`.

Show all four mask trajectories, complementary own-group reset contrasts, and average P_G/P_H policy performance. A zero φ cannot rule out effects confined to cleared peers or cancellation among cases. Interpret effects as consequences of teammates' reset through subsequent interaction, not causal attribution to a specific message. Nonadditivity of all-correct team completion alone is not evidence of psychological synergy; that endpoint is nonlinear.

### 5.4 Secondary estimates

| Comparison | Endpoint and purpose |
|---|---|
| C−B, K−C, K−B, B−L, C−F after revision | AUC plus final joint completion: practical state, delivery, and evidence-retention effects |
| K−C and K−B under sham and their revision-minus-sham contrasts | Distinguish compact-state recovery effects from generic context effects |
| `η=⟨(a[KΔ,1]−a[CΔ,1])−(a[K,1]−a[C,1])⟩_Prefix,Sort` | First response: does the receipt increase the relative value of the retained result? |
| Q_B−B and Q_C−C, separately under revision/sham | Round-two accuracy: early received-prose effect with current-source delivery fixed |
| B/C/K under answer-preserving revision | AUC, joint completion, and preservation without any changed target coordinate |

For receipts, show all six first-round cell means, the three direct receipt effects, B-versus-C and B-versus-K comparisons under each format, and four-round AUC/final/preservation companions. Positive η can result from harm to CΔ; a zero interaction can hide equal large benefits. The first-response endpoint matches the pre-new-message information boundary, not a guaranteed power gain. For Q, show subsequent trajectories/AUC and preservation as well as the immediate effect. Early gains need not persist.

These are prespecified estimates with uncertainty, not separate confirmatory tests for every cell, round, or task. The study may support useful mechanisms or simple-policy conclusions without a universal winner.

## 6. Statistical analysis, repetition, and missingness

The independent cluster is the generated world **with its one realized prefix**. Keep all events, policies, peers, rounds, groups, controls, and repeats together. θ and φ both target the equal-weight five-family mixture on all 60 or 40 worlds. The two focal crossings target only their named families. Family-specific estimates are descriptive; these five families are not a random sample of all tasks.

Use 10,000 paired world-bootstrap resamples, drawing worlds with replacement within each family at its observed sample size, with a saved resampling seed. Carry complete sibling records together; analyze each fixed subset within its own eligible population. Preserve common world identities when jointly displaying overlapping subsets. Report **97.5% two-sided percentile intervals for each of the two primary estimands** (1.25th and 98.75th percentiles), giving Bonferroni multiplicity protection to the extent the approximate bootstrap coverage holds. Use descriptive 95% percentile intervals for secondary estimates. Do not claim exact small-sample coverage or add a catalogue of p-values. Show raw world contrasts and family means beside pooled intervals.

When within-family contrasts are constant and bootstrap uncertainty degenerates, additionally report a conservative bounded-mean interval. For independent world contrasts bounded by [L,U], let F be the number of eligible families, use normalized weights `b_w=1/(F n_f)`, and error level α (0.025 for a primary interval). The weighted Hoeffding half-width is:

`h=(U−L) sqrt[½ log(2/α) Σ_w b_w²]`.

Report `[estimate−h, estimate+h]` intersected with [L,U].

Use θ range [−2,2], φ and direct accuracy-difference range [−1,1], and the correct range for each secondary interaction. This bound describes the fixed design under independent world generation; it does not account for unknown systematic implementation errors. Report all-success/all-failure completion counts with appropriate binomial bounds within eligible family populations. Zero observed variation is not population certainty.

Use 0.10 in AUC or mean peer correctness as a practical reporting reference, not a promised detection limit or an automatically valid equivalence margin. With two primary contrasts, a rough normal-approximation 80% power reference is `3.08 × SD(world contrast)/sqrt(N)`: for SD 0.35/0.60 this is 0.139/0.239 at N=60 and 0.170/0.292 at N=40. Focal n=24/16 yields unadjusted references about 0.200/0.245 at SD 0.35 and 0.343/0.420 at SD 0.60. These are sensitivity calculations, not measured power; endpoint variances differ. The fallback increases main standard errors about 22.5% at equal variance. Wide intervals cannot establish equivalence or irrelevance.

**Repeatability.** On the ten fixed worlds, keep the prefix and partition and execute one additional independently seeded continuation replicate of B/C/K/P_G/P_H under both revision and sham, with the same replay rules within that replicate. Replicate zero remains the main analysis; do not replace it or count repeats as new worlds. Display per-world θ/φ/compact-state contrasts across replicates, separating ties from sign reversals, and changes in trajectory categories. Two samples per prefix assess conditional stability, not reliable per-world variance, new-prefix variability, or receipt/Q repeatability.

**Failure and missingness.** Malformed outputs, cap-truncated JSON, recorded timeouts, and exhausted scheduled attempts are zero-credit outcomes. Unexecuted slots are unknown, not demonstrated model errors. Publish scheduled/executed counts and paired coverage. If missing slots cannot be completed, bound their outcomes between 0 and 1 through the estimand and show best/worst sensitivity; preserve shared-response identities when bounding repeated logical uses. Do not present complete-case results as the intended population.

Exclude or regenerate only for an independently verified generator, protocol, leakage, or evaluator defect. Fix it, rerun all affected matched branches, charge the cost, and disclose the deviation. Incorrect prefixes, silent peers, redundant receipts, and harmful policies remain included. Correct-prefix and correct-old-candidate strata are offline, prespecified descriptions with denominators, never runtime admission rules. No outcome-adaptive sample growth, favorable-family replacement, learned threshold search, or endpoint switching is permitted.

## 7. Explaining recovery and deriving practical conclusions

### 7.1 Repair, preservation, and synchronized completion

Map each output to unique task coordinates: ranked positions for Top-K/Sort, global indices for Prefix/Difference, and nodes for BFS. Define evaluator-only `D={j:gold_old[j]≠gold_new[j]}` and unchanged set U. Replicated peer copies are separate responses, not independent coordinates/worlds.

For each round measure new correctness on D; explicit old-gold values on D; and preservation of U coordinates that the same peer correctly answered in its protocol-valid prefix-round-four candidate. Count a newly wrong eligible U coordinate as collateral damage. Changed candidate values on U can instead repair old errors; separate these from harmful changes. Invalid candidates are incorrect for accuracy/preservation but occupy a distinct missing/malformed category for old-value persistence. Empty denominators are not applicable, with counts reported.

Average coordinate rates within eligible peers, then worlds, then equally over eligible families. Publish unique-coordinate and peer-copy counts. A world absent from a diagnostic denominator remains in the main outcomes.

Show peer and team trajectories; first joint correctness; first correctness maintained through round four; and any subsequent regression. “Stable” means stable within the observed horizon. Never average only successful recovery times or assign a failed branch an invented fifth-round time. Classify complete branches as: continuously correct; correct at the end after delay/regression; temporarily correct but incorrect at the end; or never jointly correct. Keep incomplete branches separate.

A **fragmented** trajectory has every peer correct at least once but never all four correct together. Do not combine its best answers from different rounds into an oracle-selected team result. Report valid identical-but-wrong full answers only for replicated-output tasks; differently assigned Prefix/Sort segments do not require identical answers.

Use six nonexclusive observable annotations: protocol/inference failure; v2 not yet available; incorrect after v2 receipt; explicit old-value persistence; collateral error; and regression. Prefix correctness is context. Overlapping labels need counts/intersections, not percentages presented as a partition or speculative psychological causes.

### 7.2 What information and work survived

Show old-gold prefix correctness, acquired remote-record coverage, history tokens, and communication over all four prefix rounds. This operationalizes prior collaborative work without claiming recovery after hours of real tool use or a causal effect of correction timing.

For L/B, align first **usable call-boundary** v2 receipt with subsequent accuracy. Distinguish host injection from generated forwarding, and count no receipt, receipt without subsequent success, same-call success, later success, and correctness before authoritative receipt. Prose or deduction may explain the last category. Do not average successful receipt-to-correctness lags while dropping censored peers.

For C/F, count boundary-held remote current records excluding the host-injected changed record, unique newly acquired record/version pairs, and all delivery attempts. Tombstones count as known records. Raw-source completeness is sufficient for exact fresh recomputation, not necessary; summaries can supply information absent from the raw table. Post-intervention acquisition is an outcome, not a covariate to control away from the policy effect.

For the receipt comparison, annotate explicit source-bound old-value visibility, reconstructibility under a stated correct-candidate assumption, sufficient current raw evidence, and unresolved cases. Numeric-token occurrence alone is not a source association; unresolved does not mean absent. Keep gold-correctness strata offline. Recorded source/message paths can illustrate timing, but do not construct a general exposure-cone analysis or treat delivered paths as complete semantic provenance: absence, routing, and source-selection decisions can also carry influence.

Use the following information atlas to interpret these observations:

| Retained representation | Useful information and limits |
|---|---|
| Maximum, CPU illustration only | Winning value can omit the runner-up needed after demotion. |
| Top-K | Preserves selected values, but may omit the reserve and record-to-value association. |
| Local prefix segment | A correct segment plus old/new edited value determines its update; an after-only notice may leave the historical operand unidentified. |
| Complete differences plus unchanged raw anchor | Correct differences determine the old array up to an additive constant; the anchor fixes it. Before-values need not be missing information. |
| Local sorted segment | A complete correct multiset plus old/new values can be updated, but one peer's segment can lack remote boundary values. |
| BFS distances | Old labels do not determine alternative path topology after deletion. |

The existing CPU witnesses establish update sufficiency or ambiguity for **specified views**, not natural LLM failure frequency or impossibility after further communication. Correct-summary arguments never certify an actual model candidate.

For Prefix/Difference, apply the exact update offline to each actual protocol-valid old candidate, even if wrong. With δ equal to the true input change, add δ to prefix coordinates at/after edited position k; add δ to difference d_k when k≥1 and subtract it from d_(k+1) when k≤n−2. No earlier-candidate backfill is allowed. The residual identity `(candidate+update)−(gold_old+update)=candidate−gold_old` shows how correct updating can preserve earlier errors. Missing/invalid old candidates make this reference unavailable, not grounds to exclude a world. This sometimes privileged CPU reference is never supplied to the model.

Record edit position/direction/magnitude, number of affected output owners, sort segment crossings, and BFS disconnection. Use task-level tables and a few prespecified plots, not a high-dimensional moderator model or a claim that footprint/level causes difficulty.

### 7.3 Quality, retained work, and cost

Keep retained evidence inventory, preserved correct output, and measured computation separate. Unchanged output can be recomputed; retained records can be unused. Report tokens, validated source/text deliveries, call/attempt durations, peak memory, and aggregate allocated GPU-seconds, including failures and assigned idle overhead.

The physical ledger counts a shared prefix or generation once. A hypothetical deployed policy includes its prefix plus **all 16 logical continuation calls**, assigning replayed replies their measured original generation cost. F includes its abandoned prefix. Otherwise replay would make mixed/Q policies falsely appear cheaper. Completing early does not save calls under the fixed schedule; cost to oracle-recognized stable correctness is only retrospective.

Plot paired quality/preservation against policy-accounted cost, with uncertainty. Do not combine them into an arbitrary utility or accuracy-per-message score. Similar point estimates do not establish equivalent quality, and longer prompts do not directly establish a GPU-time penalty without measurement.

Evaluate one frozen descriptive boundary rule from complete recorded branches: **choose C if every peer already holds the complete current record manifest; otherwise choose K**. It uses runtime source/version coverage, including tombstones, not gold or candidate correctness. Select the whole branch and its policy-accounted cost; compare with always B/C/K. Report selection frequencies, and one sentence if the rule is constant. Do not tune it, splice states from different trajectories, or advertise hindsight best-of-policy performance as achievable.

### 7.4 Results narrative and cases

The report should progress through: prior work and task information; recovery-policy effects; repair versus collateral damage; representation × historical information; effects on collaborators; prose timing and synchronization; and practical quality/cost with repeatability and limitations. Combine related panels into roughly seven or eight main exhibits rather than one subsection per candidate addition. Publish family/world tables and detailed traces as supporting artifacts.

Choose at most six matched case cards by a frozen rule: for corrected C−B AUC, E_keep(revision), and KΔ−K first-round accuracy, select the median strictly positive and median strictly negative complete world when each sign exists. Order by effect then immutable ID and take the lower observed median. Merge duplicate selected worlds; report empty sign categories. When all contrasts are zero, use the smallest-ID regression world, or the smallest complete world if no regression exists. Show edits, trajectories, availability, preservation, and necessary unaltered excerpts linked to call/message IDs. Cases illustrate behavior; the full annotation table establishes prevalence.

Interpretation must survive unfavorable outcomes. Equal revision/sham reset effects indicate generic cleanup. A receipt can help both representations equally despite zero interaction. Mixed resets can help one subgroup and harm another. Prose delay can discard useful coordination time. Ceiling performance can still differ in cost or temporary damage; common failure with poor full-information controls is capability-limited. Broad intervals or unstable repeats require an inconclusive conclusion, not a universal policy recommendation.

## 8. Inference configuration and feasible allocation

### 8.1 Model and capability controls

Start with [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B), with [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) as the hardware/runtime fallback. Run text-only, local inference without training. Use Transformers, bitsandbytes NF4 with double quantization, ordinary FP16 computation, and implementation-required FP32 sensitive calculations. Validate the maintained text-only loading path and actual language weights; do not assume multimodal checkpoint loading or optional kernels work on T4.

Freeze `enable_thinking=False`, temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0, and no presence penalty. These use the model's documented non-thinking general-task sampling settings with the deliberate omission of presence penalty because repeated schema keys/IDs are legitimate. The study's short output/context caps are its own bounded-computation regime, not the model card's unrestricted reasoning benchmark configuration. [Official guidance](https://huggingface.co/Qwen/Qwen3.5-9B#best-practices)

Use batch size one, one full replica and serial inference worker per T4, with independent episodes across workers. Four logical peers share weights but have fresh KV/recurrent state per call. Two 16-GB devices are not a unified memory pool. Require finite outputs, no unexplained missing/newly initialized language weights, no CPU offload or cross-device model splitting, and at least 1.5 GiB free headroom at the accepted worst prompt. Expected unused vision weights are distinct from missing language weights. Supported PyTorch attention/recurrent fallbacks are acceptable; no custom kernels or presumed FlashAttention/BF16 support. Record actual device maps, driver, memory, and kernel paths.

Use compatible maintained package versions and pin the complete passing environment, model/tokenizer revision, and templates before main execution. Do not inherit the old proposed version list as a tested lock. Alternative serving stacks and quantizers are outside this execution plan; a required change must be made before freezing and must repeat affected isolation, capability, and timing checks.

For every main world, run two separate one-call full-information controls, before and after its main edit, with all raw sources and the complete mathematical output contract. Use the same model, decoding, output cap, and task hint, with no communication. Prefix/Sort controls return the entire n-coordinate answer. These are capability diagnostics, not budget-matched team competitors or treatment selectors.

### 8.2 CPU checks and bounded development pilot

Before GPU use, implement a **protocol attainability witness**: each scripted peer sends its own current shard to a different peer in each of the first three rounds and computes its answer only after required sources are locally available. Use the existing exact task solvers locally, legal placeholders earlier, and no oracle information unavailable to the scripted peer. Check actual serialized/tokenized payloads for all five tasks, local/broadcast delivery, resets, and prose delay. This proves the horizon/channel permits a correct strategy, not that an LLM can execute it.

Use five disjoint development worlds, one per family. Begin with a load/smoke screen of at most 24 calls and 0.5 aggregate GPU-hour, whichever comes first, including long prompts, output types, forwarding, and a corrected continuation. For a candidate passing it, run:

| Pilot component | Distinct generation slots |
|---|---:|
| Five prefixes; revised L/B/C/K/F; sham B/C/K; before/after full-information controls | 730 |
| Complementary masks under revision/sham on Prefix and BFS | 96 |
| BΔ/CΔ/KΔ on Prefix and Sort | 96 |
| Q_B/Q_C under revision/sham on Sort and BFS | 96 |
| Preserving B/C/K on Top-K and BFS | 96 |
| **Full pilot / including separate smoke maximum** | **1,114 / 1,138** |

Execute the 90 prefix/full-information slots first and check their capability thresholds before spending on recovery branches. The full pilot exercises each transformation; it need not run every main combination. All reused replies are charged once physically. Failed configurations, attempts, and justified reruns consume the same development allocation.

Admission requires: no unresolved leakage/isolation/queue defect; at least 98% protocol-valid distinct scheduled pilot generation slots for the accepted configuration; at least 9/10 correct full-information controls and at least one correct control in each family; at least three of five jointly correct final prefixes and 14/20 correct final prefix-peer candidates; worst-context memory/capacity checks; and a conservative forecast for a complete schedule. Inspect family/condition failures rather than relying only on the pooled validity rate. These small operational screens do not estimate treatment effects or general competence.

If arithmetic/context capability requires it, permit one uniform size reduction to **m=6 numeric records per peer and BFS with eight nodes/twelve edges**. Keep top-ten output, four peers, phase lengths, value ranges, and five extra graph edges. Update every coordinate contract, generator, oracle, witness, and prompt consistently and repeat affected checks. Do not drop a family to manufacture recovery success or select model/phrasing by a favorable effect. If no accepted configuration passes within development resources, stop before main inference and report feasibility limitations.

### 8.3 Exact main schedule

A full continuation has 16 logical calls. Mixed and Q continuations have four replayed first-round calls and **12 new generations**. Prefixes and full-information controls are physical calls. Let `N=60 or 40` and `q=2N/5`, the number of worlds in either two-family focal set.

| Component | Formula for new generations | Target | Fallback |
|---|---|---:|---:|
| Shared prefixes | 16N | 960 | 640 |
| Revised L/B/C/K/F | 80N | 4,800 | 3,200 |
| Sham B/C/K | 48N | 2,880 | 1,920 |
| Complementary masks, both events, all worlds | 48N | 2,880 | 1,920 |
| Full-information controls | 2N | 120 | 80 |
| Preserving B/C/K, 16 worlds | 16×3×16 | 768 | 768 |
| BΔ/CΔ/KΔ, Prefix/Sort | 48q | 1,152 | 768 |
| Q_B/Q_C, both events, Sort/BFS | 48q | 1,152 | 768 |
| Extra B/C/K/mask replicate, both events, ten worlds | 10×(6×16+4×12) | 1,440 | 1,440 |
| **Distinct main generation slots** | Sum | **16,152** | **11,504** |
| **Logical call slots, counting shared uses** | Main generations +16N+16q+160 | **17,656** | **12,560** |

The logical total counts each scheduled prefix once and every continuation's first round separately; per-policy end-to-end cost additionally attributes that shared prefix to each hypothetical workflow. It is not an alternative independently regenerated design. Retries increase actual physical attempts beyond generation-slot counts. No saving assumes early stopping, fortunate output lengths, or extra-prefix selection.

### 8.4 Resource gate and freeze

Use **100 aggregate allocated GPU-hours as the initial total planning ceiling**. Reserve up to eight for development inference, two for loading/setup, and two for necessary interruptions/reruns. These allocations all count toward the ceiling. The complete 1,138-slot pilot/smoke allowance would take 6.32 hours at illustrative 20 seconds/call; actual speed, overhead, and failed configurations may still prevent completion within development resources.

Forecast main cost using measured phase/condition times and prompt lengths, the slower device, allocated idle time, and a 25% margin. Allocate device overhead without double counting it as both per-call cost and setup. A simple illustration is `12 + 1.25×main_calls×g/3600`, where g is allocated seconds per new main generation:

| Assumed g | Target total | Fallback total |
|---|---:|---:|
| 10 seconds | 68.08 GPU-hours | 51.94 GPU-hours |
| 15 seconds | 96.13 GPU-hours | 71.92 GPU-hours |
| 20 seconds | 124.17 GPU-hours | 91.89 GPU-hours |

These are arithmetic sensitivities, not measured feasibility. Use the full reserve in the pre-main conservative forecast; smaller actual spending remains visible in the ledger. Two busy GPUs can shorten elapsed time but do not halve aggregate device-hours. Record provider billing rules separately from physical allocation.

Select the complete 60-world design if the accepted model and forecast fit, otherwise the complete 40-world design. Prefer capable 9B/40 over changing models solely to obtain more worlds. If 9B cannot satisfy hardware/runtime gates, test 4B within the same development limit; never mix models across conditions. If neither full schedule fits, revise scope/resources explicitly before main execution rather than removing shams, incomplete pairs, or unfavorable families. The 100-hour figure is a resource decision point, not evidence of sufficiency.

Freeze the accepted model/environment, size, templates, source/event schemas, limits, timeout, all worlds/edits/partitions/seeds, schedule, estimands, and forecast before inspecting main outcomes. Execute balanced task/world blocks; rotate eligible sibling order/device assignment subject to replay dependencies. Monitor remaining allocated time and stop before exceeding the frozen ceiling. Unexpected incompletion is reported with coverage and bounds, not converted into exclusions or a new sample-size target.

## 9. Implementation and consistency requirements

Use a small Python package with task generators/oracles, protocol/state transformations, inference, evaluation, and analysis. Python 3.11, Pydantic 2, PyTorch/Transformers/Accelerate/bitsandbytes, NumPy/SciPy/pandas, and Matplotlib are sufficient components, subject to the passing environment lock.

Use **LangGraph with local SQLite checkpoints**, tested for this protocol, or a small Python loop if the integration cannot preserve its semantics. Checkpointing supplies persistence, not scientific isolation or semantic repair. Each branch starts in a new thread from a deep-deserialized snapshot; explicit replacement must remove cleared state without append reducers restoring it. Maintain independent delivery cursors and message effects. One SQLite file per worker is sufficient. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

The round procedure is: freeze views → render requests → obtain or replay replies → validate → stage outgoing records/text → apply this branch's delivery rule → checkpoint → advance. Store both pre-delivery and committed states where replay/queue interventions require them. B/C first-round replies are dependency parents of mixed/Q first rounds, but never their post-delivery recipient state.

Persist a raw reply before applying effects. Resume completed call IDs from that exact reply, including invalid ones; stable message IDs make delivery idempotent. Permit at most one identical-request retry for an infrastructure interruption with no durable response, charging every attempt. No retry for wrong answers, formatting, truncation, or a completed timeout. Begin development with a 120-second attempt timeout; verify adequacy before freezing it. Record failed slots and possible unobserved completed inference around a crash rather than claiming exactly-once generation.

Assign saved per-world/phase/replicate/round/peer seed streams, matched across sibling policies and events; retain independent peer streams. Matched seeds couple randomness but do not make different prompts equivalent. The required first-round replay uses exact equality, not this approximation. New continuation replicates must have new physical generation identities and seeds. No backend conversation handle, KV cache, or recurrent state persists between calls; only explicit branch-owned records are re-rendered.

| Record | Minimum required contents |
|---|---|
| World/event | Task/size, seed, raw ownership/positions, chosen edits, partition, subset membership; gold/footprints stored evaluator-side |
| Peer/checkpoint | Exact permitted source table, history/candidate/feedback, queue and delivery cursors, prefix parent and phase/round |
| Call/attempt | Logical call ID, physical generation/replay parent ID, exact rendered request, settings/seed, raw reply, validity/termination, timing/tokens/device |
| Delivery | Sender/recipient, source ID/version or prose, generation round, first usable round, host/agent origin, queue/release status |
| Outcome/cost | Correctness, coordinate denominators, trajectory/annotation fields, grouping keys, actual allocation and logical policy-cost attribution |

Essential checks before inference and before release:

1. **Task truth:** independent oracles agree on selected native cases and adversarial duplicates, array endpoints/shard boundaries, rank crossings, alternative paths/disconnection, and empty/nonempty D. Updating a source never rewrites a candidate.
2. **Visibility:** no gold, future edit, hidden shard, or condition label enters prompts; source references reveal only held current versions. Receipts contain real historical raw values, not host-computed repair advice.
3. **State interventions:** initial B/C/K/mask source tables match; C/F differ only in acquired remote evidence; K retains exactly the accepted round-four candidate or absence. Reset does not restore old truth. CPU v1→v2→v3 checks validate version handling without claiming live repeated recovery.
4. **Synchrony and replay:** no within-round access; first-round mixed/Q request equality; mixed messages combined before branch-local delivery; Q's round-two sources/own reply equal its parent; no held text leakage, premature release, duplicate delivery, or sibling mutation.
5. **Failure/restart:** invalid replies, interruptions, timeouts, overflows, and resumes preserve slot/attempt accounting; completed invalid replies cannot be resampled. No silent context truncation or permanent peer deactivation.
6. **Analysis:** θ=0 when reset has the same effect across events; φ=0 without cross-group influence; positive/negative teammate effects have correct signs; φ_corr distinguishes shared from revision-specific effects. Check fragmentation, preservation denominators, missingness bounds, paired resampling, and physical versus logical cost with synthetic fixtures.
7. **Accounting and capacity:** enumerate the full branch manifest and reconcile both schedule totals, repeat IDs, and pilot calls; tokenize the attainability witness and worst permitted contexts; verify memory and measured timing gates.

Use ordinary unit/property checks and a tiny end-to-end scripted run. A general orchestration framework, formal verifier, graph database, or coverage campaign is unnecessary. Publish the accepted configuration/environment lock, inputs/seeds, immutable prefixes/branches, raw calls/deliveries, tidy outcome/cost tables, analysis code, figures, and pilot/coverage report. Every empirical statement must be traceable to executed artifacts.

## 10. Foundations, limits, and contribution

The scientific foundation is established work, accurately attributed:

- [SILO-BENCH](https://aclanthology.org/2026.acl-long.1354/) provides private-shard coordination tasks. This study changes sizes, provisional-answer lifecycle, communication rendering, and source dynamics.
- [CIR](https://arxiv.org/html/2610.00372v1) motivates matched recovery interventions and distinguishing rescue from harm. Paired recovery evaluation is not claimed as new.
- [ICR](https://arxiv.org/html/2610.01042v1) studies answer-only/full-text communication and correction/preservation with frozen independent solutions and single-hop revision. Here the target changes after actual private-information collaboration, followed by further team feedback.
- [StateAuditor](https://arxiv.org/html/2608.01619v1) uses previous/current transitions in agent repair; [DBSP](https://arxiv.org/abs/2203.16684) supplies an incremental-computation foundation. Historical receipts and correct-summary updating are established ideas, not proposed inventions.
- [REVISE](https://arxiv.org/html/2609.00643v1) and related recovery work address structured dependencies and conservative invalidation. This study does not assume a correct semantic dependency graph for peer prose or claim to outperform those systems under their own interfaces.

The [SILO audit](research/07_repository_audit/SILO_REPOSITORY_AUDIT.md) documents native runner/evaluator limitations: submitted peers stop, historical delivery state can mutate, retries are unbounded, and generic partial scoring mishandles some nested/duplicate outputs. Reuse mathematical task definitions and attribution, not those execution semantics. These checkout findings do not establish errors in published SILO results. The [v2 protocol audit](research/04_design_extensions/evidence/PROTOCOL_AUDIT.md) supplies checked identities and constructed local-information counterexamples; its scripts are not a production recovery implementation. The [literature landscape](research/04_design_extensions/UPDATED_RESEARCH_LANDSCAPE.md) preserves wider predecessors, version notes, and unresolved access caveats. Verify precise source/version claims before publication; no exhaustive novelty claim is required.

Keep the project within one announced edit, reliable synchronous communication, four peers, one accepted quantized model, bounded non-thinking generation, and five selected task families. The study does not test unannounced-change detection, adversarial peers, asynchronous races, irreversible actions, repeated revisions, larger teams, or frontier-model generality. Small tasks and exact source forwarding simplify factual integrity; public hints and permitted centralization limit claims about autonomous algorithm discovery or distributed lower bounds.

Do not add live delayed resets, revision-time/direction sweeps, completion-reopening obligations, semantic/exposure-based deletion, verifier-assisted answer repair, learned routing, prefix-prevention training, or additional models to this schedule. Their distinct interfaces and controls would dilute the questions identified here. Prefix-progress/direction descriptors, version tests, and deterministic information examples preserve their useful lessons without another live matrix.

The intended contribution is a **controlled account of when previously acquired evidence, retained outputs, historical change information, and peer interaction help or hinder recovery**. Useful findings include a compact practical policy, limits of correction broadcasting, harmful or beneficial effects on collaborators, costly loss of correct work, or well-bounded evidence that simpler recovery suffices. Inconclusive intervals and capability failures must remain visible. A completed, reproducible negative result is preferable to a stronger claim unsupported by the available observations.
