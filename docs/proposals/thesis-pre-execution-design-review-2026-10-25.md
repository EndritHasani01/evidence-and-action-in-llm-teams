# Pre-execution design review of `thesis-recovery-v1`

**25 October 2026 · independent review written at the project author's request**

**Outcome (25 October 2026):** the user approved R1, R2 and R3, including the
optional R3(b) and R3(c). They are now part of the adopted annex
([thesis-project-specification.md](thesis-project-specification.md)) and are
implemented and CPU-verified ([implementation evidence](../validation/thesis-implementation.md)).
Before implementation, the world count was reassessed and kept at 192 with the
128 fallback ([annex §3.10](thesis-project-specification.md#310-statistical-analysis)).
Later the same day the user set the main population to **64 worlds** (8 per
stratum); the annex records the resulting precision, power and limitations.
The body below is the review as written; section 10 records the decisions.

This review assesses the adopted thesis design
([PROJECT_SPECIFICATION.md §13](../../PROJECT_SPECIFICATION.md#13-thesis-regime-thesis-recovery-v1)
and its [annex](thesis-project-specification.md)) before any GPU work. It changes
no code, configuration, specification, manifest or experimental artifact, and
it authorizes nothing. Section 10 separates the recommendations from the
decisions that are actually in force.

Evidence labels used below:

- **Verified:** checked directly in this session against repository data, code
  or a primary source.
- **Derived:** my arithmetic or simulation on verified inputs.
- **Literature:** a published finding, checked at the abstract/listing level.
- **Inference:** my judgment.
- **Open:** cannot be settled before GPU execution.

---

## 0. Bottom line

The adopted design is sound. Its central addition, a matched no-change
reopening, is the right control for the question the course could not answer.
Its statistics, isolation, missingness handling and compute plan hold up under
checking. The 3-call budget, the prompts, the 192-world target and the two models
should all stay as they are. The evidence for keeping each is given below.

The review found one consequential gap and several cheap analysis gaps:

1. **Δ_E cannot tell *what* about a change hurts the team.** The revision cells
   bundle two things: being told that a record changed, and the answer actually
   changing. The design also never tests whether a team **preserves** a
   conclusion that stays valid after a real change, which is half of the
   project's stated purpose (spec §1). **Recommendation R1:** add a real
   answer-preserving change as a third event level on every world. It runs as
   two more sibling cells, retain and clear. This yields an exact decomposition
   Δ_E = Δ_announce + Δ_answer at about +37% inference. The primary estimands
   are unchanged.
2. **The primary outcome mixes two opposite failure modes.** In the assisted
   interface, which the thesis inherits, about half of all recovery failures
   were teams that never committed: agents looped messages until their calls ran
   out. Under the unassisted course prompt, failures were instead early wrong
   commitments. **Recommendation R2:** before main, prespecify four secondary
   analyses that use no inference:
   - a formal reopening contrast;
   - the completion and wrong-commitment channels of each primary;
   - estimates within correct-prefix and incorrect-prefix worlds;
   - a self-repetition diagnostic.
3. **Minor fixes (R3):**
   - Describe Qwen's decoding precisely: the card recommends a presence penalty
     of 1.5; the thesis deliberately uses 0.
   - Optionally make the two notice texts symmetric.
   - Optionally add one rule-clarifying sentence about waiting after the
     partner has finished.

With R1 the campaign ceiling becomes 18,644 attempts. Expected main inference is
about 30 aggregate GPU-hours at Qwen's measured speed, against 22 under the
adopted design, so the 100-hour ceiling is kept. The one real cost: if Granite
runs slower than about 21 allocated GPU-seconds per call, the existing forecast
rule drops both models to 128 worlds. Under the adopted design that threshold is
about 32 s.

If the author prefers no scientific-design amendment at all, the adopted design
is defensible as it stands. In that case adopt R2 alone: it costs no GPU time
and protects the interpretation of every primary result.

---

## 1. What was examined

| Source | Use |
|---|---|
| Specification §13, the annex (sections 1–12) and the final course report | The contract under review and its stated rationale |
| `recovery/thesis/protocol.py`, `analysis.py`, `configs/thesis.json`, `configs/thesis-worlds.json` | The implementation actually reached by the contract |
| Canonical exports of the assisted campaign (`notebooks/run/assisted-v1/latest`) and Course-7 (`notebooks/run/course-7-working/latest`): `run.json`, `reports/conversations.jsonl`, `reports/attempts.csv` | New failure classification, repetition counts, throughput check (Appendix A) |
| The 18 and 22 October proposals, the literature package and the study recommendation | Alternatives already considered, so this review does not repeat them |
| Hugging Face model cards (Qwen3.5-9B, Granite 4.2-8B); 2023–2026 literature listed in §4 | External facts and published evidence |
| Monte Carlo of the adopted stratified percentile bootstrap (scratch script, method in Appendix B) | Interval width and coverage at N = 96, 128 and 192 |

---

## 2. Assessment of the adopted design

### 2.1 Strongest aspects

| Aspect | Why it matters | Status |
|---|---|---|
| Matched no-change reopening (RN, CN) | The course could not separate "the change hurts" from "being reopened hurts" ([report §5.5](../reports/final-course-report-submission.md#55-why-improved-collaboration-did-not-produce-reliable-recovery)). Δ_E answers that directly | Verified as specified and implemented |
| Four sibling continuations from one saved natural prefix | Within-world pairing removes input and prefix variance from every contrast. Correlated cell outcomes shrink interval widths by about 10–20% in simulation | Verified (code); Derived (simulation) |
| No gate after the phase boundary | Prevents admitting or excluding a model on the outcomes being studied | Verified |
| Balanced 8-stratum generator with a nested 128-world fallback; demote and keep edits | Covers decreasing and increasing answers. In the 96 keep worlds the new answer is a value only its owner has seen, so it must be communicated | Verified (manifest) |
| Exact estimands, missingness bounds, no interim analysis, a prewritten licensing table | Limits analytic flexibility; a null result stays informative | Verified |
| Two model families under one fairness boundary | Replication, not one-system anecdote | Verified |
| Reuse of the only runtime that has run on Kaggle | Two complete campaigns, exact resume, independent verifier | Verified |

Arithmetic checked and found correct (**Verified/Derived**):

- **Precision table (annex §3.10):** e.g. 2.241·√(0.3/192) = 8.86 pp.
- **5-point detection:** needs about 1,140 worlds.
- **Hoeffding companions:** 21.4 pp (N = 192) and 26.2 pp (N = 128).
- **Attempt ceilings:** 13,652 and 9,556.
- **GPU-hour sensitivity:** 44.2 h at g = 8.7 s; the ceiling holds to g ≈ 20.5 s.
- **Forecast example:** F(192) = 60.5.
- **Measured throughput:** 278 main calls over 1,208.8 s = **8.70** allocated
  GPU-s/call (attempt timestamps). Note that the pilot stage ran at **12.49**,
  so development-stage `g` may be measured above the main-stage rate.

No prompt confound between cells was found. The system text is identical in all
cells. User messages differ only in history, notice, current shard and the
owner's replacement line, as intended.

### 2.2 Weaknesses, in order of consequence

**W1. The revision cost cannot be attributed (consequential).** A revision cell
differs from a no-change cell in three ways:

- an announcement naming a changed record;
- a changed value supplied to its owner;
- a changed correct answer, plus staleness of any retained history.

Δ_E sums all three by construction (annex §3.9). These have opposite practical
implications:

- If the *announcement* disrupts, a system should avoid broadcasting changes
  that do not matter.
- If only *answer changes* hurt, the problem is integrating new information.

The course data contain a hint that the notice itself disrupts:

- Agents asked their partner about the changed record, e.g. "What is your max
  for record 19?" in `main-02/clear`.
- Local-maximum claims fell from 45/45 correct before the change to 22/28–29/34
  after it ([22 Oct reasoning §2.2](thesis-final-reasoning-2026-10-22.md#22-local-extraction-degrades-after-a-revision-verified-new)).

The adopted design also never presents a real change that leaves the answer
valid. The specification's own research question is "preserving useful previous
work without allowing obsolete work to harm the revised result". RN tests
preservation only when *nothing* changed. The course report named this exact
gap ([§5.8](../reports/final-course-report-submission.md#58-limitations), [§5.9](../reports/final-course-report-submission.md#59-implications-and-future-work)).
Earlier proposals scoped the fix as a 32-world side panel, which the annex
rightly dropped as too imprecise (annex §2.3). Run on all worlds instead, it
becomes precise and decomposes Δ_E exactly (§7).

**W2. Exact team success conflates commitment with correctness (consequential
for interpretation).** In the assisted campaign, whose interface the thesis
inherits almost verbatim, about half of the recovery failures contain no wrong
submission at all (§3). The agent either never submits, or loops a message until
its three calls are spent. Course-7, under a different prompt, failed the
opposite way: 35 of 36 recovery failures were completed wrong answers. A Δ_H or
Δ_E estimate can therefore move because history or a change alters *willingness
to commit*, not *what the team knows*. The annex lists completion and
wrong-agreement only as descriptive counts (S7). The implementation reports
them as funnel counts without intervals (`analysis.py`, `model_result`).
Without a prespecified channel analysis, any primary result is open to the
reading "it is an interface artifact".

**W3. The "reopening is the problem" conclusion has no estimand.** Annex §3.11
licenses that conclusion when "Δ_E ≈ 0, both events low". That compares the
cells with the prefix rate only informally. The prefix and CN share inputs and
first speaker and differ only by the phase line, the notice and the seeds, so
Y_prefix − Y_CN is a clean paired within-world contrast. It is computable from
data the design already collects.

**W4. Prefix correctness is reported as counts only.** The prefix is shared by
all four cells, so its correctness is pre-treatment for the continuations.
Subgroup effects conditional on it are therefore valid causal contrasts, not
post-treatment selection. "Recovery after successful collaboration" is
arguably the construct the thesis title promises. About half of all prefixes
will be wrong (course: 10/20), and retaining a wrong history is a different
intervention from retaining a right one.

**W5. Minor issues.**

- **(a) Decoding description.** The annex calls Qwen's decoding
  "model-native", but the current card's non-thinking setting includes
  `presence_penalty=1.5` (**Verified**, model card). The thesis uses 0, as the
  course did, and the earlier literature package discussed this. The choice is
  defensible: a presence penalty on generated tokens would penalize copying a
  number from `message` into `submit` within one JSON reply. It also would not
  stop cross-call copying, because that copying is from the prompt. The text
  should say "card temperature, top-p and top-k; presence penalty 0, a
  deliberate deviation".
- **(b) Notice asymmetry.** The no-change notice ends "A new phase began."; the
  change notice does not. The phase line already says "new phase" in every
  continuation, so the effect is probably negligible. It is still an unintended
  wording difference inside Δ_E.
- **(c) Waiting trap.** Waiting after the partner has finished ends a phase at
  once (`waiting_deadlock`). The prompt does not state this consequence. It
  caused 3/20 assisted prefix deadlocks: 4 such waits in prefixes, 1 in retain
  and 1 in clear (**Verified**). It mainly lowers prefix quality.

**Checked and judged *not* to be weaknesses.**

- **Common random numbers across cells.** Valid variance reduction; each cell's
  marginal distribution is unaffected.
- **Device assignment and cell order.** Recorded, not designed; harmless for a
  stateless model with all cells of a world on one GPU.
- **The bootstrap.** Near-nominal at N = 192 (§6.3).
- **"A message is a claim, not a certified source."** This wording could
  discourage uptake of partner values. However, the Course-7 prompt had similar
  wording ("claims are not certified") and *more* own-maximum fallbacks, so
  there is no evidence that this sentence causes the uptake failure.

---

## 3. What the executed campaigns show

Classification of every main episode in the two executed campaigns (**Verified**;
method in Appendix A). "Non-commitment" means no wrong submission, at least one
agent absent.

| Campaign, main (20 worlds per phase) | Success | Non-commitment only | Completed wrong | Wrong and absent |
|---|---:|---:|---:|---:|
| Assisted, prefix | 10 | 4 | 6 | 0 |
| Assisted, retain recovery | 2 | **11** | 6 | 1 |
| Assisted, clear recovery | 3 | **8** | 7 | 2 |
| Course-7, prefix | 3 | 8 | 8 | 1 |
| Course-7, retain recovery | 2 | 0 | **18** | 0 |
| Course-7, clear recovery | 2 | 1 | **17** | 0 |

Agent-slot detail for the assisted recoveries (**Verified**):

| Assisted, 40 agent slots | Correct | Absent | …of which: used all 3 calls, last action message-only | Wrong: own local maximum | Wrong: other |
|---|---:|---:|---:|---:|---:|
| Prefix | 30 | 4 | 0 (all 4 ended waiting) | 6 | 0 |
| Retain | 14 | 18 | **17** | 4 | 4 |
| Clear | 18 | 11 | **10** | 8 | 3 |

Further facts that bear on the design:

- **Loops are retention-amplified.** Among failed episodes, 13 retain agents sent
  the identical message on all three calls, against 4 under clear and 0 in the
  prefix. Retained earlier-phase entries are rendered as "Your action: …", and
  agents copy them (e.g. `main-00/retain`, `main-05/retain`). This is consistent
  with self-conditioning (§4). It means Δ_H will partly measure a copy-loop
  mechanism, which R2's repetition diagnostic makes visible. (**Verified**
  counts; mechanism is **Inference**.)
- **More calls would rescue little.** In only 2 of 11 retain and 2 of 8 clear
  non-commitment failures had every absent agent already stated the correct
  value, e.g. "954 is the global max. I will submit." with `submit: null`. The
  other absences were identical-message loops, which a fourth call would most
  likely extend. (**Verified**; the rescue estimate is **Inference**.)
- **The failure profile depends on the interface.** The assisted prompt produced
  over-caution; the unassisted prompt produced premature, often stale (14 old-answer slots under retain), commitment.
  The thesis inherits the assisted interface, so expect non-commitment to
  dominate unless the new phase rule ("both agents must submit again") changes
  it. (**Inference**; development will show it.)
- **Holder location.** In the thesis main manifest the revised answer stays
  with the changed owner in 139/192 worlds: all 96 keep worlds and 43 demote
  worlds. It moves to the partner in 53 demote worlds. These are the only
  worlds where the retained partner report is still the answer, so they are
  where retained evidence can help most. (**Verified**)

---

## 4. Relevant literature

| Finding | Source | Implication for the design |
|---|---|---|
| Agents exchange information actively but fail to integrate it into correct distributed computation ("communication–reasoning gap") | [SILO-BENCH, ACL 2026](https://aclanthology.org/2026.acl-long.1354/) | Matches the assisted pattern: delivered, not used or not committed. Supports measuring channels (R2), not only success |
| Multi-agent groups score 30.1% against 80.7% for single agents with full information. Failures persist across prompting strategies, **communication depths** and group sizes | [Li, Naito & Shirado, HiddenBench, ICML 2026](https://arxiv.org/abs/2505.11556v3) | Evidence against adding rounds as a fix. Supports the scalar controls as a capability anchor |
| In debate, belief in the correct answer is a martingale over rounds; majority voting explains most debate gains | [Choi, Zhu & Li, NeurIPS 2025](https://arxiv.org/abs/2508.17536v2) | More interaction opportunities need not improve outcomes on average |
| Merely challenging a model ("Are you sure?") flips answers about 46% of the time and lowers accuracy by about 17% on average | [Laban et al., FlipFlop](https://arxiv.org/abs/2311.08596) | A reopening alone can damage a correct decision, which motivates the reopening contrast (R2) and the preserving cells (R1) |
| Models good at updating beliefs often fail when no update is warranted (update/maintain trade-off) | [Wilie et al., Belief-R, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.586) | The adopted design tests only the update side after a real change; R1 adds the maintain side |
| Irrelevant information in context sharply reduces accuracy | [Shi et al., GSM-IC, ICML 2023](https://arxiv.org/abs/2302.00093) | An irrelevant change notice may itself disrupt; Δ_announce (R1) measures this |
| Models answer with superseded values even when the update is in context; probes still recover the current value (selection, not memory failure) | [Guo et al., CICM, 2609.38866](https://arxiv.org/abs/2609.38866v1) (preprint) | Retention can harm through selection; the funnel's "old answer" class remains needed |
| Models err more when their context contains their own earlier errors; scale does not fix this; thinking mitigates it | [Sinha et al., ICLR 2026](https://arxiv.org/abs/2509.09677) | Consistent with the 13-vs-4 retain loop count; direct mode is where the effect should be strongest |
| Correct reasoning does not guarantee the corresponding action (knowing–doing gap) | [Schmied et al., 2504.16078](https://arxiv.org/abs/2504.16078) | Supports separating commitment from correctness (R2) |
| Premature termination and information withholding are distinct multi-agent failure classes | [Cemri et al., MAST, NeurIPS 2025](https://arxiv.org/abs/2503.13657v2) | Supports reporting termination channels explicitly |
| CLT-style intervals are too narrow on benchmarks below a few hundred items | [Bowyer et al., ICML 2025](https://arxiv.org/abs/2503.01747) | Checked by simulation (§6.3): the stratified percentile bootstrap is near nominal at 192 paired worlds, slightly narrow at 96–128 |
| Treat evals as experiments: pair, cluster, prefer more items over resampling | [Miller, 2411.00640](https://arxiv.org/abs/2411.00640) | Supports the adopted choice of no repeat panel and world-level resampling |

Novelty check: a targeted search found adjacent 2026 work on stale plans and
context synchronization in agent systems, e.g. [PlanFence, 2609.03340](https://arxiv.org/html/2609.03340v1)
and [SyncPlan, 2608.01652](https://arxiv.org/pdf/2608.01652). It also found
mixed practitioner evidence on context compaction, e.g. [2606.10209](https://arxiv.org/html/2606.10209v1).
It found no controlled retain-versus-clear experiment after a source change with
a matched no-change control in LLM teams. (**Literature**, abstract-level; this
is consistent with the repository's earlier novelty statement.)

---

## 5. Alternatives considered

Each alternative is judged on what it would identify, what it costs, and what it
risks for causal interpretation.

| # | Alternative | What it buys | Cost and risk | Verdict |
|---|---|---|---|---|
| A0 | Keep the adopted design unchanged | Answers Δ_E and Δ_H as specified | Δ_E unattributable (W1); channels and reopening informal (W2–W4) | Defensible fallback |
| **A1** | **Add answer-preserving change cells RP and CP on every world** | Exact Δ_E = Δ_announce + Δ_answer; tests whether still-valid work survives a real change | +12 worst-case calls per world per model (+37.5%); manifest regeneration and CPU re-verification; lowers Granite's speed tolerance at N = 192 from about 32 s to 21 s | **Recommended (R1)** |
| A1′ | RP only (retain) | Maintain-side test with history; partial decomposition under retain | +19% calls; no decomposition of the averaged Δ_E | Acceptable reduced variant |
| A2 | 4–5 calls per agent | Fewer horizon failures | +31–63% worst-case calls; changes the construct relative to the course. Evidence (§3, HiddenBench, debate martingale) suggests loops lengthen rather than resolve; at most about 2 rescues per policy in the course data | Not recommended |
| A3 | Final-call salience ("last call: submit now") or forced final commitment | Higher completion | Removes the non-commitment behavior that may *be* the revision effect; host steering | Not recommended |
| A4 | Fewer worlds (128 or 160) to fund A1 | Holds compute flat | Δ_H half-width rises 10–22%; compute is not binding (§6) | Not needed; the existing forecast rule already falls back to 128 if Granite is slow |
| A5 | More worlds (256) | Δ_H half-width −13% | +33% calls for a small gain | Low value |
| A6 | Repeat-continuation panel | Within-world variance component | Beats new worlds only if within-world variance exceeds about 6× between-world variance (Derived); descriptive only | Not recommended (agrees with annex) |
| A7 | Controlled supplied histories (H0/HS/HSC) | Isolates the old-conclusion effect | Artificial start; targets anchoring, which the assisted data do not single out | Not recommended (agrees with annex) |
| A8 | Thinking mode | Likely higher capability, less self-conditioning | About 91× ready time measured in course-3; infeasible on T4 at this scale | Infeasible; state as a scope limit |
| A9 | Common decoding for both models | Cleaner cross-model contrast | Departs from Granite's card (temperature 1.0 and top-p 0.95 "across all tasks") | Keep vendor settings; cross-model contrast is descriptive anyway |
| A10 | Reword "a message is a claim" to boost uptake | Maybe higher needer uptake | No evidence it causes the failure (§2.2) | Not recommended |
| A11 | Exact or Bayesian intervals instead of the bootstrap | Better small-n coverage | Bootstrap already near nominal at N = 192 (§6.3) | Not needed |
| A12 | Qwen only | Half the compute, no Granite risk | Loses replication; the pre-approved exclusion rule already handles a Granite failure | Not recommended |

---

## 6. Costs, compute and precision

### 6.1 Attempts and GPU-hours (Derived from verified inputs)

Expected usage applies the course's measured 72% of team call slots (258/360)
and the measured 8.70 allocated GPU-s/call to both models. Granite's speed is
**Open**.

| Configuration | Worst-case calls per world per model | Main, both models, worst case | Main, expected | Expected aggregate GPU-h (wall h on T4×2) | Campaign attempt ceiling |
|---|---:|---:|---:|---:|---:|
| Adopted, 4 cells, N = 192 | 32 | 12,288 | ~9,060 | ~21.9 (~11.0) | 13,652 |
| **R1, 6 cells, N = 192** | **44** | **16,896** | **~12,380** | **~29.9 (~15.0)** | **18,644** |
| R1, 6 cells, N = 160 | 44 | 14,080 | ~10,300 | ~24.9 (~12.5) | 15,828 |
| R1, 6 cells, N = 128 (fallback) | 44 | 11,264 | ~8,250 | ~19.9 (~10.0) | 13,012 |

Worst-case whole-campaign sensitivity for R1 at N = 192, using the annex's own
formula `3 + 1.25 × attempts × g / 3600`:

| g (s/call) | 8.7 | 12 | 15 |
|---|---:|---:|---:|
| GPU-h | 59.3 | 80.7 | 100.1 |

The ceiling holds the target to g ≈ 15.0 s and the fallback to g ≈ 21.5 s. The
binding rule remains the measured forecast F(N), which needs its per-world
constant changed from 32 to 44. With H_spent = 6 and Qwen at 8.7 s:

- **Adopted design:** F(192) ≤ 100 while Granite's g ≤ 31.9 s.
- **R1:** F(192) ≤ 100 while Granite's g ≤ 21.2 s.
- Above those speeds, both models run 128 worlds.

Kaggle's documented 30 GPU-hours per week makes calendar time and session
logistics, not GPU-hours, the practical constraint in either configuration.

### 6.2 Precision of the primaries (Derived)

The 97.5% half-width for Δ_H is 2.241·√(q/N), where q is discordance:

| N | q = 0.25 (course) | q = 0.30 |
|---:|---:|---:|
| 192 | 8.1 pp | 8.9 pp |
| 160 | 8.9 pp | 9.7 pp |
| 128 | 9.9 pp | 10.9 pp |

R1 does not change N or the primaries, so their precision is unchanged at
N = 192. Δ_announce and Δ_answer have the same structure as Δ_E. By the same
variance argument, their 95% half-widths should be comparable to Δ_E's: about
6–8 pp at N = 192 (**Derived/Inference**).

### 6.3 Simulation of the adopted bootstrap (Derived)

The simulation used:

- correlated binary cells (probit, latent world effect ρ ∈ {0, 1});
- 8 strata;
- 600 replications;
- 2,000 stratified percentile-bootstrap draws each (the adopted method uses
  10,000);
- 97.5% intervals for Δ_E and Δ_H, and 95% for the reopening contrast.

Monte Carlo SE of coverage is about ±0.6 pp at 97.5% and ±0.9 pp at 95%.

| Scenario: prefix, RV, CV, RN, CN | N | Δ_E half-width / coverage | Δ_H half-width / coverage | prefix − CN half-width / coverage (95%) |
|---|---:|---|---|---|
| Course-like floor: .50, .10, .15, .45, .40 (ρ = 0) | 192 | 6.6 pp / .972 | 7.4 pp / .965 | 9.6 pp / .938 |
| same | 128 | 8.0 / .970 | 9.0 / .957 | 11.7 / .935 |
| Moderate: .55, .25, .30, .65, .50 (ρ = 0) | 192 | 7.4 / .977 | 9.9 / .972 | 9.7 / .943 |
| same | 128 | 8.9 / .970 | 12.0 / .953 | 11.8 / .930 |
| Reopening collapse: .50, .10, .12, .15, .15 (ρ = 0) | 192 | 5.3 / .970 | 6.9 / .968 | 8.5 / .933 |
| With ρ = 1, all scenarios, N = 192 | 192 | 4.6–6.3 / .963–.987 | 6.0–8.2 / .965–.978 | 7.3–7.9 / .932–.948 |

Conclusion: the adopted primary intervals are near nominal at N = 192. At 128
they fall up to about 2 points short of nominal. The 95% secondaries undercover
by up to about 2 points, which is acceptable for descriptive estimates but worth
one sentence in the thesis. The bootstrap needs no change.

---

## 7. Final recommendation

**Keep the adopted `thesis-recovery-v1` design, with one design amendment (R1)
and one analysis amendment (R2), both decided before any GPU session. Also
apply the documentation fix R3(a), and optionally R3(b) and R3(c).**

Unchanged:

- the task;
- the 3 calls per agent and the termination rules;
- the system and user prompts (except the optional R3 items);
- the 8 strata, 192 worlds, 16 development worlds and the 128 fallback rule;
- both pinned models and their decoding;
- the gates, freeze and authorization flow;
- the Δ_E and Δ_H primaries at 97.5%;
- the bootstrap, missingness rules and failure rules.

### R1. Answer-preserving change cells on every world

- **Generator.** For each world, a separate stream
  `Random(seed_for(MASTER, world_id, "preserving"))` picks:
  - a record r′ uniformly from the owner's 19 non-winning positions;
  - a replacement uniformly from {−1000,…,M1−1} minus the old value.

  The winner M1 is untouched, so the answer and *both* agents' local maxima are
  unchanged. All existing manifest fields keep their values. The manifest is
  regenerated with added fields and a 6-cell order, then re-committed and
  re-checked for separation.
- **Cells.**
  - RP: retain, preserving change.
  - CP: clear, preserving change.

  Current shards are the preserving shards and the answer is the original. The
  notice uses **exactly the revision notice form**: changed record r′, with the
  replacement value for the owner only. Agents therefore cannot tell from the
  notice that the answer survived. Continuation seeds, isolation and retention
  are as for the other cells.
- **Secondary estimands** (95%, alongside S3), each an exact world-level
  identity:

  ```text
  Δ_announce = ½[(Y_RN − Y_RP) + (Y_CN − Y_CP)]    disruption from a change that leaves the answer valid
  Δ_answer   = ½[(Y_RP − Y_RV) + (Y_CP − Y_CV)]    cost of the answer actually changing
  Δ_E        = Δ_announce + Δ_answer
  ```

  Also report RP − RN and CP − CN separately. For RP and CP, classify wrong
  submissions with the existing funnel classes; a submission other than M1 is
  an unnecessary revision.
- **Licensing additions** to annex §3.11:

  | Pattern | Defensible conclusion |
  |---|---|
  | Δ_announce > 0 | Announcing a change disrupts the team even when nothing it needs has changed |
  | Δ_announce ≈ 0 and Δ_answer > 0 | Irrelevant changes are absorbed; the cost lies in obtaining and adopting new information |
  | RP < RN under retain | Still-valid retained conclusions are abandoned after a real but irrelevant change (over-revision) |
- **Ceilings and forecast.**
  - Main: 44 calls per world per model.
  - Development: 16 × 44 × 2 = 1,408.
  - Campaign: 18,644, or 13,012 at the 128 fallback.
  - Forecast constant: 32 → 44.

  Primaries, multiplicity and the "both models" rule are unchanged.
- **Why this addition and not another.** It is the only candidate that adds a
  new *identified* quantity at a cost the budget absorbs. It splits the primary
  result into two components with opposite practical meanings. It also supplies
  the "preserve what is still valid" test that the project's research question
  names. It requires no new notice text, prompt or protocol rule. A reduced
  variant (RP only, +19%) keeps the maintain test but drops the decomposition.

### R2. Prespecified secondary analyses that use no inference

Freeze these before development data exist, so the choice cannot depend on any
model output.

1. **Reopening effect:** Y_prefix − Y_CN (95%), with Y_prefix − Y_RN
   descriptive. This formalizes the "reopening is the problem" row of annex
   §3.11.
2. **Channels of each primary:** the same linear contrasts on two
   unconditional episode indicators: C = both agents submitted, and
   K = at least one submitted value is wrong (95% each). These are reported side
   by side, not as an additive decomposition. This separates "teams stopped
   committing" from "teams committed wrongly".
3. **Prefix-conditional effects:** Δ_E and Δ_H within correct-prefix and
   incorrect-prefix worlds (95%), with subgroup sizes. Resample worlds within
   strata and compute subgroup means per draw. Prefix correctness is
   pre-treatment for all continuation cells.
4. **Self-repetition diagnostic:** per episode and cell, whether an agent sends
   a message identical to one of its own earlier messages from this or the
   earlier phase. Descriptive counts only.

Item 4 can be extended with a descriptive split of Δ_H by revised-answer holder
location (owner or partner, Verified 139/53 in main).

### R3. Fixes

- **(a) Documentation.** Replace "model-native sampling" for Qwen with an exact
  statement: card temperature, top-p and top-k; presence penalty 0 by deliberate
  choice; why.
- **(b) Optional.** Append "A new phase began." to the change notice so that
  revision and no-change notices differ only in content. This also applies to
  RP and CP under R1.
- **(c) Optional.** Add one rule sentence: "A finished partner cannot send
  messages, so waiting after your partner has finished ends the phase without
  your submission." This states an existing rule; it gives no correctness
  feedback. It mainly affects prefix quality (§2.2 W5(c)) and applies equally
  to every cell. Adopt it only together with R1, because it is another
  untested wording change.

---

## 8. Validation plan

### Before any GPU use (CPU; already authorized scope if R1–R3 are adopted)

| Check | Pass condition |
|---|---|
| Manifest regeneration | Every pre-existing field of all 208 worlds is unchanged in value; new fields satisfy r′ ≠ r, replacement < M1, replacement ≠ old value; both agents' local maxima and the answer unchanged; independent recomputation; separation receipt regenerated |
| Notice and witness | RP/CP notice is byte-identical in form to RV/CV apart from record index and owner value. For the non-owner, the first RP and RV views differ only in the record index while the answers differ |
| Retention and privacy | RP earlier-phase block byte-identical to RV and RN; CP empty; forbidden-label scan covers the new cells (no "preserving", no answer) |
| Capacity | Worst-case request unchanged (same history and shard lengths); recompute the bound anyway |
| Analysis fixtures | Per-world identity Δ_E = Δ_announce + Δ_answer on synthetic tables; the hand-scored example of annex §3.10 still reproduces; fixtures for reopening, C/K channels and prefix subgroups with known signs |
| Ceilings and forecast | Tests updated to 44 calls per world; the 192/128 decision reproduces the Derived thresholds in §6.1 |
| Rehearsal | Two Kaggle CPU `rehearsal` sessions with a deliberate restore, as already planned |

### Record before development (decisions, not code)

- Development continuation outcomes, including floor-level results, will not
  change cells, prompts, call budget or N. Main proceeds if G1–G4 pass. A floor
  result is a prewritten, informative outcome (annex §3.11 plus R2 item 1).
- Confirm whether Granite gets no decoding fallback on a G3 legality failure.
  The current annex rule excludes Granite in that case. Decide this now, not
  after seeing development data.

### Development and main

As in annex §4, with the 6-cell schedule. Additionally record:

- the Kaggle quota before and after the first GPU session;
- development-stage `g` per model, compared with the 8.70 main-stage and 12.49
  pilot-stage course rates.

---

## 9. Remaining uncertainties

| Uncertainty | Why it matters | Resolved by |
|---|---|---|
| Granite NF4/FP16 numerics, JSON legality at temperature 1.0, speed on T4 | Exclusion or a forced 128-world main; tighter under R1 | Development G1–G3 and measured `g` (**Open**) |
| Whether the new phase rule and owner labels change the failure profile | Determines whether results are commitment-dominated (W2) | Development outcomes, descriptive (**Open**) |
| Whether revision cells sit at the floor | Δ_H would then be bounded, not detected; R2 keeps that interpretable | Main (**Open**) |
| Whether reopening alone collapses teams | If so, Δ_E ≈ 0 and Δ_announce adds little; the reopening contrast carries the result | Main (**Open**) |
| Kaggle T4×2 quota charging and availability | Calendar time, not GPU-hours, is the binding constraint | First GPU session (**Open**) |
| GPU nondeterminism when lost work is re-executed | Rerun draws may differ from the lost ones; already recorded by design | Session records (**Open**) |
| External validity: one numeric task, two agents, direct mode, quantized models | Limits generalization; thinking mode is infeasible here | Stated as scope (**Inference**) |

---

## 10. Decision status

| Item | Status |
|---|---|
| Specification §13 and its annex | **In force, amended 25 October 2026** with R1–R3 below |
| R1: answer-preserving cells (RP, CP), regenerated manifest, new ceilings | **Approved by the user on 25 October 2026; implemented and CPU-verified** |
| R2: prespecified secondary analyses (implemented as annex S12–S16, including the holder-location split) | **Approved 25 October 2026; implemented and CPU-verified** |
| R3(a): decoding description | **Approved 25 October 2026; done** (annex §3.8, §13) |
| R3(b), R3(c): notice symmetry and waiting sentence | **Approved 25 October 2026; implemented and CPU-verified** |
| World count | Reassessed before implementation and kept at 192/128; **superseded the same day by the user's decision of 64 main worlds, 8 per stratum, no fallback** (annex second amendment, §3.10–3.11) |
| GPU development, main execution, publication | **Not authorized**; the annex §4.1 authorization sequence still applies |

---

## Appendix A. Reproducing the failure classification

Read-only over the exported canonical records. Run from the repository root with
Python 3.11+ and no third-party packages:
`python -I classify.py notebooks/run/assisted-v1/latest`, then the same for
`notebooks/run/course-7-working/latest`.

```python
import collections, json, re, sys
run = sys.argv[1]
worlds = {w["id"]: w for w in json.load(open(run + "/run.json", encoding="utf-8"))["worlds"]}
final = {}
for line in open(run + "/reports/conversations.jsonl", encoding="utf-8"):
    r = json.loads(line)
    if r["record_type"] == "episode_checkpoint" and (r["id"] not in final or r["slot"] > final[r["id"]]["slot"]):
        final[r["id"]] = r
ints = lambda s: [int(x) for x in re.findall(r"(?<![\w.])-?\d+(?![\w.])", s or "")]
for phase in ("prefix", "retain", "clear"):
    c = collections.Counter()
    for eid, r in final.items():
        wid, ph = eid.split("/", 1)
        if ph != phase or worlds.get(wid, {}).get("group") != "main":
            continue
        st = json.loads(r["state"])
        truth = worlds[wid]["original_truth" if phase == "prefix" else "revised_truth"]
        subs, events = st["submissions"], st["events"]
        wrong = any(s is not None and s != truth for s in subs)
        absent = [a for a in (0, 1) if subs[a] is None]
        c["success" if subs == [truth, truth] else
          "wrong+absent" if wrong and absent else "completed_wrong" if wrong else "non_commitment"] += 1
        if subs != [truth, truth]:
            for a in (0, 1):
                msgs = [(e.get("action") or {}).get("message") for e in events if e["agent"] == a and not e.get("error")]
                c["identical_message_on_3_calls"] += len(msgs) >= 3 and len(set(msgs)) == 1 and bool(msgs[0])
            c["all_absent_stated_truth"] += bool(absent) and not wrong and all(
                any(truth in ints((e.get("action") or {}).get("message")) for e in events if e["agent"] == a) for a in absent)
    print(phase, dict(sorted(c.items())))
```

Limits: numeric matches in messages are not proof of belief. "Identical
message" is an exact-string criterion and undercounts paraphrased loops.

## Appendix B. Simulation method

For each world, a latent effect u ~ N(0, 1). Cell c succeeds when
a_c + ρu + ε > 0, with ε ~ N(0, 1) and a_c set so the marginal success rate
equals the scenario rate. Worlds are assigned to 8 equal strata by index. Each
replication draws N worlds and computes the world contrasts. It then forms the
stratified percentile interval with the adopted index rule (⌊Bα/2⌋,
⌈B(1−α/2)⌉ − 1) and records width and whether the true value is covered. The
true value comes from 400,000 simulated worlds. The design is NumPy only,
seed 7, 600 replications, B = 2,000. It is a planning check of the method under
assumed rates, not a forecast of results.
