# Evaluation, statistical validity, model fairness and compute

The central evaluation question is a policy effect on joint team success across
a declared population of worlds. It is not best-of-many capability, average
agent-call accuracy, or a universal ranking of model architectures.

## 1. Statistical findings that matter here

**S01 — Error bars for LLM evaluations.** Miller's
[paper](https://arxiv.org/html/2411.00640v1) separates between-question variation
from within-question sampling variation and derives paired comparisons and
evaluation-planning formulas. Repeats reduce one variance component; pairing
helps when outcomes covary. Lowering temperature changes the evaluated system,
not merely its measurement noise. Single-token probability shortcuts do not
transfer to multi-turn team trajectories.

**S02 — NIST evaluation models.** Keller et al.'s
[NIST AI 800-3](https://doi.org/10.6028/NIST.AI.800-3) distinguishes fixed-benchmark
accuracy from generalized accuracy, studies hierarchical estimates with 22
models on three benchmarks, and discusses GLMM assumptions and variance
components. Repeated attempts on one item form a cluster. More efficient model
estimation depends on assumptions; it does not create a representative item
population. With two fixed model systems and policy interactions, a simple
paired world analysis is easier to defend than an elaborate latent-capability
model.

**S03 — Power in NLP.** Card et al.'s
[EMNLP paper](https://aclanthology.org/2020.emnlp-main.745/) shows that power for
paired accuracy comparisons depends on disagreement as well as mean difference
and sample size. Underpowered studies can exaggerate reported gains. Its
GLUE-specific estimates are not transferable effect sizes. Use sensitivity
ranges and a scientifically meaningful target difference before main outcomes.

**S06 — Statistical precipice.** Agarwal et al.'s
[paper](https://arxiv.org/abs/2108.13264v4) illustrates misleading point estimates,
protocol changes and few-run uncertainty in deep RL. Its stratified resampling
conditions on benchmark tasks and resamples training runs. Our primary
population instead samples worlds. Importing that resampling scheme literally
would target the wrong uncertainty. IQM and normalized-score profiles solve
different problems from bounded binary team success.

## 2. Define the estimand before choosing repeats

Let `Y[m,w,p,e,r]` be joint exact success for fixed model system m, world w,
packet p, event e and continuation trial r. A complete team episode, including
its ordinary protocol failures, produces one binary endpoint. Its agent calls
are dependent parts of that endpoint.

For the preferred direct contrast, define:

`D[m,w,r] = Y[m,w,HS,revision,r] - Y[m,w,HSC,revision,r]`.

The primary target is `Delta[m] = E_world E_sampling D[m,w,r]`, with fixed,
declared weights over edit-type × owner × first-speaker strata. This generalizes
only to the specified generator, rendering, supplied-history construction,
protocol and configured model system. It does not cover arbitrary tasks,
histories, prompts or model families.

For the proposed primary allocation, use trial 0 on all worlds. Extra trials on
a predetermined panel describe repeatability separately. This avoids weighting
some worlds more because they received more attempts. A legitimate alternative
averages a fixed number of trials within every world; it estimates the same
population mean with different efficiency, not a stronger population by default.

Keep the revision-specific interaction and the model difference
`Delta[Qwen] - Delta[Granite]` as explicit secondary contrasts. A significant
effect in one model and a nonsignificant effect in the other is not evidence that
their effects differ. Likewise, a positive interaction alone need not imply a
positive direct recovery benefit.

## 3. More worlds versus more trials

For independent trials conditional on a world, a simplified decomposition is:

`Var(mean D) = [sigma_between^2 + sigma_within^2 / R] / N`.

Here the within-world quantity is the variance of the **paired policy
contrast**, including the covariance induced by the chosen sampling procedure.
It is not the variance of isolated agent replies. If total cost is proportional
to `N*R`, then increasing R at fixed cost increases the contribution from
between-world variation. Repeats become more attractive when acquiring each new
world has a substantial fixed model cost, the number of worlds is limited, or
repeatability itself is the target. Scalar controls and setup also have costs;
the equation is a planning simplification.

Scripted histories have no model-acquisition cost. Therefore two trials in
every controlled cell need a stronger justification than “repeated trials are
rigorous.” Natural prefixes are different: their acquisition cost can make
repeated continuations more efficient for a conditional question.

**Preferred compromise:** one primary trial on 192 independent worlds, plus two
extra trials on 24 predetermined balanced worlds. The panel has three trials
total per cell. Report outcome counts, discordance and variability; do not claim
three observations precisely identify each world's success probability or a
stable intraclass correlation. This is an allocation recommendation, not a
measured optimum. No simulation or new evaluation was run to obtain it.

## 4. Honest precision targets

For a single-trial paired binary contrast, let `q = P(D != 0)` and
`delta = E(D)`. Then `Var(D) = q - delta^2`. The following approximate half-widths
use `2.24*sqrt(q/N)` near zero effect for a 97.5% two-sided interval. They are
analytic sensitivities, not guaranteed bootstrap coverage or measured power.

| Independent worlds | q=.20 | q=.50 | q=.80 |
|---:|---:|---:|---:|
| 128 | 8.9 points | 14.0 points | 17.7 points |
| 192 | 7.2 points | 11.4 points | 14.5 points |

An approximate 80% detection reference is `3.08*SD(D)/sqrt(N)` with two
model-specific primary comparisons. At N=192 and q=.50 near zero effect this is
about 15.7 points. A 5-point effect with q=.30 would require roughly 1,132 worlds
under the corresponding normal approximation. A 10-point effect with q=.30
requires roughly 276. These are planning references, not exact McNemar power.

Consequently, neither 128 worlds with repeats nor 192 single-trial worlds
promises detection of small effects. At 192 worlds each edit stratum has only
96, so stratum effects are less precise. Small bridge/probe samples should
support descriptive transfer checks, not confident policy rankings.

Freeze a practical reporting reference, such as 10 percentage points, but do
not treat it as an automatically justified equivalence margin. An interval
crossing zero can mean the study is inconclusive. “No detected effect” must not
be rewritten as “memory does not matter.”

Before adoption, accept explicitly that this budget principally addresses large
effects and coarse bounds. If the thesis requires reliable detection of a
5-point difference, this candidate fails the precision gate and needs a larger
budget or a different primary question. A small pilot cannot certify that the
unknown disagreement rate will make a smaller sample sufficiently precise.

## 5. Analysis should preserve the existing strengths

Use 10,000 paired world-bootstrap resamples within the eight declared strata,
carrying all main cells and both model outcomes together. Keep the two
model-specific primary intervals at 97.5%, secondary intervals descriptive at
95%, and the existing conservative bounded-mean companion when empirical
variation degenerates. This follows the specification's reasoning while
requiring an explicit amendment of its population and estimands. Approximate
bootstrap intervals are not exact finite-sample guarantees.

Use the correct bounds in the conservative companion: a direct world difference
lies in [-1,1], while a revision-minus-no-change world interaction lies in [-2,2].
Changing the endpoint requires changing these bounds explicitly.

Report cell means, paired gain/loss counts and individual world contrasts. Do
not pool agents, calls, event cells, repeats or models as independent samples.
When averaging a repeated panel, first average within world. A fixed benchmark
repeatability interval and a population interval answer different questions;
label either one explicitly.

Keep observed invalid replies, timeouts and exhausted episodes as recorded
failures under the adopted endpoint. Keep genuinely unexecuted slots unknown.
Show coverage and completion bounds rather than dropping inconvenient pairs or
imputing their success. Do not rerun a model-level failure until it succeeds.
Resuming a committed call reuses its exact saved outcome; a fresh trial is a
different scheduled unit. Equal random seeds are neither replay nor proof of
equivalent randomness across tokenizers.

## 6. Development, prompt sensitivity and selection cost

**S04–S05 — Reporting versus estimating tuning returns.**
[Dodge et al.](https://aclanthology.org/D19-1224/) show that apparent model
preferences can change with tuning budget and advocate reporting the search.
[Tang et al.](https://aclanthology.org/2020.acl-main.246/) derive bias and poor
coverage for an expected-maximum estimator and demonstrate consequences on
classification examples. Their critique concerns maxima, not a proof that
ordinary bootstrap intervals for paired means always fail. Retain transparent
development budgets without adding best-of-budget curves to this thesis.

**S07 — Formatting sensitivity.** Sclar et al.'s
[v2](https://arxiv.org/html/2310.11324v2) varies semantically similar formats while
fixing few-shot content/order. Model rankings can reverse; instruction tuning
and scale do not remove the effect. The grammar and short-task selection bound
generalization, and many measurements use option probabilities. Our strict
action language makes direct transfer uncertain. This motivates one frozen,
audited common presentation, not an expensive formatting search.

Bound development to one declared candidate and, if necessary, one common
alternative. Give both models the same opportunities. Gate on legality,
full-information competence, sham usefulness and resource feasibility; do not
gate on a favorable policy difference. Small gates diagnose gross failure:
9/12 sham successes, for example, would not prove a 75% population success rate.
If either model fails, preserve the failure and seek a scientific redesign.

**S09 — Explanation faithfulness.** Turpin et al.'s
[v2](https://arxiv.org/html/2305.04388v2) changes biasing prompt features and
observes answer changes not acknowledged in explanations. Effects depend on
model and prompting; detecting an inconsistency does not prove every other
explanation faithful. Our messages are task actions, not privileged readouts of
internal reasoning. Use prose to document claims, and exact submission fields
to score commitments.

## 7. Cross-model fairness and hardware

The intended checkpoints are Qwen3.5-9B and Granite 4.2-8B. The
[pinned Qwen configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json)
has hybrid linear/full attention and a multimodal outer architecture. The
[pinned Granite configuration](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/config.json)
is a dense 40-layer GQA decoder. Granite's native configured limit is 131,072;
its advertised extension is not an accepted runtime setting. Qwen's text-only
loading path and attention treatment cannot simply be applied to Granite.

| Match across systems | Permit but disclose | Verify independently |
|---|---|---|
| Worlds, source facts, packets, action semantics, call horizon, endpoints, development opportunities | Native tokenizer, template/EOS handling and declared decoding | Literal historical rendering, termination, no hidden state crossing calls |
| Hardware class and resource accounting; ideally same declared NF4/FP16 regime | Different architectural memory/runtime costs | Actual weight inventory, finite outputs, placement and peak memory |
| Direct-answer mode if adopted | Native token counts and different realized output lengths | No unbudgeted thinking; common semantic information fits both limits |

The [Qwen card](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/README.md)
contains differing non-thinking reasoning presets in different sections. It
also discusses a presence penalty absent from the earlier proposal's simple
sampling tuple. The [Granite card](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/README.md)
recommends temperature 1.0/top-p .95 and offers thinking, direct and low-effort
modes. Freeze every actual generation setting and document deliberate deviations.
“Official defaults” is not a sufficient specification. Different native sampling
presets define two usable systems, not a controlled comparison of architecture
alone. A common-decoding sensitivity arm is optional future work, not necessary
for the first thesis.

**S08 — Quantization can change behavior.** Fu et al.'s
[EMNLP paper](https://aclanthology.org/2025.emnlp-main.1548/) evaluates GPTQ/AWQ and
2-bit variants on logical truthfulness and TruthfulQA. Effects depend on model,
task and quantizer; similar broad accuracy can conceal changed behavior.
It does not test NF4, these checkpoints, or distributed recovery. Qualify the
actual quantized systems and limit claims accordingly. A full-precision main
factorial would consume resources without isolating the present policy question.

At 8,192 input plus 512 generated tokens, Granite's FP16 KV tensors alone are
approximately `2*40*8*128*8704*2 = 1.328 GiB`. Qwen's eight full-attention layers
give about .266 GiB for that component, plus recurrent state and other memory.
These are tensor arithmetic, not runtime measurements. Weights, unquantized
embeddings/head, attention workspace, logits, allocator reserve and backend
implementation still matter. A 16 GB T4 is conditional on measured NF4/FP16
acceptance; a 24 GB GPU is a sensible fallback class, not a guarantee. Use actual
reported device capacity in admission calculations. A BF16
model-card example does not validate FP16 on T4.

## 8. Conservative resource planning

The [candidate schedule](prioritized-design-tests.md#5-complete-planning-arithmetic)
fits a provisional ceiling of 17,000 new physical attempts. A deliberately
conservative screening estimate is:

`aggregate GPU-hours = 24 + 1.25 * 17,000 * g / 3600`,

where g is allocated seconds per attempt, including assigned between-call
overhead, and 24 hours reserve non-call setup, reload, interruption and idle
allocation. This applies the margin to all planned attempts, including
development; it is not a throughput benchmark.

| Assumed g | Aggregate GPU-hours |
|---:|---:|
| 10 seconds | 83.0 |
| 15 seconds | 112.5 |
| 20 seconds | 142.1 |
| 25 seconds | 171.6 |
| 30 seconds | 201.1 |

The proposed 200-hour ceiling requires g below about 29.8 seconds; the existing
100-hour ceiling would require about 12.9 under this screening formula. Use
per-model/per-category measured forecasts before execution, rather than the
short Qwen course mean or a weights-only VRAM estimate. Parallel devices reduce
elapsed wall time, not summed allocated GPU-hours. Monetary costs require a
provider and current rate; no paid allocation is selected or authorized here.

Controlled histories support continuation-cost comparisons only. They have no
observed model cost of acquisition or maintenance. Charge natural prefixes to
the natural bridge and keep physical shared work distinct from the cost each
hypothetical deployed policy would incur. Include failed calls, loading and idle
allocation. A smaller, fully interpretable study is preferable to an incomplete
larger matrix.
