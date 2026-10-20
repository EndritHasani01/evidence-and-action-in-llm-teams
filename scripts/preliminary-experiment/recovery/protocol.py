"""Strict whole-reply validation (spec §§3.2, 5.1, 8.1).

Only an immutable sender view and recorded output enter validation. No evaluator,
world lookup, delivery, inference, repair or retry occurs here. Generated IDs
measure the physical output; re-encoding its text is not a substitute.
"""

from dataclasses import dataclass
import json
import math

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .prompts import ProtocolLimits, THESIS_LIMITS
from .state import CandidateState, Feedback, OwnReply, PeerView, Slot, held_source
from .tasks import PEERS, SourceRecord, candidate_contract

MAX_OUTPUT_TOKENS = THESIS_LIMITS.output_tokens
MAX_RECIPIENTS = THESIS_LIMITS.recipients
MAX_DISTINCT_REFERENCES = THESIS_LIMITS.distinct_references
MAX_PROSE_TOKENS = THESIS_LIMITS.prose_tokens
MAX_FEEDBACK_TOKENS = THESIS_LIMITS.feedback_tokens


class _SourceReference(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    record_id: str
    version: int


class _Message(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    to: int
    source_refs: list[_SourceReference] = Field(default_factory=list)
    text: str = ""

    @field_validator("text")
    @classmethod
    def unicode_scalars(cls, text: str) -> str:
        # json.loads combines a valid escaped pair into one scalar. An
        # unpaired surrogate has no native UTF-8 tokenizer representation.
        # Reject the entire reply before counting/staging; never repair text.
        if any(0xD800 <= ord(char) <= 0xDFFF for char in text):
            raise ValueError("message text must contain Unicode scalars")
        return text


class _Reply(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    candidate: list[int] | dict[str, int]
    send: list[_Message]


@dataclass(frozen=True, slots=True)
class GeneratedReply:
    """Exact reply text/IDs, supplied by the later inference/recording boundary.

    No special-token stripping or text cleanup is done by this module. A length
    termination is independent of actual truncation: complete JSON at the cap
    is legal. `truncated` records a known loss of reply content, not a length stop.
    """

    text: str
    token_ids: tuple[int, ...]
    termination: str
    truncated: bool = False

    def __post_init__(self) -> None:
        if (type(self.text) is not str or type(self.token_ids) is not tuple
                or any(type(i) is not int or i < 0 for i in self.token_ids)
                or type(self.termination) is not str or not self.termination
                or type(self.truncated) is not bool):
            raise ValueError("record exact text, generated IDs and termination separately")


@dataclass(frozen=True, slots=True)
class StagedMessage:
    """Host-side outgoing data; no recipient state has been changed.

    Repeated references remain repeated source-delivery attempts. The next task
    assigns branch/message relationships and commits at the round barrier.
    Absent text is distinct from an explicitly submitted empty string.
    """

    sender: int
    recipient: int
    slot: Slot
    sources: tuple[SourceRecord, ...]
    text: str | None


@dataclass(frozen=True, slots=True)
class ReplyValidation:
    """Public validity stages and host audit data, without numeric correctness.

    None means a check was not reached, or no generation exists (failed slot).
    A valid candidate is only a protocol result, never an assertion of accuracy.
    Own replies and feedback carry the generating slot, so PeerView permits them
    only in a later scheduled call. Invalid/failed outcomes replace any earlier
    candidate with explicit absence.
    """

    generated: GeneratedReply | None
    json_valid: bool | None
    schema_valid: bool | None
    permissions_valid: bool | None
    prose_tokens: int | None
    candidate: CandidateState
    messages: tuple[StagedMessage, ...] = ()
    feedback: Feedback | None = None
    feedback_tokens: int = 0

    @property
    def protocol_valid(self) -> bool:
        return self.candidate.status == "valid"

    @property
    def output_tokens(self) -> int | None:
        return None if self.generated is None else len(self.generated.token_ids)

    @property
    def output_within_limit(self) -> bool | None:
        """Thesis compatibility shorthand; course audits pass explicit limits."""
        return self.output_fits()

    @property
    def prose_within_limit(self) -> bool | None:
        """Thesis compatibility shorthand; course audits pass explicit limits."""
        return self.prose_fits()

    def output_fits(self, limits: ProtocolLimits = THESIS_LIMITS) -> bool | None:
        return None if self.output_tokens is None else self.output_tokens <= limits.output_tokens

    def prose_fits(self, limits: ProtocolLimits = THESIS_LIMITS) -> bool | None:
        return None if self.prose_tokens is None else self.prose_tokens <= limits.prose_tokens

    @property
    def own_reply(self) -> OwnReply | None:
        return (None if self.generated is None
                else OwnReply(self.candidate.slot, self.generated.text))


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("nonfinite JSON constant")


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite JSON number")
    return result


def token_count(text: str, tokenizer) -> int:
    """Count literal prose/feedback with the injected actual tokenizer.

    Do not count serialized JSON escaping as prose, join recipient texts, or add
    special tokens. Invalid tokenizer behavior is a host configuration error.
    """

    ids = tokenizer.encode(text, add_special_tokens=False)
    if (type(ids) not in (list, tuple)
            or any(type(i) is not int or i < 0 for i in ids)):
        raise ValueError("tokenizer must return an integer sequence")
    return len(ids)


def public_feedback(slot: Slot, code: str, tokenizer, *,
                    limits: ProtocolLimits = THESIS_LIMITS) -> tuple[Feedback, int]:
    feedback = Feedback(slot, code)
    count = token_count(feedback.text, tokenizer)
    if count > limits.feedback_tokens:
        raise ValueError("public feedback exceeds tokenizer cap; protocol configuration cannot be used")
    return feedback, count


def _schema_code(error: ValidationError) -> str:
    # Only inspect declared top-level locations. No supplied values, unknown key
    # names, exception strings or library error dumps enter public feedback.
    errors = error.errors(include_input=False, include_context=False, include_url=False)
    locations = [e["loc"] for e in errors]
    if (any(not loc or loc[0] not in ("candidate", "send")
            or (loc[0] == "send" and len(loc) == 1) for loc in locations)
            or any(e["type"] == "missing" and len(e["loc"]) == 1 for e in errors)):
        return "reply_schema"
    if any(loc[0] == "candidate" for loc in locations):
        return "candidate_shape"
    return "message_schema"


def _permissions(reply: _Reply, view: PeerView, limits: ProtocolLimits) -> str | None:
    if view.peer is None:
        return "control_send" if reply.send else None
    recipients = [message.to for message in reply.send]
    if (len(recipients) > limits.recipients or len(set(recipients)) != len(recipients)
            or any(to not in PEERS or to == view.peer for to in recipients)):
        return "recipient"
    for message in reply.send:
        if len({(ref.record_id, ref.version) for ref in message.source_refs}) > limits.distinct_references:
            return "reference_limit"
        if any(held_source(view, ref.record_id, ref.version) is None for ref in message.source_refs):
            return "source_reference"
    return None


def validate_reply(view: PeerView, generated: GeneratedReply, tokenizer, *,
                   limits: ProtocolLimits = THESIS_LIMITS) -> ReplyValidation:
    """Deterministically validate one recorded reply, then stage all or nothing.

    Error precedence is JSON/truncation, output cap, schema/shape, permissions,
    prose cap. Reached checks are recorded separately; wrong integer answers are
    never diagnosed here. No result can change a sender/recipient view.
    """

    if type(view) is not PeerView or type(generated) is not GeneratedReply:
        raise ValueError("validate a recorded generation against its immutable sender view")
    if type(limits) is not ProtocolLimits:
        raise ValueError("validation requires adopted protocol limits")
    json_valid = False
    schema_valid = permissions_valid = None
    prose_tokens = None
    reply = None
    code = None
    try:
        data = json.loads(generated.text, object_pairs_hook=_unique_object,
                          parse_constant=_reject_constant, parse_float=_finite_float)
        if type(data) is not dict:
            raise ValueError("JSON object required")
        json_valid = True
    except (ValueError, RecursionError):
        code = "json"
    if json_valid:
        try:
            reply = _Reply.model_validate(data, strict=True)
            schema_valid = candidate_contract(view.task, view.size, view.peer).error(reply.candidate) is None
            if not schema_valid:
                code = "candidate_shape"
        except ValidationError as error:
            schema_valid = False
            code = _schema_code(error)
    if reply is not None:
        prose_tokens = sum(token_count(message.text, tokenizer) for message in reply.send)
        if schema_valid:
            code = _permissions(reply, view, limits)
            permissions_valid = code is None
            if code is None and prose_tokens > limits.prose_tokens:
                code = "prose_limit"
    if generated.truncated or not json_valid:
        code = "json"
    elif len(generated.token_ids) > limits.output_tokens:
        code = "output_limit"
    if code is not None:
        feedback, count = public_feedback(view.slot, code, tokenizer, limits=limits)
        return ReplyValidation(generated, json_valid, schema_valid, permissions_valid, prose_tokens,
                               CandidateState("invalid", view.slot), feedback=feedback, feedback_tokens=count)
    candidate = CandidateState.valid(view.task, view.size, view.peer, view.slot, reply.candidate)
    messages = tuple(StagedMessage(
        view.peer, message.to, view.slot,
        tuple(held_source(view, ref.record_id, ref.version) for ref in message.source_refs),
        message.text if "text" in message.model_fields_set else None) for message in reply.send)
    return ReplyValidation(generated, json_valid, schema_valid, permissions_valid, prose_tokens,
                           candidate, messages)


def failed_reply(view: PeerView) -> ReplyValidation:
    """A recorded infrastructure failure, distinct from invalid/unexecuted output.

    Failure details/attempt accounting belong in the later durable ledger. No
    fabricated raw reply, schema feedback, prior candidate or retry is supplied.
    """

    if type(view) is not PeerView:
        raise ValueError("failure requires its scheduled peer view")
    return ReplyValidation(None, None, None, None, None, CandidateState("failed", view.slot))
