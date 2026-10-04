# Untapped scientific structure in the existing study

Status: protocol-grounded analysis, 2026-10-04. Executed CPU evidence is separated from hypotheses in [the audit](evidence/PROTOCOL_AUDIT.md). The existing PS remains authoritative and unchanged.

## The main opportunity is finer questions about retained work

The original four policies isolate meaningful packages: correction dissemination, current source acquisition, and retained derived history. They leave several distinct resources bundled inside “reasoning”: previous candidate answers, free-form peer explanations, own outgoing proposals, validation history, and historical facts mentioned inside any of these. Adding every resource as an arm would be unaffordable. The useful next step is to discover a principled distinction that changes a concrete runtime decision.

The current design already permits that work without altering task families, peers, branch matching, exact scoring, or the primary sham-adjusted reset contrast. Its strongest unused assets are the identity and timing of delivered source records, typed prior candidates, known source replacement operations, the difference between local and replicated output assignments, and exact before/after task functions.

## 1. A revision has both a new state and a transition

The active table stores version 2; version 1 disappears. A version-1 value can remain in B's derived history but cannot be relied on. In C it disappears unless inferable from current evidence. A correction payload saying “record i now equals 4” and a payload saying “record i changed from 1 to 4” supply different inputs to incremental computation.

This is not simply extra current evidence. The before-value is historical evidence about what was computed, and its legitimate use need not assert that it is still current. Such information can replace a long old narrative with one exact transition operand. The PS's stable IDs, versioning, and immutable prefix already make this operation feasible without semantic dependency extraction or an LLM reviewer.

The information distinction is proved by constructive pairs in the audit. It is not universal: correct complete difference outputs plus unchanged private anchors recover the missing before-value. Max/top-K and BFS can remain insufficient even with old/new payloads because the old result omitted a reserve candidate or alternative route. Sort has a separate distributed boundary-transfer requirement.

An eventual test should keep before-values in a distinctly typed historical event record, never in the current source table, and never let host code compute answer deltas. Giving historical facts to previously unexposed peers is an explicit dissemination change. Gains must be attributed to this information payload, not to superior hidden reasoning or a new incremental algorithm.

## 2. Output compression determines what work is recoverable

Let `f(x)` be the task answer and `S_p(x)` the typed previous answer retained at peer p. For evidence view `E_p` and edit payload `e`, define the compatible revised-answer set

`Omega_p(S,E,e) = { f_p(x') : x agrees with S and E; applying e yields x' }`.

This is a conceptual/evaluator-only object. If it has at least two elements, the view alone cannot guarantee the revised output. If it is a singleton, a correct updater exists in principle; that does not mean the bounded model can find it. Model-generated candidates are not guaranteed equal to `S_p(x)`, and assumptions of correctness belong in theoretical statements, not policy code.

| Family | What a correct old answer retains | What may still be missing |
|---|---|---|
| Max | Winning value | Replacement competitor after lowering the winner. |
| Top-K | Selected multiset | First omitted reserve and source-ID/value association. |
| Prefix | Local cumulative coordinates | Before-value of a remote edited source or hidden incoming offset; explicit delta resolves the arithmetic. |
| Difference | Complete differences | Only a global additive constant, fixed by any unchanged own source. |
| Sort | Each peer's rank segment | Cross-segment donor values; even full multiset loses source-ID/value mapping without a before-value. |
| BFS | Distance labels | Alternative edges/path structure and their distribution. |

This mapping is a better scientific explanation than treating SILO levels as increasing complexity. However, it is not a causal task-family variable: arithmetic, output length, replication, and information acquisition still differ. A theory-informed descriptor can explain results; six heterogeneous families cannot establish a universal recovery law.

## 3. Communication history contains a temporal exposure graph

The host knows which sources each call saw, which prior generated objects remained in context, and which messages were delivered before each call. It can conservatively mark all generated objects from a call as potentially influenced by an exposed old source. Carry those labels through later history and messages. This is standard conservative information flow applied to the observed call graph, not semantic provenance.

An offline study can report:

- The fraction of old derived objects/tokens outside the revised source's temporal exposure cone.
- The number of peers whose complete retained derived history has no path from it.
- When that cone first reaches each peer, including round-four messages received after the last prefix generation.
- Raw-source acquisition breadth separately from derived-object exposure breadth.
- Their joint distribution with exact semantic footprint size and replicated output copies.

Use **possible influence**, not contamination, for this graph. A precise semantic footprint can be tiny while the conservative cone is broad, or large while a sparse history remains unexposed. The executed routing probe proves temporal ordering matters and also defeats the assertion that four rounds necessarily saturate every cone.

