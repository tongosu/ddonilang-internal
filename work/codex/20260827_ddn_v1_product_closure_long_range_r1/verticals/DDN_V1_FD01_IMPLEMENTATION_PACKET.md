# DDN-V1-FD01 실행 패킷

```text
PROGRAM_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
SSOT_ALL: v25.15.0 / b51fc82e5b922b14e10e48e733f0398d85f4d0b9cb22477ac10e08cef19e3777
SSOT_ALL_MANIFEST_SHA256: f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4
WORKSPACE_BUNDLE: v24.35.1_20260813_gaji-resolution-lock-v1-candidate-r3 / 97f6554c24d0b2a89aeb3190a5febdde4230498ebdc4156c643d8fd8a969ba9f
PUBLIC_LANGUAGE_SPEC: v0.5.0
PROGRAM_BASELINE: daabc1188d164888d7c3280588c0dbb5328bb5b6
VERIFIED_PRODUCT_FLOOR: UNCLAIMABLE
AUTHORITATIVE_V1_MEMBERSHIP_ROWS: 0
```

VERTICAL_ID: `DDN-V1-FD01`

## 목적

current V25 shared frontdoor와 Workbench observation convergence

## 허용 경로

lang/src/frontdoor.rs; tool/src/source_analysis.rs; tool/src/wasm_api.rs; solutions/seamgrim_ui_mvp/ui/workbench/source_readiness.js; workbench.js

## authoritative contract

Rust V25 frontdoor가 source analysis와 execution을 소유하고 Workbench는 canonical observation manifest만 소비한다.

## 선행·금지 경계

PC01/G14 targeted verdict 또는 정확한 unaffected 판정; UI redesign 0; new syntax 0; stable wire 0

## DoD

1. 실제 제품 source가 공통 frontdoor 또는 명시된 공개 subset을 통과한다.
2. positive·negative·migration·determinism regression을 갖는다.
3. silent fallback mutation이 RED가 된다.
4. native/WASM/Workbench 해당 범위 parity를 실제 입력으로 검증한다.
5. fixed product/test HEAD와 문서 전용 handoff commit을 분리한다.
6. 독립검토 전 PASS/CLOSED를 주장하지 않는다.

## failure disposition

두 번의 좁은 local correction 뒤에도 같은 blocker면 exact owner/authority packet으로 전환한다. 다른 safe slice는 계속한다.
