# 20260709 Codex Decision Closure Batch D1

## 결과 요약

- D0: 완료. `codex/queue-20260706`에서 시작 상태와 경계를 기록했다.
- D1 Settings digest: 완료. `문서`만 doc/meta 제외로 두고 `이야기.들머리`를 result-affecting으로 고정했다.
- D2 NuriGym step_record v0.2: 완료. 기존 consumer pack과 분리된 roundtrip pack을 `run_pack_golden.py`와 전용 checker로 재검증했다.
- D3 Gaji metadata stale closure: 완료. 세 metadata가 `9d94496 [LHF-E]`에서 이미 적용된 상태임을 보고서와 checker로 고정했다.

## 경계

- 브랜치: `codex/queue-20260706`.
- `main` 직접 커밋 금지. `main`과 queue가 같은 ref라도 커밋은 queue 브랜치에서만 수행한다.
- `docs/ssot/**` 직접 수정 금지.
- parser/runtime 문법 확장 금지.
- runtime `state_hash` 산식 변경 금지.
- 기존 untracked 참고 파일은 커밋하지 않는다.

## 시작 상태

- `git switch codex/queue-20260706`: 완료.
- `git branch --show-current`: `codex/queue-20260706`.
- 추적 변경 없음.
- 기존 untracked 참고 파일 다수는 유지하고 커밋하지 않는다.
- `pack/nurigym_step_record_v02_roundtrip_v1`은 이미 존재하나 `tests/run_nurigym_step_record_v02_roundtrip_check.py`는 없다. D2는 기존 pack을 검증 가능하게 보강한다.

## 결정 가정

1. `설정.이야기.들머리`는 entrypoint 선택으로 실행 결과를 바꿀 수 있으므로 result-affecting으로 분류한다.
2. `nurigym_step_record_v02_roundtrip_v1`은 기존 consumer pack과 역할을 분리한다.
3. gaji metadata 3건은 이미 적용된 상태이므로 새 파일 생성이 아니라 stale 상태 보정/검증으로 처리한다.

## 검증 로그

- D0 시작: `git status --short` PASS(추적 변경 없음, 기존 untracked 참고 파일만 존재).
- D1 settings:
  - `python -m json.tool pack/settings_config_digest_v1/contract.detjson` PASS.
  - `python -m py_compile tests/tools/config_digest_proto.py tests/run_settings_config_digest_v1_check.py` PASS.
  - `python tests/tools/config_digest_proto.py --selftest` PASS.
  - `python tests/run_pack_golden.py settings_config_digest_v1` PASS.
  - `python tests/run_settings_config_digest_v1_check.py` PASS.
  - `python tests/run_dayrun_g6_tools_check.py` PASS.
  - `git status --short -- docs/ssot` PASS.
- D2 step_record:
  - `python -m json.tool pack/nurigym_step_record_v02_roundtrip_v1/contract.detjson` PASS.
  - `python -m py_compile tests/run_nurigym_step_record_v02_roundtrip_check.py tests/run_nurigym_step_record_v02_roundtrip_pack_check.py` PASS.
  - `python tests/run_pack_golden.py nurigym_step_record_v02_roundtrip_v1` PASS.
  - `python tests/run_nurigym_step_record_v02_roundtrip_pack_check.py` PASS.
  - `python tests/run_nurigym_step_record_v02_roundtrip_check.py` PASS.
  - `python tests/run_nurigym_step_record_v02_consumer_g6_check.py` PASS.
- D3 gaji status:
  - `python -m py_compile tests/run_gaji_metadata_3_applied_status_check.py` PASS.
  - `python tests/run_gaji_metadata_3_applied_status_check.py` PASS.
  - `python tests/run_gaji_registry_pack_check.py` PASS.
  - `python tests/run_gaji_registry_strict_audit_check.py` PASS.
  - `python tests/run_gaji_registry_defaults_check.py` PASS.
  - `git status --short -- docs/ssot` PASS.

## 변경 기록

- D1 settings:
  - `tests/tools/config_digest_proto.py`: `DOC_SECTIONS={"문서"}`를 유지하고 `이야기.들머리`를 run/result-affecting classifier에 포함했다.
  - `pack/settings_config_digest_v1`: alias, 절 순서, `문서` 제외, `이야기.들머리` 포함 정책을 고정하는 pack을 추가했다.
  - `tests/run_settings_config_digest_v1_check.py`: pack contract, digest 정책, classifier, state_hash 비접촉 경계를 검사한다.
  - `tests/tools/reserved_sweep_lint.py`: Run3A까지 누적된 의도적 진단 토큰 추가로 `e_unique_tokens_wide` 기준값을 3812로 보정했다. 원인은 `6f69eb4` 3799 이후 declarative closure 진단 토큰이 단계별로 추가된 것이며 누락 회귀는 아니다.
- D2 step_record:
  - `pack/nurigym_step_record_v02_roundtrip_v1/input.ddn`과 golden runner fields를 추가해 `run_pack_golden.py` 경로에서 pack을 인식하게 했다.
  - `pack/nurigym_step_record_v02_roundtrip_v1/contract.detjson`: `E_STEP_RECORD_REJECTED_IN_MERGE`, `E_STEP_RECORD_CLIP_NOOP`, `E_STEP_RECORD_MISSING_STATUS_MISMATCH` diagnostic contract를 명시했다.
  - `tests/run_nurigym_step_record_v02_roundtrip_check.py`: add-only 필드, v0.1 backward read, shared merge provenance, 세 진단 shape, runtime/state_hash 비접촉 경계를 검사한다.
- D3 gaji status:
  - `docs/context/reports/GAJI_METADATA_3_APPLIED_STATUS_V1_20260709.md`: `GAJI_REGISTRY_CLOSURE_V1`와 `PROPOSAL_GAJI_MISSING_METADATA_V1_20260706`의 stale "생성 없음" 상태를 현재 적용 상태로 보정했다.
  - `docs/context/reports/INDEX.md`: 새 status 보고서를 인덱스에 추가했다.
  - `tests/run_gaji_metadata_3_applied_status_check.py`: 세 `gaji.toml` 값, tracked 상태, `9d94496 [LHF-E]` 이력, 보고서 토큰, `docs/ssot` 비접촉을 검사한다.
