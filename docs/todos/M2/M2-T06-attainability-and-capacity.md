# M2-T06 — Protocol attainability and complete tokenizer capacity

**Status:** done

**Dependencies:** [M2-T05](../M2/M2-T05-mixed-and-prose-delay-replay.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2 acceptance](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§8.2](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [tokenizer probe and its limits](../../implementation-research/inference-and-capacity.md#tokenizer-only-capacity-probe) and [remaining gates](../../implementation-research/SYNTHESIS.md#small-remaining-validation-gates).

## Intended outcome

A locally informed scripted strategy proves the real protocol is usable within four recovery rounds, and the complete renderer has a defensible worst-context bound before GPU use.

## Scope and boundaries

- Each scripted peer forwards its own currently held shard to a different peer in the first three rounds, uses legal placeholder candidates earlier, and computes only from acquired local evidence when sufficient. The solver never sees host gold or unseen records.
- Exercise all five families, both size contracts, local/broadcast revision, sham/preserving siblings, resets, receipts, mixed replay and Q through the real schemas and renderer. Include L replacement forwarding and F reacquisition.
- Tokenize actual serialized team/control candidates and useful one-shard messages. The simultaneous maximum prose/reference payload need not fit, but the witness and required output contracts must fit 384 generated tokens.
- Bound actual retained requests over the complete prefix/recovery horizon, reserving all 384 output tokens inside the authorized 262,144-token limit (revised from 8,192 on 5 October 2026). Include invalid own replies, maximum received prose, feedback, labels, tables, notices/receipts, source-delivery metadata, escaping, large wrong integers and special-looking strings.
- Use both an accounting argument and adversarial rendered fixtures. Q release cannot duplicate retained history. The research's illustrative context and correct-output examples are not a worst-case proof.

## Completion criteria

- Revised correctness is attained by the lawful scripted strategy within the stated horizon for all required interventions, without privileged solver input.
- Actual candidate/control/witness serialization meets output limits; every permitted retained context for an admitted size/template has a complete capacity argument and passing fixtures.
- Evaluate both declared sizes and state explicitly which pass. Failure at target size can use only lossless representation or the specified uniform fallback, with all affected contracts/witness checks renewed. M5 still determines final accepted size.
- If no permitted contract fits, or the bound has a gap, keep M2 blocked and record the exact incompatibility for an explicit scientific decision. Never truncate history or invent new caps.
- Close M2 only with all six tasks' evidence linked in the plan. This does not permit GPU use: M3 and M4 must also pass.

## Validation and evidence

The evidence through the original blocked handoff below records the pre-revision
implementation at commit `ed86f1b`. Its negative report is preserved separately
as `capacity_report_8192_original.json.gz`; the original commands/counts describe
that version. The authorized remedy section records current implementation and
supersedes the old gate status. The current capacity command uses the renewed
positive report, not the historical archive.

Retain the local-view witness trace, per-shape token table, tokenizer/template identity, worst-case accounting and adversarial input/output fixtures. Recheck visibility, synchrony, retention and replay against the finalized renderer where it changed. Show requested versus admitted sizes and the command/environment for every capacity result.

**CPU witness checkpoint (4 October 2026):** [witness.py](../../../recovery/witness.py)
accepts only a permitted local view, forwards each current private shard to a
different peer in rounds 1–3, and uses the existing mathematical functions only
after all current records are locally held. Pending replacements prevent solving;
known BFS tombstones are excluded from the local active graph. Legal placeholders
fill earlier slots. Active prose exercises Q without contributing solver input.
All five [attainability checks](../../../tests/attainability_checks.py) pass with
the injected CPU counter (`python -m unittest tests.attainability_checks -q`):
five families, both sizes, every scheduled sibling/repeat of the first saved
world per family, full-information controls, L replacement timing, F reacquisition,
and reversed invocation order. The full CPU entry point includes these checks.
Native witness traces, actual output token tables and complete capacity admission
were still open at this checkpoint. No scripted evidence is a model-capability result.

**Native witness checkpoint:** Four checks in
[tokenizer_attainability.py](../../../tests/tokenizer_attainability.py) pass using
the pinned Qwen3.5-9B tokenizer. The losslessly compressed
[local-view archive](../../../tests/fixtures/attainability_traces.json.gz) retains
10 family/size cases, 1,080 four-peer rounds plus 20 controls, 4,340 calls and
384 exact parent joins. Sources, delivery labels, physical output IDs, solver
availability, Q queues/release and actual reply serialization reproduce. Every
prefix and continuation attains joint correctness by round four; controls are
correct. Inputs use 699–4,915 tokens plus the full 384 output reserve; actual
witness replies use 20–195 tokens. Correct-width candidate/control/one-shard
fixtures use at most 210 tokens at target and 162 at fallback. Compression is
only for the offline evidence file; peer rendering and retention are unchanged.
Complete capacity admission remains open and adversarial investigation has
identified a real overflow; this checkpoint does not close M2.

**Prerequisite handoff (4 October 2026):** [M2-T05 completion](M2-T05-mixed-and-prose-delay-replay.md#completion-and-handoff)
passes 158 source/installed CPU checks and all 22 native-tokenizer checks.
`start_continuation` now supplies Q's parent-equivalent boundary.
`obtain_continuation_round` captures scheduled settings/seeds/replies in an
in-memory `SavedRound`; mixed/Q round one requires exact matching B/C parent
records, including invalid/failed outcomes. `commit_continuation_round` assembles
branch-local effects and Q source/prose delivery, with chronological release
before round three. Use this pair for the witness's scheduled continuations;
the provider receives permitted view/render/native input plus keyword seed and
settings. Held counts derive from committed queues/deliveries. The retained
54-round native replay archive verifies controls and timing, not attainability
or complete capacity. Durable save-before-effects integration remains M3.

## Output contracts and constructive argument

The strategy uses only the current locally held records and the public output
assignment. For every peer i, rounds 1–3 send the complete current private shard
to `(i+r) mod 4`. Each other peer therefore receives that shard once before round
four. This argument does not depend on input values, old candidate correctness,
edited owner or group partition. A pending L replacement prevents solving until
the owner forwards it; F reuses the same three sends to reacquire discarded remote
records. Delivered BFS tombstones count as known evidence and are omitted from
the local active graph. All scheduled rounds run, including after early correctness.
Receipts and received prose are exercised but are unnecessary for this witness.

The native archive executes every scheduled sibling/repeat for the first saved
main world of each family/size, through the actual schemas, renderer, synchronous
barriers, event boundaries and exact B/C-parent obtain/commit interface. This is
a constructive horizon/channel check, not population inference or a natural LLM
prefix. The per-shape table below takes the maximum over peer assignments, uses
the actual `x000`/`e000` IDs/reference fields, permits correct-range width extremes,
and includes the witness's short prose. Actual revised sends also exercise v2.

| Size | Family | Team candidate, empty send | Candidate + own shard | Full-information control |
|---|---|---:|---:|---:|
| target | Top-K | 36 | 147 | 36 |
| target | Prefix | 38 | 149 | 134 |
| target | Difference | 99 | 210 | 99 |
| target | Sort | 30 | 141 | 102 |
| target | BFS | 56 | 119 | 56 |
| fallback | Top-K | 36 | 123 | 36 |
| fallback | Prefix | 30 | 117 | 102 |
| fallback | Difference | 75 | 162 | 75 |
| fallback | Sort | 24 | 111 | 78 |
| fallback | BFS | 38 | 89 | 38 |

All rows fit 384 output tokens. A separate per-row upper bound pays one token
per candidate/punctuation byte and per digit in fixed-width IDs/versions/
recipients, with exact native BPE costs for the remaining fixed scaffolding.
The exposed pre-tokenizer/model segmentation is checked against the complete
native encoded IDs. Candidate extrema maximize correct integer character widths;
all-negative differences/distances also cover the possible sign punctuation.
Thus all correct-value widths and all live reference digits fit, with worst
upper bounds **245 target / 189 fallback**, not just the ten sampled worlds'
realized values. Both measured counts and these bounds are retained per row.
Arbitrarily wrong integers acquire no new numeric
cap: actual 200-digit signed mistakes are also validated and retained in the
capacity fixtures. Simultaneous maximum references/prose is not required to fit.

## Capacity accounting and exact failure

[tokenizer_capacity.py](../../../tests/tokenizer_capacity.py) retains the complete
calculation and 30 rendered adversarial fixtures in
[capacity_report_8192_original.json.gz](../../../tests/fixtures/capacity_report_8192_original.json.gz), alongside
two counterexamples obtained through an actual initial round. Six native checks
pass; the command then returns **1**, deliberately reporting failed admission.
Passing regression checks that reproduce an overflow does not pass the M2 gate.

Before recovery round four, B and retained mixed/Q peers can retain seven own
replies and at most 21 received texts (three other senders per generating slot).
The same envelope covers earlier prefix/recovery calls. C/F retain at most three
new own slots; K adds only its actual fourth-prefix result/absence. The accounting
overbounds even K with a separate full 384-token candidate allowance in addition
to all seven B slots. Q's held/released round-one text contributes once within
the 21 texts, never as another history copy. Its release uniqueness and exact
parent controls are checked by the witness archive and unchanged T05 fixtures.

The fixed-data envelope includes actual instructions/hints, public IDs/owners/
positions and output assignments, all current records, pending/deleted spelling,
v1/v2 notices and ordinary/disclosed receipts, all history/feedback labels, latest
status/candidate metadata and one current first-acquisition entry per source.
It uses maximum-width source values/endpoints, the widest edited ID/position,
and the longer peer-delivery labels;
these static envelopes deliberately overallow combinations that a generated
world need not realize. Seven fixed public feedback descriptions are included;
their actual 32-token guard remains in force. No past raw source-table renderings
or offline reference-attempt/queue IDs enter the accounting or peer request.

The pinned byte-level BPE has all 256 byte tokens. The maximum UTF-8 byte length
of a vocabulary symbol is 256, an upper bound on its decoded byte payload.
ASCII JSON escaping costs at most six bytes per decoded byte, including controls,
quotes, backslashes, Unicode and invalid UTF-8 replacement. Thus an own physical
token contributes at most 1,536 escaped bytes. Raw replies are bounded by their
384 persisted generated IDs, not by assuming that re-encoding has equal length.

Literal prose counts use NFC normalization. The installed native NFD implementation
was checked over every Unicode scalar: maximum canonical expansion is four
scalars. For encodable scalar text, the original scalar count cannot exceed the
NFD length of its normalized text. Paying 12 JSON bytes per original scalar gives
an overbound of `12 × 4 × 256 = 12,288` escaped bytes per counted prose token.
The current template adds 85 fixed bytes; its exact identity is checked. Every
rendered request is ASCII and byte-level BPE needs no more than one token per
byte. Consequently, with C denoting the complete fixed-data envelope:

`input_tokens ≤ C + 85 + (7×384 + 384)×1536 + (21×128)×12288`.

C ranges from 8,163 to 14,079 bytes across the ten task/size shapes. These deliberately
loose input upper bounds are 37,756,968–37,762,884 tokens, before the 384 reserve.
They are finite accounting bounds for encodable text, **not** a tight worst case,
a passing admission argument, or an estimate of ordinary context length. The
unpaired-surrogate gap below is separately exposed. No gate is certified from
the earlier research's 5,600-token payload sum or illustrative 7,175-token input.

The exact counterexample establishes failure independently of upper-bound
looseness. Model-vocabulary token **76374** decodes to 32 newlines. One invalid
reply uses exactly 384 physical tokens, termination `length`, and no repaired or
inherited candidate. The validator correctly archives its literal text and gives
nine-token JSON feedback. Three other peers legally send 128 prose tokens each.
All initial requests and outgoing valid messages fit their caps. The next focal
peer request, at **prefix round two**, fails:

| Requested size | Input tokens | Output reserve | Total | Capacity admission |
|---|---:|---:|---:|---|
| target | 14,258 | 384 | 14,642 | failed |
| fallback | 13,965 | 384 | 14,349 | failed |

The production tokenizer rejects the request without truncation or mutation.
Even without received prose, the preliminary check used 13,805/13,512 inputs;
the saved counterexamples above include the complete lawful incoming traffic.
Thirty additional retained-view fixtures cover every family and size: maximum
invalid newline history, 384-token ASCII own replies plus maximum incoming prose
and feedback, and valid large integer mistakes. They include source-delivery
metadata, notices and receipts. These are constructed permitted-history envelopes,
not executed long adversarial prefixes; the reachable round-two failures suffice
to reject universal admission. The report retains every actual rendered request,
local view, physical own IDs, token count and accounting row.

Simple lossless layout changes also fail to establish admission. Token **224227**
decodes to a Cyrillic word with leading space; repeating it 384 times re-encodes
to 2,304 tokens. For seven such prior replies, history alone uses 177,491 tokens
with ASCII JSON, 16,211 with UTF-8 JSON, or 16,212 as labeled raw text, before
source tables, instructions and output reserve. These are layout probes, not
changes to the production renderer. They disprove those particular remedies;
they do not prove that every conceivable lossless encoding is impossible.
Opaque compression or a new text transformation has no passing usability/capacity
argument here and is not silently substituted for literal retained work.

The special-string fixture preserves NUL, tabs/newlines, quotes/backslashes,
non-ASCII characters, `<think>`/`</think>` and `<|im_start|>` in actual rendered
received prose. A separate 38-token reply contains a JSON `\ud800` escape. The
current schema accepts its string, but counting literal prose raises a native
`TypeError`. No reply repair, surrogate replacement, new Unicode prohibition,
partial delivery or model retry is introduced. This additional schema/tokenizer
incompatibility needs an explicit protocol resolution before universal admission.

**Requested sizes:** target and fallback. **Admitted sizes:** none. Default
configuration, scientific specification, caps and live renderer remain unchanged.
Uniformly reducing world count cannot resolve a per-call failure. M5 still owns
final accepted size/model/environment after all earlier gates pass.

## Reproduction environment and commands

Executed on Windows / CPython 3.11.9. Source/native checks use Pydantic 2.12.5;
the installed `.venv` uses Pydantic 2.13.5 and passes `pip check`. Native checks use
Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0.
No model weights, generation, GPU allocation, pilot or main run was used.

The 9B tokenizer revision is `c202236235762e1c871ad0ccb60c8ee5ba337b9a`; 4B is
`851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Their tokenizer JSON, configuration
and external template are freshly verified byte-identical. The capacity harness
checks the previously established identities and the actual loaded template:

- tokenizer JSON SHA-256: `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42`
- tokenizer configuration SHA-256: `316230d6a809701f4db5ea8f8fc862bc3a6f3229c937c174e674ff3ca0a64ac8`
- template SHA-256: `a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715`

The loaded class is `Qwen2Tokenizer`, using the actual non-thinking template and
generation prompt. The capacity archive's 9B provenance also identifies the
byte-identical 4B tokenizer reproduction; it does not claim a 4B model test.

```powershell
python -m unittest tests.attainability_checks -q
python -m recovery validate --manifest tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json --authoritative tests/fixtures/population_target.json
python -S -m recovery validate --core-only
python -m tests.tokenizer_attainability --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
$env:PYTHONHASHSEED = '37'
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/4B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_rounds --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_events --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_replay --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

The final source and installed-outside-checkout suites each pass **163 CPU checks**
(the prior 158 plus five attainability checks). Core-only passes 80 with site
packages disabled. All **32 native verification checks** pass: the unchanged
22 prior checks, four witness checks, and six capacity/counterexample checks.
Fresh-process 4B capacity reproduction under `PYTHONHASHSEED=37` agrees exactly;
both capacity commands deliberately exit 1 for failed admission. Gzip fixtures
contain canonical UTF-8/LF JSON and `mtime=0`; normal checks only read them.
Creation uses `--write-fixture <new.json.gz>` with exclusive creation, never
overwriting a prior evidence archive.

## Blocked handoff and required decision

**At the original handoff, M2-T06 was implemented as CPU preparation and validation, but was not done.**
Attainability/output completion criteria pass; complete permitted-context
admission fails for both sizes, with a separate unpaired-surrogate gap. M2 remains
blocked (five of six tasks done); M3–M6 remain dependency-blocked. Prior task
evidence remains valid for its named checks; no passing model-capability claim
or accepted frozen configuration is created.

The safe preparation is complete: exact reachable failures, complete horizon
accounting for encodable text, useful-output/witness tables, failed ordinary
lossless layouts, Unicode boundary evidence and reproduction commands are retained.
A further remedy needs a concrete passing literal representation and a resolved
Unicode boundary, or an explicitly authorized pre-main protocol revision under
[AGENTS.md](../../../AGENTS.md). That decision must specify the affected retained
text/limits/Unicode contract and renew all affected rendering, strict-reply,
visibility, retention, mixed/Q replay, witness and capacity checks before M2 closes.
No extra cap, truncation, dropped condition, GPU authorization or design change
has been inferred from this implementation request.

## Authorized remedy implementation — 5 October 2026

The user selected ranked option 1 and then explicitly instructed implementation.
This supersedes the earlier documentation-only instruction. The scalar-message
clarification is implemented in [protocol.py](../../../recovery/protocol.py):
unpaired decoded surrogates are whole-reply schema failures before prose counting;
valid escaped pairs are accepted. Raw reply/IDs, bounded message-schema feedback,
candidate absence and no-effects semantics remain intact. The focused CPU suite
passes 25 checks and native protocol suite passes seven checks, including controls,
combining characters, escaped pairs and special-looking strings. Original negative
evidence remains in [the original archive](../../../tests/fixtures/capacity_report_8192_original.json.gz).
The lossless literal layout, column tables and template-safe footer are now
implemented. [The complete native proof](../../implementation-research/m2-t06-capacity-proof.md)
bounds the full horizon by 261,388 including reserve within the uniform 262,144
limit; all eight capacity checks admit target and fallback. Source validation
passes 167 checks and core-only passes 81. Native rendering, protocol, barriers,
boundaries, exact replay and witness archives are renewed; installed-library and
fresh-process reproduction checks pass. GPU memory, capability and
timing remain M5; no GPU run or accepted freeze is authorized.

## Completion and M2 gate

**M2-T06 is done; M2 is 6/6 verified on CPU.** The user-authorized pre-main
revision preserves retained work in the finalized literal layout and raises only
the uniform input regime; generated output (384), prose (128), feedback (32),
rounds, populations, interventions and replay rules remain fixed.

| Capacity evidence | Target | Fallback |
|---|---:|---:|
| Complete full-horizon input + output upper | 261,388 | 259,868 |
| Uniform context, including all output reserve | 262,144 | 262,144 |
| Former reachable round-two overflow, now input + reserve | 2,664 | 2,409 |
| Correct candidate/control/own-shard output upper | 245 | 189 |
| CPU admission | passed | passed |

The [complete argument](../../implementation-research/m2-t06-capacity-proof.md)
audits all 248,077 loaded vocabulary entries, including seven configuration-added
tokens, every Unicode scalar using the native normalizer, and 243 unassigned output
IDs that decode empty. Physical IDs remain recorded/charged. It derives weights
48/45, seven own/21 received allowances and complete structural fields. These
are proof allowances, not generated-token accounting or observed maxima.
The [renewed capacity archive](../../../tests/fixtures/capacity_report.json.gz)
contains all ten family/size bounds and 80 adversarial envelopes: newline/ASCII,
Cyrillic/Thai re-encoding, split Unicode, invalid UTF-8, special tokens and large
wrong integers. Maximum observed input is 33,106; this is not the proof.

The renewed witness still records 4,340 calls and 384 exact parent joins; all
required final answers remain correct. Input ranges are now 716–4,229 plus reserve;
output floors/bounds are unchanged. The replay archive now has 78 rounds, 312
requests and 104 exact parent comparisons, including persisted Unicode-invalid
parents with no source/prose effects or candidate backfill. Length decoding,
fake block headers, trailing controls, native template stripping and separate NFC
representation are explicitly checked. Original failure evidence remains intact.

**Executed verification:** source and actual installed-library suites each pass
167 checks; core-only passes 81 with site packages disabled. All 37 native checks
pass (6 renderer, 7 strict replies, 3 rounds, 4 events, 5 replay, 4 witness, 8 capacity).
A fresh process with `PYTHONHASHSEED=37` reads/reproduces every native archive and
independently reproduces the 9B report with 4B metadata; both capacity commands
exit 0. `pip check`, compilation, Markdown links/anchors, task totals and
`git diff --check` pass. Environment/revisions above remain current. The installed
harness runs from the host temporary directory, imports the actual `.venv`
package before adding source tests, and uses Pydantic 2.13.5. Its exhaustion test
now supplies the source config explicitly; it does not rely on a packaged config.

Reproduction uses the commands above with current archives; the historical
8,192 report is evidence from `ed86f1b`. Installing the current package uses
`.venv/Scripts/python.exe -m pip install --no-deps .` with normal build isolation.
No model weights, generation, GPU allocation, pilot, accepted freeze or main run
was used. Static FP16 full-attention KV at the cap is 8 GiB before other memory
and 1.5 GiB headroom. M5 must verify actual resources/capability/timing; CPU
admission does not admit a T4 configuration.

**Handoff:** [M3-T01](../M3/M3-T01-durable-round-runner.md) is ready for durable
save-before-effects integration. Progress is nine done, one ready, 19 blocked;
M3–M4 still precede any GPU use, and execution requires separate authorization.
