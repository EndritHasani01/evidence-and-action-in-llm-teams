# First-run evidence and failure analysis

Inspection date: 8 October 2026. Inputs: the [executed notebook](../../../notebooks/run/recovery-m5-preflight-first-run.ipynb), [result ZIP](../../../notebooks/run/1/m5-kaggle-preflight-results.zip), [extracted report](../../../notebooks/run/1/m5-kaggle-preflight-results/preflight-report.json), [host record](../../../notebooks/run/1/m5-kaggle-preflight-results/host.json), [storage record](../../../notebooks/run/1/m5-kaggle-preflight-results/storage-plan.json), and [summary](../../../notebooks/run/1/m5-kaggle-preflight-results/summary.json).

The result ZIP and extracted files are now located under `notebooks/run/1/` in the supplied workspace; their raw bytes still match the retained first-run checkpoint. The executed notebook remains at its original path. Links reflect this arrangement without rewriting evidence.

## What ran

The executed notebook has 32 cells. Its first 20 cells match the delivered [20-cell notebook](../../../notebooks/recovery_m5_kaggle_preflight.ipynb) after normalizing CRLF/LF representation. All nine original executable cells ran with execution counts 1–9; the twelve appended code cells are empty and unexecuted. No substantive user edit is visible in those original cells.

| Stage / executed cell | Recorded outcome | What the outcome establishes |
|---|---|---|
| Initialization / cell 3 | New directory `/kaggle/working/recovery-m5-preflight-20261008T125104687053Z`. | One preparation run, starting at approximately 12:51:04 UTC. |
| Host / cell 5 | `host-nvidia-smi` passed in 0.037 s; `host-torch` passed in 8.168 s; pinned Hub metadata HTTP 200. | Two visible T4 devices, CUDA-enabled Torch import/availability and one working HTTP route. |
| Source / cell 7 | `ValueError: The input bundle is incomplete: tests/fixtures/capacity_report.json.gz`. | The discovered extracted input did not provide this required path. |
| Installation / cell 9 | Skipped because a prerequisite was missing. | No candidate venv installation was tested. |
| Candidate verification / cell 11 | Skipped. | No maintained text-class import, finite CUDA tensor, package closure or bitsandbytes test was performed. |
| Focused/native tests / cell 13 | Skipped. | None of the planned 81 focused or 16 native checks ran on Kaggle. |
| SQLite / cell 15 | WAL, FULL, backup integrity and read-only enforcement passed. | The small diagnostic worked on this run's writable output filesystem. |
| Storage / cell 17 | Writable locations recorded; model estimates skipped because `SOURCE_READY` was false. | No model download location was admitted. |
| Export / cell 19 | ZIP and summary produced; preparation incomplete. | Failed preparation exported usable evidence; zero model generations were recorded. |

The four false preparation booleans form one dependency chain: source rejection → installation skipped → environment verification skipped → tests skipped. They are not four independent observed failures. In particular, there is no installation log proving a dependency conflict, model import failure or incompatible quantizer.

## Verified host facts

| Fact | Observed value |
|---|---|
| Python / OS / SQLite | 3.13.15 / Linux 6.18.48+, x86-64, glibc 2.39 / SQLite 3.45.1. |
| Torch | `2.11.0+cu128`, CUDA build 12.8, `cuda_available=true`, two devices. |
| Compiled architectures | `sm_75`, `sm_80`, `sm_86`, `sm_90`, `sm_100`, `sm_120`. |
| GPU 0 | Tesla T4, `GPU-62709afd-94a6-5925-d476-6f89b2d91d8c`. |
| GPU 1 | Tesla T4, `GPU-048f791f-6986-48cc-7afa-153baf9cdafa`. |
| Driver / total / free per GPU | 580.178.04 / 15,360 MiB / 14,912 MiB. Actual reported capacity is 15 GiB per device. |
| Initial working/input filesystem | Both report device 1794 and 19.50 GiB free. |
| Root and `/tmp` filesystem | Both report device 54 and about 1,069.91 GiB free. |
| Post-source working free | 16,685,645,824 bytes = 15.5397186 GiB. |
| Post-source `/tmp` free | 1,148,790,222,848 bytes; a small write probe succeeded. |

`st_dev` equality helps identify shared filesystem accounting. It does not establish that `/kaggle/input` is writable, nor that scratch has an enforceable one-terabyte per-session quota. `/kaggle/input` was only read. The root/scratch capacity is a measured pool-level fact, pending platform limits and full staging verification.

The base package versions were Pydantic 2.13.5, LangGraph 1.2.11, checkpoint 4.2.0, LangChain Core 1.6.1, Transformers 5.16.1, Accelerate 1.14.0, tokenizers 0.23.1 and Hub 1.29.0. SQLite saver and bitsandbytes were absent. These are observed image versions, not a passing project lock. The earlier CPU-image Torch `2.11.0+cpu` is superseded for this GPU session; it is not the cause of this run's source failure.

