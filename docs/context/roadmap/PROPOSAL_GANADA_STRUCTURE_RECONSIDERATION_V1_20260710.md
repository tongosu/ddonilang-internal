# PROPOSAL_GANADA_STRUCTURE_RECONSIDERATION_V1_20260710

상태: proposal / decision pending

## 전제

이 제안은 `GANADA_MARU_VERIFICATION_CONTRACT_V1_20260710.md`를 먼저 둔다. 즉, 줄기/마루 구조를 고치기 전에 `닫힘-동작` 검증 조건부터 고정한다. 기존 90칸의 상태를 이 문서에서 재판정하지 않는다.

핵심 근거는 두 가지다.

- 원본 매트릭스는 15줄기 x 6마루 운영표이고, 완료 판정은 pack/checker/CI evidence여야 한다(`docs/context/roadmap/ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:8`, `docs/context/roadmap/ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:11`).
- 2026-07-06 정정 매트릭스는 기존 체커 상당수가 기능이 아니라 문서 존재 여부를 검사했다고 지적한다(`docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:16`).

## 최근 산출물 귀속 판정

| 산출물 | 후보 귀속 | 판정 | 근거 |
|---|---|---|---|
| 설정 헤더/누리마디 위상·경합 | 가 + 아 + 타 | 다중 귀속. 언어 코어만으로는 좁고, 누리짐/검증 계약 축도 걸린다. | 큰마디 위상과 쓰기 경합은 실행 결정성 계약이다(`docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:11`, `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:24`, `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:66`). |
| 보개 표준팩/lowering | 사 + 마/하 보조 | 주 귀속은 사줄기. 교과/교육은 소비자다. | 표준 보개팩과 lowering 계약은 보개 축 자체의 생산 도구다(`docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:38`, `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:45`, `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:371`). |
| 7목적 고도화 G1 | 타 + 다 + 마 + 파 + 거 | 기존 단일 줄기에 넣기 어렵다. 성능/코퍼스/경제/물리/AI-friendly가 묶인 cross-cutting bundle이다. | DAYRUN은 perf, beta bundle, 경제 model-first, 적분기, LLM corpus, reserved sweep를 한 배치로 기록했다(`work/_session_deltas/20260707_codex_dayrun.md:6`, `work/_session_deltas/20260707_codex_dayrun.md:7`, `work/_session_deltas/20260707_codex_dayrun.md:8`, `work/_session_deltas/20260707_codex_dayrun.md:9`, `work/_session_deltas/20260707_codex_dayrun.md:10`). |
| 발표 전 동결 스윕 | 타 + 가 | 주 귀속은 타줄기 검증 인프라. 대상은 가줄기 언어 표면과 오류 코드다. | 동결 스윕 범위가 예약어, 문법 공간, E-code, schema version, pack ID 중복이다(`docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md:4`, `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md:6`, `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md:44`). |
| AI 닫힌 베타 프로토콜 | 거 + 하/마 보조 | 주 귀속은 거줄기. 교과/사용자 friction 측정은 하/마에 피드백된다. | AI 베타는 사람 베타 전처리이며 지식 격리를 핵심으로 한다(`docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md:6`, `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md:10`, `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md:30`). |

## 빠진 구조 후보

| 후보 | 필요성 | 반대 근거 | 제안 |
|---|---|---|---|
| 설정/거버넌스 심화 줄기 | 설정 해시, 누리마디 경합, SSOT 병합, OI queue는 제품 기능 한 줄기에 깔끔히 들어가지 않는다. | 타줄기의 검증 인프라와 겹칠 수 있다. | 새 줄기로 확정하지 말고, 당분간 `cross_cutting_governance` 태그를 contract에 추가하는 후속안으로 둔다. |
| 발표 전 동결 공통 마루 | 예약어/문법공간/E-code/schema/pack ID 중복은 모든 줄기 위에 걸친 release readiness다. | 6마루 체계를 7마루로 늘리면 기존 90칸 운영표가 깨진다. | 새 마루보다 전 줄기 공통 `freeze_gate` overlay로 두는 안을 우선 검토한다. |
| 증거 등급 축 | 문서-only와 제품 동작을 분리하지 않으면 2026-07-06 결함이 반복된다. | 상태값이 늘면 보고가 복잡해진다. | 이번 contract의 `닫힘-문서`/`닫힘-동작` 분리를 채택 후보로 둔다. |

## 검증 체계 개선안

| 안 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 기존 checker 재작성 | 각 ROADMAP_V2 checker가 실제 pack golden, CLI/runtime, browser runner를 실행하게 고친다. | `닫힘-동작`을 바로 제품 증거와 연결한다. | 90칸 모두를 한 번에 고치면 비용이 크고 오래 걸린다. |
| B. 닫힘 등급 세분화 | `후보`, `닫힘-문서`, `닫힘-동작`, `실패`, `결정필요`를 공식 운영 등급으로 둔다. | 문서 누적과 제품 완료를 즉시 분리한다. | 기존 장기 진행률 숫자와 충돌하므로 마이그레이션 설명이 필요하다. |

권장 순서는 B를 먼저 운영 계약으로 고정하고, A를 고우선순위 줄기부터 점진 적용하는 것이다. 이번 `ganada_maru_verification_contract_v1`은 B를 먼저 잠그는 산출물이다.

## 우선순위 제안

| 순위 | 항목 | 이유 | 닫힘 조건 |
|---:|---|---|---|
| 1 | 마줄기 lesson 수리 | 2026-07-06 정정 매트릭스가 이미 실질 lesson 존재와 golden/구문 이전 gap을 지목했다(`docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:29`). | lesson pack golden PASS + 제품 실행 PASS |
| 2 | 자줄기 UI 배선 | 백엔드 증거가 있으나 UI selector 부재가 남았다(`docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:21`, `docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:56`). | browser/UI runner PASS + 관련 backend checker PASS |
| 3 | 타줄기 ROADMAP checker 재작성 | 전체 matrix 신뢰도를 회복하는 기반이다. | markdown existence checker 단독 금지 + product/pack execution 증거 |
| 4 | 동결 gate overlay 설계 | 발표 전 이름/스키마/오류코드 risk가 전 줄기에 걸친다. | freeze sweep checker PASS + 충돌/예약어 목록 file:line 근거 |
| 5 | 설정/거버넌스 cross-cutting 태그 | 설정/누리마디/OI/SSOT 병합 산출물의 귀속 혼선을 줄인다. | contract 태그 추가 + 기존 줄기 귀속과 충돌 없음 |

## 범위 밖

- `docs/ssot/**` 직접 수정 없음.
- parser/runtime/product UI 구현 없음.
- 기존 90칸 상태 재판정 없음.
- 장기 진행률 재계산 없음.

## 검증

```text
python tests/run_pack_golden.py ganada_maru_verification_contract_v1
=> PASS

python tests/run_ganada_maru_verification_contract_check.py
=> PASS
```
