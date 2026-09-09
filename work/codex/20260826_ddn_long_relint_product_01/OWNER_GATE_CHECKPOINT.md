# DDN-LONG-RELINT-PRODUCT-01 Owner gate checkpoint R2

G0~G7과 독립적인 G18~G24 audit는 완료됐다. G8 product integration은 다음 exact 결정
전 시작할 수 없다.

## 선행 교정 — whole-HEAD baseline 금지

`905efb4a...` 또는 `fab6315c...`를 그대로 structural product baseline으로 쓰라는
이전 권고는 철회한다. 두 commit에 PC-02 pending-review 제품 commit `04566a24...`이
포함되기 때문이다. 또한 T5와 W1의 closed scopes 모두 fixed point 이전 prerequisite
bytes에 의존한다.

## 결정 1 — feature membership과 prerequisite inheritance

권고:

```text
INCLUDE: T5B~T5I closed canonical View scope
INCLUDE_OR_EXPLICIT_DEPENDENCY: R10/T1/T2/T4 prerequisite bytes used by reviewed T5 baseline
INCLUDE: PC-01 Owner-attested closed scope, if no-local-review-artifact custody is accepted
EXCLUDE: PC-02 04566a24... pending independent review
INCLUDE: W1-A/W1-B/W1-C1/W1DF/W1C2 I1/I2 reviewed closed scopes and required baseline bytes
DEFER: MATH-PHYS dirty/unbound
```

승인 literal 제안:

```text
D1_FEATURE_MEMBERSHIP: INCLUDE_REVIEWED_T5_PC01_W1_SCOPES_WITH_EXPLICIT_PREREQUISITES_EXCLUDE_PC02
D1_T5_PREREQUISITE_DISPOSITION: ACCEPT_AS_REVIEWED_T5_BASELINE_DEPENDENCY_KEEP_STANDALONE_CLAIMS_OPEN
D1_W1_PREREQUISITE_DISPOSITION: INCLUDE_INDEPENDENTLY_CLOSED_W1_A_B_BASELINE_DEPENDENCIES
D1_PC01_OWNER_ATTESTED_PASS_CUSTODY: ACCEPT_FOR_INTEGRATION_MEMBERSHIP
```

## 결정 2 — semantic convergence and PC-02 exclusion

권고:

```text
ADMIN_BASE: fab6315c only after exact PC02 inverse is approved
PRESERVE: canonical View authority/status totality/no semantic fallback and accepted prerequisites
COMPOSE: reviewed W1-A~I2 scope on six exact semantic text-conflict files
KEEP_OPEN: public ReactionProvider syntax/wire/diagnostics/default registry
FILE_LEVEL_OURS_THEIRS: FORBIDDEN
```

승인 literal 제안:

```text
D2_SEMANTIC_CONVERGENCE: R2_AFTER_PC02_INVERSE_PLUS_REVIEWED_W1_SCOPED_COMPOSITION
D2_PC02_EXCLUSION_METHOD: INVERSE_EXACT_04566A24_PATCH_IN_SUCCESSOR
```

PC-02 28 paths는 해당 commit 뒤 R2까지 추가 변경이 0이라 exact inverse가 blob 수준에서
분리 가능하다. 그래도 release membership 변경이므로 승인 전 실행하지 않는다.

## 결정 3 — tracked WASM

```text
D3_TRACKED_WASM_OWNER: REBUILD_COMBINED_SOURCE_OFFICIAL_A_B_THEN_BIND_SINGLE_FAMILY
```

현재 tracked artifact는 freshness check가 실패한다. 기존 T5 또는 W1 artifact를 선택하거나
binary merge하지 않는다.

## 결정 4 — public SPEC custody

```text
D4_PUBLIC_SPEC_CUSTODY: BIND_EXACT_LIVE_V0_5_0_18_FILE_BYTES_ONLY
```

`6974eda4...` 전체 역사 bundle은 적용하지 않는다.

## 결정 5 — R10/T1 disposition

```text
D5_R10_DISPOSITION: ACCEPT_AS_T5_REVIEWED_BASELINE_DEPENDENCY_KEEP_PROGRAM_CLAIM_OPEN
```

