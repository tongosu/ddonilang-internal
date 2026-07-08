# PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706

- 작성: 2026-07-06
- 분류: PROPOSAL / NURI / MADI / TASK_CONFLICT / EXECUTION_CONTRACT
- 상태: 관리자 제출용 제안
- 기준: SSOT v24.12.9 읽기 전용 참조
- 변경 방식: `docs/ssot/**` 직접 수정 없음, parser/runtime 변경 없음

## 0. 목적

이 문서는 누리의 시간 운용, 마디 경계, 태스크/행동 경합 처리, 슬기 지연 주입을 하나의 실행 계약으로 정리하기 위한 제안이다.

핵심 판단:

1. 공식 world commit은 큰마디 기준이다.
2. 속마디는 local 진행, 제안 생성, trace 단계이며 shared world를 직접 확정하지 않는다.
3. 경합은 "먼저 온 것이 이긴다"가 아니라 deterministic collect/filter/merge/apply 파이프라인으로 처리한다.
4. 슬기/외부/사람/UI 입력은 모두 `InputSnapshot`으로 봉인되어야 한다.
5. `설정.누리`가 시간/입력/AI/보기 설정을 모두 빨아들이면 안 된다. 시간 운용은 `설정.실행`, 입력 봉인은 `설정.샘`, AI 지연은 `설정.슬기/샘`, 세계 정체성은 `설정.누리`로 나눈다.

## 1. 기존 잠금점 요약

| 항목 | 현재 기준 |
|---|---|
| 공식 commit | 큰마디 기준 |
| 속마디 | local progression / proposal / trace |
| 기본 시계 | 공유 큰마디 |
| completion | `#모두필요`, `#빈칸채움` |
| 기본 completion | `#모두필요` |
| missing vs noop | 미제출은 `가만히`가 아님 |
| `#빈칸채움` | missing slot을 `가만히`로 승격 |
| `#모두필요` | missing 또는 `거부` 슬롯이 있으면 마디 미완성 |
| action_status | `맞음`, `가만히`, `잘림`, `거부` |
| merge 후보 | `맞음`, `가만히`, `잘림` |
| merge 제외 | `거부` |
| shared env step | 큰마디당 `env.step(merged_action)` 1회 |
| Sam ordering | `(agent_id, recv_seq)` stable ordering |
| `recv_seq` | agent별 strict monotonic |
| 중복/역행 seq | input contract violation |
| `accepted_madi/target_madi` | scheduling metadata, execution ordering key 아님 |

## 2. 시간/마디 모델

### 2.1 큰마디

큰마디는 shared world의 공식 확정 단위다.

큰마디에서 확정되는 것:

- state transition
- `state_hash`
- reward / termination / truncation
- step_record
- replay record
- merged action
- 공식 observation boundary

### 2.2 속마디

속마디는 local 계산/제안/보간/trace 단계다.

속마디에서 허용되는 것:

- local preview
- actor별 proposal
- AI/슬기 생각 대기
- animation/interpolation용 view trace
- tentative action 후보
- debug/profiling trace

속마디에서 금지되는 것:

- shared world 공식 commit
- `state_hash` 확정
- reward/termination 최종 확정
- replay canonical record 대체

### 2.3 마디틈갈래

`마디틈갈래`는 마디 사이 세부 진행 정책이다.

v1 기준:

- `한걸음`: 속마디 없음 또는 단일 단계. 현재 allowed/designed/STUB_ONLY로 본다.

후속 후보:

- `여러속마디`: 큰마디 하나 안에 여러 local substep을 둔다.
- `고정박자`: 일정한 substep 수로 나눈다.
- `사건박자`: 이벤트 발생 시점 기준으로 local substep을 만든다.

주의:

- 후속 후보는 새 시간 의미론이므로 immediate closure로 주장하지 않는다.
- 속마디가 늘어나도 공식 commit 기준은 큰마디로 유지한다.

## 3. 실행 파이프라인

큰마디 하나의 기준 파이프라인:

```text
observe
  -> collect
  -> empty handling
  -> canonicalize
  -> validate/correct
  -> filter
  -> merge
  -> apply
  -> reward
  -> termination
  -> record
```

짧은 표기:

```text
모으기 -> 빈칸처리 -> 바른꼴화 -> 검증/보정 -> 거르기 -> 합치기 -> 적용 -> 보람 -> 판끝 -> 기록
```

경계:

- `거부`는 merge 후보에서 제외된다.
- `action_status` 값 자체는 보람 계산/관찰/trace로 전달될 수 있다.
- 엔진은 `거부`에 대해 자동 패널티를 넣지 않는다.
- reward shaping은 설계자 규칙이 맡는다.

## 4. 태스크/행동 경합 처리

### 4.1 경합의 대상

경합은 같은 큰마디에 여러 입력/행동/태스크가 들어올 때 발생한다.

대표 원천:

- 사람 입력
- UI event
- 슬기 의도
- 밖일 결과
- 일정/시나리오
- 이어전달
- replay 주입
- 여러 임자 행동

### 4.2 수집

모든 world-affecting 입력은 `InputSnapshot`으로 들어온다.

수집 단계에서 해야 할 일:

- source/provenance 기록
- agent/slot 식별
- target_madi 확인
- late/drop 여부 판정
- duplicate/reverse `recv_seq` 검출
- view-only 입력 분리

### 4.3 completion

| 정책 | 의미 | missing slot 처리 |
|---|---|---|
| `#모두필요` | 필요한 입력이 모두 와야 큰마디 확정 | missing 있으면 미완성 |
| `#빈칸채움` | 비어 있는 슬롯을 `가만히`로 채워 진행 | missing을 `가만히`로 승격 |

주의:

- 미제출은 기본적으로 `가만히`가 아니다.
- `#빈칸채움`에서만 missing이 `가만히`로 승격된다.
- 명시적 `가만히`, 암시적 `가만히`, 기다림 빠짐은 로그에서 구분할 수 있어야 한다.

### 4.4 action_status

| 상태 | 의미 | merge |
|---|---|---|
| `맞음` | action space 안의 정상 행동 | 후보 |
| `가만히` | 명시 noop 또는 completion으로 채운 noop | 후보 |
| `잘림` | out-of-range를 정책에 따라 잘라낸 행동 | 후보 |
| `거부` | 유효하지 않아 적용할 수 없는 행동 | 제외 |

### 4.5 merge

merge는 "도착 순서"가 아니라 deterministic policy로 한다.

기본 원칙:

- 같은 입력 집합은 항상 같은 merged_action을 만든다.
- `거부`는 merge 후보에서 제외한다.
- tie-break는 명시 정책이 없으면 runtime/pack에서 고정한 deterministic key를 쓴다.
- `priority`, `majority`, `turn_order`, `slot_owner` 같은 merge policy는 pack별 증빙이 필요하다.

후속 OI:

- `merge_policy`의 canonical key 위치를 `설정.실행`에 둘지, `설정.누리`의 world rule pack에 둘지 결정해야 한다.
- `priority` tie-break의 표면 이름과 slot/agent 매핑 규칙을 통일해야 한다.

## 5. 슬기/AI 지연 마디

슬기 패킷은 즉시 world를 바꾸지 않는다.

기준 흐름:

```text
observe
  -> SeulgiPacket
  -> Gatekeeper
  -> accepted_madi 기록
  -> target_madi 계산
  -> InputSnapshot.ai_injections
  -> 큰마디 파이프라인
```

규칙:

- `seulgi_latency_madi`는 세션 시작 시 고정한다.
- 패킷 수신 시 `accepted_madi = now_madi`를 찍는다.
- `target_madi = accepted_madi + seulgi_latency_madi`로 계산한다.
- `target_madi <= now_madi`인 늦은 패킷은 적용하지 않고 기록/알림만 남긴다.
- 현재 마디에 적용될 패킷만 `InputSnapshot.ai_injections`에 들어간다.
- 적용 정렬은 `(agent_id, recv_seq)`다.
- `target_madi`는 scheduling metadata이며 execution ordering key가 아니다.

