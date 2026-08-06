# 또니랑 언어 소개 — Language SPEC v0.5.0 후보

> 상태: `public candidate / independent review required / not current / docs-first / product-open`
> trace: Language SPEC `v0.5.0` candidate ← internal live SSOT `v24.24.1`
> 현 공개판: Language SPEC `v0.4.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 후보와 parser/runtime/default-product 지원을 분리한다.

## 이 후보가 하는 일

이 후보는 public current v0.4.0의 RD-001~099 투영을 계승하고, internal live
SSOT v24.24.1의 RD-100~122를 공개 독자가 읽을 수 있게 보강한다.

- 지식 장면·배움 합성은 표준과 사용자가 같은 DDN·artifact·lock 경로를 쓴다.
- `보임`은 공개 관찰이며 그래프를 추정하지 않는다. 명시 보기가 없으면
  작성·발행 순서의 결과표가 기본이다.
- 공개 `모형 {}`와 `모형값`, 닫힌 `::` 성질, 초기화·출력·사건·`잇기`·
  일반 `풀기` 문법을 docs-first 계약으로 공개한다.

정확한 그래프 module/export 이름, 접근성 schema, 효과·외부 계산 ABI와
제품 parser/runtime 지원은 OPEN이다. 각 표면은
`SPEC_STABLE_SUPPORT_SURFACE_v0.5.0.md`의 상태와 함께 읽는다.

## 언어와 생태계의 네 층

1. 언어 핵심: 원자값, collection, 이름씨·고름씨, `T?`, `맺음`, 씨자리,
   바이트열, 단위량, 정체성 참조값.
2. 표준 가지: 범위·표·schema·시계열·벡터·행렬·통계·날짜·시간·기하·
   변환·색·그림·격자·graph.
3. 표준 모듬: 검증된 workflow와 교과·도메인 조립.
4. 예제·장면틀: 같은 공개 DDN 경로로 만든 복제 가능한 완성물.

표준 항목과 사용자 항목은 같은 구성 원리를 사용한다. 표준만 쓸 수 있는
숨은 renderer·runtime 특권을 만들지 않는다.

## 공개 표면을 아직 정하지 않은 것

ModelDefinition·ModelInstance·SolveRecipe·RunRequest의 의미 분리는 정본이지만
공개 model·미분·event·합성·interpolation·distribution 문법은 OPEN이다.
영어 내부 객체명과 Sam→Iyagi→Nuri→Geoul→Bogae 다섯 층은 구현 설명이며
초보자 문법이 아니다.
