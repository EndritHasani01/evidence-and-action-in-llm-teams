# Prompt 2 — Research a practical Python and Kaggle execution workflow

Work in `E:\Github\recovery_blueprint\recovery_blueprint` on
*Recovering Distributed LLM Teams After Information Changes*.

This is research session 2 of 3. The scientific candidate is in
`docs/proposals/thesis-study-recommendation.md`. Read it fully, verify that it
exists, and use its selected design as the working proposal. Do not assume the
older four-cell or six-cell numbers remain selected. If a prerequisite is
missing, identify it explicitly and complete independent technical research;
do not manufacture an approved design.

Your objective is to establish exactly how the study can be implemented and run
intuitively: **ordinary `.py` scripts contain the logic; one thin main notebook
calls them; Kaggle downloads preparation assets online; progress stays visible;
work is durably saved during execution and every code cell ends with an
appropriate checkpoint or preparation receipt.** Produce a technically grounded
Markdown design, not implementation.

## Authority and boundaries

Read the current `AGENTS.md`, `PROJECT_SPECIFICATION.md`, relevant living
implementation-plan sections, `README.md`, implementation-research synthesis,
and the scientific recommendation. Inspect the actual relevant code and the
existing Kaggle/I-01 runbooks, notebook builders, setup/download path, workers,
stores, progress UI, exports and continuation handling. Distinguish dated
historical status from current evidence.

The working scientific proposal is not yet adopted. Preserve existing source,
specification, configurations, notebooks, releases and experimental artifacts.
Do not implement the new workflow, load a model, perform inference, use GPUs,
download weights, run experimental stages, create cloud jobs or publish/upload
anything. Metadata/source reading and small CPU-only scratch probes of a
specific library behavior are allowed; document their environment and limits.
Do not install a speculative production stack just to research it.

Investigate current technical facts using official primary documentation,
maintained source and release records. Check existing pins before suggesting
changes. Do not treat an old lock, search snippet or vendor example as proof
of compatibility. Keep actual-host/GPU acceptance pending where it cannot be
established without execution.

## 1. Research the smallest reusable implementation

Map the proposed scientific stages to the existing Python implementation.
Identify what can remain unchanged, what needs scoped adaptation, and what is
unsupported. Give the smallest credible file/module map with clear function or
CLI responsibilities, inputs, outputs and persistent side effects. Prefer the
current durable runner, identifiers, configuration, stores and export code.

Keep task generation, peer views, scheduling, model calls, persistence,
analysis and reporting in Python. The notebook should provide understandable
orchestration and inspection. Its unavoidable initial download/bootstrap code
should be small; avoid embedding a second implementation in notebook cells.

Compare a small in-kernel Python facade with subprocess/CLI calls where process
isolation, environment control or progress needs make the choice consequential.
Select one primary approach using actual repository constraints. Do not add a
generic backend registry, workflow engine, coordinator service or persistence
layer for hypothetical platform support.

## 2. Make online bootstrap concrete

Design the path from a fresh Kaggle notebook to a ready study without manual
uploads of model weights or dependency bundles. Research:

- How the first cell obtains the exact project source or package before project
  helpers are importable. Prefer existing hosting and release mechanisms.
- Reproducible source revisions, dependency pins, project configuration,
  tokenizer/configuration files and model-weight retrieval. Separate small
  metadata inspection from expensive assets and model loading.
- Existing caches, resumable/partial downloads, finite retry/deadline behavior,
  disk requirements, installation failures and source/environment mismatches.
- Private source/model access if needed, using appropriate notebook secrets
  without exposing credentials in code, URLs, logs or exports. Do not assume
  the repository is public or invent a downloadable release URL.
- What must be downloaded again in a new session and what can safely be reused.
  A cache hit must not imply that the source or model revision is correct.

Select a primary delivery route and a minimal fallback. Explain unavoidable
operator inputs. If the chosen source is not currently accessible from Kaggle,
state the missing arrangement explicitly; proposing public release does not
authorize publication. Keep new run setup online-first. Restoration of an old
checkpoint is a separate input problem, not a reason to require pre-uploaded
model assets for every fresh run.

## 3. Verify model and host feasibility on paper and source

Research the intended Qwen3.5-9B and IBM Granite 4.2-8B paths independently:
Transformers support, text-only loading, native templates, direct/thinking mode,
termination, precision/quantization, attention/recurrent behavior, token limits
and fresh per-call state. Identify required differences without abstracting
two concrete paths into a framework. Library-version fields inside a checkpoint
are evidence to inspect, not necessarily minimum supported versions.

Compare realistic Kaggle GPU arrangements and one minimal alternative only
where useful. Derive memory and disk estimates conservatively, including
unquantized components, caches/state, temporary tensors, workspace and the
headroom gate. Model weights fitting is insufficient. Compare sequential model
blocks and two-device scheduling, avoiding a permanent model/device confound.

