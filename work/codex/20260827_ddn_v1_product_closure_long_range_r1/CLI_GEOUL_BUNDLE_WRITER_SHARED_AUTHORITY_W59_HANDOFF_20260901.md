# CLI Geoul bundle writer 공유 권위 W59 인계

## 계보

- goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- authority: internal SSOT v25.47.0 / RD-001~543, public SPEC v0.6.0
- baseline: `5de466baeda881ec0ac2a8cc942d601e2f0a20c8`
- product fixed: `474e7c52b61081044763c4ed70f686e0cbfd3f1c`
- fixed tree: `e1686a28cf97f282f68128185429330b66c20bfd`
- direct parent exact, merge count 0

## 제품 변화

Geoul `audit.ddni`, `audit.idx`, checkpoint와 `manifest.detjson`의 byte writer를 `ddonirang-tool::geoul_bundle::GeoulBundleWriter`로 이동했다. teul은 기존 이름을 re-export하고 private `State`를 detbin으로 바꾸는 adapter만 유지한다. 기존 binary layout, manifest fields/order, BLAKE3 hash, checkpoint cadence, sequential file write와 overwrite behavior는 byte-compatible하게 보존했다.

변경 경로는 `tool/src/geoul_bundle.rs`와 `tools/teul-cli/src/core/geoul.rs` 두 개뿐이다. 새 pack/runner/framework/meta-test/public option/command 0, tracked WASM/UI/SSOT/SPEC diff 0이다.

## 검증

- shared writer→reader→payload/identity roundtrip와 manifest: 4/4 PASS
- existing teul run consumer: 1/1 PASS
- teul offline cargo check: PASS
- teul full regression: 1043 PASS / 기존 동일 9 FAIL; 이전 teul-local manifest tests 2개를 shared module로 이동했으므로 총수만 2 감소, semantic test loss 0
- index offset를 0으로 고정한 mutation: actual RED exit 101, 0/1
- exact restore source SHA-256: `3eeabec40da4d22fc1a15f2a8494828ff61a9cbb859a7c7447cf206a5886d8da`
- restore GREEN: shared 4/4, existing consumer 1/1
- mutation residue 0, `git diff --check` PASS

## gate와 비주장

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: record/replay/dataset용 Geoul bundle 생성과 소비가 같은 shared typed transport authority를 사용한다.
- DUPLICATE_AUTHORITY_ELIMINATED: teul-private bundle writer/index/manifest family 1.
- remaining private seam: teul `State`/Value detbin adapter와 SAM-key filtering.
- `CONCRETE_DETAIL_GAP_DETECTED`: 기존 output directory 교체의 atomic replacement/overwrite compatibility는 승인된 계약이 아니므로 변경하지 않았다.
- NEW_TEST_ARTIFACT_COUNT 0, META_TEST_CREATED 0, NEW_REVIEW_TASK/WORKTREE/BRANCH 0.
- REVIEW_BUNDLE_TARGET: W53~W59 coherent internal/deferred CLI authority convergence.

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole CLI convergence, teul authority/dependency 0 전체, public membership, physical retirement, V1 closure/readiness/release/activation/Human PASS를 주장하지 않는다.
