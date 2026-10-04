# User context and priorities

## Confirmed on 24 September 2026

| Topic | User answer | Consequence |
|---|---|---|
| Academic scope | Two courses, potentially thesis | Serve the combined IIS + ABS project first; make a credible thesis extension possible. Do not assume a thesis-only deliverable or institution-specific rubric. |
| Compute | Two T4s, 30 GPU-hours | Retain the conservative aggregate GPU-hour planning constraint until real quota accounting and throughput are checked. |
| Current deliverable | Another folder to place inside recovery_blueprint | Prepare context and evidence. Do not implement the experiment or present a finished project specification as already approved. |

## Preferences visible in the conversation

The user wants research on coordination, collaboration, vulnerabilities, and optimization of teamwork, with a defensible scientific contribution. They questioned why a custom event-based runner was proposed when LangGraph exists, requested in-depth research into current tools and innovations, and asked for a future single source of truth covering requirements and technology choices.

Interpret these preferences as follows:

- Reuse established frameworks and benchmarks where they satisfy the actual experiment.
- Justify every dependency by a requirement; novelty of a tool is not a reason to adopt it.
- Assess maintenance, real usage, compatibility, and operational complexity. Popularity is useful evidence, not proof of correctness or a guarantee against bugs.
- Prefer empirical scientific value over naming a new framework or building an elaborate demo.
- Explain whether any proposed change affects only infrastructure, the experimental design, the estimand, or the broader thesis direction.
- Keep the original thesis/question available for comparison. The conversation does not authorize silently replacing the thesis with a tooling project.

The preference for reuse supports evaluating LangGraph first. It does not establish an unconditional requirement to adopt LangGraph, nor permission to alter the experiment to match its abstractions.

## Thesis continuity

The blueprint's broad identity is **What remains valid after a correction?** Its narrower question examines whether estimated support records preserve useful state while changing actions bound to superseded evidence, even when an intermediate conclusion remains true.

The folder contains no independently verified earlier approved thesis text beyond the supplied materials. Do not reconstruct a supposedly original question from memory. When comparing versions, quote the actual wording and identify its source. Retaining the title while narrowing an estimand can be legitimate; it must be explained explicitly.

## Information not supplied

Current deadline, course grading rubrics, supervisor feedback/approval, mandatory thesis format, required programming language, access to extra hardware, confirmed Kaggle quota semantics, and preferred publication venue are unknown. Do not invent these or make every unknown a blocker. Request only answers that materially change scope or admission to the main experiment.

## Model preference update

The user explicitly prefers **Qwen3.5**, superseding the inherited Qwen3-4B primary-model choice. Earlier project context used Qwen3.5-9B. The recommended primary candidate is **Qwen/Qwen3.5-9B with 4-bit quantization**, conditional on actual T4 compatibility, capability and budget gates; **Qwen/Qwen3.5-4B** is the lower-memory fallback. The family preference is confirmed; the size/quantization recommendation remains a pilot decision.
