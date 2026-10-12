# Run the course study on Kaggle

Upload the new **course-kaggle-dataset.zip** as a fresh private dataset, attach it,
and import its matching **course_kaggle.ipynb**. Select **T4 x2**, enable **Internet**,
then **Run All**. No budget, approval or memory-proof forms are required.
With Accelerator None, the same notebook produces a CPU feasibility report.

The dataset contains only `course-kaggle-source.payload` and `source-manifest.json`.
Keep the `.payload` extension: cell 3 verifies and extracts it after session startup.
This prevents Kaggle from rewriting gzip fixtures during input preparation.
Attach only the matching compact dataset, plus the latest matching resume payload.

The controls cell normally stays unchanged: `ACTION="run_all"`, `SESSION_HOURS=10`,
and `RESUME_ZIP=None`. GPU mode is detected automatically. Run All on T4 x2 records
operator authorization for the fixed pinned-model stages and a conditional
unchanged freeze after the scientific checks pass. It does not authorize changed
frozen settings, paid services or publication. The controller reserves time for
export before its configured deadline; Kaggle may still interrupt earlier.

The sequence is hardware stress/finite/cache checks, first 90 development slots,
the full five-world pilot, independent raw/effect audit and configuration freeze,
the fixed 20-world main matrix, then analysis and reports. Hardware acceptance
requires both complete-input probes with forced 256-token output and at least
1.5 GiB observed free headroom. Capability thresholds, complete-pilot 98% validity,
exact replay, persistence, all population/seed/protocol rules and missingness remain.
A failed scientific check produces an accurate limited result with retained evidence.

Progress reports stage, recorded/remaining slots, physical attempts, replay uses,
failures and unknown outcomes. Installation/download output streams live. Original
command logs, tracebacks, environment receipts, raw replies and checkpoints travel
in the resume bundle. Ten-minute quiescent backups and stage-completion exports
preserve finished calls without resampling them.

Download **course-results.zip**, **course-resume.payload**, and the executed notebook.
The results ZIP contains the summary, reports/tables/figures and gate receipts.
The resume payload is an ordinary ZIP with a transport-safe extension and contains
source, exact inputs, original worker SQLite backups and debug logs. Do not unpack
it before attaching it to Kaggle. In another session, attach the SAME dataset and
latest resume payload and Run All. Inputs/source/configuration must match exactly.
After an interactive run, stop the Kaggle session normally.

Timing is observational: logs and original allocation/process/attempt records
support retrospective accounting. Notebook observation start/end does not prove
provider assignment/deallocation. Missing earlier/later intervals remain unknown;
call counts alone do not determine allocated GPU-hours. Historical budget limits
are not execution stops in this user-approved simplified course workflow.

For analysis only, use Accelerator None and `ACTION="analyze"`. It downloads no
weights, verifies saved requests/raw validation/independent gold/committed effects,
and reproduces reports twice. Unexecuted slots remain unknown; recorded invalid
or failed slots score zero. To reproduce locally, extract the resume payload with
a ZIP tool, install `source/configs/course-cpu-reproduction.txt` and the ordinary
source package, then run:

```text
python -I source/scripts/course_kaggle_workflow.py --root source --bundle . --config operator-config.json --action analyze
```

Earlier executed bundles continue with their original matching source packet.
The uploaded `final-online-1` notebook contained no model calls; its failed source
import and disabled-GPU configuration are preserved as debugging evidence.
