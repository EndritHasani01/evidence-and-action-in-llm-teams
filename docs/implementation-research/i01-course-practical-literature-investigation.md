# I-01: practical lessons from additional scientific literature

16 October 2026. **Research and recommendations only; no adopted changes.**
This investigation follows the user's narrower objective: a scientifically sound,
manageable course project. It adds targeted full-paper research to the existing
review, without replacing it. No existing repository file, scientific contract,
implementation, prompt, configuration, scoring rule or result was changed. No
model was loaded, inference performed or GPU used.

Authority remains [PROJECT_SPECIFICATION.md §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime).
The recommendations below would need a later explicit adoption decision before
implementation or execution. Their presence in this document grants no authority.

## 1. Recommended direction for the course project

**Prioritize a usable, transparent agent environment and one fresh practical
retain/clear comparison. Do not make a new four-condition memory experiment a
prerequisite for completing the course project.**

The next question should be:

> Under one fixed, openly assisted coordination environment, how do literal
> retention and clearing affect both-agent exact recovery and effort after the
> specified maximum withdrawal?

First assess whether that environment is usable. A short task strategy deserves
earlier consideration than the previous recommendations allowed. Instructions
can explain how to exchange and combine local information while leaving the
actual numbers, messages, evidence use and final commitments to the agents.
Such assistance changes the behavioral condition and limits claims about
spontaneous coordination. It need not invalidate a practical history-policy
comparison when supplied identically from the start in both policies.

Three priorities follow:

1. Prepare one compact assistance package addressing legal actions, information
   boundaries, global submissions and finality; disclose any supplied strategy.
2. Use a small capability-oriented development battery and complete pilot
   conversations to assess its behavior. A scalar JSON screen is insufficient.
3. If useful, freeze that environment and evaluate retain/clear on new, fixed
   worlds. Preserve failures and accept a null. If it remains unusable, report
   a bounded feasibility result instead of repeatedly escalating complexity.

This differs from the earlier mechanism-oriented recommendation because the
objective has changed. Fixed-evidence/conclusion-exposure and edit/sham cells
remain a coherent option for a different question. They are not necessary to
estimate a carefully delimited **total history-policy effect** in a course
project. Neither direction has been experimentally compared here.

## 2. Starting point and research gap

### 2.1 Repository evidence used

The following were read as the starting evidence, rather than treated as new
findings of this investigation:

- [Independent Course-7 audit](../validation/i01-course-7-independent-scientific-audit.md),
  including the complete main evidence matrix and interpretation limits.
- [Experimental quality proposal](../proposals/i01-course-7-experimental-quality-improvement.md).
- [Targeted fifteen-paper review](i01-course-7-targeted-scientific-literature-review.md).
- [Literature-informed recommendations](../proposals/i01-course-7-literature-informed-recommendations.md).

Root `AGENTS.md`, specification §12, relevant implementation-plan/WBS sections,
README, technical synthesis, research navigation and relevant archived evaluation
notes supplied authority and context. The older four-agent design is not an
additional I-01 requirement. The current [core implementation](../../recovery/i01/core.py)
and [configuration](../../configs/i01-course.json) were inspected read-only.

