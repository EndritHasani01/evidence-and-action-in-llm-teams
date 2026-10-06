# M4-T04 — Policy costs and the frozen boundary rule

**Status:** active

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

**Evidence:** Started 6 October 2026 on clean `feat/m4-offline-analysis`
checkpoint `cf363fe`. M1–M3 and M4-T01's saved outcome/attempt/prefix joins
are verified prerequisites; M4-T02/T03 additionally supply paired endpoints and
information diagnostics. The unchanged M3 accounting baseline passes all 23
checks in 79.003 seconds in the declared CPU environment.

Implementation will reuse M3's ledger arithmetic and overhead partition in
offline read snapshots. Initial B/C/K source/version coverage determines one
whole C/K branch; unobserved boundaries or incomplete selected branches remain
unknown. Focused hand calculations, boundary/correctness independence checks,
original-worker reconciliation and complete CPU regression are required before
completion. Uncertainty/reporting, GPU/model admission and empirical execution
remain later gates.

Checkpoint `83a138b` shares M3's original ledger arithmetic and implements the
coverage-only choice. Ten new dependency-free checks pass; all 23 existing M3
accounting checks pass again in 77.906 seconds. The complete offline join now
adds whole-policy costs, selected/comparator endpoints, retained-evidence views,
explicit measurement gaps and `recovery analyze --costs`. The latest focused
dependency-free suite passes 27 checks in 9.243 seconds. All sixteen
[derived cost cases](../../../tests/fixtures/policy_cost_tables.json.gz) reconstruct
from original M3 workers and reconcile with its physical/policy totals,
allocation partition and exact committed delivery IDs. Full manifests add
unknown outcomes without changing physical work or known policy costs.
Complete CPU regression, installed-library verification and final consistency
audits are in progress; this task remains active until they pass.

