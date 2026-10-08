# Kaggle setup notebook plan

Prepared 8 October 2026 at the user's request to plan and create the notebook
they should use. The earlier AGENTS.md instructions were revoked by the user;
this work does not reinstate them. Scientific settings come from the committed
specification and implementation in `dist/m5-kaggle-preflight.zip`, revision
`ca46bcd55486b38bb453f5294e01f943bc7f7752`, and the current
[inference packet](m5-inference-preparation.md). The notebook prepares the actual
host for M5-T02; it does not claim that model smoke or a pilot has run.

## Intended experience

Provide one `.ipynb` with fixed defaults and a short first-cell checklist.
The user imports it into a private Kaggle notebook, attaches the existing
source ZIP as a private input, enables Internet and GPU T4 x2, and chooses Run All.
Kaggle can expose the input ZIP itself or extract it automatically; both layouts
must work without editing dataset paths. Expected failures should still reach
the export cell. The final output names the one results ZIP to download and
send back, and records which prerequisite failed.

The notebook completes host inspection, candidate setup, deterministic/native
validation and storage planning. It finishes before model-weight downloads or
generation. This is the next preparation action from the current conversation;
the separate 24-call smoke still requires exact requests, retained allocation
intervals, verified durable export and the accepted candidate host evidence.

## Sequence and decisions

| Stage | Concrete behavior | Rationale / failure behavior |
|---|---|---|
| 1. Start | Create an exclusive timestamped output directory under `/kaggle/working`. Keep the notebook kernel on standard-library orchestration. | No package replacement in the active kernel, no notebook-local spawn factories, no overwritten prior evidence. |
| 2. Inspect | Record Python, OS, SQLite, package versions, four filesystem facts, both T4 UUIDs/driver/memory, Internet reachability and host Torch facts from a fresh subprocess. | GPU and CPU images can differ. A CPU Torch build must not be mistaken for a working CUDA stack. No model is constructed. |
| 3. Source | Locate the attached archive or its extracted `SOURCE_COMMIT.txt`; check the existing Git revision and materialize the required source. Validate archive paths and symlinks before extraction. | No credential-bearing clone or publication. Missing/ambiguous inputs produce an actionable report; host inspection remains available. |
| 4. Environment | Create an isolated venv. Reuse the base environment only when its Torch is 2.11.0, CUDA 12.6/12.8/13.0 is active and compiled Turing support is present. Otherwise use a clean venv and the official torch 2.11.0 CUDA 12.6 wheel, conditional on the driver. Pin the reviewed core/model versions, then install the source with `--no-deps`. | A subprocess interpreter avoids kernel restart and stale imports. Supported existing CUDA libraries save disk and setup time; a separate clean environment avoids incompatible base Torch/vision stacks. Full package checks and import checks still have to pass. |
| 5. Validate | Check pinned versions and actual CUDA/T4 identities; inspect maintained text-class import; run `pip check`; run the 81 focused inference, replacement/checkpoint, process/crash and worker/backup checks, four native checks per model and eight capacity checks. | These are named setup/protocol checks, not sampled model outcomes or GPU memory admission. Retain stdout/stderr and failures; skip dependent stages after failure. |
| 6. SQLite | Exercise WAL/FULL and the SQLite backup API on the actual writable artifact filesystem; reopen the backup read-only. | Confirms this notebook's actual filesystem behavior in addition to subprocess/runner tests. |
| 7. Storage | Read the pinned checkpoint indexes, inspect free space after installation, and show per-model tensor-download estimates plus a one-GiB artifact allowance. Test temporary writable candidate locations and distinguish shared filesystems. | NF4 VRAM is not source-download disk space. Prefer 9B as specified; do not automatically switch models or shorten context to conceal failure. No weights are fetched. |
| 8. Export | Save package listings, checks, logs, device/storage facts and the source revision into one ZIP. State actual completed checks, failures and unexecuted model/pilot gates. | No duplicate experiment/progress store. The report is setup evidence, not an accepted configuration or completed M5-T02. The user can recover diagnostics even when setup fails. |

The notebook records its observed wall/device time as a lower bound, with
assignment time and confirmed release unavailable until actual provider
observations are supplied. It must not infer complete allocation from an
inspection timestamp. Commands have finite timeouts and a common workflow
deadline; a final message tells the user to stop the provider session after
downloading evidence. Extra account quota does not alter scientific resource
limits. No provider API, paid capacity or main execution is introduced.

## Verification before handoff

- Validate nbformat 4 and compile every code cell; leave outputs and execution
  counts empty in the shipped notebook.
- Execute the notebook locally with controlled GPU/package subprocess results
  and a temporary artifact root: missing input, archive input and automatically
  extracted input, CPU-only Torch, incompatible driver, command failure and
  insufficient space must yield explicit states and recoverable exports.
- Exercise actual source extraction, revision checks and traversal rejection.
- Run actual exported focused/native checks on Windows separately from the
  controlled notebook execution. Keep Linux/Kaggle/CUDA execution unverified.
