# Fixed64 linear-quantile checked-arithmetic handoff

- Product: `229df87f75d50f8810ea79adf87af7b08c0d86c5`
- Tree: `79a62a5129889e2f502027ac30da304c724e62ec`
- Parent: `b7de8f77cb5d436171aa1ecfcf01b06b97504dc4`
- Product path: `tool/src/ddn_runtime.rs`

The active linear `분위수` path no longer uses saturating Fixed64 operations for
position, fractional remainder, delta, interpolation product, or final sum.
An unrepresentable extreme interpolation returns `E_RUNTIME_ARITH_OVERFLOW`
before a successful update is constructed.

Evidence:

- focused extreme linear-quantile test — PASS
- `git diff --check` — PASS before commit

Mutation M1: replacing the checked delta subtraction with saturation caused the
extreme interpolation fixture to return success and made the focused rejection
assertion RED. Fixed restoration:

- SHA-256: `038064a9d0ea7762bc65aac60218c9f9b4b6e78797a898f1f5100458f82ed2db`
- blob: `c8ddbfeb036a35327c9a16e5acf60f8bcb8b4d9e`

Nonclaims: this is one active numerical caller only. It does not establish full
Fixed64 caller migration, Native/WASM behavioral convergence, tracked-WASM
freshness, release readiness, or independent review.
