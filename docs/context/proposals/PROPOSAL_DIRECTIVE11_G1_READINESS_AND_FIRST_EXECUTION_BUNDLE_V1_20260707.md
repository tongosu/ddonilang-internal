# PROPOSAL_DIRECTIVE11_G1_READINESS_AND_FIRST_EXECUTION_BUNDLE_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 분류: PROPOSAL / READINESS_AUDIT / EXECUTION_BUNDLE / SEVEN_PURPOSE_G1
- 기준: `CODEX 지시문 묶음` 지시문 11, `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md`
- 상태: 실행 준비도 정리. `docs/ssot/**` 수정 없음, parser/runtime 신규 문법 없음, closure 주장 없음

## 0. 결론

지시문 11의 7개 G1 항목은 모두 방향이 맞다. 다만 현재 저장소 상태 기준으로는 동일한 난이도가 아니다.

가장 먼저 해야 할 일은 새 기능을 크게 만들기보다, 이미 있는 증빙을 G1 이름으로 재포장하고 빠진 계약만 얇게 보강하는 것이다. 특히 `P1-G1 step_record`, `P5경제-G1`, `P5물리-G1`은 기반 자료가 이미 있고, `P4-G1`, `P6-G1`, `P7-G1`은 새 audit 또는 추출 계약이 필요하다. `F0-2`는 기존 `benchmark_baseline_v1`을 버리지 말고 `perf_baseline_v1`로 성능 회귀 게이트를 덧씌우는 방향이 안전하다.

## 1. G1 준비도 표

| 항목 | 현재 증빙 | 준비도 | 바로 할 일 |
|---|---|---:|---|
| F0-2 결정적 벤치 계약 | `pack/benchmark_baseline_v1`, `tests/run_benchmark_baseline_pack_check.py`, studio benchmark snapshot packs | 60% | `perf_baseline_v1`을 새 이름으로 만들되, 기존 benchmark pack을 하위 증빙으로 참조한다. 시간 수치와 회귀 허용폭만 새 계약으로 분리한다. |
| P1-G1 `nurigym.step_record.v0.2` | `pack/nurigym_shared_sync_action_pipeline_v1`에 `raw_action/resolved_action/normalized_action/action_status/merge_candidates/merged_action/applied_action/missing_input` 존재 | 75% | 의미는 거의 준비됨. `nurigym_step_record_v02_roundtrip_v1` pack 후보와 v0.1 호환 규칙을 공식 proposal로 묶는다. |
| P4-G1 진단 3층 | `pack/diag_fixit_coverage_v1`, fix-it JSON schema류 테스트 | 45% | fix-it 기반은 있으나 초심자 3층 채점은 별도다. 대표 E-code 20종 현황 audit과 문구 사전 detjson 초안을 만든다. |
| P5물리-G1 적분기 | `pack/stdlib_l1_integrators_v1`에 `적분.오일러/적분.반암시적오일러`, velocity verlet 관련 pack/test 존재 | 65% | `선형보간`과 Fixed64 dt/stiff 한계 1쪽 문서를 추가해야 G1이 닫힌다. 베를레는 G1 필수보다 확장 증빙으로 둔다. |
| P5경제-G1 model-first 3종 | `pack/econ_age4_ready_baseline_tax_ceiling_v1`, `pack/social_world_econ_2_v1`, 다수 경제 curriculum smoke | 70% | 수요-공급/세금은 강하다. 통화 공급은 별도 skeleton이 필요하다. 세금-후생은 기존 세금 pack을 welfare 지표 포함 skeleton으로 확장한다. |
| P6-G1 ko-common 승격 실측 | `paper1_canonize_agglutinative_ast_*` pack으로 조사/어순 동치 증빙 존재. ko-common proposal 다수 존재 | 40% | 교착어 AST 증빙과 ko-common 승격은 별개다. core_keyword_matrix, josa_role_matrix, roundtrip golden, native 확인 4조건을 실측해야 한다. |
| P7-G1 LLM 코퍼스 | 설계 문서만 존재. 실제 `llm_corpus_v1` 산출물/추출기 없음 | 25% | 기존 pack README/input/golden에서 정본 예제와 설명을 결정적으로 뽑는 프로토타입이 필요하다. |