## Source failure: proof versus explanation

The report identifies the selected folder as `/kaggle/input/datasets/endrithasani/m5-kaggle-preflight`. Therefore the auto-extracted-folder branch, rather than direct ZIP extraction, was used. Its `SOURCE_COMMIT.txt` passed the expected-marker check; all other paths in the notebook's small required-path list were present, since only one missing path was reported.

The local supplied source ZIP contains `tests/fixtures/capacity_report.json.gz`: 316,146 compressed bytes, a valid gzip stream with 17,239,656 decompressed bytes. `tests/tokenizer_capacity.py:30` explicitly opens that compressed path. Removing the requirement would defer failure to the native test and weaken source admission.

Kaggle's documented upload processing extracts archives. Its input processing is the leading explanation for a `.json.gz` member disappearing after upload. This remains an **inference**, because the run did not export a file inventory showing `capacity_report.json`, an extracted nested ZIP, or every original member. An incomplete dataset version or other upload-side transformation is still possible. The next diagnostic must capture actual paths and sizes; do not label the dataset conclusively corrupted or blame a user edit.

The source ZIP contains 14 gzip fixtures: 29,243,404 compressed bytes become 1,603,109,044 bytes when decompressed. Its two nested ZIP fixtures expand to 1,276,644,414 and 167,831,896 bytes. Thus recursively exposing archive contents can expand a compact source bundle by several gigabytes and erase filenames expected by tests. The observed working-space reduction is approximately 3.96 GiB; its cause was not instrumented and cannot be assigned entirely to those transformations.

The notebook copied the entire discovered tree before validating required paths. This can spend disk/time on an unsuitable input. Its source marker checked provenance but did not prove member-byte integrity. These are observed design weaknesses exposed by the failure, not evidence that Python/scientific source changed.

## Export and off-host verification

The result ZIP has ten members and passes ZIP CRC verification. Every extracted member in the supplied results folder is byte-identical to its ZIP member. It contains the two diagnostic database main files, a zero-byte backup WAL, a 32-KiB backup SHM, four JSON files and two host logs.

Both main-file-only diagnostic snapshots were copied to a fresh temporary directory and opened there with SQLite `mode=ro&immutable=1`. Each passed `integrity_check` and returned exactly `[(7,)]` from `probe`. This establishes that the received small backups are readable independently of the retained sidecars. Originals were not opened for writing or checkpointed. Sidecar presence alone is not a failed backup; future exports should distinguish closed diagnostic snapshots from live worker WAL requirements.

This is a useful off-host export observation. It is not a crash/restart test of actual LangGraph worker files, proof of Kaggle version persistence, or verification of restore-before-retry semantics for model attempts.

## Allocation and scientific unknowns

The notebook reports 39.774 observed wall seconds and 79.548 observed aggregate GPU-seconds as a lower bound. Provider assignment/release timestamps are both null. Time before the first cell, after the summary, ZIP download, and provider stop acknowledgement are missing. Neither 39.774 seconds nor 79.548 seconds is a complete bill or a demonstrated smoke-budget reconciliation.

No weights were loaded, no model-generated text/IDs exist, and no finite logits, language-weight inventory, NF4 operation, recurrent/cache independence, worst-context headroom or model latency were measured. Capability, recovery pilot, main execution and accepted freeze remain unexecuted. This planning inspection performs no model work.

## Artifact identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Delivered notebook | 37,051 | `a9cca42fff19b32863d42ae5852aa9635cf6eecca60c67d69f3804860f835cb1` |
| Executed notebook | 39,660 | `ca9986d25968da28fe1e05c071c7eea9ccab7005b2f02538565c29e714f74e55` |
| Returned results ZIP | 4,604 | `693f6770e7483777838e320118d92da0c5605d0e668276daf75f857fbab1da29` |
| Supplied source ZIP | 109,248,341 | `57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f` |
| Capacity gzip member | 316,146 | `e5b0843c9ce1c6a9deef81bf9d2af0b8af041ccbe867ebf31cf970a5f57a9871` |

The source ZIP has 143 members and 165,002,177 uncompressed member bytes when only its outer layer is extracted. Its baseline source marker is `ca46bcd55486b38bb453f5294e01f943bc7f7752`. These hashes are artifact-integrity evidence; they do not create new call identities or an alternate experiment store.

## Why previous validation missed this

The earlier 22 controlled workflows tested the actual archive and a tree produced by ordinary outer ZIP extraction. They did not emulate nested gzip/ZIP expansion by Kaggle. Mocked package/GPU subprocess success also did not exercise a real inherited Kaggle dependency closure. The separate 97 Windows checks remain valid CPU evidence, but they cannot validate either platform behavior.

The corrected validation must target these missing contracts directly: real upload canary, transformed input inventories, exact compressed-member preservation, clean Linux dependency resolution, owned subprocess-tree shutdown, and off-host export. Repeating Windows checks alone would not resolve them.
