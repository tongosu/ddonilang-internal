# EX01 Owner 결정 패킷

## A — 선택된 네 후보를 migration 원장으로 승인 — 추천

```text
PC01
HELLO
GRID_CURRENT
TENSOR
```

장점: 첫 실행, 언어 핵심, 자료 계산, Workbench 시각 결과를 작은 집합으로 덮는다.
각 workflow를 독립 검증할 수 있고 557개 전체 migration 때문에 critical path가 멈추지 않는다.

단점: 권리·Basic Tensor R1·native grid result·FD01 typed routing이 각각 선행한다.

## B — public SPEC v0.5.0 예제 7개를 그대로 제품 membership으로 사용 — 비추천

장점: 이미 공개된 경로를 쓸 수 있다.

단점: V25 제품 parser `0/7`, pre-V25도 `1/7`뿐이다. docs-first 예제를 product PASS로
오인하게 되고 stable SPEC가 제품보다 앞서는 상태를 고착한다.

## C — lesson 557개 전부 migration 뒤 예제 선택 — 비추천

장점: migration 완료 뒤 혼합 corpus가 줄어든다.

단점: 역사·실험·제품 파일을 한 gate로 묶고 V1 첫 사용자 workflow를 장기간 막는다.

## 추천 응답

```text
DDN_V1_EX01_DIRECTION: OPTION_A_SELECTED_FOUR_MIGRATION_CANDIDATES
PROPOSED_MIGRATION_IDS: PC01,HELLO,GRID_CURRENT,TENSOR
V1_RELEASE_MEMBERSHIP_AUTHORIZED: NO
PUBLIC_SPEC_V050_EXAMPLES: DOCS_FIRST_NOT_EXECUTABLE_PRODUCT_MEMBERS
PROJECTILE_DISPOSITION: TIER_2_AFTER_CORE_AND_RIGHTS
RIGHTS_AUDIT_REQUIRED_BEFORE_PUBLIC_COPY: YES
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO_UNTIL_FD01_AND_RIGHTS_GATES
```

이 승인은 후보·순서를 고정할 뿐 release membership, public copy, SSOT/SPEC 변경,
stable wire, activation을 허용하지 않는다.

