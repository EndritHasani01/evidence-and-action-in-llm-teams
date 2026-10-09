# ABS/IIS course study before the full thesis experiment

Prepared 9 October 2026. **Status: proposal for review; no scientific configuration, notebook, code, task status, or experiment result is changed by this document.** Repository inspected at `4eca60d`. The [project specification](../../PROJECT_SPECIFICATION.md) remains the sole scientific authority; the [implementation plan](../IMPLEMENTATION_PLAN.md) remains the engineering roadmap.

## Recommendation

**Yes: completing a smaller, auditable course study first is a good idea.** It gives ABS and IIS a functioning experimental system, actual results, and a defensible report while preserving a larger thesis study. The useful reduction is in sample size and computational regime, with the research questions and controls retained. A completed small study can be academically valuable even when the effects are negative, inconsistent, or inconclusive.

The recommended starting proposal is **Qwen3.5-4B, all five families, 20 main worlds, four peers, four prefix rounds, and four recovery rounds**, with smaller mathematical instances and proposed shorter reply/prose limits. Keep every existing mechanism, including the two primary comparisons, rather than building a different two-family demonstration. This needs **5,752 distinct main generations**, about **64.4% fewer** than the thesis target. An explicitly defined three-recovery-round alternative reduces that to **4,272**, about **73.6% fewer**, at the cost of additional implementation and interpretation changes.

Prefer the four-round version for the first course implementation. Most of the existing protocol, replay, diagnostics, and analysis retain their meaning, and it avoids changing many fixed-horizon assumptions merely to save another quarter of main calls. Choose the shorter alternative before main execution if measured runtime justifies that tradeoff. Neither version has been implemented or admitted to model execution.

“Good results” should mean a complete, reproducible dataset and an honest explanation of what happened. A smaller model or easier instances cannot guarantee that reset helps, that compact state wins, or that a statistically clear effect appears. Do not optimize the design for those outcomes.

## User goal and repository context

The latest preference is speed without a fixed deadline, retaining almost everything but using fewer worlds, a smaller model, and less computation. The archived [user context](../../research/02_agent_context/01_USER_CONTEXT_AND_PRIORITIES.md) already records the course-first, thesis-later intention. It is historical context, not permission to restore its old scientific design or compute assumptions. ABS/IIS rubrics, required report formats, and rules about using shared work for both courses remain unspecified.

