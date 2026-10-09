# M5 Kaggle upload canary: returned run 2

Reviewed 8 October 2026. **The actual Kaggle CPU canary passes all five stages.** The renamed raw payload preserved its exact bytes, gzip and nested ZIP contents. The original dataset inventory explains the first source-admission failure. Full-source preparation and M5-T02 model/host acceptance remain unexecuted.

## Retained artifacts and provenance

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| [Executed notebook](../../notebooks/run/2/recovery-m5-preflight.ipynb) | 25,043 | `f0c3f360257aaf62716744187d9124d6a53f17a4df2459073a12d96da0695a62` |
| [Returned result ZIP](../../notebooks/run/2/canary-results.zip) | 8,815 | `de4c6d9dc7a1f32e87981cd52aa4e5a7afd4b02d7b653ccbc5d6984f5e1760fc` |

Despite its generic preflight filename, the returned notebook is the six-cell [upload canary](../../notebooks/recovery_m5_kaggle_upload_canary.ipynb). All six cell sources match the delivered file after line-ending normalization. Its three code cells executed with counts 1, 2 and 3, without error outputs. The returned embedded manifest matches the delivered manifest exactly as parsed JSON. The notebook stdout summary, ZIP summary and report summary agree; the printed ZIP receipt matches the returned ZIP's SHA-256.

The helper and builder originate at `c20ebea1382e01a82de08d023a2e04f6085409d2`, against genuine scientific baseline `ca46bcd55486b38bb453f5294e01f943bc7f7752`. The notebook verifies embedded helper SHA-256 `d08a2fa62ab76addfab8c0dd74d9c0bd4f367a62ae6a9df62fb41fee5124f87a` before running it. Neither returned artifact was executed or modified during this review.

## Actual host and stage results

Start: `2026-10-08T17:09:09.343418+00:00`. Host: Python 3.13.15, Linux 6.18.48+ x86_64 with glibc 2.39, SQLite 3.45.1. The driver-directory probe found no visible GPU entries; it did not initialize CUDA or establish provider assignment, billing or release.

| Stage | Recorded result | Elapsed seconds |
|---|---|---:|
| CPU host | Passed; no visible driver GPU entries | 0.000095 |
| Input inventory | Passed; complete bounded scan, unique intended payload | 0.679454 |
| Transport bytes | Passed; exact payload and outer-member sizes/hashes | 0.008516 |
| Compressed contents | Passed; gzip, nested ZIP and synthetic SQLite checks | 0.002096 |
| Filesystem backup | Passed; WAL/FULL write and read-only committed backup | 0.045386 |

Selected input:

```text
/kaggle/input/datasets/endrithasani/m5-source-canary-payload/m5-source-canary.payload
```

The payload is 1,173 bytes, with SHA-256 `887d5d832546eb9e125812f35493a9a3d22b5e33d02849304e8dd608c3ae6bb2`. The checked notebook verifies the outer archive and every required member before the compressed-content checks. The report records preserved gzip and nested ZIP bytes and SQLite integrity `ok`, row `7`, and rejected writes on read-only reopen. The filesystem diagnostic records journal mode `wal`, synchronous `2` (`FULL`), and the same backup checks.

The summary records `canary_checks_passed: true`, no root blocker, `raw_payload` transport, zero model generations and 0.737463 observed wall seconds. Full-source preparation and model smoke are null. Provider assignment and release timestamps are also null; this wall time is a diagnostic duration, not a complete allocation interval.

## Original dataset observations

The same run attached the original input at:

```text
/kaggle/input/datasets/endrithasani/m5-kaggle-preflight
```

Its source marker matches baseline `ca46bcd55486b38bb453f5294e01f943bc7f7752`. The full inventory contains 479 entries: 52 directories and 427 regular files, with no scan errors or truncation. Regular-file sizes total 4,253,903,004 bytes; removing the tiny canary leaves 426 original-dataset files and 4,253,901,831 bytes, about 3.96 GiB.

Comparison with the original source ZIP's member list finds **all 14 outer `.json.gz` paths and both nested `.zip` paths absent**. Every corresponding suffix-stripped path is present as a file or expanded directory. In particular:

| Canonical required path | Observed input |
|---|---|
| `tests/fixtures/capacity_report.json.gz` | Missing; `capacity_report.json` is a 17,239,656-byte regular file. This matches the canonical gzip's decoded length. |
| `tests/fixtures/scripted_lifecycle_run.zip` | Missing; `scripted_lifecycle_run/` exposes 159 files. |
| `tests/fixtures/scripted_reports.zip` | Missing; `scripted_reports/` exposes 126 files. |

This directly establishes that the attached original tree did not preserve the compressed paths required by the first notebook. Archive processing during upload is consistent with the observed counterparts; its internal mechanism and the identity of every expanded byte were not measured. The reports ZIP itself contains 15 gzip members, so comparing only its outer decoded size with the expanded tree would understate potential recursive expansion.

The dataset mount paths are recorded, but exact Kaggle dataset version identifiers and save/retrieval actions were not exported. Do not invent them. The original archive, fixtures and failed first-run artifacts remain unchanged; no scientific fixture was regenerated or recompressed.

## Independent off-host review

The ZIP CRC check passes and its seven members are exactly `canary-report.json`, `summary.json`, `input-inventory.json`, `expected-manifest.json`, `transport.sqlite`, `filesystem.sqlite` and `filesystem-backup.sqlite`.

All three databases were inspected on disposable copies with SQLite `mode=ro&immutable=1`. Each passes `PRAGMA integrity_check`, contains row `7` and rejects writes. Their returned main-file hashes are:

| Database | SHA-256 |
|---|---|
| `transport.sqlite` | `5e516b46e32992539d7e29ded5a7945fa5eddc1c7160ca22ef3301f0a301791f` |
| `filesystem.sqlite` | `8fea253fc75c3e0cdb10b7cefe18b386defeb032c6cfa4fcc01832bb98427d5c` |
| `filesystem-backup.sqlite` | `459e7e0874819af4846848c8591e1df14051f87266228ce10b0eb138a707d19d` |

The transport database also matches the canonical nested synthetic database hash. The write diagnostic and committed backup are judged by integrity and content; they are not required to have identical file bytes. Returned notebook/ZIP hashes remained unchanged after review. No packages, runtime helper, CUDA probes, model downloads or inference were run during this review; the prior local test results remain separately recorded in the [implementation handoff](m5-kaggle-upload-canary.md).

## Decision and remaining dependencies

R1's path/inventory question is resolved for the observed mount, with dataset-version metadata unavailable. R2 passes for this tiny actual upload. Select the raw `.payload` format for K2; the ASCII fallback is unnecessary for this result. These observations do not prove large-payload preservation or the complete source closure.

The next implementation step in the [ordered plan](../planning/m5-kaggle-first-run/05-implementation-and-validation.md) is K2: build manifest-backed delivery of the unchanged full source archive, then K3–K9 preparation admission, clean environment, storage layout, bounded commands, corrected notebook and real host evidence. Verify all 143 canonical outer members on the actual full upload before installing or importing source. Retain every compressed member's original bytes and record the new dataset version when available.

The small off-host export demonstrates this returned backup is readable. Fresh-session durable retrieval, full worker recovery, package/native checks, SDPA dispatch, full-envelope memory, physical model loading, smoke/capability/pilot/freeze gates and allocation/release reconciliation remain open. T01 remains done; T02 remains blocked; task counts and scientific semantics are unchanged. The user has completed the requested canary step; the corrected full-source preparation packet must be implemented before another preparation run is requested.
