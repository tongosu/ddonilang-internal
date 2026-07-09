# GANADA_MARU_VERIFICATION_CONTRACT_V1_20260710

상태: verification contract / `닫힘-문서`

## 목적

가나다 15줄기 x 6마루 구조 재검토 전에, 각 칸이 무엇을 통과해야 `닫힘-동작`으로 불릴 수 있는지 먼저 고정한다. 이 문서는 상태 재판정이 아니다. 실제 판정은 `pack/ganada_maru_verification_contract_v1/contract.detjson`과 `tests/run_ganada_maru_verification_contract_check.py`를 통과한 뒤 별도 재검증에서 수행한다.

근거:

| 근거 | file:line | 내용 |
|---|---|---|
| 원본 매트릭스 목적 | `docs/context/roadmap/ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:8` | 15줄기 x 6마루 운영표 |
| 원본 DoD | `docs/context/roadmap/ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:11` | 완료 판정은 pack/checker/CI evidence |
| 정정 매트릭스 총계 | `docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:9` | 실증 재검증 결과 8칸만 강한 닫힘 |
| 검증 결함 | `docs/context/roadmap/GANADA_MATRIX_CORRECTED_20260706.md:16` | 체커가 기능이 아니라 문서 존재 여부를 검사한 문제 |
| 재검증 방법론 | `docs/context/roadmap/PLAN_GANADA_REVERIFICATION_20260706.md:16` | 실제 실행 PASS/FAIL 확인 원칙 |
| Codex guide 원칙 | `docs/context/roadmap/ROADMAP_V2_GANADA_MILESTONE_MATRIX_CODEX_GUIDE_20260426.md:22` | pack/checker/CI evidence 확인 |

## Contract 산출물

| 산출물 | 역할 |
|---|---|
| `pack/ganada_maru_verification_contract_v1/contract.detjson` | 90칸 전체 검증 조건 manifest |
| `pack/ganada_maru_verification_contract_v1/golden.jsonl` | pack runner smoke |
| `tests/run_ganada_maru_verification_contract_check.py` | 90칸 완전성, file:line, 증거 배제, UI/CLI/도구 조건 검사 |

이 contract는 다음을 명시적으로 false로 둔다: product code change, parser landed claim, runtime claim, UI behavior claim, state rejudgement claim, `docs/ssot/**` change.

## 상태 등급

| 등급 | 뜻 | `닫힘-동작` 가능 여부 |
|---|---|---|
| `미착수` | 아직 산출물 없음 | 불가 |
| `후보` | 구조/근거 후보만 있음 | 불가 |
| `닫힘-문서` | proposal/report/manifest/checker만 있음 | 불가 |
| `닫힘-동작` | 제품 경로 실행 PASS + 재현 가능한 pack/checker PASS | 가능 |
| `실패` | 실행 검증 실패 | 불가 |
| `결정필요` | 명명/범위/권한 결정 없이는 판단 불가 | 불가 |

장기 완료 표현은 이 contract의 상태값으로 쓰지 않는다. 특히 `진짜닫힘`은 2026-07-06 정정 문서의 역사적 재검증 용어로만 남기고, 새 contract claim에는 쓰지 않는다.

## 증거 등급

| 증거 | `닫힘-동작` 단독 근거 | 비고 |
|---|---:|---|
| status report | no | 작업 설명 근거일 뿐 제품 실행 아님 |
| proposal | no | 결정 후보 또는 설계 후보 |
| markdown existence checker | no | 2026-07-06 결함 재발 방지 |
| unrun pack/checker | no | 실행 결과 없음 |
| external AI claim | no | ERQ 또는 proposal로만 취급 |
| pack golden PASS | yes, 보조 | 제품 경로와 연결되어야 함 |
| product CLI/runtime PASS | yes | 언어/런타임/누리짐/도구 workflow |
| browser/UI runner PASS | yes | 작업실/나눔/교실/UI workflow |
| tooling runner/CI PASS | yes | 타줄기 검증 인프라 workflow |

## 15줄기 x 6마루 재열람표

| 줄기 | 정의 근거 | 0마루 | 1마루 | 2마루 | 3마루 | 4마루 | 5마루 |
|---|---|---|---|---|---|---|---|
| 가 말과 실행 코어 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:68` | current-line 문법 ledger | core smoke | 대표 문법 pack | 편집기 진단 | package/gaji | LTS 문법선 |
| 나 표준가지 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:83` | 후보 목록 | std_core/grid/input | std_unit/random/event | agent/resource/network/policy | registry | LTS |
| 다 수학/심볼릭 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:98` | 범위 확정 | exact/vector/function | symbolic/solve/proof | 수학 보개 | math package | LTS |
| 라 말블록 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:113` | 설계 확정 | block to DDN | roundtrip | 3모드 작업실 | 예제 공유 | editor LTS |
| 마 교과 실험실 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:128` | 교과 카탈로그 | 대표 차시 | 교과 pack | 수업 작업실 | 공개 차시 | 교과 LTS |
| 바 자유 실험실 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:143` | 빈 작업실 | 새 실험 | 실험 노트 | 자유 실험 UI | 실험 공유 | 연구자 모드 |
| 사 보개/공간/게임 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:158` | family/backend/profile | graph/space2d | sprite/grid2d | 3D/game preview | asset/view | renderer hardening |
| 아 누리짐 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:173` | Gym schema | reset/step | 대표 환경 golden | Python/Web parity | dataset registry | training workflow |
| 자 AI/슬기 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:188` | AI 경계 | SeulgiIntent | Gatekeeper/InputSnapshot | AI 제안 UI | model artifact | replay-safe workflow |
| 차 RPG | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:203` | action/story | phrase/action | story/RPG pack | RPG authoring UI | story package | engine adapter |
| 카 또니마루 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:218` | platform charter | server MVP | publication/read API | project/share UI | public registry | platform hardening |
| 타 검증/팩/도구 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:233` | skeleton | runner PASS | CI/golden gate | diag UI/LSP | registry verify | benchmark/LTS |
| 파 경제/사회/역사 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:248` | case card | 기준 시장 | bridge/social pack | 정책 ghost UI | template registry | social LTS |
| 하 교육/교재 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:263` | 총서/차시 | 대표 교재 | 차시 pack | 교사용/학생용 UI | 공개 강좌 | 교육 운영 LTS |
| 거 AI 개발보조 | `ROADMAP_V2_GANADA_MILESTONE_MATRIX_20260426.md:278` | 질문카드 | 질문카드 smoke | AI 산출물 검증 | 개발보조 UI | 저작자 도구 | AI workflow hardening |

세부 90칸의 원문 행 근거는 `contract.detjson`의 각 `current_evidence_refs`에 들어 있다. checker는 90칸 ID 순서(`가-0` ... `거-5`), 각 file:line 존재, `contains` 토큰 일치를 모두 확인한다.

## 검증 결과

```text
python tests/run_pack_golden.py ganada_maru_verification_contract_v1
=> PASS

python tests/run_ganada_maru_verification_contract_check.py
=> PASS
```

## 다음 단계

이 contract를 기준으로 `PROPOSAL_GANADA_STRUCTURE_RECONSIDERATION_V1_20260710.md`는 구조 재검토를 제안한다. 기존 90칸 상태 재판정은 별도 실행 기반 재검증 트랙에서만 수행한다.
