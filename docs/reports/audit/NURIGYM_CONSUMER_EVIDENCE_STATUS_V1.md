# NURIGYM_CONSUMER_EVIDENCE_STATUS_V1

- 작성: 2026-07-08 (Asia/Seoul)
- 성격: DAYRUN G7 보고서. 수정 없음, consumer 증빙 현황표.
- 대상: 지시문 6 누리짐 consumer closure 증빙 현황.

## 결론

누리짐 의미 계약은 current line으로 문서화되어 있지만, 모든 consumer path가 닫힌 것은 아니다. 현재 저장소에서 PASS로 확인되는 것은 `teul-cli` 기준 export/golden, shared-sync action pipeline, priority tie-break, bounded web-side evaluator parity다. 반대로 `wasmtime-py` full parity와 `PyO3` long path benchmark/million-step route는 아직 완료 주장 금지 상태다.

## 기준선

| 기준 | 근거 | 해석 |
|---|---|---|
| final line | `docs/ssot/ssot/SSOT_MASTER_v24.12.9.md:569` | reset/step/action 4상태와 web/wasmtime/PyO3 consumer 방향은 정해짐 |
| Stage 1 제한 | `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1088`, `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1098` | wasmtime-py full parity 완료 주장은 금지 |
| PyO3 제한 | `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1099`, `docs/ssot/ssot/SSOT_MASTER_v24.12.9.md:541` | PyO3 long path 완료 주장은 금지 |
| 남은 pack 후보 | `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1320`, `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md:107` | reset/resident equivalence pack은 아직 후보 |

## Consumer 증빙표

| 축 | 현재 증빙 | DAYRUN probe | 판정 |
|---|---|---|---|
| dataset export contract | `tests/run_nuri_gym_contract_check.py:123`, `tests/run_nuri_gym_contract_check.py:147` | PASS, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nuri_gym_contract_g7_probe.log` | 닫힘-동작 증거 있음 |
| shared-sync action pipeline | `pack/nurigym_shared_sync_action_pipeline_v1/contract.detjson:2`, `tests/run_nurigym_shared_sync_action_pipeline_pack_check.py:35` | PASS, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_action_pipeline_g7_probe.log` | 닫힘-동작 증거 있음 |
| priority tie-break | `pack/nurigym_shared_sync_priority_tiebreak_v1/contract.detjson:2`, `tests/run_nurigym_shared_sync_priority_tiebreak_pack_check.py:18` | PASS, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_priority_tiebreak_g7_probe.log` | 닫힘-동작 증거 있음 |
| bounded Python/Web parity pack | `pack/nurigym_python_web_parity_v1/parity.detjson:1`, `tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py:177` | node runner PASS, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_node_g7_probe.log`; pack golden PASS, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_pack_golden_g7_probe.log` | bounded parity 증거 있음 |
| A3 통합 checker | `tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py:112`, `tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py:127` | FAIL, 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_g7_probe.log` | roadmap matrix 집계 drift |
| wasmtime-py short path | `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1281` | 이번 DAYRUN 실행 없음 | 결정 필요/보류 |
| PyO3 long path | `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md:1283` | 이번 DAYRUN 실행 없음 | 결정 필요/보류 |

## Drift / 현황

| 상태 | 항목 | 근거 | 다음 처리 |
|---|---|---|---|
| drift | A3 통합 checker가 roadmap matrix 집계 `rows=90 behavior=90 docs=0`으로 실패 | 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_g7_probe.log`; checker의 기존 기대값 `77/90`, `5/90`: `tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py:118` | roadmap matrix 집계 기준 재조정 필요 |
| 보류 | `gym_reset_seed_implies_complete_episode_reset_v1` pack 없음 | 후보 표: `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md:107` | 별도 pack/runner 필요 |
| 보류 | `resident_reset_episode_equiv_v1` pack 없음 | 후보 표: `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md:108` | 별도 pack/runner 필요 |
| 보류 | `nurigym_step_record_v02_roundtrip_v1` pack 없음 | 후보 표: `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md:109` | v0.1/v0.2 호환 규칙 결정 필요 |

## 닫힘 등급

- 이 보고서: `닫힘-문서`
- 추가 runtime/parser 구현: 없음
- consumer 전체 완료 주장: 없음

