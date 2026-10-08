# Actual Kaggle CPU continuation run 5

Reviewed 8–9 October 2026. The supplied [executed notebook](../../notebooks/run/5/notebook-exec.ipynb) and [results ZIP](../../notebooks/run/5/preflight-results.zip) complete the same-session continuation of [run 4](m5-kaggle-full-preparation-run-4.md). **All 97 CPU checks pass, with zero skips.** Run 4's original parsing failure remains retained; run 5 supplies the successful provenance and previously blocked checks. No repeat CPU preflight is required for this unchanged candidate.

The [independent audit](../../notebooks/validation/m5-full-preparation-run-5/validation.json) and [review script](../../notebooks/validation/m5-full-preparation-run-5/review_run.py) verify the notebook/cell binding, ZIP receipt/member safety/CRC, prior-report identity, package/module provenance, actual command logs/counts and off-host SQLite copies. The review never executes the supplied notebook or changes either original artifact.

## Actual outcomes

| Scope | Executed result |
|---|---|
| Source recheck | All 143 canonical members pass the continuation's byte/size/hash assertions. Its expected manifest matches the delivered v3 notebook and run-4 export. |
| Installed provenance | All 88 candidate versions and 28 scientific module hashes pass. The dedicated JSON receipt matches the retained generated probe and provenance file. The isolated installed probe runs outside the source directory, with venv module origins and no base site-packages in its path. |
| Focused checks | `tests.test_inference_preparation`, `tests.inference_checks`, `tests.durable_checks`, `tests.attempt_checks`, `tests.worker_checks`: **81 passed / zero skipped**, 262.359 reported test seconds. |
| Native 9B metadata | `tests.tokenizer_inference --tokenizer metadata/9B`: **4 passed / zero skipped**, 0.145 reported test seconds. |
| Native 4B metadata | The same command with `metadata/4B`: **4 passed / zero skipped**, 0.144 reported test seconds. |
| Native capacity | `tests.tokenizer_capacity --tokenizer metadata/9B`: **8 passed / zero skipped**, 1.716 reported test seconds. Complete input-plus-output bounds remain 261,388 / 259,868 under 262,144. |
| Command ownership | All eight commands exit zero, record leader exit and confirm their process group exited. No download, installation or model command starts. |
| Filesystem/export | Synthetic WAL/FULL check passes. Both closed databases reopen independently off-host as read-only/immutable with integrity `ok`, row `7`, rejected writes and unchanged copy bytes. |
| Model/GPU acceptance | **Zero model generations**; GPU-native diagnostics, model smoke and provider assignment/release remain unrecorded. T02 stays blocked. |

All seven continuation stages pass, with no root blocker or unconfirmed cleanup. The CPU continuation runs from **2026-10-08 21:44:46 UTC to 21:50:05 UTC**, taking **319.030 seconds** inside its 900-second CPU deadline. The focused command takes 263.960 seconds inside its unchanged 360-second bound. Native command elapsed times include interpreter/import overhead and are distinct from the test durations above. Run 4's installation and this continuation are separate observed workflow durations; the intervening open-session time is not included in either.

The reused host is Linux/Python 3.13.15, SQLite 3.45.1, with no visible driver GPU entries. Torch is the candidate **2.11.0+cu128** build and reports CUDA-build metadata **12.8**. This records installed software metadata on a CPU host, not working T4 kernels. `pip check` reports no broken requirements. Pip list contains the 88 locked distributions plus pip 26.2.1 and the noneditable project 0.1.0; normalized names, freeze versions and the project wheel URL agree.

## Warnings and artifact identity

The missing-`wrapt` `sitecustomize` warning persists, including in successful child commands. Its hook origin/traceback is still unknown. The two Transformers documentation messages remain in [probe stdout](../../notebooks/validation/m5-full-preparation-run-5/export/logs/installed-probe.stdout.txt); they no longer share the machine evidence channel. No package pin or base environment is changed to suppress them. The native capacity test's 262,156-token warning belongs to the intentional overflow-rejection case; all eight tests pass, and no overlong request reaches a model.

