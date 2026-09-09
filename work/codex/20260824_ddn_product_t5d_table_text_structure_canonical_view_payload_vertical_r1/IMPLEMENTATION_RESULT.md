# [셈그림Codex -> 제품구조Chat] T5D table + text + structure canonical payload — 결과

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5D_TABLE_TEXT_STRUCTURE_CANONICAL_VIEW_PAYLOAD_VERTICAL_R1
STATUS: IMPLEMENTED_UNDER_INDEPENDENT_REVIEW
DEEP_RESEARCH_CHECK: NOT_USE
BASELINE: 0c037a2ff4e4c6268ea8e4a82a1a23182a5234a8
IMPLEMENTATION_COMMIT: e0c687eb9eecef877eb0cf44d48a747acc98e8ec
EVIDENCE_FORMAT_CORRECTION: 29f88e2d8ddf4f1c7d526745fe02b1a0aa6ace45
HANDOFF_COMMIT: THIS_DOCUMENTS_ONLY_COMMIT_REPORTED_EXTERNALLY_AFTER_CREATION
BRANCH: codex/ddn-product-t5d-table-text-structure-canonical-view-payload-r1-20260824
WORKTREE: I:\home\urihanl\ddn\codex\build\worktrees\ddn-product-t5d-table-text-structure-canonical-view-payload-r1-20260824
```

## 1. Custody

- owner packet: `C:\Users\ddongosu\.codex\attachments\aaa9f21e-111c-4e1c-8755-edd1d0463da0\pasted-text.txt`
- packet bytes: `20,087`
- packet SHA-256: `b54abaaf7d09fb7a1258ee494b674d4bb694627ce270f84c07f6947311cffc56`
- packet-declared T5C implementation: `0c037a2ff4e4c6268ea8e4a82a1a23182a5234a8`
- packet-declared T5C independent verdict: `PASS`
- local T5C review commit/artifact: Git refs 및 `work/claude`에서 별도 원본을 발견하지 못했다. 이번 프로그램의 exact start baseline과 verdict는 owner packet의 고정 입력으로만 사용했다.
- implementation direct parent: `0c037a2ff4e4c6268ea8e4a82a1a23182a5234a8`
- evidence-format correction은 pack/test 7파일의 extra blank EOF만 제거하며 제품 의미·expected JSON 값·assertion을 바꾸지 않는다.
- merge commit count: `0`
- shared dirty root modification: `0`

## 2. 구현

제3 semantic owner를 만들지 않고 기존 `semantic_view_payload.js`를 확장했다.

- exact `seamgrim.table.v0`, `seamgrim.text.v0`, `seamgrim.structure.v0`만 native authoritative structured input으로 인정한다.
- identity missing은 `unavailable`, 입력 없음은 `no_view`, schema/content/identity/reference 위반은 `invalid`, unknown version은 `unsupported`, 복수 structured resource는 `invalid`로 fail-closed한다.
- table column key/order, text content/format, structure node id/order와 edge reference를 renderer-independent candidate payload에 보존한다.
- Run, Workbench, Playground가 동일 builder 결과를 소비한다.
- Run active path의 observation-output text compatibility fallback은 끄고, schema-less shape 객체를 canonical success로 승격하지 않는다.
- table/text/structure renderer는 canonical content만 전달받으며 HTML/Canvas/DOM은 payload identity에 포함하지 않는다.
- Rust/tool/runtime/WASM surface는 변경하지 않았다.

## 3. Golden·negative·mutation

- pack: `pack/seamgrim_table_text_structure_canonical_view_payload_v1/`
- payload hashes:
  - table: `candidate:fnv1a32:canonical_view_payload:c0bbf079`
  - text: `candidate:fnv1a32:canonical_view_payload:32002728`
  - structure: `candidate:fnv1a32:canonical_view_payload:b5f13a14`
- positive/cross-surface/order/identity assertions: `PASS`
- missing/no-view, invalid, unsupported, ambiguous, missing identity: `PASS`
- exact candidate diagnostics:
  - `E_CANONICAL_TABLE_INVALID_CANDIDATE`
  - `E_CANONICAL_TEXT_UNSUPPORTED_CANDIDATE`
  - `E_CANONICAL_STRUCTURE_INVALID_CANDIDATE`
- mutations:
  - `M1_TABLE_ROW_ORDER_DRIFT`: GREEN → RED → GREEN
  - `M2_TEXT_OUTPUT_SYNTHETIC_SUCCESS`: GREEN → RED → GREEN
  - `M3_STRUCTURE_NODE_IDENTITY_DRIFT`: GREEN → RED → GREEN
  - residue: `0`

## 4. 검증

PASS:

- `node tests/seamgrim_table_text_structure_canonical_view_payload_runner.mjs`
- `node tests/seamgrim_table_text_structure_canonical_view_payload_mutation_runner.mjs`
- actual browser: T5D table `2×2`, text heading, structure `2 nodes / 1 edge`
- T5B console/graph canonical runner
- T5C space2d canonical runner
- T1 RuntimeBridge
- T2 HostBridge
- T4 SourceAnalysis
- T4f observation channel
- Workbench semantic payload unit
- Workbench committed four-view actual browser
- Workbench view-instance actual browser
- Playground smoke `4/4`
- pendulum Bogae
- measurement actual browser
- Foundation12 actual browser `12 worlds × 4 = 48/48`
- bridge text/table/structure standalone/API parity `3/3`
- `node --check` for all changed/runtime test JS
- `git diff --check`

분류된 기존 test debt:

- `node tests/seamgrim_ui_common_runner.mjs`
- 결과: `ddn preprocess: moyang block removed`
- 분류: `BASELINE_PREEXISTING`
- 동일 오류가 untouched T5C worktree에서도 재현됐다. 제품 fallback이나 expected를 완화하지 않았다.

browser dependency는 network install 없이 기존 local Playwright `1.59.1`/Chromium revision `1217`을 task-owned junction으로 연결해 사용했고 검증 후 junction을 제거했다.

## 5. 변경 경계

```text
VIEW_TYPES_BEFORE: 14_ACTIVE / 2_REGISTRY_ONLY
VIEW_TYPES_AFTER: 14_ACTIVE / 2_REGISTRY_ONLY
FEATURE_REMOVAL: 0
THIRD_VIEW_ABSTRACTION: 0

