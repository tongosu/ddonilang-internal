# SOURCE_COORD shared authority W90 handoff

## Fixed identity

- authority: internal SSOT v25.49.0 / RD-001~543 (read-only), public Language SPEC v0.6.0
- implementation parent: `f566727ac0ebd63b2b1bd67adc60c6ee005fd858`
- implementation fixed: `bfe1b67d917751c0e0107d202c5678c51f7388bd`
- implementation tree: `fc95c39a2afdf50ee6e2d0f830d7cbe8dc09e005`
- merge count from immutable PathIR P0 handoff `5806eecf64af5c69d76ea65e527ecd4a847f48fc`: 0

## Product behavior

The language crate now owns the typed UTF-16 position projection consumed by
both the official LSP frontdoor and Workbench project-authoring ranges. The
previous LSP-only implementation counted Unicode scalar values, so a symbol
after `🙂` was reported at character 1 instead of the LSP-required UTF-16
character 2. The fixed implementation keeps parser byte offsets authoritative
and projects zero-based UTF-16 positions without defining a public wire schema,
snapshot hash, UI copy, or new source syntax.

Exact product paths:

- `lang/src/source_coordinate.rs`
- `lang/src/lib.rs`
- `tool/src/lsp/server.rs`
- `tool/src/project_authoring.rs`

## Verification

- product RED: `lsp_position_uses_utf16_code_units_for_non_bmp_prefix` failed
  with actual 1 / expected 2, exit 101.
- `cargo test -p ddonirang-lang --lib`: 369/369 PASS before the final
  no-semantics cleanup; final focused source-coordinate test 1/1 PASS.
- LSP module tests: 2/2 PASS.
- Workbench/project-authoring UTF-8/UTF-16/combining/emoji/CRLF/BOM test: 1/1 PASS.
- `cargo test -p ddonirang-tool --lib`: 586 PASS, 2 pre-existing isolated
  checkout environment failures because `docs/ssot` is intentionally absent;
  both failures are `ai_prompt` SSOT-directory reads and are outside this diff.
- risk mutation: replace `.encode_utf16().count()` with `.chars().count()`;
  RED exit 101, exact restore, focused GREEN. Final restored module SHA-256 is
  `a4fb2527ccc6db7ff05efe4c6ba75e2f119c9e7e613593018ab6e0ec41b99672`;
  mutation residue 0.
- `git diff --check`: PASS.

Official tracked-WASM freshness remains fail-closed with
`source_file_count/source_tree_sha256/source_files mismatch`, because the new
language source has not been incorporated into the frozen tracked-WASM family.
No tracked-WASM byte or manifest was changed. This is
`WASM_REFRESH_AND_BUNDLED_REVIEW_REQUIRED`, not a native or Workbench product
failure and not a claim of native/WASM closure.

## Gate impact

- C0/C1/C2/C3/C4/C5/C7/C8: unchanged from W89.
- C6: native LSP and Workbench authoring now consume one UTF-16 projection
  authority; tracked-WASM refresh/parity remains open.
- user workflow changed: non-BMP Korean-source definition/reference positions
  are correct and consistent across LSP and Workbench authoring.
- reused tests: existing lang full regression, tool full regression, existing
  project-authoring coordinate test, official freshness gate.
- new test artifacts: 0; new pack/runner/meta-test/reviewer/worktree: 0.

The verified historical P5 fixed review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
with report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`
remains bound to its exact target. This W90 successor does not inherit or
broaden that PASS.

## Nonclaims and next gate

This is `SOURCE_COORD_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`. It does not
claim tracked-WASM freshness, public coordinate-wire approval, whole C0~C8,
PathIR public-contract closure, VC17 exact landing, P5/P6 closure, teul physical
retirement, V1 membership/readiness/release, activation, legal approval, Owner
Human Smoke, or Human PASS.

Next safe gate: refresh and verify the existing tracked-WASM family together
with the next coherent product/release milestone, then use the existing rolling
reviewer only. No standalone review task is created by this handoff.
