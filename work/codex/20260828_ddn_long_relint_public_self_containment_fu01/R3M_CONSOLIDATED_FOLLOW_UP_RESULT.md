# DDN-P-LONG-RELINT R3K/R3L consolidated follow-up R3M 결과

## 범위와 계보

```text
PARENT_PERSISTENT_GOAL: DDN-LONG-RELINT-PRODUCT-01
STARTING_PARENT: 396fe90cbc18e0c06cb5d557d55a8c8dcb6fe714
R3L_CUSTODY_FIXED_HEAD: eeda9a9da30be91b3d504ed5828af670590b7fb1
EXTERNAL_REVIEW_EVIDENCE: 9cdf474d917bb53085aa2e938b45d78cf32ee152
EXTERNAL_REVIEW_ANCESTRY: SIDE_BRANCH_DOCUMENT_ONLY
PRODUCT_TEST_FIXED_HEAD: 1e55e4b2984e52cfcf1141f06ed0fcefa0c3a19e
NEW_GOAL_CREATED: NO
```

`9cdf474d...`는 `51f85622...`의 문서 전용 side-branch 후손이다. 기존 계보를
rewrite하거나 review 문서를 제품 계보에 cherry-pick하지 않았다. R3K의 제품·테스트
교정만 `396fe90c...` 위에 선형 재적용했고, R3L D1~D6 문서·107-path ledger·NOTICE는
바이트 보존했다.

제품·테스트 교정 계보는 다음과 같다.

```text
396fe90c -> ca06845d -> 8aeae804 -> 449805bc -> 56a5e707
          -> 6afb43ad -> 1e55e4b2
MERGE_COMMIT_COUNT: 0
```

## F1 — projected metadata 절대경로 제거

source `ddn.project.json`의 기존 `toolchain.teul_cli_bin` 값은 제품 source metadata를
변경하지 않고 그대로 보존했다. projection manifest가 정확한 JSON path
`["toolchain", "teul_cli_bin"]`만 필수 1회 제거한다. path가 없거나 JSON이 아니면
projection은 fail-closed한다.

```text
SOURCE_DDN_PROJECT_SHA256: 9b883ce9c98c59fc270f2069d305aa3ce5ce49493b7b2949fc9cd618a2165d4f
PROJECTED_DDN_PROJECT_SHA256: 8244f80a3ce0588d04f878b4a4c78370e91ee13be87774ee8fc2c63de7625f95
PROJECTED_TEUL_CLI_BIN_FIELD_COUNT: 0
PRODUCT_METADATA_INTERNAL_PATH: 0
PRIVATE_BUILD_PATH_FALLBACK: 0
F1_STATUS: PASS
```

fresh projection의 G14 runner는 자체 CLI를 구성하므로 다른 절대경로, checkout-relative
private path 또는 환경 fallback을 추가하지 않았다.

## F2 — 전체 role·전체 file security scan

manifest 전 role을 독립 재집계한 결과는 17 role, 894파일이다.

| Role | Files |
|---|---:|
| BUILD_REQUIRED | 4 |
| CLI_SOURCE | 730 |
| COMPILE_TIME_UNIT_TEST_SUPPORT | 1 |
| PRODUCT_ASSET | 5 |
| PRODUCT_METADATA | 5 |
| PRODUCT_SOURCE | 100 |
| PROJECTION_TOOL | 1 |
| PROJECTION_TOOL_TEST | 1 |
| PROJECTION_VALIDATOR | 1 |
| PROJECTION_VALIDATOR_TEST | 1 |
| PUBLIC_CONFORMANCE_CONTRACT | 2 |
| PUBLIC_CONFORMANCE_INPUT | 3 |
| PUBLIC_CONFORMANCE_RUNNER | 2 |
| PUBLIC_SPEC_CURRENT | 1 |
| PUBLIC_SPEC_EXACT_V0_6_0 | 30 |
| TRACKED_WASM_FAMILY | 5 |
| WASM_BUILD_ENTRYPOINT | 2 |

validator는 role allowlist 없이 manifest의 894파일 전부를 순회한다. validator Python
negative fixture는 `test_*` 함수와 exact `assert_red` 진단 결속을 AST로 확인한 줄만
제외하며, Rust 제품 파일은 끝의 정확한 `#[cfg(test)] mod tests`만 구조적으로 제외한다.
파일 전체 allowlist나 broad ignore는 없다. transformation tool test의 중립 fixture도
실제 internal-path 문자열을 담지 않도록 교정했다.

34개 unit/mutation test가 모두 PASS했다. 포함된 RED 변이는 Windows drive,
UNC, device path, `file://`, private `pack/**`, `work/**`, `docs/ssot/**`,
official-store 및 이전 누락 role 경로다. 각 test는 임시 projection에서
GREEN baseline을 만든 뒤 변이를 삽입해 exact diagnostic RED를 확인하고 fixture를
폐기한다.

최종 전체 검사에는 실제 finding 한 건이 남는다.

