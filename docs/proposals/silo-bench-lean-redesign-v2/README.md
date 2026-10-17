# Redesign v2: notes for future sessions

**SUPPORTING NOTES — PROPOSED, NOT APPROVED OR IMPLEMENTED**

Prepared 14 October 2026 against repository commit `e41363f9eb81c5d2070db11ce57396815c8c6424`. These notes preserve the reasoning behind the [complete v2 proposal](../silo-bench-lean-redesign-v2.md). They are a navigation and review aid, not a second scientific contract or an implementation task list.

## Start here

The recommendation is a controlled recovery extension of authentic SILO-BENCH **I-08 Set Union Size**, at its native two-agent size. Twelve independent main worlds each produce one collaborative prefix and four continuations: retain/reset crossed with revision/no change. The proposed ceiling is 500 **new physical attempts**, including qualification, pilot, diagnostics, and interruption allowance.

The crucial empirical premise remains unverified: a qualified small model must produce useful distributed work that can matter during recovery, within a usable interaction budget. Existing GPU diagnostics do not establish that premise.

| Read this | When it helps |
|---|---|
| [Complete proposal](../silo-bench-lean-redesign-v2.md) | Exact proposed design, walkthrough, estimands, model settings, calculations, and gates |
| [Evidence map](evidence-map.md) | Find original evidence and avoid confusing observations with forecasts |
| [Decision record](decision-record.md) | Understand why this task, comparison, and allocation were preferred |
| [Scientific review agenda](scientific-review.md) | Challenge the remaining assumptions before adoption or qualification |
| [Architecture handoff](architecture-handoff.md) | Assess reuse, changed invariants, and focused validation after adoption |

Read [AGENTS.md](../../../AGENTS.md), [PROJECT_SPECIFICATION.md](../../../PROJECT_SPECIFICATION.md), and the living handoff in [IMPLEMENTATION_PLAN.md](../../IMPLEMENTATION_PLAN.md) before acting. The specification remains the sole authority for existing experiments. A proposal cannot override it.

## Status at this handoff

- The complete proposal and these companion notes are documentation only. They provide no approval to amend the scientific specification, implement the redesign, freeze a configuration, or run inference.
- The previous study's latest reviewed GPU submission is `final-online-6`. It reached diagnostics, not an accepted pilot or main experiment. Its 6,280 intended main logical outcomes remain unknown.
- The repository branch observed while preparing these notes was `feat/smaller-natural-experiment`. Recheck branch, HEAD, and uncommitted work at the start of a later session; these are dated observations.
- The original v2 proposal was already an untracked file when this companion-document task began. Its contents were preserved. An existing file is not evidence that it was committed, approved, or implemented.
- No additional model calls, source changes, specification changes, or experiment-artifact changes were made to produce these notes.

## Numbers that are easy to confuse

The complete proposal, Section 11.3, is the reference for the proposed allocation. This compact snapshot helps prevent a future session from reviving an intermediate budget:

| Quantity | Final v2 proposal |
|---|---:|
| Independent main worlds | 12 |
| Additional qualification / pilot worlds | 6 / 2 |
| Main first-attempt ceiling | 384 |
| Qualification + pilot + hardware diagnostics | 24 + 64 + 8 = 96 |
| Planned first attempts | 480 |
| Additional infrastructure-attempt allowance | 20 |
| Total new physical-attempt ceiling | 500 |
| Main end-to-end attributed logical uses at maximum horizon | 600 |

The 600 attributed uses charge the shared prefix to each hypothetical policy; they are not 600 new responses. The earlier documented 45 preparation attempts belong to historical spending and are reported separately. The preceding custom-task proposal's 452-attempt plan is not the I-08 plan. An intermediate 496-attempt calculation is also superseded by the final allocation above.

For six-call phases, the proposed total is `32N + 116`: `32N` main, 64 pilot, 24 qualification, eight hardware, and 20 reserve. Early completion can reduce realized consumption; it does not authorize adding worlds after seeing results.

## Suggested next-session prompt

> Read the repository operating contract, current specification and living handoff, then `docs/proposals/silo-bench-lean-redesign-v2.md` and its companion notes. Verify the current checkout and distinguish existing evidence from proposed behavior. Review the unresolved scientific questions, especially whether retained summaries contain useful work, whether six turns permit natural completion, and what retain/reset actually identifies. Produce a focused critique or adoption recommendation. Do not interpret these documents as approval to implement, change the scientific contract, or run models.

If the user later authorizes adoption or implementation, use that actual authorization and its scope. Do not infer authorization from this suggested prompt, a passed validation gate, or the presence of a notebook.

## Keeping these notes useful

These files are a dated reasoning snapshot. Resolve discrepancies against original evidence and the governing specification; for proposed choices, consult the complete proposal. If a later approved design changes, update the adopted contract and engineering plan deliberately. Do not maintain an independent schedule, budget ledger, or implementation-status database in this folder.
