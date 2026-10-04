# Blueprint audit and corrections

## Input audited

`recovery_blueprint`, 20 September 2026 edition, 34 files. The package contains a substantial research contract, formal model, interfaces, pilot and compute plans, reference support code, schemas, examples, and tests. It is not an implemented experimental runtime. The companion manifest records the ZIP hash.

## Corrections that future Codex must retain

| Earlier claim or possible inference | Correction |
|---|---|
| LangGraph is not mentioned in the ZIP | It appears once in `10_experiments_and_compute.md`: “No vector database, graph database, Redis, Kubernetes, LangGraph, or paid API is required for this bounded experiment.” The blueprint does not select LangGraph. |
| A custom runner is a settled user requirement | `06_architecture_and_framework.md` proposes a new event-sourced runner. The user's subsequent reuse preference requires reconsidering that choice against framework evidence and small semantic tests. |
| Roughly 60–70% of the old experiment stays the same | This was an unsupported estimate. Compare concrete task generation, interventions, outcomes, and analysis instead of repeating a percentage. |
| Recovery with incomplete provenance is a new gap | Too broad. Close work already discusses omitted dependencies and recovery under incomplete support. The exact empirical distinction needs a comparison. |
| The whole project is validated because reference tests passed | The blueprint reports 15 CPU tests and 2,260 recursive/exhaustive comparisons. These are inherited results, not rerun for this companion, and do not validate a runner, GPU backend, or study outcomes. |
| The 30-hour design is demonstrated feasible | The 29.121 aggregate GPU-hour estimate is an unmeasured forecast. Its safety margin is small. |
| Framework adoption replaces custom research logic | Checkpointing and scheduling can be reused. Observable-state contracts, support semantics, interventions, and scientific evaluation still need project-specific definitions. |

## Preserve these strengths

The research contract already distinguishes a surviving conclusion from an invalid concrete action; natural support estimation from exact support; repair scope from downstream state replacement; and team-level policy effects from claims about decentralization. It also includes all prefixes in the main analysis and treats negative findings as useful. These are important safeguards, not gaps to “fix” by adding infrastructure.

## Artifacts still absent as completed work

The full checkpoint runner, functioning SILO adapter, numeric transfer evaluator, real model smoke test, measured throughput and memory evidence, hardware/model lock, final novelty comparison, and preregistration remain future deliverables. Existing interfaces and examples are specifications, not evidence those components work.

## Source and repository caveats

`source_audit.json` contains inherited repository commits. They were not all independently revalidated in this update. Preserve their exact identifiers but verify accessible commit contents before reuse. The original audit noted SILO Python/version and license metadata inconsistencies. MemTX's repository listing does not establish a license permitting reuse. Public access alone does not resolve that question. Using papers for comparison does not require importing their code.

## What can change without changing the scientific question?

Replacing a runner while preserving observations, information exposure, branch state, calls, and interventions is an infrastructure change. Changing available evidence, allowing adaptive extra model calls, adding retrieval, or replacing the action-binding manipulation changes the experiment. Changing the primary contrast changes the research question being estimated. Document these separately in the future specification.
