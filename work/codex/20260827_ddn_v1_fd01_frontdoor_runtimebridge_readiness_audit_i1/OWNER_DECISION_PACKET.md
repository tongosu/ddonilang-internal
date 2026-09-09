# FD01 Owner 결정 패킷

## 결정이 필요한 이유

현 V25 parser는 내부 구현됐지만 제품 기본 진입에는 연결되지 않았다. 동시에 현재
lesson 557개는 V25 통과가 0이다. 따라서 `V25를 제품에 연결한다`는 방향만으로는
부족하고, **어떤 epoch를 누가 어떤 identity로 선택하는가**를 먼저 결정해야 한다.

## D1 — SourceEpoch 전환 방식

### A. internal typed epoch routing 먼저 — 추천

예:

```text
BundledProjectIdentity(projectile-v1)
  -> SourceEpoch::V25
  -> 동일 선택으로 source analysis + execution
```

사용자가 입력한 source text를 보고 추정하지 않고, 프로젝트·팩의 봉인 metadata가
내부 typed 값을 넘긴다. 공개 CLI flag나 stable wire는 아직 만들지 않는다.

장점: 현 lesson을 깨지 않고 새 V1 membership을 점진적으로 연결할 수 있다. 분석과
실행의 epoch drift를 타입·테스트로 막을 수 있다.

단점: migration 기간에 두 epoch를 명시적으로 관리해야 한다.

### B. 공식 CLI/WASM 기본값을 즉시 V25로 전환 — 비추천

장점: 표면상 구조가 단순하다.

단점: 현재 lesson 557/557이 V25 실행에 실패한다. historical PC02의 미검토 문제를
반복하고, Workbench 예제를 대규모로 동시에 깨뜨린다.

### C. source text를 보고 자동 감지·fallback — 거부 권고

장점: 일부 옛 source가 당장 실행될 수 있다.

단점: 같은 바이트가 parser 순서에 따라 다른 의미를 가질 수 있고, 실패가 다른 epoch
성공으로 위장된다. replay·진단·state identity를 고정할 수 없다.

## D2 — V1 공개 예제 migration 범위

### A. 선택 membership migration — 추천

첫 세트는 정의/결속 PC01, 작은 console 예제, current grid 한 vertical처럼 사용자에게
보여줄 workflow를 소수 선택한다. 선택 목록과 source hash를 봉인한 뒤 100% V25로
migration한다.

장점: 사용자 가치와 회귀 범위가 명확하다. V1 membership 0에서 실제 제품 근거를
차근차근 늘릴 수 있다.

단점: 선택되지 않은 lesson은 당분간 historical/internal 상태다.

### B. 557개 전부 migration 뒤 제품 연결

장점: 완료 뒤 혼합 epoch가 줄어든다.

단점: 역사·실험 파일까지 한 덩어리로 묶어 첫 제품 vertical을 지나치게 오래 막는다.

## D3 — current grid

### A. V25 원문 + native Rust result-set — 추천

current grid lesson을 선택 membership에 넣고, Rust 제품 경로가 canonical grid result를
만들어 WASM manifest로 전달하게 한다.

장점: T5F의 현재 RED를 실제 제품 의미로 닫는다. renderer와 의미 권위를 분리한다.

단점: exact grid source/result contract와 새 테스트가 필요하다.

### B. JS에서 grid result 합성 — 거부 권고

빠르지만 Rust/CLI/WASM parity가 깨지고 silent fallback이 생긴다.

### C. historical pre-V25 constructor만 복원

역사 runner 보존에는 쓸 수 있지만 current V1 grid를 닫지 못한다.

## D4 — 전역 V25 기본값 전환 gate

다음을 모두 만족한 뒤 별도 Owner 승인으로만 전환한다.

- 선택된 public example membership 100% V25 migration
- CLI/WASM/Workbench 동일 원문·동일 진단·동일 결과
- migration-required negative corpus와 silent fallback 0
- source analysis와 execution의 SourceEpoch identity 일치
- deterministic build와 actual Edge product cycle
- fresh independent plain PASS

## D5 — 외부 wire

이번 vertical은 internal typed selector만 허용한다. CLI flag, env, WASM public parameter,
project-file stable field, stable receipt wire는 만들지 않는다. public exact surface는 RD-207
등 별도 권위에서 결정한다.

## 추천 Owner 응답

```text
DDN_V1_FD01_DIRECTION: OPTION_A_INTERNAL_TYPED_EPOCH_ROUTING
GLOBAL_V25_DEFAULT_SWITCH_AUTHORIZED: NO
CONTENT_SNIFFING_AUTODETECT: FORBIDDEN
V1_PUBLIC_EXAMPLE_POLICY: SELECTED_MEMBERSHIP_MIGRATION
CURRENT_GRID_POLICY: V25_NATIVE_RESULT_SET
STABLE_SOURCE_EPOCH_WIRE_AUTHORIZED: NO
PRODUCT_IMPLEMENTATION_AUTHORIZED: YES_FD01A_INTERNAL_TYPED_VERTICAL_ONLY
```

이 응답은 SSOT/SPEC 변경, 공개 문법, UI 재설계, activation, release를 승인하지 않는다.

