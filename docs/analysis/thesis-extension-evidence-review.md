# Evidence review for the thesis extension

**18 October 2026 · read-only investigation and prospective reasoning**

This is the evidence companion to the [recommended design](../proposals/thesis-extension-2026-10-18.md),
not a new experiment or scientific authority. Repository inspected:
`005a456cda4cba54cff36084a125dc883bb5ba8a`, branch
`feat/smaller-natural-experiment`, initially clean. No weights were downloaded,
model loaded, GPU operation run, or scientific condition implemented. Official
model metadata, templates, and selected paper texts were fetched; scratch
calculations and immutable SQLite reads remained outside experimental execution.

## 1. What exists, and what its evidence establishes

The investigation followed the root operating contract, specification §§1–10
and adopted I-01 §§12–12.1, the implementation plan's milestone/handoff sections,
and the implementation-research synthesis. It then examined the course analyses,
the original and submission-ready final reports, canonical stores, selected raw
requests/actions, relevant source modules, prerequisite verification records,
and the selective research archive. This was not a new exhaustive audit of every
archived file or a rerun of every historical test suite.

| Asset | Implemented behavior and evidence | Evidential boundary |
|---|---|---|
| Original thesis mathematics | Five task generators, independent truth, edits, coordinates, balanced populations and dependency schedules in `tasks.py`, `truth.py`, `edits.py`, `populations.py`, `schedule.py`; [M1 evidence](../todos/M1/M1-T03-complete-schedules.md) | CPU mathematical/protocol evidence, not pretrained-model success |
| Four-peer protocol and interventions | Permitted source/history views, strict candidate/send replies, synchronous barriers, B/C/K/F/L, complementary masks, receipts and delayed prose; [M2 evidence](../todos/M2/M2-T06-attainability-and-capacity.md) | Implemented and CPU-verified; complete retained-context proof reaches 261,388 tokens under a 262,144 cap |
| Original durable execution | `runner.py`, `storage.py`, `attempts.py`, `workers.py`, exact replay and accounting; [M3 lifecycle](../todos/M3/M3-T05-crash-safe-scripted-lifecycle.md) | CPU fault injection and scripted lifecycle, including eleven controller kills and 4,340 logical slots/384 replays; no accepted original-thesis main inference |
| Offline thesis analysis | Exact scoring, trajectories, contrasts, missingness, costs, intervals and reports; [M4 gate](../todos/M4/M4-T06-reproducible-report-and-cpu-gate.md) | Historical 424-check full source regression and retained report reproductions; not rerun in this review |
| Qwen backend and hardware investigations | Text-only pinned loading, NF4/FP16, cache isolation, explicit T4 attention path; [attention evidence](../validation/m5-attention-memory.md) | Support is Qwen-specific; not a model-agnostic loader or Granite acceptance |
| Long-input course preparation | [Final-online-6 diagnosis](../validation/course-kaggle-final-online-6-analysis.md) records a completed 9B stress generation with only 16.813 MiB free against a 1.5 GiB gate; 4B then blocked by checkpoint-size accounting | Hardware rejection in that configuration, not a pilot, main result, or proof that short-context 9B is infeasible |
| I-01 execution system | `recovery/i01/{core,store,process,runtime,workflow,inference,archive,report}.py`: sequential final actions, two canonical WAL/FULL stores, one admission owner, finite stages, exact resume/export | Strong reusable foundation for a two-agent extension; event/policy/model assumptions are hard-coded in places |
| Assisted software release | [Requirement/installed audit](../validation/i01-assisted-implementation.md), source checkpoint `d95bb01`, new packet and 37 finite cells | Named CPU/native/installed checks support that release; its dated “unrun” statements precede the later supplied campaign |
| Completed course model evidence | [Canonical assisted run](../../notebooks/run/assisted-v1/latest/run.json), [analysis](assisted-v1/scientific-analysis.md), [forensic verifier](assisted-v1/forensic-reproducibility.md), and both report versions | Real short-context Qwen/T4 empirical evidence under `i01-course-assisted-v2`; not the original thesis or Granite |

