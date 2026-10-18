# Memory, evidence and revision: findings that transfer

This review distinguishes storing history, retrieving it, selecting authoritative
evidence, applying it, and completing an action. Success at one stage does not
establish the others. Paper IDs resolve to exact bibliographic records in the
[reading ledger](sources-and-reading-ledger.md).

## 1. Memory benchmarks measure different problems

**M01 — MemoryAgentBench.** Hu, Wang and McAuley's
[v4 full text](https://arxiv.org/html/2507.05257v4) evaluates retrieval, learning,
long-range understanding and conflict resolution. FactConsolidation supplies
successive synthetic facts under a latest-fact rule; its “forgetting” outcome is
answer-time selection, not demonstrated physical deletion. Backbone, context
length, chunk size and retrieval budget matter. Its short-context o4-mini check
reaches 80% on multi-hop questions but 14% at 32K. Questions sharing one fact list
are correlated. This is evidence that retrieval and composition can separate,
not that every model needs a forgetting mechanism.

**M02 — MemoryArena.** The
[September v2](https://arxiv.org/html/2602.16313v2) links earlier actions and
feedback to later sessions in shopping, planning, search and formal reasoning.
Some end-to-end success rates remain near zero despite partial progress.
External memory does not consistently beat full history, while retrieval helps
in some long-search settings. The authors' representation/training-mismatch
explanations are plausible hypotheses, not independently isolated causes.
Planning's severe constraint-solving floor makes it an unsuitable direct memory
benchmark for our small models. Its latency table also has exceptions to the
prose's blanket ordering of memory mechanisms.

**Our inference:** use a task whose components are separately understandable,
without requiring that every team solve it. A scalar full-information control
can diagnose numerical extraction; it does not certify coordination competence.
Short contexts make an elaborate storage/retrieval comparison a weak first use
of the thesis budget. Our historical packets are supplied evidence, not a new
long-term memory architecture.

## 2. Conflicting benchmark interpretations are scientifically useful

**M03 — Frozen last-write resolver audit.** Pakhomov and Nijkamp's
[v1](https://arxiv.org/html/2610.09193v1) obtains 642/800 answers with a fixed
parser/resolver developed on the short lists. It identifies reachable misses,
parser limitations and gold answers inconsistent with its reconstructed latest
graph. Those categories do not prove every flagged gold wrong: parsing coverage
and relation ambiguity limit adjudication. Its held-out lists reuse templates,
and only a few independent lists support broad uncertainty claims. The
important contribution for us is an audit of benchmark semantics, not evidence
that all memory reasoning reduces to bookkeeping.

**M04 — Post-retrieval assembly.** Reddy and Challaram's
[v2](https://arxiv.org/html/2606.01435v2) separates extraction from deterministic
policy execution. Direct answering rises from 67.2% to 78% in the pooled
single-hop comparison, but prompting, format and temperature also change. The
closer LLM-picker comparator reaches 76%; at the longest length it ties the
deterministic executor. On LongMemEval update questions, the structured method
does not improve the reported result. This supports task-sensitive decomposition,
with weak attribution of the entire headline gain to deterministic freshness.

**Transfer decision:** preserve independent exact task oracles and check that
public observations admit the intended inference. A CPU proof that the owner can
solve and the non-owner lacks a necessary new value is more useful than another
memory service. A host latest-write resolver is appropriate for enforcing which
source version is current. A host maximum calculator that corrects peer answers
would supply the reasoning being evaluated. Keep those roles separate.

## 3. Retaining a conclusion and retaining its basis are different treatments

**R01 — Reclaim Evaluation, revisited.** Kwon's
[v5](https://arxiv.org/html/2606.25449v5) uses planted incorrect commitments and
templated notes that preserve different amounts of recomputation evidence.
Source-first notes outperform conclusion-heavy notes where the source is compact;
neutral padding and source/noise sweeps narrow the explanation. The strongest
source-preservation intervention is controlled, and deployed writing is weaker.
Our old answer was correct before an external edit, so this is a useful
analogy rather than a replication. HS versus HSC specifically tests adding an
explicit old commitment when the source basis already survives.

**R04 — Precomputed-memory correction, revisited.** Shepard's
[v1](https://arxiv.org/html/2608.30647v1) compares pasted updates and saved-cache
delivery mainly on Llama-3.1-8B. Question-naming corrections greatly improve
adoption, but question-naming false values are also adopted. The correction
analysis screens for stale failures and corrected-text successes, so its rescue
rates are conditional. Token-matched padding distinguishes bulk from competing
revision content; naming is not shown to solve arbitrary accumulated updates.
The transferable warning is that an apparently effective update may simply
dictate the answer. Cache engineering is outside our stateless-call experiment.

**Our design consequence:** source and commitment fields should have transparent,
literal provenance. Preserve identical source-report bytes across HS and HSC.
Do not generate a “helpful” global conclusion in an update message. A common
instruction may name the affected owner/record and explain authority; the host
must not infer and supply the current global answer. Any improvement from that
answer supply would answer a different, much easier question.

The HS/HSC contrast also has a limitation that should be accepted openly:
removing a separate conclusion does not remove every occurrence of the old
maximum. That value remains useful historical evidence inside a source report.
This is a policy comparison about an explicit commitment cue, not complete
erasure of the old answer from the context.

## 4. Presentation can defeat evidence even when retrieval succeeds

**M05 — Generated versus retrieved contexts.** Tan et al.'s
[ACL paper](https://aclanthology.org/2024.acl-long.337/) constructs conflicting
context pairs on Natural Questions and TriviaQA. Readers often prefer generated
contexts even when retrieved evidence alone gave the correct answer. Preference
also occurs with another model's generated text. Similarity associations and
semantic-completeness controls suggest presentation matters; they do not isolate
a universal self-authorship bias. Appendix controls and length/completeness
tables were inspected, including the rendered table. Our scripted source
reports should therefore avoid an unnecessary prose-quality imbalance between
conditions.

**M08 — Internal versus external knowledge conflicts.** Jin et al.'s
[LREC-COLING paper](https://aclanthology.org/2024.lrec-main.1466/) varies correct
and incorrect closed-book answers against conflicting QA evidence. Models often
follow external passages, with substantial dependence on model and question.
This does not contradict M05: the alternatives and construction differ.
Closed-book induction, generated counterfactuals and token-recall metrics limit
transfer. A synthetic private integer is not a well-known fact encoded in model
weights. We should not explain our owner confusion as a proven conflict between
parametric and retrieved knowledge.

**M09 — Context position.** Liu et al.'s
[TACL paper](https://aclanthology.org/2024.tacl-1.9/) moves relevant documents and
UUID key-value pairs within contexts. Longer advertised windows do not ensure
uniform use; position effects survive relevant ordering controls. These were
older models, longer contexts and retrieval-style endpoints. This warrants
auditing our rendering order and avoiding silent truncation, not assuming a
middle-position mechanism for every short course failure.

**Practical response:** use explicit, consistent owner-qualified record labels,
for example `agent-0:r13` versus `agent-1:r13`, built from existing IDs. Keep
current private data, environmental notices and historical claims visibly
distinct. Freeze source/history ordering in the main study. If development
reveals severe layout dependence, compare at most two common layouts on disjoint
development worlds, with equal budgets for both models. Report that choice;
do not optimize layout on main outcomes or add a full position factorial.

## 5. Binding and state-tracking research challenges easy task assumptions

**M07 — Entity tracking.** Kim and Schuster's
[ACL paper](https://aclanthology.org/2023.acl-long.213/) uses controlled boxes and
operations, including lexically disjoint demonstrations and stronger contextual
dependencies. Several tested models mainly repeat initial states; GPT-3.5 shows
nontrivial tracking. Unchanged-target and changed-target cases reveal different
behaviors. Code-pretraining associations are not randomized causal evidence.
The lesson is to construct examples that distinguish the desired computation
from a shortcut, not to import the whole benchmark.

**M06 — Binding representations.** Dai, Heinzerling and Inui's
[EMNLP paper](https://aclanthology.org/2024.emnlp-main.967/) identifies ordering
subspaces and uses activation interventions to alter entity–attribute binding,
with position controls and additional models. This gives a mechanistic example
of association errors. It neither diagnoses our traces nor establishes that a
prompt label changes the same mechanism. Activation steering would introduce a
separate model intervention and substantial new work.

**M10 — State changes and shortcuts.** Tang et al.'s
[v1](https://arxiv.org/html/2605.30233v1) combines probes, interventions and
behavioral tests of PUT/REMOVE/MOVE. A global object-removal heuristic succeeds
on the original unique-object task but fails on shared labels, irrelevant
removals and some reintroductions. Effects differ across models. Negative linear
probe results do not rule out every representation of state; best-layer
interventions are not a ready deployment fix. Its strongest transfer is the
method: use counterexamples that separate genuine state reasoning from a
task-valid heuristic.

**Priority for our task:** add the winner-survives stratum described in the
[repository critique](repository-and-design-critique.md#4-two-information-structure-problems-to-resolve).
Require a deterministic indistinguishability witness: two legal revised worlds
give the non-owner the same initial view but different gold answers. This is an
acceptance property to implement after adoption, not an experiment run here.
It is more directly relevant than mechanistic probing of either intended model.

## 6. Repairing propagation is not the same as repairing use

**R03 — When Evidence Changes, revisited.** Chu's
[v1](https://arxiv.org/html/2610.03902v1) compares rereading and memory repair on
short clinical-record renderings. Some replacement misses occur even though the
new value reached the displayed facts. Adoption and preservation of other
items differ. Strong source-filtered rereading changes cost conclusions; small
samples, lexical scoring, post-hoc amendments and a disclosed protocol mismatch
limit inference. The paper does not establish a universal rereading advantage
or a causal effect of maintenance alone.

For our experiment, keep the same separation: “new value was visible” is a
checkable observation, whereas “new value was understood” is not directly
observed. A current-source inventory and exact action trace can identify a
failure after information availability without constructing a semantic graph.
Use a few fixed observable categories and retain ambiguous cases. Avoid an
exhaustive psychological taxonomy or claims that one early utterance caused a
later error without a counterfactual test.

## 7. Decisions supported by this literature

| Decision | Scientific reason | Risk / complexity | Appropriate future check |
|---|---|---|---|
| Preserve literal source evidence separately from the old commitment | Isolates a meaningful policy difference | Low; cue removal also changes length and salience | Exact HS/HSC source-byte equality and clear claim boundary |
| Cover edits whose new private value matters | Separates answer recovery from a deletion shortcut | Low–moderate generator change; different population | Independent oracle and indistinguishable-view witnesses |
| Keep no-change and a small real answer-preserving check | Distinguishes warranted persistence from blanket changing | Additional cells; diagnostic samples remain imprecise | Joint exact success and damage rates, with denominators |
| Use clear owner/record and authority presentation | Addresses demonstrated association failures | Low; any new prompt is a prospective intervention | Common development layout check, then freeze |
| Exclude RAG, learned summaries, cache patching and activation repair | They change the scientific object and add unneeded machinery | Saves compute; narrows generality | Reconsider only if accepted task requires unavailable history |

None of these papers licenses repairing a model's answer, filtering worlds by
model success, or silently replacing the adopted retention semantics.
