# Support-Aware Action Repair

A controlled study of whether stateful LLM teams can preserve still-valid conclusions while repairing concrete actions that depend on superseded evidence.

The research design tests alternative evidential support and witness-bound actions after one factual correction. It uses deterministic task semantics and evaluation, with LangGraph and local SQLite checkpoints for execution.

## Project status

The specification and reference support algebra are present. The task generators, agent workflow, inference pilot, main experiments, and empirical results remain to be implemented or run. No model performance or recovery advantage is claimed yet.

## Start here

- [Project specification](PROJECT_SPECIFICATION.md) is the current source of truth.
- [Start here](00_START_HERE.md) gives the blueprint reading order and background.
- Run the existing reference tests with `python -m unittest discover -s tests -v`.

## Scope

The planned study focuses on alternative support × action binding in a three-agent team after a single diagnosed factual update. See the specification for the frozen design, budget gates, controls, and limitations.
