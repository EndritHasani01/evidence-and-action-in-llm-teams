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
only when it contains the exact syntax `xNNN/v1=INTEGER` with an integer spelling
without leading zeros, naming the edited ID and matching its genuine archived
v1 value. Record the original call/message/delivery IDs, history index, exact
matched excerpt and character span. Keep wrong source-bound assertions separately.
Derived assertions remain untrusted prose, even when they match the raw record.

Numeric coincidence, other IDs/versions, candidates without association and
other wording do not qualify. No match means **unresolved**, never evidence that
the old value is absent or unreconstructible. This deliberately incomplete
rubric uses no LLM judge, semantic dependency graph or exposure cone. It does
not infer model use or causal dependence from exposure or delivery paths.

## Assumed correctness and actual work

Reconstruction references name the exact view and explicitly assume a correct
old candidate. Local Prefix uses adjacent cumulative coordinates, or a local
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
