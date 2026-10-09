# Implementation plan

**Authority:** [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md), dated 4 October 2026 with the authorized pre-main capacity revision of 5 October 2026. Section references below refer to that document. This plan specifies engineering work and acceptance evidence; it does not change the experiment.

**Planning baseline:** repository commit `11979117fe868b825b98ac597085af5d9203509b`. The [README](../README.md), vendored source, and all four [implementation-research documents](implementation-research/SYNTHESIS.md) were inspected. The working tree was clean before this file was added.

**Implementation status:** M1–M4 are verified on CPU and all four gates pass. Twenty-one tasks are done, including [M5-T01 CPU inference/allocation preparation](todos/M5/M5-T01-inference-and-allocation-preparation.md#completion-and-handoff). The direct Qwen adapter and existing worker/attempt diagnostics are prepared with a [proposed Kaggle smoke packet](validation/m5-inference-preparation.md). Full regression passes 449 checks at the backend checkpoint; final identity review passes 27 focused and 41 installed checks, with 260 core checks (252 passed, eight optional skips). All sixteen original-worker report scopes reproduce twice with fixed main/stopped unknowns, seven exhibits and five portable reports. The [CPU audit](validation/m4-cpu-gate.md) maps all 22 plan rows and seven specification categories to named checks. [Actual Kaggle run 5](validation/m5-kaggle-full-preparation-run-5.md) passes all 97 CPU preparation checks with zero skips, following run 4's verified source/install/build. No repeat CPU preflight is requested. M5-T02 remains blocked by actual GPU/provider/model requirements and smoke preparation. Accepted inference, hardware/capability/resource gates and empirical results remain open. See the [living handoff](#10-living-handoff); CPU admission is not GPU feasibility or an empirical result.

The [actual run-6 review](validation/m5-t4-compatibility-run-6.md) now accepts
the standalone diagnostic on both T4s: 14 attention cases, four NF4 matmuls,
six stages/four commands and both off-host snapshots. Native GQA uses math;
repeated K/V uses efficient SM75 kernels at the tested shapes. No repeat CPU
or tiny-GPU run is requested. Next review supported model attention integration
and R7 complete-envelope memory offline before full model environment/assets,
exact requests, admission and smoke. T02 stays blocked. The user reports the
GPU session stopped; exact allocation duration remains unknown.

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
  runner.py                   fixed round graph, controls and original parent access
  workers.py                  balanced local process scheduling and restart ownership
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

Run tokenizer-only validation on the actual request template and reply serialization. Verify every candidate/control shape and useful one-shard messages fit; reserve the full 384 output tokens inside the authorized 262,144 total (pre-main revision of 5 October 2026). Bound retained history across the full prefix and recovery horizon, including invalid own replies, maximum received prose, feedback, labels, current tables, notices/receipts, source-delivery metadata, unusual escaping, and wrong integers. Use an accounting bound plus adversarial rendered fixtures, not only ordinary/correct outputs or the research's illustrative context. Q release must not duplicate history. Stress template special-looking strings and lossless archive preservation.

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
| M2 | Verified on CPU (6/6 tasks done; gate passed) | [T01 views](todos/M2/M2-T01-peer-views-and-rendering.md#completion-and-handoff), [T02 replies](todos/M2/M2-T02-strict-replies-and-feedback.md#completion-and-handoff), [T03 rounds](todos/M2/M2-T03-synchronous-rounds-and-prefixes.md#completion-and-handoff), [T04 boundaries](todos/M2/M2-T04-events-retention-and-receipts.md#completion-and-handoff), [T05 replay](todos/M2/M2-T05-mixed-and-prose-delay-replay.md#completion-and-handoff), and [T06 completion](todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate). Source and actual installed-library suites each pass 167 CPU checks; core-only passes 81, and all 37 native checks plus independent 4B capacity reproduction pass. The witness retains 4,340 calls/384 parent joins and output bounds 245/189 within 384. Authorized literal blocks/column labels/footer preserve work; a complete 261,388-token upper bound fits 262,144 uniformly. Both sizes are CPU-admitted; unpaired message surrogates are bounded whole-reply schema failures. Original negative evidence is retained. GPU memory/capability/timing and final model/size remain M5. |
| M3 | Verified on CPU (5/5 tasks done; gate passed) | [M3-T05 gate evidence](todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#completion-and-m3-gate): 18 durable, 22 attempt, 14 worker, 23 accounting and nine lifecycle checks; 253 source/installed and 81 core checks pass. Eleven real controller kills preserve raw reuse, branch-local effects, cleared fields and Q prose. Both complete fixtures reconcile 4,340 logical slots / 3,956 generations / 384 replays; full main/development schedules, synthetic budget stop/resume and supported backups pass. [Fourteen-case ordinary bundle](../tests/fixtures/scripted_lifecycle_run.zip) passes offline audit and fresh reproduction; all prior M3 CPU/native archives reproduce. |
| M4 | Verified on CPU (6/6 tasks done; gate passed) | [T01](todos/M4/M4-T01-exact-outcomes-and-trajectories.md#completion-and-handoff), [T02](todos/M4/M4-T02-estimands-and-repeatability.md#completion-and-handoff), [T03](todos/M4/M4-T03-information-and-work-diagnostics.md#completion-and-handoff), [T04](todos/M4/M4-T04-policy-costs-and-boundary-rule.md#completion-and-handoff) and [T05](todos/M4/M4-T05-uncertainty-and-missingness.md#completion-and-handoff) establish exact outcomes, estimands, information/work, policy costs and paired uncertainty from original workers. [T06 completion](todos/M4/M4-T06-reproducible-report-and-cpu-gate.md#completion-and-m4-gate) supplies reports, exact cases and the passed [coverage/category audit](validation/m4-cpu-gate.md). All 424 source checks pass; focused/core/installed checks pass 25/252 (244 passed, eight optional skips)/166. Sixteen report scopes reproduce every M4 output/export twice under current source and installed hash seed 37; five reports retain 35 SVG/PNG exhibit pairs. |
| M5 | T01 verified on CPU (1/5 tasks done); operational gates open | [T01 completion](todos/M5/M5-T01-inference-and-allocation-preparation.md#completion-and-handoff) supplies the direct adapter, exact raw/seed/cache/worker diagnostics and [proposed Kaggle packet](validation/m5-inference-preparation.md). Final 27 focused / 41 installed checks pass, and the 449-check full regression passes at the backend checkpoint. The first Kaggle run supplies device/CUDA inspection but rejects source; the [actual CPU canary](validation/m5-kaggle-upload-canary-run-2.md) passes byte transport/off-host snapshots. [Run 4](validation/m5-kaggle-full-preparation-run-4.md) verifies complete source/Linux cleanup, candidate installation and project build, retaining its failed probe parser. [Actual run 5](validation/m5-kaggle-full-preparation-run-5.md) passes the repaired installed provenance and all 97 CPU checks with zero skips, clean owned commands and independently reopened exports. [Actual run 6](validation/m5-t4-compatibility-run-6.md) accepts standalone tiny attention/NF4 diagnostics on both T4s. No repeat CPU/tiny-GPU run is requested. Supported model attention integration, full-envelope headroom, full-candidate GPU host/model smoke, capability and allocation reconciliation remain pending. |
| M6 | Not started | Requires accepted M5 freeze |

### Implementation decisions

| Decision | Reason / reconsideration evidence |
|---|---|
| K10 reviews an opt-in public SDPA layout and maintained bounded prefill offline | [The attention/memory contract](planning/m5-kaggle-first-run/08-attention-and-memory.md) responds to run 6's math dispatch and materialized-K/V cost. Reinterpret KV groups as the kernel batch and broadcast heads with views; register a matching native mask formatter and force only efficient CUDA dispatch. The proposed candidate records a fixed 256-token maintained prefill chunk size. Keep baseline SDPA/settings unchanged; verify head/mask/cache/logit semantics on CPU and derive memory evidence from the existing complete bound. Actual T4 layout/model/headroom remains unaccepted; no cap, retention, package or fallback selection changes. |
| K10's first T4 step is a standalone matching-Torch/verified-wheel diagnostic | The [bounded plan](planning/m5-kaggle-first-run/07-t4-compatibility.md) isolates the tiny SDPA/NF4 question without repeating a 4.07-GB install while two GPUs are assigned. Require host Torch 2.11.0+cu128, verify/extract only the pinned bitsandbytes wheel, use fresh `-I -B` children bound to distinct UUIDs and reuse existing command/storage/export helpers. Forty-two operational/four real CPU checks and exact-cell Jupyter exports pass locally; actual run 6 now passes 14 attention/four NF4 cases on both T4s. The full model lock and affected GPU/model paths must be checked later; supported attention integration and R7 remain unresolved. No scientific/backend/quantization/fallback setting changes. |
| Actual GQA math dispatch and repeated-K/V memory are reviewed together | [Run 6](validation/m5-t4-compatibility-run-6.md) observes native-GQA math and efficient repeated-K/V SM75 kernels with matched tiny outputs. It does not implement a model adapter. A fully materialized repeated K/V pair adds a conditional 4 GiB per active full-attention layer at the cap. Native total is 14.562 GiB per T4, versus 15-GiB inventory; native total minus headroom is 13.062 GiB. Next review a supported model route's causal/mask/cache and temporary-memory semantics plus sound R7 coverage offline. No model failure, cap attainability, fallback selection or candidate change is inferred. |
| M5-T01 uses one explicit maintained text-only adapter and the existing process/attempt ledger | Native AutoModel text-config/prefix conversion and tied-head diagnostics avoid a conversion wrapper. A fresh GenerationConfig, empty DynamicCache, exact canonical settings/token JSON, saved seeds and explicit matching/distinct worker device assignments implement the stated inference boundaries. The full raw suffix stays in optional existing process/attempt evidence fields; only one verified terminal im_end is removed for parsing. Old read-only records need no migration, and no new identity, progress store, dependency or orchestration layer is added. Final CPU/static/mock checks pass 27 focused and 41 installed; native 9B/4B metadata checks pass four each. Actual weights, GPU behavior and the proposed two-T4 clock/storage plan still require T02 validation. |
| M4-T06 uses the existing read snapshot and seven explicit report exhibits | Original workers supply every M4 table and exact unaltered excerpt together. Case medians use exact rational effects then immutable IDs; complete illustration worlds require all scheduled slots in the supplied scope recorded, including failures/controls/repeats. Both selection and card joins enforce replicate zero; absent signs and all-zero regression/smallest-ID fallbacks remain explicit. Raw invalid Unicode uses reversible JSON string notation in HTML, with original text unchanged. Absolute quality/cost axes exclude paired differences while retaining their scientific tables. Derived HTML/CSV/JSON and plotting inputs are exports, not another store. Optional Matplotlib reads saved plotting data only. Final 25 focused, 424 source, 252 core (eight optional skips) and 166 installed checks pass; all sixteen original-worker scopes reproduce twice. The M1–M4 CPU audit passes; M5 hardware/capability/resource gates remain separate. |
| M4-T05 uses explicit standard-library world resampling and shared-response bounds | The existing world/component/generation joins suffice. Exactly 10,000 paired draws use saved nonnegative seed 20261006 plus each existing family index, sorted world IDs, equal-family means and type-7 linear quantiles. Matching family/world cohorts share draws; repeats remain conditional and do not increase population N. Constant within-family values have the prescribed weighted Hoeffding companion. Unknown logical copies can be constrained by recorded originals for sensitivity without becoming executed observations. Small shared nonlinear expressions are enumerated; larger ones retain shared terms with conservative labels. Preservation and its paired cost use the same eligible worlds. Whole-policy IDs remain schedule-checked; missing future costs remain unbounded. All sixteen original-worker cases reproduce; final focused/core/installed checks pass 33/225 (221 passed, four optional skips)/144, and complete CPU regression passes 396. [T05 evidence](todos/M4/M4-T05-uncertainty-and-missingness.md#validation-and-evidence) records independent binomial/quantile/bootstrap references and actual replay cancellation. |
| M4-T04 shares original ledger arithmetic between status and offline cost views | Pure functions in `costs.py` preserve M3's attempt, policy and allocation arithmetic. Offline records/checkpoints/allocations are read in the existing worker snapshots, without saver setup or a new store. Hypothetical costs include every logical use and F's original prefix; outside overhead remains experiment overhead. Initial B/C/K ID/version coverage alone chooses one C/K branch. Unavailable selected branches remain unknown, and shared generation costs cancel in paired differences. Twenty-eight dependency-free focused checks and sixteen original-worker cost reconstructions pass. Complete source regression passes 362 checks; final inventory review passes 191 core checks (188 passed, three optional skips) and 110 installed checks. [T04 evidence](todos/M4/M4-T04-policy-costs-and-boundary-rule.md#completion-and-handoff) records commands and checkpoint scope. |
| M4-T03 derives delivery inventories from saved committed checkpoints in the existing read snapshot | The last round's validated sends cannot prove their release or acquisition. The installed saver's public serializer decodes the existing committed channel in the same read-only SQLite transaction as calls/inputs/attempts, without saver setup, pending writes, runner invocation or another store. Unobserved releases and full-horizon acquisitions remain unknown. History counts require exact saved input-ID equality with a supplied tokenizer; independently encoded retained content is separate from request cost. |
| M4-T03 keeps source association conservative and candidate assumptions explicit | Exact literal `xNNN/v1=INTEGER` matches and genuine host receipts qualify; numeric coincidence and other prose remain unresolved. Every excerpt retains original IDs and spans. Reconstruction requires an actually retained last candidate under an explicit correctness assumption; C's cleared archive value cannot supply it. Offline Prefix/Difference transport instead uses the actual valid last candidate even when wrong and verifies preserved residual errors. The rubric and named-view atlas witnesses are ready for the later M5 freeze, with no peer feedback or population filtering. |
| M4-T01 derives offline scoring from existing application records | Exact outcomes and call-boundary annotations require saved calls/attempts and pre-delivery state, with original replay/prefix joins. Read-only SQLite snapshots suffice without importing the runner, inference or checkpoint serialization. BFS canonical pairs are decoded before full-node comparison; prefix eligibility uses only the last scheduled prefix reply. A demonstrated unbound-worker source mismatch is rejected against the existing manifest. Sixteen derived table cases reproduce with no new store, dependency or identity system. |
| M3-T05 avoids redundant scheduler checkpoint reads | The complete scripted fixture exposed repeated readiness scans while all workers were busy and a second saver read for state already obtained with its metadata. Dispatch now waits when no worker is idle, and scheduling derives state from that same saved checkpoint. No cache or extra record is introduced. All 14 worker checks, nine lifecycle checks and 253 source/installed regressions pass. |
| M3-T05 packages ordinary worker records through SQLite backup | The integrated crash gate and M4 handoff need inspectable persisted evidence. Existing manifests/SQLite snapshots remain authoritative; ZIP only packages them with actual kill commands/markers and derived previews. Eleven external controller kills and exact resumed-record comparisons pass, including both WAL/FULL connections, relocated workers and held prose. Fourteen cases reproduce; relative path normalization makes retained Windows references readable through ZIP paths without rewriting the evidence. No new persistence or test-management system. |
| M3-T04 derives progress/costs from existing records and checkpoints | Existing call/attempt keys and saved configuration scope resolve physical and policy costs. The ledger stores request-token counts for responsive reads, verified against exact barriers, and optional peak memory; only allocation intervals add persistence. Loading inside an attempt is included in its measured cost, while allocation partitions setup/interruption/attempt/idle once. Twenty-three focused and 244 source/installed CPU checks pass. The pinned saver's first public read commits existing transactions through `executescript`; status primes it before its read snapshot. Cross-worker parent commits get at most two read retries, with no inference/effects. Provider reservation start/billing and confirmed release remain distinct from process lifetime. Nine accounting cases and all prior archives reproduce. |
| M3-T03 accesses original worker records through SQLite read-only connections | The pinned saver public read path works with `mode=ro` and `query_only=ON`; writes are rejected. Committed channel values exclude pending node effects. Physical parent rows and attempts stay in their original file, while logical replay rows and independent queues stay in the assigned worker. Durable controls use the same raw-call/attempt ledger, with no delivery thread. Fourteen focused worker checks and 221 source/installed checks pass; parent access adds no physical charge. |
| M3-T03 enforces exclusive file ownership before recovery | A provider PID cannot identify an idle worker that has not loaded inference. A one-byte OS-lock sidecar rejects a second controller before any writer/recovery is opened; it stores no scientific or progress data and is released by the OS on owner death. Restart also confirms the preceding inference process exited before admitting replacement work. The idle-owner rejection and Q interruption/resume checks pass. |
| New shallow package; vendor/archive remain references | Native execution/scoring conflict with the required protocol; do not inherit obsolete architecture |
| M1 task core uses frozen standard-library records and caller-owned generation/ownership RNGs | No numerical, graph or inference dependency is needed for these exact computations. Public candidate contracts/source manifests are separate from offline truth; BFS IDs bind only after edge shuffling and tombstones retain endpoints. |
| M1-T02 legal edit sets precede sampling; events take only original v1 worlds | Main selection uses record then replacement, preserving uses a single pair draw without owner matching. Top-K preserving originals are strictly below the cutoff; cutoff-equal replacements preserve the ten-value multiset. Deterministic checks cover both sizes, independent BFS deletion truth and the exact 1,000-attempt ceiling. |
| Prepared populations use one canonical JSON record and fixed integer seed slots | Saved actual worlds/edits are authoritative; gold and footprints remain evaluator-side. Stable world slots/configuration give disjoint local stream seeds, with event/policy absent from continuation seeds. Nested 40-world/focal populations derive from the saved 60; loading never regenerates. Exact baseline comparison detects changed valid inputs; no checksum/identity registry is added. Both-size fixtures and CPU CLI are verified; the M5 accepted freeze remains future work. |
| M1-T03 schedules use existing world/branch/call keys and explicit prefix/raw-reply parents | Independent component/cell checks reconcile both complete main totals and the exact development matrix. Equal seeds create distinct generations unless a prescribed first-round B/C parent exists. The nested 40 is a view of the 60-world schedule; smoke is separate and the first 90 pilot slots are prefix/controls. Saved schedules are derived artifacts checked against the population, without copied raw worlds or another identity system. Save/reload, mutations, dependency orders and CPU prepare/validate pass in the 59-check suite; runtime equality/delivery remain M2/M3. |
| LangGraph barriers plus local SQLite and explicit raw-call ledger | Meets §9's starting choice; replace with the permitted small loop only for a demonstrated unresolved semantic incompatibility in M3 |
| M3-T01 uses replacement byte snapshots and an application-owned raw-call ledger | `prepare → obtain → commit` uses synchronous durability. Existing IDs join pre-delivery inputs, physical outcomes, attempts and logical replays; committed checkpoints exclusively own effects. Explicit round arguments make lost acknowledgements idempotent. Public saved checkpoint configurations exclude durable pending writes from delivery exports; normal graph resume consumes those writes. Active attempts without raw output stop for M3-T02 recovery. Tested CPU dependency pins are not an M5 freeze. [T01 evidence](todos/M3/M3-T01-durable-round-runner.md#validation-and-evidence): 18 focused checks, 185 source/installed checks, 81 core checks and both 240-round CPU/native archives pass. No small-loop fallback or second effect store. |
| M3-T02 uses one resident inference subprocess and the existing attempt keys | A spawn-compatible model loader is required for termination/reload while preserving resident weights. The parent owns SQLite; pipe I/O and an owner-sentinel watcher keep hangs and orphaned generation bounded. Known timeout is durable before kill; only an absent durable outcome after infrastructure interruption permits one identical retry. Existing `(call_id, number)` keys own bounds/observed work/uncertainty and loading/idle/stop intervals; this process table is necessary for later charging work omitted by attempt durations. Default bounds are 120 seconds plus one-second terminate/kill graces. Direct providers require explicit deterministic `scripted=True`. [T02 evidence](todos/M3/M3-T02-bounded-attempts-and-failures.md#validation-and-evidence): 22 focused and 207 source/installed CPU checks, exact archives and real kills pass. No delivery store, new identity, scheduler or dependency is added. |
| Explicit narrow peer views and pure state/delivery transformations | Makes scientific visibility, replacement and replay inspectable and CPU-testable |
| M2-T01 uses immutable permitted records and a single user-data renderer | Initial projection/held-source lookup take no evaluator or schedule labels. Current/pending/deleted sources, receipt history, derived text, feedback and latest-slot absence are distinct; public identity alone orders sources. Candidate state cannot precede recorded own/feedback slots. Native non-thinking template text and untruncated token inputs are ordinary saveable records. Fixed public feedback prevents hidden library-error payloads; complete capacity and event/round transformations remain later M2 tasks. |
| M2-T02 uses complete JSON decoding, strict Pydantic 2 and whole-reply staging | Pydantic 2 is now a declared CPU dependency. Full validation includes the strict-reply suite; explicit `--core-only` retains dependency-free checks without claiming protocol admission. Generated IDs govern the 384-token cap; literal message texts are tokenized separately and summed. Source staging resolves only immutable sender-held records and preserves repeated attempts. Fixed public feedback has an actual tokenizer guard; invalid/failed outcomes replace candidates with absence. No delivery, correctness check, response repair or extra call is introduced. |
| M2-T03 separates pure request, validation, staging and delivery barriers | The in-memory procedure uses the existing views/renderer/validator and call-key spelling; M3 still owns LangGraph/SQLite integration. Source/text component IDs preserve repeated attempts and branch-local idempotence. First-acquisition metadata remains public; full attempts/IDs/queues remain offline. Plain JSON deep-deserialization supplies drained immutable prefixes without another store. Final recovery deliveries are audited at an unscheduled next-round boundary, without a fifth opportunity. Eighteen focused checks, the 121-check source/installed suites and three native round checks pass; the existing 11 native checks still pass. |
| One serial process/replica/database per GPU; access to saved inputs | Keeps inference/RNG isolated while permitting sibling/device rotation |
| M2-T04 uses explicit boundary cases, saved schedule identities and persistent notices | Every start deep-deserializes the original prefix and checks original sources/fourth-slot outcomes. The existing schedule enumeration governs subsets/repeats; no second eligibility configuration is added. A notice on all four recovery peers identifies the applied boundary, including sham, without another stored flag. Ordinary numeric receipt fields stay identical in L/F/masks and B/C/K; a pending ordinary field reveals no value, while historical disclosure requires delivered v2. K's exact historical result/absence moves into labeled history once when replaced by a new slot. Nineteen focused CPU checks, the 140-check source/installed suites and all 18 native checks pass; exact replay and durable apply-once execution remain T05/M3. |
| Offline exact evaluation/analysis, ready before GPUs | Prevents correctness feedback and late discovery of unrecorded analysis inputs |
| M4-T02 uses explicit rational components over the M4-T01 outcome join | Exact means preserve zero-effect ties. Components retain named peers/rounds, original call/generation/prefix IDs, coefficients, exact weights, endpoint operators/ranges and unknowns for T05; no identity system, dependency or store is added. Fixed populations supply equal-family denominators, with separate complete-case descriptions and conditional repeats. Q activity derives from committed saved delivery state and never selects worlds. [T02 evidence](todos/M4/M4-T02-estimands-and-repeatability.md#validation-and-evidence) records 306 complete, 134 core, 54 installed and 53 focused/archive checks, with final focused review additions and four original-worker table cases. |
| M2-T05 separates saved continuation replies from branch-local commit | `SavedRound` retains the existing scheduled calls, immutable settings JSON and pre-delivery barrier. The prescribed B/C parent must match event/replicate, view, exact rendered/native request, settings and seed; revalidation preserves its recorded outcome. Q uses the existing pending component IDs and derives nonempty held counts from committed records, including zero for inactive branches. Eighteen focused CPU checks, all 158 source/installed checks and 22 native checks pass. No dependency or second delivery/counter store is added. Durable records/checkpoints remain M3. |
| M2-T06 witness uses only the permitted local view and existing mathematical functions | `witness.py` is a CPU validation strategy, never an inference tool or study policy. Own-shard forwarding in rounds 1–3 acquires every current record by round four, including L's replacement and F's discarded remote evidence. Five focused CPU and four native witness checks pass across all families/sizes/siblings/repeats/controls. Offline gzip preserves the full evidence without changing peer history. |
| Original M2-T06 capacity failure (before the authorized revision) | Six native checks reproduce real 384-token invalid-slot overflows at both sizes, full-horizon adversarial fixtures, conservative accounting, failed simple lossless layouts and an unpaired-surrogate gap. The native capacity command returns 1 after those checks pass; no size/cap/Unicode rule or renderer is changed. Complete admission needs a passing literal representation and resolved Unicode boundary, or an explicitly authorized pre-main scientific decision. |
| Authorized M2-T06 remedy uses literal blocks and a uniform native window | After the user selected option 1 and authorized implementation, structural column tables remove repeated labels while length-delimited blocks preserve every own reply/prose string. A footer defeats native outer-whitespace stripping; rendered text and native NFC IDs remain distinct. Scalar message validation rejects unpaired surrogates before counting/effects. The full loaded-vocabulary/Unicode/horizon proof fits 261,388 including reserve under 262,144 for both sizes without positional extension. No histories, output caps, populations or comparisons are removed. Static full-attention FP16 KV alone is 8 GiB at the cap; complete T4 headroom/timing/capability must pass M5. |
| Keep incidental names/layout flexible | Freeze interfaces and scientific invariants; avoid abstractions unsupported by a current requirement |

### Discoveries or deviations

M4-T04 inventory review found that the new retained-remote view counted the
host-injected edited record. It now applies M4-T03's `exclude_record_id`
convention. The separately computed current-manifest coverage includes that
record, as required by the frozen rule. A focused check removes only v2 and
verifies K selection, while complete inputs select C and retained remote counts
exclude v2. All sixteen updated cost cases reproduce unchanged M3 costs and
selection; no scientific or frozen-configuration change is made.

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
this established the M2-T04 prerequisite and left M2's gate open.

M2-T04 review found that replacing the latest candidate after K's first
recovery call would discard its retained historical result. The round commit
now appends that exact fourth-slot candidate/absence once as a labeled history
entry before installing the new slot outcome. It does not fabricate a full
reply, recover an earlier answer, or recompact subsequent history. Serialization
and rendering preserve this entry, including BFS tuples and invalid/failed
absence, through all four recovery calls. Nineteen focused event checks and
all 61 existing view/protocol/round checks pass. Final source/installed suites
pass 140 checks and all 18 native checks pass. The original boundary renders
and previous native fixtures remain unchanged.

M2-T04 now verifies every saved non-Q boundary, source/pending/tombstone
authority, sham and preserving siblings, literal B/C/K/F/mask retention,
historical receipts, nested isolation and identifiable boundary application.
The native archive retains four prefixes, 15 boundary snapshots and 60 first
requests. Receipt disclosure changes only the archived before-value; the saved
Prefix Sum/Sort pairs cost four/three fewer input tokens per peer than ordinary
wording, without padding. Ordinary new history and K's retained result persist
through all four recovery slots. No scientific deviation or dependency was
needed. This established the M2-T05 prerequisite, without a model/pilot/main
result or complete capacity proof.

M2-T05 now verifies exact scheduled B/C reply reuse for both masks and Q,
including invalid/failure records, mismatched dependency rejection and
event/replicate scoping. Each branch reconstructs its outgoing set from its
own original start. Q's round-two sources, own reply and source metadata match
its parent; only incoming prose waits until the round-three boundary. Release
preserves stable IDs and already-seen history, with no extra call or permanent
drop. Held counts derive from committed records and retain inactive branches.
The new native archive reproduces 54 rounds, 216 requests and 72 exact parent
comparisons; prior fixtures are unchanged. Source/installed validation passes
158 checks, core-only passes 80, and all 22 native checks pass. M2-T06 is ready;
the local-view witness, complete capacity bound and M3 durability remain open.
No scientific deviation, dependency, inference run or accepted freeze was needed.

The T05 artifact audit found that the initial inactive scenario reused IDs from
a different scripted parent response. The corrected fixture uses distinct,
predetermined saved worlds for source-only scenarios and archives their parents.
An archive-wide native check now requires unique call IDs and exact joins for
every replay. This changes the validation evidence, not the design. A final
reporting guard rejects held-prose counts before a committed recovery round,
preserving the distinction between unexecuted and observed inactive treatments.

M2-T06 completes the authorized CPU preparation but cannot close M2. Its local
strategy uses only acquired current records and public output assignments, with
ordinary own-shard routing over three rounds. Ten saved family/size cases cover
every scheduled sibling/repeat, 1,080 four-peer rounds and 20 controls, with 4,340
calls/384 exact parent joins archived. All final answers are correct. Actual
witness requests use 699–4,915 input tokens plus the full reserve; correct-width
candidate/control/one-shard outputs use at most 210 target / 162 fallback tokens.
These are constructive protocol checks, not model capability or recovery results.

The complete capacity investigation rejects both sizes before inference. One
permitted invalid 384-token reply (token 76374 repeated, decoding to long newline
runs), nine-token public feedback and three lawful 128-token received texts make
the next prefix request exceed the cap: 14,642 target / 14,349 fallback with the
384 output reserve. Thirty full-horizon fixtures and complete fixed-field/byte
accounting include labels, sources, first-acquisition metadata, receipts, wrong
integers, Unicode/escaping and Q's single release. The bounds are deliberately
loose and do not certify admission. Another token's re-encoding expansion defeats
ordinary UTF-8 JSON and raw-text alternatives even for history alone. A separate
JSON-escaped unpaired surrogate reaches the schema but raises at literal prose
tokenization; it is surfaced without repair or an invented character restriction.

Source and installed-outside-checkout validation pass 163 checks, core-only passes
80 without site packages, and all 32 native verification checks pass. Fresh-process
4B metadata reproduce the capacity report under `PYTHONHASHSEED=37`; tokenizer,
configuration and actual template identities match the pinned 9B artifacts.
Both capacity commands deliberately return 1 for the failed gate. See the
[T06 accounting, commands and environment](todos/M2/M2-T06-attainability-and-capacity.md#capacity-accounting-and-exact-failure).
No scientific/frozen-configuration change, history truncation, new cap, model
generation or GPU allocation occurred. M3 remains dependency-blocked. The next
decision must resolve the exact retained-text/capacity and Unicode incompatibilities
and renew all affected M2 checks; passing the scripted witness alone is insufficient.

The [M2-T06 lessons and ranked fixes](implementation-research/m2-t06-lessons-and-fixes.md)
record conditional remedies and their required revalidation. On 5 October 2026,
the user selected option 1: a readable lossless layout with a larger uniform
context, preserving all retained work, then authorized implementation. Scalar
message validation now rejects unpaired surrogates before native prose counting;
valid escaped pairs and other scalar text remain literal. Raw replies/IDs,
candidate absence and whole-reply no-effects semantics are preserved. The 25
focused CPU checks and seven native protocol checks pass. The literal layout,
column tables and template-safe footer are now verified under the uniform native
262,144 limit. The [complete proof](implementation-research/m2-t06-capacity-proof.md)
bounds input plus reserve by 261,388; both sizes are CPU-admitted. All 167 source
and installed-library checks, 81 core checks, 37 native checks and independent 4B
capacity reproduction pass. Native archives are renewed, including Unicode-invalid
parent replay. M2 closes and M3-T01 becomes ready. M5 still owns GPU memory,
headroom, capability, timing and final configuration/size admission; none is claimed.

M3-T01 completes on 5 October 2026. The actual worker-local graph saves exact
raw replies/failures before validation/effects and checkpoints replacement
branch state. Eighteen focused checks cover every scheduled first-round start
across all families/sizes, invalid/failed replay, mismatch rejection, clearing,
Q held-queue resume, partial raw commits and saver failures before/after delivery
commit. Source and actual installed-library regressions each pass 185 checks;
core-only passes 81. Both durable archives reproduce in fresh hash-seed-37
processes: 60 branches, 240 rounds, 960 logical calls, 864 physical attempts and
96 exact parent joins, with two Q transitions reconstructed from saved replies
and all backup states preserved. These are scripted CPU checks and native
tokenizer-only checks; no weights/model/GPU or experimental outcomes were used.
At T01 completion, active attempts without raw outcomes stopped for T02's
uncertain-completion, termination and bounded-retry handling. T02 completes
that boundary below; scheduling/controls, cross-worker parents, accounting
and the combined M3-T05 gate remain open.

M3-T02 completes on 5 October 2026. A resident spawned inference process uses
the existing exact inputs and application ledger; the parent remains responsive
and terminates a hung attempt under its default 120-second bound. Timeout is
durable before termination. Restart after the preceding owner stops preserves
unknown completion/duration and observed work, permits one identical retry and
exhausts a second interruption without a third attempt. Invalid/truncated/wrong
and known failure records remain final; ordinary failures continue the fixed
opportunities and never inherit an earlier candidate. Overflows stop before
generation. Loading/resident idle/termination intervals remain available for
M3-T04 attribution, including uncertain stop times after owner death.

Twenty-two focused checks include real controller kills before/after raw reply,
during loading and timeout termination; inference children die with their owners.
Source/installed-library suites each pass 207, and core-only passes 81. Both
240-round CPU/native durable archives remain exact. The 12-case failure archive
reproduces exact call/attempt/state records with a fresh hash seed and retains
78 attempts, 28 process intervals, nine uncertain completions and four unknown
attempt ends. Five confirmed CPU hung timeouts exceeded their deadlines by
0.015–0.031 seconds; this is not a GPU timing forecast or timeout admission.
See [T02 verification](todos/M3/M3-T02-bounded-attempts-and-failures.md#validation-and-evidence).
[M3-T03](todos/M3/M3-T03-local-worker-scheduling.md) is ready. Worker placement,
controls/cross-worker parents, resource accounting/status, the combined M3 gate
and execution-host/model adequacy remain open. Specification/configuration and
prior archives are preserved; no weights, GPU/model inference or main outcomes
were used.

M3-T03 completes on 5 October 2026. Balanced saved world-index blocks and
rotated eligible siblings execute through serial worker controllers and one
bounded resident generation process per worker. Device visibility is inherited
before child imports/factories. Original prefixes and B/C pre-delivery parents
are accessed read-only, preserving physical IDs/raw failures and branch-local
queues/effects. Full-information controls now persist in the same attempt ledger.
Literal input/settings/bounds bindings reject drift before admission; OS file
locks reject live/idle duplicate owners, and restart confirms provider exit.
Status reconstructs runnable/dependency-waiting work without correctness input
or another progress store.

Fourteen focused checks include actual uneven-delay workers, order/placement
reversal, immutable cross-worker parents, missing/mis-scoped dependency rejection,
Q termination with held prose, lost acknowledgements and exclusive idle ownership.
Source/installed suites each pass 221; core-only passes 81. Eight archived CPU
scenarios reproduce 666 logical calls, 618 distinct generations, 619 attempts,
48 exact replays, 17 process intervals and one uncertain interrupted attempt.
The export comparator now normalizes in-memory tuples to retained JSON arrays;
no scientific fields were relaxed. Both earlier CPU/native durable archives
reproduce unchanged. See [T03 evidence](todos/M3/M3-T03-local-worker-scheduling.md#validation-and-evidence).
At that handoff, [M3-T04](todos/M3/M3-T04-accounting-progress-and-budget.md) was
ready; attribution/progress/budget stops and the combined T05 gate remained open.
Specification/configuration and prior archives are unchanged. No weights,
GPU/model inference, pilot or main outcomes were used.

M3-T04 completes on 5 October 2026. Physical costs join original generations
and every measured/uncertain attempt; hypothetical policies include the original
prefix and all sixteen continuation uses, including F and invalid/failed replay
parents. Allocation intervals separately partition setup/interruption/attempt/
unobserved work/idle, with no duplicate overhead. Provider reservation start,
confirmed release and billing are separate from process lifetime. Only existing
ledger token counts/optional memory and necessary allocation intervals persist;
progress, policy totals, forecasts, dependencies and matched coverage are derived.

Twenty-three focused and 244 source/installed checks pass. The nine-case archive
reconciles 112 logical calls, 100 generations, 101 attempts, 203 synthetic attempt
seconds and 400 synthetic allocated seconds. These hand-test costs are assigned,
not observed inference times. Adverse timeouts, a hard deadline,
uncertain work and exact single-retry resume preserve unknown opportunities.
Measured phase/condition/device forecasts include slower devices, 25% margin,
serialized idle allocation, reserves and external overhead; missing cells remain
unavailable. Earlier configurations stay charged without supplying incompatible
timing samples. Live CLI, heartbeat, backup/migration and concurrent reads pass.
The initial full-suite status race was fixed after verifying that saver setup
commits an existing SQLite transaction; bounded cross-worker rereads preserve
monotonic parent commits without inference. All prior CPU/native durable,
attempt and worker archives reproduce. See [T04 evidence](todos/M3/M3-T04-accounting-progress-and-budget.md#validation-and-evidence).
[M3-T05](todos/M3/M3-T05-crash-safe-scripted-lifecycle.md) is ready; M3 remains open.
No scientific/frozen-configuration change or actual GPU/model/pilot/main run
occurred. M5 retains actual provider-release, timing/memory and hardware gates.

M3-T05 completes on 5 October 2026 and closes M3's CPU gate. Both declared sizes
execute every scheduled path for the first prepared main world of each family:
4,340 logical slots, 3,956 physical generations and 384 exact replays. Full
60/40 main and development manifests independently reconcile with all
unexecuted opportunities explicit. Eleven real external kills cover raw commit,
validation/staging, delivery checkpoints, C/F boundaries and retry exhaustion.
Uninterrupted versus relocated/reopened workers preserve every scientific call,
input, validation and unique committed transition. Invalid/timeout parents are
never resampled; held Q prose stays queued and releases chronologically. Budget
exhaustion preserves sixteen unknown slots and one uncertain attempt, then
resumes with the same configuration and one permitted retry.

The [ordinary lifecycle bundle](../tests/fixtures/scripted_lifecycle_run.zip)
retains fourteen cases, original manifests, SQLite backups, actual kill argv/
receipts/markers, request traces and derived progress/correctness previews. Its
actual packaged snapshots pass offline audit and a fresh hash-seed-37 exact
reproduction. Source and installed-library suites each pass 253 checks, core-only
passes 81, and all earlier M3 CPU/native durable, attempt, worker and accounting
archives reproduce unchanged. The fixture's redundant scheduler reads were
removed without new state/cache; portable relative archive references were
verified with the retained offline audit. See [T05 evidence](todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#validation-and-evidence).

At the M3 handoff, [M4-T01](todos/M4/M4-T01-exact-outcomes-and-trajectories.md) became ready. The preview
establishes available inputs, not completed M4 estimands/diagnostics/reporting.
M4 remains mandatory before GPU use, and M5 must repeat persistence checks in
the accepted host/environment. The scientific specification/configuration and
all prior fixtures remain unchanged; no weights, model/GPU inference, pilot,
main execution or publication occurred.

M4-T01 completes on 5 October 2026. Exact candidate scoring, D/U repair versus
collateral damage, eligible peer → world → equal-family rates, trajectories and
six nonexclusive annotation labels now run entirely offline. The
[retained tables](../tests/fixtures/exact_outcome_tables.json.gz) reproduce sixteen
cases from the M3 bundle, including full target-60/fallback-40 joins with 15,486 /
10,390 unknown slots and the sixteen stopped unknowns. Raw generation/replay/
attempt identities remain original; no earlier candidate backfill, fifth round
or answer splicing is used. The M3 preview's BFS decoding is corrected without
changing its retained wrong-answer scores or any prior artifact.

The complete CPU regression passes 278 checks including all nine lifecycle
checks. Final focused/core/installed checks pass 26/108/27, including the later
source-drift and final-prefix eligibility checks; every derived table reproduces
under hash seed 37 and M3's retained offline audit passes. See
[M4-T01 evidence](todos/M4/M4-T01-exact-outcomes-and-trajectories.md#validation-and-evidence).
At that handoff M4-T02–T04 became ready. Contrasts, information/work inventories, costs,
uncertainty/missingness and the complete synthetic report remain M4 work.
The scientific specification/configuration/dependencies and all prior fixtures
are unchanged; GPU/model/pilot/main execution and publication remain unexecuted.

M4-T02 completes on 6 October 2026. All prespecified primary/secondary effects,
receipt/Q/preserving companions, own-group/mask trajectories and conditional
repeat displays now derive from the existing full outcome join. Exact rational
components keep ties exact and retain original response IDs/weights, endpoint
operators/ranges and unknowns for T05. Equal-family summaries keep intended
population denominators; complete-case descriptions remain separate. Repeats
never replace replicate zero or add independent worlds. Q activity retains
inactive and unobserved branches without changing inclusion.

The [four retained table cases](../tests/fixtures/estimand_tables.json.gz)
reconstruct from original M3 workers under hash seed 37. Complete five-family
fixtures give θ=φ=0; full target-60/fallback-40 primary estimates remain unknown
with 15,486/10,390 unexecuted slots, rather than becoming complete-case zeros.
The complete CPU regression passes 306 checks, including all nine lifecycle
checks; core/installed/focused checks pass 134/54/53. Later review additions pass
all 21 focused checks without changing production code or retained tables. See
[T02 evidence](todos/M4/M4-T02-estimands-and-repeatability.md#completion-and-handoff).
M4-T03/T04 remain ready; T05 still requires T04 and the complete M4 report gate
remains open before GPU use. The specification, configuration, dependencies and
all prior fixtures are unchanged. Hardware/pilot/main execution and publication
remain unexecuted.

M4-T03 completes on 6 October 2026. All four prefix-round inventories, actual
owner-v1 rendered exposure, L/B receipt timing/origins/censoring, C/F boundary
evidence and new acquisitions versus all delivery attempts now derive offline
from original records. Source-bound annotations retain literal excerpt/ID/span
evidence and unresolved associations. Reconstruction requires an actually
retained last candidate under a stated correctness assumption; actual valid
Prefix/Difference candidates, including wrong ones, supply the separate
privileged delta reference and preserved residual-error identity. Cleared,
invalid or unexecuted candidates never inherit earlier answers. The rubric and
six specified-view atlas witnesses are ready for the later freeze.

The [six retained information cases](../tests/fixtures/information_tables.json.gz)
reconstruct from original M3 workers under hash seed 37, retaining full unknown
main/stopped slots. The public saved-checkpoint decoder establishes final
acquisitions in the same read-only worker snapshot without saver setup or a
second store. All 160 prefix and 40 compact-boundary native history counts
reproduce using local metadata only. The integrated CPU regression passes 334
checks including all nine lifecycle checks; after the final narrow missingness/
numeric-association review, core/installed/focused checks pass 160 (two optional
skips)/81/26. See [T03 evidence](todos/M4/M4-T03-information-and-work-diagnostics.md#completion-and-handoff)
for versions, commands and review coverage. T04 remains ready, with costs,
uncertainty/missingness and the complete report gate still open. The scientific
specification/configuration/dependencies and all prior evidence are unchanged.
GPU/model/pilot/main execution and empirical findings remain unexecuted.

M4-T04 completes on 6 October 2026. Original generation/attempt and whole-policy
cost functions are shared with M3 live status; no duplicate store or new identity
system is added. Every continuation includes its original sixteen-call prefix
and all sixteen continuation calls, including F and exact mixed/Q uses. Outside
allocation overhead remains experiment overhead, with setup/interruption/attempt/
idle partitions and billing reconciled separately. Missing scheduled calls or
measurements remain explicit; a completed raw outcome without attempts cannot be
reported free.

The frozen rule uses recorded initial current ID/version coverage, including
tombstones and excluding pending values, to choose one entire C/K branch. It
cannot consult gold, candidates, later evidence or available-branch quality.
Unavailable selected branches remain unknown. Retained remote inventory excludes
the host-injected edited record; separate current completeness includes it.
Paired world/prefix/call/generation IDs and preservation denominators support
T05/T06 without splicing or utility ratios. Oracle-stable cost is retrospective
under the unchanged fixed schedule.

Twenty-eight focused checks pass. All sixteen original-worker cost cases
reconcile with M3, including full 60/40 manifests and stopped work, and reproduce
under hash seed 37. Both complete five-family fixtures select K in all 22 scopes;
constant-rule statements are explicit. The unchanged M3 accounting archive's
23 checks and nine evidence cases reproduce. Complete CPU regression at the
feature checkpoint passes 362 checks in 1,772.907 seconds, including all nine
lifecycle checks. The later inventory-only review passes final core checks
(191 run, 188 passed, three optional skips) and 110 installed-library checks,
with eight installed module paths/bytes asserted and CLI verified outside the
checkout. See [T04 evidence](todos/M4/M4-T04-policy-costs-and-boundary-rule.md#completion-and-handoff)
for exact commands, environment and retained artifacts.

That handoff left eighteen done, one ready and ten blocked. M4-T05 was ready;
T05/T06 and the complete report gate remained open. Scientific specification, configuration,
dependencies, all earlier fixtures and prerequisite evidence remain unchanged.
No GPU/model, pilot, main execution or publication occurred.

M4-T05 completes on 6 October 2026. Exactly 10,000 paired world-cluster draws
within eligible families retain equal-family means and original world/prefix IDs.
Saved nonnegative seeds and type-7 quantiles are explicit. Primary percentile
levels and range-correct weighted Hoeffding companions follow the specification.
Repeats remain conditional on the original prefix/partition and do not increase N.
Known failed replies remain zero; missing logical uses and trajectories remain
unknown through the frozen population. Shared response coefficients combine
before extrema, with tiny nonlinear completions enumerated and larger envelopes
conservatively labeled. Empty eligible populations remain N/A.

Exact family completion bounds and separately labeled complete-case displays
retain scheduled/executed coverage and unknown eligibility. Whole-policy
quality/preservation/cost displays use common paired worlds and draws; preservation
costs use preservation's eligible cohort. Shared original costs cancel before
bounds, missing future durations stay unbounded, and selected C/K identities
remain checked against the schedule. No optimizer, dependency, persistence or
scientific configuration was added.

All sixteen uncertainty cases reproduce from the unchanged original M3 workers,
including full 60/40 manifests, actual shared first-round cancellation and stopped
prefixes. Independent NumPy/SciPy references agree on 156 exact-binomial intervals,
six quantiles and an unequal-family bootstrap. Complete CPU regression passes
396 checks including all nine lifecycle checks; final focused/core/installed checks
pass 33/225 (221 passed, four optional skips)/144. The installed CLI runs outside
the checkout, nine installed module paths/bytes match final source, and hash-seed-37
reconstruction reproduces every retained table without changing worker bytes.
See [T05 evidence](todos/M4/M4-T05-uncertainty-and-missingness.md#completion-and-handoff)
for exact commands, environment and verification limits.

At that T05 handoff, progress was nineteen done, one ready and nine blocked.
M4-T06 was ready; its full report/CPU gate remained open. Specification, configuration,
dependencies, earlier fixtures and prerequisite evidence remain unchanged.
No GPU/model, pilot, main execution or publication occurred.

M4-T06 completes on 6 October 2026 and closes M4's CPU gate. One read-only
worker snapshot supplies all scientific tables, exact raw replies, rendered
requests and branch-local prose deliveries. Seven explicit exhibits and
at most six exact-rational median cases retain absent signs, unknowns and fixed
populations. Illustration completeness includes every scheduled slot in the
supplied scope, with failures/controls/repeats recorded; selecting contrasts
and card joins both use replicate zero. Invalid non-scalar raw text remains
unchanged, using reversible JSON string notation in HTML.

Actual controls use one rendered request and prose deliveries use the original
sender ID for their branch join. Visual review separated paired differences
from absolute quality/cost axes and added explicit control counts; scientific
tables are unchanged. All seven exhibits and incomplete/stopped views were
inspected. Optional Matplotlib reads saved plotting inputs, with deterministic
SVG/PNG bytes in the recorded plotting environment, without reading workers
or resampling analysis. It is the only new optional dependency.

All sixteen original-worker scopes reproduce every M4 table, case, plotting
input, trace/input snapshot and export byte twice. This passes both current
source and installed hash-seed-37 validation with inference/execution/plotting
imports blocked, leaving original worker bytes unchanged. Five portable
reports retain 126 files, including 35 SVG and 35 PNG exhibits. Full main
joins retain 15,486/10,390 unknowns, original 60/40 denominators and only five
observed worlds; stopped work retains sixteen unknowns and unavailable cases.
These are synthetic validation, not experimental findings.

Full source regression passes all 424 checks in 2,479.221 seconds, including
all nine lifecycle checks and eleven real controller kills. Focused/core/installed
checks pass 25/252 (244 passed, eight optional skips)/166. Twelve installed
module paths/bytes match current source; the installed CLI preserves 1,178
unknown development slots and output exclusivity while rendering all seven
exhibits. Eight renewed native capacity checks retain target/fallback bounds
261,388/259,868 including reserve. The [22-row/seven-category CPU audit](validation/m4-cpu-gate.md)
passes and names the remaining M5/M6 portions explicitly. Exact commands,
environment, times and artifact links are in the
[T06 completion](todos/M4/M4-T06-reproducible-report-and-cpu-gate.md#completion-and-m4-gate).

At that T06 handoff, progress was twenty done, one ready and eight blocked.
M1–M4 CPU gates passed and M5-T01 was ready for CPU preparation. Case/annotation
rules, analysis settings and assumptions are ready for M5's future accepted bundle. M6-T02 still requires
an actual-execution or documented terminal-feasibility handoff. Scientific
specification/configuration, mandatory dependencies, execution/scoring modules,
prerequisite task evidence and all prior fixtures remain unchanged. No GPU
allocation, language weights, model inference, pilot, main experiment,
accepted freeze or publication occurred.

M5-T01 completes on 7 October 2026 on Windows/CPU. The direct native text-only
adapter verifies every language weight/device/precision, retains exact raw
suffix IDs/text, supplies fresh KV/recurrent state and saves per-call CPU/CUDA
seeds. Loading evidence and call instrumentation use the existing process and
attempt records. Final review rejects numerically equal but differently typed
settings/token records and conflicting, missing or duplicate worker/factory
devices before work.
These are CPU/static/mock checks, not observed GPU loading or generation.

The full 449-check regression passes at the backend checkpoint, including every
prior archive, original-worker report reproduction and all nine lifecycle cases.
Final focused and installed checks pass 27/41 after the identity review; core
runs 260 (252 passed, eight optional skips), and native 9B/4B metadata checks pass
four each. Eight renewed capacity checks retain 261,388/259,868 with reserve.
The [task evidence](todos/M5/M5-T01-inference-and-allocation-preparation.md#completion-and-handoff)
states exact environments, commands, revision timing and verification limits.
The specification, study configuration and all 26 prior data fixtures remain
unchanged; no weights, GPU work, accepted freeze or empirical result exists.

The user selected a [proposed private Kaggle T4-x2 plan](validation/m5-inference-preparation.md).
At most 24 smoke attempts, loading, idle second GPU and shutdown are admitted
under a 0.5 aggregate GPU-hour ceiling, with a 120-wall-second safe-stop allowance
and the existing shared 8/2/2-hour reserves. Provider/account facts, exact request
materialization, durable off-host export and confirmed release remain pending
T02 preflight. Progress is twenty-one done and eight blocked, with no active or
ready task. T02's preparation dependency is satisfied; the actual hardware/host
gate and prepared scope for model execution remain required. M5's operational gate stays
open; capability, complete pilot and measured whole-schedule admission follow.

On 8 October the user supplied CPU notebook metadata (Python 3.13, CPU-only
torch, missing bitsandbytes/SQLite saver, 19.5 GiB free disk) and chose GPU-host
preparation with available quota. The [follow-up](validation/m5-kaggle-preflight.md)
provides a portable source/tokenizer export and a brief device/package/disk cell
before CUDA selection. The GPU image may differ from the reported CPU image.
Hardware inspection can precede exact smoke request preparation; all allocated
inspection and host checks remain inside the existing smoke/development limits.
The required exact requests and candidate host checks still precede model loading.
Actual GPU output, accepted storage and measured smoke remain pending; T02 stays blocked.

The user then requested the actual notebook and detailed preparation planning.
The [Kaggle notebook](../notebooks/recovery_m5_kaggle_preflight.ipynb) supplies
fixed defaults, private-input discovery, isolated candidate installation,
device/loader/protocol/SQLite/storage checks and one recoverable results ZIP.
The [notebook plan/evidence](validation/m5-kaggle-notebook-plan.md#completion-evidence)
records 22 controlled workflow checks, a real nine-cell Windows/CPU Jupyter
execution and 81 focused plus 16 native checks from its source export. The
focused setup-command bound is 360 seconds after a measured 258.460-second
Windows run; model timeout/settings and the common workflow/smoke limits are
unchanged. The current checkout lacks usable Git metadata and four top-level
project files; the supplied committed ZIP remains the source snapshot. No
recovery/scientific code changed, no missing files were restored, and no Kaggle
execution or model admission is claimed.

On return of the executed notebook, the [first-run review](planning/m5-kaggle-first-run/01-first-run-evidence.md)
confirmed two T4s/CUDA-enabled Torch and one source-admission failure. Candidate
installation and native tests skipped; weights and model calls remain unexecuted.
The authorized [CPU upload canary](validation/m5-kaggle-upload-canary.md) now
implements the small R1/R2 diagnostic. Twelve focused checks and actual local
Jupyter valid/missing-input cases pass, with readable exports. A verified
isolated sparse checkout supports logical commits while preserving original
workspace metadata and evidence. The [returned actual Kaggle CPU canary](validation/m5-kaggle-upload-canary-run-2.md)
now passes all five stages and off-host SQLite checks. Its original-dataset
inventory finds all 14 gzip and two nested ZIP paths absent with exposed
counterparts, explaining the first failure. Raw `.payload` transport is selected
for full-source delivery; dataset version and release timestamps remain unavailable.

K2–K7 implementation is delivered in the [full CPU preparation packet](validation/m5-kaggle-full-preparation.md).
The [actual run 3](validation/m5-kaggle-full-preparation-run-3.md) verifies all
143 original source members, Linux/Python 3.13 CPU inspection, owned-process
timeout cleanup and synthetic off-host backups. Candidate setup fails inside
`ensurepip` before installation/provenance and all 81 focused/16 native checks.
K8 has partial actual evidence; K4/K8/K9 acceptance remains open.

The [narrow bootstrap repair and v3 handoff](validation/m5-kaggle-pip-bootstrap-repair.md)
pass 25 operational checks, a real local isolated pinned-pip installation and
exact-v3 Jupyter valid/missing-source exports. The eleven roots and 88-package
candidate remain unchanged. Next reuse the accepted private `m5-kaggle-source-v2`
dataset, import v3 with Accelerator None / Internet On, and return notebook/ZIP
under `notebooks/run/4/` after stopping the session. No new upload or repeat
canary is required. Actual Linux candidate installation/checks, GPU/model gates
and later work remain open; scientific code/configuration, resource ceilings
and task counts are unchanged at twenty-one done/eight blocked. User-authorized
Git/root-file recovery is complete with verified preservation; new logical
commits use the main workspace, while the earlier isolated checkout is retained.

The subsequent [manual Kaggle bootstrap result](validation/m5-kaggle-pip-bootstrap-repair.md)
reports pip 26.2.1 successfully installed inside the new venv on Python 3.13.
Its unlocated `sitecustomize`/missing-`wrapt` warning is retained alongside that
success. This checks the narrow bypass on the actual host; the complete v3
candidate install/provenance and 81/16 checks remain unexecuted, with unchanged
package pins, scientific gates and task statuses.

### Unresolved issues

| Issue | Smallest resolving step / decision evidence |
|---|---|
| Persistence and crash safety in the accepted inference host | M3-T05 passes on Windows/CPU; repeat the checkpoint/SQLite/process/backup checks in M5's accepted host lock and actual storage environment before inference admission |
| Passing model/runtime/timeout and device headroom at the revised context | M5 maintained-loader diagnostics and bounded smoke/pilot, including the complete admitted input envelope. Static full-attention FP16 KV alone is 8 GiB at 262,144; weights/activations/workspace and 1.5 GiB headroom are additional. CPU admission is not T4 feasibility. |
| 9B/4B, target/fallback size, 60/40 worlds | M5 capability and complete-schedule allocation evidence, following the specified precedence and shared development limit |
| Compute provider availability, persistence and allocation rules | [T01's proposed private Kaggle packet](validation/m5-inference-preparation.md) defines two-device charging, ceilings, shutdown allowance and local/off-host backup destinations. Record actual account terms before assignment, then capture device identities in the brief host inspection. Accepted-host storage/export and the confirmed release mechanism must pass before model loading. Provider choice cannot alter experimental semantics. |

### Final outcome / retrospective

Pending. Record the accepted configuration and achieved coverage, artifact location, reproduction result, consequential deviations, total resources, and remaining limitations. Distinguish a completed study from feasibility failure or documented incompletion.

The [actual run-4 review](validation/m5-kaggle-full-preparation-run-4.md)
accepts complete source/cleanup, all 88 candidate installs and project build.
The installed probe exits zero and independently verifies all 28 module hashes,
but documentation messages precede its JSON and block the reader plus all 97
checks. The [dedicated-output repair and continuation](validation/m5-kaggle-probe-output-repair.md)
pass 27 focused checks and real Jupyter wiring with controlled candidate outcomes.
The user kept the session open and returned the successful continuation under
`notebooks/run/5/`. The [actual run-5 review](validation/m5-kaggle-full-preparation-run-5.md)
passes all 97 checks with zero skips, the dedicated provenance file, eight
clean owned-command exits and both independent off-host SQLite copies. It
takes 319.030 CPU seconds and repeats no download/install. This closes the CPU
portion of K4/K8 and K9's CPU evidence review; GPU-specific K8 requirements remain
open. No further CPU preflight is requested. Run 6 subsequently accepts the
standalone tiny-library portion. Next resolve [K10's supported model attention
and full-envelope gates](planning/m5-kaggle-first-run/04-model-feasibility-and-smoke.md)
before verified model assets, exact 24 smoke requests and attempt/allocation
admission. A model-smoke notebook is not yet ready. Full-candidate GPU/model/pilot/freeze
gates remain open; existing GPU authorization, scientific/package/resource
semantics and twenty-one done/eight blocked statuses are unchanged. Original
failed results and the successful continuation remain retained separately.

The [actual run-6 review](validation/m5-t4-compatibility-run-6.md) independently
accepts all six stages, four clean exits, 14 attention cases/four NF4 matmuls,
85 staged wheel files, distinct physical UUIDs and both off-host snapshots.
The supplied notebook/ZIP are retained unchanged under `notebooks/run/6/`.
Observed workflow time is 38.664 seconds, a lower bound on assigned time. The
user reports the GPU session stopped; exact duration/provider timestamps and
earlier spending remain unknown. No repeat is needed or requested. Preserve
that uncertainty within the unchanged shared limits; the conditional notebook
ceiling is not a verified total or fresh allowance.

Next perform offline supported model-attention and R7 memory review. Tiny
efficient dispatch is not a full-context memory proof, especially with a
fully materialized repeated-K/V temporary and the lower observed native total.
Later full-candidate staging/host checks, model assets, 24 exact requests and
attempt/allocation admission still precede smoke. T02 and all dependent gates
remain blocked with twenty-one done/eight blocked; no backend/scientific,
fallback, package, cap or frozen setting changes and no model generations.
