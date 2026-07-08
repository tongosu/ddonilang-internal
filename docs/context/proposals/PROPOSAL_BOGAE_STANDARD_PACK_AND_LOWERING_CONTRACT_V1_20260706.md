# PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706

- 작성: 2026-07-06
- 분류: PROPOSAL / BOGAE / STANDARD_PACK / LOWERING_CONTRACT
- 상태: 관리자 제출용 제안
- 기준: SSOT v24.12.9 읽기 전용 참조
- 변경 방식: `docs/ssot/**` 직접 수정 없음, parser/runtime 변경 없음

## 0. 목적

이 문서는 보개를 `모양` 원자만으로 직접 짜야 하는 저수준 도구로 두지 않고, 사용자가 실제로 쓸 수 있는 표준 보개팩과 lowering 계약으로 정리하기 위한 제안이다.

핵심 판단:

1. 기존 `console_headless / web2d / engine3d` 백엔드 축과 `grid2d / sim2d / graph2d / grid3d / game3d` 프로필 축은 유지한다.
2. `모양`은 최종 출력 원자이고, 사용자는 `그래프/표/격자/시간줄/상태/슬기실험` 같은 의미 단위 보개를 써야 한다.
3. 모든 표준 보개는 마지막에 deterministic DrawList 또는 그에 준하는 scene payload로 내려가야 한다.
4. 보개는 state를 읽을 수 있지만, view-only 설정은 `state_hash`를 바꾸지 않는다.
5. 세계에 영향을 주는 입력은 반드시 `InputSnapshot` 경로를 통과해야 한다.

## 1. 기존 결정과의 관계

이 문서는 새 백엔드 체계를 만들지 않는다.

기존 축:

| 축 | 값 | 역할 |
|---|---|---|
| backend | `console_headless` | 기준 구현, headless 검증, 해시 확인 |
| backend | `web2d` | 2D 교육/그래프/시뮬/게임 보기 |
| backend | `engine3d` | 3D/게임 엔진 어댑터 |
| profile | `grid2d` | 2D 격자 세계 보기 |
| profile | `sim2d` | 연속 2D 시뮬레이션 보기 |
| profile | `graph2d` | 그래프/차트 보기 |
| profile | `grid3d` | 3D 격자/voxel 보기 |
| profile | `game3d` | 3D 게임 장면 보기 |

본 제안은 위 축 위에 "표준 보개팩"을 올린다.

## 2. 층 구분

| 층 | 이름 | 예 | 책임 |
|---|---|---|---|
| 1 | 의미 보개 | 그래프, 표, 격자, 시간줄, 슬기실험 | 사용자가 말하는 보기 단위 |
| 2 | 표준 보개팩 | `std_bogae_graph2d`, `std_bogae_grid2d` | 의미 보개의 공통 어휘와 기본 동작 |
| 3 | 프로필 빌더 | `graph2d`, `grid2d`, `sim2d` | 상태/메타를 DrawList로 내림 |
| 4 | 백엔드 소비자 | console, web, engine | 실제 표시, 장치별 UX |

중요한 점:

- `graph2d`는 모양 묶음이 아니라 그래프 의미 프로필이다.
- `console_headless`는 제품 보개가 아니라 검증 기준선이다.
- `web2d`와 `engine3d`는 같은 world를 다르게 보여 줄 수 있지만, world 의미를 바꾸면 안 된다.

## 2.1 사용성 원칙: `모양`은 탈출구, 표준 보개팩은 생산 도구

`모양`은 저수준 탈출구로 남겨야 한다. 사용자가 매번 축, 눈금, 범례, 좌표계, 카메라, 표, 타임라인, AI 실험 화면을 `모양` 원자로 직접 조립하게 되면 보개 체계는 실사용 언어가 아니라 drawing API가 된다.

비유:

- Python 사용자는 보통 그래프를 직접 pixel primitive로 그리지 않고 `matplotlib`, `plotly`, `pandas`, `networkx` 같은 라이브러리를 쓴다.
- 또니랑도 언어 핵심이 모든 시각화를 직접 품는 구조가 아니라, 표준 보개팩 생태계를 통해 보기와 조작을 제공해야 한다.

운영 규칙:

