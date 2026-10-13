# final-online-5 repair handoff

The [diagnosed storage refusal](course-kaggle-final-online-5-proposal.md) is repaired
in the existing online workflow. Rebuildable dependencies, installer temporary files
and original checkpoint downloads use measured session storage, while workers,
source, logs and exports remain in the output workspace. Refusals retain actual
paths, free/required bytes, timestamps and relevant mount observations.

The installer rechecks a completed installation after download interruption instead
of installing another venv. Native cache accounting credits one verified complete
file or one bounded partial prefix per shard. Initial and fallback staging share
the same actual-cache admission. An undersized cache can move to another measured
location while the interpreter and canonical scientific records remain unchanged.
Only a declared terminal 9B failure can permit reclaiming its rebuildable snapshot
for 4B; every recorded provider must be confirmed stopped and all scientific/asset
receipts remain. Corrupt assets still refuse with evidence.

Resumption now selects the candidate from existing gates before checkpoint staging,
reads saved state from its candidate bundle, and uses observational session bounds
instead of the old manual GPU-hour calculation. Native CPU preflight uses that
active candidate's launch settings. Notebook failure summaries retain the root cause,
repeated receipts do not collide, and portable exports preserve previous snapshots
while omitting disposable project-build duplicates.

The [focused CPU receipt](../../notebooks/validation/course-kaggle/final-online-5-repair-focused-cpu.json)
and [named check log](../../notebooks/validation/course-kaggle/final-online-5-repair-focused-cpu.txt)
record 84 passing final checks plus the retained passing real 24-row CPU controller
prerequisite. That controller was not repeated after setup-only edits. Coverage
includes the actual online `prepare` path with tiny pinned assets and command
doubles, failure-before-installation, cache relocation, verified installation reuse,
lost/damaged installation recovery, exact cache credit, safe fallback reclamation,
selected-child resume, the literal notebook bootstrap/export cells, unchanged gates,
native tokenizer/generation contracts and exact persisted-call reuse. Testing used
Windows/Python 3.11 and the existing CPU environment. These are engineering checks,
not native Kaggle dependency installation, physical T4 acceptance or model capability.

The original four [submitted files](../../notebooks/run/final-online-5/) remain
byte-for-byte intact. This failed setup generated no model outcomes. The approved
9B-first/4B-fallback design, compact prompt profile, 110,416+256 input/output bound,
600-second envelope-only deadline, ordinary 120-second deadline, historical 23
attempts and cumulative 71 scope are unchanged. No weights, GPU model calls, pilot,
freeze, main experiment or publication occurred during this repair.

Use the new matching notebook and lightweight dataset for a fresh first run;
retain the old submission as evidence. An old source-bound resume payload must not
be forced into the changed package. Later sessions use this same repaired dataset
and their matching latest export. [Setup, progression and resume instructions](../KAGGLE_COURSE.md)
describe the single Run All path and retained scientific gates.

Final package hashes and delivered-notebook execution evidence are recorded after
building from the committed implementation.
