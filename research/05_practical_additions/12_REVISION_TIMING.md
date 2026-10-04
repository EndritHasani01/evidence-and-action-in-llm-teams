# 12 — Earlier versus later corrections

**Recommendation: include zero-call prefix-progress analysis; keep a live timing experiment optional.** A clean live version is more expensive than merely saving another checkpoint.

## The idea and question

Ask **whether additional collaboration before a correction makes recovery easier through gathered evidence, or harder through more entrenched derived work**. This is intuitive and relevant to a team that has worked for minutes versus hours. The current PS fixes correction after four rounds, so it cannot answer the causal timing question directly.

The idea uses ordinary checkpoint branching. Its value is the operational comparison, not a new checkpoint method.

## First choice: use existing prefix traces

For rounds 1–4, show old-world exact accuracy, acquired remote-source coverage, history token count and communication volume. Link each world's fixed round-four recovery result to this prefix profile descriptively.

This costs **0 model calls** and roughly **half a day to one day** beyond the ordinary analysis. It shows what “substantial collaborative work” actually means in the experiment. It does **not** establish how the same world would have recovered if corrected earlier. Do not label a correlation between long histories and poor recovery as a timing effect.

## Smallest live comparison worth considering

Predeclare a timing subset before any model output—for example, two worlds per family, 12 worlds total. Save the immutable checkpoint after round 2 as well as the normal round-4 checkpoint. Apply the **same already-chosen edit** at both boundaries. Give both timings four recovery rounds.

The normal round-4 B/C changed and sham branches already exist. At round 2 add:

| New sibling | Calls per selected world |
|---|---:|
| B after change | 16 |
| C after change | 16 |
| B after sham | 16 |
| C after sham | 16 |
| **Added total** | **64** |

Twelve worlds therefore add **768 main calls**: 6,624 main calls with the 48-world core or 5,256 with the 36-world core. At an illustrative 15 allocated seconds/call, the increment is 3.20 GPU-hours before overhead and margins; this is not a throughput forecast. Testing the early branches on one existing development world adds 64 pilot calls if a live check is needed, within the same development cap. Estimated implementation/analysis work is **2–4 focused days**, assuming the PS's immutable checkpointing already works.

Two changed branches alone would cost 32 calls/world, or 384 on 12 worlds. That cheaper comparison is legitimate for corrected-world B versus C at different ages, but it cannot isolate whether timing changes the *correction-specific* reset effect; the generic benefit of clearing an older history can also differ. State that weaker question if choosing the cheaper option.

## What is matched, and what is intentionally different

The first two uncorrected rounds are shared, not regenerated. The round-four prefix continues along the original uncorrected branch, not along an early-correction branch. Reuse is valid only when the exact first-two-round prompts, settings, seeds and deliveries match. If the prompt announces correction specifically after round four, an early-correction experiment needs a prospectively consistent prompt; cached responses from a different prompt cannot be reused as though identical.

Every branch starts after its boundary's messages have been delivered, with no pending pre-boundary messages. Never choose “early” or “late” according to when the model first becomes correct. All generated worlds remain included, including poor early prefixes.

Extra pre-change collaboration intentionally changes source coverage, old-answer quality, history length and computation already spent. The identified question is the effect of that **timing package**, not a pure psychological effect of memory age. Recovery budgets are equal; end-to-end costs are not. Report both.

For each timing t, retain the PS-style contrast `theta_t=(C-B)_change,t-(C-B)_sham,t`; compare theta_2 with theta_4 within world. World clustering and task balance remain necessary. Twelve timing worlds are a small descriptive study, not a basis for a general time law.

## Why not simply add a later boundary?

A round-six boundary requires eight new uncorrected prefix calls plus 64 changed/sham B/C continuation calls per world: **72 calls/world**, or **864 on 12 worlds**. The original B-sham continuation is not automatically a valid replacement for those two new prefix rounds, because its neutral boundary notice changes the prompt. Longer histories also need a fresh worst-context audit.

## Possible outcomes

- Later correction could help because the team already gathered the needed evidence.
- It could hurt because useful and obsolete state become harder to separate.
- B/C could change equally after change and sham, suggesting generic history effects.
- All timings could recover similarly, making a fixed four-round boundary an adequate practical choice in this regime.

Each is useful, but timing should **not displace an affordable 48-world core or its sham controls**. Prefer the zero-call prefix profile first. Select at most one live addition for the bachelor project; timing should compete with candidate-only retention or receipt delivery rather than accumulate beside both.

Basis: [PS shared prefixes, synchrony and budget](../../PROJECT_SPECIFICATION.md), with the earlier [timing/path-dependence cautions](../04_design_extensions/CROSS_FIELD_INVENTIONS.md).
