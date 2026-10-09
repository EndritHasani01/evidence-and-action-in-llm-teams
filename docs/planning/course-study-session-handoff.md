# Course study: lessons and fresh-session handoff

Reviewed 9 October 2026 against checkout `09a85b8`. This is a starting guide, not a second specification, task tracker or passing gate. Verify the current repository and linked evidence before acting; dated observations below may be superseded.

## Start in the actual checkout

Use read-only checks before trusting a remembered path, branch or completion claim:

```powershell
git rev-parse --show-toplevel
git status --short
git branch --show-current
git log -1 --oneline
```

At this checkpoint, `docs/validation/m5-inference-preparation.md` has a pre-existing local edit. Preserve it and other uncommitted work. Stage explicit task files and inspect the staged diff before committing. Missing Git metadata or root files require diagnosis and artifact preservation, not a reset, clean, deletion or fresh repository initialization.

Read in this order:

1. [AGENTS.md](../../AGENTS.md) and [repository orientation](../../README.md).
2. The relevant [scientific specification](../../PROJECT_SPECIFICATION.md) and [implementation plan](../IMPLEMENTATION_PLAN.md) sections, including the applicable gates and living handoff. The specification alone governs scientific semantics.
3. The [course index](../todos/course/README.md), then one selected course task and its prerequisite evidence. Qualify IDs as `course/M2-T01`: the [thesis tree](../todos/README.md) uses the same short ID format for different tasks.
4. The [course proposal](abs-iis-course-study-proposal.md) for proposed scope, and the [research synthesis](../implementation-research/SYNTHESIS.md) plus only the investigations relevant to that task.

The next task at this checkpoint is [course/M1-T01](../todos/course/M1/M1-T01-course-contract-and-reuse-boundary.md). It prepares and establishes explicit course adoption before behavioral changes. The task index owns current readiness and counts; this document does not duplicate them.

## Reuse evidence within its actual scope

| Verified or observed record | Lesson for a new session |
|---|---|
| [M1–M4 CPU acceptance](../validation/m4-cpu-gate.md) | Generators/truth, protocol, interventions, durable workers/accounting and offline analysis already exist. Audit reuse and renew affected course checks; do not rebuild the project or repeat every unchanged suite. |
| [Kaggle run 5](../validation/m5-kaggle-full-preparation-run-5.md): 97 CPU checks pass, zero skips, installed provenance and off-host snapshots checked | The earlier unchanged CPU preparation is accepted. Course/source/environment changes need relevant new checks; they do not invalidate unrelated evidence or justify another generic preflight by default. |
| [Kaggle run 6](../validation/m5-t4-compatibility-run-6.md): standalone attention/NF4 diagnostic passes on both T4s | This is actual library evidence, with a host environment different from the full candidate. It contains no pretrained-model generation and does not establish full candidate, language loading, state, memory or capability acceptance. |
| [Offline attention/memory audit](../validation/m5-attention-memory.md) | The opt-in adapter and bounded prefill are CPU/source verified. Its new head/mask/chunk layout still needs actual candidate CUDA validation. Smaller prefill chunks preserve all input/cache content; they do not shorten the scientific context or prove complete-envelope fit. |
| Existing `m5-kaggle-source-v2` and historical notebook results | Preserve them. The payload contains earlier source and cannot deliver the new attention adapter or future course changes. Prepare a new committed-source packet with renewed provenance when needed, rather than treating an old source marker as evidence of current bytes. |

Older research and notebook plans intentionally retain earlier failures and pending statements. Read their dates, later handoffs and actual returned artifacts together. For example, the [first-run lessons](m5-kaggle-first-run/06-lessons-learned.md) explicitly supersede their original missing-checkout diagnosis. Do not diagnose the current repository from that historical sentence alone.

## Keep the course regime separate from the thesis regime

