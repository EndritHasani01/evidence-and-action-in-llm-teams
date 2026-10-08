# M5 full-source Kaggle preparation repair

Implementation started 8 October 2026 after the [actual upload canary passed](m5-kaggle-upload-canary-run-2.md). The [ordered repair contract](../planning/m5-kaggle-first-run/05-implementation-and-validation.md) governs this work. Scientific code/configuration, the original archive and returned notebooks/results remain unchanged. T01 stays done and T02 stays blocked until actual host/model gates pass.

**Current action:** import the [v3 notebook](../../notebooks/recovery_m5_kaggle_preflight_v3.ipynb), reuse the accepted private `m5-kaggle-source-v2` dataset, select **Accelerator None / Internet On**, and return the executed notebook/ZIP under `notebooks/run/4/`. The [bootstrap repair](m5-kaggle-pip-bootstrap-repair.md) passes 25 operational checks, a real local isolated pip install and exact-notebook Jupyter checks. Full Linux candidate/model acceptance remains open.

**Latest actual run:** [returned run 3](m5-kaggle-full-preparation-run-3.md) verifies the full source on Kaggle, Linux process cleanup and synthetic off-host backups. It fails at `venv`'s internal `ensurepip` step, before package installation or tests. The original v2 delivery/checkpoint evidence below is historical; it records the earlier missing root files and isolated-checkout workflow, superseded by the user-authorized recovery noted at the end.

## Source delivery checkpoint

[build_kaggle_bundle.py](../../scripts/build_kaggle_bundle.py) copies the canonical original ZIP unchanged to `m5-kaggle-source.payload` and emits a complete member manifest. It records the scientific baseline separately from the actual operational build commit. Existing output directories are refused; no scientific fixtures are regenerated or recompressed.

Executed on Windows/Python 3.11.9:

- `python -S -m unittest tests.test_kaggle_bundle -v`: four passed, zero skipped; [final log](../../notebooks/validation/m5-full-preparation/bundle-tests.stderr.txt).
- Streaming audit of the original archive: all 143 member CRCs/sizes/hashes read, 109,248,341 archive bytes, 165,002,177 outer decoded bytes, 14 gzip and two nested ZIP members; [audit](../../notebooks/validation/m5-full-preparation/canonical-bundle-audit.json).
- Original archive SHA-256 remains `57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f`.

The initial unsafe-backslash case exposed Windows `ZipInfo` normalization. The test now writes the intended raw header and the builder validates `orig_filename`, rejecting normalized separators and control characters. Both initial failed logs are retained alongside the passing result. This is a transport-path fix; scientific source and fixture bytes are untouched.

## Runtime and candidate checkpoint

[m5_kaggle_preflight.py](../../scripts/m5_kaggle_preflight.py) implements early inventory/source admission, a clean scratch venv, fixed package/tooling records, offline wheel installation, a separate installed-package probe, the existing 81 focused and 4/4/8 native commands, WAL/FULL backup checks and bounded allowlisted exports. The notebook embeds this helper from its one reviewed source file so missing input cannot prevent diagnosis. The original archive remains exactly unchanged; operational helper/build provenance is recorded separately from its scientific baseline.

The explicit sequential stage wrapper records failed versus blocked work and exports on handled exceptions/interruption. Owned subprocesses retain stdout/stderr separately, reserve export time before starting, and stop their owned tree on timeout/interruption. Source/env/wheels/caches remain on scratch, while reports and closed snapshots remain in output. The CPU workflow is bounded to 2,700 seconds with 90 seconds reserved for export, independently of the unchanged scientific GPU/attempt ceilings. Visible driver GPU entries refuse this CPU installation stage.

Executed on Windows/Python 3.11.9: `python -X utf8 -S -m unittest tests.test_kaggle_bundle tests.test_kaggle_preflight -v`: **23 passed, zero skipped**; [log](../../notebooks/validation/m5-full-preparation/preflight-tests.stderr.txt). Cases use real archives, files, SQLite, exports and child/grandchild timeout/interruption cleanup. Candidate install/test/GPU outcomes are explicitly controlled where unavailable. A controlled successful workflow's 97 count validates reporting; it is not an actual candidate-host scientific regression result. Real Linux process-group cleanup remains to be executed on that host. The local capture harness needed explicit UTF-8 for Windows stage output; the delivered candidate commands already set UTF-8.

Before installation, the notebook now runs a real synthetic CPU parent/child/grandchild timeout diagnostic and requires confirmed cleanup and a stopped grandchild. It preserves separate command logs and blocks installation if cleanup is uncertain. Linux group inspection treats exited zombies as exited while conservatively refusing incomplete or malformed process information. The real diagnostic passed locally with Windows process-tree termination; controlled `/proc` fixtures cover Linux live/zombie inspection, without claiming an actual Linux run. This adds a host-side check for the next Kaggle execution rather than assuming cross-platform process behavior.

