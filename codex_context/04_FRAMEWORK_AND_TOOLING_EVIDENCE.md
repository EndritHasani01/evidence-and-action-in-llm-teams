# Framework and tooling evidence

This is a selection brief, not a final dependency lock. Sources [T1–T12] are in the register. Verify versions again when the project specification is written.

## Selection rule

Every selected dependency needs a named requirement, evidence it meets that requirement, compatibility evidence, maintenance/license status, added complexity, and a fallback. Prefer the smallest coherent stack. Distinguish popularity from suitability and documentation from tested behavior. No framework is guaranteed bug-free.

| Layer | Candidate and status | Reason / decision boundary |
|---|---|---|
| Experimental orchestration | **Evaluate LangGraph first** [T1] | Established checkpoint/time-travel abstractions match frozen-prefix branches. Adoption depends on isolation and call-budget tests below. |
| Alternative orchestration | Microsoft Agent Framework [T2] | Workflow checkpoints capture executor/shared state and pending work at boundaries. Compare only if it provides a concrete advantage or LangGraph fails a requirement. |
| Typed agent layer | PydanticAI [T3] | Relevant typed graph/durability alternative; avoid stacking another orchestration lifecycle on LangGraph without need. Pydantic schemas alone are a separate choice. |
| Local model execution | Transformers baseline; vLLM measured candidate [T4–T6] | Baseline follows blueprint. Faster serving must earn adoption through compatible outputs and measured end-to-end cost on the actual T4 environment. |
| Experiment harness | Existing bounded project harness; Inspect optional [T7] | Inspect provides evaluation structures and logs, but does not remove the custom support evaluator. Choose one owner for episode lifecycle. |
| Canonical records | Explicit versioned records and append-only experiment logs | Required by the study. Framework execution traces cannot substitute for semantic evidence and action validity. |
| Inspection UI | Phoenix optional [T8] | Useful tracing if debugging requires it. Not needed to establish the primary outcome; keep canonical data independently readable. |
| Graph/analysis helpers | NetworkX, DuckDB only if justified [T9–T10] | Reachability does not compute alternative sufficient support. Parquet/SQL analysis may help later; small JSON datasets do not require a database service. |

## LangGraph semantic acceptance test

Official docs distinguish thread checkpoint state from cross-thread stores and describe replay/fork behavior. A branch can rerun downstream calls; `update_state` uses reducers and routing context. Therefore checkpoints alone do not establish experimental equivalence.

Before adoption, verify with deterministic mock agents:

1. All scientifically relevant state is captured: source versions, owned ledgers, messages, proposed actions, attempt history, and policy-visible records.
2. The parent prefix remains byte/hash-stable after every policy branch; branches share exactly the intended realized prefix.
3. External stores, caches, files, and tool state cannot leak mutations across branches. Test deliberate cross-branch contamination.
4. The freeze point has no unaccounted pending messages or background tasks. Resume produces the prescribed event order.
5. Restart/crash recovery produces no duplicated committed action or hidden extra model call. Record attempts separately from applied effects.
6. Retries, reducers, interrupts, and checkpoint history do not expose oracle labels or silently expand the fixed recovery allowance.
7. A small policy fixture produces the same observable state transitions as the formal contract, including conclusion survival plus invalid bound action.

Use local checkpoint storage appropriate to the pilot. The choice between in-memory and persistent storage depends on required restart behavior. If a requirement fails, first evaluate a small adapter. A custom runner becomes justified only by a documented unmet need, with maintenance cost made explicit.

## Hardware and serving developments worth evaluating

Current vLLM GPU documentation explicitly includes T4-class capability. Its current quantization matrix differs from older blanket assumptions about unsupported kernels. Structured-output APIs also changed: legacy `guided_json` is not the current interface; use the installed version's documented API. These developments justify a small feasibility check, not a preselected backend.

Constrained generation can change the measured protocol. Decide whether it is part of every matched condition, record invalid/truncated outputs, and freeze the method before confirmation. Faster throughput is irrelevant if semantic comparability or reproducibility is lost.

## Adoption and excluded complexity

Repository activity, releases, documented integrations, and reproducible examples are stronger selection evidence than star counts alone. There is no verified cross-framework production-usage ranking in this research. Microsoft's official AutoGen update signals a shift toward Agent Framework [T11]; old popularity is insufficient for selecting a new dependency.

The present task does not establish a need for vector search, a graph database, Redis, Kubernetes, agent-to-agent protocols, MCP servers, cloud orchestration, training, or paid APIs. Reconsider only if a concrete experimental requirement appears. Innovations are research candidates, not a shopping list.
