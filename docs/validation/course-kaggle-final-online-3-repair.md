# final-online-3 repair and delivery

The user requested full repair after the [incident proposal](course-kaggle-final-online-3-proposal.md).
The software repairs and reviewed preparation continuation are implemented. This
does not establish native full-input feasibility, capability, pilot acceptance,
freeze or main results. No GPU/model call was made during this repair.

## Upload and run

1. Import the [repaired notebook](../../dist/course-kaggle-final-online-3/course_kaggle.ipynb).
2. Upload the [repair dataset ZIP](../../dist/course-kaggle-final-online-3/course-kaggle-dataset.zip)
   as a new private Kaggle dataset and attach **only that matching dataset**.
3. Select **T4 x2**, enable **Internet**, then **Run All**. Leave the controls unchanged.

The ZIP is **18,058,741 bytes (17.22 MiB)** with three opaque files: the packed
source, integrity manifest and prepared resume payload. It contains no model
weights or dependency wheels. The resume seed is already included; attaching the
old failed payload separately is unnecessary and would create an ambiguous input.
For later sessions, attach the same dataset and one latest exported resume payload;
the separately attached export takes precedence over the seed.

A tracked copy is [notebook-fixed.ipynb](../../notebooks/run/final-online-3/notebook-fixed.ipynb).
The [operator instructions](../KAGGLE_COURSE.md) describe monitoring, exports and
analysis reproduction. The [delivery receipt](../../notebooks/validation/course-kaggle/final-online-3-repair-delivery-cpu.json)
records the exact package identities and executed checks.

## Repairs and continuation

- Diagnostic requests use the actual one-field `RenderedRequest` schema.
- Forced-length diagnostics use explicit `eos_token_id=[]`. Real pinned
  Transformers processors verify that the old `None` inherits EOS and triggers
  the finite-score failure, while the correction preserves the numerical audit.
- All 24 request boundaries and native tokenization are checked on CPU before
  checkpoint download. Ordinary settings and input/output limits remain unchanged.
- Parent failures retain the original traceback, phase, call/device and whether
  an attempt started. Progress distinguishes saved outcome reuse from generation.
- Idle providers use the existing stop sentinel within unchanged TERM/KILL bounds;
  hung/in-flight attempts retain immediate bounded termination.
- Fully recorded matrix outcomes can be reconstructed at the attempt ceiling.
  Every new physical attempt still requires the original cumulative admission.

The continuation is prepared offline from the **exact submitted archive**. There
is no runtime source-check bypass or general migration rule. Its original source,
runtime configuration, host receipts, report, plan and analysis receipts remain
under `repair/`; both original canonical worker databases and backups are
byte-identical. The two previously unprepared envelope rows change only their
unsupported rendering field. The ordinary inference module is AST-identical
apart from the diagnostic EOS assignment; the pinned dependencies and all
ordinary requests/settings are unchanged. Old outcomes retain their old source
provenance in `repair/receipt.json`.

Usage remains **one retained loader failure + 21 completed probes = 22/25**.
Only `course-hardware/envelope/device-0`, `course-hardware/envelope/device-1` and
`smoke/course-m5/24` remain. The original 21 generated replies, including invalid
ones, are reused exactly. The user-authorized 25-attempt allowance is not enlarged.

## Verification and limits

On Windows/Python 3.11, 45 focused CPU checks passed, including the real 24-row
controller, both envelope transitions, a bounded controlled hang, original-21
continuation, reconstruction at 25 without another attempt, original traceback
capture and external-resume selection. Scripted providers are CPU fixtures, not
native feasibility evidence. Real Transformers 5.12.0 and Torch 2.11.0+cpu
configuration/processors also passed the delivered preflight command with the
archived native tokenizer; no model was instantiated.

The actual notebook's CPU-safe Run All cells executed with the uploaded three-file
layout and an ordinary installed CPU package. Three required host checks and the
delivered loading check passed. Both exports reopened successfully; all 21 saved
worker bytes remained unchanged; seven SVG/PNG exhibits and two independent
report reconstructions reproduced after restore. All 97 Linux candidate pins
match the preceding package. Final packaging only additionally archives original
configuration/host receipts and corrects welcome wording: execution source,
database bytes and every executed code cell are unchanged. Archive CRC checks pass.

The delivered source is bound to `d6c2d6d9336dc80e85ca3e5fc75c8f1cb2d26797`.
Dataset SHA-256 is
`44a21a5df8ded5b464d75e83c6bade75bed6c07ac79d9b3d385b18f5bfbcd1e9`.
The receipt includes the notebook hash, source-difference audit, original worker
hashes, exact test commands and pinned processor observations.

Kaggle still must establish both 109,851-input + 256-output T4 probes within the
approved 120-second attempt bound, finite/fresh-state evidence, at least 1.5 GiB
headroom and controlled-timeout cleanup. Then the unchanged capability/pilot and
conditional freeze/main gates apply. The submitted stress replies were only
2/21 protocol-valid; they are not the pilot validity estimate. A failed native or
scientific gate therefore remains a possible accurate limited result. All 6,280
main logical uses remain unknown until actual research execution.
