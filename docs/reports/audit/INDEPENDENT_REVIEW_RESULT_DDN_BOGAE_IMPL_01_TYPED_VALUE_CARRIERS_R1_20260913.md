# BOGAE-IMPL-01 Typed Value Carriers — Independent Review R1

## Claim and immutable target

- Claim: `BOGAE-IMPL-01` typed value carriers only.
- Product commit: `8c0781d1ac10dabea4b4e5699f6b26823bc23dc4`
- Product tree: `734f262fe6dd1e8e92017eeaf0502e3a53f035be`
- Product parent: `1ba5696ee7a597e9f2452c8a85e02a8572a19d18`
- Handoff commit: `6fcec4911b2813ea8945e405c9701ca1c339595b`
- Handoff tree: `970ee4156e5dab2ddc1cce4933c6766c81a34231`
- Handoff parent: `8c0781d1ac10dabea4b4e5699f6b26823bc23dc4`
- Review base: detached, clean handoff worktree; a review-only branch was created solely to preserve this direct child record.

The product is the direct parent of the handoff. The product diff contains the fourteen claimed shared-language, runtime, and direct LSP-consumer paths; the handoff itself contains only reports/session custody files. No product, WASM, manifest, SSOT, or public-SPEC file was modified by this review.

## Authority impact

The live `CURRENT` observed during review is v25.80.0. Its successor material did not alter the narrow typed-carrier interpretation reviewed here. This verdict remains bound to the immutable product/tree/parent above, not to any later product or release state.

## Independent gates

All commands were run offline with a reviewer-owned external Cargo target directory.

| Gate | Result |
| --- | --- |
| `cargo test -p ddonirang-lang bogae_exact_provider_roles_are_canonical_and_roundtrip --offline` | PASS |
| `cargo test -p ddonirang-tool bogae_typed_scene_view_and_composition_execute_without_renderer --lib --offline -- --nocapture` | PASS |
| `cargo test -p ddonirang-tool bogae_scene_profile_mismatch_fails_before_publication --lib --offline -- --nocapture` | PASS |
| `cargo test -p ddonirang-tool bogae_composition_requires_exactly_one_primary_without_partial_publication --lib --offline -- --nocapture` | PASS |
| `cargo check -p ddonirang-tool --lib --offline` | PASS |
| `cargo check -p ddonirang-tool --lib --features wasm --target wasm32-unknown-unknown --offline` | PASS |
| review-tree `git diff --check` | PASS |

Static and dynamic review confirmed that the parser maps providers by exact name, rejects unknown and duplicate roles, and emits the declared `expected_roles` order rather than source order. Runtime operates on typed Bogae values; incompatible scene profiles and multiple primary relations fail before the candidate run is published. The focused failure tests assert absence of output and relevant runtime state, satisfying this target's no-partial-publication boundary.

## Independent scratch mutations

Scratch mutations were made in a separate worktree at the immutable product commit. Each was restored to the exact fixed Git blob and verified GREEN.

| Mutation | Actual RED | Restore | GREEN |
| --- | --- | --- | --- |
| Reverse `expected_roles` canonical emission in `lang/src/parser.rs` | Canonical-role-order test failed because the expected canonical named-pin order changed. | blob `0597a281aa22d400105746337b6b242dab5c7145`; SHA-256 `730058C658A0A91DD03F6DEB95D639D698F3BAA734A455B6E99DF19880A7092C` | canonical-role-order test PASS |
| Remove scene-element/profile compatibility gate in `tool/src/ddn_runtime.rs` | `bogae_scene_profile_mismatch_fails_before_publication` failed: the invalid Plane2 scene succeeded. | blob `95369749f0757502906fa9f13558f89baae5a4f2`; SHA-256 `00D5618EFF555890787FCC9597D97E3621989D22AD80795CA9F1BF76ABF2B9B2` | profile-mismatch atomicity test PASS |
| Remove duplicate-primary gate in `tool/src/ddn_runtime.rs` | `bogae_composition_requires_exactly_one_primary_without_partial_publication` failed: multiple primary relations succeeded. | same runtime blob and SHA-256 above | duplicate-primary atomicity test PASS |

After restoration, scratch tracked diff and staged state were zero; the reviewer tree had only this review record before commit.

## Verdict

`PASS_TARGET_BOUND`

The verdict closes only `BOGAE-IMPL-01` at the exact product/tree/parent and handoff identities listed above: `CLOSED_TARGET_BOUND` for this target only.

## Nonclaims

This review does not claim renderer inventory or rendering, projection/hash-matrix closure, full-headless lifecycle, tracked-WASM projection behavior, Workbench persistence, release readiness, public support, or Human PASS.
