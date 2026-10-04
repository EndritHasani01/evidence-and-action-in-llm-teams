# Pre-implementation investigation: synthesis

Investigated 4 October 2026. Authority: [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md), SHA-256 `049ff2b44bba185776423c4278bef890c2e55a27330513cb99757ac980a3ced1`; repository HEAD at investigation start: `16412a5bf5ea91d865f4c183191eb534fb978914`.

This is an engineering decision record, not an implementation plan or an extension of the experiment. The specification and historical artifacts were left unchanged. No model weights were loaded, GPU inference performed, development pilot run, or main outcomes generated.

## Outcome and reading order

The project is ready for a final implementation plan, with hardware admission and the exact implemented renderer remaining explicit validation gates. The important semantics can be implemented with bounded state, ordinary exact solvers, strict validation, and local persistence. They do not require a general agent platform. Read the three supporting investigations for evidence:

- [Repository, task contracts, and validation](repository-and-validation.md): reusable mathematics, obsolete runner behavior, protocol parsing, evaluation, statistics, and accounting.
- [State, replay, and persistence](state-and-replay.md): branch isolation, synchronous delivery, exact response reuse, and checkpoint behavior.
- [Inference and capacity](inference-and-capacity.md): maintained text-only loading, tokenizer probes, reproducibility, and unresolved T4/runtime gates.

Readiness for planning is not admission to expensive execution. CPU/source probes cannot establish model capability, quantized numerical stability, usable device headroom, or allocated runtime.

## Principles that govern later implementation

1. **Preserve the scientific boundaries.** The runtime owns permitted current sources and historical derived work; the evaluator owns gold, affected coordinates, correctness strata, and mathematical repair references. A public schema check must not become a correctness oracle. Model prompts must not receive condition names, branch identities, reset masks, hidden sources, or future edits.
2. **Make interventions literal state transformations.** Every sibling begins from a deep-deserialized, drained original prefix. Apply its event and retention rule once. Invalidating a source removes current authority, without deleting model-generated historical mentions. K retains the actual valid round-four candidate or its absence, including wrong answers; C clears the prescribed derived fields; F also discards acquired remote evidence.
3. **Treat a round as a barrier.** Render all four requests from immutable starting views, validate complete replies, then deliver together. Sequential physical generation is compatible with synchrony only when it cannot expose current-round outputs. New source content never appears merely because its ID is requested.
4. **Reuse responses as experimental data.** Mixed and Q first rounds consume the exact B/C raw reply records, including invalid outcomes. Check request/settings/seed/permitted-state equality first, assemble branch-specific deliveries, and never copy the parent's post-delivery recipient state. Matching random seeds is insufficient.
5. **Keep failures and missingness distinct.** A completed invalid reply or recorded timeout is a zero-credit scheduled result; an unexecuted slot is unknown. Neither inherits a previous candidate. Preserve both through restart, evaluation, and resource accounting.
6. **Make the smallest sufficient system.** Fixed four-peer/four-round state and a local per-worker SQLite store suffice. Preserve immutable inputs, exact calls, queues, responses, and checkpoints; avoid semantic dependency graphs, general routing/planning engines, live policy learning, and extra factorial arms.

## Decisions sufficiently resolved

| Finding / decision | Specification mapping | Consequence for planning |
|---|---|---|
| Reuse SILO mathematical definitions, stored fixtures, attribution, and selected CPU identities; replace its execution and generic scoring semantics | §§2.1, 5.1, 9, 10 | New explicit generators and independent exact solvers are required; installing the vendored Python >=3.13 package is unnecessary for the specified Python 3.11 system. |
| Parse strict JSON before strict Pydantic validation | §3.2 | Reject duplicate keys/nonfinite constants recursively, then enforce integer shapes, extra-field rejection, source/recipient permissions, and tokenizer caps. Protocol validity precedes all source/prose delivery. |
| Source tables, notices/receipts, derived history, candidate validity, and delivery queues require separate representations | §§3.1, 4.1–4.4 | Clearable history cannot hold the sole current-source authority or persistent notice. Unknown v2 and known tombstones have different coverage semantics. |
| Checkpointing and experimental replay are separate | §§4.2, 4.4, 9 | Application call identities and durable raw replies govern reuse; framework replay must never regenerate a required shared response. |
| LangGraph/SQLite passes the bounded replacement, branch, and resume probe | §9 | Retain the specified starting choice with replacement state and an explicit call ledger. Nine toy checks passed; full masks/Q and actual process-crash checks remain implementation gates. |
| Maintained Qwen3.5 text-only support exists; checkpoint prefix conversion and tied weights need explicit loading checks | §8.1 | Use the permitted Transformers/bitsandbytes path. A tokenizer/source check does not certify loading the language weights or running NF4 on T4. |
| Native chat templates can rewrite archived assistant text; EOS defaults and tokenizer termination differ | §§3.1–3.2, 8.1, 9 | Render history as labeled data, preserve the non-thinking request prefix and raw generated tokens, and freeze audited termination settings. Blanket special-token stripping can make invalid output look valid. |
| Per-call fresh KV/recurrent state and saved identity-based random streams are required | §§2.2, 9 | Prefer independent per-GPU worker processes: global seed setters can interfere across concurrent threads. Scheduling must not determine seeds; matched policies/events share seed assignments, while the extra replicate has new identities/seeds. |
| Statistical defaults must be overridden | §§5–7 | Bootstrap worlds within family with all siblings together; use 10,000 percentile resamples, 97.5% primary intervals, 95% descriptive secondary intervals, and the prescribed degeneracy companion. |
| Schedule and cost totals reconcile independently | §§7.3, 8.2–8.4 | Freeze both logical slots and distinct generation identities. Charge physical sharing once while attributing the original response cost to each hypothetical policy. |

