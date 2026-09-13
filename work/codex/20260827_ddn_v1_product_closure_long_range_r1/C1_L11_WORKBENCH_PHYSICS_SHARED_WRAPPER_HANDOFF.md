# C1 L11 Workbench Physics Shared Wrapper Handoff

## Fixed target

- Product commit: `a7fdb5e1416dc501e45c057c0bc1854c42245362`
- Product tree: `214d1ae829200e78cb778e6ca626454c638349cd`
- Parent: `c795cc4658f4b8869bcc5ae8395b9d43634c9092`
- Scope: the tracked Workbench physics project now emits the callable body only.
  `build_project_run_summary_with_supported_profile` remains the only owner of
  the enclosing current-V25 callable for supported Local Project execution.

## Product paths

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`
- `tool/src/local_project.rs` (shared-frontdoor native execution regression)
- `tool/src/project_authoring.rs` (exact generated-source resolver regression)
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Direct evidence

- Pre-correction tracked-WASM execution of the nested `운동:움직씨 := { ... }`
  entry failed with `E_EXECUTION_PARSE` at the nested callable type position.
- The exact current generated physics project now passes the native shared
  Local Project run twice with equal state and summary identities.
- The same raw project passes rebuilt tracked WASM twice with identical
  summary `7c97067d520df048c34709b11957f07f0065affaf715f11a3761a15223d38508`,
  state `blake3:bea9eefe75ad02c14d990d26510a22a48617fe60d7db46cd2bcb5637f72a757b`,
  and three output rows.
- `current_typed_directives_reach_the_authoring_symbol_frontdoor` passes.
- `current_workbench_physics_body_runs_through_the_shared_frontdoor` passes.
- `cargo check -p ddonirang-tool --offline`, `node --check` for the tracked
  Workbench source, `python tests/run_ddn_cli_wasm_freshness_check.py`, and
  `git diff --check` pass.
- WASM SHA-256: `abdd90f660d057ccf113a73635deb05a7ed905d04fd29ed84efec7c391370404`.

## Scope and nonclaims

- The official browser runner could not be executed in this environment because
  its `playwright` package is unavailable; no browser-behavior PASS is claimed.
- A launched whole `cargo test -p ddonirang-tool` had no recoverable final
  verdict in this session; no whole-tool PASS is claimed.
- The earlier producer and strict-hardcut mutation evidence remains historical
  custody only; this handoff does not self-claim independent review, C1 closure,
  V1 readiness, release, activation, or Human PASS.

## Review target

`a7fdb5e1416dc501e45c057c0bc1854c42245362` is a fixed product target for
targeted independent review of the Workbench Physics generated-source correction
and its tracked WASM freshness rematerialization.
