# 18 — Can the team recover a second time?

**Recommendation: add a few CPU version-transition checks; defer a live second-edit matrix.** Additional model calls: 0 for checks; 64 per selected world for the smallest fully controlled live comparison described below.

## The idea and question

Ask **whether recovery remains usable after another authoritative change, or whether problems accumulate**. This is practically relevant to agents working on a changing task for a long time. The current PS studies exactly one correction; a successful first recovery does not establish successful repeated recovery.

The useful distinction is between a factual input returning to a prior value and the team returning to its earlier knowledge state. Familiar repeated-update and path-dependence ideas can make a good follow-up without needing a new mechanism.

## CPU protocol checks first

Use deterministic mock cases to verify v1→v2→v3 replacement, source-forwarding version checks, and that clearing history cannot restore an older value. Repeated correction correctness is useful implementation assurance even if the scientific matrix stays at one edit.

Cost: **0 model calls**, approximately **half a day to one day** during protocol work. These checks establish version-handling behavior, not evidence that an LLM adapts successfully twice. No such tests or model runs are implemented by this proposal.

## A minimal live repeated-revision study

Choose the end of the original **B changed-event continuation** as the fixed parent for every selected world. From that same frozen state, fork retain/clear × second change/sham, four new four-round continuations:

| Second-stage event | Retain prior history | Clear prior history |
|---|---:|---:|
| Second authoritative correction | 16 calls | 16 calls |
| No second change | 16 calls | 16 calls |
| **Added total** | **32** | **32** |

This costs **64 calls/world**, or **768 on 12 predetermined worlds**, plus up to 64 development calls on one predetermined world if needed. With the intact original core, totals become 6,624/5,256 main calls for the 48/36-world schedules. At an illustrative 15 allocated seconds/call, 768 calls add 3.20 aggregate GPU-hours before overhead and margins. Actual measured forecasts and the original 30-hour cap govern admission. Estimated additional work is **3–5 focused days** for second-event generation, bookkeeping, context validation and analysis.

The comparison asks about a second recovery after one particular first-stage policy, B. It does not test all two-stage policy sequences. If both prior B and prior C are used as separate parents and each receives all four second-stage siblings, the cost doubles to **128 calls/world**. Prior B and C states are different; comparing them alone at stage two does not restore a shared-prefix second-stage contrast.

Choose the subset and second edit by a frozen rule before model outputs. Compute exact second-world answers independently. Do not require first-stage success for inclusion; show it as an offline pre-second-intervention stratum with a clear denominator. All four siblings must receive identical current raw evidence at their shared second-stage boundary except for the actual event intervention.

Four extra history rounds can exceed the original 8,192-token cap. Audit the maximum context before inference; silently truncating a retained branch would change the treatment. A permitted graph-edge restoration also needs an explicit version-3 live-edge event, not an assumption that a deletion-only adapter already implements it.

## Optional variant: return to the original truth

A cycle x→x′→x does not by itself demonstrate harmful path dependence. A same-final-world comparison can use the existing B-change and B-sham parents: return the changed parent to x, leave the sham parent at x, then apply retain/clear to each. This again adds **64 calls/world**. It is an alternative to the preceding matrix, not another included component.

Both paths have equal scheduled call counts and the same final source values, but their acquired evidence, rendering and histories can differ. Any result is the total effect of prior revision history. It is not proof of a hidden anchoring mechanism or of identical available information. Careful source-view reporting matters more than adding another named metric.

## What the results could teach

- Good second-stage recovery would broaden the practical coverage of the original finding.
- Deterioration despite a successful first stage would reveal an accumulation problem worth investigating.
- A benefit of clearing after the second event could motivate periodic cleanup, though a two-event result alone would not establish an optimal schedule.
- Widespread first-stage failure or context overflow could make the extra matrix uninformative; report that limitation rather than treating it as evidence of a semantic recovery principle.

These are useful questions, but the extra calls, longer contexts and more complex interpretation make them a follow-up choice. The single-correction PS already supports a coherent bachelor thesis. Prefer its complete sample and controls, add CPU checks now, and select repeated revisions only if it becomes the one clearly prioritized live extension.

Related alternatives: [change direction](13_CHANGE_DIRECTION_AND_SECOND_EDITS.md) and [revision timing](12_REVISION_TIMING.md). They should compete for budget rather than automatically be combined.
