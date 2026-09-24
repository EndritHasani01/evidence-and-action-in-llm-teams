# What remains valid after a correction?

**Evidential support and action repair in stateful LLM teams**  
Project specification · 24 September 2026

This document is the single source of truth for the implementation, experiments, analysis, and research report. It supersedes conflicting recommendations in the numbered blueprint, `codex_context`, old configuration files, and dependency lists. Those files remain historical inputs and reusable reference material. This deliverable specifies future work; it does not claim that the agent system, GPU pilot, or main experiments have been completed.

## 1. Project decisions and current status

Build a small, controlled study for the combined IIS + ABS course project, with a possible thesis extension. Preserve the existing research question and primary comparison. Use **LangGraph for execution and checkpoints**, a small amount of custom scientific logic, and deterministic evaluation. Start the hardware pilot with **Qwen/Qwen3.5-9B, NF4 4-bit weights and FP16 computation**; use **Qwen/Qwen3.5-4B with the same quantization** if the larger model cannot meet the capability, memory, or time requirements.

| Topic | Final decision and reason |
|---|---|
| Research identity | Study whether support representations preserve valid conclusions while repairing invalid concrete actions. Framework performance is not the research question. |
| Main experiment | 64 independent base worlds, two task families, four structural variants, and three recovery policies. Preserve the original primary estimand. |
| Diagnostics | Run the four scope/state interventions on 32 predetermined alternative-support, bound-action worlds. Concentrating on this condition doubles the original diagnostic cluster count while reducing calls; it gives no diagnostic interaction estimate across all four cells. |
| Baselines | Retain fresh restart, extra review, a fresh full-information single agent, and no-correction controls, on specified subsets. |
| Breadth | Defer the numeric MasDrift transfer, second model, second stochastic replicate, and topology sweeps. They are useful extensions, but are not necessary to identify the core mechanism. The resulting claims are correspondingly narrower. |
| Runtime | Replace the proposed custom event-sourced execution engine with LangGraph and local SQLite checkpoints. Keep explicit scientific records and readable call logs. |
| Task reuse | Use SILO's Any Match and Global Max ideas as attributed foundations for two small controlled generators. Do not install or retrofit its full execution engine, or report these modified tasks as native SILO scores. |
| Compute | Plan for at most 30 **aggregate allocated GPU-hours**, including failed calls, initialization, and idle allocated devices. The old 29.121-hour estimate is inapplicable to Qwen3.5. |
| Documentation | This specification, the runnable code/configuration, raw data, and one concise run report are sufficient. The old requirement catalogue, elaborate storage contracts, and extensive document hierarchy are not implementation requirements. |

**Implemented and inspected:** `reference/support.py` contains the bounded support algebra, an independent exhaustive evaluator, reachability, and repair-mask functions. `reference/contracts.py` contains Pydantic contracts; schemas, examples, and the old budget calculator also exist. On 24 September 2026, `python -m unittest discover -s tests -v` passed all **15 existing tests**, including **2,260 recursive-versus-exhaustive support comparisons**. The budget test checks the historical matrix, not this specification's new matrix.

**Still to implement:** the controlled generators, LangGraph workflow, branch isolation, local inference adapter, experiment scheduler, full outcome evaluator, analysis, and pilot. There is no measured Qwen3.5 throughput, VRAM result, accuracy, recovery advantage, or statistical power result in this deliverable. Reuse the reference functions and their meaningful tests; simplify the old contracts instead of preserving every field. Update the old configuration and inference requirements during implementation before running anything from them.

Assumptions: Python is acceptable; the two T4s are available in a Linux GPU environment such as the previously discussed Kaggle environment; no paid API is required. Deadline, grading rubric, and supervisor format are unspecified and do not prevent this design.

## 2. Research purpose

The question in the supplied research contract is retained:

> When an upstream correction leaves a team's intermediate conclusion true, under what conditions do estimated support records let the team preserve useful state while correctly revising actions that were bound to the superseded evidence?

A **witness** is the particular resource that makes a general statement true. Suppose X and Y can fulfill an order. A correction makes X unavailable. “The order is fulfillable” remains true through Y, but `dispatch(X)` becomes invalid. Retaining the conclusion, updating its justification, and changing the action are separate decisions.

The study crosses two factors: whether an alternative witness exists, and whether the pending action names a witness. The outcome is correct completion after one factual correction, including the preservation of a separate unaffected job. The experiment concerns policy effects **within a three-agent team**, not the causal effect of having multiple agents.

| Hypothesis | Evidence to look for |
|---|---|
| Adequate support can preserve useful work | Estimated repair has accurate support masks, retains valid records, and completes both jobs without invalid actions. |
| Claim-level abstraction can lose action bindings | Estimated repair fares relatively worse for bound actions when alternative support survives; action-support errors exceed claim-support errors; a deliberately coarse exact-control arm reproduces the distinction. |
| Correct invalidation scope may not produce correct behavior | Exact invalidation still leaves errors; removing the executor's remaining old state improves its decisions, or mechanical withdrawal outperforms an equally informative notice. |
| Conservative repair can damage valid work | Exposure-based withdrawal causes needless regeneration or new errors on the unaffected job. Conversely, reliable restart can make selective preservation practically unnecessary. |

These hypotheses can coexist. The study succeeds by producing a reliable estimate and an interpretable diagnosis, including a negative finding. No policy is required to win.

The expected contribution is a controlled empirical account of **alternative support × action binding**, with naturally generated compact handoffs, estimated support, and separate interventions on scope and recipient state. The logical distinction, support algebra, branching technique, and existence of stale plans are established ideas. The experiment is not a new recovery framework or a demonstration that an LLM is preferable to a deterministic solver in a fully specified domain.

Scope is deliberately limited: three roles using one checkpoint, one diagnosed factual update, reliable ordered delivery, short typed state, complete evidence at the planner/executor, and sandbox actions before any irreversible effect. No training, retrieval service, adversarial agent, permission revocation, open-world truth judgment, or long-horizon recurrence experiment is included.

## 3. Research grounding and contribution boundary

The following primary sources were checked on 24 September 2026. Paper findings are the authors' reports, not reproductions. Section references identify the inspected methods or evaluations. “Not established here” is a comparison with the inspected text, not proof that an experiment exists nowhere.

