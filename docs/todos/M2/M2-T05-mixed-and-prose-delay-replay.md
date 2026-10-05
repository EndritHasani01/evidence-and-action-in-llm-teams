# M2-T05 — Exact mixed-group replay and prose-delay delivery

**Status:** done

**Dependencies:** [M2-T04](../M2/M2-T04-events-retention-and-receipts.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md), [plan round/replay architecture](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§4.4](../../../PROJECT_SPECIFICATION.md#44-early-prose-availability-with-current-sources-fixed), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [exact response reuse](../../implementation-research/state-and-replay.md#exact-reuse-is-different-from-framework-replay).

## Intended outcome

Mixed and Q branches consume exact parent first-round records and reconstruct their own deliveries with the required equality and delay controls.

## Scope and boundaries

- Before reuse compare exact rendered request, settings, saved seed and permitted state with the same-event/same-replicate B or C parent. Any mismatch is a protocol defect.
- Reuse raw replies and recorded invalid/failure outcomes. Seeds, framework replay or similar prompts do not authorize regeneration or unrelated caching.
- Mixed branches select the B/C parent appropriate to each peer, assemble the outgoing set, then apply effects inside that branch. Never copy parent post-delivery recipient tables.
- Q replays the entire B/C first round, delivers validated sources normally, retains senders' own replies, and holds only incoming round-one prose until before round three.
- Before round two, Q and parent current sources, own reply and source-delivery metadata match. Held text must not leak through summaries, placeholders, candidate sharing, feedback or queue metadata; text-only sends create no revealing placeholder.
- At the round-three boundary append held round-one prose before round-two prose, ordered by generation round/sender with stable IDs. Preserve already-seen history order and then resume ordinary delivery.
- Use the M2 in-memory saved records now; durable reuse is M3. Count held/no-held prose so inactive Q treatments remain reportable and included.

## Completion criteria

- Mixed/Q first-round generation opportunities are satisfied solely by their exact prescribed parent records.
- Recipient effects, queues and applied message IDs are independent per branch; the same saved send may affect each sibling once.
- Both complementary masks, revised/sham Q and extra-replicate parent scoping pass fixtures.
- Q neither changes the horizon nor permanently drops/reorders already-seen text; later acquisition divergence remains an outcome.

## Validation and evidence

The evidence below records this task's original 4 October 2026 completion.
M2-T06 renewed its request archives and affected checks after the authorized
5 October renderer/protocol revision; see the renewal at the end. Original
measurements and handoff status are historical, not current gate claims.

Include invalid parents, failed parents, mixed source-plus-prose sends, text-only sends, no prose, duplicate attempts, tombstones and deliberately mismatched requests/settings/seeds/views. Assert branch-local mixed assembly, round-two source/own-reply equality, no hidden held-text sentinel, chronological release, no duplicate history and unchanged parent/sibling states.

**Evidence:** Implementation, exact-parent comparisons, native queue traces and
executed acceptance results are recorded below. The [completion handoff](#completion-and-handoff)
closes this task.

**Start checkpoint (4 October 2026):** Clean prerequisite `fac764f` passes
`python -m recovery validate`: 140 CPU checks on Windows / CPython 3.11.9.
The current specification, plan, synthesis, replay investigation and M2-T04
handoff have been inspected. Implementation will reuse the existing pre-delivery
barrier, validated schedule IDs, source/text component queue and pure delivery
functions. In-memory saved settings/seeds/replies will govern exact reuse;
durability remains M3. No scientific or configuration change is required.

**Implementation checkpoint:** [replay.py](../../../recovery/replay.py) obtains
scheduled replies into an immutable in-memory `SavedRound` before branch-local
effects. Exact parent IDs, event/replicate scope, permitted views, rendered/native
requests, settings, seeds and recorded validation must agree; missing parents
fail without generation. Q inherits its parent's boundary and uses existing
component IDs/queues for source-normal, prose-delayed delivery. Host-only held
counts derive from committed queues/deliveries, including zero for inactive Q.
All 18 focused [replay checks](../../../tests/replay_checks.py) pass; all 80
existing view/protocol/round/event checks also pass. Both masks and Q execute
four recovery rounds with four reused and twelve new calls. Native artifacts,
final source/installed validation and completion handoff remain open.

**Native checkpoint:** Four checks in
[tokenizer_replay.py](../../../tests/tokenizer_replay.py) pass with the pinned
Qwen3.5-9B tokenizer revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`.
[replay_traces.json](../../../tests/fixtures/replay_traces.json) retains four
prefixes, 54 continuation rounds, 216 exact requests and 72 parent comparisons.
It includes revised/sham B/C/masks, complete Q horizons, pending/released stable
IDs, invalid/failed parents, repeated source attempts, tombstones and two
source-only inactive Q cases. Native masks also pass all five families/both
sizes/events/replicates. Observed archive inputs are 921–3,350 tokens with the
full 384 output reserve; replies use 6–134 tokens. These fixtures do not establish
the complete capacity bound or any model result. Final regression/reproduction
and documentation audit remain open.

**Prerequisite handoff (4 October 2026):** [M2-T04 completion](M2-T04-events-retention-and-receipts.md#completion-and-handoff)
passes 140 source/installed CPU checks and all 18 native-tokenizer checks.
`start_continuation(prefix_bytes, prepared_world, scheduled_branch)` supplies
fresh, literal B/C/mask/event/receipt starts from the original drained prefix;
mixed first views, requests and native IDs exactly match the appropriate B/C
parents. `BranchState.boundary_applied` derives from persistent notices and
survives serialization. Q remains explicitly rejected until this task adds its
parent-equivalent boundary and prose-delay/replay behavior. Use the existing
`RoundResult.barrier`, `stage_effects` and `drain_deliveries` interfaces to reuse
literal saved replies before branch-local delivery, including invalid/failure
outcomes. K's retained fourth-slot result/absence becomes a labeled history
entry once a new recovery slot replaces the latest candidate. This historical handoff
established boundary semantics; the completion evidence below supersedes its
ready-state limitations. M2 gate passage remains open.

## Completion and handoff

**M2-T05 is implemented and verified on CPU.** All completion criteria pass.
Final source and outside-checkout installed validation each pass **158 checks**:
80 dependency-free core, 23 strict-reply, 18 round/prefix, 19 event/retention and
18 replay checks. Core-only validation passes all 80 checks with site packages
disabled. All **22 native-tokenizer checks** pass (four replay plus 18 prior),
including fresh-process archive reproduction with `PYTHONHASHSEED=37`. Previous
native fixtures reproduce unchanged; the new archive has canonical UTF-8/LF bytes.

The environment is Windows / CPython 3.11.9, with Pydantic 2.12.5 for source/native
checks and 2.13.5 in the installed `.venv`. Native checks use Transformers 5.12.0,
Tokenizers 0.22.2, Jinja2 3.1.6, Hugging Face Hub 1.19.0 and the pinned Qwen3.5-9B
tokenizer revision above. Installed `pip check` passes. These are CPU validation
environments, not an accepted M5 inference lock.

| Acceptance area | Executed evidence | Result |
|---|---|---|
| Exact prescribed parents | `test_both_masks_all_families_sizes_events_and_extra_replicate_parents`; native all-family counterpart | Both masks use the scheduled B/C peer parent across five families, both sizes, revision/sham and the extra replicate. Permitted view, exact rendered/native input, settings, seed and recorded outcome agree. Parent IDs retain original generation identity; no unrelated prompt/seed cache is used. |
| Protocol defects stop reuse | Request/native-input/settings/seed/view mutation, scope mutation, missing/duplicate-record and validation-corruption checks | Wrong event, replicate, world, policy, peer or round fails. Missing parents remain unexecuted dependencies; no fallback generation, resampling or fabricated failed result occurs. All dependencies are checked before effects. |
| Invalid/failed parent records | Literal mixed/Q failures, all-invalid/all-failed Q and invalid source-plus-prose fixtures | Exact raw text, generated IDs, termination and recorded absence survive revalidation. Invalid sends have no partial source/prose effects; neither invalid nor failed slots inherit old candidates. |
| Branch-local mixed assembly | `test_mixed_assembly_is_branch_local_and_repeated_commit_is_idempotent`; nested-isolation checks | Selected outgoing messages assemble before recipient delivery. Each branch starts from its original transformed prefix and owns its IDs/effects. The same saved send can affect each sibling once. Repeated commit reconstruction and released-ID attempts create no duplicate history; parent/prefix/sibling bytes remain unchanged. |
| Q sources and own work | Sort/BFS × both sizes × revision/sham × Q_B/Q_C CPU fixtures; native paired traces | All validated sources, including duplicate attempts and BFS tombstones, deliver before round two. Sources, current delivery metadata, own reply, candidate and feedback match the B/C parent. Host revision and receipt remain unchanged. |
| Held-text visibility | Incoming-sentinel and paired text-only/no-message request tests | Held text is absent from recipients' permitted/rendered/native requests, feedback and metadata. Changing held payloads or removing a text-only send cannot change that recipient's round-two request. Senders retain their own literal replies. No placeholder or queue-policy field is introduced. |
| Release and horizon | `test_release_order_existing_history_horizon_and_later_source_divergence`; complete mixed/Q runs; native Q horizons | Before round three, held round-one prose appends before round-two prose in generation/sender order with original stable delivery IDs. Already-seen history and own round-two replies stay in place. Normal delivery resumes; each mixed/Q continuation has four reused plus twelve new opportunities and no fifth call. Later source acquisition can diverge as an outcome. |
| Inactive treatment accounting | Source-only and explicit-empty fixtures, retained zero-count cases, JSON round trips | `held_prose_counts` derives nonempty counts per recipient from committed pending/released IDs. Counts persist after release; zero-prose Q remains included. Explicit empty strings still traverse the literal queue but add no prose exposure. No second counter/store is added. |
| Native evidence and limits | [replay_traces.json](../../../tests/fixtures/replay_traces.json), reproduced by `tests.tokenizer_replay` | Four prefixes, 54 continuation rounds, 216 exact requests and 72 archived parent comparisons reproduce. Revised/sham masks and complete Q horizons retain raw outcomes and pending/released snapshots. Every replay joins one exact archived parent, with no duplicate call IDs. Observed inputs use 921–3,350 tokens plus 384 reserved output; replies use 6–134 tokens. These are fixture measurements, not the complete capacity bound. |

Artifact review caught an inactive-fixture construction defect: a different
scripted response reused a rich scenario's call IDs, leaving the archived parent
join ambiguous. Inactive cases now use the predetermined second saved world of
each fixture family/size and retain their own B/C parents. A fourth native check
audits unique call IDs and every exact parent join across the whole archive.
This corrects deterministic evidence; runtime replay behavior and the scientific
schedule/configuration are unchanged. Final review also closed an inactive-count
edge case: `held_prose_counts` now rejects unexecuted recovery and uncommitted
rounds, rather than turning missing round-one observations into zero-held cases.
The source-only/empty-prose regression checks cover this distinction.

Executed commands:

```powershell
python -m unittest tests.replay_checks -q
python -m unittest tests.replay_checks tests.event_checks tests.round_checks tests.protocol_checks tests.test_peer_views -q
python -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate --core-only
python -m tests.tokenizer_replay --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_events --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_rounds --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The combined focused command passed 96 checks before the final two replay
fixtures were added; the final 18-check replay run and full 158-check suites
include both additions. The installed harness invokes
`.venv/Scripts/python.exe -m recovery validate` from a fresh temporary directory,
using absolute paths to the same configuration, population, schedule and authority;
all 158 checks pass without resampling. Native reproduction runs each listed
module in a fresh process. Archive creation and reproduction are documented in
the [fixture instructions](../../../tests/fixtures/README.md#exact-parent-replay-and-delayed-prose).

**[M2-T06](M2-T06-attainability-and-capacity.md) is ready.** Its locally informed
witness should execute scheduled continuations through `obtain_continuation_round`
and `commit_continuation_round`. Retain B/C first-round `SavedRound` records for
each event/replicate and pass them as `parents`; mixed/Q first rounds never call
the provider. New calls receive `seed` and `settings` as keyword arguments in
addition to the permitted view, rendered request and tokenized input. Keep the
obtain/save boundary before commit when M3 adds durable records. The current
in-memory runner does not implement process-crash recovery or physical attempt
costs, and no archive fixture is a complete worst-context proof.

No specification, dependency, study configuration, mathematical core, saved
population/schedule authority, prior native fixture, vendor or research artifact
was changed. No GPU, model inference, pilot, main run or publication occurred.
**M2 is 5/6 done and its gate remains open** for the local-view witness and full
capacity argument. Commits separate preparation, implementation, native evidence
and the completion handoff.

Final documentation/artifact audit passes **484 local links/anchors/line
references in 39 documents**, balanced fences, all **29 task/index status
comparisons** and milestone totals: eight done, one ready and 20 blocked.
The replay archive's canonical bytes and four-prefix/54-round/216-request/
72-parent-comparison counts agree. Git comparison against prerequisite `fac764f`
confirms the protected scientific/configuration/authority/reference artifacts
listed above are unchanged.


## Renewal under M2-T06

On 5 October 2026, the finalized literal-block renderer, column metadata,
footer and scalar-message boundary passed this task's 5 native checks.
Its canonical archive was renewed and reproduced in a fresh hash-seed-37
process; source and installed-library validation also passed. Current
archive measurements are in the [fixture instructions](../../../tests/fixtures/README.md).
[M2-T06 completion](M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records the full validation, complete capacity admission and M2 gate.
