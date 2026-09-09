# R2 targeted independent review request

## review target

- D1~D8 binding이 Owner 원문과 정확히 일치하는가
- read-only GitHub audit의 public/private/default branch/live SHA/tree counts 재현
- remote state를 변경한 호출이 0인가
- R1 public SPEC evidence correction이 정확한가
- R2 scope checker가 hard-coded current 대신 actual entrypoint/manifest를 검사하는가
- R1 preview fail-closed 4 blocker와 count 재현
- Rust/Node dependency license metadata 집계와 asset hashes 재계산
- T5G/W1C2/R10 ancestry, 94-path overlap 재계산
- product/SSOT/public SPEC/GitHub diff 0

## verdict boundary

PASS는 owner-binding/read-only audit/checker/research packet에만 해당한다. Apache-2.0 final license, rights clearance, exact integration commit, public-source self-containment, GitHub private conversion, new repository, push, release를 승인하지 않는다.
