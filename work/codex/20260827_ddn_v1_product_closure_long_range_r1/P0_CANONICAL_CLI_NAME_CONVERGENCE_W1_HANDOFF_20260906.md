# P0 canonical CLI name convergence W1 handoff

## Fixed target

- Base: `e802c92a3f3d290f0f857f263aeb2a19ef868d7b`
- Product fixed: `d96d638ed55f29e1b51813318b93e0d635ca9bdc`
- Product tree: `9e57d4bfd83fde70ce78d3a5a86d2214f1cfbd23`
- Authority observed read-only: internal SSOT v25.56.0 / RD-001~560; public Language SPEC v0.6.0.

## Claim for review

`ddonilang` and `또니랑` are canonical Native CLI target names and `ddonirang` is a compatibility alias. All three targets use `tool/src/bin/ddonirang.rs`; the entry does not branch on argv[0]. The ordinary supported ingress is now invoked by default through `ddonilang`.

## Changed paths

- `tool/Cargo.toml`
- `tool/src/bin/ddonirang.rs`
- `tests/run_v1_core_supported_ingress_w1.py`
- `scripts/build_windows_x64_public_candidate.ps1`

## Evidence

- Three target build: PASS.
- Existing supported-ingress runner: PASS: native=8, native/WASM exact=2, WASM cases=11, canonical/Korean parity=2, compatibility alias parity=2.
- WorkCost exact ledger regression: PASS (1 selected test).
- Mutation: remove `ddonilang` bin target -> RED exit 101; exact restore -> all three target builds GREEN.
- Windows candidate: PASS. `ddonilang.exe` SHA-256 `a9dcd7c81c3dd4f0ce272493403c92e0de7763379ff30a01b5577e9bd0e96013`; `ddonirang.exe` `af2809e0166450c39bb0b9a9bd03b9e6b7639071fe4c63f91400ac167de762cd`; `또니랑.exe` `54f388fe8c0f9aa4828763f52088bf1fbcce25cebbf228ff9790642f7f196544`. All are 7,146,496 bytes; candidate forbidden-path occurrences=0.

## Scope and nonclaims

This is P0-A implementation pending independent review. It does not retire `tools/teul-cli`, establish D5/D6, close P0, decide public package composition, or claim V1 readiness, release, activation, legal clearance, or Human PASS.
