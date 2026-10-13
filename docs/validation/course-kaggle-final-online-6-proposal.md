# Final-online-6: complete repair and continuation proposal

Date: 13 October 2026. Status: **proposal; production repair and updated upload
artifacts are not yet implemented**. The corresponding
[results analysis](course-kaggle-final-online-6-analysis.md) and
[CPU diagnostic receipt](../../notebooks/validation/course-kaggle/final-online-6-analysis.json)
establish the causes below.

## 1. Intended outcome

Deliver the same small online-first notebook/dataset interface. Run All should
verify both candidate inventories before costly setup, retain the measured 9B
rejection and its 22 actual attempts, automatically stage the already authorized
4B fallback, and advance through its original hardware, capability, pilot,
conditional freeze/main and reporting stages. Completed calls must resume exactly;
a scientific failure must still produce a truthful limited result.

This repair can eliminate the observed deterministic metadata, counting and
reporting defects and verify their recovery paths. It cannot guarantee model
quality, GPU headroom, provider availability, or error-free external execution.
Future errors must produce durable evidence and a bounded, clear resumption path.

## 2. Decisions that stay fixed

Keep specification §11.3 and the approved candidate order: pinned Qwen3.5-9B,
then pinned Qwen3.5-4B after terminal pre-main failure. The current 9B headroom
failure satisfies that fallback rule. There is no reason to introduce a third
model to repair a 90,240-byte metadata error.

Keep `course_compact_v1`, original peer permissions/views, current-source authority,
NF4/double FP16 loading, native tokenizer/template, sampling/seeds, 256 output and
64 outgoing prose tokens, complete 110,416-input-token bound, populations,
schedules, exact replay, persist-before-effects, missingness and scoring.
Keep two full-envelope probes with ≥1.5 GiB observed headroom, their 600-second
diagnostic deadlines, ordinary 120-second calls, bounded process cleanup,
first-90 thresholds, complete-pilot ≥98% validity and independent raw/effect audit.

Keep GPU-hour accounting observational and the controller session window bounded.
Restore no manual budget/proof/release forms. Preserve actual release uncertainty.
Do not add retries for malformed replies, wrong answers, length termination,
recorded timeouts or a measured hardware rejection.

The investigation itself performs no GPU/main execution. A future operator
Run All on T4×2 authorizes only the adopted fixed conditional stages. New models,
changed scientific/frozen settings, extra hardware attempts or publication remain
outside this repair scope.

## 3. Repair the checkpoint inventory at its source

**Files:** `scripts/m5_course_smoke_assets.py`, both candidate inspection receipts,
`scripts/build_course_kaggle.py`, existing setup/qualification tests.

Use native pinned Hub LFS sizes and SHA-256 for downloaded *file* inventory.
Retain index tensor payload bytes separately with an explicit name. For 4B:

```text
tensor_payload_bytes = 9,319,737,856
checkpoint_file_bytes = 9,319,828,096
header_and_prefix_bytes = 90,240
```

The existing `total_checkpoint_bytes` consumer denotes actual download/storage
bytes; correct it to native file bytes and add the explicitly named tensor total
only where its distinct meaning is needed. Do not alter native index contents,
apply a tolerance, guess a header allowance, round away differences, or disable
integrity verification. File SHA-256/size checks remain mandatory. Check the pinned
revision, declared shard set, positive native sizes and native SHA-256 identities.
Use file bytes in remaining-download, capacity and fallback admission calculations.

Validate **both** fixed candidates' small metadata before dependency or checkpoint
downloads in a GPU session. Reuse `native_checkpoint_files` and the existing source
manifest; save the received native inventory before comparing it so a refusal
contains expected/observed sizes, model, revision and shard names. Package creation
should also validate both pinned inventories using small network metadata, with
offline exact fixtures for deterministic checks. Do not add tensor downloads or
model construction to package validation.

Keep the two immutable revisions unchanged. Save a precise inventory error if
metadata differs. Retry only transient metadata transport errors with the existing
bounded setup mechanism; never retry a proven revision/hash/schema discrepancy.

