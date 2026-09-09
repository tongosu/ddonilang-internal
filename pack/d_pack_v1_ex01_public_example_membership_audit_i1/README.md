# D-PACK-V1-EX01-PUBLIC-EXAMPLE-MEMBERSHIP-AUDIT-I1

공개 문서 예제, 내부 conformance fixture, Workbench lesson을 하나의 제품 PASS로
섞지 않고 실제 parser 도달성·권리·migration 후보를 분리한다.

```powershell
python tools/generate_v1_ex01_public_example_membership_audit_i1.py
python tests/run_v1_ex01_public_example_membership_audit_i1.py
cargo test -p ddonirang-tool --test v1_ex01_public_example_epoch_inventory --offline --locked -- --nocapture
```

이 팩은 제품 구현, rights closure, 공개 복사, V1 release membership을 승인하지 않는다.

