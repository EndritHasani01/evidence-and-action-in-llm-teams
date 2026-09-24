# Working research plan

Version: 2026-09-20. Scope: an authoritative scientific and engineering specification, with a tested symbolic reference core; no claim that GPU experiments have been run.

## Plan established before conclusions

1. Re-read the selected direction and the relevant accumulated research. Verify current primary papers and actual public code, prioritizing close recovery, memory, and provenance work.
2. Remove occupied novelty claims. Define one falsifiable interaction question, distinguish evidential validity from action validity, and specify the experimental estimands before choosing the runtime.
3. Select the scientific foundation. Audit what SILO supplies and what a new recovery extension must implement. Compare with newer memory/recovery code.
4. Fix the formal semantics, world generator, frozen-prefix protocol, policies, information boundaries, and exact grading rules.
5. Write the RRS, interfaces, schemas, package layout, state machines, prompts, orchestration, and reproducibility contracts.
6. Derive an exact run matrix and token budget. Define capability, throughput, novelty, and effect-identification gates before confirmation.
7. Implement a small CPU reference for support semantics and run nontrivial invariant tests. Validate schema examples, run-count arithmetic, and document consistency.
8. Deliver linked specifications, machine-readable contracts/configs, implementation sequence, pilot instructions, result templates, and an archive.

## Evidence-led decisions

- The earlier proposal's broad novelty boundary is too optimistic. Selective rollback that preserves independent support is already directly studied in August 2026 work.
- Further current work covers incomplete provenance, transaction-style belief commits, and online workflow revisions. The thesis must be an explanatory study of representation and distributed state, not a claim to invent dependency repair.
- Logged exposure, declared citation, estimated evidential justification, and evaluator-known justification are separate objects. None is automatically a faithful account of a model's internal computation.
- The old 9,760-call budget assumed 100 output tokens per call. It is superseded: realistic structured outputs and extraction require a new budget.
- New documents will state all remaining literature-access limitations explicitly. Absence from search is not proof of novelty.

## Completion record

All eight planning/delivery steps are complete. Seventeen linked specification documents, executable contracts and support reference, five examples, a matrix config, source audit and cost forecast are supplied. The 15 reference tests passed, including 2,260 comparisons with an independent exhaustive oracle. The final audit also resolved mismatched seeds, transfer evidence access, action-mode instructions, priority versus feasibility, and build-order dependencies. GPU measurements, the full runtime and confirmatory experiments remain future work under the explicit gates. This completion record concerns the blueprint, not empirical thesis findings.
