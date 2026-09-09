# P4 unit registry v1 authority convergence W1 — handoff

## Status

- `IMPLEMENTED_PENDING_REVIEW`
- This closes neither P4 nor P5, V1 membership/readiness, release, activation, nor Human PASS.

## Authority and fixed lineage

- Internal live CURRENT: `v25.35.0`, `RD-001~490`
  - `docs/ssot/CURRENT.md`: 656 bytes, SHA-256 `d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa`
  - `docs/ssot/ssot/CURRENT.md`: 957 bytes, SHA-256 `a9bd37606dab7c25be5af527db93c4eb8c9e0cd6f1b54988b4211e67190c8ad4`
  - `SSOT_INDEX_v25.35.0.md`: 130,630 bytes, SHA-256 `911f87fb4516b5c8db342f5180b3e6facbc76292fc44f3ec15c39f148eab7cd6`
- Public Language SPEC: `v0.6.0`; `publish/spec/CURRENT.md` 2,758 bytes, SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`
- Baseline / direct parent: `c84b6d83d123c335bc23a8b5165e82dce5e70d4c`
- Product/test fixed HEAD: `d008bd4d8905c5834f4b68904cb0e50b8d9cb166`
- Product/test fixed tree: `f86bbac08175a1c1771d060e90f5781c01aa8368`
- Merge count in fixed commit: 0

## User workflow and release blocker

`ddn.units.json` was consumed by two official product paths with incompatible version authorities:

- Gate0 runtime registry required `v1`.
- schema construction required `v0` and silently deduplicated entries.

This made one checked-in project registry invalid for one of the two official consumers. The fixed product now uses the Gate0 loader as the single parser/validator for both runtime and schema construction. The checked-in registry version is `v1`; its 27 unit symbols and order are unchanged.

## Exact product diff

- `ddn.units.json`
  - version only: `v0` -> `v1`
  - unit membership/order: unchanged, 27/27
- `tool/src/gate0_registry.rs`
  - exposes one crate-local `v1` registry loader
  - preserves duplicate and unknown-unit fail-closed validation
  - runtime registration consumes the shared loader
  - adds one product-contract unit test in the existing test module
- `tool/src/schema.rs`
  - removes its private `UnitsRegistry` parser and `v0` authority
  - consumes the shared loader while preserving schema diagnostic prefixes

Product diff outside those three paths: 0. Tracked WASM/UI/SSOT/SPEC/public spelling/membership diff: 0.

## RED -> GREEN and regression

External build output: `I:/home/urihanl/ddn/codex/build/test-targets/ddn-v1-p4-gb-c84b6d83`.

1. RED, baseline defect reproduced in the existing Rust test module:
   - exact test count: 1
   - `checked_in_unit_registry_matches_v1_runtime_contract`
   - failure: `left Some("v0")`, `right Some("v1")`
   - exit: 1
2. GREEN after the product correction:
   - same exact test: 1/1 PASS
3. Full proportional regression:
   - `cargo test -p ddonirang-tool --lib`
   - 527/527 PASS
4. `git diff --check`: PASS

No new pack, runner, checker, mutation harness, or meta-test was created. The actual baseline contradiction is the risk-relevant RED.

## Environment boundary

An attempted official `build-schema` CLI invocation did not reach schema construction because this isolated product worktree lacks the legacy `docs/ssot/SSOT_MASTER_v20.12.0.md` preflight file. The command also returned exit 0 after printing that pre-existing error. Neither behavior is claimed as fixed or as evidence for this slice. The shared loader and schema consumer were compiled and covered by the 527-test library regression.

## Review request

Bundle this product correction with the next coherent P4/P5 product milestone for the single rolling independent reviewer. Do not create a new reviewer or worktree for this slice alone.

Review focus:

- one loader is the only `ddn.units.json` semantic validator in `tool`;
- runtime and schema accept the same checked-in `v1` registry;
- duplicate/unknown-unit failure remains fail-closed;
- 27 symbols and public spellings are unchanged;
- no product/SSOT/SPEC/membership/release transition outside the fixed scope.

## Anti-meta checkpoint

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: one checked-in unit registry can now be consumed consistently by runtime and schema product paths.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 527 full tool-library tests, including the one newly added product-contract case in the existing module.
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: stopped after the product RED, shared-authority correction, exact GREEN, and proportional regression.
- `NEXT_PRODUCT_DECISION_ENABLED`: P4/P5 can treat unit-registry version/validation as one product authority, subject to bundled independent review.

## Nonclaims and open gates

- Independent PASS: OPEN.
- Whole P4/P5 closure: OPEN.
- Windows x64 RC/public release/distribution: OPEN.
- V1 membership/readiness/activation/Human PASS: OPEN.
- The pre-existing legacy SSOT preflight and CLI exit-code behavior remain outside this slice.
