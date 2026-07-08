# OI_CANDIDATES_20260706_BUNDLE

- 작성: 2026-07-08 (Asia/Seoul)
- 성격: Open Issue 후보 일괄 등록 초안
- 기준: 2026-07-06~07 설정/누리/보개/7목적 논의
- 경계: SSOT 본문 직접 수정 아님

## 0. 상태 표기

| 상태 | 의미 |
|---|---|
| `register` | OI로 등록 권고 |
| `reserve` | 예약어/문법 공간으로만 선점 권고 |
| `evidence` | pack/report evidence 뒤 결정 |

## 1. 설정 OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-SETTINGS-NURI-KEYSET-01` | register | `설정.누리`가 세계 정체성 외에 규칙묶음/단위계/공간갈래까지 소유하는가 | identity + world-level default까지만 소유, 실행 정책은 `설정.실행` |
| `OI-SETTINGS-IYAGI-ENTRY-01` | register | `설정.이야기` 절을 지금 예약할 것인가 | 절 이름은 예약, runtime claim 없음 |
| `OI-SETTINGS-FLAT-COMPAT-01` | register | 기존 flat 설정 key를 어떤 호환 규칙으로 절 구조에 매핑할 것인가 | 입력 alias 허용, 정본 출력은 절 구조 |
| `OI-SETTINGS-RESULT-AFFECTING-CLASSIFIER-01` | register | key별 `결과영향/보기/메타/연구` 분류를 누가 소유하는가 | settings registry가 소유하고 `설정해시` 산식에서 참조 |
| `OI-SETTINGS-CONFIG-HASH-INPUT-01` | register | `설정해시` 입력에 문서/보기 metadata를 포함할 것인가 | 결과영향 key만 포함, 문서 metadata 제외 |
| `OI-SETTINGS-SEED-BAG-SURFACE-01` | reserve | `시앗묶음`을 정본 표면으로 선점할 것인가 | 예약어 선점, pack evidence 전 runtime claim 금지 |

## 2. 누리/마디 OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-SEULGI-JIYEONMADI-OWNERSHIP-01` | register | 슬기 지연마디 key가 `설정.슬기` 소유인지 `설정.실행` 소유인지 | `설정.슬기`가 policy, `설정.실행`이 madi timing |
| `OI-NURI-MADI-PHASE-OQ1-ORDER-01` | register | 임자 실행 순서는 파일 선언 순서인가 `agent_id` 사전순인가 | 파일 선언 순서 |
| `OI-NURI-MADI-PHASE-OQ2-FIXPOINT-01` | register | P2 병합은 1회 pass인가 fixpoint인가 | Gate0는 1회 pass, fixpoint는 고급 후보 |
| `OI-NURI-MADI-PHASE-OQ3-P2-OWNER-01` | register | `미루기`는 P2 병합 결과인가 P3 세계 갱신 결과인가 | P2 결과로 먼저 모델링 |
| `OI-NURI-MADI-PHASE-OQ4-EVERY-N-MADI-01` | register | `마다 n마디`가 reset/replay와 어떻게 상호작용하는가 | 큰마디 index 기준, reset 종류별 표 필요 |
| `OI-NURI-RESET-R1-NURIDASI-REAPPLY-SCOPE-01` | register | `누리다시` 때 설정/샘/슬기 snapshot을 어디까지 재적용하는가 | result-affecting settings만 재적용 |
| `OI-NURI-ACTION-MERGE-NAME-COLLISION-01` | register | `합치기갈래`와 `행동모음갈래` 중 어느 이름이 정본인가 | `행동모음갈래` 권고 |
| `OI-NURI-WRITE-CONFLICT-ERROR-01` | register | 상태 쓰기 경합 오류 코드를 확정할 것인가 | `E_MADI_WRITE_CONFLICT` 후보 |

