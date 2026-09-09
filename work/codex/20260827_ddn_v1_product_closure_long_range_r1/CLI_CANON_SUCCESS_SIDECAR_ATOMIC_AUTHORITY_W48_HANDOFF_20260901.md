# CLI canon 성공 sidecar 원자 게시 W48 인계

## 결속

- 상태: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- 권위: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0
- baseline: `bfa196828299de325ca4ac8720acdececc2bbc34`
- product fixed: `f15f8d59bd75a1ae3a6985db410cee097aa30ff6`
- product tree: `0911282120737ad9036adc4c5aafae4c57fa82e1`
- merge count: 0

## 사용자 workflow와 제품 변경

`canon --emit ddn` 성공 경로에서 canonical DDN output, fix-it JSON, diagnostic JSONL, metadata JSON을 하나의 shared multi-artifact transaction으로 게시한다. 마지막 sidecar가 실패해도 앞선 output이나 sidecar가 남지 않는다. `--out`이 없는 기존 stdout 동작은 유지한다.

변경 제품 경로는 `tools/teul-cli/src/cli/canon.rs` 하나다. 새 parser, runtime, value, canon authority, hidden fallback, 공개 명칭 또는 command membership을 추가하지 않았다. 오류 결과 sidecar의 별도 원자화는 이 slice 범위가 아니다.

## RED, 구현, mutation

- 제품 RED: metadata target을 directory로 점유하면 기존 순차 게시가 fix-it/diagnostic을 남겼다.
- GREEN: 같은 조건에서 canonical output/fix-it/diagnostic 모두 미게시이며, blocker 제거 후 네 artifact가 함께 게시된다.
- risk mutation: shared transaction 호출을 순차 `write_cli_artifact` loop로 되돌리자 focused test가 실제 RED가 되고 fix-it residue를 관찰했다.
- exact restore 후 focused GREEN 1/1, mutation residue 0.
- restored source: 47,687 bytes / SHA-256 `2b3c05352b485eb31bcf031c03273e67040e7f817aac53d024654bccc8d99c3c`.

## 검증

- focused W48 test: 1/1 PASS
- canon module: 12 PASS + 동일 기존 2 FAIL
- full teul-cli: 1,044 PASS + 동일 기존 9 FAIL, new regression 0
- W47 shared artifact transaction tests: 기존 5/5 PASS 증거 재사용
- `git diff --check`: PASS
- 새 test artifact/runner/pack/meta-test: 0
- 새 colocated Rust regression test: 1

기존 실패는 legacy `보임` 및 역사 짜임/진단 계약을 포함하며 이 변경에서 새로 생기지 않았다.

## 경계

- native filesystem CLI seam: PASS
- WASM/Workbench: 이 filesystem output 경로에 비적용, diff 0
- product diff outside `canon.rs`: 0
- tracked WASM/UI/pack/publish/SSOT/SPEC diff: 0
- partial artifact publish: 0 (검증된 성공 DDN artifact set)
- 보호 untracked custody: byte-identical, unstaged

## Anti-meta

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: canonical source와 성공 sidecar가 all-or-nothing으로 게시됨
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: canon module, full teul-cli, W47 transaction suite
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: 제품 fail-open/partial-publish 위험 하나만 검증하고 추가 receipt/hash tamper 계층을 만들지 않음
- NEXT_PRODUCT_DECISION_ENABLED: canon 성공 artifact set을 coherent CLI convergence review bundle에 포함 가능

## Nonclaims

이 구현은 독립 PASS, 전체 canon/error-path closure, C0~C8 closure, teul-cli public retirement, public command membership, P0~P6 전체 closure, V1 readiness/release/activation/legal 또는 Human PASS를 주장하지 않는다.
