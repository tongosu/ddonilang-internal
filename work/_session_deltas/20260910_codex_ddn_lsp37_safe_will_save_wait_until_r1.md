# DDN-LSP37 Safe willSaveWaitUntil Formatting — Handoff

## Identity

- Live authority used: internal SSOT `v25.72.0 / RD-001~598` and public
  Language SPEC `v0.6.0`; both were treated as read-only.
- Base: `e652a87353738c406dfa9f1441c13599c0edca21`
- Base tree: `31cbea4b9d9698e7b19028bda15d4cd99d5badcd`
- Product: `e101b97d49a85f430f4a59d487b72f0fe596920a`
- Product tree: `4e689abf35bff9825d002b318aaf08eb0b5cd21e`
- Product parent: `e652a87353738c406dfa9f1441c13599c0edca21`
- Review: `PRODUCT_FIXED_PENDING_REVIEW`
- Author/committer: `tongosu <tongosu@myarts.kr>`
- Merge count: `0`

LSP34 and LSP35 remain `PASS_TARGET_BOUND / CLOSED_TARGET_BOUND`. LSP36
remains `PRODUCT_FIXED_PENDING_REVIEW`; neither predecessor was rewritten or
reimplemented.

## Scope and ownership

LSP37 adds `textDocument/willSaveWaitUntil` and advertises
`textDocumentSync.willSaveWaitUntil=true`. The request delegates to the
existing LSP36 `formatting()` path, so the existing parser, canonicalizer,
semantic-preservation, byte-stability, snapshot, lifecycle, UTF-16, size,
and cancellation guards remain the single formatting owner.

Supported live surfaces are `.ddn`, `.ddl`, and `.옮김`. Only the open
`DocumentStore` snapshot is used. Already canonical documents return `[]`;
valid noncanonical documents return one deterministic full-document edit;
unsupported, malformed, legacy, stale, closed, or cancelled requests do not
publish edits. The server never writes or saves the document.

Changed product paths:

- `tool/src/lsp/server.rs`
- `tool/tests/lsp_formatting.rs`
- `tests/run_lsp0_transport_document_sync_check.py`

The transport checker change only relaxes its old exact `textDocumentSync`
dictionary assertion to require the existing fields plus the new
`willSaveWaitUntil` field. No new runner, pack, dependency, parser, semantic
owner, `tool/src/lib.rs` change, SSOT change, or SPEC change was made.

Product blobs:

- `tool/src/lsp/server.rs`: `e344b1b823b5b7d1d7cc046fde8c185ecdfa3337`
- `tool/tests/lsp_formatting.rs`: `9dd1b5dc7caf42819c65fb25247811da2f0825f1`
- `tests/run_lsp0_transport_document_sync_check.py`:
  `c66c728e8f6f4c2fe7cdbca12dd0e15e301f6301`

Product file SHA-256 values:

- `tool/src/lsp/server.rs`:
  `f82593ddf034d605f26c9651fea7773269b4268ee321f3829d0603465c31bdbb`
- `tool/tests/lsp_formatting.rs`:
  `15a3a33953c42ddd4fd7ed45863620657c34ee73fbc8b373e43262e4cd97cdca`
- `tests/run_lsp0_transport_document_sync_check.py`:
  `bd6662d3360070ad9ef217cf89c60d86e1f4fde79878d2be40377683d8a6d449`

## Focused and regression evidence

Focused command:

```text
cargo test -q -p ddonirang-tool --test lsp_formatting --offline
```

Result: `7 passed, 0 failed`.

Related LSP regression command covered formatting, document symbols,
definition, references, rename, hover, completion, signature help,
diagnostics, and semantic tokens. Results were all passing:

```text
15, 3, 11, 4, 7, 4, 4, 5, 3, 4 tests; zero failures
```

Other gates:

- `cargo check -q -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS
- `git diff --check`: PASS
- `python tests/run_lsp0_transport_document_sync_check.py`: PASS
- no-file persistent save request against the current binary:
  `WILL_SAVE_WAIT_UNTIL_BEFORE_EOF=PASS`

The persistent checker reported all existing transport, lifecycle,
before-EOF, fail-closed, and byte-stability cases as PASS. The additional
save-specific check confirmed the response arrived before EOF and the server
remained alive until `exit`.

## Focused behavior evidence

- initialize advertises `textDocumentSync.willSaveWaitUntil=true`.
- DDN, DDL, and `.옮김` supported live snapshots return safe canonical edits.
- canonical input returns `[]`.
- Korean and emoji are covered through the UTF-16 full-document edit range.
- didChange is read from the current snapshot.
- stale version and stale snapshot identity return `[]` without publication.
- didClose returns `[]`.
- unsupported or malformed input returns `[]`.
- cancellation returns `-32800` and publishes no partial edit.
- repeated requests are byte-stable through the shared formatting owner.

## Fresh mutation evidence

Each mutation was applied alone to `tool/src/lsp/server.rs`, followed by the
focused RED test, exact restore to the baseline blob and SHA-256, and the
focused GREEN test. Baseline server blob:
`e344b1b823b5b7d1d7cc046fde8c185ecdfa3337`; baseline SHA-256:
`f82593ddf034d605f26c9651fea7773269b4268ee321f3829d0603465c31bdbb`.

1. `M1_PARTIAL_TOKEN_GUARD`

```text
removed: symbol.full_range == requested
applied: symbol.full_range.start <= requested.start
         && requested.end <= symbol.full_range.end
```

RED: a partial-token range returned a whole-declaration edit instead of
`[]`. Exact restore returned the equality guard and requested fragment.
GREEN: `lsp36_range_formatting_accepts_one_complete_ddn_declaration_only`
passed.

2. `M2_UTF16_TO_UTF8`

```text
removed: range_to_byte_range(source, requested_range, encoding)
applied: range_to_byte_range(source, requested_range, PositionEncoding::Utf8)
```

RED: the Korean/emoji range received `[]` instead of its edit. Exact restore
returned to the negotiated encoding. GREEN: the same LSP36 focused test
passed.

3. `M3_STALE_VERSION_GUARD`

```text
removed: document.contains_key("version") && version != current_version
applied: false && document.contains_key("version") && version != current_version
```

RED: a stale `willSaveWaitUntil` request returned a formatting edit instead
of `[]`. Exact restore returned the version guard. GREEN:
`lsp37_will_save_wait_until_reuses_safe_formatting_for_live_surfaces` passed.

After every mutation the restored server bytes matched the baseline SHA-256
and blob exactly. No mutation residue remains.

## Custody and nonclaims

- Twenty pre-existing foreign tracked dirty paths and pre-existing foreign
  untracked session files were preserved and never staged, formatted, reset,
  cleaned, or stashed.
- Product commit staged exactly the three paths listed above.
- Handoff commit is docs-only and will contain exactly this session delta.
- No push was performed.
- This handoff does not claim independent review PASS, whole LSP/IDE closure,
  VS Code real-host smoke, public support, V1 readiness, release,
  activation, legal approval, or Human PASS.
- Next safe product unit is selected only after this unit's handoff:
  `LSP38` candidate evaluation, with no mapping-only/no-op commit.
