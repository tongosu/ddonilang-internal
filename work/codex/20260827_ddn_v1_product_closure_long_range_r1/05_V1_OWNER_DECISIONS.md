# V1 Owner 결정 대장 R1

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

## 이미 승인된 product-program 방향

- 네 버전축 분리
- V1.0~V4+ maturity ladder
- V1 provisional REQUIRED/OPTIONAL/DEFERRED 방향
- V0.9 external-user validation before V1.0
- minor reversible choice는 manager가 계속 진행

## OWNER_FINAL_DECISION_REQUIRED

| 결정 | 추천 | 장점 | 비용/위험 |
|---|---|---|---|
| actual SSOT V1 membership·required gate 승격 | census 독립검토 후 정본관리Work successor | readiness floor를 계산 가능 | 현 Wave에서는 아직 승격 불가 |
| official CLI identity | `tool` shared CLI를 공식으로, teul-cli는 KEEP/MOVE/DROP 감사 후 이관 | native/WASM authority 수렴 | compatibility inventory 필요 |
| Workbench current frontdoor | Rust V25 frontdoor + canonical observation manifest | JS 의미 재해석 제거 | 실제 UI/runtime integration vertical 필요 |
| public fixture isolation | 권리 확인 public conformance subset + internal feature-gated tests | 공개 tree self-contained | test layout 조정 필요 |
| stable wire/diagnostics | V1 RC 직전 별도 freeze | 조기 호환 부채 방지 | RC 전까지 experimental label 유지 |
| final license | Apache-2.0 우선 후보, rights audit 뒤 확정 | 공개 기여에 명확 | assets/third-party audit 필요 |

결정에 의존하지 않는 inventory·test isolation 설계·KEEP/MOVE/DROP 감사는 계속한다.
