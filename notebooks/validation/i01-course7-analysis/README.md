# Course-7 derived analysis evidence

The original inputs are `notebooks/run/course-7-working/latest.zip` and
`multi-agents-course-v5nb.ipynb` in the same directory. They remain unchanged.
This folder contains derived read-only analysis, not another canonical store.

Reproduce from the repository root with Python 3.11 or newer:

```powershell
python scripts/audit_i01_course7.py
```

The audit uses the standard library and existing read-only I-01 modules. It
extracts the ZIP into a temporary directory, verifies its inventory and SQLite
integrity, checks source/release/wheel identities, regenerates the fixed worlds,
replays every team call and control, and reconstructs the saved analysis. It
independently rebuilds the paired outcome and effort bootstrap draws. It does
not import a model, instantiate an inference worker, retokenize prompts, or run
an experiment. The current scientific-source hashes must match the supplied
run; if they drift, use the matching archived source to audit that run.

- `audit.json`: input hashes, executed checks, summary, world diagnostics,
  costs, notebook cell timestamps, physical memory observations and closure.
- `main-worlds.csv`: all twenty worlds, exact submissions and explicitly
  descriptive diagnostics; no world selection or replacement.
- `team-call-audit.csv`: all 206 replayed team calls with exact visible replies,
  protocol reasons, seeds, device slots, token counts and recorded effort.
- `main-costs.csv`: phase totals, means and medians over twenty main worlds.
- `figures/`: three original PNG/SVG pairs copied byte for byte from the
  checkpoint. `termination-coverage` covers all 107 scientific episodes, including
  qualification controls and pilots; it is not a main-only chart. The recovery
  cost plot uses positions 1–20 for IDs `main-00`–`main-19`.

The [report-ready analysis](../../../docs/validation/i01-course-7-results-analysis.md)
defines denominators, distinguishes failed from missing outcomes, separates
software success from model performance, and documents limits on causal claims.
Canonical human annotations remain empty; this retrospective analysis does not
retroactively certify operator review or successful checkpoint restoration.
