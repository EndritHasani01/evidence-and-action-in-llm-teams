# Course M5-T01 completion and hardware handoff

**Course M5-T01 is done: CPU preparation is implemented and verified.**
11 October 2026, Windows/CPython 3.11.9, implementation `3d1a19c` on
`feat/course-m5-inference-preparation`. The user approved moving remaining
physical R7 acceptance to [M5-T02](../todos/course/M5/M5-T02-course-hardware-smoke-and-memory.md)
and avoiding further speculative offline work. This is an engineering sequence
change under [specification Sections 8 and 11.3](../../PROJECT_SPECIFICATION.md#113-cumulative-resources-and-admission),
recorded in [plan Section 11](../IMPLEMENTATION_PLAN.md#11-course-living-handoff).
No scientific requirement, population, rendered input, model setting or
authorization gate changed. Full-envelope memory with at least 1.5 GiB free
headroom still precedes pilot admission. No weights, GPU, pilot/main, freeze,
paid compute or publication were used in this completion.

## Accepted preparation

Reuse [the original preparation checks](course-m5-inference-and-smoke-preparation.md):
64 affected source/64 ordinary installed checks, four native source/four native
installed checks, exact 4B/256/64 adapter/seed/state/terminal/provenance behavior,
and all 24 unexecuted smoke requests. All 29 production modules still match that
installed evidence. Thesis defaults/todos and accepted M1–M4 prerequisites are
unchanged; repeating their broad suites would add no changed-behavior coverage.

Reuse [the R7 supplement](course-m5-r7-offline-review.md): five source/five
outside-checkout native checks establish **109,851 input + 256 output reserve =
110,107 resident tokens** across all five families. Five loading checks verify
426 language shapes, sequential materialization and tied-head handling from
header metadata, with no weight payload. The 7,400,914,336-byte conditional
component subtotal and 3,214,021,348-byte loading-tensor allowance exclude
unbounded physical CUDA costs. Neither fit nor terminal infeasibility is claimed.

The refreshed builder carries those existing receipts and the complete proof
into the current source packet. `preparation_complete=True` is separate from
`physical_memory_accepted=False`, unknown peak/headroom, and false GPU/staging
admission. Historical `preparation_admitted=False` fields and blocked receipts
retain their original physical-memory meaning; they are not rewritten as passes.

## Reviewed packet and checks

`dist/course-m5-preparation-v3/course-m5-source.payload` contains **272 members**,
203,719,263 compressed bytes from committed source
`3d1a19cba62a286c5141af842986cff93d01c572`. SHA-256:
`24d00391f3255ff197ce4afad35d5444421a8c09325db80c9625c7abbfbc336d`.
The retained [manifest](../../notebooks/validation/course-m5-preparation/completion-packet/source-manifest.json.gz)
binds every member, pinned metadata and unchanged Linux/Python 3.13 package candidate.
The local packet is unpublished; earlier source-v2 and preparation packets remain intact.

| Executed changed-behavior check | Result |
|---|---|
| [Focused packet suite](../../notebooks/validation/course-m5-preparation/completion-focused-final-command.json), `.venv`, hash seed 419 | 11 passed, zero skips: complete input/provenance, pending hardware admission, unknown prior allowance, source refusal, LF/CRLF proof transport and code-drift rejection |
| [Committed packet build](../../notebooks/validation/course-m5-preparation/completion-packet-build-final-command.json), native CPU tokenizer | Passed; all 24 literal requests reverified, pinned metadata/lock and supplemental proof checked |
| [Literal notebook execution](../../notebooks/validation/course-m5-preparation/completion-notebook-final-command.json), native CPU environment, hash seed 419 | All three code cells passed outside the checkout; exact source review, SQLite diagnostic/export and two independent immutable read-only database reopenings passed |
| [Completion audit](../../notebooks/validation/course-m5-preparation/completion-audit.json), `.venv` | Passed: 1,730 protected files, 29 installed production modules, prerequisite receipts and historical packets unchanged; 525 local references/228 fragments valid; 12 done/9 blocked task counts agree |

The [unexecuted review notebook](../../notebooks/validation/course-m5-preparation/completion-packet/course_m5_cpu_review.ipynb),
[executed notebook](../../notebooks/validation/course-m5-preparation/completion-packet/executed.ipynb),
[result ZIP](../../notebooks/validation/course-m5-preparation/completion-packet/preflight-results.zip)
and [reopening receipt](../../notebooks/validation/course-m5-preparation/completion-packet/verification.json)
are retained. The notebook reports `prepared`, zero model generations and no
GPU/resource/freeze admission. Wrong source and existing output are refused.
The first refreshed notebook failed solely on Git's LF/CRLF representation of
the proof script. Its receipt is retained; the correction permits only those
source-text line endings and rejects changed code. Request/reply/artifact bytes
remain exact. The corrected packet and executed review supersede that failed
attempt without rerunning unaffected native capacity or runtime suites.

Rebuild from the implementation commit with pinned local metadata and a fresh
output using the [existing command](../../notebooks/validation/course-m5-preparation/completion-packet-build-final-command.json).
For local CPU review, set `COURSE_M5_PAYLOAD` to the exact delivered payload and
`COURSE_M5_OUTPUT` to a fresh directory, then Run All with Accelerator **None**
and Internet **Off**. Retain the ZIP/executed notebook and stop the CPU session.

## M5-T02 entry and acceptance

The [exact 24-slot matrix and resource handoff](course-m5-inference-and-smoke-preparation.md#packet-and-resource-handoff)
remain unchanged. Use the existing `ModelFactory`/`TransformersBackend`, serial
`ProcessProvider`, worker/attempt/allocation records and saved `CourseBudget`
with `regime="course"`; no new runtime or cost store is introduced. Preserve
distinct physical A/B/A/restart probes and the controlled-hang identity; never
use equal seeds to substitute replay. Refresh affected source/request provenance
if M5-T02 implementation or host changes require it.

Before any later loading/allocation, record explicit course-smoke authorization,
actual package/driver/device identity, scratch/output/environment/staging space,
durable exports, quota/provider duration/release terms and supported prior
allocation/attempt usage. Unknown inputs withhold admission. The unchanged
candidate downloads total 4,068,346,127 wheel bytes and the checkpoint index
describes 9,319,737,856 tensor bytes; neither is complete host disk admission.

Bound loading/diagnostics/smoke by the remaining cumulative **24 attempts and
1,800 allocated device-seconds**, including failures, retries, all assigned
load/setup/idle/release time and prior spending. Two assigned T4s allow at most
900 wall seconds before earlier spending. Keep 120-second attempt deadlines,
one-second TERM/KILL graces, bounded retries and at least 120 seconds for safe
release, increased when provider terms require it. Stop if the next admitted
attempt plus confirmed release cannot fit; no automatic extra calls are granted.

M5-T02 must combine the sound complete input proof with justified memory analysis
and actual-host coverage of loading, peak/cache growth, native workspace,
allocator/context occupancy and headroom. It also owns full candidate attention,
recurrent state/RNG/finite-output/decoding, timeout, persistence/export and
confirmed-release acceptance. Short successful outputs, meta traces or padding
cannot close R7. An unresolved check stays incomplete; a supported terminal
failure is required for the limited M6 route. M5-T02 remains blocked, and no
pilot, main, accepted runtime lock or freeze follows from finishing M5-T01.
