# W1-C2 I1 internal typed identity model

이 문서는 public syntax나 stable wire가 아닌 제품 내부 candidate identity 경계를 기록한다.

| 축 | 정본 입력 | 비identity |
|---|---|---|
| ProviderDeclarationIdentity | module, declaration semantic, body semantic | source span, 선언 순서 |
| ProviderOwnerIdentity | owner space, owner instance | worker/vector order |
| ProviderRegistrationIdentity | declaration, owner, registration semantic | reachability path |
| ExecutionInstanceIdentity | execution semantic identity | worker arrival |
| DeliveryOccurrenceIdentity | execution identity, occurrence semantic identity | nested parent dedup set |

기존 `ProviderIdentity`는 W1-C1 내부 provider 의미 key로 보존한다. 새 다섯 타입은 이를 stable wire로 재정의하지 않으며 각각 별도 opaque candidate domain을 사용한다. body 변경·owner 변경·registration 변경·execution 변경·occurrence 변경은 identity-bearing이고, source span과 worker permutation은 아니다.

상태: `PRODUCT_INTERNAL_TYPED_LANDED`, `STABLE_PROVIDER_IDENTITY_WIRE_OPEN`.
