# DDN-P-RELINT-01 release integration exact owner decision packet

## 결정이 필요한 이유

검토 결속 제품 기준점 `905efb4a...`와 W1C2 제한 closure `40cd0473...`는 공통 base `5ff2a804...`에서 갈라진 독립 계보다. 94개 changed-path overlap 중 48개 final blob이 다르고, 13개는 기계 병합도 충돌한다. 따라서 최신 날짜나 `ours`/`theirs` 선택으로 제품 의미를 결정할 수 없다.

## D1 — release feature membership

권고 `OPTION_A_INCLUDE_BOTH_LIMITED_SCOPES`:

```text
INCLUDE: Canonical View T5G~T5I closed product scope
INCLUDE: W1C2 I2 internal DdnRunner dispatch closed scope
PRESERVE_OPEN: public ReactionProvider source surface
PRESERVE_OPEN: stable provider wire and public diagnostics
EXCLUDE_PENDING_PASS: V25 PC-02
EXCLUDE_DIRTY_UNBOUND: MATH-PHYS-01~03 and detached review copy
```

대안:

- `OPTION_B_T5G_ONLY`: W1C2 closure는 다음 integration으로 미룬다.
- `OPTION_C_DEFER_ALL_PRODUCT_INTEGRATION`: inventory만 보존한다.

## D2 — 48-path semantic convergence owner

권고 `OPTION_A_T5G_STRUCTURAL_BASE_PORT_W1C2_INTERNAL_SEMANTICS`:

- T5G의 canonical View owner, status totality, no-fallback, presentation separation을 보존한다.
- W1C2의 reviewed internal route/provider dispatch, API confinement, effect atomicity만 현재 source 구조에 이식한다.
- public provider registry 기본값은 empty를 유지한다.
- public syntax, stable wire, public diagnostic authority를 추가하지 않는다.
- 48경로를 파일 단위 `ours`/`theirs`로 해결하지 않고 invariant별로 재구성한다.

대안:

- `OPTION_B_W1C2_STRUCTURAL_BASE_PORT_T5G`: 더 오래되고 큰 W1C2 tree를 구조 기준점으로 삼는다.
- `OPTION_C_PATH_BY_PATH_OWNER_MATRIX`: 48경로의 owner를 별도 표로 모두 결정한 뒤 구현한다.

## D3 — tracked WASM owner

권고 `OPTION_A_REBUILD_FROM_COMBINED_SOURCE_AND_SEAL`:

```text
BUILD_ENTRYPOINT: scripts/build_wasm_tool.ps1
BUILD_MODE: isolated A/B absolute paths
REQUIRED: source-built A == source-built B
REQUIRED: glue, d.ts, manifest, wasm all from the same integrated source
TRACKED_OVERWRITE: only in the isolated integration branch after A/B identity
STALE_ARTIFACT_REUSE: FORBIDDEN
```

대안 `OPTION_B_DO_NOT_LAND_TRACKED_WASM_YET`은 clean source integration은 허용하지만 release-integration baseline과 public projection은 계속 fail-closed한다.

## D4 — public SPEC custody binding

권고 `OPTION_A_BIND_EXACT_LIVE_V0_5_0_BYTES`:

- shared authority에서 검증한 `publish/spec/CURRENT.md`와 v0.5.0 sealed 18-file family만 byte-identical로 결속한다.
- public SPEC의 내용을 수정하거나 v0.6.0 후보를 추종하지 않는다.
- `6974eda4...`의 125-file 역사 bundle 전체를 자동 cherry-pick하지 않는다.

대안 `OPTION_B_DEFER_PUBLIC_SPEC_CUSTODY`는 제품 integration은 가능하지만 public-source baseline과 projection은 계속 준비 불가다.

## D5 — R10 checkpoint disposition

권고 `OPTION_A_ANCESTRY_RECEIPT_ONLY`:

- R10 제품 commit `15f983fe...`와 RuntimeBridge 제품 commit `0249aa0d...`가 T5G 계보에 포함됐음을 receipt로 기록한다.
- docs-only `50ddc7be...`를 별도 제품 cherry-pick하지 않는다.
- branch/worktree는 보존하고 삭제하지 않는다.

대안 `OPTION_B_BIND_R10_DOCS_CUSTODY`는 제품 byte를 바꾸지 않는 별도 문서 결속만 추가한다.

## 요청 반환 형식

```text
DDN_P_RELINT_01_OWNER_DECISION:
D1_FEATURE_MEMBERSHIP:
D2_SEMANTIC_CONVERGENCE:
D3_TRACKED_WASM_OWNER:
D4_PUBLIC_SPEC_CUSTODY:
D5_R10_DISPOSITION:
RESUME_FROM_GATE: G5_ISOLATED_PRODUCT_INTEGRATION
```

Owner 결정 전 상태:

```text
BLOCKED_BY_EXACT_OWNER_DECISION
PRODUCT_IMPLEMENTATION_NOT_STARTED
```
