# Exact experiment matrix, inference, and compute

The machine-readable authority is [configs/experiment.json](configs/experiment.json). `python -m reference.budget` verifies the arithmetic. All numbers below are planned. No T4 throughput was measured while preparing this blueprint.

## Matrix A: full target

| Block | Base worlds × variants | New prefix? | Policies / calls per world variant | Calls |
|---|---:|---|---|---:|
| Primary | 64 × 4| yes| 3 prefix +1 extraction +3 × 3 recovery for N/R/E| 3,328|
| Scope/state diagnostics | 16 × 4| reuse primary| O/OC/ON/OR, 3 calls each| 768|
| Restart | 16 × 4| reuse parent; fresh corrected run| F, 3 calls| 192|
| Extra inference | 16 × 4| reuse primary| 1 reviewer +3 N-style recovery| 256|
| Full-information single | 16 × 4| none| 1 fresh call| 64|
| No-event | 8 × 4| reuse primary| N/E, 3 calls each| 192|
| Second stochastic seed | 16 × 4| yes| 3 prefix +1 extraction +R/E × 3| 640|
| CapEx transfer | 16 × 4| yes| 3 prefix +1 extraction +R/E × 3| 640|
| Second model | 8 × 4| yes| 3 prefix +1 extraction +R/E × 3| 320|
| **Total** ||||**6,400**|

This contains 416 realized prefixes, 416 extraction calls, 64 reviewer calls, and 1,600 scored continuations/diagnostic decisions. Main primary evidence has 64 independent base worlds, not 256 independent worlds or 768 independent policy observations. Each of the two primary task families contributes 32 base worlds. Diagnostic 16 contains 8 from each family; noevent8 and model8 contain 4 each. Select subsets by a seeded hash ranking within family, before inference. Additional seeds/models do not increase the count of independently generated base worlds.

No cross-product of every baseline, model, temperature and task is intended. Primary N/R/E runs get one stochastic seed across 64 base worlds. A second seed is an explicitly limited robustness check. Second model uses the same 8 selected base worlds with new model-generated prefixes; it is a same-family diagnostic, not a cross-family generality claim.

## Model and serving choice

Primary: [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B), **FP16**, one complete replica per T4. The official model has 4B parameters and supports an explicit non-thinking template switch. Force `enable_thinking=False`. Agent/reviewer sampling: temperature 0.7, top_p = 0.8, top_k = 20; these agree with its non-thinking guidance. Extractor: greedy (`do_sample=False`), no free-form reasoning output. Cap agents/single at 256 generated tokens; extractor/reviewer at 512. These are short structured tasks, not evaluations of unrestricted reasoning ability.

