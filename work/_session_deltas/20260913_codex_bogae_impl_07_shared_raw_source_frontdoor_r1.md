# [진도개척 Work -> 또니랑 개발 관리자] BOGAE-IMPL-07 shared raw-source frontdoor R1 — 개발 결과

## 범위와 권위

- 실행 시점 live SSOT: `v25.84.0 / RD-001~626`
- live aggregate SHA-256: `51cba85bb6aaf7e977d23b9dcf5b7c94352f5ef402724addb5c4dbb99bcf872c`
- 공개 Language SPEC: `v0.7.0`
- predecessor handoff: `27399ef8965f9a1734e3c059eb40b826fc4947bb`
- BOGAE-IMPL-01/04/05/06은 재개방하지 않았다.
- 독립검토는 이 개발 batch에서 실행하지 않았다.

## 제품 target

- product commit: `bbb72b4e7e565a978a29f6ddb38c90f24f4ca325`
- product tree: `6ec87422a266780bb6d9e2caf8c763e3fb9be091`
- product parent: `27399ef8965f9a1734e3c059eb40b826fc4947bb`
- author/committer: `tongosu <tongosu@myarts.kr>`
- merge count: `0`

제품 및 검증 경로:

- `solutions/seamgrim_ui_mvp/ui/runtime/ddn_preprocess.js`
- `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js`
- `tests/seamgrim_bogae_shared_frontdoor_runner.mjs`
- `tests/seamgrim_execution_mode_preprocessed_surface_runner.mjs`
- `tool/src/wasm_api.rs`
- `tools/teul-cli/src/cli/run.rs`

## 구현 결과

- current 실행 모드는 입력 문자열을 정규화하거나 고쳐 쓰지 않고 원문 바이트를 Rust 공통 parser/type/canon frontdoor로 전달한다.
- 기존 JavaScript source migration은 명시적 `legacy-migration` 모드에서만 사용할 수 있다.
- 알 수 없는 source mode는 `E_DDN_SOURCE_MODE_UNSUPPORTED`로 fail-closed한다.
- Workbench WASM handle은 기본적으로 current mode를 사용하며, 원문 보존 여부와 mode를 debug provenance에 남긴다.
- CLI와 WASM profile 검사는 CRLF 원문의 exact SHA-256/byte identity가 보존됨을 확인한다.
- retired source의 자동 변환은 current 경로에서 0이다.
- SSOT, 공개 SPEC, public semantic identity, default execution authority 변경은 0이다.

## 고정 파일 identity

| path | Git blob | SHA-256 |
|---|---|---|
| `solutions/seamgrim_ui_mvp/ui/runtime/ddn_preprocess.js` | `729e68f1fb6fa4c875eb22cdc8d1a084b6fa04b9` | `F6D9D75BB647FBAFAAFE59663BBC7032F88860E4A8FBCB119A483D64958E27CC` |
| `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js` | `00c726cfc652cd7079db69f9b67222fdd768d076` | `263CE7ED6ACFC509C3A9F36B157EB63964A4B854BB4D73325C33B7FFB7FEFA89` |
| `tests/seamgrim_bogae_shared_frontdoor_runner.mjs` | `4b71628866b42e8070f871a81881aae5928bcbdf` | `14412F537451FC4589DB59A43CC210EF630437E54ABF31B9EFC009DBD6C92387` |
| `tests/seamgrim_execution_mode_preprocessed_surface_runner.mjs` | `d069e5a89b2c92a3e9bfbaf99e73b321f4c5798a` | `B7E9D5039EAC4B1F66FD426A6184CC608BEBD7EF38998E1C9CC2F3C18115F728` |
| `tool/src/wasm_api.rs` | `304f87f0f395d6ec2176682ec97729c7294bcba4` | `824B86CB7D7005BAA3F6669DBD2DACCB11F73E6781862EAED8DD02F3F789A19F` |
| `tools/teul-cli/src/cli/run.rs` | `1fc630d800a2fbba6ed4c5fe04238e7456c6c78c` | `A7F0C51D0E15E219E338997735205452770EAA56422B27B471DC7120085AD989` |

## 검증

- `node tests/seamgrim_bogae_shared_frontdoor_runner.mjs`: PASS
- `node tests/seamgrim_execution_mode_preprocessed_surface_runner.mjs`: PASS
- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS
- `node tests/seamgrim_ui_common_runner.mjs`: PASS
- CLI supported-profile exact source test: PASS `1/1`
- WASM V25 profile update exact source test: PASS `1/1`
- WASM-target shared library check: PASS
- `git diff --check`: PASS
- 공통 tool library 전체 회귀: `662 PASS / 39 FAIL`

39 failures는 이 target 이전에도 알려진 AI prompt golden, async receive/dispatch, project-authoring, legacy canon 경로의 묶음이다. 이번 변경 경로의 focused gate와 직접 관련된 신규 실패는 관찰되지 않았다. 전체 회귀 자체는 GREEN으로 주장하지 않는다.

비-WASM 호스트에서 `wasm_bindgen::JsValue` 오류 문자열을 직접 관찰하는 초안 test는 host가 `JsValue::from_str`을 지원하지 않아 abort했다. 해당 잘못된 test는 product 고정 전에 제거했고, 제품 실패로 분류하지 않았다. source-built WASM 대상 컴파일과 적용 가능한 profile 검사는 통과했다.

## mutation

각 mutation은 단독 적용했다.

1. current source를 legacy preprocessor로 우회: 원문 byte-preservation assertion RED, exit `1`.
2. Workbench handle 기본 mode를 legacy migration으로 변경: current handle raw-source assertion RED, exit `1`.
3. unknown `auto` mode를 허용: fail-closed assertion RED, exit `1`.

세 변이를 위 표의 exact blob/SHA-256으로 복구한 뒤 focused runner GREEN과 diff check PASS를 재확인했다.

## 비주장 및 다음 단계

- `PASS_TARGET_BOUND`, `CLOSED_TARGET_BOUND`, whole Bogae/Workbench, V1 readiness, release, Human PASS를 주장하지 않는다.
- public provider integration, BOGAE hash matrix, full-headless lifecycle, browser Human smoke는 이 target 범위가 아니다.
- 다음 정확한 단계는 clean independent reviewer가 product `bbb72b4e7e565a978a29f6ddb38c90f24f4ca325`와 이 handoff를 target-bound 검토하는 것이다.
- writer 상태: `PRODUCT_FIXED_PENDING_BATCH_INDEPENDENT_REVIEW`.
- push: `NO`.
