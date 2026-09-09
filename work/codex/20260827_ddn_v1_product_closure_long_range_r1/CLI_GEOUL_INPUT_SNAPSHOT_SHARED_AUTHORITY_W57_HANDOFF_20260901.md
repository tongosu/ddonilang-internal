# CLI Geoul InputSnapshot 공유 권위 W57 인계

## 범위와 계보

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- live authority: internal SSOT v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- baseline: `2299b0d0f1c9baf7ce35cfb3ce8997418ca219f6`
- product fixed: `7fcea34759fde918ad6113630f8e282881a22f13`
- fixed tree: `998ae7f7139d572746611e8d559e86f99d660131`
- direct parent exact, merge count 0

## 제품 변화

run, replay, replay-branch, dataset, Geoul inspection과 snapshot application이 공유하는 `InputSnapshotV1`/`NetEventV1`의 binary encode/decode 및 input-source extension validation을 `ddonirang-tool::geoul_snapshot`의 단일 typed authority로 이동했다. `tools/teul-cli/src/core/geoul.rs`는 기존 호출 경로와 public/internal command dispatch를 깨지 않도록 shared types/functions를 re-export하는 consumer가 되었다.

기존 `DDN_SAM_V1` magic, legacy snapshot decode, `ISRC` extension version, field order, `InputSource` code와 diagnostics를 바꾸지 않았다. source-extension event count가 payload event count와 다르면 shared decoder가 fail-closed하며 partial snapshot/result publication은 0이다. Geoul bundle/state encoding과 private teul State/Value는 이번 범위에 포함하지 않았다.

## 변경 경로

1. `tool/src/geoul_snapshot.rs`
2. `tool/src/lib.rs`
3. `tools/teul-cli/src/core/geoul.rs`

새 pack 0, 새 runner 0, 새 framework 0, meta-test 0, public command/option/spelling 0, tracked WASM/UI/SSOT/SPEC diff 0이다.

## 검증과 mutation

- shared InputSnapshot focused tests: 3/3 PASS
  - source extension roundtrip
  - legacy snapshot의 existing `InputSource::Person` default 호환
  - source-extension event count mismatch fail-closed
- existing teul Geoul manifest tests: 2/2 PASS
- existing teul run consumer: 1/1 PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS
- source-count equality guard를 약화한 mutation: focused test actual RED, exit 101, 0/1
- exact restore source SHA-256: `d7175ad7dd2c7bd47487ea369d051c289d7c19120d205df9884921b607141463`
- restore focused GREEN: 3/3
- mutation residue: 0
- tool lib regression: 569 PASS / 3 FAIL. 두 실패는 isolated worktree의 `docs/ssot` 부재인 기존 ai-prompt 환경 경계이고, 한 실패는 이번 3-path diff와 겹치지 않는 existing PathIR raw-DDN definedness gap이다. 이번 slice test failure 0.
- teul full regression: 1045 PASS / 기존 동일 9 FAIL; 새 drift 0
- `git diff --check`: PASS

## 제품 가치와 gate 영향

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: record/replay/branch/dataset가 읽고 쓰는 snapshot과 source provenance가 private teul codec이 아니라 shared product authority를 사용한다.
- CHANGED_V1_GATE: teul physical retirement 전에 제거해야 하는 private value/transport authority 한 family를 0으로 낮췄다.
- NATIVE: shared tool authority가 모든 기존 native consumers에 compile/re-export reachability를 제공한다.
- WASM/Workbench: Geoul binary snapshot은 현재 native/internal transport이므로 이번 slice에서는 NOT_APPLICABLE이며 새 projection을 발명하지 않았다.
- REUSED_TEST_COUNT: existing teul tests 3 + existing full regression suites 2
- NEW_TEST_ARTIFACT_COUNT: 0 (shared product module의 inline unit cases 3)
- META_TEST_CREATED: 0
- ACTIVE_REVIEW_TASK_COUNT: 0
- REVIEW_BUNDLE_TARGET: W53~W57 coherent internal/deferred CLI authority convergence; 관리가 기존 rolling reviewer를 재사용할 때만 검토한다.

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole CLI convergence, teul semantic authority/dependency 0 전체, public membership, physical retirement, P0~P6 closure, V1 readiness/release/activation, legal, Owner Human Smoke 또는 Human PASS를 주장하지 않는다.
