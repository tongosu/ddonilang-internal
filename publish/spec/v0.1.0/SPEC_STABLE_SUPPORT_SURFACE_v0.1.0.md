# 안정 지원 범위 — Language SPEC v0.1.0

> trace: Language SPEC `v0.1.0` ← SSOT `v24.14.1` ← byte-identical `v24.14.0` snapshot
> status: pre-release public draft; internal SSOT wins on conflict

이 표는 SSOT의 generated registry에서 만든 사람용 투영이다.

## CLI stable front door

| 명령 | v0.1.0 지위 |
|---|---|
| `canon` | stable contract |
| `check` | stable contract |
| `run` | stable contract |
| `world-diff` | stable contract |

`build`, `test`, `view`는 차기 후보이며 v0.1.0 안정 계약이 아니다. registry에
이름이 존재하는 다른 명령도 공개 호환 계약을 뜻하지 않는다.

## 표준 라이브러리

- registry에 기록된 stable-contract 표준 라이브러리 이름: **0개**.
- 따라서 v0.1.0은 개별 stdlib 이름의 장기 호환을 약속하지 않는다.
- 이름이 존재하는 항목은 experimental 또는 review-required일 수 있다.

## 확인된 bounded 제품 증거

- SolvePlan S0/S1/S2와 prime 표면의 검증된 부분.
- bounded connect/unit/init.
- `<<-` parser/runtime 흐름과 다중 출처·순환 오류의 검증된 부분.
- `lang_flow_hook_interaction_v1` 제품 pack이 다루는 상호작용.

일반 ODE/constraint solver 전체, 모든 schema·diagnostic 이름, 새김틀·구실·슬기씨
구현 완료로 이 범위를 확대하지 않는다.
