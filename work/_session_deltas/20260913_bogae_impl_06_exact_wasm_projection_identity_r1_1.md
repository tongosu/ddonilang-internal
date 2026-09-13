# [보개투영 Work -> 또니랑 개발 관리자] BOGAE-IMPL-06 exact WASM projection identity R1.1 — 최종 제품 인계

이 문서는 선행 제품 `e3c334eff053d6594740a24e6e1c0c447c179ace`와 handoff `85020f3401b433bcddea636ff90bca09e0dd8018`을 보존하면서, 공식 R1 지시문의 substring mutation 및 실제 source-built WASM 실행 근거를 결속한 successor다.

```yaml
LIVE_BASE: v25.83.0 / RD-001~621
PUBLIC_SPEC: v0.7.0

PRODUCT: 0fbfa18b1b3013b9eb06149ba802d4164e9a069f
PRODUCT_TREE: f61ed50bec79c5b304c7061be066e3ff79e2f0d5
PRODUCT_PARENT: 85020f3401b433bcddea636ff90bca09e0dd8018
PRODUCT_BEHAVIOR_PREDECESSOR: e3c334eff053d6594740a24e6e1c0c447c179ace

PATH_LEASE:
  - tool/src/ddn_runtime.rs
  - tool/src/wasm_api.rs
```

## 최종 계약

```yaml
EXACT_WASM_KIND_IDENTITY: PASS
EXACT_WASM_PROFILE_IDENTITY: PASS
SUBSTRING_MAPPING: 0
FUZZY_MAPPING: 0
AUTO_CAMERA: 0
AUTO_BOUNDS: 0
PROFILE_FALLBACK: 0
AUTHORED_ORDER_MUTATION: 0
LEGACY_FALLBACK_AFTER_TYPED_VIEW: 0

NATIVE_WASM_ACCEPT_REJECT_PARITY: PASS
NATIVE_WASM_FAILURE_CLASS_PARITY: PASS
```

Native와 source-built Node WASM에 같은 DDN sources와 expected provider/profile/failure identity를 적용했다. 성공은 exact `표준보기.장면` + `표준장면.평면` + `plane2`에서만 발생했다. 다중 View는 `E_BOGAE_UNSUPPORTED / typed_view_binding_ambiguous`, space3는 `E_BOGAE_UNSUPPORTED / typed_view_projection_unsupported`로 동일하게 거부됐다.

## BIC

```yaml
BIC_UNSUPPORTED_01: PASS
BIC_UNSUPPORTED_02: PASS
BIC_NATIVE_WASM_01: PASS
BIC_SCENE_GEOMETRY_01: PASS
BIC_SCENE_GEOMETRY_02: PASS
FIXTURE_PREREQUISITE_CORRECTION: NONE
```

기존 four-family execution-receipt fixture를 이 target의 권위로 사용하지 않았다. exact typed runtime/WASM projection에 집중한 fixed Rust tests와 source-built Node WASM probe를 사용했다.

## 검증

```yaml
NATIVE_EXACT_PROJECTION_TESTS: 5/5 PASS
WASM_META_REGRESSION: 6/6 PASS
NATIVE_CHECK: PASS
WASM32_CHECK: PASS
SOURCE_BUILT_NODE_WASM: PASS
CANDIDATE_OFFLINE_SEAL: PASS
DIFF_CHECK: PASS

FULL_NATIVE_LIB_ON_BEHAVIOR_PREDECESSOR:
  RESULT: 661 PASS / 39 inherited unrelated failures
  NEW_BOGAE_IMPL_06_FAILURES: 0
  RERUN_AFTER_TEST_ONLY_SUCCESSOR: NOT_REQUIRED
```

Source-built WASM custody:

```yaml
WASM_OUTPUT: I:/home/urihanl/ddn/codex/out/bogae-impl06-wasm-r3/wasm/ddonirang_tool/ddonirang_tool_bg.wasm
WASM_BYTES: 5815301
WASM_SHA256: B2CC638A9739F68EBEBF6B6D58F53CB46727B71E333E72F6BE72AC6E381898B8

REMAP_RECEIPT: I:/home/urihanl/ddn/codex/out/bogae-impl06-wasm-r3/wasm/ddonirang_tool/R3N_WASM_REMAP_RECEIPT.detjson
REMAP_RECEIPT_SHA256: 4284FF813A3D06D15CAB0E0D501963E36A7382775D2E37706C54719DEFDD382D
REMAP_SEMANTIC_IDENTITY: sha256:27202e5691aa4c357fd30ac113e5fe55aeeba8fb8e5815294c58935fb2ba0282

WASM_PROBE: I:/home/urihanl/ddn/codex/out/bogae-impl06-wasm-r3/verify_bogae_impl06.cjs
WASM_PROBE_BYTES: 2812
WASM_PROBE_SHA256: 03B15D8BF823E175866752312567772B42099095A200C4148D24468ED0F4A2C8
```

첫 candidate build는 컴파일과 artifact 생성을 마쳤으나 `CARGO_NET_OFFLINE=true` seal 조건 누락으로 최종 실패했다. 해당 출력은 PASS 근거에서 제외했다. 새 `r3` 출력에서 offline seal을 포함해 처음부터 다시 실행해 PASS했다.

## Mutation

각 mutation은 단독 적용했고 RED 뒤 exact source를 복원해 최종 5/5 GREEN을 확인했다.

```yaml
M1:
  MUTATION: exact provider equality를 starts_with substring authority로 변경
  RED: PASS / exit 1
M2:
  MUTATION: space3 missing projection에 default camera 삽입
  RED: PASS / exit 1
M3:
  MUTATION: authored x_min 대신 0.0 자동값 사용
  RED: PASS / exit 1
RESTORE_GREEN: PASS 5/5

FIXED_RUNTIME_BLOB: 8ff03dd6f84f46a4a5c7d292a41173521d397e66
FIXED_RUNTIME_SHA256: 49B8DA5A9B13427AE21943F10717CB6AE439B12501E466689E044E445BD22624
FIXED_RUNTIME_BYTES: 1245805
```

## 경계

```yaml
INDEPENDENT_REVIEW: NOT_RUN
SELF_PASS: NO
STATUS: PRODUCT_FIXED_PENDING_BATCH_INDEPENDENT_REVIEW
READY_FOR_BOGAE_IMPL_07: YES

SSOT_MUTATION: 0
PUBLIC_SPEC_MUTATION: 0
PUSH: 0
MERGE_COUNT: 0
```

BOGAE-IMPL-07, full-headless lifecycle, Local Workspace persistence, whole Workbench/Bogae, V1 readiness/release 및 Human PASS는 비주장이다.
