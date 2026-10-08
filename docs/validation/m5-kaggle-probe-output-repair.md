# Run-4 installed-probe output repair and continuation

Recorded 8 October 2026 after [actual run 4](m5-kaggle-full-preparation-run-4.md). The installed candidate and project build pass; the probe exits zero but upstream documentation messages precede its JSON on stdout. Strict whole-stream parsing fails before the remaining 97 checks. The original run and all package/scientific inputs remain unchanged.

## Narrow repair and local evidence

[m5_kaggle_preflight.py](../../scripts/m5_kaggle_preflight.py) writes the installed probe's receipt to a dedicated JSON file. The reader retains the size bound and exact dictionary/version/module-hash/class/CUDA-build/model-count validation. stdout and stderr remain separately retained, including upstream diagnostics. Generic `json_stdout` remains strict for other machine commands; no arbitrary warning lines or malformed receipts are accepted.

[m5_kaggle_continue.py](../../scripts/m5_kaggle_continue.py) provides one explicit CPU continuation for the admitted, still-open run-4 session. It checks the original report/manifest, exact source-member hashes, isolated venv configuration, expected candidate closure and CPU host before any command. It rechecks installed provenance, records pip list/freeze and runs the existing 81 focused/4+4+8 native checks through the existing owned command and test-count helpers. It performs no installation or download and uses no new experiment store or identity system. The new diagnostic output directory preserves the original failed report. Source changes, unavailable sessions, provenance/command failures and uncertain cleanup block dependent work; synthetic filesystem diagnostics/export remain available.

The continuation has a 900-second CPU deadline with the existing export reserve; focused/native command bounds remain 360/60/60/90 seconds. Incremental console messages identify the command starting. No weights, GPU-native probe, model generations, inference retries or changes to scientific resource ceilings are introduced.

Actually executed on Windows/Python 3.11.9:

- `python -X utf8 -S -m unittest tests.test_kaggle_bundle tests.test_kaggle_preflight -v`: **27 passed, zero skipped**; [final log](../../notebooks/validation/m5-probe-output-repair/final-tests.stderr.txt). The generated complete probe runs in a real noisy subprocess with unavailable external imports explicitly controlled, writes its machine file and passes strict receipt validation. The old stdout parser rejects that same diagnostic stream, reproducing the failure boundary. These controlled imports do not prove actual candidate installation, already separately observed in run 4.
- The continuation case preserves the prior failed ZIP, starts no download/install command, completes the controlled 97-count workflow and rejects changed source before commands. After narrowing its eligibility to the actual failed probe stage, that [focused case passes again](../../notebooks/validation/m5-probe-output-repair/final-scope-guard.stderr.txt).

The initial new test misclassified the command name `installed-probe` as an installation command. Its [failed log](../../notebooks/validation/m5-probe-output-repair/focused-tests.stderr.txt) remains retained. Correcting that assertion required no installation behavior change. Malformed, empty and absent machine files remain explicit failures with exportable evidence.

## Current handoff

The [pasteable continuation cell](../../notebooks/recovery_m5_kaggle_continue_run4.py) is delivered from source checkpoint `9bf7983c3d5d6873d4c852ff89c79527048ddf80`. Its [binding record](../../notebooks/validation/m5-probe-output-repair/cell-delivery.json) verifies the exact three reviewed function bodies and SHA-256 `b07299f523e2cd08dba9d9e5366df9ec75695ed5ca01abf6f4a3d7ad4163aaa2`. The cell checks the original embedded helper identity, copies its namespace and installs the repaired functions only into that copy.

Real local Jupyter executes the exact shipped cell with counts 1–4 and no error outputs, using real source/archive/filesystem/export work and explicitly controlled candidate/import/test outcomes. It preserves the original failed ZIP and original helper functions, performs no package download/install and exports the controlled 97-count continuation. [Executed harness notebook](../../notebooks/validation/m5-probe-output-repair/executed-cell.ipynb), [kernel validation](../../notebooks/validation/m5-probe-output-repair/kernel-validation.json) and [harness](../../notebooks/validation/m5-probe-output-repair/verify_cell.py) retain this wiring evidence. Controlled counts remain separate from actual Kaggle checks, which have not yet run.

The user confirms the original Kaggle session is still open. The next action is:

1. Open the linked `.py` file locally and copy its complete contents.
2. Paste into one new code cell in the **existing v3 Kaggle notebook/session**, keeping **Accelerator None**. Run **only that cell**; it reuses the installed environment and prints each command starting.
3. Download the new ZIP and updated executed notebook, stop the session, and save both under **`notebooks/run/4/continuation/`**. Original run-4 files stay at their existing paths.

This is CPU preparation, with actual continuation/check outcomes pending. T02 remains blocked by remaining host/model gates, T01 remains done and progress remains 21 done/eight blocked. The original v3 notebook is preserved as the delivered failed-run artifact; no fresh-session rerun is requested while this admitted session remains available.
