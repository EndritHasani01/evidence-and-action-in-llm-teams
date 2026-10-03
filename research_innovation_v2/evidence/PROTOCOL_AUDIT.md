# Protocol, information, and source audit

Date: 2026-10-04. This is new local source inspection and executed CPU analysis. It is not a live LLM experiment, a hardware pilot, or an independent reproduction of the previous literature results.

## Governing design actually inspected

The current PS defines four identical peers with persistent current source tables, four synchronous prefix calls per peer, drained fourth-round deliveries, one authoritative revision, and matched four-round continuation branches. Models see only their current per-peer evidence and permitted historical derived state. Host copies authenticated source references; it does not infer semantic dependencies. B and C have identical current source tables. B retains historical replies, prose, errors, and candidates; C removes them. F additionally removes acquired remote evidence. L publicly announces the changed record but initially delivers replacement contents only to its owner.

The active source table removes the old record version. It does not retain the old raw table inside conversation history. This is important: an old value may remain in B prose or candidates, but it is not guaranteed to remain even in B. C has neither the old raw version nor derived historical statements. Consequently, an authoritative **replacement** is not necessarily an explicit `(before, after)` change record from the model's perspective. The distinction is a legitimate aspect of the existing package intervention, not a flaw in its estimand.

The source archive available to the host establishes what a before-value was; knowing it does not require the task oracle. Giving it to peers would nevertheless be an additional information intervention, potentially revealing an old private value they had never seen. It must be explicit and common to the compared payload arms.

## Actual source anchors verified

| Source | Verified observation | Consequence |
|---|---|---|
| `acl26-silo-bench/benchmark_generator/paradigm_i.py:57`, `:486` | Global maximum is replicated; top-ten output retains multiplicity despite a misleading set-based verification string. | Use independent exact mathematics. Losing an incumbent can require values omitted from the old answer. |
| `acl26-silo-bench/benchmark_generator/paradigm_ii.py:57`, `:513` | Prefix output is segmented; difference output is replicated. | Output placement changes update sufficiency even for simple linear functions. |
| `acl26-silo-bench/benchmark_generator/paradigm_iii.py:57`, `:265` | Sorting outputs rank segments; BFS outputs complete node distances. | Sort has inter-peer boundary movement; old BFS distances do not encode alternative edges. |
| `acl26-silo-bench/src/engine.py:203` | Submitted agents are skipped, current generation precedes tool execution, historical contexts are appended. | Native runner is not the proposed provisional synchronous recovery protocol. |
| `acl26-silo-bench/src/msg/tools.py:49` | Receive scans and mutates historical `read` flags. | Reusing old directories cannot provide isolated sibling branches. |
| `acl26-silo-bench/src/utils/llm.py:10` | Unbounded retry and no generation cap. | Native timing cannot establish PS feasibility. |
| `acl26-silo-bench/src/utils/metrics.py:196` | Generic partial scoring constructs a value-to-position map, then an LIS. | Duplicate sort values and nested outputs need task-specific scoring. |

These are observations about the supplied checkout, not allegations about published SILO results. No production source was modified.

## CPU probes executed now

Run: `python research_innovation_v2/evidence/protocol_probe.py`.

Artifacts: [script](protocol_probe.py), [complete JSON results](protocol_probe_results.json). All assertions passed. The script uses only the Python standard library; it writes only its new result JSON. No model inference was performed.

### Constructive indistinguishability

Five numeric pairs use exactly 32 records, four peers, and eight-record source/output segments where applicable. Each pair has the same designated peer's correct old candidate, the same current private shard, and the same changed-record position/new value; the required new answer differs. No acquired remote raw records are assumed. This is a legal information configuration, not a claim that natural successful prefixes frequently produce it. Private evidence acquired through prose can explain how a correct old candidate existed without the complete source table, but these probes do not synthesize a natural model transcript.