The current README/plan include dated implementation handoffs that say assisted
inference remains unrun. The supplied final artifact and final report establish
later completion. Preserve those dated statements as history while linking the
current empirical status. Do not infer current readiness from the oldest status
paragraph at the top of the specification.

Important inspected implementation constraints are concrete: `ProtocolLimits`
accepts only the adopted thesis/course combinations; `Candidate` and language-load
audits allow pinned Qwen models; the loader checks actual T4 and its runtime;
I-01 `permitted_view` treats every non-prefix phase as the revised world; report,
manifest, and admission code assume existing stage/policy scopes. Adding Granite,
shams, packets, and repeated trials is **not** a JSON-only configuration change.
The roadmap addresses these explicit seams without a generic plugin system.

## 2. Rechecked course results and trace implications

### 2.1 Current read-only reconstruction

This session opened the two standalone backup databases in each final campaign
with `mode=ro&immutable=1`. All four `PRAGMA integrity_check` results were `ok`.
Using Python standard-library integers and the saved manifests, it independently
recomputed current maxima, terminal team success, paired categories, and
ready-model effort from call outcomes. It reproduced 10,000-draw historical
bootstrap displays using each campaign's saved seed, the four owner/first-speaker
strata, and that campaign's original percentile-index convention.

| Campaign | Calls | Retain | Clear | Both / retain-only / clear-only / neither | Clear−retain success; historical interval | Clear−retain ready seconds; historical interval |
|---|---:|---:|---:|---|---|---|
| Course-7 | 252 | 2/20 | 2/20 | 1 / 1 / 1 / 17 | 0 pp; [−10,+10] pp | +9.157; [+1.964,+17.124] |
| Assisted-v2, stored in `assisted-v1` | 356 | 2/20 | 3/20 | 0 / 2 / 3 / 15 | +5 pp; [−15,+25] pp | −3.783; [−8.241,+0.589] |

Seeds were 2026101402 and 2026101602 respectively. These intervals are historical
exploratory displays, not equivalence evidence or reliable repeated-run bounds.
The campaigns have different worlds, interfaces, seeds, schedules, and histories;
their differences do not identify an assistance effect and must not be pooled.

