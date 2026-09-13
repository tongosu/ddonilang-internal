# Fixed64 exponential smoothing checked blend handoff

## Immutable target

- Product commit: `7caa60109180591cfc1c2ad0c8c77e79c99a8ff6`
- Product tree: `77b192ac5af74a831bd3012541ada41560585548`
- Parent: `881ce2c6d28f3d4a8aee2fd770aab04f09ba65bb`
- Product paths: `core/src/fixed64.rs`, `tool/src/ddn_runtime.rs`
- Merge commits: `0`

## Claim

`필터.지수평활` now calls the shared checked Q31.32 weighted-blend owner.  The
two weighted products are accumulated in one widened intermediate and rounded
once with ties-to-even; component-wise saturation and rounding are no longer
an active runtime authority for this caller.

The runtime tests bind raw V25 source through `DdnProgram` and `DdnRunner`:

- the exact maximum endpoint remains `Fixed64::MAX`;
- a precision witness that would give `-21 raw` under component-wise rounding
  produces the one-round result `-20 raw`.

## Fixed blob custody

| Path | Git blob | SHA-256 of working Git-normalized bytes |
| --- | --- | --- |
| `core/src/fixed64.rs` | `26e0d4bd4bd3dd7320ccb9e5f225c81326a73e48` | `71413e78ebd045767a3dacb0f5d1bd3e2baa79b4f6bc4a22db6566cdc55c9f6d` |
| `tool/src/ddn_runtime.rs` | `37983ad0d2d9c4325dd12b15386d52af71408bd7` | `73e46e8bd98edfd1bf8e40bc3f0baa088e5b45bd802d3db9aca331bd358c5c84` |

## Mutation evidence

| ID | Temporary mutation | Observed RED | Exact restore | GREEN |
| --- | --- | --- | --- | --- |
| M1 | Drop the `next * weight` widened term. | Maximum-endpoint core assertion returned half-maximum. | Restore `checked_weighted_blend` to the `26e0…` blob. | Core focused test passed. |
| M2 | Reinsert the former component-wise `saturating_mul`/`saturating_add` caller. | The raw-source precision witness returned `-21 raw`, not `-20 raw`. | Restore runtime to `3798…`. | Both exponential-smoothing runtime tests passed. |
| M3 | Replace ties-to-even division with truncation. | Half-way core case returned raw `1`, not raw `2`. | Restore the ties-to-even division in `26e0…`. | Core focused test passed. |

## Executed gates

- `cargo test -p ddonirang-core` — PASS, 130/130.
- `cargo test -p ddonirang-tool --lib exponential_smoothing -- --nocapture` — PASS, 2/2.
- `cargo check -p ddonirang-tool --lib --offline` — PASS.
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS.
- `git diff --check` — PASS before product commit.

## Review packet

- Claim: active exponential-smoothing caller uses the shared checked Fixed64
  arithmetic owner and one ties-to-even rounding boundary.
- Primary risks reproduced: widened-term loss, component-wise saturation and
  rounding, and truncation.
- Nonclaims: this target does not close all Native/WASM Fixed64 boundary work,
  all runtime callers, release readiness, or Human PASS.
- Ready for independent target-bound review: YES.
