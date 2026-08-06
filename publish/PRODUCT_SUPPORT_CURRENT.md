# 현재 제품 지원 상태

> 확인일: 2026-08-06
> 이 문서는 고정된 Language SPEC과 별개의 제품 계보 안내다.

## 먼저 구분할 것

- [Language SPEC v0.5.0](spec/v0.5.0/SPEC_MANIFEST_v0.5.0.md)은 내부 SSOT
  v24.24.1의 RD-001~122를 투영한 현재 공개 docs-first 계약이다.
- [Language SPEC v0.4.0](spec/v0.4.0/SPEC_MANIFEST_v0.4.0.md)은 내부 SSOT
  v24.22.1 시점의 고정 이전 공개판이다. 이후 상태를 소급해 덮어쓰지 않는다.
- [Language SPEC v0.3.0](spec/v0.3.0/SPEC_MANIFEST_v0.3.0.md)은 내부 SSOT
  v24.17.1 시점의 고정 스냅숏이다.
- 내부 SSOT live current는 v24.25.0이다. Language SPEC v0.5.0은
  v24.24.1 시점의 고정 공개판이며 RD-123~128을 소급 투영하지 않는다.
- [Language SPEC v0.5.0 후보 R3 보존본](spec/v0.5.0-candidate-r3/SPEC_MANIFEST_v0.5.0.md)은
  독립 검토 `PASS / 13 of 13 / NO CORRECTIONS`를 받은 승격 입력 계보다.
- v0.5.0의 public current 승격은 제품 지원 약속이나 runtime landed가 아니다.
- `기본 제품`은 사용자가 기본 브랜치·URL·배포판에서 바로 만나는 것을 뜻한다.
- `검증 후보`는 격리 계보에서 제품 경로와 독립 검토를 통과했지만 기본 배포로
  승격되지 않은 것을 뜻한다.
- `정본만`은 문법·의미가 정해졌지만 전체 제품 수직을 닫지 않은 것을 뜻한다.

## 사용자 표면

| 표면 | 공개 계약 | 확인된 제품 근거 | 기본 제품 판정 |
| --- | --- | --- | --- |
| 값·계산·`<-`·`보여주기` | 현재 빠른 시작 표면 | 기본 셀그림 예제 rail과 README 첫 예제 | 기본 제품 진입 경로 |
| `(이름: 값, ...) 보임.` | v0.5.0 public docs-first, v0.3 계승 | parser→runtime→CLI/WASM→Workbench와 독립 검토 PASS | 검증 후보. 현 기본 HEAD에는 미포함 |
| `(이름) 보임.` 축약 | v0.5.0 public docs-first, v0.3 계승 | `(이름: 이름) 보임.` 정본화·실행 PASS | 검증 후보. 현 기본 HEAD에는 미포함 |
| 표준 보기 12종 | v0.5.0 public docs-first, v0.3 계승 | 전체 12종의 기본 배포 수직은 아직 닫히지 않음 | 정본만 / OPEN |
| 이름씨 구성·짧은 계약·구실 | v0.5.0 public docs-first | parser/canon/golden·KS 최종 syntax OPEN | 정본만 / OPEN |
| 맺음·선택값·참조·두고 | v0.5.0 public docs-first | 공통 parser/canon/runtime parity OPEN | 정본만 / OPEN |
| exact 수·`mol`·바이트열 | v0.5.0 public docs-first | C-02·wire·runtime·단위 golden OPEN | 정본만 / OPEN |
| 함수값·효과·선택값 연산 | v0.5.0 public docs-first | artifact/lock/runtime·stdlib parity OPEN | 정본만 / OPEN |
| 값꾸러미 위치형·이름형 의미 | v0.5.0 public docs-first | 혼합·중복·필드 수 유실 P1 `NOT FIXED` | 정본만 / OPEN |
| `얼개 {}`·가지·잠금글 | v0.5.0 canonical direction | C-05 migration/export·exact wire·UI OPEN | 정본만 / OPEN |
| 선언형 모델·SolveRecipe | v0.5.0 public docs-first | 공개 syntax·typed IR·solver OPEN | 정본만 / OPEN |
| `보임` 기본 결과표·typed 자료열 | v0.5.0 public docs-first | parser/CLI/WASM/renderer parity OPEN | 정본만 / OPEN |
| 표준 그래프 12종 의미 선반 | v0.5.0 public docs-first | exact module/export·접근성 제품 OPEN | 정본만 / OPEN |
| `모형 {}`·`모형값`·닫힌 `::` | v0.5.0 public docs-first | lexer/parser/typed AST/runtime OPEN | 정본만 / OPEN |
| 초기화·`::구함`·사건·`잇기`·일반 `풀기` | v0.5.0 public docs-first | solver/canon/schema/CLI/WASM parity OPEN | 정본만 / OPEN |

## 2026-07-31 계보 확인

- 현 기본 브랜치: `codex/queue-20260706` / `a000e262...`
- `보임` 언어 수직 독립 검토 코드: `cf503ffd...`
- 공개 관찰 Workbench 수직 독립 검토 코드: `4dece742...`
- 위 두 계보와 이후 검증 기능을 함께 포함한 통합 후보:
  `codex/seamgrim-unified-product-shell-execution-controls-w1-20260731` / `df50fc49...`

계보 포함은 기본 배포 승격이 아니다. 기본 제품 표시를 바꾸려면 통합 후보에서
학습 예제·CLI/WASM·실제 Workbench 순환을 다시 검증하고, owner가 기본 계보로 승격해야 한다.

## 공개 문서 갱신 규칙

1. v0.5.0은 현재 공개판이며 v0.4.0과 이전판은 고정 스냅숏으로 보존한다.
2. 기본 제품으로 승격된 표면은 이 문서에 먼저 반영한다.
3. 새 의미 계약은 후속 Language SPEC 버전에서만 반영한다.
4. 정본, 구현, 독립 검토, 기본 배포, 외부 사용자 성공을 서로 대체 근거로 쓰지 않는다.
