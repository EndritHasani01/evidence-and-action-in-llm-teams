# Research Requirements Specification (RRS)

Normative words: MUST is a release gate; SHOULD requires a documented reason to depart; MAY is outside the confirmatory contract. This is a research instrument with a command-line interface. A dashboard, generic agent framework, or autonomous deployment system is not required.

## Research requirements and acceptance evidence

| ID | Requirement | Acceptance evidence |
|---|---|---|
| RQ-01 | Estimate the policy × action-binding interaction in worlds with surviving alternative support. | Registered contrast, all paired branches, world-level confidence interval. |
| RQ-02 | Separate support-selection errors from behavioral repair errors. | Natural estimate, full exact scope, coarse action-scope ablation, and exact-scope state-rebuild branches from common prefixes. |
| RQ-03 | Rule out gross local-task incompetence as the explanation of team failures. | Local probes, information-complete single-agent control, correct-prefix secondary analysis; no claim of a fully matched causal decentralization test. |
| RQ-04 | Use existing research infrastructure with explicit attribution and transformation boundaries. | Pinned SILO source provenance, native calibration, adapter tests, changed-task documentation. |
| RQ-05 | Use exact observable semantics without pretending to observe internal reasoning. | Typed claims/actions, two independent symbolic evaluators, no LLM judge for primary endpoints. |
| RQ-06 | Account for extra inference and extraction. | Separate prefix/extraction/recovery cost ledger; reflection control; equal recovery-slot main comparison. |
| RQ-07 | Avoid cherry-picking naturally successful prefixes or favorable corrections. | Generated IDs/seeds frozen before inference; structural correction target precommitted; all outcomes retained. |
| RQ-08 | Expose plausible null/negative results. | Continue/pivot rules independent of a favored policy winning. |
| RQ-09 | Respect 30 aggregate GPU-hours. | Hardware admission pilot, measured budget forecast, scheduler stop before overspend. |
| RQ-10 | Maintain a defensible novelty claim. | Close-work comparison, unresolved access items resolved before preregistration or novelty narrowed further. |

## Functional requirements

| ID | Component | MUST behavior |
|---|---|---|
| FR-01 | World generator | Emit matched unique/alternative × unbound/bound variants, one correction, a control job, source ownership, public rules, and evaluator-only labels. |
| FR-02 | Generator validator | Verify all structural constraints before any model call; reject by reason without consulting model output. |
| FR-03 | Evidence store | Append versions; preserve histories; maintain one current version per key. |
| FR-04 | Agent runner | Execute A→B→C prefix and recovery schedules; enforce ownership and output schemas; retain malformed responses as failures. |
| FR-05 | Transport | Deliver immutable source capsules independently of the agent's semantic message; log send/receive/read IDs. |
| FR-06 | Claim ledger | Append typed claims, supersession, and disposition events; provide owner-specific active views. |
| FR-07 | Action ledger | Separate proposed/suspended/ready/executed/cancelled states; immutable arguments and idempotency keys. |
| FR-08 | Provenance | Store exposure, declared references, extracted support, and evaluator support in separate artifacts. |
| FR-09 | Extractor | One pre-correction call per realized prefix; bounded DNF; fail conservatively and log fallback. |
| FR-10 | Correction | Atomically append replacement evidence, advance epoch, and emit a common correction notice. |
| FR-11 | Checkpoint | Capture world, all agent state, queues, ledgers, prompt receipts, RNG seeds, and content hashes at a quiescent cut. |
| FR-12 | Branching | Clone from a read-only checkpoint; never mutate the common parent; branch IDs determine output paths. |
| FR-13 | Recovery policies | Implement each policy exactly as specified in 08; emit an inspectable RepairPlan before executing it. |
| FR-14 | Prompt builder | Render only runtime-authorized data; bound context deterministically; fail on overflow rather than silently truncate relevant evidence. |
| FR-15 | Sandbox | Record every attempted action; apply only schema/ownership/state/idempotency checks in feasible arms, without hidden semantic-oracle gating. |
| FR-16 | Evaluator | Grade actual claims, action arguments, attempted/applied effects, support decisions, and persistence; never use agent explanations as gold. |
| FR-17 | Orchestrator | Execute registered manifests, track token/time use, resume crash-safe at call/event boundaries, and finish paired blocks together. |
| FR-18 | Caching | Cache exact calls with seeds and backend/model hashes; share only identical pre-treatment artifacts. |
| FR-19 | Analysis | Produce raw paired outcomes, bootstrap intervals, exact paired diagnostics, mechanism tables, and registered figures. |
| FR-20 | Exports | Emit versioned JSONL event logs, JSON checkpoints/configs, Parquet or CSV analysis tables, and a manifest with checksums. |