## 2. 항목별 판단

### F0-2 벤치

기존 `benchmark_baseline_v1`은 이미 `education_preview`, `seamgrim_local_run`, `nurigym_million_step_baseline` 세 축을 갖고 있고 runner-backed다. 지시문 11의 `perf_baseline_v1`은 이것을 대체하는 이름이 아니라 성능 회귀 기준을 얹는 상위 계약으로 보는 편이 맞다.

권고 산출물:

- `docs/context/proposals/PROPOSAL_PERF_BASELINE_V1_20260707.md`
- `pack/perf_baseline_v1/contract.detjson`
- `tests/run_perf_baseline_pack_check.py`

주의: 최초 수치 고정 전에는 "성능 충분"을 주장하지 않는다. 측정 계약만 먼저 닫는다.

### P1-G1 step_record v0.2

지시문 11이 요구한 필드 대부분은 이미 `nurigym_shared_sync_action_pipeline_v1`에 있다. 따라서 새 runtime 의미를 만들 필요가 없다. 남은 일은 `step_record.v0.2`라는 이름으로 wire schema, add-only 호환, roundtrip 증빙을 분리하는 것이다.

권고 산출물:

- `PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707.md`
- `pack/nurigym_step_record_v02_roundtrip_v1`

호환 원칙:

- v0.1 consumer는 모르는 필드를 무시한다.
- v0.2 producer는 `raw_action`, `normalized_action`, `action_status`, `merged_action`, `applied_action`을 가능하면 항상 낸다.
- `resolved_action`, `merge_candidates`, `missing_input`은 shared/multi-agent 모드에서만 의미가 있어도 된다.

### P4-G1 진단 3층

현재 fix-it coverage는 "고칠 수 있는 payload가 결정적으로 나오는가"를 본다. 지시문 11의 요구는 한 단계 다르다. 초심자가 읽었을 때 `무엇이/어디서/어떻게`가 분리되어 보이는지 채점해야 한다.

권고 산출물:

- `docs/reports/audit/DIAG_THREE_LAYER_MESSAGE_AUDIT_V1_20260707.md`
- `pack/diag_three_layer_message_v1`
- `pack/diag_three_layer_message_v1/e_code_beginner_dictionary.detjson`

주의: 메시지 실변경은 SSOT 오너 승인 뒤에 한다. 지금은 audit과 사전 초안까지가 안전하다.

### P5물리-G1 적분기

`stdlib_l1_integrators_v1`은 좋은 출발점이지만 G1 요구에는 `선형보간`과 Fixed64 한계 문서가 빠져 있다. velocity verlet 증빙은 이미 별도로 많지만, G1 최소집합의 이름은 오일러/반암시적오일러/선형보간으로 고정하는 편이 교육 경로에 맞다.

권고 산출물:

- `pack/stdlib_l1_integrators_g1_v1`
- `docs/context/proposals/NOTE_FIXED64_SIMULATION_LIMITS_V1_20260707.md`

주의: `속도 베를레`는 좋은 확장 후보지만, G1 필수로 끌어오면 범위가 커진다.

### P5경제-G1 model-first

경제 쪽은 "없다"가 아니라 "이름이 흩어져 있다"에 가깝다. `econ_age4_ready_baseline_tax_ceiling_v1`은 수요-공급 균형, 단위세, 가격상한을 이미 다룬다. `social_world_econ_2_v1`은 model-first bridge row를 주장한다. 다만 지시문 11의 세 skeleton 명칭으로 정리되어 있지 않고, 통화 공급은 별도 축이 약하다.

권고 산출물:

- `pack/econ_model_first_supply_demand_equilibrium_v1`
- `pack/econ_model_first_money_supply_v1`
- `pack/econ_model_first_tax_welfare_v1`

