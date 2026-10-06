# M1–M4 CPU evidence and report acceptance

Authority: [specification](../../PROJECT_SPECIFICATION.md),
[repository contract](../../AGENTS.md), and
[plan coverage map](../IMPLEMENTATION_PLAN.md#9-coverage-map).
This is the evidence index for [M4-T06](../todos/M4/M4-T06-reproducible-report-and-cpu-gate.md).
It does not authorize compute or replace M5's hardware, capability, resource and
environment gates.

**CPU decision: pending final source, installed and original-worker reproduction checks.**

## Coverage map audit

Each row follows the existing plan, with no new requirement IDs. CPU checks are
separate from the explicitly pending inference and release portions.

| Specification / plan row | Named CPU implementation and evidence | Later portion |
|---|---|---|
| §1 design/estimands | [ScheduleTests](../../tests/test_schedules.py): `test_exact_memberships_no_unprescribed_crossings_and_fixed_opportunities`; [EstimandTests](../../tests/test_analysis.py): theta/retained-collaborator sign/null checks | M6 claims audit |
| §2.1 tasks/distributions | [Independent truth contracts](../../tests/test_truth_contracts.py), [tasks](../../tests/test_tasks.py), [edits](../../tests/test_edits.py); both declared sizes in [M1 gate](../todos/M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate) | No CPU gap |
| §2.2 sampling/reproducibility | [Populations](../../tests/test_populations.py), [saved manifest mutation checks](../../tests/test_schedule_manifests.py); [InformationRunTests](../../tests/test_information_run.py): `test_all_prefix_rounds_actual_exposure_history_counts_and_offline_strata` | M5 immutable freeze |
| §2.3 events/populations | [ScheduleTests](../../tests/test_schedules.py): exact memberships and poor-prefix independence; [EventBoundaryTests](../../tests/event_checks.py): `test_all_scheduled_events_subsets_and_repeats_start_from_original` | No CPU gap |
| §3.1 visibility | [Peer-view checks](../../tests/test_peer_views.py); [EventBoundaryTests](../../tests/event_checks.py): hidden before-values/endpoints/future edits and genuine disclosure-only receipt tests | No CPU gap |
| §3.2 protocol/rounds/caps | [Strict replies](../../tests/protocol_checks.py), [synchronous rounds](../../tests/round_checks.py), [native capacity](../../tests/tokenizer_capacity.py): `test_complete_bound_covers_adversarial_views_and_admits_both_sizes`; [M2 gate](../todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate) | M5 actual decoding and device memory |
| §4.1 retention/delivery | [EventBoundaryTests](../../tests/event_checks.py): equal B/C/K/mask evidence, C/F remote-only difference, wrong/invalid K and no backfill | No CPU gap |
| §4.2 complementary groups | [ReplayTests](../../tests/replay_checks.py): `test_both_masks_all_families_sizes_events_and_extra_replicate_parents`, branch-local assembly, equality and independent parent/sibling records | No CPU gap |
| §4.3 historical receipts | [EventBoundaryTests](../../tests/event_checks.py): `test_receipts_only_disclose_archived_before_field_and_never_forward_it`; [EstimandTests](../../tests/test_analysis.py): six-cell/direct-effect/eta and equal-benefit zero-interaction checks | No CPU gap |
| §4.4 prose delay | [ReplayTests](../../tests/replay_checks.py): round-two source/own-reply equality, no sentinel, chronological release and inactive treatments; [retained report activity](../../tests/fixtures/report_tables.json.gz) | No CPU gap |
| §5.1 exact outcomes | [ExactOutcomeTests](../../tests/test_evaluate.py): order/multiplicity, complete BFS keys, assigned segments; `OfflineRecordTests` distinguishes failures and unknown logical replays | No CPU gap |
| §§5.2–5.4 contrasts | [EstimandTests](../../tests/test_analysis.py): every retention/evidence/compact endpoint, group signs, receipts and Q companions; [four retained contrast scopes](../../tests/fixtures/estimand_tables.json.gz) | No CPU gap |
| §6 statistics/repeats/missingness | [StatisticalArithmeticTests](../../tests/test_uncertainty.py), `SharedMissingnessTests`, `ContrastUncertaintyTests`, `TrajectorySensitivityTests`; [sixteen uncertainty scopes](../../tests/fixtures/uncertainty_tables.json.gz) | M6 observed deviations/coverage |
| §7.1 repair/preservation/trajectories | [CoordinateOutcomeTests](../../tests/test_evaluate.py), `TrajectoryTests`, `DiagnosticAggregationTests`; [sixteen outcome scopes](../../tests/fixtures/exact_outcome_tables.json.gz) | No CPU gap |
| §7.2 information/work | [InformationCoreTests](../../tests/test_information.py): receipt censoring, association, tombstones, wrong-candidate residual identities and stated-view atlas; [six information scopes](../../tests/fixtures/information_tables.json.gz) | No CPU gap |
| §7.3 quality/cost/rule | [LedgerCostTests](../../tests/test_costs.py), `BoundaryRuleTests`, `WholePolicyTests`; [PolicyUncertaintyTests](../../tests/test_uncertainty.py): same eligible cost cohort and shared-cost cancellation | Actual GPU allocation/runtime remains M5/M6 |
| §7.4 narrative/cases | [CaseSelectionTests](../../tests/test_report.py), [ReportRunTests](../../tests/test_report_run.py), [ReportFigureTests](../../tests/test_report_figures.py), [sixteen reports](../../tests/fixtures/report_tables.json.gz) | Actual findings/claims remain M6 |
| §8.1 inference/controls | [ScheduleTests](../../tests/test_schedules.py): `test_controls_full_world_candidate_lengths_and_empty_send`; report shows original/revised capability controls without interpreting scripted success as capability | M5 language weights, state/RNG, finite outputs, devices and memory |
| §8.2 CPU/pilot/fallback | [M1](../todos/M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate), [M2](../todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate), [M3](../todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#completion-and-m3-gate), M4 evidence below; exact 24/90/1,114 bounds in schedules | M5 numerical smoke/capability/pilot thresholds |
| §§8.3–8.4 schedule/resources/freeze | [ScheduleTests](../../tests/test_schedules.py): independent complete main/development totals; [AccountingTests](../../tests/accounting_checks.py) and [LifecycleTests](../../tests/lifecycle_checks.py): stopped unknowns, safe budgets and original configuration resume | M5 measured complete-schedule forecast, allocation and freeze |
| §9 implementation/consistency/publication | Seven CPU check categories below; eleven actual controller kills in the [M3 ordinary bundle](../../tests/fixtures/scripted_lifecycle_run.zip); offline clean report reproduction | Accepted-host persistence and publication remain M5/M6 |
| §10 attribution/limits/exclusions | Report attributes prior work through the specification, states modified SILO scope and all excluded generality claims; all exhibits are synthetic validation | Verify precise source/version claims before M6 publication |

## Seven specification §9 check categories

| Category | Named acceptance checks and artifacts | CPU / later boundary |
|---|---|---|
| 1. Task truth | `ExactOutcomeTests.test_order_and_duplicate_multiplicity`, `test_bfs_full_dictionary_and_unreachable_node`; independent native/adversarial tests above; `CoordinateOutcomeTests.test_empty_D_empty_U_and_no_eligible_old_correct_coordinate` | Both sizes; source updates do not rewrite candidates |
| 2. Visibility | Hidden-field peer views; `EventBoundaryTests.test_unexposed_hidden_before_values_endpoints_and_future_edit_cannot_change_local_requests`, genuine receipt/lookup tests | Gold, hidden sources and future edits stay evaluator-side |
| 3. State interventions | `EventBoundaryTests.test_b_c_k_masks_have_identical_evidence_and_literal_retention`, C/F and K absence tests, `test_cpu_v1_v2_v3_authority_invalidation_preserves_derived_work` | v3 is a CPU authority test, not another live arm |
| 4. Synchrony/replay | `ReplayTests.test_request_native_tokens_settings_seeds_and_permitted_views_must_match`, branch-local assembly, round-two equality/no-leak/release; lifecycle Q commit kills | Exact raw replay includes invalid/failed outcomes |
| 5. Failure/restart | [AttemptLedgerTests / ProcessAttemptTests](../../tests/attempt_checks.py), [durable checks](../../tests/durable_checks.py), all nine lifecycle checks and original ordinary backups | Real CPU process kills; accepted host and actual provider still require M5 checks |
| 6. Analysis | [M4-T01](../todos/M4/M4-T01-exact-outcomes-and-trajectories.md#completion-and-handoff) through [M4-T05](../todos/M4/M4-T05-uncertainty-and-missingness.md#completion-and-handoff), all focused fixtures above; repeated reports/plots and exact case rule | Synthetic nulls/signs/cancellation/fragmentation; no empirical effect claims |
| 7. Accounting/capacity | `ScheduleTests.test_independent_main_component_tables_and_exact_generation_join`, exact development/capability counts, bounded attempts/idle allocation, [native witness](../../tests/tokenizer_attainability.py) and complete 261,388-token bound including reserve | CPU accounting/token capacity only. Actual T4 headroom, finite outputs and measured timings are **pending M5** |

## Reproduction and acceptance artifacts

The [original M3 bundle](../../tests/fixtures/scripted_lifecycle_run.zip) remains
authoritative. [report_archive.py](../../tests/report_archive.py) selects only its
evidence-named original workers. Every scope is analyzed and exported twice;
all M4 tables, selected IDs, plotting inputs and compressed/HTML/CSV bytes must
match. Original worker bytes must remain unchanged. No execution, inference or
plotting modules are imported by the data reproduction.

The [sixteen retained reports](../../tests/fixtures/report_tables.json.gz)
record fixed cases/settings, plotting data and export/link counts. The
[portable bundle](../../tests/fixtures/scripted_reports.zip) contains five
complete/incomplete/stopped reports and all 35 SVG/PNG exhibit pairs. Its
artifact check verifies links, table/plot/case joins and valid figure files.
Original-worker repeated reconstruction remains the source of these derived
exports. Named commands/results belong in
the [task evidence](../todos/M4/M4-T06-reproducible-report-and-cpu-gate.md#validation-and-evidence).

## Analysis assumptions ready for M5

Every exported `report.json` carries the case/annotation rules, source-association
rubric reference, explicit accounting clock, original generation settings and
bootstrap settings. The report includes 10,000 stratified world draws, saved
family seeds, type-7 quantiles, primary/descriptive probabilities, equal-family
denominators and complete-case labels. Exact shared-response sensitivity,
weighted Hoeffding companions, completion bounds and conditional repeats are
unchanged from M4-T05.

Cases require every scheduled slot in the supplied world scope recorded,
including failures, controls and scheduled repeats; selecting contrasts use
replicate zero. This affects illustration eligibility only. Strict sign medians
sort exact rational effects then immutable IDs; zero does not enter a sign.
Duplicate worlds merge their reasons, empty signs remain explicit, and the
all-zero fallback is deterministic. Excerpts use the earliest differing focal
peer/round; ties use the edited owner. A regression fallback additionally shows
the smallest-ID regressing continuation and its earliest regression. Raw strings
are unaltered; non-scalar Unicode uses reversible JSON string notation in HTML.
This display does not repair a reply or change its validation.

The seven grouped exhibits retain all supporting family/world tables, annotated
trajectories, raw contrasts, literal traces, inactive/unobserved Q treatments,
full-information controls, inventory/reference assumptions, physical/policy costs
and allocation/billing distinctions. Numeric occurrence is not source association;
unresolved is not absence. Cases and prose do not establish semantic causation.

## Remaining gates

[M5-T01](../todos/M5/M5-T01-inference-and-allocation-preparation.md) can become
ready when this CPU audit passes. It prepares a backend/allocation plan without
GPU use. Actual smoke, first 90 capability slots, complete pilot, measured
forecast and immutable accepted freeze remain separate M5 tasks and require
their specified evidence and execution authorization. M6 execution, empirical
claims and publication remain blocked. No GPU allocation, model loading,
inference, pilot, main experiment or accepted scientific/frozen-configuration
change is evidence for this CPU gate.
