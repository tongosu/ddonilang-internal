# CLI Bogae Bundle Shared Atomic Authority W77 Handoff

## 실행 계약

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task
- AI_CAPABILITY: product single-writer implementation and verification
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 closure single product writer
- RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
- ORIGIN_GOAL: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- DEEP_RESEARCH_CHECK: NOT_USE — existing versioned product contract and executable golden determine this slice.

## 권위와 계보

- INTERNAL_CURRENT: v25.47.0 / RD-001~543, read-only
- PUBLIC_LANGUAGE_SPEC: v0.6.0, read-only
- BASELINE: `348fd4a2445a0f66275ef1db51d89f6dfc33f530`
- PRODUCT_FIXED: `a96f15cecf2dddda99ddcb2959242cc4f26550a3`
- PRODUCT_FIXED_TREE: `969d5c004dba3e428fba7d4e8c6507cfc93dbacc`
- DIRECT_PARENT: YES
- MERGE_COUNT: 0

## exact FILE_OWNER와 제품 diff

1. `tool/src/bogae_bundle_workflow.rs`
   - Git blob `595d7be0b4b88f573f94ed7d69c4d3cabb71e055`
   - Git bytes 5,493
   - checkout SHA-256 `699121f223b6c07f532abb21f3b910e11cbc5cca1b113de9280ffba04d083a1e`
2. `tool/src/lib.rs`
   - Git blob `28c8b402fbaed9429c6891f8d1bb8f18a5291c4d`
   - Git bytes 3,280
   - checkout SHA-256 `d9b4ba85178d811214c46a1a29365f87e32031e7e1932dafc6f48d4205f88cf9`
3. `tools/teul-cli/src/cli/bogae_bundle.rs`
   - Git blob `404e6b5a380304c49721bde7ff673a9657cdc48f`
   - Git bytes 123
   - checkout SHA-256 `ffe2df7ef9854497e844721e6435fbf377c82003746d9dd4296732a93f27bf2c`

`bogae bundle`의 private teul implementation을 host-only shared tool authority로 이동했다. teul에는 shared authority를 소비하는 3-line adapter만 남았다. private owner function 1 -> 0, shared owner 0 -> 1이다.

## 실제 사용자 workflow

- INPUT: existing mapping + asset directory
- PRODUCT PATH: `bogae bundle`
- OUTPUT: mapping, content-addressed assets, `bogae_bundle_v1` manifest
- DETERMINISTIC HASH: `blake3:2a3552afd8d97b7506ed5cf632c7c5cb5faefe079996aef362cae7e3e90759b9`
- manifest SHA-256: `fd478eff103c230eda0abbd05e7fa639d23d743099e6e2c1ddd06c112c3bf121`
- mapping SHA-256: `193de5690765b98c12db20af052cbe43df39bbe8bf890b724cfdc9a50bbc6550`
- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: the complete bundle producer is reachable from shared tool authority without a private teul implementation; existing command spelling/output remain unchanged.

## 검증과 mutation

- existing `bogae_bundle_v1` pack golden baseline: PASS
- fixed implementation pack golden: PASS
- restore and fixed-head pack golden: PASS
- `cargo build --manifest-path tools/teul-cli/Cargo.toml`: PASS
- changed-file rustfmt check: PASS
- `git diff --check`: PASS
- REUSED_TEST_COUNT: 1 existing executable pack family
- NEW_TEST_ARTIFACT_COUNT: 0
- META_TEST_CREATED: 0

Risk-relevant mutation 한 축만 수행했다.

- fault: `manifest.toml` target을 directory로 선점
- fixed behavior: exit 1 `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`; mapping publish 0; asset publish 0
- mutation: one artifact set write를 순차 per-file atomic writes로 일시 교체
- mutation RED: exit 1이지만 mapping 1, asset 1이 먼저 publish됨
- exact restore: `tool/src/bogae_bundle_workflow.rs` checkout SHA-256 `699121f223b6c07f532abb21f3b910e11cbc5cca1b113de9280ffba04d083a1e`
- restore GREEN: mapping publish 0; asset publish 0
- mutation residue: 0

## 선행 dataset 후보 분류

W77 착수 전에 existing dataset runner 3개를 재사용하려 했으나, 현재 `run` frontdoor가 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`로 실패하고 후속 Geoul 입력이 생성되지 않았다. 새 fixture/runner로 우회하지 않고 dataset slice만 `REBASE_REQUIRED_BY_RUN_FRONTDOOR`로 동결했다. dataset 제품 diff/commit은 0이다.

## 보호 경계

- product diff outside exact three paths: 0
- tests/packs/tracked WASM/visible UI diff: 0
- `docs/ssot/**` diff: 0
- `publish/spec/**` diff: 0
- public command membership/naming transition: 0
- new pack/runner/meta-test/reviewer/worktree/branch: 0
- W77 external build/repro residue: 0
- four protected task-owned untracked files: byte-identical and unstaged

## Review bundle

- STATUS: `CLI_BOGAE_BUNDLE_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`
- REVIEW_BUNDLE_TARGET: W74 certificate + W75 observation + W76 Seulgi bundle + W77 Bogae bundle.
- REVIEW_DISPATCH: READY_FOR_EXISTING_ROLLING_REVIEWER_AFTER_MANAGEMENT_BINDING.
- writer-created reviewer/worktree: 0

## Nonclaims

Public `bogae bundle` membership, executable/package naming, full teul authority/dependency zero, physical teul retirement/deletion, whole P0~P6, V1 readiness/release/activation/legal status, Owner Human Smoke 및 Human PASS는 주장하지 않는다.
