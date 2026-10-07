# M5 inference candidates and allocation preparation

Prepared 7 October 2026 for [M5-T01](../todos/M5/M5-T01-inference-and-allocation-preparation.md).
Authority: [specification §§8–9](../../PROJECT_SPECIFICATION.md#8-inference-configuration-and-feasible-allocation).
This is CPU preparation evidence and the reviewable proposed action for
[M5-T02](../todos/M5/M5-T02-hardware-smoke-and-host-validation.md).
No GPU allocation, language weights, model inference, pilot, main execution,
provider upload, publication or accepted freeze occurred.

## Candidate and source review

| Component | Reviewed candidate / limit |
|---|---|
| Host | Proposed private Kaggle notebook with `GPU T4 x2`, Linux and Python 3.11; actual account availability, host version, driver and storage admission are pending. Run an importable Python module under a main guard so spawn does not depend on notebook-local functions. |
| Initial model/tokenizer | `Qwen/Qwen3.5-9B`, immutable revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. |
| Permitted hardware/runtime fallback | `Qwen/Qwen3.5-4B`, immutable revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`; repeat affected checks within the same shared development envelope. Prefer passing 9B/40 over switching solely for 60 worlds. |
| Model-stack candidates | torch 2.11.0, Transformers 5.12.0, Accelerate 1.14.0, bitsandbytes 0.49.2, tokenizers 0.22.2, huggingface-hub 1.19.0. These identify inspected local CPU packages. A compatible Linux CUDA build and the complete dependency/driver lock must pass on the actual host. |
| Existing CPU lock | Python 3.11.9, Pydantic 2.13.5, LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1, LangChain Core 1.6.6. Repeat WAL/FULL, replacement, process-crash, cross-worker and backup checks on the proposed host. |
| Loading | Native `AutoModelForCausalLM`, no remote code; explicit `device_map={"":0}` within one process-visible T4, ordinary `dtype=torch.float16`, NF4/double quantization with FP16 compute. No CPU/disk offload, splitting, model conversion, added kernel or alternate quantizer. |
| Maintained paths | `sdpa` attention with maintained PyTorch recurrent fallback where optional supported kernels are absent. Save the actual attention setting, recurrent fast-path availability, parameter dtype/device inventory and package versions in the process record. Preserve sensitive FP32 calculations. |
| Mathematical size | Existing uniform `target` (m=8 / BFS 12 nodes, 16 edges). The only permitted size fallback is the existing uniform `fallback` (m=6 / BFS 8 nodes, 12 edges); earlier affected gates must pass again. |
| Limits | 262,144 input-plus-output tokens, full 384-token output reserve, batch one, serial calls, initial 120-second attempt timeout and one-second terminate/kill graces. Timeout adequacy is unverified. |

The [maintained text class](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py)
constructs the language model, recognizes vision/MTP extras, maps tied output
weights and uses FP32 sensitive recurrent calculations. The
[AutoModel factory](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/models/auto/auto_factory.py)
extracts the text configuration, and the
[maintained conversion mapping](https://github.com/huggingface/transformers/blob/v5.12.0/src/transformers/conversion_mapping.py)
handles the checkpoint language prefix. The adapter requests loading diagnostics,
rejects missing/mismatched/error language entries, verifies the actual tied head
and every parameter/buffer placement/precision, and verifies that 4-bit NF4 was
actually selected. Expected vision/MTP extras do not excuse language failures.
The returned 5.12.0 loading-info sets are converted to JSON lists without changing
their contents. Loader exceptions remain blocked adapter defects with uncertainty,
never a new sample. Conversion failures and language initialization still require
review of the actual retained host loading log; CPU mocks cannot pass that gate.
The [official bitsandbytes interface](https://huggingface.co/docs/transformers/quantization/bitsandbytes)
describes the separate compute dtype and quantization choices.

## Exact template, decoding and call ownership

[inference.py](../../recovery/inference.py) supplies spawn-picklable model and
tokenizer factories for the existing `ProcessProvider`/`LocalScheduler`.
`candidate_settings` records the actual tokenizer template string, model/revision,
`enable_thinking=False`, caps, explicit precision and generation settings. This
includes temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0,
sampling with one beam and no presence penalty. A new `GenerationConfig` prevents
checkpoint defaults adding penalties, constraints, forced tokens or stop strings.
The process loading record includes its complete effective generation config.

Native template arguments are one user turn, `add_generation_prompt=True` and
`enable_thinking=False`. The generated prefix ends with the model's empty thinking
frame. The exact rendered text, native NFC token IDs and all-one mask remain
distinct saved request fields under M2/M3. No input truncation or archive cleanup
is introduced. The candidate EOS IDs are 248044 (`<|endoftext|>`) and 248046
(`<|im_end|>`), with PAD 248044. Only a single final verified `im_end` is removed
from parsing text; the full raw suffix and every generated ID are retained.
An internal/repeated marker, an unexpected suffix or generated `endoftext`
remains in parsing text. A complete valid JSON reply at the 384-token cap is
accepted; a cap stop alone does not assert truncation. M5-T02 must verify actual
model transport behavior before these candidates become accepted settings.

Each call rechecks permitted view/rendering/tokenization/settings equality before
generation, assigns its saved CPU and CUDA seed in one process, and supplies a
new empty `DynamicCache` for both KV and recurrent layers. A forward hook checks
cache ownership, and a logits processor rejects nonfinite model scores before
sampling filters. Hooks/cache/output references are discarded even on failure.
No cache or conversation handle is a backend field. This instrumented API behavior
is CPU/mock evidence; order/device changes may still produce different GPU tokens.
Scientific reuse always consumes the existing exact persisted parent reply.

The existing `provider_processes.backend_json` stores loading evidence once per
resident process. `attempts.backend_json` stores exact raw generated-suffix text,
the removed transport ID if any, actual seeds, PID, cache observations, finite-score
step count and memory readings. Existing call IDs, process/attempt keys, raw calls,
checkpoints and physical/policy accounting remain authoritative. There is no
second progress or delivery store. Old read-only artifacts need no migration;
exclusive new/reopened writers add nullable evidence fields only.

## Concrete development manifest and smoke requests

Use the unchanged saved [population](../../tests/fixtures/population_target.json)
and [schedules](../../tests/fixtures/schedules_target.json). Their five disjoint
development worlds, exact branch/call IDs, peer/phase seeds and replay parents
already define the full pilot: 1,114 distinct / 1,178 logical slots. The
`schedules.capability` selection contains exactly 80 prefix and ten before/after
full-information slots. Run those 90 first after smoke and inspect the specified
thresholds before authorizing recovery work. Do not execute main-world branches
or change this matrix for convenience.

The proposed smoke matrix below is separate from those pilot slots. Each row
names concrete development request origins and saved seed selection. Use
smoke-local call IDs `smoke/01` through `smoke/24`, keeping their origin IDs in the
ordinary request/settings records; do not write smoke output under a pilot call ID
or treat it as a capability observation. This is a request preparation matrix for
T02, not another population/schedule authority or an executed run manifest.
All counts are physical attempt ceilings: an infrastructure retry consumes another
smoke opportunity, and replaces a later planned probe. Failed configurations and
all instrumentation calls use the same shared envelope; there are no extra warmups.

| Smoke slots | Exact origin / CPU construction | Saved seed and purpose |
|---|---|---|
| 01–05 | First prefix request, peer zero, one each of Top-K, Prefix, Difference, Sort, BFS, in saved family order. | Each original `prefix_seed(1,0)`; five task output shapes and finite scores. |
| 06–07 | Before full-information controls for development Prefix and Sort. | Their saved before-control seeds; complete 32-coordinate output length/schema with empty sends. |
| 08 | After full-information control for development BFS. | Its saved after-control seed; complete node-key contract after the actual saved edit. |
| 09–13 | Round-four development prefix views, peer zero, from the existing CPU local-view attainability witness for each of the five families. | Each `prefix_seed(4,0)`; acquired sources and useful legal forwarding. Recorded model sends are validated literally, never fabricated. |
| 14–17 | Four first corrected-C continuation views for development Prefix, from that same drained CPU scripted prefix and saved revision. | `continuation_seed(0,1,peer)`; all four updated/reset sibling starts. Synthetic prefix construction is explicitly separate from natural pilot capability. |
| 18–19 | B recovery-round-four maximal retained view and Q_B maximal released-prose view for development Prefix/Sort, using the existing native capacity construction and real renderer. | Their `continuation_seed(0,4,0)` values; admitted worst-context envelope, finite output, peak memory and >=1.5 GiB headroom. Do not shorten histories to fit T4. |
| 20–23 | A, intervening B, A, then A after a confirmed process restart. A is slot 02's Prefix request/seed; B is slot 05's BFS request/seed. Prior slots also supply normal versus reversed family order. | Identical saved A request/settings/seed with fresh caches; log all outputs and stochastic differences, do not demand seed-based exact regeneration. Restart loading counts in setup and total allocation. |
| 24 | Slot 01's Top-K request/seed with the existing test-controlled process hang/deadline interruption, while retaining the actual host process/device identity. | Exercise durable timeout-before-termination and confirmed exit. A test-injected hang is labeled infrastructure validation, not an observed model latency or capability failure. |

Before reservation, T02 must materialize and review all 24 exact rendered/tokenized
requests, seeds and intended infrastructure probes from these named inputs using
the existing runner/ledger. CPU fixtures validate special markers, suffixes and
exact cap endings without spending additional model calls. They do not pretend
that every corresponding malformed string will be sampled in the smoke test.
Remaining probes are unexecuted/unknown if time, retries or a failing gate prevent
them. A retry is never used for invalid JSON, wrong candidates or a completed
timeout. A load, isolation or headroom failure stops admission and preserves evidence.

## Allocation, storage and proposed action

The user selected a proposed Kaggle plan. The
[Kaggle CLI documentation](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md)
identifies `NvidiaTeslaT4` as a two-T4 option and distinguishes save-only from
executing uploads. The
[NVIDIA Kaggle guidance](https://docs.nvidia.com/datascience/deployment/latest/platforms/kaggle/)
notes that starting a GPU session consumes quota and instructs stopping it after
work. Neither source proves this account's availability, remaining quota,
session durability, release latency or monetary terms. Those facts are pending
and must be recorded before an authorized reservation. No fixed weekly quota,
price, GPU UUID or passing storage service is assumed.

| Resource or convention | Concrete proposal / required observation |
|---|---|
| Devices | Capture both actual T4 UUIDs, indices, driver, CUDA, memory and package/host facts with `nvidia-smi` and package inspection. Smoke initially loads one replica on physical index 0. The other allocated T4 still counts while idle. A later device-rotation probe must replace an existing row within 24, not add calls. |
| Physical allocation | Start the allocation clock at session/device assignment, before loading; stop only at confirmed provider release. Record both allocated device intervals, including idle GPU 1. If start time is unavailable, use the earlier session-start bound and disclose uncertainty. Model process exit is not provider release. |
| Smoke ceiling | At most 24 physical attempts and 1,800 aggregate allocated GPU-seconds, whichever comes first, including allocated loading/idle/restart overhead. Two allocated devices give at most 900 wall seconds from assignment. Use the earlier provider/session ceiling if lower. |
| Safe stop | Reserve 120 wall seconds (240 aggregate GPU-seconds with two allocated devices) for backups and provider shutdown; stop admission earlier still when the existing attempt/retry/terminate bound will not fit. Initial attempts allow 120 seconds plus two one-second termination graces. A whole four-peer round can require eight bounded attempts (976 seconds), so the short smoke must admit calls individually, not blindly admit a full retry-bounded round. |
| Shared development/setup | Development inference <=8 aggregate GPU-hours across all configurations, attempts, instrumentation and justified reruns; loading/setup <=2; interruptions/reruns <=2. Distinct categories partition allocation, not additional charges for the same time. Smoke is nested in these limits. The initial total ceiling is 100 aggregate GPU-hours. |
| Main forecast | Future T05 uses the entire 12-hour reserve plus 25% margin on measured main allocation, slower-device/condition/prompt times and allocated idle overhead. Existing exact totals remain 16,152/17,656 for 60 worlds and 11,504/12,560 for 40. Two devices cannot halve aggregate hours. No timing forecast is available now. |
| Live storage | Proposed `/kaggle/working/recovery-m5/<configuration-run>/worker-0.sqlite` and `worker-1.sqlite` on the host's local writable filesystem, with WAL/FULL and the existing exclusive owner locks. `/kaggle/input` is only for immutable inputs. Do not rely on remote-mounted SQLite behavior. |
| Backups | Use the existing SQLite backup API after committed smoke probes/rounds, to exclusive paths beneath `/kaggle/working/recovery-m5/<configuration-run>/backups/`. Reopen/verify each backup. Preserve raw workers, load logs, requests, outputs, allocation records and interrupted/superseded attempts. |
| Durable destination | Proposed retained private notebook version output plus an independently downloaded copy under `C:\Users\EndritHasani\Downloads\recovery_blueprint\recovery_blueprint\artifacts\m5-development\<configuration-run>`. Record the actual private version/path and verify the off-host copies reopen before declaring them durable. Save-only notebook source is not a backup of live worker files. Availability, free space and export/recovery behavior are not verified. |
| Provider billing/quota | Record account-visible rate/quota unit, whether two idle allocated GPUs consume one session unit or two device units, setup/idle charging, billing increment and stop acknowledgement separately. The proposed scope uses existing no-charge account entitlement if available; no subscription or paid capacity is approved. Monetary cost is pending actual account terms. Research allocation always charges both devices regardless of billing. |

The reviewable next action is a **private Kaggle T4-x2 development smoke**, initially
Qwen3.5-9B/target with the candidate settings above, <=24 physical attempts and
<=0.5 aggregate allocated GPU-hour, writing only a new development artifact
directory and its verified backups. It neither admits recovery pilot spending
nor main execution. Device/storage/account facts, the concrete release mechanism
and request materialization remain preflight work in T02. Its authorization must
cover the actual scope/cost and any provider upload; no compute permission is
requested or inferred by completion of T01.

## Validation and remaining gates

Executed checks and final environment/counts are recorded in the
[task completion evidence](../todos/M5/M5-T01-inference-and-allocation-preparation.md#completion-and-handoff).
The [M1–M4 CPU audit](m4-cpu-gate.md) remains current: schema, renderer, populations,
sizes, caps, seeds, exact replay and analysis rules were not changed. Native
capacity is renewed for the candidate template. The retained
[suffix fixtures](../../tests/fixtures/inference_suffixes.json) are explicitly
CPU-constructed native token sequences, not sampled model outputs.

M5-T02 still owns actual language-weight loading, supported runtime behavior,
finite model output, GPU cache/RNG isolation, accepted-host persistence, complete
worst-context headroom and adequate timeout evidence. T03 owns the first 90
capability slots; T04 the remaining pilot/protocol rate and phase timings; T05
the measured complete-schedule resource gate and immutable accepted bundle.
Any changed model/template/lock/backend/timeout reopens affected checks. No
hardware, capability, throughput, accepted freeze or recovery effect is claimed.
