# M4-T04 — Policy costs and the frozen boundary rule

**Status:** done

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

Inventory review demonstrated that the host-injected v2 record was counted
among retained remote records. The view now uses M4-T03's exclusion convention,
while separate rule coverage still requires the edited current record. The
new regression verifies both distinctions and unchanged whole-policy selection.
All 28 final dependency-free focused checks pass in 10.121 seconds; all sixteen
updated cost cases reconcile with M3 again. This changes a derived inventory
view, not attempts, costs, quality, branch selection or scientific design.

### Implementation and scientific semantics

[costs.py](../../../recovery/costs.py) supplies the shared M3 arithmetic and
offline cost/rule analysis. [evaluate.py](../../../recovery/evaluate.py) reads
allocation/process records in the same read-only snapshots as calls, attempts,
inputs and committed checkpoints. [CLI/API usage](../../../README.md#offline-policy-costs-and-the-boundary-rule)
supports `recovery analyze --costs`, including combined diagnostics/estimands and
an explicit zoned `--as-of` clock. Export paths are exclusive. The clock bounds
open/ambiguous work; it does not filter persisted records to an earlier run.

- Physical original generations and all attempts are counted once. A policy
  includes its original sixteen-call prefix plus all sixteen continuation calls.
  F's prefix is charged; mixed/Q replay uses original measured tokens/durations,
  including retries. Completing early never removes scheduled calls.
- M3's allocation partition and overhead convention remain unchanged. Loading,
  transport and termination inside attempts are already included. Outside
  allocation overhead remains experiment overhead; the wall-clock partition
  is never added to attempt costs or assigned again to each policy. Billing is
  separate. Actual allocation/memory gaps remain unavailable, including the
  complete fixtures' absent GPU allocation evidence.
- Original measured `seconds`/token fields reconcile with M3. A missing logical
  use, including an unrecorded replay whose parent exists, makes
  `complete_policy_seconds` unavailable. Known token subtotals are accompanied
  by missing-output/memory counts and ambiguous-duration ranges. A completed
  original raw reply without its attempt record is rejected instead of priced
  as free work.
- Coverage uses only initial held current ID/version pairs. Known BFS tombstones
  count; pending replacements do not. Recorded ordinary B/C/K starts must agree.
  A pre-call committed boundary can establish coverage; later checkpoints or
  acquisitions cannot. Gold, values, candidates, history, later evidence and
  cost/quality rankings never determine selection.
- Selected and always-B/C/K views refer to one entire branch and its full
  prefix-plus-continuation cost. Unknown boundaries, unscheduled branches and
  incomplete selected branches remain explicitly unavailable. Selection
  frequencies retain all scheduled worlds and report constancy by family and
  pooled event/replicate populations.
- Retained evidence, preserved correct output and measured computation are
  separate tables. Retained remote evidence excludes the host-injected edited
  record; rule completeness includes it. Paired world/branch/prefix IDs,
  sixteen continuation call/generation IDs, full policy IDs and preservation
  denominators are retained for T05/T06. Shared generation coefficients cancel
  before duration differences. No accuracy-per-message or utility ratio is added.
- Oracle-recognized stable-completion cost is a retrospective prefix plus
  through-that-round subtotal on a complete observed trajectory. It never
  supplies saved-runtime claims, best-answer splicing, an invented fifth round,
  successful-only averages or an execution stop.

### Hand-checked fixtures and original-worker reconciliation

[Focused checks](../../../tests/test_costs.py) use independent hand expectations;
[saved-worker/CLI checks](../../../tests/test_costs_run.py) verify read-only bytes,
exclusive JSON/gzip exports, absent workers, resource snapshots and blocked
runtime/model imports. The public committed serializer is tested in the declared
CPU environment. The source/model inference stack is never invoked by analysis.

The [assigned-cost fixture](../../../tests/cost_fixture.py) contains 128 logical
calls, 116 original generations, twelve replay uses and 117 attempts. One B
first-round generation used by P_G/Q_B has a three-second interruption/retry;
every other attempt costs two seconds. One C slot is a recorded timeout.

| Quantity | Hand expectation |
|---|---:|
| Physical attempt time | 235 seconds |
| B / P_G / Q_B, each including prefix | 67 seconds |
| C / K / F / Q_C, each including prefix | 64 seconds |
| Original shared prefix | 16 calls, 32 seconds |
| Known physical request/output tokens | 234 / 115 |
| Unknown physical output attempts | 2 |
| Separate synthetic allocated time | 400 seconds |
| Allocation setup/interruption/attempt/idle | 1 / 3 / 231 / 165 seconds |

An unknown interruption duration with one observed second and a three-second
recovery bound gives [233,235] physical seconds and [65,67] policy seconds for
B/P_G/Q_B. A shared ambiguous prefix cancels in selected-minus-comparator costs.
K's oracle-stable round-one subtotal is 40 seconds, while its full fixed-schedule
policy still costs 64 seconds. These assigned CPU costs are arithmetic fixtures,
not GPU or model timing.

Coverage fixtures verify all-covered/tombstone C, missing/pending/stale/mixed K,
constant and nonconstant rules, unknown boundaries, unavailable C and K,
unavailable prefix costs, and unchanged choice after gold/candidate/history
changes. Retained-remote exclusion does not alter full-current-manifest selection.
The same selected C/K branch supplies all endpoints/costs and all denominators.

[cost_archive.py](../../../tests/cost_archive.py) reconstructs all sixteen
[retained cases](../../../tests/fixtures/README.md#policy-costs-and-frozen-boundary-rule)
from the existing M3 ordinary workers. Its
[archive check](../../../tests/test_cost_archive.py) compares every table.
M3 status remains bound to its exact execution subset. Full offline manifests
add unknown worlds while preserving physical work and every known policy cost;
no binding or manifest is changed for reconciliation.

| Retained scope | Scheduled outcomes | Recorded | Unknown | Physical attempts | Rule choices |
|---|---:|---:|---:|---:|---|
| Complete five-family fixture, each size | 2,170 | 2,170 | 0 | 1,978 | 22 K, constant |
| Full target-60 manifest | 17,656 | 2,170 | 15,486 | 1,978 | 22 K, 134 unknown |
| Full fallback-40 manifest | 12,560 | 2,170 | 10,390 | 1,978 | 22 K, 94 unknown |
| Stopped prefix | 16 | 0 | 16 | 1 uncertain | No scheduled B/C/K choice |

Each complete size has 192 exact replay uses. The thirteen original-worker
selections additionally cover real precommit kills, exhausted retries, durable
invalid/timeout outcomes, branch-local Q release, and stopped/resumed allocation.
M3's original nine-case accounting export reproduces unchanged. Existing
fixtures, specification, configuration, dependencies and prerequisite task files
are preserved.

### Reproduction and executed checks

```powershell
python -S -m unittest tests.test_costs tests.test_costs_run -q
python -S -m recovery validate --core-only
.venv/Scripts/python.exe -m unittest tests.test_cost_archive -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.cost_archive
.venv/Scripts/python.exe -m tests.accounting_archive
.venv/Scripts/python.exe -m recovery validate
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe -m compileall -q recovery tests
```

| Executed check | Result |
|---|---|
| Final dependency-free cost/CLI suite | 28 passed in 10.121 seconds |
| Final core suite after inventory review | 191 run: 188 passed, three optional dependency skips; 195.100 seconds |
| Installed-library M4 suite outside checkout | 110 passed in 232.989 seconds; eight installed module paths/bytes match source |
| Installed CLI outside checkout | Combined costs/diagnostics/estimands preserve all 1,178 unknown development slots; no worker created |
| Complete CPU source regression at `fe8602a` | 362 passed in 1,772.907 seconds, including all nine lifecycle checks; subsequent inventory-only review is covered by final focused/core/installed/archive checks above |
| Final hash-seed-37 reconstruction | All sixteen cases and every table match the updated retained export; M3 physical/policy/overhead/delivery reconciliation passes |
| Unchanged M3 accounting archive | All 23 checks pass in 78.636 seconds; all nine retained evidence cases reproduce |
| Ordinary non-editable isolated wheel build/install, `pip check`, compilation | Passed; dependencies unchanged |

Windows build 26200, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5, LangGraph
1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. This is CPU
verification, not the accepted M5 freeze. Temporary command logs/harnesses use
`$env:TEMP/m4-t04-*`; the retained export and reconstruction are durable evidence.
The documentation/status/protected-file audit passes all 426 relative links and
anchors across fourteen documents, all 29 task/index statuses and six milestone
counts. `git diff --check` passes. All earlier raw evidence and derived fixtures remain
unchanged.

### Completion and handoff

M4-T04 is implemented and verified on CPU. Checkpoints `f809a89`, `83a138b`,
`fe8602a` and `a127b9e` separately commit prerequisite preparation, shared
arithmetic/frozen choice, saved-run exports/retained evidence and inventory
review. The final evidence commit closes this task. Progress is eighteen done,
one ready and ten blocked. [M4-T05](M4-T05-uncertainty-and-missingness.md) is ready
to consume paired whole-policy endpoints/costs, original response identities,
selection/coverage denominators and explicit unknowns. M4-T05/T06 and the complete
M4 report gate remain open before GPU use.

No GPU allocation, model inference, pilot, main experiment, scientific/frozen
configuration change, important-artifact deletion or publication occurred.