**Acceptance:** the original 4B fixture is accepted with total 9,319,828,096;
the original 9B fixture stays accepted; altered revision/hash/size or omitted shard
fails before expensive work, with a retained diagnostic. Header arithmetic in the
[captured fixtures](../../notebooks/validation/course-kaggle/final-online-6-metadata/README.md)
explains the correction; it is not a new scientific weight conversion.

## 4. Make attempt accounting consistent everywhere

**Files:** `scripts/course_kaggle_bootstrap.py:qualification_choice`,
`scripts/course_kaggle_workflow.py:run_qualification`, existing preflight helper/tests.

Use the existing `smoke_attempt_usage` deduplication of native
`(call_id, number, started_at)` tuples. Prefer explicit `worker_paths` for
canonical databases; backup files remain retained evidence, never another physical
generation. Replace both raw `COUNT(*)` sums, not just their displayed number.
Apply the same canonical enumeration to hardware predecessor/quiescence readers
that currently use broad `worker-*.sqlite` globs. Avoid a second accounting store
or custom run/attempt identities.

Maintain a clear relationship:

```text
Root predecessor history: 23
Executed 9B hardware: 22 distinct attempts
4B predecessor admission: 45
Current cumulative: 45 + distinct new 4B attempts
4B new-attempt maximum: 24
Adopted cumulative ceiling: 71
```

Do not add the 9B rows again after setting a child prior to 45, and do not feed a
derived cumulative total back into root predecessor history. Correct the saved
67 only when the original canonical records prove it contains exactly 22 backup
duplicates; keep the original config/summary and a concise correction receipt.
Higher genuine documented prior usage must persist. A newly executed attempt
must always consume its candidate allowance, including infrastructure retries.
The two unused 9B positions cannot transfer to 4B.

**Acceptance:** canonical files alone, canonical plus backups, repeated references,
and extra historical snapshots all produce the same 45 for this incident. The
selected 4B config admits its unchanged 24-row matrix, to at most 69 cumulative.
Interrupted attempts and permitted retries consume actual entries. Changed start
times remain distinct physical attempts; equal call IDs alone never deduplicate
different executions. Genuine prior usage and 24/71 refusals still work.

## 5. Continue final-online-6 without repeating 9B or breaking source binding

This is an essential delivery requirement. The old payload embeds source
`ae0b98f`; a rebuilt packet will have a different manifested source. The current
notebook correctly refuses an arbitrary source mismatch. Simply telling the user
to attach the old payload, or to start an ordinary fresh 9B run, is insufficient.
Repeating the 9B matrix would waste compute and compromise the existing allowance.

Implement one **incident-specific predecessor adoption** using the existing
predecessor receipt and qualification code, not a general migration service:

1. Bind the accepted predecessor to final-online-6's exact original resume hash,
   source manifest and canonical native attempt identities. Verify ZIP/source/DB
   integrity, both observed T4 identities, confirmed process stops, the terminal
   9B headroom gate and its unaltered settings. Verify there are no development/main
   calls or frozen run to reinterpret. All these facts are available locally.
2. Verify that production changes are confined to setup, counting, continuation
   and reporting. Compare scientific core, model/revision/tokenizer/template,
   packet requests, settings, seeds and populations with the original. If their
   meaning changes, stop predecessor adoption on CPU before GPU allocation/work.
3. Retain the original submission/source/config/9B calls byte-for-byte as
   predecessor evidence. In the new source-bound bundle, admit the original 9B
   result only as a **failed predecessor qualification and counted history**.
   Never label it current-source hardware acceptance or reuse its model answers
   as 4B calls, development, main or experimental replay parents.
4. Record verified cumulative predecessor usage **45**, including the original
   23 and final-online-6's 22. Select the sole approved 4B fallback automatically.
   Its new workers start empty under the new manifested source and exactly its
   existing candidate settings. Preserve the original 67 claim and explain the
   backed-record correction.
5. Deliver this verified predecessor qualification/count in essential package
   metadata so the first repaired Run All needs no manual gate override. Keep the
   raw original resume artifact preserved and linked in the handoff. The lightweight
   dataset must not embed old environment binaries, checkpoint weights or duplicate
   experimental databases. This metadata derives from original ledgers rather than
   replacing them.

