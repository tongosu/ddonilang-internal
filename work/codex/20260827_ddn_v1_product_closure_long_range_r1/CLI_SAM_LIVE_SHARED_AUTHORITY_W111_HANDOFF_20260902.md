# W111 CLI shared live-input authority handoff

## Fixed identity

- Internal authority read-only: SSOT v25.50.0 / RD-001~551 (docs-first, product-open).
- Public Language SPEC: v0.6.0.
- Product baseline: `18432effbe7489cc5865e945fcca5b2ba8d424cf`.
- Product fixed: `b0a1adc6be0681bca34fcc63684417f7d085efa0`.
- Fixed tree: `a657d74c0366032fd36b3959a104838965c0f632`.
- Direct parent: yes. Merge count: 0.

## Product workflow

The existing retained `teul-cli run --sam-live web` spelling is unchanged.
Its live keyboard-mask state, HTTP `/input` request handling, deterministic
tick sampling, CORS response, input-tape recording, and console mode now have
one semantic owner: `ddonirang_tool::live_input`.

`tools/teul-cli/src/cli/sam_live.rs` is only a `clap` spelling adapter from
the existing `console|web` value to the shared mode. No public command name,
option spelling, UI text/layout, source language behavior, package/binary
name, or WASM artifact changed.

Changed product paths:

1. `tool/src/live_input.rs` (new shared owner)
2. `tool/src/lib.rs` (native-only module exposure)
3. `tools/teul-cli/src/cli/sam_live.rs` (retained adapter)

## Evidence

- Existing shared product unit: `live_input::tests::std_grid_game_bogae_live_web_input_server_routes_update_mask` PASS.
- Retained `teul-cli` crate: `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
- Exact risk mutation: changing the shared web-token mapping from
  `1 << idx` to `1 << (idx + 1)` made the existing test RED
  (`ArrowLeft`: observed `(2, 2, 0)`, expected `(1, 1, 0)`).
- Exact restore SHA-256 for `tool/src/live_input.rs`:
  `6b6422c256d92d997c96dffffab52bf23e8950b0b39c0790261381b8b9f79632`.
  The same test was GREEN after restore; mutation residue is 0.
- `git diff --check` PASS.
- The existing Python browser-bridge runner was not product evidence in this
  worktree because it fail-closed before execution on a pre-existing missing
  `STD_GRID_GAME_BOGAE_WEB_PLAYBACK_CONTROLS_6DAY_V1.md`; that file was not
  created or changed.

## C0-C8 and rights boundary

- C0/C1: 91-command and public command membership custody unchanged.
- C2: shared input transport authority advanced for the retained live-input route.
- C3: no public membership claim is added.
- C4: this live-input family no longer owns private teul transport/timing/key/
  HTTP/tape semantics; other teul-private families remain.
- C5: bounded V1-required build/test/pack/publish teul dependency is unchanged;
  historical/internal custody is not reclassified.
- C6: native shared-web endpoint behavior is GREEN; host-native input has no
  applicable tracked-WASM transport claim in this slice.
- C7/C8: P5/release and physical teul retirement remain open.

`UNAVAILABLE-3` attribution/legal adjudication is a separate rights track.
This product fixed target does not claim `PUBLICATION_READY`, `RELEASE_READY`,
distribution authorization, rights-cleared artifacts, activation, V1 closure,
readiness, or Human PASS.

## Review and next boundary

No review task, worktree, branch, pack, runner, or dependency was created.
The existing rolling reviewer remains the only review custody when management
chooses a coherent CLI/teul authority bundle. This fixed target is
`IMPLEMENTED_UNDER_REVIEW`, not an independent PASS.

The next safe candidate must preserve the same rule: only move an existing
approved product authority where a shared owner already has its required
dependencies and no public command, wire, UI, or legacy-compatibility decision
is needed. `bogae_console`, `worker`, `view`, and `frontdoor_parse` are not
silently included because each currently crosses an open rendering, JSON-RPC,
or parser/contract boundary.
