# Run the course study on Kaggle

Upload `course-kaggle-dataset.zip` as a **private dataset**, attach it to a new
notebook, and import `course_kaggle.ipynb`. Run the default `inspect` action with
Accelerator **None**. The notebook verifies its exact committed source and saved
course inputs before executing code. The dataset contains source, metadata,
fixed populations/schedules, the reviewed inference lock and CPU proofs; it
contains no weights, credentials or experiment results.

The notebook is an interface to the existing runner. Each invocation performs
one action. Its flags and authorization strings default to disabled/empty.
Authorization never replaces an acceptance or resource gate.

## Prepare once

1. Reconstruct earlier GPU spending, including shared preparation and failed
   sessions. Enter documented `[lower, upper]` GPU-hour bounds for every prior
   category, cumulative smoke hours/attempts, and evidence. A supported zero
   needs evidence; unknown is `None`. Keep these **same base bounds** on every
   resume. The software adds its original hardware/development/main ledgers once.
2. Verify current Kaggle quota, session duration and release procedure. The
   scientific ceilings remain **30 course / 100 overall aggregate allocated
   GPU-hours**, with the adopted 8/2/2-hour allowances. Two assigned T4s count
   twice the wall-clock time, including loading and idle time.
3. Set `ACTION="setup"`, Accelerator **None**, Internet **On**, and record the
   explicit pinned weight-staging authorization. This reuses the existing CPU
   asset builder, installs the pinned Linux Python 3.13 candidate and downloads
   the reviewed 4B revision. Model weights are not loaded. Download
   `course-assets.zip`; it contains target wheels and checkpoint files, not a
   copied environment. Its size is printed before handoff. Keep it private and
   observe the model's redistribution terms.
4. In a new session, attach `course-assets.zip` and the latest
   `course-resume.zip`, then run `ACTION="restore"` with Accelerator **None**
   and Internet **Off**. Restoration verifies pinned assets and reinstalls the
   ordinary project wheel. Select T4 ×2 only after this passes. This avoids
   spending the smoke allowance on downloads/installing packages.

A changed Kaggle image, unavailable pinned wheel, mismatched source or unknown
resource bound produces a retained blocker. Do not replace packages, reduce
contexts or raise ceilings to bypass it. The GPU candidate requires Linux
x86_64 **Python 3.13**, Torch **2.11.0+cu128**, and actual T4 devices; acceptance
is still established on the actual host.

## Execute one authorized action

Record the **actual UTC GPU assignment time** after selecting T4 ×2, the
verified provider allowance/duration, and the specific action authorization.
Set `ENABLE_GPU=True` for GPU actions. `max_work_seconds` defaults to 1,800;
the runner also applies cumulative resources, timeout/retry bounds, export time
and a 120-second provider-release reserve. It stops before any tighter bound.

| Action | What must pass first | What it does |
|---|---|---|
| `hardware` | Source/CPU gates, supported prior allocation and remaining cumulative smoke allowance | 21 native prepared probes, two full-envelope diagnostics, one controlled timeout; at most 24 cumulative attempts / 0.5 aggregate hour, including earlier smoke |
| `capability` | Actual-host loading/isolation/finite-output/headroom, complete-envelope R7 review, provider release | Exactly 80 prefix + 10 control slots, no recovery work |
| `pilot` | All 90 capability slots: ≥9/10 controls, one per family, ≥3/5 jointly correct prefixes and ≥14/20 final peers | Finish the existing 1,114 distinct / 1,178 logical development schedule; no new prefixes |
| `freeze` (CPU) | Complete pilot, ≥98% validity, independent audit, family/condition and timeout review, release, conservative resources | Freeze source/environment/templates/settings/inputs/analysis and the complete 20-world forecast; needs separate freeze authorization |
| `main` | Explicit accepted freeze, separate main authorization, current resource/provider admission | Execute/resume the complete 5,752-generation / 6,280-use main schedule in balanced blocks |

The hardware diagnostics use the proved **109,851 input + 256 output** envelope
on both replicas, forcing all output steps within separately recorded diagnostic
attempts. They do not modify scientific requests or supply pilot answers.
They may time out or fail memory; those failures remain evidence.

**R7 requires a supported review.** Read `hardware/report.json`,
`hardware/executed-plan.json`, raw attempt/load diagnostics and the included
capacity/loading proof. In `hardware_review`, record a justified complete live
memory upper bound that covers loading, native workspaces, allocator/context
occupancy and the complete allowed shapes, is at least the observed physical
peak, and leaves ≥1.5 GiB. Passing stress samples alone is insufficient.
The software also requires both complete diagnostics, finite/fresh-cache native
probes, loading/kernel/host checks and actual release. Leave `accepted=False`
if the evidence cannot support the complete bound. An unresolved review is an
open gate, not terminal infeasibility.

