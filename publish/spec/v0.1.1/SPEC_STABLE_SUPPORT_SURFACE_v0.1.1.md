# 안정 지원 범위 — Language SPEC v0.1.1

> trace: Language SPEC `v0.1.1` ← owner-approved SSOT `v24.14.2` administrator candidate
> status: current pre-release public draft; installed SSOT remains v24.14.1 until protected apply
> authority: internal current SSOT wins on conflict


이 표는 SSOT registry와 v24.14.2 사용자-facing 결정의 사람용 투영이다. 설계 정본과
제품 구현 완료는 같은 상태가 아니다.

## CLI stable front door

| 명령 | v0.1.1 지위 |
|---|---|
| `canon` | stable contract |
| `check` | stable contract |
| `run` | stable contract |
| `world-diff` | stable contract |

`build`, `test`, `view`는 차기 후보이며 v0.1.1 안정 계약이 아니다.

## 표준 라이브러리

- registry에 기록된 stable-contract 표준 라이브러리 이름: **0개**.
- 따라서 v0.1.1은 개별 stdlib 이름의 장기 호환을 약속하지 않는다.

## settings·씨앗·생태계 표면

| 표면 | 공개 지위 | 제품 완료 주장 |
|---|---|---|
| settings 8절 소유권 | canonical design | 아님 |
| 평면 `제목/설명/마디수` | closed migration input policy | hard cut 전 parity·진단 필요 |
| `씨앗값` | canonical RNG setting/code-key design | frontdoor 전체 구현 아님 |
| `씨앗묶음` | canonical named-stream design | isolation/replay evidence 필요 |
| `시앗*` | deprecated input alias | 새 출력 금지 |
| 한국어 config digest 표시명 | canonical display terminology | digest 구현 별도 |
| `가지곳간` | canonical ecosystem term | registry 서비스 구현 별도 |

## 확인된 bounded 제품 증거

- SolvePlan S0/S1/S2와 prime 표면의 검증된 부분.
- bounded connect/unit/init.
- `<<-` parser/runtime 흐름과 다중 출처·순환 오류의 검증된 부분.
- `lang_flow_hook_interaction_v1` 제품 pack이 다루는 상호작용.

일반 solver 전체, 새김틀·구실·슬기씨, settings migration 전체, 씨앗묶음 runtime,
가지곳간 원격 서비스 구현 완료로 이 범위를 확대하지 않는다.
