# PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707 — ANNEX A (구현 등급 정교화)

- 작성: 2026-07-09 KST, Claude Code (지시문 16 이행)
- 원 제안서: `docs/context/proposals/PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707.md`
- 기존 구현 확인: `pack/nurigym_step_record_v02_consumer_g6_v1/`(evidence tier `consumer_tool_layer_prototype`, `additive_only: true`)가 이미 존재하나, 원 제안서가 요구한 `nurigym_step_record_v02_roundtrip_v1`(§4)과 **이름·범위가 다르다** — 아래 (d)에서 이 간극을 구체적으로 정리한다.

**본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님.**

## (a) v0.1 대비 필드 표

| 필드 | v0.1 | v0.2 | 타입 | 필수성 | 마이그레이션 규칙 |
|---|---|---|---|---|---|
| `raw_action` | 없음 | 신규 | 원본 action 타입 | MUST | v0.1 리더는 무시 |
| `normalized_action` | 없음 | 신규 | action schema 타입 | MUST | v0.1 리더는 무시 |
| `action_status` | 없음 | 신규 | enum(`맞음`,`가만히`,`잘림`,`거부`) | MUST | v0.1 리더는 무시 |
| `resolved_action` | 없음 | 신규 | action schema 타입 | SHOULD | v0.1 리더는 무시 |
| `merged_action` | 없음 | 신규(shared mode에서 MUST) | action schema 타입 | shared: MUST / single: SHOULD | 단일 모드는 `applied_action`과 동치 허용 |
| `merge_candidates` | 없음 | 신규(shared mode에서 SHOULD) | array\<action schema\> | SHOULD | 없으면 "merge provenance incomplete" 마킹만, replay 실패 아님 |
| `applied_action` | 있음(v0.1의 사실상 유일한 action 필드) | 유지 | action schema 타입 | MUST | **필드명 자체는 안 바뀜** — v0.1 reader가 이 필드만 보고도 여전히 동작 |
| `missing_input` | 없음 | 신규 | array\<slot path\> | SHOULD | v0.1 리더는 무시 |
| `obs / reward / terminated / truncated / info` | 있음 | 유지, 변경 없음 | (기존과 동일) | MUST(기존과 동일) | 변경 없음 |

### v0.1 → v0.2 리더 호환 매트릭스

| 리더 종류 | v0.1 파일 읽기 | v0.2 파일 읽기 |
|---|---|---|
| v0.1 reader | 정상 | 정상(신규 필드 무시, `applied_action`만 사용) |
| v0.2 single-agent consumer | N/A(v0.1엔 없는 필드 요구 시 fallback 필요 — 아래 엣지케이스 E1) | 정상(`raw/normalized/action_status/applied`만 있어도 해석 가능) |
| v0.2 shared/multi-agent consumer | N/A | `merged_action`/`merge_candidates` 없으면 incomplete 마킹, 실패 아님 |

## (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | v0.2 single-agent consumer가 **v0.1 파일**(신규 필드 전혀 없음)을 읽음 | `raw_action`/`normalized_action`/`action_status`가 없으므로 이 3필드는 `null`/`미상`으로 채우고, `applied_action`만으로 최소 재생을 허용한다 — "MUST" 필드가 없다고 파일 전체를 거부하지 않는다 | 원 제안서 §3-3이 "v0.2 consumer는 최소 4필드만 있어도 해석 가능"이라 했으나, **v0.1 파일에는 그 4필드 중 3개가 아예 없는 경우**를 명시하지 않았음 — 이 ANNEX가 채우는 간극 |
| E2 | `거부` action인데 `merged_action`에 포함되어 있음(producer 버그) | `E_STEP_RECORD_REJECTED_IN_MERGE` — §3-5 "거부는 merge 후보에서 제외된 기록이 남아야 한다"의 위반을 조용히 넘기지 않는다 | 원 제안서 §3-5 규칙의 기계적 검증 필요 |
| E3 | `잘림`인데 `normalized_action == raw_action`(값이 안 바뀜) | `E_STEP_RECORD_CLIP_NOOP` 경고(fatal 아님) — "clip인데 왜 안 바뀌었나"는 producer 버그 신호이지만 wire schema 자체는 위반이 아니므로 경고로만 | §4 roundtrip 케이스 표 `clip`의 암묵적 불변식을 명시화 |
| E4 | shared mode인데 `agent_count=1` | `merged_action` MUST 요구를 완화해 single처럼 취급할지, 그래도 shared 스키마를 강제할지 결정 필요 — **남은 질문으로 이월** | (e) 참조 |
| E5 | v0.2 파일에 `missing_input`은 있는데 해당 슬롯이 `action_status=맞음`으로 기록됨(모순) | `E_STEP_RECORD_MISSING_STATUS_MISMATCH` — completion 정책상 missing slot은 `가만히`여야 하므로 모순 시 오류 | 지시문 10의 completion 정책(`#모두필요/#빈칸채움`, missing≠가만히 아님 주의)과 교차 |