dependency byte를 보존하더라도 R10/T1 standalone independent PASS나 closure를 새로
주장하지 않는다. 기존 branch/worktree도 보존한다.

## 결정 6 — public fixture membership and rights

현재 projectile test fixture는 Git commit에 없는 live `docs/ssot/**` 파일을
`include_str!`로 읽으므로 clean public repository에서 compile-time fail이다.
`PRIVATE_FIXTURE_MIGRATION_PLAN.md`의 exact custody를 입력으로 사용한다.

```text
D6_PC01_PUBLIC_CONFORMANCE_MEMBERSHIP: INCLUDE_EXACT_FIVE_FILE_PACK
D6_PC01_PACK_RIGHTS:
D6_PROJECTILE_SELECTED_EXAMPLE_MEMBERSHIP: INCLUDE_AS_PUBLIC_SELECTED_EXAMPLE
D6_PROJECTILE_LESSON_RIGHTS:
D6_PROJECTILE_PUBLIC_TARGET_PATH: examples/physics/projectile_xy.ddn
```

rights가 승인되지 않으면 해당 fixture를 자동 축약·재작성하지 않고 public
self-containment를 RED로 유지한다.

추가 provenance 감사 결과 PC-01 5-file pack은 `또니 <tongosu@myarts.kr>`의
`cf97f134...` 한 commit에서 왔고, selected examples 33 files는
`urihanl <urihanl@gmail.com>` 계보다. live projectile exact blob은 repository object
database에 없으며 같은 이름 historical product lesson 2개도 byte-identical하지 않다.
이 사실은 rights 승인을 대신하지 않으므로 D6 rights 필드는 계속 Owner 입력이다.

## 결정 7 — public conformance root policy

현행 13개 root의 bounded closure는 82 scripts, 43 pack trees, 433 files이며 R1
projection에 381 files가 없다. 이 중 두 umbrella root가 각각 43개와 30개의 script
closure를 끌어온다. giant internal test tree 전체를 public conformance로 투영할지,
public-specific aggregate로 요구 의미를 좁고 명시적으로 보존할지는 exact public
membership 결정이다.

권고:

```text
D7_PUBLIC_CONFORMANCE_ROOT_POLICY: OPTION_B_PUBLIC_SPECIFIC_AGGREGATE_WITH_EXACT_LEAF_AND_CURATED_PARITY_DURABILITY_CASES
```

이 결정은 기존 CLI/WASM parity와 Workbench durability 의미 완화를 승인하지 않는다.
승인 전 R2 manifest, checker root, fixture membership을 수정하지 않는다.

## 반환 형식

```text
DDN_LONG_RELINT_PRODUCT_01_OWNER_APPROVED:
D1_FEATURE_MEMBERSHIP:
D1_T5_PREREQUISITE_DISPOSITION:
D1_W1_PREREQUISITE_DISPOSITION:
D1_PC01_OWNER_ATTESTED_PASS_CUSTODY:
D2_SEMANTIC_CONVERGENCE:
D2_PC02_EXCLUSION_METHOD:
D3_TRACKED_WASM_OWNER:
D4_PUBLIC_SPEC_CUSTODY:
D5_R10_DISPOSITION:
D6_PC01_PUBLIC_CONFORMANCE_MEMBERSHIP:
D6_PC01_PACK_RIGHTS:
D6_PROJECTILE_SELECTED_EXAMPLE_MEMBERSHIP:
D6_PROJECTILE_LESSON_RIGHTS:
D6_PROJECTILE_PUBLIC_TARGET_PATH:
D7_PUBLIC_CONFORMANCE_ROOT_POLICY:
RESUME_FROM_GATE: G8
```

현재 상태:

```text
SUPERSEDED_BY_OWNER_DECISION_BINDING
OWNER_DECISION_D1_D7_BOUND
G8_ISOLATED_INTEGRATION_AUTHORIZED
PC01_FRESH_TARGETED_REVIEW_REQUIRED
RIGHTS_CONFIRMATIONS_REMAIN_OPEN
```
