# V1 release membership R1

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

| membership | count | authority |
|---|---|---|
| REQUIRED | 48 | provisional product-roadmap membership |
| OPTIONAL | 2 | provisional product-roadmap membership |
| DEFERRED | 4 | provisional product-roadmap membership |

## 중요한 경계

- authoritative SSOT V1 membership row: `0`
- 이 문서의 48/2/4 분류는 제품Chat Owner roadmap direction의 실행용 projection이다.
- readiness floor 계산에는 사용하지 않는다.
- OPTIONAL/DEFERRED는 V1 floor를 낮추지 않는다.
- REQUIRED blocker는 membership과 required closure gate OPEN의 교집합으로 파생한다.

## 즉시 blocker family

1. shared language/runtime authority와 official CLI identity
2. current V25 Workbench frontdoor 및 observation manifest
3. public projection self-containment와 private fixture 격리
4. public-source-only build와 clean install
5. license/notices/SBOM 및 권리 custody
6. 외부 사용자 검증과 V1 promotion