The qualification matters: this envelope is conservative for dependence through actual delivered contents and retained objects under the specified exposure model. It is not automatically conservative for every implicit channel. A peer can react to a missing expected message; sender/recipient and evidence-selection choices can depend on old information. Bounding every counterfactual absence/control channel requires additional assumptions or a substantially broader graph. State the chosen channel model explicitly and avoid an unconditional noninterference claim.

An actual partial-reset policy would clear only derived objects with a potential path while keeping B/C's exact current source tables. It requires controls against same-volume arbitrary history deletion and any simple age-based truncation. Without these controls, improvement may be ordinary context reduction. It cannot guarantee full causal independence because retained evidence selection still depends on prior work. Already-known causal rollback and taint systems are direct novelty threats.

## 4. Trustworthy raw values can carry stale selection decisions

The source table authenticates contents, not completeness. Suppose a peer saw an old cutoff and therefore forwarded only records above it. Following a correction, every retained raw record may be current while useful omitted records remain unavailable. No content-level stale fact remains, but old search decisions still shape recovery.

This is a natural bridge to the previous completion investigation without adopting its redirection. The existing max/top-K edits already lower winners and can require formerly omitted reserves. The current protocol keeps peers active, so no new `done` lifecycle is needed to ask whether old evidence acquisition choices delay recovery. Record how many new raw records are acquired after the change, and whether the changed answer requires information absent at the boundary. Do not use offline necessity labels to route the runtime.

A critical limitation: raw-source insufficiency is not full-context insufficiency. A prose summary may already contain the needed reserve. An offline record-only metric cannot certify that reacquisition was necessary for B. Use exact statement-level provenance only where existing typed records support it; do not invent a semantic parser merely to save this metric.

## 5. Sources, computations, and narratives have separate causal roles

The latest typed candidate is a pre-existing bounded artifact. Retaining only it in addition to C's current evidence is a clean middle state between C and B. It could preserve calculation while discarding the surrounding narrative. It could also preserve exactly the most influential stale object. Its production adds no prefix calls and selecting the latest valid candidate requires no oracle.

This is a useful baseline, not automatically a new method. Recent answer-only versus rationale-retention literature must be treated as a direct threat. Its most defensible role here is to test theoretical information limits or distinguish useful computed output from harmful discourse, with a sham counterpart. No gold-filtered candidate admission or output-coordinate selective patching is allowed.

## 6. The original diagnostics can answer stronger boundary questions

The PS already distinguishes changed and unchanged coordinates, old-gold retention, new correctness, and regressions. Several scientifically useful results cost no new inference:

- Does broader prior exposure coincide with a larger *paired* reset benefit after accounting for family and pre-event accuracy? Treat this as exploratory effect heterogeneity, not randomized causation.
- Does exposure breadth become almost constant in natural successful prefixes, destroying its usefulness as a selective-policy signal? A saturated signal is a useful negative result.
- Does reset lose the information needed for cheap correction while preserving enough current evidence to recompute from scratch? Transition-payload experiments can isolate part of this question.
- Do peers first become correct and then revert to an old value after receiving a retained-history peer message? The temporal trace identifies candidate episodes, but correlation alone cannot prove the message caused the regression.
- Is the saved evidence small enough that F and C have effectively identical views? Then lack of C–F benefit has a concrete mechanistic boundary.

Avoid large moderator regressions with 36–48 world clusters. Predeclare one or two descriptors, show paired plots and raw counts, and report them as exploratory unless an intervention supplies causal identification.

## 7. Interventions that require a higher bar

Delayed stale messages, asynchronous races, membership insertions, repeated corrections, task changes, and stopped-task reopening are important runtime problems, but PS intentionally excludes them. Introducing them changes the problem being studied and often requires new lifecycle rules. The previous investigation already found strong precedents in epoch fencing, control/membership invalidation, and revised completion protocols. They should not displace the clean current study just because they look more systems-oriented.

Likewise, oracle footprint-aware deletion, exact semantic validators, and hand-authored dependency graphs would make selectivity easier by supplying the information whose absence is the research difficulty. They are permissible evaluator diagnostics only when labeled; they cannot serve as an unprivileged runtime policy.

## Priority from structural evidence alone

The strongest near-term additions to investigate are (a) the difference between replacement payloads and explicit historical transitions, and (b) the limits of selective retention from observed information flow. The former changes a tiny real runtime input; the latter can yield a substantive boundary result at zero extra inference cost. Their literature novelty and pilot value remain undecided. Candidate-only retention belongs as a demanding simple baseline. Completion reopening remains a competitor with a stronger interface change and greater departure from the six-task PS, not the assumed destination.