## 3. 보개 OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-BOGAE-SELECTION-DUAL-PATH-01` | register | 보개 선택을 한국어 표면 이름과 pack id 두 층으로 둘 것인가 | 사용자 표면 이름 + `std_bogae_*` pack id 병행 |
| `OI-BOGAE-GRAPH2D-LOWERING-CONTRACT-01` | evidence | 그래프 lowering의 axis/series/missing/color 규칙을 어디까지 고정할 것인가 | `std_bogae_graph2d_v1` pack evidence로 고정 |
| `OI-BOGAE-MADANG-TRACK-V1-01` | evidence | 보개마당 트랙을 자막/해설/강조 3트랙으로 닫을 것인가 | scene snapshot schema smoke 후 결정 |
| `OI-BOGAE-STANDARD-PACK-MINSET-01` | evidence | Phase 1 최소 표준팩을 4종으로 닫을 것인가 | grid2d/graph2d/table/sim2d부터 |

## 4. 언어/방언/프로젝트 OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-DIALECT-SETTINGS-SECTION-ALIAS-COVERAGE-01` | register | 설정 절 이름의 영문/다언어 alias를 어디까지 허용할 것인가 | 입력 alias만, 정본 출력은 한국어 |
| `OI-PROJECT-DEFAULT-INHERITANCE-SCOPE-01` | register | 프로젝트 기본 설정이 파일별 설정에 어떻게 상속되는가 | 발표 전 범위 제외 또는 explicit override만 |
| `OI-MODULE-IMPORT-GATE-PRELAUNCH-01` | register | `프로젝트{}`/import 표면이 미완이면 어떻게 노출할 것인가 | `E_AGE_NOT_AVAILABLE`로 게이트 |

## 5. 발표 전 동결 OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-RESERVED-ENRICHMENT-SURFACES-01` | reserve | `가설`, `검산`, `단위 정의`, `말거리`, `~이름(...)`을 예약할 것인가 | 채택 여부와 무관하게 예약 검토 |
| `OI-SCHEMA-VERSION-NEGOTIATION-POLICY-01` | register | schema별 v0/v1/v2 읽기 규칙을 `무시/오류/변환` 중 무엇으로 둘 것인가 | 공개 schema는 기본 오류, 명시 adapter만 변환 |
| `OI-ERROR-CODE-NAMESPACE-01` | register | `E_*` namespace를 parser/runtime/contract/AGE gate로 나눌 것인가 | 접두 범주표 + 문구 golden |
| `OI-RESERVED-SYNTAX-QUIET-IDENTIFIER-01` | reserve | `#/@/~` 미사용 조합을 identifier로 조용히 허용할 것인가 | 발표 전 parser negative test 필요 |
| `OI-CANON-GOLDEN-COVERAGE-FREEZE-01` | evidence | 발표 범위 모든 표면이 정본 golden으로 덮였는가 | coverage report 필요 |

## 6. 7목적 evidence OI

| OI | 상태 | 질문 | 기본 권고 |
|---|---|---|---|
| `OI-SEVEN-AIGYM-VECTORIZED-CONSUMER-01` | evidence | 벡터화 rollout을 언어 표면이 아닌 consumer 층에서 닫을 것인가 | 새 문법 0, consumer API로 처리 |
| `OI-SEVEN-GAME-REALTIME-PERF-01` | evidence | 실시간 액션 게임 claim을 어떤 tick 기준으로 열 것인가 | perf baseline 뒤 결정 |
| `OI-SEVEN-EDU-WASM-GATE-01` | evidence | 교육 claim의 최소 전달층은 무엇인가 | WASM/놀이터 smoke가 필요 |
| `OI-SEVEN-AGGLUTINATIVE-NATIVE-REVIEW-01` | evidence | 교착어권 claim에 native review 몇 명이 필요한가 | 첫 언어 파일럿 2명 이상 |
| `OI-SEVEN-SEULGI-SURFACE-HARDCUT-01` | register | `두뇌/지연마디`를 언제 정본 승격할 것인가 | capability matrix closure 뒤 |

## 7. 우선순위

1. 발표 후 호환을 깨는 것: 예약어, schema 협상, E-code namespace, 정본 golden coverage.
2. 기록 재현성에 닿는 것: `설정해시`, `시앗묶음`, reset/replay 상호작용.
3. 사용자 생산성에 닿는 것: 보개 표준팩 minset, Graph2D lowering.
4. claim 품질에 닿는 것: 7목적 evidence OI.

