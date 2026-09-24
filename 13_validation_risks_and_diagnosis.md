# Validation, scientific risks, and failure diagnosis

## Validation hierarchy

### Symbolic evaluator

The delivered reference runs 15 tests, including 2,260 recursive-versus-exhaustive support comparisons: 1,620 across all partial assignments for ten formulas, plus 640 randomized monotone-formula comparisons. Additional tests cover unknown-versus-false, AND failure, alternative preservation, action binding, duplicate roots, supersets, empty proofs, mixed-polarity rejection, schema errors, and exact matrix counts. These tests establish a bounded core, not full benchmark correctness.

Before the full system is accepted, add: permutation invariance; irrelevant-root invariance; proof minimality; two corrections with immutable history in CPU fixtures; version monotonicity; permission-versus-factual-support separation; false conclusions with complete negative evidence; exact action-argument binding; numeric transfer supports via independent domain enumeration; and every threshold equality boundary. Compare two implementations that do not share the same recursive rule code.

### Runtime and agent protocol

Use scripted agents emitting both good and bad outputs. Test atomic reply application, unauthorized writes, stale/unknown IDs, duplicate active slots, cancel/replace/revalidate semantics, two job decisions, malformed JSON, truncated response, context overflow, and no semantic retries. A blocked incorrect request must remain in the attempt log. No real-world tool endpoint may be reachable from the sandbox.

Test checkpoint/fork by generating two different branch suffixes and verifying that parent bytes/hashes remain unchanged, queues start identical, C's pending state is copied, idempotency keys do not cross branches, and policy order cannot change a deterministic mock outcome. Inject crashes before/after event fsync and checkpoint rename; verify resumability without duplicate execution.

### Information isolation

Canary fields such as `GOLD_ONLY_CANARY` belong only to private gold files. Fail a test if they appear in a feasible prompt, extraction prompt or cache key. Run feasible workers with only the public/runtime directory. Instrument file reads in a mock test. Oracle diagnostics receive only a mask at the documented interface, never a correct replacement action. Corpus/analysis labels do not become few-shot examples from confirmatory worlds.

### Inference validation

Confirm non-thinking templates, actual model/tokenizer revision, FP16/NF4 configuration, context caps and token accounting. Test a completed response, EOS, truncation and backend failure. Pin any parser normalization: allow removal of one outer Markdown code fence and surrounding whitespace only; no LLM-assisted repair, inferred missing fields, or best-of-many selection. Parse with strict JSON/model validation. If a global serialization fix is necessary during development, rerun affected pilot calls and freeze it before confirmation.

## Failure diagnosis table

| Observation | Candidate mechanism | Discriminating evidence / action |
|---|---|---|
| Local and full-information probes fail | Model or task weakness | Inspect exact local computation; do not attribute to coordination. |
| Raw evidence absent at C | Transport/instrumentation failure | Read receipts versus planned capsules; fix and invalidate affected block. |
| Claim is wrong before correction | Prefix reasoning failure | Prefix grade and correct-prefix secondary analysis; do not label it failed recovery. |
| q remains true; old bound action executes | Lost binding or stale recipient decision | Compare natural action supports, OC, O and ON/OR on same prefix. |
| E keeps unsupported state but O withdraws it | Support-estimation/scope failure | Missing required AND leaf, missing alternative, or invalid sufficiency in extracted label. |
| R removes Z and completion drops | Exposure over-approximation / regeneration error | Read graph path exists, exact Z support unchanged, new control-job error after withdrawal. |
| ON fails but O succeeds | Correct notices insufficient without state withdrawal | Same mask, same facts, different active-state operation. |
| O fails but OR succeeds | Rebuilding recipient state helps beyond exact typed withdrawal | Inspect newly generated versus retained errors; acknowledge context-removal confound. |
| O and OR both fail; single succeeds | Distributed integration/order bottleneck remains | Compare B's new claim and C's actual inputs; do not infer hidden cognitive causes. |
| All arms improve even without a correction | Additional inference effect | No-event and extra-review controls; do not credit recovery scope alone. |
| Runtime reports safe but action attempt was bad | Guardrail masking | Primary endpoint includes attempted semantic error; report attempted/applied separately. |
| Exact labels differ between evaluators | Formal/evaluator bug | Stop all interpretation and repair; rerun affected outputs. |
| Identical calls yield unexplained differences | Backend/seed/caching problem | Check worker fingerprints, model state and serialization; document non-bitwise nondeterminism. |
| Only synthetic edited graphs show effects | Artificially created mechanism | Treat as sensitivity calibration; do not assert natural team vulnerability. |

