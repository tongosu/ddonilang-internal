# C1-L11 strict current Project frontdoor handoff

## Fixed target

- Product commit: `23f1a319553a0b8ac333aaae3dad4451eaef9209`
- Product tree: `5193995c792158d9a1df4e04dcff891b72a55c7d`
- Direct parent: `72b78f078967251e84ab311b4a6a83cd4533166d`
- Scope: `tool/src/local_project.rs`, tracked Workbench WASM binary, and its
  existing freshness manifest only.

## Product behavior

The supported current Local Project run frontdoor now tokenizes every
`ddn_source` before graph/link processing. A lexical `쓰임 {`, `드러냄 {`, or
`공개 {` pair produces `E_V25_DEFINITION_MIGRATION_REQUIRED` with the source
path and span before runtime execution or summary publication.

Historical metadata handling remains physically preserved for non-supported
paths, but its brace-block recognition now uses lexer tokens. Consequently the
same text inside a comment or string is not silently treated as module metadata
or a legacy declaration.

The supported host-resource test now supplies a typed current project fixture;
the general historical multifile fixture remains unchanged.

## Verification performed

- `cargo test -p ddonirang-tool --lib current_project_run_rejects_legacy_l11_before_runtime_publication -- --nocapture` — PASS.
- `cargo test -p ddonirang-tool --lib supported_project_run_binds_declared_host_resource_before_execution -- --nocapture` — PASS.
- `cargo test -p ddonirang-tool --lib current_workbench_physics_body_runs_through_the_shared_frontdoor -- --nocapture` — PASS.
- `cargo test -p ddonirang-lang --test v25_definition_binding_pack` — PASS (5/5).
- `cargo check -p ddonirang-tool --offline` — PASS.
- Official `scripts/build_wasm_tool.ps1 -Profile release -Target web`, followed by `tests/run_ddn_cli_wasm_freshness_check.py --write-manifest` and the ordinary freshness check — PASS.
- `git diff --check` — PASS before the fixed commit.

The final tracked artifacts are:

- `ddonirang_tool_bg.wasm`: `f6e4b09c20a0da83a030117d2f3321c7abea59000f509c90aba09db6bec5355`
- `ddonirang_tool.manifest.detjson`: `559f0bf6d63144151f8cd1eff3ba96a55fee7427c2c173d733b80de257f99eca`

## Mutation custody

- M1: bypassing the supported-profile preflight made the legacy source return a
  successful Local Project summary (RED); restoration returned the focused
  rejection test to GREEN. The contemporary restored blob was
  `194b18f8cea1fc482b45e8926c50337c97c0231a`.
- M3: replacing lexer-token recognition with raw `text.match_indices` made the
  comment-only current source fail with `E_PROJECT_METADATA_BLOCK` (RED).
  Exact restore blob: `041cb9b6e009d9c690d1f4eb7e52ee46bf161cb1`; focused test
  GREEN.
- No automatic brace-to-parenthesized conversion path exists in this target and
  none was introduced merely to manufacture M2. The fixed behavior is direct
  fail-closed rejection, not conversion.

## Known regression boundary

One full `cargo test -p ddonirang-tool` run before the host-resource fixture
correction completed `639 passed / 5 failed`. The supported host-resource
failure was corrected and its focused test is now GREEN. The remaining failures
were outside this fixed path (`ai_prompt` SSOT absence, a BOM authoring case,
and a runtime-surface canon expectation); they require separately scoped
ownership and are not represented as a whole-suite PASS.

## Status and nonclaims

`BLOCKER2_STATUS=PRODUCT_FIXED_PENDING_REVIEW`.

This handoff does not claim independent PASS, C1-L11 whole closure, V1
readiness, release, activation, publication, legal clearance, or Human PASS.
