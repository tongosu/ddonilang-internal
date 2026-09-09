# CLI Seulgi Bundle Shared Atomic Authority W76 Handoff

## 역할과 범위

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task
- AI_CAPABILITY: product single-writer implementation and verification
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 closure single product writer
- RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
- ORIGIN_GOAL: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- SLICE: W76 `seulgi bundle parity` shared authority and atomic output set
- DEEP_RESEARCH_CHECK: NOT_USE — fixed repository product paths and executable evidence determine this slice.

## 권위와 계보

- INTERNAL_CURRENT: v25.47.0 / RD-001~543, read-only
- PUBLIC_LANGUAGE_SPEC: v0.6.0, read-only
- BASELINE: `3c273e8f5dab980e1e1d6ce963c70a58791fffd8`
- PRODUCT_FIXED: `9830df6ff707fd8cf057c0b32a0cc6ef24ae1987`
- PRODUCT_FIXED_TREE: `a1937038d6a9998f12ad94fba3f4ac34f35a3a96`
- DIRECT_PARENT: YES
- MERGE_COUNT: 0

## 제품 변경

정확히 다음 세 경로만 변경했다.

1. `tool/src/seulgi_bundle_workflow.rs`
   - Git blob: `7e0e64a27482c4a54a8e88e19e98c2c2b12292cb`
   - Git bytes: 16,109
   - checkout SHA-256: `9a5d4334359578698fe8313d5b4d89280415f5bd1e78ae58b3e576d16454b2d9`
2. `tool/src/lib.rs`
   - Git blob: `412c73c7acc47e4d659d409e2e5e2cc934cbf183`
   - Git bytes: 3,213
   - checkout SHA-256: `4958ee87a63f03f92bd314eb57e382536a0579e4af5bfc6fd853e683ab3ad091`
3. `tools/teul-cli/src/cli/seulgi_bundle.rs`
   - Git blob: `d0d669d0a8fdfe5e916d07e6aa2991d4cb73875a`
   - Git bytes: 132
   - checkout SHA-256: `4337a0541f12758c7039c2eb581ef25db024ff8a44d719ee9e671e8ac17ef4b0`

`seulgi bundle parity`의 제품 구현을 host-only shared `ddonirang-tool` 모듈로 이동했다. `teul-cli`에는 shared authority를 소비하는 3-line adapter만 남았다. 이 명령의 private owner function은 1에서 0, shared owner는 0에서 1이 되었다.

두 산출물 `outputs.detjson`과 `outputs_hash.txt`는 하나의 `write_text_artifacts_atomic` 호출로 publish한다. 두 번째 target이 파일이 아니면 첫 번째 산출물도 남지 않는다.

## 사용자 workflow와 RED -> GREEN

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: deterministic Seulgi bundle parity 실행이 shared tool authority를 사용하며 두 산출물을 all-or-nothing으로 공개한다.
- BASELINE SUCCESS: exit 0.
  - `outputs.detjson` SHA-256: `ebc355d8c236200fa67885d515945d3741d23953d2069be4d603258d6cce443d`
  - `outputs_hash.txt` SHA-256: `1f428be6abe09929354270f1b7d71f0ba11b964cef4b09332ae47027788b64b0`
- BASELINE FAULT RED: `outputs_hash.txt`를 디렉터리로 선점하면 exit 1이지만 `outputs.detjson`이 남았다.
- FIXED FAULT GREEN: 동일 fault가 `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, exit 1이며 `outputs.detjson` publish 0이다.
- FIXED SUCCESS: exit 0, 위 두 SHA-256과 exact match.

## 검증

- `cargo build --manifest-path tools/teul-cli/Cargo.toml`: PASS
- `python tests/run_seulgi_bundle_provenance_check.py`: PASS
  - existing `gogae8_w88_bundle_hash_parity` golden 실행 포함
  - actual `bundle parity` product command 실행 포함
- clean fixed-head direct success: PASS
- clean fixed-head blocked-second-target failure: PASS, partial publish 0
- `rustfmt --check --config skip_children=true` on changed Rust files: PASS
- `git diff --check`: PASS
- REUSED_TEST_COUNT: 2 existing product runner/pack families
- NEW_TEST_ARTIFACT_COUNT: 0
- META_TEST_CREATED: 0

## 위험 관련 mutation

한 가지 실제 partial-publish 위험만 mutation했다.

- mutation: atomic set을 두 개의 순차 단일-file atomic write로 일시 교체
- RED: 두 번째 target fault에서 첫 번째 output이 남음
- exact restore source bytes: 16,578 checkout bytes, SHA-256 `9a5d4334359578698fe8313d5b4d89280415f5bd1e78ae58b3e576d16454b2d9`
- restore GREEN: 동일 fault에서 partial output 0
- mutation residue: 0

## 보호 경계와 상태

- product source diff outside exact three paths: 0
- test/pack diff: 0
- tracked WASM diff: 0
- visible UI diff: 0
- `docs/ssot/**` diff: 0
- `publish/spec/**` diff: 0
- public command membership transition: 0
- executable/package naming decision: 0
- new pack/runner/reviewer/worktree/branch: 0
- W76 external build/repro residue: 0 after exact cleanup
- four pre-existing task-owned untracked custody files: preserved byte-identically and unstaged

## 상태와 다음 결속

- STATUS: `CLI_SEULGI_BUNDLE_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`
- CHANGED_V1_GATE: private teul semantic owner for this approved internal workflow 1 -> 0; failure partial publish 1 -> 0.
- REVIEW_BUNDLE_TARGET: W74 certificate + W75 observation + W76 Seulgi bundle coherent CLI authority convergence milestone.
- REVIEW_DISPATCH: management-owned existing rolling reviewer only; writer created no review task.

## Nonclaims

이 handoff는 public command membership, executable/package naming, full teul dependency zero, physical `tools/teul-cli` retirement/deletion, P0~P6 closure, V1 membership/readiness/release/activation/legal status, Owner Human Smoke 또는 Human PASS를 승인하거나 주장하지 않는다.
