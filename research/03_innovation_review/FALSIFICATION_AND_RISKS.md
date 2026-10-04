# Falsification and risks

The recommended completion interface is a hypothesis about useful state management. It is not a proof that agent recovery becomes correct.

## Strongest objections

| Objection | Discriminating evidence | Outcome that weakens or kills the contribution |
|---|---|---|
| It is ordinary control-dependent invalidation | Implement objective, membership and closure reads in a provenance baseline | Equivalent behavior means the algorithmic claim disappears; retain only interface/empirical contribution. |
| A prompt saying “reconsider all options” is enough | Same evidence, previous work, call allowance, output length and revision wording; replace enforced reopening with the reminder | Similar quality and cost means no demonstrated benefit from runtime enforcement. |
| Source-only reset is sufficient | Clean planner given identical current acquired sources | No useful reuse/coordination gain means the extra lifecycle is unnecessary. |
| It only forces additional tool calls | Give the control the same current observations or identical mandatory refreshes | If the remaining difference vanishes, attribute the benefit to acquisition, not richer reasoning or completion semantics. Acquisition may still be useful, but say so. |
| A checker secretly supplies the answer | Inspect every runtime-visible field and validator operation; provide checks equally; run deterministic solver baseline | Gold footprint, affected-option labels or exact optimality feedback entering recovery invalidates the intended test. |
| Scope extraction invents completeness | Omit or corrupt scope/exclusion hints; insert a never-listed option | Failure must trigger broader reconsideration or appear as an error; silently accepting completion contradicts the design. |
| Broad reopening dominates | Compare selective scope with reopening every completion claim | Retire selective scope. Do not keep it because it looks more sophisticated. |
| Artifacts look current but remain semantically stale | Test valid metadata with wrong content, stale prose summaries, changed objective and unchanged query results | Version receipts alone cannot support a semantic reliability claim. |
| Only authored failures show an effect | Include unfiltered natural prefixes; classify failures offline | Scripted fixtures alone establish possibility, not practical importance. |
| Long-horizon savings are invented | Charge all real calls/checks/acquisition and report artificial costs separately | A token-only improvement cannot establish saved days or production economics. |

## Concrete adversarial cases

1. **New option with no old edge.** A new provider/edge/record appears outside every recorded exclusion. Runtime-owned domain membership changes, or the domain is explicitly unknown. The mechanism must reopen the root; an empty known-descendant set is insufficient.
2. **Objective changed, old query still true.** “No qualifying item under budget 50” remains a correct answer to that historical query after the budget becomes 80. It no longer closes the current question.
3. **Valid witness, invalid optimum.** An old path remains traversable after a shortcut is added. A path-validity check must not certify shortest-path completion. Executed CPU examples are in `evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md`.
4. **Improvement in an unvisited region.** The old incumbent and all its evidence remain valid. Rechecking only the incumbent cannot reveal the new optimum.
5. **False or omitted stopping note.** The agent says a region was exhausted, or records nothing. Absence of a note must not remove the automatic root obligation.
6. **Freshly stamped old reasoning.** An agent copies an old conclusion into a new epoch without new relevant work. Fresh receipt metadata alone must not count as semantic repair.
7. **Recontamination through prose.** A retained summary says “B is irrelevant”; reopened task status says inspect B. Measure whether the former suppresses the latter.
8. **Second update during recovery.** A v2 completion arrives after v3 is authoritative. Reject v2 closure even if it was correct at generation time.
9. **No relevant change.** Frequent reopening can waste work and damage previously correct decisions. Sham and answer-preserving changes quantify this tax.
10. **Cheap complete recomputation.** If enumerating and solving the finite task is cheaper than maintaining scopes, the method should lose. That is a valid boundary.

## Identification hazards

Treatments must share a pre-event checkpoint. A protocol that changes prefix behavior has a different preventive cost and requires a separate comparison. Do not produce a better prefix for the proposed method and attribute its final advantage entirely to recovery.

Measure artifact retention, active context content, source availability, required inspections and stopping rules explicitly. A result combining all five interventions cannot establish which one caused the benefit. Do not describe attention, anchoring or an internal causal reasoning process based only on changed outputs.

A changed task family, output shape, information budget or external tool can be harder independently of recovery. Calibrate fresh corrected solving and analyze failures from unsuccessful prefixes separately without dropping them from the primary population.

## Novelty threats that remain

- [REVISE](https://arxiv.org/html/2609.00643v1) can encode the proposed state as explicit control/membership nodes.
- [MemoRepair](https://arxiv.org/html/2605.07242v1) can treat a closure decision as a repairable artifact.
- Dynamic CSP and incremental search already repair exclusions and search state.
- MemContinuum already stores rejected alternatives and revisit triggers.
- GA-Rollback already includes reconsideration of candidate-search sufficiency.
- The inaccessible OpenReview “Repair Sets” paper remains an unresolved check. No claim of absence is justified.

Before submission, obtain the latest accessible versions and inspect public implementations where available. A paper that covers the same interface and uncertain-scope experiment would change positioning to replication/generalization. Do not narrow wording cosmetically to preserve a firstness claim.

## Stop rules

Do not expand the mechanism if current-source reset is adequate, natural failures are absent, correct scopes require oracle labels, or inference capability is too weak. Do not run the full main matrix if the pilot cannot distinguish competent initial collaboration from general task failure. Report a feasibility or boundary result and retain the simpler study.

No positive effect is required to justify publishing the resulting artifacts, but a **new reusable mechanism claim requires evidence of a capability beyond the matched simpler alternatives**.
