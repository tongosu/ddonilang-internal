# CLI InputTape 공유 권위 W56 인계

## 범위와 계보

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- live authority: internal SSOT v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- baseline: `388a560f38b6b0e85aa2976c81e48bf8ebeb3d62`
- product fixed: `a0c235d7d26aba31b551a3cd80207f5821125f38`
- fixed tree: `65b91760d32c12463d8ea4298e729accc13e56a7`
- direct parent exact, merge count 0

## 제품 변화

record/replay, live input, replay-branch가 공유하는 `DDN_INPUT_TAPE_V1` binary encoding, key registry, mask validation과 decoding을 `ddonirang-tool::input_tape`의 단일 typed authority로 이동했다. `tools/teul-cli/src/cli/input_tape.rs`에는 public/internal command dispatch를 보존하는 re-export adapter 한 줄만 남는다.

writer는 publish 전에 모든 record mask를 검증하고 existing shared binary atomic replacement를 사용한다. 잘못된 record는 bytes를 생성하거나 artifact를 게시하기 전에 fail-closed한다. 기존 magic, version, registry id, registry keys, alias, binary order와 consumer 호출은 바꾸지 않았다.

## 변경 경로

1. `tool/src/input_tape.rs`
2. `tool/src/lib.rs`
3. `tools/teul-cli/src/cli/input_tape.rs`

새 pack 0, 새 runner 0, 새 framework 0, meta-test 0, public command/option/spelling 0, tracked WASM/UI/SSOT/SPEC diff 0이다.

## 검증과 mutation

- shared InputTape focused tests: 3/3 PASS
  - 동일 typed tape의 byte-deterministic encode와 decode roundtrip
  - registry-hash mutation fail-closed
  - invalid mask record pre-publication rejection
- existing teul run consumer test: 1/1 PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS
- registry hash comparison bypass mutation: focused test actual RED, 0/1
- exact restore source SHA-256: `c9b12d32d17060eb3f8a51e164081c6c2feed49cd61c0e15a259a273636c6fec`
- restore focused GREEN: 3/3
- mutation residue: 0
- `git diff --check`: PASS

## 제품 가치와 gate 영향

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: input record/replay의 binary identity가 private teul implementation이 아니라 shared product authority를 사용하며 invalid in-memory record를 게시하지 않는다.
- RELEASE_BLOCKER_CHANGED: `teul-cli` physical retirement 전에 제거해야 하는 private format/value authority 한 family를 0으로 낮췄다.
- NATIVE: shared tool authority reachable
- WASM/Workbench: current record/replay binary transport는 native/internal custody이며 이번 slice에서 새 projection을 만들지 않아 NOT_APPLICABLE
- REUSED_TEST_COUNT: existing teul consumer 1 + existing Cargo compile paths
- NEW_TEST_ARTIFACT_COUNT: 0 (inline product unit cases 3)
- META_TEST_CREATED: 0
- ACTIVE_REVIEW_TASK_COUNT: 0
- REVIEW_BUNDLE_TARGET: W53~W56 coherent internal/deferred CLI authority convergence; management-assigned existing rolling reviewer only

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole CLI convergence, teul semantic authority/dependency 0 전체, public membership, physical retirement, P0~P6 closure, V1 readiness/release/activation, legal, Owner Human Smoke 또는 Human PASS를 주장하지 않는다.
