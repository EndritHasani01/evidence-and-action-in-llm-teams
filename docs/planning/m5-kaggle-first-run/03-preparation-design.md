# Proposed preparation design

**Implementation status: CPU preparation delivered and locally validated; actual Linux/Kaggle acceptance pending.** The [implementation evidence and v2 handoff](../../validation/m5-kaggle-full-preparation.md) record the 23 checks, exact-source audit and real Jupyter runs. The design below preserves its original rationale; [model smoke](04-model-feasibility-and-smoke.md) remains a later gated action.

Two delivery details became concrete: the notebook uses a new `v2` filename to preserve the original, and embeds the one reviewed helper with its build-commit checksum so missing input can still be diagnosed. It verifies the complete canonical payload/member manifest before installation; the unchanged baseline archive does not acquire an operational helper under its historical source marker. The 88-package Linux/Python 3.13 lock selects exact wheel URLs/hashes/sizes, uses scratch, and replaces its pre-download expansion forecast with actual wheel entry sizes before installation. Linux cleanup is explicitly tested by a synthetic owned-process timeout stage before any package download. These are implementation choices within the design, not changes to scientific semantics or proof of model feasibility.

## First principles

A preparation notebook must establish that the bytes executed are the reviewed source, its packages form a working candidate, its filesystem can retain evidence, and its output identifies the next unresolved gate. A provider's input transformation cannot become an implicit scientific preprocessing step. A host's preinstalled version list cannot become an accepted model lock. Disk capacity, GPU memory, allocation time and durable evidence are independent resources.

The user should import one notebook, attach one clearly named private source dataset, run fixed defaults, download one result ZIP and stop the session. They should not diagnose Python wheels, reconstruct compressed fixtures, edit paths, choose serving stacks or decide whether an unexplained failure justifies a smaller model.

## D1 — Canonical source delivery

Build delivery artifacts with a small standard-library script, proposed `scripts/build_kaggle_bundle.py`. Preserve the existing archive's protected source/fixture bytes; future approved implementation edits get a new bundle and manifest. Keep the first-run ZIP unchanged as a baseline.

The delivery manifest must record the source baseline commit, actual build commit when available, transport format, archive byte count/SHA-256, and member path/size/SHA-256. The notebook must have a known expected archive/manifest reference, rather than accept arbitrary content because `SOURCE_COMMIT.txt` matches. These are deployment-integrity checks, not new experiment IDs or a mutable progress database.

R2 selects one passing transport before the user receives it. The first candidate is the archive's exact bytes under a `.payload` filename. A changed suffix is only a hypothesis until the CPU upload canary confirms exact preservation. If the platform still expands it, use a tested base64 ASCII payload with standard-library streaming decoding instead; the existing 104.2-MiB archive would become 145,664,456 encoded bytes, about 138.9 MiB. Avoid building several untested fallback formats into the runtime.

Do not recompress an exposed JSON and claim it is the original gzip. Do not recreate extracted nested SQLite/report ZIPs from whatever files happen to be present. Those operations lose binary provenance and can conceal incomplete input. Repacking is permitted only at the delivery layer from verified canonical originals, with explicit new transport checksums and identical contained scientific bytes.

### Admission before copying

1. Locate the uniquely intended payload/manifest and record its dataset path/version when available. Diagnose ambiguous or absent candidates explicitly.
2. Inventory candidate paths, sizes and relevant transformed counterparts without copying the entire tree. Bound the scan and record truncation if its limit is reached.
3. Check available scratch space against payload decoding plus outer archive extraction and reserves.
4. Verify the delivered payload, decoded archive hash and expected source marker.
5. Reject duplicate ZIP entries, unsafe absolute/parent/drive/backslash paths, symlinks and conflicting file/directory entries before extraction.
6. Extract into an exclusive run scratch directory and verify every expected member. Keep compressed fixture and nested archive bytes compressed.
7. Verify the actual required test/deployment closure, including all modules imported by the named checks, native metadata and population/schedule fixtures. Do not replace the full manifest with the current short required-path list.

