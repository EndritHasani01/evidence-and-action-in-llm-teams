# Research and novelty update

Primary sources and access statuses appear in `09_SOURCE_REGISTER.md`. This is a targeted update of the closest work, not proof that no matching paper exists. Do not copy paper summaries into a thesis without reading and citing the actual sources.

## Close comparisons

| Work | Relevant evidence inspected | Implication for this project |
|---|---|---|
| From Faulty Memories to Corrected Actions [R1] | Typed provenance and selective replay; §3.2 excludes inference of missing support/lifecycle edges from raw natural language. Prompt contracts address tool calls and replacement arguments. Includes an LLM repair-planning baseline. | Neither action repair nor LLM-selected repair scope is new on its own. Compare natural handoff support and the factorial intervention specifically. |
| MemTX, v2 [R2] | §3.4 repairs recorded typed descendants; compensation is an obligation rather than environmental replay. §3.5 distinguishes stronger action-safety checks. §5 describes missing declared parents and scope blind spots. | “An omitted dependency defeats repair” is already recognized. Determine what the proposed experiment explains beyond that observation, including action-specific binding and residual recipient-state errors. |
| REVISE, v1 [R3] | Versioned artifacts, selectors, revision deltas, recovery of partially executed graphs, conservative fallback, staged-effect revalidation; evaluation includes LangGraph/LLMCompiler applications. | Selective runtime recomputation and framework integration are close infrastructure prior art. They do not automatically answer the proposed behavioral interaction; compare experimental objects and interventions. |
| MemoRepair [R4] | Withdrawal barrier, validated successors, predecessor closure and repair optimization. | Withdrawal-aware repair and minimal repair objectives are established neighboring ideas. |
| Repair Sets Before Repair Choices [R5] | Title/index metadata located. Full forum/PDF requests still encounter access challenges. | Mandatory unresolved close comparison. Do not claim its experiments omit this project's distinction without obtaining the paper. |
| AgentGit [R6] | Research repository describes checkpoints, branches, reversions, and tool-state handling around LangGraph. | Useful infrastructure reference. A research/pre-release repository is not evidence that adopting it will reduce this project's operational risk. |

## What this update resolves

The blueprint's full-text access gaps for the relevant MemTX and REVISE sections are resolved. The OpenReview full-text gap remains. No results from these papers were reproduced. No universal literature-exhaustiveness claim is justified.

## Candidate contribution, conditional on comparison and pilot

Test the interaction between **alternative evidential support** and **binding an action to a specific witness**, using naturally produced support records and interventions that separate estimated repair scope from replacement of recipient state.

The warehouse example is a useful construct: Y can preserve “fulfillable” after X changes, while `ship_from(X)` must change. The logical distinction itself is not a discovery. The potential contribution is a controlled explanation of when observed agent handoffs retain it and which recovery mechanism fails.

## Comparison required before novelty sign-off

For every close paper, record: version; task/environment; whether dependencies are declared, extracted, or hidden; whether action arguments have separate support; whether alternative support survives a correction; natural versus injected provenance error; downstream-state intervention; same-prefix counterfactual controls; outcomes; and exact page/section evidence. Mark “not reported in inspected sections” rather than “absent” when coverage is incomplete.

Seek the R5 author/preprint version through legitimate public routes, or request a user-supplied copy. If inaccessible, finish a provisional specification with a novelty gate. Symbolic development and affordable pilots may proceed; an unsupported novelty claim and expensive confirmatory run may not.

If the same explanatory experiment already exists, propose a meaningful replication, new boundary condition, or different estimand. Do not rename an architecture to manufacture novelty. If only infrastructure overlaps, reuse that infrastructure where suitable and preserve the scientific question.
