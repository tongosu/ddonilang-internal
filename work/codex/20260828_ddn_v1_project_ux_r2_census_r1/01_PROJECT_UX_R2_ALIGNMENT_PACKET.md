# PROJECT_UX_R2 정합 packet

## 승인 용어와 현행 owner 매핑

| 사용자 용어 | 목표 의미 | 현행 구현 owner | 정합 판정 |
|---|---|---|---|
| 또니랑 글 | `.ddn` source | `tool/src/local_project.rs::VirtualProjectFileSource`, `lang` parser | `ALIGNED` |
| `처음.ddn` | 기본 생성 파일명 | 현행 기본 `lesson.ddn`, 정식 root `뿌리.ddn` | `CONFLICT` |
| 첫글 | semantic entry role | `NormalizedProjectManifest.entry_path`; `extract_ddn_first_entry` | `PARTIAL` |
| 차림새 | 사람 의도의 project manifest | 현행 `뿌리.ddn` project block + `ddn.project.json` | `MISSING` 명칭/구조, `PARTIAL` 의미 |
| 곳간 | 명시 asset membership | `ddn.asset.json`, sealed dataset registry | `PARTIAL` |
| 가지 | dependency | vendored `gaji.toml`, `LocalGajiPin` | `ALIGNED` 내부 의미 |
| 가지잠금 | exact dependency resolution | `ddn.lock`, `LocalGajiLock` | `PARTIAL`, wire `OPEN_BY_SSOT` |
| 가지 맞추기 | 별도 atomic update UX | `teul-cli gaji update` | `PARTIAL`; Workbench UX 없음 |
| 글판 / 또니랑 글판 | SourceEpoch 선택 | `lang::ast::SourceEpoch`; project owner 없음 | `MISSING` |
| 프로젝트 뿌리 | project root concept | `PROJECT_ROOT_FILE = 뿌리.ddn` | `PARTIAL`; manifest와 root file 결합 |
| 씨 / 씨 체계 | type/type system 사용자 표현 | parser diagnostics는 혼합 표기 | `PARTIAL` |

내부 Rust/IR/API 이름은 그대로 유지할 수 있다. 이 packet은 public syntax, schema, wire를 확정하지 않는다.

## 목표 UX와 현행 현실

### 가장 작은 프로그램

단일 `.ddn` 실행 경로는 `tools/teul-cli/src/cli/run.rs`와 `tool/src/ddn_runtime.rs::DdnProgram::from_source*`에 존재한다. 다만 기본 SourceEpoch는 PreV25이며 project-owned `글판`이 아니다.

### 가장 작은 정식 프로젝트

목표는 `처음.ddn + 차림새`다. 현행 정식 discovery는 `뿌리.ddn`을 우선하고 `ddn.project.json`을 fallback으로 쓴다. `처음.ddn`은 현재 생성 기본도, manifest-independent entry authority도 아니다. 따라서 이름만 바꾸는 패치가 아니라 discovery/manifest/compatibility 분리가 필요하다.

### 차림새 의미 분리

현행 `NormalizedProjectManifest`는 `entry_path`, file hashes, project JSON hash, graph hash, lock hash를 한 canonical manifest에 모은다. 사람 설명 필드와 실행 의미 필드의 두 identity가 제품 타입으로 분리되어 있지 않다.

권고 candidate contract:

- `AuthoredManifestIdentity`: 원문 보관 identity.
- `SemanticProjectConfigIdentity`: 글판, 첫글, 가지 요구, 명시 곳간 membership, 실행 의미 config만 포함.
- 설명/이름/작성자/태그는 execution identity에서 제외.
- exact field/schema/order는 SSOT/Owner 결정 전 OPEN.

### 가지잠금

`build_project_gaji_lock(source, require_existing_lock)`은 vendored `gaji.toml`을 전수해 graph/package hash를 만들고 `ddn.lock` canonical bytes를 비교한다. lock 누락 frozen 경로는 `E_LOCK_MISSING`, 불일치는 `E_LOCK_HASH_MISMATCH`로 fail-closed한다. Run은 lock writer를 호출하지 않는다.

다만 `ddn.lock.v0-local` physical fields는 local candidate다. public stable `가지잠금` wire로 선언하지 않는다.

### 실행 불변식

| 불변식 | 현행 | R2 결론 |
|---|---|---|
| Run이 lock 변경 0 | `build_project_run_summary`는 read/compare만 수행 | 보존 |
| Run 중 dependency update 0 | local project run은 vendored graph만 읽음 | 보존 |
| Run 중 network resolution 0 | local project path에는 network client 없음 | 보존; 별도 `gaji update`와 분리 |
| content sniff epoch fallback 0 | epoch는 API 선택이지만 project selection owner 없음 | project manifest 기반 explicit selection 필요 |
| lock mismatch fail-closed | 구현됨 | 보존 |
| Rust semantic identity authority | project graph/lock은 Rust | 확대 |
| JS가 snapshot identity 발명 금지 | Workbench snapshot/local fallback에 JS FNV/shape가 존재 | `CONFLICT`; Rust 봉인 필요 |

