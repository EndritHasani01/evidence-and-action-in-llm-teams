# Practical roadmap for the proposed thesis extension

**18 October 2026 · prospective, not adopted or executed**

Implement only after approval of the [experimental design](../proposals/thesis-extension-2026-10-18.md).
The [evidence review](../analysis/thesis-extension-evidence-review.md) separates
existing implementation/verification from new work. The current specification,
course freezes, defaults, and artifacts retain their authority meanwhile.

## 1. Small implementation strategy

Extend the two-agent I-01 path. Reuse its exact actions, private finality,
waiting/deadlock rules, one admission owner, worker stores, physical attempt
ledger, raw-before-effects transactions, process termination, portable backups,
and read-only report projections. Reuse original-thesis mathematical/statistical
helpers where their contracts fit, rather than importing its entire runner.

| Preserve/reuse | Necessary change after approval | Explicitly exclude |
|---|---|---|
| `i01/core.py` action validator and state transition | New event-aware permitted view: non-prefix no longer automatically means revised data; explicit sham reopening and controlled-packet start | Solver-assisted validation, public partner submissions, extra turns, reopened premature commitments |
| Existing max generation/oracle and stable IDs | Separate controlled/natural cohorts, nested 128/96 size, preserving edit and trial schedules | New hash identity scheme, favorable-prefix selection, family replacement |
| `i01/store.py`, `process.py`, `runtime.py`, `archive.py` | Scope-aware admission ceilings and model/event/packet/trial call IDs; retain exact integer seeds and original failure/unknown accounting | Additional outcome store, handoff service, generalized experiment registry |
| Existing literal history and assisted renderer | Fixed historical reports/conclusion fields; same HS/HSC source bytes; no-change notice; condition-blind common task instructions | Semantic extraction from natural prose, learned summaries, continuous compression |
| Direct NF4/FP16 Qwen implementation | Two explicit model paths, model-specific templates/EOS/load audits; common request/outcome contract | Assuming changing the model ID is sufficient; applying Qwen's attention/recurrent adapter to Granite |
| Cost/outcome/figure/report code | Six-cell repeated outcomes, world means, primary interactions, preserving subset and separately labelled natural bridge | Agent-action pseudoreplication, best-trial outcome, pooled course results |
| Finite notebook cells and verified export | A thin interface to prepare, inspect, run one approved bounded stage, report and export | A new notebook framework or automatic advancement across authorization boundaries |

Keep the new regime explicit. Do not loosen old `ProtocolLimits`, `Candidate`,
source-binding guards, or old report interpretation globally to admit it. Add
the smallest scoped handling for the adopted new contract. Two named backend
paths are enough; a model registry/factory hierarchy is not justified. Verify
the existing course behavior at affected seams rather than redesigning it.

## 2. Dependency-ordered work and concrete acceptance

### T0 — Adopt the scoped scientific amendment

**Input:** user's approval of the design and authorization for deterministic
implementation. **Output:** a new specification section referencing the exact
population, packets, event rules, prompts, repeats, endpoints, model/decoding
conditions, stage ceilings, resource decision, and approval boundaries.

Keep §§1–12.1 and their artifacts unchanged in meaning. Update only current
handoff/navigation sections to explain the new scope. Create no main manifest
before the generation/schedule rules are adopted. Record that the proposed 200
hours are additional prospective extension resources, not a claim that historical
programme usage is known or reset. Implementation approval authorizes no GPU
stage, paid booking, main inference, freeze change, or publication.

**Acceptance:** every row of the design's amendment table has an explicit new
rule/precedence statement; no implied fallback or deferred choice changes the
primary design. A clean task-owned checkpoint makes adoption reviewable.

### T1 — Inputs, scripted histories, and exact schedule

Generate/save six qualification, twelve development, 128 target controlled, and
32 disjoint natural worlds, with the adopted nested 96 fallback and 32 preserving
subset. Use existing seed/ID primitives and saved arrays. Keep math eligibility,
owner/first-speaker balance, rejection caps, and overlap checks explicit. The
controlled/preserving shared worlds are intentional; other cohorts are disjoint.

Construct the three-call scripted prefix using only locally available data.
Keep reports separate from final submission text from the start. Build H0/HS/HSC
packets once and save their exact contents/provenance as fixture inputs. Scripted
steps must never appear as physically executed model calls or consume fabricated
attempts. Natural histories remain actual literal records, including errors.

Physical call IDs include model, event, packet, and trial; the **matched sampling seed**
stream is keyed by world/model/trial/agent/invocation and shared across the
six cells within that trial. Trial streams are independent. Save resolved seed
integers directly; do not depend on a floating-point renderer to reconstruct them.
Model-specific streams make no claim of cross-tokenizer random-draw equality.

**Acceptance:** independent max/edit checks; exact scalar gold before/after;
lawful script under both first speakers; correct private visibility; zero
conclusion sentences in report fields; byte-identical HS/HSC report blocks;
no revised remote payload, future edit, hidden eligibility, or condition label;
all world/call IDs unique and all stage totals reconcile. Target main upper
bound must be 22,208, fallback 17,472, initial development 1,112, reload allowance
80, contingency 600, whole target cap 24,000. Unused capacity adds no scope.

