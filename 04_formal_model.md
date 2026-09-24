# Formal model and evaluator semantics

This document is normative. `reference/support.py` is a small executable reference for the finite support algebra, not a complete agent runtime.

## 1. Four different objects

1. **Exposure lineage** `G_read`: an item was rendered in a call that produced an artifact. This is a sound record of exposure, not proof of use. Add an edge from every rendered evidence/claim/action record to every record emitted by that call. Exclude public instructions and clock-order edges from correction propagation.
2. **Declared references** `G_decl`: IDs the producing agent explicitly cited. Validate visibility and ID existence, but do not assume completeness, entailment, or faithfulness.
3. **Estimated support** `J_hat`: sufficient sets predicted from the frozen observable prefix by a separate extraction call. It can miss required premises, omit alternatives, or invent sufficiency.
4. **Evaluator support** `J_star`: all inclusion-minimal evidential justifications of a typed assertion under the public task semantics and a specified evidence view. It is not a claim about the model's actual internal reasoning.

All four are stored separately. A plain directed graph cannot distinguish `a AND b` from `a OR b`; support must be represented as a hypergraph or equivalent DNF.

## 2. Evidence and snapshots

An evidence version is immutable: `(evidence_id, key, version, root_id, owner, value, atom, observed_epoch, supersedes)`. Example: `x_capacity@1`, key `capacity:X`, value 9, atom `cap_ok_X=true`; a correction appends `x_capacity@2`, value 2, atom false. `root_id=capacity:X` remains unchanged across versions. Copies of a version keep its ID/root; a report does not create an independent root.

The task supplies a deterministic, public conversion from raw value to a Boolean atom, such as `capacity >= required_units` or case-sensitive substring containment. The evaluator recomputes the atom from the raw value; it never trusts an agent-provided atom.

At epoch t, the current evidence map selects exactly one version per key. A superseded version remains in the audit log but cannot justify a current assertion. Main experiments contain no simultaneous contradictions at a source. All owners receive the same committed correction epoch before recovery.

`WorldSnapshot` stores evidence versions, current-version pointers, public task rules, pending sandbox actions, and logical time. `AgentSnapshot` stores that agent's active claim IDs, pending action IDs, last received epoch, and bounded working-state records. It contains no hidden state of another agent. The event log is immutable; materialized active views are projections of it.

## 3. Claims, formulas, and labels

Each claim uses a typed, finite slot, for example `(eligible, X, true)` or `(feasible, target_job, false)`. A catalog maps a slot to a Boolean formula. This restricts semantic evaluation, not the agent's choice of answer.

Grammar:

```text
Expr := atom(name) | and(Expr, ...) | or(Expr, ...) | not(Expr)
```

For a formula f and desired Boolean value v, a subset S of currently available evidence versions is a sufficient justification iff **every completion of unobserved atom values consistent with S makes f equal v**. Define:

\[
\mathcal J^*(f=v, V)=\min_{\subseteq}\{S\subseteq V: S\models(f=v)\}.
\]

Unknown is not false. A false claim has no supporting set unless the available evidence actually entails its negation. A claim may be globally true but unsupported in an actor's evidence view.

The primary generator emits monotone formulas. The reference recursive evaluator also permits unate formulas (each atom has only one polarity); mixed-polarity formulas such as `x OR NOT x` are rejected on this path. This restriction matters: naïve recursive proof combination is not complete for unrestricted Boolean logic. The independent completion-enumeration oracle handles general bounded formulas.

For these bounded unate formulas, compute labels recursively:

| Expression / required value | Support operation |
|---|---|
| known atom equals requested value | singleton family containing that evidence ID |
| unknown atom or opposite observed value | empty family |
| AND is true | Cartesian product of children's support families, union each combination |
| AND is false | union children's false-support families |
| OR is true | union children's true-support families |
| OR is false | Cartesian product of children's false-support families |
| NOT is v | child's support for not-v |

After every operation: deduplicate sets and remove strict supersets. The result is an antichain. Empty family `[]` means no justification. Family `[[]]` means a tautological empty justification and is allowed only for an explicit public constant in the evaluator; the extractor may not emit it. Main generated claims have no empty proofs. Caps: at most 10 atomic variables, 32 minimal justifications, and 10 roots per justification. Exceeding a cap rejects the generated world before inference, with a recorded reason.

## 4. Unique, alternative, AND/OR, independence

```json
{"node_id":"q","minimal_sets":[["x_capacity@1","x_online@1","permit@1"]]}
```

This is one unique AND support set. In contrast:

```json
{"node_id":"q","minimal_sets":[
  ["x_capacity@1","x_online@1","permit@1"],
  ["y_capacity@1","y_online@1","permit@1"]
]}
```

These are alternative supports joined by OR. They share a background permit. They are **independent of the corrected X root**, not probabilistically independent and not fully root-disjoint. Store `root_overlap` and `correction_independent` separately. Two agents repeating X's report do not create an alternative proof. Unique support means exactly one minimal justification for the focal pre-correction positive conclusion; it does not mean “only one incoming edge.”

Let F be the set of superseded versions. A *pre-correction* justification survives by identity iff `S ∩ F = ∅`. A claim can also become justified by newly introduced versions; that is a new certificate and is not reuse of an obsolete certificate. Main positive-alternative cases have a surviving pre-existing proof, making preservation distinguishable from regeneration.

## 5. Action validity is separate

An action record contains exact `(verb, job_id, resource_id, value)` arguments plus its own declared support. The evaluator obtains a formula from the **actual submitted arguments**, never from what the planner intended.

- `publish(job, value)` is valid iff `feasible(job) == value`.
- `dispatch(job, resource)` is valid iff `permit AND eligible(resource)` for that job.
- `wait(job)` is the correct completion iff `feasible(job) == false`.

