# Validation strategy

This is a proposed evidence plan, not an executed experiment. The CPU repository audit and logical counterexamples are the only experiments completed in this research phase.

## Primary research question

After an announced authoritative change, does explicitly reopening completion obligations improve recovery of newly necessary work, while preserving useful prior work, compared with a fresh planner and ordinary dependency-aware recovery?

The primary causal comparison is **enforced reopening versus an otherwise identical generic reconsideration planner**. Comparisons with source-only reset estimate a broader recovery-package effect and are secondary.

The claim is about recovery behavior under a defined interface. It is not that negative dependencies are newly discovered or that a receipt proves open-world completeness.

## Stage 1: establish semantics on CPU

Implement the smallest lifecycle with a deterministic mock agent. Test current-version closure, omitted scope, inserted members, delayed completion, consecutive revisions, branch isolation and source-table replacement. Construct fixtures in which:

- all retained positive facts are correct, but an old stopping decision prevents an optimal answer;
- a historically affected artifact remains currently valid;
- a feasibility witness passes although optimality fails;
- no useful state can be saved and complete recomputation should win.

The first three have executed illustrations in `evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md`. They establish logical distinctions, not LLM effectiveness. A deterministic reference solver measures task difficulty and the overhead floor. If it is the best production solution for the small domain, say so; the LLM task remains an experimental probe.

## Stage 2: bounded development pilot

Begin with a small private-catalog/query adapter and six staged live development worlds, with additional CPU fixtures as needed. First check whether the model can solve the old and revised tasks from complete information. Then obtain naturally produced collaborative prefixes and check whether omitted-work failures arise without editing model outputs. Centralized capability is necessary but does not establish that four peers can recover in four rounds; the distributed pilot must pass separately.

Start with generic reconsideration, source-only reset and broad reopening. Add the control-aware provenance reference before interpreting superiority. Do not build scope extraction until broad reopening presents a meaningful accuracy/cost tradeoff. Inspect prompt and tool traces for leaked gold labels and scripted “right” queries. Tune the protocol only on development seeds.

A staged envelope is three worlds with prefix plus three policies (192 calls), followed only if promising operationally by three worlds with prefix plus five policies (288), and 12 before/after capability calls: 492 calls, plus at most 24 smoke calls. Stop at the three-hour development cap even if the schedule is incomplete. Twelve full five-policy pilot worlds would already require 1,152 calls before diagnostics and are not budgeted. Pilot admission must depend on capability, schema reliability, useful natural state and cost, not require a favorable measured treatment sign.

The hardware gate remains independent: Qwen3.5-9B quantized is the inherited preferred candidate, 4B the fallback. No compatibility or throughput is established here. Retain the existing 30 aggregate allocated GPU-hour ceiling and measured forecast discipline; do not assume current software versions make T4 execution feasible.

## Workloads

Use three primary structural families, selected before main execution for their relation to search closure:

| Family | Retraction-style revision | Opportunity-style revision | What must be measured |
|---|---|---|---|
| Distributed maximum/selection | Prior incumbent worsens or becomes ineligible | A previously excluded candidate becomes eligible or improves | Did the team inspect the newly relevant candidate/region? |
| Distributed top-K | Old member falls below cutoff | Eligibility expands, K changes, or a previously omitted region gains a qualifying member | Does preserved ranking work coexist with renewed coverage? |
| Graph search | Remove a necessary edge | Add an improving edge/path while old paths remain feasible | Does a feasible old route incorrectly suppress search for a better one? |

Eligibility constraints and query-mediated acquisition are explicit extensions of SILO semantics. Original maximum/top-K/BFS definitions and stored examples remain regression references. Do not call modified results native SILO scores. Prefix sums, differences and sort remain cheap generator/evaluator regression cases; they need not consume the main inference budget merely to retain six-family coverage.

For the main finite adapters, providers expose raw records or results of agent-selected queries plus domain/query revision receipts. A receipt may establish that a query ran; it does not choose the correct query or reveal the optimum. The hidden evaluator can enumerate the world. Recovery policies cannot see the gold answer, output footprint, relevant hidden option or synthetic semantic dependency graph.

Add a small **non-SILO finite catalog/configuration-search adapter** with changed constraints and retained prior tool results. Use an independent schema and tools, not just renamed integers in the same runner. It supports interface portability, not general open-world validity. A natural-language/coding transfer would require additional checker design and remains optional beyond this minimum.

## Strong policy set

