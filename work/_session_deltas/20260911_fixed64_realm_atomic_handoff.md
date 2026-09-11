# Fixed64 realm atomic-batch handoff

## Claim

`MultiRealmManager` now treats each Fixed64 batch as an atomic current-product
transition.  A representable batch commits all candidate realms; an overflow
returns `E_REALM_ARITH_OVERFLOW realm.value` without advancing any realm's
resource, state hash, RNG, or madi.

## Fixed target

- Product commit: `4306c0f6009b17fa43af8201bd96da825caf02b5`
- Tree: `a959833f979fda117d6756d083b856577ff81e35`
- Parent: `bf22e4823721a4a86d7cec898089b1c0d3a3347c`
- Product path: `core/src/realms.rs`

## Verification

- `cargo test -p ddonirang-core realms -- --nocapture` — PASS (3/3)
- `cargo test -p ddonirang-core` — PASS (137/137)
- `cargo check -p ddonirang-core --offline` — PASS
- `git diff --check` — PASS before product commit

## Mutation evidence

- M1: replaced `checked_add` with `saturating_add`; the single-realm overflow
  assertion was RED because the step returned success and advanced `madi`.
- M2: committed each sequential candidate immediately; the multi-realm overflow
  assertion was RED because realm 0's state hash changed before realm 1 failed.
- Exact restored source after both mutations: SHA-256
  `06529C87BD974185843CF0C52A4732344C0990279D6A379A6A52910CDDD558B4`,
  Git blob `92e862485b1c2740b4bbb2e86a547d393fe2960e`.

## Review request and nonclaims

Review the exact product target above for checked arithmetic, all-realm atomic
commit, and deterministic Seq/Rayon behavior.  This does not claim broader
Fixed64 caller closure, V1 readiness, release, public support, or Human PASS.
