# Retention and revisable execution: additional close work

Inspected 2026-09-30. Primary full text read by HTML and direct text extraction. Findings are not reproduced.

## Reclaim Evaluation

[Primary full text, v1](https://arxiv.org/html/2606.25449v1), 2026-06-24, §§3–5 and limitations.

Studies whether a correction can recover an exact answer after a committed wrong conclusion is compressed into memory. Matched-budget conditions retain either the conclusion or its recomputable source; neutral padding controls length. Hand-built source selection is acknowledged as an oracle, and a one-prompt deployable version is weaker. It also examines iterative memory cascades and source truncation; completeness notices can expose otherwise silent failure. This is close to the existing specification's evidence-versus-reasoning retention contrast. Its correction addresses a prior error, rather than an initially valid world changing after peer collaboration. That distinction supports a generalization study, not a novel principle that evidence preservation enables recovery.

## Revisable by Design / Revision Absorber

[Primary full text, v1](https://arxiv.org/html/2604.23283v1), 2026-04-25, §§3–7.

Models interleaved agent execution and user revisions, separates epistemic and world state, and classifies tool effects by reversibility. Earliest conflicting compensable/irreversible action sets a rollback boundary; compatibility uses an LLM call. StreamBench uses simulated annotated tools and deliberately conflicting interventions. Its structural optimality theorem assumes separability and monotonic costs; it is not a theorem that earliest-suffix rollback minimizes every semantic recovery problem. Its “idempotent” class is defined narrowly as nonmutating actions; conventional idempotent writes can mutate state. The wider lesson is that environment rollback and epistemic recovery are different obligations. An application must preserve the new requirement while undoing only controlled effects.

## 2025 foundation leads

[MemoryAgentBench, arXiv 2507.05257](https://arxiv.org/abs/2507.05257), introduced July 2025; primary abstract and [dataset card](https://huggingface.co/datasets/ai-hyz/MemoryAgentBench) inspected. Incremental multi-turn evaluation includes retrieval, learning, understanding, and forgetting/conflict resolution; this is benchmark precedent, not a collective recovery mechanism.

[Hindsight, arXiv 2512.12818](https://arxiv.org/abs/2512.12818), December 2025; primary abstract inspected. Temporal/entity-aware retention, recall, and reflection separate observed information from beliefs. Relevant memory-engineering baseline, but no full-method claim made here.

These leads complement the directly inspected 2026 recovery mechanisms. Avoid treating benchmark release/version labels or aggregate memory QA scores as evidence that a system repairs consumed collaborative state.
