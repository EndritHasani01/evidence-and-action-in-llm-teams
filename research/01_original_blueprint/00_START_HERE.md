# What remains valid after a correction?

**Authoritative research and engineering blueprint · version 1.0 · 20 September 2026**

Recommended thesis: **Evidential support and action repair in stateful LLM teams.** Study when an agent team can retain a still-true conclusion while correctly changing an action tied to superseded evidence. The contribution is an explanatory experiment about support representation and downstream state, not another recovery framework.

## The important revision to the original idea

Recent work already occupies broad claims about selective rollback, independent-support preservation, memory cascades, transactional commits and parts of incomplete-provenance recovery. This blueprint narrows the question to **alternative support × concrete action binding**, then separates estimated-support errors from the failure to apply a correct repair to downstream state. See [03_related_work.md](03_related_work.md) for the evidence and remaining access limitations.

Example: another warehouse can keep “this order is fulfillable” true after warehouse X's stock is corrected. That does not keep `ship_from(X)` valid. The experiment asks whether natural agent handoffs and recovery policies maintain that distinction, and whether a precise invalidation notice is enough to change what the executing agent does.

## Final decisions

| Decision | Specification |
|---|---|
| Main scientific question | When can estimated support safely preserve conclusions while repairing witness-bound actions after a factual correction? |
| Main design | 64 base worlds, two SILO-derived task families, four matched support/action variants, N/R/E policy branches from identical realized prefixes. |
| Mechanism diagnostics | Exact scope O; action-granularity ablation OC; exact notice without withdrawal ON; recipient-state rebuild OR. |
| Infrastructure | Extend SILO's generators; implement a small event-sourced recovery runner. Use a controlled MasDrift-derived workflow transfer. |
| Formal ground truth | Minimal AND/OR evidential supports for typed claims and actual action arguments; independent exhaustive validation. |
| Agent organization | Three owned states and contexts: source owner A, integrating planner B, executor C. Reliable source-capsule handoffs. |
| Compute | Matrix A: 6,400 calls; illustrative 29.12 aggregate GPU-hours including pilot/reserve. Matrix B: 6,080 calls without second-model block, selected before confirmation. Both require measured admission. |
| First real-model pilot | 152 calls on two base worlds; preceded by the CPU worked-world and checkpoint tests. |
| Main result | A policy-by-binding interaction estimate, with diagnostic evidence separating representation and state-repair mechanisms. A negative result is allowed. |

The exact support service is implementable when a workflow has a complete executable specification. It is a specification-aware comparator here; an “oracle” only relative to natural-language workflows lacking that service. The thesis must not argue for LLM dependency inference where an exact compiler is available.

## Reading order

| Document | Purpose |
|---|---|
| [01_working_plan.md](01_working_plan.md) | Plan created before conclusions and evidence-led revisions. |
| [02_research_contract.md](02_research_contract.md) | Question, hypotheses, estimand, novelty boundary and contribution. |
| [03_related_work.md](03_related_work.md) | Current literature audit, classical foundations, prohibited novelty claims. |
| [04_formal_model.md](04_formal_model.md) | Evidence versions, exact/estimated support, AND/OR semantics, claim/action validity. |
| [05_requirements.md](05_requirements.md) | RRS, functional/non-functional requirements, acceptance and traceability. |
| [06_architecture_and_framework.md](06_architecture_and_framework.md) | SILO decision, source audit, components, ownership, state machines and packages. |
| [07_tasks_and_protocol.md](07_tasks_and_protocol.md) | Generators, correction protocol, source transport, frozen prefixes, transfer and graders. |
| [08_policies_and_controls.md](08_policies_and_controls.md) | Exact policy behavior, baselines, controls, diagnostics and CPU ablations. |
| [09_interfaces_and_storage.md](09_interfaces_and_storage.md) | Schemas/APIs, event batches, checkpoints, seeds, caching, failures and storage. |
| [10_experiments_and_compute.md](10_experiments_and_compute.md) | Run counts, model/backend choices, token ledger, admission and execution order. |
| [11_metrics_statistics_and_outputs.md](11_metrics_statistics_and_outputs.md) | Metrics, formulas, clustered inference, power limits, result tables and figures. |
| [12_pilot_and_decision_gates.md](12_pilot_and_decision_gates.md) | Minimum pilot, capability/novelty/compute gates, continue/pivot/abandon rules. |
| [13_validation_risks_and_diagnosis.md](13_validation_risks_and_diagnosis.md) | Testing, failure diagnoses, confounders and scientific limits. |
| [14_implementation_sequence_and_thesis.md](14_implementation_sequence_and_thesis.md) | Ordered build/run plan, preregistration, thesis chapters and research artifacts. |
| [15_prompt_and_rendering_contract.md](15_prompt_and_rendering_contract.md) | Agent/extractor/reviewer templates, state rendering, parser and token limits. |
| [16_validation_report.md](16_validation_report.md) | What was actually validated in this deliverable and what remains to implement. |

## Machine-readable and executable materials

- [configs/experiment.json](configs/experiment.json): exact matrix and global call limits.
- [schemas/contracts.schema.json](schemas/contracts.schema.json): named JSON Schemas generated from the Python contracts.
- [reference/contracts.py](reference/contracts.py): strict schemas, including claims/actions, events, checkpoints and run manifests.
- [reference/support.py](reference/support.py): support algebra, independent exhaustive oracle and mask reference functions.
- [reference/budget.py](reference/budget.py): matrix arithmetic and explicitly illustrative cost forecast.
- [tests/test_reference.py](tests/test_reference.py): meaningful semantic and contract tests.
- [examples/worked_support.json](examples/worked_support.json): a surviving conclusion with an invalid old action.
- [examples/agent_reply.json](examples/agent_reply.json), [examples/extractor_reply.json](examples/extractor_reply.json), [examples/repair_plan.json](examples/repair_plan.json), [examples/event.json](examples/event.json): validated examples.
- [source_audit.json](../07_repository_audit/source_audit.json): checked repositories, commits, inspected files and literature access status.
- [budget_forecast.json](budget_forecast.json): generated count/cost calculation; `measured=false`.

## What is complete and what is not

The research specification, system contracts, run matrix and tested symbolic reference are delivered. No full agent runtime, T4 experiment, model result, numeric transfer implementation or completed preregistration is claimed. Hardware throughput and some close-paper full-text comparisons remain explicit pre-experiment gates. The older 9,760-call proposal is superseded by this design; no earlier empirical result is assumed.

Start with the CPU counterexample and the 152-call pilot. Proceed to the full implementation and confirmation only if those checks make the research question measurable within the available compute.
