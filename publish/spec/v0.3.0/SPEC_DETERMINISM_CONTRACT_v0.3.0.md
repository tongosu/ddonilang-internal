# 결정론 계약 — Language SPEC v0.3.0

> 상태: current public pre-release draft / owner-approved 2026-07-26
> trace: Language SPEC `v0.3.0` ← internal current SSOT `v24.17.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: docs-first canonical과 parser/runtime 제품 상태를 구분한다.

## 이름·순서·source chain

- 공개 의미 이름은 DDN에서 온다.
- 값꾸러미 필드, 계열, 범례, 표 열은 작성·선택 순서를 보존한다.
- 실행 map의 열쇠 정렬을 정본 순서로 쓰지 않는다.
- 모든 보기 의미는 DDN 또는 잠긴 표준 가지에서 committed trace까지 source chain을 가진다.

## 희소 표본

- `present`, `gap`, `missing`, `pruned`를 구분한다.
- `missing`은 `#계산실패`, `#원천없음`, `#기록손상` 이유를 가진다.
- 발행 기회 없음은 표본이 아니다.
- gap·missing을 가로질러 선이나 자취를 보간하지 않는다.

## 관계와 풀이

- 보기 관계 깊이는 32이고 순환은 금지한다.
- 이 안전 한도는 사용자가 끌 수 없다.
- 무제한 backtracking을 금지한다.
- SolvePlan은 후보 공간·순서·상한·실패 이유를 봉인한다.

## 표준과 사용자 경로

표준 보기·모양·장면과 사용자 복제본은 같은 일반 composition 경로를 사용한다.
표준 전용 숨은 renderer 권한을 금지한다.
