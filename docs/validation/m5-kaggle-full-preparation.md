# M5 full-source Kaggle preparation repair

Implementation started 8 October 2026 after the [actual upload canary passed](m5-kaggle-upload-canary-run-2.md). The [ordered repair contract](../planning/m5-kaggle-first-run/05-implementation-and-validation.md) governs this work. Scientific code/configuration, the original archive and returned notebooks/results remain unchanged. T01 stays done and T02 stays blocked until actual host/model gates pass.

## Source delivery checkpoint

[build_kaggle_bundle.py](../../scripts/build_kaggle_bundle.py) copies the canonical original ZIP unchanged to `m5-kaggle-source.payload` and emits a complete member manifest. It records the scientific baseline separately from the actual operational build commit. Existing output directories are refused; no scientific fixtures are regenerated or recompressed.

Executed on Windows/Python 3.11.9:

- `python -S -m unittest tests.test_kaggle_bundle -v`: four passed, zero skipped; [final log](../../notebooks/validation/m5-full-preparation/bundle-tests.stderr.txt).
- Streaming audit of the original archive: all 143 member CRCs/sizes/hashes read, 109,248,341 archive bytes, 165,002,177 outer decoded bytes, 14 gzip and two nested ZIP members; [audit](../../notebooks/validation/m5-full-preparation/canonical-bundle-audit.json).
- Original archive SHA-256 remains `57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f`.

The initial unsafe-backslash case exposed Windows `ZipInfo` normalization. The test now writes the intended raw header and the builder validates `orig_filename`, rejecting normalized separators and control characters. Both initial failed logs are retained alongside the passing result. This is a transport-path fix; scientific source and fixture bytes are untouched.

The runtime helper, clean candidate environment, bounded commands and corrected notebook are subsequent checkpoints. Full-size upload, Linux/Python 3.13 installation and GPU/model acceptance are not established by this source audit.
