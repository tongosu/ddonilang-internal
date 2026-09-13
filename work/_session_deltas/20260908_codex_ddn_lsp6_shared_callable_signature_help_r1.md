# DDN-LSP6-SHARED-CALLABLE-SIGNATURE-HELP-R1

## Authority and custody

- `IMPLEMENTATION_BASE`: `44a38719b44ad71fb3c87505e0e980769a1b9811`
- LSP4/LSP5 review state was not changed or re-run. Their fixed targets remain the predecessor review targets.
- Worktree: `I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828`
- `tool/src/lib.rs`: unchanged; no new lib.rs lease was required.
- Foreign dirty paths were preserved and never staged.

## Product implementation

Changed only these task paths:

- `tool/src/lsp/signature_help.rs` — parser-backed active-call selection, local/stdlib canonical signature presentation, ParamPin order, UTF-16 position conversion, snapshot/version binding, and fail-closed behavior.
- `tool/src/lsp/symbol.rs` — made the existing canonical local signature/type presentation helpers reusable by signature help.
- `tool/src/lsp/mod.rs` — registered the signature-help module.
- `tool/src/lsp/server.rs` — initialize capability, request route, stale version/snapshot guards, and response serialization.
- `tool/tests/lsp_signature_help.rs` — SH01-SH12 focused coverage.
- `tests/run_lsp0_transport_document_sync_check.py` — persistent transport signatureHelp-before-EOF check.

No LSP-only parser, alias, registry, callable identity, or separate semantic implementation was added.

## Verification

- Focused: `cargo test -p ddonirang-tool --test lsp_signature_help --offline` — GREEN, 2 passed after exact restores.
- LSP regressions: `cargo test -p ddonirang-tool --test lsp_signature_help --test lsp_references --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline` — GREEN: 33 tests passed.
- Black-box: `$env:CARGO_TARGET_DIR='I:/home/urihanl/ddn/codex/build/lsp0-transport-document-sync-r1'; python tests/run_lsp0_transport_document_sync_check.py` — PASS, including `SH15_BLACKBOX_SIGNATURE_HELP_BEFORE_EOF=PASS`.
- `git diff --check` — PASS for the task diff.
- Direct `rustfmt --edition 2021 --check` reported pre-existing formatting drift in foreign dirty `tool/src/lsp/mod.rs`/`server.rs` and unrelated server code; the new `signature_help.rs` itself has no formatter diff. No formatter rewrite was applied.
- `cargo check -p ddonirang-tool --offline` — blocked before tool validation by pre-existing foreign `lang` dirty API mismatch: `UnitDim::AXIS_COUNT`, `UnitDim::exponents`, `UnitDim::from_exponents`, and `Fixed64::parse_decimal_exact` missing in `lang/src/model.rs`/`parser.rs`.
- Clean validation snapshot at handoff `48452011`, with a dedicated target directory, ran `cargo check -p ddonirang-tool --offline` — PASS. The temporary snapshot and target directory were removed after verification.

## Mutation evidence

Each mutation was applied alone, the unchanged test was run for RED, the original bytes were restored immediately, and the restored hash was checked before the next mutation.

### M1 active parameter guard

- Target/hunk: `tool/src/lsp/signature_help.rs`, `active_parameter: active_parameter as u32` changed temporarily to `active_parameter.saturating_sub(1) as u32`.
- Original SHA-256: `A4C62370C8FECEBBB1F91C676C189C8DBE3C239D12495D8FF6EA4A8898C3B483`.
- RED: focused test failed both local and stdlib second-argument assertions; core output `left: Number(0), right: 1`.
- Restore SHA-256: `A4C62370C8FECEBBB1F91C676C189C8DBE3C239D12495D8FF6EA4A8898C3B483`.
- Restore GREEN: focused signature-help tests 2 passed.

### M2 UTF-16 position conversion

- Target/hunk: `tool/src/lsp/signature_help.rs`, `position_to_byte_offset(source, position, encoding)` changed temporarily to use `PositionEncoding::Utf8`.
- Original SHA-256: `A4C62370C8FECEBBB1F91C676C189C8DBE3C239D12495D8FF6EA4A8898C3B483`.
- RED: focused test failed with `SignatureHelp(InvalidPosition(ContinuationByte))`; the nested/stdlib position assertion also returned `Null` instead of the expected signature.
- Restore SHA-256: `A4C62370C8FECEBBB1F91C676C189C8DBE3C239D12495D8FF6EA4A8898C3B483`.
- Restore GREEN: focused signature-help tests 2 passed.

### M3 stale version guard

- Target/hunk: `tool/src/lsp/server.rs`, signature-help stale version comparison changed temporarily from `requested_version != snapshot.version` to `requested_version == snapshot.version`.
- Original SHA-256: `9199A4F9E3392E338E130ED52E3DE42C047EDC7860B3025D2BEFD6D8711FD75C`.
- RED: focused tests rejected current version `1` with `-32801 signature help document version이 stale합니다`, proving the guard is exercised.
- Restore SHA-256: `9199A4F9E3392E338E130ED52E3DE42C047EDC7860B3025D2BEFD6D8711FD75C`.
- Restore GREEN: focused signature-help tests 2 passed.

## Handoff

- Product commit and docs-only handoff commit are separate.
- Author and committer: `tongosu <tongosu@myarts.kr>`.
- Prohibited trailers: `0`.
- Push: `NO`.
- Next safe LSP unit: `OWNER_SELECTION_REQUIRED`; no unapproved semantic successor was invented in this task.
