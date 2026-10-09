# M5 Kaggle first-run review and implementation plan

Prepared 8 October 2026; actual acceptance reviewed 8–9 October. **Status: run 4 plus run 5 pass CPU preparation, including all 97 focused/native checks with zero skips, installed provenance and off-host snapshots. No repeat CPU preflight is requested. GPU-specific compatibility, complete-envelope memory and model smoke remain open.**

The first run detected two T4s and CUDA-enabled Torch, then stopped at the source-input contract. The uploaded archive contains the missing compressed fixture. The immediate repair belongs to input delivery and validation. A reliable next run also needs explicit environment isolation, separate scratch/output storage, useful failure reports, and allocation accounting. Passing those preparation checks will still leave physical model acceptance open.

This package responds to the request to inspect the executed notebook and plan all necessary changes before implementation. The original planning phase changed only Markdown. The subsequently authorized [CPU upload canary](../../validation/m5-kaggle-upload-canary.md) is now implemented separately. The original delivered notebook, executed notebook, result ZIP, extracted results, source ZIP, scientific configuration and scientific Python implementation are retained unchanged.

## Reading order

| Document | Purpose |
|---|---|
| [01 — First-run evidence](01-first-run-evidence.md) | What actually ran, exact failure chain, artifact identities, verified positives and unknowns. |
| [02 — Platform research and decisions](02-platform-research-and-decisions.md) | Current primary sources, resolved questions, bounded remaining research, provider alternatives. |
| [03 — Preparation design](03-preparation-design.md) | Proposed source delivery, environment, storage, stage states, subprocess control, diagnostics and user workflow. |
| [04 — Model feasibility and smoke](04-model-feasibility-and-smoke.md) | First-principles memory/time analysis, the worst-context evidence gap, unchanged smoke/pilot gates and narrow possible backend changes. |
| [05 — Implementation and validation](05-implementation-and-validation.md) | Ordered work items, file changes, acceptance checks, failure decisions and logical commit checkpoints. |
| [06 — Lessons learned](06-lessons-learned.md) | Retrospective lessons from preparation, the first run and the review, with observed evidence separated from pending validation. |
| [07 — T4 compatibility](07-t4-compatibility.md) | Authorized next-step plan for bounded standalone library diagnostics, exact operations, resource discipline and validation/delivery checkpoints. |

## Authority and scope

Use the [M5-T01 contract](../../todos/M5/M5-T01-inference-and-allocation-preparation.md), [M5-T02 contract](../../todos/M5/M5-T02-hardware-smoke-and-host-validation.md), [M5 preparation packet](../../validation/m5-inference-preparation.md), [implementation plan](../../IMPLEMENTATION_PLAN.md), [capacity investigation](../../implementation-research/inference-and-capacity.md), and [M1–M4 CPU audit](../../validation/m4-cpu-gate.md). Their implemented scientific semantics remain the starting point.

At the original planning checkpoint the workspace lacked `PROJECT_SPECIFICATION.md`, `pyproject.toml`, `README.md` and `AGENTS.md`; specification §§8–9 were read from the unchanged [source ZIP](../../../dist/m5-kaggle-preflight.zip) at baseline `ca46bcd55486b38bb453f5294e01f943bc7f7752`. The later user-authorized Git recovery preserved and hash-verified every existing file, restored genuine checkout metadata and reinstated all six missing tracked root files byte for byte. The current root [AGENTS.md](../../../AGENTS.md) and [specification](../../../PROJECT_SPECIFICATION.md) are available and govern current work. Earlier missing-file statements describe their historical checkpoints.

This is an operational follow-up to completed T01, within T02 preparation. It does not reopen T01 merely because a Kaggle transport contract failed. T02 remains unaccepted; T03–T05 and main inference remain dependent on their actual gates. The user's stated willingness to use available GPU quota is recorded authorization context; another quota confirmation is unnecessary. Availability of quota does not alter the study's scientific resource ceilings.

