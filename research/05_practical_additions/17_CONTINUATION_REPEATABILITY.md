# 17. A small repeatability check

**Recommendation: reserve as an alternative use of spare inference, not part of the minimum package. Extra main calls: 384 for the smallest balanced check.**

## Idea and question

Repeat the changed-event B/C continuations from a fixed subset of the same saved prefixes using a new, independently assigned continuation seed. Do the broad observations survive another sample from the model, or are policy differences highly variable?

This repeats recovery, not the initial collaboration. The question is conditional repeatability given those particular prefixes; it does not estimate variability over new prefixes for the same base world.

## Why it is useful

The PS has one continuation sample per policy/world. World-level inference already accounts for outcome variation across worlds, but it does not reveal whether an apparent per-world policy winner is stable across generation seeds. This check can make a modest thesis more credible, particularly when trace anecdotes otherwise look definitive.

No novelty claim is needed. Its disadvantage is that it strengthens confidence rather than adding a visibly different recovery capability.

## Minimum experiment

Choose 12 main worlds before inference, two per task, using the frozen seed-list order. Keep their original prefixes. Add one new B and one new C changed-event continuation with matched new per-world/peer/round seed assignments across the two arms. Each repeat is a complete four-round branch; use distinct replicate IDs so response caching cannot return the original sample.

Cost: `12 worlds × 2 policies × 16 calls = 384` extra calls. Repeating B/C sham as well would cost another 384 and is **not** part of this minimum check. Thus this design assesses changed-event C−B repeatability, not the reliability of the full change-minus-sham primary interaction.

Keep the original first replicate for the original primary analysis. Report the two C−B contrasts per selected world, sign agreement with a separate tie category, and whether qualitative trajectory labels persist. If averaging repeats is explored, label it separately and retain base-world clustering. Two samples do not produce a reliable per-world variance estimate.

## Effort and budget

Roughly one to two working days for replicate IDs, independent-seed scheduling, resume/cache checks and paired displays. Existing model/schema capability is unchanged, so no additional full pilot is necessary. Validate replicate identity on CPU; if a live smoke repeat is needed, explicitly charge up to 32 development calls rather than hiding it in the main budget.

At illustrative 15 allocated seconds/call, 384 calls cost 1.60 aggregate GPU-hours before extra overhead. Actual phase-specific timing, setup and failed attempts determine feasibility. This addition competes for the same spare budget as compact-state recovery; do not include both automatically.

## Interesting outcomes

- Policy direction and recovery shapes persist: stronger support for the original narrative within these prefixes.
- Average differences persist but individual winners flip: report aggregate effects and avoid deterministic per-world explanations.
- Results vary greatly across repeats: the thesis should emphasize uncertainty and bounded conclusions instead of mechanism anecdotes.
- Only selected tasks are variable: useful motivation for future replication, but two worlds per family cannot establish a task-level variance law.

Prefer compact-state recovery if the goal is one simple new mechanism comparison. Prefer this check if implementation already supports only B/C/L/F and the largest remaining concern is stochastic stability. Decide the allocation before observing main policy differences; do not buy repetitions only for favorable or surprising worlds.
