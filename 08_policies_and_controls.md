# Recovery policies, controls, and ablations

All policies share the same source update, correction text, source availability, agent prompts, output schema, three recovery slots, and sandbox. Policy-specific material is rendered in a fixed `repair_notice` field. Policy names are not shown to agents. Invalidation is an instruction/state operation, not an oracle answer.

## Main policies

### N — source notification and ordinary continuation

Supersede the source version globally and deliver the correction. Preserve all derived claims and pending actions in their previous runtime states. Add a generic notice to review consequences. Agents may revise anything they own during their three slots. Old source content is not a current evidence capsule, but active claims/actions may still cite its ID. N is not “no correction.”

### R — conservative exposure closure

Compute descendants of the superseded evidence version in `G_read`, including indirect paths through delivered claims/actions. Withdraw all reached active claims and suspend all reached pending actions. Remove withdrawn claims from active prompt sections; retain only their IDs in the notice. Retain unaffected records. Incomplete/malformed model output does not erase read receipts. No chronological-chain edges are used.

R can over-invalidate an unrelated control-job artifact because a call read X while producing it. That is the scientifically relevant cost of using exposure as a dependency approximation. Do not describe R as exact causal rollback.

### E — estimated support repair

For every active record whose exposure ancestry intersects the changed source, inspect its pre-correction estimated minimal support family. Preserve the record if at least one nonempty estimated support set contains only still-current versions. Otherwise withdraw/suspend it. For an absent or syntactically invalid estimate, use R for that record. Do not use the evaluator to verify sufficiency at runtime.

For records outside the read-closure, preserve them. If extractor IDs contradict visibility or are nonexistent, treat that record's estimate as invalid and fall back. A syntactically valid but semantically wrong set is used as predicted: it is an estimation error to measure, not silently repaired by an oracle.

Main corrections change a factual predicate, so stale proof leaves cannot be blindly renamed to the new version. On no-event controls F is empty and every policy plan is empty. Rebinding a support certificate after a changed value requires an agent-produced successor or surviving old proof.

## Diagnostic policies

| ID | Exact behavior | Interpretation / limitation |
|---|---|---|
| O | Compute U_after from the evaluator using each record owner's delivered evidence and actual typed assertion/action arguments. Apply the same withdraw/suspend operation as E. Give only record IDs/status, not gold replacement values. | Exact scope with the same behavioral executor. Can repair pre-existing errors; distinguish them and analyze correct prefixes separately. No guarantee of correct new output. |
| OC | Same as O for factual claims, but determine each action's keep/withdraw verdict from its associated `feasible(job)` Boolean instead of its actual witness-bound arguments. | Deliberate action-granularity ablation. Not a sensible proposed method. It tests whether losing the binding distinction reproduces natural failures. All current evidence remains available, so failure is not imposed by hiding the answer. |
| ON | Supply the same unsupported-record IDs as O in an explicit correction notice, but leave derived state active and pending actions unsuspended, as in N. | O versus ON tests whether correct localization needs mechanical withdrawal. Both receive identical localization information. |
| OR | Start with O. Immediately before C's recovery call, withdraw C's remaining prior typed claims and cancel every prior pending C action with reason `recipient_reset`; clear C's working view. Supply current source capsules, updated A/B reports, both job obligations, and the same notice. C must create fresh actions. Historical logs remain intact. | O versus OR tests rebuilding recipient state beyond exact withdrawal. This is a combined state-removal/context intervention, not a pure measure of psychological anchoring. |

O/OC/ON/OR are run on the same predeclared 16 base worlds × 4 variants. They receive a specification-aware semantic service that N/R/E do not receive. In this fully formalized environment, an engineer could implement that service from the public task rules: it is not intrinsically unknowable information. Treat O as a **specification-aware comparator and diagnostic**, not an unattainable intelligence upper bound. It becomes an oracle assumption only when extrapolating to workflows whose natural-language semantics are not available as an exact program. OC deliberately removes part of that contract.

## Additional baselines

**Restart (F):** discard all derived agent state, keep the corrected current source ownership, and execute a fresh A→B→C sequence ending in final actions. There is no new correction during it. It gets the same three agent-call and output caps as ordinary repair. Count its new three calls plus the original failed prefix in end-to-end cost. This is a clean-state competitor, not a zero-cost oracle. The diagnostic subset has 16 base worlds × 4 variants.

