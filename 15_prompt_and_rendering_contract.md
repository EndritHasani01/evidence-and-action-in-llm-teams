# Prompt and rendering contract

These are canonical initial templates. Tune only on development/pilot worlds, then store exact rendered bytes and freeze a template hash. Do not optimize prompts against confirmatory outcomes. Explanations are short audit fields, not hidden chain-of-thought or a source of evaluator truth.

## Common system template

```text
You are agent {actor}. Work on the two jobs using the public rules and the evidence
shown below. You own only the slots listed under YOUR_WRITES. Other agents can
be mistaken. Evidence versions marked superseded are historical, not current.
When an evidence update arrives, reconsider the conclusions and exact action
arguments that it affects. A still-true general conclusion may have a different
supporting instance. Follow the same rule whether or not a repair notice is present.
During recovery, retain an unchanged correct active record instead of rewriting
it. Replace an incorrect record. A withdrawn claim must be regenerated; it cannot
be restored merely by listing its ID under retain_claims.

Return one JSON object matching REPLY_SHAPE. Use only IDs in VISIBLE_IDS.
Do not output Markdown, additional text, or hidden reasoning. The note field is
optional and at most 160 characters. Do not invent source content. For a bound job
with no eligible option, C must explicitly choose wait; otherwise select the
eligible option under the stated priority. For an unbound job, publish its Boolean
feasibility, including false when no option is eligible. Only C emits actions.
```

The sentence distinguishing general conclusions from action arguments is present in **every arm**. Withholding this obvious rule from the baseline would manufacture an avoidable failure. If that common instruction eliminates the effect, report the result or apply the pilot ceiling rule.

## User prompt layout, fixed order

```text
PHASE: {prefix_or_recovery}; EPOCH: {epoch}
YOUR_WRITES: {allowed_slots_and_action_rights}
TASK_RULES: {public_formal_rule_in_plain_language}
JOBS: {two_job_obligations_and_public_X_before_Y_priority}
CURRENT_EVIDENCE: {sorted_source_capsules}
INBOX_CLAIMS: {sorted_active_received_claims}
YOUR_ACTIVE_CLAIMS: {sorted_owned_claims}
YOUR_PENDING_ACTIONS: {sorted_owned_actions_with_runtime_status}
CORRECTION: {same_public_delta_or_none}
REPAIR_NOTICE: {ids_to_reconsider_and_runtime_dispositions}
VISIBLE_IDS: {compact_aliases}
REPLY_SHAPE: {role_specific_compact_shape}
```

Sorting is by stable ID, not truth. Sources carry ID/key/version/value/owner, but no gold atom, factor label, expected result or proof set. Public task rules explain how to interpret raw values. Prefix A gets its own capsules plus the shared budget/completeness prerequisites in transfer; B gets the documented union; C gets the complete union. Recovery receipts are updated after the source delta.

Superseded raw source values remain in audit files, not the CURRENT_EVIDENCE section. Withdrawn claims are absent from active sections; their IDs appear in REPAIR_NOTICE. ON leaves them active but includes the same exact notification IDs. OR removes C's old owned views immediately before rendering C's slot, while retaining current source inputs and fresh A/B reports.

## Role-specific reply examples

A:

```json
{"ack_epoch":1,"claims":[{"slot":"eligible:X","value":false,"refs":["e07"]}]}
```

B:

```json
{"ack_epoch":1,"claims":[
  {"slot":"eligible:Y","value":true,"refs":["e03","e04"]},
  {"slot":"feasible:target","value":true,"refs":["e03","e04","e05"]},
  {"slot":"feasible:control","value":true,"refs":["e06","e05"]}
]}
```

C, replacing the target's pending action while retaining the unaffected control:

```json
{"ack_epoch":1,"claims":[{"slot":"feasible:target","value":true,"refs":["e03","e04","e05"]}],
 "actions":[
  {"operation":"new","target_action_id":"a01","proposal":{"job":"target","verb":"dispatch","resource":"Y","refs":["e03","e04","e05"]}},
  {"operation":"keep","target_action_id":"a02"}
 ]}
```

Examples are development fixtures only. Actual aliases differ and must be inserted consistently. A source capsule with multiple raw items is one evidence version; online and permit sources have their own versions. Never attach a generated response's fabricated atom label to the capsule.

## Support extractor template

```text
Given the frozen task rules, delivered evidence, typed claims and exact proposed
actions, identify sufficient sets of the displayed evidence-version IDs for each
node. A set is an AND: all its listed evidence is needed together. Multiple sets
are OR alternatives. Include each independently sufficient alternative you can
justify. A citation alone does not establish sufficiency. Support for a statement
that some option exists need not support an action naming a particular option.
Check the actual arguments of each action. You do not know which source, if any,
will later change. Do not predict a correction. Do not use hidden evidence.
Return {"supports":[{"n":"node_id","j":[["evidence_id",...],...]}]}.
Return j:[] if you cannot establish a support set. Never emit an empty proof []
inside j. Do not output commentary. Nodes: {nodes}. Evidence: {evidence}.
Rules: {public_rules}. Valid leaf IDs: {ids}.
```

The prompt asks for evidential sufficiency, not “what the model really thought.” Parse with `ExtractorReply.model_validate_json(raw, strict=True)` after the documented optional fence removal. Enforce provided-node and leaf-ID membership; canonicalize duplicates/supersets; record any rejected node. Do not evaluate entailment until offline scoring. Missing nodes fall back to R in E. The correction and gold support sets never appear here.

## Extra-review template

```text
Review the team's current two-job decisions after the displayed source update.
Use only the public rules and current evidence. Give a concise review of what
the team should reconsider. You cannot edit state. Do not output a dependency
graph or per-record invalidation mask. Return {"review":"..."}.
```

Limit review to 512 generated tokens and 3,584 input tokens; use the same agent sampling configuration. B's reviewer stage is allowed to recognize the right action; it is a strong extra-inference baseline. Append the review to all three recovery prompts in a fixed field and charge the extra input tokens. Its potentially longer contexts must be included in the hardware forecast, not hidden under the ordinary mean.

## Parser and limits

Use JSON deserialization and strict Pydantic validation; no coercion of `"true"` to Boolean or `"1"` to integer. Permit one outer Markdown fence removal plus whitespace trimming, identically for every policy, and log normalization. No other heuristic reconstruction. Optional reply arrays default empty, but missing required job decisions cause task failure. Enforce role-specific allowed slots and at most one action command per job after resolving target IDs.

Before a call, tokenize the fully rendered prompt plus output allowance. If over 4,096, stop with a context-overflow failure. During pilot, revise a common serializer to remove redundant metadata; never silently drop a relevant source or preferentially trim old state in one arm. The production call log stores exact serialized text, count and hash. The shorter role-specific shape, not the full schema collection, is included in prompts.
