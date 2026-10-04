# M2-T01 — Permitted peer views and lossless rendering

**Status:** active

**Dependencies:** [M1-T03](../M1/M1-T03-complete-schedules.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md), [plan state boundaries](../../IMPLEMENTATION_PLAN.md#state-and-information-boundaries), and [M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§3.1](../../../PROJECT_SPECIFICATION.md#31-state-and-visibility), [§4.3–4.4](../../../PROJECT_SPECIFICATION.md#43-historical-information--retained-representation), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [application semantics](../../implementation-research/state-and-replay.md#semantics-that-belong-to-the-application) and [template risks](../../implementation-research/inference-and-capacity.md#rendering-termination-and-call-independence).

## Intended outcome

One renderer accepts only a peer's permitted view and preserves the specified distinction between current source authority and retained derived work.

## Scope and boundaries

- Represent current sources, history, candidate validity/absence, feedback, and persistent notices/assigned receipts as distinguishable fields within ordinary records.
- Public task definitions, source-ID/owner manifest, output assignment, positions/node set and one short task-specific hint are permitted. Use one generic current-source/history instruction across conditions; do not impose a route, leader, proof, chain-of-thought or external solver.
- Render current records once in stable order outside history. Initially expose only private records. An unknown replacement is pending; a known tombstone carries deleted endpoints/status and counts as current evidence without an active edge.
- Keep notices/receipts outside clearable history. Receipt before-values are historical, never forwardable current evidence. Model-generated old values remain retained derived text.
- History consists of permitted own replies, received prose and bounded public feedback with phase/round labels, not old source-table renders or resolved forwarding payloads. Preserve special-looking text as labeled data instead of assistant turns that a template can rewrite. Avoid duplicate rendering of the latest candidate already in a reply; preserve K's explicit historical candidate/absence.
- Host worlds, evaluator fields and schedule labels must not be renderer inputs. Branch/policy/reset/subset labels, future edits, hidden values, gold and anticipated effects remain offline. Queue internals cannot become prompt metadata.

## Completion criteria

- Public IDs/order reveal no hidden values or BFS endpoints.
- A rendered request and its tokenizer input can be saved exactly and compared later; all rendering is deterministic for an equal permitted view.
- Current evidence, historical values, pending updates and tombstones have unambiguous, separately testable behavior.
- Literal text preservation and visibility pass CPU tests. Complete context-capacity admission remains M2-T06, not a claim from short fixtures.

## Validation and evidence

Use paired worlds with hidden sentinel values and change hidden gold, future edits, condition fields, BFS endpoints and queue text independently. The unaffected peer render must remain identical. Test no duplicated raw tables/payloads, exact preservation of escaped/special-looking archived strings, explicit invalid-candidate absence, and value-independent ordering. Include notice, receipt, feedback and source-delivery metadata layouts in the audit.

**Start evidence (4 October 2026):** Inspected the task contract, specification
§§2.1, 3–4 and 9, plan state boundaries/M2, research synthesis and the relevant
state/template investigations. Re-ran `python -S -m recovery validate` on Windows /
CPython 3.11.9: all **59/59 prerequisite CPU checks pass**, with site packages
disabled. M1's gate remains passed. Implement immutable, explicitly permitted
records and one lossless renderer first, then audit hidden-field independence,
source/receipt/history semantics and exact template/token inputs. Complete
capacity admission remains M2-T06; this task makes no inference or freeze claim.

**Renderer checkpoint:** [state.py](../../../recovery/state.py) now projects
private shards/complete-world controls into immutable permitted records and
resolves only held current versions. [prompts.py](../../../recovery/prompts.py)
renders one user-data archive, separate current sources, notices/receipts,
candidate status and public feedback, with source metadata free of payloads or
queue labels. `python -S -m unittest tests.test_peer_views -v` passes **19/19**
focused checks across both sizes/all families, hidden-field pairs, pending and
deleted records, historical receipts, wrong/absent compact candidates,
literal escaped text, release ordering, fresh processes and the context boundary.

The optional [native tokenizer harness](../../../tests/tokenizer_peer_views.py)
passes **5/5** CPU checks with Qwen3.5-9B revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`, Transformers 5.12.0,
Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0. Local tokenizer JSON,
configuration and template bytes were compared directly with that immutable
upstream revision. [Seven saved short fixtures](../../../tests/fixtures/peer_requests.json)
retain exact request content, native template text, token IDs and attention masks;
input lengths are 757–1,830 tokens, plus the full 384-token output reserve.
This is short-fixture evidence, not a complete capacity bound. The first harness
invocation pointed at the parent containing `9B`/`4B` folders; it failed before
writing a fixture. Using the actual `9B` metadata directory passed without a
dependency or protocol change. Full-suite, installed-package and handoff checks
remain before task completion.

**Latest-slot review checkpoint:** A focused regression first reproduced a
state-construction defect: an older candidate could remain marked valid after a
newer own reply or feedback slot. The permitted-view guard now rejects that
combination, including an unexecuted marker with recorded own work. Matching
invalid/failed outcomes keep an explicit absent candidate. The regression and all
**20/20 focused checks pass**; the full saved-population/schedule CPU run passes
**79/79**, and the native tokenizer rerun still passes **5/5** with unchanged saved
request/token bytes. This strengthens the existing no-inherited-answer invariant
without implementing M2-T02's parser or altering scientific design.

**Prerequisite handoff (4 October 2026):** [M1-T03 gate evidence](../M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate)
passes with all 59 CPU checks, including M1-T01/T02, complete schedules/replay
dependencies and the retained prepared schedule. M1's gate is passed; this task
is ready. Renderer/protocol implementation and acceptance remain unstarted.

