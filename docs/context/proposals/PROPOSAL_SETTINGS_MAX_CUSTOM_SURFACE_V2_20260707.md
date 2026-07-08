# PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V2_20260707

- 작성: 2026-07-07 (Asia/Seoul)
- 분류: PROPOSAL / SETTINGS / MAX_SURFACE / CUSTOM_CONTRACT
- 상태: 관리자 제출용 제안, docs-first 최대 지도
- 기준: SSOT v24.12.9 읽기 전용 참조
- 변경 방식: `docs/ssot/**` 직접 수정 없음, parser/runtime 변경 없음, closure 주장 없음
- 선행: `PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706`, `PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706`

## 0. 목적과 판정

이 문서는 `설정 {}`을 최대한 심화했을 때 어디까지 열 수 있는지 그리는 전체 지도다. 즉시 구현 목록이 아니라, 앞으로 어떤 키 제안이 와도 "어느 절, 어느 층, 어떤 영향, 어떤 증빙"인지 좌표를 찍기 위한 기준 문서다.

핵심 판단:

1. 설정 자유도는 크게 늘릴 수 있다.
2. 다만 모든 설정이 같은 위험도를 갖지 않는다.
3. 결과영향 설정, 보기 설정, 문서 메타를 분리해 해시와 검증 기준을 다르게 둬야 한다.
4. `설정.누리`는 세계 정체성과 초기 조건에 집중하고, 시간 운용은 `설정.실행`, 입력 봉인은 `설정.샘`, AI는 `설정.슬기`, 보기와 시각화는 `설정.보개`, 기록과 재연은 `설정.거울`로 나눈다.
5. 새 키는 기본적으로 L4에서 태어나고, pack evidence가 쌓인 뒤에만 L3/L2/L1로 내려온다.

## 1. 설정이 될 수 없는 것

아래 항목은 아무리 커스텀을 깊게 열어도 일반 설정 knob가 되면 안 된다.

| 항목 | 판정 | 이유 |
|---|---|---|
| 큰마디 canonical 위상 순서 | 불변 | 순서가 knob이면 같은 코드가 다른 세계가 됨 |
| 위상 재진입 금지 | 불변 | cascade/fixpoint loop가 비결정성 입구가 됨 |
| 훅 발신 알림의 다음 마디 이월 | 불변 | 같은 마디 cascade 방지 |
| `될때/인 동안` 1-pass 재트리거 금지 | 불변 | fixpoint 반복 금지 |
| 쓰기 경합 FATAL 기본 | 불변 기본 | 완화는 `보탬` 같은 선언적 opt-in으로만 허용 |
| 속마디 관측 격리 | 불변 기본 | 속마디 수가 결과를 바꾸면 안 됨 |
| replay 실호출 0건 | 불변 | 재연은 원천 재호출이 아니라 기록 재주입 |
| `(agent_id, recv_seq)` 실행 정렬 | fixed base | Sam/Seulgi fixed base |
| `InputSnapshot` / Gatekeeper 경유 | fixed base | 외부/AI가 세계를 직접 쓰면 replay가 무너짐 |
| `state_hash` 경계 | fixed base | view/diag/doc는 world truth가 아님 |

## 2. 해시 4분할

V1의 `설정해시` 아이디어는 채택 가치가 높다. 다만 하나의 해시에 모든 설정을 넣으면 제목 변경이나 보기 설정 변경까지 replay 오류처럼 보일 수 있다. 따라서 네 층으로 나눈다.

| 해시 | 포함 | 쓰임 |
|---|---|---|
| `run_config_hash` | 결과 상태에 간접 영향을 주는 설정 | replay/dataset/CI 불일치 오류 기준 |
| `view_config_hash` | 보개/거울/보기/성능 설정 | screenshot/view parity, 디버그 재현 |
| `doc_config_hash` | 제목/설명/말씨 등 문서 메타 | 문서 감사, 배포 산출물 추적 |
| `settings_hash` | 위 세 해시의 envelope digest | 전체 감사/아카이브 |

