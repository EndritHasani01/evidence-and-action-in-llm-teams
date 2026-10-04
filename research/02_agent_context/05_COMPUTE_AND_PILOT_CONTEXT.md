# Compute and pilot context

## Confirmed budget, inherited configuration

The user confirmed two T4s and 30 GPU-hours. Plan conservatively in aggregate device-hours: two active GPUs for one wall-clock hour consume two aggregate GPU-hours. Actual platform quota deduction remains an account/environment fact to verify; do not equate a notebook session hour with the budget unit without evidence.

Each T4 has its own 16 GB memory. Do not treat the pair as one shared 32 GB device. **The user prefers Qwen3.5, superseding the original Qwen3-4B primary-model selection.** Earlier project context selected 9B; use **Qwen/Qwen3.5-9B with 4-bit quantization as the preferred pilot candidate**, with **Qwen/Qwen3.5-4B as the lower-memory fallback**. This is a candidate selection, not a demonstrated “most compatible” configuration.

By approximate parameter arithmetic, 9B weights at 16 bits require about 18 GB before caches, activations, vision components and runtime overhead. A full 16-bit 9B replica therefore does not fit one 16 GB T4. Four-bit weight storage has a theoretical lower bound around 4.5 GB, but actual memory is higher because of quantization metadata, unquantized modules and runtime state. Evaluate one quantized replica per card only after a compatible backend passes the actual text-only workload. The 4B fallback has a smaller weight footprint; FP16 feasibility also needs a memory test.

The official cards [T13] identify the model sizes and hybrid architecture. Generic backend support for T4 does not prove that Qwen3.5's specific kernels, quantization path and dtype work on T4. Do not inherit Qwen3 settings blindly or assume BF16/FP8 acceleration. Bound context length to the experiment, explicitly configure and validate non-thinking mode if retaining the fixed-call protocol, and pin compatible releases/model revisions.

The original Qwen2.5-7B secondary model is historical, not automatically retained. Reassess any secondary-model arm after selecting the primary. Record tokenizer/chat template, license, dtype, quantization and serving versions. **The old 29.121-hour forecast does not establish Qwen3.5 feasibility and must be recomputed from its pilot measurements.**

## Inherited accounting

| Item | Blueprint plan | Status |
|---|---:|---|
| Main Matrix A | 6,400 calls | Planned |
| Matrix A budget | 29.121 aggregate GPU-hours | Unmeasured forecast, including pilot/setup reserve |
| Half-speed sensitivity | 54.242 aggregate GPU-hours | Shows fragility to throughput assumptions |
| Matrix B | 6,080 calls, second model omitted | Still needs measured admission |
| Initial pilot | 152 calls | Not run |
| Expanded pilot | 476 primary calls, up to 16 secondary probes | Reuses identical initial requests; not an additional independent 476 calls |
| Pilot cap | 2 aggregate GPU-hours | Stop before spending beyond the allowance |

Consult the parent `10_experiments_and_compute.md`, `12_pilot_and_decision_gates.md`, `budget_forecast.json`, and `reference/budget.py` for the authoritative arithmetic and admission rules. Do not transcribe these numbers into a new estimator without checking consistency.

## Serving comparison without consuming the study

Use the initial local/single probes for serving smoke tests. If comparing backends, choose a small matched subset that includes actual prompt lengths and output shapes. Charge every extra probe, failed call, warm-up, and retry to the budget. Do not run the entire pilot twice by default. Select one backend, then collect full pilot evidence under it.

Measure wall time, per-device active/reserved time as relevant to the quota, prompt/output token distributions, peak memory, parsing/truncation failures, initialization, checkpoint overhead, and parallel scheduling efficiency. Report forecasts with sensitivity or uncertainty, not a single optimistic tokens-per-second number.

Freeze model, backend, quantization, schema enforcement, prompt templates, seeds, and policy call allowances across confirmatory comparisons. A changed backend or prompt after seeing results creates a new design version and requires appropriate reruns.

## Admission and stopping

CPU semantic validation comes first. The expanded pilot's capability thresholds, memory limit, and power/precision gates remain explicit provisional design requirements, not established facts about model capability. If the budget fails, consider Matrix B only if it still answers the question. Do not selectively delete difficult worlds or diagnostic arms after observing favorable effects.

No GPU availability, quota balance, measured throughput, CUDA compatibility, or model efficacy was established by this companion. A final hardware lock and empirical cost admission are required before main data collection.
