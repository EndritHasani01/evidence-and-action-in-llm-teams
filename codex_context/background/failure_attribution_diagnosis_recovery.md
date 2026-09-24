# Failure Attribution, Diagnosis and Recovery in Multi-Agent LLM Systems

I investigated the literature through **September 2026**, with particular attention to MAST, Who&When, TraceElephant, recent causal-attribution work, recovery studies, resilience research, and the older foundations from distributed systems and software debugging.

The clearest conclusion is this:

> **We are becoming reasonably good at describing failures, somewhat better at locating them, but we are still poor at proving what caused them and much worse at repairing only the damaged part of a multi-agent system.**

That makes this one of the more scientifically interesting areas in current multi-agent research.

---

## 1. The problem is actually three different problems

A great deal of the literature loosely calls all of this "debugging", but these should be separated:

| Stage | Question | Example |
|---|---|---|
| **Detection** | Did anything go wrong? | "The final answer is incorrect." |
| **Diagnosis / attribution** | What caused it? | "Agent B introduced a false assumption at step 17." |
| **Recovery** | Can we repair that cause and continue? | "Replace B's step 17, invalidate dependent state, and rerun only affected descendants." |

These are fundamentally different.

A system can detect failure perfectly while having no idea why it failed. It can also correctly identify a suspicious step without showing that the step **caused** the failure. And even a correct diagnosis does not imply that a repair mechanism can safely resume execution.

This distinction has become increasingly explicit in recent work. The original Who&When benchmark showed that identifying the responsible agent was already difficult, but pinpointing the decisive step was dramatically harder: its best reported approach achieved **53.5% agent-level accuracy but only 14.2% step-level accuracy**. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/zhang25cq.html))

That gap is the heart of the field.

---

## 2. MAST: a vocabulary for failure, not yet a theory of causation

MAST, published at NeurIPS 2025, is probably the most important starting point. Its taxonomy was developed from expert analysis of 150 traces, then used in a dataset of more than 1,600 traces spanning seven MAS frameworks. It identifies **14 failure modes in three categories**. ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html))

| Category | Important modes |
|---|---|
| **System design / specification** | task-spec violation, role-spec violation, step repetition, conversation-history loss, failure to recognize termination |
| **Inter-agent misalignment** | conversation reset, failure to clarify, task derailment, information withholding, ignoring another agent, reasoning-action mismatch |
| **Verification / termination** | premature termination, absent/incomplete verification, incorrect verification |

The complete 14-mode taxonomy is documented in the released MAST dataset. ([huggingface.co](https://huggingface.co/datasets/Manas1204/MAST-Data?utm_source=chatgpt.com))

MAST's importance is that it changed the question from:

> "Did the MAS get the benchmark answer wrong?"

to:

> "What kind of system behavior produced the failure?"

But **MAST classification is not root-cause attribution**.

Suppose:

**Agent A hallucinates → Agent B trusts it → Agent C performs incorrect verification → final answer fails.**

A MAST annotator can legitimately identify several failure modes:

- incorrect information from A,
- B ignoring contradictory evidence,
- incorrect verification by C.

That still does not determine which event was causally decisive.

This is one of the major conceptual jumps occurring after MAST.

---

## 3. "First mistake" is not necessarily "root cause"

TraceElephant makes an especially useful distinction.

It defines the decisive failure step according to **recoverability**, not simply chronology. If Agent A makes an error but Agent B is explicitly responsible for detecting and correcting such errors, the system remains recoverable after A's mistake. If B fails to verify it, TraceElephant may assign the decisive failure to **B**, because that is the point at which the recovery opportunity disappears. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

That is much more sophisticated than:

> earliest incorrect output = responsible step.

It gives us at least four useful concepts:

**Origin** — where incorrect information initially appeared.

**Propagation point** — where another component consumed or transmitted it.

**Containment failure** — where a mechanism that should have stopped it failed.

**Decisive failure point** — where successful recovery became unlikely/impossible under the system's intended design.

These do not have to be the same step.

That distinction is highly important for real systems.

---

## 4. TraceElephant: observability matters enormously

TraceElephant, an ACL 2026 paper, attacks one weakness of Who&When: many earlier attribution benchmarks exposed only agent outputs, while actual developers can often inspect prompts, inputs, messages, tools and environment state.

It provides complete execution traces and reproducible environments for **220 failed executions from three agentic systems**. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

The result is striking.

With complete traces, tested attribution approaches reached approximately:

| Attribution | Full trace |
|---|---:|
| Agent | **65.9%** |
| Step | **30.3%** |

Compared with output-only traces, this corresponded to roughly a **22% improvement at agent level and 76% at step level**. Access to a running environment improved step-level attribution by another roughly 10%. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

This tells us something deeper than simply "give the debugger more context."

It suggests:

> **Failure attribution is partly an observability problem.**

If you do not record what agents actually received, which tools ran, which state versions they observed, and what environment state existed, some root causes may simply be **unidentifiable afterward**.

This connects MAS debugging directly to distributed tracing and observability engineering.

---

## 5. Attribution methods are evolving rapidly

There are roughly four methodological families emerging.

| Family | Idea | Main weakness |
|---|---|---|
| LLM trace reasoning | ask an LLM to inspect trace | long-context errors, symptom confusion |
| Statistical / spectrum methods | compare failing and successful executions | correlation ≠ causation |
| Dependency-based methods | track information flow | dependency ≠ causal necessity |
| Counterfactual / interventional methods | ask whether replacing a step changes outcome | expensive and hard with stochastic agents |

### LLM reasoning

Who&When established surprisingly weak performance from general reasoning models on fine-grained attribution. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/zhang25cq.html))

