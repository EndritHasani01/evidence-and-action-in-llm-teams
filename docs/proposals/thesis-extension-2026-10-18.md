# Thesis extension: historical evidence, old conclusions, and completed recovery

**Decision proposal · 18 October 2026 · not adopted or execution-authorized**

This proposal builds on the repository at `005a456cda4cba54cff36084a125dc883bb5ba8a`.
The [specification](../../PROJECT_SPECIFICATION.md) remains the sole scientific
authority. The [evidence review](../analysis/thesis-extension-evidence-review.md)
establishes the implementation, empirical findings, literature, and model facts
behind the choices below. The [roadmap](../plans/thesis-extension-roadmap.md)
defines the work and approval gates. No proposed condition is implemented here.

## 1. Recommended study and contribution

Study **when historical source evidence helps a distributed team recover, and
whether explicitly retaining its formerly correct conclusion changes that
benefit after a real source revision**. Evaluate Qwen3.5-9B and IBM Granite
4.2-8B separately under one common, bounded two-agent task and action protocol.

The main study uses controlled, legally reachable historical packets, three
memory conditions, actual withdrawal and no-change continuations, and two
independently seeded trials of every cell. A small, separate natural-history
study checks transfer to histories the models actually produce. A fixed real
answer-preserving edit subset checks whether an announcement of change causes
unnecessary answer changes. These checks are subordinate to one main question;
they are not a full factorial across provenance, edit types, tasks, and teams.

**Recommended target:** 128 independent controlled worlds, two trials per cell,
both models; 32 separate natural-history worlds; 32 predetermined controlled
worlds with one additional answer-preserving probe. The resource fallback is
96 controlled worlds, keeping the other fixed scopes. Select the size before
main inference using resources alone. Proposed limits are **200 additional
aggregate allocated GPU-hours and 24,000 new physical attempts**, with smaller
stage limits below. These require explicit adoption; the existing 100-hour
thesis plan does not silently become a new allowance.

The contribution would be an exact, reproducible account of three separable
questions: what historical evidence remains available, how an old conclusion
affects behavior at a fixed evidence basis, and whether agents turn available
information into two correct commitments. It is an empirical study of bounded
distributed recovery, not a new memory architecture or proof of internal
anchoring. An accurately measured null, useful-history benefit, failure of
source use, or model-dependent effect would all be meaningful outcomes.

## 2. Why this direction, rather than the original matrix

The course campaigns identify a competence and interpretation problem before
they identify a winning recovery policy. In the assisted campaign, retain
achieved 2/20 exact recoveries and clear 3/20; the exploratory difference was
+5 percentage points with interval [−15,+25]. Original teams succeeded on
10/20 and revised scalar controls on 18/20. Thirty-two of 35 failed recoveries
used entirely legal actions. Correct reports sometimes circulated without a
submission; visible local values were attributed to remote records; correct
prose did not reliably become the submitted integer. No recovery submission
equalled the withdrawn maximum. The older campaign had a different failure
profile, including substantial obsolete-answer repetition. Neither campaign
had a matched no-change reopening. These are observed findings, not causal
effects of assistance or evidence that stale conclusions are harmless.

| Alternative | Scientific strength | Main weakness here | Decision |
|---|---|---|---|
| Execute the existing five-family, four-peer thesis twice | Rich trajectories, retained work, receipts, and identified teammate-reset effects; substantial CPU implementation exists | At least 32,304 distinct target main generations before two-model pilots; long-context and model competence remain unaccepted; many secondary comparisons divide attention | Preserve as an implemented research asset; exclude from this main campaign |
| Reduce that design to Prefix Sum and Top-K with B/C/K and mixed resets | Meaningful update-sufficiency contrast; reuses the synchronous runner | Four-peer competence is unknown after two-peer failures; different output shapes and long literal histories add admission risk; reduced family samples weaken conclusions | Best later task-generalization study, not the first thesis extension |
| Natural retain/clear × revision/no-change only | Clean practical package comparison; closest continuity with course work | Useful evidence, wrong conclusions, successful acquisition, length, and wording remain bundled; unsuccessful prefixes can dominate | Use a fixed natural-history bridge, not the main identification design |
| Controlled sources with/without old conclusion × revision/no-change | Holds the historical evidence basis fixed; distinguishes correction from warranted persistence | Artificial starting histories; explicit conclusion remains derivable from sources; presentation and length are part of treatment | Select as the main comparison |
| Add empty history to the controlled comparison | Tests whether useful historical reports help at all, rather than assuming they do | Adds two cells and measures a larger information/presentation package | Include: this is the only extra main memory condition |
| Replace finality with provisional synchronous answers | Removes premature commitment and noncompletion as bottlenecks | Changes the research target and loses the course's concrete decision failure; would not show reliable commitments | Do not adopt in this study |
| Add a solver, forced exchange, constrained decoding, supervisor, or repair router | Could improve operational success | Supplies new competence or changes response distribution; would obscure whether agents use evidence and finish | Exclude; any such intervention needs another declared condition |

