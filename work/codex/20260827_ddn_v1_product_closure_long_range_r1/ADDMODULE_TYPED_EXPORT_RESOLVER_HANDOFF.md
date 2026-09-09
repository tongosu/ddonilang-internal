# AddModule typed export resolver handoff

Product fixed target: `8016f90e734482cc8c510ae905629907d2a1b68e`.

The Local Project linker now consumes RD-457 typed module directive metadata
through the shared parser prefix and validates each export target against the
strict V25 declaration AST. AddModule emits a current typed source file with no
legacy heading or brace metadata. Typed metadata is masked before linked
execution while retaining byte offsets for diagnostics.

The focused AddModule test creates `lib/힘.ddn`, imports it from `app/main.ddn`,
and verifies both the exported identity and resolved cross-module symbol.

Validation:

- `cargo test -p ddonirang-tool --lib structural_edit_plan_supports_add_module_duplicate_and_set_entry -- --nocapture` — PASS.
- `cargo check -p ddonirang-tool --offline` — PASS.
- `git diff --check` — PASS before the fixed commit.

Mutation evidence used the product blob
`55fedc0436055194873916792eca106d1e0e095c` / SHA-256
`820241c6c3aeb826f93f694b27285c694fadd7e1d70ebaea81b9869e53f1b62f`:

- M1 removed typed export collection: RED with `E_SYMBOL_NOT_EXPORTED`; exact restore then GREEN.
- M2 corrupted the typed export target binding: RED at the exported identity assertion; exact restore then GREEN.

Status: `ADDMODULE_EXPORT_RESOLVER=PRODUCT_FIXED`; same-reviewer rereview is
ready, but no review is dispatched by this writer. The next atomic unit is
tracked WASM freshness rematerialization from this handoff successor.
