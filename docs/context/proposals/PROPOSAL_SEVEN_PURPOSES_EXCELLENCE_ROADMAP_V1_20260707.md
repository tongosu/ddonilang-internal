# PROPOSAL_SEVEN_PURPOSES_EXCELLENCE_ROADMAP_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul)
- 분류: PROPOSAL / PRODUCT_STRATEGY / EXCELLENCE_ROADMAP
- 상태: 관리자 제출용 제안
- 기준: SSOT v24.12.9 읽기 전용 참조 + 2026-07-07 설정/보개/누리 심화 논의
- 변경 방식: `docs/ssot/**` 직접 수정 없음, parser/runtime 변경 없음, closure 주장 없음

## 0. 목적

이 문서는 일곱 목적을 모두 "조건부 충분" 또는 "미달"이 아니라 **훌륭**이라고 말할 수 있게 만들기 위해 필요한 추가 설계와 앞으로 할 일을 정리한다.

일곱 목적:

1. AI Gym
2. 한국어 Manim
3. 게임 엔진
4. 교육
5. 선언적 시뮬레이션
6. 한국어·교착어권 개발
7. AI 친화성

## 1. "훌륭" 판정 기준

어떤 목적이 훌륭하다고 말하려면 최소 네 조건이 필요하다.

| 기준 | 의미 |
|---|---|
| 설계 | 목적을 감당하는 개념/경계/계약이 충돌 없이 존재 |
| 구현 | 최소 제품 경로가 실제 코드로 작동 |
| 증빙 | pack/golden/CI/perf/브라우저 smoke가 있음 |
| 실증 | 외부 사용자 또는 실제 workflow로 확인됨 |

따라서 "훌륭"은 단순히 설계가 좋은 상태가 아니다. 적어도 하나의 대표 workflow가 끝까지 돌아야 한다.

공통 병목:

1. WASM/브라우저 전달
2. 성능 증빙
3. 외부 실증
4. 표준 보개팩
5. 진단 품질
6. pack evidence

## 2. 전체 판정표

| 목적 | 현재 판정 | 훌륭으로 바뀌는 조건 |
|---|---|---|
| AI Gym | 조건부 충분 | vectorized rollout + consumer parity + step_record 강화 + perf table |
| 한국어 Manim | 미달 | scene/timeline DSL + 수식 애니 + mp4/web export + 한국어 장면 튜토리얼 |
| 게임 엔진 | 조건부 충분 | 턴제 vertical slice + 저장/이어하기 + 입력 pacing + engine adapter smoke |
| 교육 | 설계 충분, 전달 미달 | WASM 배포 + 초심자 진단 + 1개 교실형 lesson path 실증 |
| 선언적 시뮬레이션 | 물리 충분 경로, 경제/수학 조건부 | 적분기 + model-first 경제 + exact/proof 최소 closure |
| 한국어·교착어권 개발 | 한국어 충분 경로, 교착어권 조건부 | native review + dialect pack equivalence + 국제 튜토리얼 |
| AI 친화성 | 구조 충분, 도구/코퍼스 미달 | LSP minimum + AI corpus + 슬기 표면 승격 + benchmark harness |

## 3. AI Gym을 훌륭으로 만들기

### 3.1 추가 설계

- `nurigym.vector_env.v0.1`: 여러 env를 같은 seed family 아래에서 병렬 rollout하는 스키마
- `step_record.v0.2`: raw action, canonical action, merged action, action_status, provenance, reward breakdown 기록
- `observation_space/action_space` manifest: Gymnasium 호환 최소 필드
- `settings_run_config_hash`를 dataset header에 포함
- `시앗묶음`을 RL stream isolation에 연결
- `관찰범위`를 partial observation 계약으로 승격

### 3.2 앞으로 할 일

1. `wasm`, `wasmtime-py`, `PyO3` consumer parity를 같은 fixture로 비교한다.
2. vectorized rollout 최소 구현을 만든다.
3. 16/64/256 env 처리량 benchmark를 기록한다.
4. `reset(seed, options)`, `step`, `terminated/truncated`, `info` golden을 고정한다.
5. 작은 RL 예제 2개를 끝까지 돌린다: gridworld, cartpole류.

### 3.3 훌륭 판정 DoD

- `nurigym_vector_env_smoke_v1` PASS
- dual/tri consumer parity PASS
- perf report: env/s, p50/p95 step time
- sample training loop 1개 완료
- replay mismatch 0건

## 4. 한국어 Manim을 훌륭으로 만들기

### 4.1 추가 설계

- `보개마당`을 scene/timeline DSL로 명확화
- `std_bogae_timeline`과 `scene_track` 연결
- `수식객체` / `수식변형` / `강조` / `자막` / `해설` 기본 표면
- deterministic scene payload: `seamgrim.scene.v0` 또는 후속 schema
- export target: web replay, png sequence, mp4
- 카메라/전환/레이어는 view-only로 유지