The source/conclusion distinction and paired recovery are established ideas.
Reclaim, ICR, StateAuditor, and recent evidence-revision work limit novelty
claims. The useful extension is **previously correct conclusions, actual private
source changes, subsequent team interaction, private irreversible commitments,
and repeated evaluation in two model systems**. Novelty depends on execution
and continued literature checks, not the combination of labels alone.

## 3. Task, population, and information boundary

### 3.1 Keep I-01 deliberately

Use two agents with twenty integers each, independently proposed uniformly in
−1000…1000. Both must submit the exact maximum across both shards. Preserve
the course withdrawal population: a unique old global maximum at record `r`,
remaining maximum `M2 > −1000`, and replacement sampled uniformly from
`[−1000,M2−1]`. Condition generation on the preassigned old-winner owner,
using the existing bounded rejection procedure and separate rejection counts.
Save actual arrays and edits. Never reject a world using a model outcome.

Maximum is appropriate because the difficult behavior is evidence interpretation
and coordinated commitment, while the answer and local refutations are exact.
An old maximum can omit the runner-up needed after withdrawal; historical raw
reports preserve that alternative. Extra arithmetic difficulty would obscure
the source-use question. The limitation is equally important: this study cannot
establish savings from preserving expensive computation or task-general recovery.
The existing Prefix/Sort/Top-K/BFS CPU witnesses explain possible information
boundaries, but are not additional empirical task results.

### 3.2 Three historical packets

Construct one short, correct, **scripted** original exchange per controlled world:

1. The assigned first speaker sends its complete indexed original shard as
   ordinary text and does not submit.
2. The other agent sends its complete indexed original shard and submits the
   old global maximum, which it can compute from its permitted information.
3. The first speaker submits that maximum after receiving the second shard.

This fits the existing per-agent invocation bound if tokenization succeeds.
It is a CPU fixture, not a model-generated prefix or physical inference attempt.
Retain its explicit scripted provenance. Each agent may receive only reports
and its own submission that this exchange made visible to it. The host never
pretends the models naturally acquired this information.

Build the following packets using one fixed rule, without consulting future
model outputs:

| Analysis label, never shown to agents | Historical source reports | Earlier own submission |
|---|---|---|
| H0: empty | Absent | Absent |
| HS: sources | Both indexed original shard reports from the script | Absent |
| HSC: sources plus conclusion | **Exactly the same source-report bytes as HS** | The agent's actual scripted old submission, labelled historical |

Reports contain sender, record owner/index, and original values, but no computed
maximum, recommendation, update formula, or duplicate conclusion sentence.
HS/HSC supply the same old raw evidence, including the old winning value. The
conclusion is mathematically redundant: the treatment tests **explicit old
conclusion exposure**, not whether the number can be reconstructed. HSC adds
the conclusion in a separate fixed field; H0/HS have an absent value there.
Use no length-padding arm. Accordingly, its effect includes salience, repetition,
and the small text-length difference; it is not a pure psychological mechanism.

These are new controlled representations. HS is not the old thesis policy F,
HSC is not literal natural retain, and H0 is not a full fresh restart. Do not
reuse those historical policy names or pool their results.

Current private shards remain separately authoritative. Historical reports are
accurate records of the original exchange, **not certified current sources**.
After withdrawal, one of their records is obsolete. No remote record is refreshed
by the host; no current remote shard or revised answer is supplied. The changed
owner can read its replacement; its partner must obtain adequate information
through permitted interaction. The hidden rule that the replacement cannot
win stays hidden, even if a model notices a pattern across task descriptions.

### 3.3 Events and the six main cells

Each packet has two isolated continuations from its original starting snapshot:

