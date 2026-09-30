# Independent adversarial literature/design review

Review date: 2026-09-30. Reviewed `RECOMMENDED_INNOVATION.md`, `OPEN_RESEARCH_GAPS.md`, `CANDIDATE_INNOVATIONS.md`, `VALIDATION_STRATEGY.md`, and `RESEARCH_REDIRECTION.md`. Reviewer did not edit these synthesis files.

## Overall verdict

The synthesis is unusually candid about prior art. It correctly acknowledges that closure records can be ordinary control-dependent workflow nodes, and that current receipts do not prove semantic completeness. **No fatal novelty overclaim was found.** Option 3 is defensible as a research bet conditional on the pilot, not yet as evidence that the mechanism is superior or scientifically original.

The main remaining weaknesses concern causal identification and an underspecified comparison. Fix these before promoting the recommendation into a specification.

## 1. Primary contrast conflates artifact reuse with completion reopening — high priority

`VALIDATION_STRATEGY.md` makes O−E primary. E receives acquired source evidence and a fresh planner; O also retains admissible computed artifacts and receives an open-obligation list. Any gain could come entirely from extra useful artifacts, shorter context, or stronger task decomposition. O−R similarly changes prose retention/context construction as well as completion status. Neither contrast by itself identifies the effect of making completion revisable.

**Fix:** explicitly label O−E the effect of the *whole recovery package*. Add a main matched-state control with the same current source evidence, same admissible artifacts, same pending questions, same context/token allowance, and a generic revision/reconsideration instruction, but without runtime enforcement of closure. Alternatively make this the primary comparison and keep O−E as the economic baseline. A six-world reminder diagnostic is too weak to carry the central causal claim, even though it is useful exploratory evidence. If the extra arm does not fit, reduce broad benchmark scope before weakening the mechanism comparison.

## 2. The strongest reference must include explicit completion nodes — high priority

The text correctly says REVISE can represent closure through objective/control/membership reads. But P is specified only as general control/membership-aware selective recovery. A P implementation that traces ordinary data while omitting completion semantics would artificially favor O for receiving the state representation under test.

**Fix:** specify two interpretations if necessary: ordinary observed-work instrumentation as a realistic implementation baseline, and **P+ with the same explicit closure records** as O, represented as ordinary control-dependent nodes. P+ is the reduction test. If P+ and O are behaviorally identical, report equivalence of the implementation decomposition and move the scientific claim to the empirical omission phenomenon/state-interface lesson. Do not treat semantic equivalence as an algorithmic win. See [REVISE §§3.1–3.3](https://arxiv.org/html/2609.00643v1).

## 3. Broad reopening may be exactly a fresh planner with a task list — high priority

Every main method gets the correction; there are only a few peers/scopes; broad O reopens all completions and uses a clean rendered context. With no delayed old messages, there may be no operational event where enforcement differs from ordinary evidence-preserving replanning. The framing acknowledges this, but the study could spend its budget rediscovering that a planner benefits from a good task list.

**Fix:** predefine the divergence condition: identify a natural trace in which a prior closed child suppresses current work or an old receipt would otherwise authorize `done`, and show that the lifecycle changes that decision. If none occurs, do not manufacture superiority by allowing only the baseline to obey a stale stop flag. Report the protocol as ordinary fencing hygiene and assess semantic replanning separately. The independent completion interface can still be useful, but usefulness must not be inferred from a state-machine invariant alone.

## 4. Receipt/source-view representation needs one more concrete contract — medium priority

The example record contains `objective_revision` but no explicit source/domain snapshot or receipt revision field, while acceptance is promised for the current objective/source view. An unchanged query is not enough: its result may be incomplete after a member insertion. Conversely, a historical receipt can remain accurate evidence about what ran without remaining a current coverage certificate.

**Fix:** define receipt fields for query identity, objective revision, source/domain snapshot identifier, covered scope, and operational-completion status. Clarify that historical query results are archival evidence unless current domain validity is established. Use a serialized revision/closure transition or explicit version comparison to reject races; CPU tests can establish that narrow guarantee. This is standard version validation, attributed as such.

## 5. Capability diagnostic costs imply centralized calls — medium priority

The compute table allocates only two before/after full-information calls per main world. This can assess a centralized solver's competence, but does not establish that four peers can solve the revised task within four rounds under the actual acquisition/communication interface.

**Fix:** label these centralized capability diagnostics. Include a small development check using the actual distributed interface and current world, priced separately. Failure in the main protocol should not be attributed to recovery when the fixed round cap prevents ordinary distributed completion.

## 6. “Only the second is necessarily a new scientific result” is too strong — low priority

`RESEARCH_REDIRECTION.md` distinguishes benchmark, empirical finding, and mechanism, then says only the empirical finding is necessarily a new scientific result after execution. Execution alone does not guarantee novelty: [StateAuditor](https://arxiv.org/html/2608.01619v1) already studies updated state with unrevised behavior, and related replanning work handles reconsideration.

**Fix:** say the empirical result is the intended scientific contribution, subject to distinguishing post-collaboration search omissions from these precedents and validating the comparison. A replication/generalization or null result can be worthwhile without calling it necessarily new.

## Source/novelty honesty that should be retained

- The no-firstness statements, explicit REVISE reduction, and conditional fallback are appropriate.
- Treating scope hints as advisory and unknown scope as broad reopening avoids a hidden oracle.
- Distinguishing process completion from decision verification is essential.
- Current artifact checks must not silently compute the answer; checker access parity is already correctly required.
- The finite transfer adapter establishes interface portability only. It cannot justify open-web search completeness or hours-long savings.

## Recommendation after review

Retain the direction conditionally. Before the main run, require (i) a natural omitted-work failure, (ii) a main matched-state generic-replanning control, and (iii) a closure-aware established-recovery reduction test. If these reveal no distinct behavior, use the existing mechanism and publish the empirical boundary rather than inventing a new algorithm name.
