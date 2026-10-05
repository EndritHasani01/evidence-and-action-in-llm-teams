# M2-T06 literal-layout capacity argument

5 October 2026. This proves CPU token capacity for the selected pre-main
representation and uniform **262,144** limit. It does not prove T4 memory,
throughput or model capability. The [specification](../../PROJECT_SPECIFICATION.md)
governs the revised regime; the [original negative archive](../../tests/fixtures/capacity_report_8192_original.json.gz)
preserves the rejected 8,192-token regime.

## Representation and scope

The [renderer](../../recovery/prompts.py) accepts only a permitted `PeerView`.
It puts public metadata, current sources, notices/receipts, fixed feedback and
column-labeled delivery/history rows in structural ASCII JSON. Each own reply
and received prose follows once in an indexed literal block. Recorded character
lengths decode the pre-tokenization request even if text contains fake headers,
controls, quotes, template markers or trailing whitespace. The fixed footer
prevents the native template's outer `.strip()` from removing archived whitespace.
K's actual historical candidate/absence remains explicit. No payload is parsed,
summarized, normalized or repaired by the host; current sources appear once.

Blocks have newline boundaries. NFC therefore cannot combine a block with its
framing or another block. The native tokenizer's existing normalization may
change Unicode spelling in the tokenized representation; exact rendered text
and actual native IDs remain separate, both checked for replay. Character lengths
describe rendered text before native normalization. The lossless decoder audits
that text, not a reconstructed normalized token stream. Native decoded outputs
are scalar strings; non-native audit strings with unpaired surrogates have an
explicit JSON-string fallback. They are outside the native-generation bound.
Unpaired *decoded message* surrogates are whole-reply schema failures.

## Complete payload bound

[capacity_bound.py](../../tests/capacity_bound.py) audits every model vocabulary
entry and loaded added token against the pinned artifacts, not sampled successful replies
or an assumed inequality about concatenated BPE encodings. ByteLevel's actual
256-byte alphabet is inverted; glyph UTF-8 size is not payload byte size. With
all byte symbols available, final BPE encoding never needs more tokens than its
initial bytes. Deterministic merges only reduce that count.
The loaded vocabulary includes seven special tokens supplied by tokenizer
configuration as well as `tokenizer.json`. All 248,077 entries are covered.
The 243 unassigned IDs below the checkpoint's output vocabulary size are checked
to decode empty: they add no text, while their physical output cost remains charged.

The largest byte payload is 128, mostly repeated spaces/punctuation. Two audited
facts tighten that otherwise excessive bound:

1. For a homogeneous ASCII run, the native merge table has increasing-rank
   doubling ladders up to lengths 8–128. Every homogeneous production has a
   unique result and its dependencies precede it. At each doubling stage, the
   equal-size interior symbols pair; unequal fragments and mixed context can
   affect only the two ends. Thus a length `n` run with ladder endpoint `q` costs
   at most `ceil(n/q) + 2*log2(q) + 4`: two fragments per level and two characters
   peeled by the pinned regex at word/whitespace boundaries. A regex cannot cut
   the run internally; it can peel an edge character (contraction/punctuation
   prefix/trailing whitespace). Added tokens cannot split these runs. Reserve
   the final ASCII starter against canonical composition, giving the audited
   bound `min(n, ceil((n-1)/q) + 2*log2(q) + 5)`. This bound is subadditive over
   pieces of a run, so vocabulary-token boundaries cannot invalidate it.
2. For already-normalized prose, each em dash's UTF-8 prefix `E2 80` has a native
   merge. These selected pairs have a separating third byte. A final pair cannot
   remain two adjacent singleton bytes in its Unicode pre-tokenizer piece. It
   either merges or an overlapping token protects an endpoint. A length `k`
   merged token can protect at most `k-1` selected pairs; summing its merge
   savings pays one saved token per dash. This reduces the sole 48-byte prose
   maximum (16 dashes) without assuming re-encoding is additive.

For **own replies**, pay native NFD bytes for complete scalars and three bytes
for *each* invalid/partial UTF-8 byte. Exhaustive native normalization over every
Unicode scalar verifies at most four NFD scalars, at most three NFD bytes per
input byte, and nonincreasing byte cost of canonical composition. This covers
characters assembled across physical vocabulary-token boundaries and lossy
decoder replacements. Reordering cannot insert a combining mark inside an ASCII
starter run; its protected end pays any composition. The vocabulary-wide maximum
weighted allowance is **48 input tokens per physical generated token**.

For **received prose**, the public cap already counts native NFC tokenization of
literal text. Reconstruct its normalized byte stream from those counted tokens;
the newline boundaries ensure the same normalization during input tokenization.
Pay complete scalar bytes, three per partial byte and the two merge savings above.
The vocabulary-wide maximum is **45 input tokens per counted prose token**.
Original non-NFC spellings have at most four times the normalized scalar count;
that matters for length-label widths, not tokenized payload cost.

## Horizon and structural envelope

Before recovery round four, B/L/mixed retained peers can have seven own replies
and at most 21 received texts. Every sender can direct all 128 prose tokens to
one recipient. Q holds/releases each text once. Resets/F have shorter horizons.
K has one prefix candidate plus three recovery replies and at most nine received
texts, within those same allowances; its integer payload cannot exceed the
original reply's byte allowance. A current candidate already in an own reply is
referenced, never duplicated. Controls have one full-information call.

The common payload ceiling is therefore:

`7*384*48 + 21*128*45 = 249,984 input tokens`.

[tokenizer_capacity.py](../../tests/tokenizer_capacity.py) separately overbounds
all structural bytes: complete manifest/table, widest legal values/endpoints,
v2/deletion/pending states, public assignments, maximal fixed feedback in seven
slots, widest notice/receipt, one first-acquisition row per record, history labels
and footer, both compact-candidate metadata placements, five-digit original text
lengths, and actual native wrapper. It overpays null senders/event origins and
compact zero values. Prefix/continuation labels and all peers are covered; hidden
truth, queues and resolved forwarding payloads never enter the representation.
The largest structural allowance is **10,951 + 69 wrapper bytes** (target
Difference). One token per byte is conservative for this ASCII structure.

`249,984 + 10,951 + 69 + 384 = 261,388 <= 262,144`.

The [renewed archive](../../tests/fixtures/capacity_report.json.gz) records all ten
family/size bounds, vocabulary/Unicode audits and adversarial native measurements.
Fixtures test the argument; observed maxima do not establish it. Both requested
sizes are CPU-admitted. The checkpoint window is the uniform cap, without YaRN.
The earlier output/witness limits are unchanged and all affected evidence must
be renewed under this renderer.

## Resource boundary

Both pinned text configurations declare 262,144 native positions and eight full
attention layers with four KV heads of dimension 256. FP16 full-attention KV
alone at the cap needs `262144*8*4*256*2*2 = 8 GiB`. Weights, linear-attention
state, activations, logits, workspace and the specified 1.5 GiB headroom are
additional; this is a lower bound, not a peak-memory estimate or T4 admission.
M5 must measure the accepted backend at the complete input envelope, capability,
timing and allocation forecast. No GPU execution, accepted freeze or main run
is authorized by this proof.

Native behavior reference: the audited Tokenizers 0.22.2
[BPE merge implementation](https://github.com/huggingface/tokenizers/blob/v0.22.2/tokenizers/src/models/bpe/word.rs).
