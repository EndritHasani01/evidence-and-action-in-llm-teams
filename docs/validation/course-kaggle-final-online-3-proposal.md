# Kaggle final-online-3: diagnosis and complete fix proposal

Prepared 13 October 2026 on `feat/course-m5-inference-preparation`, inspected
HEAD `6247ee9`. **Proposal only:** no production repair, source-binding exception,
new notebook/package, scientific amendment or GPU execution is adopted here.
The investigation loaded no weights and made zero GPU calls. Scientific authority
remains [PROJECT_SPECIFICATION §11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime),
including the approved observational workflow and cumulative one-time 25-attempt
repair allowance. The submitted files are preserved unchanged.

## Recommendation

Repair two CPU-detectable defects before another GPU attempt: the full-envelope
request has an unsupported `system` field, and the forced-length generation
configuration unintentionally inherits the checkpoint EOS token. Extend the
existing preflight to construct the entire hardware plan and exercise the real
pinned generation configuration. Preserve controller tracebacks at the first
catch. Then support a narrowly audited continuation of this preparation bundle,
retaining its 21 recorded outcomes and running only the three unattempted
diagnostics. Keep the notebook as the existing Run All interface.

This can prevent the demonstrated software failures and detect similar boundary
errors before expensive work. It cannot promise that hardware, platform services
or model capability will always succeed. Those failures must produce a useful,
bounded, resumable or explicitly limited result with their evidence intact.

## 1. Evidence and actual execution

Primary artifacts are the [executed notebook](../../notebooks/run/final-online-3/notebook-exec.ipynb),
[original resume payload](../../notebooks/run/final-online-3/course-resume.payload),
[results export](../../notebooks/run/final-online-3/course-results.zip) and
[last action](../../notebooks/run/final-online-3/last-action.json). The
[machine-readable diagnosis](../../notebooks/validation/course-kaggle/final-online-3-diagnosis.json)
records all nine submitted file hashes, native facts, raw-reply revalidation,
request-constructor reproduction and disposable continuation checks. Its
[CPU diagnostic script](../../notebooks/validation/course-kaggle/diagnose_final_online_3.py)
reads the submissions and modifies only temporary database copies.

Both export archives pass CRC checks. All 72 archived source members match their
manifest bytes and SHA-256 values. The notebook's nine code cells match the prior
delivered notebook. The archived package identifies source commit
`075d10737c5f06a5a0de1122dac0e8236e8aac0a`; the current repository includes the later
delivery/evidence commit. CRLF-versus-LF differences from Git source are not
package corruption. Native installation was Python 3.13.15, Torch 2.11.0+cu128,
Transformers 5.12.0, Accelerate 1.14.0 and bitsandbytes 0.49.2.

| Stage | Observed result | What it establishes |
| --- | --- | --- |
| Online setup | Completed; dependency download ~199 s, install ~86 s, checkpoint download ~296 s | The pinned installation/checkpoint path worked in this session |
| Host checks | Three passed, zero skipped; 4.941 s | The affected host checks ran on Kaggle |
| Delivered loading-contract check | Passed; ~0.115 s | The previous optional-dispatch-metadata repair was exercised |
| Native replicas | Two distinct Tesla T4 UUIDs, 15,360 MiB each | Both GPU workers loaded the actual candidate |
| Ordinary hardware probes | 21 completed generations and 21 persisted attempts | Native short/long probe execution, fresh-state/load diagnostics and raw replies exist |
| Complete-envelope probes | 0 of 2 attempted | Full 109,851-input-token acceptance is still unknown |
| Controlled timeout | 0 of 1 attempted | This matrix's native cleanup diagnostic is still unknown |
| Hardware gate | `passed: false` | No hardware acceptance or pilot admission |
| Capability / pilot / freeze / main | Unexecuted | All 6,280 main logical uses remain unknown |

Cell 7 ran from 09:31:48.957 to 09:54:16.879 UTC, approximately 22 m 28 s
(11:31 to 11:54 Budapest time). There is no uncaught notebook-cell error:
the controller caught the failure and produced the limited report and exports.
Successful export or process exit therefore does not mean the research completed.

