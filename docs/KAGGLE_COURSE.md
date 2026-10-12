# Run the course study on Kaggle

Upload **course-kaggle-dataset.zip** as a private dataset, attach it, and import
**course_kaggle.ipynb**. The small ZIP contains committed research code,
configurations, fixtures and essential metadata. Dependencies and the original
checkpoint are downloaded directly on Kaggle. There is no separate asset upload
or setup notebook. Internet must be available during installation/downloads.
The dataset ZIP exposes just **two files**: `course-kaggle-source.payload` and
`source-manifest.json`. Keep the `.payload` extension; cell 3 verifies and unpacks
the necessary research files locally after the session starts. Repository-wide
tests, documentation and historical logs are excluded. The mandatory three host
checks, their helpers and independent scoring reference remain included.

Create a fresh private dataset from this compact ZIP and attach **only that dataset**
(plus a matching resume bundle when applicable). Import its matching notebook. Attaching
the earlier expanded dataset as well would retain its file preparation overhead.
Existing experiment bundles must continue with their original matching package;
this source-bound compact release is for a fresh run.

Complete the notebook's **one setup cell**, select **T4 ×2**, turn Internet
**On**, then click **Run All**. For a durable background run, use
[Save Version → Save & Run All](https://www.kaggle.com/docs/notebooks).
No action switching is required. The sequence is:

1. Verify source; download/install hash-pinned dependencies and the pinned checkpoint.
2. Run the bounded hardware screen and both complete-envelope diagnostics.
3. Require the supported memory/headroom gate; run the first 90 development slots.
4. Require capability thresholds; finish the same five-world pilot and audit it.
5. Review pilot failures/timeout, forecast the entire matrix, and conditionally freeze.
6. Execute the fixed 20-world main matrix, with automatic bounded-window readmission.
7. Audit raw replies and committed effects; reproduce all report bytes twice.
8. Export the results and the complete portable resume/reproduction bundle.

A failed gate stops subsequent inference and produces a limited result with
original evidence. Insufficient provider time produces an incomplete result and
a safe resume bundle. The adopted population, output/context caps, masks, seeds,
replay rules and resource ceilings are unchanged. Completion cannot be promised
before the actual hardware, capability, validity and resource gates pass.

## Set up once

The first cell contains these required facts and permissions:

- Explicit, separate scope statements for **downloads**, **hardware**, **pilot**, **conditional
  freeze**, and **main**. A conditional freeze authorizes the unchanged candidate
  only after every acceptance gate passes. Main authorization never waives gates.
- Supported prior `[lower, upper]` GPU-hour bounds for development, setup,
  interruptions, other course/overall work and smoke; smoke attempt count and
  evidence. Unknown is `None`. Supported zero needs evidence. Keep the **same base
  bounds** on resumes; original worker allocations are added once by the code.
- Actual UTC assignment time, current provider allowance, maximum session duration,
  confirmation that earlier sessions were released, and their real release receipts.
- A supported complete allocator/workspace/loading memory upper bound and its
  justification. Stress-test success alone is insufficient for the approved R7 gate.

These facts are currently unresolved in the repository. They cannot safely be
filled with invented values. The default disables inference and produces a CPU
feasibility report; use Accelerator **None** for that mode. A complete, clean
pilot gets an automatic family/condition and timeout review. Any invalid/failed,
uncertain or ≥96-second pilot attempt needs the existing explicit review before
freeze, even if the pooled 98% validity threshold passes.

GPU work requires Linux x86_64 **Python 3.13** and the exact pinned candidate.
Changing the image, packages, configuration or physical layout reopens the
relevant acceptance gate. Two independent T4 replicas are required; no splitting,
offload or pooled memory is introduced. Setup verifies all 97 pinned candidate
package versions, native wheel SHA-256 values, ordinary installed module bytes,
and checkpoint revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` with native
LFS sizes/SHA-256 values. Two checkpoint shards download concurrently with bounded
HTTPS ranges. Installed inference subsequently uses the verified local snapshot.
Fresh wheel downloads are reclaimed after installation; weights, the environment
and results must still fit the measured disk space. No downloaded environment or
checkpoint is included in the resume ZIP.

On an assigned T4 ×2 session, downloading, installation and hardware validation
share the remaining **0.5 aggregate GPU-hour smoke limit**: at most 15 wall minutes
with no prior smoke usage. Slow Internet/setup can exhaust that gate. The notebook
retains a limited result and receipts instead of extending the limit. Downloads
and setup in subsequent accepted pilot/main sessions retain their cumulative
course/overall and provider limits.

## Monitor and resume

Progress prints every 15 seconds: recorded/unknown slots, attempts, replay uses
and invalid/failed slots. Every ten minutes, the runner drains in-flight work and
updates **course-resume.zip** from consistent SQLite backups. Each completed stage
also exports a backup. Local idle, installation, reviews, analysis and export
remain charged while GPUs are assigned. Stage transitions partition the same
assignment without claiming provider deallocation.

At the end, download **course-results.zip**, **course-resume.zip**, and the
executed notebook. The results ZIP contains `RESULT.html`, reports, tables,
figures and gate receipts. The resume ZIP also contains exact source, inputs,
settings, raw outcomes, original attempts and worker/checkpoint records.
For interactive runs, **Stop Session** and verify provider deallocation. Notebook
completion or local process exit is not a release receipt. Record the real UTC
release time and evidence for the next session.

To resume, attach the same small dataset and the latest resume ZIP. Update only
current provider facts/release evidence, retain the base bounds and authorizations,
then Run All again. The package detects the first unfinished stage and reuses
completed replies, including invalid and failed outcomes. A changed source packet
or saved input/configuration is rejected. Pre-install refusals retain assignment
receipts and become ordinary allocation ledgers on the next installed invocation;
an unknown earlier interval blocks GPU admission until reconciled. A new session
reinstalls and re-downloads the same verified candidate automatically. Setup reads
the original allocation ledgers before large downloads; accepted hardware is
counted once, and pilot/main resume does not reset or repeat its smoke allowance.
If a pre-install receipt missed the assignment time/device identity, add a
`bootstrap_refusal_assignments` entry to `RUN_SETTINGS` keyed by its JSON filename,
with recovered `allocated_at`/`physical_devices` and supporting `evidence`.
The original refusal receipt remains unchanged. Use actual recovered provider
facts; an unreconstructable interval remains blocked.

## Reproduce the final analysis

Use Accelerator **None**, attach the same dataset and resume ZIP, and select
`ACTION="analyze"` in the setup cell. Keep Internet **On** for the small CPU
environment install; analysis downloads no weights and invokes no inference. It verifies
saved requests, native raw validation, independent gold and branch-local delivery
reconstruction, then compares two clean report generations. Complete reporting
requires all 6,280 logical main uses, committed effects and the accepted freeze.
Missing uses remain unknown; recorded invalid/failed uses score zero.

For a local CPU reproduction, extract the resume ZIP and install
`source/configs/course-cpu-reproduction.txt` plus the ordinary source package in
an isolated Python environment. Run:

```text
python -I source/scripts/course_kaggle_workflow.py --root source --bundle . --config operator-config.json --action analyze
```

Original reports are retained. A different rendering environment may need the
pinned Linux rendering environment to reproduce figure bytes. New allocation/release
evidence produces a new analysis version instead of overwriting earlier results.

Advanced single-stage actions remain available for diagnostics. They use the same
runner and gates as Run All. Publishing, paid compute, changed scientific scope,
and altered frozen configuration retain their separate authorization requirements.
