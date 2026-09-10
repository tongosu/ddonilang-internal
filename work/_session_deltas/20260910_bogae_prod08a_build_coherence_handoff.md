# BOGAE-PROD08A build-coherence handoff

## Claim and immutable target

- Claim: the official WASM build entrypoint resolves the bindgen input from
  the same `CARGO_TARGET_DIR` used by Cargo, preventing an isolated build from
  binding an old worktree `target/` artifact.
- Product: `7e538ab5b1ca02433cfcbc454b369e3dc247c65a`
- Tree: `595221c5387c0fb3d3442af494540ca2015730e8`
- Parent: `4fe5f1c5119bb5bf7955991e683aeecb351ae130`
- Changed product paths:
  - `scripts/build_wasm_tool.ps1`
  - `tests/run_ddn_cli_wasm_freshness_check.py`

## Primary evidence

- Native: `cargo check -p ddonirang-tool --lib --offline`, with
  `CARGO_TARGET_DIR=I:/home/urihanl/ddn/codex/build/target-bogae-prod08`: PASS.
- WASM: the official `scripts/build_wasm_tool.ps1` entrypoint completed with
  the same isolated target; its compiled input was observed at
  `target-bogae-prod08/wasm32-unknown-unknown/release/ddonirang_tool.wasm`.
- Fresh isolated manifest write/validation: PASS.
- Focused tool test target listing: `644 tests, 0 benchmarks`, exit 0.
- `git diff --check`: PASS before fixed commit.

## Mutation and exact restore

- M-A1 removed `$cargoTargetRoot` and restored the old worktree target lookup.
  The existing freshness gate was RED with `WASM build input must resolve from
  CARGO_TARGET_DIR when configured`; restoration was GREEN. Restored build
  script SHA-256: `78248B7308E59FF30A2C1A2A7555F521563207A1EC7A992B87C98A7D58B402E9`;
  blob `03c324c7cce08581df5b48798e96a1eaac89b595`.
- M-A2 changed `ENGINE_RESPONSE_SCHEMA` in `tool/src/wasm_api.rs`. The sealed
  isolated manifest was RED for `source_tree_sha256`, `state_schema`, and
  `source_files`; byte-exact restore was GREEN. Restored source SHA-256:
  `ECF1CC2FB381DFE5F092C706411B9D4E6DE7382F115FE3B2666ADE0FAC298EF0`;
  blob `4db1ab214ba3969364acf686d1f2cd1f8e2986c7`.

## Review packet

- Canonical primary gates: official isolated-target WASM build, freshness
  manifest validation, and native offline tool check.
- Stop condition: any direct build failure, source/artifact binding drift, or
  another writer changing either leased path.
- Status: `PROD08A_STATUS=PRODUCT_FIXED_PENDING_REVIEW`.

## Nonclaims

This target does not claim tracked-WASM freshness after the build-script source
change, complete Native/WASM/Workbench behavior parity, V1 readiness, release,
or Human approval. Those are Blocker B or external gates.
