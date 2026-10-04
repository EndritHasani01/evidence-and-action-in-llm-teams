# Research file index

Read [README.md](README.md) for authority, recommended order and snapshot caveats. Entries are grouped by research phase and sorted by path within each phase.

## 01_original_blueprint

Original support/action blueprint and its executable reference assets. Historical; superseded.

| File | Title or artifact |
|---|---|
| [00_START_HERE.md](01_original_blueprint/00_START_HERE.md) | What remains valid after a correction? |
| [01_working_plan.md](01_original_blueprint/01_working_plan.md) | Working research plan |
| [02_research_contract.md](01_original_blueprint/02_research_contract.md) | Research contract |
| [03_related_work.md](01_original_blueprint/03_related_work.md) | Related work and novelty audit |
| [04_formal_model.md](01_original_blueprint/04_formal_model.md) | Formal model and evaluator semantics |
| [05_requirements.md](01_original_blueprint/05_requirements.md) | Research Requirements Specification (RRS) |
| [06_architecture_and_framework.md](01_original_blueprint/06_architecture_and_framework.md) | Architecture and framework decision |
| [07_tasks_and_protocol.md](01_original_blueprint/07_tasks_and_protocol.md) | Tasks, world generation, protocol, and graders |
| [08_policies_and_controls.md](01_original_blueprint/08_policies_and_controls.md) | Recovery policies, controls, and ablations |
| [09_interfaces_and_storage.md](01_original_blueprint/09_interfaces_and_storage.md) | Interfaces, schemas, checkpoints, and reproducibility |
| [10_experiments_and_compute.md](01_original_blueprint/10_experiments_and_compute.md) | Exact experiment matrix, inference, and compute |
| [11_metrics_statistics_and_outputs.md](01_original_blueprint/11_metrics_statistics_and_outputs.md) | Metrics, statistical analysis, and expected outputs |
| [12_pilot_and_decision_gates.md](01_original_blueprint/12_pilot_and_decision_gates.md) | Pilot, capability gates, and decisions |
| [13_validation_risks_and_diagnosis.md](01_original_blueprint/13_validation_risks_and_diagnosis.md) | Validation, scientific risks, and failure diagnosis |
| [14_implementation_sequence_and_thesis.md](01_original_blueprint/14_implementation_sequence_and_thesis.md) | Implementation sequence, execution plan, and thesis artifacts |
| [15_prompt_and_rendering_contract.md](01_original_blueprint/15_prompt_and_rendering_contract.md) | Prompt and rendering contract |
| [16_validation_report.md](01_original_blueprint/16_validation_report.md) | Deliverable validation report |
| [reference/__init__.py](01_original_blueprint/reference/__init__.py) | __init__.py |
| [reference/budget.py](01_original_blueprint/reference/budget.py) | budget.py |
| [reference/contracts.py](01_original_blueprint/reference/contracts.py) | contracts.py |
| [reference/export_contracts.py](01_original_blueprint/reference/export_contracts.py) | export_contracts.py |
| [reference/support.py](01_original_blueprint/reference/support.py) | support.py |
| [tests/test_reference.py](01_original_blueprint/tests/test_reference.py) | test_reference.py |
| [configs/experiment.json](01_original_blueprint/configs/experiment.json) | experiment.json |
| [schemas/contracts.schema.json](01_original_blueprint/schemas/contracts.schema.json) | contracts.schema.json |
| [examples/agent_reply.json](01_original_blueprint/examples/agent_reply.json) | agent_reply.json |
| [examples/event.json](01_original_blueprint/examples/event.json) | event.json |
| [examples/extractor_reply.json](01_original_blueprint/examples/extractor_reply.json) | extractor_reply.json |
| [examples/repair_plan.json](01_original_blueprint/examples/repair_plan.json) | repair_plan.json |
| [examples/worked_support.json](01_original_blueprint/examples/worked_support.json) | worked_support.json |
| [budget_forecast.json](01_original_blueprint/budget_forecast.json) | budget_forecast.json |
| [requirements-reference.txt](01_original_blueprint/requirements-reference.txt) | requirements-reference.txt |
| [requirements-inference.in](01_original_blueprint/requirements-inference.in) | requirements-inference.in |

## 02_agent_context

Earlier agent handoff, background, source register and context. Historical; superseded.

