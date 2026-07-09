# GAJI_METADATA_3_APPLIED_STATUS_V1

작성: 2026-07-09 KST  
목적: 과거 보고서/제안서에 남은 `gaji.toml` "생성 없음" 상태를 현재 적용 상태로 보정한다.  
경계: stale 문서 직접 수정 없음. `docs/ssot/**` 수정 없음. parser/runtime/state_hash 변경 없음.

## 결론

`std_grid`, `std_input_map`, `std_physics_1d`의 가지 metadata 3건은 이미 적용되어 있다.

- 적용 커밋: `9d94496 [LHF-E] apply approved gaji metadata`
- 현재 파일:
  - `gaji/std_grid/gaji.toml`
  - `gaji/std_input_map/gaji.toml`
  - `gaji/std_physics_1d/gaji.toml`
- 이번 D1 배치에서는 새 gaji metadata 파일을 만들지 않았다. 기존 적용 상태를 보고서와 checker로 고정한다.

## Stale 원문

아래 문서는 작성 당시에는 맞았지만 현재 상태와 다르다. 직접 수정하지 않고 이 보고서를 후속 보정 문서로 둔다.

| 문서 | 기존 주장 | 현재 보정 |
|---|---|---|
| `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:73`-`docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:75` | `std_grid`, `std_input_map`, `std_physics_1d`를 metadata 없는 패키지 후보로 분류 | 세 경로 모두 `gaji.toml` 적용됨 |
| `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:94` | 세 후보는 `gaji.toml`을 만들지 않고 후보로만 보고 | `9d94496` 이후 적용 상태 |
| `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:96` | M2에서는 `gaji.toml`을 추가하지 않음 | M2 당시 기록으로 보존, 현재 상태는 적용됨 |
| `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:5` | 실제 `gaji.toml` 파일 생성 없음 | 이후 승인 적용 완료 |
| `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:92`-`docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:93` | 이번 배치 생성 금지, 승인 후 반영 | 승인 반영 커밋 `9d94496` 확인 |

## 현재 Metadata

| package | 현재 적용 근거 | 주요 값 |
|---|---|---|
| `gaji/std_grid` | `gaji/std_grid/gaji.toml:1`, `gaji/std_grid/gaji.toml:4`, `gaji/std_grid/gaji.toml:6`, `gaji/std_grid/gaji.toml:7`, `gaji/std_grid/gaji.toml:9` | id=`gaji/std_grid`, ssot_requires=`>=20.1.22`, det_tier=`D-STRICT`, openness=`closed` |
| `gaji/std_input_map` | `gaji/std_input_map/gaji.toml:1`, `gaji/std_input_map/gaji.toml:4`, `gaji/std_input_map/gaji.toml:6`, `gaji/std_input_map/gaji.toml:7`, `gaji/std_input_map/gaji.toml:9` | id=`gaji/std_input_map`, ssot_requires=`>=20.1.22`, det_tier=`D-STRICT`, openness=`closed` |
| `gaji/std_physics_1d` | `gaji/std_physics_1d/gaji.toml:1`, `gaji/std_physics_1d/gaji.toml:4`, `gaji/std_physics_1d/gaji.toml:6`, `gaji/std_physics_1d/gaji.toml:7`, `gaji/std_physics_1d/gaji.toml:9` | id=`gaji/std_physics_1d`, ssot_requires=`>=20.2.26`, det_tier=`D-STRICT`, openness=`closed` |

## Proposal 초안과의 일치

`PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md`의 초안 값과 현재 파일 값은 일치한다.

| package | proposal 근거 | 현재 판정 |
|---|---|---|
| `gaji/std_grid` | `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:30`-`docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:38` | 일치 |
| `gaji/std_input_map` | `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:52`-`docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:60` | 일치 |
| `gaji/std_physics_1d` | `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:74`-`docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md:82` | 일치 |

## 검증

```text
python tests/run_gaji_metadata_3_applied_status_check.py
python tests/run_gaji_registry_pack_check.py
python tests/run_gaji_registry_strict_audit_check.py
python tests/run_gaji_registry_defaults_check.py
git status --short -- docs/ssot
```

## 남는 경계

- 이 보고서는 stale 상태 보정 문서다. `GAJI_REGISTRY_CLOSURE_V1`와 proposal 원문은 역사적 기록으로 둔다.
- 새 parser/runtime 문법, gaji registry product behavior, runtime `state_hash` 산식은 변경하지 않는다.
