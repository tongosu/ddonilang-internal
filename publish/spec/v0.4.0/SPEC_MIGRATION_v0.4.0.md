# v0.3.0 → v0.4.0 공개판 이행 안내

> 상태: `public current / owner-approved / docs-first / product-open`
> trace: Language SPEC `v0.4.0` public current ← independently reviewed `v0.4.0-candidate` ← internal live SSOT `v24.22.1`
> 이전 공개판: Language SPEC `v0.3.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 정본과 parser/runtime/default-product 지원을 분리한다.

## 확정된 의미 이행

| 이전·실험 표면 | v0.4.0 정본 | 처리 |
|---|---|---|
| `#잘됨(값)` | `(T,E)맺음.$잘됨(값: 값)` | clean break; 옛 표면 제거 |
| `#안됨(이유)` | `(T,E)맺음.$안됨(이유: 이유)` | clean break; 옛 표면 제거 |
| `임자가리킴` | `(대상씨)가리킴` | history 이름 제거 |
| 원자와 갈래 모두 `#이름` | `#원자`, `고름씨.$갈래` | 값 범주 분리 |
| 옛 말결 `$이름` | `$!말결` | 한 호출 한정; no-op 금지 |
| `프로젝트 {}` | `얼개 {}` | canonical direction; 제품 이행 OPEN |
| 이름형 record의 작성 순서 equality | 필드 이름·값 equality | RD-090 의미로 교정 |
| `pack`·`묶음` 사용자 정본 | 값꾸러미 | 옛 별칭 비정본 |

## 자동으로 이행하지 않는 것

- 값과 참조의 `==`를 추측해서 `===`로 바꾸지 않는다.
- exact 수를 자동으로 `셈수`로 바꾸지 않는다.
- `없음`을 `맺음.$안됨`으로, 중첩 선택값을 평탄화하지 않는다.
- 위치형과 이름형 값꾸러미를 서로 변환하지 않는다.
- 가져온 가지·함수·solver 계약을 확인할 수 없으면 현재 구현으로 fallback하지 않는다.

## 제품 이행 전 확인표

1. P1 혼합·중복·필드 수 유실 수정과 CLI/WASM parity.
2. C-02 30식과 모든 정밀도 손실 경계 반올림 golden.
3. C-04 기호 가독성 corpus와 KS 12쌍 인간 낭독.
4. C-05 단일 public/export 표와 `얼개` clean-cut.
5. C-06 오류·debug 화면의 다섯 층 노출 한도.
6. exact wire·lock·migration·negative controls.

이 표가 닫히기 전에는 제품 source 일괄 rewrite, runtime 지원 또는 기본 제품
승격을 주장하지 않는다. public docs current와 제품 착지는 별도 상태다.
