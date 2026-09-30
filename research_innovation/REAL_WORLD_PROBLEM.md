# The real-world recovery problem

Status: first-principles problem definition, 2026-09-30. No proposed method has been validated.

## What actually changes

A team has spent hours acquiring observations, deciding what to investigate, rejecting options, writing code, running tools, communicating intermediate results, and allocating unfinished work. An authoritative change arrives: a requirement is revised, a file changes, a database record is corrected, a measurement is withdrawn, or permission is revoked. Some work remains useful; some becomes false; some remains true for a different reason; some is now irrelevant. A change may also make a previously rejected option viable.

The task is to complete the current objective under current constraints, while retaining useful investment and preventing obsolete state from exercising unjustified authority. Correct output alone is insufficient if a stale action was already taken during recovery. Conversely, reproducing exactly the trajectory of a team that never saw the old fact is unnecessarily strong for ordinary factual correction. Historical reasoning can legitimately suggest a currently valid solution.

## State that recovery must account for

| State | Why it matters |
|---|---|
| Authoritative observations and instructions | Sources can disagree; arrival order need not equal authority or effective time. |
| Derived results and artifacts | An obsolete premise may have many indirect descendants, including correct ones. |
| Private context, summaries, plans and retrieved memory | Deleting a shared record does not remove its paraphrases or behavioral effects. |
| In-flight messages and tool calls | An old worker can reintroduce obsolete work after the team has apparently recovered. |
| Search decisions and rejected alternatives | Missing work is a consequence too; there may be no positive dependency edge to invalidate. |
| External effects | A sent email, purchased resource or committed deployment may require compensation, not replay. |
| Commitments between agents | Correct local revisions can still leave inconsistent assignments or incompatible partial results. |

## Required distinctions

1. **Current validity:** does this artifact meet its present contract?
2. **Historical dependence:** did old information influence its construction?
3. **Permission to use:** may this artifact influence this particular consumer now?
4. **Global adequacy:** do the accepted pieces jointly solve the revised task?
5. **Counterfactual forgetting:** must every behavioral influence of a source disappear?

These are different predicates. An old path may remain usable after an edge deletion even if it was found using a now-obsolete heuristic. A path can also remain traversable while ceasing to be shortest. An unchanged numerical answer may have lost its only justification. Privacy revocation can prohibit historical influence even when an answer remains mathematically valid. This project should target factual/requirement correction, not silently promise erasure.

## Desirable properties

- **Containment:** old work cannot enter the authoritative working state merely because it is available or persuasive.
- **Selective usefulness:** valid results, gathered sources and expensive computation can survive where justified.
- **Honest uncertainty:** an absent dependency edge is not proof of independence; unsupported cases remain unresolved.
- **Compositionality:** a locally valid piece has an explicit scope; global coverage, optimality and compatibility require their own checks.
- **Progress:** recovery can complete after updates stop and sufficient current information becomes available.
- **Cost visibility:** prevention, storage, rechecking, failed reuse, communication, model calls and compensation all count.
- **Practical integration:** ordinary artifacts, source reads, context boundaries and tools should suffice; no access to hidden chain-of-thought is assumed.

## Fundamental boundary

If two worlds produce the same recorded state and announced update, but reuse is valid in one and invalid in the other, a policy seeing only that state cannot always distinguish them. It needs additional current-world evidence, a trusted validity contract, conservative recomputation, or an explicitly accepted risk. More elaborate bookkeeping cannot reconstruct information never observed. This is an elementary indistinguishability argument, not a claimed new theorem.

## Scope ladder

The minimum experiment should establish recovery from one announced authoritative change in a reproducible environment. A useful runtime principle should also have a defined response to delayed old messages and a second change. Unannounced change detection, authority disputes, irreversible side effects, adversaries, and unrestricted natural-language validity are separate extensions. Excluding them from the first experiment does not make them unimportant.

SILO provides small exact outcome measurements. It does not establish hours-long economics, autonomous truth discovery, or general real-world reliability. Those claims require separate evidence.