- Audit the result ZIP, notebook's first-cell instructions, file links and the
  source bundle. Preserve the existing implementation and scientific files.
- Record verification in this document and update the existing handoff. Make
  a checkpoint commit if usable Git metadata is available; it currently is not.

## Completion evidence

The [created notebook](../../notebooks/recovery_m5_kaggle_preflight.ipynb)
contains 20 cells, including nine executable cells. It uses the existing
[source bundle](../../dist/m5-kaggle-preflight.zip); no model weights or new
experiment implementation are embedded. Its first cell supplies the complete
import/private-input/GPU/Internet/Run All/download instructions. Default versions
and paths need no user edits.

Executed on Windows/Python 3.11.9:

| Check | Result and retained local evidence |
|---|---|
| Notebook structure | nbformat 5.10.4 validates schema 4; all nine code cells compile; shipped outputs/counts are empty. |
| Controlled workflow | 22 cases pass: real ZIP and auto-extracted inputs, missing/drifted/incomplete/ambiguous source, wrong hardware, incompatible driver, CPU-Torch repair selection, install/command-timeout/import/package/native failures, low disk, workflow deadline, stderr warnings in hardware probes, four unsafe path forms and ZIP symlinks. Actual SQLite probes and exported backup reopening execute in these cases. CUDA/install/test subprocess outcomes are controlled, not observed GPU results. |
| Source integrity | All 143 files in the real extracted input equal the supplied archive bytes: 132 original source files, ten model metadata files and the existing revision marker. |
| Actual notebook execution | nbclient 0.10.4 / ipykernel 7.2.0 runs all nine cells in a real local CPU kernel with missing input. Diagnostics, WAL/FULL/backup and result export pass; no installation or model call occurs. |
| Actual focused command | The notebook's exact five-module command passes 81 tests / 258.460 s, using the existing core .venv against its newly extracted source. |
| Actual copied native metadata | Global native environment passes four 9B checks / 0.207 s, four 4B checks / 0.206 s and eight capacity checks / 1.813 s. Maxima remain 261,388 / 259,868 including output reserve. |

The measured focused runtime exceeds the first draft's 240-second setup-command
bound. The final notebook allows 360 seconds for that CPU test command while
retaining the common 780-second workflow deadline. This changes no model attempt
timeout, smoke resource ceiling or scientific setting. Source installation uses
ordinary isolated build requirements; Python 3.13 venvs need not contain
setuptools already. SQLite handles close before their diagnostic files are
archived. These preparation fixes were completed before handoff.

Hardware JSON/CSV is parsed from stdout while both streams remain in the log.
The added warning case verifies that harmless stderr output does not force an
unnecessary clean CUDA reinstall. The final 22-case workflow rerun and real
nine-cell Jupyter rerun pass after these fixes. Final schema/code/empty-output,
source-ZIP integrity/revision and nine local-document link checks pass.

The reused CUDA builds have maintained Turing targets in the
[bitsandbytes 0.49.2 installation matrix](https://huggingface.co/docs/bitsandbytes/v0.49.2/en/installation).
The clean CUDA 12.6 path uses NVIDIA's conservative Linux 560.28.03 toolkit
driver threshold from its [release notes](https://docs.nvidia.com/cuda/archive/12.6.0/cuda-toolkit-release-notes/index.html).
Earlier minor-compatibility paths are not assumed to work. The actual candidate
import/CUDA tests still have to pass; these references do not establish model fit.

Local control verification is retained under
C:\Users\EndritHasani\AppData\Local\Temp\recovery-notebook-verification-r4ky69io,
including verification.json and each case's output ZIP/log.
The actual executed notebook is retained under
C:\Users\EndritHasani\AppData\Local\Temp\recovery-notebook-real-kernel-dpwne6pq.
The verification utility used is
C:\Users\EndritHasani\AppData\Local\Temp\recovery-notebook-authoring-8xrbsykq\verify_notebook.py.
The core environment supplies the existing pinned graph/SQLite stack; native
checks use the inspected global model-stack versions and Pydantic 2.12.5 as
recorded in the [earlier export audit](m5-kaggle-preflight.md#local-handoff-verification).
No Linux/Python-3.13/CUDA/package-install/physical-model result is inferred from
these Windows checks.

The present workspace has .git/upstream-checkouts but no .git/HEAD, config,
index or refs; Git reports that this is not a repository. Its top-level
AGENTS.md, PROJECT_SPECIFICATION.md, README.md and pyproject.toml are also
absent. They remain in the supplied committed archive. No deleted top-level
file or Git metadata was restored. Existing code/configuration/data matches the
archive modulo pre-existing text line-ending differences; no implementation or
scientific file was edited for this notebook. A checkpoint commit is unavailable
until usable repository metadata is restored.

No Kaggle execution, weight download, model generation, GPU reservation or
provider upload occurred in this workspace. M5-T02 model/host acceptance remains
pending. The next concrete action is to import and run this preflight notebook
and retain/download its actual Kaggle results.