- Notebook: 129,199 bytes; SHA-256 `b7a031e90c7ac029b3995d64e3e85488aabce491cfd458a9538e3fabd9f18237`.
- ZIP: 44,863 bytes; SHA-256 `2e30aa95510e97eb9bea7cbab51ac4e60f5e58324e23d75f63e007ad72937b90`; 35 safe unique members / 139,386 expanded bytes. The new cell's printed receipt matches this ZIP; the old cell still displays run 4's receipt.
- The first six cell sources match the delivered v3 notebook. The executed continuation cell matches [the delivered file](../../notebooks/recovery_m5_kaggle_continue_run4.py) byte for byte; its program matches the three reviewed functions at checkpoint `9bf7983c3d5d6873d4c852ff89c79527048ddf80`. Code execution counts are 2/3/4/5; an empty unexecuted final cell is retained. Notebook schema and every code cell's syntax pass, with no notebook error output.
- The retained prior report matches run 4 byte for byte, SHA-256 `e5f1a612e86d8acc4a26b6e6b6b71cff30c2ebf4e97417a481bf50e822d5d16b`. The v3 helper/manifest/lock remain bound to build `635a76b14f8b2cbf2b00bd325debb99c97769565` and scientific baseline `ca46bcd55486b38bb453f5294e01f943bc7f7752`.
- Independent database copies: [filesystem](../../notebooks/validation/m5-full-preparation-run-5/reopened-filesystem.sqlite), SHA-256 `554c5c739e9b6a71e47f618c861104efb8a2cb12f5ef72012692365a9880cd86`; [backup](../../notebooks/validation/m5-full-preparation-run-5/reopened-filesystem-backup.sqlite), SHA-256 `79fd2a4b560315094c6c5b9fbee0ddf57b5bf180652850797d7f8e200c81b584`.

Actual local verification: `python -X utf8 notebooks/validation/m5-full-preparation-run-5/review_run.py` passes on Windows/Python 3.11.9. This is an independent artifact audit; the 97 scientific checks were executed on Kaggle, not rerun or simulated locally. [Supplied-artifact hashes](../../notebooks/validation/m5-full-preparation-run-5/original-artifact-audit.json) retain the original runs and the pre-existing local document edit.

The [final handoff audit](../../notebooks/validation/m5-full-preparation-run-5/handoff-validation.json) checks local links/anchors and all 29 task statuses, preserves 34 earlier notebook/returned artifacts and all 20 supplied-run files, and confirms an empty protected scientific diff. The pre-existing edit to `m5-inference-preparation.md` remains untouched and outside these commits.

## Acceptance and next gate

Run 4 plus run 5 pass the **CPU portion of K4/K8** and complete **K9's CPU evidence review**: canonical transport, Linux cleanup, candidate installation/build/import provenance, the prescribed 81/16 checks, synthetic filesystem diagnostics and verified off-host export. GPU-specific requirements in K8 and all physical model acceptance remain open. T01 stays done; T02 stays blocked; progress remains 21 done / eight blocked. No scientific setting, dependency candidate, replay/attempt rule, quota ceiling or frozen configuration changes.

The next work is [K10's complete-envelope and tiny T4 attention/runtime validation](../planning/m5-kaggle-first-run/04-model-feasibility-and-smoke.md), followed by verified model-asset staging, exact 24-slot materialization and attempt/allocation admission. An actual model-smoke notebook is not yet ready. A small prompt, successful import, or 33k-token stress case cannot establish full-envelope T4 headroom. A CPU session's scratch venv/cache is disposable; changing accelerator or session requires verified staging and GPU-host checks rather than assuming it survives.

Retain/download the supplied artifacts and stop the CPU session if still open. No further CPU rerun is requested. Existing GPU authorization persists; all allocated GPU time, including compatibility/setup/idle/shutdown, remains subject to the existing shared budgets and smoke admission rules. Provider release is not inferred from a notebook stop instruction.
