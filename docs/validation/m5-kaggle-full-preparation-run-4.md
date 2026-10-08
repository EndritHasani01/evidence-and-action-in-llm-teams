# Actual Kaggle full-source preparation run 4

Reviewed 8 October 2026. The user returned [notebook-exec.ipynb](../../notebooks/run/4/notebook-exec.ipynb) and [preflight-results.zip](../../notebooks/run/4/preflight-results.zip). Original bytes are retained. The [independent review](../../notebooks/validation/m5-full-preparation-run-4/validation.json) verifies the delivered source, ZIP receipt/CRC, install reports, probe receipt and off-host SQLite copies.

## Actual outcomes

| Scope | Recorded outcome |
|---|---|
| Canonical source/input | Pass; all 143 original members match, including compressed fixtures. |
| CPU host/owned-process cleanup | Pass on Linux/Python 3.13.15; intentional timeout reaps the owned parent/child/grandchild tree. |
| Candidate environment | Pass; pinned pip bootstrap, all 88 wheel downloads, offline resolution/install, isolated project build and noneditable install complete. |
| Installed-package stage | Fail; strict JSON parsing rejects upstream messages before the otherwise complete probe receipt. |
| Focused/native checks | Four dependent stages blocked; none of the 81 focused/4+4+8 native checks executed. |
| Synthetic filesystem/export | Pass; closed snapshots independently reopen read-only/immutable with integrity `ok`, row `7` and rejected writes. |
| Model/GPU gates | Zero model generations; no weights, GPU-native diagnostics, smoke or provider-allocation/release acceptance. |

Six stages pass, one fails and four are blocked. The CPU workflow takes **290.904 seconds**; environment setup accounts for **264.268 seconds**. Candidate download takes 72.223 seconds, installation 122.893 seconds and offline resolution 38.144 seconds. The four early console lines were the beginning of this successful setup, not a hung command. Actual wheel ZIP expansion is 7,253,701,334 bytes; selected downloads remain 4,068,346,127 bytes. Neither disk figure establishes a provider quota.

All eleven regular command records exit zero and confirm their Linux process group exited. The separate intentional owned-process timeout also confirms exit and passes its diagnostic. `pip check` reports no broken requirements. Resolver/install reports match every candidate version and selected wheel hash. Build-tool isolation still uses the reviewed setuptools 84.0.0/wheel 0.48.0, separately from candidate setuptools 81.0.0.

## Exact blocker and independently verified positives

`installed-probe` exits **zero**, with confirmed cleanup. Its stdout contains two `[ERROR]` documentation messages about the `loss`/`logits` parameters of `Qwen3_5CausalLMOutputWithPast`, followed by the full one-line JSON receipt. The notebook's strict `json_stdout` reads the entire stream and raises `JSONDecodeError: Expecting value: line 1 column 2 (char 1)` at the initial `[ERROR]` text. Raw [stdout](../../notebooks/validation/m5-full-preparation-run-4/export/logs/installed-probe.stdout.txt), [stderr](../../notebooks/validation/m5-full-preparation-run-4/export/logs/installed-probe.stderr.txt) and [command receipt](../../notebooks/validation/m5-full-preparation-run-4/export/logs/installed-probe.json) are preserved.

Independent review decodes the separate final JSON line and verifies all 88 package versions, all 28 installed scientific module hashes, the venv executable/module origins, maintained `Qwen3_5ForCausalLM` import and Torch CUDA-build metadata 12.8. The [decoded receipt](../../notebooks/validation/m5-full-preparation-run-4/independently-decoded-probe.json) records those actual import/assertion positives. This review does not rewrite the original failed stage or claim the blocked checks executed. The messages concern documentation; no model was constructed and no language-weight/load/finite-output outcome is inferred.

Missing-`wrapt` startup warnings remain in stderr for some successful commands, including the probe. `create-venv` has empty stderr; stripping inherited Python environment variables did not eliminate every startup warning. The hook's file/traceback is still unavailable. No unreviewed dependency is added to conceal that warning.

## Artifact provenance and next repair

- Executed notebook: 114,657 bytes; SHA-256 `f00d8dbd5a647d84d7a158286f3731cd578fb3b97a85aefe075a1067a34bd313`.
- Results ZIP: 555,169 bytes, 56 safe unique members; SHA-256 `d3f4008055c8164737c30117f97b0969ad1e9ac2edc26c00d9da230ffc32e66e` matches the printed receipt.
- All six delivered v3 cell sources match after normalizing notebook source strings/lists. Execution counts are 2/3/4, without notebook error outputs. One additional empty unexecuted code cell is harmless and retained.
- Embedded helper/manifest/lock bind to operational build `635a76b14f8b2cbf2b00bd325debb99c97769565` and unchanged scientific baseline `ca46bcd55486b38bb453f5294e01f943bc7f7752`.

The narrow correction is a dedicated machine JSON file for the installed probe, with unchanged strict schema/version/module-hash checks and preserved stdout/stderr. Do not make a generic parser ignore arbitrary noise or weaken package/scientific acceptance.

The user confirms the same Kaggle session is still open. Prepare a continuation cell that reuses its admitted source/venv, rechecks installed provenance through the corrected output channel and runs the remaining 97 checks with existing bounded command/test/export helpers. No package download/install or scientific/model run is needed for this continuation. Its original failed report remains immutable; the new CPU diagnostics will be reviewed separately. K4/K8/K9 acceptance and T02 remain open until the remaining actual checks and later model gates pass. T01 remains done; progress remains 21 done/eight blocked.

The subsequent [implemented correction and validated continuation cell](m5-kaggle-probe-output-repair.md) are delivered and the user returned [actual run 5](m5-kaggle-full-preparation-run-5.md). All 97 CPU checks pass with zero skips and independently reopened exports, without repeating installation. No further CPU preflight is requested. The original run-4 failure above remains unchanged; GPU/model gates and T02 remain open.
