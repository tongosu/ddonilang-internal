# 20260707 Codex session delta: 지시문 11 G1 실행 준비도 정리

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 범위: 첨부 `CODEX 지시문 묶음` 중 지시문 11 읽기 및 실행 준비도 정리
- SSOT 수정: 없음
- parser/runtime 변경: 없음
- closure 주장: 없음

## 확인한 입력

- 첨부 문서의 지시문 11은 `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md`의 G1 즉시 실행 항목 7건을 대상으로 한다.
- 로컬 인수인계 문서 `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md`에도 지시문 11이 이미 반영되어 있었다.
- 이번 세션에서는 전체 7건을 바로 구현하지 않고, 기존 증빙과 새 산출물 필요성을 먼저 분리했다. 지시문 자체가 "각각 별도 세션 권장"이라고 명시하기 때문이다.

## 새 산출물

- `docs/context/proposals/PROPOSAL_DIRECTIVE11_G1_READINESS_AND_FIRST_EXECUTION_BUNDLE_V1_20260707.md`

## 항목별 준비도 판단

| 항목 | 판단 |
|---|---|
| F0-2 결정적 벤치 계약 | `benchmark_baseline_v1` 기반이 있으므로 새 `perf_baseline_v1`은 대체가 아니라 성능 회귀 상위 계약으로 둔다. |
| P1-G1 step_record v0.2 | `nurigym_shared_sync_action_pipeline_v1`에 핵심 필드가 이미 있다. 새 runtime 의미보다 roundtrip pack/proposal이 필요하다. |
| P4-G1 진단 3층 | fix-it pack은 있으나 초심자 3층 채점은 별도 audit이 필요하다. |
| P5물리-G1 적분기 | `오일러/반암시적오일러`는 있음. `선형보간`과 Fixed64 한계 문서가 빠져 있다. |
| P5경제-G1 model-first | 수요-공급/세금은 기존 pack 증빙이 강하다. 통화 공급과 welfare 지표 분화가 필요하다. |
| P6-G1 ko-common | 교착어 AST 증빙은 있으나 ko-common T1 승격 조건과는 별개다. 4조건 실측 리포트가 필요하다. |
| P7-G1 LLM 코퍼스 | 설계만 있고 실제 추출기/JSONL/pack은 없다. 결정적 추출 프로토타입이 필요하다. |

## 권고 실행 순서

1. 저위험 docs/audit 묶음: P1-G1 step_record proposal, P4-G1 진단 3층 audit, P6-G1 ko-common 실측.
2. 도구/pack 묶음: F0-2 perf baseline, P7-G1 LLM corpus extractor.
3. 도메인 pack 묶음: P5물리-G1, P5경제-G1.

## 미착수

- G2/G3 항목은 착수하지 않았다.
- `docs/ssot/**`는 수정하지 않았다.
- `DEV_SUMMARY`는 갱신하지 않았다. 실제 pack/test 구현 없이 준비도 proposal만 추가했기 때문이다.
