# M2-T06 lessons, blockers, and ranked fixes

**5 October 2026. Option 1 selected, authorized, implemented and CPU-verified.**
The [specification](../../PROJECT_SPECIFICATION.md) remains authoritative.
[M2-T06 completion](../todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records checks and reproduction commands; **M2's CPU gate passes**. GPU
memory, capability and timing remain M5, with separate authorization required.

**Lessons.** The local-view witness succeeds for every family/size/intervention;
correct candidate/control/one-shard outputs have upper bounds of **245 target /
189 fallback** tokens, within 384. Attainability is not LLM capability.
Generated-token cost and retained-input cost differ: invalid replies, escaping,
normalization and re-encoding defeat simple payload sums. Passing a failure
regression is not admission. A complete bound must cover every loaded token,
Unicode boundary and structural field; observed maxima cannot replace it.
The native template also strips outer whitespace: literal blocks need a footer.

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
