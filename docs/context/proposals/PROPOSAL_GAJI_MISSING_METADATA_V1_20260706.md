# PROPOSAL: 가지 metadata 누락 후보 3건

작성: 2026-07-07 KST  
범위: `std_grid`, `std_input_map`, `std_physics_1d`의 `gaji.toml` 초안 제안  
경계: 실제 `gaji.toml` 파일 생성 없음. `docs/ssot/**` 수정 없음.

## 요약

`docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md`는 세 디렉터리를 metadata 없는 실제 package 후보로 분류했다.

| 후보 | 기존 분류 근거 | 현 파일 근거 | 판정 |
|---|---|---|---|
| `gaji/std_grid` | `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:73`, `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:94` | `gaji/std_grid/ddn/exports.ddn:1`, `gaji/std_grid/README.md:5` | `gaji.toml` 제안 대상 |
| `gaji/std_input_map` | `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:74`, `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:94` | `gaji/std_input_map/ddn/exports.ddn:1`, `gaji/std_input_map/README.md:5` | `gaji.toml` 제안 대상 |
| `gaji/std_physics_1d` | `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:75`, `docs/context/reports/GAJI_REGISTRY_CLOSURE_V1.md:94` | `gaji/std_physics_1d/ddn/exports.ddn:1`, `gaji/std_physics_1d/README.md:5` | `gaji.toml` 제안 대상 |

기존 metadata-bearing package는 `version = "0.1.0"`, `det_tier = "D-STRICT"`, `openness = "closed"`를 반복 사용한다. 표준 가지 계열 예시는 `gaji/std_math/gaji.toml:1`, `gaji/std_math/gaji.toml:3`, `gaji/std_math/gaji.toml:4`, `gaji/std_math/gaji.toml:7`, `gaji/std_math/gaji.toml:8`이다. AGE3 계열 minimum 예시는 `gaji/bogae/space2d/gaji.toml:4`, `gaji/phys/pendulum/gaji.toml:4`이다.

## 1. `gaji/std_grid`

### 근거

- 공개 surface 파일은 `격자.*` export를 가진다: `gaji/std_grid/ddn/exports.ddn:1`-`gaji/std_grid/ddn/exports.ddn:9`.
- README는 표준 격자 가지와 공개 API를 명시한다: `gaji/std_grid/README.md:1`, `gaji/std_grid/README.md:5`-`gaji/std_grid/README.md:14`.
- 경계는 정수 좌표, row-major, BFS 순서, view artifact 분리를 명시한다: `gaji/std_grid/README.md:18`-`gaji/std_grid/README.md:22`.

### 초안

```toml
id = "gaji/std_grid"
name = "표준 격자 가지"
version = "0.1.0"
ssot_requires = ">=20.1.22"

det_tier = "D-STRICT"
openness = "closed"

description = "정수 격자 world/state helper"
```

## 2. `gaji/std_input_map`

### 근거

- 공개 surface 파일은 `입력사상.*` export를 가진다: `gaji/std_input_map/ddn/exports.ddn:1`-`gaji/std_input_map/ddn/exports.ddn:4`.
- README는 InputSnapshot 기반 입력 해석 surface와 공개 API를 명시한다: `gaji/std_input_map/README.md:1`, `gaji/std_input_map/README.md:3`, `gaji/std_input_map/README.md:5`-`gaji/std_input_map/README.md:9`.
- 경계는 InputSnapshot truth, replay-safe helper, UI direct mutation 금지를 명시한다: `gaji/std_input_map/README.md:13`-`gaji/std_input_map/README.md:15`.

### 초안

```toml
id = "gaji/std_input_map"
name = "표준 입력사상 가지"
version = "0.1.0"
ssot_requires = ">=20.1.22"

det_tier = "D-STRICT"
openness = "closed"

description = "InputSnapshot 기반 입력 해석 helper"
```

## 3. `gaji/std_physics_1d`

### 근거

- 공개 surface 파일은 `물리1d.*` export를 가진다: `gaji/std_physics_1d/ddn/exports.ddn:1`-`gaji/std_physics_1d/ddn/exports.ddn:4`.
- README는 AGE3 확장용 1차원 운동/충돌 helper와 공개 API를 명시한다: `gaji/std_physics_1d/README.md:1`, `gaji/std_physics_1d/README.md:3`, `gaji/std_physics_1d/README.md:5`-`gaji/std_physics_1d/README.md:9`.
- 경계는 무차원 `dt`/질량, 단위 차원 일치, 진자와의 역할 분리를 명시한다: `gaji/std_physics_1d/README.md:13`-`gaji/std_physics_1d/README.md:15`.

### 초안

```toml
id = "gaji/std_physics_1d"
name = "표준 1D 물리 가지"
version = "0.1.0"
ssot_requires = ">=20.2.26"

det_tier = "D-STRICT"
openness = "closed"

description = "1차원 운동/충돌 helper"
```

## 결정 필요

- `std_input_map`의 `ssot_requires`를 표준 가지 계열(`>=20.1.22`)로 둘지, InputSnapshot 도입 milestone에 맞춰 더 높은 하한으로 올릴지는 승인 시 확인 필요하다. 이 proposal은 기존 표준 가지 metadata와의 일관성을 우선해 `>=20.1.22`를 초안으로 둔다.
- `std_physics_1d`는 README가 AGE3 확장이라고 명시하므로 `>=20.2.26`을 제안한다. 실제 SSOT 하한이 별도로 확정되어 있으면 승인 단계에서 바꾼다.

## 적용 금지/다음 단계

- 이번 배치에서는 `gaji/std_grid/gaji.toml`, `gaji/std_input_map/gaji.toml`, `gaji/std_physics_1d/gaji.toml`을 생성하지 않는다.
- 사용자 승인 후에만 위 초안을 실제 package root에 반영한다.
