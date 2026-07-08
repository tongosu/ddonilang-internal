# PRE_RELEASE_FREEZE_SWEEP_V1

- 작성: 2026-07-08 (Asia/Seoul)
- 성격: 발표 전 동결 스윕 1차 감사
- 기준: SSOT v24.12.9-candidate read-only + 2026-07-06~07 proposal bundle
- 범위: 예약어 후보, 문법 공간, `E_*` 오류 코드, schema version 흔적, pack 후보 ID 중복
- 비범위: parser acceptance 전수 테스트, SSOT 본문 수정, runtime 구현 claim

## 0. 결론

발표 전 동결 관점에서 가장 큰 위험은 기능 부족이 아니라 "나중에 추가하기 어려운 이름과 기록 계약"이다.

1. 새 후보 표면 26개 중 23개는 SSOT 본문에서 아직 발견되지 않았다. 예약어/문법 공간 선점 검토가 필요하다.
2. `#` 계열은 이미 많이 쓰이고, `~` 계열은 거의 비어 있다. `~이름(...)` 또는 `~분포(...)` 계열은 지금 조용히 식별자로 열어두면 나중에 확률/분포 표기로 쓰기 어렵다.
3. 제품 경로에서 `E_*` 토큰은 초기 넓은 스윕 기준 3,805개, DAYRUN 재현 스윕 기준 unique 3,749개가 잡혔다. namespace 문서와 대표 오류별 진단 golden이 필요하다.
4. `schema_version` 흔적은 200줄이 잡혔다. 일부는 `v0/v1/v2` 혼재이고, 공개 schema의 버전 협상 규칙은 schema별로 통일되어 있지 않다.
5. pack 후보 ID는 초기 부분 스윕 39개 중 충돌 2개였고, SSOT patch bundle 최종 표에서는 53개 중 충돌 4개다. 충돌은 대체로 이번 세션 또는 기존 감사 pack이 이미 점유한 이름이다.

## 1. 실행한 정적 스윕

실측은 다음 성격의 검색으로 수행했다.

- 예약어 후보: `docs/ssot`, `docs/context/proposals`, `docs/context/notes`, `docs/reports`, `pack`, `tests`, `tools`, `또니랑`
- 문법 공간 후보: `#`, `@`, `~` 관련 고정 문자열과 parser/error token
- 오류 코드: `core`, `lang`, `tool`, `tools`, `tests`, `pack`의 `E_[A-Z][A-Z0-9_]+`
- schema version: `schema_version` 고정 문자열
- pack ID: 후보 ID와 `pack/<id>` 존재 여부

주의: 이 보고서는 정적 검색이다. "parser가 실제로 조용히 identifier로 허용하는가"는 별도 negative parser test가 필요하다.

### 1.1 DAYRUN G1 추가 실측

G1 성공 기준의 반복 가능한 근거를 위해 아래 probe를 추가했다.

| 항목 | 실측값 | 근거 |
|---|---:|---|
| `RESERVED_WORDS` 개수 | 10 | `lang/ddonirang-lang/src/grammar_config.rs` |
| 조사 전용 토큰 개수 | 18 | `lang/ddonirang-lang/src/grammar_config.rs` |
| lexer keyword literal 후보 | 41 | `lang/ddonirang-lang/src/lexer.rs` |
| dialect TSV 행 수(헤더 제외) | 119 | `lang/ddonirang-lang/src/data/dialect_forms.tsv` |
| `E_*` unique token | 3,749 | `rg -o "\bE_[A-Z0-9_]+\b" lang core tool tools tests pack` |
| 기존 `pack/` 디렉터리 | 1,038 | `pack/` 1-depth directory scan |
| pack 후보 ID | 53 | `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md` |
| 기존 pack 충돌 | 4 | `perf_baseline_v1`, `llm_corpus_extract_deterministic_v1`, `ai_det_tier_capability_matrix_v1`, `stdlib_l1_integrators_v1` |

CLI identifier probe 결과는 다음과 같다. 이 probe는 새 문법을 추가하지 않고 현재 frontdoor의 조용한 허용/거부 상태만 확인했다.