The adoption must be narrow: only this exact pre-freeze failed 9B incident and its
unchanged approved 4B fallback. Reject a different payload, missing/ambiguous raw
records, an audit defect, incomplete nonterminal hardware, frozen/main state, or
another model. This preserves source binding while avoiding unauthorized repeated
sampling. No new allowance or changed scientific acceptance rule is needed.

After the new 4B run starts, ordinary same-source resume remains the existing
workflow: attach the latest matching payload, install/download missing pinned
assets, reuse durable completed calls exactly, and continue unknown work subject
to per-call, per-candidate and session constraints.

## 6. Preserve storage repair and harden the actual fallback boundary

Retain final-online-5's measured scratch selection, owned installation reuse,
verified complete/partial checkpoint accounting, early phase capacity admission,
bounded range downloader, source provenance and atomic exports. The actual 9B
session verified these paths through weights staging; rebuilding them is unnecessary.

For 4B, size its cache against native **file** bytes and capture admission before
staging. Reuse the verified same-session interpreter, not another environment.
If space is insufficient, use the existing temporary-cache relocation or strictly
owned failed-9B cache reclamation after confirmed process quiescence. Delete only
rebuildable declared checkpoint cache files; preserve original model responses,
worker databases, source manifests, attempts, reports and unknown time. Do not
delete the user's original archive.

Bound metadata/download commands by the remaining session window. A network
interruption should retain a partial prefix for the existing downloader and lead
to the same 4B candidate on resume. A complete file is reusable only with its
native SHA-256 and size. An incomplete download does not consume a model attempt.
An immutable-integrity failure stops with evidence; it never selects a third model.

Test both entry paths: **same-session 9B→4B fallback** inside `run_qualification`
and **new-session 4B staging** in `course_kaggle_bootstrap.online`. They must use
the same verified inventory, selected child, prior count and source-bound settings.

## 7. Make progression and reports tell the same story

**Files:** workflow coordinator, smoke report summaries and notebook generator.

Before every candidate transition, save the existing coordinator summary with
active candidate, stage, previous gate reason and cumulative physical attempts.
On setup/fallback failure, update that same summary from the actual exception and
its stage. Retain the 9B limited report; add a compact final qualification summary
showing the 4B staging blockage, not an apparently complete 9B-only result.

Derive executed plan progress from canonical call/attempt records. Either remove
the unused `executed`/`outcome` flags from a clearly named prepared plan, or populate
them as derived export fields. Keep the full request evidence; create no new
authoritative status ledger. Label envelope rows as memory/numerical diagnostics
and ordinary rows as hardware answer diagnostics. Calculate largest prepared and
largest executed resident tokens from the actual hardware plan/ledger, including
envelopes. Report minimum transient free, ending free, allocated and reserved
memory separately; ending free must never override minimum-headroom failure.

At the end of Run All, cell 9 should display prominently:

```text
Candidate: 4B | stage: checkpoint preparation | stopped with retained evidence
9B: rejected by full-input headroom gate (22 attempts)
Hardware history: 45 / 71; 4B used: 0 / 24
Pilot: not started | Main: 0 / 6,280 logical outcomes; remaining unknown
Cause: precise saved exception and path to its log
```

The repaired successful path substitutes its actual stage/counts. A final notebook
cell can finish because it exported an error; make research completion a separate,
explicit status. Explain that a main-scope independent audit checking zero raw
calls is a valid empty-evidence audit, not a model/pilot pass. Keep existing logs,
heartbeat, elapsed time, actual attempt failure summaries and exported tracebacks.
Do not conceal exceptions, flood output with duplicate inventories, or require
the user to read a large trace to find the active stage.

## 8. Verification that targets the missed integration paths

Reuse existing tests and fixtures. Do not repeat broad CPU suites or allocate GPU
just to validate a metadata fix. Required focused checks are:

