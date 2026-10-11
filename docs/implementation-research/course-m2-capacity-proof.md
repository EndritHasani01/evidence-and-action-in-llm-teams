# Course M2 complete native-token capacity argument

11 October 2026. Authority is [specification Section 11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime).
This renews the [original proof](m2-t06-capacity-proof.md) for the actual course
renderer, pinned 4B metadata, numeric m=6, eight-node/twelve-edge BFS and 256/64
caps. It proves legal CPU token capacity, not GPU memory, model competence,
runtime throughput, a freeze or execution authorization.

## Native payload argument

The existing [exhaustive audit](../../tests/capacity_bound.py) is rerun against
the loaded Tokenizers 0.22.2 backend and pinned tokenizer/configuration/template
bytes. It checks deterministic NFC ByteLevel BPE, its exact regex and all 256
unmerged byte symbols; dropout/unknown-token/boundary-changing added-token
behavior is rejected. All 248,077 loaded entries, including seven
configuration-added special tokens, are covered. The 243 unassigned output IDs
decode empty; they still consume physical output tokens.

The proof uses decoded byte payloads rather than vocabulary glyph UTF-8 sizes.
The largest payload is 128 bytes per vocabulary token. Homogeneous ASCII runs
use audited, uniquely produced doubling ladders with increasing dependency
ranks. Pay the two boundary fragments at every level, regex edge characters
and a final starter protected against composition. For already-NFC prose,
each em dash has a separating third byte after the audited `E2 80` merge pair;
an overlapping merge pays at least the same savings. These allowances cover
token boundaries and do not assume additive canonical re-encoding.
The native [ranked merge implementation](https://github.com/huggingface/tokenizers/blob/v0.22.2/tokenizers/src/models/bpe/word.rs)
and native run-edge/composition tests support this reused argument.

Exhaustive native NFD/NFC over all Unicode scalars verifies at most four NFD
scalars and at most three NFD bytes per original byte. Complete scalars pay
their NFD byte cost; each partial or invalid UTF-8 byte pays three. This covers
scalars assembled across generated-token boundaries and lossy decoder
replacement characters. The maximum allowance for an own reply is **48 input
tokens per physical generated token**. Prose is counted after JSON decoding and
native NFC. Reconstructing that counted normalized byte stream gives **45 input
tokens per counted prose token**, including the audited run/dash savings.

No host normalization, parsing, shortening or repair enters retained text.
Structural JSON stays ASCII; each raw reply and decoded prose occupies one
length-delimited literal block between newlines. NFC cannot compose across those
boundaries. The native template's `.strip()` cannot remove archived whitespace
because the fixed footer follows it. Exact rendered text and native token IDs
remain separately archived and checked for replay. Quotes, control characters,
fake block headers, template markers and trailing whitespace remain literal.
Unpaired decoded message surrogates remain whole-reply schema failures; exact
raw JSON escapes remain in own history. Non-native synthetic surrogate strings
use the renderer's JSON-string fallback and are outside native-generation
capacity, as in the original proof.

## Complete horizon and structure

Before recovery round four, a retained peer can have seven own replies and
21 received prose entries. Each of three senders can direct its entire 64-token
prose allowance to that recipient in each preceding slot. Q holds/releases each
entry once; changed release order cannot increase the structural row count.
Prefix calls and resets/F have shorter histories. K uses one prefix-round-four
candidate or absence plus three recovery replies and nine prose entries. Its
candidate integer bytes cannot exceed its original valid reply allowance:
canonical serialization removes JSON whitespace/escapes without adding integer
digits. Charge that payload against one of the seven own allowances, never in
addition to all seven B replies. Current candidates already in own history are
referenced once, without another payload copy. Controls have a single
full-information request and no retained history or communication.

The shared complete payload allowance is:

`7*256*48 + 21*64*45 = 86,016 + 60,480 = 146,496 input tokens`.

[Course accounting](../../tests/tokenizer_course_capacity.py) calls the existing
[structural envelope](../../tests/tokenizer_capacity.py) with explicit course
limits. It overbounds the complete public manifest/coordinates, all current
records at widest legal numeric values/endpoints, known/deleted/pending states,
revision or sham notice and ordinary/disclosed receipt, seven largest fixed
feedback slots, and one first-acquisition row per held record. Stable IDs have
their existing fixed width; owners, versions v1/v2 and round numbers have one
digit. Numeric positions/ranks reach 23, and BFS nodes reach 7. Peer 3's
Prefix/Sort assignments have the widest position labels. Revision notices are
longer than shams; ordinary receipt wording overpays the in-range before-value.
Full known numeric rows are longer than pending rows even for one-digit Prefix
values; deleted-edge rows dominate pending BFS rows.

Metadata is measured with empty literal payloads and both valid/invalid latest
slots. The envelope pays both possible compact-candidate metadata placements,
despite storing the historical payload only once; it also pays each text label's
five-digit maximum original character count. Own text has at most `256*128`
characters and original non-NFC prose at most `64*128*4`, both 32,768. Null
senders and event-origin metadata are overpaid independently in each current
delivery row. Recovery labels dominate prefix labels; the actual native wrapper
is 69 ASCII bytes. Every structural byte conservatively costs one token. The
full-information layout is checked separately under the same family envelope.

| Family | Structural bytes | Wrapper | Payload | Output reserve | Complete upper bound |
|---|---:|---:|---:|---:|---:|
| Top-K | 9,301 | 69 | 146,496 | 256 | 156,122 |
| Prefix Sum | 9,393 | 69 | 146,496 | 256 | 156,214 |
| Difference Array | 9,430 | 69 | 146,496 | 256 | **156,251** |
| Distributed Sort | 9,425 | 69 | 146,496 | 256 | 156,246 |
| BFS Distance | 7,014 | 69 | 146,496 | 256 | 153,835 |

Thus every permitted course request has at most **155,995 input tokens**, plus
the complete 256 output reserve, within the unchanged 262,144 native window.
The proposal's conditional 157,772 used the larger thesis structural allowance;
it is replaced by this independently renewed course bound.

## Evidence and resource boundary

The [course report](../../tests/fixtures/course_capacity.json.gz) retains the
exhaustive audit, complete family accounting, adversarial native requests and
physical output IDs. Fixtures exercise maximal newline/invalid own text,
Cyrillic/Thai re-encoding, split scalars, invalid UTF-8 bytes, special tokens,
quotes/controls/fake headers, maximal ASCII/dash prose, non-NFC prose and large
valid wrong integers. A real synchronous slot combines a 256-token invalid own
reply with three valid 64-token incoming texts and bounded feedback. Fixtures
challenge the argument; their measured maxima do not establish the bound.
The independently loaded pinned 9B metadata reproduces the course report because
the tokenizer/template and relevant native geometry match; this selects no
9B course model. Original positive/negative thesis archives remain unchanged.

The [local native witness](../../tests/fixtures/course_attainability.json.gz)
checks every saved course world and logical opportunity, locally acquired
sources, controls, correction, F reacquisition, masks, genuine receipts and
exact mixed/Q parents. Correct-width candidates and useful one-shard sends have
a universal 189-token serialization bound within 256, with actual prose under
64. The strategy uses no arbitrary padding or unseen solver inputs and proves
attainability independently of model competence.

Both pinned configurations have eight full-attention layers, four KV heads and
head dimension 256. FP16 full-attention KV alone costs 32,768 bytes per resident
token: `156251*32768 = 5,120,032,768` bytes, about 4.768 GiB.
Weights, recurrent state, activations, logits, workspace, actual causal/mask/cache
semantics and at least 1.5 GiB free headroom remain additional M5 obligations.
This lower bound is not a peak-memory measurement or T4 acceptance.