규칙:

1. `run_config_hash` 불일치는 기본적으로 결정적 오류다.
2. `view_config_hash` 불일치는 world replay 오류가 아니라 보기 재현 경고다.
3. `doc_config_hash` 불일치는 실행 오류가 아니다.
4. `settings_hash`는 `state_hash` 입력이 아니라 기록층 동반 필드다.
5. `step_record`, `dataset_header`, `metrics_report`, replay header는 최소 `run_config_hash`를 기록해야 한다.

후보 pack:

- `settings_run_config_hash_seal_v1`
- `settings_view_config_hash_no_state_change_v1`
- `settings_doc_config_hash_audit_v1`

## 3. 시앗묶음

단일 `시앗` 하나로 모든 난수를 뽑으면, 슬기나 보개 실험을 추가했을 때 물리/게임 난수열이 밀릴 수 있다. 따라서 이름 있는 seed stream이 필요하다.

후보 표면:

```ddn
설정 {
  누리 {
    시앗: 1234.
    시앗묶음 {
      물리: 갈래시앗(1).
      슬기: 갈래시앗(2).
      섞기: 갈래시앗(3).
    }.
  }.
}
```

권고 의미:

```text
뿌리 시앗
  -> 이름 있는 시앗묶음
  -> 마디/임자/용도별 파생 seed
  -> InputSnapshot에 봉인
```

규칙:

1. 각 stream은 root seed와 stream name으로 domain-separated hash를 만든다.
2. stream 추가/제거가 다른 stream의 난수열을 흔들면 안 된다.
3. world-affecting 난수는 최종적으로 `InputSnapshot` 또는 replay 가능한 기록층에 봉인되어야 한다.
4. `view` 전용 난수는 `view_config_hash` 쪽에서 별도 취급해야 하며 `state_hash`를 바꾸면 안 된다.

후보 pack:

- `nuri_seed_stream_isolation_v1`
- `nuri_seed_stream_inputs_snapshot_bridge_v1`

## 4. 노출 4층 모델

| 층 | 대상 | 보이는 것 | 승격 조건 |
|---|---|---|---|
| L1 | 초심자 | `차림새` preset 하나 | 기본 제공, 설명 없이 안전 |
| L2 | 일반 제작자 | `마디수`, `시앗`, `주보기`, `판끝`, `말씨` 등 소수 | golden pack + 진단 문구 |
| L3 | 고급 제작자 | completion, merge, seed stream, slot mapping, 지연마디 | pack evidence + 문서 + 위험표 |
| L4 | 연구/실험 | 공정성, 사건박자, rollback, async, 고급 AI 정책 | 별도 연구 트랙, 기본 UI 비노출 |

운영 규칙:

1. 키는 L4에서 태어난다.
2. pack evidence와 사용자 문서가 생기면 L3로 내려온다.
3. 일반 제작자가 안전하게 쓸 수 있으면 L2로 내려온다.
4. 설명 없이 써도 안전한 것만 L1 preset이 된다.
5. 광고성 조기 노출은 금지한다.

## 5. 절별 최대 키 지도

표기:

- 영향: `결과영향`, `보기`, `메타`, `계약`
- 상태: `정본`, `후보`, `연구`, `불변`

### 5.1 `설정.누리`

`설정.누리`는 세계 정체성, 초기 조건, rule pack 선택에 집중한다. 보기 family는 여기에 넣지 않는다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `환경ID` | 문자열 | 없음 | 메타 | L2 | 후보 | 외부 Gym/dataset 연동 ID. 직접 rule 선택자가 되면 안 됨 |
| `시앗` | 정수 | 명시 권고 | 결과영향 | L2 | 후보 | root seed |
| `시앗묶음 {}` | 이름별 stream | 없음 | 결과영향 | L3 | 후보 | seed stream isolation |
| `세계갈래` | `grid2d/grid3d/continuous2d/...` | 없음 | 결과영향 | L2 | 후보 | world/state family. `space2d`는 제외 |
| `크기` | 격자/경계 값 | 없음 | 결과영향 | L2 | 후보 | grid bounds/world bounds |
| `경계다룸` | `막힘/감김/떨어짐` | `막힘` | 결과영향 | L3 | 후보 | 벽/토러스/낙하 |
| `첫상태참조` | template ref | 없음 | 결과영향 | L3 | 후보 | 실제 truth는 `채비`, 여긴 선택자 |
| `규칙묶음` | rule pack refs | 없음 | 결과영향 | L3 | 후보 | 가지/pack 경계 정리 필요 |
| `계산단위계` | SI 등 | SI | 결과영향 | L3 | 후보 | 계산 정규화 단위 |