1. 자주 쓰는 보기/조작은 표준 보개팩으로 미리 제공한다.
2. 제품별 특수 표현은 커스텀 보개팩 템플릿으로 만든다.
3. 아주 특수한 경우에만 `모양` 원자로 직접 내린다.
4. 그래프/표/격자/타임라인/AI 실험 화면을 사용자가 반복해서 `모양`으로 직접 만들고 있다면, 표준 보개팩 부족으로 판정한다.

## 3. 표준 보개팩 목록

### 3.1 `std_bogae_core`

모든 보개팩의 공통 바닥.

포함:

- 캔버스 크기
- 레이어
- 색
- 글자
- 선/사각형/그림/sprite
- 선택/강조/비활성 표시
- view-only hit area
- asset 참조

내림:

- BDL1 DrawList 명령 집합
- BDL2 후보가 허용되기 전까지 원/곡선은 고정 근사 규칙 사용

### 3.2 `std_bogae_grid2d`

격자 게임, gridworld, 보드게임, 퍼즐, 교육용 행렬 보기.

포함:

- 정수 행렬
- 칸 크기
- 의미판, 색판, 글자판, 타일판
- 임자/아이템/벽/목표/위험 칸
- 선택 칸, 이동 가능 칸, 경로 표시
- fog/unknown/visited 표시
- 좌표 라벨

내림:

- `console_headless`: glyph 행렬 + 로그
- `web2d`: tile/sprite/rect DrawList
- `engine3d`: 필요하면 `grid3d` 또는 scene payload로 승격

대표 pack 후보:

- `bogae_std_grid2d_matrix_palette_v1`
- `bogae_grid2d_console_web_parity_v1`
- `bogae_grid2d_path_highlight_v1`

### 3.3 `std_bogae_graph2d`

그래프를 `모양` 직접 조립 없이 그리기 위한 표준팩.

포함:

- 축
- 눈금
- 범례
- 제목/축 이름
- 선그래프
- 점그래프
- 막대그래프
- 히스토그램
- heatmap
- 다중 series
- log/linear scale
- hover/cursor용 view-only 선택점
- 주석/기준선/영역 강조

결정성 규칙:

- auto domain, auto tick은 고정 알고리즘이어야 한다.
- 같은 데이터와 같은 view_meta는 같은 DrawList를 만들어야 한다.
- text 측정값에 따라 tick 개수가 바뀌면 안 된다.
- label 겹침 해소는 deterministic priority 규칙을 둔다.

내림:

- axis/tick/label -> `Line` + `Text`
- line series -> `Line` 연속 명령
- point series -> BDL1에서는 고정 크기 `RectFill`, BDL2에서는 `CircleFill`
- bar series -> `RectFill`
- heatmap -> cell `RectFill`

대표 pack 후보:

- `bogae_graph2d_axis_tick_determinism_v1`
- `bogae_graph2d_series_lowering_v1`
- `bogae_graph2d_label_overlap_policy_v1`

### 3.4 `std_bogae_table`

수치/상태/관찰값을 표로 보는 표준팩.

포함:

- 행/열
- 헤더
- 정렬
- cell format
- 조건부 강조
- diff 표시
- pinned row/column

내림:

- console: aligned text table
- web2d: text + rect grid
- engine3d: 기본 제외, 필요 시 HUD overlay

대표 pack 후보:

- `bogae_table_state_snapshot_v1`
- `bogae_table_diff_highlight_v1`

### 3.5 `std_bogae_sim2d`

물리, 셈그림, 연속 좌표 시뮬레이션 보기.

포함:

- world 좌표계
- camera/viewport
- 점/물체/벡터/힘/속도
- 궤적
- 센서/범위
- 충돌 영역 표시
- 수치 overlay

결정성 규칙:

- world 좌표는 fixed 계열로 계산한다.
- 픽셀 반올림은 고정 규칙을 쓴다.
- 카메라 추적은 view_meta이며 state 의미를 바꾸지 않는다.

대표 pack 후보:

- `bogae_sim2d_vector_trace_v1`
- `bogae_sim2d_sensor_overlay_v1`

### 3.6 `std_bogae_timeline`

마디, 판, episode, replay, 실험 로그를 시간축으로 보는 표준팩.

포함:

