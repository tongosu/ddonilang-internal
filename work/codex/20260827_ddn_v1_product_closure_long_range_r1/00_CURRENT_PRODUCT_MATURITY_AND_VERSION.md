# 현재 제품 maturity와 네 버전축

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

## 판정

| 축 | 현재값 | 의미 |
|---|---|---|
| INTERNAL_SSOT_VERSION | `v25.15.0` | docs-first live current |
| DEVELOPMENT_MATURITY | `UNCLAIMABLE` | actual membership/gate가 아직 비어 있음 |
| PUBLIC_LANGUAGE_SPEC_VERSION | `v0.5.0` | 내부 SSOT와 별도 고정 계보 |
| PUBLIC_PRODUCT_VERSION | `UNRELEASED` | public release/activation/Human PASS 없음 |

제품Chat이 제시한 V1.0~V4+ 사다리는 승인된 product roadmap input이다. 그러나 live SSOT의 실제 V1 membership은 0행이므로 numeric floor를 계산하지 않는다. `V0.6`도 현재 제품판으로 선언하지 않는다.

## 현재 수치

- capability family: `54`
- provisional REQUIRED/OPTIONAL/DEFERRED: `48/2/4`
- full-capability IMPLEMENTED_VERIFIED: `0`
- IMPLEMENTED_UNVERIFIED/PARTIAL/NOT_IMPLEMENTED: `2/47/5`
- UNKNOWN: `0`

독립 PASS된 세부 slice는 evidence history로 보존하지만 더 넓은 capability 전체를 `IMPLEMENTED_VERIFIED`로 계산하지 않았다.
