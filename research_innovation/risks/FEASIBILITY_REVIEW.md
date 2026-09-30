# Independent feasibility and causal-design review

Reviewed 2026-09-30 by the repository-audit researcher. Scope: `VALIDATION_STRATEGY.md`, `RESEARCH_REDIRECTION.md`, and `RECOMMENDED_INNOVATION.md` as read during this review. This is an independent critique, not a modification of those synthesis artifacts. No model inference was run.

## Overall assessment

The proposed direction fits the real problem better than another generic reset arm, and the current documents correctly disclaim a new foundational algorithm. A small obligation lifecycle and finite query adapter are feasible with more than one month of implementation time. The 30 GPU-hour constraint remains conditional on an actual model/hardware pilot. The arithmetic is correct, but the design is not yet preregistration-ready: baseline state differences, query semantics, completion acceptance and several diagnostic costs still need operational definitions.

The largest risk is causal, not computational. The main O−E contrast currently mixes preservation of typed computed work with reopening of completion. A win could establish a useful combined policy while providing no evidence that stale stopping decisions, rather than artifact reuse or shorter context, explain the improvement.

## Required resolution before freezing the next specification

### 1. Separate a useful policy contrast from the mechanism claim

As written, E receives current acquired evidence and a fresh planner, while O also retains independently admissible artifacts and explicit open obligations. If E discards correct partial computations, an O advantage may be entirely ordinary computation reuse. O versus R additionally changes raw prose exposure, old decisions in context and possibly acceptance checks.

The primary O−E contrast is defensible as a **combined-policy effectiveness** question. It does not isolate reopening. The description of O−E should say so. For a causal reopening claim, the generic-reminder diagnostic must hold fixed:

- current sources and retained typed computed artifacts;
- context rendering, history treatment and old receipt visibility;
- query access, validator access and feedback granularity;
- maximum model/tool opportunity and correction notice;
- only the runtime treatment of completion/coverage status versus advisory reminder.

One economical choice is to use the existing generic-control subset as an artifact-identical clean-context control. Do not add an entire extra main arm merely for nomenclature. If six worlds cannot distinguish the alternatives, the result can still support policy efficacy, but causal attribution to completion management remains tentative. A factorial check on a small subset can separate artifact reuse from enforced reconsideration; it need not be a full large matrix.

### 2. Define R, E, O and P as exact state transforms

Before inference, write a table stating for each arm which source records, computed artifacts, prose, candidates, child obligations, closure receipts, query caches and assignment ownership survive the boundary. State which visible bytes differ and which host acceptance checks differ.

The strong P baseline is essential. It should track actual tool/provider reads, query/domain versions, and explicit control/membership effects, with conservative treatment of unknowns. It must have the same automatically instrumented task boundaries available to O. Do not implement P as only a leaf-fact citation graph and then conclude O solves missing negative dependencies. Conversely, if P's conservative rule reopens the same root and retains the same admissible work as O, they are equivalent on that case. Test that equivalence on CPU and do not present different labels/prompts as different algorithms.

Fresh E already receives the task again without old stopping decisions. If O and E retain the same work and have the same operational completion rules, O may be exactly a structured representation of the fresh plan. That is an informative simplification, not a reason to weaken E.

### 3. Specify what a query and receipt can reveal

The current text correctly separates current process receipts from decision correctness. The actual provider/query grammar remains underspecified, so gold leakage cannot yet be ruled out.

For the finite adapter, publish each query's inputs, outputs, scope and cost. A raw-record listing or a predicate filter may be legitimate task access. An `argmax`, sorted top-K response, complete shortest-path query, or predicate that already identifies the newly relevant option may solve the reasoning problem in the host. Even without exposing the hidden gold file, such an API supplies solver assistance. It must either be part of the task definition for every arm or be removed.

