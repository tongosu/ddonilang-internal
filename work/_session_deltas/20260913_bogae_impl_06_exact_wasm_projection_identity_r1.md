# [보개투영 Work -> 또니랑 개발 관리자] BOGAE-IMPL-06 exact WASM projection identity R1 — 제품 인계

```yaml
AI_PROVIDER: OpenAI
AI_SURFACE: Codex VSCode
AI_CAPABILITY: local product implementation
SESSION_NICKNAME: 보개투영 Work
PROJECT_ROLE: Bogae product writer
RETURN_LABEL: 또니랑 개발 관리자

ACTION: PRODUCT DEVELOPMENT ONLY
INDEPENDENT_REVIEW: NOT_PERFORMED
SELF_PASS: NO
```

## 1. 권위와 계보

```yaml
LIVE_SSOT: v25.83.0 / RD-001~621
PUBLIC_SPEC: v0.7.0

BOGAE_IMPL_01:
  PRODUCT: 8c0781d1ac10dabea4b4e5699f6b26823bc23dc4
  STATUS: CLOSED_TARGET_BOUND

BOGAE_IMPL_04:
  PRODUCT: 2ace20a8bb506748bb5ae43746601c5926f2361c
  REVIEW: 4197f5a98f512c1ce9d9df267d4fb675fd50736d
  STATUS: CLOSED_TARGET_BOUND

BOGAE_IMPL_05:
  PRODUCT: d6d0bfc14fd5c378ba2cca3a397d77b13d22e3d8
  HANDOFF: a9ef081e058ba3dcf198007bd3a2e12b2c2a492b
  REVIEW: 4611ee31cd3f85367af009d9ee621950bdfc9526
  STATUS: CLOSED_TARGET_BOUND

PRODUCT: e3c334eff053d6594740a24e6e1c0c447c179ace
PRODUCT_TREE: a0fc7d402858fb97888037eadf4a7d0f98395be1
PRODUCT_PARENT: 4611ee31cd3f85367af009d9ee621950bdfc9526
```

BOGAE-IMPL-01의 typed `BogaeRuntimeValue::View`/`Scene`/`SceneElement`와 exact provider identity를 재사용했다. 새 언어·semantic identity·public wire는 추가하지 않았다.

## 2. 단독 writer와 변경 경로

```yaml
WORKTREE: I:/home/urihanl/ddn/codex/build/worktrees/ddn-bogae-impl-06-wasm-projection-r1-20260913
BRANCH: ddoni/bogae-impl-06-wasm-projection-r1-20260913
PATH_LEASE:
  - tool/src/ddn_runtime.rs
  - tool/src/wasm_api.rs
SHARED_DIRTY_ROOT_USED_AS_WRITER: NO
```

## 3. 구현된 제품 수직

- run-local typed View binding이 정확히 1개일 때만 exact projection을 수행한다.
- exact provider/profile은 `표준보기.장면 + scene + plane2`와 `표준장면.평면`이다.
- `가로범위`, `세로범위`, `요소들`을 authored typed roles에서만 읽는다.
- circle/polygon/text는 exact provider와 typed element kind가 동시에 맞을 때만 기존 `seamgrim.space2d.v0` adapter 값으로 투영된다.
- View binding이 0개일 때만 기존 legacy draw-list 경로를 `explicit_compatibility_adapter` provenance로 유지한다.
- typed View가 2개 이상이거나 profile/provider/role/geometry가 맞지 않으면 `E_BOGAE_UNSUPPORTED` 경계에서 typed fail-closed하며 legacy projection을 조회하지 않는다.
- space3에서 camera/bounds를 합성하지 않는다.
- authored element order를 그대로 보존한다.
- projection은 world/View/Bogae 값이나 committed frame/state hash를 수정하지 않는다.

```yaml
EXACT_TYPED_IDENTITY_ONLY: YES
STRING_OR_SUBSTRING_WINNER: 0
SOURCE_OR_MAP_ORDER_WINNER: 0
LEGACY_FALLBACK_AFTER_TYPED_VIEW: 0
AUTO_BOUNDS: 0
AUTO_CAMERA: 0
GEOMETRY_REPAIR: 0
SEMANTIC_INPUT_MUTATION: 0
```

## 4. 물리 case 결속

