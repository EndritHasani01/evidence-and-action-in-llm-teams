# M4-T03 — Information inventories and retained-work references

**Status:** done

**Dependencies:** [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md). M1–M3 must have passed.

## References

- [Repository contract](../../../AGENTS.md) and [plan explanatory outcomes](../../IMPLEMENTATION_PLAN.md#explanatory-outcomes-and-costs).
- Specification [§2.2 exposure](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§7.2](../../../PROJECT_SPECIFICATION.md#72-what-information-and-work-survived), and [§10 limits](../../../PROJECT_SPECIFICATION.md#10-foundations-limits-and-contribution).
- Technical evidence: [evaluator separation](../../implementation-research/repository-and-validation.md#keep-evaluator-information-outside-peer-state). If inspecting archive witnesses, first follow [research rules](../../../research/AGENTS.md).

## Intended outcome

Offline evidence shows what information and work survived, with source-bound annotations and deterministic references whose assumptions cannot be confused with actual model correctness.

## Scope and boundaries

- Summarize all four prefix rounds' old-gold correctness, acquired remote coverage, history tokens and communication. Verify edited-owner v1 exposure from actual rendered requests without requiring model use or success.
- For L/B align first usable-call-boundary v2 receipt with correctness. Distinguish host injection/forwarding, no receipt, receipt without success, same-call/later success and correctness before authoritative receipt; preserve censored peers.
- For C/F measure boundary-held remote current records excluding the host-injected revision, unique acquired ID/version pairs and all delivery attempts. Tombstones are known; pending replacements are not. Acquisition after intervention is an outcome, not a covariate to remove.
- For receipts distinguish explicit source-bound old-value visibility, reconstructibility under a stated correct-candidate assumption, sufficient current raw evidence and unresolved cases. Numeric occurrence alone is not association; unresolved is not absence. Show offline correctness strata with denominators.
- Freeze a small conservative prose-association rubric with links to actual source/message evidence. No LLM judge, general exposure/dependency graph or claim of complete semantic provenance.
- Implement the §7.2 atlas and selected CPU sufficiency/ambiguity examples for Max (CPU only), Top-K reserves, local Prefix, complete Difference plus anchor, local Sort boundaries and BFS alternatives.
- Apply Prefix/Difference delta transport offline to the actual valid last candidate even when wrong, using specified index/sign rules. Preserve the residual-error identity; no earlier-candidate backfill or runtime repair.
- Record edit position/direction/magnitude, affected output owners, Sort crossings and BFS disconnection for limited descriptive tables/plots.

## Completion criteria

- Evidence inventory, preserved output and measured computation remain separate.
- Every reference labels its information view, correctness assumptions and unavailable-candidate cases.
- Rubric/annotations are deterministic or conservatively documented with source IDs, unresolved categories and denominators, ready for the M5 freeze.
- No diagnostic changes population inclusion, provides model feedback or invents another live arm.

## Validation and evidence

Check receipt timing/censoring, tombstone/pending coverage, repeated delivery versus acquisition, numeric coincidence without association, wrong old candidates and residual identities at endpoints/shard boundaries. Reproduce selected atlas counterexamples from safe independent CPU fixtures without overwriting archive evidence.

**Evidence:** Started on 6 October 2026 on `feat/m4-offline-analysis` from clean
commit `7059d7b`. Authority, the M1–M3 CPU gates and M4-T01 prerequisite evidence
were inspected. `python -S -m unittest tests.test_evaluate tests.test_outcome_archive -q`
passes all 27 prerequisite checks in 31.510 seconds, including reconstruction
from the original lifecycle workers. Information inventories will reuse saved
requests, validations and committed checkpoints; exact history token counts
require a tokenizer that reproduces the saved inputs. No new live state or
scientific configuration is needed. The complete M4 gate remains open.

The pure [reference core](../../../recovery/information.py) and conservative
[association rubric](../../implementation-research/information-diagnostics.md)
are implemented. `python -S -m unittest tests.test_information -q` passes 12
checks in 1.152 seconds, including both sizes, every numeric edit position,
directions and peer slices, wrong-candidate residual identities, unavailable
candidates, receipt censoring, tombstones/pending records, source association
and independent specified-view atlas examples. Worker/CLI integration and
retained inventory reconstruction remain open at this checkpoint.

Ordinary-worker integration now supplies `information_run` and `recovery analyze
--diagnostics`, independently or with `--estimands`. The six retained
[inventory cases](../../../tests/fixtures/information_tables.json.gz) include
both complete five-family runs, both full unknown main populations and the
stopped/resumed prefix. The public checkpoint serializer reads final committed
deliveries in the same read-only application snapshot, with no saver setup or
runner invocation. Receipt reconstruction uses only an actually retained old
candidate; C's archived cleared result never supplies that annotation.

`python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests tests.test_evaluate -q`
passes 52 checks in 17.490 seconds. The separate native harness verifies 160
prefix peer-round and 40 compact-boundary counts at both sizes, using existing
local metadata without weights. Full CPU and installed-package verification
remain in progress at this checkpoint. A retained-table check exposed BFS tuple
versus JSON-array comparison, and the automatic multi-megabyte dictionary diff
made three preliminary validations stall. Those runs were stopped and are not
passing evidence. Endpoint/reference outputs now use JSON arrays and a compact
case/table/row mismatch assertion; safe fresh reconstruction is complete.

Final conservative review keeps an unobserved delivery release/acquisition
unknown, rather than recording a negative outcome. Hand-calculated Sort
crossings and BFS leaf-bridge deletion checks cover both sizes. The final
`python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests -q`
passes all 26 checks in 13.912 seconds; all six retained cases and 200 native
history counts reproduce under hash seed 37. The dependency-free core runs
162 checks in 133.360 seconds: 160 pass and two optional checkpoint checks skip.
The complete CPU lifecycle regression and final installed-package verification
remain in progress at this review checkpoint.

The complete integrated CPU regression passes all 334 checks in 1,571.760
seconds, including all nine lifecycle checks. While it ran, two isolated
offline review fixes preserved unknown delivery releases and prevented an
integer association from matching the prefix of a decimal, mixed-digit number
or adjacent numeric arithmetic. The final association checks retain ordinary
sentence punctuation. The final 26 focused checks pass in 12.990 seconds and
fresh hash-seed-37 archive reconstruction reproduces all six cases unchanged.
Core and installed-package checks are being refreshed against these final
review changes; the earlier installed 81-check verification already passed.

## Completion and handoff

Completed on 6 October 2026. [information.py](../../../recovery/information.py)
and `recovery analyze --diagnostics` derive the required inventories and work
references from the existing schedule, saved requests, original replies,
validations and committed checkpoints. `--estimands` combines the M4-T02 tables;
`--tokenizer` optionally measures history content with a matching local tokenizer.
The [CLI/API documentation](../../../README.md#offline-information-and-retained-work)
and [conservative rubric](../../implementation-research/information-diagnostics.md)
describe every measurement and correct-candidate assumption.

The completed outputs retain all four prefix rounds, actual owner-v1 exposure,
L/B receipt timing/origins/censoring, C/F initial evidence and separate attempts/
acquisitions, source-bound visibility, hypothetical reconstruction, raw
sufficiency and offline correctness strata. Invalid/failed last candidates stay
unavailable; wrong valid candidates preserve their residual errors under the
offline delta reference. Cleared candidates cannot supply receipt reconstruction.
The six named-view atlas examples and edit footprints cover the requested
families, including CPU-only Max, Sort ties/crossings and BFS disconnection.
Evidence, preserved output and measured computation retain their existing
separate tables/records. No peer feedback, inclusion rule or live arm changes.

### Executed validation

| Check | Executed result |
|---|---|
| M4-T01 prerequisite outcomes/archive | 27 passed in 31.510 seconds |
| Integrated references/inventories plus evaluator regression | 52 passed in 17.490 seconds |
| Complete integrated CPU regression, including real controller kills | 334 passed in 1,571.760 seconds; all nine lifecycle checks pass |
| Final focused references/inventories after both narrow review fixes | 26 passed in 12.990 seconds |
| Final dependency-free core with site packages disabled | 162 checks in 133.911 seconds: 160 passed, two optional checkpoint checks skipped |
| Final installed-library verification outside checkout | 81 passed in 128.173 seconds; all twelve module locations/source bytes verified, plus installed CLI preserving 1,178 unknown development slots |
| Fresh retained information reconstruction, hash seed 37 | All six [cases](../../../tests/fixtures/information_tables.json.gz) reproduce unchanged from original M3 workers |
| Native tokenizer history measurements, hash seed 37 | All 160 prefix peer-round and 40 compact-boundary [counts](../../../tests/fixtures/information_tokens.json) reproduce at both sizes/all five families |
| Packaging and source consistency | Noneditable `pip install --no-deps .`, `pip check`, compilation and `git diff --check` pass |
| Documentation and protected-artifact audit | 402 local links/anchors across fourteen documents pass; all 29 task/index statuses and six milestone counts agree; specification/configuration/dependencies/research/vendor/prerequisites and all prior fixtures are unchanged |

The complete integrated regression started before the two isolated offline
review fixes. Final focused, core, installed-library and fresh archive checks
above verify the final code; execution/protocol code is unchanged by those fixes.
The three stopped preliminary diff-stalled runs remain excluded from passing
evidence. The corrected compact comparisons identify a case/table/row rather
than constructing an automatic multi-megabyte diff.

Environment: Windows build 26200, Python 3.11.9, SQLite 3.45.1; CPU environment
Pydantic 2.13.5, LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and
LangChain Core 1.6.6. Native counts used the separate existing metadata-enabled
environment with Transformers 5.12.0 and Tokenizers 0.22.2. No model weights
were loaded. Installed verification imports the twelve library modules before
adding checkout tests and runs `tests.test_information`, `tests.test_information_run`,
`tests.test_evaluate`, `tests.test_outcome_archive`, `tests.test_analysis`,
`tests.test_analysis_run` and `tests.test_estimand_archive`; the CLI subprocess
runs outside the checkout. These are CPU validation environments, not an M5 freeze.

```powershell
python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests -q
python -S -m recovery validate --core-only
.venv/Scripts/python.exe -m recovery validate
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.information_archive
python -m tests.tokenizer_information --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

Checkpoint commits: `a51c780` prerequisite/scope verification, `1ce962a` reference
core, `f3de741` ordinary-worker/CLI integration and retained evidence, `970539d`
unknown delivery/footprint review, and `c18833a` conservative numeric associations.
The completion evidence and handoff are committed separately.

**Next:** [M4-T04](M4-T04-policy-costs-and-boundary-rule.md) remains ready.
M4 has three of six tasks done; costs/boundary rule, uncertainty/missingness and
the reproducible report gate remain required before GPU use. The rubric is ready
for the later M5 freeze. Hardware/model feasibility, pilot, main execution and
empirical findings remain unexecuted.

