# M5 CPU-only Kaggle upload canary

Prepared and locally verified 8 October 2026. **The returned Kaggle CPU canary passes all five stages.** The [run-2 review](m5-kaggle-upload-canary-run-2.md) verifies the actual upload, original-dataset inventory and off-host snapshots. This implements K0 provenance and the bounded R1/R2 experiment in the [ordered repair plan](../planning/m5-kaggle-first-run/05-implementation-and-validation.md). The [full-source CPU preparation packet](m5-kaggle-full-preparation.md) is now implemented and locally validated; actual Linux/Kaggle preparation and M5-T02 model acceptance remain pending.

## Files to use

| File | Use |
|---|---|
| [recovery_m5_kaggle_upload_canary.ipynb](../../notebooks/recovery_m5_kaggle_upload_canary.ipynb) | Import into Kaggle. Six cells, three executable cells, no saved outputs. |
| [m5-source-canary.payload](../../dist/m5-kaggle-upload-canary/m5-source-canary.payload) | Upload this single 1,173-byte file as a private dataset, preserving its name and extension. |
| [canary-manifest.json](../../dist/m5-kaggle-upload-canary/canary-manifest.json) | Local audit manifest. Its expectations are embedded in the notebook; no separate upload needed. |

The payload is a tiny synthetic ZIP under a `.payload` suffix. It contains a synthetic source marker, gzip and nested ZIP with a synthetic report and SQLite row. It contains no study worlds, weights, credentials or actual worker data. The suffix passed this actual tiny upload; complete-source preservation still needs verification. The [platform research](../planning/m5-kaggle-first-run/02-platform-research-and-decisions.md#bounded-remaining-research) defines this acceptance question.

## CPU test procedure (completed in run 2)

The user completed this procedure and returned both artifacts under `notebooks/run/2`. Next run the [full-source CPU preparation packet](m5-kaggle-full-preparation.md); no repeat canary or GPU run is required by this review. The procedure remains here for reproduction.

1. Create a **private Kaggle dataset** named `m5-source-canary`. Upload only `m5-source-canary.payload`, unchanged.
2. Import `recovery_m5_kaggle_upload_canary.ipynb` as a **private notebook**. Set **Accelerator: None** and **Internet: Off**.
3. Use **Add Input** to attach the new dataset. No cell edits or package installation are needed.
4. Optionally attach the original `m5-kaggle-preflight` dataset too. The notebook inventories its source marker and relevant fixture paths if present. This helps diagnose the first failure; the transport test works with just the canary.
5. Select **Run All**. Download `canary-results.zip` from the last cell and stop the session.
6. Save that ZIP and the executed notebook in `notebooks/run/` for review. The printed ZIP SHA-256 is the export receipt.

If Kaggle refuses the `.payload` upload, return its error message. If the notebook reports failure, return the result ZIP. Keep the candidate unchanged so the failure remains interpretable. The next transport, such as the plan's bounded ASCII alternative, is chosen after reviewing that evidence.

## Checks and boundaries

[m5_kaggle_upload_canary.py](../../scripts/m5_kaggle_upload_canary.py) uses the standard library. The notebook embeds the exact helper and its checksum, so input processing cannot prevent loading the diagnostic or cause execution of an unverified attached helper.

- Record Python/OS/SQLite facts and inspect the NVIDIA driver directory without Torch or CUDA initialization. Visible GPUs refuse the CPU test; this probe does not establish billing or release.
- Inventory at most 2,000 entries without following symlinks. Missing roots, scan errors or truncation prevent a partial scan from establishing unique input selection.
- Require one regular payload with the embedded size/hash. Reject missing, ambiguous, altered or incorrectly sized input.
- Verify all outer member paths, sizes and bytes; reject duplicate entries, traversal and symlinks. Inspect compressed contents without copying or repairing an attached source tree.
- Verify decoded gzip bytes, nested ZIP members and a read-only reopen of its synthetic SQLite file.
- Exercise a small local WAL/FULL write, committed backup and immutable read-only reopen with explicitly closed handles. Actual worker lifecycle acceptance remains untested.
- Retain stage states, root reasons and an allowlisted export on handled failures. Check ZIP CRC/members, publish atomically and emit its checksum outside the ZIP.

Each stage checks the 60-second local deadline before starting; SQLite opens use a one-second busy timeout. These are operational CPU limits, separate from scientific model/GPU limits. Kernel removal or unwritable output can prevent final export; completed reports remain in the unique run directory when available.

Optional R1 observations recognize the original `ca46bcd...` marker and record compressed paths, decompressed counterparts or expanded directories. They do not infer unseen processing or repair scientific fixtures. Without the original dataset, R1 is `not_observed`. The notebook installs no packages, downloads no weights, makes zero model generations and leaves full-source/model gates null.

## Local validation actually executed

Environment: Windows, Python 3.11.9, SQLite 3.45.1. No provider upload/session or model execution was started by this implementation.

| Check | Result and retained evidence |
|---|---|
| Focused standard-library suite | `python -S -m unittest tests.test_kaggle_upload_canary -v`: **12 passed, zero skipped**. [Captured result](../../notebooks/validation/m5-upload-canary-local/validation.json), [test log](../../notebooks/validation/m5-upload-canary-local/unittest.stderr.txt). |
| Real Jupyter, exact shipped notebook, valid input | All three cells execute with counts 1–3; checks pass, download displays, ZIP CRC passes and the backup reopens independently with row `7`. [Executed notebook](../../notebooks/validation/m5-upload-canary-selector/valid/executed.ipynb), [result ZIP](../../notebooks/validation/m5-upload-canary-selector/valid/canary-results.zip). |
| Real Jupyter, exact shipped notebook, missing input | All three cells execute; `payload_missing` is the root blocker, dependent compressed checks are blocked and the download remains available. [Executed notebook](../../notebooks/validation/m5-upload-canary-selector/missing/executed.ipynb), [result ZIP](../../notebooks/validation/m5-upload-canary-selector/missing/canary-results.zip). |
| Notebook integrity | nbformat validity, code compilation, empty shipped outputs/counts, embedded helper/source equality and embedded manifest/payload equality pass. |
| Protected source/evidence | Existing scientific source/configuration/fixtures and original notebooks/results remain byte-identical. All 28 scientific module ASTs match the genuine remote baseline. Thirteen original notebook/result artifacts match their committed Git blob bytes. |

Focused cases cover repeatable builds, unchanged inputs, separate runs, missing/transformed/ambiguous input, size/hash drift, unsafe/duplicate/symlink members, inventory truncation, symlinked legacy paths, GPU refusal, interruption, deadline, compressed-content defects and controlled export failure. Real archives, SQLite and exports execute; only the named unavailable/fault behavior is mocked. This does not emulate a real upload.

The first release harness completed both cases but emitted a Windows ZeroMQ teardown assertion. The subsequent real-kernel check used `WindowsSelectorEventLoopPolicy` and completed cleanly: [selector validation record](../../notebooks/validation/m5-upload-canary-selector/validation.json). This changed the local harness, not the delivered notebook.

At delivery, the final artifact/link audit checked 53 local references and confirmed all 186 prior files outside five intended progress/planning updates remained unchanged. The shipped payload passed its exact manifest. Git whitespace checks recognize preserved artifact CRLF bytes; scientific source, configuration, fixtures and the user's original notebook/results are untouched.

## Artifact and commit provenance

| Item | Identity |
|---|---|
| Genuine M5 baseline | `ca46bcd55486b38bb453f5294e01f943bc7f7752`, `origin/feat/m5-inference-preparation`. |
| Retained planning/evidence checkpoint | `bc51648` — `docs: retain M5 first-run evidence and transport repair plan`. |
| Builder/helper/test checkpoint | `c20ebea1382e01a82de08d023a2e04f6085409d2` — `feat: implement bounded CPU Kaggle upload canary`. |
| Payload SHA-256 | `887d5d832546eb9e125812f35493a9a3d22b5e33d02849304e8dd608c3ae6bb2`. |
| Shipped notebook SHA-256 | `ce936ca88595301a41ac88232bb3eb4c068ee9f515ca4e148bc6bd2a907d7d74`. |

The original workspace retains its missing Git metadata/top-level files. A verified sparse checkout at `build/m5-kaggle-canary-review` uses local branch `feat/m5-kaggle-upload-canary`; commits live there, with identical task files mirrored into the original workspace. No branch was pushed or remote application changed. The initial full clone failed with an incomplete HTTP transfer; its partial checkout is retained separately, with no active process from that attempt.

Notebook/artifact Git attributes preserve raw bytes and recognize CRLF endings during whitespace checks. Builder/helper bytes match their actual source commit. The distribution folder follows the existing ignored-build policy. Reproduce a matching payload, manifest and notebook from committed source into **new** paths:

```text
python -m scripts.build_kaggle_canary --source-commit c20ebea1382e01a82de08d023a2e04f6085409d2 --output-dir <new-output-directory> --notebook <new-notebook-path>
```

The manifest records build Python/SQLite versions. Synthetic SQLite/gzip bytes can vary across build environments; each build emits matching artifacts. Existing paths are refused. No study fixture is regenerated.

## Acceptance and next dependency

The [returned run-2 evidence](m5-kaggle-upload-canary-run-2.md) shows unique input, exact outer/member bytes, preserved gzip/nested ZIP, five passing stages and independently readable snapshots. It also shows all 14 original gzip paths and two nested ZIP paths absent, with exposed counterparts. R1's observed-path question is resolved and R2 passes for the tiny raw payload. Dataset mount references are recorded; exact version identifiers and provider release remain unavailable.

K2–K7 implementation is delivered in the [full-source CPU packet](m5-kaggle-full-preparation.md), with 23 passing operational checks and real local Jupyter evidence. Next execute K8's full preparation on Kaggle and review its evidence for K4/K8/K9 acceptance. This verifies the tested transport on the full payload and the actual Linux candidate; the tiny canary alone cannot prove large-file limits or complete closure.

Assets, full-envelope headroom, actual attention dispatch, smoke requests, allocation/release reconciliation and T02 model acceptance remain later work. T01 stays done; T02/dependent tasks retain their blocked statuses. Scientific settings, outcomes, populations, attempt/replay rules and resource ceilings remain unchanged.
