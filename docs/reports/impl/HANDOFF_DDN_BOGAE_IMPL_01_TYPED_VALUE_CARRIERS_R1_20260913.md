# DDN BOGAE-IMPL-01 typed value carriers R1 — product handoff

## Custody

```yaml
LIVE_AUTHORITY: v25.79.0 / RD-001~613
PUBLIC_SPEC: v0.7.0
PRODUCT: 8c0781d1ac10dabea4b4e5699f6b26823bc23dc4
PRODUCT_TREE: 734f262fe6dd1e8e92017eeaf0502e3a53f035be
PRODUCT_PARENT: 1ba5696ee7a597e9f2452c8a85e02a8572a19d18
STATUS: PRODUCT_FIXED_PENDING_INDEPENDENT_REVIEW
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
NEW_SEMANTIC_IDENTITY: 0
NEW_CORE_IR: 0
PUSH: NO
```

This target physically lands the existing View, Scene, SceneElement,
BogaeRelation and BogaeComposition semantics. It does not implement a renderer,
projection hash matrix, full-headless lifecycle, Local Workspace persistence or
a public observation wire.

## Physical contract

- `ExprKind::BogaeValue` owns one exact provider identity and an ordered list of
  existing `ArgBinding` roles. The enclosing expression owns the provider/call
  span; each role retains its own source span and nested expression provenance.
- AST tags cover table/chart/scene content, textgrid/plane2/space3 profiles,
  SceneElement kinds, the four existing relation kinds (`으뜸`, `겹`, `곁`,
  `돋`), and composition. They do not introduce a public identity family.
- Parser lowering accepts only exact `표준장면.*`, `표준보기.*` and
  `표준보개.*` providers. Positional, missing, duplicate and unknown roles fail
  closed. Generic call resolution is not allowed to infer or repair these
  providers.
- Roles are stored and emitted in the provider's canonical named-pin order.
  Geometry element order and composition relation order remain authored order.
- Runtime values remain typed through evaluation. View/profile combinations are
  limited to table+textgrid, chart+plane2 and scene+plane2/space3.
- Geometry validates dimensionality, positive circle radius, polygon/face
  non-degeneracy, face planarity, increasing plane bounds and exact 3D camera
  ownership.
- Composition requires exactly one primary relation, unique relation values,
  unique integer overlay order and overlay basis bound to that primary.
- Failure occurs before the run commit. Bogae values may remain run-local, but
  Local Workspace/world persistence and public-observation serialization reject
  them with the existing unsupported boundary rather than inventing a wire.

## Existing semantic crosswalk

| Current owner | Physical carrier |
| --- | --- |
| RD-125 View content/profile matrix | `ViewContentKind`, `SpatialProfile`, `ViewSpatialBinding` |
| RD-127/129/130 View/relation/composition values | `BogaeTypedValueKind`, `BogaeRuntimeValue` |
| RD-133/134/135 relation roles | `BogaeRelationKind` plus ordered named roles |
| RD-520 exact Bogae providers | exact parser specifications for `표준보개.*` |
| RD-538 exact scene/view providers | exact parser specifications for `표준장면.*`, `표준보기.*` |

## Diagnostic mapping

| Failure | Existing diagnostic owner |
| --- | --- |
| missing role | `E_CALL_REQUIRED_PIN_MISSING` |
| positional, unknown or wrong-typed role | `E_BOGAE_ENTRY_TYPE` |
| duplicate role/value | `E_BOGAE_ENTRY_DUPLICATE`, `E_BOGAE_RELATION_DUPLICATE` |
| content/profile or element/profile mismatch | `E_BOGAE_PROFILE_MISMATCH` |
| invalid geometry | `E_BOGAE_ENTRY_TYPE` |
| multiple or absent primary | `E_BOGAE_PRIMARY_COUNT` |
| overlay order/basis | `E_BOGAE_OVERLAY_ORDER_DUPLICATE`, `E_BOGAE_OVERLAY_BASIS_INVALID` |
| persistence/public-wire boundary | `E_BOGAE_UNSUPPORTED` |

Exact provider names remove the ambiguous-owner path. Non-exact spellings stay
on the existing generic resolver and are not promoted by string or source-order
inference.

## Product paths

The initial five-path lease expanded only to compiler-proven direct AST
consumers; no second semantic owner was added.

```text
lang/examples/canon_ast_dump.rs
lang/src/ast.rs
lang/src/canonicalizer.rs
lang/src/execution_mode.rs
lang/src/migration.rs
lang/src/normalizer.rs
lang/src/parser.rs
lang/src/runtime.rs
tool/src/ddn_runtime.rs
tool/src/lsp/selection_range.rs
tool/src/lsp/signature_help.rs
tool/src/lsp/symbol.rs
tool/src/project_authoring.rs
tool/src/work_cost.rs
```

Product diff: 14 files, 1,736 insertions, 261 deletions. The LSP/project/example
changes are exhaustive traversal support for the new typed AST carrier.

## Verification

- Exact Bogae parser/canonicalizer tests: 2/2 PASS.
- Runtime success/profile/atomicity focused tests: 3/3 PASS.
- Existing tool Bogae filter: library 18/18 and console binary 2/2 PASS.
- LSP signature/document-symbol/open-navigation: 15/15 PASS.
- Native tool library offline check: PASS.
- WASM32 tool library offline check: PASS.
- `git diff --check`: PASS.
- Full language library run: 376/379. The three failures are inherited typed
  send/receive NAME-LINT cases and do not touch this target.
- Full tool library run: 657/696. The 39 failures are inherited async,
  project-authoring, ai-prompt and runtime-surface baseline failures; all target
  focused gates and direct consumers above are green.

## Mutations

1. Reverse canonical role order: canonical round-trip assertion RED, exit 1;
   parser exact restore to blob `0597a281aa22d400105746337b6b242dab5c7145`,
   SHA-256 `730058C658A0A91DD03F6DEB95D639D698F3BAA734A455B6E99DF19880A7092C`;
   GREEN.
2. Remove scene element/profile compatibility guard: invalid 3D face reached a
   plane2 scene, RED exit 1; runtime exact restore to blob
   `95369749f0757502906fa9f13558f89baae5a4f2`, SHA-256
   `00D5618EFF555890787FCC9597D97E3621989D22AD80795CA9F1BF76ABF2B9B2`;
   GREEN.
3. Remove duplicate-primary guard: two primary relations were accepted, RED
   exit 1; exact runtime restore to the same fixed blob/SHA; GREEN.

## Pack disposition and nonclaims

The focused tests make `BIC-SCENE-GEOMETRY-01/02` and
`BIC-MULTIVIEW-01/02` physical-fixture candidates. No planned BIC case is
promoted to an executable oracle here. The hash cases remain unmaterialized
because the hash matrix is explicitly out of scope.

Independent review must bind the exact product commit/tree above and reproduce
the three mutations. Until then `BOGAE_IMPL_01` is product-fixed, not
`CLOSED_TARGET_BOUND`, and readiness for BOGAE-IMPL-04 is not claimed.
