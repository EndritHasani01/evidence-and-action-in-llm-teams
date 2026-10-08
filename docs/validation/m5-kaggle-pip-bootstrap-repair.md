# Run-3 pip bootstrap repair

Recorded 8 October 2026. The [actual run-3 review](m5-kaggle-full-preparation-run-3.md) accepts all 143 canonical source members and Linux owned-process cleanup, but records a failure inside `venv`'s `ensurepip`. Its inner traceback is unavailable. This repair bypasses that bootstrap dependency without assigning an unobserved distribution-specific cause or changing the candidate.

## Implementation and checks

[m5_kaggle_preflight.py](../../scripts/m5_kaggle_preflight.py) now creates the same isolated venv with `--without-pip`. One owned standard-library subprocess downloads the already reviewed pip wheel from its fixed HTTPS URL, with a 60-second total bound, a 30-second network operation timeout, an exact byte ceiling and SHA-256 verification before publication. The parent independently verifies both the receipt and file before any pip or bulk-package work. Reports/logs remain in the existing preparation export.

A fresh candidate subprocess runs pip directly from the verified wheel, then installs that exact hash-locked wheel offline into the venv. `-I`, `--isolated`, `--no-index` and `--no-deps` prevent inherited packages or an unreviewed bootstrap resolver from supplying pip. Ordinary candidate download, offline resolution, isolated source build, installed provenance and named scientific checks continue through the existing pipeline. The eleven roots, full 88-package closure and three build-tool versions are unchanged.

This follows [Python 3.13's documented `--without-pip` option](https://docs.python.org/3.13/library/venv.html) and the fresh-subprocess, wheel-path/runpy approach used by [CPython's bootstrap implementation](https://github.com/python/cpython/blob/3.13/Lib/ensurepip/__init__.py). It needs no extra bootstrap dependency or changes to the Kaggle kernel.

Actually executed on Windows/Python 3.11.9:

- `python -X utf8 -S -m unittest tests.test_kaggle_bundle tests.test_kaggle_preflight -v`: **25 passed, zero skipped**, including exact/short/oversized/corrupt download bytes, refused origins, controlled failed bootstrap receipts and handled-failure exports. Real archives, SQLite and owned child/grandchild timeout checks remain covered; [test log](../../notebooks/validation/m5-pip-bootstrap-repair/preflight-tests.stderr.txt).
- `python -X utf8 notebooks/validation/m5-pip-bootstrap-repair/verify_bootstrap.py`: **passed**. A real new venv initially has no pip, no user site and no inherited site packages. The production downloader fetches the 1,816,632-byte pip 26.2.1 wheel with SHA-256 `71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e`; the production wheel runner installs it offline. An outside-source probe confirms pip's exact version and venv origin, `pip check` passes, the install report matches the wheel hash and base distributions remain unchanged. [Validation](../../notebooks/validation/m5-pip-bootstrap-repair/bootstrap-validation.json) and [owned command logs](../../notebooks/validation/m5-pip-bootstrap-repair/logs/bootstrap-pip.json) retain the evidence.

Only the small pinned pip wheel was downloaded in that real check. No CUDA package closure or model weights were downloaded, and model generations remain zero. Local Windows bootstrap success is separate from Linux/Python 3.13 acceptance. The controlled complete workflow's 97 checks validate reporting, not actual candidate-host execution.

## Delivery and remaining gates

The source implementation checkpoint precedes generation of a new v3 notebook. The accepted private `m5-kaggle-source-v2` dataset will be reused without a new upload; the original v2 notebook, run-3 evidence and canonical archive remain retained. Returned retry evidence belongs under `notebooks/run/4/`.

Actual Kaggle bootstrap, the 88-package install/provenance and all 81 focused/16 native checks still require execution and review. T02 remains blocked by its host/model gates, T01 remains done and progress remains 21 done/eight blocked. Scientific code, fixtures, caps, decoding, attempt/replay semantics and allocation ceilings are unchanged.
