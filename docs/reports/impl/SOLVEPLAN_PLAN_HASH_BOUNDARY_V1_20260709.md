# SOLVEPLAN_PLAN_HASH_BOUNDARY_V1_20260709

generated_at: 2026-07-09

## Scope

Declarative Closure Run3A G11 records the boundary between SolvePlan
`state_hash_inputs`, future `plan_hash`, and the runtime `state_hash` formula.

This report is `닫힘-문서` only. It adds no parser/runtime behavior and changes no
hash formula.

## Decision

- `state_hash_inputs: manifest field only`.
- `actual state_hash formula change: false`.
- `plan_hash canonical bytes: pending`.
- `plan_hash emission: forbidden until canonical-byte decision`.
- `state_hash_inputs` documents candidate definition inputs for a future
  `plan_hash`; it is not a runtime `state_hash` integration.

## Current Artifact Evidence

| Evidence | File:line |
|---|---|
| V2 proposal approves the minimum SolvePlan artifact field set including `state_hash_inputs` | `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md:99` |
| V2 proposal keeps `state_hash_inputs` as a manifest field and defers actual `state_hash` integration | `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md:101` |
| V2 proposal summary keeps `state_hash_inputs` as a manifest field | `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md:193` |
| S0 SolvePlan fixture has `state_hash_inputs` | `pack/lang_seum_algebraic_v1/expected_solveplan_s0.detjson:52` |
| Connect lowering SolvePlan fixture has `state_hash_inputs` | `pack/lang_connect_lowering_v1/expected_solveplan_connect.detjson:47` |
| InitPlan SolvePlan fixture has `state_hash_inputs` | `pack/sim_init_equation_v1/expected_init_s0.detjson:55` |
| Experiment manifest keeps `state_hash_inputs_manifest_field_only=true` | `pack/sim_experiment_manifest_v1/experiment_manifest.detjson:55` |
| Experiment manifest keeps `plan_hash_status=pending_canonical_bytes_decision` | `pack/sim_experiment_manifest_v1/experiment_manifest.detjson:57` |

## Current Include Set

The current emitted `state_hash_inputs.include` set is:

- `schema`
- `source_hash`
- `stage`
- `method`
- `relations`
- `unknowns`
- `lowering`

These are definition-side candidates for future `plan_hash` canonical bytes.
They are not runtime `state_hash` inputs in this batch.

## Current Exclude Set

The current emitted `state_hash_inputs.exclude` set is:

- `diagnostics`
- `execution_results`

These remain excluded from future definition hashing unless a separate proposal
changes the boundary.

## Additional Include Candidates Requiring Decision

The following fields are candidate inputs but not part of the current emitted
include set:

- `init_plan`: needed if t=0 initialization assertions become part of canonical
  plan bytes.
- `lowering.connect_desugar.surface`: already nested under `lowering`, but the
  canonical byte rule must decide whether source spelling, normalized rows, or
  both are authoritative.
- `run_config_hash`: belongs to experiment manifest replay identity, not
  SolvePlan definition identity, unless a future decision says otherwise.
- `unit_normalization`: G5 currently checks unit behavior without injecting new
  SolvePlan `state_hash_inputs`.

## Exclude Candidates

The following must stay out of `plan_hash` and runtime `state_hash` unless a
separate decision explicitly reverses this:

- diagnostics and warning text.
- execution results, output bytes, stdout/stderr, local build paths.
- wall-clock time, benchmark measurements, host I/O, network state.
- checker names and CI profile names.

## Blockers Before `plan_hash`

Before any `plan_hash` field is emitted or any runtime `state_hash` formula is
changed, the project needs a separate canonical-byte decision covering:

- JSON/detjson canonical serialization and field ordering.
- UTF-8 normalization and line ending policy.
- source hash scope: raw file bytes vs normalized source text.
- list ordering for relations, unknowns, diagnostics, and lowering rows.
- versioning and migration behavior for `ddn.solveplan.v1`.
- whether `init_plan` is included, and if yes where it is positioned.
- whether unit normalization is represented in SolvePlan definition bytes.

## Verification

- `python tests/run_declarative_closure_g11_plan_hash_boundary_check.py`
- `git status --short -- docs/ssot` PASS expected.
