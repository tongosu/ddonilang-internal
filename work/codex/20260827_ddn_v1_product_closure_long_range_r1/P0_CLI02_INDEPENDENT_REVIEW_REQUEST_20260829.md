# [DDN V1제품마감Codex -> Codex관리Work] DDN-R-V1-P0-CLI02-I1 독립검토 요청

## 고정 대상

```text
TASK: DDN-R-V1-P0-CLI02-I1
PRODUCT_TEST_FIXED_HEAD: 84b307c5c84d43263ee342daa5610453c832fcf7
PRODUCT_TEST_FIXED_TREE: 34ebbd5b57659db2bc19678e5ed81634b483e987
IMPLEMENTATION_BASELINE: 4367dd0cf186e3f8c9176eb5c3eeeefe6b3b1010
REQUIRED_REVIEW_PARENT: THIS_DOCUMENT_CONTAINING_HANDOFF_COMMIT
EXPECTED_LINEAR_ANCESTRY: YES
EXPECTED_MERGE_COMMIT_COUNT: 0
```

review 문서 commit과 product execution target은 다르다. Reviewer는 이 요청서를 담은 handoff
commit을 parent로 검토 기록을 만들되, 제품 검증은 반드시 `PRODUCT_TEST_FIXED_HEAD`의 clean
checkout에서 수행한다.

## 필수 독립 검토

1. current Owner 입력 4개 SHA-256과 D1~D6 결속, exact worktree/baseline/file-owner 계보를 대조한다.
2. baseline의 teul canon blob과 fixed HEAD의 tool canon blob이
   `ef2f8aef2a44f8370f1e549610d1ad0347f90fd0`으로 같은지 독립 계산한다.
3. canon owner 1, preprocess owner 1, reverse source import 0, private fallback 0을 source에서 다시 센다.
4. reverse import, duplicate owner, hidden private fallback을 각각 변조해 checker RED를 관찰하고 exact restore 뒤 GREEN과 residue 0을 확인한다.
5. tool canon 46/46, preprocess 57/57, WASM exact parity 9/9, tracked WASM freshness를 clean fixed target에서 재현한다.
6. teul CLI focused suite의 8 PASS와 두 baseline-identical FAIL을 기준선/고정 HEAD 양쪽에서 대조해 신규 drift 0인지 판정한다.
7. native CLI와 WASM이 같은 tool authority를 소비하는지 확인하고, 전체 Foundation-12 FAIL을 PASS로 오인하지 않는다.
8. changed-file 9개와 WASM manifest/binary custody를 대조하고 SSOT, public SPEC, UI visual, executable name, command membership에 범위 밖 변경이 없는지 확인한다.
9. RD-178/201/202/203 및 CLI01은 UNAFFECTED, FD01A/B·Editable I1·R3K/R3N·private teul evidence는 REBASE_REQUIRED라는 영향 분류를 검토한다.

## 반환 형식

```text
VERDICT: PASS | PASS_WITH_FOLLOW_UP | REWORK
SCOPE:
PRODUCT_TEST_FIXED_HEAD:
REVIEW_PARENT:
REVIEW_COMMIT:
REPORT_PATH:
REPORT_SHA256:
CANON_OWNER_COUNT:
PREPROCESS_OWNER_COUNT:
REVERSE_SOURCE_IMPORT_COUNT:
PRIVATE_FALLBACK_COUNT:
FOCUSED_REGRESSION:
MUTATION_RED_RESTORE_GREEN:
CLI_WASM_PARITY:
WASM_CUSTODY:
PRODUCT_DIFF:
SSOT_DIFF:
PUBLIC_SPEC_DIFF:
UI_VISUAL_DIFF:
FOLLOW_UPS:
```

이 요청은 independent PASS, P0 closure, official executable/command membership, teul-cli retirement,
91 command migration, V1 membership/readiness, release, activation 또는 Human PASS를 미리 승인하지 않는다.