If direct legacy ZIP input or an extracted tree is retained for compatibility, it must satisfy the same complete member manifest. A transformed legacy tree fails with a targeted message explaining how to attach the corrected payload; it is never silently repaired. Avoid unrelated input-tree copies and executable extra modules on `PYTHONPATH`.

For the next implementation, start from the verified baseline archive or a verified checkout. Missing live top-level build/spec files and unavailable Git metadata must be resolved or explicitly recorded. Do not stamp changed source with the old commit as though it were a new committed build. Record baseline and current build provenance separately.

## D2 — Small orchestration boundary

Keep the notebook kernel on standard-library setup and display. Reusable preparation stages live in one ordinary helper, `scripts/m5_kaggle_preflight.py`, so subprocess and storage behavior can be tested without running an entire notebook for every case. The builder embeds that reviewed helper and its checksum separately from the unchanged scientific archive; bootstrap verifies the embedded bytes before executing it. Complete archive-path and member checks belong to this tested helper and run before candidate installation or scientific imports. This permits missing-payload diagnosis without trusting executable code from an attached dataset.

Use explicit sequential functions for source, environment, checks, filesystem/storage and export. No LangGraph bootstrap workflow, plugin layer, new scheduler, generic task engine or second experiment state store is needed. Existing LangGraph code is exercised only after its dependencies are installed. The notebook defaults remain preparation-only; it must not construct `ModelFactory`, download weights, or continue into smoke when a check turns green.

Create a unique run label once. Use it for scratch and output locations and retained logs. Restarting notebook execution creates new preparation evidence; it does not erase the first run or reset allocation spending. Later model restarts/resumes use existing worker IDs and ledgers rather than creating fresh scientific trials.

## D3 — Clean candidate environment

The default candidate is a plain venv with `include-system-site-packages=false`. Recreate it on the actual interpreter; do not install into the running Kaggle kernel, copy another session's venv, broadly append base site-packages, or upgrade the image in place.

| Root requirement | Initial reviewed candidate |
|---|---|
| Python | Actual Kaggle 3.13.x candidate, recording the exact version; project requires >=3.11. Passing tests are required, not an assumed Python 3.11 image. |
| Torch | `2.11.0+cu128`, official CUDA 12.8 index for this observed host. Record exact build/index/wheel identity and compiled architectures. |
| Pydantic | `2.13.5` |
| LangGraph / checkpoint / SQLite saver / Core | `1.2.12` / `4.2.0` / `3.1.1` / `1.6.6` |
| Transformers / Accelerate / bitsandbytes | `5.12.0` / `1.14.0` / `0.49.2` |
| tokenizers / Hub | `0.22.2` / `1.19.0` |

Resolve the complete closure before GPU allocation where possible. Retain resolver/install reports, wheel origins/hashes and the final installed package list. Use exact Torch selection from its official index without accidentally installing a different default CUDA build. For other roots, use the ordinary package index and constraints. A CPU staging process can download compatible GPU wheels without constructing a CUDA model.

Revalidate driver compatibility for CUDA 12.8 instead of reusing the earlier CUDA 12.6 threshold. A conservative native CUDA 12.8 GA Linux candidate uses driver >=570.26; this run's 580.178.04 exceeds it. Older CUDA minor-compatibility routes require their own reviewed evidence and are not an automatic fallback. A driver/build change creates a new candidate and reopens affected checks. [CUDA 12.8 release notes](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-toolkit-release-notes/index.html).

Install source noneditably with ordinary isolated build dependencies and `--no-deps` after the closure is present. Python 3.13 venvs do not supply setuptools by default; do not restore the previously rejected `--no-build-isolation` assumption. Record build tooling and resulting package bytes as well as runtime roots.

Reject resolver/import/native failures with their actual logs. Only adjust implicated dependencies after primary-source review; record a new candidate and reopen affected checks. Do not immediately adopt Kaggle's Transformers 5.16.1 or latest packages merely because they are installed there.

