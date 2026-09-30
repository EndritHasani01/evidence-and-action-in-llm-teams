# SILO repository audit

Inspected 24 September 2026. These are observations about the supplied checkout, not a reproduction of SILO's published experiments. [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) contains the final study design and overrides this supporting note.

## Inspection coverage

Read all three task-generator modules, the case-construction code, runner, state models, prompting/parsing/evaluation utilities, and the point-to-point, broadcast, and shared-file tools. Examined the inventory and schemas of all 180 stored cases: 30 tasks at 2, 5, 10, 20, 50, and 100 agents. The generator modules seed Python's global random generator at import; these files are not independent repetitions of each task at a given size. New experiments need explicit per-world random generators.

The [ACL paper](https://aclanthology.org/2026.acl-long.1354.pdf) and [public repository](https://github.com/jwyjohn/acl26-silo-bench) were also consulted. No Git metadata in the supplied subdirectory establishes which upstream commit it represents. Keep the supplied source and record the version actually used during implementation; do not invent a commit identifier.

## What the implemented tasks compute

The following observations come from [Level I generators](acl26-silo-bench/benchmark_generator/paradigm_i.py), [Level II generators](acl26-silo-bench/benchmark_generator/paradigm_ii.py), and [Level III generators](acl26-silo-bench/benchmark_generator/paradigm_iii.py). They describe the checkout's semantics, including details that task names alone obscure.

| Tasks | Implemented semantics and implications |
|---|---|
| I-01, I-02, I-03 | Maximum; word counts; plurality vote with a deliberately dominant candidate. A random vote edit often leaves the winner unchanged. |
| I-04 | Any-match instances contain zero or one global `ERROR` witness. Alternative witnesses would be a generator extension. |
| I-05, I-06 | Count numbers in an inclusive range; XOR of integer shards. Exact, but less informative about the distribution of affected output coordinates. |
| I-07, I-10 | Mean and population standard deviation. Floating arithmetic introduces an avoidable evaluation complication for the initial study. |
| I-08 | Cardinality of the union of integer shards. |
| I-09 | Ten largest values, sorted descending with multiplicity. The descriptive `verification_logic` string uses sets, but the generated answer is an ordered list. Use the task's explicit output contract and an independent oracle. |
| II-11 | Prefix sum of concatenated shards; **each agent returns only its segment**. A single edit changes a suffix. |
| II-12 | Centered width-three moving averages, excluding endpoints and rounding to two decimals. **Every agent returns the complete array**, so local boundary computation does not remove dissemination needs. |
| II-13 | Longest palindrome length, with a fixed palindrome inserted into the generated string. |
| II-14 | Five synchronous steps of a one-dimensional binary rule: a cell becomes one when exactly one of left/self/right is one; outside boundaries are zero. Segmented output. |
| II-15 | Greedy non-overlapping `ABC` matches. The implementation does not count all combinatorial subsequences. |
| II-16 | Total trapped rainwater, using global left/right maxima. |
| II-17 | Adjacent differences, omitting the first input position; **every agent returns the entire difference array**. A single interior edit changes two coordinates. |
| II-18 | Linked-list distance from the true head, with randomly distributed nodes. Data dependencies need not follow neighboring agent IDs. |
| II-19 | Deduplicate a globally sorted sequence whose contiguous portions are distributed. |
| II-20 | Sequential, simplified ASCII/XOR digest computation, modulo 10,000; segmented output. |
| III-21 | Globally sort integer values and return equal-sized rank segments. Duplicate values are legitimate. |
| III-22 | Upper median for even input length. Prompts discourage centralizing all data; tools do not enforce that restriction. |
| III-23 | Number of undirected connected components, including isolated nodes. |
| III-24 | Undirected, unweighted BFS distances from node zero, with `-1` for unreachable nodes. Edges are randomly distributed; every agent returns the full distance dictionary. |
| III-25 | One K-means update with public initial centroids. Per-cluster local sums and counts can be aggregated; this instance does not inherently require a global shuffle. |
| III-26 | Distinct-element count: mathematically the same problem as I-08 despite the different level and suggested algorithm. |
| III-27 | User/item dot products and top-three recommendations, with nested list outputs and floating arithmetic. |
| III-28 | One PageRank step, without redistribution of dangling-node mass. A conventional PageRank oracle could silently grade a different function. |
| III-29 | Longest-processing-time assignment, scored through load statistics rather than the actual assignment. |
| III-30 | Each agent has one row of A and **all of B**. Local matrix multiplication followed by answer sharing suffices for this partition. |

The levels are useful organizing motifs. They are not a randomized treatment or a demonstrated ordinal hardness scale for the available unrestricted, variable-payload communication tools. Input distribution, algorithm hints, output replication, arithmetic difficulty, and answer size vary together.

## Runner and evaluation findings

| Location | Finding | Consequence for a correction study |
|---|---|---|
| [engine.py](acl26-silo-bench/src/engine.py) | Submitted agents are skipped permanently; execution stops once everyone submits or the round limit is reached. | A later correction needs reactivation or provisional answers with a fixed continuation phase. |
| [engine.py](acl26-silo-bench/src/engine.py), tool modules | Tool responses are appended after a generation. A receive request cannot inform a send already generated in that same call. | Define delivery timing explicitly; count communication rounds by when information becomes visible to the next generation. |
| [msg/tools.py](acl26-silo-bench/src/msg/tools.py) | Receiving a message writes its `read` flag into a previous round's message file. | Reusing a checkpoint directory across branches can contaminate sibling runs. Use independent state and immutable message records. |
| [sfs/tools.py](acl26-silo-bench/src/sfs/tools.py) | Shared-file reads use the preceding snapshot and writes update the current shared state. | This is a different communication mechanism; it should not be casually pooled with message passing. |
| [utils/llm.py](acl26-silo-bench/src/utils/llm.py) | Infinite retry, one-hour request timeout, and no explicit generation-token budget in the adapter. | Replace the inference adapter for a bounded local GPU experiment. |
| [utils/metrics.py](acl26-silo-bench/src/utils/metrics.py) | Generic partial-credit branches do not handle all nested outputs or duplicate positions correctly. | Implement task-specific exact and coordinate scoring independently. |

The runner stores expected answers in execution metadata, but its normal prompt construction does not automatically expose them. New branch state must retain that separation. Algorithm and topology suggestions already appear in task prompts; the proposed study must not claim agents discover algorithms without guidance.

## CPU checks actually executed

1. Passed each stored gold answer through the native exact-success evaluator: **180/180 returned success 1**. This checks evaluator self-consistency, not whether all gold answers are mathematically correct.
2. Applied native partial scoring to those same perfect outputs: **18 raised `TypeError`** for nested lists (III-25, III-27, III-30 at all six sizes). **Five III-21 cases scored below 1 despite perfect answers**, because duplicate values interact incorrectly with a value-to-position map and strict increasing-subsequence calculation.
3. Independently recomputed the mathematical answers for I-01, I-09, II-11, II-17, III-21, and III-24 at all six stored sizes: **36/36 matched**. Computations used maximum, ordered selection, cumulative sum, adjacent subtraction, sorted rank slicing, and a separate queue-based BFS.

These checks do not validate the other 24 tasks' oracles, the published result files, future correction generators, or any model's performance. No GPU inference or correction experiment was run during this audit.
