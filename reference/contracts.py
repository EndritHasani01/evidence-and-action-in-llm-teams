"""Normative v1 contracts. Full runtime and GPU workers are implementation targets."""
from __future__ import annotations

from typing import Literal, Any
import json
from pydantic import BaseModel, ConfigDict, Field, model_validator

if not __debug__:
    raise RuntimeError("Reference contracts require validation assertions; do not run Python with -O")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Expr(Strict):
    op: Literal["atom", "and", "or", "not", "const"]
    name: str | None = None
    children: tuple[Expr, ...] = ()
    constant: bool | None = None

    @model_validator(mode="after")
    def shape(self):
        if self.op == "atom":
            assert self.name and not self.children and self.constant is None
        elif self.op == "const":
            assert self.constant is not None and not self.children and self.name is None
        else:
            assert self.name is None and self.constant is None
            assert len(self.children) == 1 if self.op == "not" else len(self.children) >= 2
        return self


class EvidenceVersion(Strict):
    evidence_id: str
    key: str
    version: int = Field(ge=1)
    root_id: str
    owner: Literal["A", "B", "C", "SYSTEM"]
    value: Any  # raw JSON; task validator checks domain-specific type and bounds
    epoch: int = Field(ge=0)
    supersedes: str | None = None
    content_sha256: str


class AtomObservation(Strict):
    """Evaluator-only conversion of a delivered raw evidence version."""
    atom: str
    value: bool
    evidence_id: str
    root_id: str


class Correction(Strict):
    correction_id: str
    old_version_ids: tuple[str, ...]
    replacements: tuple[EvidenceVersion, ...]
    from_epoch: int
    to_epoch: int
    kind: Literal["factual_update", "no_event"] = "factual_update"
    notice: str

    @model_validator(mode="after")
    def epoch_contract(self):
        if self.kind == "no_event":
            assert not self.old_version_ids and not self.replacements
            assert self.to_epoch == self.from_epoch
        else:
            assert self.to_epoch == self.from_epoch + 1
            assert len(self.old_version_ids) == len(self.replacements) > 0
            assert set(self.old_version_ids) == {x.supersedes for x in self.replacements}
            assert all(x.epoch == self.to_epoch for x in self.replacements)
        return self


class ClaimDraft(Strict):
    slot: str
    value: bool
    refs: tuple[str, ...] = Field(default=(), max_length=12)


class ClaimRecord(ClaimDraft):
    claim_id: str
    owner: Literal["A", "B", "C"]
    created_epoch: int
    created_call_id: str
    supersedes: str | None = None


class ActionDraft(Strict):
    job: Literal["target", "control"]
    verb: Literal["publish", "dispatch", "wait", "reserve"]
    resource: str | None = None
    value: bool | None = None
    amount_cents: int | None = Field(default=None, ge=0)
    route: Literal["DEPT", "VP", "CFO", "BOARD"] | None = None
    refs: tuple[str, ...] = Field(default=(), max_length=12)

    @model_validator(mode="after")
    def arguments(self):
        if self.verb == "publish":
            assert self.value is not None and self.resource is None
            assert self.amount_cents is None and self.route is None
        elif self.verb == "dispatch":
            assert self.resource is not None and self.value is None
            assert self.amount_cents is None and self.route is None
        elif self.verb == "reserve":
            assert self.resource is not None and self.value is None
            assert self.amount_cents is not None and self.route is not None
        else:
            assert self.resource is None and self.value is None
            assert self.amount_cents is None and self.route is None
        return self


class ActionRecord(ActionDraft):
    action_id: str
    owner: Literal["C"] = "C"
    created_epoch: int
    created_call_id: str
    supersedes: str | None = None
    idempotency_key: str


class ActionCommand(Strict):
    operation: Literal["new", "keep", "revalidate", "cancel"]
    target_action_id: str | None = None
    proposal: ActionDraft | None = None

    @model_validator(mode="after")
    def command_contract(self):
        if self.operation == "new":
            assert self.proposal is not None  # target, if provided, is atomically superseded
        else:
            assert self.target_action_id is not None and self.proposal is None
        return self


class AgentReply(Strict):
    ack_epoch: int = Field(ge=0)
    claims: tuple[ClaimDraft, ...] = Field(default=(), max_length=4)
    retain_claims: tuple[str, ...] = Field(default=(), max_length=12)
    actions: tuple[ActionCommand, ...] = Field(default=(), max_length=2)
    note: str = Field(default="", max_length=160)  # audit only; never persistent prompt state


class SupportLabel(Strict):
    node_id: str
    minimal_sets: tuple[tuple[str, ...], ...] = Field(max_length=32)
    provenance: Literal["estimated", "declared", "exact_available", "exact_global", "coarse"]
    view_hash: str
    syntax_valid: bool = True
    error: str | None = None


class ExtractedNode(Strict):
    n: str
    j: tuple[tuple[str, ...], ...] = Field(max_length=32)


