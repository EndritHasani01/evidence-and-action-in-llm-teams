# Lessons learned from M5 preparation and the first Kaggle run

Recorded 8 October 2026. **Status: original first-run retrospective retained; implementation and actual run-3 lessons added below.** The original sections' missing-checkout/pending-implementation statements describe the planning checkpoint. User-authorized Git/root-file recovery and the locally validated [v3 bootstrap repair](../../validation/m5-kaggle-pip-bootstrap-repair.md) subsequently supersede them without upgrading candidate/model gates.

This file records the lessons from preparing the notebook, reviewing the supplied first run, researching the platform and pinned runtime, and writing the implementation plan. It covers scientific evidence, source delivery, environments, storage, model feasibility, execution, resource accounting, validation and collaboration. The returned notebook and results remain the original evidence. This document does not implement the proposed repairs or upgrade any scientific gate.

## How to read the evidence

| Classification | Meaning in this retrospective |
|---|---|
| Observed | Recorded in the returned notebook, JSON, logs or inspected artifact bytes. |
| Previously validated | An earlier named local check passed within its documented environment and scope. |
| Reviewed | Established by inspecting source, configuration, documentation or immutable metadata. |
| Conditional calculation | Arithmetic is reproducible, but its application depends on stated runtime assumptions. |
| Proposed or pending | A design choice or experiment requiring implementation and actual acceptance evidence. |

The detailed evidence lives in [01 — First-run evidence](01-first-run-evidence.md), [02 — Platform research](02-platform-research-and-decisions.md), [03 — Preparation design](03-preparation-design.md), [04 — Model feasibility and smoke](04-model-feasibility-and-smoke.md), and [05 — Implementation and validation](05-implementation-and-validation.md). Earlier checks are recorded in the [original notebook plan](../../validation/m5-kaggle-notebook-plan.md). The [task contract](../../todos/M5/M5-T01-inference-and-allocation-preparation.md) and [preparation packet](../../validation/m5-inference-preparation.md) govern the scientific boundaries.

## Evidence and diagnosis

### 1. Diagnose the earliest failed prerequisite

The source stage rejected `tests/fixtures/capacity_report.json.gz`. Installation, candidate verification and tests then skipped. Four false booleans represented one dependency failure, not four independently observed defects. A useful report identifies the root failure and labels each dependent stage `blocked` or `not_run`; it does not send the user debugging packages that were never installed.

### 2. Preserve the distinction between failed, invalid and unknown

No model weights or generations were produced by this run. Dependency incompatibility, language-weight loading, NF4 behavior, finite model scores, memory, latency and capability therefore remain untested. In scientific accounting, a recorded final invalid or failed slot contributes its prescribed failure value; a missing or unexecuted logical use remains unknown. A preparation failure must not invent model outcomes or make incomplete populations appear complete.

### 3. Inspect user evidence before assigning blame

The first 20 cells of the executed notebook match the delivered cells after line-ending normalization. The twelve added cells are empty. There is no substantive user edit explaining the failure. The archive contains the missing gzip, while the selected Kaggle input folder did not provide its required path. Automatic archive processing is a leading explanation; the absent input inventory prevents a definitive conclusion about nested extraction or dataset-version differences.

### 4. Every passing check has a limited claim

The two host commands establish visible T4s and CUDA-enabled Torch. The SQLite probe establishes a small filesystem diagnostic. The earlier 22 controlled workflows establish the simulated cases they actually exercised, and the 97 Windows checks establish CPU behavior on their recorded source/environment. None establishes real Kaggle upload preservation, candidate installation or physical model acceptance. Validation summaries need named checks, actual counts, environment and skips.

### 5. Provenance, byte integrity and call identity are separate contracts

`SOURCE_COMMIT.txt` can identify an intended baseline while files are missing or transformed. Archive/member hashes establish delivery integrity; actual source/build commits establish provenance; existing call IDs and worker ledgers establish experiment identity. Each should serve its own purpose. A manifest is useful admission evidence without becoming another mutable experiment database.

### 6. Current observations take precedence over historical assumptions

The earlier CPU environment reported `torch==2.11.0+cpu`; the returned GPU run reports `2.11.0+cu128`. The current workspace also lacks usable Git metadata and several top-level files that exist in the historical source archive. Historical evidence and memory help locate contracts, but they do not establish current installation, current checkout identity or renewed authority. Record the difference rather than silently restoring files or repeating an obsolete diagnosis.