- The smaller course configuration is still a proposal until the scientific authority records its explicit adoption. Direct 4B selection, smaller instances/caps/populations and the proposed resource ceiling are consequential changes, not ordinary defaults to silently overwrite.
- The course task tree reuses foundations and owns course adaptation/acceptance. Completing it does not close original thesis tasks or replace their populations, model/resource obligations and evidence. Preserve their defaults and artifacts.
- Four recovery rounds are the proposed default. The optional three-round regime changes endpoints, attainability, capacity and schedule accounting; it is not an automatic fallback when a run is slow.
- Fewer worlds reduce total calls, not the largest permitted request. A smaller model reduces some weights, not necessarily full-attention cache geometry. Resolve the complete course input/memory argument, including invalid retained text, cache growth, workspace and required headroom. Short successful prompts, fixture maxima and arbitrary padding cannot replace that proof. See the [course memory analysis](abs-iis-course-study-proposal.md#memory-why-4b-and-fewer-worlds-are-insufficient-alone).
- Main and development worlds/streams are disjoint; controls, focal populations and repeats are predetermined. Smaller-study precision is limited. No unfavorable world, failed prefix, inactive Q case or incomplete comparison disappears to improve the report.

## Scientific mistakes to prevent

- Keep gold, hidden sources, future edits and condition metadata out of peer views. Current source authority and retained derived text are different; host repair must never supply a corrected model answer.
- Start siblings from independent drained original-prefix snapshots. Apply literal retention once. K retains the actual valid last candidate, including a wrong one, or absence; C/F differ in acquired evidence. Checkpoint reducers must not restore cleared history.
- Persist raw replies/failures before effects. Resume them exactly, including invalid outcomes. Required mixed/Q reuse checks permitted state, rendered/native request, settings, seed and parent scope; matching seeds alone is insufficient. Effects remain branch-local.
- Preserve synchronous visibility. Q delays received prose only, leaves source delivery normal, and releases held first-round prose before second-round prose before round three. Framework replay or a copied post-delivery parent state is not this intervention.
- Recorded invalid/failed slots are zero-credit outcomes; unexecuted slots are unknown. Failed slots inherit no earlier answer. Preserve shared physical-response identities through missingness bounds and keep physical attempts separate from logical policy costs.
- Keep replicate zero in primary tables and case selection. Continuation repeats share the original world/prefix and do not add independent clusters or establish new-prefix repeatability.

The exact definitions remain in the specification and selected task. These reminders are failure shields, not replacement formulas or additional experiment arms.

## Avoid repeating operational failures

- **Diagnose the first failing prerequisite.** A missing source fixture can block installation and tests without demonstrating package or model failure. Label downstream checks unexecuted. Inspect the user's notebook/results before assigning a cause.
- **Verify cloud transport before depending on it.** Archive upload/extraction can change nested compressed fixtures. Use canonical protected bytes and existing transport checks; repeat a small canary only when a changed route or observed failure needs it. Do not repair delivery by regenerating scientific fixtures.
- **Separate machine receipts from ordinary stdout.** Library documentation messages previously broke JSON parsing despite a successful child command. Use the existing dedicated evidence path. A warning such as the historical missing-`wrapt` hook needs an identified causal failure before changing the base environment or package pins.
- **Validate the installed candidate, not accidentally the source tree.** Use its explicit interpreter outside the checkout without source `PYTHONPATH` injection; inspect module provenance. Recreate environments from the passing closure rather than copying a populated venv or broadly upgrading packages.
- **Use explicit UTF-8 on Windows.** Read Unicode documents with `Get-Content -Encoding UTF8` and run Python text checks with `python -X utf8`. PowerShell's default pipe encoding can alter Unicode embedded in inline scripts before Python sees it; ASCII scripts with explicit Unicode escapes avoid that ambiguity.
- **Plan disk and export separately from VRAM.** NF4 does not shrink original weight downloads; temporary/cache copies and export creation consume disk. Two devices do not supply one combined replica-memory pool. Preserve off-host reopen checks for actual retained snapshots.
- **Count allocated time, including idle/setup/release.** Two assigned T4s for 15 minutes consume 0.5 aggregate GPU-hour. Another account does not erase scientific spending, and an unknown historical interval is not zero. Reconcile available resources before admission and confirm allocation release afterward.
- **Do not rerun model work merely to save it.** Kaggle Save & Run All can execute a new session. Use the prepared export path and retrieve the actual evidence; session-local files, notebook source and a verified off-host bundle are different durability claims.

The [existing Kaggle retrospective](m5-kaggle-first-run/06-lessons-learned.md) contains the detailed transport/environment/storage failure history. Consult the relevant part when a matching problem recurs; it is not a required sequence of extra preflight runs.

## Make the next handoff actionable

Work on one selected task outcome with the smallest necessary change. Reuse existing IDs, configuration, manifests, worker SQLite records and checkpoints; derive progress/exports rather than adding another store. Record consequential decisions in the existing plan, not another authority document.

Finish with the exact commands actually run, environment, pass/failure results, artifact locations, changed configuration, outstanding limits and next ready task. Update that task and the course index together. Make clean logical commits while preserving unrelated edits.

Documentation changes need link/consistency checks; behavioral changes need focused scientific failure-mode checks. CPU/mocks do not stand in for actual GPU acceptance. A failed feasibility gate can still yield an independently audited limited report; it cannot be marked as a completed empirical study.

Passing a technical gate grants no execution authorization. Complete the concrete safe preparation before requesting any missing approval; honor existing authorization within its recorded scope. GPU/main execution, scientific or frozen-configuration changes and external submission/publication retain the repository's separate boundaries.
