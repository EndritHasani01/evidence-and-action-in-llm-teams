# Prompt 3 — Consolidate a precise, practical project specification

Work in `E:\Github\recovery_blueprint\recovery_blueprint` on
*Recovering Distributed LLM Teams After Information Changes*.

This is research session 3 of 3. Independently scrutinize and reconcile:

- `docs/proposals/thesis-study-recommendation.md`.
- `docs/implementation-research/thesis-online-execution-design.md`.

Your objective is to turn their strongest defensible conclusions into **one
precise proposed project specification and a practical implementation roadmap**.
The specification should be understandable to me and detailed enough that a
developer can implement the study without inventing scientific behavior. It
must support Python scripts, one thin online Kaggle notebook, clear progress
and dependable checkpoints. This is specification work, not implementation.

## Authority and scope

Read current `AGENTS.md`, `PROJECT_SPECIFICATION.md`, relevant living sections
of `docs/IMPLEMENTATION_PLAN.md`, `README.md`, the earlier thesis proposals,
the 18 October literature synthesis and the actual source/verification evidence
needed to check the two new documents. Read referenced original sources for
consequential claims or conflicts. If prerequisite deliverables are missing,
identify that precisely; do not silently reconstruct their conclusions from
memory or treat an older proposal as the chosen new study.

`PROJECT_SPECIFICATION.md` remains the sole scientific authority. Preserve it,
the current engineering plan, implementations, configurations, frozen inputs,
notebooks, completed course results and historical research. Create proposed
Markdown documents only. Do not adopt amendments, implement the experiment,
download model weights, load models, perform inference, use GPUs, execute
scientific runs, book compute or publish anything. Small CPU calculations or
targeted existing read-only inspection may verify the draft's consistency.

The two preceding research outputs are candidates, not instructions that
override the current specification. Resolve their conflicts explicitly. If a
different choice is necessary, explain the evidence and trade-off; do not make
a silent change in the final prose.

## 1. Challenge the recommendation before specifying it

Check that the chosen question is scientifically meaningful given the actual
course failures and literature. Reassess task shortcuts, usefulness of old
evidence, scripted versus natural histories, comparison strength, model
capability risk, sample precision and execution cost. Do not assume a larger
matrix, more model calls or a novel mechanism makes a better thesis.

Verify that the scientific and online plans describe the same populations,
cells, prefixes, repeats, model systems, stage counts and failure rules. Check
that implementation convenience has not changed the estimand. Decide which
controls and secondary checks remain worth their cost. Keep one recommended
study, with a finite declared fallback only where scientifically justified.

Close decisions that can be resolved through research or ordinary design
judgment. Research newly unstable technical facts from official primary
sources. Actual GPU throughput, numerical behavior and headroom remain
unmeasured gates; do not invent measurements to make the document look complete.
If a material scientific or resource question truly requires my choice, state
the concrete options and their consequences while completing independent work.

## 2. Write an exact scientific contract

Specify, without leaving scientific choices to the implementer:

- Research question, intended contribution, hypotheses, allowed conclusions
  and limitations, including negative/inconclusive outcomes.
- Task inputs, mathematical truth, populations, eligibility and rejection
  rules, edit types, strata/weights and disjointness of development/main inputs.
- Source ownership, current authority, notices, historical fields, permitted
  peer views and evaluator-only information. Include a worked example of
  precisely what each agent sees before and after a boundary.
- Literal retention transformations, isolated sibling/trial starts, phase
  reopening for real edits and no change, scheduling, visibility, legal
  actions, private finality, waiting, termination and call caps.
- Exact main/control/probe populations, assignment, repeated-trial schedule,
  seed handling, primary/secondary estimands, endpoint denominators and
  missingness. Equal seeds are not exact replay or equivalent cross-model draws.
- Statistical resampling/interval conventions, clustering, multiplicity,
  practical reporting references, precision limitations and degenerate cases.
  Include small hand-scored analysis examples with expected values.
- Both intended models, pinned identities where verified, the chosen mode,
  full decoding choices, precision/context/output regime, fairness boundaries
  and bounded development opportunities. Distinguish research-verified metadata
  from GPU-qualified settings.
- Exact stage-by-stage first-attempt and contingency limits, resource accounting,
  target/fallback decision rules, capability gates and scientific stop rules.
  Wrong/invalid outcomes cannot become favorable exclusions or accuracy retries.

State every amendment needed relative to the adopted original/course regimes.
Preserve their meanings and artifacts. The new specification must not silently
redefine historical outcomes or make the old course allowance available again.

## 3. Make the operational contract equally concrete

Describe one minimal Python-first implementation and one main notebook. Fix
the scientifically consequential behavior while permitting ordinary engineering
choices that do not affect it. Specify:

- Which existing modules are reused and the minimal new/changed responsibilities,
  proposed callable/CLI interfaces, inputs, outputs and canonical storage.
