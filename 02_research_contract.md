# Research contract

Status: implementation specification v1.0, 20 September 2026. The experiments below are planned, not completed. The novelty claim is deliberately narrower than the earlier direction-selection report.

## Recommended title

**What remains valid after a correction? Evidential support and action repair in stateful LLM teams.**

## Final research question

**When an upstream correction leaves a team's intermediate conclusion true, under what conditions do estimated support records let the team preserve useful state while correctly revising actions that were bound to the superseded evidence?**

The primary structural interaction is **alternative evidential support × whether execution is bound to a particular witness**. Provenance quality and replacement of downstream state explain the interaction. A witness is the particular resource, route, document, or other instance that satisfies a condition.

Example: “the order can be fulfilled” has support from either warehouse X or Y. Correcting X's stock can leave that statement true. An already prepared `ship_from(X)` instruction can nevertheless become invalid. Preserving the conclusion, replacing its justification, and changing the action are distinct operations. No new theorem is needed to show that distinction; the scientific question is whether realistic agent handoffs preserve enough of it for recovery, and which failure mechanism dominates.

## Scope and assumptions

- Three independently stateful decision-makers: source owner A, integrating planner B, executing agent C. Separate contexts and write ownership; the same model may implement all three.
- One diagnosed, reliable factual correction per main episode, delivered between planning and execution. The original fact was valid at the planning snapshot; the experiment studies updates, not an adversarially planted falsehood.
- Closed, finite task semantics and programmatic evaluation. Agent-produced claims and actions can be wrong. Their meanings are identified through explicit schema slots; unrestricted prose is not assigned fabricated ground truth.
- Reliable, ordered communication in the main experiment. Source capsules accompany handoffs, so failure to transmit the required raw evidence is controlled. This intentionally isolates integration, representation, and state repair after evidence delivery.
- No learning, fine-tuning, online retrieval, external side effects, human participants, security attack success claim, or theorem about opaque model-internal reasoning.
- Corrections concern current facts. Authority, privacy deletion, and permission revocation are separate problems. A surviving factual proof never restores revoked authorization.

The tested team dependency is inherited claims and pending decisions under separate write ownership. The underlying goal-versus-action distinction also exists in single-agent systems. This design identifies policy effects within teams; it does not identify the causal effect of decentralization versus a centralized controller with exactly matched history, compute and state. The fresh single-agent control diagnoses local task difficulty, not that stronger comparison. Do not claim the phenomenon is unique to multi-agent systems.

## Hypotheses and discriminating observations

| Hypothesis | Plausible mechanism | Observation that favors it | Observation that weakens it |
|---|---|---|---|
| H1: adequate support representation | Agents and extractor retain action-specific dependencies; selective recovery preserves benign work without retaining invalid actions. | Estimated-support policy approaches exact-support scope and maintains completion in both action regimes. | Accurate claim support coexists with incorrect action preservation. |
| H2: abstraction loses binding information | Handoffs describe a still-true goal but omit the evidence behind concrete action arguments. | Errors concentrate in alternative-support, witness-bound worlds; action-support extraction is worse than claim-support extraction; a deliberately coarse oracle reproduces this failure while a full oracle reduces it. | Failure rate does not depend on action binding; exact and coarse scope behave alike with tight intervals. |
| H3: correct scope is insufficient | The team knows what became invalid but retains or regenerates an obsolete decision in recipient state. | Full exact scope still fails; rebuilding the executing agent's working state improves recovery from the same prefix and information. | Exact scope succeeds and rebuilding does not help. |
| H4: over-repair creates new error | Conservative invalidation discards correct summaries and incidental work; reconstruction creates avoidable errors. | Conservative policy loses valid control-job state or makes more new errors than selective policy under equal call caps. | Conservative regeneration is cheap and reliable; preservation has no meaningful benefit. |

H1–H4 can coexist. The study estimates their practical importance; it does not force a single winner.

## Exact contribution, if supported

1. A paired causal experiment showing whether the effect of a recovery policy changes when alternative support preserves a conclusion but does not preserve a concrete action.
2. A decomposition of failures into support-set estimation, action-specific support loss, and downstream state replacement, using interventions on the same frozen prefix.
3. An open, deterministic recovery extension with independently checked support labels, observable-state contracts, and reproducible trajectories. The extension is an experimental instrument, not the central scientific claim.
4. Evidence for limits as well as benefits: a well-powered negative result showing conservative restart is preferable, or a bounded result showing natural estimated support is sufficient in this regime, is valuable.

Do not claim a universal provenance-quality threshold. A finite study can estimate an operating region in its task/model population, not a general necessary bound.

## Primary estimand

Let `E` be estimated-support repair, `R` conservative exposure-based repair, `a` alternative support (0/1), and `b` witness-bound execution (0/1). Let Y be protocol-valid correct completion of both jobs with no semantically invalid attempt or applied effect, within the fixed recovery allowance.

The single primary contrast is

\[
\theta=\mathbb E_w[(Y_{E, 1,1}-Y_{R, 1,1})-(Y_{E, 1,0}-Y_{R, 1,0})].
\]

Thus the central question is whether the relative value of selective recovery changes when an otherwise equivalent conclusion is used to authorize a specific action. The unique-support conditions are essential negative controls and support a secondary three-way interaction. Alternative variants and bound variants have separate prefixes; policy branches within one variant share an identical realized prefix.

The population is the predeclared generator distribution. Include every generated world, including bad prefixes. Report a secondary analysis restricted to prefixes that were correct before correction; prefix validity is measured before treatment. Never regenerate worlds until agents happen to succeed.

The executable task contract makes a deterministic specification-aware solution possible. The experiment does not claim that LLM support extraction is necessary or superior in such domains. Exact support supplies the measurement reference; the object of study is whether natural handoffs satisfy that reference and how stateful decisions respond to correction.

## Novelty boundary

The current literature already covers dependency-based rollback, preserving independently supported material, withdrawal barriers, selective replay, provenance-based governance, and transaction-style memory discipline. See the evidence audit in [03_related_work.md](03_related_work.md). A current anonymous submission also explicitly addresses incomplete provenance. Therefore **“recovery with incomplete provenance” alone is not an adequate novelty claim**.

The defensible claim is narrower: a causal study of **semantic granularity at inter-agent handoffs**, where a surviving existential conclusion and an invalid witness-bound action must be treated differently, with natural support extraction and a separate recipient-state intervention. No searched paper was verified to contain this exact factorial experiment. That is an evidence-limited assessment, not proof of global absence. The latest incomplete-provenance submission remains a required full-text check before preregistration.

Prior work establishes useful recovery under explicit support/validity contracts. It does not, in the material inspected, establish whether naturally produced multi-agent support records preserve the action bindings those contracts need, or whether correct invalidation scope is enough for downstream behavioral repair. This study distinguishes representation failure from recipient-state persistence.

## What would change our belief?

- An E advantage only for unbound conclusions would show that aggregate task accuracy overstates selective recovery reliability.
- An E≈full-oracle result with narrow uncertainty would support the adequacy of explicit compact handoffs for this class of teams.
- A full-oracle versus state-rebuild difference would locate a behavioral bottleneck after fault localization.
- No substantial effect after capability and power gates would bound the phenomenon in short, well-instrumented teams. It would not justify adding complexity until a positive result appears.

## Success criteria for the thesis

The thesis succeeds if it produces an interpretable estimate and a validated diagnostic separation, even if E loses. It fails scientifically if all effects are consequences of an oracle enforcing its own answer, invalid local reasoning dominates, the ground-truth semantics do not match the claimed construct, or close prior work already establishes the same empirical distinction without a credible extension.
