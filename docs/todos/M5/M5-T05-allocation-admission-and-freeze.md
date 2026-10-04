# M5-T05 — Complete-schedule admission and immutable freeze

**Status:** blocked

**Dependencies:** [M5-T04](../M5/M5-T04-complete-pilot-and-timing.md). M1–M4 must have passed.

## References

- [Repository contract](../../../AGENTS.md) and [plan freeze/admission](../../IMPLEMENTATION_PLAN.md#freeze-and-admission-to-main-execution).
- Specification [§6 analysis rules](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§7.3–7.4 rules/cases](../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), [§8.3–8.4](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).

## Intended outcome

One accepted model/environment/size and one complete permitted schedule are frozen before any main outcome is inspected, with a fully evidenced admission decision.

## Scope and boundaries

- Forecast the entire main schedule using measured phase/condition/prompt costs, slower-device speed and allocated idle/overhead, with a 25% margin on main cost and the full twelve-hour reserve against the initial 100 aggregate GPU-hour ceiling.
- Do not double-count setup within per-call costs and reserve attribution; show actual spending separately from reserves and provider billing. Two devices reduce elapsed time, not aggregate device-hours.
- Select complete 60 worlds if it fits, otherwise the nested complete 40. Prefer capable 9B/40 over switching models only for more worlds. No omitted shams, masks, repeats or families.
- If neither fits, keep admission blocked and prepare the concrete scope/resource decision with evidence. A scientific-design or frozen-configuration change needs explicit authorization and renewed affected gates.
- Freeze specification/code identities, passing package/environment lock/system facts, model/tokenizer revisions and exact templates, size/schemas/caps/timeout/decoding, actual worlds/edits/ownership/partitions/subsets/streams, logical/generation/replay schedule, estimands/bootstrap settings, annotation/case/boundary rules, allocation convention/ceiling and pilot/forecast evidence.
- Reuse existing IDs/configuration/version records and canonical run inputs. Resume must reject settings/input mismatches; no new content-addressed identity or duplicate store.
- Update the project README's actual install/run/resume/status/analyze/export guidance during implementation. Passing admission is not authorization for main inference.

## Completion criteria

- An admission report links every threshold and M1–M4/host gate to executed evidence, reconciles spent/reserved/forecast resources and selects exactly one complete schedule.
- The immutable bundle supports dry-run execution/resume and contains all reproduction inputs before main outcomes exist.
- Independent freeze checks reject missing parents, inconsistent seeds, changed templates, mixed models, edited inputs/configurations and incomplete selected schedules.
- M5 closes only on a passing accepted freeze. Failed feasibility remains a blocked gate with a limited-evidence handoff; it cannot admit M6-T01.

## Validation and evidence

Run independent dry-run freeze audits against deliberately altered bundles and both schedule totals. Check accepted sizes/contracts/settings, complete environment/template records, no main outcome inspection, all analysis/case rules and provider/storage facts. Record forecast arithmetic, accepted allocation and the exact bundle identity/location for future authorization.

**Evidence:** Not yet recorded. Initial preparation/freezing is not a request to change an existing frozen scientific configuration; any later change follows the repository authorization rule.

