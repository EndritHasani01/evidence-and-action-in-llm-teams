# Fresh repository inspection

Status: completed source/data audit, 2026-09-30. This file records current-source observations and CPU checks, separately from claims in the earlier `SILO_REPOSITORY_AUDIT.md`. No model inference or production-source changes were performed in this audit.

## Preservation and scope

`PROJECT_SPECIFICATION.md` SHA256 at start: `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00` (matches parent-provided value).

Read the complete three paradigm generator modules (all 30 tasks), generator entry point, engine, models, three protocol tool modules, all nine CLI wrappers, prompts, parser, metrics, persistence, inference adapter, configuration, batch runner, analysis script, package metadata, configuration example, run script, repository/generator READMEs, LICENSE, `.gitignore`, and `.python-version`. The manifest covers 36 source/document/config files (6,006 lines); LICENSE and dotfiles were read separately. The five README figure assets were inventoried, not used as experimental evidence or re-digitized. All 180 individual benchmark cases were parsed and independently recomputed; aggregate JSON files and the matrix ZIP were also checked. The raw benchmarks contain mathematical task inputs and gold outputs; they are not recovery trajectories.

Also read the complete governing specification, earlier repository audit, `source_audit.json`, current README, superseded requirements/budget, support-algebra implementation, typed contracts, and reference tests. No `.git` metadata exists in the supplied SILO directory; an upstream commit recorded in old audit notes does not prove this copied checkout is that revision. `audit_results.json` records current file hashes instead. These hashes establish what was inspected, not model or dataset quality.

## Early findings relevant to research invention

1. The strongest reusable asset is exact task semantics and private-shard/replicated-output structure, not the native runner. The native engine permanently stops submitted agents, so correction-after-success is not implemented. Its model call happens before requested receive tools run, adding a generation boundary to information use.
2. Native P2P receive mutates old-round message files (`read = True`). Reusing checkpoint directories for sibling interventions contaminates later branches. Copying just agent context is insufficient.
3. Native broadcast stores receive progress in a per-round file and reads only the immediately preceding round's cursor. Skipping receive for an entire round loses progress and redelivers historical broadcasts; reproduced on CPU.
4. SFS reads are prior-round snapshots, but write/delete operations modify one current-round map in fixed agent order. Competing writes have last-writer behavior; delete success can depend on a write earlier in that round. Message queues, shared artifacts, delivery cursors, candidate status, and histories are distinct recovery state channels.
5. Native inference retries without a stop bound and requests no generation cap. Cost feasibility cannot inherit native behavior.
6. The top-level `budget_forecast.json` belongs to a superseded Qwen3-4B design (6,400 total calls, unmeasured). The governing specification instead gives Qwen3.5-9B/4B, four peers, 48 or 36 worlds, and 30 aggregate T4 GPU-hours. Old budget output is not evidence of current feasibility.
7. The current specification deliberately gives every agent a public change notice, clears obsolete source versions, drains all in-flight messages before change, uses one correction, and excludes asynchronous races. Thus its empirical question is history reuse under unusually clean factual delivery. This is scientifically controlled, but removes the hardest runtime problem of stale work re-entering through peers, queued messages, summaries, or shared artifacts.
8. Exact semantic change footprints can be computed offline; exposing those to a recovery mechanism would be an oracle intervention. They are useful evaluator labels and controlled stress-design variables.

## Task-level observations from complete source reading

- I-08 and III-26 both compute exact distinct count from IID duplicate-containing integer shards. Their naming/topology hints do not create a clean complexity contrast.
- III-25 is one K-means iteration with public initial centroids and local `(sum_x, sum_y, count)` sufficient statistics; it permits simple aggregation.
- III-30 supplies every peer the complete B matrix and one row of A. Its arithmetic is local, followed by output distribution.
- II-12 and II-17 have local computations but require every peer to return the whole array. Output replication drives global communication beyond boundary dependencies.
- III-22 returns the upper middle order statistic for even sample sizes, not the average of two middle values.
- II-15 counts greedy disjoint completions of an A→B→C state machine, not all combinatorial subsequences.
- II-20 uses an XOR/sum recurrence called a hash chain; it is not cryptographically irreversible and should not motivate blockchain-like claims.
- III-28 omits redistribution of dangling-node mass. Its supplied formula must be evaluated as written, not replaced with a library's standard PageRank defaults.
- III-29 provides total duration publicly and requires a deterministic greedy policy, returning only statistics rather than assignments.