### T2 — Event-aware episodes, rendering, and persistence

Implement controlled starts, sham reopening, the preserving event, and explicit
natural retain/clear starts. Current shards and event notices are outside
clearable history. Each sibling/trial deep-deserializes the right immutable
starting snapshot. Apply the event once. No hidden model handle crosses calls.

Retain the current scheduler's finality, waiting, private answers, terminal
reasons, and invalid-action effects. A known invalid outcome delivers nothing
and consumes a turn; a failed slot cannot inherit an earlier answer. Do not
implement packet conditions by rewriting natural histories after scoring.

**Acceptance:** focused deterministic cases for actual edit versus sham data;
matching reopening flags/counters/status; send-and-submit delivery; wait after
partner finality; illegal message-plus-wait; exhausted/deadlocked completion;
sibling independence; exact persisted valid/invalid resume; interruption before
and after raw persistence/commit; one bounded infrastructure retry; unresolved
spending block; export/restore of both controlled and natural records. Reuse
existing crash cases; add only counterexamples for changed behavior.

### T3 — Two native model boundaries and complete token capacity

Audit the pinned Qwen and Granite configs, tokenizer/template, chat framing,
EOS/pad/BOS, raw suffix decoding, direct mode and generation settings. Render
all archived reports/actions as labelled user data, avoiding native assistant
history rewriting. Preserve raw tokens/text separately from parsed actions.
Pin one maintained environment that supports both if feasible; separate locks
are acceptable only if required and disclosed, not as a hidden policy change.

Check all candidate requests, legal scripts, longest task/source fields, and
the full permitted post-boundary history, including feedback and the largest
legal strings. Both models must fit **8,192 input plus 512 output**, without
silent truncation, best-history selection, or uncharged repair calls. Previous
Qwen I-01 token proofs are prerequisites to reuse, not a proof for new packets
or the Granite vocabulary. If the complete bound fails, stop for a specific
prospective amendment; do not quietly shrink text during GPU execution.

**Acceptance:** tokenizer-only checks and a conservative complete envelope for
each model; useful indexed-shard script messages fit the output cap; exact
request/settings/seed reconstruction; model-specific stop-token handling;
no numerical feedback or unwanted default thinking. This stage loads no weights
and makes no GPU call. Old source/release guards remain intact.

### T4 — Analysis ready before model data

Extend existing read-only outcome/cost exports. Compute each world/cell's two-trial
mean, two primary model-specific interactions, direct source/conclusion contrasts,
both-trial consistency, preserving subset, and natural bridge separately. Carry
both models, all cells, and trials together in four-stratum world resampling.
Use the newly adopted type-7 97.5% primary/95% descriptive intervals, preserving
historical index conventions in older reports.

**Acceptance:** hand-scored examples for positive/negative/zero interaction;
a positive interaction produced only by sham benefit; source help with no
conclusion effect; one correct trial versus two; fast terminal failure; unknown
cells and their bounds; a degenerate bootstrap with bounded companion; exact
64-bit seed round-trip; physical versus logical prefix cost. A complete and a
stopped tiny scripted study must reproduce after export/restore without a model.
Do not add a generic statistics service or mirror every implementation line in
a test. Run focused changed-behavior checks and required preservation checks.

### T5 — Deliver an inspectable preparation packet

Use existing package/source capture, CLI, thin notebook, checkpoints, and reports.
Keep stage scopes finite and idempotent. Expose actual calls/limits, retained
starting packets, both model identities, terminal reasons, unknowns, and download
locations. Existing controller ownership remains the single spending authority
across active worker files; CSV/HTML/Markdown are derived projections.

**Acceptance:** isolated installed-package smoke outside the checkout; exact
source/environment binding; quiescent ZIP/extracted restore and continuation;
zero model calls on completed-stage rerun; shutdown/export reserve behavior;
one complete tiny CPU scripted lifecycle; unchanged historical artifacts and
legacy targeted behavior. Avoid repeating unrelated broad M1–M4 suites or
repackaging old evidence solely to obtain new green counts.

**Implementation checkpoint:** list changed behavior, named checks actually run,
source identity, prepared artifacts, remaining GPU gates, and the precise bounded
next action. Passing this checkpoint is not inference authorization.

### T6 — Separately authorized hardware, qualification, and development

Before approval, prepare the exact host/model/call plan and current account
limits, expected cost, persistence/export arrangements, and measured remaining
allowance. No resource booking is implicit. At most 556 initial first-attempt
slots per model are planned:

