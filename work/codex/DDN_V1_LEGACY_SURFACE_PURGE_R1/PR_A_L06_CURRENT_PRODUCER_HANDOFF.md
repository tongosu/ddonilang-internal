# PR-A / LP-02 current producer correction handoff

## Fixed target

- Product fixed: `32369cc495d262caa899c25d172df46c58d9b39a`
- Parent: `44a38719b44ad71fb3c87505e0e980769a1b9811`
- Scope: `lang/src/normalizer.rs` only.
- Authority read-only input: internal SSOT v25.67.0 / RD-001~587; public Language SPEC v0.6.0.

## Disposition

The requested L11 surfaces (`쓰임`, `드러냄`, `공개`) have no current producer in
`currentline.rs`, `normalizer.rs`, or `tool/src/preprocess.rs`. The next actual
PR-A current-producer defect was L06: a V25 callable with parameters and a
single expression body parsed into a `Stmt::Return`, then normalized back into
the retired `되돌림` block surface.

For `SourceEpoch::V25`, the normalizer now emits the existing expression-body
surface for any one-statement return body. PreV25 keeps its previous
parameterless-only shortening behavior. Parser admission, typed AST identity,
runtime dispatch, compatibility retry, and public surface spelling are not
changed.

## Evidence

- Initial product RED: `normalizer::tests::v25_single_return_callable_emits_current_expression_surface` emitted `(x:수) 증가:셈씨 := { x + 1 되돌림. }` instead of `(x:수) 증가:셈씨 := x + 1`.
- Focused GREEN: exact test PASS; normalizer focused suite 17/17 PASS; `cargo check -p ddonirang-lang` PASS; `git diff --check` PASS.
- Mutation M1 (add parameterless gate to V25 branch): RED, then raw restore SHA-256 `a583fd7392421f5cf713d5f988eb73e2ee17ba30ce2bcb3702fa5fa3851edccc` / blob `641ee289f3b33939c234da79a16b285046efa179`, GREEN.
- Mutation M2 (invert V25 epoch selection): RED, same exact restore, GREEN.
- No test-only lowering was added. The test uses `parse_v25_and_normalize`.

## Boundary

This is canonical current-source emission only. It changes no native runtime,
WASM runtime, Workbench bridge, receipt, result, or parser admission path;
therefore no runtime native/WASM behavioral parity claim is made for this
patch. A future PR-B may audit remaining producer convergence separately.

## Review target

`32369cc495d262caa899c25d172df46c58d9b39a` is the immutable product review
target. This handoff does not claim PR-A closure, P0--P6 closure, V1 readiness,
release, activation, legal approval, or Human PASS.
