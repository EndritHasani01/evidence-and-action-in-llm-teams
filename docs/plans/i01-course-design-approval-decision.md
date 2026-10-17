# I-01 course experiment: final design decision and approval boundary

16 October 2026. **Independent design review; submitted for the user's approval.**
This task creates only this new Markdown document. It changes no existing file,
scientific contract, implementation, configuration, prompt, result or artifact,
and performs no model loading, inference or GPU work.

## 1. Final decision

Select **one fresh, paired, natural-history retain/clear campaign under the
fixed assisted environment already specified**, with four complete feasibility
pilots and twenty main worlds. Keep the maximum task, pinned Qwen3.5-9B runtime,
strict actions, private finality, three invocations per agent per phase and
exact both-agent scoring. End at feasibility if the fixed candidate fails its
prespecified gate. Do not add a rescue experiment to this campaign.

The question is:

> Under this fixed assisted two-agent environment, how do literal retention and
> clearing of naturally acquired visible history differ in exact team recovery
> and effort after withdrawal of the unique winning record?

This is the **total practical history-policy contrast**, including changes in
available reports, conclusions, feedback, conversational cues and context length.
It is an appropriate course-project question. It does not isolate a pure memory
mechanism, spontaneous algorithm discovery, correction specificity or preservation
of expensive computation. Those stronger questions require different experiments.

No further scientific redesign is selected in this review. In particular, do
not replace this campaign with controlled prefixes, add sham events, screen main
prefixes for correctness, change models or turn limits, or build a memory system.
The design is sufficiently specified; the next decision is approval and release
readiness, rather than another round of open-ended design exploration.

### Relationship to the existing repository

The checkout reviewed here is on `feat/smaller-natural-experiment` at `b1d3364`,
with pre-existing uncommitted implementation and documentation changes. They
are preserved, including their unfinished status. The repository already has
the following documents; this review incorporates their operational detail
instead of creating another prompt or competing protocol specification:

| Document | Role in the selected design |
|---|---|
| [Scientific specification §12.1](../../PROJECT_SPECIFICATION.md#121-assisted-i-01-course-regime-16-october-2026) | Current sole scientific authority for the separately scoped assisted condition |
| [Final experimental design](i01-course-final-experimental-design.md) | Complete study definition, scientific target and stage allocation |
| [Exact protocol and acceptance annex](i01-course-final-design-protocol-and-acceptance.md) | Exact instructions, renderer, feedback, fixtures, seeds, assignment, forecast and verification requirements |
| [Earlier consolidated finalization record](i01-course-design-finalization-record.md) | Supporting interpretation, including uncertainty and diagnostic limitations |
| [Implementation checklist](i01-assisted-implementation-progress.md) and [evidence](../validation/i01-assisted-implementation.md) | Recorded software progress and executed checks, with remaining work explicit |

The design documents retain their dated pre-adoption wording. Current §12.1
already records adoption and implementation authorization; this review neither
rewrites nor reverses that history. For the present request, the recommendation
remains subject to the user's approval and authorizes no implementation or
execution. Any disagreement is resolved by the scientific specification, not
this review. No additional contract amendment is proposed.

## 2. Evidence and resolution of the competing recommendations

The [Course-7 audit](../validation/i01-course-7-independent-scientific-audit.md)
establishes a complete but weakly collaborating system: 3/20 correct original
teams, 2/20 exact recovery successes in each policy, and 60 rejected actions
among 206 team calls despite valid JSON and field types. Seventeen main pairs
fail in both policies; one favors each policy and one succeeds in both.
A small read-only count from the canonical stores reproduced these values in
this review. The full existing forensic audit need not be repeated.

The relevant findings extend beyond illegal actions. Agents committed local
answers despite larger received values, planned to adjust already final
submissions, interpreted notice fields as partner answers even with empty
history, and sometimes submitted values below their current local maximum.
The audit found no scorer, delivery or sibling-isolation defect explaining
these results. Source availability, correct prose and eventual agreement did
not guarantee a correct committed action. [Audit §§6–9](../validation/i01-course-7-independent-scientific-audit.md#6-failure-anatomy-from-the-complete-traces).

| Rank / competing direction | Final disposition | Scientific and practical judgment |
|---|---|---|
| 1. One assisted natural retain/clear campaign | **Select** | Best continuity with the course question and existing infrastructure; preserve its bundled interpretation |
| 2. Exact process reporting, live pilots and fixed stop rules | **Require within that campaign** | Improves interpretability and protects against another admission procedure that permits an unusable system without acknowledging it |
| 3. Fixed evidence, conclusion present/absent, edit/sham | **Defer** | Better for the mechanism question in the literature recommendations; supplied competence, new histories and four continuations answer another question |
| 4. Clarification versus strategy ablation or matched Course-7 baseline | **Do not add** | Needed to estimate ingredient/package efficacy, which is not the selected endpoint; spends scarce calls on a second target |
| 5. Stronger model, thinking, constrained action decoding or more turns | **Defer** | Plausible alternatives, but no matched I-01 evidence selects one; each changes the agent condition and needs new qualification |
| 6. Selective memory repair, provenance graphs, reflection or LLM judging | **Exclude** | Adds supervision, assumptions and cost without a demonstrated requirement in this small exact task |

The earlier [quality proposal](../proposals/i01-course-7-experimental-quality-improvement.md)
and [mechanism-oriented recommendations](../proposals/i01-course-7-literature-informed-recommendations.md)
are therefore not irreconcilable. Their preferred designs optimize different
claims. The [practical investigation](../implementation-research/i01-course-practical-literature-investigation.md)
appropriately shifts priority toward usable interaction and manageable scope.
Choose its practical target, while retaining the earlier review's cautions
about information availability, scaffolding and causal attribution.

### What the literature warrants

The existing [fifteen-paper review](../implementation-research/i01-course-7-targeted-scientific-literature-review.md)
and practical investigation remain the reading inventories. This review checked
the following consequential published evidence directly, including the cited
full-text passages. These are reported findings, not our replications:

| Publication and precise evidence | Lesson used here | Transfer limit |
|---|---|---|
| Yang et al., **SWE-agent**, NeurIPS 2024, §5.1/Table 3, PDF p. 6: summarized versus iterative search resolves 18% versus 12% in that ablation | A fixed model's interface can materially affect performance; test a compact common environment before escalating model complexity | Coding, demonstrations, lint feedback and context management differ from I-01; no numerical gain transfers. [Record/full text](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) |
| Barres et al., **τ²-Bench**, ICML 2026, §4.2/Figure 4, PDF pp. 6–7: workflow guidance raises GPT-4.1 default success .34→.52, but lowers its oracle-plan result .73→.57 | Short strategy assistance is defensible, and more scaffolding is not uniformly better | Expert/user dual control, stronger models and supplied oracle plans differ; centralized-control gaps do not isolate communication failures. [Record](https://proceedings.mlr.press/v306/barres26a.html), [official full text](https://raw.githubusercontent.com/mlresearch/v306/main/assets/barres26a/barres26a.pdf) |
| Xiao et al., **FlowBench**, Findings of EMNLP 2024, §4.3.2/Table 4, PDF pp. 6–7: static turns receive correct preceding histories; live sessions accumulate predicted actions, and format rankings vary by endpoint | Supplied-view probes cannot certify autonomous live collaboration; retain complete pilots | Simulated users and LLM-based judgments differ from exact I-01 scoring. [Record/full text](https://aclanthology.org/2024.findings-emnlp.638/) |

The inference for I-01 is ours: one disclosed assistance package plus natural
pilots is a proportionate test. These papers establish neither the efficacy of
our exact prompt nor a scientifically mandatory 3/4 competence threshold.
Publication-level novelty, comprehensive ablations and broad generalization
are not course completion criteria.

## 3. Fixed experimental definition

| Element | Decision |
|---|---|
| Condition and policy | `i01-course-assisted-v2`; `i01-assisted-feasibility-2026-10-16` |
| Task | Two private twenty-integer shards; uniform integers in −1000…1000, conditional on declared eligibility and scheduled winner owner |
| Revision | Replace the unique original winner uniformly below the remaining maximum; answer necessarily changes; hidden eligibility stays outside peer views |
| Common assistance | Exact annex §§1–3: legal-action examples, global objective/private finality, short generic strategy, separated history/notice/current source and rule-specific rejection feedback |
| Treatments | Independent sibling copies of one natural prefix; retain keeps literal visible history, clear removes it; both reset phase turns/submissions/waiting |
| Agent behavior | Strict existing three-field action interface; invalid replies consume a turn and deliver nothing; no action repair or correctness feedback |
| Model/runtime | Existing pinned Qwen3.5-9B revision, NF4/FP16 reviewed T4 runtime, direct settings; 8,192 input/512 output native tokens; no fallback |
| Data | Four qualification worlds, four pilots and twenty main worlds; new master seed `2026101601`; save and bind all before inference |
| Main population | Five worlds per changed-owner/first-speaker cell; one natural prefix each, including unsuccessful prefixes |
| Main measurement | Both literal siblings and one revised full-information scalar control per world; exact success requires both agents' final revised answers |
| Primary unit and contrast | World; mean `clear success − retain success` over all twenty intended worlds |
| Principal secondary endpoint | Paired mean post-revision ready-model seconds, including failed attempts and unsuccessful continuations |

Apply the annex literally. Public notice information is the changed owner and
record, plus replacement value only for its owner. Do not expose the old winner,
new answer, partner private submission, condition name or future edit. History
wrappers identify phase boundaries without rewriting messages or certifying
their contents. Current sources remain unsorted raw records.

Supply assistance identically from the original phase onward. Algorithm
discovery is outside the selected target, so a short generic strategy is an
honest scaffold. Agents must still calculate, communicate, choose reuse or
rechecking, and make irreversible commitments. Do not require a fresh peer
message before every submission: an accurate retained report from the unchanged
peer can already suffice. Do not require verification against an unseen shard.

Keep the exact [annex §4 assignment and seeds](i01-course-final-design-protocol-and-acceptance.md#4-data-seeds-assignment-and-execution).
Both siblings stay on one device. Across twenty main worlds, each joint
device/first-policy combination appears five times; each owner/first stratum
contains all four combinations with declared 2/3 imbalances. Interleave strata,
use ten fixed two-world batches, and serialize same-device worlds. Matching
invocation seeds couples the comparison; it never permits continuation-response
reuse or proves identical stochastic behavior across different prompts.

### Data separation and freezing

Check every new ordered whole input, original or revised, against every exposed
Course-1…7 and saved development input, and across the three new groups. The
intentional qualification-input reuse by diagnostic fixtures is allowed.
Individual integer overlap is expected and is not contamination. Record the
actual inventory checked; an incomplete required inventory or collision blocks
release rather than triggering seed search.

Main data are held out from model-guided prompt/example selection, not from
deterministic arithmetic and privacy audits. Do not imply that developers are
blind to arrays inspected for those checks. Freeze the package, source/runtime,
data, assignment, scoring, limits and gates before the first new model call.
The pilots decide whether this one fixed system is useful enough to continue;
they do not tune it. A behavior-changing revision after outcomes creates another
candidate/campaign and requires a new prospective decision and untouched data.

## 4. Exact feasibility and stopping decision

Use these stages in order. Eligibility never supplies execution authorization.

| Stage | Required evidence and decision |
|---|---|
| Software release | Satisfy annex §7 CPU/source/native/installed/restore checks; reconcile remaining checklist items before treating delivery as complete |
| Actual-host preparation, later authorized | Current source/dependencies, two distinct devices, six A/B/A state calls, eight legal committed scalar qualification replies and two full envelopes; finite/state/headroom/time evidence intact |
| Four diagnostics | Execute D00…D03 exactly once as specified in annex §5; require settled records, then a verified quiescent preparation checkpoint and measured export duration |
| Four pilots | Complete all four fixed original/retain/clear/two-control scopes despite ordinary mistakes; stop only for genuine integrity, unresolved execution/spending, termination or resource faults |
| Main usefulness decision | All four scopes terminal/committed with reconciled spending/exports; **at least 3/4 exact original teams and 7/8 exact pilot controls**; current health and sufficient measured resources |
| Main | If eligible and authorized, execute all twenty saved worlds; ordinary model errors never replace worlds or veto later batches |

Three distinctions are essential:

1. **Qualification legality and pilot accuracy are different screens.** A
   recorded malformed qualification reply fails the fixed format screen; it is
   not automatically a runtime bug. Qualification accuracy is diagnostic. Pilot
   wrong/invalid replies remain measured outcomes and enter the later fixed
   success denominators. There is no all-pilot-actions-legal requirement.
2. **Diagnostic nonpass is not a competence verdict.** D00/D03 explicitly
   request a form or local query; D01/D02 supply good histories. A legal
   message-only response to D01/D02 can miss the immediate-submission predicate
   without establishing inability to aggregate or update. Report the action
   and predicate; impose no aggregate diagnostic veto.
3. **Usefulness is not reliability certification.** Four balanced pilots cover
   all owner/first cells. Requiring three original successes exceeds the two
   cells exploitable by always committing the first speaker's local maximum,
   but cannot establish a 75% population success rate or guarantee informative
   main histories. The cutoffs are explicit course judgments, not literature
   constants. Main results concern the selected fixed environment.

Do not gate on recovery success, policy direction, statistical significance,
message style or retrospective qualitative impression. Once the objective rule
passes, trace review informs interpretation rather than discretionary admission.
If it fails, preserve every pilot and end with a feasibility report; main is
unexecuted/unknown. Do not relax thresholds, replace pilots, retry wrong answers,
switch models or automatically start a supplied-history alternative.

## 5. Resource and reliability boundary

| First-attempt stage | Ceiling |
|---|---:|
| Six state calls plus two envelopes | 8 |
| Four qualification worlds × two scalar controls | 8 |
| Four diagnostic calls | 4 |
| Four pilots × `(6 original + 6 retain + 6 clear + 2 controls)` | 80 |
| Twenty main worlds × `(6 original + 6 retain + 6 clear + 1 control)` | 380 |
| **Ordinary total** | **480** |
| Eligible contingency | **20** |
| **Independent campaign hard total** | **500** |

Stage caps, reserve and hard total apply together. Early finality saves calls
without adding worlds, prompts or diagnostics. Reuse the two canonical stores,
single admission owner, persist-before-effects, exact raw resume and quiescent
exports. Reopening or renaming a campaign never resets its spending; Course-7
is separate historical evidence, not an available balance for this campaign.

One identical infrastructure retry requires no durable outcome and confirmed
previous termination. Known wrong, invalid, truncated or recorded timeout
outcomes never retry. Unresolved spending blocks admission. Each unchanged
runtime reload requires six new state checks plus two envelopes charged to
reserve; accepted scientific results do not regenerate. Two such eight-call
cycles leave at most four reserve attempts for other eligible exposure.

Use the exact [annex §4.3 forecast](i01-course-final-design-protocol-and-acceptance.md#43-conservative-resource-forecast),
including remaining worst-case slots, the observed ordinary-call maximum plus
margin and measured current-session export overhead. Preserve dispatch timeout,
cleanup/export margin and one fixed deadline. The 700-minute window is only
the existing operator planning estimate; actual provider allowance and remaining
time must be checked. Course-7's quick wrong finalizations are not a completion
forecast. If the fixed scope cannot fit, preserve a truthful partial report;
do not shrink its population after outcomes or waive current-load checks.

## 6. Analysis and course-report requirements

Report exact arm success counts and the four paired categories before discussing
mechanisms. For complete main evidence, compute `sum(C_w − R_w)/20`. Positive
values favor clear. Keep every intended world, including failed originals,
illegal continuations and terminal noncompletion. A correct-prefix table is
descriptive counts only; it neither replaces the primary population nor proves
that the included teams followed a reliable process.

The cohort arithmetic is known once all records are settled. The selected
10,000-draw stratified paired bootstrap, seed `2026101602`, sorted zero-based
indices 250/9750, is an exploratory world-resampling display. It does not measure
repeated-generation reliability for a fixed world, establish equivalence or
guarantee nominal small-sample coverage. Preserve whole siblings within worlds
and show constant-stratum/zero-width warnings, including at a success ceiling.
No primary significance test or alternative interval selected after results.

If any required pair is unknown, the primary twenty-world point estimate and
interval are unavailable. Report fixed-denominator completion bounds by allowing
unknown binary outcomes to be 0 or 1. Known terminal failures are zero; unexecuted
or unresolved evidence is unknown. Completion bounds describe missing evidence,
not sampling uncertainty. Label any observed-case summaries separately.

Report full unsuccessful effort alongside outcome. Unknown time or tokens stay
unknown, and incomplete pairs cannot yield an intended-cohort effort contrast.
Charge the shared prefix once physically and to each hypothetical full policy
logically; scalar/diagnostic calls are research cost. Lower time from fast wrong
finalization is not demonstrated useful-work efficiency. Avoid an accuracy/cost
composite and success-only efficiency claims.

Require a compact set of additional displays from the annex:

- Original and scalar success with actual denominators and explicit coverage.
- Syntax, field-schema validity and action legality separately; affected
  episodes and terminal reasons, with behavior-dependent call denominators.
- Both-submitted completion, agreement and wrong agreement; locally refutable
  submissions over forty intended agent slots per policy, with coverage.
- Obsolete-answer repetition, with clear's unequal access to the withdrawn
  value stated. Old-answer avoidance alone is not recovery.
- The fixed six-category, lowest-index casebook, with absent categories retained
  as absent, exact call references and actual human-review status. No LLM judge
  or inferred causal failure percentages.

Scalar/team accuracy gaps combine different information, prompts and interaction;
they do not identify a pure communication-failure rate. Assistance may alter
how much history matters. A null under useful assistance is legitimate. Do not
weaken instructions or increase difficulty to manufacture a retain/clear effect.
Course-7 stays separate and unchanged; a cross-campaign difference cannot
identify the assistance package's efficacy.

## 7. Implementation readiness and final approval item

The exact design and annex already supply the implementation specification.
Use the existing [checklist](i01-assisted-implementation-progress.md) to finish
and audit the existing software when separately instructed; do not create a
second work tracker or runtime. The recorded evidence supports core/workflow/
reporting CPU progress. It still lists delivery, installed verification and a
final preservation/completion audit as pending. Uncommitted code and a runbook
describing a packet are not evidence that the packet passed those checks.
This review does not claim to complete or reverify that implementation.

| Acceptance area | Evidence required before release, per annex §7 |
|---|---|
| Data and assignment | Independent arithmetic, exact regeneration, 28 saved worlds, exposed-input inventory/disjointness, all declared placement/order balances |
| Agent interface and privacy | Exact incorporated text, native lossless worst-case bounds, ≤32-token feedback, owner-only values and no evaluator leakage |
| Protocol and state | Reachable diagnostics; literal history boundaries; isolated siblings; strict invalid effects, private finality, wake/deadlock/horizon behavior |
| Admission and resources | Gate boundary cases at 3/4 and 7/8, all four pilots collected, no recovery veto; joint 480/20/500 bounds, reload/retry/unknown and fixed-clock checks |
| Reporting and persistence | Hand-computed complete/incomplete paired cases, costs/coverage and bootstrap edges; exact saved raw resume, portable export/restore and full raw traces |
| Delivery and preservation | Source/wheel/notebook binding and installed checks; protected historical bytes and legacy behavior; requirement-by-requirement completion audit |

Preserve historical source identities. A current amended checkout need not equal
Course-7's executed source hash. Verify that old result against its frozen source
and test the new implementation's legacy path separately; never repair an old
identity assertion by rewriting historical artifacts. Actual T4 headroom, state,
latency and agent performance remain separate actual-host gates.

The classifications remain explicit: derived reporting corrections or verified
software defects are **engineering repairs**; common guidance/rendering/feedback
are a **behavioral intervention**; the fresh assisted campaign is a separately
identified **experimental regime**; §12.1 is the existing scoped **contract
adoption**. This document performs none of those changes.

**Final item for approval:** retain the exact assisted natural-history design,
four pilots, twenty main worlds, fixed usefulness gate and 480+20 ceiling, with
the narrow claims and stop rules above. No extra experimental arm or scientific
amendment is needed. Implementation completion and GPU execution are distinct
subsequent decisions. A complete failed-feasibility report, a completed paired
main result including a null, or a truthfully partial integrity/resource stop
can each be a defensible course deliverable when labelled accurately and backed
by its traces, coverage, accounting and portable export.

## Review scope and document verification

Reviewed root `AGENTS.md`, scientific §§12/12.1, current handoffs/runbook/WBS,
the complete independent audit, both literature investigations, competing
proposals, existing final design/annex/record and implementation evidence.
The three external publications above were checked against their official
records and relevant full-text passages. The τ²-Bench proceedings PDF was
downloaded and inspected outside the repository; no research binary is added.
This is a focused synthesis, not another exhaustive literature search or a
claim that every paper in the earlier reviews was independently reread here.

Verification for this new document is limited to local links/anchors, selected
external records, stage arithmetic and preservation of all pre-existing files.
No executable tests, model generation, software packaging or experimental
execution belongs to this documentation task.

All fifteen local links/anchors passed, and the 480+20=500 allocation reconciled.
A SHA-256 comparison found all 2,325 initially tracked or visible untracked
files byte-identical; this document was the only added repository file and
Git HEAD was unchanged. Ignored build/cache files were outside that inventory.