- 마디 번호
- 입력 이벤트
- 상태 해시 변화
- reward/terminated/truncated
- 되감기/비교용 view-only cursor
- 분기 비교

내림:

- console: tick log
- web2d: timeline + marker + selected slice
- engine3d: HUD overlay 또는 replay controller와 연결

대표 pack 후보:

- `bogae_timeline_madi_episode_trace_v1`
- `bogae_timeline_state_hash_diff_v1`

### 3.7 `std_bogae_nurigym`

누리짐 환경을 만들고 시험하는 전용 보기.

포함:

- observation
- action
- reward
- terminated/truncated
- info
- episode seed
- policy action provenance
- action_status 4종
- step throughput 요약

경계:

- Gym step 의미는 런타임/consumer 계약에 둔다.
- 보개는 관찰과 분석을 담당하고, 행동 주입은 `InputSnapshot` 경로를 따른다.

대표 pack 후보:

- `bogae_nurigym_step_tuple_view_v1`
- `bogae_nurigym_episode_replay_view_v1`

### 3.8 `std_bogae_seulgi_lab`

슬기를 만들고, 붙이고, 시험하고, 비교하는 전용 보기.

포함:

- `SeulgiPacket`
- `SeulgiIntent`
- 제안/거부/보류
- confidence
- 정책 비교
- 모델/규칙형/휴리스틱 비교
- 실패 사례 모음
- gatekeeper 판정

경계:

- raw prompt/response는 world truth가 아니다.
- world-affecting 슬기 제안은 반드시 `InputSnapshot` 또는 동등한 공식 입력 경로를 통과해야 한다.
- 슬기 보개는 AI 실험실이 될 수 있지만, AI가 state를 직접 바꾸는 API가 되어서는 안 된다.

대표 pack 후보:

- `bogae_seulgi_intent_review_v1`
- `bogae_seulgi_policy_compare_v1`
- `bogae_seulgi_gatekeeper_trace_v1`

### 3.9 `std_bogae_grid3d`

voxel, 3D gridworld, 3D 전술/퍼즐의 표준 보기.

포함:

- 3D 정수 격자
- voxel palette
- layer visibility
- cutaway/section
- camera preset
- height map
- 선택 voxel
- 경로/시야 표시

내림:

- console: slice/layer text
- web2d: isometric 또는 layer projection 가능
- engine3d: mesh/voxel scene payload

대표 pack 후보:

- `bogae_grid3d_voxel_slice_v1`
- `bogae_grid3d_engine_scene_payload_v1`

### 3.10 `std_bogae_game3d`

3D 게임 장면 어댑터용 보기. 단, full game engine이 아니라 world logic view다.

포함:

- actor transform
- camera hint
- animation state hint
- collision/debug overlay
- HUD
- quest/status view

경계:

- 렌더 품질, material, audio, networking, asset pipeline은 엔진/host 책임이다.
- DDN은 결정적 world logic, 입력 의미, replay 가능한 state transition을 맡는다.

대표 pack 후보:

- `bogae_game3d_actor_scene_view_v1`
- `bogae_game3d_hud_status_view_v1`

### 3.11 추가 표준 보개 후보

`grid2d/graph2d/table/timeline/sim2d`만으로 모든 보기 요구를 감당할 수는 없다. 아래 후보는 1차 구현 대상은 아니지만, 사용자가 `모양`으로 무리해서 만들 가능성이 높은 영역이므로 표준 보개 후보로 유지한다.

| 후보 | 필요 이유 | 우선도 |
|---|---|---|
| `std_bogae_network` | 노드/간선, 관계망, 상태머신, 의사결정 흐름 | P1 |
| `std_bogae_tree` | 문법트리, 증명트리, 선택지트리 | P1 |
| `std_bogae_matrix` | 행렬, tensor slice, confusion matrix, heatmap 확장 | P1 |
| `std_bogae_form_control` | 버튼, 슬라이더, 선택, 입력 패널 | P1 |
| `std_bogae_map` | 좌표 지도, 구역, 경로, 영역 강조 | P2 |
| `std_bogae_surface` | 3D surface, contour, height map | P2 |
| `std_bogae_profiler` | step time, action distribution, 성능/분포 | P2 |
| `std_bogae_debugger` | breakpoint, watch, state inspect | P2 |