주의: 경제 pack은 예측/정책 조언으로 읽히지 않게 "교육용 결정적 reduced model" 경계를 README에 반드시 쓴다.

### P6-G1 ko-common

교착어 AST 동치 pack은 강한 증빙이다. 하지만 ko-common T1 승격 조건과는 직접 등치하면 안 된다. ko-common은 한국어 상용 별칭층이고, paper1 pack은 조사/어순/AST 정본화 증빙이다.

권고 산출물:

- `docs/reports/audit/KO_COMMON_PROMOTION_READINESS_AUDIT_V1_20260707.md`
- `pack/ko_common_promotion_measurement_v1`

체크 항목:

- `core_keyword_matrix` 존재와 coverage
- `josa_role_matrix` 존재와 coverage
- roundtrip golden 수
- native 확인 여부

### P7-G1 LLM 코퍼스

이 항목은 실제 산출물이 가장 비어 있다. 다만 구현 난이도는 낮다. 처음부터 완벽한 LSP/문법 지식 베이스를 만들 필요는 없고, 기존 pack의 README, input, golden을 안정 정렬해서 JSONL로 뽑으면 된다.

권고 산출물:

- `tools/extract_llm_corpus_v1.py`
- `out/llm_corpus_v1.jsonl`
- `pack/llm_corpus_extract_deterministic_v1`

결정성 규칙:

- 입력 pack 목록은 정렬된 경로 순서로 고정한다.
- 같은 파일 내용이면 같은 JSONL 행 순서와 같은 digest가 나와야 한다.
- 생성형 요약 금지. README 첫 문단, intent, contract 필드처럼 저장소에 있는 텍스트만 쓴다.

## 3. 첫 실행 묶음 권고

### 묶음 A: 저위험 docs/audit

1. `P1-G1 step_record v0.2` proposal
2. `P4-G1 진단 3층` audit
3. `P6-G1 ko-common` 승격 실측 report

이 묶음은 parser/runtime을 건드리지 않고도 바로 가치가 있다. 그리고 G1의 "무엇을 닫을지"를 먼저 고정한다.

### 묶음 B: pack skeleton

1. `F0-2 perf_baseline_v1`
2. `P5물리-G1 stdlib_l1_integrators_g1_v1`
3. `P5경제-G1 econ_model_first_*`
4. `P7-G1 llm_corpus_extract_deterministic_v1`

이 묶음은 파일 수가 늘고 테스트가 생기므로 별도 세션으로 나누는 것이 맞다.

## 4. 하지 말아야 할 일

- G2/G3 착수 금지. 벡터화, 보개마당 트랙 v1, 실시간 60fps, ja 파일럿, 슬기 표면 승격은 이번 지시문 범위가 아니다.
- 기존 `benchmark_baseline_v1`을 폐기하거나 이름만 바꾸지 않는다.
- `paper1_canonize_agglutinative_ast_*`를 ko-common 승격 완료 증빙으로 과잉 해석하지 않는다.
- 진단 메시지 본문을 바로 바꾸지 않는다. 먼저 audit과 문구 사전 초안이 필요하다.
- 성능 수치 측정 전 "성능 충분"을 주장하지 않는다.

## 5. 다음 작업 단위 제안

가장 좋은 첫 작업 단위는 `P1-G1 + P4-G1 + P6-G1`이다. 이유는 세 항목 모두 SSOT 변경 없이 report/proposal로 닫을 수 있고, 이후 pack 구현의 기준이 된다.

그 다음 작업 단위는 `F0-2 + P7-G1`이다. 두 항목 모두 "같은 저장소 상태이면 같은 산출물"이라는 결정성 계약을 공유하므로 도구/러너 구조를 함께 맞출 수 있다.

`P5물리-G1`과 `P5경제-G1`은 교육/선언시뮬 목적의 직접 증빙이므로, 위 두 묶음 뒤에 pack skeleton으로 분리 착수한다.
