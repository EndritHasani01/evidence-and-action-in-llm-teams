# 10 — Give the team one round, then clear its reasoning

**Recommendation: second-choice optional live addition, especially if the useful question is when to reset.** Use a fixed schedule before considering an adaptive controller. This proposal needs no confidence model, training, extra reviewer or access to gold answers.

## Simple question and thesis value

Should the team clear its history immediately, or first have one chance to use its old work and exchange evidence?

The current B/C comparison is immediate retain versus immediate reset. A one-round delayed reset provides a simple operational compromise. It tests whether a short continuation can extract useful evidence from old work before clearing the conversation, or whether the delay lets old conclusions interfere with recovery.

## Exact policy D1

Start from the same corrected B state and run recovery round one exactly as B. Deliver its source references and messages at the ordinary barrier. Immediately afterward, before round two, apply C's clearing operation to **all four peers**:

- Keep each peer's authoritative current source table, including valid records acquired during round one.
- Clear all derived history, prior candidates, validation history and peer prose, including the newly generated round-one reasoning.
- Keep the authoritative current revision notice outside derived history.
- Continue for rounds two, three and four with the ordinary protocol.

There is no fifth call or extra recovery round. Clearing does not restore an old source value or rewind the external world. The schedule is fixed regardless of agreement, apparent confidence, answer correctness or error messages.

This is a **total policy comparison**. D1 versus C changes both reset timing and the evidence gathered during the extra retain-history round. That is a useful operational package. It does not identify a pure psychological effect of waiting.

## Minimum comparison and selected worlds

Use **12 predetermined main worlds, two per family**. Add D1 under change and sham. Existing B and C provide never-reset and immediate-reset baselines from the same prefix. Keep all worlds and all scheduled slots, including malformed candidates and failed prefixes.

Compare D1−B and D1−C on the original AUC and full trajectories. Round one equals B when its saved calls are shared. The first answer after clearing is round two; show its accuracy and any loss of formerly correct coordinates. Inspect newly acquired raw records and message traffic to assess whether the first round collected useful evidence.

The sham branches show whether delayed clearing is generally helpful or especially useful after correction. First stable correctness remains an offline diagnostic; the runtime never uses evaluator correctness to decide when to reset or stop. An adaptive “reset if nothing changes” rule would be a different policy and requires its own validation.

## What the six families reveal

| Task | Useful question for a one-round delay |
|---|---|
| Maximum | Can the team locate or forward the runner-up before forgetting the old maximum discussion? |
| Top-K | Does the first round collect replacement candidates that remain useful after clearing? |
| Prefix sums | Can old subtotals help peers forward useful raw evidence, or is clearing them before the chain updates harmful? |
| Difference array | Is an immediate small repair already possible, making a later reset wasteful? |
| Distributed sort | Does one exchange reveal needed boundary records, or does clearing discard the very coordination it created? |
| BFS | Can one round gather useful edge records without retaining obsolete path claims? Is three clean rounds then enough? |

The corrected value is already broadcast to all peers in this policy. Any benefit is not caused by giving D1 more authoritative correction coverage than C.

## Extra calls and effort

Round one can reuse B's identical saved responses and checkpoint; only D1 rounds two through four need new inference. Use exact shared state rather than assuming similar seeds make independent generations identical.

| Component | With exact B round-one reuse | Conservative complete branches |
|---|---:|---:|
| D1 change+sham on 12 worlds | **288** | 384 |
| D1 change+sham on two existing sham-assigned pilot worlds | 48 | 64 |

Main totals are **6,144 / 4,776** with reuse or **6,240 / 4,872** conservatively for the 48/36-world core. The pilot becomes 636 or 652 calls before the existing smoke allowance and failed attempts. The 30 aggregate GPU-hour limit remains unchanged. No table of calls proves Qwen/T4 throughput; use measured condition-specific allocation.

Estimated additional implementation effort: **2–4 focused working days** if the PS reset function and per-round checkpoints already exist. Important checks are reset-after-delivery ordering, preservation of newly acquired raw records, removal of newly created prose and candidates, and immutable sibling states. This is substantially simpler than a learned adaptive reset system.

## Interpretable outcomes

- D1 beats C and B: a brief opportunity to exploit old work followed by clearing is useful under the tested fixed budget.
- D1 matches B early but loses after clearing: the reset destroys useful new work.
- D1 beats B but loses to C: clearing helps, and waiting is costly.
- D1 matches C with fewer reset-history tokens or different evidence acquisition: timing may be flexible, but cost and uncertainty decide whether that matters.
- D1 helps equally in sham: a useful general context schedule, without evidence it is specifically a correction remedy.

This remains valuable even if a fixed rule performs as well as more elaborate approaches. **Choose it as an alternative to compact-state K**, not in addition to every other mechanism. It is a good thesis extension when a practical decision about reset timing matters more than preserving a particular answer representation.