## 네 상태 분리

| 목표 상태 | 현행 대응 | 판정 |
|---|---|---|
| EditorGeneration | `sourceAnalysisGeneration`, persistence generation | `PARTIAL`; typed project generation 아님 |
| RecoveryCheckpoint | every-input localStorage draft/native catalog | `PARTIAL`; bounded recovery ledger 아님 |
| SavedProjectRevision | server `revisions` + explicit save | `ALIGNED` 핵심 |
| ExecutionSnapshot | in-memory run input/recipe; server run revision link | `PARTIAL`; current saved head와 exact Rust envelope 결속 부족 |

글자 입력은 server `revisions`를 만들지 않고, Run도 SavedProjectRevision을 자동 생성하지 않는다. 그러나 every-input localStorage 쓰기와 server saved head 대비 unsaved execution의 권위가 분리되어야 한다.

## Editable I1 영향 matrix

Editable I1 fixed `d0ff2338...`은 primary lineage에 병합하지 않은 제품 후보다. 독립 plain PASS가 없으므로 아래는 구현 존재/claimed evidence 분류이지 승인 판정이 아니다.

| FD02A 요구 | I1 상태 | exact evidence | R2 재검토/채택 조건 |
|---|---|---|---|
| server saved HEAD exact binding | 구현됨 | `project_store.py::create_run(expected_head_revision_id)`, descriptor response | clean targeted plain PASS |
| stale unsaved source Run fail-closed | 구현됨 | `tool/src/source_epoch.rs::build_editable_revision_execution_envelope`, `E_EDITABLE_SERVER_HEAD_STALE` | R2 identities로 rename/adapter 결정 |
| Rust canonical source-tree identity | 구현됨 | `normalized_source_tree`, `source_tree_sha256` | `차림새/글판/가지잠금/곳간` inputs 포함 여부 재검토 |
| analysis/execution same snapshot | 구현됨 | analysis revision + source tree checks | primary frontdoor adoption test |
| forged JS envelope/receipt 거부 | 구현됨 | typed candidate schema + identity recomputation | WASM/CLI/Workbench parity review |
| execution receipt | 구현됨 | `editable_revision_execution_receipt_json` | public/stable claim 금지, candidate 유지 |
| atomic object custody | 구현됨 | `orphan_object_candidates`, stage/write/transaction/clear | crash/GC policy와 FD02B 재검토 |
| silent local fallback 제거 | 구현됨 | Workbench catch-path 축소, unknown local schema reject | UX-visible mode and recovery policy review |
| typed EditorGeneration/Recovery/Saved/Execution identities | 일부 | analysis generation, revision descriptor, envelope | exact four-state product model 부족 |
| project-owned SourceEpoch | 테스트/문서 또는 candidate 제한 | I1은 `PreV25-only`; V25 reject | FD03 범위, FD02A에서 발명 금지 |
| R2 차림새 semantic identity | 누락 | I1 uses current local project tree | manifest successor 필요 |
| bounded recovery + GC | 누락 | orphan custody receipt only | FD02B |
| `처음.ddn` non-magic + `첫글` authority | 누락 | current entry path carried through | later manifest vertical |

### product-first 계보 채택 조건

1. `d0ff2338...` 제품 diff에 대한 fresh targeted independent plain PASS.
2. primary baseline/후손에 의미 충돌 없이 선형 재적용; side lineage 자동 merge 금지.
3. current R3N-FU01 review 대상과 overlap/drift 재검증.
4. candidate-only schema/PreV25 limitation을 명시하고 public/stable wire로 승격하지 않음.
5. R2 semantic config/epoch/lock/resource identities와 결합할 때 새 mutation matrix 수행.
6. tracked WASM refresh 및 default activation은 별도 승인까지 0.

## 정합 결론

```yaml
PROJECT_UX_R2_ALIGNMENT: PASS_WITH_BOUNDED_CONFLICTS
NEW_PUBLIC_SYNTAX: 0
EXACT_SCHEMA_WIRE_DECIDED: 0
PRODUCT_IMPLEMENTATION: 0
FD02A_DUPLICATE_IMPLEMENTATION: FORBIDDEN
EDITABLE_I1_DISPOSITION: IMPLEMENTED_PENDING_REVIEW_SIDE_CANDIDATE
```
