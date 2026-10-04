# Implementation tasks

Authority: [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md). Engineering roadmap: [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md). Apply the [repository contract](../../AGENTS.md); [research synthesis](../implementation-research/SYNTHESIS.md) supplies supporting evidence.

Baseline inspected 4 October 2026: no current recovery implementation, accepted pilot or main results. Historical probes do not complete these tasks. This task system contains only this index and 29 task files in M1–M6; task IDs remain stable.

## Progress and next work

**Completed: 5/29. Remaining: 24. Active: 0. Ready: 1. Blocked: 23.** Counts measure verified task outcomes, not effort or runtime.

- [M1-T01](M1/M1-T01-task-worlds-and-truth.md#validation-and-evidence) is done: all five families at both sizes, exact truth/coordinates, ten attributed fixtures and 23 CPU checks pass.
- [M1-T02](M1/M1-T02-edits-and-populations.md#validation-and-evidence) is done: eligible edits, 60/40 nested populations, five development worlds, partitions, saved streams and manifest equality pass in the 42-check CPU suite.
- [M1-T03](M1/M1-T03-complete-schedules.md#validation-and-evidence) is done: independent 60/40 main totals, exact development/capability populations, prefix/reply parents, saved schedules and CPU handoff pass in the 59-check suite. M1's CPU gate is passed.
- [M2-T01](M2/M2-T01-peer-views-and-rendering.md#completion-and-handoff) is done: permitted immutable views, current/pending/deleted source authority, historical/derived work and exact request/token rendering pass in the 79-check CPU suite plus five native-tokenizer checks. Complete capacity admission remains M2-T06.
- [M2-T02](M2/M2-T02-strict-replies-and-feedback.md#completion-and-handoff) is done: strict whole-reply schemas/permissions, actual token limits, public feedback and absent invalid/failed candidates pass in the 103-check source/installed CPU suites plus six native protocol checks. The original five native renderer checks still pass.
- Next unblocked task: [M2-T03](M2/M2-T03-synchronous-rounds-and-prefixes.md), synchronous round delivery and immutable drained prefixes.
- Other blocked tasks await their listed prerequisites; dependency-blocked is distinct from a failed gate.
- No GPU run, main experiment, scientific/frozen-configuration change or publication is authorized by creation of this task system.

| Milestone | Done | Remaining | Current state | Milestone gate |
|---|---:|---:|---|---|
| M1 | 3/3 | 0 | Passed on CPU | Exact worlds, coordinates, eligible populations, saved streams and complete schedules pass; [M1-T03 gate evidence](M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate) closes M1. |
| M2 | 2/6 | 4 | M2-T03 ready | Peer views/rendering and strict replies verified; still requires synchronous interventions/replay, local-view witness and complete tokenizer bound; close in [M2-T06](M2/M2-T06-attainability-and-capacity.md). |
| M3 | 0/5 | 5 | Blocked by M2 | Durable scripted lifecycle, real process-crash/restart, worker replay, accounting and safe-stop checks pass; close in [M3-T05](M3/M3-T05-crash-safe-scripted-lifecycle.md). |
| M4 | 0/6 | 6 | Blocked by M1–M3 | All prescribed offline analysis and complete synthetic report reproduce; all M1–M4 CPU evidence passes in [M4-T06](M4/M4-T06-reproducible-report-and-cpu-gate.md). |
| M5 | 0/5 | 5 | Blocked by M1–M4 | Authorized smoke → 90-slot capability gate → full pilot → measured complete-schedule forecast and freeze; close in [M5-T05](M5/M5-T05-allocation-admission-and-freeze.md). |
| M6 | 0/4 | 4 | Blocked by M5 / evidence | Full frozen schedule, independent audit, clean offline reproduction and authorized release pass; completion requires [M6-T01](M6/M6-T01-frozen-execution-and-resume.md) and [M6-T04](M6/M6-T04-reproducible-release.md). |

## Selecting and updating a task

Statuses are **ready** (prerequisites satisfied), **active** (being worked), **blocked** (dependency, gate, missing evidence or authorization), and **done** (completion criteria and named validation passed). Record a concrete blocker when it is more specific than the listed dependencies. Code existence alone is not done.

Read the selected task, its linked specification/plan sections and prerequisite acceptance evidence; the entire task tree is not required. Dependencies below are direct prerequisites; transitive dependencies need not be repeated. Respect the roadmap's milestone order. Within a milestone, tasks without a dependency on each other can proceed independently.

At session start, confirm prerequisites against actual artifacts and set the task active. At handoff, record commands, environment, results and artifact paths in its evidence section; update status/blocker, this index, milestone counts/gate state and newly unblocked tasks together. Task files own task status/evidence; this table is their summary, not another evidence store. Update the existing plan's living sections for verified capability, consequential decisions, defects or blocked gates. Do not add trackers, scripts, manifests or another planning hierarchy.

If a change invalidates prior checks, reopen affected tasks/gates and record why. Preserve IDs and existing evidence. Do not silently redesign a scientific requirement; document the precise ambiguity and seek the authorization required by the repository contract.

## Task index and coverage

Coverage names the source sections owned by each outcome; detailed acceptance and validation live only in the linked task. Plan §§3–8 map to M1–M6. Cross-cutting plan §2 architecture is assigned to the world/CPU entry point, peer-view, durable-runner, worker, ledger, offline-analysis and freeze tasks. Plan §1 gates and §10 handoff obligations apply throughout. This structure also implements the plan §9 specification coverage map without another requirement-ID system.

| Task | Status | Direct prerequisites | Source coverage |
|---|---|---|---|
| [M1-T01 — Exact task worlds and coordinate contracts](M1/M1-T01-task-worlds-and-truth.md) | done | None | Plan §§2–3; spec §§2.1, 5.1, 7.1, 8.1–8.2, 9–10 |
| [M1-T02 — Eligible edits and reproducible populations](M1/M1-T02-edits-and-populations.md) | done | [M1-T01](M1/M1-T01-task-worlds-and-truth.md) | Plan §3; spec §§2.2–2.3, 4.2, 6, 8.2, 9 |
| [M1-T03 — Complete schedules and replay dependencies](M1/M1-T03-complete-schedules.md) | done | [M1-T02](M1/M1-T02-edits-and-populations.md) | Plan §§1–3, 9; spec §§2.3, 4, 8.1–8.3, 9 |
| [M2-T01 — Permitted peer views and lossless rendering](M2/M2-T01-peer-views-and-rendering.md) | done | [M1-T03](M1/M1-T03-complete-schedules.md) | Plan §§2, 4; spec §§3.1, 4.3–4.4, 9 |
| [M2-T02 — Strict reply validation and public feedback](M2/M2-T02-strict-replies-and-feedback.md) | done | [M2-T01](M2/M2-T01-peer-views-and-rendering.md) | Plan §4; spec §§3.2, 5.1, 8.1, 9 |
| [M2-T03 — Synchronous rounds and immutable shared prefixes](M2/M2-T03-synchronous-rounds-and-prefixes.md) | ready | [M2-T02](M2/M2-T02-strict-replies-and-feedback.md) | Plan §§2, 4; spec §§2.2, 3.1–3.2, 9 |
| [M2-T04 — Literal events, retention boundaries and receipts](M2/M2-T04-events-retention-and-receipts.md) | blocked | [M2-T03](M2/M2-T03-synchronous-rounds-and-prefixes.md) | Plan §4; spec §§2.3, 4.1–4.3, 9 |
| [M2-T05 — Exact mixed-group replay and prose-delay delivery](M2/M2-T05-mixed-and-prose-delay-replay.md) | blocked | [M2-T04](M2/M2-T04-events-retention-and-receipts.md) | Plan §§2, 4; spec §§4.2, 4.4, 9 |
| [M2-T06 — Protocol attainability and complete tokenizer capacity](M2/M2-T06-attainability-and-capacity.md) | blocked | [M2-T05](M2/M2-T05-mixed-and-prose-delay-replay.md) | Plan §4 gate; spec §§3.2, 8.2, 9 |
| [M3-T01 — Durable rounds and exact response reuse](M3/M3-T01-durable-round-runner.md) | blocked | [M2-T06](M2/M2-T06-attainability-and-capacity.md) | Plan §§2, 5; spec §§3–4, 9 |
| [M3-T02 — Bounded attempts, timeouts and interruption semantics](M3/M3-T02-bounded-attempts-and-failures.md) | blocked | [M3-T01](M3/M3-T01-durable-round-runner.md) | Plan §5; spec §§3.2, 6, 9 |
| [M3-T03 — Local worker scheduling and cross-worker replay](M3/M3-T03-local-worker-scheduling.md) | blocked | [M3-T02](M3/M3-T02-bounded-attempts-and-failures.md) | Plan §§2, 5, 8; spec §§8.1, 8.4, 9 |
| [M3-T04 — Resource accounting, progress and safe budget stops](M3/M3-T04-accounting-progress-and-budget.md) | blocked | [M3-T03](M3/M3-T03-local-worker-scheduling.md) | Plan §5; spec §§6, 7.3, 8.3–8.4, 9 |
| [M3-T05 — Crash-safe scripted lifecycle acceptance](M3/M3-T05-crash-safe-scripted-lifecycle.md) | blocked | [M3-T04](M3/M3-T04-accounting-progress-and-budget.md) | Plan §5 gate; spec §§4.2, 4.4, 6, 8.3–8.4, 9 |
| [M4-T01 — Exact outcomes, preservation and trajectories](M4/M4-T01-exact-outcomes-and-trajectories.md) | blocked | [M3-T05](M3/M3-T05-crash-safe-scripted-lifecycle.md) | Plan §6 outcomes/diagnostics; spec §§5.1, 6, 7.1, 9 |
| [M4-T02 — All prespecified contrasts and repeatability](M4/M4-T02-estimands-and-repeatability.md) | blocked | [M4-T01](M4/M4-T01-exact-outcomes-and-trajectories.md) | Plan §6 contrasts; spec §§1, 5.2–5.4, 6 |
| [M4-T03 — Information inventories and retained-work references](M4/M4-T03-information-and-work-diagnostics.md) | blocked | [M4-T01](M4/M4-T01-exact-outcomes-and-trajectories.md) | Plan §6 explanatory outcomes; spec §§2.2, 7.2, 10 |
| [M4-T04 — Policy costs and the frozen boundary rule](M4/M4-T04-policy-costs-and-boundary-rule.md) | blocked | [M4-T01](M4/M4-T01-exact-outcomes-and-trajectories.md) | Plan §6 costs; spec §7.3 |
| [M4-T05 — Paired uncertainty and shared-response missingness](M4/M4-T05-uncertainty-and-missingness.md) | blocked | [M4-T02](M4/M4-T02-estimands-and-repeatability.md), [M4-T04](M4/M4-T04-policy-costs-and-boundary-rule.md) | Plan §6 uncertainty; spec §§5–6, 7.3, 9 |
| [M4-T06 — Reproducible report and pre-GPU analysis gate](M4/M4-T06-reproducible-report-and-cpu-gate.md) | blocked | [M4-T03](M4/M4-T03-information-and-work-diagnostics.md), [M4-T05](M4/M4-T05-uncertainty-and-missingness.md) | Plan §§6, 9–10; spec §§7.4, 9–10 |
| [M5-T01 — Inference backend and allocation preparation](M5/M5-T01-inference-and-allocation-preparation.md) | blocked | [M4-T06](M4/M4-T06-reproducible-report-and-cpu-gate.md) | Plan §7 runtime; spec §§8.1, 8.4, 9 |
| [M5-T02 — Bounded hardware smoke and host validation](M5/M5-T02-hardware-smoke-and-host-validation.md) | blocked | [M5-T01](M5/M5-T01-inference-and-allocation-preparation.md); execution authorization | Plan §7 runtime/smoke; spec §§8.1–8.2, 8.4, 9 |
| [M5-T03 — Capability-first 90-slot pilot gate](M5/M5-T03-capability-first-pilot.md) | blocked | [M5-T02](M5/M5-T02-hardware-smoke-and-host-validation.md); execution authorization | Plan §7 capability/fallback; spec §§8.1–8.2, 8.4 |
| [M5-T04 — Complete development pilot and measured timing](M5/M5-T04-complete-pilot-and-timing.md) | blocked | [M5-T03](M5/M5-T03-capability-first-pilot.md); execution authorization | Plan §7 pilot/forecast; spec §§8.2–8.4, 9 |
| [M5-T05 — Complete-schedule admission and immutable freeze](M5/M5-T05-allocation-admission-and-freeze.md) | blocked | [M5-T04](M5/M5-T04-complete-pilot-and-timing.md) | Plan §7 freeze; spec §§6–9 |
| [M6-T01 — Frozen main execution and safe resume](M6/M6-T01-frozen-execution-and-resume.md) | blocked | [M5-T05](M5/M5-T05-allocation-admission-and-freeze.md); execution authorization | Plan §8 execution/deviations; spec §§2.2, 6, 8.3–8.4, 9 |
| [M6-T02 — Independent artifact and coverage audit](M6/M6-T02-independent-artifact-audit.md) | blocked | [M4-T06](M4/M4-T06-reproducible-report-and-cpu-gate.md); evidence handoff* | Plan §8 audit/limited outcome; spec §§5–6, 8–9 |
| [M6-T03 — Recorded results and evidence-grounded claims](M6/M6-T03-results-and-claims-review.md) | blocked | [M6-T02](M6/M6-T02-independent-artifact-audit.md) | Plan §8 reporting; spec §§1, 5–7, 10 |
| [M6-T04 — Reproducible release and authorized publication](M6/M6-T04-reproducible-release.md) | blocked | [M6-T03](M6/M6-T03-results-and-claims-review.md); authorization before publication | Plan §§8, 10; spec §§9–10 |

## Execution and limited-outcome gates

No GPU use before **all M1–M4 gates pass**. Tokenizer/configuration downloads and CPU checks are permitted earlier. In M5, smoke is bounded by 24 calls or 0.5 aggregate GPU-hour, whichever comes first. Only a passing smoke admits the first 90 capability slots; only their capability thresholds admit recovery pilot calls. The complete accepted pilot, measured resource forecast and immutable freeze precede main execution.

Technical gate passage and explicit authorization are separate requirements. Complete safe preparation before requesting authorization, and reuse authorization already granted within its scope. A failed gate neither permits execution nor requires speculative new infrastructure. Configuration changes reopen affected evidence; the only predefined model/size/population fallbacks are those in the specification.

*The M6-T02 evidence handoff is a real alternative prerequisite: a complete or safely stopped M6-T01 bundle, **or documented terminal M5 feasibility evidence**, plus completed M4-T06. A still-running or undocumented failed attempt is not a handoff. This lets audits, limited reports and release preparation proceed without pretending that a failed gate passed. M6-T02–T04 can become ready through this route even while M5 or M6-T01 remains blocked.

A partial run leaves M6-T01 blocked with exact remaining work, original coverage and unknown slots. A terminal feasibility failure leaves the relevant M5 gate blocked. Mark the milestone **limited/blocked**, even if the limited report/release tasks finish. Only a complete frozen schedule and passed release checks establish a completed empirical study.

## Task-system review

The pre-implementation review checked plan/specification coverage, coherent outcome boundaries, direct blockers, fallback/limited-report paths, authorization gates and local links. No task was marked implemented, verified, pilot-tested or empirically executed at creation. Current verified progress appears above. Future milestone gate evidence belongs in the named task and existing plan, with detailed execution artifacts in the canonical run bundle.

