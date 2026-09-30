# Validation strategy

This is a proposed evidence plan, not an executed experiment. The CPU repository audit and logical counterexamples are the only experiments completed in this research phase.

## Primary research question

After an announced authoritative change, does explicitly reopening completion obligations improve recovery of newly necessary work, while preserving useful prior work, compared with a fresh planner and ordinary dependency-aware recovery?

The claim is about recovery behavior under a defined interface. It is not that negative dependencies are newly discovered or that a receipt proves open-world completeness.

## Stage 1: establish semantics on CPU

Implement the smallest lifecycle with a deterministic mock agent. Test current-version closure, omitted scope, inserted members, delayed completion, consecutive revisions, branch isolation and source-table replacement. Construct fixtures in which:

- all retained positive facts are correct, but an old stopping decision prevents an optimal answer;
- a historically affected artifact remains currently valid;
- a feasibility witness passes although optimality fails;
- no useful state can be saved and complete recomputation should win.

The first three have executed illustrations in `evidence/CURRENT_VALIDITY_COUNTEREXAMPLES.md`. They establish logical distinctions, not LLM effectiveness. A deterministic reference solver measures task difficulty and the overhead floor. If it is the best production solution for the small domain, say so; the LLM task remains an experimental probe.

## Stage 2: bounded development pilot

Begin with a small private-catalog/query adapter and 6–12 development worlds. First demonstrate that the model can solve the old and revised tasks from complete information. Then obtain naturally produced collaborative prefixes and check whether omitted-work failures arise without editing model outputs.

Start with retain, source-only reset and broad reopening. Add the control-aware provenance reference before interpreting superiority. Do not build scope extraction until broad reopening presents a meaningful accuracy/cost tradeoff. Inspect prompt and tool traces for leaked gold labels and scripted “right” queries. Tune the protocol only on development seeds.

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
| R: correction + retained work/history | Natural continuation baseline. |
| E: current acquired evidence + fresh planner | Strong source-preserving reset; tests whether the new interface adds anything. |
| O: broad reopening + preserved admissible work | Minimal proposed mechanism; invalidates completion claims without inferring narrow semantic scope. |
| P: control/membership-aware selective recovery | Strong established-principle reference; runtime reads and conservative unknown handling. Label an adaptation accurately, not as a full reproduced REVISE system unless it is one. |
| F: restart from current private sources | End-to-end reacquisition baseline; abandoned prefix costs count. |
| S: scoped reopening (optional) | Add only after CPU/development evidence shows reliable runtime scope information; model hints alone cannot exempt an obligation. |

All primary policies receive the same authoritative revision. No local-vs-broadcast matrix is needed in this first study. Use the same prefix schema/records for all branches; charge their production to all policies. Add a small plain-prefix comparison in development to estimate the tax of the common instrumentation.

Where retained computed artifacts require checks, give other policies the same checker capability, feedback granularity and quota. Raw current observations and gold answer checks must remain separate. The mechanism may schedule more effective checks, but cannot receive privileged truths.

## Causal comparisons

1. **O versus E:** does preserving admissible work and reopening tasks add value over a clean planner with the same acquired evidence?
2. **O versus R:** what is gained by revoking completion, beyond receiving the correction?
3. **O versus P:** is the proposed state representation/useful fallback different from ordinary control-aware recovery?
4. **S versus O, if admitted:** does narrower scope save enough work to justify its metadata and failure risk?
5. **O versus a same-budget generic reconsideration reminder:** does runtime enforcement add value beyond wording?

For the last comparison, preserve evidence, candidate artifacts, context length as closely as possible, and model-call allowance. On a small diagnostic subset, also give the generic control the same refreshed observations obtained by O. The first contrast includes acquisition policy; the second tests what remains once information is equal. Do not interpret the latter as a full independent estimate with only a few worlds.

Use no-change O/E siblings for every main world. A real answer-preserving edit on a predetermined subset measures unnecessary reopening damage. For natural missing notes, report the observed omission rate; for injected omission/corruption, label the experiment a controlled robustness test. Never describe an artificial edge-drop distribution as a measured deployment distribution.

## Outcomes and analysis

