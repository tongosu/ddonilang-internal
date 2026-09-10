# DDN-LSP34 Open-Document Type Definition — Handoff

## Identity

- Base: `7ecab48135722d5614241d0708428d496b8c32da`
- Product: `9da2dda8dc82016017bccd0e13764ec28146004e`
- Product tree: `ce4634ac8b2d81d692963bdaa4592d8399464f90`
- Product parent: `7ecab48135722d5614241d0708428d496b8c32da`
- Review: `PRODUCT_FIXED_PENDING_REVIEW`
- Author/committer: `tongosu <tongosu@myarts.kr>`

## Scope

LSP34 completes `textDocument/typeDefinition` for open DDN documents. Existing
DocumentStore snapshots and the shared symbol owner remain authoritative. A
callable parameter with an explicit `TypeRef` is resolved through the existing
signature/ParamPin path and then matched to exactly one open type definition by
name and existing `TypeIdentity`. Closed, stale, duplicate, unknown, comment,
string, and non-type cases remain fail-closed. UTF-16 ranges, cancellation,
version/snapshot guards, and response-before-EOF are covered.

Changed product paths:

- `tool/src/lsp/server.rs`
- `tool/src/lsp/signature_help.rs`
- `tool/src/lsp/symbol.rs`
- `tool/tests/lsp_open_document_navigation.rs`

No `tool/src/lib.rs`, dependency, parser, filesystem index, remote source, or
public specification change.

## Focused evidence

Command:

```text
cargo test -q -p ddonirang-tool --test lsp_open_document_navigation
```

Result: `12 passed, 0 failed`.

The LSP34 test proves callable ParamPin type identity, exact open-document
target, UTF-16 type range, closed-target removal, deterministic repeat, and
pre-analysis cancellation (`-32800`). Existing LSP19 type-definition and
LSP10 open-document navigation cases remain green.

## Fresh mutation evidence

Each mutation was applied alone, then restored before the next mutation.

1. TypeIdentity/name guard removal in `tool/src/lsp/symbol.rs`:

```text
removed: if name == type_name {
applied: if true {
```

RED: `lsp19_type_definition_is_exact_open_document_bound_and_utf16_current`
returned `Null` instead of `file:///c-applied.ddn`.

Exact restore: `if name == type_name`; restored file SHA-256 was
`5bf30be6a1245d2b4a523bf4cab48e885cf65188790cb00aefcac677696c32ad`.

GREEN: the focused suite returned `12 passed, 0 failed`.

2. Type-definition range encoding downgrade in `tool/src/lsp/server.rs`:

```text
removed: result.range, encoding
applied: result.range, PositionEncoding::Utf8
```

RED: the UTF-16 assertion expected character `2` and observed character `6`.

Exact restore: `result.range, encoding`.

GREEN: the focused suite returned `12 passed, 0 failed` after restore.

3. Type-definition stale-version guard removal:

```text
removed: if requested_version != snapshot.version {
applied: if false && requested_version != snapshot.version {
```

RED: both LSP19 stale-version assertions failed because stale requests were
accepted.

Exact restore: `if requested_version != snapshot.version`.

GREEN: the focused suite returned `12 passed, 0 failed` after restore.

## External environment

LSP22C real VS Code Host smoke was not claimed. Three read-only checks found
`CodeSetup-stable-...` updater processes still running. No updater process was
terminated and no VSIX was rebuilt or installed. Status:
`HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`.

## Nonclaims

This handoff does not claim independent review PASS, whole LSP/IDE closure,
public extension release, V1 readiness, release, or Human PASS.
