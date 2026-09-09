# DDN-V1-EX01 공개 제품 예제 membership 후보 감사

```text
TASK: DDN-V1-EX01-PUBLIC-EXAMPLE-MEMBERSHIP-AUDIT-I1
BASELINE: 07c0ba1f21c047f8339334d1a4191f0bf6ee4f1a
LIVE_INTERNAL_SSOT: v25.15.0
PUBLIC_LANGUAGE_SPEC: v0.5.0
AUDIT_ONLY: YES
RELEASE_MEMBERSHIP_LANDED: 0
PRODUCT_IMPLEMENTATION: NOT_STARTED
```

목적은 `publish/spec`의 문서 예제, 내부 pack fixture, Workbench lesson을 하나의
“실행 가능한 공개 예제”로 잘못 묶지 않고, 첫 V1 사용자 workflow에 필요한 migration
후보를 실제 제품 parser 결과와 권리 경계로 분류하는 것이다.

핵심 결과:

- bounded 후보 15개
- public SPEC v0.5.0 docs-first 예제 7개
- pre-V25 parser 통과 6개
- V25 parser 통과 1개: PC01 positive
- 양쪽 parser 모두 실패 8개
- 1차 migration 후보 4개: PC01, Hello, current grid, Basic Tensor
- 권리와 독립검토까지 닫힌 release member 0개

기계 재현:

```powershell
python tools/generate_v1_ex01_public_example_membership_audit_i1.py
python tests/run_v1_ex01_public_example_membership_audit_i1.py
cargo test -p ddonirang-tool --test v1_ex01_public_example_epoch_inventory --offline --locked -- --nocapture
```