| Event | Current private data | Persistent public information | Purpose |
|---|---|---|---|
| Withdrawal | One winning record replaced by the saved lower value | Changed owner and record; replacement value to owner only | Actual recovery |
| No change | Original shards unchanged | Explicit neutral statement that no source changed; both agents may submit again | Generic reopening, memory, and additional-interaction control |

Every event resets phase submissions, waiting flags, invocation counters, and
current-phase delivery state in the same prescribed way; historical submissions
are data, never active final answers. The event notice survives all memory
conditions. A sham must not falsely announce a replacement, expose a selected
future edit, or broadcast a previously unseen record. The event is necessarily
visible; the scientific condition name and expected effect are not.

Run H0/HS/HSC under both events: **six cells**, not a receipt or reset-mask
factorial. Match current private sources within each event and packet field
positions across conditions. After the boundary, all cells accumulate ordinary
new visible history under the same rules. No ongoing summarization or selective
deletion occurs.

## 4. Preserve the meaningful action and team problem

Use the existing assisted I-01 public strategy and source-authority instructions,
with only the common wording needed to describe supplied historical reports and
the two event notices. Both models and every condition receive the same task,
coordination hint, action examples, and absence of numerical feedback. Freeze
the complete text before development calls; any later revision is a new version.

Keep exactly `message`, `submit`, and `wait`; strict JSON and integer validation;
no message or submission with `wait=true`; no empty non-wait action; private
submissions; send-and-submit delivery; finality within a phase; waiting that
wakes on a delivered message; at most three invocations per agent; and stopping
on completed submissions, exhausted opportunities, or inability to progress.
The first-speaker assignment is the same across a world's siblings. Public-rule
feedback can explain rejection on a later eligible turn, but cannot add a turn,
correct a maximum, certify a peer claim, or reopen a premature commitment.

This retains the course's substantive team decision problem. Synchronous
provisional candidates would answer another useful question, but would remove
the very distinction between saying the answer and committing it. We measure
that distinction rather than fixing it with host logic.

Preserve independent episode state and fresh model KV/recurrent state per call;
exact persisted-outcome resume; persist-before-effects; idempotent delivery;
one identical infrastructure retry only without a durable outcome and after
confirmed termination; and zero retries for wrong, invalid, truncated, or recorded
timeout outcomes. There is no cross-condition response replay in this design.
Matched seeds are a sampling coupling, never permission to copy an answer.

## 5. Sampling, repetition, and the two bounded checks

### 5.1 Main controlled cohort

Generate 128 controlled worlds in four balanced strata:
`old-winner owner × recovery first speaker`, 32 per stratum. The nested 96-world
fallback contains the first 24 per stratum. Interleave strata in the saved order.
Both models receive the same mathematical worlds, packets, and edits, but
generate their own outcomes. Generate disjoint six-world qualification and
twelve-world development cohorts. Do not use exposed course worlds or examples
as new evaluation data. Verify actual input overlap against locally available
historical manifests; disjoint seeds alone are insufficient.

Run **two independent continuation trials for every main cell and model**. Seeds
are independent across trials; within a trial, match per-agent invocation seeds
across sibling policies/events as in the existing design. Use the existing seed
function keyed by world/model/trial/agent/invocation, excluding packet/event
from that matched sampling stream; physical IDs still distinguish every cell.
Store seed integers exactly, never through floating-point displays. Same seed
integers do not give comparable random draws across different tokenizers or models.

The main estimand averages the two trials within each world. Report success in
both trials, success in exactly one, and neither, beside mean single-trial
success. Never select the better trial, use pass@2 as the recovery endpoint, or
count 256 trials as 256 independent worlds. Two trials estimate aggregate
conditional consistency; they do not estimate a reliable per-world probability
or variability over naturally generated prefixes.

### 5.2 Real answer-preserving check

On the first eight controlled worlds per stratum, add one trial of each packet
under a real, answer-preserving edit. Keep the main edit-owner identity; choose
uniformly among that owner's nonwinning records, then uniformly among different
replacement values below the unchanged old global maximum. Save this edit before
inference and independently verify unchanged gold. The notice has the ordinary
real-change form, without an answer-preserving label.

This gives 32 worlds, three conditions, and one full-information preserving
control per model/world. It distinguishes appropriate persistence after a real
update from persistence only when told nothing changed. It is a descriptive
robustness check, with limited precision and no second trial. It does not expand
into a third main event or receive a new primary test.