| File | Title or artifact |
|---|---|
| [00_READ_ME.md](02_agent_context/00_READ_ME.md) | Context companion for the recovery blueprint |
| [01_USER_CONTEXT_AND_PRIORITIES.md](02_agent_context/01_USER_CONTEXT_AND_PRIORITIES.md) | User context and priorities |
| [02_BLUEPRINT_AUDIT_AND_CORRECTIONS.md](02_agent_context/02_BLUEPRINT_AUDIT_AND_CORRECTIONS.md) | Blueprint audit and corrections |
| [03_RESEARCH_AND_NOVELTY_UPDATE.md](02_agent_context/03_RESEARCH_AND_NOVELTY_UPDATE.md) | Research and novelty update |
| [04_FRAMEWORK_AND_TOOLING_EVIDENCE.md](02_agent_context/04_FRAMEWORK_AND_TOOLING_EVIDENCE.md) | Framework and tooling evidence |
| [05_COMPUTE_AND_PILOT_CONTEXT.md](02_agent_context/05_COMPUTE_AND_PILOT_CONTEXT.md) | Compute and pilot context |
| [06_SCIENTIFIC_DESIGN_REVIEW.md](02_agent_context/06_SCIENTIFIC_DESIGN_REVIEW.md) | Scientific design review |
| [07_OPEN_DECISIONS_AND_ACCEPTANCE_GATES.md](02_agent_context/07_OPEN_DECISIONS_AND_ACCEPTANCE_GATES.md) | Open decisions and acceptance gates |
| [08_CODEX_HANDOFF.md](02_agent_context/08_CODEX_HANDOFF.md) | Handoff prompt for the specification-writing session |
| [09_SOURCE_REGISTER.md](02_agent_context/09_SOURCE_REGISTER.md) | Source register |
| [background/classical_mas_vs_modern_llm_agents.md](02_agent_context/background/classical_mas_vs_modern_llm_agents.md) | Classical Multi-Agent Systems vs Modern LLM Agents |
| [background/failure_attribution_diagnosis_recovery.md](02_agent_context/background/failure_attribution_diagnosis_recovery.md) | Failure Attribution, Diagnosis and Recovery in Multi-Agent LLM Systems |
| [background/multi_agent_evaluation_science.md](02_agent_context/background/multi_agent_evaluation_science.md) | Multi-Agent Evaluation Science |
| [background/README.md](02_agent_context/background/README.md) | Historical background reports |
| [background/shared_memory_distributed_knowledge_and_provenance.md](02_agent_context/background/shared_memory_distributed_knowledge_and_provenance.md) | Shared Memory, Distributed Knowledge and Provenance |
| [context_facts.json](02_agent_context/context_facts.json) | context_facts.json |
| [manifest.json](02_agent_context/manifest.json) | manifest.json |

## 03_innovation_review

First innovation investigation, literature, risks and CPU audit. Historical research and supporting evidence.

