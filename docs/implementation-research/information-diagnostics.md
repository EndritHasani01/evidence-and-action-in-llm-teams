# Offline information and work diagnostics

This is the conservative engineering rubric for
[M4-T03](../todos/M4/M4-T03-information-and-work-diagnostics.md), implementing
[specification §7.2](../../PROJECT_SPECIFICATION.md#72-what-information-and-work-survived).
It is ready for the later M5 freeze; this document does not freeze an inference
configuration or add a scientific requirement.

## Source association rubric

Inspect only the actual rendered historical receipt and literal retained own
replies/received prose. A host receipt explicitly exposes the genuine archived
v1 integer associated with its ID and versions. A derived excerpt qualifies
only when it contains the exact syntax `xNNN/v1=INTEGER` with ASCII digits and
an integer spelling without leading zeros, naming the edited ID and matching its genuine archived
v1 value. Record the original call/message/delivery IDs, history index, exact
matched excerpt and character span. Keep wrong source-bound assertions separately.
Derived assertions remain untrusted prose, even when they match the raw record.
The integer cannot be a prefix of a decimal, exponent, underscored number or
adjacent numeric arithmetic. Ordinary sentence punctuation can follow it.

Numeric coincidence, other IDs/versions, candidates without association and
other wording do not qualify. No match means **unresolved**, never evidence that
the old value is absent or unreconstructible. This deliberately incomplete
rubric uses no LLM judge, semantic dependency graph or exposure cone. It does
not infer model use or causal dependence from exposure or delivery paths.

## Assumed correctness and actual work

Reconstruction references name the exact view and explicitly assume a correct
old candidate. Use the actual last own candidate only if it remains in the
rendered retained view, as a literal own prefix-round-four reply or historical
compact candidate. C's cleared candidate is unavailable for this annotation,
even though its original value remains in the offline audit. Local Prefix uses
adjacent cumulative coordinates, or a local
coordinate plus every unchanged raw operand up to that coordinate. Complete
Difference uses one held unchanged raw anchor to fix the additive constant.
Local Sort reconstruction is attempted only with all other raw records held;
enumerate the public 0–99 domain, excluding the current replacement, and require
a unique old operand compatible with the assumed correct local segment. Multiple
or zero compatible operands remain unresolved. These conservative sufficient
checks do not exhaust all deductions possible from prose.

Prefix/Difference transport instead applies the genuine raw delta to the actual
valid prefix-round-four candidate, whether correct or wrong. It checks the
residual-error identity and records old and transported exact correctness
offline. Invalid, failed or unexecuted last candidates remain unavailable;
an earlier candidate never fills the gap. No reference is supplied to peers.

The [atlas examples](../../tests/information_examples.py) are small independent
CPU views, including Max only as an illustration. Their ambiguity claims concern
the named views before additional communication. They do not establish natural
LLM error frequency or certify any submitted candidate.

## Inventories, timing and measurements

The complete saved schedule defines all denominators. Keep every prefix peer
in all four rounds and every L/B peer in the four-call receipt display. A first
observed receipt is distinguished from an exact first boundary when earlier
boundaries are unknown. Host injections and generated forwarding retain their
delivery IDs. No receipt, receipt without success, same-call/later success and
unknown cases remain visible; correctness before receipt has positive, negative
and unknown counts. No successful-only lag average is calculated.

C/F initial remote coverage excludes the changed host record from numerator
and denominator. Known tombstones count; pending v2 does not. The unique new
ID/version acquisition count and the count of every validated send attempt are
separate. Committed delivery evidence supplies acquisition flags, including the
final post-round-four boundary (which is not an extra call). Without that final
checkpoint, observed acquisitions are explicitly partial and the full-horizon
count is unknown. A saved initial checkpoint can establish boundary inventory
even before the first call has a rendered request. Acquisition remains an outcome.

Current raw completeness is sufficient for fresh exact recomputation. A Prefix
peer also has a sufficient raw view if it holds every current operand through
the end of its output slice, even with the unrelated tail missing. Other
incomplete views are unresolved by this conservative check, not proven insufficient.
Receipt strata distinguish unknown boundaries from unresolved interpretation
and retain their scheduled peer-call and unique-world denominators, old-candidate
correctness and prefix-round-four joint correctness. Repeats stay separately labeled.

`history_content_tokens` sums the independently tokenized displayed own replies,
received prose, historical candidates and public feedback, excluding layout
headers. It does not measure incremental request cost. Check the matching
tokenizer against every saved full input sequence before counting. With no
matching tokenizer supplied, empty history is zero and nonempty history is
unavailable. Request-token counts come from saved IDs. Scripted M3 tokenization
is not relabeled as native: the separate local metadata harness records native
counts for all five families at both sizes without loading weights.

The SQLite call/attempt/input snapshot and the saved committed checkpoint are
read in one transaction with `mode=ro` and `query_only`. The installed saver's
public serializer decodes its existing committed bytes; no saver setup, private
transaction API, pending-write interpretation, runner or inference is invoked.
No new authoritative export, progress database or mutable provenance store is added.

Sort displacement uses value then stable record ID to break ties for descriptors
only. Record crossed shard-boundary ranks separately from numerically affected
output owners. BFS descriptors retain the deleted endpoints and count new
unreachable nodes. These footprints are descriptive and never admission rules.
