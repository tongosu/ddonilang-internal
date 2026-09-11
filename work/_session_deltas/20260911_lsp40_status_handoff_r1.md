# DDN-LSP40-VSCODE-LSP-STATUS-AND-DISCOVERY-R1 — HANDOFF

## Scope

- LSP39 predecessor product: `330280289af99319bb585b83ce86283ebcbb18ef`
- LSP39 handoff: `e962f03342c6e7b99c03e9d4329927c41b32d326`
- LSP40 product commit: `db3dd6af524695b6bb58cc24f952b0eaed5e3e1c`
- LSP40 product tree: `b44666d1229320c2d2031c6658e902d7621ccb86`
- LSP40 product parent: `e962f03342c6e7b99c03e9d4329927c41b32d326`
- Product paths: `tools/vscode-ddn/extension.js`, `tools/vscode-ddn/package.json`, `tools/vscode-ddn/test/activation.test.js`, `tools/vscode-ddn/test/extension.test.js`
- Foreign dirty paths were not modified, staged, or restored.

## Product behavior

- Adds `Ddonilang: Show Language Server Status` and the corresponding `onCommand:ddonilang.showLanguageServerStatus` activation boundary.
- Reports extension version, active document language id, exact admitted extension, admission state, configured path or bounded discovery, lifecycle state, server PID presence, and the last typed startup failure.
- Does not print source text, complete environment variables, or a home-directory inventory.
- Reuses bounded exact candidates and rejects non-absolute paths, missing paths, directories, symlinks/reparse points, and unsupported executable filenames.
- Preserves one shared client for repeated activation and awaits client stop on deactivation.
- Supported extension set remains exactly `.ddn`, `.또니`, `.ddl`, `.옮김`; no filesystem crawl, download, remote fallback, or user-profile mutation was added.

## Mutation evidence

The restored `tools/vscode-ddn/extension.js` SHA-256 was:
`3916D65363A668A5D8B2FEF4FB0A13BDC7268C0D4C8696174B69488E6FF5B01D`.

1. `M1_DUPLICATE_CLIENT_GUARD_REMOVED`
   - Temporary diff: replaced `if (activeClient)` in `activate` with `if (false)`.
   - RED: `activation.test.js` failed because a second activation returned a different `FakeLanguageClient` instead of reusing the first.
   - Exact restore: restored `if (activeClient)`; SHA-256 returned to `3916D65363A668A5D8B2FEF4FB0A13BDC7268C0D4C8696174B69488E6FF5B01D`.
   - GREEN: npm activation test passed.

2. `M2_INVALID_EXECUTABLE_VALIDATION_BYPASSED`
   - Temporary diff: replaced the configured-path branch `isRegularExecutable(exactPath) ? exactPath : null` with `exactPath`.
   - RED: `extension.test.js` accepted a missing configured executable instead of returning `null`.
   - Exact restore: restored the `isRegularExecutable` guard; SHA-256 returned to `3916D65363A668A5D8B2FEF4FB0A13BDC7268C0D4C8696174B69488E6FF5B01D`.
   - GREEN: npm extension test passed.

3. `M3_DEACTIVATE_STOP_REMOVED`
   - Temporary diff: replaced `await client.stop()` with `undefined`.
   - RED: `activation.test.js` reported `stopCalls` `0` instead of `1`.
   - Exact restore: restored `const result = await client.stop()`; SHA-256 returned to `3916D65363A668A5D8B2FEF4FB0A13BDC7268C0D4C8696174B69488E6FF5B01D`.
   - GREEN: npm activation test passed.

## Verification

- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --offline`: 23 passed.
- `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline`: 5 passed.
- `npm test --prefix tools/vscode-ddn`: PASS; package inventory 7 files, forbidden count 0.
- Node syntax and package JSON parse: PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check` for LSP40 paths: PASS.
- Existing real VS Code host attempt remains separately recorded as external updater/mutex blocked; no new retry loop or forced termination was performed.
- `READY_FOR_INDEPENDENT_REVIEW = YES` for the LSP40 fixed target.

## Custody

- Author/committer: `tongosu <tongosu@myarts.kr>`.
- Product commit is linear and contains no prohibited trailer.
- This handoff changes no SSOT, public SPEC, closed predecessor target, or normal VS Code profile.
