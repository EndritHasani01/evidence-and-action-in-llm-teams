# Interfaces, schemas, checkpoints, and reproducibility

The executable contracts are in [reference/contracts.py](reference/contracts.py); [schemas/contracts.schema.json](schemas/contracts.schema.json) is generated from them. The schema file is a mapping from model name to that model's standalone JSON Schema, not one combined instance schema. Use the named schema for each artifact. The reference package validates representative examples, not a complete running agent system.

## Contract inventory

| Entity | Required meaning / additional runtime validation |
|---|---|
| EvidenceVersion | immutable ID/key/version/root/owner/raw value/epoch/supersedes/hash; task validator checks raw type and version monotonicity |
| AtomObservation | evaluator-only Boolean conversion; one current observation per atom, one evidence ID per atom in the primary DSL |
| Correction | old IDs, new versions and epoch transition; replacement source keys must match superseded keys |
| ClaimDraft / ClaimRecord | Boolean slot, references, owner, call ID, epoch and superseded record; `(owner,slot)` has at most one active record |
| ActionDraft / ActionRecord | job, verb, resource/value/amount/route as applicable, references, epoch, immutable arguments, idempotency key |
| AgentReply | epoch acknowledgment, at most 4 new claims, retained IDs, at most 2 action commands, short audit-only note |
| SupportLabel | node, antichain of AND sets, OR across sets, estimate/gold origin, source-view hash, syntax status |
| ReadReceipt / GraphEdge | exact prompt-visible IDs and relation kind; no semantic assumptions added |
| Message | sender/recipient/epoch/claims/capsules/delivery step; source capsule delivery survives malformed semantic reports |
| Disposition / RepairPlan | append-only record lifecycle changes, mask origin, fallback and reset flags |
| AgentState / Snapshot | complete effective state and evidence receipts; branch snapshot also captures queues and executed effects |
| InferenceRequest / Result | rendered text/hash, full sampling and model fingerprint, seed, output, finish reason, tokens/time/attempts |
| Event / EventBatch | chained canonical event envelope and atomic batch; payload validated against kind-specific model before append |
| BranchOutcome | one row per completed/failed continuation with factors, costs, endpoint and mechanism columns |
| MatrixRow / ExperimentConfig | exact world counts, new/reused prefixes, arms, call allowances and model |

All unknown fields are forbidden. `EvidenceVersion.value` is raw JSON because families differ, but family validators constrain it to a four-item string/int array, Boolean, or the documented transfer integer/object. Disallow non-finite floats, executable payloads and arbitrary Python objects. Keep money in integer cents. Domain-specific invariants supplement JSON Schema.

Wire IDs are short aliases (`e01`, `c04`, `a02`) scoped to one episode. Persist a mapping to globally unique IDs. A short alias never refers to a different version in one episode. Aliases are assigned deterministically at creation, not by semantic correctness. Prompt token counts include the entire alias/rule/schema material.

## Critical Python interfaces

```python
class WorldFactory(Protocol):
    def make(self, family: str, base_seed: int, alternative: bool,
             bound: bool) -> tuple[PublicWorld, OracleWorld]: ...

class InferenceBackend(Protocol):
    async def generate(self, request: InferenceRequest) -> InferenceResult: ...

class EvidenceStore(Protocol):
    def apply(self, event: Correction) -> list[Event]: ...
    def current_view(self, delivered_ids: set[str]) -> list[EvidenceVersion]: ...

class StateReducer(Protocol):
    def reduce(self, snapshot: Snapshot, event: Event) -> Snapshot: ...

class PolicyPlanner(Protocol):
    def plan(self, view: RuntimeView, correction: Correction,
             support: EstimatedSupportView | None) -> RepairPlan: ...

class OraclePolicyPlanner(Protocol):
    def plan_from_mask(self, view: RuntimeView, correction: Correction,
                       unsupported_ids: set[str]) -> RepairPlan: ...

def render_view(snapshot, actor, phase, notice) -> tuple[str, ReadReceipt]: ...
def validate_reply(reply, actor, phase, view) -> list[DomainError]: ...
def apply_reply(snapshot, reply, call_id) -> list[Event]: ...
def freeze(snapshot, event_log) -> CheckpointReceipt: ...
def fork(checkpoint, branch_id) -> BranchStore: ...
def exact_support(formula, desired_value, delivered_current_evidence) -> SupportLabel: ...
def grade_branch(oracle_world, initial_snapshot, branch_events) -> BranchOutcome: ...
```

