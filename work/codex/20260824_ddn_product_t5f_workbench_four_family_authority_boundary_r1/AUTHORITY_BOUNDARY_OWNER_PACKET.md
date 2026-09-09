# [셈그림Codex -> 제품구조Chat] T5F Workbench 네 가족 authoritative result 경계 Owner packet

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5F_WORKBENCH_FOUR_FAMILY_CANONICAL_VIEW_PAYLOAD_R1
PACKET_STATUS: OWNER_DECISION_REQUIRED
DEEP_RESEARCH_CHECK: NOT_USE
T5E_CLOSURE_BASELINE: 27acdb0f4633da7473187d772ce1875dc6d5d729
AUDIT_BRANCH: codex/ddn-product-t5f-workbench-four-family-canonical-view-payload-r1-20260824
AUDIT_WORKTREE: I:\home\urihanl\ddn\codex\build\worktrees\ddn-product-t5f-workbench-four-family-canonical-view-payload-r1-20260824
PRODUCT_IMPLEMENTATION_STARTED: NO
PRODUCT_CODE_CHANGED: 0
TEST_CODE_CHANGED: 0
```

## 1. 결론

T5F 네 가족 `line / pendulum / projectile / grid`에 필요한 authoritative structured view/result 계약은 현행 공통 runtime/tool 경로에 존재하지 않는다.

공통 canonical 입력 추출기는 `console / graph / space2d / table / text / structure / grid2d`만 제공한다. Workbench는 이 결과를 frame마다 만들고 `canonical_views`로 전달하지만, 네 가족 renderer는 이를 소비하지 않는다. 대신 raw committed WASM channel/resource와 frame history를 다시 해석한다.

장기 지시문의 경계 규칙에 따라 JS에 새 의미를 발명하거나 기존 raw inference를 canonical authority로 재표시하지 않았다.

```text
BLOCKED_BY_T5F_WORKBENCH_FOUR_FAMILY_AUTHORITATIVE_STRUCTURED_RESULT_GAP
T5F_PRODUCT_IMPLEMENTATION_NOT_STARTED
CURRENT_RAW_STATE_SEMANTIC_INFERENCE_PRESERVED_AS_LEGACY_DEBT
SHARED_RUNTIME_TOOL_CONTRACT_OWNER_DECISION_REQUIRED
T5G_NOT_STARTED
```

## 2. 직접 확인한 현재 경로

### 2.1 공통 canonical owner

- `solutions/seamgrim_ui_mvp/ui/seamgrim_runtime_state.js:1542`
  - `extractCanonicalViewAuthorityInputsFromState`가 반환하는 family는 `console`, `graph`, `space2d`, `table`, `text`, `structure`, `grid2d`다.
  - `line`, `pendulum`, `projectile`, Workbench `grid` 입력은 없다.
- `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js:461`
  - `buildCanonicalViewPayloadSet`도 같은 family set만 소유한다.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2878`
  - 각 committed frame에서 위 canonical set을 만든다.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2900`
  - canonical set은 `buildCommittedSemanticViewPayload`에 전달된다.

### 2.2 네 가족의 현행 의미 합성

| family | 현행 의미 입력 | JS가 추가로 만드는 의미 | T5F 판정 |
|---|---|---|---|
| line | raw `x/y/a/b` channel/resource, frame history | point history, line equation/labels | authoritative family result 없음 |
| pendulum | raw `theta/omega/energy/L` aliases | `sin/cos(theta)` 기반 bob geometry, overlay, labels | authoritative family result 없음 |
| projectile | raw `x/y/t/vx/vy` aliases, frame history | ordered trajectory, current point, velocity overlay/labels | authoritative family result 없음 |
| grid | raw board/grid/piece aliases와 `view_meta.space2d` | dimension, entity position, geometry-source 선택, labels | Workbench-grid exact authority 없음 |

근거:

- `semantic_view_payload.js:4`의 `VIEW_CHANNEL_PREFERENCES`
- `semantic_view_payload.js:521`의 `resolveViewBinding`
- `semantic_view_payload.js:528`의 numeric fallback
- `semantic_view_payload.js:576`의 `buildCommittedSemanticViewPayload`
- `semantic_view_renderer.js:66`, `:120`, `:165`, `:211`의 네 family model

`semantic_view_renderer.js`의 네 model은 전달된 `canonical_views`를 읽지 않는다.

## 3. 기존 structured artifact가 이 공백을 자동으로 닫지 않는 이유

- 대표 물리 lesson에는 `seamgrim.space2d.v0`, `seamgrim.graph.v0`, `seamgrim.view_plan.v1` 자료가 있다.
- `view_plan_runtime.js`가 만드는 view-plan runtime은 `presentation_only: true`로 표기된다.
- Workbench의 primary family는 lesson의 `space2d` target과 별개인 `projectile`, `pendulum`, `grid`, `line`이다.
- 기존 graph/space2d를 어느 Workbench family의 정본으로 채택할지, 둘 이상일 때 precedence/ambiguity를 어떻게 처리할지, frame history와 trajectory identity를 누가 소유할지 정해져 있지 않다.
- T5E의 exact `seamgrim.nurimaker.grid_state.v1` grid2d는 Nurimaker grid-state 계약이다. 장기 지시문은 Workbench-grid와 grid2d를 성급히 합치지 말라고 명시한다.

따라서 기존 payload를 임의로 조합하는 것도 새로운 semantic contract 결정이며 구현자가 승인 없이 선택할 수 없다.

## 4. 실동작과 비후퇴 확인

현행 기능은 제거하지 않았다. 다음을 격리 worktree에서 직접 실행했다.

```text
node tests/seamgrim_workbench_semantic_view_payload_runner.mjs
PASS: seamgrim_workbench_semantic_view_payload: ok

