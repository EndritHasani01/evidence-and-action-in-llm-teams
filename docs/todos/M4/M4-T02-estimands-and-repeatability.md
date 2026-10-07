# M4-T02 — All prespecified contrasts and repeatability

**Status:** done

**Dependencies:** [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md). M1–M3 must have passed.
M1–M3 and M4-T01 have passed on CPU; their retained gate/evaluation evidence
was inspected and reproduced before this task's completion.

## References

- [Repository contract](../../../AGENTS.md) and [plan exact outcomes/contrasts](../../IMPLEMENTATION_PLAN.md#exact-outcomes-and-contrasts).
- Specification [§5.2 θ](../../../PROJECT_SPECIFICATION.md#52-primary-1-correction-specific-reset-value), [§5.3 φ](../../../PROJECT_SPECIFICATION.md#53-primary-2-effects-on-retained-collaborators), [§5.4 secondary estimates](../../../PROJECT_SPECIFICATION.md#54-secondary-estimates), and [§6 repeatability](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness).

## Intended outcome

Every prespecified estimate has an explicit formula, population and endpoint, with world/family contrasts and separately identified conditional repeats.

## Scope and boundaries

- Implement θ and its direct revised/sham C−B components with equal five-family weighting.
- Implement φ as revised E_keep over the same focal peers in rounds 2–4. Include sham E_keep, φ_corr, both E_clear effects, complementary own-group reset contrasts, four-mask trajectories and average mixed-policy performance. Round one remains a construction reference.
- Include revised C−B, K−C, K−B, B−L and C−F AUC/final-joint effects; compact-state sham effects and revision-minus-sham interactions.
- On Prefix/Sort implement round-one receipt η, all six cell means, three direct receipt effects, B-versus-C/B-versus-K under both formats, and AUC/final/preservation companions.
- On Sort/BFS implement Q_B−B and Q_C−C round-two effects separately under revision/sham, with subsequent trajectories/AUC and preservation; retain inactive no-prose cases.
- Include preserving B/C/K AUC, joint completion and preservation on its fixed sixteen-world population.
- Keep replicate zero primary. On ten repeated prefixes show per-world θ/φ/compact-state contrasts, ties versus sign reversals and trajectory-category changes; retain original prefix/partition and new continuation seeds.

## Completion criteria

- All §5.4 comparisons and companions exist on the correct eligible populations, with exact formulas and denominator provenance.
- Family balancing and fixed subsets are explicit, including overlapping world identities.
- Repeats never replace replicate zero, become new independent worlds or imply new-prefix, receipt or Q repeatability.
- Each contrast can retain unknown components for the later missingness calculation; complete-case summaries do not silently redefine the estimand.

## Validation and evidence

Use independently hand-calculated θ equal-effect null/positive/negative cases; φ no-influence null and beneficial/harmful cases; φ positive with φ_corr zero for equal event effects; and round-one exclusion. Verify focal-peer matching, own-group/E_clear signs, every secondary contrast/endpoint, equal-family rather than pooled weighting, subset eligibility, replicate separation and ties/sign reversals.

**Evidence:** Started on 6 October 2026 on `feat/m4-offline-analysis` from clean
commit `9a51df7`. The specification, plan, M4-T01 handoff and M1–M3 gate evidence
have been inspected. Analysis will reuse the full scheduled outcome/diagnostic
tables and their original generation/replay/prefix joins. The full M4 gate remains
open; uncertainty and missingness bounds remain M4-T05 work.

The first checkpoint implements [analysis.py](../../../recovery/analysis.py)'s
explicit world components, equal-family summaries and separate conditional
repeats. `python -S -m unittest tests.test_analysis -q` passes 21 formula checks;
`python -S -m unittest tests.test_analysis tests.test_evaluate -q` passes 47 checks
in 7.593 seconds. Exact rational means preserve mathematical ties; each component
retains logical/physical call IDs, rounds, peers, prefix eligibility, coefficients
and unknowns. Saved-run/CLI integration and retained reconstruction remain open
at this checkpoint. The initial fixture read incorrectly assumed a separate
fallback schedule file; tests now derive it from the existing saved fallback
population, without generating worlds or changing any retained fixture.

Saved-worker integration now provides `analyze_run` and `recovery analyze
--estimands`, preserving M4-T01's ordinary outcome export. The new
[retained contrast tables](../../../tests/fixtures/estimand_tables.json.gz)
reconstruct four cases from original accepted M3 workers, including all missing
worlds in both full main manifests. `python -S -m unittest tests.test_analysis
tests.test_analysis_run tests.test_estimand_archive tests.test_evaluate
tests.test_outcome_archive -q` passes 53 checks in 74.566 seconds. Broader CPU,
installed-library and documentation/protected-artifact checks remain open at
this second checkpoint.

### Implementation and scientific semantics

[analysis.py](../../../recovery/analysis.py) uses direct functions and the existing
M4-T01 joins, with standard-library rational arithmetic. The saved population and
schedule define cohorts; original calls/attempts/pre-delivery states define
observations. No identity system, dependency, live intervention or persistence
layer is added. [CLI/API usage](../../../README.md#offline-contrasts-and-conditional-repeats)
and [derived fixture fields](../../../tests/fixtures/README.md#prespecified-estimates-and-conditional-repeatability)
describe reproduction.

- θ is revised C−B AUC minus sham C−B AUC, with both direct components reported.
  φ is `E_keep(revision)` over the same two retained peers in each complementary
  group in rounds 2–4. Sham E_keep, φ_corr, E_clear for both events, group cell
  means, four-mask trajectories and average P_G/P_H performance remain explicit.
  Round one is a construction reference, excluded from φ.
- Own-group reset with the other group retained is
  `½[(M_G^10−M_G^00)+(M_H^01−M_H^00)]`; with the other group cleared it is
  `½[(M_G^11−M_G^01)+(M_H^11−M_H^10)]`. These preserve the same focal peers and
  the reset-minus-retain sign. Their per-round trajectories remain visible.
- Revised C−B/K−C/K−B/B−L/C−F include AUC, final joint completion and preservation.
  Compact-state sham and revision-minus-sham companions retain their explicit
  event components and endpoint ranges. Missing/invalid replies never inherit
  earlier answers.
- Prefix/Sort receipt tables expose all six first-response cells, η, three
  direct receipt effects, B−C/B−K under both formats and AUC/final/preservation
  companions. Sort/BFS Q tables retain both events separately, round-two effects,
  all subsequent trajectories/AUC/final/preservation and the first-round reference.
  Observed/inactive/unknown held-prose counts never change inclusion.
- Preserving B/C/K cells and contrasts use only the first eight Top-K and first
  eight BFS worlds, at both main counts. The actual populations are five-family
  main, two-family receipts/Q/preserving and ten fixed repeats. Overlapping Sort
  and BFS identities never become additional independent worlds.
- Accuracy summaries use equal family means, with fixed world denominators.
  Preservation averages eligible peers, then rounds/worlds, then eligible
  families. `preservation` with no round is the four-round mean; round four is
  final preservation. Empty eligibility is N/A; unknown prefix eligibility and
  unexecuted outcomes remain unknown. Every diagnostic publishes coordinate,
  peer-copy and call/prefix denominator provenance.
- Each world contrast retains a formula, endpoint, range, exact numerator and
  denominator, coefficients and the original scheduled/generation/replay/prefix
  IDs. Linear atoms retain exact weights; final joint completion keeps its
  all-four operator. Intended population estimates stay unknown when eligible
  components are unknown. Complete-case descriptions have separate world/family
  denominators and never redefine the estimand. M4-T05 will calculate bounds.
- Replicate-zero estimates and repeated contrasts are separate tables. Repeats
  retain their original prefixes/partitions and new continuation seeds. Zero
  contrasts are ties, not sign reversals; only strict opposite signs reverse.
  Trajectory changes derive from the same joined outcomes as the contrasts,
  with incomplete pairs unknown. No repeat replaces replicate zero, increases
  independent N, or supplies new-prefix/receipt/Q repeatability.

### Formula-to-fixture checks

[Hand-calculated tests](../../../tests/test_analysis.py) and
[saved-worker/CLI checks](../../../tests/test_analysis_run.py) verify these results.
Values below are deterministic implementation fixtures, not model findings.

| Formula / failure mode | Independent expected result |
|---|---|
| θ: revised C−B = 1/2; sham C−B = 1/2, 0, 1 | θ = 0, +1/2, −1/2 |
| Same retained peers, no teammate effect / beneficial / harmful reset | φ = 0 / +1 / −1 |
| Equal beneficial revision/sham collaborator effects | φ = +1; φ_corr = 0 |
| Retained first-round parents correct; effect +1 only in rounds 2–4 | φ = +1 over six peer-round calls per group; round-one E_keep = 0 |
| G/H cell fixture with cancelling E_keep | E_keep = 0; E_clear = 1/2; own-reset with other retained = −3/4, other cleared = −1/4 |
| Revised C−B, K−C, K−B, B−L, C−F AUC | +1/4, +1/4, +1/2, +1/4, −1/2; final C−F = −1 |
| Sham K−C/K−B and revision-minus-sham | Sham −1/4, −1/2; interactions +1/2, +1 |
| Receipt first-round B/C/K = 1/4,1/2,3/4; BΔ/CΔ/KΔ = 1/2,1/4,1 | η = 1/2; direct effects +1/4,−1/4,+1/4; B−C/B−K after-only −1/4,−1/2, disclosed +1/4,−1/2 |
| Same receipt fixture, with eligible unchanged outputs only in peers 0–2 | Preservation η = 1/3; KΔ−K preservation = 0 despite its +1/4 exact-accuracy effect |
| Equal large receipt benefits for C and K | Both direct effects +1/2; η = 0 |
| Q_B−B / Q_C−C at round two, revision then sham | Revision +1/2,−1/2; sham −1/4,+1/2; first-round effects 0; constant later effects give AUC = 3/4 of round-two effect |
| Unequal family sizes: three +1 worlds in one family, zero in four one-world families | Equal-family θ = 1/5, rather than pooled 3/7 |
| Eligible peer preservation 9/10 and 0/1 across four rounds | Mean = 9/20; 10 unique coordinates, 11 peer copies; unknown prefix eligibility remains unknown |
| Unknown θ component, nine complete worlds out of ten | Intended estimate unknown; separately labeled complete-case value 1 with its nine-world denominator |
| Fixed target/fallback subsets and overlaps | Main 60/40; receipts/Q 24/16 each; preserving 16/16; repeats 10/10; Sort overlap 12/8 |
| Repeat zero/zero, zero/nonzero, nonzero/zero, opposite nonzero signs | Both ties, zero-replicate tie, repeat tie, strict sign reversal; replicate-zero tables unchanged |
| Original B continuously correct, repeat temporarily correct | Category change true; an incomplete repeated branch makes the change unknown |
| Empty/inactive/unobserved Q prose, before/after release | Literal empty text counts zero exposure; inactive and unknown branches remain included; wrong release boundary fails |
| Worker, schedule or derived-table drift | Duplicate/missing outcomes, wrong seeds/prefix/scope, duplicate/missing diagnostics and wrong Q release fail; original workers/exports remain protected |

### Retained ordinary-worker reconstruction

[estimand_archive.py](../../../tests/estimand_archive.py) reconstructs all four
[retained cases](../../../tests/fixtures/estimand_tables.json.gz) directly from
the original M3 manifests and accepted worker files in
[scripted_lifecycle_run.zip](../../../tests/fixtures/scripted_lifecycle_run.zip).
It imports no runner, checkpointer, tokenizer or inference provider. Backups and
baselines are never combined with their original physical workers.

| Case | Scheduled / recorded / unknown slots | Intended θ / φ | Complete worlds for primaries |
|---|---|---|---:|
| Five-family complete fixture, each size | 2,170 / 2,170 / 0 | 0 / 0 | 5 |
| Full target-60 main manifest | 17,656 / 2,170 / 15,486 | unknown / unknown | 5 of 60 |
| Full fallback-40 main manifest | 12,560 / 2,170 / 10,390 | unknown / unknown | 5 of 40 |

The full main primary family denominators remain 12 / 8, never one complete
world per family. Complete-case values of zero are labeled as descriptions.
Q activity is observed in eight branches per size; full joins retain another
88 / 56 unknown Q branches. Fixed repeat displays retain all ten worlds and
100 event/policy trajectory pairs, including incomplete pairs. The complete
fixtures supply five repeated worlds with 50 pairs each; neither is a completed
main experiment or a repeatability finding about model behavior.

### Reproduction and executed checks

```powershell
python -S -m unittest tests.test_analysis tests.test_analysis_run tests.test_estimand_archive tests.test_evaluate tests.test_outcome_archive -q
python -S -m recovery validate --core-only
$env:PYTHONHASHSEED = '37'
python -S -m tests.estimand_archive
.venv/Scripts/python.exe -m recovery validate
.venv/Scripts/python.exe -m pip install --no-deps .
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe -m compileall -q recovery tests
```

| Executed check | Result |
|---|---|
| Focused analysis/integration/archive plus M4-T01 regressions | 53 passed in 74.566 seconds |
| Dependency-free core, site packages disabled | 134 passed in 160.793 seconds |
| Complete CPU regression, including external process kills | 306 passed in 1,658.876 seconds; all nine lifecycle checks pass |
| Installed-library validation outside checkout | 54 passed in 93.305 seconds; ten actual module paths/bytes asserted, plus the installed CLI outside the checkout |
| Fresh retained-table reproduction under hash seed 37 | All four cases and every table match |
| Ordinary isolated package build/install, `pip check`, compilation | Passed; no dependency change |
| Local links/anchors, 29 task/index statuses, protected artifacts, whitespace | 319 links/anchors across ten documents, all 29 task/index statuses and both plan/index milestone counts pass; protected/prior-artifact diffs and `git diff --check` pass |

Final focused analysis checks additionally verify every direct preservation
companion, receipt preservation's distinct eligible-peer population, nonzero
preserving endpoints, stale trajectory exports and wrong prefix/family/diagnostic
joins. These review additions pass all 21 checks in 3.066 seconds after the
broader regressions started; production code and retained tables are unchanged.

Windows build 26200, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5, LangGraph
1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6 are the CPU acceptance environment.
This tested CPU package environment is not an accepted M5 freeze. Concurrent
validation durations are not model or GPU timings.
The final documentation audit verifies the completed sixteen-done/two-ready/
eleven-blocked handoff and all milestone counts. Its temporary reproducible
helper is `$env:TEMP/m4-t02-documentation-audit.py`; final source/core/installed
logs and the installed module/CLI harness use the same `m4-t02-` prefix.
Temporary logs use `$env:TEMP/m4-t02-*`; the retained tables and executed
reconstruction supply durable evidence. Remaining M4 tasks own information/work
diagnostics, costs, uncertainty/missingness and the complete analysis/report gate.
M5 hardware/capability/timing and empirical execution remain later work.

### Completion and handoff

M4-T02 is implemented and verified on CPU on 6 October 2026. Checkpoint `7aed746`
implements the formula/denominator/repeat core; `07b4602` adds ordinary-worker/CLI
integration and retained reconstruction. The final evidence commit records the
complete CPU gate, focused review additions and updated handoff.

Progress is sixteen done, two ready and eleven blocked. M4-T03/T04 remain ready;
M4-T05 still requires T04, and M4-T06's complete analysis/report gate remains
open before GPU use. T05 can consume exact components/weights, fixed populations,
endpoint ranges and original shared-response IDs; complete-case tables are
descriptions, not substitute estimands. All scientific/configuration/dependency
files and earlier fixtures remain unchanged. No GPU/model inference, pilot,
main experiment, scientific/frozen-configuration change or publication occurred.