1. **Prefix, missing before-value.** Worlds start with `(1,3)` versus `(3,1)` and otherwise all 2s. Peer 3 has the same old prefix segment and private data. Position 0 becomes 4. Its new segment shifts by 3 versus 1. An explicit before-value distinguishes the worlds; candidate plus replacement alone does not.
2. **Sort, record identity lost.** Worlds swap values 10 and 20 at source records 0 and 1. Their whole old sorted multiset is identical. Source record 0 becomes 40. Peer 1 has identical private data and old rank segment, but revised rank 8 differs. Even a complete old sorted output does not map source IDs to their old values.
3. **Sort, boundary value missing even with delta.** Both worlds edit 10 to 50. Peer 1 has identical old ranks 8–15 and current private records, but the previously adjacent rank 16 is 30 in one world and 31 in the other. The revised local segment must import this previously unretained boundary value. Explicit old/new values do not remove this distributed information requirement.
4. **Max, discarded reserve.** Both old maxima are 99 and both revise 99 to 0, but unseen second-largest values are 98 versus 97. Correct old answer plus even a complete edit delta is insufficient.
5. **Top-K, discarded reserve.** Both old top-ten lists are 99 through 90 and both revise 99 to 0. Previously omitted rank 11 is 89 versus 88. The new answer differs despite identical retained old output and delta.

The BFS pair uses exactly 12 public nodes and 16 unique undirected edges, consisting of a tree plus five nonedges, as in PS. Both have the same complete old distance vector, the same designated peer's four edges, and the same removed edge `(0,1)`. Both deletions change answers; new distances differ. Thus even giving the deleted edge endpoints cannot reconstruct alternative topology from old distances alone. The two worlds are within the support of the intended graph family, but were constructed rather than sampled.

### Strengthening two witnesses to complete retained B views

The script additionally constructs full **scripted** four-round histories for the prefix and sort pairs. In round one, each peer sends its shard sum (prefix) or sorted shard values (sort) as prose to the other peers, with no `source_refs`. Round one candidates are schema-shaped placeholders. In rounds two through four, peers have enough communicated information to produce their correct original outputs; they send no further messages. The designated peer's own replies, received prose, candidate history, current private source records, public revision notice, and broadcast replacement record are structurally identical across the paired worlds, checked as complete objects. Its new required output differs.

For prefix, swapping two values inside the remote owner's shard preserves every communicated shard sum. For sort, swapping two values inside the remote owner's shard preserves every communicated sorted shard, while erasing which value belonged to the changed record ID. Thus even retaining the complete **particular** B history does not guarantee availability of the before-value. This is stronger than an answer-only counterexample. It does not claim every B history is insufficient: a different legal prefix could forward raw references or record exact source-ID/value pairs.

The strengthened probe also computes each required revised output using only that common retained view and the supplied historical before-value, and checks equality to the independent after-answer. For prefix it transports the retained segment by the explicit change; for sort it updates the multiset already present in the retained summaries. This establishes sufficiency for these constructed views as well as failure without the receipt. The deterministic calculation is research evidence only; it is not a runtime tool supplied to any LLM arm.

These are deterministic protocol-shaped transcripts, not outputs sampled from Qwen. Their small messages respect message-count/reference-count structure; exact tokenizer-cap validation was not performed. They establish possible information loss through ordinary summaries, not its natural frequency, behavioral importance, or successful completion of the model pilot. No history is injected into a proposed main experiment.

**Information claim:** if two admissible worlds induce the same retained view `V` and event payload but different required revised outputs, no deterministic updater of that view is correct in both worlds. Randomization cannot guarantee correctness in both either. This is an elementary indistinguishability argument, not a novel theorem. It bounds that representation and evidence view only. It is not a bound on B's complete prose, all peer views jointly, or future communication.

### Positive identities and an important failed counterexample

Exhaustively checked 8,748 single-entry revisions of six-element ternary arrays:

- Prefix sums admit `new_y[j] = old_y[j] + delta` for `j` at or after the revised coordinate.
- Adjacent differences change at most the two incident coordinates, with opposite signed deltas.
- A complete old sorted multiset can be updated by deleting one occurrence of the old value and inserting the new value.
- A correct complete difference vector plus any unchanged current raw record reconstructs the entire old array: the differences determine it up to one additive constant and the current anchor supplies that constant.

The last identity defeats the easy claim that removing the before-value necessarily makes difference-array recovery information deficient. In PS every peer retains eight own sources and only one changes, so at least seven unchanged anchors remain. Correct complete difference outputs plus those sources are sufficient even without an explicit before-value. This is why generic answer-only arguments must be checked against actual source placement.

