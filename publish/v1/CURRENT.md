# 또니랑 V1 사용자 문서 — PRE_RELEASE

```text
DOCUMENTATION_TRACK_STATUS=PRE_RELEASE
PRODUCT_RELEASED=NO
EXTERNAL_USER_COUNT=0
SUPPORTED_FOR_V1_COUNT=0
PRODUCT_PASS_MEMBERSHIP_PENDING_COUNT=0
VERIFIED_PUBLIC_EXAMPLE_COUNT=0
```

이 문서는 또니랑 V1 제품의 사용자 문서 진입점이다. 현재는 출시 전 준비판이며, 설치 가능한 공식 V1 제품이나 일반 사용자 지원을 선언하지 않는다.

## 현재 권위 경계

- 내부 의미 정본: SSOT `v25.22.0 / RD-001~469`
- 공개 언어 계약: Language SPEC `v0.6.0`
- V1 제품 지원범위: 아직 확정되지 않음
- V1 membership: 아직 배정되지 않음
- 제품 준비도: `UNCLAIMABLE`

Language SPEC에 설명된 표면이 곧바로 V1 제품에서 실행된다는 뜻은 아니다. 실제 제품 지원 여부는 [SUPPORT_MATRIX.md](./SUPPORT_MATRIX.md)의 상태만 따른다.

제품 구현이나 제한된 독립 PASS가 존재해도 V1 membership이 승인되지 않았다면
`SUPPORTED_FOR_V1`이 아니다. 현재 공개 행 중 required product gate 전체를 통과하고
membership만 기다리는 행은 0개이며, 제한된 근거는 지원 상태와 분리해 표시한다.

## 읽는 순서

1. [QUICKSTART.md](./QUICKSTART.md) — 현재 이용 가능 여부와 시작 관문
2. [SUPPORT_MATRIX.md](./SUPPORT_MATRIX.md) — 표면별 제품 지원 상태
3. [LANGUAGE_GUIDE.md](./LANGUAGE_GUIDE.md) — V1-Core 후보 개요
4. [DETERMINISM_AND_PROJECTS.md](./DETERMINISM_AND_PROJECTS.md) — 결정성·프로젝트 사용 원칙
5. [ROADMAP.md](./ROADMAP.md) — 공개 capability 방향

## 출시 전 원칙

- 독립 제품 PASS와 V1 membership 승인 없이 어떤 표면도 `SUPPORTED_FOR_V1`로 표시하지 않는다.
- `PRODUCT_PASS_MEMBERSHIP_PENDING`은 required product gate의 fixed-target 독립 PASS가 있지만
  V1 membership만 미승인인 경우에만 사용하며, 현재 적용 행은 0개다.
- 문서에 실행 예제를 넣으려면 공식 parser/frontdoor에서 원문 그대로 실행된 고정 근거가 있어야 한다.
- SSOT·Language SPEC·제품 구현이 충돌하면 이 문서가 의미를 새로 만들거나 충돌을 숨기지 않는다.