| Policy | Purpose |
|---|---|
| G: generic reconsideration with identical preserved work | Main causal control: identical sources, typed artifacts, task records, context renderer, tool/check access and call allowance as O; completion need not satisfy O's operational discharge rule. |
| E: current acquired evidence + fresh planner | Strong source-preserving reset; tests whether the new interface adds anything. |
| O: broad reopening + preserved admissible work | Minimal proposed mechanism; invalidates completion claims without inferring narrow semantic scope. |
| P: control/membership-aware selective recovery | Strong established-principle reference; runtime reads and conservative unknown handling. Label an adaptation accurately, not as a full reproduced REVISE system unless it is one. |
| F: restart from current private sources | End-to-end reacquisition baseline; abandoned prefix costs count. |
| S: scoped reopening (optional) | Add only after CPU/development evidence shows reliable runtime scope information; model hints alone cannot exempt an obligation. |

R, the original correction-plus-unrestricted-history continuation, remains a small diagnostic arm. It is useful context but is not the matched mechanism control.

All primary policies receive the same authoritative revision. No local-vs-broadcast matrix is needed in this first study. Use the same prefix schema/records for all branches; charge their production to all policies. Add a small plain-prefix comparison in development to estimate the tax of the common instrumentation.

P receives exactly the same completion nodes, objective reads, collection membership and receipt information as O. Use a reduction fixture to determine whether O is simply the same control invalidation rule expressed through a different API. If so, label the mechanism a specialization and do not interpret the comparison as competing new algorithms. Every baseline, including already completed teams, receives the revision callback and at least one scheduled opportunity to react; never manufacture an advantage by leaving native submitted agents disabled.

If CPU inspection establishes that P and O execute the identical policy, context and schedule, report that equivalence and omit redundant live P sampling. Retain P as a conformance reference, not a fictitious independent competitor. The tabulated budget remains a conservative ceiling; freeze any deduplication before main execution and do not recycle saved calls into outcome-driven extensions.

In O, broad operational discharge means: one post-revision agent-selected query to each currently required provider, each result consumed by its assigned peer in a scheduled recovery call, and a new current-objective team answer. The root's public required-provider manifest comes from the task contract, never the hidden affected set. Retire canceled children; do not wait for obsolete tasks. Host-bind receipts to actual invocation snapshots. G sees the same open-task information but may complete without meeting this rule. Both can issue the same queries. The rule can still admit a wrong or inadequately searched answer; exact evaluation exposes that failure.

Where retained computed artifacts require checks, give other policies the same checker capability, feedback granularity and quota. Raw current observations and gold answer checks must remain separate. The mechanism may schedule more effective checks, but cannot receive privileged truths.

## Causal comparisons

1. **O versus G:** what does enforcing current reconsideration add when retained work, initial information, context, tools and opportunity are equal?
2. **O versus E:** does the complete recovery package improve on a clean planner with the same acquired sources? This combines retention and control effects.
3. **O versus P:** is the proposed state representation/useful fallback different from ordinary control-aware recovery?
4. **S versus O, if admitted:** does narrower scope save enough work to justify its metadata and failure risk?
5. **O versus R on a diagnostic subset:** does the complete intervention improve over unconstrained history retention? This is not a pure test of completion state.

For O/G, preserve evidence, candidate artifacts, context length, prompt wording and model-call allowance exactly at the branch boundary. After branching, induced queries and observations may differ and are measured. On six diagnostic worlds, also give G the same refreshed observations obtained by O. O/G estimates enforcement including acquisition; the matched-observation contrast tests what remains once information is equal. Do not interpret this small diagnostic as a well-powered independent estimate.

Use no-change O/G siblings for every main world. A real answer-preserving edit on a predetermined subset measures unnecessary reopening damage. For natural missing notes, report the observed omission rate; for injected omission/corruption, label the experiment a controlled robustness test. Never describe an artificial edge-drop distribution as a measured deployment distribution.

Every branch gets a host recovery-event ID. For sham events, the objective/source revisions remain unchanged; only the recovery-event clock advances. O's required query receipts must be after that event, making the generic reconsideration tax measurable without inventing a factual revision. G receives the same neutral notice. Receipts record both event time and true source/objective versions.

## Outcomes and analysis

**Primary:** exact final decision correctness under a fixed maximum continuation budget, paired O−G and balanced across the three families and two revision types. Score the most recent well-formed provisional team answer even if a policy has not accepted completion; missing/malformed answers are incorrect. Report **accepted-correct completion** separately, requiring both a current accepted completion and an exact answer. This prevents a stricter gate from disguising unchanged reasoning quality. A falsely accepted wrong decision remains failure on both. Report absolute rates as well as contrasts.

