# DDN-LSP42-READABILITY-REGRESSION-AND-VSIX-CANDIDATE-R1 — HANDOFF

## Scope

- Packaging input target: LSP40 product `db3dd6af524695b6bb58cc24f952b0eaed5e3e1c`.
- Product tree: `b44666d1229320c2d2031c6658e902d7621ccb86`.
- Product parent: `e962f03342c6e7b99c03e9d4329927c41b32d326`.
- No product bytes changed for LSP42; no no-op product commit was created.
- VSCE: `@vscode/vsce 3.9.2`, reused from the existing local dependency; no network download.
- Source lockfile SHA-256: `D81501DAFF6D37F7AB7393E2D24D5D5DD5C476126FD7C297CA3103D45B3835C9`.

## VSIX evidence

- Path: `I:\home\urihanl\ddn\codex\out\lsp39-42-vsix\ddn-language-0.0.1-r6-final.vsix`
- SHA-256: `051ED04B03A85BC0FEA14C8F8B8C41A27378AB1A449EDB3340D436A4A42A24A1`
- File count: `9`
- Manifest SHA-256 over sorted `path|bytes|sha256` entries: `14d1cd64cf239d88a023789879b9911e0e278c04ac61dd29cd8fc54eb52dfb5a`
- Forbidden file count: `0`
- Packaged extension registration: `.ddn`, `.또니`, `.ddl`, `.옮김`
- Packaged grammar: `./syntaxes/ddn.tmLanguage.json`
- Packaged status command: `ddonilang.showLanguageServerStatus`
- Package inventory source check: 7 files, forbidden count 0, PASS.
- VSCE emitted warnings for missing repository metadata and missing LICENSE file; no license file was invented in this packaging-only unit.
- Offline reinstall was not claimed: `OFFLINE_REINSTALL = EXACT_NONCLAIM` because the real clean Extension Host gate remains blocked externally.

## Packaging mutation evidence

1. `M1_DDONI_REGISTRATION_REMOVED`
   - Temporary diff: removed `.또니` from `contributes.languages[0].extensions`.
   - RED: package-contract assertion failed with `Error: extension matrix`.
   - Exact restore: restored the line; working-copy SHA-256 returned to `8C264089DE2946706DE65A472A7D6245B1AA44895D578C56472117BD54A41DBA`.
   - GREEN: package-contract assertion passed.

2. `M2_GRAMMAR_CONTRIBUTION_REMOVED`
   - Temporary diff: removed the `syntaxes/ddn.tmLanguage.json` grammar contribution.
   - RED: package-contract assertion failed with `Error: grammar contribution missing`.
   - Exact restore: restored the task-owned package file from the fixed product HEAD; target-blob SHA-256 `1A7563AF347526D3D3DE1591609920B248F4AFC5CD31D24D0AEF090E13DFB779`.
   - GREEN: grammar contribution assertion passed.

3. `M3_STATUS_COMMAND_CONTRIBUTION_REMOVED`
   - Temporary diff: removed the `ddonilang.showLanguageServerStatus` command contribution.
   - RED: package-contract assertion failed with `Error: status command contribution missing`.
   - Exact restore: restored the task-owned package file from the fixed product HEAD; target-blob SHA-256 `1A7563AF347526D3D3DE1591609920B248F4AFC5CD31D24D0AEF090E13DFB779`.
   - GREEN: status command contribution assertion passed.

4. `M4_PACKAGE_FORBIDDEN_GUARD_REMOVED`
   - Temporary diff: removed `test/**` from `.vscodeignore`.
   - RED: existing `npm run package:inventory --prefix tools/vscode-ddn` failed with `missing .vscodeignore rule: test/**`.
   - Exact restore: restored `.vscodeignore`; SHA-256 returned to `1397483E1AA987AAE21683D0A52652C4F5563ABDDD1D96543A681BC10C6E658B`.
   - GREEN: existing package inventory passed with forbidden count 0.

## Custody and limits

- LSP39 product/handoff and LSP40 product/handoff remain separate linear commits.
- LSP42 is docs-only packaging evidence; no product, SSOT, public SPEC, normal VS Code profile, or remote state changed.
- `LSP41_STATUS = HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`; no clean-profile retry loop and no updater/normal-profile termination.
- Author/committer for this handoff: `tongosu <tongosu@myarts.kr>`.
- `READY_FOR_INDEPENDENT_REVIEW = YES` for the LSP39 and LSP40 fixed targets; LSP42 is packaging evidence bound to the LSP40 target.
