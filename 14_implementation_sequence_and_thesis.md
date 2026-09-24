# Implementation sequence, execution plan, and thesis artifacts

## Build in this order

| Milestone | Implement exactly | Completion check |
|---|---|---|
| 1. Formal executable fixtures| Use the delivered support algebra; implement a four-way fixture for each primary family and an independent exact action grader. Start with the THRESHOLD example.| q survives only in alternative worlds; old bound-X action never survives X's loss; control job unaffected.|
| 2. Event reducer and owned state| Append-only evidence/claim/action/disposition events; one owner per writable slot; explicit epoch acknowledgment.| Invalid writes rejected atomically; raw history preserved; new action arguments create a new record.|
| 3. Mock team and transport| A→B→C scripted prefix; source capsules independent of reports; both jobs proposed.| All required evidence reaches C; no action executes before the cut.|
| 4. Checkpoint and branch| Canonical full snapshot, content hashes, copy-on-write suffixes, crash-safe persistence.| Parent unchanged after divergent branches; queues/effects/seeds restored; interrupted writes resume once.|
| 5. Policies and oracle adapters| N, R, E plus O/OC/ON/OR and the common recovery executor.| Masks match hand-worked examples; O does not generate replacements; unsafe fresh actions remain measurable.|
| 6. One local model worker| Transformers FP16 Qwen3-4B, non-thinking template, agent/extractor prompts, strict parser, timing/tokens/cache. Implement the minimal extraction adapter needed by the pilot.| The first eight probes already counted in the 152-call pilot serve as smoke prompts; no extra unbudgeted serving calls or retries for wrong output.|
| 7. Minimum real pilot| 152 calls on 2 disjoint base worlds as specified in 12.| Evidence, local capability and hardware costs support continuing. Stop here if the phenomenon cannot be isolated.|
| 8. SILO adapter and generated worlds| Attributed I-04/I-01 generators with local RNG, four items per shard, deterministic twin/correction construction.| Native calibration unchanged; modified task semantics and structural invariants verified across 1,000 CPU worlds.|
| 9. Batch extraction and process scoring| Extend the pilot extraction adapter to all generated worlds; separate syntactic errors from semantic support errors; implement all process metrics.| Correct/incorrect handoffs yield distinguishable labels; no future correction or gold fields enter prompt.|
| 10. Transfer compiler and numeric grader| MasDrift-derived quote/budget workflow, finite-domain support enumeration, exact routing/amount checks.| Boundary fixtures and independent numeric truth checks pass before transfer inference.|
| 11. Expanded pilot and novelty resolution| 476 primary calls total, up to 16 second-model probes, exact/full-text prior-work audit, forecast and precision simulations.| All pilot gates pass or documented pivot/abandon decision; admitted A/B matrix.|
| 12. Manifest and analysis freeze| Generate IDs/seeds/subsets/arms; bind source/model/environment/prompt hashes; implement tables and contrasts on synthetic outcomes.| 6,400 or 6,080 calls exactly; analysis produces correct known simulated contrasts; preregistration saved.|
| 13. Main experiments| Run paired blocks with allocation metering, durable checkpoints and operational stop rules.| No silent omissions or changed prompts; all expected branch outcomes or documented failures exist.|
| 14. Explanation and reporting| Run registered analyses, inspect predeclared failure samples, write results and limits.| Every plot/table traces to raw events; negative results retained; no claim outruns the tested regime.|

Substantial implementation is justified only after Milestone 7 shows the local tasks and correction protocol are viable. This sequencing avoids spending the thesis building an instrument whose scientific construct cannot be measured.

## Expected command-line interface to implement

