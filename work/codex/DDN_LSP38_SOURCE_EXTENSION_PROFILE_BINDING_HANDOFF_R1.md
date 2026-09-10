# DDN-LSP38 source extension/profile binding handoff R1

## Authority and target

- Live SSOT: `v25.73.0 / RD-001~601`.
- Public language specification: `v0.6.0`.
- Predecessor: `8d13722809f819706c23e7df98d0899a0135b35a`.
- Product fixed: `d7af9f9a316fe31cea31445fb5b0a5ff3769e3a6`.
- Product tree: `14f9ecaae8bd02f0dcc8e55ffc6eeb927d73e01d`.
- Product parent: `8d13722809f819706c23e7df98d0899a0135b35a`.
- Merge count: `0`.

The exact physical multilingual profile registry remains OPEN. No unadmitted
profile extension was invented. The product-admitted surfaces are `.ddn`,
`.또니`, `.ddl`, and `.옮김`.

## Product change

The single LSP admission owner is `tool/src/lsp/document_store.rs`.
`classify_source(uri, language_id)` matches only the final URI extension and
the exact client language id. It has no case folding, Unicode normalization,
directory-name fallback, locale inference, or unknown-extension fallback.

The exact source hunk is:

```rust
"ddn" | "또니" if matches!(language_id, "ddn" | "ddonilang") => {
    Some(SourceKind::DdnKoreanDefault)
}
"ddl" if matches!(language_id, "ddl" | "ddonilang") => Some(SourceKind::Ddl),
"옮김" if matches!(language_id, "옮김" | "ddonilang") => Some(SourceKind::Ddl),
_ => None,
```

`DocumentSnapshot` stores the admitted `SourceKind`; all consumers use that
stored classification. Formatting no longer maintains a second URI suffix
registry. Unknown and mismatched documents remain lifecycle-visible but are
stored as `Unsupported`, so semantic consumers fail closed without changing
the existing notification lifecycle contract.

The VS Code manifest and package test bind the four admitted extensions and
the `ddonilang` snippet language. README surface documentation lists the same
four extensions.

Changed product paths (7):

- `tool/src/lsp/document_store.rs`
- `tool/src/lsp/mod.rs`
- `tool/src/lsp/server.rs`
- `tool/tests/lsp0_transport_document_sync.rs`
- `tools/vscode-ddn/package.json`
- `tools/vscode-ddn/test/extension.test.js`
- `tools/vscode-ddn/README.md`

## Verification

- `npm test --offline`: PASS; extension tests, activation tests, package
  inventory; package file count `7`, forbidden count `0`.
- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --offline`
  with isolated target: `23 passed, 0 failed`.
- `cargo test -p ddonirang-tool --test lsp_formatting --offline`:
  `7 passed, 0 failed`.
- LSP-filtered package regression (`cargo test ... lsp --offline`): all
  selected unit/integration tests passed, including transport, source
  admission, formatting, workspace navigation, rename, references, semantic
  tokens, and signature/inlay tests.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS.
- `git diff --check`: PASS; only expected CRLF normalization warnings for
  the two existing VS Code text files.

## Mutation evidence

Each mutation was applied alone, followed immediately by exact patch restore.
The restored product source hashes were checked before the next mutation.

### Blocker A

1. Removed `.또니` from `tools/vscode-ddn/package.json`.
   - RED: `extension.test.js` failed because actual extensions were
     `[.ddn, .ddl, .옮김]` rather than the required four.
   - RESTORE: `package.json` SHA-256
     `6DE6FAAAAE5B4EB972ED8049DD840E8C48BF40101B9D6DEE0B3355A51361CD91`;
     Git blob `d566b5ca15abd85232125491b53cfeaaa3910df0`.
   - GREEN: `npm test --offline` PASS.
2. Changed the snippets contribution language from `ddonilang` to `ddn`.
   - RED: `extension.test.js` failed with actual `ddn`, expected `ddonilang`.
   - RESTORE: the same package SHA-256/blob as above.
   - GREEN: `npm test --offline` PASS.

### Blocker B

1. Removed `또니` from the classifier admission arm.
   - RED: `source_admission_is_exact_and_profile_bound` failed with
     `left: None`, `right: Some(DdnKoreanDefault)`.
   - RESTORE: `tool/src/lsp/document_store.rs` SHA-256
     `6BA36E8DC759DA843B48FE5BB66D96975B906A2A3CC7DBCC958395BFC6A23D7F`;
     Git blob `87f748a20e78eec78fd4b6a7c588404ab075a1fd`.
   - GREEN: the same classifier unit passed.
2. Classified `.옮김` as `DdnKoreanDefault` instead of `Ddl`.
   - RED: `lsp37_will_save_wait_until_reuses_safe_formatting_for_live_surfaces`
     failed with `left: 0`, `right: 1`.
   - RESTORE: the same document-store SHA-256/blob as above.
   - GREEN: `lsp_formatting` passed `7/7`.

## VSIX and real-host boundary

- VSIX: `I:\home\urihanl\ddn\codex\out\lsp22c-vsix\ddn-language-0.0.1-r5.vsix`.
- `vsce`: `3.9.2`, local/offline execution.
- VSIX SHA-256:
  `8B11BAB14B70CCB124DEE9233BB3380D7B1FA1D3DE44765A111A2593AF7B367D`.
- VSIX file count: `319`.
- Forbidden/private/session/backup/test inventory count: `0`.
- Manifest extensions: `.ddn`, `.또니`, `.ddl`, `.옮김`.
- Clean-profile install: PASS; installed identity
  `ddonilang.ddn-language@0.0.1`.
- One post-fix real Host attempt was made with all four fixture surfaces.
  The log observed only built-in extensions; custom `ddn-language` activation
  and `ddonirang-lsp` were not observed. Therefore
  `REAL_HOST_ACTIVATION = NOT_OBSERVED`, not PASS.
- Task-owned Code and LSP processes after the attempt: `0`.
- Existing clean-profile evidence directories are retained; no user profile
  or updater process was modified.

## Custody

- Author and committer: `tongosu <tongosu@myarts.kr>`.
- Prohibited trailers: `0`.
- Public push, Marketplace publish, npm publish: `NO`.
- Foreign dirty paths: untouched and unstaged.
- No `tool/src/lib.rs`, SSOT, public SPEC, dependency, pack, runner, or
  history rewrite was introduced.

This handoff is evidence for independent review. It does not claim real-host
closure, release readiness, public support completion, or Human PASS.
