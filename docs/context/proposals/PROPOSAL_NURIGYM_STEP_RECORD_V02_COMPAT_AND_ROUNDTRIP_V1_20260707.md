# PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 분류: PROPOSAL / NURIGYM / STEP_RECORD / WIRE_SCHEMA
- 상태: docs-first. parser/runtime 신규 문법 없음, closure 주장 없음
- 기준: `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706` P1-G1, `pack/nurigym_shared_sync_action_pipeline_v1`

## 0. 결론

`nurigym.step_record.v0.2`는 새 의미론을 만들 필요가 없다. 현재 `nurigym_shared_sync_action_pipeline_v1`이 이미 action provenance 필드를 add-only 방식으로 내고 있으므로, G1에서 해야 할 일은 그 필드를 공식 step record wire 계약으로 묶고 v0.1 consumer 호환 규칙을 고정하는 것이다.

## 1. 현재 증빙

| 근거 | 확인 내용 |
|---|---|
| `pack/nurigym_shared_sync_action_pipeline_v1/contract.detjson` | `raw_action`, `resolved_action`, `normalized_action`, `action_status`, `merge_candidates`, `merged_action`, `applied_action`, `missing_input` 필드 요구 |
| `pack/nurigym_shared_sync_action_pipeline_v1/README.md` | status 4종 `맞음/가만히/잘림/거부`를 케이스 기반으로 고정 |
| `tests/run_nurigym_shared_sync_action_pipeline_pack_check.py` | 필드 존재, status 4종, reject-before-merge, clip-before-merge 검증 |

## 2. v0.2 필드

| 필드 | 필수성 | 의미 |
|---|---|---|
| `raw_action` | MUST | 외부 입력이 들어온 원형. 없으면 `null` 또는 빈 입력으로 기록한다. |
| `normalized_action` | MUST | action schema에 맞춰 정본화한 값. |
| `action_status` | MUST | `맞음/가만히/잘림/거부` 중 하나. |
| `merged_action` | MUST in shared mode | 여러 입력을 합친 뒤의 후보. 단일 agent 모드에서는 `applied_action`과 같아도 된다. |
| `applied_action` | MUST | 실제 누리 step에 적용된 action. |
| `resolved_action` | SHOULD | alias/default/fill-noop 등을 푼 중간값. |
| `merge_candidates` | SHOULD in shared mode | merge 전 후보 목록. |
| `missing_input` | SHOULD | completion policy에 따라 비어 있던 입력 슬롯. |

## 3. v0.1 호환 규칙

1. v0.2 producer는 v0.1 필드를 제거하지 않는다.
2. v0.1 consumer는 모르는 v0.2 필드를 무시할 수 있어야 한다.
3. v0.2 consumer는 `raw_action`, `normalized_action`, `action_status`, `applied_action`만 있어도 단일-agent step을 해석할 수 있어야 한다.
4. shared/multi-agent consumer는 `merged_action`과 `merge_candidates`가 없으면 merge provenance incomplete로 표시하되 episode replay 자체를 실패시키지 않는다.
5. `거부` action은 merge 후보에서 제외된 기록이 남아야 한다. `잘림` action은 보정된 값으로 merge 후보에 남을 수 있다.

## 4. roundtrip pack 후보

Pack ID: `nurigym_step_record_v02_roundtrip_v1`

최소 케이스:

| 케이스 | 입력 | 기대 |
|---|---|---|
| `valid` | 범위 안 action | `action_status=맞음`, `raw_action == applied_action` |
| `noop_missing` | 입력 없음 + fill-noop | `action_status=가만히`, `missing_input` 기록 |
| `clip` | 범위 밖 action + clip | `action_status=잘림`, `normalized_action != raw_action`, `applied_action == normalized_action` |
| `reject` | 범위 밖 action + reject | `action_status=거부`, `applied_action` 미적용 또는 noop 대체, merge 제외 |
| `shared_merge` | 둘 이상의 agent/action 후보 | `merge_candidates`와 `merged_action` 기록 |

## 5. DoD

- `nurigym_step_record_v02_roundtrip_v1` pack 추가
- v0.1/v0.2 add-only 호환 검사
- `raw_action/normalized_action/action_status/merged_action/applied_action` 필드 roundtrip 확인
- `docs/ssot/**` 수정 없음
- Gym 의미론 closure 주장 없음. wire 증빙만 주장
