# 2026-08-30 DDN V1 VC06 FU02 reused-worktree materialization guard

## Authority and custody

- persistent goal and existing single-writer branch/worktree reused
- internal CURRENT: `v25.25.0 / RD-001~469`
- public Language SPEC: `v0.6.0`
- `docs/ssot/**` and `publish/spec/**` mutation: `0`
- VC17 task-owned untracked/ignored custody preserved unstaged
- review `61c8dce6b9fbdb9921a71339ae7d788e6534f016` was ff-only bound from exact parent `86a094d556a2c87104cbb56cdc94576e8e8c0a94`

## Change

- fixed commit: `eefef28db6a9e3bf660331dca8568829e8b41c45`
- fixed tree: `6e62ed2087871c1bb8f13fc445366eee1f37e504`
- changed path: `tests/run_v1_core_text_byte_nfc_rebase_w1.py` only
- runner now distinguishes Git blob identity from checkout raw-byte identity and
  rejects non-LF or byte-different pack materialization before semantic execution
- product source, fixture/manifest, `.gitattributes`, tracked WASM, UI, SSOT and SPEC diff: `0`

## Evidence

- normal preflight: `12/12 PASS`
- CRLF mutation: exit `1`, `E_CHECKOUT_MATERIALIZATION_CRLF`
- exact restore SHA-256: `c0f201ec2c1b378047d888600e417a0033bbe00e9880e79046f2f3e32d4aae15`
- restored full runner: `GREEN 7 / RED 0 / PRODUCT_GAP 4`
- native/WASM exact: `11/11`; repeats `3`
- freshness and existing local-project CRLF unit: `PASS`
- new runner/framework/meta-test: `0/0/0`

## Disposition

- v25.25.0 impact: `UNAFFECTED`
- VC06 FU02: `READY_FOR_TARGETED_REREVIEW / REVIEW_WORKTREE_REBIND_REQUIRED`
- existing rolling reviewer/worktree only; new review task/worktree/branch: `0`
- VC06/VC12/VC04 and broad P1/V1 closure, membership/readiness/release/Human PASS remain open
