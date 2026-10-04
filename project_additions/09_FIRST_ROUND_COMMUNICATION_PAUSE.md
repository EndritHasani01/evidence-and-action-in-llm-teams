# 09 — Delay messages produced in the first recovery round

**Recommendation: reserve as a targeted communication experiment.** The original protocol already prevents peers from seeing one another's first-round recovery outputs until their next calls. A meaningful pause must therefore affect round two or later. Simply claiming that peers first reconsider independently would add no new treatment.

## Simple question and thesis value

Does giving each peer one more call before it sees the others' first recovery messages improve revision, or does it delay useful information too much?

This tests the timing of post-correction collaboration. It could reveal that immediate exchanges help coordination, or that an additional interval of local work is useful when early peer messages still repeat the old conclusion. Either answer matters for scheduling a small agent team.

## Exact queue policy Q

Use B's correction delivery, current source tables and retained history. Execute recovery round one normally. Validate and save outgoing messages as usual, but **hold every round-one peer message in a separate queue** instead of delivering it before round two. Each sender still retains its own generated reply.

After round two finishes, deliver the held round-one messages followed by the round-two messages, preserving each message's generation round and stable ID. They become visible before round three. Rounds three and four then use ordinary delivery. Messages are delayed, not silently discarded; source references travel with the delayed message. There is only one authoritative edit, so this proposal introduces no second-update race.

The queue policy is enforced by the runtime. It does not add a stronger “think carefully” instruction or give peers additional calls. Its total effect includes temporarily delaying both raw source forwarding and derived prose. A prose-only delay, with raw records delivered normally, would answer a different and potentially useful question; do not mix those definitions in one arm. That alternative would split delivery of `source_refs` from delivery of text, preserve own replies and the broadcast revision, and make B/Q's current source tables equal at round two. Later evidence acquisition could still diverge in response to changed reasoning. Choose one definition before the pilot; a full two-variant factorial is unnecessary for this small addition.

## Minimum useful comparison

Select **12 fixed main worlds, two per family**. Add Q after change and under sham; compare with existing B in each event. C remains context for the overall study but is not a matched communication-timing treatment.

The first recovery outputs are identical to B's **by construction if the same saved round-one calls are reused**. No peer has yet received a delayed message. The earliest causal difference appears in round-two inputs. Do not report a first-round correctness gain from this policy; such a gain would indicate that something besides message delivery changed.

Report differences in rounds two through four, full AUC, final/stable correctness, stale-value frequency, collateral damage, delivery latency and context tokens. Keep the full four-round denominator. Do not start Q's clock after the hold or grant an extra fifth round to compensate. Recovery communication opportunities are intentionally fewer early in the fixed allowance.

Sham Q−B distinguishes a general scheduling effect from a stronger effect after correction. It cannot establish that a harmful message specifically contained stale reasoning; this needs trace evidence. A saved-message example can illustrate behavior without replacing the paired aggregate result.

## Where it is useful across tasks

| Task | Likely tradeoff to examine |
|---|---|
| Maximum | Delaying a new runner-up report may be costly; extra local reconsideration may also prevent echoing the old winner. |
| Top-K | Peers often need missing candidates from others, making delayed raw evidence a substantive cost. |
| Prefix sums | Dependency chains can lose an effective propagation opportunity. Distinguish this from poor arithmetic. |
| Difference array | If most source evidence is already present, a pause may be relatively cheap and expose effects of peer reasoning. |
| Distributed sort | Delayed boundary-value exchanges can prevent rank segments from aligning within four rounds. |
| BFS | Multi-hop information propagation can be especially sensitive to the one-round delay. |

These possibilities do not predict the sign. They explain why a pause should be treated as a real resource constraint rather than free reflection time.

## Incremental calls and implementation burden

Both Q and B have exactly the same first recovery calls if queue status is not exposed in prompts and message delivery changes only afterward. Share the saved calls at the **pre-delivery round-one barrier**, with sender replies/candidates committed and recipient effects still branch-local. B then delivers the messages; Q queues them. Do not initialize Q from B's post-delivery recipient tables or inboxes, which already contain the withheld information. If the runner only stores post-delivery checkpoints, reconstruct the Q branch from its frozen round-one input state plus the exact saved replies before applying its distinct delivery rule. Continue Q for only rounds two through four: **12 additional calls per branch**.

| Component | With exact B round-one reuse | Conservative full-branch allocation |
|---|---:|---:|
| Q change+sham on 12 worlds | **288** | 384 |
| Q change+sham on two existing pilot worlds | 48 | 64 |

Use the cheaper count only if prompt construction, saved responses, model seeds, candidate state and message queue are exactly shared and their lineage is recorded. Do not resample round one and call it shared. Reserving 384 main calls is reasonable until this ordinary checkpoint reuse is verified. Main totals are **6,144 / 4,776** with exact reuse, or **6,240 / 4,872** conservatively, for the 48/36-world core.

Estimated effort: **3–5 working days**. The implementation must keep delivery status branch-local, preserve message order, record queue release, and ensure no message is delivered twice. CPU/mock cases should settle this before inference. Actual allocation and context lengths still determine whether the addition fits the 30-hour ceiling.

## Useful outcomes and decision

- Q improves revised recovery but not sham: immediate post-correction exchange can be counterproductive under this schedule.
- Q improves both: an extra local reasoning interval may be a general coordination choice.
- Q harms performance: the team needs early communication; evidence or intermediate results arrive too late.
- Q leaves round one unchanged and later curves coincide: the pause may be unnecessary, or the small sample may be inconclusive.

This is worth doing when communication timing is a central thesis interest. Otherwise K or a fixed delayed reset gives a clearer practical state-management extension without deliberately slowing both evidence and reasoning exchange.
