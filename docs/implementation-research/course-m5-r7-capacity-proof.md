# Course R7 supplemental literal-input proof

11 October 2026. This tightens the already verified
[course capacity argument](../validation/course-m2-attainability-and-capacity.md)
without changing rendered text, normalization, protocol limits, retention,
model revision or outcomes. The original 156,251-token bound and archive remain
valid. The [original proof](m2-t06-capacity-proof.md) supplies structural coverage,
partial UTF-8 treatment, homogeneous ASCII ladders and the seven-own/21-prose
horizon. This supplement supplies a smaller payload allowance only. It does
not admit weights, model execution or complete-envelope GPU memory.

## Native byte-pair certificate

The pinned Tokenizers 0.22.2 deterministic BPE starts with individual byte
symbols and repeatedly merges adjacent symbols. An initially eligible pair
cannot finish as two adjacent singleton bytes: it merges, or another merge
first touches one of its endpoints. Select pairs with at least one unselected
byte between them. Their first-touch merges are distinct: two untouched
endpoints from different selected pairs are not adjacent. Consequently each
selected pair pays at least one token of saving, regardless of merge order,
later dependency ranks or neighboring vocabulary-token boundaries. This is a
merge-count argument, not an assumption that canonical re-encoding is additive.
See the pinned [native BPE source](https://github.com/huggingface/tokenizers/blob/v0.22.2/tokenizers/src/models/bpe/word.rs).

For every complete three/four-byte non-Hangul scalar whose first two bytes
have a native one-byte/one-byte merge, charge its byte length minus one.
Each selected prefix has a separating third byte, including between adjacent
scalars; the scalar-aware regex cannot cut inside it. Other scalars pay all
their bytes. The loaded merge table has 4,203 one-byte pairs.

Within ASCII letter runs and homogeneous ASCII runs of at least eight
characters, select eligible byte pairs at least three positions apart.
Protect the first three characters from native apostrophe contractions/regex
edges and the last two from edge handling and possible NFC composition of
the final ASCII starter. The pinned regex isolates digits individually; the
audit therefore requires that no digit/digit byte merge exists. Other
homogeneous runs have no interior regex cut. Independently verified native
boundary challenges cover all 128 ASCII values, six lengths and four contexts.

For each ASCII region use the larger saving of this certificate and the old
homogeneous-run certificate; do not add both. Regions are disjoint. Protected
ends separate their savings from neighboring scalar-prefix savings. Loaded
special tokens are ASCII, have no strip behavior and no homogeneous run;
their recognized single-token representation saves at least the certificates
inside their spelling. Their delimiter boundaries do not cut an outside
protected certificate. The existing metadata audit covers the exact loaded
added tokens, not just the tokenizer JSON entries.

## Normalization and physical token boundaries

Own replies are literal native decodes, including invalid JSON and markers.
For the proof only, canonically decompose complete scalars except already
complete Hangul syllables. No request text is transformed by this code.
Canonical reordering preserves the scalar-cost sum; it cannot insert a mark
between consecutive ASCII starters. The protected final ASCII starter pays
composition at a region's end. For every Unicode scalar, the native NFC cost
is at most its native decomposition cost. This is checked exhaustively over
all 1,112,064 non-surrogate scalars using the same native normalizer.

A complete Hangul syllable can remain one three-byte atom in the proof:
its internal L/V[/T] constituents all have canonical combining class zero,
so later marks cannot reorder inside it. LV followed immediately by T can
compose to another single three-byte syllable, reducing cost. Jamo L+V[/T]
composition is also covered by the exhaustive decomposition-cost comparison.
An intervening mark blocks that composition. These facts follow the
[Unicode canonical normalization algorithm](https://www.unicode.org/reports/tr15/tr15-58.html),
and the native checks verify canonical equivalence of every proof decomposition.

Keep the original three-byte allowance for *each* partial/invalid UTF-8 byte.
It covers scalars assembled across physical token boundaries and lossy decode
replacement; no partial byte receives a pair saving. NFC only reduces the
resulting charged potential. Received prose already has an NFC native token
count; charge its counted token bytes with the same separated-pair argument.
The old original-spelling length-label bounds still overpay structure.

## Complete course bound

[course_capacity_tightening.py](../../tests/course_capacity_tightening.py)
checks the pinned metadata, all 248,077 loaded entries and all Unicode scalars.
The existing 243 unassigned output IDs decode empty and add no text, while
their physical output cost remains counted. Both payload factors become
**32**, versus the old own/prose 48/45. The maxima include token 58180
(16 em dashes) and token 85748 (two 20-space/newline groups). Native challenges
also repeat the largest entries through 256 physical slots and cover partial
scalar, Hangul, composing/reordered mark and framing boundaries.

The unchanged horizon therefore pays
`7*256*32 + 21*64*32 = 100,352` payload input tokens. Reuse the five original
family structural/wrapper allowances; no truth or future-edit data is added.

| Family | Structure + wrapper | Complete input | With 256 output reserve |
|---|---:|---:|---:|
| Top-K | 9,370 | 109,722 | 109,978 |
| Prefix | 9,462 | 109,814 | 110,070 |
| Difference | 9,499 | 109,851 | **110,107** |
| Sort | 9,494 | 109,846 | 110,102 |
| BFS | 7,083 | 107,435 | 107,691 |

The uniform runtime cap remains 262,144. This bound does not assert legal
attainability of its maximum. Existing rendered adversaries retain their exact
native counts and literal text and lie below it. Reproduction commands, failed
and corrected receipts, independent challenges and memory limits are in the
[offline R7 review](../validation/course-m5-r7-offline-review.md).