주의:

- `space2d/space3d`는 view/presentation family이므로 `설정.보개`로 보낸다.
- `환경ID`가 rule pack이나 initial state를 고르면 `환경ID`가 아니라 `규칙묶음/첫상태참조`로 분리한다.

### 5.2 `설정.실행`

`설정.실행`은 시간, 마디, completion, merge, 보람, 종료를 담당한다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `차림새` | 5종 정본 + 고급 후보 | `교과기본` | 결과영향 | L1 | 정본/후보 | 일반 사용자 기본 진입점 |
| `마디수` | 정수 | 없음 | 결과영향 | L2 | 후보 | 실행 길이 |
| `결정갈래` | D-STRICT/D-FAST/D-ULTRA | D-STRICT | 결과영향 | L3 | 정본 축 | closure 상태 분리 필요 |
| `마디맺음갈래` | `#모두필요/#빈칸채움` | `#모두필요` | 결과영향 | L3 | 정본 | 기본 UI 비노출 권고 |
| `행동모음갈래` | 차례/보탬/앞선/다수결/자리모음 | 차림새 따름 | 결과영향 | L3 | 정본+후보 | `합치기갈래`와 충돌 검토 |
| `동점다룸` | 자리차례/사전차례 | 자리차례 | 결과영향 | L3 | 후보 | merge tie-break 명시 |
| `걷기갈래` | 함께걷기/번갈걷기 | 차림새 따름 | 결과영향 | L3 | 정본 |
| `마디틈갈래` | 한걸음/여러속마디/고정박자/사건박자 | 한걸음 | 결과영향 | L3~L4 | 일부 정본+연구 |
| `속마디수` | 정수 | 없음 | 결과영향 | L4 | 연구 | 여러속마디 딸림 |
| `속틈` | 시간값 | 없음 | 결과영향 | L4 | 연구 | fixed dt 후보 |
| `보람주인갈래` | 정본 집합 | 차림새 따름 | 결과영향 | L3 | 정본 |
| `보람때갈래` | 정본 집합 | 차림새 따름 | 결과영향 | L3 | 정본 |
| `판끝갈래` | 정본 집합 | 차림새 따름 | 결과영향 | L3 | 정본 |
| `공정성갈래` | 없음/돌림 | 없음 | 결과영향 | L4 | 연구 | starvation 방지 후보 |

권고:

- `합치기갈래`라는 새 키를 만들기 전에 기존 `행동모음갈래`와 역할을 정리한다.
- `#빈칸채움`, `동점다룸`, `공정성갈래`는 고급 설정이다.

### 5.3 `설정.샘`

`설정.샘`은 입력 원천, 주입 방식, InputSnapshot 봉인을 담당한다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `입력원천` | 사람/슬기/밖일/일정/이어전달/펼침실행 | 차림새 따름 | 결과영향 | L3 | 정본 축 |
| `주입방식` | 실주입/재연주입 | 실주입 | 결과영향 | L3 | 정본 축 |
| `슬롯정의 {}` | agent slot -> source mapping | 없음 | 결과영향 | L3 | 후보 | action source spec 해소 자리 |
| `입력틈` | 마지막것/모두큐/눌림유지 | 마지막것 | 결과영향 | L3 | 후보 | UI event coalescing |
| `늦은입력다룸` | 다음마디이월/버림 | 다음마디이월 | 결과영향 | L3 | 후보 | 사람 입력의 마디 중간 도착 |

