# DDN-LSP36 Safe Range Formatting — Handoff

## Identity

- Base: `57cfd1090097681cce8781650b1d05a406effc32`
- Base tree: `c28ec26fcce05062c499d5601edf7a5f74cede2b`
- Product: `e44a2249d6d0352f3549e86e26e8de9fe9937eb2`
- Product tree: `cc663ec380390764b22151797d383a0c449aaeff`
- Product parent: `57cfd1090097681cce8781650b1d05a406effc32`
- Review: `PRODUCT_FIXED_PENDING_REVIEW`
- Author/committer: `tongosu <tongosu@myarts.kr>`

## Scope

LSP36 adds `textDocument/rangeFormatting` by reusing the existing LSP32
canonicalization and stability owner. DDN accepts exactly one complete
top-level declaration; DDL and `.옮김` accept exactly one complete language
section. Partial token/body ranges, cross-declaration ranges, invalid or
legacy input, and ambiguous input return no edit. A successful response has
exactly one atomic full-target edit and preserves semantic identity.

The implementation continues to use `DocumentStore`, the existing parser,
canonicalizer, and existing symbol/identity paths. It adds no parser,
formatter owner, filesystem scan, remote dependency, source upload,
dependency, pack, runner, or meta-test. `tool/src/lib.rs`, CLI, WASM ABI,
SSOT, and public SPEC are unchanged.

Changed product paths:

- `tool/src/lsp/server.rs`
- `tool/tests/lsp_formatting.rs`

Product blobs at the fixed target:

- `tool/src/lsp/server.rs`: `6ef64682aa8ad7e5374e5fbc7b9ddb1c799b21e6`
- `tool/tests/lsp_formatting.rs`: `c3ef84304d44382bba46d292cdc0e1c992301abb`

Product file SHA-256 values:

- `tool/src/lsp/server.rs`: `d6603be1bb23ccbfa92c90b2eec23d40101cf7bcdc64617efdd3da2d4fece8e4`
- `tool/tests/lsp_formatting.rs`: `ae3bfa2163c3a0f92309fdea49d28bd0a42b71c2a2c402cc2c8b1a782c1735f5`

## Focused and regression evidence

Focused command:

```text
cargo test -q -p ddonirang-tool --test lsp_formatting --offline
```

Result: `6 passed, 0 failed`.

Related LSP regression command covered document symbols, definition,
references, rename, hover, completion, signature help, diagnostics, and
semantic tokens. All listed test binaries passed: `15 + 3 + 11 + 4 + 4 + 4
+ 5 + 3 + 4` tests, with zero failures.

Other gates:

- `cargo check -q -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS
- `git diff --check`: PASS
- Existing persistent transport checker: PASS

The persistent checker reported `I1` through `I8`, `F13` full formatting,
and the existing hover, definition, document-symbol, workspace-symbol,
references, signature-help, inlay-hint, rename, highlight, semantic-token,
open-document navigation, type-definition, folding, and selection-range
before-EOF cases as PASS. A no-file inline black-box invocation against the
current worktree binary additionally verified:

```text
initialize.documentRangeFormattingProvider = true
textDocument/rangeFormatting response before EOF = PASS
server remained alive until exit = PASS
```

The existing checker script was not changed. Its separate cached binary did
not contain the new capability during an initial comparison; the current
worktree cargo binary was then used for the range-specific before-EOF check.

## Behavior evidence

- initialize advertises `documentRangeFormattingProvider=true`.
- Current open snapshot and negotiated UTF-16 encoding are used.
- DDN exact declaration spans and DDL exact section spans are required.
- didChange uses the current snapshot; didClose returns `[]`.
- stale document version returns `-32801`; stale snapshot identity returns
  `-32802`.
- cancellation is checked before target discovery, after canonicalization,
  and before response; no partial edit is emitted.
- invalid, legacy, unsupported, and already canonical input returns `[]`.
- output is deterministic and parse-canon-parse-canon byte-stable.

## Fresh mutation evidence

Each mutation was applied alone to `tool/src/lsp/server.rs`, followed
immediately by the focused RED test, exact restoration to the baseline blob
and SHA-256, and the same focused GREEN test. The baseline server blob was
`6ef64682aa8ad7e5374e5fbc7b9ddb1c799b21e6` and baseline SHA-256 was
`d6603be1bb23ccbfa92c90b2eec23d40101cf7bcdc64617efdd3da2d4fece8e4`.

1. Partial-token range guard:

```text
removed: symbols.iter().any(|symbol| symbol.full_range == requested)
applied: symbol.full_range.start <= requested.start
         && requested.end <= symbol.full_range.end
```

The fragment source was likewise changed from `requested` to the containing
symbol range. RED: the partial-range test expected `[]` but received one
whole-declaration edit. Exact restore returned to the equality guard and
requested fragment. GREEN: `1 passed, 0 failed`.

2. UTF-16 downgrade:

```text
removed: range_to_byte_range(source, requested_range, encoding)
applied: range_to_byte_range(source, requested_range, PositionEncoding::Utf8)
```

RED: the Korean/emoji declaration expected one edit but received `[]`.
Exact restore returned to the negotiated `encoding`. GREEN: `1 passed, 0
failed`.

3. Stale-version guard removal:

```text
removed: document.get("version").and_then(Value::as_i64)
applied: None::<i64>
```

RED: the stale DDL request expected `-32801` but received a successful edit.
Exact restore returned to the document version lookup. GREEN: `1 passed, 0
failed`.

After every mutation, the restored server bytes matched the baseline SHA-256
and blob exactly. No mutation residue remains.

## Custody and nonclaims

- Twenty pre-existing foreign tracked dirty paths were preserved, not
  formatted, staged, committed, reset, cleaned, or stashed.
- Only the two product paths above were staged in the product commit.
- The handoff document is the only path staged in the subsequent docs-only
  commit.
- No independent review PASS is claimed.
- This handoff does not claim whole LSP/IDE closure, VS Code real-host
  closure, public extension release, V1 readiness, release, or Human PASS.
- Next autonomous unit: `LSP37 safe formatting-on-save applicability mapping
  only`.
