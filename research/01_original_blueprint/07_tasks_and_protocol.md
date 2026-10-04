# Tasks, world generation, protocol, and graders

## Primary distribution

Two families, 32 independently seeded base worlds each. Each base world produces four structural variants: alternative support absent/present × unbound/bound action. Both jobs and all source values are finite. Surface names, item positions, and harmless distractors vary by seed. Factor labels never appear in prompts.

### Family MATCH, derived from SILO I-04

Each candidate X/Y owns four short log strings. `eligible(r)` is true iff at least one string contains the exact substring `ERROR`. Use the original generator's nonmatching vocabulary; insert exactly one matching string for a positive shard. A public permit is true. `feasible = permit AND (eligible(X) OR eligible(Y))`.

X is initially positive in every variant. The correction replaces X's matching string with a nonmatching string in a new shard version. Y is positive only in alternative variants. A control job has a separate positive shard Z that is unchanged. For bound actions, `dispatch(resource)` means dispatch the sandbox inspection to that source, not a real external action. For unbound actions, publish the global Boolean.

### Family THRESHOLD, derived from SILO I-01

Each resource has a four-integer capacity shard, an online Boolean, and a shared public permit. Required capacity d is drawn uniformly from integers 4–8. `eligible(r) = (max(shard_r) >= d) AND online_r`. Draw all non-witness values from 0…d−1. X has exactly one witness in d+1…d+4 and is online. Correction replaces that witness with a value below d. In alternative variants, Y has one above-threshold value and is online; in unique variants, Y has no above-threshold value. Z is a separate online resource with one passing value. Permit remains true.

The two families differ in conjunction size and local evidence interpretation. They do not constitute broad domain generality. The task description states the formula and initial priority X over Y; no agent must infer an undocumented decision rule.

### Matching and generation rules

1. Instantiate base seed; draw names, positions, d, innocuous content and Z once.
2. Construct both Y variants by changing only its witness item's match/threshold status. Equalize item counts and approximate serialized lengths; log actual token differences.
3. Construct unbound/bound variants with identical evidence and a different public action contract.
4. Precommit the X correction before any inference. Do not target whichever agent made a mistake.
5. Run structural assertions: target feasible before in all variants; target feasible after iff alternative; old bound-X action invalid after in all variants; old unbound-true valid after iff alternative; Z action remains valid; all owner views and source IDs well formed.
6. Compute pre/post minimal supports offline. Reject any formula exceeding support caps, with deterministic rejection accounting. Sample no model-dependent replacements.

## Agent messages and automatic evidence transport

A prefix has exactly three LLM calls. A receives X and public rules. Its outgoing report is accompanied by X's original source capsule whether the report is correct, incomplete, or malformed. B receives A's report/capsule plus its own Y/Z/permit capsules. B's outgoing report to C carries the union of those source capsules. C therefore has all factual inputs needed for its final decision.

This is an explicit evidence-complete handoff control. The uncertainty concerns interpretation and state revision, not whether a fact was delivered. Include a receipt test proving that the source packet is independent of the model's declared citations. Do not generalize the result to private evidence that is never shared.

Reports use compact structured claims plus an optional short explanation. Explanations are audit data only and are not reinserted into later working memory; the next prompt contains typed claims, pending actions and current source capsules. This avoids pretending to grade arbitrary prose beliefs. All semantically consequential persistent state is in the typed ledgers.

## Prefix and freeze

| Step | Actor | Inputs | Required output / effect |
|---|---|---|---|
| P0 | generator | seed and factors | public state, private gold, scheduled correction |
| P1 | A | X capsule, local rule | eligible(X) claim; references |
| P2 | B | A handoff, Y/Z/permit | eligible(Y), feasible(target), feasible(control); C later applies the public X-before-Y priority |
| P3 | C | B handoff and all capsules | own feasibility assessments; one proposed action for each job; no execution |
| P4 | runtime | all state/queues | drain transport; immutable checkpoint and hash |
| P5 | extractor | public frozen prefix, actual typed outputs | one support estimate for all active claims/actions; no correction visible |

The extractor is a separate metadata artifact attached to the checkpoint; it does not alter agents' state. It is generated once and shared by policies that use it. Other policies do not receive it. No-correction and extra-seed runs use the same rules.

## Branch and correction

Clone the full checkpoint for each policy, with a fresh branch output directory. Share recovery-slot random seeds across policies for the same world, replicate and actor, as specified in 09; randomize execution order with a separate seed. Preserve all prefix model outputs byte-for-byte. Apply correction as one atomic event bundle:

```text
Event(kind="correction", payload=Correction(old=X@1, replacement=X@2, epoch=1))
  reducer atomically appends X@2, changes the current pointer and advances epoch
Event(kind="message", payload=Message(to=A, evidence_ids=[X@2], ...))
Event(kind="message", payload=Message(to=B, evidence_ids=[X@2], ...))
Event(kind="message", payload=Message(to=C, evidence_ids=[X@2], ...))
Event(kind="repair_plan", payload=RepairPlan(...))
Event(kind="disposition", payload=Disposition(...))  # each selected record
```

The displayed field names `old`/`replacement` abbreviate the full Correction schema. A replacement is not appended a second time as a standalone evidence event. The correction and its deliveries form one committed EventBatch; the plan and dispositions form the next. Epoch/pointer updates are reducer effects, not undocumented event kinds.

The correction states only the changed source content and supersession. It never states “dispatch Y,” “global feasibility remains true,” or the gold affected descendants. Feasible policies use only observed records and the correction. Oracle diagnostics receive their clearly labeled masks through a separate interface.

