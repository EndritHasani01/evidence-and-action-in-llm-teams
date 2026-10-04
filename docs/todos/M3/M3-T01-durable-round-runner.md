# M3-T01 — Durable rounds and exact response reuse

**Status:** blocked

**Dependencies:** [M2-T06](../M2/M2-T06-attainability-and-capacity.md). The M2 gate must have passed.

## References

- [Repository contract](../../../AGENTS.md), [plan persistence architecture](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§3–4](../../../PROJECT_SPECIFICATION.md#3-common-peer-protocol) and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [persistence limits](../../implementation-research/state-and-replay.md#persistence-recommendation-and-its-limits).

## Intended outcome

The validated round procedure runs through LangGraph/local SQLite, with exact durable replies committed before effects and reconstructible branch checkpoints.

## Scope and boundaries

- Use one SQLite file per worker, ordinary application-owned transactions for calls/attempts, and explicit replacement checkpoint state for the four peers. No append reducer may restore cleared history.
- Start each branch in a new thread from a deep-deserialized drained original prefix. Persist boundary application so resume cannot apply it twice.
- Retain exact requests/settings/seeds, raw text/generated IDs or failure records, pre-delivery parent barriers, phase/round/prefix relationships, queue/cursor state and branch-scoped applied message IDs.
- Completed call identities always return their exact persisted response/failure, including invalid outcomes. Mixed/Q replay checks request/settings/seed/view equality and uses the proper event/replicate parent; never import parent post-delivery tables or deduplicate unrelated matching requests.
- Committed checkpoints own peer state and delivery effects. Derive delivery exports from committed transitions; do not add a competing authoritative effect store.
- Verify synchronous checkpoint durability and SQLite settings. Do not use saver-private transaction helpers for application writes or hold write locks during inference. Use clean checkpoint/close or SQLite backup for archives.
- Start with LangGraph as approved. Use the small-loop fallback only if the real integration demonstrates an unresolved semantic incompatibility, documenting it in the plan while retaining all contracts/tests.

## Completion criteria

- Raw responses/failures are durable before validation-dependent effects.
- Restart reconstructs an interrupted transition from saved replies without inference; stable delivery IDs prevent repeated effects within a branch.
- Explicit slot/generation/replay identities and statuses distinguish pending, active attempt, completed raw reply, timeout, exhausted infrastructure failure and replay use; validity/correctness are separate.
- Database reopen and backup preserve the authoritative committed state without restoring cleared fields or mutating siblings.

## Validation and evidence

Run scripted save/reopen/resume checks, invalid parent reuse, equality mismatch rejection, per-branch delivery idempotence and replacement clearing. Inspect actual SQLite/durability behavior instead of assuming the research toy's results transfer. M3-T05 performs the full killed-process acceptance suite after attempt/scheduler/accounting integration.

**Evidence:** Not yet recorded. Add named checks, actual package/SQLite versions and artifact paths before marking done.