| File | Title or artifact |
|---|---|
| [CANDIDATE_INNOVATIONS.md](03_innovation_review/CANDIDATE_INNOVATIONS.md) | Candidate comparison |
| [CURRENT_THINKING.md](03_innovation_review/CURRENT_THINKING.md) | Current thinking |
| [DECISION_LOG.md](03_innovation_review/DECISION_LOG.md) | Decision log |
| [decisions/REVIEW_RESOLUTIONS.md](03_innovation_review/decisions/REVIEW_RESOLUTIONS.md) | Independent review resolutions |
| [evidence/audit_repository.py](03_innovation_review/evidence/audit_repository.py) | audit_repository.py |
| [evidence/audit_results.json](03_innovation_review/evidence/audit_results.json) | audit_results.json |
| [evidence/counterexample_results.json](03_innovation_review/evidence/counterexample_results.json) | counterexample_results.json |
| [evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md](03_innovation_review/evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md) | Current validity, historical provenance, and search completeness |
| [evidence/ISOLATION_AND_CERTIFICATION_PREDECESSORS.md](03_innovation_review/evidence/ISOLATION_AND_CERTIFICATION_PREDECESSORS.md) | Direct predecessors to isolation and validity-based reuse |
| [evidence/recovery_counterexamples.py](03_innovation_review/evidence/recovery_counterexamples.py) | recovery_counterexamples.py |
| [evidence/REOPENING_EXCLUSIONS.md](03_innovation_review/evidence/REOPENING_EXCLUSIONS.md) | Reopening discarded possibilities after change |
| [evidence/REPOSITORY_INSPECTION.md](03_innovation_review/evidence/REPOSITORY_INSPECTION.md) | Fresh repository inspection |
| [evidence/SEARCH_AND_CLAIM_LEDGER.md](03_innovation_review/evidence/SEARCH_AND_CLAIM_LEDGER.md) | Search and claim ledger |
| [evidence/WORKSPACE_VALIDATION.md](03_innovation_review/evidence/WORKSPACE_VALIDATION.md) | Final workspace validation |
| [FALSIFICATION_AND_RISKS.md](03_innovation_review/FALSIFICATION_AND_RISKS.md) | Falsification and risks |
| [ideas/CANDIDATE_GENERATION.md](03_innovation_review/ideas/CANDIDATE_GENERATION.md) | Candidate generation before selection |
| [landscape/ADJACENT_FIELDS.md](03_innovation_review/landscape/ADJACENT_FIELDS.md) | Adjacent-field investigation: recovery as controlled reuse |
| [landscape/BELIEF_SLICING_AND_SNAPSHOTS.md](03_innovation_review/landscape/BELIEF_SLICING_AND_SNAPSHOTS.md) | Belief revision, slicing and consistent snapshots |
| [landscape/COMPLETION_PROTOCOL_VERDICT.md](03_innovation_review/landscape/COMPLETION_PROTOCOL_VERDICT.md) | Skeptical verdict on revision-sensitive completion |
| [landscape/MEMORY_AND_PLAN_REUSE_2025.md](03_innovation_review/landscape/MEMORY_AND_PLAN_REUSE_2025.md) | 2025 foundations: memory updating and procedural reuse |
| [landscape/PROTOCOL_RECOVERY.md](03_innovation_review/landscape/PROTOCOL_RECOVERY.md) | Agent recovery protocols: closest prior art |
| [landscape/RECENT_AGENT_WORK.md](03_innovation_review/landscape/RECENT_AGENT_WORK.md) | Recent agent-recovery work: live research ledger |
| [landscape/REOPENING_SEARCH_NOVELTY.md](03_innovation_review/landscape/REOPENING_SEARCH_NOVELTY.md) | Reopening search after change: promising distinction, strong novelty caution |
| [landscape/RETENTION_AND_REVISABLE_EXECUTION.md](03_innovation_review/landscape/RETENTION_AND_REVISABLE_EXECUTION.md) | Retention and revisable execution: additional close work |
| [landscape/REUSE_AND_UNLEARNING.md](03_innovation_review/landscape/REUSE_AND_UNLEARNING.md) | Additional close prior work: reuse and unlearning |
| [landscape/SEMANTIC_REVISION.md](03_innovation_review/landscape/SEMANTIC_REVISION.md) | Semantic revision without perfect dependencies |
| [landscape/UNCERTAIN_LOCALIZATION.md](03_innovation_review/landscape/UNCERTAIN_LOCALIZATION.md) | Uncertainty-aware rollback is also prior art |
| [LESSONS_LEARNED.md](03_innovation_review/LESSONS_LEARNED.md) | Lessons learned |
| [OPEN_RESEARCH_GAPS.md](03_innovation_review/OPEN_RESEARCH_GAPS.md) | Open research gaps |
| [README.md](03_innovation_review/README.md) | Research innovation workspace |
| [REAL_WORLD_PROBLEM.md](03_innovation_review/REAL_WORLD_PROBLEM.md) | The real-world recovery problem |
| [RECOMMENDED_INNOVATION.md](03_innovation_review/RECOMMENDED_INNOVATION.md) | Recommended direction: recovery of completion decisions |
| [RESEARCH_LANDSCAPE.md](03_innovation_review/RESEARCH_LANDSCAPE.md) | Research landscape |
| [RESEARCH_REDIRECTION.md](03_innovation_review/RESEARCH_REDIRECTION.md) | Research redirection |
| [risks/FEASIBILITY_REVIEW.md](03_innovation_review/risks/FEASIBILITY_REVIEW.md) | Independent feasibility and causal-design review |
| [risks/LITERATURE_REVIEW.md](03_innovation_review/risks/LITERATURE_REVIEW.md) | Independent adversarial literature/design review |
| [risks/MECHANISM_REVIEW.md](03_innovation_review/risks/MECHANISM_REVIEW.md) | Independent mechanism review |
| [VALIDATION_STRATEGY.md](03_innovation_review/VALIDATION_STRATEGY.md) | Validation strategy |

## 04_design_extensions

Second investigation, protocol probes, sources and design critiques. Historical research and supporting evidence.

