# 20260707 Codex dayrun

## 결과 요약

- G1 완료: SSOT 병합 준비 초안, OI 후보 묶음, 발표 전 동결 스윕 보고서 작성. 증빙: `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md`, `docs/context/proposals/OI_CANDIDATE_BUNDLE_20260706.md`, `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md`.
- G2 완료: `tests/run_perf_baseline_check.py`를 추가해 tick throughput, WASM-load axis의 CLI startup fallback, NuriGym rollout step/sec 3축을 측정하고 local baseline/gate detjson을 생성했다. 증빙: `I:/home/urihanl/ddn/codex/build/perf_baseline_v1/perf_baseline_report.detjson`, `I:/home/urihanl/ddn/codex/build/perf_baseline_v1/perf_baseline_generated_baseline.detjson`, `I:/home/urihanl/ddn/codex/build/perf_baseline_v1/perf_baseline_gate_report.detjson`.
- G3 완료: `work/beta/round0/BETA_USER_BUNDLE/`에 시작 가이드, 샘플, CLI 1쪽, T4 오류 fixture 3종, 기대 진단표, 페르소나 프롬프트 3종을 준비했다. 베타 세션 자체는 격리 위반 방지를 위해 실행하지 않았다.
- G4 완료: `stdlib_l1_integrators_g1_v1`과 경제 model-first 3종(`econ_model_supply_demand_equilibrium_v1`, `econ_model_money_supply_v1`, `econ_model_tax_welfare_v1`)을 실행 가능한 pack/golden으로 추가했다.
- G5 완료: `tests/tools/extract_llm_corpus_v1.py` 진입점과 grammar manifest 기반 card를 추가하고 `out/llm_corpus_v1.jsonl`을 126행 deterministic JSONL로 재생성했다.
- G6 완료: `tests/tools/config_digest_proto.py`, `tests/tools/reserved_sweep_lint.py`, `tests/run_dayrun_g6_tools_check.py`를 추가해 설정해시 prototype과 G1 reserved sweep 재현을 도구화했다.
- G7 완료: `docs/reports/audit/SETTINGS_GEOUL_RUN_AGE_GATE_RECHECK_V1.md`, `docs/reports/audit/NURIGYM_CONSUMER_EVIDENCE_STATUS_V1.md`를 추가해 상태 정합 리포트 2건을 남겼다.

## 질문 큐

1. `설정.누리` key set에서 `누리갈래`를 `설정.실행.차림새` 축과 분리할지, 중복으로 보고 제거할지 결정 필요.
2. `지연마디` 소유권을 `설정.슬기`, `설정.샘`, `설정.실행` 중 어디에 둘지 결정 필요.
3. OQ-1: 같은 큰마디의 임자 실행 순서를 파일 선언 순서로 할지 `agent_id` 사전순으로 할지 결정 필요.
4. OQ-2: 세움과 매마디 상호 갱신을 1회 평가로 제한하고 순환 의존을 오류로 볼지 결정 필요.
5. OQ-3: 큰마디 P2 전처리를 샘 소속으로 볼지 이야기 소속으로 볼지 결정 필요.
6. OQ-4: `(N마디)마다` 판정 시점을 P3 내부 어디에 둘지 결정 필요.
7. OQ-R1: `누리다시`가 `설정.누리`만 재읽는지 `설정.실행`까지 재읽는지 결정 필요.
8. `합치기갈래` 신설 대신 `행동모음갈래` 값 확장을 채택할지 결정 필요.
9. `가설/검산/단위 정의/말거리/~분포` 후보를 발표 전 reserved/proposal로 선점할지 결정 필요.

## 발견한 문제

- IDEAS의 예약어 후보 `가설/검산/말거리`는 현재 `RESERVED_WORDS`에 없고 CLI check에서 식별자로 통과한다.
- `단위_정의`와 `분포정규` 형태도 식별자로 통과한다. 공백 포함 `단위 정의`와 `~이름(...)` 분포 표면은 별도 문법 공간 검토가 필요하다.
- 고유 `E_*` 문자열이 3749개로 넓게 퍼져 있어 public-facing 진단 코드와 internal checker code namespace가 섞여 있다.
- pack 후보 ID 53건 중 4건은 기존 pack과 충돌한다: `perf_baseline_v1`, `llm_corpus_extract_deterministic_v1`, `ai_det_tier_capability_matrix_v1`, `stdlib_l1_integrators_v1`.
- `python tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py`는 parity pack/node runner 자체가 아니라 roadmap matrix 집계 기대값 drift(`rows=90 behavior=90 docs=0`)로 FAIL한다.
- `gym_reset_seed_implies_complete_episode_reset_v1`, `resident_reset_episode_equiv_v1`, `nurigym_step_record_v02_roundtrip_v1` pack은 후보 표에는 있으나 현재 pack 디렉터리가 없다.