| Boundary | Required deterministic evidence |
|---|---|
| Native inventory | Real saved 4B/9B Hub fixtures and header arithmetic; both accepted; changed pin/hash/size/shard set refused with expected/observed receipt |
| Early package/setup checks | Both inventories checked before heavy download; valid archived index payload total is not mistaken for file bytes |
| Accounting | Real-shaped canonical/backup snapshots reproduce 45; selector, coordinator and admission agree; retries and genuine extra history remain counted |
| Same-session fallback | Real qualification controller with scripted 9B headroom failure, native 4B fixture and tiny staged bytes; 4B selection, capacity, asset receipt and original 24-plan admission verified |
| New-session fallback | Same saved transition restored through literal notebook/bootstrap cells; only selected 4B assets staged; blocked setup can resume without duplicate environment |
| Incident adoption | Exact final-online-6 evidence accepted as failed predecessor only; changed science, source, archive, frozen/main state or ambiguous history refused before GPU work |
| Persistence | Original 9B raw records unchanged; no provider invoked for completed restored calls; 4B never reads 9B calls as its results |
| Reporting | Interrupted fallback updates root status; executed plan reflects actual records; envelope is excluded from answer validity; 6,280 unknown main outcomes persist |
| Export/resume | Quiescent SQLite export, atomic prior ZIP preservation and exact restore; latest final stage/root reason survives |
| Exact delivered notebook | Five literal code cells exercised against final source manifest, installed CPU workflow and scripted transition; no uncaught error or misleading completion state |

The current analysis already reproduces both defects with zero GPU work. Those
CPU probes establish the regression fixtures; they do not test the repaired
implementation yet. Tiny fixtures must retain the real difference between tensor
payload and file header bytes. Mocking `native_checkpoint_files` to return success
would repeat the testing gap that missed this defect.

Hardware smoke itself already records actual GPU behavior. Do not re-run its
22 completed 9B calls during engineering validation. Native Linux full-size
downloads and 4B T4 fit/capability remain clearly marked unverified until the
operator actually executes them.

## 9. Implementation order and finished artifacts

Make three coherent changes, with proportionate local commits:

1. **Inventory/accounting repair:** correct 4B native file bytes, precheck both
   candidates, retain mismatch facts, unify physical counting and add focused
   regressions around real saved fixtures and backups.
2. **Continuation/reporting repair:** implement the narrow verified predecessor
   adoption, selected 4B resume and accurate stage/error/progression exports.
   Test same-session and restored-session fallback and preserve all original data.
3. **Delivery:** build a new source-bound online-first notebook and two-file
   dataset ZIP; run the exact notebook's CPU/scripted integration; publish local
   artifact hashes and a concise runbook, cell map and resumption instructions.

The final dataset should contain only opaque packed source and its manifest.
Pinned dependencies and checkpoints download on Kaggle. Essential predecessor
metadata is small; large original logs/database evidence stay in their preserved
archive and research repository. Keep the notebook an orchestration interface
over existing code. Do not introduce a new inference runtime, dashboard service,
attempt registry, store or milestone machinery.

The handoff must state: upload the repaired notebook and matching dataset, enable
Internet/T4×2, Run All; this incident starts the already permitted **4B** stage
automatically. Keep its latest results ZIP, resume payload and executed notebook.
Further sessions attach that payload with the same package. Successful hardware
does not imply successful pilot; successful pilot alone does not imply completed
main coverage. If 4B fails a scientific gate, the correct final product is the
preserved limited result, not a silently modified experiment.

## 10. Future errors: bounded response, not promises

| Future event | Required behavior |
|---|---|
| Temporary Hub/network failure | Bounded setup retry or saved partial checkpoint; retain root cause and resume same candidate |
| Changed/missing pinned metadata or corrupted file | Refuse before model execution; show expected/observed identity; retain evidence |
| Insufficient temporary/output storage | Measured refusal with path/free/required facts; use existing owned relocation/reclamation only when applicable |
| Session deadline/provider interruption | Quiescent export if possible; retain uncertain attempts; resume exact completed outcomes and permitted unfinished work |
| Actual 4B memory/finite/loading gate failure | Preserve measured terminal result; no pilot/main, no third candidate or extra allowance |
| Invalid/wrong ordinary research reply | Record and score under original rules; no repair/resampling |
| First-90 or complete-pilot failure | Limited result after the required audit; no freeze/main |
| Raw/effect audit or frozen/main failure | Stop with evidence; no candidate switching or configuration drift |
| Error during export | Preserve last complete export; write a distinct failure receipt; state which snapshot is safe |

The priority is a reliable, truthful Run All interface that finishes its authorized
work or gives an accurate, resumable limited result. The two causal bugs in this
incident are fully explained and reproducible. Empirical success of the 4B
research remains an open result, not an engineering guarantee.
