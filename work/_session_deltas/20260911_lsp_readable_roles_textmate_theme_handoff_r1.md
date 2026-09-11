# DDN-LSP39 readable semantic roles / TextMate parity — handoff R1

## Scope

- Previous user workflow target is preserved unchanged:
  - product `0aaaf2307a403b7d8c88f099826b297a24fa367b`
  - handoff `80fd0eb6c31762cc54851dda398e0ec98ac1ac27`
- This successor covers only current syntax-role readability outside the un-authoritative LSP45 `에 따라` composite meaning.
- No LSP45 composite parser or semantic token was added.
- No `lang/**`, `core/**`, `tool/src/lib.rs`, SSOT, public SPEC, push, or real-user VS Code profile change.

## Product fixed

```ini
IMPLEMENTATION_BASE = 80fd0eb6c31762cc54851dda398e0ec98ac1ac27
PRODUCT_FIXED = ab4e909ba6488c2498bb852b58d04f9d0865a8ad
PRODUCT_TREE = 0011ae278e052269ac83decd9276616f67be5de4
PRODUCT_PARENT = 80fd0eb6c31762cc54851dda398e0ec98ac1ac27
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

Changed product paths:

- `tool/src/lsp/semantic_tokens.rs`
- `tool/tests/lsp_semantic_tokens.rs`
- `tools/vscode-ddn/package.json`
- `tools/vscode-ddn/syntaxes/ddn.tmLanguage.json`
- `tools/vscode-ddn/test/extension.test.js`
- `tools/vscode-ddn/test/package-inventory.js`
- `tools/vscode-ddn/test/readability.test.js`
- `tools/vscode-ddn/themes/ddonilang-readable-color-theme.json`

## Behavior

- Incomplete-but-lexable source preserves bounded lexical roles for atom, josa, variable/nuance, pragma, string, number, keyword, and operator tokens without inventing identifier/type identity.
- Existing semantic token legend is bound to matching TextMate scopes through `semanticTokenScopes`.
- Declaration and call-site scopes retain explicit TextMate subroles under the common function role; type definitions retain an explicit type-definition subrole.
- Current lexer josa surfaces `에`, `에서`, and `한테` are represented; this does not create an `에 따라` composite meaning.
- `Ddonilang Readable` is an opt-in contributed VS Code color theme. It does not alter user settings or auto-select a theme.

## Validation

```ini
SEMANTIC_FOCUSED = 7/7 PASS
EXTENSION_NPM_TEST = PASS
TEXTMATE_ROLE_PARITY = PASS
PACKAGE_FILE_COUNT = 8
PACKAGE_FORBIDDEN_FILE_COUNT = 0
PACKAGE_MANIFEST_SHA256 = 42bbb772eb28d6f137ce063a32637b084c66ff3c5be8fded93608d289f3a1a9b
TRANSPORT_BLACKBOX = PASS
CARGO_CHECK_DDONIRANG_LSP_OFFLINE = PASS
GIT_DIFF_CHECK = PASS
RUSTFMT_CHECK = PASS
```

Transport black-box included initialize-before-EOF, fragmented UTF-8, persistent lifecycle, semantic token full/delta, hover, definition, document/workspace symbol, formatting, references, signature help, inlay hints, rename, highlight, type definition, folding, and selection range.

## Mutation evidence

Each mutation was applied one at a time, produced the expected RED, and was restored before the next mutation.

| Mutation | RED | Exact restore | GREEN |
| --- | --- | --- | --- |
| M1 remove lexical atom/josa/variable fallback branches | focused Rust assertion failed for token type `2` | `tool/src/lsp/semantic_tokens.rs` blob `d4d32428c1797e51e02ec086fa0590abf044fc54` | focused semantic test PASS |
| M2 remove keyword identifier boundary lookarounds | `readability.test.js` failed on missing `(?<!` guard | `tools/vscode-ddn/syntaxes/ddn.tmLanguage.json` blob `370e8aa336fc8d259ebb2366049284a9519a0b83` | `npm test --offline` PASS |
| M3 remove `josa` semantic-token scope mapping | `extension.test.js` deep-equality assertion failed | `tools/vscode-ddn/package.json` blob `399e662d9be7031a6374f2a53c7adfc2f2ad8b26` | `npm test --offline` PASS |

## VSIX evidence

```ini
VSIX = I:\home\urihanl\ddn\codex\out\lsp-readable\ddn-language-0.0.1-readable-r1.vsix
VSIX_SHA256 = d4963aea6bd330326c59a06357d18601ba6526b964ec59166926cad1e6ca6aac
VSIX_FILE_COUNT = 320
VSIX_FORBIDDEN_FILE_COUNT = 0
VSIX_REQUIRED_GRAMMAR_THEME_LOCKFILE = PRESENT
NETWORK_DOWNLOAD = 0
MARKETPLACE_PUBLISH = 0
PUBLIC_PUSH = 0
```

The package contains the semantic role mapping, grammar, and opt-in readable theme. No test, internal document, backup, secret, source-map, or session file was present in the verified inventory.

## Environment and review boundary

```ini
REAL_VSCODE_HOST = HOLD_EXTERNAL_VSCODE_UPDATER_ONLY
REAL_HOST_BEHAVIOR_CLOSED = NO
SELF_PASS = NO
READY_FOR_INDEPENDENT_REVIEW = YES
```

The fixed target is awaiting the separate independent reviewer. The first user workflow remains pending its own review; this handoff does not inherit or issue a PASS for either target.