### 4.2 앞으로 할 일

1. 수식 하나가 변형되는 최소 장면을 만든다.
2. 축/그래프 위에 설명 자막이 붙는 장면을 만든다.
3. timeline scrub과 frame export를 만든다.
4. mp4 export는 host/toolchain 기능으로 연결한다.
5. 한국어 튜토리얼 3개를 만든다: 수식 변형, 그래프 설명, 물리 시뮬 해설.

### 4.3 훌륭 판정 DoD

- `manim_ko_formula_transform_v1` PASS
- `manim_ko_graph_explain_v1` PASS
- web timeline 재생 PASS
- frame export deterministic hash PASS
- mp4 export smoke PASS

## 5. 게임 엔진 역할을 훌륭으로 만들기

### 5.1 추가 설계

- 범위 명시: full engine이 아니라 deterministic world logic kernel + adapter
- `판/마당` lifecycle 확정
- 저장/이어하기 save schema
- `std_bogae_grid2d`와 `std_input_map` 결합
- 턴제/격자 game preset
- realtime action은 별도 performance tier로 분리
- engine adapter contract: Godot 또는 web2d 우선

### 5.2 앞으로 할 일

1. 턴제 격자 게임 vertical slice를 끝까지 만든다.
2. 저장/이어하기를 구현한다.
3. replay와 save/load가 같은 state_hash로 수렴하는지 검증한다.
4. web2d 또는 Godot adapter smoke를 만든다.
5. realtime 60fps 주장은 별도 benchmark 전까지 보류한다.

### 5.3 훌륭 판정 DoD

- `game_grid_turn_vertical_slice_v1` PASS
- save/load/replay parity PASS
- input pacing smoke PASS
- adapter smoke PASS
- 10분 플레이 가능한 demo 1개

## 6. 교육을 훌륭으로 만들기

### 6.1 추가 설계

- 초심자 노출층: L1 preset + 최소 문장 + 좋은 오류 메시지
- `std_bogae_graph2d`, `std_bogae_sim2d`, `std_bogae_table`, `std_bogae_timeline` 기본 장착
- 진단 메시지 rubric: 원인, 위치, 고치는 문장, 예시
- 브라우저 전달 경로: WASM build, sample loader, lesson runner
- 교실 실증 기록 형식

### 6.2 앞으로 할 일

1. WASM 배포 블로커를 닫는다.
2. 물리 lesson 3개를 브라우저에서 바로 열리게 한다.
3. 초심자 오류 메시지 20개를 고친다.
4. 교사용 운영 노트를 만든다.
5. 외부 사용자 3명 이상에게 실행을 맡기고 실패 로그를 모은다.

### 6.3 훌륭 판정 DoD

- browser lesson open/run PASS
- beginner diagnostics pack PASS
- 3개 lesson vertical slice 완료
- 외부 사용자 실증 기록 1회 이상
- "설치 없이 첫 실행" 성공

## 7. 선언적 시뮬레이션을 훌륭으로 만들기

### 7.1 물리

추가 설계:

- 최소 적분기 집합: Euler, semi-implicit Euler, RK4 후보
- `계산단위계`와 `표시단위계` 분리
- stiff system 한계 명시
- `std_bogae_sim2d` vector/trace 기본 제공

할 일:

- 진자, 포사체, 감쇠진동, RC 충전 lesson을 pack으로 닫는다.
- 적분기별 결과 차이를 보여주는 lesson을 만든다.
- Fixed64 한계와 권장 dt를 문서화한다.

훌륭 DoD:

- `sim_physics_integrator_min_v1` PASS
- `sim_physics_units_v1` PASS
- 4개 물리 lesson browser PASS

### 7.2 경제

추가 설계:

- agent-first와 model-first를 모두 지원
- `시앗묶음` 기반 확률 실험 재현
- 경제 표준 보개: 흐름, 관계망, 분포, 균형 수렴
- `std_bogae_network`, `std_bogae_graph2d`, `std_bogae_table` 결합

할 일:

- 수요/공급 균형 model-first 예제를 만든다.
- agent market 실험을 seed stream으로 재현한다.
- 정책 shock 비교 lesson을 만든다.

훌륭 DoD:

- `econ_model_first_equilibrium_v1` PASS
- `econ_agent_seed_stream_compare_v1` PASS
- graph/table/network view PASS

### 7.3 수학

추가 설계:

- exact family 최소 closure: 큰바른수/나눔수/곱수 중 우선 범위 확정
- 방정식/관계/반례찾기 최소 surface
- proof는 교육용 설명층과 엄밀 proof layer를 분리
- `std_bogae_graph2d`와 symbolic step view 결합

