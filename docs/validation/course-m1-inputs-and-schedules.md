# Course M1 inputs and schedules evidence

Prepared 9 October 2026 on Windows/PowerShell, CPython 3.11.9, from baseline
`1dfb1e50090ae70c78a18e5ece03482a6f9dc6c1` on
`feat/course-m1-contract-and-inputs`. Follow the
[task](../todos/course/M1/M1-T02-course-inputs-and-schedules.md),
[course handoff](../planning/course-study-session-handoff.md),
[M1-T01 adoption/reuse evidence](course-m1-contract-and-reuse.md) and
[sole scientific authority](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime).
This is CPU input preparation, with no model inference, GPU allocation,
pilot/main execution, accepted freeze or publication.

## Implementation and retained inputs

The existing [populations](../../recovery/populations.py),
[manifests](../../recovery/manifests.py), [schedule](../../recovery/schedule.py)
and [CPU CLI](../../recovery/__main__.py) now accept explicit course scope.
The mathematical generators, solvers, legal edit selection and source/candidate
contracts are reused unchanged. No dependency, alternate runtime, identity
system or persistence layer was added. Runtime 256/64 limits remain M2/M5 work;
the new [input-only TOML](../../configs/course-inputs.toml) records fallback
mathematical size and requires `--regime course` at prepare/validate.

[population_course.json](../../tests/fixtures/population_course.json) is the
host-owned actual-input authority. It explicitly records `regime="course"`,
master seed `20261009`, 20 main worlds/five development worlds, actual raw
records/ownership/positions, chosen changing/preserving edits, mathematical
eligibility, rejections, G/H partitions and assigned streams. Each family's four
edited owners form one preassigned balanced block. G contains peer zero; one
of the three unordered two-pair partitions is chosen uniformly with its own
stream. The existing legal sampling and 1,000-attempt exhaustion are unchanged.
The saved course population rejected one first draw in `main-top_k-01` and one
in `main-bfs_distance-02`, both for `no_owner_changing_edit`. No model output
participates in sampling or cohort selection.

The exact receipt Prefix/Sort, Q Sort/BFS and preserving Top-K/BFS cohorts each
have eight main worlds. Repeat membership is the first one per family, five
worlds; no unused second-replicate seed assignments remain on other worlds.
The five separate development worlds retain their prescribed narrower matrix.
All events refer to the immutable original, and extra replicates keep the
original prefix/partition. Source IDs remain opaque/world-local, and only the
existing public source projection may enter peer metadata. These manifests
contain hidden sources/future edits and must never be used as peer views.

[schedules_course.json](../../tests/fixtures/schedules_course.json) is derived
from that authority, with existing world/branch/call IDs, literal original-prefix
parents and prescribed B/C first-round replay parents. Its explicit regime
prevents loading it against a thesis population. Continuation seeds match across
events/policies for the same world/replicate/round/peer; distinct seeds/physical
generation identities belong to extra replicates. Equal seeds alone never
authorize replay. Every non-control branch retains all sixteen opportunities.
Controls use `peer=None`, complete-world shapes and `send=[]`.

## Independent arithmetic, seeds and compatibility

The retained [auditor](../../notebooks/validation/course-m1-inputs/verify_inputs.py)
reuses M1-T01's independent enumeration and the new tests' independently declared
course cells. It compares actual saved schedules, not two production builder
results, and also checks canonical regeneration and reversed dependency order.

| Component | Main new / logical | Development new / logical |
|---|---:|---:|
| Shared prefixes | 320 / 320 | 80 / 80 |
| Revised L/B/C/K/F | 1,600 / 1,600 | 400 / 400 |
| Sham B/C/K | 960 / 960 | 240 / 240 |
| Complementary masks, both events | 960 / 1,280 | 96 / 128 |
| Full-information controls | 40 / 40 | 10 / 10 |
| Preserving B/C/K | 384 / 384 | 96 / 96 |
| Receipts, revision only | 384 / 384 | 96 / 96 |
| Q_B/Q_C, both events | 384 / 512 | 96 / 128 |
| Additional B/C/K/mask replicate, both events | 720 / 800 | 0 / 0 |
| **Total** | **5,752 / 6,280** | **1,114 / 1,178** |

Main replay uses are 320 masks + 128 Q + 80 repeat masks = 528; development has
32 mask + 32 Q uses = 64. Development starts with exactly 80 prefix/ten control
opportunities. Smoke remains separate, at most 24 calls; planned main + accepted
development + maximum smoke is 6,890 new slots, before retries/failed candidates.
These are opportunities and mathematical counts, not attempts or spending.

The unchanged integer derivation uses `master_seed * 2**20`, existing per-world
4,096 slots and separate main/development slots. Course assigns 860 main stream
seeds plus five owner seeds, and 195 development stream seeds plus five owner
seeds: 1,065 unique assigned seeds. Actual course main/development and both saved
thesis-size seed sets (`20261004`) are disjoint. Two fresh process hash seeds
(1/3981) reproduce both course artifacts with every optional model/library import
blocked; reversed world preparation and unrelated local RNG consumption also
preserve exact inputs. The installed course checks reproduce under hash seed 37.

Both original mathematical sizes still load/regenerate their exact retained
population bytes; original target schedule bytes are identical. Thesis main
60/40 counts remain 16,152/17,656 and 11,504/12,560 at both sizes. Default scope
is thesis; its omitted regime field remains canonically omitted, while explicit
`regime="thesis"` is accepted on loading. The scientific authority, default
study TOML, original thesis todos, prior fixtures/notebooks/vendor attribution
and all remaining protected baseline files are preserved.

## Executed verification

