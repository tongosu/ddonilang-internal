# SSOT_PATCH_DRAFT_20260706_BUNDLE

- 작성: 2026-07-07 KST, Codex
- 성격: SSOT 병합 준비 초안. 이 문서는 `docs/ssot/**`를 직접 수정하지 않는다.
- 경계: 결정 후보, 후보, 질문을 분리한다. 후보를 이미 결정된 정본처럼 쓰지 않는다.
- 기준 입력: 2026-07-06 논의 산출물 8건과 `docs/ssot/ssot/*_v24.12.9.md`.

## 대상 산출물 8건

| # | 산출물 | 이번 초안에서의 역할 |
|---:|---|---|
| 1 | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md` | 지시문 1~16 경계, DoD, 금지선의 원본 |
| 2 | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md` | 보개 표준팩/lowering 후보 |
| 3 | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md` | 누리 시간/마디/태스크 경합 후보 |
| 4 | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md` | 큰마디 위상표, 쓰기 경합, reset 재적용 질문 |
| 5 | `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md` | 설정 하위 절 최대 키 지도 후보 |
| 6 | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md` | 7목적 G1/G2/G3 및 즉시 실행 후보 |
| 7 | `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md` | AI 닫힌 베타 Round 0 운영 후보 |
| 8 | `docs/context/notes/IDEAS_DDONIRANG_ENRICHMENT_V1_20260706.md` | 발표 전 예약어/문법 공간 선점 후보 |

## 결정 후보

아래 문장은 SSOT 오너가 반영할 수 있도록 "어느 파일, 어느 절, 어떤 문장" 형태로 쓴 초안이다.

| 등급 | 대상 SSOT 파일 / 절 | 추가 또는 수정 문장 초안 | 근거 |
|---|---|---|---|
| 결정 후보 | `SSOT_MASTER_v24.12.9.md` / `이번 스냅샷 요지 (v23.0.6)` | `설정 {}` 하위 절 8종(`문서/실행/이야기/누리/샘/거울/보개/슬기`)은 canonical shell로 유지하되, 각 절의 key set은 key 단위 evidence tier(`정본/후보/질문`)를 별도로 가진다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:242`, `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:78` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `v20.26.0 추가 경계` | `설정 {}` 자체는 직접 `state_hash` 입력으로 직렬화하지 않지만, `시앗/마디수/들머리/공간갈래`처럼 실행 결과 상태에 간접 영향을 줄 수 있는 key는 결과영향 키 분류표에서 별도 추적한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:172`, `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:80` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `§P0A 시간 / lifecycle / reset contract` | `마디수`는 실행 길이 선택 key 후보이며, 정본 위치 후보는 `설정.실행.마디수`다. flat `설정 { 마디수: ... }` 입력은 compat+lint 또는 즉시 비허용 중 하나를 SSOT 오너가 선택해야 한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:39` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `§P0B 다중 에이전트 시간 코어` | 실행 위상 후보는 `마디 열기 -> 입력 봉인 -> 전처리/제안 -> action 파이프라인 -> 매마디/세움/흐름씨 -> 훅 -> 보람/판끝 -> 거울 기록 -> 보개 방출` 순서를 기준 초안으로 검토한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:30` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `§P0B.3 completion / noop` 및 `§P0B.3A filter-before-merge canonical boundary` | `합치기갈래` 신설보다 기존 `행동모음갈래` 값 확장을 우선 검토한다. 후보 값은 `차례모음/보탬모음/앞선모음/다수결모음/자리모음`이며, `거부`는 merge 후보에서 제외한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:130`, `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:180` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `§P21 슬기 v1` | 슬기 지연은 `accepted_madi/target_madi` export metadata로 드러낼 수 있으나, 실행 적용 순서는 계속 `(agent_id, recv_seq)`가 정본이다. `accepted_madi/target_madi`는 실행 정렬 key가 아니다. | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:196`, `docs/ssot/ssot/SSOT_PLATFORM_v24.12.9.md:1825` |
| 결정 후보 | `SSOT_MASTER_v24.12.9.md` / `보개 백엔드/프로필 분리` | 보개 표준팩은 언어 코어 문법이 아니라 표준팩/product pack 계층으로 둔다. 1차 후보는 `std_bogae_grid2d`, `std_bogae_graph2d`, `std_bogae_table`, `std_bogae_timeline`이다. | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:476`, `docs/ssot/ssot/SSOT_MASTER_v24.12.9.md:752` |
| 결정 후보 | `SSOT_PLATFORM_v24.12.9.md` / `보개 보기 의미 / 보기 조립 / 입력 경계` | graph2d lowering은 axis/tick/label/series/legend/label-collision/auto-tick deterministic policy를 표준 보개팩 계약으로 다루며, 사용자가 그래프를 `모양` 원자만으로 직접 조립하도록 요구하지 않는다. | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:119` |
| 결정 후보 | `SSOT_TOOLCHAIN_v24.12.9.md` / `v24.6.0 immediate_dev_track cluster` | 성능 기준선은 `perf_baseline_v1`로 별도 관리하고, consumer path별 수치를 단순 동일 기준으로 비교하지 않는다. 기준선 고정 전에는 성능 충분 주장을 하지 않는다. | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:25`, `docs/ssot/ssot/SSOT_TOOLCHAIN_v24.12.9.md:204` |
| 결정 후보 | `SSOT_TOOLCHAIN_v24.12.9.md` / `v24.12.9 toolchain additions` | AI 닫힌 베타는 `BETA_USER_BUNDLE`만 제공하는 지식 격리 방식으로 수행하고, 저장소 전체 지식을 가진 세션은 베타 사용자 실행자가 될 수 없다. | `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md:22` |

