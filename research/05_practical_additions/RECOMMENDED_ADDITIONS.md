# Recommended additions: more explanatory depth, one simple extra policy

**Recommendation: keep the original experiment, build three compact analysis sections from its existing records, and add one compact-state recovery policy if the measured budget permits.** Do not implement this folder as a checklist.

The thesis should answer a connected set of questions: **what fails after a correction, why recovery differs across distributed tasks, and how much previous state is worth keeping?** That is a richer and more useful story than an overall B/C/L/F ranking. It does not require a new framework or literature-priority claim.

This assessment follows the user's new objective. The previous v2 receipt experiment is no longer the default. **Compact-state recovery is now the preferred optional experiment** because it is easy to explain, useful to a runtime, applicable to all six tasks, and cheap to implement. Its being a familiar idea is not a reason to reject it.

All proposals are plans for the unexecuted PS study. No measured recovery advantage, GPU speed or run coverage is claimed.

## The smallest recommended combination

### A. Explain the recovery process

Combine [trajectories](01_RECOVERY_TRAJECTORIES.md), [observable failure labels and casebook](02_FAILURE_TAXONOMY.md), and the small [team-synchronization panel](15_TEAM_SYNCHRONIZATION.md).

**Deliverable:** one recovery-curve figure with clear uncertainty; a small table distinguishing immediate, delayed, transient and absent joint recovery; and three to six short paired trace cards. Include old-value persistence, collateral errors and protocol failures. The synchronization panel distinguishes every peer being correct at some time from the team being correct together.

Most raw metrics are already required by the PS. The added substance is the joined analysis, explicit taxonomy and reproducible case selection. Describe what traces establish; do not assign hidden psychological causes to every error. A mixed or null experiment can still produce an informative failure account.

**Extra inference: 0.** Use one shared outcome/trace table, not three analysis systems.

### B. Explain why tasks and information states differ

Combine [task structure](05_TASK_STRUCTURE_AND_RECOVERY.md), a short [recovery-information atlas](06_RECOVERY_INFORMATION_ATLAS.md), and only the minimal delivery/evidence portion of [communication analysis](03_COMMUNICATION_AND_INFORMATION_FLOW.md).

**Deliverable:** one six-task explanatory table and two small diagnostics: correction availability versus correct response, and retained/reacquired evidence versus C–F recovery. Relate output locality, output ownership and missing alternatives to the observed traces. Use the existing exact before/after oracles offline.

This gives the six task families a scientific purpose beyond benchmark breadth. For example, changing one maximum may require an omitted alternative, whereas changing many prefix coordinates can be algebraically simple if the historical operand remains available. A full correct difference vector plus one unchanged raw anchor is a valuable counterexample to simplistic claims about information loss.

Keep this modest: no high-dimensional regression, general semantic parser, or claim that task level causes recovery difficulty. All six families stay in the core. A delivery timeline is the default; an elaborate exposure graph is not.

**Extra inference: 0.** Reuse existing v2 mathematical examples as examples, not model findings. Do not spend weeks extending the proofs.

### C. Give a practical quality-versus-cost conclusion

Use the lean [quality/reuse/cost analysis](04_QUALITY_REUSE_COST.md).

**Deliverable:** one paired quality/cost table or plot showing recovery quality, output preservation, retained evidence and actual allocated cost. The experimental GPU ledger counts a shared prefix once; hypothetical per-policy workflow comparisons each include the already-spent prefix. Becoming correct early does not save calls in the fixed schedule.

If it can be completed in half to one day, add the [single frozen boundary-rule replay](16_BOUNDARY_POLICY_REPLAY.md). Evaluate a runtime-observable rule using complete existing B/C branches. If it always selects the same policy, report that and stop; do not search main outcomes for a winning rule.

**Extra inference: 0.** Boundary-rule replay is an optional short table, not a fourth major chapter or a learned-policy project.

### D. Add one genuinely different recovery state, if affordable

Run [compact-state recovery K](07_COMPACT_STATE.md): preserve current source evidence and the peer's own round-four typed candidate, but remove the rest of the previous derived conversation. An absent or malformed round-four candidate stays absent; do not search backward for a better one or use gold to select it.

Compare **B: evidence + full history**, **K: evidence + own last answer**, and **C: evidence only** from the same prefix. Add both changed and sham K branches on 12 predetermined worlds, two per task. Existing B/C siblings provide the controls.

