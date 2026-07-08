# KO_COMMON_PROMOTION_READINESS_AUDIT_V1_20260707

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 분류: AUDIT / KO_COMMON / DIALECT / PROMOTION_READINESS
- 기준: `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706` P6-G1
- 상태: 실측 감사. registry 승격 아님, `docs/ssot/**` 수정 없음, closure 주장 없음

## 0. 결론

`ko-common`은 설계 필요성과 방향이 충분히 반복 제안되어 있다. 하지만 T1 승격을 말하려면 네 조건을 분리해서 봐야 한다.

현재 저장소에는 교착어 AST 동치 pack과 dialect smoke pack이 있어 언어 확장 방향의 증빙은 강하다. 그러나 `ko-common` 자체의 승격 조건인 `core_keyword_matrix`, `josa_role_matrix`, `roundtrip golden`, `native 확인`은 아직 하나의 실측 산출물로 닫히지 않았다.

## 1. 승격 4조건 실측

| 조건 | 현재 상태 | 판정 | 다음 작업 |
|---|---|---|---|
| `core_keyword_matrix` | 여러 proposal에서 필요성이 언급됨. authoritative matrix 파일은 이번 감사에서 확인하지 못함 | 미충족 | matrix 후보 위치 확정, core keyword coverage 산출 |
| `josa_role_matrix` | 교착어 AST pack이 조사/핀 경계 일부를 검증함. ko-common 전용 role matrix는 별도 필요 | 부분 | 한국어 상용 조사/정본 조사/핀 역할 대응표 작성 |
| roundtrip golden | `paper1_canonize_agglutinative_ast_*`, `lang_dialect_smoke_v1`, `dialect_builtin_equiv_v1` 존재 | 부분 | ko-common 입력 별칭만 대상으로 roundtrip golden 분리 |
| native 확인 | 문서상 native review 완료 증빙을 확인하지 못함 | 미충족 | 한국어 사용자 1~2인의 용어 자연성 확인 기록 필요 |

## 2. 혼동하면 안 되는 증빙

| 증빙 | 말할 수 있는 것 | 말하면 안 되는 것 |
|---|---|---|
| `paper1_canonize_agglutinative_ast_v2` | 조사/어순/핀 고정이 AST 정본화로 수렴할 수 있음 | ko-common T1 승격 완료 |
| `lang_dialect_smoke_v1` | 기본 dialect smoke가 존재함 | ko-common 상용어 coverage 완료 |
| `dialect_builtin_equiv_v1` | builtin equiv 검증 축이 있음 | 한국어 상용 별칭층 전체 완료 |
| ko-common 관련 proposals | 설계 방향과 필요성이 정리됨 | registry 등록 또는 native 검토 완료 |

## 3. 권고 pack 후보

Pack ID: `ko_common_promotion_measurement_v1`

최소 파일:

| 파일 | 목적 |
|---|---|
| `core_keyword_matrix.detjson` | 정본 키워드와 ko-common 후보 대응 |
| `josa_role_matrix.detjson` | 조사/핀/역할 대응 |
| `roundtrip_cases/*.ddn` | ko-common 입력 후보 |
| `expected/*.canon.ddn` | 정본화 결과 |
| `native_review.detjson` | 검토자, 날짜, 항목별 자연성 판정 |

## 4. 승격 전 문구

권장:

- "`ko-common`은 한국어 상용 별칭층 후보이며, 승격 조건을 실측 중이다."
- "교착어 AST 동치 증빙은 존재하지만, ko-common registry 승격과는 별도다."

비권장:

- "`ko-common` T1이 완료됐다."
- "교착어권 국제 표면이 완성됐다."
- "native review가 끝났다."

## 5. 다음 작업

1. `ko_common_promotion_measurement_v1` pack skeleton 작성
2. core keyword 30개 안팎의 matrix 후보 작성
3. 조사/역할 10~15개 matrix 후보 작성
4. roundtrip golden 최소 9개 작성
5. native review 기록 1차 수집