TOTAL_SEMANTIC_AUTHORITY_DEBT_BEFORE: 12
TOTAL_SEMANTIC_AUTHORITY_DEBT_AFTER: 12
T5D_ACTIVE_FAMILY_CANONICAL_OWNERSHIP_GAPS_BEFORE: 3
T5D_ACTIVE_FAMILY_CANONICAL_OWNERSHIP_GAPS_AFTER: 0
ACTIVE_TEXT_OUTPUT_SEMANTIC_FALLBACK_BEFORE: 1
ACTIVE_TEXT_OUTPUT_SEMANTIC_FALLBACK_AFTER: 0

CROSS_SURFACE_PARITY: RUN_WORKBENCH_PLAYGROUND_BYTE_EQUIVALENT
STATE_HASH_DRIFT: 0
STORAGE_DRIFT: 0
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
TRACKED_WASM_DIFF: 0
TRACKED_WASM_SHA256: e306d83633576e373cdb3ddf7041c2fdb26a06e2491cb80ae2cb04d66151160b
NETWORK_INSTALL: 0
```

전체 debt가 `12`로 유지되는 이유는 historical `extractStructuredViewsFromState` compatibility decoder가 active canonical path 밖의 명시적 legacy custody로 남아 D08 family debt가 아직 삭제되지 않았기 때문이다. 이번 수직은 그 decoder를 canonical success에 사용하지 않는다.

## 6. 다음 gate

T5D는 semantic fallback 제거와 세 surface parity를 포함하므로 ClaudeCode fixed-HEAD independent review가 필요하다. plain `PASS` 전에는 T5E를 시작하지 않는다.

```text
WORKBENCH_VIEW_T5D_TABLE_TEXT_STRUCTURE_CANONICAL_PAYLOAD_IMPLEMENTED_UNDER_REVIEW
READY_FOR_DDN_PRODUCT_T5D_TABLE_TEXT_STRUCTURE_CANONICAL_VIEW_PAYLOAD_INDEPENDENT_REVIEW
NEXT_RECOMMENDED_VERTICAL_AFTER_PLAIN_PASS: T5E_CONSOLE_GRID_GRID2D_CELL_GRID
PUBLIC_STABLE_ABI_NOT_CLAIMED
SSOT_SPEC_PROMOTION_NOT_CLAIMED
NATIVE_IMPLEMENTATION_NOT_AUTHORIZED
WEB_S0_NOT_CLAIMED
HUMAN_PASS_NOT_CLAIMED
```

## 7. 독립 plain PASS 결속

2026-08-24 사용자 제공 독립 검토 결과가 다음 fixed scope에 plain `PASS`를 발행했다.

- review target: `e0c687eb9eecef877eb0cf44d48a747acc98e8ec`
- reviewed handoff/evidence correction: `29f88e2d8ddf4f1c7d526745fe02b1a0aa6ace45`
- blocking findings: `0`
- corrections required: `NONE`
- completion code: `WORKBENCH_VIEW_T5D_INDEPENDENT_REVIEW_PASS`
- `MAY_CLOSE_T5D: YES`

별도 review commit·보고서 경로·bytes·SHA-256은 전달되지 않아 추정하지 않았다. 원문 provenance와 비차단 follow-up 2건은 `INDEPENDENT_PASS_BINDING.md`에 분리 기록했다.

```text
WORKBENCH_VIEW_T5D_TABLE_TEXT_STRUCTURE_CANONICAL_PAYLOAD_CLOSED
WORKBENCH_VIEW_T5D_INDEPENDENT_PLAIN_PASS_BOUND
T5D_TEXT_FORMAT_UNSUPPORTED_GOLDEN_COVERAGE_FOLLOW_UP_OPEN
SEAMGRIM_UI_COMMON_MOYANG_EXPECTATION_BASELINE_DEBT_OPEN
NEXT_VERTICAL: T5E_CONSOLE_GRID_GRID2D_CELL_GRID
```
