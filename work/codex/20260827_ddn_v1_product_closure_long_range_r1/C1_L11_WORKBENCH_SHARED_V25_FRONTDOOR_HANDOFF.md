# C1-L11 Workbench shared V25 frontdoor handoff

## Fixed target

- Product commit: `126f730b396f5817c646f255ab1cc9b95c8c4fa5`
- Parent: `764a5b4a4a5319ae2183bfda433170aacf3aebdb`
- Tree: `98bd0da322efe8e5a24c34975bc2cd8e189e358c`
- Merge commits: `0`

## Product correction

The native Workbench Physics template keeps the typed RD-457 import surface,
but uses current V25-compatible definition names.  Local-project `prepare/link`
now applies the same shared V25 `매마디:움직씨 :=` wrapper used by project-run
when an entry body has no named update target.  Workbench source readiness
uses that project frontdoor for a local project, and the Workbench VM session
passes the established `v1-core-v25` profile instead of entering the legacy
JS preprocessing path.

No public syntax, SSOT, Language SPEC, compatibility fallback, or teul path
was added.

## Evidence

- `cargo test -p ddonirang-tool --lib local_project::tests::current_workbench_physics_body_runs_through_the_shared_frontdoor -- --exact`: PASS.
- `cargo test -p ddonirang-tool --lib module_directive_analysis::tests::workbench_physics_template_uses_the_same_typed_carrier_without_chaebi -- --exact`: PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- Official `scripts/build_wasm_tool.ps1 -Profile release -Target web`: PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest` then checker: PASS.
- `git diff --check`: PASS.
- Actual tracked Workbench browser workflow: New Physics Project → Run → `current project VM run · 실행 완료 · 한 번 실행`; state hash, bounded-state hash, three output rows, and `wasm_project_prepare_link_json` lineage were present.

Tracked WASM SHA-256: `b77b2ebebd47f6fe241c612b0a6a038e9b4dd401588b0f3a9ee493d817f00095`.
Manifest SHA-256: `091d922a25e5769bcbb21ee3a6e4f7f3efddf68508c6e5be18ac8e61ba47580f`.

## Nonclaims

This is a product-fixed successor only.  It does not claim independent review,
P0-P6 closure, V1 readiness or release, activation, legal clearance, or Human
PASS.

READY_FOR_INDEPENDENT_REVIEW=YES