Before freeze, inspect `capability-gate.json`, `pilot-gate.json`, grouped failures
and the independently reconstructed pilot. Confirm the 120-second timeout is
adequate; a changed timeout/configuration requires renewed affected acceptance.
The existing forecast uses measured phase/condition costs on both replica
positions, the slower device, assigned idle time and a 25% margin. Each session
archives the actual physical UUIDs; stable replica positions support resumption
on another Kaggle VM. Missing measurements or excessive forecast withhold freeze.

## Monitor, save and resume

The action streams counts every 15 seconds. `progress.json` provides logical
coverage, attempts, literal replay uses, failures, resource bounds and resumable
work. Quiescent ordinary SQLite backups update `course-resume.zip` at ten-minute
boundaries and at final/safe stop. They include canonical source, inputs, frozen
packet where available, original workers and derived evidence; weight assets
stay in the separate reusable ZIP.

Download the current ZIP and the actual executed notebook **before stopping**.
Use Kaggle **Stop Session**, verify deallocation, and retain the real UTC release
time/evidence. Process/kernel exit does not establish provider release. Enter it
in `previous_session_release` at the next CPU/session action; original allocation
rows then close at that time. Unobserved inference around a crash stays uncertain.

Attach the latest resume ZIP in the next session, restore assets on CPU, and
repeat the same unfinished action with a new assignment clock. Completed valid,
invalid, failed and replayed calls are reused literally; the runner does not
resample them. Both worker files and their frozen bindings travel together.
Preserve earlier downloaded ZIPs. Do not combine workers from different exports,
course/thesis bundles or configurations. If the notebook setup cell fails, run
the final export cell explicitly after the action has stopped.

The notebook download/export cells do not invoke inference. Kaggle Quick Save
saves a notebook version without a fresh execution; **Save & Run All** starts
another invocation. Downloaded ZIPs are the portable resume evidence. Verify
the provider's current session/output behavior in
[Kaggle notebook documentation](https://www.kaggle.com/docs/notebooks) and
[official CLI save options](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md).

## Produce and reproduce results

After actual release, run `ACTION="analyze"` on CPU. It independently recomputes
gold, validates native requests/raw replies, reconstructs committed branch
effects/queues from archived replies, then calls the existing M4 analysis/report.
The original full main manifest supplies denominators even for a feasibility-only
or incomplete run. Development evidence is separate; invalid/failed slots score
zero, unexecuted slots remain unknown. Reports contain all seven exhibit groups,
CSV/JSON tables, literal cases/calls, deterministic plotting inputs and SVG/PNG.
Two fresh reproductions must agree byte-for-byte. Updated coverage gets a new
derived report directory; earlier reports remain available.

`analysis-receipt.json` links the latest report. A complete empirical label
requires an accepted freeze, all **6,280** main logical uses and the artifact
audit. A failed/open gate or partial run yields an accurately limited report.
The 20-world/four-per-family study remains exploratory; continuation repeats do
not add independent worlds. External publication/submission is separately authorized.

For a clean local CPU reproduction, extract `course-resume.zip` to `bundle`,
install Python 3.11+ (the captured CPU lock/target wheels can pin the environment):

```text
python -m venv cpu
<cpu-python> -m pip install -r bundle/source/configs/course-cpu-reproduction.txt bundle/source
<cpu-python> -I bundle/source/scripts/course_kaggle_workflow.py --root bundle/source --bundle bundle --config bundle/operator-config.json --action analyze
```

Use `cpu/Scripts/python.exe` on Windows or `cpu/bin/python` on Linux. No Torch,
CUDA, model weights or inference are required. The saved accounting clock,
bootstrap seed, native tokenizer metadata and original workers reproduce the
same tables/cases/plots. A stochastic scientific rerun is separate, requires
the accepted GPU environment and fresh authorization/resources, and does not
promise identical tokens across devices.

To rebuild this local upload package from a clean committed checkout:

```text
python -m scripts.build_course_kaggle --output dist/course-kaggle
```

The builder reuses the reviewed `dist/course-m5-hardware-v3` source/metadata and
candidate provenance. It adds pinned CPU rendering wheels, selects only required
fixture assets and packages the current committed source. No GPU work, weight
download, upload or publication occurs during a build.
