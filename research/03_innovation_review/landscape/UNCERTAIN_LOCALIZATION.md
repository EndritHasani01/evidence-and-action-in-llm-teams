# Uncertainty-aware rollback is also prior art

Inspected 2026-09-30, [Conformal Agent Error Attribution, arXiv 2605.06788v1](https://arxiv.org/html/2605.06788v1), 2026-05-07; full §3 and §§4–6, including rollback experiment.

Conformal algorithms predict contiguous intervals containing a labeled decisive error, then restart a multi-agent trace before the interval while supplying failed-trace information. Coverage requires calibration/test exchangeability. The study uses Who&When and injected math failures; rollback comparisons use 100 MACNET trajectories per GSM8K variant and a tuned scorer. Reported success differences are small and within one standard deviation; coverage control is the clearer result. The formulation assumes one decisive error and does not identify arbitrary missing semantic dependencies. A proposed confidence-controlled rollback region is therefore occupied. Adapting coverage to sets of affected artifacts might be worthwhile, but would require independent labels, enough calibration data, and a credible deployment distribution—hard under 30 GPU-hours and tens of worlds.

Project interpretation: reserve risk calibration as an extension. Do not burden the first mechanism with a conformal guarantee whose assumptions the benchmark cannot support. Report actual unsafe reuse and unnecessary recomputation directly.