### Verification requirements

Verify exact versions, `sys.executable`, `sys.path`, package/module locations and source-to-installed module bytes. Run an installed-package import probe outside the source directory with source `PYTHONPATH` removed and user site disabled. The source-mode tests may use the validated source tree, but must be labeled separately; `cwd=source` plus `PYTHONPATH=source` is not proof of installed-package execution.

Run `pip check` inside the clean venv, import the maintained Qwen text class without constructing it, and run the existing focused/native commands from document 05. Count actual tests and skips rather than treating command exit zero alone as proof that all expected tests ran.

On the GPU host, additionally verify both physical UUIDs, T4 capability 7.5, CUDA availability, supported compiled architecture and tiny finite tensors. Add one very small bitsandbytes NF4 quantize/dequantize or `Linear4bit` operation to expose a native binary/kernel failure before model loading. Label it a synthetic library diagnostic, with zero language-model generations; it establishes neither model loading nor worst-context memory. Ensure its subprocess exits and releases its contexts.

Add the tiny 16-query/4-KV-head SDPA eligibility/dispatch probe described in document 04. A generic finite tensor or an `sdpa` configuration string does not detect the reviewed GQA math-fallback risk. Record actual causal/mask geometry and native operation selection, distinguish library success from a suitable model runtime path, and block smoke readiness while this is unresolved. Count the GPU allocation for these synthetic probes.

No extra agent/provider abstractions, full LangChain application, remote tracing system or optional model kernels are needed.

## D4 — Scratch, output and staging contracts

| Location / role | Proposed contents | Persistence requirement |
|---|---|---|
| Verified session scratch, normally `/tmp/recovery-m5/<run>` | Decoded source archive, extracted source, venv, wheel/cache/install temporary files, optional separately staged model files. | Explicitly disposable; verify free space, quota assumptions and successful resident bytes. |
| `/kaggle/input/<attached source>` | Read-only verified transport input. | Pin the dataset version/reference; never rewrite it. |
| Optional private pinned model input | Original selected shards and tokenizer/config files, plus verified revision/file manifest. | Verify every file and actual loader path; no arbitrary public model reupload is assumed. |
| `/kaggle/working/recovery-m5-preflight-<run>` | Reports, package records, logs and closed diagnostic snapshots. | Export to an independent off-host copy before claiming durability. |
| Later `/kaggle/working/recovery-m5/<configuration-run>` | Authoritative worker files, existing owner locks, verified SQLite backups and smoke/pilot evidence. | Existing ownership, committed-state and backup rules apply. Forecast actual artifact growth before pilot/main admission. |

Record filesystem/mount identities and capacities before and after major stages. Treat locations sharing a filesystem as one capacity pool; do not add their free bytes. The first run's `/tmp` has promising capacity, but no general one-terabyte entitlement is established.

For each pool, calculate additional required bytes from exact model files, source expansion, installed wheel footprint, download `.incomplete` files, temporary build/cache copies, worker/backup growth and export overlap. Document whether completed shards are renamed in place or copied. Do not blindly double every model size, or assume no duplicates without inspecting the chosen downloader. Keep an explicit emergency evidence reserve and stop before using it for packages/weights. The old one-GiB artifact allowance is a smoke planning starting point, not sufficient evidence for the full pilot/main.

Keep expensive scratch out of saved output so Kaggle saving does not attempt to retain venvs or 18-GiB weights. Downloads belong to a separate CPU asset-staging action, or an already verified input. The preparation notebook can inspect exact remote file metadata; it still downloads no weights by default.

With `/tmp` staging, set the appropriate install/temp/cache paths explicitly. Later smoke should use an already verified snapshot offline. Current `ModelFactory` always resolves a Hub model name; document 04 compares the existing pinned cache route with a narrow local-directory extension. Do not choose a path that silently copies staged weights back into the 20-GB working pool.

## D5 — Stage state and useful failure reports

