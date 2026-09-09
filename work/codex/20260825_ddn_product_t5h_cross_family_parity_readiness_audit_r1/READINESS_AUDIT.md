# [셈그림Codex -> 제품구조Chat] T5H cross-family parity readiness — read-only audit

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
AUDIT_ID: DDN_PRODUCT_T5H_CROSS_FAMILY_PARITY_READINESS_AUDIT_R1
AUDIT_INPUT_HEAD: 0b7e51bbb0bf2f06dac05e2e415b3d0281b01820
MODE: DEPENDENCY_INDEPENDENT_READ_ONLY_PLUS_EXECUTABLE_AUDIT_PACK
T5G_PLAIN_PASS: PENDING
T5H_PRODUCT_IMPLEMENTATION_STARTED: NO
PRODUCT_SOURCE_CHANGE: 0
SSOT_SPEC_WASM_CHANGE: 0
```

## 1. Exact inventory

`buildCanonicalViewPayloadSet()`은 renderer/product active key를 정확히 14개 반환한다. family도 14개가 1:1로 일치한다. `space3d`, `grid3d`는 registry-only라 aggregate active count에서 제외한다.

## 2. Blocking readiness finding

unknown status `renderer_ready`를 모든 family input에 넣은 read-only probe 결과:

```text
FAIL_OPEN_AS_UNKNOWN_STATUS: 12
  console
  console_grid
  graph
  space2d
  table
  text
  structure
  grid2d
  workbench_line
  workbench_pendulum
  workbench_projectile
  workbench_grid

FAIL_CLOSED_AS_INVALID: 2
  scene_summary
  curriculum_semantic_scene
```

T5G correction은 두 high-level family를 닫았지만 이전 family builder들은 non-`available` status를 그대로 canonical outcome으로 전달한다. 이는 최종 공통 상태 모델의 totality와 모순되므로 T5H closure 전 반드시 교정해야 한다.

이 결과는 T5B~T5F의 previously reviewed available-path semantics를 재판정하지 않는다. composite status-domain robustness gap이며 T5G plain PASS 뒤의 T5H dependent product correction 대상으로 둔다.

## 3. Required T5H implementation after gate

1. 기존 `semantic_view_payload.js` 안에서 shared status-domain validator를 사용한다. 새 abstraction/owner를 만들지 않는다.
2. unknown status는 family별 exact `invalid` candidate diagnostic으로 닫는다.
3. `no_view`, `unavailable`, `invalid`, `unsupported`, `ambiguous`의 기존 의미와 diagnostic identity를 보존한다.
4. console-grid는 upstream canonical console status만 허용된 status domain 안에서 전파한다.
5. 14-key inventory와 consumer matrix를 executable aggregate로 유지한다.
6. T5B~T5G golden/mutation/browser를 모두 재실행한다.
7. success-path candidate bytes, state hash, storage, feature set이 변하지 않았음을 확인한다.

## 4. Safe executable evidence

- pack: `pack/seamgrim_canonical_view_t5h_readiness_audit_v1/`
- runner: `tests/seamgrim_canonical_view_t5h_readiness_audit_runner.mjs`
- aggregate: `tests/seamgrim_canonical_view_t5h_cross_family_readiness_runner.mjs`
- audit PASS means the recorded gap was reproduced exactly; it is not T5H closure.

The aggregate executes `6` golden runners, `6` mutation runners, and the status-readiness runner: `13/13 PASS`. It records stdout SHA-256 per child and makes no browser claim. Browser evidence remains an explicit separate matrix.

## 5. Gate

```text
T5H_READ_ONLY_READINESS_AUDIT_COMPLETE
T5H_STATUS_TOTALITY_GAP_RECORDED
T5H_CROSS_FAMILY_EXECUTABLE_READINESS_BASELINE_PASS_13_OF_13
T5H_DEPENDENT_PRODUCT_IMPLEMENTATION_NOT_STARTED
T5G_FIXED_HEAD_INDEPENDENT_PLAIN_PASS_PENDING
OWNER_DECISION_REQUIRED: NO
PUBLIC_ABI_STABLE_WIRE_CHANGE: 0
NATIVE_IMPLEMENTATION: 0
```