| File | Title or artifact |
|---|---|
| [CANDIDATE_ADDITIONS.md](04_design_extensions/CANDIDATE_ADDITIONS.md) | Candidate additions: comparison before recommendation |
| [CROSS_FIELD_INVENTIONS.md](04_design_extensions/CROSS_FIELD_INVENTIONS.md) | Cross-field inventions and failed translations |
| [CURRENT_THINKING.md](04_design_extensions/CURRENT_THINKING.md) | Current thinking — final research checkpoint |
| [DECISION_LOG.md](04_design_extensions/DECISION_LOG.md) | Decision log |
| [evidence/budget_and_precision.py](04_design_extensions/evidence/budget_and_precision.py) | budget_and_precision.py |
| [evidence/budget_and_precision_results.json](04_design_extensions/evidence/budget_and_precision_results.json) | budget_and_precision_results.json |
| [evidence/PROTOCOL_AUDIT.md](04_design_extensions/evidence/PROTOCOL_AUDIT.md) | Protocol, information, and source audit |
| [evidence/protocol_probe.py](04_design_extensions/evidence/protocol_probe.py) | protocol_probe.py |
| [evidence/protocol_probe_results.json](04_design_extensions/evidence/protocol_probe_results.json) | protocol_probe_results.json |
| [evidence/READ_COVERAGE.md](04_design_extensions/evidence/READ_COVERAGE.md) | Previous-workspace read coverage |
| [evidence/WORKSPACE_VALIDATION.md](04_design_extensions/evidence/WORKSPACE_VALIDATION.md) | Workspace validation |
| [FALSIFICATION_PLAN.md](04_design_extensions/FALSIFICATION_PLAN.md) | Attempt to kill the recommendation |
| [FEASIBILITY_AND_VALUE.md](04_design_extensions/FEASIBILITY_AND_VALUE.md) | Feasibility and scientific value |
| [FINALIST_EXPERIMENTS.md](04_design_extensions/FINALIST_EXPERIMENTS.md) | Minimum decisive experiments |
| [FOUNDATION_ASSESSMENT.md](04_design_extensions/FOUNDATION_ASSESSMENT.md) | Foundation assessment |
| [LESSONS_LEARNED.md](04_design_extensions/LESSONS_LEARNED.md) | Lessons learned |
| [NOVELTY_ADVERSARY.md](04_design_extensions/NOVELTY_ADVERSARY.md) | Hostile review of the finalists |
| [README.md](04_design_extensions/README.md) | Strengthening recovery after distributed LLM work |
| [RECOMMENDED_EXTENSION.md](04_design_extensions/RECOMMENDED_EXTENSION.md) | Recommendation: test what a correction must preserve to make prior work reusable |
| [reviews/COMPLETION_COMPETITOR.md](04_design_extensions/reviews/COMPLETION_COMPETITOR.md) | Independent review of the completion-reopening competitor |
| [reviews/CROSS_FIELD_CANDIDATES.md](04_design_extensions/reviews/CROSS_FIELD_CANDIDATES.md) | Adversarial cross-field candidate review |
| [reviews/FINAL_DESIGN_REVIEW.md](04_design_extensions/reviews/FINAL_DESIGN_REVIEW.md) | Independent final scientific-design review |
| [reviews/STRUCTURE_CANDIDATES.md](04_design_extensions/reviews/STRUCTURE_CANDIDATES.md) | Independent candidate analysis from protocol structure |
| [sources/CROSS_FIELD_SOURCES.md](04_design_extensions/sources/CROSS_FIELD_SOURCES.md) | Cross-field source and search notes |
| [sources/RECENT_AGENT_LITERATURE.md](04_design_extensions/sources/RECENT_AGENT_LITERATURE.md) | Recent agent literature: independent update |
| [sources/ROOT_SEARCH_LEDGER.md](04_design_extensions/sources/ROOT_SEARCH_LEDGER.md) | Root investigation search and source ledger |
| [sources/search_log_recent.md](04_design_extensions/sources/search_log_recent.md) | Recent-agent search and claim-access log |
| [sources/TRANSITION_RECEIPT_NOVELTY.md](04_design_extensions/sources/TRANSITION_RECEIPT_NOVELTY.md) | Novelty attack: historical before-values in a correction receipt |
| [SPECIFICATION_CHANGE_PLAN.md](04_design_extensions/SPECIFICATION_CHANGE_PLAN.md) | Eventual specification changes |
| [UNTAPPED_STRUCTURE.md](04_design_extensions/UNTAPPED_STRUCTURE.md) | Untapped scientific structure in the existing study |
| [UPDATED_RESEARCH_LANDSCAPE.md](04_design_extensions/UPDATED_RESEARCH_LANDSCAPE.md) | Updated research landscape |