Check Kaggle's documented environment, networking, output/storage and session
behavior from primary sources. Account-specific quotas and actual remaining
session time must remain operator-supplied facts. Do not assume a fixed free
GPU entitlement, available device or session duration. Distinguish elapsed
wall time, allocated GPU-hours and paid cost.

## 4. Storyboard the entire notebook

Choose a practical finite cell sequence for the selected study; do not copy the
course's cell count or create a giant cell that hides the whole campaign.
Provide a table with **every proposed cell** and these fields:

1. Human-readable title, purpose and short explanation.
2. Python function/CLI called and the few necessary operator settings.
3. Preconditions, permitted scope and maximum work/calls.
4. Progress displayed while running and the completion summary.
5. Files or state committed; checkpoint/receipt/export produced.
6. Behavior on success, scientific failure, infrastructure failure and rerun.
7. Whether Run All proceeds, stops at a resource/integrity gate, or awaits a
   separately authorized stage.

Cover source/bootstrap, environment inspection, asset downloads, configuration
inspection, input preparation, hardware readiness, qualification/development,
bounded main batches, analysis, reporting, export, resume and shutdown. Keep
future GPU cells specified but unexecuted. Make full request/response and peer
trace inspection possible without flooding the normal notebook output.

Show a first-run walkthrough and a resumed-run walkthrough. Explain how Run All
is convenient **within the scope actually authorized**, without silently
crossing from development into main inference. Do not require approval for every
ordinary cell or batch when the complete unchanged stage is already authorized.
If an entire fixed campaign has been explicitly authorized subject to objective
gates, respect that scope rather than inserting repeated approvals. Gate
success alone must never substitute for the initial execution authorization.

## 5. Specify progress, checkpoints and recovery precisely

The notebook should not appear frozen during downloads, installation, model
loading, generation or export. Propose concise heartbeat/progress displays with
elapsed time, current stage/model/world, physical attempts, logical completion,
remaining scope, failures, unknowns and checkpoint location. Use actual totals
where known and honest estimates elsewhere; avoid fabricated ETA or percent.

Distinguish three layers:

- **During calls:** durable raw outcome persistence before effects; no completed
  call is regenerated on resume.
- **After every code cell:** a readable progress summary and durable
  checkpoint or preparation receipt. Before a scientific store exists, do not
  pretend a download receipt is an experimental checkpoint.
  Every bounded scientific cell should leave a consistent portable checkpoint;
  choose lightweight handling for inspection and preparation cells.
- **Portable recovery:** a consistent downloadable backup containing the state,
  raw evidence, configuration, identities and analysis inputs needed to restore.

Use existing stores as the source of truth. Explain whether an export after
each bounded cell is affordable; avoid repeatedly archiving model weights,
caches or redundant copies of all history. Distinguish process exit from GPU
deallocation and a displayed download link from a completed external download.

Work through interruption during a call, after raw persistence but before
effects, between cells, during export, after kernel restart and after session
loss. Define idempotence, completed-cell reruns, exact restore, bounded
infrastructure retries, uncertain spending and mismatch refusal. Do not mutate
historical campaigns or reset allowance by changing a directory.

## 6. Reconcile execution cost with the science

Recalculate the exact stage/attempt schedule for the selected candidate,
including readiness and reloading costs. Estimate the number of sessions and
checkpoints under several realistic runtime assumptions. Separate measured
course timings from prospective estimates for new histories/models. Include
downloads, installation, loading, idle allocation, export and interruption
reserves. Show whether the target and any scientifically valid fallback can
fit; do not hide an infeasible plan behind automatic continuation.

If a technical finding requires a scientific change, propose it explicitly
with its consequence and alternatives. Do not quietly alter sample size,
conditions, call limits, model mode, retention, scoring or retries to make the
notebook easy to implement.

## Deliverable and completion criteria

Create **`docs/implementation-research/thesis-online-execution-design.md`** with:

- One recommended execution architecture and reuse/change/exclude table.
- Primary-source compatibility findings with dates, exact versions where
  verified, evidence strength and remaining actual-host gates.
- Minimal `.py` responsibilities and interfaces, a complete notebook-cell
  storyboard, illustrative progress output and first-run/resume walkthroughs.
- Online bootstrap/download and private-access plan, storage/checkpoint/export
  contract, stage transitions and concrete failure handling.
- Reconciled call/storage/memory/runtime tables and decisions needed by the
  final specification session.

Use diagrams, tables and short proposed code/command examples only where they
make behavior concrete. Label proposed commands and APIs as unimplemented;
never present them as commands already verified to work. Avoid speculative
infrastructure and a generic multi-cloud tutorial. Verify links and arithmetic.

Finish with the recommended operator experience, the deliverable path, what is
established versus still conditional, and the exact inputs handed to Prompt 3.
