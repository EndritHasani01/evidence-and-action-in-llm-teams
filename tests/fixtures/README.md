# CPU reference fixtures

[silo_selected.json](silo_selected.json) extracts only `case_id`, raw input shards,
and `expected_output.per_agent_values` from ten vendored cases: I-09, II-11,
II-17, III-21, III-24, each at native agent counts 2 and 5. Every entry includes
its exact source path. A test compares the extraction with the original JSON.

Source: [SILO-BENCH repository](https://github.com/jwyjohn/acl26-silo-bench),
vendored in [acl26-silo-bench](../../acl26-silo-bench), distributed under its
[Unlicense](../../acl26-silo-bench/LICENSE). The mathematical definitions are
in `benchmark_generator/paradigm_i.py` (I-09), `paradigm_ii.py` (II-11/II-17),
and `paradigm_iii.py` (III-21/III-24). These fixtures exercise mathematics only;
their native sizes, ranges and ownership are not the study distribution.

Production solvers are independently written. Test references use insertion
ordering, direct prefix sums, difference coefficient vectors and synchronous
edge relaxation. No generator, runner, scorer or archive script is imported.
The current specification changes numeric ranges, uses four peers, and samples
BFS as a uniform labeled Prüfer tree plus five uniform nonedges. It requires
ordered, multiplicity-preserving equality even where native hints suggest sets.

## Prepared host populations

[population_target.json](population_target.json) and
[population_fallback.json](population_fallback.json) are generated CPU fixtures
for the two mathematical sizes, using master seed `20261004` on CPython 3.11.9.
Each holds all 60 actual main worlds, five disjoint development worlds, chosen
edits, accepted eligibility, rejected attempt reasons, G/H partitions, owner-order
seeds and generation/ownership/edit/partition/prefix/continuation/control seeds.
Each had one rejected attempt for no owner-held changing Top-K record: target
world 10 and fallback world 12.
The 40-world population is the first eight per family, derived from each saved
60-world fixture. Receipt/Q/preserving/repeat memberships are also derived by
the fixed specification rules, with no duplicate population store.

These are host fixtures with hidden raw sources and future edits. They must
never be passed to a peer renderer. They contain no evaluator gold, D/U masks,
model replies, accepted inference configuration or experimental outcomes.
They are prepared evidence, not the M5 freeze. Regeneration is checked against
their exact bytes; changing valid inputs is checked against the saved authority.
Source IDs are world-local; `world_id` plus configuration supplies their scope.

Reproduce a **new** file (existing manifests cannot be overwritten):

```powershell
python -S -m recovery prepare --seed 20261004 --output population.json
python -S -m recovery validate --core-only --manifest population.json --authoritative tests/fixtures/population_target.json
```

For the uniform mathematical fallback, pass a TOML file containing exactly
`size = "fallback"` with `--config` to both commands and use the fallback
authority. Selecting 40 rather than 60 worlds never regenerates inputs.

## Prepared host schedules

[schedules_target.json](schedules_target.json) is the canonical CPU schedule
derived from [population_target.json](population_target.json). It saves main
60 and development branches/calls, assigned seeds, original-prefix parents and
required B/C first-round replay parents. The nested 40 is selected from those
same branches; it keeps their IDs, seeds and shared prefix. Raw inputs/edits stay
in the population authority and are not copied into the schedule.

Main distinct/logical slots are 16,152/17,656 for 60 and 11,504/12,560 for 40.
Development has 1,114 distinct/1,178 logical slots. Its first 90 are 80 prefix and
ten complete-world controls; smoke is separate with at most 24 further calls.
There are no model replies or outcomes in this fixture. Schedule labels are
host-only and must never enter a peer view. These are CPU preparation records,
not an accepted M5 freeze or evidence of protocol/hardware feasibility.

Reproduce a **new** file and validate the saved opportunities/dependencies:

```powershell
python -S -m recovery prepare --manifest tests/fixtures/population_target.json --output schedules.json
python -S -m recovery validate --core-only --manifest tests/fixtures/population_target.json --schedule schedules.json --authoritative tests/fixtures/population_target.json
```

For the mathematical fallback, use `population_fallback.json` and a configuration
containing exactly `size = "fallback"` with `--config` on both commands. The
fallback schedule is checked by byte-stable save/reload and installed preparation;
a duplicate retained fixture is unnecessary. Loading schedules never invokes the
world generator or schedule builder. Structural validation detects scientific
changes; optional `load_schedules(..., authoritative=saved_schedule)` also rejects
otherwise-valid artifact reordering. Population input equality remains the job
of `load_population(..., authoritative=saved_population)` / `--authoritative`.

## Permitted peer requests and tokenizer inputs

All native request archives below were renewed on 5 October 2026 under M2-T06's
literal blocks, column-labeled metadata and fixed footer. The finalized renderer
preserves raw text separately from native NFC tokenization. Prerequisite task
documents retain their original dated measurements; current counts are here.

[peer_requests.json](peer_requests.json) holds seven short scripted peer cases:
ordinary/disclosed historical receipts, a compact wrong result, compact candidate
absence, an unknown replacement edge, a known tombstone, and a retained valid
reply. [peer_view_cases.py](../peer_view_cases.py) constructs their permitted views
from ordinary task worlds. These are synthetic archive strings/candidates, with
no natural model inference or empirical outcomes. They exercise the M2-T01
interface; they do not execute retention policies or prose queues.

Each case saves exact rendered content, actual native template text, all input
token IDs and the unpadded attention mask. Standard-library tests compare the
renderer with the saved request and inspect its token archive. The separately
invoked [native harness](../tokenizer_peer_views.py) recomputes every saved token,
compares against direct native templating at both sizes/all tasks/peers/controls,
checks exact decoding/archive preservation and verifies every fixed public
feedback message fits 32 tokens. It also reproduces the Qwen assistant-turn
rewrite of archived reasoning. No inference library is imported by the full
CPU validation suite; its strict reply checks require Pydantic 2.

Provenance: Qwen3.5-9B revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`,
Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0,
on Windows / CPython 3.11.9. Local tokenizer JSON, tokenizer configuration and
template were compared byte for byte with this immutable upstream revision.
The package/revision information is offline fixture provenance, never peer data
or an accepted M5 inference freeze.

| Scripted case | Input tokens | Reserved output |
|---|---:|---:|
| Ordinary receipt | 1,743 | 384 |
| Disclosed receipt | 1,739 | 384 |
| Compact wrong result | 1,570 | 384 |
| Compact absence | 1,507 | 384 |
| Pending edge | 774 | 384 |
| Known tombstone | 799 | 384 |
| Retained valid reply | 1,502 | 384 |

Six native checks establish short-case behavior and literal-block preservation.
Complete retained-context capacity and attainability are verified separately in
M2-T06 below. The renderer rejects overflow instead of shortening retained work.

In a CPU Python environment with the recorded tokenizer packages, download only
the pinned metadata to a local folder, then verify against the retained fixture:

```powershell
$peerTokenizerDir = Join-Path $env:TEMP "recovery-peer-tokenizer"
New-Item -ItemType Directory -Force -Path $peerTokenizerDir | Out-Null
$peerTokenizerRevision = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
foreach ($metadataName in @("config.json", "tokenizer.json", "tokenizer_config.json", "chat_template.jinja")) {
    Invoke-WebRequest -Uri "https://huggingface.co/Qwen/Qwen3.5-9B/resolve/$peerTokenizerRevision/$metadataName" -OutFile (Join-Path $peerTokenizerDir $metadataName)
}
python -m tests.tokenizer_peer_views --tokenizer $peerTokenizerDir
python -S -m unittest tests.test_peer_views -v
```

The harness loads only local metadata and makes no model/GPU call. To reproduce
a **new** archive, append `--write-fixture <new_peer_requests.json>`; exclusive
creation protects existing artifacts. The checked-in fixture uses canonical
UTF-8/LF bytes, enforced by Git attributes.

## Strict replies and actual tokenizer limits

[protocol_replies.json](protocol_replies.json) saves 23 synthetic adversaries
and outcomes from [tokenizer_protocol.py](../tokenizer_protocol.py). Each generated
case retains literal text, every generated token ID, termination and the separate
known-truncation flag. Results include reached JSON/schema/permission checks,
literal prose counts, candidate validity/absence, immutable staged sources/text,
and fixed public feedback with its actual token count. The failed-slot case has
no invented raw reply or candidate. These are CPU fixtures, not sampled model
outputs, pilot results, full context admission or an accepted freeze.

The harness loads the same pinned Qwen3.5-9B metadata as the peer-request fixture.
On 4 October 2026, all four local metadata files were independently compared byte
for byte with revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. Fixture packages:
Pydantic 2.12.5, Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging
Face Hub 1.19.0 on Windows / CPython 3.11.9. Pydantic 2.13.5 also passes the
installed CPU protocol checks; these observed environments are not the M5 lock.

| Native boundary case | Generated tokens | Result |
|---|---:|---|
| Eight distinct references | 142 | Valid |
| Eight distinct references, nine attempts | 154 | Valid; every attempt retained |
| Nine distinct references | 154 | Entire reply invalid; no candidate/messages |
| Two texts totaling 128 prose tokens | 180 | Valid |
| Two texts totaling 129 prose tokens | 181 | Entire reply invalid |
| Complete JSON closing brace at output cap | 384 | Valid despite length termination |
| Complete JSON exceeding output cap | 385 | Invalid |
| Incomplete JSON at output cap | 384 | Invalid; truncation separate from termination |

Other cases cover duplicate reply/reference keys, nonfinite exponents, boolean
candidate values, stale references, escaped literal prose, unexpected special
markers, malformed output below the cap, wrong but structurally valid integers,
and failed slots. Seven native checks also verify whole-reply rejection of
unpaired decoded surrogates before effects, valid escaped pairs, controls and
combining strings. All fixed public feedback passes the actual 32-token cap.
Blanket special-token removal is shown to change an invalid reply into valid JSON;
the validator performs no stripping, cleanup or repair. The final inference
boundary must separately audit any permitted terminal transport framing in M5.

After the metadata-only download above, run:

```powershell
python -m unittest tests.protocol_checks -v
python -m tests.tokenizer_protocol --tokenizer $peerTokenizerDir
python -m tests.tokenizer_peer_views --tokenizer $peerTokenizerDir
python -m recovery validate
```

The full CPU CLI runs both the dependency-free core and strict Pydantic checks;
`--core-only` explicitly excludes strict replies. The native harness is separately
invoked because tokenizer packages remain optional. It compares all saved cases
exactly, checks candidate shapes for all tasks/both sizes/peers/controls, enforces
aggregate literal prose counts, preserves repeated references, and measures all
public feedback. Its `--write-fixture <new_protocol_replies.json>` exclusively
creates a new UTF-8/LF archive; the existing fixture is protected from overwrite.

## Synchronous rounds and drained prefixes

[round_traces.json](round_traces.json) retains an eight-round scripted Prefix Sum
target-size trace produced by [tokenizer_rounds.py](../tokenizer_rounds.py)
through the actual renderer, strict reply validator and synchronous delivery
interface. All 32 opportunities have exact rendered/template requests, native
input/generated IDs, literal raw replies or an explicit failed slot, validity
stages, staged messages, committed permitted peer data and released delivery
components. The trace records 24 protocol-valid, six invalid and two failed
slots. Its continuation starts from a fresh deserialization without applying an
event/retention policy; it is a protocol fixture, not an experimental branch.

The saved prefix is committed with no pending round-four deliveries. Owner-v1
exposure records come from all four actual rendered owner requests for each
public source. Delivery components keep sender/recipient, original slot,
first usable boundary, host/peer origin, message relationships and separate
reference attempts/acquisition outcomes. Prefix-round-four messages are available
at recovery round one; final recovery messages are drained at the unscheduled
round-five boundary, which creates no fifth call. IDs, queues, full resolved
payloads and acquisition flags remain offline; current-source delivery metadata
in prompts records the first usable acquisition per version.

The fixture uses the same pinned Qwen3.5-9B revision and CPU packages listed
above. Three native checks reproduce the complete saved trace, verify both
physical orders over all five families/both sizes/all eight rounds, and check
actual rendered exposure and final prefix drain. These scripted requests use
716–3,574 input tokens plus the full 384-token output reserve; generated outputs
use 0–243 tokens. These are observed fixture ranges, not a bound on every legal
retained context, a local-view attainability witness, model capability or M5
admission. Event/retention, exact mixed/Q controls and complete capacity are
verified separately in M2-T04–T06; durable calls and process-crash checks remain M3.

```powershell
python -m unittest tests.round_checks -v
python -m tests.tokenizer_rounds --tokenizer $peerTokenizerDir
python -m recovery validate
```

`--write-fixture <new_round_traces.json>` exclusively creates a new archive;
ordinary validation only reads the retained fixture. UTF-8/LF bytes are enforced
by Git attributes. [M2-T03](../../docs/todos/M2/M2-T03-synchronous-rounds-and-prefixes.md#validation-and-evidence)
records implementation, validation and the next-task handoff.

## Event boundaries and receipt pairs

[event_boundaries.json](event_boundaries.json), reproduced by
[tokenizer_events.py](../tokenizer_events.py), retains four drained original
prefixes and 15 complete boundary snapshots with 60 exact recovery-round-one
requests/native token sequences. Prefix Sum target and Sort fallback include
all three ordinary/disclosed receipt pairs; BFS target includes L/B and Top-K
fallback includes an answer-preserving sibling. All other declared non-Q
event/policy/subset/repeat starts are checked dynamically in the CPU suite;
native differential checks cover all five families at both sizes.

The fixture uses the same pinned Qwen3.5-9B tokenizer revision and CPU packages
as the earlier native fixtures. Current sources and derived state are identical
within each receipt pair; only `before_value` changes. The archive records
serialized receipt tokens, actual complete-request input counts and their
per-peer difference. In these saved pairs, disclosure uses four fewer input
tokens for Prefix Sum and three fewer for Sort than the ordinary absence
wording. No padding is added and these are interface-package costs, not a
claim of a pure information effect or a general token bound.

Native boundary requests across all families/sizes use 753–2,924 input tokens
with 384 reserved output tokens; scripted prefix replies use 3–269 tokens.
Four native checks verify exact fixture reproduction, disclosure differences,
mixed-parent request equality, and ordinary four-round accumulation after the
boundary. The focused 19-check CPU suite also covers every saved non-Q start,
literal retention, source authority, hidden values, nested sibling mutation,
and CPU-only v1→v2→v3 transitions. K's historical candidate or absence moves
into labeled history exactly once when a new slot replaces the latest outcome;
it persists alongside ordinary new history without fabricating a full reply.
None establishes exact mixed/Q reply reuse,
the complete worst-context bound, crash safety, model capability or a live run.

```powershell
python -m unittest tests.event_checks -q
python -m tests.tokenizer_events --tokenizer $peerTokenizerDir
```

`--write-fixture <new_event_boundaries.json>` exclusively creates a new archive;
normal validation only reads the saved UTF-8/LF fixture. See
[M2-T04 evidence](../../docs/todos/M2/M2-T04-events-retention-and-receipts.md#validation-and-evidence).

## Exact parent replay and delayed prose

[replay_traces.json](replay_traces.json), reproduced by
[tokenizer_replay.py](../tokenizer_replay.py), retains five original prefixes
(Sort target and BFS fallback worlds 1/2, plus Unicode Sort target world 3),
78 scripted continuation rounds, 312 exact permitted/rendered/native requests
and 104 explicit parent comparisons. Both
events include B/C first rounds, both complementary masks and complete Q_B/Q_C
horizons. Two additional source-only Q cases record zero held prose and retain
their own B/C parent records on distinct saved world IDs. The archive-wide join
check rejects duplicate call IDs and requires every replay to resolve to one
exact recorded parent, including inactive cases.

Each round retains its saved call IDs/seeds, settings, literal raw replies and
validation, branch-local committed snapshot, pending/released component IDs
and derived per-recipient held counts. Required comparisons verify permitted
view, rendered request, native input, settings, seed and recorded outcome.
Round-two Q current sources, own reply and source metadata equal the parent;
held prose is absent from requests. At the round-three boundary its stable IDs
release before new round-two prose without moving already-seen history.
Invalid/failed outcomes, duplicate references and BFS tombstones remain literal.
The Unicode case reuses exact invalid parents containing unpaired message
escapes; their raw text/IDs persist without source/prose effects or backfill.

Five native checks reproduce the archive and exercise both masks across all
five families, both sizes, revision/sham and extra continuation replicates.
The same pinned Qwen3.5-9B tokenizer revision and CPU packages as above produce
869–2,992 input tokens plus the full 384 output reserve, and 6–134 output tokens
in this archive. These are observed scripted ranges, not complete capacity,
durability, model capability or empirical recovery evidence.

```powershell
python -m unittest tests.replay_checks -q
python -m tests.tokenizer_replay --tokenizer $peerTokenizerDir
```

`--write-fixture <new_replay_traces.json>` exclusively creates a new archive;
normal checks only read the retained UTF-8/LF file. The 19 CPU replay checks
also cover mismatches, missing versus failed parents, no-placeholder visibility,
source/prose ordering, later acquisition divergence, inactive/empty text, nested
isolation and four replayed plus twelve new opportunities per branch. See
[M2-T05 evidence](../../docs/todos/M2/M2-T05-mixed-and-prose-delay-replay.md#validation-and-evidence).

## Protocol attainability witness

[attainability_traces.json.gz](attainability_traces.json.gz), reproduced by
[tokenizer_attainability.py](../tokenizer_attainability.py), records all scheduled
siblings/repeats of the first saved world per family at both declared sizes.
The provider receives only the permitted local view. It forwards its own current
shard to a different peer in rounds 1–3, returns legal placeholders while evidence
is incomplete, and applies the existing mathematical functions to local records
once complete. It ignores derived history and historical receipt operands.

Ten cases retain 1,080 four-peer rounds plus 20 full-information controls,
4,340 calls and 384 exact parent joins, with local inputs, source-delivery labels,
physical output IDs, availability/placeholder labels, Q queues and received prose.
Every final prefix/continuation is jointly correct, including L replacement
forwarding, F reacquisition, preserving/sham siblings, receipts and mixed/Q replay.
Four native checks reproduce the archive, verify actual output contracts,
recompute answers from archived local inputs and audit unique parents/Q release.
The actual witness uses 716–4,229 input tokens plus 384 reserved output and
20–195 output tokens. Candidate/control/own-shard width fixtures use at most
210 tokens at target and 162 at fallback. These establish protocol attainability;
they establish neither complete capacity nor model capability.

Each output row also retains a correct-value serialization upper bound, at most
245 target / 189 fallback tokens. Candidate bytes and all reference/version/
recipient digits are overpaid at one token per byte; other fixed BPE pieces use
the exact backend segmentation, checked against the complete native encoded IDs.
This covers correct integer widths and any live reference ID digits without
placing a numeric cap on model mistakes.

```powershell
python -m unittest tests.attainability_checks -q
python -m tests.tokenizer_attainability --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

`--write-fixture <new.json.gz>` exclusively creates a new compressed archive.
The gzip payload is canonical UTF-8/LF JSON with `mtime=0`; normal validation
reads it without changing it. Compression reduces only the offline fixture
(31.4 MB uncompressed, 714 KB compressed), never model-visible history. See
[M2-T06 evidence](../../docs/todos/M2/M2-T06-attainability-and-capacity.md#validation-and-evidence).

## Complete capacity failure evidence

[capacity_report_8192_original.json.gz](capacity_report_8192_original.json.gz)
preserves the original report from commit `ed86f1b`, before the authorized remedy.
It retains ten task/size accounting
rows, 30 adversarial rendered views, two reachable round-two counterexamples,
three ordinary lossless-layout probes, literal special-string delivery and an
unpaired-surrogate tokenizer gap. Requests, local views, physical own IDs and
actual input counts are retained; no model was loaded or sampled.

All six original native verification checks passed. **That version's capacity
command exited 1** because neither requested size was admitted. Exit 2 denotes a failed verification
check; a regression check reproducing an overflow does not establish capacity.
One permitted invalid 384-token reply plus lawful incoming prose gives 14,258
target / 13,965 fallback input tokens before the full 384 output reserve. The
original production path rejected these without truncation. The report also identifies
ASCII escaping, re-encoding expansion, NFC prose accounting, 200-digit valid
mistakes, complete fixed fields/feedback and literal Q history counts. Its
conservative bounds are deliberately loose, never used as a passing proof.

Reproduction of this historical negative regime requires its original code at
`ed86f1b`; the current command reads the renewed positive report below. See the task's
[accounting and failure argument](../../docs/todos/M2/M2-T06-attainability-and-capacity.md#capacity-accounting-and-exact-failure)
and [original blocked handoff](../../docs/todos/M2/M2-T06-attainability-and-capacity.md#blocked-handoff-and-required-decision).

## Complete capacity admission

[capacity_report.json.gz](capacity_report.json.gz), reproduced by
[tokenizer_capacity.py](../tokenizer_capacity.py), is the current capacity evidence.
It retains ten family/size bounds, 80 adversarial envelopes, both former reachable
counterexamples, the original three layout probes, special-string delivery and
the bounded scalar-message failure. The loaded-vocabulary/Unicode audit covers
all 248,077 entries, including seven tokens added by tokenizer configuration,
and all Unicode scalars. It also checks all 243 unassigned output IDs decode
empty while preserving their physical output cost.

The [complete argument](../../docs/implementation-research/m2-t06-capacity-proof.md)
bounds target by **261,388** and fallback by **259,868**, including all 384
output tokens, within the uniform **262,144** context. Both sizes pass CPU
admission. The former reachable overflow now uses 2,664 target / 2,409 fallback
including reserve. Adversaries cover repeated newline/ASCII, Cyrillic/Thai
re-encoding, split Unicode, invalid UTF-8, native special tokens and large valid
wrong integers. Maximum observed input is 33,106; the complete bound supplies
admission, not this measurement. Histories remain literal and are never trimmed.

```powershell
$env:PYTHONHASHSEED = '37'
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/4B"
```

Both commands pass eight native checks and return **0**. Exit 1 denotes blocked
capacity; exit 2 denotes failed verification. A separate fresh process with hash
seed 37 also reproduced all 37 native checks/archives. The 4B tokenizer/template
metadata are byte-identical to the pinned 9B artifacts; immutable revision/file
identities, actual template/class, non-thinking setting and CPU packages are
recorded in the report. No model was loaded or sampled. GPU feasibility is open:
static FP16 full-attention KV alone at this cap is 8 GiB, before weights, other
state/workspace and 1.5 GiB headroom. M5 must verify memory, capability and timing.

`--write-fixture <new.json.gz>` exclusively creates a new canonical UTF-8/LF JSON
archive inside gzip (`mtime=0`); normal checks only read it. Compression is offline
storage only. [M2-T06 completion](../../docs/todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate)
records source/installed-library/core validation and closes M2's CPU gate.

## Durable round runner traces

[durable_round_traces.json.gz](durable_round_traces.json.gz) and
[durable_native_traces.json.gz](durable_native_traces.json.gz) are derived CPU
validation exports from the actual LangGraph/SQLite runner. The first uses the
injected word counter; the second uses pinned Qwen3.5-9B tokenizer metadata.
Neither samples a model. Each covers target Sort and fallback BFS, all their
scheduled four-peer branches (these archives omit controls; T03 verifies them below), four prefix
and four recovery rounds, both events, receipts, preserving edits and repeats:
60 branches, 240 rounds, 960 logical calls, 864 physical attempts and 96 prescribed
parent reuses. Unicode-invalid and failed parents remain exact. Two Q delivery
transitions resume from saved replies, and both live SQLite backups reopen with
identical committed states and successful integrity checks.

[durable_archive.py](../durable_archive.py) derives exact views, rendered/native
requests, raw replies/validity, logical/physical joins, committed states/queues
and deterministic attempt statuses. Attempt wall clocks remain recorded in the
SQLite ledger and are omitted from this reproducible fixture. The exports have
no authority over runtime effects. JSON is canonical UTF-8/LF, gzip `mtime=0`;
ordinary reproduction reads the existing archive. `--write-fixture` exclusively
creates a new file.

```powershell
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.durable_archive
python -c "import sys; from pathlib import Path; sys.path.insert(1,str(Path('.venv/Lib/site-packages').resolve())); from tests.durable_archive import main; raise SystemExit(main())" --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B" --fixture tests/fixtures/durable_native_traces.json.gz
```

The native command uses the host's Transformers 5.12.0 / tokenizers 0.22.2 and
the tested `.venv` LangGraph/Pydantic packages; source imports take precedence.
Tokenizer/config/template files match the existing M2 identities. The metadata
path is local and may need replacement on another host; install the tokenizer
dependencies there before reproduction. [M3-T01](../../docs/todos/M3/M3-T01-durable-round-runner.md#validation-and-evidence)
records environment and focused/full verification. M3-T02 now verifies bounded
process attempts and killed-controller recovery below; scheduling/accounting and
combined lifecycle acceptance remain M3-T03–T05.

## Bounded attempt and process failure traces

[attempt_failure_traces.json.gz](attempt_failure_traces.json.gz) records 12 CPU
failure cases derived from the actual attempt ledger and replacement checkpoints:
78 attempts, 28 resident-process intervals, nine uncertain completions and four
unknown attempt end times. It retains exact calls/raw outputs/validation,
physical request instrumentation, committed states and real UTC/elapsed timing
measurements. Five confirmed hung timeouts exceeded their deadlines by
0.015–0.031 seconds on the retained Windows CPU run. This is protocol evidence,
not a model result, allocation ledger or GPU-timeout admission.

[attempt_archive.py](../attempt_archive.py) executes all 22
[attempt checks](../attempt_checks.py), including real
[controller kills](../attempt_worker.py), and compares exact call outcomes,
attempt statuses and committed states with the saved archive. Measured clocks,
PIDs and local module paths remain in evidence and can differ on reproduction.
Known timeout decisions survive kills during termination; ambiguous completion
and measured work survive restart without a third physical attempt.

```powershell
.venv/Scripts/python.exe -m unittest tests.attempt_checks -v
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.attempt_archive
```

To retain another measured run, append `--write-fixture <new_archive.json.gz>`;
exclusive creation protects prior evidence. JSON is UTF-8/LF with gzip `mtime=0`.
Reproduction never loads weights or performs model/GPU inference. See
[M3-T02 evidence](../../docs/todos/M3/M3-T02-bounded-attempts-and-failures.md#validation-and-evidence)
for the tested environment, bounds and remaining M3/M5 gates.

## Local worker scheduling traces

[worker_scheduling_traces.json.gz](worker_scheduling_traces.json.gz) is a derived
CPU export from two isolated worker controllers and their bounded resident
generation processes. Eight validation scenarios retain 666 logical calls,
618 distinct generations, 619 physical attempts, 48 exact mixed/Q replay uses,
17 process intervals and one uncertain interrupted attempt. Scenario totals
describe separate scripted validation runs, not experimental coverage.

The archive retains exact requests, saved seeds/settings, invalid/failed raw
parents, original generation joins, independent committed states/queues and
actual attempt/process times. It includes reversed peer/sibling order and
worker rotation, reopening completed work without generation, Q interruption
with held prose, a lost round acknowledgement, and five-family controls before
recovery. Device visibility is a CPU test label, not a measured CUDA device.

[worker_archive.py](../worker_archive.py) runs the focused
[worker checks](../worker_checks.py) and compares the canonical JSON scientific
records exactly. Worker placement, clocks/PIDs and module paths remain recorded
measurements and may differ on reproduction. Raw strings, token IDs, requests,
seeds, parent IDs, attempt outcomes and peer/queue state must match. Tuple fields
are normalized to their retained JSON arrays before comparison.

```powershell
.venv/Scripts/python.exe -m unittest tests.worker_checks -v
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.worker_archive
```

`--write-fixture <new_archive.json.gz>` exclusively creates a new UTF-8/LF,
gzip `mtime=0` archive. Ordinary reproduction reads existing evidence. No model
weights or GPU inference are used. [M3-T03 evidence](../../docs/todos/M3/M3-T03-local-worker-scheduling.md#validation-and-evidence)
records the environment and checks; M3-T04 owns allocation/policy costs and
terminal progress, M3-T05 the combined gate, and M5 hardware admission.

## Resource accounting and progress traces

[accounting_progress_traces.json.gz](accounting_progress_traces.json.gz) retains
nine CPU evidence cases: hand reconciliation, bounded ambiguous work, slower
device forecasts, failed-configuration costs, historical measurement admission,
timeout admission stops, a hard deadline and its resume, and terminal heartbeat
captures. Allocations explicitly say `synthetic`; these are protocol checks,
not GPU spending, model capability, pilot or main outcomes.

The hand schedule has 112 logical slots, 100 generations, 12 exact replays and
101 attempts including one infrastructure retry. It reconciles 203 recorded
synthetic attempt seconds against 400 allocated seconds on two synthetic devices.
These assigned two-second call/three-second interruption costs are hand-test
inputs, not observed inference times. B,
P_G and Q_B each cost 67 policy seconds; C, F and Q_C each cost 64, always
including the prefix and all 16 continuation uses. Ambiguous work changes the
physical attempt range to [201, 203] without inventing an end time.

[accounting_archive.py](../accounting_archive.py) runs the focused
[accounting checks](../accounting_checks.py) and reproduces exact joins, counts,
hand costs, delivery records and stop/resume outcomes. Actual clocks, checkpoint
IDs and CPU durations remain retained measurements, with bounds checked by the
tests rather than asserted byte-identical. Backup/restart, concurrent saver
initialization, cross-worker read races, token-count migration, live CLI reads
and provider reservation starts are additionally verified by these checks.

```powershell
.venv/Scripts/python.exe -m unittest tests.accounting_checks -v
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.accounting_archive
```

`--write-fixture <new_archive.json.gz>` exclusively creates a new UTF-8/LF,
gzip `mtime=0` export. Ordinary reproduction is read-only. Earlier attempt/worker
comparators omit the newly derived `request_tokens` scalar (the original
requests remain their authority) and absent peak-memory metadata; all original
scientific fields still compare exactly. Token-count/measurement checks verify
the added resource fields separately. Every prior fixture remains unchanged.
See [M3-T04](../../docs/todos/M3/M3-T04-accounting-progress-and-budget.md#validation-and-evidence).

## Crash-safe scripted lifecycle run bundle

[scripted_lifecycle_run.zip](scripted_lifecycle_run.zip) is an ordinary CPU run
bundle: saved complete target/fallback population and schedule inputs, worker
SQLite snapshots, supported reopened backups, actual controller commands/logs,
boundary markers, physical request traces and derived progress/outcome previews.
The ZIP is packaging; manifests and worker records retain their existing formats
and authority. SQLite backup includes committed WAL even for a killed owner.
No new persistence or test-management service is involved.

[lifecycle_checks.py](../lifecycle_checks.py) and the externally killed
[controller](../lifecycle_worker.py) cover raw commit, deterministic validation,
staging, delivery checkpoint and C/F boundary persistence. A cross-worker P_G
replay uses exact invalid/timeout parents; Q_B/Q_C crashes preserve held prose,
chronological release and independent original prefix/sibling states. A second
precommit kill exhausts the only retry. Synthetic allocation exhaustion retains
sixteen unknown slots and resumes with the original configuration and one
uncertain attempt. Allocations are explicitly synthetic; durations are CPU
observations, never GPU forecasts.

The two complete scripted runs each select the first already prepared main world
of every family. All their scheduled events, policies, receipts, Q variants,
controls and repeats remain included: 145 branches, 540 four-peer rounds plus ten
controls, 2,170 logical slots, 1,978 generations and 192 required replay uses per
size. The separate full-manifest reconciliation executes no slots: main 60 is
16,152/17,656 distinct/logical, main 40 is 11,504/12,560, and development is
1,114/1,178 with the complete 90-slot capability prelude. These are validation
populations and schedules, not empirical results or an accepted freeze.

Each case's `selection.json` references the complete saved manifest IDs.
`evidence.json` lists the accepted worker files, baseline/backup paths and counts.
The reader normalizes Windows case-directory separators to ZIP-relative paths;
new captures use forward slashes. The retained bundle stays unchanged.
Use only those worker files together; interrupted originals, baselines and
backups are copies of the same identities. `kill-*.json` contains the actual
subprocess launch argv and exit receipt; the test applies `Popen.kill()` externally
and confirms owner/inference exit before reopening. `boundary-*.json` records
the precise point and both WAL/FULL connections. `progress.json` includes all
logical/physical/policy joins and explicit missing costs. `offline-preview.json`
derives exact slot correctness and D/U footprints without generation. Its
preview is not the M4 estimand, diagnostic, uncertainty or reporting pipeline.
The stopped budget snapshot/preview remains alongside its resumed worker.

```powershell
.venv/Scripts/python.exe -m unittest tests.lifecycle_checks -v
.venv/Scripts/python.exe -m tests.lifecycle_archive --audit-only
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.lifecycle_archive
```

`--write-fixture <new_run.zip>` exclusively creates another bundle. Normal
reproduction preserves the retained ZIP and compares every exact call/input,
validation, committed transition, delivery, outcome and bounded attempt status.
It ignores only measured clocks/checkpoint IDs, process/module paths and worker
placement; actual measurements remain in the archive. Offline audit reconstructs
complete progress/cost/outcome records at their saved timestamps, verifies both
full schedules and reopens every accepted SQLite file. No weights, GPU, pilot or
main inference is used. See [M3-T05](../../docs/todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#validation-and-evidence)
for gate evidence and the Windows CPU environment; M4 remains mandatory before
GPU use, and the eventual accepted host must repeat persistence checks in M5.