열린 질문:

- `seulgi_latency_madi`를 `설정.슬기`에 둘지, `설정.샘`에 둘지, `설정.실행`에 둘지 결정이 필요하다.
- `target_madi` 기준으로 늦은 패킷을 drop할지, 대체 행동 요청까지 표준화할지 결정이 필요하다.

## 6. 설정 블록 경계

시간/마디/경합 계약을 `설정.누리`에 모두 넣으면 안 된다. 아래처럼 나누는 편이 안전하다.

| 블록 | 담당 | 예 |
|---|---|---|
| `설정.누리` | 세계 정체성, 세계 family, 초기 조건, rule pack | env_id, world_family, initial_state_ref |
| `설정.실행` | 마디 운용, completion, 걷기, 보람, 종료 | 마디맺음갈래, 행동모음갈래, 걷기갈래, 마디틈갈래 |
| `설정.샘` | 입력 원천, 주입 방식, InputSnapshot 봉인 | 입력원천, 주입방식, action_source |
| `설정.슬기` | AI 의도 생성/검문/지연 정책 후보 | 두뇌, 정책, 지연마디 후보 |
| `설정.거울` | 기록, 재연, 살핌 방출 | 기록갈래, 재연갈래, 살핌내주기갈래 |
| `설정.보개` | 보기 family/profile/meta | grid2d, graph2d, camera, overlay |

권고:

- `설정.누리`는 "세계가 무엇인가"에 집중한다.
- `설정.실행`은 "시간을 어떻게 걷고 마디를 어떻게 닫는가"를 맡는다.
- `설정.샘`은 "무엇이 입력으로 봉인되는가"를 맡는다.
- `설정.슬기`는 "AI가 언제 어떤 의도를 제안하는가"를 맡는다.

## 7. candidate key 초안

결정이 아니라 후보표다.

### 7.1 `설정.실행`

```ddn
설정 {
  실행 {
    마디맺음갈래: #모두필요.
    행동모음갈래: 차례모음.
    걷기갈래: 함께걷기.
    마디틈갈래: 한걸음.
    합치기갈래: priority.
  }
}
```

주의:

- `합치기갈래`는 후보 이름이다. 이미 쓰는 정본 이름과 충돌 검토가 필요하다.
- `priority`는 pack evidence가 있는 영역과 새 표면 후보를 구분해야 한다.

### 7.2 `설정.샘`

```ddn
설정 {
  샘 {
    입력원천: [사람, 슬기].
    주입방식: 실주입.
    세계영향경계: InputSnapshot.
  }
}
```

주의:

- `InputSnapshot` runtime canonical name은 바꾸지 않는다.
- 한국어 표면명을 둘 경우 runtime canonical name과 별도 alias인지 결정해야 한다.

### 7.3 `설정.슬기`

```ddn
설정 {
  슬기 {
    지연마디: 1.
    늦은제안다룸: 버림.
  }
}
```

주의:

- `지연마디` 소유권은 아직 열린 질문이다.
- `늦은제안다룸`은 새 후보이며, 즉시 구현 대상으로 주장하지 않는다.

## 8. 기본값 평가와 고급 옵션 노출 원칙

### 8.1 지금 그냥 두면 어떤 운용형인가

현행 논의를 그대로 두면 기본 누리 실행은 아래 성격에 가깝다.

> 동기식 큰마디 commit 기반의 결정적 turn/tick engine

즉 기본값은 다음에 가깝다.

| 축 | 기본 성격 |
|---|---|
| 시간 | 논리 시간 중심, wall-clock realtime 아님 |
| commit | 큰마디 기준 공식 확정 |
| 속마디 | 없거나 local trace/proposal 수준 |
| completion | `#모두필요` |
| missing input | 진행 보류, 자동 noop 아님 |
| noop | 명시 `가만히` 또는 `#빈칸채움`에서만 승격 |
| 경합 | deterministic filter/merge/apply |
| 슬기/AI | 직접 상태 변경 없음, `InputSnapshot` 경유 |
| replay | source 재호출 없이 기록된 snapshot 재생 |