## Source transport and artifact integrity

### 7. A correct local archive can fail a cloud delivery contract

The original ZIP contains the required gzip and nested archives. Kaggle documents upload-side archive processing, so attaching that ZIP is not sufficient proof that every contained archive will arrive under its original name and bytes. Source packaging and platform delivery need separate acceptance checks. The next transport must survive the actual upload route before the notebook depends on it.

### 8. Validate before copying an expanded input tree

The notebook copied the discovered tree before rejecting it. The outer archive contains only 165,002,177 uncompressed member bytes, but its 14 gzip members expand to about 1.493 GiB and its two nested ZIPs expose about 1.345 GiB more contents. A transformed tree can consume gigabytes before setup starts. Record paths, sizes, candidate ambiguity and manifest differences first; materialize only an admitted source.

### 9. Repair transport from canonical bytes

Removing the compressed fixture requirement would merely move failure to a test that opens that exact path. Recompressing an exposed JSON or rebuilding an extracted SQLite archive would lose the original binary provenance and could conceal incomplete input. Preserve canonical scientific bytes, including protected fixtures, schedules and tokenizer metadata. A new outer transport may have a new checksum while its contained protected members remain byte-identical.

### 10. Test the real transformation with a small canary

Ordinary local ZIP extraction did not reproduce the failed platform contract. A CPU canary containing a tiny gzip and nested ZIP can cheaply establish what the upload actually retains. A renamed `.payload` is a candidate to test, not a guaranteed preservation switch; base64 ASCII is a bounded alternative if needed. CLI options for tabular conversion and directory handling do not prove arbitrary archive preservation.

### 11. Validate the complete deployment closure

A short required-path list catches some omissions while allowing modified modules or missing transitive fixtures to pass. Admission should verify a complete path/size/hash manifest, source/test dependencies and native metadata. Safe extraction also needs duplicate/conflicting-entry, absolute/drive/parent/backslash traversal and symlink checks. Bootstrap must verify the helper it is about to import before executing attached content.

### 12. Build provenance must describe the actual artifact

An edited implementation must not retain an old baseline marker as its claimed build commit. Record baseline and actual build identity separately, and leave unavailable fields explicit. Place archive checksums outside the archive when including them inside would create a self-reference. Preserve the first bundle and returned results instead of overwriting them with a repaired version.

## Environment and runtime reproducibility

### 13. Package inheritance is a broad operational choice

`--system-site-packages` exposes the whole base image, including unrelated distributions. An overlay can inherit incompatible constraints or make `pip check` fail for unrelated packages. This run did not observe that failure because installation skipped. A clean candidate venv offers a smaller reproducible closure; the notebook kernel can stay on its existing environment and invoke the candidate interpreter explicitly.

### 14. Root pins are only the start of a lock

Compatible root requirements and available root wheels do not prove that all transitive requirements resolve or their native binaries run. Record the resolver/install result, wheel URLs and hashes, installed versions, imports and `pip check`. Verify Linux/Python 3.13 native dependencies. Freeze the closure after it passes; change only constraints implicated by concrete failures instead of treating a blanket upgrade as a repair.

### 15. Choose CUDA builds from actual host facts

The observed driver, CUDA build, compiled architectures and T4 capability support reviewing the CUDA 12.8 candidate. They do not prove quantized Qwen execution. A current host probe is stronger evidence than an older CPU-image listing. Verify actual CUDA tensors and a tiny native NF4 operation in the candidate subprocess, then record its exit. These are synthetic library checks with zero language-model generations.

### 16. Installed-package validation must defeat source shadowing

Running in the source directory or setting its `PYTHONPATH` can import source modules even after installation. Test installed imports from outside the tree with source path injection removed; record module origins and compare installed bytes with canonical source. Label source-mode regressions separately. Otherwise a green test may validate a different build from the one deployed.

### 17. Recreate environments; move compatible artifacts

A populated venv embeds interpreter and path assumptions and is unsuitable as a portable CPU-to-GPU session artifact. Recreate it from a verified closure or compatible wheelhouse. Python 3.13 venvs also do not provide setuptools by default; ordinary isolated package builds avoid the earlier assumption behind `--no-build-isolation`. Keep model process factories importable and main-guarded rather than notebook-local for spawn-based execution.

### 18. Version-sensitive behavior requires source review