### 5.3 Natural-history bridge

Use **32 additional, disjoint worlds**, eight per stratum, with one natural
original episode per model/world. From every terminal original episode, run
literal retain/clear siblings under withdrawal and no change, once each. Include
wrong, incomplete, silent, or illegal original behavior. No source-packet
extraction, model-answer repair, or correct-prefix screening occurs.

This bridge asks whether the practical history-package contrast resembles the
controlled result under actual collaboration. It is separately analyzed, with
its own original/revised scalar controls. It cannot isolate the effect of
history provenance: natural histories differ in content, completeness, mistakes,
length, and acquisition. Do not pool its 32 worlds with the controlled cohort,
or describe it as a powered replication of the main interaction. Correct-prefix
counts remain offline descriptions.

### 5.4 Execution order

Keep all cells/trials for a world/model on one worker/device. Use a saved random
permutation of the twelve main cell/trial episodes, counterbalanced across blocks
independently of device. Balance packet, event, and trial positions; inspect the
resulting schedule before inference for aliases. Controls are separate calls.
Rotate model blocks over available physical devices so model and device are not
permanently confounded; charge reload/readiness checks. If only one suitable GPU
is available, run balanced model blocks serially. Avoid one model on a permanently
different hardware class. Any remaining hardware difference limits speed claims.

## 6. Outcomes, identification, and statistics

### 6.1 Primary endpoint and estimand

Let `Y[w,m,h,z,t]` be 1 exactly when both agents commit the exact current maximum
within bounds, and 0 for a known terminal failure. An unexecuted/unresolved
episode is unknown. Let `pbar[w,m,h,z]` average its two trial outcomes.

For each model, define the world contrast:

```text
D[w,m] = (pbar[HS,withdrawal] - pbar[HSC,withdrawal])
       - (pbar[HS,no-change]  - pbar[HSC,no-change])
theta[m] = equal-stratum mean of D[w,m]
```

Positive theta means omitting the explicit old conclusion becomes relatively
more favorable when the source changes. It does not by itself show an absolute
recovery benefit: the withdrawal HS−HSC contrast, both arm rates, and the sham
contrast must accompany it. A sham advantage for HSC can produce positive theta
even if neither policy recovers better. D lies in [−2,2].

The two model-specific theta estimates are the **two primary estimates**. Use
10,000 seeded paired world-bootstrap resamples within the four fixed strata,
carrying all conditions, trials, and both models together. Use the existing
type-7 percentile convention, with **97.5% two-sided intervals** for each
primary estimate. Bonferroni protection is only as reliable as the approximate
bootstrap coverage; do not call these exact small-sample guarantees. The two
models are fixed systems, not a random sample of architectures.

### 6.2 Prespecified secondary and descriptive outcomes

| Outcome | Interpretation and constraint |
|---|---|
| Withdrawal HS−H0 | Practical value of supplying historical source reports, including information, length, and presentation |
| Withdrawal HSC−HS and HSC−H0 | Old-conclusion and combined memory-package effects; display paired benefits and harms |
| No-change rates/contrasts | Ability to finish after reopening and preserve a still-correct conclusion |
| `theta[Qwen]−theta[Granite]` | Descriptive difference between these configured systems, with paired world uncertainty; no inference from one interval crossing zero and another not crossing |
| Both-trials-correct, one-trial-correct, neither | Conditional consistency under two sampled continuations, not new independent N |
| Answer-preserving cell rates | Appropriate persistence after a real change; preserve its fixed subset denominator |
| Natural clear−retain components and interaction | Separate practical package estimates with wide 32-world uncertainty |
| Correct, wrong, absent individual commitments | Fixed two-agent denominator; never accuracy only among submitted answers |
| Team completion, wrong agreement, wrong disagreement, noncompletion | Distinguish commitment from correctness; show terminal reason |
| Syntax, schema, action legality, delivered messages, literal repetition | Observable process diagnostics; legal messages need not be useful |
| Withdrawn-maximum submissions; own-shard local refutations | Exact evaluator-side observations; source availability and opportunity must be shown |
| Correct report available before a later wrong/absent commitment | Trace-based evidence of an opportunity, not proof of internal uptake or a decisive cause |
| Calls, tokens, all-attempt ready time, observed allocation | Quality and effort together; no arbitrary accuracy-per-token utility |