ECHO subsequently explored hierarchical context representations and consensus rather than simply placing a huge trajectory in one prompt. ([amazon.science](https://www.amazon.science/publications/where-did-it-all-go-wrong-a-hierarchical-look-into-multi-agent-error-attribution?utm_source=chatgpt.com))

ErrorProbe goes further: it detects local anomalies, traces backward from symptoms, and uses executable evidence to validate hypotheses. It also keeps only verified failures in episodic memory. ([aclanthology.org](https://aclanthology.org/2026.findings-acl.98/))

This is a meaningful direction because diagnosis becomes:

**hypothesis → evidence → validation**

rather than:

**trace → LLM opinion**.

---

## 6. Information flow may matter more than temporal order

Suppose the trace is:

A → B → C → D → E.

The bad final output appears at E.

Temporal debugging might inspect E, D, C...

But imagine E's answer depends on one statement from A that travelled through B and D while C was unrelated.

The causal structure is not really:

A → B → C → D → E.

It might be:

A  
↘ B → D → E  
C ↗

This motivates **dependency-graph debugging**.

There has been active research in this direction, although one prominent GraphTracer preprint is a cautionary example: it proposed Information Dependency Graphs for distinguishing propagated symptoms from root causes, but the paper was subsequently **withdrawn because the authors reported a fundamental methodological error affecting the validity of the main results**. ([arxiv.org](https://arxiv.org/abs/2510.10581))

That is important scientifically. The idea of dependency-aware tracing remains attractive, but simply drawing an information graph does not establish causation.

---

## 7. Statistical attribution has exactly the same trap software debugging encountered

FAMAS, published at FSE 2026, adapts **spectrum-based fault localization** to MAS. It reruns trajectories and uses variation in agent/action activation patterns to produce suspiciousness estimates. ([conf.researchr.org](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/205/Spectrum-based-Failure-Attribution-for-Multi-Agent-Systems?utm_source=chatgpt.com))

There is a strong connection here to classical software debugging.

Spectrum-based software debugging historically asks:

> Which statements occur disproportionately often in failing executions?

But software-engineering research has repeatedly pointed out that this can measure **correlation rather than causality** and can suffer from confounding. Causal fault-localization work such as UniVal explicitly tries to estimate the failure-causing effect instead. ([research.google](https://research.google/pubs/improving-fault-localization-by-integrating-valueand-predicate-based-causal-inference-techniques/?utm_source=chatgpt.com))

Exactly the same issue appears in MAS.

Imagine Agent D is always active whenever Agent B makes an error.

D may have very high statistical association with failures because it handles B's outputs.

But removing or fixing D might accomplish nothing.

So:

\[
P(Failure\mid D\ active)
\]

is not equivalent to:

\[
P(Failure\mid do(D\ fixed)).
\]

That distinction should probably become foundational in MAS debugging.

---

## 8. Causal failure localization is now emerging

A2P — **Abduct, Act, Predict** — explicitly reframes failure attribution as counterfactual reasoning.

The method asks the model to:

1. infer a possible underlying cause,
2. propose a minimal corrective intervention,
3. predict whether the modified trajectory would succeed.

It reported much better step-level performance than basic trace-analysis approaches on Who&When. ([arxiv.org](https://arxiv.org/abs/2509.10401?utm_source=chatgpt.com))

DCFA, released in September 2026, similarly combines a global causal-inspired dependency representation with local counterfactual-inspired reasoning and reports improvements over attribution baselines. ([arxiv.org](https://arxiv.org/abs/2609.04749?utm_source=chatgpt.com))

But there is an extremely important caveat.

A model saying:

> "If step 14 were corrected, everything after it would work"

is not the same as actually performing that intervention.

A2P largely **predicts the counterfactual** inside an LLM reasoning process. ([arxiv.org](https://arxiv.org/abs/2509.10401?utm_source=chatgpt.com))

True causal validation would instead be:

\[
do(step_{14}=corrected)
\]

followed by an actual controlled execution.

This distinction remains largely open.

---

## 9. The most important methodological problem: stochastic recovery

This may be the biggest issue in current recovery research.

Imagine a failed MAS run.

You diagnose Agent B.

You change B's prompt.

You rerun the system.

It succeeds.

Did your fix work?

**Not necessarily.**

LLMs are stochastic.

A complete rerun may succeed simply because different samples were generated by:

A, B, C and D.

The purported repair may have done nothing.

A very recent August 2026 study, **Repair or Resample?**, directly attacks this issue. It introduces SymTrace and SymFail so that execution before a chosen intervention point can be reconstructed and only the downstream part regenerated. ([arxiv.org](https://arxiv.org/abs/2608.25920))

Its empirical results are sobering: existing unguided rerunning showed a reported **6.9% repair rate**, whereas symptom-driven intervention repaired **20.15%** of cases. The authors explicitly frame the problem as distinguishing causal repair from stochastic resampling. ([arxiv.org](https://arxiv.org/abs/2608.25920))

This is arguably one of the most important recent papers in the area because it changes what counts as evidence of recovery.

---

## 10. What a valid recovery experiment should look like

The correct unit of experimentation should probably be a **paired counterfactual replay**.

Suppose the original trajectory is:

\[
S_0\rightarrow A_1\rightarrow A_2\rightarrow A_3\rightarrow A_4\rightarrow Failure
\]

and diagnosis claims \(A_2\) is responsible.

Create a checkpoint immediately before \(A_2\).

Then compare:

\[
Original:
S_2\rightarrow A_2\rightarrow A_3\rightarrow A_4
\]

with:

\[
Intervention:
S_2\rightarrow A'_2\rightarrow A'_3\rightarrow A'_4
\]

The prefix \(S_2\) is identical.

But because downstream LLM execution remains stochastic, a single replay is still insufficient.

You want something closer to:

\[
\Delta =
P(Success\mid do(A_2=corrected))
-
P(Success\mid do(A_2=unchanged)).
\]

And ideally compare it with irrelevant interventions:

\[
P(Success\mid do(A_4=changed)).
\]

Now the claim is much stronger:

> changing the diagnosed step systematically increases recovery probability relative to matched resampling.

That is causal debugging rather than "we tried again and it worked."

---

## 11. Root cause versus downstream symptom

This is another major difficulty.

Imagine:

\[
A: \text{"France has 90M people"}
\]

then:

\[
B: \text{uses 90M}
\]

then:

\[
C: \text{calculates something incorrectly from 90M}
\]

then:

\[
Verifier: \text{approves it}.
\]

There are now multiple wrong things.

A naive debugger may flag C because C contains the final numerical error.

But replacing C while keeping the corrupted premise from A may still fail.

This is why diagnosis needs to ask:

> **If this particular node were repaired while keeping its ancestors fixed, would downstream execution recover?**

TraceElephant's recoverability-aware definition gets partway toward this concept. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

Classical **delta debugging** uses a similar principle: systematically alter the circumstances of a failure until the minimal failure-inducing set remains. ([st.cs.uni-saarland.de](https://www.st.cs.uni-saarland.de/papers/tse2002/?utm_source=chatgpt.com))

And Adaptive Interventional Debugging uses actual fault injection and interventions to distinguish correlation from causality in nondeterministic software. ([arxiv.org](https://arxiv.org/abs/2003.09539?utm_source=chatgpt.com))

MAS research has barely begun exploiting these ideas fully.

---

## 12. Failure propagation should be treated separately from failure generation

A particularly useful conceptual model is:

\[
\text{Origin} \rightarrow
\text{Propagation} \rightarrow
\text{Amplification} \rightarrow
\text{Escape}
\]

For example:

\[
Hallucination
\rightarrow
handoff
\rightarrow
shared memory
\rightarrow
planning
\rightarrow
incorrect verification
\rightarrow
external action.
\]

This means a **local fault can cause systemic failure**.

So "local versus systemic" should not merely describe where the error occurs.

I would distinguish:

| Type | Meaning |
|---|---|
| Local fault, local effect | one agent errs; error contained |
| Local fault, systemic effect | one error propagates through system |
| Systemic fault | architecture/state/orchestration itself is wrong |
| Repeated correlated faults | several agents fail because of common input/model/state |
| Recovery-induced fault | attempted repair corrupts previously correct state |

That last category deserves much more research.

---

## 13. Communication failures are becoming measurable

AgentAsk, published at ACL 2026, specifically examines failures occurring at agent-to-agent boundaries.

Its edge-level taxonomy identifies:

**Data Gap**, **Signal Corruption**, **Referential Drift**, and **Capability Gap**.

The proposed clarification mechanism intervenes at problematic handoffs and reported improvements of up to 4.69% while keeping additional latency/cost below 10%. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1294/))

This is useful because it treats the **communication edge itself** as a potential failure object.

Instead of saying:

> Agent B failed.

we might say:

> The A→B handoff failed because information required by B was omitted.

That is a much better abstraction for distributed agent systems.

---

## 14. Stale state is a special and underdeveloped failure class

Shared memory creates another layer.

Suppose:

\[
A\ writes\ fact\ x
\]

then the environment changes:

\[
x\rightarrow x'
\]

but B later reads \(x\).

Nothing about B's reasoning needs to be wrong.

The failure is:

> **B reasoned correctly over stale system state.**

STALE, although primarily focused on agent memory rather than multi-agent coordination, demonstrates that current agents frequently fail to recognize that previously stored information has become invalid; even the strongest evaluated system in that benchmark reached only 55.2% overall accuracy. ([arxiv.org](https://arxiv.org/abs/2605.06527))

Recent work on shared multi-agent memory explicitly names stale propagation, contradiction persistence and provenance collapse as architectural problems. ([arxiv.org](https://arxiv.org/abs/2606.24535?utm_source=chatgpt.com))

This implies that future failure attribution cannot only inspect messages.

It needs:

\[
(agent,\ step,\ state\ version,\ provenance).
\]

---

## 15. Propagated hallucinations are structurally different from ordinary hallucinations

If one model hallucinates, that is a model error.

If one agent hallucinates and ten agents treat its message as trusted evidence, that becomes a **system architecture problem**.

Research on faulty-agent resilience confirms that topology strongly affects how much damage faulty agents cause. Huang et al. found large differences between communication structures and showed that Challenger/Inspector mechanisms could recover many injected faults—up to 96.4% in their experiments. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/huang25ay.html))

Similarly, ResMAS explicitly optimizes communication topology and prompts for resilience under agent perturbations. ([ojs.aaai.org](https://ojs.aaai.org/index.php/AAAI/article/view/40824/))

So the same faulty agent can create:

\[
small\ blast\ radius
\]

in one topology and

\[
system\ collapse
\]

in another.

The **propagation graph** therefore matters almost as much as the original fault.

---

## 16. This is exactly where distributed systems becomes relevant

There is a surprisingly direct analogy.

Traditional distributed systems have processes that:

- maintain local state,
- exchange messages,
- experience failures,
- checkpoint execution,
- restore previous state,
- replay logged events.

LLM MAS have:

- agents,
- context/memory,
- natural-language messages,
- tool calls,
- nondeterministic model generations,
- external state.

Classical rollback-recovery distinguishes checkpoint-based recovery from log-based recovery and studies how to recover a consistent distributed state. ([research.ibm.com](https://research.ibm.com/publications/a-survey-of-rollback-recovery-protocols-in-message-passing-systems?utm_source=chatgpt.com))

One classic problem is the **domino effect**: rolling back one process may require rolling back other processes that consumed its messages, which may recursively require more rollback. ([courses.cs.vt.edu](https://courses.cs.vt.edu/cs5204/fall10-kafura-BB/Papers/FaultTolerance/Checkpointing-Survey.pdf?utm_source=chatgpt.com))

That maps almost perfectly onto agents.

Suppose:

\[
A_5\rightarrow B_7\rightarrow C_9\rightarrow D_{12}.
\]

If \(A_5\) is discovered to be corrupt, simply restoring A is insufficient.

B, C and D have already incorporated the bad information.

You must identify the **causal descendants** of \(A_5\).

That is essentially selective rollback over an agent dependency graph.

And this problem is barely solved for LLM MAS.

---

## 17. Selective rollback is much harder than it sounds

A proper rollback mechanism needs to know:

**What state existed before the error?**

**Which subsequent state depends on it?**

**Which actions are reversible?**

**Which messages must be replayed?**

**Which external effects already happened?**

Imagine:

Agent A queries a database.  
Agent B sends an email.  
Agent C updates a ticket.  
Agent D discovers A's answer was incorrect.

You cannot simply "rerun from A".

The email already exists.

This is the equivalent of non-rollbackable external I/O in distributed systems.

Potential solutions need concepts analogous to:

- checkpoints,
- event logs,
- idempotent operations,
- compensating actions,
- dependency tracking,
- consistent snapshots.

The distributed-systems literature has decades of work on exactly these issues. ([research.ibm.com](https://research.ibm.com/publications/a-survey-of-rollback-recovery-protocols-in-message-passing-systems?utm_source=chatgpt.com))

Applying them rigorously to agent systems is still surprisingly open.

---

## 18. Re-execution requires preserving more than conversation history

To reproduce an agent trajectory reliably you may need to record:

\[
State_t =
\{
messages,
prompts,
memory,
tool\ outputs,
environment,
model,
sampling\ configuration,
agent\ topology,
external\ artifacts
\}.
\]

Merely storing the chat transcript is insufficient.

TraceElephant's central argument is essentially this: inputs, tool/environment interactions, system configuration and architecture matter for reliable attribution. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

This also explains why reproducible failure experiments are difficult with commercial LLM APIs: even identical prompts may not guarantee bit-identical outputs.

So the correct objective may not be:

> reproduce exactly the same trajectory

but:

> reproduce the same causal state sufficiently well to estimate intervention effects.

That is a much deeper problem.

---

## 19. Replacing an unreliable agent is not equivalent to replacing a crashed server

An unreliable LLM agent may fail intermittently.

Agent B might be:

- correct 90% of the time,
- excellent at one subtask,
- terrible after long context,
- temporarily confused,
- contaminated by state,
- receiving bad inputs from Agent A.

Replacing B immediately can therefore destroy useful specialization.

AgentRevive addresses a related problem by treating agents as **Active, Standby or Terminated** rather than immediately deleting poorly performing nodes. Agents can temporarily be suppressed and later recover. ([aclanthology.org](https://aclanthology.org/2026.acl-long.373/))

This is much closer to graceful degradation.

But the deeper replacement problem remains:

> If we replace agent B after it produced corrupted state, what part of B's earlier contribution should survive?

A replacement agent cannot simply inherit everything, because that may transfer the fault.

It also cannot start empty, because that may destroy important progress.

This becomes a **state-transfer and provenance problem**.

---

## 20. Graceful degradation is emerging, but not mature

Traditional fault-tolerant systems often aim for:

\[
full\ functionality
\rightarrow
reduced\ functionality
\rightarrow
safe\ operation
\]

rather than catastrophic shutdown.

MAS should probably behave similarly.

If a research specialist fails, perhaps the system can continue using weaker evidence.

If the verifier fails, perhaps execution pauses before consequential actions.

If shared memory becomes inconsistent, perhaps agents switch to isolated state.

Current resilience work mostly studies this proactively through topology, redundancy, inspectors, Byzantine-style consensus or dynamic participation. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/huang25ay.html?utm_source=chatgpt.com))

What is still much less developed is **diagnosis-conditioned degradation**:

> We have identified component X as unreliable with confidence 0.82; how should the rest of the system reorganize without restarting?

That looks like an important open area.

---

## 21. Responsibility assignment is surprisingly philosophical

There are multiple legitimate meanings of "responsible":

\[
\text{originator}
\]

\[
\text{causal contributor}
\]

\[
\text{component expected to prevent the failure}
\]

\[
\text{component whose repair maximizes recovery}
\]

\[
\text{component architecturally responsible}.
\]

Consider:

A hallucinates.  
B should verify A.  
B fails verification.

Who is responsible?

For model-quality analysis: **A**.

For system engineering: possibly **B**.

For minimal repair: whichever intervention restores success most cheaply.

TraceElephant explicitly adopts a role-aware, recoverability-aware conception rather than merely choosing the earliest visible error. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

Future benchmarks probably need **multiple attribution labels**, not a single "culprit".

---

## 22. Privileged oracle information can make debugging benchmarks unrealistic

Another methodological danger is giving the diagnosis system information unavailable in deployment.

For example:

- gold answer,
- exact correct intermediate state,
- knowledge of which injected fault occurred,
- future trajectory,
- hidden ground-truth agent intention.

A debugger with access to these signals might perform extremely well while being unusable in a real system.

There is therefore a tension.

TraceElephant correctly argues that developer-facing debugging should exploit information developers realistically possess—inputs, tools, state and architecture. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912/))

But that should not become:

> give the debugger the answer.

A strong benchmark should explicitly distinguish:

\[
observable\ evidence
\]

from

\[
annotation\ oracle.
\]

---

## 23. Failure injection is useful but dangerous

Injected faults are extremely useful because the experimenter knows exactly what changed.

Huang et al. use injected faulty-agent behaviors to measure system resilience. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/huang25ay.html?utm_source=chatgpt.com))

AgenTracer similarly uses counterfactual replay and programmed fault injection to produce attribution training data. ([arxiv.org](https://arxiv.org/abs/2509.03312?utm_source=chatgpt.com))

But synthetic failures can create a benchmark shortcut.

Real failures are often:

- subtle,
- distributed,
- partially recoverable,
- caused by interacting weak signals,
- semantically ambiguous.

Injected failures may be cleaner.

Therefore strong work should probably evaluate both:

\[
controlled\ injected\ faults
\]

and

\[
naturally\ occurring\ failures.
\]

The first gives causal ground truth.

The second gives realism.

---

## 24. The central validity test should be intervention

This gives us a clean hierarchy.

### Level 1 — symptom detection

> "Step 25 looks wrong."

Weakest.

### Level 2 — attribution

> "Step 12 probably caused step 25."

Better.

### Level 3 — counterfactual hypothesis

> "If step 12 were corrected, the system would probably succeed."

Better still.

### Level 4 — executed intervention

Actually replace step 12 and replay from the saved state.

### Level 5 — controlled causal validation

Repeat the intervention and appropriate controls over stochastic executions and estimate:

\[
ATE =
E[Y\mid do(repair)]
-
E[Y\mid do(control)].
\]

where \(Y\) may be success, reward or verified task completion.

That final level is what I would call convincing causal recovery.

Most MAS work has not reached it.

---

## 25. What is reasonably well understood now?

By late 2026, I would say several things have credible empirical support.

**Failure modes are diverse and many originate at system boundaries rather than inside a single LLM.** MAST established a useful empirical vocabulary. ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html))

**Step-level attribution is substantially harder than agent-level attribution.** Who&When and TraceElephant both support this. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/zhang25cq.html))

**Observability dramatically improves diagnosis.** TraceElephant provides direct evidence. ([aclanthology.org](https://aclanthology.org/2026.acl-long.912.pdf))

**Communication topology changes failure propagation and resilience.** Faulty-agent and ResMAS experiments support this. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/huang25ay.html?utm_source=chatgpt.com))

**Verification is both a protection and another failure point.** MAST explicitly contains incomplete and incorrect verification failures. ([huggingface.co](https://huggingface.co/datasets/Manas1204/MAST-Data?utm_source=chatgpt.com))

**Handoff boundaries matter.** AgentAsk provides direct evidence that clarification at selected edges can reduce failure. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1294/))

**Blind rerunning should not be accepted as evidence of repair.** SymTrace/SymFail makes this methodological problem explicit. ([arxiv.org](https://arxiv.org/abs/2608.25920))

---

## 26. What remains largely open?

This is where the area becomes especially interesting.

| Problem | State in 2026 |
|---|---|
| Failure taxonomy | **Relatively mature** |
| Failure detection | **Moderately developed** |
| Agent-level attribution | **Emerging** |
| Exact step localization | **Still weak** |
| Symptom vs root-cause separation | **Open** |
| Causal attribution | **Early** |
| Failure propagation modelling | **Early/moderate** |
| State/provenance-aware debugging | **Early** |
| Reproducible stochastic replay | **Early** |
| Selective rollback | **Largely open** |
| Dependency-aware re-execution | **Largely open** |
| Repair without full restart | **Very open** |
| Agent replacement with safe state transfer | **Very open** |
| Graceful degradation after diagnosis | **Early** |
| Recovery effectiveness with causal controls | **Very open** |
| Realistic evaluation with irreversible external actions | **Almost untouched** |

This is why I think **recovery is currently less saturated than attribution**.

There are already several papers asking:

> Who caused the failure?

Far fewer convincingly answer:

> Now that you know, how do you repair exactly the corrupted portion, prove the repair was causal, preserve valid work and safely continue?

---

## 27. A particularly strong research abstraction

After reading this literature, I think the most useful abstraction is not simply:

> **Failure attribution.**

It is:

\[
\boxed{
Fault
\rightarrow
Propagation
\rightarrow
Diagnosis
\rightarrow
Intervention
\rightarrow
Recovery
}
\]

A system should ideally record an execution as a **causal/provenance graph** rather than only a linear transcript.

For example:

```text
Task
 │
 ▼
Planner A ── plan p1 ─────┐
                          ▼
Researcher B ─ result r1 → Analyst C
        │                     │
        │                     ▼
        └──────────────→ Shared State
                              │
                              ▼
                          Verifier D
                              │
                              ▼
                         Final Output
```

If `r1` later proves false, the system could determine:

\[
descendants(r1)
\]

and invalidate only those nodes.

Everything independent of `r1` remains intact.

That gives you something analogous to **incremental computation + distributed rollback + causal debugging**.

I found surprisingly little mature work solving the complete problem this way.

---

## 28. The strongest unexplored question

The gap I would take most seriously from this investigation is:

> **Can a multi-agent system identify the minimal causal failure region of a trajectory and repair only that region while preserving unaffected work?**

That would combine four currently fragmented research areas:

\[
\text{Failure attribution}
+
\text{causal inference}
+
\text{distributed rollback}
+
\text{agent recovery}.
\]

It is much deeper than simply developing another error classifier.

An experiment could deliberately create both:

- local faults that stay contained,
- local faults that propagate through multiple agents.

The system would then need to identify:

\[
root\ cause
\]

\[
affected\ descendants
\]

\[
safe\ rollback\ boundary
\]

and perform:

\[
selective\ reexecution.
\]

The strongest evidence would be whether selectively fixing the diagnosed region restores success significantly more often than matched random rollback or ordinary resampling.

That directly answers the scientific question:

> **Did we actually understand the failure well enough to repair it?**

---

## 29. The key research lesson

The field has progressed approximately like this:

\[
\textbf{2024–25:}
\quad
"What failures exist?"
\]

MAST and resilience work.

\[
\textbf{2025–26:}
\quad
"Which agent/step caused them?"
\]

Who&When, TraceElephant, ECHO, AgenTracer, FAMAS, ErrorProbe, causal-inspired approaches.

The natural next step is:

\[
\boxed{
\textbf{2026+:}
\quad
"Can we experimentally prove the cause and repair only its consequences?"
}
\]

That final step is still substantially underdeveloped.

And it connects unusually well to decades of rigorous work in **distributed checkpoint/recovery, fault localization, delta debugging and causal intervention**, rather than relying entirely on new LLM-specific heuristics. ([research.ibm.com](https://research.ibm.com/publications/a-survey-of-rollback-recovery-protocols-in-message-passing-systems?utm_source=chatgpt.com))

For the broader multi-agent research map, **Failure Attribution, Diagnosis & Recovery** is a field with significant remaining research depth, with the strongest unsolved portion being **causally validated, dependency-aware selective recovery**, rather than another taxonomy or another LLM judge.
