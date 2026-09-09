# 2026-07-11 Codex 세션 델타 - 셈그림·한국어 Manim SSOT 통합 승격 패킷

## 목적

- Wave 1·1T·2A와 진행 중인 2B의 제품 증거를 기존 SSOT OI와 연결한다.
- 과거 Wave 1 인입 proposal과 decision ledger의 오래된 구현 상태를 대체할 V2 장부를 만든다.

## 산출물

- `docs/context/proposals/PROPOSAL_SEAMGRIM_KOREAN_MANIM_WAVE1_TO_WAVE2B_SSOT_PROMOTION_PACKET_V1_20260711.md`
- `docs/context/reports/SEAMGRIM_KOREAN_MANIM_PROMOTION_LEDGER_V2_20260711.detjson`
- `tests/run_seamgrim_korean_manim_promotion_packet_check.py`

## 현재 상태

- Wave 1·1T·2A: 제품 증거 연결 완료.
- Wave 2B G0~G2: commit/pack/product path 연결 완료.
- Wave 2B G3~G8: 구현·검증 완료 전 승격을 막는 대기 항목으로 기록.
- packet status: `live_draft_waiting_wave2b_g8`.

## 경계

- 기존 OI만 사용하며 신규 OI를 만들지 않았다.
- candidate artifact 이름과 exact schema를 정본으로 승격하지 않았다.
- `docs/ssot/**`, parser/runtime, `state_hash`를 변경하지 않았다.
- Wave 2B 제품 워킹트리와 기존 unrelated 변경을 수정하거나 stage하지 않았다.