불변:

- `InputSnapshot` runtime canonical name은 바꾸지 않는다.
- world-affecting 입력은 반드시 `InputSnapshot`으로 봉인한다.

### 5.4 `설정.슬기`

`설정.슬기`는 AI 의도 생성, 검문, 지연 정책 후보를 다룬다. AI가 world를 직접 쓰는 knob는 열지 않는다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `두뇌` | 규칙형/LLM통로/배움틀 | 없음 | 결과영향 | L3 | docs-first |
| `정책` | policy ref | 없음 | 결과영향 | L3 | docs-first |
| `끼우개` | adapter ref | 없음 | 결과영향 | L3 | docs-first |
| `지연마디` | 정수 | 1 후보 | 결과영향 | L3 | 후보 | 소유권 OI: 슬기/샘/실행 |
| `늦은제안다룸` | 버림/이월/다시매김 | 버림 | 결과영향 | L3~L4 | 후보 |
| `제안한도` | 마디당 의도 수 | 없음 | 결과영향 | L4 | 후보 | Gatekeeper throttle |
| `관찰범위` | 전체/관찰목록 ref | 전체 | 결과영향 | L3 | 후보 | 부분 관찰, 소유권 OI |
| `승인갈래` | 수문장 단일값 | 수문장 | 계약 | L4 | 사실상 불변 | 우회값 금지 |
| `재연갈래` | 기록재주입 단일값 | 기록재주입 | 계약 | L4 | 사실상 불변 | 원천 재호출 금지 |
| `공방설정/추론설정` | 배움틀 | 없음 | 결과영향 | L4 | docs-first |

권고:

- `승인갈래/재연갈래`는 키처럼 보이더라도 사실상 단일값 계약이다.
- raw prompt/response/debug trace는 `state_hash` 밖에 둔다.

### 5.5 `설정.거울`

`설정.거울`은 기록, 재연, 살핌 방출, replay seek 성능을 담당한다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `기록갈래` | 전체/요약/없음 | 차림새 따름 | 보기 | L3 | 후보 |
| `재연갈래` | 기록재주입 | 기록재주입 | 계약 | L4 | 사실상 불변 | 원천 재호출 금지 |
| `살핌내주기갈래` | 뒤살핌 등 | 뒤살핌 | 보기 | L3 | 정본 자리 |
| `스냅틈` | N마디마다 snapshot | 없음 | 보기/성능 | L3 | 후보 | seek 가속, 의미 불변 증빙 필요 |
| `해시검사틈` | 매마디/판끝/없음 | 매마디 | 보기/성능 | L3 | 후보 | 검출 시점만 변화 |
| `보관한도` | 기록 보존 한도 | 없음 | 보기 | L3 | 후보 |

### 5.6 `설정.보개`

`설정.보개`는 보기 family/profile/meta를 담당한다. world truth가 아니다.

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 | 메모 |
|---|---|---|---|---|---|---|
| `주보기` | grid2d/space2d/graph/table 등 | 차림새 따름 | 보기 | L2 | 후보/정본 혼재 |
| `곁보기` | list | 없음 | 보기 | L2 | 후보 |
| `겹보기` | overlay refs | 없음 | 보기 | L3 | 후보 |
| `백엔드` | console_headless/web2d/engine3d | host 결정 | 보기 | L3 | 후보 | backend 선택은 toolchain 책임도 있음 |
| `프로필` | grid2d/sim2d/graph2d/grid3d/game3d | family 따라 | 보기 | L3 | 후보 |
| `표준팩` | `std_bogae_*` | family 따라 | 보기 | L2~L3 | 후보 |
| `재생속도` | 배속 | 1x | 보기 | L2 | 후보 |
| `표시단위계` | SI/사용자 단위 | 계산단위계 따름 | 보기 | L2 | 후보 | 계산단위계와 분리 |

주의:

