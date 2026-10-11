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

## Prepared course inputs and schedules

[population_course.json](population_course.json) and
[schedules_course.json](schedules_course.json) form a separate CPU preparation
bundle under [Specification Section 11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime).
The manifest explicitly records `regime="course"`, fallback mathematical size
and master seed `20261009`. It saves 20 actual main worlds, four per family with
one edited-owner block, and five separate development worlds. Existing world,
source, branch and call IDs keep their spelling within this bundle; they are
not cross-bundle replay identities. All assigned seeds are disjoint from both
saved thesis-size fixtures (`20261004`) and course main/development domains.

Receipt, Q and preserving cohorts each contain eight main worlds. Only the
first world per family has an additional continuation seed set: five repeats
retain their original prefix and G/H partition. Siblings match continuation
seeds across events/policies; only prescribed first-round mask/Q uses replay.
Main is 5,752 new / 6,280 logical slots (528 replay uses). Development retains
1,114 / 1,178 (64 replay uses), with 80 prefix and ten complete-world controls
first; smoke is separate. No outcomes, model settings or accepted freeze are
stored, and peer metadata must still use only the public source projection.

Prepare **new** files; existing scientific fixtures cannot be overwritten:

```powershell
python -X utf8 -S -B -m recovery prepare --regime course --config configs/course-inputs.toml --seed 20261009 --output population.json
python -X utf8 -S -B -m recovery prepare --regime course --config configs/course-inputs.toml --manifest population.json --output schedules.json
python -X utf8 -S -B -m recovery validate --core-only --regime course --config configs/course-inputs.toml --manifest population.json --schedule schedules.json --authoritative tests/fixtures/population_course.json
```

The API uses `prepare_population(seed, Size.FALLBACK, regime="course")` and
`population.worlds()` / `schedules.main_for(population)` default to this bundle's
20-world scope. Thesis preparation still defaults to 60 with nested 40 and keeps
its saved canonical bytes; omitted manifest/schedule regime means thesis.
Loading rejects wrong course size/scope, extra repeat assignments, changed seeds,
parents and cohorts without resampling. Exact saved-authority comparisons also
detect otherwise valid input edits or schedule reordering. The input-only TOML
contains exactly `size="fallback"`; `--regime course` remains explicit. Runtime
256/64 limits, protocol/capacity, worker/analysis acceptance, model/resource gates
and freeze are owned by later course tasks.

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

## Exact offline outcomes and trajectories

[exact_outcome_tables.json.gz](exact_outcome_tables.json.gz) contains derived
M4-T01 validation tables from the authoritative manifests and accepted workers
in [scripted_lifecycle_run.zip](scripted_lifecycle_run.zip). The original bundle
is unchanged. These are scripted CPU outcomes, not model capability, a pilot,
empirical findings or an accepted freeze. [outcome_archive.py](../outcome_archive.py)
reads only ordinary JSON/application SQLite records; it imports no runner,
checkpoint library, tokenizer or inference stack.

Sixteen table cases cover the thirteen accepted worker selections, the stopped
budget selection, and full target-60/fallback-40 main manifests. Backups,
interrupted originals and baselines are never combined with accepted workers.
Each complete five-world fixture has 2,170 recorded slots, 1,978 original
physical attempts and 192 exact replay uses. The full joins retain all 17,656 /
12,560 slots, including 15,486 / 10,390 unknowns outside recorded work. The
stopped snapshot keeps sixteen unknown slots and its uncertain attempt.

Each case contains these tidy JSON tables:

- `outcomes`: exact whole-candidate correctness, execution/protocol status,
  original call/generation/replay/attempt joins, prefix-round-four context and
  usable v2 delivery IDs. BFS's saved canonical key/value pairs are decoded
  before comparison with the full node dictionary; lists retain order and duplicates.
- `coordinates`, `peer_diagnostics`: unique D/U coordinates and per-peer
  changed accuracy, explicit old-gold persistence, other valid errors,
  malformed/missing changed outputs, preservation, collateral damage and repair
  of old U errors. Eligibility uses that peer's valid final-prefix candidate;
  unknown eligibility and empty denominators have explicit reasons.
- `diagnostic_summaries`: eligible peer means, then world means, then equal
  eligible family means, with unique-coordinate/peer-copy counts. Unknown
  eligible outcomes keep the summary unknown. Grouping preserves event, policy,
  round and replicate; replicate zero remains primary.
- `rounds`, `trajectories`: all four rounds, AUC over sixteen opportunities,
  final joint correctness, first/stable joint times, regression, individual/joint
  ever-correct indicators, fragmentation and the four complete categories.
  Incomplete branches stay separate. Identical wrong agreement is N/A for
  differently assigned Prefix/Sort segments.
- `annotations`, `annotation_counts`: six nonexclusive observable labels,
  original input/outcome/prefix/delivery provenance, applicable/observed/unknown
  counts, inclusive pair intersections and exact overlap patterns (including
  unknown/N/A labels). Their unit is a scheduled peer-round, not an independent
  world or a partition of psychological causes.
- `attempts`: the original physical attempt rows, including uncertain work;
  replay never introduces another physical attempt or copied raw reply.

[Hand-checked tests](../test_evaluate.py) include duplicate-sensitive answers,
complete BFS dictionaries, valid/invalid/failed/unknown outcomes, empty D/U and
old-prefix eligibility, collateral damage versus old-error repair, all trajectory
categories and fragmentation. A rate fixture gives world means 1/2 and 0 in one
family, and 1 in a second: the equal-family mean is 5/8, with 31 unique eligible
coordinates and 32 peer copies. It must not become a pooled-coordinate ratio.
[Archive checks](../test_outcome_archive.py) reproduce every retained table and
verify full population coverage, original attempts and stopped unknowns.

