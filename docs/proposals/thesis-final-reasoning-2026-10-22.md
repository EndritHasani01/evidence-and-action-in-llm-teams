# Thesis final: my reasoning and recommendation

**22 October 2026 · personal reasoning by Claude (Opus 5.5), written at the
project author's request · a recommendation, not an adopted design**

Branch `feat/thesis-final`, created from `d31414d`. The
[specification](../../PROJECT_SPECIFICATION.md) remains the sole scientific
authority. This document adopts nothing and changes no code, configuration,
canonical store or historical record. It authorizes no GPU work. It responds to
the two 18 October design documents: the [thesis proposal](thesis-extension-2026-10-18.md)
(with its [evidence review](../analysis/thesis-extension-evidence-review.md) and
[roadmap](../plans/thesis-extension-roadmap.md)), and the
[literature critique](../implementation-research/thesis-literature-2026-10-18/README.md)
that challenged it.

New numbers come from read-only queries (`mode=ro&immutable=1`) of the two
completed campaigns' canonical stores. [Appendix A](#appendix-a-reproducing-the-new-numbers)
gives the script. Claims carry one of three labels:

- **Verified:** I checked it directly against data or a primary source.
- **Derived:** my arithmetic on verified inputs.
- **Inference:** my judgment.

## 0. Bottom line

