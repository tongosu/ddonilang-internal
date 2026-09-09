# Release integration checkpoint audit

## conclusion

현재 clean commit 하나가 모든 최신 승인 프로그램을 포함하지 않는다. 자동 merge나 newest-date 선택은 release baseline을 만들지 못한다.

## key lineages

- T5G canonical view closure: `905efb4a...`, clean
- W1C2 I2 limited closure: `40cd0473...`, clean
- R10 RuntimeBridge T1 unblock: `50ddc7be...`, clean
- public projection R1: `c3c65ae2...`, clean
- math physical worktrees: branch refs `a000e262...`, tracked dirty 2 each, staged 0
- shared root: tracked dirty 201, staged 0

## ancestry and overlap

T5G와 W1C2 closure는 서로 ancestor가 아니며 merge-base는 `5ff2a804...`다.

- T5G changed paths from merge-base: 292
- W1C2 changed paths from merge-base: 2,021
- overlapping paths: 94
- overlap families: lang parser/canonicalizer/AST, tool runtime/WASM/preprocess, teul-cli, Workbench runtime/view files, tracked WASM, tests, public SPEC/status files

따라서 단순 cherry-pick/ours/theirs 선택은 금지하고 semantic convergence와 fixed-head regression이 필요하다.

T5G와 R10은 merge-base `15f983fe...`에서 갈라졌으며 직접 path overlap은 0이지만 ancestry가 분리돼 있어 integration receipt는 필요하다.

## public SPEC custody

- R1 sealed source의 public current: v0.3.0
- shared root working file의 public current: v0.5.0
- shared root에서 `publish/spec/CURRENT.md`: tracked modified

v0.5.0의 문서 authority를 부정하지 않는다. 다만 PUBLIC_SOURCE projection에는 승인 bytes가 clean sealed integration commit에 들어가야 한다.

## baseline decision

```text
RELEASE_BASELINE_OPTION_A_NEW_INTEGRATION_COMMIT: OWNER_APPROVED_DIRECTION
EXACT_INTEGRATION_COMMIT: OPEN
AUTOMATIC_MERGE: NOT_AUTHORIZED
DIRTY_ROOT_SNAPSHOT: PROHIBITED
PRODUCT_BASELINE_SAFE: YES_FOR_CONTINUED_ISOLATED_PROGRAM_WORK
REPOSITORY_OPERATIONS_SAFE: YES_FOR_ADDITIVE_AUDIT_AND_INTEGRATION_PREP
```

각 active program owner가 fixed HEAD, review/closure, dirty checkpoint disposition을 반환한 뒤 integration order를 정한다.
