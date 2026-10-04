# M1-T03 — Complete schedules and replay dependencies

**Status:** done

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

**Schedule checkpoint:** `python -S -m unittest tests.test_schedules -v` passes
nine focused checks on CPython 3.11.9. [schedule.py](../../../recovery/schedule.py)
enumerates all main/development branches, original-prefix parents, distinct call
IDs and exact B/C replay parents. [Independent tables and cell enumeration](../../../tests/test_schedules.py)
reconcile 16,152/17,656 and 11,504/12,560 distinct/logical main slots at both
mathematical sizes; development is 1,114 distinct/1,178 logical, with exactly
80 prefix and ten control calls first. Reordered dependencies, missing parents,
cycles, complete-world control shapes, repeats and poor-prefix nonselection pass.
Saved-file mutation rejection, retained fixture and CLI handoff remain.

**Saved-handoff checkpoint:** [manifests.py](../../../recovery/manifests.py)
and the [CPU CLI](../../../recovery/__main__.py) now save/reload complete derived
schedules against the existing population authority. The retained
[target schedule](../../../tests/fixtures/schedules_target.json) includes main
60 plus the exact development matrix; main 40 derives without another slot store.
The full suite passes **59/59** with `python -S`, and **59/59** through the installed
CPU package from a temporary directory using a prepared fallback schedule.
Installed preparation for both sizes matches canonical bytes; `pip check` passes.
[Saved-file adversaries](../../../tests/test_schedule_manifests.py) cover thirty
scientific/structural mutations, duplicate/nonfinite/malformed JSON, overwrite
protection, exact saved-authority comparison and fresh processes with two hash
seeds and optional imports forbidden. An initial full run caught a misplaced
test-only assertion; it was corrected and both affected checks and the full suite
were rerun successfully. Final M1 gate tables and documentation audit follow.

**Completion evidence (4 October 2026):** Windows x64 (build 26200), CPython
3.11.9. All **59/59 CPU checks pass**, including every M1-T01/T02 check. The
source run used site packages disabled; the installed run validated a saved
fallback schedule outside the checkout. No inference dependency was imported
by preparation/validation, no model/GPU call was made, and no scientific or
accepted configuration was changed.

Executed commands (the retained schedule preparation used a new output file):