The question is practical: **does keeping a compact computed result capture useful past work without carrying the entire conversation?** A winning K is useful; K matching C, matching B, or carrying forward old mistakes are also informative outcomes. This is a state-package comparison, not a pure test of anchoring or context length.

**Extra main inference: 384 calls.** Add up to 64 development calls on two predetermined development worlds within the existing pilot allowance. Twelve world clusters provide a small diagnostic, not precise per-family effects or a guarantee of detecting modest improvements. Keep the original theta as the sole primary estimand; K comparisons are prespecified descriptive secondary analyses with all cell means and uncertainty.

Do not also append partial resets, delayed resets, receipts, pause arms and repeated edits. One interpretable middle policy supplies more value than a poorly powered collection of mechanisms.

## Ranking of the options

Ranks reflect usefulness and value per effort, not originality. The first six rows form the compact recommended analysis/experiment package; several share one table or figure.

| Rank | Addition | Default decision | Reason |
|---:|---|---|---|
| 1 | [Failure taxonomy and paired cases](02_FAILURE_TAXONOMY.md) | Add lean version | Makes success, failure and mixed findings explainable rather than leaving a policy leaderboard |
| 2 | [Compact-state K](07_COMPACT_STATE.md) | Best optional new experiment | A simple usable middle state across all six tasks; one clear additional comparison |
| 3 | [Task structure](05_TASK_STRUCTURE_AND_RECOVERY.md) + [information atlas](06_RECOVERY_INFORMATION_ATLAS.md) | Add one joint section | Explains what the six tasks reveal about locality, summaries, alternatives and ownership |
| 4 | [Communication/evidence timeline](03_COMMUNICATION_AND_INFORMATION_FLOW.md) | Add minimal panels | Gives concrete interpretations of B–L and C–F without guessing semantic dependencies |
| 5 | [Recovery paths](01_RECOVERY_TRAJECTORIES.md) + [synchronization](15_TEAM_SYNCHRONIZATION.md) | Integrate into core results | Shows unstable, fragmented and delayed recovery hidden by final accuracy |
| 6 | [Quality, reuse and cost](04_QUALITY_REUSE_COST.md) | Add lean version | Converts findings into an operational tradeoff; much instrumentation is already required |
| 7 | [One boundary rule from saved branches](16_BOUNDARY_POLICY_REPLAY.md) | Optional zero-call table | Tests a practical decision without model training; stop if the rule is constant |
| 8 | [Deterministic recovery references](14_DETERMINISTIC_RECOVERY_REFERENCES.md) | Small appendix/supporting checks | Clarifies exact information/computation limits; avoid turning CPU solvers into privileged agent tools |
| 9 | [Continuation repeatability](17_CONTINUATION_REPEATABILITY.md) | Alternative to K when uncertainty is the priority | Improves confidence in seed-sensitive observations; does not add a new recovery capability |
| 10 | [Fixed delayed reset](10_DELAYED_RESET.md) | First alternative live policy | Simple question about preserving one more round of work; less direct than compact state |
| 11 | [Historical change receipts](11_HISTORICAL_CHANGE_RECEIPTS.md) | Optional focused alternative | Useful information-interface question, but narrower task coverage and a less immediate thesis story |
| 12 | [Partial team resets](08_PARTIAL_TEAM_RESETS.md) | Defer from minimum package | Interesting distributed mechanism, but meaningful mask comparisons quickly consume several arms |
| 13 | [First-round communication pause](09_FIRST_ROUND_COMMUNICATION_PAUSE.md) | Defer | Can separate early discussion effects, but adds delivery semantics and a narrower causal question |
| 14 | [Revision timing](12_REVISION_TIMING.md) | Future extension | Engaging temporal story, but prefix investment and evidence acquisition change together |
| 15 | [Change direction](13_CHANGE_DIRECTION_AND_SECOND_EDITS.md) | CPU interpretation first; defer extra runs | Direction can change the information problem itself, making a clean extra matrix harder |
| 16 | [Second revision](18_SECOND_REVISION.md) | Future work | Realistic recovery durability, but doubles temporal/control complications and weakens focus |

The file numbers are stable identifiers, not ranking positions. Keeping 18 separate option notes makes alternatives reviewable; it does not imply 18 thesis deliverables.