The earlier [10,953-comparison verifier](assisted-v1/forensic-reproducibility.md#4-executed-verification-result-and-scope)
covered full request/trajectory reconstruction, source/archive parity, reports,
and the historical campaign. That is retained verification evidence; the present
review did not relabel it as a newly rerun 10,953-check suite.

### 2.2 Current raw examples

The following requests and raw actions were read directly from canonical SQLite,
not inferred from a generated case summary. Links locate the corresponding
conversation export; IDs identify exact call rows.

| Exact assisted call | Observable fact | Consequence for design |
|---|---|---|
| [main-08/retain/agent-0/invocation-2](../../notebooks/run/assisted-v1/latest/reports/conversations.html#main-08/retain/agent-0/invocation-2) | Current own maximum 758 and delivered peer maximum 857 were visible; the final action repeated the local report with `submit:null`, `wait:false` | Separate correct communication from completed commitment; this was not blocked delivery or literal mutual wait |
| [main-09/clear/agent-1/invocation-1](../../notebooks/run/assisted-v1/latest/reports/conversations.html#main-09/clear/agent-1/invocation-1) | A visible peer report said 949 at record 16; the action instead called 695 at record 13 the partner maximum and submitted 836; 695 was own record 13 | Source/owner confusion can occur without retained history; current access does not imply use |
| [main-04/clear/agent-1/invocation-2](../../notebooks/run/assisted-v1/latest/reports/conversations.html#main-04/clear/agent-1/invocation-2) | Text named 954 as global and promised submission, but the actual `submit` remained null with partner finished | Do not score the explanation or add a host finalizer |
| [main-13/clear/agent-1/invocation-0](../../notebooks/run/assisted-v1/latest/reports/conversations.html#main-13/clear/agent-1/invocation-0) | With no current peer messages or remote replacement value, the action claimed remote record 9 changed to 397; own record 9 was 397 | Distinguish source extraction/association from old-answer persistence; keep owner labels explicit |

The [submission-ready report](../reports/final-course-report-submission.md)
additionally documents 10/20 correct original teams, 18/20 revised controls,
32/35 entirely legal failed recoveries, and no withdrawn-maximum recovery
submissions. These broader diagnostics are supported by the retained full audit
and report reconstruction; only the selected request/action examples and primary
outcome/effort calculations above were independently reread/recomputed here.

The final report's Appendix B.4 discloses a significant **prose seed-label
transcription problem**. This review compared all 356 ledger labels with exact
database request integers and confirmed 354 discrepancies: 180/182 on worker 0,
174/174 on worker 1. Raw scientific outcomes and canonical requests are intact.
Do not copy those printed labels into a new seed schedule. Keep Python integers
and exact canonical fields throughout export; JavaScript floating-point numbers
are not an appropriate transport for arbitrary 64-bit seeds. The original ledger
is preserved; this review does not silently repair it.

### 2.3 What follows, and what does not

The data support investigating evidence use, owner correspondence, reopening,
and final commitments. They do not establish that a particular prompt change,
extra turn, host validator, or memory policy will fix them. Better original
accuracy and legality coexisted with poor recovery. Clear also failed, so stale
history alone cannot explain the common failure pattern. No-change controls are
necessary to distinguish revision-specific behavior from generic reopening.

Useful historical evidence remains a real possibility: unchanged peer reports
can supply information a cleared agent would otherwise reacquire. Conversely,
the old winning result may discard needed alternatives. A controlled source
basis tests this distinction without selecting only successful natural prefixes.
It also deliberately changes the population; the natural bridge is needed to
show the distance from naturally generated interaction.

## 3. Model verification and hardware derivation

Official metadata was fetched on 18 October 2026 without model weights. Current
repository revisions were read through the Hub API; configuration, generation
settings and templates were then read at those immutable revisions. Model cards
are manufacturer descriptions, not demonstrations of this task's competence.

| Property | Qwen3.5-9B | Granite 4.2-8B |
|---|---|---|
| Checkpoint | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | [ibm-granite/granite-4.2-8b](https://huggingface.co/ibm-granite/granite-4.2-8b) |
| Observed revision | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | `f8de16cdcdbc6c779ca517604e050d82cc119e44` |
| Architecture/configuration | 32 text layers; 24 linear-attention and eight full-attention layers; four full-attention KV heads of dimension 256 | Dense full-attention transformer; 40 layers; eight KV heads of dimension 128 |
| Configured native positions | 262,144 | 131,072; do not confuse advertised long-context extension with unmodified configuration |
| Text loading | Maintained Qwen text-only path; avoid loading/crediting vision components | `GraniteForCausalLM`; not Granite 4.0 hybrid/Mamba |
| Direct mode | `enable_thinking=False` | `enable_thinking=False`; default thinking otherwise |
| Published general direct sampling | Temperature 0.7, top-p 0.8, top-k 20 | Temperature 1.0 and top-p 0.95 |
| Full checkpoint tensor payload | 19,306,216,416 bytes | 16,761,102,336 bytes |
| Repository-specific evidence | Short-context NF4/FP16 T4 campaign completed | No local loading, capability, latency, or headroom acceptance |

Architecture fields come from the pinned [Qwen configuration](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/config.json)
and [Granite configuration](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/config.json).
Payload sizes are `metadata.total_size` in their respective pinned
[Qwen tensor index](https://huggingface.co/Qwen/Qwen3.5-9B/blob/c202236235762e1c871ad0ccb60c8ee5ba337b9a/model.safetensors.index.json)
and [Granite tensor index](https://huggingface.co/ibm-granite/granite-4.2-8b/blob/f8de16cdcdbc6c779ca517604e050d82cc119e44/model.safetensors.index.json).
They exclude serialization overhead and do not represent resident NF4 allocations.

Granite's card emphasizes reasoning, code, instruction following and agentic
workflows; its published task scores do not establish direct-mode private-shard
competence. Its default template uses thinking and can strip historical assistant
thinking. Qwen also has default thinking behavior. Both templates therefore need
explicit direct-mode framing and literal archived data in a user block. Do not
let model-native conversation rewriting erase a history treatment. The
[IBM technical account](https://huggingface.co/blog/ibm-granite/granite-4-2)
helps explain the intended use, not comparative recovery performance.

The maintained [Transformers Granite documentation](https://huggingface.co/docs/transformers/main/model_doc/granite)
supports the model family; [bitsandbytes installation requirements](https://huggingface.co/docs/bitsandbytes/main/en/installation)
and [Transformers quantization documentation](https://huggingface.co/docs/transformers/main/quantization/bitsandbytes)
support NF4 as a candidate path on Turing-class hardware. None verifies this
checkpoint's complete FP16/NF4 execution in the repository's accepted environment.
The course lock's Torch 2.11.0+cu128/Transformers 5.12.0 is a candidate to inspect,
not automatic Granite acceptance. A model config's exported Transformers version
is not a tested dependency lock or an instruction to downgrade.

For batch one and FP16 KV, the ordinary full-attention cache component is
`2 × layers × KV_heads × head_dimension × tokens × 2 bytes`:

| Resident token count | Qwen full-attention KV | Granite KV |
|---:|---:|---:|
| 8,704 | 0.266 GiB | 1.328 GiB |
| 16,384 | 0.500 GiB | 2.500 GiB |
| 32,768 | 1.000 GiB | 5.000 GiB |
| 131,072 | 4.000 GiB | 20.000 GiB |
| 262,144 | 8.000 GiB | 40.000 GiB, outside unextended configured positions |

This derivation excludes recurrent state, weights, quantization metadata,
unquantized embeddings, activations, prefill/attention workspace, and allocator
overhead. It explains why short context is a scientific feasibility decision.
It is not a measured memory requirement or a guarantee of T4 fit. The new
8,192+512 proposal preserves the course's useful envelope size while requiring
a fresh proof for the changed packet renderer and both native tokenizers.

## 4. Literature: findings that change this recommendation

This was a targeted primary-source update, not an exhaustive novelty review.
The repository's [fifteen-paper scientific review](../implementation-research/i01-course-7-targeted-scientific-literature-review.md),
[practical investigation](../implementation-research/i01-course-practical-literature-investigation.md),
and [historical landscape](../../research/04_design_extensions/UPDATED_RESEARCH_LANDSCAPE.md)
were used selectively. Current official records/texts were checked for the
central recovery, communication, reliability, and model claims. Recent arXiv
items below are preprints unless an independently verified venue is named.

| Primary source and inspected material | Relevant result or limitation | Design consequence |
|---|---|---|
| [SILO-BENCH, ACL 2026](https://aclanthology.org/2026.acl-long.1354/); official record and repository task/runner audit | Private information can elicit abundant communication without effective computation; native task/run/scoring semantics differ from this project | Retain exact mathematical tasks and attribution, not benchmark scores or native stopping/retry behavior |
| [ICR, v1](https://arxiv.org/html/2610.01042v1); design, correction/preservation, Appendix G | Fixed initial solutions and no-message revision controls separate some benefits from extra reasoning; richer messages can help and harm; some full-set estimates impute outcomes | Show paired benefits/harms and genuine observed coverage; distinguish its shared-problem single-hop setup from private-source continuing interaction |
| [CIR, v1](https://arxiv.org/html/2610.00372v1); paired continuations, controls, held-out units | Recovery can rescue and harm; 300 condition-episodes arise from 75 tasks; observation corruption is not a changed environment | World clustering and a real no-change control; no learned router on a small course cohort |
| [Reclaim Evaluation, v5](https://arxiv.org/html/2606.25449v5); source-first conditions, length controls, scope boundaries | Sources and explicit conclusions are different resources; source-first gains require a compact identifiable source, and failure returns when it no longer fits | HS/HSC hold reports fixed, while H0 measures source availability; do not claim invention of source-preserving recovery |
| [StateAuditor, v1](https://arxiv.org/html/2608.01619v1); transition-based repair framework | Updated memory does not ensure updated behavior; structured transitions/repair rely on their own assumptions | Measure available information versus committed action; no automatic semantic repair |
| [REVISE, v1](https://arxiv.org/html/2609.00643v1); validity/dependency recovery | Preserving valid progress and conservative invalidation already have explicit workflow formulations | Exclude a speculative provenance graph or novel selective-rollback claim |
| [When Evidence Changes, v1](https://arxiv.org/html/2610.03902v1); pipelines, replacement results, §8 limitations | Actual source replacement and memory versus re-reading are already studied; apparent revision savings can disappear after full-pipeline accounting; small cohorts and presentation/scoring limitations remain | Actual revision alone is not novelty; meter the full workflow and restrict the contribution to distributed information use and commitments |
| [Memory Echo, v1](https://arxiv.org/html/2610.17763v1); lifecycle setup and limitations | Repeated same-source exposure and post-correction persistence are existing topics; its mitigation uses supplied provenance/validity annotations and answer processing | Literal repetition is a diagnostic, not a new mechanism or justification for importing a certified checker |
| [LLMs Get Lost in Multi-Turn Conversation, v1](https://arxiv.org/html/2505.06120v1); full/concatenated/sharded controls and reliability analysis | Interaction can reduce reliability despite stronger single-turn performance; staged instructions are not actual factual withdrawal | Scalar controls cannot certify recovery; preserve natural interaction and repeated trials |
| [τ-bench](https://arxiv.org/abs/2406.12045); repeated-trial metric definition | At-least-one success and all-trials success answer different questions | Average both planned trials and show both-trials success; no best-trial selection |
| [Belief-R, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.586/); repository's full-text analysis and official record | Appropriate maintenance and warranted updating require different checks | Include no-change and a small real answer-preserving probe |
| [MAST, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html) and [Who&When, ICML 2025](https://proceedings.mlr.press/v267/zhang25cq.html); existing full-text review | Failure vocabularies help organize traces; locating a visible mistake is different from establishing the decisive cause | Small trace-linked rubric with ambiguity; no causal percentages or independent-human-review claim |

The newer evidence-revision and Memory Echo papers further narrow novelty beyond
the original landscape. Their designs do not establish this study's expected
effect size, and their model/task scores are not feasibility evidence here.
The recommendation therefore makes a controlled empirical contribution, not an
exhaustive “first recovery method” claim. More generic memory-platform research
would not resolve the immediate capability and resource gates.

## 5. Decision, uncertainty, and verification scope

The recommendation intentionally gives up five-family generality and the
original causal teammate-reset estimand in exchange for better identification,
more independent worlds, repeated trials, both intended models, and a feasible
short-context implementation. Team effects remain real outcomes of live
interaction, but this study does not identify the effect of resetting another
agent while holding one's own state fixed. The discarded original comparison
remains scientifically valuable and implemented for a later study.

The proposal's schedule, cache components, cost table, break-even latencies, and
normal-approximation precision references were independently calculated with
standard-library arithmetic in this session. They are forecasts/derivations,
not model measurements. Existing GPU/software verification records were inspected,
not rerun. New adoption, implementation acceptance, model capability, hardware,
development outcomes, frozen main configuration, main inference, and publication
all remain pending at their respective authorization gates.

Documentation delivery checks resolve all 27 local links/fragments in the three
new documents and reconcile both schedule totals and campaign ceilings. A
SHA-256 comparison of all 2,529 initially tracked files found only the intended
implementation-plan status addition changed; specification, executable code,
configurations, canonical stores, reports, and historical evidence are unchanged.
No unrelated broad regression or new experiment was run for this documentation
change.