This package supersedes the earlier [notebook plan's](../../validation/m5-kaggle-notebook-plan.md) assumption that an automatically extracted input tree preserves compressed fixture filenames. Earlier local validation is historical evidence, not validation of the observed Kaggle transformation. Historical statements that no GPU inspection has occurred are now outdated; the bounded first-run observations in document 01 replace them. Other milestone evidence is not upgraded.

## Decisions to implement first

| Decision | Recommendation | Boundary |
|---|---|---|
| Source delivery | Preserve the original archive as one raw `.payload`; verify its bytes and every extracted required member before setup. | The tiny canary and full run-3 upload pass. Reuse the accepted dataset; retain admission checks and original scientific fixtures. |
| Input diagnostics | Capture the actual attached-file inventory, sizes, missing paths, likely transformed names and validation reason. | Diagnose before copying a potentially expanded tree. |
| Package environment | Prefer a clean venv and the observed CUDA 12.8 candidate build. Resolve and record the full dependency closure. | Actual CPU closure/provenance/checks pass in runs 4/5. GPU libraries/kernel paths remain unverified; no passing scientific lock is inferred. |
| Storage | Keep environments, downloads and temporary source work on verified scratch; retain reports and worker backups under `/kaggle/working`. | Observed scratch free space is not a provider quota or durability guarantee. |
| Next user run | Prepare the tiny T4 compatibility check after complete-envelope review; CPU preparation already passes. | That follow-up is not yet delivered. No repeat CPU run, automatic weights, smoke, fallback, pilot or main execution is requested. |
| Model feasibility | Resolve the complete-envelope memory question before promising 9B acceptance. | A 33k-token fixture and a 261k-token bound are different claims. |
| Attention dispatch | Probe the reviewed SDPA/GQA math-fallback risk using tiny tensors before model loading. | A requested `sdpa` setting is not a measured efficient kernel; 4B shares the same head geometry. |
| Timing | Account from provider/session assignment, include both GPUs and setup, and check time before starting each operation. | The first cell's timestamp is only a lower bound on allocation. |
| Research | Complete the small experiments and static checks in document 02; expand only when a named blocker persists. | No serving-stack rewrite, custom kernels, model search or scientific scope change is justified by this source failure. |

## Intended sequence

1. Preserve and audit the first-run evidence; obtain a usable checkout for future commits without manufacturing history.
2. Verify byte-preserving Kaggle transport with a tiny CPU canary; build the manifest-backed delivery and diagnostic changes.
3. Validate the clean Linux/Python 3.13 candidate closure, package provenance, subprocess cleanup, storage layout and exports.
4. Run a corrected preparation notebook and review its actual reports. Recheck GPU-specific facts if CPU staging used a different image.
5. Resolve the live worst-context coverage, SDPA dispatch and model-source staging questions; materialize the 24 exact smoke requests offline.
6. Execute only a separately prepared, bounded model smoke after its prerequisites and allocation admission pass. Then follow the existing 90-slot capability, full-pilot and freeze sequence.

Steps 1–4 now pass within the admitted CPU scope; [actual run-5 review](../../validation/m5-kaggle-full-preparation-run-5.md) records their acceptance and the remaining GPU-host obligations. Steps 5–6 are the conditional continuation, with physical model/pilot gates unchanged. Existing GPU authorization persists; it does not substitute for those gates or resource admission.

## Completion and review standard

The next implementation is complete when the supplied source survives the real Kaggle input path, the named preparation checks run in an independently recorded candidate environment, failures export useful evidence, and the user receives an unambiguous next action. Model/host admission requires the additional evidence in document 04; a green preparation summary cannot stand in for it.

This planning package was checked against the supplied JSON/logs, original archive members, notebook cell text, pinned model metadata, source contracts and current primary documentation. The two exported diagnostic databases were inspected on disposable off-host copies. Local Markdown links and numeric assertions were validated. No candidate installation, backend regression, CUDA tensor test, model download or inference was executed during planning.

The original six-document planning audit passes: six Markdown files, 26 local links/anchors, exact capacity/memory/storage arithmetic, and all six shard sizes/LFS hashes checked against their pinned metadata. Checksums of 156 existing notebooks, returned artifacts, source/archive, implementation/test/configuration files and earlier Markdown documents remain unchanged. These are planning/provenance checks, not the future candidate-host or model tests. The subsequently appended lessons file records the retrospective without changing the proposed implementation scope.

`git status` in the original workspace fails because `.git` contains only `upstream-checkouts`, with no usable repository metadata. The authorized canary implementation uses a verified sparse checkout at `build/m5-kaggle-canary-review`, based on the genuine M5 commit. Planning/evidence and implementation checkpoints are committed there on local branch `feat/m5-kaggle-upload-canary`. Original metadata and user evidence remain untouched; no remote branch changed. See the [canary handoff](../../validation/m5-kaggle-upload-canary.md#artifact-and-commit-provenance).

## Current implementation handoff

K0 has verified checkout provenance. The user completed K1's actual CPU upload test: the [run-2 review](../../validation/m5-kaggle-upload-canary-run-2.md) records five passing stages, exact tiny payload/member bytes and independently readable SQLite snapshots. The original dataset inventory shows all 14 gzip and two nested ZIP paths absent with expanded counterparts, explaining the first failure. R1's observed-path question is resolved and R2 passes for this upload; exact dataset version identifiers remain unavailable.

K2 through K7 implementation is delivered. The [actual run 4](../../validation/m5-kaggle-full-preparation-run-4.md) passes complete source/cleanup, all 88 candidate installs and isolated project build. Its probe exits zero and independently verifies every version/module hash, but stdout diagnostics cause JSON parsing to fail before all 97 focused/native checks. K4/K8/K9 acceptance remains open.

The [output-channel repair and continuation](../../validation/m5-kaggle-probe-output-repair.md) pass 27 focused checks and real local Jupyter wiring with controlled candidate/import/test outcomes. The user confirms the same session is still open. Paste the continuation file into one new code cell in the existing v3 notebook, keep Accelerator None and run only that cell. Return new evidence under `notebooks/run/4/continuation/`. No packages are downloaded or installed again; earlier artifacts and scientific semantics remain unchanged. K10 through K15 model/pilot gates remain later work.