The audit's relevant baseline is 2/20 recovery successes in each policy, 3/20
correct prefixes, and 60 illegal actions among 206 team calls despite valid
JSON. Main revised scalar controls succeeded on 15/20. These are distinct
limitations; improving only serialization cannot establish team competence.
[Audit §§5–6](../validation/i01-course-7-independent-scientific-audit.md#5-independently-reproduced-main-results).

Three canonical calls were also inspected directly using immutable read-only
SQLite connections:

| Call | Observed behavior | Specific research need |
|---|---|---|
| `main-01/prefix/agent-1/invocation-0` | Correct local 910 appears inside a rejected message-plus-wait action | Separate useful content from successful action execution |
| `main-08/clear/agent-1/invocation-0` | Empty history; record index 2 becomes “Partner submitted 2” | Test interpretation of environment metadata without stale history |
| `main-04/retain/agent-0/invocation-1` | Text recognizes global 959; committed submission is local 943 | Score and inspect the actual decision, separately from its explanation |

Records are in the [canonical Course-7 checkpoint](../../notebooks/run/course-7-working/latest/).
These are spot checks supporting the choice of literature, not a second full
audit or independently replicated human annotation study.

### 2.2 What this investigation adds

The existing review already covers stale conclusions, source preservation,
belief revision, structured decoding, self-correction and causal recovery.
Repeating that survey would offer little value. The remaining practical gaps are:

- Evidence about interface interventions that actually changed agent behavior.
- Whether explicit workflow assistance is useful, and when it backfires.
- How to distinguish success on supplied good histories from live interaction.
- How to make diagnostics informative without building another benchmark.
- How to match evaluation breadth and development cost to a narrow course claim.

Live searches followed these questions through official proceedings, ACL
Anthology, arXiv and author publication records. Seven additional papers were
selected. Six have independently verified peer-reviewed publication records;
one is treated as a preprint. This is a targeted investigation, not a systematic
review or an exhaustive novelty search. Broad protocol platforms, additional
memory frameworks and training methods were not pursued once they offered no
clear small intervention for the observed failures.

The archived evaluation notes already mention τ-bench reliability. Its inclusion
here is an independent full-text examination and a practical application, not
a claim that the underlying principle was previously unknown to the project.

## 3. What the additional papers establish

**Evidence convention:** “Reported” means an author-reported experiment, not our
reproduction. “Interpretation” identifies limitations or our inference. Page
numbers are one-based PDF pages for the versions in §9. No paper establishes
an expected improvement for our quantized Qwen3.5-9B/T4 environment.

### R1. SWE-agent: the interface is part of the experimental treatment

**Reported:** With a fixed base model, SWE-agent compares alternative commands,
feedback and context handling on SWE-bench Lite. Table 3, p. 6, reports 18.0%
resolved with its default interface, 15.0% without editing lint checks, and
12.0% with iterative rather than summarized search. Removing its demonstration
gives 16.3%. The development configuration search is described in §4 and
Appendix B.1, p. 25. These are component ablations, not universal design laws.

**Interpretation:** Coding includes execution feedback, syntax checks, many
turns and a demonstration. The default interface is a package, so the full
system gain cannot be attributed to clearer wording alone. Its context
compression and malformed-response handling (§3; Appendix C, pp. 39–44) differ
from literal I-01 retention and charged invalid turns. They cannot be copied
as neutral repairs. Single ablation differences also have limited uncertainty
analysis. [Proceedings and full text](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html).

**I-01 application:** Test a small agent-facing package before a model change.
Make rejection feedback identify the violated public action rule, while leaving
the rejection, charged turn and hidden truth intact. Do not copy retry loops or
history compression. A model's difficulty with an interface is an empirical
property of that interface/model combination, not automatically a software bug.

### R2. τ²-bench: useful workflows, imperfect causal decomposition

**Reported:** Telecom agents are evaluated with a user, with direct control of
all tools, and with an oracle action plan (§4.2). Figure 4, p. 7, reports
GPT-4.1 default success increasing from 0.34 to 0.52 under a workflow policy,
but its oracle-plan condition decreasing from 0.73 to 0.57. The setup uses 114
telecom tasks and four trials per task (§§3.2, 4.1). The “confusion” explanation
for the latter decrease is an author hypothesis, not an identified mechanism.

**Interpretation:** No-user changes control, observations, instructions and the
presence of a fallible user; subtracting its accuracy from default does not
identify a pure communication-error percentage. Oracle-plan supplies
task-specific correct actions, a stronger intervention than generic guidance.
Cross-domain simulator improvements are also observational comparisons of
different domains. Appendix C, p. 21, separates implementation/task verification
from performance evaluation. [ICML 2026 record and PDF](https://proceedings.mlr.press/v306/barres26a.html).

**I-01 application:** A short generic strategy is worth testing, with no promise
that more detail is better. Keep scalar controls as diagnostics and disclose
their different views. The two peers here are equal task participants, unlike
the expert/user asymmetry in τ²-bench; importing its simulator or oracle-plan
architecture is unnecessary.

### R3. AI Agents That Matter: development and generality have costs

**Reported:** Simple retry/warming baselines compete with more complex coding
agents when accuracy and cost are measured together (§2; Appendix A). They use
available example tests for stopping, rather than a hidden perfect verifier
(Appendix A.1, pp. 20–22). The HotPotQA study separates optimization expense
from deployment expense (§3; Table A3, p. 23); its endpoint is retrieval of
supporting documents, not final answer accuracy. §5/Table 1 distinguishes
in-distribution, distribution-shift, task and domain holdouts.

**Interpretation:** The inspected text is the July 2024 arXiv version; TMLR 2025
publication is independently verified, without asserting version identity.
Its API-price comparisons are historical. One robustness analysis excludes
unavailable time/cost for a hung task while marking it incorrect (p. 22), so it
is not a template for imputing I-01 missing costs. Its retry baseline requires
feedback unavailable to our agents. [Author publication record](https://www.cs.princeton.edu/~sayashk/publications.html),
[inspected full text](https://arxiv.org/pdf/2407.01502v1).

**I-01 application:** For a small project, extensive prompt optimization may
cost more than it saves. A fixed-generator claim needs fresh instances, not
another task family by default. Use this paper's evaluation principles without
introducing DSPy, optimization infrastructure or correctness-triggered retries.

### R4. Deliberative collaboration: tools do not guarantee correct decisions

**Reported:** Wang et al. evaluate 180 instances using seven models, a fixed
multi-module scaffold, centralized controls and optional mathematical tools
(§§2–4). The solver operates on an agent's **estimated** state (§2.2.5), not
automatically on evaluator truth. In task allocation, GPT-5.1's final decision
matches its final tool solution in 0% of cases in the reported compliance
analysis (Table 4, p. 7). Appendix C, pp. 17–18, gives a reasoning/final-action
contradiction and a case where local resource fragments are mistaken for global
limits. These examples illustrate possibilities, not their population frequency.

**Interpretation:** Exact tool agreement is not the same as answer correctness
or rational adoption. One fixed scaffold, larger models, visible reasoning,
multiple modules and up to six rounds limit transfer (Limitations, p. 9).
Full-information deliberation helps distinguish information from interaction
effects (Table 3), but also changes the computation available.
[Preprint record and full text](https://arxiv.org/abs/2607.06157v1).

**I-01 application:** A calculator or host-computed local maximum is not an
established remedy for the observed finality/source-use failures. Inspect
committed values. Do not require peers to independently verify remote data
that their permitted views do not contain, or treat disagreement as automatically
beneficial verification.

### R5. CheckList: test the required behaviors separately

**Reported:** CheckList organizes capabilities against minimum-functionality,
invariance and directional-expectation tests (§2, pp. 2–3). An 18-participant,
two-hour study compares unaided testing with capability guidance and templates
(§4.2, p. 8/Table 4). Guided participants find more behavioral problems. The
study tests a subset of the methodology, and bug-severity ratings involve
human judgment. It does not establish a reliability threshold or demonstrate
that fixing discovered cases improves held-out end-to-end accuracy.

**Interpretation:** These are mostly classification/comprehension systems,
not private-information recovery agents. Challenge examples complement rather
than replace natural evaluation (§5). An intended invariance must be justified;
changing an input's wording can change its meaning or task difficulty.
[ACL record and full text](https://aclanthology.org/2020.acl-main.442/).

**I-01 application:** Borrow the small capability matrix, not a test-generation
platform. Separate action forms, current-source reading, message uptake and
commitment. For any permutation/renaming probe, update record identities and
notice fields consistently. Keep such probes outside the main population;
passing hand-crafted cases does not certify live collaboration.

### R6. τ-bench: endpoint success and repeatability answer different questions

**Reported:** τ-bench uses final database comparisons and required information
checks, and distinguishes at-least-one success (`pass@k`) from all-trials
success (`pass^k`) (§3, pp. 4–5). Its best evaluated retail agent exceeds 60%
single-trial success but falls below 25% at `pass^8` (§5.1, pp. 7–8). Native
function calling outperforms its text-action comparators; adding a “think” tool
does not help that experiment (p. 7).

**Interpretation:** Both user and agent generation contribute variation. The
paper explicitly acknowledges that the endpoint can pass despite a missing
required confirmation (p. 5). Thus an outcome oracle does not establish all
desired process properties. Model/backend differences also prevent attributing
function-calling gains to JSON syntax alone. [ICLR 2025 full text](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf).

**I-01 application:** Preserve exact team success as primary and report protocol
behavior separately. Identical saved-response replay tests reproducibility;
independent generation repetitions test repeatability. Neither best-of-several
selection nor exponentiating the aggregate 2/20 score estimates I-01 reliability.
A dedicated repeated-trial study is optional, not another course requirement.

### R7. FlowBench: supplied good histories can overstate readiness

**Reported:** Static evaluation supplies the ground-truth previous conversation
at every turn; session evaluation lets predicted actions accumulate (§4.3,
pp. 6–7). Workflow formats generally help, but their ranking depends on the
endpoint: GPT-4o single-scenario session success is 35.1% without workflow,
41.7% with text, 43.2% with code and 42.7% with flowchart (Table 4, p. 7).
Small-Qwen results in Appendix B.5/Table 10, pp. 13–14, are static, not live
session results. Appendix C.1 reports three experimental repetitions.

**Interpretation:** Sessions, user summaries and several judgments involve
GPT-4; tool-string matching can use fuzzy LLM judgments (pp. 7, 14). Therefore
its success measures differ from exact I-01 submissions. The evidence does not
establish flowcharts as universally superior, and numerical gains cannot be
transferred to our model. [Findings of EMNLP 2024 record and PDF](https://aclanthology.org/2024.findings-emnlp.638/).

**I-01 application:** A static good-history action probe is useful diagnosis,
but cannot replace complete multi-turn pilots. Start with a short readable
procedure; a flowchart, ensemble of representations or repeated planner is not
justified merely by the paper's headline.

## 4. Integrated lessons that change our decisions

### 4.1 Earlier strategy assistance is defensible for this objective

The earlier proposals rightly distinguish clarification from teaching the
algorithm. The additional evidence strengthens a practical alternative:
**supply a small, generic coordination strategy openly**, if the course question
concerns recovery rather than discovery of distributed maximum computation.
R1, R2 and R7 support testing assistance; none proves our particular strategy
will work. The recommendation is our judgment about scope and cost.

There are three different interventions:

| Intervention | What the agent is supplied | Resulting interpretation |
|---|---|---|
| Clarification | Meaning of legal actions, sources, notices, privacy and finality | Coordination under a clearer environment |
| Strategy assistance | A generic way to exchange, combine and communicate maxima | Recovery with supplied task strategy; autonomous execution remains tested |
| Enforced workflow | Host prevents submission until prescribed exchanges occur, or computes/corrects values | A different protocol or delegated computation, requiring a different claim |

The first two can be a single practical package. If tested together, call it
a package; do not attribute its benefit to one sentence. A head-to-head study
of clarification and strategy would be needed to isolate their marginal effects,
but that attribution need not be a course deliverable.

### 4.2 Assistance must leave something meaningful for retention to do

An apparently helpful instruction can undermine the experiment. Requiring
everyone to discard previous reports and exchange all current maxima from
scratch after every edit suppresses a potential reuse benefit by design.
Requiring both agents to receive a new message before every submission has a
similar problem: a retained report from an unchanged peer can already be useful.

For example, the changed owner may retain the other peer's original maximum.
That peer's shard did not change. If the report was accurate, the changed owner
can combine it with its own current maximum and tell the partner the new result.
The harness cannot certify the report, but it need not prohibit the agent from
using it. Conversely, an old maximum reported by the changed peer cannot simply
be presumed current after the winning record is withdrawn.

The candidate should therefore teach **adequate information before irreversible
commitment**, while leaving the choice of reuse, rechecking and messages to the
agents. Do not mandate a fixed call count or a fresh broadcast every phase.
Identical guidance belongs in the initial instructions and both continuations;
neither policy should receive additional strategy only after failure.

This still changes the scope of the finding. A null under an effective strategy
could mean that the assistance makes history less consequential in this short
task. That is an acceptable bounded result, not a reason to weaken assistance
until a preferred history effect appears.

### 4.3 Better control conditions are not necessarily more control arms

R2 and R4 show why centralized controls are useful and why they are not a pure
causal decomposition. Course-7's scalar control has all forty numbers, a scalar
prompt and no peer-finality problem. Its advantage over team accuracy mixes
information access, interaction, prompting and sampling. It is not an estimate
of “percentage of failures caused by communication.” Nor is a model's scalar
accuracy a mathematical upper bound on team success.

Use a few diagnostic views to localize the next design choice. Do not create
centralized, oracle-peer, oracle-plan, calculator, structured-memory and sham
main arms simultaneously. A deterministic legal exchange can establish that the
bounded task is solvable; only model execution can establish behavioral
competence. Those two evidential roles should remain separate.

### 4.4 Development should test the action, then the interaction

R5 supplies a useful methodology and R7 a crucial warning. A model can choose
the right action when given a correct supplied transcript, yet fail to produce
that transcript in live interaction. Test both, with different labels.

One proportionate diagnostic allocation is **eight single-call probes**, two
per family below. These are proposed diagnostic fixtures, not constructed or
executed tests. They need fresh examples and a fixed acceptable-action rubric.

| Family / two probes | Specific question | Scoring and limitation |
|---|---|---|
| Public action rules | Can it express a requested message-only action and a requested wait-only action? | Strict field/action checks; obeying an explicit request does not establish spontaneous action choice |
| Source and notice interpretation | Can it read the current local maximum; can it distinguish a record index/replacement from a peer answer? | Exact local arithmetic and literal notice facts; local-query prompting differs from the team task |
| Received information and finality | Given permitted scripted reports, does it combine maxima and commit to the global rather than local value in either winner placement? | Exact final submission; expose reports only through lawful local histories; not naturally acquired collaboration |
| Historical validity | Does it reconsider the changed owner's former report while preserving an unaffected peer report in matched withdrawal examples? | Use actual original/current data to audit claims; preservation concerns that report, not an unchanged global answer |

The last family can use the existing answer-changing withdrawal mathematics;
it does not require inserting a no-change event. Reports must be ordinary
historical claims, without evaluator certification or hidden revised values.
Predetermined fixtures can deliberately expose an old correct report. That is
declared diagnostic scaffolding, not evidence that the model produced it.

If an action has several adequate realizations, accept all of them under the
predeclared rule. Do not use a single reference string as the only correct
communication strategy. Do not award team success for a partial probe.
These probes also cannot measure robustness from just one case per behavior.

Then inspect complete original/retain/clear pilots. New illegal-action loops,
locally refutable values and reasoning/submission contradictions remain visible
failures. A probe pass cannot waive them or any runtime/integrity gate.

### 4.5 Match generalization and reliability claims to the actual sample

For the recommended question, fresh instances from the same mathematical
generator are an appropriate first holdout. R3's wider holdout requirements
apply when claiming wider generality. A second task, second model, long-term
memory system and adversarial revision distribution are not prerequisites for
a narrow course finding.

Original Course-7 examples and all inspected pilot worlds are development
evidence permanently. New seeds should be accompanied by actual input-overlap
checks. Freeze the held-out list before model-guided development, keep its
contents out of examples, and do not retune after seeing its continuations.

If repetition later becomes the main question, distinguish two targets:

- Several continuation seeds from one fixed prefix measure conditional
  continuation variation under that one realized history.
- Independently regenerating original teams measures variability of the
  complete prefix-plus-recovery process.

They are not interchangeable. Retain sibling grouping and cluster repeated
observations by world. Reporting all repeated outcomes is different from picking
the best one. With the current resource limit, repetitions should replace part
of a prospectively selected scope, not be silently appended to it.

## 5. One candidate package, with explicit boundaries

This is a design description, **not a replacement prompt or implementation**.

| Ingredient | Purpose in I-01 | Boundary protecting interpretation |
|---|---|---|
| Unambiguous action documentation and small legal examples | Address message/wait incompatibility and real JSON nulls | Keep strict rejection, charged turns and legal send-and-submit |
| Explicit global endpoint and private finality | Prevent “my maximum completes my turn” and impossible later adjustment | Both agents still choose and commit their own answers |
| Clear separation of current shard, environment event and dated history | Reduce notice-as-answer and stale-invocation confusion | Preserve literal message text, owner-only replacement visibility and policy difference |
| Short generic coordination strategy | Explain exchanging sufficient local information, comparison and informing the partner | No worked held-out worlds, host maxima, hidden eligibility, forced fresh exchange or correctness feedback |
| Specific bounded legality feedback, if included | Make repeated rejected combinations diagnosable | Identify only the public violated rule; no repaired action, extra turn or gold-dependent warning |

Static common instructions can illustrate a legal exchange on an unrelated
example, but an example adds demonstration effects and copying opportunities.
The first candidate should use the shortest strategy description that is clear.
If a worked example is necessary, label it as a demonstration, use independent
values, and record that it is part of the package. Neither old success rates
nor the new papers establish an optimal prompt length or representation.

Current shards must remain raw permitted sources. Providing a deterministic
local-maximum tool would remove part of the measured task; even a perfectly
computed local value would leave aggregation and finality unresolved. Similarly,
requiring an extra reasoning field or another model call would change the
interface/computation rather than merely clarify it. Neither is a default here.

The pinned model, runtime, output bounds and mathematical distribution should
remain the same for this first candidate. They are not known to be optimal;
holding them fixed makes the initial investigation manageable and its changes
inspectable. Runtime health and scalar errors still deserve separate reporting.

## 6. Priorities and competing approaches

Ranks reflect usefulness for this course objective, not a quantitative estimate
of expected gain. Support concerns the reason to test, not proven I-01 efficacy.

| Rank | Approach | Evidence / likely value | Cost and main confound | Recommendation |
|---|---|---|---|---|
| 1 | Exact outcome/process reporting and a small trace casebook | Course-7; R5/R6. Immediate interpretability | Low, saved-data work; labels need observable criteria | Essential; preserve original primary scoring |
| 2 | One common assistance package, including a disclosed short strategy | R1/R2/R7; direct finality/action failures | Small prompt/rendering work later; package effect, supplied competence | First performance candidate |
| 3 | Small static diagnostics plus complete live pilots | R5/R7; tests qualification-task mismatch | Bounded calls; scripted histories and local queries are diagnostic conditions | Use before a new main study |
| 4 | One fresh natural-prefix retain/clear evaluation | Closest to §12's practical question | Up to 19 calls/world; information and presentation remain bundled | Preferred course follow-up if usable |
| 5 | Clarification alone versus clarification plus strategy | Separates whether task guidance matters | Additional development arm; small samples give weak attribution | Useful alternative if spontaneous coordination is central |
| 6 | Controlled source/conclusion histories and edit/sham | Existing review's stronger identification for another question | Four continuations/world; new representation, population and estimand | Optional replacement direction, not an additional requirement |
| 7 | Exact legal-action decoder or discriminated tool interface | Existing review on structured output; R1/R6 | Backend/qualification work; changes action distribution without ensuring correct decisions | Consider only if residual illegality remains dominant |
| 8 | A different model or reasoning mode | Capability remains plausible; no matched I-01 evidence | Requalification, memory/time and model/interface confounding | One conditional alternative, not a model sweep |
| 9 | Reflection/debate loops, solvers, provenance graphs or learned memory repair | Different supervision/information assumptions | Extra calls, supplied reasoning, new errors and implementation burden | Defer for this course project |

Automatically fixing invalid actions, scoring message prose as the submission,
or feeding the hidden maximum back to agents are excluded. These would undermine
the proposed interpretation rather than demonstrate agent improvement.

### What to reconsider in the existing recommendations

| Existing position | Course-focused reassessment |
|---|---|
| Prioritize the fixed-evidence four-cell mechanism design | Optional. Its identification benefit matters only if that mechanism is the chosen question |
| Defer algorithm assistance until clarification fails | Too conservative as a universal rule. A clearly disclosed generic strategy is a reasonable first course candidate |
| Preserve useful evidence while removing old conclusions | Still valuable conceptually, but natural retain/clear can remain a deliberately bundled practical comparison |
| Add a sham to establish revision specificity | Necessary for that stronger claim; unnecessary if the claim is explicitly restricted to the adopted withdrawal event |
| More capable agents automatically improve the recovery study | Qualify. Mandatory full recomputation or forced communication may remove the behavior the policy comparison is meant to measure |
| A larger study is needed before the course work is meaningful | Reconsider. A well-documented feasibility failure or small paired null can be adequate with appropriately narrow claims |

None of these judgments rewrites the previous documents. Their distinct
questions and dated recommendations remain available for a later decision.

## 7. A proportionate prospective study

### 7.1 Separate usability from the policy estimate

The smallest next execution, if later authorized, is a fixed candidate's
diagnostics and live pilots. Freeze its content before these calls. Use fresh
development worlds and preserve every result. Decide whether the environment
is useful enough to justify main, independently of which policy benefits.

A concrete **provisional course-usefulness rule** is at least two correct
original teams among three pilots and at least five correct original/revised
scalar controls among six, with complete inspectable traces and intact integrity
evidence. These numbers are project judgments intended to avoid another study
dominated by unusable starting histories; they are not thresholds established
by a paper, and such tiny samples cannot certify population reliability. The
eight probes remain diagnostics, not a fabricated aggregate competence score.

Adopt or replace that rule before any new outcomes. Review recurrent notice,
source and finality failures even when aggregate thresholds pass. If they make
the intended interpretation untenable, stop at feasibility and explain why;
do not loosen the rule or repeatedly tune until the same pilots pass. Main must
then use a new, untouched fixed cohort. Ordinary main failures remain outcomes,
not a reason to stop or substitute worlds.

This is a prospective scientific-usefulness decision, distinct from runtime
health gates and the existing recorded-outcome admission policy. Adopting it
would require an explicit amendment. It cannot retroactively turn Course-7's
pilots into failures under a rule they did not use.

### 7.2 An allocation that preserves the twenty-world course scale

One possible new independent campaign, assuming **one resident load/session**,
has the following worst-case attempt arithmetic:

| Scope | Maximum physical attempts |
|---|---:|
| Current-load state/hardware checks, including two envelopes | 8 |
| Existing-style twelve scalar qualification calls | 12 |
| Eight focused diagnostic calls | 8 |
| Three full pilot worlds: prefix, both recoveries, two scalar controls | 60 |
| Twenty held-out worlds: prefix, both recoveries, revised control | 380 |
| Reserve for explicitly eligible interruptions/requalification | 28 |
| **Total planned ceiling including reserve** | **496** |

The 19-call main bound is `6 + 6 + 6 + 1`; the 20-call pilot bound adds an
original scalar control. These are maxima, not expected spending. No new model
calls were made to obtain this arithmetic. The four remaining attempts below
500 are unallocated, not permission for extra examples or tuning. Actual work
can terminate earlier procedurally, without expanding the cohort.

This option adds diagnostic types and a new usefulness decision. It is **not**
an existing authorized schedule or permission to repurpose Course-7's remaining
allowance. Its qualification allocation and diagnostic views would need explicit
adoption, even though the numerical total fits 500. Retrying a wrong or illegal
answer is not reserve-eligible. An additional full preparation cycle could
exceed the ceiling; reforecast and adjust scope prospectively rather than skip
required current-load checks. The exact candidate's time/resource feasibility
must be measured on the actual host before main authorization.

This design evaluates one candidate. It does **not** causally establish how much
better its prompt is than Course-7: different worlds and execution conditions
also differ. Course-7 supplies a historical reference. If identifying the
package's performance effect is the primary objective, spend the limited budget
on a matched baseline/candidate development comparison instead, followed by a
smaller fresh confirmation cohort. The earlier
[two-environment development proposal](../proposals/i01-course-7-experimental-quality-improvement.md#8-proportionate-validation-plan)
already provides that alternative; do not run both complete campaigns merely
to accumulate evidence.

### 7.3 Freeze, assignment and evaluation

Before new development, set aside the held-out world list and a new master
seed; verify disjoint actual inputs from all exposed studies and examples.
Before main, freeze one candidate, model/runtime, input distribution, literal
history transformation, schedule, scoring, effort definitions and analysis.
Changing the candidate after pilots requires a new development version and
unexposed validation; it cannot silently remain the same confirmation study.

Keep natural one-shot prefixes and all intended main worlds, including failed
prefixes. Retain/clear must start from the exact same saved prefix, with the
same current sources and notice policy, independent hidden state and separate
continuation replies. Keep siblings on one device and counterbalance treatment
order independently of device and owner/first-speaker blocks. Matched seeds
are useful coupling, not response reuse or proof of identical stochasticity.

The report should have a small number of clearly separated displays:

1. **Primary:** all-world exact both-agent recovery, four paired outcome counts,
   clear-minus-retain difference, coverage and world-level uncertainty.
2. **Readiness/context:** original success, full-information controls and
   correct-prefix descriptive results, with their actual denominators.
3. **Process:** illegal actions and episodes affected, delivered useful reports,
   locally refutable submissions, notice confusion, stale-answer repetition
   and source/action contradictions. Use exact checks where possible and a
   small trace-linked human casebook where interpretation is required.
4. **Effort:** all attempted calls/tokens/ready time, including failures, with
   loading/setup separate. Show paired effort and success together.

Keep the world as analysis unit. Calls and the two agents are dependent, and
action counts have behavior-dependent denominators. Do not turn lower illegal
call percentages into an independent-binomial significance claim. Mark
unexecuted/unresolved outcomes unknown; recorded terminal failures are zero.

Preserve the historical Course-7 interval and scoring. For a new study, choose
the paired uncertainty procedure in advance and disclose small-sample/degenerate
stratum limitations. A twenty-world course study is too coarse to establish a
modest advantage or equivalence reliably. Displaying the complete paired table
is more informative than multiplying exploratory tests or bootstrap draws.

Do not condition primary results on legal continuations, completed teams or
correct controls. A correct-prefix subset is secondary and changes the target
population; recovery-time success-only summaries introduce further selection.
Never score old-answer avoidance, agreement or explanatory fluency as recovery.

### 7.4 Results that should change the decision

| New evidence | Defensible conclusion | Next action |
|---|---|---|
| Static probes improve but live originals remain poor | Supplied-context competence does not transfer to interaction | Stop this candidate at feasibility; inspect the remaining visible bottleneck |
| Action legality improves but global/finality failures persist | Interface usability improved without adequate collaboration | Do not call the recovery experiment qualified by formatting alone |
| Scalars remain poor, including current local-source probes | Capability/source reading is still a bottleneck | Consider one separately qualified model/reasoning alternative, or report the limit |
| Useful originals and controls; both policies recover well | A small or null total policy contrast under this assistance is informative | Report it; no need to manufacture harder tasks or stale-history effects |
| Useful originals; both recoveries fail | Revision-stage behavior remains problematic under the tested environment | Preserve the paired result and trace diagnosis; avoid a larger identical campaign |
| Retain/clear differ on fresh worlds | Evidence for this total policy contrast, with finite-sample uncertainty | Inspect both helpful and harmful cases; do not infer pure memory or anchoring |
| Integrity, privacy, persistence or resource evidence fails | Scientific outcome coverage may be incomplete | Stop admission and preserve known/unknown distinctions |

If substantial natural collaboration cannot be elicited within the bounded
development effort, the course can finish with a rigorous failure/feasibility
study. Alternatively, an explicitly supplied-history experiment can replace
the natural target. It should not be added as an unlimited rescue campaign or
described as naturally acquired competence.

## 8. What requires a later decision

| Category | Example | Status here |
|---|---|---|
| Engineering/reporting repair | More precise derived labels or a demonstrated persistence defect | No underlying runtime defect was established; no repair implemented |
| Behavioral intervention | Clearer notices, rule feedback, legal examples, short strategy | Proposed common condition; not adopted or tested |
| Diagnostic regime | Scripted local histories and local-query probes | Proposed measurement assistance; separate from natural main outcomes |
| New main regime | Controlled source/conclusion packets, sham reopening, enforced stages | Optional alternative question; explicit new semantics/estimand required |
| Contract amendment | New prompt version, diagnostic allocation, usefulness decision or assignment | User decision before implementation; existing authority unchanged |

There is no current case for replacing the two-worker persistence/runtime system,
adding a memory service, building a provenance graph, training a supervisor or
developing another evaluation framework. The scientific payoff comes from a
small declared intervention, usable controls, a clean holdout and honest limits.
That is sufficient ambition for this stage of the course project.

## 9. Verified bibliography and full-text access

Records checked live on 16 October 2026. All seven selected works have obtained
full PDFs. Relevant methods, results, ablations, implementation details and
limitations were read; this does not claim line-by-line reading of every long
appendix or example trajectory. Locators above refer to these exact versions.

1. **R1 — John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret,
   Shunyu Yao, Karthik Narasimhan, Ofir Press.** *SWE-agent: Agent-Computer
   Interfaces Enable Automated Software Engineering.* **NeurIPS 2024**.
   [Publication record](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html),
   [conference PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf).
2. **R2 — Victor Barres, Honghua Dong, Soham Ray, Xujie Si, Karthik R
   Narasimhan.** *τ²-Bench: Evaluating Conversational Agents in a Dual-Control
   Environment.* **ICML 2026**, PMLR 306:6736–6782; initial preprint 2025.
   [Publication record](https://proceedings.mlr.press/v306/barres26a.html),
   [conference PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/barres26a/barres26a.pdf).
   A search also found an earlier ICLR submission listing; the verified final
   publication used here is ICML, not an inferred ICLR acceptance.
3. **R3 — Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir,
   Arvind Narayanan.** *AI Agents That Matter.* **Transactions on Machine
   Learning Research, 2025**. [Journal record](https://openreview.net/forum?id=Zy4uFzMviZ),
   [author publication record](https://www.cs.princeton.edu/~sayashk/publications.html),
   [inspected arXiv v1, 1 July 2024](https://arxiv.org/pdf/2407.01502v1).
   OpenReview download returned 403; the obtained preprint is not asserted to
   be identical to the later journal text. No uninspected final-version result
   is used. A journal PDF would be useful for a final-version comparison, but
   is not necessary for the bounded recommendations here.
4. **R4 — Chenxu Wang, Yongkun Yang, Boyuan Du, Shiwei Lin, Huaping Liu.**
   *LLM Agents for Deliberative Collaboration: A Study on Joint Decision Making
   Under Partial Observability.* **Preprint**, arXiv:2607.06157v1, 7 July 2026.
   [Record](https://arxiv.org/abs/2607.06157v1),
   [PDF](https://arxiv.org/pdf/2607.06157v1). No peer-reviewed venue was verified.
5. **R5 — Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, Sameer Singh.**
   *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.*
   **ACL 2020**, pp. 4902–4912. [Record/DOI 10.18653/v1/2020.acl-main.442](https://aclanthology.org/2020.acl-main.442/),
   [PDF](https://aclanthology.org/2020.acl-main.442.pdf).
6. **R6 — Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan.**
   *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.*
   **ICLR 2025**; initial preprint 2024.
   [Conference record](https://openreview.net/forum?id=roNSXZpUDN),
   [obtained conference PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf).
   OpenReview returned 403; official ICLR proceedings supplied the full text.
7. **R7 — Ruixuan Xiao, Wentao Ma, Ke Wang, Yuchuan Wu, Junbo Zhao,
   Haobo Wang, Fei Huang, Yongbin Li.** *FlowBench: Revisiting and Benchmarking
   Workflow-Guided Planning for LLM-based Agents.* **Findings of EMNLP 2024**,
   pp. 10883–10900. [Record/DOI 10.18653/v1/2024.findings-emnlp.638](https://aclanthology.org/2024.findings-emnlp.638/),
   [PDF](https://aclanthology.org/2024.findings-emnlp.638.pdf).

| Reading version | Pages | Principal inspected material |
|---|---:|---|
| R1 NeurIPS proceedings | 125 | §§2–5 pp. 2–8; interface/design pp. 16/18; development sweep p. 25; repetition p. 35; prompts/history/error handling pp. 39–44; limitations p. 117 |
| R2 ICML proceedings | 47 | §§3–4 pp. 4–9, Figure 4 p. 7; verification/prompts pp. 21–22; original/workflow policy comparison in Appendix E.2; arXiv v1 initially read for orientation |
| R3 arXiv v1 | 33 | §§2–6 pp. 2–11; Appendix A pp. 18–23, stopping feedback, robustness and fixed/variable costs |
| R4 arXiv v1 | 22 | §§2–4 pp. 2–8; limitations p. 9; diagnostics pp. 15–16; case studies/prompts pp. 17–18 |
| R5 ACL proceedings | 11 | §2 pp. 2–3; task examples and results pp. 4–7; user studies pp. 7–8; scope limits p. 9 |
| R6 ICLR proceedings | 53 | §§3–5 pp. 3–9; endpoint/reliability definitions pp. 4–5; limitations p. 10; original arXiv methods/appendix initially inspected |
| R7 EMNLP Findings proceedings | 18 | §§3–5 pp. 3–8; limitations p. 9; failure analysis pp. 12–13; Qwen/judge validation p. 14; prompt and scoring details p. 15 |

The original SILO-BENCH remains the task precedent, already analyzed in the
existing review: [verified ACL 2026 record](https://aclanthology.org/2026.acl-long.1354/).
Its native mathematics is reference material; §12 defines our evaluation and
execution semantics. No additional native-benchmark or general multi-agent
superiority claim follows from the proposed course study.

Research materials are organized outside the repository in
`C:/Users/EndritHasani/Downloads/i01-course-practical-research-2026-10-16/`,
with selected PDFs, page-marked extracted text and retrieval notes. No binary
research material or executable helper was added to the repository. Links and
reading versions above make the investigation usable without that local cache.

Delivery checks found no broken local paths/anchors. Sixteen distinct external
URLs were checked; OpenReview records can show browser challenges, with the
full-text alternatives documented above. R1 Table 3, R2 Figure 4 and R7 Table 4
were rendered and visually checked against the quantitative claims. A final
preservation comparison found all 2,311 initially tracked files byte-for-byte
unchanged. The only new repository artifact is this Markdown document.
