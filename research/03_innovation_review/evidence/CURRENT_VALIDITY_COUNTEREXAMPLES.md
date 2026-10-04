# Current validity, historical provenance, and search completeness

These are constructed CPU counterexamples, not model results or novelty evidence. Reproduce with `python research/03_innovation_review/evidence/recovery_counterexamples.py`; inspect `counterexample_results.json`. The mathematical principles are classical. Their purpose is to prevent a recovery experiment from confusing different capabilities.

## 1. Historical support can expire while an answer remains correct

Graph edges are `{s-a, a-t, s-b, b-t}`. A stored proof for distance(s,t)=2 uses `s-a-t`. Delete `a-t`. That proof is invalid, but `s-b-t` still proves the same distance.

**Distinction:** retracting an obsolete justification is necessary; retracting the proposition itself is not always necessary. Full dependency invalidation is safe but can discard valid results. Dependency tracking plus alternative supports already addresses this in truth maintenance. Revalidation against current evidence may recover an unrecorded alternative, but that is proof reconstruction, not a new truth-maintenance principle.

**Causal experiment:** keep the current world and answer fixed, vary whether the old alternative support was recorded. Compare actual emitted-artifact dependencies, deliberately degraded dependency logs, conservative taint, and current-state checking. Give every policy equal access to validators and new source records. Degraded logs establish sensitivity to an explicit intervention, not the natural prevalence of missing semantic dependencies.

## 2. A valid artifact can be insufficient for its old role

Initially the only s→t path is `s-a-b-t`, length 3. Insert edge `s-t`. All old edges remain current. The old path remains a feasible path. Yet it is no longer a shortest path.

**Distinction:** the capability a caller needs may be stronger than the property an artifact proves. A path proves reachability; a shortest-path claim additionally needs coverage of competing paths, or an equivalent complete certificate. An old edge-read set cannot capture an unseen new edge unless the computation also records a selector/domain/membership dependency. Dynamic graph algorithms, incremental query systems, and selector-aware recovery are direct prior art. A mechanism whose only rule is “recheck each cited fact” fails this example without any corrupted fact.

**Causal experiment:** choose insertion/requirement-widening events that preserve existing witness validity while changing optimality or exhaustiveness. Report artifact feasibility and task completion separately. Compare to a baseline that invalidates every selector/domain-dependent result on membership change. If that baseline solves the problem with small overhead, a special new mechanism may be unnecessary.

## 3. Old pruning decisions can become wrong while retained positive work stays valid

Scores are A=10, B=9, C=8, D=2; task is top two. The team keeps A/B and excludes C because 8<9. Change A to 6. B=9 remains valid; C=8 is unchanged. Repairing only the old selected items produces B/A, both with valid current scores. Correct output is B/C. The old cutoff, not C's source, is what expired.

**Distinction:** recovery must sometimes revisit what was omitted, not merely what was said. “No more work is necessary” is itself a derived claim. The result exposes negative/coverage state such as “all candidates considered,” “none qualify,” or “this branch cannot beat the incumbent.” Classic branch-and-bound, dynamic CSP, truth maintenance, and incremental search already contain related dependencies; merely logging prune reasons is not novel.

**Minimal adapter:** peers evaluate separate candidate partitions and emit typed candidate facts plus a coverage record `(domain version, processed members, bound/prune condition)`. After change, reopen only expired coverage/prune obligations. Preserve unaffected evaluated facts. A changed rule must be included in the coverage context. The evaluator independently checks global top-K, but runtime checkers should only check declared local facts and whether obligations remain current; they must not reveal the missing winner.

## The checker-is-the-solver problem

In tiny SILO arithmetic tasks, a deterministic routine validating a complete maximum/top-K/BFS answer against every source essentially performs the task. Hiding the gold array while running an equivalent exact algorithm is still substantive solver assistance. Calling it a validator does not remove that assistance.

To make the claim interpretable:

- Include a checker-equivalent fresh solve/restart and retain-history baseline, with identical contracts, feedback, and invocation budget. If the checker supplies detailed repairs, every baseline gets that same repair information.
- Separate host provenance/version checks from semantic checks. Version equality is cheap and oracle-free but cannot detect a pre-existing wrong summary. A semantic check may establish more and cost more.
- Disclose whether the checker reads the whole world, only the artifact owner's allowed shard, or only explicit evidence. Local checks cannot establish global completeness unless independently valid coverage obligations compose.
- Record validation input size, CPU time, calls, and failures. Boolean validation can still guide search through repeated queries; cap and charge it.
- Report model-free schedule/taint simulations as protocol engineering evidence and live LLM runs as behavioral evidence. Neither substitutes for the other.

## Feasibility comparison for the two leading directions

**Archive and selectively re-admit typed artifacts:** easiest implementation; can use existing source tables and add artifact status plus admission checks. Good scientific question: does conservative state isolation plus narrow artifact reuse avoid stale influence under missing declared dependencies? Largest threats are certifying computation / MemoRepair prior art, validator assistance, and benefit explained entirely by context shortening. Needs old-archive exposure ablation, sham controls, currentness-versus-correctness distinction, and equal-checker baselines. It adds independent value only if a concrete runtime admission policy survives these controls, not just if another arm beats retain-all.

**Reopen expired coverage/pruning obligations while preserving positive work:** sharper failure distinction and potentially stronger external usefulness for agent research/search workflows. Requires an explicit search/coverage interface, because native SILO only stores natural-language histories and final results. Implement one small distributed candidate-search adapter (not a generic planning framework), with requirement changes or membership insertions and exact offline evaluation. Its novelty risk is high from dynamic CSP, incremental search, and REVISE control/membership dependencies. Best outcome may be a new empirical finding about which negative decisions agents fail to reopen, accompanied by a simple reusable obligation API, rather than a new algorithm.

**Recommendation from repository feasibility alone:** make typed artifact reuse the minimal runtime substrate, but test coverage/pruning expiry as the discriminating capability if literature leaves room. Choose one primary mechanism claim. A single semester-scale project should not attempt arbitrary semantic repair plus distributed consistency plus open-world truth plus adaptive planning. Existing exact SILO tasks are useful controls; a search adapter supplies the missing process state.

## Compute boundary

The existing 48-world design already schedules 5,856 main model calls, with only 24 aggregate GPU-hours provisionally available after reserve. One extra four-round policy costs 768 calls at 48 worlds (3.2 GPU-hours at 15 allocated seconds/call), before controls. Therefore a new mechanism must replace part of the old matrix or use a predeclared diagnostic subset. Host policy/checker work can be CPU-only; LLM verification calls cannot be treated as free. More than one month permits a small adapter and rigorous CPU tests, but does not create additional GPU budget.
