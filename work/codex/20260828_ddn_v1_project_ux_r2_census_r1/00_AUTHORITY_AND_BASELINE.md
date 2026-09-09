# DDN V1 PROJECT_UX_R2 권위·기준선

## 세션 선언

```yaml
AI_PROVIDER: OpenAI
AI_SURFACE: Codex VSCode
AI_CAPABILITY: isolated repository census and design-evidence custody
SESSION_NICKNAME: 셈그림ProjectUXR2전수조사Codex
PROJECT_ROLE: PRODUCT_CENSUS_SINGLE_WRITER
RETURN_LABEL: 셈그림Codex -> Codex관리Work
DEEP_RESEARCH_CHECK: NOT_USE
FROM: Codex관리Work
TO: 셈그림Codex
RETURN_TO: Codex관리Work
PARENT_PERSISTENT_GOAL: DDN-LONG-RELINT-PRODUCT-01
NEW_GOAL_CREATED: NO
PRODUCT_IMPLEMENTATION: NO
```

## 관리 보정과 원문 custody

- 관리 보정: `DDN-P-V1-PROJECT-UX-R2-CENSUS-R1`을 먼저 적용했다.
- ProductChat 원문: `DDN V1 PROJECT_UX_R2 정합·저장소 전수조사 R1`
- 제공 원문 bytes: `11,397`
- 제공 원문 SHA-256: `49c914b613facc46bc6a052106e37eb7510871d6955750e15a7c2edd785ebca7`
- 관리 보정 bytes: `11,893`
- 관리 보정 SHA-256: `a8003e0c9d31b6781e4d08e72483d3df39b631dffe33d9309f74120034b5b209`
- `PASS_CENSUS_READY_FOR_FD02A`는 영향분석과 review ticket이 준비됐다는 뜻뿐이다. FD02A 구현·독립 PASS·제품 완료를 뜻하지 않는다.

```yaml
INSTRUCTION_BASELINE: DDN-P-V1-PROJECT-UX-R2-CENSUS-R1 management correction
SUCCESSOR_BASELINE: 68974d053c6df2f1b855523b8b5eee39625d2e8c
SSOT_CURRENT_IDENTITY: v25.15.0 / b51fc82e5b922b14e10e48e733f0398d85f4d0b9cb22477ac10e08cef19e3777
INSTRUCTION_REFRESH_STATUS: APPLIED
SSOT_REFRESH_STATUS: REVERIFIED_UNCHANGED
SSOT_UPDATE_REQUEST: NOT_REQUIRED_FOR_THIS_DOCS_ONLY_CENSUS
DELTA_IMPACT: output structure and non-claim boundaries strengthened; product semantics unchanged
RE_REVIEW_TRIGGER: NOT_APPLICABLE_DOCUMENT_CENSUS_ONLY
PROGRAM_CLOSURE: NOT_APPLICABLE_PARENT_GOAL_CONTINUES
```

## Git 기준선

```yaml
PRIMARY_CENSUS_BASELINE: 6824ef7c21d5a0b95d67ae0048159ed79dcd7683
WORKTREE: I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828
BRANCH: codex/ddn-p-v1-project-ux-r2-census-r1-20260828
START_CLEAN: true
START_STAGED_COUNT: 0
SHARED_ROOT_HEAD: a000e262cb96b51007286e2fb70bb2fa31e2af32
SHARED_ROOT_TRACKED_DIRTY_ROWS: 201
SHARED_ROOT_STAGED_COUNT: 0
SHARED_ROOT_STATUS_BLOB: 3e9858a7c3115454cea1525055a4c4a888820fad
```

shared dirty root는 읽기 전용으로만 조사했다. reset, stash, clean, checkout, stage를 수행하지 않았다.

## current 권위

`6824ef7c...`에는 `docs/ssot/**`가 없으므로 current 권위 파일은 shared root에서 읽기 전용으로 검증했다. 이 외부 current와 census Git 기준선을 혼합하지 않는다.