The pinned generation implementation places the custom finite-score processor before sampling warpers; there is no demonstrated ordering defect to fix there. A version change requires renewed review. Attention dispatch and quantizer exclusions are similarly sensitive to actual library versions. Inspect the implicated behavior before changing it; retain reviewed roots until evidence justifies a different candidate.

## Storage, persistence and export

### 19. Disk, VRAM, scratch quota and durability need separate plans

The input and working paths share a filesystem device, so their free bytes cannot be added. Large root/scratch free space is a pool observation, not a guaranteed per-session quota or persistence promise. GPU memory is a separate resource, and two 15-GiB devices do not provide one 30-GiB replica pool. Record each resource's actual constraint and validate its intended use.

### 20. In-memory quantization does not shrink original downloads

The pinned selected 9B files total 17.9924 GiB and the 4B files 8.6918 GiB. The first run ended with only 15.5397 GiB free in working output. NF4 loading does not reduce those shard downloads. Stage source, environment, cache, wheels, temporary transfers and weights on verified scratch or verified pinned input; retain reports, worker files and backups in the output area. A disk-layout problem does not justify changing models.

### 21. Account for temporary and duplicate storage

Selected-file totals omit partial downloads, cache/local copies, environment expansion, source extraction and export creation. Explicit Hub, pip and temporary paths should expose where those bytes land. Prefer one audited cache/snapshot strategy, reserve export space before work and measure observed growth. A small smoke artifact reserve is not a forecast for the full pilot and main study; derive those forecasts from actual worker growth.

### 22. SQLite details matter to backup interpretation

The returned diagnostic snapshots reopened off-host on disposable copies, passed integrity checks and contained the expected row. A zero-byte WAL and 32-KiB SHM beside a backup did not make the received main file unusable. Conversely, a small diagnostic does not prove live worker crash recovery. Close handles explicitly, distinguish closed snapshots from active WAL state, use the existing backup API for live workers, and preserve originals during inspection.

### 23. Off-host recovery is the durability test

Files visible in the current session, a saved notebook source, a downloaded ZIP and a persisted provider output are different claims. Retrieve and reopen the exact retained backups in a fresh location/session before declaring the path durable. Kaggle Save & Run All uses another execution session and can repeat work; verify output capture with a CPU canary instead of rerunning study calls merely to save them.

### 24. Useful failure exports need deliberate boundaries

The failed first run still produced readable diagnostics, which is a positive design result. Retain incremental reports and allowlisted logs/snapshots, finalize exports in handled-failure cleanup, and publish a ZIP only after member/CRC checks. Keep bulky source, environments and weights outside it. Final cleanup is best effort: an uncatchable kernel death or full disk can prevent export, so earlier evidence and space reserves matter.

## Model feasibility from first principles

### 25. Four-bit parameter labels hide important memory terms

Embeddings/output heads, sensitive FP32 paths, quantization metadata, KV/recurrent state, activations, workspaces and CUDA context all consume memory. Under the reviewed FP16 embedding/head and ideally packed four-bit MLP assumptions, 9B's embedding/head + MLP + full-cap KV subtotal is 14.0391 GiB before other allocations. A 15-GiB T4 with required 1.5-GiB free headroom allows only 13.5 GiB total use. This is a conditional warning, not a measured model failure.

### 26. A smaller model can retain the same dominant context cost

Both pinned candidates have eight full-attention layers, four KV heads and head dimension 256. FP16 K/V at batch one gives `32,768 × resident_tokens` bytes: 8 GiB at 262,144 tokens. The 4B fallback therefore reduces weight terms without halving that KV term. The mathematical size fallback reduces the retained bound by only 1,520 tokens, about 0.046 GiB of this KV estimate. Neither fallback is a universal remedy.

### 27. A concrete stress request and a complete-envelope bound answer different questions

The largest retained concrete request is 33,106 input tokens; the conservative target bound is 261,388 tokens including the 384-token output reserve. Passing the concrete case would not establish all admitted contexts fit. Acceptance needs a sound tighter live-input proof, coverage of the complete required envelope, or a retained feasibility blocker. Likely short natural outputs, arbitrary padding, dropped malformed history or lowered allowances cannot fill this evidence gap.

### 28. Requesting SDPA does not identify the selected kernel

