# [DDN V1제품마감Codex -> Codex관리Work] DDN-P-V1-P0-CLI02-SHARED-CANON-PREPROCESS-AUTHORITY-W1 — 구현 결과

## 고정 대상

```text
TASK: DDN-P-V1-P0-CLI02-SHARED-CANON-PREPROCESS-AUTHORITY-W1
ACTUAL_EXECUTION_THREAD_ID: 01a04a01-b812-7840-a2a3-33208dd36e36
IMPLEMENTATION_BASELINE: 4367dd0cf186e3f8c9176eb5c3eeeefe6b3b1010
IMPLEMENTATION_COMMIT: 84b307c5c84d43263ee342daa5610453c832fcf7
PRODUCT_TEST_FIXED_HEAD: 84b307c5c84d43263ee342daa5610453c832fcf7
PRODUCT_TEST_FIXED_TREE: 34ebbd5b57659db2bc19678e5ed81634b483e987
LINEAR_ANCESTRY: YES
MERGE_COMMIT_COUNT: 0
FINAL_STATUS: P0_CLI02_SHARED_CANON_PREPROCESS_AUTHORITY_IMPLEMENTED_UNDER_REVIEW
```

## 권위·소유권 결속

- internal SSOT CURRENT: v25.19.0 / RD-001~461
- public Language SPEC CURRENT: v0.6.0
- Owner binding: D1=A, D2=A+, D3=A, D4=A, D5=A, D6=A
- FILE_OWNER: 이 세션이 P0 허용 제품 경로의 유일한 writer였다.
- exact worktree: `I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828`
- shared dirty root, 기존 long-range worktree, `docs/ssot/**`, public SPEC는 읽기 전용으로 보존했다.

## 구현

1. `tools/teul-cli/src/canon.rs`의 canon 구현을 byte-identical하게 `tool/src/canon.rs`로 옮겼다.
2. `tools/teul-cli/src/canon.rs`는 `ddonirang_tool::canon`의 얇은 adapter만 남겼다.
3. teul CLI preprocess 호출을 `ddonirang_tool::preprocess` crate API로 결속하여 reverse source import를 제거했다.
4. file metadata JSON 변환을 tool crate API로 노출하여 CLI canon consumer가 공통 제품 권위를 사용하게 했다.
5. canon/preprocess owner 수와 reverse import/private fallback을 검사하는 source authority checker를 추가했다.
6. 공식 WASM 도구를 같은 tool crate에서 다시 빌드하고 tracked UI WASM과 deterministic manifest를 갱신했다. 시각·문구·레이아웃은 바꾸지 않았다.

이동 전 teul canon blob과 이동 후 tool canon blob은 모두
`ef2f8aef2a44f8370f1e549610d1ad0347f90fd0`으로 동일하다.

## 구조 검증

```text
REVERSE_SOURCE_IMPORTS_BEFORE: 1
REVERSE_SOURCE_IMPORTS_AFTER: 0
AUTHORITATIVE_CANON_OWNER_COUNT: 1
AUTHORITATIVE_PREPROCESS_OWNER_COUNT: 1
PRIVATE_FALLBACK_COUNT: 0
AUTHORITY_CHECK: GREEN
```

## 집중 회귀

```text
cargo check -p ddonirang-tool: PASS
cargo check -p teul-cli: PASS
tool canon suite: 46/46 PASS
tool preprocess suite: 57/57 PASS
teul CLI focused canon suite: 8 PASS, baseline-identical 2 FAIL
WASM exact parity: 9/9 PASS
tracked WASM freshness: PASS
git diff --check: PASS
```

teul CLI의 다음 두 실패는 기준선에서도 동일했고 P0 신규 실패가 아니다.

- `canon_accepts_boim_surface_for_ddn_emit`
- `run_ddn_keeps_legacy_jjaim_port_diagnostics_quiet_success`

Foundation-12 전체 raw CLI/WASM parity는 제거된 legacy `보임 {}` 입력을 포함해 아직 FAIL이다.
이 결과를 P0 parity PASS로 승격하지 않으며 후속 supported-ingress/evidence rebase 대상으로 보존한다.

## mutation RED -> restore -> GREEN

teul CLI preprocess를 reverse source path import로 되돌리는 mutation을 임시 적용했을 때 authority
checker가 2개 위반으로 RED가 됐다. 원래 crate API alias를 byte-exact 복원한 뒤 GREEN, reverse
import 0, private fallback 0을 재확인했다. mutation residue는 0이다.

## clean-detached 재현

등록 worktree를 새로 만들지 않고 기존 worktree에서 fixed HEAD를 detached checkout하여 다음을
재현한 뒤 successor branch로 돌아왔다.

```text
tool/teul cargo check: PASS
authority checker: PASS
canon: 46/46 PASS
preprocess: 57/57 PASS
WASM exact parity: 9/9 PASS
WASM freshness: PASS
WORKTREE_REUSED: YES
NEW_WORKTREE_CREATED: NO
```

## evidence 영향

- UNAFFECTED: RD-178, RD-201, RD-202, RD-203 scoped behavior; CLI01 census/review
- REBASE_REQUIRED: FD01A, FD01B, Editable I1, R3K/R3N public projection, private teul runtime golden
- ADDITIVE: P0 source-authority checker와 fixed-head clean-detached evidence
- INVALIDATED: 없음. 기존 PASS를 P0 fixed HEAD에 자동 상속하지 않는다.

## 보호 경계와 비주장

```text
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
UI_VISUAL_DIFF: 0
OFFICIAL_WRITE_COUNT: 0
ACTIVATION_CALL_COUNT: 0
PUBLIC_PUSH_COUNT: 0
INDEPENDENT_PASS: NOT_CLAIMED
P0_CLOSED: NOT_CLAIMED
OFFICIAL_EXECUTABLE_OR_COMMAND_MEMBERSHIP: NOT_DECIDED_HERE
V1_MEMBERSHIP_OR_READINESS: NOT_PROMOTED
RELEASE_OR_HUMAN_PASS: NOT_CLAIMED
```
