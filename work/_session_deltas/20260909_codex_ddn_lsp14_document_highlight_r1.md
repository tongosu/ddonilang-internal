# DDN-LSP14 Same-Document Symbol Highlight — Handoff R1

## Binding

- Unit: LSP14_SAME_DOCUMENT_SYMBOL_HIGHLIGHT
- LSP13 product: 1e0cf60cec5f59ce907e7608a05234df2ab9f00c
- LSP13 handoff: 4dd41b5bf4473fae30c2858ab325462a68e047ff
- Product commit: a4924462eb6fb0d519d4b6c7ad4153dc860fca85
- Product tree: da702cff555f5d55e40ee725c9fbd56e4838c693
- Product parent: 4dd41b5bf4473fae30c2858ab325462a68e047ff
- Review state: IMPLEMENTED_PENDING_REVIEW; no LSP14 independent PASS is claimed.

## Shared owner and product scope

The existing document_highlight.rs, server.rs, DocumentStore, and symbol.rs owners remain in use. LSP14 adds no parser, filesystem index, cross-document scan, remote/upload path, or new cache.

The shared symbol owner now treats duplicate local DefinitionIdentity candidates as ambiguous and returns no resolution. This makes declaration/usages highlighting fail closed while preserving existing unique-identity behavior.

Changed exactly:

- tool/src/lsp/symbol.rs
- tool/tests/lsp_document_highlight.rs

No tool/src/lib.rs, public CLI/WASM/UI, lang/core, SSOT/SPEC, or foreign dirty path changed.

## DoD evidence

- Existing local declaration plus same-document usages highlight in deterministic source order.
- Callable declaration and representative calls remain covered by the existing highlight test.
- Korean and emoji ranges remain UTF-16 through negotiated server encoding.
- Comment/string false positives return []; the test includes a valid string containing the symbol name.
- didChange uses the current snapshot; stale version/snapshot guards remain -32801/-32802 fail-closed.
- didClose, unknown, stdlib/non-local, and ambiguous duplicate-definition positions return [].
- Repeated request output remains byte-stable.
- Existing black-box response arrives before EOF.

## Exact mutation evidence

Each mutation was applied alone, never staged, restored immediately, and followed by focused GREEN.

### M1 — comment/string token inclusion

Target hunk in tool/src/lsp/symbol.rs:

    TokenKind::Ident(_) | TokenKind::Josa(_) | TokenKind::Variable(_) => {
        Some(token.raw.as_str())
    }
-   _ => None,
+   _ => Some(token.raw.trim_matches('"')),

Command: cargo test -p ddonirang-tool --test lsp_document_highlight --offline --quiet

RED: valid string "새함수" returned declaration plus string highlight instead of [].

Restore: _ => None restored. GREEN: 3 passed; 0 failed.

### M2 — UTF-16 range downgraded to UTF-8

Target hunk in tool/src/lsp/server.rs:

- super::position::byte_range_to_lsp_range(source, highlight.range, encoding)
+ super::position::byte_range_to_lsp_range(source, highlight.range, PositionEncoding::Utf8)

Command: same focused document-highlight command.

RED: Korean/emoji reference range returned UTF-8 start/end 31..40 instead of UTF-16 19..22.

Restore: negotiated encoding argument restored. GREEN: 3 passed; 0 failed.

### M3 — stale version guard bypass

Target hunk in tool/src/lsp/server.rs:

- if requested_version != snapshot.version {
+ if false && requested_version != snapshot.version {

The mutation was applied to the document highlight document version guard only.

Command: same focused document-highlight command.

RED: stale request no longer returned -32801; the existing test assertion failed.

Restore: if requested_version != snapshot.version restored. GREEN: 3 passed; 0 failed.

## Verification

    cargo test -p ddonirang-tool --test lsp_document_highlight --offline --quiet
    3 passed; 0 failed

    cargo test -p ddonirang-tool --test lsp_document_highlight --test lsp_definition --test lsp_references --test lsp_rename --test lsp_document_symbol --test lsp_formatting --test lsp_open_document_navigation --test lsp_signature_help --test lsp_semantic_tokens --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline --quiet
    all listed test groups passed

    python tests/run_lsp0_transport_document_sync_check.py
    HL17_BLACKBOX_DOCUMENT_HIGHLIGHT_BEFORE_EOF=PASS
    LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS

    git archive a4924462 -- Cargo.toml Cargo.lock .cargo core lang numeric proof symbolic tool tests
    cargo check --manifest-path I:\home\urihanl\ddn\codex\build\lsp14-clean-snapshot-r1\tool\Cargo.toml --bin ddonirang-lsp --offline
    Finished dev profile

    git diff --check -- tool/src/lsp/symbol.rs tool/tests/lsp_document_highlight.rs
    PASS

Final task-file SHA-256:

    tool/src/lsp/symbol.rs = 08CF95A42C72DCF81ACC9211E15F940674FC6BC53564A4D3BA0175BBF189112F
    tool/tests/lsp_document_highlight.rs = B922273242E7327C1F5885DE80529A206728A8A5A5D3BADE206FAD9048337F6A

## Custody

- New dependency/pack/runner: 0/0/0
- Filesystem crawl: 0
- Source upload / remote dependency: 0/0
- Foreign dirty touched: 0
- Protected untracked changed: 0
- Push: NO at handoff creation
- Author and committer: tongosu <tongosu@myarts.kr>
- Prohibited trailer count: 0
- Next unit: not started; candidate remains deferred pending the LSP14 review boundary.