- A fresh online Kaggle bootstrap that obtains pinned source and dependencies,
  then downloads model assets only for the appropriate later authorized scope.
  State necessary access/secrets and any source-distribution prerequisite.
- The complete finite notebook-cell sequence. Each cell needs a clear purpose,
  bounded work, visible progress, completion/failure summary, checkpoint or
  receipt, and idempotent rerun behavior. The notebook calls Python rather than
  duplicating scientific logic. Every code cell must end with an appropriate
  durable checkpoint or preparation receipt; bounded scientific cells must also
  expose a consistent portable checkpoint.
- Progress during long downloads, installs, loads, calls and exports, including
  counts, elapsed time, failures/unknowns, remaining budget and checkpoint path.
- Raw persistence before effects, exact resume of completed calls, bounded
  infrastructure retries, unknown spending, cell checkpoints, portable exports,
  restoration in a new session and shutdown. Do not rely only on cell-end saves.
- Source/environment/configuration mismatch handling, per-call state isolation,
  incomplete execution/analysis behavior and independently reconstructible
  reports from canonical evidence.
- Run All within an already authorized scope, explicit boundaries before new
  GPU development/main stages, and objective resource/integrity stops. Avoid
  unnecessary per-cell permission requests or automatic expansion of scope.
  Honor an already authorized unchanged whole-campaign scope subject to its
  gates; do not mistake passing those gates for authorization by itself.

Choose sensible checkpoint granularity: enough to survive interruption and
provide a download after bounded work, without repeatedly copying model caches
or duplicating authoritative stores. Account for Kaggle's actual documented
storage/session behavior and operator-specific quota inputs. A portable archive
link is not proof that it was downloaded or that a GPU was deallocated.

Provide a concise operator walkthrough from a fresh notebook, one interrupted
run and its restoration, and one completed run to final analysis/export. Label
illustrative output as illustrative and future commands as proposed.

## 4. Check completeness with concrete scenarios

Use a compact requirement-to-verification table, avoiding hundreds of cosmetic
requirements. Cover the consequential cases:

- Correct, wrong, malformed, truncated and absent submissions.
- Correct prose without a formal commitment; message-and-submit versus wait.
- Needed current evidence absent, then delivered; wrong owner/record association.
- No change, answer-changing edit and any selected answer-preserving edit.
- Different first speakers/owners, literal packet equality and sibling isolation.
- Interruption before a reply, after durable reply, before/after effects, between
  cells and during export; repeated cell invocation and restored continuation.
- A failed capability/resource gate, one model failing, budget/session exhaustion,
  unknown spending and an incompletely executed cohort.
- Positive/negative/zero policy effects, a misleading interaction caused by the
  no-change arm, repeated outcomes and a degenerate interval.

Map each to an observable expected outcome and the smallest future CPU or
GPU acceptance check. These are prospective test specifications, not claims
that the new checks have passed. Reuse existing verified invariants instead of
designing redundant frameworks, identity systems or exhaustive coverage drives.

## Deliverables

Create **`docs/proposals/thesis-project-specification.md`**:

1. Start with a short plain-language explanation, one-page design table,
   evidence/status boundary and reading guide.
2. Present the complete scientific and operational contract above, with exact
   tables, worked examples, proposed interfaces and cell storyboard as needed.
3. State fixed choices, proposed runtime pins, conditional decisions and values
   that require later actual-host measurement in distinct terms. Avoid vague
   “handle appropriately” requirements and unresolved scientific menus.
4. End with a complete adoption/amendment section identifying the specific new
   authority text to add to `PROJECT_SPECIFICATION.md`, explicit precedence and
   preserved historical scopes. This document itself remains **proposed**.

Create **`docs/proposals/thesis-implementation-roadmap.md`**:

- A dependency-ordered path from explicit adoption through CPU implementation,
  focused verification, portable notebook delivery, authorized hardware/model
  qualification, main freeze/authorization, execution and independent analysis.
- For each step: concrete work, reused assets, expected outputs, acceptance
  evidence, realistic effort/risk and what remains unverified.
- A proposed update to the existing engineering plan, rather than a competing
  live task tracker. Link to the specification instead of copying scientific
  rules into multiple sources of truth.
- A final approval package stating exactly what adoption and CPU implementation
  would authorize, expected engineering/compute scope and what GPU, paid-compute,
  main-execution and publication permissions remain separate.

Check the documents against each other, the authority and the selected design.
Reconcile all stage totals, units, sample sizes, repeats, budgets, cell scopes,
failure paths and local links. Explain any remaining material uncertainty
explicitly. Preserve the previous research outputs as history.

Finish with the single recommended project, why it is practical, both file
paths, any real blocker and the precise approval needed next. Do not implement
or execute the proposed study in this session.
