# Implementation plan

**Authority:** [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md), final version dated 4 October 2026. Section references below refer to that document. This plan specifies engineering work and acceptance evidence; it does not change the experiment.

**Planning baseline:** repository commit `11979117fe868b825b98ac597085af5d9203509b`. The [README](../README.md), vendored source, and all four [implementation-research documents](implementation-research/SYNTHESIS.md) were inspected. The working tree was clean before this file was added.

**Implementation status:** M1 verified on CPU (M1-T01–T03 done; gate passed). The recovery package supplies task truth, prepared populations, complete schedules and replay dependencies. M2-T01–T03 verify permitted views/rendering, strict replies, synchronous scripted rounds and immutable drained prefixes; event/retention/replay/capacity and M3–M6 remain future work. No accepted inference environment, pilot or main results exist. See the [living handoff](#10-living-handoff) for current evidence; historical probes do not satisfy later gates.

## 1. Execution roadmap

Implement six capabilities in dependency order. Each milestone closes with reproducible evidence, updates the small living sections at the end, and leaves a usable handoff for the next session. Completion means its acceptance criteria passed, not merely that its files exist.

| Milestone | Capability delivered | Depends on | Admission gate |
|---|---|---|---|
| M1 | Reproducible worlds, independent truth, and complete schedules | Specification | Mathematical population, coordinate contracts, seeds, and schedule counts agree |
| M2 | Correct peer protocol and all interventions in a scripted execution | M1 | Visibility, matched requests, delivery, and actual tokenizer capacity pass |
| M3 | Durable execution, bounded failures, accounting, and progress | M2 | Process-crash/restart tests and complete scripted lifecycle pass |
| M4 | Validated offline analysis and reproducible reporting | M1–M3 | Synthetic estimands, diagnostics, missingness, and cost tests pass |
| M5 | Accepted inference configuration and frozen experimental run | M1–M4 | Bounded hardware/capability pilot and conservative complete-schedule forecast pass |
| M6 | Executed experiment and independently reproducible results | M5 freeze | Coverage, audit, artifact replay, analysis reproduction, and release checks pass |

**No GPU use before M1–M4 pass.** Tokenizer/config downloads and CPU validation are allowed earlier. Within M5, passing the smoke screen permits the first 90 capability slots; passing those capability thresholds permits the remaining recovery pilot. Only the accepted complete pilot, measured allocation forecast, and immutable freeze permit main inference. A gate failure produces a concrete diagnosis and the specified fallback or stop, never silent removal of a condition or unfavorable world.

## 2. Small implementation architecture

### Responsibilities and proposed layout

Use a small Python 3.11 package with direct functions and explicit records. LangGraph coordinates the fixed round barriers and local SQLite checkpoints; Transformers performs direct model calls. Four peers are four separately owned states, not autonomous framework agents or subgraphs. No LLM supervisor, general task-plugin system, remote service, semantic dependency graph, or runtime solver tool is needed.

The following is a guide to responsibilities, not a requirement to preserve every filename:

```text
pyproject.toml                 package, CPU dependencies, optional inference dependencies
environment.lock              complete passing package lock, finalized in M5
configs/study.toml             one study configuration; permitted size/model choices only
recovery/
  __main__.py                 thin CLI for validate, prepare, run/resume, status, analyze, export
  tasks.py                    specified generators, edits, exact solvers, coordinate contracts
  protocol.py                 strict reply schemas, parsing, permissions, public feedback
  state.py                    peer views, boundary transformations, synchronous deliveries
  prompts.py                  one renderer, task hints, notice/receipt layouts
  schedule.py                 saved seeds, populations, call dependencies, allocation/progress
  runner.py                   round graph and local worker coordination
  storage.py                  durable calls/attempts, snapshots, checkpoints, safe exports
  inference.py                text-only model loading and one independent generation call
  evaluate.py                 exact outcomes, coordinate/trajectory/information diagnostics
  analysis.py                 paired estimands, uncertainty, missingness, policy costs
  report.py                   tables, figures, frozen case selection, report assembly
tests/                        focused fixtures, independent references, integration/crash checks
runs/<run_id>/                frozen inputs/configuration, worker databases, exported results
docs/IMPLEMENTATION_PLAN.md   this living handoff
```

Keep `acl26-silo-bench/` and `research/` as reference material. Reuse mathematical definitions, selected stored fixtures, and attribution, not SILO's execution, parser, or generic scorer. Its generator imports seed global randomness; its runner stops submitted peers, mutates delivery history, and uses an unbounded retry adapter. Its package requires Python ≥3.13, so do not install it into the new Python 3.11 project. Extract small fixtures with provenance instead of importing archive scripts that overwrite evidence.

Use Pydantic 2 plus standard-library JSON/SQLite, NumPy/SciPy/pandas, Matplotlib, LangGraph and its SQLite saver; add PyTorch/Transformers/Accelerate/bitsandbytes for inference. Ordinary pytest/unit checks and deterministic randomized fixtures suffice. Avoid an additional service or dependency unless an acceptance check demonstrates a need. Research package versions are candidates, not an accepted lock. Keep CPU validation usable without importing or loading the model stack.

### State and information boundaries

These are logical records, not separate stores. Use the frozen run bundle and worker SQLite records/checkpoints as the sources of truth. Keep one authoritative record per generation, with its attempts and logical replay references; derive progress, exports, analysis tables and reports from those records. Reuse the required world/branch/call/message keys for relationships rather than adding an identity registry:

| Record/interface | Contents and ownership | Contract to verify |
|---|---|---|
| World/event manifest | Host-owned raw inputs, ownership/positions, edits, partitions, subset membership, saved streams and rejection counts | Immutable, serializable, independent of model outcomes; gold/footprints are separate evaluator records |
| Peer state | Permitted current source table, derived history, latest slot candidate/validity, public feedback, persistent notice/receipt | Replacement clears exactly the prescribed fields; no backend memory supplies additional state |
| Permitted peer view → rendered request | Public task/manifest/assignment and only that peer's allowed state | Renderer receives neither the full world nor evaluator/schedule labels; stable ordering and exact request/token preservation |
| Logical slot → physical generation or replay parent | World, event, policy, replicate, phase, round, peer; request/settings/seed and dependency identity | Required sharing is explicit; equal prompts or seeds never authorize additional cache reuse |
| Raw generation/attempt | Exact request, generated token IDs/raw text or durable failure, timing/device/memory, termination, attempts | Durable before effects; validation is a later deterministic operation |
| Branch checkpoint/delivery | Four peer states, phase/round, prefix parent, pre-delivery records, queues/cursors and applied message IDs | No mutable sharing across branches; one authoritative committed state |
| Offline outcome/export | Slot status, correctness and denominators, annotations, cost attribution, grouping/provenance IDs | Derived from the complete manifest and durable artifacts; never feeds correctness into execution |

Current sources render once outside history. A revision invalidates v1 everywhere; an unknown v2 remains an update-pending marker, and a delivered tombstone is known current evidence without an active edge. Source forwarding copies only a currently held ID/version, never an unseen host record. Notices and assigned receipts survive resets outside history. Historical receipt values are not current sources. Model-generated old values remain in retained derived history. IDs must not encode private values or BFS endpoints, including through endpoint-dependent ordering.

History retains permitted own replies, received prose, and bounded public validation feedback with phase/round labels, not past raw source-table renderings or resolved forwarding payloads. Render history as labeled data so a chat template cannot rewrite archived assistant text. Avoid duplicating the latest candidate when it is already represented in an own reply; preserve K's explicit historical candidate/absence. Do not shorten retained content to make a gate pass.

### Round execution, persistence, and worker ownership

The sole round procedure is:

**freeze all four views → render all requests → obtain/reuse all replies → validate → stage outgoing source/text effects → apply this branch's delivery rule → synchronously checkpoint → advance.**

Physical generation may be serial; no recipient observes a current-round reply before the barrier. Drain prefix-round-four deliveries before serializing the shared prefix. Every event/policy/replicate starts from a fresh deep-deserialization in a new checkpoint thread. Record boundary application in the branch checkpoint so restart cannot apply it twice. Use replacement state channels, not append reducers that can restore cleared history. The [LangGraph checkpointer documentation](https://docs.langchain.com/oss/python/langgraph/checkpointers) distinguishes checkpoint replay from reuse of external results; required response sharing belongs to the application ledger.

Use one local worker process and full model replica per T4, serial calls within each worker, and one SQLite file per worker. Rotate eligible sibling order/device assignment without violating B/C parent dependencies. Make saved prefix/reply records available to the assigned worker while preserving branch isolation and original physical generation IDs; reuse never adds physical generation cost. Keep local scheduling and record access simple, without requiring fixed worker affinity or a transfer service. Do not introduce a distributed queue or shared writable peer state.

Persist raw replies/failures in ordinary application-owned SQLite transactions before graph effects. Keep committed peer state, queues, and applied delivery IDs authoritative in checkpoints; derive delivery exports from committed transitions instead of maintaining a second independently authoritative effect store. Preserve the pre-delivery barrier required by mixed/Q replay. Use branch-scoped stable message IDs so an effect can occur once in each sibling and once only within a branch. Reconstruct an interrupted transition from saved replies without inference.

Verify synchronous checkpoint durability and actual SQLite settings in the execution environment. Do not use saver-private transaction helpers for application transactions. Archive databases after a clean checkpoint and close. The [state/replay investigation](implementation-research/state-and-replay.md) supplies useful failure fixtures, but the actual runner must pass M3. Use the specification's small-loop fallback only if this integration cannot preserve the required semantics; retain all identities, persistence, and tests if that change becomes necessary.

## 3. Milestone M1 — reproducible worlds, truth, and schedules

**Outcome and purpose.** The project can prepare the exact scientific population and enumerate every required opportunity without model inference. This prevents generator, denominator, and allocation mistakes from being discovered after costly execution. Covers §§2, 5.1, 8.2–8.3, and the task/seed/accounting parts of §9. No prerequisite beyond the specification.

Implement the five §2.1 generators and small exact solvers with explicit source/output-coordinate maps. Keep numeric ownership separate from positions and sorted output ranks. Implement the specified Prüfer-tree-plus-five-nonedges BFS distribution. Parameterize only the declared target and uniform fallback sizes: fallback BFS has eight nodes, twelve edges, three edges per peer; numeric `m=6` still returns top ten where applicable. Full-information Prefix/Sort contracts return all `n` coordinates.

Generate owner order in balanced blocks before eligibility conditioning; sample edits exactly as §2.2 requires. Main Top-K sampling is eligible-record then legal replacement; preserving Top-K sampling is uniform over legal record/replacement pairs. BFS chooses eligible edges for the fixed main owner, while preserving edits have no owner-matching constraint. Enforce both main and preserving eligibility for every Top-K/BFS world, the 1,000-attempt limit, and explicit rejection accounting. No model result may trigger regeneration.

Allocate separate saved streams for generation, edits, source/group partitions, prefixes, and continuations, keyed before execution. Continuation seed assignments match across policies/events for the same world/replicate/round/peer; physical generation identities remain distinct. Give the extra replicate new seeds/IDs while retaining its prefix and partition. Avoid scheduler order or Python process hashing in seed derivation. Save actual worlds/edits as well as seeds.

Prepare manifest generation for 60 worlds and its first-eight-per-family 40-world subset, five disjoint development worlds, all focal subsets, both complementary masks, and the ten fixed repeats. Assign G as the pair containing peer 0 from a uniformly chosen unordered two-pair partition. Main/preserving/sham events all refer to the original world. Final accepted-size manifests are frozen in M5 before main outcomes.

Enumerate logical slots and replay parents independently of execution. Encode the §2.3/§8.3 matrix directly: revised L/B/C/K/F and both masks; sham B/C/K and both masks; BΔ/CΔ/KΔ only on revised Prefix/Sort; Q_B/Q_C only on revised/sham Sort/BFS; preserving B/C/K on the fixed sixteen worlds; repeat B/C/K/masks under both events on ten worlds; two full-information controls per main world. No extra receipt, mask, Q, preserving, or repeat crossings.

| Schedule invariant | Target | Fallback |
|---|---:|---:|
| Main distinct generation slots | 16,152 | 11,504 |
| Main logical slots, shared uses included | 17,656 | 12,560 |
| Development pilot, distinct slots | 1,114 | 1,114 |
| Separate smoke maximum / capability-first pilot block | 24 / 90 | 24 / 90 |

**Acceptance evidence.** Independent test references agree with production solvers on selected native fixtures and generated cases; include duplicate cutoffs, discarded reserves, numeric endpoints/shard boundaries, sort rank crossings, BFS alternative paths/disconnection, and empty/nonempty changed-coordinate sets. Verify all output lengths/keys and both size configurations. Test legal-set sampling and owner/subset construction directly rather than relying on a flaky frequency threshold. Force exhausted rejection and confirm explicit failure. Regeneration from saved inputs is byte-stable. Independently enumerate every schedule component and reconcile §8.3 totals and `730+96+96+96+96=1,114` pilot generations. Manifest edits after serialization are detected.

**Remains later.** A correct mathematical schedule is not a runnable protocol or a feasible allocation. M2 validates its peer-visible execution; M5 chooses the accepted size/model and 60/40 allocation.

## 4. Milestone M2 — lawful protocol and matched interventions

**Outcome and purpose.** A deterministic, in-memory runner executes every branch through the real schemas, renderer, and delivery rules using scripted replies. This establishes experimental semantics independently of model competence. Depends on M1; covers §§3–4, the §8.2 witness, and visibility/state/synchrony checks in §9.

Implement complete-document JSON decoding before strict Pydantic validation. Reject duplicate keys recursively, nonfinite constants and overflow/coercion paths, booleans/floats/strings as integers, undeclared nested fields, invalid shapes, noncanonical BFS keys, code fences, trailing prose, and fragments. [Python JSON defaults](https://docs.python.org/3.11/library/json.html#standard-compliance-and-interoperability) require explicit duplicate/nonfinite rejection. Then check recipient uniqueness/permissions, held current references, at most eight **distinct** references per recipient, and actual tokenizer caps. Repeated valid references are not independently forbidden by the distinct-reference limit; retain delivery attempts separately from unique acquisitions. Any violation invalidates the entire reply and all its messages. A numerically wrong candidate with valid structure remains protocol-valid.

Enforce 384 generated tokens, three recipients, 128 prose tokens summed across the reply, and 32 feedback tokens per slot. Feedback reports only public schema/permission errors at the next scheduled call, without library error dumps, hidden payloads, correctness, or an extra opportunity. A complete valid JSON reply at the generation cap is valid; malformed/truncated replies and failed slots have no new candidate and never inherit an earlier answer. All four peers receive all four opportunities in each phase. Prompts request only the candidate/send reply, with one generic authority instruction and the same short task hint across conditions; do not impose a leader/route or request a separate proof or chain-of-thought.

Implement event and retention transformations as deterministic functions returning new state. Keep explicit, small policy cases instead of a generalized intervention language. Use the following differential checks as the behavioral contract:

| Boundary/comparison | Required fixture evidence |
|---|---|
| All sibling starts | Prefix messages are drained; originals and siblings stay unchanged under nested mutations; all starts use the original prefix, including preserving edits and repeats |
| Sham | Sources remain unchanged; all peers receive the same neutral continue-solving notice; apply B/C/K/mask retention without inventing a source revision |
| L/B | Both invalidate v1 and publish the same notice; only replacement-content recipients differ; BFS endpoints remain hidden from unexposed L peers |
| B/C/K/masks | Per-peer initial current sources are identical; C clears history/candidate/feedback; K keeps exactly its own valid fourth-prefix candidate, including wrong candidates, or absence after invalid round four |
| C/F | Same empty derived state and broadcast revision; only retained acquired remote evidence differs; F still has its corrected private shard |
| Receipts | BΔ/CΔ/KΔ preserve corresponding evidence/retention; only genuine archived before-value disclosure changes; ordinary receipt says it is not included, not unavailable everywhere |
| Mixed round one | Each peer's rendered request, settings, seed and permitted view equal its B or C parent; exact durable replies/failures are selected before assembling branch-local outgoing effects |
| Q round one/two | Replay the exact parent replies; sources and own reply before round two match the parent; source-delivery metadata stays identical; only received prose is held, with no text-only placeholder or other leak |
| Q release | Before round three, append round-one held prose before round-two prose, ordered by generation round/sender, preserving stable IDs and already-seen history order; then ordinary delivery |

After the boundary, every policy accumulates ordinary new history; K is not continuous compression. Receipts must not provide a delta, formula, output footprint, corrected candidate, or extra unchanged source. Keep all prompts free of policy/branch/reset-mask/subset identifiers, future edits, gold, and anticipated effects. Test using distinct sentinel hidden values and paired worlds: changing a hidden field cannot change the corresponding permitted rendering. Include schema feedback and source-delivery metadata in this audit. CPU v1→v2→v3 tests cover version handling only; no live second revision is added.

Build the actual attainability witness: each peer forwards its own currently held shard to a different peer in each of the first three rounds and computes only from its acquired local view once sufficient records are available. Use legal placeholder candidates earlier. Exercise all families, event deliveries, reset policies, and prose delay through the real interface. The scripted solver must not receive host gold or unseen records. Prove revised correctness is attainable within the four recovery rounds, including local replacement forwarding and F's reacquisition.

Run tokenizer-only validation on the actual request template and reply serialization. Verify every candidate/control shape and useful one-shard messages fit; reserve the full 384 output tokens inside the 8,192 total. Bound retained history across the full prefix and recovery horizon, including invalid own replies, maximum received prose, feedback, labels, current tables, notices/receipts, source-delivery metadata, unusual escaping, and wrong integers. Use an accounting bound plus adversarial rendered fixtures, not only ordinary/correct outputs or the research's illustrative context. Q release must not duplicate history. Stress template special-looking strings and lossless archive preservation.

**Acceptance evidence.** All differential checks above pass; reversed physical peer order yields identical scripted states; a valid candidate plus one invalid message yields no effects; stale/unheld references reveal nothing. The locally informed witness succeeds with legal tokenized traffic. The complete renderer capacity argument and fixtures fit both accepted contracts and all relevant policies. A gap in the worst-context argument remains a failed gate. Compact lossless representation and the specified uniform size fallback may resolve it; if neither does, stop and document the incompatibility for an explicit specification-level decision. Never silently truncate or invent another fallback.

**Remains later.** These are deterministic implementation results, not evidence of LLM recovery. Durable restart, model decoding behavior, hardware, and capability remain M3/M5 work.

## 5. Milestone M3 — durable runner, failures, cost, and progress

**Outcome and purpose.** The same scripted experiment runs through real checkpoints and worker coordination, survives interruption, and explains its remaining work and resource use. Depends on M2; covers §§6, 7.3, 8.3–8.4, and persistence/replay/accounting requirements in §9.

Wire the validated round procedure into the small LangGraph/SQLite runner. Store exact requests and pre-delivery parent replies, not just final states. Mixed/Q replay verifies equality before reuse and never imports the parent's post-delivery recipient table. Replay parents are scoped by event and continuation replicate. A mismatch stops as a protocol defect. Resuming any completed call ID returns its exact durable response or failure, including invalid results. Do not deduplicate unrelated calls merely because requests happen to match.

Represent slot status explicitly: pending/unexecuted, running attempt, durably completed reply, recorded timeout, exhausted infrastructure failure, or logical replay of a parent. Parsing/correctness are separate attributes. Before starting generation, persist an attempt record; after receiving it, persist raw output before effects. Permit at most one identical-request retry only for an infrastructure interruption without a durable response. Wrong answers, invalid formatting, truncation, and completed timeouts never trigger retries. A crash after possible inference but before persistence is recorded as an uncertain completed attempt, not exactly-once generation.

Start development with a 120-second attempt timeout. Enforce the attempt timeout, terminating a hung GPU attempt and persisting its known timeout without blocking status indefinitely. A restarted worker reloads its model and state; loading, idle allocation and lost/ambiguous work remain charged. Test timeout and interruption separately. Context overflow fails visibly before generation and stops for diagnosis as a capacity/protocol defect; it must not be hidden as truncation or a favorable missing-row exclusion.

Join every logical slot to its generation/replay parent and every generation to attempts. Keep physical accounting (one charge per actual generation/attempt) separate from hypothetical policy cost (prefix plus all sixteen continuation calls, including original measured costs for replays and F's abandoned prefix). Record token counts, call/attempt durations, validated source/text deliveries, peak memory, device allocation intervals and idle/setup/interruption overhead. Freeze an explicit overhead attribution rule and reconcile it without charging the same overhead twice. Provider billing and aggregate physical allocation are separate records.

Expose a terminal status view and a read-only `status` operation derived from manifests/ledgers. Report at call and round transitions and with a bounded heartbeat during long calls:

- Current stage, family/world, branch/replicate, round/peer and device; elapsed attempt time and last durable checkpoint.
- Scheduled/finished/remaining logical slots, distinct generations, replay uses, attempts and retries; failures separate from unknown slots.
- Completed worlds and complete matched comparison groups by family/event/subset; ready versus dependency-waiting branches.
- Actual allocated GPU-hours including idle devices, remaining ceiling/reserves, and a conservative remaining-cost/elapsed-time range from measured phase/condition work and device speed. Mark estimates unavailable until measured; do not present slot percentage as runtime percentage.
- Current gate/stop reason and the exact resumable work. A completed invalid slot counts as work finished, not as a success or a new opportunity.

Progress counters must reconstruct after restart without a second mutable progress database. Store only necessary allocation/attempt transitions beyond the existing scientific records. Check budget before admitting work using active devices, timeout/termination allowance, remaining overhead and forecast; stop allocation safely before the frozen ceiling. Success, silence, or early joint correctness never removes scheduled work.

**Acceptance evidence.** Kill and restart a real test subprocess before response commit, after durable reply, during validation/staging, and before/after delivery checkpoint. Verify unchanged completed outputs, at most two allowed infrastructure attempts, no timeout/invalid resampling, no duplicated deliveries, no restored cleared fields, exact mixed/Q reuse, and unchanged parent/sibling snapshots. Include cross-worker parent transfer and a Q crash with held prose. Compare uninterrupted and resumed committed states/deliveries/outcomes and reconcile expected differences only in physical attempt/allocation records. Reopen database backups and reconstruct progress. A tiny scripted run covers every family/intervention/repeat path; full manifests reconcile without doing all model calls. Synthetic budget exhaustion leaves explicit unexecuted slots and stops safely.

**Remains later.** Measured model timing and allocation forecasts are unavailable until M5. M4 must prove that these artifacts support every intended analysis before any GPU spending.

## 6. Milestone M4 — offline analysis and report reproduction

**Outcome and purpose.** The project can turn complete or incomplete recorded runs into the prescribed outcomes, uncertainty, diagnostics, costs, and exhibits without model calls. Depends on M1–M3; covers §§5–7 and the analysis/release checks in §9. This milestone detects missing data fields while they are still inexpensive to add.

### Exact outcomes and contrasts

Join the full slot manifest to raw/validated replies before scoring. Preserve list order/multiplicity and the complete BFS key set. Recorded invalid/failed outcomes score zero; unexecuted outcomes remain unknown. Compute exact-peer recovery AUC over all sixteen opportunities and final all-four correctness; the reset boundary is not an extra failed round. Gold is event-specific and evaluator-only.

Implement the formulas in §§5.2–5.4 directly with independently calculated synthetic expectations:

- θ and both revised/sham C−B components, with equal five-family weighting.
- φ as the revised retained-collaborator effect, using the same focal peers over rounds 2–4; report sham E_keep, φ_corr, both E_clear effects, own-group reset contrasts, four-mask trajectories, and average mixed-policy performance. Round one is a construction reference.
- Every secondary §5.4 comparison: revised retention/delivery/evidence effects and compact-state sham/interactions; receipt η at round one with all six cell means, all direct receipt effects and representation comparisons; Q effects at round two separately by event; preserving B/C/K endpoints. Supply the specified AUC/final/preservation/trajectory companions on the correct eligible populations.

Keep replicate zero primary. For the ten repeated prefixes, show paired θ/φ/compact-state contrasts, ties/sign reversals and trajectory-category changes. Do not replace outcomes, average repeats into new worlds, or claim new-prefix or receipt/Q repeatability.

### Uncertainty and incomplete execution

Implement 10,000 world-cluster bootstrap draws within each eligible family, at its observed population size, keeping all siblings/groups/peers/rounds/repeats together. Save the resampling seed and quantile convention. Use 1.25/98.75 percentiles for both primary intervals and 2.5/97.5 for descriptive secondary intervals. Analyze fixed subsets within their own populations and preserve shared world identities in overlapping displays. Show raw world contrasts and family means, not only pooled intervals. Do not inherit statistical-library bootstrap defaults.

When contrasts are constant within families, add the §6 weighted Hoeffding interval with weights `1/(F*n_f)` and the appropriate contrast range: θ in [−2,2], φ/direct differences in [−1,1], secondary interactions according to their formulas. Include eligible-family completion counts and appropriate exact binomial bounds for all-success/all-failure cases. Treat 0.10 and the specified power calculations as reporting references, not equivalence claims or achieved sensitivity.

For missingness, publish scheduled/executed counts and paired coverage. Bound unknown correctness in [0,1] through each estimand. For linear contrasts, combine coefficients of a shared response identity before choosing its lower/upper completion; logical copies cannot vary independently. For nonlinear completion/trajectory summaries, retain shared variables and derive conservative labeled bounds, using tiny enumerated fixtures as an independent check. No general optimizer is needed. Incomplete trajectories remain separate; complete-case displays cannot stand in for the frozen population.

### Explanatory outcomes and costs

Implement §7's diagnostics with explicit eligibility and provenance, rather than inferring causes from prose:

| Output | Required distinctions |
|---|---|
| Repair/preservation | Evaluator-only D/U on unique coordinates; new correctness and explicit old-gold persistence on D; preservation/collateral damage only on U coordinates correctly answered by that same peer in valid prefix round four; beneficial repairs of old U errors separate |
| Denominators | Invalid answers count as incorrect for accuracy/preservation but have a separate malformed/missing category for old-value persistence; empty denominators are N/A; average eligible peers → worlds → equal eligible families; publish unique-coordinate and peer-copy counts |
| Trajectories | First joint and first maintained joint correctness, regression, four complete-branch categories, and fragmentation; no best-answer splicing, successful-only recovery-time average, or invented fifth-round failure time; identical-but-wrong agreement only for replicated-output tasks |
| Annotations | Six nonexclusive §7.1 labels with counts/intersections: protocol/inference failure, v2 unavailable, incorrect after v2, explicit old-value persistence, collateral error, regression |
| Prefix and delivery | All four prefix rounds' correctness, remote coverage, history tokens and communication; owner-v1 rendered exposure; L/B first usable v2 boundary and host/forwarded origin, including no receipt, no success, same-call/later success and correctness before receipt, with censored cases retained |
| Evidence/work inventory | C/F boundary remote current records excluding host-injected revision, unique new ID/version acquisitions versus all delivery attempts; tombstones known, pending replacements unknown; post-intervention acquisition remains an outcome |
| Receipt information | Source-bound old-value visibility, reconstructibility under stated correct-candidate assumptions, sufficient current raw evidence, and unresolved cases; numeric occurrence is not source association; offline correctness strata include denominators |
| Deterministic references | §7.2 information atlas/selected CPU counterexamples, including CPU-only Max; actual valid old-candidate Prefix/Difference delta transport even when wrong, preserving the residual-error identity; no candidate backfill or runtime repair |
| Edit descriptors | Position/direction/magnitude, affected output owners, Sort segment crossings, BFS disconnection; descriptive tables/limited plots without a moderator search |

Keep any inspected source-bound prose annotation small, conservative and linked to exact archived evidence; freeze its rubric before main analysis, and label unresolved associations. Do not build a semantic dependency/exposure system or use an LLM judge. Synthetic wrong-candidate examples must prevent correct-summary mathematics being mistaken for evidence that actual candidates are correct.

Produce separate retained-evidence, preserved-output, and measured-computation tables. Plot paired quality/preservation against policy-accounted cost with uncertainty; do not create an arbitrary utility ratio. Retrospective oracle-recognized stable-completion cost is not saved runtime under the fixed schedule.

Implement the frozen descriptive boundary rule using initial current-source coverage: choose the complete C branch iff all peers hold the complete current record manifest, otherwise the complete K branch. Include tombstones and exclude pending replacements. Use neither gold nor candidate correctness, and never splice branches. Compare with always B/C/K, report selection frequencies, and state when the rule is constant.

### Report and acceptance evidence

Build roughly seven or eight grouped exhibits following §7.4: task/prior-work context; recovery-policy effects; repair/preservation; representation/receipts; collaborator effects; prose timing/synchronization; and quality/cost with repeatability/limitations. Supporting family/world tables and raw traces carry detail. Implement the exact case rule now: median strictly positive/negative complete world for corrected C−B AUC, E_keep(revision), and KΔ−K round-one accuracy, sorted by effect then immutable ID using the lower observed median; merge duplicate worlds and report absent signs. When all contrasts are zero, use the smallest-ID regression world, or the smallest complete world if no regression exists. Without an eligible complete world, report cases unavailable. At most six cards use unaltered excerpts linked to call/message IDs.

**Acceptance evidence.** Hand-checked synthetic fixtures establish θ's equal-effect null and signs; φ's no-influence null and beneficial/harmful signs; φ positive with φ_corr zero when effects match across events; round-one exclusion; equal-family weighting; replicate separation; and every secondary contrast. Test constant-within-family bootstrap degeneracy, interval ranges, empty denominators, malformed persistence categories, fragmentation, preservation damage versus old-error repair, and shared-identity missingness cancellation. Test a constant boundary rule and tied/empty case selections. Reconcile physical/policy costs on replayed and failed calls. Produce the complete report from the M3 scripted run twice with identical tables/case IDs and deterministic plotting inputs, without importing inference. Synthetic exhibits must be labeled as validation, never empirical findings.

**Remains later.** No effect size, capability, GPU speed, or recovery advantage has been established. M5 admits a configuration; M6 supplies empirical evidence.

## 7. Milestone M5 — accepted inference and pre-main freeze

**Outcome and purpose.** One model/environment/size passes the bounded operational pilot and can conservatively execute a complete allowed schedule. Depends on M1–M4; covers §8 and inference/environment consistency in §9. All activity in this milestone remains development, with disjoint worlds and explicit cost.

### Runtime/environment validation

Start with Qwen3.5-9B and the maintained Transformers text-only loading path. Verify the actual language-weight inventory/loading diagnostics, including tied-weight handling; expected unused vision weights do not excuse missing/newly initialized language weights. Use no multimodal wrapper conversion, remote serving stack, alternative quantizer, or custom kernel. The [inference investigation](implementation-research/inference-and-capacity.md) identifies concrete template, termination, and loading risks to test.

Configure NF4/double quantization and FP16 computation explicitly, preserving supported FP32 sensitive calculations. These are distinct settings in [Transformers' bitsandbytes interface](https://huggingface.co/docs/transformers/quantization/bitsandbytes); the passing configuration, not a package default, is frozen. Batch size is one; each worker owns one entire replica on one T4, with no CPU offload or cross-device split. Record CUDA/driver/package versions, actual device map and attention/recurrent paths, allocated/reserved/peak memory, and finite-output checks. Require at least 1.5 GiB free headroom at the accepted worst prompt.

Freeze the specified non-thinking settings (`enable_thinking=False`): temperature 0.7, top_p 0.8, top_k 20, min_p 0, repetition penalty 1.0 and no presence penalty. Audit the actual chat template, EOS/PAD IDs and terminal framing. Save generated IDs and decode only the generated suffix without cleanup that can erase invalid markers. Remove only verified terminal transport framing for parsing; do not strip arbitrary special tokens, repair JSON, impose schema-constrained generation or stop at a closing brace. Verify full valid output at the cap remains accepted.

Fresh KV/recurrent state and saved per-call RNG assignment are mandatory. Set worker device visibility before CUDA initialization and seed each serial call without concurrent process-global RNG mutation. Instrument cache creation/disposal, perturb prior call/order/resume in controlled checks, and rerun state/checkpoint tests on the accepted GPU host. Save nondeterminism/device limitations rather than promising bitwise regeneration from seeds; exact matched response reuse still comes from archived parents. Any inference calls used for these checks count against development limits.

### Bounded smoke and capability pilot

1. **Smoke:** at most 24 calls or 0.5 aggregate GPU-hour, whichever comes first. Cover worst prompts, output shapes, forwarding, a corrected continuation, finite outputs, raw decoding, timeout handling and memory. Record failures and load/setup costs. Metadata or weight fit alone cannot pass.
2. **First 90 pilot slots:** five full four-round prefixes (80) and before/after full-information controls (10), using the same outer reply schema with empty sends, same hint/decoding/caps, and full-world output lengths. Require at least 9/10 correct controls, at least one per family, at least three jointly correct final prefixes and 14/20 correct final prefix-peer candidates before recovery spending.
3. **Remaining pilot:** execute the exact §8.2 components to reach 1,114 distinct slots, reusing mask/Q first rounds. Require at least 98% protocol-valid distinct scheduled pilot generations for the accepted configuration, with no unresolved isolation/leakage/queue defect and passing capacity/memory checks. Inspect family/condition failures as well as the pooled rate. Replay uses and retries cannot inflate the validity denominator.
4. **Forecast:** measure phase/condition/prompt-dependent time, the slower device, loading and allocated idle overhead. Test 120-second timeout adequacy before freezing it. Require a conservative forecast for the whole schedule, not extrapolation from short successful calls.

Use the shared eight-hour development allocation for failed configurations, attempts and justified reruns, plus the specified two-hour setup and two-hour interruption/rerun reserves within the 100-hour total. The full 1,138 smoke-plus-pilot allowance is not permission to exceed a time limit. Keep measured spending separate from reserved amounts. A changed model, tokenizer/template, package lock, backend or timeout reopens all affected earlier gates; do not pool incompatible configurations into an admission result.

Use only the specified remedies. If arithmetic/context capability requires it, apply the single uniform `m=6`/eight-node-twelve-edge fallback and repeat all affected generator, oracle, renderer, witness and capability checks. If 9B fails hardware/runtime gates, test 4B within the same development budget. Do not choose prompts/models by favorable recovery effects or mix accepted configurations across conditions. Prefer capable 9B/40 to switching models only for more worlds. If no accepted configuration passes, stop before main inference and publish the feasibility evidence.

### Freeze and admission to main execution

Use the full twelve-hour reserve and a 25% margin on measured main cost, without double-counting setup in per-call timing. Include device idle allocation and provider billing rules separately. Select 60 worlds if its complete schedule fits, otherwise the nested complete 40. If neither fits, stop for an explicit scope/resource decision; do not remove shams, pairs, repeats, or families. Two GPUs can shorten elapsed time, not halve aggregate device-hours.

Create an immutable run bundle containing specification/code identities; accepted package/environment lock and system facts; model/tokenizer revisions and actual templates; size, schemas, caps, timeout and decoding; actual worlds/edits/ownership/partitions/subsets/seeds; complete logical/physical/replay schedule; estimands/analysis settings and annotation/case rules; measured pilot evidence, allocation convention, ceiling and forecast. Reject resume settings or inputs that differ from the persisted run bundle. Update README run/reproduction instructions during implementation, not by adding another planning-document hierarchy.

**Acceptance evidence.** An admission report links each threshold to actual pilot rows, verifies strict schedules/counts and all passing host checks, and reconciles spent/reserved/forecast allocation. An independent dry-run freeze audit rejects missing parents, inconsistent seeds, changed templates, mixed models, and incomplete selected schedules. No main outcomes are inspected before this freeze.

**Remains later.** A passed pilot is a feasibility/capability screen, not a treatment-effect estimate or a guarantee the full run will finish. M6 remains necessary even if pilot recovery looks favorable.

## 8. Milestone M6 — complete execution, audit, and reproducible results

**Outcome and purpose.** The frozen study is executed and every empirical statement can be traced to reproducible artifacts. Depends on M5; completes §§1, 6–10.

Run balanced task/world blocks, rotating eligible sibling order/device assignments subject to first-round replay dependencies. Use exactly one natural prefix per world, all four prefix rounds, and all scheduled continuation rounds. Verify owner-v1 rendered exposure and drained prefix snapshots before branching. Include failed prefixes, silent peers, redundant receipts, harmful policies and inactive Q treatments. Execute controls and fixed repeats according to the manifest, never using their main outcomes as treatment selectors.

Monitor the M3 status and conservative remaining allocation throughout. Pause/terminate safely before the frozen ceiling when necessary; preserve durable responses and mark unexecuted slots unknown. Resume within the same frozen design and available resource limit. If completion is impossible, publish the original schedule's coverage and sensitivity bounds. Do not convert the observed remainder into a new sample-size target or favorable exclusion set.

For an independently verified generator/protocol/leakage/evaluator defect, record affected artifact IDs and the reason in the deviation section. Fix it and invalidate/rerun the full affected dependency set: all affected matched branches, and a new prefix plus its descendants if the prefix itself was defective. Charge every attempt, preserve superseded artifacts, and disclose the impact. Pure analysis defects can be repaired from unchanged raw calls; never regenerate unfavorable replies to improve results. Changes needing a specification-level decision remain explicit, not hidden inside configuration edits.

After execution, audit manifest joins, attempts, source visibility/versioning, boundary transforms, exact mixed/Q requests and parents, Q release ordering, denominators, seeds/repeats, environment identities and physical/logical costs. Recompute gold independently and replay delivery/evaluation from archived inputs/replies without inference; compare committed checkpoints and exported tables. Missing data, inconsistent records and duplicated IDs fail the audit rather than disappearing from analysis.

Generate the prescribed report and supporting outputs using M4. Show all focal populations, family/world contrasts, uncertainty, coverage, inactive treatments, repeatability and capability limitations. Keep package-effect interpretations, observed communication paths, mathematical sufficiency and semantic causation distinct. Equal event effects, subgroup cancellation, ceiling performance, poor capability, broad intervals, negative and inconclusive results must remain interpretable. Describe results as SILO-derived revision tasks with the §10 limits; verify precise cited source/version claims before publication and preserve attribution. Do not claim a recovery advantage from implementation tests or a native SILO reproduction from these modified tasks.

**Release contents and final verification.** Publish the accepted lock/configuration/system manifest, exact prompts/templates, worlds/edits/seeds/schedule, immutable prefixes/branch states, raw calls/attempts/deliveries, pilot/allocation/coverage reports, tidy outcome/cost/annotation tables, analysis code, figures and report. Keep one canonical run bundle; exports are reproducible views, not competing truth stores. Document clean installation, CPU validation, frozen execution/resume/status, and offline analysis/export commands. A clean environment must reproduce tables, selected cases and plotting inputs from the bundle without GPU calls. Full stochastic rerunning is separately documented with its environment/device limits and is not promised to reproduce every token.

**Completion criterion.** The intended complete experiment is done only when the frozen schedule is complete and release checks pass. A failed feasibility gate or resource-truncated run instead closes with an explicitly limited outcome, its evidence, and outstanding work; it must not be labeled a completed empirical study.

## 9. Coverage map

This map is the implementation completeness check. At each milestone close, link the relevant tests or run evidence from the progress table; retain the specification's section structure rather than assigning a second system of requirement IDs.

| Specification | Implementation destination | Verification destination |
|---|---|---|
| §1 research design/estimands | M1 schedule; M4 estimands; M6 interpretation | Matrix enumeration, primary synthetic fixtures, final claims audit |
| §2.1 tasks/distributions | M1 generators/oracles/coordinate contracts | Independent native/adversarial references, both sizes |
| §2.2 sampling/reproducibility | M1 streams/eligibility/owner blocks; M3 identities; M5 freeze | Rejection/sampling tests, manifest replay, exposure and provenance audit |
| §2.3 events/populations | M1 subset/branch manifests; M2 sibling starts | Original-prefix and subset assertions, exact schedule counts |
| §3.1 visibility | M2 views/renderer/source authority; M3 archives | Hidden-field differential tests, source/receipt/tombstone checks |
| §3.2 protocol/rounds/caps | M2 parser/barriers/witness; M5 decode | Strict parser adversaries, token bounds, synchrony and cap-end fixtures |
| §4.1 retention/delivery | M2 transformations | Initial evidence equality, C/F contrast, K wrong/invalid candidate fixtures |
| §4.2 complementary groups | M1 partitions; M2/M3 exact mixed replay | Focal-peer/mask tests, equality and branch-local delivery/crash tests |
| §4.3 historical receipts | M2 receipt interface; M4 receipt endpoints/annotations | Disclosure-only view tests, η/six-cell fixtures and actual token cost |
| §4.4 prose delay | M2/M3 queue/replay; M4 Q outcomes | Round-two equality, no-leak/release/resume tests, inactive-treatment counts |
| §5.1 exact outcomes | M1 truth; M4 evaluator | Ordered/duplicate-aware scoring, full keys, failed versus unknown slots |
| §§5.2–5.4 all contrasts | M4 analysis | Independent signs/nulls, populations, companions and endpoint checks |
| §6 statistics/repeats/missingness | M1 repeats; M3 statuses; M4 uncertainty; M6 deviations | Cluster/stratification tests, degeneracy/bounds, shared identities, coverage |
| §7.1 repair/preservation/trajectories | M4 diagnostics | Eligibility/empty denominators, fragmentation/regression/annotation fixtures |
| §7.2 information/work | M2 delivery metadata; M4 inventories/references | Receipt timing/censoring, residual identities, stated-view counterexamples |
| §7.3 quality/cost/boundary rule | M3 ledgers; M4 policy analysis | Physical/logical reconciliation, full-branch selection, uncertainty |
| §7.4 narrative/cases | M4 report logic; M6 actual report | Frozen case selection, excerpt provenance, unfavorable-outcome interpretation |
| §8.1 inference/controls | M1 control contracts; M5 backend/environment | Language weights, fresh state/RNG, decoding, devices, memory/finite outputs |
| §8.2 CPU/pilot/fallback | M1–M4 gates; M5 bounded pilot | Witness/token proof, 24/90/1,114 counts, all numerical admission thresholds |
| §§8.3–8.4 schedule/resources/freeze | M1 enumeration; M3 progress; M5/M6 allocation | Both exact totals, full-reserve forecast, ceiling stop, immutable freeze |
| §9 implementation/consistency/publication | M1–M6 | Seven essential check categories, process crashes, offline clean reproduction |
| §10 attribution/limits/exclusions | M1 reuse boundary; M4/M6 report | No extra live arms/tools/models; source/version and claim audit |

## 10. Living handoff

Update these sections only when a capability is verified, a consequential decision changes, a defect alters remaining work, or a gate becomes blocked. Keep detailed execution evidence in the run bundle, not a diary here. Future sessions should read the relevant specification sections, this plan and linked milestone evidence before continuing.

### Progress

| Milestone | Status | Evidence / next action |
|---|---|---|
| M1 | Verified on CPU (3/3 tasks done; gate passed) | [M1-T01 evidence](todos/M1/M1-T01-task-worlds-and-truth.md#validation-and-evidence), [M1-T02 evidence](todos/M1/M1-T02-edits-and-populations.md#validation-and-evidence), and [M1-T03 gate tables](todos/M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate): 59 checks pass on Windows / Python 3.11.9 with site packages disabled and installed outside checkout. Task truth, eligible populations/streams and both complete schedules pass: 16,152/17,656 and 11,504/12,560 distinct/logical main slots; exact 1,114 distinct development slots with first 90 capability calls. Retained inputs/schedule and saved authority/mutation checks pass. |
| M2 | Partially verified on CPU (3/6 tasks done) | [M2-T03 completion](todos/M2/M2-T03-synchronous-rounds-and-prefixes.md#completion-and-handoff): 121 source/installed CPU checks (80 core + 23 strict reply + 18 round/prefix), three native round checks with an exact eight-round trace and all 11 previous native checks. Complete sibling isolation, round-four drain, actual owner-v1 exposure, order independence and attempt/acquisition metadata pass. [M2-T04](todos/M2/M2-T04-events-retention-and-receipts.md) is ready. Literal events/retention/receipts, exact mixed/Q replay, local-view witness and capacity admission remain; M2's gate is open. |
| M3 | Not started | Requires M2 |
| M4 | Not started | Requires M1–M3 |
| M5 | Not started | Requires passing M1–M4; no hardware/capability result exists |
| M6 | Not started | Requires accepted M5 freeze |

### Implementation decisions

| Decision | Reason / reconsideration evidence |
|---|---|
| New shallow package; vendor/archive remain references | Native execution/scoring conflict with the required protocol; do not inherit obsolete architecture |
| M1 task core uses frozen standard-library records and caller-owned generation/ownership RNGs | No numerical, graph or inference dependency is needed for these exact computations. Public candidate contracts/source manifests are separate from offline truth; BFS IDs bind only after edge shuffling and tombstones retain endpoints. |
| M1-T02 legal edit sets precede sampling; events take only original v1 worlds | Main selection uses record then replacement, preserving uses a single pair draw without owner matching. Top-K preserving originals are strictly below the cutoff; cutoff-equal replacements preserve the ten-value multiset. Deterministic checks cover both sizes, independent BFS deletion truth and the exact 1,000-attempt ceiling. |
| Prepared populations use one canonical JSON record and fixed integer seed slots | Saved actual worlds/edits are authoritative; gold and footprints remain evaluator-side. Stable world slots/configuration give disjoint local stream seeds, with event/policy absent from continuation seeds. Nested 40-world/focal populations derive from the saved 60; loading never regenerates. Exact baseline comparison detects changed valid inputs; no checksum/identity registry is added. Both-size fixtures and CPU CLI are verified; the M5 accepted freeze remains future work. |
| M1-T03 schedules use existing world/branch/call keys and explicit prefix/raw-reply parents | Independent component/cell checks reconcile both complete main totals and the exact development matrix. Equal seeds create distinct generations unless a prescribed first-round B/C parent exists. The nested 40 is a view of the 60-world schedule; smoke is separate and the first 90 pilot slots are prefix/controls. Saved schedules are derived artifacts checked against the population, without copied raw worlds or another identity system. Save/reload, mutations, dependency orders and CPU prepare/validate pass in the 59-check suite; runtime equality/delivery remain M2/M3. |
| LangGraph barriers plus local SQLite and explicit raw-call ledger | Meets §9's starting choice; replace with the permitted small loop only for a demonstrated unresolved semantic incompatibility in M3 |
| Explicit narrow peer views and pure state/delivery transformations | Makes scientific visibility, replacement and replay inspectable and CPU-testable |
| M2-T01 uses immutable permitted records and a single user-data renderer | Initial projection/held-source lookup take no evaluator or schedule labels. Current/pending/deleted sources, receipt history, derived text, feedback and latest-slot absence are distinct; public identity alone orders sources. Candidate state cannot precede recorded own/feedback slots. Native non-thinking template text and untruncated token inputs are ordinary saveable records. Fixed public feedback prevents hidden library-error payloads; complete capacity and event/round transformations remain later M2 tasks. |
| M2-T02 uses complete JSON decoding, strict Pydantic 2 and whole-reply staging | Pydantic 2 is now a declared CPU dependency. Full validation includes the strict-reply suite; explicit `--core-only` retains dependency-free checks without claiming protocol admission. Generated IDs govern the 384-token cap; literal message texts are tokenized separately and summed. Source staging resolves only immutable sender-held records and preserves repeated attempts. Fixed public feedback has an actual tokenizer guard; invalid/failed outcomes replace candidates with absence. No delivery, correctness check, response repair or extra call is introduced. |
| M2-T03 separates pure request, validation, staging and delivery barriers | The in-memory procedure uses the existing views/renderer/validator and call-key spelling; M3 still owns LangGraph/SQLite integration. Source/text component IDs preserve repeated attempts and branch-local idempotence. First-acquisition metadata remains public; full attempts/IDs/queues remain offline. Plain JSON deep-deserialization supplies drained immutable prefixes without another store. Final recovery deliveries are audited at an unscheduled next-round boundary, without a fifth opportunity. Eighteen focused checks, the 121-check source/installed suites and three native round checks pass; the existing 11 native checks still pass. |
| One serial process/replica/database per GPU; access to saved inputs | Keeps inference/RNG isolated while permitting sibling/device rotation |
| M2-T04 uses explicit boundary cases, saved schedule identities and persistent notices | Every start deep-deserializes the original prefix and checks original sources/fourth-slot outcomes. The existing schedule enumeration governs subsets/repeats; no second eligibility configuration is added. A notice on all four recovery peers identifies the applied boundary, including sham, without another stored flag. Ordinary numeric receipt fields stay identical in L/F/masks and B/C/K; a pending ordinary field reveals no value, while historical disclosure requires delivered v2. Seventeen focused CPU checks and the 61 existing view/protocol/round checks pass; native artifacts and final acceptance remain open. |
| Offline exact evaluation/analysis, ready before GPUs | Prevents correctness feedback and late discovery of unrecorded analysis inputs |
| Keep incidental names/layout flexible | Freeze interfaces and scientific invariants; avoid abstractions unsupported by a current requirement |

### Discoveries or deviations

M1-T01 verified that all five mathematical families and both sizes need no CPU
runtime dependencies; the model stack remains optional and unimported. Its
one-draw generator remains deliberately unconditioned; M1-T02 now supplies §2.2
population conditioning, exact edit selection, rejection accounting and persisted
streams. Both canonical fixtures regenerate exactly. Git's Windows CRLF conversion
would alter their bytes, so a narrow LF attribute protects these fixture files.
No scientific deviation was needed. Older schedules/configurations remain superseded; these CPU checks
are not protocol, hardware, pilot or empirical recovery evidence. Record future
deviations with affected specification sections, artifacts and checks to repeat.

M1-T03 closes the CPU mathematical/schedule gate with independently reconciled
60/40 main and development populations, explicit response joins and fixed prefix
sharing. The retained schedule stores main 60 and development; nested 40 derives
from the same slots. Both mathematical sizes round-trip and prepare through the
installed CLI outside the checkout. No science change or runtime dependency was
needed; actual reply equality, delivery and peer-visible execution remain M2/M3.

M2-T01 verifies the permitted-view boundary and actual lossless request/template
archive on CPU. Known tombstones and unknown replacements remain distinct;
historical receipts never become forwardable current records. Review reproduced
and fixed a stale latest-candidate state after a newer reply/feedback slot.
The full source/installed suite passes 79 checks, and five native Qwen tokenizer
checks reproduce the assistant-turn archive rewrite while preserving labeled
user-data history. No dependency or scientific change was needed. The saved
short fixtures are not the complete worst-context bound; actual protocol/event/
replay execution and capacity admission remain the subsequent M2 tasks.

M2-T02 verifies complete strict replies and whole-reply permissions/staging with
the specified Pydantic 2 dependency. Full source and installed runs pass 103
checks on Python 3.11.9 with Pydantic 2.12.5 and 2.13.5 respectively; explicit
core-only validation passes 80 without site packages. Six native Qwen checks
save/reproduce 20 adversarial replies, accept complete JSON closing at token 384,
reject aggregate 129-token prose and preserve repeated lawful forwarding attempts.
The five existing native renderer checks and saved requests still pass. Fixed
feedback remains within 32 actual tokens and never echoes library payloads;
invalid/failed slots remain absent. No scientific deviation, model call or accepted
freeze is introduced. Round commits, exact replay and complete capacity remain
later M2 tasks; ordinary dataclass records provide the next task's staging inputs.

M2-T03 verifies the complete in-memory round barrier and original-prefix cut
through the actual renderer, strict validator and exact source/text interface.
Source/installed validation passes 121 checks, core-only remains 80 and all 14
native checks pass. The saved eight-round scripted trace retains invalid/failed
slots, current-source acquisitions, exact requests/IDs, committed peer data and
actual owner-v1 exposures. Reversed physical order matches across all five
families/both sizes; deliberate nested sibling mutation cannot affect parent or
other siblings. Delivery attempts remain separate from first acquisitions, and
final messages drain without an extra call. No dependency or scientific change
was needed. This is protocol evidence, not an event-policy implementation,
full capacity proof, durable lifecycle, model capability or experimental result;
M2-T04 is ready and M2's gate remains open.

### Unresolved issues

| Issue | Smallest resolving step / decision evidence |
|---|---|
| Actual worst retained request fits 8,192 tokens | M2 complete renderer accounting plus adversarial tokenized fixtures; use only lossless layout or the allowed uniform size fallback, otherwise stop |
| Checkpoint/call/effect crash behavior in the real runner | M3 killed-process tests, then rerun against M5's accepted host lock; toy saver success is insufficient |
| Passing model/runtime/timeout and device headroom | M5 maintained-loader diagnostics and bounded smoke/pilot; no forecast or package version substitutes |
| 9B/4B, target/fallback size, 60/40 worlds | M5 capability and complete-schedule allocation evidence, following the specified precedence and shared development limit |
| Compute provider availability, persistence and allocation rules | Before GPU reservation, record actual devices, durable storage/backup location, allocation start/stop and billing rules; provider choice cannot alter experimental semantics |

### Final outcome / retrospective

Pending. Record the accepted configuration and achieved coverage, artifact location, reproduction result, consequential deviations, total resources, and remaining limitations. Distinguish a completed study from feasibility failure or documented incompletion.