할 일:

- 유리수 exact 계산 pack을 닫는다.
- 방정식 풀이 최소 예제를 만든다.
- 반례찾기/검산 lesson을 만든다.

훌륭 DoD:

- `math_exact_rational_min_v1` PASS
- `math_equation_solve_min_v1` PASS
- `math_counterexample_check_v1` PASS

## 8. 한국어·교착어권 개발을 훌륭으로 만들기

### 8.1 추가 설계

- 한국어 정본과 `ko-common` 완충을 분리
- dialect pack equivalence 기준
- native review workflow
- T1/T2 승격 조건
- 조사/격표지/SOV/교착 morphology mapping note
- 용어 인증과 registry를 분리

### 8.2 앞으로 할 일

1. 한국어 외 T1 언어 3개를 우선 고른다: ja, mn, tr 권고.
2. 각 언어 native reviewer 1명 이상을 붙인다.
3. 같은 pack을 한국어와 해당 표면으로 실행해 equivalence를 확인한다.
4. 잘못된 자연스러움보다 semantic fidelity를 우선하는 리뷰 rubric을 만든다.
5. ko-common 튜토리얼을 만든다.

### 8.3 훌륭 판정 DoD

- `dialect_ko_common_equiv_v1` PASS
- T1 언어 3개 native review 완료
- dialect pack equivalence PASS
- 비한국어 사용자 1명 이상 실증

## 9. AI 친화성을 훌륭으로 만들기

### 9.1 AI가 개발하기 쉬운 언어

추가 설계:

- LSP minimum: parse diagnostics, symbol index, hover, go-to definition
- canonicalizer API
- AI prompt corpus: good/bad examples
- grammar capability manifest와 pack evidence 연결

할 일:

- LSP minimum을 만든다.
- AI가 DDN을 생성하고 check/run하는 evaluation set을 만든다.
- lint fix suggestion을 만든다.

DoD:

- `lsp_min_parse_diag_v1` PASS
- `ai_ddn_generation_eval_v1` PASS
- generated sample pack pass rate 기록

### 9.2 AI를 평가하기

추가 설계:

- NuriGym benchmark suite
- metrics_report schema
- seed stream isolation
- partial observation

할 일:

- baseline agents 3종을 만든다: random, rule, simple learned.
- reproducible benchmark leaderboard를 만든다.

DoD:

- `nurigym_benchmark_suite_min_v1` PASS
- baseline score reproducibility PASS

### 9.3 AI를 사용하기

추가 설계:

- `설정.슬기` docs-first 키 통일
- `SeulgiIntent` payload review view
- `std_bogae_seulgi_lab`
- Gatekeeper trace
- stale intent handling

할 일:

- 슬기 제안 review UI를 만든다.
- policy compare pack을 만든다.
- gatekeeper reject/accept trace를 보개로 보여준다.

DoD:

- `seulgi_intent_review_v1` PASS
- `seulgi_gatekeeper_trace_v1` PASS
- replay without AI PASS

### 9.4 자연어 병용

판정:

- 자연어 직접 실행은 열지 않는다.
- 자연어는 proposal/choice/input 후보를 만들고, world-affecting 변화는 항상 `InputSnapshot` 경유.

DoD:

- `natural_language_proposal_not_execute_v1` PASS
- confirmation -> InputSnapshot boundary PASS

## 10. 공통 기반 작업

모든 목적을 훌륭으로 끌어올리는 공통 작업:

1. WASM/browser delivery closure
2. 표준 보개팩 1차: grid2d, graph2d, table, timeline, sim2d
3. 설정 hash 4분할
4. 시앗묶음
5. beginner diagnostics
6. perf benchmark framework
7. external validation log template
8. pack evidence dashboard

## 11. 권장 순서

### Phase 1: 가장 가까운 훌륭 2개

1. 교육 browser vertical slice
2. 물리 시뮬레이션 vertical slice

이 두 개가 끝나면 보개, WASM, 진단, lesson, pack, replay가 함께 개선된다.

### Phase 2: AI Gym + 턴제 게임

1. vectorized NuriGym
2. turn/grid game vertical slice
3. save/load/replay

### Phase 3: AI 친화성 + 경제

1. LSP minimum
2. Seulgi lab
3. econ model-first + agent seed streams

### Phase 4: 교착어권 + 한국어 Manim

1. native review/dialect equivalence
2. scene/timeline/export stack

## 12. 한 줄 결론

일곱 목적은 구조적으로 충돌하지 않는다. 그러나 모두 훌륭해지려면 새 목적을 더 늘리기보다, 공통 병목인 WASM 전달, 표준 보개팩, 설정 hash, seed stream, 성능 증빙, 외부 실증을 먼저 닫아야 한다.
