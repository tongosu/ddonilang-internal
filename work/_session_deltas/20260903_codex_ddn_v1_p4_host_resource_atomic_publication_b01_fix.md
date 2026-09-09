# DDN V1 P4 B-01 atomic publication correction — session delta

Status: Pending management verification and same-reviewer rereview.

- Live authority: internal SSOT v25.53.0 / RD-001~553, public SPEC v0.6.0 (read-only).
- Base `d7d157bb5e82496adc4a37f61b29229681c3fde1`; initial fixed `d4b7f77cd8ef977e8da36fa9bf6b82edc47158e1`; two-doc handoff `f8d0ef1d22bcf463b37d785d1ace1308894083f2`; portability follow-on fixed `f49fbe19a3a795fa216b7e2ca145a09276ec10f0`; merge `0`.
- Fixed paths: `tool/src/artifact_output.rs`, `tool/src/bin/ddonirang.rs` only.
- The old B-01 path wrote transcript then bundle separately. The correction preflights all record/project output targets before runtime and publishes the complete set once through `artifact_output::write_artifact_set_atomic`.
- Normalized duplicate/overlap and stale staging are fail-closed. Existing predecessor files survive invalid target and injected second-publication failure with no partial publish.
- Tests: artifact output `9/9`, official CLI `12/12`, host-resource `3/3`, local-project host binding `1/1`, native/WASM host-resource parity `1/1`, cargo check PASS, diff check PASS.
- Existing test modules only; new pack/runner/framework/meta-test `0`. Product source semantics, tracked WASM, SSOT, SPEC, UI, teul-cli, membership, and release state unchanged.
- The follow-on portability commit changes only the existing artifact-output test assertion; runtime behavior is byte-unchanged from `d4b7f77c`.
- Ready for existing rolling reviewer rereview only after management binds the handoff. Current status remains `P4_SHARED_HOST_RESOURCE_CONTRACT_REVIEW_FAIL_B01` until that verdict.
