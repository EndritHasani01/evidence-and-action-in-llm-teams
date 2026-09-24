# Open decisions and acceptance gates

These entries distinguish missing user information from research and engineering work Codex can do autonomously. Do not repeatedly ask the user to decide routine implementation details.

| ID | Decision / unknown | Next evidence | Blocks |
|---|---|---|---|
| D01 | Exact overlap with the OpenReview rollback-family paper | Obtain legitimate full text; complete the comparison matrix | Final novelty claim and confirmatory admission; not all development |
| D02 | LangGraph versus alternative/minimal runner | Mock branch, restart, isolation, and call-accounting tests | Runtime selection |
| D03 | Transformers versus vLLM | Small matched actual-T4 smoke test and cost forecast | Backend lock and compute admission |
| D04 | Model/revision and output enforcement | Capability, memory, validity, template and license checks | Reproducible pilot/confirmation |
| D05 | Adequate precision under available compute | Cluster-aware simulations over plausible variance/correlation ranges | Claim strength and confirmatory sample size |
| D06 | Natural error / ceiling behavior | Disjoint pilot trajectories and support measurements | Continue, negative study, or declared pivot |
| D07 | Numeric transfer evaluator | Independent finite-domain cross-checks | Transfer inference, not core symbolic work |
| D08 | Repository reuse and license compatibility | Exact pinned source and license review | Vendoring/importing relevant code |
| D09 | Deadline, rubric, supervisor constraints | Ask user only when scheduling or scope depends on them | Course-specific acceptance and thesis approval |
| D10 | Real platform quota semantics and balance | User account/environment observation | Final aggregate-budget admission |

## Required decision record

For each resolved item: date; decision; alternatives considered; requirement served; evidence and version; test outcome if applicable; cost; remaining limitation; fallback; and what would reopen it. Mark proposals as proposals until supported. Do not create false “approved” decisions on behalf of the user or supervisor.

## Gates in order

1. **Specification consistency:** one meaning for claims, action binding, support, valid completion, and budget units across documents and schemas.
2. **Symbolic correctness:** independent evaluator agreement and task transitions match the declared semantics.
3. **Runtime isolation:** identical parent prefixes, branch separation, no leakage, correct retries and attempts.
4. **Capability and serving:** inherited pilot gates and actual device constraints pass.
5. **Interpretability and precision:** failures are not dominated by basic task inability; the planned analysis can resolve a meaningful question.
6. **Novelty and registration:** close-paper comparison complete or explicitly justified replication framing, with frozen experiment and analysis.
7. **Compute admission:** measured conservative forecast leaves the required reserve before confirmation.

Failure is a decision input. It can justify a fix, smaller scope, negative-result framing, new pilot, or abandonment of this formulation. It is not permission to search indefinitely for settings that make the proposed policy win.
