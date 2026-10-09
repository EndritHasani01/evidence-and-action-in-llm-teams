# Course M2 protocol and limits evidence

Prepared 9 October 2026 on Windows/PowerShell, CPython 3.11.9, from baseline
`58890ad` on `feat/course-m1-contract-and-inputs`. Follow the
[task](../todos/course/M2/M2-T01-course-protocol-and-limits.md),
[course handoff](../planning/course-study-session-handoff.md),
[passed M1 inputs/schedules](course-m1-inputs-and-schedules.md) and
[scientific authority](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime).
This is CPU protocol verification. No pretrained model, GPU, pilot, main
experiment, accepted freeze or publication was executed.

## Implementation and reuse

The existing [renderer](../../recovery/prompts.py) now owns immutable
`THESIS_LIMITS` and `COURSE_LIMITS`. Only the adopted pairs 384/128 and 256/64 are
accepted; both retain total context 262,144, three recipients, eight distinct
current references per recipient and 32 feedback tokens. No arbitrary smaller
input window, new dependency, runtime fork, identity system or store was added.
The [input-only TOML](../../configs/course-inputs.toml) stays unchanged and does
not freeze runtime settings. Explicit course rendering requires fallback size.

`render_request(view, limits=COURSE_LIMITS)`, `tokenize_request(...,
limits=COURSE_LIMITS)` and [strict validation](../../recovery/protocol.py) use
the same value. Only the two cap numbers change in the generic instruction;
public data, task hints, assignments and literal layout remain identical.
Current sources render once; pending replacements lack payload, known tombstones
remain deleted and genuine historical receipts carry only their archived
before-value. Neither that value nor stale/unheld versions can be forwarded.
No policy/branch/mask/scope/outcome labels enter the permitted view.

The existing length-delimited history blocks and fixed footer preserve raw
special-looking strings, fake delimiters, controls and trailing whitespace.
Unpaired synthetic audit strings retain the labeled JSON-string fallback.
Decoded message text must contain Unicode scalars: escaped valid surrogate
pairs are accepted; unpaired surrogates reject the entire reply before native
prose counting. The native NFC normalizer remains a tokenizer operation, with
exact rendered text and native template text/IDs separately retained.

The strict complete-document decoder, nested Pydantic schemas and sender-view
permission checks are reused. Duplicate keys, nonfinite numbers/overflow,
coercions, booleans, wrong shapes, extra fields, fragments and fences remain
invalid. Repeated held references count toward distinct references and preserve
every delivery attempt. Wrong integer answers remain protocol-valid. Any invalid
message discards the candidate and all sends; invalid/failed slots inherit no
answer, and unexecuted slots remain unknown. Feedback uses only existing public
codes at the next scheduled opportunity.

[Exact candidate settings](../../recovery/inference.py) accept explicit course
limits with the pinned 4B candidate and record all six values in the existing
settings JSON. `limits_from_settings` rejects a 256 generation cap without
explicit course limits and rejects contradictory caps. Original thesis settings
omit the new field and retain their exact contents for both reviewed models and
attention choices. The existing
round/replay/runner/store paths derive course limits from those saved settings,
including controls, request equality, reopen and parent revalidation. Generation
and suffix decoding use 256; complete JSON at the cap remains valid. There is
no repair, constrained decoding, extra call or closing-brace stop.

Validation record shapes remain unchanged for archive/replay compatibility.
Course token audits call `output_fits(COURSE_LIMITS)` and
`prose_fits(COURSE_LIMITS)`; the original `output_within_limit` and
`prose_within_limit` properties remain thesis compatibility shorthands. The
existing exact settings record owns the applied limits, rather than duplicating
them in every reply or adding a persistence layer.

## Executed verification

| Check | Environment | Result |
|---|---|---|
| Prerequisite renderer/parser/inference and course M1 checks | Repository `.venv`; Pydantic 2.13.5, LangGraph 1.2.12, SQLite saver 3.1.1 | 80 passed |
| Dependency-free course limits/rendering | `python -S`, site packages disabled | 6 passed |
| Course strict boundaries and exact settings integration | `.venv`; synthetic token counts and CPU adapter doubles | 12 strict + 6 settings checks passed |
| Affected course/thesis integrated protocol, rounds, replay, durability and inference regression | `.venv` | 110 passed, zero skips |
| Pinned 4B native tokenizer, fresh hash seed 37 | Global CPU tokenizer environment | 9 passed, zero skips |
| Installed package outside checkout, no source `PYTHONPATH` | `.venv` interpreter; all 29 module bytes match `229684c` | 81 passed, zero skips |
| Installed course checks with hash seed 37 | Same isolated installed package | 24 passed, zero skips |
| Dependency-free complete core discovery | `python -S`, site packages disabled | 348 checks: 340 passed, eight expected optional-library skips |
| Complete lifecycle rerun after validation-spy fix | `.venv`; real externally killed scripted controllers | 9 passed, zero skips; includes all four previously failing subcases |
| Dependency consistency | `.venv` | `pip check` passed |

The complete source CPU command reached all 558 checks. Its only failures were
four kill-point subcases in two lifecycle tests: an existing validation spy did
not forward the new `limits` keyword. All 549 non-lifecycle checks passed, as
did seven lifecycle methods. The spy now accepts and forwards the keyword;
all original pause, kill, restart and checkpoint assertions remain intact.
The complete nine-method lifecycle rerun passes all four previously failing
subcases and every original lifecycle check. Together the commands cover all
558 source CPU checks with passing evidence after this instrumentation fix.
The 37-minute full command was not repeated: production modules and the 549
unaffected checks have not changed since that run or installed verification.

