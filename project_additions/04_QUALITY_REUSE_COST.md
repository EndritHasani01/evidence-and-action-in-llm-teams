# Addition 04: make the quality, retained-work, and cost tradeoff visible

**Recommendation: include a compact paired cost analysis. Zero additional model calls.**

**Simple idea:** show whether a recovery policy buys better answers, less collateral damage, or earlier recovery at a reasonable measured cost. Keep the amount of retained evidence visible without pretending that retained bytes prove useful computation was reused.

**Status:** plan for analyzing future PS inference records. No actual Qwen/T4 timings or recovery quality measurements exist yet. The v2 budget files contain call arithmetic and illustrative rates, not measured performance.

## Question and value

If clearing history helps accuracy, does it also shorten prompts and reduce inference cost? If retaining evidence helps compared with F, how much acquisition was actually avoided? When quality is similar, is there a clearly simpler or cheaper operational choice?

This turns a ranking of accuracy into a usable research conclusion. It also keeps the thesis honest about what “preserving work” means in a four-round experiment rather than an hours-long deployed system.

## Already in the PS versus the addition

The PS already requires prompt/output tokens, elapsed time, allocated GPU-hours, retained source evidence comparisons, and abandoned-prefix accounting for F. The addition is a coherent reporting view: one quality-versus-cost figure, a paired comparison table, and a precise separation of *retained inventory*, *observed outcomes*, and *actual spending*. No new economic model or learned policy is needed.

## Minimum worthwhile analysis

1. Plot task-balanced mean recovery AUC against measured continuation allocated GPU-seconds for B/C/L/F. Show uncertainty or the underlying paired points; do not report a precise frontier from four noisy means alone.
2. For the three existing contrasts C–B, B–L, C–F, report paired differences in AUC, final team completion, continuation cost, and the relevant preservation/evidence diagnostic. Avoid turning these into a new combined “utility score.”
3. Include a small accounting table with actual scheduled/executed calls, prompt tokens, generated tokens, failed attempts, and total allocated GPU-hours. Separate main runs from setup/development/reserve use.

One plot and one table are enough for a minimal version. Per-family cost breakdowns can go in the appendix because output lengths and inference difficulty differ across families.

## Data and formulas

Use world/task/prefix/policy/event IDs; stable call/attempt IDs; actual prompt/output token counts; executed/failed/missing status; worker/device allocation intervals; per-call elapsed time; prefix/continuation boundaries; and exact recovery outcomes.

For world w and policy p:

- `G_recovery[w,p]` is the sum of actual allocated GPU-seconds attributable to all continuation attempts, including capped failures and the stated allocation of idle overhead.
- `G_workflow[w,p] = G_prefix[w] + G_recovery[w,p]` is the counterfactual end-to-end cost of choosing that policy after the same prior work.
- `delta_A[w] = A[w,p] - A[w,q]` and `delta_G[w] = G_recovery[w,p] - G_recovery[w,q]` are paired policy differences.

Two distinctions are essential:

**Physical experiment cost:** the shared prefix was executed once, so the real GPU ledger counts it once. **Policy/workflow accounting:** each hypothetical policy began after that work was spent, so each end-to-end comparison includes the prefix. Do not sum the counterfactual workflow columns to claim actual experimental spending. F does not get to erase the cost of its abandoned prefix.

**Elapsed time versus allocated device time:** two simultaneously allocated GPUs for one hour consume two aggregate GPU-hours. A shorter wall-clock run is not automatically cheaper. Use the PS's measured allocation convention, recording idle periods, startup, interruptions, and retries. Do not extrapolate current throughput from an earlier model or from the v2 illustrative seconds-per-call table.

The fixed continuation allowance contains 16 scheduled calls per complete branch. A policy may use fewer tokens or less allocated time, but it does not save scheduled calls by becoming correct early. “Cost to first stable correct round” is an evaluator-assisted retrospective description only, because correctness is unavailable to a deployable stopping policy and later regression must be observed to establish within-window stability. Any separately proposed stopping rule needs its own clearly labeled offline analysis and is outside this minimal cost comparison.

