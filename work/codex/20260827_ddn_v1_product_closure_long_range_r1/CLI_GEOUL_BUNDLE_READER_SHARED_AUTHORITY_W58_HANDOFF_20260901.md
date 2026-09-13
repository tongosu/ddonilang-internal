# CLI Geoul bundle reader 공유 권위 W58 인계

## 범위와 계보

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- live authority: internal SSOT v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- baseline: `ed59294fbaa9e0b26ef91638f9b148b72ef11a03`
- product fixed: `8ab4a69dd6adcc13aa7ff5f44c87e13adf054337`
- fixed tree: `4fe396d47ba6243296280e937c381523d545ebe7`
- direct parent exact, merge count 0

## 제품 변화

dataset, replay, query와 Geoul inspection이 소비하는 `audit.ddni`/`audit.idx` header, frame, payload, index decode와 audit hash 권위를 `ddonirang-tool::geoul_bundle`의 단일 shared typed reader로 이동했다. `tools/teul-cli/src/core/geoul.rs`는 기존 command와 internal 호출 경로를 보존하는 re-export adapter이며, bundle writer가 사용하는 header encoder도 같은 shared format authority를 소비한다.

기존 `DDNI` magic, version 1, header/frame field order, little-endian encoding, BLAKE3 audit identity와 diagnostics를 바꾸지 않았다. malformed index length는 shared reader에서 fail-closed한다. teul의 private `State` encoding과 bundle writer, manifest text, output directory overwrite/atomic replacement 정책은 이번 범위에 포함하지 않았다.

## 변경 경로

1. `tool/src/geoul_bundle.rs`
2. `tool/src/lib.rs`
3. `tools/teul-cli/src/core/geoul.rs`

새 pack 0, 새 runner 0, 새 framework 0, meta-test 0, public command/option/spelling 0, tracked WASM/UI/SSOT/SPEC diff 0이다.

## 검증과 mutation

- shared Geoul reader focused tests: 2/2 PASS
  - shared header/frame/payload roundtrip decode
  - malformed `audit.idx` fail-closed
- existing teul Geoul manifest tests: 2/2 PASS
- existing teul run consumer: 1/1 PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS
- malformed-index length guard를 약화한 mutation: focused test actual RED, exit 101, 0/1
- exact restore source SHA-256: `677faeca5ada67a91d9c109378a726295c21d6838a38a9cf58b1d2a140428fa7`
- restore focused GREEN: 2/2
- mutation residue: 0
- teul full regression: 1045 PASS / 기존 동일 9 FAIL; 새 drift 0
- `git diff --check`: PASS

## 제품 가치와 gate 영향

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: dataset/replay/query가 읽는 Geoul bundle transport를 private teul parser가 아니라 shared product reader authority로 검증한다.
- CHANGED_V1_GATE: teul physical retirement 전에 제거해야 하는 private parser/transport authority 한 family를 제거했다.
- DUPLICATE_AUTHORITY_ELIMINATED: audit header/frame/index reader와 audit hash의 teul-local 구현 1 family.
- NATIVE: shared tool authority가 기존 native Geoul consumers에 compile/re-export reachability를 제공한다.
- WASM/Workbench: Geoul bundle binary transport는 현재 native/internal custody이므로 이번 slice에서는 NOT_APPLICABLE이며 새 projection을 발명하지 않았다.
- REUSED_TEST_COUNT: existing focused tests 3 + existing teul full regression 1 suite
- NEW_TEST_ARTIFACT_COUNT: 0 (shared product module inline unit cases 2)
- META_TEST_CREATED: 0
- ACTIVE_REVIEW_TASK_COUNT: 0
- REVIEW_BUNDLE_TARGET: W53~W58 coherent internal/deferred CLI authority convergence; 관리가 기존 rolling reviewer를 재사용할 때만 검토한다.

## 남은 정확한 경계

`GeoulBundleWriter`는 아직 teul-private `State`/value encoding과 sequential final-path writes를 소유한다. 기존 output directory를 교체할 때의 overwrite compatibility와 directory-level atomic replacement 계약은 현재 이 slice의 승인된 의미가 아니다. 이를 바꾸려면 실제 writer RED와 함께 별도 `CONCRETE_DETAIL_GAP_DETECTED`로 다루며, 이번 fixed target은 기존 writer behavior를 그대로 보존한다.

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole CLI convergence, teul semantic authority/dependency 0 전체, public membership, physical retirement, P0~P6 closure, V1 readiness/release/activation, legal, Owner Human Smoke 또는 Human PASS를 주장하지 않는다.
