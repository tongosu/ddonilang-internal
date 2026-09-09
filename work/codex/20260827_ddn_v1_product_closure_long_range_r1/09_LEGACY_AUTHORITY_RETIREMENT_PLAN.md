# legacy semantic authority retirement plan R1

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

| authority 후보 | 현 상태 | 목표 | 제거/이관 전 gate |
|---|---|---|---|
| `tools/teul-cli/src/lang/**` | 독립 lexer/parser 존재 | shared `lang` frontdoor로 MOVE/DROP | golden command inventory + parity |
| `tools/teul-cli/src/runtime/**` | 독립 runtime 존재 | shared runtime 또는 명시 adapter | command KEEP/MOVE/DROP + receipt parity |
| `tools/teul-cli/src/canon.rs` | 독립 lowering/canon | shared canon consumer | source/canon roundtrip corpus |
| `lang/src/currentline.rs` | 별도 regex/dispatch 역사 경로 | shared typed authority 또는 history-only | call-site·pack migration |
| `tool/src/preprocess.rs` | 일부 semantic lowering | shared frontdoor로 ownership 명시 | no harness-only lowering |
| `source_readiness.js` | strict JS source analysis | Rust V25 analysis 결과 consumer | FD01 actual Edge gate |
| Workbench renderer helpers | raw result 추론 가능성 | canonical view payload consumer only | semantic fallback mutations |

삭제는 이 프로그램에서 승인하지 않는다. inventory→migration→independent parity→successor removal 순서를 지킨다.
