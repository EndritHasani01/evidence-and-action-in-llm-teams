# Repository reuse, task truth, and protocol validation

Investigation date: **2026-10-04**. Authority: [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md), especially §§2–3, 5.1, 7.1–7.2, 8.2, and 9. Inspected root commit `16412a5bf5ea91d865f4c183191eb534fb978914`; specification SHA-256 `049ff2b44bba185776423c4278bef890c2e55a27330513cb99757ac980a3ced1`.

This investigation inspected current source and performed small CPU checks. It did not build the recovery experiment, generate its manifest, run inference, rerun archive scripts that overwrite evidence, or validate the future implementation.

## What the repository can contribute

The checkout contains evidence and reference material, not an existing recovery runner to extend. The [research archive rules](../../research/AGENTS.md) and [reading order](../../research/README.md) were followed; the [SILO audit](../../research/07_repository_audit/SILO_REPOSITORY_AUDIT.md) and [protocol audit](../../research/04_design_extensions/evidence/PROTOCOL_AUDIT.md) informed targeted source checks.

| Component | Evidence from current checkout | Decision for later planning |
|---|---|---|
| Native task mathematics | [I-09](../../acl26-silo-bench/benchmark_generator/paradigm_i.py), [II-11/II-17](../../acl26-silo-bench/benchmark_generator/paradigm_ii.py), [III-21/III-24](../../acl26-silo-bench/benchmark_generator/paradigm_iii.py) implement the required mathematical families. | Reuse definitions, attribution, and selected cases as regression fixtures. Implement small explicit solvers for the final contracts. |
| Native generators | Each module calls global `random.seed(42)` on import. Native sizes/ranges differ; BFS samples a different graph distribution. | Do not import generators into the experiment or adapt their global RNG lifecycle. New generators must follow §2 directly with independent saved streams. |
| Native runner and communication | [engine.py](../../acl26-silo-bench/src/engine.py) skips submitted peers; [msg/tools.py](../../acl26-silo-bench/src/msg/tools.py) mutates earlier message files when marking them read. | Replace execution semantics. Existing directories cannot serve as isolated sibling snapshots. |
| Native parser/inference adapter | [parsing.py](../../acl26-silo-bench/src/utils/parsing.py) extracts XML fragments and coerces values; [llm.py](../../acl26-silo-bench/src/utils/llm.py) retries indefinitely with a one-hour API timeout and no output cap. | Neither satisfies the strict reply or bounded-attempt contract. Do not wrap these functions into the new protocol. |
| Native scoring | [metrics.py](../../acl26-silo-bench/src/utils/metrics.py) normalizes values and relies on ordinary Python equality; its Sort partial scorer maps values to one position. | Use new exact and coordinate scoring after protocol validation. No normalization, tolerance, set comparison, or generic LIS scoring. |
| Archived mathematical probes | [protocol_probe.py](../../research/04_design_extensions/evidence/protocol_probe.py) and [audit_repository.py](../../research/03_innovation_review/evidence/audit_repository.py) contain useful independent computations and constructed ambiguity examples. | Reuse the lessons and small fixtures. Do not import entire audit scripts into runtime: some helpers hardcode eight-record shards or twelve nodes, and scripts write adjacent historical results. |
| Original blueprint | [contracts.py](../../research/01_original_blueprint/reference/contracts.py), [support.py](../../research/01_original_blueprint/reference/support.py), schemas, configs, tests, and requirements describe claims/actions/support extraction and a different matrix. | Preserve as history; they are not a starter architecture or a validation suite for this experiment. |
| Vendor packaging | [pyproject.toml](../../acl26-silo-bench/pyproject.toml) requires Python ≥3.13; the current specification uses 3.11. | Keep the vendor checkout as source/data evidence, without installing its package or inheriting its dependencies. |

The vendor [LICENSE](../../acl26-silo-bench/LICENSE) is Unlicense while its package metadata says MIT. Record the supplied file and resolve attribution metadata before redistribution; this does not require additional runtime architecture. The root commit identifies the inspected vendored content, not an independently verified upstream commit.

## Task generation contains the meaningful hidden risks

All five oracles are small integer computations. The risk is preserving the specified **population, ownership, edit selection, and coordinate contract**, rather than choosing a solver library. A graph dependency is unnecessary for twelve nodes; a queue traversal and an independent relaxation reference are sufficient.