Pinned source review predicts a math-fallback risk for mask-free 16-query/4-KV-head GQA on T4 SM75. A dense score tensor for 33,106 tokens and 16 heads alone is about 32.66 GiB in FP16 or 65.33 GiB in FP32. Actual model masks and dispatch remain unobserved. Both models share this geometry; the inspected newer Transformers helper does not establish a fix. Backend selection must be measured on the candidate's actual shapes and masks.

### 29. Cheap synthetic probes should precede expensive model experiments

Use tiny tensors with the real head geometry to inspect eligibility and actual dispatch, then compare the maintained explicit-KV-expansion path with finite outputs and toleranced equivalence. Cover causal prefill, decode and relevant masks. This can identify a known quadratic-allocation risk without loading weights or allocating a giant score matrix. Efficient attention still leaves the full-envelope KV and weight question unresolved.

### 30. Supported backend changes must preserve semantics and reopen affected gates

A compatible maintained version or reviewed public attention route may resolve a demonstrated dispatch blocker. It remains a proposed change until tested. Record backend/settings identity, verify causal/mask behavior and repeat affected native/request/isolation/model checks. Avoid global monkey patches, custom kernels and silent fallback. Cache/local-directory loading likewise must verify immutable revision, complete files and actual paths while preserving language-weight, NF4, precision, device and tie checks.

### 31. Measure the hardest memory moment and the actual loaded model

End-of-call free memory is not necessarily minimum free memory during prefill. Retain baseline/non-model occupancy, peak allocated/reserved values and device/process evidence; sampled polling does not guarantee unseen intervals. Audit every language weight and tied head, including expected dtype/device, rather than treating unused vision weights as an excuse for missing language weights. Put added evidence in existing backend/process/attempt records.

## Execution, independence and resource accounting

### 32. Equal seeds do not establish replay or independence

Each new physical call needs fresh KV/recurrent state, saved per-call RNG assignment and serial process ownership, with device visibility set before CUDA initialization. A/B/A/restart diagnostics deliberately create distinct physical calls even when A's request and seed match. Exact reuse comes from the prescribed persisted parent and matching request/settings/outcome evidence. It cannot come from global deduplication or a promise of seed-based regeneration.

### 33. Timeouts must cover the owned process tree

Killing or timing out the immediate subprocess does not prove installers, test workers or grandchildren stopped. Linux preparation commands need bounded termination/escalation/reaping of their owned process group and confirmed exits. Model termination remains the existing provider's responsibility. Parse machine JSON from stdout and retain stderr separately; harmless warnings must not corrupt JSON parsing or be discarded.

### 34. User quota availability and study budgets are independent

The user's stated GPU availability is sufficient context to avoid repeated quota questions. It does not change the study ceiling of 100 aggregate GPU-hours or shared development/setup/interruption reserves. Switching accounts, notebooks or sessions cannot reset scientific spending. Count assigned idle devices, installation, downloads, CPU checks performed during assignment, restarts, export and stopping according to the allocation contract.

### 35. Start and stop accounting require provider evidence

The reported 39.774 wall seconds and 79.548 aggregate GPU-seconds begin at notebook initialization and are lower bounds. Provider assignment/release timestamps are null. A child process exiting does not establish provider release. Retain assignment evidence, externally acknowledged stop and honest unknown interval bounds; do not describe a first-cell timer as a reconciled bill.

### 36. Admit work before it starts, including retries and shutdown

The smoke ceiling is 24 physical attempts and 1,800 aggregate GPU-seconds. Two assigned T4s yield at most 900 wall seconds; the 120-second stop reserve leaves at most 780 seconds before other overhead. The initial retry-bounded call can require 244 seconds, and a four-peer round 976 seconds. Admission must reserve permitted retries and termination before each smoke call. A preparation-command timeout and the 120-second scientific model-attempt bound have different roles.

### 37. Attempt ceilings must govern the provider's retry path

The existing provider enforces a bounded infrastructure retry, but that alone does not impose the smoke-wide count/deadline. Prefer a proven caller-side reservation; add only a narrow pre-attempt admission hook if necessary. Derive counts from authoritative attempt rows. A budget refusal before starting creates no attempt or fabricated failed reply; refusal after an interruption preserves its unresolved state.

### 38. Completed outcomes remain final

A wrong, malformed, cap-ending or timed-out completed answer cannot be resampled to improve the screen. Only the prescribed established infrastructure interruption admits retry. Retries consume physical attempts; replay adds no new generation; synthetic tensor checks consume allocated time while remaining distinct from language calls. Extra warmups or debugging generations cannot quietly exceed the 24-attempt ceiling. Partial required smoke coverage remains incomplete.

