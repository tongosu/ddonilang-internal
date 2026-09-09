# DDN-LSP22B-VSCE-NETWORK-DEPENDENCY-OWNER-APPROVAL-R1 — handoff

## Authority and custody

```ini
OWNER_APPROVAL = YES
PACKAGE = @vscode/vsce
EXACT_VERSION = 3.9.2
NETWORK_SOURCE = https://registry.npmjs.org/
INSTALL_SCOPE = tools/vscode-ddn development dependency only
PUBLISH_AUTHORITY = NO
MARKETPLACE_LOGIN = NO
GLOBAL_INSTALL = NO
CREDENTIAL_USE = 0
PUBLIC_PUSH = NO
```

LSP22 and its handoff were preserved. Existing successor `021374d5bf92098d8b38066f2a1fb70f791680ae` was not rewritten or rebased.

```makefile
BASE_PRODUCT = 3270f58383d6675e048570b3d276ea7becb83a75
BASE_HANDOFF = 5b433dbd918883db42cc91b493e3183306fb92de
INTERMEDIATE_SUCCESSOR = 021374d5bf92098d8b38066f2a1fb70f791680ae
PRODUCT_FIXED = 7e4888e5be74b5dedab18561d4ccc6506517da6a
PRODUCT_TREE = e0e81c2a21e652273dbeafcb5c468d92e9190097
PRODUCT_PARENT = b8a54e74efe4bafd88ea569d3663b0b039669b20
MERGE_COUNT = 0
```

## Product change

Only these four product paths are in the product commit:

```text
tools/vscode-ddn/.vscodeignore
tools/vscode-ddn/package-lock.json
tools/vscode-ddn/package.json
tools/vscode-ddn/test/package-inventory.js
```

`@vscode/vsce` was added as exact dev dependency `3.9.2`. The approved registry install,
clean install, and package tests passed. No global install, publish, marketplace login, or
credential use occurred.

```ini
VSCODE_LANGUAGECLIENT_VERSION = 8.1.0
VSCE_VERSION = 3.9.2
LOCKFILE_SHA256 = d81501daff6d37f7ab7393e2d24d5d5dd5c476126fd7c297ca3103d45b3835c9
```

The package inventory guard covers seven allowed source files and excludes test, legacy,
quickfix, internal, session, backup, secret, environment, and packaging residue.

## VSIX evidence

```makefile
VSIX_PATH = I:\home\urihanl\ddn\codex\out\lsp22b-vsix\ddn-language-0.0.1-r3.vsix
VSIX_SHA256 = 8B7071D4E3C66C044A3D4F265F94A63E339831E3AEA8746DF170AF181EA3A29B
VSIX_FILE_COUNT = 319
VSIX_RUNTIME_DEPENDENCY_PATH_COUNT = 310
VSIX_FORBIDDEN_FILE_COUNT = 0
PACKAGE_MANIFEST_SHA256 = 12b55607dd4f8be2d2fbd7f637815334369e180ad0650c18ab663ee2645a7125
```

The VSIX contains `extension/package-lock.json` and the runtime language-client/protocol
packages. No `@vscode/vsce`, `@types`, or `typescript` development residue was present.

## Mutation evidence

Each mutation was applied alone, tested RED, and restored before the next mutation. Product
files were not staged during mutation. M1 and M2 use the original/restore `extension.js`
SHA-256 `C59CC700A87449E3E8E4318FCCADC2E3E78986DE33D7E890EB498F95CDE2F5A9` and Git blob
`93c22942646b606f20684b213c354597383f4463`.

### M1 — executable discovery rejects symlink/directory

```diff
-return stat.isFile() && !stat.isSymbolicLink();
+return !stat.isSymbolicLink();
```

RED: `true !== false` at `test/extension.test.js:66`.

Exact restore: original/restore SHA-256 and blob above; `npm test` GREEN.

### M2 — deactivate cleanup stops the client

```diff
-return client.stop();
+return undefined;
```

RED: `0 !== 1` at `test/activation.test.js:85`.

Exact restore: original/restore SHA-256 and blob above; `npm test` GREEN.

### M3 — language activation event is required

```diff
 "activationEvents": [
   "onLanguage:ddonilang"
 ],
```

Mutation: the activation event array was replaced with `[]`.

RED: actual `[]`, expected `["onLanguage:ddonilang"]` at `test/extension.test.js:13`.

Exact restore: `package.json` SHA-256
`819B28CC4954D912D30ECDED76C0A978199732497A903E83C5C552EBA5490717`, Git blob
`ada82f8a7914333e4fde1afa3a2e91b31251b0b6`; `npm test` GREEN.

### M4 — forbidden internal file fails package inventory

```diff
 expectedFiles = [
   ...
+  "legacy/README.md",
 ]
```

RED: `AssertionError: actual [{ bytes: 503, path: 'legacy/README.md', sha256: '0c61cb3561205ef0761e83ceb47d5343a789970f453c1b8a258d6b403ceb1ce2' }] expected: []` at `test/package-inventory.js:52:8`.

Exact restore: `test/package-inventory.js` SHA-256
`1233AD88CB0E5A27366EFFAF452E924903AFD056F1C89FEE637C2FF9EF3517A2`, Git blob
`602b4b382a5b2991868b3882ec9f0243b6ab1103`; `npm test` GREEN with
`PACKAGE_FILE_COUNT=7`, `PACKAGE_FORBIDDEN_FILE_COUNT=0`, and manifest SHA-256
`12b55607dd4f8be2d2fbd7f637815334369e180ad0650c18ab663ee2645a7125`.

## Validation and environment boundary

```ini
NPM_CI = PASS
NPM_TEST = PASS
CARGO_CHECK = PASS (cargo check -p ddonirang-tool)
LSP_BLACKBOX_REGRESSION = PASS before EOF (diagnostics/completion/definition/references/signatureHelp/rename/documentHighlight/semanticTokens/open-document navigation)
DIFF_CHECK = PASS
VSIX_CREATED = YES
VSIX_INSTALL_SMOKE = BLOCKED_ENVIRONMENT
EXTENSION_HOST_SMOKE = BLOCKED_ENVIRONMENT_AFTER_3_ATTEMPTS
DDN_DDL_ONGIM_REAL_HOST_ACTIVATION = NOT_VERIFIED
REMOTE_SERVER_DEPENDENCY = 0
SOURCE_UPLOAD = 0
```

The clean installation directory remained empty because VS Code reported the
`vscode-updating` mutex and waited for the updater. The updater was not terminated and no
indefinite retry was made. Therefore real Extension Host activation, `.ddn`/`.ddl`/`.옮김`
activation, and real-host process cleanup are not claimed as PASS. The black-box stdio
checks do not substitute for this blocked real-host gate.

```ini
DEACTIVATE_PROCESS_CLEANUP = NOT_VERIFIED_REAL_HOST
PROCESS_RESIDUE = 0 for ddonirang-lsp.exe at checkpoint
READY_FOR_ONE_FINAL_INDEPENDENT_REVIEW = NO
LSP22_STATUS = PRODUCT_FIXED_PENDING_CLEAN_INSTALL_AND_REAL_HOST_SMOKE
NEXT_EXACT_ACTION = wait for updater to naturally release, then rerun final r3 clean install and Extension Host smoke; do not reimplement LSP22B
```

## Handoff custody

This file is the docs-only handoff for the product commit above. It must be committed as a
separate commit with no foreign files staged.

```ini
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
PUBLISH = NO
MARKETPLACE = NO
NPM_PUBLISH = NO
FORCE_PUSH = NO
HISTORY_REWRITE = NO
```
