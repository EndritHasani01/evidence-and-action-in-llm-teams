# Independent mechanism review

Reviewed 2026-09-30: `RECOMMENDED_INNOVATION.md`, `VALIDATION_STRATEGY.md`, and `FALSIFICATION_AND_RISKS.md`. This review did not edit those synthesis documents. It assesses the proposed protocol rather than measured efficacy; no live model experiment exists yet.

## Verdict

The recommendation is useful as a deliberately modest research-interface hypothesis. It is materially more interesting than another generic rollback graph because it tests **adequacy of completed work after change**, including decisions whose retained positive evidence remains true. The documents acknowledge classical and recent overlap accurately and avoid promising semantic completeness.

However, the operational discharge rule remains underspecified, and the experiment does not yet isolate runtime reopening from artifact retention strongly enough. These are fixable before implementation. Do not freeze a preregistration or claim a reusable runtime mechanism until the first two issues below are resolved.

## 1. High priority: define the smallest executable closure rule

The proposed step 'accept a new completion receipt ... and required operational checks' hides the essential intervention. Different interpretations produce different experiments:

- If a model can emit CLOSED after reading the correction, this is an explicit reconsideration prompt plus a timestamp.
- If closure requires querying every provider, this is a mandatory acquisition policy.
- If closure requires exact coverage of all competitive options, the runtime may already implement the crucial solver/search logic.
- If closure requires only a fresh planner pass with zero required acquisition, it cannot establish that the omitted branch was revisited.

The text correctly distinguishes process completion from decision verification, but that distinction must become an adapter contract before the pilot.

**Concrete correction:** add a small reference transition table defining which host-observed event closes the root. Start with a minimal universal contract such as: after revision, a current-revision reconsideration turn must finish, all currently required child obligations must be terminal, and the candidate receipt must match the source/objective snapshot actually consumed. Call this **reconsideration performed**, not search complete. List any additional per-adapter operational requirements separately. Let correctness remain exclusively an evaluation outcome.

Record separate fields for `reconsideration_performed`, `operationally_closed`, and evaluator-only `answer_correct`. This prevents a fresh receipt from becoming an accidental correctness label. If even this interface merely duplicates the generic reminder under equal calls, report that result rather than adding more hidden requirements.

## 2. High priority: the primary contrast confounds reopening and artifact retention

O retains admissible computed artifacts while E retains current acquired evidence. Therefore O versus E can improve solely because O preserves useful intermediate computation. That is a legitimate reuse contrast, but cannot establish the value of completion obligations. The generic reconsideration control shares artifacts and is the closer causal test, yet currently receives only six worlds.

**Concrete correction:** promote the matched generic reconsideration arm to the main design. Match active artifact payloads, raw history inclusion, available evidence, per-turn prompts other than the explicit lifecycle intervention, maximum calls and tool quotas. Compare this arm with O for the primary **mechanism** contrast. Keep O versus E as the main **reuse** contrast or a prespecified secondary contrast. If the compute budget requires a choice, move R or F to a smaller diagnostic subset rather than relegating the strongest alternative to six worlds.

The framework can retain one prespecified primary contrast, but it must say what that contrast establishes. If the primary remains O versus E, title the hypothesis around retained work plus reconsideration, and explicitly reserve the independent effect of runtime completion state as unestablished without sufficient matched-control evidence.

The matched-observation diagnostic is correctly described as small and descriptive. It should not be used to rescue a missing main causal control.

## 3. High priority: obsolete child obligations must be retired, not all reopened

'First implementation reopens all task completion claims' can revive work that the revised objective explicitly removed. A canceled deliverable, an obsolete query plan, or mutually incompatible old requirements can become mandatory again. Waiting for every old child would waste work or deadlock completion.

**Concrete correction:** distinguish durable goal obligations from historical execution records. Automatically reopen the durable root; old children become historical/pending reassessment, not automatically required. The current planner determines the new required-child set, using the same bounded authority as ordinary planning. Add `RETIRED`/`CANCELLED` or an orthogonal `required_under_revision` field. Cancellation must not delete evidence. Root closure waits only on children required under the current objective revision. A late completion from a retired child cannot reactivate it.

This remains a small state table; no general workflow engine is needed. A CPU fixture should revise an objective by removing a subtask, then prove the root can close without performing it.

## 4. Coverage fallback is procedural, not automatic detection of missing semantics

