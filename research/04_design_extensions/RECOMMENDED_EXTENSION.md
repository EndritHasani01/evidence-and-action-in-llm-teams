# Recommendation: test what a correction must preserve to make prior work reusable

**Decision: add one focused experimental dimension to the existing PS, supported by an exact analysis of recovery information. Preserve the original study as the core.**

The strongest feasible addition found in this investigation is to test whether **the value of retaining collaborative history depends on whether the correction supplies the former input value as well as the current one**. This is a question about recovery of accumulated computation, not a replacement thesis about search completion. A small before/after receipt is the instrument; it is not claimed as a new algorithm.

Research review completed 2026-10-04. `PROJECT_SPECIFICATION.md` and the entire earlier `research/03_innovation_review/` workspace remain unchanged. No model inference, GPU timing or recovery advantage is claimed.

## Why this is a substantive addition

The original design asks whether retaining or clearing prior reasoning is preferable once current source evidence is held fixed. That is a strong policy comparison. The new investigation exposed an additional distinction inside it:

- **Current evidence** states what is true now.
- **Historical transition evidence** states what the previous input was and what replaced it.
- **Derived work** contains results, summaries, plans and explanations produced from previous inputs.

An obsolete value should lose authority as a current fact. Yet the same value can remain a legitimate operand for revising an old calculation. The PS replaces v1 in active source tables and guarantees v2, while B may preserve v1 incidentally in discourse and C removes that discourse. Thus equal current evidence does not imply equal transition information. The original C−B effect is still valid: removing that information is part of removing history. The proposed extension asks whether an explicit runtime information contract changes its interpretation and practical result.

This changes the thesis from only “which recovery package works?” toward “what must remain observable for already-computed work to be reusable, and does the team exploit it?” It is a precise additional question with meaningful negative answers.

## Concrete evidence that motivated the choice

The [executed CPU probes](evidence/PROTOCOL_AUDIT.md) establish several boundaries:

1. Two legal 32-record prefix worlds can give a downstream peer the **same complete scripted B history, current private evidence, old correct answer and after-only correction**, while requiring different updated outputs. Swapping two earlier values preserves their sum but changes the delta for the edited record. An authenticated before-value distinguishes those worlds.
2. Sorting can erase the correspondence between a source ID and its former value. A before-value restores that correspondence, but **does not necessarily supply the remote rank-boundary value** a peer now needs.
3. A correct full difference vector plus an unchanged current raw anchor reconstructs the old array. Before-values are not universally missing.
4. Maximum, top-K and BFS can need alternatives absent from the old output even with a complete transition. A small changed-output footprint does not imply a small missing-information problem.

These are constructed, checked observation-model results, not natural LLM failure rates. In particular, the ambiguous view concerns a peer **before new recovery communication**, not a team that can never recover. The scripted transcripts are evidence of possibility under the interface; they are not sampled model behavior.

## The addition to run

Keep all original six-task B/C/L/F branches, sham controls, answer-preserving diagnostics and the primary change-by-reset AUC interaction. On **every existing Prefix Sum and Distributed Sort world**, add two siblings:

- **BΔ:** retain history, with the historical before-value explicitly included in the authoritative correction receipt.
- **CΔ:** clear history exactly as C, with the same receipt.

Current source tables remain identical to their original B/C counterparts. Old values stay out of the active source table. The receipt provides raw versions and values only: no computed delta, output coordinates, gold answer, semantic dependencies or stronger repair instruction. Controls use the same format with the before-value marked “not included in this receipt.” Length accounting and, where needed, a frozen neutral-padding convention constrain simple token-count explanations; they cannot establish equal salience.

The focused secondary question concerns the first corrected response, before newly generated peer messages arrive:

`eta1 = mean[(a[CΔ,1] - a[BΔ,1]) - (a[C,1] - a[B,1])]`,

with means balanced over the two focal families and inference clustered by world. Negative eta1 means the receipt favors retaining history relative to clearing it. Both direct receipt effects must be shown: an interaction could otherwise hide harm to one arm. The corresponding four-round AUC interaction `eta_A`, full trajectories, stable/final correctness, and collateral damage are mandatory descriptive companions. No early advantage is automatically sustained recovery, and the fixed schedule demonstrates no actual reduction in allocated model calls.

This first-round target was chosen prospectively because it matches the mathematical information boundary. It does not promise higher power. With only 16/12 focal worlds, this is an explanatory, large-effect diagnostic, not a guaranteed detection of small improvements.

## What the completed research could teach