## CPU audit results actually executed

Command: `python research/03_innovation_review/evidence/audit_repository.py` using local Python 3.11.9. Results: [audit_results.json](audit_results.json). Script: [audit_repository.py](audit_repository.py).

| Check | Result | Interpretation |
|---|---|---|
| Inventory | 180 individual cases, 30 task IDs, six sizes (2/5/10/20/50/100) | One instance per task/size, not six repetitions at a fixed size. |
| Metadata, IDs, per-agent gold copies | All 180 consistent | Lengths, ordered IDs and gold fields align. |
| Expanded user prompts | No remaining `{input_shard}` placeholder in any agent prompt | Does not establish absence of every prompt ambiguity. |
| Native exact evaluator on stored gold | 180/180 score 1 | Self-consistency only; independent recomputation below tests semantics. |
| Independent all-task recomputation | 176 exact matches; four PageRank cases differ at 0.000001 rounding boundaries | No other mismatch or exception. Native float-operation order reproduces all six PageRank golds exactly. Do not report this as 180 independent bit-exact matches. |
| Native partial evaluator on perfect gold | 18 `TypeError`s: III-25/27/30 at all six sizes | Nested lists are unhashable in the generic value-position dictionary. |
| Native partial evaluator on perfect sort | Five scores below 1: n5 .97; n10 .905; n20 .865; n50 .637; n100 .4615 | Duplicate values collapse in `expected_pos`, then strict LIS undercounts them. |
| Combined `silo_bench_full.json` | Only the 30 n=100 cases; semantically matches individual files | The combined file is not all 180 cases. Summary metadata likewise describes n=100 only. |
| `III-30_n100.json.zip` | Different older content and different shard schema than uncompressed namesake | Do not unpack over the current data. Archived first shard has `type/data/row_indices`; current has `type/A_rows/A_row_indices/B_matrix`. No oracle validation was claimed for the older archive. |
| P2P receive | Historical file `read` changes false→true; first delivery count 1, second 0 | A later branch reusing the parent message directory can lose a message. |
| Broadcast receive gap | Message delivered in r2, no receive in r3, same message delivered again in r4 | Delivery cursors are not durably carried through inactive receive rounds. |
| SFS collision/read/delete | Same-key writes leave agent1's value; prior-round read cannot see it; current-round delete succeeds | Fixed writer order, snapshot reads, and current-map mutation are distinct semantics. |

The protocol reproduction runs the actual native tool functions, with a standard-library JSON persistence shim because `srsly` is not installed. Pydantic is installed. This tests native protocol control logic, not `srsly` or full engine/LLM integration. Neither a GPU nor an API was used. Temporary protocol files were created outside the checkout and automatically removed. These are findings about this supplied checkout; they do not establish errors in the published paper's results or the exact version used there.

PageRank detail: the independent arithmetic adds `0.85 / size / outdegree` in shard order; the generator adds `0.85 * (1.0 / size) / outdegree` in node order. Both implement the documented formula, but floating evaluation order crosses half-to-even rounding boundaries. `audit_results.json` retains every differing node plus the generator-order reproduction. The six planned integer-only task families all match exactly (36/36).

## Complete task map and adaptation opportunities

Line anchors refer to the current files under `acl26-silo-bench/benchmark_generator/`; source hashes are in the audit JSON. “Replicated” means every peer must return the entire answer.

