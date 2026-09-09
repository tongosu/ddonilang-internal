# 20260706 Claude 세션 델타 — 누리 마디 심화 (위상/쓰기경합/격리/reset)

- 세션: Cowork Claude, 2026-07-06
- 역할: 검토·평가 / Co-Designer

## 결정(제안 수준, SSOT 오너 확정 필요)

1. 큰마디 위상표 v1 초안 작성 — 엔진 5계층(`샘→이야기→누리→거울→보개`) 위에 P0~P7 위상 + P3 내부 순서(3a~3g) 제안. 핵심: 훅 발신 알림은 다음 마디 샘 경유(3g), 될때/인 동안은 1-pass 재트리거 금지 권고.
2. 상태 쓰기 경합(W1~W3) v1 기본 = FATAL(`E_MADI_WRITE_CONFLICT`), `보탬` 계열 교환 연산만 opt-in 병합 권고. last-writer-wins 불채택.
3. 속마디 관측 격리 불변식 3조 — 속마디 수·순서가 커밋 결과에 영향 없음을 pack 검증 대상으로.
4. reset 5종 × 설정 재적용 상호작용표 — 누리다시의 시앗 재적용 권고, 판다시/마당다시는 질문 칸.
5. `합치기갈래` 신설 반대 — `행동모음갈래` 값 확장(앞선모음/다수결모음/자리모음) 권고. `rollback` → `되물림`(D-001) 표기 통일.

## 산출물

- `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md` (신규)
- `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md` 지시문 9 추가(설정 헤더 추가 고려 4건) + 지시문 10 심화 v2 항목(8~12) 보강

## 미완료 / 열린 질문

- OQ-1 임자 실행 순서 정본(선언 순서 권고), OQ-2 세움↔매마디 1회 평가·순환 오류, OQ-3 전처리 위상 소속, OQ-4 `(N마디)마다` 판정 시점, OQ-R1 누리다시 설정 재읽기 범위.
- 고급 preset 3종은 차림새 enum 확장이므로 SSOT 변경 경유 필요 (Codex proposal §8 주의 등재).

## 추가 산출물 (같은 날 후속)

- `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md` — 최대 설정 지도 (설정해시/시앗묶음/노출 4층)
- `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md` — 7목적 고도화 F0+G1/G2/G3
- `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md` — AI 닫힌 베타 체계 (Codex 사용자 역 / Claude Code 감사 역)
- `docs/context/notes/IDEAS_DDONIRANG_ENRICHMENT_V1_20260706.md` — 풍성화 아이디어 뱅크 (우선 5선 + 예약어 선점 목록)
- 핸드오프 지시문 11(7목적 G1), 12(SSOT 병합 준비), 13(Claude Code 감사), 14(베타 Round 0) 추가

## 검증

- `docs/ssot/**` 수정 0건, parser/runtime 변경 0건, closure 주장 없음. 문서 산출만.
