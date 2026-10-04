# Repository operating contract

## Authority and navigation

- [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) is the sole scientific authority.
  It governs the experiment, evaluation, execution constraints, and claims.
- [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) is the engineering roadmap.
  Follow its gates and update its living sections for meaningful progress or discoveries.
- [docs/implementation-research/](docs/implementation-research/) supplies technical evidence,
  not additional requirements. Start with its synthesis and read relevant investigations selectively.
- [research/](research/) is historical/supporting material. For work there, follow
  [research/AGENTS.md](research/AGENTS.md); its archive-specific rules remain in scope.
- [README.md](README.md) provides orientation. Inspect current files and relevant specification/plan
  sections before work; do not treat archived plans or status statements as verified current behavior.
- `acl26-silo-bench/` supplies reference source/data, not authoritative execution or scoring semantics.
- When documents conflict, follow the specification; surface scientific ambiguity rather than
  silently changing the design. Record consequential engineering decisions in the existing plan.

## Simplicity is a project rule

- Before adding architecture, metadata, persistence, identities, abstractions, or dependencies,
  identify the specification/plan requirement or demonstrated failure mode that needs them.
- Prefer the simplest explicit solution preserving scientific correctness, reproducibility,
  restart safety, and traceability. Generality, elegance, or speculative robustness is insufficient.
- Use existing stable IDs, persisted records, configuration and version information before adding
  custom hashes/checksums, content-addressed identity, or another identity/provenance system.
- Keep a small number of clear sources of truth. Derive progress, exports, analysis tables and
  reports from them; avoid duplicate stores, competing authoritative records, or extra persistence layers.
- Avoid production-style coordination, handoff/transfer services, and operational machinery unless
  a current requirement or observed failure demands them.
- Do not add generic frameworks, factories, registries, service/repository layers, extension points,
  or infrastructure for hypothetical future requirements. Retain complexity genuinely required by the experiment.

## Critical scientific invariants

- Keep evaluator truth, hidden sources, future edits and condition metadata out of peer views.
  Current source authority and retained derived work are distinct; never repair model answers for peers.
- Preserve isolated sibling starts, literal retention transformations, synchronous visibility,
  and the specified source/prose delivery boundaries. No hidden model state may cross calls.
- Required replay uses exact persisted replies, including invalid outcomes, with the prescribed
  equality checks and branch-local effects. Matching seeds or framework replay is not a substitute.
- Persist replies before effects; resume completed calls without resampling. Preserve idempotent
  delivery, bounded retries and failures. Failed slots never inherit earlier candidates;
  recorded failures and unexecuted slots remain distinct.
- Preserve declared populations, comparisons, analysis units and missingness rules. Never select
  worlds or stop branches for favorable outcomes. Keep physical attempts and logical policy costs distinct.

## Autonomy and authorization

- Within the requested task, inspect, edit, run deterministic tests, and perform relevant refactoring
  without confirmation. Resolve ordinary implementation choices within the scientific contract.
- Require explicit authorization before expensive GPU runs, any main experiment execution, paid compute,
  scientific-design changes, frozen-configuration changes, publication, destructive remote operations,
  or deletion of important experiment artifacts.
- Honor existing explicit authorization within its scope; do not repeatedly request it.
  Passing a gate is not authorization, and authorization does not waive scientific or resource gates.
- Before requesting authorization, complete safe preparation and explain the concrete action,
  expected cost/scope, and affected configuration or artifacts. Continue independent authorized work.

## Proportional verification and evidence

- Match verification to the change. Documentation edits need consistency/link checks, not GPU runs.
  Behavioral changes need focused deterministic checks for the affected scientific failure modes.
- Verify library behavior where isolation, replacement, replay, persistence or analysis depends on it.
  Successful model outputs do not substitute for protocol tests; retain the plan's execution gates.
- Distinguish **implemented** (code exists), **verified** (named checks actually passed),
  **pilot-tested** (bounded capability/runtime evidence), and **empirically executed**
  (recorded experiment outcomes with coverage). State the relevant environment and limits.
- Link claims to executed artifacts. Plans, forecasts, historical probes and partial runs are not
  completed experimental results; report missing work, failures and uncertainty explicitly.
