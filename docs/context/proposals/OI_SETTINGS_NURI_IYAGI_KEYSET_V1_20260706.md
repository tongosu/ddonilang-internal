# OI_SETTINGS_NURI_IYAGI_KEYSET_V1_20260706

## 상태

- 분류: OPEN ISSUE / LANG / TOOLCHAIN / NURIGYM
- 작성: 2026-07-06
- 출처: Q36-3 / `BRIEF_SETTINGS_HEADER_ALIGNMENT_AND_LEGACY_PROPOSAL_DELTA_V1`
- 상태: docs-first. Closure claim 없음.
- 구현 범위: 없음. Parser/runtime 변경 금지.

## 배경

`설정 {}`의 8절 구조에는 `누리`와 `이야기`가 예약되어 있으나, 현재 key set은 닫혀 있지 않다.

- `설정.누리`: seed 등 누리 초기 메타 후보
- `설정.이야기`: 진입점과 흐름 메타 후보

이 OI는 key set v1을 확정하기 전의 질문 목록과 후보 표를 등록한다.

## Candidate Key 표

| 절 | 후보 key | 값 예 | 의미 | 열린 질문 |
|---|---|---|---|---|
| `설정.누리` | `시앗` | `42` | deterministic seed 후보. 실행 재현의 초기 seed를 나타낸다. | 철자는 `시앗`으로 둘지, 기존 한국어 감각의 `씨앗`으로 둘지 결정 필요. `InputSnapshot.rng_seed`와 같은 값인지, 별도 세계 seed인지 결정 필요. |
| `설정.누리` | `누리갈래` | `#따로누리` / `#함께누리` | 세계 실행 갈래 후보 | `설정.실행.차림새` preset이 이미 `누리갈래`를 산출하므로 중복 소유인지 override key인지 결정 필요. |
| `설정.이야기` | `들머리` | `첫장면` | 이야기/시뮬의 entry point 후보 | lifecycle entry seed/function과 어떻게 연결되는지 결정 필요. |

## `InputSnapshot.rng_seed`와의 관계 질문

현재 코드에는 `rng_seed`가 wire/runtime 구조에 존재한다.

| 위치 | 관찰 |
|---|---|
| `core/src/platform.rs` | `rng_seed` 필드가 platform snapshot/config 계열에 존재 |
| `solutions/seamgrim_ui_mvp/ui/wasm_ddn_types.d.ts` | `rng_seed`와 `set_rng_seed(seed)` 표면 존재 |
| `tools/teul-cli/tests/run_golden.py` | `env_id`를 command args로 넘기는 경로 존재 |

결정 질문:

1. `설정.누리.시앗`은 `InputSnapshot.rng_seed`의 언어 표면인가, 아니면 world init seed인가?
2. `InputSnapshot.rng_seed`가 외부 입력 봉인 기록이라면 `설정.누리.시앗`과 같은 값이어도 소유권을 분리해야 하는가?
3. `set_rng_seed(seed)` 같은 UI/WASM 표면은 언어 헤더 값을 소비해야 하는가, toolchain/UI 설정으로 남겨야 하는가?

## NuriGym schema mapping 질문

`nurigym.dataset_header.v0.1`의 `env_id / seed`는 다음 둘 중 하나로 정해야 한다.

| 선택지 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 언어 헤더 소유 | `env_id` 또는 일부 seed를 `설정.누리`에 둔다 | lesson/source만 보고 재현 메타를 읽기 쉽다 | dataset/toolchain metadata와 중복된다 |
| B. toolchain metadata 소유 | `env_id / seed`는 dataset header 또는 CLI metadata로 둔다 | wire schema와 toolchain 책임이 명확하다 | DDN source만으로는 gym 실행 정보를 다 알 수 없다 |

권고: `seed`는 언어/누리 소유 후보로 남기되, `env_id`는 우선 toolchain metadata에 둔다. `env_id`는 Gym adapter 식별자에 가까워 언어 핵심 key로 올리기에는 이르다.

## 용어 혼동 방지 문구 초안

> "누리 설정"은 설정 헤더 전체를 느슨하게 부르는 말이 아니라, `설정 { 누리 { ... }. }` 하위 절만 가리킨다. 전체 파일 메타는 그냥 `설정` 또는 `설정 헤더`라고 부른다.

## SSOT 반영 초안

```md
### OI-SETTINGS-NURI-IYAGI-KEYSET-01

`설정.누리`와 `설정.이야기`의 v1 candidate key set을 확정한다.

- 후보: `누리.시앗`, `누리.누리갈래`, `이야기.들머리`
- 질문: `시앗/씨앗` 철자, `InputSnapshot.rng_seed`와의 관계, `누리갈래`와 `설정.실행.차림새` preset의 중복 소유권, NuriGym `env_id/seed`의 언어 헤더 소유 여부
- 상태: docs-first / no parser-runtime closure
```

## DoD 확인

| DoD | 결과 |
|---|---|
| OI 항목 | `OI-SETTINGS-NURI-IYAGI-KEYSET-01` 초안 작성 |
| candidate key 표 | 완료 |
| 질문 목록 | 완료 |
| parser/runtime 변경 0건 | 충족 |
| 공통 불변 경계 | 코드/팩/SSOT/state_hash/runtime canonical name 변경 없음 |
