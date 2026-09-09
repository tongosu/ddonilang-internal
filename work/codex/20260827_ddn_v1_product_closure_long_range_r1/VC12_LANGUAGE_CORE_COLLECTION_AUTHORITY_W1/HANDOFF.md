# VC12 language-core collection authority W1 handoff

## Status

- `VC12_LANGUAGE_CORE_COLLECTION_AUTHORITY_IMPLEMENTED_UNDER_BUNDLED_REVIEW`
- This handoff does not close VC12, P1-A, P1, V1, membership, readiness, release, activation, or Human PASS.
- Review dispatch is intentionally deferred until the coherent VC06 + VC12 + VC04 product milestone is fixed. No new reviewer or review worktree was created.

## Authority and fixed identity

- Internal live CURRENT: v25.22.0 / RD-001~469 (read-only)
- Public Language SPEC: v0.6.0 (read-only)
- Baseline: `7079dd0ff378e88eee7967f71a8f2435b14a506a`
- Product/test fixed HEAD: `2a83ec409fedd00b9f7642362fe55bf72f00b583`
- Fixed tree: `495be98ee6e5f35dd29b970bae151207f9b0ff6a`
- Direct parent relation: exact
- Merge count from baseline: 0

## User workflow changed

An explicit `v1-core-v25` Korean source can construct `(1, 2, 3) 차림`, execute it through the native and tracked-WASM supported ingress, and deterministically publish `차림[1, 2, 3]`. The public spellings `차림` and `목록` and the existing `Call` syntax surface are unchanged.

## Product convergence

- `lang::runtime::list_new` remains the single language-core construction authority; no new runtime family was added.
- `lang::stdlib::list_function_sigs` no longer owns `차림` or `목록` as stdlib providers.
- `language_core_collection_constructor_sigs` keeps the two callable syntax surfaces available to the existing parser/canonicalizer registry.
- `tool::ddn_runtime` consumes `list_new` instead of constructing `Value::List` directly.
- The work-cost registry records the constructor rows under the language-core group and seals ledger SHA-256 `d0e4da47e6295044d06991a5d06d2a992b7859caac1f1fbfe1393cf8c6e90540` with 256 rows.
- `lang/src/runtime.rs` and `lang/src/lib.rs` did not require edits: the existing helper and re-export were sufficient.
- No AST variant, parser, canonicalizer, public alias, visible UI, SSOT, or SPEC change was made.

## Fixed diff

Exactly ten paths:

1. `lang/src/stdlib.rs`
2. `tool/src/ddn_runtime.rs`
3. `tool/src/wasm_api.rs`
4. `tool/src/work_cost.rs`
5. `pack/v1_core_supported_ingress_w1/manifest.detjson`
6. `pack/v1_core_supported_ingress_w1/fixtures/language_core_collection.ddn`
7. `tests/run_v1_core_supported_ingress_w1.py`
8. `tests/run_v1_core_supported_ingress_wasm_parity_w1.mjs`
9. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
10. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The work-cost file was a minimal FILE_OWNER expansion proven necessary by the product RED: moving the provider group changed the sealed registry identity, and native execution failed closed with `E_WORK_COST_REGISTRY_MISSING_CANDIDATE` until the language-core group was recorded.

## RED and verification

- RED-first: `collection_constructor_is_language_core_not_stdlib_provider` failed because `list_function_sigs` still contained `목록` (exit 1).
- Registry RED: native/WASM supported execution failed closed with `E_WORK_COST_REGISTRY_MISSING_CANDIDATE`; after adding the language-core ledger group, the new 256-row identity was sealed and GREEN.
- Focused authority test: 1/1 PASS.
- Work-cost ledger totality: 1/1 PASS.
- `ddonirang-lang --lib`: 365/365 PASS.
- `ddonirang-tool --lib`: 524/524 PASS.
- Existing supported-ingress runner: native 6, native/WASM exact 2, tracked-WASM cases 9, deterministic repeats 4, partial summary 0 PASS.
- Existing VC06 workflow reused: 11/11 native/WASM exact payload comparison, repeats 3, GREEN 7, RED 0, known PRODUCT_GAP 4; freshness and local-project CRLF unit PASS. The four pre-existing gaps were not promoted or changed.
- Official tracked-WASM freshness: PASS.
- No hash/receipt meta-tamper suite and no test-of-test were created.

## Artifact identities

- Supported-ingress manifest SHA-256: `c2df2e693982dd53ef087ea9bd87a827fcaa8982f6c96906ccbd1185620425f2`
- Collection fixture SHA-256: `37d8591f7fb613cebec290db3158bf336227ed5fdb144416c42c76b439c364cb`
- Tracked WASM: 5,556,611 bytes / SHA-256 `6afe6aada618cbbb7dd49af22623fc7a44003aeffc5d837c14e778166b9acc1d`
- Tracked WASM manifest SHA-256: `ef9bd90df1aece8ac260843bb53dc66ff0a5fd82aa31b466d235acf319b77391`

## Anti-meta and custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: supported-profile collection construction now converges on language-core authority across native/WASM.
- `NEW_TEST_ARTIFACT_COUNT`: 1 fixture; existing runner/pack extended, new runner 0.
- `EXISTING_TEST_REUSED_COUNT`: 6 verification surfaces (supported ingress, native/WASM unit parity, lang lib, tool lib, freshness, VC06 workflow).
- `META_TEST_CREATED`: 0.
- `STOP_RULE_APPLIED`: yes; no extra checker, mutation harness, evidence pack, or review task.
- `NEXT_PRODUCT_DECISION_ENABLED`: VC04 shared value/type/runtime convergence can now build on one collection constructor authority.
- Product worktree tracked clean, staged 0; task-owned VC17 and earlier preparation outputs remain untracked and unstaged.
- TCP 8787 listener count: 0. Protected process stop/restart/kill commands: 0.

## Remaining gates

- VC04 shared value/type/runtime authority convergence.
- Existing VC06 PRODUCT_GAP rows remain open and unchanged.
- VC17 exact/final/public membership remains an Owner gate.
- Coherent milestone independent review remains open and will reuse the designated rolling reviewer only after management binding.
- P2~P6, rights/license/distribution, release, activation, and Owner Human Smoke remain open.