| Task and source start | Implemented function/output | Recovery opportunity or caution |
|---|---|---|
| I-01 `paradigm_i.py:57` | Global maximum, replicated scalar | Lowering a unique max tests stale winner and renewed search for replacement. |
| I-02 `:107` | Count `apple`, replicated scalar | Invertible delta updates; a cheap baseline can be exact. |
| I-03 `:164` | Dominant plurality winner, replicated string | Natural single-vote edits usually preserve answer; selection must be explicit. |
| I-04 `:222` | Any `ERROR`, replicated bool | Current generator has zero/one witness; multiple independent witnesses require extension. |
| I-05 `:281` | Inclusive [100,500] count | Changed rule boundaries can invalidate old classification without changing raw records. |
| I-06 `:331` | XOR checksum | Invertible correction is trivial given old/new values; useful low-level control. |
| I-07 `:384` | Mean rounded to two decimals | Sufficient-statistic reuse; floating tolerance complicates exact evaluation. |
| I-08 `:434` | Distinct count | Removal requires multiplicity/coverage, not merely a set of seen values. |
| I-09 `:486` | Descending top ten with multiplicity | Negative/pruned candidate information matters when cutoff drops. |
| I-10 `:537` | Population std, two-decimal output | Instructions use two phases; sum/squares can bypass that protocol. |
| II-11 `paradigm_ii.py:57` | Prefix sum, segmented | Known suffix change; clean collateral-damage measurement. |
| II-12 `:129` | Centered width-three mean, replicated full array | Local affected values coexist with global delivery requirement. |
| II-13 `:188` | Longest palindrome length, replicated | A fixed `racecar` insertion biases coverage; witness versus optimality distinction. |
| II-14 `:266` | Five steps of binary neighborhood rule, segmented | Bounded space-time influence; symbolic replay is easy, LLM capability may be limiting. |
| II-15 `:351` | Greedy non-overlapping ABC completion count | Historical control state can alter all downstream matching. |
| II-16 `:432` | Total trapped water, replicated | Bidirectional envelope dependencies; aggregate hides where error occurs. |
| II-17 `:513` | Adjacent differences, replicated full array | One edit affects at most two coordinates; strongest local preservation contrast. |
| II-18 `:569` | Rank from linked-list head, replicated dict | Random pointer ownership, not neighbor-ID locality; pointer edits need validity constraints. |
| II-19 `:657` | Consecutive dedup of globally sorted data, replicated | Editing values may violate sorted-input contract unless constrained. |
| II-20 `:717` | ASCII/XOR/mod10000 chain, segmented | Not cryptographic hash; equal sums/collisions permit answer-preserving edits. |
| III-21 `paradigm_iii.py:57` | Global sort, rank-segmented | Data ownership differs from output ownership; duplicate identities matter. |
| III-22 `:122` | Upper median, replicated scalar | Membership/threshold changes invalidate completeness; centralization only discouraged by prompt. |
| III-23 `:183` | Undirected connected component count | Edge deletion may break an indispensable connection or preserve alternative paths. |
| III-24 `:265` | Distances from node0; -1 unreachable; replicated dict | Good alternative proof / absence / shortestness test; native graph need not be connected. |
| III-25 `:343` | One K-means update, replicated centroid triples | Current initial centroids are public; local sufficient statistics suffice. |
| III-26 `:427` | Distinct count, replicated scalar | Same mathematical function as I-08 despite different assigned complexity level. |
| III-27 `:486` | Top three user-item dot products, replicated triples | Old top matches can remain feasible while a changed vector reopens excluded pairs. |
| III-28 `:574` | One PageRank step, replicated map | Dangling mass is not redistributed; float-operation order matters. |
| III-29 `:652` | Deterministic greedy LPT load statistics | Public total duration leaks an aggregate; assignments are not graded. |
| III-30 `:758` | A-row partition plus complete B, replicated full matrix | Local arithmetic plus output sharing; archive differs from current data. |

## Runtime source anchors and additional hazards

