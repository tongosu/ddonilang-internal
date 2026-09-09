# DDN-LSP4-SHARED-DOCUMENT-SYMBOL-R1 — handoff

## Authority and custody

```ini
ORIGINAL_LSP0_ADMISSION = CONSUMED
HISTORICAL_BASE_277C325D = DO_NOT_REUSE
CURRENT_IMPLEMENTATION_BASE = 5f7cd47a5bc8a84844d4ece6a152be09719ec96c
ACTIVE_PRODUCT_UNIT = DDN-LSP4-SHARED-DOCUMENT-SYMBOL-R1
CUSTODY_MODE = NON_OVERLAP_LEASE
NEW_WORKTREE_CREATED = NO
NEW_BRANCH_CREATED = NO
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_LIB_RS_LEASE_REQUIRED = NO
```

The existing `tool/src/lsp/symbol.rs` owner was reused. `tool/src/lib.rs` was
not changed, staged, or committed.

## Product result

Product commit:

```ini
PRODUCT_FIXED_HEAD = 36afcf9ac6e471f4564a97ef273eb15203d40222
PRODUCT_FIXED_TREE = b062c1e9652a9fc403a6891a44229c39c8445d9a
PRODUCT_FIXED_PARENT = 5f7cd47a5bc8a84844d4ece6a152be09719ec96c
```

Changed product paths are exactly:

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/document_symbol.rs
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/src/lsp/symbol.rs
tool/tests/lsp_document_symbol.rs
```

Implemented behavior:

- `textDocument/documentSymbol` is dispatched and advertised by initialize.
- Shared symbol parsing collects current V25 local definitions in source order.
- `이름씨` maps to LSP Variable kind `13`; callable seed kinds map to Function
  kind `12`.
- Each symbol returns its full declaration range, UTF-16 selection range,
  stable local definition identity, source profile, version, and snapshot
  identity.
- didChange reads the current document snapshot; stale version and snapshot
  requests are rejected; malformed/legacy source returns an empty symbol list;
  didClose returns an empty symbol list.
- Persistent transport receives a document-symbol response before EOF.

## Verification

Focused command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --no-fail-fast
```

Result: `15 + 3 + 6 + 2 + 3 = 29` tests passed, zero failed.

Existing transport checker:

```text
$env:CARGO_TARGET_DIR = 'I:/home/urihanl/ddn/codex/build/lsp4-document-symbol-r1'
python tests/run_lsp0_transport_document_sync_check.py
```

Result: existing I1–I8 and RB06/RB08 checks passed/failed-closed as expected;
H12, G12, and `S13_BLACKBOX_DOCUMENT_SYMBOL_BEFORE_EOF=PASS`; final
`LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.

`git diff --check` and Python AST parsing passed. `cargo check -p
ddonirang-tool` remains blocked by pre-existing foreign dirty `lang` changes,
not by this LSP4 diff:

```text
lang/src/model.rs: UnitDim::AXIS_COUNT, exponents, from_exponents missing
lang/src/parser.rs: Fixed64::parse_decimal_exact missing
```

## Mutation evidence

Baseline and every exact restore hash for the mutated server file:

```ini
TARGET = tool/src/lsp/server.rs
ORIGINAL_SHA256 = 0F64D4979611FE4DA372F2A2F14D1F73F4753E2B41424128F8D3EAFD4015B8AC
RESTORE_SHA256_M1 = 0F64D4979611FE4DA372F2A2F14D1F73F4753E2B41424128F8D3EAFD4015B8AC
RESTORE_SHA256_M2 = 0F64D4979611FE4DA372F2A2F14D1F73F4753E2B41424128F8D3EAFD4015B8AC
RESTORE_SHA256_M3 = 0F64D4979611FE4DA372F2A2F14D1F73F4753E2B41424128F8D3EAFD4015B8AC
```

### M1 — UTF-16 range conversion guard

Exact temporary hunk in `LspServer::document_symbols`: the `encoding`
argument for `symbol.full_range` was replaced with `PositionEncoding::Utf8`.

```text
byte_range_to_lsp_range(source, symbol.full_range, encoding)
-> byte_range_to_lsp_range(source, symbol.full_range, PositionEncoding::Utf8)
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol h01_order_kind_full_and_selection_ranges -- --nocapture
```

Expected and actual RED: exit `101`; full-range assertion reported actual
UTF-8 end character `22` versus expected UTF-16 end character `12`.
The exact hunk was restored immediately; the same focused test then passed.

### M2 — stale document-version guard

Exact temporary hunk: removed the `document.get("version")` comparison and
`-32801` error response from `LspServer::document_symbols`.

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol h02_change_stale_rejection_malformed_and_close_empty -- --nocapture
```

Expected and actual RED: exit `101`; the stale request no longer matched the
expected `-32801` error response. The exact block was restored immediately;
the same focused test then passed.

### M3 — initialize capability advertisement

Exact temporary hunk in initialize capabilities:

```text
"documentSymbolProvider": true -> false
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol h01_order_kind_full_and_selection_ranges -- --nocapture
```

Expected and actual RED: exit `101`; initialize returned `false` while the
focused assertion required `true`. The exact hunk was restored immediately;
the same focused test then passed.

## Handoff boundary

```ini
READY_FOR_INDEPENDENT_REVIEW = YES
PUSH_PERFORMED = NO
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
PRODUCT_DIFF_FROM_LSP3_FIXED = 6 paths above
NEW_DEPENDENCY = 0
NEW_PACK_RUNNER_META_TEST = 0/0/0
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

Foreign tracked changes and pre-existing protected untracked session files
were preserved and were not staged.
