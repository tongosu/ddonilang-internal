# Owner 결정 패킷 — 공식 CLI identity

## D1. 사용자에게 보이는 실행 파일 이름

### A. `ddonirang` — 추천

예:

```text
ddonirang run 작품.ddn
ddonirang check 작품.ddn
ddonirang view 작품.ddn
```

장점:

- 언어/제품 이름과 일치하고 `tool`, `teul` 같은 내부 역사 용어가 사라진다.
- CLI와 WASM을 “같은 제품의 두 실행 방식”으로 설명하기 쉽다.
- 장기 공개 문서가 깔끔하다.

단점:

- 새 binary alias, packaging, 문서, 스크립트 migration이 필요하다.
- 기존 사용자를 위해 `ddonirang-tool`과 `teul-cli` 호환 기간이 필요하다.

### B. `ddonirang-tool` 유지

장점: 현재 릴리스 산출물 이름을 유지해 변경량이 적다.

단점: 사용자 제품이라기보다 내부 도구처럼 보이고, 장기 명칭으로 덜 자연스럽다.

### C. `ddonirang-tool`과 `teul-cli` 영구 병존

장점: 단기 migration이 없다.

단점: 어느 쪽이 공식인지 계속 혼란스럽고 runtime drift 위험을 영구화한다. 비추천한다.

```text
RECOMMENDATION_D1: OPTION_A_PUBLIC_EXECUTABLE_DDONIRANG
```

## D2. semantic owner

### A. `lang` + `tool` shared product library — 추천

모든 frontend가 같은 parse/canon/runtime을 호출한다. CLI/WASM/Workbench parity를 구조적으로 만들 수 있다.

### B. teul-cli runtime을 공식 owner로 승격

기능은 많지만 private parser/runtime와 연구 명령이 거대하게 결합돼 있어 분리 비용과 공개 범위가 커진다.

```text
RECOMMENDATION_D2: OPTION_A_LANG_TOOL_SHARED_PRODUCT_AUTHORITY
```

## D3. V1 공개 CLI의 기본 명령군

### A. 작은 workflow 중심 표면 — 추천

후보: `run`, `check`, `test`, `canon`, `project`, `view`, `help`, `version`.

장점: 초심자가 이해하기 쉽고 conformance와 문서가 작다.

단점: 고급 기능은 별도 namespace 또는 internal tool이 필요하다.

### B. teul-cli 63개를 모두 공개

기능은 많지만 V1 membership, 안정성, 보안, 문서 의무가 폭증한다. 비추천한다.

```text
RECOMMENDATION_D3: OPTION_A_MINIMAL_USER_WORKFLOW_SURFACE
EXACT_COMMAND_MEMBERSHIP: OPEN_UNTIL_SSOT_OWNER_DECISION
```

## D4. 고급 명령 처리

### A. library + 정책 기반 namespace — 추천

예: 검증된 기능만 `ddonirang replay ...`로 노출하고 AI·학습·연구 기능은 internal package에 둔다.

### B. 모든 명령을 공식 CLI root에 평면 배치

탐색성과 호환성 비용이 커진다.

```text
RECOMMENDATION_D4: OPTION_A_SHARED_LIBRARY_POLICY_NAMESPACES
```

## D5. legacy binary 정책

### A. 단계적 alias·경고·제거 — 추천

`teul-cli`와 `ddonirang-tool`을 곧바로 삭제하지 않는다. 선택 명령 parity와 참조 migration이 독립 PASS를 받은 뒤 한정된 호환 기간을 둔다.

### B. 즉시 제거

팩·테스트·문서 참조가 매우 많아 안전하지 않다.

```text
RECOMMENDATION_D5: OPTION_A_STAGED_COMPATIBILITY_AND_RETIREMENT
```

## D6. crate 이름과 공개 binary 이름

### A. 처음에는 분리 — 추천

내부 crate `ddonirang-tool`은 당장 유지하고 공개 packaging에서 `ddonirang` binary를 추가한다. 소스 이동은 semantic convergence 이후 별도 과업으로 한다.

### B. crate와 binary를 동시에 전면 개명

깔끔하지만 대규모 경로·CI·문서 변경이 생겨 현재 병행 개발을 방해한다.

```text
RECOMMENDATION_D6: OPTION_A_PUBLIC_BINARY_ALIAS_FIRST
```

## D7. SSOT V1 membership

현재 v25.15.0의 authoritative V1 membership은 0행이다. 이 패킷의 추천 명령을 membership으로 간주하면 안 된다.

```text
RECOMMENDATION_D7: REQUEST_SEPARATE_SSOT_OWNER_MEMBERSHIP_SUCCESSOR
SSOT_CHANGE_AUTHORIZED: NO
```

## 권고 Owner 응답 형식

```text
DDN_V1_CLI_IDENTITY_DIRECTION: OPTION_A_PUBLIC_EXECUTABLE_DDONIRANG
DDN_V1_CLI_SEMANTIC_OWNER: OPTION_A_LANG_TOOL_SHARED_PRODUCT_AUTHORITY
DDN_V1_CLI_PUBLIC_SURFACE_DIRECTION: OPTION_A_MINIMAL_USER_WORKFLOW_SURFACE
DDN_V1_CLI_ADVANCED_COMMAND_POLICY: OPTION_A_SHARED_LIBRARY_POLICY_NAMESPACES
DDN_V1_CLI_LEGACY_POLICY: OPTION_A_STAGED_COMPATIBILITY_AND_RETIREMENT
DDN_V1_CLI_NAMING_MIGRATION: OPTION_A_PUBLIC_BINARY_ALIAS_FIRST
DDN_V1_CLI_SSOT_MEMBERSHIP: SEPARATE_SSOT_OWNER_SUCCESSOR_REQUIRED

PRODUCT_IMPLEMENTATION_AUTHORIZED: NO_UNTIL_EXACT_VERTICAL_PACKET
SSOT_CHANGE_AUTHORIZED: NO
PUBLIC_SPEC_CHANGE_AUTHORIZED: NO
PUBLIC_RELEASE_AUTHORIZED: NO
```
