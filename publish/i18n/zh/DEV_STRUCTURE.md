# Public development structure — Ddonilang

> 起始翻译；Human review open

| Layer | Path | Responsibility |
| --- | --- | --- |
| deterministic engine | `core/` | committed world-state transitions |
| language | `lang/` | grammar, parser, canonicalization |
| runtime and tool | `tool/` | execution front door and WASM API |
| CLI | `tools/teul-cli/` | command-line execution and public checks |
| numeric and proof | `numeric/`, `symbolic/`, `proof/` | bounded math and proof kernels |
| Seamgrim | `solutions/seamgrim_ui_mvp/` | browser workspace and view layer |
| public documents | `publish/` | guides and fixed public SPEC lineage |

## Verification boundary

- GitHub public CI verifies public code tests, selected golden tests, the public SPEC seal, and the
  first CLI example.
- It does not prove full browser behavior, Human review, private SSOT gates, or every docs-first
  surface.
- Runtime truth belongs to committed DDN state and records. A renderer must not invent hidden
  semantics from CSS, metadata, project titles, or file order.
- Python and JavaScript may orchestrate tools and UI, but test-only lowering is not language
  implementation evidence.

[Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md) ·
[Public Language SPEC](../../spec/CURRENT.md)
