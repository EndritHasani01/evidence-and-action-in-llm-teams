# M2-T03 — Synchronous rounds and immutable shared prefixes

**Status:** done

**Dependencies:** [M2-T02](../M2/M2-T02-strict-replies-and-feedback.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md), [plan round procedure](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§2.2](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§3](../../../PROJECT_SPECIFICATION.md#3-common-peer-protocol), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [state semantics](../../implementation-research/state-and-replay.md#semantics-that-belong-to-the-application).

## Intended outcome

A deterministic in-memory round runner executes scripted replies through the real views, renderer, validator and source/text delivery interface, and produces a drained immutable prefix.

## Scope and boundaries

- Use the fixed barrier: freeze four views, render all requests, obtain replies, validate all, stage outgoing source/text effects, commit together, then advance. Serial physical invocation must not expose current-round output.
- All four peers receive four prefix and four continuation opportunities. Submission, success, invalid replies and silence never deactivate peers.
- Forward exact payloads only from sender-held current references. Never fetch unseen records or compute aggregates for peers. Treat free text/candidates as untrusted derived work.
- Record sender/recipient, source ID/version or text, generation round, first usable round, host/agent origin and stable branch-scoped message relationships. Track delivery attempts separately from unique acquisitions.
- Drain prefix-round-four messages before snapshot serialization. Preserve enough state for new siblings, replay pre-delivery barriers and later queue/checkpoint integration; no persistence framework is required yet.
- Archive rendered owner-v1 exposure and all four prefix rounds. Exposure is a factual check, not proof of model use or a world-selection rule.

## Completion criteria

- Reversing peer invocation order produces identical scripted committed states, messages and outcomes.
- No recipient can observe another peer's current-round reply before the barrier.
- A prefix round-four snapshot has no pending deliveries and can be deep-deserialized without nested sharing.
- The in-memory procedure can later accept event-specific retention and delivery rules without changing protocol semantics.
- Delivery metadata provides the timing/origin/acquisition fields required by later analysis without leaking hidden payloads into prompts.

## Validation and evidence

The evidence below records this task's original 4 October 2026 completion.
M2-T06 renewed its request archives and affected checks after the authorized
5 October renderer/protocol revision; see the renewal at the end. Original
measurements and handoff status are historical, not current gate claims.

Exercise source-plus-text, text-only, empty and wholly invalid replies; repeat source references; tombstone versus pending coverage; and all four scheduled opportunities after early success/failure. Mutate nested state in one deserialized sibling and assert original/other siblings unchanged. Verify full round-four drain and owner-v1 rendered exposure from actual requests.

**Evidence:** Implementation, native trace and final acceptance results are
recorded below; the [completion handoff](#completion-and-handoff) closes this task.

**Start checkpoint (4 October 2026):** The clean `405a171` checkout passes
`python -m recovery validate`: 103 CPU checks on Windows / CPython 3.11.9,
Pydantic 2.12.5. M1's recorded gate and M2-T02's staging handoff are confirmed
against the current interfaces. Work is limited to the deterministic in-memory
barrier, delivery records and drained prefix; durable execution, event policies,
mixed/Q replay and complete capacity remain their subsequent tasks.

**Implementation checkpoint:** [rounds.py](../../../recovery/rounds.py) supplies
the pure prepare/validate/stage/drain/commit steps, an all-peer scripted caller,
offline branch-scoped component deliveries and deep JSON prefix deserialization.
[round_checks.py](../../../tests/round_checks.py) passes 17 focused checks;
`python -m recovery validate` passes 120 checks. The installed Python 3.11.9 /
Pydantic 2.13.5 environment also passes the 40 protocol/round checks. Prefixes
and full continuation opportunities remain independent of validity/correctness.
Native-tokenizer trace reproduction and final documentation audit are in progress.

**Native-tokenizer checkpoint:** [tokenizer_rounds.py](../../../tests/tokenizer_rounds.py)
passes three checks using pinned Qwen3.5-9B revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, Windows / CPython 3.11.9,
Pydantic 2.12.5, Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6 and
Hugging Face Hub 1.19.0. The retained
[eight-round trace](../../../tests/fixtures/round_traces.json) reproduces every
rendered/template request, native ID, literal output/failure, staged message,
delivery component, committed peer state and drained prefix. All five families
at both sizes and both invocation orders pass across prefix and continuation.
Observed scripted inputs are 699–3,912 tokens, with the full 384 output reserve;
generated outputs are 0–243 tokens. This is tokenizer-only protocol evidence,
not the complete capacity argument, an event/replay control, or model execution.

**Review checkpoint:** Prefix invocation order is materialized once so an
iterable supplies the same four-peer order in every round. Eighteen focused
checks now also verify delayed component release preserves already-seen history
and generation/sender ordering, and fresh-process snapshots are identical under
three Python hash seeds while inference/framework imports are blocked and the
global RNG remains unchanged. The final full source and outside-checkout
installed CLI suites each pass 121 checks; core-only passes 80; all 14 native
checks (three round, six protocol, five renderer) pass with unchanged prior
request/reply fixtures. Task closure awaits the status/link/documentation audit.

**Prerequisite handoff (4 October 2026):** [M2-T02 completion](M2-T02-strict-replies-and-feedback.md#completion-and-handoff)
passes 103 source/installed CPU checks, six native protocol checks and the five
unchanged native renderer checks. `validate_reply` returns separate validity
stages, literal generated text/IDs, candidate absence/validity, public feedback
and immutable staged messages resolved only from sender-held current sources.
Repeated references preserve separate delivery attempts; no effects are applied.
These records supplied the fixed four-view barrier and message/delivery
relationships implemented here. This was the prerequisite ready-state handoff;
the completion evidence below supersedes that state. M2's complete
protocol/capacity gate remains open.

## Completion and handoff

**M2-T03 is implemented and verified on CPU.** All completion criteria pass.
The final suite is **121 checks** in both the source and outside-checkout
installed environments: 80 dependency-free core, 23 strict-reply and 18 round/
prefix checks. Windows / CPython 3.11.9 uses Pydantic 2.12.5 for source/native
checks and 2.13.5 in `.venv`. Core-only validation with site packages disabled
passes all 80 core checks and explicitly excludes strict replies/rounds.
The three new native round checks and all six protocol/five renderer checks
pass; prior saved request/reply fixtures reproduce unchanged. Installed
`pip check` passes. These environments are CPU evidence, not the accepted M5 lock.

| Acceptance area | Executed evidence | Result |
|---|---|---|
| Fixed synchronous barrier | `SynchronousRoundTests.test_all_rendering_and_generation_precede_validation_and_recipient_effects` | Four views/rendered requests/token inputs are frozen before the first provider call; all replies are obtained before validation. Recipient effects stay absent until commit. Provider/configuration errors leave the parent unchanged, without retries. |
| Exact source/text interface | Source-plus-text, text-only, omitted/empty text, wholly invalid reply and tombstone/pending checks | Only sender-held current payloads are staged. Invalid sends discard the entire reply, even with a valid-shaped candidate. Derived prose never becomes raw evidence; pending BFS endpoints remain absent until exact tombstone delivery. Conflicting/stale recipient authority fails atomically. |
| Timing and acquisition | Repeat/resend, selective-component and idempotence checks | Three repeated references produce three attempts and one acquisition. Subsequent identical references remain attempts without new acquisition. Stable message/component IDs preserve branch relationships and idempotent release. Origin, generation and first usable labels remain recorded offline; public metadata keeps first acquisition per current version. Every validated source is released at its barrier. |
| Equal scheduled opportunities | Early-correct/invalid/failed fixture and final-continuation drain | All 16 prefix plus 16 continuation slots execute. Silence is literal invalid output; recorded failure and unexecuted absence remain distinct. No invalid/failed slot backfills an earlier candidate. Feedback enters only later calls. Final recovery deliveries are drained without a fifth opportunity. |
| Order independence | `SharedPrefixTests` and native all-family/both-size/eight-round order reversal | Requests, raw text/IDs, validity stages, messages, complete committed states and snapshot bytes are identical under forward/reverse physical order. Iterable invocation orders are retained for all four rounds. |
| Drained immutable prefix | Round-four drain, freeze rejection, round-trip and nested-sibling checks | Only a complete committed prefix with no queue can freeze. Round-four source/prose effects are present and labeled first usable at recovery round one. Each fork deep-deserializes every record. Nested source/history/candidate/delivery mutation in one sibling leaves parent, other sibling and archived bytes unchanged, including BFS tuples. |
| Archive and actual exposure | [round_traces.json](../../../tests/fixtures/round_traces.json), reproduced by the three native checks | All 32 scripted opportunities retain exact requests/native IDs, raw outputs/failures, validity, staged traffic, delivered components and committed peer data. All four owner-v1 prefix exposures are checked from actual rendered requests for every record, without testing model use or selecting worlds. |
| Later integration | Pure prepare/validate/stage/drain/commit functions and queued-component checks | Pre-delivery barriers and uncommitted states are inspectable. Source/text component IDs permit later delivery rules without changing views or validation. Deferred prose appends in generation/sender order without rewriting already-seen history or exposing queue placeholders. This does not claim completed event policies, exact mixed/Q controls or durable persistence. |
| Reproducibility | Three fresh Python hash-seed processes, optional-import blocker and RNG assertion | JSON prefix bytes remain identical; no model/framework stack is imported and global RNG state is unchanged. Native fixture requests use 699–3,912 input tokens with 384 reserved output; generated outputs use 0–243 tokens, without claiming the complete worst-context bound. |

Executed commands:

```powershell
python -m unittest tests.round_checks -q
python -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate --core-only
python -m tests.tokenizer_rounds --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The outside-checkout harness invoked `.venv/Scripts/python.exe -m recovery
validate` from a fresh temporary directory with absolute paths to the same
saved population, schedule and authority. It passes all 121 checks without
resampling. [Fixture instructions](../../../tests/fixtures/README.md#synchronous-rounds-and-drained-prefixes)
describe metadata-only reproduction and exclusive trace creation.

**[M2-T04](M2-T04-events-retention-and-receipts.md) is ready.** Start from
`ScriptedPrefix.snapshot` through `fork_prefix`, and use explicit `PeerState`
replacement for each event/retention rule. `RoundResult.barrier` preserves all
four original views, rendered/tokenized requests and literal validated replies;
it supplies later replay preparation without copying post-delivery recipient
tables. `stage_effects` and `drain_deliveries` expose the component queue and
record released IDs in the same committed state. Initial host deliveries and
prefix acquisitions are retained; branch IDs, queues and audit payloads never
enter peer prompts. M3 must still persist replies before effects and validate
real LangGraph/SQLite crash/resume behavior.

No scientific deviation, dependency, inference environment/configuration freeze,
model call, GPU use or experiment result was introduced. Event/retention/
receipts, exact mixed/Q reuse, local-view attainability and complete capacity
remain M2-T04–T06. **M2 is 3/6 done and its gate remains open.**

Final documentation/artifact audit passes **452 local links/anchors in 39
documents**, balanced fences, all **29 task/index status comparisons** and
milestone totals: six done, one ready and 22 blocked. The native trace is
canonical UTF-8/LF. Git comparison against the prerequisite `405a171` confirms
the specification, study configuration, dependencies, mathematical core,
population/schedule authority, protocol/renderer, prior native fixtures, vendor
and research are unchanged. Focused commits retain preparation, implementation,
native trace, review correction and completion as separate checkpoints.


## Renewal under M2-T06

On 5 October 2026, the finalized literal-block renderer, column metadata,
footer and scalar-message boundary passed this task's 3 native checks.
Its canonical archive was renewed and reproduced in a fresh hash-seed-37
process; source and installed-library validation also passed. Current
archive measurements are in the [fixture instructions](../../../tests/fixtures/README.md).
[M2-T06 completion](M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records the full validation, complete capacity admission and M2 gate.
