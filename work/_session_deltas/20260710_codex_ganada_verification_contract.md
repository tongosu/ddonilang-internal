# 2026-07-10 Codex Ganada Verification Contract

## 목적

- 가나다 15줄기 x 6마루 구조 재검토 전에 `닫힘-동작` 검증 조건을 먼저 고정한다.
- 이번 배치는 상태 재판정이나 제품 구현이 아니라, 90칸 판정 기준을 기계적으로 검증하는 contract/checker를 만든다.

## 시작 상태

- branch: `codex/queue-20260706`
- tracked dirty files: none at start.
- existing untracked reference files are left uncommitted:
  - `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`
  - `또니랑/*.md`

## 경계

- `docs/ssot/**` 직접 수정 금지.
- parser/runtime/UI/product behavior 변경 금지.
- 기존 90칸을 새로 닫힘 처리하지 않는다.
- `닫힘-동작`은 제품 경로 실행 증거와 재현 가능한 checker/pack 증거가 있을 때만 허용하는 contract로만 고정한다.

## 진행 로그

- G0: 시작 상태와 경계를 기록했다.
- GVC-CONTRACT: `pack/ganada_maru_verification_contract_v1`과 `tests/run_ganada_maru_verification_contract_check.py`를 추가했다.
  - 15줄기 x 6마루 90칸을 `contract.detjson`의 `cells`로 고정했다.
  - 각 칸은 `current_evidence_refs`로 원본 매트릭스 file:line을 가진다.
  - `status_report_only`, `proposal_only`, `markdown_existence_checker_only`, `unrun_pack_or_checker`, `external_ai_claim`은 `닫힘-동작` 증거에서 제외한다.
- GVC-REPORT: `GANADA_MARU_VERIFICATION_CONTRACT_V1_20260710.md`와 `PROPOSAL_GANADA_STRUCTURE_RECONSIDERATION_V1_20260710.md`를 추가했다.

## 검증

- `python -m json.tool pack/ganada_maru_verification_contract_v1/contract.detjson` PASS.
- `python tests/run_pack_golden.py ganada_maru_verification_contract_v1` PASS.
- `python tests/run_ganada_maru_verification_contract_check.py` PASS.

## 결정/보류

- 이번 배치는 기존 90칸을 재판정하지 않는다.
- `닫힘-동작`은 제품 경로 실행 PASS + 재현 가능한 pack/checker PASS가 있을 때만 후속 재검증에서 제안할 수 있다.
- 설정/거버넌스 심화 줄기, 발표 전 동결 공통 마루는 확정하지 않고 proposal 후보로만 남겼다.

## 다음 추천

1. `ganada_maru_verification_contract_v1` 기준으로 마줄기 lesson 수리 대상의 실제 제품 실행/pack golden 증거를 먼저 묶는다.
2. 그 다음 자줄기 UI 배선은 browser/UI runner PASS가 확보될 때만 `닫힘-동작`을 제안한다.