Each diagnostic stage should record `status` (`passed`, `failed`, `blocked`, or `not_run`), prerequisites, reason, actual start/end/elapsed time and artifact references. Existing summary booleans can be derived for compatibility. This is a preparation report, not another worker/progress database.

Distinguish a command's exit status from its logical validation: a successful Torch process returning malformed JSON is a failed diagnostic. A skipped install after source rejection is blocked by that source failure, with no installation-failure claim. Keep scientific gates null/unexecuted until their actual evidence exists.

For the observed failure, the summary should state one root blocker, the missing path, whether a likely decompressed counterpart exists, the selected dataset path/version, and the exact attachment action. List downstream blocked stages separately. Do not print the current generic suggestion to change GPU/Internet/Python/source when GPU and Internet already passed.

Export an allowlisted evidence set: reports, inventory/manifest comparison, package reports, command logs, diagnostic snapshots and run provenance. Include relative artifact paths and missing-stage reasons. Keep source, environments, weight files and unrelated working files outside this ZIP. Publish only a completed ZIP, after CRC and expected-member checks, and record its hash/size outside itself.

An outer `try/finally` must attempt final export for handled stage exceptions, parsing errors, timeouts and user interruption. Save small incremental reports after every completed stage. Uncatchable kernel death, provider removal or an unwritable output filesystem cannot guarantee a final ZIP; retain whatever completed reports/backups exist and state the limit honestly.

Summary fields should separate `preparation_checks_passed` from `model_smoke_ready`. The latter also requires verified model assets, exact request matrix, full-envelope argument, accepted persistence/export and complete allocation admission. All preparation successes can coexist with smoke readiness still false.

## D6 — Bounded commands and allocation

Use direct argument arrays and explicit interpreters. Keep stdout and stderr in separate retained streams or files; parse machine JSON only from stdout, preserving warnings in stderr. Stream large logs instead of retaining unbounded test/install output in memory.

For Linux commands that can spawn installers or test workers, create one owned process group/session. On timeout/interruption, terminate that owned group, escalate within finite bounds, reap and confirm exit, then export. A timeout on only the immediate Python process does not establish descendant termination. Never signal unrelated Kaggle/kernel processes. Keep cross-platform local verification limited to supported behavior rather than introduce a general process supervisor. The existing model `ProcessProvider` continues to own model-child termination and attempt persistence.

Record independent CPU preparation limits and GPU allocation limits. Move slow downloads/resolution to CPU staging where practical. On GPU, derive the remaining deadline from provider assignment or a conservative session-start bound; do not restart a fresh 780-second allowance at cell one after an unknown delay. Deduct backup/provider-release reserve and compare each command's full bound before launching it.

The existing packet counts GPU-assigned preparation and idle GPU 1 against the screen. Preserve that convention, retain the first run's incomplete interval for reconciliation, and share development/setup/interruption accounting across attempts and configurations. If a cold clean environment cannot fit the remaining short screen, stop or stage it on CPU; do not omit its allocated seconds or widen the screen because the account has more quota.

Provider stopping remains external unless an actually available, tested provider control is later selected. The notebook should prominently display the deadline and stop action. Do not report provider release from a cell timestamp, successful ZIP generation or model-child exit. Record an external acknowledgement and treat unresolved release as an accounting blocker.

## D7 — User experience for the corrected run

Ship a fixed-default notebook and the single tested private payload/manifest upload. The opening instructions should say exactly which asset to attach, whether this stage can run on CPU, and when T4 x2 is needed. The GPU preparation run retains Internet for installation/metadata unless a complete validated wheelhouse is attached; later smoke uses offline verified weights.

Run All should produce an actionable result even for expected prerequisite failures. The final cell must state the root blocker or named checks that passed, zero model generations, remaining model gates, one download link, and the provider stop action. Provide an off-host receipt/check procedure with the package; avoid telling the user to execute Save & Run All merely to preserve already completed smoke results.

The next user run is preparation-only. A passing result leads to reviewed model staging/request preparation; it does not automatically execute smoke, choose 4B, start the 90-slot capability stage, or alter the task population.