The original focused M1/CLI baseline passed 60 checks before changes. Population
checkpoint `105c327` passed six new course checks and the combined 66-check
regression with zero skips. Schedule/CLI checkpoint `5521961` passed thirteen
course checks with zero skips. Discovery correction `913da21` preserves every
original native-attention test body and explicit native invocation.

The relevant installed-package suite passed 73 checks, zero skips, in 60.322s
outside the checkout with no source `PYTHONPATH`; all 29 installed module bytes
matched source. The updated fourteen course checks passed separately with zero
skips in 10.546s under `PYTHONHASHSEED=37`, including the discovery correction. See
[installed provenance](../../notebooks/validation/course-m1-inputs/installed-provenance.json),
[installed log](../../notebooks/validation/course-m1-inputs/installed-validation.txt),
[hash-seed command](../../notebooks/validation/course-m1-inputs/installed-hash37-command.json)
and [hash-seed log](../../notebooks/validation/course-m1-inputs/installed-hash37-validation.txt).
The package was built/installed locally with `--no-deps --target` into the
recorded temporary directory, with matching tests/configuration/attributed
reference inputs copied alongside it. The existing CPU virtual environment's
`pip check` reports no broken requirements; torch/model packages are absent.

The first broad dependency-free CLI run exposed two existing `setUpClass`
errors because optional native Torch/Transformers checks were discovered without
those packages. The [original failure](../../notebooks/validation/course-m1-inputs/core-validation-before-fix.txt)
is retained. Those tests already specify explicit native-stack execution; their
standard unittest `load_tests` hook now keeps automatic CPU discovery separate
while `unittest tests.test_t4_attention` still selects all original tests.
The earlier full run was stopped after this diagnosis; its
[partial log](../../notebooks/validation/course-m1-inputs/full-validation-stopped.txt)
is retained and is not a completed regression. No native/T4 acceptance is claimed.

Corrected dependency-free validation passes **342 checks: 334 passed and eight
expected skips** (six checkpoint-library and two optional-renderer checks), in 218.758s.
The [core log](../../notebooks/validation/course-m1-inputs/core-validation-pass.txt)
and [exact command](../../notebooks/validation/course-m1-inputs/core-command.json)
are retained. The corrected **full CPU regression passes 534 tests, zero skips,
in 2,219.782s**, with return code zero. Its
[full log](../../notebooks/validation/course-m1-inputs/full-validation-pass.txt)
and [exact command](../../notebooks/validation/course-m1-inputs/full-command.json)
include original protocol, durable replay, attempts/workers/accounting,
controller-kill lifecycle, all sixteen report scopes reproduced twice,
uncertainty/archive reproduction and inference-mock regressions. These are CPU
checks; native Torch/Transformers integration still requires explicit execution
in its own environment.

Reproduction commands (prepare to new files; fixtures reject overwrites):

```powershell
python -X utf8 -S -B -m recovery prepare --regime course --config configs/course-inputs.toml --seed 20261009 --output population.json
python -X utf8 -S -B -m recovery prepare --regime course --config configs/course-inputs.toml --manifest population.json --output schedules.json
python -X utf8 -S -B -m recovery validate --core-only --regime course --config configs/course-inputs.toml --manifest population.json --schedule schedules.json --authoritative tests/fixtures/population_course.json
.venv/Scripts/python.exe -X utf8 -B -m recovery validate --regime course --config configs/course-inputs.toml --manifest tests/fixtures/population_course.json --schedule tests/fixtures/schedules_course.json --authoritative tests/fixtures/population_course.json
python -X utf8 -S -B notebooks/validation/course-m1-inputs/verify_inputs.py --completion --output new-completion-audit.json
.venv/Scripts/python.exe -m pip check
git diff --check
git diff --cached --check
```

The initial [independent input audit](../../notebooks/validation/course-m1-inputs/input-checkpoint-audit.json)
passes components/cohorts/owner balance, canonical inputs/schedules, seed
separation and both original size/count schedules. Its raw pre-edit snapshot
comparison verifies **1,148 protected files byte-for-byte identical**, including
the existing unstaged M5 preparation edit with SHA-256
`c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca`.
It checked 577 local references and 266 Markdown fragments at that checkpoint.
The audit's current baseline-file comparison uses a temporary raw snapshot when
available and Git baseline comparison for clean replays; it is derived evidence,
not another runtime store. The new evidence outputs use exclusive creation.

## Completion and handoff

The course **M1 input/schedule CPU gate is passed**. The
[passed completion audit](../../notebooks/validation/course-m1-inputs/completion-audit.json)
checks
the four passing suite logs/command receipts, independent population/schedule
arithmetic, saved-input/seed/replay invariants, all course task/index statuses,
local references/anchors and protected baseline files. It also verifies that
thesis roadmap Sections 1-10 remain intact and the pre-existing M5 edit is
unchanged and unstaged. At that checkpoint it checked 612 local references and
269 Markdown fragments, with two done/one ready/eighteen blocked course tasks.
The derived audit records are retained in the
[course validation directory](../../notebooks/validation/course-m1-inputs/).

Course [M2-T01](../todos/course/M2/M2-T01-course-protocol-and-limits.md) is ready.
Course M2 owns uniform 256/64 rendering,
validation/settings, interventions/replay and attainability/capacity. Course M3
renews worker/resume/accounting evidence; M4 owns course analysis denominators
and reports. Existing `status`/`analyze` CLI count choices remain thesis 60/40
until their respective course tasks; this input handoff does not accept those
runtime/analysis consumers for course main execution.

Actual host/model loading, complete course envelope/headroom, prior allocation
reconciliation, smoke, capability, complete pilot, resource admission, authorized
freeze, empirical execution and external delivery remain later gates. Nothing
here grants GPU/model execution or freezes these prepared inputs. Thesis gates
and all original task statuses remain separate.
