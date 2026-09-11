# LSP44 current-document Console 보개 — handoff R1

## Scope and authority

- Unit: `LSP44_CURRENT_DOCUMENT_CONSOLE_BOGAE`
- Product base: `979c79f7b5850868c510641e330a9eeda3f8f953`
- Product commits:
  - `42787f0f2e921fecc4db079c356280f5c5b82076` — current-document Console 보개 command, bounded runtime execution, lifecycle cleanup, package contribution, and focused tests.
  - `12740689d0e2f6871061892e1a1d738f0a9dd3ad` — explicit invalid-runtime rejection coverage.
- Product tree: `2418eb83ad834283adf9c1260e3f4635e8b93faf`
- Product parent for handoff: `12740689d0e2f6871061892e1a1d738f0a9dd3ad`
- Author/committer: `tongosu <tongosu@myarts.kr>`
- Product paths: `tools/vscode-ddn/README.md`, `tools/vscode-ddn/extension.js`, `tools/vscode-ddn/package.json`, `tools/vscode-ddn/test/activation.test.js`, `tools/vscode-ddn/test/extension.test.js`, `tools/vscode-ddn/test/console-bogae.test.js`

## Implemented contract

- Command: `ddonilang.runCurrentDocumentConsoleBogae`
- Output: `Ddonilang Console 보개` output channel in the current VS Code window.
- Executable surfaces: `.ddn`, `.또니`.
- Typed non-executable surfaces: `.ddl`, `.옮김`.
- Runtime command: `ddonilang currentline-run --cell <task-owned-temp-file> --source-profile v1-core-v25`.
- Runtime admission: exact configured local regular executable or bounded workspace target discovery; directories, symlinks, missing paths, and unsupported filenames fail closed.
- Snapshot boundary: only the active document version captured before launch may publish output.
- Lifecycle: one active execution per URI; stale, failed, cancelled, duplicate, and deactivate paths publish no success summary and clean task-owned temporary files/child process.
- No `teul-cli`, JS/Python lowering, filesystem crawl, source upload, remote runtime, or network dependency.

## Evidence

### Focused and regression tests

- `npm test` in `tools/vscode-ddn`: PASS.
  - extension tests: PASS
  - activation tests: PASS
  - Console 보개 tests: PASS
  - package inventory: 7 source/package files, forbidden count 0
- Official runtime smoke: `ddonilang.exe currentline-run --cell ... --source-profile v1-core-v25` with `1 보여주기.` returned exit 0 and stdout `1`.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS.
- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --test lsp_semantic_tokens --offline`: PASS, 23 + 5.
- `git diff --check`: PASS for task-owned product paths.

### Mutation evidence

Fixed extension blob for all restores: `bb932c55a53ec3a72f3fcd4e4d0a603491b66a91`.

1. **M1 — executable revalidation bypass**
   - Exact hunk: in `resolveRuntimeExecutable`, replace `return isRegularExecutable(exactPath, allowedNames) ? exactPath : null;` with `return exactPath;`.
   - Mutant blob: `75c9ab182af27c9c24af20f986770bfcac5dcbee`.
   - RED: `extension tests` rejected expectation; unsupported `other-server.exe` was returned as an executable path instead of `null`.
   - Restore: fixed blob above; exact restore verified.
   - GREEN: full `npm test` PASS.

2. **M2 — stale-version guard removal**
   - Exact hunk: remove the `isCurrentDocumentSnapshot(...)` rejection block before output-channel publication.
   - Mutant blob: `c0d6e776dcbdc7c7fb042b8dac47ca7bbad071af`.
   - RED: Console 보개 test received `stale\\n` instead of `null` after the document version changed during execution.
   - Restore: fixed blob above; exact restore verified.
   - GREEN: full `npm test` PASS.

3. **M3 — deactivate child cleanup removal**
   - Exact hunk: remove `await stopAllExecutions();` at the start of `deactivate`.
   - Mutant blob: `2ed6133fe366c36af1f2c137b02f324c19051df5`.
   - RED: Console 보개 test observed `child.killed === false` after deactivate.
   - Restore: fixed blob above; exact restore verified.
   - GREEN: full `npm test` PASS.

## VSIX artifact

- Path: `I:\home\urihanl\ddn\codex\out\lsp44-vsix\ddn-language-0.0.1-r8.vsix`
- SHA-256: `424226D1F8639C7EC5EE04708D42B05FEE7AE2E90BA2BEAF5F36C06172873F2A`
- Contents: 9 archive entries; extension payload includes `extension.js`, `package.json`, `package-lock.json`, grammar, snippets, and language configuration.
- Forbidden inventory matches: 0.
- `@vscode/vsce` was reused from the existing local development dependency; no network download or publish was performed.

## Environment and nonclaims

- Real VS Code Host: `HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`; updater/mutex was not force-terminated and no retry loop was run.
- Actual Extension Host activation, UI output rendering, and process cleanup in a real VS Code window remain unassessed.
- Existing foreign dirty paths were not modified, staged, or committed. The observed foreign `ddonirang-lsp.exe` PID 29160 was not touched.
- LSP39, LSP40, and LSP43 independent verdicts remain pending; this handoff does not self-PASS them or LSP44.

## Next gate

Independent review may bind this handoff to product target `12740689d0e2f6871061892e1a1d738f0a9dd3ad`. If the updater/mutex becomes observably released, run one clean-profile real Host smoke; otherwise preserve `HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`.
