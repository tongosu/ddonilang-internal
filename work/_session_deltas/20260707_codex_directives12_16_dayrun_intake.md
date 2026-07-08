# 20260707 Codex session delta: 지시문 12~16 및 DAYRUN intake

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 범위: 사용자 전달 요약(발표 전 동결 전략, AI 닫힌 베타, 지시문 12~16, DAYRUN)
- SSOT 수정: 없음
- parser/runtime 변경: 없음
- closure 주장: 없음

## 받은 내용 요지

- 발표 후 문법 변경은 사용자 코드와 기록을 깨므로, 발표 전 동결 스윕이 필요하다.
- 동결 대상은 문법 표면/의미, 정본 출력, `state_hash`, detjson wire schema, 오류 코드 체계, 예약어다.
- 발표 후 보완은 additive 구현, 성능, 표준팩, 진단 문구, 새 기능 중심으로 제한한다.
- 마지막 검토 대상은 예약어 선점, 문법 공간 예약, 오류 코드 namespace, schema version negotiation, 모듈/import gate, 정본 출력 golden coverage다.
- AI 닫힌 베타는 지식 격리 원칙 때문에 현재 Codex 세션에서 직접 베타 사용자 역할을 해서는 안 된다.
- 지시문 12~16은 설계/감사/실행 주체를 분리한다.
- 지시문 15 Tier A는 지금 가능한 도구층·pack이고, Tier B는 SSOT 병합 뒤 해금이다.

## 저장한 산출물

- `docs/context/proposals/PROPOSAL_PRE_RELEASE_FREEZE_SWEEP_AND_DAYRUN_INTAKE_V1_20260707.md`

## 현재 상태

- 지시문 15 Tier A 중 `perf 벤치 러너`와 `LLM 코퍼스 추출기`는 이미 처리됨.
- 남은 Tier A: 적분기 pack, 경제 model-first 3종, 설정해시 도구층 프로토타입, 예약어 lint 도구, 베타 번들+오류 fixture.
- 지시문 12~16과 DAYRUN 전문은 아직 저장소에 없음. 현재 문서는 요지 보존과 실행 분기까지만 한다.

## 질문 큐

1. 지시문 12~16 전문을 그대로 Codex에 붙여 넣을지, 아니면 Claude Code가 저장소 파일로 먼저 남길지 결정 필요.
2. DAYRUN G1~G7의 정확한 목표명과 성공 기준 전문이 필요하다.
3. 발표 전 동결 스윕에서 예약어 후보를 "reserved proposal"까지만 할지, lint 도구까지 바로 만들지 결정 필요.

## 다음 권고

전문이 오기 전 안전한 다음 작업은 발표 전 동결 스윕 실측 초안이다. 이 작업은 SSOT를 직접 고치지 않고 repository inventory만 만들 수 있다.
