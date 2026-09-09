# 호환성·비주장 정책 — Language SPEC v0.2.0

> 상태: owner-approved public projection candidate / pre-release / not yet published
> trace: Language SPEC `v0.2.0` ← SSOT `v24.15.0` administrator candidate
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: G7과 함수 타입 `-->`는 설계 확정, K0~K7·A1 제품 증거는 아직 OPEN이다.


## v0.x 정책

- v0.2.0은 출시 전 공개 초안이며 장기 호환성 약속 전 단계다.
- v0.x에서는 근거와 migration 기록이 있으면 문법·API·stdlib 이름이 바뀔 수 있다.
- Language SPEC v1.0.0이 첫 장기 호환성 약속 시점이다.
- v0.1.0과 v0.1.1 문서·seal은 byte-identical 보존한다.

## 이번 판에서 하지 않는 약속

- G7 parser/runtime/CLI/WASM 구현 완료나 production readiness.
- `T/U/V` 입력 호환. 이 별칭은 처음부터 만들지 않는다.
- 함수 타입 `-->`의 제품 구현 완료와 일반 함수값 전체 계약 완료.
- dynamic interface/typeclass 탐색, runtime reflection, 임의 generic 고급 기능.
- M3 stable 문법·API·artifact 이름·marketplace 지원.
- `지음자취·지음풀이·뿌리자취·지은씨앗·덧지음셈씨`의 stable wire/API 승격.

`씨앗지음`은 메타프로그래밍 연구 전체 표시명이고 `지음증거`는 M2 증거 묶음이다.
M3-실험 0은 M1/M2 공통 도구층을 사용자 생성기 한 세로줄로 검증하는 계획일 뿐이다.
comment-canon parity가 통과한 frontdoor에서만 주석·공백 변경의 기존 승인을 재사용한다.
