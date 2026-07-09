# 20260709 Codex Decision Closure Batch D2

## 결과 요약

- D0: 완료. `codex/queue-20260706`에서 시작 상태와 경계를 기록했다.
- D1 Settings keyset: 완료. `settings_keyset_policy_v1` pack/checker로 `설정.누리`/`설정.이야기` keyset과 hash 정책을 고정했다.
- D2 NuriGym step_record v0.2 public schema: 완료. opt-in `step_record_version="v0.2"` product wire와 public schema pack/checker를 추가했다.
- D3 Report: 완료. DEV_SUMMARY와 NuriGym v0.2 public schema status report를 갱신했다.

## 경계

- 브랜치: `codex/queue-20260706`.
- `main` 직접 커밋 금지.
- `docs/ssot/**` 직접 수정 금지.
- parser 문법 변경 금지.
- runtime `state_hash` 산식 변경 금지.
- 기본 NuriGym v0.1 output/golden 유지. v0.2 wire는 opt-in으로만 추가한다.
- 기존 untracked 참고 파일은 커밋하지 않는다.

## 시작 상태

- `git branch --show-current`: `codex/queue-20260706`.
- `git status --short`: 추적 변경 없음, 기존 untracked 참고 파일만 존재.
- `git status --short -- docs/ssot`: 변경 없음.
- 최근 기준 커밋: `2f40a0f [DC-D1-REPORT] record decision closure d1 results`.

## 결정 가정

1. `설정.누리` key set은 현재 증빙 기준 `시앗`, `시앗묶음`으로 고정한다.
2. `설정.이야기` key set은 `들머리`만 result-affecting으로 고정한다.
3. `설정.셈 { 적분: ... }`는 이번 keyset에 포함하지 않고 현황 기록만 한다.
4. NuriGym `step_record_version="v0.2"`는 opt-in public schema로 시작하며 default v0.1 출력은 변경하지 않는다.
5. v0.2 `done`은 `terminated || truncated`와 같아야 한다.

## 검증 로그

- D0 시작: `git status --short -- docs/ssot` PASS.
- D1 settings keyset:
  - `python -m json.tool pack/settings_keyset_policy_v1/contract.detjson` PASS.
  - `python -m py_compile tests/run_settings_keyset_policy_check.py` PASS.
  - `python tests/run_pack_golden.py settings_keyset_policy_v1` PASS.
  - `python tests/run_settings_keyset_policy_check.py` PASS.
  - `git status --short -- docs/ssot` PASS.
- D2 NuriGym v0.2 public schema:
  - `python -m json.tool pack/nurigym_step_record_v02_public_schema_v1/contract.detjson` PASS.
  - `python -m py_compile tests/run_nurigym_step_record_v02_public_schema_check.py` PASS.
  - `cargo test --manifest-path tools/teul-cli/Cargo.toml nurigym_build_step_record -- --nocapture` PASS.
  - `python tests/run_pack_golden.py nurigym_step_record_v02_public_schema_v1` PASS.
  - `python tests/run_nurigym_step_record_v02_public_schema_check.py` PASS.
  - `python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py` PASS.
  - `python tests/run_nuri_gym_contract_check.py` PASS.
  - `cargo check` PASS (기존 `ddonirang-tool` unused 경고만 출력).
  - `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
  - `git status --short -- docs/ssot` PASS.
  - 커밋 전 `python tests/run_nurigym_step_record_v02_roundtrip_check.py` / `python tests/run_nurigym_step_record_v02_consumer_g6_check.py`는 product path dirty boundary에서 중단됐다.
  - 커밋 후 `python tests/run_nurigym_step_record_v02_roundtrip_check.py` PASS.
  - 커밋 후 `python tests/run_nurigym_step_record_v02_consumer_g6_check.py` PASS.
  - 커밋 후 `python tests/run_nurigym_step_record_v02_public_schema_check.py` PASS.
  - 커밋 후 `python tests/run_settings_keyset_policy_check.py` PASS.
  - 커밋 후 `python tests/run_dayrun_g6_tools_check.py` PASS.
  - 커밋 후 `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- D3 report:
  - `docs/context/all/DEV_SUMMARY.md` 갱신.
  - `docs/context/reports/NURIGYM_STEP_RECORD_V02_PUBLIC_SCHEMA_STATUS_V1_20260709.md` 추가.
  - `docs/context/reports/INDEX.md` 갱신.
  - `git status --short -- docs/ssot` PASS.

## 커밋

- `fbf8ab2 [DC-D2-G0] start decision closure batch d2`
- `bc3b1b2 [DC-D2-SETTINGS-KEYSET] add settings keyset policy pack`
- `380c51b [DC-D2-NURIGYM-V02] add opt-in step record public schema`
- `[DC-D2-REPORT]` 예정.

## 질문 큐

- 없음.
