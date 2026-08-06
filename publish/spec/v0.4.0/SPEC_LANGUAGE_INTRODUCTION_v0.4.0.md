# 또니랑 언어 소개 — Language SPEC v0.4.0 공개판

> 상태: `public current / owner-approved / docs-first / product-open`
> trace: Language SPEC `v0.4.0` public current ← independently reviewed `v0.4.0-candidate` ← internal live SSOT `v24.22.1`
> 이전 공개판: Language SPEC `v0.3.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 정본과 parser/runtime/default-product 지원을 분리한다.

## 이 공개판이 하는 일

이 공개판은 v0.3.0 뒤에 내부 SSOT RD-043~099의 승인 의미를 공개 독자가
읽을 수 있는 형태로 투영한다. v0.3.0의 공개 관찰·이름씨·계약·표준 보기
방향은 계승하고, 값·실패·참조·수·글·함수·모듈의 의미 계약을 보강한다.

정본화된 문법이 제품에서 실행된다는 뜻은 아니다. 각 표면은
`SPEC_STABLE_SUPPORT_SURFACE_v0.4.0.md`의 제품 상태를 함께 읽어야 한다.

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