## 05_practical_additions

Practical experiment and analysis options considered for the final design. Historical proposals; consult the final specification for adopted scope.

| File | Title or artifact |
|---|---|
| [01_RECOVERY_TRAJECTORIES.md](05_practical_additions/01_RECOVERY_TRAJECTORIES.md) | Addition 01: show how recovery unfolds |
| [02_FAILURE_TAXONOMY.md](05_practical_additions/02_FAILURE_TAXONOMY.md) | Addition 02: explain failures with observable labels and a small casebook |
| [03_COMMUNICATION_AND_INFORMATION_FLOW.md](05_practical_additions/03_COMMUNICATION_AND_INFORMATION_FLOW.md) | Addition 03: connect correction delivery, available evidence, and recovery |
| [04_QUALITY_REUSE_COST.md](05_practical_additions/04_QUALITY_REUSE_COST.md) | Addition 04: make the quality, retained-work, and cost tradeoff visible |
| [05_TASK_STRUCTURE_AND_RECOVERY.md](05_practical_additions/05_TASK_STRUCTURE_AND_RECOVERY.md) | 05 — Explain recovery through task structure |
| [06_RECOVERY_INFORMATION_ATLAS.md](05_practical_additions/06_RECOVERY_INFORMATION_ATLAS.md) | 06 — A small atlas of what retained work contains |
| [07_COMPACT_STATE.md](05_practical_additions/07_COMPACT_STATE.md) | 07 — Keep the last answer, clear the conversation |
| [08_PARTIAL_TEAM_RESETS.md](05_practical_additions/08_PARTIAL_TEAM_RESETS.md) | 08 — Reset two peers and let two keep their history |
| [09_FIRST_ROUND_COMMUNICATION_PAUSE.md](05_practical_additions/09_FIRST_ROUND_COMMUNICATION_PAUSE.md) | 09 — Delay messages produced in the first recovery round |
| [10_DELAYED_RESET.md](05_practical_additions/10_DELAYED_RESET.md) | 10 — Give the team one round, then clear its reasoning |
| [11_HISTORICAL_CHANGE_RECEIPTS.md](05_practical_additions/11_HISTORICAL_CHANGE_RECEIPTS.md) | 11 — Tell the team what changed from the old value to the new one |
| [12_REVISION_TIMING.md](05_practical_additions/12_REVISION_TIMING.md) | 12 — Earlier versus later corrections |
| [13_CHANGE_DIRECTION_AND_SECOND_EDITS.md](05_practical_additions/13_CHANGE_DIRECTION_AND_SECOND_EDITS.md) | 13 — Direction of change |
| [14_DETERMINISTIC_RECOVERY_REFERENCES.md](05_practical_additions/14_DETERMINISTIC_RECOVERY_REFERENCES.md) | 14 — CPU references that explain what the LLM had to do |
| [15_TEAM_SYNCHRONIZATION.md](05_practical_additions/15_TEAM_SYNCHRONIZATION.md) | 15. Does the team recover together? |
| [16_BOUNDARY_POLICY_REPLAY.md](05_practical_additions/16_BOUNDARY_POLICY_REPLAY.md) | 16. Evaluate one practical reset rule without new model runs |
| [17_CONTINUATION_REPEATABILITY.md](05_practical_additions/17_CONTINUATION_REPEATABILITY.md) | 17. A small repeatability check |
| [18_SECOND_REVISION.md](05_practical_additions/18_SECOND_REVISION.md) | 18 — Can the team recover a second time? |
| [README.md](05_practical_additions/README.md) | Practical additions to the recovery thesis |
| [RECOMMENDED_ADDITIONS.md](05_practical_additions/RECOMMENDED_ADDITIONS.md) | Recommended additions: more explanatory depth, one simple extra policy |

## 06_final_design

Final specification preparation plan. Superseded by the root project specification.

| File | Title or artifact |
|---|---|
| [FINAL_PROJECT_SPECIFICATION_PLAN.md](06_final_design/FINAL_PROJECT_SPECIFICATION_PLAN.md) | Final scientific plan: recovery and useful state reuse in distributed LLM teams |

## 07_repository_audit

SILO repository audit and source audit record. Supporting checkout evidence.

| File | Title or artifact |
|---|---|
| [SILO_REPOSITORY_AUDIT.md](07_repository_audit/SILO_REPOSITORY_AUDIT.md) | SILO repository audit |
| [source_audit.json](07_repository_audit/source_audit.json) | source_audit.json |
