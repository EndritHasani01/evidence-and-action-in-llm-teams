# Recommended direction: recovery of completion decisions

**Decision: option 3 — substantially reframe the recovery strategy while preserving correction after distributed collaboration.**

Study **when a change should reopen a team's completed questions, even though much of its existing work remains valid**. Implement a small revision-sensitive completion interface as the experimental mechanism. Start with conservative reopening; add selective scopes only if they justify their complexity.

This investigation did **not** establish a fundamentally new recovery algorithm. It established a sharper empirical question and a potentially reusable application/runtime interface. Its components have clear predecessors. The contribution should be presented as an explicit synthesis and a causal boundary study unless subsequent implementation and literature checks establish a narrower original result.

## Central insight

Recovery has at least two obligations:

1. Existing work must be acceptable under current facts and requirements.
2. The team must reconsider whether it has done enough of the right work.

An old supplier choice can remain feasible after a budget increases. Its supporting quotes remain true. Yet previously unaffordable suppliers may now be better. Revalidating the selected supplier does not inspect them. The obsolete state is the earlier decision to stop searching that region.

The mechanism separates **artifact retention** from **completion validity**. Reopen the question; preserve the useful evidence and work that can still be used legitimately. This targets stale omissions as well as stale assertions.

## Minimal mechanism

Use ordinary persisted records, not a new agent framework. A task or search question has an automatically created obligation:

```text
obligation_id, parent_task, objective_revision
source_domain_snapshot, membership_revision
scope: known provider/query/subtask IDs, or UNKNOWN
status: OPEN | CLOSED | NEEDS_RECONSIDERATION | RETIRED
completion_receipts: tool/query/child-task references
agent_notes: proposed stopping reason and excluded alternatives
```

The runtime creates a root obligation when the task begins and registers child obligations at actual tool/subtask boundaries. Agent notes may improve scheduling, but cannot establish that an unrecorded dependency is absent. The root obligation exists even when an agent emits no useful notes.

At a revision:

1. Apply the authoritative change and make superseded source versions unavailable as current facts.
2. Reopen the durable root completion claim and reassess which children are required by the current task. Retire children canceled by the revision; do not resurrect every historical task. The first implementation reopens all currently required completion claims. A later scoped variant retains closure only where trusted runtime information establishes that the objective and relevant domain are unchanged; otherwise it reopens the parent or root.
3. Keep current source evidence and independently admissible artifacts. Archive obsolete decisions and completion receipts. Raw prior prose is not automatically certified by retaining a file. The simplest safe context construction uses current evidence, retained typed artifacts and the open task list; unrestricted prose retention is a separate experimental arm.
4. Schedule current-world work for the open obligations. An agent chooses what to inspect and how to solve; the runtime does not supply the newly relevant option or the answer.
5. Accept a new completion receipt only for the current objective/source view and required operational checks. The host binds the receipt to the immutable view actually used by the invocation; the model cannot create freshness by supplying a new version label. A delayed old receipt cannot close a reopened task.

This requires a task-state table, a revision transition, a query/subtask receipt wrapper and a context renderer. The main method needs no inference-time dependency extractor, vector database, extra reviewer model, confidence score or cost optimizer.

## Exactly what may be reused

| Old state | Treatment |
|---|---|
| Unchanged authenticated source record | Retain. |
| Obsolete source version | Keep offline for audit; replace/tombstone in active evidence. |
| Expensive artifact with adequate current input/contract evidence | Reuse within that contract; checking cost counts. |
| Historical search result for a precise unchanged query | Retain as that query's result, not as coverage of a changed objective. |
| Choice, exclusion, “nothing else matters”, or “done” | Reconsider its applicability after revision. |
| Artifact with uncertain validity | Treat as a proposal or quarantine; do not promote it by relabeling its epoch. |
| Missing/unclear search scope | Reopen a broader obligation. |
| Old in-flight completion/message | Reject its authority; any payload reuse requires the normal current admission path. |

Retaining an artifact is distinct from placing all of its old rationale into active context. When free-text reasoning is retained, semantic contamination remains an empirical risk; the protocol does not promise hidden-state erasure.

## What a completion receipt means

A receipt can establish that a current query was issued, specified sources were visited, or a child task returned under the current revision. It cannot automatically establish that the query was adequate, all relevant options were considered, the reasoning was sound, or the global optimum was found.

For a finite structured adapter, a provider can expose a complete domain listing and current query coverage. This is useful operational information. The agent still chooses valid queries, combines results and makes the decision. The hidden evaluator computes the exact answer independently. For open-ended research, completion remains a bounded claim about inspected scope; no exhaustive-search guarantee is appropriate.

A receipt must distinguish **process completed** from **decision verified**. The runtime can reject an old completion with certainty; accepting a fresh completion is not proof of correctness.

