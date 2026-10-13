# Final-online-4 repair: implemented and CPU-verified delivery

The user requested full repair after the [complete proposal](course-kaggle-final-online-4-proposal.md).
Specification §11.3 records the scoped adoption. The original five submitted
artifacts remain byte-identical; their 23 historical preparation attempts remain
counted. No GPU work, checkpoint-weight download, freeze/main run or publication
was performed here.

## Upload and run

Use these matching artifacts:

- [Ready notebook](../../notebooks/run/final-online-4/notebook-fixed.ipynb), also
  `dist/course-kaggle-final-online-4/course_kaggle.ipynb`.
- `dist/course-kaggle-final-online-4/course-kaggle-dataset.zip`: **4,673,456 bytes**,
  exactly two opaque input files, with no weights, wheels or old resume seed.
- [Concise runbook](../KAGGLE_COURSE.md), also the delivery's `START_HERE.md`.

Upload the ZIP as a fresh private dataset, attach only that dataset, import the
matching notebook, select **T4×2**, enable **Internet**, and **Run All**. Do not
attach the old final-online-3/4 payload: the scientific model/prompt changed.
Later sessions attach this same dataset and its latest matching
`course-resume.payload`. Keep results, the resume payload and executed notebook.
The final cell always exports available evidence. Provider deallocation still
requires stopping the interactive session normally.

## Implemented behavior

- Qwen3.5-9B first, with the pinned 4B as the sole declared pre-main fallback.
  Each has its own normal source/settings-bound bundle and fresh fixed matrix.
- Uniform persisted `course_compact_v1` instructions clarify answer values,
  coordinate order, integer shapes, send fields and single-line JSON. All
  permitted data bytes are unchanged; original rendering remains supported.
- Both checkpoints have verified text-weight inventories, including 9B's
  untied head. The native tokenizer/template files are identical, so their
  complete payload proof is reused with 565 conservative added ASCII bytes:
  **110,416 input + 256 output = 110,672 resident tokens**.
- Envelope probes receive **600 seconds**; all ordinary research calls retain
  **120 seconds**, original sampling and bounded cleanup. Phase/elapsed/token/
  allocator progress is flushed to existing process logs. Terminal reports name
  the actual failed attempt; incomplete memory samples cannot pass the gate.
- Historical 23 plus at most 24 hardware attempts per candidate gives the
  adopted **71 cumulative maximum**. Higher documented history is retained.
  Hardware retries consume the candidate's 24; known timeouts/wrong/invalid
  outputs are never retried. Hour totals remain observational.
- Incomplete sessions stay on their candidate. A completed pre-main hardware
  or capability/protocol failure can select 4B. Raw/effect audit defects and
  frozen/main failures cannot. Every original first-90/full-pilot/freeze gate,
  population, intervention, exact replay, seed and missingness rule remains.
- Both candidate histories receive supported SQLite backups and travel in the
  resume export. Results contain nested gate/debug JSON, reports and figures;
  all progress is derived from existing stores. Dependencies and original
  pinned checkpoint shards download online with native integrity checks.

No speculative chunk/kernel change or output repair was introduced. The new
phase measurements will show whether further performance work is justified.

## Verification and exact packet

Source packet: `4deee720e0f2bee12f5331cc933d542083a05f78`.
Dataset SHA-256:
`5b50098f1ef999d64f3cea6820d3a602d1eb89e96a39699e1edd2826d5a099ee`.
All 97 Linux/Python 3.13 dependency pins match the previous reviewed delivery.
The source packet has 85 members; its manifest publishes the renewed bound.

The [CPU receipt](../../notebooks/validation/course-kaggle/final-online-4-repair-delivery-cpu.json)
and [executed CPU notebook](../../notebooks/validation/course-kaggle/final-online-4-repair-executed-cpu.ipynb)
record actual checks on Windows/Python 3.11.9, Torch 2.11.0+cpu and Transformers
5.12.0. Seventy-seven focused checks passed, followed by two focused checks for
higher-history preservation. They include the real 24-row controller on
scripted providers, both actual native tokenizers/generation contracts, 9B worker
binding, permitted-data equality, exact durable reuse, fallback/refusal rules,
legacy incident constraints and distinct nested SQLite backups.

The existing delivery validator executed all literal notebook cells with the
ordinary installed delivered source, no source `PYTHONPATH` and zero inference
calls. The three mandatory host checks and delivered loading contract passed.
Run All/export, independent analysis twice and restored analysis passed; every
report/figure byte matched. Seven SVG and seven PNG figures were produced.
All 6,280 main uses correctly remain unknown in this CPU validation.

Actual T4 fit, ordinary latency, pretrained-model quality, pilot acceptance and
main outcomes remain unexecuted. A 600-second stress success would establish
only the amended diagnostic criterion; it does not establish the old
120-second result. If either native configuration fails its mandatory gates,
the package preserves its evidence and produces a limited result.
