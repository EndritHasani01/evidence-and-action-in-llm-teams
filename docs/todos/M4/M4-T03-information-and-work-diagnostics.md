# M4-T03 — Information inventories and retained-work references

**Status:** active

**Dependencies:** [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md). M1–M3 must have passed.

## References

- [Repository contract](../../../AGENTS.md) and [plan explanatory outcomes](../../IMPLEMENTATION_PLAN.md#explanatory-outcomes-and-costs).
- Specification [§2.2 exposure](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§7.2](../../../PROJECT_SPECIFICATION.md#72-what-information-and-work-survived), and [§10 limits](../../../PROJECT_SPECIFICATION.md#10-foundations-limits-and-contribution).
- Technical evidence: [evaluator separation](../../implementation-research/repository-and-validation.md#keep-evaluator-information-outside-peer-state). If inspecting archive witnesses, first follow [research rules](../../../research/AGENTS.md).

## Intended outcome

Offline evidence shows what information and work survived, with source-bound annotations and deterministic references whose assumptions cannot be confused with actual model correctness.

## Scope and boundaries

- Summarize all four prefix rounds' old-gold correctness, acquired remote coverage, history tokens and communication. Verify edited-owner v1 exposure from actual rendered requests without requiring model use or success.
- For L/B align first usable-call-boundary v2 receipt with correctness. Distinguish host injection/forwarding, no receipt, receipt without success, same-call/later success and correctness before authoritative receipt; preserve censored peers.
- For C/F measure boundary-held remote current records excluding the host-injected revision, unique acquired ID/version pairs and all delivery attempts. Tombstones are known; pending replacements are not. Acquisition after intervention is an outcome, not a covariate to remove.
- For receipts distinguish explicit source-bound old-value visibility, reconstructibility under a stated correct-candidate assumption, sufficient current raw evidence and unresolved cases. Numeric occurrence alone is not association; unresolved is not absence. Show offline correctness strata with denominators.
- Freeze a small conservative prose-association rubric with links to actual source/message evidence. No LLM judge, general exposure/dependency graph or claim of complete semantic provenance.
- Implement the §7.2 atlas and selected CPU sufficiency/ambiguity examples for Max (CPU only), Top-K reserves, local Prefix, complete Difference plus anchor, local Sort boundaries and BFS alternatives.
- Apply Prefix/Difference delta transport offline to the actual valid last candidate even when wrong, using specified index/sign rules. Preserve the residual-error identity; no earlier-candidate backfill or runtime repair.
- Record edit position/direction/magnitude, affected output owners, Sort crossings and BFS disconnection for limited descriptive tables/plots.

## Completion criteria

- Evidence inventory, preserved output and measured computation remain separate.
- Every reference labels its information view, correctness assumptions and unavailable-candidate cases.
- Rubric/annotations are deterministic or conservatively documented with source IDs, unresolved categories and denominators, ready for the M5 freeze.
- No diagnostic changes population inclusion, provides model feedback or invents another live arm.

## Validation and evidence

Check receipt timing/censoring, tombstone/pending coverage, repeated delivery versus acquisition, numeric coincidence without association, wrong old candidates and residual identities at endpoints/shard boundaries. Reproduce selected atlas counterexamples from safe independent CPU fixtures without overwriting archive evidence.

**Evidence:** Started on 6 October 2026 on `feat/m4-offline-analysis` from clean
commit `7059d7b`. Authority, the M1–M3 CPU gates and M4-T01 prerequisite evidence
were inspected. `python -S -m unittest tests.test_evaluate tests.test_outcome_archive -q`
passes all 27 prerequisite checks in 31.510 seconds, including reconstruction
from the original lifecycle workers. Information inventories will reuse saved
requests, validations and committed checkpoints; exact history token counts
require a tokenizer that reproduces the saved inputs. No new live state or
scientific configuration is needed. The complete M4 gate remains open.

The pure [reference core](../../../recovery/information.py) and conservative
[association rubric](../../implementation-research/information-diagnostics.md)
are implemented. `python -S -m unittest tests.test_information -q` passes 12
checks in 1.152 seconds, including both sizes, every numeric edit position,
directions and peer slices, wrong-candidate residual identities, unavailable
candidates, receipt censoring, tombstones/pending records, source association
and independent specified-view atlas examples. Worker/CLI integration and
retained inventory reconstruction remain open at this checkpoint.

Ordinary-worker integration now supplies `information_run` and `recovery analyze
--diagnostics`, independently or with `--estimands`. The six retained
[inventory cases](../../../tests/fixtures/information_tables.json.gz) include
both complete five-family runs, both full unknown main populations and the
stopped/resumed prefix. The public checkpoint serializer reads final committed
deliveries in the same read-only application snapshot, with no saver setup or
runner invocation. Receipt reconstruction uses only an actually retained old
candidate; C's archived cleared result never supplies that annotation.

`python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests tests.test_evaluate -q`
passes 52 checks in 17.490 seconds. The separate native harness verifies 160
prefix peer-round and 40 compact-boundary counts at both sizes, using existing
local metadata without weights. Full CPU and installed-package verification
remain in progress at this checkpoint. A retained-table check exposed BFS tuple
versus JSON-array comparison, and the automatic multi-megabyte dictionary diff
made three preliminary validations stall. Those runs were stopped and are not
passing evidence. Endpoint/reference outputs now use JSON arrays and a compact
case/table/row mismatch assertion; safe fresh reconstruction is complete.

Final conservative review keeps an unobserved delivery release/acquisition
unknown, rather than recording a negative outcome. Hand-calculated Sort
crossings and BFS leaf-bridge deletion checks cover both sizes. The final
`python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests -q`
passes all 26 checks in 13.912 seconds; all six retained cases and 200 native
history counts reproduce under hash seed 37. The dependency-free core runs
162 checks in 133.360 seconds: 160 pass and two optional checkpoint checks skip.
The complete CPU lifecycle regression and final installed-package verification
remain in progress at this review checkpoint.

