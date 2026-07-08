# PROPOSAL_PRE_RELEASE_FREEZE_SWEEP_AND_DAYRUN_INTAKE_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 분류: PROPOSAL / INTAKE / PRE_RELEASE_FREEZE / DAYRUN / AI_BETA
- 상태: 사용자 메시지 요지 보존 및 실행 분기. `docs/ssot/**` 수정 없음, parser/runtime 변경 없음, closure 주장 없음
- 기준: 2026-07-07 사용자 전달 요약(발표 전 동결 전략, AI 닫힌 베타, 지시문 12~16, 하루치 목표 지시서)

## 0. 결론

전략은 타당하다. 발표 뒤에 문법 표면, 정본 출력, wire schema, `state_hash` 산식, 오류 코드가 바뀌면 사용자 코드와 기록이 깨진다. 따라서 발표 전에는 호환을 깨는 설계 결함을 과하게 훑고, 발표 후에는 additive 보완만 허용하는 운영 원칙이 맞다.

다만 현재 Codex가 받은 것은 지시문 12~16과 DAYRUN의 "요약"이다. 실제 전문이 아직 저장소에 없으므로, 지금 할 일은 두 갈래다.

1. 요약에서 확정 가능한 운영 경계와 실행 순서를 보존한다.
2. 전문 없이는 과잉 실행이 될 수 있는 항목을 질문 큐로 보류한다.

## 1. 발표 전 동결 원칙

판정 기준은 하나다. 바뀌면 사용자 코드·기록·도구 의존성이 깨지는가.

| 분류 | 발표 전 완결 필요 | 발표 후 보완 가능 |
|---|---|---|
| 문법/의미 | 문법 표면, 의미, 예약어, 문법 공간 예약 | additive 새 표면, 새 표준팩 |
| 저장/재현 | 정본화기 출력, `state_hash` 산식, replay 영향 schema | 새 view/export, 성능 개선 |
| wire/API | detjson wire schema, 스키마 버전 협상, 오류 코드 체계 | v0.x add-only field |
| 제품성 | 발표 범위의 golden coverage, AGE gate | 진단 문구 개선, 구현 완성도 |

## 2. 마지막 동결 스윕 체크리스트

| 항목 | Codex 실측 가능성 | 산출물 |
|---|---:|---|
| 예약어 선점 | 가능 | 후보 예약어 목록, 현재 식별자 충돌 검색 결과 |
| 문법 공간 예약 | 부분 가능 | `#/@/~` 등 미사용 형태의 현재 허용/거부 조사표 |
| 오류 코드 네임스페이스 | 가능 | `E_*`/`W_*` 범주별 inventory와 중복/혼선 표 |
| 스키마 버전 협상 | 가능 | 주요 detjson schema별 add/ignore/error/convert 규칙 표 |
| 모듈/import 표면 | 부분 가능 | `프로젝트{}`/가지 경로/미완 gate 노출 여부 표 |
| 정본 출력 golden coverage | 가능 | 발표 범위 표면별 canon/golden coverage 표 |

## 3. 지시문 12~16 intake

| 지시문 | 주체 | 요지 | 현재 Codex 판단 |
|---|---|---|---|
| 12 | Codex | 오늘 산출물 8건의 SSOT 패치 초안, OI 일괄 등록 초안, 발표 전 동결 스윕 실측, pack ID 중복 검사 | 전문 필요. 단, 동결 스윕 실측은 Codex가 바로 수행 가능 |
| 13 | Claude Code | 경계 준수, 주장 등급, 용어 drift, 교차 참조, SSOT 권위 순서 감사 | Codex가 직접 수행할 항목 아님. 감사 입력물만 준비 |
| 14 | Codex/베타 | AI 닫힌 베타 Round 0 준비 및 CLI 기반 실행 가능 | 지식 격리 때문에 현재 세션에서 베타 사용자 실행은 금지. 번들/fixture 준비는 가능 |
| 15 | Codex 개발 | Tier A는 지금 가능, Tier B는 SSOT 병합 뒤 해금 | Tier A 중 perf baseline/LLM corpus는 이미 처리됨 |
| 16 | Claude Code | 설계 6건을 구현 등급 ANNEX로 정교화 | Codex가 직접 확정하지 않음. ANNEX 입력/질문 큐는 준비 가능 |

## 4. 지시문 15 Tier A 상태

| Tier A 항목 | 상태 | 근거/다음 |
|---|---|---|
| perf 벤치 러너 | 처리됨 | `pack/perf_baseline_v1`, `tools/scripts/run_perf_baseline_v1.py` |
| LLM 코퍼스 추출기 | 처리됨 | `pack/llm_corpus_extract_deterministic_v1`, `tools/extract_llm_corpus_v1.py` |
| 적분기 pack | 미착수 | `P5물리-G1` 남은 항목 |
| 경제 model-first 3종 | 미착수 | `P5경제-G1` 남은 항목 |
| 설정해시 도구층 프로토타입 | 미착수 | runtime/state_hash 비접촉 checker로만 가능 |
| 예약어 lint 도구 | 미착수 | 동결 스윕과 연결 |
| 베타 번들 + 오류 fixture | 미착수 | 지식 격리용 공개자료 번들 필요 |

## 5. Tier B 잠금

다음 항목은 지시문 12 -> 13 -> 사용자 병합 확인 전까지 구현 착수 금지다.

- `step_record v0.2` runtime/wire hard-cut
- `시앗묶음`
- `설정.누리` key hard-cut
- 누리 큰마디 위상표 코드화
- 설정해시가 실제 runtime replay 검증에 참여하는 변경
- 새 문법 표면/예약어의 parser 승격

## 6. DAYRUN 요지

현재 받은 DAYRUN은 전문이 아니라 운영 원칙 요약이다.

확정 가능한 운영 규칙:

1. G1 논의 유실 방지가 최우선이다.
2. 단계 나열보다 목표와 성공 기준을 준다.
3. 방법은 Codex가 자율 판단하되, 문법 표면·정본 이름·스키마 확정은 질문 큐로 넘긴다.
4. 예상보다 오래 걸리면 부분으로 기록하고 다음 목표로 이동한다.
5. 현재 세션은 저장소 지식이 있으므로 닫힌 베타 사용자 역할을 직접 수행하지 않는다. 준비까지만 한다.
6. 마감 보고는 결과, 질문 큐, 발견한 문제, 다음 날 추천 착수점으로 한다.

전문 필요 항목:

- G1~G7의 정확한 목표명
- 각 목표의 성공 기준
- 목표별 필수 검증 배터리
- 질문 큐 형식
- 베타 Round 0 과제 6종의 실제 텍스트

## 7. Codex 다음 권고

전문이 오기 전에도 안전하게 할 수 있는 다음 작업은 아래 순서다.

1. 발표 전 동결 스윕 실측 초안: 예약어 후보, 문법 공간, E-code inventory, schema version policy, golden coverage.
2. 지시문 15 Tier A 남은 구현: 적분기 pack, 경제 model-first 3종.
3. 설정해시 도구층 프로토타입: runtime 비접촉 hash preview/checker.
4. 베타 번들 준비: 공개자료-only context bundle과 오류 fixture 후보.

단, SSOT 패치 초안이나 parser/runtime hard-cut은 지시문 12 전문과 사용자 병합 결정 없이는 하지 않는다.
