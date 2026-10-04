# Recovery in distributed LLM teams

A controlled study of how multi-agent teams recover when information used during distributed problem solving is corrected.

The design uses five SILO-derived task families to study retained evidence and computation, historical change information, and how recovering peers affect one another. Shared-prefix revision and no-change continuations provide matched controls.

## Project status

The full SILO repository and revised specification are present. Selected stored task answers have been independently checked on CPU. The new correction protocol, workflow, Qwen3.5/T4 pilot, and main experiments remain future work. No GPU performance or recovery advantage is claimed.

## Start here

- [Project specification](PROJECT_SPECIFICATION.md) is the current source of truth.
- [SILO repository audit](SILO_REPOSITORY_AUDIT.md) records supporting inspection findings.
- [The specification-update plan](FINAL_PROJECT_SPECIFICATION_PLAN.md), research directories, numbered blueprint, `codex_context`, and old configurations preserve the design history. The final specification supersedes their conflicting recommendations; historical support-algebra tests do not validate this experiment.

## Scope

Four peers perform four rounds of collaborative work before an announced factual revision, then receive four recovery rounds. The study targets 60 worlds, with a 40-world resource fallback. The specification defines the retention and complementary team-reset comparisons, focused receipt/prose interventions, two primary estimands, exact evaluation, repetition, and measured feasibility gates.