### 39. Scientific gates require their own populations and evidence

Preparation precedes actual T02 model/host acceptance; T03 starts with exactly 80 prefixes and ten controls; T04 covers the full 1,114 distinct / 1,178 logical pilot slots. Validity denominators must not inflate with retries or replays. T05 requires the complete schedule forecast, 12-hour reserve, 25% main-cost margin, durable storage and accepted immutable configuration. Changing model, template, backend, lock or timeout reopens affected gates. Failed configurations cannot be pooled into a passing candidate.

### 40. Honest infeasibility is a scientific result

The prescribed 4B and mathematical-size fallbacks have specific purposes and gates. They are not convenience choices for disk shortages or favorable outcomes, and passing 9B/40 remains preferable to changing models just to obtain 60 worlds. If supported paths cannot meet complete-envelope, runtime and resource requirements, preserve terminal feasibility evidence and use the limited-evidence reporting path. More available quota does not justify changing the scientific design silently.

## Validation, implementation and working process

### 41. Reproduce the failed contract, then validate the real platform

The next controlled cases should include a correct marker with a transformed/missing gzip, expanded nested archives, modified protected members, closure failures, shared storage, descendant hangs and export interruption. Exercise real files, SQLite, ZIPs and processes wherever relevant. Mock only unavailable external behavior and label it. A real Linux/Kaggle preparation run and off-host retrieval then close gaps the controlled suite cannot.

### 42. Tests and timeouts must reflect measured behavior

The earlier focused Windows command passed 81 checks in 258.460 seconds, exceeding the draft 240-second command bound; the final preparation bound became 360 seconds. That result informs operational planning without proving GPU-host timing. Report actual counts and expected skips rather than interpreting exit zero as every required check running. Expand regression testing when a changed module or unresolved failure warrants it; repeating broad scientific suites for Markdown cannot validate transport.

### 43. Small engineering details can distort validation

PowerShell quoting and default encoding can damage multiline Python or scientific Unicode; use a here-string and `python -X utf8 -`. A SQLite connection context manages transactions without necessarily closing the handle; close explicitly before backup/export checks. Broad subprocess mocks can intercept Windows platform/IPython imports; constrain their boundary. Normalize benign ZIP path representation while retaining genuine traversal cases. Keep stderr warnings separate from JSON stdout.

### 44. Keep one small implementation and test the delivered entry point

A thin notebook plus one ordinary preparation helper makes Linux subprocess/storage behavior testable. Verify the notebook bootstrap, display and failure-export paths as well as the helper. A stale generator can overwrite reviewed notebook corrections, so avoid a second divergent implementation. Reuse the existing worker ledger, checkpoint, backup and provider structures; neither this source failure nor the attention hypothesis requires a general orchestrator or serving-stack rewrite.

### 45. Give the user a concrete next action

The user should receive fixed reviewed defaults, one intended private asset, a clear CPU/GPU stage boundary, one result ZIP and a root-specific next action. The first run already found two T4s and working network metadata access; generic instructions to enable them would not address the source failure. Make technical choices from evidence instead of delegating dependency research to the user. Keep later model execution distinct from preparation Run All.

### 46. Planning has a deliverable and a stopping point

The requested planning phase calls for concrete file changes, ordered prerequisites, acceptance checks, failure decisions and commit checkpoints. Remaining research should name a question, minimal experiment, expected evidence and stop condition. The current request remains documentation-only. Implementation can follow the reviewed plan without treating speculative runtime risks as proven defects or repeatedly reopening settled user preferences.

### 47. Commit honestly in a verified checkout

Logical checkpoints make source delivery, environment isolation, diagnostics, backend changes and measured evidence reviewable. The current workspace cannot make genuine commits because repository metadata is missing. Record that limitation and the intended checkpoints; do not initialize replacement history, invent commit identities, delete `.git` or restore missing authority files as a side effect. A verified checkout is a prerequisite for future commit provenance.

### 48. Preserve successes and failures together

The first run verified useful host facts, a small WAL/FULL/backup diagnostic and readable exported evidence while leaving preparation incomplete. Preserve those positives alongside the source rejection, skipped stages and allocation uncertainty. Future repairs should add new versioned evidence and supersede specific assumptions, retaining the original artifacts and their hashes. An auditable history makes both acceptance and a limited-feasibility conclusion defensible.