1. **Keep the thesis identity, change the main experiment.** The project's
   question, *what remains valid after a correction?*
   ([user context](../../research/02_agent_context/01_USER_CONTEXT_AND_PRIORITIES.md#thesis-continuity)),
   is best answered with the controlled history-packet design on the two-agent
   I-01 task. It should not use the original four-peer matrix or another natural
   retain/clear run.
2. **The course data point at a different bottleneck than both 18 October
   documents assume.** In the assisted campaign, the value an agent needed
   reached it in 18 of 20 recoveries in each arm. Yet that agent submitted it
   in only 3 (retain) and 6 (clear). It either never committed or fell back on
   its own local maximum. No recovery submission in either arm repeated the
   withdrawn maximum. A memory experiment that ignores this risks producing a
   null that says nothing about memory.
3. **Adopt most of the critique, but keep the empty-history arm.** My
   recommended design uses 160 controlled worlds, six cells (H0/HS/HSC ×
   revision/no-change), one primary trial and both models. It adds a 24-world
   repeat panel, the 32-world natural bridge and the 32-world answer-preserving
   probe. That is 20,672 attempts. The primary contrast is the direct
   revised-world HS − HSC difference per model.
4. **Three gaps must be fixed before implementation.**
   - The pinned Granite revision has a broken tensor index: 241 of 363 entries
     point to the wrong shard.
   - Owner-qualified record labels become necessary once each agent sees both
     shards.
   - Measured throughput makes compute cheaper than planned, but makes calendar
     time and cross-session restore the binding risks.
5. **Run the bounded development pilot early, before building the full
   analysis layer.** Its no-change gate decides whether a memory effect is
   measurable in this regime at all. If it fails, the thesis should pivot to
   the commitment bottleneck instead of spending main compute at the floor.

## 1. Where the project actually stands

| Layer | Status | My reading |
|---|---|---|
| Original four-peer, five-family thesis | Implemented and CPU-verified through M4; never executed with a model. The four-peer course regime made six online runs. The last [ended in hardware rejection](../validation/course-kaggle-final-online-6-analysis.md): 16.8 MiB free memory against a 1.5 GiB gate at the long-context envelope, with no pilot or main results. | A rigorous asset whose free-T4 feasibility was never established. I would not try to rescue it for this thesis. |
| Two-agent I-01 runtime | Executed for real. Course-7 used 252 calls and the assisted campaign 356, both with complete coverage, exact resume and an independent verifier. | The only part of the repository with model evidence. Build on it. |
| Model findings | Assisted: retain 2/20, clear 3/20, interval [−15, +25] pp. Course-7: 2/20 and 2/20. | Recovery sits at the floor. No policy difference is detectable at this size. |
| 18 October designs | Two competing proposals, neither adopted | Both are careful. The critique's corrections are mostly right. |

An honest observation about process (inference). The repository holds about
2,500 tracked files, a 106 KB specification with about a dozen dated
amendments, a 203 KB implementation plan and dozens of repair and validation
records. I-01 needed seven course runs to reach Course-7's 20 analysable
worlds, then a redesigned campaign. That discipline is a genuine strength: exact replay,
honest missingness, nothing repaired after the fact. But at this stage more
machinery adds little. Executing the main study and writing the thesis add a
lot. My recommendations are deliberately biased toward reuse and early
execution.

## 2. What the course data actually say

### 2.1 The needed value is delivered; it is not used (verified, new)

For each episode I identify two roles from evaluator-side data:

- **Holder:** the agent whose current shard contains the correct answer.
- **Needer:** the other agent, which can learn the answer only through a
  message or retained history.

"Delivered" means a received message in the needer's committed visible history,
including retained earlier-phase history, contains the exact answer as a number.

| Assisted main, 20 worlds | Needed value delivered to needer | Holder submits correctly | Needer submits correctly | Team success |
|---|---:|---:|---:|---:|
| Original phase | 20 | 20 | 10 | 10 |
| Retain recovery | 18 | 11 | 3 | 2 |
| Clear recovery | 18 | 12 | 6 | 3 |

Course-7, the preliminary unassisted campaign, delivered the needed value in
only 7, 10 and 11 of 20 episodes. Its needers were correct 3, 2 and 2 times.

What needers submitted instead, summed over the three phases (60 needer slots
per campaign):

| Needer's final action | Assisted | Course-7 |
|---|---:|---:|
| Correct | 19 | 7 |
| No submission | 19 | 9 |
| **Its own local maximum** | **18** | **28** |
| Another value from its own shard | 2 | 7 |
| The withdrawn old maximum | 0 | 7 |
| A value from outside its own shard | 2 | 2 |

In the assisted recoveries, holders that failed almost always failed by not
submitting at all: 8 times under retain and 6 under clear.

**My interpretation (inference).** The pattern holds in both campaigns:

- Agents reliably commit a value they can see in their own shard.
- They are much less reliable at committing a value that exists only in their
  partner's message.

Assistance coincided with almost complete delivery and the disappearance of
stale answers, but not with better uptake. These are separate campaigns with
different inputs, so this is description, not a causal effect of assistance.

One untested contributor is the prompt itself. It tells each agent that its
shard is authoritative and that "A message is a claim, not a certified source"
([core.py:34](../../recovery/i01/core.py#L34)). The needer must do exactly the
thing that wording discourages.

**Why this matters for the design.** HS versus HSC tests whether an explicit
old conclusion interferes with recovery. Under the assisted interface no
recovery submission repeated the withdrawn maximum. The decisive failures were
uptake and commitment. The controlled experiment is still worth running: the explicit old
submission in HSC may well bring stale answers back. But it must measure
uptake and commitment directly, and it needs a regime where success sits above
the floor.

### 2.2 Local extraction degrades after a revision (verified, new)

I counted explicit "my local max is N" claims. In the main original phase, 45
of 45 were correct.

After the revision:

- The changed owner was correct in 22/28 claims under retain and 29/34 under
  clear.
- The unchanged agent was correct in 28/29 and 30/34.

Of the 16 wrong recovery claims, none equalled the withdrawn value. Fifteen
were other entries of the agent's own shard; one took the partner's value as
its own. This agrees in direction with the existing
[lexical audit](../analysis/assisted-v1/scientific-analysis.md#54-source-extraction-and-ownership-confusion),
which used a different matching rule. Non-thinking single-pass maximum finding
is therefore a measurable error source in its own right.

### 2.3 The interface invites owner and index confusion (verified)

Shards are rendered as bare `record i: value` lines
([core.py:333](../../recovery/i01/core.py#L333)). The source notice says only
"Changed record (index only): 13" ([core.py:322](../../recovery/i01/core.py#L322)).

In `main-09/clear/agent-1/invocation-1` the partner had just reported "949
(record 16)". The agent replied "Your local max is 695 (record 13)". The value
695 is the agent's *own* record 13, and 13 is the notice's index for the
partner's record. The scientific analysis lists
[six such cases](../analysis/assisted-v1/scientific-analysis.md#54-source-extraction-and-ownership-confusion).

The controlled packets would give every agent two `record 13` lines: its own
shard and the partner's historical report. Together with the notice, that is
three references to "record 13". Without owner-qualified labels, the design
would amplify the observed failure in exactly the cells being compared.

### 2.4 Loops look like self-imitation (verified traces; mechanism is inference)

In `main-08/retain/agent-1/invocation-2` the agent has seen its partner's 758
three times. On its last call it still sends its own earlier template: "I will
wait for your maximum before submitting". Across retain recoveries:

- 31 delivered messages duplicated an earlier string from the same sender
  (18 under clear).
- 13 agent trajectories repeated one message on all three calls (4 under
  clear).

Two published findings fit these observations. Neither is cited anywhere in
the repository.

- **Self-conditioning.** [Sinha et al., ICLR 2026](https://arxiv.org/abs/2509.09677)
  report that models make more errors when the context contains their own
  earlier errors. Scaling does not remove the effect; thinking mitigates it.
  The repository measured thinking at
  [91× the ready time and 126× the tokens](../validation/i01-course-3-results-analysis.md),
  which is impractical on T4s. The thesis therefore operates where
  self-conditioning should be strongest. That is a scope statement and an
  interpretive hypothesis, not a mechanism claim.
- **The knowing-doing gap.** [Schmied et al., 2025](https://arxiv.org/abs/2504.16078)
  name the gap between correct reasoning and the action actually taken. It
  matches "954 is the global max. I will submit." followed by `submit: null`.

## 3. The thesis question I would adopt

> When a two-agent LLM team resumes after one of its private source records
> changes, does retaining historical source evidence help it recover? Does
> additionally retaining its own earlier conclusion hurt? And at which step do
> recoveries fail: delivery of the needed value, uptake by the agent that needs
> it, or final commitment?

This keeps the project's identity and a single, cleanly identified primary
contrast. The step decomposition means even a null primary result says
something specific, for example: "the old conclusion changed what agents said
but not what they committed".

## 4. The design, decision by decision

| Decision | 18 Oct proposal | 18 Oct critique | My recommendation and reason |
|---|---|---|---|
| Task and protocol | I-01 maximum; 2 agents; 3 calls each; private final submissions | Same | **Keep.** It is the only executed, verified runtime. Final submissions are where the observed failures live, so removing finality would remove the phenomenon. |
| Edit population | Winner demoted only (replacement < M2) | Add a balanced "winner remains" stratum (replacement > M2, ≠ M1) | **Adopt the critique.** The demoted-only design lets a non-owner read the answer off the old table. Two strata also build in a mechanism test: history is sufficient for the non-owner in one stratum and insufficient in the other. |
| History packets | H0 / HS / HSC | HS / HSC only | **Keep H0.** Without it a null HS − HSC is uninterpretable, since history might simply be ignored. Diagnostic D02 shows a correct supplied peer report going unused. H0 also connects to the course's clear arm. |
| Events | Withdrawal / no-change | Same | **Same.** The no-change notice must say explicitly that it opens a new phase, because the course rule "only a source revision reopens" cannot carry over. |
| Primary estimand | Interaction θ (revision minus no-change) | Direct revised-world HS − HSC | **Direct contrast.** The critique's [counterexample](../implementation-research/thesis-literature-2026-10-18/repository-and-design-critique.md#5-primary-contrast-mechanisms-and-claims) is decisive: θ can favour dropping the conclusion when doing so never improves recovery. Keep θ as a secondary result. |
| Allocation | 128 worlds × 2 trials everywhere | 192 worlds × 1 trial + 24-world 3-trial panel | **160 worlds × 1 trial + 24-world panel.** Scripted histories cost nothing to acquire, so independent worlds buy more than trials do. 160 rather than 192 pays for H0. |
| Models | Qwen3.5-9B and Granite 4.2-8B | Same | **Same, with conditions.** Re-pin Granite (§5.1). Qualify Granite first, because it is the largest unknown. Decide now that a Granite hardware or numerical failure means running Qwen alone, with disclosure, rather than searching for a third model. |
| Rendering | Fixed historical fields | Owner labels suggested | **Owner labels required** everywhere, e.g. `A0.r13` in shards, reports and the notice. Render historical reports as one neutral block, not as "Your action" entries, so HS does not get a self-imitation template that H0 lacks. Keep byte layout constant across cells. |
| Call horizon | 3 per agent | "Reconsider" | **Keep 3.** With HS the minimal successful protocol needs one or two calls per agent. The observed loops would likely just repeat with more calls, and a new horizon adds an untested parameter. |
| Prespecified secondary outcomes | Process diagnostics listed | Diagnostic chain suggested | **Add the holder/needer funnel from §2.1** as fixed secondary outcomes: delivered, holder correct, needer correct, own-maximum fallback, stale submission, absence. Record the answer-holder role as an evaluator-side world descriptor. |
| Bridge and preserving probe | 32 worlds each | Same, smaller probe | **Keep both, small and separately reported.** |

### 4.1 Schedule arithmetic (derived)

Worst-case first-attempt slots, both models, six calls per team episode:

| Component | 160 worlds (target) | 128 worlds (fallback) |
|---|---:|---:|
| Controlled main: N × 6 cells × 6 calls × 2 models | 11,520 | 9,216 |
| Original and revised scalar controls | 640 | 512 |
| Repeat panel: 24 worlds × 6 cells × 2 extra trials | 3,456 | 3,456 |
| Natural bridge: 32 × (6 + 4×6 + 2) | 2,048 | 2,048 |
| Preserving probe: 32 × (3×6 + 1) | 1,216 | 1,216 |
| Development, reload and contingency (inherited) | 1,792 | 1,792 |
| **Total ceiling** | **20,672** | **18,240** |

For comparison, the proposal's controlled main alone is 18,432 slots, and the
critique's whole design is 16,960.

### 4.2 Precision (derived)

These are approximate 97.5% half-widths, `2.24·sqrt(q/N)`, for a paired binary
contrast near zero effect. Here `q` is the share of worlds where the two cells
disagree. The course retain/clear contrast had q = 0.25.

| Worlds | q = .20 | q = .25 | q = .50 | q = .80 |
|---:|---:|---:|---:|---:|
| 128 | 8.9 pp | 9.9 pp | 14.0 pp | 17.7 pp |
| 160 | 7.9 pp | 8.9 pp | 12.5 pp | 15.8 pp |
| 192 | 7.2 pp | 8.1 pp | 11.4 pp | 14.5 pp |

The thesis can resolve effects of about 10–15 points, not 5. That should be
accepted explicitly before adoption, not discovered afterwards. HS and HSC
differ by one field, so their outcomes should correlate strongly and q may be
low (inference).

## 5. Gaps both designs miss

### 5.1 The pinned Granite revision has a defective index (verified)

The proposal pins `ibm-granite/granite-4.2-8b` at `f8de16cd…`, observed on 18
October. On 20 October IBM pushed two commits titled "granite-4.2 index file
fix". The current head is `a7042144125ce5ae64f89610e8289647fc000b9a`.

| Check | Result |
|---|---|
| Weight shards at both revisions | Identical LFS hashes and sizes for all four |
| `config.json`, chat template, generation and tokenizer configs | Identical: config fields checked, the other files by hash |
| Tensor-to-shard entries in the index at `f8de16cd` | **241 of 363 point to the wrong shard**, checked against the shards' own safetensors headers via HTTP range requests (headers only, no weights) |
| Same check at `a7042144` | 0 of 363 wrong |

Any loader that resolves tensors through the index could fail, or silently
miss weights, at the pinned revision. The proposal's payload size is unaffected
because `total_size` is identical. **Re-pin to `a7042144`**, then let the
existing language-weight inventory check confirm the load. The Qwen pin
`c202236…` is still the repository head.

### 5.2 Owner labels are required (inference from §2.3)

This is a common-interface change applied to every cell, so it cannot bias the
HS − HSC comparison. It must be frozen before development, and the token
envelope must be re-proved afterwards.

### 5.3 Compute is cheaper than planned; calendar time is the real constraint (verified and derived)

Measured on T4 × 2 in the assisted main stage:

- 278 calls ran in 20.1 elapsed minutes: **8.7 allocated GPU-seconds per call**.
- Ready time averaged 5.9 s, with about 945 input and 36 generated tokens per
  call.
- Real calls were 73% of the worst-case slots, because episodes end early.

Both 18 October plans assume 10–30 s per call. Applying their conservative
formula `24 + 1.25 × slots × g / 3600` to my 20,672 slots:

| Assumed g | Conservative forecast | Expected if 75% of slots run |
|---:|---:|---:|
| 8.7 s (measured Qwen) | 86 GPU-h | 38 GPU-h of calls |
| 12 s | 110 GPU-h | 52 GPU-h of calls |
| 15 s | 132 GPU-h | 65 GPU-h of calls |

Granite's speed is unmeasured. Packets with both shards lengthen prompts
modestly. The proposed 200-hour ceiling is generous; the existing 100-hour plan
may even suffice.

The tight constraint is calendar time. The quota figures below are
search-reported, not verified: the Kaggle documentation page returned no
readable body when fetched.

- Kaggle's [GPU tips pages](https://www.kaggle.com/docs/efficient-gpu-usage)
  are reported to state about 30 GPU-hours per week with 9-hour sessions. That
  text predates T4 × 2; current third-party reports say 12-hour sessions.
- Whether T4 × 2 draws on the quota at one or two times wall clock is
  unconfirmed.
- A [Kaggle discussion thread](https://www.kaggle.com/discussions/product-feedback/743895)
  reports the T4 × 2 option being unavailable at times.

So the main run will span several sessions over weeks. **Cross-session restore
has never happened in a real campaign**: the course report notes no observed
crash, retry or cross-session restoration
([§5.8](../reports/final-course-report-submission.md#58-limitations)).
Run a deliberate export, restore and resume drill during development, and check
the account's actual quota display before planning dates.

### 5.4 Literature to add

The two papers in §2.4 bear directly on the observed behavior. The existing
reading ledger is otherwise strong on revision and memory; the research archive
already covers STALE and PlanFence. A targeted search for papers that directly
test mid-task source revision in LLM teams found adjacent work only, consistent
with the proposal's careful novelty claim.

### 5.5 Human coding

The course's qualitative analysis was AI-assisted and unblinded. For the
thesis:

- Freeze the trace rubric.
- Fix a small panel before looking at aggregate results, for example one
  world per stratum, both models, all cells.
- Code it yourself, with a second coder if a mentor or peer can help.

A single honest coder with a frozen rubric is better than an implied panel.

## 6. Order of work: pilot early

The roadmap builds the full analysis layer (T4) before any model call. Analysis
must be frozen before **main** data, but development data only needs gate
counts. I would reorder:

1. T0: adopt the amendment, plus the decisions in §4 and §5.
2. T1–T3: inputs, packets, owner labels, event semantics, both tokenizers'
   envelope proofs and the re-pinned Granite path.
3. A thin delivery package.
4. **Bounded development on GPU, Granite qualification first**, including the
   restore drill.
5. T4: write and freeze the analysis.
6. Freeze, then request main authorization.
7. Main execution, audit and writing.

The development pilot is the largest uncertainty in the whole plan, and every
earlier day it runs is a day of slack. A rough planning range (inference),
assuming no Granite surprises:

| Stage | Working time |
|---|---|
| Adoption and implementation (T0–T3, thin T5) | 6–10 days |
| Development on GPU, both models | 2–4 days of calendar |
| Analysis freeze (T4) | 2–3 days, can overlap development |
| Main execution | 1–3 weeks of calendar (quota-bound) |
| Audit, analysis and writing | 2–3 weeks; begin writing from the course report now |

## 7. Decision rules for after development (written before any data)

These follow the proposal's gates and add what to do when a gate fails.

| Development result, per model | Action |
|---|---|
| Hardware, numerics or loading fails (Granite) | Proceed Qwen-only with disclosure, if you pre-approve this rule now; otherwise stop for a decision |
| Scalar or diagnostic qualification fails | Same as above for that model; no threshold relaxation |
| No-change HS and HSC each ≥ 9/12, legality ≥ 98%, controls ≥ 22/24 | Freeze and request main authorization |
| No-change HS or HSC < 9/12 | The regime is commitment-limited, and a memory effect would sit at the floor. Do not run the main factorial. Either test one pre-declared common interface alternative on fresh development worlds (critique priority P2), or pivot the thesis to the commitment bottleneck, using course and development data |
| H0 ≈ HS, or any effect direction | Never a gate. Record it and proceed |

## 8. My priors, recorded before any thesis data (inference, low confidence)

These change no gate or analysis. Writing them down lets the results be
compared against them honestly later.

- **No-change HSC: high success**, about 60–85% for Qwen. Re-submitting a still
  valid own conclusion is the easiest cell.
- **Revision HS: moderate**, about 30–50%. The owner is fully informed. In most
  worlds the non-owner must adopt a partner value, the step that failed about
  half the time even in correct original teams.
- **HS − HSC under revision: small, possibly zero**, about 0–10 points in HS's
  favour. The explicit old submission could revive the stale answers that
  Course-7 showed without assistance.
- **HS − H0 under revision: clearly positive**, and larger in the
  winner-demoted stratum, where history is sufficient for the non-owner.
- **Granite: unknown.** It may differ substantially from Qwen in either
  direction.

## 9. What I would deliberately not do

- Rescue the four-peer matrix, run it twice, or mix it into this thesis. Describe
  it in a methodology chapter: its capacity proof and T4 rejection are real
  findings about feasibility.
- Add a solver, host finalizer, forced exchange, consensus vote, public
  submissions or answer repair. Each would remove the bottleneck being studied.
- Use thinking mode as the main condition (cost), or tune prompts on main
  outcomes.
- Use an LLM judge for qualitative coding, or assign causal percentages to
  failure categories.
- Write more process documents than the adoption section, one implementation
  checklist and the thesis itself.

## 10. Suggested thesis structure

1. **Introduction:** what remains valid after a correction.
2. **Background:** belief revision, provenance and incremental computation;
   memory and revision in agents; distributed-information coordination;
   self-conditioning and the knowing-doing gap; paired and clustered
   evaluation.
3. **Method and infrastructure:** exact tasks, private views, finality,
   persistence and missingness. Include lessons from the four-peer design
   (capacity proof, T4 rejection) explaining why the thesis is short-context and
   two-agent.
4. **Study 1, natural recovery (exploratory):** Course-7 and the assisted
   campaign, including the §2 funnel analysis. This motivates Study 2.
5. **Study 2, controlled evidence versus conclusion (main):** H0/HS/HSC ×
   revision/no-change, two models.
6. **Study 3, transfer checks:** the natural bridge and the answer-preserving
   probe.
7. **Discussion:** the evidence-to-commitment chain, limits and implications for
   memory design in agent teams.
8. **Conclusion.** Appendices cover reproducibility, the trace casebook and
   seed handling.

## 11. Decisions I need from you

1. **Deadline and mentor expectations.** Is there a submission date? Do your
   mentors require two models or a particular scale? These decide between the
   target (160 worlds) and the fallback (128), and whether Qwen-only is
   acceptable.
2. **Design amendments.** Accept or reject: the winner-remains stratum, the
   direct primary contrast, keeping H0, 160 worlds × 1 trial plus the repeat
   panel, owner-qualified labels and the funnel outcomes.
3. **Granite.** Re-pin to `a7042144`? Pre-approve "Qwen-only on a Granite
   hardware or numerical failure"?
4. **Quota.** What does your Kaggle account show for weekly GPU hours, and how
   is T4 × 2 charged?

Approval of this reasoning would authorize nothing by itself. It would feed the
T0 adoption step, which the operating contract requires to be explicit.

## Appendix A: Reproducing the new numbers

Run from the repository root with Python 3.11+ and no third-party packages:
`python -I funnel.py notebooks/run/assisted-v1/latest`, and likewise for
`notebooks/run/course-7-working/latest`. The script opens the canonical stores
immutable and read-only.

```python
"""Read-only holder/needer funnel for an I-01 campaign. Usage: python -I funnel.py RUN_DIR"""
import collections, json, pathlib, re, sqlite3, sys

root = pathlib.Path(sys.argv[1])
worlds = {w["id"]: w for w in json.loads((root / "run.json").read_text())["worlds"]}
states = {}
for name in ("worker-0.sqlite", "worker-1.sqlite"):
    db = sqlite3.connect((root / name).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
    states.update((i, json.loads(s)) for i, s in db.execute("select id, state from episodes"))

numbers = re.compile(r"-?\d+")
for phase in ("prefix", "retain", "clear"):
    c = collections.Counter()
    for wid, w in worlds.items():
        st = states.get(f"{wid}/{phase}") if w["group"] == "main" else None
        if not st or not st.get("terminal"):
            continue
        shards = w["original" if phase == "prefix" else "revised"]
        truth = w["original_truth" if phase == "prefix" else "revised_truth"]
        holder = 0 if truth in shards[0] else 1
        needer = 1 - holder
        received = [e["text"] for e in st["history"][needer] if e["kind"] == "received_message"]
        c["delivered"] += any(truth in map(int, numbers.findall(t)) for t in received)
        h, n = st["submissions"][holder], st["submissions"][needer]
        c["holder_correct"] += h == truth
        c["holder_absent"] += h is None
        c["needer_" + ("correct" if n == truth else "absent" if n is None
                       else "own_local_max" if n == max(shards[needer])
                       else "withdrawn_max" if phase != "prefix" and n == w["original_truth"]
                       else "other_own" if n in shards[needer] else "foreign")] += 1
        c["success"] += st["submissions"] == [truth, truth]
        c["n"] += 1
    print(phase, dict(sorted(c.items())))
```

Limitations of these measures:

- "Delivered" is a number-token match and can be satisfied by a message that
  mentions the right number for another reason.
- The claim-accuracy counts in §2.2 used a separate regex,
  `\b[Mm]y\s+(new|current|revised|updated\s+)?(local\s+)?max(imum)?\s*(is|=|:)\s*N`,
  over parsed actions, and miss other phrasings.
- Throughput in §5.3 comes from the `attempts` table's admission and finish
  timestamps for the `main` stage.

All of these are descriptive. None identifies an internal cause.

## Appendix B: External checks (22 October 2026)

| Item | Source | Finding |
|---|---|---|
| Granite commits | [Hugging Face commit API](https://huggingface.co/api/models/ibm-granite/granite-4.2-8b/commits/main) | `f8de16cd…` (4 September); index fixes `6af7db37…` and `a7042144…` (20 October) |
| Granite file hashes | `/api/models/ibm-granite/granite-4.2-8b/tree/{rev}` at both revisions | Shards, config and templates identical; only `model.safetensors.index.json` differs |
| Granite shard headers | HTTP range reads of each shard's safetensors header at `a7042144` | 363 tensors; old index wrong for 241, new index wrong for 0 |
| Qwen head | [Hugging Face commit API](https://huggingface.co/api/models/Qwen/Qwen3.5-9B/commits/main) | Head is still `c202236…` (2 March 2026) |
| Self-conditioning | [arXiv:2509.09677v3](https://arxiv.org/abs/2509.09677), ICLR 2026 | Abstract and version history checked |
| Knowing-doing gap | [arXiv:2504.16078v1](https://arxiv.org/abs/2504.16078) | Abstract checked; no venue listed |
| Kaggle quota | [Kaggle GPU tips](https://www.kaggle.com/docs/efficient-gpu-usage); [quota discussion](https://www.kaggle.com/general/135810); [availability reports](https://www.kaggle.com/discussions/product-feedback/743895) | Search-reported, page bodies not read: about 30 h/week, 9–12 h sessions; T4 × 2 accounting and availability not confirmed |
| Adjacent recent work | [STALE](https://arxiv.org/abs/2605.06527), [PlanFence](https://arxiv.org/abs/2609.03340), [delayed-verification belief study](https://arxiv.org/abs/2606.27409) | The first two are already covered in `research/`; none directly tests revision recovery in an LLM team |
