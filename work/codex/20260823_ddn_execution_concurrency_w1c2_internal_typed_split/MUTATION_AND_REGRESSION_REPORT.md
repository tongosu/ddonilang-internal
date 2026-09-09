# W1-C2 I1 mutation and regression report

## Fault injection

detached product HEAD 사본에서 original GREEN 뒤 다음 9개가 각각 실제 targeted Rust test RED를 만들었고 매번 원복했다. 최종 runner는 다시 23/23 GREEN이며 worktree tracked diff는 0이다.

1. provider-before-route
2. owner instance identity 무시
3. diamond 중복 실행
4. distinct provider 누락
5. worker/reachability 순서 의미화
6. provider failure 뒤 partial candidate commit 허용
7. nested send 즉시 reentry
8. external release를 commit 앞으로 이동
9. legacy/public fallback 허용

## Regression

- lang: 363/363
- tool lib: 492/492
- teul-cli: 1165/1165
- W1-C2 runner: 23/23
- W1-C1 native/source-WASM/tracked-WASM: 10/10 (success 6, failure 4)
- W1-D~F logical oracle: 65/65; workers 1/2/8와 permutation digest 유지
- W1-D~F capacity typed integration: PASS (bounded WAIT/FIFO resume/abort evidence)
- public syntax tripwire: 0
- historical W1-B/W1-C1/W1-D~F pack diff: 0

W1-C1 CLI는 compile-time SSOT custody 때문에 full detached 사본의 tracked v24.44.1 bundle을 읽도록 실행했다. implementation worktree의 `docs/ssot/**` write/diff는 0이다.

## WASM and Edge

- detached source A: `1b161d7eabd21f1996813fab53611b701abd6cd52f2345867932e636f76dcd4c`
- detached source B: same
- tracked Workbench WASM: same
- actual Microsoft Edge: W1-C1 success `00`, ambiguity failure `07`, console/page/network errors 0
- public provider browser claim: 0
