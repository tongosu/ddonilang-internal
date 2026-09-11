# DDN-LSP38 real-host review packet R1

## Exact target binding

```ini
PRODUCT_FIXED = d7af9f9a316fe31cea31445fb5b0a5ff3769e3a6
PRODUCT_TREE = 14f9ecaae8bd02f0dcc8e55ffc6eeb927d73e01d
PRODUCT_PARENT = 8d13722809f819706c23e7df98d0899a0135b35a
HANDOFF = b7aef31091feee867ca62ca36aba1d40cfe9d13c
HANDOFF_PARENT = d7af9f9a316fe31cea31445fb5b0a5ff3769e3a6
MERGE_COUNT = 0
```

The product commit changes exactly these seven paths:

```text
tool/src/lsp/document_store.rs
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/tests/lsp0_transport_document_sync.rs
tools/vscode-ddn/README.md
tools/vscode-ddn/package.json
tools/vscode-ddn/test/extension.test.js
```

The handoff commit changes exactly one docs path:

```text
work/codex/DDN_LSP38_SOURCE_EXTENSION_PROFILE_BINDING_HANDOFF_R1.md
```

## Product evidence supplied to independent review

- Manifest and client selector surfaces are `.ddn`, `.또니`, `.ddl`, `.옮김`.
- `.또니` and `.ddn` bind to the canonical DDN source kind.
- `.ddl` and `.옮김` bind to DDL.
- Unknown extensions and profile/language mismatches become `Unsupported`;
  no locale, directory, case, or fallback inference is used.
- Four mutations were executed independently. Each produced RED, was restored
  by exact patch, and produced GREEN: two manifest/client mutations and two
  source-classifier mutations.
- `npm test --offline`: PASS.
- LSP focused and filtered regressions: PASS.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS.
- `git diff --check`: PASS.
- Product author/committer: `tongosu <tongosu@myarts.kr>`.
- Prohibited trailer count: `0`.

## Fixed VSIX

```ini
VSIX_PATH = I:\home\urihanl\ddn\codex\out\lsp22c-vsix\ddn-language-0.0.1-r5.vsix
VSIX_SHA256 = 8B11BAB14B70CCB124DEE9233BB3380D7B1FA1D3DE44765A111A2593AF7B367D
VSIX_FILE_COUNT = 319
VSIX_FORBIDDEN_FILE_COUNT = 0
VSCE_VERSION = 3.9.2
```

Clean-profile install was successful and reported:

```text
ddonilang.ddn-language@0.0.1
```

## Server candidate and clean profile

```ini
SERVER_EXECUTABLE = I:\home\urihanl\ddn\codex\target\debug\ddonirang-lsp.exe
SERVER_SHA256 = 5DF203F7673B3547D43C602C1FB58BC0E2F7508547192D757CF810E8824DBF67
SERVER_SIZE = 4798464
SERVER_FILE_KIND = regular file; not a symbolic link; hard-link metadata reported
CLEAN_USER_DATA = I:\home\urihanl\ddn\codex\out\lsp38-clean-user-data-r2
CLEAN_EXTENSIONS = I:\home\urihanl\ddn\codex\out\lsp38-clean-extensions-r2
```

The requested settings have been written only to the clean profile:

```json
{
  "ddonilang.lsp.executable": "I:/home/urihanl/ddn/codex/target/debug/ddonirang-lsp.exe",
  "ddonilang.lsp.autoDiscover": false
}
```

Binary build provenance from the fixed product commit to this external root
`target/debug` executable was not independently established; this is not
claimed as a provenance PASS.

## Real Host observation

One post-product-fix clean-profile Host attempt was made. The attempt used the
four fixtures `한국.또니`, `sample.ddn`, `surface.ddl`, and `surface.옮김`.

Observed facts:

- VS Code 1.137.0 launched a clean-profile Extension Host.
- The installed extension directory and VSIX identity were present.
- Extension Host logs activated only built-in extensions; no
  `ddonilang.ddn-language` activation line appeared.
- No `ddonirang-lsp.exe` child process appeared.
- No initialize response or diagnostics publication was observed.
- `main.log` recorded `Error: Error mutex already exists` for application
  shared storage.
- The computer-use surface exposed no targetable VS Code app window in this
  session, so direct UI confirmation of language mode and Problems was not
  possible.
- After the attempt, task-owned Code processes and task-owned LSP processes
  were both `0`.

Therefore the current boundary is explicitly:

```ini
REAL_HOST_ACTIVATION = NOT_OBSERVED
DDONIRANG_LSP_START = NOT_OBSERVED
REAL_HOST_DIAGNOSTICS = NOT_ASSESSED
LSP38_INDEPENDENT_VERDICT = NOT_ISSUED
```

This packet does not convert environment evidence into a product FAIL or
PASS. It is ready for the independent reviewer to bind the product evidence
and determine whether the remaining gate is environmental or requires a
minimal correction.
