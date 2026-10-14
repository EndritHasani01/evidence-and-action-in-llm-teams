# Evidence map for the v2 redesign

**SUPPORTING NOTES — PROPOSED, NOT APPROVED OR IMPLEMENTED**

This is an index to evidence inspected for the [14 October 2026 proposal](../silo-bench-lean-redesign-v2.md), particularly Sections 2, 5, and 11. It does not report a new experiment. Findings below retain the limits of the original inspection; linked files and upstream repositories may subsequently change.

## Authority and implementation evidence

| Question | Best starting point | Interpretation boundary |
|---|---|---|
| What currently governs the science? | [Specification](../../../PROJECT_SPECIFICATION.md), [operating contract](../../../AGENTS.md) | Existing normative requirements; v2 is not adopted |
| What work remains, and what was last handed off? | [Implementation plan](../../IMPLEMENTATION_PLAN.md), especially the living handoff | Read current entries; old status summaries may lag |
| Why were isolation and persistence designed this way? | [Technical synthesis](../../implementation-research/SYNTHESIS.md), [state and replay investigation](../../implementation-research/state-and-replay.md) | Technical evidence, not additional scientific authority |
| What has CPU validation established? | [Course CPU/report gate](../../validation/course-m4-report-and-cpu-gate.md), [durable-worker checks](../../validation/course-m3-durable-workers-and-failures.md) | Evidence for the tested implementation, not the proposed lifecycle or model competence |
| What does the implementation actually assume? | [Architecture handoff](architecture-handoff.md) and its module links | Inspect code before deciding reuse; existing tests do not prove compatibility |

## GPU evidence and limits

Start with the [final-online-6 analysis](../../validation/course-kaggle-final-online-6-analysis.md), its [machine-readable receipt](../../../notebooks/validation/course-kaggle/final-online-6-analysis.json), and the [preserved submission](../../../notebooks/run/final-online-6/). The [repair proposal](../../validation/course-kaggle-final-online-6-proposal.md) describes possible operational changes; it is not proof they ran successfully.

| Recorded finding | Consequence for redesign | Avoid this inference |
|---|---|---|
| Latest 9B ordinary diagnostics: 11/21 valid, eight length-ended malformed outputs, two prose-cap violations | Short, simpler actions deserve qualification | Every error was formatting, or the redesigned interface will necessarily work |
| Three latest full-information controls were wrong | Capability/task interpretation is an independent concern | Three cases estimate general 9B accuracy |
| Many ordinary prompts lacked complete evidence | Their aggregate exact-answer rate is not a clean capability score | Treating 0/21 exact as 21 fully informed mathematical failures |
| 9B actually loaded and generated on both T4s | Reuse the demonstrated loading path as a starting point | Thinking mode or the new context envelope is qualified |
| Full-envelope probe: 110,416 input tokens, 256 output tokens, 394.043 seconds, minimum free memory 16.813 MiB | The old envelope failed the 1.5 GiB headroom gate | Short-context 9B cannot fit, or successful generation means the gate passed |
| Latest 4B fallback stopped at metadata validation | A software defect prevented that fallback from reaching inference | It established a new 4B hardware or capability result |
| Canonical preparation history is 45 attempts; a derived total of 67 counted backups | Preserve physical-attempt identity and derive accounting from canonical records | Counting copied databases as additional experiments |
| No accepted pilot, freeze, or main execution in the latest run | Main outcomes remain unknown | Treating diagnostic or CPU outcomes as empirical treatment results |

The earlier [4B diagnostic account](../../validation/course-kaggle-final-online-4-proposal.md) and [saved analysis](../../../notebooks/validation/course-kaggle/final-online-4-analysis.json) matter too: two of 21 ordinary replies were valid, and both were wrong. Those replies were reused in later repair submissions. “No new 4B calls in final-online-6” does not mean “4B was never tested.”

