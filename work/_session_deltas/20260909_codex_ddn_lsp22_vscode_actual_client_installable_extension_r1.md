# DDN-LSP22-VSCODE-ACTUAL-CLIENT-AND-INSTALLABLE-EXTENSION-R1

## 상태

Owner dependency decision에 따라 `vscode-languageclient@8.1.0`을 사용했다.
기존 LSP21의 언어 등록 껍데기를 local stdio client로 확장했고, 서버 semantic owner는 수정하지 않았다.

```ini
BASE_HEAD = 4377edd6aa893fef3f9f8c9bbac6d5a47e41bb47
BASE_TREE = 5249fd53fc70cf6490433f332f4902f57ec4a65f
LSP21_PRODUCT = 59ad6119edfdefb578014399778ba942dbe76e08
PRODUCT_FIXED = 3270f58383d6675e048570b3d276ea7becb83a75
PRODUCT_TREE = 76cd537ed760049f6dc7c7a408f6fb9422375364
PRODUCT_PARENT = 4377edd6aa893fef3f9f8c9bbac6d5a47e41bb47
```

## 변경 범위

```text
tools/vscode-ddn/README.md
tools/vscode-ddn/package.json
tools/vscode-ddn/package-lock.json
tools/vscode-ddn/extension.js
tools/vscode-ddn/test/extension.test.js
tools/vscode-ddn/test/activation.test.js
```

`extension.js`는 다음을 제공한다.

- `activate`/`deactivate`와 `vscode-languageclient/node`의 `LanguageClient`
- local stdio `ddonirang-lsp` 실행
- `.ddn`, `.ddl`, `.옮김`의 `file`/`untitled` selector
- 명시된 absolute regular file 우선 선택
- workspace `target/debug`·`target/release` 및 extension 기준 repository target만 검사하는 bounded discovery
- directory·symlink·UNC·상대 경로·없는 executable fail-closed
- 중복 client 방지와 deactivate 시 `client.stop()`
- 시작 실패 1회 오류 표시, 무한 재시작 없음

## dependency

```ini
VSCODE_LANGUAGECLIENT_VERSION = 8.1.0
PACKAGE_SOURCE = https://registry.npmjs.org/
LOCKFILE_SHA256 = 140ac2ffcca91d6fbc9dcc812bc460ffd01b4837394b7c144335d319a2be31ea
RESOLVED = https://registry.npmjs.org/vscode-languageclient/-/vscode-languageclient-8.1.0.tgz
INTEGRITY = sha512-GL4QdbYUF/XxQlAsvYWZRV3V34kOkpRlvV60/72ghHfsYFnS/v2MANZ9P6sHmxFcZKOse8O+L9G7Czg0NUWing==
NPM_CI = PASS
OFFLINE_REINSTALL = PASS
```

다른 VS Code extension의 private dependency는 사용하지 않았다.

## 검증

```ini
EXTENSION_UNIT_TESTS = PASS
ACTIVATION_UNIT_TESTS = PASS
NODE_SYNTAX_CHECK = PASS
LSP_BLACKBOX = PASS
LSP_REGRESSION = PASS
DIFF_CHECK = PASS
SERVER_PROCESS_RESIDUE = 0
```

실행한 기존 LSP 회귀:

```text
python tests/run_lsp0_transport_document_sync_check.py
  LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
  diagnostics/completion/definition/references/signatureHelp/rename/documentHighlight/semanticTokens/open-document-navigation before EOF=PASS
cargo test -p ddonirang-tool --test lsp_completion --test lsp_definition --test lsp_diagnostics
  lsp_completion: 15 passed
  lsp_definition: 3 passed
  lsp_diagnostics: 10 passed
```

## mutation evidence

각 mutation은 단독 적용 후 즉시 복원했다.

### M1 executable selection

```diff
-    command: executable,
+    command: process.execPath,
```

기대 RED는 non-LSP executable로 initialize가 실패하는 것이며, activation guard가 다음으로 실패했다.

```text
AssertionError: actual 'C:\\Program Files\\nodejs\\node.exe'
expected '<temp>\\ddonirang-lsp.exe'
```

복원:

```ini
TARGET = tools/vscode-ddn/extension.js
ORIGINAL_SHA256 = C59CC700A87449E3E8E4318FCCADC2E3E78986DE33D7E890EB498F95CDE2F5A9
ORIGINAL_BLOB = 93c22942646b606f20684b213c354597383f4463
RESTORE_SHA256 = C59CC700A87449E3E8E4318FCCADC2E3E78986DE33D7E890EB498F95CDE2F5A9
RESTORE_BLOB = 93c22942646b606f20684b213c354597383f4463
GREEN = npm test; extension tests: PASS; activation tests: PASS
```

### M2 deactivate cleanup

```diff
-  return client.stop();
+  return undefined;
```

RED:

```text
AssertionError: 0 !== 1
at test/activation.test.js:85:12
```

복원 hash/blob은 M1과 동일하며 복원 후 `npm test` GREEN을 확인했다.

### M3 document selector

```diff
-        "extensions": [".ddn", ".ddl", ".옮김"],
+        "extensions": [".ddn", ".ddl"],
```

RED:

```text
AssertionError: actual ['.ddn', '.ddl']
expected ['.ddn', '.ddl', '.옮김']
at test/extension.test.js:15:10
```

복원:

```ini
TARGET = tools/vscode-ddn/package.json
ORIGINAL_SHA256 = B2AF2CC6099AB2EC981CBDA7DB18D19602F17225157A00A03E343C6F3161E209
ORIGINAL_BLOB = 1bfcd7e50d7617841d9c0b80344b82f71b4d968f
RESTORE_SHA256 = B2AF2CC6099AB2EC981CBDA7DB18D19602F17225157A00A03E343C6F3161E209
RESTORE_BLOB = 1bfcd7e50d7617841d9c0b80344b82f71b4d968f
GREEN = npm test; extension tests: PASS; activation tests: PASS
```

## Extension Host / VSIX

VS Code `1.136.1`과 격리된 `user-data-dir`/`extensions-dir`로 Extension Development Host를 시도했다.
호스트는 설치 프로그램의 `vscode-updating` mutex 때문에 다음 환경 오류로 시작되지 않았다.

```text
Code is currently being updated. Please wait for the update to complete before launching.
```

따라서 실제 Extension Host child-process smoke는 `BLOCKED_ENVIRONMENT`이며, 실제 host activation을 PASS라고 주장하지 않는다. 시도 중 local LSP process residue는 0이었다.

`vsce`는 로컬에 없으므로 VSIX를 손으로 만들거나 추가 다운로드하지 않았다.

```ini
VSIX_CREATED = NO
VSIX_INSTALL_SMOKE = NOT_RUN
VSIX_PACKAGER_DEPENDENCY_REQUIRED = @vscode/vsce exact version Owner approval
```

## 경계

```ini
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
FILESYSTEM_CRAWL = 0
PRIVATE_EXTENSION_COPY_REUSE = 0
FOREIGN_DIRTY_TOUCHED = 0
PRODUCT_PATHS_OUTSIDE_OWNER = 0
PUBLIC_PUSH = NO
INTERNAL_PUSH = NOT_ATTEMPTED
```

기존 `lang/**`, `tool/**` foreign dirty와 unrelated untracked session delta는 수정·stage하지 않았다.

```ini
READY_FOR_INDEPENDENT_REVIEW = YES_WITH_EXTENSION_HOST_ENVIRONMENT_GATE
NEXT_EXACT_ACTION = VS Code updater mutex 해소 후 동일 fixed target에서 Extension Host smoke 재실행
```
