# Deliverable validation report

Version 1.0, 20 September 2026. This report distinguishes completed specification checks from future experimental work.

## Completed

- Revisited the selected direction and relevant accumulated research; checked current primary literature and concrete public code. The broad novelty claim was narrowed after finding direct prior art. Literature access failures and their implications are recorded in 03 and the source audit.
- Wrote the scientific contract, formal semantics, RRS, full architecture, task/correction/branch protocol, policies, schemas/interfaces, inference/cost plan, statistical analysis, pilot gates, risk/diagnosis plan, prompts, implementation sequence and thesis outline.
- Implemented a CPU reference for minimal-support antichains, recursive labels, independent exhaustive completion labels, exposure closure, and exact/estimated scope masks.
- **15 tests passed**, including **2,260 recursive-versus-exhaustive support comparisons** and nontrivial action-binding, AND/OR, stale-version, duplicate-root, parser/contract and budget checks.
- Exported **39 named schema definitions** and validated five example artifacts. The event example's payload was checked against its declared kind. Schema generation was rerun after adding event-batch and manifest contracts.
- Recomputed the matrix: **6,400 total calls =5,920 short +480 long**. Forecast is **29.121 aggregate GPU-hours** at the documented assumed rates, **54.242 hours** at half speed; both include four hours of pilot/reserve. These are estimates, not measurements.
- Identified and corrected architecture consistency issues: action support versus conclusion support; monotone/unate versus unrestricted Boolean formulas; numerical comparisons with multiple evidence sources; atomic event batches; recipient-reset cancellation; and the distinction between a specification-aware comparator and inaccessible gold information.
- Completed the cross-document audit: 34 internal file links resolved; all nine JSON files parsed; all six Python files passed syntax checks. Confirmed strict event-payload validation, shared policy-slot seeds, transfer prerequisite delivery, mode-specific action instructions, and priority-adherent prefix grading.

## Not claimed as completed

The full agent runner, SILO adapter, numeric transfer evaluator, storage/crash implementation, T4 backend, pilot, preregistration and model experiments remain to implement according to this specification. The support reference is deliberately small. Passing its tests does not establish full agent-system correctness.

No measured model accuracy, repair improvement, throughput, power or runtime safety result is supplied. There are no invented result tables. The proposed plot/table list specifies outputs to produce after running the study.

Some very recent related work could not be fully accessed. The narrowed novelty assessment is provisional until Gate 0 resolves those comparisons. The plan remains useful if the scientific contribution becomes a careful boundary-condition study or preregistered replication, but such a change must be explicit.

## Reproduce the delivered checks

```bash
python -m pip install -r requirements-reference.txt
python -m unittest discover -s tests -v
python -m reference.export_contracts
python -m reference.budget
```

Run from the extracted package root, without Python optimization mode (`-O`). The reference contracts deliberately reject that mode because their Pydantic validators include assertions. Use strict JSON validation at wire boundaries as specified in 15.

## Release checks

The final packaging audit verifies local Markdown links, JSON parseability, schema/example correspondence, code syntax, matrix counts, and archive contents. The archive preserves relative links and directory structure. The loose documents are linked for direct reading. All source research files from the previous investigation remain unchanged.
