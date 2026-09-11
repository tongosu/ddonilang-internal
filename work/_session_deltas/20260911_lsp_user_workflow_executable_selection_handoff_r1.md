# DDN-LSP 사용자 workflow — 실행파일 선택·검증 handoff R1

## 고정 계보

- Baseline handoff: `d2872456a36ed8a2d74085d494d4b23ea7ba5e21`
- Product commit: `0aaaf2307a403b7d8c88f099826b297a24fa367b`
- Product tree: `4071eb8f2586a8572a7153b6a4834ffc9458a610`
- Product parent: `d2872456a36ed8a2d74085d494d4b23ea7ba5e21`
- Product paths:
  - `tools/vscode-ddn/extension.js`
  - `tools/vscode-ddn/package.json`
  - `tools/vscode-ddn/test/activation.test.js`
  - `tools/vscode-ddn/test/extension.test.js`
- Author and committer: `tongosu <tongosu@myarts.kr>`
- Merge count: `0`

## User-visible workflow

The new command is `ddonilang.selectLanguageServerExecutable`.

1. Open the command palette and choose the executable-selection command.
2. Choose a local file with the existing bounded picker.
3. Reject non-absolute paths, missing paths, directories, symlinks/reparse
   points, and unsupported executable basenames without changing the existing
   setting or client.
4. Choose `Workspace` (first and recommended when a workspace is open) or
   `User` configuration scope.
5. Save the validated absolute path and reuse the existing single-flight safe
   restart owner.
6. Keep the existing status command and typed lifecycle failures available.

The four language surfaces remain `.ddn`, `.또니`, `.ddl`, and `.옮김`. No new
semantic parser, remote server, source upload, filesystem crawl, or network
dependency was introduced. No normal VS Code profile was modified.

## Tests and validation

- `npm ci --offline`: PASS, 302 packages added, 0 vulnerabilities.
- `npm test --offline`: PASS — extension, activation, Console Bogae, and
  package inventory tests passed.
- Package inventory: 7 source entries, forbidden count `0`, manifest SHA-256
  `3f15911c7e9a4d44f1be6612b002214787dd48184699d51f9f167d1c353b080f`.
- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --test lsp_semantic_tokens --offline`: PASS, `23 + 6`.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS.
- `git diff --check`: PASS.

## Mutation evidence

Mutants were applied one at a time and restored to the fixed extension blob
`3e9a2d1b2c49a180740413e671b8fc68491f396c` before the next mutation.

### M1 — invalid executable accepted

- Mutation: bypass the configured executable failure gate.
- Mutant blob: `146063a5b09ec1aa3f1c9b3a3f25082af2b2c984`.
- RED: activation test expected invalid selection to leave configuration and
  client count unchanged; the mutant recorded one configuration update.
- Exact restore: restore the gate hunk; fixed blob
  `3e9a2d1b2c49a180740413e671b8fc68491f396c`.
- GREEN: `npm test --offline` PASS.

### M2 — configuration save failure restarts the client

- Mutation: replace the save-failure `return null` with a restart call.
- Mutant blob: `ee2043c93d4d93ece76d780a765bc981aa558024`.
- RED: activation test expected null, unchanged client count, and preserved
  existing path; the mutant returned a new `FakeLanguageClient`.
- Exact restore: restore the save-failure return; fixed blob
  `3e9a2d1b2c49a180740413e671b8fc68491f396c`.
- GREEN: `npm test --offline` PASS.

### M3 — duplicate restart guard removed

- Mutation: bypass the existing `restartInFlight` single-flight guard.
- Mutant blob: `b380ef05d1b2f435f26baf01f8d2e1d00720d7f1`.
- RED: activation test failed the identity assertion that two rapid restart
  requests share one Promise.
- Exact restore: restore the `restartInFlight` guard; fixed blob
  `3e9a2d1b2c49a180740413e671b8fc68491f396c`.
- GREEN: `npm test --offline` PASS.

## VSIX seal

- Tool: `@vscode/vsce` `3.9.2` from the existing lockfile.
- Path: `I:\home\urihanl\ddn\codex\out\lsp-user-workflow\ddn-language-0.0.1-user-workflow.vsix`
- SHA-256: `e634ece9a3dae7417d2df18dd0eed3dfe844d7bd45c65b68101b94a3d147acd9`
- File count: `319`
- Forbidden file count: `0`
- Manifest contains the new command and all four extensions:
  `.ddn`, `.또니`, `.ddl`, `.옮김`.

## Remaining gates

- Real VS Code Host: `HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`; updater/mutex was not
  terminated and no retry loop was run.
- Existing non-task `ddonirang-lsp.exe` PID `29160` was not touched.
- Product status: `PRODUCT_FIXED_PENDING_REVIEW`.
- This handoff does not issue an independent PASS.
