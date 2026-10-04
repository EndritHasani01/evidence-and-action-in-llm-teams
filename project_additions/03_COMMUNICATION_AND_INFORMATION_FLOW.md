# Addition 03: connect correction delivery, available evidence, and recovery

**Recommendation: include the small delivery/evidence analysis; keep full exposure graphs optional. Zero additional model calls.**

**Simple idea:** show what information was actually available before each response. Separate the authoritative correction reaching a peer from the peer subsequently producing a correct answer, and show how much previously gathered raw evidence C retains compared with F.

**Status:** proposed analysis of future PS logs. The previous workspace contains deterministic communication examples, but no natural Qwen communication/recovery dataset. This proposal does not require more peers, a topology sweep, or semantic provenance extraction.

## Question and value

Does local delivery lose time because v2 has not reached peers, or do errors continue after the corrected record is available? Does retained evidence remove a substantial reacquisition burden, or did the prefix gather little that F must recover?

This makes two existing policy contrasts tangible. B–L becomes an intervention on guaranteed content delivery with visible timing; C–F becomes an intervention on a measured inventory of acquired evidence. The thesis can explain why either contrast is small without calling communication or evidence reuse irrelevant.

## Already in the PS versus the addition

PS §6 already requires first authoritative receipt, subsequent correctness, message deliveries, source-record delivery, and payload accounting. The addition is an explicit **call-boundary timeline** joining those records and a small evidence-coverage summary. Basic source/message provenance is already available in the protocol; no new logging architecture is needed.

## Minimum worthwhile analysis

Use two panels, preferably beside the recovery curves rather than in a separate large chapter:

1. **Delivery and response:** for L and B, plot the fraction of peers with v2 available before each recovery call alongside exact-agent accuracy. In selected case cards, mark the particular call where receipt first becomes usable. B's receipt line should already be complete before round one; an exception is a protocol defect, not a behavioral result.
2. **Evidence retained and reacquired:** report the number/fraction of current remote source records available at the boundary in C and F, then the number of newly acquired source IDs over the four recovery rounds. Show the paired C–F accuracy contrast next to these counts, without claiming the counts mediate it causally.

Message totals and payload tokens belong in a small descriptive table. Do not make a dozen centrality measures or accuracy-per-message ratios the main result.

## Data and definitions

Required fields: task/world/branch/peer/round IDs; exact per-call source view; stable source IDs, owners, versions and tombstones; source-reference deliveries with origin and destination; message send and first-usable-delivery boundaries; whether the host or an agent supplied the record; candidate validity/correctness; and message/prompt token counts.

Define availability at the **start of a model call**, not at the wall-clock moment a file was written:

- `R_i = min{r : peer i's rendered view for recovery call r contains v2}`. Use `not received within four rounds` if absent throughout; do not substitute an invented finite arrival round.
- `K_i = min{r >= R_i : peer i produces a valid complete new-gold answer}` when both events are observed.
- `L_i = K_i - R_i` is the number of subsequent generation boundaries before the first correct response, conditional on observed receipt and success. A same-call correct response has lag zero.

Do not report the mean of observed `L_i` as an overall recovery-time estimate. Peers who never receive v2, never become correct, or receive it only near the horizon have different observation windows. The minimum presentation is the timeline plus counts of: no receipt; receipt but no subsequent correct answer; correct at the first eligible call; and correct at a later call. Keep their denominators explicit. A secondary lag distribution must retain censoring and the differing remaining windows.

A peer can become correct **before** an authoritative v2 record arrives: it may infer the result or receive useful prose. Mark that as a separate observation instead of forcing a negative lag or declaring receipt unnecessary in every case. First subsequent correctness is also not stable correctness; link it to [Addition 01](01_RECOVERY_TRAJECTORIES.md).

For evidence inventory, let `V_i(r)` be current record IDs in peer i's source view and `O_i` its private IDs. Let `e` be the revised record ID. Use

