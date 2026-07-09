# PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706 — ANNEX A (구현 등급 정교화)

- 작성: 2026-07-09 KST, Claude Code (지시문 16 이행)
- 원 제안서: `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md`
- 기존 fixture 정합 확인: `pack/nuri_madi_phase_trace_g1_v1/`(P0~P7 trace + `E_MADI_WRITE_CONFLICT` fixture, evidence tier `pack_skeleton`)와 스키마 충돌 없음.

**본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님.**

## (a) 정확한 스키마 표

### A.1 큰마디 위상 실행 레코드 (`nuri.madi_phase_trace.v1` 후보)

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `schema` | string | 필수 | - | `"ddn.nuri_madi_phase_trace.v1"` 고정 |
| `madi_index` | u64 | 필수 | - | P0에서 확정된 `now_madi` |
| `phase` | enum(`P0`..`P7`) | 필수 | - | 현재 위상 |
| `phase_seq` | u32 | 필수 | - | 같은 마디 내 위상 진행 순서(0부터, 재진입 없음 검증용) |
| `sub_phase` | enum(`3a`..`3g`, null) | 선택 | `null` | `phase=P3`일 때만 채움 |
| `read_boundary` | enum(`prev_commit`, `prev_commit_plus_self_tentative`, `post_commit`, `none`) | 필수 | - | 위상표 "읽기 경계" 열과 1:1 대응 |
| `write_target` | enum(`madi_counter`, `input_snapshot`, `none`, `patch_or_defer`, `world`, `reward_done`, `record_layer`, `view_meta_only`) | 필수 | - | 위상표 "쓰기" 열과 1:1 대응 |

### A.2 write-conflict 판정 레코드 (기존 `pack/nuri_madi_phase_trace_g1_v1/write_conflict_fatal.detjson` 스키마 확장)

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `conflict.class` | enum(`W1`,`W2`,`W3`) | 필수 | - | §2.1 분류 |
| `conflict.slot` | string | 필수 | - | 충돌 대상 경로(dotted) |
| `conflict.writers[].agent_id` | string | 필수 | - | 기존 필드 유지 |
| `conflict.writers[].recv_seq` | u64 | 필수 | - | 기존 필드 유지 |
| `conflict.opt_in_merge_policy_present` | bool | 필수 | `false` | §2.2 옵션(다) 적용 여부 |
| `conflict.opt_in_merge_op` | enum(`sum`,`none`) | 선택 | `none` | (다) 적용 시 연산자. v1은 `sum`(보탬)만 |
| `expected.error_code` | string | 필수 | - | `E_MADI_WRITE_CONFLICT` (opt-in 미적용 시) |
| `expected.fatal` | bool | 필수 | `true` | v1 기본값 = FATAL(권고 (가)) |

## (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | 같은 마디, 같은 슬롯에 동일 값을 두 번 쓰기(값 일치) | 여전히 `E_MADI_WRITE_CONFLICT` FATAL — "우연히 같은 값"은 결정성 예외로 두지 않는다 | 침묵 마스킹 금지 원칙(§2.2 옵션 (나) 배제 사유와 동일 논리) |
| E2 | 같은 임자가 같은 마디 안에서 같은 슬롯에 두 번 쓰기(자기 자신과의 충돌) | 충돌 아님 — `writers` 배열이 단일 `agent_id`면 순서대로 마지막 쓰기가 결정적으로 적용(임자 자신의 순차 로직은 대상 밖) | W1~W3는 "둘 이상의 임자/규칙" 정의를 그대로 따름(§2.1) |
| E3 | `opt_in_merge_policy_present=true`인데 세 번째 writer가 non-numeric 값을 씀 | `E_MADI_WRITE_CONFLICT`(합산 불가 타입) — 옵션 (다)는 교환·결합 연산 전제이므로 타입 게이트 필요 | §2.2 옵션 (다) "표면 설계 필요" 언급을 타입 체크로 구체화 |
| E4 | W2(복수 `미루기`가 같은 대상)이면서 그중 하나가 같은 덩이, 다른 하나가 다른 덩이 | 덩이 경계 무관 — 마디 끝(P4) 기준으로 판정. 덩이는 중간 커밋일 뿐 최종 충돌 판정 단위가 아님 | §2.3 "state_hash는 P4에서만 확정" |
| E5 | 3e(`될때/인 동안`)에서 재트리거 조건이 같은 마디 안에서 다시 참이 됨 | 재발화 없음(1-pass, 옵션 A) — 다음 마디에서 재판정 | §1.1 3e 권고 A |
| E6 | 3g에서 발신된 알림이 즉시 처리 가능해 보이는 경우(예: 같은 임자가 발신+수신) | 여전히 다음 마디 P1로 이월 — 예외 없음(cascade 차단 절대 규칙) | §1.1 3g |

