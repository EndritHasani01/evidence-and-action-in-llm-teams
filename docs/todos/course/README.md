# ABS/IIS course implementation tasks

This is the separate course task tree. The [existing thesis index](../README.md) and its M1–M6 files remain unchanged. IDs such as M2-T01 are local to this tree; name `course/M2-T01` or its full path when requesting implementation.

Authority: [PROJECT_SPECIFICATION.md](../../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime). Roadmap: [IMPLEMENTATION_PLAN.md](../../IMPLEMENTATION_PLAN.md#11-course-living-handoff). Follow [AGENTS.md](../../../AGENTS.md). The [course proposal](../../planning/abs-iis-course-study-proposal.md) records the proposed changes before adoption; it is not an alternative scientific authority. [Research synthesis](../../implementation-research/SYNTHESIS.md) supplies supporting evidence.

Fresh sessions can start with the [course handoff and practical lessons](../../planning/course-study-session-handoff.md) for the reading path, reusable evidence and known failure points. This index remains the course progress view.

Course scientific/resource adoption was explicitly approved on 9 October 2026.
Existing M1–M4 and thesis M5-T01 retain completion evidence: 21/29 original tasks.
Course inputs/schedules and their M1 CPU gate are verified. Runtime configuration,
later CPU gates, pretrained-model admission, pilot, freeze and empirical execution
remain pending. Task creation and design/resource adoption authorize no execution.

## Adopted course scope

The adopted scientific clause specifies one Qwen3.5-4B text-only NF4 configuration; numeric m=6; BFS eight nodes/twelve edges; five families; 20 main worlds with each edited owner represented once per family; five disjoint development worlds; four peers and four rounds per phase; 256 generated tokens and 64 prose tokens; unchanged feedback/reference/recipient limits. Receipt/Q/preserving populations have eight worlds each; extra continuation repeats have the first one per family, five total. Actual configuration acceptance remains a later gate.

The complete main schedule is **5,752 new generations / 6,280 logical opportunities**. Development is **1,114 / 1,178**, including the initial 90 capability slots. Smoke is separately limited to 24 calls and 0.5 aggregate GPU-hour. The adopted cumulative course ceiling is 30 aggregate GPU-hours inside the existing 100-hour overall ceiling, retaining 8/2/2-hour development/setup/interruption reserves and a 25% main margin. [Section 11.3](../../../PROJECT_SPECIFICATION.md#113-cumulative-resources-and-admission) governs shared prior spending and unknown allocation. These are planned counts and limits, not executed results or available quota.

Four recovery rounds are the default here. The proposal's three-round alternative is not an automatic fallback or another required implementation. Changes to horizon, caps, size, populations, model or resources require an explicit decision and renewal of affected evidence before main freeze. The original thesis regime remains available and its outstanding gates remain separate.

## Progress and next work

**2/21 course tasks done; 19 remaining; 0 active; 1 ready; 18 blocked.**
Course/M1-T01 is done: explicit adoption, the approved scientific/plan amendment,
verified reuse boundaries and [contract/handoff evidence](../../validation/course-m1-contract-and-reuse.md#completion-and-handoff)
are recorded. Course/M1-T02 is done: saved inputs, balanced cohorts, isolated
seeds and complete schedules pass the [M1 input/schedule gate](../../validation/course-m1-inputs-and-schedules.md#completion-and-handoff).
Full CPU validation passes 534 tests with zero skips. Later runtime adaptations
and course CPU gates remain open. Inherited
foundation tasks are not counted as course acceptance.

The next safe task is [course/M2-T01](M2/M2-T01-course-protocol-and-limits.md), following completed [course/M1-T02](M1/M1-T02-course-inputs-and-schedules.md). **Ready** means safe work can start; any authorization needed to finish remains explicit. **Blocked** means a listed prerequisite, evidence handoff or required authorization is missing. **Active** means implementation is underway. **Done** requires linked passing evidence. Counts describe verified task outcomes, not effort or runtime; a terminal failure is recorded without changing an unmet gate to done.

| Milestone | Done / tasks | Active | Ready | Blocked | Gate |
|---|---:|---:|---:|---:|---|
| M1 | 2/2 | 0 | 0 | 0 | Adopted contract/reuse audit and complete course input/schedule CPU gate passed |
| M2 | 0/3 | 1 | 0 | 2 | Lawful views, literal interventions, exact replay, legal witness and complete course token bound |
| M3 | 0/2 | 0 | 0 | 2 | Durable workers, bounded failures, honest accounting and crash-safe lifecycle |
| M4 | 0/4 | 0 | 0 | 4 | Course outcomes, uncertainty, costs and reproducible synthetic reporting; pre-GPU CPU gate |
| M5 | 0/5 | 0 | 0 | 5 | Actual-host smoke, capability, complete pilot, conservative resources and authorized course freeze |
| M6 | 0/5 | 0 | 0 | 5 | Complete frozen execution, independent audit, claims review, clean local reproduction and agreed delivery |

## Task index

Dependencies refer only to this course tree. Authorization, resource availability and quiescent evidence handoffs remain separate prerequisites where the task says so.

| Task | Status | Required task dependencies |
|---|---|---|
| [M1-T01 — Course contract and reuse boundary](M1/M1-T01-course-contract-and-reuse-boundary.md) | done | Scientific/resource adoption and contract/reuse audit passed |
| [M1-T02 — Course inputs and schedules](M1/M1-T02-course-inputs-and-schedules.md) | done | M1-T01 |
| [M2-T01 — Course protocol and limits](M2/M2-T01-course-protocol-and-limits.md) | active | M1-T02 |
| [M2-T02 — Course interventions and replay](M2/M2-T02-course-interventions-and-replay.md) | blocked | M2-T01 |
| [M2-T03 — Course attainability and capacity](M2/M2-T03-course-attainability-and-capacity.md) | blocked | M2-T02 |
| [M3-T01 — Course durable workers and failures](M3/M3-T01-course-durable-workers-and-failures.md) | blocked | M2-T03 |
| [M3-T02 — Course accounting and lifecycle gate](M3/M3-T02-course-accounting-and-lifecycle-gate.md) | blocked | M3-T01 |
| [M4-T01 — Course outcomes and estimands](M4/M4-T01-course-outcomes-and-estimands.md) | blocked | M3-T02 |
| [M4-T02 — Course diagnostics and policy costs](M4/M4-T02-course-diagnostics-and-policy-costs.md) | blocked | M4-T01 |
| [M4-T03 — Course uncertainty and missingness](M4/M4-T03-course-uncertainty-and-missingness.md) | blocked | M4-T01, M4-T02 |
| [M4-T04 — Course report and CPU gate](M4/M4-T04-course-report-and-cpu-gate.md) | blocked | M4-T02, M4-T03 |
| [M5-T01 — Course inference and smoke preparation](M5/M5-T01-course-inference-and-smoke-preparation.md) | blocked | M2-T03, M3-T02 |
| [M5-T02 — Course hardware smoke and memory](M5/M5-T02-course-hardware-smoke-and-memory.md) | blocked | M4-T04, M5-T01 |
| [M5-T03 — Course capability-first pilot](M5/M5-T03-course-capability-first-pilot.md) | blocked | M5-T02 |
| [M5-T04 — Course complete pilot and timing](M5/M5-T04-course-complete-pilot-and-timing.md) | blocked | M5-T03 |
| [M5-T05 — Course admission and freeze](M5/M5-T05-course-admission-and-freeze.md) | blocked | M5-T04 |
| [M6-T01 — Course frozen execution and resume](M6/M6-T01-course-frozen-execution-and-resume.md) | blocked | M5-T05 |
| [M6-T02 — Course artifact and coverage audit](M6/M6-T02-course-artifact-and-coverage-audit.md) | blocked | M4-T04 + evidence handoff* |
| [M6-T03 — Course results and claims](M6/M6-T03-course-results-and-claims.md) | blocked | M6-T02 |
| [M6-T04 — Course local reproducible release](M6/M6-T04-course-local-reproducible-release.md) | blocked | M6-T03 |
| [M6-T05 — Course authorized delivery](M6/M6-T05-course-authorized-delivery.md) | blocked | M6-T04 |

*Evidence handoff is a complete or safely stopped main bundle **OR** documented terminal M5 feasibility evidence. The audit/report/local-release/delivery route does not require passing the failed M5 gate or finishing main execution. Its outcome is explicitly limited; blocked/unfinished execution tasks remain outstanding. Intended empirical completion requires the full frozen schedule and release checks. External delivery is required only if explicitly agreed; the default deliverable is local.

## Reuse and execution boundaries

| Existing foundation | Course responsibility |
|---|---|
| M1 truth, edits, populations and schedules | Adapt inputs/cohorts and verify new counts; preserve original 60/40 schedules |
| M2 views, parser, retention, replay and witness/capacity | Carry course limits through all representations; renew affected protocol/proof checks |
| M3 durable workers, bounded attempts, accounting and lifecycle | Integrate course configuration using existing records; verify course lifecycle and resource admission |
| M4 outcomes, estimands, diagnostics, uncertainty and reports | Verify 20/eight/five-world scopes, intended-population missingness and course reports |
| M5 direct adapter, accepted CPU preparation and standalone T4 diagnostics | Verify current 4B/course source and complete memory envelope, actual model smoke, pilot and freeze |

The [existing CPU gate](../../validation/m4-cpu-gate.md), [inference task evidence](../M5/M5-T01-inference-and-allocation-preparation.md) and [attention/memory audit](../../validation/m5-attention-memory.md) are reusable only for unchanged behavior. They do not demonstrate that course caps/counts, the new CUDA layout or pretrained-model feasibility pass.

M5-T01 CPU preparation may proceed after its inputs/runner prerequisites while M4 is finishing. No GPU allocation/inference is admitted before course M1–M4 gates, the concrete runtime packet, resource checks and applicable explicit authorization. Smoke precedes the 90-slot capability screen; that screen precedes recovery-pilot spending; full pilot and forecast precede freeze; main execution requires separate authorization. Passing a gate grants no authorization. Unresolved historical allocation remains unknown, and two GPUs shorten elapsed time without halving aggregate device-hours.

## Requirement coverage audit

These owners cover all 22 rows in [plan §9](../../IMPLEMENTATION_PLAN.md#9-coverage-map). Each task links its detailed authority, acceptance and validation context; unchanged implementation is reused and only affected course evidence is renewed.

| Specification / plan coverage row | Course task owners |
|---|---|
| §1 research design/estimands | M1-T01–T02; M4-T01; M6-T03 |
| §2.1 tasks/distributions | M1-T02 |
| §2.2 sampling/reproducibility | M1-T02; M3-T01; M5-T05; M6-T02 |
| §2.3 events/populations | M1-T02; M2-T02 |
| §3.1 visibility | M2-T01–T02; M3-T01; M6-T02 |
| §3.2 protocol/rounds/caps | M2-T01–T03; M5-T01–T02 |
| §4.1 retention/delivery | M2-T02; M4-T01 |
| §4.2 complementary groups | M1-T02; M2-T02; M3-T01; M4-T01 |
| §4.3 historical receipts | M2-T02; M4-T01–T02 |
| §4.4 prose delay | M2-T02; M3-T01; M4-T01–T02 |
| §5.1 exact outcomes | M1-T02; M4-T01; M6-T02 |
| §§5.2–5.4 all contrasts | M4-T01; M6-T03 |
| §6 statistics/repeats/missingness | M1-T02; M3-T02; M4-T01–T03; M6-T01–T03 |
| §7.1 repair/preservation/trajectories | M4-T01–T02 |
| §7.2 information/work | M2-T02; M4-T02 |
| §7.3 quality/cost/boundary rule | M3-T02; M4-T02–T03 |
| §7.4 narrative/cases | M4-T04; M6-T03 |
| §8.1 inference/controls | M1-T02; M5-T01–T03 |
| §8.2 CPU/pilot/fallback | M2-T03; M3-T02; M4-T04; M5-T01–T04; M1-T01 for any course scope change |
| §§8.3–8.4 schedule/resources/freeze | M1-T01–T02; M3-T02; M5-T04–T05; M6-T01 |
| §9 implementation/consistency/publication | M2-T01–T03; M3-T01–T02; M4-T04; M5-T01–T02; M6-T02–T05 |
| §10 attribution/limits/exclusions | M1-T01; M4-T04; M6-T03–T05 |

The seven [specification §9 essential checks](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements) have explicit owners: **task truth** M1-T02; **visibility** M2-T01–T02; **state interventions** M2-T02; **synchrony and replay** M2-T02/M3-T01; **failure/restart** M3-T01–T02/M5-T02; **analysis** M4-T01–T03; **accounting and capacity** M1-T02/M2-T03/M3-T02/M4-T02/M5-T02–T05. M4-T04 consolidates the pre-GPU audit; M6-T02 audits actual evidence. Plan architecture, authorization and living-progress obligations are owned by M1-T01 and the relevant gate/delivery tasks.

## Implementing one task and updating progress

Select one full task path and read its referenced authority/evidence; the entire tree need not be loaded. Implement only that outcome, reusing existing modules/IDs/configuration/ledgers. Record named commands, environment, actual results, artifact locations and limits in the task evidence. Update its status, counts and newly unblocked dependencies here together; update the existing plan's living sections for consequential decisions or verified progress. Leave thesis task files/statuses intact. Reopen affected gates after changes without rewriting prior results.

Runtime evidence belongs in the existing canonical bundles/checkpoints/ledgers; exports are derived views. These Markdown statuses describe implementation progress, not another experimental record store. Distinguish implemented, verified, pilot-tested and empirically executed work. Course completion does not close the original thesis obligations.

Task-system review, 9 October 2026, Windows/Python 3.11.9: documentation checks pass for 22 Markdown files, 21 scoped IDs, local links/heading anchors, acyclic dependencies, progress counts, execution gates, all 22 plan coverage rows and seven essential categories. Course main/development totals reconcile independently. All 30 existing todo files and inspected authority/research/proposal files remain byte-for-byte unchanged; the pre-existing local evidence edit is preserved. No project-code tests, model calls or GPU runs were performed for this documentation work.
