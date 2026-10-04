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
