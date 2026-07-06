# 구제안 이행 델타 아카이브 20260706

- 작업: Q36-5 / 지시문 5
- 상태: context note
- 목적: 2026-03~04 외부 검토 묶음을 현행 SSOT v24.x 기준으로 재분류해, 구버전 표면이 신규 작업으로 재유입되는 것을 막는다.
- 운영 규칙: 구버전 외부 검토 문서는 델타 노트 경유로만 인용한다.

## 채택 완료

아래 항목은 현행 정본 또는 현행 OI/계약에 이미 흡수된 것으로 본다. 새 작업에서 원문 제안을 다시 1차 근거로 재논의하지 않는다.

| 구제안 | 현재 정본 |
|---|---|
| 마디 동기화 계약 우선(all_required/fill_noop/noop) | B-standard 큰마디/속마디, `#모두필요/#빈칸채움`, `가만히` |
| filter -> merge -> apply | E-7C: `action_status 판정 -> merge -> 보람 계산 -> 5튜플 반환`, `거부` merge 제외 |
| noop/invalid/clipped 의미 | action 4상태 `맞음/가만히/잘림/거부` + `벗남다룸 = 거부/자르기/기본값채움` |
| source_origin/inject_mode 2축 분리 | `입력원천` / `주입방식(실주입/재연주입)` designed AGE2+ |
| reward/termination env-agent 분리 | `보람주인갈래/보람때갈래/판끝갈래` + 차림새 5종 |
| reset 의미 명확화 | `Gym reset(seed,options) = 모두다시`, resident `:reset` 동치(v23.0.7) |
| evidence tier와 closure 연결 | `CLOSED = pack PASS evidence + SSOT status sync` 원칙 |

## 시효 만료

아래 표현은 현행 정본을 직접 확인하지 않고 재인용하지 않는다.

| 구버전 표현 | 현재 판단 |
|---|---|
| "실구현 최대치 = space2d+graph+보임+모양" | 현재선은 grid2d 포함이다. |
| "AI GYM 계약은 나중에" | 누리짐 final line은 확정 완료. 남은 것은 consumer closure다. |
| 영문 enum `noop/invalid/clipped`, `all_required/fill_noop`, `relay/rollout` | 순우리말 정본으로 대체됨. |
| reset 5종 표기(`마당다시/판다시` 포함) | 현행 canonical 표(`누리다시/보개다시/모두다시`)와 대조 후에만 인용한다. |

## 여전히 OPEN

아래 항목은 현행 OI 또는 별도 closure track으로 추적해야 한다.

| 항목 | 현행 처리 |
|---|---|
| overlay full runner / multi-panel / 공식 overlay_layers / anchor-follow | OI 또는 UI closure track으로 추적 |
| `될때 / 인 동안` full runtime | 언어/runtime follow-up track |
| `판{} / 마당{}` 최종 표면 | story/lifecycle follow-up |
| observation manifest closure(`뒤살핌`) | `설정.거울`, designed/STUB_ONLY |
| numeric exact family(P0-N parallel track) | 별도 수치 exact track |

## SSOT 병합 큐 등록

SSOT 오너가 반영할 후보 항목:

| queue id | 제안 위치 | 반영 내용 | 주의 |
|---|---|---|---|
| `SSOT-MERGE-LEGACY-PROPOSAL-DELTA-20260706` | SSOT 운영/OPEN_ISSUES/TOOLCHAIN 중 오너 지정 위치 | "구버전 외부 검토 문서는 델타 노트 경유로만 인용한다" 운영 규칙과 위 델타 분류를 병합 | Codex는 `docs/ssot/**`를 직접 수정하지 않는다. 현행 정본 의미 변경 없이 재인용 방지 규칙만 반영한다. |

## DoD 확인

| DoD | 결과 |
|---|---|
| 델타 노트 1건 | 이 파일 |
| 채택 완료 / 시효 만료 / OPEN 분류 | 완료 |
| 운영 규칙 1줄 | 상단에 명시 |
| SSOT 병합 큐 등록 | `SSOT-MERGE-LEGACY-PROPOSAL-DELTA-20260706` |
| 공통 불변 경계 | 코드/팩/SSOT/state_hash/runtime canonical name 변경 없음 |