## (c) 오류 코드 배정안

| 코드 | 배정 근거 | 카테고리 |
|---|---|---|
| `E_STEP_RECORD_REJECTED_IN_MERGE` | E2 | 런타임 |
| `E_STEP_RECORD_CLIP_NOOP` (경고, non-fatal) | E3 | 런타임(진단) |
| `E_STEP_RECORD_MISSING_STATUS_MISMATCH` | E5 | 런타임 |

## (d) pack DoD + golden fixture 스케치

**중요 발견**: 원 제안서 §4가 요구한 pack ID는 `nurigym_step_record_v02_roundtrip_v1`이지만, 실제로 존재하는 pack은 `pack/nurigym_step_record_v02_consumer_g6_v1/`(evidence tier `consumer_tool_layer_prototype`)이다. 후자는 consumer 층 프로토타입이고, 전자가 요구한 **producer→wire→consumer 왕복(roundtrip) 검증**과는 목적이 다르다. 두 pack이 같은 주제의 서로 다른 절반을 담당하는 것으로 보이며, **`nurigym_step_record_v02_roundtrip_v1`은 아직 미생성 상태로 간주해야 한다.**

- pack 후보: `nurigym_step_record_v02_roundtrip_v1` (원 제안서 §4 그대로 유지).
- golden fixture 스케치(원 제안서 §4 표를 그대로 구체화):
  - `c01_valid`: `action_status=맞음`, `raw_action == applied_action` — round-trip 후 두 값 byte-equal.
  - `c02_noop_missing`: `action_status=가만히`, `missing_input`에 정확히 1개 슬롯 경로 기록.
  - `c03_clip`: `action_status=잘림`, `normalized_action != raw_action`, `applied_action == normalized_action`, (b) E3 경고 미발생 확인(정상 케이스).
  - `c04_reject`: `action_status=거부`, `merge_candidates`에 해당 action 부재 확인((b) E2 방지 확인).
  - `c05_shared_merge`: 2 agent 입력 → `merge_candidates` 2건 + `merged_action` 1건.
  - `c06_v01_backward_read` (신규 추가 권고): v0.1 포맷 파일을 v0.2 consumer로 읽어 (b) E1 동작 확인.
  - DoD: 6케이스 PASS + `pack/nurigym_step_record_v02_consumer_g6_v1`과의 필드 정의 교차검증(동일 필드명/타입 사용).

## (e) 남은 결정 질문 (≤3)

1. **E4**: shared mode에서 `agent_count=1`일 때 `merged_action` MUST를 완화할지, 스키마를 그대로 강제해 항상 shared 형태로 기록할지.
2. **pack 이름 정리**: `nurigym_step_record_v02_roundtrip_v1`(원 제안서, 미생성)과 `nurigym_step_record_v02_consumer_g6_v1`(기존, consumer 층)의 관계를 하나로 통합할지, 역할을 분리해 둘 다 유지할지.
3. **`resolved_action`/`merge_candidates`(SHOULD 필드)가 실제로 얼마나 채워지는지** — 지금은 "있으면 좋음" 수준인데, shared mode에서 감사(audit) 목적상 SHOULD를 MUST로 올릴지.
