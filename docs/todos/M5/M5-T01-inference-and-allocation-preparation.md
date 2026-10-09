# M5-T01 — Inference backend and allocation preparation

**Status:** done

**Dependencies:** [M4-T06](../M4/M4-T06-reproducible-report-and-cpu-gate.md). M1–M4 must have passed.
M4-T06 completes on 6 October 2026 and the
[M1–M4 CPU audit](../../validation/m4-cpu-gate.md) passes. The
[report handoff](../M4/M4-T06-reproducible-report-and-cpu-gate.md#completion-and-m4-gate)
supplies fixed case/annotation rules, analysis settings, assumptions, exact
original-worker reproduction and synthetic reports. This unblocks CPU
preparation only. Actual language weights, state/RNG and raw decoding,
finite outputs, T4 memory/headroom/timing, accepted-host persistence,
capability and complete-schedule allocation remain unverified M5 work;
execution still requires its explicit authorization.

## References

- [Repository contract/authorization](../../../AGENTS.md), [plan M5 runtime](../../IMPLEMENTATION_PLAN.md#runtimeenvironment-validation), and [unresolved allocation issues](../../IMPLEMENTATION_PLAN.md#unresolved-issues).
- Specification [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [loading](../../implementation-research/inference-and-capacity.md#text-only-loading-and-t4-behavior) and [rendering/termination/call independence](../../implementation-research/inference-and-capacity.md#rendering-termination-and-call-independence).

## Intended outcome

A CPU-reviewed direct inference backend and concrete allocation plan are ready for an authorized bounded T4 smoke test.

## Scope and boundaries

- Start with Qwen3.5-9B, maintained Transformers text-only loading and diagnostics for every language weight, including tied heads. Expected unused vision weights cannot excuse missing/newly initialized language weights.
- Configure NF4, double quantization and FP16 explicitly, preserving supported sensitive FP32 calculations. Batch one; one full replica/serial process per T4; no CPU offload, device splitting, conversion wrapper, alternative serving/quantization stack or custom kernel.
- Use enable_thinking=False, temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0 and no presence penalty. Freeze actual template/EOS/PAD behavior only after passing checks.
- Save exact requests, generated IDs and raw generated-suffix text without cleanup. Remove only verified terminal transport framing for parsing; unexpected/internal markers remain. No blanket special-token stripping, JSON repair, closing-brace stopping or constrained decoding.
- Provide fresh KV/recurrent state per call, process-owned device visibility before CUDA initialization, and saved per-call CPU/CUDA seed assignment. Instrument cache lifecycle and order/resume independence; do not promise seed-based exact regeneration.
- Prepare the existing runner's backend integration and concrete development manifest, including all planned validation calls within smoke/pilot limits.
- Record available/proposed device identities, durable storage/backup location, allocation start/stop and billing rules, development/setup/interruption budgets and safe termination allowance. Prepare the reviewable action/cost/configuration before seeking any compute authorization.

## Completion criteria

- CPU/static/mock tests cover exact decoding, terminal framing, full valid cap-ending JSON, overflow-before-generation and call identity/seed/state ownership.
- Host/package/model/tokenizer candidates and template inputs are identified, explicitly not yet a passing GPU lock.
- M1–M4 evidence is current for the chosen schema/template/size; changes reopen affected checks.
- A concrete <=24-call/0.5 aggregate GPU-hour smoke plan and the shared resource envelope are documented. This task performs no GPU allocation or inference.

## Validation and evidence

Use saved generated-token fixtures with internal special markers, invalid suffixes and exact cap endings; verify no normalization turns invalid output valid. Check backend-to-ledger fields and serial worker initialization with mocks. Review actual maintained loader/configuration sources and provider/storage facts; leave hardware-dependent claims for M5-T02.

### Preparation checkpoint

Started 7 October 2026 on clean `feat/m5-inference-preparation`.
Inspected the repository contract, this task, specification §§8–9, runtime
plan, technical synthesis/loading investigation and M4-T06/CPU-audit handoff.
`.venv/Scripts/python.exe -m unittest tests.test_schedules tests.test_schedule_manifests tests.test_peer_views -q`
passes 36 checks in 31.804 seconds on Windows, Python 3.11.9. Existing saved
schedules, identities, renderer, schemas and target/fallback sizes remain the
preparation authority. No frozen scientific configuration is changed.

The user selected a proposed Kaggle plan. No reservation, upload, weights,
inference, compute authorization or GPU lock is implied. Local model-stack
metadata identifies torch 2.11.0, Transformers 5.12.0, Accelerate 1.14.0,
bitsandbytes 0.49.2, tokenizers 0.22.2 and huggingface-hub 1.19.0; the repository
CPU virtual environment deliberately has no torch. Maintained source review
confirms native `AutoModelForCausalLM` text-config extraction, language-prefix
conversion, tied-weight initialization, supported FP32 recurrent paths and
per-call `DynamicCache`. Loading diagnostics and actual device/runtime behavior
remain smoke gates. At this checkpoint, backend, fixtures and allocation
evidence were in progress.

### Backend checkpoint

The direct adapter and ordinary ledger evidence are implemented. The focused
command `.venv/Scripts/python.exe -m unittest tests.test_inference_preparation tests.inference_checks -q`
passes 25 checks in 6.175 seconds: maintained loader settings, language/tied-head
diagnostics, no offload/splitting, exact suffix/terminal handling, valid cap-ending
JSON, pre-generation request/overflow rejection, finite-score failure, fresh
cache and CPU/CUDA seed assignment, failure cleanup, process ownership,
two serial worker visibility, load/attempt evidence and exact reopened/backup
reuse. A diagnosed nonfinite backend remains blocked with uncertain completion,
with no retry or fabricated raw reply. Optional inference packages are absent
from this CPU virtual environment; every generation is a labeled mock.

The broader deterministic command adds `tests.durable_checks`,
`tests.attempt_checks`, `tests.worker_checks`, `tests.accounting_checks` and
passes all 97 checks in 391.026 seconds at the earlier 20-check adapter checkpoint.
The final 25-check adapter run supersedes that adapter subset. Native 9B
metadata-only `tests.tokenizer_inference` passes four checks in 0.137 seconds,
covering all nine retained native suffix fixtures, actual template/request IDs,
fresh generation defaults and empty independent hybrid caches.
`tests.tokenizer_capacity` renews all eight checks and the unchanged complete
target/fallback bounds, 261,388/259,868 including output reserve.

The [candidate/allocation evidence](../../validation/m5-inference-preparation.md)
records the proposed host, source review, exact template/EOS/PAD candidates,
24-attempt smoke request matrix, unchanged pilot manifest, shared 8/2/2-hour
reserves, two-device allocation convention, 120-second shutdown allowance,
live/backup/off-host destinations and pending account/provider facts.
At this checkpoint, full current-source/core/installed regressions and final
consistency review remained required. No GPU or empirical gate is passed.

### Identity review checkpoint

Final review replaced Python numeric equality with the existing canonical JSON
representation for settings and token records. Changed booleans/integers/floats
cannot pass exact identity. A factory/worker device conflict is rejected before
creating a worker store or process, rejecting contradictory assignments.
All 27 focused checks at this checkpoint pass in
8.681 seconds. The noneditable installed package outside the checkout passes
those 27 plus all 14 worker checks (41 total) in 139.913 seconds under hash seed
37; all 28 installed module paths/bytes match the final source. The first
non-isolated build probe lacked `bdist_wheel`; ordinary isolated pip building
fixed it without modifying runtime dependencies or the project build contract.

Core validation passes 260 checks in 221.223 seconds (252 passed, eight expected
optional skips). Native tokenizer/config/cache/decoding checks pass four each
for 9B/4B in 0.180/0.205 seconds. Both immutable revisions were reverified through
the public Hub API; no weights were fetched. At this checkpoint, full CPU
regression and final artifact/status review were still running. Prior protected
artifacts and all scientific schemas/inputs/rendering/analysis remain unchanged.

### Exclusive device review

A CPU construction probe found that matching duplicate GPU assignments and an
omitted worker visibility with a device-selecting factory were still accepted.
The scheduler now requires explicit matching factory/worker visibility and
distinct assigned devices before creating stores or processes. The existing
regression covers conflicting, missing and duplicate assignments, with no
files created. Final focused validation passes all 27 checks in 7.768 seconds.
Actual physical UUID mapping remains host preflight work; no registry or GPU
query is added to CPU scheduling. Renewed noneditable installed validation
passes all 41 checks in 129.691 seconds under hash seed 37; all 28 installed
module paths/bytes match final source.

## Completion and handoff

M5-T01 is implemented and verified on CPU on 7 October 2026. The direct
text-only adapter, serial runner integration, raw decoding/ledger evidence and
concrete proposed Kaggle preparation are complete. [M5-T02](M5-T02-hardware-smoke-and-host-validation.md)
has its preparation dependency satisfied and remains blocked by execution
authorization and actual host/provider preflight. M5's operational gate is open.

Environment: Windows/CPU, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1, LangChain Core 1.6.6.
The separate native-metadata environment uses torch 2.11.0+cpu (CUDA build
`None`, CUDA unavailable), Transformers 5.12.0 and the candidate versions listed
in [allocation evidence](../../validation/m5-inference-preparation.md).
No pretrained model was constructed and no weights, GPU allocation/inference, pilot,
main execution, publication, paid compute or accepted freeze occurred.

| Named validation | Executed result |
|---|---|
| Complete `.venv/Scripts/python.exe -m recovery validate` | All 449 checks passed in 2,571.482 seconds, including original-worker report reproduction twice, all nine lifecycle cases and the 25-check adapter checkpoint. This run began before the final JSON/device identity review; the final additions and changed guards are independently covered below. Unchanged analysis/renderer/oracle/archive checks were not repeated after those narrowly scoped guards. |
| Final `.venv/Scripts/python.exe -m unittest tests.test_inference_preparation tests.inference_checks -q` | All 27 passed in 7.768 seconds. This includes regression fixtures that reject numerically equal but differently typed settings/IDs/masks and conflicting, missing or duplicate factory/worker device assignments before generation/store creation. |
| `.venv/Scripts/python.exe -S -m recovery validate --core-only` | 260 run in 221.223 seconds: 252 passed, eight expected optional archive/renderer skips. |
| Noneditable installed `tests.test_inference_preparation`, `tests.inference_checks`, `tests.worker_checks`, outside checkout, hash seed 37 | All 41 passed in 129.691 seconds after exclusive-device review. All 28 installed module paths/bytes match final source. Isolated pip build passed; CPU runtime dependencies were not changed. |
| `python -m tests.tokenizer_inference --tokenizer LOCAL_9B_METADATA` / `LOCAL_4B_METADATA` | Four each passed in 0.180 / 0.205 seconds. All nine saved native suffix cases, actual templates/IDs, unmodified generation defaults and independent empty hybrid caches agree. Metadata only, no inference. |
| `python -m tests.tokenizer_capacity --tokenizer LOCAL_9B_METADATA` | Eight passed in 1.694 seconds. Complete target/fallback upper bounds remain 261,388 / 259,868 with reserve under 262,144. |
| `pip check`, `compileall`, `git diff --check` | Passed; no broken CPU requirements. |
| Protected-file/data audit against `6fa32ac` | Specification, study configuration and all 26 prior data archives/fixtures unchanged; binary archives compared as bytes, text with Git line-ending normalization. Only the new suffix fixture and its index are added. |
| Final local-link/status/resource audit | All 354 local links/anchors in seven changed Markdown files pass. All 29 task files match the index: 21 done / eight blocked, M5 1/5. Matrix rows cover smoke slots 01–24 exactly; two-device time/stop bounds reconcile, and saved pilot totals remain 1,114 distinct / 1,178 logical with 80 prefix plus ten controls first. |

The final consistency audit passes for local links/anchors, task counts/statuses,
the unchanged scientific artifacts and the exact 24-slot smoke / 1,114-distinct
pilot envelope. The [preparation packet](../../validation/m5-inference-preparation.md)
records the initial 9B/target candidate, actual template input candidates,
process/attempt evidence fields, all planned instrumentation calls, two-device
clock, shared 8/2/2-hour reserves, safe shutdown, provider facts and storage paths.
Provider availability/quota/monetary terms, request materialization, durable
off-host export and confirmed release remain T02 preflight requirements.

Actual language weights, supported T4 runtime paths, finite model outputs,
headroom, timeout adequacy, cache/RNG order/resume behavior, accepted-host
persistence and capability are unverified. T03 still owns the first 90 slots,
T04 the complete pilot and measured timing, and T05 the accepted single lock,
whole-schedule forecast and freeze. Any candidate change repeats affected
checks; no configuration mixing or seed-based exact regeneration is promised.

### Actual Kaggle CPU preparation follow-up, 8–9 October

[Run 4](../../validation/m5-kaggle-full-preparation-run-4.md) verifies complete
canonical source, Linux cleanup and the 88-package candidate/project installation.
Its probe-output parsing failure remains retained. The [actual run-5 continuation](../../validation/m5-kaggle-full-preparation-run-5.md)
passes all 97 CPU checks with zero skips, all 28 installed module hashes, eight
clean command exits and independent off-host snapshot reopening, in 319.030 CPU
seconds without repeated installation. The CPU preparation contract now passes
on the real Linux/Python 3.13.15 candidate; no repeat CPU preflight is requested.
T01 remains done. Existing GPU authorization is recorded in T02, which remains
blocked by actual GPU/model requirements; no language weights or model
generations ran. Candidate/scientific settings and task counts are unchanged.