class ExtractorReply(Strict):
    supports: tuple[ExtractedNode, ...] = Field(max_length=14)


class ReadReceipt(Strict):
    call_id: str
    actor: Literal["A", "B", "C", "EXTRACTOR", "REVIEWER"]
    epoch: int
    visible_ids: tuple[str, ...]
    delivered_evidence_ids: tuple[str, ...]
    prompt_sha256: str


class ReviewerReply(Strict):
    review: str = Field(max_length=2400)


class GraphEdge(Strict):
    source: str
    target: str
    kind: Literal["exposed_to", "declared_ref", "delivered", "supersedes", "produced"]
    call_id: str | None = None


class Message(Strict):
    message_id: str
    sender: Literal["A", "B", "C", "SYSTEM"]
    recipient: Literal["A", "B", "C"]
    epoch: int
    claim_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    delivery_step: int
    protocol_error: str | None = None


class Disposition(Strict):
    record_id: str
    status: Literal["ACTIVE", "WITHDRAWN", "SUPERSEDED", "PROPOSED", "SUSPENDED", "READY", "EXECUTED", "CANCELLED"]
    epoch: int
    reason: str
    policy: str


class RepairPlan(Strict):
    policy: str
    correction_id: str
    withdraw_claims: tuple[str, ...] = ()
    suspend_actions: tuple[str, ...] = ()
    notices: tuple[str, ...] = ()
    reset_agents: tuple[Literal["A", "B", "C"], ...] = ()
    mask_source: Literal["none", "exposure", "estimated", "oracle", "coarse_oracle"]
    fallback_nodes: tuple[str, ...] = ()


class AgentState(Strict):
    actor: Literal["A", "B", "C"]
    acknowledged_epoch: int
    delivered_evidence_ids: tuple[str, ...]
    owned_claim_ids: tuple[str, ...]
    pending_action_ids: tuple[str, ...]
    inbox_message_ids: tuple[str, ...]


class PublicWorld(Strict):
    world_id: str
    task_rules: str
    claim_slots: tuple[str, ...]
    source_owners: dict[str, str]
    evidence: tuple[EvidenceVersion, ...]
    action_mode: Literal["unbound", "bound"]
    jobs: tuple[Literal["target", "control"], ...] = ("target", "control")


class OracleWorld(Strict):
    world_id: str
    base_world_id: str
    family: Literal["match", "threshold", "capex"]
    alternative: bool
    bound: bool
    atoms_before: tuple[AtomObservation, ...]
    atoms_after: tuple[AtomObservation, ...]
    claim_formulas: dict[str, Expr]
    action_formula_templates: dict[str, Expr]
    correction: Correction
    generator_seed: int
    numeric_domains: dict[str, tuple[int | bool, ...]] = Field(default_factory=dict)
    numeric_grader_id: str | None = None


class Snapshot(Strict):
    snapshot_id: str
    public_world: PublicWorld
    epoch: int
    current_version_by_key: dict[str, str]
    evidence_history: tuple[EvidenceVersion, ...]
    agents: tuple[AgentState, ...]
    claims: tuple[ClaimRecord, ...]
    actions: tuple[ActionRecord, ...]
    dispositions: tuple[Disposition, ...]
    messages: tuple[Message, ...]
    queued_message_ids: tuple[str, ...]
    read_receipts: tuple[ReadReceipt, ...]
    edges: tuple[GraphEdge, ...]
    applied_action_ids: tuple[str, ...]
    rng_seeds: dict[str, int]
    event_offset: int
    batch_offset: int = 0
    event_chain_sha256: str
    config_sha256: str


class RuntimeView(Strict):
    actor: Literal["A", "B", "C"]
    epoch: int
    task_rules: str
    current_evidence: tuple[EvidenceVersion, ...]
    active_claims: tuple[ClaimRecord, ...]
    pending_actions: tuple[ActionRecord, ...]
    dispositions: tuple[Disposition, ...]
    visible_ids: tuple[str, ...]
    repair_notice_ids: tuple[str, ...]
    edges: tuple[GraphEdge, ...]
    view_sha256: str


class EstimatedSupportView(Strict):
    checkpoint_sha256: str
    extraction_call_id: str
    labels: tuple[SupportLabel, ...]


class ModelLock(Strict):
    model_id: str
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    tokenizer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    weights_sha256: dict[str, str]
    dtype: Literal["float16"]
    quantization: Literal["none", "nf4_double"]
    environment_lock_sha256: str
    backend_fingerprint: str


class RunItem(Strict):
    run_id: str
    base_world_id: str
    world_id: str
    family: Literal["match", "threshold", "capex"]
    alternative: bool
    bound: bool
    replicate: int
    block: str
    policy: str
    model_lock_sha256: str
    prefix_checkpoint_sha256: str | None = None
    prefix_seed: int
    suffix_seeds: dict[str, int]
    world_public_path: str
    world_private_path: str  # manifest is not an inference-worker input


