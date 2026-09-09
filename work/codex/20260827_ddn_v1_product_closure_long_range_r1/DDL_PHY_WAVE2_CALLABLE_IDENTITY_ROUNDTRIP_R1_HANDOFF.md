# DDL Physical Wave 2 Callable Identity Roundtrip — Handoff

## Fixed target

- Product fixed commit: `02e97c9281a3e7ce43fea74b0a7c14d36ec0dff4`
- Parent: `fe7ba526132ccc5947769be74f75fa17dfe1bf26`
- Tree: `d92b2309f97b5210f7f6b64e8480c8a854635d72`
- Direct lineage from Wave 1 correction `f3507fd9591baba7f91bcf6f1a28cbdbdebd4e1c`: yes; merge commits: 0.

## Scope and behavior

The internal-only `.ddl` and `.옮김` Wave 2 projection admits exactly Korean and Japanese translations of one registered pure callable. It binds a shared `DefinitionIdentity`, ordered `ParamPinIdentity`, parameter and result `TypeIdentity`, callable kind, and registry-owned relation identities. Localized names and relation spellings remain presentation only. Callable `:={...}` is represented as `OmittedPayload::CallableBody`; it is neither an ordinary DDN surface nor executable runtime input.

Changed product paths are exactly:

- `lang/src/ast.rs`
- `lang/src/canonicalizer.rs`
- `lang/src/ddl.rs`
- `lang/src/lib.rs`
- `lang/tests/ddl_callable_identity_roundtrip.rs`

No `tool/**`, parser, WASM, CLI, runtime, public wire, SSOT, or public SPEC path changed.

## Evidence

- Wave 2 focused coverage: P01–P12 and N01–N18, 5/5 tests PASS.
- Wave 1 regression: 11/11 PASS.
- Full `cargo test -p ddonirang-lang`: 373 unit + 5 Wave 2 + 11 Wave 1 + 6 V25 pack tests PASS.
- `cargo check -p ddonirang-lang`: PASS.
- `git diff --check`: PASS.
- Canonical output is LF-only and `parse → canon → parse → canon` byte-stable for both extensions and reversed section presentation.

## Risk mutations and restoration

All mutations used `lang/src/ddl.rs`; normal source identity before and after each restore is SHA-256 `154357DAA8750EA71E78FFD09DE0DE40A3D9E1C072A52231FC54EE17056B0034`, Git blob `d0391a8f513661de1fa118bc4ad8677666e9e713`.

1. M1 removed cross-language ParamPin identity comparison. N11 duplicate-pin input was accepted, producing focused RED; exact restore followed by GREEN.
2. M2 removed result `TypeIdentity` comparison. Japanese result-identity mismatch was accepted, producing focused RED; exact restore followed by GREEN.
3. M3 disabled exact callable declaration/omission matching. A value initializer was admitted as a callable projection, producing focused RED; exact restore followed by GREEN.

Mutation residue is zero.

## Review boundary

This target is ready for one fixed-target independent review. It does not claim full DDL support, runtime/CLI/WASM/wire/IDE support, public LanguageProfile admission, V1 closure/readiness/release, or Human PASS.
