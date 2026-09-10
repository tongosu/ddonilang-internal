# Generator Unit A typed import/export correction handoff

Fixed target: `4e9839935a78b5baeba0e3ef46f2e250df5826ef`
Parent: `5d4bfea03127a7b028356252d2e26d1cf391efe6`
Tree: `c8a054e9e30bff9b515fab50b6ab93f0cc26ad69`

## Product change

The Local Project authoring snapshot now consumes parenthesized RD-457 module
directives through the existing typed directive owner. It no longer performs a
second, legacy-only import/export parse for current source. The generated
physics source `(힘="./lib/힘") 쓰임.` and `(중력=중력) 드러냄.` reaches typed
metadata and the Local Project symbol frontdoor without `E_PROJECT_BLOCK_UNSUPPORTED`
or `E_SYMBOL_NOT_EXPORTED`.

Changed product paths:

- `tool/src/local_project.rs`
- `tool/src/project_authoring.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

Tracked WASM SHA-256: `16e9687f2784f0b1a713a67f8a47fd8e198bdfa411374a18e41a1a14eb7ada1d`.
Manifest SHA-256: `81505ee0f8f3c1c59c0fb78df7f9820e86dc7c788902199693a8ad46a0c01cd8`.

## Evidence

- Focused physics authoring frontdoor: PASS.
- Existing AddModule structural edit/resolution test: PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- Official release WASM build followed by `run_ddn_cli_wasm_freshness_check.py`: PASS.
- `git diff --check`: PASS before fixed commit.
- M1 typed export collection removed: RED (`E_SYMBOL_NOT_EXPORTED`), exact restore, GREEN.
- M2 exported DefinitionIdentity target altered: RED, exact restore, GREEN.
- M3 legacy brace parser reintroduced for current source: RED (`E_PROJECT_BLOCK_UNSUPPORTED`), exact restore, GREEN.

The existing broad local-project graph checker executes the project successfully
but its historical exact transcript expects directive removal, while the reviewed
RD-457 carrier byte-preserving mask retains directive whitespace. This produces
a source/receipt hash golden mismatch; no golden rewrite is included in this
Unit A correction.

## Scope and nonclaims

`LEGACY_FALLBACK_COUNT=0`; no parser, JS/Python lowering, public wire field,
SSOT, public SPEC, release, or publication change is included. This target is
`PRODUCT_FIXED_PENDING_REVIEW`, not an independent PASS or closure claim.

`READY_FOR_INDEPENDENT_REVIEW=YES`. Next exact action: Unit B only from this
handoff successor after review scheduling custody is supplied.
