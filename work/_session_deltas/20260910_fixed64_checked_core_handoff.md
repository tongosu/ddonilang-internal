# Fixed64 checked core arithmetic handoff

## Immutable product target

- Claim: the current `Fixed64` core now exposes checked addition, subtraction,
  multiplication, and division with integer-only ties-to-even rounding.
  Overflow and zero division are typed arithmetic failures rather than
  saturation or panic on that checked path.
- Product: `79c0a210a1cf83938fa6a7f3d3583b2b9f316f22`
- Tree: `0a007b91a59671c10878f20026919f10bf47d559`
- Parent: `3a3ed0f180cdf2c32d79040273bad43a4b17450e`
- Product paths:
  - `core/src/fixed64.rs`
  - `core/src/signals.rs`
  - `core/src/atomic_commit.rs`
  - `core/src/commit_canon.rs`

## Evidence

- Focused: `cargo test -p ddonirang-core fixed64 --offline -- --nocapture`: PASS
  (`16` tests).
- Regression: `cargo test -p ddonirang-core --offline`: PASS (`129` tests).
- Build: `cargo check -p ddonirang-core --offline`: PASS.
- All Cargo commands used
  `CARGO_TARGET_DIR=I:/home/urihanl/ddn/codex/build/target-v1-next-blockers`.
- `git diff --check`: PASS before the product commit.

## Mutation and exact restore

- M-A1 changed the ties comparison so an exact half rounded toward zero. The
  focused ties-to-even assertion was RED (`raw: 1`, expected `raw: 2`).
  Restore returned `core/src/fixed64.rs` to SHA-256
  `3C4B0EA3AA783619E714449D6E86C176CC43882FEBD0AE726F42172ADB5E22F7`,
  Git blob `4b59964d97d8a8382036f13e30ad99c2c9fea4bf`, followed by focused GREEN.

## Review packet

- Primary workflow: deterministic Q31.32 checked arithmetic used by the core
  contract, including overflow and exact-half rounding failures.
- Failure atomicity: the existing atomic-commit diagnostic and canonical
  serialization paths now preserve a typed `Overflow` fault rather than
  publishing a saturated checked result.
- Status: `PRODUCT_FIXED_PENDING_REVIEW`.
- Nonclaims: this is not a claim that every legacy saturating caller has been
  migrated, that the float boundary is closed, or that Fixed64/product/V1
  readiness, release, or Human gates are closed.
