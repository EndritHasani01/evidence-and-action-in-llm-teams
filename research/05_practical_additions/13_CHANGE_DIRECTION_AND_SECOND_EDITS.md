# 13 — Direction of change

**Recommendation: include simple CPU direction examples.** A small opposite-direction sibling is a reasonable alternative live addition if it becomes the thesis's chosen extension. A second consecutive correction is a separate addition in [18 — Second revision](18_SECOND_REVISION.md).

## Some corrections preserve the useful part of an old answer

Ask **whether making an old winner stronger differs from making it cease to be the winner**. Raising a known global maximum can leave the old answer almost sufficient; lowering it can require a runner-up that the answer discarded. Similarly, a top-K update can require an omitted next-ranked value. These examples explain why “one source changed” is not a uniform recovery difficulty.

This follows familiar incremental-maintenance behavior. It remains a clear and useful thesis explanation.

### Zero-call version

Include two or three exact numeric examples beside the six-task analysis. For existing Prefix Sum, Difference Array and Sort main events, record numerical direction and magnitude from the original and revised input. Analyze their existing outcomes descriptively only; direction was not separately balanced with every other task property.

Cost: **0 model calls**, roughly **half a day to one day** when the oracles exist. This should be included if it clarifies the observed task differences.

### Small live sibling

Keep the current main edit. On a predeclared numeric-task subset, consider its mirror edit: if old value is v and main new value is v+d, the sibling uses v−d at the same record. Only include worlds where that replacement is within the original numeric bounds and changes the mathematical answer, with eligibility determined before model inference. The opposite-direction event intentionally differs from the original winner-lowering selection rule in Maximum/Top-K; document that added event rather than pretending it satisfies the original rule. Do not regenerate successful-looking worlds or silently expand 0–99 or 1–9 ranges.

Run B/C on this alternate event from the **same original prefix**, not after the main event. Existing B/C sham branches can be shared across the two event comparisons. The addition costs **32 calls per eligible world**. For m=12 it is 384 calls, but m is not guaranteed: range boundaries and task constraints may leave fewer eligible worlds. Report the eligible population and denominator. At an illustrative 15 allocated seconds/call the increment is `32m/240` GPU-hours, or 1.60 hours at m=12, before overhead. Estimated additional implementation/analysis work: **1–3 days**, plus up to 32 calls for one development-world check within the existing pilot cap.

Prefix and Difference Array are the cleanest mirrored examples: the affected coordinate set is unchanged for opposite nonzero deltas at the same position. Sort can move across different rank intervals despite equal numeric magnitude. Maximum's original winner-lowering rule is deliberately asymmetric: a mirrored increase may exceed 99, and when legal the revised maximum can be immediately apparent from the broadcast value. That is a real operational contrast, but not a pure causal estimate of abstract “incremental difficulty.” Top-K can still require a different omitted replacement.

If the desired experiment uses two entirely new balanced up/down edits rather than one existing event and one mirror, B/C for both costs **64 calls/world**. Do not present this as the cheaper 32-call design. A smaller coherent task-specific comparison is preferable to an underpowered six-family direction average.

## Recommendation and outcomes

Choose the CPU direction examples now. A live opposite-direction sibling could show a strong asymmetry, show that both edits recover equally well, or show that the expected arithmetic distinction is overwhelmed by initial model errors. All three outcomes help interpret the benchmark. The current raw-source bounds, unchanged prefix and matching edit magnitude make the result easier to explain than a broad new task suite.

Keep this as an alternative to other live additions, not an accumulating requirement. Eligibility can leave a very small sample, so a CPU illustration may be the better thesis choice. Do not reduce an affordable main sample or remove sham controls to fund a direction experiment.
