# Thesis study on Kaggle: operator runbook

This runbook operates the adopted thesis regime `thesis-recovery-v1`
([PROJECT_SPECIFICATION.md §13](../PROJECT_SPECIFICATION.md#13-thesis-regime-thesis-recovery-v1),
annex [thesis-project-specification.md](proposals/thesis-project-specification.md)):
64 main and 16 development worlds, six continuations per world, Qwen3.5-9B and
Granite 4.2-8B on Kaggle T4 x2. All logic is in `recovery/thesis/`; the notebook
[`notebooks/thesis_kaggle.ipynb`](../notebooks/thesis_kaggle.ipynb) makes one call
per cell. GPU development and main execution each need your explicit
authorization; running the notebook in a GPU scope is that act.

## Before the first session (once)

1. **Commit and push** the implementation to
   `github.com/EndritHasani01/evidence-and-action-in-llm-teams` and note the full
   40-character commit SHA. Every session of the study must use that same commit.
   If `notebooks/thesis_kaggle.ipynb` is open in an editor, close it without saving
   and run `python scripts/build_thesis_notebook.py` before committing, so the
   committed notebook equals the builder output (a test checks this).
   Fallback without GitHub: `python scripts/build_thesis_source.py --commit SHA`
   writes `thesis-source-<sha12>.zip` with the committed bytes; attach it as a
   private Kaggle dataset.
2. **Checkpoint mirror (strongly recommended).** Create a **private** Hugging Face
   dataset, for example `your-name/thesis-checkpoints`, and a write token. In
   Kaggle, *Add-ons → Secrets*, add the token as `HF_TOKEN` and attach it to the
   notebook. Every checkpoint is then copied off Kaggle and verified, and the next
   session restores from it automatically. The code refuses a public repository.
3. **Kaggle account and notebook.** Phone verification enables Internet. Create a
   notebook from `notebooks/thesis_kaggle.ipynb`; turn Internet **on**. After the
   first run, pin *Environment* to the original image: the pinned packages need
   Python 3.13.

## Cell 1 settings

| Setting | Meaning |
|---|---|
| `SOURCE_COMMIT` | The pushed commit, full 40 characters; cell 1 refuses anything else |
| `STUDY_ID` | `thesis-recovery-v1`; rehearsal automatically uses `thesis-recovery-v1-rehearsal` |
| `SCOPE` | `cpu`, `rehearsal`, `development` or `main` (what may run in this session) |
| `START_NEW_STUDY` | `True` only for the very first run of a study (once for the rehearsal, once for the real study); otherwise `False` |
| `MAIN_AUTHORIZATION` | The development gate-report ID (`dev-...`) once you authorize main |
| `SESSION_HOURS` | `11`. Cell 1 caps the deadline 15 minutes inside Kaggle's 12-hour session limit, measured from when the Kaggle session started |
| `CHECKPOINT_REPO` | The private HF dataset, or `""`. If set, the `HF_TOKEN` secret must be attached or the session stops before installing |

## Sessions in order

| Session | Accelerator and settings | What happens | Expected time |
|---|---|---|---|
| A. Rehearsal | None; `SCOPE="rehearsal"`, `START_NEW_STUDY=True` | Whole pipeline with a scripted model on 2+2 worlds; checkpoints and mirror | about 15 min |
| B. Restore drill | None; `SCOPE="rehearsal"`, `START_NEW_STUDY=False`, a new session | Cell 3 restores the newest rehearsal checkpoint; zero new calls; identical report | about 15 min |
| C. Real-study preflight | None; `SCOPE="cpu"`, `START_NEW_STUDY=True` | Creates the real study; installs on the current image; CPU checks with the real tokenizers; first mirror upload | about 10 min |
| D. Development | GPU T4 x2; `SCOPE="development"`, `START_NEW_STUDY=False`; **Save & Run All** | Downloads each model, readiness, 16 development worlds per model (at most 704 calls each), gate report | 2–3.5 h |
| E. Main | GPU T4 x2; `SCOPE="main"`, `MAIN_AUTHORIZATION="dev-..."`; **Save & Run All** | Freeze (once), then the 64 main worlds for Qwen, then Granite | Qwen about 2.5 h expected (3.4 h worst case at the measured rate); Granite measured in D. Usually one session |
| F. Final | Any scope, or locally | Report from the newest checkpoint | minutes |

Sessions A–C use no GPU quota and catch most setup problems (Python version,
package lock, Internet, mirror, tokenizers) before any GPU time is spent.

After session D, read the gate report printed by cell 5 (also in
`receipts/gate-report.json` and the version's output). Paste its ID into
`MAIN_AUTHORIZATION` only if you authorize main. If one model failed its gates,
main runs the other alone; if both failed, there is no main. Development
continuation outcomes are descriptive and never change the design.

If session E ends before main is complete, start another session with the same
settings (main continues exactly where the newest checkpoint stopped). Before and
after session D, note the GPU quota Kaggle shows, to learn how it charges T4 x2.

**Interactive alternative.** In an interactive session you may authorize main
right after development: set `SCOPE="main"` and `MAIN_AUTHORIZATION`, then *Run
All* again (completed cells are quick; the downloaded weights are reused). Keep the
browser tab open: Kaggle can end an interactive session after the tab closes.

## How a session protects your work

- **Raw replies before effects.** A completed call is never regenerated; an
  interrupted one is retried once with the identical request and seed.
- **Checkpoints** every 20 minutes, at every stage end and after every cell, under
  `/kaggle/working/thesis/<STUDY_ID>/checkpoints/` (newest two kept), mirrored and
  verified (LFS SHA-256, or Git blob hash for small files) when `CHECKPOINT_REPO`
  is set.
- **Deadline inside Kaggle's limit.** No new world starts in the last 25 minutes
  before the deadline and no call is admitted in the last 18, so the final
  checkpoint and the version's output are written before Kaggle stops the session.
- **Kernel restart.** Re-running cell 1 after a kernel restart in the same Kaggle
  session continues the same session and deadline (nothing is counted as a lost
  session). If a stage process is still running, cell 3 refuses a second writer;
  call `nb.stop_running()` and wait for it to checkpoint.
- **Restore rule (cell 3).** It looks at the local run directory, every attached
  input and the mirror, and restores the **highest** checkpoint sequence. It
  refuses: two different checkpoints with one sequence; a local study older than an
  attached checkpoint; a checkpoint from another commit; a configured mirror that
  is unreachable (it could hold a newer checkpoint); and a checkpoint written in
  the last 30 minutes by a session that has not finished (another session may
  still be running).
- **Never run two sessions of one study at once.** Kaggle's editor and a *Save &
  Run All* version are separate sessions. Finish (cell 9) or stop one before
  starting the other.

## Reading the progress output

Progress lines appear every minute and after every world:

```text
[14:02:11] MAIN qwen . worlds 21/64 complete . calls this session 640 . attempts 1890 (contingency 0/300) . aggregate GPU-h 7.4/100 . deadline in 8:41:03 . about 1:12:30 left for qwen at this session's measured pace
[14:02:40] main-021 done on GPU1: prefix B . RV H . CV B . RP B . CP B . RN B . CN W . 170 s
```

Terminal codes are B (both submitted), H (horizon exhausted) and W (waiting
deadlock). The time-left estimate appears only after two worlds have finished in
this session. During main, success is hidden: you see terminal reasons, call
counts, contingency and GPU-hours, not outcomes.

## What the cells do

1. **Settings and source:** checks `SOURCE_COMMIT`, downloads that commit (three
   attempts; verifies the archive's commit header) or uses an attached source
   packet, records the session and its deadline.
2. **Install:** pinned virtual environment from `configs/i01-runtime.lock` (about 3
   minutes). Stops without an error if the image is not Python 3.13, a GPU scope
   lacks T4 x2, or the installation fails.
3. **Open:** restores, reopens or (first run only) creates the study.
4. **CPU checks:** manifest, input separation, protocol, analysis and checkpoint
   checks, and the token-capacity proof with the real tokenizers.
5. **Development** · 6. **Freeze** · 7. **Main**: skip outside their scopes.
8. **Report:** rebuilt from the canonical store; estimates appear only when main
   is complete (or after `declare-stopped`).
9. **Finish:** marks the session finished, writes the final checkpoint, uploads it,
   shows download links.

Expected stops never raise an error: the cell prints a banner, later GPU cells
skip, and cells 8–9 still run, so a *Save & Run All* version completes and Kaggle
keeps its output.

## When something stops

| Message | Meaning and action |
|---|---|
| `skipped: scope ...` | The cell is outside `SCOPE`; nothing to do |
| `Set SOURCE_COMMIT ...` / `Cannot download the source` | Fill in the full commit; check Internet is on and the commit is pushed, or attach the source packet |
| `the pinned lock needs Python 3.13` | The Kaggle image changed; pin the notebook to its original environment. A new image needs a new lock (stop and ask) |
| `installing the pinned environment failed` | Usually network; run Run All again. Logs are in `thesis-receipts/<session>/setup/` |
| `CHECKPOINT_REPO is set but the HF_TOKEN secret is not available` | Attach the secret, or set `CHECKPOINT_REPO = ""` |
| `the configured checkpoint mirror is unavailable` | The Hub did not answer; run again later, or clear `CHECKPOINT_REPO` to restore from attached inputs only |
| `another session may still be running this study` | Finish or stop the other session, or wait until the time shown |
| `time: dispatch cutoff reached` | Session time is nearly used; run again in a new session |
| `CPU checks have not passed` | Run cell 4 first (Run All does) |
| `MAIN_AUTHORIZATION ... does not match` | Paste the exact gate-report ID |
| `newer checkpoint ... exists` | A newer checkpoint is attached; move the old local run directory aside |
| `different source/config/inputs` | `SOURCE_COMMIT` differs from the study's; use the original commit |
| `another process ... owns this study` | A stage is still running; wait, or call `nb.stop_running()` |
| `integrity: ...` or `ceiling ... reached` | Stop and ask; nothing is retried automatically |

Never delete checkpoints or the run directory to "start over"; a new study needs
a new `STUDY_ID` and its own decision.

## After main is complete

Cell 8 writes `reports/` (report, analysis JSON, episodes and calls tables,
casebook, figure). Download the newest checkpoint and `reports/`, keep the Kaggle
versions, and keep the mirror. Delete nothing.

## Local commands (CPU)

Unzip a downloaded checkpoint into an empty folder `DIR`, then (read-only, no
model, no network):

```text
python -m recovery.thesis report --run DIR --out DIR/reports
python -m recovery.thesis show   --run DIR --model qwen --world main-000 --cell RV
python -m unittest tests.test_thesis_worlds tests.test_thesis_protocol tests.test_thesis_models \
  tests.test_thesis_analysis tests.test_thesis_checkpoint tests.test_thesis_run tests.test_thesis_notebook
```

`report` and `show` read the canonical store only. `status` also checks the study
binding, which includes the runtime lock's bytes; on a Windows checkout with
`core.autocrlf` those differ from the committed bytes Kaggle used, so run `status`
from an LF checkout (`git -c core.autocrlf=false checkout`) or rely on `report`.

## Verified on CPU versus still to be shown on Kaggle

Verified on CPU (Windows, Python 3.11): the whole pipeline with the scripted
double, through the notebook facade and the CLI, including a cross-session restore,
the deadline cap, kernel-restart continuation, the restore guards, mirror
verification against a fake Hub API, and the source packet's committed bytes. See
the [implementation evidence](validation/thesis-implementation.md).

Not yet shown, and checked by the sessions above: the current Kaggle image still
runs Python 3.13 and installs the lock (C); the real Hub mirror upload, listing and
restore (A, B); `/kaggle/temp` space and download speed for about 37 GB of weights
(D); Granite loading, memory, speed and JSON legality on T4 (D gates); the actual
quota charge for T4 x2 (D); the Kaggle session-start detection used for the
deadline cap (printed in cell 1 when it applies).