| Source anchor under `acl26-silo-bench/` | Observation and practical implication |
|---|---|
| `src/engine.py:86`, `:102`; `src/analyze.py:80` | Directory ID uses case ID without agent count; all six I-01 files contain `case_id=I-01`. Analyzer chooses latest per case/protocol/model, potentially collapsing all scales; same-second initialization can collide. New study needs world/branch IDs. |
| `src/engine.py:261` | Permanent submitted-state skip; replace with provisional candidates. |
| `src/engine.py:281`, `:316`, `:369` | Generation precedes tool execution/results; receiving cannot inform a send in the same response. |
| `src/msg/tools.py:49-70` | Scans all previous rounds and mutates unread flags in historical files. |
| `src/broadcast/tools.py:48-94` | Cursor only read from previous/current round; skipped-receive gap causes replay. |
| `src/sfs/tools.py:28-59`, `:65-94` | Snapshot reads plus current-map writes/deletes; collisions depend on fixed execution order. |
| `src/utils/llm.py:10-29` | Infinite retry, 3,600-second client timeout, no max generation budget. |
| `src/utils/metrics.py:196-204` | Duplicate/nested-list defects in partial correctness. |
| `src/engine.py:482-485`; `src/analyze.py:135-141` | Engine C uses input+output tokens per executed round; analyzer uses output tokens/(100×agents), despite a token-per-round name. The two cost metrics differ. |
| `src/engine.py:536`; `src/analyze.py:141` | SFS engine metric counts surviving keys modified that round; analyzer counts message-sent counters (SFS writes increment a different field). Neither equals verified information delivery. |
| `src/batch_run.py:159-169` and `_filter_task_files` | Unfiltered `*.json` includes aggregate/summary JSONs; these lack single-case shape. Explicit file filters are required. |
| `src/*/evaluate.py:19` | CLI wrappers request `metrics['token_efficiency']`, absent from engine result keys. Source-level finding; not an end-to-end run. |
| `benchmark_generator/main.py:114-128`, `:139-158` | Segmentation explicit; user prompt contains own shard, while gold is separate metadata. New prompt builders must preserve that separation. |
| `benchmark_generator/paradigm_*.py:17` | Module-global seeding; generation depends on earlier calls/size order. Use one explicit RNG per independent world. |
| `LICENSE`; `pyproject.toml:7` | LICENSE is Unlicense but package metadata says MIT; preserve attribution and actual license text. |

State channels to control independently are source versions, visible source records, own replies, peer prose, typed artifacts, candidate outputs, pending messages, read/delivery cursors, shared files, task/rule versions, model generation/cache state, and the decision that a task is finished. Resetting one channel does not establish the currentness of the others.

## What is already implemented outside SILO

`reference/support.py` contains finite unate Boolean justification algebra, alternative proof sets, descendant closure, estimated/exact masks, and exhaustive oracle support enumeration. `reference/contracts.py` defines evidence, claims, actions, epochs, dispositions, snapshots, and various evaluator/runtime views for the superseded three-role study. `tests/test_reference.py` validates that algebra and the old 6,400-call matrix. These are reusable fixtures/examples if a new design needs them, not a functioning recovery runtime or proof of the current experiment.

A candidate should not be chosen because these classes already exist. Reusing the immutable-record pattern can help; importing old action-gating or exact-support assumptions would prejudge the research question. No reference test suite was rerun because this investigation did not modify that implementation and its success would not validate the proposed design.

## What the current design rules out by construction

The specification is internally candid about scope and already has unusually good sham controls, exact coordinate scoring, cluster analysis, bounded retry accounting, and no gold repair in model-visible state. Preserve these strengths.

However, its public revision notice identifies the changed record, owner and version; source forwarding is authenticated; obsolete source versions disappear from active tables; the prefix is drained at a quiescent barrier; all branches get exactly four recovery rounds; no source/rule/selector changes recur. This excludes asynchronous stale-message resurrection, concurrent artifact completion, task-definition changes, membership changes, and invalid stopping decisions. Such failures are important real-world targets for a new mechanism and cannot be established by rerunning the current matrix alone.

