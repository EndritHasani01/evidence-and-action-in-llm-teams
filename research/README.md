# Completed research archive

The research phase is complete. Read [the final project specification](../PROJECT_SPECIFICATION.md) first: it governs implementation, evaluation and reporting. These files explain how the design evolved and provide supporting evidence. Earlier instructions, recommendations, budgets and authority labels describe their historical phase; conflicting material is superseded.

## Agent reading order

1. Read the root specification and identify the section relevant to the current task.
2. Read [the final design plan](06_final_design/FINAL_PROJECT_SPECIFICATION_PLAN.md) only for rationale and proposal disposition.
3. For task or runner semantics, read [the SILO audit](07_repository_audit/SILO_REPOSITORY_AUDIT.md) and [the protocol audit](04_design_extensions/evidence/PROTOCOL_AUDIT.md).
4. For scientific justification, read [the updated landscape](04_design_extensions/UPDATED_RESEARCH_LANDSCAPE.md), then the relevant source, review or practical-addition file.
5. Consult earlier innovation, agent context and blueprint files only when tracing an older decision or reproducing historical checks.

## Phase map

| Directory | Contents | Role |
|---|---|---|
| [01_original_blueprint](01_original_blueprint/) | Original support/action blueprint and its executable reference assets | Historical; superseded |
| [02_agent_context](02_agent_context/) | Earlier agent handoff, background, source register and context | Historical; superseded |
| [03_innovation_review](03_innovation_review/) | First innovation investigation, literature, risks and CPU audit | Historical research and supporting evidence |
| [04_design_extensions](04_design_extensions/) | Second investigation, protocol probes, sources and design critiques | Historical research and supporting evidence |
| [05_practical_additions](05_practical_additions/) | Practical experiment and analysis options considered for the final design | Historical proposals; consult the final specification for adopted scope |
| [06_final_design](06_final_design/) | Final specification preparation plan | Superseded by the root project specification |
| [07_repository_audit](07_repository_audit/) | SILO repository audit and source audit record | Supporting checkout evidence |

## Search and iteration

[INDEX.md](INDEX.md) lists every archived file by phase with its title. [manifest.json](manifest.json) provides original and current repository-relative paths, file kinds, phase labels and SHA-256 hashes. Iterate its `files` array in order, filter by `phase` or `kind`, and load only relevant files. All paths in that manifest resolve from the repository root. No duplicate copies of research documents were created.

Useful repository-root searches:

```powershell
rg -n "receipt|historical|retention" research/04_design_extensions research/05_practical_additions
rg -n "BFS|Top-K|scoring" research/07_repository_audit research/03_innovation_review/evidence
```

## Reproducing historical checks

From the repository root:

```powershell
python research/03_innovation_review/evidence/audit_repository.py
python research/03_innovation_review/evidence/recovery_counterexamples.py
python research/04_design_extensions/evidence/protocol_probe.py
python research/04_design_extensions/evidence/budget_and_precision.py
```

These scripts regenerate their adjacent evidence JSON. They are historical CPU probes, not validation of the final experiment. Their reports may include the hash of the current specification when rerun. For the original reference tests, change into `research/01_original_blueprint` and run `python -m unittest discover -s tests`; its dependency list is preserved there.

## Snapshot caveats

Stored evidence JSON and the earlier agent-context manifest retain original snapshot paths, hashes and dates. Use the new manifest for relocation lookup; do not interpret old recorded paths as current navigation. `05_practical_additions/README.md` already referenced an absent `READING_AND_CHECKS.md` before this move; that missing historical artifact is not reconstructed. The existing mistyped change-direction link has been corrected.
