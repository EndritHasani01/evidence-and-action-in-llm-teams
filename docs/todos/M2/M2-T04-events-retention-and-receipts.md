# M2-T04 — Literal events, retention boundaries and receipts

**Status:** done

**Dependencies:** [M2-T03](../M2/M2-T03-synchronous-rounds-and-prefixes.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2 differential checks](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§2.3](../../../PROJECT_SPECIFICATION.md#23-events-and-populations), [§4.1](../../../PROJECT_SPECIFICATION.md#41-what-each-peer-retains), [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), and [§4.3](../../../PROJECT_SPECIFICATION.md#43-historical-information--retained-representation).
- Technical evidence: [state boundaries](../../implementation-research/state-and-replay.md#semantics-that-belong-to-the-application).

## Intended outcome

Each event and retention policy creates exactly its prescribed starting state from a fresh copy of the original drained prefix.

## Scope and boundaries

- Use explicit small policy cases and deterministic transformations, not a generalized intervention language.
- Main revision and preserving revision invalidate v1 everywhere, publish the same permitted persistent notice and deliver v2 according to L/broadcast. Unknown v2 remains pending; BFS tombstone endpoints are hidden until content delivery.
- Sham keeps all sources unchanged and gives every peer the same neutral continue-solving notice.
- B retains derived work. C clears history, candidate and feedback. K retains exactly its own protocol-valid prefix-round-four candidate, even if wrong, or an absence marker. F clears derived work and acquired remote sources while keeping its corrected private shard and broadcast revision.
- Mixed masks use the corresponding B/C boundary per peer. Initial B/C/K/mask current sources are identical within an event; C/F differ only in retained acquired remote evidence.
- BΔ/CΔ/KΔ add genuine archived before-values with changed ID/owner/versions/public position outside current lookup. Ordinary receipts say "not included in this receipt", without claiming the value is absent everywhere. Current v2 content is identical across receipt modes.
- Never include a computed delta, formula, footprint, corrected candidate or extra unchanged record in receipts. All policies accumulate ordinary new history after the boundary; K is not continual compression.

## Completion criteria

- Every policy/event/subset uses the original prefix, including preserving siblings and repeats.
- Transformations preserve the parent and all siblings, notices/receipts survive clearing, and source updates never rewrite a candidate.
- Boundary application is identifiable for later apply-once checkpoint integration.
- Receipt contrasts change only the specified disclosure package and record its actual token cost.

## Validation and evidence

Run the plan's L/B, B/C/K/mask, C/F, sham and receipt differential fixtures, including wrong/invalid fourth-round candidates and richer earlier candidates that must not be backfilled. Test old values in retained prose, remote acquired evidence, unknown replacements, tombstones and nested mutations. Include CPU v1→v2→v3 authority tests without introducing a live second revision or new arms.

**Evidence:** Implementation, boundary snapshots, paired native renders and
executed results are recorded below. The [completion handoff](#completion-and-handoff)
closes this task.

**Start checkpoint (4 October 2026):** The clean `7f56c1b` checkout passes
`python -m recovery validate`: 121 CPU checks on Windows / CPython 3.11.9.
M1's gate and M2-T03's drained-prefix, replacement-state and delivery interfaces
are confirmed. Implementation will use explicit event/policy cases, the saved
world/branch identities and existing source/receipt layouts. Exact mixed/Q
reply reuse, complete capacity and durable apply-once execution remain later
tasks; this task supplies identifiable, serializable boundary results.

**Implementation checkpoint:** [events.py](../../../recovery/events.py) starts
each scheduled continuation from its original drained prefix and applies the
literal event/retention rule. Seventeen focused CPU checks in
[event_checks.py](../../../tests/event_checks.py) pass, including every
scheduled non-Q boundary in both saved mathematical-size populations and
development sets. All 61 existing view/protocol/round checks also pass.
Persistent notices identify boundary application without another stored flag
or ID. The numeric ordinary receipt layout also appears in L/F/masks, preserving
delivery/reset contrasts; an ordinary pending receipt has no before-value or
replacement payload. Disclosed before-values still require delivered v2.
Native paired artifacts, final source/installed checks and handoff remain open.

**Native checkpoint:** Four checks in
[tokenizer_events.py](../../../tests/tokenizer_events.py) pass using pinned
Qwen3.5-9B revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` on Windows /
CPython 3.11.9, Pydantic 2.12.5, Transformers 5.12.0, Tokenizers 0.22.2,
Jinja2 3.1.6 and Hugging Face Hub 1.19.0. The retained
[boundary archive](../../../tests/fixtures/event_boundaries.json) contains
four original prefixes, 15 complete boundary snapshots and 60 exact first
requests/native sequences, including all six receipt pairs across Prefix Sum
and Sort. Actual complete-input disclosure differences are −4 tokens per peer
for the saved Prefix Sum pairs and −3 for Sort; no padding is added. Dynamic
native checks cover all five families/both sizes, exact mixed-parent requests,
and full ordinary history accumulation in four representative continuations.
Observed boundary inputs are 736–3,218 tokens plus the full 384 output reserve;
prefix replies are 3–269 tokens. These are fixture measurements, not complete
capacity, replay, model or empirical admission. Final regression checks remain.

**Prerequisite handoff (4 October 2026):** [M2-T03 completion](M2-T03-synchronous-rounds-and-prefixes.md#completion-and-handoff)
passes 121 source/installed CPU checks and 14 native-tokenizer checks. Its
immutable, fully drained original prefix retains all current sources, own/
received history, actual fourth-slot candidate/absence, feedback and delivery
audit. `fork_prefix` deep-deserializes each fresh continuation with its original
parent ID; `PeerState` supports literal replacement while persistent notice/
receipt fields remain separate. `RoundResult.barrier` preserves exact original
requests/replies for the subsequent replay task. Use these interfaces without
repairing candidates or treating an untransformed scripted continuation as an
implemented event/policy. This was the prerequisite ready-state handoff;
the completion evidence below supersedes it. M2's gate remains open.

## Completion and handoff

**M2-T04 is implemented and verified on CPU.** All completion criteria pass.
Final source and outside-checkout installed validation each pass **140 checks**:
80 dependency-free core, 23 strict-reply, 18 round/prefix and 19 event/retention
checks. Core-only validation with site packages disabled passes all 80 core
checks and explicitly excludes replies/rounds/events. The four new native
event checks and all 14 prior native checks pass, with the previous fixtures
reproducing unchanged. Windows / CPython 3.11.9 uses Pydantic 2.12.5 for source/
native checks and 2.13.5 in `.venv`; installed `pip check` passes. These are CPU
validation environments, not an accepted M5 lock.

| Acceptance area | Executed evidence | Result |
|---|---|---|
| Original starts and populations | `test_all_scheduled_events_subsets_and_repeats_start_from_original` | Every non-Q continuation in both saved 60-world mathematical-size populations and five-world development sets starts from its own original drained prefix, including nested-40 worlds, preserving subsets and extra replicates. No outcome-dependent selection; originals remain byte-identical. |
| Local/broadcast revision | L/B differential, BFS forwarding and hidden-payload checks | All peers get the same notice; v1 loses authority and metadata everywhere. L gives v2 only to the edited owner, with pending markers elsewhere; B broadcasts it. Only replacement content/associated delivery differs. Unexposed BFS endpoints stay hidden until exact tombstone delivery. Host acquisitions use stable branch IDs and recovery-one availability. |
| B/C/K and both masks | Literal-retention checks plus native per-peer request equality | B retains actual history/candidate/feedback; C clears them; K retains only its own actual valid fourth-slot result, including wrong values, or explicit invalid/failed absence. Earlier richer work is never backfilled. Sources, source metadata, notice and receipt match across policies. Each mixed peer's view, rendered request and native IDs exactly match its B/C parent. Reply reuse remains T05. |
| C/F evidence contrast | `test_c_f_differ_only_by_acquired_remote_sources_and_corresponding_metadata` | Both clear derived work. F retains its corrected private shard and broadcast revision, dropping other acquired remote evidence and its current delivery metadata. Full prior deliveries remain offline audit data. |
| Sham and preserving events | Neutral-notice/source equality and separate-original-sibling checks | Sham changes no sources or deliveries and assigns the same continue-solving notice. Preserving B/C/K use their saved original-world edit independently of main-revision siblings; no candidate is repaired and no live second revision exists. |
| Receipts | CPU exact-field comparisons and [event_boundaries.json](../../../tests/fixtures/event_boundaries.json) | Genuine archived before-values include only changed ID, owner, versions and public position. Ordinary fields say `not included in this receipt`, including where model prose still contains old values. Paired views differ only in that field; v2 is identical and v1 cannot be forwarded. No delta, formula, footprint, corrected result or unchanged extra record is added. |
| Ordinary new history | Four-round policy checks and compact-result regression | All policies append new work. When a new slot replaces K's latest candidate, the exact historical result/absence moves into labeled history once, surviving subsequent valid, invalid and failed slots without fabricating a full reply or inheriting an old answer as a new outcome. Notices and receipts persist. |
| Isolation and apply-once seam | Nested-mutation, round-trip and nonoriginal-input rejection checks | Every sibling deep-deserializes the original. Deliberate nested source/history/candidate/notice/delivery mutation cannot alter the saved world, original or other siblings. Persistent notices identify `boundary_applied` without another store/ID. Already-transformed, partial and mismatched prefixes fail; M3 still owns crash-safe integration. |
| Source versions and visibility | CPU v1→v2→v3, paired hidden worlds, stale lookup and offline-evaluator guards | Source updates never rewrite derived work. Unknown replacements and known tombstones remain distinct. Hidden before-values/endpoints and unused future edits cannot change an unexposed peer request. Boundary execution calls no gold/eligibility evaluator. Version-three checks introduce no live arm. |
| Token costs and reproducibility | Four native checks, three hash-seeded fresh processes, optional-stack blocker and RNG assertion | Four prefixes, 15 boundary snapshots and 60 exact first requests reproduce. Saved disclosure input differences are −4 tokens/peer for Prefix Sum and −3 for Sort; actual receipt-field costs are also archived, with no padding. Native boundary inputs use 736–3,218 tokens plus 384 reserved output; scripted prefix replies use 3–269. These ranges are observations, not complete capacity admission. |

The compact-result persistence defect found during review is fixed and covered
by `test_compact_historical_result_survives_new_valid_invalid_and_failed_slots_exactly_once`.
It uses the existing candidate record as a labeled history entry, avoiding a
second candidate store or a synthesized own reply. Initial boundary renders
and all prior native fixtures remain unchanged.

Executed commands:

```powershell
python -m unittest tests.event_checks tests.test_peer_views tests.protocol_checks tests.round_checks -q
python -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate --core-only
python -m tests.tokenizer_events --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_rounds --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The first command passes 80 focused/regression checks. The outside-checkout
harness invokes `.venv/Scripts/python.exe -m recovery validate` from a fresh
temporary directory, using absolute paths to the same population, schedule and
authority; all 140 checks pass without resampling. Native metadata-only
reproduction and exclusive fixture creation are documented in the
[fixture instructions](../../../tests/fixtures/README.md#event-boundaries-and-receipt-pairs).

**[M2-T05](M2-T05-mixed-and-prose-delay-replay.md) is ready.** Use
`start_continuation` for B/C/mask starts and the existing `RoundResult.barrier`
for exact parent requests/replies. Q is explicitly rejected until its replay/
delivery rule exists. Add its parent-equivalent initial boundary together with
the required source/prose timing and equality checks; never copy a parent's
post-delivery recipient state. The existing component queue and stable delivery
IDs supply the required seams. Candidate history now permits the exact
historical fourth-slot `CandidateState`, alongside literal own replies/prose.

No specification, dependency, study configuration, mathematical core, saved
population/schedule authority, prior native fixture, vendor or research artifact
was changed. No GPU, model call, pilot, main run or publication was performed.
Exact mixed/Q replay, the local-view witness and complete capacity remain
M2-T05–T06; durable persistence remains M3. **M2 is 4/6 done and its gate remains
open.** Focused commits preserve preparation, implementation, the retention
correction, native evidence and completion as separate checkpoints.

Final documentation/artifact audit passes **468 local links/anchors/line
references in 39 documents**, balanced fences, all **29 task/index status
comparisons** and milestone totals: seven done, one ready and 21 blocked.
The new archive is canonical UTF-8/LF. Git comparison against prerequisite
`7f56c1b` confirms the protected scientific/configuration/authority/reference
artifacts listed above are unchanged.

