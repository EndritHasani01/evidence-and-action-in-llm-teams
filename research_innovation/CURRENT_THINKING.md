# Current thinking

## Initial state — 2026-09-30

The current specification proposes a controlled state-retention experiment rather than a new recovery algorithm. Its useful foundations are matched pre-change checkpoints, source/derived-state separation, no-change controls, exact task outcomes, and a bounded compute budget. These are starting constraints to examine, not conclusions to defend.

The practical question is how expensive distributed work can survive an authoritative change without obsolete work retaining unjustified influence. Recorded dependencies are potentially incomplete; simply deleting known descendants may therefore provide false assurance. Conversely, resetting all reasoning destroys accumulated work and may discard valid alternative routes.

No candidate is selected. Investigation streams: (1) fresh repository inspection and feasibility; (2) verification and adversarial reading of recent agent recovery/memory work; (3) adjacent systems ideas; (4) first-principles candidate generation and causal study design.

Next: establish source trust, enumerate actual runtime state channels, identify what prior work already solves, and compare genuinely different candidate mechanisms before recommending one.
