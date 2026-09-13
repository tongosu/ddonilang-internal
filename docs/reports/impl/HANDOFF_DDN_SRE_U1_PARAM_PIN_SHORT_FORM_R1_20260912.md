# SRE-U1 ParamPin short form — implementation handoff

## Fixed target

- Product commit: `3e774b85bde11d886bf62e893b718a5e9d67ad8f`
- Product tree: `bfce6524bcb96a92522592a8903d656d5055d2b6`
- Product parent: `61c0e3d8c2a39d660a68f9742a4956bda26320b3`
- Claim: `PRODUCT_FIXED_PENDING_INDEPENDENT_REVIEW`

## Product paths

- `lang/src/ast.rs`
- `lang/src/parser.rs`
- `lang/src/canonicalizer.rs`
- `lang/src/normalizer.rs`
- `lang/src/lib.rs`
- `tool/src/ddn_runtime.rs`

`ParamPin` now retains the existing public pin identity separately from its
local binder identity, binder span, and authored full/short provenance. The
short form expands to the same name on both axes. Calls keep using the public
pin while lexical body and runtime locals use the binder. The normalizer emits
the short form only for same-spelling pins; distinct full spelling is retained.

## Fixed blobs and SHA-256

| Path | Git blob | SHA-256 |
| --- | --- | --- |
| `lang/src/ast.rs` | `c177a4787caed2a7a9db0a47d1a72185dc0de1f2` | `BC233FEEF8A52F51A676B462647083E30392C7329F996F926EEAF488808F2484` |
| `lang/src/parser.rs` | `2a4e12d036ab4db98ce38f4a16027cb65f2574c9` | `AF24C24166AE8F3099C892DEA1ABCC609D76357F234891B9B5F9AFE1FACB2E13` |
| `lang/src/canonicalizer.rs` | `9bcf11ec4fcada5a2ce62bd4f3565424bb99570f` | `245FC237E2F75D47A7A776A558E3235692C89CEAE45612A90FFA98633E055963` |
| `lang/src/normalizer.rs` | `91c187c511961b4e3ba38d4eed6883e369998995` | `E48AB82A7B3BC0F4633A46B4B68C35C926D3A2DD5E76A592C52F365EE3B1E67D` |
| `lang/src/lib.rs` | `129d3f97957a1342331719ab1c0f8dddd76fdadb` | `3D5D142F3A76E40C7D1A6902AE1F04E453567B35FDE963C8E9A7292DBC6CB94B` |
| `tool/src/ddn_runtime.rs` | `e5ed6eb420758202cdda97b8f5c6ce64dfe4e0f2` | `A6A746F99925B3D0608F90A1903C2B911C9191BC5B432CF0BA29475A40547EEA` |

## Primary gates

- `cargo test -p ddonirang-lang sre_ --offline` — PASS (3)
- `cargo test -p ddonirang-lang --offline` — PASS (377)
- `cargo test -p ddonirang-tool sre_public_pin_binds_the_distinct_local_binder_at_runtime --offline` — PASS
- LSP signature-help, document-symbol, semantic-token integration tests — PASS (9)
- `cargo check -p ddonirang-lang -p ddonirang-tool --offline` — PASS
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --cached --check` — PASS before product commit

The package-wide wasm check selects host-only CLI binaries and fails on their
existing `cfg(not(target_arch = "wasm32"))` APIs; the wasm library check is the
applicable product bridge gate. A tracked-artifact rematerialization is not
claimed by this target.

## Mutation evidence

1. Removing the same-name shortening guard made `값=값` appear in canonical
   source; `sre_same_spelling_full_and_short_expand_to_the_same_typed_contract`
   went RED. Restored `lang/src/normalizer.rs` blob `9f43c4137943cfc242815f4884dd36891bc0a24c`, SHA-256
   `2521F83E0870E675D57D6CCC9114E41A6030075852ED59ED6CDF07EA811ADAB0`; GREEN.
2. Removing short-to-local-binder expansion caused the shared runtime source to
   fail with `정의되지 않은 변수: 값`. Restored `lang/src/parser.rs` blob
   `0672535f9969e294fe667f361815163d21e06674`, SHA-256
   `F469BD915DD8AA07198A0036BE5C1A0FB4F8AD7BB34D169DB89F028B5E11C6B3`; GREEN.
3. Removing duplicate/capture validation allowed a duplicate public pin through
   parse, making the negative contract test RED. Restored the same parser blob
   and SHA-256; GREEN.

## Review focus and nonclaims

Review the public-pin call binding versus local-binder body scope, exact
same-name shortening, distinct-name preservation, and duplicate/capture
fail-closed behavior. No new lexer token, public wire, identity family,
compatibility fallback, SSOT change, public-SPEC change, release claim, or
independent PASS is claimed.