## 후보

| 후보 | 대상 SSOT 파일 / 절 | 문장 초안 | 근거 |
|---|---|---|---|
| `설정.누리` key set | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `설정.누리` v1 key 후보는 `시앗`, `누리갈래`, `환경ID`, `공간갈래`, `첫상태참조`, `규칙묶음`으로 시작하되, `누리갈래`와 `차림새` 축 중복은 질문으로 남긴다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:52`, `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:82` |
| `설정.이야기` key set | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `설정.이야기` v1 key 후보는 `들머리`를 시작점으로 둔다. `들머리`가 결과영향 키인지 순수 메타인지 별도 판정한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:56` |
| `설정.슬기` key drift | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `두뇌종류/두뇌/끼우개/정책` 예시 drift는 정본 승격 전 통일안이 필요하다. 권고 후보는 `두뇌` 단일화 또는 `두뇌 { 갈래/끼우개/정책 }` 계층화다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:69` |
| `설정해시` | `SSOT_TOOLCHAIN_v24.12.9.md` / support/tooling cluster | `설정해시`는 SSOT 병합 전까지 독립 checker 프로토타입으로만 다루며, runtime record schema나 `state_hash` 산식에 넣지 않는다. | `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:37`, `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:294` |
| `시앗묶음` | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `시앗묶음`은 이름 있는 deterministic seed stream 후보이며, 도메인 이름 충돌과 root seed 공유 하위 호환 규칙을 annex에서 확정해야 한다. | `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:46` |
| 누리짐 step record v0.2 | `SSOT_OPEN_ISSUES_v24.12.9.md` / `OI-NURIGYM-PYTHON-CONSUMER-01` 인접 | `nurigym.step_record.v0.2`는 `raw_action/normalized_action/action_status/merged_action/applied_action`을 add-only 필드 후보로 둔다. v0.1 reader 호환 규칙이 필요하다. | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:47` |
| 진단 3층 | `SSOT_TOOLCHAIN_v24.12.9.md` / toolchain additions | 대표 `E_*` 진단은 `무엇/어디서/어떻게` 3층 품질 기준으로 감사하고, 문구 변경은 SSOT 오너 승인 후 진행한다. | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:96` |
| LLM 코퍼스 | `SSOT_TOOLCHAIN_v24.12.9.md` / toolchain additions | `out/llm_corpus_v1.jsonl`은 기존 pack/golden/grammar manifest에서 결정적으로 추출하는 AI 지원 산출물이며, 생성형 요약이나 SSOT 대체물이 아니다. | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:138` |
| IDEAS 예약어 | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `가설`, `검산`, `단위 정의`, `말거리`, `~이름(...)` 분포 표기는 채택 여부와 별개로 발표 전 reserved/proposal 선점 검토가 필요하다. | `docs/context/notes/IDEAS_DDONIRANG_ENRICHMENT_V1_20260706.md:67` |

## 질문

