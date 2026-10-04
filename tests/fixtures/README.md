# SILO reference fixtures

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