## (c) 오류 코드 배정안

| 코드 | 배정 근거 | 카테고리(`PRELAUNCH_ERROR_CODE_AUDIT_V1` 기준) |
|---|---|---|
| `E_MADI_WRITE_CONFLICT` | W1/W2/W3 전체 공통 코드(§2.2 옵션 (가)). 이미 `pack/nuri_madi_phase_trace_g1_v1/write_conflict_fatal.detjson`에 fixture로 존재, `OI_CANDIDATES_20260706_BUNDLE.md`의 `OI-NURI-WRITE-CONFLICT-ERROR-01`이 정확히 이 코드를 후보로 등재함 — 신규 코드 아니라 기존 후보 재확인 | 런타임 |
| `E_MADI_PHASE_REENTRY` (신규 후보) | §1.2 "재진입 없음" 위반 시. 위상표 자체는 설계 불변식이라 정상 실행에서는 발생 불가하지만, 구현 버그 방지용 assertion 코드로 배정 권고 | 런타임 |
| `E_NURI_SEUM_CYCLE` (신규 후보) | OQ-2에서 "순환 의존은 오류"를 채택할 경우의 코드. OQ-2 미결이므로 **결정 후 명명**(가칭) | 런타임 |

남은 질문(d)의 OQ-2 해소 전까지 `E_NURI_SEUM_CYCLE`은 이름만 가칭이다.

## (d) pack DoD + golden fixture 스케치

기존 6개 pack 후보(§7)를 그대로 채택하고, 각각의 최초 golden fixture 스케치를 아래처럼 구체화한다.

### `nuri_state_write_conflict_v1` — W1~W3 최소 재현 DDN 예제

```ddn
// c01_w1_same_madi_two_writers.ddn — W1: 같은 마디, 두 patch가 같은 키에 즉시 대입
누리 {
  agent.alpha 임자 {
    (매마디)마다 { 누리.entity.agent.alpha.위치.x <- 1. }
  }
  agent.beta 임자 {
    (매마디)마다 { 누리.entity.agent.alpha.위치.x <- -1. }
  }
}
// 기대: 1마디 진행 시 E_MADI_WRITE_CONFLICT, fatal=true, world_commit_allowed=false
```

```ddn
// c02_w2_two_defers_same_target.ddn — W2: 복수 미루기가 같은 대상을 겨냥
누리 {
  agent.alpha 임자 {
    (매마디)마다 { 미루기 { 누리.entity.agent.alpha.체력 <- 0. } }
  }
  agent.beta 임자 {
    (매마디)마다 { 미루기 { 누리.entity.agent.alpha.체력 <- 100. } }
  }
}
// 기대: 덩이 끝 적용 시 E_MADI_WRITE_CONFLICT (W2 분류)
```

