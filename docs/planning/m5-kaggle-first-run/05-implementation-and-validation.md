# Ordered implementation and validation contract

**Status: K0 provenance verified; K1's actual CPU canary passes; K2–K7 implementation/local validation delivered; K8 actual Linux/Kaggle run pending; K9 interim handoff updated.** K4's actual host acceptance and K8/K9 acceptance still require that run. The original planning phase made no notebook or Python changes. Model work below is conditional on actual evidence and belongs to M5-T02, not an automatic continuation of Run All.

## Work items and logical checkpoints

| ID | Work / proposed files | Depends on | Acceptance / checkpoint |
|---|---|---|---|
| K0 | Obtain a verified usable checkout or explicitly retain unavailable build-commit provenance. Preserve the supplied run and missing-file state. | None | Genuine branch/HEAD/base verified; no overwritten user evidence or invented Git history. Commit this six-document planning package when a real checkout is available. |
| K1 | Complete R1/R2 CPU input inventory and transport canary. | K0 provenance recorded | Actual upload preserves archive/member bytes; selected transport and dataset version recorded. If raw renamed payload fails, test one ASCII alternative before proceeding. |
| K2 | Add `scripts/build_kaggle_bundle.py`, member manifest and the passing transport; preserve canonical gzip/nested ZIP bytes and protected fixtures. | K1 | Built artifacts audited for exact closure, byte identity, safe members and baseline/build provenance. Commit: `build: preserve canonical Kaggle input bytes`. |
| K3 | Add one `scripts/m5_kaggle_preflight.py` helper and minimal notebook bootstrap; diagnose source before copying, record inventory and exact rejection reasons. | K2 | Reproduces the first-run failure with an explicit transformed/missing-source report; valid input succeeds; no model download/construction. Commit: `fix: validate Kaggle source delivery before setup`. |
| K4 | Use clean scratch venv, exact CUDA 12.8 candidate, full resolver/install records and installed-package provenance probes. | K3 | Linux/Python 3.13 closure, imports, `pip check`, source/installed distinction and package-byte checks pass. Concrete failures are fixed and affected checks rerun. Commit: `fix: isolate and record the Kaggle candidate environment`. |
| K5 | Move disposable source/env/cache/temp work to verified scratch; exact per-pool storage plan and evidence reserve. | K3, K4 | Working output excludes bulky scratch; shared filesystems not double-counted; no default weight download; full staging/path semantics explicit. |
| K6 | Add explicit stage states/root blockers, bounded owned command groups, incremental reports and handled-failure export in `finally`. | K3 | Timeouts/parsing failures/interruption preserve logs and reap descendants; summary distinguishes failed from blocked/not-run; completed ZIP can be verified off-host. Commit with K5: `fix: bound preparation work and retain recoverable evidence`. |
| K7 | Deliver `notebooks/recovery_m5_kaggle_preflight_v2.ipynb` instructions/defaults/display around the tested payload/helper, preserving the first notebook; keep zero outputs in the shipped file. | K2–K6 | User imports, attaches one private asset and runs fixed defaults; final output gives a root-specific action, one ZIP link and stop instruction. No source/runtime code duplicated unnecessarily in cells. |
| K8 | Execute preparation on real Linux/Kaggle; complete R3–R6 and actual GPU library diagnostics as the admitted stage permits. | K7 | Named focused/native checks and actual library/filesystem/export evidence recorded; no claim that mocks or CPU mode establish model acceptance. Commit K7/evidence after validation: `docs: record corrected Kaggle preparation evidence`. |
| K9 | Update `docs/validation/m5-kaggle-preflight.md`, `m5-kaggle-notebook-plan.md`, T02 evidence and the living implementation-plan handoff. | K8 | Supersede obsolete pending-inspection/auto-extraction claims; retain first failed run and keep T02 unaccepted until its actual model gate. Do not change T01 completion or later task counts without evidence. |
| K10 | Resolve R7 complete-envelope coverage and R8 tiny SDPA dispatch risk; review any required maintained/public attention compatibility change before model loading. | K2, K4, actual admitted T4 probe for R8 | Sound request/bound relationship and a supported efficient attention path for actual head/mask geometry, or an explicit feasibility blocker. Any backend change gets a separate reviewed commit and renewed affected tests. |
| K11 | Choose verified cache/local weight staging; complete R4/R5 for actual assets and durable export. If required, narrowly extend ModelFactory local-directory provenance. | K8, K10 | Pinned complete shards/metadata verified, offline loading cannot pick another revision, no hidden download/copy into working; changed backend tests pass. Commit only if needed: `feat: load verified pinned model assets offline`. |
| K12 | Add importable `scripts/m5_smoke.py`; materialize/review exact 24-slot matrix using existing structures/ledgers. | K10, K11 | Every permitted view/rendered/native request/seed/settings/slot origin reproducible offline; no pilot/main IDs or generations, no new store. |
| K13 | Prove smoke-wide per-call/retry count/deadline admission. Add a narrow pre-attempt guard to `recovery/attempts.py` only if caller-side reservation cannot protect the limits. | K12 | Scripted 24-attempt/time/retry/no-outcome-fabrication checks pass; default existing runner semantics unchanged. Commit K12/K13: `feat: prepare bounded smoke requests and attempt admission`. |
| K14 | Review and, if needed, improve actual peak/headroom and physical UUID evidence in existing backend JSON; perform bounded model smoke only after admission. | K8, K10–K13 | T02 evidence meets every required host/model gate within the screen and shared budgets, or remains honestly blocked with retained failure/partial coverage. Commit measured evidence separately. |
| K15 | Follow T03/T04/T05, including R10 storage growth and complete-schedule forecast. | Accepted K14 | Exact capability, full pilot and freeze gates; no recovery/main inference inferred from preparation success. These are later milestone tasks, not this repair's implementation scope. |