| Outcome | Defensible additional lesson |
|---|---|
| Receipt helps B more, with sustained acceptable outcomes | Preserved collaborative work becomes more useful under an explicit transition interface in the tested regime |
| Receipt improves only the first round | Earlier correct responses before new messages; attributing this to avoided communication/recomputation needs additional trace evidence, and presentation remains an explanation |
| Receipt helps both equally | Correction presentation/information matters, while the retention comparison is stable |
| Receipt harms or causes old-value copying | Historical/current role separation is unreliable enough to oppose default disclosure for this model/protocol |
| Interaction is precisely small | Stability of that retention contrast only; a small eta1 does not establish a small eta_A or small direct receipt benefits |
| Direct receipt benefits, harms and interactions are all bounded small | The simpler correction interface may be adequate within those tested quality/cost bounds |
| Wide intervals, capability floors, or uniformly complete evidence | The live addition is inconclusive or unnecessary; do not turn the algebra into a claimed empirical law |

The result should be presented with a **six-task recovery-information atlas** distinguishing current evidence, historical operands, retained summaries, lost alternatives and distributed ownership. A zero-extra-call exposure analysis may show whether a more elaborate selective policy would have any distinct state to preserve. Neither supporting analysis should be marketed as a newly invented theorem or taint algorithm.

## Why this wins over the main alternatives

The [candidate comparison](CANDIDATE_ADDITIONS.md) and [hostile review](NOVELTY_ADVERSARY.md) considered algorithms, representations, measurements, adaptive policies, partial-reset effects, cyclic updates, validation and completion reopening.

Candidate-only retention is simple, but answer-only/full-reasoning comparisons now have a direct [ICR predecessor](https://arxiv.org/html/2610.01042v1). Exposure filtering reduces to known conservative invalidation; its most defensible role is measuring applicability. Adaptive routing has a very close [CIR predecessor](https://arxiv.org/html/2610.00372v1) and needs more calibration data. Exact artifact checking can solve these small tasks and produce a misleading advantage.

Completion reopening retains a valuable distinction between valid artifacts and adequate search. However, it needs new query/acquisition semantics, more admissibility assumptions and a different main estimand. New obligation/commitment/versioned-work papers weaken its novelty advantage further. Its prior CPU examples remain useful evidence, but do not justify sacrificing the original six-task study. The [competitor review](reviews/COMPLETION_COMPETITOR.md) explains the comparison in detail.

The receipt addition is smaller, uses actual runtime observations, admits clear impossibility and redundancy counterexamples, and can produce a useful boundary result without a new model, learned classifier, semantic graph or external checker.

## Novelty claim and limits

**Do not claim:** invention of before-images, historical evidence, incremental repair, transition-aware agents, matched-prefix evaluation, or information-loss impossibility. Databases already have the first principles; [StateAuditor](https://arxiv.org/html/2608.01619v1) already uses old/current transitions in repair; correction-wording studies already show presentation matters.

**Potential contribution:** a carefully identified empirical relationship between the historical information supplied by a correction interface and the utility of retaining actual multi-round collaborative work, explained by exact local/collective information boundaries. The inspected literature does not establish that particular result. Its originality remains conditional on execution and future literature checks. This research phase supports a defensible question and design; it has not established a breakthrough method or empirical law.

## Feasibility and prioritization

The extension adds **512 calls** to the 48-world schedule or **384** to the 36-world fallback: total main schedules **6,368 / 4,872**, versus original **5,856 / 4,488**. Two existing focal development worlds add 64 calls: 652 pilot calls, or at most 676 including the smoke allowance for one passing configuration. All attempts remain within the original three-hour development cap and 30 aggregate GPU-hour ceiling.

With 24 hours provisionally available for main work, the extended schedules require averages below **13.57 / 17.73 allocated seconds per call**, before further overhead. These are break-even limits, not speed predictions. Preserve the Qwen/T4 capability, memory and timing gates.

**If 48 core worlds fit but the extension does not, keep the 48-world core and the CPU/trace analyses. Do not reduce the primary sample just to buy this exploratory addition.** If the original core already requires 36 worlds, append the focused extension only if that full schedule fits. Full details and alternative costs are in [FEASIBILITY_AND_VALUE.md](FEASIBILITY_AND_VALUE.md).

## Final recommendation

Keep the existing central question and experimental structure. Add a narrow study of **historical transition information as a condition for useful reasoning reuse**, using the receipt × retention factorial when the measured budget permits and the exact recovery-information atlas regardless. This is the simplest addition found that exposes a concrete runtime decision, preserves the PS's strengths, survives reduction to prior work with an honest empirical claim, and has interpretable failure outcomes.

The research-phase novelty, falsification, feasibility and design reviews support this bounded recommendation. They do not replace the capability pilot or empirical falsification. The next scientific revision is specified in [SPECIFICATION_CHANGE_PLAN.md](SPECIFICATION_CHANGE_PLAN.md); implementation code and specification edits are outside this completed research phase.