The docs generally recognize this. One sentence in the falsification table nevertheless says omitted/corrupted scope failures 'must trigger broader reconsideration or appear as an error.' A runtime cannot reliably detect an internally omitted alternative from absent model notes. A model can give an apparently precise but incomplete scope.

**Concrete correction:** split two cases. Observable missing/unknown metadata invokes root fallback deterministically. Hidden semantic omission is caught only by independent evaluation and remains a method failure unless a separately specified trusted coverage mechanism covers it. State that agent hints never exempt the root from reconsideration. Narrowing exemption requires trusted scope membership and a defined change-intersection test; a self-asserted scope is insufficient.

Any coverage marker must identify its universe and time. 'Every provider was queried' does not imply the queries covered every newly relevant option. Exhaustive listing can establish finite coverage but may cost as much as restart; charge that cost and admit this boundary.

## 5. Version checking needs snapshot semantics and a bounded liveness policy

The delayed-v2-after-v3 test is appropriate. The minimal protocol should say whether a generation reads one immutable snapshot or can mix source versions. Checking only `current_epoch` at receipt creation permits a response generated on v2 to be restamped v3. The host must bind the receipt to the snapshot used for the invocation, and any admitted artifact checks to their actual input view.

**Concrete correction:** host-issued invocation revision identifiers; immutable per-call source view; compare-and-close only if the root objective/source-domain revision still matches. An intervening relevant update keeps the obligation open. Keep stale payloads as proposals only through the normal admission path.

Repeated updates can prevent closure forever. Promise safety of obsolete-receipt rejection only, with liveness conditional on a sufficiently quiet interval and available sources. Under exhausted recovery budget, return a current provisional result with an explicit unresolved obligation rather than inventing a terminal guarantee. This is a normal bounded failure, not a deadlocked agent loop.

## 6. The prose-retention intervention needs one default

O's clean context construction, R's full history and E's clean planner are different context treatments. That is fine as a system comparison, but rhetoric such as 'revoking completion caused improvement' is too strong if O also removes influential old prose.

**Concrete correction:** specify O and matched reminder as using the same renderer and same retained artifacts. Include old free-form rationale only in the dedicated contamination diagnostic. Log the exact artifact IDs and text included per invocation; context length cannot be matched merely by padded tokens if semantic content differs.

Avoid an added verifier model. In the minimal version, use only raw current records and artifacts whose narrow validity is deterministically checkable without deciding the global task. If no such useful artifacts exist in an adapter, state that it tests evidence reuse only.

## 7. Useful beyond prior art, but only under a specific result

The literature already supports representing closure as an ordinary control dependency. A runtime interface can still be useful if it makes hidden stopping decisions observable cheaply, catches obsolete terminal events, and lets implementers avoid discarding costly surviving artifacts. That is an adoption argument, not an algorithmic novelty argument.

The interesting potential finding is an **asymmetry**: opportunity-style updates with still-valid incumbents cause more omission failures than retraction-style updates under matched initial competence, and a small explicit reconsideration lifecycle changes that behavior. The current plan can test this, but six worlds per event/family stratum imply exploratory estimates, not a reliable universality claim.

A particularly valuable null would show that a fresh planner with retained artifacts and a generic reconsideration prompt matches the stateful mechanism. Then recommend that simple interface as the practical contribution and do not retain the state table for prestige.

## Suggested lean implementation

One authoritative revision counter per task; a root obligation plus current required-child IDs; host-issued immutable invocation views; a table of retained evidence/artifacts; and a context renderer. Scope hints remain optional annotations. No new graph engine, dependency extraction model, global proof system or exact runtime optimizer is justified initially.

Required CPU tests: stale close, restamped stale close, canceled child, unknown scope, new membership, a second correction during reconsideration, exhausted budget, and independent sibling branches. Required live comparisons: O versus same-artifact reminder and E. Existing R/P/F arms remain valuable where the measured budget supports them.

## Ready-to-adopt corrective priorities

1. Specify closure and retirement transitions before pilot implementation.
2. Promote the same-artifact reminder control or narrow the primary claim.
3. Bind receipts to actual invocation snapshots and define bounded noncompletion.
4. Replace implied hidden-omission detection with an explicit procedural/semantic distinction.
5. Keep scope optimization optional; let a simple null result determine the final runtime recommendation.