Use descriptive 95% world-cluster intervals for secondary contrasts. Do not turn
every process metric, model, event, and trial into an independent significance
test. Report raw world patterns and strata alongside aggregates. For a constant
contrast or zero failures, show an appropriate conservative bounded-mean or
binomial companion; zero observed variation is not certainty. For theta, reuse
the specification's weighted Hoeffding construction with range [−2,2] and
alpha 0.025. For direct contrasts use their correct [−1,1] range. Binomial
bounds apply within strata to independent world-level binary summaries, not
pooled agent actions or correlated repeated successes. Combine stratum summaries
with their declared weights; do not assume a pooled binomial model with identical
success probability across the four strata.

### 6.3 Precision and sample-size decision

Do not extrapolate the five assisted discordant pairs into a known population
variance. The approximate 80% power reference for each primary contrast is
`3.08 × SD(D) / sqrt(N)`, allowing for the two primary estimates:

| Assumed world-contrast SD | N=128 | N=96 |
|---|---:|---:|
| 0.30 | 8.2 pp | 9.4 pp |
| 0.50 | 13.6 pp | 15.7 pp |
| 0.80 | 21.8 pp | 25.2 pp |
| 1.00 | 27.3 pp | 31.5 pp |

These are normal-approximation sensitivity calculations, not measured power
for a sparse, discrete interaction. Two trials reduce some within-world sampling
noise but do not guarantee a particular SD. The target supports moderate effects
more credibly than the course cohort, not automatic detection of 5–10 pp. A 10 pp
effect is a reporting reference, not an equivalence margin. If the desired claim
requires reliably detecting small effects under high SD, this budget is inadequate.
Prefer an honest interval to post-hoc expansion or endpoint replacement.

Choose 128 if the complete conservative schedule fits; otherwise choose the
predefined 96 before viewing any main outcome. If neither fits, stop and seek
an explicit scope/resource amendment. Do not remove H0, shams, a model, repeats,
or unfavorable worlds to preserve an apparent result.

### 6.4 Failure, missingness, and qualitative interpretation

Known malformed/truncated/wrong/timeout actions consume their prescribed turns;
terminal failed episodes score zero. Unknown spending, unresolved processes,
unexecuted scopes, or corrupt evidence remain unknown and can block admission.
Keep the fixed intended cohort and bound unknown outcomes through each contrast,
respecting shared source/prefix records. Report paired coverage and observed-only
descriptions separately; do not present complete cases as the intended sample.
Unknown effort has no assumed zero value or finite upper bound unless the saved
deadline/attempt evidence establishes one.

Freeze a small trace rubric covering local extraction, ownership correspondence,
delivered report availability, obsolete/current submission, prose/action mismatch,
finality, waiting, and noncompletion. Some checks are deterministic; semantic
interpretations require trace references and an ambiguous category. Select fixed
lowest-index examples for success, benefit, harm, and legal noncompletion; label
any additional examples retrospective. Human double-coding of a small balanced
sample is desirable if available, not a prerequisite invented after execution.
No LLM judge, hidden numerical feedback, or causal failure-percentage decomposition
is needed. Delivered evidence is not proof of belief, and trace repair is not a
counterfactual experiment unless separately declared and executed.

## 7. Models, fair comparison, and hardware

### 7.1 Compare two configured model systems

