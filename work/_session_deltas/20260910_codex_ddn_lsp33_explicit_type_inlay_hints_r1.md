# DDN-LSP33-EXPLICIT-TYPE-INLAY-HINTS-R1 — 결과

## 기준과 계보

ini:
LIVE_AUTHORITY = v25.72.0 / RD-001~598
PUBLIC_SPEC = v0.6.0
LSP32_PRODUCT = 985fea19ad7aa3f33cffe43021ff6d9e5d19a65f
LSP32_HANDOFF = e9ef6f40d849ca922dd0516251f51692e8c35f47
LSP33_PRODUCT = 9345563ff70f07405035caf90ac608aad8e33d47
LSP33_TREE = 673d40ce8d76b59be4b8e5fda742d3a73b40fc8f
LSP33_PARENT = e9ef6f40d849ca922dd0516251f51692e8c35f47
MERGE_COUNT = 0

LSP32 target와 review 경계는 수정하지 않았고, LSP33을 successor로 고정했다.

## 제품 수직

textDocument/inlayHint의 기존 typed owner를 확장했다.

- 기존 signature_help.rs의 typed AST와 ParamPin binding을 재사용한다.
- 기존 symbol.rs의 type_surface presentation을 재사용한다.
- TypeRef::Infer는 hint를 만들지 않는다.
- 명시적 type과 resolved positional ParamPin이 모두 있을 때만 param:type label을 게시한다.
- definitionIdentity, paramPinId, version, snapshot identity metadata를 유지한다.
- 결과를 deterministic source order로 반환하고 1000개로 제한한다.
- didChange current snapshot, didClose empty, stale version/snapshot, cancellation fail-closed를 보장한다.
- parser, type inference, new registry, new identity, filesystem scan, remote, upload는 추가하지 않았다.

현재 typed authority가 있는 .ddn만 지원한다. .ddl/.옮김에는 새 typed owner를 추측해 추가하지 않았다.

변경 product paths:
tool/src/lsp/server.rs
tool/src/lsp/signature_help.rs
tool/tests/lsp_signature_help.rs
tests/run_lsp0_transport_document_sync_check.py

## 검증

lsp_signature_help: 4 passed
lsp_formatting: 4 passed
lsp_diagnostics: 11 passed
lsp_document_symbol: 4 passed
lsp_references: 4 passed
lsp_rename: 5 passed
FAILED_BINARIES = 0

IH23_BLACKBOX_INLAY_HINT_BEFORE_EOF = PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK = PASS
cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check = PASS

Coverage: explicit Korean type labels, ParamPinId, emoji UTF-16 positions, deterministic repeat, inferred-only empty result, string/comment empty result, didChange, didClose, stale -32801, stale snapshot -32802, cancellation -32800, before-EOF transport.

## Mutation evidence

### M1 — inferred parameter hint 생성

TARGET = tool/src/lsp/signature_help.rs
BASE_SHA256 = 7A0D15810A4E64C285EBA00FC933A5CFC4817AB089BDE4661E05DD081882EF27

Exact mutation and restore:
- if matches!(param.type_ref, TypeRef::Infer) { continue; }
+ if false && matches!(param.type_ref, TypeRef::Infer) { continue; }
restore:
- if false && matches!(param.type_ref, TypeRef::Infer) { continue; }
+ if matches!(param.type_ref, TypeRef::Infer) { continue; }

RED: lsp33_inlay_hints_require_explicit_types_and_preserve_utf16 failed; 3 passed, 1 failed.
RESTORE_SHA256 = 7A0D15810A4E64C285EBA00FC933A5CFC4817AB089BDE4661E05DD081882EF27
GREEN: lsp_signature_help — 4 passed, 0 failed.

### M2 — UTF-16을 UTF-8으로 강등

Exact mutation and restore:
- let position = byte_offset_to_position(source, arg.span.start, encoding)
+ let position = byte_offset_to_position(source, arg.span.start, PositionEncoding::Utf8)
restore:
- let position = byte_offset_to_position(source, arg.span.start, PositionEncoding::Utf8)
+ let position = byte_offset_to_position(source, arg.span.start, encoding)

RED: lsp33_inlay_hints_require_explicit_types_and_preserve_utf16와 lsp18_inlay_hints_reuse_param_identity_and_live_snapshot가 실패; 2 passed, 2 failed.
RESTORE_SHA256 = 7A0D15810A4E64C285EBA00FC933A5CFC4817AB089BDE4661E05DD081882EF27
GREEN: lsp_signature_help — 4 passed, 0 failed.

### M3 — stale version guard 제거

TARGET = tool/src/lsp/server.rs
BASE_SHA256 = 2B5FDCAEAA5C248505A975A801AC4730A645F25AC05D1921FB2399C68C66750B
적용 위치: inlay hint document version이 stale합니다 branch.

Exact mutation and restore:
- if requested_version != snapshot.version {
+ if false && requested_version != snapshot.version {
restore:
- if false && requested_version != snapshot.version {
+ if requested_version != snapshot.version {

RED: lsp33_inlay_hints_require_explicit_types_and_preserve_utf16와 lsp18_inlay_hints_reuse_param_identity_and_live_snapshot가 실패; 2 passed, 2 failed.
RESTORE_SHA256 = 2B5FDCAEAA5C248505A975A801AC4730A645F25AC05D1921FB2399C68C66750B
GREEN: lsp_signature_help — 4 passed, 0 failed.

모든 mutation은 단일 축으로 수행했고 residue는 남기지 않았다.

## Git custody

PRODUCT_COMMIT = 9345563ff70f07405035caf90ac608aad8e33d47
PRODUCT_TREE = 673d40ce8d76b59be4b8e5fda742d3a73b40fc8f
PRODUCT_PARENT = e9ef6f40d849ca922dd0516251f51692e8c35f47
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
PUSH_PERFORMED = NO
NEW_DEPENDENCY = 0
NEW_PACK_RUNNER_META_TEST = 0/0/0
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
PROCESS_RESIDUE = 0
READY_FOR_INDEPENDENT_REVIEW = YES
NEXT_AUTONOMOUS_UNIT = MANAGER_SELECTION_REQUIRED

이 문서는 product commit과 분리된 docs-only handoff로 봉인한다. 현재 LSP33 상태는 PRODUCT_FIXED_PENDING_REVIEW이며, 독립검토 대상은 9345563f product target과 이 handoff commit의 결속이다.
