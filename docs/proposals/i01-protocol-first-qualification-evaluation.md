**Yes—removing the mathematical-accuracy gate is scientifically defensible for our research objective. I recommend keeping direct mode, treating mathematical accuracy as a diagnostic and experimental outcome, and retaining strict protocol and execution checks.**

This would be an explicit scientific-design amendment. My earlier proposal enforced the existing 11/12 rule; that rule is a screening choice, rather than a universal requirement for valid research.

Our question concerns the practical effect of retaining versus clearing a distributed conversation. That effect can be studied in an imperfect system. Mistakes may be particularly relevant: retaining a mistaken submission or misleading message could influence later recovery. Reasoning failures are also central to SILO-BENCH’s motivation and findings. [SILO-BENCH paper](https://arxiv.org/abs/2603.01045)

For course-2 specifically, **10/12 does demonstrate substantial observed task ability**. Both errors occurred on one world; the other five worlds passed both controls. These are six related original/revised pairs, however, so 83.3% should not be treated as a precise reliability estimate.

The main scientific risks are:

- **A floor effect.** If both treatments usually fail, their success difference may be near zero even when their behavior differs substantially. With twenty main worlds, the study could be valid but weakly informative. A null result would require cautious interpretation.
- **Weak recovery evidence.** When the original collaboration was already incorrect, the continuation measures adaptation from an imperfect history. The existing correct-prefix secondary analysis addresses recovery following successful initial collaboration, but its denominator could become small or zero.
- **Protocol compliance without meaningful collaboration.** A model could return valid JSON containing a constant integer every time. Valid schema and legal actions establish operational compatibility; they do not establish that a useful distributed conversation occurred. Pilots should therefore inspect actual task engagement and information exchange.
- **Limited attribution.** Mathematical errors do not inherently invalidate the paired policy comparison. They can add variability or form part of the policy effect itself. Full-information controls help diagnose capability, but cannot isolate “memory failure” from reasoning failure or justify subtracting control error rates from the treatment contrast.

Keeping direct mode also preserves a clear experimental condition. Switching to thinking would change generation settings, available reasoning effort, output length and resource demands. It could improve competence, but it would answer the question for a different operating condition.

My recommended policy is:

| Component | Recommended treatment |
|---|---|
| Qualification JSON and action semantics | Hard gate: exact schema, strict types and legal actions |
| Runtime integrity and resources | Hard gate: fresh state, finite scores, privacy, persistence, headroom, deadlines and attempt accounting |
| Qualification mathematical accuracy | Report completely; remove the accuracy admission threshold |
| Pilot mathematical accuracy | Report completely; mathematical mistakes alone do not disqualify |
| Pilot feasibility | Require trustworthy execution, inspectable evidence and genuine task-relevant interaction |
| Main outcomes | Preserve exact scoring: recorded unsuccessful outcomes are zero; unexecuted/unresolved outcomes remain unknown |

**The pilot rules must change consistently.** Removing 11/12 while still requiring all three original pilot teams and all six pilot controls to be correct would merely move the same accuracy barrier downstream.

I would retain the existing primary analysis over **all twenty intended worlds**, plus the already planned correct-prefix descriptive stratum. Never discard worlds because their controls or prefixes failed. Report control accuracy, prefix success, paired recovery outcomes, failure types and effort together. If pilots reveal pervasive failure or no meaningful communication, review whether the study remains informative without selecting for a favorable retain/clear effect.

There is also a transparency issue: this proposal follows observation of the 10/12 result. That does not make it indefensible, especially because no main outcomes have been observed, but the timing must be documented. Preserve the original rule and its failed result, explain the revised rationale, and freeze the amended policy before further experimental execution. This follows the transparency principle described by the [Center for Open Science](https://www.cos.io/blog/preregistration-plan-not-prison).

For the current run, the saved controls **would satisfy the scalar-control protocol portion** of this revised policy. They would still be reported as 10/12 mathematically correct, with all eighteen attempts preserved. Full-envelope and collaboration evidence remain outstanding.

I recommend this principled separation over lowering the cutoff specifically to 10/12. It accommodates normal model errors while preserving the conditions needed to interpret them. The independently identified software defects still require repair.

No files, rules or implementation have been changed.
