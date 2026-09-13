# PG-CLI-00 root Binding/Rebinding product handoff

## Fixed target

- Product: `dae9389628f80cd376d863aec9935829f285b532`
- Tree: `75a63c2ea0f267b83450105b4d4f4408dc092fd0`
- Parent: `d1130d38c077c5952b451992d5bf4d9e8a7a6be5`
- Claim: the current V25 frontdoor preserves top-level `<-` as root `Stmt::Mutate`, executes it in source order without synthesizing a callable, and fails a root rebinding value-category mismatch before a run result is published.

## Product paths

- `lang/src/ast.rs`
- `lang/src/canonicalizer.rs`
- `lang/src/normalizer.rs`
- `lang/src/parser.rs`
- `lang/tests/v25_definition_binding_pack.rs`
- `tool/src/ddn_runtime.rs`
- `tool/src/runtime_surface.rs`

## Primary evidence

- Immutable L0 input: `docs/EXAMPLES/DDN_네모쌓기_쉬운_CLI_EXACT_R1.ddn`
  - SHA-256: `2ec907853a3ff7a880e663ddbc127d40960709616da78df6b49b371fa6ad7810`
- Source-built `ddonilang`, `ddonirang`, and `또니랑` produced the same final row `{왼쪽높이:1, 가운데높이:3, 오른쪽높이:1, 점수:50, 차례:5}` and state hash `blake3:4d81fd3bb93cc2c89c3fd4de6c68dbecc8e587e94764aac8c124ddaa3cd190f4`.
- The execution envelope retained the immutable L0 SHA-256; no synthetic `매틱` source was supplied to the runtime.
- V25 root binding canonicalization is parse/canon/reparse byte-stable.

## Gates

- `cargo test -p ddonirang-lang --test v25_definition_binding_pack --offline` — PASS (6/6)
- `cargo test -p ddonirang-tool --lib v25_ --offline` — PASS (8/8)
- `cargo check -p ddonirang-lang -p ddonirang-tool --offline` — PASS
- `git diff --check` — PASS

## Mutation / exact restore

### M1 root admission removal

- Mutation: remove `TokenKind::Arrow` from the root-statement classifier.
- RED: exact L0 source rejected at byte span `13..14` with `E_PARSE`.
- Restore: `lang/src/parser.rs`, SHA-256 `6ba3cd5594a45fed73bf4713ce4715b6c9eb86f59a72ccf1689377f652710ed8`, Git blob `0a04f5b3651725a6bb35bd52f69d0bdedee7ac84`.
- GREEN: source-built `ddonilang check` accepted the exact L0 source.

### M2 root execution removal

- Mutation: bypass root statement execution.
- RED: L0 run returned `E_RUNTIME_EXECUTION` because `매마디` did not exist; no success result was returned.
- Restore: `tool/src/ddn_runtime.rs`, SHA-256 `143851d79f3508891b896ea0448664110d9ee4b4ac7dd6486786ca54e6dc4ec7`, Git blob `5870a521aa265da54353a4a79709c10fb47a3919`.
- GREEN: exact L0 run succeeded.

### M3 root type guard removal

- Mutation: bypass root rebinding category guard.
- RED: `v25_root_rebinding_type_mismatch_fails_before_any_run_output_is_published` failed because numeric-to-string rebinding returned success.
- Restore: `tool/src/ddn_runtime.rs`, same SHA-256 and blob as M2.
- GREEN: focused mismatch test passed with `E_ROOT_BINDING_TYPE_MISMATCH`.

## Review packet

- Requested verdict: `PASS_TARGET_BOUND | FAIL_TARGET_BOUND | INCONCLUSIVE_TARGET_BOUND` for the exact product target above.
- Check root parse classification, raw-source execution binding, source-order rebinding, and no-success failure behavior.
- Nonclaims: no SSOT/SPEC/release/public-support/Human PASS claim; no WASM or Workbench parity claim for this PG-CLI-00 target.

## Next exact action

Start PG-CLI-01 `차림[...]` / `(T)차림` only from this handoff successor after its exact product lease is bound.
