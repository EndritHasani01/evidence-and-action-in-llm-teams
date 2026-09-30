# Recovery after distributed reasoning

A controlled study of how multi-agent teams recover when information used during distributed problem solving is corrected.

The design uses six SILO-derived tasks to separate correction delivery, reuse of gathered evidence, and retention of prior reasoning. Matched no-change continuations distinguish correction-specific effects from general reset benefits.

## Project status

The full SILO repository and revised specification are present. Selected stored task answers have been independently checked on CPU. The new correction protocol, workflow, Qwen3.5/T4 pilot, and main experiments remain future work. No GPU performance or recovery advantage is claimed.

## Start here

- [Project specification](PROJECT_SPECIFICATION.md) is the current source of truth.
- [SILO repository audit](SILO_REPOSITORY_AUDIT.md) records supporting inspection findings.
- The numbered blueprint, `codex_context`, old configurations, and support-algebra tests are historical material; they do not define or validate the revised experiment.

## Scope

Four peers first solve a distributed task, then continue from matched checkpoints under four recovery conditions after an announced factual revision. The specification defines the comparisons, exact evaluation, pilot, and 30 aggregate GPU-hour ceiling.
