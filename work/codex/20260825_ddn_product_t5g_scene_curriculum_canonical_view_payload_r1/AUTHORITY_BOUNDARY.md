# [셈그림Codex -> 제품구조Chat] T5G scene/curriculum canonical payload authority boundary

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5G_SCENE_CURRICULUM_CANONICAL_VIEW_PAYLOAD_VERTICAL_R1
BASELINE: d49a45faa963aaddd529052a1811e09109dd8e47
T5F_FIXED_HEAD: 0abec54b30b26dbe99ce249aa3de5d7681907eab
T5F_PASS_BINDING: dd8f560c93b9454a2cd92b5921ecea89055135ac
DEEP_RESEARCH_CHECK: NOT_USE
```

## Existing owner

- canonical owner는 기존 `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js` 하나다.
- 제3 semantic/view abstraction을 만들지 않는다.
- `seamgrim.scene.v0`는 기존 session/presentation wrapper로 보존한다.
- `seamgrim.curriculum_semantic_scene.v0`는 기존 educational/presentation wrapper로 보존한다.
- wrapper의 localStorage, timestamp, view config, timeline/layers, DOM selector, accessibility text, browser reading order는 canonical identity가 아니다.

## Candidate projection and family contract

```text
SCENE_PROJECTION_SCHEMA: seamgrim.scene_summary_semantic_projection.v1_candidate
SCENE_CANONICAL_FAMILY: scene-summary
CURRICULUM_PROJECTION_SCHEMA: seamgrim.curriculum_semantic_scene_projection.v1_candidate
CURRICULUM_CANONICAL_FAMILY: curriculum-semantic-scene
CANONICAL_ENVELOPE: seamgrim.semantic_view_payload.v1_candidate
PUBLIC_ABI_OR_SCHEMA_PROMOTION: NO
```

### scene-summary

- explicit primary family가 있으면 그 family만 선택한다.
- explicit primary가 없고 authoritative available candidate가 정확히 하나이면 그 하나를 선택한다.
- 둘 이상이면 `ambiguous`; 0개이면 authoritative status를 보존하며 임의 graph default를 만들지 않는다.
- selected payload는 exact canonical envelope, matching family, `available`, non-empty candidate hash를 요구한다.
- graph points에서 timeline/layer를 만들거나 required-view 문자열만으로 semantic success를 만들지 않는다.
- wrapper layer/time/view config는 presentation/session metadata로 남을 수 있으나 nested canonical payload에는 들어가지 않는다.

### curriculum-semantic-scene

- validated curriculum card의 lesson/world/primary-view, control/observation anchor identity와 committed binding value를 semantic projection으로 사용한다.
- primary view는 exact canonical view payload에 결속한다.
- anchor id는 non-empty unique이고 kind는 `control|observation`, binding source는 `slider_panel|committed_observation_payload`만 허용한다.
- DOM selector, a11y label, browser reading order, prompt presentation은 wrapper에만 남고 canonical payload에서는 제외한다.
- primary canonical view가 없거나 invalid/unsupported/ambiguous이면 curriculum canonical success로 승격하지 않는다.

## Fail-closed

```text
AVAILABLE: exact projection + identity + authoritative canonical primary
NO_VIEW: declared semantic view absent
UNAVAILABLE: required identity/provenance unavailable
INVALID: exact family but malformed content/identity
UNSUPPORTED: unknown projection or nested schema/version
AMBIGUOUS: multiple equal authoritative candidates
SILENT_PICK_FIRST: 0
LEGACY_SYNTHETIC_AVAILABLE: 0
```

Candidate diagnostics remain product-local:

- `E_CANONICAL_SCENE_SUMMARY_INVALID_CANDIDATE`
- `E_CANONICAL_SCENE_SUMMARY_UNSUPPORTED_CANDIDATE`
- `E_CANONICAL_SCENE_SUMMARY_AMBIGUOUS_CANDIDATE`
- `E_CANONICAL_CURRICULUM_SCENE_INVALID_CANDIDATE`
- `E_CANONICAL_CURRICULUM_SCENE_UNSUPPORTED_CANDIDATE`
- `E_CANONICAL_CURRICULUM_SCENE_AMBIGUOUS_CANDIDATE`

## Non-goals

- SSOT/public SPEC change
- public stable ABI/schema
- Native renderer implementation
- registry-only `space3d`/`grid3d` activation
- localStorage or project portable stability promotion
- pixel parity
