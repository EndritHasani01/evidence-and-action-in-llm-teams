# M5-T04 — Complete development pilot and measured timing

**Status:** blocked

**Dependencies:** [M5-T03](../M5/M5-T03-capability-first-pilot.md). M1–M4 must have passed. Explicit authorization covering the GPU/paid-compute scope is also required.

## References

- [Repository contract/authorization](../../../AGENTS.md) and [plan bounded pilot/forecast](../../IMPLEMENTATION_PLAN.md#bounded-smoke-and-capability-pilot).
- Specification [§8.2 pilot matrix](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), [§8.3 schedules](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule), and [§8.4 resource gate](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze).

## Intended outcome

The single candidate completes the exact development pilot, passes protocol validity and host checks, and supplies measured inputs for a conservative whole-study forecast.

## Scope and boundaries

- Require current authorization and the passed 90-slot capability gate. Resume those exact prefixes/controls; they are part of the 1,114 total, not a second pilot.
- Complete 730 base slots for prefixes, revised L/B/C/K/F, sham B/C/K and controls; 96 masks on Prefix/BFS under both events; 96 revised receipt slots on Prefix/Sort; 96 Q slots on Sort/BFS under both events; and 96 preserving slots on Top-K/BFS.
- Reuse required mixed/Q first-round replies. Replays and retries cannot inflate the distinct scheduled-generation validity denominator.
- Inspect failures by family/condition and unresolved source/isolation/queue defects. The pilot exercises the specified matrix rather than every main combination.
- Measure phase/condition/prompt-dependent time, slower-device behavior, loading, allocated idle time, setup/interruptions and memory. Test 120-second timeout adequacy before freezing it; changing it requires renewed affected checks.
- Keep actual spending separate from reserved amounts. Development inference is shared across failed configurations/attempts/reruns, with eight development hours, two setup hours and two interruption/rerun hours inside the total ceiling.
- No prompt/model/size selection based on recovery effects, incompatible-configuration pooling, or pilot effect presented as empirical main evidence.

## Completion criteria

- Exactly 1,114 distinct pilot slots for the accepted configuration are accounted for, including the first 90; separate smoke stays within its <=24/0.5-hour allowance.
- At least 98% of distinct scheduled pilot generations are protocol-valid; capability thresholds still pass, capacity/headroom/finite-output checks pass, and no unresolved isolation/leakage/queue defect remains.
- Cost rows support a conservative full 60/40 schedule forecast including the slower device and non-call overhead; short successful calls alone are insufficient.
- If no configuration passes within development resources, keep this gate blocked and record the complete feasibility limitation for limited reporting.

## Validation and evidence

Link all thresholds to actual pilot rows; reconcile component counts, replay parents, attempts and allocation. Preserve family/condition validity tables, long-prompt/memory evidence, timeout measurements and a measured timing summary with overhead attribution. Re-run only checks affected by concrete configuration changes or failures.

**Evidence:** Not yet recorded. Pilot outcomes are development evidence and must remain separate from main estimates.

