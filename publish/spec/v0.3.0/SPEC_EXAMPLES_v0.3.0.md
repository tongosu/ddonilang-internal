# 정본 예제 — Language SPEC v0.3.0

> 상태: current public pre-release draft / owner-approved 2026-07-26
> trace: Language SPEC `v0.3.0` ← internal current SSOT `v24.17.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: docs-first canonical과 parser/runtime 제품 상태를 구분한다.

## 공개 관찰과 시간선

```ddn
(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.
각도시간선 <- (세로=#각도) 표준보기.시간선.
```

## 이름씨와 계약

```ddn
(중심:점2, 반지름:길이)인 원:이름씨 = {
  먼저 { 반지름 > 0@m } 아니면 물림.
}.

공 <- (중심=원점, 반지름=2@m)인 원.
```

## 장면과 그래프

```ddn
(시간: 시간, 각도: 각도) 보임.
진자보기 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.
```

이 예제는 docs-first 정본 표면이다. 현재 제품 실행 가능 여부는 지원 범위표를 따른다.
