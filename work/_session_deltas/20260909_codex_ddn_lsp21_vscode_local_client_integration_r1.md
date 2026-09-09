# DDN-LSP21-VSCODE-LOCAL-CLIENT-INTEGRATION-R1 — handoff

## Previous LSP20 custody

- LSP20 product: `f0af222d2555e451af35fd166a16743081c81b55`
- LSP20 product tree: `d8c20816f82620c58a5d636c5e9590ce1b87c826`
- LSP20 handoff: `adf258d711b5686116fd053c346cb7d4458c121e`
- LSP20 focused tests, persistent black-box, three mutations, cargo check, and diff check: PASS.
- LSP20 internal push was attempted but rejected by the remote hook because a pre-existing ancestor was authored by `또니`; no ref was updated. Public push was not attempted.

## Admission and dependency disposition

- Existing extension owner: `tools/vscode-ddn`.
- Existing package: syntax-only shell; no extension `main`, client entrypoint, or process owner.
- Repository root `package.json`/`package-lock.json` contain Playwright only; no `vscode-languageclient`.
- Repository `node_modules/vscode-languageclient`: absent.
- `npm cache ls vscode-languageclient --parseable --offline`: no project-resolvable cache entry.
- Copies inside other installed VSCode extensions were not adopted as a product dependency.
- No download, vendoring, network dependency, or handwritten LSP client was introduced.

`DEPENDENCY_DISPOSITION = DEPENDENCY_BLOCKER_FOR_CLIENT`

## Unit A product result

Product commit: `59ad6119edfdefb578014399778ba942dbe76e08`

- tree: `6dcfddadd70c4085932b87e3935e48eb9c781ae1`
- parent: `adf258d711b5686116fd053c346cb7d4458c121e`
- author/committer: `tongosu <tongosu@myarts.kr>`
- prohibited trailer count: 0
- changed paths: exactly `tools/vscode-ddn/package.json` and `tools/vscode-ddn/README.md`.
- language id: `ddonilang`.
- file associations: `.ddn`, `.ddl`, `.옮김`.
- configuration: exact `ddonilang.lsp.executable` override and bounded `ddonilang.lsp.autoDiscover` setting.
- syntax/configuration surface remains the existing owner; no semantic parser or LSP owner was duplicated.

This is a dependency-free language-registration/configuration slice. It does not claim extension activation code, stdio client startup, diagnostics/completion delivery through VSCode, or process lifecycle management.

## Verification

- Node JSON/config assertion over `tools/vscode-ddn/package.json`: `VSCODE_UNIT_A_CONFIG=PASS`.
- `git diff --check`: PASS.
- LSP20 server regression evidence reused from the fixed target; no LSP20 verification was repeated.
- network access: 0; source upload: 0; remote server: 0; new dependency: 0.

## Requested client mutations

The three client/process mutations are not executable against this Unit A slice because no client/process owner exists and the required dependency is unavailable offline:

1. executable override ignored — `NOT_RUN_DEPENDENCY_BLOCKER`;
2. DDN activation event removed — `NOT_RUN_DEPENDENCY_BLOCKER`;
3. shutdown process cleanup removed — `NOT_RUN_DEPENDENCY_BLOCKER`.

No RED/GREEN claim is made for these unimplemented client behaviors. The dependency-free configuration assertion above is the only Unit A focused evidence.

## Boundary and next gate

- marketplace/VSIX/public release: not claimed.
- public GitHub push: NO.
- internal push: not yet attempted for LSP21.
- product dirty/staged residue: none in owned paths.
- foreign dirty paths: untouched and unstaged.
- next exact action: obtain an approved offline-resolvable `vscode-languageclient` dependency/cache or owner decision to keep the client slice blocked; then implement the stdio client in the same owner path and execute the three client mutations.