- `space2d/space3d`는 여기에 둔다.
- view-only 입력은 `state_hash` 밖에 둔다.
- world-affecting 보개 조작은 `ui.event -> InputSnapshot` 경계를 탄다.

### 5.7 `설정.문서`

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 |
|---|---|---|---|---|---|
| `이름/제목` | 문자열 | 없음 | 메타 | L2 | 후보 |
| `설명` | 문자열 | 없음 | 메타 | L2 | 후보 |
| `말씨` | ko/ko-common/en/... | ko | 메타/입력 표면 | L2 | 정본 축 |

### 5.8 `설정.이야기`

| 키 | 값 후보 | 기본 | 영향 | 층 | 상태 |
|---|---|---|---|---|---|
| `들머리` | flow/scene ref | 기본 진입점 | 결과영향 | L2 | 후보 |
| `흐름묶음` | story/flow pack ref | 없음 | 결과영향 | L3 | 후보 |

## 6. 결과영향 분류표

| 분류 | 예 | 해시 |
|---|---|---|
| 결과영향 | `시앗`, `세계갈래`, `크기`, `마디수`, `마디맺음갈래`, `들머리`, `지연마디` | `run_config_hash` |
| 보기 | `주보기`, `프로필`, `표준팩`, `스냅틈`, `재생속도`, `표시단위계` | `view_config_hash` |
| 메타 | `제목`, `설명`, 기록용 `환경ID` | `doc_config_hash` 또는 settings envelope |
| 계약/불변 | `InputSnapshot`, Gatekeeper, replay no-recall, `(agent_id, recv_seq)` | 설정 knob 금지 |

## 7. 안전 규칙

1. 모든 결과영향 키는 `run_config_hash`에 포함한다.
2. 보기/성능 키는 결과 불변 pack을 먼저 가져야 한다.
3. `승인갈래/재연갈래`는 단일값 계약이거나 설명층으로 강등한다.
4. `설정.누리`에 view family를 넣지 않는다.
5. `설정.실행`에 merge/time 고급 knob를 열 때는 위험표를 동반한다.
6. `설정.샘/슬기`는 `InputSnapshot` 우회 경로를 만들 수 없다.
7. L3/L4 키는 초심자 UI에 노출하지 않는다.

## 8. 신규 pack 후보

| pack 후보 | 목적 |
|---|---|
| `settings_run_config_hash_seal_v1` | 결과영향 설정 digest 계산/기록/불일치 오류 |
| `settings_view_doc_hash_split_v1` | view/doc config hash 분리 |
| `nuri_seed_stream_isolation_v1` | stream 추가가 타 stream 난수열을 흔들지 않음 |
| `nuri_boundary_policy_v1` | `경계다룸` 3값 의미 |
| `sam_slot_source_mapping_v1` | `슬롯정의` 매핑 결정성 |
| `sam_input_coalesce_v1` | `입력틈` 병합 정책 |
| `seulgi_observation_scope_v1` | `관찰범위` 부분 관찰 마스킹 |
| `geoul_perf_keys_no_state_change_v1` | 스냅틈/해시검사틈 결과 불변 |
| `exec_tiebreak_deterministic_v1` | `동점다룸` 결정성 |
| `settings_exposure_layer_lint_v1` | L1~L4 노출층 lint |

## 9. 권고 우선순위

1. `run_config_hash/view_config_hash/doc_config_hash/settings_hash` 분리
2. `시앗묶음`
3. `슬롯정의`
4. `경계다룸`, `입력틈`, `늦은입력다룸`
5. `관찰범위`, `제안한도`
6. `스냅틈`, `해시검사틈`
7. L4 연구 키는 지도에만 보관

## 10. DoD

- 설정이 될 수 없는 불변 계약 표
- 해시 4분할 모델
- `시앗묶음`과 InputSnapshot 연결
- L1~L4 노출 모델
- 절별 최대 키 지도
- 결과영향/보기/메타/계약 분류표
- pack 후보 목록
- parser/runtime 변경 0건
- `docs/ssot/**` 수정 0건
- closure 주장 없음