```powershell
python -S -m unittest tests.test_schedules -v
python -S -m unittest tests.test_schedule_manifests tests.test_cpu_entrypoint -v
python -S -m recovery prepare --manifest tests/fixtures/population_target.json --output tests/fixtures/schedules_target.json
python -S -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

A temporary-directory harness invoked the installed `prepare --manifest
<population_size.json> --authoritative <population_size.json> --config
<size.toml> --output <schedules_size.json>` for **both** mathematical sizes.
Both outputs matched `schedule_bytes(prepare_schedules(saved_population))`
byte for byte. Installed `validate` with the saved fallback population,
configuration and schedule passed all 59 checks from that directory.
`pip check` reported no broken requirements. These are CPU environment checks,
not an accepted inference lock or capability result.

### Independently calculated main components

Each cell is **distinct generations / logical opportunities**. The table in
[test_schedules.py](../../../tests/test_schedules.py) is literal specification
arithmetic; a separate expected-cell enumeration checks actual subset/event/
policy/replicate membership without using production matrix helpers.

| Component | 60 worlds | 40 worlds |
|---|---:|---:|
| One four-round shared prefix per world | 960 / 960 | 640 / 640 |
| Revised L/B/C/K/F | 4,800 / 4,800 | 3,200 / 3,200 |
| Sham B/C/K | 2,880 / 2,880 | 1,920 / 1,920 |
| Complementary masks, both events | 2,880 / 3,840 | 1,920 / 2,560 |
| Before/after complete-world controls | 120 / 120 | 80 / 80 |
| Preserving B/C/K, fixed sixteen worlds | 768 / 768 | 768 / 768 |
| Revised BΔ/CΔ/KΔ, Prefix/Sort | 1,152 / 1,152 | 768 / 768 |
| Q_B/Q_C, both events, Sort/BFS | 1,152 / 1,536 | 768 / 1,024 |
| Extra B/C/K/mask replicate, both events, fixed ten worlds | 1,440 / 1,600 | 1,440 / 1,600 |
| **Total** | **16,152 / 17,656** | **11,504 / 12,560** |

### Independently calculated development components

| Component | Distinct / logical |
|---|---:|
| Five prefixes, revised L/B/C/K/F, sham B/C/K, ten controls | 730 / 730 |
| Masks, both events, Prefix/BFS only | 96 / 128 |
| Revised receipts, Prefix/Sort | 96 / 96 |
| Q, both events, Sort/BFS | 96 / 128 |
| Preserving B/C/K, Top-K/BFS | 96 / 96 |
| **Pilot total** | **1,114 / 1,178** |
| **Separate smoke maximum / combined distinct maximum** | **24 / 1,138** |

The first 90 logical slots are all distinct: **80 prefix + ten controls**.
`Schedules.capability` selects precisely that block. Smoke slots are not
silently borrowed from the pilot; their actual prompt selection/time gate is M5.

### Acceptance and M1 gate

| Acceptance area | Executed checks / artifacts | Result |
|---|---|---|
| Complete matrix and fixed populations | `ScheduleTests.test_independent_main_component_tables_and_exact_generation_join`, `test_exact_memberships_no_unprescribed_crossings_and_fixed_opportunities` | Both main counts and mathematical sizes pass; exactly the declared receipt/Q/preserving/repeat memberships, no additional crossings, one prefix per world, four rounds × four peers for every team branch. |
| Exact development matrix and first capability block | `test_independent_pilot_components_capability_block_and_separate_smoke` | 730+96+96+96+96 distinct; masks only Prefix/BFS; no extra development replicate; 80+10 capability calls first; smoke separate. |
| Prefix/response identity and repeats | Replay and repeat tests in [test_schedules.py](../../../tests/test_schedules.py) | Every continuation points to its original prefix. Masks select C for the cleared peer and B for the retained peer; Q selects its B/C parent, in the same world/event/replicate/peer. Only required first rounds share a generation. Equal seeds create no additional reuse. Repeat IDs/seeds are new; inputs/prefix/partition remain original. |
| Dependency order and fixed opportunities | Dependency/cycle and poor-prefix tests | Both full schedules and development sort on CPU, including after branch reordering. Previous-round four-peer dependencies, prefix round-four dependencies and raw-reply parents precede their uses. Missing parents/cycles/duplicates fail. Correct, wrong, invalid and timeout prefix annotations do not select or alter opportunities. |
| Complete-world controls | `test_controls_full_world_candidate_lengths_and_empty_send` | Two one-call original/revised controls per world, independent IDs/seeds, no prefix/replay parent; `peer=None` supplies full Prefix/Sort length 32/24. `Branch.empty_send` declares `send=[]` for M2's common outer schema. |
| Saved schedules and mutations | [test_schedule_manifests.py](../../../tests/test_schedule_manifests.py), [target CPU fixture](../../../tests/fixtures/schedules_target.json) | Both sizes save/reload without rebuilding/resampling; exact bytes and 60/40/development orders match. Thirty mutations, malformed/duplicate/nonfinite fields, missing slots/parents, wrong world/event/replicate/peer/retention parent, extra reuse, changed seeds and early recovery fail. Existing files are protected; saved-authority comparison also rejects valid reordering. |
| CPU handoff and isolation | [test_cpu_entrypoint.py](../../../tests/test_cpu_entrypoint.py), fresh-process schedule checks, installed temporary-directory harness | Prepare/validate works at both sizes and outside checkout; errors exit before checks or output creation. Two process hash seeds produce identical bytes without global RNG mutation or optional dependency imports. Fixture LF bytes are protected in Git. |
| M1-T01 and M1-T02 prerequisites | [M1-T01 acceptance](M1-T01-task-worlds-and-truth.md#validation-and-evidence), [M1-T02 acceptance](M1-T02-edits-and-populations.md#validation-and-evidence), complete 59-check reruns | All prior mathematics, exact candidate/coordinate contracts, edits, conditioning, bounded rejection, nested/focal populations, source/owner partitions and saved-stream/authority checks still pass. Original population fixtures and specification are unchanged. |

**M1 gate: passed on CPU.** M1-T01–T03 are done and the
[plan progress](../../IMPLEMENTATION_PLAN.md#progress) links their evidence.
[M2-T01](../M2/M2-T01-peer-views-and-rendering.md) is ready. Request/state/settings
equality before replay, synchronous effects, rendered exposure, actual protocol/
tokenizer capacity, durable execution and inference/resource admission remain
M2–M5. Passing M1 establishes neither feasibility nor recovery results.

The final documentation audit passed **402 local links/anchors in 39 documents**
and all **29 task/index status comparisons** (three done, one ready, 25 blocked).
`git diff --check` passes. Git comparison confirms the specification, size
configuration and both prerequisite population fixtures are unchanged from the
M1-T02 handoff; committed schedule bytes equal the tested canonical fixture.

