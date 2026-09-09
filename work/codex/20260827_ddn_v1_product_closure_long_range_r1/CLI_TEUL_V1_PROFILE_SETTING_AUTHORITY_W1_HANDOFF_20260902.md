# CLI/teul explicit-profile setting authority W1 handoff

## Fixed product lineage

- Baseline: `5ed9592a64e2896be7319bf20161167a6036b247`
- Product fixed commit: `279b347b3f6b1807136f6fcb465aa9fb40d3d3bd`
- Product tree: `4c0f6525d8dbd72f533e70f4ccecd5adf0031bc6`
- Direct parent relation: yes; merge count: `0`
- Changed path: `tools/teul-cli/src/cli/run.rs`

## User workflow and authority convergence

For `teul-cli run <file> --source-profile v1-core-v25`, the adapter previously
ran its retained textual `설정.마디수` extractor before invoking the shared
typed runtime.  The shared runtime already owns `configured_madi` by parsing
the typed V25 program.  The explicit-profile path now passes `None` for the
adapter-only configured value and consumes that shared authority directly.

The retained extractor and all no-profile/internal behavior remain in place;
this is not physical teul deletion, public command promotion, executable
naming, package retirement, or legacy alias policy.

## Evidence

- Existing run regression extended, no new runner/pack/framework:
  `supported_profile_run_uses_shared_v25_authority_and_fails_legacy_closed`.
- Positive user source now supplies `설정 { 마디수: 2. }` with no CLI tick
  override.  It produces the two expected `2` result rows through the shared
  V25 runtime; the pre-existing trace/state rows remain accepted output.
- The same test preserves legacy `=` fail-closed behavior under
  `v1-core-v25`.
- Risk mutation: a temporary `E_TEST_PRIVATE_SETTING_PARSER_REACHED` sentinel
  plus the former unconditional adapter call caused actual RED (exit `101`).
  The final source SHA-256 after exact restoration was
  `2BE6C462F0C4973A86E53B41E379F68646AAF1F506B51F81C96BE3270334206A`;
  final focused GREEN passed (`1 passed`, `1032 filtered`), residue `0`.
- Existing tracked-WASM supported-ingress parity was reused unchanged:
  `P1A_WASM_PARITY_PASS cases=11 deterministic_repeats=5 partial_summary=0`.
- `git diff --check` passed before fixed commit.

## Scope boundaries

- Product source/test/pack/WASM/UI/SSOT/public-SPEC changes outside the one
  path: `0`; tracked-WASM refresh: `0`.
- New dependency/test artifact/pack/runner/meta-test: `0`.
- Current authority was read-only internal SSOT v25.50.0 / RD-001~551 and
  public Language SPEC v0.6.0.
- Required V1 CLI build/test/pack/publish dependency and physical teul
  retirement remain separately audited gates.  Historical and
  internal/deferred teul custody remains intentionally preserved.
- No independent reviewer was created or dispatched.  This fixed target may
  be bundled with the next coherent CLI milestone by management.

No P0-P6 whole closure, V1 membership/readiness/release/activation/legal,
publication-rights closure, or Human PASS is claimed.
