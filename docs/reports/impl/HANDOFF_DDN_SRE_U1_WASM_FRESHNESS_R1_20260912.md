# SRE-U1 tracked WASM freshness — implementation handoff

## Fixed target

- Product commit: `be6e56cf5dda3afa38738cce8e19468e7920f5c1`
- Product tree: `1e9a6b38dde7facc0fec8eb305d3c7f635be5592`
- Product parent: `4971b76c18a039f93fda01fbb744a80ed19100b1`
- Claim: `PRODUCT_FIXED_PENDING_INDEPENDENT_REVIEW`

## Product paths

- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The tracked release/web artifact was rematerialized through the official
`scripts/build_wasm_tool.ps1` entrypoint, then sealed with the existing
freshness manifest writer. No language source, ParamPin semantics, public API,
wire, JS lowering, or fallback changed.

## Artifact identities

| Path | Git blob | SHA-256 |
| --- | --- | --- |
| `ddonirang_tool_bg.wasm` | `7bdecd2206353557ce1b40465fec23bf78f42578` | `9193D07F0438056F111A17250E81F39312DEBAF92CCE8E26D7E8A7EE2DF9CAC2` |
| `ddonirang_tool.manifest.detjson` | `f35010928a26e4bc3755e2089c725ae858183672` | `3A1E2409AB46F1A280724717EBD6C2DB7A2E205C3262F82743FBEE3AA873CCD6` |

Builder identity: rustc `1.92.0`, cargo `1.92.0`, wasm-pack `0.14.0`.

## Gates

- Baseline freshness RED: source tree and source-file fingerprint mismatch.
- Official release/web build: PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- Second official build: artifact and manifest SHA-256 unchanged; PASS.
- `node tests/ddn_cli_wasm_post_wasm_shared_changes_runner.mjs`: PASS.
- `cargo test -p ddonirang-lang sre_ --offline`: PASS (3).
- `cargo test -p ddonirang-tool sre_public_pin_binds_the_distinct_local_binder_at_runtime --offline`: PASS.
- `cargo test -p ddonirang-lang --offline`: PASS (377).
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline`: PASS.
- `git diff --check`: PASS.

## Mutation evidence

1. Replacing the fixed WASM with the predecessor blob
   `0a90c5e78bc125b8a49abdbd8f532dc4f8db1af8` made freshness fail on
   `wasm_sha256` and `wasm_size`. Restored the fixed artifact SHA-256 above;
   freshness GREEN.
2. Replacing `source_tree_sha256` in the manifest with all zeroes made
   freshness fail on `source_tree_sha256`. Restored fixed manifest SHA-256
   above; freshness GREEN.

## Review focus and nonclaims

Review exact source/artifact/manifest binding, repeat-build determinism, and
the two stale/tampered rejection axes. This target is freshness-only: it does
not claim a new language feature, full CLI/WASM equivalence, public release,
SSOT or public-SPEC transition, or independent PASS.
