# CLI canon 실패 evidence 원자 게시 W49 인계

## 결속

- 상태: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- 권위: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0
- baseline: `71aa3538301eab2aa296a8ff2c0377e0edd16bcc`
- product fixed: `4d0c61af65e5b0a6960bff77725d0337f5b612c4`
- product tree: `8c33940eb5f15054c8a974e0257a55db6cfd3353`
- merge count: 0

## 사용자 workflow와 제품 변경

`canon` canonicalization 실패 및 `--check` mismatch 경로에서 fix-it JSON과 diagnostic JSONL을 하나의 shared multi-artifact transaction으로 게시한다. diagnostic target이 실패하면 fix-it만 단독으로 남지 않으며, 두 target이 유효할 때에는 실패 evidence 두 파일이 함께 게시된다.

변경 제품 경로는 `tools/teul-cli/src/cli/canon.rs` 하나다. 공개 command membership, executable/package 이름, diagnostic spelling, parser/runtime/value/canon semantics는 바꾸지 않았다. W47/W48의 shared writer를 재사용했고 새 artifact API를 만들지 않았다.

## RED, 구현, mutation

- 제품 RED: invalid DDN `값 <- .`와 blocked diagnostic target에서 command가 `E_CLI_WRITE`로 실패한 뒤 fix-it sidecar가 단독 게시됐다.
- GREEN: 같은 조건에서 fix-it 미게시; blocker 제거 후 invalid source는 계속 fail-closed하면서 fix-it과 diagnostic이 함께 게시된다.
- 적용 분기: strict DDN parse failure, legacy quiet diagnostic pair, DDN check mismatch, exec-policy fast-path parse/check failure, 일반 projection parse/check failure.
- risk mutation: shared transaction을 순차 `write_cli_artifact` loop로 되돌리자 focused test가 실제 RED가 되고 fix-it 단독 게시를 관찰했다.
- exact restore 후 focused GREEN 1/1, mutation residue 0.
- restored source: 50,767 bytes / SHA-256 `1f5bbeb93b2cd53a90dab2095162d482d4491736c9b125fac335542750a276ee`.

## 검증

- focused W49: 1/1 PASS
- canon module: 13 PASS + 동일 기존 2 FAIL
- full teul-cli: 1,045 PASS + 동일 기존 9 FAIL, new regression 0
- `git diff --check`: PASS
- test-created temp residue: 0
- 새 test artifact/runner/pack/meta-test: 0
- 새 colocated Rust regression test: 1

기존 9개 실패는 legacy `보임`, 역사 짜임/진단, right-assignment 계보이며 이 변경에서 새로 생기지 않았다.

## 경계

- native filesystem CLI seam: PASS
- WASM/Workbench: 이 filesystem error-sidecar 경로에 비적용, diff 0
- partial evidence publish: 0 (검증된 canon failure/check-mismatch pair)
- product diff outside `canon.rs`: 0
- tracked WASM/UI/pack/publish/SSOT/SPEC diff: 0
- 보호 untracked custody: byte-identical, unstaged

## Anti-meta

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: canon 실패 시 fix-it과 diagnostic이 all-or-nothing으로 게시됨
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: canon module 및 full teul-cli
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: 실제 partial-publish 위험 하나만 mutation하고 추가 receipt/hash checker를 만들지 않음
- NEXT_PRODUCT_DECISION_ENABLED: W47~W49 canon output/evidence atomicity를 하나의 coherent CLI convergence review bundle로 검토 가능

## Nonclaims

이 구현은 독립 PASS, 모든 non-DDN 성공 projection의 sidecar 원자성, C0~C8 closure, teul-cli public retirement, public command membership, PathIR public 계약, P0~P6 전체 closure, V1 readiness/release/activation/legal 또는 Human PASS를 주장하지 않는다.