| Family | Contract detail that must survive implementation | Important adversarial checks |
|---|---|---|
| Top-K | Descending ten values, including duplicates; change a unique value strictly above the old tenth-value cutoff to a value strictly below it. | Repeated cutoff values; reserve previously outside top ten; zero cutoff; uniqueness of the edited value; changed and preserved targets. |
| Prefix | Source shards and output segments are contiguous; peer output uses global positions, not a fresh local cumulative sum. | Edit at position 0, at the final position, and across each shard boundary; positive and negative deltas; unchanged earlier coordinates. |
| Difference | Full output has `n−1` coordinates labeled `d_1…d_(n−1)`; Python list position for `d_j` is `j−1`. | Endpoints change one coordinate; interior edits change two with opposite signs; shard boundaries; negative differences. |
| Sort | Source ownership is randomized independently of values; output ownership is fixed global rank segments. | Equal values, replacement crossing several segments, retained local segment missing a remote boundary value, and source identity distinct from rank. |
| BFS | Uniform labeled Prüfer tree plus five uniformly selected nonedges, then equal random edge partition. Main deletion changes distances; preserving deletion does not. | Canonical undirected edges, alternatives, isolated nodes after deletion, `−1` conversion, source-node distance, owner eligibility, and empty/nonempty changed-coordinate sets. |

The following generation decisions are sufficiently resolved by §2; they should not become configurable experimental options:

- Fix owner-block order before generating worlds. Rejection conditioning is against that owner, not a search for a more convenient owner after seeing a graph or array. The nested first-eight fallback retains balanced owner counts.
- Top-K/BFS eligibility is checked using mathematics before model output. Count all failed generation attempts and stop explicitly at 1,000; never replace worlds because the prefix fails.
- For preserving Top-K edits, sample uniformly over legal **record/replacement pairs**. Choosing a record uniformly and then one of its legal replacements can change pair weights. Main Top-K selection instead follows its expressly specified record-then-replacement rule. BFS preserving edits are uniform over legal removable edges.
- Assign record identities independently of hidden values or endpoints. Public numeric positions may appear in IDs; BFS IDs must not encode endpoints or an endpoint-sorted rank. Preserve the same ID through a tombstone.
- Apply the main and preserving events separately to the original world/prefix. The preserving event is not applied after the main edit.
- Save raw inputs, ownership, selected edits, rejection counts, and streams. Seed-only regeneration is insufficient evidence if algorithms or package versions change.
- The fallback changes BFS from sixteen edges/four per peer to twelve edges/**three per peer**, while retaining five extra graph edges; it changes every relevant output contract. Avoid dimensions inferred from a native case name or an archived hardcoded slice.

No new generator was written in this investigation. Its eligibility rates, sampled distributions, and final manifest remain implementation checks, rather than measured findings here.

## Strict parsing needs two small layers

Pydantic 2 is useful for declared fields and exact types, but its JSON entry point alone does not satisfy the duplicate-key rule. Python's decoder also defaults to accepting nonfinite constants and repeated keys. The [Python JSON documentation](https://docs.python.org/3.11/library/json.html#standard-compliance-and-interoperability) describes these extensions and the decoding hooks; [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) and [extra-field configuration](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra) supply the schema layer.

Use full-document JSON decoding with a recursive `object_pairs_hook` that rejects repeated keys and `parse_constant` that rejects `NaN`/`Infinity`, followed by strict Pydantic validation with `extra="forbid"` at every nested reply/message/reference level. Require a top-level object. Integer fields must reject booleans, floats, and numeric strings. Candidate lengths and BFS's exact canonical decimal-string key set require task-specific checks; default JSON Schema generation does not establish those runtime checks.

A numeric token such as `1e999` can become infinity without invoking `parse_constant`. The integer-only candidate/reference/recipient schemas reject it; an explicit finite-number check is appropriate if any future protocol field admits floats. Do not introduce permissive numeric fields into this interface merely for convenience.

Schema checks alone cannot establish that a sender holds the current source version, that a recipient is another peer, that there is at most one message per recipient and at most eight distinct references per recipient, or that prose fits tokenizer limits. Validate these against the immutable start-of-round peer view. The distinct-reference limit is not an additional prohibition on repeated valid references; delivery accounting must distinguish repeated attempts from unique acquisition. On any violation, reject **the complete reply**, including all deliveries and its candidate. A wrong integer answer of the proper shape is a valid protocol reply and receives ordinary incorrect-answer scoring.

Validation feedback should use bounded public error codes/locations. Do not render `str(ValidationError)` or dump `.errors()` into history: their default output can contain supplied values, and permission errors must not reveal hidden payloads or correctness. Preserve the unmodified raw reply offline. The 32-token feedback cap does not authorize truncating own replies or received history to fit context.

No fragment extraction, JSON repair, schema-constrained generation, candidate sorting, previous-candidate backfill, extra retry, or correctness feedback is justified by this investigation. These would alter observed failure or recovery behavior.

## Executed CPU evidence

On 2026-10-04, a temporary standard-library/Pydantic probe ran on **Python 3.11.9 / Pydantic 2.12.5**. It loaded native `metrics.py` with bytecode disabled, recomputed selected stored tasks, and deleted its temporary script. No archived evidence JSON was overwritten. These observed versions are local probe versions, **not an accepted inference environment lock**.

| Probe | Executed result | Consequence |
|---|---|---|
| Strict Pydantic JSON with `{"candidate":[1],"candidate":[2],"send":[]}` | Accepted; last candidate `[2]` survived. | Duplicate detection must occur before ordinary mapping/schema validation. |
| Strict integer candidate containing `true`, `1.0`, or `"1"` | All rejected with `int_type`. | Strict schemas can enforce the required integer distinction. |
| Outer extra field; code fence; trailing prose | Rejected with `extra_forbidden` or `json_invalid`. | Reject complete documents rather than extracting a candidate fragment. |
| Recursive stdlib duplicate hook on `{"x":{"a":1,"a":2}}`; rejecting constant hook on `NaN` | Both rejected. | Hooks cover nested objects and explicit nonfinite constants. |
| Same stdlib hooks on `{"x":1e999}` | Accepted as `{'x': inf}`. | The subsequent type/finite validation layer is still necessary. |
| Whitespace surrounding a complete JSON object | Accepted. | Whitespace need not be stripped or treated as a violation. |
| Native exact scoring of `[True]` or `[1.0]` against `[1]` | Both scored 1.0. | Native equality is not protocol validation. |
| Native Level III partial scoring of exact `[1,1,2]` against `[1,1,2]` | Scored 2/3. | Duplicate-aware ordered-coordinate scoring must be independent. |
| All stored cases for I-09, II-11, II-17, III-21, III-24 | **30/30** independently recomputed answers matched stored gold. | Selected native mathematics/data are useful fixtures; this does not validate new generators or recovery execution. |

The thirty cases cover six native agent counts per family. Independent checks used incremental insertion for Top-K, direct prefix sums, adjacent subtraction, explicit sorted segmentation, and repeated synchronous edge relaxation for BFS, with unreachable `−1`. Comparison preserved list order/multiplicity and canonicalized BFS node keys. This was a truth check of existing data, not a reproduction of SILO's model results.

Source SHA-256 values at inspection: `metrics.py` = `172b88fc8ea6aa4c2f36cb4f701b9d57ec666585f1f5beb2efd0e6b898f76d72`; `paradigm_i.py` = `16533b6fbf1495f674a5042b3f093d519280fddaca6f34ebd052543c1845317f`; `paradigm_ii.py` = `87ac7b613f54adb95fd53cb5ea89a426736dedbbe055983ae486e8d26cf66dcf`; `paradigm_iii.py` = `5958f854d79cc499d0d0e27a40e0fcc726ea7667132113ce231ffecc81bbae0e`. The selected-data digest is `e7d2f07bf1df4ea5e17133dd887b823e1ad9a2d57704515affb572b89201db33`, computed by SHA-256 over filename-sorted concatenations of each filename's UTF-8 bytes, a NUL separator, and that file's binary SHA-256 digest.

## Keep evaluator information outside peer state

Use a narrow rendering input containing public task metadata, the peer's permitted current records, revision notice/assigned receipt, and allowed derived state. Keep full-world gold, changed-output masks, subset labels, branch names, and future edits in evaluator/schedule records. A broad world object passed to the renderer makes leakage easier to introduce accidentally.

Authenticated source forwarding copies only a sender-held **current** `(ID, version)` payload; it does not fetch an unseen requested source or trust model text as a source table. The revision notice invalidates v1 everywhere before the continuation. An unreceived v2 stays update-pending. A received tombstone is a known current record but never an active graph edge. Historical receipt values stay outside current lookup/forwarding; old values appearing in retained prose remain ordinary derived history.

Old gold and actual candidates serve different purposes. K preserves exactly the valid fourth-prefix-round candidate, even if wrong; invalid round four gives absence. Offline Prefix/Difference transport references operate on that actual candidate, not an oracle-repaired candidate. Coordinate diagnostics use global positions/ranks/nodes; replicated answers create peer-copy counts without new independent coordinates. Updating sources never rewrites a candidate.

The attainability witness in §8.2 can use a three-round rotating shard exchange followed by local computation: each peer then knows every required raw record before its fourth call. Its oracle must see only that scripted peer's acquired view. Counting mathematical reachability alone does not prove serialized references, candidate shapes, history, notices, and receipts fit token caps. The later witness must exercise local/broadcast delivery, resets, and delayed prose with actual tokenization.

## Remaining validation gates and bounded uncertainty

Before GPU use, the important checks are generator invariants and independent-oracle agreement; strict parser adversaries; absence of evaluator leakage; lawful forwarding and version invalidation; exact candidate preservation/absence; coordinate-index mapping; and a tiny scripted run through every state transformation. Use examples/property checks that target these semantic risks, rather than adapting the old test suite or pursuing coverage as an independent objective.

Particular fixtures should include duplicate JSON keys inside references, a valid candidate attached to one invalid message, stale/unheld references, wrong BFS key spellings such as `"01"`, complete JSON finishing at the generation cap, incomplete JSON below or at it, empty diagnostic denominators, and invalid final-prefix candidates. Failure classification must not depend on whether a plausible embedded answer happened to be right.

The choice of class names, small solver function signatures, and opaque ID format can remain flexible. The admission/selection rules, strictness, coordinate mapping, renderer visibility boundary, and distinction between raw sources and derived text are settled requirements. Further general-purpose schema frameworks, source provenance graphs, semantic dependency extractors, graph databases, and generic task-plugin systems would not resolve a present uncertainty.

## Analysis and allocation: defaults that would change the result

Sections 5–7 require no new statistical framework. Keep an explicit scheduled-slot status and join outcomes to the frozen world/branch/peer/round manifest; absence from a table must not silently become zero or disappear from denominators. Protocol-invalid, timed-out, and exhausted attempted slots score zero. Unexecuted slots remain unknown. Replicate zero supplies the main results; the ten extra continuations remain paired conditional repeatability diagnostics.

The natural analysis object is one complete world's sibling outcomes, not sixteen independent peer-round observations. Compute exact-peer AUC over four peers and four recovery rounds. Compute retained-group effects over rounds 2–4, with the same focal peers under B and the relevant complementary mask. A shared revision/sham effect is still primary φ; its subtraction belongs to φ_corr. Coordinate diagnostics average eligible peers, then worlds, then families; an empty preservation/repair denominator is unavailable, not zero. Fragmented trajectories must not be turned into an oracle-selected joint answer.

[SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) defaults to BCa, 9,999 resamples, 95% intervals, and unpaired samples. Those defaults contradict the prescribed method. The simplest faithful implementation draws 10,000 world-index arrays separately within each eligible family, carries all siblings together, computes equal-family means, and takes the specified percentiles. Pooling all families or separately bootstrapping policies changes the design. Save resampling seeds and the quantile convention. Primary intervals use 1.25/98.75 percentiles; secondary intervals use 2.5/97.5. Add the specified weighted Hoeffding companion when within-family contrasts are constant. Use [SciPy's exact binomial interval](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) for the relevant within-family completion counts; no additional hypothesis-test catalogue is needed.

For reproducible random streams, [NumPy SeedSequence](https://numpy.org/doc/stable/reference/random/parallel.html) supports fixed identifiers as well as spawning. Allocate identities/seeds before scheduling so rejection attempts, device order, or a resume cannot shift another world's streams. Do not add policy/event identifiers to matched continuation seed identities. Distinct physical generation IDs still separate newly sampled replies with equal seeds; required first-round sharing uses explicit parent IDs.

Missingness bounds must preserve shared response identity. For linear accuracy contrasts, combine coefficients of the same unknown physical response before assigning its possible 0/1 correctness; independently bounding its logical copies can invent impossible outcomes. Nonlinear joint/trajectory endpoints need shared-variable completions or conservative explicitly labeled bounds. World contrasts alone cannot reconstruct this relation, so retain the logical-call-to-generation-parent join. Do not add a general optimization engine before an actual incomplete schedule warrants it.

### New isolated accounting/statistics checks

Executed with **Python 3.11.9, NumPy 2.4.2, SciPy 1.17.1**, using synthetic arrays and an in-memory enumeration of family/world/branch counts. No experiment world, production scheduler, or results dataset was created.

| Check | Observed result |
|---|---|
| Independent per-world schedule enumeration | 60 worlds: **16,152 new / 17,656 logical** calls; 40 worlds: **11,504 new / 12,560 logical**. Mixed/Q first rounds count as four logical uses and zero new generations. |
| Pilot component arithmetic | `730 + 96 + 96 + 96 + 96 = 1,114`; separate smoke maximum adds 24, giving **1,138**. Initial capability slots = **90**. |
| Identical paired arrays, percentile bootstrap | Correct paired contrast CI `[0,0]`; default unpaired resampling gave approximately `[-3.167,3.167]` on the synthetic values. This is a library-behavior example, not an experimental effect. |
| Five constant family contrasts with unequal family means | All 10,000 stratified estimates were `0.125`; the primary percentile interval collapsed to `[0.125,0.125]` despite different family means. The degeneracy rule must inspect within-family variation. |
| Prescribed θ Hoeffding width under equal family counts | Half-width **0.7644** at N=60 and **0.9362** at N=40, before intersection with `[-2,2]`. Zero bootstrap spread does not justify certainty. |
| Four rotating incorrect peers | Exact-peer AUC **0.75**, every peer correct at least once, joint correctness never attained: fragmented. |
| Teammate effect +0.25 under both events | Primary φ **+0.25**, φ_corr **0**. Treating φ_corr as primary would lose the specified operational effect. |
| One unknown response with coefficients +1 and −1 | Shared completion bound `[0,0]`; incorrectly independent copies yield `[-1,1]`. |
| 12/12 synthetic joint completions | Exact two-sided 95% binomial interval approximately `[0.73535,1]`. Counts remain necessary even at a ceiling. |

Compact reproduction of the accounting result (independent enumeration above also checked the individual branches):

```python
for N in (60, 40):
    q = 2 * N // 5
    new = 16*N + 80*N + 48*N + 48*N + 2*N
    new += 16*3*16 + 48*q + 48*q + 10*(6*16 + 4*12)
    logical = new + 16*N + 16*q + 160
    print(N, new, logical)
# 60 16152 17656
# 40 11504 12560
```

The 100-hour ceiling includes allocations and idle overhead. With the full twelve-hour reserve and 25% main margin, `88*3600/(1.25*new)` yields **15.69 / 22.03 allocated seconds per new generation** for target/fallback. These are break-even arithmetic, not measured T4 speed. Replay savings belong to the physical ledger; hypothetical policy costs still include the shared prefix and all sixteen continuation calls, with replay uses attributed their original generation costs (§7.3).

### Historical mathematical checks reverified without overwriting evidence

Root imported [protocol_probe.py](../../research/04_design_extensions/evidence/protocol_probe.py) and called only its side-effect-free `delta_transport_checks()`, `graph_pair()`, and scripted Prefix/Sort `aggregate_only_history_pair(...)` functions. All **8,748** delta-identity cases and the ambiguity/receipt-sufficiency assertions passed. Source SHA-256 was `a572825649dc7bc44686a694ee39ca1906bec45f2243b740bc85f6e950ffa66e`. These functions assume their particular views and hardcode target dimensions; they neither test the fallback renderer nor estimate naturally occurring failure. The archived output-writing `main()` was not called.

The remaining analysis checks are small synthetic fixtures for θ's correction-specific null/sign, φ's cross-group null/sign, coordinate eligibility and collateral errors, incomplete coverage, repeated identities, and the frozen C-or-K descriptive boundary rule. They belong to implementation validation, rather than additional statistical research or outcome-driven analysis design.