Domain versions, complete membership lists and cache-validity checks must have clear ownership. Do all peers see the existence of a hidden new option? Can a provider tell an agent that a query is incomplete under the changed objective? The latter may require semantic relevance knowledge. A receipt should report what was run and under which domain/selector version; it should not silently judge whether the agent selected the right search.

If semantic artifact checks are available, checker-equivalent baselines need identical results and budgets. Checking a complete SILO answer against all inputs is effectively solving the task. Prefer typed source/currentness checks or explicitly limited local predicates unless whole-task verification is intentionally studied.

### 4. Make runtime enforcement falsifiable rather than tautological

Define exactly what changes `NEEDS_RECONSIDERATION` to `CLOSED`. A current-epoch `done` acknowledgement alone lets the old answer be restamped immediately. Requiring a specific new query can instead manufacture discovery through host-prescribed acquisition. Both are possible policies, but neither should be left implicit.

A useful implementation distinguishes fresh acknowledgement, a newly executed agent-chosen query, and a substantive decision check. The runtime may enforce a minimum operational event; the evaluator separately judges query adequacy and answer quality. Report how often agents perform formally fresh but irrelevant work.

Every baseline should receive and process at least one authorized revision callback after the correction. Do not let a retained old `done` flag prevent R from seeing the correction while O alone resumes execution. That would mainly demonstrate the native runner's terminal-state behavior or ordinary epoch fencing, not an LLM recovery advantage. Delayed old completion rejection should be a common safety invariant unless the experiment explicitly labels its removal as an engineering fault injection.

## Budget audit

All stated main-call totals are correct for the listed rows:

| Quantity | 36-world schedule | 24-world schedule |
|---|---:|---:|
| Prefix plus five changed continuations, 16 calls each | 3,456 | 2,304 |
| Two sham continuations per world | 1,152 | 768 |
| Six answer-preserving pairs | 192 | 192 |
| Six generic-control continuations | 96 | 96 |
| Eight transfer prefixes plus O/E/P | 512 | 512 |
| Two full-information controls per main world | 72 | 48 |
| Total | 5,480 | 3,920 |
| Optional scoped arm S | +576 | +384 |
| Total with S | 6,056 | 4,304 |
| 24-hour main allowance, seconds/call | 15.7664 | 22.0408 |
| Same allowance with S | 14.2668 | 20.0743 |

Remaining budget decisions:

1. The before/after diagnostic row covers only the main worlds. Equivalent controls on eight independent transfer worlds require 16 more calls. Include them or explicitly state that transfer capability is established by separately budgeted development cases.
2. A matched-observation continuation is an additional model run even when its observations are saved. If O's observation schedule requires generating its future trace first, it is a sequentially constructed diagnostic, not an independently randomized acquisition condition. The current instruction to fund it from optional S works only if an explicit amount is reserved even when S is not admitted. Six 16-call continuations cost 96 calls.
3. Development uses 6–12 worlds without an exact call ledger. Five changed arms alone require 576–1,152 calls including prefixes, before shams, complete-information diagnostics, plain-prefix instrumentation checks, smoke tests, failed model loads or a second model candidate. At 15 seconds/call, 576 calls use 2.4 hours and 1,152 use 4.8 hours. Thus 12 full pilot worlds cannot fit a three-hour development allowance at that illustrative speed. A staged pilot is sensible, but specify phase caps and stop conditions before hardware allocation.
4. The no-S main ledger has very little reason to spend the unused S allowance by default; it should remain optional reserve. Each extra live ablation consumes the same 30-hour ceiling. A smaller complete schedule is preferable to selective incomplete branches.
5. Timing thresholds assume the main allowance can all be spent on calls. Query processing, serialization, time with allocated but idle GPUs and provider pauses still count. Use observed phase-specific allocated time, not only decoder throughput.

These issues do not invalidate feasibility. They prevent claiming a guaranteed fit before the pilot. No source in this research phase measures Qwen3.5 throughput on T4.

## Early stopping and outcome definitions

