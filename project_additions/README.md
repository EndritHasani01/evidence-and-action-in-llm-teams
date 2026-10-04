# Practical additions to the recovery thesis

Prepared 2026-10-04 under the user's revised objective: maximize useful findings, a clear thesis story and feasibility. Prior-literature novelty is **not a ranking criterion**. PROJECT_SPECIFICATION.md remains the core and is not modified. The v2 recommendation is one option, not a mandate.

Start with [RECOMMENDED_ADDITIONS.md](RECOMMENDED_ADDITIONS.md) for the smallest recommended package. Numbered files are options, **not a checklist to implement in full**. Each explains a question, minimum design, cost, possible outcomes and recommendation.

No main model runs or recovery logs exist yet. “Zero extra inference” means an analysis can use the records the original experiment will produce; it does not mean the results already exist. No implementation or model inference is performed in this planning phase.

Common assumptions: 16 calls per four-peer/four-round branch; original main matrix 5,856 calls for 48 worlds or 4,488 for 36; original pilot 588 calls plus a bounded smoke screen. Every proposal must fit measured timing and the approximately 30 aggregate GPU-hour ceiling. Cost illustrations are not performance forecasts.

The prior v2 workspace was read collectively in full, including its source/review notes, scripts and complete JSON records. [READING_AND_CHECKS.md](READING_AND_CHECKS.md) records coverage and verification. The specification and v2 files are preserved.