## A concrete, limited thesis structure

1. **Core causal results:** retain the original primary interaction, B–L/C–F comparisons, no-change and answer-preserving controls, and exact uncertainty reporting.
2. **Recovery anatomy:** explain the curves using observable failure labels, peer synchronization and a small matched casebook.
3. **Distributed information and task structure:** show delivery/evidence views and a six-row task-information explanation. State where the data do not distinguish explanations.
4. **Practical state choice:** present measured quality/cost, then K versus B/C if its runs were admitted. A frozen boundary-rule table is optional.

Target about five or six main figures/tables **including the core PS figures**, plus the short casebook. Move detailed per-world traces and secondary task breakdowns to an appendix. Do not create one results subsection per candidate note.

The analysis-only package is roughly **4–7 focused working days** beyond the original logger/evaluator and data collection. K plausibly adds **2–3 days** of renderer/branch/check work plus analysis, with additional margin if integration is immature. These are planning judgments, not measured labor or a promise; individual-file estimates overlap and should not simply be summed. The smallest useful version of each note is the scope limit.

## Compute envelope for the recommended live addition

| Item | 48-world core | 36-world fallback |
|---|---:|---:|
| Original main calls | 5,856 | 4,488 |
| K changed + sham, 12 fixed worlds | 384 | 384 |
| **Main total** | **6,240** | **4,872** |
| Increase over corresponding core | 6.56% | 8.56% |
| Break-even mean within 24 main GPU-hours | 13.85 allocated s/call | 17.73 allocated s/call |

The added 384 calls cost 1.07 / 1.60 / 2.13 aggregate GPU-hours at illustrative 10 / 15 / 20 allocated seconds per call. Actual prompt lengths and phase-specific costs govern admission. At 15 seconds/call with all six reserve hours included, the total would be **32.00 hours for 48+K** or **26.30 for 36+K**. These examples demonstrate why feasibility must be measured.

Development: original 588 calls plus 64 for two K changed/sham pairs gives **652**; including a separate maximum 24-call smoke screen gives **676**. This is 2.82 hours at illustrative 15 seconds/call before additional overhead, inside three hours only if the complete measured development allocation permits it. Failed configurations and backend probes still consume that same allowance. Do not add GPU hours by relabeling pilot work.

Use the original slower-device/phase weighting and 25% timing margin. The limit is aggregate allocated device time, not wall time. Preserve complete six-family core coverage, original controls and the same accepted model across conditions.

**Decision order:** choose the original complete 48/36-world schedule under its capability/timing gates first. Add K only if the whole admitted package fits. If an affordable 48-world core cannot also fit K, keep the 48-world core plus the analysis-only package. If the original core already requires 36, add K only when 36+K fits. Freeze the selected 12 worlds and all outcomes before main results. Never remove unhelpful K runs or buy another mechanism after inspecting treatment effects.

If timing clearly permits a larger K diagnostic before outcomes, 24 fixed worlds (four per task) cost 768 added calls. Prefer extra independent worlds for the same K question over adding a second new mechanism. This is an optional pre-run expansion, not part of the minimum recommendation; whole-study coverage and budget must still fit.

## What this package can conclude even without a new winner

- If all policies recover, show which preserves correct work, how quickly peers synchronize, and what each costs.
- If reset helps, distinguish reduced old-value persistence from collateral errors and generic sham benefits, without assigning hidden mechanisms.
- If retention helps, show which task/evidence configurations make accumulated outputs useful.
- If K matches the useful parts of B at lower measured cost, it supplies a practical compact representation; matching point estimates alone is not proof of equivalence.
- If K fails, the result can show that final answers omit useful intermediate work or retain mistakes—but those explanations need the observed traces, not assumption.
- If a simple boundary rule degenerates or fails, report that cheap coverage signals do not select a useful policy here.
- If capability or protocol validity limits the experiment, the failure taxonomy and exact controls make that limitation identifiable and useful.

**Final choice:** an explanatory analysis package plus, at most, compact-state K. This is the smallest combination with broad six-task coverage, a clear mechanism comparison, low infrastructure burden and useful outcomes under success, failure or mixed results. PROJECT_SPECIFICATION.md should remain unchanged until a later specification revision is explicitly undertaken.