## Rules to carry into implementation

1. Establish the current authority, source bytes and prerequisite evidence before changing behavior.
2. Fix the earliest failed contract and test its actual deployment boundary.
3. Keep observations, reviewed assumptions, calculations and pending experiments visibly distinct.
4. Validate the installed environment, complete model envelope and actual attention path separately.
5. Admit attempts and storage before spending; preserve outcomes, uncertainty and shared accounting.
6. Verify process exit, backup retrieval and provider release as distinct obligations.
7. Make the smallest supported change, reopen affected gates and keep original evidence intact.
8. Report only checks actually run, with one actionable next step for the user.

## Actual run-3 and bootstrap repair lessons

The full-source upload verifies every original member, including compressed fixtures. The tiny canary's result became full-size acceptance only after actual run-3 evidence; the accepted dataset can now be reused without another upload. Source transport, Linux process cleanup, package bootstrap and scientific checks still have separate outcomes.

A clean venv's implicit bootstrap is itself a deployment prerequisite. The run records an inner `ensurepip` failure without its lower-level traceback, so a distribution-specific explanation remains unknown. Creating the same plain venv without pip and installing the existing exact verified wheel offline is a narrow supported bypass. It preserves the reviewed candidate, avoids inherited kernel packages and needs no new bootstrap dependency. Real local success validates that primitive on Windows; Linux/Python 3.13 acceptance still belongs to the retry.

Review harnesses need the actual receipt shape too. A wrong field name can fail a reviewer assertion after the notebook itself succeeded. Preserve that failure, correct the harness and validate the unchanged delivered artifact; keep harness defects distinct from notebook/provider failures.

Recovery should preserve existing data before restoring metadata or missing files. A complete byte-verified backup and genuine Git history allowed restoration of all six missing tracked root files without replacing existing edits. Later logical commits now use the recovered main checkout, with the earlier isolated checkout and all returned evidence retained.

## Actual run-4 output and continuation lessons

A third-party import can exit successfully and emit documentation diagnostics on stdout. Run 4's strict whole-stream parser rejected those messages before the valid receipt. Give machine results a dedicated file and keep their size/schema/version/module-hash checks strict; retain human stdout/stderr separately. A parser failure and a package/import failure are different observed boundaries.

Preserve useful work in a still-open session. After verifying the admitted source and environment again, an explicit continuation can run the remaining CPU checks without repeating a 4-GB package download. Keep the failed run immutable and export the continuation separately; this needs neither a generic resume service nor changes to experiment ledgers. Source drift or a lost session still stops admission.

Short setup summaries should identify long commands starting. The quiet interval in run 4 contained successful package download, resolution and installation, not a hang. CPU setup timing and installed Torch CUDA-build metadata remain separate from measured T4/model feasibility.

## Actual run-5 acceptance lessons, 8–9 October

The [returned continuation](../../validation/m5-kaggle-full-preparation-run-5.md) turns the locally tested repair into actual Linux/Python 3.13 evidence: all 97 checks pass with zero skips, while the dedicated receipt verifies all 88 candidate versions and 28 installed module hashes. Review the exact delivered cell, original prior report, new ZIP receipt, command cleanup and off-host snapshots together. Preserve the old parser failure and its receipt; successful continuation adds evidence rather than revising an earlier outcome.

A warning's effect needs an executed result. Missing-`wrapt` startup diagnostics and the Transformers documentation messages persist, but all eight commands and all prescribed checks pass. The deliberate native overflow warning also accompanies a passing rejection test. Keep those messages and their unresolved origins visible; they do not justify adding an unreviewed dependency or weakening the scientific checks.

Stop repeating accepted preparation work once its evidence passes. The same-session continuation completes the remaining checks in 319.030 CPU seconds without another package download or install. Actual unittest durations, whole-command durations, whole-workflow time and intervening session idle time are different measurements; none records confirmed provider release or actual GPU feasibility.

Accepted CPU scratch is disposable. A new session or accelerator image must verify environment/model staging and its own GPU-host behavior; CPU provenance does not establish T4 kernels, full-envelope headroom, language loading or finite outputs. The next work is the already identified complete-envelope and tiny T4 compatibility gate. Keep T02 blocked and model generations at zero until actual model criteria pass, while retaining the user's existing authorization and unchanged resource ceilings.