The exact evaluator is invoked by the analysis process and explicit oracle-arm adapter. A feasible policy never gets an object that contains the private world plus an instruction to “ignore the labels.” The separation is structural.

## Agent reply application

Validate ownership: A may write `eligible:X`; B may write `eligible:Y`, `feasible:target`, `feasible:control`; C may write its own `feasible:target/control` records and action commands. B's and C's identically named slots are different owned records. No cross-owner overwrite is allowed. All new claim drafts for a slot supersede that owner's previous active claim for that slot. Duplicate slots in one reply are schema errors. Omitted claims are unchanged; explicit `retain_claims` is logged but does not repair stale references.

References must exist in the actor's delivered/visible namespace, including IDs mentioned in a repair notice. An old reference can be syntactically valid but semantically stale; do not reject it using gold semantics. Unknown IDs or references to genuinely unseen private records are protocol errors. A new action that targets an old action ID cancels/supersedes it atomically. A, B cannot emit action commands. At the prefix stage, C's actions are proposed only; at the recovery stage the commands are final requests for each job.

Enforce the public action mode without consulting gold: unbound jobs allow only `publish`; bound primary jobs allow `dispatch` or `wait`; bound transfer jobs allow `reserve` or `wait`. Unknown resource identifiers are protocol errors. Choosing a known but ineligible resource passes the shape check and remains a semantic error to grade. Task correctness separately checks the documented resource priority.

`retain_claims` may name only the actor's active owned records. Regenerating a withdrawn claim requires a new typed claim draft. Omission does not reactivate a withdrawn record. Reviewer output has its own `ReviewerReply` schema. `RuntimeView`, `EstimatedSupportView`, `ModelLock`, `RunItem`, `RunManifest`, and `NodeEvaluation` are included in the executable contracts; the private experiment manifest is projected before being sent to inference workers.

Apply an entire schema-valid reply atomically. If one command violates ownership or shape, append a failure and apply none of its writes. The source capsule still travels. Do not partially salvage favorable fields.

Each line of `events.jsonl` is an EventBatch, containing one or more ordered Event objects. Validate the whole batch against a temporary projection before writing. Append one canonical JSON line, fsync it, then publish the in-memory projection. On recovery, ignore a trailing incomplete/unparseable line, verify both event and batch hash chains, and replay only complete valid batches. An invalid hash in the middle is corruption and halts recovery. The snapshot records flattened event and batch offsets. Every call reply, correction-plus-delivery operation, and repair-plan application has a distinct batch ID. A retry with an already committed batch ID is a no-op. This makes reply/correction atomicity concrete despite multiple underlying events.

## Frozen-prefix algorithm

```python
async def run_world(public, private, config):
    state = init_state(public)
    for slot, actor in enumerate(("A", "B", "C")):
        await run_agent_slot(state, actor, phase="prefix", slot=slot)
        transport.deliver_due(state)  # deterministic source capsule delivery
    assert transport.is_quiescent(state)
    checkpoint = freeze(state, events)  # no applied external effects
    estimate = await extract_support(checkpoint.public_projection())
    for policy in registered_arm_order(public.world_id):
        branch = fork(checkpoint, policy)
        correction = private.correction  # only source delta crosses boundary
        branch.apply_public_correction(correction)
        plan = policy_adapter(policy).make_plan(branch, estimate, oracle_service)
        branch.apply_plan(plan)
        for slot, actor in enumerate(("A", "B", "C")):
            if actor in plan.reset_agents:
                branch.clear_working_state(actor)  # OR resets C immediately here
            await run_agent_slot(branch, actor, phase="repair", slot=slot)
            transport.deliver_due(branch)
        branch.close_sandbox()
        persist_outcome(grade_offline(private, checkpoint, branch.events))
```

This pseudocode covers standard N/R/E/O/OC/ON/OR branches. F, B, S and no-event wrappers make the explicit changes specified in 08. `policy_adapter` uses the oracle service only for O/OC/ON/OR. Pass no future support labels into extraction. The implementation should split feasible and oracle functions, not rely on a string switch deep in the feasible policy.

## Checkpoint contents and atomicity