## 다음 날 추천 착수점

- 실제 AI 베타 Round 0는 별도 격리 세션에서 `BETA_USER_BUNDLE`만 제공해 실행한다.
- A3 NuriGym Python/Web parity checker의 roadmap matrix 집계 기준을 현재 matrix 상태와 맞춘다.
- reset/resident equivalence 및 `nurigym.step_record.v0.2` roundtrip pack 후보 3건을 별도 착수한다.

## 검증

- G1 probe: `cargo run --quiet --manifest-path tools/teul-cli/Cargo.toml -- check <freeze_probe>` 7건 실행, 6 PASS / 1 expected FAIL(`E_LEX_UNEXPECTED_CHAR`).
- E-code scan: unique `E_*` 3749개.
- pack 후보 충돌 검사: 후보 53건 / 기존 pack 충돌 4건.
- `cargo check`: PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g1.log`.
- `python tests/run_ci_sanity_gate.py --profile core_lang`: PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g1.log`.
- G2: `python tests/run_perf_baseline_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/perf_baseline_check_g2.log`.
- G2: `python tests/run_perf_baseline_v1_pack_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/perf_baseline_v1_pack_check_g2.log`.
- G2: `python tests/run_pack_golden.py perf_baseline_v1` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/perf_baseline_v1_pack_golden_g2.log`.
- G2 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g2.log`.
- G2 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g2.log`.
- G3: `python tests/run_beta_round0_bundle_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/beta_round0_bundle_check_g3.log`.
- G3 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g3.log`.
- G3 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g3.log`.
- G4: `python tests/run_stdlib_l1_integrators_g1_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/stdlib_l1_integrators_g1_check_g4.log`.
- G4: `python tests/run_econ_model_first_g1_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/econ_model_first_g1_check_g4.log`.
- G4: `python tests/run_pack_golden.py stdlib_l1_integrators_g1_v1 econ_model_supply_demand_equilibrium_v1 econ_model_money_supply_v1 econ_model_tax_welfare_v1` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/g4_pack_golden.log`.
- G4 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g4.log`.
- G4 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g4.log`.
- G5: `python tests/run_llm_corpus_extract_deterministic_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/llm_corpus_extract_deterministic_check_g5.log`.
- G5: `python tests/run_llm_corpus_v1_dayrun_check.py` PASS, rows=126, sha256=`sha256:d39ac5947f663ea3d21d9e35e0e758da764495f258e6416f354fe72ed838c7ed`. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/llm_corpus_v1_dayrun_check_g5.log`.
- G5: `python tests/run_pack_golden.py llm_corpus_extract_deterministic_v1` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/llm_corpus_pack_golden_g5.log`.
- G5 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g5.log`.
- G5 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g5.log`.
- G6: `python tests/run_dayrun_g6_tools_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/dayrun_g6_tools_check.log`.
- G6 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g6.log`.
- G6 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g6.log`.
- G7: `python tests/run_dayrun_g7_reports_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/dayrun_g7_reports_check.log`.
- G7 probe: `python tests/run_pack_golden.py lang_settings_header_closure_v1` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/lang_settings_header_closure_g7_probe.log`.
- G7 probe: `python tests/run_nuri_gym_contract_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nuri_gym_contract_g7_probe.log`.
- G7 probe: `node tests/nurigym_python_web_parity_runner.mjs` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_node_g7_probe.log`.
- G7 probe: `python tests/run_pack_golden.py nurigym_python_web_parity_v1 nuri_gym_gridmaze_v1 nuri_gym_bandit_v1` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_pack_golden_g7_probe.log`.
- G7 probe: `python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_action_pipeline_g7_probe.log`.
- G7 probe: `python tests/run_nurigym_shared_sync_priority_tiebreak_pack_check.py` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_priority_tiebreak_g7_probe.log`.
- G7 probe: `python tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py` FAIL 확인. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/nurigym_python_web_parity_g7_probe.log`.
- G7 종료 배터리: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_g7.log`.
- G7 종료 배터리: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_g7.log`.
- 하루 마감: `cargo check` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/cargo_check_final.log`.
- 하루 마감: `python tests/run_ci_sanity_gate.py --profile core_lang` PASS. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/core_lang_sanity_final.log`.
- 하루 마감: `git status --short docs/ssot` 출력 없음. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/git_status_docs_ssot_final.log`.
- 하루 마감: `git status --short` 확인. 로그 `I:/home/urihanl/ddn/codex/build/dayrun_logs/git_status_final.log`.
- `git status --short docs/ssot`: 출력 없음(SSOT 직접 수정 없음).
- `git status --short`: 기존 proof certificate 산출물, `open_*` replay 로그 변경, 이전 세션 untracked pack/test/tool 산출물과 이번 DAYRUN 신규/수정 산출물이 함께 남아 있음. main push/삭제/리셋은 하지 않음.
