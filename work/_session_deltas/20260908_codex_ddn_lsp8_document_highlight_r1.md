# DDN-LSP8 document highlight checkpoint

## Session contract

```ini
AI_PROVIDER = Codex
AI_SURFACE = Work
AI_CAPABILITY = product implementation
SESSION_NICKNAME = LSP제품개발 Work
PROJECT_ROLE = single writer
RETURN_LABEL = LSP8_DOCUMENT_HIGHLIGHT
DEEP_RESEARCH_CHECK = NOT_USE
PUSH_PERFORMED = NO
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

## Target custody

```makefile
START_HEAD = ad5587e8bde2fa77ef17ef05ffd0887dd2570f58
START_TREE = 0b58b1c6704f221e883ba617b0beb3c07d26675e
PRODUCT_FIXED_HEAD = fe0f745064c11b756ad336caf58dc5bbf1eaf513
PRODUCT_FIXED_TREE = 78f767d4ab77a2ed7e364476f33561744c039587
PRODUCT_FIXED_PARENT = ad5587e8bde2fa77ef17ef05ffd0887dd2570f58
PRODUCT_PATH_COUNT = 5
```

LSP7 remains fixed at `e88d03f702bc52a9e8f73b6422bcac38f912d711` with handoff
`ad5587e8bde2fa77ef17ef05ffd0887dd2570f58`. The shared root and all foreign
dirty paths were preserved. No `tool/src/lib.rs`, `lang/**`, `core/**`, WASM,
Workbench, or protected untracked file was modified, staged, or cleaned.

## Product scope

`textDocument/documentHighlight` is now advertised and served from the same
live document snapshot as the other LSP features. It reuses the existing
`resolve_symbol` and `collect_local_references` owners, so declaration/read
ranges have the same identity and source order as LSP5 references. The
declaration is emitted as LSP Write kind `3`; other occurrences are Read kind
`2`. Ranges use the negotiated UTF-16 encoding. Unknown, standard-library,
malformed, comment/string, stale, and closed-document cases fail closed with an
empty result or the existing stale error. No scanner, identity registry, or
cross-file lookup was added.

## Mutation evidence

Each mutation was applied alone, run immediately, restored byte-exactly, and
followed by focused GREEN tests.

### M1 — declaration inclusion

```text
Target: tool/src/lsp/document_highlight.rs
Original hunk: collect_local_references(snapshot, position, encoding, true)?
Mutation:     collect_local_references(snapshot, position, encoding, false)?
```

RED:

```text
lsp8_highlight_reuses_reference_ranges_and_utf16_order ... FAILED
left: 2, right: 3
lsp8_highlight_stale_change_false_positive_and_close_fail_closed ... FAILED
left: 1, right: 2
```

Exact restore SHA-256:

```text
72CD6D42711B0FB61428E76C64D062D1359D92C33F2B99491500D3D1F8605C23
```

After restore: focused LSP8 tests 2 passed.

### M2 — UTF-16 conversion

```text
Target: tool/src/lsp/server.rs
Original hunk: byte_range_to_lsp_range(source, highlight.range, encoding)
Mutation:     byte_range_to_lsp_range(source, highlight.range, PositionEncoding::Utf8)
```

RED:

```text
expected second highlight range line 1 character 19..22
actual second highlight range line 1 character 31..40
```

Exact restore SHA-256 at restore:

```text
2ECCFB60E50B8111F8274312EFF0A73B5832FDA026013CAAEDD06388E56471D8
```

After restore: focused LSP8 tests 2 passed.

### M3 — stale version guard

```text
Target: tool/src/lsp/server.rs
Original hunk: if requested_version != snapshot.version {
Mutation:     if requested_version == snapshot.version {
```

RED:

```text
lsp8_highlight_reuses_reference_ranges_and_utf16_order ... FAILED
called Option::unwrap() on a None value
lsp8_highlight_stale_change_false_positive_and_close_fail_closed ... FAILED
assertion failed: expected error code -32801
```

Exact restore SHA-256 at restore:

```text
2ECCFB60E50B8111F8274312EFF0A73B5832FDA026013CAAEDD06388E56471D8
```

After restore: focused LSP8 tests 2 passed.

## Validation

```text
cargo test -p ddonirang-tool --test lsp_document_highlight --offline
PASS: 2 passed, 0 failed

cargo test -p ddonirang-tool --test lsp_document_highlight --test lsp_rename --test lsp_signature_help --test lsp_references --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline
PASS: 37 passed, 0 failed

python tests/run_lsp0_transport_document_sync_check.py
PASS: HL17_BLACKBOX_DOCUMENT_HIGHLIGHT_BEFORE_EOF=PASS
PASS: LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS

git diff --check
PASS

rustfmt --edition 2021 --check tool/src/lsp/document_highlight.rs tool/tests/lsp_document_highlight.rs tool/src/lsp/mod.rs tool/src/lsp/server.rs
PASS
```

The current dirty-worktree `cargo check -p ddonirang-tool --offline` remains
blocked by pre-existing foreign `lang/**` changes referring to
`UnitDim::AXIS_COUNT`, `UnitDim::exponents`, `UnitDim::from_exponents`, and
`Fixed64::parse_decimal_exact`. Those files are outside this slice and were
not modified. No clean-target check is claimed in this checkpoint.

## Product fixed

```makefile
REVIEW_STATUS = IMPLEMENTED_PENDING_REVIEW
FULL_SEMANTIC_IDE = NOT_CLAIMED
PUBLIC_EXTENSION_RELEASE = NOT_CLAIMED
V1_RELEASE_HUMAN_PASS = NOT_CLAIMED
```

The LSP7 server/mod formatting normalization is task-owned and semantic-neutral;
the LSP8 product commit still changes exactly five task-owned paths.

## Next unit

```ini
CURRENT_LSP_UNIT = LSP8_DOCUMENT_HIGHLIGHT
NEXT_AUTONOMOUS_UNIT = LSP9_SEMANTIC_TOKENS_FULL
```
