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

The user confirms the original Kaggle session is still open. Deliver a pasteable cell bound to this repaired source checkpoint, reusing the original notebook namespace through a copy. Run only that new cell; preserve original globals, the failed report and earlier artifacts. Returned new evidence belongs under `notebooks/run/4/continuation/`. This is CPU preparation, with actual continuation/check outcomes pending. T02 remains blocked by remaining host/model gates, T01 remains done and progress remains 21 done/eight blocked.
