# Public/private boundary audit

## 채택할 3층 모델

```text
INTERNAL_WORK
    -> deterministic allowlist projection
PUBLIC_SOURCE
    -> sealed reproducible build
RELEASE_ARTIFACT
```

Public Projection은 저장소를 하나 더 손으로 복사하는 작업이 아니라 INTERNAL_WORK commit과 projection policy/tool identity에서 PUBLIC_SOURCE tree를 계산하는 promotion process다.

## INTERNAL_WORK에 남길 것

- `docs/ssot/**` 전체
- `work/**`, 독립 검토, mutation/fault-injection 원장, AI packet
- 운영 DB, profile, local build/out/target
- private research와 historical corpus
- release promotion evidence와 private operations
- 권리·보안 검토 전 asset

## PUBLIC_SOURCE 후보

- Rust product crates: core/lang/numeric/proof/symbolic/tool
- public CLI source: 최종적으로 `cli` 명칭과 단일 public frontdoor로 설명
- Workbench/셈그림 product source와 user examples
- Language SPEC public current와 공개 문서
- 최소 public conformance suite
- 재현 build script와 public-safe config

폴더 전체를 공개/비공개로 판정하지 않는다. manifest의 각 포함 단위는 PRODUCT_SOURCE, BUILD_REQUIRED, PUBLIC_CONFORMANCE, USER_EXAMPLE, PUBLIC_DOC 역할을 가진다.

## RELEASE_ARTIFACT

공식 공개 release는 PUBLIC_SOURCE만으로 재현돼야 한다. INTERNAL_WORK에서 직접 만든 artifact는 experimental/internal artifact이며 공식 공개 release와 같은 identity를 주장하지 않는다.

## R1에서 확인된 경계 위반 후보

- test-only `include_str!`가 internal `pack` 또는 `docs/ssot` fixture를 compile-time에 요구
- `.cargo/config.toml`과 root project config에 내부 절대 경로
- 공개 checker 일부가 내부 SSOT cleanliness를 검사
- public conformance allowlist의 transitive dependency closure 미완성
- 공개 license/security/support ownership 미정

이 항목은 기존 내부 소스를 이동하거나 삭제해서 해결하지 않는다. 내부 path를 유지한 채 공개 전용 fixture/config/checker surface를 제품 계보에서 작게 정리한 뒤 projection allowlist를 갱신한다.