| 질문 ID | 질문 | 대상 SSOT 위치 후보 | 근거 |
|---|---|---|---|
| OQ-1 | 임자 실행 순서를 파일 선언 순서로 볼지, `agent_id` 사전순으로 볼지 결정 필요. | `SSOT_PLATFORM_v24.12.9.md` / `§P0B` | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:59` |
| OQ-2 | 세움과 매마디 상호 갱신을 fixpoint 없이 1회 평가로 제한하고 순환 의존을 오류로 볼지 결정 필요. | `SSOT_PLATFORM_v24.12.9.md` / `§P0B` | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:60` |
| OQ-3 | 큰마디 P2 전처리를 샘 소속으로 볼지 이야기 소속으로 볼지 결정 필요. | `SSOT_PLATFORM_v24.12.9.md` / `§P0B` | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:61` |
| OQ-4 | `(N마디)마다` 판정 시점을 P3 내부 어디로 둘지 결정 필요. | `SSOT_PLATFORM_v24.12.9.md` / `§P0B` | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:62` |
| OQ-R1 | `누리다시`가 `설정.누리`만 재읽는지, `설정.실행`까지 재읽는지 결정 필요. | `SSOT_PLATFORM_v24.12.9.md` / `§P0A.3 reset kind 5종` | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:123` |
| OQ-SEULGI-LATENCY | `지연마디` 소유권을 `설정.슬기`, `설정.샘`, `설정.실행` 중 어디에 둘지 결정 필요. | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:224` |
| OQ-BOGAE-NAME | `std_bogae_graph2d` 노출 이름을 `그래프보개`로 할지 profile 이름으로 할지 결정 필요. | `SSOT_OPEN_ISSUES_v24.12.9.md` / 신규 OI | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:530` |

## pack 후보 ID 충돌 검사

실측 기준: 기존 `pack/` 디렉터리 1038개와 후보 ID 53개를 디렉터리명으로 대조했다. `YES`는 이미 같은 이름의 `pack/<id>/`가 존재한다는 뜻이며 삭제/수정은 하지 않았다.

| # | 후보 ID | 기존 pack 충돌 | 근거 | 비고 |
|---:|---|---|---|---|
| 1 | `bogae_std_grid2d_matrix_palette_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:115` | 보개 표준팩 후보 |
| 2 | `bogae_grid2d_console_web_parity_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:116` | 보개 표준팩 후보 |
| 3 | `bogae_grid2d_path_highlight_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:117` | 보개 표준팩 후보 |
| 4 | `bogae_graph2d_axis_tick_determinism_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:156` | 보개 표준팩 후보 |
| 5 | `bogae_graph2d_series_lowering_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:157` | 보개 표준팩 후보 |
| 6 | `bogae_graph2d_label_overlap_policy_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:158` | 보개 표준팩 후보 |
| 7 | `bogae_table_state_snapshot_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:182` | 보개 표준팩 후보 |
| 8 | `bogae_table_diff_highlight_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:183` | 보개 표준팩 후보 |
| 9 | `bogae_sim2d_vector_trace_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:207` | 보개 표준팩 후보 |
| 10 | `bogae_sim2d_sensor_overlay_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:208` | 보개 표준팩 후보 |
| 11 | `bogae_timeline_madi_episode_trace_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:231` | 보개 표준팩 후보 |
| 12 | `bogae_timeline_state_hash_diff_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:232` | 보개 표준팩 후보 |
| 13 | `bogae_nurigym_step_tuple_view_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:257` | 보개 표준팩 후보 |
| 14 | `bogae_nurigym_episode_replay_view_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:258` | 보개 표준팩 후보 |
| 15 | `bogae_seulgi_intent_review_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:283` | 보개 표준팩 후보 |
| 16 | `bogae_seulgi_policy_compare_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:284` | 보개 표준팩 후보 |
| 17 | `bogae_seulgi_gatekeeper_trace_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:285` | 보개 표준팩 후보 |
| 18 | `bogae_grid3d_voxel_slice_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:310` | 보개 표준팩 후보 |
| 19 | `bogae_grid3d_engine_scene_payload_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:311` | 보개 표준팩 후보 |
| 20 | `bogae_game3d_actor_scene_view_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:333` | 보개 표준팩 후보 |
| 21 | `bogae_game3d_hud_status_view_v1` | NO | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:334` | 보개 표준팩 후보 |
| 22 | `nuri_madi_big_small_boundary_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:432` | 누리 마디/태스크 후보 |
| 23 | `nuri_madi_completion_all_required_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:433` | 누리 마디/태스크 후보 |
| 24 | `nuri_madi_completion_fill_noop_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:434` | 누리 마디/태스크 후보 |
| 25 | `nuri_task_action_status_pipeline_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:435` | 누리 마디/태스크 후보 |
| 26 | `nuri_task_merge_priority_tiebreak_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:436` | 누리 마디/태스크 후보 |
| 27 | `nuri_seulgi_latency_target_madi_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:437` | 누리 마디/태스크 후보 |
| 28 | `nuri_inputsnapshot_ordering_recv_seq_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:438` | 누리 마디/태스크 후보 |
| 29 | `nuri_default_execution_profile_matrix_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:439` | 누리 마디/태스크 후보 |
| 30 | `nuri_advanced_option_risk_matrix_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:440` | 누리 마디/태스크 후보 |
| 31 | `nuri_madi_phase_order_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:151` | 누리 위상/경합 심화 후보 |
| 32 | `nuri_hook_notification_next_madi_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:152` | 누리 위상/경합 심화 후보 |
| 33 | `nuri_state_write_conflict_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:153` | 누리 위상/경합 심화 후보 |
| 34 | `nuri_submadi_snapshot_isolation_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:154` | 누리 위상/경합 심화 후보 |
| 35 | `nuri_reset_settings_reapply_matrix_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:155` | 누리 위상/경합 심화 후보 |
| 36 | `nuri_seum_maemadi_order_v1` | NO | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:156` | 누리 위상/경합 심화 후보 |
| 37 | `perf_baseline_v1` | YES | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:27` | 이미 `pack/perf_baseline_v1/` 존재 |
| 38 | `gym_reset_seed_implies_complete_episode_reset_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:47` | 7목적 후보 |
| 39 | `resident_reset_episode_equiv_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:47` | 7목적 후보 |
| 40 | `nurigym_step_record_v02_roundtrip_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:47` | 7목적 후보 |
| 41 | `nurigym_vector_env_determinism_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:52` | 7목적 후보 |
| 42 | `bogae_madang_track_v1_schema_smoke` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:70` | 7목적 후보 |
| 43 | `lifecycle_pan_basic_start_end_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:83` | 7목적 후보 |
| 44 | `save_vs_replay_artifact_split_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:83` | 7목적 후보 |
| 45 | `diag_three_layer_message_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:99` | 7목적 후보 |
| 46 | `dialect_equiv_ja_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:129` | 7목적 후보 |
| 47 | `llm_corpus_v1` | NO | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:139` | output artifact 후보 |
| 48 | `llm_corpus_extract_deterministic_v1` | YES | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:141` | 이미 `pack/llm_corpus_extract_deterministic_v1/` 존재 |
| 49 | `ai_det_tier_capability_matrix_v1` | YES | `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md:143` | 이미 `pack/ai_det_tier_capability_matrix_v1/` 존재 |
| 50 | `stdlib_l1_integrators_v1` | YES | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:218` | 이미 `pack/stdlib_l1_integrators_v1/` 존재 |
| 51 | `econ_model_supply_demand_equilibrium_v1` | NO | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:219` | 경제 model-first 후보 |
| 52 | `econ_model_money_supply_v1` | NO | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:219` | 경제 model-first 후보 |
| 53 | `econ_model_tax_welfare_v1` | NO | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:219` | 경제 model-first 후보 |

충돌 요약: 53개 후보 중 기존 pack 디렉터리 충돌 4건(`perf_baseline_v1`, `llm_corpus_extract_deterministic_v1`, `ai_det_tier_capability_matrix_v1`, `stdlib_l1_integrators_v1`). 이 4건은 새로 만들 후보가 아니라 기존 pack 보강/후속 검증 대상으로 읽어야 한다.

## 적용 순서 제안

1. `docs/context/proposals/OI_CANDIDATE_BUNDLE_20260706.md`의 OI 후보를 SSOT 오너가 선별한다.
2. 결정 후보 중 `state_hash` 산식/record schema에 닿는 항목은 문장만 반영하고 구현은 Tier B 해금 전까지 금지한다.
3. pack 후보 충돌 4건은 기존 pack 보강 항목으로 재분류한다.
4. 예약어/문법 공간 선점은 `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md` 결과를 먼저 검토한다.