These identities assume correct old outputs. Runtime policy cannot know that from hidden gold. An incorrect prior candidate can efficiently transport its old errors; this remains a central empirical failure mode.

### Temporal exposure probes

The schedules `0→1` then `1→2` and `1→2` then `0→1` have identical static edge sets and message counts. With owner 0 exposed initially, the first reaches peer 2; the second does not. Aggregated topology and message volume therefore lose relevant temporal information even in four rounds.

Enumerated all 256 fixed routings where each peer sends to at most one other peer each round. After four rounds, the owner can potentially influence 1/2/3/4 peers in 64/96/72/24 of these routings respectively. This is a finite combinatorial enumeration, **not a distribution of LLM communication**. It actually warns against declaring saturation inevitable. All-to-all messages expose every peer after the first delivery; sparse/disconnected routes can preserve unexposed histories.

The cone tracks possible dependence of generated outputs on all exposed inputs. It does not demonstrate that any conclusion used the old source, nor does it measure semantic necessity. A record-forwarding message can have source-current contents while its selection depends on old information.

The script models actual delivered-message channels. It does not model counterfactual absence of an expected message or every implicit dependence of routing decisions. Its overapproximation claim is restricted to that delivered-content model, not a universal causal noninterference guarantee.

## Historical evidence and control dependence

An obsolete source value is false when asserted as the *current* fact but true as a claim about the previous version. It can support a delta calculation. This distinction does not justify retaining every old rationale. It suggests a narrow payload experiment: versioned historical evidence can be treated as a transition operand without being re-admitted to the current source table.

Similarly, C is not fully independent of the old world. The old fact may have determined which unchanged sources were requested and forwarded. Those acquired-source memberships remain in C. Therefore a conservative derived-history cut can guarantee, at most, exclusion of the tracked old-version path from **retained derived objects**, conditional on the surviving evidence view and protocol assumptions. It cannot establish complete causal erasure while retaining evidence selected during the old computation.

## Integrity and read ledger

Current specification SHA256: `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00`, matching the September audit. Parsed all old audit JSON records and recomputed hashes for all 36 recorded source files and 180 benchmark cases: no mismatches. This verifies preservation of that inspected corpus; the earlier 176 exact all-task matches and four PageRank rounding differences were read, not rerun as new findings.

Read in full for this assignment:

- `PROJECT_SPECIFICATION.md` (all sections; repeated chunk reads resolved truncated initial display).
- `research_innovation/VALIDATION_STRATEGY.md` and `FALSIFICATION_AND_RISKS.md`.
- `research_innovation/risks/MECHANISM_REVIEW.md`, `LITERATURE_REVIEW.md`, `FEASIBILITY_REVIEW.md`.
- Every Markdown/source file in `research_innovation/evidence/`: `WORKSPACE_VALIDATION.md`, `SEARCH_AND_CLAIM_LEDGER.md`, `REPOSITORY_INSPECTION.md`, `REOPENING_EXCLUSIONS.md`, `ISOLATION_AND_CERTIFICATION_PREDECESSORS.md`, `CURRENT_VALIDITY_COUNTEREXAMPLES.md`, `audit_repository.py`, `recovery_counterexamples.py`.
- `counterexample_results.json` in full; `audit_results.json` fully parsed and all records/hash fields checked programmatically, with top-level findings and exceptions inspected. Its hundreds of repetitive success rows were not individually displayed as prose.
- Native `src/msg/tools.py`, `src/models.py`, `src/utils/llm.py`, `src/utils/metrics.py` in full.

Targeted source reads, not entire files: six selected task generator functions at the anchors above and `src/engine.py` `run_round` lines 203–421. Other generator functions were inventoried by names and the prior complete audit was read; this assignment does not claim a new full-source reread of all 30 tasks.

Memory quick pass: relevant registry lines in `C:/Users/EndritHasani/.codex/memories/MEMORY.md` were consulted for design guardrails, then checked against current PS/source. No memory-derived performance claim is used. Parent synthesis should include its required memory citation if it relies on that quick pass.