| Closest work | What it already establishes | What this project tests beyond that evidence |
|---|---|---|
| **From Faulty Memories to Corrected Actions**, v1, 11 Aug 2026, §§3.2–3.6, §5 and prompt appendices. [Paper](https://arxiv.org/html/2608.10502v1) | Typed runtime provenance, independent-support preservation, joint answer/state repair, and selective replay. Missing-edge inference from raw language is outside its stated scope. Its action verdict inherits from the associated plan, and it includes an LLM repair-planning baseline. | Explicitly grade the submitted action arguments; test learned sufficient-support sets and a surviving conclusion through a matched factorial design. OC below is a controlled abstraction ablation, **not a reproduction or claimed defect of this paper**. |
| **MemTX**, v2, 28 Jul 2026, §§3.3–3.5 and evaluation. [Paper](https://arxiv.org/html/2607.23929v2) | Transactional belief admission, action gating, and typed cascading repair over recorded dependencies. It explicitly limits repair to recorded provenance; compensation bookkeeping is not environmental replay. Its stronger gate does not certify that each action's own inputs passed validation. | Measure semantic validity of particular action arguments and behavior after a mask is supplied, while separating invalid attempts from applied effects. Missing dependencies defeating repair is already known. |
| **REVISE**, v1, 1 Sep 2026, §§3–4 and Appendix A. [Paper](https://arxiv.org/html/2609.00643v1) | Versioned artifacts, read selectors, conservative recovery under incomplete provenance, and commit-time revalidation. Evaluations include LangGraph and LLMCompiler applications. | Contrast exposure with semantic alternative proofs and measure stateful model behavior under equal recovery slots. Do not claim new selective recomputation or reproduce its concurrency/serving results. |
| **Fresh Memory, Stale Plans / PlanFence**, v1, 3 Sep 2026, §§3–5 and Appendix A. [Paper](https://arxiv.org/html/2609.03340v1) | Directly studies fresh facts with stale plans, including five Qwen3.5 agents. Trusted wrappers declare action dependencies; exact version lineage triggers a replan or block. Controlled live and replay studies already compare freshness with action-relevant validation. | Semantic preservation through a surviving alternative proof differs from checking whether original derivation versions remain current. Study natural estimated support and notice/withdrawal/reset interventions without a semantic action gate. Neither stale-plan discovery nor using Qwen3.5 is novel. |
| **MemoRepair**, v1, 8 May 2026, §2 and limitations. [Paper](https://arxiv.org/html/2605.07242v1) | Withdraws affected memory before rebuilding and validating successors; optimizes predecessor-closed repair selection. It explicitly examines missing influence edges. | Use fixed repair opportunities to isolate representation and behavioral errors. No new withdrawal barrier or repair-selection algorithm is proposed. |
| **Aborted but Not Forgotten**, v1, 16 Aug 2026, scope and paired-cache experiments. [Paper](https://arxiv.org/html/2608.15939v1) | A logical rollback can leave stale retained inference-cache state, including around LangGraph time travel. The paper distinguishes retained session handles from content-matched automatic prefix caches. | Exclude that separate mechanism: reconstruct each call from its allowed prompt with fresh KV and recurrent state. Recipient reset here concerns visible working records, not hidden retained caches. |

STALE separately benchmarks recognizing and behaviorally applying implicit memory updates. This project instead supplies an explicit diagnosed correction and exact bounded semantics. It therefore does not estimate general memory-update ability. [STALE, v1](https://arxiv.org/html/2605.06527v1)

Classical assumption-based truth maintenance already represents alternative justifications; provenance standards describe lineage without establishing logical sufficiency or hidden model reasoning. These are conceptual foundations, not new contributions. [de Kleer, 1986](https://www.sciencedirect.com/science/article/abs/pii/0004370286900809), [W3C PROV-DM](https://www.w3.org/TR/prov-dm/)

**Unresolved close source:** the supplied materials identify *Repair Sets Before Repair Choices: Identifiable Rollback Families for Self-Evolving Agent Memory*. The [OpenReview forum](https://openreview.net/forum?id=IJoWb6T3RJ) and [PDF route](https://openreview.net/pdf?id=IJoWb6T3RJ) still returned a browser challenge; public API/search attempts did not yield verified full text. Its detailed methods and overlap remain unverified. Do not repeat the companion's detailed claims about it as freshly confirmed evidence. Recheck before making a thesis novelty claim. The course experiment can proceed under a conservative **boundary-condition/replication** framing; inaccessible literature is not a reason to invent novelty or block all development. If a matching factorial study becomes available, cite it and explicitly frame this work as replication or a narrower extension.

This review supports the narrow comparison above, not a first-of-its-kind claim or an exhaustive literature survey. Do not add another full paper implementation as a baseline: their differing task contracts, gates, and call allowances would create a separate reproduction project. The controlled policies below expose the relevant mechanisms without pretending to be faithful reproductions.

## 4. Tasks and matched correction scenarios

Use **32 MATCH and 32 THRESHOLD base worlds**. Each base seed generates four variants, changing only alternative-witness availability and action mode. Choose the correction before any model output. Randomize display names, item positions, and harmless content; keep logical ownership and the X-before-Y priority fixed. Match evidence counts and approximate prompt lengths, and report actual token differences.

Both families draw on SILO's exact aggregation tasks: I-04 tests substring existence; I-01 computes a global maximum. The new study changes their scale, roles, outputs, timing, and evaluation. Use two short, locally seeded generator functions; a benchmark service or full SILO installation provides no necessary functionality. The inspected upstream package requires Python ≥3.13 and has inconsistent license metadata, another reason to avoid importing its engine. Attribute the task ideas; preserve upstream license notices if any source is actually copied. [SILO paper](https://aclanthology.org/2026.acl-long.1354/), [inspected generator](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/benchmark_generator/paradigm_i.py), [package metadata](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/pyproject.toml), [license](https://github.com/jwyjohn/acl26-silo-bench/blob/e74127782ed1c42fff474249961f022c063d76f2/LICENSE)

Every world contains a target job with candidates X/Y and an unaffected control job with candidate Z:

```text
feasible(target) = permit AND (eligible(X) OR eligible(Y))
feasible(control) = permit AND eligible(Z)
```

The permit is a factual source that remains true. Execution authority is a separate fixed rule: only C can perform the sandbox verbs.

**MATCH:** each candidate has four short log strings. Eligibility means that at least one contains the exact case-sensitive substring `ERROR`. Draw nonmatches from a fixed small vocabulary without that substring; insert exactly one match into every eligible candidate. X and Z start eligible. Y is eligible only in alternative-support variants. Correct X by replacing its one matching string with a nonmatch in a new version of the whole shard.

**THRESHOLD:** draw required capacity `d` uniformly from integers 4–8. Each candidate has a four-integer shard and a separate online Boolean. Eligibility means `max(shard) >= d AND online`. Nonwitness entries are uniform in `0..d-1`; X and Z have exactly one witness uniform in `d+1..d+4`. Alternative Y also has one; unique-support Y has none. All online flags remain true. Correct X's witness to a uniform value in `0..d-1`. The public rule still allows false online/permit values in counterfactual support evaluation; generator regularities are not extra logical premises.

Each shard is one source record; online flags and permit have separate source IDs. This keeps evidence sets small while retaining conjunctions. The control resource Z is independent of the corrected X source, although it shares the unchanged permit.

| Variant | Target after correction | Correct final target decision | Status of the correct old target decision |
|---|---|---|---|
| Unique support, unbound | Infeasible | `publish(false)` | Old `publish(true)` invalid |
| Alternative support, unbound | Feasible via Y | `publish(true)` | Old publication remains valid |
| Unique support, bound | Infeasible | `wait` | Old `dispatch(X)` invalid |
| Alternative support, bound | Feasible via Y | `dispatch(Y)` | Old `dispatch(X)` invalid despite true feasibility |

The control job always requires `publish(true)` in unbound mode or `dispatch(Z)` in bound mode. Prefix actions are only proposals. Before correction, correct bound target proposals select X using the stated priority. A prefix that selected Y is retained and marked as a priority deviation, not regenerated.

Before inference, assert all four truth/action transitions, control-job stability, legal ownership, and bounded support sizes. Reject only malformed generator outputs using deterministic reasons, never because an LLM failed. No transfer task or extra correction type is required for the core study.

## 5. State, evidence, and exact support

Keep four distinct records:

1. **Exposure:** which evidence, claims, and pending actions appeared in each prompt. Add read edges from every such item to every record created by that call. This over-approximates use; temporal order alone creates no edge.
2. **Declared references:** the producing agent's cited IDs. These can be incomplete or wrong.
3. **Estimated support:** one extractor's sufficient evidence sets for the frozen typed records, estimated before the correction is revealed.
4. **Exact support:** the evaluator's minimal sufficient evidence sets under the public task rules and the record owner's delivered evidence. This is not a reconstruction of hidden reasoning.

Evidence versions are immutable. A correction appends `X@2`, marks `X@1` superseded, and changes the current pointer. Repeated delivery preserves the same source/version identity; two copies do not create independent support. Derived assertions and action arguments are also immutable records; changing content creates a successor. Historical data remains available for analysis but is not automatically replayed into prompts.

A support family is **OR between sets, AND within a set**. For example:

```json
{
  "feasible_target": [
    ["x_shard@1", "x_online@1", "permit@1"],
    ["y_shard@1", "y_online@1", "permit@1"]
  ],
  "dispatch_X": [["x_shard@1", "x_online@1", "permit@1"]]
}
```

When `x_shard@1` is superseded, the first record has a surviving proof and the second does not. “Independent” here means independent of the corrected source, not statistically independent or entirely disjoint.

For a typed assertion `f = v`, a set S is sufficient if **every assignment of unknown atoms consistent with S makes f equal v**. Retain all inclusion-minimal sets. Unknown does not mean false. For monotone/unate Boolean formulas, recursive support combination is straightforward: true AND and false OR combine child proofs; false AND and true OR collect alternatives. Remove duplicates and strict supersets. The independent evaluator must enumerate subsets and compatible completions without reusing that recursion.

Use at most 10 atoms, 32 minimal proofs per record, and 10 evidence leaves per proof. Main formulas are monotone; the existing fast evaluator must continue rejecting mixed-polarity formulas. `[]` means no known sufficient proof. An empty proof inside a family is not a permitted extractor output. Facts newly introduced by correction can justify newly computed certificates; do not rename stale leaves to the new version and call that preservation.

Action semantics use **actual submitted arguments**:

| Action | Semantic validity |
|---|---|
| `publish(job, value)` | The current job feasibility equals `value`. |
| `dispatch(target, X/Y)` | Permit and eligibility of that particular candidate are true. |
| `dispatch(control, Z)` | Permit and Z eligibility are true. |
| `wait(job)` | The job is infeasible. |

Semantic feasibility and task priority are separate: a prefix dispatch to an eligible Y can be feasible but violate the X-first rule. Store truth/support, authorization, lifecycle status, and task correctness separately. A valid proof does not authorize an otherwise forbidden verb.

For active records at the cut, compute unsupported sets `U_before` and `U_after` from each owner's available evidence. `D = U_after - U_before` identifies records newly invalidated by the correction. Keep pre-existing errors separate. Exact diagnostic policies receive only the permitted record-ID mask, never replacement answers.

## 6. Agents, prompts, and episode protocol

The three roles share one frozen model configuration but have separate contexts and write ownership:

| Role | Initial information | Owned outputs |
|---|---|---|
| A, source owner | X's shard and local prerequisites | `eligible(X)` |
| B, integrating planner | A's report and sources; Y, Z, and permit sources | `eligible(Y)`, `feasible(target)`, `feasible(control)` |
| C, executor | B's report and complete source union | Its own two feasibility assessments and one pending/final action per job |

Deliver raw source capsules automatically with each handoff, even if the model's report is malformed. B receives A's sources; C receives their full union. Recovery preserves those access boundaries and delivers the same correction to A, B, and C before their slots. A never gains Y's private source merely because the evaluator knows it. No learned routing, unreliable messaging, or autonomous extra turn is introduced.

The effective agent memory is the rendered typed state. Optional short explanations are saved for audit only; later agents receive typed reports and source capsules. Describe the resulting inputs as **model-generated compact structured handoffs**, not unconstrained natural-language conversations or faithful thought traces.

### Fixed sequence

1. Generate and validate a world variant. Keep evaluator labels outside agent-visible state.
2. Run A → B → C once. C proposes both actions; nothing executes.
3. Finish all deterministic handoffs and save the full prefix snapshot, including exposure and pending actions.
4. Make one support-extraction call over the frozen public prefix, typed outputs, public rules, and owner-specific visibility. It cannot see the future correction. Save its result once; it does not modify the agents' ledgers.
5. For every assigned policy, load an independent copy of this prefix into a fresh branch. Apply the same factual correction and then that policy's repair plan.
6. Run A → B → C once in each ordinary recovery branch. Apply role-owned changes between slots. C issues explicit final decisions for both jobs.
7. Record attempted actions, apply protocol/lifecycle checks in the sandbox, and grade offline. Audit remaining active state without another model call.

Structural variants have **different realized prefixes**. Only policy branches within the same variant share an identical prefix. Reuse neither responses nor outcomes from a different repair mask or model configuration.

### Common rendering and responses

Every role prompt contains, in a fixed order: phase and epoch; owned slots; public task and priority rules; both job obligations as relevant; current source capsules; active received claims; owned active claims; pending actions and their statuses; correction; repair notice; visible IDs; and a compact reply shape. Sort by stable IDs, not correctness. Omit factor names, policy names, gold labels, and expected answers.

All arms receive the instruction that a general conclusion can remain true while an action naming a particular resource needs revision. All are told to retain an unchanged correct active record and replace an incorrect one. Do not make N/R artificially weak by hiding this rule.

Use strict Pydantic validation (`strict=True`, `extra="forbid"`), compact episode-local aliases, and these reply operations:

```json
{"ack_epoch":1,"claims":[{"slot":"eligible:X","value":false,"refs":["e07"]}]}
```

```json
{"ack_epoch":1,"retain_claims":["c04"],"actions":[
  {"operation":"new","target_action_id":"a01","proposal":{"job":"target","verb":"dispatch","resource":"Y","refs":["e03","e04","e05"]}},
  {"operation":"keep","target_action_id":"a02"}
]}
```

These are illustrative shapes, not answers embedded in experimental prompts. Claims have Boolean values; action verbs require only their relevant arguments. Allow at most four claim drafts and two action commands per reply. Only the actor's slots can change; each owner/slot has at most one active record. A new draft supersedes the owner's prior record in that slot. Omission leaves an active claim unchanged; it never restores a withdrawn claim. `retain_claims` cannot name withdrawn records.

Action commands are `new`, `keep`, `revalidate`, or `cancel`. A first proposal uses `new` without a predecessor; a replacement names and atomically cancels the targeted old action. Prefix proposals stay `proposed`; a permitted recovery command makes the chosen action `ready`, and finalization records its sandbox effect as `executed`. Suspended action arguments may remain visible with their suspended status, but `keep` cannot execute them: C must explicitly `revalidate` at the current epoch or replace them. Revalidation does **not** invoke the truth evaluator. C can therefore confidently revalidate an invalid action and fail. A cancellation without a replacement or a correct explicit `wait` does not complete a job.

Unbound mode permits only `publish`; bound mode permits `dispatch` or `wait`. Target dispatches may name X/Y, and control dispatches may name Z. Unknown IDs, foreign writes, duplicate slot/job commands, wrong argument shapes, and mode-forbidden verbs are protocol errors. A known stale reference is recorded as stale, not silently corrected or rejected using evaluator knowledge. Apply a reply atomically; a protocol error applies none of its writes. Preserve raw output, continue later scheduled slots with a failure marker, and still deliver source capsules. Trim whitespace and optionally remove one complete outer Markdown fence uniformly; perform no heuristic JSON reconstruction or LLM repair retry.

The extractor returns `{"supports":[{"n":"record_id","j":[["evidence_id", "..."]]}]}`. Ask for all independently sufficient minimal alternatives and require attention to actual action arguments. Include each record's owner-visible leaf IDs. Validate membership and shape, canonicalize duplicates/supersets, but do not repair semantic errors with gold. No correction, future source version, or exact support label enters this call.

The sandbox applies only shape, ownership, current-epoch acknowledgment, lifecycle, and duplicate-effect checks. Log each resolvable intended final action **before** any block. It does not prevent a semantically invalid fresh action. There are no external services or real transactions to undo, and each branch has its own sandbox ledger.

## 7. Recovery policies and what their comparisons identify

All policies first install the same corrected source, supersede its old version, and provide a correction notice. The ordinary recovery allowance is exactly three scheduled model calls, A → B → C, regardless of how many records a policy withdraws. They use the same prompt template, sampling settings, output limits, raw evidence, and action rules. Their active records and repair notices differ by design.

Let `L` be the active prefix claims and pending actions. The exposure candidate set is the descendants of the superseded source, intersected with `L`. Compute each repair mask once at the correction cut; later agent updates do not trigger extra automatic mask passes. OR's specified reset remains the one later intervention. Withdrawal removes a claim from active handoffs; suspension marks an action unusable by `keep`. Mask notices list affected IDs and dispositions, not gold replacement values. Do not carry withdrawn claim contents through an old message transcript.

| Policy | Intervention before recovery | Purpose |
|---|---|---|
| **N — correction notice** | Keep derived claims and pending actions active; provide the new source and a generic instruction to review the consequences. | A competent update-only baseline. It receives the correction and the common action-binding instruction. |
| **R — exposure repair** | Withdraw every candidate claim and suspend every candidate action in the exposure closure. | Conservative repair using what the runtime observed, without inferring semantic support. |
| **E — estimated-support repair** | Within the same candidate set, preserve a record if at least one extracted proof consists entirely of current, owner-available evidence IDs; otherwise withdraw/suspend it. | The deployable support-informed method. Semantic errors in an apparently well-formed proof are allowed to affect its decisions. |
| **O — exact scope** | Withdraw/suspend every record in `U_after`, including any prefix errors still unsupported. Supply only this exact ID mask. | Diagnostic upper bound on mask information, **not** on achievable model performance. |
| **OC — coarse action abstraction** | Use O's exact claim mask. For an action's mask, substitute its associated feasibility assertion: `dispatch` uses feasibility=true, `wait` uses feasibility=false, and `publish(v)` uses feasibility=v. | Tests the specific loss of witness binding while keeping claim judgments exact. |
| **ON — exact notice only** | Supply O's identical unsupported-ID list, explicitly as a warning, but retain all derived records and action availability as in N. | O versus ON separates informative diagnosis from mechanical withdrawal/suspension, with unavoidable visibility differences documented. |
| **OR — exact scope plus executor reset** | First apply O. Immediately before C's recovery slot, withdraw all C's remaining old claims, cancel its old pending actions, and rebuild a fresh C context from current sources, updated A/B reports, job obligations, and the same exact notice. | OR versus O tests removal of the executor's residual working state. It combines state and context changes; it is not a pure measurement of psychological anchoring. |

For E, missing records, malformed families, duplicate conflicting entries, or owner-inaccessible/unknown leaves cause **per-record fallback to R**; an entirely unparseable extractor response falls back for all candidates. A valid empty family means no known proof and therefore withdrawal. Do not use exact support to correct the extractor. Preserve records outside the candidate set. In no-event controls the invalidation plan is empty, even if extraction was incomplete; E must not turn routine extraction errors into unsolicited global repair.

R can withdraw the unaffected control job because its producer saw X. With complete evidence and only three agents, its closure may approach a restart. Measure this overlap and interpret the result accordingly; do not claim a large selective-replay advantage from the policy's name.

The exact policies are diagnostic interventions. They have privileged evaluator information and must not enter the operational policy ranking alongside N/R/E. Compare O with E to localize a scope-information deficit, while noting that O also repairs pre-existing unsupported records. Report that component separately and repeat the comparison on valid prefixes.

Three additional controls use the same checkpoint/model and public task rules:

| Control | Definition | Interpretation |
|---|---|---|
| **F — fresh restart** | Discard all derived state and pending actions; run fresh corrected A → B → C, three calls. | Tests whether maintaining prior state helps at all under this small task and equal recovery allowance. End-to-end cost includes the abandoned prefix. |
| **V — extra review** | One reviewer sees the corrected full public prefix and produces a ≤512-token repair recommendation, without changing state or accessing exact masks. Then run N-style A → B → C with that recommendation visible to all three. | A strong extra-inference control for E's extraction cost. Four calls are not an exact token/latency match; report actual costs. Use V to avoid confusing this policy with role B. |
| **S — fresh full-information agent** | One fresh C call receives corrected raw sources, both obligations, and public rules; it has no prior team state. | A capability reference, not a matched estimate of the effect of decentralization or teamwork. |

The no-event control continues N and E from the same frozen prefix with a neutral “no evidence changed” notice, no epoch increment, and empty masks. Its purpose is to detect unnecessary revision and handling errors. It is not an extra factual-correction scenario.

## 8. Experimental matrix, fairness, and reproducibility

Generate 64 independent base worlds, balanced across families. Each has all four variants. Select diagnostic and no-event subsets by a seeded shuffle **within family before inference**; do not choose failures or interesting prefixes. The 32-world diagnostic subset contains 16 worlds per family; its controls use only the alternative-support, bound-action variant. The eight no-event worlds contain four per family and use all variants. Subsets may overlap.

| Block | Shared material and scheduled calls | Calls |
|---|---|---:|
| Prefixes | 64 worlds × 4 variants × 3 roles | 768 |
| Estimated support | One extraction per realized prefix | 256 |
| Main N/R/E | 64 × 4 × 3 policies × 3 recovery roles | 2,304 |
| O/OC/ON/OR | 32 alternative/bound variants × 4 policies × 3 roles | 384 |
| F restart | Same 32 variants × 3 roles | 96 |
| V review | Same 32 variants × (1 review + 3 roles) | 128 |
| S capability | Same 32 corrected variants × 1 role | 32 |
| No-event N/E | 8 worlds × 4 variants × 2 policies × 3 roles | 192 |
| **Total, excluding development/pilot** | **256 realized prefixes; 3,872 short and 288 long calls** | **4,160** |

Short calls have a 256-token output cap; long calls are the 256 extractors and 32 reviewers, capped at 512. There are **64 independent main sampling units**, not 256 independent worlds or thousands of independent claims. The diagnostic comparison has 32 independent units. Run one stochastic replicate; this leaves model-sampling uncertainty only partially characterized.

Use separate deterministic seed namespaces for world generation, variant construction, subset selection, prefix sampling, recovery sampling, extraction, and execution order, for example with NumPy `SeedSequence`. A common recovery seed for corresponding actor/world/variant calls across policies reduces avoidable random variation; differing prompts still produce different distributions. Never reset a shared generator in a way that lets a previous branch change a later branch's seed.

Randomize policy order within each variant and balance family/policy work over both GPUs. Finish complete paired blocks. Store the assigned order, seed, device, and raw response. A deterministic seed does not promise identical floating-point generation across hardware or software releases; immutable saved responses support exact replay of the analysis.

All N/R/E branches start from an identical deep-deserialized prefix state before their different interventions; only logging metadata such as the new branch/thread ID may differ. New thread IDs, separate ledgers, and fresh inference state prevent one branch from affecting another. No mutable conversation, model-side session, retrieved memory, or writable store crosses branches. Model weights and tokenizer can be shared read-only by serial calls within a worker.

Common rules and raw facts are never removed to manufacture a policy deficit. Masks and active state are policy inputs, not nuisances to equalize away. The primary comparison holds **recovery opportunity** constant; E pays for an extra pre-correction extraction. Report both end-to-end and marginal recovery costs. The design does not establish fewer model calls from selective preservation because the three recovery slots are fixed.

Freeze generators, prompts, subsets, model/backend, masks, outcome definitions, and analysis configuration after the development pilot and before main data collection. Save that ordinary configuration and the actual run environment; no separate approval procedure is required. Main semantic failures are data, not reasons to retune prompts, change the matrix, or sample replacement worlds. A discovered implementation bug requires a clearly identified affected rerun, retained original logs, and an explanation in the run report.

## 9. Evaluation and statistical analysis

### Outcomes and errors

The primary binary outcome `Y` is **protocol-valid correct completion of both jobs within the assigned recovery allowance, without any semantically invalid attempted or applied final action**. For V the allowance includes its declared review call; S has its one-call allowance. Grade actual resource/value arguments, explicit job completion, and the public action-mode rules.

An invalid action blocked by a lifecycle check still fails the primary outcome. A cancelled action without a correct replacement does not complete a job. Prefix proposals have not executed and are not themselves recovery attempts. A malformed or incorrect prefix does not automatically force `Y=0` if recovery completely succeeds: include all prefixes in the primary analysis. A malformed recovery reply, timeout, or truncated response is a protocol failure and `Y=0`; do not silently give a corrective extra turn. A failed E extractor invokes its declared fallback and does not by itself force outcome failure.

Grade these secondary outcomes separately so the aggregate does not conceal the failure mode:

| Measure | Definition and denominator |
|---|---|
| Target/control completion | Correct completion of each job, over all scheduled branches. |
| Invalid attempt / invalid effect | Branch-level indicator and counts, with attempted and actually applied sandbox effects distinct. Unparseable actions remain protocol failures, not guessed semantic errors. |
| Prefix capability | Schema-valid, semantically correct claims and proposals with correct X-first selection, measured before treatment; report by cell/family. |
| End-state consistency | Unsupported active claims and actions at termination, as a count and fraction of active evaluable records. This is distinct from task completion. |
| Preservation | Fraction of semantically valid original active records that retain their original identity and active status; report the unaffected job separately. Empty denominators are NA. |
| Support quality | Exact proof-family match; proportion of estimated proofs that are sufficient; missing-alternative rate and exact-proof recall, separately for claims and concrete actions. Include extractor coverage and fallback rates. |
| Binding omission | Among extracted proofs for bound actions, the fraction that fail to establish the actual submitted resource's validity despite establishing global feasibility. |
| Cost | Calls, input/output tokens, wall latency, allocated GPU time, peak VRAM, and number of replaced records. No token saving is assumed in advance. |

For the policy mask `I`, report overlap with `U_after`, and unnecessary withdrawal `|I minus U_after| / |L minus U_after|`. To isolate correction-induced scope errors, remove `U_before` from the predicted mask and compare the remainder with `D`. Report precision and recall with raw counts and NA for empty denominators. Compute these metrics per world first or cluster their uncertainty by world; hundreds of records are not hundreds of independent experiments. Simple edge precision/recall cannot replace proof sufficiency because conjunction and alternative support matter.

Stale declared citations and unsupported claims are different errors. A claim can remain semantically supported by Y while still citing superseded X. Log both. Agent-declared references are not silently substituted for the extractor's proofs or treated as a complete account of reasoning.

### Primary contrast and uncertainty

Let `a=1` mean alternative support and `b=1` mean bound action. For each base world calculate:

```text
d_w = (Y[E,1,1] - Y[R,1,1]) - (Y[E,1,0] - Y[R,1,0])
theta = mean(d_w), giving MATCH and THRESHOLD equal weight
```

This preserves the original primary estimand. Negative theta means E's advantage over R is smaller for bound actions in the alternative-support condition. It does not, on its own, prove a support-extraction mechanism; use the support audit and exact interventions to assess that explanation. Report cell success rates, paired risk differences, theta, and a two-sided 95% interval in percentage points.

Use **10,000 stratified cluster-bootstrap resamples of base worlds**, sampling 32 worlds with replacement within each family and retaining every variant/policy belonging to each selected world. Use an explicitly selected percentile interval. Record the analysis seed. Do not independently resample branches or rely on normal binomial intervals for the repeated four-cell contrast. SciPy supports paired resampling and documents degenerate bootstrap behavior. [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

If all observed world contrasts are identical, a zero-width bootstrap interval is not evidence of certainty. Report the degenerate bootstrap result as such and use the conservative bounded-outcome interval `theta ± 4*sqrt(log(40)/(2*n))`, clipped to [-2,2], as the uncertainty interval for the primary contrast in that case. This Hoeffding bound uses the contrast's [-2,2] range and independent base worlds; it will be wide. Apply the same safeguard to degenerate paired diagnostic risk differences, replacing the range width 4 with 2 and clipping to [-1,1]. For a zero-event rate in a single cell, give exact binomial bounds within each family using its base-world count instead of claiming zero risk. [Hoeffding, 1963](https://doi.org/10.1080/01621459.1963.10500830)

The unique-support analogue and the difference between alternative- and unique-support interactions are secondary. Also report N/R/E paired differences, control-job damage, and family-specific patterns as exploratory. Avoid a large regression with many underpowered interactions. The main all-prefix analysis is supplemented by a correct-prefix analysis: both alternative-support prefixes must be correct for a world to enter the primary-contrast subset; all four must be correct for its three-way counterpart. Give the remaining world count and do not reinterpret this subset as the full generator population.

For the four planned diagnostic success comparisons **O−E, O−OC, O−ON, and OR−O**, use the same 32 paired alternative/bound worlds. Report paired risk differences, stratified cluster intervals, and discordant-pair counts. If reporting p-values, use exact McNemar tests (equivalently a two-sided binomial test on discordant pairs) with Holm adjustment across these four comparisons. No discordant pairs implies p=1, not equivalence. Keep F/V/S and all process outcomes descriptive/exploratory. [Exact McNemar definition](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html)

Infrastructure failures remain visible in operational success and cost. If a verified external interruption makes a paired block unobservable, resume it from recorded completed calls. If it cannot be recovered, disclose it and provide a sensitivity analysis excluding the **whole affected paired block**, never selectively remove an unfavorable arm. Do not label model OOMs, malformed JSON, or time-limit failures as arbitrary missing observations.

### Sample size and negative results

The 64-world size is a budget-constrained design for substantial effects. A rough 80%-power planning approximation is `2.8*s_d/sqrt(n)`, where `s_d` is the standard deviation of the paired world contrast. At n=64, hypothetical `s_d=0.6` or 1.0 corresponds to detectable interactions near 0.21 or 0.35; these are **illustrations, not measured variances or power guarantees**. A 20-percentage-point interaction is the declared practically substantial effect for this small study, not a promised detection threshold.

Before freezing the run, perform a small CPU simulation of feasible correlated binary outcomes under null and 0.10/0.20/0.30 interactions, across several plausible within-world correlations. Use at least 5,000 simulated datasets per chosen scenario to examine interval width, null behavior, and detection probability of the specified analysis. Document the joint-outcome generator and its assumptions. Do not plug in an optimistic pilot effect and call the design adequately powered. If intervals are expected to be broad, explicitly characterize the study as exploratory.

Interpret null or adverse findings according to the controls:

- If all policies reliably succeed, the finding is a bounded negative result for these short tasks. Do not inject bad plans after seeing the results to create an apparent need for repair.
- If local and fresh-agent capability is poor, the result cannot isolate a coordination or memory problem.
- If O improves on E and extractor audits show matching binding errors, incomplete estimated support is a plausible limiting mechanism.
- If O still fails while fresh execution succeeds, scope alone is insufficient; ON and OR help characterize the role of active recipient state. Reset combines multiple changes, so causal language must stay at that intervention's level.
- If R/F matches or beats E with comparable cost, conservative recomputation is a valid practical conclusion for this task scale.
- A nonsignificant estimate with a wide interval is inconclusive. Claim absence of a practically substantial interaction only if an appropriate interval excludes effects outside ±0.20, subject to the study's limited population.

The conclusions apply to these generator distributions, the selected quantized checkpoint, prompts, and fixed recovery opportunities. They do not establish behavior in open-world teams, larger models, repeated corrections, natural organizations, or real irreversible environments.

## 10. Practical system design

### Orchestration choice

**Select LangGraph.** Its explicit state transitions, local checkpoints, and branching fit the fixed prefix/correction/recovery protocol. It supplies the execution mechanics; it does not determine semantic support, policy masks, or experimental outcomes. The inspected release is 1.2.12, published 21 September 2026, under MIT. Maintained releases and its use in REVISE provide stronger evidence of suitability than popularity alone. [Release](https://pypi.org/project/langgraph/1.2.12/), [overview](https://docs.langchain.com/oss/python/langgraph/overview)

| Candidate | Fit for this experiment | Decision |
|---|---|---|
| LangGraph | Explicit Python state graph, checkpoints, and controlled resumptions. | Use; it removes the need to implement a general runner. |
| Microsoft Agent Framework | Maintained workflow executors with checkpoints, pending-message restoration, and local storage. | Viable, but its broader agent/workflow surface provides no required advantage here. [Checkpoint documentation](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints) |
| Pydantic Graph | Typed Python nodes and graph execution fit a small fixed workflow. | Viable, but changing to it offers no clear benefit over LangGraph's documented persistence and existing close-research use. [Graph documentation](https://pydantic.dev/docs/ai/graph/graph/) |

A plain Python loop is the emergency fallback only if a bounded LangGraph integration test exposes a blocking problem. Preserve the same state, prompts, slots, masks, and outcomes if that happens. Do not start by implementing another orchestration framework. No hosted orchestration service is needed.

Use two small graphs: a prefix graph A → B → C → freeze, and a continuation graph apply correction/policy → A → B → optional OR reset → C → finalize. The extractor runs once after prefix freeze. F initializes empty derived state; V adds its one review node; S is a separate single-call control. These are fixed routes selected by experiment configuration, not model-planned routes.

Persist each branch in its own `thread_id` using the local SQLite checkpointer. Import a deep-deserialized prefix into a **new continuation thread**, recording its parent prefix ID. Do not assume that `update_state` on an existing thread clones it. Avoid append-style reducers for replaceable ledgers: updating a list through a reducer can append stale items, and replaying from a checkpoint can rerun downstream calls. Use full-state replacement for owned ledgers and explicit ID/status updates. [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [time-travel semantics](https://docs.langchain.com/oss/python/langgraph/use-time-travel)

One writer or one SQLite database per GPU worker is sufficient. Use in-memory checkpoints in unit tests only. LangGraph's cross-thread store is unnecessary. Its transitive `langchain-core` dependency is acceptable; the higher-level LangChain agent package, Deep Agents, and hosted LangSmith tracing are not required. [Release dependency declaration](https://raw.githubusercontent.com/langchain-ai/langgraph/1.2.12/libs/langgraph/pyproject.toml)

### Small set of records and custom functions

Use Pydantic models for validation and ordinary dictionaries/lists for state. The essential records are:

| Record | Essential contents |
|---|---|
| Evidence | ID, logical source, version, owner, raw value, current/superseded status. |
| Claim | ID, owner, typed slot, Boolean value, declared references, creation epoch, active/withdrawn/superseded status. |
| Action | ID, owner C, job, verb and arguments, references, epoch, predecessor if replaced, lifecycle status. |
| Episode state | World/variant/branch IDs, epoch, delivered evidence by owner, active owned/received records, exposure edges, pending actions, repair notice. |
| Support estimate / repair plan | Record ID to leaf-set families and extraction errors; affected IDs and dispositions, with policy and fallback reason. |
| Call record | Stable call ID, actor/phase, exact messages, visible IDs, seed/settings, raw response, parse status, token counts, timing, device, termination reason. |
| Outcome | Completion, attempted/applied actions, state/support audit, prefix quality, and costs, with world/variant/policy keys. |

Use simple logging IDs such as `world/variant/policy/phase/actor`; no content hashes are necessary. Render evidence/record IDs to the model through stable compact aliases shared across a prefix's branches, so internal policy/factor names never leak through IDs. Keep private worlds, exact labels, and evaluation functions outside the agent-visible state schema. N/R/E functions should receive only public state, exposure, and estimates; do not hand them a gold object and rely on them to ignore it. A separate diagnostic adapter supplies O-family masks.

Custom logic is limited to the two world generators, Boolean/action semantics, support extraction prompt and validator, exposure closure, declared mask/state interventions, role-state updates, sandbox action handling, the inference wrapper, and analysis. Use standard graph/checkpoint, JSON, validation, and statistical libraries for the rest. A small Python package with `worlds`, `state`, `support`, `workflow`, `policies`, `inference`, `evaluate`, `analyze`, and a CLI is enough; these are suggested module boundaries, not required scaffolding.

Persist raw responses before applying them. On resume, a completed call ID returns its saved response, including a malformed one, rather than sampling again. If a process died with no durable response, allow at most one identical-request infrastructure retry, log both attempts if known, and charge both. Make sandbox effects idempotent by branch/job/action ID. Do not claim exactly-once model execution across a crash; require no duplicate sandbox effects and no hidden semantic retries.

Minimum dependencies are Python 3.11, Pydantic 2, LangGraph with its SQLite checkpointer, PyTorch/Transformers/Accelerate/bitsandbytes, NumPy/SciPy, pandas, and Matplotlib. JSONL and CSV suffice; a vector database, message broker, separate API server, distributed transaction system, or observability stack would not help identify the experimental mechanism.

## 11. Qwen3.5 and two-T4 feasibility

### Recommended initial configuration

Use the official Apache-2.0 checkpoints [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) and, if needed, [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B). Start with 9B because it is the user's preferred candidate; its higher task capability is a hypothesis to check, not a known pilot result.

| Setting | Initial choice |
|---|---|
| Loader | Transformers' native `Qwen3_5ForCausalLM` text-only class, correct text configuration and checkpoint-key mapping; no vision inputs or model training. |
| Quantization | bitsandbytes `load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`, `bnb_4bit_use_double_quant=True`. |
| Dtypes | FP16 compute and ordinary floating weights; preserve the implementation's required FP32 recurrent/numerically sensitive calculations. Override the checkpoint's BF16 default. |
| Context | Maximum **4,096 total tokens including output**; reject oversized prompts in development instead of silently truncating sources. |
| Thinking | Explicit chat-template `enable_thinking=False`; `/nothink` is not the documented Qwen3.5 switch. |
| Agents/reviewer | Sampling temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0; no presence penalty. |
| Extractor | Greedy decoding, the same non-thinking template, 512 output tokens. |
| Other output limits | 256 tokens for A/B/C and S; 512 for V's reviewer. |
| Execution | Batch size 1, one serial worker and one full quantized replica per T4, fresh generation/cache state per call. |

The non-thinking temperature/top-p/top-k choices follow the model card's general-task guidance. Its suggested presence penalty is deliberately omitted: repeated JSON keys and evidence IDs are required output, and adding a custom logits processor is unnecessary for this experiment. Record this departure and verify formatting in the pilot. Short output limits also deliberately differ from the card's long reasoning recommendations; this is not a benchmark of unrestricted Qwen reasoning. [Model-card inference guidance](https://huggingface.co/Qwen/Qwen3.5-9B#instruct-or-non-thinking-mode)

**Initial package candidates, not a tested GPU lock:** Transformers 5.17.0, bitsandbytes 0.50.2, Accelerate 1.15.0, LangGraph 1.2.12, and `langgraph-checkpoint-sqlite` 3.1.1. These released versions were checked as of the specification date. Start with an official PyTorch 2.14.0 CUDA 12.6 wheel if compatible with the actual host driver; the maintainer's packaging notice confirms that wheel line. Capture and pin the complete environment only after the hardware test passes. Do not automatically follow development branches or silently upgrade during the study. [Transformers release](https://pypi.org/project/transformers/5.17.0/), [bitsandbytes release](https://pypi.org/project/bitsandbytes/0.50.2/), [Accelerate release](https://pypi.org/project/accelerate/1.15.0/), [SQLite checkpointer](https://pypi.org/project/langgraph-checkpoint-sqlite/3.1.1/), [PyTorch packaging notice](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432)

### What compatibility evidence does and does not establish

A T4 has 16 GB of device memory and compute capability 7.5. Two cards are separate memory devices, not one 32 GB pool. NF4 kernels support Pascal and newer hardware, which includes Turing. That makes the proposed quantization path plausible, but does **not** certify the entire Qwen3.5 model/kernel combination. [NVIDIA T4 specifications](https://www.nvidia.com/en-us/data-center/tesla-t4/), [CUDA GPU capabilities](https://developer.nvidia.com/cuda/gpus), [bitsandbytes hardware support](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)

Qwen3.5-9B is a hybrid architecture with 24 linear-attention and eight full-attention layers. The Transformers 5.17.0 source includes both `Qwen3_5ForCausalLM` and ordinary PyTorch chunked/recurrent gated-delta-rule implementations. This provides a maintained fallback to investigate rather than a need to write custom kernels. Use supported SDPA/math or eager full attention; do not assume FlashAttention-2, BF16, FP8, or optional fused linear-attention kernels work on a T4. Record the actual selected paths and check finite outputs. [Model configuration](https://huggingface.co/Qwen/Qwen3.5-9B/raw/main/config.json), [versioned implementation](https://github.com/huggingface/transformers/blob/v5.17.0/src/transformers/models/qwen3_5/modeling_qwen3_5.py), [architecture documentation](https://huggingface.co/docs/transformers/main/model_doc/qwen3_5)

Nine billion weights at four bits would occupy about 4.5 GB **only as an ideal packed-weight lower bound**; 4B gives about 2 GB. Actual VRAM includes unquantized embeddings/output layers, quantization metadata, recurrent state, attention caches, activations, and allocator/workspace overhead. In the 9B configuration, vocabulary size 248,320 and hidden size 4,096 imply about 1.017 billion entries in each embedding/output matrix. If both untied matrices remain FP16, they alone occupy about 4.07 GB. Audit which modules are actually quantized. Neither the checkpoint download size nor the lower bound proves fit. [Configuration](https://huggingface.co/Qwen/Qwen3.5-9B/raw/main/config.json)

Bind each process with `CUDA_VISIBLE_DEVICES`, load entirely onto its one logical CUDA device, and inspect the device map. Do not silently use CPU offload or split 9B across the two cards: both would invalidate the assumed two-worker schedule. The three logical agents reuse the same worker's model weights with separate prompts; they do not need three simultaneous replicas. Check host RAM and disk as well as VRAM during loading. Expected unused vision/MTP weights are acceptable in a text-only load; missing or newly initialized language weights are not.

### Inference alternatives, with a bounded decision rule

Transformers + bitsandbytes is the selected starting point because it keeps direct control of prompts, seeds, call boundaries, and cache disposal. **vLLM is the one performance fallback worth a bounded comparison** if this path misses the time requirement. Its current documentation supports SM 7.5 and relevant Turing quantizers, but its Qwen3.5 recipes do not establish 9B NF4 throughput on these two T4s. A historical open issue reports severe slowness for a different 27B/four-T4/v0.17 configuration; that is a warning to measure, not evidence that today's 9B is unusable. [GPU support](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/), [quantization matrix](https://docs.vllm.ai/en/stable/features/quantization/), [Qwen3.5 recipe](https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3.5.html), [specific issue](https://github.com/vllm-project/vllm/issues/36589)

Allow at most 12 matched development prompts for a vLLM comparison, charging startup and failed calls. Prefer the same weights/quantization; a change to AWQ/GPTQ is a new model configuration and requires capability checks again. Adopt it only after isolation/format tests pass and the observed improvement is material, provisionally at least 20% in projected total run time including setup. Avoid turning the project into a serving benchmark.

llama.cpp is maintained and supports Qwen3.5/CUDA, but moving to a different GGUF quantization and adapter is additional work without a demonstrated benefit here. Defer it. Recent Qwen3.5-4B speculative-decoding/distillation research reports gains on A10G/Ada hardware using altered target/drafter models; it does not supply a T4 runtime estimate or justify training and adding a drafter to this study. [llama.cpp repository](https://github.com/ggml-org/llama.cpp), [quantized target/drafter technical report](https://arxiv.org/html/2607.04244v1)

## 12. Pilot, budget, and fallback decisions

### Development pilot

Run CPU tests first and prepare model files while GPUs are unallocated where the platform allows. Confirm the platform's actual quota accounting and session limits. Conservatively treat “30 GPU-hours” as aggregate allocation time, even if a particular service meters sessions differently.

The pilot uses seeds disjoint from the main study. Begin with a ≤24-call smoke test spanning local answers, short role outputs, and the longest extractor/reviewer shape; stop early for OOM, unsupported kernels, broken loading, excessive truncation, or clearly unaffordable latency. Smoke calls drawn from the scheduled pilot can count toward it if their configuration is unchanged. Hardware-only stress calls and alternate configurations are extra charged calls.

Then use this staged pilot, reusing completed calls only when model, prompts, and semantics are unchanged:

| Stage | Coverage | Cumulative calls |
|---|---|---:|
| Initial | Two base worlds, one per family, all four variants: 16 local checks, eight fresh S calls, 24 prefix calls, eight extractors, and 96 N/R/E/O recovery calls | 152 |
| Expanded | Four base worlds, two per family, all four variants: twice the initial coverage | 304 |
| Remaining interventions | OC/ON/OR on the four alternative/bound variants: 36 calls | 340 |
| Restart and review | F: 12 calls; V: 16 calls on those same four variants | 368 |
| No-event | N/E on the initial two worlds' alternative/unbound and alternative/bound variants: 24 calls | **392** |

The 32 expanded local checks consist of one corrected X-eligibility question and one corrected target-aggregation question for each of the 16 variants. The 16 S calls test full corrected decisions. Count schema-validity over every expected structured response; V's recommendation can use a small fixed review-text field.

Proceed to the main run only when:

- All CPU semantics, source-delivery, branch-isolation, action-attempt logging, and resume tests pass.
- At least 98% of structured pilot replies validate without repair; local correctness is at least 31/32; fresh S correctness is at least 15/16; correct prefixes are at least 13/16 and at least 3/4 in each structural cell. These are pragmatic development gates, not confidence bounds on population accuracy.
- Both workers load the intended language weights, produce finite outputs, and complete longest allowed calls without OOM, with at least 1.5 GiB of observed device-memory headroom. Verify actual driver, wheel architecture support, quantized modules, and attention/recurrent kernel paths.
- Prompt plus output limits fit; inference state is fresh across calls; each policy has the specified number of opportunities. The exact diagnostic arm is not accidentally made successful by a semantic action gate.
- The measured budget forecast below fits. A positive E effect, nonzero failure incidence, or “interesting” example is **not** a gate.

Prompt/schema fixes are allowed during development, followed by checks on disjoint development worlds. Never pool results from changed configurations into one pilot accuracy denominator. Reserve up to three aggregate GPU-hours for development/pilot; assess 9B feasibility early so an unsuccessful full run does not consume the entire fallback allowance. The 392-call number is coverage for one accepted configuration, not permission for unlimited 392-call reruns. If no configuration can be validated inside the total budget, stop at a clearly labeled feasibility result rather than inventing measurements or skipping the safeguards.

### Runtime accounting

Use the provisional allocation **3 hours development/pilot + 24 hours main work + 3 hours reserve = 30 aggregate GPU-hours**. Track actual allocation start/stop and both workers' idle intervals:

```text
charged GPU-hours = sum_over_sessions(allocated device count × elapsed seconds) / 3600
```

For example, keeping both cards allocated for one hour spends two GPU-hours. Two workers reduce elapsed wall time; they do not halve aggregate cost. Include model loading, warm-up, fallback probes, failures, serialization gaps, and allocated-but-idle time.

Measure input/output token counts, total call latency, prefill/decode timing where supported, and peak allocated/reserved/device memory, grouped by role/extractor/reviewer and representative prompt length. Simulate the actual two serial-worker queues from these measurements, including shared-prefix dependencies and load overhead. Bootstrap measured phase latencies for a conservative upper forecast, state its small-pilot limitations, and also show 1.5×/2× latency sensitivity. Begin the full design only if pilot cost plus the upper projected main cost plus the three-hour reserve fits 30 hours. Do not reuse the old model's assumed 400-token/s prefill and 20-token/s decode rates.

The 4,160-call design has only **20.77 allocated-device seconds per call on average** inside a 24-hour main allocation. This includes the share of overhead and idle time; decode speed alone is not the relevant target. The following are arithmetic scenarios, **not hardware measurements or forecasts**:

| Mean allocated seconds per call | 4,160 calls + six hours pilot/reserve | 2,080 calls + six hours pilot/reserve |
|---:|---:|---:|
| 10 | 17.56 GPU-hours | 11.78 GPU-hours |
| 20 | 29.11 GPU-hours | 17.56 GPU-hours |
| 30 | 40.67 GPU-hours | 23.33 GPU-hours |
| 40 | 52.22 GPU-hours | 29.11 GPU-hours |

### Predeclared adjustments

1. Keep 9B and the full design if its capability and budget gates pass. A slower but capable 9B does not justify silently reducing evaluation quality.
2. If kernel/throughput problems have a straightforward maintained-backend remedy, use the bounded vLLM check. Otherwise move promptly to **Qwen3.5-4B NF4** and re-establish capability/latency on development data. Preserve the 64-world design when this makes it feasible. All main arms must use one frozen model/backend configuration; do not mix 9B and 4B in a single primary contrast.
3. If neither usable configuration can afford the full matrix, select the **half-size design before main collection**: 32 base worlds, 16 per family; 16 alternative/bound diagnostic worlds, eight per family; four no-event worlds, two per family. Every row in section 8 halves, totaling **2,080 calls**: 1,936 short and 144 long. It permits 41.54 allocated seconds per call in 24 hours. Prefer a capable 9B if it fits this design; otherwise use a capable 4B.
4. Label the half-size study exploratory. At n=32, the illustrative detectable interactions above widen to approximately 0.30–0.49. Keep all primary factors and mechanisms; do not remove an inconvenient policy or claim adequate power for small effects.
5. If this also fails, report measured feasibility and the completed development evidence. More GPU budget, another supported runtime, or a materially revised study would require a new decision; do not run a knowingly incomplete confirmation and present it as the specified experiment.

During collection, enforce the allocation cap and checkpoint at complete paired blocks. A substantial unforeseen slowdown is reported as an incomplete run with its actual coverage, not retroactively described as a planned smaller study. No stopping rule depends on the observed E-versus-R effect.

## 13. Implementation sequence and expected outputs

Proceed in the following order. Most development and all deterministic evaluation/analysis should run on CPU so that GPU allocation is reserved for inference.

| Step | Work | Evidence that the step is complete |
|---|---|---|
| 1. Retain the scientific core | Reuse the bounded reference support functions and independent evaluator. Simplify Pydantic state and replace the stale configuration/dependency assumptions with this specification. | Existing support tests still pass; the new matrix is computed from configuration and totals 4,160 or the declared 2,080. |
| 2. Generate and label tasks | Implement the two generators, four variants, immutable source versions, action semantics, ownership, and priority. | Deterministic world examples and exhaustive bounded checks agree on supports, correction transitions, and control-job invariance. |
| 3. Build one mocked episode | Implement A/B/C handoffs, prefix freeze, continuation graph, strict responses, and sandbox attempts/effects using scripted model outputs. | One episode can be paused, branched, resumed, and evaluated without a GPU or external service. |
| 4. Add the policies and controls | Implement N/R/E and diagnostic masks; then F/V/S and no-event routes. | Hand-constructed examples distinguish alternative support from witness binding, and every route has the specified call count. |
| 5. Connect inference and analysis | Add one local generation adapter; serialize exact prompts/responses; implement the primary contrast, clustered resampling, and CPU precision simulation. | Synthetic outcome tables reproduce known contrasts; no-result and degenerate cases have honest uncertainty; analysis runs without calling the model. |
| 6. Run the bounded T4 pilot | Test the preferred checkpoint, resolve supported kernels/loading, measure both workers, and apply the stated fallback sequence. | A concise pilot report contains actual capability, latency, memory, failure counts, quota accounting, accepted configuration, and forecast. |
| 7. Freeze and collect | Save the chosen configuration, environments, seeds/subsets, prompts, and matrix; run complete paired blocks with resumable records. | Every scheduled branch has an outcome or an explicitly classified failure; costs reconcile with actual allocation. |
| 8. Audit and analyze | Recompute labels and metrics from saved data; validate denominators, mask behavior, and paired coverage; generate tables/figures. | Main all-prefix and secondary valid-prefix results reproduce from a single analysis command, without inference. |
| 9. Write the research report | Explain the contribution boundary, method, results, mechanisms supported by controls, costs, limitations, and future work. | Every numerical claim points to an exported table or figure; diagnostic oracle advantages are not deployment rankings. |

The essential new tests target scientific validity, not generic infrastructure coverage:

- Compare recursive and exhaustive support labels, including false conclusions, shared permits, alternative proofs, and rejection of mixed-polarity fast-path formulas.
- Verify X correction invalidates `dispatch(X)` while leaving alternative-supported feasibility and the Z job valid; apply the same checks to wrong model-produced arguments and false assertions.
- With mocked responses, verify identical parent states, independent child mutations, unchanged parent snapshots, separate sandbox effects, and policy-order invariance. Check that no gold canary field enters any feasible-policy prompt.
- Verify raw source handoffs survive malformed upstream replies, suspended `keep` is logged as an attempt then blocked, revalidation can still be semantically wrong, and a cancelled job is not counted complete.
- Verify E's per-record fallback, OC's deliberate abstraction, ON's lack of mechanical removal, OR's reset timing, and empty no-event masks.
- Simulate interruption around response persistence and sandbox application: completed calls replay their saved response, model retries are counted, and an effect cannot apply twice. Assert the exact call schedule for each route.

Keep the output structure small. Each run directory needs the frozen configuration and package/environment record; generated public worlds and separate private labels; shared prefix snapshots and support estimates; per-worker JSONL call/transition logs and SQLite checkpoints; one outcome CSV; and derived tables and PNG/PDF or SVG figures. Store the tokenizer/model revision identifier and source version when available, exact prompts, decoding settings, seeds, and actual hardware. No file-hashing layer, mirrored schema catalogue, formal requirement IDs, or change-control documents are required.

The research report should follow an academic sequence: Abstract, Introduction and question, Related work, Methods, Experimental setup, Results, Discussion, Limitations, Conclusion, and References, with a short reproducibility appendix. Lead Results with cell counts and the primary contrast, then support/state diagnostics, controls, and cost. Export a small figure set: factorial success rates with uncertainty; paired policy contrasts; claim-versus-action support errors; and preservation versus cost. Include a few complete successful and failed traces chosen by stated failure categories, not only examples favorable to E.

Future work may add a second checkpoint/seed, natural-language handoffs, repeated corrections, incomplete delivery, the deferred numeric transfer, or real tool environments. Each broadens a specific limitation; none is necessary to complete this course study.

## 14. Remaining uncertainties and settled boundaries

| Uncertainty | How it is resolved, and what may be claimed meanwhile |
|---|---|
| Actual 9B/4B T4 compatibility and runtime | The bounded hardware pilot must establish loading, memory, numerical behavior, and charged throughput. The evidence above establishes a plausible supported path, not a completed hardware verification. |
| Natural error rate and support-extractor accuracy | Measure on disjoint development episodes; proceed with a bounded negative-result framing if tasks are near ceiling. Do not manufacture errors or select main worlds using outcomes. |
| Statistical precision | Use the specified CPU scenarios and report actual intervals. The sample size and aggregate budget cannot guarantee detection of a small effect. |
| Overlap with inaccessible or newly released work | Recheck the unresolved OpenReview source before a thesis novelty claim; retain a boundary-condition/replication framing until verified. The question and estimator need not change merely because related work is closer than expected. |
| Quantization, non-thinking mode, and fallback checkpoint | Treat these as part of the studied configuration. A smaller fallback changes external validity, not the within-run policy contrast; mixed configurations cannot be pooled as if identical. |
| Platform quota and academic requirements | Check the actual allocation meter before GPU collection. Confirm deadline/rubric/supervisor requirements when they affect delivery; no institution-specific approval or format has been assumed. |

The settled scope is one controlled correction study with established orchestration, deterministic semantics, one accepted Qwen3.5 configuration, and a budget-checked matrix. Framework replacement changes execution infrastructure; concentrating diagnostics and deferring transfer/model sweeps narrows external validity; neither changes the preserved primary research question or estimand. The specification is complete for implementation, while the hardware measurements and research results remain work to be performed.
