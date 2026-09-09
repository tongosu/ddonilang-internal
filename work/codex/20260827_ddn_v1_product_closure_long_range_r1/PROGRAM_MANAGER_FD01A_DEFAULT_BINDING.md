# DDN V1 프로그램 관리자 FD01A 기본 결정 결속

```text
PROGRAM_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
DECISION_ID: DDN-V1-PM-FD01A-BINDING-01
DECISION_CLASS: REVERSIBLE_INTERNAL_PRODUCT_VERTICAL
AUTHORITY_BASIS: DO_NOT_STOP_FOR_MINOR_DECISIONS
LIVE_INTERNAL_SSOT: v25.15.0
PUBLIC_LANGUAGE_SPEC: v0.5.0
```

FD01 준비도 감사는 현재 V25 공개 제품 ingress가 0이고, 셈그림 lesson 557개 중
V25 parser 통과가 0임을 확인했다. 전역 기본값 전환은 제품을 깨뜨리므로 승인하지
않는다. 반면 internal typed SourceEpoch routing은 공개 문법·wire·기본 동작을 바꾸지
않고 분석과 실행의 epoch drift를 막는 가역적 critical-path vertical이다.

따라서 프로그램 관리자의 승인된 추천 기본값으로 다음을 결속한다.

```text
DDN_V1_FD01_DIRECTION: OPTION_A_INTERNAL_TYPED_EPOCH_ROUTING
PRODUCT_IMPLEMENTATION_AUTHORIZED: YES_FD01A_INTERNAL_TYPED_VERTICAL_ONLY
GLOBAL_V25_DEFAULT_SWITCH_AUTHORIZED: NO
CONTENT_SNIFFING_AUTODETECT: FORBIDDEN
DEFAULT_PUBLIC_V25_INGRESS_CHANGE_AUTHORIZED: NO
PUBLIC_CLI_OR_ENV_EPOCH_SELECTOR_AUTHORIZED: NO
PUBLIC_WASM_EPOCH_WIRE_AUTHORIZED: NO
STABLE_SOURCE_EPOCH_WIRE_AUTHORIZED: NO
PUBLIC_EXAMPLE_COPY_AUTHORIZED: NO
V1_RELEASE_MEMBERSHIP_AUTHORIZED: NO
SSOT_CHANGE_AUTHORIZED: NO
PUBLIC_SPEC_CHANGE_AUTHORIZED: NO
UI_VISUAL_CHANGE_AUTHORIZED: NO
PUBLIC_ACTIVATION_AUTHORIZED: NO
```

## 구현 범위

1. internal typed SourceEpoch identity를 source analysis와 execution의 공통 입력으로 쓴다.
2. default/public path는 현 pre-V25 의미와 진단을 그대로 유지한다.
3. 테스트 또는 봉인된 internal bundled-project identity 한 개만 explicit V25로 도달시킨다.
4. missing/unknown/mismatch epoch는 fail-closed한다.
5. source bytes를 sniff하여 epoch를 추정하거나 다른 parser로 silent retry하지 않는다.
6. Rust 제품 경로가 의미 권위를 가지며 JS는 selector나 semantic fallback을 만들지 않는다.

## 구현 후보 경로

- `lang/src/lib.rs`
- `tool/src/ddn_runtime.rs`
- `tool/src/runtime_surface.rs`
- `tool/src/source_analysis.rs`
- `tool/src/wasm_api.rs`
- 필요할 때만 `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js`
- 필요할 때만 `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js`
- 전용 Rust/JS tests와 D-PACK
- 공식 절차로 재생성한 tracked WASM/manifest

실제 구현자는 최소 변경으로 범위를 더 좁힐 수 있지만, 테스트 전용 lowering으로 제품
연결을 대신할 수 없다. Workbench UI source는 internal contract 전달에 불가피한 경우만
수정하며 시각·문구·layout 변경은 금지한다.

## 완료 경계

- actual Rust product call graph 연결
- analysis/execution 동일 epoch identity
- default/pre-V25 regression
- explicit V25 positive와 mismatch/missing/unknown negative
- no fallback, no partial state/output/effect
- CLI/WASM 내부 경로 parity
- clean-detached A/B reproducibility
- fixed product/test HEAD와 독립검토 요청

구현자는 `PASS`, `CLOSED`, global V25 default, public stable wire, release membership,
activation, Human PASS를 주장하지 않는다.