The latest fallback compared tensor-payload bytes, `9,319,737,856`, with whole-file bytes, `9,319,828,096`; the `90,240`-byte difference explains that metadata refusal. This is relevant only if that path is reused. The proposal does not authorize repairing it now or adding a fallback model.

## SILO-BENCH source provenance

Primary references are the [original paper](https://aclanthology.org/2026.acl-long.1354/) and [released source pinned to the inspected commit](https://github.com/jwyjohn/acl26-silo-bench/tree/e74127782ed1c42fff474249961f022c063d76f2). The inspected upstream `master` head was `e74127782ed1c42fff474249961f022c063d76f2`, timestamped 12 April 2026. This is a dated source identity, not a claim about today's upstream head.

Seven vendored files were compared with upstream after CRLF/LF normalization during the proposal review:

- [Paradigm I generator](../../../acl26-silo-bench/benchmark_generator/paradigm_i.py), [Paradigm II generator](../../../acl26-silo-bench/benchmark_generator/paradigm_ii.py), [Paradigm III generator](../../../acl26-silo-bench/benchmark_generator/paradigm_iii.py).
- [Execution engine](../../../acl26-silo-bench/src/engine.py), [message tools](../../../acl26-silo-bench/src/msg/tools.py), [metrics](../../../acl26-silo-bench/src/utils/metrics.py), [LLM access](../../../acl26-silo-bench/src/utils/llm.py).

Correspondence for these files is not a whole-checkout provenance guarantee. The vendored benchmark remains reference material, not the authority for this repository's execution or scoring.

### Findings that affect the scientific choice

| Verified benchmark property | Why it matters |
|---|---|
| Native two-agent I-08 has 30 integers per shard from `0..29`; each agent reports union cardinality | Authentic task, manageable scalar output, exact oracle, meaningful overlap |
| III-26 performs the same union operation with shuffling | Adding it would not provide a substantially different mathematical family |
| Native submission permanently deactivates a peer | Unsuitable to copy unchanged when completed work must reopen after revisions |
| Native messaging has explicit receive/tool timing and round visibility | A recovery extension must document altered inbox and turn semantics |
| Native API retry behavior is unbounded | It cannot supply an auditable 500-attempt ceiling unchanged |
| Published model results concern much larger models and aggregate settings | No direct evidence that 9B solves native-size I-08 under six turns |

For all 30 tasks and the limits of benchmark performance tables, use proposal Section 5 rather than inferring suitability from task names. In particular, mathematical simplicity, model attainability, and sensitivity to historical work are separate questions.

## Checks completed during the proposal review

The complete proposal records these read-only checks: recomputation of all six released I-08 scales; verification of its worked example and insufficiency counterexample; verification of ten latest submission-file hashes and resume-archive CRC; and in-memory integrity checks of the two canonical hardware databases, containing 20 and two attempts. Only an in-memory SQLite header was adapted for deserialization; archived bytes were unchanged. Budget and runtime arithmetic were also independently checked.

These are inspection findings, not a newly saved comprehensive test receipt. A future session may reproduce a check when it is consequential; it should not claim it reran the checks merely by reading this document. No GPU call was part of that review.

## Assumptions still requiring evidence

| Proposed assumption | Evidence needed later |
|---|---|
| 9B can solve I-08 reliably | Bounded, native-size full-information qualification |
| Six total turns permit substantive collaboration and recovery | Scripted attainability plus complete model pilot traces |
| Retained histories contain useful intermediate work | Actual prefix transcripts, not injected summaries |
| 8,192 input tokens cover permitted views | Native-tokenizer bound for the adopted renderer and action limits |
| Thinking fits and is affordable | Selected-mode envelope checks and measured output lengths/latency |
| 12 worlds are informative | Actual paired outcomes with uncertainty; no advance power guarantee |
| The study fits available Kaggle resources | Current allocation evidence and measured forecast; GPU-hour examples are sensitivities |

The [scientific review agenda](scientific-review.md) explains how these uncertainties could change the decision to proceed.
