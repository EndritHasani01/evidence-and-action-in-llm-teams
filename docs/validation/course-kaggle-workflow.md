# Course Kaggle workflow: software delivery and CPU evidence

12 October 2026; branch `feat/course-m5-inference-preparation`.
Authority: specification Sections 8–11 and the adopted course contracts. Scope:
consolidate remaining M5/M6 engineering into usable local upload artifacts, with
no GPU/model execution, scientific-design change, accepted freeze or publication.

The [runbook](../KAGGLE_COURSE.md) describes the notebook, dataset, setup,
hardware/capability/pilot, freeze/main, progress, release-aware resumption,
portable exports and clean offline analysis. The scripts orchestrate existing
workers/storage/accounting/reporting; no second experiment runtime/store is added.

| Executed check | Environment | Result |
|---|---|---|
| `unittest tests.test_course_workflow_core tests.inference_checks tests.test_course_hardware_smoke tests.worker_checks tests.accounting_checks -q` | Windows, repository Python 3.11 venv; CPU mocks/processes | 68 passed in 195.723 s; capability dispatch barrier, adapter/cache isolation, bounded failures, worker/resource behavior |
| `unittest tests.test_course_kaggle_workflow -q` | Windows, repository venv; local-view witness and ordinary SQLite/LangGraph | 8 passed in 148.307 s; all 1,114 physical / 1,178 logical pilot rows, first-90 screen, branch-local archived-response reconstruction, missing/duplicate/seed detection, portable reopen and guarded CLI/notebook |
| `unittest tests.test_course_kaggle_assets tests.test_course_smoke_assets -q` | Windows, repository venv; tiny artificial weights/wheels and CPU allocation receipts | 13 passed; native revision/LFS/metadata checks, bounded asset preparation, packing/restoration, retained receipts, gate-refused assignment accounting and full unknown main scope |
| `unittest tests.test_course_report tests.test_course_report_archive -q` | Windows, repository venv; retained original CPU workers/reports | 14 passed in 589.073 s; unchanged synthetic/default reports and course coverage/uncertainty behavior |
| `pip check` | Updated repository CPU venv; pinned tokenizer libraries, no Torch/model weights | Passed |
| `tests.tokenizer_course_inference --tokenizer <pinned 4B metadata>` | Separate existing Python 3.11 / Transformers 5.12.0 / CPU Torch 2.11.0 environment | 4 passed; native template/IDs, settings and empty independent hybrid caches; no weights/GPU |

The initial workflow run found SQLite connections left open by transaction
contexts during temporary export/corruption tests; explicit closure fixes them.
The corrected run then exhausted local C: scratch while a report regression was
also running. [That failed receipt](../../notebooks/validation/course-kaggle/workflow-corrected.txt)
is retained. The passing final workflow uses one disposable branch reconstruction
at a time and no simultaneous full audit database. Old failed-test temporary
copies were preserved when automatic review rejected their cleanup. Disk
admission, read-only asset reuse and sequential setup/packing address the genuine
disk constraints; missing space stops and retains evidence.

Further package/notebook, native-tokenizer, outside-checkout CPU reproduction
and final artifact audits are recorded in `notebooks/validation/course-kaggle/`
at the delivery checkpoint. Artifact summaries bind the notebook/dataset to the
exact committed source; rebuilds require a fresh output directory.
The first fresh CPU run identified the optional Jinja2 template dependency and
an empty-worker control-audit indexing defect. The CPU requirements now include
pinned Jinja2; the audit skips unexecuted controls without creating workers.
The preceding final packet is `dist/course-kaggle-final/`; earlier failed delivery packets
and receipts remain distinct.

## Run All continuation

The user's subsequent request replaces action switching with automatic gated
progression. One offline ZIP now supplies checkpoint/wheels as well as source.
An actual assignment is partitioned at quiescent stage changes in the original
SQLite allocation records, with no gap, double charge or invented deallocation.
Only matching open intervals can be reused. Pre-install assignment refusals
retain receipts for reconstruction into those ordinary ledgers. Automatic pilot
review accepts only a completely clean audit with every attempt below 96 seconds;
other passing pilots still require the existing explicit failure/timeout review.
Allocation-aware finalization preserves release allowance and exports evidence
even when detailed analysis must be deferred to CPU.

Executed Windows Python 3.11 CPU checks:

- `unittest tests.test_course_run_all tests.test_course_workflow_core tests.test_course_smoke_assets tests.test_course_kaggle_assets -q`:
  **21 passed in 17.271 s**. Continuous intervals, worker adoption, failed-gate
  stopping, freeze-before-main order, bounded native downloads and inherited
  capability/asset behavior. All device facts are explicit artificial fixtures.
- `unittest tests.test_course_kaggle_workflow tests.worker_checks tests.accounting_checks -q`:
  **45 passed in 311.381 s**; [receipt](../../notebooks/validation/course-kaggle/run-all-integration.txt).
  The complete scripted pilot and original saved-response/effect audit still pass;
  worker, course/thesis resource and replay behavior remain covered.

The first focused check exposed missing checkpoint tables in newly created
allocation-only successor files. Successors now initialize through the existing
DurableRunner public path, so later reads stay genuinely read-only. The corrected
checks above pass. Bare bootstrap source verification is now stdlib-only; actual
ordinary installed provenance is checked after restoration.

The packaged native checkpoint is downloaded and checksum-verified on CPU only.
No model loading, new GPU session, accepted scientific freeze, main experiment or
publication is performed. Literal notebook/offline delivery checks are recorded
at the final artifact checkpoint. Prior resource and supported R7 evidence remain
required inputs, not inferred zeros or automatic stress-test acceptance.

The packaging refinement verifies both immutable checkpoint shards concurrently
with bounded HTTP ranges and native LFS hashes, retaining partial downloads for
resumption. Fourteen focused asset checks pass in 3.224 s. Six Run All checks pass
in 2.842 s, including evidence-required recovery of a missing bootstrap assignment
clock into the ordinary allocation records without altering its original receipt.

The literal notebook's first CPU execution exposed an inherited Jupyter inline
plotting backend unavailable in the isolated report interpreter. Both the child
environment and ordinary CLI now select Agg explicitly. A Windows-held derived
ZIP is preserved while a fresh complete snapshot is published. Kaggle-expanded
resume ZIPs are detected before source selection, preserving worker bytes and
avoiding an accidental fresh experiment. Seven focused Run All checks pass in
2.952 s, including literal extracted-resume detection.

**Limits:** scripted witness success is not pretrained-model capability. Tiny
asset fixtures load/download no pretrained weights; no actual Linux/T4 install,
quantized model, complete physical memory bound, GPU smoke/pilot/main, resource
reconciliation or freeze was executed here. The R7 review remains a mandatory
actual-evidence gate. A failed/open gate produces a limited result; software
delivery does not mark the course M5/M6 empirical tasks done. Earlier thesis
defaults, task files, populations/schedules and scientific authority are preserved.
