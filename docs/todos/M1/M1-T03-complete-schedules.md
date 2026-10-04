# M1-T03 — Complete schedules and replay dependencies

**Status:** active

**Dependencies:** [M1-T02](../M1/M1-T02-edits-and-populations.md).

## References

- [Repository contract](../../../AGENTS.md), [plan M1](../../IMPLEMENTATION_PLAN.md#3-milestone-m1--reproducible-worlds-truth-and-schedules), and [roadmap gates](../../IMPLEMENTATION_PLAN.md#1-execution-roadmap).
- Specification [§2.3](../../../PROJECT_SPECIFICATION.md#23-events-and-populations), [§4](../../../PROJECT_SPECIFICATION.md#4-recovery-interventions-and-their-controls), and [§8.1–8.3](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls).
- Technical evidence: [analysis/allocation checks](../../implementation-research/repository-and-validation.md#analysis-and-allocation-defaults-that-would-change-the-result).

## Intended outcome

CPU preparation enumerates every main and development logical opportunity, distinct generation and required replay parent before execution.

## Scope and boundaries

- Encode the declared matrix directly: revised L/B/C/K/F and both masks; sham B/C/K and both masks; revised receipts on Prefix/Sort; revised/sham Q on Sort/BFS; preserving B/C/K on sixteen fixed worlds; and the ten-world extra B/C/K/mask replicate under both events.
- Include one natural four-round prefix per world and two one-call complete-world before/after controls with empty sends. Keep four peers active through all rounds regardless of correctness.
- Mixed/Q first rounds point to their corresponding B/C parents within the same event/replicate. Prefix and response sharing must be explicit; matching seeds or prompts alone creates no extra reuse.
- Pilot masks run only on Prefix/BFS. Preserve its exact component populations instead of copying the entire main matrix onto development worlds. Make the first 90 prefix/control slots selectable as the capability block; smoke is separate.
- Provide a usable CPU prepare/validate handoff. Do not build execution workers, freeze an accepted main configuration, or add unprescribed crossings.

## Completion criteria

- Independent enumeration reconciles main distinct/logical totals: 16,152/17,656 for 60 worlds and 11,504/12,560 for 40.
- Development components reconcile 730+96+96+96+96=1,114 distinct slots; the first 90 comprise 80 prefix and ten control calls. Smoke has at most 24 additional calls, for at most 1,138 combined.
- Every slot has the scientific grouping/phase/peer/round identity needed for evaluation and a distinct-generation or replay-parent relation. Extra repeats use new physical IDs/seeds, with the original prefix and partition.
- Both complete schedules and replay dependency orders validate without model calls. No early-correctness optimization changes opportunities.
- M1 closes only when M1-T01–T03 acceptance evidence passes and the plan's living progress section links that evidence.

## Validation and evidence

Use an independently calculated component table, not a second invocation of the schedule builder. Assert subset membership/counts, output contracts for controls, parent existence/event/replicate scope, acyclicity, slot uniqueness, all four opportunities per peer/phase, and unchanged schedules after a simulated poor prefix. Check saved/reloaded schedules and manifest mutation rejection. Retain a prepared CPU fixture usable by M2; M1 passing does not establish protocol or resource feasibility.

**Evidence (start, 4 October 2026):** The specification, plan M1, allocation
investigation and M1-T01/T02 acceptance artifacts have been inspected. The
existing `python -S -m recovery validate` suite passes all 42 checks on Windows /
CPython 3.11.9. Implement explicit logical calls, prefix/reply parents and CPU
dependency orders first; then saved schedule validation and the prepare handoff.
Independent tests will enumerate the matrix and pilot components without calling
the production builder a second time. No inference or accepted M5 freeze is part
of this task.

