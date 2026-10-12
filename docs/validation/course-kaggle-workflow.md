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
| `unittest tests.test_course_kaggle_assets tests.test_course_smoke_assets -q` | Windows, repository venv; tiny artificial weights/wheels and CPU allocation receipts | 12 passed; native revision/LFS/metadata checks, bounded asset preparation, packing/restoration, retained receipts and gate-refused assignment accounting |
| `unittest tests.test_course_report tests.test_course_report_archive -q` | Windows, repository venv; retained original CPU workers/reports | 14 passed in 589.073 s; unchanged synthetic/default reports and course coverage/uncertainty behavior |
| `pip check` | Updated repository CPU venv; pinned tokenizer libraries, no Torch/model weights | Passed |

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

**Limits:** scripted witness success is not pretrained-model capability. Tiny
asset fixtures load/download no pretrained weights; no actual Linux/T4 install,
quantized model, complete physical memory bound, GPU smoke/pilot/main, resource
reconciliation or freeze was executed here. The R7 review remains a mandatory
actual-evidence gate. A failed/open gate produces a limited result; software
delivery does not mark the course M5/M6 empirical tasks done. Earlier thesis
defaults, task files, populations/schedules and scientific authority are preserved.