| Probe | 표면 | 결과 | 진단 |
|---|---|---|---|
| `ident_gaseol` | `가설` | PASS | 식별자로 통과 |
| `ident_geomsan` | `검산` | PASS | 식별자로 통과 |
| `ident_malgeori` | `말거리` | PASS | 식별자로 통과 |
| `ident_unit_underscore` | `단위_정의` | PASS | 식별자로 통과 |
| `ident_distribution_name` | `분포정규` | PASS | 식별자로 통과 |
| `ident_underscore` | `이름_밑줄` | PASS | 식별자로 통과 |
| `ident_question` | `이름물음?` | FAIL(expected) | `E_LEX_UNEXPECTED_CHAR` |

따라서 IDEAS의 `가설/검산/단위 정의/~분포` 계열 중 공백 표면과 `~` 표면은 아직 parser acceptance를 별도 negative test로 확인해야 하며, `가설/검산/말거리/단위_정의/분포정규` 꼴은 현재 조용히 식별자 공간으로 통과한다.

## 2. 예약어 후보 스윕

| 후보 | SSOT 본문 발견 줄 | 비SSOT 발견 줄 | 판정 |
|---|---:|---:|---|
| `여러속마디` | 0 | 6 | SSOT 누락, 예약 검토 필요 |
| `고정박자` | 0 | 3 | SSOT 누락, 예약 검토 필요 |
| `사건박자` | 0 | 5 | SSOT 누락, 예약 검토 필요 |
| `앞선모음` | 0 | 2 | SSOT 누락, 예약 검토 필요 |
| `다수결모음` | 0 | 1 | SSOT 누락, 예약 검토 필요 |
| `자리모음` | 0 | 3 | SSOT 누락, 예약 검토 필요 |
| `늦은제안다룸` | 0 | 8 | SSOT 누락, 예약 검토 필요 |
| `시앗묶음` | 0 | 23 | SSOT 누락, 우선 예약 후보 |
| `경계다룸` | 0 | 6 | SSOT 누락, 예약 검토 필요 |
| `가설` | 3 | 12 | SSOT에 일반 용례 있음, keyword 여부 분리 필요 |
| `검산` | 0 | 6 | SSOT 누락, 예약 검토 필요 |
| `단위 정의` | 3 | 8 | SSOT에 일반 용례 있음, 표면 keyword 여부 분리 필요 |
| `말거리` | 12 | 24 | 이미 용어 흔적 있음, 정본/후보 상태 확인 필요 |
| `~이름` | 0 | 1 | 문법 공간 예약 후보 |
| `설정해시` | 0 | 20 | SSOT 누락, 우선 예약 후보 |
| `공간갈래` | 0 | 2 | SSOT 누락, 예약 검토 필요 |
| `첫상태참조` | 0 | 4 | SSOT 누락, 예약 검토 필요 |
| `규칙묶음` | 0 | 3 | SSOT 누락, 예약 검토 필요 |
| `동점다룸` | 0 | 5 | SSOT 누락, 예약 검토 필요 |
| `슬롯정의` | 0 | 6 | SSOT 누락, 예약 검토 필요 |
| `입력틈` | 0 | 7 | SSOT 누락, 예약 검토 필요 |
| `늦은입력다룸` | 0 | 5 | SSOT 누락, 예약 검토 필요 |
| `제안한도` | 0 | 3 | SSOT 누락, 예약 검토 필요 |
| `관찰범위` | 0 | 7 | SSOT 누락, 예약 검토 필요 |
| `스냅틈` | 0 | 7 | SSOT 누락, 예약 검토 필요 |
| `해시검사틈` | 0 | 6 | SSOT 누락, 예약 검토 필요 |

### 2.1 해석

- `시앗묶음`, `설정해시`, `검산`, `관찰범위`는 발표 후 추가가 어려운 표면이다.
- `가설`, `단위 정의`, `말거리`는 이미 SSOT나 문서에 일반 용례가 있어, "일반 단어"와 "reserved keyword"의 경계를 먼저 정해야 한다.
- `~이름(...)`은 실제 문자열은 거의 없지만 문법 공간의 미래 가치가 크다.

## 3. 문법 공간 스윕

