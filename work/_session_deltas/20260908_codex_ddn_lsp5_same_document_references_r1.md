# DDN-LSP5-SAME-DOCUMENT-REFERENCES-R1 — handoff

## Boundaries

```ini
LSP3_PRODUCT_TARGET = fe60fed73e129d9bfa8737dbe0b254c3b8e360ea
LSP3_REVIEW_VERDICT = PASS_TARGET_BOUND
LSP3_STATUS = CLOSED_TARGET_BOUND
LSP4_PRODUCT_TARGET = 36afcf9ac6e471f4564a97ef273eb15203d40222
LSP4_HANDOFF = fe5adf2e1d056904763978b54fa6bf2d06910b0e
CURRENT_IMPLEMENTATION_BASE = fe5adf2e1d056904763978b54fa6bf2d06910b0e
ACTIVE_PRODUCT_UNIT = DDN-LSP5-SAME-DOCUMENT-REFERENCES-R1
NEW_WORKTREE_CREATED = NO
NEW_BRANCH_CREATED = NO
CUSTODY_MODE = NON_OVERLAP_LEASE
TOOL_SRC_LIB_RS_CHANGED = 0
PUSH = NO
```

LSP4 was not reimplemented or reopened. LSP5 reuses the existing
`resolve_symbol` identity owner and adds only same-document local references.

## Product commit

```ini
PRODUCT_FIXED_HEAD = 7e853b852534a4b30ea7ff49f01d73e78d9f07b2
PRODUCT_FIXED_TREE = 13c0b4bda806730ea3de20dd6d8821f35b9f38ff
PRODUCT_FIXED_PARENT = fe5adf2e1d056904763978b54fa6bf2d06910b0e
```

Product paths changed exactly:

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/mod.rs
tool/src/lsp/references.rs
tool/src/lsp/server.rs
tool/src/lsp/symbol.rs
tool/tests/lsp_references.rs
```

Implemented behavior:

- Advertises and dispatches `textDocument/references`.
- Reuses the shared local definition identity from `resolve_symbol`.
- Returns same-document references in source order with UTF-16 ranges.
- Supports `context.includeDeclaration`.
- Rejects stale version and snapshot identity requests.
- Returns empty results for unknown, stdlib, malformed/legacy, or closed
  documents.
- Persistent transport returns references before EOF.

## Verification

Focused LSP regression:

```text
cargo test -p ddonirang-tool --test lsp_references --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --no-fail-fast
```

Result: `15 + 3 + 6 + 2 + 3 + 2 = 31` tests passed, zero failed.

Existing transport checker, using the LSP5 target output:

```text
$env:CARGO_TARGET_DIR = 'I:/home/urihanl/ddn/codex/build/lsp5-references-r1'
python tests/run_lsp0_transport_document_sync_check.py
```

Result: I1–I8 and RB06/RB08 passed or failed-closed as specified; H12, G12,
S13, and `R14_BLACKBOX_REFERENCES_BEFORE_EOF=PASS`; final
`LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.

`git diff --check` passed.

`cargo check -p ddonirang-tool` remains blocked by the same pre-existing
foreign dirty `lang/**` changes and is not an LSP5 finding:

```text
lang/src/model.rs: UnitDim::AXIS_COUNT, exponents, from_exponents missing
lang/src/parser.rs: Fixed64::parse_decimal_exact missing
```

## Mutation evidence

Baseline and exact restore hashes:

```ini
SERVER_SHA256 = 0697D64BD691A4F7E24C003C4D5D74F45E64E9F30062735C73B219B25352763D
SYMBOL_SHA256 = 95854320D4FED5818D9DC4F8390444D03F597565317259E9A5EBE518FCB5BD62
M1_SERVER_RESTORE_SHA256 = 0697D64BD691A4F7E24C003C4D5D74F45E64E9F30062735C73B219B25352763D
M2_SYMBOL_RESTORE_SHA256 = 95854320D4FED5818D9DC4F8390444D03F597565317259E9A5EBE518FCB5BD62
M3_SERVER_RESTORE_SHA256 = 0697D64BD691A4F7E24C003C4D5D74F45E64E9F30062735C73B219B25352763D
```

### M1 — reference range UTF-16 conversion

Temporary hunk in `LspServer::references` changed the range conversion from
the negotiated `encoding` to `PositionEncoding::Utf8`.

```text
byte_range_to_lsp_range(source, range, encoding)
-> byte_range_to_lsp_range(source, range, PositionEncoding::Utf8)
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_references i01_identity_order_utf16_and_declaration_context -- --nocapture
```

RED: exit `101`; emoji-containing references returned UTF-8 character ranges
(for example line 1 start `31`, end `40`) instead of the expected UTF-16
range (start `19`, end `22`). Exact restore followed, then the same test was
GREEN.

### M2 — includeDeclaration guard

Temporary hunk in `collect_local_references` changed:

```text
.filter(|range| include_declaration || Some(*range) != declaration)
-> .filter(|_| true)
```

The focused test with `includeDeclaration=false` then returned the declaration
as a third location instead of two locations. Exit `101`. Exact restore
followed, then the same test was GREEN.

### M3 — stale version guard

Temporary hunk removed the `document.get("version")` comparison and `-32801`
error response from `LspServer::references`.

Command:

```text
cargo test -p ddonirang-tool --test lsp_references i02_change_stale_malformed_and_close_empty -- --nocapture
```

RED: exit `101`; stale request no longer matched `-32801`. Exact restore
followed, the server hash returned exactly, and the same test was GREEN.

## Handoff

```ini
READY_FOR_INDEPENDENT_REVIEW = YES
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
STAGED = NONE
PROCESS_RESIDUE = 0
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

Foreign tracked changes and pre-existing protected untracked session files
were preserved and were not staged.
