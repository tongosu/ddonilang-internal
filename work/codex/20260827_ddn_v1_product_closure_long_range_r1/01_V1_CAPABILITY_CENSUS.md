# V1 capability census R1

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

| ID | 이름 | V1 | 제품 상태 | 첫 목표 | 필수화 | 경계 |
|---|---|---|---|---|---|---|
| V1-C001 | 한국어 기본 원문 표면 | REQUIRED | PARTIAL | V1.0 | V1.0 | Workbench strict JS 분석과 Rust V25 frontdoor가 아직 수렴하지 않았다. |
| V1-C002 | Definition `:=` | REQUIRED | IMPLEMENTED_UNVERIFIED | V1.0 | V1.0 | PC01 FU01 local evidence는 있으나 fresh plain PASS가 대기 중이다. |
| V1-C003 | Binding/Rebinding `<-` | REQUIRED | PARTIAL | V1.0 | V1.0 | native/WASM current rejection parity와 전체 Workbench 성공은 별개다. |
| V1-C004 | 기본 값·자료형·정체성 | REQUIRED | PARTIAL | V1.0 | V1.0 | lang/tool/teul의 중복 모델을 shared authority로 더 수렴해야 한다. |
| V1-C005 | 정확수·결정적 수치 | REQUIRED | PARTIAL | V1.0 | V1.0 | 복수 구현과 전체 public conformance가 남아 있다. |
| V1-C006 | 글·바이트·NFC | REQUIRED | PARTIAL | V1.0 | V1.0 | 전체 frontdoor와 import/export byte custody 검증이 필요하다. |
| V1-C007 | Product | REQUIRED | PARTIAL | V1.0 | V1.0 | field access scoped PASS를 Product 전체 closure로 확대하지 않는다. |
| V1-C008 | Sum·선택값·typed result | REQUIRED | PARTIAL | V1.0 | V1.0 | docs-first 의미와 physical product coverage를 분리한다. |
| V1-C009 | 이름 있는 callable | REQUIRED | PARTIAL | V1.0 | V1.0 | ResultPlace와 generic callable 전체 제품 수직은 OPEN이다. |
| V1-C010 | 익명 callable | REQUIRED | PARTIAL | V1.0 | V1.0 | exact parser/runtime/Workbench product evidence가 부족하다. |
| V1-C011 | ResultPlace | REQUIRED | PARTIAL | V1.0 | V1.0 | docs-first live 의미이고 일반 block tail·generic return은 범위 밖이다. |
| V1-C012 | 조건·반복 | REQUIRED | PARTIAL | V1.0 | V1.0 | ForEach/current-item scoped PASS는 보존하되 control-flow 전체 PASS로 확대하지 않는다. |
| V1-C013 | bounded recursion | REQUIRED | PARTIAL | V1.0 | V1.0 | public standard profile과 전체 callable recursion 검증이 필요하다. |
| V1-C014 | 기본 generic | REQUIRED | PARTIAL | V1.0 | V1.0 | K1 일부만 PARTIAL이며 K0 이후 behavior closure가 필요하다. |
| V1-C015 | 구실·골라부름 | REQUIRED | PARTIAL | V1.0 | V1.0 | stable public identity/wire는 OPEN이며 limited product evidence만 보존한다. |
| V1-C016 | 기본 collection | REQUIRED | PARTIAL | V1.0 | V1.0 | collection family별 public conformance inventory가 필요하다. |
| V1-C017 | typed Selection | REQUIRED | PARTIAL | V1.0 | V1.0 | docs-first selection 의미와 executable oracle 사이 gap이 남아 있다. |
| V1-C018 | Basic Tensor R1 | REQUIRED | PARTIAL | V1.0 | V1.0 | executable oracle와 native/WASM/Workbench parity가 OPEN이다. |
| V1-C019 | 한국어 활용형 | REQUIRED | PARTIAL | V1.0 | V1.0 | 형태 분석과 callable resolution의 단일 authority 수렴이 필요하다. |
| V1-C020 | 닫힌 여러표면·canon | REQUIRED | PARTIAL | V1.0 | V1.0 | formatter와 teul canon 중복 authority가 남아 있다. |
| V1-C021 | 모듈·여러 파일 | REQUIRED | PARTIAL | V1.0 | V1.0 | fresh public-source build와 Workbench current frontdoor를 함께 검증해야 한다. |
| V1-C022 | 프로젝트 정체성 | REQUIRED | PARTIAL | V1.0 | V1.0 | official server revision과 local fallback identity를 분리해야 한다. |
| V1-C023 | dependency identity | REQUIRED | PARTIAL | V1.0 | V1.0 | 외부 resolver/public registry 없이 local 범위만 우선 닫는다. |
| V1-C024 | local dependency·lock | REQUIRED | PARTIAL | V1.0 | V1.0 | exact public lock schema와 외부 해소는 OPEN이다. |
| V1-C025 | 기본 stdlib | REQUIRED | PARTIAL | V1.0 | V1.0 | V1 membership이 비어 있어 stdlib 필수 목록도 아직 provisional이다. |
| V1-C026 | 결정적 실행 | REQUIRED | PARTIAL | V1.0 | V1.0 | 여러 scoped PASS가 있으나 V1 required closure gate는 미정이다. |
| V1-C027 | state/result hash | REQUIRED | PARTIAL | V1.0 | V1.0 | CLI/WASM/Workbench 전체 schema/wire가 stable하지 않다. |
| V1-C028 | receipt·replay | REQUIRED | PARTIAL | V1.0 | V1.0 | RD-207 exact stable wire는 OPEN이다. |
| V1-C029 | 외부 입력 sealing | REQUIRED | PARTIAL | V1.0 | V1.0 | 입력 source별 physical adapter conformance가 필요하다. |
| V1-C030 | silent semantic fallback 금지 | REQUIRED | PARTIAL | V1.0 | V1.0 | 각 frontdoor별 mutation evidence를 계속 유지해야 한다. |
| V1-C031 | shared 언어·runtime authority | REQUIRED | PARTIAL | V1.0 | V1.0 | teul-cli와 Workbench JS의 독립 semantic authority가 남아 critical path다. |
| V1-C032 | official CLI | REQUIRED | PARTIAL | V1.0 | V1.0 | tool과 teul-cli의 public identity/KEEP-MOVE-DROP가 미결정이다. |
| V1-C033 | Native adapter | REQUIRED | PARTIAL | V1.0 | V1.0 | host capability와 semantic state의 분리 conformance가 필요하다. |
| V1-C034 | WASM path | REQUIRED | PARTIAL | V1.0 | V1.0 | A/B/tracked identity는 slice 증거이며 전체 V1 WASM surface closure가 아니다. |
| V1-C035 | RuntimeBridge | REQUIRED | PARTIAL | V1.0 | V1.0 | T1 구조는 있으나 current V25 positive source가 shared strict analysis에서 실패한다. |
| V1-C036 | HostBridge | REQUIRED | PARTIAL | V1.0 | V1.0 | official server API와 local fallback을 구분한 end-to-end gate가 필요하다. |
| V1-C037 | Common Workbench | REQUIRED | PARTIAL | V1.0 | V1.0 | current runtime success와 exact server revision reopen이 OPEN이다. |
| V1-C038 | renderer-independent canonical view | REQUIRED | PARTIAL | V1.0 | V1.0 | T5 family scoped PASS를 current T5F grid successor로 확대하지 않는다. |
| V1-C039 | project save·reopen | REQUIRED | PARTIAL | V1.0 | V1.0 | local fallback PASS와 official server revision closure를 분리한다. |
| V1-C040 | import·export 최소선 | REQUIRED | PARTIAL | V1.0 | V1.0 | stable public wire는 OPEN이고 current format은 experimental/versioned다. |
| V1-C041 | 기본 diagnostics | REQUIRED | PARTIAL | V1.0 | V1.0 | stable diagnostic wire와 Workbench structured propagation 일부가 OPEN이다. |
| V1-C042 | pre-v25 migration | REQUIRED | IMPLEMENTED_UNVERIFIED | V1.0 | V1.0 | PC01와 G14 fresh independent verdict를 기다린다. |
| V1-C043 | public source projection | REQUIRED | PARTIAL | V1.0 | V1.0 | A/B tree 결정성은 확인됐지만 self-containment와 private path preflight가 FAIL이다. |
| V1-C044 | public-source-only release build | REQUIRED | NOT_IMPLEMENTED | V1.0 | V1.0 | private include와 browser offline dependency 때문에 현재 FAIL이다. |
| V1-C045 | clean-machine install·run | REQUIRED | NOT_IMPLEMENTED | V1.0 | V1.0 | sealed offline browser/package custody가 없다. |
| V1-C046 | license·notice·SBOM | REQUIRED | NOT_IMPLEMENTED | V1.0 | V1.0 | Apache-2.0은 후보일 뿐이며 PC01/projectile public copy는 0이다. |
| V1-C047 | public conformance | REQUIRED | PARTIAL | V1.0 | V1.0 | private/rights-blocked fixture 격리 정책이 필요하다. |
| V1-C048 | 글무늬·Regex | OPTIONAL | PARTIAL | V1.0 | V1.5 | V1 floor에는 포함하지 않고 V1.5 필수화 후보로 유지한다. |
| V1-C049 | 기본 Proof·보임 | OPTIONAL | PARTIAL | V1.0 | V2.0 | pack 존재를 V1 제품 closure로 계산하지 않는다. |
| V1-C050 | State Machine | DEFERRED | PARTIAL | V2.0 | V2.5 | V2.5 REQUIRED 후보이며 V1 floor에서 제외한다. |
| V1-C051 | AI 협업 surface | DEFERRED | PARTIAL | V3.0 | V3.5 | 말힘누리·AI 제안 provenance는 별도 트랙이며 V1 floor가 아니다. |
| V1-C052 | 부분·완전 self-hosting | DEFERRED | NOT_IMPLEMENTED | V1.8 | V4_PLUS | 부분 self-hosting은 앞당길 수 있으나 완전 self-hosting은 V4+ 후보다. |
| V1-C053 | 세계·결정적 simulation | DEFERRED | PARTIAL | V2.5 | V2.8 | legacy/experimental 구현을 V1 contract로 계산하지 않는다. |
| V1-C054 | V0.9 외부 사용자 검증·V1 승격 | REQUIRED | NOT_IMPLEMENTED | V1.0 | V1.0 | external_user_success_count는 0이며 Human PASS도 없다. |

전체 필드는 `v1_capability_registry.detjson`이 소유한다. 이 표의 membership은 SSOT 표가 아니라 Owner product-roadmap input이다.
