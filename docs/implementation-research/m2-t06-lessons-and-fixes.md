# Lessons learned through M2-T06, blockers, and ranked fixes

**5 October 2026. Option 1 selected, authorized, implemented and CPU-verified.**
The [specification](../../PROJECT_SPECIFICATION.md) remains authoritative.
[M2-T06 completion](../todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records checks and reproduction commands; **M2's CPU gate passes**. GPU
memory, capability and timing remain M5, with separate authorization required.

This records lessons from the completed CPU implementation and remedy, including
mistakes encountered during this work. It is supporting evidence, not another
specification. Earlier task counts are historical; current results are linked above.

## Lessons learned

### Scientific boundaries

1. **Keep authority separate from evidence.** The specification defines the
   experiment; plans organize implementation, and probes/fixtures support claims.
   Native SILO execution and scoring cannot replace the study's exact contracts.
   Reinspect current files rather than treating archived status as current behavior.
2. **A lawful witness proves attainability, not model capability.** Computing
   from acquired local records demonstrates that the protocol permits recovery.
   It says nothing about natural LLM accuracy, treatment effects or runtime.
3. **Useful outputs and complete contexts are different gates.** Correct
   candidate/control/one-shard outputs have bounds of 245 target / 189 fallback
   within 384; that did not establish that retained requests fit 8,192.
4. **Do not turn schema validation into answer repair.** Wrong integers can be
   structurally valid. Gold, hidden records, future edits, condition labels and
   mathematical corrections stay outside peer views and public feedback.
5. **Representation changes can change the scientific regime.** A larger input
   cap and revised Unicode boundary required the selected pre-main authorization.
   Readable lossless history preserves treatment information; trimming,
   canonicalizing replies or replacing invalid text with markers would change it.
6. **Choose populations before outcomes.** Reuse saved worlds, edits, schedules
   and stable IDs. A per-call overflow is not repaired by fewer worlds, favorable
   prefixes, dropped families, early stopping or missing failed slots.

### Representation and tokenizer behavior

7. **Physical output cost is not retained-input cost.** Decode, JSON escaping,
   Unicode normalization and whole-request re-encoding can expand an output.
   Neither saved output length nor a sum of separately encoded fragments bounds
   the final request without an argument about the actual tokenizer.
8. **Invalid replies are part of retained work.** They may use the entire output
   allowance and have pathological text. A bound based only on valid or correct
   JSON misses the reachable newline counterexample documented below.
9. **Keep raw payloads outside structural escaping.** Length-delimited literal
   blocks avoid multiplying control characters through ASCII JSON. Column labels
   reduce repeated metadata while retaining every delivery/history field.
   Preserve wrong values, formatting and history order.
10. **Use lengths to audit untrusted block boundaries.** Quotes, controls, fake
    headers and special-looking strings must survive without confusing the host
    decoder. A textual delimiter search inside payloads is insufficient.
11. **Inspect the real template, including whitespace handling.** Its outer
    `.strip()` removed trailing archived whitespace in an initial layout. A fixed
    footer keeps that whitespace inside the message; dedicated checks preserve it.
12. **Lossless rendering and native normalization are distinct.** The host keeps
    exact rendered strings; native NFC may change their tokenized spelling.
    Retain and compare both rendered/template text and actual IDs. Newline block
    boundaries isolate normalization; character lengths describe original text.
13. **A Python string is not necessarily tokenizable scalar text.** An unpaired
    surrogate escaped in valid JSON originally reached native counting and raised
    `TypeError`. Reject it as a whole-reply schema failure before effects, with
    raw reply/IDs and bounded feedback intact. Valid escaped pairs remain accepted;
    replacement or normalization would silently repair the sender's message.
14. **Audit the loaded tokenizer, not just `tokenizer.json`.** AutoTokenizer
    adds seven tokens from configuration. The full loaded vocabulary has 248,077
    entries; auditing only the model vocabulary or metadata list omits behavior.
15. **Output vocabulary and assigned tokenizer IDs differ.** All 243 unassigned
    output IDs were checked to decode empty. Empty decoded text adds no retained
    payload, but its physical generated IDs still count and remain archived.
16. **Do not strip special-looking content to make a reply valid.** Native
    markers can change parsing/template behavior. Preserve literal outcomes and
    test them; M5 must separately audit actual terminal transport framing.
17. **Use ByteLevel's byte alphabet.** Vocabulary glyphs' UTF-8 lengths are not
    decoded payload lengths. Split/invalid UTF-8 fragments can join across tokens;
    pay the audited allowance per incomplete byte, not one replacement per fragment.

### Complete capacity

18. **A counterexample proves failure; a maximum observation does not prove fit.**
    The current adversarial maximum is 33,106 input tokens. Admission comes from
    the complete bound, not that measurement or the ordinary witness's range.
19. **A very loose bound is not a useful context choice.** The initial roughly
    37.8-million upper bound was conservative but could not justify a feasible cap.
    Tighten the actual representation/tokenizer argument before changing limits.
20. **Prove only the merge properties used.** Some multilingual merges reference
    later productions; a globally monotone-rank assumption was unjustified.
    The proof instead audits homogeneous ASCII merge dependencies, doubling
    ladders and boundary allowances. It never assumes general BPE additivity.
21. **Normalization needs complete Unicode coverage.** Exhaustive native scalar
    audits cover decomposition/byte expansion. Already-counted prose has a
    different allowance from physical own replies: 45 versus 48 input tokens
    per counted/generated token, respectively.
22. **Include every field and the complete horizon.** Pay seven own replies,
    21 received texts, maximal fixed feedback, labels/lengths, all current sources,
    pending/deleted states, notices/receipts, delivery rows and the native wrapper.
    Large wrong integers do not acquire an invented numeric cap.
23. **Avoid double counting mutually exclusive policy states.** K's one retained
    prefix candidate plus three recovery replies fits inside the seven-own-reply
    envelope; it is not an extra candidate on top of a full B history. Q releases
    each held text once. Overcounting these made the original bound unnecessarily loose.
24. **Reserve all output before admitting an input.** The complete target upper
    is 261,388 including 384 output tokens, within 262,144; fallback is 259,868.
    The renderer still rejects oversize requests without truncation.
25. **Fallbacks solve particular constraints.** The smaller mathematical size
    also failed the original cap; 4B has identical pinned tokenizer/template
    metadata. Neither automatically fixes re-encoding or Unicode failures.

### State, delivery and replay

26. **Source authority and derived history must remain distinct.** Invalidation
    changes usable source versions; it does not remove old model-generated prose.
    A pending replacement reveals no hidden payload, and a known BFS tombstone
    identifies a deleted edge without restoring it.
27. **Synchrony is a visibility rule.** Render immutable start-of-round views,
    validate whole replies, then commit next-round deliveries. Physical invocation
    order must not expose current-round replies or change committed results.
28. **Retention is literal, and siblings start independently.** Reconstruct each
    sibling from its drained original prefix; apply its event/retention once.
    Keep K's actual fourth-round candidate or absence, including wrong answers,
    without backfilling an earlier valid candidate or continuing to compact later work.
29. **Exact reuse requires more than a seed.** Check scheduled scope, permitted
    views, rendered/template/native input, settings, seed and recorded outcome.
    Reuse invalid parents too. Rebuild deliveries in the receiving branch rather
    than copying a parent's post-delivery state.
30. **Delayed prose does not delay source delivery.** Q keeps round-two sources,
    own replies and source metadata equal to its parent while holding only prose.
    Release stable text IDs once at the prescribed boundary, in chronological order.
31. **Fixture identities need the same discipline as execution.** An earlier
    inactive replay fixture reused IDs across different responses. Distinct saved
    worlds and archive-wide unique-call/exact-parent joins fixed that defect.
    Empty/inactive Q cases remain in evidence with zero held prose.
32. **Failed, invalid and unexecuted slots are different.** Recorded failures and
    invalid replies have absent candidates; unexecuted slots remain unknown.
    No successful older candidate fills them. Persist-before-effects and crash-safe
    resumption remain requirements to verify in the actual M3 runner.

### Verification and implementation workflow

33. **Test the failure mechanism, not only successful examples.** Native checks
    cover controls, combining text, surrogate pairs/lone escapes, trailing
    whitespace, split bytes, special tokens, large mistakes and invalid replay.
    Keep a reachable round-two overflow distinct from a constructed full-horizon envelope.
34. **A passing regression can still mean a blocked gate.** Original capacity
    checks correctly reproduced overflow, then returned 1. Current admission
    returns 0; failed verification returns 2. State both checks and admission.
35. **Regenerate affected evidence after representation changes.** Renew all
    renderer, protocol, round, event, replay, witness and capacity archives; then
    reproduce them read-only in a fresh process. Set `PYTHONHASHSEED` before that
    process starts, and independently check the other checkpoint's metadata.
36. **Test the installed package independently of the source import.** An
    installed-suite failure exposed a test's checkout-relative default config
    assumption. Passing the source config explicitly fixed the test; production
    CLI behavior was not changed. Import the installed library before adding tests.
37. **Keep dependency assumptions visible.** `--no-build-isolation` failed in the
    older environment because wheel-building support was absent. Normal build
    isolation installed the package successfully without runtime dependency changes.
    Record actual package versions rather than treating a prior environment as frozen.
38. **Avoid accidental work inside exhaustive loops.** Repeated `get_vocab()`
    calls copied the full vocabulary during its own audit. Cache the loaded map
    once. This was a verification-helper performance bug, not a protocol defect.
39. **Preserve negative evidence and scope old claims.** The original report is
    retained byte for byte. Offline canonical gzip reduces fixture storage only,
    never peer history. Dated old commands/counts describe their original version;
    current status links renewed evidence.
40. **Keep sources of truth small and progress consistent.** Reuse existing
    IDs, barriers, queues and records; add no generic framework or second tracker.
    Update task status, prerequisite renewal notes, index, plan and next ready task
    together. Check links/anchors/counts and make meaningful checkpoint commits.
41. **Verify proportionally and report only executed checks.** Source and installed
    suites each passed 167 checks, core-only 81, native checks 37 plus independent
    4B capacity reproduction. Compilation, package consistency, artifact fidelity,
    document links and task totals were also checked. Documentation-only follow-up
    needs consistency checks rather than repeating inference or full behavioral suites.
42. **Make Windows text encoding explicit.** Unicode passed through shell/stdin
    paths became question marks in two documentation ranges. Read/write UTF-8,
    check the resulting file, and preserve canonical fixture bytes rather than
    trusting console appearance.
43. **Distinguish tool failures from test failures.** Shell handling of native
    stderr can obscure a successful unittest result. Capture logs and inspect the
    Python exit/result. A failed patch with partial-line context requires reading
    the exact current line, not repeatedly guessing its text.
44. **Inspect archive shape before extracting statistics.** Some `cases` fields
    are dictionaries and others lists; token counts may require lengths of saved
    IDs. Printing a whole case map accidentally floods output with replies/IDs.
    Read field shapes and report only the requested summaries.

### Remaining limits

45. **Native context support is not device admission.** Static FP16 full-attention
    KV alone is 8 GiB at the cap. Weights, linear-attention state, activations,
    logits/workspace and 1.5 GiB headroom are additional. A tight CPU bound does
    not establish that a T4 configuration is usable.
46. **Capability, timing and allocation still need measurement.** M5 must validate
    the accepted backend at the complete input envelope and forecast the full
    schedule. Neither a successful witness nor smaller typical prompts settles this.
47. **A gate pass does not authorize the next expensive action.** M2's CPU gate
    makes M3-T01 ready; M3–M4 still precede GPU work. No model inference, GPU run,
    pilot, accepted freeze, main result or empirical recovery claim was produced.

## Original blockers and ranked fixes

**Exact original blockers.** The pinned Qwen3.5-9B/4B tokenizer/template artifacts
are byte-identical. The [preserved 8,192 archive](../../tests/fixtures/capacity_report_8192_original.json.gz)
records the following failures before the authorized revision:

- **Reachable overflow:** token `76374` decodes to 32 newlines. A retained
  invalid 384-token reply, nine-token feedback and three legal 128-token texts
  caused overflow on the next call.
  Prefix round two requires **14,258 + 384 = 14,642 target** and
  **13,965 + 384 = 14,349 fallback** tokens, against 8,192.
- **Re-encoding expansion:** token `224227` repeated 384 times re-encodes to
  2,304 tokens. Seven own replies alone cost **177,491 ASCII-JSON / 16,211
  UTF-8-JSON / 16,212 labeled-raw-text** tokens. These constructed probes refute
  those layouts, not every lossless encoding. A full-horizon fixture uses
  **92,828 input + 384 reserve** with the unchanged renderer. Observed maxima
  and the loose ~37.8-million upper bound cannot determine a suitable new cap.
- **Undefined Unicode outcome:** a 38-token JSON reply containing `"\ud800"`
  as message text passed string-schema validation; native prose counting raised
  `TypeError` instead of a bounded slot outcome. A larger context cannot fix it.

**Unicode fix required alongside every capacity option.** The authorized
clarification requires Unicode scalar message text: accept valid surrogate pairs and reject
unpaired surrogates as whole protocol-invalid replies before effects. Preserve
raw replies/IDs, candidate absence and fixed bounded feedback; never replace or
normalize text to repair it. This is an explicit pre-main protocol decision. Rerun
strict/native validation for lone/pair escapes, controls, combining characters
and special-looking strings, synchronous no-effects, and invalid-outcome replay.

**Ranking.** Prioritize preserving treatment information, then simplicity/risk.
The selected option now has a complete bound and passing adversarial checks;
its resource admission remains conditional.

| Rank / option | Scientific soundness | Simplicity | Implementation risk | Design impact |
|---|---|---|---|---|
| 1. Lossless layout + larger uniform context | High: retains all work | High | Low code; high resource uncertainty | Changes input-budget regime |
| 2. Exact literal token-fragment assembly | High if fidelity is proved | Low | High: template/token boundaries | Changes input representation |
| 3. Uniform budgets on rendered reply/prose cost | Defensible new regime | Moderate to low | High: enforcement before emission | Changes caps/generation distribution |
| 4. Canonical valid history + invalid-slot markers | Defensible revised question | High | Low to moderate | Changes the retained-history treatment |

1. **Selected, subject to resources.** Preserve every payload/label in a
   readable lossless layout; raise 8,192 uniformly only with a tight bound.
   Keep output budgets, interventions and populations. This minimizes information
   loss and code complexity, but revises the bounded-computation regime.
   **Rerun:** all M2 rendering/retention/replay/witness/capacity evidence; later M5
   worst-prompt memory, capability, timing and complete-schedule forecast.
   **Reject** if checkpoint support, T4 headroom or allocation cannot cover the
   proven requirement. Neither 16K nor 32K is automatically sufficient.

2. **Reserve for a small, faithful implementation.** Assemble labeled fragments
   using saved own generated IDs and separately encoded prose, avoiding whole-text
   re-encoding; never reuse hidden model state. `7×384 + 21×128 = 5,376` excludes
   all framing, feedback, tables, K state and control-token safeguards.
   **Rerun:** decoded-text/template fidelity, special-token isolation, all M2
   checks, exact mixed/Q inputs and complete bounds; M3 persisted reconstruction
   and M5 actual inference. **Reject** if this needs opaque encoding, extensive
   machinery or cannot preserve the single labeled user-message boundary.
   Tokenized representation semantics require explicit review.

3. **Authorize only as a new generation regime.** Limit the cost of raw replies
   in their actual retained representation *before* an oversized token is emitted,
   including invalid fragments; also bound serialized message cost. Derive uniform
   budgets from useful-output floors and the complete bound. Preserve emitted
   bytes/wrong values; rejection after generation cannot bound retained raw text.
   **Rerun:** candidate/control/witness floors, stopping/masking/termination,
   strict failures, retention, mixed/Q replay, capacity and M5 capability/cost.
   Prefer this over discarding work when literal retention is essential; **reject**
   if enforcement is complex or useful replies cannot fit. Sampling changes must
   be explicit.

4. **Least preferred: explicitly narrow the retained-history question.** Keep
   canonical valid candidate/send content, verbatim prose and wrong integers;
   replace invalid own text with labeled markers/feedback. Keep the full raw
   audit. Simpler code discards potentially useful invalid work and formatting,
   changing B/mixed/Q history and the interpretation of C−B and B−K.
   **Rerun:** revised boundaries, K absence, all M2 checks and complete bounds
   including valid Unicode/large wrong integers; revise claims and renew M5.
   **Reject** without that scientific revision or if valid histories still exceed
   capacity. Removing one counterexample is insufficient; summaries/repairs are
   not substitutes.

**Reject standalone shortcuts:** fallback size already fails; 4B has the same
tokenizer; fewer worlds cannot repair a per-call overflow. Lower token caps need
renewed expansion bounds/witnesses. Silent trimming, dropped families/failed slots
and selection of short/valid prefixes change treatments or populations.

**Implemented selection:** the user chose option 1 and authorized implementation
on 5 October 2026, superseding the earlier documentation-only restriction.
Column-labeled metadata and length-delimited literal blocks preserve all work;
the footer retains trailing whitespace. Raw rendered text and native NFC IDs
remain separate replay inputs. Scalar-message failures preserve raw replies/IDs
and have no effects. The [complete proof](m2-t06-capacity-proof.md) covers all
248,077 loaded tokens, including seven configuration-added tokens, and all
Unicode scalars. The full horizon is bounded by **261,388 including output**
inside a uniform **262,144**, with both sizes admitted. All affected archives
were renewed: **167 source/installed-library, 81 core-only and 37 native checks**
pass, with independent 4B reproduction. Original failure evidence remains intact.
Static full-attention FP16 KV alone is 8 GiB at this cap; resource feasibility
is untested. M5 must admit the complete regime under [AGENTS.md](../../AGENTS.md);
these CPU results authorize no GPU run, pilot, freeze or main execution.