| Stage per model | Maximum | Pass condition before dependent spending |
|---|---:|---|
| Initial current-load A/B/A state checks and full envelopes | 8 | Correct isolation replies, finite scores, correct loading/device map, complete 8,704-token resident envelope, ≥1.5 GiB free headroom on each used device |
| Six qualification worlds, original/revised scalar controls | 12 | All actions legal/committed; at least 11/12 exact |
| Supplied-view local/source/commitment diagnostics | 8 | All actions legal/committed; at least 7/8 exact predefined behavioral targets |
| Twelve development worlds: six controlled cells once, two controls, one natural original | 528 | Execute all fixed scopes; controlled team actions ≥98% legal, controls ≥22/24 exact, HS sham ≥9/12 and HSC sham ≥9/12; complete durable evidence/exports and adequate resources |
| **Initial total** | **556** | No gate on memory-effect direction, withdrawal success, H0 success, or natural-prefix correctness |

Preparation may use fewer calls when only one device is active, but unused slots
do not license new diagnostics. Extra unchanged-runtime readiness is four calls
per reloaded replica (A/B/A and one forced-length envelope), at most 80 across
the campaign. Ten two-replica reload cycles is an accounting equivalent, not
a guarantee that ten sessions suffice. Plan model/device rotation and session
count against that allowance before main authorization.

Start with load/direct/termination/export limits 600/180/5/120 seconds as
provisional course-derived bounds. Accept or revise adequate measured deadlines
prospectively before freeze, without resampling already recorded scientific
outcomes. Full envelopes force output reserve only in hardware diagnostics;
ordinary scientific calls stop normally. All failures, reloads, retries, unknown
exposure and idle allocation count. A resource/integrity failure stops dependent
dispatch; ordinary wrong pilot outcomes remain recorded and determine only the
predeclared usefulness gate.

The 16-hour development reserve covers both models, not each. No candidate
search or automatic thinking/model/backend fallback is selected. A required
behavioral revision after these results is a new development version with fresh
validation data and explicit authorization. Do not relax a threshold in place.

### T7 — Freeze the complete scope and request main authorization

Use the complete cost formula and **both** models' measured times. Select 128
controlled worlds if the conservative total fits 200 aggregate GPU-hours;
otherwise the fixed 96 if it fits; otherwise stop. Keep the preserving and
natural scopes, both trials, all memory cells, and both models. Preserve previous
spent/unknown resources; do not create a fresh allowance by changing run paths.

**Acceptance:** both models pass; no unresolved privacy/numerical/process/storage
fault; exact dependency locks/source/templates; complete input/order/seed manifests;
frozen rubric/statistics; forecast including allocated idle time, loading,
requalification, checkpoints, exports and 25% main margin; actual session/quota
and restore plan; sufficient remaining attempts/hours. Reconcile common-unit
timings so generation overhead is not counted twice as setup.

Present the accepted target/fallback, remaining worst-case calls, estimated and
maximum allocation, actual provider cost if paid, affected output location,
and stop/restore procedure. **Only the user's subsequent main authorization
permits execution.** Do not equate a recorded freeze or an objective gate pass
with that authorization.

### T8 — Complete, audit, and write the thesis

Execute balanced saved blocks with checkpoints, preserving every intended world
and trial. Ordinary wrong/illegal/unfinished outcomes never select later worlds.
Integrity/resource stops retain a truthful partial export; resume settled calls
exactly. Independent final reconstruction uses canonical manifests and stores,
not only generated summaries or printed seed labels.

Required final exhibits: six main cell rates by model; direct contrasts and two
primary interactions with raw world patterns; both-trial consistency; completion
and correct/wrong/absent commitments; the preserving check; the natural bridge;
quality/effort side by side; exact coverage and unknown bounds; and a small
trace-linked casebook. No need for a catalogue of generic plots or extra reports.

**Acceptance:** manifest/attempt/coverage reconciliation; independent score,
interval and cost reproduction; preserved original artifacts; inspectable raw
requests/responses/effects; honest limitations and protocol deviations. Thesis
writing and private review can follow; publication or public artifact release
requires separate authorization and a concrete reviewed package.

## 3. Effort and authorization summary

A realistic implementation planning allowance is roughly **10–17 focused working
days**: adoption/inputs 2–3; event/state/rendering 2–4; native model boundary and
capacity 2–4; analysis/reporting and installed delivery 3–4; final review 1–2.
Work overlaps, and Granite compatibility may invalidate the estimate. This is
engineering planning, not a measured completion promise. GPU development and
main sessions follow separate gates and add elapsed time.

| Decision | What an approval would authorize | What remains separate |
|---|---|---|
| Approve design/implementation | Scoped specification adoption, code changes, deterministic/tokenizer verification, prepared source/notebook artifacts | All GPU/model calls, paid compute, main inference |
| Approve bounded preparation | The named hardware/qualification/development scopes, limits and actual host | Main inference; scientific retuning; additional resource purchases |
| Approve measured main plan | The frozen complete target or fallback within remaining caps | Extra worlds/trials, changed configuration, publication |
| Approve publication | The reviewed thesis/artifact package and named destination | Destructive remote operations or deletion of important evidence |

**Next decision:** approve the recommended scientific amendment and T0–T5
deterministic implementation. No execution authorization is requested by the
existence of this roadmap, and no implementation has begun in this session.
