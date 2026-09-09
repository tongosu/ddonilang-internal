# VC13 strict Selection shared-authority W100 handoff

## Status and authority

- Status: `VC13_STRICT_SELECTION_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.
- Live internal CURRENT: v25.49.0 / RD-001~543, pointer SHA-256 `bc508d45e053d8c8a84b08e8c1657bc6eec5e82c1ad4a04d12d7daf22dfec6fa`.
- Public Language SPEC: v0.6.0, pointer SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- v25.49 successor impact: `UNAFFECTED_WITH_ADDITIVE_RELEASE_CUSTODY`; it adds no semantic RD relative to this product slice.
- Baseline: `2349531481458d63cefb362e2fe27ee154b62b24`.
- Product/test fixed commit: `6a6e25032b6a11a4b5b2f4f0ce0d7a3f81365f7e`.
- Fixed tree: `6a8d147249226b1d7f5c18c9e1c8816b876dea10`.
- Direct parent: exact; merge count from baseline: 0.

This fixed target does not close VC13, P1, V1, readiness, release, activation, or Human PASS.

## User workflow and product convergence

An explicit `v1-core-v25` Korean program can construct a homogeneous `차림`, read an in-range element with typed postfix Selection, and receive the same deterministic result through official native and tracked-WASM ingress. An out-of-range strict Selection now aborts with the existing structured runtime envelope and existing `FATAL:CHARIM_INDEX_OUT_OF_RANGE` message instead of silently becoming `없음`; failed output publication is zero.

`lang::runtime::list_nth` is the single selection authority. Both tool dispatch spellings, `차림.값` and its existing `번째` route, consume that helper. The tool no longer duplicates the value/default decision. No parser, AST, canon, public spelling, safe-lookup name, or new diagnostic family was introduced.

## Exact fixed diff

Exactly nine paths:

1. `lang/src/runtime.rs`
2. `tool/src/ddn_runtime.rs`
3. `pack/v1_core_supported_ingress_w1/manifest.detjson`
4. `pack/v1_core_supported_ingress_w1/fixtures/language_core_collection.ddn`
5. `pack/v1_core_supported_ingress_w1/fixtures/strict_selection_out_of_range.ddn`
6. `tests/run_v1_core_supported_ingress_w1.py`
7. `tests/run_v1_core_supported_ingress_wasm_parity_w1.mjs`
8. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
9. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No SSOT, public SPEC, visible UI, `tools/teul-cli`, publish, or release-projection path changed.

## RED, GREEN, parity, and mutation

- Product RED: official native `run --source-profile v1-core-v25` on the new strict-selection fixture returned `E_RUNTIME_TYPE_MISMATCH`, actual `없음`, proving the shared runtime had silently defaulted the out-of-range read.
- Product GREEN: the same invocation returns nonzero `E_RUNTIME_EXECUTION` with existing message `FATAL:CHARIM_INDEX_OUT_OF_RANGE`, with no output rows or output-log fields.
- Language regression: 369/369 PASS.
- Tool focused P1-A regression: 7/7 PASS.
- Tool full library: 606 PASS plus the same two isolated-worktree environment failures because `docs/ssot` is absent; no new failure.
- Existing supported-ingress runner: native 8, native/WASM exact 2, tracked-WASM cases 11, deterministic repeats 5, partial summary 0, official CLI positive 4 and negative 5 PASS.
- Tracked-WASM freshness: PASS.
- Workbench-applicable path: its tracked structured WASM consumer uses the same exported supported-profile runtime; JS semantic reconstruction and visible UI change are both zero.
- Risk mutation: restoring `list_nth` silent `없음` fallback made `runtime_list_nth_out_of_range_fails_closed` RED with exit 101. Exact restore SHA-256 `4bcfc1a33f6248099f3cf241182f8aeb10f012e58f21fa9bf74b95d7509c3ecc` returned GREEN; residue 0.

## Fixed artifact identities

- Supported-ingress manifest: 1,030 bytes / SHA-256 `189eeb379630e431c84925267c7035787288c14c6f8a9bf4258b1173b5733ac3`.
- Strict-selection fixture: 127 bytes / SHA-256 `14400e5796be2ef74a73a02407c05205441a7d290477cb7028e8eb8cf8a15992`.
- Tracked WASM: 5,579,392 bytes / SHA-256 `6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e`.
- Tracked WASM freshness manifest: 29,626 bytes / SHA-256 `e688084bf79b74de19298015e6ce3b35c916eecd409639afa03c83fe90c3fa70`.

## Anti-meta and open gates

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: strict list Selection no longer publishes a silent default, and native/WASM consume one language-core authority.
- `NEW_TEST_ARTIFACT_COUNT`: 1 product fixture; new runner/pack/framework/meta-test 0.
- `EXISTING_TEST_REUSED_COUNT`: 5 surfaces (language lib, tool focused, tool lib, supported ingress, freshness).
- `META_TEST_CREATED`: 0.
- `ACTIVE_REVIEW_TASK_COUNT`: 0; the existing rolling reviewer handle is preserved and management owns dispatch.
- `REVIEW_BUNDLE_TARGET`: W90-W100 current-source CLI/P5/VC13 coherent milestone at this handoff successor.
- VC14 Basic Tensor R1 stays `CONCRETE_DETAIL_GAP_DETECTED`: exact physical parser/AST/wire/runtime/diagnostic is PRODUCT-OPEN, and the public example also relies on an untyped-definition form rejected by the current supported profile. No inference or Tensor surface was invented.
- Historical teul/internal-deferred selection behavior is custody only and was not promoted, deleted, or used as V1 semantic authority.
- C0-C8 CLI convergence status is unchanged by this slice; required teul execution dependency remains zero in the fixed V1 projection, while physical teul retirement and public command/executable decisions remain open.

## Custody

The product worktree was tracked clean and staged zero immediately after the fixed commit. Four pre-existing task-owned untracked custody files remain byte-preserved and unstaged. Protected process stop/restart/kill commands: 0. TCP 8787 listener operations: 0. New reviewer, review worktree, branch, task, pack, or runner: 0.