## Non-functional requirements

| ID | Requirement | Concrete bound or test |
|---|---|---|
| NFR-01 | Reproducibility | Record source commits, model/tokenizer revision, weight hashes, package lock, CUDA/driver/backend, every seed, every rendered prompt, and unparsed output. Same CPU fixture reproduces byte-identical canonical events. GPU bitwise equality is not promised. |
| NFR-02 | Isolation | Evaluator inputs live in a separate process/directory contract; feasible policy types cannot accept OracleWorld. Canary tests fail if expected answers/support labels appear in prompts. |
| NFR-03 | Deterministic core | Generator, policy masks given supports, state reducer, and graders are pure functions of explicit inputs. No module-global RNG. |
| NFR-04 | Resource control | Agent call cap 256 generated tokens; extractor 512; context cap 4096 including output allowance; expected prompt means are measured, not assumed. One model replica per T4. |
| NFR-05 | Failure visibility | JSON/schema/timeout/semantic failure are distinct. All consumed tokens and attempts retained. No silent repair-by-retry. |
| NFR-06 | Checkpoint atomicity | Write temporary file, fsync, rename, then mark complete. Restart after injected crash must either see the previous complete state or the new complete state. |
| NFR-07 | Data scale | Maximum 10 roots, 32 minimal support sets, 12 active typed claims, 2 pending jobs, and 3 agents in the main study. Exceeding bounds is an explicit error. |
| NFR-08 | Auditability | Every final row resolves to branch→checkpoint→events→prompts→responses→source versions; every disposition records policy/reason. |
| NFR-09 | Portability | CPU reference runs with Python standard library plus Pydantic v2. GPU adapter is optional and separated. No paid API is required. |
| NFR-10 | Security/side effects | No real dispatch, payment, email, or external write; verbs mutate only branch-local sandbox state. |

## Acceptance milestones

**M0 semantics:** exhaustive finite oracle and recursive oracle agree; the alternative/bound counterexample is correct; changes to a control root do not alter target proofs.

**M1 runtime:** deterministic mock agents exercise every policy, checkpoint fork, stale version, invalid ID, duplicate execution, and crash boundary. Mock success is an engineering result, not an LLM result.

**M2 pilot:** capability, evidence delivery, parser, scope variation, token, and throughput gates in 12 pass. The novelty audit is resolved or the claim is narrowed in the registered protocol.

**M3 confirmation:** preregistered manifest, sealed analysis code, complete paired blocks, no post-outcome prompt changes.

**M4 thesis release:** all tables reconstruct from raw logs; null and failed branches included; software and benchmark transformations described; no placeholder result numbers.

## Traceability

RQ-01→FR-01/12/19→primary contrast. RQ-02→FR-08/13/16→exact/coarse/rebuild diagnostics. RQ-03→FR-04/16→pilot and single-agent controls. RQ-05→FR-16/NFR-02→oracle and leakage tests. RQ-06/09→FR-17/18/NFR-04→compute ledger. RQ-07→FR-02/11/17→manifest audit. RQ-10→03 and pilot Gate 0.