이 후보들은 모두 언어 핵심 문법으로 넣지 않고, 표준팩 또는 제품팩으로 두는 것을 기본값으로 한다.

## 4. 제품선별 기본 묶음

| 제품선 | 기본 보개팩 |
|---|---|
| 셈그림 | `std_bogae_graph2d`, `std_bogae_sim2d`, `std_bogae_table`, `std_bogae_timeline` |
| 말힘누리/게임 | `std_bogae_grid2d`, `std_bogae_timeline`, `std_bogae_game3d`, `std_bogae_table` |
| 누리짐 | `std_bogae_grid2d`, `std_bogae_nurigym`, `std_bogae_timeline`, `std_bogae_table` |
| 슬기 실험실 | `std_bogae_seulgi_lab`, `std_bogae_table`, `std_bogae_timeline`, `std_bogae_graph2d` |
| 거울/재연 | `std_bogae_timeline`, `std_bogae_table`, `std_bogae_grid2d`, `std_bogae_sim2d` |

이 구조의 장점:

- 같은 누리가 보개 선택에 따라 게임, 교육툴, AI 실험실, replay debugger가 된다.
- 제품마다 새 언어를 만들 필요가 없다.
- 각 제품은 표준 보개팩 조합으로 차별화된다.

## 5. lowering 공통 계약

모든 표준 보개팩은 아래 순서로 내려간다.

```text
world/state snapshot
  + view request
  + view_meta
  -> standard bogae payload
  -> profile builder
  -> DrawList 또는 deterministic scene payload
  -> backend consumer
```

공통 MUST:

1. 같은 입력 snapshot + 같은 view_meta는 같은 payload를 만든다.
2. 같은 payload는 같은 DrawList 또는 scene payload를 만든다.
3. `state_hash`는 view-only 설정으로 변하지 않는다.
4. `bogae_hash`는 픽셀 결과가 아니라 deterministic payload/DrawList 기준으로 계산한다.
5. backend가 지원하지 않는 필수 family/profile은 조용히 무시하지 않고 deterministic FAIL 또는 DEGRADED PASS를 낸다.
6. world-affecting 입력은 `InputSnapshot`으로 들어간다.
7. view-only 입력은 cursor/zoom/pan/selection 같은 view_meta로 남는다.

## 6. 그래프가 어려운 이유와 해결

그래프는 `모양` 원자만으로 만들면 다음 요소를 매번 직접 짜야 한다.

- domain 산정
- scale 변환
- tick 산정
- label 배치
- legend 배치
- 다중 series 색/스타일
- 겹침 해소
- hover/cursor

따라서 `graph2d`는 반드시 표준 보개팩으로 제공해야 한다.

제안 GraphSpec:

```text
GraphSpec {
  kind: line | point | bar | histogram | heatmap
  domain_x: auto | fixed(min,max)
  domain_y: auto | fixed(min,max)
  scale_x: linear | log
  scale_y: linear | log
  series: [Series]
  axes: AxisSpec
  legend: none | top | right | bottom
  annotations: [Annotation]
}
```

auto 규칙:

- auto domain은 데이터 min/max에 fixed padding 비율을 적용한다.
- auto tick은 정해진 후보 집합에서만 고른다.
- label collision은 priority 순서로 숨기며, 측정 환경에 따라 바뀌면 안 된다.

## 6.1 시뮬레이션 보개가 미리 제공해야 하는 것

시뮬레이션에서도 같은 원칙을 적용한다. 사용자가 직접 만들어야 하는 것은 그 시뮬레이션만의 특별한 생김새, 도메인 아이콘, 교육용 강조, 특수 센서 표시 정도여야 한다.

표준 `sim2d/grid2d/timeline/table` 보개가 기본 제공해야 하는 것:

- 좌표계
- 축
- 격자
- 카메라
- 확대/축소
- 물체 궤적
- 속도/힘 벡터
- 충돌 영역 표시
- 시간 조절
- 수치 패널
- 상태표
- 마디/재연 타임라인
- 입력 이벤트 표시
- state diff

경계:

- `누리`는 세계와 변화 규칙을 만든다.
- `보개`는 누리 상태를 사람이 이해하고 조작할 수 있는 보기로 투영한다.
- `커스텀 모양`은 이 시뮬레이션만의 얼굴을 만드는 용도다.