```bash
python -m recovery_study.cli validate-config configs/experiment.json
python -m recovery_study.cli generate --split pilot --manifest artifacts/pilot/manifest.json
python -m recovery_study.cli verify-oracles --manifest artifacts/pilot/manifest.json
python -m recovery_study.cli run-pilot --stage minimal --gpu-ids 0,1
python -m recovery_study.cli forecast --pilot artifacts/pilot --matrix configs/experiment.json
python -m recovery_study.cli freeze --matrix A --output artifacts/recovery_v1/registry
python -m recovery_study.cli run --manifest artifacts/recovery_v1/registry/manifest.json --gpu-ids 0,1
python -m recovery_study.cli resume --experiment artifacts/recovery_v1
python -m recovery_study.cli evaluate --experiment artifacts/recovery_v1
python -m recovery_study.cli analyze --experiment artifacts/recovery_v1
python -m recovery_study.cli audit-release --experiment artifacts/recovery_v1
```

These commands define the future interface; `recovery_study` is not delivered as a completed runtime. The runnable commands supplied now are:

```bash
python -m unittest discover -s tests -v
python -m reference.export_contracts
python -m reference.budget
```

Run them from the extracted blueprint directory with Python 3.11+ and Pydantic v2. The symbolic reference was executed on the available CPU runtime; GPU compatibility remains a pilot obligation.

## Preregistration checklist

Fix generator version/domains/seeds, matched-factor construction, diagnostic subset hashes, policy algorithms, model/quantization/backend, all prompts/parsing rules, caps, pilot exclusion, A/B matrix, primary contrast/endpoint, failure handling, infrastructure sensitivity analysis, bootstrap and multiplicity rules, and the rule for stopping on budget/invariants. Include the close-work novelty paragraph and the explicit benchmark-transformation statement. The preregistration is a research artifact; no public posting or messaging is required to begin implementation.

## Thesis chapters

1. **Problem and contribution:** what can stay true while an action becomes invalid; why independent state/ownership makes repair consequential.
2. **Prior knowledge and novelty boundary:** truth maintenance, provenance and distributed snapshots; recent memory/workflow recovery; assumptions the experiment tests.
3. **Formalization and hypotheses:** evidence versions, available support, minimal justifications, concrete action bindings and primary estimand.
4. **Experimental instrument:** SILO extension, three-agent protocol, checkpoints, policies, schemas and exact graders; keep framework details subordinate to identification.
5. **Pilot and protocol:** capability, compute, measurement validity, preregistration, statistical power and resulting design choices.
6. **Results:** primary interaction, support errors, O/OC/ON/OR diagnosis, baselines and resource accounting.
7. **Generality and limitations:** small transfer/model/seed checks, failed hypotheses, unresolved alternatives and structural applicability.
8. **Conclusions and future work:** what evidence supports about preserving conclusions and revising execution, without inflating the scope.

Appendices: schema/API reference; prompt templates; formal evaluator validation; experiment manifest; complete result tables; failure-case audit; license/provenance register.

## Research artifacts to release

- Attributed task adapter and reproducible world generator, with exact source commits and licenses.
- Symbolic and numeric support/action evaluators with independent conformance tests.
- Minimal event-sourced runner, frozen-prefix replay, policies and local model adapter.
- Preregistration, dependency/model locks, seeds, split/subset manifests and hardware measurement.
- Raw prompts, outputs, event logs, checkpoints, support estimates and labels; exclude secrets and model weights where redistribution is inappropriate.
- Analysis scripts, per-world tables, bootstrap outputs and standalone PDF/SVG figures.
- Negative results and protocol/infrastructure failure records, including failed pilot variants in a separate development partition.
- A concise artifact README that regenerates the principal figures from saved outcomes without GPU inference.

## Next research program if the initial result is interesting

The natural extension is not a larger generic framework. It is a controlled change in one assumption: privately held alternative evidence, asynchronous correction delivery, independently owned agents that cannot expose full state, repeated corrections, action compensation, or an explicit budget for richer provenance. Each adds a new identification problem. First establish whether action-specific support and recipient-state replacement explain behavior in the bounded synchronous setting.

## Final recommendation

Pursue **an empirical study of the adequacy of support representation for preserving conclusions while repairing witness-bound actions**. Use a SILO-derived generator extension, a small transparent runner, exact evaluators, natural estimated support, and paired interventions. Start with the CPU counterexample and 152-call pilot. The thesis should be judged by whether it distinguishes representation failure from state-repair failure, not by whether its selective policy has the highest average score.
