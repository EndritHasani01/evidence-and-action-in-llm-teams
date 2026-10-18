# Sources, versions and full-text reading ledger

**Access date: 18 October 2026.** This is a decision-oriented investigation,
not a systematic review or an exhaustive census of the literature. Bibliographic
identity was checked against primary arXiv records, official proceedings,
institutional reports and the original texts. Claims refer to the versions
below. An arXiv entry is not treated as peer-reviewed merely because it exists.

## 1. Investigation method and limits

The starting evidence was the repository's authority, implementation and course
artifacts, the [existing proposal](../../proposals/thesis-extension-2026-10-18.md),
its [evidence review](../../analysis/thesis-extension-evidence-review.md), and the
two focused reviews:

- [Course-7 targeted review](../i01-course-7-targeted-scientific-literature-review.md).
- [Practical course investigation](../i01-course-practical-literature-investigation.md).

Searches expanded beyond their paper lists. Representative search families
covered distributed/hidden information in LLM teams; debate, voting and
consensus; evidence updating and source conflicts; entity binding and state
changes; memory use in action; repeated evaluation, power, prompt sensitivity
and quantization. References and forward connections were followed where they
could change an actual design decision. The principal chains were:

| Connection followed | Design issue it sharpened |
|---|---|
| MemoryAgentBench → resolver audit and post-retrieval assembly | Updating semantics, gold validity and extraction-versus-policy confounding |
| Entity tracking → binding interventions → state-change counterexamples | Whether task success distinguishes the intended operation from a shortcut |
| Positive debate studies → voting/consensus and sensitivity comparisons | Information gain versus extra computation and decision-procedure changes |
| Hidden profiles → grounding and distributed knowledge | Available facts, accepted information and completed coordinated actions |
| Error-bar methods → NIST hierarchical evaluation → power analysis | Population target, repeated worlds and budget allocation |
| Tuning-budget reporting → its statistical critique | Transparent development without importing a biased maximum estimator |
| Previously reviewed correction studies → context preference controls | Evidence use, misleading answer cues and appropriate negative controls |

Full texts were obtained from primary arXiv HTML/PDF, official ACL PDFs,
institutional/author copies, and Hugging Face's paper-text access. Methods,
results, relevant controls and limitations were read, with selected appendices
according to the decision. Important PDF tables were rendered and inspected
where extraction was unreliable. The ledger does not imply every appendix,
proof, dataset or released implementation was audited.

**D (deep):** methods and results read with consequential controls, analysis or
appendices. **T (targeted):** actual full text consulted for the named question,
with a narrower reading scope. Neither label means independently reproduced.
No external study was executed, and reported numbers were not recomputed from
its raw data. Downloaded papers and reading scripts stayed in temporary research
storage; no model weights were downloaded.

An initial identifier cross-check found 96 arXiv IDs in existing repository
material. This helped distinguish already-cited papers from new leads, but
mere prior citation is not deep prior review, and absent IDs do not prove a
paper was never mentioned. Novelty counts are therefore not a finding.

Selection favors accessible English-language texts and interpretable methods.
This may miss relevant work elsewhere. Recent workshop papers and preprints
are useful for controls and hypotheses but carry less evidential weight than
replicated, well-controlled findings. Transfer to Qwen3.5-9B and Granite 4.2-8B
remains an inference throughout.

## 2. Memory, evidence and state changes

### M01