The current specification has developed into a substantial thesis-scale study: five task families; multiple retention, delivery, and team-reset policies; historical receipts; prose timing; preservation controls; repeatability; exact evaluation; and resource accounting. Its complete target has 60 worlds and 16,152 distinct main generations; its fallback has 40 worlds and 11,504. A course variant requires an explicit scope decision because 20 worlds and direct selection of 4B are outside those current main-admission rules. See specification [§§2–7](../../PROJECT_SPECIFICATION.md#2-worlds-task-structure-and-events) and [§8](../../PROJECT_SPECIFICATION.md#8-inference-configuration-and-feasible-allocation).

Current local evidence validates CPU/scripted behavior and the offline attention integration. [Run 6](../validation/m5-t4-compatibility-run-6.md) validates a standalone T4 library diagnostic; the [attention/memory audit](../validation/m5-attention-memory.md) leaves complete-envelope model memory admission open. There are no accepted pretrained-model smoke, development-pilot, or main outcomes. Changing the course scope can reduce that feasibility problem; it does not turn these earlier checks into model evidence.

## Proposed course configuration

These values describe one proposed course regime, not edits to thesis defaults.

| Item | Current thesis design | Recommended course proposal |
|---|---|---|
| Language model | 9B first; 4B hardware/runtime fallback | Qwen3.5-4B directly, selected for course resources before treatment outcomes |
| Inference | Text-only NF4, double quantization, FP16 with necessary FP32 calculations | Same loading/computation approach; actual 4B/T4 path must pass |
| Main worlds | 60, or nested 40 | 20: four independently generated worlds per family |
| Families | Top-K, Prefix Sum, Difference Array, Sort, BFS | All five |
| Numeric instance size | Eight records per peer; permitted uniform fallback to six | Six records per peer, 24 total, declared from the start |
| BFS size | 12 nodes / 16 edges; permitted fallback to 8 / 12 | Eight nodes / twelve edges, including five edges beyond the tree |
| Peers | Four | Four |
| Prefix | Four synchronous rounds | Four synchronous rounds |
| Recovery | Four synchronous rounds | Four; optional three-round alternative described below |
| Generated reply cap | 384 tokens | Proposed 256 tokens, including candidate and all messaging JSON |
| Prose cap | 128 tokens summed across outgoing texts | Proposed 64 tokens summed across outgoing texts |
| Source forwarding | Up to three recipients and eight current references per recipient | Same; source delivery and prose remain separate |
| Decoding | Non-thinking; temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0, no presence penalty | Same |
| Context handling | Uniform 262,144 limit; complete permitted-view proof required | Retain native limit initially; renew a tighter course-envelope proof and memory argument; never silently truncate |
| Edited owners | Balanced in blocks of four within family | One complete block per family: each owner exactly once |
| Development | Five separate worlds, one per family | Five separate course-development worlds, one per family |
| Extra continuation replicate | Ten worlds: first two per family | Five worlds: first one per family, fixed before outcomes |
| Reporting | Full thesis-scale inference and release | Complete course dataset, exploratory interpretation, concise report and reproducible local artifacts |

Twenty worlds is a natural small choice **if retaining the existing within-family owner balance**: five families times four owners. Five or ten worlds can support a demonstration, but cannot keep that balance and provide very little within-family variation. Twenty is not a universal minimum for a valid experiment; it is the smallest complete owner-balanced version of this design.

Preserve the existing value ranges, ownership rules, edit eligibility, and exact answer contracts. Top-K still returns ten values. Prefix and Sort assign six coordinates per peer; Difference Array returns all 23 differences; BFS returns the complete eight-node dictionary. Do not make instances easier by selecting correct prefixes, favorable edits, or successful model outputs.

Use a new saved master seed whose existing seed streams are verified disjoint from course development and thesis inputs. Generate and save the actual worlds, edits, owner order, partitions, and continuation seeds before main inference. Keep course and thesis bundles separate, using the existing IDs and records within each bundle. Equal-looking world IDs across bundles are not interchangeable evidence or replay parents.

The smaller caps are provisional acceptance candidates. First verify that every output type, full-information control, and legal source-forwarding witness fits. Then check actual protocol validity and capability. If 256 is inadequate, revise the proposed cap before the main freeze and renew capacity, memory, timing, and settings evidence. Do not repair or regenerate individual cap-truncated replies. Do not shorten retained history retrospectively to force a fit.

## What stays in the study

| Mechanism or question | Course coverage | Scientific meaning retained |
|---|---|---|
| Main correction | Answer-changing revision on all 20 worlds | Recovery after one announced factual change |
| Sham control | B/C/K and both mixed masks on all 20 worlds | Separate correction-specific effects from generic cleanup |
| L/B/C/K/F | All five after revision | Local versus broadcast content delivery; full history versus evidence-only versus last candidate; acquired evidence versus fresh restart |
| Complementary team masks | P_G and P_H under revision and sham on all 20 worlds | Effect of teammates' reset on retained collaborators, with exact first-round sharing |
| Historical receipts | B_delta/C_delta/K_delta on all eight Prefix/Sort worlds, revision only | Actual retained representation crossed with genuine before-and-after information |
| Prose timing | Q_B/Q_C under both events on all eight Sort/BFS worlds | Early received prose with first-round source delivery held fixed |
| Answer-preserving edits | B/C/K on all eight Top-K/BFS worlds | Preservation and collateral changes when the target answer is unchanged |
| Full-information controls | Before and after main revision on every world | Single-call capability diagnostic; not a budget-matched team competitor |
| Repeatability | New continuation replicate of B/C/K/masks under both events on five fixed worlds | Conditional stability given the same prefix, not five extra independent worlds |
| Diagnostics and costs | All eligible executed course branches | Repair, old-value persistence, preservation, fragmentation, regression, evidence availability, communication, and physical/logical cost |

Keep the current restrictions on these crossings. Receipts do not gain sham or preserving arms; Q is not crossed with receipts or masks; extra repeats do not become receipt/Q repeatability evidence. This preserves breadth without adding experiments.

All siblings start from the same immutable realized prefix. B/C/K and masks keep their specified current-source relationship. K keeps the actual last prefix candidate, including wrong answers or an absence marker. Mixed and Q first rounds replay the exact persisted B/C outcomes, including invalid replies, after request/state/settings/seed equality checks. Stage their outgoing set and apply effects within their own branch. No hidden cache, recurrent state, oracle feedback, or repaired answer crosses calls.

## The optional shorter horizon

Four prefix rounds support the existing legal strategy: forward the own shard to a different peer in each of rounds one through three, then answer after the required information is available. Preserve that prefix rather than weakening prior collaboration to save a small number of calls.

**Three recovery rounds is the shortest alternative that keeps the existing Q release inside observation.** Q holds received round-one prose through round two and releases it before round three. A two-round study would never observe the released prose; it would study withholding within the horizon, changing the intended intervention. Three rounds preserve that release but observe only one response after it, rather than two.

If selected, declare a separate three-round course estimand: normalized exact-peer AUC averages 12 peer-round opportunities; final completion is at round three; collaborator effects average rounds two and three; stable completion means stable through round three. Prefix eligibility and K still use prefix round four. The direct receipt endpoint remains recovery round one and the immediate Q endpoint remains round two. State the shorter horizon in every comparison, cost denominator, figure, and claim. These are not the original four-round quantities with an unexecuted fourth round treated as failure or unknown.

## Exact call budget

These are **distinct scheduled generation slots**, not actual attempts, elapsed time, or counts of independent samples. They preserve required first-round replay and share each world's prefix once. For 20 course worlds the two-family scopes contain eight worlds each, preserving contains eight, and the extra replicate contains five.

| Main component | Thesis 60 / four recovery rounds | Thesis 40 / four recovery rounds | Course 20 / four recovery rounds | Course 20 / three recovery rounds |
|---|---:|---:|---:|---:|
| Shared prefixes | 960 | 640 | 320 | 320 |
| Revised L/B/C/K/F | 4,800 | 3,200 | 1,600 | 1,200 |
| Sham B/C/K | 2,880 | 1,920 | 960 | 720 |
| Complementary masks, both events | 2,880 | 1,920 | 960 | 640 |
| Full-information controls | 120 | 80 | 40 | 40 |
| Preserving B/C/K | 768 | 768 | 384 | 288 |
| Historical receipts | 1,152 | 768 | 384 | 288 |
| Q_B/Q_C, both events | 1,152 | 768 | 384 | 256 |
| Extra B/C/K/mask replicate, both events | 1,440 | 1,440 | 720 | 520 |
| **Distinct main generations** | **16,152** | **11,504** | **5,752** | **4,272** |
| **Logical scheduled call slots, including replay uses** | **17,656** | **12,560** | **6,280** | **4,800** |

For course recovery length `R`, let `d=4R` and `s=4(R-1)`. The main total is:

`16*20 + 5*d*20 + 3*d*20 + 4*s*20 + 2*20 + 3*d*8 + 3*d*8 + 4*s*8 + 5*(6*d + 4*s)`.

The 528 replay uses are `16*20 + 16*8 + 16*5`; add these to new generations for logical scheduled opportunities. A hypothetical deployed policy additionally pays its shared prefix and every logical continuation: 16 prefix calls plus 16 recovery calls, or 16 plus 12 in the shorter version. A replay does not make that deployed policy free.

| Development component | Four recovery rounds | Three recovery rounds |
|---|---:|---:|
| Five prefixes and ten full-information controls, run first | 90 | 90 |
| Revised L/B/C/K/F on five worlds | 400 | 300 |
| Sham B/C/K on five worlds | 240 | 180 |
| Masks on Prefix/BFS under both events | 96 | 64 |
| Receipts on Prefix/Sort | 96 | 72 |
| Q on Sort/BFS under both events | 96 | 64 |
| Preserving B/C/K on Top-K/BFS | 96 | 72 |
| **Complete development generations** | **1,114** | **842** |
| Separate smoke maximum | 24 | 24 |
| **Main + accepted development + smoke maximum** | **6,890** | **5,138** |

The corresponding thesis totals are 17,290 or 12,642. The default course plan halves main generations relative to the 40-world fallback, and reduces target main generations by 64.4%. Its unchanged full pilot means the total reduction versus the target is 60.2%; the shorter alternative reduces the total by 70.3%. Failed configurations, justified reruns, infrastructure retries, or interrupted generations add resource spending beyond these planned slots. Existing preparation spending is also separate from these new-generation counts.

## Runtime: faster, but still a real experiment

Model parameter count does not provide a measured speed ratio. Fewer worlds reduce repeated work; shorter output/prose limits can reduce generation and input cost; a smaller mathematical instance can reduce answer length. Keeping all mechanisms still requires thousands of calls. This is plausibly a substantial saving, not a promise of a short demonstration finishing in minutes.

The table uses the same hypothetical effective allocated seconds per new generation, `g`, for both course schedules. It excludes separately counted setup/release overhead. Real forecasting must use phase, condition, prompt length, device, and failure measurements, including assigned idle time.

| Assumed g | Default main GPU-hours | Shorter main GPU-hours | Default main + pilot + smoke GPU-hours | Shorter main + pilot + smoke GPU-hours |
|---|---:|---:|---:|---:|
| 5 seconds | 7.99 | 5.93 | 9.57 | 7.14 |
| 10 seconds | 15.98 | 11.87 | 19.14 | 14.27 |
| 20 seconds | 31.96 | 23.73 | 38.28 | 28.54 |

These are arithmetic sensitivities, not observed Qwen/T4 throughput. Two allocated GPUs running independent workers can shorten elapsed time; they do not halve aggregate GPU-hours. One active worker with the second GPU assigned but idle still spends that device's allocation. Four peers share a replica and have fresh state per call; two T4s are not a single larger memory pool.

For review, a **30 aggregate GPU-hour course ceiling** is a reasonable proposed decision limit, not known available quota or a newly authorized budget. Retaining the current conservative twelve-hour setup/development/interruption reserve and 25% main margin gives `12 + 1.25*main_calls*g/3600`: at `g=10`, default course cost is 31.97 hours and the shorter version is 26.83. Thus even the default small study might miss that ceiling. Any different reserve must be justified by actual preparation and development evidence, not hidden to make the forecast pass.

Choose a complete course configuration using CPU feasibility and measured costs before main outcomes, preferably before running its full pilot. If a later configuration change needs another pilot, budget both attempts. Reconcile prior shared preparation spending and unknown allocation intervals against the existing overall resource contract; another account does not erase previous scientific cost. Confirm actual provider session limits, remaining allocation, and durable export before execution. If no complete proposed version fits the accepted ceiling, stop and revise scope openly before main execution.

## Memory: why 4B and fewer worlds are insufficient alone

The official [Qwen3.5-4B model card](https://huggingface.co/Qwen/Qwen3.5-4B#model-overview) and [pinned configuration](https://huggingface.co/Qwen/Qwen3.5-4B/blob/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/config.json) describe a hybrid language model with eight full-attention layers, four KV heads, and head dimension 256. Use the already reviewed revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. The model supports a template switch to disable thinking; retain the study's existing sampling choices rather than importing unrelated benchmark settings. [Official non-thinking guidance](https://huggingface.co/Qwen/Qwen3.5-4B#instruct-or-non-thinking-mode).

The existing [offline audit](../validation/m5-attention-memory.md) shows that 9B and 4B have the same full-attention cache geometry: **32,768 FP16 KV bytes per resident token**, or **8 GiB at 262,144 tokens**. Smaller language weights help, but fewer worlds do not reduce any one call's maximum history. Mathematical size reduction alone also does not remove arbitrary permitted historical text.

The proposed 256/64 caps address that history envelope directly. As a conditional transfer of the [existing capacity proof](../implementation-research/m2-t06-capacity-proof.md), retain its 48-token own-reply expansion factor, 45-token prose factor, and conservative largest structural/wrapper allowance of 11,020:

| Conditional course envelope | Calculation including output reserve | Resident-token upper value | Full-attention FP16 KV alone |
|---|---|---:|---:|
| Four prefix + four recovery rounds | `7*256*48 + 21*64*45 + 11020 + 256` | 157,772 | 4.815 GiB |
| Four prefix + three recovery rounds | `6*256*48 + 18*64*45 + 11020 + 256` | 136,844 | 4.176 GiB |

These are checked arithmetic under stated assumptions, **not an executed course capacity proof or memory acceptance**. Verify those assumptions against the pinned 4B tokenizer, updated instructions/caps, all permitted history states, and actual renderer. The old structural allowance must still cover the course rendering. Neither value justifies an arbitrary 16K/32K/128K input cap; both exceed 128K. A small successful prompt or a padded long prompt cannot replace coverage of permitted views.

The smaller envelope is promising, but KV is only one term. Include language weights, NF4 metadata, recurrent state, activations, cache-growth copies, masks, CUDA workspace, allocator occupancy, and **at least 1.5 GiB free headroom**. Verify the selected efficient attention path on actual T4s, including the new layout if used. The current adapter's CPU acceptance is not CUDA or pretrained-model acceptance. Use maintained text-only loading, with no unexpected missing language weights, CPU offload, or cross-device splitting. Course acceptance would cover only its declared envelope; the original thesis R7 blocker remains a separate obligation.

## Strength and limits of the resulting evidence

Retain the two primary questions: correction-specific reset value and effects on retained collaborators. Preserve component contrasts, normalized exact-peer AUC, final joint completion, the two-family receipt/prose analyses, coordinate repair/preservation, repeatability, and cost accounting. For the default four-round proposal these endpoints keep their existing definitions; the three-round definitions require the explicit changes above.

The independent unit is still **one world with its one realized prefix**. There are 20 independent main clusters, four per family, and eight in each focal crossing. Thousands of peer-round replies are not thousands of independent experimental observations. Five continuation repeats assess conditional stability and do not increase the main sample size.

At equal world-contrast variance, reducing 60 worlds to 20 increases standard errors by approximately `sqrt(3)=1.73`. Using the specification's rough two-primary 80% power reference, `3.08*SD/sqrt(N)`, SD 0.35/0.60 gives about **0.241/0.413** at N=20, versus **0.139/0.239** at N=60. These are sensitivity calculations, not measured power; changing model, size, caps, or horizon can change variance. Small effects around 0.10 will often be hard to distinguish.

Use the existing paired within-family world bootstrap, primary/secondary interval conventions, bounded-mean companion when uncertainty degenerates, and raw world/family contrasts. Four worlds per family make intervals fragile; 10,000 resamples do not create new information or guarantee coverage. Avoid a catalogue of significance tests and claims of equivalence from a near-zero estimate. Present this as a small exploratory course study, with uncertainty and its fixed five-family scope explicit.

Include incorrect prefixes, silent peers, inactive prose-delay treatments, redundant receipts, wrong retained candidates, failures, and harmful policies. Recorded invalid/failed slots receive zero; unexecuted slots remain unknown and need coverage and missingness bounds. Do not switch models across conditions, grow the sample because an effect is weak, remove a failed family, or present selected successful cases as prevalence.

A defensible report can conclude that a method helped in this regime, harmed preservation, produced task-dependent tradeoffs, had little detectable effect, or encountered capability limits. It cannot establish a universal best recovery policy, robustness across models, psychological anchoring, or broader asynchronous/adversarial teamwork.

## Minimal implementation and execution plan after adoption

1. **Declare the course scope in the scientific authority.** Make a small, explicit authorized addition to the root specification describing the course regime and its claims. Preserve the full thesis contract. Record the engineering decision in the existing plan. This proposal alone adopts nothing, freezes nothing, and authorizes no main run.
2. **Add only the necessary configuration support.** Current population validation permits 60/40 worlds, and schedule/analysis/report code fixes several four-round and subset assumptions. Support the declared 20-world scope and five-repeat subset through the existing manifests and configuration; keep defaults intact. Wire the proposed caps consistently through rendering, validation, inference/settings, and capacity. If three recovery rounds are selected, update barriers, replay dependencies, completeness checks, AUC/final-round/trajectory definitions, and logical costs together. Reuse existing generators, solvers, IDs, SQLite/checkpoints, worker records, and exports. No new orchestration framework, provenance system, or parallel progress store is needed.
3. **Validate the affected course behavior on CPU.** Independently reconcile the schedule totals and owner/subset balance; check disjoint inputs; verify legal forwarding and answer attainability for every task under the new caps; renew native token bounds. Exercise isolation, exact mixed/Q replay including invalid parents, Q release, interruption/resume, and altered-setting rejection with focused scripted checks. Check diagnostics, clustering, final-round handling, unknown versus failed slots, and costs on synthetic course outcomes. Reuse unchanged passing checks; do not reinstall or rerun earlier preparation without a concrete need.
4. **Run a bounded 4B hardware smoke and capability-first pilot.** Prepare the concrete packet and CPU-downloadable assets first. Use at most 24 smoke calls and the applicable 0.5 aggregate-hour allowance, with prior allocation reconciled. Validate model loading, actual attention path, fresh call state, complete course-envelope memory/headroom, durable export, and provider release. Start development with the same 90 prefix/control opportunities. Retain the operational screens: at least 9/10 correct controls with at least one per family, three of five jointly correct final prefixes, and 14/20 correct final prefix candidates. These are screens, not treatment-effect estimates.
5. **Finish the complete course pilot, forecast, and freeze.** Run 1,114 development generations, or 842 for the shorter regime; require at least 98% protocol-valid distinct scheduled slots, inspect family/condition failures, and resolve protocol defects. Measure actual phase/condition costs and worst-envelope memory. Freeze model/environment/templates, size/caps/horizon, all course inputs/seeds/subsets, schedule, analysis/case rules, timeout, budget, and backup/release procedure before main outcomes. Passing admission is distinct from authorization for main execution.
6. **Execute, audit, and write the course report.** Run the complete frozen 20-world matrix in balanced blocks with durable resume and allocation accounting. Perform an independent completeness/replay/source audit, derive tables and figures offline, and reproduce them in a clean environment without GPU calls. Prepare a local report/artifact bundle; course submission and public publication remain distinct actions.

The original [M5 hardware gate](../todos/M5/M5-T02-hardware-smoke-and-host-validation.md), [allocation/freeze task](../todos/M5/M5-T05-allocation-admission-and-freeze.md), and [M6 report/release tasks](../todos/M6/M6-T03-results-and-claims-review.md) cannot be marked complete by replacing their 60/40-world obligations with course results. Record course-scoped acceptance explicitly. Reuse evidence that truly covers unchanged behavior, and keep outstanding thesis obligations visible. Avoid duplicating the entire task system; an explicit course checklist in the existing plan can identify applicable and remaining obligations.

## Report and thesis continuity

The course report can retain the specification's main narrative in a compact form: problem and prior work; task information and experimental instrument; capability/coverage; reset and compact-state effects; collaborators/receipts/prose; repair versus collateral damage; quality/cost/repeatability; limitations. Combine related comparisons in approximately seven or eight exhibits, with full per-world tables, traces, and environment details in supporting artifacts. Keep the existing fixed case-selection and boundary-policy rules rather than selecting attractive examples after results appear.

The same experiment can supply two course perspectives, subject to their actual rules: agent interaction, private observations, synchrony, and team effects for one; model integration, bounded inference, validation, evaluation, and intelligent-system reliability for the other. Do not invent expansions of ABS/IIS, mandatory course methods, or permission to submit identical reports. Use a shared evidence base with the required course-specific discussion once rubrics are available.

For the thesis, reuse the engineering improvements and lessons, then run the original admitted full design on separate inputs. Keep course main, course development, and thesis results distinct. Different models, instance sizes, caps, or horizons are different regimes; do not pool their worlds into one primary estimate. Describe any course-informed thesis changes and new hypotheses before the new thesis freeze. Course outcomes should not become hidden tuning data for later confirmatory claims.

## Research still needed and decision

Broad new literature research, another serving framework, a new GPU provider, and model training are not prerequisites for this proposal. The targeted remaining work is concrete: verify 4B capability with the actual strict JSON/channel budget, renew course capacity and complete-memory arguments, measure T4 runtime, check current provider/session/export constraints, and establish the applicable course requirements. These observations determine feasibility; public model benchmarks and past CPU checks do not answer them.

**Proceed with a course-first study, preserving all mechanisms and starting from the 20-world four-round proposal.** It is a sensible balance between finishing sooner, retaining thesis relevance, and avoiding extensive horizon refactoring. Keep the three-recovery-round option available as an explicitly validated resource tradeoff. If the priority later becomes only a very short demonstration, describe that as feasibility/case-study work rather than silently presenting it as this complete comparative study.

### Verification of this analysis

Documentation-only checks on 9 October: independently recalculated both original main schedules, both proposed course schedules, logical replay uses, development totals, runtime sensitivities, and conditional memory arithmetic using Python 3.11 standard-library code. Checked the new document's local references/anchors and preservation of existing scientific files and user edits before its documentation commit. Official 4B metadata and non-thinking guidance were consulted; model fit, speed, validity, and treatment effects remain unmeasured. No notebook execution, pretrained-model loading, GPU allocation, pilot, main experiment, or configuration freeze was performed for this analysis.
