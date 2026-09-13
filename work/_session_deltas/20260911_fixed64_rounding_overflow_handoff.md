# Fixed64 rounding overflow handoff — 2026-09-11

## Immutable product target

- Product: `a950d84d1eb5897eee3be798760a4630e843eaef`
- Tree: `c756b7158f4ec2650a0c4762213f5a5fc970a8ea`
- Parent: `50cee3293f945f1a2060cf88853b110d21859ad6`
- Product paths:
  - `tool/src/ddn_runtime.rs`
  - `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
  - `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Claim

Current runtime ceiling and ties-to-even rounding reject a result whose integer
value cannot be represented by Q31.32. The typed runtime diagnostic is
`E_RUNTIME_ARITH_OVERFLOW`; the update returns before success publication.
The same Rust runtime is compiled into the rematerialized tracked WASM.

## Focused evidence

- `ddn_runtime::tests::fixed64_ceil_and_round_reject_unrepresentable_integer_results`: PASS
- `ddn_runtime::tests::fixed64_rounding_runtime_overflow_publishes_nothing`: PASS
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS after official
  `scripts/build_wasm_tool.ps1 -Profile release -Target web` and manifest rewrite.
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check`: PASS before product commit.

The one full `cargo test -p ddonirang-tool --offline` run completed with
668 passing and 5 pre-existing failures outside this change: numeric-calculus
one-ULP expectation, BOM/project parsing, supported-profile canon, and two
`ai_prompt` tests that require a missing `docs/ssot` directory in this isolated
worktree.

## Mutation evidence

Fixed source before each mutation: SHA-256
`3AD72EED42E572E2964E5420D9EDB752AE1A4DB03177B64158C7EC5073C4406D`,
blob `f1912136efff65a98285cee7b0880641e8e63e19`.

1. Restored ceil saturation: direct ceiling/rounding boundary test RED.
2. Restored round saturation: direct ceiling/rounding boundary test RED.
3. Replaced current `천장` overflow propagation with `unwrap_or(Fixed64::MAX)`:
   runtime atomicity test RED.

Each hunk was restored byte-exactly to the fixed source and the relevant
focused test was GREEN.

## Review request and nonclaims

Review the exact product target above for current runtime overflow propagation,
the absence of saturation, test coverage, and tracked-WASM freshness. This is
not a claim about every Fixed64 caller, public support, V1 readiness, release,
or Human PASS.
