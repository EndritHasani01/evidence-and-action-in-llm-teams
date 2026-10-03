# Independent final scientific-design review

Reviewer: protocol/source investigator. Date: 2026-10-04. This review assesses proposed design and executed CPU evidence; no live model effect, hardware performance, or novel algorithm has been established.

## Focused estimand: prefer immediate recovery, retain full trajectories

The extension should predeclare

`eta_1 = (a[C_delta,1] - a[B_delta,1]) - (a[C,1] - a[B,1])`

as its focused descriptive secondary estimand, with the same interaction on four-round AUC, `eta_A`, as a required trajectory companion. The existing six-family sham-adjusted AUC interaction `theta` remains the project's primary estimand.

This choice is scientifically preferable to making only `eta_A` the extension's focus. Every peer's first recovery generation occurs before any new recovery message is delivered. The constructive indistinguishability result applies exactly at that boundary: a specific retained local view plus replacement notice can be compatible with different revised answers. New communication can resolve that ambiguity later. Averaging across later rounds asks an additional question about how consequential the immediate deficit remains under recovery, which must be reported but is not identical to the information argument.

This is a prospective choice made before model data exist. It is not justified by a more favorable observed effect. It **does not automatically increase power**. If all differences occur in round one and later contrasts are zero, `eta_A = eta_1 / 4`, and its standard deviation also scales by one quarter. Standardized signal is then unchanged. Any precision difference depends on the covariance and variation of later-round outcomes, which are unmeasured.

Mandatory interpretation safeguards:

- Report the direct receipt effects `B_delta-B` and `C_delta-C` at round one, plus all four cell means. A negative interaction can mean harm to C rather than benefit to B.
- Preserve four-round AUC, final/stable correctness, full recovery curves, and unaffected-coordinate preservation. A first-round improvement followed by regression is not evidence for deploying the interface by default.
- First-round failure is not team impossibility. The edited owner or another informed peer can supply missing information in the next call boundary.
- With 12/16 focal world clusters and two families, treat the interaction as focused exploratory evidence. Peers, coordinates, and rounds are not extra independent samples.
- Select this endpoint before the pilot and retain it regardless of whether its direction looks attractive. Capability/cost, not effect signs, determine admission.

### Illustrative one-round lag arithmetic

Assume a correct old prefix, that only downstream nonowner peers need the missing before-value, that the edited owner sends it during recovery round one, and that recipients recover perfectly in round two without a receipt but in round one with it. Assume C receives no benefit and no policy suffers collateral harm. These are illustrative assumptions, not observed behavior.

If edited owners 0, 1, 2, 3 are balanced, the numbers of downstream nonowner peers are 3, 2, 1, 0: an average 1.5. Receipt benefit is then `1.5/4 = 0.375` in first-round B accuracy and `1.5/16 = 0.09375` in B's four-round AUC. Therefore `eta_1 = -0.375` and `eta_A = -0.09375`. This is not an upper bound: real models can suffer prolonged failures, owner uncertainty, and receipt-induced errors. It shows why the immediate capability and total recovery value should both be visible.

## Review of the proposed interface

The factorial is appropriately narrow if B/C remain identical in current source evidence within each payload pair, each receipt arm receives the same authenticated historical record, and only the raw old/new values plus version roles are added. No arithmetic delta, affected-output mask, update formula, or semantic correction is supplied by host code.

The historical record is additional information, potentially new to peers that never saw its old version. This is not oracle leakage, because the source/update system already owns that information, but it is an intentional dissemination change and must be counted. The old version must remain absent from the authoritative current table. Rendering it outside resettable history prevents C from accidentally deleting the treatment.

Consistent layout and tokenizer accounting are useful. Neutral padding cannot equalize salience or attention, so the empirical estimand remains an interface effect. In particular, explicit before/after framing may help even when B already contains the before-value. That outcome weakens a missing-information explanation without invalidating the interface comparison.

## What the CPU evidence does and does not show

The executed [probe](../evidence/protocol_probe.py) establishes mathematical and structural facts. The complete [audit](../evidence/PROTOCOL_AUDIT.md) records limitations and the source read ledger.