Both canonical worker databases pass SQLite integrity checks. Worker 0 holds
19 completed calls/attempts; worker 1 holds two. Their provider-process records
confirm process exit, and their observed allocation segments are closed. Segment
closure does not confirm Kaggle session deallocation or resolve missing prior
GPU-hour history. The recorded load facts show all audited tensors on `cuda:0`,
three attention checks per replica and legitimate `device_map: null`.

## 2. Confirmed immediate failure: incompatible request construction

The observed stop is:

```text
TypeError: RenderedRequest.__init__() got an unexpected keyword argument 'system'
```

[hardware_plan](../../scripts/m5_course_smoke.py) creates the two synthetic
full-envelope requests with this dictionary:

```python
rendered=dict(system="Hardware memory diagnostic; no scientific scoring", content=text)
```

[RenderedRequest](../../recovery/prompts.py) has exactly one field, `content`.
The controller later calls `RenderedRequest(**row["rendered"])`. The first
envelope row therefore fails before `prepare_control`, admission, model loading
or `begin_attempt`. The second envelope row has the same defect. Neither has a
call row or physical attempt in the submitted databases.

The CPU diagnosis reconstructed the plan with the exact archived native tokenizer:
all 24 rows equal `hardware/executed-plan.json`; precisely the two envelope rows
raise this error. Removing only their unsupported field in memory makes all 24
requests constructible. This is an adapter/schema defect, not an OOM, download
failure, inference timeout or scientific gate failure.

**Fix:** build the diagnostic dictionary with
`asdict(RenderedRequest(content=text))`. Keep the diagnostic label in the existing
row metadata. Preserve the native synthetic input IDs, all-one attention mask,
109,851 input tokens, 256-token reserve, original seeds, IDs, worker assignment and
fresh-process flags. This diagnostic intentionally supplies a synthetic tensor;
do not run its repeated-token text through the ordinary chat renderer and thereby
change the tested input envelope. Ordinary peer rendering remains unchanged.

## 3. Second defect: ineffective EOS suppression in the unexecuted path

[QwenBackend._generate](../../recovery/inference.py) currently sets:

```python
config.eos_token_id = None
config.min_new_tokens = config.max_new_tokens = 256
```

In the exact pinned Transformers 5.12.0 wheel, `_prepare_generation_config`
fills unset (`None`) configuration values from the model defaults. Its
`MinNewTokensLengthLogitsProcessor` masks EOS scores with `-inf` while fewer than
256 new tokens have been generated. The custom `_FiniteScores` processor runs
after that built-in processor and rejects any nonfinite score. Thus intentional
EOS masking can be mistaken for a model numerical failure.

This is **a verified configuration defect and a predicted next native failure**,
not an error observed in this submitted run: request construction prevented that
path from running. The CPU check used the real `GenerationConfig` implementation,
verified byte-identical to the hash-pinned wheel, and executed that wheel's actual
configuration-preparation function. With the checkpoint text-config EOS 248044,
`None` resolved to 248044; an explicit empty list remained `[]`. Both retained
`min_new_tokens == max_new_tokens == 256`. No model or Torch generation ran.

**Fix:** use explicit `eos_token_id=[]` for this forced-length hardware diagnostic
only. Verify the effective configuration, processor sequence and stopping
criteria in the pinned runtime, then require exactly 256 generated tokens and
256 finite-score observations in the native probes. Keep the finite check and
fresh cache checks. Do not sanitize NaNs, ignore arbitrary `-inf`, disable the
numerical audit globally or change ordinary peer EOS `[248044, 248046]`.

