# M4-T04 — Policy costs and the frozen boundary rule

**Status:** ready

**Dependencies:** [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md). M1–M3 must have passed.

## References

- [Repository contract](../../../AGENTS.md) and [plan explanatory outcomes/costs](../../IMPLEMENTATION_PLAN.md#explanatory-outcomes-and-costs).
- Specification [§7.3](../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), [§8.3](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).

## Intended outcome

Offline analysis produces auditable physical and hypothetical policy-cost tables and evaluates the single prespecified source-coverage boundary rule.

## Scope and boundaries

- Consume the existing M3 ledger and overhead convention; add no duplicate cost store.
- Reconcile physical generations/attempts/allocation once versus each policy's prefix plus all sixteen logical continuation calls. Replay receives original measured generation cost; F includes its abandoned prefix.
- Include tokens, validated source/text deliveries, durations, peak memory, allocated idle/setup/interruption overhead, failures and ambiguous work. Keep billing separate.
- Select the complete C branch iff every peer initially holds the complete current source manifest; otherwise select the complete K branch. Include tombstones and exclude pending updates. Use no gold, candidate correctness or later acquired evidence.
- Evaluate the selected whole branch and its whole policy cost against always B/C/K. Report selection counts/frequencies and explicitly describe a constant rule.
- Keep retained evidence, preserved correct output and measured computation in separate views. Prepare paired quality/preservation versus policy-cost data for later uncertainty and plotting.
- Any cost to oracle-recognized stable completion is retrospective under the fixed schedule, not actual saved runtime. Do not tune the rule, splice branches or invent an accuracy-per-message/utility ratio.

## Completion criteria

- Policy and physical totals reproduce the M3 ledgers without making shared/mixed/Q policies artificially cheap.
- Rule selection depends only on recorded initial current-source coverage and always identifies one entire observed branch.
- Missing complete branches produce explicit unavailable/unknown results for subsequent bounds; no favorable fallback selection.
- Outputs preserve paired world identities for uncertainty, selected-branch provenance and all denominators.

## Validation and evidence

Hand-calculate costs with shared prefixes, replay, F, failed/retried generations and idle overhead. Change gold/candidate correctness while holding boundary coverage fixed and assert unchanged selection. Check all-covered/tombstone, missing/pending, mixed coverage, constant-rule and unavailable-branch fixtures. Reconcile selected costs with the same complete C/K branch's costs.

**Evidence:** Not yet recorded. Add cost reconciliation and boundary-rule fixture results before marking done.

