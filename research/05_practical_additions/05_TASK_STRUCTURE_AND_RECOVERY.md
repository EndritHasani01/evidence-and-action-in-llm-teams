# 05 — Explain recovery through task structure

**Recommendation: include. Additional model calls: 0. Estimated work: 1–2 focused days once the normal outcome table exists.** Estimates are planning judgments, not measured implementation times.

## The idea and question

Use the six existing tasks to explain *what has to be repaired and who has to produce the repaired answer*. The question is: **when recovery is difficult, is the changed region large, does it cross output responsibilities, or is the missing information absent from the old result?**

This makes the thesis more interesting without changing the experiment. Instead of six unrelated accuracy rows, it gives the reader concrete reasons why two equally small input corrections create different recovery problems. A difference-array edit affects at most two values, yet every peer must return a complete corrected array. A prefix edit may affect many values but permit a simple arithmetic update. These are useful contrasts even when a familiar principle explains them.

## Structure already present

The table uses the PS's original eight-record-per-peer sizes. Update the numbers consistently if its permitted development size reduction is used.

| Family | Unique output coordinates / total peer copies | What the selected edit changes | Responsibility and coordination |
|---|---:|---|---|
| Maximum | 1 / 4 | The single maximum | All four peers must replace it; the old maximum need not retain the runner-up |
| Top-K | 10 / 40 | Some ranked values, including the lost selected value | All peers need the revised list; an omitted replacement may become necessary |
| Prefix Sum | 32 / 32 | A suffix starting at the edited input position | Output segments belong to different peers; a downstream peer can need an earlier shard's historical operand or revised cumulative boundary |
| Difference Array | 31 / 124 | At most two adjacent output coordinates | Arithmetic effect is local, but every peer returns the full vector; small footprint does not mean only one peer needs recovery |
| Distributed Sort | 32 / 32 | Ranks crossed by a value movement, with duplicate values sometimes leaving coordinates equal | Input owner and affected output owners can differ; missing boundary values can require renewed exchange |
| BFS Distance | 12 / 48 | Nodes whose distances change, potentially including disconnection | All peers return the distance map; old distances omit alternative paths |

These are task properties, not a proposed ordering from easy to hard. They also explain why counting peer copies as independent affected problems is misleading.

## Smallest useful analysis

Add a compact annotation row to each existing world/event record:

1. Unique changed-coordinate count `|D|`, total unique coordinates, and affected peer-copy count. These already belong in the PS.
2. Number of peers whose assigned answer has at least one changed coordinate. Keep this separate from the number of changed values.
3. For Prefix Sum: edited global position, source owner, and whether the edit is at the first position of a shard. For Sort: number of output segments intersecting D, and whether the input owner's own output segment is unaffected.
4. For BFS: whether deletion disconnects any node; optionally retain the maximum finite distance increase, with disconnection separate rather than treated as a negative numerical difference.

Produce one task overview table, one panel of per-world B/C effects beside these annotations, and two short trace examples chosen by a stated descriptive rule. A suitable rule is the largest and smallest observed collateral-damage world within a family, with the full world table available; do not present selected examples as typical rates.

Use the existing changed-coordinate repair, unchanged-coordinate preservation, and whole-answer recovery curves. Do not invent a second competing accuracy score or add a large regression. With six/eight worlds per family, a few honest within-family comparisons are more informative than fitted coefficients for many correlated features.

## What the results could teach

- If a small difference-array footprint still creates widespread whole-answer failure, replicated output responsibility and retention of other errors deserve attention.
- If Prefix Sum preserves most previous work while Sort needs another exchange, output placement and missing boundary information offer a concrete interpretation to check in traces.
- If all families recover equally, the study establishes that these structural differences did not produce a practically visible boundary in the measured setting.
- If task differences track initial competence or output length instead, report that rather than attributing them to communication structure.

The annotations are **descriptive explanations to investigate**, not independently randomized causes. In particular, the permitted communication graph is fully connected; a prefix-chain hint does not enforce a communication lower bound. Gold-derived D labels remain evaluator-only.

## Scope and cost

No new worlds, model calls, prompts, or recovery arms. Reuse existing generators, oracles and traces. Implementation means a few analysis columns and report panels, not a new benchmark.

Combine this with the [information atlas](06_RECOVERY_INFORMATION_ATLAS.md) and [deterministic references](14_DETERMINISTIC_RECOVERY_REFERENCES.md) as one explanatory chapter. Their effort overlaps; budgeting all three as independent mini-projects would overstate the work.

Basis: [PS §§3–6](../../PROJECT_SPECIFICATION.md), inspected native task output contracts, and the previous [cross-field deductions](../04_design_extensions/CROSS_FIELD_INVENTIONS.md). These familiar task distinctions are worth including for explanatory value, irrespective of novelty.
