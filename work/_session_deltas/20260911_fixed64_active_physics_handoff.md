# Fixed64 active physics checked-arithmetic handoff

## Target

- Product commit: `27c9e37c1ced7c8458aee772f431a2617df0171e`
- Product tree: `ff3448d39ecf505a20523def5b1fcba89f3e1819`
- Parent: `349005d6fc669d8b3d19a678d48b326f6c9f1832`
- Product paths: `tool/src/ddn_runtime.rs`

## Claim for independent review

The active `물리1d.위치갱신` and `물리1d.속도갱신` runtime callers now use
checked Fixed64 multiplication and addition.  Overflow is returned as the typed
`E_RUNTIME_ARITH_OVERFLOW` failure before a run output can be published.

Focused product behavior:

- normal physics smoke remains green;
- both active callers reject `Fixed64::MAX + 1 * 1` through the runtime
  frontdoor;
- both reject with `E_RUNTIME_ARITH_OVERFLOW` rather than a saturated value.

## Executed evidence

- `cargo test -p ddonirang-tool --lib physics_ -- --nocapture` — PASS (5 tests)
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `cargo test -p ddonirang-tool --lib` — 643 passed; 5 pre-existing failures:
  two `ai_prompt` tests require a missing `docs/ssot` directory in this isolated
  worktree, plus unrelated numeric calculus, BOM project-authoring, and
  runtime-surface assertions.
- `git diff --check` — PASS before the product commit.

## Mutation evidence

Fixed source after both tests: SHA-256
`72cdb4a93963a5d6e1825eb0b97aeec6f3daccb5e7375335c461b8e82128d51b`, blob
`78dffe9b097f68012e70c90fa722f69846974c48`.

1. Replacing the position caller's checked operations with saturating operations
   made `physics_position_update_overflow_is_typed_and_publishes_nothing` RED:
   the overflow incorrectly produced a run output.  Exact restoration returned
   the focused test to GREEN.
2. Downgrading the overflow diagnostic to `E_RUNTIME_EXECUTION` made the same
   focused test RED.  Exact restoration returned the focused physics group to
   GREEN.

## Nonclaims

- This target is not an independent PASS and is not `CLOSED_TARGET_BOUND`.
- This slice does not claim that every Fixed64 caller in the repository has been
  audited, nor that tracked WASM freshness was rematerialized.
- No SSOT, public SPEC, public wire, pack, release, or Human gate changed.
