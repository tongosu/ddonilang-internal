# Targeted independent review request

## reviewer scope

R1의 제품 기능을 검토하는 것이 아니라 다음을 독립 검토한다.

1. source commit과 projection manifest/tool identity
2. A/B output tree raw identity
3. excluded internal classes가 output에 없는지
4. role별 allowlist가 실제 파일과 일치하는지
5. cargo build PASS와 unit-test fixture fail-closed 재현
6. public conformance transitive closure 누락 18경로 재계산
7. absolute internal path와 facade/license/security gap
8. `905efb4a...`가 release baseline으로 승격되지 않았는지
9. shared dirty root, SSOT, public SPEC, product, GitHub가 불변인지

## allowed verdict

```text
PASS
PASS_WITH_FOLLOW_UP
REWORK_REQUIRED
FAIL
```

PASS는 R1 projection/audit 자체에만 해당하며 PUBLICATION_READY, release baseline, license, GitHub visibility/push를 승인하지 않는다.
