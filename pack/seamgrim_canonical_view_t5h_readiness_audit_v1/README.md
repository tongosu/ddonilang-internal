# seamgrim_canonical_view_t5h_readiness_audit_v1

T5H status-totality contract. It freezes the exact 14-key canonical inventory, requires every unknown status to fail closed as `invalid`, and preserves the five accepted non-success statuses without changing available-path meaning.

```powershell
node tests/seamgrim_canonical_view_t5h_readiness_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_status_totality_mutation_runner.mjs

$env:DDN_T5F_SOURCE_WASM_DIR = '<current source-built WASM directory>'
node tests/seamgrim_canonical_view_t5h_cross_family_readiness_runner.mjs
```

`PASS` means all 14 families reject the unknown probe with family-local candidate diagnostics and preserve `no_view`, `unavailable`, `invalid`, `unsupported`, and `ambiguous`. T5H closure still additionally requires the actual-surface/compatibility matrix and full regression/browser handoff.

The aggregate runner executes the 12 T5B–T5G golden/mutation runners plus the status-readiness and status-mutation runners. Browser runners stay separate because they require explicit local Playwright custody; their absence from this aggregate is not a browser PASS claim.

The dependency-independent browser/fallback matrix is executable separately:

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = '<current source-built WASM directory>'
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<local node_modules containing playwright and playwright-core>'
node tests/seamgrim_canonical_view_t5h_browser_fallback_readiness_runner.mjs
```

`browser_fallback_matrix.detjson` enumerates all 14 active families, the existing browser runner that probes each family, the golden/mutation group that guards against semantic fallback, and explicit current-product, compatibility-only, and `NOT_APPLICABLE` surface cells. The aggregate runs five browser groups, the representative curriculum browser gate, and the 14-command T5B–T5H readiness aggregate. T5G plain `PASS` is bound and status totality is closed; the matrix does not mislabel every browser family probe as a distinct per-surface browser execution.

The consumer token `playground` has a separate identity audit:

```powershell
node tests/seamgrim_canonical_view_t5h_playground_surface_identity_audit_runner.mjs
```

The current `play.html` explicitly marks `legacy_compatibility_only` and redirects the former Playground address to Workbench Studio, while `playground.js` has no active HTML/JS importer. Owner `OPTION_B_PLAYGROUND_IS_LEGACY_COMPATIBILITY_ONLY` keeps its authoritative language/runtime owner shared but excludes it from full current-product surface identity. Existing T5C–T5F projection evidence is retained as historical compatibility evidence; it is not promoted into Run/Workbench lifecycle, storage, or revision parity.

```powershell
node tests/seamgrim_canonical_view_t5h_playground_option_b_mutation_runner.mjs
```

`surface_evidence_matrix.detjson` classifies the 26 actual current-product cells by executable evidence strength. Twelve Playground cells are kept separately as `LEGACY_COMPATIBILITY_ONLY`, and the four Workbench-family Run aliases are recorded as `NOT_ACTUAL_PRODUCT_CONSUMER` because `screens/run.js` has no family-specific consumer. Current-product parity is therefore closed without silently promoting compatibility aliases or synthetic function aliases.

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = '<source-built WASM directory>'
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<local Playwright node_modules>'
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_mutation_runner.mjs
```
