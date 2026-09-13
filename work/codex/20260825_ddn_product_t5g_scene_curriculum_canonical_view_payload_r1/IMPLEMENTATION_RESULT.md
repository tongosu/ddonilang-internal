# [셈그림Codex -> 제품구조Chat] T5G scene/curriculum canonical payload — 결과

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5G_SCENE_CURRICULUM_CANONICAL_VIEW_PAYLOAD_R1
STATUS: IMPLEMENTED_UNDER_INDEPENDENT_REVIEW
DEEP_RESEARCH_CHECK: NOT_USE
T5F_FIXED_HEAD: 0abec54b30b26dbe99ce249aa3de5d7681907eab
T5F_HANDOFF_ANCESTOR: 7a83d5dd457b420570ecc0f1092fff7eab9bf946
T5F_CONTROL_TOWER_CORRECTION: dd8f560c93b9454a2cd92b5921ecea89055135ac
V25_PC02_SUCCESSOR_BASELINE: d49a45faa963aaddd529052a1811e09109dd8e47
AUTHORITY_BOUNDARY_COMMIT: 24fb07f152c9aed19409e48a80f86c0d981beeee
INITIAL_PRODUCT_FIXED_HEAD: f1b37d61ea12ae2292b7f723ab17785c875085a1
INITIAL_HANDOFF_COMMIT: 011568967d71d2ba3e4536767c2fda61b61972e9
STATUS_MATRIX_CORRECTION: f3e93a154d97838ae1885bf512265836183b747c
PRODUCT_FIXED_HEAD: f3e93a154d97838ae1885bf512265836183b747c
BRANCH: codex/ddn-product-t5g-scene-curriculum-canonical-view-payload-r1-20260825
```

## 1. Authority and product behavior

- 기존 `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`만 canonical owner로 확장했다. 제3 view abstraction은 만들지 않았다.
- `scene-summary`는 명시된 primary family의 exact canonical payload 하나만 소비한다. primary가 없고 동등 candidate가 둘 이상이면 `ambiguous`이며 graph를 기본 의미로 선택하지 않는다.
- `curriculum-semantic-scene`은 검증된 lesson/world/primary identity, control/observation binding, exact nested primary canonical payload만 canonical identity에 포함한다.
- DOM selector, a11y label, browser reading order, prompt, timestamp, localStorage, view config, frame sample, overlay/layer는 presentation/session metadata로 분리했다.
- 기존 wrapper schema `seamgrim.scene.v0`와 `seamgrim.curriculum_semantic_scene.v0` 및 기존 presentation runtime binding은 보존했다.
- unknown schema, missing identity, duplicate anchor, identity mismatch, ambiguity는 product-local candidate diagnostic으로 fail-closed한다.
- completion audit에서 발견한 알 수 없는 projection status 통과를 제거했다. 허용 상태 밖의 `renderer_ready`, `dom_bound` 같은 값은 두 family 모두 exact `invalid` diagnostic으로 닫힌다.

## 2. 중요한 실제 제품 경계

대표 수업 `rep_math_function_line_v1`의 현행 화면은 기존 compatibility/presentation 경로로 graph를 표시하지만, 해당 실행의 upstream canonical graph는 exact structured authority 부재로 `no_view`다. T5G는 이를 graph canonical success로 세탁하지 않았다.

```text
ACTUAL_PRODUCT_SCENE_CANONICAL_STATUS: no_view
ACTUAL_PRODUCT_CURRICULUM_CANONICAL_STATUS: no_view
PRESENTATION_RUNTIME_BINDING_COMPLETE: true
CANONICAL_BINDING_COMPLETE: false
SILENT_GRAPH_PROMOTION: 0
```

exact authoritative fixture를 브라우저 안에서 import한 별도 수직은 두 family 모두 `available`이며 같은 nested primary canonical bytes를 보존한다. 따라서 available 계약과 실제 제품의 honest no-view 경계를 둘 다 증명한다.

## 3. Evidence

- pack: `pack/seamgrim_scene_curriculum_canonical_view_payload_v1/`
- scene golden SHA-256: `5926f674c3351f3c9efc4f2e18ef589106cbb1880bcaa3a4dc34b6e25fa8ea40`
- curriculum golden SHA-256: `34d86b08cc5d3d2821d08a1eaa32aedb9b516dfaa5e884ea737121b867c6afdf`
- exact golden: `2/2 PASS`
- family status matrix: `14/14 PASS` (`POSITIVE / MISSING_NO_VIEW / INVALID / UNSUPPORTED / AMBIGUOUS / IDENTITY / UNKNOWN_STATUS` × 2)
- ordering matrix: `3/3 PASS` (scene required family, curriculum anchor, curriculum concept)
- mutation: `5/5 GREEN -> RED -> GREEN`, residue `0`
- scene session byte parity: `PASS`
- curriculum project snapshot byte parity: `PASS`
- presentation metadata in canonical identity: `0`
- actual local Chromium: `PASS`, network install `0`
- representative curriculum five lessons: `PASS`
- T5B, T5C, T5D, T5E, T5F: `PASS`
- RuntimeBridge, HostBridge, observation channel, snapshot/portable artifact: `PASS`
- clean-detached `f3e93a154d97838ae1885bf512265836183b747c`: `PASS`, clean/staged `0`

T5F regression used the current PC-02 source-built WASM at `I:\home\urihanl\ddn\codex\build\wasm\ddonirang_tool`, SHA-256 `db941a629d141b0e322aaa3ed4af36d09cdfba4c9ca4c6c68eae19d8f0adb1e4`.

## 4. Pre-existing non-blocking debt

- `tests/seamgrim_editor_run_transaction_runner.mjs` expects exact text `setScreen("run");`, while baseline `d49a45fa` already uses `setScreen("run", { shellSpace });`. The same failure was reproduced in an isolated baseline worktree; it is not introduced by T5G.
- T5C-origin stale `seamgrim_ui_common_runner.mjs` expectation remains OPEN.
- T5D text unsupported-format golden coverage remains OPEN.
- T4f mutation runner Windows CRLF housekeeping remains OPEN.

## 5. Change boundary and gate

```text
THIRD_VIEW_ABSTRACTION: 0
FEATURE_REMOVAL: 0
GRAPH_DEFAULT_SEMANTIC_SUCCESS: 0
STATE_HASH_DRIFT: 0
STORAGE_DRIFT: 0
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
TRACKED_WASM_DIFF: 0
MERGE_COMMIT_COUNT: 0
NETWORK_INSTALL: 0
OFFICIAL_DB_WRITE: 0
ACTIVATION_CALL: 0
```

PID `53196`과 port `8787`은 종료 시 존재하지 않았으며 이 작업은 시작·종료·호출하지 않았다. 임시 browser server/socket/data directory residue는 `0`이다.

```text
WORKBENCH_VIEW_T5G_SCENE_CURRICULUM_CANONICAL_PAYLOAD_IMPLEMENTED_UNDER_REVIEW
READY_FOR_DDN_PRODUCT_T5G_SCENE_CURRICULUM_CANONICAL_VIEW_PAYLOAD_INDEPENDENT_REVIEW
T5H_NOT_STARTED_PENDING_T5G_PLAIN_PASS
PROGRAM_STATE: ACTIVE / CORE_VIEW_CONVERGENCE_SUBSTANTIALLY_CLOSED
PUBLIC_STABLE_ABI_NOT_CLAIMED
SSOT_SPEC_PROMOTION_NOT_CLAIMED
NATIVE_IMPLEMENTATION_NOT_AUTHORIZED
WEB_S0_NOT_CLAIMED
HUMAN_PASS_NOT_CLAIMED
```
