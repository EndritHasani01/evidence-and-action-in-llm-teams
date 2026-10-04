# 15. Does the team recover together?

**Recommendation: include as a small panel in the recovery analysis, not a separate experiment. Extra calls: 0.**

## Idea in simple terms

A team can fail even when every peer gets its part right at some point. Their correct moments may not overlap. Distinguish “each peer eventually produced its correct output” from “the four peers were correct together and stayed that way.”

For example, correct peer sets across four rounds might be `{0,1,2}`, `{0,1,3}`, `{0,2,3}`, `{1,2,3}`. Mean peer accuracy is 0.75, everyone was correct repeatedly, but the team never completed jointly. This is an illustration, not an observed result.

## Question and why it matters

Are failures concentrated in one persistently unsuccessful peer, or does correctness move between peers without becoming a stable team result? Would improving local reasoning alone explain the problem, or does the observed team trajectory need closer coordination analysis?

The distinction makes particular use of four peers. It gives a clear story beyond a final policy ranking and avoids treating average peer accuracy as team completion. It does not prove coordination caused a failure.

## Minimum analysis

Use exact correctness of each **assigned** peer output after every recovery round. Let `c[p,r]` be its 0/1 correctness, including malformed candidates as zero:

- `joint_ever = max_r product_p c[p,r]`: some round has all peers correct.
- `individual_ever = product_p max_r c[p,r]`: each peer was correct in at least one round.
- A fragmented trajectory has `individual_ever=1` and `joint_ever=0`.
- Distinguish transient joint success from success that persists through round four, using the PS's existing stable-recovery definition.

Show one four-row peer-by-round correctness raster per selected trace, and a compact count of fragmented versus never-individually-complete trajectories. This can share the figure/data pipeline of [01_RECOVERY_TRAJECTORIES.md](01_RECOVERY_TRAJECTORIES.md). Report world counts and paired policy differences; do not resample the 16 peer-round cells as independent observations.

For replicated-output tasks only (max, top-K, difference and BFS), add the rate of **valid identical but wrong full candidates**. Prefix/sort peers have different assigned segments, so whole-answer agreement is not a meaningful requirement for them. Do not force a universal consensus score.

The PS already reports joint completion and first/stable correct rounds. The actual addition is the decomposition of incomplete teamwork and the explicit comparison with individual-ever success, not rebranding those existing metrics.

## Effort and controls

Approximately half to one working day beyond an existing per-peer outcome table and trajectory plot. No new prompts, orchestration, judgments or model calls. Empty categories should be reported as zero counts, not filled by hand-picked anecdotes.

Do not assemble the best answers from different rounds and call that a deployable recovery policy: that would require oracle knowledge of when each answer was correct. A fragmented trajectory is evidence about observed timing, not proof that all useful facts were simultaneously available or safely recognizable.

## Interesting possible outcomes

- B produces many individually correct answers but unstable joint completion: retained interaction deserves trace inspection.
- C has fewer reversions and more stable joint success even with similar mean accuracy.
- Failure sits consistently with the same output owner: task/output-placement explanations become more useful than generic consensus language.
- All peer and team indicators move together: synchronization adds little and the thesis can keep only one illustrative panel.

**Scope limit:** four rounds can miss later convergence; say “not jointly correct within the measured horizon.”