### Concrete first discharge rule

In the finite-search adapter the task contract supplies a public list of required providers/partitions, not the relevant winner. To reclose a broad root obligation, each currently required provider must have a host-recorded post-revision query with agent-chosen parameters; the assigned peer must then consume its result in a scheduled recovery invocation. A new team answer must be assembled for the current objective. Queries may return an empty set, and may be badly chosen. This rule establishes **that reconsideration work occurred**, not adequate semantic coverage. Merely repeating an old restrictive query can satisfy the process check and still fail exact evaluation.

Known current query receipts may exempt scopes only in the optional scoped policy under a documented runtime contract. Hidden semantic omissions remain possible even when metadata appears complete; the fallback can respond to detectable unknown/malformed scope, not magically detect every unrecorded omission.

After updates stop, the protocol can progress if the finite required queries and scheduled invocations succeed. If queries fail or the call budget expires, return unresolved/incomplete rather than inventing completion. Continuous revisions carry no liveness guarantee. The mechanism handles no irreversible external effects in the first implementation.

### Primary comparison after independent review

The main causal control is a generic reconsideration planner with **the same current sources, typed artifacts, task records, context rendering, tools, feedback capability and model-call allowance**. Both see the same open questions. The proposed arm requires the operational discharge rule before accepting completion; the control can submit without fulfilling it. This estimates the effect of enforced reconsideration, including its induced acquisition work. A smaller matched-observation control tests whether any gain remains once refreshed information is equal.

A control-aware recovery baseline receives the same explicit completion nodes and read information. It may implement the identical rule. That reduction must be demonstrated rather than obscured; equivalence rules out claiming a distinct recovery algorithm.

## How imperfect reasoning and metadata are handled

- Missing exclusion notes do not eliminate the automatic root obligation.
- Narrow scope suggested by a model is advisory unless checked against runtime-owned scope information.
- Unknown scope triggers broad reopening; it never certifies safe non-reconsideration.
- Source freshness and actual decision accuracy are evaluated separately.
- The broad-reopening baseline reveals whether selective metadata provides real value.
- Final correctness is scored even if all process receipts are fresh. A confidently reclosed wrong task remains a failure.

This degrades toward reconsidering the task with preserved evidence, rather than toward invisible selective reuse. It may still fail to discover a relevant option. That failure must be reported, not masked by a successful protocol check.

## Why this is not a renamed invention

[Dynamic constraint maintenance](https://muller.unitime.org/lscs04.pdf) already restores values when elimination reasons disappear. [Incremental search](https://idm-lab.org/bib/abstracts/papers/aij04.pdf) reuses work while repairing affected search state. [REVISE](https://arxiv.org/html/2609.00643v1) already handles explicit control/membership dependencies. [MemContinuum's schema](https://raw.githubusercontent.com/krakozavr/MemContinuum/main/docs/SCHEMA.md) already records rejected alternatives and revisit triggers.

Therefore, none of the following is claimed as new: negative dependencies, reconsideration, rejection memory, versioned completion, selective replay, or validation-before-use. The **candidate contribution** is an operational distinction and measurement program for opaque multi-agent work: instrument completion automatically, keep scope uncertainty visible, and test whether preserving valid positive work while reopening stopping decisions repairs omissions at lower cost than stronger established baselines.

Where the interface is encoded as ordinary control nodes, call it a specialization of established recovery. That honest positioning is stronger than claiming a new algorithm whose novelty disappears under inspection.

## Generalization beyond SILO

- A coding workflow may retain a passing module while reopening whether the test suite covers a changed requirement.
- A research team may retain source extracts while reopening a literature-search boundary after the research question changes.
- A planning team may retain quotes and feasible subplans while reopening options excluded by an old constraint.
- A data workflow may retain cached answers to old queries while reopening whether those queries answer the new objective.

These are proposed application mappings, not demonstrated deployments. The transferable object is the separation between durable artifacts and revisable completion obligations. SILO-derived tasks provide controlled semantics; one additional search adapter is needed to demonstrate that the interface is not merely a numerical-task convention.

## What would make the scientific result interesting

The method may improve discovery of newly relevant options, reduce repeated acquisition, or prevent old completion messages from suppressing recovery. It may instead show that a fresh planner or a broad reopen policy is sufficient. Either result informs whether runtimes should invest in semantic scope extraction, explicit completion state, or simple evidence-preserving reconsideration.

Do not claim usefulness from a worked example or CPU state machine alone. Require the live, matched comparisons and kill conditions in [VALIDATION_STRATEGY.md](VALIDATION_STRATEGY.md) and [FALSIFICATION_AND_RISKS.md](FALSIFICATION_AND_RISKS.md).
