# 다음 SSOT 제품 개발계획 gap packet

이 문서는 SSOT 변경이나 신규 의미 결정이 아니라 다음 관리 트랙의 exact 입력이다.

## 현재 구현·검토 상태

- PC01 typed-local migration diagnostic: 제품·mutation·A/B WASM 검증 완료, fresh plain PASS 대기
- G14 legacy expected rejection 3건: native/WASM·mutation·detached A/B PASS, independent plain PASS 대기
- T5 14-family canonical view: historical reviewed scope 보존; current T5F grid successor는 DEFER
- W1 prior closures: 보존. 현 successor의 hardcoded-baseline runners는 현재 product diff를 stale ingress change로 판정함
- Workbench: T1/T2/T4f static/product-boundary runner PASS, actual Edge current V25 source success는 OPEN
- public projection: deterministic A/B이나 non-browser self-containment와 security path preflight FAIL

## exact gaps

1. Workbench shared source analysis가 current V25 frontdoor를 어떤 profile/entry로 소유할지 결정
2. Rust execution result가 canonical observation manifest를 언제 반드시 제공할지 current product contract 결정
3. debug `teul-cli` startup stack overflow의 개발 도구 follow-up ownership 결정; release entrypoint는 PASS
4. public test compile에서 private `include_str!` fixtures를 public test-data로 승격할지, test feature로 격리할지 결정
5. public projection의 internal absolute build path 제거 정책
6. Playwright/npm/browser archive의 sealed offline bundle custody
7. PC01/projectile rights와 final license
8. T5F current grid exact surface와 first-user workflow

## 다음 1~3 product walk 후보

1. `CURRENT_FRONTDOOR_WORKBENCH_PARITY_WALK`: current V25 source analysis와 execution result/observation manifest를 CLI/WASM/Workbench에서 단일 owner로 수렴
2. `PUBLIC_SOURCE_SELF_CONTAINMENT_WALK`: private test includes·absolute paths·G14 pack allowlist·teul startup을 fresh projection에서 fail-closed하게 교정
3. `SEALED_BROWSER_AND_RIGHTS_WALK`: offline browser bundle, notices, PC01/projectile rights를 각각 독립 custody

권고 순서는 1→2→3이다. 1을 결정하지 않으면 Workbench current execution success를 증명할 수 없고, 2를 결정하지 않으면 source-only public repository가 재현되지 않으며, 3을 결정하지 않으면 browser/public release가 계속 차단된다.
