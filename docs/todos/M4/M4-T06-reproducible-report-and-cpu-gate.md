# M4-T06 — Reproducible report and pre-GPU analysis gate

**Status:** done

**Dependencies:** [M4-T03](../M4/M4-T03-information-and-work-diagnostics.md), [M4-T05](../M4/M4-T05-uncertainty-and-missingness.md). M1–M3 must have passed.
Both prerequisites are done as of 6 October 2026, and M1–M3's CPU gates pass.
The [M4-T05 handoff](M4-T05-uncertainty-and-missingness.md#completion-and-handoff)
supplies paired uncertainty, shared-response sensitivity, completion/coverage,
conditional-repeat trajectories and paired policy costs from the original workers.
All sixteen retained uncertainty cases reproduce. This task completes the
synthetic report and M1–M4 CPU acceptance on 6 October 2026. The
[CPU audit](../../validation/m4-cpu-gate.md) passes; actual hardware, capability,
resource admission and accepted-host validation remain M5 gates.

## References

- [Repository contract](../../../AGENTS.md), [plan report acceptance](../../IMPLEMENTATION_PLAN.md#report-and-acceptance-evidence), [coverage map](../../IMPLEMENTATION_PLAN.md#9-coverage-map), and [living handoff](../../IMPLEMENTATION_PLAN.md#10-living-handoff).
- Specification [§7.4](../../../PROJECT_SPECIFICATION.md#74-results-narrative-and-cases), [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements), and [§10](../../../PROJECT_SPECIFICATION.md#10-foundations-limits-and-contribution).

## Intended outcome

Offline analyze/export operations reproduce the complete intended report from the scripted run, closing all CPU gates before any GPU spending.

## Scope and boundaries

- Assemble roughly seven or eight grouped exhibits: task/prior-work context; recovery policy effects; repair/preservation; representation/receipts; collaborator effects; prose timing/synchronization; and quality/cost with repeatability/limitations.
- Include family/world tables, traces, raw contrasts, uncertainty, coverage, inactive Q treatments, capability controls, information inventories, separate work/cost views and limitations as supporting outputs.
- Implement case selection now: for corrected C−B AUC, revised E_keep and KΔ−K round-one accuracy choose the lower observed median strictly positive and negative complete world, sorting by effect then immutable ID. Merge duplicate worlds, report missing signs and cap cards at six.
- If all contrasts are zero, select the smallest-ID regression world or smallest complete world if none regress. If no eligible complete world exists, cases are unavailable. Preserve unaltered excerpts with call/message IDs, edits, trajectories, availability and preservation.
- Preserve interpretations for equal event effects, subgroup cancellation, receipt benefits with zero interaction, harmful delay, ceiling/poor capability, broad intervals and unstable repeats. No favorable-case selection or semantic causation inferred from prose.
- Keep offline imports independent of inference. Derive exports from the canonical artifacts, with no second authoritative store.

## Completion criteria

- Every M4 output can be reproduced from the M3 scripted bundle twice with identical tables, selected IDs and deterministic plotting inputs.
- The frozen case/annotation rules, analysis settings and assumptions are ready for M5's bundle.
- Check the plan's coverage map and all seven §9 check categories against named M1–M4 evidence; gaps remain blocked. M1–M4 acceptance must pass before GPU use.
- Update the plan's progress/decisions/issues with verified evidence. Label all scripted exhibits as synthetic validation, never empirical findings.

## Validation and evidence

Test tied/missing positive and negative signs, duplicate selections, all-zero regression fallback and no complete cases. Run complete and deliberately incomplete scripted bundles through analysis/export in an environment without inference imports. Compare repeated outputs and plotting data, verify report links/provenance, and inspect figures for coherent labels/denominators. Use the focused synthetic checks from M4-T01–T05 as the report's acceptance evidence rather than claiming effects.

### Checkpoint evidence

Started 6 October 2026 from clean `330bf7c` on
`feat/m4-offline-analysis`. The repository contract, task, specification §§1–7,
9–10, plan report/coverage requirements, technical synthesis, prerequisite
M4-T03/T05 evidence and M1–M3 CPU gate evidence were inspected.
`python -S -m unittest tests.test_analysis tests.test_information tests.test_costs tests.test_uncertainty -q`
passes all 87 prerequisite checks in 10.536 seconds on Python 3.11.9, with
site packages disabled.

The initial scope reused existing original-worker joins and scientific tables.
Acceptance work at that checkpoint was exact rational case selection, unaltered ID-linked
excerpts, seven grouped exhibits and deterministic plotting inputs, complete and
incomplete offline reproduction, and the named M1–M4 coverage/category audit.
Plot rendering is separate from inference. No new authoritative store, scientific
configuration, GPU/model execution, pilot or empirical result is needed. M4's
report/CPU gate remained open until all required checks passed.

The report/CLI now passes 18 dependency-free focused checks in 12.722 seconds;
the optional renderer adds two checks, with all 20 passing in 28.346 seconds.
Cases use exact rational effects, original IDs and recorded complete-world
slots (failures remain recorded); scheduled repeats cannot replace replicate
zero. Exports preserve raw strings, worker bytes and exclusive destinations;
repeated scientific tables, case IDs, plotting inputs and compressed bytes match.
Seven explicit exhibits include raw world/family displays, all supporting M4
tables and assumptions. Matplotlib is an optional `report` extra, imported only
for rendering; the mandatory CPU/inference dependencies are unchanged.
At that checkpoint original M3 reconstruction, final figure review, complete
CPU/installed checks and the named coverage/category audit remained required.

Original-worker review reproduced all sixteen scopes twice in 704.395 seconds,
including both complete five-family scopes, full frozen 60/40 main joins and
stopped work. Every scientific table, case, plotting input and export byte
matched; original worker bytes stayed unchanged. Real records exposed two
schema details now covered independently: full-information controls store one
rendered request, and prose deliveries derive their branch from the original
sender call. Invalid non-scalar reply text is preserved in JSON and displayed
with reversible JSON string notation in HTML, without repair.

Post-schema/figure review passed 24 focused checks in 35.476 seconds. Review of all
seven exhibits plus incomplete/stopped views separated paired policy
differences from absolute quality/cost axes and clarified control counts;
scientific tables are unchanged. The [portable bundle](../../../tests/fixtures/scripted_reports.zip)
contains five reports, 35 SVG and 35 PNG exhibits. Its artifact check passes
in 29.668 seconds, covering every local report link, JSON/table/plot join,
case excerpt and figure file. The [CPU audit](../../validation/m4-cpu-gate.md)
maps all 22 plan rows and seven specification check categories to named evidence.
At that checkpoint current-source reproduction, full regression and installed
checks were still required; this task and M4's gate remained active/open.

The pre-join-review core command, `python -S -m recovery validate --core-only`,
runs 251 checks in 219.957 seconds: 243 pass and eight optional archive/renderer
checks skip. The actual installed M4 package suite outside the checkout passes
165 checks in 224.674 seconds under `PYTHONHASHSEED=37`; twelve installed module
paths/bytes match current source. Installed `analyze --report --figures` preserves
all 1,178 unknown development slots, saves seed 37, renders seven figure pairs,
passes 27 local links and protects the absent worker and existing output.
The renewed native tokenizer capacity command passes eight checks in 1.994
seconds with local 9B metadata only; target/fallback bounds remain
261,388/259,868 including reserve. `compileall` and `pip check` passed. Full source
regression and blocked-import original-worker reconstruction were then running.

Review additionally made the card join enforce replicate zero directly. The
existing estimand export already separates repeated contrasts, so every retained
case remains unchanged and uses only original trajectories. An independent
fixture that appends a conflicting replicate-one contrast failed before the
one-line join fix and passes afterward. The original-worker assertion now also
requires all card trajectories to be replicate zero. Renewed focused checks
pass 25 in 35.458 seconds; full source/core/installed and blocked-import
reconstruction were restarted against this final code.

## Completion and M4 gate

The following results supersede intermediate checkpoint counts above.
M4-T06 is implemented and verified on CPU; **M4's gate passes**. All M1–M4
CPU gates are closed, and [M5-T01](../M5/M5-T01-inference-and-allocation-preparation.md)
is ready for CPU backend/allocation preparation. Passing this gate does not
authorize GPU use or satisfy any M5 operational gate.
Environment: Windows/CPU, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and LangChain Core 1.6.6.
Optional plotting uses Matplotlib 3.11.0, NumPy 2.4.6, Agg and DejaVu Sans;
its environment record does not freeze inference.

| Scope / named check | Executed result |
|---|---|
| `python -S -m recovery validate --core-only` | 252 run in 232.486 seconds: 244 passed, eight optional decoder/archive/renderer skips. |
| `tests.test_report`, `tests.test_report_run`, `tests.test_report_figures` | All 25 passed in 35.458 seconds; exact medians, signs, merges, fallbacks, repeat-zero joins, literal raw text, unknowns, exclusive outputs, offline imports and repeated SVG/PNG bytes. |
| Noneditable installed M4 suite outside checkout under `PYTHONHASHSEED=37` | All 166 passed in 240.574 seconds; twelve installed module paths and bytes match final source. |
| Installed `analyze --report --figures` outside checkout | Passed in 15.328 seconds: all 1,178 development slots unknown, seed 37 saved, seven figure pairs, 27 local links, absent worker unchanged and existing output protected. |
| Installed `tests.report_archive` with inference/execution/Matplotlib imports blocked and hash seed 37 | All sixteen original-worker scopes reproduce twice in 638.969 seconds, matching every table/report/trace/input and compressed/HTML/CSV byte; original worker bytes unchanged. Current source's same sixteen-scope check also passes within the integrated suite. |
| `ReportArchiveTests.test_portable_complete_incomplete_and_stopped_reports_match_retained_evidence` | Passed separately in 29.668 seconds and in the final installed/source suites; five reports, 126 files, 35 SVG and 35 PNG exhibits, valid links/anchors and report/plot/table/case joins. |
| Independent derived-table regression-excerpt fixture | Passed in 3.047 seconds: all-zero fallback joins the expected K round-two peer-one call, actual prefix round-four call, unchanged raw trace, trajectory and availability IDs. This checks the case join, separately from evaluator truth tests. |
| `tests.tokenizer_capacity --tokenizer LOCAL_9B_METADATA` | Eight passed in 1.994 seconds; target/fallback bounds 261,388/259,868 including reserve. Local tokenizer metadata only, no language weights. |
| `compileall`, `pip check`, `git diff --check` | Passed against final code. |
| Complete `.venv/Scripts/python.exe -m recovery validate` | All 424 passed in 2,479.221 seconds, with no skips; includes all nine integrated lifecycle checks and eleven real controller kills. |

The installed suite loads evaluation, analysis, information, costs, uncertainty,
report, figures, manifests, tasks, populations, schedule and truth from
`site-packages` before exposing the checkout's tests. It runs the M4 core/run
modules plus optional rendering and portable-artifact checks. The independent
installed archive process blocks `torch`, `transformers`, `accelerate`,
`bitsandbytes`, `matplotlib`, runner, workers, inference and storage imports.
Test transcripts and true subprocess return codes are retained locally under
`$env:TEMP/m4-t06-*`; original scientific/CPU artifacts remain unchanged.

The named [22-row/seven-category audit](../../validation/m4-cpu-gate.md)
passes its link/anchor, task/index/milestone, existing-test-name and protected
artifact checks: 550 local links/anchors across sixteen documents, all 29
task/index statuses and all six milestone counts agree. It separates CPU evidence from accepted-host/device, finite
output, capability, resource forecast and empirical/release work. Whole source
regression passes; no CPU acceptance gap remains. The original specification,
configuration, mandatory dependencies, execution/scoring modules and all prior
fixtures/prerequisite task evidence are unchanged. Matplotlib is the optional
report extra only.

The [sixteen reports](../../../tests/fixtures/report_tables.json.gz) and
[five-report bundle](../../../tests/fixtures/scripted_reports.zip) are derived
synthetic validation, not empirical findings. Complete fixture scopes each
retain 2,170 recorded calls; full 60/40 joins retain 15,486/10,390 unknowns,
and stopped work retains sixteen unknowns with unavailable cases. Cases never
change populations; all interpretations, assumptions and nonexclusive annotation
rules are ready for M5's future accepted bundle. No GPU allocation, language
weight loading, model inference, pilot, main experiment, scientific/frozen
configuration change or publication occurred. M6-T02 remains blocked pending
a quiescent actual-execution or documented terminal-feasibility handoff.