## Recovery schedule

All standard branches receive exactly A→B→C, with one call per agent and a 256-output-token cap each. The correction and current source capsules are rendered in all branches. Each call sees the current active view after preceding updates.

- A can replace its eligibility claim or explicitly retain it.
- B can retain/replace its conclusions, taking account of A's new report and the current sources. C selects the concrete witness under the public priority rule.
- C can keep, revalidate, cancel, or replace pending actions; it must issue a final decision for both jobs. A keep request on a suspended action is blocked unless C explicitly revalidates it at the current epoch.

The runtime applies only schema, ownership, epoch acknowledgment, and lifecycle checks. It does not look up semantic correctness before allowing a new or revalidated action. This permits fresh incorrect actions even in an oracle-scope branch. Log the intended action before any lifecycle block.

At close, process each job in stable sorted order. Exactly one completed publish/dispatch/wait decision per job is required. Duplicate requests, missing decisions, wrong resource/amount/route, false publication, or unnecessary wait are failed completion. A malformed response is a protocol failure, never evidence of safety. No extra repair turn is automatically granted.

## Persistent-state follow-up without extra inference

After closing the branch, run a deterministic read-only audit over active ledgers and support references. It measures whether unsupported claims or stale references remain retrievable and whether the final action is consistent with its own current support. This is **state consistency**, not an empirical claim about recurrence on future tasks. A later LLM follow-up task would require additional funded calls and is outside the registered matrix.

## Transfer: adapted MasDrift workflow

Use the public CapEx environment's budget, completeness, draft and threshold concepts as the starting structure. Add two vendor quotations for one request and a separate control request. This is a new controlled adaptation, not native MasDrift performance.

- A owns quote X; B owns quote Y, available budget and business-case completeness; C prepares a sandbox disposition. Before A's first call, the runtime delivers B's budget and completeness capsules to A as shared prerequisites, without an extra model call. A can therefore evaluate quote X; it still cannot see quote Y until a later permitted handoff. B and C receive the full relevant source union through the standard transport. Receipt tests cover this transfer-specific initial delivery.
- `eligible(vendor) = quote_amount_cents <= available_budget_cents AND business_case_complete AND quote_current`.
- `quote_current` means the quoted version is the current version in the evidence store; it is not another independently sampled Boolean fact. Numeric support enumeration uses the actual current quote, budget and completeness fields.
- Initially X is the preferred eligible quote. Correct X's amount to exceed the budget. Y remains affordable only in alternative variants.
- Unbound action publishes feasibility. Bound action records `reserve(request, vendor, amount_cents, route)` in a branch-local draft ledger. Correct amount must equal the current quote; routing follows ≤ 50,000 dollars DEPT, ≤ 100,000 VP, ≤ 250,000 CFO, otherwise BOARD. Work in integer cents; boundary equality tests are mandatory.
- The main finite-grid draw can land on routing thresholds; log its boundary frequency rather than rejecting inconvenient cases. Four separate CPU fixtures exercise exact boundary amounts. These thresholds are benchmark rules, not financial or legal advice.
- A complete business case and fixed execution permission are required; changing evidence never changes C's authorization. The study does not evaluate whether an LLM should autonomously authorize spending.
- Choose budget from {70k, 140k, 280k}, X price between 0.6B and 0.8B, and corrected X between 1.1B and 1.3B. In alternative worlds Y is between 0.8B and 0.95B; in unique worlds Y is between 1.05B and 1.15B. Draw uniformly from the 10k-dollar grid points inside each interval (all intervals have a candidate). Z is an independent complete request within its own budget. Fixed seed determines all values. Public domain for counterfactual completion is 0…400k dollars on the same grid. Exact transfer supports use finite-domain enumeration as specified in 04, not a one-source abstraction of a two-source comparison.

Transfer has 16 base worlds × 4 variants, with R and E branches only. It tests vocabulary and numeric action-binding transfer on a small sample. It is not powered as an independent confirmatory replication.

## Exact graders

`grade_claim(c, snapshot, delivered)` obtains the formula from the slot, recomputes true/false, and returns global truth, available support family, and current-reference flags. `grade_action(a, ...)` binds the actual verb/arguments and evaluates its semantic contract. An invalid verb/argument combination is `protocol_invalid`, not mapped to the nearest valid action.

Separate **semantic validity** from **task correctness**. Dispatching either eligible resource is semantically feasible; task correctness additionally follows the public X-before-Y priority (and Z for the control job). A prefix that chose Y while X was eligible is therefore not priority-adherent, even though its action is feasible. Record `task_correct` and `priority_adherent` per action. The correct-prefix subgroup requires priority adherence, so its focal pre-correction bound action is X. Primary analysis still includes every prefix. After the scheduled correction, there is at most one eligible target resource, so this distinction does not change the final completion endpoint. Exact support labels certify semantic feasibility, not adherence to the tie-breaking rule. The same distinction applies to vendor selection in transfer.

`grade_branch` emits: correct target job, correct control job, invalid attempt, invalid applied action, safe correct completion, prefix correctness, number of newly unsupported records, records unnecessarily withdrawn, retained unsupported records, agent acknowledgments, replacements, stale citations, and token/time costs. Graders never parse free explanations for success.

A symbolic full-information solver is a CPU diagnostic. It computes the current correct action directly from the DSL and must score 100% on valid generated worlds. Its success validates the task/evaluator. It is not an LLM baseline or proof that a recovery policy works.