| 패턴 | 발견 줄 | 해석 |
|---|---:|---|
| `#모두필요` | 120 | `#` 계열은 이미 마디맺음갈래 등에서 사용 중 |
| `#빈칸채움` | 94 | `#` 새 조합은 충돌 검토 필요 |
| `@단위계` | 0 | 단위계 annotation 후보는 별도 설계 필요 |
| `~분포` | 0 | 비어 있음. 확률/분포 후보로 예약 가치 큼 |
| `~이름` | 1 | 아이디어 문서 수준 |
| `BLOCK_HEADER` | 94 | block header 오류/진단 체계가 이미 있음 |
| `HASH_FORBIDDEN` | 5 | `#` block header 금지 진단 흔적 있음 |
| `BANG_UNARY_RESERVED` | 15 | unused operator를 reserved error로 막은 선례 있음 |

### 3.1 권고

- `~` 계열은 발표 전 negative parser test로 "조용한 identifier 허용" 여부를 확인해야 한다.
- `#` 계열은 이미 의미가 많으므로 새 표면 추가 시 tag/마디맺음/헤더 금지와 충돌표가 필요하다.
- `@` 계열은 현재 검색상 약하지만 단위/annotation과 연결될 가능성이 있어 reserved syntax 표가 필요하다.

## 4. 오류 코드 스윕

| 항목 | 수치 |
|---|---:|
| 제품/pack/test 경로의 `E_*` unique token | 3,805 |
| DAYRUN 재현 스윕의 `E_*` unique token | 3,749 |
| 테스트/러너성 접두를 거칠게 제외한 `E_*` token | 2,782 |

대표적으로 확인된 코드/계열:

- `E_AGE_NOT_AVAILABLE`
- `E_BLOCK_HEADER_COLON_FORBIDDEN`
- `E_BLOCK_HEADER_HASH_FORBIDDEN`
- `E_BANG_UNARY_RESERVED`
- `E_OPEN_LOG_PARSE`
- `E_OPEN_LOG_TAMPER`
- `E_GAJI_LOCK_SCHEMA`
- `E_BOGAE_CODEC_MISMATCH`

### 4.1 위험

- `E_*`가 이미 많아 도구/테스트가 문자열에 의존할 가능성이 높다.
- parser/runtime/contract/AGE gate 구분이 문서상 namespace로 닫히지 않으면 발표 후 오류 코드 정리가 깨지는 변경이 된다.
- 교육 목적상 오류 코드는 "무엇이/어디서/어떻게" 3층 진단 사전과 연결되어야 한다.

### 4.2 권고

1. `OI-ERROR-CODE-NAMESPACE-01` 등록.
2. 접두 범주를 최소 5개로 분리: parser, canon, runtime, open/replay, pack/contract, AGE gate.
3. 대표 오류 20종은 `DIAG_THREE_LAYER_BEGINNER_DICTIONARY_DRAFT_V1_20260707.detjson`을 출발점으로 golden화.
4. 발표 전에는 기존 코드명을 rename하지 말고, 새 코드 추가 규칙부터 고정.

## 5. Schema Version 스윕

| 항목 | 수치/관찰 |
|---|---|
| `schema_version` 발견 줄 | 200 |
| 확인된 버전 흔적 | `v0`, `v1`, `v2`, `ddn.vendor.index.v1` |
| 확인된 정책 흔적 | 일부 경로는 `need v1`, 일부 open schema는 `expected=... actual=...` 오류 |

대표 관찰:

- `open.clock`과 `open.file_read`는 v1/v2 허용 흔적이 있다.
- `open.rand`, `open.input`, `open.solver`, `open.net`, `open.ffi`, `open.gpu`는 expected schema mismatch 오류가 있다.
- `gaji` lock 계열은 `schema_version=v1` 강제 흔적이 있다.

### 5.1 권고

공개 schema마다 아래를 명시해야 한다.

| 정책 | 의미 |
|---|---|
| `reject` | 다른 version은 오류 |
| `read_compat` | 이전 version 읽기 허용 |
| `upgrade` | 읽은 뒤 canonical 최신 version으로 변환 |
| `ignore_unknown_additive` | 알 수 없는 additive field 무시 |

`step_record v0.1 -> v0.2`처럼 add-only wire 확장은 이 표가 없으면 발표 후 호환성 논쟁이 된다.

## 6. Pack 후보 ID 중복 검사

