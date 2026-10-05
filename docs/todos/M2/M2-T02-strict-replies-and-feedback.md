# M2-T02 — Strict reply validation and public feedback

**Status:** done

**Dependencies:** [M2-T01](../M2/M2-T01-peer-views-and-rendering.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), and [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls).
- Technical evidence: [strict parsing](../../implementation-research/repository-and-validation.md#strict-parsing-needs-two-small-layers).

## Intended outcome

A complete reply receives one deterministic protocol-valid/invalid result, with lawful messages and bounded public feedback, without judging or repairing mathematical correctness.

## Scope and boundaries

- Decode one complete JSON object before strict Pydantic 2 validation. Reject duplicate keys recursively, nonfinite constants/overflow/coercion, booleans/floats/strings as integers, extra nested fields, fences, trailing prose and incomplete fragments.
- Require candidate/send schemas, task-specific integer shapes and canonical full BFS keys. Full-information controls require empty sends and complete-world candidate lengths.
- Validate against the immutable sender view: another peer as recipient, at most one message per recipient/three total, and at most eight distinct currently held ID/version references per recipient. Repetition of a valid reference is not independently forbidden by the distinct-reference limit.
- Apply actual tokenizer limits: 384 generated tokens, 128 prose tokens summed across message texts and at most 32 feedback tokens per slot. Complete valid JSON at the output cap is valid; record termination separately from truncation.
- Any invalid message invalidates the entire reply, including its candidate and all sends. Wrong numbers in a structurally valid candidate remain valid protocol output.
- Deliver only schema/permission feedback at the next scheduled call. Never echo hidden payloads, library validation dumps, correctness, or extra opportunities. Failed/invalid slots have no new candidate; never inherit an earlier answer.

## Completion criteria

- Parsing, structural validity, permissions, token limits and numeric correctness are separate concepts and outputs.
- Invalid replies produce zero staged messages and an explicit invalid/absent candidate.
- Raw replies remain unchanged for audit/history under the retention contract; no JSON repair, sorting, fragment extraction or schema-constrained generation is introduced.
- Feedback remains useful, public and within the actual token cap.

## Validation and evidence

The evidence below records this task's original 4 October 2026 completion.
M2-T06 renewed its request archives and affected checks after the authorized
5 October renderer/protocol revision; see the renewal at the end. Original
measurements and handoff status are historical, not current gate claims.

Test duplicate keys at every nesting level, nonfinite/huge exponent tokens, coercions, wrong lengths, BFS key "01", extra fields, self/unknown/duplicate recipients, stale/unheld refs, repeated lawful refs, per-recipient distinct-reference limits and aggregate prose limits. Include a valid candidate with one invalid send, wrong but valid integers, complete cap-ending JSON, malformed outputs below/at cap, failed slots, and feedback sentinel leaks. Preserve repeated delivery attempts for later accounting.

**Evidence:** Implementation started 4 October 2026 from clean commit `fd44e57`.
The prerequisite source command `python -S -m recovery validate --manifest
tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json
--authoritative tests/fixtures/population_target.json` passed all 79 checks on
Windows / CPython 3.11.9. M1's gate and M2-T01's artifacts are present.

**Implementation checkpoint:** [protocol.py](../../../recovery/protocol.py)
implements the complete decoder, strict nested Pydantic schemas, public candidate
contracts, sender-view permissions, physical output/prose/feedback caps and
all-or-none immutable staging. [protocol_checks.py](../../../tests/protocol_checks.py)
passes 23 focused CPU checks on both local Pydantic 2.12.5 and installed 2.13.5
with CPython 3.11.9. At this checkpoint, full source integration passed 102
checks before the additional missing-dependency CLI regression; final counts
appear in the completion evidence below.
`pip check` passes in `.venv`. Pydantic 2 is the required schema dependency;
`validate --core-only` explicitly preserves the earlier standard-library subset.
No accepted inference environment or scientific configuration is changed.

**Native-tokenizer checkpoint:** [tokenizer_protocol.py](../../../tests/tokenizer_protocol.py)
passes six checks against the 20 saved synthetic cases in
[protocol_replies.json](../../../tests/fixtures/protocol_replies.json). Qwen3.5-9B
revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` uses Transformers 5.12.0,
Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0 in the local CPU
environment. All four metadata files (`config.json`, `tokenizer.json`,
`tokenizer_config.json`, `chat_template.jinja`) match the pinned upstream bytes
in a fresh comparison. No weights are loaded. Eight distinct references with
nine actual delivery attempts pass; nine distinct references fail. Aggregate
128/129 prose tokens produce valid/invalid replies at 180/181 generated tokens.
A complete closing brace at token 384 is accepted with length termination;
385 tokens and a truncated fragment at 384 are invalid. All fixed feedback fits
32 actual tokens. The five M2-T01 native checks still pass with unchanged saved
requests/token IDs. [Fixture documentation](../../../tests/fixtures/README.md#strict-replies-and-actual-tokenizer-limits)
records reproduction and the remaining capacity/inference boundaries.

Executed native commands:

```powershell
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

**Prerequisite handoff (4 October 2026):** [M2-T01 completion evidence](M2-T01-peer-views-and-rendering.md#completion-and-handoff)
passes with 79 standard-library CPU checks and five native-tokenizer checks.
Immutable permitted views, held-current-source lookup, literal request rendering,
candidate absence/age guards and fixed public feedback layouts are available.
At that prerequisite handoff, this task became ready and its strict parser,
whole-reply validation and tokenizer permissions were unimplemented. The verified
completion below supersedes that status; M2's complete protocol/capacity gate
remains open.

## Completion and handoff

**Verified 4 October 2026:** Windows x64 / CPython 3.11.9. Full source validation
passes **103/103** checks using Pydantic 2.12.5; the installed editable package
passes **103/103** using Pydantic 2.13.5 while preparing/validating a fallback
schedule outside the checkout. These comprise 80 dependency-free core checks
(79 prerequisites plus a missing-dependency regression) and 23 protocol checks.
Explicit site-disabled core validation passes **80/80**. The native protocol
harness passes **6/6**, and the original renderer harness still passes **5/5**.
`pip check` and `git diff --check` pass. No model weights, GPU/model calls,
experiment outcomes, scientific-design changes or accepted freeze are involved.

Executed final integration commands:

```powershell
python -m unittest tests.protocol_checks -v
python -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate --core-only
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest tests.protocol_checks -v
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The outside-checkout harness used `.venv/Scripts/python.exe -m recovery prepare`
with `--manifest <absolute population_fallback.json> --authoritative <same
population> --config <temporary fallback.toml> --output <new schedules.json>`,
then `validate` with the same inputs plus `--schedule <new schedules.json>`.
The temporary configuration contained exactly `size = "fallback"`. Saved
population/schedule inputs were validated without resampling. Both environments
are CPU validation evidence, not an accepted M5 inference lock.

| Acceptance area | Executed evidence | Result |
|---|---|---|
| Complete strict JSON | Decoder adversaries in [protocol_checks.py](../../../tests/protocol_checks.py) | Duplicate keys at every level, escaped-key collisions, constants/exponent overflow, excessive integer decoding, fences, fragments, trailing prose/markers and multiple objects fail. Whitespace is allowed; no repair or extraction occurs. |
| Exact public schemas and candidate shapes | All-family/both-size/all-peer/control loops, nested-schema and BFS-key checks | Required candidate/send, exact integer types, nested extra-field rejection, lengths and canonical full BFS keys pass. Null optional values are rejected; omitted fields are lawful. Control sends must be empty and Prefix/Sort control candidates complete. Wrong, negative, unsorted and repeated integers remain protocol-valid and unchanged; offline exact scoring stays separate. |
| Sender-view permissions | Recipient/source/revision/tombstone/reference-limit cases | Self/unknown/duplicate recipients, stale/unheld/pending refs and nine distinct refs fail. Three other recipients and eight distinct refs per recipient pass. Exact current payloads are staged from the sender only; known tombstones stay deleted. Repetitions remain separate delivery attempts. |
| Whole-reply failure | Correct candidate plus invalid send, stage absence checks | Any invalid send discards every message and candidate. Public stage checks/counts remain distinct from correctness; no recipient view changes during validation. |
| Literal raw audit/history | Purity/repeatability, special-text and native-ID fixtures | Exact text/IDs/termination survive validation; own replies remain literal labeled history. Numeric list order/multiplicity stay unchanged. BFS key order is semantically irrelevant while raw key spelling/order stays archived. Unexpected special markers are not stripped. |
| Actual tokenizer caps | [20 native fixtures](../../../tests/fixtures/protocol_replies.json) and six native checks | Generated IDs govern 384; literal texts are separately tokenized and summed to 128. Complete JSON closes at token 384 and passes despite length termination. 385 tokens, malformed below/at cap and known truncation fail. Eight distinct references with nine attempts pass; nine distinct fail. |
| Public feedback and timing | Sentinel/host-error cases, native feedback guard and next-view checks | Only fixed public descriptions render, all within 32 actual tokens. No supplied sentinel, hidden payload, library validation dump or correctness enters feedback. Generating-slot labels prevent same-call exposure; feedback can enter the next scheduled view. Incompatible feedback tokenization is a configuration error, never silent truncation. |
| Invalid/failed/unexecuted distinction | Latest-slot/history/failure cases | Invalid and recorded failed slots have absent new candidates even with earlier valid history. Failure has no fabricated generation/feedback. Unexecuted remains distinct. Validation adds no calls or retries. |
| Integration and dependencies | Source/installed 103-check suites, 80 core-only checks, original five native checks, `pip check` | M1 task/population/schedule evidence and exact saved request/token fixtures remain valid. Pydantic is a declared CPU dependency; full validation cannot silently omit protocol checks. No inference stack is imported by those CPU checks. |

**M2-T02 is done; [M2-T03](M2-T03-synchronous-rounds-and-prefixes.md) is ready.**
Use `GeneratedReply`, `validate_reply` / `failed_reply`, `ReplyValidation` and
`StagedMessage` directly for the fixed barrier. Successful stages hold immutable
sender payloads and every repeated reference attempt, plus optional literal
text; invalid/failed stages are empty. Candidate/own-reply/feedback outcomes carry
their generating slot. The next task owns message relationships, synchronous
commits, source acquisition and immutable-prefix construction; this task applies
no deliveries. Retention/events, exact mixed/Q reuse and complete attainable/worst
context capacity remain M2-T04–T06; durable persistence/retry accounting remains
M3. M2's milestone gate is open.

Final documentation audit passes **437 local links/anchors in 39 documents**,
balanced fences/text checks and all **29 task/index status comparisons**: five
done, one ready, 23 blocked. M2 is 2/6 done with M2-T03 ready. Git comparison
against `fd44e57` confirms the specification, size configuration, M1 code and
input/schedule fixtures, renderer/request fixture, vendor and research remain
unchanged. The new 20-case reply fixture has canonical UTF-8/LF bytes. The only
new runtime dependency is the specification's Pydantic 2 schema layer.


## Renewal under M2-T06

On 5 October 2026, the finalized literal-block renderer, column metadata,
footer and scalar-message boundary passed this task's 7 native checks.
Its canonical archive was renewed and reproduced in a fresh hash-seed-37
process; source and installed-library validation also passed. Current
archive measurements are in the [fixture instructions](../../../tests/fixtures/README.md).
[M2-T06 completion](M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records the full validation, complete capacity admission and M2 gate.
