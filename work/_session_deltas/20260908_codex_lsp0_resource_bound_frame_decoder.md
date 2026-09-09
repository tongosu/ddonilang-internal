# 2026-09-08 LSP-0 resource-bounded frame decoder

## Status

- `LSP0_RESOURCE_BOUND_FINDING_CORRECTED=YES`
- Product fixed: `54070b7362dd48f9c977ef835bb0f36fc478641d`
- Handoff pending as a separate docs-only commit.

## Change

- Added bounded header, declared body, and pending-frame guards to the existing
  JSON-RPC `FrameDecoder`.
- Added poisoned fail-closed behavior after limit rejection.
- Added RB02/RB03/RB06–RB12 Rust assertions and endless-header and oversized-
  declared-body checks to the existing checker.
- No semantic LSP surface or external custody path changed.

## Evidence

- Focused Rust: 22/22 PASS.
- Existing checker: normal streaming lifecycle, truncation/malformed input,
  endless header, and oversized declared body all PASS.
- CM1 and CM2: RED → exact restore hash
  `d93eebb3775388e78af39a16ccd8d4f9369a3c6c2637a8c3381179ec80ac2d1f` → GREEN.
- Validation snapshot used because shared checkout Cargo compilation reaches
  pre-existing foreign `lang/**`/shared `core` mismatches first.

## Next action

Send the resource-bound correction and handoff to the same reviewer for the
resource-only rereview. Do not reopen the already reviewed streaming behavior.