node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs
PASS: seamgrim_workbench_semantic_view_renderer: ok

node tests/seamgrim_workbench_committed_view_verticals_browser_runner.mjs
PASS: seamgrim_workbench_committed_view_verticals_browser: ok
```

마지막 검증은 로컬 Playwright/Chromium cache만 사용했고 network install은 없었다. projectile, pendulum, grid, line의 기존 committed-state 표시·history·trajectory·overlay가 동작함을 재현했다. 이 PASS는 기존 기능 보존 증거일 뿐 canonical authority 충족 증거가 아니다.

## 5. Owner가 확정해야 할 exact 계약

다음 중 하나라도 미정이면 T5F 구현을 재개할 수 없다.

1. 네 family의 authoritative producer가 shared Rust runtime/tool인지, 기존 structured family의 명시적 합성 계약인지
2. family별 schema/version과 exact field set/order
3. state/result/frame/tick identity와 producer/version/provenance
4. trajectory/history의 owner, 순서, active cursor 경계, 중복·누락 처리
5. line의 point/equation 관계와 `a/b` 또는 point-series precedence
6. pendulum의 bob geometry가 runtime result인지 renderer presentation projection인지
7. projectile current point, trajectory, velocity vector의 exact 단위·identity·ordering
8. Workbench-grid의 board/cell/entity/draw geometry 계약과 `grid2d`/`space2d` 관계
9. missing/no-view/unavailable/invalid/unsupported/ambiguous 진단과 fail-closed 규칙
10. 기존 raw-state 경로의 explicit compatibility 기간과 provenance 표기

## 6. Owner 선택지

### OPTION_A — shared runtime/tool 네-family structured result

shared Rust runtime/tool가 family별 authoritative structured result를 생성하고, JS는 이를 canonical payload로 검증·정본화한 뒤 renderer에 전달한다.

- 장점: raw alias/history inference 제거 목표와 가장 직접적으로 일치한다.
- 필요 결정: 위 10개 exact 계약 전부.
- 권고: `RECOMMENDED`.

### OPTION_B — 기존 canonical family의 명시적 composition

Owner가 `graph / space2d / grid2d`와 explicit view-plan binding 중 어떤 조합이 각 Workbench family의 authority인지 exact mapping으로 지정한다.

- 장점: 기존 structured 결과 재사용 가능성이 있다.
- 위험: family mapping, precedence, temporal identity를 새로 결정해야 하며 `presentation_only` view-plan을 무심코 authority로 승격해서는 안 된다.
- 이 옵션도 exact mapping 승인 전 구현 불가다.

### OPTION_C — family split / partial defer

권위가 이미 충분한 family만 별도 vertical로 분리하고 나머지는 raw inference `LEGACY_DEBT`로 보존한다.

- 장점: 작은 후속 구현 가능.
- 한계: T5F 네-family closure와 T5G 진행 조건을 충족하지 않는다.

## 7. 비주장·보호 경계

```text
FEATURE_REMOVAL: 0
ACTIVE_VIEW_COUNT_CHANGE: 0
THIRD_VIEW_ABSTRACTION: 0
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
TRACKED_WASM_DIFF: 0
PUBLIC_STABLE_ABI_NOT_CLAIMED
NATIVE_IMPLEMENTATION_NOT_AUTHORIZED
WEB_S0_NOT_CLAIMED
HUMAN_PASS_NOT_CLAIMED
```

T5C stale UI-common expectation, T5D unsupported text-format golden gap, T4f mutation runner CRLF housekeeping은 기존 OPEN으로 보존한다.

## 8. 감사 입력 SHA-256

```text
6d8aa0e2170f72572a6757c4f11110f715a35df96687c16c220281b0f4f5718a  solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js
efbc88cd8bc770a7119b1504355aba40187e710086b08b3296ad26f363c580bf  solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js
a9250ba7b63eb23b5011824da93ff11fa5a05846d26c57dd0cdfc8ca61f71975  solutions/seamgrim_ui_mvp/ui/workbench/workbench.js
ad150ee45a445362a6e5ff9b46ea8477a8048e63f59c0ab37111c60d0685a5df  solutions/seamgrim_ui_mvp/ui/seamgrim_runtime_state.js
64d5cef51d695c0ba7d941abbc3e952a59a5552bd86606647e83f62bda4ec6b9  tests/seamgrim_workbench_semantic_view_payload_runner.mjs
51244364eb64ed44e064a2a8077ae7df0505e40254e4a365fd912d318359d9ba  tests/seamgrim_workbench_semantic_view_renderer_runner.mjs
887614bf4510f0a72f4f817ed27befc416718bb8066aa104fd3357356de60405  tests/seamgrim_workbench_committed_view_verticals_browser_runner.mjs
```