Yuanzhe Hu, Yu Wang and Julian McAuley. *Evaluating Memory in LLM Agents via
Incremental Multi-Turn Interactions.* [arXiv:2507.05257v4](https://arxiv.org/abs/2507.05257v4),
28 June 2026 revision; first submitted 2025. **D; revisited.** Read §§3–4,
FactConsolidation definition/validation and chunk/top-k/backbone analyses;
compared earlier accessible v2 text with v4. Use v4 results in this package.

### M02

Zexue He et al. *MemoryArena: Benchmarking Agent Memory in Interdependent
Multi-Session Agentic Tasks.* [arXiv:2602.16313v2](https://arxiv.org/abs/2602.16313v2),
17 September 2026. **D.** Read task/dependency construction, memory-agent loop,
§4 comparisons, partial/complete success and latency analyses. Rechecked the
current v2 after initially obtaining v1; the HTML heading shortens the title.
Some model naming and blanket latency prose remain internally inconsistent.

### M03

Egor Pakhomov and Erik Nijkamp. *Bookkeeping, Composition, or Unreachable Gold?
Reading MemoryAgentBench's Conflict-Resolution Scores Against a Frozen
Last-Write Resolver.* [arXiv:2610.09193v1](https://arxiv.org/abs/2610.09193v1),
6 October 2026. **D.** Read resolver development/held-out construction, comparator
limitations, uncertainty and residual taxonomy, including Appendix A. Workshop
acceptance is author-reported in the arXiv comments; treat as a recent audit,
not definitive adjudication of benchmark gold.

### M04

Vikas Reddy and Sumanth Reddy Challaram. *Reliable Post-Retrieval Assembly for
Agent Memory: Separating Evidence Extraction from Policy Execution.*
[arXiv:2606.01435v2](https://arxiv.org/abs/2606.01435v2), 2 August 2026.
**D.** Read extraction/policy setup, LLM-picker comparator, negative update result
and multi-hop comparisons. Earlier versions/search records use *Don't Ask the
LLM to Track Freshness*; this package cites the current title and version.

### M05

Hexiang Tan et al. *Blinded by Generated Contexts: How Language Models Merge
Generated and Retrieved Contexts When Knowledge Conflicts?*
[ACL 2024, long.337](https://aclanthology.org/2024.acl-long.337/).
**D.** Read §§3–5, conflicting-subset construction, model/retriever comparisons,
parametric-answer filtering, completeness controls and Appendix B ordering/
similarity/length checks. Visually inspected Tables 6–7. Correlational similarity
analysis is distinguished from the more controlled truncation comparison.

### M06

Qin Dai, Benjamin Heinzerling and Kentaro Inui. *Representational Analysis of
Binding in Language Models.* [EMNLP 2024, main.967](https://aclanthology.org/2024.emnlp-main.967/).
**T.** Read binding-task construction, PCA/subspace method, causal interventions
and ordering-versus-position controls in §§2–4; inspected additional-model
analysis selectively. This is mechanistic background, not a diagnosis or
intervention adopted for our models.

### M07

Najoung Kim and Sebastian Schuster. *Entity Tracking in Language Models.*
[ACL 2023, long.213](https://aclanthology.org/2023.acl-long.213/).
**D.** Read dataset desiderata, operation generation, evaluation and results,
including lexical mismatch, ambiguous references and move-contents conditions.
Changed-target versus unchanged-target reporting is particularly relevant.
Multiple questions/states from a scenario are not independent worlds.

### M08

Zhuoran Jin et al. *Tug-of-War between Knowledge: Exploring and Resolving
Knowledge Conflicts in Retrieval-Augmented Language Models.*
[LREC-COLING 2024, main.1466](https://aclanthology.org/2024.lrec-main.1466/).
**T.** Read §§3–4: memory induction, conflict generation, metrics and
correct/incorrect internal-answer comparisons. The proposed contrastive decoder
was screened, not independently assessed as an implementation candidate.

### M09

Nelson F. Liu et al. *Lost in the Middle: How Language Models Use Long Contexts.*
[TACL 2024, 1.9](https://aclanthology.org/2024.tacl-1.9/).
**T.** Read multi-document and key-value setups, positional intervention,
closed-book/oracle comparisons and ordering controls. Its relevance is a
rendering/capability caution; no effect size is transferred to our short inputs.

### M10

Zilu Tang, Qiao Zhao, Gabriel Franco, Derry Wijaya, Aaron Mueller, Sebastian
Schuster and Najoung Kim. *Do Language Models Track Entities Across State
Changes?* [arXiv:2605.30233v1](https://arxiv.org/abs/2605.30233v1), 28 May 2026.
**D.** Read §§2–5, probe contrasts, REMOVE interventions and all three behavioral
counterexamples; consulted dataset/model and behavioral appendices selectively.
Claims about state representation are scoped to the probes and interventions.

## 3. Coordination, group decisions and action

### C01

Yuxuan Li, Aoi Naito and Hirokazu Shirado. *Systematic Failures in Collective
Reasoning under Distributed Information in Multi-Agent LLMs.*
[arXiv:2505.11556v4](https://arxiv.org/abs/2505.11556v4), 13 May 2026 revision.
**D.** Read benchmark selection, full/hidden comparisons, discussion/dissent
interventions, disclosure and structured-protocol experiments, and Appendix A
task/intervention details and prompts. “HiddenBench” is a useful search name,
not the bibliographic title.

### C02

Lars Benedikt Kaesberg, Jonas Becker, Jan Philip Wahle, Terry Ruas and Bela
Gipp. *Voting or Consensus? Decision-Making in Multi-Agent Debate.*
[Findings of ACL 2025, 606](https://aclanthology.org/2025.findings-acl.606/).
**D.** Read §§3, 4.1–4.2 and selected implementation descriptions in Appendix C.
Visually checked Figure 2's table after faulty text extraction. Early stopping
and mandatory discussion differ across the compared protocols.

### C03

Hyeong Kyu Choi, Xiaojin Zhu and Sharon Li. *Debate or Vote: Which Yields Better
Decisions in Multi-Agent Large Language Models?*
[arXiv:2508.17536v2](https://arxiv.org/abs/2508.17536v2), 23 October 2025.
**D; revisited.** Read §§3–4, extensions and Appendix A settings; inspected the
theoretical conditions and empirical martingale interpretation. Distinguish the
idealized update theorem from the actual debate experiments.

### C04

Andries Smit, Paul Duckworth, Nathan Grinsztajn, Thomas D. Barrett and Arnu
Pretorius. *Should we be going MAD? A Look at Multi-Agent Debate Strategies for
LLMs.* [arXiv:2311.17371v3](https://arxiv.org/abs/2311.17371v3), 18 July 2024.
**D.** Read strategies, §3 comparisons, hyperparameter transfer, agreement
modulation and limitations; consulted the configuration inventory. Main text
best-result and cross-dataset selection analyses are not interchangeable.

### C05

Yubin Kim et al. *Towards a Science of Scaling Agent Systems.*
[arXiv:2512.08296v3](https://arxiv.org/abs/2512.08296v3), 8 April 2026.
**D; revisited.** Read six-benchmark setup, regression, clustered/multiplicity
qualification, limitations and Appendices C/E. The later publication is titled
[*Capable language models can outgrow the benefits of collaboration*](https://doi.org/10.1038/s42256-026-01268-y),
Nature Machine Intelligence (2026); its publisher full text was inaccessible.
Inspected the authors' v2.2.3 correction notice and conditional selection script,
without executing either. Do not mix earlier four-benchmark and v3 results.

### C06

Saaket Agashe, Yue Fan, Anthony Reyna and Xin Eric Wang. *LLM-Coordination:
Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language
Models.* [arXiv:2310.03903v3](https://arxiv.org/abs/2310.03903v3), 28 April 2025.
**T.** Read game/CoordinationQA setup, verification/ToM ablations, cross-play
comparisons and limitations. The accessible text's internal links identify v3.

### C07

Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum and Igor Mordatch.
*Improving Factuality and Reasoning in Language Models through Multiagent
Debate.* [ICML 2024, PMLR 235:11733–11763](https://proceedings.mlr.press/v235/du24e.html).
**T; revisited.** Bibliography verified against PMLR; reading used
[arXiv v1](https://arxiv.org/html/2305.14325v1), §§2–3 and limitations. This is not
a claim to have audited every appendix of the later proceedings version.

### C08

Herbert H. Clark and Susan E. Brennan. *Grounding in Communication.* In
*Perspectives on Socially Shared Cognition*, 1991, pp.127–149.
[Author-hosted chapter](https://web.stanford.edu/~clark/1990s/Clark%2C%20H.H.%20_%20Brennan%2C%20S.E.%20_Grounding%20in%20communication_%201991.pdf).
**T.** Read presentation/acceptance, purpose-dependent criterion, collaborative
effort and medium constraints in the scanned chapter. Conceptual transfer,
not experimental evidence for a particular LLM protocol.

### C09

Joseph Y. Halpern and Yoram Moses. *Knowledge and Common Knowledge in a
Distributed Environment.* JACM 37(3), 549–587, 1990.
[DOI](https://doi.org/10.1145/79147.79161);
[full text](https://groups.csail.mit.edu/tds/papers/Halpern/JACM90.pdf).
**T.** Read knowledge hierarchy, coordinated attack, local-history/system
definitions and timing assumptions. Not all impossibility proofs were audited.
The 2000 arXiv reprint date is not the original publication year.

### C10

Garold Stasser and William Titus. *Pooling of Unshared Information in Group
Decision Making: Biased Information Sampling During Discussion.* JPSP 48(6),
1467–1478, 1985. [DOI](https://doi.org/10.1037/0022-3514.48.6.1467);
[full text](https://www.uni-muenster.de/imperia/md/content/psyifp/aeechterhoff/vorlesungkommunikation/stasser_titus_unsharedinfogroupdisc_jpsp1985.pdf).
**T.** Read judgmental-task restriction, sampling model, participant/material
construction and pre/post preference results. Human mechanism equivalence is
not inferred. Read through the PDF service when local certificate access failed.

## 4. Evaluation, statistics and configured systems

### S01

Evan Miller. *Adding Error Bars to Evals: A Statistical Approach to Language
Model Evaluations.* [arXiv:2411.00640v1](https://arxiv.org/abs/2411.00640v1),
1 November 2024. **D.** Read repeated sampling, paired comparisons,
power/budget planning and clustered extensions. Applied variance decomposition
to our paired world contrast rather than treating calls as observations.

### S02

Drew Keller, Kweku Kwegyir-Aggrey, Ryan Steed, Anita K. Rao, Julia L. Sharp and
A. Stevie Bergman. *Expanding the AI Evaluation Toolbox with Statistical
Models.* NIST AI 800-3, February 2026.
[Report and DOI](https://doi.org/10.6028/NIST.AI.800-3).
**D.** Read §§3–4, empirical evaluation setup, variance interpretation and §6.2
assumptions/limitations. Fixed items and a superpopulation are distinct targets;
GLMM efficiency is conditional on modeling assumptions.

### S03

Dallas Card, Peter Henderson, Urvashi Khandelwal, Robin Jia, Kyle Mahowald and
Dan Jurafsky. *With Little Power Comes Great Responsibility.*
[EMNLP 2020, main.745](https://aclanthology.org/2020.emnlp-main.745/).
**D.** Read power construction, paired accuracy/disagreement analysis and
empirical assessment in §§2–3. No GLUE effect-size prior was imported into our
study, and no power simulation was run here.

### S04

Jesse Dodge, Suchin Gururangan, Dallas Card, Roy Schwartz and Noah A. Smith.
*Show Your Work: Improved Reporting of Experimental Results.*
[EMNLP-IJCNLP 2019, D19-1224](https://aclanthology.org/D19-1224/).
**T.** Read expected-validation-performance construction and budget-dependent
classification/embedding cases. Followed its estimator to the direct critique S05.

### S05

Raphael Tang, Jaejun Lee, Ji Xin, Xinyu Liu, Yaoliang Yu and Jimmy Lin.
*Showing Your Work Doesn't Always Work.*
[ACL 2020, main.246](https://aclanthology.org/2020.acl-main.246/).
**D.** Read §3 derivation/proof, §4 simulation construction and coverage/ranking
results. Its maximum-estimator critique is not generalized to every bootstrap
mean or used to reject transparent budget reporting.

### S06

Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville and Marc
G. Bellemare. *Deep Reinforcement Learning at the Edge of the Statistical
Precipice.* NeurIPS 2021; [arXiv:2108.13264v4](https://arxiv.org/abs/2108.13264v4),
5 January 2022 revision. **T; revisited.** Read §4 tools, few-run coverage
cautions and discussion; checked the pinned PDF after consulting accessible
full-text Markdown. The evaluated task/run hierarchy differs from ours.

### S07

Melanie Sclar, Yejin Choi, Yulia Tsvetkov and Alane Suhr. *Quantifying Language
Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to
start worrying about prompt formatting.* ICLR 2024;
[arXiv:2310.11324v2](https://arxiv.org/abs/2310.11324v2), 1 July 2024.
**D.** Read format grammar, §4 setup/ranking reversals and Appendix C limitations;
consulted task selection and additional results. Do not extrapolate headline
spread as the expected effect of our action renderer.

### S08

Yao Fu, Xianxuan Long, Runchao Li, Haotian Yu, Mu Sheng, Xiaotian Han, Yu Yin
and Pan Li. *Quantized but Deceptive? A Multi-Dimensional Truthfulness
Evaluation of Quantized LLMs.*
[EMNLP 2025, main.1548](https://aclanthology.org/2025.emnlp-main.1548/).
**T.** Read quantizer/model selection, task construction and output comparisons;
consulted layer-wise analysis. Visually inspected the quantizer/results table.
NF4 and the intended model checkpoints are not tested in this paper.

### S09

Miles Turpin, Julian Michael, Ethan Perez and Samuel R. Bowman. *Language
Models Don't Always Say What They Think: Unfaithful Explanations in
Chain-of-Thought Prompting.* NeurIPS 2023;
[arXiv:2305.04388v2](https://arxiv.org/abs/2305.04388v2), 9 December 2023.
**D.** Read bias interventions, prompting controls, results and limitations.
Counterfactual inconsistency detects a faithfulness failure; passing a limited
test does not prove faithful reasoning.

## 5. Important previously reviewed work revisited

### R01

Alex Kwon. *Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One.*
[arXiv:2606.25449v5](https://arxiv.org/abs/2606.25449v5), 21 July 2026.
**D.** Read note construction, source-first/length controls, capability and
source-size boundaries, deployed-interface distinctions and selected correction
robustness appendices. Distinguish its planted wrong commitment from our
formerly correct answer made stale by an external edit.

### R02

Shixuan Li et al. *Beyond Final Accuracy: Auditing Communication in LLM
Multi-Agent Systems.* [arXiv:2610.01042v1](https://arxiv.org/abs/2610.01042v1),
1 October 2026. **D.** Read independent–communicate–revise setup, correction/
corruption strata, no-message controls, question bootstrap and generation/
processing settings. This controlled directed-revision audit differs from our
interactive recovery loop.

### R03

Wenhui Chu. *When Evidence Changes: Evaluating Memory Repair and Re-reading in
Language-Model Agents.* [arXiv:2610.03902v1](https://arxiv.org/abs/2610.03902v1),
2 October 2026. **D.** Read tasks, pipelines, cost identity, source-filtered
length sweep, replacement results and limitations; inspected Appendix J's
confirmatory plan, outcomes and protocol erratum. Post-hoc scorer and pooling
analyses remain separate from prespecified comparisons.

### R04

Asa Shepard. *What It Costs to Compose, Rebuild, and Correct Precomputed
Memory.* [arXiv:2608.30647v1](https://arxiv.org/abs/2608.30647v1), 31 August 2026.
**D.** Read substrate/common setup, §6 correction factorial, screening, padding,
wrong-naming control and limitations; consulted appendix screening/reporting
details. Cache/cartridge composition is background, not proposed infrastructure.

## 6. Non-paper primary sources and unresolved access

- **Qwen:** [pinned model repository](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a).
  Inspected configuration and model-card generation/mode guidance. No
  `generation_config.json` was available at this revision. Conflicting presets
  within the card must be resolved by an explicit chosen setting, not a claim
  of one unambiguous official default.
- **Granite:** [pinned model repository](https://huggingface.co/ibm-granite/granite-4.2-8b/tree/f8de16cdcdbc6c779ca517604e050d82cc119e44).
  Inspected configuration, generation configuration and mode guidance. These
  are vendor specifications and recommendations, not our hardware or capability
  acceptance results.
- **Agent-scaling corrections:** [v2.2.3 changelog](https://github.com/ybkim95/agent-scaling/blob/v2.2.3/CHANGELOG.md)
  and [conditional architecture-selection protocol](https://github.com/ybkim95/agent-scaling/blob/v2.2.3/scripts/architecture_selection_eval.py).
  Source read only; reported reproduction assertions were not executed here.
- **Screened, not used as a foundation:** *Certified Sequential Inference for
  Repeated-Sampling LLM Evaluation*, [accessible manuscript](https://langaigenerative.github.io/test/paper.pdf).
  The copy is anonymous and labeled an ACL submission; authorship, archival
  acceptance and version were not verified. Its claims do not justify a
  sequential-stopping design or replace S01–S03.

Two full-text mirrors initially returned older versions of M01 and M02; current
primary versions were retrieved before synthesis. C05's initial mirror was also
older than the six-benchmark v3 used here. Search snippets can retain old titles,
abstracts or numbers. Author, title, version and actual reading source are
therefore recorded separately. The inaccessible final C05 publisher text is the
main unresolved publication-access limitation.

## 7. Evidence discipline for the next design session

Treat a reported experiment as evidence under its actual task, model, budget,
information and scoring conditions. Treat authors' explanations without an
isolating intervention as hypotheses. Treat every proposed application here as
our inference until tested. No paper result supplies authorization, guarantees
our model competence, or changes the repository's scientific authority.