The proposed design permits legitimate early completion while also requesting fixed-slot quality curves. Freeze how these coexist. A stopped branch can retain its last provisional candidate for descriptive quality-at-time plots, but those points are not new model answers. Show accepted completion, provisional exact correctness, active/open task counts, consumed calls and right-censoring separately.

An “exact final correctness” endpoint should not automatically mark a numerically correct but operationally blocked branch as wrong unless the target is explicitly **valid accepted completion**. Report both values to reveal overconservative reopening. Otherwise a method that safely refuses false closure can look arbitrarily worse, or a method that relabels an answer can look arbitrarily better.

O/E sham siblings are a good control. Clarify whether a sham triggers broad reopening, whether E resets, and whether no source/objective revision number advances. If the method responds only to real revision events, one sham cannot isolate all generic effects of runtime reopening. An explicit boundary/reminder control should receive equivalent interaction opportunities without an invented source change.

Revision type is balanced across independent worlds rather than paired within each prefix in the proposed main schedule. That is affordable and legitimate; event-type differences must be described as differences across generated strata, not as paired effects of revision type. With only six worlds per stratum, uncertainty remains large. Family and revision labels do not identify the causal effect of difficulty, affected footprint or search coverage.

## Repository fit and implementation burden

The proposal correctly keeps mathematical task semantics and replaces the native execution semantics. Native SILO has no revisable root/child completion obligations, query-selected information acquisition, revision receipts, immutable intervention forks or provisional submission loop. These are new implementation tasks, not configuration changes.

The repository findings make a small new loop or minimal LangGraph graph preferable to preserving the old runner:

- submitted peers currently stop permanently;
- P2P receive mutates historical message files;
- broadcast can replay old messages after a skipped receive round;
- SFS collision semantics depend on writer order;
- generic partial scores and several analysis accounting paths are unsuitable.

For more than one month, three structural families plus one small independent adapter are plausible if the interface is frozen early. The first implementation week is ambitious but possible for basic lifecycle/CPU fixtures. Scope extraction, real asynchronous scheduling, dynamic checkpoint migrations and open-world checkers would exceed the current research need.

The proposed algorithmic tasks still involve a few rounds of cheap arithmetic. They establish a controlled recovery mechanism, not measured savings after days of work. Counted expensive-query costs can test scheduling logic, but remain synthetic costs. Retain this limitation when describing practical utility.

For the finite-search transfer to count as interface portability, use independent tool schema and objective/record types and reuse the same lifecycle implementation without task-specific recovery rules. Eight transfer worlds support only a small demonstration. If the adapter is simply the same top-K arithmetic under supplier names, label it a representational transfer rather than a new application domain.

## Artifact and preservation checks performed during review

- Recomputed the main-call arithmetic and timing thresholds above.
- Compared all 36 source-manifest hashes and all 180 benchmark hashes against `audit_results.json`: no mismatches.
- Compared current specification SHA256 to the audit: still `D6DA776F73B6AD03874DC17DF546B6662DB3569C9F0B80780179CDFFE44FBC00`.
- Confirmed counterexample result status: three deterministic cases passed. These illustrate logical failure possibilities, not live-agent prevalence or superiority.
- Added `sys.dont_write_bytecode = True` to the evidence audit script so subsequent imports do not generate caches in the inspected tree.
- Removed only the generated `research_innovation/evidence/__pycache__/audit_repository.cpython-311.pyc` and then its empty directory, using explicit verified paths and native PowerShell. No source, dataset or other-directory cache was deleted.

## Review decision

Proceed with the proposed research direction as a **conditional, bounded empirical/interface contribution**. Before changing the authoritative specification, resolve the exact arm-state table, query/receipt contract, operational reclosure gate and complete diagnostic/development call ledger. Keep the strongest current-data reset and control-aware recovery baselines. If the minimal O policy becomes equivalent to them, report that simplification and focus on the observed failure taxonomy rather than inventing architectural differences.