```yaml
BIC_SCENE_GEOMETRY_01:
  STATUS: PASS
  EVIDENCE: exact plane2 provider, authored bounds, element order and provider identity

BIC_SCENE_GEOMETRY_02:
  STATUS: PASS
  EVIDENCE: missing horizontal bounds fails without observed-data repair

BIC_UNSUPPORTED_01:
  STATUS: PASS
  EVIDENCE: two typed View bindings fail as typed_view_binding_ambiguous; no legacy winner

BIC_UNSUPPORTED_02:
  STATUS: PASS
  EVIDENCE: space3 View fails as typed_view_projection_unsupported; no camera/bounds synthesis

BIC_NATIVE_WASM_01:
  STATUS: PARTIAL_APPLICABLE_PASS
  EVIDENCE: shared exact projector native tests PASS and wasm32 library compile PASS
  NONCLAIM: no standalone browser/WASM executable oracle was run
```

## 5. 검증

```yaml
FOCUSED_RUNTIME:
  COMMAND: cargo test -p ddonirang-tool --lib bogae_exact_ --offline
  RESULT: PASS 4/4

FOCUSED_WASM_META:
  COMMAND: cargo test -p ddonirang-tool --lib --features wasm build_view_meta_ --offline
  RESULT: PASS 6/6

NATIVE_CHECK:
  COMMAND: cargo check -p ddonirang-tool --lib --offline
  RESULT: PASS

WASM32_CHECK:
  COMMAND: cargo check -p ddonirang-tool --lib --features wasm --target wasm32-unknown-unknown --offline
  RESULT: PASS

DIFF_CHECK: PASS
```

제품 고정 전 native 전체 lib 회귀는 한 번 실행했다.

```yaml
FULL_NATIVE_LIB_REGRESSION:
  RESULT: 661 PASS / 39 FAIL
  TARGET_CASES: ALL NEW BOGAE_IMPL_06 TESTS PASS
  FAILURE_DISPOSITION: inherited unrelated isolated-environment/name-lint/project-authoring/runtime-surface baseline failures
  BROAD_FULL_PASS_CLAIMED: NO

NATIVE_HOST_WITH_WASM_FEATURE_FULL_TEST:
  RESULT: NOT_APPLICABLE_AS_FULL_GATE
  REASON: existing wasm-bindgen JsValue test aborts on non-wasm host target
```

## 6. 독립 mutation

각 mutation을 단독 적용하고 해당 focused gate가 RED가 된 뒤 fixed bytes로 정확 복원하고 GREEN을 재확인했다.

```yaml
M1:
  CHANGE: ambiguous typed View를 fail-closed 대신 no-typed-view로 강등
  RED: PASS / exit 1
  RESTORE_GREEN: PASS

M2:
  CHANGE: authored horizontal lower bound 대신 0.0 자동값 사용
  RED: PASS / exit 1
  RESTORE_GREEN: PASS

FIXED_FILES:
  tool/src/ddn_runtime.rs:
    GIT_BLOB: cf395b51cf4a32b296418c8abb85a8b859742e57
    SHA256: 023E7655DFC06D146CEA9ACB980EF1D952D9B46D5E26006C84433A04AEBFD8D5
    BYTES: 1243970
  tool/src/wasm_api.rs:
    GIT_BLOB: 37d9cdee9622993e25fa19ce02d2a7a3487172b3
    SHA256: C81CB06F4D80DB5E9F12C440535A33864AFBD14252C61E20E2450F11E05CDF87
    BYTES: 189415
```

## 7. 범위 경계와 다음 단계

다음을 주장하지 않는다.

- BOGAE-IMPL-07 shared frontdoor
- full-headless lifecycle
- browser Host 실행
- typed View의 Local Workspace persistence/restore
- whole Native/WASM executable parity
- whole Bogae/Workbench
- V1 readiness, release, Human PASS

```yaml
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
PUSH: NO
INDEPENDENT_REVIEW_READY: YES
FINAL_STATUS: PRODUCT_FIXED_PENDING_BATCH_INDEPENDENT_REVIEW
NEXT_ALLOWED_ACTION: 별도 검증 Work에서 e3c334eff053d6594740a24e6e1c0c447c179ace target-bound independent review
```