이 기본형은 교육, 보드/격자 게임, NuriGym, replay 검증에 적합하다. 반대로 다음 성격은 기본값이 아니다.

- OS thread scheduler
- realtime physics engine loop
- async actor runtime
- optimistic transaction engine
- wall-clock event loop
- 자동 rollback/netcode

### 8.2 왜 기본값을 단순하게 둬야 하는가

마디/태스크/경합은 너무 깊은 영역이다. 초심자와 일반 제작자는 직접 만지지 않는 것이 맞다.

기본 노출 원칙:

1. 초심자에게는 `차림새` preset만 보인다.
2. 중급자는 `마디수`, `판끝`, `보람`, `입력`, `보개` 정도를 만진다.
3. 고급자만 completion, merge, substep, latency, late packet, fairness를 만진다.
4. runtime canonical name(`InputSnapshot`, `recv_seq`, `target_madi`)은 설명/진단층에는 보이되, 일반 작성 표면의 첫 화면에는 숨긴다.

### 8.3 권장 preset

| preset | 대상 | 시간/경합 성격 | 기본 옵션 |
|---|---|---|---|
| `교과기본` | 수업/예제 | 단일 누리, 단순 큰마디 | `#모두필요`, `한걸음`, 보람 없음 |
| `체험기본` | 조작형 학습 | 단일 사용자 체험 | `#모두필요`, `한걸음`, 뒤살핌 |
| `배움기본` | AI/Gym 학습 | episode/reward 중심 | `#모두필요`, `저마다보람`, `사건보람` |
| `협동기본` | 여러 임자 협동 | shared sync | `#모두필요`, deterministic merge |
| `놀이기본` | 턴제/격자 게임 | 번갈걷기/차례 | `#모두필요`, 보람 없음 기본 |
| `물리실험고급` | 연속/준연속 시뮬 | fixed substep 후보 | `여러속마디`, fixed dt 후보 |
| `슬기실험고급` | AI 지연/정책 실험 | fixed latency + replay | `지연마디`, late drop 후보 |
| `경합실험고급` | multi-agent conflict 연구 | merge policy 비교 | priority/majority/slot_owner 후보 |

주의:

- 뒤의 세 preset은 고급 후보이며 즉시 closure 대상이 아니다.
- 고급 preset은 문서/pack evidence가 생긴 뒤 단계적으로 열어야 한다.

### 8.4 고급자에게만 열 옵션

| 옵션 | 의미 | 위험 |
|---|---|---|
| `마디틈갈래` | 큰마디 안 substep 운용 | state/reward 확정 경계 혼동 |
| `#빈칸채움` | missing을 `가만히`로 승격 | 침묵과 noop 혼동 |
| `합치기갈래` | 경합 merge policy | 공정성/직관성/pack 증빙 필요 |
| `priority` tie-break | 우선순위 기반 선택 | agent/slot mapping 불명확 시 불공정 |
| `majority` | 다수결 merge | 동점 처리 규칙 필요 |
| `turn_order` | 차례 기반 적용 | simultaneous action과 충돌 |
| `지연마디` | 슬기/AI fixed latency | stale intent 처리 필요 |
| `늦은제안다룸` | late packet drop/revalidate/degrade | replay/UX/안전성 영향 |
| `공정성갈래` | starvation 방지/rotation | 결정성 유지와 충돌 가능 |
| `rollback` 후보 | 늦은 입력 보정 | replay/netcode 난도 급상승 |

권고:

- `rollback`, async shared env, wall-clock realtime scheduler는 장기 연구 후보로만 둔다.
- `#빈칸채움`, `priority`, `지연마디`도 pack evidence 없이 기본 UI에 노출하지 않는다.

### 8.5 더 나은 설정 제공 방식

사용자에게 raw knob를 직접 나열하기보다 "목적형 preset + 고급 펼침"으로 제공한다.

예:

```ddn
설정 {
  실행 {
    차림새: 교과기본.
  }
}
```

고급 예:

```ddn
설정 {
  실행 {
    차림새: 경합실험고급.
    마디맺음갈래: #모두필요.
    합치기갈래: priority.
  }
  슬기 {
    지연마디: 1.
    늦은제안다룸: 버림.
  }
}
```

위 고급 예시는 후보 표면이다. parser/runtime closure가 아니라 설정 설계 방향이다.

### 8.6 판단 기준

어떤 옵션을 열지 판단할 때 아래 질문을 먼저 한다.

1. 이 옵션이 state/reward/termination을 바꾸는가?
2. replay에서 같은 결과를 보장할 수 있는가?
3. missing input과 noop을 사용자가 혼동하지 않는가?
4. AI가 본 상태와 적용 상태가 달라졌을 때 안전한가?
5. pack으로 golden을 만들 수 있는가?
6. 초심자가 몰라도 되는가?

6번 답이 "예"이면 기본 UI가 아니라 고급 설정으로 둔다.

## 9. pack 후보

| pack 후보 | 목적 |
|---|---|
| `nuri_madi_big_small_boundary_v1` | 큰마디/속마디 commit 경계 |
| `nuri_madi_completion_all_required_v1` | `#모두필요` missing/거부 처리 |
| `nuri_madi_completion_fill_noop_v1` | `#빈칸채움` missing -> `가만히` |
| `nuri_task_action_status_pipeline_v1` | `맞음/가만히/잘림/거부` 파이프라인 |
| `nuri_task_merge_priority_tiebreak_v1` | deterministic priority merge |
| `nuri_seulgi_latency_target_madi_v1` | accepted/target madi와 late drop |
| `nuri_inputsnapshot_ordering_recv_seq_v1` | `(agent_id, recv_seq)` ordering 및 duplicate/reverse fail |
| `nuri_default_execution_profile_matrix_v1` | 기본 preset과 고급 옵션 노출 경계 |
| `nuri_advanced_option_risk_matrix_v1` | `#빈칸채움/merge/latency/rollback` 위험 분류 |

## 10. 지시문 후보

> 지시문 10 - 누리 시간/마디/태스크 경합 계약 심화
>
> 큰마디/속마디, completion(`#모두필요/#빈칸채움`), action_status(`맞음/가만히/잘림/거부`), filter-before-merge, deterministic merge, 슬기 지연마디, `(agent_id, recv_seq)` 실행 정렬을 하나의 실행 계약으로 정리한다. `설정.누리`는 세계 정체성, `설정.실행`은 마디 운용, `설정.샘`은 입력 봉인, `설정.슬기`는 AI 제안/지연으로 경계를 분리한다. parser/runtime 변경 없이 PROPOSAL과 pack 후보 목록까지만 산출한다.

DoD:

- 시간/마디 모델 표
- 경합 파이프라인
- completion/action_status/merge 규칙표
- 설정 블록 경계표
- 지연마디 소유권 OI 후보
- pack 후보 ID
- parser/runtime 변경 0건
- `docs/ssot/**` 수정 0건
- closure 주장 없음

## 11. 권고 결론

시간 마디와 태스크 경합은 누리 커스텀의 핵심이다. 다만 이것을 `설정.누리` 하나에 넣기보다, 세계 정체성/실행 정책/입력 봉인/슬기 지연/거울 기록으로 나눠야 한다.

권고:

1. 큰마디 공식 commit 원칙은 유지한다.
2. 속마디는 local proposal/trace로 제한한다.
3. 기본 completion은 `#모두필요`로 둔다.
4. `#빈칸채움`과 merge policy 변형은 extension pack track으로 둔다.
5. AI/슬기 지연은 `accepted_madi/target_madi`로 드러내되 execution ordering은 `(agent_id, recv_seq)`로 유지한다.
6. `설정.실행`에 마디 운용 후보 키를 모으고, `설정.누리`는 world identity와 initial/rule pack에 집중시킨다.
7. 기본 사용자는 preset만 쓰게 하고, completion/merge/substep/latency/rollback 계열은 고급 설정으로 숨긴다.
