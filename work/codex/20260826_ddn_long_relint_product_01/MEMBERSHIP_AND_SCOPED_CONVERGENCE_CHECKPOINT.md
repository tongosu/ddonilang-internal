# DDN-LONG-RELINT-PRODUCT-01 membership and scoped convergence checkpoint

## 결론

`905efb4a...`와 `fab6315c...`는 clean commit이지만 그대로 제품 통합 baseline으로
사용할 수 없다. 두 commit 모두 별도 PC-02 프로그램의
`IMPLEMENTED_PENDING_INDEPENDENT_REVIEW` 제품 commit `04566a24...`을 ancestor로
포함한다.

또한 T5 canonical View와 W1-C1~I2의 검토된 결과는 각각 review fixed point 이전의
제품 baseline에 의존한다. 따라서 closure HEAD 전체를 그대로 택하거나 마지막
implementation commit만 떼어 적용하는 두 방식 모두 feature membership을 정확히
증명하지 못한다.

```text
G8_PRODUCT_INTEGRATION_NOT_STARTED
ADMINISTRATIVE_HEAD_AS_PRODUCT_BASELINE: INELIGIBLE
OWNER_DECISION_REQUIRED
```

## T5/R2 lineage contamination

```text
a000e262...
→ T1/T2/T4 prerequisite product commits
→ T5B~T5F
→ cf97f134... PC-01 implementation
→ 3ac1cefb... PC-01 fixed target
→ 9cb28ee8... PC-01 handoff
→ 04566a24... PC-02 implementation pending independent review
→ T5G/T5H/T5I
→ 905efb4a... canonical View closure
→ c3c65ae2... public R1
→ fab6315c... public R2
```

- PC-02 commit changed 28 paths.
- `04566a24...` 이후 `fab6315c...`까지 those 28 paths의 추가 변경은 0이다.
- 따라서 PC-02 inverse는 blob 수준에서 분리 가능하지만 실제 inverse commit 생성은
  release membership 결정이므로 수행하지 않았다.
- PC-01은 Owner-attested `CLOSED / INDEPENDENT_PASS`이나 별도 local review artifact는
  공급되지 않았다.
- R10/T1/T2/T4 계열 9개 prerequisite product commit은 T5 closure의 ancestor지만
  standalone plain-PASS closure artifact를 찾지 못했다. T5의 검토된 실제 baseline
  의존성으로 받아들일지는 Owner 결정이다.

## W1 reviewed scope

```text
W1_SCOPE_BASE: 2ec750aa576fdbd1ebd0bd400d95775e597e9983
W1_SCOPE_HEAD: 40cd0473061abe806b4b09ba51ccd7bfbbc82431
W1_SCOPE_CHANGED_PATHS: 82
```

`2ec750aa...` 자체는 independently closed W1-A/W1-B와 그 이전 제품 baseline을
포함한다. 후속 delta만 재생하면 `lang/src/delivery.rs`, W1-C1 oracle과 runner 등
검토 대상의 선행 제품·증거가 빠진다. 이 prerequisite baseline도 integration
membership에 명시되어야 한다.

## no-write three-way preview

PC-02 patch를 개념적으로 제거한 T5/R2 tree와 W1 reviewed slice를 Git blob으로만
3-way 비교했다. worktree나 index, 제품 파일은 쓰지 않았다.

```text
CHANGED_IN_BOTH_SCOPED_PATHS: 15
AUTHORITY_DOCUMENT_OVERLAP: 4
TEST_EVIDENCE_OVERLAP: 2
SEMANTIC_OVERLAP: 7
GENERATED_ARTIFACT_OVERLAP: 2

ADD_DELETE_OR_ABSENT_REQUIRES_EXACT_PATH_REVIEW: 7
TEXT_CONFLICT_REQUIRES_SEMANTIC_COMPOSITION: 7
GENERATED_BINARY_MUST_REBUILD_NOT_MERGE: 1
```

텍스트 의미 합성이 필요한 제품 경로는 다음 6개다. manifest는 생성물로 분리한다.

- `lang/src/lib.rs` — conflict hunk 1
- `tool/src/ddn_runtime.rs` — conflict hunk 23
- `tool/src/runtime_surface.rs` — conflict hunk 1
- `tools/teul-cli/src/cli/run.rs` — conflict hunk 3
- `tools/teul-cli/src/runtime/error.rs` — conflict hunk 2
- `tools/teul-cli/src/runtime/eval.rs` — conflict hunk 6

`lang/src/delivery.rs`는 effective T5/R2 tree에 없는 W1 prerequisite 제품 파일이다.
tracked WASM과 manifest는 어느 쪽 blob도 선택하지 않고 combined source에서 공식
A/B build 후 새 단일 family로 결속해야 한다.

## evidence

```text
LEDGER: SCOPED_MEMBERSHIP_MERGE_AUDIT.detjson
LEDGER_SHA256: 827612b0180811eea4d3d88464e4ae496d9dea2f7e35c8a1429ed42fcb23655e
PRODUCT_WRITE: 0
INDEX_WRITE: 0
WORKTREE_INTEGRATION_WRITE: 0
```
