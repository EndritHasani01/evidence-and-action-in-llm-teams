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
python -S -m recovery validate --manifest population.json --authoritative tests/fixtures/population_target.json
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
python -S -m recovery validate --manifest tests/fixtures/population_target.json --schedule schedules.json --authoritative tests/fixtures/population_target.json
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
rewrite of archived reasoning. No optional library is imported by the default
CPU validation suite.

Provenance: Qwen3.5-9B revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`,
Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0,
on Windows / CPython 3.11.9. Local tokenizer JSON, tokenizer configuration and
template were compared byte for byte with this immutable upstream revision.
The package/revision information is offline fixture provenance, never peer data
or an accepted M5 inference freeze.

| Scripted case | Input tokens | Reserved output |
|---|---:|---:|
| Ordinary receipt | 1,830 | 384 |
| Disclosed receipt | 1,826 | 384 |
| Compact wrong result | 1,667 | 384 |
| Compact absence | 1,604 | 384 |
| Pending edge | 757 | 384 |
| Known tombstone | 801 | 384 |
| Retained valid reply | 1,578 | 384 |

These measurements establish short-case behavior only. Complete worst retained
contexts, legal reply/message capacity and attainability remain M2-T06. The
renderer rejects overflow instead of shortening retained work.

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
