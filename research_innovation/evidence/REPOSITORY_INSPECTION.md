# Fresh repository inspection

Status: working audit, begun 2026-09-30. This file records current-source observations and CPU checks, separately from claims in the earlier `SILO_REPOSITORY_AUDIT.md`. No model inference or production-code changes are authorized or performed in this audit.

## Preservation and scope

`PROJECT_SPECIFICATION.md` SHA256 at start: `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00` (matches parent-provided value).

Read the complete three paradigm generator modules (all 30 tasks), generator entry point, engine, models, three protocol tool modules, prompts, parser, metrics, persistence, inference adapter, configuration, batch runner, analysis script, package metadata, configuration example, run script, and repository README. Remaining supporting docs/wrappers and all stored-case data are being checked. The raw benchmarks contain mathematical task inputs and gold outputs; they are not recovery trajectories.

## Early findings relevant to research invention

1. The strongest reusable asset is exact task semantics and private-shard/replicated-output structure, not the native runner. The native engine permanently stops submitted agents, so correction-after-success is not implemented. Its model call happens before requested receive tools run, adding a generation boundary to information use.
2. Native P2P receive mutates old-round message files (`read = True`). Reusing checkpoint directories for sibling interventions contaminates later branches. Copying just agent context is insufficient.
3. Native broadcast stores receive progress in a per-round file and reads only the immediately preceding round's cursor. Skipping receive for an entire round appears to lose progress and redeliver historical broadcasts; CPU reproduction pending.
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

## Pending

Complete all-case data/oracle audit; reproduce protocol hazards; add exact line anchors and bounded feasibility/experiment proposals. Distinguish the current checkout from the version underlying published SILO results.
