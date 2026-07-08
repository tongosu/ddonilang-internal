# DIAG_THREE_LAYER_MESSAGE_AUDIT_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 분류: AUDIT / DIAGNOSTIC / EDUCATION_G1
- 기준: `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706` P4-G1
- 상태: 감사 및 문구 사전 초안. 메시지 실변경 없음, parser/runtime 변경 없음, closure 주장 없음

## 0. 결론

현재 진단 체계는 fix-it payload와 스키마 검증이 이미 있다. 하지만 교육 G1이 요구하는 3층 메시지, 즉 `무엇이 잘못됐나 / 어디서 잘못됐나 / 어떻게 고치나`를 초심자 관점으로 일관 채점하는 계약은 아직 별도 산출물로 닫히지 않았다.

따라서 다음 단계는 메시지 본문을 바로 바꾸는 것이 아니라, 대표 E-code 20종에 대해 3층 충족 여부를 채점하고 초심자 문구 사전 초안을 golden 대상으로 올리는 것이다.

## 1. 평가 기준

| 층 | 기준 | 판정 |
|---|---|---|
| 무엇 | 오류 원인을 한 문장으로 말한다 | `있음/부분/없음` |
| 어디서 | 파일, 줄, 열 또는 문제 코드 조각을 준다 | `있음/부분/없음` |
| 어떻게 | fix-it 또는 사람이 따라 할 수정 방향을 준다 | `있음/부분/없음` |

## 2. 현재 강점

| 근거 | 내용 |
|---|---|
| `pack/diag_fixit_coverage_v1` | legacy term, header colon, 짜임 alias, grouped value, 괄호/중괄호 누락 fix-it coverage |
| `pack/diag_fixit_json_schema_v1` | fix-it JSON schema와 빈 결과/성공 경로 검증 |
| `studio_diagnostic_fixit_*` packs | Studio 쪽 fix-it preview/integration 증빙 |

## 3. 대표 E-code 20종 채점

| code | 무엇 | 어디서 | 어떻게 | 비고 |
|---|---|---|---|---|
| `E_BLOCK_HEADER_COLON_FORBIDDEN` | 부분 | 있음 | 있음 | fix-it 있음. 초심자 문구는 보강 필요 |
| `E_CANON_MAEGIM_GROUPED_VALUE_REQUIRED` | 부분 | 부분 | 있음 | 실제 error code와 fix-it code 분리 정리 필요 |
| `E_PARSE_EXPECTED_RBRACE` | 부분 | 있음 | 있음 | 닫는 `}` 삽입 제안 있음 |
| `E_PARSE_EXPECTED_RPAREN` | 부분 | 있음 | 있음 | 닫는 `)` 삽입 제안 있음 |
| `E_PARSE_MAEGIM_GROUPED_VALUE_REQUIRED` | 부분 | 부분 | 있음 | grouped value 설명 필요 |
| `E_EXEC_ENUM_INVALID` | 부분 | 부분 | 없음 | 허용 enum 목록 안내 필요 |
| `E_EXEC_POLICY_DUPLICATE` | 부분 | 부분 | 없음 | 중복 선언 제거 안내 필요 |
| `E_EFFECT_IN_STRICT_MODE` | 부분 | 부분 | 없음 | strict mode와 effect 관계 설명 필요 |
| `E_EFFECT_IN_ISOLATED_MODE` | 부분 | 부분 | 없음 | isolated mode에서 금지된 효과 안내 필요 |
| `E_EFFECT_SURFACE_ALIAS_FORBIDDEN` | 부분 | 부분 | 없음 | 정본 표면으로 바꾸는 제안 필요 |
| `E_OPEN_DENIED` | 있음 | 부분 | 부분 | policy allowlist 수정 방향 필요 |
| `E_OPEN_IO` | 있음 | 부분 | 없음 | 파일 접근 실패와 정책 실패 구분 필요 |
| `E_OPEN_LOG_MISSING` | 있음 | 부분 | 부분 | replay log 경로 안내 필요 |
| `E_OPEN_LOG_PARSE` | 있음 | 부분 | 없음 | log 형식/재생성 안내 필요 |
| `E_OPEN_LOG_TAMPER` | 있음 | 부분 | 부분 | replay 불일치와 재기록 절차 설명 필요 |
| `E_OPEN_REPLAY_MISS` | 있음 | 부분 | 부분 | record/replay 차이 안내 필요 |
| `E_GUSEONG_INSTANCE_DUP` | 부분 | 부분 | 없음 | 같은 이름의 구성요소 이름 변경 안내 필요 |
| `E_GUSEONG_INSTANCE_UNDECLARED` | 부분 | 부분 | 없음 | 선언 누락 위치와 선언 예시 필요 |
| `E_GUSEONG_LINK_CYCLE` | 부분 | 부분 | 없음 | 순환 연결 끊기 안내 필요 |
| `E_PARSE_CALL_JOSA_AMBIGUOUS` | 있음 | 부분 | 부분 | `값:핀` 고정 예시를 fix-it 후보로 연결 필요 |

## 4. 초안 산출물

동일 폴더에 `DIAG_THREE_LAYER_BEGINNER_DICTIONARY_DRAFT_V1_20260707.detjson`를 추가했다. 이 파일은 문구 실변경이 아니라 `diag_three_layer_message_v1` pack 후보의 입력 초안이다.

## 5. 다음 작업

1. `diag_three_layer_message_v1` pack skeleton 생성
2. 위 20종을 golden dictionary로 고정
3. 실제 CLI/Studio 메시지와 dictionary 간 drift 검사
4. SSOT 오너 승인 후 메시지 본문 반영

## 6. 비주장

- 이번 감사는 진단 품질이 닫혔다고 주장하지 않는다.
- 메시지 본문을 바꾸지 않았다.
- `docs/ssot/**`를 수정하지 않았다.