The [checkpoint audit](../../notebooks/validation/course-m2-protocol/checkpoint-audit.json)
passes 604 local references and 269 fragments, verifies all 21 course statuses,
and confirms 1,167 protected files are byte-identical at that checkpoint.
These include original thesis todos/defaults/fixtures, the adopted specification,
course input/schedule fixtures and the user's pre-existing M5 evidence edit.
Original plan Sections 1-10 and both models' baseline/opt-in exact settings remain
unchanged. The [completion audit](../../notebooks/validation/course-m2-protocol/completion-audit.json)
passes the handoff counts and links, verifies
the exact four failing full-run subcases and the passing lifecycle rerun, and
checks 1,166 protected starting files. The one-file count reduction permits only
the three-line lifecycle-spy correction, whose exact baseline comparison is
checked separately. The user's M5 edit remains byte-identical and unstaged.

The native environment is Transformers 5.12.0, Tokenizers 0.22.2, Jinja2 3.1.6,
Hugging Face Hub 1.19.0 and Pydantic 2.12.5. All four local metadata files match
the pinned 4B revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` in a fresh
upstream byte comparison; the [environment record](../../notebooks/validation/course-m2-protocol/native-environment.json)
retains exact URLs, sizes and SHA-256 values. No model weights were downloaded
or loaded for these checks.

[course_protocol.json.gz](../../tests/fixtures/course_protocol.json.gz) retains
eleven permitted rendered/native cases, 23 exact reply/validation cases and
225 candidate/one-shard cases covering all 20 main/five development worlds and
every peer/full-information shape. The candidate/one-shard cases use at most
132 generated tokens; feedback uses at most 14 native tokens. Separate physical
256/257 and aggregate prose 64/65 cases establish cap boundaries. The final
native token contains the completing brace at 256. Nine repeated delivery
attempts with eight distinct references pass; nine distinct references fail.
Both original thesis request/reply archives reproduce exactly with the 4B
tokenizer after canonical JSON comparison.

These are finite protocol fixtures and useful-channel checks. They establish
no complete retained-context bound or local attainability witness. Those remain
[course/M2-T03](../todos/course/M2/M2-T03-course-attainability-and-capacity.md).

## Commands and retained failures

Exact argument arrays, working directories, exit codes and raw logs are retained
in [course-m2-protocol](../../notebooks/validation/course-m2-protocol/).
The installed provenance identifies the actual package path and all module
bytes; its tests ran outside the source checkout with source `PYTHONPATH` absent.

```powershell
.venv/Scripts/python.exe -m unittest tests.test_course_limits tests.course_protocol_checks tests.course_settings_checks tests.inference_checks tests.test_inference_preparation tests.round_checks tests.replay_checks tests.durable_checks -v
python -m tests.tokenizer_course_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/4B"
.venv/Scripts/python.exe -m recovery validate --regime course --config configs/course-inputs.toml --manifest tests/fixtures/population_course.json --schedule tests/fixtures/schedules_course.json --authoritative tests/fixtures/population_course.json
python -S -m recovery validate --core-only --regime course --config configs/course-inputs.toml --manifest tests/fixtures/population_course.json --schedule tests/fixtures/schedules_course.json --authoritative tests/fixtures/population_course.json
.venv/Scripts/python.exe -m unittest tests.lifecycle_checks -v
.venv/Scripts/python.exe -m pip check
python -S -X utf8 notebooks/validation/course-m2-protocol/verify_protocol.py --completion --output notebooks/validation/course-m2-protocol/completion-audit.json
git diff --check
```

The initial global baseline could not import the SQLite saver; integrated checks
therefore use the existing complete `.venv`. The first non-isolated package
build lacked `bdist_wheel`; the passing build uses isolated tooling without
changing project dependencies or upgrading the runtime environment. An initially
missed durable equality reconstruction used thesis limits; the failing checkpoint
and passing correction are retained. Initial native test assertions confused
JSON lists with tuples and required the final token to contain only a brace;
the corrected checks compare canonical structures and require the completing
brace in the last token. The original barrier and external-kill validation spies
now forward the limits keyword while preserving every synchrony and kill-point
assertion. The full failing log is retained rather than relabeled as a passing
single-command run. Its original bytes are stored in
[full-validation.txt.gz](../../notebooks/validation/course-m2-protocol/full-validation.txt.gz)
so raw unittest trailing whitespace stays lossless while `git diff --check`
passes. The initial build failure is retained similarly.

## Completion and handoff

Course/M2-T01 is done: explicit course rendering, validation, reservation and
exact settings are implemented and CPU/native verified, with original thesis
semantics/defaults preserved. [Course/M2-T02](../todos/course/M2/M2-T02-course-interventions-and-replay.md)
is ready to renew the course intervention/retention/replay matrix using these
real interfaces. Course interventions/replay acceptance, the complete
witness/capacity gate,
worker/accounting and analysis adaptation, actual hardware/model memory and
capability, resource reconciliation, pilot, freeze, empirical execution and
external delivery remain separate tasks and gates. Original thesis todos,
defaults and experiment artifacts retain their separate obligations.