## 7. 단계 제안

### Phase 0: 문서 고정

- 이 제안을 관리자 제출용 PROPOSAL로 둔다.
- 기존 backend/profile split과 충돌 여부를 감사한다.
- SSOT 변경이 필요하면 별도 OI로 올린다.

DoD:

- 표준 보개팩 목록
- lowering 공통 계약
- graph2d 최소 계약
- state/view/input 경계

### Phase 1: 최소 표준팩 4종

우선순위:

1. `std_bogae_grid2d`
2. `std_bogae_graph2d`
3. `std_bogae_table`
4. `std_bogae_timeline`

이유:

- 셈그림과 게임 MVP 양쪽에 즉시 필요하다.
- console/web parity를 함께 검증할 수 있다.
- 그래프 직접 조립 문제를 가장 빨리 줄인다.

### Phase 2: AI/Gym 보기

추가:

- `std_bogae_nurigym`
- `std_bogae_seulgi_lab`

이유:

- 슬기와 누리짐은 별도 제품선 가치가 크다.
- AI가 state를 직접 바꾸지 않는 경계를 눈으로 확인할 수 있다.

### Phase 3: 3D 보기

추가:

- `std_bogae_grid3d`
- `std_bogae_game3d`

이유:

- 3D는 엔진 의존성이 크므로 core contract를 먼저 닫은 뒤 adapter로 간다.

## 8. 지시문 후보

다음 핸드오프 지시문으로 추가할 수 있다.

> 지시문 8 - 보개 표준팩/lowering 계약 설계
>
> `console_headless/web2d/engine3d` 백엔드 축과 `grid2d/sim2d/graph2d/grid3d/game3d` 프로필 축을 유지한 채, `std_bogae_grid2d`, `std_bogae_graph2d`, `std_bogae_table`, `std_bogae_timeline`을 1차 표준팩으로 설계한다. 각 표준팩은 의미 payload, lowering 규칙, backend capability gate, state_hash/view_meta/InputSnapshot 경계를 표로 가진다. parser/runtime 변경 없이 PROPOSAL과 pack 후보 목록까지만 산출한다.

DoD:

- 표준 보개팩 1차 목록
- 각 보개팩의 payload 초안
- graph2d lowering 규칙
- pack 후보 ID
- SSOT/OI 후보 목록
- parser/runtime 변경 0건
- `docs/ssot/**` 수정 0건

## 9. 열린 질문

1. `std_bogae_graph2d`의 정본 이름을 `그래프보개`로 노출할지, `보개.graph2d` 같은 profile 이름으로 노출할지 결정이 필요하다.
2. `std_bogae_table`을 보개 family로 볼지, `text/structure`의 하위로 볼지 결정이 필요하다.
3. `std_bogae_seulgi_lab`에서 raw model response 보관 범위와 개인정보/재현성 경계가 필요하다.
4. `std_bogae_game3d`가 engine scene payload까지 정의할지, 최소 actor/view hint까지만 정의할지 결정이 필요하다.
5. `graph2d` auto tick 알고리즘을 pack으로 고정할지, 구현 helper로 먼저 고정할지 결정이 필요하다.

## 10. 권고 결론

보개는 `모양`만으로 충분하다고 보면 안 된다. `모양`은 최종 draw 원자이고, 실제 사용자는 표준 보개팩을 통해 의미 단위로 보기와 조작을 만들어야 한다.

권고:

1. `grid2d`, `graph2d`, `table`, `timeline`을 1차 표준 보개팩으로 닫는다.
2. `nurigym`, `seulgi_lab`을 2차 표준 보개팩으로 둔다.
3. `grid3d`, `game3d`는 engine adapter와 함께 3차로 둔다.
4. 그래프는 반드시 `graph2d` 표준팩으로 제공한다.
5. 모든 보개팩은 `state_hash`와 `InputSnapshot` 경계를 명확히 가진다.
6. `모양` 직접 사용이 반복되는 영역은 표준 보개팩 후보로 승격한다.
7. 시뮬레이션은 표준 보개가 좌표계/축/카메라/궤적/벡터/타임라인을 제공하고, 사용자는 특수한 도메인 표현만 커스텀하는 구조로 둔다.
