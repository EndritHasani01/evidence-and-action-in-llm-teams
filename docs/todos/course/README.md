# ABS/IIS course implementation tasks

This is the separate course task tree. The [existing thesis index](../README.md) and its M1–M6 files remain unchanged. IDs such as M2-T01 are local to this tree; name `course/M2-T01` or its full path when requesting implementation.

Authority: [PROJECT_SPECIFICATION.md](../../../PROJECT_SPECIFICATION.md). Roadmap: [IMPLEMENTATION_PLAN.md](../../IMPLEMENTATION_PLAN.md). Follow [AGENTS.md](../../../AGENTS.md). The [course proposal](../../planning/abs-iis-course-study-proposal.md) supplies proposed changes, not an alternative scientific authority. [Research synthesis](../../implementation-research/SYNTHESIS.md) supplies supporting evidence.

Inspected 9 October 2026 at `d04a904`. Existing M1–M4 and thesis M5-T01 have completion evidence: 21/29 original tasks. That foundation is reused, not rebuilt or counted as course acceptance. Course configuration, course CPU gates, model admission, pilot, freeze, and empirical execution have not been completed.

## Proposed course scope

M1-T01 must establish explicit adoption in the scientific authority before behavioral changes. The starting proposal is one Qwen3.5-4B text-only NF4 configuration; numeric m=6; BFS eight nodes/twelve edges; five families; 20 worlds with four edited owners per family; five disjoint development worlds; four peers and four rounds in each phase; 256 generated tokens and 64 prose tokens; unchanged 32-token feedback and reference/recipient limits. Receipt/Q/preserving populations contain eight worlds each; extra continuation repeats contain the first one per family, five total. Main generations/logical opportunities are 5,752/6,280; development is 1,114 with the first 90 capability slots included; smoke is separately capped at 24 calls and 0.5 aggregate GPU-hour. The proposed course ceiling is 30 aggregate GPU-hours with the current 8/2/2-hour development/setup/interruption reserves and 25% main margin, subject to explicit adoption and prior-spending treatment.

Four recovery rounds are the default for this task system. The proposal's three-round alternative is not an automatic fallback or another required implementation. Changing horizon, caps, sample size, model, or resources requires an explicit decision and renewal of affected evidence before main freeze.

## Progress and next work

Foundation-task documentation checkpoint: **0/11 course tasks done; 11 remaining; 0 active; 1 ready; 10 blocked.** M5/M6 execution and release contracts will complete this index in the next documentation checkpoint before handoff. No project implementation is being performed during task-system creation.

The next safe task is [course/M1-T01](M1/M1-T01-course-contract-and-reuse-boundary.md). Ready means safe work can start; any authorization needed to finish remains explicit. Blocked means a listed prerequisite or evidence handoff is missing. Active means implementation is underway. Done requires linked passing evidence. Counts are verified task outcomes, not estimated effort or GPU time.

| Milestone | Done / tasks | Ready | Blocked | Gate |
|---|---:|---:|---:|---|
| M1 | 0/2 | 1 | 1 | Adopted course contract; independently verified inputs, populations and counts |
| M2 | 0/3 | 0 | 3 | Lawful views, literal interventions, exact replay, legal witness and complete course token bound |
| M3 | 0/2 | 0 | 2 | Durable course workers, bounded failures, honest accounting and crash-safe lifecycle |
| M4 | 0/4 | 0 | 4 | Course outcomes, uncertainty, costs and reproducible synthetic reporting |

## Task index and requirement ownership

| Task | Status | Required task dependencies | Plan/specification coverage |
|---|---|---|---|
| [M1-T01 — Course contract and reuse boundary](M1/M1-T01-course-contract-and-reuse-boundary.md) | ready | None; explicit adoption before applying scientific changes | Plan §§1–2, 9–10; spec §§1–2, 8–10; course scope |
| [M1-T02 — Course inputs and schedules](M1/M1-T02-course-inputs-and-schedules.md) | blocked | M1-T01 | Plan §3; spec §§2, 4, 5.1, 8.2–8.3, 9 |
| [M2-T01 — Course protocol and limits](M2/M2-T01-course-protocol-and-limits.md) | blocked | M1-T02 | Plan §4 and visibility boundaries; spec §§3, 8.1, 9 |
| [M2-T02 — Course interventions and replay](M2/M2-T02-course-interventions-and-replay.md) | blocked | M2-T01 | Plan §§2, 4; spec §§4, 9 |
| [M2-T03 — Course attainability and capacity](M2/M2-T03-course-attainability-and-capacity.md) | blocked | M2-T02 | Plan §4 gate; spec §§3.2, 8.2, 9 |
| [M3-T01 — Course durable workers and failures](M3/M3-T01-course-durable-workers-and-failures.md) | blocked | M2-T03 | Plan §§2, 5 persistence/failures/workers; spec §§3–4, 6, 9 |
| [M3-T02 — Course accounting and lifecycle gate](M3/M3-T02-course-accounting-and-lifecycle-gate.md) | blocked | M3-T01 | Plan §5 accounting/progress/gate; spec §§6, 7.3, 8.3–8.4, 9 |
| [M4-T01 — Course outcomes and estimands](M4/M4-T01-course-outcomes-and-estimands.md) | blocked | M3-T02 | Plan §6 outcomes/contrasts; spec §§5, 6 repetition, 7.1 |
| [M4-T02 — Course diagnostics and policy costs](M4/M4-T02-course-diagnostics-and-policy-costs.md) | blocked | M4-T01 | Plan §6 explanation/costs; spec §§7.1–7.3 |
| [M4-T03 — Course uncertainty and missingness](M4/M4-T03-course-uncertainty-and-missingness.md) | blocked | M4-T01, M4-T02 | Plan §6 uncertainty/incompletion; spec §§5–6, 7.3 |
| [M4-T04 — Course report and CPU gate](M4/M4-T04-course-report-and-cpu-gate.md) | blocked | M4-T02, M4-T03 | Plan §6 report/gate; spec §§7.4, 9–10 |

## Reuse and updating evidence

The [existing CPU gate](../../validation/m4-cpu-gate.md) establishes generators/truth, strict protocol, literal transformations/replay, real durable workers/accounting, and offline analysis/reporting. [Inference preparation](../M5/M5-T01-inference-and-allocation-preparation.md) supplies an existing direct adapter; [offline attention/memory evidence](../../validation/m5-attention-memory.md) remains CPU/source evidence. The course tasks own only changed configuration support, affected regression checks, and course-scoped acceptance. Existing code is not evidence that the new caps/counts already pass. GPU library diagnostics do not establish pretrained-model feasibility.

For a future implementation session, select one full task path, read that task and its referenced authority/evidence, implement only its outcome, and record named commands, environment, pass/failure results, artifact locations and limits in its evidence section. Update its status and this index together; update the plan's living sections for verified course progress or consequential discoveries. Leave thesis task files/statuses intact. Reopen affected course gates after changes rather than rewriting prior results. Store runtime evidence in existing canonical bundles/checkpoints/ledgers and derive exports; these Markdown statuses are implementation progress only.

No GPU work is admitted until all course M1–M4 gates pass. Metadata/tokenizer downloads and CPU checks may run earlier. Technical gates and execution authorization remain separate. Course completion will not complete the original thesis obligations.
