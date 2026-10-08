# M5 full-source Kaggle preparation: returned run 3

Reviewed 8 October 2026. **The complete source upload, Linux CPU host, owned-process cleanup and synthetic filesystem checks pass. Candidate preparation fails while `venv` invokes `ensurepip`.** Package installation, installed provenance and all 97 focused/native checks remain unexecuted; no model generations occurred. T01 remains done and T02 remains blocked.

## Returned artifacts and review

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| [Executed notebook](../../notebooks/run/3/notebook-exec.ipynb) | 111,733 | `efe476ada4fde533f85f316c0c0130689196a0bd9f7dfae608193f6cfb0e087a` |
| [Result ZIP](../../notebooks/run/3/preflight-results.zip) | 29,776 | `d135f6749b9e206a3c8a9f797f2a987f4c0bddabeffbda124d3b3a1e3c939e2a` |

All six cell sources match the delivered [v2 notebook](../../notebooks/recovery_m5_kaggle_preflight_v2.ipynb). Three code cells ran with counts 1–3 and no notebook error output: the stage wrapper handled the setup failure and exported evidence. Notebook stdout, ZIP summary and report summary agree. The printed ZIP receipt matches the returned file. All 17 ZIP members pass path/uniqueness/allowlist/CRC checks. The returned source manifest equals the delivered manifest as parsed JSON, and `candidate.lock` matches its pinned checksum.

The [review audit](../../notebooks/validation/m5-full-preparation-run-3/validation.json) and [extracted evidence](../../notebooks/validation/m5-full-preparation-run-3/export/preflight-report.json) retain the comparisons. Original returned files remained unchanged throughout review. The notebook was inspected, not rerun locally.

## What actually ran

Start `2026-10-08T19:44:59.225417+00:00`; observed CPU workflow time 7.490307 seconds. Host: Python 3.13.15, Linux 6.18.48+ x86_64/glibc 2.39, SQLite 3.45.1, no visible driver GPU entries. Provider assignment/release remain unrecorded.

| Stage | Actual outcome | Evidence and limit |
|---|---|---|
| Input inventory | Passed | Unique raw payload; four inventory entries, no truncation/errors. |
| Full source | Passed, 4.944336 s | Payload SHA-256 `57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f`; all 143 canonical members verified and 165,002,177 outer bytes extracted. |
| CPU host | Passed | Actual Linux/Python 3.13 CPU gate, without kernel CUDA initialization. |
| Owned-process cleanup | Passed, 2.256937 s | The intentional two-second timeout reaped the leader, confirmed Linux group exit and stopped the grandchild ticker. The command's timeout is the expected diagnostic outcome. |
| Candidate environment | Failed, 0.218279 s | `/usr/bin/python3 -m venv ...` returned 1 when its internal `ensurepip` command returned 1. |
| Installed provenance | Blocked | Candidate environment failed. |
| Focused and native checks | Blocked | No 81-focused or 4/4/8-native command ran. |
| Filesystem backup | Passed, 0.043550 s | Synthetic WAL/FULL committed backup, row 7, integrity/read-only enforcement. |

The full-source dataset mount is `/kaggle/input/datasets/endrithasani/m5-kaggle-source-v2`; its exact dataset version remains unavailable. No transformed compressed source counterparts were found. This extends the tiny run-2 canary to the entire 109,248,341-byte canonical payload, preserving all 14 gzip and two nested ZIP members. Scientific baseline is `ca46bcd55486b38bb453f5294e01f943bc7f7752`; operational helper/build commit is `42fb405e09d879c1bd4594e9250cfbe53ad3e373`. This accepts this full-source delivery, without generalizing to other platform uploads or accepting a model host.

The [venv command record](../../notebooks/validation/m5-full-preparation-run-3/export/logs/create-venv.json) confirms leader/group exit after failure. Its [stderr](../../notebooks/validation/m5-full-preparation-run-3/export/logs/create-venv.stderr.txt) identifies the nested `venv/bin/python3 -m ensurepip --upgrade --default-pip` failure. That nested command's lower-level traceback is not retained, so missing bundled wheels, distribution restrictions or another internal cause are not established.

## Storage and off-host evidence

Before extraction, scratch pool 53 reported 1,148,796,342,272 free bytes; output pool 1794 reported 20,940,513,280. They are distinct capacity pools. These are observed filesystem values, not provider quota or durable retention guarantees. The failure precedes bulk-wheel admission/download; no package-expansion or model-asset staging gate passed.

Both returned SQLite files were copied outside the extracted evidence directory and reopened independently with `mode=ro&immutable=1`. Integrity is `ok`, the only row is 7 and writes fail. The committed backup checksum matches the report. These small synthetic checks do not establish full worker/crash recovery or fresh-session provider retrieval.

| Snapshot | SHA-256 |
|---|---|
| `filesystem.sqlite` | `554c5c739e9b6a71e47f618c861104efb8a2cb12f5ef72012692365a9880cd86` |
| `filesystem-backup.sqlite` | `79fd2a4b560315094c6c5b9fbee0ddf57b5bf180652850797d7f8e200c81b584` |

## Decision and next dependency

K8 now has actual complete-source, Linux cleanup and synthetic off-host evidence. K4's candidate installation/provenance and K8/K9 preparation acceptance remain blocked by bootstrap. Preserve the eleven candidate roots, 88-package lock, scientific source and all failed evidence.

The narrow repair is to create the clean venv with `--without-pip`, then download and verify the already pinned pip 26.2.1 wheel and install it offline in that venv. This avoids dependence on the image's internal `ensurepip` bootstrap. The [Python 3.13 venv documentation](https://docs.python.org/3.13/library/venv.html) describes this option; [CPython's ensurepip implementation](https://github.com/python/cpython/blob/3.13/Lib/ensurepip/__init__.py) demonstrates invoking pip from a wheel in a fresh subprocess. Use the existing bounded command/log/export path and retain exact wheel identity. The inner failure's cause remains unknown even after choosing a supported bypass.

At this review checkpoint the repair is proposed, not yet validated. Subsequent implementation and handoff belong in the [full preparation evidence](m5-kaggle-full-preparation.md). The accepted source dataset can be reused unchanged for the corrected notebook; no repeat upload canary or fixture reconstruction is needed. GPU library/attention, full-envelope/model staging, exact smoke, allocation/release, capability/pilot/freeze and main execution gates remain separate.