The intended checkpoints are `Qwen/Qwen3.5-9B` revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a` and
`ibm-granite/granite-4.2-8b` revision
`f8de16cdcdbc6c779ca517604e050d82cc119e44`, observed on 18 October 2026.
Pin these observations prospectively after dependency/template acceptance;
neither Granite nor the new study has been qualified in this repository.

Use non-thinking generation for both, the same 8,192 input and 512 output token
limits, NF4 double quantization, FP16 computation, batch one, and fresh call-owned
state. No private thinking is carried forward. Token limits use each model's own
tokenizer; equal counts are not equal textual or computational capacity. Exact
mathematical inputs, action opportunities, messages, source access, and common
instructions are the main fairness controls.

Use the documented non-thinking general-task decoding regime for each system:
Qwen temperature 0.7/top-p 0.8/top-k 20; Granite temperature 1.0/top-p 0.95,
explicit top-k 0. Set min-p 0, repetition penalty 1, presence penalty 0, one beam,
and sampling on. Granite's unrestricted top-k is an explicit study choice to
avoid an inherited framework default; presence penalty 0 preserves repeated
legitimate schema keys. Freeze every setting and document these departures from
defaults. No tuning by recovery effect or same-temperature superiority claim.
The official cards are linked in the [evidence review](../analysis/thesis-extension-evidence-review.md#3-model-verification-and-hardware-derivation).

Identical decoding would be a cleaner comparison of one common sampler, but
would deliberately move Granite away from its published generation guidance.
Manufacturer-aligned decoding gives a more useful policy replication in two
usable systems. Accordingly, model differences include decoding, tokenizer,
training, and quantization behavior; they do not identify an architecture effect
or say which model is intrinsically better. No additional common-decoding arm
or thinking fallback is selected.

### 7.2 Hardware requirement, not a weights-only promise

The practical first candidate is the existing T4-class, one-replica-per-device
NF4/FP16 execution. A 24 GiB NVIDIA device provides a more comfortable alternative
if available; it still needs a supported, separately accepted lock. Use identical
hardware class and quantization across the two models. No CPU offload,
cross-device splitting, presumed BF16 support on T4, or unified two-T4 memory pool.

From official configurations, the ordinary FP16 full-attention KV cache at
8,704 resident tokens is approximately **0.266 GiB for Qwen's eight full-attention
layers** and **1.328 GiB for Granite's forty layers**. Qwen also needs recurrent
state. These are derived cache components, not peak-memory measurements. At
131,072 tokens Granite's KV alone is 20 GiB; at the old 262,144-token thesis cap
it would be 40 GiB and outside its unextended configured window. The old context
regime cannot be adopted as a common T4 baseline.

Budget roughly 5–8 GiB for NF4-resident weights/metadata/unquantized components
per model as a screening allowance, plus cache, activations, attention workspace,
CUDA allocations, and **at least 1.5 GiB measured free headroom** at the complete
accepted envelope. This range is not a fit guarantee: efficient attention and
loader behavior can dominate. Full checkpoint tensor bytes are about 17.98 GiB
and 15.61 GiB respectively, not NF4 device footprints. Plan for at least 32 GiB
host RAM, preferably 64, and approximately 100 GiB free staging/output disk;
verify actual requirements before assignment.

The existing inference code is explicitly Qwen/T4-specific. Granite requires
its own maintained `GraniteForCausalLM` path, termination IDs, template audit,
numerical/load checks, and isolation evidence. Do not apply Qwen's recurrent or
attention patches to Granite. BF16 examples on a model card do not accept FP16
NF4 on the target host. The old short-context Qwen course run supports a candidate
starting point, not acceptance of a new model, packet, or runtime.

## 8. Exact scope and conservative compute

Counts below are **worst-case first-attempt invocation slots**. Early finality or
deadlock can leave opportunities unused; do not forecast that saving. Historical
packets have zero model-generation cost, and are disclosed as supplied fixtures.

| Main component | Per model | Both models, target | Both models, fallback |
|---|---:|---:|---:|
| Controlled: N worlds × 3 packets × 2 events × 2 trials × 6 calls | 72N | 18,432 | 13,824 |
| Controlled original/revised scalar controls, once per world | 2N | 512 | 384 |
| Preserving probe: 32 × (3 packets × 6 calls + 1 control) | 608 | 1,216 | 1,216 |
| Natural bridge: 32 × (6 prefix + 4 siblings × 6 + 2 controls) | 1,024 | 2,048 | 2,048 |
| **Main total** | **74N+1,632** | **22,208** | **17,472** |

No scalar control is copied into a team cell. Controls are not replicated twice
because they are diagnostics, not the primary repeated team outcome. Natural
prefixes are charged once physically and to each hypothetical deployed policy
logically. All continuation cells/trials are separate physical generations;
resume reuses only that same saved call's exact outcome.

Controlled cost comparisons concern continuations **conditional on supplied
packets**. They do not establish end-to-end memory-maintenance savings: no model
cost of acquiring those scripted histories was observed. Record any measured
fixture-construction CPU effort separately. The natural bridge can report its
observed prefix plus continuation costs; do not impute a free model-generated
prefix to the controlled experiment or pool these cost targets.

Proposed campaign allocation:

| Allocation | Maximum new physical attempts | Resource planning reserve |
|---|---:|---:|
| Development and initial readiness, both models | 1,112 | 16 aggregate GPU-hours |
| Additional unchanged-runtime reload readiness, at most ten eight-call cycles | 80 | Included in setup/interruption reserves |
| Target main schedule | 22,208 | Measured forecast below |
| Infrastructure retry/reconciliation contingency | 600 | Four interruption hours plus conservative main margin; no error resampling |
| **Hard target campaign ceiling** | **24,000** | **200 aggregate allocated GPU-hours** |

Use another four hours for setup/loading, giving **24 reserved hours** in the
conservative complete-campaign forecast. These are caps/reserves, not permission
to spend them. All allocated idle time and failed candidates count. Extra loads
or uncertain spending consume the same limits; renaming a directory resets none.

Let `g` be conservative allocated seconds per new main invocation, based on
measured phase/model times and the slower eligible device, including assigned
between-call overhead once. Use the maximum observed ordinary scientific duration
within each model/event/packet category, weighted by its remaining worst-case
slot count. For an unmeasured bridge/probe category use the largest comparable
scientific duration for that model. Forced-length hardware envelopes establish
capacity and are recorded separately. Apply the 25% margin to this forecast;
sample maxima are conservative planning inputs, not probabilistic latency bounds.
The simple common-g screening formula is `24 + 1.25 × main_slots × g / 3600`:

| Assumed g | N=128 total GPU-hours | N=96 total GPU-hours |
|---|---:|---:|
| 10 s | 101.1 | 84.7 |
| 15 s | 139.7 | 115.0 |
| 20 s | 178.2 | 145.3 |
| 25 s | 216.8 | 175.7 |
| 30 s | 255.3 | 206.0 |

These are arithmetic sensitivities, not observed Granite throughput. With all
reserves, the target needs `g <= 22.82 s`; the fallback needs `g <= 29.01 s`.
The course's roughly 6-second mean ready time on short Qwen calls must not be
used as a two-model allocated-time guarantee. Full-envelope diagnostics,
longer messages, competent longer episodes, loading, exports, and idle allocation
can change the cost substantially.

Two fully used devices shorten ideal elapsed time, not aggregate device-hours.
At 200 aggregate hours, even ideal two-device execution is 100 elapsed hours,
requiring multiple sessions under the previously reported approximate Kaggle
session window. Verify current account/session limits and off-session restoration;
do not assume a free quota, confirmed provider release, or survival of shutdown.
Cash cost is the accepted provider's current per-device rate times charged hours,
plus separately identified charges; no paid booking is authorized here. Historical
programme spending remains separately recorded, including unknown allocation.

## 9. Feasibility and acceptance gates

Detailed implementation acceptance is in the [roadmap](../plans/thesis-extension-roadmap.md).
The scientific decisions are:

1. **Contract approval:** explicitly adopt the new controlled population,
   packets/events, bridge, repeats, endpoints, two-model regime, and budgets.
   Until then, specification §§1–12.1 and all prior freezes remain unchanged.
2. **Deterministic acceptance before GPU use:** independently validate generation,
   the legal scripted history, HS/HSC byte equality, current-source privacy,
   event/reopening/finality semantics, exact resume/attempt accounting, and the
   complete native token envelope for both tokenizers. The existing 8,192-token
   I-01 proof does not automatically cover these new packets. Never truncate
   history; a failed bound requires an explicit pre-main amendment or stop.
3. **Bounded hardware/qualification:** separately authorize the declared calls,
   then accept exact weights/templates/EOS, finite output, call-state isolation,
   full envelopes, storage/restore, deadlines, and headroom on every active device.
   At least 11/12 qualification scalar controls and 7/8 local/source-use diagnostic
   targets must be correct per model; all these diagnostic actions must be legal.
4. **Twelve fixed development worlds per model:** execute all six controlled
   cells once and both scalar controls, plus a natural original episode for each
   world. Require at least 22/24 correct scalar controls, at least 9/12 exact
   no-change teams in **each** of HS and HSC, at least 98% legal attempted
   controlled team actions, complete committed evidence, and intact health,
   resources, and exports. H0 and withdrawal success are reported but have no
   effect-direction or success veto. Natural originals diagnose bridge context
   and are not selected or required to pass. These are usefulness screens with
   wide uncertainty, not reliability certification.
5. **Freeze and separate main authorization:** both models must pass, and the
   complete target or fallback forecast must fit. Freeze configuration, source,
   inputs, prompts, timing, order, analysis and rubric. Seek authorization for
   that concrete complete scope. A gate pass alone authorizes no main execution.
6. **Execution/release:** run every intended main world regardless of ordinary
   errors or effect direction, stopping only for actual integrity/resource
   problems. Independently reproduce scores, coverage, intervals, and costs.
   Publication/export to a public destination remains separately authorized.

Development first-attempt arithmetic per model is eight initial hardware/state
calls, twelve qualification controls, eight supplied-view diagnostics, and
`12 × (6×6 + 2 + 6) = 528` development slots: **556 per model, 1,112 total**.
Development diagnostics cover both agents, own-shard extraction with owner-labelled
records, changed-owner interpretation, and commitment with an available peer
report. Expected numerical targets remain evaluator-side. They do not teach
answers or become extra main data.

If either model fails a scientific usefulness gate, preserve the full feasibility
result and stop the two-model main plan. A single-model redesign, longer reasoning,
new assistance, different task, larger hardware, or threshold revision requires
an explicit prospective decision. Do not search candidates until one passes or
relax a gate because the observed memory effect is interesting.

## 10. Explicit proposed amendments and preserved authority

Adopt this, if approved, as a separately named thesis-extension section/regime,
not a rewrite of completed results or an implicit replacement of every historical
section. The adoption text must identify precedence for this new campaign only:

| Existing authority | Proposed scoped amendment |
|---|---|
| §§1–2: five families, four peers, natural prefixes, 60/40 worlds | One I-01 family, two peers, 128/96 supplied-history worlds plus separate 32-world natural bridge; old populations remain intact |
| §§3–4: synchronous provisional candidates, B/C/K/masks/receipts | Preserve §12.1's sequential final actions; add three explicitly defined controlled packets and genuine no-change reopening |
| §§5–6: original AUC/reset/interference primaries and repetition | Two model-specific conclusion-exposure interactions on repeated exact team success; world-level averaging/uncertainty as above |
| §8 and §10: one accepted model, Qwen/4B fallback, 262k envelope, 100-hour plan | Two required 9B/8B systems, 8,192+512 short-call regime, no 4B/thinking fallback, new 200-hour/24,000-attempt ceiling |
| §§12–12.1: course worlds, assisted-v2 prompts, 500-attempt campaigns | A new campaign with new inputs/schedules, packet/event wording, accounting and gates; course semantics/results are not migrated |

Preserve all original thesis code/defaults, saved populations, CPU proofs,
incomplete/unexecuted evidence, course stores, source packets, notebooks, analyses,
figures, and both report versions. Do not alter historical invalid replies or
seed labels to make them consistent with new behavior. Use exact canonical seed
integers; the submission report identifies transcription errors in the prose
ledger, which remains historical evidence rather than a seed authority.

## 11. Interpretation and approval recommendation

| Possible finding | Defensible conclusion |
|---|---|
| HS helps relative to H0 after withdrawal | Historical source reports are a useful resource in this interface, with measured package costs |
| Dropping the old conclusion helps especially after withdrawal | Explicit old-conclusion exposure has a change-dependent behavioral cost under a fixed historical evidence basis |
| HSC helps sham but neither arm helps withdrawal | Positive interaction may reflect lost preservation benefit, not successful recovery; show direct rates |
| Both evidence-rich arms fail despite scalar/sham competence | Current-source interpretation, inter-agent uptake, or commitment remains a recovery bottleneck; distinguish observed cases |
| Controlled results are good but the natural bridge fails | Supplying a competent historical basis does not establish that models reliably acquire and use it naturally |
| The two models differ | A boundary across two configured systems, requiring direct interaction uncertainty; no architecture-level causal claim |
| All controlled arms perform well or intervals overlap broad effects | A ceiling or an imprecise comparison; preserve it without adding harder conditions after seeing outcomes |

**Approve the controlled three-packet study, its two bounded checks, and the
scoped implementation roadmap as the next thesis direction.** The first
authorization should adopt the amendment and permit deterministic implementation
and verification only. GPU qualification/development, the measured main scope,
paid resources, and publication remain separate explicit decisions. This is the
smallest recommended programme that addresses useful historical evidence,
change specificity, real interaction, final commitments, repetition, and both
intended models without inheriting the original matrix's full complexity.