Freeze all agent projections; current-version map and full evidence history; claims/actions/dispositions; delivered and queued messages; source receipts; read edges; sandbox effects and idempotency keys; RNG seed map; logical clock; event offset and chain hash; config/model/prompt revision references. The checkpoint occurs after all prefix deliveries and before any correction. Queues should be empty, but are still serialized and asserted empty.

Write canonical JSON to a temporary file, fsync, atomically rename, and record its SHA-256. A branch is a fresh materialized projection plus an append-only suffix referencing that hash. A branch never appends to the parent event log. Copying only conversation text is prohibited. Native LLM hidden state/KV cache is not checkpointed; each call is reconstructed from rendered text.

## Seeds and cache

Use `seed64 = int.from_bytes(SHA256(root_seed || namespace || canonical_parameters)[:8], 'big') % (2**63-1)`. Separate namespaces: generator, names, prefix-sampling, extraction, recovery-slot, policy-order, subset-selection, bootstrap. Explicitly serialize the delimiter/parameter JSON; never use Python's randomized `hash()`.

Recovery slot seeds are shared across policies for the same world/replicate/actor slot (common random numbers); policy-order seeds are separate. Model outputs can differ because prompts differ. This coupling is recorded and analysis clusters by base world. The second stochastic replicate regenerates prefix, estimate and suffix with a new replicate seed. The second model regenerates all its prefixes and estimates.

Cache key hashes: rendered prompt bytes, model/weight/tokenizer revision, quantization/backend fingerprint, full decoding parameters, seed, schema/prompt version. Cache only completed raw responses, including malformed outputs; a cached malformed output is not resampled. Identical requests may legitimately reuse results, but cached responses are not independent repetitions. Any changed prompt/evidence/state/model/seed is a miss. Never reuse a suffix after changing its repair mask unless the complete rendered request and inference configuration really are identical.

Report physical executed calls and logical experimental calls separately. The 6,400-call budget assumes no accidental suffix cache savings. Analysis has one outcome per registered branch, not one per cache entry.

## Failure handling

- Semantic error, wrong answer, missed correction, malformed JSON, truncated output or invalid reference: count as model/protocol failure. No semantic retry. Continue the remaining prescribed slots with an error marker.
- Transient backend process/transport failure before an output is returned: at most one infrastructure retry of the identical request/seed; charge all attempts. Persist error and allocation time. Two failures mark branch infrastructure-terminal, not safe.
- OOM or context overflow: stop the block and diagnose globally. Do not silently reduce context or quantize only the failing arm. A changed backend/config requires a new experiment version and regeneration of affected paired blocks.
- Harness invariant/storage corruption: halt the experiment. Repair code on development fixtures; invalidate and rerun affected blocks with a documented reason, never based on outcome direction.
- Budget exhaustion: finish the current paired block only if its reserved allowance fits; otherwise do not launch it. Missing blocks stay missing. No favorable partial-policy comparisons.

## Artifact tree

```text
artifacts/<experiment_id>/
  registry/{config.json,environment.lock,model_manifest.json,preregistration.md}
  worlds/<id>/{public.json,private_gold.json,correction.json}
  prefixes/<id>/<replicate>/{events.jsonl,checkpoint.json,estimate.json}
  branches/<id>/<replicate>/<policy>/{events.jsonl,plan.json,outcome.json}
  calls/<call_hash>/{request.json,response.json}
  analysis/{branches.parquet,support_nodes.parquet,contrasts.csv,figures/}
  manifests/{files.sha256,run_status.json,cost_ledger.jsonl}
```

Private gold is excluded from the worker's mounted/readable prompt directory. An analysis process may read both; a feasible inference/policy process may read only public/runtime artifacts. SQLite in WAL mode may track job status on a single host; immutable JSON/JSONL remain canonical. Each worker has one writer queue; do not let two processes append the same log.

The per-run request projection contains no `world_private_path`; it is removed from RunManifest before worker dispatch. Environment variables and API credentials, if any are used during unrelated setup, never enter prompts, fingerprints, or saved request artifacts.

After every complete base-world block, persist logs to the configured durable experiment location and verify checksums. Kaggle output checkpoints must survive session interruption. Cache model weights before timed execution when permitted, but report allocation time separately; GPU-hours include idle allocated GPUs under the conservative accounting.