## What to call reuse

Keep three quantities distinct:

| Quantity | What it means | Useful comparison |
|---|---|---|
| Retained current remote-source inventory | Previously gathered authenticated records available at recovery start. | C versus F, using [Addition 03](03_COMMUNICATION_AND_INFORMATION_FLOW.md). |
| Preservation of previously correct unaffected outputs | Existing correct results survived the correction/recovery episode. | C versus B and answer-preserving controls. |
| Actual prompt/completion/acquisition cost | Measured work performed by the runtime under the fixed protocol. | All policy contrasts. |

None alone measures hidden reuse of the model's computation. More retained records can be unused. Fewer tokens can accompany worse answers. An unchanged answer can be recomputed from scratch. Say “retained evidence,” “preserved output,” and “measured cost” instead of inventing a single work-saved percentage.

Count actual source delivery attempts and unique newly acquired records, but do not convert them into saved GPU-hours or money without a measured relationship. The benchmark's tiny arithmetic/source records do not establish savings after days of expensive tool work.

## Decision rules for interpreting the plot

- A policy with better quality and lower measured mean cost is an attractive observed tradeoff. Show paired uncertainty before claiming it consistently dominates another policy.
- Similar point estimates do not establish equivalence. If intervals remain wide, say the tradeoff is unresolved.
- If costs differ but quality is effectively indistinguishable within defensible bounds, a cheaper simpler policy becomes a practical choice in this tested setting.
- If higher quality costs more, report the two-dimensional tradeoff. Do not choose an arbitrary price per correct answer or hide the cost increase inside a normalized score.
- A positive correction-specific theta does not by itself imply a practically useful C advantage. Show the actual changed-event C–B quality and cost differences alongside the sham comparison.

World-level paired resampling remains the uncertainty unit. Match cost and quality coverage; incomplete branches require explicit accounting and bounded outcome sensitivity, rather than a favorable complete-case quality/cost plot. Failures consume resources even when they earn zero accuracy.

## Extra cost and effort

**Extra inference: 0.** Approximately 1–2 focused analysis days once timing/attempt logs are reliable. The difficult prerequisite is accurate runtime cost instrumentation already required by the PS; this estimate excludes implementing it and performing the original pilot. Existing statistical and plotting tools suffice.

The four analysis proposals share their outcome/trace tables. Their effort estimates should not be added as though each requires a separate data pipeline. A compact, reusable analysis table is preferable to four bespoke reporting systems.

## Interesting outcomes, including negatives

- C improves quality and reduces prompt-time cost: a simple reset has both scientific and operational value.
- B preserves quality better despite longer contexts: accumulated derived work earns its cost under this protocol.
- C outperforms F without a large inference-cost difference: authenticated evidence reuse matters even when raw arithmetic is cheap.
- F matches recovery quality but loses more unaffected correct outputs: endpoint accuracy alone misses a useful continuity cost.
- All policies have essentially the same complete-schedule cost: do not promise compute savings; the contribution concerns quality and preservation under equal opportunity.
- Measurement noise or missing blocks prevents ranking costs reliably: report the uncertainty instead of relying on token counts as a substitute for GPU allocation.

**Minimum recommendation:** pair existing quality outcomes with actual measured continuation cost and explicit retained-evidence/output-preservation summaries. This is useful whether the final result favors retention, reset, restart, or no meaningful difference.

## Sources

Grounded in [PS §§6 and 8](../PROJECT_SPECIFICATION.md), the v2 [budget arithmetic](../research_innovation_v2/evidence/budget_and_precision_results.json), and [final review](../research_innovation_v2/reviews/FINAL_DESIGN_REVIEW.md). The additions-pass read ledger is in [Addition 01](01_RECOVERY_TRAJECTORIES.md#sources-and-read-scope). Prior forecast examples remain planning calculations; all claimed practical costs must come from the eventual measured run.
