# M4-T06 — Reproducible report and pre-GPU analysis gate

**Status:** active

**Dependencies:** [M4-T03](../M4/M4-T03-information-and-work-diagnostics.md), [M4-T05](../M4/M4-T05-uncertainty-and-missingness.md). M1–M3 must have passed.
Both prerequisites are done as of 6 October 2026, and M1–M3's CPU gates pass.
The [M4-T05 handoff](M4-T05-uncertainty-and-missingness.md#completion-and-handoff)
supplies paired uncertainty, shared-response sensitivity, completion/coverage,
conditional-repeat trajectories and paired policy costs from the original workers.
All sixteen retained uncertainty cases reproduce. This task is ready to assemble
the complete synthetic report; its report/CPU gate has not passed.

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

**Evidence:** Started 6 October 2026 from clean `330bf7c` on
`feat/m4-offline-analysis`. The repository contract, task, specification §§1–7,
9–10, plan report/coverage requirements, technical synthesis, prerequisite
M4-T03/T05 evidence and M1–M3 CPU gate evidence were inspected.
`python -S -m unittest tests.test_analysis tests.test_information tests.test_costs tests.test_uncertainty -q`
passes all 87 prerequisite checks in 10.536 seconds on Python 3.11.9, with
site packages disabled.

The report will reuse the existing original-worker joins and scientific tables.
Remaining acceptance work is exact rational case selection, unaltered ID-linked
excerpts, seven grouped exhibits and deterministic plotting inputs, complete and
incomplete offline reproduction, and the named M1–M4 coverage/category audit.
Plot rendering is separate from inference. No new authoritative store, scientific
configuration, GPU/model execution, pilot or empirical result is needed. M4's
report/CPU gate remains open until all required checks pass.

The report/CLI now passes 18 dependency-free focused checks in 12.722 seconds;
the optional renderer adds two checks, with all 20 passing in 28.346 seconds.
Cases use exact rational effects, original IDs and recorded complete-world
slots (failures remain recorded); scheduled repeats cannot replace replicate
zero. Exports preserve raw strings, worker bytes and exclusive destinations;
repeated scientific tables, case IDs, plotting inputs and compressed bytes match.
Seven explicit exhibits include raw world/family displays, all supporting M4
tables and assumptions. Matplotlib is an optional `report` extra, imported only
for rendering; the mandatory CPU/inference dependencies are unchanged.
Original M3 reconstruction, final figure review, complete CPU/installed checks
and the named coverage/category audit remain required before gate closure.

Original-worker review reproduced all sixteen scopes twice in 704.395 seconds,
including both complete five-family scopes, full frozen 60/40 main joins and
stopped work. Every scientific table, case, plotting input and export byte
matched; original worker bytes stayed unchanged. Real records exposed two
schema details now covered independently: full-information controls store one
rendered request, and prose deliveries derive their branch from the original
sender call. Invalid non-scalar reply text is preserved in JSON and displayed
with reversible JSON string notation in HTML, without repair.

Final focused report checks pass 24 in 35.476 seconds. Visual review of all
seven exhibits plus incomplete/stopped views separated paired policy
differences from absolute quality/cost axes and clarified control counts;
scientific tables are unchanged. The [portable bundle](../../../tests/fixtures/scripted_reports.zip)
contains five reports, 35 SVG and 35 PNG exhibits. Its artifact check passes
in 29.668 seconds, covering every local report link, JSON/table/plot join,
case excerpt and figure file. The [CPU audit](../../validation/m4-cpu-gate.md)
maps all 22 plan rows and seven specification check categories to named evidence.
Final current-source reproduction, full regression and installed-package
checks are still required; this task and M4's gate remain active/open.