- Five 32-record pairs have identical designated-peer candidate/current-private-evidence views and different revised required answers.
- Two stronger scripted prefixes produce identical complete designated-peer B views, including received prose and candidate history, for Prefix Sum and Sort. Their before-values differ and their required new answers differ.
- These are legal information-flow constructions, not naturally sampled Qwen traces. They must not be injected into main runs and then called natural failure evidence. Exact tokenizer validation of the constructed text was not executed.
- The probes establish no universal need for historical values. Difference-array outputs plus an unchanged current anchor reconstruct the old array. Fully acquired current sources permit fresh exact recomputation without old values.
- Sort can still need a remote boundary value with an explicit delta; max/top-K can need previously discarded reserves; BFS can need alternative topology. An event receipt is not a recovery oracle.
- The temporal cone enumeration demonstrates ordering sensitivity and both saturation and nonsaturation possibilities. It cannot supply natural LLM prevalence or infer true semantic dependencies.
- The observed-edge cone must specify its channel model. Message absence, routing, and retained-evidence selection can carry implicit old-world influence; actual delivered edges alone do not bound every such channel. No unconditional information-flow safety claim follows.

The strengthened complete-B witnesses were added during this investigation, and the full assertion suite was rerun afterward successfully. Old audit results were parsed and source/data hashes rechecked; earlier all-task oracle results were not rebranded as newly reproduced experiments.

## Feasibility and main-study protection

Reviewed the proposed 6,368/4,872 main-call schedules and 652-call extended pilot (676 with the separate maximum smoke screen). These agree with the branch arithmetic: two new 16-call continuations on 16/12 focal main worlds, and on two existing development worlds. The example time conversions are arithmetic, not measurements.

Prioritizing the original 48-world core over dropping to 36 to purchase exploratory receipt arms is scientifically sensible. The extension should be omitted if its full measured cost does not fit the hard 30 aggregate GPU-hour ceiling. The mathematical atlas and zero-call trace analysis still strengthen interpretation. No favorable pilot treatment effect is needed for admission; no unfavorable effect should cause selective omission.

## Novelty and thesis scope

Before/after change records, incremental updates, and preservation of historical truth are established principles. The candidate's defensible contribution is a measured interaction between correction information and retention of opaque collaborative state, supported by exact information limits in the existing task environment. A positive performance difference alone does not establish a new algorithm or first-of-kind general recovery system.

The original PS already estimates a valid total retain/reset effect. Loss of old values with old history is part of that treatment. The extension refines what a runtime should communicate; it does not repair a supposedly invalid original experiment. Preserve this distinction in the thesis narrative.

The previous completion-reopening direction remains a legitimate competitor, but adding a query/closure lifecycle would alter the existing experiment more substantially and faces a control-dependency reduction. Nothing in the inspected protocol forces that redirection. A focused interface study is a reasonable lower-cost research bet, conditional on literature positioning, capability, and actual timing.

## Final synthesis review and requested wording corrections

Read the completed `RECOMMENDED_EXTENSION.md`, `FALSIFICATION_PLAN.md`, and `SPECIFICATION_CHANGE_PLAN.md` in full, plus `FINALIST_EXPERIMENTS.md`, `FEASIBILITY_AND_VALUE.md`, and `sources/TRANSITION_RECEIPT_NOVELTY.md`. Rechecked the revised first-round estimand and the complete-B counterexample/sufficiency code. The proposed `eta_1` focus is independently recommended for conceptual alignment, with the restrictions above.

Two interpretation statements required tightening:

1. **An early benefit does not identify a communication mechanism.** A first-round gain establishes earlier correctness before newly generated peer messages arrive. It is consistent with a reduced information/acquisition/recomputation delay but can also reflect salience or convenient presentation. The recommendation's first-round-only outcome row and falsification decision must use outcome-level language unless the trace/representation evidence supports the stronger explanation.
2. **A zero interaction is not zero interface value, and the endpoint matters.** Precisely small `eta_1` establishes stability of the immediate retain/reset contrast only. Stability of the original changed-event AUC contrast also requires appropriately bounded `eta_A`. Both B and C can benefit substantially and equally, yielding a zero interaction without making the receipt unnecessary. Recommending the simpler interface requires considering bounded direct effects, harms, and cost, not interaction size alone. Receipt-by-sham behavior remains untested.

These are wording/interpretation fixes, not reasons to reject the factorial or add inference arms. The final design otherwise preserves the governing scientific question, exact observation boundary, prior-art humility, no-oracle contract, matched controls, exploratory inference designation, original sample priority, and compute ceiling.

**Closed after verification:** both corrections were incorporated into the final recommendation and falsification text and then checked again. First-round-only benefits are now described as earlier correctness, with communication/recomputation attribution conditional on additional evidence. Near-zero interaction language now distinguishes `eta_1`, `eta_A`, and direct receipt effects/cost. No remaining must-fix scientific-consistency issue was found in the completed recommendation, falsification plan, or specification-change plan. This closes research-design review only; capability, timing, empirical utility, and final novelty positioning still require the declared later evidence.