`retained_remote_i = |V_i(boundary) \ (O_i union {e})|`.

Excluding `e` prevents the host's broadcast intervention being counted as previously gathered evidence. For complete-coverage flags, compare against the task's complete current record universe; a tombstone is the current version of its record, not an absent forgotten edge. State whether a reported count includes tombstones. Count unique newly acquired `(record_id, version)` pairs separately from all delivery attempts and fan-out.

Raw source-table coverage is not total knowledge coverage. B may contain summaries of unseen records; C may solve without acquiring every record. Full current source coverage is a sufficient information condition for exact fresh computation, but incomplete coverage does not prove an agent lacks the answer. Never label an unforwarded raw record “the cause” of failure merely because the oracle uses its value.

## Optional: one temporal information-flow illustration

If actual traces make it useful, reconstruct the time-ordered path of the revised record and messages generated after its exposure. This can show why identical message counts conceal different routes. The prior CPU probe already demonstrates that `0→1` then `1→2` is different from the reversed timing; it does not establish which route natural models use.

Keep this optional analysis modest: one source-exposure timeline or peer raster and, at most, the fraction of historical derived objects reached in the **modeled delivered-content graph**. Count actual message edges and retained-history links. Do not call it the model's true dependency graph or introduce a runtime reset rule based on it.

Missing expected messages, routing choices, and source-selection decisions can carry implicit information. A graph of actual delivered contents does not account for every such channel. It cannot certify causal independence, identify which reasoning was contaminated, or prove that a small semantic output footprint ought to require little recovery.

## Interpretation and inference

- B–L is the clean intervention effect supplied by the original matched design. Receipt-time correlations within L are descriptive and can be confounded by difficulty, communication choices, and initial competence.
- C and F have different evidence at initialization by design. Subsequent evidence acquisition is a treatment outcome, not a variable to “control away” to obtain the original effect.
- Aggregate peer indicators within worlds and then balance task families. World clusters remain the independent units; source copies and message deliveries are not independent samples.
- Show which record deliveries came from the host. A policy receiving four injected copies of the changed record has not generated four successful correction messages.
- Keep malformed replies, unavailable deliveries, and infrastructure gaps explicit. Trace reconstruction must not silently invent sends that were rejected by the protocol.

## Extra cost and effort

**Extra inference: 0.** The minimum analysis should take roughly 1–3 focused days after valid PS logs exist and shares data preparation with trajectory/failure analysis. A general temporal graph implementation could take several additional days; omit it unless the actual trace provides a clear explanatory use. Do not trade core experimental worlds for this descriptive analysis.

## Interesting outcomes, including negatives

- L distributes v2 almost immediately and matches B: peer delivery is already effective under this clean announced-change protocol.
- All peers receive v2 early but remain wrong: delivery is insufficient, without identifying the remaining hidden cause.
- C retains many useful raw records and recovers earlier than F: evidence preservation has a concrete operational interpretation.
- C and F begin with nearly the same source inventory: a small C–F difference is unsurprising in this acquisition regime.
- Message volume is high but few new records become available: communication activity should not be equated with verified information delivery.
- Almost all history lies inside the modeled exposure region: there may be little observable room for a selective history-reset policy; this remains a conditional trace observation.

**Minimum recommendation:** include the call-boundary delivery panel and retained/reacquired evidence table. Add a temporal graph only when it explains something the simpler timeline cannot.

## Sources

Grounded in [PS §§5–7](../PROJECT_SPECIFICATION.md), [untapped structure](../research_innovation_v2/UNTAPPED_STRUCTURE.md), and the [protocol audit](../research_innovation_v2/evidence/PROTOCOL_AUDIT.md). The additions-pass read ledger is in [Addition 01](01_RECOVERY_TRAJECTORIES.md#sources-and-read-scope). These analyses stand on their practical explanatory value; they do not depend on proving a new information-flow method.