The supporting state investigation records tested candidate versions (LangGraph 1.2.12 / SQLite saver 3.1.1), including the saver transaction caveat. Use the specification's small-loop fallback only if the real integration cannot preserve the required semantics. Framework choice must not change visibility, replay, sampling, or outcomes.

## Repository-specific lessons

- The archive is evidence, not a dependency tree or another specification. Old support/receipt/reopening machinery, six-family schedules, 30-hour budgets, and proposed package locks must not re-enter this five-family, 100-hour design. Historical optional proposals are requirements only where adopted by the current specification; the descriptive boundary rule now chooses C or K.
- Native source modules seed global randomness at import, and their distributions and sizes differ from the declared modified experiment. Borrow formulas and cases, not RNG lifecycle or native world generation. Store actual generated worlds and edits alongside seed streams.
- Native submission deactivates peers, receive operations mutate historical delivery state, and the API retry adapter retries indefinitely. Those behaviors are directly incompatible with fixed scheduled opportunities, immutable sibling prefixes, and bounded attempt accounting.
- Mathematical retained-result arguments assume the stated view and, where specified, a correct old candidate. They neither establish natural LLM failure rates nor justify repairing an actual candidate before exposing it. Root rechecked 8,748 archived delta-identity cases plus the scripted Prefix/Sort history and BFS ambiguity assertions without invoking the historical script's output-writing main function.

## Decisions intentionally left open

These depend on implementation or the bounded pilot, rather than more general research:

- The complete passing CUDA/PyTorch/Transformers/bitsandbytes lock, model/tokenizer revision, attention/recurrent fallback, actual language-weight inventory, and 120-second timeout adequacy.
- Whether 9B meets capability, finite-output, memory, and measured-runtime gates; whether the prescribed 4B or uniform size fallback is necessary. The study must use one accepted configuration across conditions.
- Exact prompt wording, stable record-ID spelling, schema field spelling for source references, serialization format, and thin module boundaries. They must satisfy tested visibility/equality/token contracts; speculative extensibility adds no value.
- Actual attainable/worst retained context sizes after the renderer exists. The constructed tokenizer fixture leaves only 633 tokens for additional instructions/fields; it omits some final metadata and is not a worst-context proof.
- 60 versus the nested 40 worlds, determined by the accepted configuration's conservative complete-schedule forecast before main outcomes. Provider allocation and billing details are not available in this workspace.

## Risks the implementation plan must account for

| Risk | Required check / handling |
|---|---|
| A source/reset/queue operation leaks hidden truth or changes a matched request | Assert per-peer permitted views, exact mixed/Q first-round equality, and branch-local pre-delivery reconstruction; include invalid parents and tombstones. |
| Persistence restores cleared state or re-executes generation | Use explicit replacement and durable raw call records; inject crashes before/after reply persistence and delivery commit, then verify bounded attempts and idempotent effects. |
| A permissive parser credits or forwards an invalid reply | Test duplicate/nested keys, bool/float/coerced ints, extra fields, nonfinite/overflow numbers, truncation, stale/unknown refs, duplicates/invalid recipients, and length/token limits. |
| Legal communication or retained history cannot fit caps | Tokenize the actual attainability witness, full-information candidate contracts, and worst permitted histories before GPU use; never silently truncate. |
| Quantization fits weights but fails worst-context execution | Probe the exact text-only replica on one T4; record finite outputs, device placement, FP16/FP32 paths, no offload, and >=1.5 GiB headroom. |
| Cost/sharing or statistical grouping silently changes the experiment | Reconcile all slots/attempts/replay parents, exclude round one from φ, preserve replicate zero as primary, and bootstrap world clusters within their eligible families. |
| Incompletion becomes favorable exclusion | Freeze complete manifests, distinguish zero-credit failure from unknown slots, publish paired coverage and bounds respecting shared response identities. |

## Small remaining validation gates

The later plan should include these gates without converting them into new research arms:

1. **CPU correctness and protocol:** task generators/oracles including fallback shapes; legal witness; strict parser and schema checks; no gold/condition leakage; literal B/C/K/F/L/mask/receipt transformations.
2. **State and restart:** one tiny scripted complete prefix with sibling branches, mixed/Q exact first-round reuse, delayed text release, reset replacement, independent message effects, and crash/resume accounting.
3. **Tokenizer and hardware:** actual rendered worst inputs plus reserved output; useful legal sends and complete control outputs; then the specified <=24-call/0.5-hour smoke screen and bounded development pilot. Do not spend on recovery branches before the first 90 capability slots pass.
4. **Analysis and allocation:** synthetic θ/φ sign and null cases, fragmented trajectories, preservation/empty denominators, stratified paired percentiles/degeneracy bounds, shared-response missingness bounds, and full logical/physical schedule reconciliation.
5. **Pre-main freeze:** accepted single model/environment/size/protocol, manifests, templates, seeds, timeout, estimands, and conservative measured forecast. Execute the complete accepted schedule or report documented incompletion.

The local host is CPU-only for this investigation. No T4 acceptance or throughput result exists. With all 12 reserved hours and the prescribed 25% main margin, the illustrative average allocated-time limits are approximately **15.69 seconds/new generation for 60 worlds** and **22.03 seconds/new generation for 40 worlds**. These are arithmetic decision thresholds, not runtime forecasts; measured phase/device overhead and idle allocation still matter.

Further broad research is unlikely to improve the implementation plan materially. The remaining uncertainty is concentrated in the implemented renderer/state checks and the already-specified bounded capability/resource gates.