Second checkpoint: [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct), NF4 with FP16 compute and double quantization; the same structured task contract, agent decoding values and caps. Quantization changes together with model size, so this is an external-validity check, not an isolated model-size causal experiment. [Transformers' bitsandbytes documentation](https://huggingface.co/docs/transformers/quantization/bitsandbytes) lists NF4 support on Pascal or newer NVIDIA hardware.

Each [T4](https://www.nvidia.com/en-us/data-center/tesla-t4/) has 16 GB; two cards do not form a 32 GB shared-memory device. Do not use tensor parallelism. Use two independent worker processes, each restricted to one CUDA device and one serial generation request. Start with batch size 1. Do not assume FlashAttention2 or BF16 support on T4. Use PyTorch SDPA with a tested supported fallback, and record the chosen kernel path. FP16 primary weights require roughly 8 GB before runtime/KV overhead; fit is plausible, not a substitute for a memory pilot.

Use Transformers rather than making the study depend on a particular vLLM GPU-generation support matrix. A faster backend may be selected only during the pilot, followed by revalidation and a pinned environment before confirmatory inference. Do not switch backends only for a difficult arm.

## Technologies

Python 3.11; Pydantic v2 for strict contracts and JSON Schema; PyTorch and Hugging Face Transformers for inference; Accelerate for model loading; bitsandbytes for the 7B diagnostic; NumPy/SciPy/statsmodels for analysis; pandas/PyArrow for Parquet; matplotlib for exportable figures. Python standard-library JSON, hashlib, sqlite3, pathlib and unittest suffice for the reference core and deterministic persistence. Use pytest/Hypothesis in the full runtime implementation for property/state-machine testing if available.

Use an offline local SQLite/JSONL experiment registry, not an externally hosted tracking dependency. A convenience MLflow or Trackio UI may be added later, but canonical results must reconstruct without it. No vector database, graph database, Redis, Kubernetes, LangGraph, or paid API is required for this bounded experiment.

Resolve dependencies once on the actual Kaggle environment, freeze exact versions/hashes, and save `pip freeze`, CUDA/driver information, package lock, model revision and tokenizer revision. The bootstrap constraints are `transformers>=4.51,<5`, `torch>=2.6,<3`, `pydantic>=2,<3`, `accelerate>=1,<2`, with compatible bitsandbytes selected by the smoke test. These are compatibility ranges, **not a tested installation lock**. A lock generated and validated on the hardware is a required pilot artifact. No runtime `latest` downloads after preregistration.

## Budget derivation

Conservative interpretation: 30 **aggregate GPU-hours**, i.e. approximately 15 wall-clock hours if both GPUs remain allocated throughout. Do not assume Kaggle's quota is counted per session rather than per device. If the account's actual rule differs, record it; the thesis does not rely on extra budget.

There are 5,920 short calls and 480 long calls. Planning means:

| Call class | Mean input | Mean generated | Hard generated cap |
|---|---:|---:|---:|
| Agent / single | 1,100| 180| 256|
| Extractor / reviewer | 2,200| 300| 512|

Therefore the planned total is 7,568,000 input tokens and 1,209,600 generated tokens. Context cap is 4,096 including generation allowance. The budget does not price a 256-token cap as though every call generated only 50 tokens; measured output means must replace these assumptions.

For block i, estimate

\[
H_i=\frac{I_i/p_i+O_i/d_i}{3600},\qquad
H_{total}=1.12\sum_i H_i+4.
\]

Planning speeds are 400 input tokens/s and 20 generated tokens/s **per T4** for the 4B worker; 300 and 15 respectively for the quantized 7B worker. The 12% allowance covers processing/serialization overhead; 4 aggregate hours cover a maximum 2-hour GPU pilot and 2 hours for initialization, retries, interruption and reserve. These speeds are illustrative, not benchmark measurements.

Matrix A costs **29.12 aggregate GPU-hours** under those assumptions. At half those speeds it costs **54.24 hours** and is infeasible. Running both GPUs halves elapsed time but does not halve aggregate GPU-hours. Summing input and output service time is a planning approximation; admission uses measured end-to-end call latency and GPU allocation time.

## Admission, Matrix B, and stop rules

Before any confirmatory data, sample all call shapes on hardware and bootstrap the projected total from measured phase-specific latencies/token counts. Matrix A is admitted only if the one-sided 95% forecast bound plus spent pilot time and remaining reserve is ≤ 30 aggregate hours, memory peak ≤ 14.5 GB per card, and capability gates pass.

If only the second-model block makes A exceed budget, choose **Matrix B: identical design with the 320-call second-model row removed, total 6,080 calls**. This is the only predeclared compute fallback. Preserve all primary worlds and diagnostic mechanisms. Freeze the A/B choice before confirmation; do not drop a block because its results are unfavorable.

If B also fails the admission bound, the present full study is not feasible under the stated quota. Optimize serving or simplify prompt serialization during the development phase, then rerun the pilot. If still infeasible, revise the research question and preregister a new design; do not quietly reduce the sample until a large claim rests on a handful of runs.

If the 4B checkpoint fails capability, a 7B-only design is a new compute plan, not a free substitution. Price it and rerun admission. A software task that fits VRAM but cannot deliver the experiment matrix does not pass feasibility.

## Execution order and accounting

1. CPU generation, oracle verification, schema tests and manifest creation before GPU allocation.
2. GPU pilot; freeze model/backend/prompts and choose Matrix A or B.
3. Execute primary blocks, alternating task families and randomizing within-block policy order. Reserve all three branches before starting a world variant.
4. Execute the registered diagnostics on their predetermined prefixes; do not select failures only.
5. Execute no-event, second-seed and transfer blocks. Run the 7B diagnostic last if Matrix A was admitted and its reserved allocation remains available.
6. Stop inference; complete analysis on CPU. Recheck source novelty before thesis submission.

Physical compute is charged once for shared prefixes/estimates. For deployment-cost comparisons, charge each policy its own hypothetical prefix cost; charge E its extraction stage and B its reviewer stage. Report both marginal recovery and end-to-end cost. The primary comparison is equal recovery opportunity, not a claim of equal total inference cost.