**Primary:** exact final task correctness under a fixed maximum continuation budget, paired O−E and balanced across the three families and two revision types. A malformed, blocked or falsely completed branch is not correct. Report the absolute success rates as well as the contrast.

**Key mechanism evidence:** whether newly relevant regions were queried; whether obsolete completion prevented query issuance; current objective/query coverage receipts; duplicates in task assignments; false completion (declared done but exact answer wrong); and preservation of previously correct unaffected components. These operational measures do not prove internal cognition.

**Cost:** actual model calls, prompt/output tokens, allocated GPU time, source/tool requests, duplicate acquisition, validation work and any pre-change bookkeeping. Stop according to the runtime's operational completion policy, not the hidden gold answer. Also report fixed-slot quality curves so a method cannot win simply by declaring completion prematurely. Distinguish provisional answer quality from accepted completion.

Report sham-adjusted O−E as a secondary interaction, plus event-type differences with uncertainty. A positive interaction alone does not establish that O is beneficial after a real change. Use independent base-world/prefix clusters; peer rounds and event siblings are not independent samples. Stratify resampling by family and revision class. With six worlds per stratum, intervals will be imprecise: report paired points, bootstrap intervals and bounded sensitivity; do not promise equivalence or small-effect detection.

Predeclare one primary contrast. Treat remaining comparisons as descriptive unless multiplicity control and adequate precision are explicitly planned. Include all generated valid worlds, including poor prefixes; correct-prefix results are secondary. Select revisions before inference. Never choose an edit because it happens to fool the baseline or expose a favored omission in its trace.

## Concrete compute envelope

Planning envelope: four peers; at most four prefix and four continuation rounds (16 calls per branch); 36 main worlds, balanced as 3 families × 2 revision types × 6 worlds. Each world has one primary revision, not both. Shared prefixes are executed once. Fixed caps do not require spending unused calls after legitimate operational completion.

| Main component | 36 worlds | 24-world fallback |
|---|---:|---:|
| Prefixes plus R/E/O/P/F continuations | 3,456 | 2,304 |
| O/E no-change siblings on every world | 1,152 | 768 |
| O/E answer-preserving siblings on 6 predetermined worlds | 192 | 192 |
| Generic-reconsideration control on 6 worlds | 96 | 96 |
| 8 transfer worlds: prefix plus O/E/P | 512 | 512 |
| Before/after full-information diagnostics | 72 | 48 |
| **Main call ceiling** | **5,480** | **3,920** |
| Optional S on every main revision | +576 | +384 |

The extra matched-observation diagnostic reuses saved current observations; if it requires additional model runs, fund it by replacing part of the optional S budget before main execution, not by hiding calls. This envelope is a capacity calculation, not a frozen final preregistration; freeze the admitted arms and exact call ledger after the development pilot.

Reserve up to 3 allocated GPU-hours for development, 1 for loading/setup and 2 for failures/reruns, leaving 24 for main execution. That permits at most **15.77 allocated seconds/call** for 5,480 calls or **22.04** for 3,920, before extra main overhead. With S these thresholds become **14.27** and **20.07**. Apply the existing conservative 25% timing margin using observed phase/condition lengths. Two active GPUs for an hour consume two aggregate hours. These are break-even limits, not predicted T4 performance.

Do not sacrifice controls or selectively remove difficult completed worlds to fit the budget. Choose the complete 36- or 24-world design before main outcomes. If neither fits or capability fails, report infeasibility and simplify the research question.

## Minimum evidence for each claim

| Claim | Minimum evidence |
|---|---|
| The failure exists | Executable counterexample; insufficient for frequency or efficacy. |
| Agents exhibit it | Natural unfiltered prefixes plus exact decision and acquisition traces. |
| The mechanism helps | Matched O/E/R comparisons with total cost and sham controls. |
| Reopening causes the benefit | Reminder and matched-observation diagnostics; accurate attribution to acquisition versus later reasoning. |
| Scope information helps | S beats O on a quality/cost frontier under omissions, not only perfect labels. |
| The interface generalizes | Same lifecycle in the independent finite-search adapter with its own tool semantics. |
| A new algorithm exists | Not established by this plan; needs a specific difference beyond established control-dependent recovery. |