The prefix also lasts only four calls per peer on small algorithmic inputs. It can measure reuse of gathered records and short calculations, but not the absolute savings of hours/days of expensive tool work. A tiny additional adapter with expensive evaluations represented by counted tool actions can test scheduling semantics. Artificial delays should not be mistaken for real end-to-end efficiency; report counted work and actual compute separately.

## Feasible discriminating extensions

1. **Stale work re-entry:** inject one legitimately pre-change delayed message/artifact after the correction. Compare reset-only, epoch/version rejection, conservative exposure tracking, and any proposed reuse policy. CPU schedules can be exhaustive; only a small predeclared live subset needs inference. Epoch fencing itself is established distributed-systems practice, not novel.
2. **Historical support versus current validity:** remove one witness while an unrecorded alternative remains. A conservative policy can be safe but lose useful results; revalidation must show it earns its cost. Compare with alternative-support truth maintenance where support is available; do not claim that case is unsolved. See [CURRENT_VALIDITY_COUNTEREXAMPLES.md](CURRENT_VALIDITY_COUNTEREXAMPLES.md).
3. **Feasibility versus completeness:** add an edge or lower a top-K incumbent so old positive work remains valid while old exclusion/termination decisions do not. This requires explicit coverage/pruning records or an additional small search adapter. The exact output evaluator alone cannot reveal whether a method manages this process state.
4. **Missing dependencies:** alter the declared dependency log while leaving the source/event/agent-produced artifact fixed. Compare natural annotations, predeclared edge deletion, and conservative runtime exposure. Exact semantic graph is evaluator-only. Natural incomplete provenance and synthetically dropped edges must be reported separately.
5. **Checkers and stronger baselines:** if artifact admission uses semantic validators, give retain/restart baselines the same checker access and feedback; include fresh recomputation plus validation and recompute-cheap/retain-expensive simple policies. An exact whole-world SILO checker is effectively a solver and may explain the entire gain.

## Budget arithmetic and scope tradeoffs

Current specification: 48-world main schedule 5,856 calls; 36-world fallback 4,488 calls. Both include one 16-call shared prefix/world, four 16-call changed continuations, two 16-call sham continuations, 384 answer-preserving calls, and two full-information calls/world. A complete candidate pilot is 588 calls. Reserve is 3 GPU-hours development, 1 loading/setup, 2 interruptions; 24 remain provisionally for main execution.

Break-even average allocated seconds/call: 86,400/5,856 = 14.7541 (48 worlds), 86,400/4,488 = 19.2513 (36). These are ceilings, not measured throughput. At 15 seconds/call a new four-round policy costs 768×15/3600 = 3.2 aggregate GPU-hours at 48 worlds (2.4 at 36). One extra 4-call verifier/team round across all 48 worlds costs 192 calls, 0.8 hours at the same unmeasured rate, plus its prompt-length effect. Equal wall-clock seconds per call cannot be assumed across long-history and reset arms.

Therefore replace secondary axes rather than append every new mechanism to the old full matrix. An example affordable design could prioritize retain-all, evidence-only reset, a simple dependency/epoch baseline, and one proposed mechanism, with carefully chosen sham and corruption subsets. This is a design sketch, not a frozen schedule or power claim. CPU counterexamples and schedule checks are cheap; every LLM revalidator/extractor/resume attempt must enter the same 30-hour ledger. Independent devices reduce elapsed time, not aggregate allocated GPU-hours.

No model/hardware capability has been established. The Qwen3.5 9B→4B policy remains a pilot candidate. Package/model/hardware facts from the old specification were read for constraints, not independently reverified in this repository-only audit.

## Final preservation check

The completed CPU audit again recorded `PROJECT_SPECIFICATION.md` SHA256 `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00`. Research artifacts are confined to `research/03_innovation_review/evidence/`. Specification and production source contents remain unchanged.