```yaml
INTERNAL_SSOT_CURRENT: v25.15.0
SSOT_RANGE: RD-001..RD-437
SSOT_ALL: docs/ssot/ssot/SSOT_ALL_v25.15.0.md
SSOT_ALL_SHA256: b51fc82e5b922b14e10e48e733f0398d85f4d0b9cb22477ac10e08cef19e3777
SSOT_MANIFEST: docs/ssot/ssot/SSOT_ALL_MANIFEST_v25.15.0.md
SSOT_MANIFEST_SHA256: f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4
SSOT_SEAL: docs/ssot/ssot/CURRENT_SHA256_v25.15.0.md
SSOT_SEAL_FILE_SHA256: 7df920afe46aa6495d1a85bc7a4745370ee3adde063301ac033a5a050b8b17d2
SSOT_LIVE_FAMILY_COUNT: 39
SSOT_MANIFEST_ROW_COUNT: 259
SSOT_DIRECT_INPUT_COUNT: 221
PUBLIC_LANGUAGE_SPEC_CURRENT: v0.6.0
PUBLIC_SPEC_POINTER: publish/spec/CURRENT.md
WORKSPACE_BUNDLE_CURRENT: v24.35.1_20260813_gaji-resolution-lock-v1-candidate-r3
WORKSPACE_BUNDLE_ARCHIVE_SHA256: f6d75ac4b04f38739d6a9936227ffb81e81868bff824cde912e6e26e1eb7451b
WORKSPACE_BUNDLE_MANIFEST_SHA256: 97f6554c24d0b2a89aeb3190a5febdde4230498ebdc4156c643d8fd8a969ba9f
OPERATING_POLICY: 0.15.1 overlay
COMMON_OPERATIONS: 0.14.0 base + 0.15.0 successor closure + 0.15.1 session refresh overlay
```

`docs/ssot/CURRENT.md`와 `docs/ssot/ssot/CURRENT.md`의 “public Language SPEC v0.5.0 유지” 문구는 실제 `publish/spec/CURRENT.md = v0.6.0`과 다르다.

```text
AUTHORITY_METADATA_DRIFT
PUBLIC_SPEC_LIVE_POINTER_V0_6_0_CONTROLS
SSOT_MANAGER_FOLLOW_UP_ONLY
SSOT_DIRECT_EDIT_NOT_AUTHORIZED
```

## WIP 계약

- 새 작업 전 tracked dirty/staged를 먼저 확인한다.
- shared dirty root를 정리하지 않는다.
- SSOT와 public SPEC는 직접 수정하지 않는다.
- 독립 PASS가 없는 side 후보를 current 제품 사실로 승격하지 않는다.
- 활성 goal 수와 unmerged proposal 수 제한을 지킨다. 이번 과업은 Owner가 명시한 기존 goal의 read-only census successor다.
- 제품 구현은 금지되어 FD02A/FD02B/FD03 ticket까지만 작성한다.

## side lineage custody

| Evidence | Commit | Primary baseline 관계 | 판정 | 사용 방식 |
|---|---|---|---|---|
| Editable R0 | `36e0441b75c828e1756a1ce363dff88442525ca3` | merge-base `305dd9d3...`; 비조상 | `REVIEW` 문서 근거 | read-only |
| Editable I1 fixed | `d0ff23389e27b8268fe9eead8d0138abd6d77b06` | 별도 선형 side lineage | `IMPLEMENTED_PENDING_REVIEW` | 영향표와 채택 조건만 추출 |
| Editable I1 review parent | `2d489c8d9b2651f5314afdfa4a453568622dfbfd` | `d0ff2338...`의 direct child | 독립 verdict commit 없음 | review request custody |
| R3O correction | `de7efbb4556397ca15fc167225cfdd055d591116` | 비조상 docs-only side | `CLOSED` 문서 증거 | read-only |
| R3N-FU01 fixed | `9389563e752fcc63b0425e05671473e1adb42ced` | `6824ef7c...`의 조상 | 제품 기준선 포함 | census current |
| R3N-FU01 review parent | `6824ef7c21d5a0b95d67ae0048159ed79dcd7683` | primary baseline | review 대기 계보 | 변경 금지 |

Editable 선형 계보는 `f8152501 → 36e0441 → 985533c0 → ecac39c7 → 727168af → a8a7af99 → f53f45a6 → 74169681 → cfdea843 → c2492bc7 → d0ff2338 → 2d489c8d`이며 merge commit은 없다. 어느 side commit도 자동 병합하지 않았다.

## 보호 자원 시작값

```yaml
OFFICIAL_DB: I:/home/urihanl/ddn/codex/official-store/seamgrim-local-official-v1/seamgrim_projects.sqlite3
OFFICIAL_DB_BYTES: 573440
OFFICIAL_DB_SHA256: 3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
PID_53196: ABSENT
PORT_8787: NOT_LISTENING
OFFICIAL_WRITE_COUNT: 0
ACTIVATION_CALL_COUNT: 0
NETWORK_DOWNLOAD_COUNT: 0
```
