# DDN-LSP executable-selection recovery — handoff

상태: `IMPLEMENTED_PENDING_REVIEW`

## 대상 계보

- Product: `8e4967deee793a9a5be9db1a922de68c73913083`
- Product tree: `5625e9ee8eaf4cea53ab9b613433e0acfad73af6`
- Product parent: `d9a5b7c414c6c54820a69df4de744c23ae44277f`
- Product author/committer: `tongosu <tongosu@myarts.kr>`
- Product paths: `tools/vscode-ddn/extension.js`, `tools/vscode-ddn/test/activation.test.js`

기존 `ddonilang.selectLanguageServerExecutable` 구현을 재사용해 시작 실패 알림에
`실행파일 선택` action을 연결했다. 선택된 파일은 기존 regular-file, basename, absolute-path
검증을 통과해야 하며, 설정 저장 뒤 기존 `restartLanguageServer`를 한 번만 호출한다.
정상 시작 시 실패 알림 억제 상태를 해제하고, deactivate 시에도 다음 activation을 위해
초기화한다.

## 검증

```text
npm test                         PASS
  extension tests                PASS
  activation tests               PASS
  console bogae tests            PASS
  readability role parity        PASS
  package forbidden files        0
git diff --check                 PASS
```

Activation focused test는 다음 workflow를 직접 검증한다.

```text
missing executable
→ typed startup failure notification
→ `실행파일 선택` action
→ existing picker and scope save
→ single safe restart
→ running client
```

## Mutation evidence

### M1 — invalid executable validation bypass

Exact mutation:

```diff
- const failure = configuredExecutableFailure(normalized);
+ const failure = null;
```

- Mutated source SHA-256: `3899CBC791B95CF21767C9227CB3E3282F2F45F0D4EB32A20830EB73C225839A`
- RED: `activation.test.js` invalid selection assertion `1 !== 0`
- Exact restore: `const failure = configuredExecutableFailure(normalized);`
- Restored source SHA-256: `AAD065D4F85AD0AA6CA807FD9B34B5727E19F84C16153DF30BCAEDACEEB05AC1`
- GREEN: `node test/activation.test.js` PASS

### M2 — duplicate restart guard removal

Exact mutation:

```diff
 function restartLanguageServer(context, vscode) {
-  if (restartInFlight) {
-    return restartInFlight;
-  }
```

- Mutated source SHA-256: `4587492CF15590F550F01FC6A0C4C1D95F7CE43B1A85CAD5EBE38C6BFB111AB7`
- RED: `activation.test.js` concurrent restart identity assertion failed (`Promise` objects were not reference-equal)
- Exact restore: restored the `restartInFlight` guard
- Restored source SHA-256: `AAD065D4F85AD0AA6CA807FD9B34B5727E19F84C16153DF30BCAEDACEEB05AC1`
- GREEN: `node test/activation.test.js` PASS

## VSIX artifact

- Tool: `@vscode/vsce 3.9.2` (`node_modules/.bin/vsce.cmd`)
- Path: `I:\home\urihanl\ddn\codex\out\lsp-executable-recovery-r1\ddn-language-0.0.1-executable-recovery-r1.vsix`
- SHA-256: `7FF7B7EE095BD50AD714C83C72B1E23D6C9789EDD606813CA4B30BFBBB6A54C3`
- VSIX files: `10`
- Forbidden package files: `0`

실제 VS Code Host와 updater/mutex 상태는 이 handoff에서 주장하지 않는다.
독립 reviewer가 위 product target과 이 handoff를 결속해 별도 verdict를 발급해야 한다.