Generation options and their defaults are documented in the
[official Transformers generation reference](https://huggingface.co/docs/transformers/main_classes/text_generation).
The incident-specific behavior above comes from the exact wheel with SHA-256
`500be9eb644ede81c3103eee7687fc36d05dd75d1c76686c3820b26396fe7c7c`,
rather than an assumption about a newer documentation build.

## 4. Why verification missed these defects

The current envelope-plan test checks row counts, distinct IDs, worker positions
and token arithmetic; it never constructs `RenderedRequest` for those rows.
The envelope-generation test calls the backend directly with mock Transformers.
Its mock does not perform real default inheritance or EOS masking, and the test
currently asserts the incorrect `None` configuration. The delivered CPU notebook
exercise uses disabled GPU execution and consequently never traverses this
hardware controller path.

The previous verification covered its named loading, packaging, replay and export
checks, but it did not establish full hardware orchestration correctness. Both
new defects were detectable without a GPU. Broadly rerunning unchanged tests
would not close those particular gaps; testing the actual boundaries will.

## 5. Preserve the completed work and the authorized allowance

The cumulative count is **1 retained final-online-2 load failure + 21 new
completed attempts = 22 of 25**. Three slots remain:

1. `course-hardware/envelope/device-0`;
2. `course-hardware/envelope/device-1`;
3. `smoke/course-m5/24`, the controlled hang.

The Python error consumes no additional physical attempt. A fresh full matrix
would instead bring the incident to at least `1 + 21 + 24 = 46`; deleting the
old databases or resetting the counter would violate the approved allowance.
Do not reinterpret this preparation error as the permitted one infrastructure
retry or discard the invalid generated replies.

Using disposable copies of both saved databases, the diagnosis prepared the
corrected requests, obtained all 21 completed replies through `ProcessProvider`
with provider construction and admission forbidden, and registered only the
three missing requests. The completed call rows, including raw/validation JSON,
were identical before and after; saved `run_inputs.inputs_json` remained
byte-identical; zero new attempts were created. This establishes storage/request
compatibility, not permission to bypass source provenance.

Two wrapper barriers also need repair: cold bootstrap rejects this fatal report
before downloads, and Run All resumes only recognized interruptions/session
deadlines. The original source manifest rejects changed-source restores. Simply
adding every `TypeError` to a retry list or disabling source equality is unsafe.

**Recommended continuation:** introduce one explicitly reviewed, preparation-only
compatibility exception for this incident, within the original bundle and stable
call identities. Obtain explicit approval for that source-binding exception
before using it; the existing 25-attempt authorization already covers the count
and does not need to be requested again. The proposal does not adopt the exception.

Admission to this continuation must verify all of these concrete facts:

- The original archive/source/plan and both canonical worker databases are present
  and intact; no pilot/main run or accepted freeze exists.
- Exactly these 21 calls are completed, their raw replies/settings/seeds/permitted
  views/tokenized requests are unchanged, and the three identified diagnostics
  have no existing physical attempts. No active, blocked, failed or ambiguous
  additional attempt is hidden behind the reported preparation error.
- The reviewed source difference changes only diagnostic request construction,
  forced-length EOS handling, diagnostics/preflight and continuation control.
  Ordinary rendering, native model/runtime pins, sampling, protocol and input
  populations stay identical. Any broader difference refuses this exception.
- The original 075d107 source remains archived, the corrected execution source
  is archived separately using existing version/member metadata, and a repair
  receipt identifies which old records were reused and which new diagnostics
  used the correction. Never relabel the 21 old attempts as generated by new code.
- `budget.prior_smoke_attempts` remains one while the databases retain 21 attempts;
  do not set prior to 22 and count those same 21 again. Backups remain duplicates,
  not additional attempts. The applicable cumulative maximum remains 25.
- In a new session, repeat the required host checks and native pinned-environment
  verification; record the actual two T4 UUIDs and new observed interval. The
  three missing requests start fresh provider processes. Previous observation
  end is not evidence that Kaggle released the session.

This should be a small incident-specific check in the existing restore/bootstrap
paths, not a general migration service, second ledger, cross-bundle replay rule
or universal source-hash bypass. If the facts cannot be established, export the
limited result and make a separate scope decision rather than silently restarting.

## 6. Prevent similar failures at the actual integration boundary

Add a small plan-validation mode to the existing smoke command and invoke it
after pinned CPU dependencies/tokenizer are available, **before checkpoint
download or GPU provider construction**. Use the same planner and constructors
as execution. Verify all 24 rows, exact schemas/IDs/seeds/worker positions,
ordinary permitted rendering, two diagnostic token tensors/reserve/fresh-process
flags, and one controlled hang. The ordinary requests must equal their archived
inputs; synthetic diagnostics need their explicit diagnostic validation.

Add focused checks rather than a new testing framework:

| Check | Required evidence |
| --- | --- |
| Plan construction | Current failing packet reproduces the two constructor errors; corrected packet constructs all 24 requests with unchanged ordinary rows |
| Pinned generation configuration | Real `GenerationConfig` resolves diagnostic EOS to `[]`; ordinary EOS/settings are unchanged; min/max output remain 256 |
| Processor interaction | On a CPU environment with the pinned Torch/Transformers, exercise the actual built-in minimum-token and custom finite processors: ordinary finite scores stay finite without EOS masking in the diagnostic |
| Entire hardware controller | Run the real `execute_requests` loop using small scripted ordinary/envelope/hang providers; traverse both envelope transitions and the timeout, verify expected durable states and bounded cleanup |
| Failure/resume boundary | Inject the pre-attempt constructor failure after 21 completions; restore temporary copies, reuse all completed bytes, execute only the missing IDs, keep the prior attempt and refuse changed ordinary requests |
| Fatal refusal | Failed native attempts, changed pins/inputs, extra attempts, an accepted freeze or ambiguous active process refuse the preparation-only continuation before downloads |
| Delivered notebook/export | Execute the rebuilt notebook's literal CPU-safe cells with the actual two-file source package; restore/export the original incident fixture and verify read-only report reconstruction |

The real controller currently hardcodes its envelope provider and native timeout.
A narrow injectable provider/timeout seam for the scripted check is enough;
production remains the native factories and approved 120-second bound. Do not
replace the controller with a simulated implementation. Mock tests can still
check call ownership, but must not stand in for pinned library semantics.

## 7. Useful failure logs, progress and cleanup

The saved `logs/workflow-error.json` contains only the outer `BudgetStop` raised
by Run All, not the original constructor frame: `execute_requests` reduced that
exception to a string. Record the full original traceback at that first catch in
the existing hardware log/report. Include the phase, failing call ID, worker and
whether a durable attempt had started. Preserve the outer failure too. The earlier
full child trace repair does not cover parent-side preparation errors.

Keep the existing stage log and heartbeat, with progress derived from the
authoritative worker rows. Display ordinary `21/21`, envelope `0/2`, cleanup
`0/1`, cumulative attempts `22/25`, and the current call/device/input length.
Distinguish preparation errors, recorded native failures, failed scientific gates,
session interruption and limited export. A final line should say explicitly
whether hardware, pilot, main and analysis completed, and name the stop reason.
Budget-hour estimates remain observational; no removed hour gate is reintroduced.

The notebook contains `wrapt` sitecustomize warnings, but the affected commands
still pass. They are not this failure. Do not upgrade/unpin packages merely to
silence them; preserve stderr and keep stdlib-only setup isolated as already
implemented. It also reports leaked semaphore warnings. The exact leaked-object
origin is not established by this export. The current provider close path
terminates a living child even after a completed call, so reproduce that lifecycle
on Linux before deciding the smallest cleanup change.

The existing child protocol already accepts a stop sentinel. Prefer a bounded
graceful stop for an idle, completed provider, then fall back to the existing
TERM/KILL bounds. Hung/in-flight processes still require immediate bounded
termination; owner-death protection and the one-retry rule remain. Signal
termination can skip cleanup and leave tracked resources, as described by the
[Python 3.13 multiprocessing documentation](https://docs.python.org/3.13/library/multiprocessing.html).
Do not hide tracker warnings or extend a scientific call deadline for cleanup.

## 8. Independent model and runtime risks

All 21 raw replies were revalidated with the archived native tokenizer and the
existing course validator; every result matched the saved validation JSON:

| Outcome | Count | Interpretation |
| --- | --- | --- |
| Protocol-valid | 2 | Valid format, not proof of a correct task solution |
| Invalid JSON, stopped at 256 tokens | 12 | Verbose/truncated replies exhaust the output cap |
| Invalid candidate shape | 5 | Examples include sorting objects instead of the required integer array, or the wrong array length |
| Invalid message schema | 2 | Examples omit the required recipient field |

These stress witnesses are not the prescribed first-90 capability sample or
complete pilot; `2/21` must not be reported as the pilot validity estimate.
Nevertheless, they are substantial evidence that the current candidate may fail
the unchanged capability/98% validity gates. Invalid outcomes must stay invalid;
do not repair parsed JSON, retry answers for better outcomes, increase the 256
cap, constrain decoding without approval or selectively remove difficult worlds.

After hardware passes, run the original capability screen and full pilot under
the approved configuration. If those fail, produce the specified limited result.
An optional more compact instruction might improve length/schema adherence, but
it changes prompt bytes and requires a separate approved configuration decision,
new native capacity/request checks and the corresponding capability/pilot gates.
It is not part of the unchanged preparation continuation proposed above.

The largest completed inputs were 22,200 and 22,219 tokens, taking ~59.8 and
~59.3 seconds for 256-token replies. The observed minimum free memory was
~10.42 GiB and peak global device usage ~4.14 GiB **for executed short/long
probes only**. That does not establish headroom at 109,851 tokens. Both replicas
reported `recurrent_fast_path: false`. The full input is approximately 4.94 times
the largest observed input and must still fit within the approved 120-second
attempt including provider loading. A native timeout/OOM/nonfinite result remains
possible after these software repairs. Do not silently increase that deadline or
add/change native kernels and dependency pins to make acceptance pass.

A single-session finish is also unverified. Pilot (including its first 90) and
main contain 1,114 and 5,752 distinct physical generations, respectively. Even with both GPUs perfectly
busy, 6,866 calls inside a 10-hour controller window require a mean below
~10.49 seconds, before setup, hardware, export or analysis. For scale only,
a hypothetical 30-second mean implies ~28.6 hours on two GPUs; this is not a
measured pilot/main forecast. Use the existing measured pilot forecasts and
durable windows, display expected remaining work and resume across sessions when
needed. Do not invent provider quota/release or automatically allocate an external
session. An unattended Run All can finish its available window and export safely;
it cannot guarantee an entire study inside an unmeasured session duration.

## 9. Implementation and acceptance sequence

Keep this as one coherent repair workflow with a few reviewable commits:

1. Correct diagnostic request construction and explicit EOS suppression; update
   the failing tests and preserve original controller tracebacks.
2. Add the all-row preflight and scripted full-controller/resume checks, plus the
   real pinned configuration/processor checks. Run them before packaging.
3. Prepare the narrow original-bundle continuation and its source-difference
   receipt for explicit review. Preserve the originals and the 22 cumulative
   attempts. No attempt-limit increase is proposed.
4. Rebuild the existing lightweight notebook and two-file dataset. Verify literal
   CPU-safe notebook integration, progress, limited exports and exact restoration.
   Keep pinned online checkpoint/dependency downloads and integrity checks.
5. On the authorized native T4×2 session, after the source-continuation decision,
   run **only the three missing diagnostics**. Reuse the 21 saved calls. Assert
   two full 109,851 + 256 probes, finite/cache/load evidence, at least 1.5 GiB
   observed free headroom and bounded controlled-timeout cleanup. Any failed
   recorded attempt consumes its slot and yields the accurate limited result;
   there is no automatic extra retry allowance.
6. Only with accepted hardware continue the original first-90 capability screen,
   complete pilot, required raw/effect audit and conditional unchanged freeze/main.
   Preserve outcome-independent populations, seeds, replay, failures and unknowns.
   Export the results and resume payload, then reproduce analysis from those
   records independently. Main remains unexecuted until those gates pass.

The completed investigation provides the concrete incident evidence and CPU
reproductions for steps 1–3. It does not claim that the proposed repairs, source
continuation, native full-envelope acceptance or final experiments have run.

## Reproducing this diagnosis

Run against inspected HEAD `6247ee9` with the local CPU project environment:

```powershell
.venv/Scripts/python.exe notebooks/validation/course-kaggle/diagnose_final_online_3.py
```

For the additional exact-wheel configuration proof, provide the original verified
Transformers wheel (the investigation used the existing local asset cache):

```powershell
.venv/Scripts/python.exe notebooks/validation/course-kaggle/diagnose_final_online_3.py --transformers-wheel E:/CourseKaggleDelivery/assets-cache/wheels/transformers-5.12.0-py3-none-any.whl
```

This is an incident diagnostic, not a regression test to run unchanged after the
planner repair: it intentionally proves the old two-row failure. It needs no
weights, provider or GPU and leaves all submitted files untouched. The checked-in
JSON receipt records the executed optional-wheel investigation as well as the
base diagnosis.
