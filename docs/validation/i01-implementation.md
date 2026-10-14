# I-01 implementation evidence

14 October 2026, Windows Python 3.11.9 development checkout. This document
records focused implementation checks, not an extensive CPU campaign or Kaggle
research acceptance. No model is loaded and no empirical study call is made.

## M0 / M1 checkpoint

Design adoption: `6875aae`. Native fixture maximum 827 and revision
agent 0 row 12 → 100 maximum 780 were recomputed by `recovery.i01.core.oracle`.
The focused development command generated 29 saved worlds, checked the legal
three-call confirmation sequence ends with both submissions, and checked literal
retain and empty clear histories. Those checks passed. Fixed main assignment
contains five worlds in each owner/first-speaker stratum, with paired recovery
seeds and balanced treatment execution order. Actual tokenizer, model capability,
runtime, hardware/headroom and Kaggle operation remain pending.

## Durable design

The old four-peer `WorkerStore` is not used for synthetic I-01 rounds. The small
I-01 registration schema uses the same WAL/FULL transaction discipline. Each
world belongs to one canonical database. Admission is serialized by the one
controller across the explicit two-store inventory; raw replies/failures and
effects are separate transactions, with effects and checkpoint atomic together.
Only stage/gate/session metadata is held in slot 0. Historical DBs are untouched.
