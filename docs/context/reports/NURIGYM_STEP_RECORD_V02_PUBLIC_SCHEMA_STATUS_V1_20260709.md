# NuriGym step_record v0.2 Public Schema Status V1 (2026-07-09)

## 결론

- 상태: opt-in public schema product wire landed.
- 기본 출력: `v0.1` 유지. `step_record_version` 미지정 시 dataset header와 step rows에 v0.2 public fields를 내보내지 않는다.
- opt-in 출력: input JSON에 `"step_record_version": "v0.2"`가 있을 때만 legacy `nurigym.step.v1` row에 add-only fields를 방출한다.
- 경계: parser 문법 변경 없음, runtime `state_hash` 산식 변경 없음, Gymnasium full compatibility claim 없음.

## 구현 근거

- input JSON optional key: `tools/teul-cli/src/cli/nurigym.rs:42`.
- default `v0.1` / opt-in `v0.2` parser: `tools/teul-cli/src/cli/nurigym.rs:1525`.
- dataset header의 v0.2 opt-in 표시: `tools/teul-cli/src/cli/nurigym.rs:1314`.
- step row의 v0.2 fields(`step_record_version`, `terminated`, `truncated`, `info`) 방출: `tools/teul-cli/src/cli/nurigym.rs:1365`.
- v0.2에서 action pipeline fields를 항상 방출하고 `missing_input`을 배열로 내보내는 경로: `tools/teul-cli/src/cli/nurigym.rs:1381`, `tools/teul-cli/src/cli/nurigym.rs:1402`, `tools/teul-cli/src/cli/nurigym.rs:1430`.
- core step structs의 additive 종료 원인 보존:
  - gridmaze: `core/src/nurigym/gridmaze.rs:34`, `core/src/nurigym/gridmaze.rs:124`, `core/src/nurigym/gridmaze.rs:158`.
  - cartpole: `core/src/nurigym/cartpole.rs:38`, `core/src/nurigym/cartpole.rs:107`, `core/src/nurigym/cartpole.rs:140`.
  - pendulum: `core/src/nurigym/pendulum.rs:33`, `core/src/nurigym/pendulum.rs:97`, `core/src/nurigym/pendulum.rs:131`.
  - bandit: `core/src/nurigym/bandit.rs:28`, `core/src/nurigym/bandit.rs:89`.

## Pack 관계

- D1 `nurigym_step_record_v02_roundtrip_v1`: producer-wire-consumer fixture compatibility와 diagnostic contract 검증.
- D2 `nurigym_step_record_v02_public_schema_v1`: 실제 `teul-cli nurigym run` 제품 wire emission 검증.
- D2 contract는 opt-in/default/public fields/case 관계를 명시한다: `pack/nurigym_step_record_v02_public_schema_v1/contract.detjson:7`, `pack/nurigym_step_record_v02_public_schema_v1/contract.detjson:25`, `pack/nurigym_step_record_v02_public_schema_v1/contract.detjson:46`, `pack/nurigym_step_record_v02_public_schema_v1/contract.detjson:53`.

## 검증 근거

- checker는 실제 `teul-cli nurigym run`을 실행한다: `tests/run_nurigym_step_record_v02_public_schema_check.py:116`.
- checker는 v0.2 row에서 legacy fields/additive fields, `done == terminated || truncated`, 배열형 `missing_input`을 검증한다: `tests/run_nurigym_step_record_v02_public_schema_check.py:162`.
- checker는 default v0.1 row가 v0.2 fields를 내보내지 않는지 검증한다: `tests/run_nurigym_step_record_v02_public_schema_check.py:217`.

## 실행 로그

- `python tests/run_pack_golden.py nurigym_step_record_v02_public_schema_v1` PASS.
- `python tests/run_nurigym_step_record_v02_public_schema_check.py` PASS.
- `python tests/run_nurigym_step_record_v02_roundtrip_check.py` PASS.
- `python tests/run_nurigym_step_record_v02_consumer_g6_check.py` PASS.
- `python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py` PASS.
- `python tests/run_nuri_gym_contract_check.py` PASS.
- `python tests/run_dayrun_g6_tools_check.py` PASS.
- `cargo check` PASS.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- `git status --short -- docs/ssot` PASS.