For a bound action, the set of proofs of `feasible(job)` is not the action's support set. A proof through Y can preserve feasibility but cannot justify `dispatch(X)`.

Four independent evaluator columns are required: `truth_valid`, `has_available_support`, `authorized`, and `runtime_status`. The main task fixes authorization to C and the permitted sandbox verbs. The evaluator may find a true action blocked by a conservative policy or a false action active under an estimated policy. Never overwrite these columns with a single “valid” flag.

Also store `task_correct` and action-only `priority_adherent`. Feasibility support does not encode the public X-before-Y tie-break: a feasible Y choice before correction can violate task priority without being an infeasible action. Correct-prefix analyses require priority adherence. Public action-mode restrictions (publish versus dispatch/reserve/wait) are protocol constraints, specified in 09.

Action arguments are immutable. A changed resource creates a new action record that supersedes the pending one. “Rebind” means replace arguments and support together; it never edits history. An executed action cannot be undone by deleting its record. The primary experiment corrects before execution. Transfer executes in a resettable sandbox and reports both attempted and applied effects.

## 6. Available versus global support

Compute `J_global` over all current world evidence and `J_available(agent)` over evidence delivered to that agent. The full-support diagnostic uses only `J_available` for the artifact owner. It never tells an agent about a hidden witness.

In the main protocol all task-relevant source capsules reach B and C with the handoffs, so their global and available factual support coincide after delivery. A's private view remains local. Delivery is tested explicitly; a parser failure in a message must not remove its separately transported source capsule. This control removes missing raw evidence as an explanation of the core effect.

## 7. Exact unsupported set

At the correction cut, let L be all active typed claims and pending actions. For each record x, bind its actual assertion/action formula and compute its current available support. Then:

\[
U^*=\{x\in L:\mathcal J^*(x, V_{owner(x),t+1})=\varnothing\}.
\]

The full-support diagnostic masks U*. It is an oracle for *repair scope*, not for the new answer: it supplies IDs to reconsider, not a correct replacement action. It can include pre-existing unsupported claims; report `preexisting_invalid` separately from `became_invalid` to avoid attributing every failure to the correction.

For intervention evaluation, use both `U_event = U_after \ U_before` and `U_after`. Invalidation precision/recall uses U_event for the correction-specific mechanism; final active-state consistency uses U_after.

## 8. Estimated support and evaluation

The extractor reads the frozen prefix, public rules, source capsules already delivered, actual action arguments, and valid IDs. It sees neither the future correction nor evaluator labels. It emits root-version DNF for each active typed claim and pending action. Syntactic validation permits wrong semantics: a false sufficient set remains an observable extraction error rather than being silently replaced with an oracle answer.

Resolve declared claim references recursively to leaf versions only in the declared-support ablation. A cycle without an independently grounded proof yields no known support. The natural extractor outputs leaf-version IDs directly, so its support object is acyclic by construction.

Main support-estimation scores compare the pre-correction estimate to `J_star` on the same view and typed node. Evaluate set-level sufficiency, minimality, missing alternatives, and whether the post-correction unsupported verdict is correct. Edge F1 alone is insufficient because the same edge set can encode different AND/OR semantics.

## 9. Worked four-way world

`permit=true`, X has capacity 9 and is online. Required units=5. Correction changes X capacity to 2. The control job has an independent eligible resource Z.

| Variant | Y before/after | Focal conclusion after correction | Old unbound action | Old bound action |
|---|---|---|---|---|
| unique, unbound | capacity 2, online | false | `publish(true)` invalid; publish(false) required | not part of this variant |
| alternative, unbound | capacity 8, online | true | `publish(true)` remains semantically valid, with Y support | not part of this variant |
| unique, bound | capacity 2, online | false | not part of this variant | `dispatch(X)` invalid; wait required |
| alternative, bound | capacity 8, online | true | not part of this variant | `dispatch(X)` invalid; dispatch(Y) required |

Initial tie preference is X, so all correct bound prefixes choose X. If an agent chooses Y before correction, retain the episode in the primary intention-to-treat analysis and mark the deviation; do not selectively regenerate it. The control job tests unnecessary destruction of unrelated state.

## 10. Invariants

Only current evidence supports current certificates; proof alternatives are OR and premises within one proof are AND; supersets do not count as additional alternatives; corrected versions never mutate in place; actions are graded against their own arguments; historical correctness is retained at its original epoch; artifact ownership restricts agent writes; no evaluator-only field enters a feasible policy prompt; all repair branches begin at the same immutable checkpoint; semantic failure never triggers a hidden retry.

## 11. Numeric transfer support

Do not treat the comparison `quote <= budget` as an atomic observation with a fabricated single source ID. Its truth can depend on two independently owned numeric sources. The CapEx transfer uses a second, exhaustive finite-domain support evaluator.

Public numeric domain: amounts are integer multiples of 10,000 dollars from 0 through 400,000 dollars, represented in cents. Completeness is Boolean. For each typed assertion or actual action, use a registered pure predicate over quoteX, quoteY, budget and completeness. Bind the action's submitted vendor/amount/route before evaluating. Enumerate subsets of delivered current evidence; a subset is sufficient iff every domain completion consistent with it satisfies the predicate. Remove nonminimal subsets. Evaluate only the source fields read by that predicate; the control job is separate. Short-circuit on a falsifying completion and cache truth tables by canonical predicate/argument/domain hash.

This is exact relative to the explicitly public finite domain. It is not an approximation that assumes every comparison always needs both operands. For example, a known extreme bound may make one operand sufficient. No native SILO score or free-form financial reasoning claim follows from this constructed transfer. The CPU reference currently tests the primary Boolean evaluator; numeric-transfer evaluator conformance is a mandatory implementation/pilot gate.
