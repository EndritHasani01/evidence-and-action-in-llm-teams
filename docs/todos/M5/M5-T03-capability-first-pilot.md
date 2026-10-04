# M5-T03 — Capability-first 90-slot pilot gate

**Status:** blocked

**Dependencies:** [M5-T02](../M5/M5-T02-hardware-smoke-and-host-validation.md). M1–M4 must have passed. Explicit authorization covering the GPU/paid-compute scope is also required.

## References

- [Repository contract/authorization](../../../AGENTS.md) and [plan bounded pilot](../../IMPLEMENTATION_PLAN.md#bounded-smoke-and-capability-pilot).
- Specification [§8.1 controls](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.2 thresholds/fallback](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), and [§8.4 resources](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze).

## Intended outcome

The accepted smoke candidate establishes the prescribed arithmetic/collaboration capability before any recovery-pilot generations are admitted.

## Scope and boundaries

- Require current authorization covering these development calls and the passed smoke/host gate.
- Execute exactly five disjoint development prefixes, four peers × four rounds = 80 slots, plus ten before/after full-information controls.
- Controls use the same outer reply schema, task hint, decoding and caps, with empty sends and complete-world outputs; Prefix/Sort return all n coordinates. They are capability diagnostics, not policy competitors.
- Run every prefix round regardless of early success. Invalid replies, timeouts and failures consume their scheduled slots; do not select a better prefix or resample formatting.
- Recovery spending is blocked until the capability thresholds pass.
- If arithmetic/context capability requires it, use only the single uniform m=6/eight-node-twelve-edge fallback, retaining top ten, ranges, four peers/rounds and five added graph edges. Renew all affected generators/oracles/contracts/rendering/witness/capability checks; no family-specific shrinkage or omission.
- All failed configurations, attempts and justified reruns share the eight-hour development allocation within the 100-hour total, plus the stated setup/interruption reserves. Model/hint/phrasing selection cannot use favorable recovery effects.

## Completion criteria

- At least 9/10 full-information controls are exactly correct, with at least one in each family.
- At least three of five prefixes are jointly correct at their final round and at least 14/20 final prefix-peer candidates are correct.
- All 90 distinct slots, failures, family results and physical costs are recorded for one internally consistent candidate configuration.
- A change in model/tokenizer/template/lock/backend/timeout/size invalidates affected prior gate evidence until renewed; incompatible configurations are not pooled.
- If thresholds cannot pass within resources, keep the gate blocked, retain feasibility evidence and proceed only to diagnosis/limited reporting.

## Validation and evidence

Produce a row-linked capability table showing all ten controls and twenty final prefix-peer outcomes, plus joint-prefix counts, exact settings, world/seed disjointness and total slot/attempt/allocation reconciliation. Verify the scheduler refused recovery before the gate and that every permitted fallback reran affected CPU/hardware checks.

**Evidence:** Not yet recorded. Passing these small screens would establish operational capability, not a treatment effect.