```text
PATH: solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
ROLE: TRACKED_WASM_FAMILY
INTERNAL_PATH_MATCH_COUNT: 115
DIAGNOSTIC: E_PUBLIC_INTERNAL_ABSOLUTE_PATH
```

따라서 invalid projection에 성공 validation receipt를 발행하지 않았다. 구현상 scanner
대상은 894/894지만, 성공 receipt의 필수 값
`SECURITY_SCANNED_FILES == TOTAL_PROJECTED_FILES`와
`UNSCANNED_SECURITY_RELEVANT_FILES == 0`은 tracked WASM finding이 해결되기 전에는
주장하지 않는다.

```text
F2_TOTAL_PROJECTED_FILES: 894
F2_SCANNER_CONFIGURED_FILES: 894
F2_SECURITY_SCANNED_FILES_IN_SUCCESS_RECEIPT: NOT_ISSUED_FAIL_CLOSED
F2_UNSCANNED_FILES_IN_SUCCESS_RECEIPT: NOT_ISSUED_FAIL_CLOSED
F2_ROLE_COUNT: 17
F2_STATUS: BLOCKED_BY_TRACKED_WASM_EMBEDDED_ABSOLUTE_PATH
```

## Projection A/B

```text
SOURCE_COMMIT: 1e55e4b2984e52cfcf1141f06ed0fcefa0c3a19e
FILE_COUNT_A_B: 894 / 894
PUBLIC_TREE_IDENTITY_A_B: sha256:83fcaaae6fab7127e91985f0b071272f4e42b0459a13564a89235efac4106fef
TREE_MANIFEST_FILE_SHA256_A_B: 6759dfec5938d70a454597a5da3fd009b1b1453b22eb260d704632596b6ef6fc
PROJECTION_RECEIPT_FILE_SHA256_A_B: 2ecaa0ff4903260265c6ca2080b6e6d2c321d5ec4d670d476442841c1f50b4a9
BYTE_IDENTITY: PASS
VALIDATOR_RESULT_A_B: RED / RED — same tracked WASM finding
```

## 회귀

```text
PROJECTION_TOOL_VALIDATOR_TESTS: PASS 34/34
TOOL_LIB_SOURCE: PASS 517/517
TOOL_LIB_PROJECTION: PASS 517/517
TOOL_BINARY_SOURCE: 405 PASS / ai-prompt 2 expected authority RED
TOOL_BINARY_PROJECTION: 405 PASS / same ai-prompt 2 RED
PROJECTION_ADDITIONAL_RED: 0
G14: PASS 3/3
PUBLIC_SPEC_RAW_GIT_BLOB_SEAL: PASS 29/29
TRACKED_WASM_REFRESH: 0
```

## R3L custody와 보호 경계

다음 기존 artifact는 수정하지 않았다.

```text
OWNER_DIRECTION_BINDING_D1_D6_R3L.md:
  a02ccf94c12e3adee70a62bd152f1b28e3d74a9c015ff1ec04598a24fa29f478
WORKBENCH_BROWSER_PATH_RIGHTS_LEDGER_R3L.detjson:
  704d48bd3ef50a28d1a800162312edc03ef75e54cf8f65790597121fe7b18321
WORKBENCH_BROWSER_READ_ONLY_CUSTODY_AUDIT_R3L.md:
  0e1b666cd55bd10c99588af210dcf9b2c0d756e21a3b32d4716e02d37f8a4a08
THIRD_PARTY_NOTICE_DRAFT_R3L.md:
  dbdf6b2671eba3002e86e9255a1ebaf6d0143a566810c3dfdbe342f2fcedd540
PUBLIC_FACADE_CANDIDATE_R3J/NOTICE_CANDIDATE.md:
  bc08698db3f17bcaed0f07784610234f0998dd50250cca76b5e1efb13f42a479
R3L_LEDGER_PATH_COUNT: 107
```

```text
DOCS_SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
WORKBENCH_UI_DIFF: 0
TRACKED_WASM_DIFF: 0
OFFICIAL_WRITE_COUNT: 0
ACTIVATION_CALL_COUNT: 0
NETWORK_DOWNLOAD_COUNT: 0
```

## 인계 판정

기존 `TARGETED_INDEPENDENT_REVIEW_REQUEST.md`의 SHA-256
`8778c0a33205e11daceec3014f26effa002404f122f3c46b5d4b243aadebc5ec`는
그대로 보존했다. F2가 아직 실패하므로 Scope A/B/C의 새 targeted rereview request를
작성하거나 Claude에 보내지 않는다.

```text
CURRENT_REVIEW_REQUEST_DISPOSITION: STALE_PENDING_F2_TRACKED_WASM_OWNER_DECISION
TARGETED_REREVIEW_REQUEST: NOT_CREATED
R3K_R3L_LIMITED_CLOSURE: NOT_CLAIMED
FINAL_STATUS: BLOCKED_BY_R3M_TRACKED_WASM_EMBEDDED_ABSOLUTE_PATH
```
