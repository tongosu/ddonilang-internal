# DDN Chaebi Hardcut Wave 5/6 Final Handoff

## Fixed product target

- Product target: `303b411c53db71d3f5aff482198363eb238ecb5f`
- Product tree: `e6e04188345b1a6e81c2d19a4ac655568a7a222e`
- Product parent: `6c85d8404a7ed37fce0100410030c32cfad299e9`
- Authority input: internal SSOT v25.63.0 / RD-001~583; public Language SPEC v0.6.0.

No Wave 5 or Wave 6 product change was required. This handoff is a docs-only
direct successor; it does not amend or otherwise rewrite the fixed product
target.

## Wave 5 current-frontdoor result

`ALREADY_ZERO_ON_303B411C` for the current V25 execution paths:

- the three native names share `tool/src/bin/ddonirang.rs`; it has no teul-cli
  command path and no argv0 semantic branch;
- the shared native/WASM execution path takes the explicit `v1-core-v25`
  profile and reaches the strict V25 parser guard;
- `ui/runtime/runtime_bridge.js` delegates `runSummaryWithSourceProfile` to
  `wasm_run_summary_with_source_profile_json`; Workbench passes its explicit
  source-profile identity to that bridge;
- Seamgrim `/api/run` writes raw input then calls `run_ddonilang`, whose
  resolver permits only a precise `DDONILANG_BIN` override or `ddonilang`;
  it has no teul resolver, retry, or source lowering path.

`export_graph.py` retains teul functions only for its separated historical
maegim/graph adapter custody. They are not selected by the official `/api/run`
call path. Existing `workbench.js` legacy examples and presentation-only
maegim controls are not V25 execution fallbacks: the current Workbench path
passes raw source to the shared profile-aware WASM operation, where legacy
`채비 {}` is rejected before runtime state or success publication.

## Wave 6 active-fixture classification

The official `pack/v1_core_supported_ingress_w1/manifest.detjson` consumes
seven cases. None contains `채비 {}`.

| Cases | Classification |
| --- | --- |
| `VC01_VC02_VC03_POSITIVE`, `VC12_LANGUAGE_CORE_COLLECTION` | `CURRENT_POSITIVE_DIRECT_DEFINITION` |
| `VC18_LEGACY_DEFINITION` | `LEGACY_NEGATIVE_MIGRATION_REQUIRED` |
| `VC13_STRICT_SELECTION_OUT_OF_RANGE`, `VC04_VALUE_TYPE_MISMATCH`, `VD01_DIRECT_RECURSION`, `VD01_MUTUAL_RECURSION` | `HISTORICAL_NOT_CURRENT` for this Chaebi hardcut |

No active fixture required a semantic rewrite. Historical/deferred packs and
`tools/teul-cli/**` remain untouched.

## Verification

- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`: PASS; raw
  Workbench WASM call sites remain zero and the shared bridge preserves payload,
  diagnostic, and state identity.
- `node tests/run_v1_core_supported_ingress_wasm_parity_w1.mjs`: PASS;
  11 cases, five deterministic repeats, partial summary 0.
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- `git diff --check`: PASS before this handoff.
- Existing `tests/run_seamgrim_export_graph_preprocess_check.py` could not be
  used as a current-frontdoor gate because its historical fixture
  `build/meta_fallback_fixture.ddn` is absent. This is recorded as historical
  test-input custody, not as a product fallback or a product regression.

The dedicated Cargo target was used for dispatched native checks. Its tool
build/test output could not be recovered after the terminal transport ended;
the final independent reviewer must rerun the native three-name positive and
legacy-negative commands at the fixed target rather than infer them from this
handoff.

## Bound result and nonclaims

- `CURRENT_STRICT_PARSE_CHAEBI=REJECT`
- `TRACK_B_CURRENT_REACHABILITY=0`
- `TEUL_CURRENT_FALLBACK=0`
- `CHAEBI_PREPROCESS_FALLBACK=0`
- `AUTO_CONVERSION_COUNT=0`
- `PARTIAL_PUBLICATION_ON_REJECT=0` for the checked parser/runtime/WASM paths
- `HISTORICAL_CUSTODY_PRESERVED=YES`

This prepares exactly `303b411c` for one final fixed-target independent review.
It does not claim P0-P6 closure, V1 readiness or release, teul physical
deletion, public-SPEC promotion, or Human PASS.