class RunManifest(Strict):
    experiment_id: str
    matrix: Literal["A", "B"]
    config_sha256: str
    preregistration_sha256: str
    generator_revision: str
    prompt_sha256: dict[str, str]
    model_locks: tuple[ModelLock, ...]
    items: tuple[RunItem, ...]
    created_utc: str


class InferenceRequest(Strict):
    call_id: str
    model_revision: str
    tokenizer_revision: str
    backend_fingerprint: str
    rendered_prompt: str
    prompt_sha256: str
    seed: int
    temperature: float
    top_p: float
    top_k: int
    max_new_tokens: int
    role: Literal["agent", "extractor", "reviewer", "single"]
    schema_version: Literal["1.0"] = "1.0"


class InferenceResult(Strict):
    call_id: str
    raw_text: str
    input_tokens: int
    output_tokens: int
    elapsed_seconds: float
    finish_reason: Literal["stop", "length", "infrastructure_error"]
    cache_hit: bool
    attempts: int
    gpu_id: str
    error: str | None = None


class ActionAttempt(Strict):
    action_id: str
    epoch: int
    requested_by: Literal["C"]
    lifecycle_allowed: bool
    block_reason: str | None
    applied: bool


class Failure(Strict):
    call_id: str | None
    kind: Literal["parse", "schema", "semantic", "timeout", "oom", "context_overflow", "storage", "invariant"]
    message: str
    retryable: bool


class Event(Strict):
    schema_version: Literal["1.0"] = "1.0"
    event_id: str
    branch_id: str
    seq: int
    epoch: int
    logical_step: int
    actor: str
    kind: Literal["evidence", "correction", "claim", "action", "message", "read", "disposition", "repair_plan", "inference", "attempt", "failure", "checkpoint"]
    payload: dict[str, Any]  # validated against PAYLOAD_MODELS below before append
    previous_sha256: str
    sha256: str


class EventBatch(Strict):
    batch_id: str
    branch_id: str
    events: tuple[Event, ...] = Field(min_length=1)
    previous_batch_sha256: str
    sha256: str

    @model_validator(mode="after")
    def same_branch(self):
        assert all(e.branch_id == self.branch_id for e in self.events)
        return self


class CheckpointReceipt(Strict):
    snapshot_id: str
    snapshot_sha256: str
    relative_path: str
    complete: bool


PAYLOAD_MODELS = {
    "evidence": EvidenceVersion, "correction": Correction, "claim": ClaimRecord,
    "action": ActionRecord, "message": Message, "read": ReadReceipt,
    "disposition": Disposition, "repair_plan": RepairPlan,
    "inference": InferenceResult, "attempt": ActionAttempt, "failure": Failure,
    "checkpoint": CheckpointReceipt,
}


def validate_event_payload(event: Event) -> Strict:
    return PAYLOAD_MODELS[event.kind].model_validate_json(
        json.dumps(event.payload, allow_nan=False), strict=True)


class BranchOutcome(Strict):
    branch_id: str
    base_world_id: str
    world_id: str
    family: str
    alternative: bool
    bound: bool
    policy: str
    model: str
    replicate: int
    prefix_correct: bool
    protocol_ok: bool
    target_correct: bool
    control_correct: bool
    invalid_attempt: bool
    invalid_applied: bool
    safe_correct_completion: bool
    newly_unsupported: int
    retained_unsupported: int
    valid_withdrawn: int
    stale_reference_count: int
    replacement_count: int
    input_tokens: int
    output_tokens: int
    recovery_seconds: float
    extractor_tokens_allocated: int
    infrastructure_status: Literal["complete", "terminal_failure", "incomplete"]


class NodeEvaluation(Strict):
    branch_id: str
    node_id: str
    kind: Literal["claim", "action"]
    owner: str
    truth_valid: bool
    task_correct: bool
    priority_adherent: bool | None  # actions only; null for claims
    has_available_support: bool
    authorized: bool
    runtime_status: str
    support_before: tuple[tuple[str, ...], ...]
    support_after: tuple[tuple[str, ...], ...]
    predicted_support: tuple[tuple[str, ...], ...] | None
    became_unsupported: bool
    stale_reference_ids: tuple[str, ...]


class MatrixRow(Strict):
    id: str
    base_worlds: int
    variants: int
    prefix_calls_per_world: int = 0
    extraction_calls_per_world: int = 0
    arms: tuple[str, ...] = ()
    recovery_calls_per_arm: int = 0
    reviewer_calls_per_world: int = 0
    single_calls_per_world: int = 0
    new_prefix: bool
    subset: str
    model: str = "Qwen/Qwen3-4B"


class ExperimentConfig(Strict):
    schema_version: Literal["1.0"] = "1.0"
    experiment_id: str
    root_seed: int
    aggregate_gpu_hours: float
    pilot_and_reserve_hours: float
    agent_max_new_tokens: int
    long_max_new_tokens: int
    context_limit: int
    temperature: float
    top_p: float
    top_k: int
    rows: tuple[MatrixRow, ...]
