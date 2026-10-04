# M1-T02 — Eligible edits and reproducible populations

**Status:** done

**Dependencies:** [M1-T01](../M1/M1-T01-task-worlds-and-truth.md).

## References

- [Repository contract](../../../AGENTS.md) and [plan M1](../../IMPLEMENTATION_PLAN.md#3-milestone-m1--reproducible-worlds-truth-and-schedules).
- Specification [§2.2–2.3](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§8.2](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [generation risks](../../implementation-research/repository-and-validation.md#task-generation-contains-the-meaningful-hidden-risks).

## Intended outcome

Serializable populations contain actual worlds, edits, partitions, eligibility/rejection records and all preassigned random streams, independently of model outcomes.

## Scope and boundaries

- Randomize owner order in blocks of four before conditioning generation. Preserve three main edits per owner in 12 worlds/family and two in the nested first eight.
- Prefix/Difference/Sort select an owner-held position uniformly, then a different in-range replacement uniformly. Main Top-K selects an eligible record uniformly, then a legal lower value; preserving Top-K samples uniformly over legal record/replacement pairs. BFS samples eligible owner-held changing edges; preserving deletions have no owner-matching constraint.
- Require both changing and preserving eligibility in every Top-K/BFS world. Limit generation to 1,000 attempts/world, record rejections, and fail explicitly on exhaustion. Never regenerate based on a prefix or other model result.
- Prepare 60 worlds and the nested 40, five disjoint development worlds, receipt and Q subsets, first-eight Top-K/BFS preserving subsets, and first-two-per-family repeat subsets. Draw a uniform unordered two-pair partition per world; G contains peer 0. Retain it across events/repeats.
- Save separate generation/edit/partition/prefix/continuation streams and actual inputs/edits. Continuation seeds match across policies/events for a given world/replicate/round/peer. Extra repeats have new continuation seeds, while retaining the prefix. Scheduling and process hashing must not determine seeds.
- Main, sham and preserving events refer to the original world; there is only one live edit per episode. These are prepared manifests, not the accepted M5 freeze.

## Completion criteria

- Mathematical eligibility, edit distributions, owner balance and all fixed subsets are explicit and testable for both sizes.
- Persisted manifests can be reloaded without resampling or changing worlds, IDs, ownership, partitions or streams.
- Changed serialized inputs are detected through comparison with the saved authoritative manifest using existing IDs/configuration; no separate identity registry or custom checksum system is introduced.
- Evaluator gold/footprints stay separate from public manifests and future peer views.

## Validation and evidence

Test exact legal sets and deterministic selection boundaries rather than a flaky frequency threshold. Force exhausted rejection. Check development/main disjointness, target/fallback nesting, fixed subset sizes/overlap, all three partition possibilities, owner balance, distinct repeat seeds and sibling seed matching. Reordering preparation or consuming an unrelated stream must not shift other identities. Verify byte-stable regeneration from saved inputs and detection of a modified manifest.

**Evidence (start, 4 October 2026):** M1-T01 is done and its implementation,
23-check CPU evidence, specification sections and generation-risk investigation
have been inspected. Implement legal edit sets first, then immutable population
records and isolated saved streams, then reload/mutation and population checks.
No inference, accepted M5 freeze or scientific-design change is part of this task.

**Edit checkpoint:** `python -S -m unittest tests.test_edits -v` passed five
focused checks on CPython 3.11.9. [edits.py](../../../recovery/edits.py) implements
immutable single-source revisions/shams, exact legal sets and the two sampling
rules; [test_edits.py](../../../tests/test_edits.py) enumerates selection boundaries,
numeric endpoints, unique/duplicate Top-K values, zero cutoffs, and every BFS
deletion against independent relaxation at both sizes. Preserving Top-K requires
the original value strictly below the cutoff; a replacement equal to the cutoff
is legal because it leaves the complete ten-value answer unchanged, including
multiplicity. No record-identity tie-break is part of the answer contract.

**Population checkpoint:** `python -S -m unittest tests.test_populations -v`
passed ten checks on CPython 3.11.9. [populations.py](../../../recovery/populations.py)
prepares 60 main/five development worlds for either mathematical size, nested
40-world views, all fixed subsets, G/H partitions and disjoint integer seed slots.
[manifests.py](../../../recovery/manifests.py) saves actual host inputs and loads
them without resampling; equality with a saved authoritative population detects
even mathematically valid changed inputs. [test_populations.py](../../../tests/test_populations.py)
checks three seed roots/both sizes, all subset counts/owner blocks, reordering,
two process hash seeds, optional-import isolation, exact 1,000-attempt exhaustion
and acceptance on attempt 1,000, rejection reasons, byte-stable regeneration,
and malformed/modified manifests. CLI, retained fixture and final evidence remain.

**Completion evidence (4 October 2026):** Windows x64 / CPython 3.11.9.
The complete suite passed **42/42 checks**, including the prior M1-T01 checks,
with site packages disabled and in the dependency-free editable CPU environment.
No model stack was imported, no inference was run, and no accepted configuration
was frozen. Executed commands:

```powershell
python -S -m unittest tests.test_edits -v
python -S -m unittest tests.test_populations -v
python -S -m recovery prepare --seed 20261004 --output tests/fixtures/population_target.json
python -S -m recovery validate --manifest tests/fixtures/population_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate
.\.venv\Scripts\python.exe -m recovery validate
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The fallback fixture was prepared with `prepare_population(20261004, Size.FALLBACK)`
and `save_population`. A temporary-directory harness additionally invoked the
installed `prepare --config <fallback.toml> --seed 20261004 --output <prepared.json>`
and `validate --config <fallback.toml> --manifest <prepared.json> --authoritative
<population_fallback.json>` commands outside the checkout. Preparation matched
the retained fallback fixture byte for byte; installed validation passed all 42
checks. `pip check` reported no broken requirements. These are CPU environment
checks, not the accepted inference environment.

| Acceptance area | Checks / retained artifacts | Result |
|---|---|---|
| Exact legal sets and selection | `LegalEditTests` in [test_edits.py](../../../tests/test_edits.py) | Both sizes; every numeric owner/replacement boundary, unique/duplicate/zero Top-K cutoffs, preserving cutoff ties, and all BFS edges against independent relaxation pass. Main uses record then value; preserving uses a single uniform pair/edge selection. |
| Eligibility conditioning and bounded rejection | `PopulationTests.test_rejection_reasons_owner_fixed_and_explicit_thousand_attempt_exhaustion`, `test_bfs_rejects_fixed_owner_without_changing_edge`; CLI exhaustion check | Owner is fixed before generation; only mathematical eligibility is rejected. Exactly 1,000 failures raise with every rejection recorded; acceptance on attempt 1,000 succeeds. CLI reports all failures and writes no accepted manifest. |
| Populations, balance and fixed overlap | `test_all_populations_edit_truth_subsets_owner_balance_and_nesting` | 60/40 main worlds: 12/8 per family and 3/2 edits per owner. Five development worlds have disjoint IDs/streams. Receipt/Q are 24/16, preserving 16 at either count, repeats ten. The focal overlap is exactly Sort. Preserving edits can belong to other owners. |
| Partitions and seeds | Partition/owner-order, stream and reordering checks in [test_populations.py](../../../tests/test_populations.py) | All three unordered partitions are selectable uniformly; G contains peer 0. Generation/ownership/edit/partition/prefix/continuation/control streams and owner streams are disjoint; event/policy do not enter continuation keys. Repeat seeds differ while original-world/prefix slots/partition remain fixed. Reordering and unrelated draws cannot shift worlds. |
| Saved authority and reproducibility | [target fixture](../../../tests/fixtures/population_target.json), [fallback fixture](../../../tests/fixtures/population_fallback.json), [fixture notes](../../../tests/fixtures/README.md#prepared-host-populations) | Each fixture saves 60 + five actual worlds, edits, eligibility, rejections, partitions and seeds. Each has one recorded Top-K rejection. Three roots at both sizes round-trip and regenerate byte-stably; reload forbids generation. Both process hash seeds match. Existing files cannot be overwritten. |
| Input mutation and evaluator separation | Authoritative-comparison, structural-mutation and retained-fixture checks | A mathematically valid altered Prefix input fails comparison with saved authority. Bad configuration/identity/seeds/partitions/edits/rejections, duplicate/extra fields and coercions fail. Gold/footprints/correctness/candidates are absent; public source projections remain ID/owner/position only. Full manifests are host-owned and never peer views. |
| CPU CLI and portability | [test_cpu_entrypoint.py](../../../tests/test_cpu_entrypoint.py), installed temporary-directory harness, [.gitattributes](../../../.gitattributes) | Both sizes prepare through CLI; mismatch/overwrite/failure exits are explicit. Optional dependencies/global RNG remain untouched. Population fixtures have LF enforced because this checkout uses `core.autocrlf=true`; staged bytes equal the tested canonical files. |

The documentation audit checked 380 relative links/anchors and all 29 task statuses
against the index. Task/progress records now show M1-T02 done and M1-T03 ready.
M1 remains open at 2/3: schedule enumeration/replay dependencies are M1-T03;
rendered exposure, actual prefixes/peer views and protocol execution are M2;
the accepted population/environment freeze and inference remain M5. No scientific
deviation or new runtime dependency was required.

