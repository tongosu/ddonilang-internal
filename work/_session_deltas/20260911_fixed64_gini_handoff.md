# Fixed64 Gini checked-arithmetic handoff

- Product: `35e94a68a4cda6178b6d3d05d131fccd553e624d`
- Tree: `2c5ba558ea374b83618c866f41f13fdf3cdfa541`
- Parent: `eb32674d89cdb9ab49b2f9b69235d06b79ed0210`
- Product path: `tool/src/ddn_runtime.rs`

The active `지니` / `지니계수` builtin now uses checked Fixed64 accumulation,
pair-difference accumulation, denominator multiplication, and division. An
unrepresentable intermediate is a typed `E_RUNTIME_ARITH_OVERFLOW` failure;
no result is published.

Evidence:

- `cargo test -p ddonirang-tool --lib gini_ -- --nocapture` — PASS
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --check` — PASS before commit

Mutation M1: changing the checked denominator multiplication to saturation made
the overflow fixture (`1073741824`, `1`) return a successful update; the focused
test was RED. Exact restoration returned GREEN.

- restored SHA-256: `743ed4030b54f931f1e533a11a6c4c6745b901a26d78b4fcfa0b02e933e2ad92`
- restored blob: `c4c4b5d7939cefc04832ea2003da33e6c44cffac`

Nonclaims: this covers only active Gini aggregation; it is not an all-caller
Fixed64 audit, tracked WASM freshness claim, release claim, or independent PASS.
