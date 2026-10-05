# M3-T03 — Local worker scheduling and cross-worker replay

**Status:** active

**Dependencies:** [M3-T02](../M3/M3-T02-bounded-attempts-and-failures.md#completion-and-handoff).
M2 passed and M3-T02 completed on 5 October 2026. Use its bounded
`ProcessProvider` and exclusive worker-local ledger/checkpoints; preserve known
timeouts, the single identical retry and observed/uncertain process work.

## References

- [Repository contract](../../../AGENTS.md), [plan worker ownership](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [fresh-call/RNG ownership](../../implementation-research/inference-and-capacity.md#rendering-termination-and-call-independence).

## Intended outcome

A small local scheduler executes balanced blocks across isolated serial workers and resolves exact replay dependencies regardless of worker placement.

## Scope and boundaries

- One process and database per worker, serial calls within each worker; M5 attaches one full model replica to each T4. Validate now with CPU scripted workers.
- Schedule balanced task/world blocks and rotate eligible sibling order/device assignment while respecting prefix and B/C first-round parent dependencies.
- Make immutable prefix/reply records available to an assigned worker with original physical generation IDs. A copied/accessed parent remains the same physical generation, not a new charge or fresh result.
- Preserve independent branch state, cursors and queues across workers. Set intended device visibility before CUDA initialization in the future backend; process-global RNG must not race across threads.
- Use existing IDs, saved seeds, records and local process coordination. No distributed queue, shared writable peer state, fixed-affinity requirement or transfer service is warranted.
- Resume from existing manifests/checkpoints, retaining which work is dependency-waiting or runnable. Never select work by correctness or drop silence/early-success branches.

## Completion criteria

- Cross-worker prefix and mixed/Q parent access preserves original identities, exact raw replies and branch-local effects.
- Worker/order changes do not change seed assignment, logical schedule, scripted results or replay parents.
- A missing/inconsistent dependency stops clearly instead of silently regenerating it.
- A worker restart can resume assigned work without a new configuration or duplicate logical slot.

## Validation and evidence

Run two local CPU worker processes with intentionally uneven delays and order reversal. Move a mixed/Q continuation to the other worker, including invalid parent replies and held prose. Check parent identity/cost references, immutable snapshots, independent queues, saved seeds and equal committed scripted outcomes. Deliberately remove/mis-scope a parent and verify rejection. Test scheduler recovery from one interrupted worker.

Implementation started on 5 October 2026 after inspecting T01/T02's runner,
ledger and executed CPU evidence. Use read-only access to original worker
records for prefixes and B/C parents; keep reply/attempt ownership and delivery
checkpoints in their original worker files. A small local process controller
will derive runnable/dependency-waiting work from the saved schedule and those
checkpoints, rotate eligible starts, and preserve the existing bounded provider.

**Evidence:** Not yet recorded. Add cross-worker traces and actual process/environment results before marking done.

