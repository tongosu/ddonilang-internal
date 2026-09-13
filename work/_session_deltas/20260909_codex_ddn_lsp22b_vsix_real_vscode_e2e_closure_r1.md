# DDN-LSP22B-VSIX-AND-REAL-VSCODE-END-TO-END-CLOSURE-R1

## 계보

기존 LSP22 client 구현을 재구현하지 않고 packaging boundary만 successor로 추가했다.
`3270f583` 이후 branch에 이미 존재하던 unrelated successor `021374d5`는 수정·rebase·amend하지 않았다.

```ini
BASE_PRODUCT = 3270f58383d6675e048570b3d276ea7becb83a75
BASE_HANDOFF = 5b433dbd918883db42cc91b493e3183306fb92de
INTERVENING_EXISTING_SUCCESSOR = 021374d5bf92098d8b38066f2a1fb70f791680ae
FINAL_PRODUCT_TARGET = 32b6b8a7ad2a3d33baebda49dec35e13a9744897
FINAL_PRODUCT_TREE = 144dc922617ae727305d5d6f0d1afbab4929bffe
FINAL_PRODUCT_PARENT = 021374d5bf92098d8b38066f2a1fb70f791680ae
```

## VSIX tool gate

```ini
VSCE_VERSION = NOT_FOUND
VSIX_TOOL_BLOCKER = OWNER_NETWORK_APPROVAL_REQUIRED
NETWORK_DOWNLOAD = NO
```

`@vscode/vsce` command, workspace copy, and offline npm cache를 확인했으나 사용할 수 없었다.
따라서 VSIX 포맷을 손으로 재구현하거나 패키지를 추가 다운로드하지 않았다.

## deterministic package inventory

`.vscodeignore`를 추가해 다음 경계를 명시했다.

```text
node_modules/**
test/**
legacy/**
quickfix/**
work/**
docs/**
backup/**
secret/**
```

허용 inventory는 다음 7개로 고정했다.

```text
README.md
extension.js
language-configuration.json
package-lock.json
package.json
snippets/ddn.code-snippets
syntaxes/ddn.tmLanguage.json
```

```ini
VSIX_PATH = NONE
PACKAGE_FILE_COUNT = 7
PACKAGE_FORBIDDEN_FILE_COUNT = 0
PACKAGE_MANIFEST_SHA256 = 5846beab9fc1a0261f91baf338fbb4c0b9af05d629857556d85122402d5958c5
LOCKFILE_SHA256 = 140ac2ffcca91d6fbc9dcc812bc460ffd01b4837394b7c144335d319a2be31ea
```

inventory 실행은 `npm test`에 포함되어 deterministic file list와 각 파일 SHA-256을 출력한다.

## 검증

```ini
VSCODE_LANGUAGECLIENT_VERSION = 8.1.0
NPM_CI = PASS
OFFLINE_REINSTALL = PASS
NPM_TEST = PASS
CARGO_CHECK = PASS
LSP_REGRESSION = PASS
DIFF_CHECK = PASS
```

기존 LSP black-box와 `lsp_completion` 15개, `lsp_definition` 3개, `lsp_diagnostics` 10개가 PASS했다.

## Extension Host 환경 결과

격리된 `user-data-dir`와 `extensions-dir`에서 VS Code `1.136.1` Extension Development Host를 세 번 시도했다.
모두 설치 프로그램의 정상 updater가 보유한 `vscode-updating` mutex로 차단됐다.

```text
checkInnoSetupMutex: vscode-updating is held
checkInnoSetupMutex: vscode-updating still held after 30837ms, giving up
Error: Code is currently being updated. Please wait for the update to complete before launching.
```

다른 사용자의 updater process를 종료하지 않았다. 실제 host activation, `.ddn`/`.ddl`/`.옮김`별 activation, 실제 VSIX install smoke는 이 환경에서 PASS로 주장하지 않는다.

```ini
EXTENSION_HOST_SMOKE = BLOCKED_ENVIRONMENT_AFTER_3_ATTEMPTS
VSIX_INSTALL_SMOKE = NOT_RUN
VSCODE_EXTENSION_ACTIVATION = NOT_VERIFIED_IN_HOST
LOCAL_LSP_SERVER_START = NOT_VERIFIED_IN_HOST
DDN_DDL_ONGIM_ACTIVATION = NOT_VERIFIED_IN_HOST
DIAGNOSTICS = SERVER_AND_UNIT_PASS_HOST_UNVERIFIED
COMPLETION = SERVER_AND_UNIT_PASS_HOST_UNVERIFIED
NAVIGATION = SERVER_AND_UNIT_PASS_HOST_UNVERIFIED
DEACTIVATE_PROCESS_CLEANUP = UNIT_PASS_HOST_UNVERIFIED
```

시도 후 확인한 task-owned local `ddonirang-lsp` process residue는 0이었다.

## mutation evidence

M1/M2/M3는 predecessor LSP22 handoff에서 이미 RED→exact restore→GREEN으로 고정되어 있다.
이번 packaging unit의 M4도 단독 수행했다.

### M4 forbidden inventory insertion

```diff
 const expectedFiles = [
   "README.md",
   "extension.js",
+  "legacy/README.md",
   "language-configuration.json",
```

RED:

```text
AssertionError: actual [{ path: 'legacy/README.md', ... }]
expected: []
at test/package-inventory.js:38:8
```

복원:

```ini
TARGET = tools/vscode-ddn/test/package-inventory.js
ORIGINAL_SHA256 = 5A952AA309A8BFA953C6ED01D7618B784DBFECC3494B2C10E268043FF570E8B3
ORIGINAL_BLOB = 4b75163e27ec75224fc272f215fdcecc0880d8db
RESTORE_SHA256 = 5A952AA309A8BFA953C6ED01D7618B784DBFECC3494B2C10E268043FF570E8B3
RESTORE_BLOB = 4b75163e27ec75224fc272f215fdcecc0880d8db
GREEN = npm test; inventory 7 files, forbidden 0
```

## commit 경계

```text
32b6b8a7ad2a3d33baebda49dec35e13a9744897
  feat(vscode): constrain extension package inventory
  tools/vscode-ddn/.vscodeignore
  tools/vscode-ddn/package.json
  tools/vscode-ddn/test/package-inventory.js
```

작성자·커미터는 `tongosu <tongosu@myarts.kr>`이고 prohibited trailer는 0이다.

```ini
REMOTE_SERVER_DEPENDENCY = 0
SOURCE_UPLOAD = 0
UNEXPECTED_PACKAGE_FILES = 0
PRIVATE_EXTENSION_COPY_REUSE = 0
PUBLIC_PUSH = NO
FORCE_PUSH = NO
HISTORY_REWRITE = NO
```

```ini
LSP22_STATUS = PRODUCT_FIXED_PENDING_VSIX_AND_REAL_HOST_SMOKE
READY_FOR_ONE_FINAL_INDEPENDENT_REVIEW = NO
NEXT_EXACT_ACTION = @vscode/vsce exact version과 network 사용 승인 또는 기존 vsce 제공 후 동일 fixed target에서 VSIX/clean-install/real-host smoke 수행
```