A diagnosis is a supported explanation, not a label chosen after reading the outcome. Some cases may remain ambiguous; allow an `unresolved` category.

## Threats and mitigations

| Threat | Why material | Mitigation and residual limit |
|---|---|---|
| New work occupies the gap | The area moved substantially in 2026 | Current audit and Gate 0; narrow empirical contribution; no unconditional novelty statement. |
| Wrapper solves the task | Symbolic truth is easy here | Evaluator is offline; feasible policies use imperfect estimates; fresh wrong actions remain possible. Deterministic solver is explicitly an upper diagnostic. |
| Labels are possible justifications, not actual cognition | Citations may be unfaithful or post-hoc | Call them evidential sufficiency labels; measure behavior separately; no claims about internal causal chains. |
| Exact support reveals hidden facts | Oracle benefit could be information gain | Use actor-delivered evidence and source-complete handoffs; log all oracle privileges. |
| Representation forces failure | OC deliberately omits bindings | OC is a mechanistic ablation only; central evidence must involve naturally estimated support. |
| Simple tasks erase the effect | Strong agents may revise reliably | Ceiling gate and informative-null criterion; structural question persists but empirical effect is not assumed. |
| Weak models exaggerate the effect | Small models may miss local logic | Strong local/single gates, correct-prefix analysis, narrow 7B diagnostic when admitted. |
| Homogeneous models correlate errors | No independent expertise diversity | Treat as a fixed team class; no claims about heterogeneous ensembles. |
| Mechanism also exists in one agent | A claim can outlive its concrete plan even without a team | State the within-team estimand. Fresh single-agent success rules out gross local incompetence but does not establish a uniquely multi-agent mechanism or an effect of decentralization. A matched-history centralized control would require a separately funded design. |
| Binding changes task difficulty | Bound actions require more detail | Information-complete controls, identical evidence, typed output caps, prefix grades; cannot perfectly equate cognitive difficulty. |
| Reset changes context length/content | OR combines state cleanup and prompt change | Interpret as a state-reconstruction intervention, not a pure persuasion/anchoring measure. |
| Fixed three-slot schedule hides cost savings | No adaptive scheduling | Claim preservation/behavior effects; do not claim fewer calls or optimal repair scheduling. |
| Structural variants have different prefixes | Matching alone does not freeze all factors | Use independent prefixes per structural variant and common prefixes only across policies; analyze base-world clusters. |
| Small diagnostic sample | 16 independent diagnostic worlds | Report exact counts and wide intervals; do not overinterpret failed significance. |
| Closed semantics and complete delivery | More favorable than private, open-world organizations | State the boundary; later research can vary hidden support and asynchronous delivery. |
| Transfer is adapted and synthetic | Domain vocabulary is not deployment validation | Exact adaptation documentation and conservative generality claims. |
| Budget optimism | Throughput/token caps can dominate | Measured admission and A/B fallback; stop rather than quietly underpower. |
| Invalid replies counted safe | Easy to game harm metrics | Separate protocol errors; primary requires completed correct jobs. |
| Selective reporting / multiple testing | Many useful process metrics | Single primary contrast, registered diagnostic family, complete tables including null outcomes. |

## Scientific limits that remain after mitigation

The result concerns short, synchronized, evidence-complete, three-agent organizations with one known correction and explicit typed state. It does not establish asynchronous convergence, Byzantine tolerance, privacy-preserving revision, long-horizon recurrence prevention, policy-revocation compliance, or recovery from irreversible external side effects. Those are later research programs, not capabilities implied by a successful benchmark result.
