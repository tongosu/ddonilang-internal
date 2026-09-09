# DDN-LSP7 prepareRename/rename checkpoint

## Session contract

```ini
AI_PROVIDER = Codex
AI_SURFACE = Work
AI_CAPABILITY = product implementation
SESSION_NICKNAME = LSP제품개발 Work
PROJECT_ROLE = single writer
RETURN_LABEL = LSP7_PREPARE_RENAME_AND_RENAME
DEEP_RESEARCH_CHECK = NOT_USE
PUSH_PERFORMED = NO
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

## Target custody

```makefile
START_HEAD = 413c44b409e30cf93b1fe13593749ed34b2b4c19
START_TREE = 580a8bdf3090936fed8ca7cb0efccd6fda173826
IMPLEMENTATION_BASE = 44a38719b44ad71fb3c87505e0e980769a1b9811
LSP4_PRODUCT = 36afcf9ac6e471f4564a97ef273eb15203d40222
LSP5_PRODUCT = 7e853b852534a4b30ea7ff49f01d73e78d9f07b2
LSP5_HANDOFF = 44a38719b44ad71fb3c87505e0e980769a1b9811
```

The shared root and foreign dirty paths were not modified, staged, or cleaned.
`tool/src/lib.rs` was not changed. Existing LSP4/LSP5 review states were not rerun.

## Product scope

The LSP7 vertical adds `textDocument/prepareRename` and `textDocument/rename` for
same-document local immutable/callable identities. It reuses the existing symbol
owner (`resolve_symbol` and `collect_local_references`) and publishes only the
current document snapshot. It provides UTF-16 ranges, deterministic edits, the
canonical local definition identity, current version/snapshot metadata, and
fail-closed behavior for stale requests, unknown/closed documents, standard
library symbols, collisions, invalid names, punctuation, and unsupported
positions. No cross-file scan, filesystem mutation, or new semantic registry was
added.

## Changed product/test paths

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/src/lsp/rename.rs
tool/tests/lsp_rename.rs
```

Unexpected task-owned paths: 0. `tool/src/lib.rs`, `lang/**`, `core/**`, WASM,
Workbench, and foreign dirty paths were untouched.

## Mutation evidence

Each mutation was applied alone, executed immediately, restored byte-exactly,
and followed by GREEN focused tests.

### M1 — declaration inclusion

```text
Target: tool/src/lsp/rename.rs
Original hunk: collect_local_references(snapshot, position, encoding, true)?
Mutation:     collect_local_references(snapshot, position, encoding, false)?
```

Focused RED:

```text
lsp7_prepare_and_rename_reuses_local_identity_and_utf16_ranges ... FAILED
left: 2, right: 3
```

Restore SHA-256:

```text
BB42ED53BF85B47E8AD50C6D56F1E5E10D721907B018020A91B1C122F1A67BE4
```

After restore: focused LSP7 tests 2 passed.

### M2 — UTF-16 range conversion

```text
Target: tool/src/lsp/server.rs
Original hunk: byte_range_to_lsp_range(source, range, encoding)
Mutation:     rename edit conversion forced PositionEncoding::Utf8
```

Focused RED:

```text
second rename edit range mismatch: left start character 31/end 40,
expected start character 19/end 22
```

Restore SHA-256:

```text
62BFCA076DFEDD34ED51972EBE94FD40A8A1E7A63C2E7AB2F0CBFCB1591A29EB
```

After restore: focused LSP7 tests 2 passed.

### M3 — stale version guard

```text
Target: tool/src/lsp/server.rs
Original hunk: if requested_version != snapshot.version {
Mutation:     if requested_version == snapshot.version {
```

Focused RED:

```text
lsp7_prepare_and_rename_reuses_local_identity_and_utf16_ranges ... FAILED
called Option::unwrap() on a None value
lsp7_change_stale_collision_invalid_nonlocal_and_close_fail_closed ... FAILED
assertion failed: expected error code -32801
```

Restore SHA-256:

```text
62BFCA076DFEDD34ED51972EBE94FD40A8A1E7A63C2E7AB2F0CBFCB1591A29EB
```

After restore: focused LSP7 tests 2 passed.

## Validation

```text
cargo test -p ddonirang-tool --test lsp_rename --offline
PASS: 2 passed, 0 failed

cargo test -p ddonirang-tool --test lsp_rename --test lsp_signature_help --test lsp_references --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline
PASS: 35 passed, 0 failed

python tests/run_lsp0_transport_document_sync_check.py
PASS: SH16_BLACKBOX_RENAME_BEFORE_EOF=PASS
PASS: LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS

git diff --check
PASS

rustfmt --edition 2021 --check tool/src/lsp/rename.rs tool/tests/lsp_rename.rs
PASS
```

The current dirty worktree `cargo check -p ddonirang-tool --offline` remains
blocked by pre-existing foreign `lang/**` changes referring to
`UnitDim::AXIS_COUNT`, `UnitDim::exponents`, `UnitDim::from_exponents`, and
`Fixed64::parse_decimal_exact`. Those files are outside this slice and were not
modified. A clean-target check is a separate gate and is not claimed here.

## Product fixed

```makefile
PRODUCT_FIXED_HEAD = e88d03f702bc52a9e8f73b6422bcac38f912d711
PRODUCT_FIXED_TREE = dfda6b73a7d13e89450b24c668526d60711101b3
PRODUCT_FIXED_PARENT = 413c44b409e30cf93b1fe13593749ed34b2b4c19
PRODUCT_PATH_COUNT = 5
PRODUCT_FILE_CHANGE = 0 outside task-owned LSP7 paths
```

The exact mutation restores completed before final rustfmt normalization. Final
task-owned file SHA-256 values are:

```text
tool/src/lsp/rename.rs = A0C711010CB67C781D83FECADF40379781955ADDD59D8276B6351345F68A7A32
tool/src/lsp/server.rs = 62BFCA076DFEDD34ED51972EBE94FD40A8A1E7A63C2E7AB2F0CBFCB1591A29EB
tool/tests/lsp_rename.rs = C9C82CD11137A55EE58D57C56660AA996FD902DD82A6201113ACA2FEF9E28792
tests/run_lsp0_transport_document_sync_check.py = 21DDA59707F9C26978F5FABF64F202E5F90A3607442B3DAAC0E390A5781E1848
tool/src/lsp/mod.rs = F28E7454449936B22E8E72D450AB577516E66D8BD89967480EA1E0414B15A1BD
```

## Next unit

```ini
CURRENT_LSP_UNIT = LSP7_PREPARE_RENAME_AND_RENAME
REVIEW_STATUS = IMPLEMENTED_PENDING_REVIEW
NEXT_AUTONOMOUS_UNIT = LSP8_DOCUMENT_HIGHLIGHT
FULL_SEMANTIC_IDE = NOT_CLAIMED
PUBLIC_EXTENSION_RELEASE = NOT_CLAIMED
V1_RELEASE_HUMAN_PASS = NOT_CLAIMED
```