**Key mechanism evidence:** whether newly relevant regions were queried; whether obsolete completion prevented query issuance; current objective/query coverage receipts; duplicates in task assignments; false completion (declared done but exact answer wrong); and preservation of previously correct unaffected components. These operational measures do not prove internal cognition.

**Cost:** actual model calls, prompt/output tokens, allocated GPU time, source/tool requests, duplicate acquisition, validation work and any pre-change bookkeeping. Stop according to the runtime's operational completion policy, not the hidden gold answer. Also report fixed-slot quality curves so a method cannot win simply by declaring completion prematurely. Distinguish provisional answer quality from accepted completion.

Report sham-adjusted O−G as a secondary interaction, plus event-type differences with uncertainty. A positive interaction alone does not establish that O is beneficial after a real change. Use independent base-world/prefix clusters; peer rounds and event siblings are not independent samples. Stratify resampling by family and revision class. With six worlds per stratum, intervals will be imprecise: report paired points, bootstrap intervals and bounded sensitivity; do not promise equivalence or small-effect detection.

Predeclare one primary contrast. Treat remaining comparisons as descriptive unless multiplicity control and adequate precision are explicitly planned. Include all generated valid worlds, including poor prefixes; correct-prefix results are secondary. Select revisions before inference. Never choose an edit because it happens to fool the baseline or expose a favored omission in its trace.

## Concrete compute envelope

Planning envelope: four peers; at most four prefix and four continuation rounds (16 calls per branch); 36 main worlds, balanced as 3 families × 2 revision types × 6 worlds. Each world has one primary revision, not both. Shared prefixes are executed once. Fixed caps do not require spending unused calls after legitimate operational completion.

| Main component | 36 worlds | 24-world fallback |
|---|---:|---:|
| Prefixes plus G/E/O/P/F continuations | 3,456 | 2,304 |
| O/G no-change siblings on every world | 1,152 | 768 |
| O/G answer-preserving siblings on 6 predetermined worlds | 192 | 192 |
| Retain-history R diagnostic on 6 worlds | 96 | 96 |
| Matched-observation G diagnostic on 6 worlds | 96 | 96 |
| 8 transfer worlds: prefix plus O/G/P | 512 | 512 |
| Before/after full-information diagnostics, main plus transfer | 88 | 64 |
| **Main call ceiling** | **5,592** | **4,032** |
| Optional S on every main revision | +576 | +384 |

The matched-observation diagnostic reuses saved observations but its additional model calls are explicitly budgeted. This envelope is a capacity calculation, not a frozen final preregistration; freeze admitted arms, exact artifact transforms, query API, stopping rules and call ledger after the development pilot. Optional S brings the ceilings to 6,168 and 4,416. Robustness LLM ablations beyond the funded diagnostics require replacing optional S before main execution; CPU conformance checks do not consume the inference budget.

Reserve up to 3 allocated GPU-hours for development, 1 for loading/setup and 2 for failures/reruns, leaving 24 for main execution. That permits at most **15.45 allocated seconds/call** for 5,592 calls or **21.43** for 4,032, before extra main overhead. With S these thresholds become **14.01** and **19.57**. Apply the existing conservative 25% timing margin using observed phase/condition lengths. Two active GPUs for an hour consume two aggregate hours. These are break-even limits, not predicted T4 performance.

Do not sacrifice controls or selectively remove difficult completed worlds to fit the budget. Choose the complete 36- or 24-world design before main outcomes. If neither fits or capability fails, report infeasibility and simplify the research question.

## Minimum evidence for each claim

| Claim | Minimum evidence |
|---|---|
| The failure exists | Executable counterexample; insufficient for frequency or efficacy. |
| Agents exhibit it | Natural unfiltered prefixes plus exact decision and acquisition traces. |
| The mechanism helps | Matched O/G with total cost and sham controls; O/E/R separately estimate package effects. |
| Reopening causes the benefit | Reminder and matched-observation diagnostics; accurate attribution to acquisition versus later reasoning. |
| Scope information helps | S beats O on a quality/cost frontier under omissions, not only perfect labels. |
| The interface generalizes | Same lifecycle in the independent finite-search adapter with its own tool semantics. |
| A new algorithm exists | Not established by this plan; needs a specific difference beyond established control-dependent recovery. |
