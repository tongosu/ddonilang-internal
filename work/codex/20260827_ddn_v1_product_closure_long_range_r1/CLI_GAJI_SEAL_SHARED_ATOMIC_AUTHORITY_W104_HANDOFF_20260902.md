# CLI Gaji Seal Shared Atomic Authority W104 Handoff

## Identity

- Authority: internal SSOT v25.49.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline and direct parent: `910a4bc78521ea36de14cc574fca07d6812984e6`.
- Product fixed: `f57315ca88bb705f8d0bfa73ce4bb61351c77fd1`.
- Fixed tree: `92897efe9f07912495a4bed0d59ff42df4a08af9`.
- Merge count: 0.
- Goal: persistent `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains ACTIVE.

## User workflow and authority change

The existing `teul-cli gaji seal --input ... --out ...` workflow now delegates
request decoding, local-project artifact construction, directory population, and
atomic publication to `ddonirang_tool::gaji_seal_workflow`. The teul command is
an adapter and no longer owns a private temp-directory/rename/materialization
implementation. Existing command spelling and successful stdout are unchanged.

The shared workflow preserves immutable-target failure and uses the existing
shared `local_project` builder and `artifact_output` atomic directory publisher.
A population failure publishes no target and leaves no staging residue.

## Exact fixed diff

1. `tool/src/gaji_seal_workflow.rs` — 4,774 bytes / SHA-256 `582537ae8a25bc9bb8c619f47a6c6736adcb7de0082ef5d7ad98019130be4843`.
2. `tool/src/lib.rs` — 3,855 bytes / SHA-256 `ea533343cc91af5d9242bfb01dc93d50ad4d8a19e1c1f00c60ec5f3bbf3583f1`.
3. `tools/teul-cli/src/main.rs` — 570,184 bytes / SHA-256 `62bd120246ea105c724e412d4a656202d9c36ba9320a9102ebe3408573729906`.
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` — 29,964 bytes / SHA-256 `e52be745d4bbffc7e8c0c70e785d08fc056b25d762895e2437b3fecaf3d68036`.

Tracked WASM binary was not rebuilt or changed: 5,579,392 bytes / SHA-256
`6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e`.
The manifest source inventory was refreshed because the non-wasm shared module
and `lib.rs` source identity are new; official freshness is GREEN.

## Verification

- Shared workflow focused tests: 2/2 PASS.
- Existing local-project gaji extraction/lifecycle tests: 5/5 PASS.
- Existing local-gaji artifact/remix/bounds tests: 3/3 PASS.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- Actual teul workflow: two independent seals, 4/4 files each, identical paths
  and SHA-256 values; package identity
  `9830235db855ec491f980477f8470ad5caa53613a8e584cda155c92787783deb`.
- Existing-target rerun: exit 1 / `E_GAJI_SEAL_IMMUTABLE`; prior 4 files byte-preserved.
- Injected population failure: target publish 0 and residue 0.
- Immutability guard bypass mutation: RED exit 101; exact source restore SHA-256
  `582537ae8a25bc9bb8c619f47a6c6736adcb7de0082ef5d7ad98019130be4843`;
  final focused GREEN 2/2.
- Full tool library: 611 PASS + the same 2 isolated-worktree environment failures
  caused by absent `docs/ssot` in `ai_prompt`; no new product regression.
- Official tracked-WASM freshness: PASS.
- `git diff --check`: PASS.

NEW_PACK=0, NEW_RUNNER=0, META_TEST=0, NEW_REVIEW_TASK=0,
NEW_REVIEW_WORKTREE=0. Two inline product tests exercise the shared workflow;
they do not test another test or report.

## Review and status boundary

The already-bound P5 review commit
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` is an ancestor and its report
recomputes to SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`.
The stale reviewer-handle blocker is therefore removed. W104 is implemented
under review and is proposed as part of the coherent W102+W103+W104 rolling CLI
authority bundle; management must decide when to dispatch the existing rolling
reviewer.

`doc verify` remains slice-locally blocked by missing fixed corpus and its old
private State-hash golden. Canon fixit convergence remains slice-locally blocked
because the shared parser lacks the existing teul rich diagnostic/byte-to-line
physical contract. Neither blocker is a whole-goal impasse.

## Nonclaims

This does not close C0~C8, all teul private authority, teul physical retirement,
public command membership, public executable/package naming, P0~P6, V1
membership/readiness/release/activation, PathIR public ingress, VC17 exact
landing, or Owner Human Smoke/Human PASS.