At planning completion, K0 was blocked for commits because the original workspace was not a usable repository. The authorized canary implementation now uses a verified sparse checkout at `build/m5-kaggle-canary-review`, from the genuine M5 baseline, on local branch `feat/m5-kaggle-upload-canary`. Original metadata and missing top-level files remain untouched. Planning/evidence and implementation checkpoints are committed there; see the [handoff](../../validation/m5-kaggle-upload-canary.md#artifact-and-commit-provenance). No replacement history was manufactured.

**Current work-item status:** K0 provenance is verified, with user-authorized main-checkout metadata/root-file restoration completed without losing existing bytes. K1's [actual run-2 canary](../../validation/m5-kaggle-upload-canary-run-2.md) passes all five stages. The [actual full-source run 3](../../validation/m5-kaggle-full-preparation-run-3.md) verifies all 143 original members, Linux CPU inspection/process cleanup and synthetic off-host backups, completing the full source transport question for this asset. K8 has partial actual evidence; candidate setup fails inside `ensurepip` before installation/provenance and the 81/16 scientific checks. The [bootstrap repair and v3 packet](../../validation/m5-kaggle-pip-bootstrap-repair.md) pass 25 operational checks, a real local isolated pip installation and exact-v3 Jupyter exports. Reuse the accepted dataset and return the next CPU run under `notebooks/run/4/`. K4's actual candidate criteria and K8/K9 acceptance remain open, with K9's interim handoff updated. K10–K15 remain later model/pilot work. Original notebook/source/results, scientific semantics and task counts are unchanged.

Build the companion artifact after approved source changes. Embed the resulting payload reference in the shipped notebook; avoid hashing an archive that contains its own generated checksum field. A member manifest and an external archive checksum can have distinct roles without circular provenance. Record actual source/build commit separately from the old baseline marker. Preserve earlier bundle versions; do not overwrite the user's returned evidence.

## Meaningful validation for the operational repair

These checks target observed and credible deployment contracts. They are not a coverage campaign or copies of the implementation. Existing scientific regressions remain required only where a changed module/configuration affects them.

| Area | Required cases | Evidence to retain |
|---|---|---|
| Transport | Actual CPU Kaggle canary; canonical gzip and nested ZIP bytes preserved; direct archive/verified tree only if supported. | Upload/version reference, received payload hash, complete member comparison. A local `ZipFile.extractall` tree is insufficient by itself. |
| Observed failure | Tree with `capacity_report.json` instead of `.json.gz`; at least one expanded nested archive; marker correct but expected compressed member absent. | Exact inventory/root failure and blocked dependents; no test skip masquerading as success. |
| Integrity | Correct marker with a modified Python member, gzip member, schedule or native metadata; corrupt/truncated payload; missing dependency fixture. | Admission fails before install/import with member-specific evidence. Canonical scientific inputs remain untouched. |
| Input safety | Duplicate ZIP entries, conflicting entries, absolute/parent/drive/backslash traversal, symlinks, absent/ambiguous inputs, unrelated attached model dataset. | No outside-source writes; bounded scan; unambiguous intended input selection. |
| Environment | Clean Linux/Python 3.13 resolver; wheel-only compatibility where required; exact Torch CUDA build and actual compiled architecture; package/import/native failures; unrelated base packages present. | Full closure and import origins; base environment remains unchanged. No broad inherited-package conflict treated as accepted. |
| Installed provenance | Outside-source import with source `PYTHONPATH` removed; installed module bytes compared with canonical source; source-mode tests labeled honestly. | Interpreter/path/package record, tested build identity and matching module hashes. |
| GPU diagnostics | Both unique T4 UUIDs, capability 7.5, finite tiny tensor, tiny NF4 native operation; tiny 16/4-head causal SDPA GQA versus expanded-KV eligibility/dispatch; wrong GPU, CPU Torch, missing native binary or changed build. | Actual subprocess logs and confirmed exits. Synthetic library diagnostics remain distinct from model generations; math fallback cannot be mislabeled efficient SDPA. |
| Storage | Shared filesystem roots, lower quota than pool free, insufficient working/scratch capacity, partial downloads/copies, reserve reached, full/unwritable output path. | Planned versus observed bytes, no duplicate-capacity arithmetic, handled report/export outcome. No automatic 4B or cap change. |
| Commands | Nonzero exit, malformed machine stdout, harmless stderr warnings, timeout with partial output, child/grandchild hanging, interrupt, deadline reached before start. | Separate streams, logical status, finite owned-tree cleanup and recovered export. No unrelated process killed. |
| Summary | One failed source prerequisite with installation/tests blocked; native skip or partial success; all required preparation stages pass while assets/smoke remain pending. | Actual executed counts, clear next action and null/unexecuted scientific gates. |
| Persistence/export | Real WAL/FULL diagnostic, committed replacement/backup tests, closed backup reopen, corrupt ZIP/backup rejection, fresh-session retrieve, no accidental Save & Run All duplication. | Exact backup/ZIP hashes, integrity/rows, retrieval action/version and external provider release acknowledgement. |
| Idempotence/evidence | Repeat preparation creates a separate output/scratch run; partial earlier evidence survives; model resume reuses completed exact worker calls. | No overwrite or reset of scientific spending/IDs/outcomes. Distinguish a new preparation run from a model regeneration. |

Controlled cases should exercise real files/SQLite/ZIP/processes wherever relevant, mocking only unavailable external package/GPU/provider behavior. Verify the export contents and original artifact hashes after failures. Then run the real notebook on Linux/Kaggle: controlled success cannot replace that acceptance step.

## Existing candidate-host commands

Use the candidate interpreter, the fully validated source/test closure and offline native metadata. Retain stdout/stderr, wall times, actual test counts and expected skips. These commands are planned for implementation; they were **not rerun in this planning turn**.

```text
<candidate-python> -m unittest tests.test_inference_preparation tests.inference_checks tests.durable_checks tests.attempt_checks tests.worker_checks -q
<candidate-python> -m tests.tokenizer_inference --tokenizer metadata/9B
<candidate-python> -m tests.tokenizer_inference --tokenizer metadata/4B
<candidate-python> -m tests.tokenizer_capacity --tokenizer metadata/9B
<candidate-python> -m pip check
```

At the reviewed source baseline, these are 81 focused checks plus 4/4/8 native checks, 97 total. Preserve the current focused-command 360-second maximum until actual host timing justifies a different operational timeout; the preceding Windows observation was 258.460 seconds. This is a preparation-command timeout, not the model-attempt 120-second scientific setting. The deliberate capacity overflow guard can emit its expected warning without failing admission.

Require nbformat validity, code-cell syntax, empty shipped execution counts/outputs, a real kernel execution of the handled-failure path, and real successful Linux/Kaggle execution of the admitted preparation path. If a helper changes, test it directly and the notebook's actual bootstrap/display path; avoid maintaining a stale second generator that can overwrite reviewed notebook fixes.

Run installed-package checks outside the source directory as separately specified in document 03. If local-directory/model-admission code changes, rerun focused inference/attempt/worker and installed tests affected by those changes, then actual smoke. Do not rerun broad M1–M4 analysis suites solely for Markdown or transport filename changes when source bytes are identical.

## Smoke validation and refusal cases

Before any model run, scripted checks must demonstrate these boundaries using the prepared requests and existing ledgers:

- Changed permitted view, rendered/native IDs, mask, seed, candidate settings, source revision or local model file is rejected before generation.
- Distinct physical devices are assigned before CUDA initialization; resident model processes remain serial; a visibility/UUID conflict stops admission.
- Request overflow creates no physical attempt; finite-score failure remains a blocked provider defect with uncertainty, without sanitization/retry.
- A completed invalid/wrong/cap-ending/timeout outcome persists and resumes exactly; infrastructure retry requires the existing established interruption and original request/bounds.
- A retry consumes the global ceiling. A 25th attempt, retry after exhausted time, or a new attempt after unresolved termination cannot start.
- Budget refusal before an attempt leaves that slot unexecuted; refusal after an interruption preserves the interrupted attempt and unresolved completion rather than inventing a final reply.
- Restart confirms the prior owner/provider exited; order/restart probes use new diagnostic call identities while keeping A's request/settings/seed equal.
- Memory acceptance uses full-envelope coverage and peak evidence, not only end-of-call free memory or tensor-download size.
- Source worker records, original exact replies, failed configurations, attempts, backups and allocation intervals survive off-host export/reopen; replay adds no physical generation.

Inspect real load and model logs when running the admitted smoke. No CPU mock can validate missing/newly initialized language weights, physical NF4 kernels, finite model scores, retained hybrid state or actual peak memory. Correctness screens belong to T03, while smoke verifies the named model/runtime coverage and does not estimate recovery effects.

## Failure decisions

| Trigger | Required response | Decision explicitly excluded |
|---|---|---|
| Transformed/missing fixture | Fix transport from canonical originals; keep inventory and failed run. | Delete the requirement, regenerate a scientific fixture, or infer a Python/GPU failure. |
| Dependency/wheel/import failure | Review that exact constraint/ABI, create a documented new candidate if necessary, rerun affected checks. | Blanket upgrade/downgrade all packages or mutate the Kaggle kernel. |
| 9B working disk insufficient | Use verified scratch or pinned read-only input, with exact staging/export accounting. | Automatic 4B selection or treating NF4 as a smaller download. |
| Full envelope not established | Complete R7 or retain the memory gate as unknown/blocked. | Accept a short prompt as proof, pad arbitrary tokens, lower caps or omit retained text. |
| SDPA chooses unsuitable math fallback | Complete tiny R8 probes and review a supported version/public attention route; record backend changes and reopen affected tests. | Equate `attn_implementation=sdpa` with an efficient kernel, blindly upgrade Transformers, add custom CUDA kernels or allocate a known giant score matrix as a first probe. |
| Hardware/runtime/headroom failure | Retain failure, stop admission, consider only the specified 4B fallback within shared budgets. | Pool configurations or split/offload the replica. |
| Time/count budget insufficient | Stop before starting; preserve partial/unexecuted coverage and release evidence. | Reset counters for a new notebook/account or add warmups outside the ceiling. |
| Provider/export contract inadequate | Complete the CPU persistence canary or compare another T4 host on recorded requirements. | Claim session-local files are durable or rerun study calls merely to save them. |
| All supported candidates fail | Keep T02/affected gate blocked and prepare limited-evidence feasibility reporting. | Mark the milestone complete because effort/quota was exhausted. |

## Evidence updates after implementation

Keep the user's first run immutable and refer to it as preparation failure with successful device inspection and a small filesystem diagnostic. For each later run, record artifact paths/hashes, source/build/candidate identity, actual commands/counts, root blockers, device/fs facts, allocation bounds and export/release receipt. Use existing worker tables for physical model/attempt/cost facts; preparation JSON remains a diagnostic export.

Revise living handoff text after real observations arrive. T02 stays blocked until the actual smoke/host criteria pass; T03 remains the first 90 slots, T04 the full 1,114-slot pilot, T05 the accepted freeze. Do not turn the user's quota availability into another permission blocker, or mistake it for a passing empirical/resource gate.

Acceptance review should be able to answer four separate questions from retained evidence: Did reviewed source arrive intact? Did the actual candidate environment and storage pass preparation? Did the model pass its complete-envelope smoke within resources? Are later pilot/freeze gates satisfied? Each answer must have its own evidence or an explicit unknown.