```ddn
// c03_w3_merged_action_vs_rule_write.ddn — W3: merged_action 반영과 규칙 쓰기 충돌
누리 {
  agent.alpha 임자 {
    (매마디)마다 { 누리.entity.agent.alpha.위치.x <- 받은행동.dx. }
  }
  // 별도 규칙이 같은 마디에 같은 슬롯을 씀
  전역 규칙 {
    (매마디)마다 { 누리.entity.agent.alpha.위치.x <- 0. }
  }
}
// 기대: E_MADI_WRITE_CONFLICT (W3 분류, action 반영과 규칙 쓰기 간)
```

각 케이스의 golden은 `expected_error_code=E_MADI_WRITE_CONFLICT` + `conflict.class` 태그(W1/W2/W3)를 `write_conflict_fatal.detjson` 확장 스키마(§(a) A.2)로 검증한다.

### `nuri_madi_phase_order_v1` — 훅 4가족 × 위상 배치 결정표

| 훅 가족 | 배치 위상 | 근거 |
|---|---|---|
| `할때` (`(시작)할때`) | 3a | 원 제안서 §1.1 3a와 동일 |
| `마다` (`(매마디)마다`, 기본형) | 3b | 원 제안서 §1.1 3b |
| `마다` (`(N마디)마다`, 변형) | 3b 내부, `madi_index % N == 0`일 때만 실행 — **OQ-4 권고 지점** | 아래 OQ-4 예시 참조 |
| `바뀔때마다` | 3d | 원 제안서 §1.1 3d |
| `될때 / 인 동안` | 3e (1회 판정, 1-pass) | 원 제안서 §1.1 3e |

### `(N마디)마다` 판정 시점(OQ-4) 옵션별 결과 차이 예시 3개

가정: `(3마디)마다 { 누리.점수 <- 누리.점수 + 1. }`, 3b에서 `merged_action`이 이번 마디에 점수를 바꿀 수도 있는 상황.

| 옵션 | 판정 위치 | 마디 1,2,3,4,5,6 결과(점수 증가 발생 마디) | 비고 |
|---|---|---|---|
| 옵션 A (3b 진입 직후, `merged_action` 반영 전) | 3b 최상단 | 3, 6 | `(N마디)마다` 본문이 그 마디의 `merged_action` 효과를 아직 못 봄 |
| 옵션 B (3b 내부, `merged_action` 반영 후) | 3b 하단 | 3, 6 (동일 마디에 발동하지만 실행 순서상 merged_action 이후) | 같은 마디 안에서 `merged_action`이 만든 값을 `(N마디)마다` 본문이 읽을 수 있음 — 순서 의존 버그 위험 |
| 옵션 C (3c 세움 재평가 이후) | 3c 하단 | 3, 6 (세움 재평가 결과까지 반영된 상태에서 실행) | 세움 재평가가 점수에 영향을 주는 규칙이 있으면 옵션 A/B와 최종값이 달라질 수 있음 |

권고: **옵션 A** — `(N마디)마다`는 "이번 마디가 몇 번째인가"만으로 결정되는 시간 훅이지 행동 결과에 의존하는 훅이 아니므로, `merged_action` 반영 전에 판정해 행동-무관성을 보장한다. 원 제안서 OQ-4는 이 예시로 해소 가능하나 **최종 채택은 사용자/SSOT 오너 결정**.

## (e) 남은 결정 질문 (≤3)

1. **OQ-2 순환 의존 처리 방식**: 세움↔매마디 순환 의존을 정적 분석(canon 단계)으로 잡을지, 실행 중 감지(런타임 오류 `E_NURI_SEUM_CYCLE` 가칭)로 잡을지 — 정적 분석이 더 안전하지만 canonicalizer 구현 비용이 크다.
2. **OQ-4 (N마디)마다 판정 시점**: 위 3옵션 중 최종 채택(권고: 옵션 A).
3. **§2.2 옵션 (다) 적용 범위**: "보탬(합)" 연산만 v1 opt-in으로 열지, 다른 교환·결합 연산(예: `최댓값`, `최솟값`)도 포함할지.
