# VC17 Owner Decision Binding R1

- 결속일: 2026-08-29
- 실행 goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` successor execution
- 결정 전달: `[Codex관리Work -> DDN V1제품마감Codex] DDN-P-V1-VC17-OWNER-DECISION-BINDING-R1 + 44 VALIDATION`
- 결속 parent: `363f3e15f1ca149cb6d630469d49782902ca5ef1`
- provider fixed source: `23f6087e1a932d9c813c485fa117c58da20e081c`
- current authority: internal SSOT v25.21.0 / RD-001~468, public Language SPEC v0.6.0 (read-only)

## Owner decisions

### OD-VC17-01

- 선택: `A / PURE_MINIMAL`
- 결속 상태: `VC17_PURE_MINIMAL_44_REQUIRED_CANDIDATE_BASELINE_BOUND`
- 의미: census의 44개 `V1_REQUIRED_CANDIDATE`를 검증 시작 기준으로 채택한다.
- 제한: 44개는 exact/final/public V1 membership이 아니다. VC01~VC16 직접 의존성, 최소 유용성 bundle, 적용 가능한 native/WASM/Workbench reachability 및 제품 근거를 검증한 뒤 별도 membership gate에서 판단한다.

### OD-VC17-02

- 선택: `B / LANGUAGE_CORE_COLLECTION_CONSTRUCTOR`
- 결속 상태: `VC12_COLLECTION_SEMANTIC_AUTHORITY_LANGUAGE_CORE_BOUND`
- 의미: collection constructor의 semantic role은 language core에 둔다.
- 제한: 현재 `차림` provider/export는 implementation custody/adapter로 보존한다. public spelling, alias, runtime arrangement와 migration/canon 결속은 OPEN이다.

## 보존된 OPEN

- Basic Tensor R1 actual provider/export: 0
- small Product/Sum/result minimum usefulness: GAP
- `채우기`: exact audit pending
- 44 candidates와 exact/final/public membership 사이의 검증 gate
- public executable/command membership와 Workbench default ingress
- release, activation, legal, Owner Human Smoke와 Human PASS

## Mutation boundary

이 결속은 product/test/pack/tracked-WASM/UI/SSOT/SPEC/public export/membership/release transition을 만들지 않는다. 기존 네 census 산출물은 byte-for-byte 보존한다.

## Anti-meta disposition

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: VC17 후보 검증에서 collection constructor를 stdlib membership으로 중복 계산하지 않고 44행을 실제 의존성 기준으로 분류할 수 있게 됨
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 0 (결속 단계)
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: YES
- `NEXT_PRODUCT_DECISION_ENABLED`: 검증된 exact V1 stdlib membership candidate를 관리/Owner에게 반환

## Nonclaims

`VC17_PURE_MINIMAL_44_REQUIRED_CANDIDATE_BASELINE_BOUND` 및 `VC12_COLLECTION_SEMANTIC_AUTHORITY_LANGUAGE_CORE_BOUND`만 결속한다. VC17/P1/V1 closure, exact membership, readiness, release, activation, legal 또는 Human PASS를 주장하지 않는다.
