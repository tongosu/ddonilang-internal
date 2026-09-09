# DDN-V1-FD01 Frontdoor / RuntimeBridge 준비도 감사 I1

이 디렉터리는 V1 제품 마감 프로그램의 첫 제품 vertical을 시작하기 전에 현재
V25 parser, CLI, WASM, RuntimeBridge, Workbench가 실제로 어디까지 연결됐는지를
읽기 전용으로 고정한다.

```text
TASK: DDN-V1-FD01-READINESS-AUDIT-I1
BASELINE: 25a63aba7dc6ab362dd3f640385ad9a7ebfa0455
LIVE_INTERNAL_SSOT: v25.15.0
PUBLIC_LANGUAGE_SPEC: v0.5.0
VERDICT: FD01_PRODUCT_FRONTDOOR_NOT_YET_CONVERGED
PRODUCT_IMPLEMENTATION: NOT_STARTED
SSOT_CHANGED: 0
PUBLIC_SPEC_CHANGED: 0
UI_CHANGED: 0
PUBLIC_ACTIVATION: NOT_AUTHORIZED
```

## 핵심 결론

- Rust V25 parser와 `DdnProgram::from_v25_source`는 존재한다.
- 그러나 공식 CLI, 기본 WASM VM, source analysis의 현재 제품 진입은 pre-V25
  constructor를 사용한다. 공개 V25 제품 ingress는 `0`이다.
- RuntimeBridge와 Workbench의 source-readiness·observation 전달 구조는 실제 Rust
  WASM 결과를 소비하며 fail-closed다. 이 구간의 JS 의미 합성은 발견되지 않았다.
- 셈그림 lesson 557개를 양쪽 parser로 실제 분류했을 때 V25 통과는 `0`이었다.
  따라서 전역 기본 parser를 지금 V25로 바꾸면 현 lesson 전체가 깨진다.
- historical PC02는 독립 plain PASS 전에 Owner 승인 exact inverse로 제외됐다.
  그 commit을 그대로 재적용할 권한도, 근거도 없다.
- 다음 안전 단계는 전역 전환이 아니라 **명시적 internal typed SourceEpoch routing**과
  선택된 V1 공개 예제의 점진적 migration이다.

## 산출물

- `AUTHORITY_AND_REACHABILITY_AUDIT.md`
- `HISTORICAL_PC02_CUSTODY.md`
- `LESSON_EPOCH_COMPATIBILITY_MATRIX.md`
- `OWNER_DECISION_PACKET.md`
- `FD01_SUCCESSOR_IMPLEMENTATION_PACKET.md`
- `FAULT_AND_TEST_MATRIX.md`
- `AUDIT_RESULT.md`
- `fd01_surface_inventory.detjson`
- `fd01_successor_dag.detjson`
- `fd01_test_ledger.detjson`

기계 재현:

```powershell
python tools/generate_v1_fd01_readiness_audit_i1.py
python tests/run_v1_fd01_readiness_audit_i1.py
cargo test -p ddonirang-tool --test v1_fd01_lesson_epoch_inventory --offline --locked -- --nocapture
```