**Extra inference (B):** run N with one additional pre-recovery reviewer call. Reviewer sees the common corrected public projection and produces a short generic review, without support masks. Then run the normal A→B→C slots. Its extra call receives the extractor's 512-token cap and is counted as a long call. It asks whether E's advantage is attributable merely to an additional inference stage. The reviewer cannot edit ledger state or call the evaluator. Same diagnostic subset. Cost matching is by reserved input/output allowance; report realized cost, since identical call counts alone do not match tokens.

**Information-complete single agent (S):** one fresh C-like call receives the corrected full source set, public rules and both jobs, with no team history. It has the same 256-output cap. It diagnoses local task difficulty and centralized access; it is not a resource-matched team competitor. Same 64 diagnostic worlds.

**No-event controls:** branch from the same prefix, do not change an evidence version or epoch, and give a neutral “review current decisions; no facts changed” notice. Run N and E with three slots each on 8 base worlds × 4 variants. E must emit an empty plan. This measures damage or gains from mere re-execution.

**Deterministic solver:** exact current-world decisions and proof sets, CPU only, every world. No LLM performance comparison is claimed.

If a deployment has the same complete executable task contracts, use a deterministic solver or exact truth-maintenance service instead of inferring those dependencies with an LLM. E is being studied as an imperfect operational representation, not advocated over an available exact compiler. This prevents a synthetic benchmark from creating artificial demand for a learned support extractor.

## Unfunded algorithms that MUST NOT quietly enter the matrix

Full reproduction of MemoRepair's min-cut selector, a new learned extractor, a topology sweep, random-edge noise grids with LLM replay, repeated multi-correction horizons, adversarial agents, and broad model-family comparisons are outside v1.0. They require a revised budget and preregistration. A second model diagnostic is narrowly funded in 10; it is not a broad replication.

## CPU-only representation ablations

Apply to saved natural prefixes, without reusing altered continuations:

- Compare extracted DNF with declared citations treated as one conjunction. Missing declarations yield unknown, not a free true proof.
- Collapse DNF into an ordinary incoming-edge set and compare the resulting all-AND and all-OR verdicts to exact unsupported sets. This measures representational information loss.
- Drop exactly one necessary leaf from each exact AND set, or drop one alternative set, or duplicate a report sharing the same root. Enumerate each legal edit separately. These are evaluator sensitivity experiments, not natural-error prevalence estimates.
- Compute policy masks and precision/recall for these altered graphs. Do **not** attach the original LLM outcome to an altered mask and call it a counterfactual recovery outcome. Any changed continuation requires fresh inference.

## Reference algorithm

```python
def plan_estimated(view, correction, estimates):
    candidates = read_descendants(view, correction.old_version_ids)
    withdrawn, suspended, fallback = set(), set(), set()
    for node in sorted(candidates & view.active_record_ids):
        label = estimates.get(node)
        if label is None or not label.syntax_valid:
            fallback.add(node)
        keep = (
            label is not None and label.syntax_valid
            and any(proof and proof <= view.current_evidence_ids
                    for proof in label.minimal_sets)
        )
        if not keep:
            (suspended if view.is_action(node) else withdrawn).add(node)
    return RepairPlan(
        policy="E", correction_id=correction.correction_id,
        withdraw_claims=tuple(sorted(withdrawn)),
        suspend_actions=tuple(sorted(suspended)),
        notices=tuple(sorted(withdrawn | suspended)),
        mask_source="estimated", fallback_nodes=tuple(sorted(fallback)))
```

Here `active_record_ids`, `current_evidence_ids` and `is_action` are pure indexed projections of the RuntimeView's records and dispositions; they are not additional persisted fields. The current-evidence set is resolved for each record owner in the same evidence namespace used by the extractor. This algorithm estimates certificate survival; it does not infer a hidden model computation, generate a new proof, or grant execution permission.

## Fairness and estimand limits

Fixed recovery slots isolate the effects of preserved state and repair information. They do not demonstrate lower inference cost from selective scheduling because every ordinary branch runs three calls. Report regenerated-record count and actual token differences, but do not advertise an unmeasured reduction in call count. End-to-end E includes extractor cost; N/R do not. Diagnostic extraction already computed for analysis must not be falsely charged as a deployment cost to N/R.

The extractor sees the complete observable prefix before correction; the extra reviewer sees the correction but has no support mask. This is a deliberately strong extra-inference control, not an exact architectural decomposition. O supplies privileged semantic information. These information differences are part of each labeled comparison, not hidden controls.