```powershell
python -S -m unittest tests.test_evaluate -v
$env:PYTHONHASHSEED = '37'
python -S -m tests.outcome_archive
```

The latter compares every table with the retained export. `--write-fixture
<new_tables.json.gz>` exclusively creates another derived export; ordinary
reproduction preserves the fixture. The public `recovery analyze` command and
API are documented in [README](../../README.md#offline-exact-outcomes-and-trajectories).
Information/work inventories, cost analysis, uncertainty/missingness bounds and
the full reproducible report remain later M4 tasks.

## Prespecified estimates and conditional repeatability

[estimand_tables.json.gz](estimand_tables.json.gz) contains four derived M4-T02
cases from the original [scripted lifecycle bundle](scripted_lifecycle_run.zip):
the complete five-family fixture at each size and the full target-60/fallback-40
main joins. [estimand_archive.py](../estimand_archive.py) reads only the original
accepted workers and saved manifests. All earlier fixtures remain unchanged.
These tables validate CPU implementation; they are not model, pilot or empirical
recovery results.

- `populations` fixes the main, receipt, Q, preserving and repeat cohorts before
  outcomes. Shared world IDs preserve overlapping subsets; original prefixes,
  partitions and continuation seeds remain explicit. Preserving uses sixteen
  worlds at both main counts; repeats use ten original worlds.
- `world_contrasts` and `summaries` expose θ, its revised/sham components, φ
  (`E_keep(revision)`), sham/correction-specific/E_clear and own-group effects,
  all mask trajectories/mixed means, main secondary effects, six receipt cells,
  η/direct/representation companions, Q effects and preserving B/C/K endpoints.
  Accuracy, normalized AUC, final joint completion and preservation scopes are
  named. World/family formulas and denominators never pool peer opportunities
  or complete cases into the intended population.
- Each component retains its coefficient, exact rational mean, peers/rounds,
  eligibility, scheduled/observed calls and original call/generation/prefix IDs.
  Linear atoms include exact weights; final joint completion retains its
  all-four operator. Unknown components survive for M4-T05. Structural empty
  preservation denominators are N/A; unknown old-prefix eligibility is distinct.
- `repeat_contrasts`, `repeatability` and `trajectory_changes` retain replicate
  zero as primary. Repeats use the same prefixes/partitions and new continuation
  seeds; zero-effect ties are distinct from strict sign reversals. Incomplete
  trajectory pairs are unknown. No receipt/Q/new-prefix repetition is implied.
- `prose_activity` derives actual nonempty held texts from committed saved Q
  states, preserving delivery IDs and counts before/after release. Empty text is
  queued literally without prose exposure. Inactive/unobserved treatments remain
  included; missing committed delivery evidence is unknown, not observed silence.

Both complete fixtures have 2,170 recorded slots and θ=φ=0. Full main joins keep
15,486 / 10,390 unknown slots. Their intended primary estimates are unknown,
with five complete worlds and separately labeled complete-case values of zero.
Q activity is observed in eight branches per size; the full main tables retain
another 88 / 56 unobserved Q branches. Hand-calculated fixtures supply nonzero
effects, inactive prose, sign reversals and category changes absent from these
protocol-focused workers.

```powershell
python -S -m unittest tests.test_analysis tests.test_analysis_run tests.test_estimand_archive -q
$env:PYTHONHASHSEED = '37'
python -S -m tests.estimand_archive
```

Reconstruction compares every derived table with the retained export.
`--write-fixture <new_tables.json.gz>` exclusively creates another export.
The [CLI/API](../../README.md#offline-contrasts-and-conditional-repeats) reads
ordinary saved runs without inference. Intervals, missingness bounds, cost and
the full M4 report gate remain later work.

## Information inventories and retained work

[information_tables.json.gz](information_tables.json.gz) contains six derived
M4-T03 cases reconstructed by [information_archive.py](../information_archive.py)
from the accepted original workers in [scripted_lifecycle_run.zip](scripted_lifecycle_run.zip).
Both five-family fixtures have 2,170 recorded slots. Full target-60/fallback-40
joins retain 15,486/10,390 unknown slots; the stopped prefix retains sixteen
unknown outcomes even though its already-rendered owner-v1 exposure is verified.
No backup is combined with its original physical worker.

Each case contains `prefix`, `owner_exposure`, `communication`, `delivery_attempts`,
`receipt_timing`/`receipt_timing_counts`, `boundary_acquisition`,
`receipt_information`/`receipt_strata`, `transport_references`, `edit_descriptors`
and the information `atlas`. Call/branch/peer/round and original replay/prefix
IDs join the existing outcomes. Original committed checkpoints, decoded with
the public CPU serializer in the worker's read transaction, establish final
source acquisitions. Repeated references remain separate attempts; only newly
known ID/version pairs count as acquisitions. Unobserved commitment stays unknown.

The [association and measurement rubric](../../docs/implementation-research/information-diagnostics.md)
keeps numeric coincidence unresolved, identifies literal source-bound matches,
and states every correct-candidate assumption. A cleared old candidate cannot
supply receipt reconstruction. Prefix/Difference transport nevertheless remains
a separately labeled offline reference on the actual valid last candidate,
including its residual errors. Invalid/failed last candidates are unavailable.

The included [independent atlas witnesses](../information_examples.py) demonstrate
Max/Top-K discarded alternatives, local Prefix after-only ambiguity and
before-value sufficiency, complete Difference with an unchanged anchor, local
Sort boundary ambiguity/full-multiset sufficiency, and BFS alternative topology.
These small named views are CPU illustrations; further communication can resolve
their ambiguity. No historical archive script or output is changed.

[information_tokens.json](information_tokens.json) retains 160 native prefix
peer-round counts and 40 compact-boundary counts across all families and both
sizes. [tokenizer_information.py](../tokenizer_information.py) uses the existing
local pinned 9B metadata, validates full input-ID equality and compares independent
backend encodings. Scripted M3 token IDs cannot be substituted for native counts.
Counts describe independently encoded retained content, not marginal prompt cost
or model/GPU timing; no weights are loaded.

```powershell
python -S -m unittest tests.test_information tests.test_information_run.InformationRunTests -q
.venv/Scripts/python.exe -m unittest tests.test_information_run.InformationArchiveTests -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.information_archive
python -m tests.tokenizer_information --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

Reconstruction compares complete table values; mismatches name the case/table/row
without producing an enormous automatic dictionary diff. `--write-fixture`
exclusively creates a new derived export. [CLI/API usage](../../README.md#offline-information-and-retained-work)
accepts ordinary saved runs. These tables are validation evidence, not empirical
recovery results. [Policy costs](#policy-costs-and-frozen-boundary-rule) are now
available; uncertainty/missingness is supplied below and the complete report gate
remains M4-T06.

## Policy costs and frozen boundary rule

[policy_cost_tables.json.gz](policy_cost_tables.json.gz) contains sixteen derived
M4-T04 cases: thirteen original-worker selections from the existing M3 bundle,
two complete main population joins and one stopped prefix. Reconstruction by
[cost_archive.py](../cost_archive.py) reads evidence-named original workers only,
at the saved accounting clock `2026-10-06T00:00:00+00:00`; no providers run.
M3's exact subset-bound live snapshots independently reconcile physical and
policy totals, allocation/overhead and committed delivery IDs. Adding the full
manifest leaves physical work and known policy costs unchanged.

Each case contains `physical`, `generations`, `policy_costs`, `resources`,
`validated_deliveries`/`delivery_counts`, `retained_evidence`,
`quality_preservation`, `boundary_selections`, `selection_frequencies`,
`strategy_worlds` and `paired_comparisons`. Original call/generation/attempt,
world/event/policy/replicate/prefix IDs join the existing exact outcome tables.
Policy `seconds` and token fields reproduce M3's measured subtotals;
`complete_policy_seconds` is unavailable with any unknown scheduled policy call.
Output/memory measurement gaps and uncertain attempts are counted explicitly.
Allocation partitions and provider billing remain separate. No duplicate store,
new identity system, inference call or execution decision is added.
Retained remote evidence excludes the host-injected edited record, matching
M4-T03. The separate rule coverage requires every current record, including it.

The [hand-calculated fixture](../cost_fixture.py) has 128 logical calls,
116 original generations, 117 attempts, twelve replays, a three-second
interruption/retry, and a recorded timeout. Every other attempt costs two seconds:
physical cost is 235 seconds; B/P_G/Q_B cost 67 each, C/K/F/Q_C cost 64 each,
including the 32-second shared prefix. Known physical request/output tokens are
234/115, with two unknown output attempts. An ambiguous interruption gives
[233,235] seconds physically and [65,67] for B/P_G/Q_B. A separate 400-second
synthetic allocation partitions into one setup, three interruption, 231 attempt
and 165 idle seconds; it is never added to 235 measured attempt seconds.

Both complete five-family cases contain 2,170 logical outcomes, 1,978 physical
attempts and 192 replays. All 22 ordinary B/C/K comparison choices select K;
their frequency tables explicitly state that the rule is constant. Synthetic
all-covered/tombstone fixtures select C; missing/pending/mixed coverage selects K.
Unavailable C/K branches never trigger favorable fallback. Full target-60 and
fallback-40 joins preserve 15,486/10,390 unknown outcome slots and 134/94 unknown
choice boundaries. The stopped prefix retains sixteen unknown outcomes and one
uncertain attempt. These are scripted protocol/cost fixtures, not model findings.

```powershell
python -S -m unittest tests.test_costs tests.test_costs_run -q
.venv/Scripts/python.exe -m unittest tests.test_cost_archive -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.cost_archive
.venv/Scripts/python.exe -m tests.accounting_archive
```

Reconstruction compares every table with the retained export and reconciles
the unchanged M3 ledger. `--write-fixture` exclusively creates a new export.
[CLI/API usage](../../README.md#offline-policy-costs-and-the-boundary-rule)
supports ordinary saved runs. Uncertainty/bounds are supplied by M4-T05 below;
complete report reproduction remains M4-T06.
No GPU/model, pilot, main execution or accepted freeze is implied.

## Paired uncertainty and shared-response missingness

[uncertainty_tables.json.gz](uncertainty_tables.json.gz) records sixteen derived
M4-T05 scopes reconstructed by [uncertainty_archive.py](../uncertainty_archive.py)
from evidence-named original workers in the existing M3 bundle. Worker bytes
are checked before/after every analysis. The saved accounting clock is
`2026-10-06T00:00:00+00:00`, resampling seed 20261006, and family seeds are that
seed plus the existing task-order index. Each family draws its observed world
count with replacement 10,000 times. Sorted world IDs define the draw indices;
identical cohorts share draws across endpoints. Quantiles use linear
interpolation at `(B-1)*p`, type 7. Primaries use probabilities 0.0125/0.9875;
descriptive secondaries use 0.025/0.975. Repeats are separate conditional displays.

Each case contains all uncertainty settings, populations, original world/repeat
components, world sensitivity, family/pooled intervals and separate complete
cases, family completion counts, incomplete trajectory categories/marginals,
paired whole-policy quality/preservation/cost views and reporting references.
The complete five-family fixtures each have 2,170 recorded outcomes. Full target
and fallback joins retain 15,486/10,390 unknown slots, original main family
denominators 12/8, and only five observed worlds. Their primary point intervals
are unavailable; complete-case descriptions are zero. Frozen θ sensitivity is
[-1.8333333333333333,1.8333333333333333] for target and [-1.75,1.75] for fallback;
φ sensitivity is [-0.9166666666666666,0.9166666666666666] and [-0.875,0.875]. These
are bounds on scripted validation joins, not experimental estimates.

[Independent focused fixtures](../test_uncertainty.py) check finite stratified
resampling support, weighted/clipped Hoeffding intervals, exact binomial counts,
shared linear cancellation, shared nonlinear feasible completions, fragmentation,
conservative larger trajectories, unknown eligibility and paired cost cohorts.
Unknown shared prefix costs cancel in differences; absolute future costs have
no asserted finite upper bound. A recorded parent can constrain a missing
logical use without changing its unknown execution status. Empty diagnostic
populations stay unavailable. Larger nonlinear envelopes retain variable/term
identities and warn that marginal extrema need not be jointly attainable.

```powershell
python -S -m unittest tests.test_uncertainty tests.test_uncertainty_run -q
.venv/Scripts/python.exe -m unittest tests.test_uncertainty_archive -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.uncertainty_archive
```

Every retained table must reproduce. `--write-fixture` exclusively creates a
new derived export; the original run and all prerequisite fixtures remain
unchanged. [CLI/API usage](../../README.md#offline-uncertainty-and-missingness)
works on ordinary saved runs without importing inference. The report and full
M4 gate are recorded below; CPU evidence does not admit GPU or main execution.

## Reproducible synthetic reports

[report_tables.json.gz](report_tables.json.gz) retains sixteen M4-T06 reports
from the original evidence-named M3 workers: thirteen ordinary selections,
two full frozen 60/40 main joins and the stopped prefix. Each contains the
seven exhibits, exact case selection, deterministic plotting inputs, settings,
coverage, supporting table-row counts and repeated export/link evidence.
The source workers remain authoritative; these records are derived validation.

[scripted_reports.zip](scripted_reports.zip) is a portable companion with five
reports: complete target/fallback, deliberately incomplete full-main
target-60/fallback-40, and stopped work. Extract it and open `INDEX.md`, then
the linked `report.html`. It includes 126 files: an index, five reports with
all tables/input snapshots/traces, CSVs, cases, settings and plotting data,
and 35 SVG plus 35 PNG exhibits with plotting-environment records. Every
report/figure is labeled synthetic CPU validation. It contains no SQLite
execution copy or second authoritative store.

The complete fixtures have 2,170 recorded outcomes each. Full target/fallback
joins preserve 15,486/10,390 unknown slots and denominators 60/40, with only
five observed worlds. Intended primary estimates/intervals are unavailable;
complete-case descriptions and shared-response sensitivity are distinct.
The stopped prefix retains sixteen unknown slots and unavailable cases.
Missing native history counts and empty preservation populations remain N/A.
Cases retain exact replies, before/after edits, original call/message/delivery
IDs, trajectories, availability and preservation denominators. Invalid
non-scalar Unicode is displayed as a reversible JSON string literal without
repairing its original raw reply.

```powershell
python -S -m unittest tests.test_report tests.test_report_run -q
.venv/Scripts/python.exe -m unittest tests.test_report_figures -q
.venv/Scripts/python.exe -m unittest tests.test_report_archive -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.report_archive --export new-report-reproduction
# Optional plotting from those already-saved inputs:
.venv/Scripts/python.exe -m recovery.figures --report new-report-reproduction/complete-target
```

[report_archive.py](../report_archive.py) reads only original M3 workers,
analyzes every scope twice, compares every table/report/trace/input, checks
worker bytes before/after, exports twice and compares compressed/HTML/CSV
bytes. It checks exact scheduled/recorded/unknown counts and every local
report link/anchor. The retained bundle check joins report/plot/table/case
evidence and checks all SVG/PNG files. `--write-fixture` exclusively creates
a new expected export; it never replaces original evidence. Optional
Matplotlib rendering has its own deterministic-byte checks and was visually
reviewed; it imports no inference and reads no workers.

[CLI/API usage](../../README.md#reproducible-offline-reports),
[task evidence](../../docs/todos/M4/M4-T06-reproducible-report-and-cpu-gate.md#validation-and-evidence)
and the [M1–M4 CPU audit](../../docs/validation/m4-cpu-gate.md) record the
commands and limits. CPU report acceptance does not establish language-weight
loading, finite GPU output, T4 headroom/timing, capability, accepted-host
persistence, allocation feasibility, pilot results or main findings.

## Native inference suffix fixtures

[inference_suffixes.json](inference_suffixes.json) contains nine CPU-constructed
native generated-token sequences for the pinned Qwen tokenizer. They include a
single final transport token, internal/repeated markers, thinking/start markers,
unexpected suffixes, preserved end-of-text and valid/incomplete/invalid JSON at
exactly 384 generated IDs. These are decoding fixtures, not sampled model output.
Every case retains its generated IDs, raw suffix, parsing text, termination and
independently expected protocol validity. No normalization or repair is allowed.

```powershell
python -m tests.tokenizer_inference --tokenizer LOCAL_9B_METADATA
python -m tests.tokenizer_inference --tokenizer LOCAL_4B_METADATA
.venv/Scripts/python.exe -m unittest tests.test_inference_preparation tests.inference_checks -q
```

The native command also verifies actual template inputs, fresh generation
defaults and independent empty hybrid-cache objects, without constructing a
model. Mock subprocess checks cover saved seed/state ownership, exact raw
evidence and resume/backup behavior. See the
[M5 preparation evidence](../../docs/validation/m5-inference-preparation.md)
for the proposed smoke/allocation scope and still-unverified GPU gates.

## Course protocol and native limits

[course_protocol.json.gz](course_protocol.json.gz) is the separate course archive
for the pinned Qwen3.5-4B tokenizer revision
`851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` and explicit `COURSE_LIMITS`.
It preserves eleven permitted rendered/native cases, 23 exact reply cases and
225 candidate/one-shard cases covering the 20 main/five development worlds,
all four peers and full-information controls. Cases include ordinary/disclosed
receipts, wrong/absent compact work, pending updates, tombstones and literal
special-looking history with trailing whitespace. Exact rendered strings and
native template text/IDs remain separate.

```powershell
python -m tests.tokenizer_course_protocol --tokenizer LOCAL_4B_METADATA
.venv/Scripts/python.exe -m unittest tests.test_course_limits tests.course_protocol_checks tests.course_settings_checks -v
```

The nine native checks reproduce this archive and both unchanged thesis
request/reply archives. They verify complete JSON at 256 generated IDs versus
257, fragments/known truncation, aggregate prose 64/65, recursive duplicate keys,
strict permissions and Unicode scalars. Nine reference attempts with eight
distinct held references pass; nine distinct references fail. Useful
candidate/one-shard cases use at most 132 output tokens; fixed feedback uses at
most 14 native tokens. These finite fixtures do not establish the complete
retained-context bound or attainability gate, which belongs to course/M2-T03.
No model weights or GPU are used. The
[course M2 protocol evidence](../../docs/validation/course-m2-protocol-and-limits.md)
records environments, exact commands, installed provenance and retained failures.
The new archive never replaces original thesis fixtures or defaults.

## Course interventions and exact replay

[course_interventions.json.gz](course_interventions.json.gz) retains the separate
scripted course matrix with the pinned 4B tokenizer and explicit 256/64 settings.
It contains 25 drained original prefixes with 100 raw prefix rounds, all 438
scheduled continuation starts and all 592 exact B/C replay joins, including
development masks and main continuation repeats. Full Q horizons and selected
K/receipt horizons bring the retained continuation rounds to 630: 2,920 exact
peer requests across both phases. Raw replies/failures, rendered strings,
native IDs/masks/template text, settings/seeds, permitted state, committed state,
host/peer source attempts/acquisitions and held/released prose remain available
in existing record shapes.

The 40 first-round Q branches include eight inactive source-only cases, each
with its own unique scheduled parent IDs. The full course assertions separately
cover all-invalid/all-failed parents, Unicode and stale-reference whole-reply
failure, explicit empty prose, text-only omission/no placeholder, wrong/absent K,
pending versus known tombstones, hidden fields, version handling, sibling
mutation and invocation reversal. All 7,008 scripted continuation slots are
checked; the retained archive selects later Q/K rounds rather than duplicating
every ordinary recovery round.

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest tests.course_intervention_checks -v
python -X utf8 -m tests.tokenizer_course_interventions --tokenizer LOCAL_4B_METADATA
```

The native harness passes 15 intervention assertions and three archive checks,
and reproduces exact case records in a fresh process with hash seed 37. It loads
only local tokenizer metadata. New archives can be written with
`--write-fixture NEW_ARCHIVE.json.gz`; existing paths are rejected. Archive JSON
is canonical UTF-8/LF with deterministic gzip metadata.

Observed inputs use at most 2,563 native tokens, and replies at most 207 across
the retained prefix/continuation records, reserving the full 256 output tokens.
These are finite fixture measurements. The locally informed witness, complete
course retained-context bound and model/GPU feasibility remain separate gates.
The [course intervention evidence](../../docs/validation/course-m2-interventions-and-replay.md)
records commands, environments, installed verification and preservation audits.

## Course local witness and complete capacity

[course_attainability.json.gz](course_attainability.json.gz) retains the locally
informed course strategy across all 25 saved worlds: 100 prefix rounds, all
1,752 continuation rounds, 50 controls and 7,458 logical opportunities,
including 592 exact B/C parent joins. Existing raw record shapes preserve
permitted views, rendered/native strings/IDs/masks, replies, settings, seeds,
committed states and Q queues/release metadata. The script forwards each current
own shard to a different peer in rounds 1–3 and computes only from acquired
records. Early legal placeholders are allowed; every final prefix/continuation
and full-information control is exactly correct. Its 225 worst-width correct
candidate/control/useful-shard fixtures have maximum measured output 162 and
a universal 189-token serialization bound within 256, with useful prose within 64.

[course_capacity.json.gz](course_capacity.json.gz) retains the renewed complete
vocabulary/Unicode audit, all five structural accounting rows and 110 raw native
adversarial envelopes, including invalid own text, maximal ASCII/dash and
non-NFC prose, partial/invalid UTF-8, template-like strings, quoting/controls,
fake block headers, bounded feedback and large valid wrong integers. A real
invalid 256-token slot receives three valid 64-token texts. The largest archived
native envelope uses 22,247 input tokens; this supports the
[complete proof](../../docs/implementation-research/course-m2-capacity-proof.md),
which independently bounds **155,995 input + 256 output = 156,251**.
Seventeen additional compact/pending/receipt measurements are in the native logs.
Both pinned 4B and 9B metadata reproduce the same accounting/report. The course
model remains 4B; original positive/negative thesis archives remain unchanged.

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest tests.course_attainability_checks -v
python -X utf8 -m tests.tokenizer_course_attainability --tokenizer LOCAL_4B_METADATA
python -X utf8 -m tests.tokenizer_course_capacity --tokenizer LOCAL_4B_METADATA --comparison-tokenizer LOCAL_9B_METADATA
```

The native course runs pass 18 checks, reproduced in a fresh hash-seed-37 process
and outside the checkout with the installed package. New native archives require
`--write-fixture NEW_ARCHIVE.json.gz`; existing paths are rejected. JSON/gzip
encoding is canonical and deterministic. The
[course M2 gate evidence](../../docs/validation/course-m2-attainability-and-capacity.md)
records exact commands, metadata, passing regressions, retained failures/fixes,
installed module provenance and preservation audits. This is CPU scripted
attainability and complete native-token capacity. No model weights, GPU/model
memory/headroom, capability, pilot, main outcomes or freeze are accepted here.

## Course durable workers and bounded failures

[course_worker_run.zip](course_worker_run.zip) uses the existing ordinary bundle
layout: saved population/schedule JSON, worker SQLite backups and derived
selection/progress/kill evidence. Its 16 CPU scenarios retain 1,422 completed
logical calls, 1,278 physical generation slots, 1,281 attempts, 144 exact parent
replays and five uncertain attempts. Ten real controller kills cover raw
persistence, validation/staging, event-boundary and delivery commits, held Q
prose, a known timeout and two interrupted attempts without a third. These are
validation scenario totals, not coverage of the 5,752/6,280 main schedule.

The checks exercise explicit course bindings, equal-looking foreign/unbound
parent rejection, all 50 saved control shapes, serial workers with reversed
order/placement, idle ownership exclusion, overflow without truncation, and
exact valid/invalid/failed resume. Original parent records remain read-only;
branch-local queues/effects and native request arrays remain in existing records.
Backups reopen with equal scientific/progress records.

[course_native_worker_run.zip](course_native_worker_run.zip) separately retains
four prefix rounds, two B/C parent rounds, eight P_G/Q_B replay uses and all four
Q_B rounds with the local pinned 4B tokenizer. Twenty re-rendered native requests
and backup/reopen equality pass. The check uses existing auxiliary CPU tokenizer
packages with the repository SQLite environment; no weights or GPU are loaded.

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest tests.course_worker_checks -v
.venv/Scripts/python.exe -X utf8 -m tests.course_worker_archive --audit-only
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -X utf8 -m tests.course_worker_archive
```

`--write-fixture NEW_BUNDLE.zip` exclusively creates a new ordinary bundle.
Reproduction compares literal calls, requests/tokens/settings/seeds/parents,
committed transitions and attempt outcomes; observed clocks/PIDs/placement are
retained but need not be identical. Existing failure, worker and lifecycle
fixtures remain unchanged. See the
[course durability evidence](../../docs/validation/course-m3-durable-workers-and-failures.md)
for commands and execution boundaries. The later M3-T02 evidence below closes
the combined CPU lifecycle gate; these records are no pretrained-model,
GPU/runtime, pilot, freeze, main-experiment or publication acceptance.

## Course accounting and scripted lifecycle

The downstream [course outcomes/estimands archive](course_analysis_tables.json.gz)
is a derived export from this original lifecycle, not another run or an
authoritative worker store. See the [course analysis section](#course-outcomes-and-estimands)
for read-only reproduction.

[course_lifecycle_run.zip](course_lifecycle_run.zip) retains three ordinary CPU
cases with saved course population/schedules, literal selected IDs, worker
SQLite records, backup copies, progress and an offline correctness preview.
One main world per family executes all interventions, controls and repeat paths:
145 branches, 2,170 logical calls, 1,978 generations and 192 exact replays. Across
all three validation cases there are 2,332 completed logical calls, 2,124 distinct
generations, 2,126 attempts, 208 replays and two uncertain attempts. The existing
course worker bundle supplies ten independently audited real kill scenarios.

The hand case assigns 261–263 physical attempt seconds and 400 allocated
synthetic seconds, partitioned into setup 2, interruption 1, attempts 258,
uncertain work 2 and assigned idle 137. Provider billing and optional memory
remain separate. Hypothetical policies pay the original prefix and all sixteen
logical continuations, including original replay costs and F's abandoned prefix.
The stopped case retains sixteen unknown opportunities and one uncertain attempt;
release is acknowledged and resume uses the same scope/settings with one retry.

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest tests.course_accounting_checks -v
.venv/Scripts/python.exe -X utf8 -m tests.course_lifecycle_archive --audit-only
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -X utf8 -m tests.course_lifecycle_archive
```

Fresh-process reproduction compares scientific inputs, requests/tokens/settings,
seeds, raw/validation outcomes, replay identities and committed branch-local
states. Operational clocks/PIDs may differ. Backup/reopen and packaged offline
audits are exact; `--write-fixture NEW_BUNDLE.zip` rejects an existing destination.
The complete 5,752/6,280 main and 1,114/1,178 development schedules are enumerated
independently, with all missing worker slots unknown and no worker files created.
This is a tiny scripted selection and synthetic resource evidence. See the
[course accounting/lifecycle evidence](../../docs/validation/course-m3-accounting-and-lifecycle.md)
for commands, environment and the final acceptance state; actual model/runtime,
GPU throughput, historical quota, smoke/pilot, freeze and main execution remain
separate gates.

Course/M3-T02's full CPU acceptance passes 607 source/91 installed checks with
zero skips and 13 final focused accounting checks. The combined course M3 gate
is complete; course M4 owns complete cohort analysis/reporting. Actual prior
spending and remaining smoke/quota must be recovered at their later gate.

## Course outcomes and estimands

[course_analysis_tables.json.gz](course_analysis_tables.json.gz) retains seven
derived CPU validation scopes from the untouched
[course lifecycle bundle](course_lifecycle_run.zip): its three ordinary cases,
the stopped snapshot, the full intended 20-world join using the original
five-family workers, and completely unexecuted main/development joins. The
[reconstruction helper](../course_analysis_archive.py) imports no runtime,
protocol parser, provider, tokenizer or inference stack. It reads original
worker files with SQLite read-only/query-only access; backup copies are never
pooled with their originals. Independent insertion-order numeric references
and synchronous edge relaxation score literal raw replies; separate hand
formulas check AUC, final joint completion, theta and phi.

The full main join retains 6,280 slots: 2,170 recorded and 4,110 unknown, including
135 failed and 270 invalid recorded replies at zero credit. It preserves all
20 main worlds, eight receipt/Q/preserving worlds and five repeated prefixes.
Its 6,824 replicate-zero world contrasts, 1,240 repeated contrasts, 80 conditional
comparison rows and 50 trajectory pairs reproduce exactly. Five observed main
worlds do not complete the intended estimands; both intended primaries remain
unknown with fixed four-per-family denominators. Separate complete-case zeros
are descriptions of scripted fixtures. The stopped snapshot preserves sixteen
unknown opportunities, and absent main/development workers remain absent.

The intact [earlier worker bundle](course_worker_run.zip) separately reproduces
all sixteen original failure/replay/kill scopes: 1,422 recorded and 312 unknown
uses. Its controls-only ledger spans main and development inputs; those slots
are checked individually and pooling them for estimands is explicitly rejected.
The five-family lifecycle supplies the primary course contrast reconstruction.
These validation scopes supply no independent empirical worlds or model results.

```powershell
python -S -m tests.course_analysis_archive
python -S -m tests.course_analysis_archive --worker-audit
python -S -m unittest tests.test_course_analysis tests.test_course_analysis_archive -v
```

The helper exclusively creates a new derived file only when explicitly given
`--write-fixture path`; default execution compares every table with the retained
export. Raw source ZIPs, manifests, schedules, physical-response identities,
settings and seeds remain unchanged. [Acceptance evidence](../../docs/validation/course-m4-outcomes-and-estimands.md)
records commands, independent expectations and remaining course gates.

## Course diagnostics and policy costs

[course_diagnostic_cost_tables.json.gz](course_diagnostic_cost_tables.json.gz)
retains seven derived diagnostic/cost scopes from the same untouched course M3
lifecycle: three ordinary cases, the stopped snapshot, the full intended
20-world join and missing main/development joins. It contains coordinate rates,
trajectory/annotation tables, initial inventories, receipt timing and conservative
source association, actual-last-candidate transport, physical/full-policy costs
and the frozen whole C/K rule. Raw unchanged excerpts name original calls and
generations; the six existing atlas witnesses keep their stated views and
correct-summary assumptions. All data are synthetic CPU validation.

[course_diagnostics_archive.py](../course_diagnostics_archive.py) reads only
original SQLite ledgers/checkpoints, never backups alongside originals. Its
independent SQL joins, insertion/relaxation gold, coordinate eligibility,
inventories, message attempts/acquisitions, source payloads, receipt boundaries,
literal spans, transport residuals and original attempt sums check the exports.
The public checkpoint serializer decodes existing bytes without saver setup.
No protocol execution, model, runtime store or new scientific identity is used.

The full intended join retains 2,170 recorded/4,110 unknown uses, 320 prefix rows,
212 scheduled L/B peer receipt alignments, 864 receipt-information peer-call rows
and 28 revision/preserving exposure rows. Across its 58 world/event/replicate
boundary choices, 22 observed complete branches select K and 36 unobserved
boundaries remain unknown. This is not 58 independent worlds. Hand fixtures
also test constant C and incomplete selected branches without fallback. Shared
prefixes/generations are charged once physically; each deployed policy pays
its prefix and all sixteen continuation uses, including F's abandoned prefix,
original replay costs, failed and uncertain attempts. The hand cost case is
261-263 attempt-seconds and 400 synthetic allocated seconds; no model/GPU speed
is measured.

The scripted word counter must reproduce each saved input ID sequence before
history is counted. Those counts are not native tokenizer evidence. The
separate original native-worker audit retains measured request IDs and leaves
34 nonempty history counts unavailable without a matching tokenizer. Earlier
worker fault probes retain their 312 unknown uses and are audited separately.

```powershell
.venv/Scripts/python.exe -m tests.course_diagnostics_archive
.venv/Scripts/python.exe -m tests.course_diagnostics_archive --worker-audit
.venv/Scripts/python.exe -m tests.course_diagnostics_archive --native-audit
.venv/Scripts/python.exe -m unittest tests.test_course_diagnostics tests.test_course_diagnostic_archive -v
```

## Course paired uncertainty and missingness

[course_uncertainty_tables.json.gz](course_uncertainty_tables.json.gz) retains
seven derived scopes from the unchanged course lifecycle workers: complete
selected records, hand costs, resumed/stopped work, full intended 20-world joins
and wholly unexecuted main/development populations. These are exploratory CPU
validation tables, not model results. The saved resampling seed is `20261011`,
with 10,000 within-family world draws and type-7 97.5% primary/95% secondary
intervals. Four main worlds per family, eight-world focal/preserving cohorts
and five conditional repeated prefixes keep their original IDs.

The full intended join retains 2,170 recorded/4,110 unknown uses. Its theta/phi
sensitivity is [-1.5,1.5]/[-0.75,0.75]; intended statistical intervals remain
unavailable, while five-world complete-case zeros are separately descriptive.
Raw contrasts, family means, paired coverage, completion bounds, trajectories
and whole-policy quality/preservation/cost displays remain explicit.

[course_uncertainty_archive.py](../course_uncertainty_archive.py) rejoins the
original SQLite snapshots read-only and checks unchanged accepted outcome/cost
tables. Independent exact rational coefficients verify 11,422 eligible linear
rows across the seven scopes, with original generation IDs combined before
extrema. Missing logical uses are never fabricated from recorded parents.
Unknown eligibility and future costs retain conditional/conservative or
unbounded labels. Tiny nonlinear enumeration and independent draws/binomial
references are in [course formula tests](../test_course_uncertainty.py).

```powershell
.venv/Scripts/python.exe -m tests.course_uncertainty_archive
.venv/Scripts/python.exe -m unittest tests.test_course_uncertainty tests.test_course_uncertainty_archive -v
```

See [course acceptance](../../docs/validation/course-m4-uncertainty-and-missingness.md).
At that uncertainty checkpoint, the complete course report gate remained separate;
the following report acceptance records its subsequent evidence.

## Course synthetic reports and CPU gate

[course_report_tables.json.gz](course_report_tables.json.gz) retains eight
reports from the unchanged [course lifecycle](course_lifecycle_run.zip): seven
accepted prerequisite scopes plus an explicitly synthetic terminal-feasibility
example. Every report/table/case/plotting input and ordinary HTML/JSON/CSV/gzip
export is reproduced twice by [course_report_archive.py](../course_report_archive.py).
Outcome/estimand, diagnostic/cost and uncertainty joins match the accepted
prerequisite archives exactly; original workers are read-only and missing ones
remain absent. Seed `20261011` and accounting clock
`2026-10-11T23:59:59+00:00` are explicit derived-analysis inputs, not a main freeze.

[course_scripted_reports.zip](course_scripted_reports.zip) holds five portable
reports: a complete selected scope, incomplete 20-world main, safely stopped
prefix, unexecuted development and synthetic terminal-feasibility report.
Each has seven SVG/PNG exhibit pairs, all scientific tables, supporting world
contrasts/intervals, exact trace strings and ID-linked case cards. Open its
`INDEX.md` and each `report.html` locally. All 35 pairs are rendered deterministically
with the recorded plotting environment and reopened from clean CPU scratch.

Complete means all slots in the supplied synthetic scope are recorded, including
failures; it does not mean empirical completion of the 20-world course study.
Full intended main keeps 2,170 recorded/4,110 unknown uses; theta/phi sensitivity
remains [-1.5,1.5]/[-0.75,0.75]. Intended intervals are unavailable and five-world
complete-case zeros descriptive. The terminal example is not an actual GPU/model
failure: all 6,280 main uses remain unknown, with freeze/model/headroom unavailable.
Replicate zero determines primary displays/cases; five conditional repeats add
no independent worlds. Four-per-family/eight-world focal precision stays exploratory.

The original scripted word counter supplies explicitly synthetic history counts.
CLI consumers without a matching tokenizer retain unavailable nonempty counts;
no native Qwen token measurement is invented. Direct report/assembly APIs pass
`regime="course"`; the CLI uses the manifest's regime/count automatically. The
report regime must match its accepted uncertainty population scope.

```powershell
.venv/Scripts/python.exe -m tests.course_report_archive
.venv/Scripts/python.exe -m tests.course_report_archive --export NEW_REPORT_DIRECTORY --figures
.venv/Scripts/python.exe -m unittest tests.test_course_report tests.test_course_report_archive -v
```

To attach a documented terminal gate failure verbatim, use existing saved course
inputs/workers, an explicit accounting clock/seed and a fresh export destination:

```powershell
.venv/Scripts/python.exe -m recovery analyze --report --manifest tests/fixtures/population_course.json --schedule tests/fixtures/schedules_course.json --worker PATH_TO_ORIGINAL_WORKER --output NEW_REPORT_DIRECTORY --as-of 2026-10-11T23:59:59+00:00 --resampling-seed 20261011 --terminal-feasibility PATH_TO_DOCUMENTED_FAILURE
```

That option labels supplied evidence without changing coverage, treating unknowns
as negative results or passing a gate. Preparing fresh inputs still requires
`--regime course --config configs/course-inputs.toml`; report analysis does not
resample them. [Course report/CPU acceptance](../../docs/validation/course-m4-report-and-cpu-gate.md#completion-and-handoff)
passes 52 source/52 installed methods and 33 dependency-free methods with zero skips.
Model/runtime, resources, smoke/capability/pilot, accepted freeze, main execution
and external delivery remain separate.

Default execution compares the retained tables; `--write-fixture NEW_PATH`
exclusively creates a new derived export. [Course acceptance evidence](../../docs/validation/course-m4-diagnostics-and-policy-costs.md)
owns its executed diagnostic results; the report acceptance above records the
combined CPU gate and remaining model/GPU gates. No empirical course population, runtime freeze or execution
authorization is established by these fixtures.


## Course native inference suffixes

[course_inference_suffixes.json](course_inference_suffixes.json) contains seven
constructed pinned-native 4B suffix fixtures under the adopted 256-token cap.
Internal markers and unexpected EOS remain literal; only one verified final
im_end is removed for parsing. Complete JSON at the cap is valid, while
malformed cap endings remain invalid. These are CPU parser/config/cache checks,
with no model inference. Reproduce with `python -m tests.tokenizer_course_inference
--tokenizer LOCAL_4B_METADATA`. See [course preparation evidence](../../docs/validation/course-m5-inference-and-smoke-preparation.md).
