# Run the course study on Kaggle

Upload **course-kaggle-dataset.zip** as a private dataset, attach it, and import
**course_kaggle.ipynb**. The offline ZIP includes the committed source, fixed
inputs, pinned Linux wheels and the original checkpoint revision. There is no
separate asset upload or setup notebook. Weights remain in read-only input
storage; only the installed environment and experiment outputs use working disk.

Complete the notebook's **one setup cell**, select **T4 ×2**, turn Internet
**Off**, then click **Run All**. For a durable background run, use
[Save Version → Save & Run All](https://www.kaggle.com/docs/notebooks).
No action switching is required. The sequence is:

1. Verify source and native asset identities; install the pinned ordinary package.
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

- Explicit, separate scope statements for **hardware**, **pilot**, **conditional
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
offload or pooled memory is introduced. CPU preparation downloaded assets only;
it did not load the pretrained model or establish GPU feasibility.

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

To resume, attach the same offline dataset and the latest resume ZIP. Update only
current provider facts/release evidence, retain the base bounds and authorizations,
then Run All again. The package detects the first unfinished stage and reuses
completed replies, including invalid and failed outcomes. A changed source packet
or saved input/configuration is rejected. Pre-install refusals retain assignment
receipts and become ordinary allocation ledgers on the next installed invocation;
an unknown earlier interval blocks GPU admission until reconciled.

## Reproduce the final analysis

Use Accelerator **None**, attach the same dataset and resume ZIP, and select
`ACTION="analyze"` in the setup cell. Internet can remain Off with the bundled
Linux candidate; analysis never loads weights or invokes inference. It verifies
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
bundled pinned Linux environment to reproduce figure bytes. New allocation/release
evidence produces a new analysis version instead of overwriting earlier results.

Advanced single-stage actions remain available for diagnostics. They use the same
runner and gates as Run All. Publishing, paid compute, changed scientific scope,
and altered frozen configuration retain their separate authorization requirements.
