# Strategic architecture and validation handoff

**SUPPORTING NOTES — PROPOSED, NOT APPROVED OR IMPLEMENTED**

This document expands the engineering implications of [proposal Sections 9, 12, and 13](../silo-bench-lean-redesign-v2.md). It describes responsibilities and failure modes, not individual functions or a prescribed code structure. The existing [specification](../../../PROJECT_SPECIFICATION.md) and [implementation plan](../../IMPLEMENTATION_PLAN.md) remain governing documents until a separate adoption.

## Preserve the durable core; replace incompatible scientific assumptions

| Responsibility | Existing anchors | Proposed disposition |
|---|---|---|
| Mathematical worlds and exact truth | [tasks.py](../../../recovery/tasks.py) | Bind native I-08 and an independently checked scalar oracle; do not import native benchmark scoring wholesale |
| Sources, derived history, and intervention state | [state.py](../../../recovery/state.py), [events.py](../../../recovery/events.py) | Preserve the distinction; adapt two-peer correction, pending versions, literal history clearing, and reopening |
| Agent views and replies | [prompts.py](../../../recovery/prompts.py) | Simplify to ordinary messages, optional attachments, optional scalar submission; separate visible work from archived output |
| Scheduling and continuation | [rounds.py](../../../recovery/rounds.py), [runner.py](../../../recovery/runner.py) | Replace fixed four-peer/four-round assumptions for the new regime with bounded eligible turns |
| Model ownership and calls | [inference.py](../../../recovery/inference.py) | Reuse the demonstrated resident-worker path; requalify thinking framing, token limits, timeout, and fresh-state behavior |
| Durable outcomes and accounting | [storage.py](../../../recovery/storage.py), [attempts.py](../../../recovery/attempts.py) | Reuse persist-before-effects, exact resume, canonical attempt identity, and read-only reconstruction |
| Evaluation and reporting | [analysis.py](../../../recovery/analysis.py), [uncertainty.py](../../../recovery/uncertainty.py), [report.py](../../../recovery/report.py) | Replace fixed-slot outcomes/AUC with episode success and effort; retain world pairing and unknown-aware reporting |

“Reuse” is a responsibility-level judgment. It is not proof that the whole module is unchanged or compatible. Inspect how state shape, checkpoint boundaries, and consumers interact before committing to a change boundary.

## Three state boundaries must stay distinct

1. **Current permitted evidence:** each peer's private current records and exact records actually acquired, including explicit pending/obsolete status after an event.
2. **Working history:** visible messages, previous submissions, and bounded public validation feedback. This is the object of retain/reset.
3. **Audit evidence:** exact inputs, raw outputs, thinking, token IDs, settings, validation, timing, attempts, and durable effects. Clearing working history never deletes this archive.

Lifecycle state is additional control state: who may act, who is waiting, whose submission is active, and what review is pending. It must not smuggle old submissions into a reopened phase or reconstruct cleared history during resume.

The fork boundary must be drained and reproducible. All four continuations begin from the same realized prefix, with the event and retention transformations applied explicitly. Continuation generations are new. A completed call reused during exact resume is different from experimental sharing of a prefix; matching seeds are sufficient for neither.

## Assumptions that cannot survive unchanged

| Old assumption | Consequence under the proposal |
|---|---|
| Every active slot must produce an answer | Message-only and wait actions can be valid |
| Every peer acts in each synchronous round | Eligibility and submission can eliminate unused opportunities |
| Round four defines the prefix boundary | Completion, cap, or deadlock can end a phase; messages must still be drained before the fork |
| Submission ends a peer permanently | Incoming messages and phase events can reopen work |
| A previous candidate can stand in for a failed or missing output | Current-phase submissions must be explicit; stale candidates cannot fill gaps |
| Missing slots all have the same meaning | Unused opportunities after completion differ from executed failures and interrupted unknown episodes |
| All raw text is later conversational history | Private thinking and malformed raw outputs remain audit-only under the proposed framing |
| Existing non-thinking caps and timeouts are universal | Native mode boundaries and the new bounded context/output regime need validation |
| Notebook status or backup totals establish execution coverage | Coverage and attempts derive from canonical durable records |

Sequential delivery in the proposal differs from the current contract's synchronous visibility. This is an explicit proposed scientific-protocol change, not a scheduling optimization to sneak into an existing regime.

## Focused validation after adoption

The following matrix identifies evidence that would be needed later. It does not claim these redesigned checks exist or have passed.

| Boundary | Representative failure to exclude | Evidence needed before model pilot |
|---|---|---|
| I-08 mathematics | Treating an occurrence deletion as set deletion when another copy remains | Released-case reproduction and duplicate/last-occurrence counterexamples |
| View isolation | Hidden partner values, future edit type, or truth entering a prompt | Explicit permitted-view comparisons across representative states |
| Retain/reset | Reset deletes acquired sources or retain repairs wrong work | Matched current-source equality and literal-history checks |
| Source revision | Obsolete forwarded payload remains authoritative | Owner-local replacement, common invalidation, and subsequent exact forwarding checks |
| Completion | Gold-dependent stop, silent consensus, or ignored pending review | Scripted correct, wrong, disagreeing, waiting, and late-message traces |
| Turn limits | Polling waiters or transferring unused turns changes opportunity | Bounded per-agent schedules and terminal-state checks |
| Durability | Crash resamples a completed response or duplicates a delivery | Interruption before/after durable output and effects, then exact resume |
| Thinking/context | Hidden thinking crosses calls or legal history exceeds the cap | Native-template inspection, tokenizer envelope, and fresh-call state checks |
| Accounting | Backups, retries, or unused opportunities are miscounted | Reconstruct attempts and episode coverage from canonical evidence |
| Offline reporting | Unknown becomes zero, or branch count becomes sample size | Complete/incomplete paired-world examples and independent reconstruction |

Use existing validation where its invariant and interface remain unchanged. The [durable-worker evidence](../../validation/course-m3-durable-workers-and-failures.md) and [state/replay investigation](../../implementation-research/state-and-replay.md) are valuable prerequisites; they are not a reason to rerun every old check or skip checks of changed behavior.

## Keep operational risk small

Maintain one model replica and serial worker per device, no hidden cross-call state, one durable record of actual outcomes, and derived reports. Two devices can execute separate worlds; do not interpret that as pooled memory or halved aggregate GPU cost.

The known checkpoint-size and backup-counting defects matter where the selected path reuses them. Repairing unrelated old pipeline stages, rebuilding all persistence, adding a generic event framework, or completing every old milestone is not a prerequisite to this smaller study.

Retire receipt crossings, delayed prose, mixed retention masks, the C/K rule, and multi-family schedules from the proposed active regime while preserving their existing artifacts for future thesis work. Retirement from a new study does not mean deletion or retroactive invalidation of earlier evidence.

## Dependency order for a later authorized implementation

1. Adopt the scientific scope and explicitly document changed semantics, claims, and allocation.
2. Establish the exact I-08 task/population and agent-visible state boundary.
3. Adapt lifecycle, optional submissions, durable forks, and resume semantics together.
4. Adapt model framing and prove the finite input envelope; prepare truthful attempt/coverage reporting.
5. Complete focused CPU checks and prepare the concrete bounded qualification packet.
6. Run authorized hardware/competence qualification, then the complete pilot; freeze only the configuration supported by that evidence.
7. Execute and report the intended main population with exact outcomes, costs, failures, and missingness.

This order keeps scientific ambiguities from becoming entrenched in infrastructure. A finished runner is not evidence that the task is attainable, the intervention is meaningful, or the main study should run.
