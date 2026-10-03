# Eventual specification changes

**Research plan only. No implementation code. PROJECT_SPECIFICATION.md has not been edited.** This plan follows the research-phase recommendation and independent reviews; actual inference feasibility and scientific results remain untested.

## Revision scope

Preserve the governing question: how should a distributed team recover after formerly valid information changes while retaining useful work? Add a focused question about historical transition information as a condition for useful reuse. The addition is an attributed experimental dimension, not a new recovery algorithm or replacement thesis.

| Existing PS section | Proposed scientific change | Preserve |
|---|---|---|
| §1 Research decision | Add the secondary question and distinguish current evidence, historical transition evidence and derived work | Main question, four-peer/six-family scope, B/C/L/F and primary theta |
| §2 Prior research | Incorporate current source/version notes for CIR, ICR, StateAuditor, RIAG, PlanFence v2, transition/wording and classical IVM/CDC; narrow novelty claim | Explicit replication/generalization framing and unresolved-source caveats |
| §3 SILO foundation | Add only the observation that output placement and information compressed into summaries matter for update sufficiency | Existing mathematical task attribution and native-runner/evaluator cautions |
| §4 Worlds/interventions | Mark every Prefix Sum/Sort main world as a focal receipt world before inference; no new world/event distribution | Seeds, owner balancing, correction selection, all six tasks, answer-preserving subset, no performance-based generation |
| §5 Protocol/state | Define a persistent authoritative correction notice outside derived history; before-value not included in standard notice and explicitly historical in Δ notice; add BΔ/CΔ only for focal changed events | Current source table/version replacement, private evidence, synchronous four-round phases, B/C history treatment and L/F semantics |
| §6 Evaluation | Prespecify first-round eta1 over the two focal families; eta_A and full trajectories descriptive; introduce limited observable-state/atlas annotations | Six-family AUC theta as sole primary, exact grading, U/D diagnostics, failed-prefix inclusion, world clustering |
| §7 Records | Record receipt mode and exact rendered notice separately from history; archive observable-state audit outputs offline | No semantic extractor, no new model, no oracle feedback; branch/cache isolation and bounded retries |
| §8 Feasibility | Add 512/384 main calls only if whole schedule fits; add 64 pilot calls on two focal development worlds; preserve core-first decision order | 30-hour ceiling, three-hour development cap, setup/rerun reserves, Qwen/T4 gates and 48/36 core rules |
| §9 Checks | Verify identical B/BΔ and C/CΔ current tables, raw archived before-values, temporal-role rendering, no delta/gold leakage, exact focal-pair accounting | Existing independent oracles, protocol/isolation checks, no within-round visibility, all outcomes counted |
| §10 Boundaries | State local pre-communication theorem scope, interface/presentation ambiguity, two-family/small-n empirical scope, unchanged receipt-sham coverage, no savings from fixed calls | Original hardware/model/team-size and exact-task limitations |

## Normative details to settle in that revision

1. **Receipt wording:** the after-only field says “not included in this receipt,” never that the runtime or retained history lacks the value. The enriched receipt labels v1 as historical and v2 as current. It supplies old/new raw values, not their arithmetic difference or a repair procedure.
2. **Rendering lifetime:** both receipt modes remain available across recovery calls outside the clearable history. This avoids C losing the assigned intervention after one call. Generic instructions, total context cap, output cap and prompts otherwise match.
3. **Token control:** freeze a minimal common schema and accepted-tokenizer matching convention before the pilot; disclose that token matching does not equalize salience. Do not add unbudgeted factorial wording arms.
4. **Delivery:** Δ modes apply to broadcast B/C only. L still gives new content only to the owner and the announced-change metadata to others; F still restarts from corrected private evidence plus the broadcast revision. No hidden receipt enrichment of L/F.
5. **Focal scope:** all Prefix Sum/Sort worlds, never a subset selected by prefix success, old-value visibility, effect direction or recovery difficulty. Core no-change and answer-preserving runs remain exactly the designated policy/event comparisons; no claim that receipt is crossed with those events.
6. **Estimator:** `eta1 = (a[CΔ,1]-a[BΔ,1])-(a[C,1]-a[B,1])`. Negative favors retaining history relative to reset. Show both direct receipt effects. `eta_A` uses the same contrast on four-round AUC. Balance two focal families; cluster at base world/prefix.
7. **Inference designation:** recommend one prespecified exploratory secondary eta1 with descriptive 95% paired uncertainty and no new significance claim; keep original primary/secondary multiplicity conventions. If confirmatory status is desired, revise the family/error-control plan before running, not after seeing results.
8. **Capability and budget decision:** preserve an affordable 48-world core even if receipts must be omitted. If core timing already requires 36, include receipts only when 36 plus all focal branches fits. Same rule for development: no extra quota and no extra model configuration without charging it.

## The theoretical addition to state explicitly

Define update sufficiency only relative to a named observable representation and edit payload: indistinguishable observations must imply the same revised target for a universally correct updater to exist. Attribute the principle to incremental maintenance/observation arguments. Include constructive prefix/sort gaps, the difference-anchor redundancy result, and max/top-K/BFS discarded-alternative limits. A correct-summary proof is evaluator-side reasoning, not a guarantee that an LLM's actual summary is correct.

The complete scripted-B witnesses concern one peer before new messages, with permitted aggregate prose and no forwarded raw records. They show that after-only recovery can require new communication. They do not prove that naturally sampled prefixes often create this condition, nor that no four-round team policy can recover. Keep this limit next to the result.

## What should remain untouched

Do not replace the six-family study with a search benchmark. Do not add completion obligations, training, a reviewer model, a semantic provenance graph, a vector database, a current-answer validator, a learned router, extra peers, asynchronous serving or a topology sweep. Those candidates failed the joint novelty/identification/cost comparison for this phase.

Do not remove the original sham, answer-preserving revisions, fresh restart, local delivery, recovery trajectories, exact D/U analysis, protocol failures or allocated GPU accounting. Do not reinterpret static graph topology as a causal exposure measure. Keep source occurrence, observed delivery, semantic dependence and actual stale influence distinct.

## Expected scientific gain and cost

Gain: a sharply defined runtime choice and a theoretical account of when retained work needs historical operands, additional alternatives, or more communication. The original primary results remain interpretable even if the addition fails.

Cost: about 9% more main calls for the corresponding core schedule, two extra focal pilot continuations per world on two worlds, and a small rendering/analysis extension. Eta1 has only 12/16 clusters and may be inconclusive. Full original-core precision takes priority over buying the extra experiment.

A later specification revision should adopt this entire bounded package or explicitly document a changed tradeoff. It should not copy only the favorable novelty language while dropping the controls, cost gates or falsification rules.
