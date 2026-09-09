# DDN-V1-FD01A 후속 구현 패킷

## 상태

```text
PACKET_ID: DDN-V1-FD01A-INTERNAL-TYPED-SOURCE-EPOCH-VERTICAL-W1
STATUS: READY_AFTER_EXACT_OWNER_APPROVAL
BASELINE: FD01 audit handoff commit to be fixed
PRODUCT_IMPLEMENTATION_STARTED: NO
```

## 목표

전역 기본 parser를 바꾸지 않고, internal typed `SourceEpoch` 선택이 source analysis와
execution에 동일하게 전달되는 첫 수직 경로를 구현한다. 선택된 test fixture 또는
bundled project 한 개만 V25 경로로 도달시키고 기존 기본 경로는 그대로 둔다.

## 허용 후보 경로

- `lang/src/lib.rs` 및 필요한 shared typed epoch 경계
- `tool/src/ddn_runtime.rs`
- `tool/src/runtime_surface.rs`
- `tool/src/source_analysis.rs`
- `tool/src/wasm_api.rs`
- `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js`
- `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js`
- `solutions/seamgrim_ui_mvp/ui/workbench/source_readiness.js`
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`
- 이 vertical 전용 Rust/JS test, D-PACK, tracked WASM/manifest

실제 write 전에 path ownership과 current hash를 다시 고정한다. UI 파일은 contract 전달에
필요할 때만 수정하며, 시각 디자인이나 사용자 문구 변경은 허용하지 않는다.

## G0~G10

| Gate | 내용 |
|---|---|
| G0 | live SSOT/SPEC, baseline, dirty-root, protected resource 재감사 |
| G1 | Owner 응답 exact 결속; historical PC02 비권위 재확인 |
| G2 | SourceEpoch identity와 analysis/execution 공통 입력 계약 테스트 먼저 RED |
| G3 | internal typed current/migration entrypoint 최소 구현 |
| G4 | source analysis를 동일 explicit epoch에 연결 |
| G5 | WASM/RuntimeBridge bundled-project 경로에 explicit epoch 전달 |
| G6 | 선택된 V25 fixture 1개 end-to-end CLI/WASM/Workbench 연결 |
| G7 | default empty/pre-V25 경로와 557 corpus 무변경 회귀 |
| G8 | fault injection, stale epoch, mismatch, missing metadata, fallback 0 |
| G9 | clean-detached A/B build, tracked WASM identity, actual Edge cycle |
| G10 | fixed HEAD와 독립검토 요청 결속; self-PASS 금지 |

## 필수 불변식

- source analysis epoch = execution epoch
- source bytes alone do not select epoch
- missing/unknown/mismatch metadata fails closed
- default public V25 ingress remains 0 unless 별도 Owner gate가 열림
- pre-V25 historical source 의미와 진단 무변경
- partial state/output/effect 0 on failure
- JS syntax/semantic synthesis 0
- public source epoch stable wire 0

## 금지

```text
GLOBAL_V25_DEFAULT_SWITCH
CONTENT_SNIFFING_SOURCE_EPOCH_AUTODETECT
BLIND_CHERRY_PICK_04566a24
PUBLIC_CLI_OR_ENV_EPOCH_FLAG
PUBLIC_WASM_STABLE_EPOCH_PARAMETER
UI_REDESIGN
SSOT_OR_PUBLIC_SPEC_EDIT
ACTIVATION_OR_DEPLOYMENT
```