| 후보 ID | 현재 `pack/<id>` 존재 | 판정 |
|---|---:|---|
| `std_bogae_core_v1` | no | 사용 가능 |
| `std_bogae_grid2d_v1` | no | 사용 가능 |
| `std_bogae_graph2d_v1` | no | 사용 가능 |
| `std_bogae_table_v1` | no | 사용 가능 |
| `std_bogae_sim2d_v1` | no | 사용 가능 |
| `std_bogae_timeline_v1` | no | 사용 가능 |
| `std_bogae_nurigym_v1` | no | 사용 가능 |
| `std_bogae_seulgi_lab_v1` | no | 사용 가능 |
| `std_bogae_grid3d_v1` | no | 사용 가능 |
| `std_bogae_game3d_v1` | no | 사용 가능 |
| `std_bogae_network_v1` | no | 사용 가능 |
| `std_bogae_tree_v1` | no | 사용 가능 |
| `std_bogae_matrix_v1` | no | 사용 가능 |
| `std_bogae_form_control_v1` | no | 사용 가능 |
| `std_bogae_surface_v1` | no | 사용 가능 |
| `std_bogae_profiler_v1` | no | 사용 가능 |
| `std_bogae_debugger_v1` | no | 사용 가능 |
| `nuri_madi_phase_table_v1` | no | 사용 가능 |
| `nuri_state_write_conflict_v1` | no | 사용 가능 |
| `nuri_submadi_snapshot_isolation_v1` | no | 사용 가능 |
| `nuri_reset_interaction_v1` | no | 사용 가능 |
| `nuri_action_collection_policy_v1` | no | 사용 가능 |
| `nuri_advanced_preset_contract_v1` | no | 사용 가능 |
| `settings_config_hash_proto_v1` | no | 사용 가능 |
| `settings_seed_bag_v1` | no | 사용 가능 |
| `settings_result_affecting_keys_v1` | no | 사용 가능 |
| `settings_bogae_selection_dual_path_v1` | no | 사용 가능 |
| `settings_section_dialect_alias_coverage_v1` | no | 사용 가능 |
| `perf_baseline_v1` | yes | 이미 생성됨 |
| `nurigym_step_record_v02_roundtrip_v1` | no | 사용 가능 |
| `diag_three_layer_message_v1` | no | 사용 가능 |
| `stdlib_l1_integrators_g1_v1` | no | 사용 가능 |
| `econ_model_first_supply_demand_equilibrium_v1` | no | 사용 가능 |
| `econ_model_first_money_supply_v1` | no | 사용 가능 |
| `econ_model_first_tax_welfare_v1` | no | 사용 가능 |
| `ko_common_promotion_measurement_v1` | no | 사용 가능 |
| `llm_corpus_extract_deterministic_v1` | yes | 이미 생성됨 |
| `save_vs_replay_artifact_split_v1` | no | 사용 가능 |
| `bogae_madang_track_v1_schema_smoke` | no | 사용 가능 |

### 6.1 해석

- 보개/누리/설정 후보 pack ID는 모두 비어 있다.
- `perf_baseline_v1`, `llm_corpus_extract_deterministic_v1`는 중복 위험이 아니라 이번 G1 실행으로 이미 점유된 정상 상태다.
- 위 표는 초기 부분 스윕 39건이다. DAYRUN 최종 충돌표는 `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md`의 53건 표를 기준으로 하며, 추가 충돌 2건은 `ai_det_tier_capability_matrix_v1`, `stdlib_l1_integrators_v1`이다.

## 7. 발표 전 필수 후속

1. reserved-word lint 도구화: 이 보고서의 후보 목록을 입력으로 반복 가능하게 만든다.
2. parser negative tests: `~분포`, `~이름(...)`, 미사용 `#/@/~` 조합이 조용히 identifier로 통과하는지 확인한다.
3. 오류 코드 namespace 문서: 새 코드 추가 규칙과 rename 금지 원칙을 고정한다.
4. schema version policy 표: 공개 schema마다 reject/read_compat/upgrade/ignore 규칙을 명시한다.
5. canonical golden coverage: 발표 범위 표면마다 정본 출력 golden이 있는지 별도 report로 닫는다.

## 8. 닫힘 등급

- 이 보고서 자체: `닫힘-문서`
- 제품/runtime/parser 동작 변경: 없음
- 발표 전 동결 완료 주장: 없음
- SSOT 본문 변경: 없음
