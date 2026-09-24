# Context companion for the recovery blueprint

Prepared 24 September 2026. Place this entire `codex_context/` folder inside `recovery_blueprint/`.

## Purpose

Give a future Codex session the user context, updated evidence, corrections, and decision criteria needed to produce one authoritative `PROJECT_SPECIFICATION.md`. This folder is research input, not that specification and not a new implementation mandate. No experiments were run to produce this companion.

## Read in this order

1. `01_USER_CONTEXT_AND_PRIORITIES.md` — confirmed intent and boundaries.
2. The parent blueprint's `00_START_HERE.md`, `02_research_contract.md`, and `12_pilot_and_decision_gates.md`.
3. `02_BLUEPRINT_AUDIT_AND_CORRECTIONS.md` — what to retain and reconsider.
4. `03_RESEARCH_AND_NOVELTY_UPDATE.md` and `04_FRAMEWORK_AND_TOOLING_EVIDENCE.md`.
5. `05_COMPUTE_AND_PILOT_CONTEXT.md`, `06_SCIENTIFIC_DESIGN_REVIEW.md`, and `07_OPEN_DECISIONS_AND_ACCEPTANCE_GATES.md`.
6. `08_CODEX_HANDOFF.md` — the goal and process for writing the specification.
7. `09_SOURCE_REGISTER.md` and relevant parent files; use `background/` selectively.

## Authority and uncertainty

- Current explicit user instructions and confirmed answers take precedence.
- The parent blueprint remains the detailed design baseline. This companion identifies corrections and proposals; a recommendation here does not silently supersede every corresponding requirement there.
- Resolve conflicts explicitly in the future specification with a decision, reason, source, and affected requirement IDs.
- Recent primary sources outrank older assistant summaries for external facts. Neither determines the user's preferences.
- Separate confirmed requirements, inherited design choices, evidence-backed recommendations, untested engineering assumptions, and unresolved decisions.
- Preserve the original broad thesis identity while testing whether the narrower question is feasible and distinct. Changing a framework does not by itself change the research question.

## Contents and evidence limits

The ten numbered Markdown files provide the curated context. `context_facts.json` supplies machine-readable statuses. `manifest.json` records integrity hashes and the original ZIP identity. Four unchanged background reports provide older literature leads; their claims require verification.

Research access date: 2026-09-24. Relevant full-text sections of MemTX and REVISE are now accessible. One close OpenReview submission remains inaccessible. Documentation review does not establish runtime compatibility or experimental results. Hardware throughput, exact framework versions, model revisions, account quota accounting, and final novelty remain open.

The original ZIP is not included or modified. Its 34 files are still needed alongside this folder. No paid services, accounts, credentials, or full paper copies are included.

## Model amendment

The user now prefers Qwen3.5. Use **Qwen3.5-9B, 4-bit, as the preferred pilot candidate**, with Qwen3.5-4B as the fallback. This supersedes the parent blueprint's Qwen3-4B selection. See `05_COMPUTE_AND_PILOT_CONTEXT.md`; old GPU-hour estimates are historical and must be recalculated.
