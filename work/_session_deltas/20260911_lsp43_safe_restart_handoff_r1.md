# DDN-LSP43-SAFE-LANGUAGE-SERVER-RESTART-R1 — HANDOFF

## Scope

- Baseline: LSP42 final head `c7223aba18bbff800fa4d80838e84d00e78588bb`.
- Product commit: `32641a7451f7da3d917d42ce65122f59d491e52b`.
- Product tree: `e54d1b3f43fde87c209d55af2ed6786d3583474f`.
- Product parent: `c7223aba18bbff800fa4d80838e84d00e78588bb`.
- Product paths: `tools/vscode-ddn/README.md`, `tools/vscode-ddn/extension.js`, `tools/vscode-ddn/package.json`, `tools/vscode-ddn/test/activation.test.js`, `tools/vscode-ddn/test/extension.test.js`.
- No `tool/src/lsp/**`, `lang/**`, core/runtime, SSOT, public SPEC, normal VS Code profile, or foreign dirty path was changed.

## Product behavior

- Adds one canonical command identity: `ddonilang.restartLanguageServer`, contributed as `Ddonilang: Restart Language Server` and activated by `onCommand:ddonilang.restartLanguageServer`.
- Reuses the existing bounded executable resolver and re-reads exact configuration on every restart.
- Stops and detaches the old client before starting a replacement; at most one active client and one task-owned server process are allowed.
- Concurrent restart requests share one in-flight Promise and do not create a second client.
- Stop failure becomes `SERVER_STOP_FAILED`; start failure becomes `SERVER_START_FAILED`; both clear the active client reference and publish `failed`, never stale `running`.
- A later restart can recover after either typed failure.
- Supported surfaces remain exactly `.ddn`, `.또니`, `.ddl`, `.옮김`. No filesystem crawl, remote fallback, source upload, or user-profile mutation was added.

## Mutation evidence

Fixed source blob for `tools/vscode-ddn/extension.js`:

- Git blob: `f11776375849a434bc12a39279b0d4f8a07f6b0f`.
- Restored file SHA-256: `258b27dfb99e3d6d85a801ea6c5c35cff0e981efd14fd9530372a80992587839`.

1. `M1_DUPLICATE_RESTART_GUARD_REMOVED`
   - Exact temporary diff: removed the `if (restartInFlight) { return restartInFlight; }` guard.
   - RED: `activation.test.js` failed at the same-Promise assertion (`actual: Promise`, `expected: Promise`, `strictEqual`); the unguarded second path also attempted an actual `vscode` load after the test harness was restored.
   - Exact restore: `git restore --source=HEAD -- extension.js`; blob returned to `f11776375849a434bc12a39279b0d4f8a07f6b0f`, SHA-256 returned to `258b27dfb99e3d6d85a801ea6c5c35cff0e981efd14fd9530372a80992587839`.
   - GREEN: `npm test` passed.

2. `M2_OLD_CLIENT_CLEANUP_REMOVED`
   - Exact temporary diff: removed `activeClient = null` before awaiting `client.stop()`.
   - RED: `activation.test.js` returned the old `FakeLanguageClient` instead of constructing the replacement; assertion failed at the replacement identity check.
   - Exact restore: same HEAD blob and SHA-256 as above.
   - GREEN: `npm test` passed.

3. `M3_FAILED_RESTART_STATUS_CLEAR_REMOVED`
   - A partial first mutation removing only the inner `lifecycleState = "failed"` was not accepted because the outer fallback still made the test GREEN; it was restored without evidence.
   - Exact accepted temporary diff: removed both the `startClient` failure assignment and the restart-wrapper fallback assignment that publish `failed` after a failed start.
   - RED: `activation.test.js` observed `actual 'starting'` instead of `expected 'failed'` after failed restart.
   - Exact restore: same HEAD blob and SHA-256 as above.
   - GREEN: `npm test` passed.

All mutation residue was restored before packaging and handoff creation.

## Verification

- `npm test` in `tools/vscode-ddn`: PASS; extension tests PASS, activation/restart tests PASS, package inventory 7 files, forbidden count 0.
- `node --check extension.js`: PASS.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS using task-specific target directory `I:\home\urihanl\ddn\codex\out\lsp43-cargo-target`.
- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --test lsp_semantic_tokens --offline`: PASS, 23 + 5 tests.
- `git diff --check`: PASS.
- Existing LSP39 semantic-token and LSP40 status behavior remained covered by the applicable regressions; no Rust LSP source was changed.

## VSIX successor evidence

- Path: `I:\home\urihanl\ddn\codex\out\lsp43-vsix\ddn-language-0.0.1-r7.vsix`.
- SHA-256: `0D965F6081CD26EA784A4A8E8280A4FFC9BB06063A4F7DF7C2F3FB66C82DB357`.
- Size: `44048` bytes.
- VSIX file count: `9`.
- Extension package inventory: 7 files; forbidden file count `0`.
- Package inventory manifest SHA-256: `c9abc049e5400683c6f58ae978f2af004655e33f239829205c73200e25d70d8d`.
- Packaged extensions: `.ddn`, `.또니`, `.ddl`, `.옮김`.
- Packaged commands: `ddonilang.showLanguageServerStatus`, `ddonilang.restartLanguageServer`.
- Packaged grammar: `extension/syntaxes/ddn.tmLanguage.json`.
- `@vscode/vsce` local version: `3.9.2`; no network download, publish, or Marketplace mutation.
- Offline clean reinstall: `EXACT_NONCLAIM`; no claim is made because the real Host gate remains externally blocked.

## Host and custody boundary

- `REAL_HOST_STATUS = HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`.
- No updater or mutex was force-terminated, no retry loop was run, and no normal VS Code profile was changed.
- The pre-existing foreign `ddonirang-lsp.exe` process was not touched; task-owned VSCE processes were cleaned and task process residue is 0.
- LSP39 review verdict: `PENDING`; LSP40 review verdict: `PENDING`; LSP43 is `PRODUCT_FIXED_PENDING_REVIEW`.
- `READY_FOR_INDEPENDENT_REVIEW = YES` for LSP43 target `32641a74...`, with r7 artifact evidence attached by path/hash.

## Custody

- Author/committer: `tongosu <tongosu@myarts.kr>`.
- Product commit is linear and has no prohibited trailer.
- This handoff is docs-only and changes no product, SSOT, public SPEC, remote, or normal VS Code state.
