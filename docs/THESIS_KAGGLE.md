# Thesis study on Kaggle: operator runbook

This runbook operates the adopted thesis regime `thesis-recovery-v1`
([PROJECT_SPECIFICATION.md §13](../PROJECT_SPECIFICATION.md#13-thesis-regime-thesis-recovery-v1),
annex [thesis-project-specification.md](proposals/thesis-project-specification.md)).
All logic is in `recovery/thesis/`; the notebook
[`notebooks/thesis_kaggle.ipynb`](../notebooks/thesis_kaggle.ipynb) makes one call
per cell. GPU development and main execution each need your explicit
authorization; running the notebook in a GPU scope is that act.

## Before the first session

1. Commit and push the implementation to
   `github.com/EndritHasani01/evidence-and-action-in-llm-teams`. Note the full
   40-character commit SHA. The notebook downloads exactly that commit.
   (Fallback without GitHub: `python scripts/build_thesis_source.py --commit SHA`
   and attach the resulting `thesis-source-<sha12>.zip` as a private Kaggle dataset.)
2. Optional but recommended: create a **private** Hugging Face dataset
   (for example `your-name/thesis-checkpoints`) and a write token. In Kaggle,
   *Add-ons → Secrets*, add it as `HF_TOKEN` and attach it to the notebook. The
   code refuses to mirror to a public repository.
3. Create a Kaggle notebook from `notebooks/thesis_kaggle.ipynb`. Settings:
   Internet **on**; accelerator **GPU T4 x2** for GPU scopes (none for `cpu` or
   `rehearsal`). After the first run, pin *Environment* to the original image.

## Cell 1 settings

| Setting | Meaning |
|---|---|
| `SOURCE_COMMIT` | The pushed commit to run. Every session of one study must use the same commit |
| `STUDY_ID` | `thesis-recovery-v1`; rehearsal automatically uses `thesis-recovery-v1-rehearsal` |
| `SCOPE` | `cpu`, `rehearsal`, `development` or `main` (what may run in this session) |
| `START_NEW_STUDY` | `True` only for the very first run of a study; otherwise `False` |
| `MAIN_AUTHORIZATION` | The development gate-report ID (`dev-...`) once you authorize main |
| `SESSION_HOURS` | Hours this session may use from now. `11` for a fresh 12-hour GPU session; less if time has already passed |
| `CHECKPOINT_REPO` | Private HF dataset for the off-session mirror, or empty |

## Sessions in order

| Session | Settings | What happens | Expected time |
|---|---|---|---|
| A. CPU rehearsal | `SCOPE="rehearsal"`, `START_NEW_STUDY=True`, no GPU | Whole pipeline with a scripted model on 2+2 worlds; checkpoints and mirror | under 30 min |
| B. Restore drill | Same, `START_NEW_STUDY=False`, a new session | Cell 3 restores the newest rehearsal checkpoint; no work repeats; the report is identical | under 30 min |
| C. Development | `SCOPE="development"`, `START_NEW_STUDY=True`, T4 x2 | Downloads each model, readiness, 16 development worlds per model (at most 704 calls each), gate report | 2–3.5 h |
| D+. Main | `SCOPE="main"`, `MAIN_AUTHORIZATION="dev-..."`, T4 x2, **Save & Run All** | Freeze (once), then main worlds until done or the cutoff | Qwen about 7.5 h expected, 10.2 h worst case at the measured rate, so it may need a second session; Granite measured in C |
| Final | Any scope, or locally | Report from the newest checkpoint | minutes |

After session C, read the gate report printed by cell 5 (also in
`receipts/gate-report.json`). Paste its ID into `MAIN_AUTHORIZATION` only if you
authorize main. If one model failed its gates, main runs the other alone; if both
failed, there is no main.

Before and after session C, note the GPU quota Kaggle shows, to learn how it
charges T4 x2.

## What the cells do

1. **Settings and source:** downloads the pinned source (verifying the archive's
   commit header), records the session deadline.
2. **Install:** pinned virtual environment from `configs/i01-runtime.lock` (about 3 minutes).
3. **Open:** restores the newest checkpoint from attached inputs or the mirror,
   or reopens the local study, or creates it (first run only).
4. **CPU checks:** manifest, input separation, protocol, analysis and checkpoint
   checks, and the token-capacity proof with the real tokenizers.
5. **Development** · 6. **Freeze** · 7. **Main**: skip outside their scopes.
8. **Report:** rebuilt from the canonical store; estimates appear only when main
   is complete (or after `declare-stopped`).
9. **Finish:** final checkpoint, mirror upload, download links, session closed.

Every world runs one natural prefix, then six isolated continuations from it
(retain or clear × answer-changing revision `V`, answer-preserving change `P`
or no change `N`: `RV CV RP CP RN CN`), then two scalar controls: at most 44
calls per world and model.

Progress lines appear every minute and after every world. During main,
outcomes are hidden: you see terminal reasons (B both submitted, H horizon,
W deadlock), call counts, contingency and GPU-hours, not success rates.

## Saving and restoring

* Every call's raw reply is saved before its effects. A checkpoint ZIP is written
  every 20 minutes, at every stage end and after every cell, under
  `/kaggle/working/thesis/<STUDY_ID>/checkpoints/` (newest two kept).
* Off-session copies: the private mirror (automatic), or the output of a
  completed **Save & Run All** version (attach it as input next time), or a
  download of the newest checkpoint (attach it as a private dataset).
* Cell 3 always restores the **highest** checkpoint sequence it can see. It
  refuses two different checkpoints with one sequence, a local study older than
  an attached checkpoint, and a checkpoint from another commit.
* After a lost session, calls that were in flight are retried once with the
  identical request and seed; work done after the last checkpoint is recomputed
  identically. Nothing is selected by outcome.

## When something stops

| Message | Meaning and action |
|---|---|
| `skipped: scope ...` | The cell is outside `SCOPE`; nothing to do |
| `time: dispatch cutoff reached` | Session time is nearly used; run again in a new session |
| `CPU checks have not passed` | Run cell 4 first (Run All does) |
| `MAIN_AUTHORIZATION ... does not match` | Paste the exact gate-report ID |
| `newer checkpoint ... exists` | A newer checkpoint is attached; move the old local run directory aside |
| `different source/config/inputs` | `SOURCE_COMMIT` differs from the study's; use the original commit |
| `another process ... owns this study` | A stage is still running; wait, or call `nb.stop_running()` |
| `integrity: ...` or `ceiling ... reached` | Stop and ask; nothing is retried automatically |

Never delete checkpoints or the run directory to "start over"; a new study needs
a new `STUDY_ID` and its own decision.

## Local commands (CPU)

Unzip a downloaded checkpoint into an empty folder `DIR`, then (read-only, no
model, no network):

```text
python -m recovery.thesis report --run DIR --out DIR/reports
python -m recovery.thesis show   --run DIR --model qwen --world main-000 --cell RV
python -m recovery.thesis status --run DIR --study thesis-recovery-v1 --scope cpu --source-commit SHA
python -m unittest tests.test_thesis_worlds tests.test_thesis_protocol tests.test_thesis_models \
  tests.test_thesis_analysis tests.test_thesis_checkpoint tests.test_thesis_run tests.test_thesis_notebook
```
