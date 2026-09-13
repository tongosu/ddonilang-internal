# CLI canon structured artifact set 원자 게시 W50 인계

## 결속

- 상태: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- 권위: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0
- baseline: `cfcd93484d114e379ff275058a7a8d4d857be419`
- product fixed: `715394cae280b3207a0415712145d08ffb22d473`
- product tree: `17c927882f12e9cbf021b2206c2c62d7377dca07`
- merge count: 0

## 사용자 workflow와 제품 변경

Guseong flatten, Alrim plan, execution-policy map, Maegim control 네 structured canon projection의 output, fix-it JSON, diagnostic JSONL, metadata JSON을 하나의 shared multi-artifact transaction으로 게시한다. 최종 projection output이 실패해도 앞선 sidecar가 남지 않는다. output path가 없을 때에는 sidecar transaction 성공 뒤 기존 stdout projection을 유지한다.

변경 제품 경로는 `tools/teul-cli/src/cli/canon.rs` 하나다. projection schema/content, parser/runtime/canon semantics, 공개 명칭과 command membership은 변경하지 않았다. `Both`와 `FixitsJson`의 기존 동작은 이번 범위에서 바꾸지 않았다.

## RED, 구현, mutation

- 제품 RED: valid Guseong source와 directory로 점유된 최종 output target에서 `E_CLI_WRITE` 뒤 fix-it/diagnostic/metadata가 부분 게시됐다.
- GREEN: 같은 조건에서 세 sidecar 모두 미게시; blocker 제거 후 projection과 세 sidecar가 함께 게시된다.
- 동일 helper 소비 projection: GuseongFlatJson, AlrimPlanJson, ExecPolicyMapJson(빈 fast path 포함), MaegimControlJson.
- risk mutation: shared transaction을 순차 artifact writer로 되돌리자 focused test가 실제 RED가 되고 fix-it 단독 게시를 관찰했다.
- exact restore 후 focused GREEN 1/1, mutation residue 0.
- restored source: 54,763 bytes / SHA-256 `64ce0d3b808ee95bb9944611e52b2011182f67141702c1666841891f3c9a3f7d`.

## 검증

- focused W50: 1/1 PASS
- canon module: 14 PASS + 동일 기존 2 FAIL
- full teul-cli: 1,046 PASS + 동일 기존 9 FAIL, new regression 0
- `git diff --check`: PASS
- test-created temp residue: 0
- 새 test artifact/runner/pack/meta-test: 0
- 새 colocated Rust regression test: 1

## 경계

- native filesystem CLI seam: PASS
- WASM/Workbench: filesystem structured projection output 경로에 비적용, diff 0
- verified partial artifact publish: 0
- product diff outside `canon.rs`: 0
- tracked WASM/UI/pack/publish/SSOT/SPEC diff: 0
- 보호 untracked custody: byte-identical, unstaged

## Anti-meta

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: 네 structured projection의 output과 성공 sidecar가 all-or-nothing으로 게시됨
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: canon module 및 full teul-cli
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: 실제 projection publish 결함 하나만 위험 mutation으로 검증
- NEXT_PRODUCT_DECISION_ENABLED: W47~W50 canon artifact transaction을 한 coherent CLI convergence milestone로 검토 가능

## Nonclaims

이 구현은 독립 PASS, `Both`의 optional sidecar 전체 원자성, C0~C8 closure, teul-cli public retirement, public command membership, PathIR public 계약, P0~P6 전체 closure, V1 readiness/release/activation/legal 또는 Human PASS를 주장하지 않는다.