The eleven reviewed roots resolve with uv 0.11.6 for CPython 3.13/Linux x86_64/manylinux 2.28 to **88 packages**. [Target resolution](../../notebooks/validation/m5-full-preparation/pylock.linux313.toml), [selected wheel metadata](../../notebooks/validation/m5-full-preparation/candidate-wheel-files.json), [short candidate lock](../../notebooks/validation/m5-full-preparation/candidate-linux313.lock), and [audit](../../notebooks/validation/m5-full-preparation/candidate-resolution-audit.json) retain versions, origins and hashes. Exact selected wheel sizes sum to **4,068,346,127 bytes** (3.7889 GiB). Only metadata was fetched locally; no complete CUDA wheel installation or weight download was performed.

The build tools are separately pinned to pip 26.2.1, setuptools 84.0.0 and wheel 0.48.0 with [release wheel records](../../notebooks/validation/m5-full-preparation/build-tool-metadata.json). Source builds retain ordinary isolation with explicit build constraints, then install the one built project wheel noneditably. [pip's documented build constraints/report options](https://pip.pypa.io/en/stable/cli/pip_install/) and [uv's target-resolution workflow](https://docs.astral.sh/uv/pip/compile/) support this preparation; no package pins are claimed to be a passing scientific lock yet.

To avoid downloading packages implicitly during a remote dry-run, the notebook uses the already selected wheel URLs/sizes/hashes for admission and download, then performs pip's actual dry-run resolution against verified local wheels. Before download it records a conservative four-times package-expansion forecast plus a one-GiB build reserve. After download it replaces that forecast with exact wheel ZIP entry sizes before installation. Filesystems sharing a device form one capacity pool with an explicit 256-MiB evidence reserve; observed pool free space remains distinct from quota and model-asset admission. Shared-pool admission uses the smallest observed capacity, including different quota views of the same device; the added deterministic case verifies refusal before downloads.

At the v2 local checkpoint, full-size Kaggle upload, actual Linux/Python 3.13 installation/import/native checks and GPU/model acceptance were unverified. Actual run 3 subsequently passes upload/Linux cleanup, while candidate/model acceptance remains open. Docker's Linux engine is unavailable locally; no Linux installation success is inferred from Windows or cross-platform resolution. The historical v2 delivery and local Jupyter evidence follow.

## Final notebook validation

The exact shipped [v2 notebook](../../notebooks/recovery_m5_kaggle_preflight_v2.ipynb) has six cells, three code cells and no saved outputs or execution counts. Notebook schema, code compilation, helper/lock/manifest bindings and the helper's exact Git blob hash pass; [delivery audit](../../notebooks/validation/m5-full-preparation/delivery-audit.json). The payload is the canonical 109,248,341-byte archive unchanged, containing all 143 original members. Its full checksum remains `57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f`.

Real Jupyter executed all three code cells, with counts 1–3 and no error outputs, in two cases using the exact final notebook. Original cell sources remain identical:

| Case | Actually verified | Pending work |
|---|---|---|
| [Full canonical input](../../notebooks/validation/m5-full-preparation-kernel-final/valid-source/executed.ipynb) | All 143 source members admitted/extracted/verified; Linux/Python 3.13 gate correctly refuses local Windows; handled failure exports. | Candidate installation, Linux process cleanup and focused/native commands did not run. |
| [Missing input](../../notebooks/validation/m5-full-preparation-kernel-final/missing-source/executed.ipynb) | `payload_missing` root diagnosis; dependent setup/checks blocked; export remains available. | No source/candidate/model work is inferred. |

Both cases pass ZIP member/CRC checks and synthetic WAL/FULL backup checks. Copies outside their run directories reopen independently with read-only/immutable SQLite, `integrity_check=ok`, row `7` and rejected writes. [Final kernel validation](../../notebooks/validation/m5-full-preparation-kernel-final/validation.json) records ZIP hashes and artifact paths. The Windows selector event-loop setting belongs only to the local harness. Earlier preliminary kernel evidence is retained separately. Zero model generations, no local CUDA wheel installation and no actual GPU acceptance are reported.

The [preservation audit](../../notebooks/validation/m5-full-preparation/preservation-audit.json) confirms an empty scientific Git diff, 57 unchanged source/configuration/fixture files, matching ASTs for all 28 scientific modules and unchanged raw bytes for 16 earlier committed notebooks/returned artifacts. First-run result files already moved in the supplied workspace to `run/1` are recorded at their current paths; their content is unchanged. The [handoff audit](../../notebooks/validation/m5-full-preparation/handoff-audit.json) checks local references and all 29 task statuses against the index. Missing root authority/build files remain missing, and their historical references remain explicitly recorded rather than restored.

## Historical v2 files and completed run-3 procedure

| File | Use |
|---|---|
| [recovery_m5_kaggle_preflight_v2.ipynb](../../notebooks/recovery_m5_kaggle_preflight_v2.ipynb) | Import this new notebook into Kaggle. It preserves the original failed notebook. |
| [m5-kaggle-source.payload](../../dist/m5-kaggle-source-v2/m5-kaggle-source.payload) | Upload this one unchanged file to a new private dataset named `m5-kaggle-source-v2`. |
| [source-manifest.json](../../dist/m5-kaggle-source-v2/source-manifest.json) | Local audit copy; already embedded in the notebook, so no separate upload is required. |

The following v2 procedure was delivered before run 3. Use the current v3 action at the top for the retry.

1. Create the private dataset above with only `m5-kaggle-source.payload`, preserving its filename and extension.
2. Import the v2 notebook privately, attach that dataset, choose **Accelerator: None** and **Internet: On**.
3. Choose **Run All** without editing cells. The source check precedes a synthetic process cleanup check, pinned package download/install, installed provenance, 81 focused and 16 native checks, and filesystem/export diagnostics.
4. Download `preflight-results.zip` and the executed notebook, stop the session, and save both under `notebooks/run/3/` for review. Return failure evidence too; its root blocker determines the correction.

The notebook's CPU workflow is bounded to 45 minutes, including an export reserve. It stages about 4.07 GB of pinned package wheels on scratch, subject to conservative capacity admission and later exact expansion checks. The running Kaggle kernel is unchanged. It downloads no language weights and does not launch GPU diagnostics or model smoke. The CPU venv/wheel directory is disposable session scratch: later GPU preparation must recreate or verifiably stage the accepted environment/assets; their persistence is not assumed. GPU quota authorization already exists, while actual candidate/model/resource gates remain open.

## Artifact and commit provenance

The scientific source baseline is `ca46bcd55486b38bb453f5294e01f943bc7f7752`. Operational source checkpoints on local branch `feat/m5-kaggle-upload-canary` in `build/m5-kaggle-canary-review` are:

- `d26c6f9`: preserve canonical input bytes and member closure.
- `8c094f5`: isolate and validate full-source preparation and the target candidate.
- `14b460b`: use the smallest observed capacity of shared storage pools.
- `42fb405e09d879c1bd4594e9250cfbe53ad3e373`: require owned-process cleanup before installation. This is the build commit embedded in the final packet.

The [delivery audit](../../notebooks/validation/m5-full-preparation/delivery-audit.json) records notebook SHA-256 `0765be21eeba5de8b0afa25b76e69ba67cc8dac4d2bed1d7e77347aa0992cac3`, helper/lock hashes and candidate/package byte totals. Commit history lives in the verified isolated checkout and task files are mirrored to the original workspace. No remote branch was changed and no missing root authority/build files were restored. The distribution folder remains ignored; the complete manifest is embedded in the committed notebook. Reproduction requires the retained canonical original ZIP, committed helper/builder and target lock/tool metadata. Use new output paths because existing artifacts are refused:

```text
python -m scripts.build_kaggle_bundle --source-archive dist/m5-kaggle-preflight.zip --output-dir <new-output-directory> --build-commit 42fb405e09d879c1bd4594e9250cfbe53ad3e373 --candidate-pylock notebooks/validation/m5-full-preparation/pylock.linux313.toml --build-tools notebooks/validation/m5-full-preparation/build-tool-metadata.json --helper scripts/m5_kaggle_preflight.py --notebook <new-notebook-path>
```

K2–K7 implementation and local validation are delivered; K9's interim handoff is updated. K4's actual candidate-host criteria and K8/K9 acceptance depend on the returned full-source Kaggle run. Full-envelope coverage, T4 native/attention diagnostics, model staging, bounded exact smoke, allocation/release reconciliation, capability/pilot/freeze and main execution remain separate later gates. T01 stays done; T02 remains blocked; progress stays 21 done/eight blocked.

## Actual run-3 review checkpoint

The [run-3 review](m5-kaggle-full-preparation-run-3.md) accepts complete raw source delivery: all 143 members, including the 14 gzip/two nested ZIP members, survived the actual upload. Linux/Python 3.13, owned-process timeout cleanup and synthetic SQLite/export checks also pass. Five preparation stages pass, one environment stage fails and five dependents are blocked. No candidate packages or 97 focused/native checks ran; model generations remain zero.

The returned six notebook cell sources and manifest match the delivered v2 packet, the printed receipt matches the 17-member ZIP, and both snapshots reopen independently read-only off-host. Original artifact bytes are preserved. The reported inner `ensurepip` failure has no lower-level traceback, so no particular distribution cause is asserted. Fix bootstrap using the already reviewed pip wheel in a venv created without pip; the scientific source, 88-package candidate and accepted dataset remain unchanged.

After user-authorized Git recovery, the main workspace is again a usable checkout on the same branch/history, and all six missing root files have been restored byte for byte. The earlier isolated checkout remains preserved; new review/repair commits now use the main workspace. The pre-existing local preparation-document edit remains outside these commits.
